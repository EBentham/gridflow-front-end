# FES building block data: writer's report (round 1)

Page `neso_data_portal/future-energy-scenario-fes-building-block-data`, a family page. The page set's lead is
`fes_building_blocks_main`. Build `--only neso_data_portal/fes_building_blocks_main`: no errors. Detector `[]`. No em
dashes in the page. The mirror is identical (`cmp`). The note keeps CRLF on all 840 lines. The vault diff is the
`page:` block, `updated:` and three short body additions (155 lines added, 3 removed).

## The decision: the main table is held, so nothing on the page comes from it

The launch prompt asked for a chart of the main table. The registry and the ledger both hold it whole:
- registry `future-energy-scenario-fes-building-block-data.json`, `fes_building_blocks_main.record.eligibility.status: held`, unit E-SEM;
- ledger row 48, "Held: `fes_building_blocks_main` (E-SEM: year-label period, omitted row grain)";
- rulings 608 and 623;
- the note's Holds section: "nothing published from this family".

So I charted no projection, showed no value, range or row from it, and the notebook never reads it. The page
follows the approved tRESP demand pathways pattern, which has the same shape (a held pathway lead and an eligible
building-block definitions table):
- `chart.silver` and `record.select.silver` point at `fes_building_blocks_block_definitions`;
- the notebook uses `data.sql()` on the two reference tables;
- the main member prints "Rows not shown: ...".

The page is not `held`, because two of the three tables are eligible.

**Lead recommendation:** make `fes_building_blocks_block_definitions` the lead in `neso_data_portal.json`, then
`_block_licence_area`, then `_main`. That files the artefacts under an eligible table and fixes the notebook tab,
which reads `fes_building_blocks_main.ipynb`. The seat made the same reorder for tRESP and Phase 2 FFR. The explicit
`silver:` keys already name the definitions table, so after a reorder only `page.family.members` needs reordering.

Hard rules 1 and 2 (FES projections never charted as history; read main lazily) are met by construction: the chart
counts definitions rows, and main was only scanned lazily for structure (counts, distinct ids, key uniqueness). It
was never collected and no value was read.

## Chart and how it was reproduced

- **What it shows:** a bar chart of definitions rows per FES edition, `group: edition` mapped to "FES 2020" ... "FES
  2025", `aggregation: count`, `sort: label`, unit "building blocks".
- **Duplicates:** `dedup` on `[resource_id, building_block_id_number]` by `capture_written_at` is a guard only. There
  is one capture per resource, so 0 duplicates were dropped (series provenance `duplicates_dropped: 0`).
- **Series:** 49, 64, 66, 66, 66, 66 (`site/hifi/data/series/neso_data_portal/fes_building_blocks_main.json`, 377
  rows used, `spec_origin: vault`).
- **Reproduce:**
  `pl.read_parquet(".../fes_building_blocks_block_definitions/**/*.parquet").group_by("edition").len()` gives the same
  six counts. Notebook cell 3 prints them too.
- **Why this chart:** hard rule 3. Block ids mean what the same edition's definitions say, and they do change. The
  chart and caption carry that ("An id can change meaning between editions, so read each with its own edition"). The
  frame shows it, and notebook cell 4 lists the 12 ids from 2020 that are missing in 2021.
- **Dating:** the key note dates the bars to NESO's files. Each bar is one file, and the 2021, 2022 and 2023 files
  carry a September 2026 `last_modified` (catalogue snapshot `20261006T195819Z`; capture sidecars).
- **Alternative:** if the checker judges a count chart filler, `type: none` with a reason is the tRESP precedent. I
  kept the bar because the 49 to 64 to 66 step is the visible reason to join on edition.

## Captures and editions (every capture checked)

| Table | Resources | Captures | Rows | `dedup` |
|---|---|---|---|---|
| `fes_building_blocks_main` | 6 (2020 to 2025) | one each, 2026-10-08; 2020 to 2022 fail `DuplicateEntityKeyError` (adjudicated, bronze only) | 2023 1,341,482; 2024 1,582,756; 2025 1,296,513 (lazy count, matches ledger) | not used (held) |
| `_block_definitions` | 6 (2020 to 2025) | one each, 2026-10-08 (`bronze_capture_id` n_unique 1 per edition) | 49 / 64 / 66 / 66 / 66 / 66 = 377 | guard on chart and frame |
| `_block_licence_area` | 1 (2024) | one, 2026-10-08 | 19 | n/a (notebook only) |

