# 7-day-ahead-national-forecast: writer's report

Family page `7-day-ahead-national-forecast`, lead `national_forecast_7d_day_ahead_demand` (eligible), member
`national_forecast_7d_historic_day_ahead` (held). Written 2026-10-24. The manifest's slug, lead and members are right.

Files:
- canonical note `C:\gridflow-wt\vault-neso-dem\30-vendors\neso-data-portal\datasets\7-day-ahead-national-forecast.md`
  (CRLF kept, 544 CRLF of 544 lines); mirror `C:\gridflow-wt\fe-neso-dem\vault\neso_data_portal\7-day-ahead-national-forecast.md`, `cmp` clean
- `site/hifi/data/series/neso_data_portal/national_forecast_7d_day_ahead_demand.json` (gridflow-distil, `spec_origin: vault`)
- `site/hifi/data/samples/neso_data_portal/national_forecast_7d_day_ahead_demand.json` (gridflow-sample)
- `site/hifi/data/notebooks/neso_data_portal/national_forecast_7d_day_ahead_demand.json` and `-4.png` (run_notebooks.py)
- page `site/hifi/data-sources/neso_data_portal/7-day-ahead-national-forecast.html`

Gates: `gridflow-build --only neso_data_portal/national_forecast_7d_day_ahead_demand` wrote the page, no error.
Detector `[]`. Zero em dashes in the page and in the `page:` block. No staged chart spec or authored override existed.

