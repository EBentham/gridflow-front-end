---
source: "neso_data_portal"
package: "fes-flexibility-data-table-data-table-flx1"
dataset_key: "fes_flx1_flexibility"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: "NESO states no period for the year labels, or what blanks mean; 2023 numbers carry spaces."
  title: FES flexibility data
  summary: >-
    NESO's GB electricity system flexibility table (FLX1) from its Future Energy Scenarios (FES)
    and 2026 Ten-Year Outlook, one file per edition.
  facts:
    vendor: "NESO Data Portal: four CSVs, one per edition, 2023 to 2026"
    cadence: "Ad hoc (NESO); editions 2023 to 2026, as at 6 October 2026"
    grain: "One value per item, detail, unit, scenario or pathway and year label, per edition"
    history: "NESO created the package on 7 July 2023"
  landscape: power
  what_it_is: >-
    NESO's GB flexibility on the supply and demand sides: storage capacity and energy,
    dispatchable supply, demand side response, vehicle to grid, electrolysis and interconnectors.
    Each row names its unit, GW, GWh or TWh; interconnectors use both GW and TWh. The `Detail`
    column splits each item, for example storage by technology. The package has no definitions
    file.
  how_used:
    - "GB storage, demand side response and vehicle to grid under each FES pathway"
    - "Flexibility beside FES supply and demand from the same edition"
    - "Interconnector capacity and annual flows in each scenario or pathway"
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then four CSVs, each downloaded whole unless its
      `last_modified` is unchanged. Shown: 2023, 2024, 2026.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=fes-flexibility-data-table-data-table-flx1"
      - "GET https://api.neso.energy/dataset/2e3275e2-dd6a-4c2e-8cfb-eeb9b4320dcb/resource/e86745fd-1ef2-4112-a14c-84682a387b68/download/fes2023_flx1_v001.csv"
      - "GET https://api.neso.energy/dataset/2e3275e2-dd6a-4c2e-8cfb-eeb9b4320dcb/resource/c7d7a19d-255f-4585-b53b-487891aeda54/download/fes2024_flx1_v003.csv"
      - "GET https://api.neso.energy/dataset/2e3275e2-dd6a-4c2e-8cfb-eeb9b4320dcb/resource/0ff1a94f-224d-4863-8137-7d9a0d2cd7f8/download/10yo2026_flx1_v001.csv"
    commands:
      - {run: gridflow ingest neso_data_portal fes_flx1_flexibility --last 24h, comment: "changed CSVs to bronze"}
      - {run: gridflow transform neso_data_portal fes_flx1_flexibility --last 24h, comment: "the capture's date to silver"}
  related:
    - {dataset: neso_data_portal/future-energy-scenario-electricity-supply-data-table-es1, note: "NESO's FES electricity supply table, including storage and interconnectors"}
    - {dataset: neso_data_portal/fes-electricity-demand-summary-data-table-ed1, note: "NESO's FES electricity demand table, by component and scenario"}
    - {dataset: neso_data_portal/regional-breakdown-of-fes-data-electricity, note: "FES by grid supply point, with demand side response and storage"}
    - {dataset: neso_data_portal/demand-flexibility, note: "NESO's Demand Flexibility Service, demand side response it buys"}
---

# FES: Pathways to Net Zero – Flexibility Data table (FLX1)

This package is NESO's **Future Energy Scenarios (FES)** flexibility table (FLX1). The package
notes say one FES output is "an agreed set of data tables containing the GB FES values for the
electricity system flexibility". Each CSV is one **edition** (2023, 2024, 2025, and a 2026 file
whose name starts `10yo2026`; the 2026 resource description calls it a Ten-Year Outlook output,
not an FES output). Each row is one combination of flexibility type, sub-type, data item, unit,
scenario or pathway, fuel and detail, with one value per year column. The data items are
electricity storage connection capacity, electricity storage energy storage potential,
dispatchable electricity supply capacity, demand side response, vehicle to grid, demand,
electrolysis (installed electric capacity), interconnectors and (2025 and 2026 only) total
consumer led flexibility. The vendor `Unit` column names each row's unit, and it is **not one
unit for the family**: it is GW, GWh or TWh row by row.

