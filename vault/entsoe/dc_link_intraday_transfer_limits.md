---
source: entsoe
dataset_key: dc_link_intraday_transfer_limits
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: DC link intraday transfer limits
  summary: >-
    Intraday transfer limits in MW, one direction per series; only the four GB borders of
    the eight pairs requested are DC links.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A93, Article 11.3
    cadence: "Per series, as `resolution` states; `PT60M` in these rows"
    grain: One row per interval start, `in_Domain` zone, `out_Domain` zone and business type
  landscape: power
  what_it_is: >-
    ENTSO-E's intraday transfer limit on a DC interconnector border, in MW (`MAW`), business type
    `B06` ("DC link constraint"). A day and pair with no published limit returns an
    acknowledgement (Reason 999, "No matching data found"), not rows. Documents here span a CET
    delivery day; silver keeps the hours inside the UTC request day. The GB and NL pair is BritNed.
  how_used:
    - Hour-by-hour limit on a DC link, set against its physical flow.
    - A flag for days on which an intraday limit was published at all.
    - The intraday limit set against forecast transfer capacity on the same pair.
  chart:
    type: line
    silver: entsoe/dc_link_intraday_transfer_limits
    time: timestamp_utc
    value: quantity_mw
    filter:
      - {column: in_area_code, op: eq, value: "10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA"}
      - {column: out_area_code, op: eq, value: "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL"}
    group: out_area_code
    group_map:
      "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL": britned
    series_order: [britned]
    aggregation: mean
    time_bucket: 1h
    window: {start: "2026-08-01", end: "2026-08-01"}
    unit: MW
  chart_view:
    title: GB and NL intraday limit, 1 August 2026
    caption: >-
      Silver `entsoe/dc_link_intraday_transfer_limits`, MW, the series with `in_area_code` GB and
      `out_area_code` NL, hourly, 1 August 2026 UTC. The line ends at 21:00, the last hour of the
      document, which spans the CET delivery day from 22:00 UTC on 31 July.
    alt: >-
      Line chart of the hourly intraday transfer limit in MW from
      entsoe/dc_link_intraday_transfer_limits, in_area_code GB and out_area_code NL, 00:00 to 21:00
      UTC on 1 August 2026. It starts at 600 MW, dips to 450 MW at 03:00, climbs to 1,021 MW at
      07:00 and holds between 1,032 and 1,038 MW from 08:00 to 14:00. It falls through 980 and 620
      MW to a low of 300 MW at 17:00, then recovers to 650 MW at 19:00 and 20:00 and ends at 600 MW.
    x_label: UTC hour, 1 August 2026
    key:
      - {series: britned, label: GB and NL, codes: "in_Domain GB, out_Domain NL", paint: petrol, note: "Hourly blocks as sent; an A03 point repeats until the next declared one."}
  raw_feed:
    note: >-
      One GET per zone pair per UTC day, for eight ordered pairs. `gridflow ingest` stores each
      reply in bronze, acknowledgements included; `gridflow transform` parses the rows to silver.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A93&periodStart=202608010000&periodEnd=202608020000&in_Domain=10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA&out_Domain=10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe dc_link_intraday_transfer_limits --start 2026-08-01 --end 2026-08-02, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe dc_link_intraday_transfer_limits --start 2026-08-01 --end 2026-08-01, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: ge, value: "2026-08-01T14:00:00Z"}
        - {column: timestamp_utc, op: le, value: "2026-08-01T21:00:00Z"}
      order_by: [timestamp_utc]
      columns: [timestamp_utc, in_area_code, out_area_code, quantity_mw, business_type, resolution, published_at]
    key: [timestamp_utc, in_area_code, out_area_code, business_type]
    caption: "14:00 to 21:00 UTC on 1 August 2026, including the 300 MW low at 17:00."
    fields:
      timestamp_utc: "Interval start, UTC: period start plus (position minus one) resolutions"
      in_area_code: "The `in_Domain` EIC as sent; the limit's direction is not verified"
      out_area_code: "The `out_Domain` EIC, the zone across the border"
      quantity_mw: "MW as sent (`MAW`); an A03 point repeats until the next declared one"
      business_type: "`B06`, \"DC link constraint\" in ENTSO-E's code list"
      resolution: "Interval length as sent, `PT60M` here; not normalised"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, within seconds of gridflow's request"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the silver relation for `dc_link_intraday_transfer_limits`,
      filtered on `timestamp_utc` with both ends included. Lineage columns are dropped and rows come ordered by
      `timestamp_utc` only, so sort before plotting.
    cells:
      - |
        df = data.entsoe.query("dc_link_intraday_transfer_limits", "2026-08-01", "2026-08-01")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
        df = df.sort_values(["timestamp_utc", "in_area_code", "out_area_code"])
      - df[["timestamp_utc", "in_area_code", "out_area_code", "quantity_mw", "business_type"]].head(8)
      - |
        df.plot(x="timestamp_utc", y="quantity_mw", drawstyle="steps-post", ylabel="MW",
                color="#155A6E", legend=False, figsize=(8, 3.5))
    needs: 1 August 2026
    plot_alt: >-
      Step plot of quantity_mw in MW for GB and NL, 00:00 to 21:00 UTC on 1 August 2026. It steps
      from 600 down to 450 MW at 03:00, up to between 1,021 and 1,038 MW from 07:00 to 14:00, down
      to 300 MW at 17:00, and back to 650 MW at 19:00.
  related:
    - {dataset: entsoe/net_transfer_capacity, note: "Forecast transfer capacity requested for the same eight ordered pairs"}
    - {dataset: entsoe/cross_border_flows, note: "Physical flow on the same ordered pairs, GB and NL included"}
    - {dataset: entsoe/commercial_schedules, note: "Scheduled exchanges on the same eight ordered pairs"}
    - {dataset: elexon/fuelhh, note: "Elexon's half-hourly Netherlands interconnector flow, `INTNED`"}
