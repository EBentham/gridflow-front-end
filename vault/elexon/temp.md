---
source: elexon
dataset_key: temp
vendor: Elexon BMRS
last_verified: 2026-05-21
layer_coverage: bronze, silver
v2_fix_history:
  - date: 2026-05-20
    phase: gridflow-G5-W1.4
    pr: https://github.com/EBentham/gridflow/pull/7
    change: silver transformer now carries vendor measurementDate through as `measurement_date` (Date)
  - date: 2026-05-20
    phase: gridflow-G5-W4
    pr: https://github.com/EBentham/gridflow/pull/7
    change: ElexonTemp Pydantic schema declared
page:
  title: Temperature
  summary: >-
    Elexon's midday temperature for Great Britain, averaged over six weather stations, with the date
    it is for and its publish time.
  facts:
    vendor: Elexon BMRS, dataset TEMP
    cadence: Measured at midday, per Elexon; most shown published at 15:45 UTC
    grain: One row per publish time, each carrying its measurement date
  what_it_is: >-
    Elexon's TEMP: the average °C value measured at midday for Great Britain, gathered from six
    weather stations. Each row carries the date it is for and its publish time; the response has no
    unit field. gridflow fetches and dates each row by its publish time, so 13 September's reading,
    published the next morning, arrives with the 14th.
  how_used:
    - A daily temperature feature for a GB demand or price model.
    - "Proxy degree days: this midday reading stands in for the usual daily mean."
    - Setting a day's demand outturn or forecast against its temperature.
  chart:
    type: line
    silver: elexon/temp
    time: measurement_date
    value: temperature
    filter:
      - {column: measurement_date, op: ge, value: "2026-09-13"}
      - {column: measurement_date, op: le, value: "2026-09-21"}
    dedup: {"on": [measurement_date], order_by: timestamp_utc}
    aggregation: last
    window: {start: "2026-09-13", end: "2026-09-21"}
    unit: °C
  chart_view:
    title: Temperature, 13 to 21 September 2026
    caption: >-
      Silver `elexon/temp`, °C (Elexon's unit), one point per measurement date from 13 to 21
      September 2026, the latest publication of each. Each point sits on its measurement
      date, not its publish time.
    alt: >-
      Line chart of temperature from elexon/temp, in °C, one point per measurement date from 13 to
      21 September 2026. It starts at 17.7 on the 13th, peaks at 18.6 on the 14th, eases to 18.3 on
      the 15th, then falls to 16.0 on the 18th, rises to 17.1 on the 19th and ends at 16.0 on the
      21st.
    x_label: measurement date
    key:
      - {series: temperature, label: Temperature, codes: TEMP, paint: petrol, note: "13 September's reading was published on the 14th, at 09:06 UTC."}
  raw_feed:
    note: >-
      From the Elexon Insights API, in 24-hour publish windows. A reading arrives in its publish
      window, so 13 September's came with the 14th. `gridflow transform` types it into silver.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/TEMP?publishDateTimeFrom=2026-09-14T00:00:00Z&publishDateTimeTo=2026-09-15T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon temp --start 2026-09-14 --end 2026-09-22, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon temp --start 2026-09-14 --end 2026-09-21, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: measurement_date, op: ge, value: "2026-09-13"}
        - {column: measurement_date, op: le, value: "2026-09-20"}
      order_by: [timestamp_utc]
    key: [timestamp_utc]
    caption: "Measurement dates 13 to 20 September 2026; the first was published the next morning."
    fields:
      timestamp_utc: "Vendor publish time (`publishTime`), UTC; the row key"
      measurement_date: "The date the reading is for (`measurementDate`), as sent"
      temperature: "Elexon's six-station average, °C, measured at midday; the response sends no unit"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_temp`, filtered on
      `timestamp_utc`, the publish time, with both end dates included: 14 to 21 September brings
      readings for 13 to 21. Lineage columns are dropped.
    cells:
      - |
        df = data.elexon.query("temp", "2026-09-14", "2026-09-21")
        df = df.sort_values("timestamp_utc")
        df["timestamp_utc"] = df["timestamp_utc"].dt.tz_convert("UTC")
      - df[["timestamp_utc", "measurement_date", "temperature"]].head()
      - |
        df.plot(x="measurement_date", y="temperature", ylabel="°C",
                color="#155A6E", figsize=(8, 3.5))
    needs: publish dates 14 to 21 September 2026
    plot_alt: >-
      Line plot of temperature against measurement_date, 13 to 21 September 2026: 17.7 °C on the
      13th, 18.6 on the 14th, down to 16.0 on the 18th, 17.1 on the 19th and 16.0 on the 21st.
  related:
    - {dataset: elexon/indo, note: Demand outturn for the same days}
    - {dataset: elexon/ndf, note: Demand forecasts for the same days}
    - {dataset: openmeteo/historical_demand, note: "City-level hourly temperature to set against this six-station GB value"}
    - {dataset: openmeteo/forecast_demand, note: "City-level temperature forecasts, available before this GB value is published"}
---

# Elexon - Temperature Data (`TEMP`)

## Overview

GB ambient temperature data — daily-published values used by NESO in demand-forecasting calibration. The dataset publishes one record per measurement date with the realised temperature. The `/datasets/TEMP` response carries no seasonal-normal, low or high reference values (fields `dataset`, `measurementDate`, `publishTime`, `temperature` only; bronze sample below).

Elexon's endpoint description, read in a browser on 2026-09-28 at
https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/TEMP (the page renders only with JavaScript):
"This endpoint provides the average degree celsius value measured at midday deemed to be representative of the
temperature for Great Britain. Data is gathered from 6 weather stations. Default output will be the last 31 days.
Values are received from 5pm each day." The same page's response schema shows the four fields above and no unit field.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/TEMP` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Daily publication. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | No | As per Elexon Swagger spec for temp. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | As per Elexon Swagger spec for temp. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/TEMP?publishDateTimeFrom=2026-04-01T00:00Z&publishDateTimeTo=2026-04-02T00:00Z&format=json" \
  -o "/tmp/elexon-temp.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/temp/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/TEMP?publishDateTimeFrom=2026-04-01T00:00Z&publishDateTimeTo=2026-04-02T00:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "TEMP",
      "measurementDate": "2026-04-01",
      "publishTime": "2026-04-01T15:45:00Z",
      "temperature": 10.6
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/temp/year=YYYY/month=MM/temp_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.temp.TempTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonTemp` (added 2026-05-20, gridflow G5-W4).
**Dedup key**: `(timestamp_utc)`
**Point-in-time field**: `timestamp_utc`, the vendor `publishTime` (`temp.py:58-59`); no separate `published_at` column

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `measurement_date` | `date` | Yes | `measurementDate` | G5-W1.4: vendor measurement-date carried through to silver. |
| `timestamp_utc` | `datetime[UTC]` | No | `publishDateTime` or `publishTime` | The vendor publish instant, renamed and parsed as `%Y-%m-%dT%H:%M:%SZ` (`temp.py:58-59,80-84`); falls back to `measurement_date` at 00:00Z only when no publish field is present (`temp.py:70-74`). It is the dedup key, so a measurement date published twice keeps two rows. |
| `temperature` | `float` | No | `temperature` | Celsius — measured. |
| `normal_temperature` | `float` | Yes | `normal` | Celsius — seasonal normal. Not in the `/datasets/TEMP` response (bronze sample above has no `normal`); written only if bronze carries it (`temp.py:62,86-88,116`). |
| `low_temperature` | `float` | Yes | `low` | Celsius — seasonal low. Not in the `/datasets/TEMP` response; written only if bronze carries `low` (`temp.py:63,116`). |
| `high_temperature` | `float` | Yes | `high` | Celsius — seasonal high. Not in the `/datasets/TEMP` response; written only if bronze carries `high` (`temp.py:64,116`). |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`temp.py:98-103`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-04-01T15:45:00Z",
        "measurement_date": "2026-04-01",
        "temperature": 10.6,
        "data_provider": "elexon",
        "ingested_at": "2026-05-08T12:00:00Z"
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Daily resolution** — one reading per measurement date, but the row key is the publish time (`temp.py:25,96`). A reading published the next morning lands in the next day's publish window and silver partition: 2026-09-13's was published 2026-09-14T09:06:00Z (bronze `2026/09/14`; the 2026-09-13 window returned `{"data":[]}`).
- **Reference temperatures** (normal/low/high) are seasonal climatology, not forecasts.

---

## Implementation delta

- **Daily publication** — empty within 3-hour windows.
- **Pydantic schema declared** as of gridflow G5-W4: `ElexonTemp`.

### V2-FIX changelog

- **2026-05-20 — gridflow G5-W1.4 (PR #7)**: silver transformer now casts
  `measurementDate` to a Date column and includes it in `output_cols`.
  Previously the field was renamed but dropped before write — schema
  table claimed the field existed, code silently omitted it (P2
  schema-vs-output mismatch bug).
- **2026-05-20 — gridflow G5-W4 (PR #7)**: `ElexonTemp` Pydantic class
  added to `schemas/elexon.py`.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/temp.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
