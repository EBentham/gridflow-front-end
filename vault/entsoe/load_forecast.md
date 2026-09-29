---
source: entsoe
dataset_key: load_forecast
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Load forecasts at four horizons
  summary: >-
    ENTSO-E's total load forecasts per bidding zone, in MW: day-ahead per interval; week-, month-
    and year-ahead with one of two values kept.
  facts:
    vendor: ENTSO-E Transparency Platform, document A65; processes A01, A31, A32, A33 (Article 6.1)
    cadence: Day-ahead `PT15M` in every response charted; week-ahead per day; month- and year-ahead per week
    grain: "Day-ahead: one row per bidding zone and interval start, from the latest fetch"
  landscape: power
  what_it_is: >-
    Regulation 543/2013 (Article 6.1) sets four total load forecasts per bidding zone: day-ahead
    per interval; week-ahead, a maximum and minimum per day; month- and year-ahead, per week.
    gridflow keeps one of each pair (`A61`); no quoted source says which. Total load:
    generation plus imports, minus exports and storage use (Article 2.27). GB and IE-SEM got code
    999 on charted days.
  how_used:
    - The benchmark a zonal load model has to beat, once fetched before delivery.
    - Residual load forecast per zone, net of `wind_solar_forecast`.
  chart:
    type: line
    silver: entsoe/load_forecast
    time: timestamp_utc
    value: load_forecast_mw
    group: area_code
    group_map:
      "10Y1001A1001A82H": de_lu
      "10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC": fr
      "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL": nl
      "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2": be
    series_order: [de_lu, fr, nl, be]
    aggregation: last
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: MW
  chart_view:
    title: Day-ahead load forecast by zone, 14 to 20 September 2026
    caption: >-
      Silver `entsoe/load_forecast` (day-ahead) only, MW, every 15-minute value over the UTC days
      14 to 20 September 2026, one line per zone. Values as ENTSO-E served them on 21 September,
      after delivery; the document carries no issue time.
    alt: >-
      Line chart of the day-ahead total load forecast from entsoe/load_forecast, in MW, every 15
      minutes from 14 to 20 September 2026 (UTC), one line per zone. DE-LU runs highest throughout,
      with weekday peaks of 61.8 to 63.4 GW, weekend peaks of 52.0 and 51.5 GW and a low of 37.2 GW
      at 01:45 UTC on the 20th. FR runs between 31.3 and 51.8 GW. NL and BE stay between 6.7 and
      13.3 GW; NL's lowest, 7.6 GW, falls at 13:30 UTC on the 19th.
    x_label: UTC date; each starts at 00:00
    key:
      - {series: de_lu, label: Germany and Luxembourg (DE-LU), paint: petrol}
      - {series: fr, label: France (FR), paint: horizon}
      - {series: nl, label: Netherlands (NL), paint: clay}
      - {series: be, label: Belgium (BE), paint: olive}
  raw_feed:
    note: >-
      From the ENTSO-E Transparency Platform API: one XML document per zone and UTC day for each
      member; the others swap `processType` to `A31`, `A32` or `A33`. Same commands, name swapped.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A65&periodStart=202609140000&periodEnd=202609150000&outBiddingZone_Domain=10Y1001A1001A82H&processType=A01&securityToken=<your-entsoe-api-key>"
    commands:
      - {run: gridflow ingest entsoe load_forecast --start 2026-09-14 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform entsoe load_forecast --start 2026-09-14 --end 2026-09-20, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: ge, value: "2026-09-15T11:00:00Z"}
        - {column: timestamp_utc, op: le, value: "2026-09-15T11:15:00Z"}
      order_by: [timestamp_utc, area_code]
      columns: [timestamp_utc, area_code, load_forecast_mw, published_at, resolution, forecast_horizon]
    key: [timestamp_utc, area_code]
    caption: "All four zones with rows, at 11:00 and 11:15 UTC on 15 September 2026."
    fields:
      timestamp_utc: "Interval start, UTC: period start plus (position minus 1) times resolution"
      area_code: "Bidding zone EIC as sent; `10Y1001A1001A82H` is DE-LU"
      load_forecast_mw: "Forecast total load in MW: the point's `quantity`, unit `MAW`"
      published_at: "Fetch time (`createdDateTime`), not an issue time; the latest fetch per interval wins"
      resolution: "Interval length as ENTSO-E sends it; `PT15M` is 15 minutes"
      forecast_horizon: "Constant per table: `day_ahead` here; `week_ahead`, `month_ahead`, `year_ahead` in the others"
  notebook:
    lead: >-
      Returns pandas DataFrames from `silver_entsoe_load_forecast` and `silver_entsoe_actual_load`:
      whole UTC days on `timestamp_utc`, both ends included, lineage dropped. The cells score the
      forecast as fetched on 21 September, after delivery, not as issued.
    cells:
      - |
        fc = data.entsoe.query("load_forecast", "2026-09-14", "2026-09-20")
        act = data.entsoe.query("actual_load", "2026-09-14", "2026-09-20")
        keys = ["timestamp_utc", "area_code"]
        both = fc.merge(act, on=keys).sort_values(keys, ignore_index=True)
      - |
        both["error_mw"] = both.load_forecast_mw - both.load_mw
        both[keys + ["load_forecast_mw", "load_mw", "error_mw"]].head()
      - |
        both.groupby("area_code").error_mw.agg(lambda s: s.abs().mean()).round()
      - |
        err = both.pivot_table(index="timestamp_utc", columns="area_code", values="error_mw")
        ax = err.plot(ylabel="forecast minus actual, MW", figsize=(8, 3.5))
        ax.legend(ncols=2, loc="lower center", bbox_to_anchor=(0.5, 1.0));
    needs: load_forecast and actual_load, 14 to 20 September 2026
    plot_alt: >-
      Line plot of forecast minus actual load, in MW, per area_code, 14 to 20 September 2026 on a
      UTC+1 clock. NL peaks at 6,602, 6,030 and 6,698 MW near midday on the 15th, 18th and 20th.
      DE-LU runs from -4,186 MW to a one-interval 4,157 MW just after midnight on the 17th. FR
      stays within 2,300 MW, BE within 1,100.
  related:
    - {dataset: entsoe/actual_load, note: "The outturn to score this forecast against, same zones and intervals"}
    - {dataset: entsoe/wind_solar_forecast, note: "Day-ahead wind and solar forecast; subtract it for residual load"}
    - {dataset: entsoe/forecast_margin, note: "Year-ahead margin, the same `A33` process as `load_forecast_yearly`"}
    - {dataset: elexon/ndf, note: "GB demand forecast; gridflow's GB calls to ENTSO-E returned code 999"}
  family:
    slug: load-forecasts
    members:
      - dataset: load_forecast
        differs: "Day-ahead (`A01`): one MW value per interval, `PT15M` as charted"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A65&periodStart=202609140000&periodEnd=202609150000&outBiddingZone_Domain=10Y1001A1001A82H&processType=A01&securityToken=<your-entsoe-api-key>"
      - dataset: load_forecast_weekly
        differs: "`A31`, per day: of the regulated maximum and minimum, silver keeps one (`A61`)"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A65&periodStart=202609140000&periodEnd=202609150000&outBiddingZone_Domain=10Y1001A1001A82H&processType=A31&securityToken=<your-entsoe-api-key>"
      - dataset: load_forecast_monthly
        differs: "`A32`, weekly: one of maximum and minimum kept (`A61`); weeks repeat per day fetched"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A65&periodStart=202609140000&periodEnd=202609150000&outBiddingZone_Domain=10Y1001A1001A82H&processType=A32&securityToken=<your-entsoe-api-key>"
      - dataset: load_forecast_yearly
        differs: "`A33`, weekly: one of maximum and minimum kept (`A61`); weeks repeat per day fetched"
        request: "GET https://web-api.tp.entsoe.eu/api?documentType=A65&periodStart=202609140000&periodEnd=202609150000&outBiddingZone_Domain=10Y1001A1001A82H&processType=A33&securityToken=<your-entsoe-api-key>"
