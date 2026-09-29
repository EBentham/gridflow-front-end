---
source: elexon
dataset_key: indgen
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Indicated generation, demand, imbalance and margin
  summary: >-
    Half-hourly forecasts for the current and next day: indicated generation (`INDGEN`), demand
    (`INDDEM`), imbalance (`IMBALNGC`) and margin (`MELNGC`), nationally and by zone.
  facts:
    vendor: Elexon BMRS, datasets INDGEN, INDDEM, IMBALNGC and MELNGC
    cadence: About every 30 minutes
    grain: One row per half-hour, zone, publish day; IMBALNGC, MELNGC keep one unlabelled zone row
  landscape: power
  what_it_is: >-
    Forecasts per half-hour, national (`N`) and by zone, `B1` to `B17`. Per Elexon, `INDGEN` sums
    positive Physical Notifications and `INDDEM` negative ones; `IMBALNGC` is `INDGEN` minus the
    transmission demand forecast; `MELNGC` is summed Maximum Export Limits minus the national
    demand forecast. Silver keeps one unlabelled `IMBALNGC` and `MELNGC` zone row per half-hour,
    the API's last (`N` in this window).
  how_used:
    - "Day-ahead features for imbalance price and NIV models: indicated imbalance and margin."
    - "Tightness screening: a low indicated margin marks half-hours with little spare capacity."
    - "Self-dispatch tracking: how indicated generation moves between day-ahead and same-day publishes."
  chart:
    type: line
    silver: elexon/indgen
    time: timestamp_utc
    value: indicated_generation_mw
    filter:
      - {column: boundary, op: eq, value: "N"}
      - {column: settlement_date, op: eq, value: "2026-09-17"}
      - {column: published_at, op: in, value: ["2026-09-16T10:48:00Z", "2026-09-17T00:17:00Z"]}
    group: published_at
    group_map:
      "2026-09-16 10:48:00.000000+00:00": day_ahead
      "2026-09-17 00:17:00.000000+00:00": same_day
    series_order: [day_ahead, same_day]
    aggregation: last
    window: {start: "2026-09-16", end: "2026-09-17"}
    unit: MW
  chart_view:
    title: National indicated generation, 17 September 2026, two publishes
    caption: >-
      Silver `elexon/indgen` only, boundary `N`, MW, settlement date 17 September 2026 as the 10:48
      UTC publish on 16 September and the 00:17 UTC publish on 17 September forecast it. Demand,
      imbalance and margin are in the notebook below.
    alt: >-
      Line chart of GB national indicated generation (INDGEN, boundary N) from elexon/indgen, in
      MW, for settlement date 17 September 2026 as two publishes forecast it: 10:48 UTC on 16
      September, from 04:00 UTC, and 00:17 UTC on 17 September, from 00:30 UTC at 25,277 MW. The
      lines stay within 1,122 MW until 06:30 UTC; from 07:00 the 00:17 publish runs higher, by up
      to 5,992 MW at 11:30, while the 10:48 line falls to 22,495 MW at 13:00. Both peak at 18:30
      UTC, at 33,220 (00:17) and 31,228 MW (10:48).
    x_label: UTC; the settlement day begins 23:00, 16 September
    key:
      - {series: day_ahead, label: "10:48 UTC, 16 Sep", codes: INDGEN, note: "Starts at 04:00 UTC: for earlier half-hours silver keeps another 16 September publish.", paint: petrol}
      - {series: same_day, label: "00:17 UTC, 17 Sep", codes: INDGEN, note: "Starts at 00:30 UTC: this publish holds no earlier half-hours.", paint: clay}
  raw_feed:
    note: >-
      From the Elexon Insights API in 24-hour publish windows; swap `INDGEN` for `INDDEM`,
      `IMBALNGC` or `MELNGC`. gridflow sends no `boundary`, so the national row and every zone
      arrive.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/INDGEN?publishDateTimeFrom=2026-09-16T00:00:00Z&publishDateTimeTo=2026-09-17T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon indgen --start 2026-09-16 --end 2026-09-18, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon indgen --start 2026-09-16 --end 2026-09-17, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-17"}
        - {column: settlement_period, op: eq, value: 36}
        - {column: boundary, op: in, value: ["N", "B1", "B6", "B9"]}
      order_by: [boundary, published_at]
      columns: [boundary, published_at, indicated_generation_mw]
    key: [settlement_date, settlement_period, boundary, published_at]
    caption: "Period 36 of 17 September (16:30 UTC): national and three zones, from both kept publishes."
    fields:
      settlement_date: "GB settlement date, the vendor's `settlementDate` label"
      settlement_period: Half-hour of the settlement date, 1 to 48; 46 or 50 on clock-change days
      boundary: "`N` for national; `B1` to `B17` for the system zones Elexon publishes"
      published_at: "Vendor `publishTime`; each publish day's file keeps one publish per half-hour and zone"
      indicated_generation_mw: "Sum of positive Physical Notifications for the half-hour in MW, the vendor's `generation`"
      timestamp_utc: Start of the half-hour, computed from the settlement date and period
  notebook:
    lead: >-
      Returns pandas DataFrames from `silver_elexon_indgen`, its three siblings and `silver_elexon_tsdf`,
      filtered on `settlement_date`, both ends included; lineage columns dropped. The cells keep the
      00:17 UTC publish, with `boundary` filtered to `N` where present.
    cells:
      - |
        import pandas as pd
        cols = {
            "indgen": "indicated_generation_mw",
            "inddem": "indicated_demand_mw",
            "imbalngc": "indicated_imbalance",
            "melngc": "indicated_margin",
            "tsdf": "forecast_demand_mw",
        }
        pub = pd.Timestamp("2026-09-17 00:17", tz="UTC")
        parts = []
        for name, col in cols.items():
            df = data.elexon.query(name, "2026-09-17", "2026-09-17")
            df = df[df.published_at.dt.tz_convert("UTC") == pub]
            if "boundary" in df:
                df = df[df.boundary == "N"]
            ts = df.timestamp_utc.dt.tz_convert("UTC")
            parts.append(df.set_index(ts)[col].rename(name))
        nat = pd.concat(parts, axis=1).sort_index()
      - |
        nat.reset_index().head()
      - |
        check = nat.indgen - nat.imbalngc - nat.tsdf
        check.agg(["min", "max"])
      - |
        nat[["indgen", "tsdf", "melngc", "imbalngc"]].plot(
            ylabel="MW", figsize=(8, 3.5),
            color=["#155A6E", "#C77E3C", "#66793B", "#3E8C97"])
    needs: INDGEN, INDDEM, IMBALNGC, MELNGC and TSDF, published 16 and 17 September 2026
    plot_alt: >-
      Line plot in MW of the 00:17 UTC publish's national rows for 17 September 2026, 00:30 to
      22:30 UTC: indgen (petrol), tsdf (clay), melngc (olive) and imbalngc (horizon). TSDF peaks
      at 33,351 MW at 18:00 and margin falls to its low, 24,475 MW, at 18:30. Imbalance dips to
      -1,026 MW at 07:30 and rises to 6,430 MW at 22:30.
  related:
    - {dataset: elexon/pn, note: "Unit Physical Notifications; INDGEN and INDDEM sum them by sign"}
    - {dataset: elexon/tsdf, note: "Transmission demand forecast that IMBALNGC subtracts from INDGEN"}
    - {dataset: elexon/ndf, note: "National demand forecast that MELNGC subtracts from summed MELs"}
    - {dataset: elexon/lolpdrm, note: "De-rated margin and loss-of-load probability: a different margin measure"}
  family:
    slug: indicated-day-ahead
    members:
      - dataset: indgen
        differs: "Sum of positive Physical Notifications, MW; national `N` plus zones `B1` to `B17`"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/INDGEN?publishDateTimeFrom=2026-09-16T00:00:00Z&publishDateTimeTo=2026-09-17T00:00:00Z&page=1"
      - dataset: inddem
        differs: "Sum of negative Physical Notifications (importing units), so negative; `N` plus zones"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/INDDEM?publishDateTimeFrom=2026-09-16T00:00:00Z&publishDateTimeTo=2026-09-17T00:00:00Z&page=1"
      - dataset: imbalngc
        differs: "`INDGEN` minus transmission demand forecast, MW; silver keeps the zone row listed last, unlabelled"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/IMBALNGC?publishDateTimeFrom=2026-09-16T00:00:00Z&publishDateTimeTo=2026-09-17T00:00:00Z&page=1"
      - dataset: melngc
        differs: "Summed MELs minus national demand forecast; silver keeps the zone row listed last, unlabelled"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/MELNGC?publishDateTimeFrom=2026-09-16T00:00:00Z&publishDateTimeTo=2026-09-17T00:00:00Z&page=1"
