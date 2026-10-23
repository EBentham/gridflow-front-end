---
source: "neso_data_portal"
package: "system-inertia-cost"
dataset_key: "system_inertia_cost"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# System Inertia Cost

Daily average price that NESO paid per unit of system inertia, published as one CSV per financial year from 2017-18 onwards. The vendor describes the figure as the average daily inertia price, derived from accepted offers tagged for inertia and the associated inertia estimates (gridflow @.planning/phases/v0.22-K-SYS-1/K-SYS-1-FACTS.md §7). The unit is pounds per GVAs (GVA.s) - a rate, never a total daily spend. It is a retrospective, indicative price: there is no forecast column and no issue column.

Use it as a daily indicative price alongside the settlement-period inertia estimates in @system-inertia.md, but do not multiply an inertia estimate by this rate and call the result a cost. The two datasets have different grains (settlement period versus day) and the published cost denominator covers inertia supplied for tagged actions across settlement periods, not the outturn estimate.

Supported by National Energy SO Open Data

- Publisher group: System
- Registry group: system · archetype: SER

## Files by disposition

Nine resources are captured to silver; one (the 2026 resource) is a resource-level HOLD. There are no DOC resources in this package. All ten are `upload` CSVs, captured 2026-10-08 (silver run 2026-10-08).

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| GB System Inertia Costs 2017 | CSV | upload | `28dc603e-3472-45cd-8e7b-998efc674084` |
| GB System Inertia Costs 2018 | CSV | upload | `1146f7af-9f3b-4a8a-a37d-3003c727bfbf` |
| GB System Inertia Costs 2019 | CSV | upload | `620491fa-ae1b-45b3-baa0-6e87c2d574cf` |
| GB System Inertia Costs 2020 | CSV | upload | `130c9f71-cbce-4027-b5b8-13cba14df0dd` |
| GB System Inertia Costs 2021 | CSV | upload | `3518e47e-ffb3-4561-aff1-4a102fcb242d` |
| GB System Inertia Costs 2022 | CSV | upload | `8a3a4233-e9aa-45c2-b0c4-28b8d614165b` |
| GB System Inertia Costs 2023 | CSV | upload | `3cc32e61-bf87-471c-bf00-abb356d3f8c8` |
| GB System Inertia Costs 2024 | CSV | upload | `91947c0c-bbbf-4d55-a29d-dc610d91d075` |
| GB System Inertia Costs 2025 | CSV | upload | `a6a52241-1774-48d8-935f-2bef0d843e18` |

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| GB System Inertia Costs 2026 | CSV | upload | `6295f4ed-b43d-4a80-8ca9-c27c9fa16517` | The captured resource uses `Settlement Date,Cost_per_GVAs` and filename `inertia_costs.csv`, shared with resources whose dates are ISO. Its sole date is `01/04/2026`, which cannot pass their declared ISO cast, and does not independently establish day/month order. ADR-039 maps formats by exact filename, so it cannot distinguish these resources. Re-disposition requires a corrected vendor upload, an explicit distinguishing vendor filename/date contract, or a declared engine mechanism that resolves formats by a sufficient resource discriminator. (SYS-1) |

The hold is a reader/typing limitation (one filename, two incompatible date literals), not an ADR-040 adjudicated failure. The held resource contributes 0 silver rows and its data values are not published here. Nothing else in this family is held or failed.

## Resource downloads and coverage

Download URLs are the CKAN snapshot URLs (snapshot 20261006T195819Z). Resource names say a calendar year, but the files are financial years: every resource starts on 1 April of its label year (vendor resource description: one file per financial year). The "CKAN last_modified" column is the vintage clock described below.

