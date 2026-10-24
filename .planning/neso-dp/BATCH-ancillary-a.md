# NESO Data Portal pages: Ancillary services, part 1 (frequency response and reserve)

Opened 2026-10-18 under the approved overnight plan (`OVERNIGHT-PLAN.md`, ruling 62). 11 full pages and 4 held
pages, one branch and one PR. Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-as-a`, branch `feat/neso-dp-ancillary-a`, cut from
  `feat/neso-dp-template-pass` (the template fixes: several columns as series, y floor and gaps, related package
  slugs, the `needs` rule, several requests per member, held pages, long-span ticks, 390 px wrapping). Read
  `.planning/v5/author-brief.md` **in the worktree** (it documents the new options) and the template-pass report
  `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\template-pass\REPORT.md`.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-as-a`, branch `docs/neso-dp-ancillary-a` off quant-vault
  `origin/master` (be22305). Canonical notes: `30-vendors\neso-data-portal\datasets\<slug>.md` (CRLF: edit with the
  Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree, same filename as the canonical note. The
  seat made the first copy. After every edit, `cp` the canonical note over it and `cmp` it.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json` (families with
  `note`, or `package_tables` for one table). The lead is the first member. If the lead or the member list is wrong,
  say so in your report (or message the seat): never edit the manifest yourself.
- **Build:** `uv run --system-certs --extra build gridflow-build --only neso_data_portal/<lead key>`. Artefacts are
  staged under the lead key.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\ancillary-a\`
  (`<slug>-author.md`, `<slug>-review.md`, then `-review-2.md` and so on).
- **Owner's review server**, when running: port 9670. Never stop it.

## The pages

Data truth for each: the ledger row in `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\.planning\v0.22-FE-LEDGER.md`
(tables, row counts, which tables are eligible and which are held, with the question that holds them), the canonical
note, gridflow code (`connectors/neso_data_portal/`, `silver/neso_data_portal/`, `schemas/`, the registry), and local
silver `C:\gridflow-data\silver\neso_data_portal\<table>\` (read only, lazily, select columns).

| # | Page (slug) | Members, lead first (held tables marked) | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `balancing-reserve-auction-requirement-forecast` | `br_auction_requirement_fc_da`, `br_auction_requirement_fc_da_archive` (held), `br_auction_requirement_fc_medium_term` (held) | 9941 | 9961 |
| 2 | `dynamic-containment-data` | `dynamic_containment_dc_dr_dm_results`, `dynamic_containment_dc_dr_dm_block`, `dynamic_containment_masterdata`, `dynamic_containment_dc_dr_dm_results_sum` (held), `dynamic_containment_dc_dr_dm_linear` (held) | 9942 | 9962 |
| 3 | `dynamic-moderation-requirements` | `dm_requirements` | 9943 | 9963 |
| 4 | `dynamic-regulation-requirements` | `dr_requirements` | 9944 | 9964 |
| 5 | `quick-reserve-auction-requirement-forecast` | `qr_auction_requirement_fc` | 9945 | 9965 |
| 6 | `slow-reserve-requirement-forecast` | `slow_reserve_requirement_fc` | 9946 | 9966 |
| 7 | `static-firm-frequency-response-auction-results` | `sffr_auction_results_main`, `sffr_auction_results_buy_orders` (held) | 9947 | 9967 |
| 8 | `static-firm-frequency-response-requirement` | `sffr_requirement` | 9948 | 9968 |
| 9 | `phase-2-ffr-auction-results-summary` | `ffr_phase2_auction_phase_resultsum`, `_resultsbyunit`, `_blockorders`, `_block_order`, `_linearorders`, `_linear_orders`, then held: `ffr_phase2_auction_phase_results_sum`, `ffr_phase2_auction_phase_results_unit`, `ffr_phase2_result_summary_archive`, `ffr_phase2_results_by_unit_archive`, `ffr_phase2_blockorders_archive`, `ffr_phase2_linearorders_archive` | 9949 | 9969 |
| 10 | `firm-frequency-response-post-tender-reports` | `ffr_post_tender_reports_csv_ext`, `ffr_post_tender_reports_workbook` (held), `ffr_post_tender_reports_csv`, `ffr_post_tender_reports_ext` | 9950 | 9970 |
| 11 | `eac-auction-results` | `eac_results_summary`, `_summary_fy`, `_daily_summary`, `_by_unit`, `_by_unit_fy`, `_daily_by_unit`, `_buy_orders`, `_buy_orders_fy`, `_daily_buy_orders`, `_sell_orders`, `_daily_sell_orders` (all `eac_results_*`) | 9951 | 9971 |
| H | Held batch: `dynamic-containment-4-day-forecast` (`dc_forecast_4d`, `dc_forecast_4d_history`), `long-term-forecasts-for-dc-dm-dr-requirements` (`dc_dm_dr_long_term_fc`), `eac-mock-auction-results` (8 `eac_mock_results_*` tables), `eac-br-mock-auction-results` (4 `eac_br_mock_results_*` tables) | every table held | 9952 | 9972 |

Known risks:
- **Truncated captures (found 2026-10-18, defect 20i):** a re-check on 2026-10-16 stored a cut-off copy of at least one
  datastore table and its `_latest` view serves it. Before relying on `_latest` or `query()`, compare row counts across
  your table's captures; if the newest fell, build artefacts from the last complete capture, report it as a defect, and
  say nothing about it on the page (no local-data references).
- **EAC auction results:** 36.3M rows (`sell_orders` 32.3M). Read lazily, select columns, never collect a whole
  table. The ledger notes sell-order times are raw strings. The showcase EAC BR page found the workbench `query()`
  filters EAC tables on capture time (remediation 20c): check whether the same holds here before writing the notebook.
- **Phase 2 FFR:** two spellings of each family (`blockorders` and `block_order`, `linearorders` and
  `linear_orders`): establish whether they are different files or epochs and say so plainly; archives held
  (PHASE2-ARCHIVE-SEMANTICS); the 2019-11-22 by-unit member is held (collision).
- **FFR post-tender reports:** one silver family over three file shapes; the workbook family is held; TR123, TR125,
  TR147 and TR154 held; workbook and CSV overlap for TR139 to TR166 (never add them).
- **Dynamic containment data:** a retired package; results_sum and linear are held for price units.
- **Requirement forecasts (BR, quick, slow, DM, DR, SFFR):** small tables; establish what one row is, the issue time
  versus the delivery window, and whether the files keep earlier editions. Thin but accurate ships.
- **Held batch:** held pages per ruling 6 and the template's held mode (author-brief). The one plain line per table
  says why its rows are not shown, from the ledger's question, in plain words (no codes): for example "NESO's files
  do not say when each forecast was issued".

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

Everything in `.planning/v5/p26/BATCH-rest.md` sections "Shared-worktree rules" and "Seat rulings carried over"
applies unchanged, and `.planning/neso-dp/BATCH-dfs.md` "Bobbo's rulings for NESO package pages". Worked examples:
the four NESO showcase pages (`demand-flexibility`, `eac-br-auction-results`, `aggregated-bsad`,
`constraint-breakdown`, notes in the worktree's `vault/neso_data_portal/`), plus `elexon/demand-forecasts` (a family).
Several agents share the worktree: keep strictly to your own package's files.

## Shipped state

All 15 approved and committed. Gates green (pytest 204, build --check, htmlhint 0, lychee 0, detector [] x15).
Site PR https://github.com/EBentham/gridflow-front-end/pull/61 (base feat/neso-dp-template-pass), vault PR
https://github.com/EBentham/quant-vault/pull/64. Waiting for Bobbo's look. Merged into part 2's branches.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | ad9562a4783453cd8 | a50242a7703a8ea1e | APPROVED round 2; committed fe 739b914, vault 5be3d3d |
| 11 | a76d9b8cd4fa20a83 | aafbabed80d91a79c | APPROVED (round 3 fixes seat-verified); committed fe 2988786, vault 8514454 |
| H | ab9104ee227505a6f | a3fc7c0cd619579fa | APPROVED round 2, nits fixed; committed fe a5792ff, vault bf7b7f4 |
| 2 | ac1533bccfac8ccf9 | ab58ec729a213bb03 | APPROVED, nits fixed; committed fe dbb28af, vault e9690f0; ruling: ships from the complete 2026-10-08 capture, truncated 2026-10-16 capture logged as 20i, not on the page |
| 3 | a620ecd328b3178cb | afc8fb614d6583e8b | APPROVED, nits fixed; committed fe 9d989ff, vault ccb8e58 |
| 4 | a7c515de865ed2dbe | a2db251ee5aebc2b0 | APPROVED (round 2 majors seat-verified) ; committed |
| 5 | a064fc3f999458336 | a4f740413e7771f79 | APPROVED, nits fixed; committed |
| 6 | ad98aeca3cfc9a4db | a136e989d13cd2bc9 | APPROVED (round 2 major seat-verified); committed |
| 7 | ac5d1cc2d76dd8911 | a275028b640f86024 | APPROVED round 2; committed; 20j logged |
| 8 | adf1a644470e37e3a | a04b7a2ca87b61618 | APPROVED, nits fixed; committed |
| 9 | abbb4ef8abd514f95 | a5e5a58c455dc54d2 | APPROVED, nits fixed; committed a340491 |
| 10 | a04615370afb38a68 | aba46a9462e27bed3 | APPROVED, nits fixed; committed |

## Template follow-ups (seat items, not page findings)

- A family member lists at most four requests; EAC sell orders read 36 files (current month plus monthly archives).
- At 768 the folded frame can show no value column until unfolded; the unfolded frame scrolls sideways.
- The notebook preview breaks long names mid-word at 768 and 390.
- A series file built from local window times stamps them with `Z` (display is right; the file label is misleading).
- The notebook tab label clips at 390 px (EAC auction results).
- The notebook runner adds a stray column to grouped tables (seen in EAC results, DM, DR notebooks).
- A page allows at most three commands (FFR post-tender needed four: two sibling ingests plus pipeline).
- Bar-chart category labels longer than about 16 characters clip at 390 px (industry notifications).
- Chart specs: the text-time parse runs before filters (rows with another format fail even when filtered out); no weekly or monthly bucket for long daily spans.
- Chart and sample artefacts read every silver capture of a table; a table whose captures repeat rows needs a `dedup:` in its chart and frame (no default). Audited 2026-10-23: no approved page double-counts.
- A family page cannot list request URLs for files outside its members (monthly BSUoS forecast archive and PDF). Family pages do not print `raw_feed.requests` at all (DFS 2023/24 `package_show`).
- Bar labels round to two significant figures (Capacity Market clearing prices: £27.50 shows as 28, £22.50 as 22). Small values round to one decimal (resource adequacy LOLE).
- The sample frame cannot wrap long text, so a definitions or notes column is always folded (FES ED4).
- A held page whose tables have no silver still shows a "silver tables" heading (levelised cost of green hydrogen; ETYS, DNO and GIS pages likewise).
- A bronze-only package (no silver table) still renders the "silver, typed and validated" band and "The silver tables" heading (Demand Profile Dates); the hold line carries it, but the band should say there is no table.
- The column guide accepts only the lead table's columns (`build.py` line 1296); a second eligible member (transmission losses yearly table) has no guide of its own.
- A full page needs eight sample rows; a table with fewer rows can only ship held (voltage contracted units, one row). Boundary files (ETYS, GSP) have no line-map visual.
- Chart specs have no derived duration (end minus start), so utilisation hours cannot be charted from interval tables (stability midterm; likely Pathfinder utilisation).
- A 30-minute line chart gets a single x tick (whole-hour ticks only), seen on system frequency.
