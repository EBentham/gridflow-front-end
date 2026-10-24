---
source: entsoe
dataset_key: procured_balancing_capacity
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Procured balancing capacity by area
  summary: >-
    The balancing capacity each area procured, one row per series and quarter-hour, each series
    with a direction, agreement type, MW and price.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A15, process type A51
    cadence: Quarter-hour points; each series holds one MW and price over its block
    grain: One row per series and quarter-hour in each area
  landscape: market
  what_it_is: >-
    The balancing capacity procured in each area. Each series, which gridflow reads as one offer,
    carries a direction (`A01` up, `A02` down), an agreement type, MW and a price per MW. On 1
    August 2026, FR, NL, BE and DE-LU sent results; GB and IE-SEM had none. An area's procured MW
    sums its series per direction and agreement type.
  how_used:
    - Reserve volumes and capacity prices per area, for adequacy and price models.
    - Upward against downward procurement within an area, block by block.
    - Capacity prices read beside the same zone's day-ahead energy prices.
  caveat: ENTSO-E sends each price in EUR per MW, without saying per hour or per block.
  chart:
    type: line
    silver: entsoe/procured_balancing_capacity
    time: timestamp_utc
    value: quantity_mw
    filter:
      - {column: direction, op: eq, value: A01}
      - {column: market_agreement_type, op: eq, value: A01}
    group: area_code
    group_map:
      "10Y1001A1001A82H": de_lu
      "10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC": fr
      "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL": nl
      "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2": be
    series_order: [de_lu, fr, nl, be]
    aggregation: sum
    window: {start: "2026-08-01", end: "2026-08-01"}
    unit: MW
  chart_view:
    title: Upward capacity procured per area, 1 August 2026
    caption: >-
      Silver `entsoe/procured_balancing_capacity`, MW, each quarter-hour of the UTC day 1 August
      2026: every area's upward (`A01`) series under daily agreements (`A01`), summed. Downward
      series and NL's other agreement type, `A13` (meaning not documented here), are left out.
    alt: >-
      Line chart of upward capacity procured per area under daily agreements, from
      entsoe/procured_balancing_capacity, in MW, each quarter-hour of 1 August 2026 (UTC). The
      lines step at block edges. DE-LU is highest: 1,821 MW at midnight, 2,203 from 18:00 to 22:00.
      FR holds about 600 overnight, about 910 from 06:00, 1,528 to 1,537 from 14:00 to 18:00, about
      705 until 22:00, then about 605. NL holds 247 until 22:00, then 191. BE moves between 76 and 101.
    x_label: UTC time on 1 August 2026
    key:
      - {series: de_lu, label: Germany and Luxembourg, codes: DE-LU, paint: petrol}
      - {series: fr, label: France, codes: FR, paint: horizon}
      - {series: nl, label: Netherlands, codes: NL, paint: olive, note: "Daily agreement only; NL's `A13` series (meaning not documented here) are left out."}
      - {series: be, label: Belgium, codes: BE, paint: clay}
  raw_feed:
    note: >-
      One GET per area and UTC day, paged with `offset` until a reply holds fewer than 100 series.
      On 1 August 2026, GB and IE-SEM got an acknowledgement, reason 999.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A15&periodStart=202608010000&periodEnd=202608020000&area_Domain=10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL&offset=0&processType=A51&securityToken=$ENTSOE_API_KEY"
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A15&periodStart=202608010000&periodEnd=202608020000&area_Domain=10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL&offset=100&processType=A51&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe procured_balancing_capacity --start 2026-08-01 --end 2026-08-02, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe procured_balancing_capacity --start 2026-08-01 --end 2026-08-01, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: area_code, op: eq, value: "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL"}
        - {column: timestamp_utc, op: eq, value: "2026-08-01T12:00:00Z"}
        - {column: quantity_mw, op: ge, value: 29}
      order_by: [direction, market_agreement_type, procurement_price]
      columns: [timestamp_utc, quantity_mw, procurement_price, direction, market_agreement_type, area_code, currency_unit, series_mrid, document_mrid, published_at]
    key: [timestamp_utc, area_code, document_mrid, series_mrid]
    caption: "NL, 12:00 UTC 1 August 2026: series of 29 MW or more, both directions and agreements."
    fields:
      timestamp_utc: "Quarter-hour start, UTC; a series' one point repeats across its block"
      area_code: "The area's EIC, from the document's `area_Domain.mRID`"
      document_mrid: "The document's `mRID`; ENTSO-E stamps a fresh one on every reply"
      series_mrid: "Series number within its document; numbering restarts at 1 in each document"
      direction: "`flowDirection.direction`: `A01` up, `A02` down"
      market_agreement_type: "`type_MarketAgreement.type` as sent; `A01` is daily products"
      quantity_mw: "The series' MW (`MAW`); the area's total sums series per direction and agreement type"
      procurement_price: "`procurement_Price.amount`, the series' price per MW in `currency_unit`"
      currency_unit: "`currency_Unit.name` as sent"
      standard_market_product: "`standard_MarketProduct.marketProductType` as sent; empty when the area sends none"
      original_market_product: "`original_MarketProduct.marketProductType` as sent; empty when the area sends none"
      psr_type: "`mktPSRType.psrType`, ENTSO-E's resource type code, as sent"
      business_type: "`businessType` as sent: `B95` in these rows"
      resolution: "Point spacing as sent: `PT15M`"
      published_at: "Reply `createdDateTime`, UTC: a fetch-time stamp, not when the capacity was allocated"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation
      `silver_entsoe_procured_balancing_capacity`, filtered on `timestamp_utc` (UTC days, both
      ends included) and returned in the session's time zone, Europe/London here. Lineage columns
      are dropped; rows are time-ordered only.
    cells:
      - df = data.entsoe.query("procured_balancing_capacity", "2026-08-01", "2026-08-01")
      - df[["timestamp_utc", "area_code", "direction", "market_agreement_type", "quantity_mw", "procurement_price"]].head()
      - |
        up = df[(df.direction == "A01") & (df.market_agreement_type == "A01")]
        mw = up.groupby(["timestamp_utc", "area_code"]).quantity_mw.sum().unstack()
        mw.plot(figsize=(8, 3.5), ylabel="MW procured, upward")
    needs: 1 August 2026
    plot_alt: >-
      Line plot of upward MW procured under daily agreements, one line per area EIC, with London
      times from 01:00 on 1 August to 00:45 on 2 August 2026. DE-LU steps between 1,821 and 2,203;
      FR between 586 and 1,537, highest from 15:00 to 19:00 London time; NL and BE stay below 250.
  related:
    - {dataset: entsoe/balancing-energy-bids, note: "Energy bids in the same areas, offered for activation"}
    - {dataset: entsoe/current_balancing_state, note: "Minute imbalance in three of the same areas: FR, NL and BE"}
    - {dataset: entsoe/day_ahead_prices, note: "Day-ahead energy prices in the same zones, beside capacity prices"}
