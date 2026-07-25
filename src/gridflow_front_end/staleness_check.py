"""gridflow-staleness-check — authored-page vs. vault-mirror integrity gate.

The docs-propagation chain has four hops: canonical vault (Obsidian) →
committed mirror (`vault/<vendor>/*.md`) → authored HTML overrides
(`authored-pages/<vendor>/*.html`) → deployed site. Nothing previously
checked that hop 3 stayed in sync with hop 2 once an override was authored
(review finding R8-F01). This script closes that gap with two checks:

1. **Stamp check** — read `vault/.last_synced_from_vault` (the JSON stamp
   left by the vault-mirror propagation). Missing or unparseable is a hard
   failure: the committed mirror carries no provenance for when it was last
   pulled from the vault. A stamp older than 30 days is only a WARNING —
   syncs are event-driven, not scheduled, so age alone doesn't prove drift.
2. **Authored-vs-mirror check** — for every vendor dataset page in the
   committed mirror that has a parsed Silver schema block, a *wired*
   Pydantic schema (see below), and an authored HTML override, every Silver
   schema column name from the mirror must appear as a whole word in the
   authored HTML (word-boundary match, not raw substring — `currency` must
   not match inside `currency_unit`, and `available_capacity_mw` must not
   match inside `unavailable_capacity_mw`). A column present in the mirror
   but absent from the authored override means the override has drifted
   from the page it was meant to showcase.

Datasets with no wired Pydantic schema (``pydantic_schema_wired=False`` —
"dynamic" schemas, e.g. most of ENTSO-G) are excluded from the column
comparison entirely: their authored pages deliberately render a "dynamic —
no Pydantic class" stat instead of enumerating columns, so column-level
staleness is undefined for them. They're counted separately in the summary.

**Baseline ratchet:** a committed backlog of already-known-stale pages lives
at ``.github/staleness-baseline.txt`` (one ``vendor/slug`` per line). A page
with missing columns that IS listed there is reported as a non-failing
``KNOWN-STALE (baselined)`` warning; a page with missing columns NOT listed
there fails the run. A baselined page that no longer has any missing columns
is reported as an informational nudge to remove it from the baseline. The
baseline may only shrink over time (burn-down), never grow silently — this
script does not auto-add to it, and CI (`ci.yml`) separately fails a PR that
adds a line to it.

Pages with no Silver schema section, or with no authored counterpart, are
skipped (and counted). Authored pages with no mirror counterpart are
reported as orphans (informational only — not a failure).

Usage
-----
    gridflow-staleness-check
    gridflow-staleness-check --vault-path /path/to/vault --authored-path /path/to/authored-pages
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from gridflow_front_end.build import (
    AUTHORED_DIR,
    REAL_VENDORS,
    REPO_ROOT,
    parse_vault_file,
    resolve_vault_path,
)

STAMP_FILENAME = ".last_synced_from_vault"
STAMP_MAX_AGE_DAYS = 30
STAMP_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DEFAULT_BASELINE_PATH = REPO_ROOT / ".github" / "staleness-baseline.txt"


@dataclass
class StalePage:
    """One authored override missing one or more mirror Silver schema columns."""

    vendor_id: str
    slug: str
    missing_columns: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.vendor_id}/{self.slug}"


def _column_present(name: str, authored_html: str) -> bool:
    """Whole-word match: `name` must appear as a distinct token, not a substring.

    `_` counts as a word character in Python regex, so this correctly rejects
    `currency` matching inside `currency_unit`, and `available_capacity_mw`
    matching inside `unavailable_capacity_mw`.
    """
    return re.search(rf"\b{re.escape(name)}\b", authored_html) is not None


def check_stamp(stamp_path: Path) -> bool:
    """Validate the vault sync stamp JSON.

    Args:
        stamp_path: Path to `vault/.last_synced_from_vault`.

    Returns:
        True if the stamp exists and parses; False (with an ERROR printed to
        stderr) if it's missing or malformed. An age over
        ``STAMP_MAX_AGE_DAYS`` (checked on exact elapsed seconds, not a
        truncated day count) only emits a WARNING and does not fail — vault
        syncs are event-driven, not scheduled.
    """
    try:
        raw = stamp_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"[gridflow-staleness-check] ERROR: cannot read {stamp_path}: {exc}", file=sys.stderr)
        return False

    try:
        data = json.loads(raw)
        synced_at = data["synced_at_utc"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        print(
            f"[gridflow-staleness-check] ERROR: cannot parse {stamp_path}: {exc}", file=sys.stderr
        )
        return False

    try:
        synced_dt = dt.datetime.strptime(synced_at, STAMP_TIME_FORMAT).replace(tzinfo=dt.UTC)
    except (ValueError, TypeError) as exc:
        print(
            f"[gridflow-staleness-check] ERROR: unparseable synced_at_utc {synced_at!r} in {stamp_path}: {exc}",
            file=sys.stderr,
        )
        return False

    age_seconds = (dt.datetime.now(dt.UTC) - synced_dt).total_seconds()
    if age_seconds > STAMP_MAX_AGE_DAYS * 86400:
        age_days_display = round(age_seconds / 86400, 1)
        print(
            f"[gridflow-staleness-check] WARNING: vault sync stamp is {age_days_display} days old "
            f"(synced_at_utc={synced_at}) — confirm no vault changes are unpropagated.",
            file=sys.stderr,
        )
    return True


def load_baseline(baseline_path: Path) -> set[str]:
    """Load the known-stale ratchet baseline.

    Args:
        baseline_path: Path to `.github/staleness-baseline.txt`. Missing file
            is treated as an empty baseline (not an error — a repo may start
            with zero known-stale pages).

    Returns:
        Set of `"<vendor>/<slug>"` labels. Blank lines and `#`-comment lines
        are ignored.
    """
    if not baseline_path.exists():
        return set()
    labels: set[str] = set()
    for line in baseline_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        labels.add(stripped)
    return labels


def check_authored_pages(
    vault_path: Path, authored_dir: Path
) -> tuple[list[StalePage], list[str], int, int, list[str]]:
    """Compare authored overrides against the mirror's Silver schema columns.

    Datasets with no wired Pydantic schema are excluded from the column
    comparison (their authored pages render "dynamic", never enumerating
    columns) and counted under `n_skipped_dynamic`.

    Slugs are taken from ``DatasetDoc.slug`` (which honours a frontmatter
    `dataset_key` override), not the markdown filename stem, so a
    stem/dataset_key mismatch can never silently skip a deployed override.

    Args:
        vault_path: Root of the committed vault mirror (contains `<vendor>/*.md`).
        authored_dir: Root of authored HTML overrides (contains `<vendor>/*.html`).

    Returns:
        Tuple of (stale pages with missing columns, clean page labels
        `"<vendor>/<slug>"`, count skipped as dynamic-schema, count skipped
        for no-schema/no-authored-override, orphan authored page labels).
    """
    stale: list[StalePage] = []
    clean_labels: list[str] = []
    n_skipped_dynamic = 0
    n_skipped_other = 0
    mirror_slugs: dict[str, set[str]] = {}

    for vendor_id, cfg in REAL_VENDORS.items():
        vendor_dir = vault_path / vendor_id
        mirror_slugs[vendor_id] = set()
        if not vendor_dir.is_dir():
            continue
        vendor_label = cfg["label"]
        for md_path in sorted(vendor_dir.glob("*.md")):
            if md_path.name.lower() == "readme.md":
                continue
            doc = parse_vault_file(md_path, vendor_id=vendor_id, vendor_label=vendor_label)
            slug = doc.slug
            mirror_slugs[vendor_id].add(slug)
            if not doc.schema_rows:
                n_skipped_other += 1
                continue
            if not doc.pydantic_schema_wired:
                n_skipped_dynamic += 1
                continue
            authored_path = authored_dir / vendor_id / f"{slug}.html"
            if not authored_path.exists():
                n_skipped_other += 1
                continue
            authored_html = authored_path.read_text(encoding="utf-8")
            missing = [
                row.name for row in doc.schema_rows if not _column_present(row.name, authored_html)
            ]
            if missing:
                stale.append(StalePage(vendor_id=vendor_id, slug=slug, missing_columns=missing))
            else:
                clean_labels.append(f"{vendor_id}/{slug}")

    orphans: list[str] = []
    for vendor_id in REAL_VENDORS:
        authored_vendor_dir = authored_dir / vendor_id
        if not authored_vendor_dir.is_dir():
            continue
        known_slugs = mirror_slugs.get(vendor_id, set())
        for html_path in sorted(authored_vendor_dir.glob("*.html")):
            if html_path.stem == "_landing":
                continue
            if html_path.stem not in known_slugs:
                orphans.append(f"{vendor_id}/{html_path.stem}")

    return stale, clean_labels, n_skipped_dynamic, n_skipped_other, orphans


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns process exit code (0 clean, 1 stale/error)."""
    parser = argparse.ArgumentParser(
        prog="gridflow-staleness-check", description=__doc__.split("\n", 1)[0]
    )
    parser.add_argument(
        "--vault-path",
        default=None,
        help="Path to the committed vault mirror root. Defaults to $GRIDFLOW_VAULT_PATH, "
        "then the vendored ./vault/ directory.",
    )
    parser.add_argument(
        "--authored-path",
        default=None,
        help="Path to the authored-pages root. Defaults to the vendored ./authored-pages/ directory.",
    )
    parser.add_argument(
        "--baseline-path",
        default=None,
        help="Path to the known-stale ratchet baseline file. Defaults to "
        "./.github/staleness-baseline.txt.",
    )
    args = parser.parse_args(argv)

    vault_path = resolve_vault_path(args.vault_path)
    authored_dir = (
        Path(args.authored_path).expanduser().resolve() if args.authored_path else AUTHORED_DIR
    )
    baseline_path = (
        Path(args.baseline_path).expanduser().resolve()
        if args.baseline_path
        else DEFAULT_BASELINE_PATH
    )

    print(f"[gridflow-staleness-check] vault: {vault_path}")
    print(f"[gridflow-staleness-check] authored: {authored_dir}")
    print(f"[gridflow-staleness-check] baseline: {baseline_path}")

    if not check_stamp(vault_path / STAMP_FILENAME):
        return 1

    baseline = load_baseline(baseline_path)
    stale, clean_labels, n_skipped_dynamic, n_skipped_other, orphans = check_authored_pages(
        vault_path, authored_dir
    )

    for orphan in orphans:
        print(
            f"[gridflow-staleness-check] INFO: orphan authored page (no mirror counterpart): {orphan}"
        )

    hard_fail = [p for p in stale if p.label not in baseline]
    baselined_stale = [p for p in stale if p.label in baseline]
    clean_but_baselined = [label for label in clean_labels if label in baseline]

    for page in baselined_stale:
        cols = ", ".join(page.missing_columns)
        print(
            f"[gridflow-staleness-check] WARNING: KNOWN-STALE (baselined): {page.label} "
            f"— missing column(s): {cols}",
            file=sys.stderr,
        )

    for label in clean_but_baselined:
        print(
            f"[gridflow-staleness-check] INFO: clean — remove from baseline: {label}",
        )

    n_checked = len(stale) + len(clean_labels)

    if hard_fail:
        print(
            f"[gridflow-staleness-check] FAIL: {len(hard_fail)} stale authored page(s) "
            f"not covered by the baseline:",
            file=sys.stderr,
        )
        for page in hard_fail:
            cols = ", ".join(page.missing_columns)
            print(f"  STALE: {page.label} — missing column(s): {cols}", file=sys.stderr)
        return 1

    print(
        f"[gridflow-staleness-check] OK: checked {n_checked} authored page(s) against mirror Silver "
        f"schema columns ({len(baselined_stale)} known-stale baselined, "
        f"{n_skipped_dynamic} skipped — dynamic schema, "
        f"{n_skipped_other} skipped — no schema or no authored override, "
        f"{len(orphans)} orphan authored page(s))."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
