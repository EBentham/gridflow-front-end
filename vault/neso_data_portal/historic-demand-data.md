---
source: "neso_data_portal"
package: "historic-demand-data"
dataset_key: "historic_demand"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Historic Demand Data

This package is GB electricity demand outturn per settlement period (half-hour) from 2001 to
the present. NESO publishes it on the Open Data Portal as one CSV per calendar year, 26
resources in all (2001–2026). Each row is one UK settlement date and period. It carries
**National Demand (ND)**, **Transmission System Demand (TSD)** and England and Wales demand.
It also carries NESO's estimates of embedded (distribution-connected) wind and solar
generation and their installed capacities, non-BM STOR, pump-storage pumping and the flow on
each GB interconnector. The column set grows with the header epochs: four more
interconnectors appear from the 2019 file, and the Scottish transfer appears in the
2001–2008 and 2023-onward files. The vendor dictionary says
ND is equivalent to the Initial National Demand Outturn (INDO) on BM Reports, and TSD to the
Initial Transmission System Demand Outturn (ITSDO). gridflow ingests both from Elexon
(@../../elexon/datasets/indo.md, @../../elexon/datasets/itsdo.md). Use this package for a long
half-hourly demand history, or as a demand and embedded-generation baseline for models that
need years before Elexon's holdings start. Settlement periods follow
@../../../20-domain/concepts/settlement-period.md.

The package notes say the dataset "is populated 21 days in arrears". They also say it
receives retrospective corrections to solar capacity and outturn, possibly "several months
after the first publication". They add that retrospective edits to demand "may occur", to
adjust for NESO's balancing services. A vendor note also says NESO "is aware of some data
quality issues with this dataset". The current-year file is the slower, corrected sibling of
@./daily-demand-update.md, which has about ten days' lag and a 7-day forecast tail (see the
relationship note below). gridflow has a silver output for all 26 years, but it is **held**:
the meaning of a literal `NA` token in the 2001–2008 files is undefined (see Holds).

- Publisher group: Demand
- Registry group: demand · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Historic Demand Data 2001 | CSV | upload | `e8608e9a-f56c-457f-b9e7-bfffcfd19731` |
| Historic Demand Data 2002 | CSV | upload | `4daaac31-ae56-461e-8efe-6b33e147225a` |
| Historic Demand Data 2003 | CSV | upload | `30650247-acbf-414d-8ae2-2aa4aac57537` |
| Historic Demand Data 2004 | CSV | upload | `5f5c076c-d3a3-4f33-a137-501cc3d2ca9b` |
| Historic Demand Data 2005 | CSV | upload | `42a41acd-53b6-450d-af1b-4a92a352895c` |
| Historic Demand Data 2006 | CSV | upload | `949bb4a4-8374-4730-89ef-302d82428d2c` |
| Historic Demand Data 2007 | CSV | upload | `c0da767c-447d-48d1-93fd-ca3955d078ae` |
| Historic Demand Data 2008 | CSV | upload | `ec63adc8-e8a1-45cc-a593-5953b1ede7b1` |
| Historic Demand Data 2009 | CSV | upload | `ed8a37cb-65ac-4581-8dbc-a3130780da3a` |
| Historic Demand Data 2010 | CSV | upload | `b3eae4a5-8c3c-4df1-b9de-7db243ac3a09` |
| Historic Demand Data 2011 | CSV | upload | `01522076-2691-4140-bfb8-c62284752efd` |
| Historic Demand Data 2012 | CSV | upload | `4bf713a2-ea0c-44d3-a09a-63fc6a634b00` |
| Historic Demand Data 2013 | CSV | upload | `2ff7aaff-8b42-4c1b-b234-9446573a1e27` |
| Historic Demand Data 2014 | CSV | upload | `b9005225-49d3-40d1-921c-03ee2d83a2ff` |
| Historic Demand Data 2015 | CSV | upload | `cc505e45-65ae-4819-9b90-1fbb06880293` |
| Historic Demand Data 2016 | CSV | upload | `3bb75a28-ab44-4a0b-9b1c-9be9715d3c44` |
| Historic Demand Data 2017 | CSV | upload | `2f0f75b8-39c5-46ff-a914-ae38088ed022` |
| Historic Demand Data 2018 | CSV | upload | `fcb12133-0db0-4f27-a4a5-1669fd9f6d33` |
| Historic Demand Data 2019 | CSV | upload | `dd9de980-d724-415a-b344-d8ae11321432` |
| Historic Demand Data 2020 | CSV | upload | `33ba6857-2a55-479f-9308-e5c4c53d4381` |
| Historic Demand Data 2021 | CSV | upload | `18c69c42-f20d-46f0-84e9-e279045befc6` |
| Historic Demand Data 2022 | CSV | upload | `bb44a1b5-75b1-4db2-8491-257f23385006` |
| Historic Demand Data 2023 | CSV | upload | `bf5ab335-9b40-4ea4-b93a-ab4af7bce003` |
| Historic Demand Data 2024 | CSV | upload | `f6d02c0f-957b-48cb-82ee-09003f2ba759` |
| Historic Demand Data 2025 | CSV | upload | `b2bde559-3455-4021-b179-dfe60c0337b0` |
| Historic Demand Data 2026 | CSV | upload | `8a4a771c-3929-4e56-93ad-cdf13219dea5` |