---

# Elexon - Day and Day-Ahead Indicated Generation (`INDGEN`)

## Overview

Indicated Generation — the GB generation component of the NESO indicated-imbalance forecast. Companion to INDDEM and IMBALNGC.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/INDGEN` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Day-ahead and intra-day. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `boundary` | string | No | As per Elexon Swagger spec for indgen. | `N` |
| `publishDateTimeFrom` | string | No | As per Elexon Swagger spec for indgen. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | As per Elexon Swagger spec for indgen. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/INDGEN?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-indgen.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/indgen/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/INDGEN?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "INDGEN",
      "generation": 272,
      "publishTime": "2026-05-06T02:47:00Z",
      "startTime": "2026-05-06T03:00:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 9,
      "boundary": "B1"
    },
    {
      "dataset": "INDGEN",
      "generation": 261,
      "publishTime": "2026-05-06T02:47:00Z",
      "startTime": "2026-05-06T03:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 10,
      "boundary": "B1"
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/indgen/year=YYYY/month=MM/indgen_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.indgen.INDGENTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonIndGen` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, settlement_period, boundary)`, `unique(keep="last")` with no prior sort, over one UTC publish day's bronze (`silver/elexon/indgen.py:114-117`)
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `indicated_generation_mw` | `float` | No | `generation` | MW. |
| `boundary` | `str` | Yes | `boundary` | `N` (national) or a system zone, `B1` to `B17` (bronze rows, 2026-09-29). |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Publication time / document vintage; bitemporal point-in-time field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`indgen.py:119-124`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 9,
        "timestamp_utc": "2026-05-06T03:00:00+00:00",
        "indicated_generation_mw": 272,
        "boundary": "B1",
        "data_provider": "elexon",
        "ingested_at": "2026-05-08T12:00:00Z"
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Forecast revision behaviour** — multiple publishes per period. The API republishes about every 30 minutes and each silver file holds one UTC publish day; within it the dedup keeps one row per key, the last the API returned, with no sort (`indgen.py:114-117`). The API lists the newest publish first (project check on bronze, 2026-09-29), so the survivor is the day's earliest publish covering that half-hour: 00:17 UTC, or about 10:48 UTC for the half-hours that publish adds. A half-hour recurs in up to three publish days' files, so filter on `published_at` before joining or summing.
- **Definition** ([Elexon BSC glossary](https://elexon.co.uk/glossary/indicated-generation)): the half-hour average MW expected generation, the sum of the Physical Notifications that are positive (exporting BM units), for each System Zone and nationally.

---

## Implementation delta

- **Pydantic schema** `ElexonIndGen` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/indgen.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
