---
source: neso_data_portal
dataset_key: daily_wind_availability
vendor: "NESO Open Data Portal"
last_verified: 2026-08-19
layer_coverage: "bronze, silver"
page:
  title: Daily wind availability by BM unit
  summary: >-
    NESO's forecast of each wind BM unit's technical availability, in MW, one figure per unit and
    day, 2 to 14 days ahead.
  facts:
    vendor: NESO Data Portal, package `daily-wind-availability`, file `windavailability.csv`
    cadence: Daily resolution; NESO's catalogue lists update frequency as hourly; the chart shows one file
    grain: One row per BM unit, availability day and NESO file version (`published_at`)
  landscape: power
  what_it_is: >-
    NESO's forecast of each wind BM unit's technical availability in MW, one figure per day, 2 to
    14 days ahead. NESO calls it availability, not what the wind lets a farm produce. Each capture
    is the whole file; gridflow keeps every capture. The project matched `BMU_ID` to Elexon's
    `national_grid_bm_unit`, not to `bm_unit_id`.
  how_used:
    - Available wind capacity per day as a supply input to margin and scarcity models.
    - Spotting units whose availability steps down or up within the next two weeks.
    - Comparing with Elexon's per-unit availability in `uou2t14d`, joined on the National Grid ID.
  chart:
    type: line
    silver: neso_data_portal/daily_wind_availability
    time: availability_date
    value: availability_mw
    filter:
      - {column: availability_mw, op: ge, value: 0}
    dedup: {"on": [bmu_id, availability_date], order_by: published_at}
    aggregation: sum
    window: {start: "2026-08-22", end: "2026-09-03"}
    unit: MW
  chart_view:
    title: Total wind availability, published 20 August 2026
    caption: >-
      Silver `neso_data_portal/daily_wind_availability`, MW: NESO's file published 20 August 2026,
      summed over BM units per availability day, 22 August to 3 September. `ASHWW-1`, sent as -1
      MW, is left out. The MW axis does not start at zero.
    alt: >-
      Line chart of total wind availability from neso_data_portal/daily_wind_availability, in MW,
      for each availability day from 22 August to 3 September 2026, all from NESO's file published
      20 August. Values stay between 25,381 and 26,474 on an axis that does not start at zero: 25,744 on the
      22nd, 25,968 on the 23rd, then 25,381 from 28 to 30 August. It steps up to 26,215 on 31 August
      and holds at 26,474 from 1 to 3 September.
    x_label: availability day (GB)
    key:
      - {series: availability_mw, label: Available wind, codes: MW, paint: horizon, note: "Sum of `availability_mw` over the file's BM units, one value per day."}
  raw_feed:
    note: >-
      Two calls: `package_show` names the file, then gridflow downloads it through the resource's
      redirect. The window only names the bronze partition (its end date); NESO serves only the
      current file.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=daily-wind-availability"
      - "GET https://api.neso.energy/dataset/3758a0ed-6c96-4e36-88d0-107f5020ddf3/resource/7aa508eb-36f5-4298-820f-2fa6745ae2e7/download/windavailability.csv"
    commands:
      - {run: gridflow ingest neso_data_portal daily_wind_availability --last 24h, comment: "bronze; the current file only"}
      - {run: gridflow transform neso_data_portal daily_wind_availability --start 2026-08-20 --end 2026-08-20, comment: "the UTC day the ingest ran"}
  record:
    select:
      filter:
        - {column: availability_date, op: eq, value: "2026-08-31"}
        - {column: bmu_id, op: in, value: [ABRBO-1, ASHWW-1, DBAWO-1, FALGW-1, HOWBO-1, MOWWO-1, NNGAO-1, WHILW-2]}
      order_by: [bmu_id]
      columns: [bmu_id, availability_date, availability_mw, published_at, timestamp_utc]
    key: [bmu_id, availability_date, published_at]
    caption: "Availability day 31 August 2026, eight units picked by ID; `ASHWW-1` arrives as -1 MW."
    fields:
      bmu_id: "NESO `BMU_ID`, verbatim: National Grid's unit ID, the form in `national_grid_bm_unit`"
      availability_date: "NESO `Date`: the GB day the availability applies to"
      availability_mw: "NESO `MW`: technical availability in MW; NESO does not define -1"
      published_at: "NESO's last-modified time for the file (CKAN `last_modified`), read as UTC"
      timestamp_utc: "Start of the GB availability day in UTC: 23:00 the day before in summer"
  notebook:
    lead: >-
      `query()` reads the DuckDB relation `silver_neso_data_portal_daily_wind_availability_latest`,
      the most recently published row per unit and day, filtered on `availability_date` with both
      ends included. Lineage columns are dropped.
    cells:
      - |
        df = data.neso_data_portal.query("daily_wind_availability", "2026-08-22", "2026-09-03")
        df["published_at"] = df["published_at"].dt.tz_convert("UTC")
      - df.sort_values(["availability_date", "bmu_id"])[["bmu_id", "availability_date", "availability_mw", "published_at"]].head()
      - |
        total = df[df.availability_mw >= 0].groupby("availability_date")["availability_mw"].sum()
        ax = total.plot(ylabel="MW", figsize=(8, 3.5), marker="o", ylim=(0, 30000))
    needs: a NESO file covering 22 August to 3 September 2026
    plot_alt: >-
      Line plot with markers of the daily sum of availability_mw against availability_date, 22
      August to 3 September 2026, y axis 0 to 30,000 MW. The line sits between 25,381 and 25,968 MW
      to 30 August, then 26,215 on the 31st and 26,474 from 1 September.
  related:
    - {dataset: elexon/uou2t14d, note: "Elexon's per-unit availability 2 to 14 days ahead; join on `national_grid_bm_unit`"}
    - {dataset: elexon/bmunits_reference, note: "Unit names and fuel type, joined on `national_grid_bm_unit`"}
    - {dataset: elexon/windfor, note: "Elexon's GB wind generation forecast: output, where this is availability"}
    - {dataset: elexon/fuelhh, note: "Wind outturn by half-hour, to set against forecast availability"}
