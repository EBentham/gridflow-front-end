---
source: elexon
dataset_key: indo
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Initial demand outturn
  summary: >-
    Elexon's initial GB demand outturn for each half-hour, at two boundaries (`INDO` national,
    `ITSDO` transmission), plus `INDOD`, a daily total.
  facts:
    vendor: Elexon BMRS, datasets INDO, ITSDO and INDOD
    cadence: Every 30 minutes; INDOD once a day
    grain: One row per settlement period; INDOD one row per settlement date
  landscape: power
  what_it_is: >-
    `INDO` and `ITSDO` are the same half-hourly outturn at two boundaries. NESO defines `INDO` as
    national demand, and `ITSDO` as that plus a fixed station-load estimate (500 MW in BST, 600 MW
    in GMT), pumped-storage pumping and interconnector exports, so `ITSDO` is the higher figure.
    NESO's embedded wind and solar estimates are in neither. `INDOD` is each day's `INDO` total.
  how_used:
    - The actual to score a GB demand forecast against, at the matching boundary.
    - Demand and residual-demand features for a GB power price model.
    - Daily demand totals for trend and weather work, from INDOD.
  chart:
    type: line
    silver: elexon/indo
    time: timestamp_utc
    value: initial_demand_outturn_mw
    filter:
      - {column: settlement_date, op: ge, value: "2026-09-14"}
      - {column: settlement_date, op: le, value: "2026-09-20"}
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: National demand (INDO), 14 to 20 September 2026
    caption: >-
      Silver `elexon/indo` only, MW, every half-hour of settlement dates 14 to 20 September 2026,
      one value per half-hour. `ITSDO`, the transmission figure, is not drawn here; the notebook
      below plots both.
    alt: >-
      Line chart of GB national demand (INDO) from elexon/indo, in MW, for every half-hour of
      settlement dates 14 to 20 September 2026 (Monday to Sunday). Each day dips overnight, to
      16,807 to 19,207 MW on the weekdays, and peaks in the early evening, at 28,192 to 30,813 MW
      on the weekdays, the highest on Wednesday 16th. Saturday peaks lower, at 26,475 MW, and
      Sunday dips at midday to 14,191 MW, the lowest in the window.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: initial_demand_outturn_mw, label: National demand, codes: INDO, paint: petrol}
  raw_feed:
    note: >-
      From the Elexon Insights API in 24-hour publish windows; swap `indo` for `itsdo` or `indod`.
      Both windows start a day early: in BST a settlement date begins at 23:00 UTC.
    commands:
      - {run: gridflow ingest elexon indo --start 2026-09-13 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon indo --start 2026-09-13 --end 2026-09-20, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-20"}
        - {column: settlement_period, op: in, value: [1, 2, 12, 24, 29, 36, 39, 48]}
      order_by: [settlement_period]
    mark: {settlement_period: 1}
    key: [settlement_date, settlement_period]
    caption: "Eight of settlement date 2026-09-20's 48 periods; period 1 starts at 23:00 UTC on the 19th."
    fields:
      settlement_date: "GB settlement date, the vendor's `settlementDate` label"
      settlement_period: Half-hour of the settlement date, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: Start of the half-hour, computed from the settlement date and period
      initial_demand_outturn_mw: "National demand for the half-hour in MW, the vendor's `demand`"
      published_at: "Vendor publish time, from `publishTime`"
      data_provider: "Same on every row: elexon"
      ingested_at: When the silver transform ran
  notebook:
    lead: >-
      Returns pandas DataFrames from `silver_elexon_indo`, `silver_elexon_itsdo` and
      `silver_elexon_indod`, each filtered on `settlement_date`, both ends included; lineage columns
      dropped. The last cell checks INDOD against half the INDO sum.
    cells:
      - |
        indo = data.elexon.query("indo", "2026-09-14", "2026-09-20")
        itsdo = data.elexon.query("itsdo", "2026-09-14", "2026-09-20")
      - |
        key = ["settlement_date", "settlement_period", "timestamp_utc"]
        both = indo[key + ["initial_demand_outturn_mw"]].merge(
            itsdo[key + ["initial_transmission_system_demand_outturn_mw"]], on=key)
        both.columns = key + ["indo_mw", "itsdo_mw"]
        both["itsdo_minus_indo_mw"] = both.itsdo_mw - both.indo_mw
        both = both.sort_values("timestamp_utc", ignore_index=True)
        both.head()
      - |
        both.plot(x="timestamp_utc", y=["itsdo_mw", "indo_mw"], ylabel="MW",
                  color=["#C77E3C", "#155A6E"], figsize=(8, 3.5))
      - |
        indod = data.elexon.query("indod", "2026-09-14", "2026-09-20")
        daily = indo.groupby("settlement_date", as_index=False).initial_demand_outturn_mw.sum()
        daily["indo_sum_over_2"] = daily.pop("initial_demand_outturn_mw") / 2
        indod[["settlement_date", "initial_demand_outturn_mw"]].merge(daily, on="settlement_date")
    needs: INDO, ITSDO and INDOD, published 13 to 20 September 2026
    plot_alt: >-
      Line plot of itsdo_mw (clay) and indo_mw (petrol) for settlement dates 14 to 20 September
      2026. Same daily cycle, ITSDO above INDO throughout; the lines nearly
      touch on the evening of the 16th and are furthest apart before dawn on the 20th. ITSDO peaks
      near 33,500 MW on the 17th; INDO falls to about 14,200 MW on the 20th.
  related:
    - {dataset: elexon/fuelhh, note: "Pumped storage and interconnector codes: the pumping and exports ITSDO adds"}
    - {dataset: elexon/ndf, note: "Day-ahead forecast of national demand, to score against INDO"}
    - {dataset: elexon/tsdf, note: "Forecast of transmission system demand, to score against ITSDO"}
    - {dataset: neso_data_portal/embedded_wind_solar_forecast, note: "Embedded wind and solar, which lower both demand figures"}
  family:
    slug: demand-outturn
    members:
      - dataset: indo
        differs: "National demand: excludes station load, pumped-storage pumping and interconnector exports"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/INDO?publishDateTimeFrom=2026-09-13T00:00:00Z&publishDateTimeTo=2026-09-14T00:00:00Z&page=1"
      - dataset: itsdo
        differs: "Transmission demand: INDO plus station-load estimate, pumped-storage pumping and interconnector exports"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/ITSDO?publishDateTimeFrom=2026-09-13T00:00:00Z&publishDateTimeTo=2026-09-14T00:00:00Z&page=1"
      - dataset: indod
        differs: "One row per date: a daily total that tracks half the day's INDO sum"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/INDOD?publishDateTimeFrom=2026-09-13T00:00:00Z&publishDateTimeTo=2026-09-14T00:00:00Z&page=1"
---

# Elexon - Initial National Demand Outturn (`INDO`)

## Overview

Initial National Demand Outturn (INDO) — the first published estimate of the realised national demand per settlement period. INDO is published shortly after delivery and is the headline GB demand outturn series.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/INDO` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | ~hour after each settlement period closes. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | No | As per Elexon Swagger spec for indo. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | As per Elexon Swagger spec for indo. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/INDO?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-indo.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/indo/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/INDO?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "INDO",
      "publishTime": "2026-05-06T03:00:00Z",
      "startTime": "2026-05-06T02:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 8,
      "demand": 20775
    },
    {
      "dataset": "INDO",
      "publishTime": "2026-05-06T02:30:00Z",
      "startTime": "2026-05-06T02:00:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 7,
      "demand": 21718
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/indo/year=YYYY/month=MM/indo_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.indo.INDOTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonINDO` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, settlement_period)`
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `initial_demand_outturn_mw` | `float` | No | `demand` | MW. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Publication time / document vintage; bitemporal point-in-time field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`indo.py:115-121`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 8,
        "timestamp_utc": "2026-05-06T02:30:00+00:00",
        "initial_demand_outturn_mw": 20775,
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

- **First-publish outturn** — INDO is published before final settlement and is revised over time. For final reconciled outturn, use settlement-run datasets.
- **INDO is below ITSDO, not above** (verified 2026-07-30, ~2,375 MW average gap on 24 July 2026, flat across the day — see [itsdo.md](./itsdo.md) gotchas; exact decomposition of the gap is still TODO, embedded solar has been ruled out as a driver). Do not assume INDO is the larger of the two national/transmission demand figures, and do not assume the gap is embedded-generation-driven.

---

## Implementation delta

- **Pydantic schema** `ElexonINDO` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Modelling notes

### Definition citations (gridflow_models v2.1 F-5, OWNER #865)

Source record: `gridflow_models/.planning/phases/v2.1-F-5-vendor-definitions/CITATIONS.md` (Opus research review CONVERGED, REVIEW-RESEARCH-2); archived bytes under `C:/gridflow-data/receipts/v2.1-F-5/sources/` (`#NN:line`). Written under OWNER #865 on 2026-09-24. Citations only: the owner's class-3 ruling on them is pending at the gridflow_models v2.1 close.

