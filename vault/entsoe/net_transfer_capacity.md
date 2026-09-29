---
source: entsoe
dataset_key: net_transfer_capacity
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Day-ahead net transfer capacity
  summary: >-
    ENTSO-E's forecast of how much power may be exchanged across a border, in MW, one direction
    per series, for the daily product.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A61, contract type A01 (daily)
    cadence: Hourly points (`PT60M`) in the responses received, one document per pair per UTC day
    grain: One row per interval start, `in_Domain` zone and `out_Domain` zone
  landscape: market
  what_it_is: >-
    ENTSO-E's forecast transfer capacity across a border in one direction, for the daily product:
    capacity forecast for commercial exchange, not what was allocated or nominated. Of the
    eight ordered pairs gridflow requests, FR to BE and FR to DE-LU returned "No matching data
    found" in the responses received.
    Rows with `in_area_code` GB read as capacity into GB (project check).
  how_used:
    - Import capacity into GB on each border, hour by hour, for the next day.
    - "Set against `cross_border_flows` to see how close physical flow runs to capacity."
    - "A feature for spread models: capacity cuts on a border, and when they end."
  chart:
    type: line
    silver: entsoe/net_transfer_capacity
    time: timestamp_utc
    value: ntc_mw
    filter:
      - {column: in_area_code, op: eq, value: "10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA"}
    group: out_area_code
    group_map:
      "10YFR\x2DRTE\x2D\x2D\x2D\x2D\x2D\x2DC": france
      "10Y1001A1001A59C": ireland
      "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2": belgium
      "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL": netherlands
    series_order: [france, ireland, belgium, netherlands]
    aggregation: last
    window: {start: "2026-09-08", end: "2026-09-21"}
    unit: MW
  chart_view:
    title: Capacity into GB by border, 8 to 21 September 2026
    caption: >-
      Silver `entsoe/net_transfer_capacity`, MW, hourly as sent, the four series with
      `in_area_code` GB, 8 to 21 September 2026 UTC. Each declared point holds until the next
      (curve type A03). Forecast capacity, not flow; the two NL pairs are not drawn.
    alt: >-
      Line chart from entsoe/net_transfer_capacity, MW, hourly capacity into GB by border, 8 to 21
      September 2026 UTC. France is 4,028 until 06:00 on the 9th, then 3,028. Ireland
      (SEM) is 400 until the 13th, then 1,413, dipping to 913 from 15:00 to 20:00 on the 14th.
      Belgium sits at 1,012, at 1,032 from 08:00 to 12:00 most days, dips to 750 on the 8th and
      804 on the 18th, and is zero from 05:00 on the 21st. The Netherlands is zero until 22:00
      on the 19th, then 1,016.
    x_label: UTC date; hourly points
    key:
      - {series: france, label: From France, codes: "out_Domain FR", paint: petrol, note: "4,028 MW until 06:00 UTC on the 9th, then 3,028 to the window's end."}
      - {series: ireland, label: From Ireland (SEM), codes: "out_Domain IE-SEM", paint: clay, note: "400 MW until 00:00 UTC on the 13th, then 1,413; 913 from 15:00 to 20:00 on the 14th."}
      - {series: belgium, label: From Belgium, codes: "out_Domain BE", paint: horizon, note: "1,012 MW, 1,032 from 08:00 to 12:00 UTC most days; zero from 05:00 on the 21st."}
      - {series: netherlands, label: From the Netherlands, codes: "out_Domain NL", paint: olive, note: "Zero until 22:00 UTC on the 19th, then 1,016 MW."}
  raw_feed:
    note: >-
      One GET per ordered zone pair per UTC day, eight pairs, with the daily contract type fixed.
      `gridflow ingest` stores each reply in bronze; `gridflow transform` parses it to silver.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A61&periodStart=202609190000&periodEnd=202609200000&in_Domain=10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA&out_Domain=10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL&contract_MarketAgreement.Type=A01&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe net_transfer_capacity --start 2026-09-08 --end 2026-09-22, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe net_transfer_capacity --start 2026-09-08 --end 2026-09-21, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: in_area_code, op: eq, value: "10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA"}
        - {column: out_area_code, op: eq, value: "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL"}
        - {column: timestamp_utc, op: ge, value: "2026-09-19T18:00:00Z"}
        - {column: timestamp_utc, op: le, value: "2026-09-20T01:00:00Z"}
      order_by: [timestamp_utc]
      columns: [timestamp_utc, ntc_mw, in_area_code, out_area_code, published_at, resolution]
    key: [timestamp_utc, in_area_code, out_area_code]
    caption: "GB from NL, hourly, 18:00 UTC on 19 September to 01:00 on the 20th."
    fields:
      timestamp_utc: "Interval start, UTC: period start plus (position minus one) times resolution"
      ntc_mw: "Forecast capacity in MW as sent (`MAW`); an A03 point holds until the next"
      in_area_code: "The `in_Domain` EIC; GB rows read as capacity into GB (project check)"
      out_area_code: "The `out_Domain` EIC, the zone on the other side of the border"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, not the forecast's issue time"
      resolution: "Interval length code as sent, for example `PT60M`; not normalised"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_entsoe_net_transfer_capacity`, filtered on
      `timestamp_utc` with both ends included. Lineage columns are dropped and rows come ordered by
      `timestamp_utc` only, so sort before pivoting.
    cells:
      - |
        df = data.entsoe.query("net_transfer_capacity", "2026-09-08", "2026-09-21")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
        df = df.sort_values(["timestamp_utc", "in_area_code", "out_area_code"])
      - df.groupby(["in_area_code", "out_area_code"])["ntc_mw"].agg(["min", "max", "count"]).reset_index()
      - |
        gb = df[df["in_area_code"].str.startswith("10YGB")].copy()
        gb["border"] = gb["out_area_code"].str[3:5].replace({"10": "IE-SEM"})  # IE-SEM's EIC has no letters there
        wide = gb.pivot(index="timestamp_utc", columns="border", values="ntc_mw")
        wide[["FR", "IE-SEM", "BE", "NL"]].plot(ylabel="MW", drawstyle="steps-post", color=["#155A6E", "#C77E3C", "#3E8C97", "#66793B"], figsize=(8, 3.5))
    needs: 8 to 21 September 2026
    plot_alt: >-
      Step plot of ntc_mw into GB by border, 8 to 21 September 2026 UTC. FR drops from 4,028 to
      3,028 MW on the 9th; IE-SEM rises from 400 to 1,413 on the 13th; BE holds near 1,012 to
      1,032 and falls to zero on the 21st; NL is zero until late on the 19th, then 1,016.
  related:
    - {dataset: entsoe/cross_border_flows, note: "Physical flow on the same ordered pairs, to set against capacity"}
    - {dataset: entsoe/total_capacity_allocated, note: "Capacity already allocated in auctions on these pairs, not the forecast"}
    - {dataset: entsoe/dc_link_intraday_transfer_limits, note: "Intraday transfer limits on the same ordered pairs"}
    - {dataset: entsoe/day_ahead_prices, note: "Prices at the continental and Irish ends; none for GB"}
---

# ENTSO-E — Forecasted Net Transfer Capacity (A61, day-ahead)

## Overview

Day-ahead Net Transfer Capacity (NTC) per zone-pair, in MW. Article 11.1
of Regulation (EC) 543/2013 — the maximum forecast commercial exchange
capacity offered to the market for the trading day. Published by TSOs
typically D-1 around mid-day after capacity calculation. Used in spread
models (NTC is the upper bound on commercial flow) and as an input to
congestion forecasts.

→ Domain: [Net transfer capacity](../../../20-domain/markets/net-transfer-capacity.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://web-api.tp.entsoe.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | Query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | 1 req/s default, back off on 429 |
| Pagination       | None |
| Historical depth | 2014-12-05 onward, border-dependent |
| Publication lag  | D-1 mid-day |
| Response format  | XML (`Publication_MarketDocument`) |

### ENTSO-E parameter tuple (validation criterion)

| Field | Value |
|-------|-------|
| documentType | `A61` |
| processType | (none) |
| businessType (request) | (none — server returns `A27` on TimeSeries) |
| `contract_MarketAgreement.Type` | `A01` (daily) — **required by code** as a fixed extra param |
| domain-param-name | `in_Domain` + `out_Domain` (zone_pair) |

### Cross-zonal parameters

A61 is directional. Same border-pair table as A11 cross_border_flows:
gridflow sends the eight `_FLOW_PAIRS` (in, out) of `connectors/entsoe/client.py:40-49`
(GB-FR, GB-NL, GB-BE, GB-IE-SEM, FR-BE, FR-DE-LU, NL-DE-LU, NL-BE) and never the
reverse. For FR-BE and FR-DE-LU every response received (42 of 42, over 19 days:
2026-08-01 to 2026-08-05 and 2026-09-08 to 2026-09-21, with 13 and 14 September
fetched twice) is a Reason 999 acknowledgement, "No matching data found for Data item
FORECASTED_TRANSFER_CAPACITIES_EXPLICIT [11.1]", so silver holds six pairs. Project
check 2026-09-29: on the GB-FR, GB-BE and GB-NL pairs, hourly `cross_border_flows`
flow into GB (same in/out) tops out at about these NTC values, so `in_Domain` reads
as the receiving zone (GB-IE-SEM flow stays far below NTC, so it neither confirms nor
contradicts); ENTSO-E's own definition is not quoted here.

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | Yes | API key | UUID |
| `documentType` | str | Yes | `A61` | `A61` |
| `contract_MarketAgreement.Type` | str | Yes | `A01` (daily product) | `A01` |
| `in_Domain` | str | Yes | EIC | `10YGB----------A` |
| `out_Domain` | str | Yes | EIC | `10YFR-RTE------C` |
| `periodStart` / `periodEnd` | str | Yes | `yyyymmddHHMM` UTC | |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -o "/tmp/entsoe-net_transfer_capacity.xml" \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A61&contract_MarketAgreement.Type=A01&in_Domain=10YGB----------A&out_Domain=10YFR-RTE------C&periodStart=202605060000&periodEnd=202605070000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/net_transfer_capacity/<year>/<month>/<day>/raw_<YYYYMMDDTHHMMSSZ fetch time>_<sha256[:8]>.xml`, plus a `.meta.json` sidecar (`bronze/writer.py:33-34,56`)
**Format**: Raw XML, immutable.
**Granularity**: One file per (in_Domain, out_Domain, day).

