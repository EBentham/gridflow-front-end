---
source: entsoe
dataset_key: total_nominated_capacity
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSO-E — Total Nominated Capacity (A26, businessType=B08)

## Overview

Total commercial capacity nominated by market participants per zone-pair.
Article 12.1.B of Regulation (EC) 543/2013. Distinct from
`commercial_schedules` (A09) in that A26/B08 is the *aggregated nominated
total* (a sum over participants) at the auction-product level. One of two
A26-document variants. Used in capacity-utilisation models alongside A09.

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
| Publication lag  | No later than one hour after each round of nomination (Regulation (EU) 543/2013 Art. 12(2)) |
| Response format  | XML |

### ENTSO-E parameter tuple (validation criterion)

| Field | Value |
|-------|-------|
| documentType | `A26` |
| processType | (none) |
| businessType | `B08` (total nominated capacity) |
| `contract_MarketAgreement.Type` | (not in request; GB replies carry three TimeSeries, `A01`, `A06`, `A07`: see Known issues) |
| domain-param-name | `in_Domain` + `out_Domain` (zone_pair) |

### Cross-zonal parameters

A26/B08 is directional. Default UK-centric pairs.

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | Yes | API key | UUID |
| `documentType` | str | Yes | `A26` | `A26` |
| `businessType` | str | Yes | `B08` | `B08` |
| `in_Domain` | str | Yes | Receiving zone EIC (project check: GB/FR, GB/NL and GB/BE rows track `cross_border_flows` into GB, hourly correlation 0.88 to 0.93, 2026-08 and 2026-09) | `10YGB----------A` |
| `out_Domain` | str | Yes | Sending zone EIC | `10YFR-RTE------C` |
| `periodStart` / `periodEnd` | str | Yes | UTC | |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -o "/tmp/entsoe-total_nominated_capacity.xml" \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A26&businessType=B08&in_Domain=10YGB----------A&out_Domain=10YFR-RTE------C&periodStart=202605060000&periodEnd=202605070000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/total_nominated_capacity/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per (border, day).

### Bronze sample

```xml
<?xml version="1.0" encoding="utf-8"?>
<Publication_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0">
  <mRID>b0ce3ea9d6484aeeb014676a3e30e644</mRID>
  <type>A26</type>
  <createdDateTime>2026-05-08T18:06:25Z</createdDateTime>
  <period.timeInterval>
    <start>2026-05-06T00:00Z</start>
    <end>2026-05-07T00:00Z</end>
  </period.timeInterval>
  <TimeSeries>
    <mRID>1</mRID>
    <businessType>B08</businessType>
    <in_Domain.mRID codingScheme="A01">10YGB----------A</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YFR-RTE------C</out_Domain.mRID>
    <contract_MarketAgreement.type>A01</contract_MarketAgreement.type>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <curveType>A03</curveType>
    <Period>
      <timeInterval>
        <start>2026-05-06T00:00Z</start>
        <end>2026-05-07T00:00Z</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>3028</quantity></Point>
      <Point><position>6</position><quantity>2928</quantity></Point>
      <Point><position>22</position><quantity>2029</quantity></Point>
    </Period>
  </TimeSeries>
</Publication_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/total_nominated_capacity/year=YYYY/month=MM/total_nominated_capacity_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h6_market.TotalNominatedCapacityTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeTransmissionMarketQuantity`
**Dedup key**: `(timestamp_utc, in_area_code, out_area_code, business_type)`
**Point-in-time field**: `none`

### Silver schema

H6 quantity envelope: `timestamp_utc`, `in_area_code`, `out_area_code`,
`quantity_mw`, `business_type`, `resolution`, `published_at` (response
`createdDateTime`, `h6_market.py:105,114`), `data_provider`, `ingested_at`.
No contract-type column: see Known issues.

### Silver sample

