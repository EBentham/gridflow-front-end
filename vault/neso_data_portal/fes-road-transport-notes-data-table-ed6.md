---
source: "neso_data_portal"
package: "fes-road-transport-notes-data-table-ed6"
dataset_key: "fes_ed6_road_transport_notes"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-14
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# FES: Pathways to Net Zero – Road Transport Notes Data Table (ED6)

This package is the **notes table for NESO's road-transport data** in the Future Energy
Scenarios (FES) series. The package notes say the FES publish "data tables containing the GB
FES values for road transport"; ED6 is the explanatory companion to the ED5 summary table,
not a table of projections. Each CSV is one **edition** of the FES (2023, 2024, 2025, and a
2026 file whose name starts `10yo2026`; the 2026 tables are the Ten Year Outlook). It holds
three string columns and no numbers: `Column` names a column of the ED5 table, `Category`
names a value that appears in that ED5 column, and `Description` explains it (the
descriptions give definitions of vehicle counts, the energy demand items, and peak versus
annual data, with formulas that reference other ED5 items). It is a **codebook for ED5**:
`column_name` and `category` point to an ED5 column and one of that column's values. See
@30-vendors/neso-data-portal/datasets/fes-road-transport-summary-data-table-ed5.md.

gridflow keeps the four files as **reference rows**: no unpivot, no projection year, no
value. Silver holds **106 rows from 4 resources** (2023: 27 · 2024: 27 · 2025: 26 · 2026: 26).
Unlike its ED5 sibling, this family is **eligible** (not held): it carries no numeric
measure and no year label, so the open questions on ED5 (what a year header denotes, what a
blank projection cell means) do not apply to it. The ED5 hold still applies to ED5 itself;
reading an ED6 description does not settle it (see Holds).

**Edition is a dimension.** Each edition is a separate, complete set of notes. Never merge
editions into one codebook, and read a note against the ED5 file of the same edition (see
Join to ED5).

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Road Transport Notes (ED6) 2023 | CSV | upload | `30012023-6c0b-4da5-bd77-4f2b244a950d` |
| Road Transport Notes (ED6) 2024 | CSV | upload | `7fe93ddc-7a88-478b-8f60-4531c15bd538` |
| Road Transport Notes (ED6) 2025 | CSV | upload | `43add83b-bf94-493b-8f5d-de7fdbefc5bb` |
| Road Transport Notes (ED6) 2026 | CSV | upload | `06601add-c47b-427c-bdde-845b270e72e1` |

There are no DOC, catalogue-only or held resources in this package: all four resources are
CSV and all four are transformed to silver.

### Resource detail

Package `fes-road-transport-notes-data-table-ed6` (CKAN id
`5a3b9d32-5da8-4237-8468-dfb7bb4ebe78`) has **4 resources** in the 2026-10-06 catalogue
snapshot (all CSV). `last_modified` is the CKAN value in that snapshot. Download links are
the snapshot's resource URLs; `size` is null in the snapshot.