| Resource | Filename | Download | CKAN last_modified | Silver rows | Settlement dates covered |
|---|---|---|---|---:|---|
| 2017 | `inertia_costs17.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/28dc603e-3472-45cd-8e7b-998efc674084/download/inertia_costs17.csv) | 2021-12-07T12:12:09.974451 | 365 | 2017-04-01 to 2018-03-31 |
| 2018 | `inertia_costs18.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/1146f7af-9f3b-4a8a-a37d-3003c727bfbf/download/inertia_costs18.csv) | 2021-12-07T12:14:12.860862 | 365 | 2018-04-01 to 2019-03-31 |
| 2019 | `inertia_costs19.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/620491fa-ae1b-45b3-baa0-6e87c2d574cf/download/inertia_costs19.csv) | 2021-12-07T12:14:59.890158 | 366 | 2019-04-01 to 2020-03-31 |
| 2020 | `inertia_costs20.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/130c9f71-cbce-4027-b5b8-13cba14df0dd/download/inertia_costs20.csv) | 2021-12-07T12:15:37.611975 | 365 | 2020-04-01 to 2021-03-31 |
| 2021 | `inertia_costs.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/3518e47e-ffb3-4561-aff1-4a102fcb242d/download/inertia_costs.csv) | 2022-04-07T08:30:42.821949 | 361 | 2021-04-01 to 2022-03-31 |
| 2022 | `inertia_costs22.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/8a3a4233-e9aa-45c2-b0c4-28b8d614165b/download/inertia_costs22.csv) | 2024-04-02T16:17:02.960104 | 362 | 2022-04-01 to 2023-03-31 |
| 2023 | `inertia_costs.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/3cc32e61-bf87-471c-bf00-abb356d3f8c8/download/inertia_costs.csv) | 2025-01-21T15:54:38.545770 | 366 | 2023-04-01 to 2024-03-31 |
| 2024 | `inertia_costs.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/91947c0c-bbbf-4d55-a29d-dc610d91d075/download/inertia_costs.csv) | 2025-09-04T13:30:48.701007 | 365 | 2024-04-01 to 2025-03-31 |
| 2025 | `inertia_costs.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/a6a52241-1774-48d8-935f-2bef0d843e18/download/inertia_costs.csv) | 2026-04-10T09:06:09.725049 | 366 | 2025-04-01 to 2026-04-01 |
| 2026 (HOLD) | `inertia_costs.csv` | [download](https://api.neso.energy/dataset/59f20804-9c9e-4f70-a809-c4c48a4f4c6e/resource/6295f4ed-b43d-4a80-8ca9-c27c9fa16517/download/inertia_costs.csv) | 2026-04-14T14:54:26.059319 | 0 (held) | one data row in bronze (3,282 bronze CSV rows in total) |

Silver total: 3,281 rows (activation receipt, RESULTS "SYS-1", RULINGS 647). The 2025 resource reaches one day into 2026-27, so the financial-year boundary and the resource label do not line up exactly.

## Families

### `system_inertia_cost`

- Kind: tabular · archetype: SER · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Date | `settlement_date` | date | `inertia_costs17.csv` → `%d/%m/%Y`; `inertia_costs18.csv` → `%d/%m/%Y`; `inertia_costs19.csv` → `%d/%m/%Y`; `inertia_costs20.csv` → `%d/%m/%Y`; `inertia_costs22.csv` → `%Y-%m-%d`; `inertia_costs.csv` → `%Y-%m-%d` | no | — | — |
| Cost | `cost_gbp_per_gvas` | int64 | — | yes | — | not carried in the generated schema; the legacy dictionary and methodology give £ per GVAs (see Units) |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Date | `settlement_date` | date | `inertia_costs17.csv` → `%d/%m/%Y`; `inertia_costs18.csv` → `%d/%m/%Y`; `inertia_costs19.csv` → `%d/%m/%Y`; `inertia_costs20.csv` → `%d/%m/%Y`; `inertia_costs22.csv` → `%Y-%m-%d`; `inertia_costs.csv` → `%Y-%m-%d` | no | — | — |
| Cost_per_GVAs | `cost_gbp_per_gvas` | int64 | — | yes | — | £ per GVAs |

- Entity key: `resource_id`, `settlement_date`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: date_sp1 (`settlement_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

## Two clocks

- **Vintage clock - `ckan_last_modified`.** `published_at` and `available_at` are both the CKAN `last_modified` of the captured resource file (the table above). There is no issue column in the vendor data and no evidence that a daily price was publicly available at its operational day, so availability is the upload date, not the settlement date. The 2017-2020 resources therefore carry an `available_at` of 2021-12-07, years after their event time. Point-in-time queries must filter on `available_at`.
- **Event clock - `date_sp1(settlement_date)`.** Each row is one calendar day. The silver `timestamp_utc` / `event_time` is the UK settlement-period-1 start of that date, i.e. the engine's daily anchor, not a vendor timestamp (for example a summer date lands at 23:00 UTC the previous evening). Treat it as a day label: the price is a daily average and has no sub-day resolution.

