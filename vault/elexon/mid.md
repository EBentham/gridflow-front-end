---
source: elexon
dataset_key: mid
vendor: Elexon BMRS
last_verified: 2026-09-07
layer_coverage: bronze, silver
v2_fix_history:
  - date: 2026-05-20
    phase: gridflow-G5-W1.2
    pr: https://github.com/EBentham/gridflow/pull/7
    change: silver transformer now also recognises current-API field names (dataProvider, price) alongside legacy (dataProviderId, midPrice)
page:
  title: Market index price and volume
  summary: >-
    Great Britain's market index for each half-hour settlement period: a price in £/MWh and a
    volume in MWh, per data provider.
  facts:
    vendor: Elexon BMRS, dataset MID
    cadence: Every 30 minutes
    grain: One row per settlement period and data provider
  landscape: market
  what_it_is: >-
    Elexon's market index for each GB settlement period, from two providers, `APXMIDP` and
    `N2EXMIDP`. Per Elexon's Market Index Definition Statement, the price is the volume-weighted
    average of half-hour, one-, two- and four-hour products traded within eight hours of the
    submission deadline, and the volume their sum. Day-ahead auction trades carry no weight; below
    25 MWh, both default to zero.
  how_used:
    - A traded reference price for each half-hour, set against the imbalance price.
    - Target or lagged feature for a half-hourly GB power price model.
    - Traded volume as a liquidity check on the price beside it.
  chart:
    type: line
    silver: elexon/mid
    time: timestamp_utc
    value: market_index_price
    filter:
      - {column: data_provider_id, op: eq, value: APXMIDP}
      - {column: settlement_date, op: ge, value: "2026-09-15"}
      - {column: settlement_date, op: le, value: "2026-09-21"}
    aggregation: last
    window: {start: "2026-09-14", end: "2026-09-21"}
    unit: £/MWh
  chart_view:
    title: Market index price, 15 to 21 September 2026
    caption: >-
      Silver `elexon/mid`, £/MWh, one value per half-hour of settlement dates 15 to 21 September
      2026, from `APXMIDP` only. `N2EXMIDP` is left out: it sends a price and volume of 0 in
      every period shown.
    alt: >-
      Line chart of the APXMIDP market index price from elexon/mid, in £/MWh, for every half-hour
      of settlement dates 15 to 21 September 2026. It runs between 46 and 212 on the 15th and 16th,
      dips just below zero on the 17th, 18th and 19th (lowest -3.26), falls to -19.03 at 15:00 UTC
      on the 20th, rises to 198 that evening, and stays between 135 and 207 on the 21st.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: market_index_price, label: Market index price, codes: APXMIDP, paint: petrol}
  raw_feed:
    note: >-
      From the Elexon Insights API, in 24-hour windows of period start time. `gridflow ingest`
      writes each response to bronze; `gridflow transform` types it into silver, reading the
      day before too.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/MID?from=2026-09-20T00:00:00Z&to=2026-09-21T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon mid --start 2026-09-14 --end 2026-09-22, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon mid --start 2026-09-15 --end 2026-09-21, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-20"}
        - {column: settlement_period, op: ge, value: 32}
        - {column: settlement_period, op: le, value: 35}
      order_by: [settlement_period, data_provider_id]
    key: [settlement_date, settlement_period, data_provider_id]
    caption: "Settlement date 2026-09-20, periods 32 to 35, both providers: `APXMIDP` turns from negative to positive."
    fields:
      settlement_date: GB settlement date, as Elexon labels it
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: Start of the half-hour, computed from settlement date and period
      data_provider_id: "Market index data provider code, as sent (`dataProvider`)"
      market_index_price: "Volume-weighted price of qualifying trades, £/MWh; 0 below the liquidity threshold"
      market_index_volume: "Summed volume of qualifying trades, MWh; 0 below the liquidity threshold"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_mid`, both providers,
      filtered on `settlement_date` with both ends included. Lineage columns are dropped and rows
      come ordered by `settlement_date` only.
    cells:
      - |
        df = data.elexon.query("mid", "2026-09-15", "2026-09-21")
        df = df.sort_values(["timestamp_utc", "data_provider_id"])
      - df[["settlement_date", "settlement_period", "data_provider_id", "market_index_price", "market_index_volume"]].head()
      - |
        apx = df[df.data_provider_id == "APXMIDP"]
        apx.plot(x="timestamp_utc", y="market_index_price", ylabel="£/MWh",
                 color="#155A6E", figsize=(8, 3.5))
    needs: 15 to 21 September 2026
    plot_alt: >-
      Line plot of the APXMIDP market_index_price against timestamp_utc, 15 to 21 September 2026:
      115 to 212 £/MWh most of the 15th and 16th (one dip to 46), near zero around midday on the
      17th and 18th and for most of the 19th and 20th, low of -19 on the 20th, then 135 to 207 on
      the 21st.
  related:
    - {dataset: elexon/system_prices, note: "The imbalance price for the same settlement periods"}
    - {dataset: elexon/fuelhh, note: "Generation by fuel for the same settlement periods"}
    - {dataset: elexon/indo, note: "Demand outturn for the same settlement periods"}
---

# Elexon - Market Index Data (`MID`)

## Overview

Market Index Data — published reference prices and volumes from accredited Market Index Data Providers (MIDPs), used by the BSC to derive the Power Exchange Reference Price. MID is the wholesale-market anchor that ties Balancing Mechanism cash-out prices to traded GB power prices.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/MID` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Half-hourly, aligned with each settlement period. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `from` | string | Yes | The "from" start time or settlement date for the filter. | `2026-05-06T00:00Z` |
| `to` | string | Yes | The "to" start time or settlement date for the filter. | `2026-05-06T03:00Z` |
| `settlementPeriodFrom` | integer | No | The "from" settlement period for the filter. This should be an integer from 1-50 inclusive. | `1` |
| `settlementPeriodTo` | integer | No | The "to" settlement period for the filter. This should be an integer from 1-50 inclusive. | `48` |
| `dataProviders` | array | No | The data providers to query. If no data provider is selected both will be displayed. | `APXMIDP` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/MID?from=2026-05-06T00:00Z&to=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-mid.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/mid/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/MID?from=2026-05-06T00:00Z&to=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "MID",
      "startTime": "2026-05-06T03:00:00Z",
      "dataProvider": "APXMIDP",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 9,
      "price": 105.43,
      "volume": 1892.45
    },
    {
      "dataset": "MID",
      "startTime": "2026-05-06T03:00:00Z",
      "dataProvider": "N2EXMIDP",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 9,
      "price": 0.0,
      "volume": 0.0
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/mid/year=YYYY/month=MM/mid_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.mid.MIDTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonMID`
**Dedup key**: `(settlement_date, settlement_period, data_provider_id)`, `unique(keep="last")` in the transformer (`silver/elexon/mid.py:122-125`)
**Point-in-time field**: none from the vendor; `available_at` follows the vintage policy below (`silver/elexon/mid.py:29-41`)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `data_provider_id` | `str` | Yes | `dataProviderId` (legacy) / `dataProvider` (current) | MIDP code (e.g. APXMIDP). G5-W1.2: live API renamed to `dataProvider` 2026-05; transformer renames both. |
| `market_index_price` | `float` | Yes | `midPrice` (legacy) / `price` (current) | GBP/MWh. G5-W1.2: live API renamed to `price` 2026-05; transformer renames both. |
| `market_index_volume` | `float` | Yes | `volume` | MWh. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`mid.py:127-131`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 9,
        "timestamp_utc": "2026-05-06T03:00:00+00:00",
        "data_provider_id": "APXMIDP",
        "market_index_price": 105.43,
        "market_index_volume": 1892.45,
        "data_provider": "elexon",
        "ingested_at": "2026-05-08T12:00:00Z"
    },
]
```

---

### Vintage policy (ADR-031; identity updated 2026-09-07, gridflow v0.21 unit L, PR #79)

**Current identity `elexon-mid/vp-2026-09b`, lag 35 min from settlement-period
start** (= 5 min after period end), `dataset_version` 1.1.0. It replaces
`elexon-mid/vp-2026-09` at 60 min; ADR-031 requires a new dated identity whenever a
lag changes, so both labels exist on disk until MID's rebuild re-stamps every row.

**Why 35 and not 60.** The cadence observation below (period end + ~1 min) puts real
availability at period start + ~31 min. 60 min was chosen as a deliberately loose
upper bound; it is 29 minutes looser than the one measurement, and a lag that
overstates delay hides data a backtest was entitled to see. 35 min keeps a 4-minute
margin above the observation. **This is still an ASSUMPTION resting on a single
observation on a single day** — a tighter number, not a better-evidenced one.

**No vendor statement of publication cadence exists** (researched 2026-09-07,
`TODO: verify` retained). Current BSCP01 gives MID *Providers* a target to send data
to BMRA by the end of the settlement period — a submission target, not an Insights
publication guarantee. The current OpenAPI describes the stream as suitable for
frequent polling but states no latency. A 15-minute figure exists only in a
superseded 2017 BMRA URS and cannot establish current behaviour.

**On-disk state (rebuilt 2026-09-07).** 1,832 files, **175,423 rows**, all
`dataset_version` 1.1.0. Labels: `elexon-mid/vp-2026-09b` × 171,965, every one at
**exactly +35 min**, plus `ingest-clock` × 3,458. **Duplicate keys 3,652 → 0** (APXMIDP
1,830 → 0) — the rebuild carried unit P's partition trim as well as this stamp, and the
row delta is exactly the duplicate count. Coverage is unchanged: the same 15 missing
APXMIDP periods over 11 days that were there before, each absent from bronze. The
`ingest-clock` rows were **not** re-stamped by the wider covering set, contrary to the
plan's expectation — their distribution is identical before and after.

### Superseded declaration (v0.20, for reference)

MID emits no vendor `published_at`, so `available_at` was the ingest clock —
a backfilled 2021 row read as "available" on the day it was backfilled.
gridflow v0.20 declares a **Vintage Policy** on `MIDTransformer`
(`VINTAGE_POLICY`, `silver/elexon/mid.py`):

| Field | Value |
|---|---|
| name | `elexon-mid/vp-2026-09` |
| lag | **60 min from settlement-period start** (= 30 min after period end) — **ASSUMPTION** by analogy with INDO's measured ~30-min latency; `TODO: verify` MID publication cadence against Elexon |
| applies_before | `2026-08-01T00:00Z` — rows with an earlier `event_time` are reconstructed; later rows keep the honest ingest clock |
| rule | `available_at = coalesce(published_at, event_time + lag)` only when `event_time < applies_before` AND `event_time + lag < ingest_stamp`; otherwise the ingest stamp |

**Publication cadence, measured 2026-09-06.** Elexon does not document a
publication cadence for this dataset, so it was checked against the live
endpoint. At 15:01Z the latest available period was settlement period 32,
covering 14:30–15:00Z, which had ended one minute before. The in-progress
period was absent. So MID is **not** published ahead of delivery, and its
latency after period end is about a minute. The declared 60-minute lag is
therefore a conservative upper bound, roughly 30 minutes looser than
reality, which is the safe direction: a consumer sees the price late, never
early. One observation on one day. Settlement periods are numbered on UK
local time, so under BST a period's UTC start is an hour behind its label.

Every row carries a `vintage_policy` label: the policy name when the
reconstruction won, `"ingest-clock"` when the ingest stamp won, `"vendor"`
when a `published_at` won. Parquet written before v0.20 has no column and
reads as null — treat null as unknown. This is a declared approximation of
availability, not a vendor fact. Source of truth: `docs/DECISION_LOG/ADR-031-vintage-policy-reconstruction.md`.

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Two data providers** per period (`APXMIDP`, `N2EXMIDP`; corrected 2026-09-28, no other code in silver). Silver dedup includes `data_provider_id` (`mid.py:122-125`), so each period has one row per provider: filter on a provider before treating the price as one series.
- **Partition grain is capture date; silver grain is settlement date (v0.21 unit P,
  PR #78, 2026-09-07).** A bronze capture partition D also carries the first
  periods of D+1. Measured over 400 MID bronze files
  (`settlement_date - partition_date`): `{0: 37,268, +1: 1,764}` — forward spill
  only, unlike fuelhh which spills both ways. The silver file for date D is
  therefore built from bronze partitions **D-1 and D**, then trimmed to the rows
  date D owns. Before this the per-date overwrite wrote the same key into two
  files: **3,652 duplicate keys** measured on disk (periods 1 and 3).
  **Rebuilt 2026-09-07 under v0.21 unit L** (see Vintage policy above): 0 duplicate
  keys on `(settlement_date, settlement_period, data_provider_id)`, re-checked over
  all 1,842 silver files on 2026-09-28.

---

## Implementation delta

- **Param style**: docs require `from`/`to`; code matches.

### V2-FIX changelog

- **2026-05-20 — gridflow G5-W1.2 (PR #7)**: live Elexon API now returns
  `dataProvider` / `price` rather than the original `dataProviderId` /
  `midPrice`. Silver transformer extended to rename both shapes; pre-G5
  silver carried `null` on `data_provider_id` and `market_index_price`
  because the live bronze didn't match the original rename map (P1
  silent-null bug).

---

## Modelling notes

### Definition citations (gridflow_models v2.1 F-5, OWNER #865)

Source record: `gridflow_models/.planning/phases/v2.1-F-5-vendor-definitions/CITATIONS.md` (Opus research review CONVERGED, REVIEW-RESEARCH-2); archived bytes under `C:/gridflow-data/receipts/v2.1-F-5/sources/` (`#NN:line`). Written under OWNER #865 on 2026-09-24. Citations only: the owner's class-3 ruling on them is pending at the gridflow_models v2.1 close.

- **What MID is:** under the Market Index Definition Statement (MIDS v9.0, effective 18 Apr 2019; still "the current
  MIDS" per Elexon's MIDS review 2025, last updated 24 Sep 2025, #05:544, #05:571), the price is the volume-**weighted
  average price** of qualifying trades and the volume is the "sum of the volume" (MIDS Appendices A1/A2). Qualifying
  trades are "Half Hour, One Hour, Two Hour and Four Hour products traded within eight hours of the Submission Deadline"
  (#05). The **Day Ahead Auction** product has weight 0 for both MIDPs (MIDS change log, CP1359). **MID is a short-horizon
  qualifying-trade index, not a day-ahead auction price.** `TODO:` the MIDS version in force for Aug–Sep 2026 is not
  archived beyond the 2025 review.
- **Providers:** MIDS names EPEX SPOT SE and Nord Pool AS methods (#03:709). The BMRS guide expands `APXMIDP` as
  "Automated Power Exchange (UK)" (#04:11093–11097). `TODO:` no archived primary line maps `APXMIDP` → EPEX or
  `N2EXMIDP` → Nord Pool. The two methods are identical in products, weights, formula and the 25 MWh threshold. The
  provider code seen in the data is `N2EXMIDP`; the gotcha above that said `NORDPOOLMIDP` was corrected on 2026-09-28.
- **Zero price/volume:** below the **25 MWh** individual liquidity threshold, price and volume default to zero; zero can
  also mean "no qualifying trades" (#03, #05). The legacy 2018 BMRS guide adds a missing-submission default ("was not
  received. Price and volume defaulted to 0.", #04). `TODO:` whether that still applies in 2026. Elexon (2024/25): "For
  Nord Pool, 17,492 Settlement Periods (99.3%) had the MIP and MIV defaulted to zero … For 16,918 of these … there were no
  qualifying trades" (#05:765). Seat measurement, not a definition: `N2EXMIDP` volume is zero in 813/816 periods,
  2026-08-18…2026-09-03.

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/mid.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
