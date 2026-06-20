#!/usr/bin/env python3
"""v3 Phase 13 — mechanical Stream-M sweep over ``authored-pages/``.

Deterministic, idempotent, and churn-free (preserves LF endings). Default is a
dry run that only reports; pass ``--apply`` to write. ``--only`` selects a comma-
separated subset of sweeps. Re-running after an apply is a no-op (every sweep is
expressed as an exact/anchored replace that does not match its own output).

The build reads ``authored-pages/`` (source) and renders to the gitignored
``site/hifi/data-sources/`` — so we edit source, never generated output.

Sweeps:
  viewport  Swap the desktop-locked ``width=1280`` viewport for a responsive one
            (both self-close spellings). [Batch 1 — applied]
  examples  Python·parquet tab -> gridflow-models facade
            (``data.<source>.query("<slug>", start, end)`` / ``.describe(...)``),
            DuckDB read_parquet(...) -> the ``silver_<slug>`` view. Source/slug
            come from the authoritative gridflow-models registry; slugs absent
            from it (orphans) and the ``_landing`` hubs are skipped untouched.
  cites     Remove trailing ``cite`` / ``src-cite`` provenance spans (internal
            class-path / vault refs). Honest vendor-field "Source:" prose stays.
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import re
import sys

REGISTRY_PATH = pathlib.Path(
    "C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow_models/src/gridflow_models"
    "/research/handles/_get_method_registry.py"
)


def find_root(start: pathlib.Path) -> pathlib.Path:
    """Walk up from ``start`` until the dir containing ``authored-pages/``."""
    for candidate in (start, *start.parents):
        if (candidate / "authored-pages").is_dir():
            return candidate
    raise SystemExit("authored-pages/ not found above script location")


def load_dataset_source() -> dict[str, str]:
    """Load ``{slug: source}`` straight from the gridflow-models registry.

    Fail loud if the package isn't where we expect — never silently fabricate a
    facade call for a dataset we can't confirm exists.
    """
    if not REGISTRY_PATH.is_file():
        raise SystemExit(f"gridflow-models registry not found at {REGISTRY_PATH}")
    spec = importlib.util.spec_from_file_location("_gf_registry", REGISTRY_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load registry module from {REGISTRY_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {slug: src for slug, src, _date_col in module._DATASETS_INVENTORY if src}


ROOT = find_root(pathlib.Path(__file__).resolve())
AUTHORED = ROOT / "authored-pages"
DATASET_SOURCE = load_dataset_source()

# ── Sweep: viewport (Batch 1) ────────────────────────────────────────────────
VIEWPORT_NEW = '<meta name="viewport" content="width=device-width, initial-scale=1" />'
VIEWPORT_OLD = (
    '<meta name="viewport" content="width=1280" />',
    '<meta name="viewport" content="width=1280"/>',
)


def sweep_viewport(text: str, slug: str, source: str | None) -> str:
    """Replace the desktop-locked viewport with a responsive one (both spellings)."""
    for old in VIEWPORT_OLD:
        text = text.replace(old, VIEWPORT_NEW)
    return text


# ── Sweep: examples (Batch 2) ────────────────────────────────────────────────
# Relabel the Python tab button (any suffix: polars / parquet / pandas).
_PY_LABEL_RE = re.compile(
    r"(setTab\('[^']+','py',this\)\"[^>]*>)Python\s*·\s*[^<]*(</button>)"
)
# The whole <pre> inside the Python panel (group id varies per page).
_PY_PANEL_RE = re.compile(
    r'(<div data-tab-panel="[^"]*-py"[^>]*>\s*<div class="code-wrap">\s*)'
    r"<pre\b[^>]*>.*?</pre>",
    re.DOTALL,
)
# DuckDB read_parquet('data/silver/<src>/<slug>...') -> silver_<slug>. Handles all
# three shipped path shapes: partitioned glob (<slug>/**/*.parquet), single file in
# a slug dir (<slug>/<slug>.parquet), and flat (<slug>.parquet). Slug = group 2
# (first segment after <src>), taken from the PATH so a cross-dataset JOIN maps right.
_READ_PARQUET_RE = re.compile(
    r"read_parquet\(<span class=\"s\">(['\"])data/silver/[^/<]+/([^/<.]+)"
    r"(?:\.parquet|/[^<]*?\.parquet)\1</span>\)"
)


def _facade_pre(source: str, slug: str) -> str:
    """The replacement Python panel: gridflow-models data-access, house style."""
    return (
        '<pre class="code dark" style="padding: 18px 22px;">'
        '<span class="k">from</span> gridflow_models <span class="k">import</span> setup_notebook\n'
        "\n"
        "data, models, common = setup_notebook()\n"
        "\n"
        f'<span class="c"># {slug}: stored silver rows as a pandas DataFrame</span>\n'
        f'df = data.{source}.query(<span class="s">"{slug}"</span>, '
        '<span class="s">"2026-01-01"</span>, <span class="s">"2026-01-31"</span>)\n'
        "\n"
        '<span class="c"># columns, dtypes, nullability, notes</span>\n'
        f'data.{source}.describe(<span class="s">"{slug}"</span>)</pre>'
    )


def sweep_examples(text: str, slug: str, source: str | None) -> str:
    """Swap the Python example to the facade + modernise the DuckDB view name."""
    if slug.startswith("_") or source is None:
        return text  # hub or orphan — leave untouched (caller logs orphans)
    text = _PY_LABEL_RE.sub(r"\1Python · gridflow-models\2", text)
    text = _PY_PANEL_RE.sub(lambda m: m.group(1) + _facade_pre(source, slug), text)
    text = _READ_PARQUET_RE.sub(lambda m: f"silver_{m.group(2)}", text)
    return text


# ── Sweep: cites (Batch 2) ───────────────────────────────────────────────────
# Trailing provenance tags (internal class-path / vault refs). Inspected across
# vendors: they sit at the END of schema-table cells and caveat boxes, never
# mid-sentence, so element removal leaves grammatical prose. Some wrap a nested
# <code class="mono">…</code>, so match lazily across it (no inner </span> exists).
_CITE_RE = re.compile(r'<span class="(?:cite|src-cite)">.*?</span>', re.DOTALL)


def sweep_cites(text: str, slug: str, source: str | None) -> str:
    """Strip ``cite`` / ``src-cite`` spans; honest vendor-field provenance stays."""
    return _CITE_RE.sub("", text)


SWEEPS = {
    "viewport": sweep_viewport,
    "examples": sweep_examples,
    "cites": sweep_cites,
}


def read_text(path: pathlib.Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_text(path: pathlib.Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    parser.add_argument(
        "--only",
        default=",".join(SWEEPS),
        help="comma-separated sweeps to run (default: all)",
    )
    args = parser.parse_args(argv)

    selected = [name.strip() for name in args.only.split(",") if name.strip()]
    unknown = [name for name in selected if name not in SWEEPS]
    if unknown:
        raise SystemExit(f"unknown sweep(s): {', '.join(unknown)} — known: {', '.join(SWEEPS)}")

    pages = sorted(AUTHORED.rglob("*.html"))
    changed_total = 0
    per_sweep: dict[str, int] = {name: 0 for name in selected}
    orphans: list[str] = []

    for page in pages:
        slug = page.stem
        source = DATASET_SOURCE.get(slug)
        if "examples" in selected and not slug.startswith("_") and source is None:
            orphans.append(page.relative_to(ROOT).as_posix())
        before = read_text(page)
        after = before
        for name in selected:
            stepped = SWEEPS[name](after, slug, source)
            if stepped != after:
                per_sweep[name] += 1
            after = stepped
        if after != before:
            changed_total += 1
            if args.apply:
                write_text(page, after)

    print(f"sweeps: {', '.join(selected)}")
    for name in selected:
        print(f"  {name}: {per_sweep[name]} file(s)")
    if "examples" in selected:
        print(f"  orphans skipped (slug not in registry): {len(orphans)}")
        for orphan in orphans:
            print(f"    - {orphan}")
    print(f"total files {'written' if args.apply else 'that would change'}: {changed_total}")
    print(f"(scanned {len(pages)} authored pages; registry has {len(DATASET_SOURCE)} datasets; "
          f"{'APPLIED' if args.apply else 'DRY RUN'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
