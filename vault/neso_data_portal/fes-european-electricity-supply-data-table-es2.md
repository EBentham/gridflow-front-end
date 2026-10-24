---
source: "neso_data_portal"
package: "fes-european-electricity-supply-data-table-es2"
dataset_key: "fes_es2_european_supply"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: FES European electricity supply
  summary: >-
    NESO's European electricity supply table (ES2) from its Future Energy Scenarios (FES) and
    2026 Ten-Year Outlook, one file per edition.
  facts:
    vendor: "NESO Data Portal: four CSVs, one per edition, 2023 to 2026"
    cadence: "Ad hoc (NESO); editions 2023 to 2026, as at 6 October 2026"
    grain: "One value per country, EU scenario, variable, technology and year label, per edition"
    history: "NESO created the package on 7 July 2023"
  landscape: power
  what_it_is: >-
    Electricity supply in European countries, by EU scenario and an alignment to FES scenarios or
    pathways. Rows are `Capacity (MW)` or `Demand (TWh)` by category and technology; the unit
    sits in the `Variable` label. Countries are NESO's names, not codes. ES1 is the GB table. The
    package has no definitions file.
  how_used:
    - "Capacity by technology in European countries, under each EU scenario"
    - "European demand beside GB supply from the same FES edition"
    - "Neighbouring countries' capacity set beside GB interconnector flows in ES1"
  chart:
    type: bar
    silver: neso_data_portal/fes_es2_european_supply
    value: value
    filter:
      - {column: edition, op: eq, value: 2025}
      - {column: country, op: eq, value: France}
      - {column: eu_scenario, op: eq, value: EU Green}
      - {column: variable, op: eq, value: Capacity (MW)}
      - {column: subtype, op: eq, value: Nuclear}
      - {column: projection_year, op: in, value: [2030, 2035, 2040, 2045, 2050]}
    dedup: {"on": [resource_id, edition, country, eu_scenario, fes_pathway_alignment, variable, category, type, subtype, projection_year], order_by: capture_written_at}
    group: projection_year
    aggregation: max
    sort: label
    unit: MW
  chart_view:
    title: French nuclear capacity, FES 2025, EU Green
    caption: >-
      Silver `fes_es2_european_supply`, FES 2025 edition (NESO's file last modified 10 December
      2025), EU scenario `EU Green`, aligned by NESO with Holistic Transition and Electric
      Engagement: France, `Capacity (MW)`, `Nuclear`, one row per fifth year label, as written.
    alt: >-
      Horizontal bar chart of NESO's nuclear capacity for France in the FES 2025 edition, EU
      scenario EU Green, in MW, one bar per year label: 2030 63,020; 2035 57,610; 2040 51,550;
      2045 47,195; 2050 44,395. Each label is lower than the one before.
    key:
      - {series: value, label: French nuclear capacity, codes: EU Green, paint: petrol,
         note: "NESO's year labels as written; NESO states no date behind a capacity value"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then four CSVs, downloaded whole when
      `last_modified` changes. 2026 has no rows; NESO replaced its notes file on 9 October 2026.
      Shown: 2023, 2025, 2026.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=fes-european-electricity-supply-data-table-es2"
      - "GET https://api.neso.energy/dataset/bd83ce0b-7b1e-4ff2-89e8-12d524c34d99/resource/6563801b-6da4-46e7-b147-3d81c0237779/download/fes2023_es2_v001.csv"
      - "GET https://api.neso.energy/dataset/bd83ce0b-7b1e-4ff2-89e8-12d524c34d99/resource/fbfdc6c6-52b6-4e3a-96b9-f4e7941f61ec/download/fes2025_es2_v006.csv"
      - "GET https://api.neso.energy/dataset/bd83ce0b-7b1e-4ff2-89e8-12d524c34d99/resource/e8ed65c6-6785-4e2b-84a5-696057f103c9/download/10yo2026_es2_v001.csv"
    commands:
      - {run: gridflow ingest neso_data_portal fes_es2_european_supply --last 24h, comment: "changed CSVs to bronze"}
      - {run: gridflow transform neso_data_portal fes_es2_european_supply --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: edition, op: eq, value: 2025}
        - {column: country, op: eq, value: France}
        - {column: projection_year, op: eq, value: 2036}
        - {column: subtype, op: in, value: [Nuclear, Demand Total (TWh)]}
      dedup: {"on": [resource_id, edition, country, eu_scenario, fes_pathway_alignment, variable, category, type, subtype, projection_year], order_by: capture_written_at}
      order_by: [variable, eu_scenario, fes_pathway_alignment]
      columns: [country, eu_scenario, fes_pathway_alignment, variable, subtype, projection_year, value, category, type,
                edition, resource_id, published_at, timestamp_utc]
    key: [resource_id, edition, country, eu_scenario, fes_scenario_alignment, variable, category, type, subtype,
          subsubtype, fes_pathway_alignment, projection_year]
    caption: "France, FES 2025, label 2036: nuclear capacity per EU scenario, then demand per alignment."
    fields:
      country: "NESO's country or market name, such as `France` or `SEM`; not a code"
      eu_scenario: "NESO's European scenario, such as `EU Green`; names change by edition"
      fes_pathway_alignment: "The FES pathways NESO aligns the row with, 2024 and 2025 files"
      variable: "`Capacity (MW)` or `Demand (TWh)`: the row's measure and unit"
      subtype: "NESO's technology, or `Demand Total (TWh)` on demand rows"
      projection_year: "NESO's year header as an integer; its period or date is not stated"
      value: "NESO's value in the unit named in `variable`; blanks stay blank"
      category: "NESO's group: `Renewable`, `Low Carbon`, `Thermal`, `Storage` or `Demand`"
      type: "NESO's technology type, between category and subtype"
      edition: "The FES edition, from the file name; 2026 has no rows"
      fes_scenario_alignment: "The FES scenarios NESO aligns the row with, 2023 file only"
      subsubtype: "NESO's finest technology split, 2023 file only"
      resource_id: "CKAN file id, one per edition; first column of the entity key"
      published_at: "NESO's last-modified time for the edition's file, read as UTC"
      timestamp_utc: "When gridflow captured the file, UTC; the table has no event time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  caveat: "NESO states no period or date for the year labels, or what blanks mean."
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the `_latest` view, which keeps every edition's file, and pick FES 2025 by `edition`.
    cells:
      - |
        es2 = data.sql("""
            SELECT eu_scenario, projection_year, value
            FROM silver_neso_data_portal_fes_es2_european_supply_latest
            WHERE edition = 2025 AND country = 'France'
              AND variable = 'Capacity (MW)' AND subtype = 'Nuclear'
        """)
        wide = es2.pivot(index="projection_year", columns="eu_scenario", values="value").rename_axis(index=None, columns=None)
        wide.loc[[2030, 2035, 2040, 2045, 2050]]
      - |
        ax = wide.plot(figsize=(9, 3.5), color=["#155A6E", "#8A9A2B", "#B5651D"],
                       xlabel="NESO's year label, as written", ylabel="France nuclear capacity, MW");
      - |
        data.sql("""
            SELECT variable, eu_scenario, fes_pathway_alignment, count(*) AS cells,
                   count(value) AS filled, min(projection_year) FILTER (WHERE value IS NULL) AS first_blank_label
            FROM silver_neso_data_portal_fes_es2_european_supply_latest
            WHERE edition = 2025
            GROUP BY variable, eu_scenario, fes_pathway_alignment
            ORDER BY variable, eu_scenario, fes_pathway_alignment
        """)
    needs: NESO's three FES European electricity supply files from 2023 to 2025
    plot_alt: >-
      Line plot of NESO's nuclear capacity for France in the FES 2025 edition, MW, by year label
      2024 to 2050, one line per EU scenario. All three are 61,370 at label 2024 and 63,020 from
      2025 to 2032, then fall overall. EU Blue and EU Central are equal at every label, 39,595 at
      2050; EU Green ends at 44,395.
  related:
    - {dataset: neso_data_portal/future-energy-scenario-electricity-supply-data-table-es1, note: "The GB counterpart: NESO's FES electricity supply table"}
    - {dataset: neso_data_portal/interconnector-register, note: "NESO's register of GB interconnectors, many to countries listed here"}
    - {dataset: neso_data_portal/fes-electricity-demand-summary-data-table-ed1, note: "NESO's FES GB electricity demand table"}
---

# FES: Pathways to Net Zero – European Electricity Supply Data Table (ES2)

This package is NESO's **Future Energy Scenarios (FES)** European electricity supply data table
(ES2). The package notes say one FES output is "an agreed set of data tables containing the
European electricity supply values". Each CSV is one **edition** of the FES (2023, 2024, 2025;
a fourth, 2026, resource was a notes file until NESO replaced it with a supply table on
2026-10-09, see below). A row is one (country, EU
scenario, FES scenario or pathway alignment, variable, category, type, sub-type[, sub-sub-type])
combination with one value per year column. It is the European counterpart of the GB supply
table @./future-energy-scenario-electricity-supply-data-table-es1.md (ES1): ES1 describes GB
supply, ES2 describes the supply of the European countries listed under Dimensions. The vendor
`Variable` label carries the row's unit in brackets (`Capacity (MW)` or `Demand (TWh)`), so one
year column mixes units by row (see Units). The year headers are the vendor's labels. The period
each label covers (calendar year or other; start or end) and, for capacity, the observation date
are **not established** for the three quantitative editions (`TODO: verify`; see Holds). Some
early year columns may be historical rather than projected, and this page does not establish
whether any column is outturn or projection. Until the hold is answered, do not use the values as
either outturn or a forecast.