---

# NESO Data Portal — Daily Wind Availability

## Overview

Per-BMU wind availability forecasts, 2–14 days ahead: the MW each
wind BM unit expects to have available on a given day.
NESO republishes the whole file, so successive captures are successive
forecast vintages of the same days — you can ask what NESO expected for day
D as of capture time T. A supply-side input for margin and scarcity models;
`BMU_ID` is stored verbatim. It is National Grid's unit ID (`ABRBO-1`, no `T_`
prefix): it matches Elexon's `national_grid_bm_unit`, never `bm_unit_id`
(checked 2026-10-06 against the 20 Aug 2026 capture: 231 of 276 IDs found in
`elexon/bmunits_reference`, 0 on `bm_unit_id`).

NESO's own description (CKAN `package_show`, captured in gridflow
`.planning/phases/neso-data-portal/_probe/package_search_p0.json`): the
package notes give "wind generator availability in megawatts (MW) at a daily
resolution for 2-14 days ahead"; the resource description says it is the
technical availability of the wind farms, not what they can produce from the
wind speed. The package `extras` give `Update Frequency: Hourly` (CKAN
`extras`; also in the 20 Aug 2026 catalogue snapshot under `_generated/`).

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
| Publication lag  | TODO — lag not stated by NESO; the catalogue `extras` list `Update Frequency: Hourly`; `ckan_last_modified` is the vendor's own publication instant |
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
ABRBO-1,2026-08-22,99
ABRBO-1,2026-08-23,99
ABRBO-1,2026-08-24,99
```

(First rows of the 20 Aug 2026 capture, `raw_20260820T214333Z_e91f317b.csv`.
Rows are sorted by unit then date; `MW` is a whole number in that capture, and
the file ends with a line holding only a carriage return.)

(Header is contract-exact: `BMU_ID, Date, MW`. A drifted header raises
`CsvHeaderDriftError` at fetch time (D-36) and again at transform (D-19).
Fixture provenance: the unit fixture is hand-authored from the
research-asserted header — Stage A captured no CSV sample for this resource —
and a live-marked test pins the real header against the portal.)

---

## Silver layer

**Path pattern**: `data/silver/neso_data_portal/daily_wind_availability/year=<YYYY>/month=<MM>/daily_wind_availability_<YYYYMMDD>_run<stamp>.parquet` (APPEND_ONLY — one file per vintage; `silver/base.py:2633-2635`)
**Transformer class**: `gridflow.silver.neso_data_portal.daily_wind_availability.DailyWindAvailabilityTransformer`
**Pydantic schema**: `gridflow.schemas.neso_data_portal.NesoDailyWindAvailability`
**Dedup key**: `(bmu_id, availability_date, published_at)` — `published_at` is in the key unconditionally; the dataset is APPEND_ONLY precisely so successive vendor publications coexist (D-21/D-24)
**Point-in-time field**: `published_at` (vendor's `ckan_last_modified`, via the D-23 provenance reader; `available_at == published_at`, D-22)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `bmu_id` | `str` | No | `BMU_ID` | Verbatim — no case folding, stripping, or prefix normalisation (repo-wide BM-unit rule); joins to Elexon's `national_grid_bm_unit`, not `bm_unit_id` |
| `availability_date` | `date` | No | `Date` | The GB availability day; strict cast, non-ISO raises |
| `availability_mw` | `float` | No | `MW` | Forecast technical availability, MW; strict cast, non-numeric raises. `-1` occurs (see Known issues) |
| `timestamp_utc` | `datetime[UTC]` | No | derived | D-25: `settlement_period_to_utc(availability_date, 1)` — SP1 of the GB day. BST date → 23:00Z previous day; GMT date → 00:00Z same day. Derived instant; `availability_date` is the user-facing field |
| `published_at` | `datetime[UTC]` | No | sidecar `ckan_last_modified` | Vendor publication instant. Required, never nullable: a body without it is declined (D-23/FM-05), never stamped from the fetch clock |
| `data_provider` | `str` | No | derived | Constant `neso_data_portal` |

### Silver sample

```python
[
    {
        "bmu_id": "ABRBO-1",
        "availability_date": date(2026, 8, 22),
        "availability_mw": 99.0,
        "timestamp_utc": datetime(2026, 8, 21, 23, 0, tzinfo=timezone.utc),
        "published_at": datetime(2026, 8, 20, 21, 20, 7, 510686, tzinfo=timezone.utc),
        "data_provider": "neso_data_portal",
    },
    {
        "bmu_id": "ACHRW-1",
        "availability_date": date(2026, 8, 22),
        "availability_mw": 43.0,
        "timestamp_utc": datetime(2026, 8, 21, 23, 0, tzinfo=timezone.utc),
        "published_at": datetime(2026, 8, 20, 21, 20, 7, 510686, tzinfo=timezone.utc),
        "data_provider": "neso_data_portal",
    },
]
```

(Real rows from the 20 Aug 2026 capture. Silver also carries the lineage
columns `event_time` (= `timestamp_utc`), `available_at` (= `published_at`),
`source_run_id` and `dataset_version`; there is no `ingested_at` column.)

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
- **`-1` MW is sent and undocumented.** In the 20 Aug 2026 capture `ASHWW-1`
  carries `-1` on every day; NESO does not say what `-1` means. Exclude it (or
  treat it as unknown) before summing availability.
- **An all-null row reaches silver (defect, 2026-10-06).** The CSV ends with a
  line holding only `\r`; `pl.read_csv` (`silver/csv_bronze.py:123-128`) reads
  it as a row of nulls, the strict casts keep the nulls, and schema validation
  is fail-soft (`silver/base.py:2021`), so silver holds one row with null
  `bmu_id`, `availability_date`, `availability_mw` and `timestamp_utc`. A query
  filtered on `availability_date` never returns it.
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