---

# ENTSO-E — Procured balancing capacity (A15 / A51)

## Overview

Volume of balancing **capacity** (reserve) procured by a TSO ahead of
real-time, broken down by market agreement type (e.g. `A01` daily, `A02`
weekly). This is the **capacity** product (an availability price per
MW; live documents give `price_Measure_Unit.name` `MAW` and state no time
basis), distinct from **balancing energy** (the activated MWh
products covered by `balancing_energy_bids` and the H7 activated
prices/quantity datasets).

A TSO procures capacity through tenders on rolling timeframes; this
dataset reports the MW procured for each interval, split across many
TimeSeries: in live responses (FR, NL, BE, DE-LU, 1 to 5 August 2026)
each series carries one direction, one quantity and one
`procurement_Price.amount`, so no single series is the area total. Silver
keeps one row per series and quarter-hour; an area's procured MW is the
sum of its rows for one direction and agreement type
(`EntsoeBalancingCapacity` docstring, `schemas/entsoe.py:735-738`). Useful
for: capacity-margin / reserve-adequacy modelling, capacity-payment
shadow-price modelling, and tracking how reserve procurement levels
respond to forecasted system stress.

A15 is paired with `processType=A51` (procurement), and the H8 spec
uses `area_Domain` (single control area). This dataset is one-area —
not cross-zonal — for the cross-zonal counterpart see
[cross_zonal_balancing_capacity.md](./cross_zonal_balancing_capacity.md).

