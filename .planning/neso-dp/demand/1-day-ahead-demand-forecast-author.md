# 1-day-ahead-demand-forecast: writer's report

Family page `1-day-ahead-demand-forecast`, lead `demand_forecast_1d_day_ahead_national` (eligible), member
`demand_forecast_1d_historic_day_ahead` (held). Written 2026-10-23/24.

Files:
- canonical note `C:\gridflow-wt\vault-neso-dem\30-vendors\neso-data-portal\datasets\1-day-ahead-demand-forecast.md`
  (CRLF kept, 505 CRLF of 505 lines); mirror `C:\gridflow-wt\fe-neso-dem\vault\neso_data_portal\1-day-ahead-demand-forecast.md`, `cmp` clean
- `site/hifi/data/series/neso_data_portal/demand_forecast_1d_day_ahead_national.json` (gridflow-distil, spec_origin vault)
- `site/hifi/data/samples/neso_data_portal/demand_forecast_1d_day_ahead_national.json` (gridflow-sample)
- `site/hifi/data/notebooks/neso_data_portal/demand_forecast_1d_day_ahead_national.json` and `-4.png` (run_notebooks.py)
- page `site/hifi/data-sources/neso_data_portal/1-day-ahead-demand-forecast.html`

Gates: `gridflow-build --only neso_data_portal/demand_forecast_1d_day_ahead_national` wrote the page with no
error on it (the two errors it filters out belong to other writers' held pages: `da_demand_fc_performance`
`page.held` 17 words, `demand_profile_dates` `related[1].note` 13 words). Detector `[]`. Zero em dashes in the
page. No staged chart spec or authored override existed for this dataset.

