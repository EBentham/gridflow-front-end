---
source: elexon
dataset_key: windfor
vendor: Elexon BMRS
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Wind generation forecast
  summary: >-
    Elexon's hourly forecast of GB wind generation, issued up to eight times a day; gridflow keeps
    every issue.
  facts:
    vendor: Elexon BMRS, dataset WINDFOR
    cadence: Up to eight issues a day, per Elexon's API docs
    grain: One row per target hour and issue time
  landscape: power
  what_it_is: >-
    Elexon's wind generation forecast (WINDFOR), which its API docs say covers wind farms the ESO
    can see through operational metering. Each issue gives one figure per hour; those charted,
    all published on 20 September, run to 20:00 UTC on the 22nd. gridflow keeps every issue,
    keyed on its publish time. The feed sends no unit; gridflow's column says MW.
  how_used:
    - A point-in-time wind feature for a GB price model, from the issue then available.
    - Residual demand ahead of time, from a demand forecast less forecast wind.
    - Forecast error and revision, scored against WIND outturn in FUELHH.
  chart:
    type: line
    silver: elexon/windfor
    time: timestamp_utc
    value: latest_forecast_mw
    filter:
      - {column: published_at, op: in, value: ["2026-09-20T03:30:00Z", "2026-09-20T12:30:00Z", "2026-09-20T23:30:00Z"]}
    group: published_at
    group_map:
      "2026-09-20 03:30:00.000000+00:00": issue_0330
      "2026-09-20 12:30:00.000000+00:00": issue_1230
      "2026-09-20 23:30:00.000000+00:00": issue_2330
    series_order: [issue_0330, issue_1230, issue_2330]
    aggregation: last
    window: {start: "2026-09-20", end: "2026-09-22"}
    unit: MW
  chart_view:
    title: Three issues of 20 September 2026
    caption: >-
      Silver `elexon/windfor`, MW, one value per target hour from 00:00 UTC on 20 September to
      20:00 UTC on the 22nd, from three of the eight issues published on the 20th. Where lines
      meet, the later issue repeats hours already begun.
    alt: >-
      Line chart of three forecast issues from elexon/windfor, in MW, for each target hour from
      00:00 UTC on 20 September to 20:00 UTC on the 22nd, issued at 03:30, 12:30 and 23:30 UTC on
      the 20th. All three peak at 20,629 at 01:00 on the 20th, then fall to lows of 4,769, 4,017
      and 3,449 early on the 21st. From 02:00 to 23:00 on the 21st each later issue is lower. They
      end at 2,815, 2,287 and 1,603.
    x_label: target hour, UTC
    key:
      - {series: issue_0330, label: Issued 03:30 UTC, paint: clay}
      - {series: issue_1230, label: Issued 12:30 UTC, paint: petrol}
      - {series: issue_2330, label: Issued 23:30 UTC, paint: horizon, note: "At 12:00 UTC on the 21st: 4,106, against 6,338 from the 03:30 issue."}
  raw_feed:
    note: >-
      From the Elexon Insights API, in 24-hour publish windows: a day's bronze holds the issues
      published that day. `gridflow transform` types them into silver, one row per hour and issue.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR?publishDateTimeFrom=2026-09-20T00:00:00Z&publishDateTimeTo=2026-09-21T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon windfor --start 2026-09-20 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon windfor --start 2026-09-20 --end 2026-09-20, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: timestamp_utc, op: eq, value: "2026-09-21T12:00:00Z"}
        - {column: published_at, op: ge, value: "2026-09-20T00:00:00Z"}
        - {column: published_at, op: lt, value: "2026-09-21T00:00:00Z"}
      order_by: [published_at]
    key: [timestamp_utc, published_at]
    caption: "Target hour 12:00 UTC on 21 September, from all eight issues published on the 20th."
    fields:
      timestamp_utc: "Target hour the forecast is for, from the vendor `startTime`, UTC"
      latest_forecast_mw: "Forecast from `generation`; MW by gridflow's column name, the feed sends no unit"
      published_at: "Issue time, from the vendor `publishTime`, UTC"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB relation `silver_elexon_windfor`, filtered on
      `timestamp_utc`, the target hour, whole UTC days with both ends included: every stored issue
      for those hours. Lineage columns are dropped.
    cells:
      - |
        df = data.elexon.query("windfor", "2026-09-20", "2026-09-22")
        for col in ["timestamp_utc", "published_at"]:
            df[col] = df[col].dt.tz_convert("UTC")
        df = df[df.published_at.dt.day == 20]
      - df.sort_values(["timestamp_utc", "published_at"])[["timestamp_utc", "published_at", "latest_forecast_mw"]].head()
      - |
        wide = df.pivot(index="timestamp_utc", columns="published_at", values="latest_forecast_mw")
        wide.columns = wide.columns.strftime("%H:%M")
        wide.plot(ylabel="MW", figsize=(8, 3.5))
    needs: issues published on 20 September 2026
    plot_alt: >-
      Line plot of latest_forecast_mw against timestamp_utc, one line for each of the eight issues
      published on 20 September 2026, labelled 03:30 to 23:30. All start near 20,300 MW at 00:00
      UTC on the 20th, fall to lows of 3,400 to 4,800 MW early on the 21st, and end between 1,603
      and 2,815 MW at 20:00 UTC on the 22nd.
  related:
    - {dataset: elexon/fuelhh, note: "WIND outturn per settlement period, to score these forecasts"}
    - {dataset: elexon/agws, note: "Actual or estimated wind generation, onshore and offshore, to check against"}
    - {dataset: elexon/fuelinst, note: "Five-minute WIND outturn, for checking the forecast within the day"}
    - {dataset: elexon/ndf, note: "Demand forecast; less forecast wind, it gives residual demand"}