Download links and the one capture of each resource (2026-10-08, all CKAN upload resources;
sizes and CKAN `last_modified` from each capture's sidecar under
`C:/gridflow-data/bronze/neso_data_portal/historic_demand/2026/10/08/`). "Epoch" uses this
page's numbering (the schema tables below). Data rows equal the silver rows per resource.

| Year | File | Epoch | `SETTLEMENT_DATE` format | Bytes | Data rows | CKAN `last_modified` |
|---|---|---:|---|---:|---:|---|
| 2001 | [demanddata_2001.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/e8608e9a-f56c-457f-b9e7-bfffcfd19731/download/demanddata_2001.csv) | 3 | `%Y-%m-%d` | 1,461,282 | 17,520 | 2025-06-20T08:35:31.018121 |
| 2002 | [demanddata_2002.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/4daaac31-ae56-461e-8efe-6b33e147225a/download/demanddata_2002.csv) | 3 | `%Y-%m-%d` | 1,459,634 | 17,520 | 2025-06-20T08:35:55.064874 |
| 2003 | [demanddata_2003.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/30650247-acbf-414d-8ae2-2aa4aac57537/download/demanddata_2003.csv) | 3 | `%Y-%m-%d` | 1,462,386 | 17,520 | 2025-06-20T08:36:18.971427 |
| 2004 | [demanddata_2004.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/5f5c076c-d3a3-4f33-a137-501cc3d2ca9b/download/demanddata_2004.csv) | 3 | `%Y-%m-%d` | 1,465,731 | 17,568 | 2025-06-20T08:36:41.853468 |
| 2005 | [demanddata_2005.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/42a41acd-53b6-450d-af1b-4a92a352895c/download/demanddata_2005.csv) | 3 | `%Y-%m-%d` | 1,519,367 | 17,520 | 2025-06-20T08:37:05.580758 |
| 2006 | [demanddata_2006.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/949bb4a4-8374-4730-89ef-302d82428d2c/download/demanddata_2006.csv) | 3 | `%Y-%m-%d` | 1,543,093 | 17,520 | 2025-06-20T08:37:30.333853 |
| 2007 | [demanddata_2007.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/c0da767c-447d-48d1-93fd-ca3955d078ae/download/demanddata_2007.csv) | 3 | `%Y-%m-%d` | 1,530,735 | 17,520 | 2025-06-20T08:37:56.090537 |
| 2008 | [demanddata_2008.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/ec63adc8-e8a1-45cc-a593-5953b1ede7b1/download/demanddata_2008.csv) | 3 | `%Y-%m-%d` | 1,594,396 | 17,568 | 2025-06-20T08:38:21.660130 |
| 2009 | [demanddata_2009.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/ed8a37cb-65ac-4581-8dbc-a3130780da3a/download/demanddata_2009.csv) | 1 | `%d-%b-%Y` | 1,221,064 | 17,520 | 2023-07-24T12:16:55.273828 |
| 2010 | [demanddata_2010.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/b3eae4a5-8c3c-4df1-b9de-7db243ac3a09/download/demanddata_2010.csv) | 1 | `%d-%b-%Y` | 1,237,038 | 17,520 | 2023-07-24T12:17:59.367327 |
| 2011 | [demanddata_2011.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/01522076-2691-4140-bfb8-c62284752efd/download/demanddata_2011.csv) | 1 | `%d-%b-%Y` | 1,269,447 | 17,520 | 2023-07-24T12:19:33.983929 |
| 2012 | [demanddata_2012.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/4bf713a2-ea0c-44d3-a09a-63fc6a634b00/download/demanddata_2012.csv) | 1 | `%d-%b-%Y` | 1,323,744 | 17,568 | 2023-07-24T12:21:01.069378 |
| 2013 | [demanddata_2013.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/2ff7aaff-8b42-4c1b-b234-9446573a1e27/download/demanddata_2013.csv) | 1 | `%d-%b-%Y` | 1,372,112 | 17,520 | 2023-07-24T12:30:21.215757 |
| 2014 | [demanddata_2014.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/b9005225-49d3-40d1-921c-03ee2d83a2ff/download/demanddata_2014.csv) | 1 | `%d-%b-%Y` | 1,379,848 | 17,520 | 2023-07-24T12:32:14.516476 |
| 2015 | [demanddata_2015.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/cc505e45-65ae-4819-9b90-1fbb06880293/download/demanddata_2015.csv) | 1 | `%d-%b-%Y` | 1,380,366 | 17,520 | 2023-07-24T12:35:23.084117 |
| 2016 | [demanddata_2016.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/3bb75a28-ab44-4a0b-9b1c-9be9715d3c44/download/demanddata_2016.csv) | 1 | `%d-%b-%Y` | 1,367,182 | 17,568 | 2023-07-24T12:41:09.588932 |
| 2017 | [demanddata_2017.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/2f0f75b8-39c5-46ff-a914-ae38088ed022/download/demanddata_2017.csv) | 1 | `%d-%b-%Y` | 1,385,795 | 17,520 | 2023-07-24T12:43:04.594718 |
| 2018 | [demanddata_2018.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/fcb12133-0db0-4f27-a4a5-1669fd9f6d33/download/demanddata_2018.csv) | 1 | `%d-%b-%Y` | 1,389,142 | 17,520 | 2023-07-24T12:45:05.955597 |
| 2019 | [demanddata_2019.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/dd9de980-d724-415a-b344-d8ae11321432/download/demanddata_2019.csv) | 2 | `%d-%b-%Y` | 1,554,786 | 17,520 | 2025-04-08T19:45:40.926204 |
| 2020 | [demanddata_2020.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/33ba6857-2a55-479f-9308-e5c4c53d4381/download/demanddata_2020.csv) | 2 | `%d-%b-%Y` | 1,560,521 | 17,568 | 2025-04-08T19:49:15.816242 |
| 2021 | [demanddata_2021.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/18c69c42-f20d-46f0-84e9-e279045befc6/download/demanddata_2021.csv) | 2 | `%d-%b-%Y` | 1,589,451 | 17,520 | 2025-04-08T19:51:19.727410 |
| 2022 | [demanddata_2022.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/bb44a1b5-75b1-4db2-8491-257f23385006/download/demanddata_2022.csv) | 2 | `%d-%b-%Y` | 1,682,356 | 17,520 | 2025-04-08T19:52:21.391966 |
| 2023 | [demanddata_2023.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/bf5ab335-9b40-4ea4-b93a-ab4af7bce003/download/demanddata_2023.csv) | 3 | `%d-%b-%y` | 1,732,679 | 17,520 | 2025-04-08T19:54:08.935442 |
| 2024 | [demanddata_2024.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/f6d02c0f-957b-48cb-82ee-09003f2ba759/download/demanddata_2024.csv) | 3 | `%d-%b-%Y` | 1,809,707 | 17,568 | 2025-04-08T19:55:41.954513 |
| 2025 | [demanddata_2025.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/b2bde559-3455-4021-b179-dfe60c0337b0/download/demanddata_2025.csv) | 3 | `%Y-%m-%d` | 1,869,771 | 17,520 | 2026-06-09T13:25:07.456371 |
| 2026 | [demanddataupdate_2026.csv](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/8a4a771c-3929-4e56-93ad-cdf13219dea5/download/demanddataupdate_2026.csv) | 4 | `%Y-%m-%d` | 1,331,452 | 12,478 | 2026-10-08T08:20:27.652049 |

