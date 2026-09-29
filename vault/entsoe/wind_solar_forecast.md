---
source: entsoe
dataset_key: wind_solar_forecast
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Day-ahead wind and solar forecast
  summary: >-
    ENTSO-E's day-ahead forecast of wind and solar generation per bidding zone, in MW; gridflow
    keeps one value per target time.
  facts:
    vendor: ENTSO-E Transparency Platform, document A69, process A01 (day-ahead)
    cadence: Day-ahead; interval from the response's `resolution`, PT15M or PT60M in these responses
    grain: One row per target time, bidding zone and production type
  landscape: power
  what_it_is: >-
    ENTSO-E's day-ahead forecast of wind and solar generation, in MW, for each bidding zone
    gridflow asks for: GB, FR, NL, BE, DE-LU and IE-SEM. The codes are B16 solar, B18 wind
    offshore and B19 wind onshore. GB answers with an acknowledgement and no data. Silver keeps
    one forecast per target time; the document carries no forecast issue time.
  how_used:
    - A zone's forecast wind and solar as a feature for a day-ahead price model.
    - Residual load ahead of delivery, from the load forecast less forecast wind and solar.
    - Forecast error by production type, scored against outturn under the same codes.
  chart:
    type: stacked-area
    silver: entsoe/wind_solar_forecast
    time: timestamp_utc
    value: generation_forecast_mw
    filter:
      - {column: area_code, op: eq, value: 10Y1001A1001A82H}
    group: production_type
    group_map:
      B16: solar
      B18: wind_offshore
      B19: wind
    series_order: [wind_offshore, wind, solar]
    aggregation: sum
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: DE-LU forecast, 14 to 20 September 2026
    caption: >-
      Silver `entsoe/wind_solar_forecast`, MW, bidding zone DE-LU, every 15-minute target interval
      of 14 to 20 September 2026 UTC, one production type per band, stacked. Day-ahead forecast
      values, not outturn.
    alt: >-
      Stacked area chart of the day-ahead wind and solar forecast for bidding zone DE-LU from
      entsoe/wind_solar_forecast, in MW, every 15 minutes of 14 to 20 September 2026 UTC. From
      zero upward: wind offshore (251 to 6,885), wind onshore (570 at 17:00 on the 14th to 36,442
      at 15:45 on the 20th) and solar (zero every night, peaking at 46,739 at 10:30 on the 15th). The total runs from 1,834 at 17:45 on the 14th to 63,664 at 11:00 on the 17th.
    x_label: target time, UTC
    key:
      - {series: solar, label: Solar, codes: B16, tag: solar}
      - {series: wind, label: Wind onshore, codes: B19, tag: onshore}
      - {series: wind_offshore, label: Wind offshore, codes: B18, paint: hatch-lines}
  raw_feed:
    note: >-
      From the ENTSO-E API, one request per zone and UTC day. `gridflow transform` fills the
      vendor's A03 blocks, keeping one value per target time, zone and code within that day.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A69&periodStart=202609140000&periodEnd=202609150000&in_Domain=10Y1001A1001A82H&processType=A01&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe wind_solar_forecast --start 2026-09-14 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform entsoe wind_solar_forecast --start 2026-09-14 --end 2026-09-20, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: eq, value: "2026-09-14T22:00:00Z"}
        - {column: production_type, op: in, value: [B16, B19]}
      order_by: [area_code, production_type]
      columns: [timestamp_utc, area_code, production_type, generation_forecast_mw, resolution, published_at]
    key: [timestamp_utc, area_code, production_type]
    caption: "Target time 22:00 UTC, 14 September 2026: solar (B16) and onshore wind (B19), four zones."
    fields:
      timestamp_utc: "Start of the target interval, from the period start and point position, UTC"
      area_code: "Bidding zone EIC, from `inBiddingZone_Domain.mRID`"
      production_type: "ENTSO-E PSR code: B16 solar, B18 wind offshore, B19 wind onshore"
      generation_forecast_mw: "Forecast from the point `quantity`; the document's unit is MAW, megawatts"
      resolution: "Interval length from the period `resolution`, as the zone sends it"
      published_at: "Document `createdDateTime`: a fetch-time stamp, not the forecast's issue time"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_entsoe_wind_solar_forecast`,
      filtered on `timestamp_utc`, whole UTC days with both ends included. Lineage columns are
      dropped; `published_at` and `ingested_at` stay.
    cells:
      - |
        df = data.entsoe.query("wind_solar_forecast", "2026-09-14", "2026-09-20")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
      - |
        de = df[df.area_code == "10Y1001A1001A82H"].sort_values(["timestamp_utc", "production_type"])
        de[["timestamp_utc", "area_code", "production_type", "generation_forecast_mw"]].head()
      - |
        wide = de.pivot(index="timestamp_utc", columns="production_type", values="generation_forecast_mw")
        wide = wide.rename(columns={"B16": "solar", "B18": "wind offshore", "B19": "wind onshore"})
        ax = wide.plot.area(ylabel="MW", figsize=(8, 3.5), ylim=(0, 80000))
        ax.legend(ncol=3, loc="upper left");
    needs: 14 to 20 September 2026
    plot_alt: >-
      Stacked area plot of generation_forecast_mw against timestamp_utc for DE-LU, 14 to 20
      September 2026, solar at the bottom, then wind offshore and wind onshore. Solar forms a daily
      hump that falls to zero each night; the total peaks near 64,000 MW on the 17th and is
      lowest, near 1,800 MW, on the evening of the 14th.
  related:
    - {dataset: entsoe/actual_generation, note: "Outturn under the same B16, B18 and B19 codes, to score these"}
    - {dataset: entsoe/load_forecast, note: "Day-ahead load forecast; less wind and solar, it gives residual load"}
    - {dataset: entsoe/day_ahead_prices, note: "Day-ahead prices for the same zones and delivery days"}
    - {dataset: elexon/windfor, note: "GB wind forecast; ENTSO-E returns no A69 data for GB"}
---

# ENTSO-E — Day-ahead wind / solar generation forecast (A69/A01)

## Overview

Day-ahead generation forecast in MW for the wind-onshore (B19), wind-offshore
(B18) and solar (B16) production types per bidding zone (codes per
`silver/entsoe/wind_solar_forecast.py:23-24`, `schemas/entsoe.py:127`). Published once per
day around 18:00 D-1 UTC. Used as the canonical reference forecast for
pricing models and as a benchmark for in-house wind/solar nowcast skill.

→ [Actual generation](actual_generation.md), [Generation forecast](generation_forecast.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | https://web-api.tp.entsoe.eu |
| Path             | /api |
| Method           | GET |
| Auth             | query param `securityToken=$ENTSOE_API_KEY` |
| Rate limit       | not documented — code uses 1 req/s |
| Pagination       | None |
| Historical depth | 2014-12-05 onwards |
| Publication lag  | Published D-1 ~18:00 UTC; refreshed intraday |
| Response format  | XML — root `GL_MarketDocument` |
| Document type    | A69 |
| Process type     | A01 (day-ahead) |
| Business type    | n/a |
| Domain param name| `in_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `documentType` | str | yes | `A69` | `A69` |
| `processType` | str | yes | `A01` | `A01` |
| `in_Domain` | EIC | yes | Bidding zone | `10YGB----------A` |
| `periodStart` | str | yes | UTC `yyyymmddhhmm` | `202605060000` |
| `periodEnd` | str | yes | UTC `yyyymmddhhmm` | `202605070000` |
| `psrType` | str | no | Filter to one of B16/B18/B19 | `B19` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  "https://web-api.tp.entsoe.eu/api?securityToken=$ENTSOE_API_KEY&documentType=A69&processType=A01&in_Domain=10Y1001A1001A82H&periodStart=202605060000&periodEnd=202605070000" \
  -H "Accept: application/xml"
