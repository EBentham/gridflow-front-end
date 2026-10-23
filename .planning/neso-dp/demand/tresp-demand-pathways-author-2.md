# tRESP demand pathways: writer's report, round 2 (new lead)

Seat ruling (PROXY-SOURCED, manifest commit `8b73997`): the family leads with `tresp_building_block_definitions`,
then `tresp_gsp_area_names`, then the five held pathway tables.

## What changed

- **Page block, `page.family.members`:** reordered to the manifest order. The `package_show` request moved from the
  GSP pathway member to the new first member (`tresp_building_block_definitions`), which now lists two requests
  (`package_show`, the workbook). `tresp_demand_pathways_gsp` now lists only its CSV. No other field mentioned the
  lead or member order, so nothing else changed. `record.select.silver` stays explicit
  (`neso_data_portal/tresp_building_block_definitions`), which is now also the lead's own table.
- **Artefacts:** deleted only my two untracked old-key files
  (`site\hifi\data\samples\neso_data_portal\tresp_demand_pathways_gsp.json`,
  `site\hifi\data\notebooks\neso_data_portal\tresp_demand_pathways_gsp.json`). I regenerated them under the new key:
  - `gridflow-distil`: "no chart (spec type none)"; no series file.
  - `gridflow-sample`: the same eight rows, 16 columns.
  - `scripts/run_notebooks.py`: 5 cells, 0 errors (12 demand blocks; counts by sector and unit; five area names).
- **Mirror:** canonical note (CRLF, 661 lines) copied to `vault\neso_data_portal\tresp-demand-pathways.md`; `cmp`
  clean.

## Gates

- `gridflow-build --only neso_data_portal/tresp_building_block_definitions`: no errors, page written.
- Detector `[]`; 0 em dashes.
- Rendered member order: building blocks, GSP area names, then GSP, England, Scotland, Wales, RESP region. Five
  "Rows not shown" lines, one per held pathway table.
- Round 1's template problem is fixed by the new lead. The notebook tab reads
  `tresp_building_block_definitions.ipynb`. The notebook label says "cells on
  neso_data_portal/tresp_building_block_definitions", and the frame label reads that table too.
- No server or background process started this round (seat instruction), so no new screenshots. The page's
  structure changed only in the raw-feed member order. Round 1's screenshots at all four widths showed nothing
  clipped, so the member reorder should not affect layout.

## Review fixes (checker's `tresp-demand-pathways-review.md`, REVISE, 2 majors and 4 nits)

All six fixed. Build `--only neso_data_portal/tresp_building_block_definitions` clean (budgets enforced), detector `[]`,
0 em dashes, mirror `cmp` clean (CRLF, 662 lines). Prose only, so the sample and notebook artefacts are unchanged and
their digests still pass.

1. **Major, `record.fields.fes_bb_id_number` and the body:** now "Pathway files' `building_block_id`; only the suffixed
   ids match no Future Energy Scenarios (FES) id" (14 words). Before writing "only", I checked all 35 ids against
   silver `fes_building_blocks_block_definitions`. All 31 unsuffixed ids match exactly (8 demand, 18 generation,
   5 storage); the four suffixed demand ids match none. The body sentence in the `tresp_building_block_definitions`
   section now says the same, dated 2026-10-24 and naming the table checked.
2. **Major, shared held line (five members):** now "NESO states no period for annual GWh values, and four block ids
   match no FES id." (16 words). `what_it_is` now ends "The page shows rows from the two lists of blocks and
   areas, none from the pathway files." That says plainly that the whole pathway files are not shown. To stay within
   60 words I dropped the "such as electric vehicles and heat pumps" example, which the summary already gives.
3. **Nit, FES expanded once:** in the `fes_bb_id_number` column note ("Future Energy Scenarios (FES)").
4. **Nit, `demand_generation_storage`:** "NESO's 35 blocks span demand, generation and storage".
5. **Nit, `how_used[0]`:** "NESO says DNOs will use it for their ED3 plans, 2028 to 2033".
6. **Nit, `facts.cadence`:** "Ad hoc (NESO); files last modified 30 January 2026, as at 6 October 2026".

No new defect. GSP, DNO and ED3 are still not expanded on the page, because the checker's nit asked only for FES.

## Unchanged from round 1

Evidence table, held line, body correction (dated "one capture" check), open items and Defects all stand as in
`tresp-demand-pathways-author.md`. No gridflow defect.
