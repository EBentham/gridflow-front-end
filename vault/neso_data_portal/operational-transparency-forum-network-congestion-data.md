---
source: "neso_data_portal"
package: "operational-transparency-forum-network-congestion-data"
dataset_key: "otf_network_congestion"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Operational Transparency Forum - Network congestion data

NESO's weekly table of **transmission boundary constraint limits** as presented at the
Operational Transparency Forum (OTF). Each row is one date. The columns are 11 named GB
transmission boundaries (B6, B7, B9, B15 and others, see below), each with an **Actual** and a
**Forecast** column in the same row. All 22 value columns are in **MW**. The package notes
describe it as "weekly constraint limits (MW) for major transmission boundaries, spanning a
rolling six-month window forward and backward" as presented in OTF. The captured body runs from
2026-04-11 to 2027-04-11 (53 rows) against a CKAN `last_modified` of 2026-10-07, which is about
six months either side.

NESO describes the columns as boundary constraint limits in MW (vendor dictionary; Actual and
"forecasted ( YA/MT)" wordings are quoted under Families below). `TODO: verify` what a boundary
limit physically denotes and how it relates to constraint costs. Related NESO packages, for
orientation only: @thermal-constraint-costs.md and @24-months-ahead-constraint-limits.md.

**This family is held (unit E-SEM).** The table mixes populated Actual columns with blank ones
and carries no issue or publication column. The semantics of `Date` are not established, and the
body fails the forward-target rule of RULINGS 529: 26 of its 53 target dates are on or before the
vintage date. Silver exists, but nothing here is eligible for publication or point-in-time model
use. This page therefore gives schema, clocks, counts and structure only, and **no data values**.
See Holds.

