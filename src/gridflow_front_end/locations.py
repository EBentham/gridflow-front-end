"""The Open-Meteo weather sites: where gridflow asks, where the vendor answers, and their climate.

For each Open-Meteo archive dataset with a map on its page, read the site list from gridflow's
code (``connectors/openmeteo/endpoints.py``: ``DEMAND_LOCATIONS``, ``WIND_LOCATIONS``,
``SOLAR_LOCATIONS``) and compute, from local silver, the grid point the archive answered from and a
few statistics per site over whole calendar years. Writes
``site/hifi/data/locations/openmeteo/<dataset>.json``; commit it. ``gridflow-build`` draws the map
and its table from that file and never reads silver or gridflow, so CI builds the same page.

Usage
-----
    gridflow-distil --locations                       # all three datasets
    python -m gridflow_front_end.locations --dry-run  # report, write nothing

Needs the ``distil`` extra (Polars). Coordinates are copied from the code's own literals, so the
page shows exactly what gridflow requests; the region of a wind site is the comment above it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import polars as pl

from gridflow_front_end.artefacts import locations_path as _locations_path
from gridflow_front_end.paths import SITE_DIR, resolve_silver_path

GENERATED_BY = "gridflow-distil --locations"
VENDOR = "openmeteo"
SILVER_VENDOR = "open_meteo"
DEFAULT_GRIDFLOW = Path("C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow")
ENDPOINTS = Path("src/gridflow/connectors/openmeteo/endpoints.py")
TRANSFORMER = Path("src/gridflow/silver/openmeteo/historical.py")
# Whole calendar years, so every month counts equally in a mean and a yearly total is a real year.
YEARS = (2022, 2025)
EARTH_RADIUS_KM = 6371.0088  # mean Earth radius (IUGG)

# dataset -> (the tuple in endpoints.py, what the stats describe)
DATASETS: dict[str, tuple[str, str]] = {
    "historical_demand": ("DEMAND_LOCATIONS", "demand"),
    "historical_wind": ("WIND_LOCATIONS", "wind"),
    "historical_solar": ("SOLAR_LOCATIONS", "solar"),
}


class LocationsError(Exception):
    """The code or the silver on disk cannot give a complete, unambiguous site table."""


@dataclass(frozen=True)
class Site:
    """One configured site, with its coordinates exactly as the code writes them."""

    name: str
    lat: str
    lon: str
    group: str | None


def resolve_gridflow_path(cli_arg: str | None) -> Path:
    """gridflow repo root: CLI flag, then ``$GRIDFLOW_REPO_PATH``, then the local default."""
    if cli_arg:
        return Path(cli_arg).expanduser().resolve()
    env_path = os.environ.get("GRIDFLOW_REPO_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return DEFAULT_GRIDFLOW


def locations_path(site_dir: Path, dataset: str) -> Path:
    """Where one dataset's site file is written."""
    return _locations_path(site_dir, VENDOR, dataset)


_HEADER = re.compile(r"^(?P<name>[A-Z_]+_LOCATIONS)\s*:.*=\s*\(\s*$")
_SITE = re.compile(
    r'WeatherLocation\(\s*"(?P<name>[a-z0-9_]+)"\s*,\s*(?P<lat>-?\d+(?:\.\d+)?)\s*,'
    r"\s*(?P<lon>-?\d+(?:\.\d+)?)"
)
_COMMENT = re.compile(r"^\s*#\s*(?P<text>.+?)\s*$")


def _group(comment: str) -> str:
    """A region comment as page text: ``Offshore — southern North Sea`` reads ``Offshore, southern North Sea``."""
    text = re.sub(r"\s*[—–]\s*|\s+-\s+", ", ", comment)
    return " ".join(text.split())


def parse_locations(source: str) -> dict[str, list[Site]]:
    """Every ``*_LOCATIONS`` tuple in ``endpoints.py``, its sites in code order.

    A comment line inside a tuple names the group of the sites below it (the wind list's regions);
    a tuple with no such comment has no groups.
    """
    out: dict[str, list[Site]] = {}
    current: list[Site] | None = None
    group: str | None = None
    for line in source.splitlines():
        if current is None:
            m = _HEADER.match(line)
            if m:
                current, group = [], None
                out[m.group("name")] = current
            continue
        if line.strip() == ")":
            current = None
            continue
        c = _COMMENT.match(line)
        if c:
            group = _group(c.group("text"))
            continue
        s = _SITE.search(line)
        if s:
            current.append(Site(s.group("name"), s.group("lat"), s.group("lon"), group))
    return out


