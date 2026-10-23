# NESO Data Portal pages: Trading

Opened 2026-10-23 under the approved plan (ruling 62) and the resume (ruling 65). 1 full page and 6 held pages, one
branch and one PR stacked on Demand Flexibility Service. Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-trd`, branch `feat/neso-dp-trading`, cut from `feat/neso-dp-dfs`.
  Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-trd`, branch `docs/neso-dp-trading`, cut from `docs/neso-dp-dfs`.
  Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (keep each note's line endings; Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\trading\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: approved pages in the Ancillary
  services, Balancing costs, Constraint management, System and Demand Flexibility Service batch files.

## The pages

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `day-ahead-power-exchange-prices-nordpool` | `nordpool_da_prices` | 9861 | 9864 |
| H1 | Held: `balancing-services-contract-enactment` (`bs_contract_enactment_balancing`, `_balancing_service`), `index-linked-contract-volume` (`index_linked_contract_volume`), `super-stable-export-limit-contract-enactment` (`ssel_contract_enactment`) | every table held | 9862 | 9865 |
| H2 | Held: `historic-gtma-grid-trade-master-agreement-trades-data` (`gtma_trades_data`, `_data_pre`, `gtma_trades_fy`), `interconnector-requirement-and-auction-summary-data` (`ic_requirement_auction`), `upcoming-trades` (`upcoming_trades`) | every table held | 9863 | 9866 |

Seat ruling (PROXY-SOURCED, 2026-10-23): `historic-gtma-grid-trade-master-agreement-trades-data` ships held, as the
approved plan and the live hub classify it, although the ledger notes `gtma_trades_data` GU1 to GU5 and
`gtma_trades_data_pre` as eligible. Same pattern and ruling as `skip-rates`; raised for Bobbo at the group's PR.

Known risks:
- **Nord Pool day-ahead prices:** the ledger lists the table eligible with a caveat: "temporal none: delivery instant
  not composed". Establish from code and rows what the delivery hour and date columns are and their clock; never
  invent a delivery instant gridflow does not compose; say what the rows support. Check every capture's row count.
- **Held pages:** one plain line per table on why rows are not shown, from the ledger's question, no codes, no
  local-data references (dated NESO facts only).

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
| 1 | afd2889b06d512586 | a96ad836058109e39 | checking; 20az, 20ba logged |
| H1 | ab801ef4b9396fd64 | ad23a4f1b295468b5 | checking; 20bb, 20bc logged |
| H2 | | | not started |