gridflow reshapes each wide body into **long rows**: one row per (dimension tuple,
`projection_year`) with a `value`, and stamps an `edition` from the file name (ADR-042). Silver
holds **11,382 rows from 3 resources** (2024: 5,550 · 2025: 4,860 · 2026: 972), of which
**1,848** have a blank (null) `value`. The 2023 resource is a resource-level **HOLD** (padded
numbers fail the strict cast, below) and has **no silver rows**. The family itself is **held**
(unit E-SEM, see Holds): the period each year label denotes and the meaning of a blank cell are
not established. This page therefore gives schema, row counts, clocks and missingness only,
never data values, samples or ranges of values.

Sibling scenario packages in this vault: @./fes-electricity-demand-summary-data-table-ed1.md,
@./fes-european-electricity-supply-data-table-es2.md,
@./fes-road-transport-summary-data-table-ed5.md and @./fes-road-transport-notes-data-table-ed6.md.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Flexibility data table (FLX1) 2024 | CSV | upload | `c7d7a19d-255f-4585-b53b-487891aeda54` |
| Flexibility data table (FLX1) 2025 | CSV | upload | `299bc6c8-7608-4946-ab0a-5bc22129c897` |
| Flexibility data table (FLX1) 2026 | CSV | upload | `0ff1a94f-224d-4863-8137-7d9a0d2cd7f8` |

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Flexibility data table (FLX1) 2023 | CSV | upload | `e86745fd-1ef2-4112-a14c-84682a387b68` | the 2023 body fails the strict float64 cast on 1152 projection cells, every one a number with trailing ASCII spaces (e.g. `6.06 `; 45 per column 2021-2028, 36 per column 2029-2050) and an unpivot value has no trim declaration (`ValueSpec` has no `trim`); re-disposition only after a declared unpivot-value trim mechanism or a corrected NESO upload (a new last_modified) (E-SEM) |

### Resource detail

Package `fes-flexibility-data-table-data-table-flx1` (CKAN id
`2e3275e2-dd6a-4c2e-8cfb-eeb9b4320dcb`) has **4 resources** in the 2026-10-06 catalogue
snapshot, all CSV, all `url_type: upload`; there are no DOC resources. `last_modified` is the
CKAN value in that snapshot. Download links are the snapshot's resource URLs; `size` is null in
the snapshot. Edition comes from the exact file name, which agrees with the resource name; the
modification year is not the edition (the 2024 file was last modified in 2025).

