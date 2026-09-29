---
source: entsoe
dataset_key: balancing_energy_bids
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSO-E — Balancing energy bids (A37 / A47 / B74)

## Overview

Individual balancing energy bid offers submitted by Balance Service
Providers (BSPs) into a TSO's reserve activation pool. Each TimeSeries
in the response represents one bid (one mRID), tagged with direction
(up/down regulation) and product type (Original_MarketProduct,
Standard_MarketProduct), with a Period containing the offered MW
volumes per resolution interval.

This is the **bid-level** view — each row represents one bidder's offer
for one timestamp. For aggregate (summed-across-bidders) balancing
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
| Pagination       | `offset` parameter (mandatory). API documents up to 4800 TimeSeries; if exceeded, increment `offset` by 100 until pages exhausted (per ENTSOE API guide §4.1). **Observed 2026-09-26:** every populated response (42 zone-days, Aug and Sep 2026) carried exactly 100 `Bid_TimeSeries` in total, across its ZIP entries (e.g. 94 + 6, 99 + 1), so a page is 100 series here. gridflow never requests `offset=100` (see Implementation delta). |
| Historical depth | TODO — H8 catalogue, varies by control area. GB has no published data (EMPTY). |
| Publication lag  | Near real-time after gate closure of the relevant balancing market interval. |
| Response format  | XML (`Balancing_MarketDocument`) |

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
| `Direction` | string | Optional | `A01` (up) / `A02` (down) — filter | `A01` |
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
**Format**: Raw XML (`Balancing_MarketDocument`), as-received.
**Granularity**: One file per ZIP entry of one response. One request per zone in `DEFAULT_ZONES` (GB, FR, NL, BE, DE-LU, IE-SEM) per UTC day (`client.py:249`, `endpoints.py:395`). A37 responses arrive as ZIPs, one `.xml` per entry, the entry name kept in `.meta.json` `request_params.zip_entry` (`client.py:367-381`). GB, NL and IE-SEM return a code-999 acknowledgement; FR, BE and DE-LU publish.

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
> **Residual, deliberate:** the bid **price** (`<energy_Price.amount>`,
> observed down to −14997 EUR/MWh) is still discarded — the silver schema has
> no price column, so recovered rows carry quantity only. Verified that no gold
> view, model handle, notebook or quality check reads these rows as complete
> bid records; bronze retains the bytes. Filed as a v0.19 carry.
>
> **Live shape by zone (bronze 1 to 5 Aug and 13 to 21 Sep 2026, read 2026-09-29).**
> Every `Bid_TimeSeries` carries `connecting_Domain.mRID`, `acquiring_Domain.mRID`,
> `auction.mRID`, `businessType` `B74`, `flowDirection.direction`, `divisible`,
> `quantity_Measure_Unit.name` `MAW`, `currency_Unit.name` `EUR`,
> `price_Measure_Unit.name` `MWH` and one Point per Period
> (`quantity.quantity`, `energy_Price.amount`), PT15M.
> - **BE**: one document per request, `reserveBid_Period` 22:00Z to 22:00Z (the CET/CEST day),
>   `standard_MarketProduct.marketProductType` `A05` or `A07`, `status` `A06`/`A11`, 1 to 18 Periods
>   per series. The series `mRID` is a small sequence number (1 to 81) that is **reused** for an
>   `A05` and an `A07` series in the same document.
> - **FR**: `reserveBid_Period` 00:00Z to 00:15Z only; `original_MarketProduct.marketProductType`
>   `A02`, `auction.mRID` a local datetime, 8-digit `mRID`. A second ZIP entry (document
>   `domain.mRID` `10Y1001C--00085O`, `auction.mRID` `AUCTION-mFRR`) carries `A05` series for the
>   same quarter-hour.
> - **DE-LU**: `reserveBid_Period` 00:00Z to 00:15Z only; `A07` with `auction.mRID`
>   `AUCTION-mFRR` and acquiring domain `10Y1001C--00085O`; almost all `A02`.
> - The meanings of `A05`, `A07`, `A02` (product) and `A06`/`A11` (status) are not established in
>   the repo. Note that `A07` bids are labelled `AUCTION-mFRR` by the vendor.

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
**Dedup key**: `(timestamp_utc, area_code, bid_mrid, direction)`
**Point-in-time field**: `published_at`, the document `createdDateTime` (`h8_balancing.py:91`), a fetch-time stamp within seconds of the request, not a bid submission time.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | derived (Period start + (position - 1) × resolution, `parsers.py:530`) | UTC-aware. |
| `area_code` | `str` | No | `connecting_Domain.mRID` | Renamed from `connecting_domain`. |
| `quantity_mw` | `float` | No | `<quantity.quantity>` (alias for `ReserveBid_MarketDocument`, `parsers.py:171-173`) | Bid volume offered in MW (`MAW`). |
| `business_type` | `str` | No | `<businessType>` | Default "" in canonical. `B74` for bids. |
| `bid_mrid` | `str` | No | `Bid_TimeSeries/<mRID>` | Default "" in canonical. Renamed from `timeseries_mrid`. Unique per bid for FR and DE-LU; for BE a per-document sequence number reused across products, so not a bid identity on its own. |
| `direction` | `str` | No | `flowDirection.direction` (the only spelling in live responses) | Default "" in canonical. `A01`=up, `A02`=down. |
| `original_market_product` | `str` | No | `Original_MarketProduct/marketProductType` | Default "" in canonical. Bidder-side product. |
| `standard_market_product` | `str` | No | `Standard_MarketProduct/marketProductType` | Default "" in canonical. Standardised product code. |
| `resolution` | `str` | No | `<resolution>` (raw ISO-8601 duration code, emitted verbatim) | Default "" in canonical. `PT15M` in every live response. |
| `published_at` | `datetime[UTC]` | Yes | document `createdDateTime` | Fetch-time stamp (`h8_balancing.py:91`). |
| `data_provider` | `str` | No | derived | Default "entsoe" in canonical. |
| `ingested_at` | `datetime` | Yes | derived | Stamped at silver transform time (`h8_balancing.py:99`). |

