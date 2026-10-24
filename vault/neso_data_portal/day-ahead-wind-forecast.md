---
source: "neso_data_portal"
package: "day-ahead-wind-forecast"
dataset_keys: ["da_wind_forecast_day_ahead", "da_wind_forecast_day_ahead_bmu", "da_wind_forecast_historic_day_ahead", "da_wind_forecast_historic_day_ahead_bmu"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Day-ahead wind forecast
  summary: >-
    NESO's forecast of GB metered wind output for each half-hour of the next day, in MW, nationally
    and per wind BM unit.
  facts:
    vendor: "NESO Data Portal, package `day-ahead-wind-forecast`: 11 CSV files"
    cadence: "Daily; NESO states 09:00 to 09:15 clock time, which file stamps do not match"
    grain: "One row per settlement period; in the BMU file, per period and BM unit"
    history: NESO describes its archives as all day-ahead forecasts from 2018
  landscape: power
  what_it_is: >-
    NESO's day-ahead forecast of metered wind output, in MW, for each half-hour of the next UK day,
    beside operational wind capacity on the transmission network. The BMU file splits the day by wind BM unit, the farms
    behind the national forecast. In NESO's 8 and 16 October 2026 files the units sum
    to the national figure, to the nearest MW.
  how_used:
    - Benchmark a day-ahead wind model against NESO's half-hourly forecast
    - Set beside Elexon's wind forecast and wind outturn for the same periods
    - Attach a day-ahead forecast to individual wind BM units, by unit name
  chart:
    type: line
    silver: neso_data_portal/da_wind_forecast_day_ahead
    time: timestamp_utc
    value: incentive_forecast
    filter:
      - {column: date, op: eq, value: "2026-10-17"}
    dedup: {"on": [datetime_gmt], order_by: published_at}
    aggregation: last
    window: {start: "2026-10-16", end: "2026-10-17"}
    unit: MW
  chart_view:
    title: Forecast wind output, 17 October 2026
    caption: >-
      Silver `da_wind_forecast_day_ahead`, MW: NESO's national forecast for the 48 settlement periods
      of 17 October 2026, which start at 23:00 UTC on the 16th (BST), in the file stamped 08:40 on 16
      October, read as UTC. The axis starts at zero.
    alt: >-
      Line chart from neso_data_portal/da_wind_forecast_day_ahead: NESO's forecast wind output in MW
      for each settlement period of 17 October 2026, from 23:00 UTC on the 16th to 22:30 UTC on the
      17th, on an axis from zero. It starts at the day's highest, 11,425, falls to 10,119 at 05:30,
      edges up to 10,214 at 07:30, falls to 9,479 at 15:00, rises to 9,619 at 18:00 and ends at the
      lowest, 8,966.
    x_label: settlement period start, UTC
    y_min: 0
    key:
      - {series: incentive_forecast, label: Forecast wind output, codes: Incentive_forecast, paint: horizon,
         note: "Out of 25,501 MW of operational wind capacity, the `capacity` column below"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each current or archive file downloaded whole
      unless unchanged; the yearly unit archives are datastore dumps. Dates select nothing.
    commands:
      - {run: gridflow ingest neso_data_portal da_wind_forecast_day_ahead --last 24h,
         comment: whole file; window must end recently}
      - {run: gridflow transform neso_data_portal da_wind_forecast_day_ahead --last 24h,
         comment: the capture's date to silver}
      - {run: gridflow pipeline neso_data_portal da_wind_forecast_day_ahead_bmu --last 24h,
         comment: "the unit file: bronze, then silver"}
  record:
    select:
      filter:
        - {column: date, op: eq, value: "2026-10-17"}
        - {column: settlement_period, op: le, value: 8}
      dedup: {"on": [datetime_gmt], order_by: published_at}
      order_by: [settlement_period]
      columns: [datetime_gmt, date, settlement_period, incentive_forecast, capacity, published_at]
    key: [datetime_gmt, published_at]
    caption: "Periods 1 to 8 of 17 October 2026: in BST the day starts 23:00 UTC."
    fields:
      datetime_gmt: "Start of the settlement period; NESO's dictionary gives UTC despite the name"
      date: The UK settlement date the period belongs to
      settlement_period: "Half-hour of the settlement day; NESO says period 1 ends 00:30 UK time"
      incentive_forecast: "Forecast wind output for the half-hour, MW; NESO calls it the incentive forecast"
      capacity: "Operational wind capacity on the transmission network, MW; the same in every row"
      published_at: "NESO's last-modified time for the file, read as UTC; rows carry no issue time"
      timestamp_utc: "Equals `datetime_gmt`: the period start, UTC"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `tail()` reads each table's `_latest` view (the newest capture, latest periods first), lineage
      columns dropped. Times arrive in the session zone, so the cells convert them to UTC; the second
      sums the units per period.
    cells:
      - |
        nat = data.neso_data_portal.tail("da_wind_forecast_day_ahead")
        for c in ["timestamp_utc", "published_at"]:
            nat[c] = nat[c].dt.tz_convert("UTC")
        nat = nat.sort_values("timestamp_utc", ignore_index=True)
        nat[["timestamp_utc", "date", "settlement_period", "incentive_forecast", "capacity",
             "published_at"]].head()
      - |
        bmu = data.neso_data_portal.tail("da_wind_forecast_day_ahead_bmu", 20_000)
        bmu["timestamp_utc"] = bmu["timestamp_utc"].dt.tz_convert("UTC")
        units = bmu.groupby("timestamp_utc").agg(units=("generator_name", "nunique"),
                                                 unit_sum=("wind_forecast", "sum"))
        check = nat.set_index("timestamp_utc").join(units)
        print("units per period:", sorted(check.units.unique().tolist()))
        print("largest national minus unit sum, MW:",
              round((check.incentive_forecast - check.unit_sum).abs().max(), 3))
      - |
        top = nat.incentive_forecast.max() * 1.1
        ax = nat.plot(x="timestamp_utc", y="incentive_forecast", ylim=(0, top), legend=False,
                      color="#3E8C97", figsize=(8, 3.5), xlabel="settlement period start, UTC",
                      ylabel="forecast wind output, MW");
    needs: a recent capture of NESO's national and BMU day-ahead wind files
    plot_alt: >-
      Line plot of NESO's forecast wind output in MW for the 48 settlement periods of 17 October 2026,
      from 23:00 UTC on the 16th, on an axis from zero: 11,425 at the start, falling to 8,966 at
      22:30 UTC, with small rises around 07:30 and 18:00.
  related:
    - {dataset: elexon/windfor, note: "Elexon's wind generation forecast, issued several times a day"}
    - {dataset: neso_data_portal/embedded_wind_solar_forecast, note: "NESO's embedded wind forecast, outside this transmission-connected one"}
    - {dataset: neso_data_portal/14-days-ahead-operational-metered-wind-forecasts, note: "NESO's metered wind forecast out to 14 days, also per farm"}
    - {dataset: neso_data_portal/daily_wind_availability, note: "Availability per wind BM unit, beside these per-unit forecasts"}
  family:
    slug: day-ahead-wind-forecast
    members:
      - {dataset: da_wind_forecast_day_ahead,
         differs: "The next UK day's half-hours: national forecast and operational wind capacity",
         request: "GET https://api.neso.energy/dataset/fbe3701d-1487-443e-abe9-47a6c01ecce2/resource/b2f03146-f05d-4824-a663-3a4f36090c71/download/b2f03146-f05d-4824-a663-3a4f36090c71-20261016084006.csv"}
      - {dataset: da_wind_forecast_day_ahead_bmu,
         differs: "The same day per wind BM unit, with unit name, region and capacity",
         request: "GET https://api.neso.energy/dataset/fbe3701d-1487-443e-abe9-47a6c01ecce2/resource/90e581e9-2d7f-4eaa-8fe0-6e323ee0f5f7/download/da_windunit_forecast_20261016083509.csv"}
      - {dataset: da_wind_forecast_historic_day_ahead,
         differs: "The national forecasts NESO has kept since 2018, each with a forecast time stamp",
         request: "GET https://api.neso.energy/dataset/fbe3701d-1487-443e-abe9-47a6c01ecce2/resource/7524ec65-f782-4258-aaf8-5b926c17b966/download/7524ec65-f782-4258-aaf8-5b926c17b966-20261016084502.csv",
         held: "Forecast time stamps carry no zone, and many fall at or after the period they forecast."}
      - {dataset: da_wind_forecast_historic_day_ahead_bmu,
         differs: "Per BM unit, in eight files labelled 2018 to 2025; first and last shown",
         request: ["GET https://api.neso.energy/datastore/dump/9c26224d-ba6f-4fff-a21f-6f0090d8ac7d",
                   "GET https://api.neso.energy/datastore/dump/81413643-508e-4358-8414-c87e7c4bcc43"],
         held: "NESO gives each forecast's UK publication time, but nothing shows the values unchanged since."}
---

# Day Ahead Wind Forecast

NESO's **day-ahead wind generation forecast** for GB, published on the Open Data Portal as
eleven CSV resources. The package notes say it holds "national and BMU wind forecast over a day
ahead timescale as well as all historic day ahead wind forecasts". There are two current files
and two archives:

- The **national** file is one half-hourly forecast for the next UK day (48 settlement periods
  in each of the 2026-10-08 and 2026-10-16 captures), with the total operational wind capacity
  beside it. The resource
  description calls it "the NESO's day ahead operational metered wind forecast", in MW.
- The **BMU** file breaks the same day into one forecast per wind Balancing Mechanism unit. The
  vendor says these are the windfarms used to build the national forecast. It is not a complete
  list of BM units, and it excludes licence-exempt windfarms. In both captures (2026-10-08 and
  2026-10-16) the unit `Wind_Forecast` values summed per period equal the national
  `Incentive_forecast` to the nearest MW (largest gap 0.497 MW over 96 periods), and the unit
  capacities sum to the national `Capacity` (25,365.8 against 25,366; 25,500.8 against 25,501).
- The **historic national** file is, in NESO's words, "all historic day ahead wind forecasts from
  2018 to the most recent forecast", with a forecast timestamp per row.
- The **historic BMU** archive is eight datastore resources, labelled 2018 to 2025, each with a
  publication timestamp per row.

Use the current files as a day-ahead wind benchmark against Elexon's WINDFOR
(@../../elexon/datasets/windfor.md), and the BMU file to attach a NESO forecast to individual
wind BM units (@../../../20-domain/concepts/bm-units.md). Settlement periods are explained in
@../../../20-domain/concepts/settlement-period.md. Only the two **current** families are eligible
for publication. Both archives are in silver but **held**, because neither has an established
clock for when each archived value was available (see Holds). Catalogue page:
[Day Ahead Wind Forecast](https://www.neso.energy/data-portal/day-ahead-wind-forecast).

- Publisher group: Generation
- Registry group: generation · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Day Ahead Wind BMU Forecast | CSV | upload | `90e581e9-2d7f-4eaa-8fe0-6e323ee0f5f7` |
| Day Ahead Wind Forecast | CSV | upload | `b2f03146-f05d-4824-a663-3a4f36090c71` |
| Historic Day Ahead Wind BMU Forecasts 2018 | CSV | dump | `9c26224d-ba6f-4fff-a21f-6f0090d8ac7d` |
| Historic Day Ahead Wind BMU Forecasts 2019 | CSV | dump | `11bc4219-0524-468d-8378-bba06c6114c4` |
| Historic Day Ahead Wind BMU Forecasts 2020 | CSV | dump | `ae7cd368-7fcf-47ab-a835-27a6ee7a679e` |
| Historic Day Ahead Wind BMU Forecasts 2021 | CSV | dump | `53587966-5b79-4a8c-8029-efe1c3d13601` |
| Historic Day Ahead Wind BMU Forecasts 2022 | CSV | dump | `411cfef3-2297-49b0-8426-476d913ba310` |
| Historic Day Ahead Wind BMU Forecasts 2023 | CSV | dump | `b8a784ac-f6fe-4f93-a965-ce6a32df0963` |
| Historic Day Ahead Wind BMU Forecasts 2024 | CSV | dump | `22625e0b-f63b-4d0e-9bbd-54383fc3e931` |
| Historic Day Ahead Wind BMU Forecasts 2025 | CSV | dump | `81413643-508e-4358-8414-c87e7c4bcc43` |
| Historic Day Ahead Wind Forecasts | CSV | upload | `7524ec65-f782-4258-aaf8-5b926c17b966` |

Every resource has disposition **SILVER**. Each maps to exactly one family:

| Resource | Family | Silver eligibility |
|---|---|---|
| Day Ahead Wind Forecast | `da_wind_forecast_day_ahead` | eligible |
| Day Ahead Wind BMU Forecast | `da_wind_forecast_day_ahead_bmu` | eligible |
| Historic Day Ahead Wind Forecasts | `da_wind_forecast_historic_day_ahead` | held (E-SEM) |
| Historic Day Ahead Wind BMU Forecasts 2018–2025 (8) | `da_wind_forecast_historic_day_ahead_bmu` | held (E-SEM) |

Downloads (upload URLs as captured on 2026-10-08; NESO renames the upload file on each
publication, so a dated link goes stale after the next upload, and the catalogue page above
always lists the current one):

- Day Ahead Wind Forecast:
  [b2f03146-…-20261008084006.csv](https://api.neso.energy/dataset/fbe3701d-1487-443e-abe9-47a6c01ecce2/resource/b2f03146-f05d-4824-a663-3a4f36090c71/download/b2f03146-f05d-4824-a663-3a4f36090c71-20261008084006.csv)
  (CKAN `last_modified` 2026-10-08T08:40:07.850057).
- Day Ahead Wind BMU Forecast:
  [da_windunit_forecast_20261008083510.csv](https://api.neso.energy/dataset/fbe3701d-1487-443e-abe9-47a6c01ecce2/resource/90e581e9-2d7f-4eaa-8fe0-6e323ee0f5f7/download/da_windunit_forecast_20261008083510.csv)
  (CKAN `last_modified` 2026-10-08T08:35:11.947478).
- Historic Day Ahead Wind Forecasts:
  [7524ec65-…-20261008084501.csv](https://api.neso.energy/dataset/fbe3701d-1487-443e-abe9-47a6c01ecce2/resource/7524ec65-f782-4258-aaf8-5b926c17b966/download/7524ec65-f782-4258-aaf8-5b926c17b966-20261008084501.csv)
  (CKAN `last_modified` 2026-10-08T08:45:11.458782).
- Historic BMU archive (datastore dumps; the URL is stable):
  [2018](https://api.neso.energy/datastore/dump/9c26224d-ba6f-4fff-a21f-6f0090d8ac7d) ·
  [2019](https://api.neso.energy/datastore/dump/11bc4219-0524-468d-8378-bba06c6114c4) ·
  [2020](https://api.neso.energy/datastore/dump/ae7cd368-7fcf-47ab-a835-27a6ee7a679e) ·
  [2021](https://api.neso.energy/datastore/dump/53587966-5b79-4a8c-8029-efe1c3d13601) ·
  [2022](https://api.neso.energy/datastore/dump/411cfef3-2297-49b0-8426-476d913ba310) ·
  [2023](https://api.neso.energy/datastore/dump/b8a784ac-f6fe-4f93-a965-ce6a32df0963) ·
  [2024](https://api.neso.energy/datastore/dump/22625e0b-f63b-4d0e-9bbd-54383fc3e931) ·
  [2025](https://api.neso.energy/datastore/dump/81413643-508e-4358-8414-c87e7c4bcc43).
  The dumps have no CKAN `last_modified` (blank in every sidecar).
- The 2026-10-16 captures fetched `b2f03146-…-20261016084006.csv` (CKAN `last_modified`
  2026-10-16T08:40:07.867477), `da_windunit_forecast_20261016083509.csv` (08:35:11.316089) and
  `7524ec65-…-20261016084502.csv` (08:45:08.186884).

Captures on 2026-10-08, one per resource (gridflow
`@.planning/phases/v0.22-K-GEN-1/K-GEN-1-FACTS.md` §1):

| Family | Body | Bytes | Data rows |
|---|---|---:|---:|
| `da_wind_forecast_day_ahead` | `raw_20261008T091712Z_b2f03146-…_57d1e568.csv` | 2,263 | 48 |
| `da_wind_forecast_day_ahead_bmu` | `raw_20261008T091716Z_90e581e9-…_13bdee1b.csv` | 1,012,023 | 11,088 |
| `da_wind_forecast_historic_day_ahead` | `raw_20261008T091720Z_7524ec65-…_0e7ab229.csv` | 9,672,511 | 148,825 |
| `da_wind_forecast_historic_day_ahead_bmu` | 8 dump bodies (per-resource table in that family) | 2,400,858,694 | 21,906,814 |

Recaptures on 2026-10-16 (bronze and silver row counts agree; for the other seven BMU dumps the
ingest log reports "7 unchanged since newest capture", the connector's identical-body skip;
gridflow `@.planning/phases/v0.22-close/refresh-20261016/ingest.log`):

| Family | Body | Bytes | Data rows | Against 2026-10-08 |
|---|---|---:|---:|---|
| `da_wind_forecast_day_ahead` | `raw_20261016T192201Z_b2f03146-…_b8940f74.csv` | 2,236 | 48 | next target day (2026-10-17); no row repeats |
| `da_wind_forecast_day_ahead_bmu` | `raw_20261016T192207Z_90e581e9-…_098114f3.csv` | 1,014,033 | 11,088 | same 231 generators, target 2026-10-17; no row repeats |
| `da_wind_forecast_historic_day_ahead` | `raw_20261016T192211Z_7524ec65-…_b4a0929f.csv` | 9,697,699 | 149,209 | all 148,825 earlier rows unchanged; 384 added |
| `da_wind_forecast_historic_day_ahead_bmu` (2025) | `raw_20261016T193728Z_81413643-…_09e13458.csv` | 405,732,852 | 3,683,474 | all 3,136,000 earlier rows unchanged; 547,474 added (see that family) |

The package has **no DOC resources** and no `_files` family (FACTS GEN1-4). There is no vendor
documentation file to download. The vendor sources are the package notes, the resource
descriptions and the CKAN field dictionaries, read 2026-10-08 (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/`). The historic dictionaries
are also on the portal:
[historic national](https://www.neso.energy/data-portal/day-ahead-wind-forecast/historic_day_ahead_wind_forecasts),
[historic BMU (2023)](https://www.neso.energy/data-portal/day-ahead-wind-forecast/historic_day_ahead_wind_bmu_forecasts_2023).

## Families

### `da_wind_forecast_day_ahead`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Datetime_GMT | `datetime_gmt` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC ISO 8601 |
| Date | `date` | date | `%Y-%m-%d` | yes | — | — |
| Settlement_period | `settlement_period` | int64 | — | yes | — | — |
| Capacity | `capacity` | float64 | — | yes | — | MW |
| Incentive_forecast | `incentive_forecast` | float64 | — | yes | — | MW |

- Entity key: `datetime_gmt`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`datetime_gmt`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the captured file: `2026-10-08T08:40:07.850057` for the 2026-10-08
   capture and `2026-10-16T08:40:07.867477` for the 2026-10-16 one.
   CKAN emits it without an offset, and gridflow reads it as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Each capture's 48 rows share
   its own vintage. The
   file has no issue column, so the issue recipe is `none`. The date-time token in the upload
   filename is not a documented issue instant and is not used as one (FACTS §2).
2. **Event time (`utc_instant` on `datetime_gmt`).** `timestamp_utc` = `event_time` =
   `datetime_gmt`, the UTC **start** of the target settlement period. Checked on every silver
   row on 2026-10-09. The column is named "GMT" and the body carries no `Z`, but the dictionary
   unit is "UTC ISO 8601". Every measured timestamp equals UK settlement-day start plus
   `30 × (SP − 1)` minutes, including on a BST day (FACTS T01, g1). The 2026-10-08 capture covers
   UK settlement date 2026-10-09, SP 1–48: 2026-10-08T23:00Z to 2026-10-09T22:30Z. The
   2026-10-16 capture covers 2026-10-17, SP 1–48: 2026-10-16T23:00Z to 2026-10-17T22:30Z, with
   `timestamp_utc` equal to `datetime_gmt` on all 48 rows (silver, 2026-10-24).

**Why this family is eligible (forward-target rule, RULINGS 529, applied by RULINGS 542).**
Every target in the capture starts after the file's vintage. The earliest target is
2026-10-08T23:00Z; the vintage is 2026-10-08T08:40Z. So the CKAN vintage is a safe
availability clock for every row: no value can be read as available before it existed. A test
pins this property on the fixture. It holds for the 2026-10-08 capture and for the 2026-10-16
one (earliest target 2026-10-16T23:00Z, vintage 2026-10-16T08:40Z); later captures are not
guaranteed to satisfy it (FACTS GEN1-1).

**Units (vendor dictionary only).** `Capacity` and `Incentive_forecast` are **MW**, declared in
the dictionary (FACTS g4). `Settlement_period` is an index with no physical unit. `Date` is the
UK settlement date that pairs with the SP. It is not itself a UTC instant. The current
dictionary leaves the `Incentive_forecast` description blank. The historic dictionary describes
the same column as the "Wind incentive forecast for day ahead produced for each half hourly
settlement period". `TODO: verify` what "incentive" means here, for example whether it names
the forecast submitted under a NESO forecasting incentive scheme. The vendor does not say.

**Sentinels and missing values (FACTS g5).** No null token is declared. The 2026-10-08 capture
has no blank, `N/A`, `NA` or `-1` cells, and no value numerically equal to −1. In silver, no
column is null in either capture, and neither `capacity` nor `incentive_forecast` has a zero or
a negative value (checked 2026-10-09; 2026-10-16 capture checked 2026-10-24). No bounds are
imposed.

**Identity and selection.** `datetime_gmt` is unique in each capture: 48 rows, 48 targets (FACTS
T04; 2026-10-16 checked in silver). The two captures share no target. That is a measured guard, not a vendor-stated key (`TODO: verify` contractual key).
`_latest` is `whole_capture`: each new capture replaces the forecast as a whole.

**Elexon cross-check.** The local WINDFOR store (target times 2021-09-01T20:00Z to
2026-09-28T20:00Z) has no overlap with this capture, so no value comparison exists yet (FACTS §5,
C10).

**Activation (2026-10-09, master `f19effb`, PR #92).** Transformed at cutoff 2026-10-08:
**48 silver rows**, equal to the planned count, with no prior silver overwritten. Reconcile
`--all` at that cutoff found 0 gaps over 55 families, overlap 0 (gridflow
`@.planning/v0.22-RESULTS.md` §GEN-1; RULINGS 545 merge, 546 activation). After the 2026-10-16
recapture the base table holds 96 rows and `_latest` the newer 48.

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1`). Silver lives at
`C:/gridflow-data/silver/neso_data_portal/da_wind_forecast_day_ahead/`.

### `da_wind_forecast_day_ahead_bmu`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Datetime | `datetime` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC ISO 8601 |
| Date | `date` | date | `%Y-%m-%d` | yes | — | — |
| Settlement_Period | `settlement_period` | int64 | — | yes | — | — |
| Generator_Name | `generator_name` | string | — | yes | — | — |
| Generator_Full_Name | `generator_full_name` | string | — | yes | — | — |
| Region | `region` | string | — | yes | — | — |
| Capacity | `capacity` | float64 | — | yes | — | MW |
| Wind_Forecast | `wind_forecast` | float64 | — | yes | — | MW |

- Entity key: `datetime`, `generator_name`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` =
   `2026-10-08T08:35:11.947478` for the 2026-10-08 capture and `2026-10-16T08:35:11.316089` for
   the 2026-10-16 one, the CKAN `last_modified` read as UTC (ADR-030). Every row of a capture
   shares its vintage. No issue column exists, so the issue recipe is `none`.
2. **Event time (`utc_instant` on `datetime`).** `timestamp_utc` = `event_time` = `datetime`,
   the UTC start of the target settlement period (FACTS T01, g1; checked on every silver row
   2026-10-09, and on the 2026-10-16 capture 2026-10-24). The 2026-10-08 capture covers UK
   settlement date 2026-10-09, SP 1–48, 2026-10-08T23:00Z to 2026-10-09T22:30Z; the 2026-10-16
   capture covers 2026-10-17, 2026-10-16T23:00Z to 2026-10-17T22:30Z.

**Why this family is eligible (RULINGS 529/542).** Every target starts after the vintage
(earliest target 2026-10-08T23:00Z against vintage 08:35Z; on 2026-10-16, 23:00Z against
08:35Z), so the vintage is a safe availability clock for every row (FACTS GEN1-1). A fixture
test pins the property.

**Units (vendor dictionary only).** `Capacity` and `Wind_Forecast` are **MW** (FACTS g4).
`Generator_Name`, `Generator_Full_Name` and `Region` are text dimensions. The vendor
defines the regions as the ITL 1 regions for England plus the DNO licence areas for Wales and
Scotland, extended to national borders. Offshore regions use the IHO sea areas, split by the land
area their mainland connection is in. Each capture has the same 231 generators and 10 distinct
regions, with no blank region.

**Relation to the national file (measured, not vendor-stated).** NESO says the BMU file covers
the windfarms used to produce the national forecast. In both captures the per-period sum of
`wind_forecast` over the 231 generators equals the national `incentive_forecast` for the same
period to within 0.497 MW (96 periods; the national figure is whole MW), and the sum of unit
`capacity` is 25,365.8 MW against the national 25,366 (2026-10-08) and 25,500.8 against 25,501
(2026-10-16). Silver, 2026-10-24.

**Sentinels and missing values (FACTS g5).** No null token is declared, and none of `N/A`, `NA`,
`-1` or blank occurs. Zeros are real values and are kept. The 2026-10-08 capture has 144 zero
`capacity` cells (three generators across all 48 periods) and 320 zero `wind_forecast` cells,
176 of them beside a positive capacity; the 2026-10-16 capture has 96 zero `capacity` cells (two
generators) and 288 zero `wind_forecast` cells, 192 beside a positive capacity. The longest zero
run is the whole 48-period day for both columns (FACTS g5; silver checked 2026-10-09 and
2026-10-24). No negative values occur in either capture. `TODO: verify` whether a
zero capacity means "not operational" or "not reported". No vendor source says, so zeros are not
converted to nulls.

**Identity and selection.** `(datetime, generator_name)` is unique in each capture: 11,088 rows =
231 generators × 48 periods (FACTS T04; 2026-10-16 checked in silver). It is a measured guard, not a vendor key
(`TODO: verify` contractual key). `_latest` is `whole_capture`. A generator missing from a newer
capture is not carried forward from an older one.

**Generator names are BM unit IDs, kept as delivered.** All 231 distinct names match the local
Elexon reference's `national_grid_bm_unit` exactly, and none matches `bm_unit_id` (FACTS §5,
C05). Join to Elexon on `national_grid_bm_unit`
(@../../elexon/datasets/bmunits_reference.md). Names are stored byte-identical, with no prefix,
case or alias changes.

**Activation (2026-10-09, master `f19effb`, PR #92).** **11,088 silver rows** at cutoff
2026-10-08, equal to the planned count, nothing overwritten; reconcile 0 gaps (RULINGS 546).
After the 2026-10-16 recapture the base table holds 22,176 rows and `_latest` the newer 11,088.
Silver carries the same eight lineage/clock columns as the national family, at
`C:/gridflow-data/silver/neso_data_portal/da_wind_forecast_day_ahead_bmu/`.

### `da_wind_forecast_historic_day_ahead`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Datetime_GMT | `datetime_gmt` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| Date | `date` | date | `%Y-%m-%d` | yes | — | — |
| Settlement_period | `settlement_period` | int64 | — | yes | — | — |
| Capacity | `capacity` | float64 | — | yes | — | MW |
| Incentive_forecast | `incentive_forecast` | float64 | — | yes | — | MW |
| Forecast_Timestamp | `forecast_timestamp` | string | — | yes | — | — |

- Entity key: `datetime_gmt`, `forecast_timestamp`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`datetime_gmt`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM).** This family's silver output exists but is not eligible for publication
or point-in-time use. This page gives schema, row counts and structural counts only. It gives
no data values or ranges. See Holds.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the captured archive, `2026-10-08T08:45:11.458782` (offset-less, read as
   UTC per ADR-030); all 148,825 rows of that capture share it. The 2026-10-16 capture's 149,209
   rows share `2026-10-16T08:45:08.186884`. It says when the archive file last changed, not when
   any archived forecast became available. The issue recipe is `none`.
2. **Event time (`utc_instant` on `datetime_gmt`).** `timestamp_utc` = `event_time` =
   `datetime_gmt`, the UTC start of the target period. The dictionary describes the column as
   "in UTC", and every measured offset against UK settlement start is zero (FACTS T01, g1).

**Why `Forecast_Timestamp` is kept as raw text, not an issue clock.** The vendor dictionary
describes it as "the date and time at which the forecast was made", but gives no zone and no
unit. Its example ends in `Z`; the delivered values carry no offset, so the `Z` cannot be
borrowed (FACTS T03). The 2026-10-08 capture holds 3,007 distinct labels; 148,441 targets carry
one label and 192 carry two. About 14,000 target/label rows have a label at or after the start
of the period they forecast, under either a UTC or a Europe/London reading (14,021 and 13,755).
A zone choice alone does not resolve that (FACTS §2, C06). The 2026-10-16 capture holds 3,015
labels, 148,825 one-label targets and the same 192 two-label targets; 14,181 and 13,899 rows
have a label at or after target start (silver, 2026-10-24).

**Recent labels sit on the target day itself (observed).** In the 2026-10-08 capture, 115 of the
118 target days from 13 June to 8 October 2026 (5,520 rows) carry only the label
`<target day>T08:45:00`; the other three carry other or extra labels (for example `14:55`). The
days just before (9 to 12 June) carry `<target day>T09:25:00`, and older labels vary in day and
time. The 2026-10-16 capture adds UK days 9 to 16 October (384 rows, 48 each) in the same form,
123 such days in all. The 9 October values equal, on all 48 periods, the current national file
captured on 2026-10-08 (CKAN `last_modified` 2026-10-08T08:40:07, read as UTC), yet their label
is `2026-10-09T08:45:00`, about a day later and after the target day began under either zone.
Inference, not shown: for these rows the label looks like the time the archive was appended, not
when the forecast was first published. Labels before 13 June follow other patterns. `TODO: verify` the issue zone, whether late
labels are backfill or recovery times, and whether each label dates the availability of the
exact value beside it.

**Units (vendor dictionary only).** `Capacity` and `Incentive_forecast` are **MW** (FACTS g4).
The dictionary gives no unit for `Datetime_GMT`, hence "—" in the schema.

**Sentinels and missing values (FACTS g5).** No null token is declared, and none of `N/A`, `NA`,
`-1` or blank occurs in the body. Values are kept as delivered, with no sentinel conversion and
no bounds.

**Identity and selection.** `datetime_gmt` alone is not unique: the 192 two-label targets give a
duplicate surplus of 192. `(datetime_gmt, forecast_timestamp)` is unique (FACTS T05), and is the
key. `TODO: verify` the vendor's revision identity. `_latest` is `whole_capture`.

**Elexon cross-check (corroboration only).** FACTS §5 joined the archive to every stored WINDFOR
observation at five time shifts (−60 to +60 minutes). Exact matches were sparse at every shift,
and no shift made the two series agree. Different issue vintages could explain this, so it
establishes neither equivalence nor difference. `TODO: verify` with same-publication captures on
both sides.

**Activation (2026-10-09, master `f19effb`).** **148,825 silver rows** at cutoff 2026-10-08,
equal to the planned count, nothing overwritten; reconcile 0 gaps (RULINGS 546). The 2026-10-16
recapture adds 149,209 rows (base table 298,034; `_latest` the newer 149,209). Silver columns:
the six vendor columns plus the same eight lineage/clock columns, at
`C:/gridflow-data/silver/neso_data_portal/da_wind_forecast_historic_day_ahead/`.

### `da_wind_forecast_historic_day_ahead_bmu`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Datetime | `datetime` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC ISO 8601 |
| Date | `date` | date | `%Y-%m-%d` | yes | — | — |
| Settlement_Period | `settlement_period` | int64 | — | yes | — | — |
| Generator_Name | `generator_name` | string | — | yes | — | — |
| Generator_Full_Name | `generator_full_name` | string | — | yes | — | — |
| Region | `region` | string | — | yes | — | — |
| Capacity | `capacity` | float64 | — | yes | — | MW |
| Wind_Forecast | `wind_forecast` | float64 | — | yes | — | MW |
| Timestamp | `timestamp` | datetime | `%Y-%m-%dT%H:%M:%S` | no | Europe/London | ISO 8601 UK Time |

- Entity key: `resource_id`, `datetime`, `generator_name`, `issue_time`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: utc_instant (`datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Held (unit E-SEM).** Silver exists but is not eligible for publication or point-in-time use.
This page gives schema, row counts and structural counts only, with no data values or ranges.
See Holds.

**The two clocks for this family:**

1. **Vintage (`capture_fallback`, not `ckan_last_modified`).** These resources are datastore
   dumps, and a dump has no CKAN `last_modified` (blank in every sidecar). CKAN metadata time is
   not row-publication time, so gridflow does not substitute it. Per ADR-035, a dump's vintage
   is the **gridflow capture time** (gridflow
   `@docs/DECISION_LOG/ADR-035-neso-datastore-dump-leg.md`). So `published_at` is **null** on
   every row, and `available_at` = `capture_written_at`, the sidecar `written_at` of that
   resource's capture (checked on all 21,906,814 rows of the 2026-10-08 captures, 2026-10-09; the
   2026-10-16 recapture of 2025 carries null `published_at` and its own `written_at`,
   2026-10-16T19:37:29.287953). This clock says only when
   gridflow first held the values. It is not when NESO published them.
2. **Event time (`utc_instant` on `datetime`).** `timestamp_utc` = `event_time` = `datetime`,
   the UTC start of the target period. All eight resources agree with the settlement-start
   convention (FACTS T01, g1).

**Issue time.** This is the only family in the package with an issue clock. The record declares
`Timestamp` as the issue column. The BMU dictionary says it is "the datetime at which the
forecast was published", unit "ISO 8601 UK Time". gridflow parses it in `Europe/London` and
converts it to UTC as `issue_time`, with `ambiguous: "raise"`, so a label inside the autumn DST
fold would fail loudly rather than be guessed. No observed label falls in a fold (FACTS T03).
`issue_time` is in the entity key, as the record contract requires. The hold is not about the
zone. It is about whether the archived values are the ones first published at that instant.

Distinct issue labels per resource, one label per target/generator in every resource (FACTS
GEN1-1):

| Resource label | Resource id | Body bytes | Silver rows | Distinct issue labels | Capture `written_at` (UTC) |
|---|---|---:|---:|---:|---|
| 2018 | `9c26224d-ba6f-4fff-a21f-6f0090d8ac7d` | 167,570,749 | 1,535,468 | 259 | 2026-10-08T09:37:43.699148 |
| 2019 | `11bc4219-0524-468d-8378-bba06c6114c4` | 278,036,065 | 2,545,926 | 365 | 2026-10-08T09:43:29.039095 |
| 2020 | `ae7cd368-7fcf-47ab-a835-27a6ee7a679e` | 290,751,177 | 2,654,256 | 366 | 2026-10-08T09:48:09.411820 |
| 2021 | `53587966-5b79-4a8c-8029-efe1c3d13601` | 297,251,386 | 2,719,536 | 365 | 2026-10-08T09:52:53.642805 |
| 2022 | `411cfef3-2297-49b0-8426-476d913ba310` | 303,568,790 | 2,774,160 | 365 | 2026-10-08T09:58:03.249018 |
| 2023 | `b8a784ac-f6fe-4f93-a965-ce6a32df0963` | 328,503,284 | 2,994,880 | 365 | 2026-10-08T10:03:52.141679 |
| 2024 | `22625e0b-f63b-4d0e-9bbd-54383fc3e931` | 389,845,121 | 3,546,588 | 366 | 2026-10-08T09:25:38.824145 |
| 2025 | `81413643-508e-4358-8414-c87e7c4bcc43` | 345,332,122 | 3,136,000 | 311 | 2026-10-08T09:34:53.316402 |
| 2025 (recapture) | `81413643-508e-4358-8414-c87e7c4bcc43` | 405,732,852 | 3,683,474 | 365 | 2026-10-16T19:37:29.287953 |

**The 2026-10-08 capture of 2025 looks cut short (inferred from two captures).** It ends after
exactly 3,136,000 rows, partway
through one settlement period: 38 of the 210 generators at 2025-11-07T22:00Z, against 209 to 211
in every other period. The 2026-10-16 recapture keeps all 3,136,000 earlier rows unchanged,
completes that period, and runs to 2025-12-31T23:30Z (17,520 periods, 365 labels, the last
2025-12-30T09:00 UK time). The other seven resources each run to 23:30Z on 31 December of their
year (2018 from 2018-04-16T23:00Z). So the growth most likely reflects a complete download of
the same resource rather than NESO appending to it; the resource's CKAN `metadata_modified`
(2026-07-20T09:09:48) is the same in both sidecars. gridflow admitted the short body as a
complete capture (no declared length on a dump). Per-resource `_latest` now selects the
2026-10-16 capture for 2025 (ADR-039), so `_latest` holds 22,454,288 rows.

The year in each resource name is a vendor label. It does not prove the resource holds a
complete calendar year (FACTS GEN1-2). There is no 2026 resource. The archive and the current
BMU file share **zero** `(Datetime, Generator_Name)` rows.

**Header.** Every dump has the current BMU header with `Timestamp` appended. The dumps add no
`_id` column (FACTS GEN1-2).

**Units (vendor dictionary only).** `Capacity` and `Wind_Forecast` are **MW** (FACTS g4).
`TODO: verify` that the dictionary read applies to all eight resources. The field-info read used
the 2023 resource only. The other seven share its header exactly.

**Sentinels and missing values (FACTS g5).** No null token is declared, and no `N/A`, `NA`,
`-1` or blank cell occurs in any resource. Zeros (including long zero runs) and negative
forecasts are kept as delivered. Neither is treated as a sentinel, and no nonnegative bound is
imposed, because no vendor source declares a missing-value convention. `TODO: verify` the
meaning of zero runs (FACTS g5).

**Identity and selection.** `(Datetime, Generator_Name)` is unique within every resource body
(FACTS T05). The key adds `resource_id` and `issue_time`. `_latest` is `whole_capture` with
`latest_partition: "resource_id"`. Each resource's newest capture is kept on its own, so a newer
capture of one year never discards another year (gridflow
`@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md`). `TODO: verify` the vendor's key
and revision grain.

**Activation (2026-10-09, master `f19effb`).** **21,906,814 silver rows** over 8 resources at
cutoff 2026-10-08, equal to the planned count, nothing overwritten. The 2026-10-16 recapture of
2025 adds 3,683,474 rows to the base table (25,590,288 over 9 captures). Peak transform memory was
2,596.1 MiB. Reconcile 0 gaps (RULINGS 546). Silver columns: the nine vendor columns plus
`issue_time`, `resource_id`, `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version`
(`1+e1`), at `C:/gridflow-data/silver/neso_data_portal/da_wind_forecast_historic_day_ahead_bmu/`.

## Cadence

- Registry refresh: intraday
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live
- Intraday: captured once per refresh run — sampled, not complete

The national resource description gives the publication as **daily, between 09:00 and 09:15
(clock time)**. The BMU and historic resources state no schedule. The three upload files were
modified together each morning: on 2026-10-06, 2026-10-08 and 2026-10-16 at 08:35–08:45
(CKAN `last_modified`, read as UTC). Read as UTC, 08:40 is 09:40 BST, which is after the stated
window. `TODO: verify` whether the CKAN time is the upload time and the window describes the
forecast run, or whether the window is out of date.

The historic BMU dumps were created on 2026-07-07 (2024, 2025) and 2026-07-22 (2018–2023). Their
CKAN metadata was last modified in July 2026. The 2025 dump recaptured on 2026-10-16 ends at
2025-12-31T23:30Z; its larger size most likely reflects the first capture's truncation, not an
append (see that family). `TODO: verify` whether a 2026 resource will be added, and whether current BMU forecasts
ever migrate into the archive.

Because the files publish daily and gridflow captures intraday, most captures will repeat the
same upload. Each capture is still stored. Two captures per upload resource exist (2026-10-08 and
2026-10-16). Between them the historic national file kept all 148,825 earlier rows unchanged and
added 384 (UK days 9 to 16 October). `TODO: verify` whether it is ever rewritten rather than
appended; two captures cannot show that.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `da_wind_forecast_historic_day_ahead`: held: TODO: Forecast_Timestamp has no vendor zone (its values carry no offset); 192 targets carry two labels and ~14k labels fall at or after target start; the issue zone and when each value was available are undefined (unit E-SEM)
- `da_wind_forecast_historic_day_ahead_bmu`: held: TODO: the vendor dictionary gives Timestamp as a UK-time publication instant, but no source shows the archived values are unchanged since that instant (unit E-SEM)

Both archives are held by RULINGS 542 (seat ruling, PROXY-SOURCED, from K-GEN-1-FACTS). Unit
E-SEM must answer:

1. **Historic national.** The zone of `Forecast_Timestamp`; why some labels fall at or after
   the period they forecast; and whether each label dates the availability of the exact value
   beside it. Until then `Forecast_Timestamp` stays raw text and the issue recipe stays `none`.
2. **Historic BMU.** Independent evidence, such as a vendor revision/backfill policy or
   independently preserved publications, that each value is unchanged since its `Timestamp`.
   Even then, ADR-035's dump-vintage rule would not lift automatically: the capture-time vintage
   stays unless a ruling changes it.

The silver outputs stay on disk. This page publishes no data values from them.

`da_wind_forecast_day_ahead` and `da_wind_forecast_day_ahead_bmu` are **eligible** under the
forward-target rule (RULINGS 529, applied by 542). The package-level `eligibility: eligible` in
the front matter is the package registry entry; holds are per family (gridflow
`@src/gridflow/connectors/neso_data_portal/registry/day-ahead-wind-forecast.json`,
`@docs/neso_data_portal/eligibility.md`).

Related GEN-1 holds: the ordinary 14-day national and BMU wind files
(@14-days-ahead-wind-forecasts.md) are held because their bodies contain targets at or before
the vintage. The 14-day operational metered wind files
(@14-days-ahead-operational-metered-wind-forecasts.md) are eligible.

**Implementation delta (vendor dictionary vs body and record).**

- **Settlement-period wording conflicts across dictionaries.** The current national dictionary
  says SP1 is "the half hour ending 00:30 UK Time". The BMU dictionaries say periods end "at the
  half hour or hour". The historic national dictionary says periods begin "on the hour or the
  half-hour". The timestamps match period **start** in every body (FACTS g1). The record follows
  the measurement. The "ending" wording describes the interval, not the timestamp label.
- **Capacity descriptions look swapped.** The current national dictionary describes `Capacity`
  as the capacity "of the windfarm". The current BMU dictionary describes it as "the total
  operational wind capacity", with example 16891. The historic dictionaries use the expected
  wording (national total; per-generator capacity). `TODO: verify` with NESO. The unit (MW) is
  the same either way.
- **"Anonymised" generator names are not anonymised.** The current BMU dictionary calls
  `Generator_Name` an "Anonymised generator name" (example `WINDFARM_1`). Every captured name is
  a real National Grid BM unit ID (231/231 Elexon matches). The record keeps names as delivered.
- **Historic national dictionary examples carry `Z`; the body does not.** `Datetime_GMT` and
  `Forecast_Timestamp` examples end in `Z`, and the `Date` example is a full date-time. The body
  has offset-less date-times and plain ISO dates. The record parses the body as delivered.
- **Region outage note.** The current BMU resource description warns that, during NESO's move to
  a new forecast system, "Regions" reference data may be lost for a time. The 2026-10-08
  capture has every region populated. `region` is nullable in the record, so a blank-region
  capture would type cleanly.
- **Key columns marked nullable.** `generator_name` (both BMU families) and `forecast_timestamp`
  are entity-key columns but nullable in the record. No captured body has a blank in them, so
  this has had no effect.
