---
source: neso_data_portal
dataset_key: embedded_wind_solar_forecast
vendor: "NESO Open Data Portal"
last_verified: 2026-08-19
layer_coverage: "bronze, silver"
page:
  title: Embedded wind and solar forecast
  summary: >-
    NESO's forecast of GB embedded wind and solar output, with capacity, per settlement period;
    gridflow keeps every issue it captures.
  facts:
    vendor: "NESO Data Portal, resource \"Embedded Solar and Wind Forecast\""
    cadence: "NESO: hourly updates, from within the day to 14 days ahead; one issue charted"
    grain: One row per settlement date, settlement period and issue
  landscape: power
  what_it_is: >-
    NESO's forecast of embedded (distribution-connected) wind and solar output, with embedded
    capacity, for each GB settlement period. gridflow reads the resource "Embedded Solar and Wind
    Forecast": one issue per file, its instant in the filename, read as UTC. NESO's catalogue says
    the data moved to a new forecast system and recommends the "Jun - Dec" dataset.
  how_used:
    - Adding embedded output back to transmission demand to estimate underlying GB demand.
    - Embedded solar and wind as features for GB demand and price models.
    - "Forecast error: score every captured issue, not just the newest, against NESO's outturn estimates."
  chart:
    type: line
    silver: neso_data_portal/embedded_wind_solar_forecast
    time: event_time
    value: embedded_solar_forecast
    filter:
      - {column: issue_time, op: eq, value: "2026-08-20T21:25:00Z"}
    aggregation: last
    window: {start: "2026-08-20", end: "2026-09-02"}
    unit: MW
  chart_view:
    title: Embedded solar forecast, issued 20 August 2026
    caption: >-
      Silver `neso_data_portal/embedded_wind_solar_forecast`, MW, the forecast issue stamped
      21:25, read as UTC, on 20 August 2026: every settlement period it covers, from 21:00 UTC that
      day to 2 September. Lead time grows left to right.
    alt: >-
      Line chart of the embedded solar forecast, in MW, from one NESO issue stamped 21:25 (read as
      UTC) on 20 August 2026, every half-hour from 21:00 UTC on 20 August to 22:30 UTC on 2
      September. Periods starting 21:00 to 02:30 UTC stay at or near zero (63 at most, at 23:30
      UTC on the 25th). Daily peaks, between
      10:00 and 12:30 UTC, climb from 7,808 on the 21st to 11,182 at 12:00 UTC on the 24th, then
      10,051 and 8,442, and stay between 7,255 and 7,861 from the 27th.
    x_label: settlement period start, UTC
    key:
      - {series: embedded_solar_forecast, label: Embedded solar, codes: EMBEDDED_SOLAR_FORECAST, paint: chartreuse, note: "Forecast output only; the rows below give capacity, 23,301 MW."}
  raw_feed:
    note: >-
      Two calls: CKAN `package_show` names the current file, then its download link redirects to
      the CSV. The window selects nothing; each ingest captures the current issue whole.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=embedded-wind-and-solar-forecasts"
      - "GET https://api.neso.energy/dataset/91c0c70e-0ef5-4116-b6fa-7ad084b5e0e8/resource/db6c038f-98af-4570-ab60-24d71ebd0ae5/download/202608202125_embedded_forecast.csv"
    commands:
      - {run: gridflow ingest neso_data_portal embedded_wind_solar_forecast --last 24h, comment: "bronze; the current issue only"}
      - {run: gridflow transform neso_data_portal embedded_wind_solar_forecast --last 24h, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-08-24"}
        - {column: settlement_period, op: ge, value: 24}
        - {column: settlement_period, op: le, value: 31}
      order_by: [settlement_period]
      columns: [settlement_date, settlement_period, embedded_solar_forecast, issue_time, embedded_solar_capacity, embedded_wind_forecast, embedded_wind_capacity, time_gmt_raw, published_at]
    key: [settlement_date, settlement_period, issue_time]
    caption: "Settlement date 24 August 2026, periods 24 to 31: this issue's solar peak."
    fields:
      settlement_date: "GB settlement date, from `SETTLEMENT_DATE`"
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      issue_time: "Issue instant from the filename's 12-digit token, read as UTC"
      embedded_solar_forecast: "Forecast embedded solar output, `EMBEDDED_SOLAR_FORECAST`; MW in gridflow's code"
      embedded_solar_capacity: "Embedded solar capacity, `EMBEDDED_SOLAR_CAPACITY`; MW in gridflow's code; the same in these rows"
      embedded_wind_forecast: "Forecast embedded wind output, `EMBEDDED_WIND_FORECAST`; MW in gridflow's code"
      embedded_wind_capacity: "Embedded wind capacity, `EMBEDDED_WIND_CAPACITY`; MW in gridflow's code; the same in these rows"
      time_gmt_raw: "`TIME_GMT` kept as text; here the period's end, UTC clock; undocumented"
      published_at: "The file's CKAN `last_modified`, read as UTC; orders issues in `_latest`"
  notebook:
    lead: >-
      Reads `silver_neso_data_portal_embedded_wind_solar_forecast_latest` (newest issue per period),
      filtered on `settlement_date`, both ends included, dropping `event_time` and lineage columns.
      The dates match the 20 August 2026 issue; use those your capture covers.
    cells:
      - |
        df = data.neso_data_portal.query("embedded_wind_solar_forecast", "2026-08-20", "2026-09-02")
        df = df.sort_values(["settlement_date", "settlement_period"], ignore_index=True)
        df["issue_time"] = df["issue_time"].dt.tz_convert("UTC")
      - df[["settlement_date", "settlement_period", "issue_time", "embedded_solar_forecast", "embedded_wind_forecast"]].head()
      - |
        df.plot(y=["embedded_solar_forecast", "embedded_wind_forecast"], ylabel="MW",
                xlabel="settlement periods from the first in the issue",
                color=["#AFC64E", "#155A6E"], figsize=(8, 3.5));
    needs: one capture of the current file
    plot_alt: >-
      Line plot of embedded_solar_forecast and embedded_wind_forecast, in MW, against the
      settlement periods of the 20 August 2026 issue, in order. Solar forms a daily hump, highest at 11,182
      MW on the fourth hump; wind stays between 263 and 2,483 MW.
  related:
    - {dataset: neso_data_portal/historic_generation_mix, note: "NESO's outturn mix, with `wind_emb` and `solar` columns to compare"}
    - {dataset: elexon/indo, note: "Demand outturn for the same settlement periods"}
    - {dataset: elexon/windfor, note: "Elexon's wind forecast for operationally metered farms"}
    - {dataset: entsoe/wind_solar_forecast, note: "Day-ahead wind and solar forecasts for other zones; none for GB"}
---

# NESO Data Portal — Embedded Solar and Wind Forecast

## Overview

NESO's half-hourly forecast of **embedded** (distribution-connected) wind and
solar generation and capacity for GB, per settlement period. Embedded
generation is invisible to Elexon's transmission-metered datasets — it shows
up there only as suppressed demand — so this fills a gap the Elexon stack
structurally cannot: net demand, effective margin, and solar-driven demand
suppression. Each vendor file is one forecast issue, its instant stamped in
the filename; successive issues are successive vintages of the same
settlement periods. Only the **current** file is ingested; the historical
archives are catalogued but not built.

→ [Settlement period](../../../20-domain/concepts/settlement-period.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://api.neso.energy/api/3/action/` |
| Path             | `package_show?id=embedded-wind-and-solar-forecasts` → resource URL from `resources[]`, then file download (302 → presigned CDN URL) |
| Method           | GET |
| Auth             | None — keyless public API (verified 2026-08-16) |
| Rate limit       | Vendor guidance: max 1 request/second (CKAN actions); IP-block enforcement. Connector throttles every send |
| Pagination       | None; single file download |
| Historical depth | Rolling forecast window (current issue only; archive chunks exist as separate resources, not implemented — some served via the datastore bulk-dump path whose rate class is unstated, see vendor README) |
| Publication lag  | Forecast — issued ahead of real time. NESO's package `notes` (catalogue snapshot `_generated/snapshots/20260820T214455Z/catalog-snapshot.json`): half-hourly resolution, "from within day up to 14 days ahead", "updated on an hourly basis" (a vendor statement, not observed: one capture held; the resource's own description says "daily resolution", contradicted by the half-hourly rows); `issue_time` from the filename token is the authoritative issue instant, corroborated within 120 s of `ckan_last_modified` on the real capture |
| Response format  | JSON (CKAN metadata envelope) → CSV (the data file) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | string | Yes | CKAN package (dataset) slug | `embedded-wind-and-solar-forecasts` |

Resource selected by **exact `resources[].name == "Embedded Solar and Wind
Forecast"`** (D-03), format `CSV`, URL re-resolved every fetch (D-06).

### Working curl example

```bash
# Keyless — no auth header:
curl -X GET \
  "https://api.neso.energy/api/3/action/package_show?id=embedded-wind-and-solar-forecasts"
```

---

## Bronze layer

**Path pattern**: `data/bronze/neso_data_portal/embedded_wind_solar_forecast/<year>/<month>/<day>/raw_<fetched_at>_<sha256 of body, first 8 hex>.csv` (`bronze/writer.py:57`)
**Format**: Raw CSV, as-received. Immutable. `<stem>.meta.json` sidecar carries fetch provenance including the vendor `resource_filename` whose 12-digit token is the issue instant (D-15/D-23).
**Granularity**: One file per capture (one forecast issue); partition is the ingest window's end date (D-13)

### Bronze sample

```csv
DATE_GMT,TIME_GMT,SETTLEMENT_DATE,SETTLEMENT_PERIOD,EMBEDDED_WIND_FORECAST,EMBEDDED_WIND_CAPACITY,EMBEDDED_SOLAR_FORECAST,EMBEDDED_SOLAR_CAPACITY
2026-08-20T00:00:00,21:30,2026-08-20T00:00:00,45,857,6417,0,23301
2026-08-20T00:00:00,22:00,2026-08-20T00:00:00,46,847,6417,0,23301
```

(First two rows of the capture of `202608202125_embedded_forecast.csv`. The two date
columns are midnight-stamped datetimes, which the transformer parses with
`%Y-%m-%dT%H:%M:%S`; on this capture, `TIME_GMT` is half an hour after each period's start, UTC.)

(Header is contract-exact — 8 columns. Real captured rows are in
`tests/fixtures/neso_data_portal/embedded_forecast.csv`, taken from
`_probe/sample_embedded-forecast-current.csv`.)

---

## Silver layer

**Path pattern**: `data/silver/neso_data_portal/embedded_wind_solar_forecast/year=<YYYY>/month=<MM>/embedded_wind_solar_forecast_<YYYYMMDD>_run<bronze sidecar written_at, ISO with ":" and "+" as "-">.parquet` (APPEND_ONLY — one file per vintage; `<YYYYMMDD>` is the bronze capture partition, not a settlement date; the run stamp is the sidecar's `written_at` via `_timestamp_from_sidecar` (`silver/base.py:102-107`, `1019`, `1067`), NOT the silver `available_at` column, which equals `published_at`; real file `..._20260820_run2026-08-20T21-43-41.158795-00-00.parquet`; `storage/paths.py:58-61`, `silver/base.py:2633-2636`)
**Transformer class**: `gridflow.silver.neso_data_portal.embedded_wind_solar_forecast.EmbeddedWindSolarForecastTransformer`
**Pydantic schema**: `gridflow.schemas.neso_data_portal.NesoEmbeddedWindSolarForecast`
**Dedup key**: `(settlement_date, settlement_period, issue_time)` — `issue_time`, not `published_at`, is the vintage axis: the vendor stamps the forecast's own issue instant into the filename and it is the finer, more meaningful clock (D-24)
**Point-in-time field**: `issue_time` (vintage axis) / `published_at` (`ckan_last_modified`; `available_at == published_at`, D-22)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `SETTLEMENT_DATE` | GB settlement date |
| `settlement_period` | `int` | No | `SETTLEMENT_PERIOD` | **Bounded 1..periods-in-day** (46/48/50 — D-27, two-sided): the schema validator and the transformer filter share ONE predicate (`is_valid_settlement_period`); out-of-calendar rows are excluded with a WARNING naming period, date and the day's real length, and counted in `last_excluded_row_count` (D-40) |
| `issue_time` | `datetime[UTC]` | No | sidecar `resource_filename` 12-digit token | The forecast issue instant. Required and part of the entity key; a filename with no token → the body is declined with a WARNING, **never** stamped from the fetch clock (D-23/FM-05) |
| `time_gmt_raw` | `str` | No | `TIME_GMT` | Vendor stamp carried **unparsed** — its start-vs-end convention is undocumented, so no code path depends on it (D-26). Corroborated non-bindingly as period-END on the real capture |
| `embedded_wind_forecast` | `float` | No | `EMBEDDED_WIND_FORECAST` | MW; strict cast |
| `embedded_wind_capacity` | `float` | No | `EMBEDDED_WIND_CAPACITY` | MW; strict cast |
| `embedded_solar_forecast` | `float` | No | `EMBEDDED_SOLAR_FORECAST` | MW; strict cast |
| `embedded_solar_capacity` | `float` | No | `EMBEDDED_SOLAR_CAPACITY` | MW; strict cast |
| `published_at` | `datetime[UTC]` | No | sidecar `ckan_last_modified` | Vendor publication instant; required (D-23) |
| `data_provider` | `str` | No | derived | Constant `neso_data_portal` |

**Deliberately absent**: `timestamp_utc` (D-26) — `event_time` derivation
prefers a `timestamp_utc` column over the settlement pair, and only the
pair branch goes through the DST-fold-safe `settlement_period_to_utc`;
emitting an instant here would take `event_time` off the safe path on
exactly the 46/50-period days. `DATE_GMT` is also not emitted (calendar
half of the same undocumented GMT stamp; bronze retains the bytes, so
re-adding it is a re-transform, not a re-ingest).

### Silver sample

```python
[
    {
        "settlement_date": date(2026, 8, 20),
        "settlement_period": 45,
        "issue_time": datetime(2026, 8, 20, 21, 25, tzinfo=timezone.utc),
        "time_gmt_raw": "21:30",
        "embedded_wind_forecast": 857.0,
        "embedded_wind_capacity": 6417.0,
        "embedded_solar_forecast": 0.0,
        "embedded_solar_capacity": 23301.0,
        "published_at": datetime(2026, 8, 20, 21, 25, 3, 319647, tzinfo=timezone.utc),
        "data_provider": "neso_data_portal",
    },
]
```

---

## Gold layer

None implemented. Consumer surface:
`silver_neso_data_portal_embedded_wind_solar_forecast` (all vintages) and
`silver_neso_data_portal_embedded_wind_solar_forecast_latest` (one winning
row per `(settlement_date, settlement_period)`) — `_latest` is the consumer
default (D-30).

---

## Known issues and gotchas

- **Out-of-calendar settlement periods are excluded, not errors** (D-27 /
  FM-16): a row claiming SP49 on a 48-period day (or SP0 on any day) is
  filtered with a WARNING and counted; valid siblings still transform. The
  bound is two-sided because `settlement_period_to_utc` bound-checks
  nothing — SP0 would land in the *previous* settlement day, SP49 in the
  *next*. DST days: 46 periods spring, 50 autumn; SP49/SP50 on the autumn
  day are distinct instants 30 minutes apart.
- **`TIME_GMT` is an unparsed passthrough** — undocumented convention;
  corroborated (non-bindingly) as period-end on the real capture. A future
  corroboration failure means NESO changed convention; the pipeline does
  not depend on it.
- **NESO's catalogue recommends a different resource** (package `notes`,
  snapshot `_generated/snapshots/20260820T214455Z/catalog-snapshot.json`):
  "NESO have moved the data source to its new forecast system. We recommend
  that customers now use the 'Jun - Dec' dataset", i.e. the resource
  "Embedded Solar and Wind Forecast Archive 2026 (Jun - Dec)". gridflow reads
  the resource "Embedded Solar and Wind Forecast" (`connectors/neso_data_portal/endpoints.py:118`),
  last modified 2026-08-20T21:25:03 in that snapshot. Which resource carries
  the live forecast is an open research question; not resolved here.
- **Backfill is not available** (D-35): only the current issue is served;
  history lives in archive resources that are out of this slice's scope.
  `gridflow backfill` refuses; historical `--start/--end` ingest refuses
  (D-34).
- **A token-less `resource_filename` declines the whole body** (FM-05) —
  loudly (`completed_with_warnings`, `bronze_unvouched` counted), never a
  fetch-clock substitute. All-declined dates report `failed` (D-41).
- **D-13 operator guidance** and **FM-15 completeness limit** as for the
  other datasets: transform over the ingest window's end date; vintages
  only as dense as capture cadence.
- **Clock corroboration (D-15)**: `issue_time` and `published_at` agreed to
  3.877 s on the real capture; a live-marked test re-checks |ckan − HTTP
  Last-Modified| < 5 min and specifically NOT ~3600 s (the
  timezone-mistake signature).

---

## Implementation delta

- **`DATE_GMT`**: present in the vendor header, deliberately not emitted to
  silver — D-24's column contract omits it (undocumented GMT stamp,
  calendar half). Bronze retains it. Not a drift; recorded so nobody
  re-adds it without reading D-26's reasoning.

---

## Modelling notes

TODO. Intended use: net-demand and embedded-generation features (join to
Elexon demand outturn on the settlement pair via `event_time`);
solar-suppression studies; forecast-error features by comparing successive
`issue_time` vintages against eventual outturn proxies. Filter guidance:
consume `_latest` for the current view; use the full base view keyed by
`issue_time` for revision studies.

---

## Links

- [Official API docs](https://api.neso.energy/api/3/action/package_show?id=embedded-wind-and-solar-forecasts)
- [Connector source](../../../../../Python/gridflow/src/gridflow/connectors/neso_data_portal/client.py)
- [Silver transformer](../../../../../Python/gridflow/src/gridflow/silver/neso_data_portal/embedded_wind_solar_forecast.py)
- [Pydantic schema](../../../../../Python/gridflow/src/gridflow/schemas/neso_data_portal.py)
- Gold view/builder: none
- [Domain: settlement period](../../../20-domain/concepts/settlement-period.md)
