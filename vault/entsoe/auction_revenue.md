---
source: entsoe
dataset_key: auction_revenue
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Explicit auction revenue by border
  summary: >-
    TSO revenue from daily explicit capacity auctions on GB's borders with the Netherlands and
    Belgium, in EUR per hour, published by ENTSO-E.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A25, business type B07
    cadence: Hourly (`PT60M`) points in the responses gridflow holds
    grain: One row per hour and zone pair per file; most hours in two files
  landscape: market
  what_it_is: >-
    Revenue from explicit capacity auctions on a border (Article 12.1.A), as ENTSO-E publishes
    it, in EUR as sent in `currency_Unit.name`. gridflow pins `contract_MarketAgreement.Type` A01,
    the daily auction, so every row is the daily product and a delivery day's hours can be summed.
    Rows keep the ordered pair as sent; which direction an amount covers is not stated.
  how_used:
    - Hourly auction value of GB's links to the Netherlands and Belgium.
    - Set against `total_capacity_allocated` for an implied price in EUR per MW.
    - A congestion-rent feature beside the GB to continent price spread.
  chart:
    type: line
    silver: entsoe/auction_revenue
    time: timestamp_utc
    value: amount_eur
    filter:
      - {column: timestamp_utc, op: ge, value: "2026-09-14T22:00:00Z"}
      - {column: timestamp_utc, op: lt, value: "2026-09-21T22:00:00Z"}
      - {column: in_area_code, op: eq, value: "10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA"}
    dedup: {on: [timestamp_utc, in_area_code, out_area_code], order_by: published_at}
    group: out_area_code
    group_map:
      "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL": netherlands
      "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2": belgium
    series_order: [netherlands, belgium]
    aggregation: last
    window: {start: "2026-09-14", end: "2026-09-21"}
    unit: EUR
  chart_view:
    title: Auction revenue, GB-NL and GB-BE, 15 to 21 September 2026
    caption: >-
      Silver `entsoe/auction_revenue`, EUR per hour as sent, both borders with `in_area_code` GB,
      delivery days 15 to 21 September 2026 (22:00 to 22:00 UTC). Most hours sit in two silver
      files; one copy is kept, nothing summed.
    alt: >-
      Line chart of hourly auction revenue in EUR from entsoe/auction_revenue for GB with the
      Netherlands and GB with Belgium, delivery days 15 to 21 September 2026. The Netherlands line
      is zero until 22:00 UTC on 19 September, reaches 14,712 EUR on the 20th and peaks at 115,434
      EUR at 11:00 UTC on the 21st. Belgium peaks at 11:00 UTC: 81,198 EUR on the 15th, 78,442 on
      the 16th and 13,210 on the 18th; it stays under 4,400 EUR on the other days.
    x_label: UTC date; delivery days start 22:00 UTC
    key:
      - {series: netherlands, label: GB and Netherlands, codes: "out_Domain NL", paint: petrol, note: "Zero every hour of delivery days 15 to 19: one zero point a day, repeated (A03)."}
      - {series: belgium, label: GB and Belgium, codes: "out_Domain BE", paint: horizon, note: "Highest at 11:00 UTC on 15 and 16 September; under 4,400 EUR from the 19th."}
  raw_feed:
    note: >-
      One GET per ordered pair per UTC day; a reply can span two delivery days. GB-NL and GB-BE
      carry a series; the other six answer "no matching data".
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A25&periodStart=202609200000&periodEnd=202609210000&in_Domain=10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA&out_Domain=10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL&businessType=B07&contract_MarketAgreement.Type=A01&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe auction_revenue --start 2026-09-14 --end 2026-09-21, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe auction_revenue --start 2026-09-14 --end 2026-09-20, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: ge, value: "2026-09-21T08:00:00Z"}
        - {column: timestamp_utc, op: le, value: "2026-09-21T11:00:00Z"}
      dedup: {on: [timestamp_utc, in_area_code, out_area_code], order_by: published_at}
      order_by: [timestamp_utc, out_area_code]
      columns: [timestamp_utc, in_area_code, out_area_code, amount_eur, resolution, published_at, business_type]
    key: [timestamp_utc, in_area_code, out_area_code, business_type]
    caption: "Both borders, 08:00 to 11:00 UTC on 21 September 2026, one copy of each hour."
    fields:
      timestamp_utc: "Hour start, UTC: period start plus (position minus 1) times resolution"
      in_area_code: "The `in_Domain` EIC as requested: GB on the GB-NL and GB-BE series"
      out_area_code: "The `out_Domain` EIC, the zone across the border"
      business_type: "`B07`, auction revenue, as the request asks and the series states"
      amount_eur: "EUR for the hour, from `price.amount`; an A03 point repeats until the next"
      resolution: "Point length as sent; `PT60M` in these rows"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, within seconds of gridflow's request"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_entsoe_auction_revenue`, filtered on `timestamp_utc`
      with both ends included. Lineage columns are dropped. Most hours arrive twice, once per silver
      file, so drop duplicates before summing.
    cells:
      - |
        df = data.entsoe.query("auction_revenue", "2026-09-14", "2026-09-21")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
        key = ["timestamp_utc", "in_area_code", "out_area_code"]
        df = df.drop_duplicates(subset=key).sort_values(key)
      - df[["timestamp_utc", "in_area_code", "out_area_code", "amount_eur", "resolution"]].head(8)
      - |
        df["delivery_day"] = df["timestamp_utc"].dt.tz_convert("Europe/Brussels").dt.date.astype(str)
        df["border"] = "GB-" + df["out_area_code"].str[3:5]
        days = df[df["delivery_day"].between("2026-09-15", "2026-09-21")]
        daily = days.pivot_table(index="delivery_day", columns="border", values="amount_eur", aggfunc="sum")
        daily.plot.bar(ylabel="EUR per delivery day", color=["#3E8C97", "#155A6E"], figsize=(8, 3.5))
    needs: 14 to 20 September 2026
    plot_alt: >-
      Bar chart of amount_eur summed per delivery day (Brussels date) and border, 15 to 21 September
      2026. GB-BE: about 247,000 EUR on the 15th, 382,000 on the 16th, 51,000 on the 18th and under
      12,000 on the other days. GB-NL: zero from the 15th to the 19th, about 41,000 on the 20th and
      660,000 on the 21st.
  related:
    - {dataset: entsoe/total_capacity_allocated, note: "MW allocated on the same ordered pairs, hour by hour"}
    - {dataset: entsoe/cross_border_flows, note: "Physical flow on the same two borders, same pair orientation"}
    - {dataset: entsoe/day_ahead_prices, note: Prices on the continental side of each border}
    - {dataset: elexon/mid, note: "GB's market index price, the other side of the spread"}