## Units, sentinels and identifiers

- **Unit.** Both header epochs are the same vendor quantity and land in one silver column, `cost_gbp_per_gvas` (int64, nullable). Epoch 1 (`Cost`, resources 2017-2020) and epoch 2 (`Cost_per_GVAs`, resources 2021-2026) are documented by NESO as the daily average cost of a unit of inertia in pounds per GVAs; the epoch-2 field dictionary carries the explicit unit "£ per GVAs" and the legacy dictionary's description omits the "s" in one phrase while its unit and the dataset methodology include it (K-SYS-1-FACTS §7 T01, ruling 642). No conversion is applied. The vendor example value shows whole numbers, consistent with int64.
- **Zeros.** Zero is a supplied numeric value and stays numeric; it is never nulled or dropped. Zero counts per resource (settlement days with a zero price, longest consecutive file-order run): 2017: 358 (116); 2018: 288 (29); 2019: 279 (30); 2020: 219 (18); 2021: 237 (28); 2022: 231 (30); 2023: 202 (17); 2024: 170 (28); 2025: 192 (19). TODO: verify what a zero means - no inspected source says whether it is no tagged inertia action, a computed zero rate, or another reporting condition (INERTIA-COST-ZERO).
- **Other sentinels.** No blank cells, `-1`, `N/A`, `NA`, thousands separators, currency symbols or percent signs occur in the value cells of any captured resource; every value passes the int64 cast (FACTS g5). Because the dtype is nullable, a future blank would land as null rather than zero.
- **Identifiers.** The only identifier is the CKAN `resource_id`, stored as-is, which separates financial-year files in the entity key. There are no group labels or BMU/EIC codes in this family.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The vendor publishes one resource per financial year, and the CKAN catalog snapshot (20261006T195819Z) describes every resource as updated daily, appending to one file per financial year. The observed `last_modified` values are listed in the coverage table above (2021-12-07 for 2017-2020, then 2022-04-07, 2024-04-02, 2025-01-21, 2025-09-04, 2026-04-10 and, for the held 2026 resource, 2026-04-14). A `last_modified` later than a financial-year end is consistent with that append description and is not by itself evidence of revision. TODO: verify whether any resource was revised after first publication; no conclusion is drawn here. `latest` is `whole_capture` per `resource_id`: for each resource, the newest whole captured file supersedes older captures of that same resource, while different resources never replace each other.

## Known issues and gotchas

- **Date formats are filename-specific.** Resources 2017-2020 use `%d/%m/%Y`; 2021-2025 use ISO `%Y-%m-%d`. The format map is keyed on exact filename (ADR-039), and five resources (four admitted, plus the held 2026 resource) share `inertia_costs.csv`.
- **The 2026 resource is held** because its single date literal is a slash date (`01/04/2026`) under the same filename as the ISO resources, and its day/month order is not independently established. Re-disposition conditions are in the HOLD table. TODO: verify with NESO whether the 2026 upload is DMY and whether the file will be corrected.
- **Conditional overlap if the held resource were later admitted.** If the 2026 literal is read as day/month, it repeats the final settlement date already present in the 2025 resource. This is a conditional observation, not a settled fact; precedence between the two would then need an ADR-039/040 ruling, and none is invented here.
- **Missing days are preserved, not filled.** The 2021 resource lacks 2021-11-24, 2021-11-25, 2021-11-26 and 2021-12-08 (361 rows); the 2022 resource lacks 2022-05-16, 2022-05-17 and 2022-08-18 (362 rows). The reason is not documented. TODO: verify with NESO.
- **Entity-key uniqueness is measured, not vendor-guaranteed.** The settlement date is unique within every captured resource (duplicate excess 0), but the dictionary states no primary-key guarantee. TODO: verify (vendor key guarantee).
- **Resource label is not a calendar year.** See the coverage table; join on `settlement_date`, never on the label.
- **Settlement-day grain.** The daily row is an anchor at settlement period 1 for the GB (UK) day; no per-period or DST (46/50-period) structure exists in this dataset.

## Holds

- none

The family itself has no hold; the only hold is the resource-level one on the 2026 file listed above (unit SYS-1). Nothing in this family is an ADR-040 adjudicated failure.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data