### Bronze sample

```xml
<?xml version="1.0" encoding="utf-8"?>
<Publication_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0">
  <mRID>67c3c08a2dbf4c1bbaa1a114f52eed6a</mRID>
  <type>A61</type>
  <createdDateTime>2026-05-08T18:05:26Z</createdDateTime>
  <period.timeInterval>
    <start>2026-05-06T00:00Z</start>
    <end>2026-05-07T00:00Z</end>
  </period.timeInterval>
  <TimeSeries>
    <mRID>1</mRID>
    <businessType>A27</businessType>
    <in_Domain.mRID codingScheme="A01">10YGB----------A</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YFR-RTE------C</out_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <curveType>A03</curveType>
    <Period>
      <timeInterval>
        <start>2026-05-06T00:00Z</start>
        <end>2026-05-07T00:00Z</end>
      </timeInterval>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>3028</quantity></Point>
    </Period>
  </TimeSeries>
</Publication_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/net_transfer_capacity/year=YYYY/month=MM/net_transfer_capacity_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.net_transfer_capacity.NetTransferCapacityTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeNetTransferCapacity`
**Dedup key**: `(timestamp_utc, in_area_code, out_area_code)`
**Point-in-time field**: `published_at`, the response `createdDateTime`: a fetch-time stamp, not the forecast's issue time (`silver/entsoe/net_transfer_capacity.py:89`)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | derived from period + position | |
| `in_area_code` | `str` | No | `TimeSeries.in_Domain.mRID` | EIC |
| `out_area_code` | `str` | No | `TimeSeries.out_Domain.mRID` | EIC |
| `ntc_mw` | `float` | No | `Point.quantity` | MW |
| `resolution` | `str` | No | `Period.resolution` | Default "" in canonical. e.g. `PT60M`. |
| `published_at` | `datetime[UTC]` | Yes | document `createdDateTime` | Fetch-time stamp, within seconds of the request (`net_transfer_capacity.py:89`, `schemas/entsoe.py:355`) |
| `data_provider` | `str` | No | derived | `"entsoe"` |
| `ingested_at` | `datetime[UTC]` | Yes | derived | |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-05-06T00:00:00Z",
        "in_area_code": "10YGB----------A",
        "out_area_code": "10YFR-RTE------C",
        "ntc_mw": 3028.0,
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