- No resource of this package appears in any later bronze partition. Only `2026/10/08` exists under all three
  families, although 106 families have a `2026/10/16` folder.
- Key uniqueness was 0 duplicate tuples on definitions and on main (lazy `group_by(entity_key)`).
- Every main block id has a same-edition definition (anti-join, 0 missing).

## What one row is

- **`fes_building_blocks_main`:**
  - One projected `value`, in the row's own `unit` (`MW`, `GWh` or `Number`), for one building block, DNO licence
    area, GSP, FES scenario (2023, in `fes_scenario`) or pathway (2024 and 2025, in `fes_pathway`), and
    `projection_year` label, in one edition's file.
  - It is the vendor's wide year columns unpivoted (ADR-042). `timestamp_utc` is the capture time. The vintage is CKAN
    `last_modified` (`available_at`).
  - Held.
- **`fes_building_blocks_block_definitions`:**
  - One building block in one edition: template, technology, technology detail, NESO's unit text, detail and comments.
  - Later layouts add the Ofgem alignment column, ESO comments and the `Included in ESO Data` flag.
  - Key: `resource_id, edition, building_block_id_number`.
- **`fes_building_blocks_block_licence_area`:**
  - One area name used in the FES 2023 building-block files (`fes23_bb_area_name`), with its full licence name, its
    Elexon GSP group and name, and its FES 2024 area name.
  - 19 rows: 14 DNO, 3 TO, 1 IDNO, 1 Not Connected.

## Evidence table

| Claim | Evidence |
|---|---|
| Main held whole (E-SEM: year-label period; 2020 to 2022 omitted grain) | registry `eligibility`; ledger row 48; note Holds |
| Held line "NESO states no period for the year labels; 2020 to 2022 repeat rows with different values." (16 words) | registry question, both parts; note: "repeat building block x GSP x DNO x unit with different values" |
| Blocks per edition 49/64/66/66/66/66 | committed series; notebook cell 3 output |
| `Lct_BB001` to `Lct_BB004` same ids, vans moved in 2021 | sample rows (`technology_detail`: "cars & motorbikes" becomes "vans, cars & motorbikes"; "other than cars and motorbikes" becomes "other than vans, cars and motorbikes"); `comments` the same |
| 12 ids from 2020 missing in 2021; 2021 adds 27 | Polars set difference; notebook cell 4 lists the 12 |
| 2025 `Technology` = `Offshore-Wind (off-Grid)` on all 12 demand rows | silver; bronze `raw_20261008T105310Z_cc3118da-...csv` lines 26 to 37; the 2024 file is blank there |
| `Included in ESO Data` Y/N only in 2022 and 2023 | silver null counts by edition (66 nonnull in 2022 and 2023, 0 elsewhere) |
| `eso_additional_notes` only in 2020; `eso_comments` 2021 to 2023; alignment from 2021 | silver non-null counts; schema epochs in the note |
| `unnamed_8` and `unnamed_10` empty, 2022 file | note body (blank in all 66 rows); silver null on all 377 |
| 2024 `template` mostly blank | silver: 62 of 66 null |
| `edition` from the file name | registry `edition_by_filename` |
| `published_at` = CKAN `last_modified` read as UTC | registry `vintage`; sidecar `ckan_last_modified`; silver tz UTC |
| Request URLs | each equals a bronze sidecar `request_url` (script check); `package_show` from `endpoints.py:49` |
| Downloads skipped when `last_modified` is unchanged | `client.py:1752-1765` |
| `--last 24h`; the window is not a selector | `client.py:1583-1589`; approved NESO note precedent |
| `query()` filters on the capture time, so `data.sql()` | batch "Checked facts" (remediation 20at) |
| NESO quote, "not for building regional pathways", ENA Open Networks | package `notes`, snapshot `20261006T195819Z` |
| Package created 13 August 2020 | snapshot `metadata_created` 2020-08-13 |
| tRESP "structured like FES 2025 building blocks" | tRESP package notes, quoted in the tRESP review |
| Notebook ran clean | `run_notebooks.py`: 5 cells, 0 errors, 0 images |

## Body corrections (canonical note)

