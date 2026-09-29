---
source: entsoe
dataset_key: generation_forecast
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Day-ahead generation forecast
  summary: >-
    ENTSO-E's day-ahead forecast of aggregated generation per bidding zone: one MW total per
    target time, with no split by production type.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A71, process type A01
    cadence: Every 15 minutes for DE-LU, FR and NL, hourly for BE, in these responses
    grain: One row per target time and bidding zone; a re-fetch replaces it
  landscape: power
  what_it_is: >-
    ENTSO-E's day-ahead aggregated generation forecast: one MW total per bidding zone and target
    time. The responses charted carry no production type. gridflow requests six zones; for this
    window GB and IE-SEM came back empty. A response can also carry an `outBiddingZone_Domain`
    series, which silver cannot tell apart; it keeps whichever comes later in the document.
  how_used:
    - Supply-side feature per bidding zone for a continental day-ahead price model.
    - Less the load forecast, a day-ahead surplus or shortfall per zone.
    - Scoring TSO forecast skill against actual generation summed per zone.
  chart:
    type: line
    silver: entsoe/generation_forecast
    time: timestamp_utc
    value: generation_forecast_mw
    group: area_code
    group_map:
      "10Y1001A1001A82H": de_lu
      "10YFR-RTE-\x2D-\x2D-\x2DC": fr
      "10YNL-\x2D-\x2D-\x2D-\x2D-\x2DL": nl
      "10YBE-\x2D-\x2D-\x2D-\x2D-\x2D2": be
    series_order: [de_lu, fr, nl, be]
    aggregation: mean
    time_bucket: 1h
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: Generation forecast by zone, 14 to 20 September 2026
    caption: >-
      Silver `entsoe/generation_forecast`, MW, target hours of 14 to 20 September 2026, UTC.
      DE-LU, FR and NL are sent per quarter-hour and shown as hourly means; BE is sent hourly.
    alt: >-
      Line chart of entsoe/generation_forecast, hourly mean MW by bidding zone, for target hours
      14 to 20 September 2026, UTC. DE-LU is highest, peaking each day at 10:00 or 11:00 UTC, from
      59,500 MW on the 14th to 77,208 MW on the 17th, with overnight lows of 30,584 to 44,632 MW.
      France runs from 36,908 to 63,638 MW, lower at the weekend. The Netherlands runs from 7,362
      to 14,432 MW, lowest around midday on most days. Belgium runs from 2,033 to 7,742 MW.
    x_label: target hour, UTC
    key:
      - {series: de_lu, label: Germany and Luxembourg, codes: DE-LU, paint: petrol}
      - {series: fr, label: France, codes: FR, paint: horizon}
      - {series: nl, label: Netherlands, codes: NL, paint: olive}
      - {series: be, label: Belgium, codes: BE, paint: clay, note: "Sent hourly, so no averaging."}
  raw_feed:
    note: >-
      From the ENTSO-E web API, one request per bidding zone and UTC day. `gridflow ingest` writes
      each XML response to bronze; `gridflow transform` types it into silver.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A71&periodStart=202609200000&periodEnd=202609210000&in_Domain=10Y1001A1001A82H&processType=A01&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe generation_forecast --start 2026-09-14 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform entsoe generation_forecast --start 2026-09-14 --end 2026-09-20, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: in, value: ["2026-09-20T12:00:00Z", "2026-09-20T13:00:00Z"]}
      order_by: [timestamp_utc, area_code]
      columns: [timestamp_utc, area_code, generation_forecast_mw, resolution, published_at, production_type]
    key: [timestamp_utc, area_code, production_type]
    caption: "Target times 12:00 and 13:00 UTC on 20 September 2026, for each of the four zones."
    fields:
      timestamp_utc: "Target time: start of the step, period start plus (position minus 1) steps, UTC"
      area_code: "Bidding zone EIC, from `inBiddingZone_Domain` or `outBiddingZone_Domain`; silver cannot tell which"
      generation_forecast_mw: "Forecast `quantity` in MW (`MAW`); omitted A03 positions repeat the previous value"
      resolution: "Step as sent: `PT15M` or `PT60M`"
      published_at: "Response `createdDateTime`; here within seconds of gridflow's fetch, not an issue time"
      production_type: "PSR type code when sent; these responses send none, so it is empty"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_entsoe_generation_forecast`,
      filtered on `timestamp_utc`, the target time, as whole UTC days with both ends included.
      Lineage columns are dropped.
    cells:
      - |
        df = data.entsoe.query("generation_forecast", "2026-09-14", "2026-09-20")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
      - df.sort_values(["timestamp_utc", "area_code"])[["timestamp_utc", "area_code", "generation_forecast_mw", "resolution"]].head()
      - |
        de = df[df.area_code == "10Y1001A1001A82H"].sort_values("timestamp_utc")
        de.plot(x="timestamp_utc", y="generation_forecast_mw", ylabel="MW",
                color="#155A6E", figsize=(8, 3.5))
    needs: 14 to 20 September 2026
    plot_alt: >-
      Line plot of generation_forecast_mw against timestamp_utc for DE-LU, every quarter-hour of
      14 to 20 September 2026: one peak each day between 10:15 and 11:15 UTC, from 59,597 MW on
      the 14th to 77,609 MW on the 17th, and overnight lows from 30,443 MW on the 14th to 44,567
      MW on the 20th.
  related:
    - {dataset: entsoe/wind_solar_forecast, note: "Day-ahead wind and solar forecast for the same zones"}
    - {dataset: entsoe/actual_generation, note: "Outturn per production type; summed per zone, it scores this forecast"}
    - {dataset: entsoe/load_forecast, note: "Day-ahead load forecast; the demand side of the same day"}
    - {dataset: entsoe/day_ahead_prices, note: "Day-ahead prices for the same bidding zones"}
---

# ENTSO-E — Day-ahead generation forecast aggregated (A71/A01)

## Overview

Day-ahead total aggregated generation forecast in MW per bidding zone,
one total per zone (no `MktPSRType` in the 2026-08/09 responses). Distinct from `wind_solar_forecast` (A69)
in that A71/A01 covers all dispatchable + non-dispatchable types, whereas
A69 covers only the variable renewables. Used as a TSO-published reference
for total generation expectation.

→ [Wind/solar forecast](wind_solar_forecast.md), [Actual generation](actual_generation.md)

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
| Historical depth | 2014-12-05 onwards |
| Publication lag  | Published D-1 ~18:00 UTC |
| Response format  | XML — root `GL_MarketDocument` |
| Document type    | A71 |
| Process type     | A01 (day-ahead) |
| Business type    | n/a |
| Domain param name| `in_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | str | yes | `A71` | `A71` |
| `processType` | str | yes | `A01` | `A01` |
| `in_Domain` | EIC | yes | Bidding zone | `10Y1001A1001A82H` |
| `periodStart` | str | yes | UTC `yyyymmddhhmm` | `202605060000` |
| `periodEnd` | str | yes | UTC `yyyymmddhhmm` | `202605070000` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A71&processType=A01&in_Domain=10Y1001A1001A82H&periodStart=202605060000&periodEnd=202605070000" \
  -H "Accept: application/xml"
