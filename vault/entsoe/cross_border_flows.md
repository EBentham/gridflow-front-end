---
source: entsoe
dataset_key: cross_border_flows
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Physical flows across borders
  summary: >-
    Physical power flows across European bidding-zone borders in MW, one direction per border for
    the eight zone pairs gridflow requests.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A11
    cadence: "Per series, as `resolution` states; `PT60M` or `PT15M` in these rows"
    grain: One row per interval start, `in_Domain` zone and `out_Domain` zone
  landscape: power
  what_it_is: >-
    ENTSO-E's physical flow on a bidding-zone border, in MW, one direction per series: physical
    flows, not the schedules in `commercial_schedules`. gridflow requests one direction of each of
    eight borders, so no border can be netted from this table. Rows with `in_area_code` GB track
    power arriving in GB, a project check against Elexon's interconnector flows.
  how_used:
    - Gross flow into GB on each interconnector border, hour by hour.
    - Physical flow set against the scheduled exchange on the same border.
    - A feature for price-spread and congestion models between neighbouring zones.
  chart:
    type: line
    silver: entsoe/cross_border_flows
    time: timestamp_utc
    value: flow_mw
    filter:
      - {column: in_area_code, op: eq, value: "10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA"}
      - {column: out_area_code, op: in, value: ["10YFR\x2DRTE\x2D\x2D\x2D\x2D\x2D\x2DC", "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2", "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL"]}
    group: out_area_code
    group_map:
      "10YFR\x2DRTE\x2D\x2D\x2D\x2D\x2D\x2DC": france
      "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2": belgium
      "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL": netherlands
    series_order: [france, belgium, netherlands]
    aggregation: mean
    time_bucket: 1h
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: Flows into GB by border, 14 to 20 September 2026
    caption: >-
      Silver `entsoe/cross_border_flows`, MW, hourly means of the France, Belgium and Netherlands
      series with `in_area_code` GB, 14 to 20 September 2026 UTC; the last two are sent
      quarter-hourly here. gridflow never requests the reverse, so flow out of GB is absent.
    alt: >-
      Line chart of hourly mean flow in MW from entsoe/cross_border_flows, three series with
      in_area_code GB, 14 to 20 September 2026 UTC. France is highest, near 3,060 MW for hours on every day
      except the 19th (945 MW at most), and drops below 15 MW each day. Belgium moves between zero
      and about 1,040 MW, staying under 65 MW on the 17th. The Netherlands stays below 1 MW until
      the 19th, then reaches 374 MW that day and 1,017 MW late on the 20th.
    x_label: UTC date; hourly means
    key:
      - {series: france, label: From France, codes: "out_Domain FR", paint: petrol, note: "Hourly as sent. Tracks the positive parts of Elexon's INTFR, INTIFA2 and INTELEC, summed."}
      - {series: belgium, label: From Belgium, codes: "out_Domain BE", paint: horizon, note: "Quarter-hours averaged to the hour. Near zero here whenever Elexon's INTNEM is negative."}
      - {series: netherlands, label: From the Netherlands, codes: "out_Domain NL", paint: olive, note: "Quarter-hours averaged to the hour. Tracks the positive part of Elexon's INTNED."}
  raw_feed:
    note: >-
      One GET per zone pair per UTC day, for eight ordered pairs. `gridflow ingest` stores each
      reply in bronze; `gridflow transform` parses it to silver.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A11&periodStart=202609160000&periodEnd=202609170000&in_Domain=10YGB\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DA&out_Domain=10YFR\x2DRTE\x2D\x2D\x2D\x2D\x2D\x2DC&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe cross_border_flows --start 2026-09-14 --end 2026-09-21, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe cross_border_flows --start 2026-09-14 --end 2026-09-20, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: eq, value: "2026-09-16T21:00:00Z"}
      order_by: [in_area_code, out_area_code]
      columns: [timestamp_utc, in_area_code, out_area_code, flow_mw, resolution, published_at]
    key: [timestamp_utc, in_area_code, out_area_code]
    caption: "The eight ordered zone pairs gridflow requests, at 21:00 UTC on 16 September 2026."
    fields:
      timestamp_utc: "Interval start, UTC: period start plus (position minus one) resolutions"
      in_area_code: "The `in_Domain` EIC; GB rows track flow into GB (project check)"
      out_area_code: "The `out_Domain` EIC, the zone across the border"
      flow_mw: "MW as sent (`MAW`); an A03 point repeats until the next declared one"
      resolution: "Interval length as sent, for example `PT15M` or `PT60M`; not normalised"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, within seconds of gridflow's request"
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_entsoe_cross_border_flows`, filtered on
      `timestamp_utc` with both ends included. Lineage columns are dropped and rows come ordered by
      `timestamp_utc` only, so sort before pivoting.
    cells:
      - |
        df = data.entsoe.query("cross_border_flows", "2026-09-14", "2026-09-20")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
        df = df.sort_values(["timestamp_utc", "in_area_code", "out_area_code"])
      - df[["timestamp_utc", "in_area_code", "out_area_code", "flow_mw", "resolution"]].head(8)
      - |
        gb = df[df["in_area_code"].str.startswith("10YGB")].copy()
        gb["border"] = gb["out_area_code"].str[3:5]  # FR, BE, NL; IE-SEM's code gives "10"
        hourly = gb.pivot_table(index=gb["timestamp_utc"].dt.floor("h"), columns="border", values="flow_mw")
        hourly[["FR", "BE", "NL"]].plot(ylabel="MW", color=["#155A6E", "#3E8C97", "#66793B"], figsize=(8, 3.5))
    needs: 14 to 20 September 2026
    plot_alt: >-
      Line plot of hourly mean flow_mw with in_area_code GB, one line per border (FR, BE, NL),
      14 to 20 September 2026 UTC. FR reaches about 3,060 MW on most days and dips near zero
      between; BE peaks near 1,040 MW with long spells at zero; NL stays near zero until the 19th
      and reaches about 1,000 MW on the 20th.
  related:
    - {dataset: entsoe/commercial_schedules, note: "Scheduled exchanges on the same eight ordered pairs, not physical flow"}
    - {dataset: entsoe/net_transfer_capacity, note: "Forecast transfer capacity for the same ordered pairs"}
    - {dataset: entsoe/day_ahead_prices, note: "Prices at the continental and Irish ends; none for GB"}
    - {dataset: elexon/fuelhh, note: "Elexon's interconnector flows, used here to check the direction"}
---

# ENTSO-E — Physical Cross-Border Flows (A11)

## Overview

Physical cross-border power flows between ENTSO-E bidding zones in MW, at the resolution each response states (`PT60M` or `PT15M` in the responses gridflow holds; one border switched between them)
(metered or best estimate). Article 12.1.G of Regulation (EC) 543/2013.
Each TimeSeries carries one direction of a border; the reverse direction is a
separate TimeSeries on a separate request. Direction (project check, 2026-09-29,
not an ENTSO-E quote): rows with `in_Domain` = GB track the positive part of Elexon
FUELHH interconnector flows (positive as import to GB is itself a project check, not an Elexon rule) for 14 to 20 September 2026, per cable
summed for FR, so `in_Domain` reads as the receiving zone and `out_Domain` as the sending one.
Used as a feature for cross-border price-spread models, congestion analysis,
GB interconnector utilisation, and as a target for flow-forecasting.

→ Domain refs: [Cross-border flow](../../../20-domain/markets/cross-border-flow.md)
[Bidding zone EIC codes](../../../20-domain/concepts/eic-codes.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://web-api.tp.entsoe.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | Query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | Not formally documented — gridflow uses 1 req/s; back off on 429 |
| Pagination       | None (single XML document per call); split long windows client-side |
| Historical depth | From 2014-12-05 (ENTSO-E TP launch), border-dependent |
| Publication lag  | Hourly resolution, typically published within 1 hour of real time |
| Response format  | XML (`Publication_MarketDocument`) |

### ENTSO-E parameter tuple (validation criterion)

| Field | Value |
|-------|-------|
| documentType | `A11` |
| processType | (none) |
| businessType (request) | (none — server returns `A66` on TimeSeries) |
| domain-param-name | `in_Domain` + `out_Domain` (zone_pair) |

### Cross-zonal parameters

A11 is a directional flow, so both directions of a border take two requests
(one for each direction). gridflow sends one direction per border: the eight
ordered pairs in `_FLOW_PAIRS` (`connectors/entsoe/client.py:40-49`). The
direction column follows the project check in the Overview, which covers the
GB pairs only; the continental rows assume the same convention, unchecked:

| in_Domain | out_Domain | Border name | Direction |
|-----------|------------|-------------|-----------|
| `10YGB----------A` | `10YFR-RTE------C` | GB–FR (IFA, IFA2, ElecLink) | FR → GB (checked) |
| `10YGB----------A` | `10YNL----------L` | GB–NL (BritNed) | NL → GB (checked) |
| `10YGB----------A` | `10YBE----------2` | GB–BE (Nemo) | BE → GB (checked) |
| `10YGB----------A` | `10Y1001A1001A59C` | GB–IE-SEM | IE-SEM → GB (checked, weaker: hourly correlation about 0.79 with the per-cable positive parts; at most 70 MW while GB exported) |
| `10YFR-RTE------C` | `10YBE----------2` | FR–BE | BE → FR (assumed) |
| `10YFR-RTE------C` | `10Y1001A1001A82H` | FR–DE-LU | DE-LU → FR (assumed) |
| `10YNL----------L` | `10Y1001A1001A82H` | NL–DE-LU | DE-LU → NL (assumed) |
| `10YNL----------L` | `10YBE----------2` | NL–BE | BE → NL (assumed) |

The reverse of each pair (for example `in_Domain` FR, `out_Domain` GB) is not requested.

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | Yes | API key (UUID) | `00000000-...` |
| `documentType` | str | Yes | `A11` (cross-border physical flow) | `A11` |
| `in_Domain` | str | Yes | Source zone EIC | `10YGB----------A` |
| `out_Domain` | str | Yes | Destination zone EIC | `10YFR-RTE------C` |
| `periodStart` | str | Yes | Inclusive UTC start `yyyymmddHHMM` | `202605060000` |
| `periodEnd` | str | Yes | Exclusive UTC end `yyyymmddHHMM` | `202605070000` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -o "/tmp/entsoe-cross_border_flows.xml" \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A11&in_Domain=10YGB----------A&out_Domain=10YFR-RTE------C&periodStart=202605060000&periodEnd=202605070000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/cross_border_flows/<year>/<month>/<day>/raw_<YYYYMMDDTHHMMSSZ fetch time>_<sha256[:8]>.xml`, plus a `.meta.json` sidecar (`bronze/writer.py:33-34,56`)
**Format**: Raw XML, as-received. Immutable — never modified after write.
**Granularity**: One file per (in_Domain, out_Domain, day) tuple

