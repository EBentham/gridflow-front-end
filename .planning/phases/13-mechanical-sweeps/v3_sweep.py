#!/usr/bin/env python3
"""v3 Phase 13 — mechanical Stream-M sweep over ``authored-pages/``.

Deterministic, idempotent, and churn-free (preserves LF endings). Default is a
dry run that only reports; pass ``--apply`` to write. ``--only`` selects a comma-
separated subset of sweeps. Re-running after an apply is a no-op (every sweep is
expressed as an exact replace that does not match its own output).

The build reads ``authored-pages/`` (source) and renders to the gitignored
``site/hifi/data-sources/`` — so we edit source, never generated output.

Sweeps:
  viewport  Swap the desktop-locked ``width=1280`` viewport for a responsive one
            (161 dataset pages; ``system_prices`` + the 6 ``_landing`` hubs are
            already correct, so they are no-ops).

  (examples / honesty land in Batch 2 once the gridflow-models registry and the
   cite-span population have been inspected — see 13-BRIEF.)
"""
from __future__ import annotations

import argparse
import pathlib
import sys


def find_root(start: pathlib.Path) -> pathlib.Path:
    """Walk up from ``start`` until the dir containing ``authored-pages/``."""
    for candidate in (start, *start.parents):
        if (candidate / "authored-pages").is_dir():
            return candidate
    raise SystemExit("authored-pages/ not found above script location")


ROOT = find_root(pathlib.Path(__file__).resolve())
AUTHORED = ROOT / "authored-pages"

# ── Sweep: viewport ──────────────────────────────────────────────────────────
# Two populations ship two spellings (spaced vs unspaced self-close); normalise
# both to the canonical responsive form used by system_prices + the hubs.
VIEWPORT_NEW = '<meta name="viewport" content="width=device-width, initial-scale=1" />'
VIEWPORT_OLD = (
    '<meta name="viewport" content="width=1280" />',
    '<meta name="viewport" content="width=1280"/>',
)


def sweep_viewport(text: str) -> str:
    """Replace the desktop-locked viewport with a responsive one (both spellings)."""
    for old in VIEWPORT_OLD:
        text = text.replace(old, VIEWPORT_NEW)
    return text


SWEEPS = {
    "viewport": sweep_viewport,
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
        help="comma-separated sweeps to run (default: all implemented)",
    )
    args = parser.parse_args(argv)

    selected = [name.strip() for name in args.only.split(",") if name.strip()]
    unknown = [name for name in selected if name not in SWEEPS]
    if unknown:
        raise SystemExit(f"unknown sweep(s): {', '.join(unknown)} — known: {', '.join(SWEEPS)}")

    pages = sorted(AUTHORED.rglob("*.html"))
    changed_total = 0
    per_sweep: dict[str, int] = {name: 0 for name in selected}

    for page in pages:
        before = read_text(page)
        after = before
        for name in selected:
            stepped = SWEEPS[name](after)
            if stepped != after:
                per_sweep[name] += 1
            after = stepped
        if after != before:
            changed_total += 1
            rel = page.relative_to(ROOT).as_posix()
            print(f"  {'WRITE' if args.apply else 'would change'}: {rel}")
            if args.apply:
                write_text(page, after)

    print()
    print(f"sweeps: {', '.join(selected)}")
    for name in selected:
        print(f"  {name}: {per_sweep[name]} file(s)")
    print(f"total files {'written' if args.apply else 'that would change'}: {changed_total}")
    print(f"(scanned {len(pages)} authored pages; {'APPLIED' if args.apply else 'DRY RUN'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
