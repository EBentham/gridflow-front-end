# 14-days-ahead-operational-metered-wind-forecasts: writer's report

Family page `14-days-ahead-operational-metered-wind-forecasts`, lead `metered_wind_forecast_14d`
(eligible), member `metered_wind_forecast_14d_windfarm` (eligible). Written 2026-10-24. The page
set's lead and member list are right (same order as the note's `page.family`). Nothing is held.

Files:
- canonical note `C:\gridflow-wt\vault-neso-gen\30-vendors\neso-data-portal\datasets\14-days-ahead-operational-metered-wind-forecasts.md`
  (CRLF before and after: 0 lone LF; Edit tool only)
- mirror `C:\gridflow-wt\fe-neso-gen\vault\neso_data_portal\14-days-ahead-operational-metered-wind-forecasts.md`, `cmp` clean
- `site/hifi/data/series/neso_data_portal/metered_wind_forecast_14d.json` (gridflow-distil, `spec_origin: vault`)
- `site/hifi/data/samples/neso_data_portal/metered_wind_forecast_14d.json` (gridflow-sample)
- `site/hifi/data/notebooks/neso_data_portal/metered_wind_forecast_14d.json` and `-5.png` (run_notebooks.py)
- page `site/hifi/data-sources/neso_data_portal/14-days-ahead-operational-metered-wind-forecasts.html`

No staged chart spec, authored override or earlier artefact existed for this dataset.

Gates: `gridflow-build --only neso_data_portal/metered_wind_forecast_14d` wrote the page with no
error (the "37 lines in Known issues" warning is build-wide, not this note). Detector `[]`. Zero em
dashes in the page. Rubric grep (`locally`, `held`, `our `, `since 20`, digits + rows/days, `live`,
`now`, `real-time`, arrows, middle dots, planning words): only "14 days ahead", NESO's own horizon.

