---
source: entsoe
dataset_key: total_capacity_allocated
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Capacity allocated and nominated
  summary: >-
    Cross-border capacity per border and direction, in MW: what earlier allocation rounds had
    already allocated, and what was then nominated.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A26, business types A29 and B08
    cadence: "Allocated: one value per day-long Period; nominated hourly or quarter-hourly, as received"
    grain: One row per interval start, `in_Domain` zone and `out_Domain` zone
  landscape: market
  what_it_is: >-
    In MW, per border and direction. Total capacity already allocated (Article 12.1.c) is what
    earlier allocation procedures allocated before an allocation. Total nominated capacity
    (12.1.b) is what was nominated per market time unit; GB replies carry three contract series,
    `A01`, `A06` and `A07`, and silver keeps only `A07`. Rows with `in_area_code` GB read as
    capacity into GB (project check).
  how_used:
    - Capacity into GB already allocated before each daily allocation, per border.
    - "Headroom: `net_transfer_capacity` minus capacity already allocated, hour by hour."
    - Hourly `A07` nominations on GB borders, set beside allocated capacity.
  chart:
    type: line
    silver: entsoe/total_capacity_allocated
    time: timestamp_utc
    value: quantity_mw
    filter:
      - {column: in_area_code, op: eq, value: "10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA"}
    group: out_area_code
    group_map:
      "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL": netherlands
      "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2": belgium
    series_order: [netherlands, belgium]
    aggregation: last
    window: {start: "2026-09-14", end: "2026-09-21"}
    unit: MW
  chart_view:
    title: Capacity already allocated into GB, 14 to 21 September 2026
    caption: >-
      Silver `entsoe/total_capacity_allocated` only, MW, rows with `in_area_code` GB, 14 to 21
      September 2026 UTC. Replies send one value per 22:00 to 22:00 UTC Period, which gridflow
      repeats hourly (curve type `A03`). Nominated capacity is in the notebook below.
    alt: >-
      Line chart of capacity already allocated into GB, from entsoe/total_capacity_allocated, in
      MW, hourly, 14 to 21 September 2026 UTC. From the Netherlands is 0 MW until 21:00 UTC on 19
      September, 850 MW from 22:00 that day, and 900 MW from 22:00 on 20 September to the end.
      From Belgium holds 725 MW until 21:00 UTC on 20 September and is 0 MW from 22:00.
    x_label: UTC; values step at 22:00 UTC
    key:
      - {series: netherlands, label: From the Netherlands, codes: "out_Domain NL", paint: petrol, note: "On the axis until 22:00 UTC, 19 September; replies carry auction category `A04` (hourly), not `A01` (base)."}
      - {series: belgium, label: From Belgium, codes: "out_Domain BE", paint: horizon}
  raw_feed:
    note: >-
      One GET per ordered pair per UTC day, eight pairs; nominated sends `businessType=B08`
      without the auction and contract parameters. EIC dashes shown as `%2D`. Same commands,
      name swapped.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A26&periodStart=202609200000&periodEnd=202609210000&in_Domain=10YGB%2D%2D%2D%2D%2D%2D%2D%2D%2D%2DA&out_Domain=10YNL%2D%2D%2D%2D%2D%2D%2D%2D%2D%2DL&businessType=A29&auction.Category=A01&contract_MarketAgreement.Type=A01&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe total_capacity_allocated --start 2026-09-14 --end 2026-09-22, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe total_capacity_allocated --start 2026-09-14 --end 2026-09-21, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: in_area_code, op: eq, value: "10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA"}
        - {column: timestamp_utc, op: in, value: ["2026-09-19T21:00:00Z", "2026-09-19T22:00:00Z", "2026-09-20T21:00:00Z", "2026-09-20T22:00:00Z"]}
      order_by: [out_area_code, timestamp_utc]
      columns: [timestamp_utc, in_area_code, out_area_code, quantity_mw, business_type, resolution, published_at]
    key: [timestamp_utc, in_area_code, out_area_code, business_type]
    caption: "Both GB pairs either side of 22:00 UTC, 19 and 20 September 2026."
    fields:
      timestamp_utc: "Interval start, UTC: period start plus (position minus 1) times resolution"
      in_area_code: "The `in_Domain` EIC; GB rows read as capacity into GB (project check)"
      out_area_code: "The `out_Domain` EIC, the zone across the border"
      quantity_mw: "MW as sent (`MAW`); an A03 point repeats until the next declared one"
      business_type: "`A29`, capacity already allocated; the nominated table carries `B08`"
      resolution: "Interval length as sent, `PT60M` in these rows; not normalised"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, within seconds of gridflow's request"
  notebook:
    lead: >-
      Reads `silver_entsoe_total_capacity_allocated` and `silver_entsoe_total_nominated_capacity`
      as pandas, filtered on `timestamp_utc`, both ends included; lineage dropped. Cells: Belgium
      into GB, nominated as the `A07` series. Allocated counts only earlier rounds (Art. 12(1)(c)),
      so `A07` can exceed it.
    cells:
      - |
        import pandas as pd
        cols = ["timestamp_utc", "in_area_code", "out_area_code", "quantity_mw"]
        alloc = data.entsoe.query("total_capacity_allocated", "2026-09-14", "2026-09-21")[cols]
        nom = data.entsoe.query("total_nominated_capacity", "2026-09-14", "2026-09-21")[cols]
      - |
        def be_to_gb(df):
            df = df[df.in_area_code.str.startswith("10YGB") & df.out_area_code.str.startswith("10YBE")]
            return df.set_index(df.timestamp_utc.dt.tz_convert("UTC")).quantity_mw.sort_index()
        both = pd.concat({"allocated": be_to_gb(alloc), "nominated_A07": be_to_gb(nom)}, axis=1)
        both.loc["2026-09-20 20:00":"2026-09-21 01:00"].reset_index()
      - |
        ax = both.plot(ylabel="MW", drawstyle="steps-post", figsize=(8, 3.5), color=["#155A6E", "#C77E3C"])
        ax.legend(loc="upper left", bbox_to_anchor=(1, 1));
    needs: both tables, 14 to 21 September 2026
    plot_alt: >-
      Step plot in MW for Belgium into GB, 14 to 21 September 2026 UTC. Allocated (petrol) holds
      725 MW, then 0 MW from 22:00 on 20 September. Nominated A07 (clay) swings between 0 and 1,055 MW
      (10:00 on 14 September), passes 725 MW on most days, and stays at 0 MW from 04:00 on 21
      September.
  related:
    - {dataset: entsoe/net_transfer_capacity, note: "Forecast transfer capacity for the same ordered pairs, not allocated or nominated"}
    - {dataset: entsoe/commercial_schedules, note: "Scheduled exchanges (document type A09) on the same ordered pairs"}
    - {dataset: entsoe/auction_revenue, note: "Revenue from explicit auctions on the same ordered pairs"}
    - {dataset: entsoe/cross_border_flows, note: "Physical flow on the same ordered pairs"}
  family:
    slug: capacity-allocated-nominated
    members:
      - dataset: total_capacity_allocated
        differs: "Business type `A29`, contract type `A01` (daily): one value per Period, as sent"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A26&periodStart=202609200000&periodEnd=202609210000&in_Domain=10YGB%2D%2D%2D%2D%2D%2D%2D%2D%2D%2DA&out_Domain=10YNL%2D%2D%2D%2D%2D%2D%2D%2D%2D%2DL&businessType=A29&auction.Category=A01&contract_MarketAgreement.Type=A01&securityToken=$ENTSOE_API_KEY"
      - dataset: total_nominated_capacity
        differs: "`B08`, hourly or quarter-hourly; silver keeps `A07` of three contract series (`A01`, `A06`, `A07`)"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A26&periodStart=202609200000&periodEnd=202609210000&in_Domain=10YGB%2D%2D%2D%2D%2D%2D%2D%2D%2D%2DA&out_Domain=10YBE%2D%2D%2D%2D%2D%2D%2D%2D%2D%2D2&businessType=B08&securityToken=$ENTSOE_API_KEY"