- Most A61 publications use a **single Point with curveType A03** (variable
  resolution) — the published NTC is constant for a flat day-ahead window
  rather than 24 hourly points. gridflow's parser forward-fills each declared
  point to the next one, so silver holds one row per `PT60M` step
  (`connectors/entsoe/parsers.py:533-600`); on 2026-09-16 the six pairs sent
  1, 1, 1, 3, 16 and 17 declared points for 24 rows each.
- `contract_MarketAgreement.Type` is **mandatory** even though some examples
  in older guides show it as optional. Without it, A61 returns Acknowledgement
  with Reason 999.
- Possible direction: NTC(A→B) is generally not equal to NTC(B→A). Fetch both.
- Old NTC values may be revised via republished documents; silver dedup
  keeps the last fetched: bronze files are read in name order (fetch time
  first), then `unique(keep="last")` (`net_transfer_capacity.py:42,78`);
  `ingested_at` is the silver write time.

---

## Implementation delta

- **Tuple recorded:** `(documentType=A61, processType=none, businessType=none-in-request, contract_MarketAgreement.Type=A01, domain=in_Domain+out_Domain)`. Matches code — the `net_transfer_capacity` entry in `endpoints.py` `DOC_TYPES`.
- **Live validation 2026-05-08:** GB → FR for 2026-05-06 returned `Publication_MarketDocument` with 1 TimeSeries, 1 point of 3028 MW. PASS.
- TimeSeries `<businessType>` returned as `A27` (capacity allocation) — undocumented in code but expected per Article 11.1.

---

## Modelling notes

- NTC is not a hard bound on `flow_mw` from cross_border_flows. Project check
  2026-09-29 (hourly mean flow against NTC, same in/out, 2,426 hours from
  2026-08-01 to 2026-09-20): in hours with NTC above zero, flow on the GB
  pairs reaches at most 1.04 x NTC, bar one GB-BE hour at 1.11 (889 MW against
  804). Flow also runs at NTC 0: GB from NL has 286 such hours with flow
  positive in 259 (mostly about 0.06 MW, but 86.5 MW at 13:00 and 374 MW at
  19:00 UTC on 2026-09-19), and on NL-DE-LU flow exceeds NTC in 141 of 432
  hours, by up to 2,560 MW. So `utilisation = flow / ntc` slightly above 1 is
  normal on the GB pairs only where NTC > 0; it is undefined at NTC 0 and not
  meaningful on the NL pairs.
- Useful as a regime feature: low NTC days (outages, planned reductions) are
  systematically higher-spread.

---

## Links

- [Official API docs (PDF)](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/net_transfer_capacity.py`
- `src/gridflow/schemas/entsoe.py`
