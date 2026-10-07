---
source: open_meteo
dataset_key: historical_solar
vendor: Open-Meteo
last_verified: 2026-06-04
layer_coverage: bronze, silver
page:
  title: Weather at GB solar sites
  summary: >-
    Hourly irradiance, cloud cover and temperature at six GB solar sites from Open-Meteo: archive
    history, plus forecast-host values fetched after the hour.
  facts:
    vendor: Open-Meteo, Historical Weather API and Forecast API
    cadence: Hourly; archive ERA5 and ERA5-Land 5 days late, ECMWF IFS without delay
    grain: One row per UTC hour and site, six GB solar sites
    history: Archive from 1940 (ERA5); the Forecast API serves up to 16 days ahead
  landscape: power
  what_it_is: >-
    Twelve variables at six solar sites, Cornwall to Norfolk: irradiance, horizontal and on a panel
    tilted 35° south, cloud at three heights, temperature, snow. `historical_solar` reads the
    archive. `forecast_solar` reads the forecast host for any dates gridflow sends; every stored row
    was fetched days after its hour, so they are after-the-fact values, not forecasts. No model run
    is kept.
  how_used:
    - Irradiance on the tilted panel as the main feature of a solar output model.
    - The direct and diffuse split, to tell clear hours from overcast ones.
    - "The forecast member's request and columns, a template for capturing real forecasts."
  chart:
    type: line
    silver: open_meteo/historical_solar
    time: timestamp_utc
    value: shortwave_radiation_wm2
    filter:
      - {column: location, op: in, value: [cornwall, kent]}
    group: location
    series_order: [cornwall, kent]
    aggregation: mean
    window: {start: "2026-06-13", end: "2026-06-19"}
    unit: "W/m²"
  chart_view:
    title: Hourly irradiance, Cornwall and Kent, 13 to 19 June 2026
    caption: >-
      Silver `historical_solar`, global horizontal irradiance in W/m², one value per hour, 13 to 19
      June 2026 UTC, two of the six sites. Each value is the vendor's mean over the hour ending at
      its stamp. `forecast_solar` is not drawn.
    alt: >-
      Line chart of global horizontal irradiance from open_meteo/historical_solar, in W/m², one
      value per hour, 13 to 19 June 2026 UTC, for Cornwall and Kent. Both lines sit at or near
      zero each night. On the 13th both peak at the 13:00 UTC stamp, Cornwall at 903 and Kent at 877. From
      the 15th Cornwall's daily peak falls to between 281, on the 17th, and 696, while Kent's stays
      between 703 and 860.
    x_label: UTC; each value covers the hour before
    key:
      - {series: cornwall, label: Cornwall, codes: cornwall, paint: horizon}
      - {series: kent, label: Kent, codes: kent, paint: clay}
  locations:
    title: Where the weather is taken
    caption: >-
      The six points gridflow requests at GB solar sites, and the archive grid point Open-Meteo
      answered from, within about 5 km. Cornwall and Kent keep their chart colours; forecast grid
      points are not drawn.
  raw_feed:
    note: >-
      One GET per site to the archive host; `tilt=35&azimuth=0` sets the panel. `end_date` is
      inclusive and `timezone=UTC` makes stamps UTC. Bronze sits under the window's start date.
    requests:
      - "GET https://archive-api.open-meteo.com/v1/archive?latitude=50.3&longitude=-5.0&hourly=temperature_2m,shortwave_radiation,direct_radiation,direct_normal_irradiance,diffuse_radiation,global_tilted_irradiance,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,snowfall,snow_depth&start_date=2026-06-13&end_date=2026-06-19&timezone=UTC&tilt=35&azimuth=0"
    commands:
      - {run: gridflow ingest open_meteo historical_solar --start 2026-06-13 --end 2026-06-19, comment: "bronze; the end date is fetched"}
      - {run: gridflow transform open_meteo historical_solar --start 2026-06-13 --end 2026-06-19, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: location, op: eq, value: cornwall}
        - {column: timestamp_utc, op: ge, value: "2026-06-15T07:00:00+00:00"}
        - {column: timestamp_utc, op: le, value: "2026-06-15T14:00:00+00:00"}
      order_by: [timestamp_utc]
      columns: [timestamp_utc, location, shortwave_radiation_wm2, direct_radiation_wm2, diffuse_radiation_wm2, global_tilted_irradiance_wm2, cloud_cover_low_pct, cloud_cover_pct]
    key: [timestamp_utc, location]
    caption: "Cornwall, 07:00 to 14:00 UTC, 15 June 2026; under low cloud, diffuse exceeds direct from 08:00."
    fields:
      timestamp_utc: "The vendor's `time`, requested in UTC; means and sums cover the hour before it"
      location: "Site name from gridflow's fixed list of six, Cornwall to Norfolk"
      shortwave_radiation_wm2: Global horizontal irradiance, mean over the preceding hour, W/m²
      direct_radiation_wm2: Direct beam on a horizontal surface, mean over the preceding hour, W/m²
      diffuse_radiation_wm2: Diffuse sky radiation on a horizontal surface, preceding-hour mean, W/m²
      global_tilted_irradiance_wm2: "On a panel tilted 35° facing due south, preceding-hour mean, W/m²"
      cloud_cover_low_pct: Low cloud and fog up to 3 km at the stamp, %
      cloud_cover_pct: Total cloud cover at the stamp, as a percentage of the sky
      latitude: "Latitude of the vendor's grid cell, not the site point gridflow requests"
      longitude: "Longitude of the vendor's grid cell, not the site point gridflow requests"
      temperature_2m_c: Air temperature 2 m above ground at the stamp, °C
      direct_normal_irradiance_wm2: Direct beam on a surface facing the sun, preceding-hour mean, W/m²
      cloud_cover_mid_pct: Cloud from 3 to 8 km at the stamp, %
      cloud_cover_high_pct: Cloud above 8 km at the stamp, %
      snowfall_cm: Snow over the preceding hour in cm of snow, not water equivalent
      snow_depth_m: Snow lying on the ground at the stamp, metres
  notebook:
    source: open_meteo
    lead: >-
      Returns a pandas DataFrame from `silver_open_meteo_historical_solar`, filtered on
      `timestamp_utc`, both end dates included; lineage columns dropped. The cells total each day
      in kWh/m², then split Cornwall's irradiance into direct and diffuse.
    cells:
      - |
        df = data.open_meteo.query("historical_solar", "2026-06-13", "2026-06-19")
        df["timestamp_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
        df = df.sort_values(["timestamp_utc", "location"], ignore_index=True)
        noon = df[df.timestamp_utc.dt.hour == 12]
        noon[["timestamp_utc", "location", "shortwave_radiation_wm2", "global_tilted_irradiance_wm2", "cloud_cover_pct"]].head()
      - |
        kwh = df.groupby([df.timestamp_utc.dt.date, "location"]).shortwave_radiation_wm2.sum() / 1000
        kwh.unstack().round(2)
      - |
        c = df[df.location == "cornwall"].set_index("timestamp_utc")
        c[["direct_radiation_wm2", "diffuse_radiation_wm2"]].plot.area(
            ylabel="W/m², mean of the hour before", color=["#C77E3C", "#155A6E"], figsize=(8, 3.5));
    needs: 13 to 19 June 2026
    plot_alt: >-
      Stacked area plot of Cornwall's hourly irradiance, 13 to 19 June 2026, in W/m²: direct
      (clay) below, diffuse (petrol) above, together the global value. On the 13th and 14th direct
      light is most of a midday total near 900. From the 15th diffuse makes up most of it, and the
      total peaks under 700, under 300 on the 17th.
  related:
    - {dataset: elexon/agpt, note: "GB solar outturn per half-hour, to fit against this irradiance"}
    - {dataset: neso_data_portal/embedded_wind_solar_forecast, note: "NESO's embedded solar output forecast, to compare with irradiance"}
    - {dataset: openmeteo/historical_demand, note: "Same archive at demand cities, with global irradiance only"}
    - {dataset: openmeteo/historical_wind, note: "Same archive at wind sites, with cloud cover at three heights"}
  family:
    slug: solar-weather
    members:
      - dataset: historical_solar
        differs: "Archive host; by default blends ECMWF IFS, ERA5 and ERA5-Land"
        request: "GET https://archive-api.open-meteo.com/v1/archive?latitude=50.3&longitude=-5.0&hourly=temperature_2m,shortwave_radiation,direct_radiation,direct_normal_irradiance,diffuse_radiation,global_tilted_irradiance,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,snowfall,snow_depth&start_date=2026-06-13&end_date=2026-06-19&timezone=UTC&tilt=35&azimuth=0"
      - dataset: forecast_solar
        differs: "Forecast host, own grid cells; no run time; every row fetched after its hour"
        request: "GET https://api.open-meteo.com/v1/forecast?latitude=50.3&longitude=-5.0&hourly=temperature_2m,shortwave_radiation,direct_radiation,direct_normal_irradiance,diffuse_radiation,global_tilted_irradiance,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,snowfall,snow_depth&start_date=2026-09-13&end_date=2026-09-22&timezone=UTC&tilt=35&azimuth=0"
---

# Open-Meteo — Historical Solar Weather (Open-Meteo archive, GB capacity-weighted sites)

## Overview

Hourly historical solar-irradiance values from Open-Meteo's archive at
**6 capacity-weighted GB solar sites**. The connector sends no `models`
parameter, so the archive answers with its default, which the vendor
describes as: "The default Best Match combines IFS HRES, ERA5 and
ERA5-Land seamlessly" (open-meteo.com/en/docs/historical-weather-api,
read 2026-10-06). The sites are East Anglia
(Norfolk), Wiltshire/Somerset, Kent, Cornwall, Sussex, Oxfordshire.
All sites are below the Bristol-Norwich line (53° N); GB installed
solar capacity is heavily south-east biased, and Glasgow at 55.9° N
receives ~60% of the annual irradiance of Cornwall at 50.3° N. New at
F7.5.