gridflow reshapes each wide body into **long rows**: one row per (dimension tuple,
`projection_year`) with a `value`, and it stamps an `edition` from the file name (ADR-042).
Silver holds **67,968 rows from 3 resources** (2023: 22,997 · 2024: 24,640 · 2025: 20,331), of
which **2,608** have a blank (null) `value`. The silver output is **held** (unit E-SEM; see
Holds). **The 2026 resource is held at resource level and has no silver at all**: its body is an
11-row notes table, not the supply table (see Resource detail). On 2026-10-09 NESO replaced that
body with a supply table under the same resource id and file name; gridflow captured it on
2026-10-16, and it stays held at resource level (see "Second 2026 capture"). This note gives
schema, row counts, clocks and missingness; the site page shows the 2023 to 2025 rows, a chart
of one FES 2025 row and a notebook, with one line naming the hold question (ruling 66,
2026-10-24).

Edition is a dimension: **never sum or combine editions.** Each edition is a separate vintage of
the vendor's modelling, not an increment of the previous one. The scenario and pathway columns
are separate columns (the 2023 edition uses `fes_scenario_alignment`, the 2024 and 2025 editions
use `fes_pathway_alignment`), and the EU scenario is a further, independent dimension.

Sibling scenario packages in this vault: @./future-energy-scenario-electricity-supply-data-table-es1.md
(ES1, the GB supply table, same mechanism), @./fes-electricity-demand-summary-data-table-ed1.md
(ED1) and @./future-energy-scenario-fes-building-block-data.md. The ES2 and ES1 bodies have **no
literal row overlap** on their common columns in any edition (FACTS C4b), but that is evidence
against duplicate rows only and does **not** prove the two tables are independent modelling
outputs (`TODO: verify` with NESO).