| Edition | Disposition | File | CKAN `last_modified` | Wide rows | Download |
|---|---|---|---|---:|---|
| 2023 | HOLD | `fes2023_flx1_v001.csv` | 2023-07-10T03:27:12.556782 | 185 | [CSV](https://api.neso.energy/dataset/2e3275e2-dd6a-4c2e-8cfb-eeb9b4320dcb/resource/e86745fd-1ef2-4112-a14c-84682a387b68/download/fes2023_flx1_v001.csv) |
| 2024 | SILVER | `fes2024_flx1_v003.csv` | 2025-06-27T09:22:49.054408 | 185 | [CSV](https://api.neso.energy/dataset/2e3275e2-dd6a-4c2e-8cfb-eeb9b4320dcb/resource/c7d7a19d-255f-4585-b53b-487891aeda54/download/fes2024_flx1_v003.csv) |
| 2025 | SILVER | `fes2025_flx1_v006.csv` | 2025-12-10T17:00:25.208610 | 180 | [CSV](https://api.neso.energy/dataset/2e3275e2-dd6a-4c2e-8cfb-eeb9b4320dcb/resource/299bc6c8-7608-4946-ab0a-5bc22129c897/download/fes2025_flx1_v006.csv) |
| 2026 | SILVER | `10yo2026_flx1_v001.csv` | 2026-09-16T14:35:58.106567 | 36 | [CSV](https://api.neso.energy/dataset/2e3275e2-dd6a-4c2e-8cfb-eeb9b4320dcb/resource/0ff1a94f-224d-4863-8137-7d9a0d2cd7f8/download/10yo2026_flx1_v001.csv) |

- **The 2026 file is a Ten Year Outlook table.** It is NESO's 2026 Ten Year Outlook output, not
  an FES edition. It carries a single scenario label (`Ten Year Outlook`) and so far fewer rows
  (36 wide rows against 180 or 185). Whether it continues the FES series is not stated.
  `TODO: verify` with NESO.
- **Vendor datastore typing differs from the CSV body.** The CKAN field-info snapshot of the
  2026 resource types the year columns 2037-2050 as text and 2024-2036 as numeric. The 2026 CSV
  body itself casts to `Float64` with zero failures. `TODO: verify` why the datastore types them
  as text; nothing in gridflow reads the datastore.
- File names `v001`, `v003`, `v006` show NESO re-uploads files within an edition. The vendor
  publishes no revision policy. gridflow keys the edition on the file name, not the version token.

## Families

### `fes_flx1_flexibility`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Flexibility type | `flexibility_type` | string | — | no | — | — |
| Flexibility sub-type | `flexibility_sub_type` | string | — | no | — | — |
| Data item | `data_item` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| Pathway | `pathway` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | no | — | — |
| Detail | `detail` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Flexibility type | `flexibility_type` | string | — | no | — | — |
| Flexibility sub-type | `flexibility_sub_type` | string | — | no | — | — |
| Data item | `data_item` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| Pathway | `pathway` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | no | — | — |
| Detail | `detail` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Flexibility type | `flexibility_type` | string | — | no | — | — |
| Flexibility sub-type | `flexibility_sub_type` | string | — | no | — | — |
| Data item | `data_item` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| Scenario | `scenario` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | no | — | — |
| Detail | `detail` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 3: `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `flexibility_type`, `flexibility_sub_type`, `data_item`, `unit`, `scenario`, `fuel`, `detail`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2024_flx1_v003.csv` → 2024; `fes2025_flx1_v006.csv` → 2025; `10yo2026_flx1_v001.csv` → 2026
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### Shape and epoch map

Each silver resource is exactly one header epoch and exactly one edition. Every body has seven
dimension columns, then contiguous year columns. Epoch numbers follow the schema tables above.
The `pathway` and `scenario` columns are separate (the vendor header says `Pathway` in the 2024
and 2025 files and `Scenario` in the 2023 and 2026 files); gridflow does not merge them.

| Epoch | Edition | Resource | Year columns (header labels) | Wide rows | Long rows | Null `value` |
|---|---|---|---|---:|---:|---:|
| 1 | 2024 | `c7d7a19d-…` | 2021–2050 (30) | 185 | 5,550 | 782 |
| 2 | 2025 | `299bc6c8-…` | 2024–2050 (27) | 180 | 4,860 | 552 |
| 3 | 2026 | `0ff1a94f-…` | 2024–2050 (27) | 36 | 972 | 514 |
| | **Total silver** | 3 resources | | 401 | **11,382** | **1,848** |
| — | 2023 (HOLD) | `e86745fd-…` | 2021–2050 (30) | 185 | none (5,550 would-be) | — |

The silver counts equal the activation receipt (RULINGS 827; RESULTS §SCN-2a: FLX1 11,382, 0
failures). The 2023 header (`Scenario` with 2021–2050) matches none of the three recorded
epochs and the resource is excluded from the edition map while held. Its 185 wide rows have
zero duplicated dimension/year tuples before casting (K-SCN-2 FACTS §3).

Populated columns by edition (null in the other editions):

| Silver column | Populated in editions | Null in editions |
|---|---|---|
| `pathway` | 2024, 2025 | 2026 |
| `scenario` | 2026 | 2024, 2025 |

Whether vendor `Pathway` and `Scenario` mean the same thing across editions is **not**
established by the CSVs (the entity key keeps both columns so no row collapses). The label sets
differ by edition (for example the 2026 file has one label, `Ten Year Outlook`, and the 2025 file has a
`Ten Year Forecast` label); do not equate them. `TODO: verify` with NESO before any
cross-edition join on them.

Dimension cardinalities in silver (count of distinct non-null labels, no value statistics):

| Edition | `data_item` | `detail` | `fuel` | scenario or pathway | `unit` |
|---|---:|---:|---:|---:|---:|
| 2024 | 8 | 32 | 5 | 5 | 3 |
| 2025 | 9 | 31 | 4 | 5 | 3 |
| 2026 | 9 | 31 | 4 | 1 | 3 |

`flexibility_type` has one label in every edition (`Electricity system flexibility`); the
sub-types are `Supply side flexibility` and `Demand side flexibility`. The `Detail` cell
separates, for example, storage technologies (total, liquid air, compressed air, batteries,
pumped hydro), demand-side reduction and charging/V2G measures, dispatchable technologies, and
electrolysis connection types. `TODO: verify` the full meaning of each `Detail` label; the CSVs
carry no definitions and no FLX1 definitions resource exists in this package.

#### Clocks

Two clocks, separate and not to be mixed (ADR-030, ADR-042):

1. **Vintage (`published_at` = `available_at`):** the CKAN `last_modified` of the captured
   resource. It is when NESO last changed that file, not when the vendor generated the values.
   Verified in silver: `published_at` equals `available_at` on every row.
   - 2024: 2025-06-27T09:22:49.054408Z
   - 2025: 2025-12-10T17:00:25.208610Z
   - 2026: 2026-09-16T14:35:58.106567Z
   - 2023 (held, no silver): 2023-07-10T03:27:12.556782Z
2. **Event time:** the temporal recipe is **`none`**. A projection year is a vendor header
   label, not a dated instant, so there is no row-level event time. `timestamp_utc` (and
   `event_time`, which equals it on every row) is the **capture time** of the bronze file,
   here 2026-10-08 10:55 UTC (the three silver files captured within about six seconds). It
   carries no information about the year a value covers. The period a label covers is held (see
   Holds); `projection_year` is only the vendor's header label as an integer.

`edition` is stamped from the file name (`edition_by_filename`), independent of both clocks.
It is not an issue time. Point-in-time queries bound `available_at <= as_of` per capture
(RULINGS 597); that bound is on the vintage clock, not on the capture time. Every file here was
captured on 2026-10-08, after its `last_modified`, so `available_at <= as_of` is not proof that
the bytes held now were the bytes captured by then (ADR-039 FM-12). `TODO: verify` whether NESO
edits a file in place without bumping `last_modified`; nothing here shows it either way.

**Editions are a dimension: never sum or merge across editions.** The same
(data item, detail, scenario or pathway, year) can appear in several editions with different
values; they are different publications, not a time series of one forecast.

#### Units

Units come from the vendor's own `Unit` column in each row, never inferred from a column or
data-item name. Observed unit labels, by wide row:

| Edition | GW | GWh | TWh |
|---|---:|---:|---:|
| 2023 (held) | 140 | 25 | 20 |
| 2024 | 145 | 25 | 15 |
| 2025 | 140 | 25 | 15 |
| 2026 | 28 | 5 | 3 |

Observed data-item/unit relationships (K-SCN-2 FACTS §3):

| Data item | Captured unit |
|---|---|
| Electricity storage connection capacity | GW |
| Electricity storage energy storage potential | GWh |
| Dispatchable electricity supply capacity | GW |
| Demand side response | GW |
| Vehicle to Grid | GW |
| Demand | GW |
| Electrolysis (installed electric capacity) | GW |
| Interconnectors | GW for capacity/peak-flow rows; TWh for annual flow rows |
| Total consumer led flexibility (2025 and 2026 only) | GW |

The same `Data item` can carry more than one unit (interconnectors), so `unit` is part of the
entity key and **must be kept** with the value. Never sum `value` across `unit`, across
`data_item`, or across editions. The per-column "Vendor unit" cell above is `—` because the
unit is per row, not per column. The vendor dictionary names the dimensions but does not
define the quantities behind each item; `TODO: verify` the definitions (for example "flexibility
at peak") with NESO.

#### Missing values and sentinels

- **Blank year cells are kept as null `value`**, never replaced by zero (1,848 rows in silver,
  table above). What a blank means (not modelled, not applicable, unavailable) is part of the
  hold question; the CSVs do not say. `TODO: verify`.
- Blank cells by raw column: 2024 file `2021`: 5, `2030`–`2050`: 37 each; 2025 file
  `2030`–`2035`: 2 each, `2036`–`2050`: 36 each; 2026 file `2024`: 10, `2037`–`2050`: 36 each;
  2023 file (held) `2029`–`2050`: 37 each. No other column has a blank cell.
- **No text sentinel is evidenced.** The whole-cell tokens `-`, `N/A`, `NA`, `n/a`, `#N/A`,
  `NULL`, `null` and `NaN` occur zero times in every column of every captured body. No
  null-token rule is applied.
- **Zeros are values**, not nulls. Zero cells occur in every captured body and no source
  inspected identifies them as sentinels. Preserve them. Their counts are not repeated here
  while the family is held.
- **2023 padded numbers (held resource).** 1,152 projection cells in the 2023 body are numbers
  with trailing ASCII spaces and fail the strict cast. The 2024, 2025 and 2026 bodies have zero
  such cells. No bronze byte is repaired and no trim rule is applied (RULINGS 822: no engine
  change). The cause is lexical, so it is not a duplicate-key or decoding failure.
- Every non-blank cell in the 2024, 2025 and 2026 bodies casts strictly to `Float64`; no NaN
  is in silver. The dimension cells are non-null and the full long key is unique in every body
  (zero duplicates; for 2023 the dimension/year tuple, before the value cast). The key is a
  measured guard key, not a vendor-documented identity (`TODO: verify` with NESO).
- Encoding: all bodies decode strictly as UTF-8; the 2024 file carries a UTF-8 BOM, which the
  reader handles. No ragged rows, embedded newlines or comma-bearing cells.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

One CSV per annual edition, so a new resource appears about once a year (editions in the
snapshot: 2023, 2024, 2025, 2026). Each resource was captured once, on 2026-10-08. Package
`metadata_modified` in the 2026-10-06 snapshot is 2026-09-16T14:35:58.177002. The vendor does
not publish a revision policy. `TODO: verify` whether a published edition file is revised in
place; only a changed `last_modified` across successive captures can show it, and each resource
has been captured once so far.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_flx1_flexibility`: held: TODO: For each FLX1 edition and measure, what interval or observation date does its year label denote, including annual interconnector energy, storage energy potential, installed capacity and flexibility at peak? Does a winter-related label identify the starting or ending year? What does a blank projection cell mean? Can NESO republish `fes2023_flx1_v001.csv` without numeric edge whitespace, or will a separately authorized engine change permit explicitly declared ASCII trimming of unpivot values? (unit E-SEM)

The silver output exists on disk (11,382 rows) but is **held**: it is not eligible for
publication or for point-in-time model use until unit E-SEM answers the question above
(held at activation, RULINGS 827). The registry carries `eligible` at package level and `held`
at family level (gridflow `@docs/neso_data_portal/eligibility.md`); the family status governs
the silver output. The hold has three parts:

1. **What a year header denotes.** `projection_year` is the vendor's header label as an
   integer. The period it denotes (an interval or an observation date), and whether the label is
   the start or the end of it, is not stated in the CSVs, per measure and per edition: annual
   interconnector energy, storage energy potential, installed capacity and flexibility at peak
   are all open. Whether a winter-related label names the starting or ending year is also open.
   The vendor dictionaries identify year-of-data labels but do not settle this. The
   matching-edition FES workbook notes are the strongest next source (not inspected).
   `TODO: verify`.
2. **Blank cells.** A blank may mean not modelled, not applicable or something else. gridflow
   keeps null and never converts to zero or fills it.
3. **FLX1 2023 resource.** The 2023 body is a resource-level HOLD (unit E-SEM): padded numbers
   fail the strict `Float64` cast and an unpivot value cannot declare a trim. Re-disposition
   needs either a corrected NESO upload (a new `last_modified`) or a separately authorized
   engine change that declares ASCII trimming of unpivot values. Neither is in scope; the
   2023 bytes stay in bronze unchanged and no silver rows exist for it.

Settles it: a NESO statement (or matching-edition workbook notes) of the period each year label
covers per measure and edition, the meaning of an empty projection cell, and a republished 2023
file without edge whitespace. Until then the page shows no values, samples or statistics of
values, and no gold view or gridflow_models consumer reads this family.

## Links

- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/fes-flexibility-data-table-data-table-flx1.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- ADRs: gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (clocks),
  `@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md` (per-resource `_latest`),
  `@docs/DECISION_LOG/ADR-042-neso-scenario-unpivot-and-edition.md` (unpivot and edition)
- Package page: [NESO Data Portal – FLX1](https://www.neso.energy/data-portal/fes-flexibility-data-table-data-table-flx1)
- 2026 resource page: [Flexibility data table (FLX1) 2026](https://www.neso.energy/data-portal/fes-flexibility-data-table-data-table-flx1/flexibility_data_table_flx1_2026)
- FES documents (workbooks): [NESO FES documents](https://www.neso.energy/publications/future-energy-scenarios-fes/fes-documents)
- Vendor README: @../README.md