Used as the solar-PV-generation backtest feed. The dataset adds the
full irradiance decomposition over the F0-era `historical` set:
**GHI** (`shortwave_radiation`), **DNI** (`direct_normal_irradiance`),
**DHI** (`diffuse_radiation`), and **GTI** (`global_tilted_irradiance`)
at a UK fixed-tilt representative geometry (`tilt=35°`, `azimuth=0°`
— latitude minus ~15°, due south; Open-Meteo PV convention 0=S, ±180=N). Also carries cloud cover at three
heights and snow variables (snowfall, snow_depth) for snow-shading
events.

→ This dataset answers: *what irradiance components arrived at the GB
solar sites over hours h0..h1, both on horizontal and on a UK fixed
tilt panel?* The forecast host's counterpart is [forecast_solar](./forecast_solar.md);
its stored rows were all fetched after their hour (see its Known issues).
For population-centre or wind-site weather, use
[historical_demand](./historical_demand.md) or
[historical_wind](./historical_wind.md).

`historical_solar` is **net-new at F7.5** — no F0-era predecessor.
Historical bronze backfill required (~6 sites × 8 yr × 365 d ≈ 17 500
location-days; documented in `F7.5-RESULTS.md` but not run during
phase execution).

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://archive-api.open-meteo.com/v1` |
| Path             | `/archive` |
| Method           | GET |
| Auth             | None (public, free tier — no key, no header) |
| Rate limit       | Soft limit ~10 000 requests/day per IP (vendor-published, free tier); ~600/min burst. Project caps at 5 req/s. |
| Pagination       | None — chunk via `start_date` / `end_date` window |
| Historical depth | 1940-01-01 (ERA5 reanalysis depth — vendor states "since 1940") |
| Publication lag  | Per model (vendor docs, read 2026-10-06): ERA5 and ERA5-Land "Daily with 5 days delay"; ECMWF IFS "Every 6 hours with no delay". The default blend therefore fills recent days from IFS: a fetch at 2026-09-27 00:10 UTC returned non-null values up to 2026-09-26 23:00 |
| Response format  | JSON (columnar — one parallel array per variable) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `latitude` | float | Yes | WGS-84 latitude in decimal degrees | `52.62` |
| `longitude` | float | Yes | WGS-84 longitude in decimal degrees | `1.05` |
| `start_date` | date | Yes | Inclusive start of the window, `YYYY-MM-DD` | `2025-06-01` |
| `end_date` | date | Yes | Inclusive end of the window, `YYYY-MM-DD` | `2025-06-07` |
| `hourly` | csv string | Yes | Comma-separated variable names — connector requests **12** fields | `temperature_2m,shortwave_radiation,direct_radiation,...` |
| `tilt` | int | Yes (for GTI) | Panel tilt above horizontal, degrees | `35` |
| `azimuth` | int | Yes (for GTI) | Panel azimuth, degrees — Open-Meteo PV convention `0=S, ±180=N` (NOT compass) | `0` |
| `timezone` | string | No (default `GMT`) | Connector always passes `UTC` | `UTC` |

