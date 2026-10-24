# tRESP generation pathways: writer's report (round 1)

Page `neso_data_portal/tresp-generation-pathways`, a family page. The lead is `tresp_generation_pathways_resp_region`,
then `_gsp`, `_la_england`, `_la_scotland` and `_la_wales`. All five are eligible and none is held. The build
`--only neso_data_portal/tresp_generation_pathways_resp_region` ran with no errors. Detector `[]`. No em dashes on the
page. Mirror `cmp` clean (CRLF, 561 lines). The manifest's lead and member list are right.

## What I established

1. **What one row is.** In each member, one row is the installed MW for one building block, one area, one pathway and
   one year, with `unit` = `MW`. The geography columns differ by member:
   - `resp_region` (RESP nation or region, 11 values) in the lead.
   - `tresp_gsp_area` plus `dno_licence_area` in `_gsp` (231 areas).
   - `lad24cd` and `lad24nm` (ONS codes and names as at 31 December 2024, per NESO's dictionary) in the three local
     authority members (296, 32 and 22 codes).

   Sources: the gridflow registry `connectors/neso_data_portal/registry/tresp-generation-pathways.json` (headers,
   dtypes, entity key `resource_id` + block + area + pathway + `projection_year`, `latest: whole_capture`,
   `temporal: none`, `vintage: ckan_last_modified`); NESO's field info (`20261008T114228Z`), where `Unit` is
   "Capacity installed (MW)", `Value` is "tRESP Pathway value" ("Indicative tRESP Pathway value" for local
   authorities), and `Year` is "the year against which the Pathway value has been provided for, with volume at
   31 March". Pathway text, NESO's words: a single Short-Term Pathway 2025 to 2035 (`tRESP - HT`) branches into three
   Long-Term Pathways (HT, EE, HE) for 2035 to 2050.
2. **How the five geographies relate** (Polars on silver, capture 2026-10-08, checked 2026-10-24, all 1,334 block,
   pathway and year groups):
   - The GSP rows sum to the RESP-region total to within 7.3e-12 MW. They are two cuts of one total.
   - England, Scotland and Wales local authorities together sum to that same total to within 0.00034 MW.
   - Within a nation they do not match. Scottish local authorities differ from the `Scotland` region by up to
     44.9 MW, and Welsh ones from `Wales` by up to 60.0 MW. This fits NESO's resource text: local authority values
     are indicative because "the Pathways are defined at the larger tRESP GSP area, and DNOs will disaggregate within
     those areas".
   - NESO's package text says the regions and local authorities cover "Great Britain".
   - Each GSP area carries exactly one DNO licence area.
3. **Building-block ids.** There are 23 ids, the same set in all five members (`Gen_BB001` to `Gen_BB013`,
   `Gen_BB015`, `_016`, `_018`, `_019`, `_023`, and `Srg_BB001` to `_005`). This matches NESO's "23 tRESP generation
   building blocks".
   - **Demand page's block table:** all 23 are in `tresp_building_block_definitions` (its 18 Generation and 5 Storage
     rows). That table gives every one of them the unit "Capacity Installed (MW)". None of the four suffixed demand ids
     occurs here.
   - **FES:** all 23 match an id in silver `fes_building_blocks_block_definitions`, in every edition from the 2024
     resource on. The 2020 sheet lacks `Gen_BB023`. So the demand page's FES caveat does not apply to these tables.
     Matching ids do not prove matching definitions; the note keeps that TODO.
4. **Times.** There is no event time: `temporal: none`, and `timestamp_utc` = `event_time` = capture time
   (2026-10-08 11:40 UTC, one value per table). `published_at` = `available_at` = CKAN `last_modified` (30 January
   2026, 08:27 to 08:37 UTC). The year column is a 31 March snapshot per NESO's dictionary (quoted above). So the
   notebook uses `data.sql()` on the `_latest` views. 2035 holds identical values under all three pathways (max
   difference 0.0), as NESO's branching describes.
5. **Captures, row counts and repeats.** Each table has one bronze capture (`2026/10/08`), one silver file, one
   `bronze_capture_id`, 0 repeated entity keys and 0 nulls. Counts: RESP region 14,674; GSP 308,154; England 394,864;
   Scotland 42,688; Wales 29,348. These match the ledger row (`v0.22-FE-LEDGER.md:45`) and the note. No member has a
   2026-10-16 partition. `dedup:` on the full entity key, ordered by `capture_written_at`, is set on both the chart and
   the frame as a guard (`duplicates_dropped: 0`).
6. **Chart.** It is a `bar` chart. `projection_year` is an `Int64`; `distil.py` needs a temporal column for a time
   axis, and `time_text` parses strings only. So the bars are years, every fifth year 2025 to 2050. The values are
   block `Gen_BB012` (large solar, 10 kW and over), pathway `tRESP - HT`, summed over the RESP regions, in MW
   installed at 31 March: 12,778 / 28,738 / 44,345 / 55,089 / 60,905 / 64,451 (series file, 66 rows used). It is
   summed over regions within one block, which is additive. Vehicle-to-grid, the only negative block, is avoided.
   The notebook plots all three pathways across 2025 to 2050 to complement it.
