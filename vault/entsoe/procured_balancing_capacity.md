---
source: entsoe
dataset_key: procured_balancing_capacity
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSO-E — Procured balancing capacity (A15 / A51)

## Overview

Volume of balancing **capacity** (reserve) procured by a TSO ahead of
real-time, broken down by market agreement type (e.g. `A01` daily, `A02`
weekly). This is the **capacity** product (€/MW/h-style availability
payment), distinct from **balancing energy** (the activated MWh
products covered by `balancing_energy_bids` and the H7 activated
prices/quantity datasets).

A TSO procures capacity through tenders on rolling timeframes; this
dataset reports the MW procured for each interval, split across many
TimeSeries: in live responses (FR, NL, BE, DE-LU, 1 to 5 August 2026)
each series carries one direction, one quantity and one
`procurement_Price.amount`, so no single series is the area total. Useful
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
| Pagination       | `offset` parameter (mandatory, start at 0) per ENTSOE API §4.1. The connector pages in steps of 4800 and stops at a page with fewer than 4800 series (`client.py:63`, `client.py:347`); live A15 pages carry 100, so only the first is fetched. |
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
**Granularity**: One file per (zone in `DEFAULT_ZONES`, UTC day window, offset page) (`client.py:249`, `endpoints.py:395`).

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
`curveType` `A03` and (all but BE) `standard_MarketProduct.marketProductType`; and give
each series one `Point` (position 1) with `quantity` and
`procurement_Price.amount`, held across its `Period` at `PT15M`.

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/procured_balancing_capacity/year=YYYY/month=MM/procured_balancing_capacity_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h8_balancing.ProcuredBalancingCapacityTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeBalancingCapacity`
**Dedup key**: `(timestamp_utc, area_code, market_agreement_type)`
**Point-in-time field**: none

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | derived | UTC-aware. |
| `area_code` | `str` | No | `area_Domain.mRID` | Renamed from `area_domain`. Empty on live responses: the tag sits at document level and the parser reads it only inside `TimeSeries` (`parsers.py:302`). |
| `quantity_mw` | `float` | No | `<quantity>` | Procured capacity in MW. |
| `market_agreement_type` | `str` | No | `<Type_MarketAgreement.Type>` | Default "" in canonical. `A01`=daily, `A02`=weekly, `A03`=monthly, `A04`=yearly. Empty on live responses: they spell the tag `type_MarketAgreement.type`, which the parser does not match (`parsers.py:320-326`). |
| `business_type` | `str` | No | `<businessType>` | Default "" in canonical. `B95` on every series in the live responses of 1 to 5 August 2026. |
| `resolution` | `str` | No | `<resolution>` | Default "" in canonical. |
| `published_at` | `datetime[UTC]` | Yes | `<createdDateTime>` | Document creation time, within seconds of the fetch (`h8_balancing.py:91`). |
| `data_provider` | `str` | No | derived | Default "entsoe" in canonical. |
| `ingested_at` | `datetime` | Yes | derived | Stamped at silver transform time (`h8_balancing.py:99`). |

### Silver sample

From the GB fixture; live responses do not parse this way (see Known issues).

```python
[
    {
        "timestamp_utc": datetime(2024, 1, 15, 0, 0, tzinfo=UTC),
        "area_code": "10YGB----------A",
        "quantity_mw": 500.0,
        "market_agreement_type": "A01",
        "business_type": "",
        "resolution": "PT60M",
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 5, 8, 18, 3, tzinfo=UTC),
    },
    {
        "timestamp_utc": datetime(2024, 1, 15, 1, 0, tzinfo=UTC),
        "area_code": "10YGB----------A",
        "quantity_mw": 525.0,
        "market_agreement_type": "A01",
        "business_type": "",
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

- **GB returns EMPTY.** Live curl on 2026-05-08 returned reason 999: `No matching data found for Data item PROCURED_BALANCING_CAPACITY_R3 [12.3.F] (10YGB----------A)...`. The ingest of 1 to 5 August 2026 got the same reason for GB and for IE-SEM (`10Y1001A1001A59C`).
- **Dedup includes `market_agreement_type`.** Multiple TimeSeries with the same `area_code` but different `Type_MarketAgreement.Type` (daily vs weekly procurement) coexist for the same timestamp. The dedup key `(timestamp_utc, area_code, market_agreement_type)` reflects this.
- **Silver collapses live responses to one row per quarter-hour.** With `area_code` and `market_agreement_type` both empty, the dedup key keeps one row per timestamp across every area, direction and series (`keep="last"`, `h8_balancing.py:104`). For 1 August 2026, the parser yields 8,020 points from the four populated responses; the dedup leaves 96 and the day window 88. Direction is parsed but is not in `output_cols` (`h8_balancing.py:172-182`); `mktPSRType.psrType` is not matched (the parser reads a nested `MktPSRType`, `parsers.py:345`); `procurement_Price.amount` is dropped because the transformer reads `quantity` only (`h8_balancing.py:32`).
- **Pagination stops after the first page.** The connector pages in steps of 4800 and stops at a page with fewer than 4800 series (`client.py:63`, `client.py:347`). Every populated A15 response of 1 to 5 August 2026 carried exactly 100 series and ended before the day did (DE-LU at 02:00 UTC), so the rest of each day was never requested.
- **22:00 to 24:00 UTC is lost every day.** Live documents run from 22:00 UTC to 22:00 UTC (the CEST day). The event-window filter (`EVENT_WINDOW_FILTER = True`, `h8_balancing.py:187`) keeps only points inside the requested UTC day, and the previous day's document ends at 22:00 UTC, so those eight quarter-hours land in no silver partition. The classification notes the upper edge as unobserved (`_event_window.py:515-519`).
- **`business_type` is `B95` throughout.** Every live series of 1 to 5 August 2026 carries `B95`, so it does not distinguish records; neither does `Type_MarketAgreement.Type` while it parses empty.

### Control-area vs cross-zonal

A15 is single-area only (`area_Domain`). The cross-zonal capacity
counterpart is A38, see
[cross_zonal_balancing_capacity.md](./cross_zonal_balancing_capacity.md).

---

## Implementation delta

- **Connector pages at the wrong step.** It sends `offset=0`, then steps by 4800 only when a page holds 4800 series (`client.py:347`); live A15 pages hold 100, so results cap at the first 100 series per area and day.
- **`Type_MarketAgreement.Type` filter is documented optional but the dedup key requires it to distinguish rows.** If a future call ever filters to a single agreement type, the dedup remains valid; if it does not filter, the response splits across multiple TimeSeries, but the parser does not read the live `type_MarketAgreement.type` spelling (`parsers.py:320-326`), so the value parses empty and the rows collapse.

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
