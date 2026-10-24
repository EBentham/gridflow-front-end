"""A held page's raw sample: the first rows of one bronze file, exactly as the vendor sent them.

A held page has no silver rows to show (ruling 66 keeps page-level ``held`` for packages with
no silver table: bronze-only file groups). It may still show what can honestly be shown: the
header and first eight lines of one raw file, read from local bronze (read only) and committed
as ``site/hifi/data/raw-samples/<vendor>/<dataset>.json``. The note picks the file under
``page.raw_feed.sample``::

    raw_feed:
      sample:
        table: daily_balancing_costs        # optional: the bronze table (default: the page's key)
        file: q1_cost_fy1718.csv            # optional: NESO's file name (default: newest capture)
        caveat: Rows repeat and carry no run column, so revisions cannot be told apart.

``gridflow-sample`` writes the file beside the silver samples; ``gridflow-build`` renders it
in the bronze stratum with its caveat, and fails when the note's choice and the committed file
disagree. Only line-oriented text files (CSV, plain text) can be sampled.

This module is stdlib-only, so the build can import it without the distil extra.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gridflow_front_end import artefacts

GENERATED_BY = "gridflow-sample"
ROWS = 8
LINE_MAX = 4000  # a longer "line" is a file that is not line-oriented (a one-line JSON body)
TEXT_SUFFIXES = (".csv", ".txt")
# NESO writes some files in Windows-1252, not UTF-8 (the BSUoS forecasts); they are read as such
# so the sample shows the characters NESO meant, and the payload records which reading it took.
ENCODINGS = ("utf-8-sig", "cp1252")


class RawSampleError(Exception):
    """The raw file a note names cannot be sampled."""


def _meta(path: Path) -> dict[str, Any]:
    meta = path.with_name(path.name[: -len(path.suffix)] + ".meta.json")
    if not meta.is_file():
        return {}
    data = json.loads(meta.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _file_name(path: Path, meta: dict[str, Any]) -> str:
    params = meta.get("request_params")
    if isinstance(params, dict) and isinstance(params.get("resource_filename"), str):
        return str(params["resource_filename"])
    return path.name


def pick_file(bronze_root: Path, vendor: str, table: str, file: str) -> tuple[Path, dict[str, Any]]:
    """The bronze capture a raw sample is read from: the named file's, else the newest.

    Args:
        bronze_root: The bronze root (``C:/gridflow-data/bronze``).
        vendor: The vendor id (``neso_data_portal``).
        table: The bronze table directory.
        file: The vendor's file name to pick (``q1_cost_fy1718.csv``), or "" for any.

    Raises:
        RawSampleError: No capture matches.
    """
    table_dir = bronze_root / vendor / table
    if not table_dir.is_dir():
        raise RawSampleError(f"bronze table not found: {table_dir}")
    captures = []
    for path in table_dir.rglob("raw_*"):
        if not path.is_file() or path.name.endswith(".meta.json"):
            continue
        meta = _meta(path)
        if file and _file_name(path, meta) != file:
            continue
        captures.append((str(meta.get("fetched_at", "")), path.as_posix(), path, meta))
    if not captures:
        wanted = f" named {file!r}" if file else ""
        raise RawSampleError(f"no raw file{wanted} under {table_dir}")
    _, _, path, meta = max(captures)
    return path, meta


def read_head(path: Path, rows: int = ROWS) -> tuple[list[str], str]:
    """The header and first ``rows`` lines of a text file, and the encoding they were read in.

    Raises:
        RawSampleError: The file is not line-oriented text.
    """
    if path.suffix.lower() not in TEXT_SUFFIXES:
        raise RawSampleError(f"{path.name}: only a CSV or text file can be sampled")
    raw: list[bytes] = []
    with path.open("rb") as fh:
        for _ in range(rows + 1):
            line = fh.readline(LINE_MAX + 3)
            if not line:
                break
            raw.append(line)
    head = b"".join(raw)
    if b"\x00" in head:
        raise RawSampleError(f"{path.name}: holds NUL bytes, so it is not a text file")
    for encoding in ENCODINGS:
        try:
            text = head.decode(encoding)
        except UnicodeDecodeError:
            continue
        lines = text.splitlines()
        if any(len(ln) > LINE_MAX for ln in lines):
            raise RawSampleError(f"{path.name}: a line runs past {LINE_MAX} characters")
        return lines, "utf-8" if encoding == "utf-8-sig" else encoding
    raise RawSampleError(f"{path.name}: not readable as {' or '.join(ENCODINGS)}")


def build_payload(
    bronze_root: Path, vendor: str, dataset: str, table: str, file: str
) -> dict[str, Any]:
    """Pick, read and describe one held page's raw sample.

    Args:
        bronze_root: The bronze root.
        vendor: The vendor id.
        dataset: The key the page's artefacts are filed under.
        table: ``raw_feed.sample.table``, or "" for ``dataset``.
        file: ``raw_feed.sample.file``, or "" for the newest capture.
    """
    path, meta = pick_file(bronze_root, vendor, table or dataset, file)
    lines, encoding = read_head(path)
    if not lines:
        raise RawSampleError(f"{path.name}: the file is empty")
    return {
        "dataset": f"{vendor}/{dataset}",
        "generated_by": GENERATED_BY,
        "select_sha256": artefacts.raw_sample_digest(table, file),
        "table": table or dataset,
        "file": _file_name(path, meta),
        "body_sha256": str(meta.get("body_sha256", "")),
        "encoding": encoding,
        "lines": lines,
    }
