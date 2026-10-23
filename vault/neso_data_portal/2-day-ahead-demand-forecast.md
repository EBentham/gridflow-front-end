---
source: "neso_data_portal"
package: "2-day-ahead-demand-forecast"
dataset_keys: ["demand_forecast_2d_day_ahead", "demand_forecast_2d_historic_day_ahead"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# 2 Day Ahead Demand Forecast

NESO's two-day-ahead forecast of GB **national demand (ND)** at a day's **cardinal points**.
Cardinal points are the recurring peaks, troughs and fixed clock times of the daily demand
curve that NESO forecasts. They are not a half-hourly grid. Each upload of the current file
holds one target date (D+2) with one row per cardinal point: 12 rows in the capture to date.
The resource description defines national demand as the GB generation requirement, the sum of
metered generation excluding station load, pump-storage pumping and interconnector exports. It
is therefore ND, not transmission system demand (TSD) (gridflow
`@.planning/phases/v0.22-K-DEM-1/K-DEM-1-FACTS.md` DEM1-1, C9). The package description says the
forecast helps the industry balance supply and demand positions. A second resource archives
every past two-day-ahead forecast with a `FORECAST_TIMESTAMP` column. The current family is
**eligible**. Every target in a capture lies after the capture's CKAN vintage, so the vintage is
a valid issue proxy (RULINGS 529). The archive family is **held** because its issue clock is
unresolved (see Holds).

Do not join these values as a half-hourly series. A cardinal-point value is a forecast of a
peak, trough or fixed-time point within a window on the target date. Elexon's medium-term NDFD
publishes a daily peak, and NDF is half-hourly. Neither is the same shape (FACTS DEM1-1).

- Publisher group: Demand
- Registry group: demand · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| 2 Day Ahead Demand Forecast | CSV | upload | `cda26f27-4bb6-4632-9fb5-2d029ca605e1` |
| Historic 2 Day Ahead Demand Forecasts | CSV | upload | `24abd271-5936-45c7-85f4-2a6b450ef6b7` |

- **2 Day Ahead Demand Forecast** → `demand_forecast_2d_day_ahead` (eligible).
  Download as captured: [ng_demand_2da_20261009.csv](https://api.neso.energy/dataset/836df27e-e92c-45bf-80c0-a197e7c0ece3/resource/cda26f27-4bb6-4632-9fb5-2d029ca605e1/download/ng_demand_2da_20261009.csv).
  The download filename changes with each upload: the 2026-10-06 catalogue snapshot listed
  `ng_demand_2da_20261008.csv`, the 2026-10-08 capture fetched `ng_demand_2da_20261009.csv`. The
  stable handle is the resource id, not the URL. CKAN datastore active.
  Captured: `raw_20261008T100606Z_cda26f27-4bb6-4632-9fb5-2d029ca605e1_7e4c8778.csv`, 578 bytes,
  12 data rows, one header epoch.
- **Historic 2 Day Ahead Demand Forecasts** → `demand_forecast_2d_historic_day_ahead` (held).
  Download: [archive_2dayahead.csv](https://api.neso.energy/dataset/836df27e-e92c-45bf-80c0-a197e7c0ece3/resource/24abd271-5936-45c7-85f4-2a6b450ef6b7/download/archive_2dayahead.csv).
  CKAN datastore active. Captured:
  `raw_20261008T100614Z_24abd271-5936-45c7-85f4-2a6b450ef6b7_3ac36727.csv`, 970,225 bytes,
  14,608 data rows, one header epoch.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Demand Curve - Sample | PNG | upload | `607621c1-20c1-4b29-81e1-16156d04b13f` |

- Download: [cardinal-points.png](https://api.neso.energy/dataset/836df27e-e92c-45bf-80c0-a197e7c0ece3/resource/607621c1-20c1-4b29-81e1-16156d04b13f/download/cardinal-points.png)
  (CKAN `last_modified` 2019-12-12T15:08:01.064226). The vendor describes it as a demand curve
  showing what time of day the different cardinal points occur.
- Captured: `raw_20261008T100610Z_607621c1-20c1-4b29-81e1-16156d04b13f_cfff1cd9.png`,
  133,480 bytes, family `demand_forecast_2d_files`. Catalogue only: no silver output.

## Families

### `demand_forecast_2d_day_ahead`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| DAYSAHEAD | `daysahead` | int64 | — | yes | — | — |
| TARGETDATE | `targetdate` | date | `%Y%m%d` | no | — | — |
| FORECASTDEMAND | `forecastdemand` | float64 | — | yes | — | MW |
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
   `2026-10-07T15:15:00.349284`, which CKAN emits without an offset. gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`, D-15). Every silver
   row of a capture shares this one vintage. The file has **no issue column**, so the vintage is
   the only issue clock (FACTS g2). gridflow does not derive an issue from the capture filename
   or from target date minus lead (FACTS §2).
2. **Event time (`date_sp1` on `targetdate`).** `event_time` = `timestamp_utc` = the UTC
   instant of settlement period 1 (00:00 UK local) on the target date. Target 2026-10-09 (BST)
   gives `2026-10-08 23:00 UTC` on every row (checked 2026-10-09). This **anchors the target
   date only**. It is not the instant of any cardinal point, and all 12 rows of a target share
   it. The cardinal-point window clocks stay raw strings in `cp_st_time` / `cp_end_time`, and
   gridflow makes no UTC instant from them (FACTS T03/T04, g1). Event time is not the capture
   time here.

**Why the vintage is a valid issue proxy (RULINGS 529).** Every target date in the capture
(2026-10-09) is later than the date of its CKAN vintage (2026-10-07). Each row was therefore
published before its target day began, so `available_at` never post-dates the target. A test
pins this forward-target property on the fixture. A capture with a past target fails it
(gridflow `@.planning/phases/v0.22-K-DEM-1/K-DEM-1-SPEC.md` §Tests). Observed, not inferred:
the vintage `15:15` UTC is `16:15` BST, the opening of the vendor's stated publication window
(see Cadence).

**Cardinal-point structure (eligible, from the capture).** One target date, `daysahead` = 2:

| `cardinalpoint` | `cp_type` | `cp_st_time` | `cp_end_time` | `f_point` | `forecastdemand` (MW) |
|---|---|---|---|---|---:|
| 1F | F | 30 | 30 | | 21012 |
| 1S | T | 100 | 130 | | 20808 |
| 1A | P | 200 | 230 | | 20756 |
| 4 | F | 400 | 400 | | 18981 |
| 1B | T | 430 | 730 | Om | 18118 |
| 2F | F | 800 | 800 | | 26261 |
| 2A | P | 830 | 1200 | DM | 29156 |
| 2B | P | 1230 | 1300 | | 26716 |
| 3B | T | 1330 | 1630 | Dm | 23998 |
| 3C | P | 1700 | 1830 | | 29437 |
| 4B | P | 1900 | 2000 | EM | 30598 |
| 4C | F | 2400 | 2400 | | 21470 |

The dictionary defines `CP_TYPE` as Fixed (F, a fixed time of day), Trough (T, minimum demand)
or Peak (P, maximum demand). `F_Point` marks the four published forecasting points. The
dictionary comment gives their windows as "half hour ending" ranges: overnight minimum 00:30 to
07:30, daytime peak 08:00 to 13:00, daytime minimum 13:30 to 16:30, evening peak 17:00 to 24:00.
The dictionary spells the overnight code `OM`; the body carries `Om`. Both are recorded as the
vendor wrote them. Clocks are HHMM without leading zeros (`30` = 00:30), and `2400` closes the
date.

**Units (vendor dictionary only, [NESO package page](https://www.neso.energy/data-portal/2-day-ahead-demand-forecast)).**

- `FORECASTDEMAND` is **MW**, stated directly in this resource's dictionary (`unit: MW`, FACTS
  C2, g4). No sibling transfer is needed, unlike the 1-day package.
- `DAYSAHEAD` is the forecast lead in **days**. This dictionary leaves the unit blank and
  describes `2` as the 2-day-ahead forecast. The same-package archive dictionary gives `Days`,
  and FACTS C4 matched the current rows to the archive (FACTS T01). It is an integer lead, not a
  physical value.
- `TARGETDATE` is a calendar date (`%Y%m%d`), with no physical unit.
- `CP_ST_TIME` / `CP_END_TIME` are HHMM clock encodings, not quantities. The generated table's
  `1930` under `CP_END_TIME` copies the dictionary's unit field verbatim. It is an example-like
  value placed in the unit slot, not a unit (FACTS §2 note on copied dictionary metadata, g4).
- `CARDINALPOINT`, `CP_TYPE`, `F_Point` are categorical text.

**CP clock zone conflict.** This dictionary describes `CP_ST_TIME` and `CP_END_TIME` as "Time
UTC". The archive dictionary says they are relative to the timezone in effect in the UK at the
forecast date. FACTS C4 found the clock values identical across the current/archive pair.
`TODO: verify` which zone the cardinal-point clocks use, and whether a clock labels the start
or the end of its half-hour (the `F_Point` comment uses "half hour ending" wording). Until then
the clocks stay raw.

**Sentinels and missing values (FACTS g5).** The vendor declares no sentinel spelling, and the
record has no null-token map.

- Blank `F_Point` cells (8 of 12 in this capture) are kept as **empty strings**, not nulls. In
  this capture the four labelled rows are the four forecasting points and the eight blank rows
  are the other cardinal points. `TODO: verify` that this is the vendor's rule. The dictionary
  does not say it.
- `NA` was not observed in this file. It occurs only in the archive (see below).
- No zeros or negative values are converted. No min/max bounds are imposed.

**Identity and selection.** The entity key is **every column**: a capture-level duplicate guard,
not a documented revision identity (FACTS g3; gridflow
`@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md`). The profiler proposed
`FORECASTDEMAND` alone as the key. It was unique in the body, but demand values can coincide or
change, so it was rejected. The candidate `(daysahead, targetdate, cardinalpoint)` was measured
unique too (FACTS C1). `TODO: verify` a vendor-documented revision identity. `_latest` is
`whole_capture`: the newest capture wins as a whole
(gridflow `@docs/DECISION_LOG/ADR-034-neso-generic-silver-engine.md`).

**Correspondence with the archive.** All 12 current rows equal their archive counterparts on
demand, CP clocks and the other compared fields (FACTS C4). At capture the archive already held
the current forecast. The two resources' CKAN vintages are 12 seconds apart.

**Elexon cross-check (corroboration only).** The current target lies after gridflow's local
Elexon forecast holdings, so no equality join was possible for this body (FACTS DEM1-1, C8).
`TODO: verify` definitive Elexon equivalence by issue. It needs overlapping NESO and Elexon
captures from the same forecast publication.

**Activation (2026-10-09, master `73fde80`).** Transformed with cutoff 2026-10-08 (one
capture). Silver has **12 rows**, equal to the planned count. No prior silver existed, so
nothing was overwritten. Reconcile `--all --cutoff 2026-10-08` found 0 gaps over 36 recorded
families (gridflow `@.planning/v0.22-RESULTS.md` §DEM-1; RULINGS 531–533).

Silver columns beyond the eight vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (all timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1,
epoch 1).

### `demand_forecast_2d_files`

- Kind: files · archetype: FC · refresh: intraday · empty allowed: no
- files: catalogue only

This family captures the cardinal-point demand-curve PNG (see DOC above). It explains the
cardinal-point labels visually. It does not settle the CP clock zone.

### `demand_forecast_2d_historic_day_ahead`

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

**Held.** This family's silver exists on disk but is not eligible for publication or
point-in-time use (see Holds). This page gives schema, units and counts only, no data values.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
   `last_modified` of the captured archive, `2026-10-07T15:15:12.392517` (no offset, read as UTC
   per ADR-030 D-15). It is shared by all 14,608 rows. It says when the archive file last
   changed, not when any row's forecast was made. Rows for long-past targets carry the
   same vintage.
2. **Event time (`date_sp1` on `targetdate`).** `event_time` = `timestamp_utc` = the UTC
   instant of settlement period 1 on the target date, the same date anchor as the current
   family. It is not a cardinal-point instant. `targetdate` parses as `%Y-%m-%d` here, not the
   current file's `%Y%m%d`.

The archive's own issue clock, `FORECAST_TIMESTAMP`, is kept as a **raw string**. The issue
recipe is `none`, and the column is not used as `issue_time` (FACTS T01, DEM1-3, g2). The
dictionary calls it "the date and time at which the forecast was made", and every value carries
a `Z` suffix and parses structurally (FACTS C1). Read as UTC, the newest label falls after the
archive file's CKAN `last_modified` (itself read as UTC per ADR-030 D-15). That would place the
purported forecast creation after the recorded file modification. A UK-local reading
would resolve that, but file metadata alone does not prove it (FACTS DEM1-3, C4).
`TODO: verify` the zone and whether the timestamp is an immutable issue instant.

**Units (vendor dictionary only, [historic dictionary](https://www.neso.energy/data-portal/2-day-ahead-demand-forecast/historic_2_day_ahead_demand_forecasts)).**
`FORECASTDEMAND` **MW**; `DAYSAHEAD` **Days** (lead). `CP_ST_TIME` / `CP_END_TIME` are HHMM
clocks the dictionary describes as UK-local at the forecast date (see the conflict above).
`TARGETDATE` and `FORECAST_TIMESTAMP` are calendar/clock fields. The remaining columns are
categorical.

**Sentinels and missing values (FACTS g5).** No null-token map, and silver has zero nulls in
every column.

- `F_Point` carries the literal string `NA` on 3,479 rows and blanks (kept as empty strings) on
  5,987 rows. Both are preserved raw. `TODO: verify` what `NA` means versus blank.
- No zeros or negatives are converted, and no bounds are imposed.

**Identity and selection.** Guard key = every column, including `forecast_timestamp`. It is
unique on all 14,608 rows. FACTS C1 measured exactly one timestamp per lead/target/cardinal
point in this body. That is observed uniqueness, not evidence that a forecast is never
corrected (FACTS §2). `TODO: verify` a documented revision identity. `_latest` is
`whole_capture`. The conditional future design, `data_column(forecast_timestamp)` with
`key_latest`, waits on the clock being settled (FACTS DEM1-3).

**Coverage discrepancy.** The resource description says the archive runs "from 2018 to the most
recent forecast". The captured body starts later than 2018 (measured in FACTS §2, C1/C9).
`TODO: verify` archive completeness: an earlier vendor body or a vendor explanation would
settle it. Do not claim 2018 coverage from the description.

**Activation (2026-10-09, master `73fde80`).** Transformed with cutoff 2026-10-08: **14,608
rows**, equal to the planned count. No prior silver existed, and reconcile found 0 gaps
(gridflow `@.planning/v0.22-RESULTS.md` §DEM-1; RULINGS 532–533).

## Cadence

- Registry refresh: intraday
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live
- Intraday: captured once per refresh run — sampled, not complete

The current resource's description states "Publication frequency: daily" and "Publication time:
between 16:15 and 17:00 (clock time)". Each upload replaces the current file with the next
target date and a new filename. gridflow keeps one snapshot per refresh run, so a missed day is
a missed forecast in the current family. Whether the archive then backfills that day is
`TODO: verify`. The archive appears to be re-uploaded on the same schedule: its vintage is 12
seconds after the current file's. `TODO: verify` whether past archive rows are ever rewritten.
Only repeated captures compared row by row can show this. No scheduled gridflow refresh exists
yet, so captures are on demand.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `demand_forecast_2d_historic_day_ahead`: held: TODO: FORECAST_TIMESTAMP zone is undocumented (values carry Z but sit after the file's CKAN last_modified when read as UTC); whether it is the immutable issue instant (unit E-SEM)

The archive silver exists on disk but is **held**. It is not eligible for publication or for
point-in-time model use until unit E-SEM answers the question above (RULINGS 529). Without a
trusted per-row issue clock, the only availability clock is the archive's CKAN vintage. That
vintage post-dates almost every row's target, so the archive cannot serve as a point-in-time
forecast history. Availability is not backdated to target minus lead or to a `Z`-read
timestamp (FACTS g2). The current family does not have this problem: in the capture to date its
single target lies after its vintage, and the forward-target test pins that property. That is
why it is eligible.

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. Holds are per family: `demand_forecast_2d_day_ahead` is eligible,
`demand_forecast_2d_historic_day_ahead` is held.

Related holds on the same question (gridflow `@docs/neso_data_portal/eligibility.md`): the
1-day archive (`demand_forecast_1d_historic_day_ahead`, which adds vendor-documented
email-recovery timestamps), the 7-day archive (`national_forecast_7d_historic_day_ahead`) and
the 2–14-day archive (`national_demand_fc_2_14d_historic_day`). The last two add that the field
has no vendor definition. All are unit E-SEM.
