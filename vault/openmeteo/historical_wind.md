---
source: open_meteo
dataset_key: historical_wind
vendor: Open-Meteo
last_verified: 2026-06-03
layer_coverage: bronze, silver
page:
  title: Weather at GB wind farms
  summary: >-
    Hourly weather at 12 GB wind-farm locations from Open-Meteo's archive and forecast APIs,
    including wind at 10 m and 100 m.
  facts:
    vendor: Open-Meteo, historical weather (archive) and forecast APIs
    cadence: One value per hour, stamped in UTC
    grain: One row per hour and wind location
  landscape: power
  what_it_is: >-
    Hourly weather at 12 points near GB wind farms (approximate centres from capacity registers):
    eight offshore, four onshore. Wind speed at 10 m and 100 m, direction, 10 m gusts, temperature,
    pressure, cloud, dew point and precipitation; gridflow converts speeds to m/s and derives air
    density. The forecast member adds 80, 120 and 180 m and keeps no issue time.
  how_used:
    - Weather inputs to a GB wind generation model, fitted against `fuelhh` WIND outturn.
    - Air density and the 10 m to 100 m shear for power-curve corrections.
  chart:
    type: line
    silver: open_meteo/historical_wind
    time: timestamp_utc
    value: wind_speed_100m_mps
    filter:
      - {column: location, op: in, value: [beatrice, walney, hornsea, whitelee]}
    group: location
    series_order: [beatrice, walney, hornsea, whitelee]
    aggregation: last
    window: {start: "2025-09-29", end: "2025-10-05"}
    unit: m/s
  chart_view:
    title: 100 m wind, 29 September to 5 October 2025
    caption: >-
      Silver `open_meteo/historical_wind` (archive member only), `wind_speed_100m_mps` in m/s,
      29 September to 5 October 2025 UTC. Four of 12 sites (three offshore coasts, one
      onshore) over a week from near calm to 34.9. Forecast rows (no issue time) are not drawn.
    alt: >-
      Line chart of wind speed at 100 m from open_meteo/historical_wind, in m/s, hourly from 29
      September to 5 October 2025 UTC, at Beatrice, Walney, Hornsea and Whitelee. All four stay at
      or below 15.2 m/s to the end of 1 October, with lows of 0.4 at Beatrice and 0.5 at Walney on
      the 29th and 0.4 at Hornsea on the 30th. On 3 October Walney peaks at 27.0, Whitelee at 26.4
      and Beatrice at 34.9 (23:00); Hornsea peaks at 24.4 on the 4th. All end between 10.1 and 12.5.
    x_label: hour, UTC
    key:
      - {series: beatrice, label: "Beatrice, offshore", codes: beatrice, note: "Moray Firth; the highest point, 34.9 m/s at 23:00 UTC on 3 October", paint: petrol}
      - {series: walney, label: "Walney, offshore", codes: walney, note: Irish Sea, paint: horizon}
      - {series: hornsea, label: "Hornsea, offshore", codes: hornsea, note: Southern North Sea, paint: olive}
      - {series: whitelee, label: "Whitelee, onshore", codes: whitelee, note: Scotland, paint: clay}
  locations:
    title: Where the weather is taken
    caption: >-
      The 12 points gridflow requests for wind farms, each with the grid point answering it.
      Triton Knoll's point lies 28 km west of the farm, answered on the coast, so its statistics describe
      the coast. Charted sites keep their colours.
  raw_feed:
    note: >-
      One request per location; bronze files each location's response under the window's first
      day. gridflow sends no `models`, so Open-Meteo answers with its default model blend.
    requests:
      - "GET https://archive-api.open-meteo.com/v1/archive?latitude=53.88&longitude=1.79&hourly=temperature_2m%2Csurface_pressure%2Cwind_speed_10m%2Cwind_speed_100m%2Cwind_direction_10m%2Cwind_direction_100m%2Cwind_gusts_10m%2Ccloud_cover%2Ccloud_cover_low%2Ccloud_cover_mid%2Ccloud_cover_high%2Cdew_point_2m%2Cprecipitation&start_date=2025-09-29&end_date=2025-10-05&timezone=UTC"
    commands:
      - {run: gridflow ingest open_meteo historical_wind --start 2025-09-29 --end 2025-10-05, comment: "bronze; the end date is fetched"}
      - {run: gridflow transform open_meteo historical_wind --start 2025-09-29 --end 2025-10-05, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: eq, value: "2025-10-03T23:00:00Z"}
        - {column: location, op: in, value: [beatrice, seagreen, highland_central, whitelee, walney, hornsea, triton_knoll, pen_y_cymoedd]}
      order_by: [location]
      columns: [location, timestamp_utc, wind_speed_100m_mps, wind_speed_10m_mps, wind_gusts_10m_mps, wind_direction_100m_deg, air_density_kg_m3]
    key: [timestamp_utc, location]
    caption: "23:00 UTC on 3 October 2025 at eight of the 12 locations, in alphabetical order."
    fields:
      location: "gridflow's name for one of its 12 GB wind locations"
      timestamp_utc: "The hour Open-Meteo stamps, in UTC because gridflow sends `timezone=UTC`"
      wind_speed_100m_mps: "Wind speed at 100 m, an instant value; km/h converted to m/s"
      wind_speed_10m_mps: "Wind speed at 10 m, an instant value; km/h converted to m/s"
      wind_gusts_10m_mps: "Gust speed at 10 m for the stamped hour; km/h converted to m/s"
      wind_direction_100m_deg: "Wind direction at 100 m, in degrees"
      air_density_kg_m3: "Derived by gridflow: dry-air density from surface pressure and 2 m temperature"
      latitude: "Latitude of the grid point Open-Meteo answered with, not the request's"
      longitude: "Longitude of the grid point Open-Meteo answered with, not the request's"
      temperature_2m_c: "Air temperature at 2 m, °C"
      surface_pressure_hpa: "Surface pressure, hPa"
      wind_direction_10m_deg: "Wind direction at 10 m, in degrees"
      cloud_cover_pct: "Total cloud cover, %"
      cloud_cover_low_pct: "Low cloud cover, %"
      cloud_cover_mid_pct: "Mid-level cloud cover, %"
      cloud_cover_high_pct: "High cloud cover, %"
      dew_point_2m_c: "Dew point at 2 m, °C"
      precipitation_mm: "Precipitation in mm, summed over the hour before the stamp"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_open_meteo_historical_wind`, filtered on
      `timestamp_utc`, whole UTC days with both ends included; lineage columns and `vintage_policy`
      are dropped, `ingested_at` stays.
    source: open_meteo
    cells:
      - |
        df = data.open_meteo.query("historical_wind", "2025-09-29", "2025-10-05")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
        df = df.sort_values(["timestamp_utc", "location"], ignore_index=True)
      - |
        df[["timestamp_utc", "location", "wind_speed_10m_mps", "wind_speed_100m_mps", "wind_gusts_10m_mps"]].head()
      - |
        shear = df.wind_speed_100m_mps / df.wind_speed_10m_mps
        shear.groupby(df.location).median().round(2).sort_values()
      - |
        sites = ["beatrice", "walney", "hornsea", "whitelee"]
        wide = df[df.location.isin(sites)].pivot(index="timestamp_utc", columns="location", values="wind_speed_100m_mps")[sites]
        wide.plot(ylabel="wind speed at 100 m, m/s", color=["#155A6E", "#3E8C97", "#66793B", "#C77E3C"], figsize=(8, 3.5));
    needs: 29 September to 5 October 2025
    plot_alt: >-
      Line plot of wind_speed_100m_mps against timestamp_utc, 29 September to 5 October 2025, for
      beatrice (petrol), walney (horizon), hornsea (olive) and whitelee (clay). All four stay under
      about 19 m/s until 3 October, when beatrice spikes to about 35 m/s late on. On the
      4th whitelee drops to 10 to 19 m/s; the offshore three stay about 18 to 27.
  related:
    - {dataset: elexon/fuelhh, note: "WIND outturn to fit these wind speeds against"}
    - {dataset: elexon/agws, note: "Offshore and onshore wind generation, to match the location types"}
    - {dataset: elexon/windfor, note: "GB wind generation forecast, a benchmark for a weather-driven model"}
    - {dataset: openmeteo/historical_solar, note: "The same archive and model blend at six solar locations"}
  family:
    slug: wind-weather
    members:
      - dataset: historical_wind
        differs: "Archive host, default model blend; wind at 10 m and 100 m only"
        request: "GET https://archive-api.open-meteo.com/v1/archive?latitude=53.88&longitude=1.79&hourly=temperature_2m%2Csurface_pressure%2Cwind_speed_10m%2Cwind_speed_100m%2Cwind_direction_10m%2Cwind_direction_100m%2Cwind_gusts_10m%2Ccloud_cover%2Ccloud_cover_low%2Ccloud_cover_mid%2Ccloud_cover_high%2Cdew_point_2m%2Cprecipitation&start_date=2025-09-29&end_date=2025-10-05&timezone=UTC"
      - dataset: forecast_wind
        differs: "Forecast host; adds 80, 120, 180 m; keeps no model run or issue time"
        request: "GET https://api.open-meteo.com/v1/forecast?latitude=53.88&longitude=1.79&hourly=temperature_2m%2Csurface_pressure%2Cwind_speed_10m%2Cwind_speed_100m%2Cwind_direction_10m%2Cwind_direction_100m%2Cwind_gusts_10m%2Ccloud_cover%2Ccloud_cover_low%2Ccloud_cover_mid%2Ccloud_cover_high%2Cdew_point_2m%2Cprecipitation%2Cwind_speed_80m%2Cwind_speed_120m%2Cwind_speed_180m%2Cwind_direction_80m%2Cwind_direction_120m%2Cwind_direction_180m&start_date=2026-09-13&end_date=2026-09-22&timezone=UTC"
---

# Open-Meteo — Historical Wind Weather (archive, GB capacity-weighted sites)

## Overview

Hourly historical wind-relevant weather from Open-Meteo's archive API
(not pure ERA5: the connector sends no `models` parameter,
`connectors/openmeteo/client.py:109-116`, and the vendor docs say "The
default Best Match combines IFS HRES, ERA5 and ERA5-Land seamlessly";
checked 2026-10-06) at **12 capacity-weighted GB wind sites** — 8 offshore
clusters (Dogger Bank, Hornsea, East Anglia, Triton Knoll, Walney,
Gwynt y Môr, Beatrice, Seagreen) and 4 onshore (Highland Central,
Borders Crystal Rig, Whitelee, Pen y Cymoedd). New at F7.5.

Used as the wind-generation backtest feed — `wind_speed_10m` and
`wind_speed_100m` are the headline features, paired with directions,
gusts, cloud cover, dew point (icing risk), and derived air density
(turbine power-curve density correction).

→ This dataset answers: *what wind speed/direction/gust occurred at
the GB wind sites over hours h0..h1?* For near-real-time use
[forecast_wind](./forecast_wind.md). For population-centre or solar-site
weather, use [historical_demand](./historical_demand.md) or
[historical_solar](./historical_solar.md).

`historical_wind` was added at F7.5; it has no F0-era predecessor.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://archive-api.open-meteo.com/v1` |
| Path             | `/archive` |
| Method           | GET |
| Auth             | None (public, free tier — no key, no header) |
| Rate limit       | Soft limit ~10 000 requests/day per IP (vendor-published, free tier); ~600/min burst. Project caps at 5 req/s in `config/sources.yaml`. |
| Pagination       | None — chunk via `start_date` / `end_date` window |
| Historical depth | 1940-01-01 (the depth of the blend's ERA5 component — vendor states "since 1940") |
| Publication lag  | Not one figure: no model is pinned, and the vendor docs give ERA5 and ERA5-Land "Daily with 5 days delay" but IFS HRES "Every 6 hours with no delay"; the response does not say which model answered an hour (checked 2026-10-06) |
| Response format  | JSON (columnar — one parallel array per variable) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `latitude` | float | Yes | WGS-84 latitude in decimal degrees | `53.88` |
| `longitude` | float | Yes | WGS-84 longitude in decimal degrees | `1.79` |
| `start_date` | date | Yes | Inclusive start of the window, `YYYY-MM-DD` | `2025-01-15` |
| `end_date` | date | Yes | Inclusive end of the window, `YYYY-MM-DD` | `2025-01-21` |
| `hourly` | csv string | Yes | Comma-separated variable names — connector requests **13** archive fields | `temperature_2m,wind_speed_10m,...` |
| `timezone` | string | No (default `GMT`) | Connector always passes `UTC` | `UTC` |

Connector requests these `hourly` variables (`endpoints.WIND_ARCHIVE_VARS`):
`temperature_2m`, `surface_pressure`, `wind_speed_10m`,
`wind_speed_100m`, `wind_direction_10m`, `wind_direction_100m`,
`wind_gusts_10m`, `cloud_cover`, `cloud_cover_low`, `cloud_cover_mid`,
`cloud_cover_high`, `dew_point_2m`, `precipitation`.

**`WIND_ARCHIVE_VARS` deliberately excludes `wind_speed_{80,120,180}m`
and the matching directions — see [Archive 10m+100m
limitation](#archive-10m100m-limitation).**

### Working curl example

```bash
# No auth required — Hornsea offshore probe
curl --ssl-no-revoke -fsS \
  "https://archive-api.open-meteo.com/v1/archive?latitude=53.88&longitude=1.79&start_date=2025-01-15&end_date=2025-01-21&hourly=wind_speed_10m,wind_speed_100m,wind_gusts_10m,dew_point_2m,cloud_cover&timezone=UTC"
```

Verified 2026-05-09 (F7.5 hub-height verification): HTTP 200, 168
hourly entries (7 days × 24 hours), 10m and 100m non-null for all hours.

---

## Archive 10m+100m limitation

The archive reliably exposes only **`wind_speed_10m`** and
**`wind_speed_100m`** for hub-height wind. Heights `80m`, `120m`,
`180m` return `units: "undefined"` and **all-null** values. Verified
2026-05-09 against:

| Probe                          | 10m units | 80m units    | 100m units | 120m units   | 180m units   | Mean 10m | Mean 100m | Corr 10/100m |
|--------------------------------|-----------|--------------|------------|--------------|--------------|---------:|----------:|-------------:|
| Hornsea (53.88, 1.79) offshore | km/h      | undefined ❌ | km/h       | undefined ❌ | undefined ❌ | 23.81    | 27.08     | 0.949        |
| Whitelee (55.69, -4.27) onshore| km/h      | undefined ❌ | km/h       | undefined ❌ | undefined ❌ | 18.58    | 30.87     | 0.977        |

The 10m → 100m ratio differs by regime (offshore mean 1.14, onshore
1.66), which is itself a feature signal (the Hellmann shear exponent).
Both fields therefore carry distinct information despite the high
correlation.

`WIND_ARCHIVE_VARS` deliberately excludes `wind_speed_{80,120,180}m`
and the matching directions to avoid silver carrying empty columns.
The wider hub-height set is available on the **forecast** endpoint —
see [forecast_wind](./forecast_wind.md). `WindWeather` types all
hub-height fields `float | None`, but silver shape is **not** identical:
the transformer writes only the columns of its own variable list
(`silver/openmeteo/historical.py:296-313`), so this table has no 80m /
120m / 180m columns at all (checked 2026-10-06).

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/open_meteo/historical_wind__<location>/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per (location, fetch). The connector iterates
the twelve `WIND_LOCATIONS` per call and emits one `RawResponse` per
site. The `dataset` field on each `RawResponse` is
`f"historical_wind__{location.name}"` (**double underscore**), so bronze
partitions live under
`bronze/open_meteo/historical_wind__<site>/...`. The silver
transformer's `BRONZE_DATASET_PREFIX` is `"historical_wind"`.

### Bronze sample

```json
{
  "latitude": 53.88,
  "longitude": 1.79,
  "generationtime_ms": 0.55,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "elevation": 0.0,
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C",
    "surface_pressure": "hPa",
    "wind_speed_10m": "km/h",
    "wind_speed_100m": "km/h",
    "wind_direction_10m": "°",
    "wind_direction_100m": "°",
    "wind_gusts_10m": "km/h",
    "cloud_cover": "%",
    "dew_point_2m": "°C",
    "precipitation": "mm"
  },
  "hourly": {
    "time": ["2025-01-15T00:00", "2025-01-15T01:00"],
    "temperature_2m": [4.2, 3.9],
    "surface_pressure": [1010.2, 1009.8],
    "wind_speed_10m": [22.5, 24.1],
    "wind_speed_100m": [25.8, 27.4],
    "wind_direction_10m": [225.0, 228.0],
    "wind_direction_100m": [230.0, 232.0],
    "wind_gusts_10m": [38.0, 41.0],
    "cloud_cover": [85.0, 90.0],
    "cloud_cover_low": [60.0, 75.0],
    "cloud_cover_mid": [25.0, 15.0],
    "cloud_cover_high": [0.0, 0.0],
    "dew_point_2m": [3.0, 2.8],
    "precipitation": [0.0, 0.1]
  }
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/open_meteo/historical_wind/year=YYYY/month=MM/historical_wind_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.openmeteo.historical.HistoricalWindWeather`
**Pydantic schema**: `gridflow.schemas.weather.WindWeather`
**Dedup key**: `(timestamp_utc, location)` — `df.unique(subset=["timestamp_utc", "location"], keep="last")`
**Point-in-time field**: `available_at` — bitemporal stamp from `BaseSilverTransformer` (F0). Stability of archive values is not documented: the default blend includes IFS HRES, which has no delay, so recent hours may not be ERA5 values.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | `hourly.time[i]` | UTC tz applied |
| `location` | `str` | No | derived | Site key from `WIND_LOCATIONS` (hornsea, dogger_bank, walney, ...) |
| `latitude` | `float` | No | top-level `latitude` | Float64 |
| `longitude` | `float` | No | top-level `longitude` | Float64 |
| `temperature_2m_c` | `float` | Yes | `hourly.temperature_2m[i]` | °C |
| `surface_pressure_hpa` | `float` | Yes | `hourly.surface_pressure[i]` | hPa |
| `precipitation_mm` | `float` | Yes | `hourly.precipitation[i]` | mm, sum of the preceding hour (vendor docs) |
| `wind_speed_10m_mps` | `float` | Yes | `hourly.wind_speed_10m[i]` | m/s at 10m |
| `wind_speed_80m_mps` | `float` | Yes | not requested on archive | **column not written on this dataset** — see [Archive limitation](#archive-10m100m-limitation) |
| `wind_speed_100m_mps` | `float` | Yes | `hourly.wind_speed_100m[i]` | m/s at 100m |
| `wind_speed_120m_mps` | `float` | Yes | not requested on archive | **column not written on this dataset** |
| `wind_speed_180m_mps` | `float` | Yes | not requested on archive | **column not written on this dataset** |
| `wind_direction_10m_deg` | `float` | Yes | `hourly.wind_direction_10m[i]` | degrees (0=N) |
| `wind_direction_80m_deg` | `float` | Yes | not requested on archive | **column not written on this dataset** |
| `wind_direction_100m_deg` | `float` | Yes | `hourly.wind_direction_100m[i]` | degrees |
| `wind_direction_120m_deg` | `float` | Yes | not requested on archive | **column not written on this dataset** |
| `wind_direction_180m_deg` | `float` | Yes | not requested on archive | **column not written on this dataset** |
| `wind_gusts_10m_mps` | `float` | Yes | `hourly.wind_gusts_10m[i]` | Peak gust 10m, m/s |
| `cloud_cover_pct` | `float` | Yes | `hourly.cloud_cover[i]` | Total cover, % |
| `cloud_cover_low_pct` | `float` | Yes | `hourly.cloud_cover_low[i]` | % |
| `cloud_cover_mid_pct` | `float` | Yes | `hourly.cloud_cover_mid[i]` | % |
| `cloud_cover_high_pct` | `float` | Yes | `hourly.cloud_cover_high[i]` | % |
| `dew_point_2m_c` | `float` | Yes | `hourly.dew_point_2m[i]` | °C — proxy for icing risk |
| `air_density_kg_m3` | `float` | Yes | derived | `surface_pressure_Pa / (287.05 × T_K)` — turbine power-curve density correction |
| `data_provider` | `str` | No | derived | Constant `"open_meteo"` |
| `ingested_at` | `datetime[UTC]` | Yes | derived | Wall-clock UTC at silver-build time |

The schema declares 80m / 120m / 180m fields for symmetry with
`forecast_wind`; on this dataset the columns are absent, because the
transformer outputs only `WIND_ARCHIVE_VARS` columns
(`silver/openmeteo/historical.py:296-313`). Bitemporal columns
(`event_time`, `available_at`, `source_run_id`, `dataset_version`) are
stamped at write time; `DATASET_VERSION = "2.0.0"`.

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2025, 1, 15, 0, 0, tzinfo=UTC),
        "location": "hornsea",
        "latitude": 53.88,
        "longitude": 1.79,
        "temperature_2m_c": 4.2,
        "surface_pressure_hpa": 1010.2,
        "precipitation_mm": 0.0,
        "wind_speed_10m_mps": 6.25,
        "wind_speed_80m_mps": None,
        "wind_speed_100m_mps": 7.17,
        "wind_speed_120m_mps": None,
        "wind_speed_180m_mps": None,
        "wind_direction_10m_deg": 225.0,
        "wind_direction_80m_deg": None,
        "wind_direction_100m_deg": 230.0,
        "wind_direction_120m_deg": None,
        "wind_direction_180m_deg": None,
        "wind_gusts_10m_mps": 10.56,
        "cloud_cover_pct": 85.0,
        "cloud_cover_low_pct": 60.0,
        "cloud_cover_mid_pct": 25.0,
        "cloud_cover_high_pct": 0.0,
        "dew_point_2m_c": 3.0,
        "air_density_kg_m3": 1.273,
        "data_provider": "open_meteo",
        "ingested_at": datetime(2026, 5, 9, 9, 12, 5, tzinfo=UTC),
    },
    {
        "timestamp_utc": datetime(2025, 1, 15, 12, 0, tzinfo=UTC),
        "location": "whitelee",
        "latitude": 55.69,
        "longitude": -4.27,
        "temperature_2m_c": 1.8,
        "surface_pressure_hpa": 1004.5,
        "precipitation_mm": 0.4,
        "wind_speed_10m_mps": 4.89,
        "wind_speed_80m_mps": None,
        "wind_speed_100m_mps": 7.86,
        "wind_speed_120m_mps": None,
        "wind_speed_180m_mps": None,
        "wind_direction_10m_deg": 250.0,
        "wind_direction_80m_deg": None,
        "wind_direction_100m_deg": 254.0,
        "wind_direction_120m_deg": None,
        "wind_direction_180m_deg": None,
        "wind_gusts_10m_mps": 8.33,
        "cloud_cover_pct": 95.0,
        "cloud_cover_low_pct": 80.0,
        "cloud_cover_mid_pct": 30.0,
        "cloud_cover_high_pct": 5.0,
        "dew_point_2m_c": 0.5,
        "air_density_kg_m3": 1.279,
        "data_provider": "open_meteo",
        "ingested_at": datetime(2026, 5, 9, 9, 12, 5, tzinfo=UTC),
    },
]
```

---

### Vintage policy (ADR-031, added 2026-09-06)

Archive rows emit no vendor `published_at`. gridflow v0.20 declares a
**Vintage Policy** on the historical transformer (`silver/openmeteo/historical.py`;
the forecast transformer sets `VINTAGE_POLICY = None`):

| Field | Value |
|---|---|
| name | `open_meteo-historical_wind/vp-2026-09` |
| lag | **5 days** after the hour — from this page's "~5 days behind real time" ERA5 reanalysis cadence (vault-sourced, not vendor-guaranteed; the default blend's IFS HRES part has no delay, so this is the code's assumption, not a property of every row) |
| applies_before | `2026-08-01T00:00Z` (the August 2026 smoke ingest); earlier `event_time` is reconstructed, later rows keep the ingest clock |
| rule | `available_at = coalesce(published_at, event_time + 5d)` only when `event_time < applies_before` AND `event_time + 5d < ingest_stamp`; otherwise the ingest stamp |

Every row carries a `vintage_policy` label (policy name / `"ingest-clock"` /
`"vendor"`); pre-v0.20 parquet reads as null — treat null as unknown. Source of
truth: `docs/DECISION_LOG/ADR-031-vintage-policy-reconstruction.md`.

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Archive 10m+100m limitation.** See [§ above](#archive-10m100m-limitation).
  Hub heights {80m, 120m, 180m} are silently null on the archive endpoint;
  the connector deliberately does not request them. The forecast endpoint
  carries the wider set.
- **Approximate site centroids.** The 12 wind locations are
  capacity-weighted approximations, not per-turbine NRO coordinates.
  See `docs/DECISION_LOG/ADR-020-openmeteo-location-approximation.md`
  for the rationale (vendor licensing, NRO data ergonomics, modelling
  granularity trade-off).
- **Two-host design.** Wind archive lives at
  `archive-api.open-meteo.com`, while [forecast_wind](./forecast_wind.md)
  lives at `api.open-meteo.com`. The connector chooses the correct host
  via the `historical_*` dataset prefix.
- **Archive lag.** No model is pinned. The vendor docs give ERA5 and
  ERA5-Land a 5-day delay and IFS HRES none, and the response does not
  say which model answered an hour. End_date within the last 5 days may
  return null trailing values.
- **Grid-cell snapping.** `latitude` / `longitude` echoed in the
  response can differ from the request (snapped to a grid cell of the
  model that answered). Silver stores the *response* values.
- **Wind units.** Silver wind speeds and gusts are in **m/s** — the
  connector converts the km/h archive response (`m/s = km/h / 3.6`), so
  the `_mps`-suffixed columns are power-curve-ready.
- **`air_density_kg_m3` requires `surface_pressure`.** Both are
  requested on this dataset, so the derivation is always populated when
  the archive returns the underlying fields.
- **Bronze double-underscore separator.** Bronze paths use
  `historical_wind__<site>`, **not** `historical_wind_<site>`.
- **Naming.** Vault folder `open-meteo`, Python package `openmeteo`,
  config key `open_meteo` — see [README §Naming](../README.md#naming).
  Do not rename.

---

## Implementation delta

- **Hub-height archive limitation observed and locked into
  `WIND_ARCHIVE_VARS`** (verified 2026-05-09; documented above).
  `WIND_FORECAST_VARS` includes the wider set as `WIND_ARCHIVE_VARS +
  (wind_speed_80m, wind_speed_120m, wind_speed_180m, wind_direction_80m,
  wind_direction_120m, wind_direction_180m)`.
- **Added at F7.5.** Backfill commands are documented in
  `.planning/phases/F7.5-open-meteo-renewable-extension/F7.5-RESULTS.md`
  under "Re-ingest commands".
- **Approximate locations** — see ADR-020. If a future modelling phase
  needs per-turbine resolution, the location list is upgradable in
  `endpoints.py:WIND_LOCATIONS` without schema changes.
- **`WindWeather` Pydantic schema** added at F7.5 in
  `src/gridflow/schemas/weather.py`. All hub-height fields typed
  `float | None` so the same schema validates both archive (sparse) and
  forecast (dense) silver writes.

---

## Modelling notes

- **Wind-generation modelling.** `wind_speed_10m` and
  `wind_speed_100m` are the headline features; the 10m → 100m ratio
  is a useful shear-derived feature. Cube-root or
  power-curve-mapped derivations belong in feature engineering, not
  silver. (Silver wind is already m/s, so no km/h conversion is needed
  before applying turbine power curves.)
- **Air-density correction.** `air_density_kg_m3` is the canonical
  correction term applied to manufacturer power curves at standard
  density (1.225 kg/m³). Useful as a multiplicative or residual
  feature.
- **Icing risk.** `dew_point_2m` near or below freezing combined with
  high cloud cover and precipitation flags icing windows; offshore
  blade icing is a documented operational risk.
- **Backtest joins.** Pair against Elexon `windfor` (NESO-published
  wind forecast) for forecast-skill backtests, and against Elexon
  `fuelhh` `WIND` field for actual aggregate output.
- **Spatial aggregation.** Sites are GW-capacity-weighted; for
  GB-aggregate wind output, weight by installed offshore + onshore
  capacity per site rather than equally.

---

## Links

- [Official API docs (Historical Weather)](https://open-meteo.com/en/docs/historical-weather-api)
- `Python/gridflow/src/gridflow/connectors/openmeteo/client.py`
- `Python/gridflow/src/gridflow/silver/openmeteo/historical.py`
- `Python/gridflow/src/gridflow/schemas/weather.py`
- [Gold view/builder](#) — none
- [Forecast counterpart](./forecast_wind.md)
- [Demand weather (7 cities)](./historical_demand.md)
- [Solar weather (6 sites)](./historical_solar.md)
- `Python/gridflow/docs/DECISION_LOG/ADR-020-openmeteo-location-approximation.md`
