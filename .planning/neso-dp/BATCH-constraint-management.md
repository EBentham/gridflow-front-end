# NESO Data Portal pages: Constraint management

Opened 2026-10-23 under the approved plan (ruling 62) and the resume (ruling 65). 2 full pages and 6 held pages, one
branch and one PR stacked on Balancing costs. Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-cm`, branch `feat/neso-dp-constraint-management`, cut from
  `feat/neso-dp-balancing-costs`. Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-cm`, branch `docs/neso-dp-constraint-management`, cut from
  `docs/neso-dp-balancing-costs`. Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (CRLF, Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\constraint-mgmt\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: approved pages in
  `BATCH-ancillary-a.md`, `BATCH-ancillary-b.md` and `BATCH-balancing-costs.md` (notes in this worktree's
  `vault/neso_data_portal/`), and the live showcase `constraint-breakdown`.

## The pages

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `thermal-constraint-costs` | `thermal_constraint_costs`, `thermal_constraint_costs_xlsx` | 9901 | 9911 |
| 2 | `outturn-voltage-costs` | `outturn_voltage_costs_main`, `outturn_voltage_costs_historical` | 9902 | 9912 |
| H1 | Held: `24-months-ahead-constraint-cost-forecast` (`constraint_cost_fc_24m`), `24-months-ahead-constraint-limits` (`constraint_limits_24m`), `constraint-management-intertrip-service-information-cmis` (`cmis_intertrip`), `day-ahead-constraint-flows-and-limits` (`da_constraint_flows_limits`, capture failed) | every table held | 9903 | 9913 |
| H2 | Held: `operational-transparency-forum-network-congestion-data` (`otf_network_congestion`), `voltage-requirement` (`voltage_requirement`) | every table held | 9904 | 9914 |

Known risks:
- **Thermal constraint costs:** five yearly resources plus a workbook family; the ledger holds the 2021-22 resource;
  CSV and workbook years may overlap (never add them). Check every capture's row count.
- **Outturn voltage costs:** the current file has 38 rows and the historical file 2,508; the lead is the current file
  by seat choice; say in the report if the historical member should lead.
- **Held pages:** one plain line per table on why rows are not shown, from the ledger's question, no codes.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own package's files. Do not end your
turn until your report or review is written.

## Checked facts

See `BATCH-ancillary-b.md` "Checked facts": chart and frame artefacts read every silver capture, so set `dedup:` when
captures repeat rows (or as a guard where a recapture would); the workbench `query()` returns session-zone times.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | a646042e31a645f9b | | writing |
| 2 | | | not started |
| H1 | | | not started |
| H2 | | | not started |
