---
source: "neso_data_portal"
package: "fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3"
dataset_keys: ["fes_ed3_heat_demand_natural_gas", "fes_ed3_heat_demand_natural_gas_sum_ed", "fes_ed3_heat_demand_sum_ed"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-15
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# FES: Pathways to Net Zero – Natural Gas, Residential and non-domestic (I&C) Heat Demand Summary Data table (ED3)

NESO's natural-gas and heat-demand summary tables from the Future Energy Scenarios (FES) data
workbook and, for 2026, the Ten Year Outlook. Each table is wide: one row per data item for one
scenario or pathway, with one column per projection year. They describe how much gas GB is
projected to use, and how much heat is projected to be demanded, by sector, fuel and technology.
Once the holds below lift they are candidate scenario inputs for gas-demand and heat-decarbonisation
questions in GB energy-system models. The tables sit beside the other FES summary tables
(@fes-electricity-demand-summary-data-table-ed1.md,
@fes-european-electricity-supply-data-table-es2.md,
@fes-flexibility-data-table-data-table-flx1.md,
@fes-road-transport-summary-data-table-ed5.md).

**The package holds three different tables, not one table in three copies.** The package name says
ED3, but the six resources are:

1. **The 2023 and 2024 combined table** (ED3, "Natural Gas and Residential Heat Demand Summary"):
   gas and residential heat in one wide table. The two editions hold 905 and 1,168 heat rows and
   55 gas-summary rows each.
2. **The 2025 and 2026 natural-gas summary** (ED3, "Natural Gas Demand Summary"): 55 and 11 rows.
3. **The 2025 and 2026 heat-demand summary** (ED7, "Heat Demand Summary"): 1,297 and 249 rows.

The two later tables split the earlier combined one, but **not row for row**. Ten of the eleven
gas-summary descriptions repeat the older ones literally and the hydrogen-production description
changes punctuation. The heat sector labels, technologies, timeframe labels and unit labels all
change across editions, and the older heat rows use the unit `number` where ED7 uses `stock`.
gridflow keeps three families, one per table, and keeps every vendor string as published, so no
equivalence between an old and a new label is asserted (FACTS §5). The family key
`fes_ed3_heat_demand_sum_ed` holds **ED7**, not an ED3 summary. The `sum_ed` suffix is the registry's
name for the heat summary.

**The silver output of all three families is held (unit E-SEM).** It exists on disk, and this page
gives its schema, row counts and structure. It publishes no data values from it. The meaning of the
year label, of the non-physical units and of a blank cell is not established (see Holds). The
package-level `eligibility: eligible` in the front matter is the package registry entry. The hold
is per family.

Reading rules for anyone who does open the silver:

- **Never add aggregate gas demand to technology-level heat demand.** The gas summary (ED3) is an
  aggregate by sector. ED7 is by technology, and it includes gas boilers, gas CHP and
  communal or district heat technologies. The two share no literal row identity and no literal
  overlap between gas `component` labels and heat `technology` labels, but that is not evidence
  they are additive. Any reconciliation needs same-edition coverage, unit and aggregation rules from
  NESO, which do not exist yet (FACTS §5).
- **Never sum editions.** The 2023, 2024, 2025 and 2026 rows for one data item and one year are
  separate forecasts, not observations. `edition` is a dimension of every row.
- **Units are per row and are not all physical.** Each wide row carries its own `units`, and
  `number`, `uptake` and `stock` are non-physical labels whose scale and denominator are
  undocumented (held). Filter by `units`. Never sum across units.
- **The earlier peak gas item is labelled `GWh`, the later one `GWh/day`.** gridflow keeps both as
  published and does not convert. `TODO: verify` which is correct for the 2023 edition.
- **ED4 uses an October-start gas year for its peak 1-in-20 item only.** The ED4 definition of that
  item runs from October to the September of the following year. Do not carry the convention over
  to annual gas items or to any heat item.
- **ED4 2026 warns about comparability.** Its electricity-generation gas-demand definition says the
  outlook includes extra gas demand from electricity-network constraints and that the earlier
  forecast is not directly comparable. Do not read a change in that gas item across editions as a
  forecast revision.
- **`scenario` and `pathway` are two separate columns.** The 2023 and 2026 files head the column
  `Scenario`, the 2024 and 2025 files head it `Pathway`. Each silver row has exactly one populated
  and the other null. gridflow does not merge them. `TODO: verify` whether NESO treats the two
  headings as the same concept.
- **A null `value` is a blank vendor cell**, with an undocumented meaning. A `0` is a value.
- **`projection_year` is a label.** It is the integer column header. The period or date it denotes
  is undocumented (see Holds).
- **ED4 is the codebook of these ED3 items.** @fes-natural-gas-demand-definitions-ed4.md gives a
  definition per `Item no.`, and `item_no` there is an identifier, not a measure. Join it on the
  same `edition`. It has 10 definitions in 2023 and 2024 and 11 in 2025 and 2026.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN
- Vendor tags: Demand, Electricity, FES, FES2023, Forecast, Subscribable
- CKAN package id `2fd7b713-9a85-45d8-87d8-cb3f01fd0e89`, created 2023-07-07, metadata last
  modified `2026-09-16T14:55:40.272776`
- Vendor page: [the NESO package page](https://www.neso.energy/data-portal/fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3)
- Vendor description (verbatim): "One of the FES outputs is an agreed set of data tables containing
  the GB FES values for natural gas and residential heat demand which are included in this dataset."
  The 2026 resource descriptions say "Ten-Year Outlook outputs" where the earlier ones say "FES
  outputs", and the ED7 descriptions add "covering demand for space heating".
  `TODO: verify` how NESO scopes the 2026 outlook against the 2023–2025 FES editions before
  comparing the editions column for column.

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Natural Gas Demand Summary (ED3) 2025 | CSV | upload | `f33e8ded-d302-40c4-be10-c7ca3a04b401` |
| Heat Demand Summary (ED7) 2025 | CSV | upload | `2019e900-11eb-40ce-ae54-a49a2abb5d4b` |
| Heat Demand Summary (ED7) 2026 | CSV | upload | `9394f025-8454-4db0-b73c-083e301a1e74` |
| Natural Gas Demand Summary (ED3) 2026 | CSV | upload | `c3d4acaf-5cd5-47f8-81a9-a4c10e16d55a` |
| Natural Gas and Residential Heat Demand Summary (ED3) 2023 | CSV | upload | `1f1de28d-eff7-4c5b-83fa-33cd7ad1bd39` |
| Natural Gas and Residential Heat Demand Summary (ED3) 2024 | CSV | upload | `fb452e53-881c-4d4e-a236-a5b6b50f2840` |

All six are `SILVER`, each feeding one of the three families. There is no `DOC`, `GIS` or `COVERED`
resource in the package, and no resource is held individually (the holds are per family). The
files, as captured on 2026-10-08, with the family each one feeds:

| Edition | Table and family | Download | Bronze bytes | Wide data rows | CKAN `last_modified` (offset-less, read as UTC) |
|---|---|---|---:|---:|---|
| 2023 | Combined, `fes_ed3_heat_demand_natural_gas` | [fes2023_ed3_v001.csv](https://api.neso.energy/dataset/2fd7b713-9a85-45d8-87d8-cb3f01fd0e89/resource/1f1de28d-eff7-4c5b-83fa-33cd7ad1bd39/download/fes2023_ed3_v001.csv) | 199,414 | 960 | `2023-07-10T03:31:06.331229` |
| 2024 | Combined, `fes_ed3_heat_demand_natural_gas` | [fes2024_ed3_v005.csv](https://api.neso.energy/dataset/2fd7b713-9a85-45d8-87d8-cb3f01fd0e89/resource/fb452e53-881c-4d4e-a236-a5b6b50f2840/download/fes2024_ed3_v005.csv) | 246,977 | 1,223 | `2025-02-17T17:12:48.492536` |
| 2025 | Gas summary, `fes_ed3_heat_demand_natural_gas_sum_ed` | [fes2025_ed3_v006.csv](https://api.neso.energy/dataset/2fd7b713-9a85-45d8-87d8-cb3f01fd0e89/resource/f33e8ded-d302-40c4-be10-c7ca3a04b401/download/fes2025_ed3_v006.csv) | 21,287 | 55 | `2025-12-10T16:50:20.589918` |
| 2026 | Gas summary, `fes_ed3_heat_demand_natural_gas_sum_ed` | [10yo2026_ed3_v001.csv](https://api.neso.energy/dataset/2fd7b713-9a85-45d8-87d8-cb3f01fd0e89/resource/c3d4acaf-5cd5-47f8-81a9-a4c10e16d55a/download/10yo2026_ed3_v001.csv) | 3,159 | 11 | `2026-09-16T14:54:22.558692` |
| 2025 | Heat, ED7, `fes_ed3_heat_demand_sum_ed` | [fes2025_ed7_v006.csv](https://api.neso.energy/dataset/2fd7b713-9a85-45d8-87d8-cb3f01fd0e89/resource/2019e900-11eb-40ce-ae54-a49a2abb5d4b/download/fes2025_ed7_v006.csv) | 294,208 | 1,297 | `2025-12-10T16:51:16.997421` |
| 2026 | Heat, ED7, `fes_ed3_heat_demand_sum_ed` | [10yo2026_ed7_v001.csv](https://api.neso.energy/dataset/2fd7b713-9a85-45d8-87d8-cb3f01fd0e89/resource/9394f025-8454-4db0-b73c-083e301a1e74/download/10yo2026_ed7_v001.csv) | 40,211 | 249 | `2026-09-16T14:55:40.190751` |

The stable handle for a resource is its id, not the file name. Every body decodes as strict UTF-8
with no ragged rows. Only `fes2024_ed3_v005.csv` carries a UTF-8 BOM, which the reader handles
(FACTS §9). The file name and the resource name agree on the edition for every resource.
gridflow reads the edition from the **exact file name** and never infers it from the projection
years, the CKAN timestamps or the capture date. The captured name of the 2025 gas-summary resource
**begins with a space** (" Natural Gas Demand Summary (ED3) 2025"), so match on id or file name,
not on the resource name. The 2026 files carry the filename prefix `10yo2026`.

The 2026 resources are much smaller than the 2025 ones: 11 gas-summary rows against 55 (3,159 bytes
against 21,287) and 249 heat rows against 1,297 (40,211 bytes against 294,208). The 2026 files hold
one `scenario` value where the 2025 files hold five `pathway` values (measured from silver), which
accounts for the gas summary exactly (11 = 55 / 5). The heat table is not an exact fifth because its
technology and fuel sets also differ. `TODO: verify` with the vendor how it scopes the 2026 outlook.

## Families

### `fes_ed3_heat_demand_natural_gas`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Scenario | `scenario` | string | — | yes | — | — |
| Sector | `sector` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | yes | — | — |
| Technology | `technology` | string | — | no | — | — |
| Time | `time` | string | — | yes | — | — |
| Units | `units` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `2020` → 2020, `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Pathway | `pathway` | string | — | yes | — | — |
| Sector/Aggregation Level | `sector_aggregation_level` | string | — | yes | — | — |
| Fuel | `fuel` | string | — | yes | — | — |
| Technology | `technology` | string | — | no | — | — |
| Data Type | `data_type` | string | — | yes | — | — |
| Units | `units` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `2020` → 2020, `2021` → 2021, `2022` → 2022, `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `scenario`, `sector`, `fuel`, `technology`, `time`, `units`, `pathway`, `sector_aggregation_level`, `data_type`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_ed3_v001.csv` → 2023; `fes2024_ed3_v005.csv` → 2024
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource, read as UTC per ADR-030 (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). There is one vintage per
   resource, and every row of an edition shares it: `2023-07-10T03:31:06.331229` for 2023 and
   `2025-02-17T17:12:48.492536` for 2024. Checked on every silver row on 2026-10-15:
   `available_at` equals `published_at` on all 67,673 rows, and each `published_at` equals its
   resource's `last_modified`. The vintage says when the file last changed on the portal. It does
   not say when NESO first published the edition. The 2024 resource was created on the portal on
   2024-07-12 and last changed on 2025-02-17, and its file name carries `v005`, so the portal copy
   has been replaced at least once since creation (a file-name and timestamp observation, not a
   vendor statement). `TODO: verify` with the vendor what changed. Do not read the vintage as the
   original publication date of the FES 2024 workbook.
2. **Event time (temporal recipe `none`).** The record declares no event-time recipe, because the
   year labels have no established period (see Holds). `timestamp_utc` is therefore the **capture
   time**, not a modelled time. `event_time` and `capture_written_at` carry the same instant. All
   rows of an edition share one `timestamp_utc` (2023: `2026-10-08T10:53:59.217853Z`, 2024:
   `2026-10-08T10:54:01.922700Z`). Do not use `timestamp_utc` as a forecast horizon or a model time
   axis. The only year information is `projection_year`, a label.

Rows per edition and resource (silver, from the 2026-10-08 transform):

| Edition | Resource id | Wide rows × year columns | Silver rows | Null `value` rows | Projection-year labels |
|---|---|---|---:|---:|---|
| 2023 | `1f1de28d-eff7-4c5b-83fa-33cd7ad1bd39` | 960 × 31 | 29,760 | 4,225 | 2020–2050 |
| 2024 | `fb452e53-881c-4d4e-a236-a5b6b50f2840` | 1,223 × 31 | 37,913 | 5,063 | 2020–2050 |
| | | | **67,673** | **9,288** | |

**What a wide row is.** Both editions hold two kinds of row in one table: heat items and
gas-summary items (FACTS §5, measured by comparing the dictionary rows).

| Edition | Heat rows | Gas-summary rows | Total |
|---|---:|---:|---:|
| 2023 | 905 | 55 | 960 |
| 2024 | 1,168 | 55 | 1,223 |

Silver has **no column that marks a row as heat or gas-summary**, so the split above is a content
comparison, not a silver field. `TODO: verify` the vendor's rule for separating them before building
anything on a split. The 55 gas-summary rows span eleven description categories, and they sit in the
same `scenario` or `pathway`, `technology`, `time` or `data_type` and `units` columns as the heat
rows (the later gas summary has `description` and `component` columns instead). Distinct label
counts per edition (counts only, no label lists for a held family):

| Edition | Scenario / pathway | Sector or sector-aggregation | Fuel (non-null) | Technology | Timeframe (`time` or `data_type`) | Units |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 5 `scenario` | 13 `sector` | 9 | 29 | 6 `time` | 5 |
| 2024 | 5 `pathway` | 14 `sector_aggregation_level` | 10 | 30 | 5 `data_type` | 6 |

The 2023 file's `scenario`, `sector` and `time` columns are populated and its `pathway`,
`sector_aggregation_level` and `data_type` columns are null on all 29,760 rows. The 2024 file is the
mirror image on all 37,913 rows. The vendor's [2024 dictionary](https://www.neso.energy/data-portal/fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3/natural_gas_and_residential_heat_demand_summary_ed3_2024)
describes `Units` as the unit in which the item is reported and `Data Type` as its timeframe. The
`Time` column of the 2023 file is read the same way only as far as the held question lets it:
`TODO: verify` that `Time` (2023) and `Data Type` (2024) are the same concept.

**Units (vendor dictionary: the row's `Units` field).** Each wide row carries its own unit. The
unit is read from that field and never inferred from the column name. The units, as published
(FACTS g4), and the wide rows in each file:

| `units` | 2023 | 2024 |
|---|---:|---:|
| `TWh` | 265 | 383 |
| `GW` | 320 | 359 |
| `number` | 160 | 218 |
| `uptake` | 160 | 208 |
| `GWh` | 55 | 50 |
| `GWh/day` | 0 | 5 |

- The silver `units` column holds these strings verbatim. There is no conversion and no separate
  unit column.
- `number` and `uptake` are not physical units. Their basis and scale are undocumented, and no
  denominator is given for `uptake`. `TODO: verify` before reading any `uptake` value as a share or
  a percentage. Do not assume either.
- The 55 `GWh` rows of 2023 match the 55 gas-summary rows in number. In 2024 the 55 gas-summary
  rows are 50 `GWh` rows and 5 `GWh/day` rows, and the later gas summary shows the same 50 and 5
  split by timeframe (`Annuals` and `Peak 1in20`). The peak gas-demand item is the one the later body labels
  `GWh/day`, and the same-edition ED4 defines it by a gas year starting in October. The 2023 body
  labels that daily peak item `GWh`. gridflow keeps the published label and does not rewrite it
  from the ED4 interpretation. `TODO: verify` the reported unit for the peak daily gas-demand item
  in the 2023 table (this is part of the hold).
- `TWh` rows are energy over a period and `GW` rows are power. The dictionary does not say which
  period the `TWh` rows integrate over, nor at what moment a `number` count is taken.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- **Blank cells** are kept as **null** `value`. They are not dropped and not filled.
- The vendor does not say what a blank means. Unmodelled, unavailable, inapplicable and not yet
  published are all possible. Their position or frequency does not settle it. `TODO: verify` (part
  of the hold).
- The blank year columns in the CSV bodies:

  | Edition | Blank cells per year column | Year columns |
  |---|---:|---|
  | 2023 | 1 | `2028` |
  | 2023 | 192 | each of `2029`–`2050` |
  | 2024 | 1 | each of `2028` and `2029` |
  | 2024 | 233 | each of `2030`–`2049` |
  | 2024 | 401 | `2050` |

  Every other year column has no blanks. These blanks are the silver rows with a null `value`:
  4,225 in 2023 and 5,063 in 2024. The blank `Fuel` cells are a separate matter: 335 wide rows in
  2023 and 486 in 2024 have no fuel. They are kept as a null `fuel` dimension and give 10,385 and
  15,066 silver rows. A null `fuel` is not a null `value`.
- The whole-cell tokens `-`, `N/A`, `NA`, `n/a`, `#N/A`, `NULL`, `null` and `NaN` occur **zero
  times** in every column of every captured body. There are no text sentinels in the value cells.
- **Zeros are values.** Numeric zeros occur in both editions. No primary source identifies them as
  sentinels. They stay as `0.0`. Do not treat zero as missing.
- Every non-blank cell casts strictly to float64, with zero failures in both resources.

**Identity and selection.** The entity key is `resource_id`, `edition`, `scenario`, `sector`,
`fuel`, `technology`, `time`, `units`, `pathway`, `sector_aggregation_level`, `data_type` and
`projection_year`. This is a **measured guard key**: both complete bodies passed it with zero
duplicated long rows, and no measure belongs in it. No vendor text declares it as the identity of a
row. `TODO: verify` the vendor's own uniqueness rule. Because the 2023 and 2024 dimension columns
differ, one of each pair is always null per row. `_latest` is `whole_capture` per `resource_id`: a
newer capture of a resource replaces that resource's previous capture as a whole. It never replaces
another edition. No revision rule between captures of one resource is claimed.

### `fes_ed3_heat_demand_natural_gas_sum_ed`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Pathway | `pathway` | string | — | yes | — | — |
| Description | `description` | string | — | no | — | — |
| Fuel | `fuel` | string | — | no | — | — |
| Component | `component` | string | — | no | — | — |
| Data Type | `data_type` | string | — | no | — | — |
| Units | `units` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Scenario | `scenario` | string | — | yes | — | — |
| Description | `description` | string | — | no | — | — |
| Fuel | `fuel` | string | — | no | — | — |
| Component | `component` | string | — | no | — | — |
| Data Type | `data_type` | string | — | no | — | — |
| Units | `units` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `pathway`, `description`, `fuel`, `component`, `data_type`, `units`, `scenario`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2025_ed3_v006.csv` → 2025; `10yo2026_ed3_v001.csv` → 2026
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource, read as UTC per ADR-030. One vintage per resource:
   `2025-12-10T16:50:20.589918` for 2025 and `2026-09-16T14:54:22.558692` for 2026. Checked on every
   silver row on 2026-10-15: `available_at` equals `published_at` on all 1,848 rows, and each
   `published_at` equals its resource's `last_modified`. The vintage is the last change on the
   portal, not the first publication of the edition. The 2026 resource was created on the portal at
   `2026-09-16T14:54:22.664663`, within a second of its `last_modified`.
2. **Event time (temporal recipe `none`).** No event-time recipe is declared. `timestamp_utc` is the
   **capture time** (2025: `2026-10-08T10:54:06.022320Z`, 2026: `2026-10-08T10:54:08.488330Z`), and
   `event_time` and `capture_written_at` carry the same instant. It is not a forecast horizon. The
   only year information is `projection_year`, a label.

Rows per edition and resource:

| Edition | Resource id | Wide rows × year columns | Silver rows | Null `value` rows | Projection-year labels |
|---|---|---|---:|---:|---|
| 2025 | `f33e8ded-d302-40c4-be10-c7ca3a04b401` | 55 × 28 | 1,540 | 165 | 2023–2050 |
| 2026 | `c3d4acaf-5cd5-47f8-81a9-a4c10e16d55a` | 11 × 28 | 308 | 154 | 2023–2050 |
| | | | **1,848** | **319** | |

The 2025 table has five pathways and eleven descriptions (55 rows). The 2026 table has one scenario
and eleven descriptions (11 rows), and its scenario cell reads `Ten Year Outlook`. Each edition has 10 distinct `component` values and every `fuel` cell is `gas`. The
2025 file populates `pathway` and nulls `scenario` on all 1,540 rows, and the 2026 file populates
`scenario` and nulls `pathway` on all 308 rows. The `data_type` column has two values per edition:
`Annuals` and `Peak 1in20`.

**Units (vendor dictionary: the row's `Units` field), by timeframe:**

| `data_type` | `units` | 2025 wide rows | 2026 wide rows |
|---|---|---:|---:|
| `Annuals` | `GWh` | 50 | 10 |
| `Peak 1in20` | `GWh/day` | 5 | 1 |

- The unit is `GWh` for every annual row and `GWh/day` for every peak row. This is the vendor's
  label, read from the row. Annual values are energy, peak values are a daily rate.
- Whether an `Annuals` value covers a calendar year, a gas year or something else is not stated, and
  neither is how its integer label identifies the interval. The ED4 gas-year start (October to
  September of the following year) is defined for the total GB peak 1-in-20 demand item, **for that
  item only**. Do not apply it to the `Annuals` rows. `TODO: verify`.
- The later body labels the peak item `GWh/day` where the older combined table labelled it `GWh`
  (see above). No conversion is applied in either direction.
- ED4 2026 says its electricity-generation gas demand now includes extra demand arising from
  electricity-network constraints, and warns that the earlier forecast is not directly comparable.
  The 2025 and 2026 gas summaries are therefore not comparable item for item on that component.
  `TODO: verify` the edition-specific coverage of electricity-generation gas demand and the
  network-constraint treatment (part of the hold).

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- **Blank cells** are kept as **null** `value`, with undocumented meaning. `TODO: verify` (part of
  the hold).
- The blanks sit at the far end of the horizon: 11 blank cells in each of the year columns
  `2036`–`2050` in the 2025 body (15 columns) and 11 in each of `2037`–`2050` in the 2026 body (14
  columns), which is 165 and 154 silver rows. The year header runs to 2050 in both. The blank tail
  is included in the unpivot and is not trimmed.
  A blank in one edition says nothing about another edition.
- The whole-cell tokens `-`, `N/A`, `NA`, `n/a`, `#N/A`, `NULL`, `null` and `NaN` occur zero
  times. **Zeros are values**: numeric zeros occur in both editions and are kept as `0.0`.
- Every non-blank cell casts strictly to float64, with zero failures.

**Identity and selection.** The entity key is `resource_id`, `edition`, `pathway`, `description`,
`fuel`, `component`, `data_type`, `units`, `scenario` and `projection_year`. This is a measured
guard key: both complete bodies passed it with zero duplicated long rows, and no vendor text
declares it. `TODO: verify` the vendor's uniqueness rule. `_latest` is `whole_capture` per
`resource_id`, and it never replaces another edition.

### `fes_ed3_heat_demand_sum_ed`

This family holds **ED7**, as evidenced by the file names and resource names. The vendor
description of both resources adds "covering demand for space heating".

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Pathway | `pathway` | string | — | yes | — | — |
| Sector/Aggregation Level | `sector_aggregation_level` | string | — | no | — | — |
| Fuel | `fuel` | string | — | yes | — | — |
| Technology | `technology` | string | — | no | — | — |
| Data Type | `data_type` | string | — | no | — | — |
| Units | `units` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 1: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Scenario | `scenario` | string | — | yes | — | — |
| Sector/Aggregation Level | `sector_aggregation_level` | string | — | no | — | — |
| Fuel | `fuel` | string | — | yes | — | — |
| Technology | `technology` | string | — | no | — | — |
| Data Type | `data_type` | string | — | no | — | — |
| Units | `units` | string | — | no | — | — |
| (unpivot) | `projection_year` | int64 | — | no | — | — |
| (unpivot) | `value` | float64 | — | yes | — | — |

Unpivot, epoch 2: `2023` → 2023, `2024` → 2024, `2025` → 2025, `2026` → 2026, `2027` → 2027, `2028` → 2028, `2029` → 2029, `2030` → 2030, `2031` → 2031, `2032` → 2032, `2033` → 2033, `2034` → 2034, `2035` → 2035, `2036` → 2036, `2037` → 2037, `2038` → 2038, `2039` → 2039, `2040` → 2040, `2041` → 2041, `2042` → 2042, `2043` → 2043, `2044` → 2044, `2045` → 2045, `2046` → 2046, `2047` → 2047, `2048` → 2048, `2049` → 2049, `2050` → 2050

- Entity key: `resource_id`, `edition`, `pathway`, `sector_aggregation_level`, `fuel`, `technology`, `data_type`, `units`, `scenario`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2025_ed7_v006.csv` → 2025; `10yo2026_ed7_v001.csv` → 2026
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource, read as UTC per ADR-030. One vintage per resource:
   `2025-12-10T16:51:16.997421` for 2025 and `2026-09-16T14:55:40.190751` for 2026. Checked on every
   silver row on 2026-10-15: `available_at` equals `published_at` on all 43,288 rows, and each
   `published_at` equals its resource's `last_modified`. The vintage is the last change on the
   portal, not the first publication of the edition. The 2025 gas summary and the 2025 heat summary
   changed within a minute of each other on 2025-12-10 and look like one bulk upload
   (`TODO: verify` with the vendor).
2. **Event time (temporal recipe `none`).** No event-time recipe is declared. `timestamp_utc` is the
   **capture time** (2025: `2026-10-08T10:54:12.302570Z`, 2026: `2026-10-08T10:54:15.301755Z`), and
   `event_time` and `capture_written_at` carry the same instant. It is not a forecast horizon. The
   only year information is `projection_year`, a label.

Rows per edition and resource:

| Edition | Resource id | Wide rows × year columns | Silver rows | Null `value` rows | Projection-year labels |
|---|---|---|---:|---:|---|
| 2025 | `2019e900-11eb-40ce-ae54-a49a2abb5d4b` | 1,297 × 28 | 36,316 | 5,655 | 2023–2050 |
| 2026 | `9394f025-8454-4db0-b73c-083e301a1e74` | 249 × 28 | 6,972 | 3,984 | 2023–2050 |
| | | | **43,288** | **9,639** | |

The 2025 file populates `pathway` and nulls `scenario` on all 36,316 rows, and the 2026 file
populates `scenario` and nulls `pathway` on all 6,972 rows. Distinct label counts per edition
(counts only, no label lists for a held family):

| Edition | Scenario / pathway | Sector-aggregation levels | Fuel (non-null) | Technology | `data_type` | Units |
|---|---:|---:|---:|---:|---:|---:|
| 2025 | 5 `pathway` | 3 | 7 | 16 | 6 | 4 |
| 2026 | 1 `scenario` | 3 | 5 | 14 | 6 | 4 |

The sector-aggregation dimension distinguishes residential, commercial and industrial rows. The
`data_type` dimension includes annual demand, cumulative annual output, peak output, and
behavioural and insulation savings. Preserve the source spellings. Their names do not establish
the period, the scale or how a savings row relates to the technology demand rows (see Holds).

**Units (vendor dictionary: the row's `Units` field).** The units, as published (FACTS g4), and the
wide rows in each file:

| `units` | 2025 | 2026 |
|---|---:|---:|
| `TWh` | 548 | 104 |
| `GW` | 347 | 67 |
| `uptake` | 196 | 38 |
| `stock` | 206 | 40 |

- The silver `units` column holds these strings verbatim. There is no conversion.
- `uptake` and `stock` are non-physical labels. The scale and denominator of `uptake`, and the
  counting basis and snapshot date of `stock`, are undocumented. The vendor's
  [2026 ED7 dictionary](https://www.neso.energy/data-portal/fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3/heat_demand_summary_ed7_2026)
  supplies column types but no definitions that resolve these. `TODO: verify` before use.
- `stock` in ED7 and `number` in the older combined table both read as counts, but gridflow asserts
  no equivalence between them. `TODO: verify`.
- `TWh` rows are energy over a period and `GW` rows are power. The dictionary does not say which
  period the `TWh` rows integrate over.

**Sentinels and missing values (FACTS g5).** The record declares no null token.

- **Blank cells** are kept as **null** `value`, with undocumented meaning. `TODO: verify` (part of
  the hold).
- The blank year columns in the CSV bodies:

  | Edition | Blank cells per year column | Year columns |
  |---|---:|---|
  | 2025 | 377 | each of `2036`–`2050` |
  | 2026 | 249 (every row) | each of `2023`, `2024` and `2037`–`2050` |

  Every other year column has no blanks. These blanks are the silver rows with a null `value`:
  5,655 in 2025 and 3,984 in 2026. In the 2026 body the first two year columns are blank on every
  row, so the first populated projection year is 2025. The blank `Fuel` cells are separate: 402 wide
  rows in 2025 and 78 in 2026 have no fuel, kept as a null `fuel` and giving 11,256 and 2,184
  silver rows. A null `fuel` is not a null `value`.
- The whole-cell tokens `-`, `N/A`, `NA`, `n/a`, `#N/A`, `NULL`, `null` and `NaN` occur zero
  times. **Zeros are values**: numeric zeros occur in both editions and are kept as `0.0`.
- Every non-blank cell casts strictly to float64, with zero failures.

**Identity and selection.** The entity key is `resource_id`, `edition`, `pathway`,
`sector_aggregation_level`, `fuel`, `technology`, `data_type`, `units`, `scenario` and
`projection_year`. This is a measured guard key: both complete bodies passed it with zero
duplicated long rows, and no vendor text declares it. `TODO: verify` the vendor's uniqueness rule.
`_latest` is `whole_capture` per `resource_id`, and it never replaces another edition.

### Silver columns and location (all three families)

Silver columns beyond the vendor columns: `edition`, `resource_id`, `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id`, `dataset_version` (all timestamps tz-aware UTC; `dataset_version` is `1+e1` on
every row of every edition: the registry record version (1) plus the silver engine version (`e1`).
It does not identify the schema epoch). The two schema epochs of each family are numbered 1 and 2
in edition order on this page only. No silver column carries an epoch number.

Bronze holds the raw CSV bytes unchanged under
`C:\gridflow-data\bronze\neso_data_portal\<family>\2026\10\08\raw_<capture time>_<resource id>_<hash>.csv`,
with a `.meta.json` sidecar beside each. The silver files sit under
`C:\gridflow-data\silver\neso_data_portal\<family>\year=2026\month=10\`, one Parquet file per
capture, so two per family.

**Activation (2026-10-15, master `f1ea613`, PR #124).** Transformed with window 2026-10-08, one
capture per resource and no prior silver: **112,851 rows**, equal to the planned count and with 0
failures. By family: `fes_ed3_heat_demand_natural_gas` 67,673, `fes_ed3_heat_demand_natural_gas_sum_ed`
1,848, `fes_ed3_heat_demand_sum_ed` 43,288, and the ED4 codebook `fes_ed4_gas_demand_defs` 42. The
whole batch was merged triple-green. Reconcile `--all --cutoff 2026-10-13` exited 0 over 247
families with 0 gaps, and coverage was clean (gridflow `@.planning/v0.22-RESULTS.md` §SCN-2b; RULINGS
831 and 833).

**Point-in-time.** The as-of cutoff is `available_at` (RULINGS 597 and ADR-042). The vintage is the
CKAN `last_modified`, which is a conservative proxy and nothing finer. Each edition has its own
vintage and enters as of that date. Because the value columns carry historical year values as well
as projections (the year headers start in 2020 or 2023), these bodies are not purely forward-looking
forecasts, and projection years before an edition's vintage need not be projections at all
(gridflow `@.planning/phases/v0.22-K-SCN-2/K-SCN-2-FACTS.md` §10). `TODO: verify` which year columns
the vendor treats as outturn or estimate.

### ED4, the codebook for these tables

ED4 (@fes-natural-gas-demand-definitions-ed4.md) is the vendor's codebook for the ED3 items. Its
`description` names a data item and its `definition` explains it, keyed by `item_no`, which the
vendor's dictionary marks as a "Unique Key". `item_no` is an identifier, not a measure, and it has no
unit. Join ED4 to these families on the **same `edition`**: ED4 carries its own `edition`, and its
definitions differ between editions (10 items in 2023 and 2024, 11 in 2025 and 2026). ED4 is an
eligible reference family with 42 silver rows (10, 10, 11 and 11 by edition) and no hold. Use it to
resolve what a gas item means. It carries the October-start gas-year definition of the total GB peak
1-in-20 demand item and the 2026 comparability warning about electricity-generation gas demand.
The vendor links an ED4 description to an ED3 data item. `TODO: verify` the exact item-to-row
mapping before joining at row level.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- Edition-driven: the package holds one resource per edition per table. The 2026 resources have a
  CKAN `last_modified` of `2026-09-16`. The 2023 combined resource was last modified on 2023-07-10,
  the 2024 combined resource on 2025-02-17, and the 2025 resources on 2025-12-10. `TODO: verify`
  when NESO adds the next edition's resources, and whether it will continue the split into a gas
  summary and a heat summary, which is how the 2025 and 2026 editions are published.
- `TODO: verify` whether NESO revises a published edition in place. The version part of the
  captured file names (`v001`, `v005`, `v006`, `v001`) is the only hint, and it is a file-name
  observation, not a vendor statement. The 2024 resource shows a later `last_modified` than its
  creation date, which is consistent with a replacement, but the vendor has not said so.
- Captures to date: one per resource (2026-10-08). No scheduled refresh has run yet, so no revision
  behaviour has been observed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_ed3_heat_demand_natural_gas`: held: TODO: For each heat and gas measure, define its year interval or stock/snapshot date and whether the integer labels a starting or ending year. Define the scale and denominator of `uptake`, the basis of `number`, and the timeframe labels including cumulative and peak outputs. Confirm the reported unit for the peak daily gas-demand item in the earlier table. What does each blank projection cell mean? (unit E-SEM)
- `fes_ed3_heat_demand_natural_gas_sum_ed`: held: TODO: What interval does each `Annuals` GWh value cover, and how does its integer year label identify that interval? What does a blank projection cell mean? Please confirm the edition-specific coverage of electricity-generation gas demand and the network-constraint treatment described in ED4. (unit E-SEM)
- `fes_ed3_heat_demand_sum_ed`: held: TODO: For every ED7 unit and data type, what interval or observation date does a year header denote? What are the scale and denominator of `uptake`, the counting basis and snapshot date of `stock`, and the start/end convention for peak-year labels? How are savings related to the reported technology demand? What does a blank projection cell mean? (unit E-SEM)

All three families are held by the SCN-2 batch records (RULINGS 821 and 822, with the activation in
831 and 833). Their silver output stays on disk. No gold view or model feed is planned for any of
them while the holds stand. This page publishes no data values from them: no sample rows and no
minimum, maximum or other value statistics. Row counts, null-cell counts and schema are given
because they describe structure, not values. Unit E-SEM must answer these things before the holds
can lift:

1. **The period behind each year label.** What interval or observation date the integer denotes,
   separately for energy items (`TWh`, `GWh`), power items (`GW`, `GWh/day`) and count or share
   items (`number`, `uptake`, `stock`). For example, is a `TWh` item a calendar year, a gas year or
   a financial year, and is a `stock` count taken at the start, the end or the middle of the year?
   Does the integer label the start or the end year?
2. **The non-physical units.** The scale and denominator of `uptake`, the basis of `number`, and
   the counting basis and snapshot date of `stock`.
3. **The timeframe and peak labels.** What the timeframe labels mean, including cumulative and peak
   outputs, and which unit the peak daily gas-demand item carries in the earlier table (`GWh` in
   2023 or `GWh/day`). How savings rows relate to the reported technology demand.
4. **What a blank cell means.** The vendor does not say whether it is unmodelled, unavailable,
   inapplicable or something else, in any of the three tables.
5. **The ED4 coverage questions.** The edition-specific coverage of electricity-generation gas
   demand and the network-constraint treatment described in ED4.

What the vendor text does establish, and what it does not (FACTS §5 and g1):

- Same-edition ED4 establishes the gas-year start label for the total GB peak 1-in-20 demand item:
  October to the September of the following year. It is explicit that this is that item only.
- ED4 2026 establishes that its electricity-generation gas-demand outlook includes demand arising
  from network constraints and is not directly comparable with the earlier forecast.
- The [2024 combined dictionary](https://www.neso.energy/data-portal/fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3/natural_gas_and_residential_heat_demand_summary_ed3_2024)
  names `Units` as the reported unit and `Data Type` as the timeframe. The
  [2026 ED7 dictionary](https://www.neso.energy/data-portal/fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3/heat_demand_summary_ed7_2026)
  gives column types only. Neither settles the period, the scale or the blank cells.
- No other SCN-2 family's year convention transfers to these tables. ED6 and ES2 have their own
  notes (@fes-road-transport-notes-data-table-ed6.md,
  @fes-european-electricity-supply-data-table-es2.md).
- The matching-edition FES workbook notes are the strongest next source, and they have not been
  read. NESO publishes them on its [FES documents page](https://www.neso.energy/publications/future-energy-scenarios-fes/fes-documents).
  `TODO: verify` the year and measure conventions there before any hold is lifted.

Until the holds lift:

- Do not publish values from any of the three families, or join them to an observed series by
  `projection_year`.
- Do not use them point-in-time at finer than the CKAN `last_modified` vintage.
- Do not add aggregate gas demand to technology-level heat demand, do not sum across editions,
  across units, or across `scenario` and `pathway`, and do not read `item_no` as a measure.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`): ES2
(@fes-european-electricity-supply-data-table-es2.md), FLX1
(@fes-flexibility-data-table-data-table-flx1.md) and ED5
(@fes-road-transport-summary-data-table-ed5.md) are held on the same kind of year-period and
blank-cell question, along with the 2026 ES2 notes resource and the 2023 FLX1 resource, which are
resource holds. ED4 (@fes-natural-gas-demand-definitions-ed4.md) and ED6
(@fes-road-transport-notes-data-table-ed6.md) are eligible reference families with no hold. All
holds are unit E-SEM.
