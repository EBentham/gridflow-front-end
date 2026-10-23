# 2-day-ahead-demand-forecast: writer's report

Family page `2-day-ahead-demand-forecast`, lead `demand_forecast_2d_day_ahead` (eligible), member
`demand_forecast_2d_historic_day_ahead` (held). Written 2026-10-24. Pattern: the approved `1-day-ahead-demand-forecast`
page; every fact below was re-derived from the 2-day files, not copied.

Files:
- canonical note `C:\gridflow-wt\vault-neso-dem\30-vendors\neso-data-portal\datasets\2-day-ahead-demand-forecast.md`
  (CRLF kept, 505 CRLF of 505 lines); mirror `C:\gridflow-wt\fe-neso-dem\vault\neso_data_portal\2-day-ahead-demand-forecast.md`, `cmp` clean
- `site/hifi/data/series/neso_data_portal/demand_forecast_2d_day_ahead.json` (gridflow-distil, `spec_origin: vault`)
- `site/hifi/data/samples/neso_data_portal/demand_forecast_2d_day_ahead.json` (gridflow-sample)
- `site/hifi/data/notebooks/neso_data_portal/demand_forecast_2d_day_ahead.json` and `-4.png` (run_notebooks.py)
- page `site/hifi/data-sources/neso_data_portal/2-day-ahead-demand-forecast.html`

Gates: `gridflow-build --only neso_data_portal/demand_forecast_2d_day_ahead` wrote the page with no error. Detector `[]`.
Zero em dashes in the page and the `page:` block. Word counts by the build's `words()`: `what_it_is` 60 (budget 60),
caption 40 (40), alt 63, `plot_alt` 49, lead 35 (35), held line 12. No staged chart spec or authored override existed.