Screenshots (light) at 1440, 1024 and 768 (full page, cut into sections `c<w>-<n>.png`) and at 390
through a 390 px iframe in four offset slices (`d390-<offset>.png`), in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\mw14-writer\`.
Nothing clipped or overlapping: the long package slug in the Vendor fact wraps inside its cell,
both member keys and request URLs wrap in their wells, the three commands wrap at 390, the frame
folds behind `…` and the guide reads cleanly, the notebook cells wrap inside the panel. The
site has no dark theme. Server on 9802 started with its PID recorded; the bash PID (34049) was the
MSYS wrapper, so I confirmed the Windows listener (PID 17168) was my exact command
(`python -m http.server 9802 --directory C:/gridflow-wt/fe-neso-gen/site/hifi`) and stopped that
PID only; port 9802 free afterwards.

## What one row is

| Member | One row | Quantities (unit from NESO's dictionary) |
|---|---|---|
| `metered_wind_forecast_14d` (national) | one half-hour target (`datetime`, `date`, `settlement_period`) of one issue (`forecast_datetime` = `issue_time`); registry key `(datetime, issue_time)` | `wind_forecast` MW ("Wind forecast for each half hourly settlement period"), `capacity` MW ("total operational wind capacity that is connected to the National Grid Transmission Network") |
| `metered_wind_forecast_14d_windfarm` | one half-hour target and one wind farm (`generator_name`, `generator_full_name`, `region`); registry key `(datetime, generator_name)`; no issue column | `wind_forecast` MW, `capacity` MW ("operational wind capacity of the windfarm that is connected to the National Grid Transmission Network") |

Half-hourly, not hourly: 670 consecutive 30-minute targets per capture, settlement periods per
UK settlement day, NESO's dictionary describing settlement periods "at 30 minute intervals".

**What "operational metered" covers.** NESO's package text (catalogue snapshot `20261006T195819Z`):
national and windfarm-level 0-14 day ahead wind forecasts "for all the windfarms which provide
real-time operational metering (SCADA telemetry) to the NESO", based on evaluated Operational
Capacity, "a deterministic value based on recent actual production levels of that windfarm,
captured from SCADA telemetry". Both dictionaries describe capacity as connected to the
transmission network. So: the farms NESO meters through SCADA, with transmission-network
capacity. NESO does not say in this package that embedded farms are excluded in so many words; the
page says what NESO says (SCADA metering, transmission-network capacity) and links the embedded
wind forecast as the separate NESO forecast for embedded wind. The page avoids "real-time" (a
banned word) by writing "operational metering (SCADA)".

**Farms sum to national: yes, both captures.** Per target, the 272 farm `wind_forecast` values
sum to the national value within 0.4998 MW (8 Oct) and 0.4986 MW (16 Oct), mean 0.24 MW; the
rounded farm sum equals the national value at all 670 targets in each capture. Farm capacities sum
to 26,737.8 against 26,738 MW (8 Oct) and 26,859.8 against 26,860 MW (16 Oct). The page says it
"in NESO's files of 8 and 16 October 2026", and the notebook shows it on the reader's own capture
(`farms per half-hour: [272]`, `largest national minus farm sum, MW: 0.499`). NESO does not state
the relation (note `TODO: verify` kept).

## Times and the clock (scoped to these rows)

| Capture | Member | Rows | CKAN `last_modified` (read as UTC) | Issue (`ForecastDatetime`, stated UTC) | Target span, UTC |
|---|---|---:|---|---|---|
| 2026-10-08 11:12Z | national | 670 | 2026-10-08T10:16:12.426355 | 2026-10-08T09:52:34Z | 10-08 10:30 (SP 24) to 10-22 09:00 |
| 2026-10-16 20:40Z | national | 670 | 2026-10-16T20:16:19.155934 | 2026-10-16T19:52:23Z | 10-16 20:30 (SP 44) to 10-30 19:00 (SP 39) |
| 2026-10-08 11:12Z | windfarm | 182,240 | 2026-10-08T10:16:24.243581 | none (no column) | same as national |
| 2026-10-16 20:40Z | windfarm | 182,240 | 2026-10-16T20:16:31.024310 | none | same as national |

- `datetime` is the UTC **start** of the half-hour: dictionary unit "ISO 8601 (UTC)", registry
  `zone: UTC`, `temporal: utc_instant`, and on every row of both national captures it equals the
  UTC start of its `date`/`settlement_period` under the UK settlement-day convention (0
  mismatches), including the clock-change day. `timestamp_utc == datetime` on every row of both
  tables; `issue_time == forecast_datetime`; `available_at == published_at`.
- **Clock change observed.** The 16 Oct capture spans 25 October: that `date` has 50 periods
  (SP 1 to 50) from 2026-10-24T23:00Z; 26 October's SP 1 starts 2026-10-26T00:00Z. UTC stays an
  unbroken half-hour sequence. The frame shows exactly this seam (SP 45 to 50 of 25 Oct, then SP 1
  and 2 of 26 Oct). This resolves the note's autumn DST TODO; spring stays unobserved.
- **`published_at` read as UTC is supported here.** Each CKAN vintage is 24 minutes after the
  file's own `ForecastDatetime` (stated UTC, with `Z`) when read as UTC; read as BST it would fall
  before the forecast was produced. The windfarm file-name tokens (`_1115`, `_2115`) sit one hour
  after the UTC vintages, matching BST clock time. Every target is after its vintage in both
  captures (forward-target rule holds on 16 Oct too).
- The notebook converts session-zone times (`tail()` returns Europe/London) with
  `tz_convert("UTC")`; outputs show `+00:00`.

## Captures, row counts, repeats

| Member | Capture | Bronze rows | Silver rows | Against the other capture |
|---|---|---:|---:|---|
| national | 2026-10-08 | 670 | 670 | |
| national | 2026-10-16 | 670 | 670 | 266 targets shared (10-16 20:30Z to 10-22 09:00Z) under a different issue; none equal (largest difference 5,169 MW) |
| windfarm | 2026-10-08 | 182,240 | 182,240 | |
| windfarm | 2026-10-16 | 182,240 | 182,240 | same 272 farms and 19 regions; 72,352 `(datetime, generator_name)` keys repeat (266 x 272); two capacities changed |

Headers identical across captures; CRLF, no BOM (bytes counted on the 16 Oct files). Within each
capture neither key repeats. The base silver table holds both captures (1,340 and 364,480 rows);
`_latest` (`whole_capture`) holds the newest. **Chart and frame filter on
`issue_time == 2026-10-16T19:52:23Z`** and set `dedup: {on: [datetime], order_by: published_at}`
as a guard (`duplicates_dropped: 0`; distil read 1,340, matched 670).

## Chart

Line, `wind_forecast` against `timestamp_utc`, filter `issue_time == 2026-10-16T19:52:23Z`,
window 2026-10-16 to 2026-10-30, one point per half-hour (670), MW, `y_min: 0`. One whole issue:
from 11,553 at 20:30 UTC on the 16th, down to the lowest, 7,887 at 10:00 UTC on 18 Oct, up to
16,055 to 17,573 on 23 Oct, the peak 18,240 at 02:00 UTC on 26 Oct, ending at 12,818 at 19:00 UTC
on 30 Oct. The key note gives capacity, 26,860 MW, which the frame shows. Capacity is not drawn
(a flat line adds nothing; the zero-based axis already shows scale).

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Metered wind forecast, MW, 0 to 14 days, national and per farm (`summary`, `what_it_is`) | package notes and both resource descriptions, catalogue snapshot `20261006T195819Z`; dictionaries `field-info/20261008T114228Z/metered_wind_forecast_14d{,_windfarm}.json` (units MW) |
| SCADA-metered farms, transmission-network capacity (`what_it_is`, `capacity` field) | package notes (quoted above); `Capacity` descriptions in both dictionaries |
| Farms sum to national, nearest MW, 8 and 16 Oct (`what_it_is`) | Polars on both capture pairs (above); notebook cell 2 output |
| Daily, no stated time (`facts.cadence`) | snapshot extras "Update frequency: Daily"; no time given anywhere in the package text |
| Grain (`facts.grain`), Key `datetime, issue_time` | registry `14-days-ahead-operational-metered-wind-forecasts.json` `entity_key` for each family |
| `datetime` UTC period start (field, x label) | dictionary unit; registry zone/temporal; 0 mismatches against UK settlement start on both captures |
| `settlement_period` "period 1 ends 00:30 UK time" | dictionary comment, both resources |
| `forecast_datetime` "when NESO says it produced the forecast, UTC; the same in every row here" | dictionary "Date and time of when the forecast is produced", unit ISO 8601 (UTC); one value per capture; the 8 rows show one value |
| `issue_time` equals `forecast_datetime` | registry `issue: {kind: data_column, column: forecast_datetime}`; equal on every row |
| `published_at` CKAN last-modified read as UTC, "here 24 minutes after issue" | registry `vintage: ckan_last_modified`; ADR-030; frame shows 19:52:23 and 20:16:19 |
| `capacity` "the same in every row here" not claimed; key note 26,860 MW | frame shows 26860.0 on all 8 rows |
| Requests (member `request`) | 16 Oct bronze sidecars `request_url` |
| Raw note (one `package_show`, whole files, skipped when unchanged; dates select nothing; windfarm name changes) | `client.py:1583-1622` (window not a selector, D-16), `:1752-1765` (upload skipped when `last_modified` unchanged); file names `_20261006_2015`, `_20261008_1115`, `_20261016_2115` |
| Commands | `cli.py` ingest/transform/pipeline; `client.py:1533-1549` (window end must be recent, within 48 h, not future); same form as the approved day-ahead and Demand pages |
| `tail()` reads `_latest`, lineage dropped, session zone (`notebook.lead`) | gridflow_models `research/handles/source.py:453-487`; probed `_relation_name_for_dataset` -> `silver_neso_data_portal_metered_wind_forecast_14d{,_windfarm}_latest`, date column `timestamp_utc` |
| Related | page set: `day-ahead-wind-forecast`, `monthly-operational-metered-wind-output` (slugs), `embedded_wind_solar_forecast` (table key of the live page), `elexon/windfor`; notes from those pages' summaries (WINDFOR "issued up to eight times a day") |

## Body corrections (canonical note)

- Intro: "The current capture runs ..." now covers both captures (670 half-hours each); "The
  captured national file holds a single forecast issue ... keeps only the forecast present at
  capture time" now says each capture, and that issues between captures are missed.
- Files: 16 Oct recaptures added for both resources (file names, bytes, rows, header, line
  endings); the national file name is stable across all three dates.
- National clocks: "For the one capture to date ... All 670 silver rows share this one vintage"
  replaced with both vintages and the UTC-reading consistency check; event-time check extended to
  both captures.
- Issue time: "The capture holds one issue" now each capture, with the 16 Oct issue.
- Eligibility: 16 Oct forward-target check added.
- Horizon: both captures' spans; "No clock-change day fell inside this capture ... DST-day
  behaviour is unobserved" replaced by a "Clock change (observed once, autumn 2026)" paragraph;
  the TODO narrowed to the spring change.
- Units: capacity and range per capture.
- Identity: per capture; new paragraph "Captures repeat targets" (266 shared targets, no equal
  values, how the page picks one issue).
- Relation to windfarm file: 16 Oct numbers added.
- Activation: second capture noted (base 1,340, `_latest` 670 on 2026-10-24).
- Windfarm: both vintages; file-name tokens; 16 Oct forward-target; layout per capture plus the
  two capacity changes (SOFWO-11 112 to 176 MW, DBBWO-3 160 to 218 MW, together the national
  +122 MW); zero counts for 16 Oct; identity per capture plus "Captures repeat keys" (72,352
  repeated keys, no issue column, `_latest` holds newest only); activation notes the recapture.
- Cadence: 16 Oct stamps and token added; "Captures to date: one per family (2026-10-08). No
  scheduled refresh has run yet." replaced with two per family. Holds: "DST-day labelling" ->
  "spring clock-change labelling".

Not changed: the 41 unmatched generator names (FACTS claim, not re-derived), region table (16 Oct
counts identical to it), front matter `updated:` (precedent left it).

## Unverified

- Whether NESO publishes this package more than once a day (issues at 09:52 and 19:52 UTC on
  different days; the 6 Oct snapshot shows 19:16 UTC). The page says only "Daily, NESO says, at no
  stated time of day".
- Spring clock-change labelling (46 periods): no capture spans one.
- Whether the 41 farm names with no Elexon match are embedded or otherwise different sites.

## Open questions

- Related is capped at 4. I kept day-ahead (same fleet, next day), monthly metered output (the
  outturn to score against), embedded wind and solar (the wind this forecast does not cover) and
  Elexon WINDFOR (the benchmark). `daily_wind_availability` is left out; the seat may swap it in
  for WINDFOR.
- The notebook uses `tail()` with no dates so a reader's own capture reproduces it; the windfarm
  call passes `n = 200_000` to take a whole capture (182,240 rows here). The third output line
  ("most periods in one settlement day: 50") holds only while a capture spans the autumn change; on
  a reader's later capture it will read 48.

## Template problems

- None new. As on the pattern page: three commands is the cap, so the windfarm table gets one
  `pipeline` line; at 390 the hero scenery shows only the substation, interconnector and offshore
  turbines (template crop, not clipping).

## Defects

- No gridflow code defect found. Observation, by design: the windfarm table's base silver relation
  repeats its registry key `(datetime, generator_name)` across captures (72,352 keys over the 8 and
  16 Oct captures) with no issue column; only `published_at` / `bronze_capture_id` separate the
  forecasts. `_latest`, `query()` and `tail()` are unaffected. Worth a line in the gridflow_models
  help for anyone reading the base relation.
- **NESO, dictionaries (vendor):** both resources give `Datetime` and `ForecastDatetime` examples
  without a zone (`2021-02-22T00:00:00`, `2021-02-22T17:12:09`) while the unit says UTC and the
  data carry `Z`. For the NESO question packet if not there.
- **NESO, publication schedule (vendor):** "Update frequency: Daily", but issues are seen at 09:52
  UTC (8 Oct) and 19:52 UTC (16 Oct) and CKAN stamps at 10:16, 19:16 and 20:16 UTC; NESO states no
  time or count per day. Captures may miss issues. Question for NESO.

## Round 2 (review nits, 2026-10-24)

All five nits applied in the canonical note (CRLF kept, 506 of 506 lines), mirrored, `cmp` clean.

1. `related[embedded_wind_solar_forecast].note`: now "NESO's embedded wind forecast, outside this
   transmission-connected one" (the sibling's wording; the limit is put on the capacity, NESO's words).
2. `chart_view.alt`: "climbs to a high of 17,573 on 23 October" (UTC 23 October runs 16,429 to
   17,573; 16,055 is the 23:00Z half-hour on 22 October and is dropped).
3. `record.fields.issue_time`: "Equals `forecast_datetime`; half-hours also forecast in the 8 October
   issue have two rows" (14 words). The count 266 is left out: it is a count over our captures,
   not visible on the page; the note body keeps it.
4. Notebook cell 2: the line now prints "most periods in one settlement day of this capture: 50".
   Notebook rerun with `run_notebooks.py` (5 cells, no errors, outputs otherwise unchanged).
5. `chart_view.caption`: "produced, NESO says, at 19:52 UTC on 16 October 2026" (39 words). Not
   "read as UTC": NESO's dictionary gives `ForecastDatetime` in UTC and the value carries `Z`; "read
   as UTC" is the wording for CKAN's offset-less `last_modified` (`published_at`).

Gates: `gridflow-build --only neso_data_portal/metered_wind_forecast_14d` wrote the page, no error;
detector `[]`; 0 em dashes. Chart spec and sample selection unchanged, so the series and sample did
not need regenerating (the build's digest check passed). No new screenshots: the changes are short
text in fields already checked at all four widths (the longer `issue_time` line wraps in the guide).
