---
source: entsoe
dataset_key: forecast_margin
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Year-ahead forecast margin
  summary: >-
    ENTSO-E's year-ahead forecast margin per bidding zone: one MW figure for the year, from
    document type A70 with process type A33.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A70, process type A33
    cadence: "One `P1Y` point per year, as sent in these responses"
    grain: One row per year and bidding zone, per silver file
  landscape: power
  what_it_is: >-
    EU Regulation 543/2013, Article 2(30), defines it as, in part, "the difference between the yearly
    forecast of available generation capacity and the yearly forecast of maximum total load".
    The 2026 figure is stamped 23:00 UTC on 31 December 2025. The sign travels in `businessType`:
    A91 positive, A92 negative. Silver drops it.
  how_used:
    - Reading the 2026 margin in MW for FR, NL and BE, sent positive (A91).
    - A slow-moving input to year-ahead price and interconnector spread models.
  chart:
    type: bar
    silver: entsoe/forecast_margin
    value: forecast_margin_mw
    filter:
      - {column: area_code, op: ne, value: "10Y1001A1001A82H"}
      - {column: timestamp_utc, op: eq, value: "2025-12-31T23:00:00Z"}
    dedup: {on: [timestamp_utc, area_code], order_by: published_at}
    group: area_code
    group_map:
      "10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC": fr
      "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL": nl
      "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2": be
    aggregation: sum
    sort: value_desc
    unit: MW
  chart_view:
    title: Forecast margin for 2026, NL, FR and BE
    caption: >-
      Silver `entsoe/forecast_margin`, MW, the 2026 figure (stamped 23:00 UTC on 31 December 2025).
      These silver files each repeat it; one copy is kept. DE-LU is left out: it is sent negative
      (A92), and silver drops the sign.
    alt: >-
      Bar chart of the 2026 year-ahead forecast margin from entsoe/forecast_margin, in MW, one bar
      per bidding zone, largest first: NL 41,891; FR 1,500; BE 180. The BE bar is a sliver beside
      NL's. DE-LU is not drawn; its document gives a negative margin of 4,126 MW.
    key:
      - {series: nl, label: Netherlands (NL), paint: olive}
      - {series: fr, label: France (FR), paint: horizon}
      - {series: be, label: Belgium (BE), paint: clay}
  raw_feed:
    note: >-
      One GET per bidding zone and UTC day, for six zones. In these responses a one-day request
      returns the whole year's document; GB and IE-SEM return code 999, no data.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A70&periodStart=202609140000&periodEnd=202609150000&outBiddingZone_Domain=10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL&processType=A33&securityToken=$ENTSOE_API_KEY"
    commands:
      - {run: gridflow ingest entsoe forecast_margin --start 2026-09-14 --end 2026-09-15, comment: "bronze; one day, end excluded"}
      - {run: gridflow transform entsoe forecast_margin --start 2026-09-14 --end 2026-09-14, comment: "bronze to silver; end included"}
  record:
    select:
      filter:
        - {column: published_at, op: ge, value: "2026-09-15T20:18:01Z"}
      order_by: [published_at, area_code]
      columns: [area_code, forecast_margin_mw, published_at, timestamp_utc, resolution]
    key: [timestamp_utc, area_code, published_at]
    caption: "The last two fetches, four zones each; DE-LU's 4,126 is sent as negative (A92)."
    fields:
      area_code: "Bidding zone EIC, from `outBiddingZone_Domain.mRID`"
      forecast_margin_mw: "MW (`MAW`) from `quantity`, unsigned: the A91 or A92 sign is dropped"
      published_at: "Response `createdDateTime`, UTC: a fetch-time stamp, within seconds of gridflow's request"
      timestamp_utc: "Period start, UTC: 2025-12-31 23:00 is midnight CET, the start of 2026"
      resolution: "Point length as sent; `P1Y` in these rows"
  notebook:
    lead: >-
      `query()` reads `silver_entsoe_forecast_margin` by whole UTC days of `timestamp_utc`, ends
      included, without lineage columns. The 2026 figure is stamped 31 December 2025. Drop per-file
      duplicates, and DE-LU: silver loses its negative (A92) sign.
    cells:
      - |
        df = data.entsoe.query("forecast_margin", "2025-12-31", "2025-12-31")
        key = ["timestamp_utc", "area_code"]
        df = df.sort_values("published_at").drop_duplicates(subset=key, keep="last")
      - "zones = {'10Y1001A1001A82H': 'DE-LU', '10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC': 'FR',\n         '10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL': 'NL', '10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2': 'BE'}\ndf = df.assign(zone=df['area_code'].map(zones), published_at=df['published_at'].dt.tz_convert('UTC'))\n# DE-LU is sent negative (A92); silver keeps only 4126, unsigned, so drop it.\ndf = df[df['zone'] != 'DE-LU']\ndf[['zone', 'forecast_margin_mw', 'resolution', 'published_at']].reset_index(drop=True)"
      - |
        shown = df.sort_values("forecast_margin_mw", ascending=False)
        ax = shown.plot.bar(x="zone", y="forecast_margin_mw", ylabel="MW", legend=False, rot=0, figsize=(6, 3))
        ax.bar_label(ax.containers[0], fmt="{:,.0f}");
    needs: one day of 2026, for example 14 September
    plot_alt: >-
      Bar chart of the 2026 forecast_margin_mw for NL, FR and BE, largest first, each bar labelled
      with its value: NL 41,891, FR 1,500, BE 180. Only NL's bar is tall; BE's is too short to see.
      DE-LU is left out because silver drops its negative sign.
  related:
    - {dataset: entsoe/installed_capacity, note: "Installed MW per production type for the same zones and year"}
    - {dataset: entsoe/load_forecast_yearly, note: "The year-ahead load forecast for the same zones (A65, A33)"}
    - {dataset: entsoe/actual_load, note: "Realised load in the zones and year this margin covers"}
