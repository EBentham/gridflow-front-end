---
source: elexon
dataset_key: market_depth
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Settlement market depth
  summary: >-
    Great Britain's balancing volumes for each half-hour settlement period: offer and bid volumes,
    accepted and priced accepted volumes, and indicated imbalance.
  facts:
    vendor: Elexon BMRS, settlement market-depth endpoint
    cadence: Half-hourly settlement periods
    grain: One row per settlement period, from the latest response
  landscape: market
  what_it_is: >-
    Elexon's summary of each GB settlement period's balancing volumes: offer and bid volumes, total
    accepted offer and bid volumes, and priced accepted offer and bid volumes, in MWh by gridflow's
    schema, plus the indicated imbalance. The response's metadata lists four datasets: IMBALNGC,
    BOD, DISEBSP and DISPTAV. Where `system_prices` gives each period's price, this gives its volumes.
  how_used:
    - Reading an imbalance price beside how much was accepted each way.
    - Features for an imbalance price or net imbalance volume forecast.
    - Tracking accepted balancing volume per half-hour, offers and bids apart.
  chart:
    type: line
    silver: elexon/market_depth
    time: timestamp_utc
    value: total_accepted_offer_volume_mwh
    filter:
      - {column: settlement_date, op: ge, value: "2026-09-16"}
      - {column: settlement_date, op: le, value: "2026-09-22"}
    aggregation: last
    window: {start: "2026-09-15", end: "2026-09-22"}
    unit: MWh
  chart_view:
    title: Accepted offer volume, 16 to 22 September 2026
    caption: >-
      Silver `elexon/market_depth`, MWh, one value per half-hour of settlement dates 16 to 22
      September 2026: the total accepted offer volume as sent. Accepted bids, in
      `total_accepted_bid_volume_mwh`, are negative in this window and not drawn.
    alt: >-
      Line chart of the total accepted offer volume from elexon/market_depth, in MWh, for every
      half-hour of settlement dates 16 to 22 September 2026. It runs from 441 to 2,818 on the 16th,
      stays between 1,278 and 3,753 from the 17th to the 19th (peak at 17:30 UTC on the 19th),
      ranges from 2,841 early on the 20th to 239 at its end, then stays between 211 and 1,362 on the
      21st and between 0 and 724 on the 22nd.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: total_accepted_offer_volume_mwh, label: Accepted offers, paint: petrol, note: "Accepted bids, in the same table, are below zero in this window; the notebook plots both."}
  raw_feed:
    note: >-
      One call per settlement date. The most recently fetched response wins each period; a
      same-day request returned null volumes for the day's later periods (seen on 1 September 2026).
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/market-depth/2026-09-20?page=1"
    commands:
      - {run: gridflow ingest elexon market_depth --start 2026-09-16 --end 2026-09-22, comment: "bronze; the end date is fetched"}
      - {run: gridflow transform elexon market_depth --start 2026-09-16 --end 2026-09-22, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-20"}
        - {column: settlement_period, op: ge, value: 26}
        - {column: settlement_period, op: le, value: 33}
      order_by: [settlement_period]
    key: [settlement_date, settlement_period]
    caption: "Settlement date 2026-09-20, periods 26 to 33, when accepted bids outweighed accepted offers."
    fields:
      settlement_date: GB settlement date, as Elexon labels it
      settlement_period: Half-hour of the settlement day, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: Start of the half-hour, computed from settlement date and period
      indicated_imbalance_mwh: "Indicated imbalance as sent; the column says MWh, gridflow's IMBALNGC schema says MW"
      offer_volume_mwh: "Offer volume, MWh, as sent (`offerVolume`)"
      bid_volume_mwh: "Bid volume, MWh, as sent (`bidVolume`); negative in these rows"
      total_accepted_offer_volume_mwh: "Total accepted offer volume, MWh, as sent; the charted column"
      total_accepted_bid_volume_mwh: "Total accepted bid volume, MWh, as sent; negative in these rows"
      priced_accepted_offers_volume_mwh: "Priced accepted offer volume, MWh, as sent (`pricedAcceptedOffersVolume`)"
      priced_accepted_bids_volume_mwh: "Priced accepted bid volume, MWh, as sent; zero in periods 26 and 33 here"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB view `silver_elexon_market_depth`, one row per
      settlement period, filtered on `settlement_date` with both ends included. Lineage columns are
      dropped and rows come ordered by `settlement_date` only.
    cells:
      - |
        df = data.elexon.query("market_depth", "2026-09-16", "2026-09-22")
        df = df.sort_values("timestamp_utc")
      - df[["settlement_date", "settlement_period", "total_accepted_offer_volume_mwh", "total_accepted_bid_volume_mwh"]].head()
      - |
        ax = df.plot(x="timestamp_utc",
                     y=["total_accepted_offer_volume_mwh", "total_accepted_bid_volume_mwh"],
                     ylabel="MWh", color=["#155A6E", "#C77E3C"], figsize=(8, 3.5))
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.3), ncols=2);
    needs: 16 to 22 September 2026
    plot_alt: >-
      Line plot of total_accepted_offer_volume_mwh (above zero) and total_accepted_bid_volume_mwh
      (below zero) against timestamp_utc, 16 to 22 September 2026. From the 17th to the 19th offers
      run between about 1,300 and 3,750 MWh and bids between about -1,750 and -4,234; both shrink
      towards zero from late on the 20th.
  related:
    - {dataset: elexon/system_prices, note: "Imbalance prices for the same settlement periods"}
    - {dataset: elexon/boal, note: "Acceptances unit by unit, where this table has one row per period"}
    - {dataset: elexon/imbalngc, note: "Indicated imbalance per period; this response's metadata lists IMBALNGC"}
    - {dataset: elexon/mid, note: "Traded market index price for the same settlement periods"}
