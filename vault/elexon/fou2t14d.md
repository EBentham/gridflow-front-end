---
source: elexon
dataset_key: fou2t14d
vendor: Elexon BMRS
last_verified: 2026-09-17
layer_coverage: bronze, silver
page:
  title: Availability forecast by fuel type
  summary: >-
    Elexon's forward view of generation and interconnector availability, per fuel type, for each
    day 2 to 14 days ahead; every publish kept.
  facts:
    vendor: Elexon BMRS, dataset FOU2T14D
    cadence: Not stated in Elexon's API docs; the charted publishes are an hour apart
    grain: One row per delivery date, fuel-type code and publish time
  landscape: power
  what_it_is: >-
    Elexon's forward view of availability for generation and interconnector capacity, accounting
    for planned outages: what the Grid Code calls Output Usable. Each publish gives one figure per
    fuel-type code per London delivery date, 2 to 14 days ahead, not per half-hour. gridflow keeps
    every publish, keyed on its publish time. The feed sends no unit; gridflow's column says MW.
  how_used:
    - "Forward margin: availability by fuel against the 2 to 14 day demand forecast."
    - Point-in-time features for a price model, from the publish then available.
    - "Revision signals: how a delivery date's availability moved between publishes."
  chart:
    type: line
    silver: elexon/fou2t14d
    time: published_at
    value: output_usable_mw
    filter:
      - {column: settlement_date, op: eq, value: "2026-09-24"}
      - {column: fuel_type, op: in, value: [CCGT, WIND, NUCLEAR]}
    group: fuel_type
    group_map:
      CCGT: gas
      WIND: wind
      NUCLEAR: nuclear
    series_order: [gas, wind, nuclear]
    aggregation: last
    window: {start: "2026-09-19", end: "2026-09-21"}
    unit: MW
  chart_view:
    title: Forecast for 24 September, publish by publish
    caption: >-
      Silver `elexon/fou2t14d`, MW: the availability that each hourly publish, 00:00 UTC on 19
      September to 23:00 on the 21st, gave for delivery date 24 September 2026. Forecasts, not
      outturn; one value per publish, nothing summed.
    alt: >-
      Line chart from elexon/fou2t14d, in MW: the availability each hourly publish from 00:00 UTC
      on 19 September to 23:00 on the 21st gave for delivery date 24 September. Gas (CCGT) stays
      between 21,011 and 21,099 until 21:00 on the 20th, drops to 20,271 to 20,324, then falls in
      three steps, 14:00 to 16:00 on the 21st, to 19,161. Wind moves between 10,524 and 12,504,
      jumping from 10,524 to 12,442 at 10:00 on the 20th, and ends at 11,606. Nuclear steps once,
      from 3,570 to 4,210 at 21:00 on the 20th.
    x_label: publish time, UTC
    key:
      - {series: gas, label: Gas (CCGT), codes: CCGT}
      - {series: wind, label: Wind, codes: WIND}
      - {series: nuclear, label: Nuclear, codes: NUCLEAR, note: "One step here: 3,570 to 4,210 at the 21:00 UTC publish on the 20th."}
  raw_feed:
    note: >-
      From the Elexon Insights API, in 24-hour publish windows that include both ends. `gridflow
      transform` types each day's publishes into silver, one row per delivery date, code and
      publish.
    requests:
      - "GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FOU2T14D?publishDateTimeFrom=2026-09-21T00:00:00Z&publishDateTimeTo=2026-09-22T00:00:00Z&page=1"
    commands:
      - {run: gridflow ingest elexon fou2t14d --start 2026-09-19 --end 2026-09-22, comment: "bronze; the end instant is included"}
      - {run: gridflow transform elexon fou2t14d --start 2026-09-19 --end 2026-09-21, comment: bronze to silver}
  record:
    select:
      filter:
        - {column: settlement_date, op: eq, value: "2026-09-24"}
        - {column: fuel_type, op: eq, value: WIND}
        - {column: published_at, op: ge, value: "2026-09-20T08:00:00Z"}
        - {column: published_at, op: le, value: "2026-09-20T15:00:00Z"}
      order_by: [published_at]
      columns: [output_usable_mw, published_at, settlement_date, fuel_type]
    key: [settlement_date, fuel_type, published_at]
    caption: "Delivery date 24 September, WIND: eight hourly publishes, 08:00 to 15:00 UTC on the 20th."
    fields:
      settlement_date: "Delivery date the forecast is for, from the vendor `forecastDate`, a London date"
      fuel_type: "Elexon fuel-type code; `INT*` are interconnectors, whose zone and name silver drops"
      published_at: "Publish time, from the vendor `publishTime`, UTC"
      output_usable_mw: "Output Usable for the day; no unit sent, MW by gridflow's column name"
      timestamp_utc: "Midnight UTC of the delivery date, set by gridflow; the vendor sends a date"
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB view `silver_elexon_fou2t14d_latest`, which keeps
      only the newest stored publish per delivery date and fuel, filtered on `settlement_date` with
      both ends included. Lineage columns are dropped.
    cells:
      - |
        df = data.elexon.query("fou2t14d", "2026-09-24", "2026-10-06")
        df["published_at"] = df.published_at.dt.tz_convert("UTC")
        df.published_at.unique()
      - df.sort_values(["settlement_date", "fuel_type"])[["settlement_date", "fuel_type", "published_at", "output_usable_mw"]].head()
      - |
        wide = df.pivot(index="settlement_date", columns="fuel_type", values="output_usable_mw")
        wide[["CCGT", "WIND", "NUCLEAR"]].plot(ylabel="MW", figsize=(8, 3.5))
    needs: publishes from 19 September to 00:00 UTC on 22 September 2026
    plot_alt: >-
      Line plot of output_usable_mw by settlement_date, 24 September to 6 October 2026, all from the
      00:00 UTC publish of 22 September. CCGT climbs from 19,214 to 24,826 MW on 1 October, dips to
      23,872, and ends at 24,910. WIND swings from 5,824 on the 25th to 15,891 on the 29th. NUCLEAR
      rises from 4,210 to 5,158.
  related:
    - {dataset: elexon/uou2t14d, note: "The same forward availability, per BM unit instead of per fuel"}
    - {dataset: elexon/fuelhh, note: "Outturn by fuel-type code, to set against a delivery date's forecast"}
    - {dataset: elexon/remit, note: "Unit outage messages, to look for the outage behind a revision"}
    - {dataset: elexon/ndfd, note: "Demand forecast over the same 2 to 14 day horizon"}
