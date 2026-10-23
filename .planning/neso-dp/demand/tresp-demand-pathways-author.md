# tRESP demand pathways: writer's report (round 1)

Page `neso_data_portal/tresp-demand-pathways`, a family page, lead `tresp_demand_pathways_gsp` (held). Build
`--only neso_data_portal/tresp_demand_pathways_gsp`: no errors. Detector `[]`. No em dashes in the page.

## The decision on the held lead

The page can show eligible rows honestly with a held lead, so I recommend neither a lead change nor a held page.
The template reads the frame from any silver table named in `record.select.silver` (`artefacts.sample_silver`,
`artefacts.py`), with precedent on approved pages (industry notifications, current BSUoS). The frame's aria label
names the table it reads (`silver_neso_data_portal_tresp_building_block_definitions`); the frame caption says which
rows these are; the five pathway members each print "Rows not shown: ..." under their file. The `page:` block is
not `held`, because two of the seven tables are eligible.

- **Chart:** `type: none`, reason "The five pathway tables are held, and the two reference lists hold no measure to
  chart." A count of building blocks by unit or sector would be filler. Distil reports "no chart (spec type none)";
  no series file exists.
- **Frame:** `tresp_building_block_definitions`, the eight demand blocks for heat pumps, district heating and air
  conditioning. They cover all three demand units (`Number`, `Annual Demand (GWh)`, `Surface Area`) and all four
  suffixed ids the hold is about (`Dem_BB005_1/_2`, `Lct_BB015_1/_2`). `dedup` on `fes_bb_id_number` by
  `capture_written_at` is a guard only (one capture).
- **Notebook:** `data.sql()` on both lists' `_latest` views (all 12 demand blocks; counts by sector and unit; the
  first five GSP area names). Ran clean, 0 errors, no plot.
- **Optional, seat's call:** making `tresp_building_block_definitions` the lead in the manifest would file the
  artefacts under an eligible table and fix the notebook tab label (see Template problems). Not needed for honesty.

## What I established

1. **tRESP in NESO's words** (package `notes`, catalogue snapshot `20261006T195819Z`): "The transitional RESP (tRESP)
   is the first output from NESO's Regional Energy Strategic Plan (RESP) team", a bridge to the full RESP approach
   from 2028; DNOs use it with Ofgem's business planning guidance for ED3 (2028-33). One short-term pathway
   (2025 to 2035, `tRESP - HT`) branches into three long-term pathways (HT, EE, HE) for 2035 to 2050. 35 building
   blocks across demand and generation/storage; this package carries the 12 demand blocks.
2. **One row per member:**
   - `tresp_demand_pathways_gsp`: one value per building block, tRESP GSP area, pathway and `Year`, with the DNO
     licence area.
   - `_la_england`, `_la_scotland`, `_la_wales`: the same per local authority (`lad24cd`, ONS codes as at
     31 December 2024), "indicative" per NESO.
   - `_resp_region`: the same per RESP nation and region.
   - `tresp_building_block_definitions`: one row per building block (35: 12 Demand, 18 Generation, 5 Storage).
   - `tresp_gsp_area_names`: one row per tRESP GSP area code with its name (231).
3. **Units, NESO's dictionary** (field-info `20261008T114228Z`, snapshot `20261006T195819Z`): `Unit` is "Number or
   square metre (m2) or GWh"; `Value` is "tRESP Pathway value" ("Indicative tRESP Pathway value" for local
   authorities) with no unit of its own; `Year` is "the year against which the Pathway value has been provided for,
   with volume at 31 March". Per block: 8 `Number`, 2 `GWh` (`Dem_BB005_1`, `Lct_BB015_1`), 2 `m2`
   (`Dem_BB005_2`, `Lct_BB015_2`), matching the workbook's `Units` text.
4. **Held line, one shared line for all five** (ledger question, unit E-SEM): "NESO gives no period for annual GWh
   values, nor a FES definition for four block ids." (16 words.)