---

# ENTSO-E — Total Capacity Already Allocated (A26, businessType=A29)

## Overview

Total cross-zonal capacity already allocated through past auctions, in MW
per zone-pair. Article 12.1.C of Regulation (EC) 543/2013. Sister A26
dataset to `total_nominated_capacity`. Used to assess what slice of NTC has
been pre-committed via long-term auctions before each daily clearing.

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
| documentType | `A26` |
| processType | (none) |
| businessType | `A29` (capacity already allocated) |
| `auction.Category` (lowercase) | `A01` |
| `contract_MarketAgreement.Type` (lowercase) | `A01` (daily) |
| domain-param-name | `in_Domain` + `out_Domain` (zone_pair) |

### Cross-zonal parameters

A26/A29 is directional. Default UK-centric pairs.

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | Yes | API key | UUID |
| `documentType` | str | Yes | `A26` | `A26` |
| `businessType` | str | Yes | `A29` | `A29` |
| `auction.Category` | str | Yes | `A01` (lowercase) | `A01` |
| `contract_MarketAgreement.Type` | str | Yes | `A01` (lowercase) | `A01` |
| `in_Domain` | str | Yes | Receiving zone EIC (project check: `in_Domain` GB reads as into GB; see `total_nominated_capacity`) | `10YGB----------A` |
| `out_Domain` | str | Yes | Sending zone EIC | `10YFR-RTE------C` |
| `periodStart` / `periodEnd` | str | Yes | UTC | |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -o "/tmp/entsoe-total_capacity_allocated.xml" \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A26&businessType=A29&auction.Category=A01&contract_MarketAgreement.Type=A01&in_Domain=10YGB----------A&out_Domain=10YFR-RTE------C&periodStart=202605060000&periodEnd=202605070000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/total_capacity_allocated/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per (border, day).

