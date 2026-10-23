# tRESP demand pathways: checker's review (round 1)

Page `neso_data_portal/tresp-demand-pathways`, lead `tresp_building_block_definitions`. Checked against gridflow code, local
silver and bronze (read only), the NESO catalogue snapshot `20261006T195819Z`, the ledger row and the registry.

## Verdict: REVISE (2 majors, 4 nits)

Gates: `gridflow-build --only neso_data_portal/tresp_building_block_definitions` clean; detector `[]`; no em dashes; mirror
`cmp` clean against the vault worktree; note diff against `origin/master` is the `page:` block, `updated:` and one dated
sentence (no whole-file rewrite, CRLF kept). Screenshots at 1440, 1024, 768 and a 390 px iframe (server on 9856, PID 20813,
stopped by that PID): nothing clipped or overlapping; the folded frame at 390 shows only `fes_bb_id_number` (known follow-up).
The site has no dark theme. `type: none` renders cleanly: no chart section, no empty heading, no stray `reason` text.

## Findings

1. **major** `page.record.fields.fes_bb_id_number` ("Block id, the pathway files' `building_block_id`; named for FES, but
   tRESP's own"; same claim in the note body, `tresp_building_block_definitions` section: "the column is named for FES but the
   ids are tRESP's").
   - NESO's text does not say the ids are tRESP's own. The package notes say the pathways "are structured in a similar way to
     the building block outputs from NESO's Future Energy Scenarios (FES) 2025" (snapshot `20261006T195819Z`, package `notes`).
   - The data contradicts "tRESP's own" for most of them. Joining the twelve demand ids to silver
     `fes_building_blocks_block_definitions` (`building_block_id_number`, editions 2020 to 2025) matches 8 of 12 exactly
     (everything except `Dem_BB005_1/_2`, `Lct_BB015_1/_2`). FES even defines the unsuffixed parents `Dem_BB005`
     ("I&C HP Demand", GWh) and `Lct_BB015` ("A/C I&C units"). Same figure in gridflow `K-SCN-1-FACTS.md` lines 237-247.
   - A reader takes the column note to mean the whole id column is tRESP's own, which is wrong for eight of the twelve demand ids.
   - Fix: say what was checked, for example "Block id, the pathway files' `building_block_id`; four suffixed ids match no FES id"
     (13 words, within budget), and correct the body sentence the same way.

2. **major** `page.family.members[2..6].held` (the shared line, "NESO gives no period for annual GWh values, nor a FES
   definition for four block ids.").
   - Part one is faithful: the ledger question and the registry `eligibility.question` ask for the interval an annual GWh
     `Year` label covers, and NESO's dictionary dates volumes at 31 March without an interval.
   - Part two misstates the second question. The ledger says "which FES definition applies to the suffixed ids (no exact FES
     building-block id)". The finding is that no FES id matches those four, which is gridflow's exact-id comparison, not NESO
     silence. NESO does define all four ids, in the table on this very page (the frame shows `Dem_BB005_1`, `Dem_BB005_2`,
     `Lct_BB015_1`, `Lct_BB015_2` with technology, detail and unit). "NESO gives no ... FES definition for four block ids" invites
     the question "what are those four ids?", and the frame directly above contradicts a plain reading of "gives no definition".
   - The page also never says the whole file is held, not just the GWh rows and four ids. The registry holds each family whole
     (registry `families[*].record.eligibility.status: held`; note body "the eight `Number` blocks are not published separately
     either").
   - Fix, 16 words: "NESO states no period for annual GWh values, and four block ids match no FES id." Whether to add "so
     the file stays whole-held" is the seat's call; it does not fit the budget.

3. **nit** `page.what_it_is`, `page.record.fields.fes_bb_id_number`, every `held:`: "FES" is never expanded anywhere on the
   page (0 occurrences of "Future Energy"). GSP, DNO and ED3 are not expanded either. tRESP and RESP are. One expansion of
   FES (the column note is the natural place) would make the held line readable cold.

4. **nit** `page.record.fields.demand_generation_storage` ("NESO's 35 blocks cover both tRESP packages"): the page never
   mentions the generation pathways package, so "both packages" has no referent. Say "demand, generation and storage" instead
   (the notebook output already prints the three groups: Generation 18, Storage 5, Demand 12 split by unit).

5. **nit** `page.how_used[0]` ("DNOs develop their ED3 plans, 2028 to 2033, with it ..."): NESO writes "will use" in a January 2026
   release. Present-tense use is not evidenced. "NESO says DNOs will use it ..." is accurate and the "(NESO)" tag is already there.

6. **nit** `page.facts.cadence` ("every file last modified 30 January 2026"): true of the catalogue snapshot of 6 October 2026
   (`last_modified` on all eight resources), but undated, so it reads as a standing fact. "as at 6 October 2026" would date it.
   Low priority.

## What I checked and found correct

- **Frame.** Reproduced from silver (`neso_data_portal/tresp_building_block_definitions`, 35 rows, 16 columns, one capture, 0 key
  duplicates, nulls only in `technology_detail` on 7 generation rows). The eight rows are the four heat pump blocks
  (`Dem_BB005_1/_2`, `Lct_BB005`, `Lct_BB006`), one district heating (`Lct_BB009`) and three air conditioning (`Lct_BB014`,
  `Lct_BB015_1/_2`) blocks. They cover all three demand units (`Number`, `Annual Demand (GWh)`, `Surface Area`) and all four
  suffixed ids; the four left out are the electric vehicle blocks (`Number`). Order matches `order_by` (technology, then id).
  The unfolded frame values (`child_crc32` 2238457871, `published_at` 2026-01-30 08:15:29.726307 UTC, `timestamp_utc`
  2026-10-08 11:39:46.157281 UTC, the bronze path) match silver. The sample is `generated_by: gridflow-sample`.
- **Notebook.** `scripts/run_notebooks.py` JSON, 5 cells, no error outputs, tab `tresp_building_block_definitions.ipynb`, aria label
  names the lead. Outputs agree with silver: 12 demand blocks; counts Generation 18, Storage 5, Demand Number 8, Annual
  Demand (GWh) 2, Surface Area 2; the first five area names. All cells read only (`data.sql`). The lead sentence is right:
  `query()` filters on `timestamp_utc`, which is the capture time for a table with no event time.
- **tRESP in NESO's words.** "the first output from NESO's Regional Energy Strategic Plan (RESP) team" is an 11-word quote
  from the package notes. 12 demand building blocks, one short-term pathway to 2035 branching to three to 2050, DNOs and ED3
  2028-33: all in the snapshot notes.
- **What one row is.** Building-block table: one row per block (35; Demand 12, Generation 18, Storage 5). GSP area names: one
  row per area code (231, all distinct). Pathway members: one value per block, area, pathway and year, with the key from the
  registry entity keys. Local-authority rows are "indicative" per NESO's resource descriptions. ONS codes "at 31 December 2024"
  is carried from the body (the `LAD24CD` column); I did not re-derive that date.
- **Units.** Block to unit pairs on silver (all three pathway tables I read: GSP, England, RESP region): 8 `Number`, 2 `GWh`
  (`Dem_BB005_1`, `Lct_BB015_1`), 2 `m2` (`Dem_BB005_2`, `Lct_BB015_2`). The `units` field line is true and uses NESO's
  dictionary wording.
- **Captures.** One capture per table, all `2026/10/08` (bronze listing and `n_unique(bronze_capture_id) = 1` in all seven
  silver tables). Row counts match the ledger and the registry-era figures: 160,776; 206,016; 22,272; 15,312; 7,656; 35; 231.
  No tRESP capture on 16 October: 106 families have a `2026/10/16` bronze folder, none contains a sidecar naming any of the
  eight tRESP resource ids (grep of `*.meta.json`), and the seven tRESP families have only `2026/10/08`. The dated note-body
  sentence ("Checked 2026-10-24 ...") is therefore true and is the only body change besides `updated:`.
- **Raw feed.** Request URLs equal the bronze sidecar `request_url` values; `package_show` is `CKAN_ACTION_PREFIX` plus
  `?id=tresp-demand-pathways`. The note's "each file whole unless its `last_modified` is unchanged" matches
  `client.py:1752-1769`; the sibling-fed families fetch nothing (`client.py:1700`). Commands follow the established NESO
  pattern (`--last 24h`, "the capture's date to silver").
- **NESO's area-name typos kept as published.** `SPEN_group_LAMBHILL_275kV` is "tRESP Lamnhill Group SPEN" and `SHRW_IRONB_NGED` is
  "tRESP Ironbridge Shrewsburry 132kV NGED" in silver, unaltered. Neither appears on the page, in the notebook output or in the
  note body (they sit only in the writer's Defects list), so nothing is mis-corrected.
- **Related.** Both slugs exist in the page set and the build resolves them. The notes are under 12 words and say how the pages
  relate. The "draws its own GSP areas" note matches NESO's GIS resource description ("tRESP GSP areas define the
  interpretation for the tRESP outputs").
- **Member pointers.** Seven member pages link to `tresp-demand-pathways.html#<member>` and all seven anchors exist.
- **Public copy.** No em dashes, no "held" or planning words, no local counts on the page. Facts line "NESO created the package,
  version 1.0, on 28 January 2026" matches `metadata_created` and `version` in the snapshot. `published_at` "read as UTC"
  matches `_bronze.py:192-206` (CKAN's naive stamp is read as UTC, corroborated but not a vendor contract).

## Defects for the log

No gridflow defect. The two NESO typos above are vendor labels (codes are the keys). One documentation defect for the vault:
the body sentence in finding 1 ("the ids are tRESP's") is wrong for eight of twelve demand ids.
