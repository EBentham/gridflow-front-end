"""Page fields read from vault-note front matter."""

from __future__ import annotations

from gridflow_front_end import chart_spec
from gridflow_front_end.build import _parse_frontmatter
from gridflow_front_end.page_fields import parse_page_fields

NOTE = """---
source: elexon
dataset_key: fuelhh
last_verified: 2026-09-09
v2_fix_history:
  - date: 2026-05-20
    change: something
page:
  summary: Half-hourly generation by fuel type.
  what_it_is: >-
    Outturn per settlement period,
    split by fuel.
  how_used:
    - Fuel-mix analytics.
    - Emissions reporting.
  caveats:
    - No solar rows.
  chart:
    type: line
    silver: elexon/fuelhh
    time: timestamp_utc
    value: generation_mw
    aggregation: sum
    window:
      start: 2026-09-01
      end: 2026-09-07
    unit: MW
    caption: Generation by fuel.
---

# Elexon - FUELHH

## Overview

Body text.
"""


def test_note_without_page_block_is_empty() -> None:
    fields, errors = parse_page_fields("---\nsource: elexon\n---\n# x\n")
    assert fields.is_empty and errors == []
    fields, errors = parse_page_fields("# no front matter\n")
    assert fields.is_empty and errors == []


def test_page_block_is_read() -> None:
    fields, errors = parse_page_fields(NOTE)
    assert errors == []
    assert fields.summary == "Half-hourly generation by fuel type."
    assert fields.what_it_is == "Outturn per settlement period, split by fuel."
    assert fields.how_used == ("Fuel-mix analytics.", "Emissions reporting.")
    assert fields.caveats == ("No solar rows.",)
    assert fields.chart is not None
    # YAML dates come back as the ISO strings a JSON spec would carry.
    assert fields.chart["window"] == {"start": "2026-09-01", "end": "2026-09-07"}
    assert chart_spec.validate_spec(fields.chart) == []


def test_malformed_page_fields_are_reported() -> None:
    bad = NOTE.replace("  summary: Half-hourly generation by fuel type.", "  summary: [1, 2]")
    bad = bad.replace("  caveats:\n    - No solar rows.", "  caveats: none\n  colour: red")
    _, errors = parse_page_fields(bad)
    joined = " | ".join(errors)
    assert "page.summary" in joined
    assert "page.caveats" in joined
    assert "unknown field" in joined


def test_build_frontmatter_ignores_nested_keys() -> None:
    fm, body = _parse_frontmatter(NOTE)
    assert fm["dataset_key"] == "fuelhh"
    assert fm["last_verified"] == "2026-09-09"
    # Nested page/chart keys must not leak in as top-level fields.
    assert "summary" not in fm and "unit" not in fm and "date" not in fm
    assert body.startswith("# Elexon")