def load_sites(gridflow: Path, tuple_name: str) -> tuple[list[Site], str]:
    """The sites of one tuple, checked against the module's own values, and the file's digest."""
    path = gridflow / ENDPOINTS
    if not path.is_file():
        raise LocationsError(f"gridflow endpoints not found: {path} (set --gridflow-path)")
    source = path.read_text(encoding="utf-8")
    tuples = parse_locations(source)
    if tuple_name not in tuples:
        raise LocationsError(f"{path}: no {tuple_name} tuple")
    sites = tuples[tuple_name]
    # The text is the source of the literals; the imported module confirms the parse missed nothing.
    spec = importlib.util.spec_from_file_location("_gridflow_openmeteo_endpoints", path)
    if spec is None or spec.loader is None:
        raise LocationsError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolves annotations through sys.modules
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(spec.name, None)
    real = [(loc.name, loc.latitude, loc.longitude) for loc in getattr(module, tuple_name)]
    parsed = [(s.name, float(s.lat), float(s.lon)) for s in sites]
    if parsed != real:
        raise LocationsError(f"{tuple_name}: parsed {parsed} but the module holds {real}")
    return sites, hashlib.sha256(source.encode("utf-8")).hexdigest()


def hdd_base(gridflow: Path) -> float:
    """The heating degree base temperature, °C, from the silver transformer (``_HDD_BASE``)."""
    path = gridflow / TRANSFORMER
    m = re.search(r"^_HDD_BASE\s*=\s*([0-9.]+)", path.read_text(encoding="utf-8"), re.MULTILINE)
    if not m:
        raise LocationsError(f"{path}: no _HDD_BASE")
    return float(m.group(1))


def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance on a sphere of the mean Earth radius."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def _scan(silver_root: Path, dataset: str, columns: list[str]) -> pl.LazyFrame:
    table = silver_root / SILVER_VENDOR / dataset
    files = sorted(table.rglob("*.parquet"))
    if not files:
        raise LocationsError(f"no parquet files under {table}")
    lf = pl.scan_parquet(
        files, hive_partitioning=False, missing_columns="insert", extra_columns="ignore"
    ).select(columns)
    ts = lf.collect_schema()["timestamp_utc"]
    if isinstance(ts, pl.Datetime) and ts.time_zone is not None:
        # naive UTC inside Polars: a tz-aware value crossing into Python needs tz data Windows lacks
        lf = lf.with_columns(
            pl.col("timestamp_utc").dt.convert_time_zone("UTC").dt.replace_time_zone(None)
        )
    return lf


