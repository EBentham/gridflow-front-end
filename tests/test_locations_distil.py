"""The weather-site distil step: gridflow's site lists and the statistics read from silver.

Needs Polars (the ``distil`` extra); the drawing and page tests in ``test_locations_map.py`` do not.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

import pytest

pl = pytest.importorskip("polars")

from gridflow_front_end import distil, locations  # noqa: E402  (needs the distil extra)

ENDPOINTS = '''"""Fixture endpoints."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherLocation:
    name: str
    latitude: float
    longitude: float
    timezone: str = "UTC"


DEMAND_LOCATIONS: tuple[WeatherLocation, ...] = (
    WeatherLocation("london", 51.5074, -0.1278),
    WeatherLocation("glasgow", 55.8642, -4.2518),
)

WIND_LOCATIONS: tuple[WeatherLocation, ...] = (
    # Offshore — southern North Sea
    WeatherLocation("hornsea", 53.88, 1.79),
    # Onshore — Wales
    WeatherLocation("pen_y_cymoedd", 51.69, -3.61),
)

SOLAR_LOCATIONS: tuple[WeatherLocation, ...] = (
    WeatherLocation("kent", 51.20, 0.70),
)
'''
START, END = dt.datetime(2022, 1, 1), dt.datetime(2026, 1, 1)
HOURS = 35064


def _gridflow(root: Path) -> Path:
    ep = root / "gridflow" / locations.ENDPOINTS
    ep.parent.mkdir(parents=True)
    ep.write_text(ENDPOINTS, encoding="utf-8")
    tr = root / "gridflow" / locations.TRANSFORMER
    tr.parent.mkdir(parents=True)
    tr.write_text("_HDD_BASE = 15.5\n_CDD_BASE = 22.0\n", encoding="utf-8")
    return root / "gridflow"


def _stamps(first: dt.datetime, n: int) -> list[dt.datetime]:
    return [first + dt.timedelta(hours=i) for i in range(n)]


def _write(root: Path, dataset: str, frame: Any) -> Path:
    out = root / "silver" / "open_meteo" / dataset / "year=2022" / "part.parquet"
    out.parent.mkdir(parents=True)
    frame.with_columns(pl.col("timestamp_utc").dt.replace_time_zone("UTC")).write_parquet(out)
    return root / "silver"


def _site_rows(
    name: str, lat: float, lon: float, stamps: list[dt.datetime], **cols: list[float]
) -> Any:
    n = len(stamps)
    return pl.DataFrame(
        {
            "timestamp_utc": stamps,
            "location": [name] * n,
            "latitude": [lat] * n,
            "longitude": [lon] * n,
            **cols,
        }
    )


# ------------------------------------------------------------------------- reading gridflow's code


def test_sites_come_from_the_code_with_their_region_comments() -> None:
    parsed = locations.parse_locations(ENDPOINTS)
    assert [s.name for s in parsed["DEMAND_LOCATIONS"]] == ["london", "glasgow"]
    wind = parsed["WIND_LOCATIONS"]
    assert [(s.name, s.lat, s.lon, s.group) for s in wind] == [
        ("hornsea", "53.88", "1.79", "Offshore, southern North Sea"),
        ("pen_y_cymoedd", "51.69", "-3.61", "Onshore, Wales"),
    ]
    assert parsed["SOLAR_LOCATIONS"][0].lat == "51.20"  # the literal, trailing zero kept
    assert parsed["DEMAND_LOCATIONS"][0].group is None


def test_the_parse_is_checked_against_the_module(tmp_path: Path) -> None:
    gridflow = _gridflow(tmp_path)
    sites, digest = locations.load_sites(gridflow, "WIND_LOCATIONS")
    assert len(sites) == 2 and len(digest) == 64
    ep = gridflow / locations.ENDPOINTS
    # a site the regex cannot read (a keyword argument) must not be silently dropped
    ep.write_text(
        ENDPOINTS.replace(
            'WeatherLocation("kent", 51.20, 0.70)',
            'WeatherLocation("kent", latitude=51.2, longitude=0.7)',
        ),
        encoding="utf-8",
    )
    with pytest.raises(locations.LocationsError, match="module holds"):
        locations.load_sites(gridflow, "SOLAR_LOCATIONS")


def test_distance_is_great_circle() -> None:
    # one degree of latitude on the mean-radius sphere
    assert locations.distance_km(53.0, 0.0, 54.0, 0.0) == pytest.approx(111.195, abs=1e-3)
    # Triton Knoll: the request and the archive's grid point
    assert locations.distance_km(53.45, 0.42, 53.391914, 0.171429) == pytest.approx(17.7, abs=0.05)


# ------------------------------------------------------------------------- statistics from silver


def test_demand_stats(tmp_path: Path) -> None:
    gridflow = _gridflow(tmp_path)
    stamps = _stamps(
        START - dt.timedelta(hours=5), HOURS + 10
    )  # a few hours either side of the window
    cold = START + dt.timedelta(days=400, hours=7)
    frames = []
    for name, lat, lon in (("london", 51.49, -0.16), ("glasgow", 55.85, -4.22)):
        temp = [-3.0 if t == cold else (-20.0 if not START <= t < END else 10.0) for t in stamps]
        hdd = [max(0.0, 15.5 - v) for v in temp]
        frames.append(_site_rows(name, lat, lon, stamps, temperature_2m_c=temp, hdd_k=hdd))
    silver = _write(tmp_path, "historical_demand", pl.concat(frames))
    payload = locations.build_payload("historical_demand", silver, gridflow)
    assert payload["dataset"] == "openmeteo/historical_demand"
    assert payload["window"] == {"start": "2022-01-01", "end": "2025-12-31", "hours": HOURS}
    assert payload["hdd_base_c"] == 15.5
    london = payload["sites"][0]
    assert london["name"] == "london" and london["configured"] == {
        "lat": "51.5074",
        "lon": "-0.1278",
    }
    st = london["stats"]
    assert st["coldest_c"] == -3.0  # the -20 hours outside the window are not counted
    assert st["coldest_at"] == cold.strftime("%Y-%m-%dT%H:%MZ")
    assert st["mean_temp_c"] == pytest.approx((10.0 * (HOURS - 1) - 3.0) / HOURS, abs=1e-3)
    assert st["hdd_per_year"] == pytest.approx((5.5 * (HOURS - 1) + 18.5) / 24 / 4, abs=0.05)
    assert london["offset_km"] == pytest.approx(
        locations.distance_km(51.5074, -0.1278, 51.49, -0.16), abs=0.05
    )


def test_wind_stats_and_a_missing_hour(tmp_path: Path) -> None:
    gridflow = _gridflow(tmp_path)
    stamps = _stamps(START, HOURS)
    speeds = [float(i % 13) for i in range(HOURS)]
    frames = [
        _site_rows("hornsea", 53.884, 1.737, stamps, wind_speed_100m_mps=speeds),
        _site_rows("pen_y_cymoedd", 51.705, -3.607, stamps, wind_speed_100m_mps=speeds),
    ]
    silver = _write(tmp_path, "historical_wind", pl.concat(frames))
    payload = locations.build_payload("historical_wind", silver, gridflow)
    ordered = sorted(speeds)
    pos = 0.9 * (HOURS - 1)
    lo = int(pos)
    p90 = ordered[lo] + (ordered[lo + 1] - ordered[lo]) * (pos - lo)
    hornsea = payload["sites"][0]
    assert hornsea["group"] == "Offshore, southern North Sea"
    assert hornsea["stats"]["mean_100m_mps"] == pytest.approx(sum(speeds) / HOURS, abs=1e-3)
    assert hornsea["stats"]["p90_100m_mps"] == pytest.approx(p90, abs=1e-3)

    short = pl.concat([frames[0].head(HOURS - 1), frames[1]])
    (silver / "open_meteo" / "historical_wind" / "year=2022" / "part.parquet").unlink()
    _write(tmp_path / "again", "historical_wind", short)
    with pytest.raises(locations.LocationsError, match="35063 of 35064 hours"):
        locations.build_payload("historical_wind", tmp_path / "again" / "silver", gridflow)


def test_solar_days_follow_the_hour_ending_stamp(tmp_path: Path) -> None:
    gridflow = _gridflow(tmp_path)
    # stamps from 00:00 on the first day to 00:00 after the last: the first covers the hour before
    # the window, the last the final hour of 2025
    stamps = _stamps(START, HOURS + 1)

    def ghi(t: dt.datetime) -> float:
        if t == START:
            return 9999.0  # the hour 23:00 to 00:00 on 31 December 2021: outside the window
        if t == END:
            return 3000.0  # the hour 23:00 to 00:00 on 31 December 2025: inside it
        if t.hour != 13:
            return 0.0
        return {6: 2000.0, 12: 500.0}.get(t.month, 1000.0)

    values = [ghi(t) for t in stamps]
    silver = _write(
        tmp_path,
        "historical_solar",
        _site_rows("kent", 51.213, 0.647, stamps, shortwave_radiation_wm2=values),
    )
    st = locations.build_payload("historical_solar", silver, gridflow)["sites"][0]["stats"]
    days = HOURS // 24
    june, december, rest = 4 * 30, 4 * 31, days - 4 * 30 - 4 * 31
    total = june * 2.0 + december * 0.5 + rest * 1.0 + 3.0
    assert st["mean_daily_kwh_m2"] == pytest.approx(total / days, abs=1e-3)
    assert (st["sunniest_month"], st["sunniest_kwh_m2"]) == (6, 2.0)
    assert st["darkest_month"] == 12
    assert st["darkest_kwh_m2"] == pytest.approx((december * 0.5 + 3.0) / december, abs=1e-3)


def test_distil_flag_runs_the_locations_step(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    gridflow = _gridflow(tmp_path)
    stamps = _stamps(START, HOURS)
    frames = [
        _site_rows(n, 51.0, 0.0, stamps, temperature_2m_c=[5.0] * HOURS, hdd_k=[10.5] * HOURS)
        for n in ("london", "glasgow")
    ]
    silver = _write(tmp_path, "historical_demand", pl.concat(frames))
    rc = distil.main(
        [
            "--locations",
            "--dry-run",
            "--silver-path",
            str(silver),
            "--gridflow-path",
            str(gridflow),
            "--dataset",
            "openmeteo/historical_demand",
        ]
    )
    assert rc == 0
    assert "openmeteo/historical_demand: 2 sites, 35064 hours each" in capsys.readouterr().out
