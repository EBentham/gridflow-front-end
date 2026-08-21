---
source: neso_data_portal
dataset_key: daily_wind_availability
vendor: "NESO Open Data Portal"
last_verified: 2026-08-19
layer_coverage: "bronze, silver"
---

# NESO Data Portal — Daily Wind Availability

## Overview

Per-BMU daily wind availability forecast, 2–14 days ahead: for each
transmission-connected wind BM unit, the MW expected to be available on each
future GB availability day. NESO republishes the whole file, so successive
captures are successive forecast vintages of the same days — the dataset
answers "what did NESO believe about wind availability for day D, as of
capture time T?". In models it is a supply-side input for margin/scarcity
forecasting, and its `BMU_ID` column cross-references Elexon BM units
directly (stored verbatim for exactly that join). Chosen as the first
Data-Portal dataset because it is the cleanest possible shape: daily grain,
no intra-day timezone ambiguity, three columns.

→ [Settlement period](../../../20-domain/concepts/settlement-period.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://api.neso.energy/api/3/action/` |
| Path             | `package_show?id=daily-wind-availability` → resource URL from `resources[]`, then file download (302 → presigned CDN URL) |
| Method           | GET |
| Auth             | None — keyless public API (verified 2026-08-16, 24 live calls, no key anywhere in NESO's guidance) |
| Rate limit       | Vendor guidance: max 1 request/second (CKAN actions); enforced by IP block, not HTTP 429. Connector throttles every send, redirect hops and retries included |
| Pagination       | None for `package_show`; the download is a single file |
| Historical depth | Rolling forward-looking window (2–14 days ahead); no historical archive resource. TODO: confirm whether NESO retains superseded files anywhere |
| Publication lag  | TODO — republication cadence not stated by NESO; `ckan_last_modified` is the vendor's own publication instant |
| Response format  | JSON (CKAN metadata envelope) → CSV (the data file) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | string | Yes | CKAN package (dataset) slug | `daily-wind-availability` |

The resource within the package is selected by **exact
`resources[].name == "Daily Wind Availability"`** (D-03) with format `CSV` —
never by UUID and never by a cached download URL; UUIDs are recorded as
provenance only. Resource URLs are re-resolved from `package_show` on every
fetch (D-06).

### Working curl example

```bash
# Keyless — no auth header. Metadata call (the connector then downloads the
# resource URL found in resources[] where name == "Daily Wind Availability"):
curl -X GET \
  "https://api.neso.energy/api/3/action/package_show?id=daily-wind-availability"
```

---

## Bronze layer

**Path pattern**: `data/bronze/neso_data_portal/daily_wind_availability/<year>/<month>/<day>/raw_<fetched_at>_<uuid>.csv`
**Format**: Raw CSV, as-received. Immutable — never modified after write. A `<stem>.meta.json` sidecar carries the fetch provenance (`ckan_last_modified`, resource filename, request params).
**Granularity**: One file per capture (whole-file republication); partition is the ingest window's **end date** (D-13)

### Bronze sample

```csv
BMU_ID,Date,MW
T_ABRBO-1,2026-08-16,42.5
T_ACHRW-1,2026-08-16,118.0
T_ABRBO-1,2026-08-17,39.1
```

(Header is contract-exact: `BMU_ID, Date, MW`. A drifted header raises
`CsvHeaderDriftError` at fetch time (D-36) and again at transform (D-19).
Fixture provenance: the unit fixture is hand-authored from the
research-asserted header — Stage A captured no CSV sample for this resource —
and a live-marked test pins the real header against the portal.)

---

## Silver layer

**Path pattern**: `data/silver/neso_data_portal/daily_wind_availability/<year>/<month>/<day>/data_<run_suffix>.parquet` (APPEND_ONLY — one file per vintage)
**Transformer class**: `gridflow.silver.neso_data_portal.daily_wind_availability.DailyWindAvailabilityTransformer`
**Pydantic schema**: `gridflow.schemas.neso_data_portal.NesoDailyWindAvailability`
**Dedup key**: `(bmu_id, availability_date, published_at)` — `published_at` is in the key unconditionally; the dataset is APPEND_ONLY precisely so successive vendor publications coexist (D-21/D-24)
**Point-in-time field**: `published_at` (vendor's `ckan_last_modified`, via the D-23 provenance reader; `available_at == published_at`, D-22)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `bmu_id` | `str` | No | `BMU_ID` | Verbatim — no case folding, stripping, or prefix normalisation (repo-wide BM-unit rule); joins to Elexon BM units |
| `availability_date` | `date` | No | `Date` | The GB availability day; strict cast, non-ISO raises |
| `availability_mw` | `float` | No | `MW` | Forecast available capacity, MW; strict cast, non-numeric raises |
| `timestamp_utc` | `datetime[UTC]` | No | derived | D-25: `settlement_period_to_utc(availability_date, 1)` — SP1 of the GB day. BST date → 23:00Z previous day; GMT date → 00:00Z same day. Derived instant; `availability_date` is the user-facing field |
| `published_at` | `datetime[UTC]` | No | sidecar `ckan_last_modified` | Vendor publication instant. Required, never nullable: a body without it is declined (D-23/FM-05), never stamped from the fetch clock |
| `data_provider` | `str` | No | derived | Constant `neso_data_portal` |

### Silver sample

```python
[
    {
        "bmu_id": "T_ABRBO-1",
        "availability_date": date(2026, 8, 16),
        "availability_mw": 42.5,
        "timestamp_utc": datetime(2026, 8, 15, 23, 0, tzinfo=timezone.utc),
        "published_at": datetime(2026, 8, 16, 18, 20, 11, tzinfo=timezone.utc),
        "data_provider": "neso_data_portal",
    },
    {
        "bmu_id": "T_ACHRW-1",
        "availability_date": date(2026, 8, 16),
        "availability_mw": 118.0,
        "timestamp_utc": datetime(2026, 8, 15, 23, 0, tzinfo=timezone.utc),
        "published_at": datetime(2026, 8, 16, 18, 20, 11, tzinfo=timezone.utc),
        "data_provider": "neso_data_portal",
    },
]
```

---

## Gold layer

None implemented. The consumer surface is the DuckDB view pair
`silver_neso_data_portal_daily_wind_availability` (all vintages) and
`silver_neso_data_portal_daily_wind_availability_latest` (one winning row per
`(bmu_id, availability_date)`) — **`_latest` is the consumer default (D-30)**;
the base view legitimately contains duplicates across captures (FM-11,
accepted and pinned by test).

---

## Known issues and gotchas

- **Whole-file republication means the base view duplicates by design**
  (FM-11): two captures of identical content produce duplicate rows in the
  base view and exactly one row per key in `_latest`. Consume `_latest`
  unless you are explicitly studying vintages.
- **No backfill** (D-35): `gridflow backfill` refuses this source — the
  portal serves only the current file, so a historical date range cannot be
  re-fetched. `gridflow ingest` with a historical `--start/--end` refuses
  with the D-34 message for the same reason.
- **Operator guidance (D-13)**: prefer `gridflow pipeline`, or transform over
  a window covering the ingest window's **end date** — bronze partitions on
  the window end, so a transform pointed at the wrong date finds nothing.
  Residuals: a capture straddling UTC midnight lands in the end-date
  partition (FM-13 pins this), and a transform for a date with no capture
  reports `failed` rather than silently succeeding.
- **Completeness limit (FM-15)**: the pipeline can only prove what it
  captured — vendor republications between captures are invisible; the
  vintage record is as dense as the ingest cadence, no denser.
- Skipped bodies (missing/unusable sidecar) surface as
  `completed_with_warnings` with the file counted in `bronze_unvouched`; a
  date whose every body is declined reports `failed` (D-41, ADR-030).

---

## Implementation delta

No discrepancies found. (The header contract is deliberately declared twice —
connector `DATASETS` for the fetch-time admission rung (D-36) and the
transformer module for transform time (D-19) — with an E2E test asserting the
two declarations agree; that is a designed redundancy, not a delta.)

---

## Modelling notes

TODO. Intended use (not yet designed in gridflow_models): supply-margin and
scarcity features — join to Elexon BM-unit metadata on `bmu_id`, aggregate
available wind MW per day, compare against outturn (`elexon/fuelhh` wind) for
forecast-error features. Vintage dimension (`published_at`) supports
forecast-revision studies.

---

## Links

- [Official API docs](https://api.neso.energy/api/3/action/package_show?id=daily-wind-availability) — plus NESO's CKAN guidance page (see vendor [README](../README.md))
- [Connector source](../../../../../Python/gridflow/src/gridflow/connectors/neso_data_portal/client.py)
- [Silver transformer](../../../../../Python/gridflow/src/gridflow/silver/neso_data_portal/daily_wind_availability.py)
- [Pydantic schema](../../../../../Python/gridflow/src/gridflow/schemas/neso_data_portal.py)
- Gold view/builder: none
- [Domain: settlement period](../../../20-domain/concepts/settlement-period.md)