Total: 450,766 data rows. Each 2001–2025 body covers 1 January to 31 December of its filename
year; the 2026 body runs from 2026-01-01 to 2026-09-17. Note the current-year filename is
`demanddataupdate_2026.csv`, not `demanddata_2026.csv`. All 26 CSV resources are CKAN
datastore-active in the 2026-10-06 catalogue snapshot; gridflow captures the uploaded files,
not the datastore.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Frequently Asked Questions (FAQ) | DOC | upload | `243ca76a-eefe-419d-a4b5-397073deb100` |

- Download: [faq-neso.docx](https://api.neso.energy/dataset/8f2fe0af-871c-488d-8bad-960426f24601/resource/243ca76a-eefe-419d-a4b5-397073deb100/download/faq-neso.docx)
  (CKAN `last_modified` 2024-10-21T12:04:20.336881).
- Captured: `raw_20261008T110848Z_243ca76a-eefe-419d-a4b5-397073deb100_39ecfdf2.docx`,
  169,027 bytes. Catalogue only: no silver output. It is primary evidence for this page. It
  answers that the units are MW, that "All values are an average over the half hour", and
  that "All times are UK time and for the half hour beginning" (gridflow
  `@.planning/phases/v0.22-DEM-1H-multi-resource-selection/RESEARCH.md` U5;
  `@.planning/phases/v0.22-K-DEM-1/K-DEM-1-FACTS.md` C5). Its body is byte-identical to the
  Demand Data Update package's FAQ (same SHA-256), though the two resources carry different
  CKAN `last_modified` values. None of its paragraphs defines the literal `NA` token.

## Families

### `historic_demand`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| SETTLEMENT_DATE | `settlement_date` | date | `%d-%b-%Y` | no | — | — |
| SETTLEMENT_PERIOD | `settlement_period` | int64 | — | no | — | — |
| ND | `nd` | float64 | — | yes | — | MW |
| TSD | `tsd` | string | — | yes | — | MW |
| ENGLAND_WALES_DEMAND | `england_wales_demand` | float64 | — | yes | — | MW |
| EMBEDDED_WIND_GENERATION | `embedded_wind_generation` | string | — | yes | — | MW |
| EMBEDDED_WIND_CAPACITY | `embedded_wind_capacity` | string | — | yes | — | MW |
| EMBEDDED_SOLAR_GENERATION | `embedded_solar_generation` | string | — | yes | — | MW |
| EMBEDDED_SOLAR_CAPACITY | `embedded_solar_capacity` | string | — | yes | — | MW |
| NON_BM_STOR | `non_bm_stor` | float64 | — | yes | — | MW |
| PUMP_STORAGE_PUMPING | `pump_storage_pumping` | float64 | — | yes | — | MW |
| IFA_FLOW | `ifa_flow` | float64 | — | yes | — | MW |
| IFA2_FLOW | `ifa2_flow` | string | — | yes | — | MW |
| BRITNED_FLOW | `britned_flow` | string | — | yes | — | MW |
| MOYLE_FLOW | `moyle_flow` | string | — | yes | — | MW |
| EAST_WEST_FLOW | `east_west_flow` | string | — | yes | — | MW |
| NEMO_FLOW | `nemo_flow` | string | — | yes | — | MW |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| SETTLEMENT_DATE | `settlement_date` | date | `%d-%b-%Y` | no | — | — |
| SETTLEMENT_PERIOD | `settlement_period` | int64 | — | no | — | — |
| ND | `nd` | float64 | — | yes | — | MW |
| TSD | `tsd` | string | — | yes | — | MW |
| ENGLAND_WALES_DEMAND | `england_wales_demand` | float64 | — | yes | — | MW |
| EMBEDDED_WIND_GENERATION | `embedded_wind_generation` | string | — | yes | — | MW |
| EMBEDDED_WIND_CAPACITY | `embedded_wind_capacity` | string | — | yes | — | MW |
| EMBEDDED_SOLAR_GENERATION | `embedded_solar_generation` | string | — | yes | — | MW |
| EMBEDDED_SOLAR_CAPACITY | `embedded_solar_capacity` | string | — | yes | — | MW |
| NON_BM_STOR | `non_bm_stor` | float64 | — | yes | — | MW |
| PUMP_STORAGE_PUMPING | `pump_storage_pumping` | float64 | — | yes | — | MW |
| IFA_FLOW | `ifa_flow` | float64 | — | yes | — | MW |
| IFA2_FLOW | `ifa2_flow` | string | — | yes | — | MW |
| BRITNED_FLOW | `britned_flow` | string | — | yes | — | MW |
| MOYLE_FLOW | `moyle_flow` | string | — | yes | — | MW |
| EAST_WEST_FLOW | `east_west_flow` | string | — | yes | — | MW |
| NEMO_FLOW | `nemo_flow` | string | — | yes | — | MW |
| NSL_FLOW | `nsl_flow` | string | — | yes | — | MW |
| ELECLINK_FLOW | `eleclink_flow` | string | — | yes | — | MW |
| VIKING_FLOW | `viking_flow` | string | — | yes | — | MW |
| GREENLINK_FLOW | `greenlink_flow` | string | — | yes | — | MW |

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| SETTLEMENT_DATE | `settlement_date` | date | `demanddata_2001.csv` → `%Y-%m-%d`; `demanddata_2002.csv` → `%Y-%m-%d`; `demanddata_2003.csv` → `%Y-%m-%d`; `demanddata_2004.csv` → `%Y-%m-%d`; `demanddata_2005.csv` → `%Y-%m-%d`; `demanddata_2006.csv` → `%Y-%m-%d`; `demanddata_2007.csv` → `%Y-%m-%d`; `demanddata_2008.csv` → `%Y-%m-%d`; `demanddata_2023.csv` → `%d-%b-%y`; `demanddata_2024.csv` → `%d-%b-%Y`; `demanddata_2025.csv` → `%Y-%m-%d` | no | — | — |
| SETTLEMENT_PERIOD | `settlement_period` | int64 | — | no | — | — |
| ND | `nd` | float64 | — | yes | — | MW |
| TSD | `tsd` | string | — | yes | — | MW |
| ENGLAND_WALES_DEMAND | `england_wales_demand` | float64 | — | yes | — | MW |
| EMBEDDED_WIND_GENERATION | `embedded_wind_generation` | string | — | yes | — | MW |
| EMBEDDED_WIND_CAPACITY | `embedded_wind_capacity` | string | — | yes | — | MW |
| EMBEDDED_SOLAR_GENERATION | `embedded_solar_generation` | string | — | yes | — | MW |
| EMBEDDED_SOLAR_CAPACITY | `embedded_solar_capacity` | string | — | yes | — | MW |
| NON_BM_STOR | `non_bm_stor` | float64 | — | yes | — | MW |
| PUMP_STORAGE_PUMPING | `pump_storage_pumping` | float64 | — | yes | — | MW |
| SCOTTISH_TRANSFER | `scottish_transfer` | string | — | yes | — | MW |
| IFA_FLOW | `ifa_flow` | float64 | — | yes | — | MW |
| IFA2_FLOW | `ifa2_flow` | string | — | yes | — | MW |
| BRITNED_FLOW | `britned_flow` | string | — | yes | — | MW |
| MOYLE_FLOW | `moyle_flow` | string | — | yes | — | MW |
| EAST_WEST_FLOW | `east_west_flow` | string | — | yes | — | MW |
| NEMO_FLOW | `nemo_flow` | string | — | yes | — | MW |
| NSL_FLOW | `nsl_flow` | string | — | yes | — | MW |
| ELECLINK_FLOW | `eleclink_flow` | string | — | yes | — | MW |
| VIKING_FLOW | `viking_flow` | string | — | yes | — | MW |
| GREENLINK_FLOW | `greenlink_flow` | string | — | yes | — | MW |

Schema, epoch 4:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| SETTLEMENT_DATE | `settlement_date` | date | `%Y-%m-%d` | no | — | — |
| SETTLEMENT_PERIOD | `settlement_period` | int64 | — | no | — | — |
| ND | `nd` | float64 | — | yes | — | MW |
| FORECAST_ACTUAL_INDICATOR | `forecast_actual_indicator` | string | — | yes | — | — |
| TSD | `tsd` | string | — | yes | — | MW |
| ENGLAND_WALES_DEMAND | `england_wales_demand` | float64 | — | yes | — | MW |
| EMBEDDED_WIND_GENERATION | `embedded_wind_generation` | string | — | yes | — | MW |
| EMBEDDED_WIND_CAPACITY | `embedded_wind_capacity` | string | — | yes | — | MW |
| EMBEDDED_SOLAR_GENERATION | `embedded_solar_generation` | string | — | yes | — | MW |
| EMBEDDED_SOLAR_CAPACITY | `embedded_solar_capacity` | string | — | yes | — | MW |
| NON_BM_STOR | `non_bm_stor` | float64 | — | yes | — | MW |
| PUMP_STORAGE_PUMPING | `pump_storage_pumping` | float64 | — | yes | — | MW |
| SCOTTISH_TRANSFER | `scottish_transfer` | string | — | yes | — | MW |
| IFA_FLOW | `ifa_flow` | float64 | — | yes | — | MW |
| IFA2_FLOW | `ifa2_flow` | string | — | yes | — | MW |
| BRITNED_FLOW | `britned_flow` | string | — | yes | — | MW |
| MOYLE_FLOW | `moyle_flow` | string | — | yes | — | MW |
| EAST_WEST_FLOW | `east_west_flow` | string | — | yes | — | MW |
| NEMO_FLOW | `nemo_flow` | string | — | yes | — | MW |
| NSL_FLOW | `nsl_flow` | string | — | yes | — | MW |
| ELECLINK_FLOW | `eleclink_flow` | string | — | yes | — | MW |
| VIKING_FLOW | `viking_flow` | string | — | yes | — | MW |
| GREENLINK_FLOW | `greenlink_flow` | string | — | yes | — | MW |

- Entity key: `resource_id`, `settlement_date`, `settlement_period`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`settlement_date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Epoch numbering.** This page numbers the header epochs 1–4. The registry record
(`epochs[0..3]`), ADR-039 and the K-DEM-1 FACTS number the same headers 0–3, so page epoch N
is record epoch N−1. The order follows the profiler, **not** chronology. The 2001–2008 files
were backfilled with a later-style header, so a column "added" between epochs is not
evidence of when an interconnector was commissioned or a measure first existed (FACTS
§historic_demand).

| Page epoch | Years | Rows | Header change from the previous epoch | `SETTLEMENT_DATE` parse |
|---:|---|---:|---|---|
| 1 | 2009–2018 | 175,296 | — | scalar `%d-%b-%Y` |
| 2 | 2019–2022 | 70,128 | adds `NSL_FLOW`, `ELECLINK_FLOW`, `VIKING_FLOW`, `GREENLINK_FLOW` | scalar `%d-%b-%Y` |
| 3 | 2001–2008, 2023–2025 | 192,864 | adds `SCOTTISH_TRANSFER` | per filename (see below) |
| 4 | 2026 | 12,478 | adds `FORECAST_ACTUAL_INDICATOR` after `ND` | scalar `%Y-%m-%d` |

No surviving header name is renamed. Page epoch 4 is the same header as
`daily_demand_update` (@./daily-demand-update.md).

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource file. CKAN emits it without an offset, and
   gridflow reads it as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`).
   Unlike a single-file family, the vintage here is **per resource**. Every row of one yearly
   file shares that file's vintage, so the family carries 26 vintages. They fall in five
   upload cohorts (see the resource table): 2009–2018 on 2023-07-24, 2019–2024 on 2025-04-08,
   2001–2008 on 2025-06-20, 2025 on 2026-06-09, and 2026 on 2026-10-08. Checked against silver
   on 2026-10-09: each resource has exactly one `published_at`, equal to its sidecar value, and
   `available_at = published_at` on every row. The record has no issue time (issue recipe
   `none`).
   - The vintage says when the **file** last changed, not when any settlement period was
     first published. The vendor publishes 21 days in arrears and corrects data afterwards,
     and gridflow sees each correction only as a new version of a whole yearly file. So a
     row's `available_at` can be years after its settlement date. That is conservative
     for point-in-time use: an as-of query never sees a value before its file version
     existed. The cost is that an as-of date before a resource's `last_modified` sees **no**
     rows from that resource, because only one capture of each exists. For example, the
     2009–2018 files are invisible to any as-of before 2023-07-24.
   - ADR-039 FM-12 (accepted residual): when a body's `ckan_last_modified` predates its
     capture (every file here, e.g. 2009 modified 2023-07-24, captured 2026-10-08),
     `available_at <= as_of` is not proof the bytes gridflow holds were the ones published at
     that instant. An earlier version of the file may have existed and been overwritten
     before capture.