→ Domain concepts:
  [Reserve products](../../../20-domain/concepts/reserve-products.md)
  [Capacity vs energy products](../../../20-domain/concepts/capacity-vs-energy.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://web-api.tp.entsoe.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | Query param `securityToken=<ENTSOE_API_KEY>` |
| Rate limit       | Vendor-published: not documented. Project default: 1 req/s. |
| Pagination       | `offset` parameter (mandatory, start at 0) per ENTSOE API §4.1. A reply carries at most 100 series; `offset=n` returns series n+1 to n+100. The connector pages in steps of 100 and stops at a page with fewer than 100 series, counted across a ZIP reply's documents; it fails the fetch after 10,000 full pages (`client.py:56-70`, `client.py:363-374` on the paging fix). |
| Historical depth | TODO — H8 catalogue, varies by area. GB has no published data. |
| Publication lag  | After tender close — daily / weekly / monthly cadences depending on `Type_MarketAgreement.Type`. |
| Response format  | XML (`Balancing_MarketDocument`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | string | Yes | `A15` | `A15` |
| `processType` | string | Yes | `A51` | `A51` |
| `offset` | int | Yes | Pagination offset, start at `0` | `0` |
| `area_Domain` | string (EIC) | Yes | Control area EIC. **Not** `controlArea_Domain`. | `10YGB----------A` |
| `periodStart` | string | Yes | UTC `yyyyMMddHHmm` | `202605070000` |
| `periodEnd` | string | Yes | UTC `yyyyMMddHHmm`, max 1 day | `202605080000` |
| `Type_MarketAgreement.Type` | string | Optional | `A01`=daily, `A02`=weekly, etc. — filter on procurement product | `A01` |
| `securityToken` | string | Yes | API key | `<UUID>` |

ENTSOE tuple: `(documentType=A15, processType=A51, businessType=n/a, area-param-name=area_Domain)`. Optional `(BusinessType, type_MarketAgreement.Type)`: `BusinessType` is **not** required at query level (the response carries `<businessType>` per TimeSeries); `Type_MarketAgreement.Type` is an optional filter — fixture carries `Type_MarketAgreement.Type=A01`.

### Working curl example

```bash
curl --ssl-no-revoke -fsS -H "Accept: application/xml" \
  "https://web-api.tp.entsoe.eu/api?documentType=A15&processType=A51&offset=0&area_Domain=10YGB----------A&periodStart=202605070000&periodEnd=202605080000&securityToken=${ENTSOE_API_KEY}" \
  -o /tmp/entsoe-procured_balancing_capacity.xml \
  -w "HTTP %{http_code} | %{size_download} bytes\n"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/procured_balancing_capacity/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML.
**Granularity**: One file per (zone in `DEFAULT_ZONES`, UTC day window, offset page) (`client.py:249`, `endpoints.py:395`). A page that arrives as a ZIP is stored as one file per XML entry, its sidecar naming the `zip_entry` (`client.py:386-405`).

### Bronze sample

From `tests/fixtures/entsoe/procured_balancing_capacity_gb.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Balancing_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:balancingdocument:4:0">
  <mRID>fixture-procured-balancing-capacity-gb-20240115</mRID>
  <revisionNumber>1</revisionNumber>
  <type>A15</type>
  <process.processType>A51</process.processType>
  <TimeSeries>
    <mRID>capacity-1</mRID>
    <Type_MarketAgreement.Type>A01</Type_MarketAgreement.Type>
    <area_Domain.mRID codingScheme="A01">10YGB----------A</area_Domain.mRID>
    <Period>
      <timeInterval>
        <start>2024-01-15T00:00Z</start>
        <end>2024-01-15T02:00Z</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>500</quantity></Point>
      <Point><position>2</position><quantity>525</quantity></Point>
    </Period>
  </TimeSeries>
</Balancing_MarketDocument>
```

The fixture does not match live responses. Live A15 documents (bronze of
1 to 5 August 2026) carry `area_Domain.mRID` once at document level, not
inside `TimeSeries`; spell the agreement tag `type_MarketAgreement.type`;
add `businessType` `B95`, `flowDirection.direction`, `mktPSRType.psrType`,
`curveType` `A03` and (all but BE) `standard_MarketProduct.marketProductType`
(BE sends `original_MarketProduct.marketProductType` instead); and give
each series one `Point` (position 1) with `quantity` and
`procurement_Price.amount`, held across its `Period` at `PT15M`. Units are
`currency_Unit.name` `EUR`, `quantity_Measure_Unit.name` `MAW` and
`price_Measure_Unit.name` `MAW`. Each document also carries
`allocationDecision_DateAndOrTime.dateTime` (for example 2026-07-31T07:00Z
on a BE document for 1 August), which silver does not keep.

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/procured_balancing_capacity/year=YYYY/month=MM/procured_balancing_capacity_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h8_balancing.ProcuredBalancingCapacityTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeBalancingCapacity`
**Dedup key**: `(timestamp_utc, area_code, document_mrid, series_mrid)`: one row per series of one reply and quarter-hour (`h8_balancing.py:262-265` on the silver fix, `DATASET_VERSION` `2.0.0`). Only the latest fetch run of each request is read (`LATEST_FETCH_PER_REQUEST`, `_latest_fetch_files`, `h8_balancing.py:361`).
**Point-in-time field**: none

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | derived | UTC-aware quarter-hour start; a series' one point (curve `A03`) repeats across its `Period`, clipped to the UTC day. |
| `area_code` | `str` | No | `area_Domain.mRID` | Renamed from `area_domain`. Live documents carry it once at document level; the parser falls back to it when a series has none (`parsers.py:238`, `:488` on the silver fix). |
| `quantity_mw` | `float` | No | `<quantity>` | One series' procured MW (`MAW`); the area's procured MW is the sum over series for one direction and agreement type. |
| `procurement_price` | `float` | Yes | `<procurement_Price.amount>` | The series' price per MW in `currency_unit` (`parsers.py:549`). |
| `currency_unit` | `str` | No | `<currency_Unit.name>` | `EUR` in the live documents. |
| `market_agreement_type` | `str` | No | `<type_MarketAgreement.type>` | Default "" in canonical. `A01` is daily products (ENTSO-E's code list, as noted on the `contracted_reserves` A81 entry, `endpoints.py:323-324`; not stated on the A15 entry); NL also sends `A13`. The live lowercase spelling is matched (`parsers.py:354`). |
| `direction` | `str` | No | `<flowDirection.direction>` | `A01` up, `A02` down (the mapping in `activated_balancing_prices.py:90`). |
| `standard_market_product` | `str` | No | `<standard_MarketProduct.marketProductType>` | Empty when the document sends none (BE). |
| `original_market_product` | `str` | No | `<original_MarketProduct.marketProductType>` | Empty when the document sends none (all but BE). |
| `psr_type` | `str` | No | `<mktPSRType.psrType>` | Matched since the silver fix (`parsers.py:381`). |
| `business_type` | `str` | No | `<businessType>` | Default "" in canonical. `B95` on every series in the live responses of 1 to 5 August 2026. |
| `document_mrid` | `str` | No | document `<mRID>` | ENTSO-E stamps a fresh one on every reply, so it identifies a page, not a result. |
| `series_mrid` | `str` | No | `TimeSeries/<mRID>` | Restarts at 1 in every document, so in every page (`h8_balancing.py:54-57`) and in each document of a ZIP page. |
| `resolution` | `str` | No | `<resolution>` | Default "" in canonical. |
| `published_at` | `datetime[UTC]` | Yes | `<createdDateTime>` | Document creation time, within seconds of the fetch (`h8_balancing.py:107`); not the allocation decision time. |
| `data_provider` | `str` | No | derived | Default "entsoe" in canonical. |
| `ingested_at` | `datetime` | Yes | derived | Stamped at silver transform time (`h8_balancing.py:116`). |

### Silver sample

Two NL rows of 1 August 2026, 12:00 UTC, one up and one down offer (lineage columns omitted; `ingested_at` truncated to the second).

```python
[
    {
        "timestamp_utc": datetime(2026, 8, 1, 12, 0, tzinfo=UTC),
        "area_code": "10YNL----------L",
        "quantity_mw": 69.0,
        "procurement_price": 6.21,
        "currency_unit": "EUR",
        "market_agreement_type": "A01",
        "direction": "A01",
        "standard_market_product": "A01",
        "original_market_product": "",
        "psr_type": "A04",
        "business_type": "B95",
        "document_mrid": "53d5ff9971124166835c0636d59eecc6",
        "series_mrid": "88",
        "resolution": "PT15M",
        "published_at": datetime(2026, 10, 24, 14, 8, 18, tzinfo=UTC),
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 10, 24, 14, 55, 38, tzinfo=UTC),
    },
    {
        "timestamp_utc": datetime(2026, 8, 1, 12, 0, tzinfo=UTC),
        "area_code": "10YNL----------L",
        "quantity_mw": 72.0,
        "procurement_price": 8.0,
        "currency_unit": "EUR",
        "market_agreement_type": "A01",
        "direction": "A02",
        "standard_market_product": "A01",
        "original_market_product": "",
        "psr_type": "A04",
        "business_type": "B95",
        "document_mrid": "53d5ff9971124166835c0636d59eecc6",
        "series_mrid": "75",
        "resolution": "PT15M",
        "published_at": datetime(2026, 10, 24, 14, 8, 18, tzinfo=UTC),
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 10, 24, 14, 55, 38, tzinfo=UTC),
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB returns EMPTY.** Live curl on 2026-05-08 returned reason 999: `No matching data found for Data item PROCURED_BALANCING_CAPACITY_R3 [12.3.F] (10YGB----------A)...`. The ingest of 1 to 5 August 2026, and the paged re-fetch of 1 August on 2026-10-24, got the same reason for GB and for IE-SEM (`10Y1001A1001A59C`).
- **Several offers share every attribute.** Series with the same area, direction, agreement type and product coexist at one time with different quantities and prices, so a row is keyed on the reply's document mRID and the series mRID (`h8_balancing.py:262-265`). Sum `quantity_mw` per area, direction and agreement type for the area's procured MW; never across directions or agreement types.
- **A page may be a ZIP of several documents.** On 1 August 2026, BE's page at `offset=300` held two documents of 45 and 55 series, and FR's at `offset=2000` two of 31 and 69. The pager counts series across the entries (`client.py:356-363` on the paging fix).
- **Bronze fetched before the paging fix holds page one only.** The ingest of 2026-08-16 (1 to 5 August 2026) took the first 100 series per area and day. Only 1 August was re-fetched with paging (2026-10-24, silver `DATASET_VERSION` `2.0.0`); the other days' silver is partial until they are re-ingested. The 22:00 to 24:00 UTC gap seen before the fix came from the missing pages: the paged 1 August reply includes the next CEST day's first blocks, and its silver runs 00:00 to 23:45 UTC.
- **`business_type` is `B95` throughout.** Every live series of 1 to 5 August 2026 carries `B95`, so it does not distinguish records.
- **`published_at` is the fetch, not the allocation.** It is the reply's `createdDateTime`, seconds before the fetch. The document's `allocationDecision_DateAndOrTime.dateTime` is not parsed, so silver cannot say when the capacity was allocated.

### Control-area vs cross-zonal

A15 is single-area only (`area_Domain`). The cross-zonal capacity
counterpart is A38, see
[cross_zonal_balancing_capacity.md](./cross_zonal_balancing_capacity.md).

---

## Implementation delta

- **`Type_MarketAgreement.Type` filter is optional and not sent** (`endpoints.py:354-360`), so a reply carries every agreement type; `market_agreement_type` keeps them apart in silver.
- **The allocation decision time is not parsed** (`allocationDecision_DateAndOrTime.dateTime`), so silver has no point-in-time field for when the capacity was procured.

---

## Modelling notes

- Procured-capacity volumes are leading indicators for **reserve scarcity** — when capacity below historical mean, balancing energy prices typically firm up.
- Use as a feature in: capacity-payment shadow-price models, reserve-margin nowcasts, and balancing market spreads.
- Pair with [aggregated_balancing_energy_bids.md](./aggregated_balancing_energy_bids.md) (capacity vs energy, before activation) and the H7 activated datasets (capacity vs realised activations).

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf) — Section 17 / 12.3.F
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py` — `procured_balancing_capacity`
- `src/gridflow/silver/entsoe/h8_balancing.py` — `ProcuredBalancingCapacityTransformer`
- `src/gridflow/schemas/entsoe.py` — `EntsoeBalancingCapacity`
- `tests/fixtures/entsoe/procured_balancing_capacity_gb.xml`
- [Cross-zonal counterpart](./cross_zonal_balancing_capacity.md)
