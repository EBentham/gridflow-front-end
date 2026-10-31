---
source: "neso_data_portal"
package: "7-day-ahead-national-forecast"
dataset_keys: ["national_forecast_7d_day_ahead_demand", "national_forecast_7d_historic_day_ahead"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Seven-day-ahead national demand forecast
  summary: >-
    NESO's forecast of GB national demand seven days ahead, at the target day's peaks, troughs and
    fixed times, in MW.
  facts:
    vendor: "NESO Data Portal, package `7-day-ahead-national-forecast`: two CSV files"
    cadence: Daily, between 16:15 and 17:00 clock time
    grain: "One row per target date and cardinal point: a peak, trough or fixed time"
    history: NESO's archive file holds seven-day-ahead forecasts from 2018
  landscape: power
  what_it_is: >-
    NESO forecasts national demand (the GB generation requirement, excluding station load,
    pump-storage pumping and interconnector exports) seven days ahead, at the target day's cardinal
    points: peaks, troughs and fixed times. The current file holds one target date. NESO describes the
    archive as all 7-day-ahead forecasts from 2018; as of 16 October 2026 it skips from June 2018 to
    April 2023.
  how_used:
    - Benchmark a week-ahead demand model at the evening peak and overnight trough
    - Set beside Elexon's daily demand outlook for the same target day
    - "Week-ahead shape features for price models: the gap between evening peak and trough"
  chart:
    type: bar
    silver: neso_data_portal/national_forecast_7d_day_ahead_demand
    filter:
      - {column: targetdate, op: eq, value: "2026-10-23"}
    dedup: {"on": [targetdate, cardinalpoint], order_by: published_at}
    group: cardinalpoint
    group_map:
      "1F": "00:30 fixed"
      "1S": "01:00-01:30 trough"
      "1A": "02:00-02:30 peak"
      "4": "04:00 fixed"
      "1B": "04:30-07:30 trough"
      "2F": "08:00 fixed"
      "2A": "08:30-12:00 peak"
      "2B": "12:30-13:00 peak"
      "3B": "13:30-16:30 trough"
      "3C": "17:00-18:00 peak"
      "4B": "18:30-20:00 peak"
      "4C": "24:00 fixed"
    value: forecastdemand
    aggregation: last
    sort: label
    unit: MW
  chart_view:
    title: Forecast national demand by cardinal point, 23 October 2026
    caption: >-
      Silver `national_forecast_7d_day_ahead_demand`, MW: NESO's forecast for Friday 23 October 2026,
      in the file stamped 15:15 on 16 October, read as UTC; one bar per cardinal point. Windows as NESO
      writes them, labelled UTC in its dictionary but unconfirmed.
    alt: >-
      Horizontal bar chart from neso_data_portal/national_forecast_7d_day_ahead_demand: NESO's
      forecast national demand in MW for 23 October 2026, made seven days ahead, one bar per cardinal
      point in time order. From 22,507 at 00:30 it falls to the 19,192 trough over 04:30-07:30, rises
      to a 30,121 peak over 08:30-12:00, dips to 25,825 over 13:30-16:30, reaches the day's highest,
      32,182, over 18:30-20:00, and ends at 22,304 at 24:00.
    key:
      - {series: forecastdemand, label: Forecast national demand, paint: petrol,
         note: "A peak is its window's highest demand, a trough its lowest; fixed is one time"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each file downloaded whole unless its
      `last_modified` is unchanged. Dates select nothing; each daily upload replaces the current file.
    commands:
      - {run: gridflow ingest neso_data_portal national_forecast_7d_day_ahead_demand --last 24h,
         comment: whole file; window must end recently}
      - {run: gridflow transform neso_data_portal national_forecast_7d_day_ahead_demand --last 24h,
         comment: the capture's date to silver}
  record:
    select:
      filter:
        - {column: targetdate, op: eq, value: "2026-10-23"}
        - {column: cardinalpoint, op: in, value: ["1F", "1S", "1B", "2A", "2B", "3B", "3C", "4B"]}
      dedup: {"on": [targetdate, cardinalpoint], order_by: published_at}
      columns: [targetdate, cardinalpoint, cp_type, cp_st_time, cp_end_time, forecastdemand, f_point,
                published_at, daysahead]
    key: [targetdate, cardinalpoint, published_at]
    caption: Eight of the 12 cardinal points forecast for 23 October 2026, in NESO's order.
    fields:
      targetdate: The day the forecast is for; NESO sends it as `YYYYMMDD`
      cardinalpoint: NESO's code for the point; NESO does not list what the codes mean
      cp_type: "`F` a fixed time, `T` a trough (window minimum), `P` a peak (window maximum)"
      cp_st_time: Window start, `HHMM` text without leading zeros; NESO labels it UTC, unconfirmed
      cp_end_time: Window end, same encoding; equals the start at fixed points; `2400` ends the day
      forecastdemand: Forecast national demand at the point, MW
      f_point: "`Om`, `DM`, `Dm`, `EM`: overnight minimum, daytime peak, daytime minimum, evening peak; else empty"
      published_at: NESO's last-modified time for the file, read as UTC; rows carry no issue time
      daysahead: Days ahead of the target date; 7 for this file
      timestamp_utc: Start of the target date's first settlement period, UTC; not a point's time
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `tail()` reads the `_latest` view (the newest capture's rows, newest target date first), lineage
      columns dropped. Times arrive in the session zone, so the first cell converts them to UTC and sorts
      by window start.
    cells:
      - |
        df = data.neso_data_portal.tail("national_forecast_7d_day_ahead_demand")
        for c in ["timestamp_utc", "published_at", "capture_written_at"]:
            df[c] = df[c].dt.tz_convert("UTC")
        df = df.assign(start=df.cp_st_time.astype(int)).sort_values("start")
        df[["targetdate", "cardinalpoint", "cp_type", "cp_st_time", "cp_end_time",
            "forecastdemand", "f_point", "published_at"]]
      - |
        label = df.cp_st_time.str.zfill(4) + " " + df.cardinalpoint
        ax = df.set_index(label).forecastdemand.plot.bar(
            figsize=(8, 3.5), color="#155A6E", width=0.8, rot=45,
            xlabel="window start (NESO's HHMM, zero-padded) and cardinal point",
            ylabel="forecast national demand, MW");
    needs: a recent capture of NESO's seven-day-ahead national demand forecast file
    plot_alt: >-
      Bar plot of NESO's forecast national demand in MW for 23 October 2026, one bar per cardinal point,
      labelled by window start and code. The lowest is 19,192 at 0430 1B, the overnight trough; the
      highest is 32,182 at 1830 4B, the evening peak, after 31,090 at 1700 3C.
  related:
    - {dataset: neso_data_portal/1-day-ahead-demand-forecast, note: "The same cardinal points, forecast one day ahead"}
    - {dataset: neso_data_portal/2-14-days-ahead-national-demand-forecast, note: "Cardinal-point forecasts at every lead from 2 to 14 days"}
    - {dataset: elexon/ndfd, note: "Elexon's daily national demand outlook, 2 to 14 days ahead"}
    - {dataset: elexon/indo, note: Initial national demand outturn to score each forecast point against}
  family:
    slug: 7-day-ahead-national-forecast
    members:
      - {dataset: national_forecast_7d_day_ahead_demand,
         differs: "Newest publication only: one target date, seven days on; the file name carries it",
         request: "GET https://api.neso.energy/dataset/2b90a483-f59d-455b-be6d-3cb4c13a85d0/resource/70d3d674-15a6-4e41-83b4-410440c0b0b9/download/ng_demand_7da_20261023.csv"}
      - {dataset: national_forecast_7d_historic_day_ahead,
         differs: "What NESO calls all seven-day-ahead forecasts from 2018, each with a forecast time stamp",
         request: "GET https://api.neso.energy/dataset/2b90a483-f59d-455b-be6d-3cb4c13a85d0/resource/6f7408b4-47fd-4ae7-b1e5-f095a3a5a2dc/download/archive_7dayahead.csv",
         held: "Forecast time stamps end in Z, but NESO does not confirm UTC; the field is undocumented."}
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
**historic** file is, in NESO's words, all 7-day-ahead forecasts from 2018 (its target dates
skip from June 2018 to April 2023 in both captures; see Files), with a
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
- Recaptured 2026-10-16: `raw_20261016T204058Z_70d3d674-15a6-4e41-83b4-410440c0b0b9_ccd2871d.csv`
  (file `ng_demand_7da_20261023.csv`, CKAN `last_modified` `2026-10-16T15:15:01.261954`), 578 bytes,
  12 data rows, all targeting 2026-10-23, same header. Silver holds 12 rows per capture, equal to
  bronze; no row repeats across the two captures (different target dates).

**Historic 7 Day Ahead Demand Forecasts** (family `national_forecast_7d_historic_day_ahead`)

- Download:
  [archive_7dayahead.csv](https://api.neso.energy/dataset/2b90a483-f59d-455b-be6d-3cb4c13a85d0/resource/6f7408b4-47fd-4ae7-b1e5-f095a3a5a2dc/download/archive_7dayahead.csv)
  (stable filename; CKAN datastore active).
- Resource description: "All historic 7 day ahead demand forecasts from 2018 to the most recent
  forecast."
- Observed in both captures: target dates run 2018-04-01 to 2018-06-28, then nothing until
  2023-04-08, then daily to the newest target, missing only 2023-04-17, 2024-08-28, 2024-12-14
  and 2026-09-07. So "all ... from 2018" is NESO's description, not the file's coverage.
- Captured: `raw_20261008T111319Z_6f7408b4-47fd-4ae7-b1e5-f095a3a5a2dc_61a5e08c.csv`,
  1,043,045 bytes, 15,703 data rows, one header epoch.
- Recaptured 2026-10-16: `raw_20261016T204103Z_6f7408b4-47fd-4ae7-b1e5-f095a3a5a2dc_8f23eead.csv`
  (CKAN `last_modified` `2026-10-16T15:15:09.731374`), 1,050,209 bytes, 15,811 data rows, same
  header. Silver equals bronze in each capture.

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
   `last_modified` of the captured file. For the two captures to date that is
   `2026-10-07T15:15:00.672524` (2026-10-08 capture) and `2026-10-16T15:15:01.261954`
   (2026-10-16 capture), which CKAN emits without an offset; gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`, D-15). The 12
   silver rows of each capture share that capture's vintage. The file has no issue column, so the
   vintage is the only availability clock.
   Observed, no inference drawn: 15:15 UTC is 16:15 BST, the start of the vendor's stated
   16:15–17:00 "clock time" publication window; both vintages, and the catalogue snapshot's
   `2026-10-06T15:15:02`, fall at 15:15 read as UTC.
2. **Event time (`date_sp1` on `targetdate`).** `event_time` = `timestamp_utc` = the start of
   settlement period 1 of the target date, i.e. UK local midnight converted to UTC. For target
   2026-10-14 (BST) that is `2026-10-13 23:00 UTC` on every row (checked 2026-10-09), and for
   target 2026-10-23 `2026-10-22 23:00 UTC` (2026-10-16 capture, checked 2026-10-24). This is
   **not** the capture time, and it is **not** the instant of any cardinal point: it anchors
   the target calendar date only (FACTS T04, g1). The CP's position within the day is in the
   raw `cp_st_time` / `cp_end_time` strings, which are not parsed (see Units).

**Why it is eligible (RULINGS 529).** Every target date in the file is later than the date of
its CKAN `last_modified`: the capture's target 2026-10-14 is seven days after the vintage date
2026-10-07, and the 2026-10-16 capture's target 2026-10-23 is seven days after its vintage date
2026-10-16. A forecast published before the day it forecasts cannot be a hindsight value, so
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
  T01). All rows of both captures carry `7`.
- `cp_st_time`, `cp_end_time`: HHMM clock encodings, not quantities. The dictionary describes
  both as "Time UTC". FACTS g1 records that the dictionary's UTC statement conflicts with the
  UK-local alignment measured for medium-term families, so both are kept as raw strings.
  `TODO: verify` the zone of the CP clocks for this package with the vendor. Observed: the
  tokens are not zero-padded (`30`, `100`, `2400`), fixed-type points carry equal start and
  end, and the last fixed point carries `2400`.
- `cardinalpoint`, `cp_type`, `f_point`: categorical text. The dictionary lists `cp_type` as
  Fixed / Trough / Peak (`F` / `T` / `P` in the data). `TODO: verify` the full vendor
  definition of each cardinal-point code (each capture carries `1F`, `1S`, `1A`, `4`, `1B`,
  `2F`, `2A`, `2B`, `3B`, `3C`, `4B`, `4C`, with the same windows on 14 and 23 October); the
  dictionary describes CPs in general terms only.
- `targetdate`: calendar date, no unit.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- A blank `F_Point` is kept as the vendor's **empty string** `""`, not converted to null
  (8 of the 12 rows in each capture). Only the four forecasting-point rows carry a label.
- No `NA` token occurs in this package.
- No zero or `-1` handling applies; no bounds are imposed on `forecastdemand`.
- Observed, unresolved: the dictionary comment defines the forecasting points as OM, DM, Dm,
  EM, with windows stated as "half hour ending" times; the data carries `Om`, not `OM`, for the
  overnight minimum. `TODO: verify` the casing is the same label, and the clock the "half hour
  ending" windows use.

**Identity and selection.** The entity key is **every column**: a capture-level duplicate
guard, not a revision identity (FACTS T05, g3; gridflow
`@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md`). The CP candidate
`(daysahead, targetdate, cardinalpoint)` was measured unique on each capture but is not frozen
as a business key, because no vendor text guarantees it across revisions. `_latest` is
`whole_capture`: the newest capture wins as a whole, which suits a file that holds one target
day. `TODO: verify` the vendor's revision identity for a CP forecast.

**Current versus archive.** All 12 rows of the current capture appear, equal on lead, target,
CP and value, in the historic archive captured the same morning (FACTS C4). The archive
therefore already carries the newest forecast. Every archive row in that correspondence had a
single `FORECAST_TIMESTAMP` per lead/target/CP. The same held on 2026-10-16: all 12 rows of the
current file (target 2026-10-23) equal the archive captured that evening on lead, target, CP,
value and window, with label `2026-10-16T11:21:21Z`; the 2026-10-14 rows are still in it,
unchanged, labelled `2026-10-07T12:47:45Z`. Unlike the 1-day package, this archive kept the
publication the current file showed, in both captures.

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
   `last_modified` of the captured archive file, read as UTC (ADR-030 D-15):
   `2026-10-07T15:15:13.758197` for the 15,703 rows of the 2026-10-08 capture and
   `2026-10-16T15:15:09.731374` for the 15,811 rows of the 2026-10-16 capture. It says when the
   archive file changed, not when any row's forecast was issued. Between the two captures all
   15,703 earlier rows stayed unchanged and 108 were added: 12 rows for each target date from
   2026-10-15 to 2026-10-23, one label each.
2. **Event time (`date_sp1` on `targetdate`).** `event_time` = `timestamp_utc` = the UTC
   instant of UK local midnight starting each row's target date; `event_time` equals
   `timestamp_utc` on every row (checked 2026-10-09). It is not the capture time and not a CP instant; it anchors the target date
   only (FACTS T05, g1).

**`FORECAST_TIMESTAMP` is kept raw.** It is a string column, issue recipe `none`, and no
`issue_time` is derived (gridflow
`@tests/unit/test_neso_dem1_records.py::test_historic_forecast_timestamp_is_kept_raw_and_no_issue_time_is_derived`).
Every value carries a `Z` suffix and parses structurally (FACTS C1), and the archive has
exactly one timestamp per lead/target/CP (15,703 groups on 2026-10-08, FACTS C1; 15,811 on
2026-10-16), and one per target date in both captures. Observed in both captures: on 15,750
of the 15,811 rows the label's date is seven days before the target date; 13 rows (target
2018-05-01) are six days before; and 48 rows, the 12 points of targets 2018-04-01, 04-02,
04-03 and 04-05, are labelled `2018-05-18T11:42:55Z` to `11:51:13Z`, 43 to 47 days **after**
the day they forecast. So for those rows the label cannot be the issue instant. The vendor dictionary
entry for the field is **empty**: no title, description or unit (field-info snapshot
2026-10-08; FACTS T04). Its meaning (forecast-made time or something else), its actual zone,
and whether it is fixed at issue are all unestablished.

Note on the hold text: an earlier generated hold question said the labels "sit after the
file's CKAN last_modified when read as UTC". FACTS DEM1-3 drew that from the 1-day, 2-day and
2–14-day archives; this archive was not in that table. The registry question now reads "has
no vendor definition and its zone is undocumented (values carry Z); whether it is the
immutable issue instant" (gridflow
`@src/gridflow/connectors/neso_data_portal/registry/7-day-ahead-national-forecast.json`). For
this 7-day archive the measurement goes the other way: the label on the archive rows matching
the current forecast, read as UTC, sits before the file's `last_modified` (FACTS C4), and in
each capture every label, read as UTC, is earlier than that capture's `last_modified` (newest
labels `2026-10-07T12:47:45Z` and `2026-10-16T11:21:21Z`). That does not lift the
hold. The field still has no vendor definition, and an ordering check against file
modification time cannot establish its zone or meaning. `TODO: verify` with the vendor.

**Units.** As for the current family: `forecastdemand` **MW** (archive dictionary
`unit: MW`; FACTS T02/g4,
[vendor dictionary](https://www.neso.energy/data-portal/7-day-ahead-national-forecast/historic_7_day_ahead_demand_forecasts));
`daysahead` lead in days (FACTS T01); CP clocks HHMM strings that the dictionary labels
"Time UTC", kept raw (FACTS T02/T03; `TODO: verify` zone).

**Sentinels (FACTS g5).** Blank `F_Point` cells are present and kept as the empty string `""`;
no `NA` token occurs in this archive (unlike the 1-day and 2-day archives). `F_Point` carries
the `Om` spelling here too. No null token, no bounds. All silver columns have zero nulls in
both captures.

**Identity and selection.** Entity key = every column, a guard key (FACTS T06, g3). The archive
candidate `(daysahead, targetdate, cardinalpoint, forecast_timestamp)` and the narrower
`(targetdate, cardinalpoint)` were both measured unique on each capture. `whole_capture`
selection; a future `key_latest` on target + CP + lead with an `issue_time` in the key becomes
possible only once the timestamp's clock is supplied (FACTS DEM1-3). `TODO: verify` the
vendor's revision identity.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The current-file resource description states daily publication between 16:15 and 17:00 "clock
time" (UK local is the natural reading; `TODO: verify` the vendor means UK local). The
package carries no "Update Frequency" extra. gridflow has two captures of each resource
(2026-10-08 and 2026-10-16), each taken on demand. Observed across the 2026-10-06 snapshot and
the two captures: the current file holds a single target day and its filename moved from one
target date to the next (`..._20261013`, `..._20261014`, `..._20261023`). `TODO: verify` whether
each upload replaces the previous forecast outright, so that a day not captured is recoverable
only from the archive (in both captures the archive held the current file's rows). Between the
two captures the archive kept all 15,703 earlier rows unchanged and added 108 (nine target
dates), which fits a daily append; `TODO: verify` whether it is ever rewritten (two captures
cannot rule it out).

**Activation (2026-10-09, master `73fde80`, PR #89).** Both families were transformed with
cutoff 2026-10-08 (one capture each). Silver holds **12 rows** (current) and **15,703 rows**
(archive), equal to the planned counts. No prior silver existed, so nothing was overwritten.
Reconcile `--all --cutoff 2026-10-08` exited 0 with 0 gaps over 36 recorded families
(gridflow `@.planning/v0.22-RESULTS.md` §DEM-1; RULINGS 531–533). Silver path:
`C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`.
The 2026-10-16 captures were transformed the same evening, adding one silver file per family:
the current table now holds 24 rows over two files (12 in `_latest`), the archive 15,703 and
15,811 rows in its two files (the newer 15,811 in `_latest`).

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

- `national_forecast_7d_historic_day_ahead`: held: TODO: FORECAST_TIMESTAMP has no vendor definition and its zone is undocumented (values carry Z); whether it is the immutable issue instant (unit E-SEM)

The archive's silver exists on disk but is **held**: not eligible for publication or
point-in-time model use until unit E-SEM answers the question above (RULINGS 529). Without a
defined issue clock, the CKAN vintage only bounds when the archive file existed. It cannot say
when each past forecast was known, so a row cannot be placed at its true availability time.
This page therefore publishes the archive's schema, row count, clock recipes and target-date
coverage only, not its forecast values or time stamps. The measured ordering against `last_modified` for this package is
described under the family (it differs from the earlier generated wording) and does not lift the
hold; the four April 2018 targets labelled after the day they forecast show the label is not
always an issue time.

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. The hold is per family and sits on `national_forecast_7d_historic_day_ahead`; the
current family `national_forecast_7d_day_ahead_demand` is eligible.

Related holds (gridflow `@docs/neso_data_portal/eligibility.md`): the 1-day, 2-day and
2–14-day historic archives are held on the same `FORECAST_TIMESTAMP` question (the 1-day adds
vendor-documented email-recovery times); the 2–14-day half-hourly family and
`daily_demand_update` are held on their own questions. All are unit E-SEM.
