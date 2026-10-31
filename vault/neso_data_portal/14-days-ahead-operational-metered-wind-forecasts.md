---
source: "neso_data_portal"
package: "14-days-ahead-operational-metered-wind-forecasts"
dataset_keys: ["metered_wind_forecast_14d", "metered_wind_forecast_14d_windfarm"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: 14-day metered wind forecast
  summary: >-
    NESO's forecast of GB metered wind output for each half-hour out to 14 days ahead, in MW,
    nationally and per wind farm.
  facts:
    vendor: "NESO Data Portal, package `14-days-ahead-operational-metered-wind-forecasts`: 2 CSV files"
    cadence: Daily, NESO says, at no stated time of day
    grain: "One row per half-hour and issue; in the windfarm file, per half-hour and farm"
  landscape: power
  what_it_is: >-
    NESO's forecast of wind output, in MW, for each half-hour out to 14 days ahead, from the wind
    farms that send NESO operational metering (SCADA), beside their total capacity on the
    transmission network. The windfarm file splits it by farm; in NESO's files of 8 and
    16 October 2026 the farms sum to the national figure, to the nearest MW.
  how_used:
    - Add a two-week wind feature to a price or margin model, by half-hour
    - Build regional wind features from the per-farm forecast and its region labels
    - Benchmark a medium-range wind model against NESO's forecast, half-hour by half-hour
  chart:
    type: line
    silver: neso_data_portal/metered_wind_forecast_14d
    time: timestamp_utc
    value: wind_forecast
    filter:
      - {column: issue_time, op: eq, value: "2026-10-16T19:52:23Z"}
    dedup: {"on": [datetime], order_by: published_at}
    aggregation: last
    window: {start: "2026-10-16", end: "2026-10-30"}
    unit: MW
  chart_view:
    title: Forecast wind output, 16 to 30 October 2026
    caption: >-
      Silver `metered_wind_forecast_14d`, MW: one whole issue of NESO's national forecast, produced,
      NESO says, at 19:52 UTC on 16 October 2026, for each half-hour from 20:30 UTC that day to 19:00 UTC on 30 October.
      The axis starts at zero.
    alt: >-
      Line chart from neso_data_portal/metered_wind_forecast_14d: NESO's national wind forecast in MW,
      issued on 16 October 2026, for each half-hour from 20:30 UTC that day to 19:00 UTC on 30
      October, on an axis from zero. It starts at 11,553, falls to the lowest, 7,887, at 10:00 UTC on
      18 October, climbs to a high of 17,573 on 23 October, peaks at 18,240 at 02:00 UTC on
      26 October, then eases to 12,818 at the end.
    x_label: half-hour start, UTC
    y_min: 0
    key:
      - {series: wind_forecast, label: Forecast wind output, codes: Wind_Forecast, paint: horizon,
         note: "Out of 26,860 MW of operational wind capacity, the `capacity` column below"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each file downloaded whole unless its
      last-modified time is unchanged. Dates select nothing; the windfarm file's name changes each issue.
    commands:
      - {run: gridflow ingest neso_data_portal metered_wind_forecast_14d --last 24h,
         comment: whole file; window must end recently}
      - {run: gridflow transform neso_data_portal metered_wind_forecast_14d --last 24h,
         comment: the capture's date to silver}
      - {run: gridflow pipeline neso_data_portal metered_wind_forecast_14d_windfarm --last 24h,
         comment: "the farm file: bronze, then silver"}
  record:
    select:
      filter:
        - {column: issue_time, op: eq, value: "2026-10-16T19:52:23Z"}
        - {column: datetime, op: ge, value: "2026-10-25T21:00:00Z"}
        - {column: datetime, op: le, value: "2026-10-26T00:30:00Z"}
      dedup: {"on": [datetime], order_by: published_at}
      order_by: [datetime]
      columns: [datetime, issue_time, date, settlement_period, wind_forecast, capacity, published_at,
                forecast_datetime]
    key: [datetime, issue_time]
    caption: "Periods 45 to 50 of 25 October, when clocks go back, then 26 October's first two."
    fields:
      datetime: "Start of the half-hour forecast, UTC, as NESO's dictionary gives it"
      issue_time: "Equals `forecast_datetime`; half-hours also forecast in the 8 October issue have two rows"
      date: The UK settlement date the period belongs to
      settlement_period: "Half-hour of the settlement day; NESO says period 1 ends 00:30 UK time"
      wind_forecast: Forecast wind output of the metered farms for the half-hour, MW
      capacity: "Operational wind capacity connected to the transmission network, MW, NESO says"
      published_at: "NESO's last-modified time for the file, read as UTC, here 24 minutes after issue"
      forecast_datetime: "When NESO says it produced the forecast, UTC; the same in every row here"
      timestamp_utc: "Equals `datetime`: the period start, UTC"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `tail()` reads each table's `_latest` view (the newest capture, latest half-hours first), lineage
      columns dropped. Times arrive in the session zone, so the cells convert them to UTC; the second
      sums the farms per half-hour.
    cells:
      - |
        nat = data.neso_data_portal.tail("metered_wind_forecast_14d", 1_000)
        for c in ["timestamp_utc", "issue_time", "published_at"]:
            nat[c] = nat[c].dt.tz_convert("UTC")
        nat = nat.sort_values("timestamp_utc", ignore_index=True)
        cols = ["timestamp_utc", "date", "settlement_period", "wind_forecast",
                "capacity", "issue_time", "published_at"]
        nat[cols].head()
      - |
        farms = data.neso_data_portal.tail("metered_wind_forecast_14d_windfarm", 200_000)
        farms["timestamp_utc"] = farms["timestamp_utc"].dt.tz_convert("UTC")
        per = farms.groupby("timestamp_utc").agg(
            farms=("generator_name", "nunique"), farm_sum=("wind_forecast", "sum"))
        check = nat.set_index("timestamp_utc").join(per)
        print("farms per half-hour:", sorted(check.farms.unique().tolist()))
        print("largest national minus farm sum, MW:",
              round((check.wind_forecast - check.farm_sum).abs().max(), 3))
        print("most periods in one settlement day of this capture:",
              nat.groupby("date").size().max())
      - |
        top = nat.wind_forecast.max() * 1.1
        ax = nat.plot(x="timestamp_utc", y="wind_forecast", ylim=(0, top), legend=False,
                      color="#3E8C97", figsize=(8, 3.5), xlabel="half-hour start, UTC",
                      ylabel="forecast wind output, MW");
    needs: a recent capture of NESO's national and windfarm 14-day metered wind files
    plot_alt: >-
      Line plot of NESO's national wind forecast in MW from the 16 October 2026 issue, each half-hour
      from 20:30 UTC that day to 19:00 UTC on 30 October, on an axis from zero: lowest 7,887 on 18
      October, highest 18,240 on 26 October, ending at 12,818.
  related:
    - {dataset: neso_data_portal/day-ahead-wind-forecast, note: "NESO's next-day wind forecast, nationally and per BM unit"}
    - {dataset: neso_data_portal/monthly-operational-metered-wind-output, note: "NESO's metered wind outturn, to score these forecasts against"}
    - {dataset: neso_data_portal/embedded_wind_solar_forecast, note: "NESO's embedded wind forecast, outside this transmission-connected one"}
    - {dataset: elexon/windfor, note: "Elexon's wind forecast, issued up to eight times a day, to compare"}
  family:
    slug: 14-days-ahead-operational-metered-wind-forecasts
    members:
      - {dataset: metered_wind_forecast_14d,
         differs: "National forecast per half-hour, with total capacity and the forecast's production time",
         request: "GET https://api.neso.energy/dataset/ca6fc361-9099-4ab2-ac02-c959431e84bc/resource/b1ae17c2-cc5e-4254-9bbf-3eddcf30d033/download/14da_wind_forecast_all.csv"}
      - {dataset: metered_wind_forecast_14d_windfarm,
         differs: "The same half-hours per wind farm: name, full name, region, capacity; no issue time",
         request: "GET https://api.neso.energy/dataset/ca6fc361-9099-4ab2-ac02-c959431e84bc/resource/31e6d895-af48-41bd-a4db-28a78c7e9c4b/download/14da_windunit_forecast_20261016_2115.csv"}
---

# 14 Days Ahead Operational Metered Wind Forecasts

NESO's 0–14 day ahead **half-hourly wind generation forecast** for the windfarms that send
real-time operational metering (SCADA telemetry) to NESO. The package has two CSVs. One gives
the **national** total per settlement period. The other gives the same forecast **per
windfarm**, with the farm's short name, full name and region. The vendor says the forecasts are
based on evaluated **Operational Capacity**: a deterministic value derived from each
windfarm's recent actual output, as captured from SCADA telemetry (package description,
2026-10-06 catalogue snapshot). This is a transmission-metered view. Embedded (distribution-
connected) wind is covered by a separate package (@embedded-wind-and-solar-forecasts.md).
Each file covers the next 14 days at half-hour resolution. Each capture runs from the
first settlement period after publication to about 14 days out (670 half-hours in both the
2026-10-08 and 2026-10-16 captures). Use the
national series as a medium-horizon wind feature or benchmark against Elexon WINDFOR
(@../../elexon/datasets/windfor.md), and the windfarm series for regional or unit-level wind
features (@../../../20-domain/modelling/renewable-and-demand-forecasting.md). Each captured
national file holds a single forecast issue, with no archive of earlier issues, and gridflow
keeps only the forecast present at each capture time (issues published between captures are
missed).
Both families are **eligible** under the forward-target rule (RULINGS 529, applied to this
batch by RULINGS 542). Nothing in this package is held.

- Publisher group: Generation
- Registry group: generation · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| 14 Day Ahead Operational Metered Wind Forecast | CSV | upload | `b1ae17c2-cc5e-4254-9bbf-3eddcf30d033` |
| 14 Day Ahead Operational Metered Windfarm-Level Wind Forecast | CSV | upload | `31e6d895-af48-41bd-a4db-28a78c7e9c4b` |

- 14 Day Ahead Operational Metered Wind Forecast → `metered_wind_forecast_14d`.
  Download: [14da_wind_forecast_all.csv](https://api.neso.energy/dataset/ca6fc361-9099-4ab2-ac02-c959431e84bc/resource/b1ae17c2-cc5e-4254-9bbf-3eddcf30d033/download/14da_wind_forecast_all.csv).
  The file name is stable across publications (same in the 2026-10-06 snapshot and the
  2026-10-08 and 2026-10-16 captures). CKAN datastore active.
  Captured: `raw_20261008T111216Z_b1ae17c2-cc5e-4254-9bbf-3eddcf30d033_418a1a40.csv`,
  50,151 bytes, 670 data rows, one header epoch (H-A), CRLF line endings, no BOM.
  Recaptured: `raw_20261016T204029Z_b1ae17c2-cc5e-4254-9bbf-3eddcf30d033_1352dade.csv`,
  50,089 bytes, 670 data rows, same header, CRLF line endings, no BOM (sidecar, checked
  2026-10-24).
- 14 Day Ahead Operational Metered Windfarm-Level Wind Forecast → `metered_wind_forecast_14d_windfarm`.
  Download as captured: [14da_windunit_forecast_20261008_1115.csv](https://api.neso.energy/dataset/ca6fc361-9099-4ab2-ac02-c959431e84bc/resource/31e6d895-af48-41bd-a4db-28a78c7e9c4b/download/14da_windunit_forecast_20261008_1115.csv).
  The file name carries a date-time token and changes with each publication. The 2026-10-06
  catalogue snapshot listed `14da_windunit_forecast_20261006_2015.csv` for the same resource
  id. The stable handle is the resource id, not the URL. CKAN datastore active.
  Captured: `raw_20261008T111220Z_31e6d895-af48-41bd-a4db-28a78c7e9c4b_bfebc077.csv`,
  19,603,927 bytes, 182,240 data rows, one header epoch (H-B), CRLF line endings, no BOM.
  Recaptured from `14da_windunit_forecast_20261016_2115.csv`:
  `raw_20261016T204033Z_31e6d895-af48-41bd-a4db-28a78c7e9c4b_5bfe3f67.csv`, 19,596,664 bytes,
  182,240 data rows, same header, CRLF line endings, no BOM (sidecar, checked 2026-10-24).

### DOC

None. The package has no DOC-disposition resource and no `_files` family (gridflow
`@.planning/phases/v0.22-K-GEN-1/K-GEN-1-FACTS.md` GEN1-4). The field definitions come from the
CKAN datastore dictionary of each resource, captured 2026-10-08
(`.planning/research/neso-snapshots/field-info/20261008T114228Z/`).

## Families

### `metered_wind_forecast_14d`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Datetime | `datetime` | datetime | `%Y-%m-%dT%H:%M:%SZ` | no | UTC | ISO 8601 (UTC) |
| Date | `date` | date | `%Y-%m-%d` | yes | — | — |
| Settlement_Period | `settlement_period` | int64 | — | yes | — | — |
| Capacity | `capacity` | float64 | — | yes | — | MW |
| Wind_Forecast | `wind_forecast` | float64 | — | yes | — | MW |
| ForecastDatetime | `forecast_datetime` | datetime | `%Y-%m-%dT%H:%M:%SZ` | no | UTC | ISO 8601 (UTC) |

- Entity key: `datetime`, `issue_time`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource: `2026-10-08T10:16:12.426355` for the 2026-10-08
   capture and `2026-10-16T20:16:19.155934` for the 2026-10-16 capture, which CKAN emits without
   an offset. gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Each capture's 670
   silver rows share that capture's vintage. Read as UTC, each vintage falls 24 minutes after the
   file's own `ForecastDatetime` (stated UTC); read as UK time (BST), it would fall before it.
2. **Event time (`utc_instant` on `datetime`).** `timestamp_utc` = `event_time` = `datetime`,
   the target half-hour. Checked on every silver row on 2026-10-09, and on both captures on
   2026-10-24 (including the 50-period clock-change day, below). The vendor labels
   `Datetime` "ISO 8601 (UTC)". Every row's `Datetime` equals the **start** of its
   `Date`/`Settlement_Period` under the UK settlement-day convention, with zero offset (FACTS
   T01, g1). So `datetime` is the period **start**, not the end, even though the vendor's
   settlement-period comment describes SP1 as the half hour *ending* 00:30 UK time. Event time
   is **not** the capture time.

**Issue time.** This family has a per-row production clock. `ForecastDatetime` is the vendor's
"date and time of when the forecast is produced", unit "ISO 8601 (UTC)". The record maps it to
`issue_time` (silver keeps both `forecast_datetime` and `issue_time`, equal). Each capture holds
**one** issue shared by all its 670 targets: `2026-10-08T09:52:34Z` (FACTS GEN1-1) and
`2026-10-16T19:52:23Z` (checked 2026-10-24). Each sits 24 minutes before its CKAN vintage. The vintage, **not** the issue time, drives `published_at` and
`available_at`. gridflow does not use `issue_time_evidenced`, because no source shows that a
forecast was available at its stated production instant, or that published values never change
after it (FACTS g2). `TODO: verify` issue immutability and availability at `ForecastDatetime`.

**Why this family is eligible (forward-target rule, RULINGS 529 / 542).** Every target in the
capture is after the capture's CKAN `last_modified`. The earliest target is
2026-10-08T10:30:00Z against a vintage of 2026-10-08T10:16:12Z. No target row sits at or
before the vintage (FACTS GEN1-1). The 2026-10-16 capture keeps the property: earliest target
2026-10-16T20:30:00Z against a vintage of 2026-10-16T20:16:19Z, no row at or before it
(checked 2026-10-24). The forecast was therefore public at the vintage instant,
before any of its targets began, so the vintage is a valid conservative availability clock.
gridflow pins this property in
`@tests/unit/test_neso_gen1_records.py::test_eligible_fixture_targets_are_after_the_capture_vintage`,
and the production instant in `::test_national_issue_columns_declare_the_production_instant`.
Eligibility is conditional on later captures keeping the property. The sibling ordinary
14-day package (@14-days-ahead-wind-forecasts.md) fails it and is held.

**Horizon of the captured file.** 670 consecutive half-hours, 30 minutes apart, in each
capture: 2026-10-08T10:30Z (`date` 2026-10-08, SP 24) to 2026-10-22T09:00Z (`date` 2026-10-22)
in the 2026-10-08 capture, and 2026-10-16T20:30Z (`date` 2026-10-16, SP 44) to
2026-10-30T19:00Z (`date` 2026-10-30, SP 39) in the 2026-10-16 capture. The file starts at the
next settlement period after publication, not at midnight. The record allows SP 1–50.

**Clock change (observed once, autumn 2026).** The 2026-10-16 capture spans the 25 October
change from BST to GMT. That `date` has **50** settlement periods (SP 1–50), starting
2026-10-24T23:00Z; 26 October's SP 1 starts 2026-10-26T00:00Z. `Datetime` stays an unbroken UTC
half-hour sequence, and on every row of both captures it equals the UTC start of its
`Date`/`Settlement_Period` under the UK settlement-day convention (checked 2026-10-24). The
2026-10-08 capture has 48 periods on every full day. The spring change (46 periods) is
unobserved. `TODO: verify` the spring-change labelling.

**Units (vendor dictionary only).** `Capacity` and `Wind_Forecast` are **MW**, both declared in
the resource's datastore dictionary (FACTS g4). The dictionary describes `Capacity` as the total
operational wind capacity connected to the National Grid transmission network, and
`Wind_Forecast` as the forecast for each half-hourly settlement period. `Settlement_Period` is an
index and `Date` a settlement-date label. Neither carries a physical unit. Within each capture
`capacity` is the same value in every row (26,738 MW on 2026-10-08, 26,860 MW on 2026-10-16),
and every `wind_forecast` value is a whole number. The forecast ranges from 2,716 to 21,464 MW
in the 2026-10-08 capture and from 7,887 to 18,240 MW in the 2026-10-16 capture.

**Sentinels and missing values (FACTS g5).** The record declares no null token. Full-body
checks found no `N/A`, `NA`, literal `-1` or numeric −1 and no blank cells. Silver has **no
nulls** in any column. The national file has no zero values and no negatives.

**Identity and selection.** The entity key is `(datetime, issue_time)`. Within each capture both
`datetime` alone and `(datetime, issue_time)` have zero duplicates (FACTS T05; both captures
checked 2026-10-24). No vendor text documents a contractual key or revision grain.
`TODO: verify` the vendor's revision key.
`_latest` is `whole_capture`: the newest capture replaces the previous one as a whole.

**Captures repeat targets.** The base silver table keeps every capture: 1,340 rows from the
2026-10-08 and 2026-10-16 captures. The two share 266 targets (2026-10-16T20:30Z to
2026-10-22T09:00Z) under different issues, and no shared target has the same value in both
(largest difference 5,169 MW). A reader of the base table must pick an issue (or use
`_latest`); the page's chart and sample rows filter to the 2026-10-16 issue and de-duplicate on
`datetime` as a guard.

**Relation to the windfarm file.** Summed over all windfarm rows for each target,
the windfarm `wind_forecast` matches the national value to within 0.5 MW in all 670 targets
(mean absolute difference 0.24 MW), and windfarm `capacity` sums to the national 26,738 MW to
within 0.2 MW. Measured on 2026-10-09 silver. The 2026-10-16 captures agree the same way: all
670 targets within 0.499 MW (mean 0.24 MW; the rounded farm sum equals the national value at
every target), and farm capacity sums to 26,859.8 against the national 26,860 MW (checked
2026-10-24). This is consistent with the national file being
the rounded sum of the windfarm file. No vendor text states it.
`TODO: verify` with the vendor that the national figure is defined as the windfarm sum.

**Activation (2026-10-09, master `f19effb`, PR #92).** Transformed at cutoff 2026-10-08 (one
capture): **670 silver rows**, equal to the planned count. No prior silver existed, so nothing
was overwritten. Reconcile `--all --cutoff 2026-10-08` exited 0 with 0 gaps over 55 recorded
families (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1; RULINGS 545–546). A second capture
(2026-10-16, 670 rows) is in silver as its own file; on 2026-10-24 the base table held 1,340
rows and `_latest` the 670 of 2026-10-16.

Silver columns beyond the vendor columns: `issue_time`, `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (all timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1,
epoch 1).

### `metered_wind_forecast_14d_windfarm`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Datetime | `datetime` | datetime | `%Y-%m-%dT%H:%M:%SZ` | no | UTC | ISO 8601 (UTC) |
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

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the captured resource: `2026-10-08T10:16:24.243581` and
   `2026-10-16T20:16:31.024310` (offset-less, read as UTC per ADR-030). Each capture's 182,240
   silver rows share that capture's vintage. Each is 12 seconds after the national file's
   vintage of the same day.
2. **Event time (`utc_instant` on `datetime`).** `timestamp_utc` = `event_time` = `datetime`,
   the UTC **start** of the target half-hour (vendor unit "ISO 8601 (UTC)"; zero measured offset
   from settlement start, FACTS T01). Checked on every silver row on 2026-10-09, and
   `timestamp_utc` = `datetime` on both captures on 2026-10-24. It is not the capture time.

The record's issue recipe is `none`. Unlike the national file, the windfarm file has **no
production-time column**. The date-time token in the file name (`20261008_1115`,
`20261016_2115`) is not evidenced as an issue instant, so gridflow does not read one from it
(FACTS §`metered_wind_forecast_14d_windfarm`). The vintage is the only availability clock.

**Why this family is eligible (forward-target rule, RULINGS 529 / 542).** Every target is
after the CKAN vintage: earliest target 2026-10-08T10:30:00Z against a vintage of
2026-10-08T10:16:24Z, zero rows at or before it (FACTS GEN1-1); in the 2026-10-16 capture,
2026-10-16T20:30:00Z against 2026-10-16T20:16:31Z, again zero (checked 2026-10-24). Pinned by
the same test as the national family. Eligibility is conditional on later captures keeping the
property.

**Layout of the captured file.** 272 windfarms × 670 half-hours = 182,240 rows in each
capture. Every generator has exactly 670 rows, covering the same targets as the national file
of the same day (2026-10-08 SP 24 to 2026-10-22 in the first capture; 2026-10-16 SP 44 to
2026-10-30 SP 39, with the 50-period 25 October, in the second). Each `generator_name` maps to
exactly one `generator_full_name` and one `region` (272 distinct name/full-name/region triples)
and has one constant `capacity` across the horizon. Both captures list the same 272 farms; two
farms' capacities rose between them (`SOFWO-11` Sofia 11, 112 to 176 MW; `DBBWO-3` Dogger Bank
B3, 160 to 218 MW), which is the national capacity's rise from 26,738 to 26,860 MW.

**Generator names.** The vendor defines `Generator_Name` as "the shortened name of the wind
farm" and `Generator_Full_Name` as its full name. Both are stored byte-for-byte as supplied
(pinned by `::test_wind_values_keep_zeros_negatives_and_names_as_is`). Matched exactly against
Elexon reference data, 231 of the 272 names equal an Elexon `national_grid_bm_unit`, and none
equals a `bm_unit_id` (FACTS §5). An exact join to Elexon therefore goes through
`national_grid_bm_unit`; do not add prefixes or otherwise rewrite the names. The other 41 names
have no exact Elexon match. `TODO: verify` what those 41 sites are.

**Regions.** The vendor comment says regions use the ITL 1 regions for England, the DNO licence
areas for Wales and Scotland extended to their national borders, and, offshore, the IHO sea
areas split by the land region where the farm connects. The capture has **19 regions**:

| Region | Windfarms |
|---|---:|
| NORTH SCOTLAND | 90 |
| SOUTH SCOTLAND | 79 |
| NORTH SEA - EAST ENGLAND | 21 |
| NORTH SEA - NORTH SCOTLAND | 20 |
| NORTH SEA - YORKSHIRE & HUMBER | 19 |
| IRISH SEA - NORTH WEST ENGLAND | 11 |
| IRISH SEA - NORTH WALES | 7 |
| NORTH SEA - SOUTH EAST ENGLAND | 6 |
| NORTH SEA - EAST MIDLANDS | 4 |
| NORTH SEA - NORTH EAST ENGLAND | 4 |
| ENGLISH CHANNEL - SOUTH EAST ENGLAND | 2 |
| NORTH SEA - SOUTH SCOTLAND | 2 |
| EAST MIDLANDS | 1 |
| NORTH WALES | 1 |
| NORTH WEST ENGLAND | 1 |
| SOUTH EAST ENGLAND | 1 |
| SOUTH WALES | 1 |
| SOUTH WEST ENGLAND | 1 |
| YORKSHIRE & HUMBER | 1 |

**Units (vendor dictionary only).** `Capacity` and `Wind_Forecast` are **MW**, declared in the
resource's datastore dictionary (FACTS g4). `Capacity` is the windfarm's operational wind
capacity connected to the transmission network. `Wind_Forecast` is the half-hourly forecast.
Forecast values are fractional (for example 14.877474 MW for ABRBO-1 at the first target).
Name, full name and region are text dimensions.

**Sentinels, zeros and missing values (FACTS g5).** No null token is declared, no blank cells,
no `N/A`/`NA`/−1, and no negatives. Silver has no nulls. Zeros are common and are **kept as
zeros**:

- `capacity` = 0 in 1,340 rows; `wind_forecast` = 0 in 4,598 rows (2026-10-08 capture). The
  2026-10-16 capture has the same 1,340 zero-capacity rows and 5,437 zero forecasts, 4,097 of
  them beside positive capacity (checked 2026-10-24).
- 2 windfarms have zero capacity for the whole horizon, and 3 have a zero forecast for the
  whole horizon (the longest zero run, 670 half-hours, is a whole generator); in the 2026-10-16
  capture, 2 and 4.
- Zero forecasts also occur where capacity is positive.
- No row has `wind_forecast` above `capacity`.

No vendor source says a zero means missing, unavailable or not applicable.
`TODO: verify` the vendor's meaning of zero capacity and zero-forecast runs.

**Identity and selection.** The entity key is `(datetime, generator_name)`, with zero duplicates
over the complete body of each capture (FACTS T04; both captures checked 2026-10-24). No vendor
text documents it as a contractual key.
`TODO: verify` the vendor's revision key. `_latest` is `whole_capture`.

**Captures repeat keys.** The base silver table keeps both captures (364,480 rows). The 266
targets they share give 72,352 `(datetime, generator_name)` pairs that appear twice, with
different forecasts and no issue column to tell them apart; only `published_at` and
`bronze_capture_id` do. `_latest` (what `query()` and `tail()` read) holds the newest capture
only.

**Activation (2026-10-09, master `f19effb`, PR #92).** Transformed at cutoff 2026-10-08:
**182,240 silver rows**, equal to the planned count, with no prior silver overwritten. Reconcile
reported 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1; RULINGS 545–546). Silver
carries the same lineage/clock columns as the national family, without `issue_time`. A second
capture (2026-10-16, 182,240 rows) is in silver as its own file.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

The vendor gives no publication time of day. The 2026-10-08 capture has CKAN `last_modified`
values of 10:16 UTC (11:16 BST) for both resources, and the national forecast was produced at
09:52:34 UTC. The 2026-10-16 capture has 20:16 UTC (21:16 BST), a national forecast produced
at 19:52:23 UTC, and a windfarm file name token of `20261016_2115`. The 2026-10-06 snapshot
showed both resources last modified at about 19:16 UTC, and a windfarm file name token of
`20261006_2015`. So publication is not at a fixed time of day, or happens more than once a day.

- `TODO: verify` the vendor's publication schedule and whether a day can carry more than one
  issue. gridflow captures once per refresh run, so any intermediate issue is missed. Each
  capture keeps only the forecast present at capture time.
- `TODO: verify` whether the windfarm file-name token is the publication clock time (it reads
  11:15 against an 11:16 BST `last_modified` on 2026-10-08, and 21:15 against 21:16 BST on
  2026-10-16). gridflow does not rely on it.
- Captures to date: two per family (2026-10-08 and 2026-10-16), each a new issue.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

Both families are **eligible** under the forward-target rule (RULINGS 529, applied to GEN-1 by
RULINGS 542). The remaining open items (issue immutability, vendor keys, zero semantics,
spring clock-change labelling) are `TODO: verify` notes, not holds. They do not block publication of these current
bodies.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`): the
ordinary 14-day national and BMU forecasts (@14-days-ahead-wind-forecasts.md) are held because
their current bodies contain targets at or before the CKAN vintage (3 and 693 rows). The
historic day-ahead wind archives (@day-ahead-wind-forecast.md) are held on issue-clock
questions. All are unit E-SEM.