Supported by National Energy SO Open Data

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| European Electricity Supply Data Table (ES2) 2025 | CSV | upload | `fbfdc6c6-52b6-4e3a-96b9-f4e7941f61ec` |
| European Electricity Supply Data Table (ES2) 2023 | CSV | upload | `6563801b-6da4-46e7-b147-3d81c0237779` |
| European Electricity Supply Data Table (ES2) 2024 | CSV | upload | `7902b197-ada0-47ae-bd2e-db566a8d0fab` |

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| European Electricity Supply Data Table (ES2) 2026 | CSV | upload | `e8ed65c6-6785-4e2b-84a5-696057f103c9` | the 2026 body is an 11-row `Notes`, `Description` notes table, not the European electricity supply table: it has no projection-year columns and no values, so it cannot be an epoch of the unpivot record (V-18); re-disposition only after NESO confirms the resource's intent (DOC or a reference family) or uploads a quantitative ES2 2026 table (a new last_modified) (E-SEM); registry reason, describing the 2026-10-08 capture |

### Resource detail

Package `fes-european-electricity-supply-data-table-es2` (CKAN id
`bd83ce0b-7b1e-4ff2-89e8-12d524c34d99`) has **4 resources**, all CSV, in the 2026-10-06
catalogue snapshot (the vault's earlier snapshot, acquired 2026-08-16 before the 2026 upload,
shows 3). There are no DOC (PDF) resources in this package: **the CSVs carry no definitions**,
and the package gives no companion definitions table. The vendor does publish a per-edition field
dictionary on its portal (2023 and 2024 pages linked under Links); the dictionary describes
`Variable` as the unit used to measure the data point and the year headers as the year of the
data item, without the interval or snapshot date (`TODO: verify` where a 2025 dictionary is
published). `last_modified` is the CKAN value in that snapshot; download links are the snapshot's
resource URLs; `size` is null in the snapshot.