```

Live verification 2026-05-08:
- GB: HTTP 200, **EMPTY** (Ack 999 "DAY_AHEAD_AGGREGATED_GENERATION_R3 [14.1.C]"). Brexit-GB.
- DE-LU: HTTP 200, **PASS** — `GL_MarketDocument`, 1 TimeSeries.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/generation_forecast/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, immutable.
**Granularity**: One file per (zone, day).

### Bronze sample (DE-LU, truncated)

```xml
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <type>A71</type>
  <process.processType>A01</process.processType>
  <TimeSeries>
    <businessType>A01</businessType>
    <inBiddingZone_Domain.mRID>10Y1001A1001A82H</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <Period>
      <resolution>PT60M</resolution>
      <Point><position>1</position><quantity>52310</quantity></Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/generation_forecast/year=YYYY/month=MM/generation_forecast_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.generation_forecast.GenerationForecastTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeGenerationForecast`
**Dedup key**: `(timestamp_utc, area_code, production_type)`
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | Period start + (position - 1) * resolution (`parsers.py:530`) | tz-aware UTC |
| area_code | str | No | `<inBiddingZone_Domain.mRID>` | EIC |
| production_type | str | No | `<MktPSRType><psrType>` if present, else "" | A71/A01 aggregate has no MktPSRType, so the value is `""`: the parser returns an empty string and `fill_null("unknown")` only fills nulls (`parsers.py:269,345-348`, `generation_forecast.py:70-73`) |
| generation_forecast_mw | float | No | `<Point><quantity>` | MW |
| resolution | str | No | `<Period><resolution>` | ISO code as sent (`parsers.py:437-439,459`): `PT15M` for DE-LU, FR, NL and `PT60M` for BE in 2026-08/09 responses. |
| published_at | datetime[UTC] | Yes | `<createdDateTime>` | Document `createdDateTime`; typed-null when the source omits it. In the 2026-08/09 bronze it is within seconds of the fetch (`fetched_at` in the sidecar), so it is when the API answered, not the TSO's forecast issue time. |
| data_provider | str | No | constant | "entsoe" |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-05-05T22:00:00+00:00",
        "area_code": "10Y1001A1001A82H",
        "production_type": "",
        "generation_forecast_mw": 52310.0,
        "resolution": "PT60M",
        "data_provider": "entsoe",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB EMPTY post-Brexit.** No GB equivalent — Elexon publishes residual demand forecast (`ndf`) but not gross generation forecast.
- A71 is a **shared documentType with `installed_capacity_units`** — they're disambiguated by `processType` (A01 vs A33). Building the wrong tuple silently returns the other dataset's payload.
- Aggregate A71/A01 contains no `MktPSRType` element, so `production_type` is `""` in silver (not `"unknown"`: the fill only applies to nulls).
- Forecast revisions overwrite each other.
- A response can carry a second TimeSeries under `outBiddingZone_Domain.mRID` (BE, 2026-09-08). The parser maps it to the same `in_domain` as the generation series (`parsers.py:289-297`), and silver has no direction column, so `unique(keep="last")` on `(timestamp_utc, area_code, production_type)` keeps whichever series comes later in the document (`generation_forecast.py:75`). On that day the generation series came second and won.
- GB and IE-SEM return Acknowledgement reason 999 ("No matching data found") for every request in the 2026-08/09 bronze.

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §14.1.C): `(documentType=A71, processType=A01, businessType=n/a, in_Domain)`.
  - Code (`endpoints.py:DOC_TYPES["generation_forecast"]`): `("A71", "A01", -, domain_style="in_domain")` → `in_Domain`.
  - **Match.**
- A71 doc type is reused in code for `installed_capacity_units` (A71/A33) — different process type. Make sure consumers select on dataset key, not documentType alone.

---

## Modelling notes

- Demand-supply imbalance feature for price modelling: `generation_forecast - load_forecast`.
- Use as cross-check vs sum of A75 actual generation per zone — TSO forecast skill metric.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `OneDrive/Desktop/Python/gridflow/src/gridflow/connectors/entsoe/client.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/silver/entsoe/generation_forecast.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/schemas/entsoe.py`
- Gold view/builder