- `updated:` changed from 2026-10-10 to 2026-10-24.
- **"Building-block ids":** added that ids are not stable across editions. `Lct_BB001` to `Lct_BB004` move vans in
  2021, and 12 ids from 2020 (including `Srg_BB006` to `Srg_BB011` and the four unprefixed ids) are absent from 2021,
  which adds 27. Evidence: Polars set difference, dated to the 2026-10-08 captures.
- **"Join to the main table":** added that `Included in ESO Data` is `Y` on exactly the 50 ids the main files use and
  `N` on the 16 others, in the 2022 and 2023 definitions. This is measured; NESO does not define the flag.
- **New short paragraph, "`Technology` in 2025":** the 2025 fill-down, citing the bronze file lines.
- Every other body claim I re-checked is true:
  - main and definitions row counts, captures and `published_at`;
  - blocks, GSPs and DNO areas per edition (50/376/19, 50/378/19, 50/378/18);
  - year ranges and units per edition, and the scenario and pathway names;
  - 2024 null counts (`template` 62, `technology` 38);
  - the licence-area table.

## Unverified

- What `Included in ESO Data` and the Ofgem alignment column mean. The page says NESO does not define the flag.
- Whether NESO will correct the 2025 `Technology` cells.

## Template problems (seat items)

- The notebook tab and aria label name the held lead (`fes_building_blocks_main.ipynb`). This is fixed by the lead
  reorder.