---

# Elexon - 2-14 Day Ahead Generation Availability by Fuel (`FOU2T14D`)

## Overview

2-14 day-ahead generation availability aggregated by fuel type (FOU2T14D). Elexon's OpenAPI description: "a forward view of availability (also referred to as Output Usable data under the Grid Code) for generation and interconnector capacity, accounting for planned outages covering 2 days ahead to 14 days ahead; it is aggregated by Fuel Types categories" (Insights.Api `/datasets/FOU2T14D`, local copy of `swagger.json` captured 2026-09-27). Each row is one fuel type's figure for one delivery date (`forecastDate`); the row schema `AvailabilityByFuelTypeDaily` carries no settlement period and no unit. The OpenAPI states no publish schedule; Elexon's 2018 CP1506 assessment report (BSC Panel paper 280/09, 5 July 2018, p5) lists FOU2T14D as received "Every weekday", but silver's `publishTime` values fall on every hour, weekends included (silver observation, 2026-09-29). Used for medium-term margin and capacity-factor projections.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://data.elexon.co.uk/bmrs/api/v1` |
| Path             | `/datasets/FOU2T14D` |
| Method           | GET |
| Auth             | None required for tested endpoints (2026-05-08). Some endpoints accept an `apikey` header (env: `ELEXON_API_KEY`); registration at https://www.elexonportal.co.uk/. |
| Rate limit       | Vendor-published: not stated. Project default 2 req/sec (asyncio.Semaphore); verified safe 2026-05-08. |
| Pagination       | Connector handles via `page=N` query param; stops when `page >= total_pages`. Reference endpoints (`/reference/bmunits/all`) are not paginated. |
| Historical depth | Several years. |
| Publication lag  | Not stated in the OpenAPI; silver holds a publish every hour (see Overview). The request window is closed at both ends: a publish at exactly `publishDateTimeTo` is returned (`partition_window.py:104-111`; 13 of the 14 bronze days on disk 2026-09-29 hold 25 publishes, 00:00 to the next 00:00, and 18 September lacks its 10:00 publish). |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `fuelType` | array | No | As per Elexon Swagger spec for fou2t14d. | `CCGT` |
| `publishDate` | string | No | The publish date for filtering. This must be in the format yyyy-MM-dd. | `2026-05-06` |
| `publishDateTimeFrom` | string | No | As per Elexon Swagger spec for fou2t14d. | `2026-05-06T00:00Z` |
| `publishDateTimeTo` | string | No | As per Elexon Swagger spec for fou2t14d. | `2026-05-06T03:00Z` |
| `biddingZone` | array | No | As per Elexon Swagger spec for fou2t14d. | `GB` |
| `interconnector` | boolean | No | As per Elexon Swagger spec for fou2t14d. | `false` |
| `format` | string | No | Response data format. Use json/xml to include metadata. | `json` |

