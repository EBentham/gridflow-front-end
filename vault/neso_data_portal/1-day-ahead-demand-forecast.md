---
source: "neso_data_portal"
package: "1-day-ahead-demand-forecast"
dataset_keys: ["demand_forecast_1d_day_ahead_national", "demand_forecast_1d_historic_day_ahead"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Day Ahead Demand Forecast

NESO's day-ahead forecast of GB **national demand**, published on the Open Data Portal as two
CSVs. The vendor defines national demand as the GB generation requirement: the sum of metered
generation from operational metering, **excluding** generation for station load, pump-storage
pumping and interconnector exports. This is the ND measure, not TSD (gridflow
`@.planning/phases/v0.22-K-DEM-1/K-DEM-1-FACTS.md` DEM1-1). The forecast is not a half-hourly
profile. It gives demand at a fixed set of **cardinal points**: the recurring peaks, troughs and
fixed-time points of the daily demand curve. Each row names a point, its type (fixed, trough or
peak) and the clock window it falls in. The **current** file holds the latest forecast for the
next day (12 cardinal points). The **historic** file is the vendor's archive of every day-ahead
forecast since 2018. Each archive row carries a `FORECAST_TIMESTAMP`. Use the package as a
day-ahead ND forecast benchmark against Elexon NDF
(@../../elexon/datasets/ndf.md), or as a feature for demand-shape models
(@../../../20-domain/modelling/renewable-and-demand-forecasting.md). Only the current file is
eligible for publication. The archive's silver output is held because its issue clock is
unresolved (see Holds).

- Publisher group: Demand
- Registry group: demand · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Day Ahead National Demand Forecast | CSV | upload | `aec5601a-7f3e-4c4c-bf56-d8e4184d3c5b` |
| Historic Day Ahead Demand Forecasts | CSV | upload | `9847e7bb-986e-49be-8138-717b25933fbb` |

- Day Ahead National Demand Forecast → `demand_forecast_1d_day_ahead_national`.
  Download as captured: [ng_demand_1da_20261009.csv](https://api.neso.energy/dataset/8fbc8a09-06af-4c90-886f-d3025d38a349/resource/aec5601a-7f3e-4c4c-bf56-d8e4184d3c5b/download/ng_demand_1da_20261009.csv).
  The file name carries the target date and changes with each publication. The 2026-10-06
  catalogue snapshot listed `ng_demand_1da_20261007.csv` for the same resource id. The stable
  handle is the resource id, not the URL. CKAN datastore active.
  Captured: `raw_20261008T100551Z_aec5601a-7f3e-4c4c-bf56-d8e4184d3c5b_cde77f39.csv`,
  578 bytes, 12 data rows, one header epoch.
- Historic Day Ahead Demand Forecasts → `demand_forecast_1d_historic_day_ahead`.
  Download: [archive_1dayahead.csv](https://api.neso.energy/dataset/8fbc8a09-06af-4c90-886f-d3025d38a349/resource/9847e7bb-986e-49be-8138-717b25933fbb/download/archive_1dayahead.csv)
  (the vendor describes it as all historic day-ahead forecasts from 2018 to the most recent
  forecast; CKAN datastore active).
  Captured: `raw_20261008T100559Z_9847e7bb-986e-49be-8138-717b25933fbb_b92031eb.csv`,
  3,889,600 bytes, 58,561 data rows, one header epoch.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Demand Curve - Sample | PNG | upload | `bcc91aed-76fd-4114-86b8-7c83de23b35c` |

- Download: [cardinal-points.png](https://api.neso.energy/dataset/8fbc8a09-06af-4c90-886f-d3025d38a349/resource/bcc91aed-76fd-4114-86b8-7c83de23b35c/download/cardinal-points.png)
  (CKAN `last_modified` 2019-12-12T15:01:08.405123).
- Captured: `raw_20261008T100555Z_bcc91aed-76fd-4114-86b8-7c83de23b35c_cfff1cd9.png`,
  133,480 bytes, family `demand_forecast_1d_files`. Catalogue only: no silver output. The
  vendor describes it as a demand curve showing the time of day at which the cardinal points
  occur. It is the closest thing to a key for the `CARDINALPOINT` codes (see below).

## Families

### `demand_forecast_1d_day_ahead_national`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| DAYSAHEAD | `daysahead` | int64 | — | yes | — | 2 |
| TARGETDATE | `targetdate` | date | `%Y%m%d` | no | — | — |
| FORECASTDEMAND | `forecastdemand` | float64 | — | yes | — | — |
| CARDINALPOINT | `cardinalpoint` | string | — | yes | — | — |
| CP_TYPE | `cp_type` | string | — | yes | — | — |
| CP_ST_TIME | `cp_st_time` | string | — | yes | — | — |
| CP_END_TIME | `cp_end_time` | string | — | yes | — | 1930 |
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
   `2026-10-08T08:00:00.985148`, which CKAN emits without an offset. gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All 12 silver rows
   share this one vintage. The file has **no issue column**, and the record's issue recipe is
   `none`: no row carries its own forecast-issue time.
2. **Event time (`date_sp1` on `targetdate`).** `timestamp_utc` = `event_time` = the start of
   settlement period 1 of the target date, i.e. UK local midnight of `targetdate` expressed in
   UTC (for a BST target date, 23:00 UTC on the previous day). Checked on every silver row on
   2026-10-09. Event time is therefore **not** the capture time. It is a **date anchor**: every
   cardinal point of a target date shares the same `timestamp_utc`. The instant at which each
   peak, trough or fixed point occurs is not derived. It stays in the raw `cp_st_time` /
   `cp_end_time` strings (FACTS T04).

**Why this family is eligible (forward-target rule, RULINGS 529).** Every target date in the
capture falls after the capture's CKAN `last_modified` (target 2026-10-09 against a vintage of
2026-10-08T08:00Z). The forecast was therefore public at the vintage instant, before its
target day began, so the CKAN vintage is a valid conservative proxy for the missing issue time.
gridflow pins this property in
`@tests/unit/test_neso_dem1_records.py::test_current_cp_targets_are_later_than_the_capture_vintage`.
A capture whose target date is not later than its vintage fails that test. Eligibility is
conditional on that property continuing to hold.

**Cardinal-point layout of the captured file** (structure only, demand values omitted):

| `cardinalpoint` | `cp_type` | `cp_st_time` | `cp_end_time` | `f_point` |
|---|---|---|---|---|
| 1F | F | 30 | 30 | |
| 1S | T | 100 | 130 | |
| 1A | P | 200 | 230 | |
| 4 | F | 400 | 400 | |
| 1B | T | 430 | 730 | Om |
| 2F | F | 800 | 800 | |
| 2A | P | 830 | 1200 | DM |
| 2B | P | 1230 | 1300 | |
| 3B | T | 1330 | 1630 | Dm |
| 3C | P | 1700 | 1830 | |
| 4B | P | 1900 | 2000 | EM |
| 4C | F | 2400 | 2400 | |

- `CP_TYPE` is F, T or P: fixed (a fixed time of day), trough (a minimum over a window) or peak
  (a maximum over a window), per the vendor dictionary. Fixed points have equal start and end
  clocks.
- `CP_ST_TIME` / `CP_END_TIME` are HHMM clocks written without leading zeros (`30` = 00:30;
  `2400` closes the day). They are kept as strings. They bound the window in which the point
  falls. A trough or peak is not necessarily at either end (FACTS g1).
- `CARDINALPOINT` codes (`1F`, `1S`, `2A`, …): the dictionary explains the cardinal-point concept
  but does not list the codes. `TODO: verify` the vendor's definition of each code. The DOC
  image above shows where the points sit on the daily curve.
- `F_Point` marks the four "forecasting points". The vendor comment defines them as overnight
  minimum (half hours ending 00:30–07:30), daytime peak (08:00–13:00), daytime minimum
  (13:30–16:30) and evening peak (17:00–24:00), each in half-hour-ending terms. The comment spells
  the first one `OM`, but the file carries `Om`. Rows that are not forecasting points carry a blank.

**CP clock zone conflict.** The current file's dictionary labels both CP clocks "Time UTC".
The archive dictionary says the same clocks are in the UK time in effect on the forecast date.
The 12 current rows equal their newest archive counterparts on demand and on both CP clocks
(FACTS C4). The two statements therefore describe the same values, and at most one can be right.
`TODO: verify` the zone with the vendor. Until then the clocks stay raw strings and no instant
is built from them.

**Units (vendor dictionary only).**

- `FORECASTDEMAND`: **MW**. The current file's dictionary leaves the unit blank. The MW comes
  from the same-package archive dictionary
  ([historic dictionary](https://www.neso.energy/data-portal/1-day-ahead-demand-forecast/historic_day_ahead_demand_forecasts)),
  which declares `unit: MW` for the same field. The transfer rests on the measured equality of all
  12 current rows with their archive counterparts (FACTS T02, C4, g4). The unit was not inferred
  from the column name.
- The generated table's "Vendor unit" entries `2` (DAYSAHEAD) and `1930` (CP_END_TIME) are
  **not units**. They are example-like values copied into the vendor's `unit` field. The same
  dictionary also calls FORECASTDEMAND a "2 day ahead" value. The dictionary was evidently
  copied from the 2-day package (FACTS §`demand_forecast_1d_day_ahead_national`). Read
  `daysahead` as the lead in days (the archive dictionary's `Days`), `targetdate` as a calendar
  date, and the CP clocks as HHMM encodings. None of these carries a physical unit.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- Blank `F_Point` cells are quoted empty strings in the bronze CSV (`""`). Silver keeps them
  as **empty strings, not null** (8 of 12 rows). No vendor rule says a blank means missing.
- No column has a null in silver. No min/max bounds are imposed and no value is converted.

**Identity and selection.** The entity key is **every column**, a capture-level duplicate
guard (FACTS g3). The lead/target/CP triple `(daysahead, targetdate, cardinalpoint)` is unique
in the capture, but no vendor text documents it as a revision identity.
`TODO: verify` the vendor's revision key. `_latest` is `whole_capture`: the newest capture
replaces the previous one as a whole.

**Activation (2026-10-09, master `73fde80`, PR #89).** Transformed at cutoff 2026-10-08 (one
capture): **12 silver rows**, equal to the planned count. No prior silver existed, so nothing
was overwritten. Reconcile `--all --cutoff 2026-10-08` exited 0 with 0 gaps over 36 recorded
families (gridflow `@.planning/v0.22-RESULTS.md` §DEM-1; RULINGS 531–533).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1, epoch 1).

### `demand_forecast_1d_files`

- Kind: files · archetype: FC · refresh: intraday · empty allowed: no
- files: catalogue only

This family captures the cardinal-points demand-curve PNG (see DOC above). It has no silver
output and no clocks beyond the capture's CKAN `last_modified`.

### `demand_forecast_1d_historic_day_ahead`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| DAYSAHEAD | `daysahead` | int64 | — | yes | — | Days |
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

**Held (unit E-SEM).** This family's silver output exists but is not eligible for publication
or point-in-time use. This page gives schema, row counts and structural counts only. It gives
no data values or ranges. See Holds.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the captured archive, `2026-10-08T08:00:22.840245` (offset-less, read as
   UTC per ADR-030). All 58,561 rows share this one vintage. The vintage says when the archive
   file last changed. It does **not** say when any archived forecast became available. Every
   archived forecast was public by then, but most much earlier.
2. **Event time (`date_sp1` on `targetdate`).** `timestamp_utc` = `event_time` = the UK
   local-midnight start of the target date in UTC. Checked on every silver row on 2026-10-09.
   It is not the capture time. As in the current file, it is a date anchor, and the CP instant
   stays in the raw clock strings.

The record's issue recipe is `none`. `FORECAST_TIMESTAMP` is kept as a **raw string**, not
as an issue clock, for three reasons:

- The vendor dictionary describes it as the date and time the forecast was made. The vendor
  comment adds that some forecasts were overwritten and later recovered from emails. Those rows
  carry the **recovery** time, not the original issue time. Nothing in the file identifies them.
- Every value ends in `Z` and parses structurally (0 failures, FACTS C1). Read as UTC, though,
  the newest archive label falls **after** the file's own CKAN `last_modified`. A forecast
  cannot have been made after the file containing it was saved. So the `Z` alone does not
  establish UTC (FACTS DEM1-3, C4). `TODO: verify` the actual zone.
- No source shows that archived rows are immutable once issued (FACTS g2).

**CP clocks.** The archive dictionary says `CP_ST_TIME` / `CP_END_TIME` are in the UK time in
effect at the forecast date and time (FACTS T01/T02). They are kept as raw HHMM strings. See the
zone conflict with the current file's dictionary above.

**Units (vendor dictionary).** `FORECASTDEMAND` is **MW**, `DAYSAHEAD` is **Days**, both
declared directly in the
[historic dictionary](https://www.neso.energy/data-portal/1-day-ahead-demand-forecast/historic_day_ahead_demand_forecasts).
The other columns are dates, clock encodings or categories and carry no physical unit.

**Sentinels and missing values (FACTS g5).** No null token is declared.

- `F_Point` holds the literal string `NA` in 36,300 rows and a blank (empty string) in 2,414
  rows. Both are preserved as strings. `TODO: verify` what the vendor means by `NA` versus a
  blank. They may mean "not a forecasting point" or "not recorded".
- No column has a null in silver. No bounds are imposed.

**Identity and selection.** The guard key is every column, with zero duplicates in the capture.
`(daysahead, targetdate, cardinalpoint)` repeats, because the archive holds more than one issue
for many target points. Per lead/target/CP group, FACTS C1 measured 1 distinct timestamp in
17,026 groups, 2 in 20,703 and 3 in 43. Adding the raw `forecast_timestamp` makes the key unique.
`TODO: verify` the vendor's revision identity. A per-key `_latest` would need `issue_time` in
place of the raw timestamp, and that waits on E-SEM (FACTS DEM1-3). Until then `_latest` is
`whole_capture`.

**Elexon cross-check (corroboration only).** FACTS DEM1-1 compared the archive with locally held
Elexon NDF/TSDF and NDFD/TSDFD under four timing interpretations. Matches were sparse. They
support the vendor's ND classification but settle neither the CP clock zone nor the issue clock.
A definitive equivalence needs same-publication captures on both sides.
`TODO: verify` (FACTS DEM1-1).

**Activation (2026-10-09, master `73fde80`).** Transformed at cutoff 2026-10-08:
**58,561 silver rows**, equal to the planned count, with no prior silver overwritten. Reconcile
reported 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` §DEM-1; RULINGS 532–533). Silver
carries the same eight lineage/clock columns as the current family.

## Cadence

- Registry refresh: intraday
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live
- Intraday: captured once per refresh run — sampled, not complete

The vendor's resource description gives the current file's publication as **twice daily**,
between 09:00–09:15 and 12:00–12:15 clock time. The one capture to date has a CKAN
`last_modified` of 08:00:00 UTC (09:00 BST), consistent with the morning slot. Because gridflow
captures once per refresh run, a run can miss one of the two daily publications. The current
family keeps only the publication present at capture time.

- `TODO: verify` whether the 12:00 publication revises the 09:00 forecast for the same target
  date, or what it changes. The archive's 1–3 timestamps per target point are consistent with
  more than one issue per day. That does not establish the publication pattern, and the
  recovered-timestamp caveat applies.
- `TODO: verify` whether the archive is appended or rewritten on each publication. Only
  repeated captures compared row by row can show this.
- Captures to date: one per family (2026-10-08). No scheduled refresh has run yet.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `demand_forecast_1d_historic_day_ahead`: held: TODO: FORECAST_TIMESTAMP zone is undocumented (values carry Z but sit after the file's CKAN last_modified when read as UTC); whether it is the immutable issue instant; some timestamps are vendor-documented email-recovery times (unit E-SEM)

The archive is held by RULINGS 529 (seat ruling, PROXY-SOURCED). It can never be used
point-in-time with its CKAN vintage, because that vintage is later than almost every forecast in
the file. The only per-row clock, `FORECAST_TIMESTAMP`, has an unestablished zone. The vendor
also says some values are recovery times rather than issue times. Unit E-SEM must answer
three things before the hold can lift:

1. The zone of `FORECAST_TIMESTAMP`.
2. Whether it is the immutable issue instant.
3. How to identify the email-recovered rows.

The silver output stays on disk. This page publishes no data values from it.

`demand_forecast_1d_day_ahead_national` is **eligible**. It is not held, under the
forward-target rule above (RULINGS 529). The package-level `eligibility: eligible` in the front
matter is the package registry entry. The hold is per family.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`): the 2-day
(@2-day-ahead-demand-forecast.md), 7-day (@7-day-ahead-national-forecast.md) and 2–14-day
(@2-14-days-ahead-national-demand-forecast.md) archives are held on the same
`FORECAST_TIMESTAMP` question, along with the 2–14-day half-hourly file and
`daily_demand_update` (@daily-demand-update.md). All are unit E-SEM. `historic_demand` is split
to unit DEM-1H and stays ingest-only (RULINGS 528).
