---
source: entsoe
dataset_key: net_positions
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Implicit auction net positions
  summary: >-
    A bidding zone's net position from day-ahead market coupling, in MW per market time unit, sent
    as a size with a direction.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A25, business type B09
    cadence: Quarter-hourly points in the responses gridflow holds
    grain: "One row per interval start, `in_Domain` and `out_Domain`; one is the zone"
  landscape: market
  what_it_is: >-
    ENTSO-E's day-ahead implicit net position for a bidding zone: its exports and imports from
    day-ahead market coupling, netted, in MW. ENTSO-E sends a size plus a direction, not a sign: the
    zone sits in `out_area_code` for export and `in_area_code` for import (a project reading), with
    a `REGION_CODE` placeholder opposite.
  how_used:
    - Whether a zone cleared day-ahead as net exporter or importer, per quarter-hour.
    - A signed position feature for zone price-spread and flow models.
    - Checking cleared day-ahead positions against metered generation minus load.
  chart:
    type: stacked-area
    silver: entsoe/net_positions
    time: timestamp_utc
    value: quantity_mw
    # DE-LU on either side of the row; the other side is REGION_CODE, whose dashes are \x2D escapes.
    filter:
      - {column: in_area_code, op: in, value: ["10Y1001A1001A82H", "REGION_CODE\x2D\x2D\x2D\x2D\x2D"]}
      - {column: out_area_code, op: in, value: ["10Y1001A1001A82H", "REGION_CODE\x2D\x2D\x2D\x2D\x2D"]}
    group: in_area_code
    group_map:
      "REGION_CODE\x2D\x2D\x2D\x2D\x2D": exporting
      "10Y1001A1001A82H": importing
    series_order: [exporting, importing]
    aggregation: sum
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: DE-LU day-ahead net position, 14 to 20 September 2026
    caption: >-
      Silver `entsoe/net_positions`, MW, each quarter-hour of 14 to 20 September 2026 UTC for DE-LU,
      one row each. Every quarter-hour here has one direction, so one band shows at a time; both sit
      above zero, as ENTSO-E sends no sign.
    alt: >-
      Stacked area chart of DE-LU day-ahead net position from entsoe/net_positions, in MW, each
      quarter-hour of 14 to 20 September 2026 UTC; one band shows at a time, both above zero.
      Importing reaches 11,428 MW at 17:30 on the 14th and fills all of the 16th. Exporting is brief
      on the 14th (852 MW at most), then fills most middays, peaking at 13,219 MW at 10:45 on the
      19th, with importing mostly in the evening and at night. The 20th is exporting throughout, up
      to 12,714 MW.
    x_label: UTC date; quarter-hours
    key:
      - {series: exporting, label: Exporting, codes: "DE-LU as out_Domain", paint: petrol, note: "Export by the project's reading, checked against DE-LU generation minus load."}
      - {series: importing, label: Importing, codes: "DE-LU as in_Domain", paint: olive, note: "Import by the same reading; the row's other side is a `REGION_CODE` placeholder."}
  raw_feed:
    note: >-
      One GET per zone per UTC day, six zones; GB and IE-SEM return no-data acknowledgements in
      every response gridflow holds. `gridflow ingest` writes bronze, `gridflow transform` silver.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A25&periodStart=202609170000&periodEnd=202609180000&in_Domain=10Y1001A1001A82H&out_Domain=10Y1001A1001A82H&businessType=B09&contract_MarketAgreement.Type=A01&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe net_positions --start 2026-09-14 --end 2026-09-21, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe net_positions --start 2026-09-14 --end 2026-09-20, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: ge, value: "2026-09-17T06:00:00Z"}
        - {column: timestamp_utc, op: lt, value: "2026-09-17T08:00:00Z"}
        - {column: in_area_code, op: in, value: ["10Y1001A1001A82H", "REGION_CODE\x2D\x2D\x2D\x2D\x2D"]}
        - {column: out_area_code, op: in, value: ["10Y1001A1001A82H", "REGION_CODE\x2D\x2D\x2D\x2D\x2D"]}
      order_by: [timestamp_utc]
      columns: [timestamp_utc, in_area_code, out_area_code, quantity_mw, business_type, resolution, published_at]
    key: [timestamp_utc, in_area_code, out_area_code, business_type]
    caption: "DE-LU, 06:00 to 07:45 UTC on 17 September 2026: importing, then exporting from 07:00."
    fields:
      timestamp_utc: "Interval start, UTC: period start plus (position minus 1) times resolution"
      in_area_code: "`in_Domain` EIC: the zone when it imports (project reading), else `REGION_CODE\x2D\x2D\x2D\x2D\x2D`"
      out_area_code: "`out_Domain` EIC: the zone when it exports (project reading), else `REGION_CODE\x2D\x2D\x2D\x2D\x2D`"
      quantity_mw: "Net position in MW as sent (`MAW`): a size, with no sign"
      business_type: "`B09`, ENTSO-E's business type for a net position"
      resolution: "Interval length as sent, `PT15M` here; not normalised"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, within seconds of gridflow's request"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_entsoe_net_positions`, filtered on `timestamp_utc`
      with both ends included. Lineage columns are dropped and rows come ordered by `timestamp_utc`
      only, so sort before plotting.
    cells:
      - |
        df = data.entsoe.query("net_positions", "2026-09-14", "2026-09-20")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
        df = df.sort_values(["timestamp_utc", "in_area_code", "out_area_code"])
      - df[["timestamp_utc", "in_area_code", "out_area_code", "quantity_mw"]].head(8)
      - |
        exporting = df["in_area_code"].str.startswith("REGION")
        df["zone"] = df["out_area_code"].where(exporting, df["in_area_code"])
        df["net_mw"] = df["quantity_mw"].where(exporting, -df["quantity_mw"])
        de = df[df["zone"] == "10Y1001A1001A82H"]
        de.plot(x="timestamp_utc", y="net_mw", ylabel="MW, export positive", legend=False,
                color="#155A6E", figsize=(8, 3.5))
    needs: 14 to 20 September 2026
    plot_alt: >-
      Line plot of DE-LU net_mw against timestamp_utc, 14 to 20 September 2026 UTC, export drawn
      positive. It starts near -4,150 MW and falls to about -11,400 MW on the 14th's evening.
      Midday export peaks run from about 8,400 MW on the 15th to 13,200 MW on the 19th; the 16th
      stays below zero and the 20th stays above it.
  related:
    - {dataset: entsoe/day_ahead_prices, note: "Prices cleared in the same day-ahead coupling"}
    - {dataset: entsoe/cross_border_flows, note: "Metered flow on single borders, not a zone's netted position"}
    - {dataset: entsoe/actual_generation, note: "With actual load, the check behind the export reading"}
    - {dataset: entsoe/actual_load, note: "With generation, the check behind the export reading"}
