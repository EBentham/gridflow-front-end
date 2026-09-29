---
source: entsoe
dataset_key: actual_load
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Actual total load by zone
  summary: >-
    Realised total load per European bidding zone from ENTSO-E's Transparency Platform: one MW
    value per zone and interval.
  facts:
    vendor: ENTSO-E Transparency Platform, document A65, process A16 (Article 6.1.A)
    cadence: 15 minutes (`PT15M`) in every response charted
    grain: One row per bidding zone and interval
  landscape: power
  what_it_is: >-
    ENTSO-E's actual total load (Article 6.1.A) per bidding zone: one MW value per interval.
    gridflow asks for six zones, one call per zone and UTC day. GB and IE-SEM got ENTSO-E's "no
    matching data" answer (code 999) on the days charted. ENTSO-E defines what total load
    includes; that definition is not quoted here.
  how_used:
    - Target for a short-term load forecast per zone, with weather and calendar features.
    - Forecast error against `load_forecast`, ENTSO-E's day-ahead load forecast for the same zones.
    - Residual load per zone, net of wind and solar from `actual_generation`.
  chart:
    type: line
    silver: entsoe/actual_load
    time: timestamp_utc
    value: load_mw
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
    title: Total load by zone, 14 to 20 September 2026
    caption: >-
      Silver `entsoe/actual_load`, MW, every 15-minute value over the UTC days 14 to 20 September
      2026, one line per bidding zone: DE-LU, FR, NL and BE.
    alt: >-
      Line chart of total load from entsoe/actual_load, in MW, every 15 minutes from 14 to 20
      September 2026 (UTC), one line per zone. DE-LU runs highest on almost every interval, with weekday morning peaks of 63
      to 65 GW, weekend peaks of 52 and 51 GW and a Sunday low of 35 GW. FR runs between 31 and 51
      GW. NL and BE stay between 4 and 12 GW; NL's lows fall near midday, 4.1 GW at 11:00 UTC on
      the 15th.
    x_label: UTC date; each starts at 00:00
    key:
      - {series: de_lu, label: Germany and Luxembourg (DE-LU), paint: petrol, note: "One interval as sent, 23:15 UTC on the 16th, drops to 39.4 GW; cause undocumented."}
      - {series: fr, label: France (FR), paint: horizon}
      - {series: nl, label: Netherlands (NL), paint: clay, note: "Lows fall between late morning and early afternoon UTC; cause undocumented."}
      - {series: be, label: Belgium (BE), paint: olive}
  raw_feed:
    note: >-
      From the ENTSO-E Transparency Platform API: one XML document per zone and UTC day. `gridflow
      ingest` writes each to bronze; `gridflow transform` parses that day's points into silver.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A65&periodStart=202609140000&periodEnd=202609150000&outBiddingZone_Domain=10Y1001A1001A82H&processType=A16&securityToken=<your-entsoe-api-key>"
    commands:
      - {run: gridflow ingest entsoe actual_load --start 2026-09-14 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform entsoe actual_load --start 2026-09-14 --end 2026-09-20, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: ge, value: "2026-09-15T11:00:00Z"}
        - {column: timestamp_utc, op: le, value: "2026-09-15T11:15:00Z"}
      order_by: [timestamp_utc, area_code]
      columns: [timestamp_utc, area_code, load_mw, resolution, published_at]
    key: [timestamp_utc, area_code]
    caption: "All four zones with rows, at 11:00 and 11:15 UTC on 15 September 2026."
    fields:
      timestamp_utc: "Interval start, UTC: period start plus (position minus 1) times resolution"
      area_code: "Bidding zone EIC as sent; `10Y1001A1001A82H` is DE-LU"
      load_mw: "Total load in MW: the point's `quantity`, unit `MAW`"
      resolution: "Interval length as ENTSO-E sends it; `PT15M` is 15 minutes"
      published_at: "Fetch-time stamp: the response's `createdDateTime`, within seconds of the request"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_entsoe_actual_load`: whole UTC
      days on `timestamp_utc`, both ends included, lineage columns dropped. Times print in the
      kernel's local time.
    cells:
      - df = data.entsoe.query("actual_load", "2026-09-14", "2026-09-20")
      - df[["timestamp_utc", "area_code", "load_mw"]].head()
      - |
        wide = df.pivot_table(index="timestamp_utc", columns="area_code", values="load_mw")
        ax = wide.plot(ylabel="MW", figsize=(8, 3.5))
        ax.legend(ncols=2, loc="lower center", bbox_to_anchor=(0.5, 1.0));
    needs: 14 to 20 September 2026
    plot_alt: >-
      Line plot of load_mw for each area_code from 14 to 20 September 2026, on a UTC+1 clock. DE-LU
      runs from 35 to 65 GW and FR from 31 to 51 GW, both lower at the weekend. BE and NL stay
      between 4 and 12 GW; NL's lows fall near midday, about 4,100 MW on the 15th.
  related:
    - {dataset: entsoe/load_forecast, note: "The day-ahead forecast of this load, for the same zones"}
    - {dataset: entsoe/actual_generation, note: "Generation by type in the same zones, for residual load"}
    - {dataset: entsoe/day_ahead_prices, note: "Day-ahead prices, requested for the same bidding zones"}
    - {dataset: elexon/indo, note: "GB demand outturn; gridflow's GB calls to ENTSO-E returned code 999"}
---

# ENTSO-E — Actual Total Load (A65/A16)

## Overview

Realised (metered) total load in MW per bidding zone, published per ENTSO-E
Transparency Platform Article 6.1.A (`ACTUAL_TOTAL_LOAD_R3`). Document type
`A65` ("System total load") with process type `A16` ("Realised") returns
`<TimeSeries>` keyed by `outBiddingZone_Domain` with `<quantity>` values.
Resolution is typically PT15M for continental zones. This is the canonical
demand series used for forecast-error analysis, peak detection, and
weather-vs-demand modelling.

Related domain notes:
  [System load](../../../20-domain/concepts/system-load.md)
  [EIC codes](../../../20-domain/concepts/eic-codes.md)

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
| Historical depth | ~5 years on most zones |
| Publication lag  | ~1 hour after settlement period close |
| Response format  | XML (GL_MarketDocument) |
| Document type    | `A65` |
| Process type     | `A16` (Realised) |
| Domain param name | `outBiddingZone_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | yes | API key | `<your-entsoe-api-key>` |
| `documentType` | str | yes | `A65` | `A65` |
| `processType` | str | yes | `A16` | `A16` |
| `outBiddingZone_Domain` | str (EIC) | yes | Bidding zone EIC | `10Y1001A1001A82H` |
| `periodStart` | str (`yyyyMMddHHmm` UTC) | yes | Window start | `202605060000` |
| `periodEnd` | str (`yyyyMMddHHmm` UTC) | yes | Window end | `202605070000` |

