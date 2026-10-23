# NESO Data Portal pages: System

Opened 2026-10-23 under the approved plan (ruling 62) and the resume (ruling 65). 7 full pages and 3 held pages, one
branch and one PR stacked on Constraint management. Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-sys`, branch `feat/neso-dp-system`, cut from
  `feat/neso-dp-constraint-management`. Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-sys`, branch `docs/neso-dp-system`, cut from
  `docs/neso-dp-constraint-management`. Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (CRLF, Edit
  tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\system\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: approved pages in the
  Ancillary services, Balancing costs and Constraint management batch files.

## The pages

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `system-frequency-data` | `system_frequency`, `_dmy_csv`, `_gmt_csv`, `_gmt_zip`, `_offset_csv`, `_offset_zip` (all `system_frequency*`) | 9881 | 9891 |
| 2 | `system-inertia` | `system_inertia` | 9882 | 9892 |
| 3 | `system-inertia-cost` | `system_inertia_cost` | 9883 | 9893 |
| 4 | `etys-gb-transmission-system-boundaries` | `etys_boundaries_files` | 9884 | 9894 |
| 5 | `gis-boundaries-for-gb-grid-supply-points` | `gis_grid_supply_points` | 9885 | 9895 |
| 6 | `monthly-utilisation-data-of-voltage-contracted-units` | `voltage_units_utilisation` | 9886 | 9896 |
| 7 | `stability-midterm-y-1-utilisation-report` | `stability_midterm_y1` | 9887 | 9897 |
| H | Held: `gis-boundaries-for-gb-dno-license-areas` (`gis_dno_license_areas_files`), `stability-pathfinder-service-information` (`stability_pathfinder_availability_report`, `_utilisation_report`), `system-operating-plan-sop` (`system_operating_plan`) | every table held | 9888 | 9898 |

Known risks:
- **System frequency:** very large (per-second readings over many files); read lazily, select columns, never collect
  a whole table; several file shapes (DMY, GMT, offset; CSV and ZIP); establish the clock of each shape.
- **Boundary and GIS packages:** the rows may be geometry or file lists rather than time series; a chart may not fit;
  a map or `type: none` is the honest choice, never a forced time chart.
- **Many packages were recaptured on 16 October 2026:** check every capture's row count and header; set `dedup:`.
- **Held pages:** one plain line per table on why rows are not shown, from the ledger's question, no codes.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own package's files. Do not end your
turn until your report or review is written.

## Checked facts

See `BATCH-ancillary-b.md` "Checked facts": chart and frame artefacts read every silver capture, so set `dedup:` when
captures repeat rows (or as a guard); the workbench `query()` returns session-zone times.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | a749fd6f6e38f1073 | a4b317c69d5ba7fda | APPROVED (round 2 fixes seat-verified); committed; 20am-20ao logged |
| 2 | ac585660b723d140a | a3abd3888b5279e42 | APPROVED, nits fixed (seat-verified); committed; 20ap logged |
| 3 | a241e64afe1c76794 | aea3ffa34ed013ff7 | APPROVED (round 2 fixes seat-verified, quarter count reproduced); committed (full page despite held bid-and-offer sibling: ledger eligible, gaps stated; seat, PROXY-SOURCED); 20aq, 20ar logged |
| 4 | a63dff72e875b5c9b | afa0890b88337ca91 | APPROVED (round 2 fixes seat-verified); committed; held (one shapefile, no silver table: seat accepts, PROXY-SOURCED) |
| 5 | a53100ea68ce297c5 | a232c0e595357601a | APPROVED (round 2 fixes seat-verified against silver); committed; 20at, 20aw logged |
| 6 | a28ffdf91cd9e7bae | a542f7fbadd95327a | APPROVED, nits fixed (seat-verified); committed; held (one row: seat accepts, PROXY-SOURCED); 20as logged |
| 7 | af7ffe5a7853e4a94 | a1fb8deb58ea211a4 | APPROVED (round 2 fixes seat-verified); committed; 20au, 20av logged |
| H | a02e1e6b7b10036a6 | ab0cdc7993c9d4848 | revising (DNO, SOP APPROVE + nits; Pathfinder REVISE 1 major; DNO: keep requests, cut CRS wording, seat PROXY-SOURCED); 20ax, 20ay logged |