2. **Event time (`sp_pair` on `settlement_date`, `settlement_period`).** `timestamp_utc` is the
   **start** of the settlement period: UK local midnight of the settlement date, plus 30
   minutes per period after the first, converted to UTC. `event_time` equals `timestamp_utc`.
   Event time is therefore **not** the capture time for this family. The FAQ settles the
   convention: "All times are UK time and for the half hour beginning" (FACTS C5, T02/T06/T22).
   The 2026 dictionary agrees: "Settlement period 1 runs from 00:00-00:30", and its
   `SETTLEMENT_DATE` comment reads "This follows clock change." Checked against silver on
   2026-10-09:
   - The period-start mapping holds on all 450,766 rows, and `timestamp_utc` is unique across
     the family.
   - Days by period count: 26 days of 46, 9,340 of 48 and 25 of 50. `settlement_period` spans
     1..50. Examples from the activation receipt: 2005-03-27 has 46 periods, 2023-10-29 and
     2024-10-27 have 50.
   - The 2026 body (to 2026-09-17) holds the spring short day but not yet the autumn long
     day. The record's period range stays 1..50 regardless.
   - The conversion is the shared settlement helper, not family-specific code.

   The local Elexon cross-check supports period start as corroboration only (FACTS §DEM1-1,
   C7). Current-year ND joined to INDO matched exactly on 125 of 12,092 pairs mapped as
   period start, and on 7 of 12,092 mapped as period end. TSD against ITSDO is too sparse to
   decide timing. Equality is not expected in general, because these are retrospectively
   corrected values. The FAQ, not these tallies, is the authority.

