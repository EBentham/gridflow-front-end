---
source: "neso_data_portal"
package: "2-14-days-ahead-national-demand-forecast"
dataset_keys: ["national_demand_fc_2_14d_days_ahead", "national_demand_fc_2_14d_days_ahead_half", "national_demand_fc_2_14d_historic_day"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Two-week national demand forecast
  summary: >-
    NESO's GB national demand forecast for each day 2 to 14 days ahead, at its peaks, troughs and
    fixed times, in MW.
  facts:
    vendor: "NESO Data Portal, package `2-14-days-ahead-national-demand-forecast`: three CSV files"
    cadence: Twice daily, at 09:20 and 14:20 by NESO's notes, which give no zone
    grain: "One row per target date and cardinal point: a peak, trough or fixed time"
    history: NESO's archive file holds 2 to 14 day forecasts from 2020
  landscape: power
  what_it_is: >-
    NESO forecasts national demand (GB generation requirement, excluding station load, pump-storage
    pumping and interconnector exports) 2 to 14 days ahead at each day's cardinal points, a set that
    changed at the October clock change. NESO describes the archive as all forecasts since 2020; from
    19 September to 16 October 2026 it kept one of each day's two updates.
  how_used:
    - Benchmark a two-week demand model at the evening peak and overnight minimum
    - Set beside Elexon's daily `NDFD` forecast for the same target dates
    - Track how one day's forecast moves as its lead shortens, capture by capture
  chart:
    type: line
    silver: neso_data_portal/national_demand_fc_2_14d_days_ahead
    time: targetdate
    filter:
      - {column: published_at, op: ge, value: "2026-10-16T00:00:00+00:00"}
      - {column: f_point, op: in, value: [EM, Om]}
    dedup: {"on": [targetdate, f_point], order_by: published_at}
    group: f_point
    group_map: {EM: evening, Om: overnight}
    series_order: [evening, overnight]
    value: forecastdemand
    aggregation: last
    window: {start: "2026-10-18", end: "2026-10-30"}
    unit: MW
  chart_view:
    title: Evening peak and overnight minimum, 18 to 30 October 2026
    x_label: target date, 2 to 14 days ahead
    caption: >-
      Silver `national_demand_fc_2_14d_days_ahead`, MW, from the file stamped 15:19 on 16 October 2026
      (read as UTC): rows NESO marks `EM` and `Om`, one per target date. From 25 October the evening
      peak window is 17:00-18:00, not 18:30-20:00, as NESO writes them.
    alt: >-
      Line chart from neso_data_portal/national_demand_fc_2_14d_days_ahead: NESO's forecast national
      demand in MW for target dates 18 to 30 October 2026, two lines. The evening peak starts at
      33,421, reaches 35,929 on 19 October, falls to 31,454 on Saturday 24 October, then climbs to its
      highest, 37,809, on 28 October and ends at 36,330. The overnight minimum eases from 21,664 on 20
      October to its lowest, 17,303, on 26 October, then holds near 20,400.
    key:
      - {series: evening, label: Evening peak, paint: petrol,
         note: "`EM`: highest demand of half-hours ending 17:00 to 24:00, per NESO's 1-day, 2-day and 7-day dictionaries"}
      - {series: overnight, label: Overnight minimum, paint: clay,
         note: "`Om`: lowest demand of half-hours ending 00:30 to 07:30, per NESO's 1-day, 2-day and 7-day dictionaries"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each file downloaded whole unless its
      `last_modified` is unchanged. The current file's name carries its last target date.
    commands:
      - {run: gridflow ingest neso_data_portal national_demand_fc_2_14d_days_ahead --last 24h,
         comment: whole file; window must end recently}
      - {run: gridflow transform neso_data_portal national_demand_fc_2_14d_days_ahead --last 24h,
         comment: the capture's date to silver}
  record:
    select:
      filter:
        - {column: published_at, op: ge, value: "2026-10-16T00:00:00+00:00"}
        - {column: targetdate, op: in, value: ["2026-10-24", "2026-10-26"]}
        - {column: cardinalpoint, op: in, value: ["1B", "2A", "3C", "4B", "DP"]}
      dedup: {"on": [targetdate, cardinalpoint], order_by: published_at}
      order_by: [targetdate]
      columns: [targetdate, cardinalpoint, cp_type, cp_st_time, cp_end_time, forecastdemand, f_point,
                daysahead, published_at]
    key: [targetdate, cardinalpoint, published_at]
    caption: Four points each on 24 and 26 October 2026, either side of the clock change.
    fields:
      targetdate: The day the forecast is for; NESO sends it as `YYYYMMDD`
      cardinalpoint: NESO's code for the point; a code can change meaning, as `4B` does here
      cp_type: "`F` a fixed time, `T` a trough (window minimum), `P` a peak (window maximum)"
      cp_st_time: Window start, `HHMM` without leading zeros; NESO says UTC, the data suggest UK time
      cp_end_time: Window end, same encoding; equals the start at fixed points; `2400` ends the day
      forecastdemand: Forecast national demand at the point, MW
      f_point: "`Om`/`DM`/`Dm`/`EM`: overnight low, daytime peak and low, evening peak (NESO's 1-, 2-, 7-day dictionaries)"
      daysahead: "Days ahead, NESO's D+n: the target is n days after publication"
      published_at: NESO's last-modified time for the file, read as UTC; rows carry no issue time
      timestamp_utc: Start of the target date's first settlement period, UTC; not a point's time
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `tail()` reads the `_latest` view (the newest capture's rows, newest target date first), lineage
      columns dropped; `n=200` covers the whole file. Times arrive in the session zone, so the first
      cell converts them to UTC.
    cells:
      - |
        df = data.neso_data_portal.tail("national_demand_fc_2_14d_days_ahead", n=200)
        for c in ["timestamp_utc", "published_at", "capture_written_at"]:
            df[c] = df[c].dt.tz_convert("UTC")
        pts = df[df.f_point.isin(["EM", "Om"])].sort_values(["targetdate", "f_point"])
        pts[["targetdate", "daysahead", "cardinalpoint", "cp_st_time", "cp_end_time",
             "f_point", "forecastdemand", "published_at"]]
      - |
        ax = pts.pivot(index="targetdate", columns="f_point", values="forecastdemand").plot(
            figsize=(8, 3.5), marker="o", color={"EM": "#155A6E", "Om": "#9A5B3C"},
            xlabel="target date", ylabel="forecast national demand, MW");
    needs: a recent capture of NESO's 2 to 14 day cardinal point file
    plot_alt: >-
      Line plot of NESO's forecast national demand in MW by target date, 18 to 30 October 2026. The
      EM line (evening peak) dips from 35,929 on 19 October to 31,454 on 24 October, then rises to
      37,809 on 28 October; the Om line (overnight minimum) runs from 21,664 on 20 October down to
      17,303 on 26 October.
  related:
    - {dataset: neso_data_portal/2-day-ahead-demand-forecast, note: "The same cardinal points two days ahead, in NESO's separate file"}
    - {dataset: neso_data_portal/7-day-ahead-national-forecast, note: The same points for one target date seven days ahead}
    - {dataset: elexon/ndfd, note: "Elexon's 2 to 14 day national demand forecast, one figure a date"}
    - {dataset: elexon/indo, note: Initial national demand outturn to score each forecast point against}
  family:
    slug: 2-14-days-ahead-national-demand-forecast
    members:
      - {dataset: national_demand_fc_2_14d_days_ahead,
         differs: "Latest publication: cardinal points for days 2 to 14; the file name is dated",
         request: "GET https://api.neso.energy/dataset/633daec6-3e70-444a-88b0-c4cef9419d40/resource/9af18ed4-efc8-4779-bef5-c0927fee9b0a/download/ng_demand_14da_20261030.csv"}
      - {dataset: national_demand_fc_2_14d_days_ahead_half,
         differs: "The same forecast as a half-hourly curve, by UK clock and by UTC",
         request: "GET https://api.neso.energy/dataset/633daec6-3e70-444a-88b0-c4cef9419d40/resource/7c0411cd-2714-4bb5-a408-adb065edf34d/download/ng-demand-14da-hh.csv",
         held: "NESO does not say whether each UTC time starts or ends its half-hour."}
      - {dataset: national_demand_fc_2_14d_historic_day,
         differs: "2 to 14 day forecasts NESO has kept since 2020, with forecast time stamps",
         request: "GET https://api.neso.energy/dataset/633daec6-3e70-444a-88b0-c4cef9419d40/resource/4dd712a2-ee2c-455d-a9c0-9d3564c80fa0/download/archive_14dayahead.csv",
         held: "Forecast time stamps end in Z, but NESO does not confirm UTC; the field is undocumented."}
---

# 2-14 Days Ahead Demand Forecast

NESO's medium-term GB **national demand (ND)** forecast, from 2 to 14 days ahead, published as
three CSV uploads on the Open Data Portal. The package notes say the files are "updated twice
daily, at 09:20 and 14:20". The three files are:

- **Cardinal Point Forecast.** For each lead of 2–14 days, one forecast for each **cardinal
  point** of the target day: the fixed times, troughs and peaks that recur in the daily demand
  shape.
- **Half Hourly Forecast.** The same horizon as a half-hourly curve.
- **Historic archive.** NESO describes it as "All historic 2-14 day ahead demand forecasts from
  2020 to the most recent forecast". Its 2026-10-16 capture holds one issue per publication day
  for every day from 2026-09-19 to 2026-10-16, although the files update twice daily (see
  Cadence).

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
  6,328 bytes, 156 data rows. Recaptured 2026-10-16:
  `raw_20261016T204046Z_9af18ed4-efc8-4779-bef5-c0927fee9b0a_3cc7e796.csv`
  (`ng_demand_14da_20261030.csv`), 6,133 bytes, **151** data rows; the stamp again equals the
  last target date (2026-10-30). Fewer rows because the cardinal-point set changes at the clock
  change (see Shape of a capture), not a missing day.
- **Half Hourly Forecast** → `national_demand_fc_2_14d_days_ahead_half` (held).
  Download: [ng-demand-14da-hh.csv](https://api.neso.energy/dataset/633daec6-3e70-444a-88b0-c4cef9419d40/resource/7c0411cd-2714-4bb5-a408-adb065edf34d/download/ng-demand-14da-hh.csv).
  Captured: `raw_20261008T111304Z_7c0411cd-2714-4bb5-a408-adb065edf34d_9454ade5.csv`,
  29,113 bytes, 624 data rows. Recaptured 2026-10-16:
  `raw_20261016T204050Z_7c0411cd-2714-4bb5-a408-adb065edf34d_f47cc5af.csv`, 29,159 bytes,
  625 data rows (the clock-change day 2026-10-25 has 49).
- **Historic 2-14 Day Ahead Demand Forecasts** → `national_demand_fc_2_14d_historic_day` (held).
  Download: [archive_14dayahead.csv](https://api.neso.energy/dataset/633daec6-3e70-444a-88b0-c4cef9419d40/resource/4dd712a2-ee2c-455d-a9c0-9d3564c80fa0/download/archive_14dayahead.csv).
  Captured: `raw_20261008T111309Z_4dd712a2-ee2c-455d-a9c0-9d3564c80fa0_2f070940.csv`,
  24,824,849 bytes, 370,700 data rows. Recaptured 2026-10-16:
  `raw_20261016T204055Z_4dd712a2-ee2c-455d-a9c0-9d3564c80fa0_58669bdc.csv`, 24,907,331 bytes,
  371,933 data rows.

All three resources are `datastore_active` in CKAN. The datastore totals at a field-info read
on 2026-10-08 (156 / 624 / 370,700) matched the 2026-10-08 captured row counts. Each capture has
one header epoch, and in every capture silver rows equal bronze data rows. No row repeats within a
capture, and no current-file or half-hourly row repeats across the two captures (their target dates
overlap on 18 to 22 October, but every value there was revised).

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
   `last_modified` of the captured resource: `2026-10-08T08:45:03.632388` for the 2026-10-08
   capture and `2026-10-16T15:19:59.536755` for the 2026-10-16 capture. CKAN emits it without an
   offset, and gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Every row of a
   capture shares this vintage. The file has **no issue column**, so the vintage is the only
   availability clock. Do not borrow the archive's `FORECAST_TIMESTAMP` for this family
   (FACTS g2).
2. **Event time (`date_sp1` on `targetdate`).** `timestamp_utc` = `event_time` = the start of
   settlement period 1 (00:00 UK local time) on the target date, converted to UTC. During BST
   that is 23:00 UTC on the previous day. This held on all 156 silver rows (checked
   2026-10-09) and on all 151 rows of the 2026-10-16 capture, whose targets cross the clock change
   (23:00 UTC through 2026-10-25, 00:00 UTC from 2026-10-26). Event time is the target day, **not the capture time**. The `none` fallback
   (timestamp_utc = capture time) does not apply to any family in this package. The anchor is
   date-level only. It does not place the cardinal point within the day, and all 12 points of
   a target day share one `timestamp_utc`.

**Why this family is eligible (RULINGS 529).** In the activated capture every target date
(2026-10-10 → 2026-10-22, leads 2 → 14) falls after the capture's CKAN `last_modified` date
(2026-10-08). The same holds in the 2026-10-16 capture (targets 2026-10-18 → 2026-10-30, after
its 2026-10-16 vintage). So the vintage is a true "known by" time for every forecast in the file: a value
cannot have been observed after the file that already contained it. A test pins this property
(gridflow `@tests/unit/test_neso_dem1_records.py`, `_forward_violations`). It fails when a
fixture contains a past target.

**Shape of a capture.** The 2026-10-08 capture has 156 rows: 13 leads (`daysahead` 2–14) × 12
cardinal points. In both captures each lead has exactly one target date, and lead *n* targets the
capture date + *n* days. The cardinal points in the 2026-10-08 capture (vendor codes, kept
verbatim):

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

**The point set changes at the clock change (2026-10-16 capture, 151 rows).** Targets
2026-10-18 to 2026-10-24 carry the 12 points above (3C 1700 → 1800, 4B 1830 → 2000 on every
day). The clock-change day 2026-10-25 carries 12 points in a new layout: `3C` is gone, a new
`DP` (P, 1700 → 1800, `f_point` `EM`) is the evening peak, `4B` becomes a **fixed** point at
2100 → 2100 with blank `f_point`, and `1A` widens to 100 → 230. From 2026-10-26 to 2026-10-30
`1S` is also gone, leaving 11 points. So 7 × 12 + 12 + 5 × 11 = 151; every target date is
present. The code `4B` therefore names a peak window before the change and a fixed time after it:
a code alone is not a stable point identity. `f_point` also moves: on 2026-10-30 `Om` sits on
`L04` (fixed, 400), not `1B`. The vendor dictionary's own example `CARDINALPOINT` value is `DP`.

The vendor dictionary describes `CP_TYPE` as Fixed / Trough / Peak (`F` / `T` / `P`). It
describes `F_Point` as the forecasting points "overnight demand minimum, daytime demand maximum,
daytime demand minimum and evening demand maximum", but does not pair them with codes. NESO's
dictionaries for the 1-day, 2-day and 7-day packages do (field-info `20261008T114228Z`, `F_Point`
comment): Overnight minimum (OM), minimum national demand between half hour ending 00:30 and
07:30; Daytime peak (DM), maximum between half hour ending 08:00 and 13:00; Daytime minimum (Dm),
13:30 to 16:30; Evening peak (EM), maximum between half hour ending 17:00 and 24:00. This file
writes `Om` for OM. In both captures the `EM` row is each target day's highest value and the `Om`
row its lowest. Peak and trough windows can change between target days, as the 3C and 4B
rows show. Because the window is part of the row, the guard key includes it.

`FORECASTDEMAND` ranges from 17,358 to 36,082 MW across the 2026-10-08 capture, and from 17,303
to 37,809 MW across the 2026-10-16 capture. The first rows of
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
  the **empty string**, not null (104 of 156 rows on 2026-10-08, 99 of 151 on 2026-10-16). Filter with
  `f_point = ''`, not `IS NULL`.
- A literal `NA` in `F_Point` would also survive as the string `NA`. It does not occur in this
  capture. It occurs in the historic 1-day and 2-day archives. `TODO: verify` its meaning there.
- `FORECASTDEMAND` has no blanks and no zeros in either capture. No bounds are imposed, and
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
`@.planning/v0.22-RESULTS.md` §DEM-1; RULINGS 531–533). A second capture (2026-10-16, 151 rows)
followed; the base table now holds 307 rows and `_latest` the 151 of the newer capture.

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
   `last_modified`, read as UTC: `2026-10-08T08:46:32.246773` and, for the 2026-10-16 capture,
   `2026-10-16T15:21:36.457364`. The file has no issue column.
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
- That is strong evidence but not a vendor definition. The 2026-10-08 capture has no DST
  transition day.
- The 2026-10-16 capture (625 rows, dates 2026-10-18 to 2026-10-30) repeats the pattern: 612 of
  625 rows match `DATE` and `CTIME` in Europe/London, the other 13 are the `2400` rows. It
  includes the autumn clock change, 2026-10-25, a 25-hour day of 50 half-hours, but the file gives
  it **49** rows: `CTIME` runs `30`, `100`, `130`, `130`, `200`, with `GDATETIME` 23:30, 00:00,
  00:30, 01:30, 02:00 UTC. The repeated hour's second `100` (01:00 UTC) is absent, so one
  half-hour of that day is missing from the file. The `2400` row on that day is 2026-10-26 00:00
  UTC (midnight GMT). Spring (46-period) behaviour is still unobserved.
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
The 2026-10-16 capture added 625; no row repeats across the two (their 240 shared half-hours,
2026-10-18 to 2026-10-22, all carry revised values).

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
   `last_modified`, read as UTC: `2026-10-08T08:46:27.592963`, and `2026-10-16T15:21:30.359237`
   for the 2026-10-16 capture. This is the only availability
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
- The values are structurally `Z`-suffixed. In the 2026-10-08 capture, read literally as UTC,
  the newest of them (`2026-10-08T09:45:02Z`) sits **after** the file's own CKAN
  `last_modified` (08:46:27), which cannot be true of a creation time. UK-local reading is
  plausible but unproven (FACTS DEM1-3). The 2026-10-16 capture does not test this: its newest
  stamp (`2026-10-16T09:45:03Z`) is before that file's `last_modified` (15:21:30) either way.
- Immutability and availability at issue are not documented.

gridflow therefore keeps it as a raw string with issue recipe `none`. It is in the entity key as
a raw value only.

**Structure (counts only, FACTS C1/C4).** Each (lead, target, cardinal point) has 1 or 2
distinct timestamps (281,914 groups with 1, 44,393 with 2 in the 2026-10-08 capture; 283,147 and
44,393 in the 2026-10-16 capture). No lead and target date after 2026-10-02 has two. Across leads, a target/cardinal
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
are 0 occurrences in the activated silver (checked 2026-10-09), nor in the 2026-10-16 capture.

**Activation.** **370,700 rows**, equal to the planned count. Peak memory was 910.1 MiB, the
batch maximum (gridflow `@.planning/v0.22-RESULTS.md` §DEM-1).

**The 2026-10-16 recapture (371,933 rows).** All 370,700 rows of the 2026-10-08 capture are
present unchanged, so silver now holds them twice (the whole archive repeats per capture; any
read across captures must keep one). The 1,233 added rows are exactly eight issues, one per
publication day from 2026-10-09 to 2026-10-16, each stamped 09:45:00Z to 09:45:05Z and each
covering leads 2 to 14 (156, 156, 156, 155, 154, 153, 152, 151 rows: the shrinking count is the
winter point set entering the horizon). Target dates now run to 2026-10-30; the earliest is
still 2020-09-24.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The package notes say the files are "updated twice daily, at 09:20 and 14:20".
`TODO: verify` the zone of those times; UK local is likely but not stated. gridflow's registry
refresh is daily, so each run captures one state of the cardinal-point and half-hourly files,
and the other daily update is not retained. `TODO: verify` whether the historic archive keeps
both daily issues. Observed in the 2026-10-16 archive capture: every publication day from
2026-09-19 to 2026-10-16 (28 days) has exactly one issue, stamped about 09:45Z; 2026-09-18 and
some earlier days have two. On 2026-10-08 the current file (vintage 08:45:03) equals the
archive's `2026-10-08T09:45:02Z` issue on all 156 values. On 2026-10-16 the current file
(vintage 15:19:59, the later update by its stamp) matches the archive's only issue that day,
`2026-10-16T09:45:03Z`, on all 151 lead, target and point combinations but on only 44 values.
So for recent days the archive holds the morning issue and not the later one.

Observed at capture (no inference drawn): the three files' CKAN `last_modified` values fall
between 08:45 and 08:47 UTC on 2026-10-08 and between 15:19 and 15:22 UTC on 2026-10-16. Neither
matches NESO's "09:20 and 14:20" in UTC or UK time.

Captures to date: two per family (2026-10-08 and 2026-10-16), on demand.

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
  half-hour end (or start), and clock-change days that hold every half-hour (the 2026-10-16
  capture spans the autumn change and lists 49 of its 50; see above). The family could then move
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
