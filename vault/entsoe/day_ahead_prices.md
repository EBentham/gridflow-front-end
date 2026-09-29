---
source: entsoe
dataset_key: day_ahead_prices
vendor: ENTSO-E Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Day-ahead prices by bidding zone
  summary: >-
    Day-ahead market clearing prices for each bidding zone gridflow requests, per quarter-hour or
    hour, in the currency ENTSO-E sends.
  facts:
    vendor: ENTSO-E Transparency Platform, document type A44
    cadence: Daily; evening replies here already held the next delivery day
    grain: One row per bidding zone and price period (15 or 60 minutes)
  landscape: market
  what_it_is: >-
    ENTSO-E's day-ahead clearing price per bidding zone and period, for the zones gridflow
    requests. From 14 to 20 September 2026, FR, NL, BE and DE-LU cleared in quarter-hours and
    IE-SEM hourly. GB returns Acknowledgement 999, no data. DE-LU sends two numbered price
    sequences; silver keeps one per quarter-hour, whichever the latest reply lists last.
  how_used:
    - The EU side of a GB interconnector spread, beside Elexon's market index price.
    - Zone-to-zone spreads, read against cross-border flows and transfer capacity.
    - A price target or feature for day-ahead forecasting per zone.
  chart:
    type: line
    silver: entsoe/day_ahead_prices
    time: timestamp_utc
    value: price_eur_mwh
    filter:
      - {column: area_code, op: ne, value: "10Y1001A1001A82H"}
      - {column: currency, op: eq, value: EUR}
    group: area_code
    group_map:
      "10Y1001A1001A59C": ie_sem
      "10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC": fr
      "10YNL\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2DL": nl
      "10YBE\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D\x2D2": be
    series_order: [ie_sem, fr, nl, be]
    aggregation: mean
    time_bucket: 1h
    window: {start: "2026-09-14", end: "2026-09-20"}
    unit: EUR/MWh
  chart_view:
    title: Day-ahead price, hourly, 14 to 20 September 2026
    caption: >-
      Silver `entsoe/day_ahead_prices`, EUR/MWh, UTC days 14 to 20 September 2026: the
      quarter-hour prices of FR, NL and BE averaged to each hour; IE-SEM as sent, hourly. DE-LU is
      left out: silver mixes its two price sequences.
    alt: >-
      Line chart of hourly day-ahead prices from entsoe/day_ahead_prices, in EUR/MWh, for UTC days
      14 to 20 September 2026. FR, NL and BE move together: evening peaks of 306 to 442 on the
      14th, lower prices from the 17th, and hours just below zero around midday on the 19th and
      20th (lowest -3.1, NL). IE-SEM ranges from 1, early on the 19th, to 359, and on the 20th stays
      between 147 and 359 while the other three fall to about zero at midday.
    x_label: UTC day; delivery days open 22:00 UTC
    key:
      - {series: ie_sem, label: "Ireland (SEM)", codes: IE-SEM, paint: petrol, note: "Hourly as sent; the other three are means of four quarter-hours."}
      - {series: fr, label: France, codes: FR, paint: horizon}
      - {series: nl, label: Netherlands, codes: NL, paint: olive}
      - {series: be, label: Belgium, codes: BE, paint: clay}
  raw_feed:
    note: >-
      From the ENTSO-E Transparency Platform, one call per zone and UTC day. Replies hold whole
      delivery days (from 22:00 UTC here); `gridflow transform` keeps rows inside the requested day.
    requests:
      - "GET https://web-api.tp.entsoe.eu/api?documentType=A44&periodStart=202609200000&periodEnd=202609210000&in_Domain=10Y1001A1001A59C&out_Domain=10Y1001A1001A59C&securityToken=<your-entsoe-api-key>"
    commands:
      - {run: gridflow ingest entsoe day_ahead_prices --start 2026-09-14 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform entsoe day_ahead_prices --start 2026-09-14 --end 2026-09-20, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: area_code, op: ne, value: "10Y1001A1001A82H"}
        - {column: timestamp_utc, op: in, value: ["2026-09-20T12:00:00", "2026-09-20T13:00:00"]}
      order_by: [timestamp_utc, area_code]
      columns: [timestamp_utc, area_code, price_eur_mwh, currency, resolution, published_at]
    key: [timestamp_utc, area_code]
    caption: "12:00 and 13:00 UTC, 20 September 2026: IE-SEM above 200, the rest below zero."
    fields:
      timestamp_utc: "Start of the price period, UTC: `start + (position - 1) × resolution`"
      area_code: "Bidding-zone EIC from `in_Domain.mRID`, as sent; `10Y1001A1001A59C` is IE-SEM"
      price_eur_mwh: "Price per MWh in `currency`; omitted points repeat the previous one (curve type A03)"
      currency: "Vendor's `currency_Unit.name`; trust it over the `price_eur_mwh` column name"
      resolution: "Vendor period length: `PT15M` or `PT60M` in these rows"
      published_at: "Response `createdDateTime`, stamped within seconds of the fetch; not the auction time"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_entsoe_day_ahead_prices`, filtered
      on `timestamp_utc` (UTC days, both ends included), returned in the session's time zone,
      Europe/London here. Lineage columns are dropped; rows are ordered by time only.
    cells:
      - |
        df = data.entsoe.query("day_ahead_prices", "2026-09-14", "2026-09-20")
        df = df.sort_values(["area_code", "timestamp_utc"])
      - df[["timestamp_utc", "area_code", "price_eur_mwh", "currency", "resolution"]].head()
      - |
        fr = df[df.area_code.str.startswith("10YFR")]
        ie = df[df.area_code == "10Y1001A1001A59C"]
        ax = fr.plot(x="timestamp_utc", y="price_eur_mwh", label="FR, 15 min",
                     color="#3E8C97", figsize=(8, 3.5))
        ie.plot(x="timestamp_utc", y="price_eur_mwh", label="IE-SEM, hourly",
                color="#155A6E", ylabel="EUR/MWh", ax=ax)
    needs: 14 to 20 September 2026
    plot_alt: >-
      Line plot of price_eur_mwh against timestamp_utc, 14 to 20 September 2026: FR's quarter-hours
      (about -1 to 333 EUR/MWh) and IE-SEM's hours (1 to 359). The two share a daily shape until
      the 20th, when FR sits near zero from early morning to mid-afternoon while IE-SEM rises to 359.
  related:
    - {dataset: entsoe/cross_border_flows, note: "Physical flows across the borders between these same zones"}
    - {dataset: entsoe/actual_load, note: "Realised load in the same bidding zones"}
    - {dataset: entsoe/wind_solar_forecast, note: "Day-ahead wind and solar forecasts for the same zones and days"}
    - {dataset: elexon/mid, note: "GB's market index price, the GB side of a spread"}
---

# ENTSO-E — Day-ahead Prices (A44)

## Overview

Day-ahead market clearing prices in EUR/MWh for each bidding zone, published
by the ENTSO-E Transparency Platform (Article 12.1.D of EU Regulation
543/2013). Each `<TimeSeries>` represents an `(in_Domain, out_Domain)` pair
(typically the same EIC for an internal day-ahead price); `<Point>` elements
carry the cleared price for each settlement interval (typically PT60M or
PT15M for the integrated 15-minute markets).

This is the canonical EU price reference for spread modelling across
interconnected zones — used as the baseline against which UK GB prices,
balancing prices, and intraday prices are compared. Post-Brexit, GB
day-ahead prices are not published on ENTSO-E (returns Acknowledgement code
999 — see Implementation delta below).

Related domain notes:
  [Day-ahead market](../../../20-domain/markets/day-ahead.md)
  [EIC codes](../../../20-domain/concepts/eic-codes.md)

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://web-api.tp.entsoe.eu` |
| Path             | `/api` |
| Method           | GET |
| Auth             | Query param `securityToken` from env var `ENTSOE_API_KEY` |
| Rate limit       | Not vendor-published — codebase configured at 1 req/s (`config/sources.yaml:192`); treat 1 req/s as polite |
| Pagination       | None |
| Historical depth | ~5 years on most zones (vendor-bounded) |
| Publication lag  | ~12:55 CET D-1 for D, then revisions |
| Response format  | XML (Publication_MarketDocument); larger windows may be returned as a ZIP-of-XML |
| Document type    | `A44` |
| Process type     | n/a |
| Domain param name | `in_Domain`, `out_Domain` (zone-pair, both set to the bidding zone EIC for an internal day-ahead price) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `securityToken` | str | yes | API key (UUID) | `<your-entsoe-api-key>` |
| `documentType` | str | yes | Always `A44` | `A44` |
| `in_Domain` | str (EIC mRID) | yes | Bidding zone EIC | `10Y1001A1001A82H` |
| `out_Domain` | str (EIC mRID) | yes | Bidding zone EIC (= `in_Domain` for an intra-zone price) | `10Y1001A1001A82H` |
| `periodStart` | str (`yyyyMMddHHmm` UTC) | yes | Window start | `202605060000` |
| `periodEnd` | str (`yyyyMMddHHmm` UTC) | yes | Window end (max one year, vendor-enforced) | `202605070000` |

