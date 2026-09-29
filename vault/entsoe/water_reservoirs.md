---
source: entsoe
dataset_key: water_reservoirs
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Water reservoirs and hydro storage
  summary: >-
    The weekly average energy stored in a bidding zone's water reservoirs and hydro storage plants,
    in MWh, one figure per week.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A72, process type A16
    cadence: One `P7D` point per week in the responses gridflow holds
    grain: One row per week and zone per silver file; each day's file repeats it
  landscape: power
  what_it_is: >-
    Article 16(1)(d) of Regulation 543/2013: the aggregated weekly average filling of water
    reservoirs and hydro storage plants, in MWh, per bidding zone. Each point is stamped at its
    week's start, 22:00 UTC on a Sunday in these rows (midnight Monday in Paris). Of gridflow's six
    zones, only France returns a document in the responses it holds.
  how_used:
    - A slow-moving hydro stock feature for French medium-term power price models.
    - Comparing a week with the same week a year earlier, both years ingested.
    - Pairing the stock with `actual_generation` reservoir (B12) and pumped-storage (B10) output.
  chart:
    type: line
    silver: entsoe/water_reservoirs
    time: timestamp_utc
    value: reservoir_mwh
    filter:
      - {column: area_code, op: eq, value: "10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC"}
    dedup: {"on": [timestamp_utc, area_code], order_by: published_at}
    aggregation: last
    window: {start: "2026-07-26", end: "2026-09-13"}
    unit: MWh
  chart_view:
    title: France reservoir filling, 26 July to 13 September 2026
    caption: >-
      Silver `entsoe/water_reservoirs`, MWh, France, weekly averages stamped 22:00 UTC on the
      Sundays 26 July to 13 September 2026; each day's file repeats its week, so the latest copy is
      kept. No weeks stamped 9 to 30 August are drawn.
    alt: >-
      Line chart of France's weekly average reservoir filling from entsoe/water_reservoirs, in MWh,
      four weekly points, each drawn at the middle of its week. Two short segments: 2,261,238 MWh
      for the week stamped 26 July falling to 2,191,776 for 2 August, then 1,989,272 for 6
      September falling to 1,952,966 for 13 September. Nothing is drawn between the two segments.
    x_label: UTC date; points drawn mid-week
    key:
      - {series: reservoir_mwh, label: France, codes: FR, paint: petrol, note: "Weekly average in MWh, stamped at the week's start, Monday 00:00 Paris (22:00 UTC Sunday in CEST)."}
  raw_feed:
    note: >-
      One GET per zone per UTC day, six zones. In the responses gridflow holds only France returns
      a document, and a one-day request returns the week containing its start.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A72&periodStart=202609080000&periodEnd=202609090000&in_Domain=10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC&processType=A16&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe water_reservoirs --start 2026-07-27 --end 2026-09-15, comment: "bronze; end date excluded"}
      - {run: gridflow transform entsoe water_reservoirs --start 2026-07-27 --end 2026-09-14, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: area_code, op: eq, value: "10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC"}
        - {column: timestamp_utc, op: in, value: ["2026-07-26T22:00:00Z", "2026-09-06T22:00:00Z"]}
      order_by: [timestamp_utc, published_at]
      columns: [timestamp_utc, area_code, published_at, reservoir_mwh, resolution]
    key: [timestamp_utc, area_code, published_at]
    caption: "France, weeks stamped 26 July and 6 September: one copy per requested day, same value."
    fields:
      timestamp_utc: "Week start, UTC: period start plus (position minus 1) times `P7D`"
      area_code: "Bidding zone EIC, from `inBiddingZone_Domain.mRID`"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, so each day's copy differs"
      reservoir_mwh: "Weekly average filling in MWh, from `quantity`; the unit field is not stored"
      resolution: "Point length as sent; `P7D` in these rows"
  notebook:
    lead: >-
      `query()` filters `silver_entsoe_water_reservoirs` on `timestamp_utc`, whole UTC days, both
      ends included, and drops lineage columns. Every day's silver file repeats its week, so keep
      the latest copy of each.
    cells:
      - |
        df = data.entsoe.query("water_reservoirs", "2026-07-26", "2026-09-13")
        for col in ["timestamp_utc", "published_at"]:
            df[col] = df[col].dt.tz_convert("UTC")
        key = ["timestamp_utc", "area_code"]
        weekly = df.sort_values("published_at").drop_duplicates(subset=key, keep="last").sort_values(key)
      - weekly[["timestamp_utc", "area_code", "reservoir_mwh", "published_at"]]
      - |
        fr = weekly[weekly["area_code"].str.startswith("10YFR")].set_index("timestamp_utc")
        gwh = fr["reservoir_mwh"].asfreq("7D") / 1000
        gwh.plot(marker="o", ylabel="GWh, weekly average", legend=False, color="#155A6E", figsize=(8, 3.5))
    needs: 27 July to 14 September 2026
    plot_alt: >-
      Line plot of France's weekly reservoir filling in GWh against week start, 26 July to 13
      September 2026, with markers. About 2,261 GWh on 26 July falls to 2,192 on 2 August; after a
      break, about 1,989 on 6 September falls to 1,953 on 13 September.
  related:
    - {dataset: entsoe/actual_generation, note: "Reservoir (B12) and pumped-storage (B10) output drawing on this stock"}
    - {dataset: entsoe/installed_capacity, note: "France's installed reservoir and pumped-storage MW behind the stock"}
    - {dataset: entsoe/day_ahead_prices, note: "French prices that hydro-stock features are modelled against"}
