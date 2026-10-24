---
source: "neso_data_portal"
package: "demand-profile-dates"
dataset_key: "demand_profile_dates"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze"
eligibility: "eligible"
page:
  held: "NESO repeats some rows exactly, so no key tells rows apart; gridflow keeps the raw file."
  title: Demand profile dates
  summary: >-
    For each forecast day, the past day NESO picked to turn its cardinal-point demand forecast into
    half hours.
  facts:
    vendor: "NESO Data Portal, package Demand Profile Dates (`demand-profile-dates`): one CSV file"
    cadence: "Daily; NESO changed some past days' profile dates between 8 and 16 October 2026"
    grain: "Each row: a forecast date and the profile date chosen for it"
    history: "From the start of 2018 to 14 days ahead, NESO says"
  landscape: power
  what_it_is: >-
    NESO forecasts national demand at cardinal points: peaks, troughs and fixed times. It makes
    them half-hourly using a profile date, the past day it judges the
    closest match for weather, embedded generation, time of year, recurring calendar activity and
    special events. The file pairs each forecast date with its profile date, which NESO says can
    change as the day nears.
  how_used:
    - Explain the half-hourly shape of a NESO demand forecast by its profile date
    - Rebuild NESO's step from cardinal-point forecasts to half hours
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the CSV downloaded whole unless its
      `last_modified` is unchanged. Ingest only: gridflow builds no silver table.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=demand-profile-dates"
      - "GET https://api.neso.energy/dataset/11a2a8d3-3d65-4545-af02-be85e54db078/resource/48862d1a-f285-4709-a48c-1c0e8e7b37c3/download/profile_dates.csv"
    commands:
      - {run: gridflow ingest neso_data_portal demand_profile_dates --last 24h, comment: "whole CSV, bronze only"}
    sample:
      file: profile_dates.csv
      caveat: "In this 16 October 2026 file, eight later dates repeat in full; nothing tells copies apart."
  related:
    - {dataset: neso_data_portal/1-day-ahead-demand-forecast, note: "NESO's day-ahead cardinal-point forecast, which these dates turn into half hours"}
    - {dataset: neso_data_portal/2-14-days-ahead-national-demand-forecast, note: "Cardinal points 2 to 14 days ahead, the reach of these dates"}
    - {dataset: neso_data_portal/day-ahead-half-hourly-demand-forecast-performance, note: "How NESO's half-hourly day-ahead forecast scored against outturn"}
    - {dataset: neso_data_portal/historic-demand-data, note: "Half-hourly demand outturn of the past days chosen here, once filled"}
---

# Demand Profile Dates

A two-column lookup. Each row pairs a demand-forecast **target date** (`FORECAST_DATE`) with
the **historical analogue date** (`PROFILE_DATE`) that NESO picked for it. NESO forecasts
national demand at a small set of cardinal points (the daily peaks, troughs and turning points;
see @./1-day-ahead-demand-forecast.md and @./2-14-days-ahead-national-demand-forecast.md). It
turns those points into a half-hourly demand curve by borrowing the shape of a past day. The
package description says the profile date is NESO's estimate of the historic date "which will
most closely match" the target day. The match covers weather, embedded generation, time of
year, recurring calendar activity and special events. The vendor says the file runs from the
start of 2018 up to 14 days ahead. The choice is **revisable**: "These dates can change as we
get closer to real time". It is not a profile-class or day-type list. It records which
analogue lies behind the half-hourly shape of a published forecast. That helps when you
explain forecast-shape errors or rebuild NESO's profiling step.

**Read this first.** This family is **captured in bronze but not loaded to silver**. It has
**no registry record**, so no transformer runs. There are no silver rows, no silver views and
no `_latest` view. The reason is in RULINGS 538. The vendor file repeats identical rows: 3,224
rows hold only 3,216 distinct `(FORECAST_DATE, PROFILE_DATE)` pairs. The engine's
duplicate-key guard rejects a capture with repeated keys, and no column set avoids the
repeats, because the repeated rows are identical in full. gridflow forbids silent
deduplication, so the family stays ingest-only (class 3) until the blocker is settled (see
Identity). The site page shows the header and first eight lines of NESO's 16 October 2026 file,
as fetched, and no table.

- Publisher group: Demand
- Registry group: demand · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Demand Profile Dates | CSV | upload | `48862d1a-f285-4709-a48c-1c0e8e7b37c3` |

The package has one resource. It has no DOC, GIS, COVERED or ingest-only files (K-DEM-2-FACTS
§1, "`_files` / DOC scope").