### Working curl example

```bash
# Replace <your-entsoe-api-key> with $ENTSOE_API_KEY
curl -X GET --ssl-no-revoke \
  "https://web-api.tp.entsoe.eu/api?securityToken=<your-entsoe-api-key>&documentType=A44&in_Domain=10Y1001A1001A82H&out_Domain=10Y1001A1001A82H&periodStart=202605060000&periodEnd=202605070000" \
  -H "Accept: application/xml"
```

Note: GB (`10YGB----------A`) returns Acknowledgement code 999 ("No matching
data found for Data item ENERGY_PRICES [12.1.D]") because GB exited the
EU day-ahead market after Brexit. Use Elexon `system_prices` for GB.

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsoe/day_ahead_prices/<year>/<month>/<day>/raw_<uuid>.xml`
**Format**: Raw XML, as-received. Immutable — never modified after write.
**Granularity**: One file per (zone, query window). ZIP responses (large windows) are unpacked and each inner XML is stored as a separate raw file.

### Bronze sample

(First ~500 bytes of a DE-LU PT60M day-ahead response, 2026-05-06.)

```json
{
  "envelope": "Publication_MarketDocument xmlns='urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3'",
  "type": "A44",
  "createdDateTime": "2026-05-05T11:00:00Z",
  "TimeSeries": [
    {
      "mRID": "1",
      "businessType": "A62",
      "in_Domain.mRID": "10Y1001A1001A82H",
      "out_Domain.mRID": "10Y1001A1001A82H",
      "currency_Unit.name": "EUR",
      "price_Measure_Unit.name": "MWH",
      "Period": {
        "timeInterval": {"start": "2026-05-06T00:00Z", "end": "2026-05-07T00:00Z"},
        "resolution": "PT60M",
        "Point": [
          {"position": 1, "price.amount": 85.50},
          {"position": 2, "price.amount": 82.30}
        ]
      }
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsoe/day_ahead_prices/year=YYYY/month=MM/day_ahead_prices_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsoe.day_ahead_prices.DayAheadPricesTransformer`
**Pydantic schema**: `gridflow.schemas.entsoe.EntsoeDayAheadPrice`
**Dedup key**: `(timestamp_utc, area_code)` — last write wins
**Point-in-time field**: `published_at`, the response document's `createdDateTime` (`silver/entsoe/day_ahead_prices.py:93-94`). In the September 2026 captures it matches the fetch time (for example `createdDateTime` 2026-09-21T09:59:33Z in a response fetched at 09:59:34Z), not the auction's publication time.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `timestamp_utc` | `datetime` (tz-aware UTC) | No | `Period.timeInterval.start + (position-1)*resolution` | Rejected if naive |
| `area_code` | `str` | No | `TimeSeries/in_Domain.mRID` | EIC bidding zone mRID, as-is (no normalisation) |
| `price_eur_mwh` | `float` | No | `Point/price.amount` | Price per MWh in `currency` (the `_eur_` name is legacy; `schemas/entsoe.py:13-20`). Curve type A03 omits repeated points; the parser forward-fills them (`connectors/entsoe/parsers.py:533-601`) |
| `currency` | `str` | No (default `"EUR"`) | `TimeSeries/currency_Unit.name` | Source denomination (EUR/GBP); authoritative over the legacy `_eur_` value-column name. |
| `resolution` | `str` | No (default `""`) | `Period/resolution` | ISO duration: `PT60M` or `PT15M` |
| `published_at` | `datetime` (tz-aware UTC) | Yes | `Publication_MarketDocument/createdDateTime` | Response document creation time (`silver/entsoe/day_ahead_prices.py:93-94`; `schemas/entsoe.py:28`) |
| `data_provider` | `str` | No (default `"entsoe"`) | derived | Constant `"entsoe"` |
| `ingested_at` | `datetime` (tz-aware UTC) | Yes | derived | Set by transformer at silver write |

### Silver sample

```python
[
    {
        "timestamp_utc": datetime(2026, 5, 6, 0, 0, tzinfo=UTC),
        "area_code": "10Y1001A1001A82H",
        "price_eur_mwh": 85.50,
        "resolution": "PT60M",
        "data_provider": "entsoe",
        "ingested_at": datetime(2026, 5, 8, 18, 4, 28, tzinfo=UTC),
    },
    {
        "timestamp_utc": datetime(2026, 5, 6, 1, 0, tzinfo=UTC),
        "area_code": "10Y1001A1001A82H",
        "price_eur_mwh": 82.30,
        "resolution": "PT60M",
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

- **GB returns Acknowledgement code 999** — post-Brexit, GB day-ahead prices
  are not published via ENTSO-E. The connector still queries GB by default
  (`DEFAULT_ZONES` includes `GB`); the silver transformer simply produces
  zero rows for GB. Use Elexon `system_prices` for GB market reference.
- **15-minute zones**: in the September 2026 captures FR, NL, BE and DE-LU
  send PT15M and IE-SEM sends PT60M (bronze
  `day_ahead_prices/2026/09/15/raw_20260921T0959*.xml`). The silver schema preserves `resolution` as a string;
  downstream gold/model layers must aggregate or interpolate as needed.
- **ZIP-of-XML responses**: large windows (multi-day) may be returned as a
  ZIP archive containing day-partitioned XML files. The connector
  auto-detects (`PK\x03\x04` magic bytes) and unpacks before silver parsing.
- **`in_Domain` == `out_Domain`** for intra-zone day-ahead prices. The
  connector sends both with the same EIC; silver maps `in_Domain.mRID`
  to `area_code`.
- **No revisions**: day-ahead prices are not republished post-clearing.
  The dedup `(timestamp_utc, area_code)` is not sufficient for DE-LU: its
  documents carry two TimeSeries per delivery day,
  `classificationSequence_AttributeInstanceComponent.position` 1 and 2, with
  different prices (up to 322 EUR/MWh apart on 14 September 2026). The parser
  does not read the sequence and `unique(keep="last")`
  (`silver/entsoe/day_ahead_prices.py:83`) keeps whichever series the latest reply
  for that day lists last (`read_bronze` concatenates every capture in name
  order, `:36`), so silver DE-LU mixes the two (14 Sep 2026: 87 quarter-hours
  from sequence 1, 8 from sequence 2; 15 Sep: 8 and 88). The document does not
  say what the sequences are. FR, BE and IE-SEM also send two series per day
  on some days, but with identical prices.

---

## Implementation delta

- **Tuple comparison**: code-tuple in `endpoints.py` for `day_ahead_prices`
  is `(documentType=A44, processType=None, businessType=None, domain=in_Domain+out_Domain)`.
  Reference docs (ENTSO-E Static Content Guide PDF) could not be fetched
  directly during this validation pass (`HTTP 400` from
  `transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.pdf`
  — likely CDN protection); the tuple is `unverified - PDF fetch failed`
  against the canonical guide. However the live response on a known-good
  zone (DE-LU) returns a well-formed `<Publication_MarketDocument><type>A44`
  with `<TimeSeries>`, confirming the request shape is accepted by the API.
- No discrepancies between the connector's request shape and the live API's
  accepted shape were observed.

---

## Modelling notes

- Used as the reference EU spot reference for cross-border spread features
  (FR, NL, BE, IE-SEM vs. GB). For UK price modelling, GB clearing comes
  from Elexon (`system_prices`) and the EU side from ENTSO-E here.
- Common derived features: hourly clean-spark spread, peak/off-peak diff,
  rolling daily volatility, day-of-week mean.
- Filter rule: drop rows with `area_code == "10YGB----------A"` for any
  modelling feature (always empty post-Brexit).

---

## Links

- [Official API docs](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html)
- `src/gridflow/connectors/entsoe/client.py`
- `src/gridflow/connectors/entsoe/endpoints.py`
- `src/gridflow/silver/entsoe/day_ahead_prices.py`
- `src/gridflow/schemas/entsoe.py`
- Gold view/builder
- [Domain: day-ahead market](../../../20-domain/markets/day-ahead.md)