Screenshots (light) at 1440, 1024, 768 and 390 (390 through a 390 px iframe) in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\dem7d-writer\`
(`shot-<w>.png`, crops `c<w>-<n>.png`). Nothing clipped or overlapping. At 390 the longest bar labels
("01:00-01:30 trough", "04:30-07:30 trough") start about 14 px from the edge, as on the 1-day page. The site has no
dark theme. Server on 9843 started with its PID recorded (24131) and stopped by that PID only.

## What one row is

| Member | One row | Quantity | Demand definition |
|---|---|---|---|
| current (`national_forecast_7d_day_ahead_demand`) | one cardinal point of one target date seven days on: `targetdate` + `cardinalpoint`, with type (`F`/`T`/`P`) and window (`cp_st_time`, `cp_end_time`); 12 rows, one target date per file | `forecastdemand`, MW | national demand (ND) |
| historic (`national_forecast_7d_historic_day_ahead`) | the same, plus `forecast_timestamp`; one issue (one label) per target date in both captures | same | same |

Not a daily peak or minimum series and not seven days of rows: the current file is one target day's 12 points. So the
chart is a bar per cardinal point of that day, not a bar per day.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| ND definition (`what_it_is`) | catalogue snapshot `20261006T195819Z`, resource `70d3d674`: "National Demand is the Great Britain generation requirement ... excludes generation required to meet station load, pump storage pumping and interconnector exports." |
| Daily, 16:15 to 17:00 clock time (`facts.cadence`) | same resource: "Publication frequency: daily. Publication time: between 16:15 and 17:00 (clock time)." CKAN stamps `2026-10-06T15:15:02`, `2026-10-07T15:15:00`, `2026-10-16T15:15:01` all fall at 16:15 BST read as UTC. |
| Archive "from 2018" (`facts.history`, `what_it_is`, member `differs`) | resource `6f7408b4`: "All historic 7 day ahead demand forecasts from 2018 to the most recent forecast." Attributed to NESO on the page. |
| Archive skips June 2018 to April 2023 (`what_it_is`) | silver, both captures: target dates 2018-04-01 to 2018-06-28 (89 dates), then from 2023-04-08 daily, missing only 2023-04-17, 2024-08-28, 2024-12-14, 2026-09-07. A fact of NESO's file, not of local holdings; see Open questions. |
| MW (`chart.unit`, `forecastdemand`) | both 7-day dictionaries `FORECASTDEMAND` `unit: MW` (field-info `20261008T114228Z/national_forecast_7d_*.json`). Unlike the 1-day package, the current dictionary has the unit, so the field line carries no "from the archive" note. |
| Peak/trough/fixed (`cp_type`, key note) | both dictionaries: Fixed (a fixed time), Trough (minimum demands), Peak (maximum demands). |
| `f_point` codes | current dictionary comment: OM, DM, Dm, EM; the file carries `Om`. Empty on 8 of 12 rows in each capture. |
| CP windows "labelled UTC ... unconfirmed" (caption, `cp_st_time`) | both 7-day dictionaries: "Time UTC". No dictionary dispute here (the 1-day archive's says UK time); the note keeps the zone as `TODO: verify` (FACTS g1 measured UK-local alignment on medium-term families). |
| `targetdate` sent as `YYYYMMDD` | registry `7-day-ahead-national-forecast.json` current epoch `format: %Y%m%d`; bronze `7,20261023,...`. |
| `timestamp_utc` = start of the target date's first settlement period | registry `temporal: date_sp1` on `targetdate`; silver 2026-10-13 23:00 UTC for 14 Oct, 2026-10-22 23:00 UTC for 23 Oct. |
| `published_at` = NESO last-modified, read as UTC; no issue time | registry `vintage: ckan_last_modified`, `issue: none`; silver `published_at` equals each sidecar's `ckan_last_modified`. |
| Daysahead 7 | silver: every row of both captures. |
| `tail()` lead and notebook | same code path as the approved 1-day page (`_latest`, `ORDER BY targetdate DESC`, session zone); the run printed 12 rows for 2026-10-23 with `published_at` `2026-10-16 15:15:01.261954+00:00`, so the UTC conversion took effect. |
| Requests | sidecar `request_url` of the 2026-10-16 captures (`ng_demand_7da_20261023.csv`, `archive_7dayahead.csv`); connector downloads `upload` resources whole after `package_show`, skipping an unchanged `last_modified` (`client.py`; same rule and wording as the approved 1-day page, not re-traced line by line here). |
| Commands | `cli.py` ingest and transform take `--last` (lines 191, 266); same form as the approved 1-day page. |
| Related | `neso_data_portal.json` lists `1-day-ahead-demand-forecast` and `2-14-days-ahead-national-demand-forecast`; `elexon.json` family `demand-forecasts` has `ndfd` ("one figure a day", 2 to 14 days ahead, per `vault/elexon/ndf.md`), `demand-outturn` has `indo`. |

## Times and clock for the current file (its rows only)

- Two captures, 12 rows each, different target dates, no row repeated:
  - 2026-10-08 11:13 UTC: target 2026-10-14, file `ng_demand_7da_20261014.csv`, CKAN `2026-10-07T15:15:00.672524`;
  - 2026-10-16 20:40 UTC: target 2026-10-23, file `ng_demand_7da_20261023.csv`, CKAN `2026-10-16T15:15:01.261954`.
- Each target is seven days after its vintage date (the forward-target rule holds on both).
- Rows carry no time of their own beyond the date anchor; window clocks stay raw strings.

## Held historic file: hold line

`held: "Forecast time stamps end in Z, but NESO does not confirm UTC; the field is undocumented."` (16 words)

The first clause is the 1-day page's, word for word. The second follows this file's registry question ("has no vendor
definition and its zone is undocumented (values carry Z); whether it is the immutable issue instant"): NESO's 7-day
archive dictionary gives `FORECAST_TIMESTAMP` no title, description or unit, and has no email-recovery comment, so the
1-day's second clause does not apply.

A stronger, measured alternative for the seat, if preferred: four April 2018 target dates (1, 2, 3, 5 April) are stamped
`2018-05-18T11:42:55Z` to `11:51:13Z`, 43 to 47 days after the day they forecast, so the label is not always an issue
time. In the note body; not on the page.

## Captures, row counts, repeats

| Table | Capture | Bronze bytes / data rows | Silver rows | Notes |
|---|---|---|---|---|
| current | 2026-10-08 | 578 / 12 | 12 | target 2026-10-14 |
| current | 2026-10-16 | 578 / 12 | 12 | target 2026-10-23 |
| historic | 2026-10-08 | 1,043,045 / 15,703 | 15,703 | |
| historic | 2026-10-16 | 1,050,209 / 15,811 | 15,811 | all 15,703 earlier rows unchanged; 108 added (targets 15 to 23 Oct, 12 rows, one label each) |

Declared content lengths match. One label per target date and one row per (target, point) in both archive captures.
The current file's 12 rows equal the archive's on lead, target, point, value and window in both captures (14 Oct in
both; 23 Oct in the 16 Oct archive, label `2026-10-16T11:21:21Z`). Every label, read as UTC, is earlier than its
capture's `last_modified`. The chart and frame read both current captures (24 rows); the `targetdate` filter picks 12;
`dedup: {"on": [targetdate, cardinalpoint], order_by: published_at}` is set on both as a guard
(`duplicates_dropped: 0`).

## Chart

Bar chart, 12 bars, one per cardinal point of target 23 October 2026 (Friday, the newest), MW, from zero, in time-of-day
order through the `group_map` labels and `sort: label`. Windows checked against both captures: identical to the 1-day
page's labels (3C 1700-1800, 4B 1830-2000). Values: low 19,192 (04:30-07:30 trough), high 32,182 (18:30-20:00 peak).
As on the 1-day page, the `02:00-02:30 peak` (21,867) sits below the `01:00-01:30 trough` (21,902); the key note
covers it (each is its own window's extreme). The held archive is never charted.

## Body corrections (canonical note)

- Files: added the 2026-10-16 recapture of both CSVs (names, bytes, rows, CKAN stamps; silver equals bronze); added the
  archive's observed target-date coverage (2018-04-01 to 2018-06-28, then from 2023-04-08, four single missing dates),
  marking "all ... from 2018" as NESO's description.
- Intro: "holds every 7-day-ahead forecast since 2018, per the vendor" replaced by NESO's words, attributed, plus the gap.
- Current clocks: "For the one capture to date" and "All 12 silver rows share this one vintage" replaced with both
  vintages; both fall at 15:15 read as UTC. Event-time check and forward-target evidence extended to target 2026-10-23.
- "All rows of the capture carry `7`", the CP code list, "8 of the 12 rows", "measured unique on the capture" scoped to
  both captures; same windows on 14 and 23 Oct.
- Current versus archive: added the 2026-10-16 correspondence (12 of 12 equal, labels above).
- Historic clocks: "All 15,703 silver rows share this one vintage" replaced with both vintages and the append observation.
- `FORECAST_TIMESTAMP`: group counts scoped per capture; added the lead distribution (15,750 rows seven days, 13 six days,
  48 rows labelled 43 to 47 days after their target).
- Hold-text note and Holds: the quoted question was stale ("sit after the file's CKAN last_modified"); replaced with the
  registry's current question, and recorded that every label in each capture sits before `last_modified`.
- Nulls: "zero nulls" scoped to both captures.
- Cadence: "one capture of each resource ... no scheduled refresh exists yet" replaced with two captures; the
  append-or-rewrite TODO updated (fits a daily append; rewrites not ruled out).
- Activation: added the 2026-10-16 transforms (current 24 rows over two files, 12 in `_latest`; archive 15,703 and 15,811).

## Unverified

- Whether the CP windows are UTC or UK clock (dictionary says UTC; unconfirmed).
- Whether NESO ever rewrites the archive; two captures show only an append.
- What the 2018 `CARDINALPOINT` codes `04`, `4A`, `DP` mean (archive only; not on the page).

## Open questions

- `what_it_is` states the archive's gap ("the file skips from June 2018 to April 2023"). It is a property of NESO's
  published file, seen identically in both captures, not of local holdings; I judged it the most useful fact for a
  reader planning a backtest. If the seat reads it as a local-coverage statement, drop the clause (the sentence still
  stands on NESO's description).
- Related (cap 4): 1-day page, 2 to 14 day page, `elexon/ndfd`, `elexon/indo`. The 2-day page is left to the hub. The
  2 to 14 day file carries lead 7 too, but its 23 October values differ from this file's by up to 101 MW and it lacks
  point `4`, so the note says only "at every lead from 2 to 14 days".

## Template problems

None new. At 768 the bar labels are small (about 9 px), as on the 1-day page.

## Defects

- **NESO 7-day-ahead archive (vendor/data):** `FORECAST_TIMESTAMP` for targets 2018-04-01, 2018-04-02, 2018-04-03 and
  2018-04-05 (48 rows) reads `2018-05-18T11:42:55Z` to `11:51:13Z`, 43 to 47 days after the day forecast; 13 rows for
  2018-05-01 are labelled six days ahead. The label is not always an issue time. Evidence for the held question; no
  gridflow change.
- **NESO 7-day-ahead archive (vendor/data):** NESO describes the file as all forecasts from 2018, but its target dates
  run 2018-04-01 to 2018-06-28 and then resume on 2023-04-08 (missing also 2023-04-17, 2024-08-28, 2024-12-14,
  2026-09-07). For the NESO question packet.
- **gridflow registry vs note (doc):** the note's Holds line quoted an older generated question ("sit after the file's
  CKAN last_modified when read as UTC"), which is wrong for this archive (every label sits before); the registry already
  has the corrected wording, the note is now aligned. No code change.
- **Observed for the 2 to 14 day page (not mine):** its 2026-10-16 capture has 151 rows, not 156 (13 leads x 12), in
  `national_demand_fc_2_14d_days_ahead`; that writer should check.
- No gridflow code defect found.

Nothing added to git or committed.