| Edition | Disposition | File | CKAN `last_modified` | Download |
|---|---|---|---|---|
| 2023 | SILVER | `fes2023_ed6_v001.csv` | 2023-07-10T03:26:39.716174 | [CSV](https://api.neso.energy/dataset/5a3b9d32-5da8-4237-8468-dfb7bb4ebe78/resource/30012023-6c0b-4da5-bd77-4f2b244a950d/download/fes2023_ed6_v001.csv) |
| 2024 | SILVER | `fes2024_ed6_v001.csv` | 2024-07-15T06:41:16.480938 | [CSV](https://api.neso.energy/dataset/5a3b9d32-5da8-4237-8468-dfb7bb4ebe78/resource/7fe93ddc-7a88-478b-8f60-4531c15bd538/download/fes2024_ed6_v001.csv) |
| 2025 | SILVER | `fes2025_ed6_v006.csv` | 2025-12-10T17:02:44.975794 | [CSV](https://api.neso.energy/dataset/5a3b9d32-5da8-4237-8468-dfb7bb4ebe78/resource/43add83b-bf94-493b-8f5d-de7fdbefc5bb/download/fes2025_ed6_v006.csv) |
| 2026 | SILVER | `10yo2026_ed6_v001.csv` | 2026-09-16T15:01:14.222912 | [CSV](https://api.neso.energy/dataset/5a3b9d32-5da8-4237-8468-dfb7bb4ebe78/resource/06601add-c47b-427c-bdde-845b270e72e1/download/10yo2026_ed6_v001.csv) |

- **Edition comes from the file name, corroborated by the resource name.** Each file name and
  its catalogue resource name (`Road Transport Notes (ED6) <year>`) agree on the year.
  gridflow stamps `edition` from the file name (`edition_by_filename`), not from
  `last_modified`, the version token or the capture date.
- **The version token differs by file** (`v001`, `v001`, `v006`, `v001`), which shows NESO
  re-uploads files under the same slot (the 2025 file is at `v006`). The vendor publishes no
  revision policy; `TODO: verify` whether a published edition is revised in place.
- **The 2023 file carries nine blank separator rows** (see Missing values).

## Families

### `fes_ed6_road_transport_notes`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1 (one header, identical in all four files):

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Column | `column_name` | string | — | no | — | — |
| Category | `category` | string | — | no | — | — |
| Description | `description` | string | — | no | — | — |

Silver also carries the standard provenance columns written to every silver row: `edition`
(int64), `resource_id`, `timestamp_utc`, `published_at`, `available_at`, `event_time`,
`bronze_capture_id`, `capture_written_at`, `source_run_id`, `dataset_version` (the value is
`1+e1` on every row: record version 1, epoch 1). None is null.

- Entity key: `resource_id`, `edition`, `column_name`, `category`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_ed6_v001.csv` → 2023; `fes2024_ed6_v001.csv` → 2024; `fes2025_ed6_v006.csv` → 2025; `10yo2026_ed6_v001.csv` → 2026
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### Shape and counts

Each resource is exactly one header epoch and exactly one edition. Counts are from the
2026-10-08 silver (matching the activation receipt, RULINGS 827) and the pre-merge profile.

| Edition | Resource | Raw data rows | Blank separator rows removed | Silver rows | Cells with an embedded newline | Cells with a comma |
|---|---|---:|---:|---:|---:|---:|
| 2023 | `30012023-…` | 36 | 9 | 27 | 0 | 5 |
| 2024 | `7fe93ddc-…` | 27 | 0 | 27 | 19 | 5 |
| 2025 | `43add83b-…` | 26 | 0 | 26 | 19 | 8 |
| 2026 | `06601add-…` | 26 | 0 | 26 | 19 | 10 |
| | **Total** | | **9** | **106** | | |

(Embedded-newline and comma counts are over all parsed cells of the body; the silver
`description` column holds the newlines in each of 2024-2026.) Every file decodes strictly as
UTF-8; the 2024 file starts with a byte-order mark, which the reader handles.

Distinct labels per edition (count of distinct `column_name` values, and rows per
`column_name`):

| Edition | `Data Item` rows | `Fuel` rows | `Peak/Annual/Minimum` rows |
|---|---:|---:|---:|
| 2023 | 22 | 2 | 3 |
| 2024 | 22 | 2 | 3 |
| 2025 | 22 | 2 | 2 |
| 2026 | 22 | 2 | 2 |

Every `column_name` is one of those three labels (the spelling is `Data Item` with a capital
I; the ED5 header spells it `Data item`, see Join to ED5). Every `(column_name, category)`
pair is unique in every edition (zero duplicate keys). Descriptions run from 43 to 486
characters, none null.

What changed between editions (labels only):

- The 22 `Data Item` rows and the 2 `Fuel` rows have the same category labels in all four
  editions (one `Data Item` label has a trailing space in every edition and is kept as
  received).
- The `Peak/Annual/Minimum` rows differ: the 2023 and 2024 files list the categories
  `# Vehicles`, `Peak` and `Reference data`; the 2025 and 2026 files list `Annual` and `Peak`.
  The `# Vehicles` and `Reference data` rows have no counterpart in the later files, and
  `Annual` has none in the earlier ones. Whether the later `Annual` note replaces the earlier
  `# Vehicles` note is `TODO: verify` with NESO; gridflow does not map one to the other.
- The description text of a given category is revised between editions (for example the
  2024-2026 versions of some descriptions run across several lines where the 2023 text is one
  line). gridflow keeps each edition's text as published and does not diff them.

#### Silver sample

Two silver rows from the 2025 edition (provenance columns omitted; the vendor `description`
is truncated here for the page and is longer in silver):

```python
[
    {"edition": 2025, "column_name": "Data Item", "category": "# Cars - All",
     "description": "All cars (as defined by DfT/DVLA ...). History from Vehicle licensing data tables - VEH0101. ..."},
    {"edition": 2025, "column_name": "Peak/Annual/Minimum", "category": "Peak",
     "description": "Data representing demand or available capacity, applicable at the time of transmission system peak (5pm-6pm)"},
]
```

#### Clocks

Two clocks, separate and not to be mixed (ADR-030, ADR-042):

1. **Vintage (`published_at` = `available_at`):** the CKAN `last_modified` of the captured
   resource. It is when NESO last changed that file, not when the vendor wrote the notes.
   Verified in silver: `published_at` equals `available_at` on every row.
   - 2023: 2023-07-10T03:26:39.716174Z
   - 2024: 2024-07-15T06:41:16.480938Z
   - 2025: 2025-12-10T17:02:44.975794Z
   - 2026: 2026-09-16T15:01:14.222912Z
2. **Event time:** the temporal recipe is **`none`**. These are reference notes with no
   dated instant, so there is no row-level event time. `timestamp_utc` (and `event_time`,
   which equals it on every row) is the **capture time** of the bronze file, here
   2026-10-08 10:54:43 UTC (2023), 10:54:46 (2024), 10:54:48 (2025) and 10:54:51 (2026). It
   carries no information about the date a note applies to.

`edition` is stamped from the file name, independent of both clocks; it is not an issue time.
Point-in-time queries bound `available_at <= as_of` per capture; that bound is on the
vintage clock, not on the capture time. Every file was captured on 2026-10-08, after its
`last_modified`, so `available_at <= as_of` does not prove that the bytes held now were the
bytes NESO published by then (ADR-039); `TODO: verify` whether NESO edits a file in place
without bumping `last_modified`. Nothing here shows it either way.

#### Units

None. ED6 has no numeric column and no unit column. A description may name a quantity (for
example data items whose names start `TWh` or `#`), but a unit is taken only from the vendor
dictionary, never inferred from a data-item name. The unit of an ED5 value is the `Unit`
column of that ED5 row.

#### Missing values and sentinels

- **Blank separator rows.** The 2023 body contains nine rows in which every cell is blank.
  The reader drops all-blank rows before casting (a logged, documented rule), so the
  36 raw data rows become 27 silver rows. This is not deduplication: no populated row is
  dropped, no occurrence index is added, and the 27 retained rows match the CSV exactly.
- **No sentinels.** The tokens `-`, `N/A`, `NA`, `n/a` (and `#N/A`, `NULL`, `null`, `NaN`) occur
  zero times in any ED6 cell. There is no null-token rule and no whitespace trim on cell
  values. Silver has no null in any column. The word `N/A` in a vendor dictionary page is
  metadata, not a body sentinel.
- **No numeric zeros or blank projection cells.** The "blank projection cells are null,
  zeros are values" rule of the other SCN pages has nothing to apply to here: there are no
  projection cells.

#### Join to ED5

`column_name` and `category` are meant to point at an ED5 column and one of its values, and
the descriptions reference ED5 items in square brackets. The join is **not literal**:

- `column_name` is `Data Item`, `Fuel` or `Peak/Annual/Minimum`. The ED5 header spells them
  `Data item`, `Fuel` and `Peak/Annual/Minimum` (silver `data_item`, `fuel`,
  `peak_annual_minimum`), so `Data Item` needs a case-insensitive match to `Data item`.
- Measured on 2026-10-08 silver labels, comparing `category` with the distinct labels of the
  same-edition ED5 column (labels only, no ED5 values): of the 22 `Data Item` rows, 22 (2023)
  or 21 (2024, 2025, 2026) match an ED5 `data_item` label exactly; 1 of the 2 `Fuel` rows
  matches an ED5 `fuel` label in every edition; of the `Peak/Annual/Minimum` rows, 1 of 3
  (2023, 2024) or 2 of 2 (2025, 2026) match. The unmatched labels differ by exact string; the
  cause (whitespace, wording, or a note with no ED5 counterpart) was not investigated.
  `TODO: verify` before treating ED6 as a complete key to ED5.
- Join on edition: an ED6 row of one edition describes the ED5 file of the same edition. Do
  not apply a 2025 note to 2023 data.

ED5 carries a hold (unit E-SEM) on what its year labels and blank cells mean; the ED6 notes
describe ED5's items but do not answer that question.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

One CSV per annual FES edition, so a new resource appears about once a year (editions in the
snapshot: 2023, 2024, 2025, 2026). Each resource was captured once, on 2026-10-08. Package
`metadata_modified` in the 2026-10-06 snapshot is 2026-09-16T15:01:14.299737. The registry
captured each resource once, so a change to a published file's `last_modified` between
captures has not been observed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

The package is `eligible` in the registry and the family is eligible in the eligibility
report (gridflow `@docs/neso_data_portal/eligibility.md`). This is a reference record with no
temporal meaning, so the year-period and blank-cell questions that hold ED5 do not arise
here. Two residual items are not holds:

1. **Vendor uniqueness.** `TODO: verify` that NESO states `(Column, Category)` is unique. The
   entity key is a measured composite (zero duplicates in every edition), not a
   vendor-declared identity. A future repeated populated key fails the duplicate-key guard
   rather than being silently deduplicated.
2. **Join completeness.** See Join to ED5: some labels do not match an ED5 label exactly.

No gold view or gridflow_models consumer reads this family (RULINGS 555: no gold feed for
the docs wave of this package).

## Links

- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/fes-road-transport-notes-data-table-ed6.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- Reader (blank-row rule): gridflow `@src/gridflow/silver/csv_bronze.py`
- ADRs: gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (clocks),
  `@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md` (records and holds),
  `@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md` (per-resource `_latest`),
  `@docs/DECISION_LOG/ADR-042-neso-scenario-unpivot-and-edition.md` (edition)
- Sibling (the table these notes explain): @30-vendors/neso-data-portal/datasets/fes-road-transport-summary-data-table-ed5.md
- Package page: [NESO Data Portal – ED6](https://www.neso.energy/data-portal/fes-road-transport-notes-data-table-ed6)
- Vendor README: @../README.md