**Units (vendor dictionary only).** The skeleton's MW column comes from the field info of the
2026 resource, the one the profiler read (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/historic_demand.json`; package
page [historic-demand-data](https://www.neso.energy/data-portal/historic-demand-data)). Every
demand, embedded-generation, capacity, STOR, pumping, Scottish-transfer and interconnector
column there is **MW**. The earlier epochs rest on two further sources: the FAQ's
dataset-wide answer ("MW"), and the 2001 and 2025 resource dictionaries, which describe the
same measures as MW (RESEARCH U5; FACTS g4). `TODO: verify` the 2002–2024 per-year
dictionaries, which were not read individually. `SETTLEMENT_PERIOD` has an empty dictionary
unit: it is an ordinal, not a quantity. `FORECAST_ACTUAL_INDICATOR` has an empty unit: it is
a category (`A` actual, `F` forecast), not a physical value. Definitions worth keeping, from
the 2026 dictionary:

- **ND** is the sum of metered generation. It excludes generation for station load,
  pump-storage pumping and interconnector exports, and is calculated from the Transmission
  Network Operators' operational generation metering.
- **TSD** = ND plus station load, pumping and exports. It includes an estimate of station load
  of 500 MW in BST and 600 MW in GMT.
- **England and Wales demand** is ND on an England and Wales basis.
- **Embedded wind and solar** generation are model estimates of output NESO cannot meter. The
  capacities are NESO's "best view", not definitive.
- **Non-BM STOR** covers units outside the ND generator definition, as generation or demand
  reduction.
- **Pump storage pumping**: "the -ve signifies pumping load".
- **Scottish transfer** is the flow from Scotland to England and Wales; negative means England
  and Wales to Scotland.
- **Interconnector flows**: negative means export out of GB, positive means import into GB.

`TODO: verify` semantic continuity across the years. The current dictionary is not a change
log for every epoch. The FAQ distinguishes operational TSD from I014 settlement-derived TSD
and records that I014 data was removed pending a quality investigation (FACTS C5). Keep the
vendor fields as delivered. Do not substitute I014 measures for operational ND/TSD, add
embedded generation into ND, or negate pumping values to "correct" their sign.

**Sentinels and missing values (FACTS g5; RESEARCH U5).** The vendor declares no sentinel
spelling, and the record has no null-token map.

- **Literal `NA`** is kept as the string `NA`. No NESO source defines it (FAQ, 2001/2025/2026
  dictionaries and package notes all read). It is the subject of the hold. Every column that
  carries `NA` in any body is typed `string` in **every** epoch, because a silver name has one
  dtype across epochs (ADR-039 C-3, record rule V-1). Measured `NA` placement on 2026-10-09
  (missingness only):

  | Column(s) | Resource years where every row is `NA` |
  |---|---|
  | `TSD`, `MOYLE_FLOW` | 2001–2004 |
  | `EMBEDDED_WIND_GENERATION`, `EMBEDDED_WIND_CAPACITY` | 2001–2006 |
  | `EMBEDDED_SOLAR_GENERATION`, `EMBEDDED_SOLAR_CAPACITY`, `SCOTTISH_TRANSFER`, `IFA2_FLOW`, `BRITNED_FLOW`, `EAST_WEST_FLOW`, `NEMO_FLOW`, `NSL_FLOW`, `ELECLINK_FLOW`, `VIKING_FLOW`, `GREENLINK_FLOW` | 2001–2008 |

  No other year has a literal `NA`, and none is partial: in each case the token fills the whole
  year. Column totals match FACTS T07–T21 (70,128 / 105,168 / 140,256). `ND`,
  `ENGLAND_WALES_DEMAND`, `NON_BM_STOR`, `PUMP_STORAGE_PUMPING` and `IFA_FLOW` have no `NA` in
  any body and are `float64`.
- **Structural nulls.** A column absent from a body's header is null in that body's silver
  rows. `NSL_FLOW`, `ELECLINK_FLOW`, `VIKING_FLOW` and `GREENLINK_FLOW` are null for 2009–2018
  (175,296 rows). `SCOTTISH_TRANSFER` is null for 2009–2022 (245,424 rows).
  `FORECAST_ACTUAL_INDICATOR` is null for 2001–2025 (438,288 rows). These nulls mean "not in
  this file", not a vendor missing value.
- **Zeros are preserved as values**, never converted to null, whatever their run length.
  `TODO: verify` whether an all-zero
  interconnector run means no flow, unavailable history or a backfill placeholder.
- `-1` in signed flow columns is kept as a number. The vendor defines negative as the export
  direction, so there is no global sentinel conversion. `TODO: verify` the meaning of `-1` in
  `NON_BM_STOR`, which the vendor does not document.
- `TODO: verify` the sign of `PUMP_STORAGE_PUMPING`. The dictionary says negative signifies
  pumping load, but FACTS g5 records positive entries in the captured bodies. Values are kept
  unchanged until the vendor clarifies.
- Literal `N/A` was not observed by the full-body token scan, so no such spelling is declared.

**Identity and selection (ADR-039).** The entity key is `(resource_id, settlement_date,
settlement_period)`.

- `resource_id` is **not a vendor column**. The engine stamps each row with its capture's
  sidecar resource UUID (ADR-039 P-2). It is a reserved name, so a vendor column of that name
  would be refused.
- `_latest` is `whole_capture` **per `resource_id`** (`latest_partition: resource_id`, P-1/P-3).
  It keeps the newest complete capture of each yearly file, rather than the single newest
  capture of the whole family, which would have kept only 2026. The as-of bound is applied
  before ranking, so each resource's winner is chosen only among captures available at the
  as-of instant.
- The settlement pair is unique within every body, and **no pair is shared across resources**:
  2001–2025 each span exactly their filename year (RESEARCH U4). That disjointness is measured,
  not a vendor guarantee.
- If NESO ever recreates a year under a new UUID with the same name, gridflow treats the two
  UUIDs as two resources. `_latest` serves both, and reconcile reports an `overlap` gap for
  every shared pair. No precedence is invented (ADR-039 P-5, C-1, FM-7). A deleted resource
  leaves its last capture in `_latest` (FM-8).
- Do not dedup on `(settlement_date, settlement_period)` alone. There is no run type or
  version column, and none is invented. `TODO: verify` an explicit vendor revision identity
  (FACTS T24). Revisions arrive only as a new version of the whole yearly file.

**Per-filename date formats (ADR-039 P-4).** Page epoch 3 shares one header across three
`SETTLEMENT_DATE` forms. The record maps each exact filename to a format:
`demanddata_2001.csv`–`demanddata_2008.csv` and `demanddata_2025.csv` use `%Y-%m-%d`,
`demanddata_2023.csv` uses `%d-%b-%y`, and `demanddata_2024.csv` uses `%d-%b-%Y`. An epoch-3
body whose filename is not listed fails the capture (`UnmappedResourceFormatError`) with a
failure record and no completion; there is no fallback. Epochs 1, 2 and 4 use one scalar
format. Accepted residual FM-9: a `%d-%b-%Y` column that meets a two-digit-year body parses
silently as year `00yy`, and no strict parser tells the two apart. Every 2026-10-08 body was
measured, and the tests check each fixture's dates fall in its filename year, but a future
re-upload could still trip it. A downstream guard catches it: every row's settlement date
should fall in its filename year.

**Row composition.** All 12,478 rows of the 2026 body are labelled `A` (actual) (FACTS C10;
silver 2026-10-09). The 2001–2025 bodies have no indicator column. The 2026 resource
description carries a vendor note, verbatim: "NESO have moved the data source to its new
forecast system. We are aware of an issue with missing Scottish transfer data". The 2026
body's `SCOTTISH_TRANSFER` has no literal `NA` and no null cells. `TODO: verify` how the
missing Scottish-transfer data appears in the file, and which settlement dates it affects.

**Relationship to Demand Data Update (`daily_demand_update`).** The 2026 body and the daily
file share an identical header. On their overlap (2026-09-01 → 2026-09-17, 816 settlement
pairs), every column is equal on every row (FACTS C3, §DEM1-4), so neither capture is a
measured revision of the other. The vendor describes this package as 21 days in arrears with
retrospective corrections, and the daily package as about ten days' lag plus a forecast
tail. `TODO: verify` cross-package revision precedence: the vendor states no rule that either
package overrides the other. A consumer may choose "historic first, daily as faster fallback"
as an explicit policy, but must not present it as a vendor hierarchy.

**Activation (2026-10-09, master `6070640`, PR #90).** ADR-039 landed in PR #90, and the
family was transformed from the 2026-10-08 captures (26 captures; no prior silver, so nothing
was overwritten). Silver has **450,766 rows**, equal to the planned count. The
`silver_neso_data_portal_historic_demand_latest` view serves 450,766 rows over 26 resources
and 26 years (2001-01-01 → 2026-09-17), which shows the per-resource selection working. The
key has 0 duplicates. Reconcile `--all --cutoff 2026-10-08` exited 0 with 0 gaps over 37
families, including `overlap` 0. Coverage was unchanged at 1,379 captured and 6 missing
(gridflow `@.planning/v0.22-RESULTS.md` §DEM-1H; RULINGS 535–537).

Silver layout: 26 Parquet files under
`C:/gridflow-data/silver/neso_data_portal/historic_demand/year=2026/month=10/`. The
`year=`/`month=` partition is the **capture** date, not the settlement date, so do not
partition-prune by settlement year. Columns (32): the 23-column vendor union (the 21 columns
of the page-epoch-2 header, then the epoch-only `scottish_transfer` and
`forecast_actual_indicator`); then `resource_id`; then `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`.
All timestamps are tz-aware UTC. `dataset_version` is `1+e1`: record version 1 and generic
engine version 1 (`ENGINE_VERSION`, gridflow `@src/gridflow/silver/neso_data_portal/generic.py`).
It is the same for every epoch.

### `historic_demand_files`

- Kind: files · archetype: SER · refresh: daily · empty allowed: no
- files: catalogue only

This family captures the FAQ document (see DOC above). It produces no silver output. Its text is
the primary source for this page's unit, half-hour-average and period-start statements.

Clocks: with no silver rows, there is no event time (`timestamp_utc` does not arise). The only
clock is the document's vintage, its CKAN `last_modified` (2024-10-21T12:04:20.336881, read as
UTC).

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The package notes say the data "is populated 21 days in arrears". Corrections to solar
capacity and outturn, and to demand, can follow months later. The resource descriptions give
no update time of day. Only the current-year file appears to change routinely. Its CKAN
`last_modified` was 2026-10-06T08:20:29.686856 in the 2026-10-06 catalogue snapshot and
2026-10-08T08:20:27.652049 at capture two days later. Past years change in batches: the four
past-year upload cohorts in the resource table (2023-07-24, 2025-04-08, 2025-06-20,
2026-06-09).
`TODO: verify` the current-year file's update cadence and whether each update also revises
earlier rows of the year. Only more captures, compared pair by pair, can show this. One
capture of each resource exists to date (2026-10-08). Whatever the capture schedule, the
per-resource `_latest` keeps each year's newest complete capture.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `historic_demand`: held: TODO: literal NA in the epoch-2 bodies (2001-2008, 2023-2025) in TSD, the embedded wind/solar columns, SCOTTISH_TRANSFER and every interconnector flow but IFA: missing, not applicable or zero? NESO defines no meaning; those columns stay text across every epoch until it does. (unit E-SEM)

The silver output exists on disk, but it is **held**: it is not eligible for publication or for
point-in-time model use until unit E-SEM answers the question above. The record carries the
hold (ADR-039 P-6), and RULINGS 537 confirms it at activation. NESO's files put a literal `NA`
where these MW columns would hold a number. The vendor never says whether `NA` means "data
missing", "not applicable" (for example before an interconnector existed) or zero.
Declaring it a null token, reading it as zero, or dropping the rows would each invent a
missing-value rule. So the token is kept as delivered, and every affected column stays text
in every year, including the years with no `NA` (ADR-039 C-3; RESEARCH U5). This page
therefore gives schema, row counts, clocks and missingness only, not data values or ranges.

The generated hold line names the whole page-epoch-3 header group (2001–2008, 2023–2025).
Measured on 2026-10-09, the token occurs only in the 2001–2008 files (see Sentinels above).
The 2023–2025 files share the header but carry no `NA`.

What settles it: a vendor definition of the literal `NA`, including whether its meaning
differs by field or by historical year. Once it exists, switching the affected columns to
numeric is a one-record edit. Every non-`NA` value already casts to float (ADR-039 C-3).

How the hold came about: `historic_demand` was split out of the demand batch into its own
unit, because per-family `whole_capture`, the bare-pair key and the mixed date formats could
not express it (RULINGS 528). That unit was ruled the highest ceremony tier, because it
changes `_latest` revision selection on the point-in-time path (RULINGS 530). It merged
triple-green as PR #90 (RULINGS 535) and was activated with the hold in place (RULINGS
536–537).

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. The hold is per family and sits on `historic_demand`. Related holds in the same batch
(gridflow `@docs/neso_data_portal/eligibility.md`): `daily_demand_update` is held on the
meaning of zero ND/TSD on forecast rows, also unit E-SEM.

**Implementation delta (vendor dictionary vs record).**

- The 2026 dictionary types every value column as `integer` (`int4`). The record casts the
  `NA`-free columns to nullable `float64` (the batch rule for demand and flow columns) and
  keeps the `NA`-carrying columns as `string`.
- The dictionary describes the `NA`-carrying measures as MW numbers. The 2001–2008 bodies
  deliver a literal `NA` in them instead (the hold).
- The 2026 dictionary's `SETTLEMENT_DATE` example is `01/01/2026`. The captured 2026 body uses
  `%Y-%m-%d`, which the record parses. The body is ground truth. Within one header (page
  epoch 3) the bodies use three different date formats, which the record maps per filename.
- The dictionary says negative `PUMP_STORAGE_PUMPING` signifies pumping load; the captured
  bodies also contain positive entries (FACTS g5). `TODO: verify`.
- The dictionary calls ND "equivalent to" INDO and TSD to ITSDO. Measured equality against the
  local Elexon holdings is sparse (see the event-time section). `TODO: verify` whether the
  vendor values are later revisions of the initial outturns.
