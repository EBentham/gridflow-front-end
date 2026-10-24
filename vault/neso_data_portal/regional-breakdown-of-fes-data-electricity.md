---
source: "neso_data_portal"
package: "regional-breakdown-of-fes-data-electricity"
dataset_keys: ["fes_regional_demand_active_power", "fes_regional_dg_gt_1mw", "fes_regional_dg_lt_1mw", "fes_regional_dsr", "fes_regional_gsp_info", "fes_regional_storage_gt_1mw", "fes_regional_storage_gt_1mw_pre2023", "fes_regional_storage_lt_1mw", "fes_regional_storage_lt_1mw_pre2023"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Regional breakdown of FES data (Electricity)

This package is NESO's regional cut of its **Future Energy Scenarios (FES)** for electricity: for
each FES edition from 2021 to 2024, projected demand, demand side response, distributed
generation and distributed storage, broken down by place. The vendor describes it as long-term
electricity forecasts per region, where a region is a Grid Supply Point (GSP) or a large site
connected directly to the transmission system, and the places are identified by short codes
(GSP identifiers in the demand and DSR tables, and `etys_location` or `location` codes in the
generation and storage tables). Every row is
one scenario, one place and one `year` label (kept here as `year_label`, a two-digit label, see
below), and carries several measures side by side (a capacity and three characteristic-condition
values for generation and storage; three condition values for demand). It answers "where, on
the network, does each FES edition expect demand, response, generation and storage to be, for
each scenario and year label?" and is a scenario input for regional features in models, not a
measurement and not a forecast issued on a date.

**Six things to know before using any of it.**

1. **Four of the nine output families are held** (unit E-SEM): `fes_regional_dg_gt_1mw`,
   `fes_regional_dg_lt_1mw`, `fes_regional_gsp_info` and `fes_regional_storage_lt_1mw`,
   plus one resource (the 2021 storage greater-than-1 MW file) held at resource level. Silver
   exists for the families; nothing is published from the held ones. For them this page gives
   schema, row counts, clocks and key facts, and **never data values, ranges or example rows**.
   The five eligible families are described with their values.
2. **`year_label` is a two-digit label, and its meaning depends on the family.** It is not a
   calendar year and the page never converts it to one (FACTS g1; see "The year label" below).
3. **No temporal recipe.** `timestamp_utc` is gridflow's capture time (2026-10-08), not a
   projection date. The vintage is the CKAN `last_modified` of each edition's file, which is
   `available_at`.
4. **One capture per resource, one edition per resource.** Editions are independent: a 2023
   row and a 2024 row for the same place coexist and are never superseded by one another.
5. **Place codes are not a clean foreign key.** The demand table carries GSP, extra and
   direct-connect identifiers that do not all appear in the same-edition GSP lookup (see its
   family section for the counts). The DSR `gsp` codes all match the lookup in every edition
   measured, but the join is still not guaranteed in general. The generation and storage tables
   carry `etys_location` (distributed generation, and storage below 1 MW) or `location` (storage
   above 1 MW) codes; whether `location` is an ETYS code is `TODO: verify`. Never inner-join to
   the lookup.
6. **There are no DOC resources in this package**, so there is no document to download. All 27
   resources are CSV uploads (listed in full below). The vendor's per-resource dictionary pages,
   for example the
   [2024 demand dictionary](https://www.neso.energy/data-portal/regional-breakdown-fes-data-electricity/regional_breakdown_of_2024_fes_demand_active_power),
   are the source of the column meanings below.

The shared research is gridflow
`@.planning/phases/v0.22-K-SCN-1/K-SCN-1-FACTS.md` (section SCN-1b) and the verification is
`@.planning/phases/v0.22-K-SCN-1b/VERIFICATION.md`. Sibling scenario packages:
@./tresp-demand-pathways.md, @./tresp-generation-pathways.md and
@./fes-electricity-demand-summary-data-table-ed1.md.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| FES 2021 Grid Supply Point Info | CSV | upload | `41fb4ca1-7b59-4fce-b480-b46682f346c9` |
| FES 2022 Grid Supply Point Info | CSV | upload | `000d08b9-12d9-4396-95f8-6b3677664836` |
| FES 2023 Grid Supply Point Info | CSV | upload | `805e20e4-6a8b-4113-9d2d-09efa0a4bbb9` |
| FES 2024 Grid Supply Point Info | CSV | upload | `21c2b09c-24ff-4837-a3b1-b6aea88f8124` |
| Regional Breakdown of 2021 FES: Demand (Active Power) | CSV | upload | `3360c832-acc3-4656-8a38-f0bdf57bde88` |
| Regional Breakdown of 2021 FES: Demand Side Response (DSR) | CSV | upload | `180d9908-7c4a-4db7-b6f1-92067209854c` |
| Regional Breakdown of 2021 FES: Demands from distributed storage sites less than 1 MW | CSV | upload | `f0db3dc8-4e8f-40e0-9def-58e0bca11e47` |
| Regional Breakdown of 2021 FES: Distributed generation greater than 1 MW | CSV | upload | `fc6e9d6e-0995-447a-8819-2099c845ad7e` |
| Regional Breakdown of 2021 FES: Distributed generation less than 1 MW | CSV | upload | `e05c34ec-1a0b-496c-b098-e35d4f998dc9` |
| Regional Breakdown of 2022 FES: Demand (Active Power) | CSV | upload | `6a1d99c2-a3c5-4ae0-b66a-21e4c15a9ae6` |
| Regional Breakdown of 2022 FES: Demand Side Response (DSR) | CSV | upload | `3b32009a-55cb-4493-9dd0-a1fdd61d5d28` |
| Regional Breakdown of 2022 FES: Demands from distributed storage sites greater than 1 MW | CSV | upload | `ae5e3faf-b264-478e-82a5-fe0eb3101bba` |
| Regional Breakdown of 2022 FES: Demands from distributed storage sites less than 1 MW | CSV | upload | `08f1f7f3-0448-4e80-aeb6-0ef082d86e8f` |
| Regional Breakdown of 2022 FES: Distributed generation greater than 1 MW | CSV | upload | `162bdb05-1d05-46f8-b3cd-55a86ef65b8e` |
| Regional Breakdown of 2022 FES: Distributed generation less than 1 MW | CSV | upload | `8cd8a80a-9c36-436c-9014-8666c77e95d7` |
| Regional Breakdown of 2023 FES: Demand (Active Power) | CSV | upload | `66d309b9-0202-48ad-a7dc-eeafd9f53a65` |
| Regional Breakdown of 2023 FES: Demand Side Response (DSR) | CSV | upload | `a6138c38-d173-4040-b853-de659c660e38` |
| Regional Breakdown of 2023 FES: Demand from distributed storage sites greater than 1 MW | CSV | upload | `0465e5a3-ff3a-4e95-ac66-f59afd54cfe3` |
| Regional Breakdown of 2023 FES: Demand from distributed storage sites less than 1 MW | CSV | upload | `86f90e3f-2a48-4bfc-80a9-9ff65c353d6e` |
| Regional Breakdown of 2023 FES: Distributed generation greater than 1 MW | CSV | upload | `922a4355-ec87-4744-95ef-bdba58610f06` |
| Regional Breakdown of 2023 FES: Distributed generation less than 1 MW | CSV | upload | `4b4ec273-69b0-4bcd-bd50-b777af6f1052` |
| Regional Breakdown of 2024 FES: Demand (Active Power) | CSV | upload | `7bd643c0-6aad-41ac-aa59-92b68992d9a4` |
| Regional Breakdown of 2024 FES: Demand from distributed storage sites greater than 1 MW | CSV | upload | `eba5fd0a-ea22-4c00-84c2-35260e328736` |
| Regional Breakdown of 2024 FES: Demand from distributed storage sites less than 1 MW | CSV | upload | `0a1fce9e-8711-4017-bdef-867c0ab040a1` |
| Regional Breakdown of 2024 FES: Distributed generation greater than 1 MW | CSV | upload | `c50eb94e-2e6a-43c6-b72a-ed9ae590b88b` |
| Regional Breakdown of 2024 FES: Distributed generation less than 1 MW | CSV | upload | `31ad4fd0-f67e-47f6-89bc-1bebda19eb25` |

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Regional Breakdown of 2021 FES: Demands from distributed storage sites greater than 1 MW | CSV | upload | `b954c63f-c108-4e71-9b43-b249d0d92a1b` | the 2021 body opens with a two-line preamble (a generated-file note and a blank line) before its header on physical line 3, which the CSV reader cannot skip, and its table repeats one (scenario, tech, year, location) tuple three times (table rows 11776-11778) so the entity key is not unique; re-disposition only after a supported header-row recipe and an authorised duplicate policy, or a corrected NESO upload (a new last_modified) (E-SEM) |

**Reading the disposition tables.** "SILVER" is a disposition of the *resource* (it is read to
silver), which is separate from whether the *family output* is eligible: 26 of the 27 resources
are SILVER, but four families are held at output level (see Holds), and one SILVER resource
(the 2022 GSP lookup) fails to read (see its family). The single HOLD resource has bronze only.

**Downloads and captures.** All 27 resources have `url_type: upload` and were captured once, on
2026-10-08, from `api.neso.energy` (bronze under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`, one CSV and one sidecar per
resource). Sizes and row counts are from FACTS (bytes are the physical body size; rows are table
rows measured over the complete body). The package was created in the catalogue on 2021-07-06,
last had its metadata changed on 2025-10-15, has no version string, and carries 20 catalogue tags.
Licence id `ESO`, "NESO Open Data Licence".

| Resource | Edition | Download | Bytes | Data rows | CKAN `last_modified` | Family |
|---|---|---|---:|---|---|---|
| Demand (active power) | 2021 | [fes2021_regional_breakdown_active_power.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/3360c832-acc3-4656-8a38-f0bdf57bde88/download/fes2021_regional_breakdown_active_power.csv) | 10,986,770 | 352,284 | 2021-07-06T11:06:43.990644 | `fes_regional_demand_active_power` |
| Demand (active power) | 2022 | [fes2022_regional_breakdown_active_power.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/6a1d99c2-a3c5-4ae0-b66a-21e4c15a9ae6/download/fes2022_regional_breakdown_active_power.csv) | 10,661,855 | 340,920 | 2022-07-15T13:37:46.607400 | `fes_regional_demand_active_power` |
| Demand (active power) | 2023 | [fes2023_regional_breakdown_active_power.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/66d309b9-0202-48ad-a7dc-eeafd9f53a65/download/fes2023_regional_breakdown_active_power.csv) | 10,330,209 | 329,556 | 2023-08-29T08:50:58.979654 | `fes_regional_demand_active_power` |
| Demand (active power) | 2024 | [fes2024_regional_breakdown_active_power.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/7bd643c0-6aad-41ac-aa59-92b68992d9a4/download/fes2024_regional_breakdown_active_power.csv) | 8,153,655 | 257,964 | 2024-07-15T06:43:07.255666 | `fes_regional_demand_active_power` |
| DG greater than 1 MW | 2021 | [fes2021_regional_breakdown_distributed_generation.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/fc6e9d6e-0995-447a-8819-2099c845ad7e/download/fes2021_regional_breakdown_distributed_generation.csv) | 4,055,763 | 103,431 | 2021-07-06T10:59:37.680231 | `fes_regional_dg_gt_1mw` |
| DG greater than 1 MW | 2022 | [fes2022_regional_breakdown_distributed_generation.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/162bdb05-1d05-46f8-b3cd-55a86ef65b8e/download/fes2022_regional_breakdown_distributed_generation.csv) | 4,701,143 | 111,700 | 2022-07-15T13:35:02.326000 | `fes_regional_dg_gt_1mw` |
| DG greater than 1 MW | 2023 | [fes2023_regional_breakdown_distributed_generation.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/922a4355-ec87-4744-95ef-bdba58610f06/download/fes2023_regional_breakdown_distributed_generation.csv) | 4,076,150 | 107,234 | 2023-07-07T13:38:06.066671 | `fes_regional_dg_gt_1mw` |
| DG greater than 1 MW | 2024 | [fes2024_regional_breakdown_distributed_generation.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/c50eb94e-2e6a-43c6-b72a-ed9ae590b88b/download/fes2024_regional_breakdown_distributed_generation.csv) | 4,255,817 | 75,106 | 2024-07-15T06:47:00.809819 | `fes_regional_dg_gt_1mw` |
| DG less than 1 MW | 2021 | [fes2021_regional_breakdown_sub1mw_generation.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/e05c34ec-1a0b-496c-b098-e35d4f998dc9/download/fes2021_regional_breakdown_sub1mw_generation.csv) | 7,005,723 | 171,531 | 2021-07-06T10:54:05.003828 | `fes_regional_dg_lt_1mw` |
| DG less than 1 MW | 2022 | [fes2022_regional_breakdown_sub1mw_generation.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/8cd8a80a-9c36-436c-9014-8666c77e95d7/download/fes2022_regional_breakdown_sub1mw_generation.csv) | 8,733,877 | 235,075 | 2022-07-15T13:35:59.358715 | `fes_regional_dg_lt_1mw` |
| DG less than 1 MW | 2023 | [fes2023_regional_breakdown_sub1mw_generation.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/4b4ec273-69b0-4bcd-bd50-b777af6f1052/download/fes2023_regional_breakdown_sub1mw_generation.csv) | 8,466,869 | 227,671 | 2023-07-07T13:37:51.948191 | `fes_regional_dg_lt_1mw` |
| DG less than 1 MW | 2024 | [fes2024_regional_breakdown_sub1mw_generation.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/31ad4fd0-f67e-47f6-89bc-1bebda19eb25/download/fes2024_regional_breakdown_sub1mw_generation.csv) | 8,177,447 | 156,324 | 2024-07-15T06:48:05.243503 | `fes_regional_dg_lt_1mw` |
| Demand side response | 2021 | [fes2021_regional_breakdown_demand_side_response.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/180d9908-7c4a-4db7-b6f1-92067209854c/download/fes2021_regional_breakdown_demand_side_response.csv) | 940,085 | 45,384 | 2021-07-06T11:01:06.905207 | `fes_regional_dsr` |
| Demand side response | 2022 | [fes2022_regional_breakdown_demand_side_response.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/3b32009a-55cb-4493-9dd0-a1fdd61d5d28/download/fes2022_regional_breakdown_demand_side_response.csv) | 903,438 | 43,920 | 2022-07-15T13:34:19.868883 | `fes_regional_dsr` |
| Demand side response | 2023 | [fes2023_regional_breakdown_demand_side_response.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/a6138c38-d173-4040-b853-de659c660e38/download/fes2023_regional_breakdown_demand_side_response.csv) | 873,446 | 42,456 | 2023-07-07T13:35:51.589125 | `fes_regional_dsr` |
| GSP info | 2021 | [fes2021_regional_breakdown_gsp_info.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/41fb4ca1-7b59-4fce-b480-b46682f346c9/download/fes2021_regional_breakdown_gsp_info.csv) | 15,326 | 370 | 2021-07-06T10:53:01.441148 | `fes_regional_gsp_info` |
| GSP info | 2022 | [fes2022_regional_breakdown_gsp_info.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/000d08b9-12d9-4396-95f8-6b3677664836/download/fes2022_regional_breakdown_gsp_info.csv) | 15,316 | 370 (not read to silver) | 2022-07-15T13:31:25.009443 | `fes_regional_gsp_info` |
| GSP info | 2023 | [fes2023_regional_breakdown_gsp_info.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/805e20e4-6a8b-4113-9d2d-09efa0a4bbb9/download/fes2023_regional_breakdown_gsp_info.csv) | 15,269 | 370 | 2023-07-07T13:36:07.968680 | `fes_regional_gsp_info` |
| GSP info | 2024 | [fes2024_regional_breakdown_gsp_info.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/21c2b09c-24ff-4837-a3b1-b6aea88f8124/download/fes2024_regional_breakdown_gsp_info.csv) | 16,416 | 373 | 2024-07-15T06:43:26.501169 | `fes_regional_gsp_info` |
| Storage greater than 1 MW | 2023 | [fes2023_regional_breakdown_dxstorage_gt1mw.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/0465e5a3-ff3a-4e95-ac66-f59afd54cfe3/download/fes2023_regional_breakdown_dxstorage_gt1mw.csv) | 530,184 | 14,042 | 2023-07-07T13:36:43.988472 | `fes_regional_storage_gt_1mw` |
| Storage greater than 1 MW | 2024 | [fes2024_regional_breakdown_dxstorage_gt1mw.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/eba5fd0a-ea22-4c00-84c2-35260e328736/download/fes2024_regional_breakdown_dxstorage_gt1mw.csv) | 414,317 | 10,627 | 2024-07-15T06:45:04.345465 | `fes_regional_storage_gt_1mw` |
| Storage greater than 1 MW | 2021 | [fes2021_regional_breakdown_dxstorage_gt1mw.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/b954c63f-c108-4e71-9b43-b249d0d92a1b/download/fes2021_regional_breakdown_dxstorage_gt1mw.csv) | 437,570 | 11,778 after the preamble (HOLD, not read) | 2021-07-06T10:50:48.532360 | `fes_regional_storage_gt_1mw_pre2023` |
| Storage greater than 1 MW | 2022 | [fes2022_regional_breakdown_dxstorage_gt1mw.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/ae5e3faf-b264-478e-82a5-fe0eb3101bba/download/fes2022_regional_breakdown_dxstorage_gt1mw.csv) | 538,315 | 14,245 | 2022-07-15T13:33:26.428024 | `fes_regional_storage_gt_1mw_pre2023` |
| Storage less than 1 MW | 2023 | [fes2023_regional_breakdown_dxstorage_sub1mw.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/86f90e3f-2a48-4bfc-80a9-9ff65c353d6e/download/fes2023_regional_breakdown_dxstorage_sub1mw.csv) | 1,324,371 | 45,510 | 2023-07-07T13:37:11.264211 | `fes_regional_storage_lt_1mw` |
| Storage less than 1 MW | 2024 | [fes2024_regional_breakdown_dxstorage_sub1mw.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/0a1fce9e-8711-4017-bdef-867c0ab040a1/download/fes2024_regional_breakdown_dxstorage_sub1mw.csv) | 1,468,158 | 31,248 | 2024-07-15T06:45:51.492269 | `fes_regional_storage_lt_1mw` |
| Storage less than 1 MW | 2021 | [fes2021_regional_breakdown_dxstorage_sub1mw.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/f0db3dc8-4e8f-40e0-9def-58e0bca11e47/download/fes2021_regional_breakdown_dxstorage_sub1mw.csv) | 1,225,360 | 39,955 | 2021-07-06T10:48:22.393456 | `fes_regional_storage_lt_1mw_pre2023` |
| Storage less than 1 MW | 2022 | [fes2022_regional_breakdown_dxstorage_sub1mw.csv](https://api.neso.energy/dataset/963525d6-5d83-4448-a99c-663f1c76330a/resource/08f1f7f3-0448-4e80-aeb6-0ef082d86e8f/download/fes2022_regional_breakdown_dxstorage_sub1mw.csv) | 1,367,212 | 46,990 | 2022-07-15T13:36:47.954918 | `fes_regional_storage_lt_1mw_pre2023` |

- **gridflow captures the uploaded file** (not any CKAN datastore dump), so `url_type` is
  `upload` and the vintage is `ckan_last_modified` (ADR-030, ADR-033). Whether the vendor also
  serves these resources as datastore tables is not established here (`TODO: verify`).
- **One resource's `last_modified` differs from its siblings.** The 2023 demand file was last
  modified on 2023-08-29, while every other 2023 resource was last modified on 2023-07-07. The
  vendor does not say why; it is the genuine captured vintage and must not be replaced by the
  edition year.
- **The DSR table has no 2024 resource** in this package (editions 2021, 2022 and 2023 only).
  The catalogue snapshot of 2026-10-06 lists no regional resource for any edition after 2024.

## Families

**What applies to all nine families.**

*The year label (FACTS g1, vendor dictionaries).* Every projection table has a column `year`,
stored as `year_label` (int64). Its values are two-digit labels (they are not four-digit
years, and gridflow does not add the century: the record model has no arithmetic label
mapping for an ordinary column, FACTS "Year representation"; RULINGS 607). The meaning depends
on the family and is stated per family below:

| Family | Meaning of `year_label` (vendor dictionary, cited in FACTS) |
|---|---|
| `fes_regional_demand_active_power` | the financial year beginning in April and ending in March of the following year; label `25` denotes 2025/26, a start-year label |
| `fes_regional_dsr` | the same financial start-year label |
| `fes_regional_dg_gt_1mw` | capacity is present for the winter starting in the labelled year |
| `fes_regional_storage_gt_1mw`, `fes_regional_storage_gt_1mw_pre2023` | the winter starting in the labelled year |
| `fes_regional_storage_lt_1mw`, `fes_regional_storage_lt_1mw_pre2023` | the winter starting in the labelled year |
| `fes_regional_dg_lt_1mw` | **unsettled**: `TODO: verify` calendar, financial or winter period (FACTS g1; part of the hold) |
| `fes_regional_gsp_info` | none: a reference table with no year |

`edition` is the FES publication year taken from the filename (see each family's edition
map) and is **not** the century of the label. The label has no physical unit. The verification
(`@.planning/phases/v0.22-K-SCN-1b/VERIFICATION.md`, warning 1) records that no registry record
carries this meaning, which is why it is stated here. Never read `year_label` and `edition`
as the same quantity.

*Identity and selection.* Each resource is one edition of one table, so each capture is a whole
file. The record sets `latest` to `whole_capture` per `resource_id`
(`latest_partition: resource_id`): each edition's capture is its own partition, and a later NESO
re-upload of a resource would add a new whole capture and `_latest` would take that resource
whole. A bronze capture is never edited. The entity key of each family (its "Entity key" line
below) includes `resource_id` and `edition`. The key is unique on every complete nonblank body
for all measured families except the held 2021 storage resource (FACTS g3); NESO does not state
a composite-uniqueness guarantee for any of them (`TODO: verify` vendor-declared uniqueness).
That affects nothing today: selection is by whole capture, not by key.

*The two clocks (every family).*

1. **Vintage: `ckan_last_modified`.** `published_at` and `available_at` are the CKAN
   `last_modified` of the captured file, both equal, and different per edition (listed per family
   below). It is **not** the capture time and **not** the year label (ADR-030). An as-of query is
   `WHERE available_at <= :as_of` (RULINGS 597). For a model asking "what did NESO publish by
   date D", an edition is visible from its `available_at` onward and not before.
2. **Event time: none.** The record has `temporal: none`, so **`timestamp_utc` is the capture
   time** (2026-10-08, listed per family below) and `event_time` equals it on every row. It
   carries no projection information; do not use it as a time axis. No row has an issue time.
   The year label is a scenario period, not an observation or issue time, and no timezone issue
   arises because neither clock is a civil local time.

*Units (vendor dictionary only, as cited in FACTS).* Every measure column in every
projection family has dictionary unit **MW**; for demand the unit is **MW, not MVA**. The
dictionaries attach the unit to the measure column (there is no per-row unit column), and the
schema tables below record it as the "Vendor unit". Year and identifier columns have no unit. The GSP lookup's `Latitude`/`Longitude` unit or CRS is `TODO` (see that
family). Units are never inferred from a column name.

*Measures are scenario values, not observations.* The measure names are conventions for
characteristic system conditions, and their meaning is set per family. In the demand family the
three columns `DemandPk`, `DemandAM` and `DemandPM` are the national winter peak, summer morning
minimum and summer afternoon minimum windows (FACTS g1/g4). For distributed generation greater
than 1 MW, `wintpk`, `summam` and `summpm` are output at the winter peak and summer minima
(FACTS g4). For storage greater than 1 MW they are demand/filling at the specified system
conditions, with negative values indicating filling rates (FACTS g4); FACTS gives the
greater-than-1 MW pre-2023 family the same measure interpretation, and describes the
less-than-1 MW pre-2023 family's measures as charging demand with negative filling rates
(FACTS g1/g4). For the held families
`fes_regional_dg_lt_1mw` and `fes_regional_storage_lt_1mw` the meaning of these measures is
`TODO: verify` (see each family). `capacity` is the family's capacity measure (its population
and meaning vary by family, see each). These are not timestamped observations.

*Place codes.* The vendor describes GSP identifiers as Elexon identifiers where possible,
with direct-connect sites and exceptional identifiers also present; `etys_location` values are short
connection-location codes. Both are stored as published with no normalisation and are **not**
EIC codes (@../../../20-domain/concepts/eic-codes.md) and not universal foreign keys into the GSP
lookup. Preserve unmatched codes; an inner join would drop valid vendor rows.

*Sentinels and missing values (FACTS g5).* NESO declares no null token. None of the listed
literal tokens (a lone `-`, `N/A`, `NA`, `n/a`) occurs in the projection families, and every
nonblank measure casts strictly to float64 and every `year` to int64, with zero failures in every
resource (FACTS g6). A **blank** measure cell is stored as null, never as zero; counts of
blanks are given per family. A numeric zero is a zero: no vendor source defines zero as
missing, so it is never converted to null. The single sentinel in the package is the literal
`#N/A` in the GSP lookup's coordinates (see that family), which is why those two columns stay raw
strings. The record has no null-token map.

*Silver layout (all nine).* Parquet files under
`C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`, one file per capture,
written by runs between `2026-10-08T10-56-39` and `2026-10-08T10-57-58`. The `year=`/`month=`
partition is the **capture** date. Lineage columns appended to the vendor columns:
`edition`, `resource_id`, `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version`. All
timestamps are tz-aware UTC. `dataset_version` reads `1+e1` on every capture of every family,
including those the verification matched to a second header layout; what `e1` encodes is not
established here (`TODO: verify`), so do not use it to tell layouts apart.

*The "pre2023" split.* Two storage tables are split into a `_pre2023` family and a current
family. For the greater-than-1 MW storage table the split is retained because the 2021 file cannot be
read by the CSV reader (a preamble before the header) and its key is not unique, so it is kept
as a resource-level hold, and the 2022 file sits with the pre2023 family. For the
less-than-1 MW storage table the conflicting 2023/2024 dictionaries (descriptions that mix
storage and generation) prevent claiming unchanged semantics across the split, so the older
interpretation is not applied across it (FACTS g4). Do not treat either split as a different physical quantity.

### `fes_regional_demand_active_power`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| scenario | `scenario` | string | — | no | — | — |
| GSP | `gsp` | string | — | no | — | — |
| DemandPk | `demand_pk` | float64 | — | yes | — | MW |
| DemandAM | `demand_am` | float64 | — | yes | — | MW |
| DemandPM | `demand_pm` | float64 | — | yes | — | MW |
| type | `type` | string | — | no | — | — |
| year | `year_label` | int64 | — | no | — | — |

- Entity key: `resource_id`, `edition`, `scenario`, `gsp`, `type`, `year_label`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2021_regional_breakdown_active_power.csv` → 2021; `fes2022_regional_breakdown_active_power.csv` → 2022; `fes2023_regional_breakdown_active_power.csv` → 2023; `fes2024_regional_breakdown_active_power.csv` → 2024
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible. Silver: 1,280,724 rows, 17 columns.** Year label: the financial year beginning in
April (`25` denotes 2025/26; FACTS g1). Measures all **MW, not MVA** (FACTS g4): `DemandPk` is
expected local demand coincident with the national winter peak, `DemandAM` at the national
summer morning minimum, `DemandPM` at the summer afternoon minimum; the dictionary supplies
the characteristic windows. They are scenario values, not observations.

| Edition | Rows | `published_at` = `available_at` | `timestamp_utc` (capture) |
|---|---:|---|---|
| 2021 | 352,284 | 2021-07-06T11:06:43.990644 | 2026-10-08T10:56:39.787331 |
| 2022 | 340,920 | 2022-07-15T13:37:46.607400 | 2026-10-08T10:56:42.741607 |
| 2023 | 329,556 | 2023-08-29T08:50:58.979654 | 2026-10-08T10:56:45.344928 |
| 2024 | 257,964 | 2024-07-15T06:43:07.255666 | 2026-10-08T10:56:48.413285 |

Both clocks as stated above: `timestamp_utc` carries no information about the year label, and
the vintage differs per edition. Measured on silver (2026-10-10): label values run from 20 to 50
(edition 2021), 21 to 50 (2022), 22 to 50 (2023) and 23 to 50 (2024). `scenario` has 4 distinct
codes in editions 2021 to 2023 and 3 in 2024; the codes seen across the family are `CT`, `EE`,
`FS`, `HE`, `HT`, `LW`, `SP`, `ST` (`TODO: verify` the vendor's meaning of each, which neither the
registry nor FACTS records). `type` has 8 distinct codes (`C`, `D`, `E`, `H`, `I`, `R`, `T`,
`Z`; `TODO: verify` their meaning). `gsp` has 639 distinct codes in each of editions 2021 to
2023 and 851 in 2024; against the same-edition GSP lookup, 367 match and 272 do not
(2021 to 2023) and 370 match and 481 do not (2024) (FACTS). Unmatched examples include extra and
direct-connect identifiers (for example `B_EXTRA_1`); keep them.

*Blanks and zeros.* Only `DemandPk` has blank cells: 14,136 (2021), 13,680 (2022) and 13,224
(2023) cells, none in 2024; `DemandAM` and `DemandPM` have none. Blanks are null, not zero (the
silver null counts agree). Zero counts and the longest consecutive run in physical table
order (FACTS, "Regional zero counts and runs"):

| Edition | `DemandPk` | `DemandAM` | `DemandPM` |
|---|---|---|---|
| 2021 | 71,128 / 439 | 125,722 / 3,400 | 123,881 / 3,400 |
| 2022 | 64,827 / 450 | 119,463 / 2,829 | 117,554 / 2,829 |
| 2023 | 62,502 / 435 | 115,298 / 2,734 | 112,219 / 2,734 |
| 2024 | 72,608 / 3,090 | 91,215 / 1,792 | 71,060 / 1,792 |

Zeros are heavy and must be preserved: they are vendor values, not missing data.

### `fes_regional_dg_gt_1mw`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| scenario | `scenario` | string | — | no | — | — |
| tech | `tech` | string | — | no | — | — |
| year | `year_label` | int64 | — | no | — | — |
| etys_location | `etys_location` | string | — | no | — | — |
| capacity | `capacity` | float64 | — | yes | — | MW |
| wintpk | `wintpk` | float64 | — | yes | — | MW |
| summam | `summam` | float64 | — | yes | — | MW |
| summpm | `summpm` | float64 | — | yes | — | MW |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| scenario | `scenario` | string | — | no | — | — |
| tech | `tech` | string | — | no | — | — |
| year | `year_label` | int64 | — | no | — | — |
| etys_location | `etys_location` | string | — | no | — | — |
| capacity | `capacity` | float64 | — | yes | — | MW |
| wintpk | `wintpk` | float64 | — | yes | — | MW |
| summam | `summam` | float64 | — | yes | — | MW |
| summpm | `summpm` | float64 | — | yes | — | MW |
|  | `unnamed_9` | string | — | yes | — | — |
| _duplicated_0 | `unnamed_10` | string | — | yes | — | — |
| _duplicated_1 | `unnamed_11` | string | — | yes | — | — |
| _duplicated_2 | `note` | string | — | yes | — | — |

- Entity key: `resource_id`, `edition`, `scenario`, `tech`, `etys_location`, `year_label`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2021_regional_breakdown_distributed_generation.csv` → 2021; `fes2022_regional_breakdown_distributed_generation.csv` → 2022; `fes2023_regional_breakdown_distributed_generation.csv` → 2023; `fes2024_regional_breakdown_distributed_generation.csv` → 2024
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Silver: 397,471 rows, 22 columns. HELD (E-SEM): no values shown.** Year label: capacity is
present for the winter starting in the labelled year (FACTS g1). The four measures have
dictionary unit **MW**. The hold question is the capacity population: the greater-than-1 MW
resource's `capacity` description says sub-1 MW distributed generation, contradicting its title
and filename, and it is not repaired from the filename (see Holds).

| Edition | Rows | `published_at` = `available_at` | `timestamp_utc` (capture) |
|---|---:|---|---|
| 2021 | 103,431 | 2021-07-06T10:59:37.680231 | 2026-10-08T10:56:52.270524 |
| 2022 | 111,700 | 2022-07-15T13:35:02.326000 | 2026-10-08T10:56:54.720227 |
| 2023 | 107,234 | 2023-07-07T13:38:06.066671 | 2026-10-08T10:56:57.081146 |
| 2024 | 75,106 | 2024-07-15T06:47:00.809819 | 2026-10-08T10:56:59.828320 |

*Two layouts.* The 2021, 2023 and 2024 bodies have the eight-column layout; the 2022 body has
four trailing columns with empty or duplicated headers, which the record declares by their
parsed names (`""`, `_duplicated_0`, `_duplicated_1`, `_duplicated_2`) and maps to explicit
silver names `unnamed_9`, `unnamed_10`, `unnamed_11` and `note`. In the 2022 body the first
three of those are blank in every row and the fourth is blank in all but one row, which carries
a free-text note; the note text is not reproduced here. The silver union frame holds the four
columns as null for the other editions (null in every row for `unnamed_9` to `unnamed_11`, and
in all but that one row for `note`).

*Blanks.* None of the four measures has a blank cell in any edition (silver null counts).
Place codes: `etys_location` is stored as published; coverage against the same-edition GSP
lookup is complete in every edition (every code matches). The family has no `gsp` column.

### `fes_regional_dg_lt_1mw`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| scenario | `scenario` | string | — | no | — | — |
| tech | `tech` | string | — | no | — | — |
| year | `year_label` | int64 | — | no | — | — |
| etys_location | `etys_location` | string | — | no | — | — |
| capacity | `capacity` | float64 | — | yes | — | MW |
| wintpk | `wintpk` | float64 | — | yes | — | MW |
| summam | `summam` | float64 | — | yes | — | MW |
| summpm | `summpm` | float64 | — | yes | — | MW |

- Entity key: `resource_id`, `edition`, `scenario`, `tech`, `etys_location`, `year_label`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2021_regional_breakdown_sub1mw_generation.csv` → 2021; `fes2022_regional_breakdown_sub1mw_generation.csv` → 2022; `fes2023_regional_breakdown_sub1mw_generation.csv` → 2023; `fes2024_regional_breakdown_sub1mw_generation.csv` → 2024
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Silver: 790,601 rows, 18 columns. HELD (E-SEM): no values shown.** Year label: **unsettled**,
`TODO: verify` whether it denotes a calendar, financial or winter period (FACTS g1: the
vendor's two-digit example explains the numeric label but not the period). The four measures
have dictionary unit **MW**, but the 2024 resource dictionary describes storage of at least
1 MW (including negative filling rates) although the resource is distributed generation below
1 MW, so the population and the meaning and direction of `capacity`, `wintpk`, `summam` and
`summpm` are `TODO: verify` (see Holds).

| Edition | Rows | `published_at` = `available_at` | `timestamp_utc` (capture) |
|---|---:|---|---|
| 2021 | 171,531 | 2021-07-06T10:54:05.003828 | 2026-10-08T10:57:04.504161 |
| 2022 | 235,075 | 2022-07-15T13:35:59.358715 | 2026-10-08T10:57:07.008367 |
| 2023 | 227,671 | 2023-07-07T13:37:51.948191 | 2026-10-08T10:57:09.733265 |
| 2024 | 156,324 | 2024-07-15T06:48:05.243503 | 2026-10-08T10:57:12.177000 |

*Blanks.* In the 2021 body each of the four measures has 511 blank cells, stored as null
(silver null counts agree); the later editions have none. No literal sentinel token occurs.
Place-code coverage against the same-edition GSP lookup has one unmatched code in every edition;
its identity is not repeated here. The vendor's own dictionary text for this family is the
mismatch the hold is about; the 2023 dictionary page does not supply a usable alternative
(FACTS).

### `fes_regional_dsr`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| scenario | `scenario` | string | — | no | — | — |
| GSP | `gsp` | string | — | no | — | — |
| DSR | `dsr` | float64 | — | yes | — | MW |
| year | `year_label` | int64 | — | no | — | — |

- Entity key: `resource_id`, `edition`, `scenario`, `gsp`, `year_label`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2021_regional_breakdown_demand_side_response.csv` → 2021; `fes2022_regional_breakdown_demand_side_response.csv` → 2022; `fes2023_regional_breakdown_demand_side_response.csv` → 2023
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible. Silver: 131,760 rows, 14 columns.** Year label: the financial year beginning in
April (`25` denotes 2025/26; FACTS g1). `DSR` has dictionary unit **MW**: the expected change
in demand at winter peak (FACTS g4); the dictionary does not justify changing the sign or
treating zeros as unavailable values. Editions 2021 to 2023 only; the package has no 2024 DSR
resource.

| Edition | Rows | `published_at` = `available_at` | `timestamp_utc` (capture) |
|---|---:|---|---|
| 2021 | 45,384 | 2021-07-06T11:01:06.905207 | 2026-10-08T10:57:15.972865 |
| 2022 | 43,920 | 2022-07-15T13:34:19.868883 | 2026-10-08T10:57:18.485417 |
| 2023 | 42,456 | 2023-07-07T13:35:51.589125 | 2026-10-08T10:57:21.250581 |

Measured on silver: label values run from 20 to 50 (2021), 21 to 50 (2022) and 22 to 50 (2023).
`scenario` has 4 distinct codes per edition and 5 across the family (`CT`, `FS`, `LW`, `SP`, `ST`;
`TODO: verify` their meaning). `gsp` has 366 distinct codes in each edition, all of them present in
the same-edition GSP lookup. *Blanks:* none; no sentinel tokens; all casts succeed. *Zeros* (zero
count / longest run in physical order): 1,984 / 124 (2021), 2,400 / 120 (2022), 2,320 / 4 (2023);
preserve them, they are not missing values.

### `fes_regional_gsp_info`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| GSP ID | `gsp_id` | string | — | no | — | — |
| GSP Group | `gsp_group` | string | — | yes | — | — |
| Minor FLOP | `minor_flop` | string | — | yes | — | — |
| Name | `name` | string | — | yes | — | — |
| Latitude | `latitude` | string | — | yes | — | — |
| Longitude | `longitude` | string | — | yes | — | — |
| Comments | `comments` | string | — | yes | — | — |

- Entity key: `resource_id`, `edition`, `gsp_id`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2021_regional_breakdown_gsp_info.csv` → 2021; `fes2022_regional_breakdown_gsp_info.csv` → 2022; `fes2023_regional_breakdown_gsp_info.csv` → 2023; `fes2024_regional_breakdown_gsp_info.csv` → 2024
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Silver: 1,113 rows over editions 2021, 2023 and 2024, 17 columns. HELD (E-SEM): no values
shown.** This is reference data (a lookup of GSP identifiers to group, name and approximate
position); it has no year and no measure, so there is no year label and no unit except the
position columns, whose unit or CRS is `TODO` (the dictionary describes approximate positions
but does not establish a declared CRS; do not infer one from plausible values). `GSP ID` is unique in
every capture (370, 370 and 373 distinct identifiers) and is the vendor's identifier.

| Edition | Rows in silver | `published_at` = `available_at` | `timestamp_utc` (capture) |
|---|---:|---|---|
| 2021 | 370 | 2021-07-06T10:53:01.441148 | 2026-10-08T10:57:24.776324 |
| 2022 | none (capture fails to read; 370 body rows) | 2022-07-15T13:31:25.009443 | 2026-10-08 (bronze only) |
| 2023 | 370 | 2023-07-07T13:36:07.968680 | 2026-10-08T10:57:29.582165 |
| 2024 | 373 | 2024-07-15T06:43:26.501169 | 2026-10-08T10:57:32.461859 |

*The 2022 capture fails to read, by design of the record.* The 2022 body contains an invalid
UTF-8 byte (`0x92`, at zero-based offset 2946, inside a name) and decodes plausibly as
Windows-1252; the other captures are valid UTF-8 with a byte-order mark. The record declares
`utf-8` (one encoding per record; applying Windows-1252 globally would corrupt the others), so
the 2022 capture fails alone with a `UnicodeDecodeError`. That failure is an **ADR-040
`failed` adjudication** in `_reconcile_adjudications.json` (RULINGS 607): not an open gap and
not stale. Reconcile counts it among the 11 adjudicated (RULINGS 615). Settling it needs a
vendor-confirmed encoding and either per-resource encoding dispatch or a separate correctly
encoded record (`TODO: verify`; see Holds).

*Coordinates and sentinels (FACTS g5).* `Latitude` and `Longitude` stay raw strings. The 2021 and
2022 bodies carry six literal `#N/A` cells per coordinate; the 2023 body has six blanks per
coordinate (stored as null in silver); the 2024 body has neither. `Comments` is blank in 354
(2021), 354 (2022 body), 354 (2023) and 353 (2024) rows. All other columns have no listed
sentinel token. Because the literal `#N/A` is not a null token in the record, it survives as a
string; do not cast without deciding what it means (`TODO: verify` with NESO).

### `fes_regional_storage_gt_1mw`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| scenario | `scenario` | string | — | no | — | — |
| tech | `tech` | string | — | no | — | — |
| year | `year_label` | int64 | — | no | — | — |
| location | `location` | string | — | no | — | — |
| Capacity | `capacity` | float64 | — | yes | — | MW |
| wintpk | `wintpk` | float64 | — | yes | — | MW |
| summam | `summam` | float64 | — | yes | — | MW |
| summpm | `summpm` | float64 | — | yes | — | MW |

- Entity key: `resource_id`, `edition`, `scenario`, `tech`, `location`, `year_label`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_regional_breakdown_dxstorage_gt1mw.csv` → 2023; `fes2024_regional_breakdown_dxstorage_gt1mw.csv` → 2024
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible. Silver: 24,669 rows, 18 columns.** Year label: the winter starting in the labelled
year (FACTS g1). All four measures have dictionary unit **MW**: `Capacity` is the available
charging rate; the other three describe demand (filling) at the specified system conditions,
with negative values indicating filling rates (FACTS g4). Editions 2023 and 2024 (the 2022 file
is in the `_pre2023` sibling; the 2021 file is held).

| Edition | Rows | `published_at` = `available_at` | `timestamp_utc` (capture) |
|---|---:|---|---|
| 2023 | 14,042 | 2023-07-07T13:36:43.988472 | 2026-10-08T10:57:36.424151 |
| 2024 | 10,627 | 2024-07-15T06:45:04.345465 | 2026-10-08T10:57:39.027979 |

Measured on silver: label values run from 22 to 50 (2023) and 23 to 50 (2024). `scenario` has 5
distinct codes in 2023 and 3 in 2024 (8 across the family: `CF`, `CT`, `EE`, `FS`, `HE`, `HT`,
`LW`, `ST`; `TODO: verify` their meaning); `tech` has 4 distinct values per edition (5 across
the family, as published: `Battery`, `CAES`, `LAES`, `PHES`, `Pumped Storage`; `TODO: verify`
whether `PHES` and `Pumped Storage` denote one technology across editions, which the vendor
does not state). `location` has 164 distinct codes (2023) and 132 (2024), all present in the
same-edition GSP lookup. *Blanks:* none; no sentinel tokens; all casts succeed. *Zeros* (zero
count / longest run in physical order): `Capacity` 0 / 0 (2023) and 122 / 1 (2024); `wintpk`
and `summam` are zero in every row of both editions (14,042 and 10,627 rows); `summpm` 0 / 0
(2023) and 122 / 1 (2024). Preserve all of them.

### `fes_regional_storage_gt_1mw_pre2023`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| scenario | `scenario` | string | — | no | — | — |
| tech | `tech` | string | — | no | — | — |
| year | `year_label` | int64 | — | no | — | — |
| location | `location` | string | — | no | — | — |
| Capacity | `capacity` | float64 | — | yes | — | MW |
| wintpk | `wintpk` | float64 | — | yes | — | MW |
| summam | `summam` | float64 | — | yes | — | MW |
| summpm | `summpm` | float64 | — | yes | — | MW |

- Entity key: `resource_id`, `edition`, `scenario`, `tech`, `location`, `year_label`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2022_regional_breakdown_dxstorage_gt1mw.csv` → 2022
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible (2022 only). Silver: 14,245 rows, 18 columns.** Same measure names, dictionary
units (**MW**) and charging interpretation as the current greater-than-1 MW sibling, and the
same winter-start year label (FACTS g1/g4). The 2022 file: `published_at` = `available_at` =
2022-07-15T13:33:26.428024; `timestamp_utc` = 2026-10-08T10:57:45.166372.

**The 2021 resource is a resource-level HOLD, not DOC and not a cleaned CSV.** It has bronze
(captured 2026-10-08, resource `b954c63f-c108-4e71-9b43-b249d0d92a1b`, sidecar and body under
this family's bronze folder) and **no silver and no edition entry** in this family. Two
reasons, both measured on the complete body (FACTS): (1) the body opens with a generated-file
note and a blank line, so the header is on physical line 3, and the CSV reader and record model
have no header-row or skip-row recipe; (2) after locating the real table (11,778 rows) one
(scenario, tech, year, location) tuple repeats three times with identical values, so the entity
key is not unique (one duplicate tuple, two excess rows). Re-disposition needs a supported
header-row recipe plus an authorised duplicate policy, or a corrected NESO upload with a new
`last_modified` (E-SEM; neither the tuple's identifiers nor its values are repeated here).

Measured on silver (2022): label values run from 21 to 50; `scenario` has 5 distinct codes (`CF`,
`CT`, `FS`, `LW`, `ST`); `tech` has 4 (`Battery`, `CAES`, `LAES`, `Pumped Storage`); `location`
has 151 distinct codes, all present in the same-edition GSP lookup. *Blanks:* `summam` and
`summpm` each have 76 blank cells (null), the other columns none; no sentinel tokens. *Zeros*
(zero count / longest run): `Capacity` 0 / 0, `wintpk` 14,245 / 14,245 (all rows), `summam`
14,169 / 14,169 (every nonblank row), `summpm` 0 / 0.

### `fes_regional_storage_lt_1mw`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| scenario | `scenario` | string | — | no | — | — |
| year | `year_label` | int64 | — | no | — | — |
| etys_location | `etys_location` | string | — | no | — | — |
| capacity | `capacity` | float64 | — | yes | — | MW |
| wintpk | `wintpk` | float64 | — | yes | — | MW |
| summam | `summam` | float64 | — | yes | — | MW |
| summpm | `summpm` | float64 | — | yes | — | MW |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| scenario | `scenario` | string | — | no | — | — |
| tech | `tech` | string | — | yes | — | — |
| year | `year_label` | int64 | — | no | — | — |
| etys_location | `etys_location` | string | — | no | — | — |
| capacity | `capacity` | float64 | — | yes | — | MW |
| wintpk | `wintpk` | float64 | — | yes | — | MW |
| summam | `summam` | float64 | — | yes | — | MW |
| summpm | `summpm` | float64 | — | yes | — | MW |

- Entity key: `resource_id`, `edition`, `scenario`, `tech`, `etys_location`, `year_label`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_regional_breakdown_dxstorage_sub1mw.csv` → 2023; `fes2024_regional_breakdown_dxstorage_sub1mw.csv` → 2024
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Silver: 76,758 rows, 18 columns. HELD (E-SEM): no values shown.** Year label: the winter
starting in the labelled year (FACTS g1). The four measures have dictionary unit **MW**, but the
current resource descriptions are inconsistent: the 2023 descriptions of the three condition
measures refer to storage charging while `capacity` describes distributed generation, and the 2024
descriptions call them generation output despite the storage-demand title, so the population,
capacity meaning and sign are `TODO: verify` (see Holds). The older interpretation of the
`_pre2023` sibling is not applied automatically.

| Edition | Rows | `published_at` = `available_at` | `timestamp_utc` (capture) |
|---|---:|---|---|
| 2023 | 45,510 | 2023-07-07T13:37:11.264211 | 2026-10-08T10:57:49.488080 |
| 2024 | 31,248 | 2024-07-15T06:45:51.492269 | 2026-10-08T10:57:52.168193 |

*Two layouts.* The 2023 body has no `tech` column and the 2024 body adds it; the record keeps
`tech` nullable in the union (it is null in every 2023 row, which is why it is in the key as a
nullable column). *Blanks:* none in the measures; no sentinel tokens; all casts succeed. Place
codes: coverage against the same-edition GSP lookup is complete in both editions.

### `fes_regional_storage_lt_1mw_pre2023`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| scenario | `scenario` | string | — | no | — | — |
| year | `year_label` | int64 | — | no | — | — |
| etys_location | `etys_location` | string | — | no | — | — |
| capacity | `capacity` | float64 | — | yes | — | MW |
| wintpk | `wintpk` | float64 | — | yes | — | MW |
| summam | `summam` | float64 | — | yes | — | MW |
| summpm | `summpm` | float64 | — | yes | — | MW |

- Entity key: `resource_id`, `edition`, `scenario`, `etys_location`, `year_label`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2021_regional_breakdown_dxstorage_sub1mw.csv` → 2021; `fes2022_regional_breakdown_dxstorage_sub1mw.csv` → 2022
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible. Silver: 86,945 rows, 17 columns.** Year label: the winter starting in the labelled
year. The dictionary explicitly describes `capacity` as the capacity of sub-1 MW storage and the
three condition measures as charging demand with negative filling rates, all **MW** (FACTS
g1/g4). The physical measures match the current sibling, but the conflicting current
dictionaries prevent claiming unchanged semantics across the split.

| Edition | Rows | `published_at` = `available_at` | `timestamp_utc` (capture) |
|---|---:|---|---|
| 2021 | 39,955 | 2021-07-06T10:48:22.393456 | 2026-10-08T10:57:55.801307 |
| 2022 | 46,990 | 2022-07-15T13:36:47.954918 | 2026-10-08T10:57:58.726143 |

Measured on silver: label values run from 20 to 50 (2021) and 21 to 50 (2022). `scenario` has 5
distinct codes per edition and 6 across the family (`CF`, `CT`, `FS`, `LW`, `SP`, `ST`; `TODO:
verify` their meaning). `etys_location` has 305 distinct codes (2021) and 370 (2022), all present
in the same-edition GSP lookup. `(scenario, etys_location, year_label)` is unique in both bodies.
*Blanks:* none; no sentinel tokens; all casts succeed. *Zeros* (zero count / longest run):
`capacity` 51 / 1 (2021) and 8,260 / 4 (2022); `wintpk` and `summam` zero in every row of both
editions; `summpm` 69 / 1 (2021) and 8,265 / 4 (2022). Preserve them.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The captured `last_modified` dates fall in July 2021, July 2022, July 2023 (and August 2023 for
the 2023 demand file) and July 2024; the vendor states no publication schedule. There is no scheduled refresh in gridflow (the package was captured
once, on 2026-10-08, by the portal sweep). Whether NESO will add further editions to this
package, re-upload an existing resource, or publish the regional tables elsewhere is unknown
(`TODO: verify`): the catalogue snapshot of 2026-10-06 lists no regional resource for a later
edition. If NESO adds resources the registry needs a new record entry for each; a re-upload to
an existing resource id adds a new capture and `_latest` follows it.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_regional_dg_gt_1mw`: held: TODO: vendor correction confirming the capacity population/threshold. The >1 MW resource's `capacity` description says sub-1 MW distributed generation ("Total aggregate capacity of sub 1 MW distributed generation of this technology type associated with this location"), contradicting its title and filename; it is not repaired from the filename. (unit E-SEM)
- `fes_regional_dg_lt_1mw`: held: TODO g1: calendar/financial/winter period meaning for this family. TODO g4: correct population and meaning/direction of `capacity`, `wintpk`, `summam`, `summpm`. The 2024 resource dictionary describes storage of at least 1 MW, including negative filling rates, although the resource is distributed generation below 1 MW; settle with the corrected resource dictionary or matching-edition workbook notes. (unit E-SEM)
- `fes_regional_gsp_info`: held: TODO: coordinate unit/CRS. The dictionary describes approximate positions but does not establish a declared CRS; obtain the vendor definition. `Latitude` and `Longitude` stay raw strings until the sentinel meaning (the 2021 and 2022 bodies carry six literal `#N/A` cells per coordinate, the 2023 body six blanks) and the coordinate semantics are settled. (unit E-SEM)
- `fes_regional_storage_lt_1mw`: held: TODO: matching-edition vendor definitions resolving population, capacity meaning and sign. The 2023 cardinal descriptions refer to storage charging while `capacity` describes distributed generation, and the 2024 descriptions call the cardinal measures generation output despite the storage-demand title; the pre-2023 storage interpretation is not applied automatically. (unit E-SEM)

The silver outputs of these four families exist on disk, but they are **held**: not eligible
for publication or for model use until unit E-SEM has an answer (RULINGS 607). Each is a
**domain-truth question** (vendor semantics) that gridflow does not guess; the hold applies to
the whole family output, not to a subset of columns:

1. **DG greater than 1 MW** (`fes_regional_dg_gt_1mw`): which population does `capacity`
   describe? Its resource description says sub-1 MW generation, against the title and
   filename. Settles it: a NESO correction of the description, or a statement of the threshold.
2. **DG less than 1 MW** (`fes_regional_dg_lt_1mw`): two open questions. (a) What period does
   the year label denote (calendar, financial or winter)? (b) What are the correct population
   and the meaning and direction of `capacity`, `wintpk`, `summam` and `summpm`? Its 2024
   dictionary describes storage rather than generation. Settles it: the corrected resource
   dictionary or the matching-edition workbook notes.
3. **GSP lookup** (`fes_regional_gsp_info`): what are the unit/CRS of `Latitude` and `Longitude`,
   and what does a literal `#N/A` (or a blank) mean there? Plus the encoding of the 2022
   capture. Settles it: the vendor definition of the coordinates and the encoding.
4. **Storage less than 1 MW** (`fes_regional_storage_lt_1mw`): what is the population of the
   edition's `capacity` and the sign convention of the other three, given that the 2023 and
   2024 descriptions disagree with each other and with the title? Settles it: matching-edition
   vendor definitions.

Not held (eligible): `fes_regional_demand_active_power`, `fes_regional_dsr`,
`fes_regional_storage_gt_1mw`, `fes_regional_storage_gt_1mw_pre2023` and
`fes_regional_storage_lt_1mw_pre2023`. Resource-level HOLD: the 2021 storage greater-than-1 MW
file (above, with its preamble and duplicate key; recorded in the HOLD table, not as a family hold).
Open but not a hold: the full-year conversion of the label, which the current engine cannot do
for an ordinary column (`TODO: verify` whether a canonical four-digit representation is required
by a downstream contract; the verification assigns it to a later docs or record-model unit).

**Activation (2026-10-10, master `4b1ec09`, PR #101).** The frozen records merged triple-green
(CI pass twice, Sol diff review APPROVE on pass 1 with no findings, VERIFICATION passed 11/11;
RULINGS 614) and were activated with cutoff 2026-10-08, no prior silver, nothing overwritten
(RULINGS 615). Row counts equal the plan: demand 1,280,724 · DG greater than 1 MW 397,471 · DG
less than 1 MW 790,601 · DSR 131,760 · GSP lookup 1,113 over editions 2021, 2023 and 2024 (the
2022 capture fails `UnicodeDecodeError`, adjudicated `failed`) · storage greater than 1 MW 24,669
· its pre2023 sibling 14,245 (2022 only) · storage less than 1 MW 76,758 · its pre2023 sibling
86,945. Reconcile `--all --cutoff 2026-10-08` exited 0 (94 families, 0 gaps, 11 adjudicated, 0
stale, peak 1,960.3 MiB) (gridflow `@.planning/v0.22-RESULTS.md`, section SCN-1b). No engine,
reader or record-model change was needed.

References: gridflow `@.planning/phases/v0.22-K-SCN-1/K-SCN-1-FACTS.md` (section SCN-1b,
g1 to g6, the year-label, key, geography and cast decisions),
`@.planning/phases/v0.22-K-SCN-1b/VERIFICATION.md` (warning 1: the year label is not carried by
any registry record), `@.planning/RULINGS.md` (603, 605, 607, 614, 615),
`@src/gridflow/connectors/neso_data_portal/registry/regional-breakdown-of-fes-data-electricity.json`,
`@src/gridflow/connectors/neso_data_portal/registry/_reconcile_adjudications.json`,
`@docs/neso_data_portal/eligibility.md`,
`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`,
`@docs/DECISION_LOG/ADR-033-neso-registry-upload-leg.md`,
`@docs/DECISION_LOG/ADR-040-neso-reconcile-adjudication.md`,
`@docs/DECISION_LOG/ADR-042-neso-scenario-unpivot-and-edition.md`.
