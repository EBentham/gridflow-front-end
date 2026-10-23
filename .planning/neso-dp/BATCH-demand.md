# NESO Data Portal pages: Demand

Opened 2026-10-23 under the approved plan (ruling 62) and the resume (ruling 65). 6 full pages and 7 held pages, one
branch and one PR stacked on Trading. Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-dem`, branch `feat/neso-dp-demand`, cut from `feat/neso-dp-trading`.
  Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-dem`, branch `docs/neso-dp-demand`, cut from `docs/neso-dp-trading`.
  Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (keep each note's line endings; Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\demand\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: approved pages in the earlier batch
  files (System, Demand Flexibility Service and Trading are the most recent).

## The pages

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `1-day-ahead-demand-forecast` | `demand_forecast_1d_day_ahead_national`, `demand_forecast_1d_historic_day_ahead` (held) | 9841 | 9851 |
| 2 | `2-day-ahead-demand-forecast` | `demand_forecast_2d_day_ahead`, `demand_forecast_2d_historic_day_ahead` (held) | 9842 | 9852 |
| 3 | `7-day-ahead-national-forecast` | `national_forecast_7d_day_ahead_demand`, `national_forecast_7d_historic_day_ahead` (held) | 9843 | 9853 |
| 4 | `2-14-days-ahead-national-demand-forecast` | `national_demand_fc_2_14d_days_ahead`, `_days_ahead_half` (held), `_historic_day` (held) | 9844 | 9854 |
| 5 | `national-demand-balancing-mechanism-units` | `national_demand_bmus` (a reference list) | 9845 | 9855 |
| 6 | `tresp-demand-pathways` | `tresp_building_block_definitions`, `tresp_gsp_area_names` (the eligible workbook reference tables), `tresp_demand_pathways_gsp`, `_la_england`, `_la_scotland`, `_la_wales`, `_resp_region` (all five held) | 9846 | 9856 |
| H1 | Held: `day-ahead-half-hourly-demand-forecast-performance` (`da_demand_fc_performance`), `daily-demand-update` (`daily_demand_update`), `demand-profile-dates` (`demand_profile_dates`, bronze only: NESO repeats identical rows), `historic-demand-data` (`historic_demand`) | every table held | 9847 | 9857 |
| H2 | Held: `long-term-2-52-weeks-ahead-national-demand-forecast` (`demand_forecast_2_52w`), `school-holiday-percentages` (`school_holiday_percentages`), `transmission-losses` (`transmission_losses_main`, `_financial_year`) | every table held | 9848 | 9858 |

Known risks:
- **The four forecast pages share a shape:** a current file of a dozen-odd rows (eligible) and a large historic file
  (held: NESO does not confirm the zone of the forecast time stamps). The current file is small: pick an honest chart or `type: none`; never chart
  the held historic rows. Page 1 sets the pattern; keep the four pages'
  wording for the shared hold the same.
- **tRESP demand pathways:** only the two workbook reference tables are eligible; the five pathway tables are held
  (annual GWh interval, suffixed block ids). The lead is the first pathway table by manifest order; a reference-table
  chart may not fit, so `type: none` is fine. A member lists at most four requests.
- **National demand BM units:** a reference list (no time series); `query()` filters on capture time for tables with
  no event time (use `data.sql()`).
- **Transmission losses:** the ledger names no hold question but the hub holds it; the writer establishes the honest
  reason from the notes and data, or recommends a full page with numbers for the seat to rule.
- **Recaptures:** check every capture's row count and header; set `dedup:` when captures repeat rows.
- **Held pages:** one plain line per table on why rows are not shown, from the ledger's question, no codes, no
  local-data references (dated NESO facts only).

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own package's files. Do not end your
turn until your report or review is written. Correct out-of-date note-body statements (for example "only one
capture") yourself when the data proves them wrong.

## Checked facts

See `BATCH-ancillary-b.md` "Checked facts": chart and frame artefacts read every silver capture, so set `dedup:` when
captures repeat rows (or as a guard); the workbench `query()` returns session-zone times. On a table with no event
time, `query()` filters on the capture time (remediation 20at): use `data.sql()` there.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | a607859324f54582c | abfa72550bccbf2e7 | APPROVED (round 2 fixes seat-verified); committed; 20bg logged |
| 2 | aaa530902e16c13ba | | writing |
| 3 | a09b4921a2eb9b6ea | | writing |
| 4 | | | not started |
| 5 | aff832a32c1030ea2 | ab3dc8141aec8a48f | APPROVED (round 2 fixes seat-verified); committed; 20bf logged |
| 6 | a9e81f314a34edccf | a6c15891c978684e7 | APPROVED (round 2 fixes seat-verified); committed; lead changed to the building-block table (seat, PROXY-SOURCED) |
| H1 | a403343c59ca240d0 | abed098ced7d8bb2c | revising (3 APPROVE with nits, historic REVISE: 1 major); 20bh, 20bi logged |
| H2 | a33842486afc7e15e | | writing |
