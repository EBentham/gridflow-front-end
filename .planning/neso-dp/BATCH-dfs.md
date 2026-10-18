# NESO Data Portal: the Demand Flexibility Service page (first package page)

Opened 2026-10-18. Bobbo approved one writer (Opus 5.5 · high) and one checker (Sonnet 5.5 · high), on the real
dataset template, no variants: NESO pages match every other dataset page on the site exactly.

## Where things are

- **Front-end worktree:** `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a46469c2-19b0-4f57-b2d5-81c7c1abca22\scratchpad\fe-neso`
  - Branch `feat/neso-dp-package-pages`. The build now reads one note per package (manifest `families[].note`).
  - The page is family `demand-flexibility`, members lead first: `demand_flexibility_utilisation_summary`,
    `demand_flexibility_utilisation_report`, `demand_flexibility_industry_notification`,
    `demand_flexibility_service_requirement`.
  - **Artefacts** (sample, chart series, notebook) are staged under the lead key `demand_flexibility_utilisation_summary`.
  - **Build:** `uv run --system-certs --extra build gridflow-build --only neso_data_portal/demand_flexibility_utilisation_summary`.
- **Vault worktree:** `C:\gridflow-wt\vault-dfs`, branch `docs/neso-dp-dfs-page` off quant-vault `origin/master`.
  - Canonical note: `30-vendors\neso-data-portal\datasets\demand-flexibility.md` (CRLF; edit with the Edit tool).
- **Mirror:** `vault\neso_data_portal\demand-flexibility.md` in the front-end worktree, same filename. After every
  edit, `cp` the canonical note over it and `cmp` it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\dfs\`
  (`demand-flexibility-author.md`, `demand-flexibility-review.md`, then `-review-2.md` and so on).
- **Ports:** writer 9911, checker 9921.

## The other three showcase pages (added 2026-10-18; same worktrees, same rules)

Bobbo set the scope on 2026-10-18: the hub plus these four showcase pages only. All four are written in parallel
in the shared worktree, so keep strictly to your own files (BATCH-rest "Shared-worktree rules").

| Page (slug) | Tables, lead first | Artefacts and `--only` key | Writer port | Checker port | Reports |
|---|---|---|---|---|---|
| `demand-flexibility` | as above | `demand_flexibility_utilisation_summary` | 9911 | 9921 | `dfs\demand-flexibility-*.md` |
| `eac-br-auction-results` (family, Balancing Reserve auction results) | `eac_br_results_summary`, `eac_br_results_by_unit`, `eac_br_results_buy_orders`, `eac_br_results_sell_orders` | `eac_br_results_summary` | 9912 | 9922 | `eac-br\eac-br-auction-results-*.md` |
| `aggregated-bsad` (single) | `aggregated_bsad` | `aggregated_bsad` | 9913 | 9923 | `bsad\aggregated-bsad-*.md` |
| `constraint-breakdown` (single) | `constraint_breakdown` | `constraint_breakdown` | 9914 | 9924 | `constraint\constraint-breakdown-*.md` |

Build with `--only neso_data_portal/<artefacts key>`. Canonical notes: `30-vendors\neso-data-portal\datasets\<slug>.md`
in the vault worktree; mirrors `vault\neso_data_portal\<slug>.md` in the front-end worktree.

Seat-checked facts for these three (reproduce before relying on them):
- **Constraint breakdown:** per day, cost (£) and volume (MWh) for four reasons: largest loss, inertia, voltage,
  thermal. Not "constraints, reserve, response, energy". 3,470 rows over 10 resources (ledger).
- **Aggregated BSAD:** 166,944 rows; the ledger records A01/A02 `UnicodeDecodeError` and A07
  `DuplicateEntityKeyError` as failed resources: the page must not imply those resources are covered.
- **Balancing Reserve auction results:** 3.9M rows (by_unit 621,111, buy_orders 98,592, summary 57,216,
  sell_orders 3,124,058). Read silver lazily and select columns.

## Rules

- Writer: `.planning/v5/author-brief.md` (including "Family pages"). Checker: `.planning/v5/review-rubric.md`.
  Anatomy: `DESIGN.md` "Dataset page anatomy". Everything in `.planning/v5/p26/BATCH-rest.md` sections
  "Shared-worktree rules" and "Seat rulings carried over" applies here unchanged.
- **Worked examples:** `elexon/demand-forecasts` (lead `ndf`, a family), `elexon/system_prices` (price line),
  `elexon/remit` (event register), `neso_data_portal/historic_generation_mix` (this vendor).
- **Data truth:** local silver `C:\gridflow-data\silver\neso_data_portal\demand_flexibility_*\` (read only);
  gridflow code `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\src\gridflow\` (`connectors/neso_data_portal/`,
  `silver/neso_data_portal/`, `schemas/`); the ledger row for `demand-flexibility` in
  `..\gridflow\.planning\v0.22-FE-LEDGER.md`; the canonical note itself.

## Bobbo's rulings for NESO package pages (2026-10-16)

- The page matches the live dataset pages exactly: "What it is and how it's used" with the facts table beside it, a
  chart with its commentary, the raw feed, the silver frame with the fold-out `…` (never a scrolling frame) and its
  column guide, the notebook, related datasets.
- **Held parts say why.** `demand_flexibility_service_requirement` is held (no publication time): it is listed with
  its raw files, and one plain line says why its rows are not shown. No chart, sample or notebook for it.
- This page documents only the current-service package `demand-flexibility`. The three frozen DFS packages are other
  pages; related links to them are fine.

## Facts the seat already checked (reproduce before relying on them)

- Archive season 2024-11-29 to 2026-03-27; current resources from 2026-04-14 (adds `event_id`, `event_type`
  Upwards/Downwards, UTC labels). Archive and current are disjoint seasons, not copies.
- Keys: summary and requirement `resource_id, delivery_date, window_from, service_requirement_type`; report adds
  `dfs_unit_id`. Notification is archive-only.
- Summary procured and cost equal the sum of the report's Accepted rows: never add the two tables. A Rejected row's
  `dfs_procured_mw` is the bid, not a volume bought.
- Event 141 (2026-10-05, 17:00 to 20:00 local): 500 MW asked each window; accepted 48.5, 50.1, 181.1, 182.0, 20.7,
  19.9 MW; 45 accepted bids at 18:00.
- The archive utilisation report is ingested but not tabled (ledger: ADR-040 check failed); the page must not imply
  the report covers the archive season.