---

# ENTSO-E — Year-ahead Forecast Margin (A70/A33)

## Overview

Year-ahead forecast margin in MW per bidding zone. Commission Regulation (EU)
No 543/2013, Article 2(30): "'year-ahead forecast margin' means the difference
between the yearly forecast of available generation capacity and the yearly
forecast of maximum total load taking into account the forecast of total
generation capacity, the forecast of availability of generation and the
forecast of reserves contracted for system services;". Article 8(1): TSOs
"shall calculate and provide for each bidding zone the year-ahead forecast
margin evaluated at the local market time unit", published "one week before
the yearly capacity allocation but no later than the 15th calendar day of the
month before the year to which the data relates". (Source: the regulation as
adopted, legislation.gov.uk `eur/2013/543`, fetched 2026-09-29; EUR-Lex
returned an empty page.) The responses gridflow holds carry one `P1Y` point
per zone, not a value per market time unit.
Article 8.1 (`YEAR_AHEAD_FORECAST_MARGIN_R3`). Document type
`A70` + process type `A33` ("Year ahead"). Used in capacity-adequacy
analyses and as a market-tightness signal.

Related domain notes:
  [Capacity adequacy](../../../20-domain/concepts/capacity-adequacy.md)

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
| Publication lag  | Yearly |
| Response format  | XML (GL_MarketDocument) |
| Document type    | `A70` |
| Process type     | `A33` (Year ahead) |
| Domain param name | `outBiddingZone_Domain` |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | yes | API key | `<your-entsoe-api-key>` |
| `documentType` | str | yes | `A70` | `A70` |
| `processType` | str | yes | `A33` | `A33` |
| `outBiddingZone_Domain` | str (EIC) | yes | Bidding zone EIC | `10Y1001A1001A82H` |
| `periodStart` | str | yes | `yyyyMMddHHmm` UTC | `202605060000` |
| `periodEnd` | str | yes | `yyyyMMddHHmm` UTC | `202605070000` |

### Working curl example

```bash
curl -X GET --ssl-no-revoke \
  "https://web-api.tp.entsoe.eu/api?securityToken=<your-entsoe-api-key>&documentType=A70&processType=A33&outBiddingZone_Domain=10Y1001A1001A82H&periodStart=202605060000&periodEnd=202605070000" \
  -H "Accept: application/xml"
```

GB and IE-SEM (`10Y1001A1001A59C`) return code 999 (`YEAR_AHEAD_FORECAST_MARGIN_R3 [8.1]`)
in the responses gridflow holds (bronze acknowledgements, 16 Aug and 15 Sep 2026 fetches).

