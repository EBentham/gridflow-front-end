---
source: "neso_data_portal"
package: "negative-reserve-active-power-margin-nrapm-forecast"
dataset_keys: ["nrapm_forecast_national_daily_days", "nrapm_forecast_scotland_daily_days", "nrapm_forecast_weekly_week_national", "nrapm_forecast_weekly_week_scotland"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Daily & Weekly NRAPM (Negative Reserve Active Power Margin) Forecast

NESO's forecast of the risk of a **Negative Reserve Active Power Margin (NRAPM)**. That is a
condition where, in the vendor's words, there is insufficient flexibility available to ensure
that generation matches demand during low demand periods. The vendor's package notes say a system NRAPM warning asks generators for more
flexible parameters and tells participants there is a risk of **emergency instructions**. The
forecast exists to signal that risk to the market ahead of time. The package has four CSVs, a
national (system-level) and a Scotland version of each of two horizons:

- **Daily, 2–14 days ahead.** For each target date, two rows, one per demand **cardinal point**:
  `1B` (overnight daily minimum) and `3B` (daily minimum), per the vendor resource
  descriptions. Each row gives the forecast **MW away from risk** of an NRAPM under forecast
  conditions.
- **Weekly, 2–52 weeks ahead.** One row per week. The vendor resource descriptions call it the
  probability of seeing a wind load factor that would cause an NRAPM. Each row has a wind
  load-factor column and a probability column.

Use the daily files as a forward indicator of NRAPM risk in low-demand periods on the GB
system, and as context for Balancing Mechanism actions at the overnight daily minimum (1B) and
daily minimum (3B) (@../../../20-domain/markets/gb-balancing-mechanism.md). gridflow's own
inference, not vendor-stated: the files may also serve as a feature for negative-price and
curtailment risk (TODO: verify against a vendor or market source before relying on it). The
daily files are eligible for
publication. The weekly files' silver output is **held**, because their value columns have no
vendor unit or scale and their dictionary text contradicts itself (see Holds). Related margin
data: the `Negative Reserve` column of Daily OPMR (@daily-opmr.md) and Weekly OPMR
(@weekly-opmr.md), both held in the same batch.

- Publisher group: Generation
- Registry group: generation · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| National Daily 2-14 days NRAPM Forecast | CSV | upload | `4c391daa-14e2-4991-a476-5539033ebb3d` |
| Scotland Daily 2-14 days NRAPM Forecast | CSV | upload | `c2861f81-b400-4456-870e-d51a4b530331` |
| Weekly 2-52 week National NRAPM Forecast | CSV | upload | `42377a3d-e202-475f-9069-dcd4d1fae952` |
| Weekly 2-52 week Scotland NRAPM forecast | CSV | upload | `88f3e766-fff2-418c-aef2-4b627d2cdabd` |

All four are CKAN uploads with the datastore active. The file names are stable (no date token).
Captures are one per family, all on 2026-10-08, each with one header epoch.

- National Daily 2-14 days NRAPM Forecast → `nrapm_forecast_national_daily_days` (eligible).
  Download: [dailynrapmresult.csv](https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/4c391daa-14e2-4991-a476-5539033ebb3d/download/dailynrapmresult.csv).
  Captured: `raw_20261008T111424Z_4c391daa-14e2-4991-a476-5539033ebb3d_6a70ed41.csv`,
  660 bytes, 26 data rows.
- Scotland Daily 2-14 days NRAPM Forecast → `nrapm_forecast_scotland_daily_days` (eligible).
  Download: [scotdailynrapmresult.csv](https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/c2861f81-b400-4456-870e-d51a4b530331/download/scotdailynrapmresult.csv).
  Captured: `raw_20261008T111428Z_c2861f81-b400-4456-870e-d51a4b530331_65a59a29.csv`,
  649 bytes, 26 data rows.
- Weekly 2-52 week National NRAPM Forecast → `nrapm_forecast_weekly_week_national` (**held**).
  Download: [weeklynrapmresult.csv](https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/42377a3d-e202-475f-9069-dcd4d1fae952/download/weeklynrapmresult.csv).
  Captured: `raw_20261008T111431Z_42377a3d-e202-475f-9069-dcd4d1fae952_f7ceaa0f.csv`,
  1,745 bytes, 55 data rows.
- Weekly 2-52 week Scotland NRAPM forecast → `nrapm_forecast_weekly_week_scotland` (**held**).
  Download: [scotweeklynrapmresult.csv](https://api.neso.energy/dataset/64151a33-3075-437d-bf11-fc00f297520e/resource/88f3e766-fff2-418c-aef2-4b627d2cdabd/download/scotweeklynrapmresult.csv).
  Captured: `raw_20261008T111435Z_88f3e766-fff2-418c-aef2-4b627d2cdabd_f6d8d5f3.csv`,
  1,747 bytes, 55 data rows.

The package has **no DOC resources** and no `_files` family (gridflow
`@.planning/phases/v0.22-K-GEN-1/K-GEN-1-FACTS.md` GEN1-4).

**Column rename (vendor notice).** The package notes announced that on 5 August 2026 the daily
value column ids would change from `... NRAPM (Forecast Conditions)` to
`... NRAPM_Forecast Conditions`. The 2026-10-08 captures already carry the new `_Forecast
Conditions` spelling, and the records freeze only that epoch. A capture with the old spelling
would not match epoch 1. `TODO: verify` whether any older bodies with the pre-rename header
need a second epoch. None has been captured.

## Families

### `nrapm_forecast_national_daily_days`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| CP | `cp` | string | — | yes | — | — |
| MW away from risk of System Level NRAPM_Forecast Conditions | `mw_away_from_risk_of_system_level_nrapm_forecast_conditions` | float64 | — | yes | — | MW |

- Entity key: `date`, `cp`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the captured resource. For the one capture to date that is
   `2026-10-08T11:04:46.768036`, which CKAN emits without an offset. gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All 26 silver rows
   share this vintage. The file has **no issue column**, and the record's issue recipe is
   `none`.
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` = `event_time` = the start of
   settlement period 1 of the target date: UK local midnight of `date` in UTC (23:00 UTC the
   previous day during BST). Checked on every silver row on 2026-10-09. Event time is **not**
   the capture time. It is a **date anchor**: the `1B` and `3B` rows of a date share the same
   `timestamp_utc`. No intraday instant is built for a cardinal point, because the vendor gives
   no CP clock window in this package (FACTS §`nrapm_forecast_national_daily_days`).

**Why this family is eligible (forward-target rule, RULINGS 529, applied to GEN-1 by RULINGS
542).** Every target date in the capture falls after the capture's CKAN `last_modified`. The
earliest target anchor is 2026-10-09T23:00Z against a vintage of 2026-10-08T11:04Z, with 0 rows
at or before the vintage (FACTS GEN1-1). The forecast was public at the vintage, before any of
its target days began. The CKAN vintage is therefore a conservative proxy for the missing issue
time. The GEN-1 tests pin this property for each eligible no-issue forecast. Eligibility holds
only while later captures keep it.

**What a capture contains.** The 2026-10-08 capture covers target dates 2026-10-10 to
2026-10-22: 13 dates, i.e. days 2 to 14 ahead. Each date has exactly two rows, `cp` = `1B` and
`3B`. The vendor's CP dictionary entry explains cardinal points generically. The codes are
glossed only in the resource description ("overnight daily minimum 1B and daily minimum 3B").
`TODO: verify` the clock window of each CP. FACTS T01 records it as unspecified.

**Units (vendor dictionary only).** The value column is **MW**, declared in the field
dictionary (`unit: MW`) and in the resource description ("Forecast Megawatt (MW) away from
risk"). Do not rescale it (FACTS g4, GEN1-3).

**Sign.** The capture holds one negative value (national, `1B`, 2026-10-10: −2,862 MW). The
other 25 rows are positive. The vendor does not define the sign convention. The reading "a
negative value is inside the NRAPM risk zone" is plausible from the column name but is **not
established**. `TODO: verify` the sign meaning with the NESO methodology. Values are kept as
published, with no bound imposed.

**Sentinels and missing values (FACTS g5).** No `N/A`, `NA` or literal `-1` tokens, no
value equal to −1, no blank cells, and no zeros. The record declares no null token. Silver has
no nulls in any column.

**Identity and selection.** `(date, cp)` is unique across the whole body (FACTS T02, C02). No
vendor text declares it a contractual key. `TODO: verify` the vendor key. `_latest` is
`whole_capture`: the newest capture replaces the previous one as a whole.

**Datastore count mismatch.** The vendor datastore reported `total: 52` records for this
resource when queried at 2026-10-08T13:20Z. The uploaded CSV captured two hours earlier has
26 rows. The Scotland datastore reported 26. `TODO: verify` whether the national datastore
holds a second set of rows (for example an appended earlier forecast) that the upload does not.
gridflow captures the upload, not the datastore.

National and Scotland are **separate forecast series**. They share target keys but the daily
values never coincide (FACTS GEN1-3). Whether the Scotland calculation is a component of the
national one is undocumented. Do not subtract one from the other or dedup across them.
`TODO: verify` geographical scope and additivity.

**Activation (2026-10-09, master `f19effb`, PR #92).** Transformed at cutoff 2026-10-08:
**26 silver rows**, equal to the planned count, with no prior silver overwritten. Reconcile
`--all --cutoff 2026-10-08` exited 0 with 0 gaps over 55 families (gridflow
`@.planning/v0.22-RESULTS.md` §GEN-1; RULINGS 545–546).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1`).

### `nrapm_forecast_scotland_daily_days`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| CP | `cp` | string | — | yes | — | — |
| MW away from risk of Scotland Level NRAPM_Forecast Conditions | `mw_away_from_risk_of_scotland_level_nrapm_forecast_conditions` | float64 | — | yes | — | MW |

- Entity key: `date`, `cp`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = CKAN
   `last_modified` `2026-10-08T10:55:55.308683` (offset-less, read as UTC per ADR-030). All 26
   rows share it. No issue column; issue recipe `none`.
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` = `event_time` = UK local midnight
   of the target date in UTC. Checked on every silver row on 2026-10-09. It is a date anchor,
   not the capture time, and not a CP-specific instant.

**Eligible (RULINGS 529/542).** Every target falls after the vintage: the earliest anchor is
2026-10-09T23:00Z against a vintage of 2026-10-08T10:55Z, with 0 rows at or before it (FACTS
GEN1-1).

**Contents and units.** Same layout as the national file: target dates 2026-10-10 to
2026-10-22, two rows per date (`1B`, `3B`). The value column is **MW** (field dictionary
`unit: MW`; resource description "Forecast Megawatt (MW) away from risk of Scotland Level
NRAPM"). All 26 values in this capture are positive. The sign convention is undocumented, as
for the national file.

**Sentinels (FACTS g5).** No null tokens, no −1, no blanks, no zeros. Silver has no nulls.

**Identity.** `(date, cp)` unique across the body (FACTS T02). `TODO: verify` the vendor key.
`_latest` is `whole_capture`. The vendor datastore total (26) matches the captured CSV.

**Activation (2026-10-09, master `f19effb`).** **26 silver rows**, equal to plan, nothing
overwritten, reconcile 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1). Silver carries
the same eight lineage/clock columns as the national family.

### `nrapm_forecast_weekly_week_national`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Week number | `week_number` | string | — | yes | — | — |
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| Wind Load Factor required to cause a System Level NRAPM | `wind_load_factor_required_to_cause_a_system_level_nrapm` | float64 | — | yes | — | — |
| Probability of seeing Wind load factor above | `probability_of_seeing_wind_load_factor_above` | float64 | — | yes | — | — |

- Entity key: `date`, `week_number`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM).** This family's silver output exists but is not eligible for publication
or point-in-time use. This page gives schema, row counts and structure only. It gives **no data
values, ranges or value statistics**. See Holds.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = CKAN `last_modified`
   `2026-10-08T10:46:06.065398` (offset-less, read as UTC). All 55 rows share it. No issue
   column; issue recipe `none`. The week label is a target, not an issue time (FACTS GEN1-1).
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` = `event_time` = UK local midnight
   of `date` in UTC. Checked on every silver row on 2026-10-09. It is not the capture time.
   It anchors the **start date of the week** only. The record does not spread a row across the
   seven days of its week. The vendor `Date` is kept as published; it is not recomputed from
   the week label (FACTS T03).

All target anchors fall after the vintage: the earliest is 2026-10-24T23:00Z (FACTS GEN1-1).
That is **not** why the family is held. The hold is about units.

**Units: none declared.** Both value columns have an empty `unit` in the vendor dictionary.
No conversion is applied (FACTS g4, GEN1-3). In particular, gridflow does not decide whether the
load factor or the probability is a fraction or a percentage.

**Dictionary contradictions** (vendor
[national weekly dictionary](https://www.neso.energy/data-portal/negative-reserve-active-power-margin-nrapm-forecast/weekly_2-52_week_national_nrapm_forecast)):

- The column `Wind Load Factor required to cause a System Level NRAPM` has the **title** "Wind
  Load Factor required to cause a **Scotland** Level NRAPM" and a **description** about the
  *probability* of seeing such a load factor in Scotland.
- The column `Probability of seeing Wind load factor above` has a description of the *forecast
  wind load factor* required to cause a System Level NRAPM.
- The titles and descriptions thus appear to swap the two columns' roles, and one mislabels the
  geography. gridflow keeps the vendor **column ids** as the silver names and asserts neither
  reading. `TODO: verify` corrected field semantics with NESO.
- The `Date` description reads "Date at which forecast will occur. Given in (Coordinated
  Universal Time) UTC or UTC+1 during British Summer Time". A calendar date has no zone, so
  this does not change the date recipe. The Scotland dictionary calls the same field "the date
  commencing the week number".

**Structure of the capture** (no values). 55 rows, 55 distinct dates, 55 distinct week labels,
no nulls. Every `week_number` has the shape `<week>W<yy>` (vendor example `13W20`), kept as a
string. The `Date` values fall on Saturdays or Sundays, and consecutive dates are 6, 7 or 8 days
apart. `TODO: verify` NESO's week-commencing convention; it is not a fixed weekday in this
capture. 55 rows also exceeds the 51 weeks a "2–52 week" horizon would give. `TODO: verify`
what the extra rows cover. The registry keeps every published row.

**Sentinels (FACTS g5).** No `N/A`, `NA` or literal `-1` tokens, no value equal to −1, and
no blank cells. Zeros are kept as numbers; no vendor rule makes a zero a sentinel. Silver has no
nulls.

**Identity.** `(date, week_number)` is unique across the body (FACTS T04). `TODO: verify` the
vendor key. `_latest` is `whole_capture`.

**Activation (2026-10-09, master `f19effb`).** **55 silver rows**, equal to plan, nothing
overwritten (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1). Held output stays on disk.

### `nrapm_forecast_weekly_week_scotland`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Week number | `week_number` | string | — | yes | — | — |
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| Wind Load Factor required to cause a Scotland Level NRAPM | `wind_load_factor_required_to_cause_a_scotland_level_nrapm` | float64 | — | yes | — | — |
| Probability of seeing Wind load factor above | `probability_of_seeing_wind_load_factor_above` | float64 | — | yes | — | — |

- Entity key: `date`, `week_number`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM).** Schema, row counts and structure only on this page; **no data values,
ranges or value statistics**. See Holds.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = CKAN `last_modified`
   `2026-10-08T10:35:06.056281` (offset-less, read as UTC). All 55 rows share it. No issue
   column; issue recipe `none`.
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` = `event_time` = UK local midnight
   of the week-commencing `date` in UTC. Checked on every silver row on 2026-10-09. Not the
   capture time; anchors the week's start date only. The earliest anchor, 2026-10-24T23:00Z,
   is after the vintage (FACTS GEN1-1). The hold is about units, not timing.

**Units: none declared**, and the dictionary contradicts itself (vendor
[Scotland weekly dictionary](https://www.neso.energy/data-portal/negative-reserve-active-power-margin-nrapm-forecast/weekly_2-52_week_scotland_nrapm_forecast)):

- The column `Wind Load Factor required to cause a Scotland Level NRAPM` is **titled** "...
  **System** Level NRAPM" and **described** as the *probability* of seeing a load factor that
  would cause an NRAPM in Scotland.
- The column `Probability of seeing Wind load factor above` is described as the *forecast wind
  load factor* required to cause a **System** Level NRAPM.
- Both `unit` fields are empty. No scale (fraction or percentage) is stated.

gridflow keeps the vendor column ids as silver names and applies no conversion.
`TODO: verify` corrected semantics and scale with NESO.

**Structure of the capture** (no values). 55 rows, 55 distinct dates and week labels, no
nulls, `<week>W<yy>` labels. Dates fall on Saturdays or Sundays with 6–8-day steps, as in the
national file. National and Scotland weekly share their target keys, but their rows are not
copies of each other (FACTS GEN1-3). Keep the families separate.

**Sentinels (FACTS g5).** No null tokens, no −1, no blanks. Silver has no nulls.

**Identity.** `(date, week_number)` unique across the body (FACTS T04). `TODO: verify` the
vendor key. `_latest` is `whole_capture`.

**Activation (2026-10-09, master `f19effb`).** **55 silver rows**, equal to plan, nothing
overwritten (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1).

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Daily

The four resources are updated separately. In the 2026-10-06 catalogue snapshot, the daily
files had a CKAN `last_modified` of 2026-10-06 (about 10:52–10:58) and the weekly files of
2026-10-01 (about 07:57–08:01). On 2026-10-08 all four had been modified that morning
(10:35–11:05, CKAN time read as UTC). So the weekly files are not necessarily rewritten every
day, even though the package says "Daily".

- `TODO: verify` the publication schedule of each file (daily for the 2–14-day files; daily or
  weekly for the 2–52-week files). Repeated captures will show it.
- `TODO: verify` whether a new publication replaces the whole file or revises only some
  target dates. `whole_capture` makes no assumption either way.
- Captures to date: one per family (2026-10-08). No scheduled refresh has run yet.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `nrapm_forecast_weekly_week_national`: held: TODO: the load-factor and probability columns have no vendor unit or scale, and the dictionary titles and descriptions contradict each other (unit E-SEM)
- `nrapm_forecast_weekly_week_scotland`: held: TODO: the load-factor and probability columns have no vendor unit or scale, and the dictionary titles and descriptions contradict each other (unit E-SEM)

Both weekly families are held by RULINGS 542 (seat ruling, PROXY-SOURCED), from FACTS
§`nrapm_forecast_weekly_week_*` and GEN1-3. The timing would pass the forward-target rule. The
problem is meaning: a user cannot tell which column is the load factor and which the
probability, nor whether either is a fraction or a percentage. Unit E-SEM must obtain a
corrected NESO dictionary, or methodology text, that states for each column:

1. What it measures (load factor required versus probability of exceeding it).
2. Its geography (system or Scotland).
3. Its numeric scale.

The ranges of the captured values are **not** evidence of scale. Until the hold lifts, the
silver output stays on disk and this page publishes no data values from it.

`nrapm_forecast_national_daily_days` and `nrapm_forecast_scotland_daily_days` are **eligible**
under the forward-target rule (RULINGS 529/542). The front matter's package-level
`eligibility: eligible` is the package registry entry. Holds are per family
(gridflow `@docs/neso_data_portal/eligibility.md`).

Related holds in the same batch: Daily OPMR (@daily-opmr.md) and Weekly OPMR (@weekly-opmr.md)
on issue-time and calendar questions; the 14-day wind current files
(@14-days-ahead-wind-forecasts.md) on past targets; the historic day-ahead wind archives
(@day-ahead-wind-forecast.md) on issue zone and availability. All are unit E-SEM.