- A family member may list at most four requests, but main and definitions have six files each. Both show the first
  and latest file (definitions also shows 2021, the frame's edition), and `raw_feed.note` says so.
- `raw_feed.commands` allows at most three lines, so the mapping is covered by "swap in either key" (the approved
  transmission-losses precedent).
- At 768 and 390 the folded frame shows only `building_block_id_number` and `edition` until it is unfolded, which
  hides `technology_detail`, the column the caption is about. This is the known fold follow-up.
- The site has no dark theme. The dark screenshot differs only where the turbines rotate.

## Screenshots

- Static server on 9942, started with its PID recorded (57113) and stopped by that PID.
- Headless Chrome, `timeout 60`, at 1440, 1024 and 768 full page, and 390 through a 390 px iframe.
- Nothing is clipped or overlapping: hero chips wrap, wells break long URLs, the bar labels and key note fit.
- Files are in
  `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\fesbb-writer\`
  (`p1440-*.png`, `p1024-all.png`, `p768-all.png`, `c390-g*.png`, `p1440-dark.png`).

## Files written

- Canonical note:
  `C:\gridflow-wt\vault-neso-fes\30-vendors\neso-data-portal\datasets\future-energy-scenario-fes-building-block-data.md`.
- Mirror: `C:\gridflow-wt\fe-neso-fes\vault\neso_data_portal\future-energy-scenario-fes-building-block-data.md`.
- Artefacts: `C:\gridflow-wt\fe-neso-fes\site\hifi\data\{series,samples,notebooks}\neso_data_portal\fes_building_blocks_main.json`.
- Built page: `C:\gridflow-wt\fe-neso-fes\site\hifi\data-sources\neso_data_portal\future-energy-scenario-fes-building-block-data.html`.

## What the checker should look at hardest

1. Whether the page leaks anything from the held main table. It should not:
   - main's `differs` line names its dimensions only;
   - the "50 ids" fact is in the note body only, not on the page;
   - no value, range or row from main appears anywhere.
2. The held line against both parts of the registry question.
3. The frame caption "vans moved in 2021" against the eight rows and their `comments`.
4. Whether the count bar earns its place, or `type: none` is better (the tRESP precedent).
5. The `technology` column line (the 2025 fill-down) against bronze.

## Defects (pasteable)

- **NESO FES building-block definitions 2025: `Technology` filled down onto demand rows.**
  - Where: resource `cc3118da-cbbe-49e8-a8ee-9bdd89a8bf9c` (`fes2025_bb2_v001.csv`, last modified
    2025-07-14T04:48:17Z).
  - What: all 12 `Dem_` rows carry `Technology` = `Offshore-Wind (off-Grid)`, the value of the `Gen_BB024` row above
    them. The 2024 file leaves those cells blank, and `technology_detail` (for example "Residential HP Demand") gives
    the real meaning.
  - Effect: gridflow keeps the cells as published, so `technology` is not a reliable label for 2025 demand blocks.
  - Action: vendor quirk, no gridflow change. The vault note and the page column guide state it.
- **Page set: the building-block family's lead is a held table.**
  - `site/hifi/data/neso_data_portal.json` family `future-energy-scenario-fes-building-block-data` leads with
    `fes_building_blocks_main` (held, E-SEM).
  - Proposed order: `fes_building_blocks_block_definitions`, `fes_building_blocks_block_licence_area`,
    `fes_building_blocks_main`.
- No gridflow code defect found.

## Lead change (seat reorder, commit 6c47d2c on `feat/neso-dp-fes`)

The page set now leads with `fes_building_blocks_block_definitions`, then `_block_licence_area`, then `_main`. This
supersedes the artefact paths and lead-key notes above.

- **Note:** `page.family.members` reordered to match. The `package_show` request moved from main to the new lead, so
  definitions lists `package_show` plus its 2020, 2021 and 2025 files (four requests) and main lists its 2020 and
  2025 files. No page words changed: the explicit `chart.silver` and `record.select.silver` already named the
  definitions table. CRLF is kept (840 of 840 lines), and the mirror is identical (`cmp`).
- **Artefacts regenerated under the new key:** `site/hifi/data/{series,samples,notebooks}/neso_data_portal/fes_building_blocks_block_definitions.json`.
  - The series is the same: 49/64/66/66/66/66, 377 rows, 0 duplicates dropped.
  - The sample has the same eight rows (the `Lct_BB001` to `_004` blocks in 2020 and 2021).
  - The notebook reran with 5 cells, 0 errors and the same outputs.
- **Old artefacts deleted:** the three untracked `fes_building_blocks_main.json` files under series, samples and
  notebooks, each by exact path.
- **Build:** `--only neso_data_portal/fes_building_blocks_block_definitions` has no errors. Detector `[]`, 0 em dashes.
- **Notebook tab:** it now reads `fes_building_blocks_block_definitions.ipynb`, and the aria label says "cells on
  neso_data_portal/fes_building_blocks_block_definitions". The template problem listed above is resolved.
- **Column guide:** re-checked against the definitions table, which is now the lead. Every non-pipeline column in
  the sample has a line, and no line names a column outside it.
- **Count bar:** kept, per the seat.
- **Main member:** still prints "Rows not shown: ..." with the same held line.

## Fixes after review round 1 (APPROVE, 5 nits)

1. **`record.fields.technology`:** now reads "NESO's text; 2025 file (modified 14 July 2025) fills `Dem_` rows with
   `Offshore-Wind (off-Grid)`" (14 words). It names the file by its `last_modified` (2025-07-14T04:48:17Z) and scopes
   the fill-down to the `Dem_` rows.
2. **`record.fields.alignment_with_ofgem_core_scenario_key_drivers`:** now reads "NESO's matching Ofgem driver; 13
   blocks filled 2021 to 2024, every block in 2025". The counts are silver non-null counts: 13 in each of 2021 to
   2024, 66 in 2025.
3. **`notebook.cells[1]`:** the dropped-ids cell now selects `building_block_id_number, technology` only. The longest
   cell is "Hydrogen fuelled generation", so nothing truncates. The notebook reran with 5 cells, 0 errors and no "..."
   in that output.
4. **`chart_view.caption`:** now reads "Silver `fes_building_blocks_block_definitions`: block ids in each edition's
   definitions file, not projections; NESO's 2022 and 2023 files flag 50 of the 66 as included in ESO data. An id can
   change meaning between editions, so read each with its own edition." It is exactly 40 words; "one member of this
   family" was dropped, since the table is now the lead. No re-distil was needed (the words live in `chart_view`).
5. **`facts.vendor`:** now reads "NESO Data Portal: 13 CSVs, six editions of two tables, one 2024 mapping".
   - `raw_feed.note` repeated "one per table and edition", so I removed it there too: "... then 13 CSVs, each
     downloaded whole unless its `last_modified` is unchanged. Shown: first and latest, plus the 2021 definitions."
   - On the optional point, `how_used[0]` now reads "Check how FES aligns with DNOs' own regional scenarios, NESO's
     stated purpose", closer to NESO's "clarity ... on alignment of FES and DFES".

Gates: the build `--only neso_data_portal/fes_building_blocks_block_definitions` has no errors. Detector `[]`, 0 em
dashes. The note keeps CRLF (840 of 840 lines), and the mirror is identical (`cmp`).