---

# ENTSO-E — Auction Revenue (A25, businessType=B07)

## Overview

Revenue earned by TSOs from explicit cross-border capacity auctions, in EUR
per zone-pair and trading horizon. Article 12.1.A of Regulation (EC) 543/2013.
This is one of **four A25-document variants**, distinguished from the others
by `(businessType, auction.Type)` combinations. Used to build the
TSO-revenue side of congestion-cost models and to value capacity rights.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://web-api.tp.entsoe.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | Query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | 1 req/s default |
| Pagination       | None |
| Historical depth | 2014-12-05 onward |
| Publication lag  | After auction settlement |
| Response format  | XML |

### ENTSO-E parameter tuple (validation criterion)

| Field | Value |
|-------|-------|
| documentType | `A25` |
| processType | (none) |
| businessType | `B07` (auction revenue) |
| `contract_MarketAgreement.Type` | `A01` (daily) |
| domain-param-name | `in_Domain` + `out_Domain` (zone_pair) |

### Cross-zonal parameters

A25/B07 is directional. Use UK-centric border pairs from A11.

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | Yes | API key | UUID |
| `documentType` | str | Yes | `A25` | `A25` |
| `businessType` | str | Yes | `B07` | `B07` |
| `contract_MarketAgreement.Type` | str | Yes | `A01` | `A01` |
| `in_Domain` | str | Yes | Source EIC | `10YGB----------A` |
| `out_Domain` | str | Yes | Destination EIC | `10YFR-RTE------C` |
| `periodStart` / `periodEnd` | str | Yes | UTC | |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -o "/tmp/entsoe-auction_revenue.xml" \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A25&businessType=B07&contract_MarketAgreement.Type=A01&in_Domain=10YGB----------A&out_Domain=10YFR-RTE------C&periodStart=202605060000&periodEnd=202605070000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/auction_revenue/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per (ordered zone pair, UTC request day); a populated reply can span two CET delivery days (`client.py` `day_subwindows`; bronze 2026-08/09).

### Bronze sample

