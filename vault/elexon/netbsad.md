---
source: elexon
dataset_key: netbsad
vendor: Elexon BMRS
last_verified: 2026-05-21
layer_coverage: bronze, silver
v2_fix_history:
  - date: 2026-05-20
    phase: gridflow-G5-W1.1
    pr: https://github.com/EBentham/gridflow/pull/7
    change: silver transformer now emits 8 finer-grained adjustment columns
  - date: 2026-05-20
    phase: gridflow-G5-W4
    pr: https://github.com/EBentham/gridflow/pull/7
    change: ElexonNETBSAD Pydantic schema declared
page:
  title: Net balancing services adjustments
  summary: >-
    The system operator's net balancing services adjustments per GB settlement period, published
    by Elexon: cost, volume and price terms, buy and sell.
  facts:
    vendor: Elexon BMRS, dataset NETBSAD
    cadence: Half-hourly, by settlement period
    grain: One row per settlement period
  landscape: market
  what_it_is: >-
    One row per GB settlement period with, for buy and sell, a net cost adjustment, two net
    volume adjustments (energy, system) and a price adjustment. Per Elexon, the buy price price
    adjustment (BPA, £/MWh) is added to the system buy price when the system is short, the SPA
    to the sell price when long. DISBSAD lists the individual actions.
  how_used:
    - Checking whether a period's imbalance price carries a BPA or SPA adder.
    - Rebuilding system buy and sell prices from the balancing actions behind them.
  chart:
    type: line
    silver: elexon/netbsad
    time: timestamp_utc
    value: buy_price_price_adjustment
    filter:
      - {column: settlement_date, op: ge, value: "2026-09-15"}
      - {column: settlement_date, op: le, value: "2026-09-21"}
    dedup: {"on": [settlement_date, settlement_period], order_by: ingested_at}
    aggregation: last
    window: {start: "2026-09-14", end: "2026-09-21"}
    unit: £/MWh
  chart_view:
    title: Buy price price adjustment, 15 to 21 September 2026
    caption: >-
      Silver `elexon/netbsad`, £/MWh, one value per half-hour of settlement dates 15 to 21
      September 2026: the buy price price adjustment (BPA), each period counted once. It is 0 in
      every period, as are the other seven terms.
    alt: >-
      Line chart of the buy price price adjustment from elexon/netbsad, in £/MWh, for every
      half-hour of settlement dates 15 to 21 September 2026. The line lies flat at 0 for the
      whole week, with no rise or dip anywhere.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: buy_price_price_adjustment, label: Buy price adjustment, codes: BPA, paint: petrol, note: "0 in every period here, as are the SPA and the six cost and volume terms."}
  raw_feed:
    note: >-
      From the Elexon Insights API in 24-hour `from`/`to` windows from midnight UTC. Replies here
      also carry the half-hour starting at `to`, so silver repeats it.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/NETBSAD?from=2026-09-20T00:00:00Z&to=2026-09-21T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon netbsad --start 2026-09-14 --end 2026-09-22, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon netbsad --start 2026-09-14 --end 2026-09-21, comment: "starts early: dates begin 23:00 UTC"}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-21"}
        - {column: settlement_period, op: ge, value: 33}
        - {column: settlement_period, op: le, value: 40}
      dedup: {"on": [settlement_date, settlement_period], order_by: ingested_at}
      order_by: [settlement_period]
    key: [settlement_date, settlement_period]
    caption: "Settlement date 2026-09-21, periods 33 to 40: all eight adjustment terms are 0 in each."
    fields:
      settlement_date: GB settlement date, as Elexon labels it
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: Start of the half-hour, computed from settlement date and period
      net_buy_price_cost_adjustment_energy: "Net buy price cost adjustment (energy), from `netBuyPriceCostAdjustmentEnergy`"
      net_buy_price_volume_adjustment_energy: "Net buy price volume adjustment (energy), from `netBuyPriceVolumeAdjustmentEnergy`"
      net_buy_price_volume_adjustment_system: "Net buy price volume adjustment (system), from `netBuyPriceVolumeAdjustmentSystem`"
      buy_price_price_adjustment: "BPA, £/MWh; Elexon adds it to the buy price when the system is short"
      net_sell_price_cost_adjustment_energy: "Net sell price cost adjustment (energy), from `netSellPriceCostAdjustmentEnergy`"
      net_sell_price_volume_adjustment_energy: "Net sell price volume adjustment (energy), from `netSellPriceVolumeAdjustmentEnergy`"
      net_sell_price_volume_adjustment_system: "Net sell price volume adjustment (system), from `netSellPriceVolumeAdjustmentSystem`"
      sell_price_price_adjustment: "SPA, £/MWh; Elexon adds it to the sell price when the system is long"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_netbsad`, filtered on
      `settlement_date` with both ends included. Lineage columns are dropped; the midnight
      half-hour can come twice, so drop repeats on the key.
    cells:
      - |
        df = data.elexon.query("netbsad", "2026-09-15", "2026-09-21")
        key = ["settlement_date", "settlement_period"]
        df = df.drop_duplicates(key).sort_values("timestamp_utc")
      - df[key + ["buy_price_price_adjustment", "sell_price_price_adjustment"]].head()
      - (df.filter(like="adjustment") != 0).sum()
      - |
        df.plot(x="timestamp_utc", y=["buy_price_price_adjustment", "sell_price_price_adjustment"],
                ylabel="£/MWh", color=["#155A6E", "#8A6D3B"], figsize=(8, 3.5))
    needs: 14 to 21 September 2026
    plot_alt: >-
      Line plot of buy_price_price_adjustment and sell_price_price_adjustment against
      timestamp_utc, 15 to 21 September 2026: both lie flat at 0 £/MWh for the whole week, one
      on top of the other.
  related:
    - {dataset: elexon/disbsad, note: "The individual adjustment actions, one row each, per period"}
    - {dataset: elexon/system_prices, note: "The prices BPA and SPA adjust; its net imbalance picks which"}
    - {dataset: elexon/boal, note: "Balancing Mechanism acceptances, the other actions behind the price"}
    - {dataset: elexon/market_depth, note: "Accepted bid and offer volumes for the same settlement periods"}
---

# Elexon - Net Balancing Services Adjustment Data (`NETBSAD`)

## Overview

Net Balancing Services Adjustment Data (NETBSAD) — net price-adjustment and volume-adjustment terms applied to BSP/SSP so the cash-out prices reflect the cost of balancing services other than energy actions in BOALF. Elexon's guidance splits BSAD into two components, the individual Balancing Services Adjustment Actions ("disaggregated BSAD", the DISBSAD dataset) and the Buy/Sell Price Price Adjustment (BPA/SPA); no vendor text found says NETBSAD is computed from DISBSAD (checked 2026-09-29).

### Vendor documentation (quoted 2026-09-29)

- Elexon, *Imbalance Pricing Guidance*, v15.0, 25 June 2020 (https://www.elexon.co.uk/bsc/documents/training-guidance/bscguidance-notes/imbalance-pricing/), p. 11: "BSAD is split into two components: Balancing Services Adjustment Actions (BSAA); and Buy Price Price Adjustment (BPA)/Sell Price Price Adjustment (SPA)." "The BPA is added when the net imbalance of the Transmission System is short. The SPA is added when the net imbalance of the Transmission System is long." "It does not have a volume. It simply adjusts the volume-weighted average price."
- Same, p. 29: "The BPA is used when the Transmission System is short (and the NIV is positive), and the SPA is used when the Transmission System is long (and the NIV is negative)." Worked example: "System Buy Price = 30 + 6.50 = £36.50/MWh" with a BPA of £6.50/MWh.
- Elexon glossary, Buy Price Price Adjustment (https://www.elexon.co.uk/glossary/buy-price-price-adjustment/): "The amount sent by the Transmission Company ... as part of Balancing Services Adjustment Data (BSAD), as the 'Buy Price Price Adjustment'."
- Elexon glossary, Buy Price Volume Adjustment (Energy) (https://www.elexon.co.uk/bsc/glossary/buy-price-volume-adjustment-energy/): EBVA is "The amount sent by the Transmission Company as the 'Net Buy Price Volume Adjustment (Energy)'"; EBVA = max(aggregated volume of relevant Balancing Services purchased for energy balancing less that sold, 0).
- Units of the six net cost and volume terms, and their sign conventions, are not stated in the sources above.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/NETBSAD` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Same cadence as system prices. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `from` | string | Yes | The "from" start time or settlement date for the filter. | `2026-05-06T00:00Z` |
| `to` | string | Yes | The "to" start time or settlement date for the filter. | `2026-05-06T03:00Z` |
| `settlementPeriodFrom` | integer | No | The "from" settlement period for the filter. This should be an integer from 1-50 inclusive. | `1` |
| `settlementPeriodTo` | integer | No | The "to" settlement period for the filter. This should be an integer from 1-50 inclusive. | `48` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/NETBSAD?from=2026-05-06T00:00Z&to=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-netbsad.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/netbsad/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/NETBSAD?from=2026-05-06T00:00Z&to=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "NETBSAD",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 9,
      "netBuyPriceCostAdjustmentEnergy": 0.0,
      "netBuyPriceVolumeAdjustmentEnergy": 0.0,
      "netBuyPriceVolumeAdjustmentSystem": 0.0,
      "buyPricePriceAdjustment": 0.0,
      "netSellPriceCostAdjustmentEnergy": 0.0,
      "netSellPriceVolumeAdjustmentEnergy": 0.0,
      "netSellPriceVolumeAdjustmentSystem": 0.0,
      "sellPricePriceAdjustment": 0.0
    },
    {
      "dataset": "NETBSAD",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 8,
      "netBuyPriceCostAdjustmentEnergy": 0.0,
      "netBuyPriceVolumeAdjustmentEnergy": 0.0,
      "netBuyPriceVolumeAdjustmentSystem": 0.0,
      "buyPricePriceAdjustment": 0.0,
      "netSellPriceCostAdjustmentEnergy": 0.0,
      "netSellPriceVolumeAdjustmentEnergy": 0.0,
      "netSellPriceVolumeAdjustmentSystem": 0.0,
      "sellPricePriceAdjustment": 0.0
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/netbsad/year=YYYY/month=MM/netbsad_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.netbsad.NETBSADTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonNETBSAD` (added 2026-05-20, gridflow G5-W4).
**Dedup key**: `(settlement_date, settlement_period)`
**Point-in-time field**: `ingested_at` (no native PIT field)

### Silver schema

The transformer keeps only the columns present in the bronze it reads
(`netbsad.py:167`, `available = [c for c in output_cols if c in df.columns]`):
legacy bronze yields the legacy 4, current bronze the current 8. Silver built
from current bronze carries only the 8; the legacy 4 are absent, not null
(checked 2026-09-29). Schema declarations mark all 12 as `Optional`.

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `net_buy_price_adjustment` | `float` | Yes | `netBuyPriceAdjustment` | _Legacy (pre-2026 bronze)._ GBP/MWh adjustment to BSP. |
| `net_sell_price_adjustment` | `float` | Yes | `netSellPriceAdjustment` | _Legacy (pre-2026 bronze)._ GBP/MWh adjustment to SSP. |
| `net_buy_volume_adjustment` | `float` | Yes | `netBuyVolumeAdjustment` | _Legacy (pre-2026 bronze)._ MWh. |
| `net_sell_volume_adjustment` | `float` | Yes | `netSellVolumeAdjustment` | _Legacy (pre-2026 bronze)._ MWh. |
| `net_buy_price_cost_adjustment_energy` | `float` | Yes | `netBuyPriceCostAdjustmentEnergy` | Cost adjustment to net buy price, energy axis. |
| `net_buy_price_volume_adjustment_energy` | `float` | Yes | `netBuyPriceVolumeAdjustmentEnergy` | Volume adjustment to net buy price, energy axis. |
| `net_buy_price_volume_adjustment_system` | `float` | Yes | `netBuyPriceVolumeAdjustmentSystem` | Volume adjustment to net buy price, system axis. |
| `buy_price_price_adjustment` | `float` | Yes | `buyPricePriceAdjustment` | Price-on-price adjustment to net buy price. |
| `net_sell_price_cost_adjustment_energy` | `float` | Yes | `netSellPriceCostAdjustmentEnergy` | Cost adjustment to net sell price, energy axis. |
| `net_sell_price_volume_adjustment_energy` | `float` | Yes | `netSellPriceVolumeAdjustmentEnergy` | Volume adjustment to net sell price, energy axis. |
| `net_sell_price_volume_adjustment_system` | `float` | Yes | `netSellPriceVolumeAdjustmentSystem` | Volume adjustment to net sell price, system axis. |
| `sell_price_price_adjustment` | `float` | Yes | `sellPricePriceAdjustment` | Price-on-price adjustment to net sell price. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | Silver transform time (`netbsad.py:138-142`, `datetime.now(UTC)`), not bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-09-21",
        "settlement_period": 33,
        "timestamp_utc": "2026-09-21T15:00:00+00:00",
        "net_buy_price_cost_adjustment_energy": 0.0,
        "net_buy_price_volume_adjustment_energy": 0.0,
        "net_buy_price_volume_adjustment_system": 0.0,
        "buy_price_price_adjustment": 0.0,
        "net_sell_price_cost_adjustment_energy": 0.0,
        "net_sell_price_volume_adjustment_energy": 0.0,
        "net_sell_price_volume_adjustment_system": 0.0,
        "sell_price_price_adjustment": 0.0,
        "data_provider": "elexon",
        "ingested_at": "2026-09-26T18:30:06.000739+00:00"
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Relation to DISBSAD is not "computed from"**: Elexon's guidance treats the disaggregated actions (DISBSAD) and the BPA/SPA as the two parts of BSAD (see Vendor documentation above); no vendor text found says NETBSAD sums DISBSAD.
- **Boundary half-hour repeats across partitions**: the connector requests `from=D 00:00Z` to `to=D+1 00:00Z` (`endpoints.py` `netbsad`, `client.py` `_fetch_datetime_range`), and every reply on disk (checked 2026-09-29) also carries the period starting at `to`, so the 00:00 UTC half-hour lands in two silver partitions. `netbsad` is in `PUBLICATION_WINDOW_EXEMPT` (`_publication_window.py:61`), so nothing trims it; readers of `silver_elexon_netbsad` must dedup on `(settlement_date, settlement_period)`.
- **All zero in the captured window**: every one of the eight terms is `0.00` in every bronze record on disk (2026-08-01 to 2026-09-22, checked 2026-09-29). The vendor sends the zeros; this is not a parse fault. In the same settlement periods, silver `disbsad` carries non-zero action volumes (Energy -450 to 772.85 MWh, System -600 to 750 MWh summed per period, 674 shared periods, checked 2026-09-29). Cause not established; do not read NETBSAD as a sum of DISBSAD.

---

## Implementation delta

- **Param style**: docs require `from`/`to`; code matches.
- **Pydantic schema declared** as of gridflow G5-W4 (2026-05-20):
  `ElexonNETBSAD` in `schemas/elexon.py`.

### V2-FIX changelog

- **2026-05-20 — gridflow G5-W1.1 (PR #7)**: live Elexon API now returns 8
  finer-grained adjustment columns (cost vs volume × energy vs system × buy
  vs sell) rather than the legacy 4. Silver transformer extended to rename
  both shapes; pre-G5 silver carried `null` on every adjustment column
  because the live bronze didn't match the original rename map (W1.1 was a
  P1 silent-null bug). Pre-2026 bronze still produces the legacy 4.
- **2026-05-20 — gridflow G5-W4 (PR #7)**: `ElexonNETBSAD` Pydantic class
  added to `schemas/elexon.py` — declares all 12 adjustment columns +
  bitemporal fields. Parametrised acceptance test in
  `tests/contracts/test_elexon_schema_alignment.py` pins schema-vs-
  transformer alignment.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/netbsad.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