def _window() -> tuple[dt.datetime, dt.datetime, int]:
    start = dt.datetime(YEARS[0], 1, 1)
    end = dt.datetime(YEARS[1] + 1, 1, 1)
    return start, end, int((end - start).total_seconds() // 3600)


def _stamp(value: dt.datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%MZ")


def _r(value: float | None, places: int = 3) -> float | None:
    return None if value is None else round(float(value), places)


def _instant_rows(lf: pl.LazyFrame, value: str) -> pl.LazyFrame:
    """Rows whose stamp is an instant (temperature, wind speed) inside the window."""
    start, end, _ = _window()
    return lf.filter((pl.col("timestamp_utc") >= start) & (pl.col("timestamp_utc") < end)).select(
        "timestamp_utc", "location", value
    )


def _demand(lf: pl.LazyFrame) -> dict[str, dict[str, Any]]:
    start, end, _ = _window()
    df = (
        lf.filter((pl.col("timestamp_utc") >= start) & (pl.col("timestamp_utc") < end))
        .select("timestamp_utc", "location", "temperature_2m_c", "hdd_k")
        .collect()
    )
    years = YEARS[1] - YEARS[0] + 1
    agg = df.group_by("location").agg(
        pl.len().alias("hours"),
        pl.col("temperature_2m_c").null_count().alias("nulls"),
        pl.col("temperature_2m_c").mean().alias("mean"),
        pl.col("temperature_2m_c").min().alias("coldest"),
        # the first hour that reached the minimum
        pl.col("timestamp_utc")
        .sort_by(["temperature_2m_c", "timestamp_utc"])
        .first()
        .cast(pl.String)
        .alias("at"),
        (pl.col("hdd_k").sum() / 24 / years).alias("hdd"),
        pl.col("hdd_k").null_count().alias("hdd_nulls"),
    )
    out: dict[str, dict[str, Any]] = {}
    for row in agg.iter_rows(named=True):
        out[row["location"]] = {
            "hours": row["hours"],
            "nulls": row["nulls"] + row["hdd_nulls"],
            "stats": {
                "mean_temp_c": _r(row["mean"]),
                "coldest_c": _r(row["coldest"]),
                "coldest_at": _stamp(dt.datetime.fromisoformat(row["at"])),
                "hdd_per_year": _r(row["hdd"], 1),
            },
        }
    return out


def _wind(lf: pl.LazyFrame) -> dict[str, dict[str, Any]]:
    v = pl.col("wind_speed_100m_mps")
    agg = (
        _instant_rows(lf, "wind_speed_100m_mps")
        .group_by("location")
        .agg(
            pl.len().alias("hours"),
            v.null_count().alias("nulls"),
            v.mean().alias("mean"),
            v.quantile(0.9, interpolation="linear").alias("p90"),
        )
        .collect()
    )
    return {
        row["location"]: {
            "hours": row["hours"],
            "nulls": row["nulls"],
            "stats": {"mean_100m_mps": _r(row["mean"]), "p90_100m_mps": _r(row["p90"])},
        }
        for row in agg.iter_rows(named=True)
    }


def _solar(lf: pl.LazyFrame) -> dict[str, dict[str, Any]]:
    start, end, _ = _window()
    # Irradiance is the vendor's mean over the hour ENDING at the stamp, so the window's hours are
    # stamped 01:00 on its first day to 00:00 after its last, and each hour belongs to the day and
    # month in which it began.
    hourly = (
        lf.filter((pl.col("timestamp_utc") > start) & (pl.col("timestamp_utc") <= end))
        .select("timestamp_utc", "location", "shortwave_radiation_wm2")
        .with_columns((pl.col("timestamp_utc") - pl.duration(hours=1)).alias("begins"))
    )
    daily = (
        hourly.group_by("location", pl.col("begins").dt.date().alias("day"))
        .agg(
            (pl.col("shortwave_radiation_wm2").sum() / 1000).alias("kwh"),
            pl.len().alias("hours"),
            pl.col("shortwave_radiation_wm2").null_count().alias("nulls"),
        )
        .collect()
    )
    totals = daily.group_by("location").agg(
        pl.col("hours").sum(), pl.col("nulls").sum(), pl.col("kwh").mean().alias("mean")
    )
    months = (
        daily.group_by("location", pl.col("day").dt.month().alias("month"))
        .agg(pl.col("kwh").mean().alias("kwh"))
        .sort("location", "kwh", "month", descending=[False, True, False])
    )
    out: dict[str, dict[str, Any]] = {}
    for row in totals.iter_rows(named=True):
        ranked = months.filter(pl.col("location") == row["location"])
        best, worst = ranked.row(0, named=True), ranked.row(ranked.height - 1, named=True)
        out[row["location"]] = {
            "hours": row["hours"],
            "nulls": row["nulls"],
            "stats": {
                "mean_daily_kwh_m2": _r(row["mean"]),
                "sunniest_month": best["month"],
                "sunniest_kwh_m2": _r(best["kwh"]),
                "darkest_month": worst["month"],
                "darkest_kwh_m2": _r(worst["kwh"]),
            },
        }
    return out


_STATS = {"demand": _demand, "wind": _wind, "solar": _solar}
_COLUMNS = {
    "demand": ["temperature_2m_c", "hdd_k"],
    "wind": ["wind_speed_100m_mps"],
    "solar": ["shortwave_radiation_wm2"],
}


def build_payload(dataset: str, silver_root: Path, gridflow: Path) -> dict[str, Any]:
    """One dataset's site file.

    Raises:
        LocationsError: The code and silver disagree on the sites, a site answers from more than
            one grid point, or a site lacks an hour (or a value) in the window.
    """
    tuple_name, kind = DATASETS[dataset]
    sites, digest = load_sites(gridflow, tuple_name)
    lf = _scan(
        silver_root,
        dataset,
        ["timestamp_utc", "location", "latitude", "longitude"] + _COLUMNS[kind],
    )
    start, end, hours = _window()
    cells = (
        lf.filter((pl.col("timestamp_utc") >= start) & (pl.col("timestamp_utc") <= end))
        .group_by("location", "latitude", "longitude")
        .agg(pl.len())
        .collect()
    )
    stats = _STATS[kind](lf)
    names = [s.name for s in sites]
    if set(stats) != set(names):
        raise LocationsError(
            f"{dataset}: silver sites {sorted(stats)} differ from code {sorted(names)}"
        )
    rows: list[dict[str, Any]] = []
    for site in sites:
        mine = cells.filter(pl.col("location") == site.name)
        if mine.height != 1:
            raise LocationsError(f"{dataset}/{site.name}: answered from {mine.height} grid points")
        got = stats[site.name]
        if got["hours"] != hours or got["nulls"]:
            raise LocationsError(
                f"{dataset}/{site.name}: {got['hours']} of {hours} hours, {got['nulls']} null values"
            )
        lat, lon = float(mine["latitude"][0]), float(mine["longitude"][0])
        rows.append(
            {
                "name": site.name,
                "group": site.group,
                "configured": {"lat": site.lat, "lon": site.lon},
                "answered": {"lat": round(lat, 6), "lon": round(lon, 6)},
                "offset_km": round(distance_km(float(site.lat), float(site.lon), lat, lon), 1),
                "stats": got["stats"],
            }
        )
    payload: dict[str, Any] = {
        "_about": (
            "Weather sites for the map on this dataset's page: coordinates from gridflow's "
            "endpoints.py, answered grid points and statistics from silver. Written by "
            f"{GENERATED_BY}; gridflow-build reads it."
        ),
        "dataset": f"{VENDOR}/{dataset}",
        "generated_by": GENERATED_BY,
        "kind": kind,
        "locations_from": f"gridflow {ENDPOINTS.as_posix()}, {tuple_name}",
        "endpoints_sha256": digest,
        "silver": f"{SILVER_VENDOR}/{dataset}",
        "window": {"start": f"{YEARS[0]}-01-01", "end": f"{YEARS[1]}-12-31", "hours": hours},
    }
    if kind == "demand":
        payload["hdd_base_c"] = hdd_base(gridflow)
    payload["sites"] = rows
    return payload


def dumps(payload: Mapping[str, Any]) -> str:
    """One key per line and one site per line, so a regenerated file diffs by site."""

    def one(value: object) -> str:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(", ", ": "))

    lines = ["{"]
    keys = list(payload)
    for i, key in enumerate(keys):
        comma = "," if i < len(keys) - 1 else ""
        value = payload[key]
        if key == "sites":
            lines.append(f"  {json.dumps(key)}: [")
            lines.extend(
                f"    {one(s)}{',' if j < len(value) - 1 else ''}" for j, s in enumerate(value)
            )
            lines.append(f"  ]{comma}")
        else:
            lines.append(f"  {json.dumps(key)}: {one(value)}{comma}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    """Write every Open-Meteo site file (``gridflow-distil --locations``)."""
    parser = argparse.ArgumentParser(
        prog="gridflow-distil --locations", description=__doc__.split("\n")[0]
    )
    parser.add_argument(
        "--silver-path", default=None, help="Silver root (default C:/gridflow-data/silver)."
    )
    parser.add_argument(
        "--gridflow-path", default=None, help="gridflow repo root ($GRIDFLOW_REPO_PATH)."
    )
    parser.add_argument(
        "--dataset",
        action="append",
        default=[],
        help="historical_demand, _wind or _solar; repeatable.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Compute and report, write nothing.")
    args = parser.parse_args(argv)
    silver_root = resolve_silver_path(args.silver_path)
    gridflow = resolve_gridflow_path(args.gridflow_path)
    failures = 0
    wanted = [d.removeprefix(f"{VENDOR}/") for d in args.dataset]
    unknown = sorted(set(wanted) - set(DATASETS))
    if unknown:
        parser.error(f"no map for {unknown}; choose from {sorted(DATASETS)}")
    for dataset in wanted or sorted(DATASETS):
        try:
            payload = build_payload(dataset, silver_root, gridflow)
        except LocationsError as exc:
            failures += 1
            print(f"  FAIL {VENDOR}/{dataset}: {exc}", file=sys.stderr)
            continue
        far = max(payload["sites"], key=lambda s: s["offset_km"])
        print(
            f"  {VENDOR}/{dataset}: {len(payload['sites'])} sites, {payload['window']['hours']} hours "
            f"each; farthest grid point {far['name']} {far['offset_km']} km"
        )
        if not args.dry_run:
            out = locations_path(SITE_DIR, dataset)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(dumps(payload), encoding="utf-8", newline="\n")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
