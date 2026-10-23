---
source: "neso_data_portal"
package: "tresp-demand-pathways"
dataset_keys: ["tresp_building_block_definitions", "tresp_demand_pathways_gsp", "tresp_demand_pathways_la_england", "tresp_demand_pathways_la_scotland", "tresp_demand_pathways_la_wales", "tresp_demand_pathways_resp_region", "tresp_gsp_area_names"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Transitional Regional Energy Strategic Plan (tRESP) - Demand Pathways

This package is NESO's published **demand** side of the **transitional Regional Energy
Strategic Plan (tRESP)**: projected volumes for 12 demand building blocks (electric
vehicles, heat pumps, district heating and air conditioning) out to 2050, by place. The
vendor notes describe the tRESP as the first output of NESO's Regional Energy Strategic Plan
(RESP) team, a bridge between today's electricity distribution network planning and the
full RESP approach due from 2028. Distribution network operators (DNOs) use it alongside
Ofgem's business-planning guidance for the third distribution price-control period (ED3,
2028-33). The pathways are structured like the building-block outputs of NESO's Future
Energy Scenarios 2025, but they are **tRESP adaptations, not FES editions**: Ofgem asked
NESO for a single short-term pathway (2025 to 2035), informed by the DNOs' Holistic
Transition pathway, which then branches into three long-term pathways (2035 to 2050):
Holistic Transition (`tRESP - HT`), Electric Engagement (`tRESP - EE`) and Hydrogen
Evolution (`tRESP - HE`). Every row is one projected quantity for one building block, one
place, one pathway and one `Year` label; the unit rides on the row, because the
quantity is a count for some blocks, an annual energy in GWh for two, and a surface area for
two more. It answers "how many EVs, heat pumps and so on, and how much electricity for
commercial heat pumps and air conditioning, does NESO project in this feeding area, local
authority or region?" and is a strategic-planning input for regional demand features in
models, not a measurement.

**Four things to know before using any of it.**

1. **The five demand data families are held** (unit E-SEM). The vendor never says what
   interval an annual-energy (GWh) value covers, and four building-block ids have no exact
   FES counterpart (see Holds). Silver exists; nothing is published from it. This page
   therefore gives schema, row counts and clocks for those families, and **never data
   values, ranges or example rows**. The two reference tables (building-block
   definitions and GSP-area names) are not held, so their content is shown.
2. **No temporal recipe.** `timestamp_utc` is gridflow's capture time, not a projection
   date. The projection date is the `Year` label (volume at 31 March of that year).
3. **One capture, one vintage.** The only capture is 2026-10-08 of files the vendor last
   modified on 2026-01-30. `available_at` is that CKAN `last_modified`.
4. **Local-authority rows are indicative.** NESO defines the pathways at the larger tRESP
   GSP-area level; the local-authority files are its approximate attribution, which the
   vendor says is not to be used as a planning target (resource description).

The sibling package for generation and storage is @./tresp-generation-pathways.md (MW
installed capacity; its outputs are not held for the same reason). It shares the same
pathways, geographies and reference tables. The shared research for both is gridflow
`@.planning/phases/v0.22-K-SCN-1/K-SCN-1-FACTS.md` (section SCN-1a).

- Publisher group: Demand
- Registry group: demand · archetype: SCN

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| tRESP Demand Pathways per Grid Supply Point Area | CSV | upload | `d616d330-4829-4f8a-b74b-00a57b41bc20` |
| tRESP Demand Pathways per RESP Nation and Region | CSV | upload | `cb1f1b31-1fde-40ab-86c9-34a3e1bdb665` |
| tRESP Indicative Demand Pathways per Local Authority for England | CSV | upload | `c3a261a4-94e9-4d75-b0de-d3805b0b5ae8` |
| tRESP Indicative Demand Pathways per Local Authority for Scotland | CSV | upload | `67d699eb-c5e9-42cd-a57a-74fcc52bcea9` |
| tRESP Indicative Demand Pathways per Local Authority for Wales | CSV | upload | `ccb3dfc8-ab4a-4f32-b944-8eced2e87bff` |

### GIS

