# NESO Data Portal pages: Connection registers

Opened 2026-10-24 under the approved plan (ruling 62) and the resume (ruling 65). 3 full pages, one branch and one PR
stacked on Interconnectors. Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-cr`, branch `feat/neso-dp-connection-registers`, cut from
  `feat/neso-dp-interconnectors`. Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-cr`, branch `docs/neso-dp-connection-registers`, cut from
  `docs/neso-dp-interconnectors`. Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (keep each note's
  line endings; Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\connection-registers\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: approved full pages in
  `BATCH-generation.md` (reports in `generation\`) and `BATCH-demand.md`.

## The pages

| # | Page (slug) | Members | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `transmission-entry-capacity-tec-register` | `tec_register` | 9841 | 9851 |
| 2 | `embedded-register` | `embedded_register` | 9842 | 9852 |
| 3 | `interconnector-register` | `interconnector_register` (two Moyle stage rows overlap: never sum) | 9843 | 9853 |

Known risks:
- **Registers are reference tables with no event time:** `query()` filters on capture time, so notebooks use
  `data.sql()`. Dates in the registers (connection dates, effective-from) are what NESO states, not event times: never
  chart a projected connection date as history without saying so.
- **Charts:** an honest summary (for example MW by status or plant type, or connected capacity by year) with units and
  the capture date stated; a register changes in place, so date every count to NESO's file.
- **Interconnector register:** the two Moyle stage rows overlap; never sum MW across them.
- **Recaptures:** check every capture's row count and header; set `dedup:` when captures repeat rows.
- **Seat rulings carried over (Interconnectors, PROXY-SOURCED):** name a far-end country only where NESO's text or a
  cited source states it.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own package's files; never `git add`
or commit (the seat commits). Do not end your turn until your report or review is written. Correct out-of-date
note-body statements yourself when the data proves them wrong.

## Checked facts

See `BATCH-ancillary-b.md` "Checked facts": chart and frame artefacts read every silver capture, so set `dedup:` when
captures repeat rows (or as a guard). On a table with no event time, `query()` filters on the capture time (remediation
20at): use `data.sql()`. The column guide accepts only the lead table's columns.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | a1111bee79407f06f | a31a821522a5f04b0 | checking; 20bx logged; ships with the 16 Oct file gap stated (seat, PROXY-SOURCED, metered-wind precedent) |
| 2 | aef85fb4eda55cf26 | aa419d8314d16ce62 | checking; 20by logged |
| 3 | a9bfd403eeb22aae1 | aa193752879207a90 | REVISE (1 major: attribute the all-stages wording, Moyle 475/500; 4 nits), round 2 writing; 20bw logged; related links: seat kept the writer's four (TEC, embedded, IFA, BritNed) |
