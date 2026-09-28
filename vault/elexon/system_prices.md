---
source: elexon
dataset_key: system_prices
vendor: Elexon BMRS
last_verified: 2026-09-07
layer_coverage: bronze, silver, gold
page:
  title: System buy and sell prices
  summary: >-
    Great Britain's imbalance prices for every half-hour settlement period: the system sell and
    buy prices in £/MWh, with net imbalance volume.
  facts:
    vendor: Elexon BMRS, dataset DISEBSP
    cadence: Every 30 minutes
    grain: One row per settlement period and capture; the latest view keeps one
  landscape: market
  what_it_is: >-
    Elexon's imbalance prices for each GB settlement period: the system sell price (SSP) and
    system buy price (SBP) in £/MWh, the net imbalance volume in MWh, and a price derivation
    code. gridflow parses the two prices from separate API fields; in the week charted they are
    identical in every period. The endpoint sends no settlement-run field, so `run_type` is null.
  how_used:
    - Target for a GB imbalance price forecast, alongside net imbalance volume.
    - Pricing the cost of a half-hour's imbalance against a traded position.
    - Comparing cash-out with the market index price for the same period.
  chart:
    type: line
    silver: elexon/system_prices
    time: timestamp_utc
    value: system_sell_price
    filter:
      - {column: settlement_date, op: ge, value: "2026-09-16"}
      - {column: settlement_date, op: le, value: "2026-09-22"}
    dedup: {"on": [settlement_date, settlement_period], order_by: published_at}
    aggregation: last
    window: {start: "2026-09-15", end: "2026-09-22"}
    unit: £/MWh
  chart_view:
    title: Imbalance price, 16 to 22 September 2026
    caption: >-
      Silver `elexon/system_prices`, £/MWh, one value per half-hour of settlement dates 16 to 22
      September 2026: each period's system sell price from its latest capture. The buy
      price is identical in every period shown.
    alt: >-
      Line chart of the system sell price from elexon/system_prices, in £/MWh, for every half-hour
      of settlement dates 16 to 22 September 2026. It ranges from 55 to 275 on the 16th, dips just
      below zero on the 17th, 18th and 19th (lowest about -14), falls to -50 at 13:30 UTC on the
      20th, and stays between 103 and 293 on the 21st and 22nd, except one spike to 594 at 20:00
      UTC on the 22nd.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: system_sell_price, label: System sell price, codes: SSP, paint: petrol, note: "SBP equals it in every period of this window."}
  raw_feed:
    note: >-
      From the Elexon Insights API, one call per settlement date. `gridflow ingest` writes each
      response to bronze; `gridflow transform` types it into silver, appending a row per capture.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/2026-09-20?page=1"
    commands:
      - {run: gridflow ingest elexon system_prices --start 2026-09-16 --end 2026-09-22, comment: "bronze; the end date is fetched"}
      - {run: gridflow transform elexon system_prices --start 2026-09-16 --end 2026-09-22, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-20"}
        - {column: settlement_period, op: ge, value: 26}
        - {column: settlement_period, op: le, value: 33}
      dedup: {"on": [settlement_date, settlement_period], order_by: published_at}
      order_by: [settlement_period]
    mark: {settlement_period: 30}
    key: [settlement_date, settlement_period]
    caption: "Settlement date 2026-09-20, periods 26 to 33, the latest version of each: all below zero."
    fields:
      settlement_date: GB settlement date, as Elexon labels it
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: Start of the half-hour, computed from settlement date and period
      system_sell_price: System sell price (SSP), £/MWh, as sent
      system_buy_price: System buy price (SBP), £/MWh, parsed from its own API field
      net_imbalance_volume: Net imbalance, MWh; positive means the system was short, negative long (Elexon N0430)
      run_type: Settlement run; null, because this endpoint sends no run field
      price_derivation_code: "Elexon's code for how the price was derived, as sent"
      published_at: "Vendor record time (`createdDateTime`), UTC; the latest one wins"
      data_provider: "Same on every row: elexon"
      ingested_at: When the silver transform ran
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB view `silver_elexon_system_prices_latest`, which
      keeps each period's newest vendor version, filtered on `settlement_date` with both ends
      included. Lineage columns are dropped and rows come ordered by `settlement_date` only.
    cells:
      - |
        df = data.elexon.query("system_prices", "2026-09-16", "2026-09-22")
        df = df.sort_values("timestamp_utc")
      - df[["settlement_date", "settlement_period", "system_sell_price", "system_buy_price", "net_imbalance_volume"]].head()
      - |
        df.plot(x="timestamp_utc", y="system_sell_price", ylabel="£/MWh",
                color="#155A6E", figsize=(8, 3.5))
    needs: 16 to 22 September 2026
    plot_alt: >-
      Line plot of system_sell_price against timestamp_utc, 16 to 22 September 2026: 55 to 275
      £/MWh on the 16th, falling to near zero for much of the 19th and 20th (low of -50 on the
      20th), then 103 to 293 on the 21st and 22nd, except one spike to 594 late on the 22nd.
  related:
    - {dataset: elexon/mid, note: "Market index price for the same settlement periods"}
    - {dataset: elexon/boal, note: "The accepted bids and offers behind each period's price"}
    - {dataset: elexon/netbsad, note: "Balancing-services adjustments applied to these prices"}
    - {dataset: elexon/market_depth, note: "Accepted balancing volumes for the same settlement periods"}
---

# Elexon - System Buy/Sell Prices (`DISEBSP`)

## Overview

System Buy Price (SBP) and System Sell Price (SSP) — the cash-out prices used by the GB electricity Balancing Mechanism to settle imbalance. SBP is what generators pay (or are paid) for being short relative to their physical notifications, and SSP is what suppliers pay for being long. Together with the Net Imbalance Volume, this dataset is the canonical signal for short-term GB power-market value and is the basis of the imbalance price in BSC settlement.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/balancing/settlement/system-prices/{settlementDate}` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years (settlement records back to BMRS launch). |
| Publication lag  | Released as the settlement run progresses: II within ~hours, SF on settlement day, R1/R2/R3/RF over reconciliation timeline. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `settlementDate` | string | Yes | The settlement date to filter. This must be in the format yyyy-MM-dd. | `2026-05-06` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/2026-05-06?format=json" \
  -o "/tmp/elexon-system_prices.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/system_prices/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/2026-05-06?format=json:

```json
{
  "metadata": {
    "datasets": [
      "DISEBSP"
    ]
  },
  "data": [
    {
      "settlementDate": "2026-05-06",
      "settlementPeriod": 1,
      "startTime": "2026-05-05T23:00:00Z",
      "createdDateTime": "2026-05-06T23:44:34Z",
      "systemSellPrice": 96.79,
      "systemBuyPrice": 96.79,
      "bsadDefaulted": false,
      "priceDerivationCode": "N",
      "reserveScarcityPrice": 0.0,
      "netImbalanceVolume": -37.99166666666667,
      "sellPriceAdjustment": 0.0,
      "buyPriceAdjustment": 0.0,
      "replacementPrice": null,
      "replacementPriceReferenceVolume": null,
      "totalAcceptedOfferVolume": 578.0084677419355,
      "totalAcceptedBidVolume": -616.25,
      "totalAdjustmentSellVolume": 0.0,
      "totalAdjustmentBuyVolume": 0.0,
      "totalSystemTaggedAcceptedOfferVolume": 578.0084677419355,
      "totalSystemTaggedAcceptedBidVolume": -615.25,
      "totalSystemTaggedAdjustmentSellVolume": null,
      "totalSystemTaggedAdjustmentBuyVolume": null
    },
    {
      "settlementDate": "2026-05-06",
      "settlementPeriod": 2,
      "startTime": "2026-05-05T23:30:00Z",
      "createdDateTime": "2026-05-07T00:14:29Z",
      "systemSellPrice": 97.02,
      "systemBuyPrice": 97.02,
      "bsadDefaulted": false,
      "priceDerivationCode": "N",
      "reserveScarcityPrice": 0.0,
      "netImbalanceVolume": -35.72121737036261,
      "sellPriceAdjustment": 0.0,
      "buyPriceAdjustment": 0.0,
      "replacementPrice": null,
      "replacementPriceReferenceVolume": null,
      "totalAcceptedOfferVolume": 605.8404121863799,
      "totalAcceptedBidVolume": -641.704550703696,
      "totalAdjustmentSellVolume": 0.0,
      "totalAdjustmentBuyVolume": 0.0,
      "totalSystemTaggedAcceptedOfferVolume": 605.8404121863799,
      "totalSystemTaggedAcceptedBidVolume": -640.704550703696,
      "totalSystemTaggedAdjustmentSellVolume": null,
      "totalSystemTaggedAdjustmentBuyVolume": null
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/system_prices/year=YYYY/month=MM/system_prices_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.system_prices.SystemPriceTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonSystemPrice`
**Dedup key**: `(settlement_date, settlement_period)`, applied by the `silver_elexon_system_prices_latest` view, not in silver (`gridflow/silver/latest_views.py:95-99`)
**Point-in-time field**: `run_type` — **None on the live `DATE_PATH` feed** (`/balancing/settlement/system-prices/{date}`, DISEBSP). It is populated only by legacy/alternate endpoints that surface `settlementRunType`, where the precedence II<SF<R1<R2<R3<RF<DF applies. The transformer does not dedup: `APPEND_ONLY` and `VINTAGE_PER_BRONZE_FILE` keep every capture's rows (`system_prices.py:65-66`). The `_latest` view keeps one row per key, ordered by `available_at` (`coalesce(published_at, ingest time)`, `silver/base.py:2155`; the vendor `published_at` whenever it is present) DESC, with the null `run_type` rank inert (`latest_views.py:261-263`).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `system_sell_price` | `float` | No | `systemSellPrice` | GBP/MWh; ge=-500 le=10000. |
| `system_buy_price` | `float` | No | `systemBuyPrice` | GBP/MWh. |
| `net_imbalance_volume` | `float` | No | `netImbalanceVolume` | MWh. The system's net shortfall or surplus in the half hour, as balanced by the system operator. Positive means the system was short (it bought energy by accepting offers); negative means it was long (it accepted bids). Elexon data item N0430; gridflow passes the value through unchanged (`system_prices.py:126,204`). |
| `run_type` | `str` | Yes | `settlementRunType` (when present) | II / SF / R1 / R2 / R3 / RF / DF — BSC settlement run precedence. `/balancing/settlement/system-prices/{date}` does not expose this field, so live silver from that endpoint has `run_type = None`. Older fixtures and any future endpoint that surfaces `settlementRunType` will populate it. Nullable (Optional[str] in canonical). |
| `price_derivation_code` | `str` | Yes | `priceDerivationCode` | How the SBP/SSP was derived for the period. Observed values: `N` (normal), `P` (provisional). No regex constraint — vendor-managed value list. Nullable (Optional[str] in canonical). |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `published_at` | `datetime[UTC]` | Yes | `createdDateTime` | Vendor record time, cast to UTC (`gridflow/silver/elexon/system_prices.py:129,168-182`); see Vintage stamp below. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`system_prices.py:223-228`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 1,
        "timestamp_utc": "2026-05-06T00:00:00+00:00",
        "system_sell_price": 96.79,
        "system_buy_price": 96.79,
        "net_imbalance_volume": -37.99166666666667,
        "run_type": null,
        "price_derivation_code": "N",
        "data_provider": "elexon",
        "ingested_at": "2026-05-09T12:00:00Z"
    },
]
```

---

### Vintage stamp — vendor `createdDateTime` (rewritten 2026-09-07, gridflow v0.21 unit L, PR #79)

**The premise of the previous section was false, and this is the correction.**
It read "DISEBSP emits no vendor `published_at`". That inferred "no vendor stamp"
from the absence of the field *name* `publishTime`. The DISEBSP payload carries
**`createdDateTime` on every raw row — 94,415 / 94,415 measured 2026-09-06** — a
per-record vendor instant. It was simply unmapped, so v0.20's Vintage Policy was
reconstructing `available_at` for a dataset that had a real one.

From gridflow v0.21 (`DATASET_VERSION` 2.0.0):

| Field | Value |
|---|---|
| `published_at` | raw `createdDateTime`, cast tz-aware UTC at the transformer boundary |
| `available_at` | `coalesce(published_at, ...)` — so the vendor stamp, labelled `vendor` |
| Vintage Policy | retained as a **counted, logged fallback** for rows lacking the field (expected 0) |

**Measured vendor behaviour, recorded as observation, not explained.** The lag
between `createdDateTime` and settlement-period start has two regimes: a median of
**~52 minutes in 2021-2023**, and **~24.7 hours in 2024-2026**. The change of regime
is a vendor fact; no Elexon document found states its cause. `TODO: verify`.
One row of 94,415 (2023-03-18 SP16) is stamped 3.9 minutes after period start, i.e.
**before its own period ends**; this codebase asserts no `event_time <= available_at`
invariant (`windfor` legitimately inverts it too), so it is vendor pass-through.

**Direction of change.** Against the retired 90-minute assumption this is **not**
uniformly conservative: 2021-2023 rows become visible **earlier**, 2024+ rows
**later**. It is the vendor's own record time, which is the point of preferring it.

**Residual, still open (`TODO: verify`).** Whether `createdDateTime` is the initial
run's record time or the record time of whichever run we happen to hold is
undocumented. Elexon's Insights docs do not state it. So a late settlement revision
of a pre-cutover period may still carry a stamp that understates when that *value*
became knowable — the revision-chain residual ADR-031 disclosed is narrowed by the
vendor stamp, not eliminated by it.

`price_derivation_code` `K` observed on 10 rows. Source of truth:
`docs/DECISION_LOG/ADR-031-vintage-policy-reconstruction.md` (status: proposed) and
`docs/available_at_stamp_fidelity.md`, both amended 2026-09-07.

**On-disk state (rebuilt 2026-09-07).** All **94,415** silver rows carry the vendor
stamp: `vintage_policy` = `vendor` on every row, policy-fallback count **0**,
`published_at` 0 nulls, `available_at == published_at` everywhere, `dataset_version`
2.0.0. Checked against bronze on the key `(settlement_date, settlement_period,
published_at)`: 87,990 distinct keys both sides, **0 missing either way, 0 price
mismatches**. The tree gained one file and 27 rows — settlement date 2026-09-06 SP1-27,
a partial trailing day whose bronze capture had never been transformed.
110 dates carry doubled captures (the APPEND_ONLY class), collapsed by the `_latest`
projection, which orders by `available_at DESC` and so now selects the later
`createdDateTime` — confirmed on all 85 doubled keys.

## Gold layer

Two gold artifacts consume this dataset:

**Name**: `gold_uk_imbalance_context`
**Type**: SQL view
**File**: `src/gridflow/gold/views/uk_imbalance_context.sql`
**Joins**: `silver_elexon_system_prices` LEFT JOIN `silver_neso_carbon_intensity` on `timestamp_utc`
**Adds**: NESO carbon intensity forecast/actual/index alongside system prices and imbalance volume; `run_type` was replaced by `price_derivation_code` in the SELECT (v0.17 P1.5 — live silver no longer emits `run_type`).
**Grain**: one row per `silver_elexon_system_prices` row — half-hourly settlement period **per vintage** (APPEND_ONLY per ADR-025; the view does not select latest vintage).

**Name**: `system_marginal_price`
**Type**: Polars gold builder (`SystemMarginalPriceBuilder`)
**File**: `src/gridflow/gold/system_marginal_price.py`
**Reads**: silver `elexon/system_prices` parquet via `scan_parquet_range`, then `select_latest_vintage` (one row per settlement period — the builder, unlike the view, DOES collapse vintages).
**Adds**: `spread` (buy − sell), `abs_imbalance`, `hour_of_day`, `day_of_week` (ISO, 1=Mon..7=Sun — differs by one from `gridflow_models`' Python `weekday()` convention; pinned by `test_day_of_week_convention_iso`).
**Grain**: one row per settlement period (latest vintage).

Full column contracts: see the Gold layer contracts section of
[data-contracts.md](../../../10-projects/gridflow/data-contracts.md).

---

## Known issues and gotchas

- **Settlement runs**: on endpoints that send `settlementRunType`, the same `(settlement_date, settlement_period)` reappears with different `run_type` (II → SF → R1 → R2 → R3 → RF → DF) as reconciliation progresses. The transformer keeps every capture (`APPEND_ONLY`, `system_prices.py:65-66`); the `_latest` view selects the newest `available_at` per key, and on this endpoint `run_type` is null, so no run ranking applies. For point-in-time queries, filter the base view on `published_at`.
- **Settlement period range 1..50** — DST days (46 spring, 50 autumn) handled by `utils/time.settlement_period_to_utc`.

---

## Implementation delta

- **Path**: docs require `{settlementDate}` in path (`/balancing/settlement/system-prices/{settlementDate}`); code declares `path = "/balancing/settlement/system-prices"` and the date is appended in `_fetch_date_path()` — equivalent at request time, but the registry path string is doc-shape-incomplete. Cosmetic.
- **`priceDerivationCode` vs `run_type` mismapping — RESOLVED in V2 (2026-05-09).** Pre-V2 the silver renamed `priceDerivationCode` → `run_type` and the Pydantic regex `^(II|SF|R[1-3]|RF|DF)$` rejected the live values `N` / `P`. V2-FIX-04: silver now maps `priceDerivationCode` → `price_derivation_code` (a separate column with no regex constraint), and the schema's `run_type` is `Optional[str]` because this endpoint exposes no run-type field. Confirmed live 2026-05-09: 48 rows from `/balancing/settlement/system-prices/2026-05-06` round-trip through `ElexonSystemPrice` with 0 errors. See gridflow commit `fix(V2-C):`.

---

## Changelog

- **2026-05-09 — V2-FIX-04.** Silver maps `priceDerivationCode` to dedicated `price_derivation_code` column. Schema `run_type` made `Optional[str]` (this endpoint doesn't surface BSC run type). New schema field `price_derivation_code: str | None`. Regression tests in `tests/unit/test_schemas.py` and `tests/unit/test_silver_transforms.py`.
- **2026-05-08 — V1.** Live-validated; `priceDerivationCode = "N"` regex-mismatch surfaced.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/system_prices.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- [Gold view](../../../../../../Python/gridflow/src/gridflow/gold/views/uk_imbalance_context.sql) · [Gold builder](../../../../../../Python/gridflow/src/gridflow/gold/system_marginal_price.py)
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
