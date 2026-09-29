---
source: entsoe
dataset_key: load_forecast_weekly
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
---

# ENTSO-E — Week-ahead Load Forecast (A65/A31)

## Overview

Week-ahead total load forecast in MW per bidding zone: two series per zone,
business types `A60` and `A61`, each with one `P1D` point per day (every data
response in bronze, 1 Aug to 14 Sep 2026, checked 2026-09-29). Document type
`A65` + process type `A31` ("Week ahead"). Legal basis: Regulation (EU) No
543/2013, Article 6(1)(c), "a week-ahead forecast of the total load for every
day of the following week, which shall for each day include a maximum and a
minimum load value" (retained copy, https://www.legislation.gov.uk/eur/2013/543). Used as a longer-horizon reference for forecast
adaptation studies and weekly capacity planning.

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
| Publication lag  | Regulation 543/2013 Art. 6(2)(c): "each Friday no later than two hours before the gate closure of the day-ahead market in the bidding zone and be updated when significant changes occur" |
| Response format  | XML (GL_MarketDocument) |
| Document type    | `A65` |
| Process type     | `A31` (Week ahead) |
| Domain param name | `outBiddingZone_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | yes | API key | `<your-entsoe-api-key>` |
| `documentType` | str | yes | `A65` | `A65` |
| `processType` | str | yes | `A31` | `A31` |
| `outBiddingZone_Domain` | str (EIC) | yes | Bidding zone EIC | `10Y1001A1001A82H` |
| `periodStart` | str | yes | `yyyyMMddHHmm` UTC | `202605060000` |
| `periodEnd` | str | yes | `yyyyMMddHHmm` UTC | `202605070000` |

### Working curl example

```bash
curl -X GET --ssl-no-revoke \
  "https://web-api.tp.entsoe.eu/api?securityToken=<your-entsoe-api-key>&documentType=A65&processType=A31&outBiddingZone_Domain=10Y1001A1001A82H&periodStart=202605060000&periodEnd=202605070000" \
  -H "Accept: application/xml"
```

GB returns code 999 (`TOTAL_LOAD_FORECAST [6.1.C&D&E]`).

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/load_forecast_weekly/<year>/<month>/<day>/raw_<YYYYMMDDTHHMMSSZ>_<hash>.xml`, with a `.meta.json` sidecar (`bronze/writer.py:57`)
**Format**: Raw XML.
**Granularity**: One file per (zone, UTC day): the connector splits a window into calendar days (`connectors/entsoe/client.py:162`, `day_subwindows`). For a request of UTC day D the responses in bronze return one period from 22:00 UTC on D-1 to 22:00 UTC on D (the CEST day), one point per series.

### Bronze sample

(DE-LU, request 2026-09-10 00:00 to 2026-09-11 00:00 UTC, bronze
`2026/09/10/raw_20260915T201403Z_ec0064b8.xml`, abridged.)

```json
{
  "envelope": "GL_MarketDocument",
  "type": "A65",
  "process.processType": "A31",
  "TimeSeries": [
    {
      "businessType": "A60",
      "outBiddingZone_Domain.mRID": "10Y1001A1001A82H",
      "curveType": "A03",
      "Period": {"timeInterval": {"start": "2026-09-09T22:00Z", "end": "2026-09-10T22:00Z"},
                 "resolution": "P1D", "Point": [{"position": 1, "quantity": 41844.280878}]}
    },
    {
      "businessType": "A61",
      "outBiddingZone_Domain.mRID": "10Y1001A1001A82H",
      "curveType": "A03",
      "Period": {"timeInterval": {"start": "2026-09-09T22:00Z", "end": "2026-09-10T22:00Z"},
                 "resolution": "P1D", "Point": [{"position": 1, "quantity": 63167.051073}]}
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/load_forecast_weekly/year=YYYY/month=MM/load_forecast_weekly_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.load_forecast_weekly.LoadForecastWeeklyTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeLoadForecastWeekly`
**Dedup key**: `(timestamp_utc, area_code)`, `keep="last"` (`silver/entsoe/load_forecast_weekly.py:68`). The key has no business type, so the `A60` and `A61` points of a day collide and only the later-parsed one survives: `A61` on all 48 silver rows (bronze and silver compared, 2026-09-29). Exempt from the event-window filter (`silver/entsoe/_event_window.py:159`).
**Point-in-time field**: `published_at`, the document `createdDateTime`: a fetch-time stamp, not the forecast's issue time

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime` (tz-aware UTC) | No | `Period.timeInterval.start + (position-1)*resolution` | 22:00 UTC (the CEST day start) in every row in silver |
| `area_code` | `str` | No | `outBiddingZone_Domain.mRID` | EIC |
| `load_forecast_mw` | `float` | No | `Point/quantity` | MW |
| `resolution` | `str` | No (default `""`) | `Period/resolution` | `P1D` in every response in bronze |
| `forecast_horizon` | `str` | No (default `"week_ahead"`) | derived | Constant |
| `published_at` | `datetime[UTC]` | Yes | `<createdDateTime>` | The response's creation time, within 1 s of the sidecar `fetched_at` in every data response in bronze (checked 2026-09-29): a fetch-time stamp, not the TSO's issue time; typed-null when the source omits it. |
| `data_provider` | `str` | No (default `"entsoe"`) | derived | Constant |
| `ingested_at` | `datetime` (tz-aware UTC) | Yes | derived | |

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2026, 9, 9, 22, 0, tzinfo=UTC),
        "area_code": "10Y1001A1001A82H",
        "load_forecast_mw": 63167.051073,  # the A61 point; A60 (41844.280878) dropped
        "resolution": "P1D",
        "forecast_horizon": "week_ahead",
        "published_at": datetime(2026, 9, 15, 20, 14, 4, tzinfo=UTC),
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 9, 15, 20, 14, 31, 609127, tzinfo=UTC),
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
- **Two series, one kept**: every data response carries business types `A60`
  and `A61`, one point each per day; the regulation requires a maximum and a
  minimum per day (Art. 6(1)(c)). `A60` is below `A61` in every response in
  bronze; no source in the repo or vault names which code is which. The
  parser keeps `business_type` (`connectors/entsoe/parsers.py:453`), but the
  transformer drops it and dedups on `(timestamp_utc, area_code)`, so silver
  holds `A61` only (48 of 48 rows).
- **`P1D` resolution**: the parser advances it as a fixed 1-day step
  (`_RESOLUTION_MAP`, `parsers.py:39`); each response in bronze has one
  position, so the step is never applied.

---

## Implementation delta

- Code-tuple: `(A65, A31, None, outBiddingZone_Domain)`.
  Guide PDF unfetchable; tuple `unverified - PDF fetch failed` against
  canonical docs. Live DE-LU returns valid `GL_MarketDocument` with
  `process.processType=A31` — request shape accepted.
- **Silver bug (validated 2026-09-29)**: dedup `(timestamp_utc, area_code)`
  collapses the `A60`/`A61` pair into one row and keeps `A61`, losing one of
  the day's two regulated values. Logged as a gridflow defect.

---

## Modelling notes

- Long-horizon trend baseline. Used in seasonal capacity-mix studies.
- Drop GB rows for modelling.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/load_forecast_weekly.py`
- `src/gridflow/schemas/entsoe.py`
- Gold view/builder
- [Domain: load forecast](../../../20-domain/concepts/load-forecast.md)
