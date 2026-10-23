---
source: "neso_data_portal"
package: "day-ahead-half-hourly-demand-forecast-performance"
dataset_key: "da_demand_fc_performance"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-16
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Day Ahead Half Hourly Demand Forecast Performance

NESO's scorecard for its own day-ahead forecast of GB **national demand**. The vendor describes
the package as the historic half-hourly day-ahead national demand forecast, as published via
BMRS, set beside the demand outturn, an estimate of TRIAD avoidance, and the Absolute Percentage
Error (APE) of each half hour, from April 2021 onwards. For earlier periods the vendor points to
the 1B metric data it submitted to Ofgem (vendor package notes; the link is in the package
metadata). It is a single CSV with one row per outturn half hour. Each row carries the forecast,
the outturn, the TRIAD-corrected outturn and the error, plus the time the forecast was made.

TRIAD avoidance is the demand reduction that large users make in the winter peak half hours
that set transmission charges. The vendor's TRIAD columns restore that reduction to the outturn
so the forecast is not scored against an artificially lowered demand (vendor dictionary, see
Units). The vendor also says the TRIAD estimates may be revised after publication.

This is the strongest candidate gridflow has found for pairing a half-hourly day-ahead ND forecast
with its outturn in one file. That makes it the natural input for a forecast-versus-outturn view and
for a benchmark against Elexon NDF (@../../elexon/datasets/ndf.md). Background on why such
forecasts matter for models:
@../../../20-domain/modelling/renewable-and-demand-forecasting.md.

**Status: silver exists, publication is held.** The time columns carry a literal `Z` while the
vendor dictionary says they follow UK clock changes (GMT/BST). Which end of the half hour
`Datetime` marks, how the autumn clock-change days are labelled, and whether `Publish_Datetime`
is a publication instant are all undocumented. The hold is unit E-SEM (class 3, see Holds). This
page gives schema, row counts and structural counts only. It gives no demand values, errors or
ranges.

- Publisher group: Demand
- Registry group: demand · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Day Ahead Half Hourly Demand Forecast Performance | CSV | upload | `08e41551-80f8-4e28-a416-ea473a695db9` |