### Bronze sample

Live 2026-05-08 GB→FR daily and 30-day: Acknowledgement, Reason 999 —
`TOTAL_CAPACITY_ALLOCATED [12.1.C] (10YGB----------A, 10YFR-RTE------C)`.
Populated payload (bronze GB/NL reply for 2026-09-20, `raw_20260926T180334Z_aea3bdbf.xml`):
`Publication_MarketDocument` with one TimeSeries: `auction.type` `A02`,
`auction.category` `A04` (the request sends `auction.Category=A01`; the GB/BE, FR/BE,
FR/DE-LU, NL/DE-LU and NL/BE replies echo `A01`), `businessType` `A29`,
`contract_MarketAgreement.type` `A01`, `curveType` `A03`, `PT60M`. The reply to a
00:00 to 00:00 UTC request carries two Periods, 2026-09-19T22:00Z to 2026-09-20T22:00Z and
2026-09-20T22:00Z to 2026-09-21T22:00Z, each with one Point (position 1: 850, then 900 MW).
The A03 parser repeats that point for every hour of the Period (`parsers.py:582-600`), and the
event-window filter keeps only the request's UTC day (`h6_market.py:228`).

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/total_capacity_allocated/year=YYYY/month=MM/total_capacity_allocated_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h6_market.TotalCapacityAllocatedTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeTransmissionMarketQuantity`
**Dedup key**: `(timestamp_utc, in_area_code, out_area_code, business_type)`
**Point-in-time field**: `none`

### Silver schema

H6 quantity envelope (same fields as `total_nominated_capacity`), including
`published_at` (`h6_market.py:105,114`), the response `createdDateTime`.

### Silver sample

A real row from silver. It replaces a GB→FR 1500 MW example that matched no reply: this
note's own 2026-05-08 probe found GB→FR empty.

```python
[
    {
        "timestamp_utc": "2026-09-19T22:00:00Z",
        "in_area_code": "10YGB----------A",
        "out_area_code": "10YNL----------L",
        "quantity_mw": 850.0,
        "business_type": "A29",
        "resolution": "PT60M",
        "published_at": "2026-09-26T18:02:31Z",
        "data_provider": "entsoe",
        "ingested_at": "2026-09-26T18:04:01.515918Z",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Lowercase `auction.Category`** vs the otherwise capitalised
  `Auction.Category` of `transfer_capacity_use`. ENTSO-E parameter casing is
  inconsistent across articles — copy from the connector.
- Allocation publications are sparse: of the eight ordered pairs gridflow requests,
  GB/FR and GB/IE-SEM return Acknowledgements, while GB/NL and GB/BE return
  `Publication_MarketDocument`s (bronze, 2026-08 and 2026-09 replies). The cause of the
  empty borders is not documented.
- Definition (Regulation (EU) 543/2013 Art. 12(1)(c)): "prior to each capacity
  allocation the total capacity already allocated through previous allocation
  procedures per market time unit and per direction"; published "at the latest when
  publication of offered capacity figures become due" (Art. 12(2)).

---

## Implementation delta

- **Tuple recorded:** `(documentType=A26, processType=none, businessType=A29, auction.Category=A01, contract_MarketAgreement.Type=A01, domain=in_Domain+out_Domain)`. Matches code — the `total_capacity_allocated` entry in `endpoints.py` `DOC_TYPES`.
- **Live validation 2026-05-08 GB→FR daily and 30-day:** Acknowledgement, Reason 999. **EMPTY** for GB→FR. The cause recorded then ("post-Brexit GB borders publish no long-term allocation") is contradicted by bronze: GB/NL and GB/BE return `Publication_MarketDocument` in 14 of 14 files each (2026-08 and 2026-09). The cause of the empty GB/FR border is undocumented.
- **Disambiguation from sister A26 `total_nominated_capacity`:**
  - `total_nominated_capacity`: `businessType=B08`, no auction.Category, no contract.
  - **`total_capacity_allocated`** (this page): `businessType=A29` + `auction.Category=A01` (lowercase) + `contract_MarketAgreement.Type=A01` (lowercase).

---

## Modelling notes

- Pair with `total_nominated_capacity` and NTC (`net_transfer_capacity`) to
  compute headroom: `headroom = NTC − allocated`. Used as a feature for
  day-ahead intraday transition (residual capacity available to ID).

---

## Links

- [Official API docs (PDF)](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/h6_market.py`
- `src/gridflow/schemas/entsoe.py`
