"""The silver distil, run against small synthetic parquet tables."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

import pytest

pl = pytest.importorskip("polars")

from gridflow_front_end import chart_spec
from gridflow_front_end.distil import (
    DistilError,
    SpecSource,
    build_payload,
    distil_spec,
    dumps_payload,
)

T0 = dt.datetime(2026, 9, 1, tzinfo=dt.UTC)


def _write(root: Path, table: str, frames: dict[str, Any]) -> None:
    """Write each frame as one daily partition file, like gridflow silver."""
    for name, df in frames.items():
        out = root / table / "year=2026" / "month=09" / f"{name}.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(out)


def _fuel_rows(start: dt.datetime, periods: int) -> Any:
    rows = []
    for i in range(periods):
        ts = start + dt.timedelta(minutes=30 * i)
        rows += [
            {"timestamp_utc": ts, "fuel_type": "WIND", "generation_mw": 100.0 + i},
            {"timestamp_utc": ts, "fuel_type": "CCGT", "generation_mw": 50.0},
            {"timestamp_utc": ts, "fuel_type": "OCGT", "generation_mw": 5.0},
            {"timestamp_utc": ts, "fuel_type": "INTFR", "generation_mw": -20.0},
        ]
    return pl.DataFrame(rows).with_columns(pl.col("timestamp_utc").dt.replace_time_zone("UTC"))


FUEL_SPEC: dict[str, Any] = {
    "type": "line",
    "silver": "elexon/fuelhh",
    "time": "timestamp_utc",
    "value": "generation_mw",
    "group": "fuel_type",
    "group_map": {"WIND": "wind", "CCGT": "gas", "OCGT": "gas"},
    "series_order": ["wind", "gas"],
    "aggregation": "sum",
    "window": {"last": "2h"},
    "unit": "MW",
    "caption": "Generation by fuel group.",
}


def test_per_fuel_series_are_summed_not_averaged(tmp_path: Path) -> None:
    _write(tmp_path, "elexon/fuelhh", {"d1": _fuel_rows(T0, 6)})
    chart = distil_spec(FUEL_SPEC, tmp_path)
    assert chart["x_kind"] == "time"
    # Window "last 2h" keeps the four periods after (last - 2h).
    assert chart["x"] == [
        "2026-09-01T01:00:00Z",
        "2026-09-01T01:30:00Z",
        "2026-09-01T02:00:00Z",
        "2026-09-01T02:30:00Z",
    ]
    by_key = {s["key"]: s["values"] for s in chart["series"]}
    assert [s["key"] for s in chart["series"]] == ["wind", "gas", "INTFR"]
    assert by_key["wind"] == [102.0, 103.0, 104.0, 105.0]
    assert by_key["gas"] == [55.0] * 4  # CCGT + OCGT, a sum per period
    assert by_key["INTFR"] == [-20.0] * 4  # unmapped values keep their raw label
    assert chart["provenance"]["unmapped_groups"] == ["INTFR"]
    assert chart["provenance"]["rows_read"] == 24


def test_group_default_collects_unmapped_values(tmp_path: Path) -> None:
    _write(tmp_path, "elexon/fuelhh", {"d1": _fuel_rows(T0, 2)})
    spec = dict(FUEL_SPEC, group_default="other")
    chart = distil_spec(spec, tmp_path)
    assert {s["key"] for s in chart["series"]} == {"wind", "gas", "other"}


def test_dedup_keeps_the_latest_published_row(tmp_path: Path) -> None:
    ts = [T0, T0, T0 + dt.timedelta(minutes=30)]
    df = pl.DataFrame(
        {
            "timestamp_utc": ts,
            "published_at": [T0, T0 + dt.timedelta(hours=1), T0],
            "system_sell_price": [10.0, 99.0, 20.0],
        }
    ).with_columns(pl.col("timestamp_utc", "published_at").dt.replace_time_zone("UTC"))
    _write(tmp_path, "elexon/system_prices", {"d1": df})
    spec = {
        "type": "line",
        "silver": "elexon/system_prices",
        "time": "timestamp_utc",
        "value": "system_sell_price",
        "dedup": {"on": ["timestamp_utc"], "order_by": "published_at"},
        "aggregation": "last",
        "window": {"last": "1d"},
        "unit": "£/MWh",
        "caption": "System price.",
    }
    chart = distil_spec(spec, tmp_path)
    assert chart["series"][0]["values"] == [99.0, 20.0]
    assert chart["provenance"]["duplicates_dropped"] == 1


def test_daily_bucket_leaves_gaps_as_missing_days(tmp_path: Path) -> None:
    days = [T0 + dt.timedelta(days=d, hours=4) for d in (0, 1, 5)]
    df = pl.DataFrame(
        {
            "timestamp_utc": days * 2,
            "point_label": ["A"] * 3 + ["B"] * 3,
            "flow_gwh_per_day": [1.0, 2.0, 3.0, 10.0, None, 30.0],
        }
    ).with_columns(pl.col("timestamp_utc").dt.replace_time_zone("UTC"))
    _write(tmp_path, "entsog/physical_flows", {"d1": df})
    spec = {
        "type": "line",
        "silver": "entsog/physical_flows",
        "time": "timestamp_utc",
        "value": "flow_gwh_per_day",
        "group": "point_label",
        "time_bucket": "1d",
        "aggregation": "sum",
        "window": {"start": "2026-09-01", "end": "2026-09-30"},
        "unit": "GWh/d",
        "caption": "Daily flow.",
    }
    chart = distil_spec(spec, tmp_path)
    assert chart["x"] == ["2026-09-01T00:00:00Z", "2026-09-02T00:00:00Z", "2026-09-06T00:00:00Z"]
    by_key = {s["key"]: s["values"] for s in chart["series"]}
    assert by_key["A"] == [1.0, 2.0, 3.0]
    # A null flow is missing data, never a zero.
    assert by_key["B"] == [10.0, None, 30.0]
    assert chart["provenance"]["null_values_dropped"] == 1


def test_bar_chart_has_no_time_axis(tmp_path: Path) -> None:
    df = pl.DataFrame(
        {
            "fuel_type": ["WIND", "WIND", "CCGT", None],
            "registered_capacity_mw": [10.0, 5.0, 40.0, 999.0],
        }
    )
    _write(tmp_path, "elexon/bmunits_reference", {"all": df})
    spec = {
        "type": "bar",
        "silver": "elexon/bmunits_reference",
        "value": "registered_capacity_mw",
        "filter": [{"column": "fuel_type", "op": "not_null"}],
        "group": "fuel_type",
        "aggregation": "sum",
        "unit": "MW",
        "caption": "Capacity by fuel.",
    }
    chart = distil_spec(spec, tmp_path)
    assert chart["x_kind"] == "category"
    assert chart["x"] == ["CCGT", "WIND"]
    assert chart["series"][0]["values"] == [40.0, 15.0]
    assert chart["window"] is None
    assert chart["provenance"]["rows_read"] == 4
    assert chart["provenance"]["rows_matched"] == 3


def test_missing_table_or_column_fails_loudly(tmp_path: Path) -> None:
    with pytest.raises(DistilError, match="not found"):
        distil_spec(FUEL_SPEC, tmp_path)
    _write(tmp_path, "elexon/fuelhh", {"d1": _fuel_rows(T0, 2)})
    with pytest.raises(DistilError, match="not in silver"):
        distil_spec(dict(FUEL_SPEC, value="output_mw"), tmp_path)
    with pytest.raises(DistilError, match="select no rows"):
        distil_spec(
            dict(FUEL_SPEC, filter=[{"column": "fuel_type", "op": "eq", "value": "SOLAR"}]),
            tmp_path,
        )


def test_max_points_guard(tmp_path: Path) -> None:
    _write(tmp_path, "elexon/fuelhh", {"d1": _fuel_rows(T0, 10)})
    with pytest.raises(DistilError, match="max_points"):
        distil_spec(dict(FUEL_SPEC, window={"last": "1d"}, max_points=3), tmp_path)


def test_payload_round_trips_and_matches_its_spec(tmp_path: Path) -> None:
    _write(tmp_path, "elexon/fuelhh", {"d1": _fuel_rows(T0, 4)})
    payload = build_payload(SpecSource("elexon", "fuelhh", FUEL_SPEC, "staging"), tmp_path)
    text = dumps_payload(payload)
    loaded = json.loads(text)
    assert loaded == json.loads(json.dumps(payload))
    assert chart_spec.check_series(loaded, FUEL_SPEC, "elexon/fuelhh") == []
    # One line per series keeps re-distil diffs readable.
    assert text.count('{"key": ') == len(payload["series"])