- Download as captured: [1b-incentive.csv](https://api.neso.energy/dataset/5281b494-5566-42dd-bf1a-9ce38642fabf/resource/08e41551-80f8-4e28-a416-ea473a695db9/download/1b-incentive.csv).
  The file name is the vendor's (`1b-incentive` echoes the Ofgem 1B incentive metric). The stable
  handle is the resource id. CKAN datastore active; CKAN package id
  `5281b494-5566-42dd-bf1a-9ce38642fabf`.
- Vendor resource description: historic half-hourly day-ahead national demand forecast, alongside
  the outturn values, TRIAD avoidance adjustments and APE for each half hour from April 2021
  onwards; updated monthly.
- Captured: `raw_20261008T091708Z_08e41551-80f8-4e28-a416-ea473a695db9_ca3e01ad.csv`,
  9,573,900 bytes, 96,786 data rows, one header epoch, UTF-8 with a byte-order mark. The
  sidecar records `declared_content_length` 9,573,900 equal to the body size.
- The package has no other resources. There is no DOC file and no second family.

## Families

### `da_demand_fc_performance`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Month | `month_name` | string | — | yes | — | — |
| Date | `outturn_date` | date | `%Y-%m-%d` | yes | — | — |
| Datetime | `outturn_datetime` | string | — | yes | — | GMT/BST |
| Settlement_Period | `settlement_period` | int64 | — | yes | — | — |
| Demand_Forecast | `demand_forecast` | int64 | — | yes | — | MW |
| Demand_Outturn | `demand_outturn` | int64 | — | yes | — | MW |
| TRIAD_Avoidance_Estimate | `triad_avoidance_estimate` | int64 | — | yes | — | MW |
| TRIAD_Avoidance_Corrected_Demand_Outturn | `triad_avoidance_corrected_demand_outturn` | int64 | — | yes | — | MW |
| APE | `ape` | float64 | — | yes | — | % |
| Absolute_Error | `absolute_error` | int64 | — | yes | — | MW |
| Publish_Datetime | `publish_datetime` | string | — | yes | — | GMT/BST |

- Entity key: `month_name`, `outturn_date`, `outturn_datetime`, `settlement_period`, `demand_forecast`, `demand_outturn`, `triad_avoidance_estimate`, `triad_avoidance_corrected_demand_outturn`, `ape`, `absolute_error`, `publish_datetime`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource: `2026-10-08T09:15:10.605360`, which CKAN emits
   without an offset and gridflow reads as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All 96,786 silver rows share
   this one vintage. It says when the file last changed. It does **not** say when any single
   forecast became available. Every `Publish_Datetime` in the capture falls before the vintage
   (checked at query time, see Cadence for how the vintage moves). The file is rewritten as a
   whole, so no row carries its own availability stamp.
2. **Event time (temporal recipe `none`).** The record declares no temporal recipe, so
   `timestamp_utc` is the **capture time**, not the outturn time. In silver `timestamp_utc` and
   `event_time` both equal `capture_written_at` (`2026-10-08T09:17:08.775840Z`) on every row (1
   distinct value, checked at query time). The real outturn position is in the raw columns
   `outturn_date`, `settlement_period` and the string `outturn_datetime`. They are kept as the
   vendor wrote them because no tz-aware conversion is yet established (see Holds). Do not use
   `timestamp_utc` as a time axis for this family.

The vendor's own per-row clock is `Publish_Datetime`, which the dictionary defines as the
datetime at which the forecast was made. gridflow does not use it as an issue clock. The record's
issue recipe is `none`, and whether it dates publication or availability is an open question
(see Holds).

**Units (vendor dictionary only).** Taken from the datastore field information for this
resource (snapshot `20261006T195819Z`, field info swept 2026-10-08), not inferred from column names.

| Column | Vendor unit | Vendor description (paraphrased) |
|---|---|---|
| `demand_forecast` | MW | National demand forecast for the specified datetime |
| `demand_outturn` | MW | National demand outturn for the specified datetime |
| `triad_avoidance_estimate` | MW | TRIAD avoidance estimated to have taken place at the time of the outturn |
| `triad_avoidance_corrected_demand_outturn` | MW | National demand outturn after adding any estimated TRIAD avoidance |
| `ape` | % | Absolute Percentage Error of the forecast |
| `absolute_error` | MW | Absolute Error of the forecast |
| `outturn_datetime`, `publish_datetime` | GMT/BST | Follows clock changes (BST when the UK was in BST and vice versa) |

`month_name`, `outturn_date` and `settlement_period` are labels and carry no unit. The
dictionary does not say which demand measure "national demand" is. The vendor's day-ahead
cardinal-point packages define it as ND (generation requirement excluding station load,
pumped-storage pumping and interconnector exports), see
@1-day-ahead-demand-forecast.md. `TODO: verify` that this package uses the same ND definition.
The dictionary does not give the APE formula, the denominator (forecast or outturn, TRIAD
corrected or not) or its rounding. `TODO: verify` before recomputing it.

**Sentinels and missing values (FACTS g5).** The record declares no null token and no bounds
beyond `settlement_period` 1..50.

- None of the 11 vendor columns contains a null in silver (0 nulls per column, checked at query time).
- The vendor comment says `TRIAD_Avoidance_Estimate` is 0 for every period outside TRIAD season,
  and that the corrected outturn is unchanged from the outturn outside TRIAD season. A zero
  estimate is therefore a **real zero**, not a missing value. gridflow does not convert it.
- No other sentinel, `NA` token or blank convention is documented or seen as a null. `TODO: verify`
  that the vendor uses no placeholder value in the forecast or error columns.

**Settlement-period structure (structural counts only).** The silver table has 2,017 outturn
dates. Settlement period spans 1..50 in the data.

| Rows per outturn date | Days | Reading |
|---|---|---|
| 48 | 2,007 | ordinary day (plus one 25-hour day, see below) |
| 46 | 5 | spring clock-change days (2022-03-27, 2023-03-26, 2024-03-31, 2025-03-30, 2026-03-29) |
| 50 | 4 | autumn clock-change days (2021-10-31, 2023-10-29, 2024-10-27, 2025-10-26) |
| 20 | 1 | the final date, partial (the capture's own day) |

The autumn day of 2022-10-30 has **48** rows, not 50, and 46 distinct settlement-period labels.
On the autumn day of 2021-10-31 there are 50 rows but only 48 distinct labels. The label pairs
repeat as already named in the hold question: SP4/SP5 on 2021-10-31 and SP2/SP3 on 2022-10-30.
`(outturn_date, settlement_period)` therefore occurs twice in 4 groups (the two repeated pairs).
No two rows are identical on all 11 vendor columns. Do not dedup on `(outturn_date,
settlement_period)` alone (project rule: DST days have 46 or 50 periods and labels must not be
silently collapsed).

**Datetime label behaviour (observed, not a ruling).** `outturn_datetime` and `publish_datetime`
parse as `%Y-%m-%dT%H:%M:%SZ` on every row (0 failures) and every `publish_datetime` is earlier
than its row's `outturn_datetime`. `publish_datetime` has exactly one value per outturn date
(2,017 distinct values over 2,017 dates), so it behaves as one forecast issue per target day.
In 2,016 rows the `outturn_datetime` calendar date differs from `outturn_date`. Earlier research
(gridflow `@.planning/phases/v0.22-E-profiler-pilot/RESEARCH.md`) found SP1 of 2021-04-01
labelled `00:30:00Z`, SP48 of that day labelled `00:00:00Z` on the next day, and on the 46-period
day 2022-03-27 SP1 labelled `00:30:00Z` and SP2 `02:00:00Z`. That pattern suggests period-**end**
labels written in UK wall-clock time with a literal `Z` appended. It is an inference only. A
further hint: two rows of the final partial day (SP19, SP20) have an `outturn_datetime` that is
later than the file's own CKAN `last_modified` if the `Z` is read as true UTC, which a published
outturn cannot be. All of this is why the strings are kept raw. `TODO: verify` with NESO the
timezone, the start/end convention, the labelling of the autumn day and the meaning of
`Publish_Datetime` before any instant is derived.

**Revision behaviour.** The vendor package notes say TRIAD avoidance estimates may be revised
after publication. The dictionary does not say whether forecast or outturn values are revised.
The file is a monthly rewrite of the whole series. With `latest: whole_capture` each new capture
replaces the previous one as a whole, and earlier states remain only in bronze. `TODO: verify`
whether earlier months are restated on each update. Only repeated captures compared row by row
can show it. One capture exists so far.

**Identity and selection.** The entity key is every vendor column, a capture-level duplicate
guard with zero duplicates in the capture. The vendor does not document a row identity.
`(outturn_date, settlement_period)` is unique except for the four repeated labels above, so it is
not a safe key. `TODO: verify` the vendor's row identity once the label repeats are explained.

**Activation (2026-10-08, master `29b563c`).** Transformed at cutoff 2026-10-08 (first and only
capture): `gridflow transform neso_data_portal da_demand_fc_performance --start 2026-10-08 --end
2026-10-08` wrote **96,786 silver rows**. No prior silver existed, so nothing was overwritten.
Reconcile at that cutoff exited 0 with 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` §E and
§BS; RULINGS 504). The row count equals the datastore `total` the field-info sweep read
(96,786, 2026-10-08T12:08Z). As of the query on 2026-10-16T18:37Z silver still holds one parquet
file, one capture and 96,786 rows. Silver columns beyond the vendor columns: `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id`, `dataset_version` (all timestamps tz-aware UTC; `dataset_version` `1+e1` =
record version 1, epoch 1).

Silver path: `C:\gridflow-data\silver\neso_data_portal\da_demand_fc_performance\year=2026\month=10\`.

**Downstream.** There is no gold view for this family. The day-ahead forecast-versus-outturn
view (G-1) was not built (RULINGS 591, gridflow
`@docs/DECISION_LOG/ADR-041-gold-forecast-vs-outturn-contracts.md`, status proposed after owner
ruling 874). A follow-up research unit (RULINGS 596) found no evidence that lifts this hold.

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Monthly
- Captured once per refresh run. Captures to date: one (2026-10-08).

The CKAN `last_modified` of the resource was `2026-10-06T09:15:08` in the 2026-10-06 catalogue
snapshot and `2026-10-08T09:15:10` at capture. The file therefore changed between those two
dates, two days apart, which is more often than "Monthly" suggests. Both stamps are near 09:15 UTC. The final date in the
capture is a partial day, so the file also carries the current day. `TODO: verify` the real
update cadence and the lag between an outturn half hour and its appearance in the file. Only
repeated captures can show it.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above. Vendor dictionary:
[Day Ahead Half Hourly Demand Forecast Performance](https://www.neso.energy/data-portal/day-ahead-half-hourly-demand-forecast-performance/day_ahead_half_hourly_demand_forecast_performance).

## Holds

- `da_demand_fc_performance`: held: TODO: Datetime and Publish_Datetime end in 'Z' but the dictionary states GMT/BST; whether Datetime marks period start or end; Settlement_Period repeats SP4/SP5 on 2021-10-31 and SP2/SP3 on 2022-10-30; whether Publish_Datetime is the publication instant (unit E-SEM)

The hold is a class 3 call (the profiler pilot, RULINGS 504; carried by the eligibility report in
gridflow `@docs/neso_data_portal/eligibility.md`). A held package holds every output of the
package. Silver exists and stays on disk, but the family is **not eligible** for publication or
point-in-time use. The package-level `eligibility: eligible` in the front matter is the
registry's package entry. The hold sits on the family record. This page publishes no data values
from the family.

Unit E-SEM needs four answers from NESO before the hold can lift:

1. How the literal `Z` on `Datetime` and `Publish_Datetime` reconciles with the dictionary's
   GMT/BST statement.
2. Whether `Datetime` marks the start or the end of the half hour.
3. How the autumn clock-change days are labelled. 2021-10-31 repeats SP4/SP5 and 2022-10-30
   repeats SP2/SP3, with 50 and 48 rows respectively.
4. Whether `Publish_Datetime` is the instant the forecast was published, and so usable as an
   availability time, or only the time the forecast was produced. The dictionary defines it only
   as the datetime at which the forecast was made.

Until then the CKAN vintage cannot stand in for an issue time. It is the last-modified stamp of
a monthly rewritten file and is later than every forecast it holds. The research and gold units
(RULINGS 591, 596) kept this family as the strongest named candidate for a half-hourly
day-ahead ND comparison, but its time and availability contract is unresolved.

Related holds from the same demand-forecast cluster (gridflow `@docs/neso_data_portal/eligibility.md`):
the cardinal-point archives and the 2–14-day half-hourly file, for example
@1-day-ahead-demand-forecast.md, @2-14-days-ahead-national-demand-forecast.md and
@daily-demand-update.md. They are held on their own timestamp questions.