Unverified: 3028 and 2928 MW are the first TimeSeries in the 2026-05-06 bronze sample above.
Silver keeps the last-listed series (`A07` in the 2026-08 and 2026-09 replies; see Known
issues), so real silver rows for that day may differ. No May bronze or silver is held to check.

```python
[
    {
        "timestamp_utc": "2026-05-06T00:00:00Z",
        "in_area_code": "10YGB----------A",
        "out_area_code": "10YFR-RTE------C",
        "quantity_mw": 3028.0,
        "business_type": "B08",
        "resolution": "PT60M",
        "data_provider": "entsoe",
        "ingested_at": "2026-05-08T18:05:30Z",
    },
    {
        "timestamp_utc": "2026-05-06T05:00:00Z",
        "in_area_code": "10YGB----------A",
        "out_area_code": "10YFR-RTE------C",
        "quantity_mw": 2928.0,
        "business_type": "B08",
        "resolution": "PT60M",
        "data_provider": "entsoe",
        "ingested_at": "2026-05-08T18:05:30Z",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- A26/B08 returns *aggregated* nominations — sum across all explicit auction
  holders, not per-holder data.
- Definition (Regulation (EU) 543/2013 Art. 12(1)(b)): "for every market time unit and
  per direction between bidding zones the total capacity nominated".
- `<contract_MarketAgreement.type>` is not in the request. Each GB/FR, GB/NL and GB/BE
  reply carries three TimeSeries, same `in_Domain`/`out_Domain`, contract types `A01`,
  `A06` and `A07` in that order (Daily, Long term, Intraday in entsoe-py's
  `MARKETAGREEMENTTYPE` map; not checked against an ENTSO-E code list). FR/DE-LU replies
  carry `A07` only, at `PT15M`. Bronze, 2026-08 and 2026-09 replies.
- **Silver keeps one contract series (gridflow defect).** The parser does not return the
  contract type and the dedup key is `(timestamp_utc, in_area_code, out_area_code,
  business_type)` with `keep="last"` (`h6_market.py:91-99`), so the `A01` and `A06` rows
  are dropped and silver holds the `A07` series: equal to it in every hour checked on the
  three GB pairs (2026-08 and 2026-09), and equal hour for hour to `commercial_schedules`
  on those pairs.
- `curveType=A03` returns sparse positions (compressed-resolution); the parser fills
  them, repeating each declared point until the next one to the Period end
  (`parsers.py:533-600`), so silver has a row for every interval.

---

## Implementation delta

- **Tuple recorded:** `(documentType=A26, processType=none, businessType=B08, domain=in_Domain+out_Domain)`. Matches code — the `total_nominated_capacity` entry in `endpoints.py` `DOC_TYPES`.
- **Live validation 2026-05-08 GB→FR for 2026-05-06:** `Publication_MarketDocument` with 3 TimeSeries (one per nominated MarketAgreement / direction split; in the 2026-08 and 2026-09 replies the three are contract types `A01`, `A06`, `A07`, same direction), variable-resolution points, MW values 2029-3028 across 24h. **PASS**.
- **Disambiguation from sister A26 `total_capacity_allocated`** (this is critical because both share `documentType=A26`):
  - **`total_nominated_capacity`** (this page): `businessType=B08`, no `auction.Category`, no `contract_MarketAgreement.Type` in request.
  - `total_capacity_allocated`: `businessType=A29` + `auction.Category=A01` + `contract_MarketAgreement.Type=A01`.

---

## Modelling notes

- Pair with `total_capacity_allocated` to compute
  `nomination_ratio = nominated / allocated`. Above 100% is not a data flag:
  allocated (Art. 12(1)(c)) counts only capacity from allocation procedures before an
  allocation, while nominations follow later rounds too. Silver's GB/BE nominated `A07`
  series exceeds allocated (725 MW) in some hours of 2026-09-14 to 2026-09-20.
- Useful as a feature for capacity-rights utilisation models.

---

## Links

- [Official API docs (PDF)](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/h6_market.py`
- `src/gridflow/schemas/entsoe.py`