Live 2026-05-08: Acknowledgement, Reason 999 — `AUCTION_REVENUE [12.1.A]
(10YGB----------A, 10YFR-RTE------C)`. Retried 30-day window: still EMPTY.
Sanity NL→DE 30-day: also EMPTY. Populated payloads (bronze 2026-08-01 to 05 and
2026-09-13 to 21, e.g. `2026/09/20/raw_20260926T175330Z_005f5299.xml`): only the GB-NL and GB-BE
requests return a `Publication_MarketDocument`; the other six pairs return Reason 999. Each
series carries `auction.type` A02, `contract_MarketAgreement.type` A01, `currency_Unit.name` EUR,
`curveType` A03 and `PT60M` points under `price.amount`; `period.timeInterval` runs 22:00 to 22:00
UTC in these documents and a one-UTC-day request can return both delivery days it touches.

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/auction_revenue/year=YYYY/month=MM/auction_revenue_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h6_market.AuctionRevenueTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeTransmissionMarketAmount`
**Dedup key**: `(timestamp_utc, in_area_code, out_area_code, business_type)`
**Point-in-time field**: `none`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | period + position | |
| `in_area_code` | `str` | No | `in_Domain.mRID` | EIC |
| `out_area_code` | `str` | No | `out_Domain.mRID` | EIC |
| `amount_eur` | `float` | No | `Point.price.amount` | EUR per `currency_Unit.name`; the transformer drops the currency (`h6_market.py:130`, `:107`) |
| `business_type` | `str` | No | TS `businessType` | Default "" in canonical. `B07`. |
| `resolution` | `str` | No | `Period.resolution` | Default "" in canonical. |
| `published_at` | `datetime[UTC]` | Yes | document `createdDateTime` | Fetch-time stamp, within seconds of the request (`h6_market.py:105`) |
| `data_provider` | `str` | No | derived | `"entsoe"` |
| `ingested_at` | `datetime[UTC]` | Yes | derived | |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-09-21T11:00:00Z",
        "in_area_code": "10YGB----------A",
        "out_area_code": "10YNL----------L",
        "amount_eur": 115433.72,
        "business_type": "B07",
        "resolution": "PT60M",
        "published_at": "2026-09-26T17:53:44Z",
        "data_provider": "entsoe",
        "ingested_at": "2026-09-26T17:53:55.060361Z",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **EUR-amount, not MW.** Uses `EntsoeTransmissionMarketAmount` schema — the
  H6 transformer correctly switches to `amount_eur` via `_H6AmountTransformer`.
- Publication is sparse — many GB borders publish auction revenue weekly or
  monthly rather than per-day.
- **Each delivery hour lands in two silver partitions.** A UTC-day request returns both CET
  delivery days it touches, the class is EXEMPT from the event-window trim
  (`_event_window.py:210`), and the transformer dedups within one partition only
  (`h6_market.py:98`). The `silver_entsoe_auction_revenue` view is a plain parquet glob, so dedup on
  `(timestamp_utc, in_area_code, out_area_code)` before summing (silver, Aug and Sep 2026: 1,296 rows, 744 keys).
- **A03 curve.** ENTSO-E's curvetypes guide ("Introduction of different Timeseries possibilities
  (curvetypes) with ENTSO-E electronic documents", v1.4, §4.3): "only the position where a block
  change occurs is provided" and "The value of the Qty remains constant within each Block". The
  parser repeats the last declared point on each omitted position (`parsers.py:533-600`).

---

## Implementation delta

- **Tuple recorded:** `(documentType=A25, processType=none, businessType=B07, contract_MarketAgreement.Type=A01, domain=in_Domain+out_Domain)`. Matches code — the `auction_revenue` entry in `endpoints.py` `DOC_TYPES`.
- **Live validation 2026-05-08 GB→FR daily and 30-day:** Acknowledgement, Reason 999. Sanity NL→DE 30-day: also EMPTY. **EMPTY** — cause: "border has zero allocation in window" (auction-revenue publication cadence is sparser than daily; the test windows did not overlap a published settlement).
- **Disambiguation from other A25 variants** (critical because A25 multiplexes four datasets):
  - **`auction_revenue`** (this page): `businessType=B07`, `contract_MarketAgreement.Type=A01`, `domain_style=zone_pair` (cross-border revenue per border), unit EUR.
  - `transfer_capacity_use`: `businessType=B05` + `Auction.Category=A01` + `contract_MarketAgreement.Type=A01`, zone_pair, unit MW (capacity USE, not money).
  - `congestion_income`: `businessType=B10` + `contract_MarketAgreement.Type=A01`, zone_pair, unit EUR (income from implicit/flow-based allocation, not from explicit auctions).
  - `net_positions`: `businessType=B09` + `contract_MarketAgreement.Type=A01`, **`domain_style=zone`** (single zone, NOT zone_pair), unit MW (net implicit-auction position).

---

## Modelling notes

- Pair with `total_capacity_allocated` (A26/A29) to get implied
  EUR/MW for the auction product; useful for capacity-rights valuation.

---

## Links

- [Official API docs (PDF)](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/h6_market.py`
- `src/gridflow/schemas/entsoe.py`