---

# ENTSO-E — Implicit Auction Net Positions (A25, businessType=B09, single-zone)

## Overview

Net implicit-auction position per bidding zone, in MW — the algebraic sum
of cleared cross-zonal flows attributable to the zone after SDAC clearing.
Article 12.1.E of Regulation (EC) 543/2013. **The only A25 variant that
uses single-zone (`domain_style=zone`) parameters** rather than a
border-pair. Used as a feature for SDAC clearing analysis and zone-level
import/export economics.

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
| Publication lag  | After SDAC settlement |
| Response format  | XML |

### ENTSO-E parameter tuple (validation criterion)

| Field | Value |
|-------|-------|
| documentType | `A25` |
| processType | (none) |
| businessType | `B09` (implicit auction net position) |
| `contract_MarketAgreement.Type` | `A01` (daily): the day-ahead net position; the DDD (v3r4 p.55) keeps the total, with intraday, as a separate publication |
| domain-param-name | `in_Domain` only (`domain_style=zone`, single zone — connector mirrors `out_Domain` to `in_Domain`) |

### Single-domain parameters (NOT cross-zonal)

A25/B09 net_positions is **single-zone**. The connector's
`domain_style="zone"` (the `net_positions` entry in `endpoints.py`) means `in_Domain` is the
zone whose net position is reported. The current curl form passes the same
EIC for both `in_Domain` and `out_Domain` to satisfy the connector's URL
builder.

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | Yes | API key | UUID |
| `documentType` | str | Yes | `A25` | `A25` |
| `businessType` | str | Yes | `B09` | `B09` |
| `contract_MarketAgreement.Type` | str | Yes | `A01` | `A01` |
| `in_Domain` | str | Yes | Bidding zone EIC | `10YGB----------A` |
| `out_Domain` | str | (mirrored) | Same EIC | `10YGB----------A` |
| `periodStart` / `periodEnd` | str | Yes | UTC | |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -o "/tmp/entsoe-net_positions.xml" \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A25&businessType=B09&contract_MarketAgreement.Type=A01&in_Domain=10YGB----------A&out_Domain=10YGB----------A&periodStart=202605060000&periodEnd=202605070000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/net_positions/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per (zone, day).