7. **Frame.** Eight South West `Gen_BB012` rows for 2025, 2034, 2035 (three pathways, equal values) and 2036 (three
   pathways, diverging). This shows the branch.

## Evidence table

| Claim | Evidence |
|---|---|
| Row counts 14,674 / 308,154 / 394,864 / 42,688 / 29,348; one capture each; 0 key repeats; 0 nulls | Polars on silver (`s1.py`); bronze listing shows only `2026/10/08` per member |
| Rows per pathway (HT/EE/HE) as in the note's table | Polars group_by pathway (`s6.py`) |
| `unit` = `MW` on every row; NESO's unit "Capacity installed (MW)" | silver unique; field info `tresp_generation_pathways_*.json` |
| `Year` = volume at 31 March | field info, `Year` description |
| `timestamp_utc` = capture time, no event time | registry `temporal: {kind: none}`; silver single value = `capture_written_at` |
| `published_at` = CKAN `last_modified` 2026-01-30 | silver; catalogue snapshot `20261006T195819Z` resource `last_modified` |
| Package created 28 January 2026, version 1.0, ad hoc | snapshot `metadata_created`, `version`, extras "Update frequency: Ad-hoc" |
| "first output" quote; DNOs will use it for ED3, 2028-33; 23 generation blocks; "across Great Britain" | snapshot package `notes` |
| "Indicative" explanation | snapshot resource descriptions (three local authority files) |
| GSP sum = region sum (7.3e-12 MW); local authority sum = region sum (0.00034 MW); Scotland 44.9 MW, Wales 60.0 MW apart | Polars (`s2.py`), 1,334 groups |
| 2035 equal across pathways | Polars pivot, max difference 0.0 |
| One DNO licence area per GSP area | Polars n_unique per area, max 1 |
| 23 ids in tRESP definitions, all MW; all 23 in FES definitions from 2024 on, 2020 lacks `Gen_BB023` | Polars (`s3.py`, `s4.py`) |
| Negatives only in `Srg_BB005`; never positive (GSP has 118 zeros); minimum -8,424.3 MW (RESP region) | Polars (`s6.py`) |
| Request URLs | bronze sidecar `request_url` (five); `CKAN_ACTION_PREFIX` `endpoints.py:49`; `client.py:1705` (`package_show` per family) |
| Commands | `cli.py:187-200` (ingest), `:262-268` (transform), `:485-491` (pipeline: one window for ingest then transform); the build allows 1 to 3 commands |
| Notebook outputs | `run_notebooks.py`: 5 cells, 0 errors, 1 image. HT 2033 37,671.8 and 2034 41,008.4; 2035 44,345.0 for all three; GSP = region for 2050 in all three pathways (56,903.5 / 64,451.1 / 56,546.1) |

## Body corrections (canonical note)

- `updated:` 2026-10-10 changed to 2026-10-24.
- GSP section: the TODO "whether each area maps to exactly one DNO licence area" is replaced by the dated measured
  answer (yes in the 2026-10-08 capture; no NESO rule).
- England local authority section: the TODO on what "indicative" means is replaced by NESO's own explanation, quoted
  from the resource description (catalogue snapshot `20261006T195819Z`).
- "Cross-geography consistency": the TODO is replaced by NESO's "across Great Britain" text and the dated
  measurements in point 2 above. Advice: regions and GSP areas are two cuts of one total; do not roll local
  authorities up to a nation.
- Cadence: added a dated check that the 2026-10-16 recapture took no tRESP generation file.
- Every other measured body claim was re-checked and is true: zero counts, negative counts, minimum values, distinct
  areas, the FES comparison and the rows per pathway.

## Unverified

- The sign convention of `Srg_BB005` (vehicle-to-grid), negative throughout. The page says NESO does not explain it.
- Whether matching block ids mean matching FES definitions (note TODO kept).
- Whether NESO will overwrite these resources or add new ones for a later tRESP release (note TODO kept).
- Whether a zero means "zero capacity" or "not modelled" (note TODO kept; not on the page).

## Open questions

- None blocking.

## Template problems

- An integer year column cannot drive a time axis. `time_text` calls `.str.to_datetime` and fails on an `Int64`, and
  `distil.py:312` rejects a non-temporal time column. So a pathway-by-year line chart (three series) is impossible.
  I used a single-series bar chart of one pathway and kept the three-pathway view in the notebook plot. A follow-up
  could let `time_text` (or a `time_year` option) read an integer year as 1 January, or as 31 March here.
- A bar chart has one series, so pathways cannot sit side by side.
- `raw_feed.commands` allows at most three entries. To cover the two tables the notebook reads, the GSP table uses one
  `gridflow pipeline` line rather than separate ingest and transform lines.
- At 390 the folded frame shows only `building_block_id` and `resp_region` before the fold (known follow-up).
- The site has no dark theme, so I took light screenshots only.

