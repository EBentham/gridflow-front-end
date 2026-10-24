# NESO Data Portal pages: Strategic Energy Planning, and Data Portal changes and known issues

Opened 2026-10-24 under the approved plan (ruling 62) and the resume (ruling 65). The last two groups, one package each,
each on its own branch and PR (SEP stacked on FES, DPC stacked on SEP). With these the page set holds all 131 packages.
Bobbo looks at the pages before merge.

The plan counted the SSEP shapefile package as a full page. It has no silver table (bronze ZIPs only), so it ships held,
as the ETYS boundaries, DNO licence-area and GIS charging-zone packages did (seat, PROXY-SOURCED).

## Where things are

- **SEP:** front-end `C:\gridflow-wt\fe-neso-sep` (`feat/neso-dp-sep`, cut from `feat/neso-dp-fes`), vault
  `C:\gridflow-wt\vault-neso-sep` (`docs/neso-dp-sep`, cut from `docs/neso-dp-fes`).
- **DPC:** front-end `C:\gridflow-wt\fe-neso-dpc` (`feat/neso-dp-dpc`, cut from `feat/neso-dp-sep`), vault
  `C:\gridflow-wt\vault-neso-dpc` (`docs/neso-dp-dpc`, cut from `docs/neso-dp-sep`).
- Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` in the vault worktree (keep line endings; Edit tool);
  mirror `vault\neso_data_portal\<slug>.md` in the front-end worktree; `cp` and `cmp` after every edit. Never edit the
  page set. Read `.planning\v5\author-brief.md` in the front-end worktree.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\sep-dpc\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`.

## The pages

| # | Page (slug) | Members | Worktree | Writer port | Checker port |
|---|---|---|---|---|---|
| 1 | `data-portal-planned-changes-known-issues` | `portal_known_issues` (241 rows, eligible) | `fe-neso-dpc` | 9961 | 9971 |
| H | Held: `ssep-onshore-publication-zone-shapefile` (`ssep_publication_zones_files`, bronze only: 3 ZIPs, onshore, offshore and economic zones) | held | `fe-neso-sep` | 9962 | 9972 |

Known risks:
- **Known issues register:** a text register NESO edits in place (planned changes and known issues, with dates and
  statuses). Treat it like the industry notifications and event registers: an honest summary chart (for example items
  by status or by month raised, dated to NESO's file) or `type: none`; quote NESO's text; never claim an issue is
  resolved unless the row says so; check every capture and set `dedup:`. A table with no event time: use `data.sql()`.
- **SSEP shapefiles:** state the three ZIPs as NESO gives them; claim nothing about zone counts or geometry beyond
  what the files state (charging-zone precedent: separate dated sentences, no equivalence); cut coordinate-system
  wording unless the file states it. NESO's draft and final SSEP: say which the files are only where NESO does.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own package's files; never `git add`
or commit (the seat commits). Do not end your turn until your report or review is written.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | a38fce4dccab3dbc6 | ae9fe78524bd08512 | REVISE (1 major: 8 Oct values attributed to gridflow's capture; 5 nits), round 2 writing; 20ci logged |
| H | a0b72c16a49a0f95f | | writing |