| Resource | Format | Capture | Id |
|---|---|---|---|
| RESP Nations and Regions Areas | GPKG | upload | `4fdf4204-784f-4bab-aa81-f80480673dab` |
| tRESP Grid Supply Point (GSP) Areas | GPKG | upload | `59a5ec35-8fec-4b84-ba8c-236d97823178` |

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Lists of tRESP Pathways Building Blocks and of tRESP GSP areas with names | XLSX | upload | `11c36b60-eee5-45e9-b0da-6240e6e60d1c` | data container: the Building Blocks and GSP Areas with Names sheets feed tresp_building_block_definitions and tresp_gsp_area_names by child; the old building-block sheet stays held (see its child) (SCN-1) |
| ↳ tRESP Building Blocks | — | — | SILVER `tresp_building_block_definitions` | — |
| ↳ tRESP GSP Areas with Names | — | — | SILVER `tresp_gsp_area_names` | — |
| ↳ tRESP BB list - old | — | — | HOLD: TODO: the sheet's table has its header in row 3 (A:G) and data in rows 4-46, then a blank row 47 and a live data row 48 (`Alignment framework \| Demand \| Domestic \| Dem_BB001a \| Number of domestic customers \| Number \| Y – GSP`); a recipe ending at row 46 loses that row, one ending at row 48 fails the empty-data-row rule (ADR-037 P-6(d)), and the last_row growth check inspects only the next row, which the blank row would let truncation escape. Needs a vendor-corrected contiguous table or an explicitly supported multi-block/sparse-row recipe; proposed family tresp_building_block_definitions_old: record pending. (SCN-1) | — |

**Downloads and captures.** All eight resources have `url_type: upload` and were captured
once, on 2026-10-08, from `api.neso.energy` (sizes, URLs and CKAN `last_modified` from each
sidecar under `C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`). Every
resource was last modified by the vendor on 2026-01-30; the package was created on
2026-01-28 and is version 1.0 (CKAN). No resource carries an edition or version in its
name or filename.