Not carried to silver: `energy_Price.amount` (the bid price), `acquiring_Domain.mRID`, `auction.mRID`, `status`, `divisible`.

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
- **`offset` is mandatory, and silver holds page one only.** Documented in ENTSOE API guide §4.1. Live pages carry 100 series. The connector sends `offset=0` and stops there (see Implementation delta), so every zone-day is cut at 100 bids, silently. Effect, measured 2026-09-29 on bronze 1 to 5 Aug and 13 to 21 Sep 2026: FR and DE-LU silver holds exactly 100 bids per day, all at 00:00 UTC (the first quarter-hour), and DE-LU's are all `A02`; BE holds 64 to 81 distinct `bid_mrid` per day across 00:00 to 21:45 UTC.
- **Dedup collision on BE (silver drops real bids).** The key `(timestamp_utc, area_code, bid_mrid, direction)` (`h8_balancing.py:148`) omits the product, and BE reuses one `mRID` for an `A05` and an `A07` series; `unique(keep="last")` (`h8_balancing.py:104`) keeps whichever parsed later. Reproduced with gridflow's parser: 88,146 in-window BE points → 78,763 silver rows (9,383 lost, 10.6%); on 15 Sep 2026 12:00 UTC, 50 BE bids (1,524 MW) → 42. Adding `standard_market_product` and `original_market_product` to the key removes every collision (90,946 in-window points, 90,946 unique). Surviving rows are internally consistent (product, direction and MW from one series).
- **BE loses 22:00 to 24:00 UTC every day.** BE documents run 22:00Z to 22:00Z; the HALF_OPEN event-window filter (`EVENT_WINDOW_FILTER = True`, `h8_balancing.py:152`) drops the day-D document's first eight quarter-hours (they belong to D-1), and the D-1 document ends at 22:00Z. 10,628 parsed points dropped over the 14 days. The FILTER_SAFE classification (`_event_window.py:528-556`) rests on a DE-LU probe whose document starts at the request start; BE's does not.
- **`bid_mrid` is not a bidder identity.** The transformer renames `timeseries_mrid` → `bid_mrid`. FR and DE-LU send distinct 8-digit or random mRIDs; BE sends a per-document sequence reused across products (above). Nothing in the response names the BSP.
- **Direction spelling.** Every live series sends `flowDirection.direction`; the parser also accepts `<Direction>` (`parsers.py:316-319`).

### Control-area vs cross-zonal

A37 uses `connecting_Domain` (the area where the bid connects to the
reserve pool), not `area_Domain` (which is the TSO control area). This
distinction matters for cross-zonal balancing — a French BSP can submit
bids that connect via the GB control area through the IFA interconnector.
For domestic balancing only, `connecting_Domain` and `area_Domain` will
typically point to the same EIC.

---

## Implementation delta

- **Pagination loop never reaches page two for A37.** The loop exists (`client.py:313-349`) but steps `offset` by `_ENTSOE_PAGE_SIZE = 4800` (`client.py:63`) and stops when a page counts fewer than 4800 series. Its counter `count_timeseries_or_none` counts only elements named `TimeSeries` (`client.py:483-512`), and A37 sends `Bid_TimeSeries`, so the count is 0 and the loop always stops after `offset=0`. Live pages carry 100 series, so both the step and the counter need fixing.
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