| Resource | Disposition | Download |
|---|---|---|
| Demand Profile Dates (CSV, `datastore_active: true`) | SILVER → `demand_profile_dates` (**not realised**: no record, `transformer: null`) | [profile_dates.csv](https://api.neso.energy/dataset/11a2a8d3-3d65-4545-af02-be85e54db078/resource/48862d1a-f285-4709-a48c-1c0e8e7b37c3/download/profile_dates.csv) |

- Package id `11a2a8d3-3d65-4545-af02-be85e54db078`; version 1.0; created 2024-04-23. The
  catalogue snapshot `20261006T195819Z` lists no author. Its tags are Dates, Demand,
  Forecast, Historical, Profile and Subscribable.
- Vendor dataset page: <https://www.neso.energy/data-portal/demand-profile-dates>.
- **Implementation delta, reconciled.** The registry JSON gives the package `eligibility:
  eligible` and the resource a `SILVER` disposition. The eligibility report
  (`docs/neso_data_portal/eligibility.md`) lists the family as "ingest-only (no silver
  output)". The code has no record (`registry.families["demand_profile_dates"].record is
  None`). The three agree once you read RULINGS 538. Eligibility (licence and format) is
  satisfied, and the SILVER disposition shows the intended target. The duplicate rows alone
  keep a record from being written.

## Families

### `demand_profile_dates`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no
- ingest-only: no silver yet

Bronze schema, epoch 1 (exact header H-DPD: `FORECAST_DATE`, `PROFILE_DATE`):

| Vendor column | Proposed silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| FORECAST_DATE | `forecast_date` | date | `%Y-%m-%d` | no (0 blanks observed) | TODO: verify | — (dictionary `unit: ""`) |
| PROFILE_DATE | `profile_date` | date | `%Y-%m-%d` | no (0 blanks observed) | TODO: verify | — (dictionary `unit: ""`) |

The silver column names are the FACTS T01 **proposal**. Nothing exists in silver under these
names. Both columns parse fully as `%Y-%m-%d`, with zero cast failures over all 3,224 rows
(FACTS §3). The vendor dictionary types both fields as `date`. It gives `FORECAST_DATE` as
"The date for which the profile date was used" and `PROFILE_DATE` as "The profile date that
has been chosen for that forecast date".

#### The two clocks (proposed, not applied)

No record exists, so neither clock is stamped on any row. The FACTS research proposes the
following recipe. A future record would apply it.

- **Vintage clock (`ckan_last_modified`).** `available_at` = `published_at` = the CKAN
  `last_modified` of the resource at the moment gridflow captured it. Every row of one capture
  would carry the same value. The activation capture's sidecar records
  `ckan_last_modified = 2026-10-07T15:15:05.280419`. The earlier catalogue snapshot
  (`20261006T195819Z`) shows `2026-10-06T15:15:03.644743`. That is one daily update before the
  capture, so the two values differ. This is the time NESO last replaced the file. It is
  not the time any single analogue was chosen. The resource is an `upload`, and the body has
  no issue-time column. The vendor states that the dates are revised, so no immutable issue
  time can be read from the file (FACTS g2).
- **Event clock (`temporal: none`).** In plain terms, there is no event-time recipe:
  `timestamp_utc` would be the **capture time**, not either date in the row. This does not
  claim that the capture time is the date the row represents. `FORECAST_DATE` and
  `PROFILE_DATE` would stay as separate typed `date` columns (FACTS T01; ADR-036). A UTC
  instant is not built because the vendor gives no timezone and no day boundary for either
  date. TODO: verify with NESO which timezone and day boundary the two dates use, for
  example whether they are GB local calendar days.

#### Units

Neither column has a unit. Both are calendar dates, and the vendor dictionary leaves `unit`
empty for both. There are no numeric value columns (FACTS g4).

#### Sentinels and missing values

The research census (FACTS §3 g5) found **zero** blank, `-1`, `N/A`, `NA` or literal-zero
cells in the inspected body. A future record should add no null-token mappings.

#### Identity and the blocker

Measured uniqueness in the activation capture (FACTS §3, C-B):

| Candidate key | Rows | Distinct keys | Duplicate excess |
|---|---:|---:|---:|
| `FORECAST_DATE` | 3,224 | 3,216 | 8 |
| `(FORECAST_DATE, PROFILE_DATE)` | 3,224 | 3,216 | 8 |

- Both candidates fail the same way, so every repeated target date is a **byte-identical
  row**, not a conflicting analogue. In the activation capture seven target dates repeat: six
  appear twice and one appears three times. All of them fall in the most recent weeks of the
  file. FACTS §3 lists the exact pairs. The 2026-10-16 capture still repeats all seven and adds
  an eighth, 2026-10-08 (twice): 3,234 rows, 3,225 distinct, again identical in full. No column set separates the repeats, because the file has only these two
  columns.
- The vendor gives no uniqueness guarantee (FACTS g3, T02). The CKAN resource declares no
  `datastore_unique_keys` in the snapshot.
- The `whole_capture` `_latest` mode does **not** bypass the generic engine's duplicate-key
  guard (`src/gridflow/silver/neso_data_portal/casting.py:531-534`). A record would therefore fail
  every capture.
- Dropping the repeats in silence, or adding an ordinal key, is forbidden (RULINGS 538).
- **What settles it** (FACTS §3, "Consequence"): (a) NESO publishes a corrected body without
  identical repeats; (b) NESO names a missing discriminator, such as a forecast-run or issue
  column; or (c) a separately approved engine policy for exact-duplicate rows. TODO: verify
  with NESO whether the repeated rows are intended, and what would tell them apart, or
  whether they are a publishing defect.
- Repo pin: `tests/unit/test_neso_dem2_records.py::test_demand_profile_dates_has_no_record`
  fails if a record is added without revisiting this ruling.

#### Bronze at activation

| Property | Value |
|---|---|
| Captures | 1 at activation; a second on 2026-10-16 (see Cadence) |
| File | `C:/gridflow-data/bronze/neso_data_portal/demand_profile_dates/2026/10/08/raw_20261008T100618Z_48862d1a-f285-4709-a48c-1c0e8e7b37c3_7a8ab7c3.csv` |
| Bytes · rows | 74,184 · 3,224 |
| Written | 2026-10-08T10:06:18Z (sidecar SHA-256 verified, FACTS C-M) |
| Silver | **none.** Not transformed at the DEM-2 activation (cutoff 2026-10-08). There is no silver directory and no row count |
| Reconcile | `--all --cutoff 2026-10-08`: exit 0, 0 gaps over 41 families. This family stays ingest-only (v0.22-RESULTS §DEM-2) |

The CKAN `datastore_search` total read at 2026-10-08T12:19Z was 3,224, the same as the CSV
capture's row count. TODO: verify whether the datastore table carries the same repeated rows
as the CSV download.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

The vendor updates the file daily and documents that profile dates can change as real time
approaches. Each daily capture is therefore its own vintage, and an older capture can hold a
different analogue for the same target date.

A second capture exists: `raw_20261016T200228Z_48862d1a-f285-4709-a48c-1c0e8e7b37c3_569dae35.csv`
(74,414 bytes, 3,234 rows, same header, CKAN `last_modified` `2026-10-16T15:15:04.513916`), forecast
dates 2018-01-01 to 2026-10-30, no date missing. Against the first: every target date up to
2026-10-07 keeps its analogue; nine target dates from 2026-10-08 to 2026-10-18 changed analogue
(for example 2026-10-08 from 2024-10-03 to 2025-09-30); nine new dates run 2026-10-22 to
2026-10-30. Several of the changed dates (2026-10-08 to 2026-10-15) were already past when the
second file was published, so the file changes after the day as well as "closer to real time".
`TODO: verify` with NESO whether a past date's profile date is the one finally used. Neither
capture gives one target date two different analogues.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: <https://www.neso.energy/data-portal/ngeso-open-licence>. Any derived output
must carry the attribution line above verbatim.

## Holds

- none

There is no held silver output because there is **no silver output at all**. The family is
blocked structurally (class 3, RULINGS 538) by the identical-row repeats described under
Identity. It is not an E-SEM semantics hold, and it has no hold question. It is settled by
one of the three routes listed there. Until then, the data exists only as immutable bronze
captures.

## References

- @../README.md — NESO Data Portal vendor page (CKAN, file-download model)
- @./1-day-ahead-demand-forecast.md · @./2-14-days-ahead-national-demand-forecast.md — the cardinal-point forecasts these analogue dates shape
- @./historic-demand-data.md · @./daily-demand-update.md — demand siblings
- gridflow `docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (vintage clock), `ADR-034-neso-generic-silver-engine.md` (generic engine, `_latest`), `ADR-036-neso-profiler-and-pilot-records.md` (`temporal: none`)
- gridflow `.planning/phases/v0.22-K-DEM-2/K-DEM-2-FACTS.md` §1, §2, §3 and `K-DEM-2-SPEC.md`
- gridflow `.planning/v0.22-RESULTS.md` §DEM-2; RULINGS 538, 540, 541
- gridflow registry `src/gridflow/connectors/neso_data_portal/registry/demand-profile-dates.json`; eligibility report `docs/neso_data_portal/eligibility.md`
- gridflow `tests/unit/test_neso_dem2_records.py` (no-record pin)
