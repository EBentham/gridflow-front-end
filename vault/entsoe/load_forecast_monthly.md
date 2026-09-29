---
source: entsoe
dataset_key: load_forecast_monthly
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSO-E — Month-ahead Load Forecast (A65/A32)

## Overview

Month-ahead total load forecast in MW per bidding zone: two series per zone,
business types `A60` and `A61`, each with one `P7D` point per week (every data
response in bronze, 1 Aug to 14 Sep 2026, checked 2026-09-29). Document type
`A65` + process type `A32` ("Month ahead"). Legal basis: Regulation (EU) No
543/2013, Article 6(1)(d), "a month-ahead forecast of the total load for
every week of the following month, which shall include, for a given week, a
maximum and a minimum load value" (retained copy,
https://www.legislation.gov.uk/eur/2013/543). Same transformer as day-ahead
(`LoadForecastMonthlyTransformer` subclasses `LoadForecastTransformer`,
`silver/entsoe/load_forecast_monthly.py:11`) and the same schema, with
`forecast_horizon` set to `month_ahead`.

Related domain notes:
  [Load forecast](../../../20-domain/concepts/load-forecast.md)

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
| Publication lag  | Regulation 543/2013 Art. 6(2)(d): "no later than one week before the delivery month and be updated when significant changes occur" |
| Response format  | XML (GL_MarketDocument) |
| Document type    | `A65` |
| Process type     | `A32` (Month ahead) |
| Domain param name | `outBiddingZone_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | yes | API key | `<your-entsoe-api-key>` |
| `documentType` | str | yes | `A65` | `A65` |
| `processType` | str | yes | `A32` | `A32` |
| `outBiddingZone_Domain` | str (EIC) | yes | Bidding zone EIC | `10Y1001A1001A82H` |
| `periodStart` | str | yes | `yyyyMMddHHmm` UTC | `202605060000` |
| `periodEnd` | str | yes | `yyyyMMddHHmm` UTC | `202605070000` |

### Working curl example

```bash
curl -X GET --ssl-no-revoke \
  "https://web-api.tp.entsoe.eu/api?securityToken=<your-entsoe-api-key>&documentType=A65&processType=A32&outBiddingZone_Domain=10Y1001A1001A82H&periodStart=202605060000&periodEnd=202605070000" \
  -H "Accept: application/xml"
```

GB returns code 999 (`TOTAL_LOAD_FORECAST [6.1.C&D&E]`).

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/load_forecast_monthly/<year>/<month>/<day>/raw_<YYYYMMDDTHHMMSSZ>_<hash>.xml`, with a `.meta.json` sidecar (`bronze/writer.py:57`)
**Format**: Raw XML.
**Granularity**: One file per (zone, UTC day): the connector splits a window into calendar days (`connectors/entsoe/client.py:162`, `day_subwindows`). Each response in bronze returns one 7-day period, the week containing the requested day's 00:00 UTC start (weeks run from Sunday 22:00 UTC, Monday 00:00 CEST, in these responses), so consecutive days' files repeat the same week.

### Bronze sample

(DE-LU, request 2026-09-10 00:00 to 2026-09-11 00:00 UTC, bronze
`2026/09/10/raw_20260915T201452Z_e08e2048.xml`, abridged.)

