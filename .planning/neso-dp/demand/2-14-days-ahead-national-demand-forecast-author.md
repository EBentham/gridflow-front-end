# 2-14-days-ahead-national-demand-forecast: writer's report

Family page `2-14-days-ahead-national-demand-forecast`, lead `national_demand_fc_2_14d_days_ahead` (eligible), members
`national_demand_fc_2_14d_days_ahead_half` (held) and `national_demand_fc_2_14d_historic_day` (held). Written 2026-10-24.

Files:
- canonical note `C:\gridflow-wt\vault-neso-dem\30-vendors\neso-data-portal\datasets\2-14-days-ahead-national-demand-forecast.md`
  (CRLF kept, 598 of 598 lines CRLF after the final edit); mirror
  `C:\gridflow-wt\fe-neso-dem\vault\neso_data_portal\2-14-days-ahead-national-demand-forecast.md`, `cmp` clean
- `site/hifi/data/series/neso_data_portal/national_demand_fc_2_14d_days_ahead.json` (gridflow-distil, spec_origin vault)
- `site/hifi/data/samples/neso_data_portal/national_demand_fc_2_14d_days_ahead.json` (gridflow-sample)
- `site/hifi/data/notebooks/neso_data_portal/national_demand_fc_2_14d_days_ahead.json` and `-4.png` (run_notebooks.py)
- page `site/hifi/data-sources/neso_data_portal/2-14-days-ahead-national-demand-forecast.html`

