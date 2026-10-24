---
source: "neso_data_portal"
package: "future-energy-scenario-fes-building-block-data"
dataset_keys: ["fes_building_blocks_block_definitions", "fes_building_blocks_block_licence_area", "fes_building_blocks_main"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: FES building block data
  summary: >-
    NESO's Future Energy Scenarios (FES) split to Grid Supply Points in common building blocks,
    with each edition's definitions and a licence-area mapping.
  facts:
    vendor: "NESO Data Portal: 13 CSVs, six editions of two tables, one 2024 mapping"
    cadence: "Ad hoc (NESO); editions 2020 to 2025, as at 6 October 2026"
    grain: "One row per building block per FES edition, as shown"
    history: "NESO created the package on 13 August 2020"
  landscape: power
  what_it_is: >-
    NESO calls the building blocks "a top-down breakdown of the national level FES pathway
    results" to Grid Supply Points, in a template agreed through the Energy Networks Association
    Open Networks project, and says they are not for building regional pathways. Each edition has
    its own definitions. The page shows those; the projections table is held.
  how_used:
    - "Check how FES aligns with DNOs' own regional scenarios, NESO's stated purpose"
    - "Decode a projection row's `building_block_id_number` with the same edition's definitions"
    - "Map licence-area names to Elexon GSP groups, picking the name column by edition"
  chart:
    type: bar
    silver: neso_data_portal/fes_building_blocks_block_definitions
    dedup: {"on": [resource_id, building_block_id_number], order_by: capture_written_at}
    group: edition
    group_map: {"2020": FES 2020, "2021": FES 2021, "2022": FES 2022, "2023": FES 2023, "2024": FES 2024, "2025": FES 2025}
    aggregation: count
    sort: label
    unit: building blocks
  chart_view:
    title: Building blocks NESO defines in each FES edition
    caption: >-
      Silver `fes_building_blocks_block_definitions`: block ids in each edition's definitions file,
      not projections; NESO's 2022 and 2023 files flag 50 of the 66 as included in ESO data. An id
      can change meaning between editions, so read each with its own edition.
    alt: >-
      Horizontal bar chart from neso_data_portal/fes_building_blocks_block_definitions: the number
      of building blocks in each FES edition's definitions file. FES 2020 has 49, FES 2021 has 64,
      and FES 2022, 2023, 2024 and 2025 have 66 each.
    key:
      - {series: count, label: Building blocks, paint: petrol, note: "Each bar is one NESO file; those for 2021, 2022 and 2023 were last modified in September 2026."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then 13 CSVs, each downloaded whole unless its
      `last_modified` is unchanged. Shown: first and latest, plus the 2021 definitions.
    commands:
      - {run: gridflow ingest neso_data_portal fes_building_blocks_block_definitions --last 24h, comment: "changed files; swap in either key"}
      - {run: gridflow transform neso_data_portal fes_building_blocks_block_definitions --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      silver: neso_data_portal/fes_building_blocks_block_definitions
      filter:
        - {column: building_block_id_number, op: in, value: [Lct_BB001, Lct_BB002, Lct_BB003, Lct_BB004]}
        - {column: edition, op: in, value: [2020, 2021]}
      dedup: {"on": [resource_id, building_block_id_number], order_by: capture_written_at}
      order_by: [building_block_id_number, edition]
      columns: [building_block_id_number, edition, technology_detail, technology, units, detail,
                template, comments, alignment_with_ofgem_core_scenario_key_drivers, resource_id,
                published_at, timestamp_utc]
    key: [building_block_id_number, edition, resource_id]
    caption: "The four electric vehicle blocks in FES 2020 and 2021: same ids, vans moved in 2021."
    fields:
      building_block_id_number: "NESO's block id, the projections table's join key; its meaning can change by edition"
      edition: "FES edition, from the file name; join the projections on this and the id"
      resource_id: "CKAN id of the edition's file; with edition and block id, the entity key"
      technology_detail: "NESO's detail of the technology; null where NESO gives none"
      technology: "NESO's text; 2025 file (modified 14 July 2025) fills `Dem_` rows with `Offshore-Wind (off-Grid)`"
      units: "NESO's unit text, kept as spelt; the projections' own `unit` column governs their values"
      detail: "What the block measures, in NESO's words, such as installed capacity"
      template: "NESO's block group, such as `Generation`; the 2024 file leaves most blank"
      comments: "NESO's comment on what the block covers; null where blank"
      alignment_with_ofgem_core_scenario_key_drivers: "NESO's matching Ofgem driver; 13 blocks filled 2021 to 2024, every block in 2025"
      eso_additional_notes: "2020 file only: NESO's additional notes on the block"
      eso_comments: "2021 to 2023 files only: NESO's further comments on the block"
      included_in_eso_data: "2022 and 2023 files only: `Y` or `N`; NESO does not define it"
      unnamed_8: "An unnamed, empty column in NESO's 2022 file"
      unnamed_10: "A second unnamed, empty column in NESO's 2022 file"
      published_at: "NESO's last-modified time for the edition's file, read as UTC"
      timestamp_utc: "When gridflow captured the file, UTC; the table has no event time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, here the capture time, so these cells use `data.sql()`
      on the `_latest` views of the two reference tables. No cell reads the held projections table.
    cells:
      - |
        blocks = data.sql("""
            SELECT edition, count(*) AS blocks
            FROM silver_neso_data_portal_fes_building_blocks_block_definitions_latest
            GROUP BY edition ORDER BY edition
        """)
        blocks
      - |
        dropped = data.sql("""
            SELECT building_block_id_number, technology
            FROM silver_neso_data_portal_fes_building_blocks_block_definitions_latest
            WHERE edition = 2020 AND building_block_id_number NOT IN (
                SELECT building_block_id_number
                FROM silver_neso_data_portal_fes_building_blocks_block_definitions_latest
                WHERE edition = 2021)
            ORDER BY building_block_id_number
        """)
        dropped
      - |
        areas = data.sql("""
            SELECT area_type, fes23_bb_area_name, fes2024_area_name, elexon_gsp_group
            FROM silver_neso_data_portal_fes_building_blocks_block_licence_area_latest
            ORDER BY area_type, fes23_bb_area_name
        """)
        areas.head(8)
    needs: NESO's FES building-block definitions and licence-area mapping
    plot_alt: >-
      No plot: the cells print the blocks per edition, the 2020 ids missing from 2021, and the first
      eight licence-area rows.
  related:
    - {dataset: neso_data_portal/tresp-demand-pathways, note: "NESO structures tRESP like the FES 2025 building blocks"}
    - {dataset: neso_data_portal/regional-breakdown-of-fes-data-electricity, note: "NESO's other regional cut of FES, by GSP and site codes"}
    - {dataset: neso_data_portal/gis-boundaries-for-gb-dno-license-areas, note: "Boundaries of the DNO licence areas the mapping names"}
    - {dataset: neso_data_portal/fes-electricity-demand-summary-data-table-ed1, note: "National FES demand; these files split FES results to GSPs"}
  family:
    slug: future-energy-scenario-fes-building-block-data
    members:
      - dataset: fes_building_blocks_block_definitions
        differs: "What each block id means in one edition: technology, detail and unit"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=future-energy-scenario-fes-building-block-data"
          - "GET https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/9fb5211f-9689-4d6f-a73e-cf28f03c5885/download/building-block-definitions.csv"
          - "GET https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/0dce4330-7dfe-4db6-97c9-443e82246cbc/download/building-block-definitions-2021.csv"
          - "GET https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/cc3118da-cbbe-49e8-a8ee-9bdd89a8bf9c/download/fes2025_bb2_v001.csv"
      - dataset: fes_building_blocks_block_licence_area
        differs: "FES 2023 and 2024 area names against licence names and Elexon GSP groups"
        request: "GET https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/0ec29244-277e-41d1-bca7-17f12b71eb60/download/building-block-licence-area-name-mapping-2024.csv"
      - dataset: fes_building_blocks_main
        differs: "FES projections per block, licence area, GSP, scenario and year, one file per edition"
        request:
          - "GET https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/bff7061d-fbd3-4d8a-a95b-876affc2033d/download/fes2020_building_blocks.csv"
          - "GET https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/73f69d8f-e9cb-4a2d-8538-baf03b5eadef/download/fes2025_bb1_v006.csv"
        held: NESO states no period for the year labels; 2020 to 2022 repeat rows with different values.
---

# FES: Pathways to Net Zero Building Block Data

This package is NESO's "building block" breakdown of its **Future Energy Scenarios (FES)**. The
vendor describes it as a top-down split of the national-level FES results to Grid Supply Point
(GSP) level, developed under the Energy Networks Association (ENA) Open Networks project, using an
agreed common set of "building blocks" (a numbered technology or demand component such as a
generation type, a storage type, a demand component or a low-carbon technology) so that FES and
the Distribution Network Operators' own regional scenarios (DFES) can be compared like for like.
The vendor says it is meant to clarify alignment between FES and the DFES, and **not** to be used
to create regional pathways. In gridflow terms it is a scenario input: for each FES edition from
2020 to 2025 it gives, per building block, DNO licence area and GSP, a value for each projection
year, in the unit the row itself states. It answers "where, across the DNO areas and GSPs, did
each FES edition place each technology or demand component, year by year?". It is not a
measurement, and it is not a forecast issued on a date.

**Six things to know before using any of it.**

1. **The main table (`fes_building_blocks_main`) is held** (unit E-SEM). Silver exists for the
   2023, 2024 and 2025 editions, but nothing is published from it. For it this page gives schema,
   row counts, clocks, units and key facts, and **never data values, ranges or example rows**. The
   other two families (the block definitions and the licence-area mapping) are eligible and are
   described with their values.
2. **Editions 2020, 2021 and 2022 of the main table are not loaded.** Their rows share the entity
   key (the vendor's rows repeat building block x GSP x DNO x unit with different values and no
   column says what distinguishes them), so each capture fails with `DuplicateEntityKeyError` and
   is an ADR-040 adjudicated failed capture (RULINGS 608, 623). Bronze holds the three files;
   silver holds nothing for them. They are never deduplicated or aggregated.
3. **The year label's period is unknown.** NESO's dictionaries say the value is "for the specified
   year" and do not say whether that year is calendar, financial or winter. gridflow stores the
   label as the integer `projection_year` and attaches no period (see "The projection year" below).
4. **No temporal recipe.** `timestamp_utc` is gridflow's capture time (2026-10-08), not a
   projection date. The vintage is the CKAN `last_modified` of each file, which is `available_at`.
5. **`fes_scenario` and `fes_pathway` are two separate columns, never merged.** Editions 2020 to
   2023 fill `fes_scenario`; editions 2024 and 2025 fill `fes_pathway` and leave `fes_scenario`
   null. Renaming one into the other would assert the two vocabularies are interchangeable, which
   no source says.
6. **There are no DOC resources in this package**, so there is no document to download. All 13
   resources are CSV uploads (listed in full below). The vendor's per-resource dictionary pages, for
   example the [2020 dictionary](https://www.neso.energy/data-portal/future-energy-scenario-fes-building-block-data/fes_2020_building_blocks_-_version_13)
   and the [2021 dictionary](https://www.neso.energy/data-portal/future-energy-scenario-fes-building-block-data/fes_2021_building_blocks_-_version_80),
   are the source of the column meanings below.

The shared research is gridflow `@.planning/phases/v0.22-K-SCN-1/K-SCN-1-FACTS.md` (section
SCN-1c), the held question and baseline mapping are in `@.planning/phases/v0.22-K-SCN-1/K-SCN-1c-SPEC.md`,
the verification is `@.planning/phases/v0.22-K-SCN-1c/VERIFICATION.md`, and the activation receipt
is `@.planning/v0.22-RESULTS.md` (section SCN-1c). Rulings: 603 (batch split), 608 (main held,
three adjudicated failures, baseline mapping), 622 (merge), 623 (activation). Sibling scenario
packages: @./regional-breakdown-of-fes-data-electricity.md, @./tresp-demand-pathways.md and
@./fes-electricity-demand-summary-data-table-ed1.md.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Building Block Definitions 2020 | CSV | upload | `9fb5211f-9689-4d6f-a73e-cf28f03c5885` |
| Building Block Definitions 2021 | CSV | upload | `0dce4330-7dfe-4db6-97c9-443e82246cbc` |
| Building Block Definitions 2022 | CSV | upload | `e5ab7ecb-0ab1-4fe7-833c-1fe905b086f8` |
| Building Block Definitions 2023 | CSV | upload | `f400d905-4159-4bcb-8e7d-f28528545d89` |
| Building Block Definitions 2024 | CSV | upload | `778a505c-1972-463b-b4bf-53e33c4d3470` |
| Building Block Definitions 2025 | CSV | upload | `cc3118da-cbbe-49e8-a8ee-9bdd89a8bf9c` |
| Building Block Licence Area Name Mapping 2024 | CSV | upload | `0ec29244-277e-41d1-bca7-17f12b71eb60` |
| FES 2020 Building Blocks - Version 1.3 | CSV | upload | `bff7061d-fbd3-4d8a-a95b-876affc2033d` |
| FES 2021 Building Blocks - Version 8.0 | CSV | upload | `5f93098e-1d52-44bf-a375-d3edfb89f8a5` |
| FES 2022 Building Blocks - Version 4.0 | CSV | upload | `36fd3aa9-6e42-418f-b1bb-a31bbfcf2008` |
| FES 2023 Building Blocks - Version 1.1 | CSV | upload | `8d57568c-2534-4682-ab1d-72fcf2d14998` |
| FES 2024 Building Blocks - Version 1.1 | CSV | upload | `be1f002b-bd8b-4f8d-9e1d-72d680336e26` |
| FES 2025 Building Blocks | CSV | upload | `73f69d8f-e9cb-4a2d-8538-baf03b5eadef` |

**Reading the disposition table.** All 13 resources are disposition SILVER (read to silver), and
there are no HOLD, DOC or other resources. That is a disposition of the *resource*, separate from
two other facts: the main family output is held (see Holds), and three SILVER main resources (the
2020, 2021 and 2022 files) cannot be loaded because their rows share the entity key (adjudicated
failed captures, above). Of the 13, ten reach silver: 6 definitions, 1 licence-area mapping and 3
main editions.

**Downloads and captures.** All 13 resources have `url_type: upload` and were captured once, on
2026-10-08, from `api.neso.energy` (bronze under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`, one CSV and one sidecar per
resource). Sizes and row counts are from FACTS (bytes are the physical body size; "table rows" is
the number of rows below the header in the file; "reader rows" is what the CSV reader keeps after
removing wholly blank rows). The package was created in the catalogue on 2020-08-13, last had its
metadata changed on 2026-09-16, carries version string `1.0` and 15 catalogue tags, and is
licensed "NESO Open Data Licence" (licence id `ESO`).

| Resource | Edition | Download | Bytes | Table rows / reader rows | CKAN `last_modified` | Family |
|---|---|---|---:|---|---|---|
| FES 2020 Building Blocks - Version 1.3 | 2020 | [fes2020_building_blocks.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/bff7061d-fbd3-4d8a-a95b-876affc2033d/download/fes2020_building_blocks.csv) | 11,553,187 | 32,565 / 32,565 (fails: shared key) | 2020-09-07T13:38:22.491166 | `fes_building_blocks_main` |
| FES 2021 Building Blocks - Version 8.0 | 2021 | [fes-2021-building-blocks-version-008.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/5f93098e-1d52-44bf-a375-d3edfb89f8a5/download/fes-2021-building-blocks-version-008.csv) | 11,567,428 | 44,336 / 44,336 (fails: shared key) | 2022-02-17T10:22:57.199905 | `fes_building_blocks_main` |
| FES 2022 Building Blocks - Version 4.0 | 2022 | [fes-2022-building-blocks-version-4.0.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/36fd3aa9-6e42-418f-b1bb-a31bbfcf2008/download/fes-2022-building-blocks-version-4.0.csv) | 12,640,835 | 50,812 / 50,812 (fails: shared key) | 2022-09-23T16:06:07.625574 | `fes_building_blocks_main` |
| FES 2023 Building Blocks - Version 1.1 | 2023 | [fes-2023-building-blocks-version-1.1.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/8d57568c-2534-4682-ab1d-72fcf2d14998/download/fes-2023-building-blocks-version-1.1.csv) | 11,421,609 | 50,809 / 46,258 | 2023-07-21T15:52:22.011143 | `fes_building_blocks_main` |
| FES 2024 Building Blocks - Version 1.1 | 2024 | [fes-2024-building-blocks-version-1.1.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/be1f002b-bd8b-4f8d-9e1d-72d680336e26/download/fes-2024-building-blocks-version-1.1.csv) | 13,349,288 | 56,527 / 56,527 | 2024-08-02T10:37:06.008284 | `fes_building_blocks_main` |
| FES 2025 Building Blocks | 2025 | [fes2025_bb1_v006.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/73f69d8f-e9cb-4a2d-8538-baf03b5eadef/download/fes2025_bb1_v006.csv) | 11,530,820 | 48,019 / 48,019 | 2025-12-10T16:53:30.336039 | `fes_building_blocks_main` |
| Building Block Definitions 2020 | 2020 | [building-block-definitions.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/9fb5211f-9689-4d6f-a73e-cf28f03c5885/download/building-block-definitions.csv) | 8,353 | 53 / 49 | 2020-08-13T12:40:08.469499 | `fes_building_blocks_block_definitions` |
| Building Block Definitions 2021 | 2021 | [building-block-definitions-2021.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/0dce4330-7dfe-4db6-97c9-443e82246cbc/download/building-block-definitions-2021.csv) | 11,046 | 64 / 64 | 2026-09-16T13:33:00.286867 | `fes_building_blocks_block_definitions` |
| Building Block Definitions 2022 | 2022 | [building-block-definitions-2022.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/e5ab7ecb-0ab1-4fe7-833c-1fe905b086f8/download/building-block-definitions-2022.csv) | 12,205 | 66 / 66 | 2026-09-03T13:45:29.162340 | `fes_building_blocks_block_definitions` |
| Building Block Definitions 2023 | 2023 | [building-block-definitions-2023.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/f400d905-4159-4bcb-8e7d-f28528545d89/download/building-block-definitions-2023.csv) | 12,029 | 66 / 66 | 2026-09-03T13:44:08.323327 | `fes_building_blocks_block_definitions` |
| Building Block Definitions 2024 | 2024 | [building-block-definitions-2024.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/778a505c-1972-463b-b4bf-53e33c4d3470/download/building-block-definitions-2024.csv) | 7,523 | 66 / 66 | 2024-07-15T06:35:12.667550 | `fes_building_blocks_block_definitions` |
| Building Block Definitions 2025 | 2025 | [fes2025_bb2_v001.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/cc3118da-cbbe-49e8-a8ee-9bdd89a8bf9c/download/fes2025_bb2_v001.csv) | 11,583 | 66 / 66 | 2025-07-14T04:48:17.882181 | `fes_building_blocks_block_definitions` |
| Building Block Licence Area Name Mapping 2024 | 2024 | [building-block-licence-area-name-mapping-2024.csv](https://api.neso.energy/dataset/30df2649-99cf-4f84-9128-6c58fc1ea72a/resource/0ec29244-277e-41d1-bca7-17f12b71eb60/download/building-block-licence-area-name-mapping-2024.csv) | 1,436 | 19 / 19 | 2024-07-15T06:35:22.821993 | `fes_building_blocks_block_licence_area` |

The late `last_modified` dates on the 2021, 2022 and 2023 definitions files (September 2026) are
genuine vintages, so they are `available_at` and are not replaced with the edition year (see the
definitions family for the consequence for as-of queries). The file for edition 2025 of the
definitions is named `fes2025_bb2_v001.csv`; its title says "Building Block Definitions 2025".

## Families

**What applies to all three families.**

*Identity and selection.* Each resource is one edition of one table, so each capture is a whole
file. The record sets `latest` to `whole_capture` per `resource_id` (`latest_partition:
resource_id`): each edition's capture is its own partition, and a later NESO re-upload of a
resource would add a new whole capture and `_latest` would take that resource whole. A bronze
capture is never edited. `edition` is the FES publication year taken from the exact filename
(each family's edition map below; a filename that is not in the map fails loudly, it is never
guessed). The entity key of each family includes `resource_id` and `edition`. NESO states no
composite-uniqueness guarantee for any of them (`TODO: verify` vendor-declared uniqueness); the
key is unique on every loaded capture, and is not unique on the three main captures that fail.

*The two clocks (every family).*

1. **Vintage: `ckan_last_modified`.** `published_at` and `available_at` are the CKAN
   `last_modified` of the captured file, both equal, and different per edition (listed per family
   below). It is **not** the capture time and **not** the edition or projection year (ADR-030). An
   as-of query is `WHERE available_at <= :as_of` (RULINGS 597). An edition is visible from its
   `available_at` onward and not before.
2. **Event time: none.** The record has `temporal: none`, so **`timestamp_utc` is the capture
   time** (2026-10-08, listed per family below) and `event_time` equals it on every row. It
   carries no projection information; do not use it as a time axis. No row has an issue time.
   The projection year is a scenario period, not an observation or issue time.

*Units (vendor dictionary only, as cited in FACTS; never inferred from a column name).* The main
table has no unit column in the vendor dictionary sense: **each row carries its own `unit`
column**, and `value` is in that unit (see the main family). The block-definitions `Units` column is
a free-text descriptor (see that family). The licence-area mapping has no numeric measure and no
unit. The "Vendor unit" column in the generated schema tables below is the vendor dictionary's
entry as recorded by the registry; where it reads `MW` against a text column that is the
dictionary's blanket entry and does not describe the column (FACTS: the early dictionaries' blanket
MW entries do not describe rows whose own unit is `Number` or `GWh`).

*Missing values and sentinels (FACTS g5).* NESO declares no null token. None of the listed
literal tokens (a lone `-`, `NA`, `n/a`) occurs in any capture of the package. The literal `N/A`
occurs only in the licence-area mapping (see that family), where it is kept as text. Blank cells
are stored as null, never as zero. A numeric zero is a zero: no vendor source defines zero as
missing, so it is never converted to null. The record has no null-token map. Every nonblank
`value` and `Share of GSP` cell casts strictly to float64 and every year header to int64, with
zero failures on all six main bodies (FACTS).

*Silver layout (all three).* Parquet files under
`C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`, one file per capture,
written by runs between `2026-10-08T10-52-56` and `2026-10-08T10-53-34`. The `year=`/`month=`
partition is the **capture** date. Lineage columns appended to the vendor columns: `edition`,
`resource_id`, `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`,
`event_time`, `available_at`, `source_run_id`, `dataset_version`. All timestamps are tz-aware UTC.
`dataset_version` reads `1+e1` on every capture of every family, including those that use a
second or later header layout; what `e1` encodes is not established here (`TODO: verify`), so do
not use it to tell layouts apart. Because the layouts differ, the silver tables are unions of the
epochs' columns with nulls where a layout lacks a column (see the definitions family).

### `fes_building_blocks_block_definitions`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Template | `template` | string | — | yes | — | MW |
| Technology | `technology` | string | — | yes | — | MW |
| Building Block ID Number | `building_block_id_number` | string | — | no | — | MW |
| Technology Detail | `technology_detail` | string | — | yes | — | MW |
| Units | `units` | string | — | yes | — | MW |
| Detail | `detail` | string | — | yes | — | MW |
| Comments | `comments` | string | — | yes | — | — |
| ESO Additional Notes | `eso_additional_notes` | string | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Template | `template` | string | — | yes | — | MW |
| Technology | `technology` | string | — | yes | — | MW |
| Building Block ID Number | `building_block_id_number` | string | — | no | — | MW |
| Technology Detail | `technology_detail` | string | — | yes | — | MW |
| Units | `units` | string | — | yes | — | MW |
| Detail | `detail` | string | — | yes | — | MW |
| Comments | `comments` | string | — | yes | — | — |
| Alignment with Ofgem Core Scenario Key Drivers | `alignment_with_ofgem_core_scenario_key_drivers` | string | — | yes | — | — |
| ESO Comments | `eso_comments` | string | — | yes | — | — |

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Template | `template` | string | — | yes | — | MW |
| Technology | `technology` | string | — | yes | — | MW |
| Building Block ID Number | `building_block_id_number` | string | — | no | — | MW |
| Technology Detail | `technology_detail` | string | — | yes | — | MW |
| Units | `units` | string | — | yes | — | MW |
| Detail | `detail` | string | — | yes | — | MW |
| Comments | `comments` | string | — | yes | — | — |
|  | `unnamed_8` | string | — | yes | — | — |
| Alignment with Ofgem Core Scenario Key Drivers | `alignment_with_ofgem_core_scenario_key_drivers` | string | — | yes | — | — |
| _duplicated_0 | `unnamed_10` | string | — | yes | — | — |
| Included in ESO Data | `included_in_eso_data` | string | — | yes | — | — |
| ESO Comments | `eso_comments` | string | — | yes | — | — |

Schema, epoch 4:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Template | `template` | string | — | yes | — | MW |
| Technology | `technology` | string | — | yes | — | MW |
| Building Block ID Number | `building_block_id_number` | string | — | no | — | MW |
| Technology Detail | `technology_detail` | string | — | yes | — | MW |
| Units | `units` | string | — | yes | — | MW |
| Detail | `detail` | string | — | yes | — | MW |
| Comments | `comments` | string | — | yes | — | — |
| Alignment with Ofgem Core Scenario Key Drivers | `alignment_with_ofgem_core_scenario_key_drivers` | string | — | yes | — | — |
| Included in ESO Data | `included_in_eso_data` | string | — | yes | — | — |
| ESO Comments | `eso_comments` | string | — | yes | — | — |

Schema, epoch 5:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Template | `template` | string | — | yes | — | MW |
| Technology | `technology` | string | — | yes | — | MW |
| Building Block ID Number | `building_block_id_number` | string | — | no | — | MW |
| Technology Detail | `technology_detail` | string | — | yes | — | MW |
| Units | `units` | string | — | yes | — | MW |
| Detail | `detail` | string | — | yes | — | MW |
| Comments | `comments` | string | — | yes | — | — |
| Alignment with Ofgem Core Scenario Key Drivers | `alignment_with_ofgem_core_scenario_key_drivers` | string | — | yes | — | — |

- Entity key: `resource_id`, `edition`, `building_block_id_number`
- Latest: `whole_capture` per `resource_id`
- Edition: `building-block-definitions.csv` → 2020; `building-block-definitions-2021.csv` → 2021; `building-block-definitions-2022.csv` → 2022; `building-block-definitions-2023.csv` → 2023; `building-block-definitions-2024.csv` → 2024; `fes2025_bb2_v001.csv` → 2025
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible. Silver: 377 rows (49 + 64 + 66 + 66 + 66 + 66), 23 columns** (the union of the five
layouts plus the lineage columns). This is reference data: one row per building block per
edition, no projection year, no numeric measure, and it is not an unpivot. The block id
(`building_block_id_number`) identifies the block in vendor text and is unique in every edition
(measured, not a vendor guarantee). Each row describes a block: its template, technology, a
technology detail, the unit descriptor, a longer detail and comment, and in later editions a
column aligning the block with Ofgem's core scenario key drivers and a flag `Included in ESO Data`
(`TODO: verify` the vendor's meaning of the alignment text and of the `Included in ESO Data` flag).

| Edition | Layout (epoch) | Rows | `published_at` = `available_at` | `timestamp_utc` (capture) |
|---|---|---:|---|---|
| 2020 | 1 (8 columns) | 49 | 2020-08-13T12:40:08.469499 | 2026-10-08T10:52:56.827482 |
| 2021 | 2 (9 columns) | 64 | 2026-09-16T13:33:00.286867 | 2026-10-08T10:52:59.591925 |
| 2022 | 3 (12 columns) | 66 | 2026-09-03T13:45:29.162340 | 2026-10-08T10:53:02.747471 |
| 2023 | 4 (10 columns) | 66 | 2026-09-03T13:44:08.323327 | 2026-10-08T10:53:05.280666 |
| 2024 | 5 (8 columns) | 66 | 2024-07-15T06:35:12.667550 | 2026-10-08T10:53:07.837772 |
| 2025 | 5 (8 columns) | 66 | 2025-07-14T04:48:17.882181 | 2026-10-08T10:53:10.665613 |

*Two clocks.* Vintage is the `last_modified` above: note that the 2021, 2022 and 2023 definitions
carry **September 2026** vintages even though they describe earlier editions, so an as-of query
before those dates does not see them, while the same-edition main files were published in 2022 to
2023 (the 2023 main file, loaded to silver, on 2023-07-21). Do not join editions across the two families on `available_at`; join on
`edition`. Event time: none, so `timestamp_utc` is the capture time.

*Raw rows versus silver.* The 2020 file has 53 table rows, of which four are wholly blank; the
CSV reader removes them, so 49 rows are kept. No other definitions file has a blank row.

*Unnamed columns.* The 2022 file has two physically unnamed columns at positions 8 and 10 (the
generated epoch 3 table above: `unnamed_8`, and `unnamed_10` for the column the parser names
`_duplicated_0`). Both are blank in all 66 rows of that file. The registry names them, so the
distinct parsed header names settle the repeated-header flag; the two columns hold nothing. In the
silver union, `unnamed_8` and `unnamed_10` are null on all 377 rows.

*The `Units` column (vendor descriptor, not normalised).* It is kept exactly as the vendor
spells it and is not a guessed unit enum. The spellings across the editions are: `" MW"` (with a
leading space), `"MW"`, `"MW availability"`, `"Metres squared"`, `" Metres squared "`,
`"% customers "`, `"Number of"`, `"Number of "` (trailing space), `"Number of properties connected
to DH"`, `"Number of properties connected to Low carbon district heating"` (2025 only), `"GWh"`, and
a blank. Both the leading and trailing whitespace variants are real and are preserved. The 2024
file has **two** rows whose `Units` cell is blank: `TODO: verify` the vendor's unit for those two
blocks; they stay null until NESO supplies them. These descriptors say what unit the *main* table
uses for a block, but the main table's own `unit` column is authoritative for its rows (and its
spellings, `MW`, `GWh` and `Number`, differ from these descriptors).

*Blanks (silver nulls by edition; every column not named has none).*

| Edition | Null counts |
|---|---|
| 2020 | `eso_additional_notes` 36 (`template`, `technology`, `units` have none; the columns this layout lacks are null by union) |
| 2021 | `eso_additional_notes`, `unnamed_8` and `unnamed_10` do not exist in this layout (null by union); `alignment_with_ofgem_core_scenario_key_drivers` 51; `eso_comments` 45 |
| 2022 | `alignment_with_ofgem_core_scenario_key_drivers` 53; `eso_comments` 48; `unnamed_8` 66; `unnamed_10` 66 |
| 2023 | `alignment_with_ofgem_core_scenario_key_drivers` 53; `eso_comments` 48 |
| 2024 | `template` 62; `technology` 38; `units` 2; `alignment_with_ofgem_core_scenario_key_drivers` 53 |
| 2025 | none beyond the common descriptive columns below (this layout has no `eso_comments` or `included_in_eso_data`) |

In every edition the common descriptive columns have a few blanks: `technology_detail` (14 raw
blanks in 2020 including the four blank rows, 10 in each of 2021 to 2025) and `comments` (32 raw in
2020 and 35 in each of 2021 to 2025); `detail` has 5 in 2020 and 2024 and 3 in each of 2021 to 2023
and 2025 (all FACTS g5 raw counts; the 2020 figures include the four blank rows).

*`Technology` in 2025.* The 2025 file writes `Offshore-Wind (off-Grid)` in `Technology` on all 12
demand rows (`Dem_`), the value of the generation row above them (`Gen_BB024`); the 2024 file
leaves those cells blank (bronze `raw_20261008T105310Z_cc3118da-...csv` lines 26 to 37, against
`raw_20261008T105307Z_778a505c-...csv`). It looks like a fill-down in NESO's file; gridflow keeps
it as published, so `technology` is not a reliable label for 2025 demand blocks (use
`technology_detail`).

*Building-block ids.* The ids carry a prefix family: `Gen_` (generation), `Srg_` (storage),
`Dem_` (demand) and `Lct_` (low-carbon technology) with a `BB` number, and a letter suffix in some
editions; the 2020 file also has four ids that follow no such prefix. Counts by prefix are 20 / 11 /
5 / 9 in 2020 (+4 others), 24 / 11 / 10 / 19 in 2021, 24 / 11 / 12 / 19 in 2022 to 2025 (`Gen` /
`Srg` / `Dem` / `Lct`). The prefix words are an observation of the ids, not a vendor definition
(`TODO: verify` the vendor's name for each family of block). An id is not stable across
editions: `Lct_BB001` to `Lct_BB004` keep their ids but move vans from the "other road vehicles"
blocks to the car and motorbike blocks in 2021 (`technology_detail`, `comments`), and 12 of the
2020 ids (among them `Srg_BB006` to `Srg_BB011`, the DSR blocks, and the four unprefixed ids) are
absent from 2021, which adds 27 (2026-10-08 captures). Read each id with its own edition.

*Join to the main table.* In each of editions 2023, 2024 and 2025, every one of the 50
building-block ids in the main table's silver exists in the same-edition definitions; the
definitions have 16 further blocks that the main table does not use. In the 2022 and 2023
definitions, `Included in ESO Data` is `Y` on exactly those 50 ids and `N` on the 16 (measured;
NESO does not define the flag). The definitions file for
editions 2020 to 2022 can be read independently, but the corresponding main captures are not
loaded.

### `fes_building_blocks_block_licence_area`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Area Type | `area_type` | string | — | yes | — | — |
| FES23 BB Area Name | `fes23_bb_area_name` | string | — | no | — | — |
| Full Licence Name | `full_licence_name` | string | — | yes | — | — |
| Elexon GSP Group | `elexon_gsp_group` | string | — | yes | — | — |
| Elexon GSP Group Name | `elexon_gsp_group_name` | string | — | yes | — | — |
| FES2024 Area Name | `fes2024_area_name` | string | — | yes | — | — |
| Comments | `comments` | string | — | yes | — | — |

- Entity key: `resource_id`, `edition`, `fes23_bb_area_name`
- Latest: `whole_capture` per `resource_id`
- Edition: `building-block-licence-area-name-mapping-2024.csv` → 2024
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible. Silver: 19 rows, 17 columns, one capture.** A reference table that maps the area names
used in the FES 2023 building-block files (`FES23 BB Area Name`) to the full licence name, the
Elexon GSP group and the area names used from FES 2024 (`FES2024 Area Name`). It has no numeric
measure, no year and no unit. `published_at` = `available_at` = 2024-07-15T06:35:22.821993;
`timestamp_utc` (capture) = 2026-10-08T10:53:14.274565. Event time: none.

Its 19 rows are, by `area_type`: 14 `DNO` rows (the distribution network operators), 3 `TO` rows
(NGET, SHETL, SPTL, the transmission owners), 1 `IDNO` row (independent distribution network
operators) and 1 `Non-network connected` row (labelled `Not Connected`; its comment gives offshore
wind exclusively for hydrogen production as an example). All 19 values of `fes23_bb_area_name` are
unique and nonblank (measured; no vendor uniqueness guarantee, `TODO: verify`).

| `area_type` | `fes23_bb_area_name` | `full_licence_name` | `elexon_gsp_group` | `elexon_gsp_group_name` | `fes2024_area_name` |
|---|---|---|---|---|---|
| DNO | ENW | Electricity North West | `_G` | North Western | Electricity North West |
| DNO | EPN | Eastern Power Networks | `_A` | Eastern | UKPN Eastern |
| DNO | East Midlands | NGED (East Midlands) | `_B` | East Midlands | NGED East Midlands |
| DNO | LPN | London Power Networks | `_C` | London | UKPN London |
| DNO | NPgN | Northern Power Grid (Northeast) | `_F` | Northern | NPg Northeast |
| DNO | NPgY | Northern Power Grid (Yorkshire) | `_M` | Yorkshire | NPg Yorkshire |
| DNO | SEPD | Southern Electric Power Distribution | `_H` | Southern | SSEN South |
| DNO | SHEPD | Scottish Hydro Electric Power Distribution | `_P` | North Scotland | SSEN (SHEPD) |
| DNO | SPD | SP Distribution | `_N` | South Scotland | SPEN |
| DNO | SPM | SP Manweb | `_D` | Merseyside and North Wales | SPEN Manweb |
| DNO | SPN | South Eastern Power Networks | `_J` | South Eastern | UKPN South East |
| DNO | South Wales | NGED (South Wales) | `_K` | South Wales | NGED South Wales |
| DNO | South Western | NGED (South West) | `_L` | South Western | NGED South West |
| DNO | West Midlands | NGED (West Midlands) | `_E` | Midlands | NGED West Midlands |
| TO | NGET | National Grid Electricity Transmission | N/A | N/A | NGET |
| TO | SHETL | Scottish Hydro Electricity Transmission | N/A | N/A | SHETL |
| TO | SPTL | Scottish Power Transmission | N/A | N/A | SPTL |
| IDNO | IDNO | Independent Distribution Network Operator | N/A | N/A | IDNO |
| Non-network connected | Not Connected | Not Connected | N/A | N/A | Not Connected |

*Sentinels.* `elexon_gsp_group` and `elexon_gsp_group_name` each contain **five literal `N/A`
cells** (the five rows with no Elexon group: three `TO`, `IDNO` and `Not Connected`). They are kept
as the text `N/A` and are not converted to null: gridflow adopts no vendor meaning for them beyond
"no Elexon GSP group applies" (the registry records the literal; `TODO: verify` NESO's stated
meaning). `comments` is blank on 18 rows (null). The Elexon group ids are the single-letter codes
with a leading underscore (`_A` to `_P`), stored as published and not normalised.

*Join to the main table.* The main table's `dno_license_area` uses the names in this mapping:
edition 2023 uses `fes23_bb_area_name` values (18 of its 19 distinct labels match; the one that
does not is the label `IDNO - Refer to Comment Field`), and editions 2024 and 2025 use
`fes2024_area_name` values (18 of 19 match in 2024, with the same unmatched label, and 18 of 18
match in 2025). A join on the wrong name column therefore silently matches only a handful of areas
(4 of 19 labels in 2024 when joined on `fes23_bb_area_name`). Pick the column by edition, and do not
inner-join (the `IDNO - Refer to Comment Field` rows would drop).

### `fes_building_blocks_main`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building Block ID Number | `building_block_id_number` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| DNO License Area | `dno_license_area` | string | — | no | — | — |
| FES Scenario | `fes_scenario` | string | — | yes | — | — |
| GSP | `gsp` | string | — | no | — | — |
| Comment | `comment` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `Baseline (2019)` → 2019, `2020` → 2020, `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| FES Scenario | `fes_scenario` | string | — | yes | — | — |
| Building Block ID Number | `building_block_id_number` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| DNO License Area | `dno_license_area` | string | — | no | — | — |
| GSP | `gsp` | string | — | no | — | — |
| Share of GSP | `share_of_gsp` | float64 | — | yes | — | — |
| Comment | `comment` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `Baseline (2020)` → 2020, `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| FES Scenario | `fes_scenario` | string | — | yes | — | — |
| Building Block ID Number | `building_block_id_number` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| DNO License Area | `dno_license_area` | string | — | no | — | — |
| GSP | `gsp` | string | — | no | — | — |
| Share of GSP | `share_of_gsp` | float64 | — | yes | — | — |
| Comment | `comment` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 3: `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 4:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| FES Scenario | `fes_scenario` | string | — | yes | — | — |
| Building Block ID Number | `building_block_id_number` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| DNO License Area | `dno_license_area` | string | — | no | — | — |
| GSP | `gsp` | string | — | no | — | — |
| Share of GSP | `share_of_gsp` | float64 | — | yes | — | — |
| Comment | `comment` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 4: `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 5:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| FES Pathway | `fes_pathway` | string | — | yes | — | — |
| Building Block ID Number | `building_block_id_number` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| DNO License Area | `dno_license_area` | string | — | no | — | — |
| GSP | `gsp` | string | — | no | — | — |
| Share of GSP | `share_of_gsp` | float64 | — | yes | — | — |
| Comment | `comment` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 5: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 6:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| FES Pathway | `fes_pathway` | string | — | yes | — | — |
| Building Block ID Number | `building_block_id_number` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| DNO License Area | `dno_license_area` | string | — | no | — | — |
| GSP | `gsp` | string | — | no | — | — |
| Share of GSP | `share_of_gsp` | float64 | — | yes | — | — |
| Comment | `comment` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 6: `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `fes_scenario`, `fes_pathway`, `building_block_id_number`, `dno_license_area`, `gsp`, `unit`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2020_building_blocks.csv` → 2020; `fes-2021-building-blocks-version-008.csv` → 2021; `fes-2022-building-blocks-version-4.0.csv` → 2022; `fes-2023-building-blocks-version-1.1.csv` → 2023; `fes-2024-building-blocks-version-1.1.csv` → 2024; `fes2025_bb1_v006.csv` → 2025
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM). Silver exists for editions 2023, 2024 and 2025 only: 4,220,751 rows
(1,341,482 + 1,582,756 + 1,296,513), 20 columns.** This section gives structure, counts and clocks.
It carries no value, range, zero count or sample row, and nothing published from this family may
until the hold is answered (see Holds).

*Shape: a wide file unpivoted to long.* Each source row is one building block, in one unit, for one
DNO licence area and one GSP, in one scenario (or pathway), with one column per projection year.
The record unpivots the year columns (ADR-042): each source row becomes one long row per year
column, with `projection_year` the integer label and `value` the cell as float64 (nullable). The
header layouts differ by edition, in six epochs: the set of year columns shrinks by edition (the
2020 file has a `Baseline (2019)` column plus 2020 to 2050; the 2021 file a `Baseline (2020)`
column plus 2021 to 2050; the 2022 file 2021 to 2050; 2023: 2022 to 2050; 2024: 2023 to 2050; 2025:
2024 to 2050), and the scenario column is `FES Scenario` up to 2023 and `FES Pathway` from 2024.
Long row counts equal the retained source rows times the number of year columns:

| Edition | Epoch | Year columns | Source rows kept | Long rows | Loaded? |
|---|---:|---|---:|---:|---|
| 2020 | 1 | `Baseline (2019)`, 2020 to 2050 (32) | 32,565 | 1,042,080 | no: shared key, adjudicated failed |
| 2021 | 2 | `Baseline (2020)`, 2021 to 2050 (31) | 44,336 | 1,374,416 | no: shared key, adjudicated failed |
| 2022 | 3 | 2021 to 2050 (30) | 50,812 | 1,524,360 | no: shared key, adjudicated failed |
| 2023 | 4 | 2022 to 2050 (29) | 46,258 | 1,341,482 | yes |
| 2024 | 5 | 2023 to 2050 (28) | 56,527 | 1,582,756 | yes |
| 2025 | 6 | 2024 to 2050 (27) | 48,019 | 1,296,513 | yes |

The 2025 file has 27 year columns, not 31, so its long count is not "rows x 31". The 2023 file's
50,809 table rows include a fully blank tail of 4,551 rows; the CSV reader removes it, leaving
46,258. The long counts for 2020, 2021 and 2022 are the counts the unpivot would give (they match
the key-collision counts below) but those captures are never written to silver.

*The baseline column.* The 2020 and 2021 files carry a baseline column (`Baseline (2019)` and
`Baseline (2020)`). The vendor dictionaries call these the baseline values for 2019, and for 2020
in the next edition; so the record maps the labels to the integers **2019** (in the 2020
edition) and **2020** (in the 2021 edition), see the unpivot lines above. That evidences the
labelled year only, not the period it denotes (below). Because those editions are not loaded, no
silver row carries the baseline mapping today; it is kept in the record so that the mapping is
already decided if a corrected capture arrives. Editions 2022 to 2025 have no baseline column.

*The projection year (FACTS g1).* `projection_year` is an integer taken from the column header
and is a scenario year label. The accessible resource dictionaries say a value is "for the
specified year" without resolving whether the label is a calendar year, a financial year or a
winter year, for any edition, or for the baseline. **That is part of the hold** and is `TODO:
verify` per edition from the matching-edition FES data workbook notes or a specific NESO
explanation. Do not carry an older FES convention across editions without edition-specific
support, and do not turn the label into a date. The label has no unit.

*Units (vendor dictionary, as cited in FACTS).* The vendor dictionary lists MW against the value
columns of the early editions as a blanket entry, which does not describe the rows whose own
unit is `Number` or `GWh`. The authoritative unit is the **row's own `unit` column**, so `value`
is read together with `unit`. The exact nonblank `unit` values in the captures are `MW`, `GWh`
and `Number` in every edition loaded to silver (2023, 2024, 2025); the 2020 file has `MW` and
`Number` and the 2021 file has `GWh`, `MW`, `MW availability` and `Number` (those editions are
not loaded). The meaning observed from the block definitions: generation and storage blocks are
`MW`; the demand blocks `Dem_BB003` to `Dem_BB008` (and their suffixed variants) are `GWh`;
`Dem_BB009` is `MW`; from 2021 the other demand blocks (`Dem_BB001a`, `Dem_BB002a`) and the
included low-carbon-technology blocks are `Number` (in 2020 two demand blocks are `MW`) (FACTS,
actual cells, not a rule for uncaptured block ids). Whether an energy (`GWh`) value is a
year total, and what interval the year covers, is part of the period question above (`TODO:
verify`). The share column has no unit (`TODO: verify` its basis).

*Key and uniqueness.* The entity key (above) includes `resource_id` and `edition`, the nullable
`fes_scenario` and `fes_pathway` (exactly one of which is filled per edition), the block id, DNO
area, GSP, unit and `projection_year`. On the loaded editions the key is unique (zero duplicate
tuples). On the three failed editions it is not, even after adding the DNO area, the unit and the
comment to the candidate key:

| Edition | Rows sharing a key after the unpivot (the failing count) | Source-row groups behind it |
|---|---:|---|
| 2020 | 81,664 | 2,552 source rows in 1,276 repeated key tuples (each key shared by 2 rows), over 32 year columns |
| 2021 | 10,974 | 354 source rows (168 repeated tuples plus 186 excess rows), multiplicity up to 18, over 31 year columns |
| 2022 | 55,410 | 1,847 source rows (670 repeated tuples plus 1,177 excess rows), multiplicity up to 141, over 30 year columns; 471 excess rows are identical in every cell |

The vendor's rows repeat building block x GSP x DNO x unit (and the scenario or pathway) with
different values, and no column distinguishes them: some dimension of the row grain has been
omitted from the published file. `edition` and `resource_id` are constant inside a body and
cannot separate them, and adding the values to the key would encode revisions as identity. The 2022
file also has rows identical in every cell, so no choice of key built from the file's own columns
makes it unique. Resolving it needs a vendor explanation of the omitted dimension, corrected
captures, or an explicitly authorised aggregation or row-identity policy; ADR-040 adjudication is
not permission to discard the rows silently. This is the second half of the hold question.

*Loaded editions, structure only.*

| Edition | Rows | `fes_scenario` or `fes_pathway` | Blocks / DNO areas / GSPs | `published_at` = `available_at` | `timestamp_utc` (capture) |
|---|---:|---|---|---|---|
| 2023 | 1,341,482 | `fes_scenario`, 4 distinct (`fes_pathway` null on every row) | 50 / 19 / 376 | 2023-07-21T15:52:22.011143 | 2026-10-08T10:53:27.019988 |
| 2024 | 1,582,756 | `fes_pathway`, 4 distinct (`fes_scenario` null on every row) | 50 / 19 / 378 | 2024-08-02T10:37:06.008284 | 2026-10-08T10:53:30.058267 |
| 2025 | 1,296,513 | `fes_pathway`, 4 distinct (`fes_scenario` null on every row) | 50 / 18 / 378 | 2025-12-10T16:53:30.336039 | 2026-10-08T10:53:34.208849 |

`projection_year` runs 2022 to 2050 (29 distinct) in edition 2023, 2023 to 2050 (28) in 2024 and
2024 to 2050 (27) in 2025. The scenario and pathway names are the vendor's labels: edition 2023
uses `Consumer Transformation`, `Falling Short`, `Leading the Way` and `System Transformation`;
editions 2024 and 2025 use `Electric Engagement`, `Holistic Transition` and `Hydrogen Evolution`
plus `Counterfactual` (2024) or `Falling Behind` (2025). `fes_scenario` and `fes_pathway` are
different vocabularies and stay in different columns.

*Two clocks.* Vintage: the `last_modified` above, which is `available_at` and differs per edition;
the 2025 file (title "FES 2025 Building Blocks", no version in the title) was last modified on
2025-12-10. Event time: none, so `timestamp_utc` carries no projection information.

*Missing values and sentinels (silver nulls, FACTS g5).* `value` has **no** null on any loaded
edition (the three loaded files have no blank projection cell after the 2023 blank tail is
removed) and no sentinel token. The 2020 and 2022 files do have blank projection cells (2020
across all 31 projection columns, 2022 across all 30; the per-column vectors are in FACTS) but those
files are not loaded. `Share of GSP` is blank on every row of edition 2023 (the column exists in that layout
and is entirely empty), on 982,016 long rows of 2024 (35,072 source rows) and on 959,256 of 2025
(35,528 source rows), and is a populated float on the remaining rows; the meaning of a blank share
and the basis of a populated one are `TODO: verify` (FACTS: the current dictionary gives a
meaning to a blank in its own context, which is not retrospectively applied to older editions;
older blanks are not filled). `comment` is mostly null (1,334,261, 1,573,572 and 1,293,489 null
long rows in 2023, 2024 and 2025). Zeros in `value` are vendor values and are never nulled; their
counts are withheld here because the family is held.

*Join keys.* `dno_license_area` joins to the licence-area mapping (names depend on the edition, see
that family) and `building_block_id_number` joins to the same-edition block definitions. `gsp` is
the vendor's GSP name or code as published (no normalisation, not an EIC code). Never inner-join
on `gsp` or `dno_license_area`: the IDNO label differs from the mapping's.

*Memory.* The generic engine's largest healthy capture (the 2024 main file) peaks at about 805 MiB
process working set when typed in memory (the three failing captures fail at 571, 731 and 744
MiB; verification peak figures, Windows peak working set including interpreter and Polars
overhead).

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Ad hoc

The captured `last_modified` dates are irregular: the main editions were last modified in
September 2020, February 2022, September 2022, July 2023, August 2024 and December 2025; the
definitions between August 2020 and September 2026; the mapping in July 2024. The vendor states no
publication schedule. There is no scheduled refresh in gridflow (the package was captured once, on
2026-10-08, by the portal sweep). Whether NESO will add a 2026 edition, re-upload an existing
resource (a new `last_modified` makes a new whole capture and `_latest` follows it), or correct the
2020 to 2022 main files is unknown (`TODO: verify`): the catalogue snapshot of 2026-10-06 lists 13
resources and no later edition. If NESO adds resources the registry needs a new record entry for
each (an unmapped filename fails loudly rather than being guessed).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_building_blocks_main`: held: TODO: for each edition, what period does a building-block year label (and the 2019/2020 baseline) denote — calendar year, financial year or winter? And what omitted row-grain dimension makes the 2020–2022 rows unique (repeated building block × GSP × DNO × unit rows with different values)? NESO's dictionaries state neither. (unit E-SEM)

The silver output of `fes_building_blocks_main` exists on disk for editions 2023, 2024 and 2025,
but it is **held**: not eligible for publication or for model use until unit E-SEM has an answer
(RULINGS 608, 623). It is a **domain-truth question** (vendor semantics) that gridflow does not
guess; the hold applies to the whole family output, not to a subset of columns or editions. It has
two parts:

1. **The period of the year label** (every edition, including the 2019 and 2020 baseline labels):
   calendar year, financial year or winter. Settles it: the matching-edition FES data workbook
   notes, or a specific NESO explanation. The mapping of the baseline labels to the integers 2019
   and 2020 is evidenced and is not what is held.
2. **The omitted row-grain dimension of the 2020, 2021 and 2022 files**: which column or concept
   distinguishes the repeated building block x GSP x DNO x unit rows. Settles it: a NESO
   explanation, corrected captures, or an explicitly authorised aggregation policy. Until then the
   three captures stay bronze-only, adjudicated failed (ADR-040, `DuplicateEntityKeyError`, 81,664 /
   10,974 / 55,410 rows sharing a key), and are not deduplicated.

Not held (eligible): `fes_building_blocks_block_definitions` and
`fes_building_blocks_block_licence_area`. Open but not a hold: the meaning of `Share of GSP`, of the
`Included in ESO Data` flag and of the alignment column (each `TODO: verify` above); the unit of
two 2024 definitions rows; the `dataset_version` suffix `e1`.
