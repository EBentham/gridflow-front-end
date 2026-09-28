---
source: elexon
dataset_key: agpt
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Actual generation per type
  summary: >-
    Great Britain's generation for every half-hour settlement period: one MW figure per
    production type, including solar and wind offshore and onshore.
  facts:
    vendor: Elexon BMRS, dataset AGPT (B1620)
    cadence: Every 30 minutes
    grain: One row per settlement period and production type
  landscape: power
  what_it_is: >-
    Elexon's actual generation per production type for each GB settlement period: one MW figure
    per type, sent as a readable label (`Fossil Gas`, `Wind Offshore`) rather than a code. A
    recent half-hour carries 11 types. They include `Solar` and wind split into offshore and
    onshore, which FUELHH lacks, and no interconnectors.
  how_used:
    - Solar and wind outturn by type for GB price and residual-demand models.
    - Checking wind and solar forecasts against outturn, offshore and onshore apart.
    - Cross-checking the FUELHH fuel mix for the same settlement periods.
  chart:
    type: stacked-area
    silver: elexon/agpt
    time: timestamp_utc
    value: generation_mw
    filter:
      - {column: settlement_date, op: ge, value: "2026-09-14"}
      - {column: settlement_date, op: le, value: "2026-09-20"}
    dedup: {on: [settlement_date, settlement_period, psr_type], order_by: published_at}
    group: psr_type
    group_map:
      Nuclear: nuclear
      Biomass: biomass
      Hydro Run-of-river and poundage: hydro
      Fossil Hard coal: coal_oil
      Fossil Oil: coal_oil
      Other: other
      Fossil Gas: gas
      Wind Offshore: wind
      Wind Onshore: wind
      Solar: solar
      Hydro Pumped Storage: ps
    series_order: [nuclear, biomass, hydro, coal_oil, other, gas, wind, solar, ps]
    aggregation: sum
    window: {start: "2026-09-13", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: Generation by type, 14 to 20 September 2026
    caption: >-
      Silver `elexon/agpt`, MW, every half-hour of settlement dates 14 to 20 September 2026,
      with a group's types summed. For a day from 15:30 UTC on the 17th, wind reads 2.2 to 4.6
      GW; FUELHH wind does not dip. Cause unverified.
    alt: >-
      Stacked area chart of GB generation by production type from elexon/agpt, in MW, for every
      half-hour of settlement dates 14 to 20 September 2026. From zero upward: nuclear (3.3 to 3.7
      GW), biomass, run-of-river hydro, coal and oil (zero), other, gas (1.5 to 12.1 GW), wind (up
      to 20.2 GW, but 2.2 to 4.6 GW for a day from the 17th), solar (up to 10.1 GW on the 20th)
      and pumped storage (up to 1.2 GW). The total runs from 12.4 to 33.8 GW; nothing falls below
      zero.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: ps, label: Pumped storage, codes: Hydro Pumped Storage, paint: hatch-cross, note: "Zero or above in this window, unlike the signed PS code in FUELHH."}
      - {series: solar, label: Solar, codes: Solar, tag: solar, note: "FUELHH has no solar code."}
      - {series: wind, label: Wind, codes: "Wind Offshore, Wind Onshore", tag: wind, note: "Offshore and onshore summed here; the rows keep them apart."}
      - {series: gas, label: Gas, codes: Fossil Gas, tag: gas}
      - {series: other, label: Other, codes: Other, note: "Elexon's own type; what it holds is undocumented."}
      - {series: coal_oil, label: Coal and oil, codes: "Fossil Hard coal, Fossil Oil", paint: hatch-dots, note: "Zero in every half-hour of this window."}
      - {series: hydro, label: "Hydro, run-of-river", codes: Hydro Run-of-river and poundage, paint: hatch-lines}
      - {series: biomass, label: Biomass, codes: Biomass, tag: biomass}
      - {series: nuclear, label: Nuclear, codes: Nuclear, tag: nuclear}
  raw_feed:
    note: >-
      From the Elexon Insights API in 24-hour publish windows; bronze is filed by publish day.
      Period 48 below was published after midnight UTC, so both commands run a day longer.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/AGPT?publishDateTimeFrom=2026-09-14T00:00:00Z&publishDateTimeTo=2026-09-15T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon agpt --start 2026-09-14 --end 2026-09-22, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon agpt --start 2026-09-14 --end 2026-09-21, comment: "bronze to silver, by publish day"}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-20"}
        - {column: settlement_period, op: eq, value: 48}
        - {column: psr_type, op: in, value: [Biomass, Fossil Gas, Hydro Pumped Storage, Nuclear, Other, Solar, Wind Offshore, Wind Onshore]}
      order_by: [psr_type]
    key: [settlement_date, settlement_period, psr_type]
    caption: "All eight rows are settlement date 2026-09-20, period 48: 8 of its 11 types."
    fields:
      settlement_date: "GB settlement date, the vendor's settlementDate label as sent"
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: Start of the half-hour, computed from settlement date and period
      psr_type: "Production type as Elexon sends it: a label, not a code"
      generation_mw: "MW for the period, from the vendor's quantity field"
      business_type: Vendor business type as sent; wind and solar differ in these rows
      document_id: Vendor document id; one document carries all eight rows here
      document_revision: Revision number of that document, as sent
      published_at: Vendor publish time; here after midnight UTC, the next day
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_agpt`, filtered on
      `settlement_date` with both ends included. Lineage columns are dropped.
    cells:
      - df = data.elexon.query("agpt", "2026-09-14", "2026-09-20")
      - df[["settlement_date", "settlement_period", "psr_type", "generation_mw"]].head()
      - |
        wide = df.pivot_table(
            index="timestamp_utc", columns="psr_type", values="generation_mw")
        wide[["Solar", "Wind Offshore", "Wind Onshore"]].plot(
            ylabel="MW", color=["#AFC64E", "#3E8C97", "#155A6E"], figsize=(8, 3.5))
    needs: 14 to 21 September 2026
    plot_alt: >-
      Line plot of Solar, Wind Offshore and Wind Onshore generation_mw against timestamp_utc for
      settlement dates 14 to 20 September 2026. Solar peaks each day, from about 6,100 to 10,100
      MW. Both wind lines drop sharply on the afternoon of the 17th, offshore to about 100 to 300
      MW, and recover on the 18th, offshore near 11,000 MW.
  related:
    - {dataset: entsoe/actual_generation, note: "The same production-type split for EU zones; empty for GB"}
    - {dataset: elexon/fuelhh, note: "The same half-hours by BMRS fuel code, with no solar"}
    - {dataset: elexon/agws, note: "Wind and solar alone, actual or estimated, per period"}
    - {dataset: elexon/atl, note: "Total load for the same periods, from the same B-series group"}
---

# Elexon - Actual Aggregated Generation Per Type (`AGPT / B1620`)

## Overview

Actual Aggregated Generation Per Type (AGPT, ENTSO-E B1620) — every PSR (Production-Storage Resource) type's aggregated MW output per settlement period. AGPT is the GB equivalent of the ENTSO-E B1620 series and is what feeds the GB row of pan-European generation transparency dashboards.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/AGPT` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years (since B-series rollout). |
| Publication lag  | Soon after each settlement period closes (B-series). Measured 2026-09-28 on Aug-Sep 2026 silver (not a vendor statement): `published_at` is 149 min after `timestamp_utc` on every row, so periods 47-48 of a settlement day fall in the next UTC day's publish window. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | Yes | As per Elexon Swagger spec for agpt. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | Yes | As per Elexon Swagger spec for agpt. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/AGPT?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-agpt.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/agpt/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/AGPT?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "AGPT",
      "documentId": "NGET-EMFIP-AGPT-06476951",
      "documentRevisionNumber": 1,
      "publishTime": "2026-05-06T02:59:22Z",
      "businessType": "Production",
      "psrType": "Biomass",
      "quantity": 2974.0,
      "startTime": "2026-05-06T00:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 4
    },
    {
      "dataset": "AGPT",
      "documentId": "NGET-EMFIP-AGPT-06476951",
      "documentRevisionNumber": 1,
      "publishTime": "2026-05-06T02:59:22Z",
      "businessType": "Production",
      "psrType": "Hydro Pumped Storage",
      "quantity": 1.0,
      "startTime": "2026-05-06T00:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 4
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/agpt/year=YYYY/month=MM/agpt_YYYYMMDD.parquet` (`YYYYMMDD` is the bronze publish-window day, not the settlement date: no `PARTITION_SOURCE_OFFSETS`, bronze filed by `data_date = start.date()`, `client.py:314`)
**Transformer class**: `gridflow.silver.elexon.agpt.AGPTTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonAGPT` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, settlement_period, psr_type)`
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `psr_type` | `str` | No | `psrType` | Elexon's human-readable PSR *label* (e.g. "Biomass", "Wind Onshore"), stored as-is — NOT an ENTSO-E B-code. |
| `generation_mw` | `float` | No | `quantity` | MW. |
| `business_type` | `str` | Yes | `businessType` | ENTSO-E business type. |
| `document_id` | `str` | Yes | `documentId` | ENTSO-E document MRID. |
| `document_revision` | `int` | Yes | `documentRevisionNumber` | Document revision number. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Publication time / document vintage; bitemporal point-in-time field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`agpt.py:119-124`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 4,
        "timestamp_utc": "2026-05-06T00:30:00+00:00",
        "psr_type": "Biomass",
        "generation_mw": 2974.0,
        "business_type": "Production",
        "document_id": "NGET-EMFIP-AGPT-06476951",
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

- **PSR types are human-readable labels.** Elexon's AGPT API returns PSR *labels* (e.g. "Biomass", "Hydro Pumped Storage"); silver stores them verbatim. They are NOT ENTSO-E B-codes — do not assume a B01-B25 code domain.
- **Cross-source representation differs.** Elexon stores human-readable PSR *labels*; ENTSO-E's `wind_solar_forecast` stores the raw B-code. The same concept is represented two ways across sources — downstream joins must not assume a shared code domain.
- **`document_revision`** — same period+psr_type can be re-issued. The transformer does not compare revisions: it keeps the last row per key in bronze file order (`raw_{ts}_{hash}`, so the latest fetch) within one publish-day partition (`agpt.py:114-117`, `bronze/writer.py:57`). A re-issue published on a later day lands in a later silver file. Only revision 1 seen in silver as of 2026-09-28.
- **Wind dip, 17-18 Sep 2026 (cause unverified).** From 2026-09-17 15:30 to 2026-09-18 15:30 UTC, `Wind Offshore` reads 117-288 MW and `Wind Offshore` + `Wind Onshore` 2.2-4.6 GW, while FUELHH `WIND` for the same half-hours reads 11.7-16.9 GW. All rows revision 1 (measured 2026-09-28 on local silver). Not checked against the live API.

---

## Implementation delta

- **Pydantic schema** `ElexonAGPT` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).
- **B-series (B1620)** — payload follows ENTSO-E document/timeseries shape but exposed via Elexon's flattened JSON.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/agpt.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
