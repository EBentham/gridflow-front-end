---
source: entsoe
dataset_key: redispatching_internal
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Congestion management
  summary: >-
    TSO measures against grid constraints under Article 13.1: redispatch inside a zone or across a
    border, countertrading, and each zone's monthly cost.
  facts:
    vendor: ENTSO-E Transparency Platform, document types A63, A91 and A92
    cadence: "Redispatch and countertrading quarter-hourly (`PT15M`) as sent; costs one value per month (`P1M`)"
    grain: One row per interval start, zone pair, business type; costs once per daily partition
  landscape: market
  what_it_is: >-
    Article 13.1 publications. Redispatching (`A63`) is a TSO-ordered adjustment to relieve a
    constraint, inside one zone (`A85`) or across a border (`A46`); countertrading (`A91`) is a
    cross-zone exchange between TSOs; `A92` is each zone's monthly cost in EUR, which silver copies
    into every daily partition. Up and down arrive as separate series; silver keeps no direction
    column.
  how_used:
    - Quarter-hours of internal redispatch per zone, as a congestion signal for flow models.
    - Monthly congestion cost per zone in EUR, split by business type `A46`, `B03`, `B04`.
    - "A binary feature: whether any redispatch or countertrade was sent for a day."
  chart:
    type: line
    silver: entsoe/redispatching_internal
    time: timestamp_utc
    value: quantity_mw
    filter:
      - {column: in_area_code, op: eq, value: "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL"}
    group: business_type
    group_map: {A85: netherlands}
    aggregation: last
    window: {start: "2026-09-15", end: "2026-09-21"}
    unit: MWH
  chart_view:
    title: Internal redispatch, Netherlands, 15 to 21 September 2026
    caption: >-
      Silver `entsoe/redispatching_internal`, Netherlands rows, quarter-hourly, 15 to 21 September
      2026 UTC, value as sent (`MWH`). Netherlands replies carry separate up and down series; silver keeps one per
      quarter-hour, and here every point is the down (`A02`) series.
    alt: >-
      Line chart of internal redispatch in the Netherlands, down series only, from
      entsoe/redispatching_internal, value as sent in MWH, quarter-hourly, 15 to 21 September 2026
      UTC. Values step between 0 and 84.0, the peak from 19:00 to 19:45 UTC on 18 September. The
      line sits at 0 for stretches on 15 and 16 September and from 15:00 UTC on 21 September; from
      17 to 20 September it never drops below 32.5.
    x_label: UTC, quarter-hours
    key:
      - {series: netherlands, label: "Netherlands, down (A02)", codes: "A85, flowDirection A02", paint: petrol, note: "The up (`A01`) series for the same quarter-hours is not in silver."}
  raw_feed:
    note: >-
      One GET per UTC day per border pair (eight) or, for costs, per zone (six). Internal replies
      name one zone in both domains; the Netherlands returns under three pairs.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A63&periodStart=202609180000&periodEnd=202609190000&in_Domain=10YNL%2D%2D%2D%2D%2D%2D%2D%2D%2D%2DL&out_Domain=10YBE%2D%2D%2D%2D%2D%2D%2D%2D%2D%2D2&businessType=A85&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe redispatching_internal --start 2026-09-15 --end 2026-09-22, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe redispatching_internal --start 2026-09-15 --end 2026-09-21, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: in_area_code, op: eq, value: "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL"}
        - {column: timestamp_utc, op: ge, value: "2026-09-18T18:15:00Z"}
        - {column: timestamp_utc, op: le, value: "2026-09-18T20:00:00Z"}
      order_by: [timestamp_utc]
      columns: [timestamp_utc, in_area_code, out_area_code, quantity_mw, business_type, resolution, published_at]
    key: [timestamp_utc, in_area_code, out_area_code, business_type]
    caption: "The Netherlands, eight quarter-hours around the chart's peak, 18 September 2026."
    fields:
      timestamp_utc: "Interval start, UTC: period start plus (position minus 1) times resolution"
      in_area_code: "The reply's `in_Domain` EIC: the zone itself, not the requested pair"
      out_area_code: "The reply's `out_Domain` EIC: the same zone for internal redispatch"
      quantity_mw: "As sent (`MWH`); direction not recorded; forward-filled from the last point (`A03`)"
      business_type: "`A85`, internal redispatch; the cross-border table carries `A46`"
      resolution: "Interval length as sent, `PT15M` in these rows; not normalised"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, within seconds of gridflow's request"
  notebook:
    lead: >-
      Reads `silver_entsoe_redispatching_internal` as pandas, filtered on `timestamp_utc`, both ends
      included; lineage dropped. Cells: the Netherlands rows, then quarter-hours above zero and the
      peak per UTC day.
    cells:
      - |
        df = data.entsoe.query("redispatching_internal", "2026-09-15", "2026-09-21")
        df["timestamp_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
        nl = df[df.in_area_code.str.startswith("10YNL")].sort_values("timestamp_utc")
        nl[["timestamp_utc", "in_area_code", "quantity_mw", "business_type"]].head()
      - |
        day = nl.timestamp_utc.dt.date.rename("utc_day")
        nl.groupby(day).quantity_mw.agg(above_zero=lambda s: int((s > 0).sum()), peak="max").reset_index()
      - |
        nl.set_index("timestamp_utc").quantity_mw.plot(ylabel="MWH as sent", drawstyle="steps-post", figsize=(8, 3.5), color="#155A6E");
    needs: 15 to 21 September 2026
    plot_alt: >-
      Step plot of the Netherlands' internal redispatch, down series, value as sent in MWH, 15 to 21
      September 2026 UTC. It steps between 0 and 84, with the peak on the evening of 18 September,
      holds between 62.5 and 84 on 18 and 19 September, and falls to 0 from 15:00 UTC on 21
      September.
  related:
    - {dataset: entsoe/cross_border_flows, note: "Physical flow on the same eight ordered border pairs"}
    - {dataset: entsoe/net_transfer_capacity, note: "Forecast transfer capacity on the same ordered border pairs"}
    - {dataset: entsoe/auction_revenue, note: "Border auction revenue in EUR; the costs here are per zone"}
  family:
    slug: congestion-management
    members:
      - dataset: redispatching_internal
        differs: "`A63` with `businessType=A85`; one zone per series, quarter-hourly `MWH` as sent"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A63&periodStart=202609180000&periodEnd=202609190000&in_Domain=10YNL%2D%2D%2D%2D%2D%2D%2D%2D%2D%2DL&out_Domain=10YBE%2D%2D%2D%2D%2D%2D%2D%2D%2D%2D2&businessType=A85&securityToken=$ENTSOE_API_KEY"
      - dataset: redispatching_cross_border
        differs: "`businessType=A46`; one border pair per series; the named line is not kept in silver"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A63&periodStart=202607070000&periodEnd=202607080000&in_Domain=10YNL%2D%2D%2D%2D%2D%2D%2D%2D%2D%2DL&out_Domain=10YBE%2D%2D%2D%2D%2D%2D%2D%2D%2D%2D2&businessType=A46&securityToken=$ENTSOE_API_KEY"
      - dataset: countertrading
        differs: "`A91`; many replies are an Acknowledgement; data carries `B03`, one point per quarter-hour, `MAW`"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A91&periodStart=202609220000&periodEnd=202609230000&in_Domain=10YFR%2DRTE%2D%2D%2D%2D%2D%2DC&out_Domain=10Y1001A1001A82H&securityToken=$ENTSOE_API_KEY"
      - dataset: congestion_management_costs
        differs: "`A92`, one zone; EUR per month (`P1M`); some months gain a false second point"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A92&periodStart=202607010000&periodEnd=202607020000&in_Domain=10YNL%2D%2D%2D%2D%2D%2D%2D%2D%2D%2DL&out_Domain=10YNL%2D%2D%2D%2D%2D%2D%2D%2D%2D%2DL&securityToken=$ENTSOE_API_KEY"
---

# ENTSO-E — Redispatching: Internal (A63 / businessType A85)

## Overview

Internal-zone redispatching activations — measures within a single bidding
zone to relieve internal grid constraints. Article 13.1.A of Regulation (EC)
543/2013. Sister dataset to `redispatching_cross_border`. Used in models of
internal congestion frequency, internal redispatch cost, and as a feature
for system-stress prediction.

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
| Publication lag  | D-1 |
| Response format  | XML |

### ENTSO-E parameter tuple

| Field | Value |
|-------|-------|
| documentType | `A63` |
| processType | (none) |
| businessType | `A85` (internal redispatch) |
| domain-param-name | `in_Domain` + `out_Domain` (zone_pair, but with `in_Domain == out_Domain` for internal) |

### Cross-zonal parameters

A63/A85 is logically per-zone, but the connector does **not** send
`in_Domain == out_Domain`: `domain_style="zone_pair"` sends the eight
cross-border `_FLOW_PAIRS` (GB/FR, GB/NL, GB/BE, GB/IE-SEM, FR/BE, FR/DE-LU,
NL/DE-LU, NL/BE; `client.py:40-49`, `211-227`). The reply's TimeSeries names
the zone itself in both domains (e.g. NL→NL), so one zone can come back under
several pairs: the NL document returned for GB/NL, NL/DE-LU and NL/BE alike
(2026-08 and 2026-09 bronze); silver's dedup collapses the copies.
(Corrected 2026-09-29 from code; the earlier text said `(GB, GB)`, `(FR, FR)`, `(NL, NL)`.)

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | Yes | API key | UUID |
| `documentType` | str | Yes | `A63` | `A63` |
| `businessType` | str | Yes | `A85` for internal | `A85` |
| `in_Domain` | str | Yes | Zone EIC | `10YGB----------A` |
| `out_Domain` | str | Yes | Same zone EIC | `10YGB----------A` |
| `periodStart` / `periodEnd` | str | Yes | UTC | |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -o "/tmp/entsoe-redispatching_internal.xml" \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A63&businessType=A85&in_Domain=10YGB----------A&out_Domain=10YGB----------A&periodStart=202605060000&periodEnd=202605070000"
```

(Validation used GB→FR for the standard test border; production code calls
the eight `_FLOW_PAIRS`, not GB→GB / FR→FR: see above.)

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/redispatching_internal/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per (zone, day).

### Bronze sample

Live call 2026-05-08: Acknowledgement, Reason 999 —
`REDISPATCHING_INTERNAL_R3 [13.1.A] (10YGB----------A)`. A populated
response would carry TimeSeries with `<businessType>A85</businessType>`.

Populated replies seen in 2026-08 and 2026-09 bronze (NL and BE) are a
`TransmissionNetwork_MarketDocument` whose `period.timeInterval` spans two
CET days (22:00Z to 22:00Z) for a one-UTC-day request. Every TimeSeries
carries `flowDirection.direction` (`A01` or `A02`; gridflow reads these as up
and down in `activated_balancing_qty.py:25`), `quantity_Measurement_Unit.name`
`MWH`, `curveType` `A03`, `resolution` `PT15M` and Reason `B24`. NL sends one
day-long series per direction per CET day (`mktPSRType.psrType` `A05`); BE
sends shorter series (`A04`), some naming a line in `location.name` (e.g.
`BRUGGE - SLYKE 150.15`) with `pSRType.psrType` `B21`.

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/redispatching_internal/year=YYYY/month=MM/redispatching_internal_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h6_market.RedispatchingInternalTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeTransmissionMarketQuantity`
**Dedup key**: `(timestamp_utc, in_area_code, out_area_code, business_type)`
**Point-in-time field**: `none`

### Silver schema

Same H6 quantity envelope: `timestamp_utc`, `in_area_code`, `out_area_code`,
`quantity_mw`, `business_type`, `resolution`, `published_at`, `data_provider`, `ingested_at`
(`h6_market.py:107-117`; `published_at` added 2026-09-29).

### Silver sample

Real row from silver, replacing a synthetic GB example (400.0, `PT60M`) on 2026-09-29.
`quantity_mw` holds the value as sent; the unit in the reply is `MWH`, not MW.

```python
[
    {
        "timestamp_utc": "2026-09-18T19:00:00Z",
        "in_area_code": "10YNL----------L",
        "out_area_code": "10YNL----------L",
        "quantity_mw": 84.0,
        "business_type": "A85",
        "resolution": "PT15M",
        "published_at": "2026-09-26T17:55:17Z",
        "data_provider": "entsoe",
        "ingested_at": "2026-09-26T17:55:41Z",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **EMPTY-by-design** on most days for most zones — internal redispatch is
  event-driven.
- The Reason text for an empty response carries only one EIC
  (`(10YGB----------A)`) even though the request used both `in_Domain` and
  `out_Domain` — the API treats this as a single-zone query when in == out.
- Distinguished from `redispatching_cross_border` only by `businessType`.
- **Direction is lost in silver (2026-09-29).** The parser reads
  `flowDirection.direction` (`parsers.py:316-319`), but the H6 transformer
  neither outputs it nor keys on it: dedup is `(timestamp_utc, in_area_code,
  out_area_code, business_type)`, `keep="last"` (`h6_market.py:91-99`). Where
  a quarter-hour has both an `A01` and an `A02` value, the later-listed series
  wins. In the NL replies `A02` follows `A01`, so NL silver equals the `A02`
  series (672 of 672 NL rows, 15 to 21 Sep 2026; the `A01` value differs in
  476 of them). BE days carry only one direction each, so BE silver rows mix
  `A01` and `A02` with nothing to tell them apart.
- **Unit.** Replies send `quantity_Measurement_Unit.name` `MWH`; the parser
  does not read it and the column is named `quantity_mw`.

---

## Implementation delta

- **Tuple recorded:** `(documentType=A63, processType=none, businessType=A85, domain=in_Domain+out_Domain)`. Matches code — the `redispatching_internal` entry in `endpoints.py` `DOC_TYPES`.
- **Live validation 2026-05-08:** GB→FR (standard test border) returned Acknowledgement, Reason 999, single-zone interpretation `(10YGB----------A)`. **EMPTY** — cause: "border has zero allocation in window" (no internal GB redispatch published that day).
- Disambiguation: this page = **businessType=A85** (internal); sister page (`redispatching_cross_border`) = **businessType=A46**.

---

## Modelling notes

- Internal redispatch is the primary measure of in-zone constraint pressure.
  Useful as a daily count (`internal_redispatch_events_today`) regressor for
  imbalance-volatility models.

---

## Links

- [Official API docs (PDF)](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/h6_market.py`
- `src/gridflow/schemas/entsoe.py`
