# FES building block data: checker's review (round 1)

Page `neso_data_portal/future-energy-scenario-fes-building-block-data`, lead `fes_building_blocks_block_definitions`.

**Verdict: APPROVE.** 0 blockers, 0 majors, 5 nits.

Checks run:
- Build `--only neso_data_portal/fes_building_blocks_block_definitions`: no errors. The one warning (37 gotcha lines dropped) is global, not this page.
- Detector `[]`. Zero em dashes in the built page.
- Mirror `cmp`: identical to the canonical note.
- Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe). Nothing clipped or overlapping. At 768 and 390 the folded frame hides `technology_detail` (known fold follow-up, seat item).
- Server on port 9952 started and stopped by its own PID (the Windows python process listening on that port); nothing else touched.

## What I verified

**1. Nothing from the held main table reaches the page.**
- The three artefacts (series, samples, notebooks under the definitions key) contain no `fes_building_blocks_main` string. The page mentions main only in the hero chip, the family member's `differs` line (dimension names only), its two request URLs (each equals a bronze sidecar `request_url`) and the "Rows not shown" line.
- No value, range, scenario name, unit or row from main appears. The page has no "50 ids" fact; that stays in the note body.
- The old `fes_building_blocks_main.*` artefacts are gone; no stray file remains.
- Notebook cells read only the definitions and licence-area `_latest` views.
- I read main lazily (one column, `building_block_id_number`, distinct per edition) only to check the note's "Y on exactly the 50 ids" sentence. It is true for 2023, and the same 50 ids equal the 2022 Y set (16 N in both). Every main id has a same-edition definition in 2023, 2024 and 2025.

**2. The held line covers both parts.**
- The registry question (family record `eligibility.question`), ledger row 48 and the eligibility report all ask two things: the period the year labels denote (including the 2019/2020 baseline), and the omitted row-grain dimension behind the repeated 2020 to 2022 rows.
- Page: "NESO states no period for the year labels; 2020 to 2022 repeat rows with different values." That covers both, whole table, no codes, no planning words, no local-data reference, no em dash. "NESO states no period" matches the registry's "NESO's dictionaries state neither".
- Note Holds section agrees (81,664 / 10,974 / 55,410 rows sharing a key; bronze only).

**3. The count bar.**
- Reproduced from silver: 49, 64, 66, 66, 66, 66 (377 rows, one capture per edition, 0 duplicates). 2020 is 49 because the file has 53 table rows and 4 blank ones that the reader drops (note table: "53 / 49").
- Honest: bars are zero-based (the 49 and 64 bar lengths are in ratio 49:64), the caption says "rows in each edition's definitions file, a count of block ids, not projections", and the key note correctly dates the three September 2026 files (2021 file 2026-09-16, 2022 and 2023 files 2026-09-03).
- Useful enough to keep: it is the only quantity on a page whose lead is otherwise text, and the 49 to 64 step is the visible reason ids are joined on edition. It is weak (four equal bars) and the reason for the step lives only in notebook cell 4 (12 ids dropped, 27 added; verified). Keep; `type: none` is not needed here, unlike tRESP, which has no measure at all. See nit 4 for one clarification.

**4. The EV frame.** Truthful. The eight rows are NESO's own text, read from silver:
- `Lct_BB001`: "Pure Electric (cars & motorbikes)" becomes "(vans, cars & motorbikes)"; `comments` "Cars and Motorbikes" becomes "Light Vans,Cars and Motorbikes". `Lct_BB002` the same.
- `Lct_BB003` and `_004`: "other than cars and motorbikes" (comments "Vans, HGVs, Buses") becomes "other than vans, cars and motorbikes" (comments "HGVs and Buses").
- Ids identical; the wording is unchanged from 2021 to 2025. "Same ids, vans moved in 2021" is an accurate reading of NESO's definition text. At 1440 `technology_detail` is visible in the frame; `comments` is in the folded columns.