**Sign.** The margin's sign travels in `TimeSeries/businessType`, not in
`quantity`. ENTSO-E Code Lists v29r0, section 3.4 BusinessTypeList (p. 16):
A91 "positive forecast margin", A92 "Negative forecast margin". In the
responses gridflow holds, DE-LU (`10Y1001A1001A82H`) is sent as A92 and FR,
NL and BE as A91.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/forecast_margin/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML.
**Granularity**: One file per zone per requested UTC day (`connectors/entsoe/client.py:162`,
`day_subwindows`). In the responses gridflow holds, each one-day request returns the whole
year's document (period 2025-12-31T23:00Z to 2026-12-31T23:00Z), so every day's files repeat it.

### Bronze sample

```json
{
  "envelope": "GL_MarketDocument",
  "type": "A70",
  "process.processType": "A33",
  "TimeSeries": [
    {
      "businessType": "A92",
      "outBiddingZone_Domain.mRID": "10Y1001A1001A82H",
      "quantity_Measure_Unit.name": "MAW",
      "Period": {"resolution": "P1Y", "Point": [{"position": 1, "quantity": 4126}]}
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/forecast_margin/year=YYYY/month=MM/forecast_margin_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.forecast_margin.ForecastMarginTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeForecastMargin`
**Dedup key**: `(timestamp_utc, area_code)`, within one transform day only
(`silver/entsoe/forecast_margin.py:62`); copies of the year document repeat across daily files
**Point-in-time field**: none

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime` (tz-aware UTC) | No | derived | Period start (`parsers.py:527-528`, calendar year step for `P1Y`) |
| `area_code` | `str` | No | `outBiddingZone_Domain.mRID` | EIC |
| `forecast_margin_mw` | `float` | No | `Point/quantity` | MW (`MAW`); unsigned: `businessType` (A91 positive, A92 negative) is not kept (`forecast_margin.py:75-83`) |
| `resolution` | `str` | No (default `""`) | `Period/resolution` | typically `P1Y` |
| `published_at` | `datetime` (tz-aware UTC) | Yes | `createdDateTime` | Response creation time: a fetch-time stamp, not an issue time |
| `data_provider` | `str` | No (default `"entsoe"`) | derived | Constant |
| `ingested_at` | `datetime` (tz-aware UTC) | Yes | derived | |

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2025, 12, 31, 23, 0, tzinfo=UTC),
        "area_code": "10YNL----------L",
        "forecast_margin_mw": 41891.044,
        "resolution": "P1Y",
        "published_at": datetime(2026, 9, 15, 20, 18, 12, tzinfo=UTC),
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 9, 15, 20, 18, 17, 839353, tzinfo=UTC),
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **GB empty post-Brexit**. IE-SEM also returns code 999 in the responses gridflow holds.
- **Annual resolution**: `P1Y` points use calendar-year arithmetic, not a
  365-day step (`connectors/entsoe/parsers.py:47`, `:76-93`, `:527-528`).
- **Negative margin is not visible in silver.** A negative margin is sent as
  `businessType` A92 with a positive `quantity`; the transformer does not keep
  `business_type` (`silver/entsoe/forecast_margin.py:75-83`), so DE-LU's A92
  4,126 MW reads as +4,126 in silver. Restore the sign from bronze.
- **Repeated year document.** One-day requests each return the whole year's
  document, and dedup acts within one transform day only; drop duplicates on
  `(timestamp_utc, area_code)` across files, keeping the latest `published_at`.
- **Schema validation**: the silver transformer constructs a Pydantic
  `EntsoeForecastMargin` from the first row to surface schema drift. Watch
  for `ValidationError` in the silver step on unexpected schema changes.

---

## Implementation delta

- Code-tuple: `(A70, A33, None, outBiddingZone_Domain)`.
  Guide PDF unfetchable; tuple `unverified - PDF fetch failed` against
  canonical docs. Live DE-LU returns `GL_MarketDocument` with
  `process.processType=A33` and `type=A70` — request shape accepted.

---

## Modelling notes

- Capacity-adequacy feature for longer-horizon GB-EU spread modelling.
  Lower margin in adjacent zones can signal price upside via interconnector
  flows.
- Drop GB rows.

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/forecast_margin.py`
- `src/gridflow/schemas/entsoe.py`
- Gold view/builder
- [Domain: capacity adequacy](../../../20-domain/concepts/capacity-adequacy.md)
