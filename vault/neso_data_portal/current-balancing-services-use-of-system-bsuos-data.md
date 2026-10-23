---
source: "neso_data_portal"
package: "current-balancing-services-use-of-system-bsuos-data"
dataset_keys: ["current_bsuos_cap_adjustments", "current_bsuos_historic_ii", "current_bsuos_historic_rf", "current_bsuos_historic_sf", "current_bsuos_ii", "current_bsuos_rf", "current_bsuos_sf"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Current Balancing Services Use of System (BSUoS) Charges

Half-hourly BSUoS (Balancing Services Use of System) charge data for Great Britain, published by NESO as one file per settlement run. The vendor publishes a file for each run type it calculates a BSUoS charge for: Interim Initial (`II`), Settlement Final (`SF`) and Reconciliation Final (`RF`), updated daily with the actual half-hourly BSUoS price, plus total cost and volume by settlement period (CKAN package notes, snapshot 20261006T195819Z). The package has three layers: three "current" CSVs (one per run, post-change layout), historic CSVs (II, SF and RF, one resource per financial year or multi-year block, spanning three header epochs), and four Excel workbooks that carry the BSUoS price-cap adjustment schemes CMP381 and CMP395.

Use it to see what NESO charged per settlement period and how that charge was revised as a settlement day moved through successive runs. Each run is a recalculation of the same settlement day with updated costs and metered volumes, so the three run types are revisions of one another, not additive amounts: reconciliation is the difference between the latest calculated charge and amounts already settled (NESO charging-methodology report, gridflow @.planning/phases/v0.22-K-BAL-1/K-BAL-1-FACTS.md BAL-1a). II is informational; SF and RF are the billable iterations in that report. Never add a row of one run to the same settlement period of another run.

The vendor attribution line is carried verbatim: Supported by National Energy SO Open Data

- Publisher group: Balancing costs
- Registry group: balancing · archetype: SER
- Batch: v0.22 BAL-1 (merged as PR 106, activated 2026-10-10; RULINGS 653, 655, 656)

## Files by disposition

All 18 resources are `upload` captures, captured 2026-10-08, with silver written in the BAL-1 activation (window 2026-10-08..2026-10-10; no prior silver). Fourteen CSV resources map to six tabular families; the four workbooks map to the files family `current_bsuos_files` and are routed, per sheet, to either the SILVER cap-adjustment family or DOC. There are no HOLD or failed resources in this package.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| CMP381 II BSUoS Data | XLSX | upload | `88dcf101-1358-4d78-934f-527484d8789d` |
| ↳ II Output | — | — | SILVER `current_bsuos_cap_adjustments` |
| ↳ Prior Comms | — | — | DOC |
| CMP381 SF BSUoS Data | XLSX | upload | `ead98e64-b345-450a-9c45-c6eae9cc1bbe` |
| ↳ SF Output | — | — | SILVER `current_bsuos_cap_adjustments` |
| ↳ Prior Comms | — | — | DOC |
| CMP395 II BSUoS Data | XLSX | upload | `6ae55c11-7b79-4ea4-9775-1a0b3ccb5275` |
| ↳ II Output | — | — | SILVER `current_bsuos_cap_adjustments` |
| ↳ Prior Comms | — | — | DOC |
| CMP395 SF BSUoS Data | XLSX | upload | `1feb6b1e-549a-4af2-869a-e90b0a7a9c76` |
| ↳ SF Output | — | — | SILVER `current_bsuos_cap_adjustments` |
| ↳ Prior Comms | — | — | DOC |
| Current II BSUoS Data | CSV | upload | `0eda5e28-1dc6-48da-8663-c00e12f2a1e2` |
| Current RF BSUoS Data | CSV | upload | `26b0f410-27d4-448a-9437-45277818b838` |
| Current SF BSUoS Data | CSV | upload | `f0060fd0-1fc9-4288-a0b3-4af9b592b0cf` |
| Historic II BSUoS Data | CSV | upload | `3372646d-419f-4599-97a9-6bb4e7e32862` |
| Historic II BSUoS Data 2023-2024 | CSV | upload | `d151c80a-f6a8-4b79-9387-1a68cd445af5` |
| Historic II BSUoS Data 2024-2025 | CSV | upload | `ea47c8e4-caa3-49c7-a442-e9644d330f63` |
| Historic II BSUoS Data 2025-2026 | CSV | upload | `45e87b67-ed5d-49ea-a149-2b37f467e542` |
| Historic RF BSUoS Data | CSV | upload | `2e8b2ea6-cdb5-4936-8636-4ab5a3f7e350` |
| Historic RF BSUoS Data 2023-2024 | CSV | upload | `47642de9-0738-47df-b230-94a097b61ae7` |
| Historic RF BSUoS Data 2024-2025 | CSV | upload | `544ad552-65e6-47f9-b89c-0b9929dbb869` |
| Historic SF BSUoS Data | CSV | upload | `241b40c3-1f20-4607-b329-0466d215871d` |
| Historic SF BSUoS Data 2023-2024 | CSV | upload | `a68fecf2-99a0-407a-90bb-2a6ebc39d9aa` |
| Historic SF BSUoS Data 2024-2025 | CSV | upload | `320cdc0d-457f-4849-a0fc-bf6bdd4e21e5` |
| Historic SF BSUoS Data 2025-2026 | CSV | upload | `927aac83-c218-476c-9c20-29cf20cee448` |

The DOC children are the `Prior Comms` sheet of each of the four workbooks (empty in all four captures); they are reached only by downloading the parent workbook, listed below. Each workbook's output sheet (`II Output` or `SF Output`) is a data table with its header on row 8, below scheme notes, and is routed to the one SILVER family `current_bsuos_cap_adjustments` (activated earlier by unit X, RESULTS §X).

## Resource downloads and coverage

Download URLs are the CKAN snapshot URLs (snapshot 20261006T195819Z). "Vintage" is the CKAN `last_modified` recorded by the capture sidecar, the clock described under Two clocks. Silver rows and date ranges are read back from the activated silver.

### Workbooks (CMP381 and CMP395 cap schemes)

| Resource | Filename | Download | CKAN last_modified | Silver rows (output sheet) |
|---|---|---|---|---:|
| CMP381 II BSUoS Data | `cmp381-current_ii_bsuos_110422.xlsx` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/88dcf101-1358-4d78-934f-527484d8789d/download/cmp381-current_ii_bsuos_110422.xlsx) | 2022-04-11T16:08:00.098987 | 3,550 |
| CMP381 SF BSUoS Data | `cmp381-current_sf_bsuos_270422.xlsx` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/ead98e64-b345-450a-9c45-c6eae9cc1bbe/download/cmp381-current_sf_bsuos_270422.xlsx) | 2022-05-13T12:13:47.387269 | 3,550 |
| CMP395 II BSUoS Data | `cmp395-current_ii_bsuos_130423.xlsx` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/6ae55c11-7b79-4ea4-9775-1a0b3ccb5275/download/cmp395-current_ii_bsuos_130423.xlsx) | 2023-04-13T14:22:54.127412 | 8,496 |
| CMP395 SF BSUoS Data | `cmp395-current_sf_bsuos_030523.xlsx` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/1feb6b1e-549a-4af2-869a-e90b0a7a9c76/download/cmp395-current_sf_bsuos_030523.xlsx) | 2023-05-03T10:24:33.847516 | 8,496 |

