---
source: "neso_data_portal"
package: "fes-electricity-demand-summary-data-table-ed1"
dataset_key: "fes_ed1_electricity_demand"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# FES: Pathways to Net Zero – Electricity Demand Summary Data table (ED1)

This package is NESO's **Future Energy Scenarios (FES)** electricity-demand summary table
(ED1). The package notes say one FES output is "an agreed set of data tables containing the
GB FES values for electricity demand". Each CSV is one **edition** of the FES (2023, 2024,
2025, and a 2026 file whose name starts `10yo2026`). It lists, for each demand item
(`Data item`), one value per year column under several named scenarios or pathways. Each row
is one (level, data item, unit, scenario or pathway, fuel, peak/annual/minimum) combination
with one value per year column, and the vendor `Unit` column names that row's unit. The year
headers are the vendor's labels. The period each label covers (calendar year, financial year
or another period) and whether the integer is the start or end of it are **not established**
(`TODO: verify`; this is the first part of the hold question, see Holds). Some early year
columns (for example 2010-2022 in the 2023 file, which begins 2010) may be historical rather
than projected, and this page does not establish whether any column is outturn or projection.
Until the hold is answered, do not use the values as either outturn or a forecast.

gridflow reshapes each wide body into **long rows**: one row per (dimension tuple,
`projection_year`) with a `value`, and it stamps an `edition` from the file name (ADR-042;
this is the SC pilot of the scenario mechanism). Silver holds **45,985 rows from 4 resources**
(2023: 21,730 · 2024: 16,275 · 2025: 7,000 · 2026: 980), of which **5,971** have a blank
(null) `value`. The silver output is **held** (unit E-SEM; see Holds). This page therefore
gives schema, row counts, clocks and missingness only, never data values, samples or ranges
of values. The three ED2 definition PDFs are catalogue-only documents (DOC).

Sibling scenario packages in this vault: @./tresp-demand-pathways.md and
@./tresp-generation-pathways.md (tRESP, which is already long-shaped).

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Electricity Demand Summary (ED1) 2023 | CSV | upload | `de41fa7f-5bd6-4da4-aff1-aede85d7b651` |
| Electricity Demand Summary (ED1) 2024 | CSV | upload | `9514d486-5fa8-4bbb-80d3-59668e1eeb5f` |
| Electricity Demand Summary (ED1) 2025 | CSV | upload | `300c07b9-baeb-4411-bc40-987cbb4aec0b` |
| Electricity Demand Summary (ED1) 2026 | CSV | upload | `2769bcac-e2ae-45b9-a9d6-0e2c3e6312c7` |

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Electricity Demand Definitions Data table (ED2) 2025 | PDF | upload | `93761974-17f5-43da-a690-71faaab610a5` |
| Electricity Demand Definitions Data table (ED2) 2023 - Version 2 | PDF | upload | `0a127297-b33a-48fa-bf7b-e02fd350d1be` |
| Electricity Demand Definitions Data table (ED2) 2024 | PDF | upload | `2651d72a-a62d-4fe6-a283-408398e853e8` |

### Resource detail

Package `fes-electricity-demand-summary-data-table-ed1` (CKAN id
`2c15c755-d8fe-4229-9169-3b6dd7c88fec`) has **7 resources** in the 2026-10-06 catalogue
snapshot (4 CSV, 3 PDF). `last_modified` is the CKAN value in that snapshot. Download links
are the snapshot's resource URLs; `size` is null in the snapshot.