---

# ENTSO-E — Day-ahead Load Forecast (A65/A01)

## Overview

Day-ahead total load forecast in MW per bidding zone — TSO-published
prediction for the following day, used as the reference forecast against
which actual load (A65/A16) measures forecast error. Document type `A65`
+ process type `A01` ("Day ahead"). Resolution `PT15M` in all 104 data
responses in bronze (1 Aug to 20 Sep 2026, checked 2026-09-29).

Legal basis: Regulation (EU) No 543/2013, Article 6(1)(b), "a day-ahead
forecast of the total load per market time unit". Article 2(27): "'total
load', including losses without power used for energy storage, means a load
equal to generation and any imports deducting any exports and power used for
energy storage". Text from the retained copy at
https://www.legislation.gov.uk/eur/2013/543 (EUR-Lex returned an empty page,
2026-09-29).

Related domain notes:
  [Load forecast](../../../20-domain/concepts/load-forecast.md)
  [Forecast error](../../../20-domain/concepts/forecast-error.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://web-api.tp.entsoe.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | Query param `securityToken` from env var `ENTSOE_API_KEY` |
| Rate limit       | Not vendor-published; codebase 1 req/s |
| Pagination       | None |
| Historical depth | ~5 years |
| Publication lag  | Regulation 543/2013 Art. 6(2)(b): "no later than two hours before the gate closure of the day-ahead market in the bidding zone and be updated when significant changes occur" |
| Response format  | XML (GL_MarketDocument) |
| Document type    | `A65` |
| Process type     | `A01` (Day ahead) |
| Domain param name | `outBiddingZone_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | yes | API key | `<your-entsoe-api-key>` |
| `documentType` | str | yes | `A65` | `A65` |
| `processType` | str | yes | `A01` | `A01` |
| `outBiddingZone_Domain` | str (EIC) | yes | Bidding zone EIC | `10Y1001A1001A82H` |
| `periodStart` | str | yes | `yyyyMMddHHmm` UTC | `202605060000` |
| `periodEnd` | str | yes | `yyyyMMddHHmm` UTC | `202605070000` |

### Working curl example

```bash
curl -X GET --ssl-no-revoke \
  "https://web-api.tp.entsoe.eu/api?securityToken=<your-entsoe-api-key>&documentType=A65&processType=A01&outBiddingZone_Domain=10Y1001A1001A82H&periodStart=202605060000&periodEnd=202605070000" \
  -H "Accept: application/xml"
```

GB returns code 999 (`DAY_AHEAD_TOTAL_LOAD_FORECAST_R3 [6.1.B]`).

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/load_forecast/<year>/<month>/<day>/raw_<YYYYMMDDTHHMMSSZ>_<hash>.xml`, with a `.meta.json` sidecar (`bronze/writer.py:57`)
**Format**: Raw XML.
**Granularity**: One file per (zone, UTC day): the connector splits a window into calendar days (`connectors/entsoe/client.py:162`, `day_subwindows`). Every data response in bronze (checked 2026-09-29) returns exactly the requested UTC day as its period.

### Bronze sample

(First ~500 bytes of DE-LU 2026-05-06 response.)

```json
{
  "envelope": "GL_MarketDocument xmlns='urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0'",
  "type": "A65",
  "process.processType": "A01",
  "TimeSeries": [
    {
      "businessType": "A04",
      "outBiddingZone_Domain.mRID": "10Y1001A1001A82H",
      "quantity_Measure_Unit.name": "MAW",
      "Period": {
        "timeInterval": {"start": "2026-05-06T00:00Z", "end": "2026-05-07T00:00Z"},
        "resolution": "PT15M",
        "Point": [{"position": 1, "quantity": 44175.567575}]
      }
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/load_forecast/year=YYYY/month=MM/load_forecast_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.load_forecast.LoadForecastTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeLoadForecast`
**Dedup key**: `(timestamp_utc, area_code)`, `keep="last"` over bronze files read in name (fetch-time) order (`silver/entsoe/load_forecast.py:38,68`), so a later fetch of the same day replaces an earlier one. Rows outside the partition's request window are dropped (`EVENT_WINDOW_FILTER = True`, `load_forecast.py:27`).
**Point-in-time field**: `published_at`, the document `createdDateTime`: a fetch-time stamp, not the forecast's issue time (see Known issues)

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime` (tz-aware UTC) | No | `Period.timeInterval.start + (position-1)*resolution` | UTC required; all data responses in bronze are `curveType` A03 (checked 2026-09-29, 90 to 96 declared points per day), and the parser forward-fills an A03 curve's omitted positions (`connectors/entsoe/parsers.py:533-596`) |
| `area_code` | `str` | No | `outBiddingZone_Domain.mRID` | EIC |
| `load_forecast_mw` | `float` | No | `Point/quantity` | MW |
| `resolution` | `str` | No (default `""`) | `Period/resolution` | `PT15M`/`PT60M` |
| `forecast_horizon` | `str` | No (default `"day_ahead"`) | derived | Constant `"day_ahead"` |
| `published_at` | `datetime[UTC]` | Yes | `<createdDateTime>` | The response's creation time: across the 104 data responses in bronze it fell within 2 s of the sidecar `fetched_at` (checked 2026-09-29), so it is a fetch-time stamp, not the TSO's issue time; typed-null when the source omits it (`silver/entsoe/_published_at.py`). |
| `data_provider` | `str` | No (default `"entsoe"`) | derived | Constant |
| `ingested_at` | `datetime` (tz-aware UTC) | Yes | derived | |

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2026, 5, 6, 0, 0, tzinfo=UTC),
        "area_code": "10Y1001A1001A82H",
        "load_forecast_mw": 44175.567575,
        "resolution": "PT15M",
        "forecast_horizon": "day_ahead",
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 5, 8, 18, 4, 28, tzinfo=UTC),
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB and IE-SEM empty**: `10YGB----------A` and `10Y1001A1001A59C` (both in
  `DEFAULT_ZONES`, `connectors/entsoe/endpoints.py:395`) returned code 999 in all
  26 bronze files each, dated 2026-08-01 to 2026-09-20 (checked 2026-09-29).
- **Forecast revisions**: the regulation has the forecast "updated when
  significant changes occur" (Art. 6(2)(b)), but the document carries no issue
  time or revision history (`revisionNumber` 1 in every response in bronze).
  Silver keeps the latest *fetch* per `(timestamp_utc, area_code)`, not the
  latest revision as issued: for 2026-09-08, DE-LU was fetched on 9 Sep and
  15 Sep, 8 of 96 intervals differed by up to 11 MW, and silver holds the
  15 Sep values. Every fetch in bronze came after its delivery day, so the
  table cannot be used as a point-in-time day-ahead forecast.
- **15-min resolution** typical for continental zones; older windows or
  specific zones may publish PT60M.

---

## Implementation delta

- Code-tuple: `(A65, A01, None, outBiddingZone_Domain)`.
  Guide PDF unfetchable (`HTTP 400` from
  `transparency.entsoe.eu/.../Guide.pdf`); tuple is `unverified - PDF
  fetch failed` against canonical docs. Live DE-LU response returns
  expected `GL_MarketDocument` with `process.processType=A01`, confirming
  the API accepts the connector's request shape.
- No discrepancies observed.

---

## Modelling notes

- Pair with `actual_load` (A65/A16) on `(timestamp_utc, area_code)` to
  derive the forecast error series. Common target for forecast-error-aware
  pricing or peak-detection models.
- Drop GB rows for modelling.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/load_forecast.py`
- `src/gridflow/schemas/entsoe.py`
- Gold view/builder
- [Domain: forecast error](../../../20-domain/concepts/forecast-error.md)
