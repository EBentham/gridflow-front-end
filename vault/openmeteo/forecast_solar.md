---
source: open_meteo
dataset_key: forecast_solar
vendor: Open-Meteo
last_verified: 2026-06-04
layer_coverage: bronze, silver
---

# Open-Meteo — Forecast Solar Weather (GB capacity-weighted sites, 1–16 days)

## Overview

Hourly solar-irradiance forecast for the next 1–16 days at the **6
capacity-weighted GB solar sites** (East Anglia (Norfolk),
Wiltshire/Somerset, Kent, Cornwall, Sussex, Oxfordshire). Same
variable set, location list, and tilt geometry as
[historical_solar](./historical_solar.md): full irradiance
decomposition (GHI / DNI / DHI / GTI at `tilt=35°`, `azimuth=0°`),
cloud cover at three heights, and snow variables.

Used as the forward-looking solar-PV forecast feed for short-term
generation forecasting and bid optimisation. New at F7.5.

→ This dataset answers: *what irradiance is forecast at the GB solar
sites over the next N hours, both on horizontal and on a UK fixed tilt
panel?* For lookback / backtesting, use
[historical_solar](./historical_solar.md). For population-centre or
wind-site forecasts, use [forecast_demand](./forecast_demand.md) or
[forecast_wind](./forecast_wind.md).

`forecast_solar` is **net-new at F7.5** — no F0-era predecessor.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://api.open-meteo.com/v1` |
| Path             | `/forecast` |
| Method           | GET |
| Auth             | None (public, free tier — no key, no header) |
| Rate limit       | Soft limit ~10 000 requests/day per IP (vendor-published, free tier); ~600/min burst. Project caps at 5 req/s. |
| Pagination       | None — chunk via `start_date` / `end_date` (or `forecast_days`) |
| Historical depth | Forward-looking only — supports `past_days` to stitch up to ~92 days of recent past, but the canonical path for past data is the [archive endpoint](./historical_solar.md) |
| Publication lag  | Model-dependent; the vendor lists update intervals per model (open-meteo.com/en/docs, read 2026-10-06), e.g. ICON "Every 3 hours", GFS "Every hour", IFS "Every 6 hours". The connector pins no model, and the response does not name the run it came from |
| Response format  | JSON (columnar — one parallel array per variable) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `latitude` | float | Yes | WGS-84 latitude in decimal degrees | `52.62` |
| `longitude` | float | Yes | WGS-84 longitude in decimal degrees | `1.05` |
| `hourly` | csv string | Yes | Comma-separated variable names — connector requests **12** fields | `temperature_2m,shortwave_radiation,direct_radiation,...` |
| `tilt` | int | Yes (for GTI) | Panel tilt above horizontal, degrees | `35` |
| `azimuth` | int | Yes (for GTI) | Panel azimuth, degrees — Open-Meteo PV convention `0=S, ±180=N` (NOT compass) | `0` |
| `forecast_days` | int | No | Number of forecast days (default 7, max 16) | `2` |
| `start_date` | date | No | Window start; gridflow uses this | `2026-05-08` |
| `end_date` | date | No | Window end; gridflow uses this | `2026-05-09` |
| `timezone` | string | No (default `GMT`) | Connector always passes `UTC` | `UTC` |
| `models` | csv string | No | Pin a specific NWP model — connector does not pin | — |

The connector's `WeatherDatasetSpec.extra_params` for `forecast_solar`
is `(("tilt", "35"), ("azimuth", "0"))` — same UK fixed-tilt
representative geometry (35° tilt, due south) as the archive counterpart.

Connector requests these `hourly` variables (`endpoints.SOLAR_HOURLY_VARS`):
`temperature_2m`, `shortwave_radiation`, `direct_radiation`,
`direct_normal_irradiance`, `diffuse_radiation`,
`global_tilted_irradiance`, `cloud_cover`, `cloud_cover_low`,
`cloud_cover_mid`, `cloud_cover_high`, `snowfall`, `snow_depth`.