```json
{
  "envelope": "GL_MarketDocument",
  "type": "A65",
  "process.processType": "A32",
  "TimeSeries": [
    {
      "businessType": "A60",
      "outBiddingZone_Domain.mRID": "10Y1001A1001A82H",
      "curveType": "A03",
      "Period": {"timeInterval": {"start": "2026-09-06T22:00Z", "end": "2026-09-13T22:00Z"},
                 "resolution": "P7D", "Point": [{"position": 1, "quantity": 37051.137529}]}
    },
    {
      "businessType": "A61",
      "outBiddingZone_Domain.mRID": "10Y1001A1001A82H",
      "curveType": "A03",
      "Period": {"timeInterval": {"start": "2026-09-06T22:00Z", "end": "2026-09-13T22:00Z"},
                 "resolution": "P7D", "Point": [{"position": 1, "quantity": 65211.208123}]}
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/load_forecast_monthly/year=YYYY/month=MM/load_forecast_monthly_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.load_forecast_monthly.LoadForecastMonthlyTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeLoadForecast` (shared base — the schema reuses `EntsoeLoadForecast` with `forecast_horizon="month_ahead"`)
**Dedup key**: `(timestamp_utc, area_code)`, `keep="last"`, applied within one daily partition only (`silver/entsoe/load_forecast.py:68`, inherited). The key has no business type, so the `A60`/`A61` pair collapses to `A61` (16 of 16 distinct keys, bronze and silver compared 2026-09-29). The event-window filter is off (`load_forecast_monthly.py:16`), so each daily partition keeps the whole week: silver holds 48 rows for 16 distinct keys, a week repeated up to 6 times with equal values.
**Point-in-time field**: `published_at`, the document `createdDateTime`: a fetch-time stamp, not the forecast's issue time

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime` (tz-aware UTC) | No | `Period.timeInterval.start + (position-1)*resolution` | Week start; 22:00 UTC on a Sunday in every row in silver |
| `area_code` | `str` | No | `outBiddingZone_Domain.mRID` | EIC |
| `load_forecast_mw` | `float` | No | `Point/quantity` | MW |
| `resolution` | `str` | No (default `""`) | `Period/resolution` | `P7D` in every response in bronze |
| `forecast_horizon` | `str` | No (default `"month_ahead"`) | derived | Constant |
| `published_at` | `datetime[UTC]` | Yes | `<createdDateTime>` | The response's creation time, within 7 s of the sidecar `fetched_at` in every data response in bronze (checked 2026-09-29): a fetch-time stamp, not the TSO's issue time; typed-null when the source omits it. |
| `data_provider` | `str` | No (default `"entsoe"`) | derived | Constant |
| `ingested_at` | `datetime` (tz-aware UTC) | Yes | derived | |

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2026, 9, 6, 22, 0, tzinfo=UTC),
        "area_code": "10Y1001A1001A82H",
        "load_forecast_mw": 65211.208123,  # the A61 point; A60 (37051.137529) dropped
        "resolution": "P7D",
        "forecast_horizon": "month_ahead",
        "published_at": datetime(2026, 9, 15, 20, 14, 52, tzinfo=UTC),
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 9, 15, 20, 15, 56, 846169, tzinfo=UTC),
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB and IE-SEM empty**: both returned code 999 in all 12 bronze files each,
  dated 2026-08-01 to 2026-09-14 (checked 2026-09-29).
- **Two series, one kept**: every data response carries `A60` and `A61`, one
  point each per week; the regulation requires a maximum and a minimum per
  week (Art. 6(1)(d)). `A60` is below `A61` in every response in bronze; no
  source in the repo or vault names which code is which. Silver keeps `A61`
  only (see Dedup key).
- **Repeated weeks**: `data.entsoe.query("load_forecast_monthly", ...)` returns
  a week once per daily partition that holds it; deduplicate on
  `(timestamp_utc, area_code)` before use.
- **`P7D`, not `P1M`**: every response in bronze is weekly. The parser's
  calendar arithmetic for `P1M` (`_advance_calendar`,
  `connectors/entsoe/parsers.py:76-93,523-528`) is not exercised.

---

## Implementation delta

- Code-tuple: `(A65, A32, None, outBiddingZone_Domain)`.
  Guide PDF unfetchable; tuple `unverified - PDF fetch failed` against
  canonical docs. Live DE-LU returns `GL_MarketDocument` with
  `process.processType=A32` — request shape accepted.
- **Resolution**: the responses are `P7D`, not `P1M`. For `P1M` the parser
  now uses calendar arithmetic, not a `timedelta(days=30)`
  (`connectors/entsoe/parsers.py:76-93,523-528`); the 30-day value in
  `_RESOLUTION_MAP` is only a fallback (`parsers.py:31-34`).
- **Silver defects (validated 2026-09-29)**: the `A60`/`A61` collapse and the
  repeated weeks across daily partitions (see Silver layer). Logged as gridflow
  defects.

---

## Modelling notes

- Long-horizon trend feature in seasonal models. Coarse — typical use is
  to set monthly demand expectations as a baseline against which weekly
  / daily features modulate.
- Drop GB rows.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/load_forecast_monthly.py`
- `src/gridflow/schemas/entsoe.py`
- Gold view/builder
- [Domain: load forecast](../../../20-domain/concepts/load-forecast.md)
