---
source: "neso_data_portal"
package: "2-14-days-ahead-national-demand-forecast"
dataset_keys: ["national_demand_fc_2_14d_days_ahead", "national_demand_fc_2_14d_days_ahead_half", "national_demand_fc_2_14d_historic_day"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# 2-14 Days Ahead Demand Forecast

NESO's medium-term GB **national demand (ND)** forecast, from 2 to 14 days ahead, published as
three CSV uploads on the Open Data Portal. The package notes say the files are "updated twice
daily, at 09:20 and 14:20". The three files are:

- **Cardinal Point Forecast.** For each lead of 2–14 days, one forecast for each **cardinal
  point** of the target day: the fixed times, troughs and peaks that recur in the daily demand
  shape.
- **Half Hourly Forecast.** The same horizon as a half-hourly curve.
- **Historic archive.** Every past 2–14 day forecast. The vendor says it runs from 2020 to the
  most recent forecast.

The vendor resource text defines ND as the GB generation requirement measured by transmission
operational metering. It excludes generation for station load, pump-storage pumping and
interconnector exports. It is therefore **not TSD** (K-DEM-1-FACTS DEM1-1).

The current cardinal-point file is **eligible**. Every target date in it lies after the
file's CKAN `last_modified`, so the capture vintage is a valid issue-time proxy (RULINGS 529).
The half-hourly curve and the historic archive are **held** (unit E-SEM). The half-hourly
curve is held because its UTC label is not vendor-confirmed as the half-hour end. The archive
is held because its `FORECAST_TIMESTAMP` has no vendor definition and no established zone. See
Holds.

The closest Elexon series are NDFD, a medium-term ND forecast that gives one daily-peak value per date
(@../../elexon/datasets/ndfd.md), and NDF (@../../elexon/datasets/ndf.md). They are related but
not interchangeable. Sibling NESO horizons: @1-day-ahead-demand-forecast.md,
@2-day-ahead-demand-forecast.md, @7-day-ahead-national-forecast.md.

- Publisher group: Demand
- Registry group: demand · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| 2-14 Days Ahead Cardinal Point Forecast | CSV | upload | `9af18ed4-efc8-4779-bef5-c0927fee9b0a` |
| 2-14 Days Ahead Half Hourly Forecast | CSV | upload | `7c0411cd-2714-4bb5-a408-adb065edf34d` |
| Historic 2-14 Day Ahead Demand Forecasts | CSV | upload | `4dd712a2-ee2c-455d-a9c0-9d3564c80fa0` |

All three resources are SILVER. The package has no DOC resources, so it has no PDF/DOCX
methodology and no `_files` family.

- **Cardinal Point Forecast** → `national_demand_fc_2_14d_days_ahead` (eligible).
  Download at capture: [ng_demand_14da_20261022.csv](https://api.neso.energy/dataset/633daec6-3e70-444a-88b0-c4cef9419d40/resource/9af18ed4-efc8-4779-bef5-c0927fee9b0a/download/ng_demand_14da_20261022.csv).
  **The filename is date-stamped and rolls with each upload.** The 2026-10-06 catalogue
  snapshot listed `ng_demand_14da_20261020.csv`, and the 2026-10-08 capture fetched
  `…_20261022.csv`. In the capture the stamp equals the file's last target date
  (2026-10-22). Resolve the URL from the CKAN resource each time, and never hard-code it.
  Captured: `raw_20261008T111301Z_9af18ed4-efc8-4779-bef5-c0927fee9b0a_fa27c9c0.csv`,
  6,328 bytes, 156 data rows.
- **Half Hourly Forecast** → `national_demand_fc_2_14d_days_ahead_half` (held).
  Download: [ng-demand-14da-hh.csv](https://api.neso.energy/dataset/633daec6-3e70-444a-88b0-c4cef9419d40/resource/7c0411cd-2714-4bb5-a408-adb065edf34d/download/ng-demand-14da-hh.csv).
  Captured: `raw_20261008T111304Z_7c0411cd-2714-4bb5-a408-adb065edf34d_9454ade5.csv`,
  29,113 bytes, 624 data rows.
- **Historic 2-14 Day Ahead Demand Forecasts** → `national_demand_fc_2_14d_historic_day` (held).
  Download: [archive_14dayahead.csv](https://api.neso.energy/dataset/633daec6-3e70-444a-88b0-c4cef9419d40/resource/4dd712a2-ee2c-455d-a9c0-9d3564c80fa0/download/archive_14dayahead.csv).
  Captured: `raw_20261008T111309Z_4dd712a2-ee2c-455d-a9c0-9d3564c80fa0_2f070940.csv`,
  24,824,849 bytes, 370,700 data rows.

All three resources are `datastore_active` in CKAN. The datastore totals at a field-info read
on 2026-10-08 (156 / 624 / 370,700) matched the captured row counts. Each capture has one
header epoch.

## Families

### `national_demand_fc_2_14d_days_ahead`

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
   `last_modified` of the captured resource. For the one capture to date that is
   `2026-10-08T08:45:03.632388`. CKAN emits it without an offset, and gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Every row of a
   capture shares this vintage. The file has **no issue column**, so the vintage is the only
   availability clock. Do not borrow the archive's `FORECAST_TIMESTAMP` for this family
   (FACTS g2).
2. **Event time (`date_sp1` on `targetdate`).** `timestamp_utc` = `event_time` = the start of
   settlement period 1 (00:00 UK local time) on the target date, converted to UTC. During BST
   that is 23:00 UTC on the previous day. This held on all 156 silver rows (checked
   2026-10-09). Event time is the target day, **not the capture time**. The `none` fallback
   (timestamp_utc = capture time) does not apply to any family in this package. The anchor is
   date-level only. It does not place the cardinal point within the day, and all 12 points of
   a target day share one `timestamp_utc`.

**Why this family is eligible (RULINGS 529).** In the activated capture every target date
(2026-10-10 → 2026-10-22, leads 2 → 14) falls after the capture's CKAN `last_modified` date
(2026-10-08). So the vintage is a true "known by" time for every forecast in the file: a value
cannot have been observed after the file that already contained it. A test pins this property
(gridflow `@tests/unit/test_neso_dem1_records.py`, `_forward_violations`). It fails when a
fixture contains a past target.

**Shape of a capture.** There are 156 rows: 13 leads (`daysahead` 2–14) × 12 cardinal points.
Each lead has exactly one target date, and lead *n* targets the capture date + *n* days. The
cardinal points in the 2026-10-08 capture (vendor codes, kept verbatim):

| `cardinalpoint` | `cp_type` | `cp_st_time` → `cp_end_time` | `f_point` |
|---|---|---|---|
| 1F | F | 30 → 30 | blank |
| 1S | T | 100 → 130 | blank |
| 1A | P | 200 → 230 | blank |
| L04 | F | 400 → 400 | blank |
| 1B | T | 430 → 730 | Om |
| 2F | F | 800 → 800 | blank |
| 2A | P | 830 → 1200 | DM on 12 days, blank on 1 |
| 2B | P | 1230 → 1300 | blank on 12 days, DM on 1 |
| 3B | T | 1330 → 1630 | Dm |
| 3C | P | 1700 → 1800 (11 days) / 1700 → 1830 (2 days) | blank |
| 4B | P | 1830 → 2000 (11 days) / 1900 → 2000 (2 days) | EM |
| 4C | F | 2400 → 2400 | blank |

The vendor dictionary describes `CP_TYPE` as Fixed / Trough / Peak (`F` / `T` / `P`). It
describes `F_Point` as the forecasting points "overnight demand minimum, daytime demand maximum,
daytime demand minimum and evening demand maximum". `TODO: verify` the mapping of the codes
`Om` / `DM` / `Dm` / `EM` onto those four labels. The dictionary lists the labels but does not
pair them with codes. Peak and trough windows can change between target days, as the 3C and 4B
rows show. Because the window is part of the row, the guard key includes it.

`FORECASTDEMAND` ranges from 17,358 to 36,082 MW across the capture. The first rows of
the capture are lead 2, target 2026-10-10: 1F 20,660, 1S 20,104, 1A 20,357, L04 18,385 MW.

**CP clocks: the dictionary and the body disagree (kept raw).** The vendor dictionary
labels `CP_ST_TIME` and `CP_END_TIME` "Time UTC". They are HHMM integers without zero-padding:
`30` is 00:30 and `2400` closes the day. FACTS T03/C6 joined the fixed cardinal points
(start = end) to the half-hourly file's UTC `GDATETIME`:

| Clock interpretation | Joined rows | Equal demand values |
|---|---:|---:|
| UTC, no shift | 51 | 0 |
| UTC, minus 30 min | 51 | 0 |
| Europe/London, no shift | 52 | 52 |
| Europe/London, minus 30 min | 51 | 0 |

The captured clocks behave as **UK-local labels**, which contradicts the dictionary. gridflow
therefore keeps both clocks as raw strings and builds no CP instant.
`TODO: verify` the zone of the cardinal-point clocks with NESO. Until then, do not convert them
to UTC. This is the main vendor-doc / body conflict on this page.

**Units (vendor dictionary only, [cardinal-point data dictionary](https://www.neso.energy/data-portal/2-14-days-ahead-national-demand-forecast/2-14_days_ahead_cardinal_point_forecast)).**
`FORECASTDEMAND` is **MW** (`unit: MW`), and the resource description defines the measure as
ND. The dictionary types it `int4`. gridflow casts it to float64, and integer values are
unchanged. `DAYSAHEAD` has an empty unit field. The dictionary defines it as the
day-ahead number ("4" for a 4 Day Ahead forecast), so it is a lead in days, not a physical
quantity (FACTS T01, g4). The CP clocks are clock encodings, not durations. `CARDINALPOINT`,
`CP_TYPE` and `F_Point` are categorical text.

**Sentinels and missing values (FACTS g5).** No null-token map is declared, so no global
sentinel conversion happens.

- Blank `F_Point` is written in bronze as a quoted empty string (`""`), and silver keeps it as
  the **empty string**, not null (104 of 156 rows in this capture). Filter with
  `f_point = ''`, not `IS NULL`.
- A literal `NA` in `F_Point` would also survive as the string `NA`. It does not occur in this
  capture. It occurs in the historic 1-day and 2-day archives. `TODO: verify` its meaning there.
- `FORECASTDEMAND` has no blanks and no zeros in this capture. No bounds are imposed, and
  zeros or `-1` would be preserved.

**Identity and selection.** The entity key is every column. It is a **capture guard**, not a
revision identity (FACTS g3, T06). The cardinal-point key `(daysahead, targetdate,
cardinalpoint)` was measured unique, but no vendor text says it identifies a stable record
across uploads. `TODO: verify` the vendor's revision identity. `_latest` is therefore
`whole_capture`: the newest capture wins as a whole. Because each upload replaces the whole
forward window, history across uploads lives only in the dated silver captures (and in the
archive below, once it is released).

**Activation (2026-10-09, master `73fde80`).** Cutoff 2026-10-08, one capture: **156 rows**,
equal to the planned count. No prior silver existed, so nothing was overwritten. Reconcile
`--all --cutoff 2026-10-08` found 0 gaps across 36 recorded families (gridflow
`@.planning/v0.22-RESULTS.md` §DEM-1; RULINGS 531–533).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version`. All timestamps are tz-aware UTC. `dataset_version` `1+e1` = record version 1,
epoch 1. This is the same for all three families.

### `national_demand_fc_2_14d_days_ahead_half`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| DATE | `date` | date | `%Y-%m-%d` | no | — | — |
| CTIME | `ctime` | string | — | yes | — | — |
| GDATETIME | `gdatetime` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | — |
| NATIONALDEMAND | `nationaldemand` | float64 | — | yes | — | MW |

- Entity key: `date`, `ctime`, `gdatetime`, `nationaldemand`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM). This page gives schema, clocks and counts only, and no data values.**

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the capture's CKAN
   `last_modified`, `2026-10-08T08:46:32.246773`, read as UTC. The file has no issue column.
2. **Event time (`date_sp1` on `date`).** `timestamp_utc` = `event_time` = 00:00 UK local on
   `DATE`, converted to UTC (checked on all 624 rows, 2026-10-09). It is **not the capture
   time**. It is a day-level anchor, so all 48 half-hours of a date share one `timestamp_utc`.
   Never use `timestamp_utc` as a half-hour key for this family.

The half-hour position is carried separately:

- `gdatetime` is a typed **UTC** column. The vendor dictionary says it "is in GMT/UTC
  regardless of forecast date's GB timezone".
- `ctime` is the raw UK-clock HHMM string. The dictionary says `DATE` and `CTIME` use "the GB
  timezone (BST/GMT)".

The family was not shipped as `utc_instant(gdatetime)`. The record's instant recipe has no
offset parameter. If `GDATETIME` is an end label, `utc_instant` would stamp each value
30 minutes late as a period start (FACTS T03).

**Hold question:** whether `GDATETIME` (UTC) labels the half-hour **end**. The structural
evidence (FACTS C6):

- The capture has 13 target dates with 48 rows each. On every date `CTIME` runs from `30` to
  `2400`.
- On 611 of 624 rows, `GDATETIME` converted to Europe/London matches both `DATE` and `CTIME`.
- The other 13 rows are the `2400` rows. These hold next-day local midnight against the
  preceding date, which is consistent with end labels.
- That is strong evidence but not a vendor definition. The capture also has no DST transition
  day, so 46- or 50-period behaviour is unobserved.
- No overlapping Elexon forecast exists to cross-check it: zero joined rows under both start
  and end mappings (FACTS C8).

**Units (vendor dictionary only, [half-hourly data dictionary](https://www.neso.energy/data-portal/2-14-days-ahead-national-demand-forecast/2-14_days_ahead_half_hourly_forecast)).**
`NATIONALDEMAND` is **MW** (`unit: MW`; dictionary type `int4`, cast to float64), and it is ND
per the resource description. `CTIME` is an HHMM clock encoding (dictionary type `int4`, kept as
a string so `2400` survives).

**Sentinels (FACTS g5).** No null token is declared, and the capture has no blank cells in any
vendor column. Zeros and `-1` would be preserved, and no bounds are imposed.

**Identity.** `GDATETIME` was measured unique in the body. The entity key is still the
every-column guard, and `_latest` is `whole_capture` (FACTS T04).
`TODO: verify` the vendor revision key.

**Activation.** **624 rows**, equal to the planned count (cutoff 2026-10-08, RULINGS 532–533).

### `national_demand_fc_2_14d_historic_day`

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

**Held (unit E-SEM). This page gives schema, clocks and counts only, and no data values.**

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the capture's CKAN
   `last_modified`, `2026-10-08T08:46:27.592963`, read as UTC. This is the only availability
   clock gridflow uses. It is deliberately **not** backdated to `FORECAST_TIMESTAMP` or to
   target minus lead (FACTS g2). Every archived row, however old, carries the vintage of the
   capture that delivered it.
2. **Event time (`date_sp1` on `targetdate`).** `timestamp_utc` = `event_time` = 00:00 UK
   local on the target date, in UTC (checked on all 370,700 rows, 2026-10-09). It is **not the
   capture time**. It is day-level, like the current file.

Note that the archive writes `TARGETDATE` as `%Y-%m-%d`, while the current file uses `%Y%m%d`.

**Hold question: `FORECAST_TIMESTAMP`.** The archive is the only resource in the package with a
per-row issue candidate, but:

- The vendor dictionary leaves every attribute of `FORECAST_TIMESTAMP` empty: no title,
  description or unit
  ([historic data dictionary](https://www.neso.energy/data-portal/2-14-days-ahead-national-demand-forecast/historic_2-14_day_ahead_demand_forecasts)).
- The values are structurally `Z`-suffixed. Read literally as UTC, the newest of them sits
  **after** the file's own CKAN `last_modified`, which cannot be true of a creation time.
  UK-local reading is plausible but unproven (FACTS DEM1-3).
- Immutability and availability at issue are not documented.

gridflow therefore keeps it as a raw string with issue recipe `none`. It is in the entity key as
a raw value only.

**Structure (counts only, FACTS C1/C4).** Each (lead, target, cardinal point) has 1 or 2
distinct timestamps (281,914 groups with 1, 44,393 with 2). Across leads, a target/cardinal
point has between 1 and 26. So `(targetdate, cardinalpoint)` alone collapses forecast history.
Any future `key_latest` must keep the lead and an established issue time (FACTS DEM1-3). The
archive's cardinal-point clocks carry the same dictionary-says-UTC / body-behaves-local conflict
as the current file. They are kept raw (FACTS T02/T03).

**Units (vendor dictionary only).** `FORECASTDEMAND` is **MW** (`unit: MW`) and is ND.
`DAYSAHEAD` is a lead in days (unit field empty). The CP clocks and `FORECAST_TIMESTAMP` are
clock/time encodings, not physical values.

**Sentinels (FACTS g5).** Blank `F_Point` is kept as the empty string, the same as in the
current file. No null token is declared, and no vendor column has null cells after typing. The
literal `NA` token found in the 1-day and 2-day archives does not occur in `F_Point` here: there
are 0 occurrences in the activated silver (checked 2026-10-09).

**Activation.** **370,700 rows**, equal to the planned count. Peak memory was 910.1 MiB, the
batch maximum (gridflow `@.planning/v0.22-RESULTS.md` §DEM-1).

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The package notes say the files are "updated twice daily, at 09:20 and 14:20".
`TODO: verify` the zone of those times; UK local is likely but not stated. gridflow's registry
refresh is daily, so each run captures one state of the cardinal-point and half-hourly files,
and the other daily update is not retained. `TODO: verify` whether the historic archive keeps
both daily issues. Its 1–2 timestamps per lead/target/CP are consistent with that, but do not
prove it.

Observed at capture (no inference drawn): the three files' CKAN `last_modified` values fall
between 08:45 and 08:47 UTC on 2026-10-08.

No scheduled gridflow refresh exists yet. Captures are on demand.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `national_demand_fc_2_14d_days_ahead_half`: held: TODO: whether GDATETIME (UTC) labels the half-hour end (611/624 rows align as end labels; 2400 closes the date) - vendor confirmation needed; DST-day behaviour unobserved (unit E-SEM)
- `national_demand_fc_2_14d_historic_day`: held: TODO: FORECAST_TIMESTAMP zone is undocumented (values carry Z but sit after the file's CKAN last_modified when read as UTC); whether it is the immutable issue instant; the field has no vendor definition (unit E-SEM)

Both held outputs exist in silver, but neither is eligible for publication or point-in-time
model use until unit E-SEM answers its question (RULINGS 529). This page publishes their
schema, clocks and row counts only.

- **What would lift the half-hourly hold:** a vendor statement that `GDATETIME` is the
  half-hour end (or start), and a capture spanning a clock change. The family could then move
  to an instant temporal recipe with the correct boundary.
- **What would lift the archive hold:** a vendor definition of `FORECAST_TIMESTAMP` (its
  meaning, zone and immutability). That would allow an issue recipe on it and a `key_latest` on
  (lead, target, cardinal point, issue).

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. Holds are per family, and only `national_demand_fc_2_14d_days_ahead` is eligible.

Related, same unit and batch (gridflow `@docs/neso_data_portal/eligibility.md`): the 1-day,
2-day and 7-day historic archives are held on the same `FORECAST_TIMESTAMP` question.
`daily_demand_update` is held on zero ND/TSD forecast-tail rows. The current 1-day, 2-day and
7-day cardinal-point files are eligible on the same forward-target rule as this package's
current file. `historic_demand` stays ingest-only until unit DEM-1H (RULINGS 528).