**What a time stamp covers** (vendor variable table, open-meteo.com/en/docs,
read 2026-10-06): the irradiance variables are a "Preceding hour mean" in
W/m², so the row stamped 12:00 covers 11:00 to 12:00; `snowfall` is a
"Preceding hour sum" in cm of snow; `temperature_2m`, the `cloud_cover`
variables and `snow_depth` are "Instant". Stamps are UTC (`timezone=UTC`).
See [historical_solar](./historical_solar.md#query-parameters) for the quotes.

### Working curl example

```bash
# No auth required — Cornwall, 2 days forecast with full irradiance set
curl --ssl-no-revoke -fsS \
  "https://api.open-meteo.com/v1/forecast?latitude=50.30&longitude=-5.00&hourly=shortwave_radiation,direct_radiation,direct_normal_irradiance,diffuse_radiation,global_tilted_irradiance,cloud_cover&tilt=35&azimuth=0&forecast_days=2&timezone=UTC"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/open_meteo/forecast_solar__<location>/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per (location, fetch). The connector iterates
the six `SOLAR_LOCATIONS` per call and emits one `RawResponse` per
site. The `dataset` field on each `RawResponse` is
`f"forecast_solar__{location.name}"` (**double underscore**), so
bronze partitions live under `bronze/open_meteo/forecast_solar__<site>/...`.
The silver transformer's `BRONZE_DATASET_PREFIX` is `"forecast_solar"`.

### Bronze sample

```json
{
  "latitude": 50.30,
  "longitude": -5.00,
  "generationtime_ms": 0.65,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "elevation": 35.0,
  "hourly_units": {
    "time": "iso8601",
    "shortwave_radiation": "W/m²",
    "direct_radiation": "W/m²",
    "direct_normal_irradiance": "W/m²",
    "diffuse_radiation": "W/m²",
    "global_tilted_irradiance": "W/m²",
    "cloud_cover": "%",
    "snowfall": "cm",
    "snow_depth": "m"
  },
  "hourly": {
    "time": ["2026-05-08T11:00", "2026-05-08T12:00", "2026-05-08T13:00"],
    "temperature_2m": [14.5, 15.8, 16.6],
    "shortwave_radiation": [580.0, 700.0, 720.0],
    "direct_radiation": [400.0, 500.0, 520.0],
    "direct_normal_irradiance": [750.0, 770.0, 780.0],
    "diffuse_radiation": [180.0, 200.0, 200.0],
    "global_tilted_irradiance": [670.0, 770.0, 790.0],
    "cloud_cover": [30.0, 25.0, 20.0],
    "cloud_cover_low": [15.0, 10.0, 5.0],
    "cloud_cover_mid": [10.0, 10.0, 10.0],
    "cloud_cover_high": [5.0, 5.0, 5.0],
    "snowfall": [0.0, 0.0, 0.0],
    "snow_depth": [0.0, 0.0, 0.0]
  }
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/open_meteo/forecast_solar/year=YYYY/month=MM/forecast_solar_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.openmeteo.forecast.ForecastSolarWeather`
**Pydantic schema**: `gridflow.schemas.weather.SolarWeather`
**Dedup key**: `(timestamp_utc, location)` — `df.unique(subset=["timestamp_utc", "location"], keep="last")`
**Point-in-time field**: `available_at` — bitemporal stamp from `BaseSilverTransformer` (F0). No `forecast_run_at`; older vintages overwritten on re-transform (which fetch wins: see Known issues).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | `hourly.time[i]` | UTC tz applied |
| `location` | `str` | No | derived | Site key from `SOLAR_LOCATIONS` |
| `latitude` | `float` | No | top-level `latitude` | Float64. The forecast model's grid-cell centre, not the requested site point, and not the archive's cell. Cornwall: requested 50.30, returned 50.30215 |
| `longitude` | `float` | No | top-level `longitude` | Float64. Grid-cell centre, as `latitude`. Cornwall: requested -5.00, returned -5.004654 |
| `temperature_2m_c` | `float` | Yes | `hourly.temperature_2m[i]` | °C |
| `shortwave_radiation_wm2` | `float` | Yes | `hourly.shortwave_radiation[i]` | GHI, W/m² |
| `direct_radiation_wm2` | `float` | Yes | `hourly.direct_radiation[i]` | Beam on horizontal, W/m² |
| `direct_normal_irradiance_wm2` | `float` | Yes | `hourly.direct_normal_irradiance[i]` | DNI, W/m² |
| `diffuse_radiation_wm2` | `float` | Yes | `hourly.diffuse_radiation[i]` | DHI, W/m² |
| `global_tilted_irradiance_wm2` | `float` | Yes | `hourly.global_tilted_irradiance[i]` | GTI on UK fixed tilt (35°, due south = azimuth 0), W/m² |
| `cloud_cover_pct` | `float` | Yes | `hourly.cloud_cover[i]` | % |
| `cloud_cover_low_pct` | `float` | Yes | `hourly.cloud_cover_low[i]` | % |
| `cloud_cover_mid_pct` | `float` | Yes | `hourly.cloud_cover_mid[i]` | % |
| `cloud_cover_high_pct` | `float` | Yes | `hourly.cloud_cover_high[i]` | % |
| `snowfall_cm` | `float` | Yes | `hourly.snowfall[i]` | Snowfall over the preceding hour in cm of snow, not water equivalent (vendor: divide by 7 for water mm) |
| `snow_depth_m` | `float` | Yes | `hourly.snow_depth[i]` | Standing snow depth, m |
| `data_provider` | `str` | No | derived | Constant `"open_meteo"` |
| `ingested_at` | `datetime[UTC]` | Yes | derived | Wall-clock UTC at silver-build time |

Bitemporal columns (`event_time`, `available_at`, `source_run_id`,
`dataset_version`) are stamped at write time; `DATASET_VERSION = "2.0.0"`.

**No `air_density_kg_m3` derivation on this dataset** — same rationale
as [historical_solar](./historical_solar.md#silver-schema): the solar
variable list does not request `surface_pressure`. Property test
`tests/unit/test_openmeteo_air_density.py` asserts the solar
transformer does NOT carry air density.

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2026, 5, 8, 11, 0, tzinfo=UTC),
        "location": "cornwall",
        "latitude": 50.30215,
        "longitude": -5.004654,
        "temperature_2m_c": 14.5,
        "shortwave_radiation_wm2": 580.0,
        "direct_radiation_wm2": 400.0,
        "direct_normal_irradiance_wm2": 750.0,
        "diffuse_radiation_wm2": 180.0,
        "global_tilted_irradiance_wm2": 670.0,
        "cloud_cover_pct": 30.0,
        "cloud_cover_low_pct": 15.0,
        "cloud_cover_mid_pct": 10.0,
        "cloud_cover_high_pct": 5.0,
        "snowfall_cm": 0.0,
        "snow_depth_m": 0.0,
        "data_provider": "open_meteo",
        "ingested_at": datetime(2026, 5, 9, 9, 12, 5, tzinfo=UTC),
    },
    {
        "timestamp_utc": datetime(2026, 5, 8, 12, 0, tzinfo=UTC),
        "location": "kent",
        "latitude": 51.202526,
        "longitude": 0.7145386,
        "temperature_2m_c": 17.0,
        "shortwave_radiation_wm2": 720.0,
        "direct_radiation_wm2": 510.0,
        "direct_normal_irradiance_wm2": 800.0,
        "diffuse_radiation_wm2": 210.0,
        "global_tilted_irradiance_wm2": 790.0,
        "cloud_cover_pct": 20.0,
        "cloud_cover_low_pct": 5.0,
        "cloud_cover_mid_pct": 10.0,
        "cloud_cover_high_pct": 5.0,
        "snowfall_cm": 0.0,
        "snow_depth_m": 0.0,
        "data_provider": "open_meteo",
        "ingested_at": datetime(2026, 5, 9, 9, 12, 5, tzinfo=UTC),
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **On-disk GTI is south-facing (checked 2026-10-06; supersedes the OM-04
  "north-facing, known-wrong" note).** The pre-fix `azimuth=180` silver is no
  longer on disk: local silver now holds only 1 to 5 Aug and 13 to 22 Sep 2026,
  from fetches on 2026-08-16 and 2026-09-26 whose bronze sidecars record
  `tilt=35&azimuth=0`. Midday (12:00 and 13:00 UTC, clear hours) median
  GTI/GHI is 1.15 in Aug and 1.40 in Sep, never below 0.8. See OM-04.
- **No `air_density_kg_m3` on this dataset** — see
  [historical_solar §Known issues and gotchas](./historical_solar.md#known-issues-and-gotchas).
  Solar variable list does not request `surface_pressure`.
- **GTI requires `tilt` and `azimuth`** — same `tilt=35`, `azimuth=0`
  (due south) as historical via `WeatherDatasetSpec.extra_params`.
- **Two-host design.** Forecast lives at `api.open-meteo.com`, while
  [historical_solar](./historical_solar.md) lives at
  `archive-api.open-meteo.com`.
- **Unpinned NWP model.** Open-Meteo's forecast endpoint uses a router;
  irradiance forecast skill varies by model. If reproducibility
  matters, pin via `models=<id>`.
- **Forecast vintages overwritten.** No `forecast_run_at` column; one row
  per `(timestamp_utc, location)`. Silver day D reads one bronze partition
  per site: the exact date D if it has files, else the nearest earlier one
  within 35 days (`silver/openmeteo/historical.py:183-197`,
  `silver/base.py:2337-2365`), keeping only D's hours and, within that
  partition, the last file in name (fetch-time) order
  (`historical.py:258`, `unique(keep="last")`). So a newer fetch that
  started on an earlier date than an existing exact partition does not
  replace it. `available_at` is the time gridflow stored the response, an
  ingest-run stamp, not a model run time (`VINTAGE_POLICY =
  None`, `forecast.py:65`), not a model run time.
- **Past dates are fetched as asked.** The connector sends `start_date` and
  `end_date` as given (`connectors/openmeteo/client.py:109-116`) and does
  not refuse past windows. Every row in local silver was fetched after its
  target hour (1 to 6 Aug fetched 2026-08-16; 13 to 22 Sep fetched
  2026-09-26), so none is a forecast made ahead of time. What `/forecast`
  returns for past dates is not documented in this note; the vendor points
  to its Historical Forecast API for archived runs.
- **Approximate site centroids** — see ADR-020. All 6 sites are below
  53° N (south-east bias).
- **Snow shading.** Same caveat as
  [historical_solar](./historical_solar.md) — snow yield-collapse
  modelling belongs in feature engineering.
- **`past_days` not used.** For past data, use the
  [historical_solar](./historical_solar.md) endpoint.
- **Bronze double-underscore separator.** Bronze paths use
  `forecast_solar__<site>`, **not** `forecast_solar_<site>`.
- **Naming.** Vault folder `open-meteo`, Python package `openmeteo`,
  config key `open_meteo` — see [README §Naming](../README.md#naming).

---

## Implementation delta

- **Net-new dataset at F7.5.** Bronze backfill needed before query
  use; commands documented in F7.5-RESULTS.md.
- **GTI tilt/azimuth via `extra_params`** — same approach as
  `historical_solar`.
- **No air-density derivation** — see Known issues.
- **No `forecast_run_at` column.**
- **No model pinning.**
- **`SolarWeather` Pydantic schema** present at F7.5 in
  `src/gridflow/schemas/weather.py`. Same schema as historical for
  symmetry; `BaseOpenMeteoTransformer` shares the pivot logic.

---

## Modelling notes

- **Day-ahead solar-PV modelling.** `global_tilted_irradiance` is the
  most direct feature for fixed-tilt sites at 35° due south. For tracker
  installations the GTI underestimates; use `direct_normal_irradiance`
  and a tracker-specific transposition.
- **Cloud-cover dynamics.** Forecast cloud cover at three heights is
  particularly useful for hour-ahead nowcast features.
- **Forecast-skill backtests.** Not possible from the stored rows: there
  is no `forecast_run_at`, and every stored row was fetched after its
  target hour (see Known issues), so no row has a positive lead time.
  Lead-time features against [historical_solar](./historical_solar.md)
  need forecasts captured ahead of the hour first.
- **Status of the notes above.** The day-ahead and nowcast uses describe
  what the forecast host can serve when fetched ahead of time, not what
  the stored rows hold.
- **Aggregate forecast.** Sites are GW-capacity-weighted south-east
  hotspots; weight by installed capacity per region for GB-aggregate
  forecast.

---

## Links

- [Official API docs (Forecast)](https://open-meteo.com/en/docs)
- `Python/gridflow/src/gridflow/connectors/openmeteo/client.py`
- `Python/gridflow/src/gridflow/silver/openmeteo/forecast.py`
- `Python/gridflow/src/gridflow/schemas/weather.py`
- [Gold view/builder](#) — none
- [Historical counterpart](./historical_solar.md)
- [Demand forecast (7 cities)](./forecast_demand.md)
- [Wind forecast (12 sites)](./forecast_wind.md)
- `Python/gridflow/docs/DECISION_LOG/ADR-020-openmeteo-location-approximation.md`
