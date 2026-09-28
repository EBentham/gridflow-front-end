"""Chart spec validation, digest and series cross-checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from gridflow_front_end import chart_spec
from gridflow_front_end.page_fields import parse_page_fields
from gridflow_front_end.paths import DEFAULT_VAULT, SITE_DIR

LINE: dict[str, Any] = {
    "type": "line",
    "silver": "elexon/fuelhh",
    "time": "timestamp_utc",
    "value": "generation_mw",
    "group": "fuel_type",
    "aggregation": "sum",
    "window": {"last": "7d"},
    "unit": "MW",
    "caption": "Generation by fuel.",
}
BAR: dict[str, Any] = {
    "type": "bar",
    "silver": "elexon/bmunits_reference",
    "value": "registered_capacity_mw",
    "group": "fuel_type",
    "aggregation": "sum",
    "unit": "MW",
    "caption": "Capacity by fuel.",
}


def _with(base: dict[str, Any], **changes: Any) -> dict[str, Any]:
    spec = dict(base)
    for key, value in changes.items():
        if value is None:
            spec.pop(key, None)
        else:
            spec[key] = value
    return spec


def test_valid_line_and_bar_specs() -> None:
    assert chart_spec.validate_spec(LINE) == []
    assert chart_spec.validate_spec(BAR) == []


def test_none_spec_needs_a_reason_and_nothing_else() -> None:
    assert chart_spec.validate_spec({"type": "none", "reason": "identifier-only table"}) == []
    assert chart_spec.validate_spec({"type": "none"})
    assert chart_spec.validate_spec({"type": "none", "reason": "x", "unit": "MW"})


@pytest.mark.parametrize(
    ("spec", "fragment"),
    [
        (_with(LINE, type="pie"), "type"),
        (_with(LINE, silver="fuelhh"), "silver"),
        (_with(LINE, time=None), "time"),
        (_with(LINE, window=None), "window"),
        (_with(LINE, window={"last": "7w"}), "window.last"),
        (_with(LINE, window={"start": "2026-09-10", "end": "2026-09-01"}), "start is after end"),
        (_with(LINE, aggregation="median"), "aggregation"),
        (_with(LINE, value=None), "value"),
        (_with(LINE, unit=""), "unit"),
        (_with(LINE, caption="  "), "caption"),
        (_with(LINE, colour="red"), "unknown key"),
        (_with(LINE, caption="a --- b"), "---"),
        (_with(LINE, sort="label"), "sort"),
        (_with(LINE, time_bucket="1w"), "time_bucket"),
        (_with(LINE, filter=[{"column": "fuel_type", "op": "in", "value": []}]), "non-empty"),
        (_with(LINE, filter=[{"column": "fuel_type", "op": "not_null", "value": 1}]), "no value"),
        (_with(LINE, filter=[{"column": "fuel type", "op": "eq", "value": 1}]), "column"),
        (_with(LINE, dedup={"on": [], "order_by": "published_at"}), "dedup.on"),
        (_with(LINE, group=None, group_map={"A": "a"}), "needs a group"),
        (_with(LINE, group_default="other"), "group_map"),
        (_with(LINE, series_order=["wind", "wind"]), "repeat"),
        (_with(BAR, time="timestamp_utc"), "no time axis"),
        (_with(BAR, window={"last": "7d"}), "no time axis"),
        (_with(BAR, group=None), "category"),
        (_with(BAR, limit=0), "limit"),
        (_with(LINE, reason="why"), "reason"),
    ],
)
def test_invalid_specs_are_rejected(spec: dict[str, Any], fragment: str) -> None:
    errors = chart_spec.validate_spec(spec)
    assert errors, f"expected an error mentioning {fragment!r}"
    assert any(fragment in e for e in errors), errors


def test_count_needs_no_value() -> None:
    assert chart_spec.validate_spec(_with(BAR, value=None, aggregation="count")) == []


def test_digest_ignores_key_order() -> None:
    reordered = dict(reversed(list(LINE.items())))
    assert chart_spec.spec_digest(reordered) == chart_spec.spec_digest(LINE)
    assert chart_spec.spec_digest(_with(LINE, unit="GW")) != chart_spec.spec_digest(LINE)


def _series_for(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "spec_sha256": chart_spec.spec_digest(spec),
        "x": ["2026-09-01T00:00:00Z", "2026-09-01T00:30:00Z"],
        "series": [{"key": "wind", "values": [1.0, 2.0]}],
    }


def test_check_series_accepts_a_matching_pair() -> None:
    assert chart_spec.check_series(_series_for(LINE), LINE, "elexon/fuelhh") == []


def test_check_series_catches_every_mismatch() -> None:
    key = "elexon/fuelhh"
    assert chart_spec.check_series(None, None, key) == []
    assert chart_spec.check_series(_series_for(LINE), None, key)  # orphan series
    assert chart_spec.check_series(None, LINE, key)  # spec never distilled
    assert chart_spec.check_series(_series_for(LINE), _with(LINE, unit="GW"), key)  # stale
    none_spec = {"type": "none", "reason": "no measure"}
    assert chart_spec.check_series(None, none_spec, key) == []
    assert chart_spec.check_series(_series_for(LINE), none_spec, key)
    ragged = _series_for(LINE)
    ragged["series"][0]["values"] = [1.0]
    assert chart_spec.check_series(ragged, LINE, key)


def test_resolve_spec_prefers_the_vault_note(tmp_path: Path) -> None:
    staged = chart_spec.staged_spec_path(tmp_path, "elexon", "fuelhh")
    staged.parent.mkdir(parents=True)
    staged.write_text(json.dumps(LINE), encoding="utf-8")
    spec, origin, notes = chart_spec.resolve_spec(tmp_path, "elexon", "fuelhh", None)
    assert (spec, origin, notes) == (LINE, "staging", [])
    vault = _with(LINE, unit="GW")
    spec, origin, notes = chart_spec.resolve_spec(tmp_path, "elexon", "fuelhh", vault)
    assert spec == vault and origin == "vault" and len(notes) == 1


def test_committed_specs_are_valid_and_their_series_current() -> None:
    series_files = sorted(chart_spec.series_dir(SITE_DIR).glob("*/*.json"))
    assert series_files
    for path in series_files:
        vendor, dataset = path.parent.name, path.stem
        note = DEFAULT_VAULT / vendor / f"{dataset}.md"
        vault_chart = parse_page_fields(note.read_text(encoding="utf-8"))[0].chart
        spec, _origin, _notes = chart_spec.resolve_spec(SITE_DIR, vendor, dataset, vault_chart)
        assert spec is not None, path
        assert chart_spec.validate_spec(spec) == [], path
        series = chart_spec.load_series(SITE_DIR, vendor, dataset)
        assert chart_spec.check_series(series, spec, f"{vendor}/{dataset}") == []
