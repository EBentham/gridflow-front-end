"""Execute each dataset page's demo notebook for real and commit its outputs.

Run with the gridflow_models interpreter (it has the ``gridflow_models``
kernel, nbclient, nbformat and PyYAML)::

    C:\\Users\\Bobbo\\OneDrive\\Desktop\\Python\\gridflow_models\\.venv\\Scripts\\python.exe \\
        scripts/run_notebooks.py [--dataset elexon/fuelhh ...] [--vault-path vault]

For every vault note on the new dataset template, the notebook is the setup
cell, ``data.<source>`` (the source's help card), then the note's
``page.notebook.cells``. They run top to bottom on the ``gridflow_models``
kernel against the local warehouse: read-only calls (``query``, ``sql``,
``head``, a plot), never ``refresh``, ``backfill`` or an ingest. Outputs are
stored as data, not HTML: the help card's verbs, a DataFrame's cells as pandas
printed them, text, and each plot as a PNG beside the JSON:

    site/hifi/data/notebooks/<vendor>/<dataset>.json
    site/hifi/data/notebooks/<vendor>/<dataset>-<n>.png

``gridflow-build`` renders the notebook drawer from these files and checks
their cell digest, so CI never needs the data or a kernel. A cell that raises
fails the run and writes nothing.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import html
import re
import struct
import sys
import time
from pathlib import Path
from typing import Any

import nbformat
from nbclient import NotebookClient

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from gridflow_front_end import artefacts
from gridflow_front_end.page_fields import parse_page_fields

SITE_DIR = REPO / "site" / "hifi"
READ_ONLY_VERBS = re.compile(r"\.(refresh|backfill|ingest|delete|drop|write)\s*\(")


def help_card(raw: str) -> dict[str, Any]:
    """The SourceClient help card: its verbs and one-liners in order, and its discovery footer.

    The header's dataset count is left off: it disagrees with ``list_datasets()``
    (a gridflow_models bug) and the page states no count.
    """
    rows = re.findall(r"flex:0 0 170px[^>]*>([^<]+)</div><div[^>]*>([^<]+)</div>", raw)
    foot = re.search(r"(Discover datasets:)\s*<code[^>]*>([^<]+)</code>", raw)
    if not rows or not foot:
        raise RuntimeError("the help card's HTML changed shape; update help_card()")
    return {
        "kind": "card",
        "rows": [[html.unescape(n), html.unescape(d)] for n, d in rows],
        "foot": [foot.group(1), html.unescape(foot.group(2))],
    }


def dataframe(raw: str) -> dict[str, Any]:
    """pandas' own ``to_html`` output, cell for cell."""
    head = re.findall(r"<th>(.*?)</th>", raw.split("</thead>")[0])
    body = raw.split("<tbody>")[1]
    index: list[str] = []
    cells: list[list[str]] = []
    for row in re.findall(r"<tr>(.*?)</tr>", body, flags=re.DOTALL):
        index.append(html.unescape(re.findall(r"<th>(.*?)</th>", row)[0]))
        cells.append([html.unescape(c) for c in re.findall(r"<td>(.*?)</td>", row)])
    return {
        "kind": "df",
        "columns": [html.unescape(h) for h in head],
        "index": index,
        "rows": cells,
    }


def png_size(data: bytes) -> tuple[int, int]:
    """Width and height from a PNG header."""
    w, h = struct.unpack(">II", data[16:24])
    return int(w), int(h)


