# NESO Data Portal pages: Balancing costs

Opened 2026-10-23 under the approved plan (ruling 62) and the resume (ruling 65). 1 full page and 7 held pages, one
branch and one PR stacked on Ancillary services part 2. `constraint-breakdown` is already live (showcase). Bobbo looks
at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-bc`, branch `feat/neso-dp-balancing-costs`, cut from
  `feat/neso-dp-ancillary-b`. Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-bc`, branch `docs/neso-dp-balancing-costs`, cut from
  `docs/neso-dp-ancillary-b`. Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (CRLF, Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\balancing-costs\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: approved Ancillary services pages
  (notes in this worktree's `vault/neso_data_portal/`, reviews in `.planning\neso-dp\ancillary-a\` and `ancillary-b\`),
  and the live showcase `constraint-breakdown` in this group.

## The pages

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `current-balancing-services-use-of-system-bsuos-data` | `current_bsuos_ii`, `_sf`, `_rf`, `_historic_ii`, `_historic_sf`, `_historic_rf`, `_cap_adjustments` (all `current_bsuos_*`) | 9921 | 9931 |
| H1 | Held: `bsuos-fixed-tariffs` (`bsuos_fixed_tariffs`), `gb-system-inertia-bid-and-offer-costs` (`inertia_bid_offer_costs`), `balancing-services-use-of-system-bsuos-daily-forecast` (`bsuos_daily_forecast`, bronze only), `daily-balancing-costs-balancing-services-use-of-system` (`daily_balancing_costs`, bronze only) | every table held | 9922 | 9932 |
| H2 | Held: `daily-balancing-volume-balancing-services-use-of-system` (`daily_balancing_volume`, bronze only), `bsuos-monthly-forecast` (8 `bsuos_monthly_forecast_*`), `skip-rates` (11 `skip_rates_*`) | every table held | 9923 | 9933 |

Seat ruling (PROXY-SOURCED, 2026-10-23): `skip-rates` ships held, as the approved plan and the live hub classify it
("the files don't say when each row was first published"), although the ledger lists a `skip_rates_summary` eligible
pair. Raised for Bobbo at the group's PR.

Known risks:
- **Current BSUoS charges:** seven tables over three settlement runs (II, SF, RF) and their historic files; the ledger
  notes an adjudicated HI3/HI4 overlap in `historic_ii`; `cap_adjustments` may have no record. A member lists at most
  four requests. Establish what one row is per run and never add runs together. Check every capture's row count.
- **Held pages:** one plain line per table on why rows are not shown, from the ledger's question, no codes.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own package's files.

## Checked facts

See `BATCH-ancillary-b.md` "Checked facts": NESO decodes the reserve service codes; chart and frame artefacts read every
silver capture, so set `dedup:` when captures repeat rows; the workbench `query()` returns session-zone times.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | a84288460a7068afd | a6599d96979f38d15 | APPROVE with 4 nits; writer fixing; 20y-20ab logged |
| H1 | ae43a22f0a09c23a0 | a8462fd681419a9cf | APPROVED x4, nits fixed (seat-verified); committed |
| H2 | a320e8f970e6cee02 | | writing |