---

# Elexon - Settlement Market Depth (`MARKET-DEPTH`)

## Overview

Settlement Market Depth — per settlement period summary of indicative imbalance, offer/bid volumes, and accepted balancing volumes. The response's `metadata.datasets` lists IMBALNGC, BOD, DISEBSP and DISPTAV (bronze `market_depth/2026/09/20`, fetched 2026-09-26; the bronze sample below shows the same list); it gives a single per-period snapshot useful for liquidity analytics.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/balancing/settlement/market-depth/{settlementDate}` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years (matches settlement records). |
| Publication lag  | Aligned with settlement run progression. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `settlementDate` | string | Yes | The settlement date for the filter. This must be in the format yyyy-MM-dd. | `2026-05-06` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/market-depth/2026-05-06?format=json" \
  -o "/tmp/elexon-market_depth.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/market_depth/<year>/<month>/<day>/raw_<fetched_at>_<sha256[:8]>.json` (`bronze/writer.py:33-34,57`)
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/market-depth/2026-05-06?format=json:

```json
{
  "metadata": {
    "datasets": [
      "IMBALNGC",
      "BOD",
      "DISEBSP",
      "DISPTAV"
    ]
  },
  "data": [
    {
      "settlementDate": "2026-05-06",
      "settlementPeriod": 1,
      "indicatedImbalance": 1122,
      "offerVolume": 60440.0,
      "bidVolume": -64830.0,
      "totalAcceptedOfferVolume": 578.0084677419355,
      "totalAcceptedBidVolume": -616.25,
      "pricedAcceptedOffersVolume": 0.0,
      "pricedAcceptedBidsVolume": -469.39166666666665
    },
    {
      "settlementDate": "2026-05-06",
      "settlementPeriod": 2,
      "indicatedImbalance": 656,
      "offerVolume": 60567.5,
      "bidVolume": -64840.0,
      "totalAcceptedOfferVolume": 605.8404121863799,
      "totalAcceptedBidVolume": -641.704550703696,
      "pricedAcceptedOffersVolume": 7.916666666666667,
      "pricedAcceptedBidsVolume": -531.5335829617604
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/market_depth/year=YYYY/month=MM/market_depth_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.market_depth.MarketDepthTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonMarketDepth` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, settlement_period)`
**Point-in-time field**: `ingested_at` (no native PIT field)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `indicated_imbalance_mwh` | `float` | Yes | `indicatedImbalance` | MWh by column name; unit unconfirmed: gridflow's `ElexonImbalNGC` gives IMBALNGC's indicated imbalance in MW (`schemas/elexon.py:338`). |
| `offer_volume_mwh` | `float` | Yes | `offerVolume` | MWh. |
| `bid_volume_mwh` | `float` | Yes | `bidVolume` | MWh. |
| `total_accepted_offer_volume_mwh` | `float` | Yes | `totalAcceptedOfferVolume` | MWh. |
| `total_accepted_bid_volume_mwh` | `float` | Yes | `totalAcceptedBidVolume` | MWh. |
| `priced_accepted_offers_volume_mwh` | `float` | Yes | `pricedAcceptedOffersVolume` | MWh. |
| `priced_accepted_bids_volume_mwh` | `float` | Yes | `pricedAcceptedBidsVolume` | MWh. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | Silver transform time, `datetime.now(UTC)` (`market_depth.py:115-120`). |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 1,
        "timestamp_utc": "2026-05-05T23:00:00+00:00",
        "indicated_imbalance_mwh": 1122,
        "offer_volume_mwh": 60440.0,
        "bid_volume_mwh": -64830.0,
        "total_accepted_offer_volume_mwh": 578.0084677419355,
        "total_accepted_bid_volume_mwh": -616.25,
        "priced_accepted_offers_volume_mwh": 0.0,
        "priced_accepted_bids_volume_mwh": -469.39166666666665,
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

- **Built from IMBALNGC/BOD/DISEBSP/DISPTAV** (the response's `metadata.datasets`) — don't double-count when joining with the underlying datasets.

---

## Implementation delta

- **Path**: same shape pattern as `system_prices` (date appended at request time).
- **Pydantic schema** `ElexonMarketDepth` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/market_depth.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