Silver total for `current_bsuos_cap_adjustments`: 24,092 rows, settlement days 2022-01-17 to 2023-03-31 (CMP381: 3,550 rows per run; CMP395: 8,496 rows per run). The scheme notes on the workbooks state a price cap of £20/MWh effective 17/01/2022 to 31/03/2022 inclusive (CMP381) and £40/MWh effective 06/10/2022 to 31/03/2023 inclusive (CMP395) (gridflow @.planning/phases/v0.22-X-R-noncsv/X-R-FACTS.md).

### Current runs (`current_bsuos_ii`, `current_bsuos_sf`, `current_bsuos_rf`)

| Resource | Filename | Download | Vintage (CKAN last_modified) | Silver rows | Settlement dates covered |
|---|---|---|---|---:|---|
| Current II BSUoS Data | `current_ii_bsuos_data.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/0eda5e28-1dc6-48da-8663-c00e12f2a1e2/download/current_ii_bsuos_data.csv) | 2026-10-07T12:23:52.792085 | 8,736 | 2026-04-01 to 2026-09-29 |
| Current SF BSUoS Data | `current_sf_bsuos_data.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/f0060fd0-1fc9-4288-a0b3-4af9b592b0cf/download/current_sf_bsuos_data.csv) | 2026-10-07T12:25:45.157754 | 8,016 | 2026-04-01 to 2026-09-14 |
| Current RF BSUoS Data | `current_rf_bsuos_data.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/26b0f410-27d4-448a-9437-45277818b838/download/current_rf_bsuos_data.csv) | 2026-10-07T12:27:00.397791 | 6,672 | 2025-04-01 to 2025-08-17 |

"Current" means the currently published run file, not the current charging year: the RF file covers 2025-04-01 to 2025-08-17.

### Historic II (`current_bsuos_historic_ii`): 141,695 silver rows

| Resource | Filename | Download | Vintage (CKAN last_modified) | Silver rows | Settlement dates covered |
|---|---|---|---|---:|---|
| Historic II BSUoS Data | `2017-2023-ii.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/3372646d-419f-4599-97a9-6bb4e7e32862/download/2017-2023-ii.csv) | 2023-04-19T11:26:14.741540 | 105,167 | 2017-04-01 to 2023-03-31 |
| Historic II BSUoS Data 2023-2024 | `2023-2024-ii.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/d151c80a-f6a8-4b79-9387-1a68cd445af5/download/2023-2024-ii.csv) | 2024-04-25T12:12:57.875352 | 18,384 | 2023-04-01 to 2024-04-17 |
| Historic II BSUoS Data 2024-2025 | `current_ii_bsuos_data.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/ea47c8e4-caa3-49c7-a442-e9644d330f63/download/current_ii_bsuos_data.csv) | 2025-04-23T12:20:03.734539 | 624 | 2025-04-01 to 2025-04-13 |
| Historic II BSUoS Data 2025-2026 | `2025-2026-ii.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/45e87b67-ed5d-49ea-a149-2b37f467e542/download/2025-2026-ii.csv) | 2026-05-11T11:32:20.516878 | 17,520 | 2025-04-01 to 2026-03-31 |

### Historic SF (`current_bsuos_historic_sf`): 157,776 silver rows

| Resource | Filename | Download | Vintage (CKAN last_modified) | Silver rows | Settlement dates covered |
|---|---|---|---|---:|---|
| Historic SF BSUoS Data | `2017-2023-sf.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/241b40c3-1f20-4607-b329-0466d215871d/download/2017-2023-sf.csv) | 2023-04-28T13:00:16.486391 | 105,168 | 2017-04-01 to 2023-03-31 |
| Historic SF BSUoS Data 2023-2024 | `2023-2024-sf.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/a68fecf2-99a0-407a-90bb-2a6ebc39d9aa/download/2023-2024-sf.csv) | 2024-04-25T12:07:01.189404 | 17,568 | 2023-04-01 to 2024-03-31 |
| Historic SF BSUoS Data 2024-2025 | `2024-2025-sf.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/320cdc0d-457f-4849-a0fc-bf6bdd4e21e5/download/2024-2025-sf.csv) | 2025-05-01T16:43:13.047170 | 17,520 | 2024-04-01 to 2025-03-31 |
| Historic SF BSUoS Data 2025-2026 | `2025-2026-sf.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/927aac83-c218-476c-9c20-29cf20cee448/download/2025-2026-sf.csv) | 2026-05-11T13:00:01.647239 | 17,520 | 2025-04-01 to 2026-03-31 |

### Historic RF (`current_bsuos_historic_rf`): 157,776 silver rows (2 body rows excluded)

| Resource | Filename | Download | Vintage (CKAN last_modified) | Silver rows | Settlement dates covered |
|---|---|---|---|---:|---|
| Historic RF BSUoS Data | `2016-2023-rf.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/2e8b2ea6-cdb5-4936-8636-4ab5a3f7e350/download/2016-2023-rf.csv) | 2024-07-09T11:11:27.261725 | 122,688 (body 122,690) | 2016-04-01 to 2023-03-31 |
| Historic RF BSUoS Data 2023-2024 | `2023-2024-rf.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/47642de9-0738-47df-b230-94a097b61ae7/download/2023-2024-rf.csv) | 2025-09-16T10:35:41.968941 | 17,568 | 2023-04-01 to 2024-03-31 |
| Historic RF BSUoS Data 2024-2025 | `2024-2025-rf.csv` | [download](https://api.neso.energy/dataset/d6a4bf54-c63f-4014-a716-49fd3878ca52/resource/544ad552-65e6-47f9-b89c-0b9929dbb869/download/2024-2025-rf.csv) | 2026-10-01T10:13:35.346062 | 17,520 | 2024-04-01 to 2025-03-31 |

Total silver rows across the package families: 8,736 + 8,016 + 6,672 + 141,695 + 157,776 + 157,776 + 24,092 = 504,763. The reconcile run after activation (`reconcile --all --cutoff 2026-10-10`, 122 families) exited 0 with 0 gaps and 23 adjudicated (RULINGS 656).

## Families

### `current_bsuos_cap_adjustments`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Day | `settlement_day` | date | `%Y-%m-%d %H:%M:%S` | no | — | — |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Price (£/MWh Hour) | `bsuos_price_mwh_hour` | float64 | — | yes | — | — |
| Half-hourly Charge | `half_hourly_charge` | float64 | — | yes | — | — |
| Total Daily BSUoS Charge | `total_daily_bsuos_charge` | float64 | — | yes | — | — |
| Run Type | `run_type` | string | — | no | — | — |
| Total Chargeable Energy Volume (MWh) | `total_chargeable_energy_volume_mwh` | float64 | — | yes | — | — |
| CAPPED BSUoS Price (£/MWh) | `capped_bsuos_price_mwh` | float64 | — | yes | — | — |
| REVISED Half-Hourly Charge | `revised_half_hourly_charge` | float64 | — | yes | — | — |
| Total Net Adjustment to Invoices | `total_net_adjustment_to_invoices` | float64 | — | yes | — | — |

- Entity key: `settlement_day`, `settlement_period`, `run_type`
- Latest: `key_latest`
- Temporal recipe: sp_pair (`settlement_day`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Notes: the output sheets of the four workbooks, header on row 8, columns A:J. `REVISED Half-Hourly Charge` and `Total Net Adjustment to Invoices` carry the literal token `N/A` where no adjustment applies, mapped to null by the frozen record (see Units, sentinels and identifiers). All keys overlap the corresponding historic CSV resource but the workbooks add four fields (chargeable volume, capped price, revised charge, net adjustment) and the values differ, so this family is a separate SILVER child, not a covered duplicate (K-BAL-1-FACTS BAL-1d).

### `current_bsuos_files`

- Kind: files · archetype: SER · refresh: daily · empty allowed: no
- files: catalogue only

The four CMP381 / CMP395 workbooks as downloaded files; their data sheets are carried by `current_bsuos_cap_adjustments` above.

### `current_bsuos_historic_ii`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Day | `settlement_day` | date | `%Y-%m-%dT%H:%M:%S ` | no | — | — |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Price (£/MWh Hour) | `bsuos_price_mwh_hour` | float64 | — | yes | — | — |
| Half-hourly Charge | `half_hourly_charge` | float64 | — | yes | — | — |
| Total Daily BSUoS Charge | `total_daily_bsuos_charge` | float64 | — | yes | — | — |
| Run Type | `run_type` | string | — | no | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Day | `settlement_day` | date | `%Y-%m-%dT%H:%M:%S ` | no | — | — |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Tariff (£/MWh) | `bsuos_tariff_gbp_per_mwh` | float64 | — | yes | — | £ |
| BSUoS Fund Tariff (£/MWh) | `bsuos_fund_tariff_gbp_per_mwh` | float64 | — | yes | — | £ |
| Volume (MWh) | `volume_mwh` | float64 | — | yes | — | — |
| BSUoS Recovery (£) | `bsuos_recovery_gbp` | float64 | — | yes | — | — |
| BSUoS Fund Recovery (£) | `bsuos_fund_recovery_gbp` | float64 | — | yes | — | — |
| BSUoS Total Recovery (£) | `bsuos_total_recovery_gbp` | float64 | — | yes | — | — |
| Run Type | `run_type` | string | — | no | — | — |
| Actual BSUoS Cost(£) | `actual_bsuos_cost_gbp` | float64 | — | yes | — | — |

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Day | `settlement_day` | date | `%Y-%m-%dT%H:%M:%S ` | no | — | — |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Tariff (£/MWh) | `bsuos_tariff_gbp_per_mwh` | float64 | — | yes | — | £ |
| BSUoS Fund Tariff (£/MWh) | `bsuos_fund_tariff_gbp_per_mwh` | float64 | — | yes | — | £ |
| Volume (MWh) | `volume_mwh` | float64 | — | yes | — | — |
| BSUoS Recovery (£) | `bsuos_recovery_gbp` | float64 | — | yes | — | — |
| BSUoS Fund Recovery (£) | `bsuos_fund_recovery_gbp` | float64 | — | yes | — | — |
| BSUoS Total Recovery (£) | `bsuos_total_recovery_gbp` | float64 | — | yes | — | — |
| Run Type | `run_type` | string | — | no | — | — |
| Actual BSUoS Cost (£) | `actual_bsuos_cost_gbp` | float64 | — | yes | — | £ |

- Entity key: `resource_id`, `settlement_day`, `settlement_period`, `run_type`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`settlement_day`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Epoch 1 is the 2017-2023 resource, epoch 2 the 2023-2024 resource (`Actual BSUoS Cost(£)`, no space) and epoch 3 the 2024-2025 and 2025-2026 resources (`Actual BSUoS Cost (£)`, with space). The two actual-cost spellings map to one silver column. The `Vendor unit` cells above come from the generated vendor metadata and are incomplete or inconsistent; the units this page uses are in the Units section.

### `current_bsuos_historic_rf`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Day | `settlement_day` | date | `%Y-%m-%dT%H:%M:%S ` | no | — | ISO 8601 |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Price (£/MWh Hour) | `bsuos_price_mwh_hour` | float64 | — | yes | — | — |
| Half-hourly Charge | `half_hourly_charge` | float64 | — | yes | — | — |
| Total Daily BSUoS Charge | `total_daily_bsuos_charge` | float64 | — | yes | — | — |
| Run Type | `run_type` | string | — | no | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Day | `settlement_day` | date | `%Y-%m-%dT%H:%M:%S ` | no | — | ISO 8601 |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Tariff (£/MWh) | `bsuos_tariff_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
| BSUoS Fund Tariff (£/MWh) | `bsuos_fund_tariff_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
| Volume (MWh) | `volume_mwh` | float64 | — | yes | — | MWh |
| BSUoS Recovery (£) | `bsuos_recovery_gbp` | float64 | — | yes | — | £ |
| BSUoS Fund Recovery (£) | `bsuos_fund_recovery_gbp` | float64 | — | yes | — | £ |
| BSUoS Total Recovery () | `bsuos_total_recovery_gbp` | float64 | — | yes | — | £ |
| Run Type | `run_type` | string | — | no | — | — |
| Actual BSUoS Cost (£) | `actual_bsuos_cost_gbp` | float64 | — | yes | — | £ |

- Entity key: `resource_id`, `settlement_day`, `settlement_period`, `run_type`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`settlement_day`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Epoch 1 is the multi-year resource `2016-2023-rf.csv`; epoch 2 is the 2023-2024 and 2024-2025 resources. The vendor header `BSUoS Total Recovery ()` has lost its currency symbol; it is accepted exactly as published.

### `current_bsuos_historic_sf`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Day | `settlement_day` | date | `%Y-%m-%dT%H:%M:%S ` | no | — | — |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Price (£/MWh Hour) | `bsuos_price_mwh_hour` | float64 | — | yes | — | — |
| Half-hourly Charge | `half_hourly_charge` | float64 | — | yes | — | — |
| Total Daily BSUoS Charge | `total_daily_bsuos_charge` | float64 | — | yes | — | — |
| Run Type | `run_type` | string | — | no | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Day | `settlement_day` | date | `%Y-%m-%dT%H:%M:%S ` | no | — | — |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Tariff (£/MWh) | `bsuos_tariff_gbp_per_mwh` | float64 | — | yes | — | £ |
| BSUoS Fund Tariff (£/MWh) | `bsuos_fund_tariff_gbp_per_mwh` | float64 | — | yes | — | £ |
| Volume (MWh) | `volume_mwh` | float64 | — | yes | — | — |
| BSUoS Recovery (£) | `bsuos_recovery_gbp` | float64 | — | yes | — | — |
| BSUoS Fund Recovery (£) | `bsuos_fund_recovery_gbp` | float64 | — | yes | — | — |
| BSUoS Total Recovery () | `bsuos_total_recovery_gbp` | float64 | — | yes | — | — |
| Run Type | `run_type` | string | — | no | — | — |
| Actual BSUoS Cost (£) | `actual_bsuos_cost_gbp` | float64 | — | yes | — | £ |

- Entity key: `resource_id`, `settlement_day`, `settlement_period`, `run_type`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`settlement_day`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Epoch 1 is the 2017-2023 resource; epoch 2 is the 2023-2024, 2024-2025 and 2025-2026 resources.

### `current_bsuos_ii`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Date | `settlement_date` | date | `%Y-%m-%dT%H:%M:%S ` | no | — | ISO 8601 |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Tariff_GBP per MWh | `bsuos_tariff_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
| Volume_MWh | `volume_mwh` | float64 | — | yes | — | MWh |
| BSUoS Total Recovery_GBP | `bsuos_total_recovery_gbp` | float64 | — | yes | — | £ |
| Run Type | `run_type` | string | — | no | — | — |
| Actual BSUoS Cost_GBP | `actual_bsuos_cost_gbp` | float64 | — | yes | — | £ |