Gates: `gridflow-build --only neso_data_portal/national_demand_fc_2_14d_days_ahead` wrote the page with no error (first
run caught three fields one word over budget; trimmed). Detector `[]`. Zero em dashes in the page and in the `page:`
block (the note body's 21 are pre-existing table cells). No staged chart spec or authored override existed.

Screenshots (light) at 1440, 1024, 768 and 390 (390 through a 390 px iframe page placed in `site/hifi` for the shot and
deleted straight after), in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\dem214-writer\`
(`shot-<w>.png`, cropped `c<w>-<n>.png`). Nothing clipped or overlapping; at 390 the chart's x ticks thin to alternate
dates and the key stacks below. Server on 9844 started with its PID recorded (26916) and stopped by that PID only.

## The 151-row capture (seat's question)

Not a missing day or point. The 2026-10-16 file covers all 13 target dates (18 to 30 October, leads 2 to 14), but
NESO switches to a different cardinal-point set at the autumn clock change:

| Target dates | Points | What changes |
|---|---|---|
| 18 to 24 Oct | 12 | the usual set: `3C` P 1700-1800, `4B` P 1830-2000 (`EM`) |
| 25 Oct (clock change) | 12 | `3C` gone; new `DP` P 1700-1800 carries `EM`; `4B` becomes **F** 2100-2100, blank `f_point`; `1A` widens to 100-230 |
| 26 to 30 Oct | 11 | as 25 Oct, and `1S` gone too |

7 x 12 + 12 + 5 x 11 = 151. Bronze has 151 data lines (6,133 bytes = declared length), silver 151. No key repeats
(`daysahead, targetdate, cardinalpoint` unique). Consequence for readers: a code is not a stable point identity (`4B`
is a peak window, then a fixed time). The chart avoids codes: it uses `f_point` (`EM`, `Om`), which NESO assigns to
whichever point holds that extreme.

## What one row is

| Member | One row | Quantity | Source |
|---|---|---|---|
| current (`_days_ahead`) | one cardinal point of one target date in one publication: `daysahead` (2-14), `targetdate`, `cardinalpoint`, `cp_type`, window `cp_st_time`/`cp_end_time`, `f_point` | `forecastdemand`, MW | dictionary `FORECASTDEMAND` unit MW; resource text defines ND |
| half-hourly (`_days_ahead_half`) | one half-hour of one target date: `date`, `ctime` (UK clock), `gdatetime` (UTC per NESO) | `nationaldemand`, MW | dictionary unit MW |
| archive (`_historic_day`) | as the current file plus `forecast_timestamp`; one row per issue | `forecastdemand`, MW | dictionary unit MW |

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| ND definition (`what_it_is`) | resource description, catalogue snapshot `20261006T195819Z`, resources `9af18ed4`/`7c0411cd`: "National Demand is the Great Britain generation requirement ... excludes generation required to meet station load, pump storage pumping and interconnector exports." |
| "Twice daily, at 09:20 and 14:20 by NESO's notes, which give no zone" (`facts.cadence`) | package notes, same snapshot: "These files are updated twice daily, at 09:20 and 14:20." No zone given. |
| "NESO's archive file holds 2 to 14 day forecasts from 2020" (`facts.history`); "NESO describes the archive as all 2 to 14 day forecasts from 2020" (`what_it_is`) | resource `4dd712a2` description: "All historic 2-14 day ahead demand forecasts from 2020 to the most recent forecast." Both captures' earliest target is 2020-09-24 (consistent). Attributed to NESO per the 1-day ruling. |
| "recently it keeps one of each day's two updates" (`what_it_is`) | 2026-10-16 archive capture: every publication day 2026-09-19 to 2026-10-16 (28 days) has exactly one `forecast_timestamp`, about 09:45Z; 2026-09-18 has two. On 16 Oct the current file (vintage 15:19:59) matches the archive's only issue that day (`2026-10-16T09:45:03Z`) on all 151 lead/target/point keys but only 44 values, so the later update is not in the archive. On 8 Oct the current file (08:45:03) equals the archive's 09:45:02Z issue on all 156 values. "Two updates" is NESO's "twice daily". |
| "the set changed at the October clock change" (`what_it_is`); "a code can change meaning, as `4B` does here" (`cardinalpoint`) | silver 2026-10-16 capture, table above; the frame shows `4B` P 1830-2000 on 24 Oct and F 2100 on 26 Oct. |
| MW (`chart.unit`, `forecastdemand`) | field-info `20261008T114228Z/national_demand_fc_2_14d_days_ahead.json`: `FORECASTDEMAND` `unit: MW`. This package's own dictionary gives it (unlike the 1-day current file). |
| `EM` / `Om` definitions (chart key notes; `f_point` field) | this package's dictionary lists the four labels without pairing codes. NESO's 1-day, 2-day and 7-day dictionaries (same field-info folder, `F_Point` `comment`) pair them: "Overnight minimum (OM): minimum national demand between half hour ending 00:30 and 07:30 ... Evening peak (EM): maximum national demand between half hour ending 17:00 and 24:00". Key notes say "as NESO's day-ahead dictionaries define it". In both captures, every target date has exactly one `EM` and one `Om` row, and `EM` is that day's maximum and `Om` its minimum (Polars check). |
| `cp_type` F/T/P | dictionary: Fixed, Trough, Peak. |
| `cp_st_time` "NESO says UTC, the data suggest UK time" | dictionary: "Time UTC"; note body FACTS T03/C6 join table (Europe/London no shift: 52 of 52 equal; UTC: 0). Rechecked on 25 Oct: `1F` 30 = 21,746 = half-hourly `CTIME` 30 (`GDATETIME` 23:30Z the evening before); `DP` window ends 1800 = 33,234 = half-hour 18:00Z. |
| `targetdate` sent as `YYYYMMDD` | registry current epoch `format: %Y%m%d`; bronze `2,20261018,24559,...`. |
| `daysahead` "NESO's D+n: the target is n days after publication" | dictionary: "The date the demand forecast is for i.e. D+4 for 4 Day Ahead"; both captures: lead n targets capture date + n. |
| `timestamp_utc` = start of target date's first settlement period | registry `temporal: date_sp1` on `targetdate`; all 156 and all 151 rows equal `targetdate` 00:00 Europe/London in UTC (23:00Z to 25 Oct, 00:00Z from 26 Oct). |
| `published_at` read as UTC, no issue time | registry `vintage: ckan_last_modified`, `issue: none`; ADR-030; silver `published_at` = sidecar `ckan_last_modified` (08:45:03.632388, 15:19:59.536755). |
| Chart: line on `targetdate`, filter `published_at >= 2026-10-16`, `f_point in [EM, Om]`, dedup `[targetdate, f_point]` by `published_at`, window 18-30 Oct | distil provenance: 2 files, 307 rows read, 26 matched, 26 used, `duplicates_dropped: 0`. `distil.py` accepts a `pl.Date` time column, so points sit on the target date (no 23:00Z shift). Dedup is a guard: the published_at filter already selects one file. |
| Alt numbers | committed series: evening 33,421 / 35,929 / 35,304 / 34,950 / 33,884 / 32,177 / 31,454 / 33,234 / 36,096 / 37,689 / 37,809 / 37,600 / 36,330; overnight 20,147 / 21,190 / 21,664 / 21,132 / 20,276 / 19,293 / 19,269 / 18,468 / 17,303 / 20,316 / 20,403 / 20,490 / 20,467. 24 Oct 2026 is a Saturday (17 Oct is, per the 1-day review). "Holds near 20,400" covers 20,316 to 20,490. |
| Caption "From 25 October the evening peak window is 17:00-18:00, not 18:30-20:00" | `EM` row: `4B` 1830-2000 on 18-24 Oct, `DP` 1700-1800 on 25-30 Oct (windows as NESO writes them). |
| Sample rows (`record.caption`) | 8 rows: 24 Oct `1B 2A 3C 4B`, 26 Oct `1B 2A DP 4B`, all from the 16 Oct file (`published_at` filter; dedup guard). |
| Notebook lead | probe with the gridflow_models interpreter: `_validate_dataset_for_source` returns `targetdate`; relation `silver_neso_data_portal_national_demand_fc_2_14d_days_ahead_latest`; `tail(..., n=200)` returns 151 rows; `event_time`, `available_at`, `source_run_id`, `dataset_version` absent; times `datetime64[us, Europe/London]`. `tail()` is `ORDER BY targetdate DESC LIMIT ?` (`research/handles/source.py:453-488`). Notebook output shows `published_at` `2026-10-16 15:19:59.536755+00:00` (converted). |
| Requests | connector `client.py`: upload members fetched whole after one `package_show`, skipped when `ckan_last_modified` equals live `last_modified` (lines ~1751-1767). URLs are the 2026-10-16 bronze sidecars' `request_url`. |
| Commands | same `--last 24h` form as the approved 1-day page; `cli.py` ingest/transform take `--last` (lines 191, 266). |
| Related | `neso_data_portal.json` page set lists `2-day-ahead-demand-forecast` and `7-day-ahead-national-forecast` (7-day holds one target date: its note says so); `elexon.json` family `demand-forecasts` has `ndfd` (one figure per date, `vault/elexon/ndfd.md`: "one figure per day; the fields do not say which daily statistic") and `demand-outturn` has `indo`. |

## Times and clock for the eligible file (scoped to its rows)

- 2026-10-08 capture: vintage 08:45:03.632388 (read as UTC), file `ng_demand_14da_20261022.csv`, targets 10 to 22 Oct.
- 2026-10-16 capture: vintage 15:19:59.536755, file `ng_demand_14da_20261030.csv`, targets 18 to 30 Oct.
- Every target lies after its vintage (forward-target rule holds in both).
- Neither stamp matches NESO's "09:20 and 14:20" in UTC (08:45, 15:19) or BST (09:45, 16:19). The page quotes NESO's
  times as NESO's, and says "read as UTC" for the stamp; no slot inference.
- Point windows are raw text; the zone dispute (dictionary UTC, data UK) is unchanged and stated on the guide line.

## Captures, row counts, repeats

| Table | Capture | Bronze data rows | Silver rows | Notes |
|---|---|---|---|---|
| current | 2026-10-08 | 156 | 156 | 13 dates x 12 |
| current | 2026-10-16 | 151 | 151 | point set changes at the clock change (above) |
| half-hourly | 2026-10-08 | 624 | 624 | 13 x 48 |
| half-hourly | 2026-10-16 | 625 | 625 | 12 x 48 + **49** on 25 Oct (should be 50) |
| archive | 2026-10-08 | 370,700 | 370,700 | |
| archive | 2026-10-16 | 371,933 | 371,933 | all 370,700 earlier rows unchanged; 1,233 added = 8 issues (9 to 16 Oct), one per day |

No row repeats within any capture. Across captures: current and half-hourly share target dates 18 to 22 Oct (60 and 240
rows) but every value was revised, so no identical rows; the archive repeats its whole history per capture (held, not
charted). The chart and frame filter to the 16 Oct file and carry `dedup` as a guard (drops 0).

## Held members: hold lines

- Half-hourly: "NESO does not say whether each UTC time starts or ends its half-hour." (12 words.) From the registry
  question (whether `GDATETIME` (UTC) labels the half-hour end). NESO's dictionary does give the clock ("GMT/UTC
  regardless of forecast date's GB timezone"), so the open part is start or end only. The 49-row clock-change day is in
  the note body and Defects, not in the line.
- Archive: "Forecast time stamps end in Z, but NESO does not confirm UTC; the field is undocumented." (15 words.) Word
  for word the 7-day line: this registry question is the same as the 7-day one (zone undocumented; no vendor
  definition), with no email-recovery comment (that is 1-day only). The "sits after CKAN last_modified" part of the
  question holds on the 8 Oct capture only (body corrected).

## Body corrections (canonical note)

- Intro: "Historic archive. Every past 2–14 day forecast. The vendor says..." replaced with NESO's quoted description
  plus the one-issue-a-day observation scoped to the 16 Oct capture.
- Files: 16 Oct recaptures of all three CSVs (names, sizes, rows); the 151 explained; datastore-total sentence scoped to
  8 Oct; repeats sentence added.
- Current clocks: "For the one capture to date" replaced with both vintages; event-time check extended to 151 rows and
  the clock change; forward-target evidence extended.
- Shape: 156-row statement scoped to 8 Oct; new paragraph on the 16 Oct point set (25 Oct layout, 11-point days, `4B`
  meaning change, `Om` on `L04` on 30 Oct, dictionary example `DP`).
- `F_Point` TODO: the code pairing is now cited from NESO's 1-day/2-day/7-day dictionaries; `EM`/`Om` = day max/min in
  both captures.
- `FORECASTDEMAND` range scoped per capture; blank `f_point` counts per capture (104/156, 99/151); "no zeros" for both.
- Activation (current): second capture, base 307 rows, `_latest` 151.
- Half-hourly: both vintages; "no DST transition day ... unobserved" replaced: the 16 Oct capture spans the autumn
  change and lists 49 half-hours on 25 Oct (`CTIME` 130 twice, no 01:00Z row); spring still unobserved; activation
  line adds 625 and no cross-capture repeats; "what would lift the hold" updated.
- Archive: both vintages; the "after CKAN last_modified" evidence scoped to 8 Oct (16 Oct does not test it); group
  counts per capture; `NA` absent in 16 Oct; new recapture paragraph (append of one issue per day).
- Cadence: archive-keeps-both TODO kept, with the observation; 16 Oct CKAN stamps added; "No scheduled gridflow refresh
  exists yet" replaced with "Captures to date: two per family".

## Unverified

- What NESO's 09:20 and 14:20 refer to; neither capture's stamp matches either reading.
- Whether the archive ever keeps the second daily update (28 recent days have one issue each; older days sometimes two).
- Spring clock-change behaviour of both files; whether the 49-row autumn day is a one-off.
- Whether the winter point set holds all winter (only five 11-point days seen).

## Open questions

- Related is capped at 4. I chose the 2-day and 7-day pages (their horizons fall inside 2 to 14) plus Elexon `ndfd`
  and `indo`; the 1-day page already links here. The seat may prefer the 1-day page over one of these.
- Title "Two-week national demand forecast" (the 6-word budget rules out "2 to 14 days ahead national demand
  forecast"); the hub title keeps NESO's "2-14 days ahead". Seat's call if the sibling titles should match a pattern.
- The chart axis starts at 0 MW; both lines are readable. A `y_min` floor could stretch the variation; I left the zero
  floor as the honest default.

## Template problems

- None blocking. The x axis label is set by `chart_view.x_label`; a date-typed time column renders day ticks correctly
  ("18 Oct" ... "30 Oct", alternate dates at 390).
- The 390 check needs an iframe page served from the site root; I placed it in `site/hifi` for one shot and deleted it.
  A shared harness page in the scratchpad served by its own server would avoid touching the worktree.

## Defects

- **NESO 2-14 day half-hourly forecast, clock-change day missing a half-hour (vendor data):** the 2026-10-16 capture of
  `ng-demand-14da-hh.csv` lists 49 rows for 2026-10-25 (a 25-hour day of 50 half-hours): `CTIME` reads 30, 100, 130, 130,
  200 with `GDATETIME` 23:30, 00:00, 00:30, 01:30, 02:00 UTC; no row at 01:00 UTC. One half-hour of forecast demand is
  absent. gridflow keeps the file as sent (bronze 49 = silver 49); the family is held. Add to the NESO question packet
  with the start-or-end question.
- **NESO 2-14 day archive keeps one of two daily updates (vendor/data):** every publication day 2026-09-19 to
  2026-10-16 has one issue (about 09:45Z) in the archive, although NESO says the files update twice daily; the
  2026-10-16 current file (stamp 15:19:59, read as UTC) differs from that day's archived issue on 107 of 151 values. A
  backtest from the archive sees the morning issue only. Same pattern as the 1-day archive (20bg). No gridflow change.
- **NESO 2-14 day cardinal points change identity at the clock change (vendor/data, documentation):** from target
  2026-10-25 the point set changes (`3C` and later `1S` dropped, `DP` added, `4B` turns from a 1830-2000 peak into a
  fixed 2100 point). Any gridflow consumer keying history on `cardinalpoint` alone (for example a future `key_latest`)
  would join unlike points across the change; key on the window or `f_point` too. No gridflow code does this today.
- No gridflow code defect found.
