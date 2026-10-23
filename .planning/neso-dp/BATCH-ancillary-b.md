# NESO Data Portal pages: Ancillary services, part 2 (instructions, STOR, notifications, BSAD)

Opened 2026-10-18 under the approved overnight plan (ruling 62). 10 full pages and 4 held pages; branch and PR stacked
on part 1 (`BATCH-ancillary-a.md`). Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-as-b`, branch `feat/neso-dp-ancillary-b`, cut from
  `feat/neso-dp-ancillary-a` (template fixes plus part 1). Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-as-b`, branch `docs/neso-dp-ancillary-b`, cut from
  `docs/neso-dp-ancillary-a`. Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (CRLF, Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\ancillary-b\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: part 1's approved pages (notes in
  this worktree's `vault/neso_data_portal/`) and their reviews in `.planning\neso-dp\ancillary-a\`.

## The pages

| # | Page (slug) | Members, lead first (held marked) | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `ancillary-services-important-industry-notifications` | `as_industry_notifications_balancing`, `_dc_dm_dr`, `_quick_reserve`, `_slow_reserve`, `_stor_important`, `_sffr_important` (held) | 9981 | 9991 |
| 2 | `balancing-services-adjustment-data-forward-contracts` | `bsad_forward_contracts` | 9982 | 9992 |
| 3 | `non-bm-ancillary-service-dispatch-platform-asdp-instructions` | `asdp_instructions` | 9983 | 9993 |
| 4 | `obp-non-bm-reserve-instructions` | `obp_reserve_instructions` | 9984 | 9994 |
| 5 | `obp-non-bm-physical-notifications` | `obp_physical_notifications` | 9985 | 9995 |
| 6 | `obp-reserve-availability-utilisation-price` | `obp_reserve_avail_price` | 9986 | 9996 |
| 7 | `optional-downward-flexibility-management-odfm-market-information` | `odfm_market_information_instructed`, `_load_factors` (held), `_results` (ingest only, no table) | 9987 | 9997 |
| 8 | `short-term-operating-reserve-stor-day-ahead-auction-results` | `stor_da_auction_results` | 9988 | 9998 |
| 9 | `short-term-operating-reserve-stor-day-ahead-buy-curve` | `stor_da_buy_curve` | 9989 | 9999 |
| 10 | `stor-windows` | `stor_windows` | 9980 | 9990 |
| H | Held: `contract-transfer-of-obligation` (`contract_transfer_obligation`, bronze only), `disaggregated-bsad` (`disaggregated_bsad`, ingest only: identical repeated rows), `non-bm-ancillary-service-dispatch-platform-asdp-window-prices` (`asdp_window_prices`), `obligatory-reactive-power-service-orps-utilisation` (`orps_utilisation_reactive`, `_historic_reactive`, `_reactive_default`) | every table held | 9979 | 9978 |

Known risks:
- **Truncated captures (defect 20i):** compare row counts across captures before relying on `_latest`; if the newest
  fell, build from the last complete capture, report it, say nothing on the page.
- **BSAD forward contracts:** 149,424 rows; F01/F05 `DuplicateEntityKeyError` recorded failures (ledger): the page
  must not imply those files are covered (the Aggregated BSAD showcase handled the same).
- **OBP physical notifications:** 495,086 rows; lazy reads.
- **Industry notifications:** text registers (event registers); the SFFR file is held.
- **STOR buy curve:** the package has a TXT hash document; one family.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own package's files.

## Checked facts (start from these; do not re-claim the opposite)

- **NESO does decode the reserve service codes** (checked 2026-10-23 by two checkers against the catalogue snapshot
  `20261006T195819Z`): `quick-reserve-auction-requirement-forecast` reads "Negative Quick Reserve (NQR) and Positive
  Quick Reserve (PQR)"; `slow-reserve-requirement-forecast` reads "Negative Slow Reserve (NSR) and Positive Slow Reserve
  (PSR)"; the ASDP notes give "Regional Development Programme (RDP) MegaWatt (MW) Dispatch". A package whose own
  dictionary leaves a code bare can cite these; never write that NESO decodes none of them.
- **Chart and frame artefacts read every silver capture of a table.** If captures repeat rows, set `dedup:` on the
  chart and frame (the OBP prices page is the example).
- **The workbench `query()` returns times in the session zone (Europe/London here)**, not UTC: convert in the notebook.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| H | ac4d838fad146bef9 | a7e1cd9d58f2518e1 | APPROVED round 2, nits fixed; committed |
| 1 | a7bdadeddd98e7449 | a9acc70ea35be78d3 | APPROVED (round 2 fixes seat-verified); committed fe d4016f1, vault 79941a2; 20n logged |
| 2 | ab90e4f799035d73c | aa9f90d2aabec7096 | APPROVED (round 2 fixes seat-verified); committed; 20o logged |
| 3 | abd18a84e1f5fabb1 | a7cca7dbb557ffe18 | APPROVED (round 2 fixes seat-verified); committed; 20p logged |
| 4 | a1153f90d0765c153 | a90a0afe04c073de9 | APPROVED, nits fixed (seat-verified); committed; 20q, 20r logged |
| 5 | a1aa64f9f77a3ac69 | a734d2629fc8d1a47 | revising (REVISE: 3 majors, 6 nits); 20t logged |
| 6 | ad2a23efea2aeecaa | ae6d34b6e498b163c | APPROVED (round 2 fixes seat-verified); committed; 20s logged |
| 7 | aa1a3c5e76550588d | a67b67c815e99b01b | APPROVED, nits fixed (seat-verified); committed; 20u logged |
| 8 | a0f4c6cf3e400cbf2 | ac7ecf986ba87acc7 | checking; 20v logged |
| 9 | a4f649837fdbcd49c | | writing |
| 10 | | | not started |

## Template follow-ups (seat items, not page findings)

See `BATCH-ancillary-a.md`.