### Bronze sample

Live 2026-05-08 GB: Acknowledgement, Reason 999 —
`IMPLICIT_ALLOCATIONS_NET_POSITIONS [12.1.E] (10YGB----------A)` (note the
single EIC in the Reason text, confirming the single-zone interpretation).
Retried 30-day window: also EMPTY.

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/net_positions/year=YYYY/month=MM/net_positions_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.h6_market.NetPositionsTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeTransmissionMarketQuantity`
**Dedup key**: `(timestamp_utc, in_area_code, out_area_code, business_type)`
**Point-in-time field**: `none`

### Silver schema

H6 quantity envelope. **Note**: the request mirrors the zone into both
domains, but the response does not: each TimeSeries carries the zone on one
side and `REGION_CODE-----` on the other, so silver rows are either
(zone, `REGION_CODE-----`) or (`REGION_CODE-----`, zone), one direction per
interval (probe `entsoe_A25_net_positions_FR_20260601.xml:19-20`; mapped
unchanged by `h6_market.py:66-72`). Corrected 2026-09-29.

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-09-17T07:00:00Z",
        "in_area_code": "REGION_CODE-----",
        "out_area_code": "10Y1001A1001A82H",
        "quantity_mw": 2059.1,
        "business_type": "B09",
        "resolution": "PT15M",
        "published_at": "2026-09-26T18:16:48Z",
        "data_provider": "entsoe",
        "ingested_at": "2026-09-26T18:18:18Z",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Single-zone**, despite using a sister transformer that ordinarily handles
  zone-pair data. Set `in_Domain` only; the connector mirrors `out_Domain`
  internally.
- `quantity_mw` is unsigned (every silver row is positive; the transformer
  only casts it, `h6_market.py:86`). ENTSO-E marks direction, not sign
  (DDD v3r4 p.55: "indicator whether the value represents import or export").
  Zone as `out_area_code` reads as export, zone as `in_area_code` as import:
  a project reading, not stated in the DDD, checked for DE-LU against actual
  generation minus actual load (hourly correlation 0.89). Corrected 2026-09-29;
  the earlier "negative = export" line did not match the rows.
- Only published for SDAC zones. Post-Brexit GB is not in SDAC, so GB
  publishes EMPTY. IE-SEM, also in `DEFAULT_ZONES` (`endpoints.py:395`),
  returns the same Reason 999 acknowledgement on every bronze day checked
  2026-09-29.

---

## Implementation delta

- **Tuple recorded:** `(documentType=A25, processType=none, businessType=B09, contract_MarketAgreement.Type=A01, domain=in_Domain only — `domain_style=zone`)`. Matches code — the `net_positions` entry in `endpoints.py` `DOC_TYPES`.
- **Live validation 2026-05-08 GB daily and 30-day:** Acknowledgement, Reason 999, single-EIC fingerprint `(10YGB----------A)`. **EMPTY** — cause: "border has zero allocation in window" (GB not in SDAC post-Brexit; would need a SDAC-participating zone to PASS).
- **Disambiguation from other A25 variants — this is the ONLY single-zone A25:**
  - `auction_revenue`: `businessType=B07`, zone_pair, EUR.
  - `transfer_capacity_use`: `businessType=B05` + `Auction.Category=A01`, zone_pair, MW.
  - `congestion_income`: `businessType=B10`, zone_pair, EUR.
  - **`net_positions`** (this page): `businessType=B09`, **`domain_style=zone`** (single zone), MW.

---

## Modelling notes

- Net position is the canonical measure of zone-level SDAC dependence.
  Useful as a regression target for "net importer / net exporter" regime
  classification models.
- For non-SDAC GB, surrogate via `cross_border_flows` (A11) summed across
  all interconnectors.

---

## Links

- [Official API docs (PDF)](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/h6_market.py`
- `src/gridflow/schemas/entsoe.py`