| Edition | Disposition | File | CKAN `last_modified` | Download |
|---|---|---|---|---|
| 2023 | SILVER | `fes2023_es2_v001.csv` | 2023-07-10T03:32:05.482290 | [CSV](https://api.neso.energy/dataset/bd83ce0b-7b1e-4ff2-89e8-12d524c34d99/resource/6563801b-6da4-46e7-b147-3d81c0237779/download/fes2023_es2_v001.csv) |
| 2024 | SILVER | `fes2024_es2_v001.csv` | 2024-07-15T06:30:08.953371 | [CSV](https://api.neso.energy/dataset/bd83ce0b-7b1e-4ff2-89e8-12d524c34d99/resource/7902b197-ada0-47ae-bd2e-db566a8d0fab/download/fes2024_es2_v001.csv) |
| 2025 | SILVER | `fes2025_es2_v006.csv` | 2025-12-10T16:55:04.054020 | [CSV](https://api.neso.energy/dataset/bd83ce0b-7b1e-4ff2-89e8-12d524c34d99/resource/fbfdc6c6-52b6-4e3a-96b9-f4e7941f61ec/download/fes2025_es2_v006.csv) |
| 2026 | HOLD (E-SEM) | `10yo2026_es2_v001.csv` | 2026-09-16T14:33:44.536460 | [CSV](https://api.neso.energy/dataset/bd83ce0b-7b1e-4ff2-89e8-12d524c34d99/resource/e8ed65c6-6785-4e2b-84a5-696057f103c9/download/10yo2026_es2_v001.csv) |

Raw body sizes and rows (FACTS C2): 2023 180,217 bytes / 793 rows; 2024 212,993 / 880;
2025 192,774 / 753; 2026 2,179 / 11. The 2025 resource name carries a leading space in the
catalogue; gridflow keeps the registry name as captured.

- **The edition map is exact.** Only the three file names above (2023-2025) are in the record's
  `edition_by_filename`. An unmapped file name fails loudly rather than being guessed from the
  naming convention (the 2026 file `10yo2026_es2_v001.csv` breaks the `fesYYYY_` pattern). The
  held 2026 resource has no edition entry and is expected by no completion check. The version
  tokens (`v001`, `v006`) show NESO re-uploads within an edition under the same resource slot;
  gridflow keys the edition on the file name, not on the token.
- **Why 2026 is held.** The 2026 body, as captured 2026-10-08, is an 11-row table with columns `Notes` and
  `Description`: it has no projection-year columns and no values, so it cannot be an epoch of the
  unpivot record (ADR-042 V-18, which requires every epoch to output `projection_year` and
  `value`). Inventing those columns would misrepresent the source. Yet the catalogue's resource
  description says the file holds "the European electricity supply values" for the Ten-Year
  Outlook, so this reads as a mismatch between description and body: whether NESO intends a notes
  resource or uploaded the wrong file is the third part of the hold question. Per the FACTS
  read, the notes text itself states annual capacity snapshots on the first of January and
  calendar-year generation and demand values for the notes' stated scope. That is primary text in
  the 2026 notes only; it does **not** establish the same conventions for the 2023-2025 tables
  (`TODO: verify`). The 2026 notes are captured in bronze but never transformed, and are not
  reproduced here. Re-disposition is possible as DOC or as a separate reference family if NESO
  confirms the intent, or as an epoch if NESO uploads a quantitative table (a new
  `last_modified`). Ruling 822: held at resource level, no engine change.
- **Second 2026 capture (checked 2026-10-24 against bronze).** The 2026-10-16 capture
  (`raw_20261016T203342Z_e8ed65c6-…_9558b894.csv`, 32,362 bytes) carries CKAN `last_modified`
  `2026-10-09T09:33:06.347834`: NESO replaced the notes body with a quantitative supply table,
  the condition the hold names. Header: `Country`, `EU Scenario`, `FES Scenario Alignment`,
  `Variable`, `Category`, `Type`, `SubType`, then `2024` to `2050` (27 year columns); 199 data
  rows, 17 countries, one EU scenario label (`EU Central`), `FES Scenario Alignment` blank on
  every row, `Capacity (MW)` 182 rows and `Demand (TWh)` 17. Non-blank cells sit only under
  `2025` to `2036`; every one is a plain number (2,388), and 2,985 cells are blank. No BOM; CRLF.
  The header matches none of the three recorded epochs (epoch 1 has `SubSubType` and starts at
  2022; epochs 2 and 3 have `FES Pathway Alignment`), and two dimension tuples repeat with
  different values (`France` and `Italy`, `Capacity (MW)` / `Other` / `Other` / `Other`), so the
  current duplicate guard would also reject it. The registry disposition and reason still
  describe the notes body; the resource stays `HOLD` and untransformed. `TODO: verify`
  re-disposition (a new epoch, and NESO's word on the repeated tuples) at the next registry edit.
  The replaced notes body is kept in the 2026-10-08 bronze capture.
- All four CSVs were probed in full against the captured bronze bodies (FACTS SCN-2). Every body
  decodes strictly as UTF-8; the 2024 file carries a UTF-8 BOM that the reader handles. Every
  body parses with no ragged rows, and no repair of source bytes is applied.

## Families

### `fes_es2_european_supply`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Country | `country` | string | — | no | — | — |
| EU Scenario | `eu_scenario` | string | — | no | — | — |
| FES Scenario Alignment | `fes_scenario_alignment` | string | — | yes | — | — |
| Variable | `variable` | string | — | no | — | — |
| Category | `category` | string | — | no | — | — |
| Type | `type` | string | — | no | — | — |
| SubType | `subtype` | string | — | yes | — | — |
| SubSubType | `subsubtype` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Country | `country` | string | — | no | — | — |
| EU Scenario | `eu_scenario` | string | — | no | — | — |
| FES Pathway Alignment | `fes_pathway_alignment` | string | — | yes | — | — |
| Variable | `variable` | string | — | no | — | — |
| Category | `category` | string | — | no | — | — |
| Type | `type` | string | — | no | — | — |
| SubType | `subtype` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Country | `country` | string | — | no | — | — |
| EU Scenario | `eu_scenario` | string | — | no | — | — |
| FES Pathway Alignment | `fes_pathway_alignment` | string | — | yes | — | — |
| Variable | `variable` | string | — | no | — | — |
| Category | `category` | string | — | no | — | — |
| Type | `type` | string | — | no | — | — |
| SubType | `subtype` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 3: `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `country`, `eu_scenario`, `fes_scenario_alignment`, `variable`, `category`, `type`, `subtype`, `subsubtype`, `fes_pathway_alignment`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_es2_v001.csv` → 2023; `fes2024_es2_v001.csv` → 2024; `fes2025_es2_v006.csv` → 2025
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### Dimensions

Dimension cardinalities per edition (count of distinct non-null labels in silver, no label
values; absent columns noted):

| Edition | `country` | `eu_scenario` | scenario or pathway alignment | `variable` | `category` | `type` | `subtype` | `subsubtype` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2023 | 18 | 2 | 2 (`fes_scenario_alignment`) | 2 | 5 | 16 | 23 | 40 |
| 2024 | 18 | 2 | 4 (`fes_pathway_alignment`) | 2 | 5 | 16 | 19 | no column |
| 2025 | 17 | 3 | 7 (`fes_pathway_alignment`) | 2 | 5 | 16 | 21 | no column |

Wide-row counts (distinct dimension tuples, one per body row) are 793 for 2023, 880 for 2024 and
753 for 2025; times the number of year columns (29, 28, 27) they give the silver row counts.
The `fes_scenario_alignment` and `subsubtype` columns exist only in the 2023 epoch, and
`fes_pathway_alignment` only in the 2024 and 2025 epochs; in silver the absent columns are null
(`fes_scenario_alignment` is null on all 2024 and 2025 rows, `fes_pathway_alignment` on all 2023
rows). Scenario (a 2023 column) and pathway (a 2024 and 2025 column) are kept as separate columns
and are not merged: a pathway label is not a proven alias of a scenario label (`TODO: verify`
with NESO).

`country` holds NESO's literal names, **not ISO codes**, and gridflow does not normalise them.
The names observed across the editions are Austria, Belgium, Czech Republic, Denmark, Finland,
France, Germany, Ireland (IAI), Italy, Luxembourg, Netherlands, Norway, Poland, Portugal,
Slovenia, Spain, Sweden, Switzerland. The 2023 edition uses `Ireland (IAI)`; the 2024 edition
uses `SEM` in its place (the same list otherwise), and the 2025 edition has the 2024 list without
Luxembourg. `Ireland (IAI)` and `SEM` are not proven to cover the same territory (`TODO: verify`
with NESO the scope of each and any prescribed external code standard). The EU scenario and the
alignment strings are literal dimensions; a comma-containing alignment value is a single CSV
cell, not a declaration to expand one observation into several scenarios.

#### Clocks

Two clocks, separate and not to be mixed (ADR-030, ADR-042):

1. **Vintage (`published_at` = `available_at`):** the CKAN `last_modified` of the captured
   resource (registry `vintage: ckan_last_modified`). It is when NESO last changed that file, not
   when the vendor generated the values. Verified in silver: `published_at` equals
   `available_at` on every row.
   - 2023: 2023-07-10T03:32:05.482290Z
   - 2024: 2024-07-15T06:30:08.953371Z
   - 2025: 2025-12-10T16:55:04.054020Z
2. **Event time:** the temporal recipe is **`none`**. A projection year is a vendor header label,
   not a dated instant, so there is no row-level event time. `timestamp_utc` (and `event_time`,
   which equals it on every row, verified in silver) is the **capture time** of the bronze file,
   here 2026-10-08 about 10:55 UTC (the three captures within about six seconds). It carries no
   information about the year a value covers. The period a label covers is held (see Holds);
   `projection_year` is only the vendor's header label as an integer. The transform window was
   2026-10-08, and that run wrote the first silver for this family.

`edition` is stamped from the file name, independent of both clocks; it is not an issue time.
Point-in-time queries bound `available_at <= as_of` per capture (RULINGS 597, the available-at
cutoff); that bound is on the vintage clock, not on the capture time. Selection is
`whole_capture` per `resource_id` (ADR-039, ADR-042), so each edition keeps its own latest
capture and a newer edition never displaces an older one. Every file was captured on 2026-10-08,
after its `last_modified`, so `available_at <= as_of` is not proof that the bytes held now were
the bytes captured by then (ADR-039 FM-12). `TODO: verify` whether NESO edits a file in place
without bumping `last_modified`; nothing here shows it either way.

#### Units

The unit is **inside the `Variable` label**, in brackets, and gridflow keeps `variable` verbatim
with no unit column and no conversion. The same year column therefore mixes units by row; no
single unit annotation is valid for a column, and a unit must never be inferred from a column
name. The vendor's ES2 dictionaries describe `Variable` as the unit used to measure the data
point (FACTS g4, citing the NESO 2023 and 2024 ES2 dictionaries). Only two labels occur, in
every quantitative edition:

| `variable` label | Unit in the label | Wide rows (2023 / 2024 / 2025) |
|---|---|---|
| `Capacity (MW)` | MW | 757 / 808 / 668 |
| `Demand (TWh)` | TWh | 36 / 72 / 85 |

Filter by `variable` before aggregating, and never sum across the two labels. What `Capacity`
and `Demand` measure for each category, type and sub-type, the observation date of a capacity
value and the interval of a demand value are not defined in the CSVs (`TODO: verify` with NESO;
part of the hold question).

#### Missing values and sentinels

- **Blank year cells are kept as null `value`**, never replaced by zero (2,608 rows: 2023: 2,351;
  2024: 2; 2025: 255). What a blank means (not modelled, not applicable, unavailable or other) is
  part of the hold question; the CSVs do not say, and neither position nor frequency establishes
  it (`TODO: verify`). Zero is a real value and is kept as zero.
- The blanks are structured. In the 2023 file every year column has between 39 and 132 blank
  cells (all in `Capacity (MW)` rows in silver); the 2024 file has exactly one blank cell in each
  of the `2023` and `2024` columns (both `Capacity (MW)`); the 2025 file has 17 blank cells in
  each year column from 2036 to 2050 (all `Demand (TWh)` rows in silver). A header year must
  therefore not be read as proof that a projection exists for it.
- `SubType` and `SubSubType` are blank in 36 wide rows of the 2023 file (the `Demand (TWh)`
  rows; 1,044 long rows), and in no row of the 2024 and 2025 files. The 2024 and 2025 files have
  no `SubSubType` column. `Country`, `EU Scenario`, `Variable`, `Category` and `Type` are never
  blank. Valid rows are kept; a blank lower-level dimension never excludes a row.
- Every non-blank year cell in the three SILVER bodies casts strictly to `Float64` (0 failures);
  no null-token or whitespace rule is applied. The whole-cell tokens `-`, `N/A`, `NA`, `n/a`,
  `#N/A`, `NULL`, `null` and `NaN` occur **zero times in any column** of any ES2 body, so there
  is no literal sentinel in this package. Dictionary text saying `N/A` is metadata, not a body
  sentinel.
- Silver has no NaN in `value`. The long-key duplicate guard found zero duplicated tuples in
  every quantitative body, but no source inspected declares the composite key: the entity key is
  a measured guard key, not a vendor-declared identity (`TODO: verify` with NESO).
- The held 2026 body is not in silver and is not reproduced here.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

One CSV per annual FES edition, so a new resource appears about once a year (editions in the
snapshot: 2023 to 2026). Each resource was captured on 2026-10-08; the 2026 resource was
captured again on 2026-10-16 after NESO replaced its body on 2026-10-09 (see Resource detail),
the only second capture in this package so far. Package
`metadata_modified` in the 2026-10-06 snapshot is 2026-09-16T14:33:44.601325. The version tokens
in the file names show NESO re-uploads files within an edition; the vendor does not publish a
revision policy. `TODO: verify` whether a published edition file is revised in place. Only a
changed `last_modified` across successive captures can show it, and the registry captured each
resource once so far. Activation receipt: transform window 2026-10-08, 0 failures; the reconcile
at cutoff 2026-10-13 had 0 gaps (RESULTS SCN-2a, RULINGS 827).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_es2_european_supply`: held: TODO: For each quantitative ES2 edition, what interval does `Demand (TWh)` cover, and what observation date does `Capacity (MW)` represent? Does a year label denote the starting or ending year? What does a blank projection cell mean? Is `10yo2026_es2_v001.csv` intentionally a notes resource, or was the European electricity supply table replaced by an incorrect upload? Please identify or republish the quantitative European supply resource for this edition. (unit E-SEM)

The silver output exists on disk (67,968 rows, 2023 to 2025) but is **held**: gridflow's models
may not use it for point-in-time work until unit E-SEM answers the question above (held
at activation, RULINGS 827). The registry carries `eligible` at package level and `held` at
family level (gridflow `@docs/neso_data_portal/eligibility.md`); the family status governs the
silver output. The hold has three parts:

1. **What a year header denotes (all quantitative editions).** `projection_year` is the vendor's
   header label as an integer. For each quantitative edition: what interval does `Demand (TWh)`
   cover, and what observation date does `Capacity (MW)` represent? Does a year label denote the
   starting or ending year? The period is not stated in the CSVs or in the dictionaries captured.
   The matching-edition FES Data Workbook notes might say; the FACTS research could not read them
   (the workbook downloads were rejected as unsupported content), so this stays
   `TODO: verify` with NESO.
2. **What a blank projection cell means.** 2,608 blank cells are kept as null (see Missing
   values); the meaning (unmodelled, unavailable, inapplicable or other) is undocumented, and
   neither the blank tails nor any zero value justify substitution, extrapolation or omission.
3. **What the 2026 resource is.** Is `10yo2026_es2_v001.csv` intentionally a notes resource, or
   was the European electricity supply table replaced by an incorrect upload? NESO is asked to
   identify or republish the quantitative European supply resource for this edition. If the
   notes are intentional, NESO is asked for their scope and their relationship to the earlier ES2
   tables. The resource is held at resource level (no silver) until then. NESO replaced the
   notes with a supply table on 2026-10-09 (captured 2026-10-16,
   see Resource detail); the resource stays held until gridflow re-dispositions it, and the
   replacement repeats two dimension tuples with different values.

Settles it: a NESO statement of the period each year label covers per edition (and the
observation date of a capacity value), a meaning for a blank cell, and either a quantitative
ES2 2026 upload or a confirmation that the 2026 file is a notes resource (then DOC disposition or
a reference family). The site page shows the 2023 to 2025 rows, read through the `_latest`
silver view, with one line naming the year-label and blank-cell questions (ruling 66,
2026-10-24). Until the hold lifts, gridflow gold does not read this family (no gold view or gridflow_models consumer for this
package; RULINGS 611 applies the same decision to the sibling SCN docs-wave packages).

## Links

- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/fes-european-electricity-supply-data-table-es2.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- ADRs: gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (clocks),
  `@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md` (records and holds),
  `@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md` (per-resource `_latest`),
  `@docs/DECISION_LOG/ADR-042-neso-scenario-unpivot-and-edition.md` (unpivot and edition)
- Package page: [NESO Data Portal – ES2](https://www.neso.energy/data-portal/fes-european-electricity-supply-data-table-es2)
- Vendor field dictionaries: [2023 ES2 dictionary](https://www.neso.energy/data-portal/fes-european-electricity-supply-data-table-es2/european_electricity_supply_data_table_es2_2023), [2024 ES2 dictionary](https://www.neso.energy/data-portal/fes-european-electricity-supply-data-table-es2/european_electricity_supply_data_table_es2_2024)
- FES workbooks (not yet inspected): [NESO FES documents](https://www.neso.energy/publications/future-energy-scenarios-fes/fes-documents)
- Sibling page: @./future-energy-scenario-electricity-supply-data-table-es1.md
- Vendor README: @../README.md
