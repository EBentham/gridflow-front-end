---
source: "neso_data_portal"
package: "bsuos-monthly-forecast"
dataset_keys: ["bsuos_monthly_forecast_actual_sum", "bsuos_monthly_forecast_fc_summary", "bsuos_monthly_forecast_fc_summary_pct", "bsuos_monthly_forecast_impact_on_due", "bsuos_monthly_forecast_including_new", "bsuos_monthly_forecast_sum_winter", "bsuos_monthly_forecast_summary", "bsuos_monthly_forecast_summary_pct"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-12
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: true
  title: Monthly BSUoS forecast
  summary: >-
    NESO's monthly forecast of balancing costs for each of the next 24 months, in £m, with older
    outturn summaries and COVID scenarios.
  facts:
    vendor: "NESO Data Portal: 142 CSV files, a zipped workbook archive and a PDF"
    cadence: "Monthly, as NESO lists it; each month's forecast is a new file"
    grain: "Forecast: one file per edition, one row per target month, costs in £m"
    history: NESO lists files from March 2020
  landscape: market
  what_it_is: >-
    The Balancing Services Use of System (BSUoS) charge recovers the cost of day-to-day system
    operation. Each month NESO forecasts those costs for the next 24 months, by category, such as
    energy imbalance, reserve and constraints, with an estimated BSUoS volume. Older files add
    outturn summaries and COVID demand scenarios. NESO says the forecast may bear no relation to
    later tariffs.
  how_used:
    - How NESO's expected balancing cost for a month moved from edition to edition
    - Expected costs beside the settled BSUoS charges and fixed tariffs
  raw_feed:
    note: >-
      NESO's `package_show`, then each file whole unless `last_modified` is unchanged (a few
      shown). Only forecast summary files with a valid UTF-8 header reach silver; everything else
      is bronze only.
    commands:
      - {run: gridflow ingest neso_data_portal bsuos_monthly_forecast_fc_summary --last 24h, comment: "whole files; swap in any key"}
      - {run: gridflow transform neso_data_portal bsuos_monthly_forecast_fc_summary --last 24h, comment: "forecast summary only; rows not shown"}
      - {run: gridflow ingest neso_data_portal bsuos_monthly_forecast_files --last 24h, comment: the archive and PDF}
  family:
    slug: bsuos-monthly-forecast
    members:
      - dataset: bsuos_monthly_forecast_actual_sum
        differs: "Outturn for the previous 12 months; monthly files, March 2020 to December 2021"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=bsuos-monthly-forecast"
          - "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/fdd43811-b1ff-490e-8ad2-98d67822931e/download/monthly-bsuos-actual-summary-mar_20.csv"
          - "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/1f8b0d9a-a98b-4cf4-9496-16a5c9db551f/download/monthly-bsuos-actual-summary-14122021.csv"
        held: "The header's £ is not valid UTF-8, so gridflow keeps these files in bronze only."
      - dataset: bsuos_monthly_forecast_fc_summary
        differs: "The 24-month forecast, one file per monthly edition, from March 2020"
        request:
          - "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/ef004890-679a-4d28-ac00-427ff6e7260d/download/monthly-bsuos-forecast-summary-mar_20.csv"
          - "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/b458c4e5-ab80-43e5-907e-6c7069350390/download/bsuos-forecast-october-2026.csv"
        held: NESO does not say when each monthly edition was issued, only when its file last changed.
      - dataset: bsuos_monthly_forecast_fc_summary_pct
        differs: "The forecast under COVID demand cuts of 5, 10 and 15 percent"
        request:
          - "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/9b840832-2438-472e-906e-45edbb311e1b/download/monthly-bsuos-forecast-summary-june-5-percent.csv"
          - "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/f6a319e9-5423-4edb-bbae-48e61088b36a/download/monthly-bsuos-forecast-summary-september-15-percent.csv"
        held: "The header's £ is not valid UTF-8, so gridflow keeps these files in bronze only."
      - dataset: bsuos_monthly_forecast_impact_on_due
        differs: A COVID low-demand forecast without the new commercial services
        request: "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/8fad0617-c238-4bbf-b6f3-418862dcbf17/download/monthly-bsuos-summary-no-new-services.csv"
        held: "The header's £ is not valid UTF-8, so gridflow keeps this file in bronze only."
      - dataset: bsuos_monthly_forecast_including_new
        differs: "The May 2020 COVID forecast, with the new services' savings"
        request: "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/5ed292d9-f4cc-4034-b0f4-cdf3477cbaa4/download/monthly-bsuos-summary-expected-costs.csv"
        held: "The header's £ is not valid UTF-8, so gridflow keeps this file in bronze only."
      - dataset: bsuos_monthly_forecast_sum_winter
        differs: The September 2022 edition with a winter contingency cost column
        request: "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/839c1a80-ce74-4cd4-b634-197a54974b29/download/bsuos-forecast-september-2022-with-winter-contingency-cost.csv"
        held: "One header £ is not valid UTF-8, so gridflow keeps this file in bronze only."
      - dataset: bsuos_monthly_forecast_summary
        differs: "Past 12 months' outturn with the next 24 months' forecast, 2020 to 2021"
        request:
          - "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/6b20199f-8f95-4409-b26e-d89cbf5255da/download/monthly-bsuos-summary-mar_20.csv"
          - "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/b9fbb769-bb54-4f00-95f1-888421fcbdbe/download/monthly-bsuos-summary-14122021.csv"
        held: "The header's £ is not valid UTF-8, so gridflow keeps these files in bronze only."
      - dataset: bsuos_monthly_forecast_summary_pct
        differs: "That combined summary under the 5, 10 and 15 percent COVID cuts"
        request:
          - "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/253e5f12-a555-4792-a613-2bafa657e4fc/download/monthly-bsuos-summary-june-5-percent.csv"
          - "GET https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/87b7525c-a434-4162-9e5c-658e12b01f61/download/monthly-bsuos-summary-september-15-percent.csv"
        held: "The header's £ is not valid UTF-8, so gridflow keeps these files in bronze only."
  related:
    - {dataset: neso_data_portal/current-balancing-services-use-of-system-bsuos-data, note: "Settled BSUoS charges per run, to set against these forecasts"}
    - {dataset: neso_data_portal/bsuos-fixed-tariffs, note: "The fixed tariffs NESO sets, which this forecast may not match"}
    - {dataset: neso_data_portal/daily-balancing-costs-balancing-services-use-of-system, note: "Outturn balancing cost per settlement period, in six categories"}
    - {dataset: neso_data_portal/balancing-services-use-of-system-bsuos-daily-forecast, note: "NESO's half-hourly BSUoS charge forecast, to March 2023"}
---

# Monthly Balancing Services Use of System (BSUoS) Forecast Data

This package is NESO's **rolling forecast of Balancing Services Use of System (BSUoS) costs**.
BSUoS is the charge that recovers the cost of balancing the GB system. NESO reports it monthly,
with a forecast for the next month and a rolling 24-month period, and this package holds the
24-month-ahead forecast (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). The vendor
publishes it "without prejudice" and warns that it is an estimate that may bear no relation to
the indicative or actual tariffs NESO publishes later. Each monthly **edition** is one CSV with
one row per **target month** (24 rows in every loaded edition) and one column per cost
component: energy imbalance, positive and negative reserve, frequency control, constraints,
restoration, other, the total balancing cost, NESO's internal cost and incentive, and an
estimated BSUoS volume. The question it answers is "what did NESO expect balancing to cost in
each of the next 24 months, as published in this edition?" For modelling it is the
**expectation side** of BSUoS cost recovery, to be compared with settled outturn
(@./current-balancing-services-use-of-system-bsuos-data.md) and the fixed tariffs
(@./bsuos-fixed-tariffs.md).

The package is big and uneven. CKAN lists **144 resources**: 142 CSVs, one PDF and one
workbook archive. They fall into **eight tabular families** that gridflow captured on
2026-10-08. Only **one family has silver**, `bsuos_monthly_forecast_fc_summary`, and it is
**held**: the vendor gives no issue time for any edition, so no edition can yet be placed on a
point-in-time clock (see Holds). **The other seven tabular families are ingest-only**: their
bodies are not valid UTF-8 (a `0xA3` pound byte) and gridflow has no record for them
(RULINGS 667). The workbook archive is held and the PDF is a document. Because the one silver
family is held, **this page gives schema, row counts, clocks and missingness only, with no
data values**.

