---
source: entsoe
dataset_key: balancing_energy_bids
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Balancing energy bids
  summary: >-
    The balancing energy bids offered in FR, BE and DE-LU, each quarter-hour: MW, price and
    direction, plus BE's aggregated offered MW.
  facts:
    vendor: ENTSO-E Transparency Platform, document types A37 and A24
    cadence: Quarter-hour points (`PT15M`), requested one UTC day at a time
    grain: "Bids: one row per zone, bid series, products, direction and quarter-hour"
  landscape: market
  what_it_is: >-
    Individual balancing energy bids per quarter-hour: offered MW (`MAW`) and a price in EUR per
    MWh, with a direction code (`A01` up, `A02` down, as gridflow reads them) and ENTSO-E's
    product codes. Of six zones gridflow asked, FR, BE and DE-LU sent bids on the days requested.
    The aggregated member is BE's offered MW per direction, as ENTSO-E publishes it.
  how_used:
    - Where the cheapest upward and downward balancing energy sits, quarter-hour by quarter-hour.
    - Price and depth features for imbalance and activation price models.
    - "Comparing balancing energy bid prices with the day-ahead price in the same zone."
  chart:
    type: line
    silver: entsoe/balancing_energy_bids
    time: timestamp_utc
    value: energy_price
    filter:
      - {column: direction, op: eq, value: A01}
    group: area_code
    group_map:
      "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2": BE
      "10YFR\x2DRTE\x2D\x2D\x2D\x2D\x2D\x2DC": FR
      "10Y1001A1001A82H": DE-LU
    series_order: [BE, FR, DE-LU]
    aggregation: min
    window: {start: "2026-08-01", end: "2026-08-01"}
    unit: EUR/MWh
  chart_view:
    title: Lowest upward bid price in each zone, 1 August 2026
    caption: >-
      Silver `entsoe/balancing_energy_bids`, EUR/MWh, 1 August 2026 (UTC): for each zone and
      quarter-hour, gridflow takes the lowest price among the individual upward (`A01`) bids of
      any product. ENTSO-E publishes bids, not a zone price; no volumes are added.
    alt: >-
      Line chart of the lowest upward (A01) bid price per quarter-hour, taken by gridflow over each
      zone's individual bids, in EUR/MWh, from entsoe/balancing_energy_bids for BE, FR and DE-LU on
      1 August 2026 (UTC). DE-LU is flat at 220 all day. FR holds 141.87 overnight and in the
      evening, drops to 115 from 07:30 and 111.30 from 09:00 to 12:45 UTC, and reaches 150.30
      after 22:00. BE moves most: 182 to 225 before 06:00, down to 84.32 at 12:45 UTC, and 175 to
      225 after 18:00.
    x_label: UTC time on 1 August 2026
    key:
      - {series: BE, label: BE, codes: "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2", paint: petrol}
      - {series: FR, label: FR, codes: "10YFR\x2DRTE\x2D\x2D\x2D\x2D\x2D\x2DC", paint: clay}
      - {series: DE-LU, label: DE-LU, codes: 10Y1001A1001A82H, paint: olive}
  raw_feed:
    note: >-
      One GET per zone per UTC day, paged 100 series at a time through `offset` until a short
      page. GB, NL and IE-SEM answered reason 999 on the days requested.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A37&periodStart=202608010000&periodEnd=202608020000&connecting_Domain=10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2&businessType=B74&offset=0&processType=A47&securityToken=<your-entsoe-api-key>"
    commands:
      - {run: gridflow ingest entsoe balancing_energy_bids --start 2026-08-01 --end 2026-08-02, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe balancing_energy_bids --start 2026-08-01 --end 2026-08-01, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: area_code, op: eq, value: "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2"}
        - {column: timestamp_utc, op: eq, value: "2026-08-01T12:00:00Z"}
        - {column: direction, op: eq, value: A01}
        - {column: bid_mrid, op: in, value: ["34", "35", "75", "76"]}
      order_by: [bid_mrid, standard_market_product]
      columns: [timestamp_utc, area_code, bid_mrid, direction, standard_market_product, quantity_mw, energy_price, currency_unit, original_market_product, business_type, resolution, published_at]
    key: [timestamp_utc, area_code, bid_mrid, direction, standard_market_product, original_market_product]
    caption: "BE, 12:00 UTC, 1 August 2026: four series numbers, each under two products in separate documents."
    fields:
      timestamp_utc: "Quarter-hour start, UTC: period start plus (position minus one) times 15 minutes"
      area_code: "Connecting area EIC, from each bid's `connecting_Domain.mRID`"
      bid_mrid: "Series `mRID` as sent; BE mixes small repeating numbers with long ids"
      direction: "`flowDirection.direction`: `A01` up or `A02` down, as gridflow reads them"
      standard_market_product: "`standard_MarketProduct` code as sent; blank on FR's own bids"
      original_market_product: "`original_MarketProduct`, a product code, not the direction: `A02` on FR's own bids"
      quantity_mw: "Offered MW for the quarter-hour, from `quantity.quantity` (unit `MAW`)"
      energy_price: "Bid price per MWh in `currency_unit`, from the point's `energy_Price.amount`"
      currency_unit: "The bid's `currency_Unit.name`: `EUR` here"
      business_type: "`businessType` as sent: `B74`, the type gridflow requests"
      resolution: "Point spacing as sent: `PT15M`"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, not when the bid was made"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_entsoe_balancing_energy_bids`, filtered on
      `timestamp_utc` with both ends included. Lineage columns are dropped and rows come ordered by
      `timestamp_utc` only, so sort before grouping.
    cells:
      - |
        df = data.entsoe.query("balancing_energy_bids", "2026-08-01", "2026-08-01")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
        df = df.sort_values(["area_code", "timestamp_utc", "energy_price"])
      - df[["timestamp_utc", "area_code", "direction", "standard_market_product", "quantity_mw", "energy_price"]].head(8)
      - df.groupby(["area_code", "direction", "standard_market_product", "original_market_product"]).size()
      - |
        be = df[df["area_code"].str.startswith("10YBE")]
        edge = be.groupby(["timestamp_utc", "direction"])["energy_price"].agg(["min", "max"]).unstack()
        edge = edge[[("min", "A01"), ("max", "A02")]]
        edge.columns = ["lowest upward", "highest downward"]
        edge.plot(ylabel="EUR/MWh", color=["#155A6E", "#C77E3C"], figsize=(8, 3.5))
    needs: 1 August 2026
    plot_alt: >-
      Line plot for BE on 1 August 2026 (UTC), EUR/MWh per quarter-hour: the lowest upward bid
      price (petrol) and the highest downward bid price (clay). Upward: 182 to 225 before 06:00,
      84.32 at 12:45. Downward: 101 to 115 until 04:15, then falling; 0 from 09:30 to 13:45, -10
      at 14:00, and 138 at 21:00.
  related:
    - {dataset: entsoe/procured_balancing_capacity, note: "Balancing capacity procured in the same zones, by direction"}
    - {dataset: entsoe/current_balancing_state, note: "Minute imbalance in BE, with the same direction codes"}
    - {dataset: entsoe/day_ahead_prices, note: "Day-ahead prices in the same zones, a reference for bid prices"}
    - {dataset: elexon/system_prices, note: "GB's imbalance prices; ENTSO-E answers GB bid requests with no data"}
  family:
    slug: balancing-energy-bids
    members:
      - dataset: balancing_energy_bids
        differs: "Each bid series per quarter-hour: MW, price, direction and product codes"
        request:
          - "GET https://web-api.tp.entsoe.eu/api?documentType=A37&periodStart=202608010000&periodEnd=202608020000&connecting_Domain=10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2&businessType=B74&offset=0&processType=A47&securityToken=<your-entsoe-api-key>"
          - "GET https://web-api.tp.entsoe.eu/api?documentType=A37&periodStart=202608010000&periodEnd=202608020000&connecting_Domain=10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2&businessType=B74&offset=100&processType=A47&securityToken=<your-entsoe-api-key>"
      - dataset: aggregated_balancing_energy_bids
        differs: "Aggregated offered MW by direction, no price; only BE answered 22 to 25 September"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A24&periodStart=202609220000&periodEnd=202609230000&area_Domain=10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2&processType=A51&securityToken=<your-entsoe-api-key>"
