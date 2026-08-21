---
source: neso_data_portal
dataset_key: embedded_wind_solar_forecast
vendor: "NESO Open Data Portal"
last_verified: 2026-08-19
layer_coverage: "bronze, silver"
---

# NESO Data Portal — Embedded Solar and Wind Forecast

## Overview

NESO's half-hourly forecast of **embedded** (distribution-connected) wind
and solar generation and capacity for GB, per settlement period. Embedded
generation is invisible to Elexon's transmission-metered datasets — it
appears there only as suppressed demand — so this dataset fills the gap the
Elexon stack structurally cannot: models of net demand, effective margin, or
solar-driven demand suppression need it. Each vendor file is one forecast
issue (the issue instant is stamped in the vendor's own filename);
successive issues are successive vintages of the same settlement periods.
Only the **current** resource of the 11-resource package is ingested
(chosen slice); archive chunks are catalogued but not implemented.

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
| Publication lag  | Forecast — issued ahead of real time. Issue cadence TODO (not stated); `issue_time` from the filename token is the authoritative issue instant, corroborated within 120 s of `ckan_last_modified` on the real capture |
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

**Path pattern**: `data/bronze/neso_data_portal/embedded_wind_solar_forecast/<year>/<month>/<day>/raw_<fetched_at>_<uuid>.csv`
**Format**: Raw CSV, as-received. Immutable. `<stem>.meta.json` sidecar carries fetch provenance including the vendor `resource_filename` whose 12-digit token is the issue instant (D-15/D-23).
**Granularity**: One file per capture (one forecast issue); partition is the ingest window's end date (D-13)

### Bronze sample

```csv
DATE_GMT,TIME_GMT,SETTLEMENT_DATE,SETTLEMENT_PERIOD,EMBEDDED_WIND_FORECAST,EMBEDDED_WIND_CAPACITY,EMBEDDED_SOLAR_FORECAST,EMBEDDED_SOLAR_CAPACITY
20260816,00:30,20260816,1,1250,6800,0,15900
20260816,01:00,20260816,2,1310,6800,0,15900
```

(Header is contract-exact — 8 columns. Real captured rows are in
`tests/fixtures/neso_data_portal/embedded_forecast.csv`, taken from
`_probe/sample_embedded-forecast-current.csv`.)

---

## Silver layer

**Path pattern**: `data/silver/neso_data_portal/embedded_wind_solar_forecast/<year>/<month>/<day>/data_<run_suffix>.parquet` (APPEND_ONLY — one file per vintage)
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
        "settlement_date": date(2026, 8, 16),
        "settlement_period": 1,
        "issue_time": datetime(2026, 8, 16, 18, 25, tzinfo=timezone.utc),
        "time_gmt_raw": "00:30",
        "embedded_wind_forecast": 1250.0,
        "embedded_wind_capacity": 6800.0,
        "embedded_solar_forecast": 0.0,
        "embedded_solar_capacity": 15900.0,
        "published_at": datetime(2026, 8, 16, 18, 20, 11, tzinfo=timezone.utc),
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
