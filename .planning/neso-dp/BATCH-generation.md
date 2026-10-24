# NESO Data Portal pages: Generation

Opened 2026-10-24 under the approved plan (ruling 62) and the resume (ruling 65). 5 full pages and 5 held pages, one
branch and one PR stacked on Demand. `daily-wind-availability` and `embedded-wind-and-solar-forecasts` are already live
pages (pre-v0.22); link to them, never edit them. Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-gen`, branch `feat/neso-dp-generation`, cut from `feat/neso-dp-demand`.
  Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-gen`, branch `docs/neso-dp-generation`, cut from `docs/neso-dp-demand`.
  Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (keep each note's line endings; Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\generation\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: approved pages in the earlier batch
  files (Demand, Trading and System are the most recent).

## The pages

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `day-ahead-wind-forecast` | `da_wind_forecast_day_ahead`, `_day_ahead_bmu`, `_historic_day_ahead` (held), `_historic_day_ahead_bmu` (held) | 9801 | 9811 |
| 2 | `14-days-ahead-operational-metered-wind-forecasts` | `metered_wind_forecast_14d`, `metered_wind_forecast_14d_windfarm` | 9802 | 9812 |
| 3 | `negative-reserve-active-power-margin-nrapm-forecast` | `nrapm_forecast_national_daily_days`, `_scotland_daily_days`, `nrapm_forecast_weekly_week_national` (held), `_weekly_week_scotland` (held) | 9803 | 9813 |
| 4 | `monthly-operational-metered-wind-output` | `metered_wind_output_monthly` | 9804 | 9814 |
| 5 | `tresp-generation-pathways` | `tresp_generation_pathways_resp_region`, `_gsp`, `_la_england`, `_la_scotland`, `_la_wales` (all eligible) | 9805 | 9815 |
| H1 | Held: `14-days-ahead-wind-forecasts` (`wind_forecast_14d_days_ahead`, `wind_forecast_14d_day_ahead_bmu`), `daily-opmr` (`daily_opmr`), `weekly-opmr` (`weekly_opmr`) | every table held | 9806 | 9816 |
| H2 | Held: `weekly-wind-availability` (`weekly_wind_availability`), `wind-bmu-boa-volumes` (`wind_bmu_boa_volumes`) | every table held | 9807 | 9817 |

Known risks:
- **Day-ahead wind forecast:** the two current files are eligible; the two archives are held (no vendor zone on the
  forecast time stamps; targets with two labels; the BMU archive is about 22 million rows over 8 resources: never load
  it whole). This page sets the pattern for the forecast pages in this group.
- **14-day metered wind forecasts:** both tables are eligible (gridflow's eligibility report; the ledger names only the
  forecast). The wind-farm table is large (about 182,000 rows): chart or frame a stated slice.
- **NRAPM:** the daily national and Scotland tables are eligible (date and settlement period); the weekly tables are held
  (load-factor and probability columns have no vendor unit or scale).
- **Monthly metered wind output:** nine monthly resources; the August and September overlap was adjudicated in gridflow
  (ADR-040): read it before stating coverage.
- **tRESP generation pathways:** every table is eligible (MW installed at 31 March); the seat made the RESP-region table
  the lead (smallest, regional). The demand package page (`tresp-demand-pathways`, approved) is the sibling: keep its
  wording on FES ids and NESO's dates. A member lists at most four requests. `query()` filters on capture time for tables
  with no event time: use `data.sql()`.
- **Recaptures:** check every capture's row count and header; set `dedup:` when captures repeat rows.
- **Held pages:** one plain line per table on why rows are not shown, from the ledger's question, covering the whole
  table, no codes, no local-data references (dated NESO facts only).

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own package's files; never `git add`
or commit (the seat commits). Do not end your turn until your report or review is written. Correct out-of-date
note-body statements (for example "only one capture") yourself when the data proves them wrong.

## Checked facts

See `BATCH-ancillary-b.md` "Checked facts": chart and frame artefacts read every silver capture, so set `dedup:` when
captures repeat rows (or as a guard); the workbench `query()` returns session-zone times. On a table with no event
time, `query()` filters on the capture time (remediation 20at): use `data.sql()` there. The column guide accepts only
the lead table's columns; describe a second table's columns in its member line.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | ab701b35a12d38c04 | a9de29bfc06aafd5d | APPROVED, nits fixed (seat-verified); committed; 20bq logged |
| 2 | a48d8b9e47c223da5 | | writing |
| 3 | ab264ea28a0b271b2 | a41945f902dcee342 | APPROVED (round 2 fixes seat-verified); committed; 20br logged |
| 4 | a433a0c274e3774e4 | ad0238aea64f407ad | APPROVED, nits fixed (seat-verified); committed; 20bp logged (overlap is 1 to 5 April 2026, not Aug-Sep) |
| 5 | ab173f966d65b4fd9 | | writing |
| H1 | | | not started |
| H2 | | | not started |