| Edition | Disposition | File | CKAN `last_modified` | Download |
|---|---|---|---|---|
| 2023 | SILVER | `fes2023_ed1_v001.csv` | 2023-07-10T03:30:52.627453 | [CSV](https://api.neso.energy/dataset/2c15c755-d8fe-4229-9169-3b6dd7c88fec/resource/de41fa7f-5bd6-4da4-aff1-aede85d7b651/download/fes2023_ed1_v001.csv) |
| 2024 | SILVER | `fes2024_ed1_v002.csv` | 2024-07-16T11:10:23.666541 | [CSV](https://api.neso.energy/dataset/2c15c755-d8fe-4229-9169-3b6dd7c88fec/resource/9514d486-5fa8-4bbb-80d3-59668e1eeb5f/download/fes2024_ed1_v002.csv) |
| 2025 | SILVER | `fes2025_ed1_v006.csv` | 2025-12-10T17:03:48.740109 | [CSV](https://api.neso.energy/dataset/2c15c755-d8fe-4229-9169-3b6dd7c88fec/resource/300c07b9-baeb-4411-bc40-987cbb4aec0b/download/fes2025_ed1_v006.csv) |
| 2026 | SILVER | `10yo2026_ed1_v001.csv` | 2026-09-16T14:24:51.109781 | [CSV](https://api.neso.energy/dataset/2c15c755-d8fe-4229-9169-3b6dd7c88fec/resource/2769bcac-e2ae-45b9-a9d6-0e2c3e6312c7/download/10yo2026_ed1_v001.csv) |
| 2023 (Version 2) | DOC | `fes2023_ed2_v002.pdf` | 2023-08-24T10:07:14.976681 | [PDF](https://api.neso.energy/dataset/2c15c755-d8fe-4229-9169-3b6dd7c88fec/resource/0a127297-b33a-48fa-bf7b-e02fd350d1be/download/fes2023_ed2_v002.pdf) |
| 2024 | DOC | `fes2024_ed2_v001.pdf` | 2024-07-15T06:28:40.026543 | [PDF](https://api.neso.energy/dataset/2c15c755-d8fe-4229-9169-3b6dd7c88fec/resource/2651d72a-a62d-4fe6-a283-408398e853e8/download/fes2024_ed2_v001.pdf) |
| 2025 | DOC | `fes2025_ed2_v004.pdf` | 2025-08-19T14:06:11.798101 | [PDF](https://api.neso.energy/dataset/2c15c755-d8fe-4229-9169-3b6dd7c88fec/resource/93761974-17f5-43da-a690-71faaab610a5/download/fes2025_ed2_v004.pdf) |

- **No ED2 definitions for 2026.** The package has no ED2 resource for the 2026 file. Which
  definition applies to the 2026 rows is part of the hold question.
- **The ED2 PDFs hold the variable definitions.** The CSVs hold identifiers and labels only,
  not definitions (SC RESEARCH §3). The PDFs are captured to bronze as `fes_ed1_electricity_demand_files`
  and are **not parsed**; gridflow does not extract definitions from them.
- **Pairing is not implied by dates.** The 2025 ED2 PDF was last modified in 2025-08, before
  the 2025 ED1 CSV's last modification (2025-12). The 2023 ED2 is "Version 2", modified after
  the 2023 CSV. The same-edition pairing of an ED2 version with an ED1 version is therefore
  not implied by file dates. `TODO: verify` with NESO which ED2 version defines each ED1 file.
- File names `v001`, `v002`, `v006` (ED1) show the vendor republishes under the same resource
  slot. gridflow keys the edition on the file name, not on the version token (see Clocks).

## Families

### `fes_ed1_electricity_demand`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Aggregation Level | `aggregation_level` | string | — | yes | — | — |
| Data item | `data_item` | string | — | yes | — | — |
| Unit | `unit` | string | — | yes | — | — |
| Scenario | `scenario` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | yes | — | — |
| Peak/ Annual/ Minimum | `peak_annual_minimum` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `2010` → 2010, `2011` → 2011, `2012` → 2012, `2013` → 2013, `2014` → 2014, `2015` → 2015, `2016` → 2016, `2017` → 2017, `2018` → 2018, `2019` → 2019, `2020` → 2020, `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Aggregation Level | `aggregation_level` | string | — | yes | — | — |
| Data item | `data_item` | string | — | yes | — | — |
| Unit | `unit` | string | — | yes | — | — |
| Pathway | `pathway` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | yes | — | — |
| Peak/ Annual/ Minimum | `peak_annual_minimum` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `2020` → 2020, `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Aggregation Level | `aggregation_level` | string | — | yes | — | — |
| Data item | `data_item` | string | — | yes | — | — |
| Unit | `unit` | string | — | yes | — | — |
| Pathway | `pathway` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | yes | — | — |
| Peak/ Annual/ Minimum | `peak_annual_minimum` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 3: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 4:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Level | `level` | string | — | yes | — | — |
| Data item | `data_item` | string | — | yes | — | — |
| Unit | `unit` | string | — | yes | — | — |
| Scenario | `scenario` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | yes | — | — |
| Peak/ Annual/ Minimum | `peak_annual_minimum` | string | — | yes | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 4: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `aggregation_level`, `level`, `data_item`, `unit`, `scenario`, `pathway`, `fuel`, `peak_annual_minimum`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_ed1_v001.csv` → 2023; `fes2024_ed1_v002.csv` → 2024; `fes2025_ed1_v006.csv` → 2025; `10yo2026_ed1_v001.csv` → 2026
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### Shape and epoch map

Each resource is exactly one header epoch and exactly one edition. Every body has six
dimension columns, then contiguous year columns. Epoch numbers follow the tables above.

| Epoch | Edition | Resource | Year columns (header labels) | Wide rows | Long rows | Null `value` |
|---|---|---|---|---|---|---:|
| 1 | 2023 | `de41fa7f-…` | 2010–2050 (41) | 530 | 21,730 | 2,432 |
| 2 | 2024 | `9514d486-…` | 2020–2050 (31) | 525 | 16,275 | 2,235 |
| 3 | 2025 | `300c07b9-…` | 2023–2050 (28) | 250 | 7,000 | 750 |
| 4 | 2026 | `2769bcac-…` | 2023–2050 (28) | 35 | 980 | 554 |
| | **Total** | 4 resources | | 1,340 | **45,985** | **5,971** |

The counts equal the activation receipt (RULINGS 600; RESULTS §SC) and the pre-merge strict
probe (SC RESEARCH §3: 21,730 / 16,275 / 7,000 / 980 long rows, 0 duplicate keys).

Column naming differs across editions (the header text is kept; gridflow does not merge columns):

| Silver column | Populated in editions | Null in editions |
|---|---|---|
| `aggregation_level` | 2023, 2024, 2025 | 2026 |
| `level` | 2026 | 2023, 2024, 2025 |
| `scenario` | 2023, 2026 | 2024, 2025 |
| `pathway` | 2024, 2025 | 2023, 2026 |

Whether vendor `Aggregation Level` and `Level`, or `Scenario` and `Pathway`, mean the same
thing across editions is **not** established by the CSVs (the entity key keeps both columns
so no row collapses). `TODO: verify` with NESO before any cross-edition join on them.

Dimension cardinalities per edition (count of distinct non-null labels, no label values):

| Edition | `data_item` | `unit` | scenario or pathway | `peak_annual_minimum` | level or aggregation level |
|---|---:|---:|---:|---:|---:|
| 2023 | 77 | 2 | 5 | 4 | 5 |
| 2024 | 76 | 2 | 5 | 4 | 5 |
| 2025 | 50 | 2 | 5 | 2 | 5 |
| 2026 | 29 | 2 | 1 | 3 | 5 |

`fuel` has one distinct label in every edition.

#### Clocks

Two clocks, separate and not to be mixed (ADR-030, ADR-042):

1. **Vintage (`published_at` = `available_at`):** the CKAN `last_modified` of the captured
   resource. It is when NESO last changed that file, not when the vendor generated the
   values. Verified in silver: `published_at` equals `available_at` on every row; and
   `event_time` equals `timestamp_utc` on every row.
   - 2023: 2023-07-10T03:30:52.627453Z
   - 2024: 2024-07-16T11:10:23.666541Z
   - 2025: 2025-12-10T17:03:48.740109Z
   - 2026: 2026-09-16T14:24:51.109781Z
2. **Event time:** the temporal recipe is **`none`**. A projection year is a vendor header
   label, not a dated instant, so there is no row-level event time. `timestamp_utc` (and
   `event_time`, which equals it) is the **capture time** of the bronze file, here
   2026-10-08 10:53 UTC (all four captured within about eight seconds). It carries no
   information about the year a value covers. The period a label covers is held (see Holds);
`projection_year` is only the vendor's header label as an integer.

`edition` is stamped from the file name (`edition_by_filename`), independent of both clocks.
It is not an issue time. Point-in-time queries bound `available_at <= as_of` per capture
(RULINGS 597); that bound is on the vintage clock, not on the capture time. Where a body's
`ckan_last_modified` predates its capture (every file here was captured on 2026-10-08, after
its `last_modified`), `available_at <= as_of` is not proof that the bytes held now were the
bytes captured by then (ADR-039 FM-12, citing ADR-034 C-3). `TODO: verify` whether NESO edits
a file in place without bumping `last_modified`; nothing here shows it either way.

#### Units

Units come from the vendor's own `Unit` column in each row, never inferred from a column or
data-item name. SC RESEARCH §3 records the row-specific `Unit` values as `GW` or `GWh`, and
notes the same `Data item` can appear in both units, so `unit` is part of the entity key and
**must be kept** with the value. Silver has two distinct `unit` labels in every edition. The
per-column "Vendor unit" cell above is `—` because the unit is per row, not per column. The
CSV does not define the quantities behind the units (see Holds, ED2 mapping).

#### Missing values and sentinels

- **Blank year cells are kept as null `value`**, never replaced by zero (5,971 rows; table
  above). What a blank means (not modelled, not applicable, or zero) is part of the hold
  question; the CSVs do not say.
- Every non-blank year cell in all four bodies casts strictly to `Float64` (SC RESEARCH §3).
  No `N/A`, `-` or other text sentinel is evidenced; no null-token or whitespace rule is
  applied. No NaN in silver.
- The six dimension cells are non-null in every body and the full long key is unique in
  every body (0 duplicate keys, SC RESEARCH §3).

### `fes_ed1_electricity_demand_files`

- Kind: files · archetype: SCN · refresh: adhoc · empty allowed: no
- files: catalogue only

The three ED2 definition PDFs. Bronze only (`bronze/neso_data_portal/fes_ed1_electricity_demand_files/`);
no silver output, no parsing. All three PDFs are captured (2026-10-08).

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

One CSV per annual FES edition, so a new resource appears about once a year (editions in the
snapshot: 2023, 2024, 2025, 2026). Each resource was captured once, on 2026-10-08. Package
`metadata_modified` in the 2026-10-06 snapshot is 2026-09-16T14:24:51.188078. The version
tokens in the file names (`v001`, `v002`, `v006`, `v001`) show NESO re-uploads files within
an edition; the vendor does not publish a revision policy. `TODO: verify` whether a published
edition file is revised in place. Only a changed `last_modified` across successive captures
can show it, and the registry captured each resource once so far.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_ed1_electricity_demand`: held: TODO: For every ED1 variable and edition 2023–2026, what period does a year header denote, and does its integer label denote the starting or ending year? Which same-edition ED2 definition applies to each ED1 Data item, aggregation level and measure, including the 2026 Ten Year Outlook? What does a blank projection cell mean (not modelled, not applicable or zero)? NESO states none of these in the CSVs; projection_year is the vendor's header label and blank cells are kept as null. (unit E-SEM)

The silver output exists on disk (45,985 rows) but is **held**: it is not eligible for
publication or for point-in-time model use until unit E-SEM answers the question above
(held at activation, RULINGS 600). The registry carries `eligible` at package level and
`held` at family level (gridflow `@docs/neso_data_portal/eligibility.md`); the family status
governs the silver output. The hold has three parts:

1. **What a year header denotes.** `projection_year` is the vendor's header label as an
   integer. The period it denotes, and whether the label is the start or the end of that
   period, is not stated in the CSVs, for any variable or edition (the hold question asks
   this per variable and per edition). `TODO: verify` in the ED2 PDFs or with NESO.
2. **Which ED2 definition applies.** The CSVs carry labels, not definitions. The same-edition
   ED2 PDF defines each `Data item`, aggregation level and measure. No ED2 resource exists for
   the 2026 file (named `10yo2026`; the hold question calls it the Ten Year Outlook, and the
   package gives no relation to the 2023-2025 FES editions). `TODO: verify` the 2026 definitions
   and whether `Level` replaces `Aggregation Level` with the same meaning.
3. **Blank cells.** A blank may mean not modelled, not applicable or zero. gridflow keeps
   null and never converts to zero.

Settles it: a NESO statement (or ED2 definitions) of the period each year label covers, the
mapping from each ED1 `Data item` to its same-edition definition (including the 2026 file),
and the meaning of an empty projection cell. Until then the page shows no values, samples or
statistics of values, and gridflow gold does not read this family (RULINGS 611: no gold view
or gridflow_models consumer for this package).

## Links

- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/fes-electricity-demand-summary-data-table-ed1.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- ADRs: gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (clocks),
  `@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md` (records and holds),
  `@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md` (per-resource `_latest`),
  `@docs/DECISION_LOG/ADR-042-neso-scenario-unpivot-and-edition.md` (unpivot and edition)
- Package page: [NESO Data Portal – ED1](https://www.neso.energy/data-portal/fes-electricity-demand-summary-data-table-ed1)
- Vendor README: @../README.md