---

# ENTSO-E — Balancing energy bids (A37 / A47 / B74)

## Overview

Individual balancing energy bid offers submitted by Balance Service
Providers (BSPs) into a TSO's reserve activation pool. Each `Bid_TimeSeries`
in the response is one bid series (one mRID, not unique for BE), tagged with direction
(up/down regulation) and product type (Original_MarketProduct,
Standard_MarketProduct), with a Period containing the offered MW
volumes per resolution interval.

This is the **bid-level** view — each row is one bid series for one
quarter-hour; the response does not name the bidder. For aggregate (summed-across-bidders) balancing
energy quantities, use
[aggregated_balancing_energy_bids.md](./aggregated_balancing_energy_bids.md).
For activation outcomes (how much of those bids were actually called
on), use the H7 activated balancing prices/quantity datasets.

A37 is paired with `processType=A47` (balancing energy bid submission).
The H8 spec uses `connecting_Domain` here, not `area_Domain`, because
balancing energy bids can come from cross-zonal market participants
that connect via interconnectors. `connecting_Domain` is the area at
which the bid connects to the reserve pool.

→ Domain concepts:
  [Balancing market](../../../20-domain/markets/balancing-market.md)
  [Reserve products](../../../20-domain/concepts/reserve-products.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://web-api.tp.entsoe.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | Query param `securityToken=<ENTSOE_API_KEY>` |
| Rate limit       | Vendor-published: not documented. Project default: 1 req/s. |
| Pagination       | `offset` parameter (mandatory). A reply carries at most 100 `Bid_TimeSeries` (across its ZIP entries) and `offset=n` returns series n+1 to n+100; 4800 is the API guide's offset ceiling, not the page size, and is not enforced for A37 (live probe 2026-10-24, gridflow `client.py` `_ENTSOE_PAGE_SIZE` comment on `fix/entsoe-balancing-paging`). gridflow pages in steps of 100 until a page holds fewer than 100 series. On 1 Aug 2026 that took 331 pages for FR and for DE-LU (offsets 0 to 33000) and 62 for BE (0 to 6100). |
| Historical depth | TODO — H8 catalogue, varies by control area. GB has no published data (EMPTY). |
| Publication lag  | Near real-time after gate closure of the relevant balancing market interval. |
| Response format  | XML (`ReserveBid_MarketDocument`, series named `Bid_TimeSeries`), in a ZIP |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | string | Yes | `A37` | `A37` |
| `processType` | string | Yes | `A47` (balancing energy bid submission) | `A47` |
| `businessType` | string | Yes | `B74` (offer) | `B74` |
| `offset` | int | Yes | Pagination offset, start at `0` | `0` |
| `connecting_Domain` | string (EIC) | Yes | Connecting area EIC. Note: not `area_Domain` and not `controlArea_Domain`. | `10YGB----------A` |
| `periodStart` | string | Yes | UTC `yyyyMMddHHmm` | `202605070000` |
| `periodEnd` | string | Yes | UTC `yyyyMMddHHmm`, max 1 day window | `202605080000` |
| `securityToken` | string | Yes | API key | `<UUID>` |
| `Direction` | string | Optional | `A01` (up) / `A02` (down), as gridflow reads them — filter | `A01` |
| `Original_MarketProduct` | string | Optional | Filter on bidder's original market product | `A01` |
| `Standard_MarketProduct` | string | Optional | Filter on standardised product | `A05` |

ENTSOE tuple: `(documentType=A37, processType=A47, businessType=B74, area-param-name=connecting_Domain)`. Optional `(BusinessType, type_MarketAgreement.Type)` not applicable — A37 carries Original_MarketProduct / Standard_MarketProduct instead.

### Working curl example

```bash
curl --ssl-no-revoke -fsS -H "Accept: application/xml" \
  "https://web-api.tp.entsoe.eu/api?documentType=A37&processType=A47&businessType=B74&offset=0&connecting_Domain=10YGB----------A&periodStart=202605070000&periodEnd=202605080000&securityToken=${ENTSOE_API_KEY}" \
  -o /tmp/entsoe-balancing_energy_bids.xml \
  -w "HTTP %{http_code} | %{size_download} bytes\n"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/balancing_energy_bids/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML (`ReserveBid_MarketDocument`), as-received.
**Granularity**: One file per ZIP entry of one response page (`offset` in `.meta.json` `request_params`). One request per zone in `DEFAULT_ZONES` (GB, FR, NL, BE, DE-LU, IE-SEM) per UTC day (`EntsoeConnector._build_unit_tasks`, `endpoints.py` `DEFAULT_ZONES`). A37 responses arrive as ZIPs, one `.xml` per entry, the entry name kept in `.meta.json` `request_params.zip_entry` (`EntsoeConnector._raw_response_to_records`). GB, NL and IE-SEM return a code-999 acknowledgement; FR, BE and DE-LU publish.

> **⚠ The live envelope does NOT match the fixture below — live-probe verified
> 2026-08-04.** The vendor returns a `ReserveBid_MarketDocument` whose series
> elements are **`Bid_TimeSeries`**, not the `Balancing_MarketDocument` /
> `TimeSeries` shape this hand-built fixture assumes, and whose points carry
> **`<quantity.quantity>`**, not `<quantity>`. Evidence: gridflow
> `.planning/phases/R3-test-integrity/probes/entsoe_A37_extracted.xml` —
> 100 `<Bid_TimeSeries>` elements, **zero** bare `<TimeSeries>`.
> **Treat the sample below as fixture shape, not vendor shape.**
>
> **✅ CONFIRMED then FIXED — v0.18 R4-b, 2026-08-16 (gridflow PR #65).**
> The zero-row consequence was no longer inferred: measured against the saved
> 144 KB probe, the old parser returned **0 records from 100 populated bid
> series, with no warning at all**. It was a two-layer defect — fixing the
> element name alone still yielded zero rows, because the transformer's
> `value_tag="quantity"` was also matched by exact equality and the vendor
> sends `quantity.quantity`.
>
> The parser now resolves its accepted series and value tags from the document
> root, so a `ReserveBid_MarketDocument` is handled without changing behaviour
> for any other document type. Two ambiguity guards ride with it: a document
> presenting more than one accepted **series** name, or a `<Point>` presenting
> more than one accepted **value** tag, is refused loudly with zero records
> rather than resolved by element order. A zero-match diagnostic now warns when
> any ENTSO-E document yields no series matches at all — calibrated at one trip
> across the whole saved probe corpus, that trip being this very payload.
>
> **Price carried since the 2026-10-24 fix (gridflow PR #132, `fix/entsoe-balancing-silver`).**
> The parser now reads each Point's `energy_Price.amount` beside the quantity, and silver keeps it
> as `energy_price` with `currency_unit` (`h8_balancing.py` `BalancingEnergyBidsTransformer.output_cols`).
> On 1 Aug 2026 prices run from -15000 to 14999 EUR/MWh (DE-LU).
>
> **Live shape by zone (bronze 1 Aug 2026, all pages, fetched 2026-10-24; read 2026-10-24).**
> Every `Bid_TimeSeries` carries `connecting_Domain.mRID`, `acquiring_Domain.mRID`,
> `auction.mRID`, `businessType` `B74`, `flowDirection.direction`, `divisible`,
> `quantity_Measure_Unit.name` `MAW`, `currency_Unit.name` `EUR`,
> `price_Measure_Unit.name` `MWH` and Points of (`quantity.quantity`, `energy_Price.amount`), PT15M.
> A request for UTC day D returns many documents, each a ZIP entry, whose
> `reserveBid_Period` overlaps the day.
> - **BE**: documents from 15 minutes long up to the CET/CEST day (22:00Z to 22:00Z), including
>   those that start on D after 22:00Z, so the whole UTC day is covered.
>   `standard_MarketProduct.marketProductType` `A05` or `A07`, `status` `A06`/`A11`. Of 6,164 BE
>   series on 1 Aug, 5,818 have acquiring domain `10Y1001C--00085O`, `auction.mRID`
>   `AUCTION-mFRR` and a long, unique series `mRID` of the form `<40 hex>_20260801_<n>_U` or `_D`;
>   the other 346 have acquiring domain `10YBE----------2`, a numeric auction id and a small series
>   `mRID` (1 to 124) that recurs across documents and products. No two documents send the same
>   `mRID`, product and direction for one quarter-hour on 1 Aug.
> - **FR**: documents of 15 or 30 minutes. Most series are FR's own: acquiring domain
>   `10YFR-RTE------C`, `original_MarketProduct.marketProductType` `A02`, `auction.mRID` a local
>   datetime, no `status`, an 8-digit series `mRID` (30155699 to 30177352 on 1 Aug) that recurs
>   across quarter-hour documents. The rest are `A05` series with acquiring domain
>   `10Y1001C--00085O`, `auction.mRID` `AUCTION-mFRR` and a 33-character hex `mRID`.
> - **DE-LU**: documents of 15 or 30 minutes; `A07` (and 11 `A05`) series, all with `auction.mRID` `AUCTION-mFRR` and acquiring
>   domain `10Y1001C--00085O`, each with its own 22-character `mRID` (33,081 distinct on 1 Aug); both directions (`A01` 15,717 and `A02` 17,364 points on 1 Aug).
> - The meanings of `A05`, `A07`, `A02` (product) and `A06`/`A11` (status) are not established in
>   the repo. Note that `A07` bids are labelled `AUCTION-mFRR` by the vendor. Silver keeps no
>   `status`, so a minimum price taken over silver rows includes series of either status.

### Bronze sample

From `tests/fixtures/entsoe/balancing_energy_bids_gb.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Balancing_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:balancingdocument:4:0">
  <mRID>fixture-balancing-energy-bids-gb-20240115</mRID>
  <revisionNumber>1</revisionNumber>
  <type>A37</type>
  <process.processType>A47</process.processType>
  <TimeSeries>
    <mRID>bid-1</mRID>
    <businessType>B74</businessType>
    <Direction>A01</Direction>
    <Original_MarketProduct><marketProductType>A01</marketProductType></Original_MarketProduct>
    <Standard_MarketProduct><marketProductType>A05</marketProductType></Standard_MarketProduct>
    <connecting_Domain.mRID codingScheme="A01">10YGB----------A</connecting_Domain.mRID>
    <Period>
      <timeInterval>
        <start>2024-01-15T00:00Z</start>
        <end>2024-01-15T02:00Z</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>45</quantity></Point>
      <Point><position>2</position><quantity>52</quantity></Point>
    </Period>
  </TimeSeries>
</Balancing_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/balancing_energy_bids/year=YYYY/month=MM/balancing_energy_bids_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h8_balancing.BalancingEnergyBidsTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeBalancingEnergyBid`
**Dedup key**: `(timestamp_utc, area_code, bid_mrid, direction, standard_market_product, original_market_product)` (`h8_balancing.py` `BalancingEnergyBidsTransformer.unique_subset`, `fix/entsoe-balancing-silver`). Silver reads only the latest fetch run of each request, every page of it (`LATEST_FETCH_PER_REQUEST`, `_latest_fetch_files`). On 1 Aug 2026 the fixed parser gives 80,843 in-day points and 80,843 unique keys, so no bid is dropped.
**Point-in-time field**: `published_at`, the document `createdDateTime` (`with_published_at` in `h8_balancing.py`), a fetch-time stamp within seconds of the request, not a bid submission time.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | derived (Period start + (position - 1) × resolution, `parsers.py` `_point_timestamp`) | UTC-aware. |
| `area_code` | `str` | No | `connecting_Domain.mRID` | Renamed from `connecting_domain`. |
| `quantity_mw` | `float` | No | `<quantity.quantity>` (alias for `ReserveBid_MarketDocument`, `parsers.py` `_VALUE_TAG_ALIASES_BY_DOC_ROOT`) | Bid volume offered in MW (`MAW`). |
| `energy_price` | `float` | Yes | Point `<energy_Price.amount>` | Bid price per `price_Measure_Unit.name` (`MWH`) in `currency_unit`. |
| `currency_unit` | `str` | No | `<currency_Unit.name>` | `EUR` on every live bid. |
| `business_type` | `str` | No | `<businessType>` | Default "" in canonical. `B74` for bids. |
| `bid_mrid` | `str` | No | `Bid_TimeSeries/<mRID>` | Default "" in canonical. Renamed from `timeseries_mrid`. Form varies by zone (1 Aug 2026): BE sends long unique ids for its `AUCTION-mFRR` series (5,818 of 6,164) and small numbers 1 to 124 for the rest, which recur across documents and products; FR's own bids an 8-digit number that recurs across quarter-hour documents; DE-LU a unique 22-character id. Not a bid identity on its own for BE's numbers or FR's own bids. |
| `direction` | `str` | No | `flowDirection.direction` (the only spelling in live responses) | Default "" in canonical. `A01`=up, `A02`=down as gridflow reads them (the mapping in `activated_balancing_qty.py`); no ENTSO-E code list is quoted here. |
| `original_market_product` | `str` | No | `Original_MarketProduct/marketProductType` | Default "" in canonical. Bidder-side product. |
| `standard_market_product` | `str` | No | `Standard_MarketProduct/marketProductType` | Default "" in canonical. Standardised product code. |
| `resolution` | `str` | No | `<resolution>` (raw ISO-8601 duration code, emitted verbatim) | Default "" in canonical. `PT15M` in every live response. |
| `published_at` | `datetime[UTC]` | Yes | document `createdDateTime` | Fetch-time stamp (`with_published_at`). |
| `data_provider` | `str` | No | derived | Default "entsoe" in canonical. |
| `ingested_at` | `datetime` | Yes | derived | Stamped at silver transform time (`_H8BalancingTransformer.transform`). |

Not carried to silver: `acquiring_Domain.mRID`, `auction.mRID`, `status`, `divisible`, `price_Measure_Unit.name`.

### Silver sample

From the GB fixture (GB publishes nothing live):

```python
[
    {
        "timestamp_utc": datetime(2024, 1, 15, 0, 0, tzinfo=UTC),
        "area_code": "10YGB----------A",
        "quantity_mw": 45.0,
        "business_type": "B74",
        "bid_mrid": "bid-1",
        "direction": "A01",
        "original_market_product": "A01",
        "standard_market_product": "A05",
        "resolution": "PT60M",
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 5, 8, 18, 3, tzinfo=UTC),
    },
    {
        "timestamp_utc": datetime(2024, 1, 15, 1, 0, tzinfo=UTC),
        "area_code": "10YGB----------A",
        "quantity_mw": 52.0,
        "business_type": "B74",
        "bid_mrid": "bid-1",
        "direction": "A01",
        "original_market_product": "A01",
        "standard_market_product": "A05",
        "resolution": "PT60M",
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 5, 8, 18, 3, tzinfo=UTC),
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB returns EMPTY.** Live curl on 2026-05-08 returned reason 999: `No matching data found for Data item BALANCING_ENERGY_BIDS_R3 [GL EB 12.3.B&C] (10YGB----------A)...`. National Grid ESO does not publish to ENTSOE for this data item.
- **`offset` is mandatory.** Documented in ENTSOE API guide §4.1; a page carries 100 series and gridflow pages until a short page (see Pagination). A day is whole only when every page was fetched.
- **Bronze fetched before the paging fix holds page one only (gridflow gap, not a vendor one).** Days ingested before 2026-10-24 were fetched with `offset=0` alone: 2 to 5 Aug and 13 to 21 Sep 2026 hold one page (100 series) per zone, and their silver is cut to those bids (FR and DE-LU: the first quarter-hour only). Only 1 Aug 2026 has been re-ingested with every page; the other days stay partial until re-ingested.
- **The key includes the product (fixed 2026-10-24, gridflow PR #132).** The old key `(timestamp_utc, area_code, bid_mrid, direction)` dropped real BE bids, because BE's small series numbers are shared by series of different products and prices; `standard_market_product` and `original_market_product` are now in the key. Those numbers (and FR's own 8-digit ids) recur across documents, but on 1 Aug 2026 no two documents send the same `mRID`, product and direction for one quarter-hour, so the key is unique on all 80,843 points.
- **BE's 22:00 to 24:00 UTC is covered once every page is fetched.** BE documents for the CET/CEST day start at 22:00Z, but a request for UTC day D also returns the documents that start on D after 22:00Z, so the event-window filter keeps 00:00 to 23:45 UTC (1 Aug 2026: every zone 00:00 to 23:45). The old page-one bronze lacked those documents.
- **`bid_mrid` is not a bidder identity.** The transformer renames `timeseries_mrid` → `bid_mrid`. BE's small numbers and FR's own 8-digit ids recur (above); BE's long ids and DE-LU's ids are unique on 1 Aug 2026. Nothing in the response names the BSP.
- **Direction spelling.** Every live series sends `flowDirection.direction`; the parser also accepts `<Direction>` (`parse_timeseries_xml`).

### Control-area vs cross-zonal

A37 uses `connecting_Domain` (the area where the bid connects to the
reserve pool), not `area_Domain` (which is the TSO control area). This
distinction matters for cross-zonal balancing — a French BSP can submit
bids that connect via the GB control area through the IFA interconnector.
For domestic balancing only, `connecting_Domain` and `area_Domain` will
typically point to the same EIC.

---

## Implementation delta

- **Pagination (fixed 2026-10-24, gridflow PR #130, `fix/entsoe-balancing-paging`).** `_ENTSOE_PAGE_SIZE` is now 100 and `count_timeseries_or_none` counts `Bid_TimeSeries` as well as `TimeSeries`, so the loop pages until a short page. A runaway guard fails the fetch after 10,000 full pages (`EntsoePagingLimitError`) rather than keep a partial day.
- **Schema-vs-fixture default for `business_type`.** Schema default is `""` but `endpoints.py` always sends `B74` and the fixture carries `B74`. Empty default is harmless but misleading — the dataset will never produce a row with empty `business_type` from this query path.

---

## Modelling notes

- Bid-level features (offered MW, direction, product type) are useful for: balancing market price formation, BSP behaviour modelling, capacity-margin shadow-price modelling.
- For aggregate balancing pressure, use `aggregated_balancing_energy_bids` instead — bid-level data is high-cardinality and noisy when summed across bidders.
- GB modelling alternative: Elexon `boal` (bid-offer-acceptance) — different schema (per-acceptance, not per-bid) but equivalent semantic content.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf) — Section 17.4 / GL EB 12.3.B&C
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py` — `balancing_energy_bids`
- `src/gridflow/silver/entsoe/h8_balancing.py` — `BalancingEnergyBidsTransformer`
- `src/gridflow/schemas/entsoe.py` — `EntsoeBalancingEnergyBid`
- `tests/fixtures/entsoe/balancing_energy_bids_gb.xml`
- [Aggregated counterpart](./aggregated_balancing_energy_bids.md)