- **Mapping.** NESO: National Demand "is equivalent to the Initial National Demand Outturn (INDO)"; Transmission System
  Demand "is equivalent to the Initial Transmission System Outturn (ITSDO)" (NESO data portal, Daily demand update
  definitions, #01:244, #01:268; live page, undated). The Grid Code's terms are **National Demand** and **National
  Electricity Transmission System Demand** (Grid Code Glossary, Issue 6 Revision 45, 13 Aug 2026, #02:3009–3033); no
  archived Grid Code text names INDO/ITSDO.
- **Station-transformer load:** INDO excludes it (Grid Code National Demand "minus … the Demand taken by Station
  Transformers"). ITSDO includes it **as a fixed estimate**: "Transmission System Demand includes an estimate of station
  load of 500MW in BST and 600MW in GMT" (#01:268). ITSDO−INDO does not contain metered station load.
- **Pumped-storage pumping and interconnector exports:** INDO excludes both; ITSDO includes both. TSD is "ND plus the
  additional generation required to meet station load, pump storage pumping and interconnector exports" (#01:268); the
  Grid Code National Demand "does not include … any exports".
- **Electricity Storage Modules (battery charging):** the Grid Code lists "Pumped Storage Units' and Electricity Storage
  Modules'" in both clauses (excluded from National Demand, included in NETS Demand; #02:3013–3015, 3031–3033). NESO
  names only pump-storage pumping, so the sources disagree. `TODO:` battery treatment in INDO/ITSDO *as published*.
- **Embedded wind and solar:** NESO's unmetered estimates are components of neither series. They are "embedded in the
  distribution network and invisible to National Grid ESO. Their effect is to suppress the electricity demand" (#01:292,
  #01:316, with #01:244 "sum of metered generation"). Supply from **Embedded Large Power Stations** is included in both
  (Grid Code). `TODO:` no blanket classification of all distribution-connected wind/solar.

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/indo.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
