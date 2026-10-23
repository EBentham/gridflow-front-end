---
source: "neso_data_portal"
package: "7-day-ahead-national-forecast"
dataset_keys: ["national_forecast_7d_day_ahead_demand", "national_forecast_7d_historic_day_ahead"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# 7 Day Ahead Demand Forecast

NESO's seven-day-ahead forecast of GB **national demand (ND)**, published daily on the Open
Data Portal as two CSVs. The vendor defines ND as the GB generation requirement: the sum of
metered generation, excluding generation needed for station load, pump-storage pumping and
interconnector exports (resource description, catalogue snapshot 2026-10-06; FACTS C9). The
forecast is not a half-hourly curve. Each row is one **cardinal point (CP)** of the target day:
a fixed-time point, a trough (daily minimum) or a peak (daily maximum), with the CP's start and
end clock and, on four rows, a vendor "forecasting point" label (overnight minimum, daytime
peak, daytime minimum, evening peak). The vendor says the forecast helps the industry balance
supply and demand positions. For a model it is a medium-horizon view of the shape of a target
day's demand, and a baseline to score other forecasts against at seven days' lead.

The **current** file holds the newest forecast only: 12 cardinal points for one target date,
seven days ahead. It is **eligible**. Every target date in it lies after the file's CKAN
`last_modified`, so the capture vintage is a valid stand-in for issue time (RULINGS 529). The
**historic** file holds every 7-day-ahead forecast since 2018, per the vendor, with a
`FORECAST_TIMESTAMP` column the vendor does not define. It is **held** until that column's
meaning and clock are established (unit E-SEM; see Holds).

Related: the same cardinal-point layout is used by the 1-day (@1-day-ahead-demand-forecast.md),
2-day (@2-day-ahead-demand-forecast.md) and 2–14-day
(@2-14-days-ahead-national-demand-forecast.md) packages. Elexon's national demand forecasts
are @../../elexon/datasets/ndf.md (half-hourly) and @../../elexon/datasets/ndfd.md (daily
peak).

- Publisher group: Demand
- Registry group: demand · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| 7 Day Ahead Demand Forecast | CSV | upload | `70d3d674-15a6-4e41-83b4-410440c0b0b9` |
| Historic 7 Day Ahead Demand Forecasts | CSV | upload | `6f7408b4-47fd-4ae7-b1e5-f095a3a5a2dc` |

**7 Day Ahead Demand Forecast** (family `national_forecast_7d_day_ahead_demand`)

- Download (as captured 2026-10-08):
  [ng_demand_7da_20261014.csv](https://api.neso.energy/dataset/2b90a483-f59d-455b-be6d-3cb4c13a85d0/resource/70d3d674-15a6-4e41-83b4-410440c0b0b9/download/ng_demand_7da_20261014.csv)
  (CKAN datastore active).
- **The filename rotates.** It carries the target date and changes with each daily upload. The
  catalogue snapshot of 2026-10-06 pointed at `ng_demand_7da_20261013.csv`; the capture of
  2026-10-08 fetched `..._20261014.csv`, whose rows all target 2026-10-14. Resolve the URL from
  the resource id each run. Never hard-code the filename.
- Resource description (verbatim facts): publication frequency daily; publication time
  "between 16:15 and 17:00 (clock time)".
- Captured: `raw_20261008T111311Z_70d3d674-15a6-4e41-83b4-410440c0b0b9_419d233a.csv`,
  578 bytes, 12 data rows, one header epoch.

**Historic 7 Day Ahead Demand Forecasts** (family `national_forecast_7d_historic_day_ahead`)

- Download:
  [archive_7dayahead.csv](https://api.neso.energy/dataset/2b90a483-f59d-455b-be6d-3cb4c13a85d0/resource/6f7408b4-47fd-4ae7-b1e5-f095a3a5a2dc/download/archive_7dayahead.csv)
  (stable filename; CKAN datastore active).
- Resource description: "All historic 7 day ahead demand forecasts from 2018 to the most recent
  forecast."
- Captured: `raw_20261008T111319Z_6f7408b4-47fd-4ae7-b1e5-f095a3a5a2dc_61a5e08c.csv`,
  1,043,045 bytes, 15,703 data rows, one header epoch.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Demand Curve - Sample | PNG | upload | `2be09dad-2569-4fca-b4a9-92219e89c063` |

- Download:
  [cardinal-points.png](https://api.neso.energy/dataset/2b90a483-f59d-455b-be6d-3cb4c13a85d0/resource/2be09dad-2569-4fca-b4a9-92219e89c063/download/cardinal-points.png)
  (CKAN `last_modified` 2019-12-12T15:13:32.578659).
- Captured: `raw_20261008T111315Z_2be09dad-2569-4fca-b4a9-92219e89c063_cfff1cd9.png`,
  133,480 bytes, family `national_forecast_7d_files`. Catalogue only: no silver output. The
  vendor describes it as showing what time of day the different cardinal points occur.
  `TODO: verify` whether the image's CP times are UK clock or UTC; the image has not been read
  into this page.

## Families

### `national_forecast_7d_day_ahead_demand`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| DAYSAHEAD | `daysahead` | int64 | — | yes | — | — |
| TARGETDATE | `targetdate` | date | `%Y%m%d` | no | — | — |
| FORECASTDEMAND | `forecastdemand` | float64 | — | yes | — | MW |
| CARDINALPOINT | `cardinalpoint` | string | — | yes | — | — |
| CP_TYPE | `cp_type` | string | — | yes | — | — |
| CP_ST_TIME | `cp_st_time` | string | — | yes | — | — |
| CP_END_TIME | `cp_end_time` | string | — | yes | — | — |
| F_Point | `f_point` | string | — | yes | — | — |

- Entity key: `daysahead`, `targetdate`, `forecastdemand`, `cardinalpoint`, `cp_type`, `cp_st_time`, `cp_end_time`, `f_point`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`targetdate`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file. For the one capture to date that is
   `2026-10-07T15:15:00.672524`, which CKAN emits without an offset; gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`, D-15). All 12
   silver rows share this one vintage. The file has no issue column, so the vintage is the only
   availability clock.
   Observed, no inference drawn: 15:15 UTC is 16:15 BST, the start of the vendor's stated
   16:15–17:00 "clock time" publication window.
2. **Event time (`date_sp1` on `targetdate`).** `event_time` = `timestamp_utc` = the start of
   settlement period 1 of the target date, i.e. UK local midnight converted to UTC. For target
   2026-10-14 (BST) that is `2026-10-13 23:00 UTC` on every row (checked 2026-10-09). This is
   **not** the capture time, and it is **not** the instant of any cardinal point: it anchors
   the target calendar date only (FACTS T04, g1). The CP's position within the day is in the
   raw `cp_st_time` / `cp_end_time` strings, which are not parsed (see Units).

**Why it is eligible (RULINGS 529).** Every target date in the file is later than the date of
its CKAN `last_modified`: the capture's target 2026-10-14 is seven days after the vintage date
2026-10-07. A forecast published before the day it forecasts cannot be a hindsight value, so
the vintage is a conservative stand-in for issue time. The property is pinned by gridflow
`@tests/unit/test_neso_dem1_records.py::test_current_cp_targets_are_later_than_the_capture_vintage`,
which also proves the pin fails on a past target. A future capture with a target on or before
its vintage date would void this reasoning.

**Units (vendor dictionary only, field-info snapshot 2026-10-08, gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/national_forecast_7d_day_ahead_demand.json`).**

- `forecastdemand`: **MW** (dictionary `unit: MW`; FACTS C2, g4). It is national demand (ND),
  per the resource description, not transmission system demand (FACTS DEM1-1).
- `daysahead`: the forecast lead in days. The dictionary unit field is empty; its description
  says the number identifies the forecast day, e.g. `7` for the 7-day-ahead forecast (FACTS
  T01). All rows of the capture carry `7`.
- `cp_st_time`, `cp_end_time`: HHMM clock encodings, not quantities. The dictionary describes
  both as "Time UTC". FACTS g1 records that the dictionary's UTC statement conflicts with the
  UK-local alignment measured for medium-term families, so both are kept as raw strings.
  `TODO: verify` the zone of the CP clocks for this package with the vendor. Observed: the
  tokens are not zero-padded (`30`, `100`, `2400`), fixed-type points carry equal start and
  end, and the last fixed point carries `2400`.
- `cardinalpoint`, `cp_type`, `f_point`: categorical text. The dictionary lists `cp_type` as
  Fixed / Trough / Peak (`F` / `T` / `P` in the data). `TODO: verify` the full vendor
  definition of each cardinal-point code (the capture carries `1F`, `1S`, `1A`, `4`, `1B`,
  `2F`, `2A`, `2B`, `3B`, `3C`, `4B`, `4C`); the dictionary describes CPs in general terms only.
- `targetdate`: calendar date, no unit.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- A blank `F_Point` is kept as the vendor's **empty string** `""`, not converted to null
  (8 of the 12 rows). Only the four forecasting-point rows carry a label.
- No `NA` token occurs in this package.
- No zero or `-1` handling applies; no bounds are imposed on `forecastdemand`.
- Observed, unresolved: the dictionary comment defines the forecasting points as OM, DM, Dm,
  EM, with windows stated as "half hour ending" times; the data carries `Om`, not `OM`, for the
  overnight minimum. `TODO: verify` the casing is the same label, and the clock the "half hour
  ending" windows use.

**Identity and selection.** The entity key is **every column**: a capture-level duplicate
guard, not a revision identity (FACTS T05, g3; gridflow
`@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md`). The CP candidate
`(daysahead, targetdate, cardinalpoint)` was measured unique on the capture but is not frozen
as a business key, because no vendor text guarantees it across revisions. `_latest` is
`whole_capture`: the newest capture wins as a whole, which suits a file that holds one target
day. `TODO: verify` the vendor's revision identity for a CP forecast.

**Current versus archive.** All 12 rows of the current capture appear, equal on lead, target,
CP and value, in the historic archive captured the same morning (FACTS C4). The archive
therefore already carries the newest forecast. Every archive row in that correspondence had a
single `FORECAST_TIMESTAMP` per lead/target/CP.

**Bronze sample (eligible family; first rows of the capture, CRLF line endings):**

```text
"DAYSAHEAD","TARGETDATE","FORECASTDEMAND","CARDINALPOINT","CP_TYPE","CP_ST_TIME","CP_END_TIME","F_Point"
7,20261014,21787,"1F","F",30,30,""
7,20261014,21029,"1S","T",100,130,""
7,20261014,21144,"1A","P",200,230,""
```

**Silver sample (2 of 12 rows; engine columns abbreviated):**

```python
[
    {"daysahead": 7, "targetdate": date(2026, 10, 14), "forecastdemand": 18655.0,
     "cardinalpoint": "1B", "cp_type": "T", "cp_st_time": "430", "cp_end_time": "730",
     "f_point": "Om", "timestamp_utc": "2026-10-13T23:00:00+00:00",
     "published_at": "2026-10-07T15:15:00.672524+00:00", "dataset_version": "1+e1"},
    {"daysahead": 7, "targetdate": date(2026, 10, 14), "forecastdemand": 32262.0,
     "cardinalpoint": "4B", "cp_type": "P", "cp_st_time": "1830", "cp_end_time": "2000",
     "f_point": "EM", "timestamp_utc": "2026-10-13T23:00:00+00:00",
     "published_at": "2026-10-07T15:15:00.672524+00:00", "dataset_version": "1+e1"},
]
```

**Elexon cross-check: no corroboration.** FACTS DEM1-1 (C7) compared the 7-day archive with
local Elexon NDF and NDFD holdings. Matches were negligible: 1 of 3,967 NDF pairs under the
UK-clock end-label mapping and none under the other three, and 1 of 1,831 NDFD daily-peak
pairs. The current file's target lies beyond the Elexon holdings, so it could not be compared.
The ND classification therefore rests on the vendor's own definition, not on measured
equality. `TODO: verify` Elexon equivalence by issue, which needs same-publication captures of
both sources.

### `national_forecast_7d_files`

- Kind: files · archetype: FC · refresh: daily · empty allowed: no
- files: catalogue only

This family captures the "Demand Curve - Sample" PNG (see DOC above). No silver output.

### `national_forecast_7d_historic_day_ahead`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| DAYSAHEAD | `daysahead` | int64 | — | yes | — | — |
| TARGETDATE | `targetdate` | date | `%Y-%m-%d` | no | — | — |
| FORECASTDEMAND | `forecastdemand` | float64 | — | yes | — | MW |
| CARDINALPOINT | `cardinalpoint` | string | — | yes | — | — |
| CP_TYPE | `cp_type` | string | — | yes | — | — |
| CP_ST_TIME | `cp_st_time` | string | — | yes | — | — |
| CP_END_TIME | `cp_end_time` | string | — | yes | — | — |
| F_Point | `f_point` | string | — | yes | — | — |
| FORECAST_TIMESTAMP | `forecast_timestamp` | string | — | yes | — | — |

- Entity key: `daysahead`, `targetdate`, `forecastdemand`, `cardinalpoint`, `cp_type`, `cp_st_time`, `cp_end_time`, `f_point`, `forecast_timestamp`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`targetdate`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held family: schema, row counts and clock recipes only. No data values are published here.**

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured archive file, `2026-10-07T15:15:13.758197` read as UTC
   (ADR-030 D-15). All 15,703 silver rows share this one vintage. It says when the archive
   file changed, not when any row's forecast was issued.
2. **Event time (`date_sp1` on `targetdate`).** `event_time` = `timestamp_utc` = the UTC
   instant of UK local midnight starting each row's target date; `event_time` equals
   `timestamp_utc` on every row (checked 2026-10-09). It is not the capture time and not a CP instant; it anchors the target date
   only (FACTS T05, g1).

**`FORECAST_TIMESTAMP` is kept raw.** It is a string column, issue recipe `none`, and no
`issue_time` is derived (gridflow
`@tests/unit/test_neso_dem1_records.py::test_historic_forecast_timestamp_is_kept_raw_and_no_issue_time_is_derived`).
Every value carries a `Z` suffix and parses structurally (FACTS C1), and the archive has
exactly one timestamp per lead/target/CP (15,703 groups, FACTS C1). The vendor dictionary
entry for the field is **empty**: no title, description or unit (field-info snapshot
2026-10-08; FACTS T04). Its meaning (forecast-made time or something else), its actual zone,
and whether it is fixed at issue are all unestablished.

Note on the hold text: the generated hold question (below) says the labels "sit after the
file's CKAN last_modified when read as UTC". FACTS DEM1-3 drew that from the 1-day, 2-day and
2–14-day archives; this archive was not in that table. For this 7-day archive the one
measurement goes the other way: the label on the archive rows matching the current forecast,
read as UTC, sits before the file's `last_modified` (FACTS C4). Whether that holds across all
rows was not measured. That does not lift the
hold. The field still has no vendor definition, and an ordering check against file
modification time cannot establish its zone or meaning. `TODO: verify` with the vendor.

**Units.** As for the current family: `forecastdemand` **MW** (archive dictionary
`unit: MW`; FACTS T02/g4,
[vendor dictionary](https://www.neso.energy/data-portal/7-day-ahead-national-forecast/historic_7_day_ahead_demand_forecasts));
`daysahead` lead in days (FACTS T01); CP clocks HHMM strings that the dictionary labels
"Time UTC", kept raw (FACTS T02/T03; `TODO: verify` zone).

**Sentinels (FACTS g5).** Blank `F_Point` cells are present and kept as the empty string `""`;
no `NA` token occurs in this archive (unlike the 1-day and 2-day archives). `F_Point` carries
the `Om` spelling here too. No null token, no bounds. All silver columns have zero nulls.

**Identity and selection.** Entity key = every column, a guard key (FACTS T06, g3). The archive
candidate `(daysahead, targetdate, cardinalpoint, forecast_timestamp)` and the narrower
`(targetdate, cardinalpoint)` were both measured unique on the capture. `whole_capture`
selection; a future `key_latest` on target + CP + lead with an `issue_time` in the key becomes
possible only once the timestamp's clock is supplied (FACTS DEM1-3). `TODO: verify` the
vendor's revision identity.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The current-file resource description states daily publication between 16:15 and 17:00 "clock
time" (UK local is the natural reading; `TODO: verify` the vendor means UK local). The
package carries no "Update Frequency" extra. gridflow has one capture of each resource
(2026-10-08), taken on demand; no scheduled refresh exists yet. Observed across the
2026-10-06 snapshot and the 2026-10-08 capture: the current file holds a single target day and
its filename moved from one target date to the next. `TODO: verify` whether each upload
replaces the previous forecast outright, so that a day not captured is recoverable only from
the archive. `TODO: verify` whether the
archive is appended daily or rewritten (only repeated captures compared row by row can show
it).

**Activation (2026-10-09, master `73fde80`, PR #89).** Both families were transformed with
cutoff 2026-10-08 (one capture each). Silver holds **12 rows** (current) and **15,703 rows**
(archive), equal to the planned counts. No prior silver existed, so nothing was overwritten.
Reconcile `--all --cutoff 2026-10-08` exited 0 with 0 gaps over 36 recorded families
(gridflow `@.planning/v0.22-RESULTS.md` §DEM-1; RULINGS 531–533). Silver path:
`C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`.

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1,
epoch 1). No gold view or builder consumes either family.

**Implementation delta (vendor dictionary vs record).**

- `FORECASTDEMAND`: dictionary type `int4` (examples are integers); the record types it
  `float64`, per the batch column rule (gridflow
  `@.planning/phases/v0.22-K-DEM-1/K-DEM-1-SPEC.md`). Lossless; no defect.
- `CP_ST_TIME` / `CP_END_TIME`: dictionary types `int4` (current `CP_END_TIME` is listed as
  datastore `text`); the record keeps both as raw strings on purpose (zone conflict above).
- Archive `TARGETDATE`: the dictionary example is `20200930` (compact), but the archive body
  uses `%Y-%m-%d`; the current file uses `%Y%m%d`. The record parses each file's actual form.
- Current `TARGETDATE` description reads "D+7 for 1 Day Ahead" (vendor wording slip; the
  archive's reads "D+7 for 7 Day Ahead").

**Modelling notes.** Eligible use: the current family as a seven-day-ahead ND forecast at
cardinal points, available from its vintage. Joining it to half-hourly demand needs the CP
clock zone settled first, and a daily-peak CP must not be joined as a half-hourly value (FACTS
DEM1-1). Forecast-skill studies across leads (1-day, 2-day, 7-day, 2–14-day) need the held
archives and wait on E-SEM. `TODO: verify` modelling use in gridflow_models; none is designed
yet.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `national_forecast_7d_historic_day_ahead`: held: TODO: FORECAST_TIMESTAMP zone is undocumented (values carry Z but sit after the file's CKAN last_modified when read as UTC); whether it is the immutable issue instant; the field has no vendor definition (unit E-SEM)

The archive's silver exists on disk but is **held**: not eligible for publication or
point-in-time model use until unit E-SEM answers the question above (RULINGS 529). Without a
defined issue clock, the CKAN vintage only bounds when the archive file existed. It cannot say
when each past forecast was known, so a row cannot be placed at its true availability time.
This page therefore publishes the archive's schema, row count and clock recipes only, not
its data values or ranges. The measured ordering against `last_modified` for this package is
described under the family (it differs from the generated wording) and does not lift the hold.

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. The hold is per family and sits on `national_forecast_7d_historic_day_ahead`; the
current family `national_forecast_7d_day_ahead_demand` is eligible.

Related holds (gridflow `@docs/neso_data_portal/eligibility.md`): the 1-day, 2-day and
2–14-day historic archives are held on the same `FORECAST_TIMESTAMP` question (the 1-day adds
vendor-documented email-recovery times); the 2–14-day half-hourly family and
`daily_demand_update` are held on their own questions. All are unit E-SEM.
