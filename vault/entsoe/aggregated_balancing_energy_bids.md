---
source: entsoe
dataset_key: aggregated_balancing_energy_bids
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSO-E — Aggregated balancing energy bids (A24 / A51)

## Overview

Aggregate (TSO-side, summed-across-bidders) balancing energy bid
volumes for a control area. Where
[balancing_energy_bids.md](./balancing_energy_bids.md) gives you one
TimeSeries per bidder, A24 collapses to one TimeSeries per
(direction, product) — reflecting the total MW the TSO sees offered
into its reserve activation pool at each timestamp.

This is the dataset to use for capacity-stack-style modelling, gross
balancing supply curves, and pre-activation reserve adequacy. For
post-activation outcomes use the H7 activated balancing prices/quantity
datasets.

A24 is paired with `processType=A51` (aggregated balancing). H8 spec
uses `area_Domain` (singular control area), with the response carrying
`<area_Domain.mRID>` rather than `connecting_Domain`.

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
| Pagination       | None — A24 aggregate is small (one TimeSeries per direction/product). |
| Historical depth | TODO — H8 catalogue, varies by area. GB has no published data. |
| Publication lag  | After interval close (typically same-day for ISP-resolution markets). |
| Response format  | XML (`Balancing_MarketDocument`) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | string | Yes | `A24` | `A24` |
| `processType` | string | Yes | `A51` (aggregated) | `A51` |
| `area_Domain` | string (EIC) | Yes | Control area EIC. **Not** `controlArea_Domain`. | `10YGB----------A` |
| `periodStart` | string | Yes | UTC `yyyyMMddHHmm` | `202605070000` |
| `periodEnd` | string | Yes | UTC `yyyyMMddHHmm`, max 1 day | `202605080000` |
| `securityToken` | string | Yes | API key | `<UUID>` |

ENTSOE tuple: `(documentType=A24, processType=A51, businessType=n/a, area-param-name=area_Domain)`. The TimeSeries response itself carries `<businessType>` and `<flowDirection.direction>` per series, but neither is a query input — they classify each returned series. Live BE responses (22 to 25 Sep 2026) send `businessType` `A14`, not `B74`.

### Working curl example

```bash
curl --ssl-no-revoke -fsS -H "Accept: application/xml" \
  "https://web-api.tp.entsoe.eu/api?documentType=A24&processType=A51&area_Domain=10YGB----------A&periodStart=202605070000&periodEnd=202605080000&securityToken=${ENTSOE_API_KEY}" \
  -o /tmp/entsoe-aggregated_balancing_energy_bids.xml \
  -w "HTTP %{http_code} | %{size_download} bytes\n"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/aggregated_balancing_energy_bids/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML.
**Granularity**: One file per zone in `DEFAULT_ZONES` (GB, FR, NL, BE, DE-LU, IE-SEM) per UTC day (`client.py:249`, `endpoints.py:395`). No `offset`: the doc type declares no optional params (`endpoints.py:348-353`).

> **Live shape (BE, 22 to 25 Sep 2026, fetched 2026-09-27; read 2026-09-29).** Only BE
> published: GB, FR, NL, DE-LU and IE-SEM returned code 999 on all four days, and all six zones
> returned code 999 for 1 to 5 Aug 2026. The populated `Balancing_MarketDocument` carries
> `area_Domain.mRID` **at document level** (a child of the root, beside `period.timeInterval`
> 00:00Z to 00:00Z, the UTC day), not inside the TimeSeries as in the fixture below. It has two
> TimeSeries, `mRID` `1` (`flowDirection.direction` `A02`) and `2` (`A01`), each with
> `businessType` `A14`, `standard_MarketProduct.marketProductType` `A01`,
> `quantity_Measure_Unit.name` `MAW`, `curveType` `A03` and one PT15M Period over the day
> (83 to 95 declared points per series, forward-filled to 96 by the parser).

### Bronze sample

From `tests/fixtures/entsoe/aggregated_balancing_energy_bids_gb.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Balancing_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:balancingdocument:4:0">
  <mRID>fixture-aggregated-balancing-energy-bids-gb-20240115</mRID>
  <revisionNumber>1</revisionNumber>
  <type>A24</type>
  <process.processType>A51</process.processType>
  <TimeSeries>
    <mRID>aggregated-bid-1</mRID>
    <businessType>B74</businessType>
    <area_Domain.mRID codingScheme="A01">10YGB----------A</area_Domain.mRID>
    <Period>
      <timeInterval>
        <start>2024-01-15T00:00Z</start>
        <end>2024-01-15T02:00Z</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>92</quantity></Point>
      <Point><position>2</position><quantity>87</quantity></Point>
    </Period>
  </TimeSeries>
