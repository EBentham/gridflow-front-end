# NESO Data Portal pages: Demand Flexibility Service

Opened 2026-10-23 under the approved plan (ruling 62) and the resume (ruling 65). 3 full family pages, one branch and
one PR stacked on System. `demand-flexibility` (2024 onwards), the group's showcase, is already live. Bobbo looks at
the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-dfs`, branch `feat/neso-dp-dfs`, cut from `feat/neso-dp-system`.
  Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-dfs`, branch `docs/neso-dp-dfs`, cut from `docs/neso-dp-system`.
  Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (CRLF, Edit tool). (`C:\gridflow-wt\vault-dfs` is
  an older, unrelated worktree: never use it.)
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\dfs-packages\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: the live showcase
  `demand-flexibility` (same four-table shape; note in this worktree's `vault/neso_data_portal/`), and approved pages in
  the Ancillary services, Balancing costs, Constraint management and System batch files.

## The pages

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `demand-flexibility-service` (2023/24) | `dfs_utilisation_report_sum`, `dfs_utilisation_report`, `dfs_industry_notification`, `dfs_service_requirements` | 9871 | 9874 |
| 2 | `demand-flexibility-service-live-events` (2022/23) | `dfs_live_events_utilisation_report_sum`, `_utilisation_report`, `_service_update_industry`, `_service_requirement` | 9872 | 9875 |
| 3 | `demand-flexibility-service-test-events` (2022/23) | `dfs_test_events_utilisation_report_sum`, `_utilisation_report`, `_service_update_industry`, `_service_requirement` | 9873 | 9876 |

Known risks:
- **Three seasons of one service:** the showcase covers 2024 onwards; these pages cover 2023/24 and the 2022/23 live
  and test events. Never compare across seasons without saying the rules changed; never add test and live events.
- **Requirement tables:** the ledger holds `dfs_service_requirements` and `dfs_test_events_service_requirement` (no
  publication time); the live events requirement is eligible. One plain line per held member, from the ledger's
  question, no codes.
- **Times:** event windows are UK local time in NESO's files; establish the clock from code and rows; convert the
  workbench's session-zone times in the notebook.
- **Recaptures:** check every capture's row count and header; set `dedup:` when captures repeat rows.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own package's files. Do not end your
turn until your report or review is written.

## Checked facts

See `BATCH-ancillary-b.md` "Checked facts": chart and frame artefacts read every silver capture, so set `dedup:` when
captures repeat rows (or as a guard); the workbench `query()` returns session-zone times. On a table with no event
time, `query()` filters on the capture time (remediation 20at): use `data.sql()` there.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | a5b2ef126d1ac033c | abd767d645cc03653 | checking |
| 2 | ae543fe4acb47dc1f | | writing |
| 3 | a559298e77cdc9ea4 | | writing |