## Screenshots

I started a static server on 9805 with `python -m http.server ... & echo $!` (PID 34890) and stopped it by that PID.
Headless Chrome, `timeout 60`, at 1440, 1024 and 768 full page, and 390 through a 390 px iframe. Nothing is clipped
or overlapping: the hero chips wrap at 390, the wells break long URLs, the bar labels and values are all visible, and
the frame folds behind `…`. Files are in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\tresp-gen-writer\`
(`p1440-0..3.png`, `p1024-0..3.png`, `p768-0..3.png`, `c390-0..5.png`).

## Files written

- Canonical note: `C:\gridflow-wt\vault-neso-gen\30-vendors\neso-data-portal\datasets\tresp-generation-pathways.md`
  (CRLF kept). Mirrored byte for byte to
  `C:\gridflow-wt\fe-neso-gen\vault\neso_data_portal\tresp-generation-pathways.md`.
- `C:\gridflow-wt\fe-neso-gen\site\hifi\data\series\neso_data_portal\tresp_generation_pathways_resp_region.json`
- `C:\gridflow-wt\fe-neso-gen\site\hifi\data\samples\neso_data_portal\tresp_generation_pathways_resp_region.json`
- `C:\gridflow-wt\fe-neso-gen\site\hifi\data\notebooks\neso_data_portal\tresp_generation_pathways_resp_region.json`
  and `...-4.png`
- Built page (gitignored): `site\hifi\data-sources\neso_data_portal\tresp-generation-pathways.html`, plus the five
  member pointers to `#<member>`.

## What the checker should look hardest at

- `record.fields.building_block_id` ("all 23 match a ... FES block id") and `value` ("negative in these files"). Both
  are scoped measurements; confirm the wording is acceptable.
- The chart caption's "summed over every RESP nation and region", and the decision not to state the count 11 on the
  page.
- The `gridflow pipeline` command line for the GSP table.

## Defects

No gridflow defect found. Vendor data points, kept as published (no gridflow action):

- `Srg_BB005` (vehicle-to-grid) is zero or negative on every row of all five files, under a unit NESO calls
  "Capacity installed (MW)". NESO gives no sign convention (capture 2026-10-08).
- Within a nation, the indicative local authority files do not sum to the RESP nation (Scotland up to 44.9 MW, Wales
  up to 60.0 MW apart), although all cuts agree at the GB total. This is consistent with NESO's stated method; it is
  recorded so nobody rolls local authorities up to a RESP nation.

## Round 2 (checker's review: REVISE, 1 major, 4 nits; all fixed)

1. **Major, `page.raw_feed.note`:** it now reads "one `package_show`, then the table's file downloaded whole, unless its
   `last_modified` is unchanged. Dates select nothing; silver keeps every capture." This follows the approved
   `demand-flexibility` note: each family ingest fetches only its own file.
2. **Nit, chart words:** the title is now "Large solar capacity projected, tRESP Holistic Transition, 2025 to 2050"
   (10 words). The caption says "projected MW installed at 31 March", and the chart alt and `notebook.plot_alt` say
   "projected". The spec is unchanged, so the series digest still passes.
3. **Nit, `record.fields.projection_year`:** now "Year the value is for: MW installed at 31 March, per NESO".
4. **Nit, `record.fields.value` and `building_block_id`:**
   - `value`: "MW; vehicle-to-grid (`Srg_BB005`) is zero or negative, no sign stated; FES: \"MW availability\"".
   - `building_block_id`: "Block id; all 23 match a Future Energy Scenarios (FES) id; definitions not compared".
   - I re-checked the FES unit: silver `fes_building_blocks_block_definitions` gives `Srg_BB005` "MW availability" in
     the 2024 to 2026 resources and "MW" in the 2020 one.
   - The note body's negative-values paragraph now says the block is zero or negative (118 GSP zeros) and records the
     FES unit, dated 2026-10-24.
5. **Nit, note body "Cross-geography consistency":** it now adds that the English file differs from the nine English
   regions by up to 72.2 MW, and that the three differences net out at the total. I reproduced this: `Srg_BB005`, HT,
   2050, 72.23 MW. The older TODO on whether the 11 regions tile Great Britain is reworded to geometry only, with
   double counting ruled out by the cuts agreeing at the total.

**Gates:**
- `gridflow-build --only neso_data_portal/tresp_generation_pathways_resp_region`: no errors.
- Detector `[]`; 0 em dashes.
- Mirror `cmp` clean (CRLF, 567 lines, 0 bare LF).
- No artefacts regenerated: the chart spec, record select and notebook cells are unchanged, and the build's digest
  checks pass.
- I took no new screenshots. Only prose changed, and the new title is the same length class as the round-1 title,
  which wrapped cleanly at 390.

**Defects:** unchanged; no gridflow defect. Vendor observation added: NESO calls `Srg_BB005` "Capacity installed (MW)"
in tRESP but "MW availability" in the FES 2021 to 2025 definitions, and publishes it zero or negative in both.