### Working curl example

```bash
curl -X GET --ssl-no-revoke \
  "https://web-api.tp.entsoe.eu/api?securityToken=<your-entsoe-api-key>&documentType=A65&processType=A16&outBiddingZone_Domain=10Y1001A1001A82H&periodStart=202605060000&periodEnd=202605070000" \
  -H "Accept: application/xml"
```

GB (`10YGB----------A`) returns Acknowledgement 999
(`ACTUAL_TOTAL_LOAD_R3 [6.1.A]`). Use Elexon `indo`/`itsdo` for GB realised
demand.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/actual_load/<year>/<month>/<day>/raw_<YYYYMMDDTHHMMSSZ>_<hash>.xml`, with a `.meta.json` sidecar (`bronze/writer.py:57`)
**Format**: Raw XML.
**Granularity**: One file per (zone, UTC day): the connector splits a window into calendar days (`connectors/entsoe/client.py:162`, `day_subwindows`).

### Bronze sample

(First ~500 bytes of a DE-LU 2026-05-06 response.)

```json
{
  "envelope": "GL_MarketDocument xmlns='urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0'",
  "type": "A65",
  "process.processType": "A16",
  "TimeSeries": [
    {
      "businessType": "A04",
      "outBiddingZone_Domain.mRID": "10Y1001A1001A82H",
      "quantity_Measure_Unit.name": "MAW",
      "Period": {
        "timeInterval": {"start": "2026-05-06T00:00Z", "end": "2026-05-07T00:00Z"},
        "resolution": "PT15M",
        "Point": [{"position": 1, "quantity": 43236.25422}]
      }
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/actual_load/year=YYYY/month=MM/actual_load_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.actual_load.ActualLoadTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeActualLoad`
**Dedup key**: `(timestamp_utc, area_code)`
**Point-in-time field**: `published_at`, the document `createdDateTime` (`silver/entsoe/actual_load.py:76`). In the 104 bronze documents checked on 2026-09-29 it fell within 4 s of the request, so it is the response time, not the TSO's publish time.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime` (tz-aware UTC) | No | `Period.timeInterval.start + (position-1)*resolution` | tz-aware UTC required; all 104 data responses in bronze (checked 2026-09-29) are `curveType` A03, and the parser forward-fills an A03 curve's omitted positions (`connectors/entsoe/parsers.py:533-596`) |
| `area_code` | `str` | No | `outBiddingZone_Domain.mRID` (parser remaps to `in_domain`) | EIC, no normalisation |
| `load_mw` | `float` | No | `Point/quantity` | Megawatts (unit `MAW` = MW) |
| `resolution` | `str` | No (default `""`) | `Period/resolution` | `PT15M`, `PT30M`, `PT60M` |
| `published_at` | `datetime` (tz-aware UTC) | Yes | document `createdDateTime` | ADR-025 P1.1 vintage (`silver/entsoe/actual_load.py:76`); tracks the request time |
| `data_provider` | `str` | No (default `"entsoe"`) | derived | Constant |
| `ingested_at` | `datetime` (tz-aware UTC) | Yes | derived | Set by transformer |

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2026, 5, 6, 0, 0, tzinfo=UTC),
        "area_code": "10Y1001A1001A82H",
        "load_mw": 43236.25422,
        "resolution": "PT15M",
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 5, 8, 18, 4, 26, tzinfo=UTC),
    },
    {
        "timestamp_utc": datetime(2026, 5, 6, 0, 15, tzinfo=UTC),
        "area_code": "10Y1001A1001A82H",
        "load_mw": 43011.13,
        "resolution": "PT15M",
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 5, 8, 18, 4, 26, tzinfo=UTC),
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB empty post-Brexit** — code 999 returned for `10YGB----------A`.
  Use Elexon `indo`/`itsdo` for GB realised demand instead.