</Balancing_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/aggregated_balancing_energy_bids/year=YYYY/month=MM/aggregated_balancing_energy_bids_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h8_balancing.AggregatedBalancingEnergyBidsTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeBalancingEnergyBid` (shared with bid-level)
**Dedup key**: `(timestamp_utc, area_code, bid_mrid, direction)`
**Point-in-time field**: `published_at`, the document `createdDateTime` (`h8_balancing.py:91`), a fetch-time stamp within seconds of the request.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | derived (Period start + (position - 1) × resolution, `parsers.py:530`; A03 forward-fill) | UTC-aware. |
| `area_code` | `str` | No | `area_Domain.mRID` | Renamed from `area_domain`. **Empty on live responses**: the vendor sends `area_Domain.mRID` at document level, and the parser reads it only among TimeSeries children (`parsers.py:302`; `_root_document_metadata`, `parsers.py:121-145`, ignores it). |
| `quantity_mw` | `float` | No | `<quantity>` | Aggregated bid volume in MW (`MAW`). |
| `business_type` | `str` | No | `<businessType>` | Default "" in canonical. `A14` in live BE responses. |
| `bid_mrid` | `str` | No | `TimeSeries/<mRID>` | Default "" in canonical. Aggregated TimeSeries identifier (not a bidder identity): `1` and `2` in each live document. |
| `direction` | `str` | No | `<flowDirection.direction>` (when present) | Default "" in canonical. `A01`/`A02`; present on both live series. |
| `original_market_product` | `str` | No | (rare in aggregate) | Default "" in canonical. Empty in live BE responses. |
| `standard_market_product` | `str` | No | `standard_MarketProduct.marketProductType` | Default "" in canonical. `A01` in live BE responses. |
| `resolution` | `str` | No | `<resolution>` | Default "" in canonical. `PT15M` live. |
| `published_at` | `datetime[UTC]` | Yes | document `createdDateTime` | Fetch-time stamp (`h8_balancing.py:91`). |
| `data_provider` | `str` | No | derived | Default "entsoe" in canonical. |
| `ingested_at` | `datetime` | Yes | derived | Stamped at silver transform time (`h8_balancing.py:99`). |

### Silver sample

From the GB fixture (GB publishes nothing live):

```python
[
    {
        "timestamp_utc": datetime(2024, 1, 15, 0, 0, tzinfo=UTC),
        "area_code": "10YGB----------A",
        "quantity_mw": 92.0,
        "business_type": "B74",
        "bid_mrid": "aggregated-bid-1",
        "direction": "",
        "original_market_product": "",
        "standard_market_product": "",
        "resolution": "PT60M",
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 5, 8, 18, 3, tzinfo=UTC),
    },
    {
        "timestamp_utc": datetime(2024, 1, 15, 1, 0, tzinfo=UTC),
        "area_code": "10YGB----------A",
        "quantity_mw": 87.0,
        "business_type": "B74",
        "bid_mrid": "aggregated-bid-1",
        "direction": "",
        "original_market_product": "",
        "standard_market_product": "",
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

- **GB returns EMPTY.** Live curl on 2026-05-08 returned reason 999: `No matching data found for Data item AGGREGATED_BALANCING_ENERGY_BIDS_R3 [12.3.E] (10YGB----------A)...`.
- **DE-LU also returned EMPTY** on a 2026-08-03 live probe for 2026-06-01 — a 967-byte `Acknowledgement_MarketDocument`, reason 999, same `No matching data found` text. So the empty response is not GB-specific. Probe saved at gridflow `.planning/phases/R3-test-integrity/probes/entsoe_A24_aggregated_balancing_energy_bids_DE_20260601.xml`.
- **A24 is NOT affected by the A37 envelope defect** — checked, not assumed (gridflow v0.18 R4-b, 2026-08-16). The sibling `balancing_energy_bids` (A37) returns `ReserveBid_MarketDocument`/`Bid_TimeSeries` and was parsing to zero rows silently until fixed; A24's probe contains **zero `TimeSeries`-like elements of any name**, because it returned no data at all. Scope of that fix was therefore one dataset, not two. **Update 2026-09-29:** a populated A24 envelope is now held (BE, 22 to 25 Sep 2026; see the live-shape note under Bronze layer): `Balancing_MarketDocument`/`TimeSeries`/`quantity`, which the parser reads. The bronze sample below is still the fixture.
- **`area_code` is empty in silver (gridflow defect).** Live A24 puts `area_Domain.mRID` at document level; the parser only reads it inside TimeSeries (`parsers.py:302`). All 768 silver rows (BE, 22 to 25 Sep 2026) have `area_code == ""`. Values are otherwise exactly the bronze re-parse. Latent: the dedup key `(timestamp_utc, area_code, bid_mrid, direction)` would merge zones the day a second zone publishes, since every document numbers its series `1` and `2`. Same root cause as `procured_balancing_capacity` and `current_balancing_state`.
- **Only BE publishes here.** GB, FR, NL, DE-LU and IE-SEM returned code 999 for every request in 22 to 25 Sep 2026; BE also returned 999 for 1 to 5 Aug 2026.
- **Direction may be missing in TimeSeries.** Aggregated responses sometimes split direction into two TimeSeries (one per direction) and sometimes emit a single TimeSeries without a direction tag. The schema's `direction` defaults to empty rather than NULL — model code should treat `""` as "all directions / unknown". (Live BE responses send two series, one per direction.)
- **Shared schema with bid-level dataset.** The same `EntsoeBalancingEnergyBid` Pydantic schema is reused. Live BE responses leave `original_market_product` empty and send `standard_market_product` `A01`.
- **Stale classification.** `_event_window.py:910-936` records A24 as UNKNOWN, "never observed populated"; BE is now populated, with documents aligned to the UTC day (00:00Z to 00:00Z), so no rows fall outside the transform day.

### Control-area vs cross-zonal

A24 is single-area (`area_Domain`) — aggregated within one control
area. For cross-zonal balancing capacity (capacity reserved on
interconnectors), use
[cross_zonal_balancing_capacity.md](./cross_zonal_balancing_capacity.md).

---

## Implementation delta

- **Schema reuse:** Shared `EntsoeBalancingEnergyBid` schema with bid-level dataset; no aggregate-specific schema. This keeps types consistent but means the silver row carries unused empty fields. Acceptable; track as a refactor candidate, not a bug.
- **No `businessType` in query, despite presence in fixture.** The endpoint registry lists no `extra_params` for A24 — query is sent without `businessType`. Fixture and live response both contain `<businessType>B74</businessType>` per TimeSeries. ENTSOE accepts the call without `businessType` because A24/A51 has only one valid business type.

---

## Modelling notes

- Capacity-stack feature for balancing-market price models (gross supply at each timestamp).
- Useful for **balancing-supply scarcity** signals — sudden drops in aggregated offered MW typically precede price spikes.
- Lower cardinality than bid-level; preferred when a model's feature pipeline cannot accommodate per-bidder data.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf) — Section 17 / 12.3.E
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py` — `aggregated_balancing_energy_bids`
- `src/gridflow/silver/entsoe/h8_balancing.py` — `AggregatedBalancingEnergyBidsTransformer`
- `src/gridflow/schemas/entsoe.py` — `EntsoeBalancingEnergyBid`
- `tests/fixtures/entsoe/aggregated_balancing_energy_bids_gb.xml`
- [Bid-level counterpart](./balancing_energy_bids.md)