| Resource | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---:|---:|---|
| Demand per GSP area | [tresp_pathways_demand_published.csv](https://api.neso.energy/dataset/e5e8eb8e-9fbd-4355-b4ad-9bbf00569d15/resource/d616d330-4829-4f8a-b74b-00a57b41bc20/download/tresp_pathways_demand_published.csv) | 11,189,109 | 160,776 | 2026-01-30T08:24:47.341529 |
| Demand per RESP nation and region | [tresp_pathways_demand_by_resp_region_published.csv](https://api.neso.energy/dataset/e5e8eb8e-9fbd-4355-b4ad-9bbf00569d15/resource/cb1f1b31-1fde-40ab-86c9-34a3e1bdb665/download/tresp_pathways_demand_by_resp_region_published.csv) | 489,762 | 7,656 | 2026-01-30T08:23:31.655328 |
| Demand per local authority, England | [la_england_pathways_demand_published.csv](https://api.neso.energy/dataset/e5e8eb8e-9fbd-4355-b4ad-9bbf00569d15/resource/c3a261a4-94e9-4d75-b0de-d3805b0b5ae8/download/la_england_pathways_demand_published.csv) | 13,370,607 | 206,016 | 2026-01-30T08:21:33.560888 |
| Demand per local authority, Scotland | [la_scotland_pathways_demand_published.csv](https://api.neso.energy/dataset/e5e8eb8e-9fbd-4355-b4ad-9bbf00569d15/resource/67d699eb-c5e9-42cd-a57a-74fcc52bcea9/download/la_scotland_pathways_demand_published.csv) | 1,488,029 | 22,272 | 2026-01-30T08:19:49.400933 |
| Demand per local authority, Wales | [la_wales_pathways_demand_published.csv](https://api.neso.energy/dataset/e5e8eb8e-9fbd-4355-b4ad-9bbf00569d15/resource/ccb3dfc8-ab4a-4f32-b944-8eced2e87bff/download/la_wales_pathways_demand_published.csv) | 989,626 | 15,312 | 2026-01-30T08:18:41.157016 |
| tRESP GSP areas (GIS) | [tresp_gsp_areas.gpkg](https://api.neso.energy/dataset/e5e8eb8e-9fbd-4355-b4ad-9bbf00569d15/resource/59a5ec35-8fec-4b84-ba8c-236d97823178/download/tresp_gsp_areas.gpkg) | 5,394,432 | n/a | 2026-01-30T08:18:03.718093 |
| RESP nations and regions (GIS) | [resp_boundaries_202511_bfc_27700.gpkg](https://api.neso.energy/dataset/e5e8eb8e-9fbd-4355-b4ad-9bbf00569d15/resource/4fdf4204-784f-4bab-aa81-f80480673dab/download/resp_boundaries_202511_bfc_27700.gpkg) | 58,142,720 | n/a | 2026-01-30T08:16:55.769781 |
| Building-block and GSP-name lists (workbook) | [lists-of-tresp-pathways-building-blocks-and-of-tresp-gsp-areas-with-names.xlsx](https://api.neso.energy/dataset/e5e8eb8e-9fbd-4355-b4ad-9bbf00569d15/resource/11c36b60-eee5-45e9-b0da-6240e6e60d1c/download/lists-of-tresp-pathways-building-blocks-and-of-tresp-gsp-areas-with-names.xlsx) | 41,878 | n/a | 2026-01-30T08:15:29.726307 |

- **There are no DOC resources in this package**, so there is no document to download. The
  vendor's own package page is [tresp-demand-pathways](https://www.neso.energy/data-portal/tresp-demand-pathways);
  its per-dataset dictionary pages (for example
  [tresp_demand_pathways_per_grid_supply_point_area](https://www.neso.energy/data-portal/tresp-demand-pathways/tresp_demand_pathways_per_grid_supply_point_area))
  are the source of the column descriptions below.
- **The five CSVs also exist as CKAN datastore tables** (field info records `datastore_active`
  for them). gridflow captures the uploaded file, not the datastore dump, so `url_type` is
  `upload` and the vintage is `ckan_last_modified` (ADR-030, ADR-033).
- **The two GPKG files are GIS**: kept in bronze as immutable captures, not loaded to
  silver. GPKG is GeoPackage (SQLite). The GSP file holds the tRESP GSP-area polygons that
  `tresp_gsp_area` refers to; the vendor warns that DNO feeding-area definitions may not
  split by licence area, may have gaps or overlaps when aggregated to Great Britain and may
  vary over time, but that the tRESP GSP areas are the authoritative interpretation for
  the tRESP outputs. The RESP file holds the nation and region polygons that `resp_region` refers
  to (its filename dates the boundary set `202511`, EPSG:27700 by the `27700` in the
  filename; the CRS inside the file is `TODO: verify`).
- **The workbook** has three sheets read as children. `tRESP Building Blocks` and
  `tRESP GSP Areas with Names` are silver reference families (below). `tRESP BB list - old`
  stays held: its table has a blank row 47 then a live data row 48, which no ADR-037
  recipe can read faithfully (FACTS section "tresp_demand_pathways_files"). Its 44 populated
  data rows have no duplicate or blank keys; the hold concerns only the reader mechanism.
  The old sheet is superseded by the current Building Blocks sheet in purpose, but
  `TODO: verify` whether NESO regards it as retired (the workbook states no status).

## Families

**What applies to all seven families.**

*Identity and selection.* Each CSV family has exactly one resource, so each has exactly one
capture and one header epoch (`dataset_version` `1+e1`). The record sets `latest` to
`whole_capture` per `resource_id` (`latest_partition: resource_id`). A later NESO re-upload
of a resource would add a new whole capture and `_latest` would take it whole; a bronze
capture is never edited. The vendor key is the tuple in each family's "Entity key" line
below, plus the engine-stamped `resource_id` (not a vendor column). It is **unique on every
full body, with zero duplicate tuples and zero null key cells** (FACTS g3; confirmed on the
silver rows 2026-10-10 for the GSP family); NESO does not state a composite-uniqueness
guarantee (`TODO: verify` vendor-declared uniqueness). That affects nothing today: selection
is by whole capture, not by key. Because each family holds one capture, `_latest` equals
the base row count in every family.

*The two clocks (all seven families).*

1. **Vintage: `ckan_last_modified`.** `published_at` and `available_at` are the CKAN
   `last_modified` of the captured file, both equal. For these families that is
   2026-01-30 (times per family below). It is **not** the capture time and **not** the
   projection year (ADR-030). An as-of query is `WHERE available_at <= :as_of`
   (RULINGS 597). With one capture, a model asking "what did NESO publish by date D"
   sees all rows from 2026-01-30 onward and none before.
2. **Event time: none.** The record has `temporal: none`, so **`timestamp_utc` is the
   capture time** (2026-10-08, times per family below) and `event_time` equals it on
   every row. It carries no information about the projection date. Do not use it for a time
   axis. The projection date is the vendor's `Year` label, held as `projection_year`
   (int64): the vendor dictionary says it is the year the pathway value is provided for, with
   the volume taken at 31 March. It is a date label, not an issue time: no row has an issue
   time, and the publication of all projections is the single vintage above (FACTS T03). The label is the year in which the 31 March falls; for stock
   quantities (counts) this fixes the observation date. For annual energy (GWh) it does
   **not** establish the interval covered (the hold; see Holds). No timezone issue arises,
   since neither clock is a local civil time.

*Units (vendor dictionary only).* The dictionary for the `Unit` column reads "Number or
square metre (m2) or GWh", and `Value` is "tRESP Pathway value" ("Indicative tRESP Pathway
value" in the local-authority files). The dictionary gives no unit on `Value` itself and
no per-block mapping; the per-block mapping comes from the **vendor's building-block
reference sheet** (the workbook's `tRESP Building Blocks` sheet, silver family
`tresp_building_block_definitions`, whose `Units` text is NESO's), matched to the exact
`Unit` string in the CSV rows (FACTS g4). `unit` stays a row column: never apply one scalar
unit to `value`. Mapping for the 12 demand blocks:

| Block id | Technology and detail (vendor reference sheet) | Sheet `Units` | CSV `Unit` |
|---|---|---|---|
| `Lct_BB001` | Electric Vehicles: Pure Electric (Vans, Cars & Motorbikes) | Number | `Number` |
| `Lct_BB002` | Electric Vehicles: Plug-in-hybrid (Vans, Cars and Motorbikes) | Number | `Number` |
| `Lct_BB003` | Electric Vehicles: Pure Electric (Buses, Coaches and HGVs) | Number | `Number` |
| `Lct_BB004` | Electric Vehicles: Plug-in-hybrid (Buses, Coaches and HGVs) | Number | `Number` |
| `Lct_BB005` | Heat Pumps: Domestic - Non-hybrid | Number | `Number` |
| `Lct_BB006` | Heat Pumps: Domestic – Hybrid | Number | `Number` |
| `Dem_BB005_1` | Heat Pumps: Industrial & Commercial Heat Pumps excl. processes (incl. Hybrid) | Annual Demand (GWh) | `GWh` |
| `Dem_BB005_2` | Heat Pumps: Industrial & Commercial Heat Pumps excl. processes (incl. Hybrid) | Surface Area | `m2` |
| `Lct_BB009` | District Heating: Domestic customers on Heat Pump-Supplied Networks | Number | `Number` |
| `Lct_BB014` | Airconditioning Units: AC Domestic Units | Number | `Number` |
| `Lct_BB015_1` | Airconditioning Units: AC Industrial & Commercial Units | Annual Demand (GWh) | `GWh` |
| `Lct_BB015_2` | Airconditioning Units: AC Industrial & Commercial Units | Surface Area | `m2` |

Each of the five demand families carries exactly these 12 block ids, and exactly 8 ids
carry `Number`, 2 carry `GWh`, 2 carry `m2` (measured on silver 2026-10-10). A `Number`
value is a count of the named technology or customer component; the sheet gives no other
unit, and `TODO: verify` whether counts are stocks at 31 March (the dictionary says the volume is taken
at 31 March but does not call it a stock). Do not sum values across blocks or units.
The `_1`/`_2` suffix pairs are two measures of one technology (annual energy, then surface
area), not two vintages.

*Three vocabulary notes.* (a) `Pathway` has exactly three values: `tRESP - HT`,
`tRESP - EE`, `tRESP - HE`. The short-term section (2025 to 2035) is published once,
under `tRESP - HT`; the three long-term pathways (2035 to 2050) all start from that shared
boundary year, so a boundary-year label appears under more than one pathway. That is not a
duplicate, and the pathway is part of the key. Per the dictionary the horizons are
2025-2035 short-term and 2035-2050 long-term; this page states no measured year range for
the held families. (b) Spelling of geography labels is preserved as published. (c) Block
ids are stored as published, with no normalisation; the suffixed ids are different
variables and must never be suffix-stripped to force a join to FES.

*Sentinels and missing values (FACTS g5).* NESO declares no sentinel or null token. In
every column of every CSV there are **zero** blank, `-`, `N/A`, `NA` or `n/a` cells, and
every `Value` casts to float64 and every `Year` to int64 with zero failures. Silver has
**0 nulls in every column of every demand family** (2026-10-10). A numeric zero in `Value`
is a zero: no vendor source defines zero as missing, so it is never converted to null or
filled. The record has no null-token map. A downstream consumer must not treat zeros as
absent technology without a vendor statement.

*Block-id correspondence to FES (FACTS, exact-id comparison).* Against the FES building-block
definitions of 2021-2025, 8 of the 12 demand ids match exactly; the four suffixed ids
`Dem_BB005_1/_2` and `Lct_BB015_1/_2` have no exact match (and no FES definition covers
them). Against the FES main building-block tables of 2022-2025 only 7 of 12 match, because
`Lct_BB014` is also absent. Matching names is not proof that definitions are unchanged.
`TODO: verify` with NESO an explicit tRESP-to-FES mapping.

*Silver layout (all seven).* One Parquet file per family under
`C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`, from runs
`2026-10-08T11-39` to `2026-10-08T11-40` (one run per family: the two reference tables
11-39-46, GSP 11-39-50, England 11-39-54, Scotland 11-39-57, Wales 11-40-02, RESP region
11-40-06). The `year=`/`month=` partition is the **capture** date. Lineage columns
appended to the vendor columns: `resource_id`, `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version`. All timestamps are tz-aware UTC. The two workbook children add
`child_id` (the sheet name) and `child_crc32` after the vendor columns; both children come
from the same workbook capture.

### `tresp_building_block_definitions`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Demand/ Generation/ Storage | `demand_generation_storage` | string | — | no | — | — |
| Technology | `technology` | string | — | no | — | — |
| FES BB ID Number | `fes_bb_id_number` | string | — | no | — | — |
| Technology Detail | `technology_detail` | string | — | yes | — | — |
| Units | `units` | string | — | no | — | — |

- Entity key: `resource_id`, `fes_bb_id_number`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The workbook sheet `tRESP Building Blocks` (`header_row: 1`, columns A:E, last row 36). **35
rows**: 12 `Demand`, 5 `Storage`, 18 `Generation` (matching the vendor notes' "35 building
blocks"), all keys distinct, none blank; `technology_detail` is null on 7 rows (generation
blocks with no sub-detail) and nowhere else. This is the vendor's dictionary for
`building_block_id` in this package and in @./tresp-generation-pathways.md; its Demand rows
are the table above. The join to a pathway family is `building_block_id` =
`fes_bb_id_number` (the column is named for FES but the ids are tRESP's, so the four
suffixed ids appear here and in no FES table). The 35 rows are the whole table, not a time
series: a re-upload replaces it whole. Both clocks as above: `published_at` = `available_at`
= 2026-01-30T08:15:29.726307 UTC (the workbook's `last_modified`); `timestamp_utc` =
2026-10-08T11:39:46.157281 UTC. Silver: **35 rows**, 16 columns.

### `tresp_demand_pathways_files`

- Kind: files · archetype: SCN · refresh: adhoc · empty allowed: no
- files: catalogue only

This is the catalogue family for the three non-CSV resources (the two GPKG GIS files and
the workbook container). It has no silver output of its own; the workbook's sheets feed
`tresp_building_block_definitions` and `tresp_gsp_area_names` as children. Bronze holds
the three captures of 2026-10-08.

### `tresp_demand_pathways_gsp`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building_block_id | `building_block_id` | string | — | no | — | — |
| tRESP_GSP_area | `tresp_gsp_area` | string | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Value | `value` | float64 | — | no | — | — |
| Unit | `unit` | string | — | no | — | Number or square metre (m2) or GWh |
| DNO_licence_area | `dno_licence_area` | string | — | no | — | — |

- Entity key: `resource_id`, `building_block_id`, `tresp_gsp_area`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Silver: 160,776 rows, 16 columns. HELD (E-SEM): no values shown.** Vintage:
`published_at` = `available_at` = 2026-01-30T08:24:47.341529 UTC; `timestamp_utc` =
2026-10-08T11:39:50.139049 UTC (capture time). The finest geography. `tresp_gsp_area` is
NESO's tRESP Grid Supply Point feeding-area code (GSP-group treatment in Scotland, per the
package notes); the vendor refers to the GSP shapefile for its definition. Distinct codes:
**231**, and the set is identical, with none unmatched either side, to the 231 codes of
`tresp_gsp_area_names` (join on `tresp_gsp_area`). Its code format is not an EIC and not an
interchangeable regional-FES GSP id (@./fes-electricity-demand-summary-data-table-ed1.md
has a separate FES geography); never join it to EIC codes
(@../../../20-domain/concepts/eic-codes.md). `dno_licence_area` (per the dictionary, the DNO licence area the pathway value
is provided for) has **14** distinct values. Measured on this capture: each of the 231 GSP areas carries
exactly one `dno_licence_area` (0 GSP areas with more than one). Whether the vendor
guarantees that mapping in future captures is `TODO: verify`. Column order differs from the
local-authority files (`Unit` before `DNO_licence_area`, `Value` before `Unit`); read by
name.

### `tresp_demand_pathways_la_england`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building_block_id | `building_block_id` | string | — | no | — | — |
| LAD24CD | `lad24cd` | string | — | no | — | — |
| LAD24NM | `lad24nm` | string | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Unit | `unit` | string | — | no | — | Number or square metre (m2) or GWh |
| Value | `value` | float64 | — | no | — | — |

- Entity key: `resource_id`, `building_block_id`, `lad24cd`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Silver: 206,016 rows, 16 columns. HELD (E-SEM): no values shown.** Vintage:
`published_at` = `available_at` = 2026-01-30T08:21:33.560888 UTC; `timestamp_utc` =
2026-10-08T11:39:54.204836 UTC. Indicative values per English local authority.
`lad24cd` and `lad24nm` are the Office for National Statistics code and name for local
authority districts and unitary authorities as at **31 December 2024** (vendor dictionary),
so the code is the stable id and is used in the key; the name is kept alongside. Distinct
`lad24cd`: **296**. Codes reflect ONS geography as at that date. The vendor
attributes the pathways to local authorities from the GSP-area level and does not publish
the method (`TODO: verify` the disaggregation method).

### `tresp_demand_pathways_la_scotland`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building_block_id | `building_block_id` | string | — | no | — | — |
| LAD24CD | `lad24cd` | string | — | no | — | — |
| LAD24NM | `lad24nm` | string | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Unit | `unit` | string | — | no | — | Number or square metre (m2) or GWh |
| Value | `value` | float64 | — | no | — | — |

- Entity key: `resource_id`, `building_block_id`, `lad24cd`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Silver: 22,272 rows, 16 columns. HELD (E-SEM): no values shown.** Vintage:
`published_at` = `available_at` = 2026-01-30T08:19:49.400933 UTC; `timestamp_utc` =
2026-10-08T11:39:57.658066 UTC. Same shape and semantics as the England file, for
Scottish local authorities. Distinct `lad24cd`: **32**.

### `tresp_demand_pathways_la_wales`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building_block_id | `building_block_id` | string | — | no | — | — |
| LAD24CD | `lad24cd` | string | — | no | — | — |
| LAD24NM | `lad24nm` | string | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Unit | `unit` | string | — | no | — | Number or square metre (m2) or GWh |
| Value | `value` | float64 | — | no | — | — |

- Entity key: `resource_id`, `building_block_id`, `lad24cd`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Silver: 15,312 rows, 16 columns. HELD (E-SEM): no values shown.** Vintage:
`published_at` = `available_at` = 2026-01-30T08:18:41.157016 UTC; `timestamp_utc` =
2026-10-08T11:40:02.562200 UTC. Same shape and semantics as the England file, for Welsh
local authorities. Distinct `lad24cd`: **22**.

### `tresp_demand_pathways_resp_region`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building_block_id | `building_block_id` | string | — | no | — | — |
| RESP_region | `resp_region` | string | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Value | `value` | float64 | — | no | — | — |
| Unit | `unit` | string | — | no | — | Number or square metre (m2) or GWh |

- Entity key: `resource_id`, `building_block_id`, `resp_region`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Silver: 7,656 rows, 15 columns. HELD (E-SEM): no values shown.** Vintage:
`published_at` = `available_at` = 2026-01-30T08:23:31.655328 UTC; `timestamp_utc` =
2026-10-08T11:40:06.710260 UTC. The coarsest geography: the RESP nations and regions of
the RESP boundary file. `resp_region` has **11** distinct labels, kept exactly as
published. The dictionary names no external code standard for them (`TODO: verify` any
code scheme; none is evidenced).

### `tresp_gsp_area_names`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| tresp_gsp_area | `tresp_gsp_area` | string | — | no | — | — |
| tresp_gsp_area_name | `tresp_gsp_area_name` | string | — | no | — | — |

- Entity key: `resource_id`, `tresp_gsp_area`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

The workbook sheet `tRESP GSP Areas with Names` (`header_row: 1`, columns A:B, last row
232). **231 rows**, 231 distinct `tresp_gsp_area` codes, none blank, no nulls: the lookup
from the GSP feeding-area code to a name. Names typically carry a substation name, often a voltage, and the DNO, for
example code `_L@ABHA1` is "tRESP Abham 132kV NGED". The name is a label for
display; do not use it as a key. Vintage and capture as for the building-block sheet above
(2026-01-30T08:15:29.726307 UTC; 2026-10-08T11:39:46.157281 UTC). Silver: **231 rows**,
13 columns.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad-hoc

NESO publishes the tRESP irregularly. The catalogue entry is the first tRESP release
(created 2026-01-28, last metadata change 2026-01-30). There is no scheduled refresh in
gridflow (the batch was captured once, 2026-10-08, by the portal sweep). Whether NESO will
re-upload to the same resource id or add a new resource for a later tRESP release is
unknown, and the vendor gives no release or version identifier: `TODO: verify` with NESO.
If it adds new resources, the registry needs a new record for each; if it re-uploads, a
new capture is added automatically and `_latest` follows it.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `tresp_demand_pathways_gsp`: held: TODO: for the annual-energy building blocks (`Unit` = GWh), what interval does the `Year` label cover — the financial year ending 31 March of that year, the calendar year, or another interval? The tRESP dictionary dates volumes at 31 March but states no interval for annual energy. Also: which FES definition applies to the suffixed ids `Dem_BB005_1/_2`, `Lct_BB015_1/_2` (no exact FES building-block id). (unit E-SEM)
- `tresp_demand_pathways_la_england`: held: TODO: for the annual-energy building blocks (`Unit` = GWh), what interval does the `Year` label cover — the financial year ending 31 March of that year, the calendar year, or another interval? The tRESP dictionary dates volumes at 31 March but states no interval for annual energy. Also: which FES definition applies to the suffixed ids `Dem_BB005_1/_2`, `Lct_BB015_1/_2` (no exact FES building-block id). (unit E-SEM)
- `tresp_demand_pathways_la_scotland`: held: TODO: for the annual-energy building blocks (`Unit` = GWh), what interval does the `Year` label cover — the financial year ending 31 March of that year, the calendar year, or another interval? The tRESP dictionary dates volumes at 31 March but states no interval for annual energy. Also: which FES definition applies to the suffixed ids `Dem_BB005_1/_2`, `Lct_BB015_1/_2` (no exact FES building-block id). (unit E-SEM)
- `tresp_demand_pathways_la_wales`: held: TODO: for the annual-energy building blocks (`Unit` = GWh), what interval does the `Year` label cover — the financial year ending 31 March of that year, the calendar year, or another interval? The tRESP dictionary dates volumes at 31 March but states no interval for annual energy. Also: which FES definition applies to the suffixed ids `Dem_BB005_1/_2`, `Lct_BB015_1/_2` (no exact FES building-block id). (unit E-SEM)
- `tresp_demand_pathways_resp_region`: held: TODO: for the annual-energy building blocks (`Unit` = GWh), what interval does the `Year` label cover — the financial year ending 31 March of that year, the calendar year, or another interval? The tRESP dictionary dates volumes at 31 March but states no interval for annual energy. Also: which FES definition applies to the suffixed ids `Dem_BB005_1/_2`, `Lct_BB015_1/_2` (no exact FES building-block id). (unit E-SEM)

The silver outputs of these five families exist on disk, but they are **held**: not
eligible for publication or for model use until unit E-SEM has an answer (RULINGS 605;
held at activation, RULINGS 610). The hold is the same for all five and has two parts:

1. **Annual-energy interval.** The vendor dates every volume at 31 March of the `Year`
   label (a point in time), which is enough for counts and for surface areas, but a
   GWh value is a flow over a period and the dictionary does not say which period: the
   financial year ending that 31 March, the calendar year, or something else. Two blocks
   per family are annual energy (`Dem_BB005_1`, `Lct_BB015_1`). Until this is answered, a
   GWh value cannot be placed on a calendar axis or compared with outturn demand. Settles it:
   a NESO tRESP methodology or building-block definition naming the interval. This is a
   **domain-truth question** (vendor semantics); gridflow does not guess it. The hold
   applies to the whole family, not only to the GWh rows: the registry holds the output as
   one unit.
2. **Suffixed block ids.** `Dem_BB005_1`, `Dem_BB005_2`, `Lct_BB015_1` and `Lct_BB015_2`
   have no exact FES building-block id, so which FES definition governs them is not
   established. Settles it: a NESO tRESP-to-FES building-block mapping, or definitions that
   cover those ids.

The hold is applied per family (the registry holds the whole output, all 12 blocks), so
the eight `Number` blocks are not published separately either. The sibling generation package has
no equivalent hold (installed MW at 31 March).

Not held: `tresp_building_block_definitions` and `tresp_gsp_area_names` (eligible reference
tables). Not a hold but still open: the workbook's `tRESP BB list - old` sheet (reader
mechanism; proposed family `tresp_building_block_definitions_old`, record pending).

**Activation (2026-10-10, master `0bc09a0`, PR #100).** The frozen records merged
triple-green (CI pass twice, Sol diff review APPROVE on pass 1 with no findings,
VERIFICATION passed; RULINGS 609) and were activated with cutoff 2026-10-08, no prior
silver, nothing overwritten (RULINGS 610). Row counts equal the plan: 160,776 · 206,016 ·
22,272 · 15,312 · 7,656 (demand, in the order GSP, England, Scotland, Wales, RESP region),
and 35 and 231 for the two reference tables. Reconcile `--all --cutoff 2026-10-08` exited
0 (85 families, 0 gaps, 10 adjudicated, 0 stale), so there is no open gap and no
adjudication for this package (gridflow `@.planning/v0.22-RESULTS.md`, section SCN-1a).
No engine change was needed; the `Year` and `Value` columns are ordinary int64 and
float64 columns (ADR-042).

References: gridflow `@.planning/phases/v0.22-K-SCN-1/K-SCN-1-FACTS.md` (section SCN-1a,
g1 to g6, T01 to T04), `@.planning/phases/v0.22-SC-scenario-mechanism/RESEARCH.md`
(tRESP physical headers), `@.planning/RULINGS.md` (597, 599, 600, 603, 605, 609, 610),
`@src/gridflow/connectors/neso_data_portal/registry/tresp-demand-pathways.json`,
`@docs/neso_data_portal/eligibility.md`,
`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`,
`@docs/DECISION_LOG/ADR-033-neso-registry-upload-leg.md`,
`@docs/DECISION_LOG/ADR-037-neso-container-readers-and-covered-harness.md`,
`@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md`,
`@docs/DECISION_LOG/ADR-042-neso-scenario-unpivot-and-edition.md`.