---

# ENTSO-E — Water reservoirs and hydro storage plants (A72/A16)

## Overview

Aggregated weekly water-reservoir filling level (energy stored in MWh) per
bidding zone. Published once per week. Used as a slow-moving structural
driver of hydro-rich price markets (Nordic, Iberian, Italian) — low
filling rates strengthen prices on multi-week horizons. Resolution `P7D`,
unit MWh.

Vendor definition (the no-data acknowledgement names the data item
`AGGREGATE_FILLING_RATE_OF_WATER_RESERVOIRS_R3 [16.1.D]`): Regulation (EU)
No 543/2013 Article 16(1)(d), "aggregated weekly average filling rate of all
water reservoir and hydro storage plants (MWh) per bidding zone including the
figure for the same week of the previous year"; Article 16(2)(d): published "on
the third working day following the week to which the information relates"
(https://www.legislation.gov.uk/eur/2013/543/article/16, read 2026-09-29).

→ [Domain: Hydro](../../../20-domain/concepts/hydro.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | https://web-api.tp.entsoe.eu |
| Path             | /api |
| Method           | GET |
| Auth             | query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | 1 req/s |
| Pagination       | None |
| Historical depth | ~2014 onwards (varies by area) |
| Publication lag  | third working day after the week (Reg. 543/2013 Art. 16(2)(d)) |
| Response format  | XML — root `GL_MarketDocument`, resolution `P7D`, unit `MWH` |
| Document type    | A72 |
| Process type     | A16 (realised) |
| Business type    | n/a (TimeSeries businessType=A01 typical) |
| Domain param name| `in_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | str | yes | `A72` | `A72` |
| `processType` | str | yes | `A16` | `A16` |
| `in_Domain` | EIC | yes | Bidding zone | `10YNO-1--------2` |
| `periodStart` | str | yes | UTC `yyyymmddhhmm` | `202604010000` |
| `periodEnd` | str | yes | UTC `yyyymmddhhmm` | `202605010000` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A72&processType=A16&in_Domain=10YNO-1--------2&periodStart=202604010000&periodEnd=202605010000" \
  -H "Accept: application/xml"
```

Live verification 2026-05-08:
- GB 1-day window: HTTP 200, **EMPTY** (Ack 999 "AGGREGATE_FILLING_RATE_OF_WATER_RESERVOIRS_R3 [16.1.D]"). GB is hydro-light and does not publish A72.
- ES 1-day window: HTTP 200, **EMPTY** — too short (P7D resolution).
- NO-1 30-day window: HTTP 200, **PASS** — `GL_MarketDocument`, 1 TimeSeries with weekly Points. `quantity_Measure_Unit.name = MWH`. Quantity ~10176 MWh per week.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/water_reservoirs/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per (zone, day).

### Bronze sample (NO-1 truncated)

```xml
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <type>A72</type>
  <process.processType>A16</process.processType>
  <TimeSeries>
    <mRID>1</mRID>
    <businessType>A01</businessType>
    <inBiddingZone_Domain.mRID codingScheme="A01">10YNO-1--------2</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MWH</quantity_Measure_Unit.name>
    <Period>
      <timeInterval>
        <start>2026-03-29T22:00Z</start><end>2026-05-03T22:00Z</end>
      </timeInterval>
      <resolution>P7D</resolution>
      <Point><position>1</position><quantity>10176</quantity></Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/water_reservoirs/year=YYYY/month=MM/water_reservoirs_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.water_reservoirs.WaterReservoirsTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeWaterReservoirs`
**Dedup key**: `(timestamp_utc, area_code)`, within one silver file only (`silver/entsoe/water_reservoirs.py:59`). A one-day request returns the whole week containing its start (bronze `2026/08/01` and `2026/08/02` FR files both carry the week starting `2026-07-26T22:00Z`), so every daily file repeats its week; dedup across files on `published_at`.
**Point-in-time field**: `published_at` (document `createdDateTime`, `water_reservoirs.py:70`; within seconds of the fetch)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | Period start + (position - 1) × resolution (`parsers.py:530`) | Weekly resolution P7D; the week's start |
| area_code | str | No | `<inBiddingZone_Domain.mRID>` | EIC |
| reservoir_mwh | float | No | `<Point><quantity>` | Unit `MWH` per the response (renamed from `value`) |
| resolution | str | No | parsed | Default "" in canonical. `P7D` typical. |
| published_at | datetime[UTC] | Yes | `<createdDateTime>` | Fetch-time stamp (`water_reservoirs.py:70`) |
| data_provider | str | No | constant | "entsoe" |
| ingested_at | datetime[UTC] | Yes | derived | Silver transform time (`water_reservoirs.py:61`) |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-03-29T22:00:00+00:00",
        "area_code": "10YNO-1--------2",
        "reservoir_mwh": 10176.0,
        "resolution": "P7D",
        "data_provider": "entsoe",
        "ingested_at": "2026-05-08T18:00:00+00:00",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Use a 30-day window minimum** — P7D resolution means a 1-day window returns no data even when the zone publishes. (Not so for FR: gridflow's one-day FR requests, e.g. bronze `2026/08/01` `periodStart=202608010000&periodEnd=202608020000`, return the whole week containing the request start. The ES probe above stands as recorded.)
- **GB / DE-LU / IE-SEM EMPTY** — these zones have no significant hydro reservoir reporting. Hydro markets: NO, SE, ES, IT, FR, AT, CH, DK-2. (In gridflow's bronze for August and September 2026, NL and BE also return no-data acknowledgements; FR is the only default zone that returns a document.)
- Unit is **MWh** not MW — different dimensionality from generation datasets. Don't sum across with generation series.
- Some zones report energy (MWh), others percentage filling — the silver schema uses `reservoir_mwh` consistent with the Norwegian / Iberian publication convention. (Unverified: no source cited. The parser never reads `quantity_Measure_Unit.name` (`parsers.py` TimeSeries loop, 286-360), so silver carries no unit; every FR response gridflow holds says `MWH`.)

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §16.1.D): `(documentType=A72, processType=A16, businessType=n/a, in_Domain)`.
  - Code: `("A72", "A16", -, domain_style="in_domain")` → `in_Domain`.
  - **Match.**
- Default `DEFAULT_ZONES` in `endpoints.py` is GB-centric (GB, FR, NL, BE, DE-LU, IE-SEM) — only FR returns A72 data. There is no way to request another zone: `_build_unit_tasks` loops `DEFAULT_ZONES` unconditionally (`client.py:249`) and `**params` forwards only the doc type's `optional_params` (`client.py:306`), which A72 does not declare (`endpoints.py:113`). Flag as a config gap (not a code bug).

---

## Modelling notes

- Slow-moving feature for medium-term price models (Nordic / Iberian).
- Combine with snowpack / precipitation forecasts for hydro-driven price regimes.
- Differential ratio vs five-year median is the standard hydrological balance feature.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `OneDrive/Desktop/Python/gridflow/src/gridflow/connectors/entsoe/client.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/silver/entsoe/water_reservoirs.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/schemas/entsoe.py`
- Gold view/builder