Screenshots (light) at 1440, 1024, 768 and 390 (390 through a 390 px iframe), in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\dem1d-writer\`
(`shot-<w>.png`, cropped `c<w>-<n>.png`). Nothing clipped or overlapping; at 390 the longest bar labels
("01:00-01:30 trough", "04:30-07:30 trough") start about 14 px from the edge. The site has no dark theme (no
dark rules in `theme.css`, `tokens.css` or `site.js`), so there is no dark view to check. Server started on
9841 with its PID recorded and stopped by that PID only.

## What one row is

| Member | One row | Quantity | Demand definition |
|---|---|---|---|
| current (`demand_forecast_1d_day_ahead_national`) | one cardinal point of one target date: `targetdate` + `cardinalpoint`, with type (`F`/`T`/`P`) and window (`cp_st_time`, `cp_end_time`) | `forecastdemand`, MW | national demand (ND) |
| historic (`demand_forecast_1d_historic_day_ahead`) | the same, plus `forecast_timestamp`; several issues per target point | same | same |

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| ND definition (`what_it_is`) | NESO resource description, catalogue snapshot `20261006T195819Z` (gridflow `.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json`): "National Demand is the Great Britain generation requirement ... excludes generation required to meet station load, pump storage pumping and interconnector exports." |
| Twice daily, 09:00 to 09:15 and 12:00 to 12:15 clock time (`facts.cadence`) | same resource description: "Publication frequency: twice daily ... between 09:00 & 09:15 and between 12:00 & 12:15 (clock time)". The two captures' CKAN stamps (08:00:00 and 11:00:01 UTC) fall at 09:00 and 12:00 BST when read as UTC. |
| Archive from 2018 (`facts.history`, `what_it_is`, member `differs`) | historic resource description: "All historic day ahead demand forecasts from 2018 to the most recent forecast." |
| MW (`chart.unit`, `forecastdemand` field) | historic dictionary `FORECASTDEMAND` `unit: MW` (field-info `20261008T114228Z/demand_forecast_1d_historic_day_ahead.json`). The current dictionary leaves the unit blank (and calls it "2 day ahead", copied); the field line says the unit is from the archive dictionary. |
| Peak/trough/fixed (`cp_type`, key note) | both dictionaries: Fixed (a fixed time), Trough (minimum during a set period), Peak (maximum during a set period), F/T/P. |
| `f_point` codes | dictionary comment: OM overnight minimum, DM daytime peak, Dm daytime minimum, EM evening peak; file carries `Om`. Empty (not null) on other rows: silver, 8 of 12 rows in each capture. |
| CP clock zone dispute (caption, `cp_st_time`) | current dictionary: "Time UTC"; historic dictionary: "relative to the timezone in effect in the UK at the forecast time and date". |
| `targetdate` sent as `YYYYMMDD` | registry `1-day-ahead-demand-forecast.json` current epoch `format: %Y%m%d`; bronze `1,20261017,...`. |
| `timestamp_utc` = start of the target date's first settlement period | registry `temporal: date_sp1` on `targetdate`; silver: 2026-10-08 23:00 UTC for 9 Oct, 2026-10-16 23:00 UTC for 17 Oct. |
| `published_at` = NESO last-modified, read as UTC; no issue time | registry `vintage: ckan_last_modified`, `issue: none`; ADR-030; silver `published_at` equals each capture's `ckan_last_modified` in the bronze sidecar. |
| `query()`/`tail()` read `_latest`, date column `targetdate`, lineage dropped, session zone | probe with the gridflow_models interpreter: `_validate_dataset_for_source` returns `targetdate`; relation `silver_neso_data_portal_demand_forecast_1d_day_ahead_national_latest`; returned times are `datetime64[us, Europe/London]`; DuckDB `TimeZone` = `Europe/London`; `event_time`, `available_at`, `source_run_id`, `dataset_version` absent. `tail()` is `ORDER BY targetdate DESC LIMIT n` (`research/handles/source.py`). |
| Requests (member `request`) | connector `client.py`: `url_type: upload` members are downloaded whole from the resource URL after one `package_show`, skipped when `last_modified` is unchanged. URLs are the bronze sidecars' `request_url` for the 2026-10-16 captures. |
| Commands | same `--last 24h` form as the approved Nord Pool and DFS pages; `cli.py` ingest and transform both take `--last`. |
| Related links | `site/hifi/data/neso_data_portal.json` lists `2-day-ahead-demand-forecast` and `2-14-days-ahead-national-demand-forecast` (same cardinal-point columns in silver; the 2 to 14 day package also has the `_half` half-hourly table); `elexon.json` families `demand-forecasts` (`ndf`) and `demand-outturn` (`indo`). |

## Times and clock for the current file (scoped to its rows)

- Two captures, 12 rows each, different target dates, no row repeated:
  - 2026-10-08 10:05 UTC: target 2026-10-09, CKAN `last_modified` 2026-10-08T08:00:00.985148 (morning slot);
  - 2026-10-16 20:02 UTC: target 2026-10-17, file `ng_demand_1da_20261017.csv`, CKAN 2026-10-16T11:00:01.383712 (midday slot).
- Each target date is later than its capture's vintage (the forward-target rule still holds).
- The rows carry no time of their own beyond the date anchor; window clocks stay raw strings, zone disputed by NESO's two dictionaries.

## Held historic file: the shared hold line

`held: "Forecast time stamps end in Z, but NESO does not confirm UTC; some are email-recovery times."` (15 words)

For the 2-day, 7-day and 2 to 14 day pages: keep the first clause word for word, "Forecast time stamps end in Z,
but NESO does not confirm UTC", and end it with a full stop, or add a second clause only where that file's own
question adds one (the 7-day and 2 to 14 day registry questions say "the field has no vendor definition"; only the
1-day dictionary has the email-recovery comment).

Note: the batch file and launch prompt call this a "settlement-time zone" question. The registry's question
(`registry/1-day-ahead-demand-forecast.json`, eligibility of `demand_forecast_1d_historic_day_ahead`) is about the
`FORECAST_TIMESTAMP` zone, whether it is the immutable issue instant, and the email-recovery rows. The line follows
the registry.

## Captures, row counts, repeats

| Table | Capture | Bronze data rows | Silver rows | Notes |
|---|---|---|---|---|
| current | 2026-10-08 | 12 | 12 | target 2026-10-09 |
| current | 2026-10-16 | 12 | 12 | target 2026-10-17 |
| historic | 2026-10-08 | 58,561 | 58,561 | |
| historic | 2026-10-16 | 58,657 | 58,657 | all 58,561 earlier rows unchanged; 96 added (targets 10 to 17 Oct, 12 rows, one issue each) |

No truncation (declared content lengths 578 and 3,895,968 bytes match). The chart and frame read both current
captures (24 rows); the filter on `targetdate` picks 12, and `dedup: {"on": [targetdate, cardinalpoint],
order_by: published_at}` is set on both as a guard (it drops nothing today: `duplicates_dropped: 0`). It keeps
the later publication if a morning and a midday file for the same target are ever both captured.

## Chart

Bar chart, 12 bars, one per cardinal point of target 17 October 2026 (the newest), MW, from zero, ordered by time
of day through `group_map` labels ("00:30 fixed" ... "24:00 fixed") with `sort: label`. No time axis: every row of
a target date shares one midnight anchor and the window clocks are disputed strings, so a time line would invent
instants. Values: 20,520 (04:30-07:30 trough) to 31,966 (18:30-20:00 peak). Never charts the historic rows.

## Body corrections (canonical note)

- Files: added the 2026-10-16 recapture of both CSVs (names, sizes, rows; silver equals bronze).
- Current family clocks: "For the one capture to date" and "All 12 silver rows share this one vintage" replaced
  with both vintages, read as UTC they fall in NESO's two slots; event-time check extended to the second capture;
  forward-target evidence extended to target 2026-10-17.
- Cardinal-point layout: scoped to the 2026-10-08 capture; recorded that `3C` and `4B` windows differ on 17 Oct
  (1700-1800, 1830-2000), so windows are not fixed per code.
- CP clock zone conflict: the "12 current rows equal their archive counterparts" claim scoped to 2026-10-08; on
  2026-10-16 the windows match but all 12 values differ (midday publication not in the archive at its 11:00:18
  vintage). Unit transfer sentence scoped the same way.
- Sentinels: blanks are 8 of 12 rows in each capture.
- Activation: second capture added; base table 24 rows, `_latest` 12.
- Historic: "All 58,561 rows share this one vintage" replaced with both vintages and the append observation;
  `F_Point` counts scoped (36,300 `NA` / 2,414 blank on 8 Oct; 36,300 / 2,478 on 16 Oct); the "label after
  last_modified" evidence scoped to the 2026-10-08 capture, noting the 16 Oct capture does not test it.
- Cadence: second slot observed; one observation on the midday revision; the append-or-rewrite TODO updated;
  "Captures to date: one per family ... No scheduled refresh has run yet" replaced with two per tabular family.

## Unverified

- Whether the archive ever keeps the midday publication: the 96 rows added between captures carry one issue per
  target date, and the 17 Oct issue in the archive is the morning one (08:36:38Z) while the current file held a
  different midday forecast. Two captures cannot settle the archive's rule.
- The cardinal-point code meanings beyond the sample curve image (TODO stands in the note).
- Whether the 09:00 and 12:00 publications always differ; one observed pair did.

## Open questions

- Related is capped at 4. I chose the 2-day and 2 to 14 day pages plus Elexon `ndf` and `indo`; the 7-day page
  is not linked (the hub lists it). The seat may prefer the 7-day page over `indo`.
- The notebook uses `tail()` rather than `query()` with dates, so a reader's own capture reproduces it (the
  current file only ever holds the next day). The siblings can reuse the same two cells with their table key.

## Template problems

- `--only` scopes errors by table key, so an error naming a family slug (`1-day-ahead-demand-forecast`) would be
  filtered out as "not rendered" when building by the lead's table key. Not hit here; worth a look.
- At 768 the wide bar drawing is scaled down and its labels are small (about 9 px). Readable, not clipped.

## Defects

- **NESO 1-day-ahead demand forecast, current file dictionary (vendor):** the `aec5601a` dictionary is copied from
  the 2-day package: `FORECASTDEMAND` described as "National 2 day ahead demand forecast values" with no unit,
  `DAYSAHEAD` unit "2", `CP_END_TIME` unit "1930". Its CP clocks say "Time UTC" while the archive dictionary says
  UK time in effect. Already in the note; for the NESO question packet if not there.
- **NESO 1-day-ahead archive (vendor/data):** between captures 2026-10-08 and 2026-10-16 the archive added exactly
  one issue per target date (96 rows, 8 dates), the morning one, although the current file published a different
  midday forecast for 17 October. If the archive keeps only one issue per day, a backtest built from it sees the
  09:00 forecast, not the 12:00 revision. Needs more captures to confirm; no gridflow change.
- No gridflow code defect found.