**5. The 2025 `Technology` defect.**
- Verified in bronze: `raw_20261008T105310Z_cc3118da-...csv` lines 26 to 37 are the 12 `Dem_` rows (`Dem_BB001a` to `Dem_BB009`), all `Offshore-Wind (off-Grid)`, the value of `Gen_BB024` on line 25. The 2024 file leaves them blank. Silver: 2025 12 of 12 filled, 2024 12 of 12 null, 2020 to 2023 read `Demand`.
- The note paragraph is accurate and cites the lines. The page's column guide states it. See nit 1 on dating.

**6. Everything else.**
- Licence-area table: 19 rows (14 DNO, 3 TO, 1 IDNO, 1 non-network connected, labelled `Not Connected` in the file). The first eight notebook rows match silver, and the Elexon groups are correct for the names.
- Notebook: five cells, definitions and licence-area only, outputs match silver. Tab and aria label now name the definitions lead.
- Related links: all four slugs are in the page set (tRESP, regional breakdown, DNO licence-area GIS, ED1). Only the regional-breakdown page exists in this partial build, so the others resolve on the full build.
- Note body corrections: ids not stable across editions (12 missing from 2021, 27 added) verified; Y/N flag (50/16, 2022 and 2023) verified; members reordered with `package_show` on the new lead verified in the diff.
- NESO quote, "not for regional pathways", ENA Open Networks and package creation date (2020-08-13) match the catalogue snapshot `20261006T195819Z`. All 13 request URLs match sidecars. The `last_modified` skip logic matches `client.py:1752-1765`.
- Column guide: `template` 62 of 66 null in 2024, `included_in_eso_data` 66 non-null in 2022 and 2023 only, `eso_additional_notes` and `eso_comments` scopes as stated.

## Findings

1. **Nit.** `record.fields.technology`. "in 2025 every demand row reads `Offshore-Wind (off-Grid)`" is stated but not dated and is ambiguous. "2025" is the edition and does not say which file or capture, and the low-carbon demand blocks (`Lct_`, template "Demand Low Carbon Technologies") read `Electric Vehicles`, so "demand row" means only the 12 `Dem_` rows. Suggest: "in the FES 2025 file (last modified 14 July 2025), the 12 `Dem_` rows read `Offshore-Wind (off-Grid)`, a fill-down; the 2024 file leaves them blank". Evidence: bronze lines 26 to 37; registry `last_modified` 2025-07-14T04:48:17Z.
2. **Nit.** `record.fields.alignment_with_ofgem_core_scenario_key_drivers`. "From 2021, NESO's matching Ofgem core scenario driver" implies the cell is filled from 2021. Silver non-null counts: 2021 to 2024, 13 of 64 or 66 rows; 2025, 66 of 66 (many read "Not mentioned in Ofgem Core Scenario BBs"). The sample shows null on `Lct_BB002` in 2021. Suggest: "from 2021; filled on 13 blocks to 2024, on every block in 2025".
3. **Nit.** `notebook.cells[1]` (the dropped-ids cell). The runner's display cuts `technology_detail` to "Transmission connected interconnection of othe...", which then shows on the page. Drop `technology_detail` from that select, or accept the runner's truncation.
4. **Nit.** `chart_view.caption`. 66 blocks per edition can read as "66 projected". NESO's own `Included in ESO Data` flag in the definitions (Y on 50, N on 16, 2022 and 2023 only) supports one clause without touching main, for example "NESO flags 50 of the 66 as included in ESO data in 2022 and 2023". Optional; the current caption is already honest.
5. **Nit.** `facts.vendor`. "13 CSVs, one per table and FES edition" suggests every table has every edition; the licence-area mapping has only the 2024 file (6 + 6 + 1). "13 CSVs: six editions each of two tables and a 2024 licence-area mapping" is exact. Also `how_used[0]`: "block for block" goes slightly beyond NESO's wording ("clarity on alignment of FES and DFES"); fine to keep if "(NESO's stated purpose)" is read loosely.

No gridflow or data defects beyond the 2025 `Technology` fill-down already in the writer's Defects section. The page-set lead is now an eligible table, so the earlier lead problem is resolved.