### Working curl example

```bash
# Replace <ELEXON_API_KEY> with your env var if you choose to send one (Elexon endpoints
# tested 2026-05-08 do NOT require a key; set anyway for vendor courtesy).
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://data.elexon.co.uk/bmrs/api/v1/datasets/FOU2T14D?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json" \
  -o "/tmp/elexon-fou2t14d.json"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/elexon/fou2t14d/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable — never modified after write.
**Granularity**: One file per API call (paginated requests append additional files for the same date partition).

### Bronze sample

Captured live 2026-05-08 from the https://data.elexon.co.uk/bmrs/api/v1/datasets/FOU2T14D?publishDateTimeFrom=2026-05-06T00:00Z&publishDateTimeTo=2026-05-06T03:00Z&format=json:

```json
{
  "data": [
    {
      "dataset": "FOU2T14D",
      "fuelType": "BIOMASS",
      "publishTime": "2026-05-06T03:00:00Z",
      "systemZone": null,
      "forecastDate": "2026-05-08",
      "forecastDateTimezone": "Europe/London",
      "outputUsable": 2931,
      "biddingZone": null,
      "interconnectorName": null,
      "interconnector": false
    },
    {
      "dataset": "FOU2T14D",
      "fuelType": "CCGT",
      "publishTime": "2026-05-06T03:00:00Z",
      "systemZone": null,
      "forecastDate": "2026-05-08",
      "forecastDateTimezone": "Europe/London",
      "outputUsable": 22274,
      "biddingZone": null,
      "interconnectorName": null,
      "interconnector": false
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/elexon/fou2t14d/year=YYYY/month=MM/fou2t14d_YYYYMMDD_run<available_at>.parquet`
**Write mode**: append-only revision-preserving Silver files (`APPEND_ONLY = True`).
**Transformer class**: `gridflow.silver.elexon.fou2t14d.FOU2T14DTransformer`
**Pydantic schema**: `gridflow.schemas.elexon.ElexonFOU2T14D` — validated fail-soft on the full frame at write time (VTA-SCHEMA-01: invalid rows are logged and counted, never dropped).
**Dedup key**: `(settlement_date, fuel_type, published_at)`, plus `settlement_period` when bronze carries it (`silver/elexon/fou2t14d.py:175-179`; `ENTITY_KEY_COLUMNS` at line 59). The `silver_elexon_fou2t14d_latest` view keeps the newest publish per `(settlement_date, fuel_type)` (`latest_views.py:104-107`); gridflow_models `query("fou2t14d", ...)` reads that view.
**Point-in-time field**: `published_at`

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `settlement_date` | `date` | No | `settlementDate` or `forecastDate` | Settlement date (BST/GMT calendar). |
| `settlement_period` | `int` | Yes | `settlementPeriod` | 1..50 (DST: 46 spring, 50 autumn). Written only if bronze carries `settlementPeriod` (`fou2t14d.py:120`); the live `forecastDate` rows do not, so silver has no such column. |
| `timestamp_utc` | `datetime[UTC]` | No | _derived_ | Midnight UTC of `settlement_date` when there is no `settlement_period` (the live shape, `fou2t14d.py:132-139`); otherwise from (settlement_date, settlement_period) via `utils/time.settlement_period_to_utc`. |
| `fuel_type` | `str` | No | `fuelType` | Fuel category (CCGT, COAL, NUCLEAR, WIND, etc.). |
| `output_usable_mw` | `float` | No | `outputUsable` | MW. |
| `published_at` | `datetime[UTC]` | Yes | `publishTime` | Publication time / document vintage; bitemporal point-in-time field. |
| `data_provider` | `str` | No | _derived_ | Default `"elexon"`. |
| `ingested_at` | `datetime[UTC]` | Yes | _derived_ | When the silver transform ran (`datetime.now`, `fou2t14d.py:181-186`), not the bronze ingest time. |

### Silver sample

```python
[
    {
        "settlement_date": "2026-05-08",
        "timestamp_utc": "2026-05-08T00:00:00+00:00",
        "fuel_type": "BIOMASS",
        "output_usable_mw": 2931,
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

- **Forecast horizon**: data is for delivery dates 2-14 days ahead. The settlement_date in silver is the *future delivery date*, not the publish date.

- **The delivered silver is DAILY grain, and `settlement_period` is not in it** (measured
  2026-09-17 against the whole `elexon/fou2t14d` silver dataset — 5 parquet files, 29,887 rows,
  19 fuel types, one `source_run_id`). The schema table above lists `settlement_period` (1..50,
  nullable) and derives `timestamp_utc` from `(settlement_date, settlement_period)`. In the
  delivered table there is **no `settlement_period` column at all**, and there are **18
  settlement dates with exactly 18 distinct `timestamp_utc` values — one per date, each at 00:00
  UTC**. The page's own sample row is consistent with this (`2026-05-08T00:00:00+00:00`). So a
  consumer gets one usable-MW figure per fuel per *delivery date*, not a half-hourly profile;
  anything that joins this to half-hourly keys is broadcasting a daily constant. Measured against
  this snapshot — it is not a claim about what the API can return.
- **`published_at == available_at` on every row** (29,887 of 29,887), i.e. vendor time, unlike
  `elexon/remit`, whose `available_at` is stamped at ingest (processing time). That is what makes
  a FOU2T14D backfill able in principle to reach historical point-in-time cutoffs where a REMIT
  backfill cannot. **TODO: verify** whether Elexon actually serves historical FOU2T14D
  publications — this snapshot holds publications for 2026-08-01..08-06 only, and nothing
  establishes that the absent 08-07..09-01 ones can still be fetched. *Update 2026-09-29:* a
  fetch made on 2026-09-26 (bronze `2026/09/13/raw_20260926T183343Z_28971c04.json`, request
  `publishDateTimeFrom=2026-09-13T00:00:00Z`) returned all 25 publishes of that window, so
  publishes at least 13 days old were still served then; how far back Elexon serves is unverified.
- **Coverage decays across the horizon, so "N days covered" overstates it.** In the 2026-08-03..
  08-20 delivery range the middle of the window carries ~2,299 rows/day while the last three days
  carry **950 / 494 / 38** rows from **50 / 26 / 2** distinct publications. The tail days are
  nominally covered and substantively almost empty.

---

## Implementation delta

- **`forecastDate → settlement_date` mapping**: API uses `forecastDate` for the future delivery date; silver renames to `settlement_date` to match the canonical schema column.
- **Pydantic schema** `ElexonFOU2T14D` exists in `schemas/elexon.py` and is applied via `BaseSilverTransformer._validate_against_schema` (fail-soft).

---

## Modelling notes

TODO

---

## Links

- [Official API docs (Swagger UI)](https://bmrs.elexon.co.uk/api-documentation)
- [Connector source](../../../../../../Python/gridflow/src/gridflow/connectors/elexon/endpoints.py)
- [Silver transformer](../../../../../../Python/gridflow/src/gridflow/silver/elexon/fou2t14d.py)
- [Pydantic schema](../../../../../../Python/gridflow/src/gridflow/schemas/elexon.py)
- Gold view/builder
- [Domain: GB Balancing Mechanism](../../../20-domain/markets/gb-balancing-mechanism.md)