def outputs(cell: Any, stem: str, images: dict[str, bytes]) -> list[dict[str, Any]]:
    """One executed cell's outputs as data; plot PNGs are collected into ``images``."""
    out: list[dict[str, Any]] = []
    for o in cell.outputs:
        if o.output_type == "error":
            raise RuntimeError(f"cell [{cell.execution_count}] raised {o.ename}: {o.evalue}")
        if o.output_type == "stream":
            if o.name == "stdout" and o.text.strip():
                out.append({"kind": "text", "text": o.text.rstrip()})
            continue
        data = o.get("data", {})
        if "image/png" in data:
            png = base64.b64decode(data["image/png"])
            name = f"{stem}-{cell.execution_count}.png"
            images[name] = png
            w, h = png_size(png)
            out.append({"kind": "image", "src": name, "width": w, "height": h})
        elif "text/html" in data and "flex:0 0 170px" in data["text/html"]:
            out.append(help_card(data["text/html"]))
        elif "text/html" in data and "<table" in data["text/html"]:
            out.append(dataframe(data["text/html"]))
        elif "text/plain" in data:
            text = data["text/plain"]
            if o.output_type == "display_data" and text.startswith("<Figure size"):
                continue  # matplotlib's repr of the figure it just drew as a PNG
            out.append({"kind": "text", "text": text})
    return out


def run(vendor: str, dataset: str, source: str, cells: list[str], log: list[str]) -> None:
    """Execute one notebook and write its JSON and images."""
    for i, cell in enumerate(cells):
        if READ_ONLY_VERBS.search(cell):
            raise RuntimeError(f"{vendor}/{dataset} cell {i + 1} is not read-only: {cell!r}")
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_code_cell(src) for src in cells]
    nb.metadata["kernelspec"] = {
        "name": artefacts.KERNEL,
        "display_name": artefacts.KERNEL,
        "language": "python",
    }
    t0 = time.perf_counter()
    NotebookClient(nb, kernel_name=artefacts.KERNEL, timeout=900, allow_errors=True).execute()
    secs = time.perf_counter() - t0
    images: dict[str, bytes] = {}
    stored = []
    for cell in nb.cells:
        stored.append(
            {
                "n": cell.execution_count,
                "source": cell.source,
                "outputs": outputs(cell, dataset, images),
            }
        )
    out_dir = artefacts.notebooks_dir(SITE_DIR) / vendor
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob(f"{dataset}-*.png"):
        old.unlink()
    for name, png in images.items():
        (out_dir / name).write_bytes(png)
    payload = {
        "dataset": f"{vendor}/{dataset}",
        "generated_by": "scripts/run_notebooks.py",
        "cells_sha256": artefacts.cells_digest(cells),
        "kernel": artefacts.KERNEL,
        "source": source,
        "cells": stored,
    }
    artefacts.notebook_path(SITE_DIR, vendor, dataset).write_text(
        artefacts.dumps(payload), encoding="utf-8"
    )
    log.append(f"{vendor}/{dataset}: {len(cells)} cells in {secs:.1f} s, {len(images)} image(s)")
    for c in stored:
        kinds = [o["kind"] for o in c["outputs"]] or ["(no output)"]
        log.append(f"  In [{c['n']}]: {c['source'].splitlines()[0][:70]!r} -> {kinds}")


def main(argv: list[str] | None = None) -> int:
    """Run every (or the named) dataset notebook."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--vault-path", default=str(REPO / "vault"), help="Vault mirror root.")
    parser.add_argument(
        "--dataset", action="append", default=[], help="<vendor>/<dataset>; repeatable."
    )
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    wanted = set(args.dataset)
    log = [f"run {dt.datetime.now(dt.UTC).isoformat(timespec='seconds')}"]
    failures = 0
    for note in sorted(Path(args.vault_path).glob("*/*.md")):
        vendor, dataset = note.parent.name, note.stem
        if wanted and f"{vendor}/{dataset}" not in wanted:
            continue
        fields, errors = parse_page_fields(note.read_text(encoding="utf-8"))
        if not fields.present or not fields.notebook.cells:
            continue
        if errors:
            log.append(f"FAIL {vendor}/{dataset}: {errors}")
            failures += 1
            continue
        source = artefacts.notebook_source(vendor, fields.notebook.source)
        cells = artefacts.notebook_cells(source, fields.notebook.cells)
        try:
            run(vendor, dataset, source, cells, log)
        except RuntimeError as exc:
            log.append(f"FAIL {vendor}/{dataset}: {exc}")
            failures += 1
    print("\n".join(log))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