---

# ENTSO-E — DC Link Intraday Transfer Limits (A93)

## Overview

Intraday transfer-limit values for DC interconnector links (e.g. IFA, BritNed,
NSL, Viking Link, IFA2, ElecLink, NEMO). Article 11.3 of Regulation (EC)
543/2013. Limits are typically updated within the trading day as DC link
operators reassess capability against ramp constraints, AC system state, and
maintenance. Used as a real-time feature for short-horizon flow models.

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
| Historical depth | 2014-12-05 onward (intraday updates only published when capability changes) |
| Publication lag  | Intraday revisions throughout the trading day |
| Response format  | XML |

### ENTSO-E parameter tuple

| Field | Value |
|-------|-------|
| documentType | `A93` |
| processType | (none) |
| businessType (request) | (none) |
| domain-param-name | `in_Domain` + `out_Domain` (zone_pair) |

### Cross-zonal parameters

A93 is per-DC-link (border-pair). Same default UK-centric border table as
A11 / A61.

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | Yes | API key | UUID |
| `documentType` | str | Yes | `A93` | `A93` |
| `in_Domain` | str | Yes | EIC | `10YGB----------A` |
| `out_Domain` | str | Yes | EIC | `10YFR-RTE------C` |
| `periodStart` / `periodEnd` | str | Yes | UTC `yyyymmddHHMM` | |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -o "/tmp/entsoe-dc_link_intraday_transfer_limits.xml" \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A93&in_Domain=10YGB----------A&out_Domain=10YFR-RTE------C&periodStart=202605060000&periodEnd=202605070000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/dc_link_intraday_transfer_limits/<year>/<month>/<day>/raw_<YYYYMMDDTHHMMSSZ fetch time>_<sha256[:8]>.xml`, plus a `.meta.json` sidecar (`bronze/writer.py:33-34,57`)
**Format**: Raw XML, immutable.
**Granularity**: One file per (in_Domain, out_Domain, day).

### Bronze sample

Live call on 2026-05-08 returned `Acknowledgement_MarketDocument` with
Reason 999 — `No matching data found for Data item
CB_CAPACITY_FOR_DC_LINKS_INTRADAY_R3 [11.3] (10YGB----------A,
10YFR-RTE------C)`.

A populated response, GB/NL, fetched 2026-08-16 for the 2026-08-01 window
(`2026/08/01/raw_20260816T135213Z_15606c0a.xml`), is a `Publication_MarketDocument`
with `businessType` `B06` ("DC link constraint", ENTSO-E code list v29r0),
`quantity_Measure_Unit.name` `MAW` (megawatt), `curveType` `A03` (variable sized
block) and `resolution` `PT60M`. Its period is one CET delivery day,
`2026-07-31T22:00Z` to `2026-08-01T22:00Z`, and positions 3, 15 and 23 are not
declared (the A03 forward-fill repeats the previous value):

```xml
<TimeSeries>
  <mRID>1</mRID>
  <businessType>B06</businessType>
  <in_Domain.mRID codingScheme="A01">10YGB----------A</in_Domain.mRID>
  <out_Domain.mRID codingScheme="A01">10YNL----------L</out_Domain.mRID>
  <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
  <curveType>A03</curveType>
  <Period>
    <timeInterval>
      <start>2026-07-31T22:00Z</start>
      <end>2026-08-01T22:00Z</end>
    </timeInterval>
    <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>700</quantity></Point>
      <Point><position>2</position><quantity>600</quantity></Point>
      <Point><position>4</position><quantity>550</quantity></Point>
  </Period>