---

# Elexon - Wind Generation Forecast (`WINDFOR`)

## Overview

Wind Generation Forecast, hourly, reissued up to 8 times a day: Elexon's OpenAPI description of `/forecast/generation/wind` says NGESO publishes it at 03:30, 05:30, 08:30, 10:30, 12:30, 16:30, 19:30 and 23:30, for wind farms visible to the ESO with operational metering. Each `/datasets/WINDFOR` row is one issue's figure (`generation`, an integer, no unit field) for one target hour (`startTime`), stamped with its issue time (`publishTime`); the row schema (`DatasetRows.WindGenerationForecast`) has no initial/latest split and no settlement fields. WINDFOR is the canonical GB wind forecast against which actual wind output (FUELHH) is benchmarked.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/WINDFOR` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Up to 8 issues a day (Elexon OpenAPI, `/forecast/generation/wind`). |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | No | As per Elexon Swagger spec for windfor. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | As per Elexon Swagger spec for windfor. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR?publishDateTimeFrom=2026-05-05T00:00Z&publishDateTimeTo=2026-05-06T00:00Z&format=json" \
  -o "/tmp/elexon-windfor.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/windfor/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR?publishDateTimeFrom=2026-05-05T00:00Z&publishDateTimeTo=2026-05-06T00:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "WINDFOR",
      "publishTime": "2026-05-05T23:30:00Z",
      "startTime": "2026-05-04T20:00:00Z",
      "generation": 2983
    },
    {
      "dataset": "WINDFOR",
      "publishTime": "2026-05-05T23:30:00Z",
      "startTime": "2026-05-04T21:00:00Z",
      "generation": 3046
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/windfor/year=YYYY/month=MM/windfor_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.wind_forecast.WindForecastTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonWindForecast`
**Dedup key**: `(timestamp_utc, published_at)`, keep last: this endpoint sends no settlement fields, so the `(settlement_date, settlement_period, published_at)` branch never applies (`silver/elexon/wind_forecast.py:160-165`). A silver file's date is its bronze publish-window date, so it holds the issues published that day (`connectors/elexon/client.py:314` sets `data_date` to the window start; `wind_forecast.py:60-84` reads that one bronze day).
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | Yes | `settlementDate` | Not written: `/datasets/WINDFOR` sends no `settlementDate`, and the transformer selects only columns present (`wind_forecast.py:175-186`). Declared nullable in ElexonWindForecast. |
| `settlement_period` | `int` | Yes | `settlementPeriod` | Not written, as `settlement_date`. |
| `timestamp_utc` | `datetime[UTC]` | No | `startTime` | The target hour's start, parsed from the vendor `startTime` (`wind_forecast.py:133-140`); the settlement-period branch needs fields this endpoint does not send. |
| `initial_forecast_mw` | `float` | Yes | `initialForecast` | Not written: the endpoint sends no `initialForecast`. |
| `latest_forecast_mw` | `float` | Yes | `generation` | That issue's forecast, cast to float; MW by column name, the response has no unit field. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Issue time of the forecast, UTC (`wind_forecast.py:146-151`). Part of the dedup key. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`wind_forecast.py:167-173`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "timestamp_utc": "2026-09-21T12:00:00+00:00",
        "latest_forecast_mw": 6338.0,
        "published_at": "2026-09-20T03:30:00+00:00",
        "data_provider": "elexon",
        "ingested_at": "2026-09-26T18:31:15.792291+00:00"
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Sparse publication** — multiple publishes per day; not strictly half-hourly.
- **Revisions are rows, not columns**: `latest_forecast_mw` is each issue's own figure and `initial_forecast_mw` is never written. The same `timestamp_utc` appears once per issue, told apart by `published_at` (`wind_forecast.py:160-165`).

---

## Implementation delta

- **Sparse publication cadence** — empty within 3-hour windows; required at-least-1-day window in V1 validation.
- **`ElexonWindForecast` schema** allows `settlement_date` and `settlement_period` to be `None`.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/wind_forecast.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
