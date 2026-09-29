---
source: elexon
dataset_key: ndf
vendor: Elexon BMRS
last_verified: 2026-07-31
layer_coverage: bronze, silver
page:
  title: Demand forecasts
  summary: >-
    Elexon's GB demand forecasts: half-hourly `NDF` (national) and `TSDF` (transmission), and daily
    `NDFD` and `TSDFD` for 2 to 14 days ahead.
  facts:
    vendor: Elexon BMRS, datasets NDF, NDFD, TSDF and TSDFD
    cadence: NDF and TSDF about every 30 minutes; NDFD and TSDFD daily
    grain: "NDF: half-hour and publish; TSDF: half-hour, boundary, publish day; NDFD, TSDFD: date, publish"
  landscape: power
  what_it_is: >-
    `NDF` forecasts GB national demand, which NESO equates with `INDO`, for each half-hour; silver
    keeps every publish. `TSDF` forecasts transmission system demand, which NESO equates with
    `ITSDO`, as boundary `N`, beside other boundary codes (`B1`, `B2` and so on). `NDFD` and `TSDFD`
    give one figure per day, 2 to 14 days ahead; the fields do not say which daily statistic.
  how_used:
    - The benchmark a GB demand model has to beat, scored against `INDO`.
    - "Forecast-revision features: how a half-hour's forecast moves from publish to publish."
    - A demand outlook for the next two weeks, one figure a day, from `NDFD`.
  chart:
    type: line
    silver: elexon/ndf
    time: timestamp_utc
    value: national_demand_mw
    filter:
      - {column: settlement_date, op: eq, value: "2026-09-17"}
      - {column: published_at, op: in, value: ["2026-09-16T07:45:00Z", "2026-09-16T22:47:00Z"]}
    group: published_at
    group_map:
      "2026-09-16 07:45:00.000000+00:00": morning
      "2026-09-16 22:47:00.000000+00:00": evening
    series_order: [morning, evening]
    aggregation: last
    window: {start: "2026-09-16", end: "2026-09-17"}
    unit: MW
  chart_view:
    title: Two forecasts for 17 September 2026, published the day before
    caption: >-
      Silver `elexon/ndf`, MW, settlement date 17 September 2026 as two publishes on 16 September
      forecast it, one value per half-hour. Other publishes are not drawn; the frame below follows
      one half-hour through eight.
    alt: >-
      Line chart of the GB national demand forecast (NDF) from elexon/ndf, in MW, for settlement
      date 17 September 2026, as published at 07:45 and 22:47 UTC on 16 September. The 07:45 line
      starts at 04:00 UTC, at 18,180 MW. The lines stay within 460 MW of each other until 07:00 UTC;
      from 07:30 the 07:45 publish runs higher, by up to 2,712 MW at 15:00 UTC. It peaks at 29,970
      MW at 18:30; the 22:47 publish peaks at 29,000 MW at 18:00 and dips to 18,000 MW at 03:00.
    x_label: UTC; the settlement day begins 23:00, 16 September
    key:
      - {series: morning, label: 07:45 UTC publish, codes: NDF, note: "Starts at 04:00 UTC: this publish holds no earlier half-hours of the day.", paint: petrol}
      - {series: evening, label: 22:47 UTC publish, codes: NDF, paint: clay}
  raw_feed:
    note: >-
      From the Elexon Insights API in 24-hour publish windows; swap `NDF` for `NDFD`, `TSDF` or
      `TSDFD`. Each silver file holds one UTC publish day, so a settlement date spans several.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/NDF?publishDateTimeFrom=2026-09-16T00:00:00Z&publishDateTimeTo=2026-09-17T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon ndf --start 2026-09-13 --end 2026-09-21, comment: "bronze; the end is exclusive"}
      - {run: gridflow transform elexon ndf --start 2026-09-13 --end 2026-09-20, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-17"}
        - {column: settlement_period, op: eq, value: 36}
        - column: published_at
          op: in
          value: ["2026-09-16T07:45:00Z", "2026-09-16T11:18:00Z", "2026-09-16T17:47:00Z", "2026-09-16T19:47:00Z",
                  "2026-09-16T21:47:00Z", "2026-09-17T06:46:00Z", "2026-09-17T09:46:00Z", "2026-09-17T16:18:00Z"]
      order_by: [published_at]
    key: [settlement_date, settlement_period, forecast_type, published_at]
    caption: "Eight publishes of the forecast for 17 September, period 36 (16:30 UTC), oldest first."
    fields:
      settlement_date: "GB settlement date, the vendor's `settlementDate` label"
      settlement_period: Half-hour of the settlement date, 1 to 48; 46 or 50 on clock-change days
      timestamp_utc: Start of the half-hour, computed from the settlement date and period
      forecast_type: "`day_ahead` on every NDF row; NDFD rows carry `2_14_day`"
      national_demand_mw: "Forecast national demand for the half-hour in MW, the vendor's `demand`"
      published_at: "Vendor publish time, from `publishTime`; in the key, so every publish stays"
  notebook:
    lead: >-
      Returns pandas DataFrames from `silver_elexon_ndf` and `silver_elexon_indo`, filtered on
      `settlement_date`, both ends included; lineage columns dropped. The query cell converts times
      to UTC; the rest score the 07:45 UTC and last publishes against INDO.
    cells:
      - |
        ndf = data.elexon.query("ndf", "2026-09-14", "2026-09-20")
        indo = data.elexon.query("indo", "2026-09-14", "2026-09-20")
        for df in (ndf, indo):
            df["timestamp_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
        ndf["published_at"] = ndf.published_at.dt.tz_convert("UTC")
      - |
        cols = ["timestamp_utc", "national_demand_mw"]
        morning = ndf[ndf.published_at.dt.strftime("%H:%M") == "07:45"][cols]
        last = ndf.sort_values("published_at").groupby("timestamp_utc").tail(1)[cols]
        both = morning.merge(last, on="timestamp_utc").merge(
            indo[["timestamp_utc", "initial_demand_outturn_mw"]], on="timestamp_utc")
        both.columns = ["timestamp_utc", "ndf_0745_mw", "ndf_last_mw", "indo_mw"]
        both = both.sort_values("timestamp_utc", ignore_index=True)
        both.head()
      - |
        err = both.set_index("timestamp_utc")[["ndf_0745_mw", "ndf_last_mw"]].sub(both.indo_mw.values, axis=0)
        err.abs().mean().round()
      - |
        err.plot(ylabel="forecast minus INDO, MW", color=["#155A6E", "#C77E3C"], figsize=(8, 3.5))
    needs: NDF and INDO, published 13 to 20 September 2026
    plot_alt: >-
      Line plot of forecast minus INDO outturn, in MW, from 04:00 UTC on 14 September to 22:30 UTC
      on 20 September: the 07:45 UTC publish (petrol) and the last publish (clay). The 07:45 line
      reaches 3,603 MW at 15:00 UTC on the 15th and falls to -1,360 MW on the 19th; the last
      publish stays between -1,015 and 2,943 MW.
  related:
    - {dataset: elexon/indo, note: "National outturn to score `NDF` against, at the same boundary"}
    - {dataset: elexon/itsdo, note: "Transmission outturn to score `TSDF` boundary `N` against"}
    - {dataset: elexon/windfor, note: "Wind forecast; subtract it from `NDF` for residual demand"}
    - {dataset: neso_data_portal/embedded_wind_solar_forecast, note: "Embedded wind and solar forecast, which lowers national demand"}
  family:
    slug: demand-forecasts
    members:
      - dataset: ndf
        differs: "Half-hourly national demand; every publish kept, keyed by `published_at`"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/NDF?publishDateTimeFrom=2026-09-16T00:00:00Z&publishDateTimeTo=2026-09-17T00:00:00Z&page=1"
      - dataset: ndfd
        differs: "One national figure per date, 2 to 14 days ahead; period fixed at 1"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/NDFD?publishDateTimeFrom=2026-09-16T00:00:00Z&publishDateTimeTo=2026-09-17T00:00:00Z&page=1"
      - dataset: tsdf
        differs: "Transmission demand at `N` plus other boundary codes; one vintage per publish day"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/TSDF?publishDateTimeFrom=2026-09-16T00:00:00Z&publishDateTimeTo=2026-09-17T00:00:00Z&page=1"
      - dataset: tsdfd
        differs: "One transmission figure per date, 2 to 14 days ahead; no settlement period"
        request: "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/TSDFD?publishDateTimeFrom=2026-09-16T00:00:00Z&publishDateTimeTo=2026-09-17T00:00:00Z&page=1"
---

# Elexon - National Demand Forecast (Day-Ahead) (`NDF`)

## Overview

National Demand Forecast (day-ahead) — the published GB electricity demand forecast in MW per settlement period, issued for the next-day delivery horizon. NDF is the headline GB demand forecast and a primary load-forecasting benchmark.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/NDF` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Day-ahead publication. |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `publishDateTimeFrom` | string | No | As per Elexon Swagger spec for ndf. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | As per Elexon Swagger spec for ndf. | `2026-05-06T03:00Z` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/NDF?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-ndf.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/ndf/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/NDF?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "NDF",
      "demand": 21200,
      "publishTime": "2026-05-06T02:47:00Z",
      "startTime": "2026-05-06T03:00:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 9,
      "boundary": "N"
    },
    {
      "dataset": "NDF",
      "demand": 21177,
      "publishTime": "2026-05-06T02:47:00Z",
      "startTime": "2026-05-06T03:30:00Z",
      "settlementDate": "2026-05-06",
      "settlementPeriod": 10,
      "boundary": "N"
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/ndf/year=YYYY/month=MM/ndf_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.elexon.demand_forecast.DemandForecastTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonDemandForecast`
**Dedup key**: `(settlement_date, settlement_period, forecast_type, published_at)` (`silver/elexon/demand_forecast.py:150-153`)
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | No | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Derived from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `forecast_type` | `str` | No | _derived_ | `day_ahead` (NDF) or `2_14_day` (NDFD). |
| `national_demand_mw` | `float` | No | `nationalDemand` or `demand` | MW. |
| `transmission_demand_mw` | `float` | Yes | `transmissionSystemDemand` | MW. **Not populated by the live NDF feed** — the live response carries no `transmissionSystemDemand` field (only `demand` + `boundary`), so this column is absent from NDF silver: the transformer keeps only the output columns present (`demand_forecast.py:110-111,174`). The transformer maps it only when an endpoint surfaces `transmissionSystemDemand`. |
| `published_at` | `datetime` | Yes | `publishTime` | Publication time of the forecast (Canonical: ElexonDemandForecast.published_at). |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran: stamped `datetime.now(UTC)` by the transformer (`demand_forecast.py:155-160`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-06",
        "settlement_period": 9,
        "timestamp_utc": "2026-05-06T03:00:00+00:00",
        "forecast_type": "day_ahead",
        "national_demand_mw": 21200,
        "published_at": "2026-05-06T02:47:00+00:00",
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

- **Forecast revisions**: silver dedup is `(settlement_date, settlement_period, forecast_type, published_at)` — note the vintage field is **`published_at`**, not `issue_time` (no such column exists in the silver schema; the earlier wording was wrong). Because `published_at` is *in* the key, **the full vintage history survives into silver** — NDF is the dataset to use for forecast-evolution work. Live-verified 2026-07-31: NDF is republished roughly every 30 minutes (publish times at ~:17 and ~:47), and a single target settlement period accumulates a vintage from every publish that covers it as the delivery horizon shortens. Those publishes fall on up to three publish days (next point), so a count taken from one 24-hour publish window understates it. Contrast [tsdf.md](./tsdf.md), which drops vintages.
- **Bronze/silver daily files are bucketed by publish day, not settlement day.** NDF is a `PUBLISH_DATETIME` endpoint forecasting *ahead*, so a single publish day's file covers several target settlement dates — a 2026-07-29 publish window returned target `settlementDate` values of 29, 30 **and** 31 July. To assemble all vintages for one delivery day, read across the full glob and filter on the `settlement_date` **column**, never on the filename; and backfill publish days from roughly `target_date - 2` onward. Same trap as [agws.md](./agws.md).
- **Pairs with INDO, not ITSDO.** `national_demand_mw` is the *national* demand forecast and matches INDO's scale — live-verified 2026-07-31: NDF 22,810 MW vs INDO outturn 23,003 MW for 2026-07-30 SP 3 (0.8% apart). Do not benchmark NDF against ITSDO, which runs ~2,375 MW higher (see [itsdo.md](./itsdo.md)). The `transmission_demand_mw` column is absent from NDF silver (`demand_forecast.py:174` keeps only columns present).

---

## Implementation delta

- **Shared transformer** `DemandForecastTransformer` handles both NDF and NDFD; the registered transformer for `ndf` and `ndfd` distinguishes via `forecast_type` field. Pydantic schema `ElexonDemandForecast` is shared.

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/demand_forecast.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