</TimeSeries>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/dc_link_intraday_transfer_limits/year=YYYY/month=MM/dc_link_intraday_transfer_limits_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h6_market.DcLinkIntradayTransferLimitsTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeTransmissionMarketQuantity`
**Dedup key**: `(timestamp_utc, in_area_code, out_area_code, business_type)`
**Point-in-time field**: `none`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | period + position | |
| `in_area_code` | `str` | No | `in_Domain.mRID` | EIC |
| `out_area_code` | `str` | No | `out_Domain.mRID` | EIC |
| `quantity_mw` | `float` | No | `Point.quantity` | DC link transfer limit MW |
| `business_type` | `str` | No | TS `businessType` | Default "" in canonical. `B06` ("DC link constraint") in the populated responses of 2026-08-16. |
| `resolution` | `str` | No | `Period.resolution` | Default "" in canonical. |
| `published_at` | `datetime[UTC]` | Yes | document `createdDateTime` | Via `with_published_at` (`h6_market.py:105`); a fetch-time stamp, within 1 s of each file's `fetched_at` in the 2026-08-16 bronze |
| `data_provider` | `str` | No | derived | `"entsoe"` |
| `ingested_at` | `datetime[UTC]` | Yes | derived | |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-08-01T17:00:00Z",
        "in_area_code": "10YGB----------A",
        "out_area_code": "10YNL----------L",
        "quantity_mw": 300.0,
        "business_type": "B06",
        "resolution": "PT60M",
        "published_at": "2026-08-16T13:52:13Z",
        "data_provider": "entsoe",
        "ingested_at": "2026-08-16T13:52:53.260295Z",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **EMPTY-by-design for many borders.** Article 11.3 only requires a publication
  when a DC link operator revises a previously published intraday limit. A
  PT24H "no revisions" day returns `Acknowledgement_MarketDocument` with
  Reason 999 (`No matching data found`).
- The Reason text spells the article reference: `[11.3]` and the data-item
  string `CB_CAPACITY_FOR_DC_LINKS_INTRADAY_R3` — useful diagnostic.
- Variable resolution and asymmetric publication times — silver does not
  align across borders.
- **Delivery-day over-span is trimmed.** Both populated documents of 2026-08-16
  span a CET/CEST delivery day (22:00Z to 22:00Z in summer), so each straddles two
  UTC request days.
  The event-window filter (`EVENT_WINDOW_FILTER = True`, `h6_market.py:141`;
  `base.py:1915-1953`) keeps only rows inside the partition's own
  `[periodStart, periodEnd)`. The 2026-08-05 request returned the 2026-08-06
  delivery day; silver day 2026-08-05 keeps its first two hours (22:00Z, 23:00Z),
  and the rest belongs to silver day 2026-08-06, which needs its own ingest.

---

## Implementation delta

- **Tuple recorded:** `(documentType=A93, processType=none, businessType=none-in-request, domain=in_Domain+out_Domain)`. Matches code — the `dc_link_intraday_transfer_limits` entry in `endpoints.py` `DOC_TYPES`.
- **Live validation 2026-05-08 GB→FR for 2026-05-06:** Acknowledgement, Reason 999, no data published. **EMPTY** — cause: "border has zero allocation in window" (no DC-link revision recorded that day).
- Empty result is expected and not a code defect; consumers should treat absence as "no revision" rather than 0.

---

## Modelling notes

- Intraday limit revisions are rare events — feature engineer as
  `limit_revision_present_today` (binary) and `limit_diff_vs_ntc` (delta from
  the day-ahead A61 NTC) when present.
- Useful in cascade-failure / outage models where DC ramp limits matter.

---

## Links

- [Official API docs (PDF)](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/h6_market.py`
- `src/gridflow/schemas/entsoe.py`