### Bronze sample

```xml
<?xml version="1.0" encoding="utf-8"?>
<Publication_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0">
  <mRID>1cc6d87479954899a9952cb35f5547b4</mRID>
  <type>A11</type>
  <createdDateTime>2026-05-08T18:05:24Z</createdDateTime>
  <period.timeInterval>
    <start>2026-05-06T00:00Z</start>
    <end>2026-05-07T00:00Z</end>
  </period.timeInterval>
  <TimeSeries>
    <mRID>1</mRID>
    <businessType>A66</businessType>
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
      <Point><position>1</position><quantity>2967.4375</quantity></Point>
      <Point><position>2</position><quantity>2918.5925</quantity></Point>
    </Period>
  </TimeSeries>
</Publication_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/cross_border_flows/year=YYYY/month=MM/cross_border_flows_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.cross_border_flows.CrossBorderFlowsTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeCrossborderFlow`
**Dedup key**: `(timestamp_utc, in_area_code, out_area_code)`
**Point-in-time field**: `none` (no run-type semantics; revisions overwrite)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime[UTC]` | No | derived from `Period.timeInterval.start` + `position` | Inclusive interval start |
| `in_area_code` | `str` | No | `TimeSeries.in_Domain.mRID` | EIC, never normalised |
| `out_area_code` | `str` | No | `TimeSeries.out_Domain.mRID` | EIC, never normalised |
| `flow_mw` | `float` | No | `Point.quantity` | MW (Measure_Unit `MAW`) |
| `resolution` | `str` | No | `Period.resolution` | ISO code verbatim (e.g. `PT60M`, `PT15M`); not normalised |
| `published_at` | `datetime[UTC]` | Yes | document `createdDateTime` | Via `with_published_at` (`cross_border_flows.py:84`); a fetch-time stamp, not a publication time: in the 2026-09-16 bronze it is within seconds of each file's fetch time |
| `data_provider` | `str` | No | derived | Always `"entsoe"` |
| `ingested_at` | `datetime[UTC]` | Yes | derived | UTC now at silver write |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-05-06T00:00:00Z",
        "in_area_code": "10YGB----------A",
        "out_area_code": "10YFR-RTE------C",
        "flow_mw": 2967.4375,
        "resolution": "PT60M",
        "data_provider": "entsoe",
        "ingested_at": "2026-05-08T18:05:30Z",
    },
    {
        "timestamp_utc": "2026-05-06T01:00:00Z",
        "in_area_code": "10YGB----------A",
        "out_area_code": "10YFR-RTE------C",
        "flow_mw": 2918.5925,
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

- A11 is **directional**. Net flow on a border requires both directions
  fetched and subtracted; one direction may show 0 / be absent.
- Resolution typically `PT60M` for legacy borders, but ENTSO-E publishes some
  as `PT15M` post-2024 — silver does not normalise resolution.
- `<curveType>A03</curveType>` (variable-resolution curve) is the common case;
  a declared point holds until the next declared position, and the parser repeats
  it for every resolution step up to the period end (`connectors/entsoe/parsers.py:533-600`).
  A one-point day (the FR–BE probe of 2026-08-01) becomes 96 quarter-hour rows.
- `quantity_Measure_Unit.name` is `MAW` (megawatt) — note the unusual ENTSO-E
  spelling. Treat as MW.
- Server-set `businessType` `A66` (settlement total) is on the TimeSeries; do
  not pass `businessType` in the request — it is ignored / can cause empties.

---

## Implementation delta

- **Tuple recorded:** `(documentType=A11, processType=none, businessType=none-in-request, domain=in_Domain+out_Domain)`. Matches `connectors/entsoe/endpoints.py` `cross_border_flows` entry. PASS.
- **Live validation 2026-05-08:** GB → FR for 2026-05-06, returned `Publication_MarketDocument` with 1 TimeSeries, 24 hourly points. PASS.
- **Schema field set (G5-W3, 2026-05):** `EntsoeCrossborderFlow` now declares all seven columns the transformer emits — `timestamp_utc`, `in_area_code`, `out_area_code`, `flow_mw`, `resolution`, `data_provider`, `ingested_at` (`resolution` and `ingested_at` were added per the schema docstring; they previously drifted from the V1 §13 declaration). The silver Parquet column set matches the schema declaration. `published_at` has since been added (ADR-025 P1.1, `cross_border_flows.py:83-84`, `schemas/entsoe.py:88`), making eight.

---

## Modelling notes

- Used as feature for GB interconnector utilisation models, day-ahead price
  spread models, and congestion-rent models.
- Net interconnector flow = `flow_mw(GB→X) − flow_mw(X→GB)` per timestamp;
  consume both directions. gridflow cannot serve this yet: it requests one direction
  per border (`connectors/entsoe/client.py:40-49`).
- Quality filter: drop rows where the same `(timestamp_utc, in, out)` appears
  with multiple revisions, keep the last fetched (already done in silver: a day's
  bronze files are read in name order, fetch time first, then `unique(..., keep="last")`,
  `cross_border_flows.py:37,73`; `ingested_at` is the silver write time, the same on every row of a run).

---

## Links

- [Official API docs (PDF)](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/cross_border_flows.py`
- `src/gridflow/schemas/entsoe.py`
- [Gold view/builder](../../../../) (none)