5. **Reference tables:** the building-block list (technology, detail, NESO's unit text, sector) and the GSP area code
   to name lookup, both sheets of one workbook (`11c36b60-...xlsx`) read through the `tresp_demand_pathways_files`
   sibling family.

## Evidence table

| Claim | Evidence |
|---|---|
| Row counts: GSP 160,776; England 206,016; Scotland 22,272; Wales 15,312; RESP region 7,656; blocks 35; names 231 | Polars on silver, all match the ledger row (`v0.22-FE-LEDGER.md:44`) |
| One capture per table, 0 repeated keys | `bronze_capture_id` n_unique = 1 in all seven; key duplicates 0 |
| No 16 October recapture | 106 families have a `2026/10/16` bronze partition; none of the eight tRESP resource ids appears outside `2026/10/08` |
| Every file last modified 30 January 2026; package created 28 January 2026, version 1.0 | catalogue snapshot `20261006T195819Z`: `last_modified` per resource, `metadata_created`, `version` |
| tRESP description, "first output" quote, ED3 2028-33, pathway branching | snapshot package `notes` and resource descriptions |
| Units and `Year` wording | field-info `tresp_demand_pathways_{gsp,la_england,resp_region}.json` |
| 12 blocks per family; block-to-unit pairs as above; 0 nulls; years 2025 to 2050 (HT), 2035 to 2050 (EE, HE) | Polars on the five held tables (not shown on the page) |
| GSP areas 231, LADs 296/32/22, regions 11, DNO areas 14, one DNO per GSP area | Polars, re-confirms the note body |
| Workbook children read from the files family's bronze | registry `siblings: ["tresp_demand_pathways_files"]`; `silver/neso_data_portal/generic.py:298`; `client.py:1700` (sibling-fed family fetches nothing) |
| Request URLs | bronze sidecar `request_url` (workbook); `CKAN_ACTION_PREFIX` `endpoints.py:49`; resource URLs from the snapshot |
| `child_crc32` is the sheet part's CRC-32 | `silver/neso_data_portal/casting.py:445-447`, `readers.py:608-621` |
| `child_id`, `child_crc32`, `resource_id` columns | `casting.py:153-172` (`record_dtypes`) |
| Notebook views exist and return the rows | `scripts/run_notebooks.py` output, 0 errors |

## Body corrections (canonical note)

- "Four things to know", item 3 ("One capture, one vintage"): still true, so not changed in substance; added a dated
  check that the 2026-10-16 portal recapture took no tRESP file and bronze and silver hold the 2026-10-08 capture
  alone. Evidence: the bronze listing above.
- `updated:` 2026-10-10 to 2026-10-24.
- Every other measured body claim re-checked and true (counts, distinct geographies, unit mapping, nulls, column
  counts 16/16/16/16/15/16/13, vintages and capture times).

## Unverified

- Whether NESO will re-upload to the same resource ids or add new resources for a later tRESP release (note body
  already marks it `TODO: verify`).
- The CRS inside the RESP GPKG (body `TODO: verify`, not on the page).

## Open questions

- None blocking. The seat may prefer the building-block table as the manifest lead (see above).

## Template problems

- On a family page whose frame and notebook read a non-lead table, the notebook tab says
  `tresp_demand_pathways_gsp.ipynb` and the notebook aria label says "cells on
  neso_data_portal/tresp_demand_pathways_gsp", naming the held lead (`build.py:1467`, `:1471-1473`). The frame's
  aria label is right (it uses `sample["silver"]`).
- The facts "Key" line shows the frame table's key (`fes_bb_id_number, resource_id`), not the lead's; I wrote
  `grain` to say which table the shown rows come from.
- A family page cannot list request URLs for files outside its members: the two GIS files (`tresp_gsp_areas.gpkg`,
  `resp_boundaries_202511_bfc_27700.gpkg`) are named only in `raw_feed.note` (known follow-up).
- The site has no dark theme (no `prefers-color-scheme` rule in `theme.css` or `tokens.css`), so the dark
  screenshots equal the light ones.
- At 390 the folded frame shows only `fes_bb_id_number` until unfolded (known follow-up).

## Screenshots

Static server on 9846 started with its PID recorded and stopped by that PID. Headless Chrome, `timeout 60`, 1440,
1024 and 768 full page, 390 through a 390 px iframe; light and dark (identical). Nothing clipped or overlapping: hero
chips wrap at 390, wells break long URLs, frame folds behind `…`. Files in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\tresp-dem-writer\`
(`p1440-light.png`, `p1024-light.png`, `p768-light.png`, `c390-light-0..3.png` and the dark copies).

## Files written

- Canonical note: `C:\gridflow-wt\vault-neso-dem\30-vendors\neso-data-portal\datasets\tresp-demand-pathways.md`
  (CRLF kept, 661 lines), mirrored byte for byte to
  `C:\gridflow-wt\fe-neso-dem\vault\neso_data_portal\tresp-demand-pathways.md` (`cmp` clean).
- `C:\gridflow-wt\fe-neso-dem\site\hifi\data\samples\neso_data_portal\tresp_demand_pathways_gsp.json`
- `C:\gridflow-wt\fe-neso-dem\site\hifi\data\notebooks\neso_data_portal\tresp_demand_pathways_gsp.json`
- No series file (chart `type: none`). Built page and member pointers under
  `C:\gridflow-wt\fe-neso-dem\site\hifi\data-sources\neso_data_portal\`.

## What the checker should look hardest at

- That a non-held page with a held lead is acceptable, and that the frame's source table is clear to a reader.
- The shared held line against the ledger question.
- `fes_bb_id_number` field line ("named for FES, but tRESP's own"): the four suffixed ids appear in no FES table
  (gridflow FACTS SCN-1a, exact-id comparison).

## Defects

No gridflow defect found. Vendor data quirks, kept as published (no gridflow action):

- NESO tRESP GSP area names carry typos: `SPEN_group_LAMBHILL_275kV` is named "tRESP Lamnhill Group SPEN" and
  `SHRW_IRONB_NGED` "tRESP Ironbridge Shrewsburry 132kV NGED" (workbook sheet `tRESP GSP Areas with Names`, capture
  2026-10-08). Labels only; the codes are the keys.
- The workbook's building-block column is headed "FES BB ID Number" but holds tRESP ids, four of which have no FES
  counterpart (already part of the E-SEM hold).
