---
source: neso
dataset_key: intensity_stats
vendor: National Energy System Operator (NESO)
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Carbon intensity statistics
  summary: >-
    NESO's GB carbon intensity statistics, labelled gCO2/kWh by gridflow: maximum, average and
    minimum with a band, over a window or 24-hour blocks.
  facts:
    vendor: "NESO Carbon Intensity API, routes `/intensity/stats/{from}/{to}` and `/{block}`"
    cadence: "On request; gridflow asks for windows of at most 14 days (NESO allows 30)"
    grain: "One row per window or block, from its `from` and `to`"
  landscape: power
  what_it_is: >-
    NESO's maximum, average and minimum GB carbon intensity over a window, labelled gCO2/kWh by
    gridflow, with an index band. `intensity_stats` returns one summary per window;
    `intensity_stats_block` splits it into blocks, and gridflow always asks for 24 hours. The
    fields do not say which half-hourly values they summarise; the notebook sets 13 to 21
    September's blocks beside daily `actual` figures.
  how_used:
    - "A daily carbon regime feature: the day's average, range and band in one row."
    - "Cross-checking `carbon_intensity`: 13 to 21 September's daily `actual` extremes and rounded means agree."
    - Ranking days by average intensity to pick low-carbon days for shifted load.
  chart:
    type: line
    silver: neso/intensity_stats_block
    time: timestamp_utc
    value: average_gco2_kwh
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-21"}
    unit: gCO2/kWh
  chart_view:
    title: Daily average carbon intensity, 13 to 21 September 2026
    caption: >-
      Silver `neso/intensity_stats_block`, gCO2/kWh (gridflow's label): NESO's average for each
      24-hour UTC block, 13 to 21 September 2026, one point a day. The chart shows the block member;
      the frame below holds 14 to 21 September's maximum and minimum.
    alt: >-
      Line chart of NESO's daily average GB carbon intensity from neso/intensity_stats_block, in
      gCO2/kWh, one point per 24-hour UTC block, 13 to 21 September 2026. It falls from 168 on the
      13th and 146 on the 14th to 77 on the 15th, recovers to 113 on the 16th, then sits at 65, 61
      and 60 from the 17th to the 19th before rising to 84 on the 20th and 164 on the 21st.
    x_label: block start, UTC; each block runs 24 hours
    key:
      - {series: average_gco2_kwh, label: Daily average, codes: gCO2/kWh, paint: petrol, note: "NESO's `average` for each 24-hour block, plotted at the block's start."}
  raw_feed:
    note: >-
      Every input is a path segment. gridflow splits the ingest window into requests of at most 14
      days; the block is always 24 hours.
    requests:
      - "GET https://api.carbonintensity.org.uk/intensity/stats/2026-09-13T00:00Z/2026-09-22T00:00Z/24"
      - "GET https://api.carbonintensity.org.uk/intensity/stats/2026-08-01T00:00Z/2026-08-06T00:00Z"
    commands:
      - {run: gridflow ingest neso intensity_stats_block --start 2026-09-13 --end 2026-09-22, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform neso intensity_stats_block --start 2026-09-13 --end 2026-09-13, comment: "bronze is filed under first day"}
  record:
    select:
      silver: neso/intensity_stats_block
      filter:
        - {column: timestamp_utc, op: ge, value: "2026-09-14T00:00:00Z"}
        - {column: timestamp_utc, op: lt, value: "2026-09-22T00:00:00Z"}
      order_by: [timestamp_utc]
      columns: [timestamp_utc, average_gco2_kwh, max_gco2_kwh, min_gco2_kwh, intensity_index, period_end_utc]
    key: [timestamp_utc, period_end_utc]
    caption: "`intensity_stats_block`: the 24-hour blocks starting 14 to 21 September 2026, oldest first."
    fields:
      timestamp_utc: "Start of the window or block, the vendor's `from`, read as UTC"
      period_end_utc: "End of the window or block, the vendor's `to`; a day later here"
      average_gco2_kwh: "NESO's `average` over the block; gCO2/kWh is gridflow's label, the response states none"
      max_gco2_kwh: "NESO's `max`: the block's highest value, same gridflow label"
      min_gco2_kwh: "NESO's `min`: the block's lowest value, same gridflow label"
      intensity_index: "NESO's band; the API docs list five, `very low` to `very high`"
  notebook:
    lead: >-
      `query()` reads `silver_neso_intensity_stats_block` and `silver_neso_carbon_intensity`,
      filtered on `timestamp_utc` with both ends included; lineage columns dropped. The cells set
      NESO's blocks beside daily figures from the half-hourly `actual` values.
    cells:
      - |
        blk = data.neso.query("intensity_stats_block", "2026-09-13", "2026-09-21")
        ci = data.neso.query("carbon_intensity", "2026-09-13", "2026-09-21")
        for df in (blk, ci):
            df["timestamp_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
        blk = blk.sort_values("timestamp_utc").set_index("timestamp_utc")
      - blk[["average_gco2_kwh", "max_gco2_kwh", "min_gco2_kwh", "intensity_index"]].head()
      - |
        day = (ci.set_index("timestamp_utc").actual_gco2_kwh
               .resample("1D").agg(["max", "mean", "min"]).add_prefix("actual_"))
        blk[["max_gco2_kwh", "average_gco2_kwh", "min_gco2_kwh"]].join(day.round(2))
      - |
        ax = blk[["max_gco2_kwh", "average_gco2_kwh", "min_gco2_kwh"]].plot(
            ylabel="gCO2/kWh", marker="o", figsize=(8, 3.5), color=["#C77E3C", "#155A6E", "#66793B"])
    needs: NESO block statistics and half-hourly intensity, 13 to 21 September 2026
    plot_alt: >-
      Line plot with markers of NESO's daily maximum (clay), average (petrol) and minimum (olive)
      carbon intensity, gCO2/kWh, 13 to 21 September 2026. The maximum runs from 87 on the 18th to
      216 on the 21st, the minimum from 34 on the 15th to 106 on the 21st; the average falls from
      168 to 60, then ends at 164.
  related:
    - {dataset: neso/carbon_intensity, note: "Half-hourly actual and forecast intensity; the notebook recomputes blocks from it"}
    - {dataset: neso/generation, note: "Half-hourly fuel mix shares for the same days"}
    - {dataset: neso/intensity_factors, note: "Per-fuel emission factors, under the same gCO2/kWh label"}
    - {dataset: neso/regional_intensity, note: "Intensity by region, where these statistics are national only"}
  family:
    slug: intensity-statistics
    members:
      - dataset: intensity_stats
        differs: "One summary for the whole request window, at most 14 days"
        request: "GET https://api.carbonintensity.org.uk/intensity/stats/2026-08-01T00:00Z/2026-08-06T00:00Z"
      - dataset: intensity_stats_block
        differs: "The window split into 24-hour blocks, one row per block; charted here"
        request: "GET https://api.carbonintensity.org.uk/intensity/stats/2026-09-13T00:00Z/2026-09-22T00:00Z/24"
---

# NESO - National carbon intensity statistics (`intensity_stats`)

## Overview

This dataset summarises GB carbon intensity over a requested time block rather than exposing every raw half hour. It answers how clean or carbon-heavy a period was in aggregate, useful for regime features, rolling labels, and QA against half-hour intensity series. See [Carbon intensity](../../../20-domain/concepts/carbon-intensity.md) and [Settlement period](../../../20-domain/concepts/settlement-period.md).

---

## API endpoint

| Property | Value |
|----------|-------|
| Base URL | `https://api.carbonintensity.org.uk` |
| Path | `/intensity/stats/{from}/{to}` |
| Method | GET |
| Auth | None; send `Accept: application/json` |
| Rate limit | Not documented by NESO; Gridflow config uses 10 req/s. |
| Pagination | None. Dynamic inputs are path segments, not query parameters. |
| Historical depth | TODO - official docs do not state earliest date; max 30 days per request |
| Publication lag | Derived from available intensity observations |
| Response format | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| from | string | Yes | Path parameter: Start datetime in ISO8601 format YYYY-MM-DDThh:mmZ | 2024-01-15T00:00Z |
| to | string | Yes | Path parameter: End datetime in ISO8601 format YYYY-MM-DDThh:mmZ | 2024-01-16T00:00Z |

### Working curl example

```bash
curl --ssl-no-revoke -X GET \
  "https://api.carbonintensity.org.uk/intensity/stats/2024-01-15T00:00Z/2024-01-16T00:00Z" \
  -H "Accept: application/json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/neso/intensity_stats/<year>/<month>/<day>/raw_<timestamp>_<hash>.json`
**Format**: Raw JSON, as received. Immutable after write, with `.meta.json` provenance sidecar.
**Granularity**: One file per request window of at most 14 days, filed under the window's first day (`data_date=window_start.date()`, `connectors/neso/carbon_intensity.py:79`). Silver reads only that exact partition, so a window's rows land in one silver file named for its first day.

### Bronze sample

```json
{"data":[{"from":"2024-01-15T00:00Z","to":"2024-01-16T00:00Z","intensity":{"max":250,"average":180,"min":120,"index":"moderate"}}]}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/neso/intensity_stats/year=<YYYY>/month=<MM>/intensity_stats_<YYYYMMDD>.parquet`
**Transformer class**: `gridflow.silver.neso.carbon_intensity.IntensityStatsTransformer`
**Pydantic schema**: `gridflow.schemas.neso.CarbonIntensityStats`
**Dedup key**: `(timestamp_utc, period_end_utc)`
**Point-in-time field**: `timestamp_utc`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | from | Stats block start. |
| period_end_utc | datetime[UTC] | Yes | to | Stats block end. |
| max_gco2_kwh | float | Yes | intensity.max | Maximum carbon intensity in block. |
| average_gco2_kwh | float | Yes | intensity.average | Average carbon intensity in block. |
| min_gco2_kwh | float | Yes | intensity.min | Minimum carbon intensity in block. |
| intensity_index | str | No | intensity.index | Docs category string: one of very low, low, moderate, high, very high in docs (recorded in `carbon_intensity.md`, silver schema `intensity_index` row). |
| data_provider | str | No | derived | Always neso. |
| ingested_at | datetime[UTC] | No | derived | Silver transform timestamp. |

### Silver sample

```python
[{"timestamp_utc":"2024-01-15T00:00:00+00:00","period_end_utc":"2024-01-16T00:00:00+00:00","max_gco2_kwh":250.0,"average_gco2_kwh":180.0,"min_gco2_kwh":120.0,"intensity_index":"moderate","data_provider":"neso","ingested_at":"2026-05-04T00:00:00+00:00"}]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- Official docs use UTC timestamps ending in `Z`; keep joins in UTC.
- The connector sends no query parameters; all documented inputs are path parameters.
- The response sends `max`, `average` and `min` as bare numbers with no unit (bronze bodies, e.g. `bronze/neso/intensity_stats/2026/08/01/`); `gCO2/kWh` is gridflow's column label (`_transform_stats`, `silver/neso/carbon_intensity.py:501-528`).

---

## Implementation delta

- **`from` / `to` placeholders**: official docs and `config/sources.yaml` use `{from}` and `{to}`; `src/gridflow/connectors/neso/endpoints.py` uses `{from_dt}` and `{to_dt}` internally before formatting the same path.
- **`max_query_days`**: official docs allow 30 days for statistics; the connector chunks at 14 days with its own constant `_MAX_DAYS_PER_REQUEST = 14` (`connectors/neso/carbon_intensity.py:21`, chunk loop `:149-164`), which matches `max_query_days: 14` in `config/sources.yaml`. So one `intensity_stats` row summarises one chunk: an ingest window longer than 14 days gives several rows, not one summary of the whole window.

---

## Modelling notes

Use averages/min/max as rolling carbon regime features. Do not mix block statistics with half-hour targets without aligning the block window and avoiding leakage.

---

## Links

- [Official API docs](https://carbon-intensity.github.io/api-definitions/)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/neso/carbon_intensity.py)
- [Endpoint metadata](../../../../../../Python/gridflow/src/gridflow/connectors/neso/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/neso/carbon_intensity.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/neso.py)
- [Gold view/builder](../../../../../../Python/gridflow/src/gridflow/gold/views/uk_imbalance_context.sql)
- [Domain: Carbon intensity](../../../20-domain/concepts/carbon-intensity.md)