Screenshots (light) at 1440, 1024, 768 and 390 (390 through a 390 px iframe), in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\dem2d-writer\`
(`shot-<w>.png`, cropped `c<w>-<n>.png`). Nothing clipped or overlapping; at 390 the longest bar labels
("01:00-01:30 trough", "04:30-07:30 trough") start about 14 px from the edge, as on the 1-day page. No dark theme exists
on the site. Server started on 9842 with its PID recorded (23882) and stopped by that PID only.

## What one row is

| Member | One row | Quantity | Demand definition |
|---|---|---|---|
| current (`demand_forecast_2d_day_ahead`) | one cardinal point of one target date (D+2): `targetdate` + `cardinalpoint`, with type (`F`/`T`/`P`) and window (`cp_st_time`, `cp_end_time`); `daysahead` = 2 | `forecastdemand`, MW | national demand (ND) |
| historic (`demand_forecast_2d_historic_day_ahead`) | the same, plus `forecast_timestamp`; in both captures exactly one issue per target date | same | same |

Unit authenticity: the 2-day current dictionary (`field-info/20261008T114228Z/demand_forecast_2d_day_ahead.json`,
resource `cda26f27`) is the original. Its texts name its own lead ("2" for 2 Day Ahead, D+2, title "Two Day Ahead
Demand Forecast") and give `FORECASTDEMAND` `unit: MW`, example `2` under `DAYSAHEAD`. The 1-day current dictionary
(`aec5601a`) repeats the same descriptions with the unit fields shifted (`DAYSAHEAD` unit "2", `FORECASTDEMAND` unit
blank). So MW here needs no transfer from the archive; the page's field line says MW without a source caveat. The
2-day archive dictionary also says MW. Note: the original carries the oddity too (`CP_END_TIME` unit "1930").

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| ND definition (`what_it_is`) | resource `cda26f27` description, catalogue snapshot `20261006T195819Z`: "National Demand is the Great Britain generation requirement ... excludes generation required to meet station load, pump storage pumping and interconnector exports." |
| Daily, 16:15 to 17:00 clock time (`facts.cadence`) | same description: "Publication frequency: daily. Publication time: between 16:15 and 17:00 (clock time)." All three CKAN stamps seen (snapshot 2026-10-06T15:15:02, captures 2026-10-07T15:15:00 and 2026-10-16T15:15:01) fall at 16:15 BST when read as UTC. |
| Archive "from 2018" attributed; file starts April 2023 (`facts.history`, `what_it_is`) | resource `24abd271` description: "All historic 2 day ahead demand forecasts from 2018 to the most recent forecast." Both archive captures start at target 2023-04-03 (bronze first data row `2,"2023-04-03",22135,"1F",...`; silver min). |
| One issue per target date (`what_it_is`, scoped to the October 2026 file) | silver, 2026-10-16 capture: `forecast_timestamp.n_unique()` by `targetdate` = 1 on all 1,294 dates; same on 1,285 dates in the 2026-10-08 capture. Unlike the 1-day package, NESO publishes this file once daily, so no twice-daily caveat applies. |
| MW (`chart.unit`, `forecastdemand`) | current dictionary `FORECASTDEMAND` `unit: MW` (see above). |
| Peak/trough/fixed (`cp_type`, key note) | both dictionaries: Fixed (a fixed time), Trough (minimum during a set period), Peak (maximum during a set period). |
| `f_point` codes | dictionary comment: OM overnight minimum, DM daytime peak, Dm daytime minimum, EM evening peak; file carries `Om`. Empty strings on 8 of 12 rows in each current capture (silver). |
| CP clock zone dispute (caption, `cp_st_time`) | current dictionary: "Time UTC"; archive dictionary: "relative to the timezone in effect in the UK at the forecast time and date". |
| `targetdate` sent as `YYYYMMDD` | registry `2-day-ahead-demand-forecast.json` current epoch `format: %Y%m%d`; bronze `2,20261018,...`. |
| `timestamp_utc` = start of the target date's first settlement period | registry `temporal: date_sp1` on `targetdate`; silver 2026-10-08 23:00 UTC for 9 Oct, 2026-10-17 23:00 UTC for 18 Oct. |
| `published_at` = NESO last-modified, read as UTC; no issue time | registry `vintage: ckan_last_modified`, `issue: none`; silver `published_at` equals each sidecar's `ckan_last_modified` (2026-10-07T15:15:00.349284, 2026-10-16T15:15:01.350931). |
| `tail()` reads `_latest`, date column `targetdate`, lineage dropped, session zone (`notebook.lead`) | probe with the gridflow_models interpreter: `_validate_dataset_for_source` -> `targetdate`; relation `silver_neso_data_portal_demand_forecast_2d_day_ahead_latest`; 12 rows, 12 columns (`event_time`, `available_at`, `source_run_id`, `dataset_version` absent); times `datetime64[us, Europe/London]` (`published_at` printed `2026-10-16 16:15:01.350931+01:00`). `tail()` SQL is `ORDER BY targetdate DESC LIMIT ?` (`research/handles/source.py:483`). |
| Requests (member `request`) | connector `client.py:1663-1769`: one `package_show`, newest capture with the live `last_modified` is `unchanged`, others downloaded. URLs are the 2026-10-16 sidecars' `request_url`. |
| Commands | same `--last 24h` form as the approved 1-day page; `cli.py:200-230` `--last` precedence. |
| Related | page set `neso_data_portal.json` has `1-day-ahead-demand-forecast` and `2-14-days-ahead-national-demand-forecast`; `elexon.json` family `demand-forecasts` has `ndfd` (the vault NDFD note: daily forecast for each date 2 to 14 days ahead) and `demand-outturn` has `indo`. |

## Times and the clock for the current file (scoped to its rows)

- Two captures, 12 rows each, different targets, no row repeated (`(targetdate, cardinalpoint)` unique over 24 rows):
  - 2026-10-08 10:06 UTC: `ng_demand_2da_20261009.csv`, target 2026-10-09, CKAN 2026-10-07T15:15:00.349284;
  - 2026-10-16 20:02 UTC: `ng_demand_2da_20261018.csv`, target 2026-10-18, CKAN 2026-10-16T15:15:01.350931.
- Each target is two days after its vintage date (forward-target rule holds).
- Rows carry no time beyond the date anchor; window clocks stay raw strings, zone disputed by NESO's two dictionaries.
- The current file equals the archive on both target dates: 9 Oct (issue `2026-10-07T16:08:54Z`) and 18 Oct (issue
  `2026-10-16T15:54:18Z`), all 12 values, windows and `F_Point` labels identical.

## Held historic file

`held: "Forecast time stamps end in Z, but NESO does not confirm UTC."` (12 words)

The registry question (`registry/2-day-ahead-demand-forecast.json`, eligibility of the archive family) is the 1-day
question without the email-recovery clause: `FORECAST_TIMESTAMP` zone undocumented (Z suffix, but after the file's
CKAN `last_modified` when read as UTC), and whether it is the immutable issue instant. So the shared first clause,
word for word, ending with a full stop. Ledger row: `2-day-ahead-demand-forecast | DEM-1 | ... 12 · ... 14,608 |
current | historic (E-SEM)`. Both captures show the question: newest label `2026-10-07T16:08:54Z` against file stamp
15:15:12, then `2026-10-16T15:54:18Z` against 15:15:09 (read as UTC, 39 to 54 minutes after the file changed).

## Captures, row counts, repeats

| Table | Capture | Bytes (declared = actual) | Bronze data rows | Silver rows | Notes |
|---|---|---|---|---|---|
| current | 2026-10-08 | 578 | 12 | 12 | target 2026-10-09 |
| current | 2026-10-16 | 578 | 12 | 12 | target 2026-10-18 |
| historic | 2026-10-08 | 970,225 | 14,608 | 14,608 | targets 2023-04-03 to 2026-10-09, 1,285 dates |
| historic | 2026-10-16 | 977,389 | 14,716 | 14,716 | all 14,608 earlier rows unchanged; 108 added (targets 10 to 18 Oct, 12 rows, one issue each) |

The chart and frame read both current captures (24 rows); the `targetdate` filter picks 12, and
`dedup: {"on": [targetdate, cardinalpoint], order_by: published_at}` is set on both as a guard
(`duplicates_dropped: 0` in the series provenance).

## Chart

Bar chart, 12 bars, one per cardinal point of target Sunday 18 October 2026 (the newest), MW, from zero, in time order
through `group_map` labels with `sort: label`. Window: that one target date, from the file stamped 2026-10-16 15:15
(read as UTC). Values 20,147 (`1B`, 04:30-07:30 trough) to 33,421 (`4B`, 18:30-20:00 peak). The labels match the
18 October windows in the file (`3C` 1700-1800, `4B` 1830-2000; these differ from 9 October). Never charts the
historic rows.

## Body corrections (canonical note)

- Intro: "12 rows in the capture to date" now names both captures; "archives every past two-day-ahead forecast"
  replaced with NESO's description, quoted and attributed, plus "both captured archive files start at target
  2023-04-03".
- Files: added the 2026-10-16 recapture of both CSVs (names, sizes, rows, silver equals bronze).
- Current clocks: "For the one capture to date" and "Every silver row of a capture shares this one vintage" replaced
  with both vintages; event-time check extended to target 2026-10-18; forward-target evidence extended; the 16:15 BST
  observation now covers both vintages.
- Cardinal-point table scoped to the 2026-10-08 capture; recorded that `3C` and `4B` windows differ on 18 Oct, and
  that the change starts at target 2026-10-12 in the archive.
- Units: recorded that this current dictionary is the original the 1-day one repeats.
- Sentinels: blanks are 8 of 12 "in each capture".
- Correspondence with the archive: added the 2026-10-16 match (all 12 equal; vintages 8 s apart).
- Activation: base table 24 rows, `_latest` 12 after the recapture.
- Historic: vintage shared "by all 14,608 rows" replaced with both vintages and counts; time-stamp evidence for both
  captures; `F_Point` counts scoped (`NA` 3,479 on targets 2023-04-03 to 2024-07-13 in both; blanks 5,987 then
  6,059); identity uniqueness for both captures; coverage discrepancy made exact (start 2023-04-03, 2026-09-02 absent,
  9 to 12 points per date, a `DP` code); recapture appended to Activation.
- Cadence: "No scheduled gridflow refresh exists yet, so captures are on demand" replaced with two captures per
  tabular family; archive rewrite TODO updated with the append-only observation between the two captures.
- Holds: "in the capture to date its single target" now "in each capture to date".

## Unverified

- Whether the archive ever rewrites past rows over more than two captures (none rewritten between 8 and 16 Oct).
- Why the archive file starts at 2023-04-03 against NESO's "from 2018"; why target 2026-09-02 is missing.
- The cardinal-point code meanings beyond the dictionary's concept text (NESO lists no codes).

## Open questions

- `what_it_is` and `facts.history` state the archive file's start ("its October 2026 file starts in April 2023") as a
  dated fact about NESO's published file, read from the two captures. It is the honest counterweight to NESO's "from
  2018", but the checker should rule whether a dated vendor-file fact passes the no-local-data rule. Fallback: drop the
  clause and keep only "NESO describes the archive as all two-day-ahead forecasts from 2018", with the 2023 start in
  the note body only.
- Related is capped at 4: the 1-day and 2 to 14 day pages, Elexon `ndfd` (covers D+2) and `indo`. The 7-day page is
  not linked; the seat may prefer it over `indo`.

## Template problems

None new. At 768 the bar labels are small (about 9 px), as on the 1-day page; readable, not clipped.

## Defects

- **NESO 2-day-ahead archive coverage (vendor/data):** resource `24abd271` says "All historic 2 day ahead demand
  forecasts from 2018 to the most recent forecast", but both captured files (2026-10-08, 2026-10-16) start at target
  2023-04-03; target 2026-09-02 is absent; dates carry 9 to 12 cardinal points (783 of 1,294 dates have 11). A backtest
  from this archive has no 2018 to March 2023 history. No gridflow change.
- **NESO 2-day-ahead archive time stamps (vendor, already the hold question):** in both captures the newest
  `FORECAST_TIMESTAMP` (`...Z`) is 39 to 54 minutes after the file's CKAN `last_modified` read as UTC, consistent with UK
  local time mislabelled Z. For the NESO question packet with the 1-day, 7-day and 2 to 14 day archives.
- **NESO dictionaries (vendor):** the 1-day current dictionary is a copy of this 2-day one (confirmed direction: the
  2-day texts name their own lead); the 2-day original itself puts "1930" in `CP_END_TIME`'s unit field and calls the
  CP clocks "Time UTC" against the archive dictionary's UK time.
- No gridflow code defect found.

Nothing added to git or committed.

## Round 2 (review REVISE: 1 major, 1 nit), 2026-10-24

1. **Major, note body Cadence.** "none of which gridflow captured from the current file" was false for 2026-10-18 (the
   2026-10-16 current capture is that target). Now, as the review words it: "it added every target date 2026-10-10 to
   2026-10-18; gridflow had captured only 2026-10-18 of those from the current file."
2. **Nit, `page.notebook.cells[0]`.** The loop converting three columns is replaced by one line converting only
   `published_at`, the one time column the cell shows. `notebook.lead` now says "converts `published_at` to UTC" (35
   words, budget 35). Notebook artefacts regenerated with `run_notebooks.py`: no error, the table shows the same 12 rows
   in start-time order with `published_at` `2026-10-16 15:15:01.350931+00:00`; the plot cell is unchanged.

Gates: canonical note re-mirrored, `cmp` clean, 504 of 504 lines CRLF; `gridflow-build --only
neso_data_portal/demand_forecast_2d_day_ahead` wrote the page with no error; detector `[]`; 0 em dashes. Chart spec and
sample select unchanged, so the series and sample were not regenerated. No screenshots retaken: the only page change is
one sentence of the notebook lead and the first cell's code. Nothing added to git or committed.