- **IE-SEM empty too**: `10Y1001A1001A59C`, one of the connector's `DEFAULT_ZONES`
  (`connectors/entsoe/endpoints.py:395`), returned code 999 in all 26 bronze
  files on hand, dated 2026-08-01 to 2026-09-20 (checked 2026-09-29).
- **Quantity unit `MAW`** — the ENTSO-E XML reports `quantity_Measure_Unit.name = "MAW"`,
  which is megawatts (the standard ENTSO-E unit code for MW). The silver
  field is named `load_mw` to match the convention.
- **15-minute resolution by default** for continental zones. Some smaller
  zones still publish PT60M.
- **outBiddingZone_Domain** is the parameter — NOT `BiddingZone_Domain` or
  `in_Domain`. Mismatch silently returns wrong scope or 400.
- **Revisions** can occur within ~24 hours as TSO meter data is
  back-validated. Re-running `ingest` for a recent date is the simplest
  way to absorb revisions; the dedup `(timestamp_utc, area_code)` keeps
  the most-recent value.

---

## Implementation delta

- **Tuple comparison**: code-tuple `(documentType=A65, processType=A16, businessType=None, domain=outBiddingZone_Domain)`.
  Static Content Guide PDF could not be fetched (`HTTP 400` — CDN
  protection); tuple is `unverified - PDF fetch failed` against the
  canonical guide. Live DE-LU response confirms the API accepts the shape
  and returns the documented `GL_MarketDocument` envelope with `type=A65`,
  `process.processType=A16`, and `outBiddingZone_Domain.mRID` matching the
  request — so the live API is consistent with the connector's tuple.
- No discrepancies observed between connector and live API behaviour.

---

## Modelling notes

- Target variable for short-term load forecasting models. Typical features:
  weather (temperature, irradiance, wind), calendar (hour-of-day,
  day-of-week, public holiday), lagged load (load_t-24h, load_t-168h).
- Pair with `load_forecast` (A65/A01) to build forecast-error series for
  error-distribution modelling.
- Drop GB rows when modelling — always empty.
- For UK demand modelling, prefer Elexon `indo` (instantaneous national
  demand, half-hourly) — same physical signal, fully populated.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/actual_load.py`
- `src/gridflow/schemas/entsoe.py`
- Gold view/builder
- [Domain: system load](../../../20-domain/concepts/system-load.md)