- Entity key: `settlement_date`, `settlement_period`, `run_type`
- Latest: `whole_capture`
- Temporal recipe: sp_pair (`settlement_date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

### `current_bsuos_rf`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Date | `settlement_date` | date | `%Y-%m-%dT%H:%M:%S ` | no | — | ISO 8601 |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Tariff_GBP per MWh | `bsuos_tariff_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
| Volume_MWh | `volume_mwh` | float64 | — | yes | — | MWh |
| BSUoS Total Recovery_GBP | `bsuos_total_recovery_gbp` | float64 | — | yes | — | £ |
| Run Type | `run_type` | string | — | no | — | — |
| Actual BSUoS Cost_GBP | `actual_bsuos_cost_gbp` | float64 | — | yes | — | £ |

- Entity key: `settlement_date`, `settlement_period`, `run_type`
- Latest: `whole_capture`
- Temporal recipe: sp_pair (`settlement_date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

### `current_bsuos_sf`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Date | `settlement_date` | date | `%Y-%m-%dT%H:%M:%S ` | no | — | ISO 8601 |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BSUoS Tariff_GBP per MWh | `bsuos_tariff_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
| Volume_MWh | `volume_mwh` | float64 | — | yes | — | MWh |
| BSUoS Total Recovery_GBP | `bsuos_total_recovery_gbp` | float64 | — | yes | — | £ |
| Run Type | `run_type` | string | — | no | — | — |
| Actual BSUoS Cost_GBP | `actual_bsuos_cost_gbp` | float64 | — | yes | — | £ |

- Entity key: `settlement_date`, `settlement_period`, `run_type`
- Latest: `whole_capture`
- Temporal recipe: sp_pair (`settlement_date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

## Two clocks

Every family in this package has the same two clocks.

- **Vintage clock - `ckan_last_modified`.** `published_at` and `available_at` are both the CKAN `last_modified` of the captured resource file (see the Vintage column in the coverage tables). No scoped CSV carries an issue-instant column, and settlement runs are revisions of the same settlement day, so the registry sets the issue recipe to `none` and availability is the upload date, never the settlement date. A historic resource uploaded in 2023 therefore carries an `available_at` in 2023 for rows whose settlement day is 2017. The workbooks' filename dates are not independently proved issue instants. Point-in-time queries must filter on `available_at`. Every capture's sidecar says `url_type: upload`, so the vintage is `ckan_last_modified`, not the capture-time fallback.
- **Event clock - `sp_pair(settlement date, settlement period)`.** The silver `timestamp_utc` / `event_time` is the UTC start of the half-hour settlement period, computed by the settlement engine from the GB settlement date and the period index (for example settlement day 2026-04-01, period 1 lands at 2026-03-31T23:00:00Z because British Summer Time is UTC+1). The vendor's date column is a settlement-date label serialised with midnight text (`2026-04-01T00:00:00 `); the cast treats it as a date and never as an instant in any timezone. Period index range is 1..50 (46 periods on the spring clock-change day, 50 on the autumn one). The event time is an engine convention for the period start, not a vendor-supplied timestamp.

## Units, sentinels and identifiers

- **Units** come from the vendor field dictionaries and column headers as cited in K-BAL-1-FACTS g4, never from a column name alone. `settlement_period` is a dimensionless half-hour index. BSUoS price and tariff columns are £/MWh; volume is MWh; half-hourly charge, daily charge, recovery, fund recovery, total recovery and actual cost are £. Qualifications:
  - `BSUoS Price (£/MWh Hour)` (historic epoch 1) is £/MWh, stated explicitly in the Historic II dictionary despite the "Hour" wording. For SF and RF the unit cell is blank; £/MWh is a medium-confidence dimensional inference from the vendor's charge definition (price multiplied by MWh gives £), corroborated by the explicit II dictionary.
  - `BSUoS Fund Tariff (£/MWh)` is £/MWh by its title and the RF dictionary. The generated `Vendor unit` cell of the II and SF metadata shows an isolated `£`, which conflicts with the title; no conversion is applied. TODO: verify with NESO the fund-tariff unit cell in the Historic II and SF dictionaries.
  - `BSUoS Total Recovery ()` (Historic SF and RF epoch 2) has lost its unit in the header. £ is carried from the matching total-recovery field in the RF and current dictionaries (medium confidence, cross-run linkage).
  - `Volume (MWh)` in Historic II and SF is MWh from the vendor title and the matching RF dictionary.
  - The `ISO 8601` shown in the `Vendor unit` column of some tables above is the vendor's date-format note, not a unit.
  - Workbook (`current_bsuos_cap_adjustments`) units follow the already frozen contract: `Total Chargeable Energy Volume (MWh)` is MWh and `CAPPED BSUoS Price (£/MWh)` is £/MWh by header, and the three charge fields share the Historic dictionary units. TODO: verify the unit of `REVISED Half-Hourly Charge` and `Total Net Adjustment to Invoices`; the headers carry none and this page does not infer one.
- **Aggregation basis.** Old-epoch `Total Daily BSUoS Charge` is a daily sum repeated on every period row of its day (£). Do not sum it across periods. For the post-change fields the dictionary describes total recovery and actual cost as whole-day quantities, but both vary within every observed day in all three current files, so they are not repeated daily totals. TODO: verify the accumulation basis of `bsuos_total_recovery_gbp` and `actual_bsuos_cost_gbp` with NESO. Until then keep them as published, do not sum to a daily total and do not treat them as repeated daily totals. Keep the old daily total and the new total recovery as distinct fields; their economic meanings differ.
- **Blank fund tariff.** `BSUoS Fund Tariff` is blank in the historic bodies: 36,528 rows in Historic II, 52,608 in Historic SF and 35,088 in Historic RF. The field is nullable and a blank lands as null, never zero. TODO: verify with NESO whether a blank means missing or not applicable.
- **Zeros are numbers.** `BSUoS Fund Recovery` holds a numeric zero on exactly as many rows as the fund tariff is blank (36,528 / 52,608 / 35,088 respectively). Zero is preserved as a number; no inspected source defines it as missing.
- **No other sentinels.** The complete bodies of all fourteen CSV resources have no `NA`, `N/A`, numeric `-1`, thousands separators, currency symbols or percent signs in value columns, and every numeric cast passed (zero cast failures; K-BAL-1-FACTS g5, VERIFICATION). Dates in every scoped resource pass the declared `%Y-%m-%dT%H:%M:%S ` format, whose trailing space accommodates the padded date text in the Historic RF and SF bodies.
- **Workbook null token.** In `current_bsuos_cap_adjustments` the literal `N/A` is the null token for `REVISED Half-Hourly Charge` and `Total Net Adjustment to Invoices`: 3,386 values per column in CMP381 II, 3,383 in CMP381 SF and 8,487 in each CMP395 workbook (K-BAL-1-FACTS g5). Other columns have no null token.
- **Identifiers.** The run is carried in the body in the `Run Type` column, mapped to `run_type` (string, non-null) and a member of every entity key. Values: `II` Interim Initial, `SF` Settlement Final, `RF` Reconciliation Final. The historic families add the CKAN `resource_id` to the key so a financial-year file is its own partition. There are no BM unit or EIC identifiers in this package.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Daily (Weekdays)

The historic resources are updated far less often than daily: their `last_modified` values range from 2023-04-19 to 2026-10-01 (see the coverage tables), and the single last-modified cell is the vintage. Whether a given historic resource was revised after first publication is not established by this capture. TODO: verify.

## Known issues and gotchas

- **Run is part of identity.** A settlement date and period alone is not a key. The current II and SF files share 8,016 settlement-period keys; the tariff agrees across them but volume, total recovery and actual cost differ on every shared pair. Date-and-period-only storage would silently overwrite one run with another.
- **Newest run is not guaranteed to win.** The engine's `_latest` selection removes `run_type` from the grain and ranks the settlement run, but availability ordering leads and run rank is secondary, so an older RF row does not automatically defeat a newer II row. Selecting "highest maturity run" needs an explicit consumer decision; separate family views do not themselves create a combined cross-run view (K-BAL-1-FACTS BAL-1a).
- **Current files are not the current year.** `current_bsuos_rf` covers 2025-04-01 to 2025-08-17. A current/historic overlap of zero keys per run was measured in the captured bodies; do not assume perpetual disjointness, because a file rollover can change it.
- **Historic II resource names and boundaries are unreliable.** `Historic II BSUoS Data 2023-2024` extends to 2024-04-17. `Historic II BSUoS Data 2024-2025` is named for a year but its body holds only 2025-04-01 to 2025-04-13 (624 rows) and its URL filename is `current_ii_bsuos_data.csv`, the same filename as the current II file. `Historic II BSUoS Data 2025-2026` (2025-04-01 to 2026-03-31) contains all 624 of those keys with identical raw row values.
- **Historic II overlap is adjudicated and both are served.** The 2024-2025 and 2025-2026 resources share 624 keys with zero differing rows. Under the ADR-040 overlap ledger (RULINGS 653) both resources are retained and neither is dropped, silently renamed or treated as superseding the other. Because each resource is its own `whole_capture` partition, a query across the family counts those 624 keys twice unless it filters on `resource_id`. The family holds 141,071 distinct canonical keys among its 141,695 rows. TODO: verify with NESO whether the 2024-2025 upload is mislabelled and whether it will be corrected.
- **Two invalid Historic RF rows are excluded by design.** In `2016-2023-rf.csv` the rows for 2022-03-27 periods 47 and 48 do not exist on that 46-period spring clock-change day. They are excluded as schema-invalid rows (122,690 body rows, 122,688 in silver); this is a row exclusion, not a duplicate-key, encoding or failed-capture adjudication.
- **Missing period in Historic II.** The 2017-2023 resource lacks the pair 2021-01-14 period 48. It is not filled. TODO: verify the reason with NESO.
- **Header-spelling drift.** Actual-cost headers differ across resources (`Actual BSUoS Cost(£)` versus `Actual BSUoS Cost (£)`) and the exact header list selects the epoch; a new spelling from the vendor will stop that file from matching until a record is added.
- **Date columns differ by family.** Historic families use `settlement_day`; current families use `settlement_date`; the workbook family uses `settlement_day` with a different format (`%Y-%m-%d %H:%M:%S`). The trailing space in the CSV format is deliberate.
- **Entity-key uniqueness is measured, not vendor-guaranteed.** Every scoped body is unique on settlement date, period and run, but the vendor dictionaries state no primary-key constraint. TODO: verify (vendor key guarantee).
- **Workbook scope.** The cap-adjustment data covers only the CMP381 and CMP395 scheme windows (2022-01-17 to 2022-03-31 and 2022-10-06 to 2023-03-31 per the scheme notes). It is not a general BSUoS source.
- **Related packages, not this one.** NESO publishes sibling balancing-cost datasets under separate packages and they are not in this page: @bsuos-fixed-tariffs.md (held), @daily-balancing-costs-balancing-services-use-of-system.md and @daily-balancing-volume-balancing-services-use-of-system.md (no silver, because their bodies carry no settlement-run column; RULINGS 538 precedent, 653), @gb-system-inertia-bid-and-offer-costs.md (held), and @constraint-breakdown.md.

## Holds

- none

This package has no held family, resource or output, and no ADR-040 adjudicated failure. The one adjudication is the Historic II overlap (HI3 / HI4, both retained). The held outputs of the same batch (`bsuos_fixed_tariffs`, `inertia_bid_offer_costs`) live in their own packages, linked above.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data
