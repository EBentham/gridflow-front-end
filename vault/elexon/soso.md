---
source: elexon
dataset_key: soso
vendor: Elexon BMRS
last_verified: 2026-05-09
layer_coverage: bronze, silver
page:
  title: SO-SO interconnector prices
  summary: >-
    Elexon's system operator to system operator (SO-SO) prices for trades across GB
    interconnectors: one row per contract, with direction, MW and price.
  facts:
    vendor: Elexon BMRS, dataset SOSO
    cadence: No cadence stated by Elexon; contracts here start on the hour
    grain: One row per settlement date, contract id and direction
  landscape: market
  what_it_is: >-
    Per Elexon, Britain's system operator and the transmission system operators it connects to by
    interconnector provide SO-SO services to each other, to adjust flows closer to real time. Each
    row is one contract: a trader unit, a direction sent as `Bid` or `Offer`, a quantity in MW and
    a price Elexon labels in £. Elexon's docs define neither direction.
  how_used:
    - Each trader unit's Bid and Offer prices per start hour, against GB imbalance prices.
    - Features for a model of interconnector flows adjusted close to real time.
    - Comparing prices under different trader units for the same start hour.
  chart:
    type: line
    silver: elexon/soso
    time: timestamp_utc
    value: trade_price
    filter:
      - {column: trader_unit, op: eq, value: EWIC_EG}
      - {column: settlement_date, op: ge, value: "2026-09-14"}
      - {column: settlement_date, op: le, value: "2026-09-18"}
    group: trade_direction
    group_map:
      Bid: bid
      Offer: offer
    series_order: [bid, offer]
    aggregation: mean
    window: {start: "2026-09-13", end: "2026-09-18"}
    unit: "£"
  chart_view:
    title: EWIC_EG prices, 14 to 18 September 2026
    caption: >-
      Silver `elexon/soso`, £ as Elexon labels it, trader unit `EWIC_EG`, settlement dates 14 to
      18 September 2026: the mean of each start hour's eight 25 MW `Bid` contracts, and of its eight
      `Offer` contracts. `GL1_EG` carries the same prices here.
    alt: >-
      Line chart of the mean EWIC_EG Bid and Offer prices from elexon/soso, in £, for every start
      hour of settlement dates 14 to 18 September 2026. Both move in steps that repeat each day.
      The Bid mean is 345 to 367 from 22:00 to 04:00 UTC, 769.6 from 04:00 to 10:00 UTC and about
      476 from 10:00 to 22:00 UTC. The Offer mean stays below zero: -0.045 from 22:00 to 04:00 UTC,
      then -29.1 on the 14th, 17th and 18th and about -58.7 on the 15th and 16th.
    x_label: settlement date; each starts at 23:00 UTC
    key:
      - {series: bid, label: Bid price, codes: Bid, paint: petrol, note: "Mean over the hour's Bid contracts; 769.6 from 04:00 to 10:00 UTC each day."}
      - {series: offer, label: Offer price, codes: Offer, paint: clay, note: "Mean over the hour's Offer contracts; below zero in every hour shown."}
  raw_feed:
    note: >-
      Elexon Insights API, 23-hour publish windows (Elexon allows 24); bronze is filed by window
      start day. September settlement dates start 23:00 UTC, so commands begin a day early.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/SOSO?publishDateTimeFrom=2026-09-14T22:00:00Z&publishDateTimeTo=2026-09-15T21:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon soso --start 2026-09-13 --end 2026-09-19, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon soso --start 2026-09-13 --end 2026-09-18, comment: "bronze to silver, by publish window"}
  record:
    select:
      filter:
        - {column: start_time, op: eq, value: "2026-09-15T12:00:00"}
        - column: contract_identification
          op: in
          value: [EG_20260915_1200_1, EG_20260915_1200_9, GL_20260915_1200_1, GL_20260915_1200_9, SO_20260915_1200_1, SO_20260915_1200_9, NG_20260915_1200_17, NG_20260915_1200_25]
      order_by: [trader_unit, trade_direction]
      columns: [trader_unit, trade_price, trade_direction, contract_identification, settlement_date, trade_quantity_mw]
    key: [settlement_date, contract_identification, trade_direction]
    caption: "Start 2026-09-15 12:00 UTC: one Bid and one Offer from each of four trader units."
    fields:
      trader_unit: "Trader unit code, as sent (`traderUnit`)"
      trade_price: "Price as sent (`tradePrice`); Elexon labels it in £ and says no more"
      trade_direction: "`Bid` or `Offer`, as sent; Elexon's docs define neither"
      contract_identification: "Contract id as sent; here a prefix, the date, the start hour, a number"
      settlement_date: "Settlement date, the vendor's `settlementDate` as sent"
      trade_quantity_mw: "Quantity in MW, as Elexon labels it (`tradeQuantity`)"
      timestamp_utc: "Contract start, copied from `start_time`: the feed sends no settlement period"
      sender_identification: "Sender party code, as sent (`senderIdentification`)"
      receiver_identification: "Receiver party code, as sent (`receiverIdentification`)"
      resource_provider: "Resource provider code, as sent (`resourceProvider`)"
      start_time: "Contract start, UTC, as sent (`startTime`)"
      end_time: "Null: the vendor's `endTime` carries no `Z`, so the parse fails"
      published_at: "Vendor publish time (`publishTime`); silver is filed by publish window"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_soso`, filtered on
      `settlement_date` with both ends included. Lineage columns are dropped and rows come ordered
      by `settlement_date` only.
    cells:
      - |
        df = data.elexon.query("soso", "2026-09-14", "2026-09-18")
        df = df.sort_values(["timestamp_utc", "trader_unit", "contract_identification"])
      - df[["trade_direction", "trade_price"]].head()
      - |
        ewic = df[df.trader_unit == "EWIC_EG"]
        wide = ewic.pivot_table(
            index="timestamp_utc", columns="trade_direction",
            values="trade_price", aggfunc="mean")
        ax = wide[["Bid", "Offer"]].plot(
            ylabel="£", color=["#155A6E", "#C77E3C"],
            ylim=(-100, 1000), figsize=(8, 3.5))
        ax.legend(ncols=2, loc="upper left");
    needs: 13 to 18 September 2026
    plot_alt: >-
      Line plot of the hourly mean Bid and Offer trade_price for EWIC_EG against timestamp_utc, 14
      to 18 September 2026. Bid steps each day from about 360 to 770 for six hours from 04:00 UTC,
      then about 476 until 22:00 UTC. Offer stays just below zero overnight and falls to about -29
      or -59 for the rest of the day.
  related:
    - {dataset: elexon/fuelhh, note: "Metered interconnector flows per half-hour, one signed code per link"}
    - {dataset: elexon/system_prices, note: "The GB imbalance price for the same hours"}
    - {dataset: elexon/boal, note: "Accepted Balancing Mechanism bids and offers for the same hours"}
    - {dataset: elexon/mid, note: "The traded GB market index price for the same hours"}
---

# Elexon - SO-SO Prices (Cross-Border Interconnector Trading) (`SOSO`)

## Overview

SO-SO prices — the prices and volumes traded between transmission system operators across GB interconnectors (Moyle, IFA, IFA2, BritNed, NSL, ElecLink, NEMO, Greenlink, Eleclink, Viking). SOSO is the canonical interconnector-trading reference series.

Vendor wording (read 2026-09-29). The API reference for `/datasets/SOSO` (https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/SOSO): "This endpoint provides system operator to system operator prices data, filtered by publish time. This API endpoint has a maximum range of 24 hours." It defines no response field; its example shows `tradeDirection` as `A02`, while the feed sends `Bid` or `Offer`. Elexon's Insights page "SO-SO trade prices" (https://bmrs.elexon.co.uk/soso-trade-prices): "System operator to system operator (SO-SO) services are provided mutually with other transmission system operators connected to Britain's transmission system via interconnectors", used when "the system operator needs to adjust these interconnector flows closer to real time"; its table heads are "Trade Quantity (MW)" and "Trade Price (£)". Neither page says which side `Bid` and `Offer` are.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/SOSO` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Day-ahead and as trades are agreed. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | Yes | As per Elexon Swagger spec for soso. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | Yes | As per Elexon Swagger spec for soso. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/SOSO?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-07T00:00Z&format=json" \
  -o "/tmp/elexon-soso.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/soso/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/SOSO?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-07T00:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "SOSO",
      "publishTime": "2026-05-06T23:03:10Z",
      "senderIdentification": "10X1001A1001A515",
      "receiverIdentification": "10X1001A1001A59Q",
      "contractIdentification": "NG_20260507_0100_32",
      "resourceProvider": "10X1001A1001A515",
      "tradeDirection": "Bid",
      "tradeQuantity": 25.0,
      "tradePrice": 120.27,
      "traderUnit": "EWIC_NG",
      "startTime": "2026-05-07T01:00:00Z",
      "endTime": "2026-05-07T02:00:00",
      "settlementDate": "2026-05-07"
    },
    {
      "dataset": "SOSO",
      "publishTime": "2026-05-06T23:03:10Z",
      "senderIdentification": "10X1001A1001A515",
      "receiverIdentification": "10X1001A1001A59Q",
      "contractIdentification": "NG_20260507_0100_31",
      "resourceProvider": "10X1001A1001A515",
      "tradeDirection": "Bid",
      "tradeQuantity": 25.0,
      "tradePrice": 114.27,
      "traderUnit": "EWIC_NG",
      "startTime": "2026-05-07T01:00:00Z",
      "endTime": "2026-05-07T02:00:00",
      "settlementDate": "2026-05-07"
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/soso/year=YYYY/month=MM/soso_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.soso.SOSOTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonSOSO` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `settlement_date`, `contract_identification`, `trade_direction` (keep last; `silver/elexon/soso.py:141-144`)
**Point-in-time field**: `published_at`, the vendor's `publishTime` (`silver/elexon/soso.py:127-139`); silver files are publish windows, not settlement days (ADR-026)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Copied from `startTime`: the feed sends no `settlementPeriod`, so the transformer's `start_time` branch applies and `settlement_period` never reaches silver (`silver/elexon/soso.py:90-108`, `:172`). |
| `contract_identification` | `str` | No | `contractIdentification` | SOSO contract MRID. |
| `sender_identification` | `str` | Yes | `senderIdentification` | Sender TSO identifier. |
| `receiver_identification` | `str` | Yes | `receiverIdentification` | Receiver TSO identifier. |
| `resource_provider` | `str` | Yes | `resourceProvider` | Resource provider. |
| `trade_direction` | `str` | Yes | `tradeDirection` | `Bid` or `Offer` as sent; Elexon does not define either side (see Overview). |
| `trade_quantity_mw` | `float` | Yes | `tradeQuantity` | MW (Elexon's "Trade Quantity (MW)"). |
| `trade_price` | `float` | Yes | `tradePrice` | Elexon labels it "Trade Price (£)"; no per-unit basis stated. |
| `trader_unit` | `str` | Yes | `traderUnit` | Trader unit identifier. |
| `start_time` | `datetime[UTC]` | Yes | `startTime` | Trade start time. |
| `end_time` | `datetime[UTC]` | Yes | `endTime` | Null: the vendor sends `endTime` with no `Z` (bronze sample above) and the parse format requires one, `strict=False` (`silver/elexon/soso.py:118-125`). |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Vendor publish time (`silver/elexon/soso.py:127-139`). |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | Silver transform time, `datetime.now(UTC)` (`silver/elexon/soso.py:146-150`). |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-07",
        "timestamp_utc": "2026-05-07T01:00:00+00:00",
        "contract_identification": "NG_20260507_0100_32",
        "sender_identification": "10X1001A1001A515",
        "receiver_identification": "10X1001A1001A59Q",
        "resource_provider": "10X1001A1001A515",
        "trade_direction": "Bid",
        "trade_quantity_mw": 25.0,
        "trade_price": 120.27,
        "trader_unit": "EWIC_NG",
        "start_time": "2026-05-07T01:00:00Z",
        "end_time": None,
        "published_at": "2026-05-06T23:03:10Z",
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

- **Max-1-day query window enforced** — see Implementation delta.
- **Per-interconnector**: the dataset covers all GB ICs; filter by `senderIdentification`/`receiverIdentification` in gold.

---

## Implementation delta

- **Vendor-enforced max 1-day query window — RESOLVED in V2 (2026-05-09).** `ENDPOINTS["soso"].max_chunk_hours = 23` matches the same fix applied to REMIT. Boundary re-verified live 2026-05-09: 23h request → HTTP 200, 25h request → HTTP 400. See gridflow commit `fix(V2-C):` and [remit.md](./remit.md#changelog).
- **Pydantic schema** `ElexonSOSO` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Changelog

- **2026-05-09 — V2-FIX-03.** `max_chunk_hours=23` (paired with REMIT). See [remit.md](./remit.md#changelog) for shared evidence.
- **2026-05-08 — V1.** Live-validated; vendor 1-day cap surfaced.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/soso.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
