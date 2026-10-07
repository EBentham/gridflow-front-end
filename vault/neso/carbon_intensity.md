---
source: neso
dataset_key: carbon_intensity
vendor: National Energy System Operator (NESO)
last_verified: 2026-05-08
layer_coverage: bronze, silver, gold
page:
  title: National carbon intensity
  summary: >-
    NESO's GB national carbon intensity per half-hour in gCO2/kWh: forecast, estimated actual and
    band, through nine API routes.
  facts:
    vendor: NESO Carbon Intensity API, national intensity routes
    cadence: Half-hourly; NESO forecasts ahead and estimates actuals afterwards
    grain: One row per half-hour, keyed by its start in UTC
  landscape: power
  what_it_is: >-
    GB electricity carbon intensity in gCO2/kWh for each half-hour: NESO's forecast, its estimated
    actual, and a band from very low to very high whose cut-offs the response does not carry. The
    nine routes choose half-hours differently and parse to the same columns. NESO sends no issue
    time, so silver cannot say which forecast run a value came from.
  how_used:
    - A carbon signal beside price and demand features, joined on `timestamp_utc`.
    - Shifting flexible load into low bands; `intensity_fw48h` looks 48 hours ahead.
    - Comparing NESO's forecast with its estimated actual, the forecast as served at fetch.
  chart:
    type: line
    silver: neso/carbon_intensity
    time: timestamp_utc
    value: actual_gco2_kwh
    aggregation: last
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: gCO2/kWh
  chart_view:
    title: Estimated actual intensity, 14 to 20 September 2026
    caption: >-
      Silver `neso/carbon_intensity`, gCO2/kWh, NESO's estimated actual for each half-hour of the
      UTC days 14 to 20 September 2026. The forecast sits beside it in the frame and the notebook
      below.
    alt: >-
      Line chart of NESO's estimated actual GB carbon intensity from neso/carbon_intensity, in
      gCO2/kWh, per half-hour from 00:00 UTC on 14 September to 23:30 UTC on 20 September 2026. It
      opens at 194 and reaches its highest, 195, at 05:00 UTC on the 14th. From the 15th each day falls
      to 34 to 42 at 11:00 UTC, except the 16th at 117. Peaks at 18:00 UTC reach 156 on the 15th,
      drop to 76 on the 18th and rise to 164 on the 20th; the line ends at 138.
    x_label: UTC; each point is a half-hour's start
    key:
      - {series: actual_gco2_kwh, label: Estimated actual, paint: petrol, note: "Its band, `intensity_index`, is in the frame; the forecast is in the notebook."}
  raw_feed:
    note: >-
      NESO's Carbon Intensity API, path inputs only, up to 14 days a call. In responses checked, the
      first half-hour ends at `from`, the last at `to` (undocumented).
    requests:
      - "GET https://api.carbonintensity.org.uk/intensity/2026-09-14T00:00Z/2026-09-21T00:00Z"
    commands:
      - {run: gridflow ingest neso carbon_intensity --start 2026-09-14 --end 2026-09-21, comment: "bronze; one call, one partition"}
      - {run: gridflow transform neso carbon_intensity --start 2026-09-14 --end 2026-09-14, comment: the whole window's partition}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: ge, value: "2026-09-15T18:00:00Z"}
        - {column: timestamp_utc, op: le, value: "2026-09-15T21:30:00Z"}
      order_by: [timestamp_utc]
      columns: [timestamp_utc, forecast_gco2_kwh, actual_gco2_kwh, intensity_index, period_end_utc]
    key: [timestamp_utc]
    caption: "Half-hours from 18:00 to 21:30 UTC on 15 September; the 19:30 forecast reads 28."
    fields:
      timestamp_utc: "Start of the half-hour in UTC, the vendor's `from`"
      forecast_gco2_kwh: "NESO's forecast for the half-hour in gCO2/kWh, as served at fetch"
      actual_gco2_kwh: "NESO's estimated actual in gCO2/kWh; null until NESO estimates it"
      intensity_index: "NESO's band, very low to very high; in these rows it tracks `actual`"
      period_end_utc: "End of the half-hour in UTC, the vendor's `to`"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_neso_carbon_intensity`, filtered on `timestamp_utc` by
      UTC day, both ends included; lineage columns dropped. The cells sort by time and set the
      forecast against the estimated actual.
    cells:
      - |
        ci = data.neso.query("carbon_intensity", "2026-09-14", "2026-09-20")
        ci["timestamp_utc"] = ci.timestamp_utc.dt.tz_convert("UTC")
        ci = ci.sort_values("timestamp_utc", ignore_index=True)
      - |
        ci[["timestamp_utc", "forecast_gco2_kwh", "actual_gco2_kwh", "intensity_index"]].head()
      - |
        err = ci.forecast_gco2_kwh - ci.actual_gco2_kwh
        err.abs().describe().round(1)
      - |
        ci.set_index("timestamp_utc")[["forecast_gco2_kwh", "actual_gco2_kwh"]].plot(
            ylabel="gCO2/kWh", color=["#C77E3C", "#155A6E"], figsize=(8, 3.5))
    needs: carbon_intensity for 14 to 20 September 2026
    plot_alt: >-
      Line plot of NESO's forecast (clay) and estimated actual (petrol) in gCO2/kWh, 14 to 20
      September 2026 in UTC. The lines mostly overlap, a mean absolute gap of 9.6, from near 200
      at the start of the 14th. Single half-hour forecast drops stand out, the deepest to 28 at
      19:30 UTC on the 15th against an actual of 136.
  related:
    - {dataset: neso/regional_intensity, note: "The same measure by region and nation, from the same API"}
    - {dataset: neso/generation, note: "The fuel mix NESO reports for the same half-hours"}
    - {dataset: neso/intensity_stats, note: "NESO's maximum, average and minimum national intensity over a range"}
    - {dataset: elexon/system_prices, note: "The gold imbalance view joins prices to this series on `timestamp_utc`"}
  family:
    slug: national-carbon-intensity
    members:
      - dataset: carbon_intensity
        differs: "Any range up to 14 days a call, from `from` to `to`"
        request: "GET https://api.carbonintensity.org.uk/intensity/2026-09-14T00:00Z/2026-09-21T00:00Z"
      - dataset: intensity_at
        differs: "One half-hour per call, the record ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/intensity/2026-08-01T00:00Z"
      - dataset: intensity_current
        differs: "No inputs; the half-hour NESO serves as current, one row per call"
        request: "GET https://api.carbonintensity.org.uk/intensity"
      - dataset: intensity_date
        differs: "One call per date, returning that UK day's half-hours"
        request: "GET https://api.carbonintensity.org.uk/intensity/date/2026-08-01"
      - dataset: intensity_fw24h
        differs: "From the half-hour ending at `from`, 24 hours on; past half-hours carry actuals"
        request: "GET https://api.carbonintensity.org.uk/intensity/2026-08-01T00:00Z/fw24h"
      - dataset: intensity_fw48h
        differs: "From the half-hour ending at `from`, 48 hours on; NESO forecasts two days ahead"
        request: "GET https://api.carbonintensity.org.uk/intensity/2026-08-01T00:00Z/fw48h"
      - dataset: intensity_period
        differs: "gridflow calls once per period: 48 a day, 46 or 50 at clock changes"
        request: "GET https://api.carbonintensity.org.uk/intensity/date/2026-08-01/4"
      - dataset: intensity_pt24h
        differs: "Back 24 hours, to the half-hour ending at `from`"
        request: "GET https://api.carbonintensity.org.uk/intensity/2026-08-01T00:00Z/pt24h"
      - dataset: intensity_today
        differs: "No inputs; today's UK-day half-hours, actuals null until NESO estimates them"
        request: "GET https://api.carbonintensity.org.uk/intensity/date"
---

# NESO - National carbon intensity range (`carbon_intensity`)

## Overview

This dataset represents GB electricity carbon intensity in gCO2/kWh for half-hour market periods. It answers how carbon-heavy scheduled consumption is expected or estimated to be, which is useful as a target, feature, or regime indicator for price, balancing, demand, and carbon-aware scheduling models. See [Carbon intensity](../../../20-domain/concepts/carbon-intensity.md) and [Settlement period](../../../20-domain/concepts/settlement-period.md).

---

## API endpoint

| Property | Value |
|----------|-------|
| Base URL | `https://api.carbonintensity.org.uk` |
| Path | `/intensity/{from}/{to}` |
| Method | GET |
| Auth | None; send `Accept: application/json` |
| Rate limit | Not documented by NESO; Gridflow config uses 10 req/s. |
| Pagination | None. Dynamic inputs are path segments, not query parameters. |
| Historical depth | TODO - official docs do not state earliest date; max 14 days per request |
| Publication lag | Forecast ahead, actual as estimated after each half hour |
| Response format | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| from | string | Yes | Path parameter: Start datetime in ISO8601 format YYYY-MM-DDThh:mmZ | 2024-01-15T00:00Z |
| to | string | Yes | Path parameter: End datetime in ISO8601 format YYYY-MM-DDThh:mmZ | 2024-01-16T00:00Z |

### Working curl example

```bash
curl --ssl-no-revoke -X GET \
  "https://api.carbonintensity.org.uk/intensity/2024-01-15T00:00Z/2024-01-16T00:00Z" \
  -H "Accept: application/json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/neso/carbon_intensity/<year>/<month>/<day>/raw_<timestamp>_<hash>.json`
**Format**: Raw JSON, as received. Immutable after write, with `.meta.json` provenance sidecar.
**Granularity**: One file per API call; range and daily routes may produce one file per chunk/day/period.

### Bronze sample

```json
{"data":[{"from":"2024-01-15T00:00Z","to":"2024-01-15T00:30Z","intensity":{"forecast":245,"actual":239,"index":"moderate"}},{"from":"2024-01-15T00:30Z","to":"2024-01-15T01:00Z","intensity":{"forecast":250,"actual":248,"index":"moderate"}}]}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/neso/carbon_intensity/year=<YYYY>/month=<MM>/carbon_intensity_<YYYYMMDD>.parquet`
**Transformer class**: `gridflow.silver.neso.carbon_intensity.CarbonIntensityTransformer`
**Pydantic schema**: `gridflow.schemas.neso.CarbonIntensity`
**Dedup key**: `(timestamp_utc)`, within one silver date partition (`silver/neso/carbon_intensity.py:485`); nothing deduplicates across partitions, and the partition date is the request window's first day (`connectors/neso/carbon_intensity.py:79`)
**Point-in-time field**: `timestamp_utc`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | from | Half-hour period start. |
| period_end_utc | datetime[UTC] | Yes | to | Half-hour period end. |
| forecast_gco2_kwh | float | Yes | intensity.forecast | Forecast carbon intensity in gCO2/kWh. |
| actual_gco2_kwh | float | Yes | intensity.actual | Estimated actual carbon intensity in gCO2/kWh; often null before actuals publish. |
| intensity_index | str | No | intensity.index | One of very low, low, moderate, high, very high in docs; stored as string. |
| data_provider | str | No | derived | Always neso. |
| ingested_at | datetime[UTC] | No | derived | Silver transform timestamp. |

### Silver sample

```python
[{"timestamp_utc":"2024-01-15T00:00:00+00:00","period_end_utc":"2024-01-15T00:30:00+00:00","forecast_gco2_kwh":245.0,"actual_gco2_kwh":239.0,"intensity_index":"moderate","data_provider":"neso","ingested_at":"2026-05-04T00:00:00+00:00"},{"timestamp_utc":"2024-01-15T00:30:00+00:00","period_end_utc":"2024-01-15T01:00:00+00:00","forecast_gco2_kwh":250.0,"actual_gco2_kwh":248.0,"intensity_index":"moderate","data_provider":"neso","ingested_at":"2026-05-04T00:00:00+00:00"}]
```

---

## Gold layer

**Name**: `gold_uk_imbalance_context`
**Type**: SQL view
**File**: `src/gridflow/gold/views/uk_imbalance_context.sql`
**Joins**: `silver_elexon_system_prices_latest` LEFT JOIN `silver_neso_carbon_intensity` on `timestamp_utc` (source-qualified names; the single-token aliases are deprecated)
**Adds**: Carbon intensity forecast, actual, and index alongside Elexon system prices and imbalance volume.
**Grain (corrected 2026-07-26, v0.18 R1 Cycle A / F-01)**: one row per `(settlement_date, settlement_period)` — the winning vintage by `available_at` (system_prices is APPEND_ONLY per ADR-025). Filtering `available_at <= :as_of` is a **fail-closed cutoff, not historical point-in-time selection** (an as_of between vintages returns no row); true PIT needs the **all-vintage** `silver_elexon_system_prices` surface (or its deprecated `silver_system_prices` alias) filtered `available_at <= as_of` then latest-of-survivors, consumer-side.
**Leakage note**: `carbon_intensity_actual_gco2_kwh` is realised ex-post and NOT available at delivery time (column comment in the view). The view's comment calls the forecast column the ex-ante feature, but silver holds it as served at fetch time, not as issued (see Known issues), so it is not a verified ex-ante value.

Full column contract: see the Gold layer contracts section of
[data-contracts.md](../../../10-projects/gridflow/data-contracts.md).

---

## Known issues and gotchas

- Official docs use UTC timestamps ending in `Z`; keep joins in UTC.
- The connector sends no query parameters; all documented inputs are path parameters.
- Actual carbon intensity values can be null or absent, especially before post-period estimates are available.
- The range returns every half-hour whose end falls in `[from, to]`, both included: `/intensity/2026-08-01T00:00Z/2026-08-06T00:00Z` returned 241 half-hours, 2026-07-31 23:30 to 2026-08-05 23:30 UTC (bronze sidecar and silver, checked 2026-10-06; NESO's docs do not state it). Adjacent windows, and the 14-day chunks of a longer one (`connectors/neso/carbon_intensity.py:149-161`), therefore both return their boundary half-hour, into different partitions.
- NESO sends no issue or publish time. `available_at` is the bronze sidecar stamp on `--reingest`, else the transform clock (`silver/base.py:1181-1183`); a re-fetch into the same partition replaces the earlier values (`unique(keep="last")` over bodies in fetch order), so silver keeps no forecast vintage.
- For `intensity_period`, GB clock-change days can have 46 or 50 settlement periods in implementation even though official docs describe period 1-48.

---

## Implementation delta

- **`from` / `to` placeholders**: official docs and `config/sources.yaml` use `{from}` and `{to}`; `src/gridflow/connectors/neso/endpoints.py` uses `{from_dt}` and `{to_dt}` internally before formatting the same path.
- **`endpoint` in `config/sources.yaml`**: config stores `/intensity`; connector endpoint metadata expands this to `/intensity/{from_dt}/{to_dt}` for actual requests.
- **Distinct from `intensity_current`**: see [intensity_current](./intensity_current.md). The two datasets share the same `/intensity` path in `config/sources.yaml` but `connectors/neso/endpoints.py::ENDPOINTS` defines `carbon_intensity` as a range route (`/intensity/{from_dt}/{to_dt}`, max 14 days) and `intensity_current` as the no-arg current route (`/intensity`). Both produce the same silver schema (`CarbonIntensity`); they are not aliases — they answer different questions (current single record vs ranged history).

---

## Modelling notes

`forecast_gco2_kwh` is NESO's forecast as served at fetch time, not an issued forecast: NESO sends no issue time and silver keeps the latest fetch per partition (see Known issues), so do not treat it as a verified ex-ante feature. Use `actual_gco2_kwh` as an ex-post target or label. Filter null actuals before supervised training, join by `timestamp_utc` to Elexon prices, demand, generation, weather, and interconnector features.

---

## Links

- [Official API docs](https://carbon-intensity.github.io/api-definitions/)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/neso/carbon_intensity.py)
- [Endpoint metadata](../../../../../../Python/gridflow/src/gridflow/connectors/neso/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/neso/carbon_intensity.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/neso.py)
- [Gold view/builder](../../../../../../Python/gridflow/src/gridflow/gold/views/uk_imbalance_context.sql)
- [Domain: Carbon intensity](../../../20-domain/concepts/carbon-intensity.md)