OTF's own explanation (NESO document 383631, [OTF boundary and forecast
explanation](https://www.neso.energy/document/383631/download)) describes a nearer-term forecast
view updated weekly and a longer-term forecast view after that. It does not describe a simple
week-ahead forecast against actual table. `TODO: verify` which view each column family
corresponds to. The vendor dictionary labels the Forecast columns "forecasted ( YA/MT)", and the
abbreviation is not expanded anywhere in the captured dictionary.

Related pages in the same constraint-management batch:

- @24-months-ahead-constraint-limits.md: weekly limits for a 24-month horizon, a different
  boundary code set. The exact boundary codes shared with this table: none (see Boundary
  identifiers).
- @day-ahead-constraint-flows-and-limits.md: half-hourly day-ahead limits and flows by
  constraint group. Its capture is adjudicated **failed** (duplicate entity keys, ADR-040) and
  has **0** silver rows.
- @thermal-constraint-costs.md, @voltage-requirement.md and
  @constraint-management-intertrip-service-information-cmis.md complete the batch.

- Publisher group: Constraint management
- Registry group: constraint-management · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Network congestion Forecast and Actual data | CSV | upload | `aa9d4303-b7ec-4881-be07-16bad8824ab6` |

The package has **one** resource, and it is SILVER. There are no DOC resources, so there is no
`_files` family and no PDF or workbook methodology to link. Package id
`a30dacc7-af6e-465b-ad96-eb2383376ac9`. The resource is `datastore_active` in CKAN.

- **Network congestion Forecast and Actual data** → `otf_network_congestion` (held).
  Download as captured: [otf_constraint_data_07-10-2026.csv](https://api.neso.energy/dataset/a30dacc7-af6e-465b-ad96-eb2383376ac9/resource/aa9d4303-b7ec-4881-be07-16bad8824ab6/download/otf_constraint_data_07-10-2026.csv).
  Bronze: `raw_20261008T111609Z_aa9d4303-b7ec-4881-be07-16bad8824ab6_dae26846.csv`, 5,706 bytes,
  53 data rows, one header epoch, fetched 2026-10-08T11:16:09 UTC.

**The filename is date-stamped and changes with each upload.** The 2026-10-06 catalogue snapshot
recorded `otf_constraint_data_30-09-2026.csv` (CKAN `last_modified` 2026-09-30T07:31:28), and the
2026-10-08 capture recorded `otf_constraint_data_07-10-2026.csv` (`last_modified`
2026-10-07T10:43:02). The resource id is stable across both. Resolve the current URL from the
CKAN resource record and never hard-code the filename. The date token in the name is not a
documented issue instant (see Clocks).

## Families

### `otf_network_congestion`

- Kind: tabular · archetype: FC · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| Min of B4 B5 - Actual | `min_of_b4_b5_actual` | float64 | — | yes | — | MW |
| B6 - Actual | `b6_actual` | float64 | — | yes | — | MW |
| B6a - Actual | `b6a_actual` | float64 | — | yes | — | MW |
| B7 - Actual | `b7_actual` | float64 | — | yes | — | MW |
| GMSNOW - Actual | `gmsnow_actual` | float64 | — | yes | — | MW |
| LE1 - Actual | `le1_actual` | float64 | — | yes | — | MW |
| B9 - Actual | `b9_actual` | float64 | — | yes | — | MW |
| DRESHEX - Actual | `dreshex_actual` | float64 | — | yes | — | MW |
| EC5 - Actual | `ec5_actual` | float64 | — | yes | — | MW |
| B15 - Actual | `b15_actual` | float64 | — | yes | — | MW |
| SC - Actual | `sc_actual` | float64 | — | yes | — | MW |
| Min of B4 B5 - Forecast | `min_of_b4_b5_forecast` | float64 | — | yes | — | MW |
| B6 - Forecast | `b6_forecast` | float64 | — | yes | — | MW |
| B6a - Forecast | `b6a_forecast` | float64 | — | yes | — | MW |
| B7 - Forecast | `b7_forecast` | float64 | — | yes | — | MW |
| GMSNOW - Forecast | `gmsnow_forecast` | float64 | — | yes | — | MW |
| LE1 - Forecast | `le1_forecast` | float64 | — | yes | — | MW |
| B9 - Forecast | `b9_forecast` | float64 | — | yes | — | MW |
| DRESHEX - Forecast | `dreshex_forecast` | float64 | — | yes | — | MW |
| EC5 - Forecast | `ec5_forecast` | float64 | — | yes | — | MW |
| B15 - Forecast | `b15_forecast` | float64 | — | yes | — | MW |
| SC - Forecast | `sc_forecast` | float64 | — | yes | — | MW |

- Entity key: `date`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the capture's CKAN
   `last_modified`, `2026-10-07T10:43:02.910511`. CKAN emits it without an offset, and gridflow
   reads it as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`).
   Every row of the capture shares this vintage. The file has **no issue column**, so the
   vintage is the only availability clock. The filename date token (`07-10-2026`) is a name, not
   a documented publication instant, and is not used as a clock. `issue.kind` is `none`.
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` = `event_time` = the **UK-local
   midnight starting `date`, expressed in UTC**. That is 23:00 UTC on the previous calendar day
   when the date is in BST, and 00:00 UTC when it is in GMT. The first silver row, dated
   2026-04-11, carries `timestamp_utc` 2026-04-10T23:00:00Z. Checked on all 53 silver rows
   (2026-10-10): the only UTC hours present are 00 and 23, `event_time` equals `timestamp_utc`
   on every row, and `timestamp_utc` does **not** equal the capture time. This is an engine
   storage anchor, not a vendor claim that `Date` denotes a midnight instant. Whether `Date`
   labels the start of a week, the end of a week or a reporting day is the open hold question.
   The `none` temporal fallback (timestamp_utc = capture time) does not apply to this family.

**Hold question.** `Date` has no vendor description (the dictionary entry for it has an empty
description and an empty unit). The body has these structural facts:

- 53 distinct dates, 2026-04-11 through 2027-04-11, no duplicates.
- Date steps: 51 intervals of 7 days and **one of 8 days** (2026-12-26 to 2027-01-03).
- Weekday of the label: **38 Saturdays, then 15 Sundays**. The switch from Saturday to Sunday
  falls at the 8-day step, on 2027-01-03.
- 26 dates are on or before the vintage date 2026-10-07, and 27 are after it.
- **Actual columns:** 27 rows have all 11 Actual columns populated, 2026-04-11 through
  2026-10-10. The 26 rows from 2026-10-17 to the end have **every** Actual column blank. The
  last populated Actual row (2026-10-10) is three days after the vintage date, which a plain
  reading of "actual" does not explain.
- **Forecast columns** are populated on all 53 rows, including the 26 earliest dates that sit
  on or before the vintage. Those are therefore retrospective forecast values, not forecasts
  available at the capture time.

`TODO: verify` with NESO: whether `Date` is a week start, week end or reporting label and why
the weekday of the label changes; how each Actual value is calculated (for example a minimum
over the week); whether the Forecast value in a past row is the value published at the time or
a rebuilt one; and when each forecast was issued. A single capture cannot show how a later
capture revises a prior forecast row or fills a blank Actual. `TODO: verify` this against a
second capture.

**Boundary identifiers.** Each paired label appears as `<label> - Actual` and
`<label> - Forecast`: Min of B4 B5, B6, B6a, B7, GMSNOW, LE1, B9, DRESHEX, EC5, B15, SC (11
labels). They are stored as column names with the vendor spelling lower-cased, and carry no
BM-unit or EIC codes. The labels are not normalised or aliased.

NESO's OTF document presents these aliases: `B6 (SCOTEX)`, `B7 (SSHARN)`, `FLOWSTH (B9)`,
`LE1 (SEIMP)` and `B15 (ESTEX)`. They are reference relationships only, and **gridflow does not
use them to join or merge anything**. Exact-string comparison of the 11 labels against the code
sets of its neighbours in this batch found **no shared code** with the 24-month limits (12
codes), the day-ahead constraint groups (31 codes) or the thermal constraint groups (6 codes),
because those tables name boundaries by other spellings (for example `SCOTEX`, `ESTEX`,
`DRESHEX1`). Do not merge `DRESHEX` with `DRESHEX1`, or any similar pair. `TODO: verify` a
vendor crosswalk with applicability dates before any join.

**Units (vendor dictionary only: CKAN datastore field info for resource `aa9d4303…`, snapshot
20261006T195819Z; [package page](https://www.neso.energy/data-portal/operational-transparency-forum-network-congestion-data),
[resource dictionary](https://www.neso.energy/data-portal/operational-transparency-forum-network-congestion-data/network_congestion_forecast_and_actual_data)).**
All 22 value columns carry `unit: MW` and dictionary type `numeric`, and are cast to float64.
The Actual columns are described as "Actual `<boundary>` boundary constraint limit", and the
Forecast columns as "forecasted ( YA/MT) `<boundary>` boundary constraint limit". The two
`Min of B4 B5` columns are described as the minimum of the B4/B5 boundary limits. `Date` has no
unit. No unit is inferred from a column name.

**Sentinels and missing values (FACTS g5).** The 11 Actual columns each contain exactly **26
blank cells**, always the same 26 rows (the dates from 2026-10-17). The 11 Forecast columns
contain no blank cells and no `NA`, `N/A` or `-1` tokens, and no zero cells. No null-token map is
declared. Blanks load as nulls, and the columns are nullable. A vendor guarantee that every
blank means "not yet actual" is `TODO: verify`. No bound is imposed on any value.

**Identity.** `date` was measured unique across the full body. No vendor text declares it a
contractual key, so the entity key is a capture guard and `_latest` is `whole_capture`: the
newest capture wins as a whole. `TODO: verify` the vendor revision key. History across uploads
exists only in the dated silver captures.

**Silver shape.** One Parquet file under `year=2026/month=10` in
`C:/gridflow-data/silver/neso_data_portal/otf_network_congestion/`, **53 rows by 31 columns**: the
23 vendor columns above plus `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`. All
timestamps are tz-aware UTC. `dataset_version` is `1+e1` (record version 1, epoch 1).

**Activation (2026-10-10, master `49f7c1a`).** Cutoff 2026-10-08, one capture: **53 rows**, equal
to the planned count. No prior silver existed, so nothing was overwritten. Reconcile
`--all --cutoff 2026-10-08` exited 0 over 105 families with 0 gaps, 15 adjudicated and 0 stale
(gridflow `@.planning/v0.22-RESULTS.md` §CON; RULINGS 630, 632, 634, 635; verification at
`@.planning/phases/v0.22-K-CON/VERIFICATION.md`).

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Weekly

"Weekly" is the only vendor statement of cadence. The two uploads observed (CKAN `last_modified`
2026-09-30 and 2026-10-07) are seven days apart, consistent with it, but two points do not
establish a schedule. `TODO: verify` the upload day and time, and whether each upload replaces
the whole rolling window (the captured body suggests so). Captures to date were on demand;
`config/sources.yaml` declares a `schedule: "daily"` value for `otf_network_congestion`, which is
a different cadence again from the registry's weekly refresh. `TODO: verify` which, if any,
scheduled refresh is in force. An upload that lands between two captures is lost, so the
dated silver captures are a sample of the vendor's history, not the full history.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `otf_network_congestion`: held: TODO: is Date a week start, week end or reporting label (38 Saturdays, 15 Sundays, one 8-day step), how are actuals calculated, and when was each forecast issued? 26 targets are on or before the vintage, so the forward-target test fails. (unit E-SEM)

The held output exists in silver, but it is not eligible for publication or point-in-time model
use until unit E-SEM answers its question (RULINGS 529, 632). This page publishes its schema,
clocks and row count only.

- **What fails the forward-target test.** 26 of the 53 targets are on or before the vintage
  date. With no issue column, nothing shows when each value was available. The Forecast values
  on those 26 rows are retrospective, so the capture vintage cannot stand in for an issue time
  (ADR-035; RULINGS 529). These results apply to the captured body. Later captures roll the
  window forward and may differ.
- **What would lift the hold:** vendor answers to the three questions above (the meaning of
  `Date` and of the 7-then-8-day weekday step, the Actual calculation, and the issue time of
  each Forecast value), plus evidence that a published row is immutable or that revisions are
  versioned. A narrower fix would be to keep only rows whose target is after the vintage, which
  would leave the 27 later dates. That filter would be a design decision for unit E-SEM, not a
  current behaviour, and it would not answer the `Date` semantics question.
- **Not a downstream gap:** there is no gold view. No gridflow_models consumer is recorded for
  this family (`TODO: verify`).

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. The hold is per family, and this package's only family is held.
