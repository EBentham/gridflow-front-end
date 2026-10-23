---
source: "neso_data_portal"
package: "14-days-ahead-operational-metered-wind-forecasts"
dataset_keys: ["metered_wind_forecast_14d", "metered_wind_forecast_14d_windfarm"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
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
Each file covers the next 14 days at half-hour resolution. The current capture runs from the
first settlement period after publication to about 14 days out (670 half-hours). Use the
national series as a medium-horizon wind feature or benchmark against Elexon WINDFOR
(@../../elexon/datasets/windfor.md), and the windfarm series for regional or unit-level wind
features (@../../../20-domain/modelling/renewable-and-demand-forecasting.md). The captured
national file holds a single forecast issue, with no archive of earlier issues, and gridflow
keeps only the forecast present at capture time.
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
  2026-10-08 capture). CKAN datastore active.
  Captured: `raw_20261008T111216Z_b1ae17c2-cc5e-4254-9bbf-3eddcf30d033_418a1a40.csv`,
  50,151 bytes, 670 data rows, one header epoch (H-A), CRLF line endings, no BOM.
- 14 Day Ahead Operational Metered Windfarm-Level Wind Forecast → `metered_wind_forecast_14d_windfarm`.
  Download as captured: [14da_windunit_forecast_20261008_1115.csv](https://api.neso.energy/dataset/ca6fc361-9099-4ab2-ac02-c959431e84bc/resource/31e6d895-af48-41bd-a4db-28a78c7e9c4b/download/14da_windunit_forecast_20261008_1115.csv).
  The file name carries a date-time token and changes with each publication. The 2026-10-06
  catalogue snapshot listed `14da_windunit_forecast_20261006_2015.csv` for the same resource
  id. The stable handle is the resource id, not the URL. CKAN datastore active.
  Captured: `raw_20261008T111220Z_31e6d895-af48-41bd-a4db-28a78c7e9c4b_bfebc077.csv`,
  19,603,927 bytes, 182,240 data rows, one header epoch (H-B), CRLF line endings, no BOM.

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
   `last_modified` of the captured resource. For the one capture to date that is
   `2026-10-08T10:16:12.426355`, which CKAN emits without an offset. gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All 670 silver rows
   share this one vintage.
2. **Event time (`utc_instant` on `datetime`).** `timestamp_utc` = `event_time` = `datetime`,
   the target half-hour. Checked on every silver row on 2026-10-09. The vendor labels
   `Datetime` "ISO 8601 (UTC)". Every row's `Datetime` equals the **start** of its
   `Date`/`Settlement_Period` under the UK settlement-day convention, with zero offset (FACTS
   T01, g1). So `datetime` is the period **start**, not the end, even though the vendor's
   settlement-period comment describes SP1 as the half hour *ending* 00:30 UK time. Event time
   is **not** the capture time.

**Issue time.** This family has a per-row production clock. `ForecastDatetime` is the vendor's
"date and time of when the forecast is produced", unit "ISO 8601 (UTC)". The record maps it to
`issue_time` (silver keeps both `forecast_datetime` and `issue_time`, equal). The capture holds
**one** issue, `2026-10-08T09:52:34Z`, shared by all 670 targets (FACTS GEN1-1). It sits 24
minutes before the CKAN vintage. The vintage, **not** the issue time, drives `published_at` and
`available_at`. gridflow does not use `issue_time_evidenced`, because no source shows that a
forecast was available at its stated production instant, or that published values never change
after it (FACTS g2). `TODO: verify` issue immutability and availability at `ForecastDatetime`.

**Why this family is eligible (forward-target rule, RULINGS 529 / 542).** Every target in the
capture is after the capture's CKAN `last_modified`. The earliest target is
2026-10-08T10:30:00Z against a vintage of 2026-10-08T10:16:12Z. No target row sits at or
before the vintage (FACTS GEN1-1). The forecast was therefore public at the vintage instant,
before any of its targets began, so the vintage is a valid conservative availability clock.
gridflow pins this property in
`@tests/unit/test_neso_gen1_records.py::test_eligible_fixture_targets_are_after_the_capture_vintage`,
and the production instant in `::test_national_issue_columns_declare_the_production_instant`.
Eligibility is conditional on later captures keeping the property. The sibling ordinary
14-day package (@14-days-ahead-wind-forecasts.md) fails it and is held.

**Horizon of the captured file.** 670 consecutive half-hours, 30 minutes apart, from
2026-10-08T10:30Z (`date` 2026-10-08, SP 24) to 2026-10-22T09:00Z (`date` 2026-10-22). The file
starts at the next settlement period after publication, not at midnight. The settlement periods
observed run 1–48. The record allows 1–50. No clock-change day fell inside this capture
(the 2026 autumn change is 25 October), so DST-day behaviour (46 or 50 periods) is unobserved.
`TODO: verify` how the vendor labels `Datetime` and `Settlement_Period` across a clock change.

**Units (vendor dictionary only).** `Capacity` and `Wind_Forecast` are **MW**, both declared in
the resource's datastore dictionary (FACTS g4). The dictionary describes `Capacity` as the total
operational wind capacity connected to the National Grid transmission network, and
`Wind_Forecast` as the forecast for each half-hourly settlement period. `Settlement_Period` is an
index and `Date` a settlement-date label. Neither carries a physical unit. In this capture
`capacity` is the same value in every row (26,738 MW), and every `wind_forecast` value is a
whole number. The forecast ranges from 2,716 to 21,464 MW across the 14 days.

**Sentinels and missing values (FACTS g5).** The record declares no null token. Full-body
checks found no `N/A`, `NA`, literal `-1` or numeric −1 and no blank cells. Silver has **no
nulls** in any column. The national file has no zero values and no negatives.

**Identity and selection.** The entity key is `(datetime, issue_time)`. In the capture both
`datetime` alone and `(datetime, issue_time)` have zero duplicates (FACTS T05). No vendor text
documents a contractual key or revision grain. `TODO: verify` the vendor's revision key.
`_latest` is `whole_capture`: the newest capture replaces the previous one as a whole.

**Relation to the windfarm file.** Summed over all windfarm rows for each target,
the windfarm `wind_forecast` matches the national value to within 0.5 MW in all 670 targets
(mean absolute difference 0.24 MW), and windfarm `capacity` sums to the national 26,738 MW to
within 0.2 MW. Measured on 2026-10-09 silver. This is consistent with the national file being
the rounded sum of the windfarm file. No vendor text states it.
`TODO: verify` with the vendor that the national figure is defined as the windfarm sum.

**Activation (2026-10-09, master `f19effb`, PR #92).** Transformed at cutoff 2026-10-08 (one
capture): **670 silver rows**, equal to the planned count. No prior silver existed, so nothing
was overwritten. Reconcile `--all --cutoff 2026-10-08` exited 0 with 0 gaps over 55 recorded
families (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1; RULINGS 545–546).

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
   `last_modified` of the captured resource, `2026-10-08T10:16:24.243581` (offset-less, read as
   UTC per ADR-030). All 182,240 silver rows share this one vintage. It is 12 seconds after the
   national file's vintage.
2. **Event time (`utc_instant` on `datetime`).** `timestamp_utc` = `event_time` = `datetime`,
   the UTC **start** of the target half-hour (vendor unit "ISO 8601 (UTC)"; zero measured offset
   from settlement start, FACTS T01). Checked on every silver row on 2026-10-09. It is not the
   capture time.

The record's issue recipe is `none`. Unlike the national file, the windfarm file has **no
production-time column**. The date-time token in the file name (`20261008_1115`) is not
evidenced as an issue instant, so gridflow does not read one from it (FACTS
§`metered_wind_forecast_14d_windfarm`). The vintage is the only availability clock.

**Why this family is eligible (forward-target rule, RULINGS 529 / 542).** Every target is
after the CKAN vintage: earliest target 2026-10-08T10:30:00Z against a vintage of
2026-10-08T10:16:24Z, zero rows at or before it (FACTS GEN1-1). Pinned by the same test as the
national family. Eligibility is conditional on later captures keeping the property.

**Layout of the captured file.** 272 windfarms × 670 half-hours = 182,240 rows. Every
generator has exactly 670 rows, covering the same targets as the national file (2026-10-08
SP 24 to 2026-10-22, 30-minute steps, SP 1–48 observed). Each `generator_name` maps to exactly
one `generator_full_name` and one `region` (272 distinct name/full-name/region triples) and has
one constant `capacity` across the horizon.

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

- `capacity` = 0 in 1,340 rows; `wind_forecast` = 0 in 4,598 rows.
- 2 windfarms have zero capacity for the whole horizon, and 3 have a zero forecast for the
  whole horizon (the longest zero run, 670 half-hours, is a whole generator).
- Zero forecasts also occur where capacity is positive.
- No row has `wind_forecast` above `capacity`.

No vendor source says a zero means missing, unavailable or not applicable.
`TODO: verify` the vendor's meaning of zero capacity and zero-forecast runs.

**Identity and selection.** The entity key is `(datetime, generator_name)`, with zero duplicates
over the complete body (FACTS T04). No vendor text documents it as a contractual key.
`TODO: verify` the vendor's revision key. `_latest` is `whole_capture`.

**Activation (2026-10-09, master `f19effb`, PR #92).** Transformed at cutoff 2026-10-08:
**182,240 silver rows**, equal to the planned count, with no prior silver overwritten. Reconcile
reported 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` §GEN-1; RULINGS 545–546). Silver
carries the same lineage/clock columns as the national family, without `issue_time`.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

The vendor gives no publication time of day. The one capture to date has CKAN `last_modified`
values of 10:16 UTC (11:16 BST) for both resources, and the national forecast was produced at
09:52:34 UTC. The 2026-10-06 snapshot showed both resources last modified at about 19:16 UTC,
and a windfarm file name token of `20261006_2015`. So publication is not at a fixed time of day,
or happens more than once a day.

- `TODO: verify` the vendor's publication schedule and whether a day can carry more than one
  issue. gridflow captures once per refresh run, so any intermediate issue is missed. Each
  capture keeps only the forecast present at capture time.
- `TODO: verify` whether the windfarm file-name token is the publication clock time (it reads
  11:15 against an 11:16 BST `last_modified`). gridflow does not rely on it.
- Captures to date: one per family (2026-10-08). No scheduled refresh has run yet.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

Both families are **eligible** under the forward-target rule (RULINGS 529, applied to GEN-1 by
RULINGS 542). The remaining open items (issue immutability, vendor keys, zero semantics, DST-day
labelling) are `TODO: verify` notes, not holds. They do not block publication of these current
bodies.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`): the
ordinary 14-day national and BMU forecasts (@14-days-ahead-wind-forecasts.md) are held because
their current bodies contain targets at or before the CKAN vintage (3 and 693 rows). The
historic day-ahead wind archives (@day-ahead-wind-forecast.md) are held on issue-clock
questions. All are unit E-SEM.
