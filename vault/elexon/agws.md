---
source: elexon
dataset_key: agws
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Wind and solar generation
  summary: >-
    Great Britain's wind and solar generation for every half-hour settlement period: solar,
    offshore wind and onshore wind as separate MW figures.
  facts:
    vendor: Elexon BMRS, dataset AGWS (B1630)
    cadence: Every 30 minutes
    grain: One row per settlement period and production type
  landscape: power
  what_it_is: >-
    Elexon's actual or estimated wind and solar generation for each GB settlement period, the
    ENTSO-E B1630 figure: one MW value per production type, sent as a label (`Solar`,
    `Wind Offshore`, `Wind Onshore`). No column says whether a value is actual or estimated. In
    the rows below, each period was published two and a half hours after it began.
  how_used:
    - Solar and wind supply terms for a GB residual-demand or price model.
    - Scoring a wind forecast such as WINDFOR against outturn, offshore and onshore apart.
    - Solar outturn per half-hour, which the FUELHH fuel mix does not carry.
  chart:
    type: stacked-area
    silver: elexon/agws
    time: timestamp_utc
    value: generation_mw
    filter:
      - {column: settlement_date, op: ge, value: "2026-09-19"}
      - {column: settlement_date, op: le, value: "2026-09-25"}
    dedup: {"on": [settlement_date, settlement_period, psr_type], order_by: published_at}
    group: psr_type
    group_map:
      Wind Onshore: onshore
      Wind Offshore: offshore
      Solar: solar
    series_order: [onshore, offshore, solar]
    aggregation: sum
    window: {start: "2026-09-18", end: "2026-09-25"}
    unit: MW
  chart_view:
    title: Wind and solar, 19 to 25 September 2026
    caption: >-
      Silver `elexon/agws`, MW, every half-hour of settlement dates 19 to 25 September 2026, one
      value per production type, stacked: the top edge is the three types summed.
    alt: >-
      Stacked area chart of GB wind and solar generation from elexon/agws, in MW, for every
      half-hour of settlement dates 19 to 25 September 2026. From zero upward: onshore wind (0.5
      to 8.8 GW), offshore wind (0.4 to 11.5 GW) and solar (zero overnight, peaking between 6.2 and
      10.1 GW each day). Wind is strongest on the 19th, up to 19.1 GW combined, and weakest on the
      22nd, down to 1.6 GW. The total runs from 2.0 to 25.1 GW.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: solar, label: Solar, codes: Solar, tag: solar, note: "FUELHH has no solar code."}
      - {series: offshore, label: Offshore wind, codes: Wind Offshore, paint: horizon, tag: offshore wind}
      - {series: onshore, label: Onshore wind, codes: Wind Onshore, paint: hatch-lines, note: "Unpainted: the palette has one colour for wind."}
  raw_feed:
    note: >-
      From the Elexon Insights API in 24-hour publish windows; bronze is filed by publish day.
      Period 46 below was published after midnight UTC, so both commands run a day longer.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/AGWS?publishDateTimeFrom=2026-09-19T00:00:00Z&publishDateTimeTo=2026-09-20T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon agws --start 2026-09-19 --end 2026-09-27, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon agws --start 2026-09-19 --end 2026-09-26, comment: "bronze to silver, by publish day"}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-25"}
        - {column: settlement_period, op: in, value: [1, 14, 27, 46]}
        - {column: psr_type, op: in, value: [Solar, Wind Offshore]}
      order_by: [settlement_period, psr_type]
    key: [settlement_date, settlement_period, psr_type]
    caption: "Settlement date 2026-09-25: Solar and Wind Offshore at periods 1, 14, 27 and 46."
    fields:
      settlement_date: "GB settlement date, the vendor's settlementDate as sent"
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: Start of the half-hour, computed from settlement date and period
      psr_type: "Production type as Elexon sends it: a label, not a code"
      generation_mw: "MW for the period, from the vendor's quantity field"
      business_type: Vendor business type as sent; solar and wind differ here
      document_id: Vendor document id; the two rows of each period here share one
      document_revision: Revision number of that document, as sent
      published_at: "Vendor publish time; period 46's falls after midnight UTC, the next day"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_agws`, filtered on
      `settlement_date` with both ends included. Lineage columns are dropped.
    cells:
      - |
        df = data.elexon.query("agws", "2026-09-19", "2026-09-25")
        df = df.sort_values(["timestamp_utc", "psr_type"])
      - df[["settlement_date", "settlement_period", "psr_type", "generation_mw"]].head()
      - |
        wide = df.pivot_table(index="timestamp_utc", columns="psr_type",
                              values="generation_mw")
        ax = wide[["Wind Offshore", "Wind Onshore", "Solar"]].plot(
            ylabel="MW", color=["#3E8C97", "#1C2B22", "#AFC64E"],
            style=["-", "--", "-"], ylim=(0, 14500), figsize=(8, 3.5))
        ax.legend(ncols=3, loc="upper right");
    needs: 19 to 26 September 2026
    plot_alt: >-
      Line plot of Wind Offshore, Wind Onshore (dashed) and Solar generation_mw against
      timestamp_utc for settlement dates 19 to 25 September 2026. Offshore peaks near 11,500 MW
      early on the 19th and onshore near 8,800 MW that day; on the 22nd both stay below 3,400 MW.
      Solar peaks each day, from about 6,200 to 10,100 MW, and is zero overnight.
  related:
    - {dataset: elexon/agpt, note: "Every production type for the same periods, wind and solar included"}
    - {dataset: elexon/windfor, note: "Elexon's wind forecast, to score against this outturn"}
    - {dataset: elexon/fuelhh, note: "The same half-hours by fuel code: wind as one code, no solar"}
    - {dataset: entsoe/wind_solar_forecast, note: "ENTSO-E's forecast of the same three types, as B16, B18 and B19"}
---

# Elexon - Actual or Estimated Wind and Solar Power Generation (`AGWS / B1630`)

## Overview

Actual or Estimated Wind and Solar Power Generation (AGWS, ENTSO-E B1630) — wind/solar split of generation per settlement period. AGWS uses the same ENTSO-E PSR taxonomy as AGPT but is restricted to renewable categories.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/AGWS` |
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
| `publishDateTimeFrom` | string | Yes | As per Elexon Swagger spec for agws. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | Yes | As per Elexon Swagger spec for agws. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/AGWS?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-agws.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/agws/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/AGWS?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "AGWS",
      "documentId": "NGET-EMFIP-AGWS-20861078",
      "documentRevisionNumber": 1,
      "publishTime": "2026-05-06T02:58:21Z",
      "businessType": "Wind generation",
      "psrType": "Wind Onshore",
      "quantity": 1238.414,
      "startTime": "2026-05-06T00:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 4
    },
    {
      "dataset": "AGWS",
      "documentId": "NGET-EMFIP-AGWS-20861078",
      "documentRevisionNumber": 1,
      "publishTime": "2026-05-06T02:58:21Z",
      "businessType": "Wind generation",
      "psrType": "Wind Offshore",
      "quantity": 4153.834,
      "startTime": "2026-05-06T00:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 4
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/agws/year=YYYY/month=MM/agws_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.agws.AGWSTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonAGWS` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, settlement_period, psr_type)`
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `psr_type` | `str` | No | `psrType` | Elexon's human-readable PSR *label* (e.g. "Wind Onshore", "Wind Offshore"), stored as-is — NOT an ENTSO-E B-code. |
| `generation_mw` | `float` | No | `quantity` | MW. |
| `business_type` | `str` | Yes | `businessType` | ENTSO-E business type. |
| `document_id` | `str` | Yes | `documentId` | ENTSO-E document MRID. |
| `document_revision` | `int` | Yes | `documentRevisionNumber` | Document revision number. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Publication time / document vintage; bitemporal point-in-time field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: `datetime.now(UTC)` stamped by the transformer (`silver/elexon/agws.py:119-123`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 4,
        "timestamp_utc": "2026-05-06T00:30:00+00:00",
        "psr_type": "Wind Onshore",
        "generation_mw": 1238.414,
        "business_type": "Wind generation",
        "document_id": "NGET-EMFIP-AGWS-20861078",
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

- **Same gotchas as AGPT** — limited to wind/solar PSR types.
- **Cross-source representation differs.** Elexon stores human-readable PSR *labels*; ENTSO-E's `wind_solar_forecast` stores the raw B-code. The same concept is represented two ways across sources — downstream joins must not assume a shared code domain.
- **Daily silver files are bucketed by publish/ingestion day, not settlement day** (re-checked 2026-09-28 against silver re-transformed 2026-09-27; the 2026-07-30 reading of "periods 41–48 only" no longer holds). `agws_20260724.parquet` holds periods 1–45 of `settlement_date=2026-07-24` plus periods 46–48 of 2026-07-23, because AGWS is a `PUBLISH_DATETIME`-style endpoint (`connectors/elexon/endpoints.py:168-172`; bronze `data_date` is the publish-window start, `connectors/elexon/client.py:314`) and each period is published 2 h 30 min after it starts (`published_at - timestamp_utc` = 150 min on every row of settlement dates 1–25 Sep 2026), so a BST day's last three periods fall in the next UTC publish day. Always filter on the `settlement_date` column across the full glob (`agws/**/*.parquet`) — never assume one filename's date == one settlement day's data. This is a different partitioning behaviour than `settlement_date`-partitioned datasets like FUELHH/INDO/ITSDO, which hold one clean full day per file.
- **`Solar` PSR type is present and non-trivial** (live-verified 2026-07-30: 0 MW overnight, ~12,700 MW midday peak on 24 July 2026) — not documented in the original spec, which only mentioned wind. Scope (BM-registered only vs. a broader national/embedded estimate) is unconfirmed — TODO before relying on it as an embedded-generation proxy. `Wind Onshore + Wind Offshore` summed only correlates 0.66 with FUELHH's `WIND` fuel type on the same day (mean abs diff ~1,270 MW) — the two wind figures are not interchangeable; cause of the discrepancy is also TODO.

---

## Implementation delta

- **Same B-series/ENTSO-E lineage** as AGPT (B1630).
- **Pydantic schema** `ElexonAGWS` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/agws.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
