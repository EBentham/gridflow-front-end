---
source: elexon
dataset_key: atl
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Actual total load
  summary: >-
    Great Britain's actual total load for each half-hour settlement period: one MW figure per
    period, Elexon data item B0610.
  facts:
    vendor: Elexon BMRS, dataset ATL (B0610)
    cadence: One vendor document per settlement period, each published on its own
    grain: One row per settlement period
  landscape: power
  what_it_is: >-
    ATL is the B0610 actual total load for the GB bidding zone: one MW value per settlement
    period, sent as `quantity` with its own document id. It is not INDO national demand: in the
    notebook it runs a median 7,916 MW above INDO from 12:00 to 18:00 UTC. In the week
    charted many half-hours have no row, mostly before midday.
  how_used:
    - A GB total-load actual in the B0610 form, beside INDO and ITSDO.
    - Measuring the gap between total load and INDO national demand by hour.
    - A load feature for a GB power price model, once missing half-hours are handled.
  chart:
    type: line
    silver: elexon/atl
    time: timestamp_utc
    value: total_load_mw
    filter:
      - {column: settlement_date, op: ge, value: "2026-09-14"}
      - {column: settlement_date, op: le, value: "2026-09-20"}
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: Actual total load (ATL), 14 to 20 September 2026
    caption: >-
      Silver `elexon/atl`, MW, one value per half-hour of settlement dates 14 to 20 September
      2026, as sent. Many half-hours have no row: the line breaks at each one, and a reading with
      no neighbour shows as a dot.
    alt: >-
      Line chart of GB actual total load from elexon/atl, in MW, for settlement dates 14 to 20
      September 2026, in short pieces and lone dots: the line breaks at every half-hour with no
      row, most of them before midday UTC. Daily highs are 30,836 to 34,330 MW, near midday or at
      17:00 UTC; lows, 03:30 to 05:00 UTC, are 19,958 to 22,392 MW. At 06:30 UTC on the 18th the
      line drops from 25,600 to 2,670 MW and stops there.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: total_load_mw, label: Total load, codes: ATL, paint: petrol, note: "One half-hour, 06:30 UTC on the 18th, reads 2,670 MW as sent."}
  raw_feed:
    note: >-
      From the Elexon Insights API in 24-hour publish windows. Both windows run a day past 20
      September: its period 48 was published after midnight UTC, as the frame below shows.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/ATL?publishDateTimeFrom=2026-09-20T00:00:00Z&publishDateTimeTo=2026-09-21T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon atl --start 2026-09-14 --end 2026-09-22, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon atl --start 2026-09-14 --end 2026-09-21, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-20"}
        - {column: settlement_period, op: ge, value: 39}
      order_by: [settlement_period]
    key: [settlement_date, settlement_period]
    caption: "Settlement date 2026-09-20, periods 39 to 48 without 40 and 42; 48 published after midnight UTC."
    fields:
      settlement_date: "GB settlement date, the vendor's `settlementDate` label"
      settlement_period: Half-hour of the settlement date, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: "Start of the half-hour, computed from the settlement date and period"
      total_load_mw: "Actual total load for the half-hour in MW, the vendor's `quantity`"
      document_id: "Vendor document id, from `documentId`, as sent"
      document_revision: "Revision of that document, from `documentRevisionNumber`"
      published_at: "Vendor publish time, from `publishTime`, UTC"
  notebook:
    lead: >-
      Returns pandas DataFrames from `silver_elexon_atl` and `silver_elexon_indo`, each filtered on
      `settlement_date` with both ends included; lineage columns dropped. The cells set ATL beside
      INDO national demand for the same half-hours.
    cells:
      - |
        atl = data.elexon.query("atl", "2026-09-14", "2026-09-20")
        indo = data.elexon.query("indo", "2026-09-14", "2026-09-20")
      - |
        key = ["settlement_date", "settlement_period", "timestamp_utc"]
        both = indo[key + ["initial_demand_outturn_mw"]].merge(
            atl[key + ["total_load_mw"]], on=key, how="left")
        both.columns = key + ["indo_mw", "atl_mw"]
        both["atl_minus_indo_mw"] = both.atl_mw - both.indo_mw
        both["timestamp_utc"] = both.timestamp_utc.dt.tz_convert("UTC")
        both = both.sort_values("timestamp_utc", ignore_index=True)
        both.head()
      - |
        both.plot(x="timestamp_utc", y=["atl_mw", "indo_mw"], ylabel="MW",
                  color=["#155A6E", "#C77E3C"], figsize=(8, 3.5))
      - |
        from_hour_utc = (both.timestamp_utc.dt.hour // 6 * 6).rename("from_hour_utc")
        both.groupby(from_hour_utc).atl_minus_indo_mw.agg(["min", "median", "max"]).reset_index()
    needs: ATL published 14 to 21 September 2026, and INDO 13 to 20
    plot_alt: >-
      Line plot of atl_mw (petrol) and indo_mw (clay), settlement dates 14 to 20 September 2026.
      INDO is continuous; ATL breaks where half-hours have no row. ATL sits above INDO most of
      each day, furthest apart around midday, peaking near 34,000 MW; INDO's evening peaks reach
      about 30,800 MW. One ATL half-hour on the 18th drops to about 2,700 MW.
  related:
    - {dataset: elexon/indo, note: "National demand for the same half-hours; the notebook compares them"}
    - {dataset: elexon/agpt, note: "Generation per production type, from the same B-series group"}
    - {dataset: elexon/ndf, note: "Day-ahead forecast of national demand, not of total load"}
    - {dataset: elexon/fuelhh, note: "Generation by fuel type for the same settlement periods"}
---

# Elexon - Actual Total Load Per Bidding Zone (`ATL / B0610`)

## Overview

Actual Total Load Per Bidding Zone (ATL, ENTSO-E B0610) — the realised total load for the GB bidding zone per settlement period. ATL is what the EU transparency platform consumes for GB load.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/ATL` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Soon after each settlement period closes (B-series). |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | Yes | As per Elexon Swagger spec for atl. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | Yes | As per Elexon Swagger spec for atl. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/ATL?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-atl.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/atl/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/ATL?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "ATL",
      "documentId": "NGET-EMFIP-ATL-06475722",
      "documentRevisionNumber": 1,
      "publishTime": "2026-05-06T02:55:04Z",
      "startTime": "2026-05-06T01:00:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 5,
      "quantity": 25774.0
    },
    {
      "dataset": "ATL",
      "documentId": "NGET-EMFIP-ATL-06475721",
      "documentRevisionNumber": 1,
      "publishTime": "2026-05-06T02:25:04Z",
      "startTime": "2026-05-06T00:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 4,
      "quantity": 26368.0
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/atl/year=YYYY/month=MM/atl_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.atl.ATLTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonATL` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, settlement_period)`
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `total_load_mw` | `float` | No | `quantity` | MW. |
| `business_type` | `str` | Yes | `businessType` | Written only if the response carries `businessType` (`silver/elexon/atl.py:70`, `:137`); the ATL bronze sample above has none, so silver has no such column. |
| `document_id` | `str` | Yes | `documentId` | ENTSO-E document MRID. |
| `document_revision` | `int` | Yes | `documentRevisionNumber` | Document revision number. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Publication time / document vintage; bitemporal point-in-time field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | Silver transform time, stamped by the transformer (`silver/elexon/atl.py:117-121`). |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 5,
        "timestamp_utc": "2026-05-06T01:00:00+00:00",
        "total_load_mw": 25774.0,
        "document_id": "NGET-EMFIP-ATL-06475722",
        "document_revision": 1,
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

- **Total load** is one number per period (no PSR split).

---

## Implementation delta

- **Same B-series** group as AGPT (B1620); ATL is B0610 (`connectors/elexon/endpoints.py:162-176`).
- **Pydantic schema** `ElexonATL` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/atl.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