The connector's `WeatherDatasetSpec.extra_params` for `historical_solar`
is `(("tilt", "35"), ("azimuth", "0"))` — the UK fixed-tilt
representative geometry (35° tilt, due south). Both params are **required** when
`global_tilted_irradiance` is in the `hourly` list.

Connector requests these `hourly` variables (`endpoints.SOLAR_HOURLY_VARS`):
`temperature_2m`, `shortwave_radiation`, `direct_radiation`,
`direct_normal_irradiance`, `diffuse_radiation`,
`global_tilted_irradiance`, `cloud_cover`, `cloud_cover_low`,
`cloud_cover_mid`, `cloud_cover_high`, `snowfall`, `snow_depth`.

**What a time stamp covers** (vendor variable table, open-meteo.com/en/docs,
read 2026-10-06). The five irradiance variables are a "Preceding hour mean"
in W/m² (`shortwave_radiation`: "Shortwave solar radiation as average of the
preceding hour"), so the row stamped 12:00 covers 11:00 to 12:00. `snowfall`
is a "Preceding hour sum" in cm of snow ("For the water equivalent in
millimeter, divide by 7"). `temperature_2m`, the four `cloud_cover`
variables and `snow_depth` are "Instant" values at the stamp. Cloud layers:
low "up to 3 km altitude", mid "from 3 to 8 km", high "from 8 km". With
`timezone=UTC` the stamps are UTC (the response reports `"timezone": "GMT"`,
`utc_offset_seconds: 0`).

### Working curl example

```bash
# No auth required — Cornwall solar probe with full irradiance set
curl --ssl-no-revoke -fsS \
  "https://archive-api.open-meteo.com/v1/archive?latitude=50.30&longitude=-5.00&start_date=2025-06-01&end_date=2025-06-07&hourly=shortwave_radiation,direct_radiation,direct_normal_irradiance,diffuse_radiation,global_tilted_irradiance,cloud_cover&tilt=35&azimuth=0&timezone=UTC"
```

Verified 2026-05-09 (F7.5): GHI = `shortwave_radiation` and the
separation `GHI ≈ DNI × cos(zenith) + DHI` is a useful invariant —
silver passes through the API's separation-model output and a property
test (`tests/unit/test_openmeteo_irradiance_components.py`) asserts
`direct_radiation + diffuse_radiation` is within 5% of
`shortwave_radiation` for daylight rows.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/open_meteo/historical_solar__<location>/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per (location, fetch). The connector iterates
the six `SOLAR_LOCATIONS` per call and emits one `RawResponse` per
site. The `dataset` field on each `RawResponse` is
`f"historical_solar__{location.name}"` (**double underscore**), so
bronze partitions live under
`bronze/open_meteo/historical_solar__<site>/...`. The silver
transformer's `BRONZE_DATASET_PREFIX` is `"historical_solar"`.

### Bronze sample

```json
{
  "latitude": 50.30,
  "longitude": -5.00,
  "generationtime_ms": 0.7,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "elevation": 35.0,
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C",
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
    "time": ["2025-06-01T11:00", "2025-06-01T12:00", "2025-06-01T13:00"],
    "temperature_2m": [16.3, 17.8, 18.6],
    "shortwave_radiation": [620.0, 750.0, 780.0],
    "direct_radiation": [430.0, 540.0, 565.0],
    "direct_normal_irradiance": [780.0, 800.0, 810.0],
    "diffuse_radiation": [190.0, 210.0, 215.0],
    "global_tilted_irradiance": [710.0, 820.0, 845.0],
    "cloud_cover": [25.0, 20.0, 15.0],
    "cloud_cover_low": [10.0, 5.0, 5.0],
    "cloud_cover_mid": [10.0, 10.0, 5.0],
    "cloud_cover_high": [5.0, 5.0, 5.0],
    "snowfall": [0.0, 0.0, 0.0],
    "snow_depth": [0.0, 0.0, 0.0]
  }
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/open_meteo/historical_solar/year=YYYY/month=MM/historical_solar_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.openmeteo.historical.HistoricalSolarWeather`
**Pydantic schema**: `gridflow.schemas.weather.SolarWeather`
**Dedup key**: `(timestamp_utc, location)` — `df.unique(subset=["timestamp_utc", "location"], keep="last")`
**Point-in-time field**: `available_at` — bitemporal stamp from `BaseSilverTransformer` (F0).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | `hourly.time[i]` | UTC tz applied |
| `location` | `str` | No | derived | Site key from `SOLAR_LOCATIONS` (cornwall, kent, ...) |
| `latitude` | `float` | No | top-level `latitude` | Float64. The vendor's grid-cell centre, not the requested site point: "This coordinate might be a few kilometres away from the requested coordinate" (open-meteo.com/en/docs). Cornwall: requested 50.30, returned 50.298767 |
| `longitude` | `float` | No | top-level `longitude` | Float64. Grid-cell centre, as `latitude`. Cornwall: requested -5.00, returned -5.061493 |
| `temperature_2m_c` | `float` | Yes | `hourly.temperature_2m[i]` | °C — drives module-temperature derate |
| `shortwave_radiation_wm2` | `float` | Yes | `hourly.shortwave_radiation[i]` | GHI — global horizontal irradiance, W/m² |
| `direct_radiation_wm2` | `float` | Yes | `hourly.direct_radiation[i]` | Beam component on horizontal, W/m² |
| `direct_normal_irradiance_wm2` | `float` | Yes | `hourly.direct_normal_irradiance[i]` | DNI — beam normal to sun, W/m² |
| `diffuse_radiation_wm2` | `float` | Yes | `hourly.diffuse_radiation[i]` | DHI — diffuse on horizontal, W/m² |
| `global_tilted_irradiance_wm2` | `float` | Yes | `hourly.global_tilted_irradiance[i]` | GTI on UK fixed tilt (35°, due south = azimuth 0), W/m² |
| `cloud_cover_pct` | `float` | Yes | `hourly.cloud_cover[i]` | Total cover, % |
| `cloud_cover_low_pct` | `float` | Yes | `hourly.cloud_cover_low[i]` | % |
| `cloud_cover_mid_pct` | `float` | Yes | `hourly.cloud_cover_mid[i]` | % |
| `cloud_cover_high_pct` | `float` | Yes | `hourly.cloud_cover_high[i]` | % |
| `snowfall_cm` | `float` | Yes | `hourly.snowfall[i]` | Snowfall over the preceding hour in cm of snow, not water equivalent (vendor: divide by 7 for water mm) |
| `snow_depth_m` | `float` | Yes | `hourly.snow_depth[i]` | Standing snow depth, m |
| `data_provider` | `str` | No | derived | Constant `"open_meteo"` |
| `ingested_at` | `datetime[UTC]` | Yes | derived | Wall-clock UTC at silver-build time |

Bitemporal columns (`event_time`, `available_at`, `source_run_id`,
`dataset_version`) are stamped at write time; `DATASET_VERSION = "2.0.0"`.

**No `air_density_kg_m3` derivation on this dataset.** The solar
variable list does not request `surface_pressure`, so air density
cannot be computed and the column is omitted from `SolarWeather`. (The
demand and wind schemas do carry it; see those pages.) Property test
`tests/unit/test_openmeteo_air_density.py` asserts the solar
transformer does NOT carry air density, locking this contract in.

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2025, 6, 1, 11, 0, tzinfo=UTC),
        "location": "cornwall",
        "latitude": 50.298767,
        "longitude": -5.061493,
        "temperature_2m_c": 16.3,
        "shortwave_radiation_wm2": 620.0,
        "direct_radiation_wm2": 430.0,
        "direct_normal_irradiance_wm2": 780.0,
        "diffuse_radiation_wm2": 190.0,
        "global_tilted_irradiance_wm2": 710.0,
        "cloud_cover_pct": 25.0,
        "cloud_cover_low_pct": 10.0,
        "cloud_cover_mid_pct": 10.0,
        "cloud_cover_high_pct": 5.0,
        "snowfall_cm": 0.0,
        "snow_depth_m": 0.0,
        "data_provider": "open_meteo",
        "ingested_at": datetime(2026, 5, 9, 9, 12, 5, tzinfo=UTC),
    },
    {
        "timestamp_utc": datetime(2025, 12, 15, 12, 0, tzinfo=UTC),
        "location": "east_anglia_norfolk",
        "latitude": 52.618626,
        "longitude": 1.0074626,
        "temperature_2m_c": 4.5,
        "shortwave_radiation_wm2": 95.0,
        "direct_radiation_wm2": 12.0,
        "direct_normal_irradiance_wm2": 60.0,
        "diffuse_radiation_wm2": 83.0,
        "global_tilted_irradiance_wm2": 175.0,
        "cloud_cover_pct": 90.0,
        "cloud_cover_low_pct": 75.0,
        "cloud_cover_mid_pct": 30.0,
        "cloud_cover_high_pct": 5.0,
        "snowfall_cm": 0.2,
        "snow_depth_m": 0.01,
        "data_provider": "open_meteo",
        "ingested_at": datetime(2026, 5, 9, 9, 12, 5, tzinfo=UTC),
    },
]
```

The winter row above (Norfolk, December noon) shows the mostly-diffuse
regime under heavy cloud — DNI collapses, DHI dominates GHI, GTI on a
35° tilted panel exceeds GHI on horizontal because the steeper sun
angle is partially compensated by the panel orientation (and a touch of
ground reflection).

---

### Vintage policy (ADR-031, added 2026-09-06)

ERA5 archive rows emit no vendor `published_at`. gridflow v0.20 declares a
**Vintage Policy** on the historical transformer (`silver/openmeteo/historical.py`;
the forecast transformer sets `VINTAGE_POLICY = None`):

| Field | Value |
|---|---|
| name | `open_meteo-historical_solar/vp-2026-09` |
| lag | **5 days** after the hour — from the "~5 days behind real time" ERA5 cadence this page stated until 2026-10-06 (vault-sourced, not vendor-guaranteed). Superseded premise: the archive's default blend also uses ECMWF IFS, which the vendor lists with no delay (see API endpoint above); the policy is unchanged pending a research unit |
| applies_before | `2026-08-01T00:00Z` (the August 2026 smoke ingest); earlier `event_time` is reconstructed, later rows keep the ingest clock |
| rule | `available_at = coalesce(published_at, event_time + 5d)` only when `event_time < applies_before` AND `event_time + 5d < ingest_stamp`; otherwise the ingest stamp |

Every row carries a `vintage_policy` label (policy name / `"ingest-clock"` /
`"vendor"`); pre-v0.20 parquet reads as null — treat null as unknown. Source of
truth: `docs/DECISION_LOG/ADR-031-vintage-policy-reconstruction.md`.

## Gold layer

None implemented.

---

## Known issues and gotchas

- **On-disk GTI corrected (OM-04).** Earlier silver here was fetched at the
  pre-fix `azimuth=180` (north). The affected May-2026 dates were re-ingested
  from the ERA5 archive at `azimuth=0` and re-transformed on 2026-06-04, so
  on-disk `global_tilted_irradiance_wm2` is now south-facing and correct
  (verified: every date's solar-noon GTI exceeds GHI). See OM-04 (v0.15 VT5).
- **No `air_density_kg_m3` on this dataset.** Solar variable list does
  not request `surface_pressure`, so the derivation cannot run.
  Contract enforced by `test_openmeteo_air_density.py`. If a future
  modelling phase needs solar-site density, add `surface_pressure` to
  `SOLAR_HOURLY_VARS` and the derivation will activate via
  `BaseOpenMeteoTransformer.DERIVE_AIR_DENSITY`.
- **GTI requires `tilt` and `azimuth` query params.** The connector
  injects `tilt=35&azimuth=0` via `WeatherDatasetSpec.extra_params`
  (azimuth 0 = due south under Open-Meteo's PV convention 0=S / ±180=N).
  Modifying the tilt geometry requires a code change in
  `_SOLAR_GTI_PARAMS` and a downstream re-ingest; document any change
  here. UK fixed-tilt sites typically use latitude minus ~15°, due
  south.
- **GHI ≈ DNI·cos(z) + DHI invariant.** Property test asserts
  `direct_radiation + diffuse_radiation ≈ shortwave_radiation` within
  5% for daylight rows. Open-Meteo's separation model is the upstream
  source; silver does not re-derive components.
- **Approximate site centroids.** The 6 solar locations are
  capacity-weighted approximations; see ADR-020.
- **Snow shading.** `snowfall` and `snow_depth` are kept as features;
  panel snow cover is a documented operational risk for solar yield.
  Snow-cover modelling belongs in feature engineering, not silver.
- **Two-host design.** Solar archive lives at
  `archive-api.open-meteo.com`, while [forecast_solar](./forecast_solar.md)
  lives at `api.open-meteo.com`.
- **Archive lag depends on the model.** ERA5 and ERA5-Land arrive 5 days
  late; the default blend fills recent days from ECMWF IFS with no delay
  (vendor docs, read 2026-10-06), so a recent window returns values rather
  than trailing nulls (fetch of 2026-09-22 to 27 at 2026-09-27 00:10 UTC:
  no nulls through 2026-09-26 23:00). Whether those IFS-filled hours change
  when ERA5 arrives is not documented here.
- **Latitude bias.** All 6 sites are below 53° N. Aggregate solar
  yield modelling for GB should not be derived by averaging these
  sites with northerly load — they are deliberately south-eastern.
- **Bronze double-underscore separator.** Bronze paths use
  `historical_solar__<site>`, **not** `historical_solar_<site>`.
- **Naming.** Vault folder `open-meteo`, Python package `openmeteo`,
  config key `open_meteo` — see [README §Naming](../README.md#naming).

---

## Implementation delta

- **Net-new dataset at F7.5.** No bronze on disk; backfill required.
- **GTI tilt/azimuth via `extra_params` on `WeatherDatasetSpec`.**
  The frozen dataclass uses a tuple of `(key, value)` pairs because it
  needs to stay `frozen=True`; the connector materialises it back to a
  dict at request time. If the dataset is duplicated for a different
  tilt geometry (e.g. UK two-axis tracker representative), create a
  new `WeatherDatasetSpec` rather than mutating the existing one.
- **No air-density derivation** — see Known issues.
- **Approximate locations** — see ADR-020.
- **`SolarWeather` Pydantic schema** added at F7.5 in
  `src/gridflow/schemas/weather.py`. All irradiance fields typed
  `float | None`.

---

## Modelling notes

- **Day-ahead solar-PV modelling.** `global_tilted_irradiance` is the
  most direct feature — it represents the irradiance arriving on the
  representative panel geometry — but watch out: the tilt is fixed at
  35° due south (azimuth 0), so for sites with tracker installations the GTI will
  systematically underestimate. `shortwave_radiation` is GHI; combine
  with cloud cover for cloud-shading proxy features.
- **DNI / DHI separation.** Useful for tracker-vs-fixed comparisons
  and for clear-sky / overcast regime classification (high DNI/GHI =
  clear; low DNI/GHI = overcast).
- **Module temperature.** `temperature_2m` plus a Sandia /
  King-style temperature model belongs in feature engineering; silver
  carries the raw input.
- **Snow shading.** `snowfall` + `snow_depth` flag yield-collapse
  windows; modelling should derate during snow-cover hours.
- **Backtest joins.** Pair against Elexon `fuelhh` (national `SOLAR`
  field) for actual aggregate solar output, weighted by installed
  capacity per site. ENTSOE `actual_generation` (B16) is the EU-grid
  equivalent.
- **Spatial aggregation.** All 6 sites are south-eastern hotspots;
  for GB aggregate, weight by installed solar MW per region.

---

## Links

- [Official API docs (Historical Weather)](https://open-meteo.com/en/docs/historical-weather-api)
- `Python/gridflow/src/gridflow/connectors/openmeteo/client.py`
- `Python/gridflow/src/gridflow/silver/openmeteo/historical.py`
- `Python/gridflow/src/gridflow/schemas/weather.py`
- [Gold view/builder](#) — none
- [Forecast counterpart](./forecast_solar.md)
- [Demand weather (7 cities)](./historical_demand.md)
- [Wind weather (12 sites)](./historical_wind.md)
- `Python/gridflow/docs/DECISION_LOG/ADR-020-openmeteo-location-approximation.md`