- Publisher group: Balancing costs
- Registry group: balancing · archetype: FC
- Package page: [bsuos-monthly-forecast](https://www.neso.energy/data-portal/bsuos-monthly-forecast)
- Attribution: Supported by National Energy SO Open Data

**Related packages.** The settled charges are in
@./current-balancing-services-use-of-system-bsuos-data.md and the fixed tariffs in
@./bsuos-fixed-tariffs.md. The sibling **daily BSUoS forecast** package
(@./balancing-services-use-of-system-bsuos-daily-forecast.md) is a separate package and has
**no record and no silver family**: its bodies carry no run column and are not valid UTF-8
(RULINGS 667, 538, 653).

**Where each family stands (2026-10-12).**

| Family | CSV resources | Header epochs | Encoding of captured bodies | Status |
|---|---:|---:|---|---|
| `bsuos_monthly_forecast_fc_summary` | 75 | 16 raw / 14 reader (8 in the record) | 53 valid UTF-8, 22 invalid | **silver, held**: 53 editions loaded, 1,272 rows; 22 captures adjudicated |
| `bsuos_monthly_forecast_actual_sum` | 22 | 2 | none valid UTF-8 | ingest-only, no record |
| `bsuos_monthly_forecast_fc_summary_pct` | 12 | 2 | none valid UTF-8 | ingest-only, no record |
| `bsuos_monthly_forecast_impact_on_due` | 1 | 1 | not valid UTF-8 | ingest-only, no record |
| `bsuos_monthly_forecast_including_new` | 1 | 1 | not valid UTF-8 | ingest-only, no record |
| `bsuos_monthly_forecast_sum_winter` | 1 | 1 | mixed bytes, not valid UTF-8 | ingest-only, no record |
| `bsuos_monthly_forecast_summary` | 18 | 5 | none valid UTF-8 | ingest-only, no record |
| `bsuos_monthly_forecast_summary_pct` | 12 | 1 | none valid UTF-8 | ingest-only, no record |
| `bsuos_monthly_forecast_files` | 2 (PDF, ZIP) | n/a | n/a | catalogue only: 1 DOC, 1 HOLD |

Counts are from the batch research (gridflow
`@.planning/phases/v0.22-K-BAL-2/K-BAL-2-FACTS.md`, sections 2 and 4) and the registry record
(gridflow `@src/gridflow/connectors/neso_data_portal/registry/bsuos-monthly-forecast.json`).

## Files by disposition

Every one of the 144 resources is an uploaded file (`url_type` upload), listed below with its
registry disposition: **142 SILVER, 1 DOC, 1 HOLD**. The registry assigns SILVER to every CSV
because each CSV is a candidate data file for its family. It does **not** mean a silver table
exists. Of the eight tabular families, only `bsuos_monthly_forecast_fc_summary` has a record and
silver (held), and 22 of its 75 resources failed to decode (see that family). The CSVs of the
other seven families are in bronze only. Every resource was captured once, on 2026-10-08, as
immutable bronze bytes. A resource's file is served at
`https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/<Id>/download/<file name>`.
The vendor's file names differ from the resource names below; the file names that matter are
given where a family, the edition map, or the PDF is described.

Resource counts by family and disposition:

| Family | SILVER | DOC | HOLD |
|---|---:|---:|---:|
| `bsuos_monthly_forecast_actual_sum` | 22 | 0 | 0 |
| `bsuos_monthly_forecast_fc_summary` | 75 | 0 | 0 |
| `bsuos_monthly_forecast_fc_summary_pct` | 12 | 0 | 0 |
| `bsuos_monthly_forecast_impact_on_due` | 1 | 0 | 0 |
| `bsuos_monthly_forecast_including_new` | 1 | 0 | 0 |
| `bsuos_monthly_forecast_sum_winter` | 1 | 0 | 0 |
| `bsuos_monthly_forecast_summary` | 18 | 0 | 0 |
| `bsuos_monthly_forecast_summary_pct` | 12 | 0 | 0 |
| `bsuos_monthly_forecast_files` | 0 | 1 | 1 |

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| BSUoS Forecast for May 2020 – Including new services | CSV | upload | `5ed292d9-f4cc-4034-b0f4-cdf3477cbaa4` |
| Impact on BSUoS due to COVID-19 low demands – Excluding new services | CSV | upload | `8fad0617-c238-4bbf-b6f3-418862dcbf17` |
| Monthly BSUOS Actual Summary February 2021 | CSV | upload | `d1e5c83a-b276-4e0e-9737-8e1d79656b30` |
| Monthly BSUOS Actual Summary March 2021 | CSV | upload | `c9876d87-2b78-4b35-972a-4bb7f2b7d025` |
| Monthly BSUOS Forecast Summary August 10 Percent | CSV | upload | `21ec8a37-7a9c-4262-9d54-755e4074fc48` |
| Monthly BSUOS Forecast Summary August 15 Percent | CSV | upload | `9e50b846-5b22-4c18-b5f5-8d61b33eff0e` |
| Monthly BSUOS Forecast Summary August 5 Percent | CSV | upload | `cf75f2e2-6dc3-41f5-bdb5-1d794f87647f` |
| Monthly BSUOS Forecast Summary February 2021 | CSV | upload | `11af9f47-0adf-475e-8bc4-0265db7903b4` |
| Monthly BSUOS Forecast Summary March 2021 | CSV | upload | `3c0ee750-c753-4bf3-8de2-aa93924499b6` |
| Monthly BSUOS Forecast Summary September 10 Percent | CSV | upload | `7e6be8b2-1528-4b68-b444-7cd1c1fdd557` |
| Monthly BSUOS Forecast Summary September 15 Percent | CSV | upload | `f6a319e9-5423-4edb-bbae-48e61088b36a` |
| Monthly BSUOS Forecast Summary September 5 percent | CSV | upload | `a1afe42b-1983-48d0-9b2d-0902a2579905` |
| Monthly BSUOS Summary August 10 Percent | CSV | upload | `67ab6ea8-095e-45ee-97b1-f5b554e597fb` |
| Monthly BSUOS Summary August 15 Percent | CSV | upload | `aeac49ab-98b9-4d7a-8f0d-7a261c5c5516` |
| Monthly BSUOS Summary August 5 Percent | CSV | upload | `ae1f2394-06dc-42c8-b216-1286b637bff5` |
| Monthly BSUOS Summary February 2021 | CSV | upload | `e980e80c-4558-4cc1-9da7-eefd9b8dd37e` |
| Monthly BSUOS Summary July 10 Percent | CSV | upload | `f97eac2c-73a7-4485-ae87-69a311cf91aa` |
| Monthly BSUOS Summary July 15 Percent | CSV | upload | `74729416-1abd-4223-9cb0-b3bea0021cee` |
| Monthly BSUOS Summary July 5 Percent | CSV | upload | `20f17f8a-0fca-4bff-8b5f-0f854dd0130e` |
| Monthly BSUOS Summary March 2021 | CSV | upload | `465b2fa8-d770-4584-aa67-e3ae9a9f70c1` |
| Monthly BSUOS Summary September 10 Percent | CSV | upload | `81703773-4ed5-40fe-b737-e3c601be1b92` |
| Monthly BSUOS Summary September 15 Percent | CSV | upload | `87b7525c-a434-4162-9e5c-658e12b01f61` |
| Monthly BSUOS Summary September 5 Percent | CSV | upload | `f9ccf645-4721-4516-9a07-60326618da95` |
| Monthly BSUoS Actual Summary Apr_20 | CSV | upload | `81ea4cf9-c067-492a-9892-82161c8c1672` |
| Monthly BSUoS Actual Summary April 2021 | CSV | upload | `bfa78e9a-5eee-4db3-83c0-66e504d875d9` |
| Monthly BSUoS Actual Summary August 2021 | CSV | upload | `babaa281-9c46-4337-931c-4962627da9ca` |
| Monthly BSUoS Actual Summary August_20 | CSV | upload | `e5e68d42-76cc-417a-8dbc-00d7e7346f93` |
| Monthly BSUoS Actual Summary Dec_20 | CSV | upload | `e9dad655-0278-494b-8097-1b6e6a78dbe8` |
| Monthly BSUoS Actual Summary December 2021 | CSV | upload | `1f8b0d9a-a98b-4cf4-9496-16a5c9db551f` |
| Monthly BSUoS Actual Summary January 2021 | CSV | upload | `923a86f2-cf7c-4228-a0f1-108488a621a8` |
| Monthly BSUoS Actual Summary Jul_20 | CSV | upload | `83809a38-17f3-4a79-98e3-55a080d205fc` |
| Monthly BSUoS Actual Summary July 2021 | CSV | upload | `48839508-12a8-4415-a74c-473f0b8e3506` |
| Monthly BSUoS Actual Summary Jun_20 | CSV | upload | `a3bbe4ae-7821-4d17-b129-a9b95d9ddf3b` |
| Monthly BSUoS Actual Summary June 2021 | CSV | upload | `d4f04c3e-b843-4d30-9069-184bcfe84451` |
| Monthly BSUoS Actual Summary Mar_20 | CSV | upload | `fdd43811-b1ff-490e-8ad2-98d67822931e` |
| Monthly BSUoS Actual Summary May 2021 | CSV | upload | `97802999-2084-4f13-be5e-8347acbec46b` |
| Monthly BSUoS Actual Summary May_20 | CSV | upload | `9487b368-b20a-4b2b-b282-0b1b42bfb79a` |
| Monthly BSUoS Actual Summary Nov_20 | CSV | upload | `42f21a68-6700-4585-b63b-bc0080a99d2b` |
| Monthly BSUoS Actual Summary November 2021 | CSV | upload | `172ca899-6145-4ffa-a29e-3c6b6656a90f` |
| Monthly BSUoS Actual Summary Oct_20 | CSV | upload | `a8cc74ca-c813-45f1-b37b-1e567208da70` |
| Monthly BSUoS Actual Summary October 2021 | CSV | upload | `53926e09-2807-455f-9092-f3a047a046b1` |
| Monthly BSUoS Actual Summary Sep_20 | CSV | upload | `808a34e1-a3ea-4638-8b1b-df757bd65b14` |
| Monthly BSUoS Actual Summary September 2021 | CSV | upload | `f0ff35d6-cdf1-40f1-a41c-b2dd38a61b8a` |
| Monthly BSUoS Forecast Summary - April 2026 | CSV | upload | `d8231d25-e7df-4292-a71d-53f8a2b6ed26` |
| Monthly BSUoS Forecast Summary - August 2026 | CSV | upload | `ebd99538-2dcf-4ab1-9791-099690200658` |
| Monthly BSUoS Forecast Summary - July 2026 | CSV | upload | `108aeff1-ed0c-42cb-a2fa-51940395fe5f` |
| Monthly BSUoS Forecast Summary - June 2026 | CSV | upload | `ce1cc6a0-8a7e-41ae-9a97-097932c5a474` |
| Monthly BSUoS Forecast Summary - March 2026 | CSV | upload | `fb8ec037-d2c6-4b39-936e-1611a4ea4994` |
| Monthly BSUoS Forecast Summary - May 2026 | CSV | upload | `5588977f-0ec8-4a32-a0b0-5a0615780e06` |
| Monthly BSUoS Forecast Summary - October 2026 | CSV | upload | `b458c4e5-ab80-43e5-907e-6c7069350390` |
| Monthly BSUoS Forecast Summary - September 2026 | CSV | upload | `5e835054-6f5b-433c-a063-6a573107d561` |
| Monthly BSUoS Forecast Summary Apr_20 | CSV | upload | `46d81790-4b05-404b-b12b-6262bbb55cd2` |
| Monthly BSUoS Forecast Summary April 2021 | CSV | upload | `772a145f-78d9-4049-aa27-dafb2bef2f68` |
| Monthly BSUoS Forecast Summary April 2022 | CSV | upload | `066e26cf-acea-4925-bbfd-b2576cc43b59` |
| Monthly BSUoS Forecast Summary April 2023 | CSV | upload | `ff6bd12f-7c0b-4d0a-a477-5c8113ffa14d` |
| Monthly BSUoS Forecast Summary April 2024 | CSV | upload | `0bef1780-082d-46ec-90af-62b3d0586061` |
| Monthly BSUoS Forecast Summary April 2025 | CSV | upload | `c3b4c80c-ea63-4b72-854d-1260833aaf25` |
| Monthly BSUoS Forecast Summary August 2021 | CSV | upload | `c3e4060e-40d9-4b7a-8de1-7cfd5930649a` |
| Monthly BSUoS Forecast Summary August 2022 | CSV | upload | `af497533-959e-40d3-a4cf-a977e41d19f1` |
| Monthly BSUoS Forecast Summary August 2023 | CSV | upload | `60ee18d3-b999-4413-aac5-82a30d2a982c` |
| Monthly BSUoS Forecast Summary August 2024 | CSV | upload | `2d5f0be1-2aab-4ab7-af28-c67a2f38db6b` |
| Monthly BSUoS Forecast Summary August 2025 | CSV | upload | `48a2cf4b-e3c8-4317-b329-a55007f4595f` |
| Monthly BSUoS Forecast Summary Dec_20 | CSV | upload | `35cceee7-cea0-4e3d-95d3-e9937106d6a9` |
| Monthly BSUoS Forecast Summary December 2021 | CSV | upload | `e76b08ff-bc9a-422e-88e0-e7e325ec7d82` |
| Monthly BSUoS Forecast Summary December 2022 | CSV | upload | `cac31462-bcc6-41e2-ae4d-44eb817e70fd` |
| Monthly BSUoS Forecast Summary December 2023 | CSV | upload | `949a0088-5f0b-432a-add6-36cda83a4532` |
| Monthly BSUoS Forecast Summary December 2024 | CSV | upload | `fd51885f-62f0-4c99-8f9b-c8a3ad3ef7df` |
| Monthly BSUoS Forecast Summary December 2025 | CSV | upload | `7d58f22a-5540-4558-b21b-b1fbb457a283` |
| Monthly BSUoS Forecast Summary February 2022 | CSV | upload | `98fea024-d154-4f4b-840e-5e84e5c649ff` |
| Monthly BSUoS Forecast Summary February 2023 | CSV | upload | `37f2da36-e296-4120-a862-cd5c6b9e2a3f` |
| Monthly BSUoS Forecast Summary February 2024 | CSV | upload | `963cf73a-138e-4521-986b-12079f45b78d` |
| Monthly BSUoS Forecast Summary February 2025 | CSV | upload | `8c8f2e4c-b27d-4780-9c12-a5f338072e64` |
| Monthly BSUoS Forecast Summary February 2026 | CSV | upload | `765f46e9-516a-4bc2-92b2-974dfc3913b0` |
| Monthly BSUoS Forecast Summary January 2021 | CSV | upload | `d56a5b59-2a59-4fb4-be01-71f1de01e6bd` |
| Monthly BSUoS Forecast Summary January 2023 | CSV | upload | `e720d5c4-d462-4d32-a784-9ad2f2e26533` |
| Monthly BSUoS Forecast Summary January 2024 | CSV | upload | `f19c9722-7f63-48e5-844e-6f2c1d20f607` |
| Monthly BSUoS Forecast Summary January 2025 | CSV | upload | `f79b4be1-c292-4eb3-b185-a0790c62ebc3` |
| Monthly BSUoS Forecast Summary January 2026 | CSV | upload | `48bca1ee-5c8c-44f1-8f6e-be4a84df092b` |
| Monthly BSUoS Forecast Summary July 10 Percent | CSV | upload | `5e1d066b-8ddb-4f79-a9da-ebee68ceec73` |
| Monthly BSUoS Forecast Summary July 15 Percent | CSV | upload | `0c413c78-c9cd-4f73-8157-7256745147ee` |
| Monthly BSUoS Forecast Summary July 2021 | CSV | upload | `46fe0789-9da3-4fb8-9788-22632cb325fb` |
| Monthly BSUoS Forecast Summary July 2022 | CSV | upload | `9fe9953c-8c4a-4b9a-8548-cfa0c16590a8` |
| Monthly BSUoS Forecast Summary July 2023 | CSV | upload | `3ed31178-bd64-41ce-8665-85b77db7aaaf` |
| Monthly BSUoS Forecast Summary July 2024 | CSV | upload | `7d6bb550-ba4d-461f-82d0-02002461d7f3` |
| Monthly BSUoS Forecast Summary July 2025 | CSV | upload | `bb23c52b-f379-4e4a-b249-29e556ab2d61` |
| Monthly BSUoS Forecast Summary July 5 Percent | CSV | upload | `eaa5e134-5523-47a4-b91d-757b62b8378c` |
| Monthly BSUoS Forecast Summary June 10 Percent | CSV | upload | `568234c3-43ad-418e-aace-64c29240dd02` |
| Monthly BSUoS Forecast Summary June 15 Percent | CSV | upload | `ed75b74b-9b81-4fd2-8f87-461fa743fafc` |
| Monthly BSUoS Forecast Summary June 2021 | CSV | upload | `f8c698d9-244c-4eaf-9599-4f466224afac` |
| Monthly BSUoS Forecast Summary June 2022 | CSV | upload | `aef8c119-d9e3-496a-8185-e1be35f6f71b` |
| Monthly BSUoS Forecast Summary June 2023 | CSV | upload | `df1959c4-144f-4dd7-a89b-686a5ad404d0` |
| Monthly BSUoS Forecast Summary June 2024 | CSV | upload | `5ac846e5-d862-4994-83a3-0fd39b152ef5` |
| Monthly BSUoS Forecast Summary June 2025 | CSV | upload | `054982aa-f45f-4452-bb9e-5dc32cef84b5` |
| Monthly BSUoS Forecast Summary June 5 Percent | CSV | upload | `9b840832-2438-472e-906e-45edbb311e1b` |
| Monthly BSUoS Forecast Summary Mar_20 | CSV | upload | `ef004890-679a-4d28-ac00-427ff6e7260d` |
| Monthly BSUoS Forecast Summary March 2022 | CSV | upload | `db352475-1dc7-462a-9f57-cfcf269fa5f2` |
| Monthly BSUoS Forecast Summary March 2023 | CSV | upload | `70f93287-3067-475a-a240-ccb7af2a7b10` |
| Monthly BSUoS Forecast Summary March 2024 | CSV | upload | `9120ae56-f4b5-4512-baaa-e20f8b31a014` |
| Monthly BSUoS Forecast Summary March 2025 | CSV | upload | `495879f8-4605-4ade-b4d1-7b1d37a163fa` |
| Monthly BSUoS Forecast Summary May 2021 | CSV | upload | `e448a3bc-fd28-4fd1-a36b-2abea6c37ed2` |
| Monthly BSUoS Forecast Summary May 2022 | CSV | upload | `69bbddf1-2299-4908-b6d5-979cec86130e` |
| Monthly BSUoS Forecast Summary May 2023 | CSV | upload | `578b493e-db5c-41e3-8b52-f91c5f80389c` |
| Monthly BSUoS Forecast Summary May 2024 | CSV | upload | `ebdd84ac-02cb-4552-a427-9b0dc56f5482` |
| Monthly BSUoS Forecast Summary May 2025 | CSV | upload | `2177f79e-afb3-4bb2-92f3-ce771bc96a25` |
| Monthly BSUoS Forecast Summary May_20 | CSV | upload | `f5c20630-1330-4a33-99bb-8b33a28d5cbb` |
| Monthly BSUoS Forecast Summary Nov_20 | CSV | upload | `b41ca68b-9248-4442-a158-664e13e6f9c8` |
| Monthly BSUoS Forecast Summary November 2021 | CSV | upload | `5b443736-832a-4412-be9c-0288e3ddb199` |
| Monthly BSUoS Forecast Summary November 2022 | CSV | upload | `55216f27-d445-494d-b9d8-51af448349db` |
| Monthly BSUoS Forecast Summary November 2023 | CSV | upload | `50cede2c-b090-4e6e-b103-67e79cfc6264` |
| Monthly BSUoS Forecast Summary November 2024 | CSV | upload | `d3f9a301-bba4-4f23-a11c-d40681c2fe04` |
| Monthly BSUoS Forecast Summary November 2025 | CSV | upload | `77c75ff4-bc95-4e0d-bd4a-7e8bb2282fd0` |
| Monthly BSUoS Forecast Summary Oct_20 | CSV | upload | `bdd9b33f-7055-46b2-af73-2fd958c39288` |
| Monthly BSUoS Forecast Summary October 2021 | CSV | upload | `84ee9c82-928a-44ff-a932-ca56cf8b14ec` |
| Monthly BSUoS Forecast Summary October 2022 | CSV | upload | `8ddd61ed-1003-479a-bc78-6dfe0f91da6b` |
| Monthly BSUoS Forecast Summary October 2023 | CSV | upload | `2fa45fb3-583a-4eec-b247-259b827e1a73` |
| Monthly BSUoS Forecast Summary October 2024 | CSV | upload | `55fd644c-e984-4ecd-9777-77396ce5192b` |
| Monthly BSUoS Forecast Summary October 2025 | CSV | upload | `a9a91f3c-55d4-4c0b-86d7-81e97d71a3c9` |
| Monthly BSUoS Forecast Summary September 2021 | CSV | upload | `c7040e92-95ca-41d5-b6a2-3c29b58260c3` |
| Monthly BSUoS Forecast Summary September 2022 | CSV | upload | `85f033df-c21b-419a-8e08-15c8efecd344` |
| Monthly BSUoS Forecast Summary September 2022 with Winter Contingency Cost | CSV | upload | `839c1a80-ce74-4cd4-b634-197a54974b29` |
| Monthly BSUoS Forecast Summary September 2023 | CSV | upload | `e1d028db-abe3-43d1-a531-f5d9073fb10c` |
| Monthly BSUoS Forecast Summary September 2024 | CSV | upload | `2267c6a0-d471-4ccf-bd5d-a6866f7c4297` |
| Monthly BSUoS Forecast Summary September 2025 | CSV | upload | `dd4d9981-120c-4344-9e45-715ddf71f887` |
| Monthly BSUoS Summary Apr_20 | CSV | upload | `f2f25e35-5c3e-4c50-b59f-620c4fcbebee` |
| Monthly BSUoS Summary April 2021 | CSV | upload | `f5e851c8-aa29-4741-b03c-e06ace717166` |
| Monthly BSUoS Summary August 2021 | CSV | upload | `bd86885b-3dc4-45f7-975a-5a4a76fb10c6` |
| Monthly BSUoS Summary Dec_20 | CSV | upload | `a4a37840-3591-4f37-891d-8051dd03b067` |
| Monthly BSUoS Summary December 2021 | CSV | upload | `b9fbb769-bb54-4f00-95f1-888421fcbdbe` |
| Monthly BSUoS Summary January 2021 | CSV | upload | `3defb516-f85f-40c6-a4ec-a15d1fe97079` |
| Monthly BSUoS Summary July 2021 | CSV | upload | `c73f7b87-d525-4690-9d7f-9d0e2024908a` |
| Monthly BSUoS Summary June 10 Percent | CSV | upload | `5bb53829-1358-4db0-9408-64ba83e97631` |
| Monthly BSUoS Summary June 15 Percent | CSV | upload | `7a475feb-a8af-41e1-98bc-9070c02d3b60` |
| Monthly BSUoS Summary June 2021 | CSV | upload | `8b8cfa4a-e445-4e94-937b-dbfb1c09dcee` |
| Monthly BSUoS Summary June 5 Percent | CSV | upload | `253e5f12-a555-4792-a613-2bafa657e4fc` |
| Monthly BSUoS Summary Mar_20 | CSV | upload | `6b20199f-8f95-4409-b26e-d89cbf5255da` |
| Monthly BSUoS Summary May 2021 | CSV | upload | `37c01b9f-e7d9-4bbb-9f00-55e02341a3e7` |
| Monthly BSUoS Summary May_20 | CSV | upload | `c6edf882-b617-42d4-956e-bdf76eab837c` |
| Monthly BSUoS Summary Nov_20 | CSV | upload | `84f6a379-8725-40a4-b731-afee0d63ee4e` |
| Monthly BSUoS Summary November 2021 | CSV | upload | `78d04abd-8464-46a0-a5fa-11995444c9a0` |
| Monthly BSUoS Summary Oct_20 | CSV | upload | `21220a71-e3a3-43e5-a6c1-635bc34c1ba1` |
| Monthly BSUoS Summary October 2021 | CSV | upload | `d208431e-9ef5-435b-a8e9-fe5b4b486a15` |
| Monthly BSUoS Summary September 2021 | CSV | upload | `65ed0d3d-12bc-4650-9562-44f53345c672` |

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| BSUoS Forecasting Update Jan 2022 - Communications Pack | PDF | upload | `d0be7040-87f7-4002-bc3e-5fa58e5e2a99` |

The one DOC resource is a communications pack from the vendor ("An update on changes to BSUoS
forecasting"). It carries no gridflow record and is kept as a document. Download:
[bsuos-forecasting-update-26jan2022-.pdf](https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/d0be7040-87f7-4002-bc3e-5fa58e5e2a99/download/bsuos-forecasting-update-26jan2022-.pdf)
(409,938 bytes in the 2026-10-08 capture; CKAN `last_modified` 2022-01-26T11:02:55.535267).
The 15 `Accuracy` sheets inside the held workbook archive are also DOC; they are listed under
HOLD below.

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| BSUoS_Report_Jan 19 - Mar 20 | XLSX | upload | `e69ab0c0-34bc-4fad-89a9-980739332642` | TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Forecast Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Actual Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Data_store | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Error Stats | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Data | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_april_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_dec_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_dec_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_dec_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_dec_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_dec_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_dec_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_dec_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_feb_20_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_feb_20_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_feb_20_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_feb_20_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_feb_20_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_feb_20_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_feb_20_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Forecast Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Actual Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Data_store | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Error Stats | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Data | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::ROCOF | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_february_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_jan_20_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_jan_20_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_jan_20_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_jan_20_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_jan_20_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_jan_20_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_jan_20_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Forecast Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Actual Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Data_store | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Error Stats | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Data | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_january_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_mar_20_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_mar_20_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_mar_20_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_mar_20_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_mar_20_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_mar_20_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_mar_20_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Forecast Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Actual Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Data_store | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Error Stats | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Data | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_may_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_nov_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_nov_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_nov_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_nov_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_nov_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_nov_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_nov_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_oct_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_oct_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_oct_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_oct_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_oct_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_oct_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/bsuos_report_oct_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Forecast Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Actual Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Data_store | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Error Stats | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Data | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_aug_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Forecast Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Actual Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Data_store | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Error Stats | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Data | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jul_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Forecast Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Actual Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Data_store | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Error Stats | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Data | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_jun_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Forecast Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Actual Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Data_store | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Error Stats | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Data | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_march_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Accuracy | — | — | DOC | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Forecast Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Actual Data For Import | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Data_store | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Error Stats | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Data | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Monthly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Weekly Summary Actual | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::Monthly Summary Forecast | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |
| ↳ BSUoS Report Jan 19 - Mar 20/busos_report_sep_19_data.xlsx::All Monthly | — | — | HOLD: TODO: WORKBOOK-CHILD-RECORDS — 15 workbooks / 151 sheets; table bounds, identifiers, units, time and issue semantics unsettled per child (FACTS BAL-2a-3); no overlap establishes COVERED. (BAL-2) | — |

The HOLD resource is a **ZIP archive served under an XLSX label**: `BSUoS_Report_Jan 19 - Mar 20`,
file [bsuos-report-jan-19-mar-20.zip](https://api.neso.energy/dataset/c0376ed7-3205-4fe2-9496-28496f1f287a/resource/e69ab0c0-34bc-4fad-89a9-980739332642/download/bsuos-report-jan-19-mar-20.zip)
(11,384,013 bytes in the 2026-10-08 capture; CKAN `last_modified` 2021-01-07T12:14:44.359194).
The vendor describes it as BSUoS outturn and a one-month-ahead forecast, with BSUoS volatility
and forecast accuracy, for January 2019 to March 2020. Research opened it and found **15
workbooks with 151 sheets**. The registry lists every sheet as a child: the 15 `Accuracy`
sheets are DOC and every other child is HOLD. The sheet layouts are title blocks, side-by-side
blocks, month-column matrices and one edition-column store, so no sheet is a faithful table yet.
Four of them (`Monthly Summary Actual`, `Weekly Summary Actual`, `Monthly Summary Forecast`,
`All Monthly`) are candidate tables. The hold reason is `TODO: WORKBOOK-CHILD-RECORDS`: table
bounds, identifiers, units, time semantics and issue semantics are unsettled for each child.
Target months in the workbook overlap the CSV families, but the shared named values did not
agree exactly in any compared pair. That shows overlap, not coverage, and **no sheet is
COVERED**. (FACTS BAL-2a-3.)

## Families

### `bsuos_monthly_forecast_actual_sum`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no
- ingest-only: no silver yet

**What it is.** Monthly BSUoS **actual (outturn) summaries**, one resource per month from
March 2020 to December 2021 (22 resources; Mar_20 to Dec_20 and January to December 2021). Each
body is 12 rows. This is historical outturn, not a forward forecast, although it sits in this
package.

**State.** Bronze only; **no record** (RULINGS 667). None of the 22 bodies is valid UTF-8, and
the vendor declares no encoding, so there is no faithful decode. `TODO: verify` the vendor's
encoding, or obtain an explicit adjudication, before a record is possible.

**Header epochs (FACTS BAL-2a-1).** Two: 14 resources (168 rows) with the service-cost columns
plus three trailing columns with empty names; 8 resources (96 rows, May to December 2021) in
which one of those is named `CMP345/350 Deferred Costs`. The first empty-named column is
numeric in all 264 rows and has no vendor name or unit, so it can be neither dropped nor read as
a charge. `TODO: verify` its identity. `Month` is unique within each body.

**Units (vendor dictionary, FACTS g4).** The dictionary labels the bare service-cost, Profit and
ALoMCP columns as £ (not £m). The internal-cost header says £m but the dictionary says £, so
the scale is unresolved (`TODO: verify` with an edition-specific vendor statement). The bare
`CMP345/350 Deferred Costs` has no declared unit. `Demand` is described as a volume but labelled
£ (`TODO: ACTUAL-DEMAND-UNIT`).

**Clocks.** Vintage `ckan_last_modified` (upload resources). Event time: `none`; `Month` would
be kept as the vendor's label, and the month boundary and clock are unestablished
(`TODO: BSUOS-MONTH-CLOCK`).

### `bsuos_monthly_forecast_fc_summary`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no

**What it is.** The main forecast: one CSV per monthly **edition**, each giving a 24-month
cost forecast, one row per target month. This family is **held** (see Holds and the prose after
the tables). It has 75 resources. Silver holds **53 editions** (February 2022 to October 2026,
with no May 2022 and no April to June 2023), **1,272 rows, 24 per edition**. The other 22
resources failed to decode as UTF-8 and are adjudicated as failed captures (RULINGS 667): the 18
oldest (March 2020 to December 2021, including the misplaced November 2020 file described below),
May 2022, and April, May and June 2023.

The eight header epochs below map to editions as follows (the counts sum to 53):

| Epoch | Editions | Count |
|---|---|---:|
| 1 | February 2022, April 2022 | 2 |
| 2 | March 2022 | 1 |
| 3 | June to September 2022 | 4 |
| 4 | October 2022 to March 2023 | 6 |
| 5 | July 2023 | 1 |
| 6 | August 2023 to January 2024 | 6 |
| 7 | February to July 2024 | 6 |
| 8 | August 2024 to October 2026 | 27 |

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Month | `month_vendor` | string | — | no | — | — |
| Energy_Imbalance_£m | `energy_imbalance_gbp_m` | float64 | — | yes | — | £m |
| Positive_Reserve_£m | `positive_reserve_gbp_m` | float64 | — | yes | — | £m |
| Negative_Reserve_£m | `negative_reserve_gbp_m` | float64 | — | yes | — | £m |
| Frequency_Control_£m | `frequency_control_gbp_m` | float64 | — | yes | — | £m |
| Other_£m | `other_gbp_m` | float64 | — | yes | — | £m |
| Constraints_£m | `constraints_gbp_m` | float64 | — | yes | — | £m |
| Restoration_£m | `restoration_gbp_m` | float64 | — | yes | — | £m |
| Balancing Costs (Central) £m | `balancing_costs_central_gbp_m` | float64 | — | yes | — | £m |
| Estimated Internal BSUoS & ESO Incentive £m | `estimated_internal_bsuos_eso_incentive_gbp_m` | float64 | — | yes | — | £m |
| BSUoS Cost Recovery £m | `bsuos_cost_recovery_gbp_m` | float64 | — | yes | — | — |
| ALoMCP £m | `alomcp_gbp_m` | float64 | — | yes | — | — |
| CMP345/350 Deferred Costs £m | `cmp345_350_deferred_costs_gbp_m` | float64 | — | yes | — | — |
| CMP381 Deferred Costs £m | `cmp381_deferred_costs_gbp_m` | float64 | — | yes | — | — |
| Estimated BSUoS Volume (TWh) | `estimated_bsuos_volume_twh` | float64 | — | yes | — | TWh |
|  | `unnamed_16` | string | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Month | `month_vendor` | string | — | no | — | — |
| Energy_Imbalance_£m | `energy_imbalance_gbp_m` | float64 | — | yes | — | £m |
| Positive_Reserve_£m | `positive_reserve_gbp_m` | float64 | — | yes | — | £m |
| Negative_Reserve_£m | `negative_reserve_gbp_m` | float64 | — | yes | — | £m |
| Frequency_Control_£m | `frequency_control_gbp_m` | float64 | — | yes | — | £m |
| Other_£m | `other_gbp_m` | float64 | — | yes | — | £m |
| Constraints_£m | `constraints_gbp_m` | float64 | — | yes | — | £m |
| Balancing Costs (Central) £m | `balancing_costs_central_gbp_m` | float64 | — | yes | — | £m |
| Estimated Internal BSUoS & ESO Incentive £m | `estimated_internal_bsuos_eso_incentive_gbp_m` | float64 | — | yes | — | £m |
| BSUoS Cost Recovery £m | `bsuos_cost_recovery_gbp_m` | float64 | — | yes | — | — |
| ALoMCP £m | `alomcp_gbp_m` | float64 | — | yes | — | — |
| CMP345/350 Deferred Costs £m | `cmp345_350_deferred_costs_gbp_m` | float64 | — | yes | — | — |
| CMP381 Deferred Costs £m | `cmp381_deferred_costs_gbp_m` | float64 | — | yes | — | — |
| Estimated BSUoS Volume (TWh) | `estimated_bsuos_volume_twh` | float64 | — | yes | — | TWh |
|  | `unnamed_15` | string | — | yes | — | — |

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Month | `month_vendor` | string | — | no | — | — |
| Energy_Imbalance_£m | `energy_imbalance_gbp_m` | float64 | — | yes | — | £m |
| Positive_Reserve_£m | `positive_reserve_gbp_m` | float64 | — | yes | — | £m |
| Negative_Reserve_£m | `negative_reserve_gbp_m` | float64 | — | yes | — | £m |
| Frequency_Control_£m | `frequency_control_gbp_m` | float64 | — | yes | — | £m |
| Other_£m | `other_gbp_m` | float64 | — | yes | — | £m |
| Constraints_£m | `constraints_gbp_m` | float64 | — | yes | — | £m |
| Restoration_£m | `restoration_gbp_m` | float64 | — | yes | — | £m |
| Balancing Costs (Central) £m | `balancing_costs_central_gbp_m` | float64 | — | yes | — | £m |
| Estimated Internal BSUoS & ESO Incentive £m | `estimated_internal_bsuos_eso_incentive_gbp_m` | float64 | — | yes | — | £m |
| ALoMCP £m | `alomcp_gbp_m` | float64 | — | yes | — | — |
| CMP381 Deferred Costs £m | `cmp381_deferred_costs_gbp_m` | float64 | — | yes | — | — |
| Estimated BSUoS Volume (TWh) | `estimated_bsuos_volume_twh` | float64 | — | yes | — | TWh |

Schema, epoch 4:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Month | `month_vendor` | string | — | no | — | — |
| Energy_Imbalance_£m | `energy_imbalance_gbp_m` | float64 | — | yes | — | £m |
| Positive_Reserve_£m | `positive_reserve_gbp_m` | float64 | — | yes | — | £m |
| Negative_Reserve_£m | `negative_reserve_gbp_m` | float64 | — | yes | — | £m |
| Frequency_Control_£m | `frequency_control_gbp_m` | float64 | — | yes | — | £m |
| Other_£m | `other_gbp_m` | float64 | — | yes | — | £m |
| Constraints_£m | `constraints_gbp_m` | float64 | — | yes | — | £m |
| Restoration_£m | `restoration_gbp_m` | float64 | — | yes | — | £m |
| Balancing Costs (Central) £m | `balancing_costs_central_gbp_m` | float64 | — | yes | — | £m |
| Estimated Internal BSUoS & ESO Incentive £m | `estimated_internal_bsuos_eso_incentive_gbp_m` | float64 | — | yes | — | £m |
| ALoMCP £m | `alomcp_gbp_m` | float64 | — | yes | — | — |
| CMP381 Deferred Costs £m | `cmp381_deferred_costs_gbp_m` | float64 | — | yes | — | — |
| Winter Contingency Cost (Central) £m | `winter_contingency_cost_central_gbp_m` | float64 | — | yes | — | — |
| Estimated BSUoS Volume (TWh) | `estimated_bsuos_volume_twh` | float64 | — | yes | — | TWh |

Schema, epoch 5:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Month | `month_vendor` | string | — | no | — | — |
| Energy_Imbalance_£m | `energy_imbalance_gbp_m` | float64 | — | yes | — | £m |
| Positive_Reserve_£m | `positive_reserve_gbp_m` | float64 | — | yes | — | £m |
| Negative_Reserve_£m | `negative_reserve_gbp_m` | float64 | — | yes | — | £m |
| Frequency_Control_£m | `frequency_control_gbp_m` | float64 | — | yes | — | £m |
| Constraints_£m | `constraints_gbp_m` | float64 | — | yes | — | £m |
| Other_£m | `other_gbp_m` | float64 | — | yes | — | £m |
| Restoration_£m | `restoration_gbp_m` | float64 | — | yes | — | £m |
| Balancing Costs (Central) £m | `balancing_costs_central_gbp_m` | float64 | — | yes | — | £m |
| Estimated Internal BSUoS & ESO Incentive £m | `estimated_internal_bsuos_eso_incentive_gbp_m` | float64 | — | yes | — | £m |
| ALoMCP £m | `alomcp_gbp_m` | float64 | — | yes | — | — |
| CMP381 Deferred Costs £m | `cmp381_deferred_costs_gbp_m` | float64 | — | yes | — | — |
| Winter Contingency Cost (Central) £m | `winter_contingency_cost_central_gbp_m` | float64 | — | yes | — | — |
| Winter Security of Supply Cost (£m) | `winter_security_of_supply_cost_gbp_m` | float64 | — | yes | — | £m |
| Volume | `volume` | float64 | — | yes | — | — |

Schema, epoch 6:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Month | `month_vendor` | string | — | no | — | — |
| Energy_Imbalance_£m | `energy_imbalance_gbp_m` | float64 | — | yes | — | £m |
| Positive_Reserve_£m | `positive_reserve_gbp_m` | float64 | — | yes | — | £m |
| Negative_Reserve_£m | `negative_reserve_gbp_m` | float64 | — | yes | — | £m |
| Frequency_Control_£m | `frequency_control_gbp_m` | float64 | — | yes | — | £m |
| Constraints_£m | `constraints_gbp_m` | float64 | — | yes | — | £m |
| Other_£m | `other_gbp_m` | float64 | — | yes | — | £m |
| Restoration_£m | `restoration_gbp_m` | float64 | — | yes | — | £m |
| Balancing Costs (Central) £m | `balancing_costs_central_gbp_m` | float64 | — | yes | — | £m |
| Estimated Internal BSUoS & ESO Incentive £m | `estimated_internal_bsuos_eso_incentive_gbp_m` | float64 | — | yes | — | £m |
| Winter Security of Supply Cost (£m) | `winter_security_of_supply_cost_gbp_m` | float64 | — | yes | — | £m |
| Estimated BSUoS Volume (TWh) | `estimated_bsuos_volume_twh` | float64 | — | yes | — | TWh |

Schema, epoch 7:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Month | `month_vendor` | string | — | no | — | — |
| Energy_Imbalance_£m | `energy_imbalance_gbp_m` | float64 | — | yes | — | £m |
| Positive_Reserve_£m | `positive_reserve_gbp_m` | float64 | — | yes | — | £m |
| Negative_Reserve_£m | `negative_reserve_gbp_m` | float64 | — | yes | — | £m |
| Frequency_Control_£m | `frequency_control_gbp_m` | float64 | — | yes | — | £m |
| Constraints_£m | `constraints_gbp_m` | float64 | — | yes | — | £m |
| Other_£m | `other_gbp_m` | float64 | — | yes | — | £m |
| Restoration_£m | `restoration_gbp_m` | float64 | — | yes | — | £m |
| Balancing Costs (Central) £m | `balancing_costs_central_gbp_m` | float64 | — | yes | — | £m |
| Estimated Internal BSUoS & ESO Incentive £m | `estimated_internal_bsuos_eso_incentive_gbp_m` | float64 | — | yes | — | £m |
| Winter Security of Supply Cost (£m) | `winter_security_of_supply_cost_gbp_m` | float64 | — | yes | — | £m |
| 21/22 Under-Recovered Costs (£m) | `under_recovered_costs_21_22_gbp_m` | float64 | — | yes | — | £m |
| Estimated BSUoS Volume (TWh) | `estimated_bsuos_volume_twh` | float64 | — | yes | — | TWh |

Schema, epoch 8:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Month | `month_vendor` | string | — | no | — | — |
| Energy_Imbalance_£m | `energy_imbalance_gbp_m` | float64 | — | yes | — | £m |
| Positive_Reserve_£m | `positive_reserve_gbp_m` | float64 | — | yes | — | £m |
| Negative_Reserve_£m | `negative_reserve_gbp_m` | float64 | — | yes | — | £m |
| Frequency_Control_£m | `frequency_control_gbp_m` | float64 | — | yes | — | £m |
| Constraints_£m | `constraints_gbp_m` | float64 | — | yes | — | £m |
| Other_£m | `other_gbp_m` | float64 | — | yes | — | £m |
| Restoration_£m | `restoration_gbp_m` | float64 | — | yes | — | £m |
| Balancing Costs (Central) £m | `balancing_costs_central_gbp_m` | float64 | — | yes | — | £m |
| Estimated Internal BSUoS & ESO Incentive £m | `estimated_internal_bsuos_eso_incentive_gbp_m` | float64 | — | yes | — | £m |
| Winter Security of Supply Cost (£m) | `winter_security_of_supply_cost_gbp_m` | float64 | — | yes | — | £m |
| 21/22 Under-Recovered Costs (£m) | `under_recovered_costs_21_22_gbp_m` | float64 | — | yes | — | £m |
| CMP398/412 Claim Costs (£m) | `cmp398_412_claim_costs_gbp_m` | float64 | — | yes | — | £m |
| Interest Repayment (£m) | `interest_repayment_gbp_m` | float64 | — | yes | — | £m |
| Additional NESO Framework Costs (£m) | `additional_neso_framework_costs` | float64 | — | yes | — | TWh |
| Estimated BSUoS Volume (TWh) | `estimated_bsuos_volume_twh` | float64 | — | yes | — | TWh |

- Entity key: `resource_id`, `edition`, `month_vendor`
- Latest: `whole_capture` per `resource_id`
- Edition: `bsuos-forecast-february-2022-csv.csv` → 202202; `bsuos-forecast-march-2022-csv.csv` → 202203; `bsuos-forecast-april-2022_2.csv` → 202204; `bsuos-forecast-june-2022.csv` → 202206; `bsuos-forecast-july-2022.csv` → 202207; `bsuos-forecast-august-2022.csv` → 202208; `bsuos-forecast-september-2022.csv` → 202209; `bsuos-forecast-october-2022.csv` → 202210; `bsuos-forecast-november-2022.csv` → 202211; `bsuos-forecast-december-2022.csv` → 202212; `bsuos-forecast-jan23.csv` → 202301; `bsuos-forecast-february-2023.csv` → 202302; `bsuos-forecast-march-2023.csv` → 202303; `bsuos-forecast-july-2023.csv` → 202307; `bsuos-forecast-aug-2023.csv` → 202308; `bsuos-forecast-sep-2023.csv` → 202309; `bsuos-forecast-oct-2023.csv` → 202310; `bsuos-forecast-nov-2023.csv` → 202311; `bsuos-forecast-dec-2023.csv` → 202312; `bsuos-forecast-jan-2024.csv` → 202401; `bsuos-forecast-feb-2024.csv` → 202402; `bsuos-forecast-mar-2024.csv` → 202403; `bsuos-forecast-apr-2024.csv` → 202404; `bsuos-forecast-may-2024.csv` → 202405; `bsuos-forecast-june-2024-v1.1.csv` → 202406; `bsuos-forecast-july-2024.csv` → 202407; `bsuos-forecast-august-2024.csv` → 202408; `bsuos-forecast-september-2024.csv` → 202409; `bsuos-forecast-october-2024.csv` → 202410; `bsuos-forecast-november-2024.csv` → 202411; `bsuos-forecast-december-2024.csv` → 202412; `bsuos-forecast-january-2025.csv` → 202501; `bsuos-forecast-february-2025.csv` → 202502; `bsuos-forecast-march-2025.csv` → 202503; `bsuos-forecast-april-2025.csv` → 202504; `bsuos-forecast-may-2025.csv` → 202505; `bsuos-forecast-june-2025.csv` → 202506; `bsuos-forecast-july-2025.csv` → 202507; `bsuos-forecast-aug-2025-2.csv` → 202508; `bsuos-forecast-sep-2025.csv` → 202509; `bsuos-forecast-october-2025.csv` → 202510; `bsuos-forecast-november-2025.csv` → 202511; `bsuos-forecast-december-2025.csv` → 202512; `bsuos-forecast-january-2026.csv` → 202601; `bsuos-forecast-february-2026.csv` → 202602; `bsuos-forecast-march-2026.csv` → 202603; `bsuos-forecast-april-2026.csv` → 202604; `bsuos-forecast-may-2026.csv` → 202605; `bsuos-forecast-june-2026.csv` → 202606; `bsuos-forecast-july-2026.csv` → 202607; `bsuos-forecast-august-2026.csv` → 202608; `bsuos-forecast-september-2026-v2.csv` → 202609; `bsuos-forecast-october-2026.csv` → 202610
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Two clocks.**

1. **Vintage (`ckan_last_modified`).** `published_at` is the CKAN `last_modified` of the captured
   file, read as UTC (ADR-030), and `available_at` equals it. In silver (2026-10-12) every
   edition has exactly one `published_at`, and `available_at = published_at` on all 1,272 rows.
   The values run from 2022-02-07T11:59:38Z (February 2022 edition) to 2026-09-21T10:38:16Z
   (October 2026 edition). The upload time is **not** the instant NESO issued the forecast:
   historical editions were uploaded later than their file-name month suggests, and the filename
   month is only an edition label. As-of queries on `available_at` therefore show an edition
   only from its upload, and the family is held for this reason.
2. **Event time (temporal recipe `none`).** The record has no temporal column. `timestamp_utc`
   and `event_time` are the **capture time** (they equal `capture_written_at` on every row, and
   so are the same for every row of an edition), not a time the vendor measured or published.
   The target month stays in `month_vendor` as the vendor's text label, because the vendor gives
   no month boundary or time zone (`TODO: BSUOS-MONTH-CLOCK`; vendor dictionary: type `yearmonth`,
   "the month BSUoS forecasted for"). Do not turn it into a UTC instant.

**Month label spellings.** `month_vendor` is stored exactly as delivered. 25 editions spell it
`Mon-YY` (February 2022 to December 2024 editions) and 28 spell it `DD/MM/YYYY` (July 2023 to
October 2026 editions); both spellings occur in the same period. A consumer must parse both.

**Identity and selection.** The entity key is `(resource_id, edition, month_vendor)`. Silver
holds 1,272 rows and 0 duplicate keys, equal to the planned count. `edition` is the integer
`YYYYMM` of the vendor file-name month (the explicit file-name to edition map above, ADR-042),
so `202610` is the October 2026 file. Editions overlap on target months and **disagree**: across
all 75 resources, of 1,653 overlapping target-month pairs between consecutive editions (ordered
by upload), 173 agree on every shared measure, 1,435 differ and 45 have no shared named measure
(FACTS g3). Every edition is therefore a separate vintage. `_latest` is `whole_capture` per
`resource_id`: the newest capture of each resource, never one capture for the family. The
vendor publishes no key; `TODO: verify` a vendor-guaranteed unique key and whether a published
edition is ever revised in place.

**Units (vendor dictionary, FACTS g4).** The `Vendor unit` column in the schema tables comes from
the vendor's saved field info for the current file shape (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/bsuos_monthly_forecast_fc_summary.json`).
The dictionary gives **£m** for the cost components, the internal cost and incentive, the winter
security, 21/22 under-recovered, CMP398/412 and interest columns, and **TWh** for the estimated
BSUoS volume. It has no entry for `BSUoS Cost Recovery`, `ALoMCP`, the two deferred-cost columns,
`Winter Contingency Cost (Central)` or the bare `Volume`; their schema rows show `—` and the unit
is `TODO: verify`, even where the header text says £m. Open unit questions:

- `Additional NESO Framework Costs (£m)` (epoch 8): the header says £m but the dictionary unit is
  **TWh**. The vendor dictionary gives TWh; the record carries no unit for this column and
  gridflow stores the value as delivered (`TODO: FRAMEWORK-COST-UNIT`).
- `volume` (epoch 5, July 2023 only): the bare `Volume` header has no vendor unit.
- `unnamed_16` and `unnamed_15` (epochs 1 and 2): columns with an **empty vendor header**, kept as
  nullable strings. Both are null in every loaded row. They have no vendor name or unit.
- Older vendor dictionaries label `Demand` as £ while describing a volume, and some older
  dictionaries give the internal cost as £ where the header says £m (FACTS g4). The loaded
  epochs have no `Demand` column, and these conflicts concern the older editions, which are
  among the undecoded ones. `TODO: verify` before any of those editions gets a record.

**Sentinels and missingness (FACTS g5).** The first column, `Month`, is required. Wholly blank
rows exist in some bodies (22 across the 75 resources) and are excluded by the required-column
rule, with a recorded tally. Every loaded edition has exactly 24 rows. Zero cells stay zero and
nothing else is inferred. One sentinel needs a ruling:

- **The dash.** Three editions (March, April and May 2024, epoch 7) write `-` in
  the cost columns `Winter Security of Supply Cost (£m)` and `21/22 Under-Recovered Costs (£m)`,
  padded with spaces. Counted in bronze: **34, 35 and 36 dash cells** respectively (105 in all;
  54 in the under-recovered column and 51 in the winter-security column). The January and
  February 2024 editions write `0` for the same target months. gridflow loads the padded dash as
  **null**. It does **not** read it as zero, because whether the dash means zero or
  not-available is an open vendor question: `TODO: the meaning of ' - ' in a cost column`. If a
  ruling says zero, March to May 2024 is re-transformed from bronze.
- **How it loads (ADR-034, Amendment 1).** The record declares an opt-in ASCII edge trim and the
  null token `-` on exactly those two columns of epoch 7, applied in the order trim, then
  null-token match, then the strict numeric cast. Before the amendment those three bodies failed
  the cast (RULINGS 678) and left 50 editions and 1,200 rows. No other column or epoch uses the
  trim, and no cast failure remains.

**Activation (2026-10-12).** BAL-2a (PR #107, master `eeaac8d`, RULINGS 681; activation RULINGS 682) loaded 50 editions
and 1,200 rows with 25 failed captures: 22 `UnicodeDecodeError` (adjudicated, RULINGS 667) and
3 `InvalidOperationError` (March to May 2024, left open under RULINGS 678). BAL-2aH (PR #108,
master `6f5e3b1`, RULINGS 686) added the trim. The re-transform of the 2026-10-08 to 2026-10-12
window (RULINGS 687, after a snapshot of the 50 existing files) gave **53 editions and 1,272
rows, 0 duplicate keys**, with the 50 earlier partitions byte-equal to the snapshot. Reconcile
`--all --cutoff 2026-10-12` exited 0 over 123 families with 0 gaps, 45 adjudicated and 0 stale
(gridflow `@.planning/v0.22-RESULTS.md`, sections BAL-2a and BAL-2aH).

**Silver layout.** One Parquet file per capture under
`C:/gridflow-data/silver/neso_data_portal/bsuos_monthly_forecast_fc_summary/year=2026/month=10/`
(53 files). The `year=`/`month=` partition is the **capture** date. Columns: `month_vendor`,
the vendor measure columns (the union across epochs; a column absent from an edition is null),
`edition`, `resource_id`, `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`. All
timestamps are tz-aware UTC. No gold view or builder reads this family.

**Misplaced file.** The resource `Monthly BSUoS Forecast Summary Nov_20`
(`b41ca68b-9248-4442-a158-664e13e6f9c8`) in this family is byte-identical to the actual-summary
resource `Monthly BSUoS Actual Summary Nov_20` (`42f21a68-6700-4585-b63b-bc0080a99d2b`), so it is
an actual summary, not a forecast. It is one of the 22 undecoded resources.

**Why the usual shortcut fails.** Where every target month in a forecast file is after the file's
CKAN `last_modified`, gridflow lets the vintage stand in for the issue time (RULINGS 529,
forward-target exception). That holds for only two of the 75 resources (the March and April 2022
editions). The other loaded editions include target months on or before their own upload, so the
exception fails (FACTS g2).

### `bsuos_monthly_forecast_fc_summary_pct`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no
- ingest-only: no silver yet

**What it is.** The same forecast under **demand-suppression scenarios**. There are 12 resources:
the June, July, August and September editions at 5, 10 and 15 percent (the resource names say
"Forecast Summary ... Percent"). The percentage labels the scenario, not the unit of any value;
the filename-to-scenario reading is supported by NESO's contemporary forecast publication
([NESO document 284381](https://www.neso.energy/document/284381/download)), which does not
give an issue time.

**State.** Bronze only; **no record** (RULINGS 667). All 12 bodies are invalid UTF-8. Two raw
header epochs (5 resources / 120 rows, 7 resources / 168 rows). `Month` is unique within each
body and the key would be `resource_id` plus `Month`. Every resource has target months on or
before its own upload, so the forward-target exception does not apply.

**Units (FACTS g4).** `TODO: verify`: the monetary headers say £m but the dictionary says £, and
the charge header says £/MWh where the dictionary says £. The scale needs a vendor
clarification. `Demand` is labelled £ while described as a volume (`TODO: FC-PCT-DEMAND-UNIT`).
An anonymous numeric column has a few populated cells (7) and no vendor identity or unit.

**Clocks.** Vintage `ckan_last_modified`; event time `none` with the raw `Month` label.

### `bsuos_monthly_forecast_files`

- Kind: files · archetype: FC · refresh: monthly · empty allowed: no
- files: catalogue only

**What it is.** The catalogue family for the two non-CSV resources: the communications-pack PDF
(DOC) and the `BSUoS_Report_Jan 19 - Mar 20` archive (HOLD). Both are captured as bronze bytes
and neither has silver. See the HOLD table and the notes after it above for the 15 workbooks and
151 sheets.

### `bsuos_monthly_forecast_impact_on_due`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no
- ingest-only: no silver yet

**What it is.** One resource, "Impact on BSUoS due to COVID-19 low demands – Excluding new
services" (file `monthly-bsuos-summary-no-new-services.csv`): a 36-row forecast scenario for
low demand, with one header epoch. The resource name is the only description;
`TODO: verify` the scenario wording and period with the vendor.

**State.** Bronze only; **no record** (RULINGS 667). The body is not valid UTF-8. It has
target months both before and after its own upload (21 and 15) and no issue column, so the
forward-target exception does not apply. `Month` is unique in the body.

**Units (FACTS g4).** The internal-cost header says £m but the dictionary says £ (`TODO: verify`);
the other named service costs, Profit and ALoMCP are labelled £ in the dictionary, and `Demand`
is described as a volume but labelled £ (`TODO: verify`).

**Clocks.** Vintage `ckan_last_modified`; event time `none`, raw `Month` label kept.

### `bsuos_monthly_forecast_including_new`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no
- ingest-only: no silver yet

**What it is.** One resource, "BSUoS Forecast for May 2020 – Including new services" (file
`monthly-bsuos-summary-expected-costs.csv`): the alternative to the previous family that includes
the new services. It is a 36-row body with one header epoch.

**State.** Bronze only; **no record** (RULINGS 667). The body is not valid UTF-8, has target
months both before and after its own upload (21 and 15) and no issue column. `Month` is
unique. Units carry the same open questions as `bsuos_monthly_forecast_impact_on_due`
(`TODO: verify`).

**Clocks.** Vintage `ckan_last_modified`; event time `none`, raw `Month` label kept.

### `bsuos_monthly_forecast_sum_winter`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no
- ingest-only: no silver yet

**What it is.** One resource, "Monthly BSUoS Forecast Summary September 2022 with Winter
Contingency Cost": the September 2022 edition with a winter-contingency cost column added. It is
a 24-row body with one header epoch.

**State.** Bronze only; **no record** (RULINGS 667). The header mixes valid UTF-8 text with a
single `0xA3` byte (the winter-cost column), so a blanket single-byte re-decode would corrupt the
UTF-8 fields (`TODO: verify` a vendor encoding or an adjudication). One target month is on or
before the upload and 23 are after, so the forward-target exception fails.

**Units.** The cost columns are £m and `Estimated BSUoS Volume` is TWh, as the vendor headers
and dictionary declare (FACTS g4).

**Clocks.** Vintage `ckan_last_modified`; event time `none`, raw `Month` label kept.

### `bsuos_monthly_forecast_summary`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no
- ingest-only: no silver yet

**What it is.** The monthly "BSUoS Summary" tables: 18 resources dated between March 2020 and
December 2021 (not every month is present). Most bodies combine historical and forecast target
months in one table: 17 bodies have 36 rows and one, with a forecast-style header, has 24.

**State.** Bronze only; **no record** (RULINGS 667). None of the 18 bodies is valid UTF-8. There
are five header epochs (8, 1, 1, 7 and 1 resources; 636 rows in all), with some trailing columns
that have empty vendor names and hold no values. Month is unique within each body; the key
would be `resource_id` plus `Month`. Of the target months, 255 are on or before their upload and
381 after, so the family is not all-forward. Editions overlap and their shared values were
revised between resources, so it cannot be treated as one disjoint monthly series.

**Units (FACTS g4).** `TODO: verify` the internal-cost scale (header £m, dictionary £), the bare
`Constraints` and deferred-cost columns, and `Demand` (described as a volume, labelled £). The
charge column says £/MWh in its header.

**Clocks.** Vintage `ckan_last_modified`; event time `none`, raw `Month` label kept.

### `bsuos_monthly_forecast_summary_pct`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no
- ingest-only: no silver yet

**What it is.** The "BSUoS Summary" tables under the 5, 10 and 15 percent demand-suppression
scenarios, for the June, July, August and September editions: 12 resources of 36 rows each, one
header epoch (432 rows).

**State.** Bronze only; **no record** (RULINGS 667). All 12 bodies are invalid UTF-8. `Month` is
unique within each body; the key would be `resource_id` plus `Month`. Every resource has historical
target months, so the forward-target exception fails.

**Units (FACTS g4).** Here the selected dictionary establishes `Demand` in **TWh**. The bare
service-cost, Profit and ALoMCP columns are labelled £, and the internal cost has the same
£m-versus-£ conflict as elsewhere (`TODO: verify`). The scenario percentage does not change any
column's unit.

**Clocks.** Vintage `ckan_last_modified`; event time `none`, raw `Month` label kept.

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Monthly

The vendor says the forecast is updated monthly, and the held family's 53 editions agree: each
month's edition is a separate upload, and the CKAN `last_modified` of the editions runs from
2022-02-07 to 2026-09-21. Uploads are not at a fixed day of the month, and some months are
absent from the decoded set (May 2022 and April to June 2023 are among the 22 undecoded
resources). The CKAN package itself was last modified on 2026-09-21. gridflow captured every
resource once, on 2026-10-08; the capture history is therefore one point, and nothing yet shows
whether NESO revises an edition after upload. `TODO: verify` the publication calendar and
whether an uploaded edition is ever replaced in place. Only repeated captures, compared pair by
pair, can show it.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above. The vendor's own
disclaimer applies to the content: the forecast is published without prejudice and is subject to
estimations that may not match later tariffs.

## Holds

- `bsuos_monthly_forecast_fc_summary`: held: TODO: the issue instant and availability of each monthly edition (filename month is an edition label, not an issue time); all 53 UTF-8 editions load, and March-May 2024 load the accounting token as null (RULINGS 678); the loaded editions include targets on or before their upload (RULINGS 529 forward-target rule fails); the target-month clock (BSUOS-MONTH-CLOCK); the units of bare `Volume` (July 2023) and `Additional NESO Framework Costs (£m)` (dictionary says TWh); and whether `' - '` in a cost column means zero (the January and February 2024 editions read `0` for the same target months) or not-available; a zero ruling re-transforms March-May 2024 from bronze. (unit v0.22-K-BAL-2a)

The silver output exists on disk and is **held**. It may not be published or used for
point-in-time models until the unit that settles the semantics question (E-SEM) answers the
question above. The registry records the hold against the unit that created it
(`v0.22-K-BAL-2a`); the hold sits in the record. Adding the dash-to-null load (RULINGS 678, 680,
686, 687) deliberately did not settle the dash question, so the family stayed held: the record
still declares `status: held` after the trim, and the eligibility report agrees with the
registry.

**The hold questions, in plain terms.**

1. **Issue time and availability.** The filename month is an edition label. The only clock is the
   CKAN `last_modified` of the upload. `TODO: verify` when each edition was actually issued and
   whether the uploaded bytes are the ones NESO published then.
2. **Forward-target rule fails.** The loaded editions include target months on or before their
   own upload, so RULINGS 529's exception (vintage stands in for the issue time) does not hold.
   Only the March and April 2022 editions pass it, and a family-wide rule cannot rest on two.
3. **Target-month clock (`TODO: BSUOS-MONTH-CLOCK`).** No vendor statement defines the month
   boundary or zone for `Month`.
4. **Units.** The bare `Volume` of the July 2023 edition and `Additional NESO Framework Costs
   (£m)` (header £m, dictionary TWh) are unresolved (`TODO: FRAMEWORK-COST-UNIT`), as are the
   scales of the columns the dictionary does not cover.
5. **The dash.** Whether `-` in a cost column means zero or not-available is an open vendor
   question. It loads as null, never zero. The unit holding the answer is E-SEM.

**Other outputs held or without a record.** Only this family has silver. The other seven
tabular families have no record (RULINGS 667; encoding unresolved), the daily forecast package
has no record, the workbook archive is HOLD (`TODO: WORKBOOK-CHILD-RECORDS`), and no gold view
reads anything in this package. Consumers must not treat the silver rows as a published
forecast history.

**Never publish the values.** This page shows schema, row counts, clocks and missingness only,
and no export of this family's values should be published until the hold is lifted.

