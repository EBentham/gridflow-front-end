# NESO Data Portal pages: FES: Pathways to Net Zero

Opened 2026-10-24 under the approved plan (ruling 62) and the resume (ruling 65). 5 full pages and 11 held pages (two
held batches), one branch and one PR stacked on Carbon intensity. Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-fes`, branch `feat/neso-dp-fes`, cut from
  `feat/neso-dp-carbon-intensity`. Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-fes`, branch `docs/neso-dp-fes`, cut from
  `docs/neso-dp-carbon-intensity`. Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (keep each
  note's line endings; Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it. If a lead
  table is the wrong choice for the chart or column guide, say so in your report; the seat reorders.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\fes\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: approved full pages in
  `BATCH-generation.md` and `BATCH-demand.md`; held batches in `interconnectors\held-*.md` and
  `carbon-intensity\held-*.md`.

## The pages

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `regional-breakdown-of-fes-data-electricity` | `fes_regional_demand_active_power`, `_dg_gt_1mw`, `_dg_lt_1mw`, `_dsr`, `_gsp_info`, `_storage_gt_1mw`, `_storage_gt_1mw_pre2023`, `_storage_lt_1mw`, `_storage_lt_1mw_pre2023` | 9941 | 9951 |
| 2 | `future-energy-scenario-fes-building-block-data` | `fes_building_blocks_block_definitions`, `_block_licence_area`, `fes_building_blocks_main` (held; seat reordered at the writer's request, 6c47d2c) | 9942 | 9952 |
| 3 | `resource-adequacy-in-2030s` | `resource_adequacy_2030s_results`, `_peak_demand`, `_portfolio` | 9943 | 9953 |
| 4 | `fes-natural-gas-demand-definitions-ed4` | `fes_ed4_gas_demand_defs` | 9944 | 9954 |
| 5 | `fes-road-transport-notes-data-table-ed6` | `fes_ed6_road_transport_notes` | 9945 | 9955 |
| H1 | Held: `building-heat-model` (`building_heat_model_example_output_half`, `building_heat_model_list_input` no silver), `fes-electricity-demand-summary-data-table-ed1` (`fes_ed1_electricity_demand`), `future-energy-scenario-electricity-supply-data-table-es1` (`fes_es1_electricity_supply`), `fes-european-electricity-supply-data-table-es2` (`fes_es2_european_supply`), `fes-flexibility-data-table-data-table-flx1` (`fes_flx1_flexibility`) | every table held | 9946 | 9956 |
| H2 | Held: `fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3` (`fes_ed3_heat_demand_natural_gas`, `_natural_gas_sum_ed`, `_sum_ed`), `fes-road-transport-summary-data-table-ed5` (`fes_ed5_road_transport`), `fes-whole-system-gas-supply-data-table-ws1` (`fes_ws1_gas_supply`), `fes-whole-system-gas-supply-emissions-data-table-ws2` (`fes_ws2_gas_emissions`), `local-authority-level-spatial-heat-model-outputs-fes` (`fes_la_heat_model_domestic`, `_residential`), `levelised-cost-of-green-hydrogen` (3 `lcoh_*` tables, no silver) | every table held | 9947 | 9957 |

Known risks:
- **Scenarios, not history:** FES rows are projections by scenario, edition (publication year) and year. Never chart a
  projection as history; name the scenario and edition in every chart caption; never mix editions in one series
  without saying so. Use NESO's scenario names as the file gives them.
- **Editions:** most tables have several editions (`latest_partition: resource_id` in the registry); state which
  edition a chart, frame or count uses and date it to NESO's file.
- **Size:** `fes_building_blocks_main` (about 1.3-1.6 million rows per edition) and `fes_regional_demand_active_power`
  (about 1.3 million) are large: read lazily, select columns, never collect whole tables.
- **Regional breakdown:** the `_pre2023` storage tables are separate gridflow tables (the writer found the 2022 file has
  the same header as 2023 and 2024); never sum across tables without saying so. GSP info is reference data.
- **WS1:** never sum across units (the ledger). **Local authority heat model:** the domestic and residential tables are
  separate; never join them.
- **Levelised cost of green hydrogen:** licence carve-out (gridflow ruling 477): publish nothing from the files; a
  catalogue page only (what it is, NESO's description, the files listed), stated plainly.
- **Building heat model:** the list-input file has no silver table; the example output is one January day.
- **Recaptures:** check every capture's row count and header; set `dedup:` when captures repeat rows.
- **Held pages:** one plain line per table on why rows are not shown, from the ledger's question, covering the whole
  table, no codes, no local-data references (dated NESO facts only). Keep shared wording the same across the batch
  where the question is the same.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own packages' files; never `git add`
or commit (the seat commits). Other agents work in the same worktrees: if the build stops on another package's files,
check your own built page and say so. Do not end your turn until your report or review is written. Correct
out-of-date note-body statements yourself when the data proves them wrong.

## Checked facts

See `BATCH-ancillary-b.md` "Checked facts": chart and frame artefacts read every silver capture, so set `dedup:` when
captures repeat rows (or as a guard). On a table with no event time, `query()` filters on the capture time (remediation
20at): use `data.sql()`. The column guide accepts only the lead table's columns.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| 1 | a0c28a65bd96ca1f4 | ad2d312da0c3c01c9 | checking; 20cc logged |
| 2 | a7d6f785b85eb39ff | a7baf4ea258c6e697 | checking; rebuilt under the definitions lead; 20cd logged |
| 3 | a12902a5b35eeed53 | | writing |
| 4 | | | |
| 5 | | | |
| H1 | | | |
| H2 | | | |
