"""Page fields read from vault-note front matter: the dataset page content model."""

from __future__ import annotations

from gridflow_front_end import chart_spec
from gridflow_front_end.build import _parse_frontmatter
from gridflow_front_end.page_fields import anatomy_errors, parse_page_fields

NOTE = """---
source: elexon
dataset_key: fuelhh
last_verified: 2026-09-09
v2_fix_history:
  - date: 2026-05-20
    change: something
page:
  title: Generation by fuel type
  summary: Half-hourly generation by fuel type.
  facts:
    vendor: Elexon BMRS, dataset FUELHH
    cadence: Every 30 minutes
    grain: One row per settlement period and fuel-type code
  what_it_is: >-
    Outturn per settlement period,
    split by fuel.
  how_used:
    - Fuel-mix analytics.
    - Emissions reporting.
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
  chart_view:
    title: Generation, 1 to 7 September 2026
    caption: Silver elexon/fuelhh, MW.
    alt: A line of generation.
    key:
      - {series: generation_mw, label: Generation, paint: petrol}
  raw_feed:
    note: From the Elexon Insights API.
    requests: ["GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH"]
    commands:
      - {run: gridflow ingest elexon fuelhh --start 2026-09-01 --end 2026-09-07, comment: bronze only}
  record:
    select:
      filter: [{column: settlement_date, op: eq, value: 2026-09-26}]
    mark: {fuel_type: PS}
    key: [settlement_date, settlement_period, fuel_type]
    caption: Eight rows.
    fields:
      settlement_date: GB settlement date
  notebook:
    lead: Returns a pandas DataFrame.
    cells:
      - df = data.elexon.query("fuelhh", "2026-09-01", "2026-09-07")
      - df.head()
    needs: 1 to 7 September 2026
  related:
    - {dataset: elexon/fuelinst, note: Instantaneous outturn by fuel type}
---

# Elexon - FUELHH

## Overview

Body text.
"""


def test_note_without_page_block_is_empty() -> None:
    fields, errors = parse_page_fields("---\nsource: elexon\n---\n# x\n")
    assert fields.is_empty and not fields.present and errors == []
    fields, errors = parse_page_fields("# no front matter\n")
    assert fields.is_empty and errors == []


def test_page_block_is_read() -> None:
    fields, errors = parse_page_fields(NOTE)
    assert errors == []
    assert fields.present
    assert fields.title == "Generation by fuel type"
    assert fields.what_it_is == "Outturn per settlement period, split by fuel."
    assert fields.how_used == ("Fuel-mix analytics.", "Emissions reporting.")
    assert fields.facts.cadence == "Every 30 minutes"
    assert fields.record.key == ("settlement_date", "settlement_period", "fuel_type")
    # YAML dates come back as the ISO strings a JSON spec (and the sample digest) carry.
    assert fields.record.select["filter"][0]["value"] == "2026-09-26"
    assert fields.chart is not None
    assert fields.chart["window"] == {"start": "2026-09-01", "end": "2026-09-07"}
    assert chart_spec.validate_spec(fields.chart) == []
    assert anatomy_errors(fields) == []


def test_malformed_page_fields_are_reported() -> None:
    bad = NOTE.replace("  summary: Half-hourly generation by fuel type.", "  summary: [1, 2]")
    bad = bad.replace("  how_used:\n", "  caveats: none\n  how_used:\n")
    _, errors = parse_page_fields(bad)
    joined = " | ".join(errors)
    assert "page.summary" in joined
    assert "unknown key(s) ['caveats']" in joined


def test_missing_and_over_budget_fields_fail() -> None:
    long_title = "  title: " + " ".join(["word"] * 7)
    bad = NOTE.replace("  title: Generation by fuel type", long_title)
    bad = bad.replace(
        "  related:\n    - {dataset: elexon/fuelinst, note: Instantaneous outturn by fuel type}\n",
        "",
    )
    fields, errors = parse_page_fields(bad)
    assert errors == []
    joined = " | ".join(anatomy_errors(fields))
    assert "page.title: 7 words, over its budget of 6" in joined
    assert "page.related: missing" in joined


def test_khaki_is_only_for_other() -> None:
    bad = NOTE.replace("paint: petrol}", "paint: khaki}")
    fields, _ = parse_page_fields(bad)
    assert any("khaki is the vendor code OTHER only" in e for e in anatomy_errors(fields))


def test_chart_caption_lives_in_the_view() -> None:
    bad = NOTE.replace("    unit: MW\n", "    unit: MW\n    caption: Old caption.\n")
    fields, _ = parse_page_fields(bad)
    assert any("put the caption in page.chart_view.caption" in e for e in anatomy_errors(fields))


def test_an_unquoted_dedup_on_key_survives_yaml() -> None:
    note = NOTE.replace(
        "      filter: [{column: settlement_date, op: eq, value: 2026-09-26}]\n",
        "      filter: [{column: settlement_date, op: eq, value: 2026-09-26}]\n"
        "      dedup: {on: [settlement_date], order_by: published_at}\n",
    )
    fields, errors = parse_page_fields(note)
    assert errors == []
    assert fields.record.select["dedup"] == {"on": ["settlement_date"], "order_by": "published_at"}


def test_build_frontmatter_ignores_nested_keys() -> None:
    fm, body = _parse_frontmatter(NOTE)
    assert fm["dataset_key"] == "fuelhh"
    assert fm["last_verified"] == "2026-09-09"
    # Nested page/chart keys must not leak in as top-level fields.
    assert "summary" not in fm and "unit" not in fm and "date" not in fm
    assert body.startswith("# Elexon")
