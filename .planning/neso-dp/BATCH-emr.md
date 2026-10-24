# NESO Data Portal pages: Electricity Market Reform

Opened 2026-10-24 under the approved plan (ruling 62) and the resume (ruling 65). 1 full page (8 tables), one branch and
one PR stacked on Network charges. Bobbo looks at the page before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-emr`, branch `feat/neso-dp-emr`, cut from
  `feat/neso-dp-network-charges`. Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-emr`, branch `docs/neso-dp-emr`, cut from
  `docs/neso-dp-network-charges`. Canonical note `30-vendors\neso-data-portal\datasets\capacity-market-register.md`
  (keep its line endings; Edit tool).
- **Mirror:** `vault\neso_data_portal\capacity-market-register.md` in the front-end worktree; the seat made the first
  copy; `cp` and `cmp` after every edit.
- **Page set:** the seat added the package to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\emr\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: approved multi-table full pages in
  `BATCH-generation.md` and `BATCH-demand.md`.

## The page

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `capacity-market-register` | `capacity_market_auction_static` (lead), `_auction_cost`, `_unit_cmu`, `_unit_cmu_history`, `_components`, `_component_history`, `_component_history_pre`, `_de_rating_factors` (all eligible) | 9901 | 9911 |

Build with `--only neso_data_portal/capacity_market_auction_static`.

Known risks:
- **Personal data:** `capacity_market_unit_cmu` (and probably its history and component tables) carries contact
  telephone numbers and email addresses. Never show contact columns in the frame, the column guide, the notebook
  output or the chart. Name the columns' existence at most, never their values.
- **Size:** `capacity_market_component_history_pre` has about 1.9 million rows. Read it lazily, select columns, and
  never collect the whole table.
- **Auctions, not time series:** rows belong to auctions (T-1, T-4, early auction) and delivery years. Chart an honest
  per-auction or per-delivery-year summary (for example, clearing price in GBP per kW per year by auction). Say what
  the money units are as NESO gives them. Never invent a time axis from capture times.
- **Recaptures:** check every capture's row count and header; set `dedup:` when captures repeat rows.
- **Notebook:** if the lead table has no event time, `query()` filters on the capture time (remediation 20at), so use
  `data.sql()`.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own package's files; never `git add`
or commit (the seat commits). Do not end your turn until your report or review is written. Correct out-of-date
note-body statements yourself when the data proves them wrong.

## Checked facts

See `BATCH-ancillary-b.md` "Checked facts": chart and frame artefacts read every silver capture, so set `dedup:` when
captures repeat rows (or as a guard). The column guide accepts only the lead table's columns.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | ab7eef35f60c4efae | a65e1ecf6ab01097f | REVISE (1 major: summed awarded MW worded as a NESO total; 8 nits; privacy clean), round 2 writing; 20ca logged (CMU change log carries contact data); bar-label rounding added to template follow-ups |