```

Live verification 2026-05-08:
- GB: HTTP 200, **EMPTY** (Acknowledgement reason 999 "GENERATION_FORECAST_WIND_SOLAR [14.1.D]"). Brexit-GB.
- DE-LU: HTTP 200, **PASS** — `GL_MarketDocument`, 3 TimeSeries (B16 / B18 / B19).

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/wind_solar_forecast/<year>/<month>/<day>/raw_<fetch-ts>_<body-hash>.xml` (`bronze/writer.py:57`)
**Format**: Raw XML, immutable.
**Granularity**: One file per (zone, day, fetch).

### Bronze sample (DE-LU, truncated)

```xml
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
  <type>A69</type>
  <process.processType>A01</process.processType>
  <TimeSeries>
    <businessType>A93</businessType>
    <inBiddingZone_Domain.mRID>10Y1001A1001A82H</inBiddingZone_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <MktPSRType><psrType>B19</psrType></MktPSRType>
    <Period>
      <timeInterval>...</timeInterval>
      <resolution>PT15M</resolution>
      <Point><position>1</position><quantity>0</quantity></Point>
    </Period>
  </TimeSeries>
</GL_MarketDocument>
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/wind_solar_forecast/year=YYYY/month=MM/wind_solar_forecast_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.wind_solar_forecast.WindSolarForecastTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeWindSolarForecast`
**Dedup key**: `(timestamp_utc, area_code, production_type)`
**Point-in-time field**: `published_at` (response creation time, not the forecast issue time; see the schema table)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | No | derived from Period start + position | UTC tz-aware |
| area_code | str | No | `<inBiddingZone_Domain.mRID>` | EIC |
| production_type | str | No | `<MktPSRType><psrType>` | B16=solar, B18=wind offshore, B19=wind onshore (`schemas/entsoe.py:132`) |
| generation_forecast_mw | float | No | `<Point><quantity>` | renamed from `value` |
| resolution | str | No | parsed | Default "" in canonical. `PT15M` / `PT60M`. |
| published_at | datetime[UTC] | Yes | `<createdDateTime>` | Response document creation time; on the A69 responses checked (bronze Aug and Sep 2026) it falls within seconds of the sidecar `fetched_at`, so it is the fetch time, not the forecast issue time. Typed-null when the source omits it. |
| data_provider | str | No | constant | "entsoe" |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-09-14T22:00:00+00:00",
        "area_code": "10Y1001A1001A82H",
        "production_type": "B16",
        "generation_forecast_mw": 0.0,
        "resolution": "PT15M",
        "published_at": "2026-09-21T10:07:59+00:00",
        "data_provider": "entsoe",
    },
    {
        "timestamp_utc": "2026-09-14T22:00:00+00:00",
        "area_code": "10Y1001A1001A82H",
        "production_type": "B19",
        "generation_forecast_mw": 3458.69357,
        "resolution": "PT15M",
        "published_at": "2026-09-21T10:07:59+00:00",
        "data_provider": "entsoe",
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB EMPTY post-Brexit.** Use Elexon `windfor` for GB wind forecasts.
- A69 carries B16 (solar), B18 (wind offshore) and B19 (wind onshore); the September 2026 responses for DE-LU, FR, NL and BE each carry all three (bronze and silver, 14 to 20 Sep).
- Forecast revisions during the day overwrite each other in silver — no point-in-time. Re-running ingestion late in the day may change historical files.
- In the September 2026 responses, DE-LU, FR and NL send PT15M and BE and IE-SEM send PT60M (silver `resolution`, 14 to 20 Sep); ENTSO-E states no rule.
- Series are `curveType` A03: omitted positions repeat the previous value, and the parser forward-fills them (`connectors/entsoe/parsers.py:533-600`), so silver holds more points than bronze declares.

---

## Implementation delta

- Tuple verified 2026-05-08:
  - Docs (API guide §14.1.D): `(documentType=A69, processType=A01, businessType=n/a, in_Domain)`.
  - Code: `("A69", "A01", -, domain_style="in_domain")` → `in_Domain`.
  - **Match.**
- `psrType` is documented as optional filter; it is in the `optional_params` tuple (`connectors/entsoe/endpoints.py:49`), so the connector forwards it when passed.

---

## Modelling notes

- Day-ahead price models — wind/solar forecast is the dominant negative pressure on prices.
- Forecast-error features — `(actual - forecast) / forecast` per production type.
- Use as benchmark for in-house weather-driven nowcasts.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf)
- `OneDrive/Desktop/Python/gridflow/src/gridflow/connectors/entsoe/client.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/silver/entsoe/wind_solar_forecast.py`
- `OneDrive/Desktop/Python/gridflow/src/gridflow/schemas/entsoe.py`
- Gold view/builder
