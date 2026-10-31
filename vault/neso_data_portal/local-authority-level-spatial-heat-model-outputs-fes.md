---
source: "neso_data_portal"
package: "local-authority-level-spatial-heat-model-outputs-fes"
dataset_keys: ["fes_la_heat_model_domestic", "fes_la_heat_model_residential"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Local authority heat model outputs
  summary: >-
    NESO's spatial heat model results for its Future Energy Scenarios (FES): buildings on each
    heating technology, per GB local authority.
  facts:
    vendor: "NESO Data Portal: 20 CSVs, one per edition and modelled year"
    cadence: "Ad hoc (NESO); FES 2022, 2024 and 2025 editions, as at 6 October 2026"
    grain: "One row per local authority, year, scenario or pathway, and sector"
    history: "NESO created the package on 9 March 2022"
  landscape: power
  what_it_is: >-
    Two separate tables, never stacked or joined. FES 2022 domestic files give buildings on each
    heating technology and their proportions. FES 2024 and 2025 residential files give dwellings or
    buildings only, and some technology columns change name between the editions. Each file is one
    modelled year, five-yearly to 2050. NESO's dictionary calls the 2022 oil boiler stock a
    proportion.
  how_used:
    - "Heat pump and gas boiler numbers by local authority, under each scenario or pathway"
    - "Map the heating technology mix across GB local authorities, edition by edition"
  chart:
    type: bar
    silver: neso_data_portal/fes_la_heat_model_residential
    value: stock_ashp
    filter:
      - {column: edition, op: eq, value: 2025}
      - {column: pathway, op: eq, value: Holistic Transition}
    dedup: {"on": [resource_id, edition, la_code, projection_year, pathway, sector], order_by: capture_written_at}
    group: projection_year
    aggregation: sum
    sort: label
    unit: dwellings or buildings
  chart_view:
    title: Air-source heat pumps, FES 2025, Holistic Transition
    caption: >-
      Silver `fes_la_heat_model_residential`, the residential table, FES 2025 (NESO's files of 25
      November 2025), pathway Holistic Transition: `stock_ashp`, gridflow's sum over 371 local
      authorities, one bar per modelled year as NESO's `Year` gives it. A projection.
    alt: >-
      Horizontal bar chart of NESO's projected dwellings or buildings using an air-source heat pump,
      FES 2025 edition, pathway Holistic Transition, gridflow's sum over 371 local authorities, one
      bar per modelled year: 2025 359,178; 2030 2,070,328; 2035 6,341,010; 2040 9,162,201; 2045
      11,571,185; 2050 13,209,035. The count rises about 37-fold.
    key:
      - {series: stock_ashp, label: Air-source heat pumps, codes: stock ASHP, paint: petrol, note: "NESO's residential dictionary: number of homes or buildings using the technology"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show` per table, then its files, each downloaded whole
      unless its `last_modified` is unchanged. Shown: each edition's first and last year.
    commands:
      - {run: gridflow ingest neso_data_portal fes_la_heat_model_residential --last 24h, comment: "whole CSVs; swap in either key"}
      - {run: gridflow transform neso_data_portal fes_la_heat_model_residential --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      silver: neso_data_portal/fes_la_heat_model_residential
      filter:
        - {column: edition, op: eq, value: 2025}
        - {column: la_code, op: eq, value: E08000035}
        - {column: projection_year, op: in, value: [2025, 2050]}
      dedup: {"on": [resource_id, edition, la_code, projection_year, pathway, sector], order_by: capture_written_at}
      order_by: [projection_year, pathway]
      columns: [la_code, local_authority, projection_year, pathway, stock_ashp, stock_gas_boiler,
                stock_hydrogen_boiler, stock_gshp, sector, edition, resource_id, published_at,
                timestamp_utc]
    key: [resource_id, edition, la_code, projection_year, pathway, sector]
    caption: "The residential table, FES 2025: Leeds in its 2025 and 2050 files, four pathways."
    fields:
      la_code: "Local authority code; NESO's dictionary says December 2019 districts"
      local_authority: "Local authority name, as NESO spells it"
      projection_year: "NESO's `Year`: one modelled year per file; NESO states no count date"
      pathway: "NESO's FES pathway; four per edition, not the same four in 2024 and 2025"
      stock_ashp: "Dwellings or buildings using an air-source heat pump, per NESO's dictionary"
      stock_gas_boiler: "Dwellings or buildings using a gas boiler"
      stock_hydrogen_boiler: "Dwellings or buildings using a hydrogen boiler"
      stock_gshp: "Dwellings or buildings using a ground-source heat pump"
      sector: "NESO's sector: `Residential` in every row of the files shown"
      stock_biofuel_boiler: "FES 2024 only: a biofuel boiler; null in FES 2025 rows"
      stock_biomass_boiler: "Dwellings or buildings using a biomass boiler"
      stock_community: "FES 2024 only: `Community`, fossil-fuel heat networks per NESO's dictionary"
      stock_dh: "FES 2024 only: `DH`, low-carbon district heat networks per NESO's dictionary"
      stock_electric_resistive: "Dwellings or buildings using electric resistive heating"
      stock_electric_storage: "Dwellings or buildings using electric storage heating"
      stock_hybrid_ashp_biofuel_boiler: "FES 2024 only: an air-source heat pump with a biofuel boiler"
      stock_hybrid_ashp_electric_resistive: "An air-source heat pump with electric resistive heating, as one hybrid"
      stock_hybrid_ashp_hydrogen_boiler: "An air-source heat pump with a hydrogen boiler, as one hybrid"
      stock_oil_boiler: "Dwellings or buildings using an oil boiler"
      stock_biolpg_boiler: "FES 2025 only: a BioLPG boiler; NESO does not say it is 2024's biofuel"
      stock_fossil_fuel_communal_heating: "FES 2025 only: fossil fuel communal heating"
      stock_hybrid_ashp_biolpg_boiler: "FES 2025 only: an air-source heat pump with a BioLPG boiler"
      stock_low_carbon_district_heating: "FES 2025 only: low carbon district heating"
      edition: "FES edition, from the file name: 2024 or 2025"
      resource_id: "CKAN file id, one per edition and modelled year; first key column"
      published_at: "NESO's last-modified time for the file, read as UTC"
      timestamp_utc: "When gridflow captured the file, UTC; the table has no event time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the residential table's `_latest` view. The domestic FES 2022 table is never stacked or
      joined with it. The sums are gridflow's.
    cells:
      - |
        hp = data.sql("""
            SELECT pathway, projection_year, SUM(stock_ashp) AS ashp
            FROM silver_neso_data_portal_fes_la_heat_model_residential_latest
            WHERE edition = 2025
            GROUP BY pathway, projection_year
        """)
        wide = hp.pivot(index="projection_year", columns="pathway", values="ashp").rename_axis(index=None, columns=None)
        wide.round(-3)
      - |
        ax = wide.plot(figsize=(8, 3.5), style="o-", xlabel="NESO's modelled year",
                       ylabel="air-source heat pumps, all authorities");
      - |
        data.sql("""
            SELECT la_code, local_authority, stock_ashp, stock_gas_boiler, stock_hydrogen_boiler
            FROM silver_neso_data_portal_fes_la_heat_model_residential_latest
            WHERE edition = 2025 AND pathway = 'Holistic Transition' AND projection_year = 2050
            ORDER BY stock_ashp DESC
            LIMIT 5
        """).round(0)
    needs: NESO's FES 2025 local authority residential files
    plot_alt: >-
      Line plot of NESO's projected dwellings or buildings with an air-source heat pump, FES 2025
      edition, summed over 371 local authorities, modelled years 2025 to 2050, one line per pathway.
      All start near 359,000; Holistic Transition ends highest at about 13.2 million and Falling
      Behind lowest at about 7.7 million.
  family:
    slug: local-authority-level-spatial-heat-model-outputs-fes
    members:
      - dataset: fes_la_heat_model_domestic
        differs: "FES 2022 domestic: buildings per heating technology and their proportion, 2020 to 2050"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=local-authority-level-spatial-heat-model-outputs-fes"
          - "GET https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/c3dd66ab-cb07-4e4d-bbab-d79074ea1713/download/fes22_la_level_outputs_2020_domestic_all_scenarios.csv"
          - "GET https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/3a9451a1-9e79-4fda-a570-79544b30f44e/download/fes22_la_level_outputs_2050_domestic_all_scenarios.csv"
        caveat: "NESO states no count date, calls oil boiler stock a proportion, and leaves hydrogen blanks unexplained."
      - dataset: fes_la_heat_model_residential
        differs: "FES 2024 and 2025 residential: dwellings or buildings per heating technology, five-yearly"
        request:
          - "GET https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/31d45b63-e70d-4cf1-a912-918bf3de58d5/download/fes24_la_level_outputs_2020_residential_all_scenarios.csv"
          - "GET https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/010d5cb3-2907-4ccd-949f-a3ec726b5109/download/fes24_la_level_outputs_2050_residential_all_scenarios.csv"
          - "GET https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/e2215328-bd74-47c2-a22f-3878bb0fbbd5/download/fes25_la_level_outputs_2025_residential_all_scenarios.csv"
          - "GET https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/593f1c8c-b278-4405-9164-21dfacd70a6d/download/fes25_la_level_outputs_2050_residential_all_scenarios.csv"
        caveat: "NESO states no count date for each year's stock."
  related:
    - {dataset: neso_data_portal/building-heat-model, note: "NESO's tool modelling one home's half-hourly heat demand"}
    - {dataset: neso_data_portal/fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3, note: "NESO's FES heat demand by technology, for GB as a whole"}
    - {dataset: neso_data_portal/regional-breakdown-of-fes-data-electricity, note: "Another regional FES breakdown: electricity by Grid Supply Point"}
---

# Local Authority Level Spatial Heat Model Outputs (FES)

NESO's local-authority-level output of the spatial heat model it uses for the Future Energy
Scenarios (FES). Each row is one local authority, one projection year, one scenario or pathway
and one sector, with one column per heating technology (air-source and ground-source heat
pumps, hybrids, gas, oil, biomass and BioLPG boilers, hydrogen boilers, electric resistive and
storage heating, and community or district heating). The package notes describe it as the
number of buildings per local authority on each heating technology, and for the older tables
also the proportion of buildings on each. Once the holds below lift, it is a candidate scenario
input for allocating heat electrification (heat-pump uptake and the loss of gas heating) to
local authorities in GB energy-system models. The package notes describe it as regional results
from the Spatial Heat model, i.e. model output. The vendor does not say whether the 2020 slice
reflects observed stock or a modelled baseline (`TODO: verify`, part of the `Year` hold).

The package is **two separate tables published under one CKAN package**, and gridflow keeps
them as two families:

- `fes_la_heat_model_domestic` is the **FES 2022** "domestic" output. Seven resources, one per
  projection year (2020, 2025, 2030, 2035, 2040, 2045, 2050). It has both stock columns and
  stock-proportion columns, and a `scenario` column.
- `fes_la_heat_model_residential` is the **FES 2024 and FES 2025** "residential" output.
  Thirteen resources: seven for FES 2024 (2020 to 2050) and six for FES 2025 (2025 to 2050).
  It has stock columns only, and a `pathway` column. The vendor renamed several technology
  columns between the two editions.

The domestic and residential tables are not one table with a renamed sector. Their headers,
technology sets and editions differ (see Families). The package has 20 resources in total, all
CSV, all captured as `upload` files, and all `SILVER`. There is no `DOC` resource. The
publisher is NESO; the package is part of the FES group. It sits beside the building-level heat
model (@building-heat-model.md) and the FES heat-demand table
(@fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3.md), and
the vendor README is @../README.md.

**The silver output of both families is held in gridflow (unit E-SEM).** This note gives its
schema, row counts and structure. Under ruling 66 the site page shows rows, with one caveat line
per table naming its open question; its chart, eight sample rows and notebook come from the
residential table alone, never stacked or joined with the domestic one. The meaning of the `Year`
column (the stock assessment date) is not established for either table (see Holds). The package-level
`eligibility: eligible` in the front matter is the package registry entry. The hold is per
family.

Reading rules for anyone who does open the silver:

- **Edition is a dimension.** Domestic is edition 2022. Residential is editions 2024 and 2025.
  The FES 2024 and FES 2025 rows for the same authority, year and technology are two
  different published forecasts, not two observations, and their pathway names are not the same
  set (see the next rule). Never sum or average across `edition`.
- **Scenarios and pathways are alternatives, not parts.** There are four per slice or edition
  (the domestic `scenario`, the residential `pathway`). The residential table carries **five**
  distinct pathway names across its two editions: Counterfactual appears in FES 2024 only and
  Falling Behind in FES 2025 only, so do not assume the same four pathways in both editions when
  joining them. Never sum across them, and never mix a
  domestic scenario with a residential pathway. They are two separate columns in two separate
  tables. gridflow does not merge or map them. `TODO: verify` whether NESO treats the FES 2022
  scenarios and the FES 2024 and 2025 pathways as the same concept.
- **Domestic and residential are separate tables.** Do not stack them, and do not read a
  difference between them as a change over time. They differ in edition, column set and
  technology naming.
- **Stock and proportion are different quantities.** In the domestic table `stock_*` columns are
  numbers of buildings and `stock_proportion_*` columns are proportions of buildings, per the
  vendor dictionary. Keep the proportions in the vendor scale; do not relabel them as
  percentages or rescale them. The residential table has `stock_*` columns only, which are
  numbers of dwellings or buildings per the dictionary.
- **One domestic stock column is contradicted by its own dictionary.** The dictionary
  describes `stock_oil_boiler` as a proportion, although it has a stock heading and a stock
  column name. See Holds. Do not "correct" it from the size of the numbers.
- **Do not sum technology columns.** Whether `stock_total` is the sum of the technology columns,
  and what `stock_totalhps` contains (in particular whether hybrids are inside it), is not
  established. `TODO: verify`. Adding the vendor total to its components double counts if it
  is a total.
- **Renamed residential columns are not aliased.** The FES 2024 and FES 2025 residential
  tables name some technologies differently (see Families). gridflow keeps every vendor column
  under its own name. A technology absent from one edition's file is null in that edition's
  silver rows. That null is "column not in the file", not a vendor blank.
- **Coverage is not a rectangle in the domestic table.** The 2020 slice has one authority fewer
  than the later slices, and that authority is present in only two of the four scenarios in the
  later slices. Check coverage before summing authorities to a national total.
- **`projection_year` is a model year label.** It is the `Year` column of the file body. The
  stock date it denotes is undocumented (see Holds). Do not join it to an observed series as a
  calendar date.
- **A null is a blank vendor cell or an absent column**, never a zero. A `0` is a value, not a
  sentinel.
- **Attribution.** Supported by National Energy SO Open Data.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN
- Vendor tags: FES, Heat, Local Authority, Regional, Subscribable

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| FES 2024 local authority outputs 2020 residential all scenarios | CSV | upload | `31d45b63-e70d-4cf1-a912-918bf3de58d5` |
| FES 2024 local authority outputs 2025 residential all scenarios | CSV | upload | `556a0c77-58f1-4b27-8b8d-105ab2236d25` |
| FES 2024 local authority outputs 2030 residential all scenarios | CSV | upload | `1910373f-ccfb-49b3-bd18-bc0fe560b818` |
| FES 2024 local authority outputs 2035 residential all scenarios | CSV | upload | `549772c3-54e7-40ed-8536-2e5d7e4af4ef` |
| FES 2024 local authority outputs 2040 residential all scenarios | CSV | upload | `3c889f7e-4254-4822-9e2d-6bc58baf111e` |
| FES 2024 local authority outputs 2045 residential all scenarios | CSV | upload | `c62bba09-78e9-4a98-8b41-a387d5004306` |
| FES 2024 local authority outputs 2050 residential all scenarios | CSV | upload | `010d5cb3-2907-4ccd-949f-a3ec726b5109` |
| FES 2025 local authority outputs 2025 residential all scenarios | CSV | upload | `e2215328-bd74-47c2-a22f-3878bb0fbbd5` |
| FES 2025 local authority outputs 2030 residential all scenarios | CSV | upload | `d71b4155-1ee3-492e-9446-4b99b19a8e63` |
| FES 2025 local authority outputs 2035 residential all scenarios | CSV | upload | `eb7be505-5886-4983-94ce-bf1d43c09066` |
| FES 2025 local authority outputs 2040 residential all scenarios | CSV | upload | `e4d69fcb-0d43-49dd-9faa-23f4ee37e983` |
| FES 2025 local authority outputs 2045 residential all scenarios | CSV | upload | `459b8436-17d9-40f1-bb8a-83139b9599c4` |
| FES 2025 local authority outputs 2050 residential all scenarios | CSV | upload | `593f1c8c-b278-4405-9164-21dfacd70a6d` |
| FES 22 local authority outputs 2020 domestic all scenarios | CSV | upload | `c3dd66ab-cb07-4e4d-bbab-d79074ea1713` |
| FES 22 local authority outputs 2025 domestic all scenarios | CSV | upload | `52baf0e4-b02b-4f69-8cd5-ca52c97bf872` |
| FES 22 local authority outputs 2030 domestic all scenarios | CSV | upload | `f41f65e2-9f55-496b-afaa-76efcee4cda2` |
| FES 22 local authority outputs 2035 domestic all scenarios | CSV | upload | `7cec6380-1ad5-44e6-a0d4-246c43456498` |
| FES 22 local authority outputs 2040 domestic all scenarios | CSV | upload | `73f57682-bf0e-4bb6-8471-191f7cb75417` |
| FES 22 local authority outputs 2045 domestic all scenarios | CSV | upload | `e60da220-afb8-4a9e-9327-552a3c8df549` |
| FES 22 local authority outputs 2050 domestic all scenarios | CSV | upload | `3a9451a1-9e79-4fda-a570-79544b30f44e` |

All 20 are `SILVER`. The 7 domestic resources feed `fes_la_heat_model_domestic` and the 13
residential resources feed `fes_la_heat_model_residential`. There is no `DOC` resource and no
resource-level `HOLD` or catalogue-only resource in the package. The holds are on the two
families (see Holds). The resource names follow the pattern `FES 22 local authority outputs
<year> domestic all scenarios`, `FES 2024 local authority outputs <year> residential all
scenarios` and `FES 2025 local authority outputs <year> residential all scenarios`. The files, as
captured on 2026-10-08 (the catalogue snapshot is 2026-10-06):

**Domestic (FES 2022)**

| Edition | Projection year | Download | Bytes | Data rows | CKAN `last_modified` (offset-less, read as UTC) |
|---|---|---|---:|---:|---|
| 2022 | 2020 | [fes22_la_level_outputs_2020_domestic_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/c3dd66ab-cb07-4e4d-bbab-d79074ea1713/download/fes22_la_level_outputs_2020_domestic_all_scenarios.csv) | 577,488 | 1,480 | `2022-08-31T07:33:03.509314` |
| 2022 | 2025 | [fes22_la_level_outputs_2025_domestic_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/52baf0e4-b02b-4f69-8cd5-ca52c97bf872/download/fes22_la_level_outputs_2025_domestic_all_scenarios.csv) | 800,029 | 1,482 | `2022-08-31T07:34:02.299496` |
| 2022 | 2030 | [fes22_la_level_outputs_2030_domestic_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/f41f65e2-9f55-496b-afaa-76efcee4cda2/download/fes22_la_level_outputs_2030_domestic_all_scenarios.csv) | 831,861 | 1,482 | `2022-08-31T07:35:07.017785` |
| 2022 | 2035 | [fes22_la_level_outputs_2035_domestic_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/7cec6380-1ad5-44e6-a0d4-246c43456498/download/fes22_la_level_outputs_2035_domestic_all_scenarios.csv) | 857,729 | 1,482 | `2022-08-31T07:35:55.905799` |
| 2022 | 2040 | [fes22_la_level_outputs_2040_domestic_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/73f57682-bf0e-4bb6-8471-191f7cb75417/download/fes22_la_level_outputs_2040_domestic_all_scenarios.csv) | 857,727 | 1,482 | `2022-08-31T07:37:12.485221` |
| 2022 | 2045 | [fes22_la_level_outputs_2045_domestic_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/e60da220-afb8-4a9e-9327-552a3c8df549/download/fes22_la_level_outputs_2045_domestic_all_scenarios.csv) | 857,920 | 1,482 | `2022-08-31T07:37:53.735487` |
| 2022 | 2050 | [fes22_la_level_outputs_2050_domestic_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/3a9451a1-9e79-4fda-a570-79544b30f44e/download/fes22_la_level_outputs_2050_domestic_all_scenarios.csv) | 855,991 | 1,482 | `2022-08-31T07:38:37.918963` |

**Residential (FES 2024 and FES 2025)**

| Edition | Projection year | Download | Bytes | Data rows | CKAN `last_modified` (offset-less, read as UTC) |
|---|---|---|---:|---:|---|
| 2024 | 2020 | [fes24_la_level_outputs_2020_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/31d45b63-e70d-4cf1-a912-918bf3de58d5/download/fes24_la_level_outputs_2020_residential_all_scenarios.csv) | 207,400 | 1,484 | `2025-11-25T14:57:39.152279` |
| 2024 | 2025 | [fes24_la_level_outputs_2025_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/556a0c77-58f1-4b27-8b8d-105ab2236d25/download/fes24_la_level_outputs_2025_residential_all_scenarios.csv) | 225,000 | 1,484 | `2025-11-25T14:58:37.929980` |
| 2024 | 2030 | [fes24_la_level_outputs_2030_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/1910373f-ccfb-49b3-bd18-bc0fe560b818/download/fes24_la_level_outputs_2030_residential_all_scenarios.csv) | 229,519 | 1,484 | `2025-11-25T14:59:36.439709` |
| 2024 | 2035 | [fes24_la_level_outputs_2035_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/549772c3-54e7-40ed-8536-2e5d7e4af4ef/download/fes24_la_level_outputs_2035_residential_all_scenarios.csv) | 234,177 | 1,484 | `2025-11-25T15:00:29.700100` |
| 2024 | 2040 | [fes24_la_level_outputs_2040_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/3c889f7e-4254-4822-9e2d-6bc58baf111e/download/fes24_la_level_outputs_2040_residential_all_scenarios.csv) | 236,333 | 1,484 | `2025-11-25T15:01:23.381717` |
| 2024 | 2045 | [fes24_la_level_outputs_2045_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/c62bba09-78e9-4a98-8b41-a387d5004306/download/fes24_la_level_outputs_2045_residential_all_scenarios.csv) | 233,521 | 1,484 | `2025-11-25T15:02:45.811599` |
| 2024 | 2050 | [fes24_la_level_outputs_2050_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/010d5cb3-2907-4ccd-949f-a3ec726b5109/download/fes24_la_level_outputs_2050_residential_all_scenarios.csv) | 227,674 | 1,484 | `2025-11-25T15:03:37.952878` |
| 2025 | 2025 | [fes25_la_level_outputs_2025_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/e2215328-bd74-47c2-a22f-3878bb0fbbd5/download/fes25_la_level_outputs_2025_residential_all_scenarios.csv) | 223,306 | 1,484 | `2025-11-25T15:04:38.401027` |
| 2025 | 2030 | [fes25_la_level_outputs_2030_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/d71b4155-1ee3-492e-9446-4b99b19a8e63/download/fes25_la_level_outputs_2030_residential_all_scenarios.csv) | 229,177 | 1,484 | `2025-11-25T15:05:32.327222` |
| 2025 | 2035 | [fes25_la_level_outputs_2035_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/eb7be505-5886-4983-94ce-bf1d43c09066/download/fes25_la_level_outputs_2035_residential_all_scenarios.csv) | 234,900 | 1,484 | `2025-11-25T15:06:37.175691` |
| 2025 | 2040 | [fes25_la_level_outputs_2040_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/e4d69fcb-0d43-49dd-9faa-23f4ee37e983/download/fes25_la_level_outputs_2040_residential_all_scenarios.csv) | 238,237 | 1,484 | `2025-11-25T15:07:28.545103` |
| 2025 | 2045 | [fes25_la_level_outputs_2045_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/459b8436-17d9-40f1-bb8a-83139b9599c4/download/fes25_la_level_outputs_2045_residential_all_scenarios.csv) | 234,938 | 1,484 | `2025-11-25T15:08:50.039625` |
| 2025 | 2050 | [fes25_la_level_outputs_2050_residential_all_scenarios.csv](https://api.neso.energy/dataset/bfa95333-542e-4625-b5d0-17ced50a89ed/resource/593f1c8c-b278-4405-9164-21dfacd70a6d/download/fes25_la_level_outputs_2050_residential_all_scenarios.csv) | 228,272 | 1,484 | `2025-11-25T15:10:15.833424` |

The stable handle for a resource is its id, not the file name. The package id is
`bfa95333-542e-4625-b5d0-17ced50a89ed`. Every body decodes as strict UTF-8 with no ragged rows
(gridflow `@.planning/phases/v0.22-K-SCN-3/K-SCN-3-FACTS.md` §7, g6). Every body carries a `Year`
column whose single distinct value equals the projection year in the table above, so the year is
read from the body and never from the file name. The edition is read from the exact file name
(`fes22_...` is 2022, `fes24_...` is 2024, `fes25_...` is 2025) and never from the body year, the
CKAN timestamp or the capture date. The resource name agrees with the file name for every
resource.

Rows per slice: every domestic slice is 1,482 rows except 2020, which is 1,480. Every
residential slice is 1,484 rows. The silver row count equals the CSV data-row count for every
resource, because the tables are already one row per authority, year, scenario or pathway and
sector (there is no unpivot).

## Families

### `fes_la_heat_model_domestic`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| CODE_x | `code_x` | string | — | no | — | — |
| Local_Authority | `local_authority` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Scenario | `scenario` | string | — | no | — | — |
| Sector | `sector` | string | — | no | — | — |
| stock ASHP | `stock_ashp` | float64 | — | no | — | — |
| stock Community | `stock_community` | float64 | — | no | — | — |
| stock DH | `stock_dh` | float64 | — | no | — | — |
| stock Electric resistive | `stock_electric_resistive` | float64 | — | no | — | — |
| stock Electric storage | `stock_electric_storage` | float64 | — | no | — | — |
| stock GSHP | `stock_gshp` | float64 | — | no | — | — |
| stock Gas boiler | `stock_gas_boiler` | float64 | — | no | — | — |
| stock Oil boiler | `stock_oil_boiler` | float64 | — | no | — | — |
| stock Total | `stock_total` | float64 | — | no | — | — |
| stock TotalHPs | `stock_totalhps` | float64 | — | no | — | — |
| stock_proportion ASHP | `stock_proportion_ashp` | float64 | — | no | — | — |
| stock_proportion Community | `stock_proportion_community` | float64 | — | no | — | — |
| stock_proportion DH | `stock_proportion_dh` | float64 | — | no | — | — |
| stock_proportion Electric resistive | `stock_proportion_electric_resistive` | float64 | — | no | — | — |
| stock_proportion Electric storage | `stock_proportion_electric_storage` | float64 | — | no | — | — |
| stock_proportion GSHP | `stock_proportion_gshp` | float64 | — | no | — | — |
| stock_proportion Gas boiler | `stock_proportion_gas_boiler` | float64 | — | no | — | — |
| stock_proportion Oil boiler | `stock_proportion_oil_boiler` | float64 | — | no | — | — |
| stock_proportion TotalHPs | `stock_proportion_totalhps` | float64 | — | no | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| CODE_x | `code_x` | string | — | no | — | — |
| Local_Authority | `local_authority` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Scenario | `scenario` | string | — | no | — | — |
| Sector | `sector` | string | — | no | — | — |
| stock ASHP | `stock_ashp` | float64 | — | no | — | — |
| stock BioLPG boiler | `stock_biolpg_boiler` | float64 | — | yes | — | — |
| stock Biomass boiler | `stock_biomass_boiler` | float64 | — | yes | — | — |
| stock Community | `stock_community` | float64 | — | no | — | — |
| stock DH | `stock_dh` | float64 | — | no | — | — |
| stock Electric resistive | `stock_electric_resistive` | float64 | — | no | — | — |
| stock Electric storage | `stock_electric_storage` | float64 | — | no | — | — |
| stock GSHP | `stock_gshp` | float64 | — | no | — | — |
| stock Gas boiler | `stock_gas_boiler` | float64 | — | no | — | — |
| stock Hybrid (ASHP + BioLPG boiler) | `stock_hybrid_ashp_biolpg_boiler` | float64 | — | yes | — | — |
| stock Hybrid (ASHP + Electric resistive) | `stock_hybrid_ashp_electric_resistive` | float64 | — | yes | — | — |
| stock Oil boiler | `stock_oil_boiler` | float64 | — | no | — | — |
| stock Total | `stock_total` | float64 | — | no | — | — |
| stock TotalHPs | `stock_totalhps` | float64 | — | no | — | — |
| stock_proportion ASHP | `stock_proportion_ashp` | float64 | — | no | — | — |
| stock_proportion BioLPG boiler | `stock_proportion_biolpg_boiler` | float64 | — | yes | — | — |
| stock_proportion Biomass boiler | `stock_proportion_biomass_boiler` | float64 | — | yes | — | — |
| stock_proportion Community | `stock_proportion_community` | float64 | — | no | — | — |
| stock_proportion DH | `stock_proportion_dh` | float64 | — | no | — | — |
| stock_proportion Electric resistive | `stock_proportion_electric_resistive` | float64 | — | no | — | — |
| stock_proportion Electric storage | `stock_proportion_electric_storage` | float64 | — | no | — | — |
| stock_proportion GSHP | `stock_proportion_gshp` | float64 | — | no | — | — |
| stock_proportion Gas boiler | `stock_proportion_gas_boiler` | float64 | — | no | — | — |
| stock_proportion Hybrid (ASHP + BioLPG boiler) | `stock_proportion_hybrid_ashp_biolpg_boiler` | float64 | — | yes | — | — |
| stock_proportion Hybrid (ASHP + Electric resistive) | `stock_proportion_hybrid_ashp_electric_resistive` | float64 | — | yes | — | — |
| stock_proportion Oil boiler | `stock_proportion_oil_boiler` | float64 | — | no | — | — |
| stock_proportion TotalHPs | `stock_proportion_totalhps` | float64 | — | no | — | — |

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| CODE_x | `code_x` | string | — | no | — | — |
| Local_Authority | `local_authority` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Scenario | `scenario` | string | — | no | — | — |
| Sector | `sector` | string | — | no | — | — |
| stock ASHP | `stock_ashp` | float64 | — | no | — | — |
| stock BioLPG boiler | `stock_biolpg_boiler` | float64 | — | yes | — | — |
| stock Biomass boiler | `stock_biomass_boiler` | float64 | — | yes | — | — |
| stock Community | `stock_community` | float64 | — | no | — | — |
| stock DH | `stock_dh` | float64 | — | no | — | — |
| stock Electric resistive | `stock_electric_resistive` | float64 | — | no | — | — |
| stock Electric storage | `stock_electric_storage` | float64 | — | no | — | — |
| stock GSHP | `stock_gshp` | float64 | — | no | — | — |
| stock Gas boiler | `stock_gas_boiler` | float64 | — | no | — | — |
| stock Hybrid (ASHP + BioLPG boiler) | `stock_hybrid_ashp_biolpg_boiler` | float64 | — | yes | — | — |
| stock Hybrid (ASHP + Electric resistive) | `stock_hybrid_ashp_electric_resistive` | float64 | — | yes | — | — |
| stock Hybrid (ASHP + Hydrogen boiler) | `stock_hybrid_ashp_hydrogen_boiler` | float64 | — | yes | — | — |
| stock Hydrogen boiler | `stock_hydrogen_boiler` | float64 | — | yes | — | — |
| stock Oil boiler | `stock_oil_boiler` | float64 | — | no | — | — |
| stock Total | `stock_total` | float64 | — | no | — | — |
| stock TotalHPs | `stock_totalhps` | float64 | — | no | — | — |
| stock_proportion ASHP | `stock_proportion_ashp` | float64 | — | no | — | — |
| stock_proportion BioLPG boiler | `stock_proportion_biolpg_boiler` | float64 | — | yes | — | — |
| stock_proportion Biomass boiler | `stock_proportion_biomass_boiler` | float64 | — | yes | — | — |
| stock_proportion Community | `stock_proportion_community` | float64 | — | no | — | — |
| stock_proportion DH | `stock_proportion_dh` | float64 | — | no | — | — |
| stock_proportion Electric resistive | `stock_proportion_electric_resistive` | float64 | — | no | — | — |
| stock_proportion Electric storage | `stock_proportion_electric_storage` | float64 | — | no | — | — |
| stock_proportion GSHP | `stock_proportion_gshp` | float64 | — | no | — | — |
| stock_proportion Gas boiler | `stock_proportion_gas_boiler` | float64 | — | no | — | — |
| stock_proportion Hybrid (ASHP + BioLPG boiler) | `stock_proportion_hybrid_ashp_biolpg_boiler` | float64 | — | yes | — | — |
| stock_proportion Hybrid (ASHP + Electric resistive) | `stock_proportion_hybrid_ashp_electric_resistive` | float64 | — | yes | — | — |
| stock_proportion Hybrid (ASHP + Hydrogen boiler) | `stock_proportion_hybrid_ashp_hydrogen_boiler` | float64 | — | yes | — | — |
| stock_proportion Hydrogen boiler | `stock_proportion_hydrogen_boiler` | float64 | — | yes | — | — |
| stock_proportion Oil boiler | `stock_proportion_oil_boiler` | float64 | — | no | — | — |
| stock_proportion TotalHPs | `stock_proportion_totalhps` | float64 | — | no | — | — |

- Entity key: `resource_id`, `edition`, `code_x`, `projection_year`, `scenario`, `sector`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes22_la_level_outputs_2020_domestic_all_scenarios.csv` → 2022; `fes22_la_level_outputs_2025_domestic_all_scenarios.csv` → 2022; `fes22_la_level_outputs_2030_domestic_all_scenarios.csv` → 2022; `fes22_la_level_outputs_2035_domestic_all_scenarios.csv` → 2022; `fes22_la_level_outputs_2040_domestic_all_scenarios.csv` → 2022; `fes22_la_level_outputs_2045_domestic_all_scenarios.csv` → 2022; `fes22_la_level_outputs_2050_domestic_all_scenarios.csv` → 2022
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Silver column counts: every Parquet file of this family carries the same **46** columns: the 36
vendor-derived columns of the widest epoch (5 dimensions, 16 stock and 15 stock-proportion
columns) plus 10 gridflow columns. A stock column an epoch does not have is all null in that
epoch's rows. The three header epochs map to resources as follows: epoch 1 is the 2020 slice
(10 stock and 9 stock-proportion columns), epoch 2 is the 2025 slice (adds BioLPG boiler,
biomass boiler and two hybrid technologies), and epoch 3 is the 2030 to 2050 slices (adds the
hydrogen boiler and the hybrid with a hydrogen boiler).

**Two clocks.**

- **Vintage clock: `ckan_last_modified`.** `published_at` is the CKAN `last_modified` of the
  captured file and `available_at` equals it (ADR-030). For this family the seven values run
  from `2022-08-31T07:33:03.509314` (2020 slice) to `2022-08-31T07:38:37.918963` (2050 slice).
  Point-in-time use: `WHERE available_at <= :as_of`. An `as_of` before 2022-08-31 returns no
  domestic rows. The CKAN timestamp is a conservative proxy for the date NESO made the file
  available, and nothing finer. The package itself was created in CKAN on 2022-03-09, earlier
  than any of these files.
- **Event clock: none.** The temporal recipe is `none`: `timestamp_utc` is the **capture time**
  (2026-10-08, 10:55:39 to 10:55:57 UTC), and `event_time` is set equal to it on every row. It is not
  an observation time and not a date inside the data. The only time in the data is the
  `projection_year` label, which is a model year, not an event time. Do not use `timestamp_utc`
  to order or window the data by projection year.

**Units (vendor dictionary, FACTS §4.4).** The registry record carries no structured unit for any
column, so the `Vendor unit` column in the schema tables is blank. The dictionary states:

- `stock_*` columns: **number of buildings** using that heating technology.
- `stock_proportion_*` columns: **proportion of buildings** using that technology. The scale is the
  vendor's. gridflow does not multiply or relabel it, and does not call it a percentage.
- `projection_year` (vendor `Year`): a dimension, not a measure. The dictionary calls it the year
  within the FES scenarios, which does not name a stock date (see Holds).
- **Contradiction:** the dictionary describes `stock_oil_boiler` as a **proportion**. It is the
  only stock column so described. The same text is on the live dictionary of the 2050 resource
  ([NESO domestic dictionary](https://www.neso.energy/data-portal/local-authority-level-spatial-heat-model-outputs-fes/fes_22_local_authority_outputs_2050_domestic_all_scenarios)).
  The quantity and unit of that column are unresolved. `TODO: verify`.
- `stock_total` and `stock_totalhps`: the vendor dictionary text for what they total is not in the
  evidence gathered for this page. `TODO: verify`. There is no `stock_proportion_total` column.

Nothing is inferred from a column name or from the size of a value.

**Sentinels and missing values (FACTS g5, §6.3).** The record declares no null token.

- **Blank cells** are kept as **null**. They occur in only four columns: `stock_hybrid_ashp_hydrogen_boiler`,
  `stock_hydrogen_boiler` and their two `stock_proportion_` counterparts. Each has **1,111 blanks
  in the 2030 slice** and **741 blanks in each of the 2035, 2040, 2045 and 2050 slices**. The
  2020 and 2025 slices contain no blank cells. The vendor does not say what a blank means
  (unmodelled, not applicable, not available or something else). Do not read it as zero, as an
  absent technology or as an excluded scenario from where the blanks fall. `TODO: verify`
  (part of the hold).
- The hydrogen columns do not exist in the 2020 and 2025 files, so those rows are all null in
  silver for the same four columns. That null is an absent column, not a vendor blank.
- The whole-cell tokens `-`, `N/A`, `NA` and `n/a` occur zero times in the captured LA bodies.
  There are no text sentinels in the value cells.
- **Zeros are values.** No primary source identifies them as sentinels. They stay as `0.0`.
  Do not treat zero as missing.
- Every non-blank cell casts strictly to float64, and every body `Year` casts to int64, with zero
  failures.

**Geography.** `code_x` holds the authority code and `local_authority` the name, stored as-is.
Every code matches `[ESW][0-9]{8}`. The 2020 slice has **370** distinct codes and every later
slice has **371**. The code-type prefix counts are:

| Prefix | 2020 slice | 2025 to 2050 slices |
|---|---:|---:|
| E09 | 33 | 33 |
| E06 | 55 | 56 |
| E07 | 192 | 192 |
| E08 | 36 | 36 |
| S12 | 32 | 32 |
| W06 | 22 | 22 |

The single difference is the Isles of Scilly (`E06000053`), absent from the 2020 slice. In the
later slices it appears in only two of the four scenarios, so those slices hold 1,482 rows
(370 authorities x 4 scenarios + 2). The codes are GSS-shaped, but no ONS membership validation
was run. The residential dictionary states its geography is Local Authority Districts from
December 2019 ([2024 resource dictionary](https://www.neso.energy/data-portal/local-authority-level-spatial-heat-model-outputs-fes/fes_2024_local_authority_outputs_2050_residential_all_scenarios)).
`TODO: verify` that the domestic table uses the same boundary vintage. Do not join either table
to a later boundary set without a code lookup.

**Identity and selection.** The entity key is `resource_id`, `edition`, `code_x`,
`projection_year`, `scenario` and `sector`. This is a **measured guard key**: every complete body
passed it with zero duplicated rows, including when the authority name is left out of it. No
vendor text declares it as the identity of a row. `TODO: verify` the vendor's own uniqueness
rule. `_latest` is `whole_capture` per `resource_id`: a newer capture of a resource replaces that
resource's previous capture as a whole, and never another resource or edition. No revision rule
between captures of one resource is claimed. The edition map is the seven exact `fes22_...`
file names, each mapped to 2022.

**Activation (2026-10-15, master `06378b9`, PR #125).** Transformed with window 2026-10-08, one
capture per resource and no prior silver: **10,372 rows** (1,480 + 6 x 1,482), equal to the
planned count, with no transform failure for this family. The one recorded failure of the SCN-3
batch is on a WS1 resource. Reconcile `--all --cutoff 2026-10-13` exited 0 over 255 families with
0 gaps, and coverage was clean (gridflow `@.planning/v0.22-RESULTS.md` §SCN-3; RULINGS 838, 839,
842 and 844).

Silver columns beyond the vendor columns: `edition`, `resource_id`, `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id`, `dataset_version` (all timestamps tz-aware UTC; `dataset_version` is `1+e1` on
every row: the registry record version (1) plus the silver engine version (`e1`). It does not
identify the schema epoch). The three schema epochs are numbered 1 to 3 on this page only; no
silver column carries an epoch number. The vendor `Year` becomes `projection_year`.

Bronze: `C:\gridflow-data\bronze\neso_data_portal\fes_la_heat_model_domestic\2026\10\08\`, one raw
CSV and one `.meta.json` per capture, immutable. Silver:
`C:\gridflow-data\silver\neso_data_portal\fes_la_heat_model_domestic\year=2026\month=10\`, one
Parquet file per capture.

### `fes_la_heat_model_residential`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| la_code | `la_code` | string | — | no | — | — |
| Local_Authority | `local_authority` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Sector | `sector` | string | — | no | — | — |
| stock ASHP | `stock_ashp` | float64 | — | no | — | — |
| stock Biofuel boiler | `stock_biofuel_boiler` | float64 | — | yes | — | — |
| stock Biomass boiler | `stock_biomass_boiler` | float64 | — | no | — | — |
| stock Community | `stock_community` | float64 | — | yes | — | — |
| stock DH | `stock_dh` | float64 | — | yes | — | — |
| stock Electric resistive | `stock_electric_resistive` | float64 | — | no | — | — |
| stock Electric storage | `stock_electric_storage` | float64 | — | no | — | — |
| stock GSHP | `stock_gshp` | float64 | — | no | — | — |
| stock Gas boiler | `stock_gas_boiler` | float64 | — | no | — | — |
| stock Hybrid (ASHP + Biofuel boiler) | `stock_hybrid_ashp_biofuel_boiler` | float64 | — | yes | — | — |
| stock Hybrid (ASHP + Electric resistive) | `stock_hybrid_ashp_electric_resistive` | float64 | — | no | — | — |
| stock Hybrid (ASHP + Hydrogen boiler) | `stock_hybrid_ashp_hydrogen_boiler` | float64 | — | no | — | — |
| stock Hydrogen boiler | `stock_hydrogen_boiler` | float64 | — | no | — | — |
| stock Oil boiler | `stock_oil_boiler` | float64 | — | no | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| la_code | `la_code` | string | — | no | — | — |
| Local_Authority | `local_authority` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Sector | `sector` | string | — | no | — | — |
| stock ASHP | `stock_ashp` | float64 | — | no | — | — |
| stock BioLPG boiler | `stock_biolpg_boiler` | float64 | — | yes | — | — |
| stock Biomass boiler | `stock_biomass_boiler` | float64 | — | no | — | — |
| stock Electric resistive | `stock_electric_resistive` | float64 | — | no | — | — |
| stock Electric storage | `stock_electric_storage` | float64 | — | no | — | — |
| stock Fossil fuel communal heating | `stock_fossil_fuel_communal_heating` | float64 | — | yes | — | — |
| stock GSHP | `stock_gshp` | float64 | — | no | — | — |
| stock Gas boiler | `stock_gas_boiler` | float64 | — | no | — | — |
| stock Hybrid (ASHP + BioLPG boiler) | `stock_hybrid_ashp_biolpg_boiler` | float64 | — | yes | — | — |
| stock Hybrid (ASHP + Electric resistive) | `stock_hybrid_ashp_electric_resistive` | float64 | — | no | — | — |
| stock Hybrid (ASHP + Hydrogen boiler) | `stock_hybrid_ashp_hydrogen_boiler` | float64 | — | no | — | — |
| stock Hydrogen boiler | `stock_hydrogen_boiler` | float64 | — | no | — | — |
| stock Low carbon district heating | `stock_low_carbon_district_heating` | float64 | — | yes | — | — |
| stock Oil boiler | `stock_oil_boiler` | float64 | — | no | — | — |

- Entity key: `resource_id`, `edition`, `la_code`, `projection_year`, `pathway`, `sector`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes24_la_level_outputs_2020_residential_all_scenarios.csv` → 2024; `fes24_la_level_outputs_2025_residential_all_scenarios.csv` → 2024; `fes24_la_level_outputs_2030_residential_all_scenarios.csv` → 2024; `fes24_la_level_outputs_2035_residential_all_scenarios.csv` → 2024; `fes24_la_level_outputs_2040_residential_all_scenarios.csv` → 2024; `fes24_la_level_outputs_2045_residential_all_scenarios.csv` → 2024; `fes24_la_level_outputs_2050_residential_all_scenarios.csv` → 2024; `fes25_la_level_outputs_2025_residential_all_scenarios.csv` → 2025; `fes25_la_level_outputs_2030_residential_all_scenarios.csv` → 2025; `fes25_la_level_outputs_2035_residential_all_scenarios.csv` → 2025; `fes25_la_level_outputs_2040_residential_all_scenarios.csv` → 2025; `fes25_la_level_outputs_2045_residential_all_scenarios.csv` → 2025; `fes25_la_level_outputs_2050_residential_all_scenarios.csv` → 2025
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Silver column counts: every Parquet file of this family carries the same **33** columns: 23
vendor-derived columns (5 dimensions plus 18 stock columns, the union of both editions) and 10
gridflow columns. The two header epochs map to editions: epoch 1 is FES 2024 (7 resources, 14
stock columns) and epoch 2 is FES 2025 (6 resources, 14 stock columns). A column the edition's
file does not have is all null in that edition's rows.

**Renamed technology columns.** The two editions share 10 stock columns by name. The rest differ:

| FES 2024 only | FES 2025 only |
|---|---|
| `stock_biofuel_boiler` | `stock_biolpg_boiler` |
| `stock_hybrid_ashp_biofuel_boiler` | `stock_hybrid_ashp_biolpg_boiler` |
| `stock_community` | `stock_fossil_fuel_communal_heating` |
| `stock_dh` | `stock_low_carbon_district_heating` |

The rows pair columns by position in the vendor's list, not by a vendor statement of equivalence.
The vendor dictionaries describe the 2024 `Community` column as fossil-fuel heat networks and
`DH` as low-carbon district heat networks. That supports reading the last two rows as related, but
gridflow does **not** alias them: the column pairs stay separate and a consumer that wants a
single series must choose the mapping and state it. The dictionaries do not establish whether
`Biofuel` and `BioLPG` are the same technology. `TODO: verify` before treating the first two rows
as a rename. The names `Community`, `DH` and `BioLPG boiler` also occur in the domestic table,
and `TODO: verify` whether they mean the same thing there.

**Two clocks.**

- **Vintage clock: `ckan_last_modified`.** `published_at` is the CKAN `last_modified` of the
  captured file and `available_at` equals it (ADR-030). All 13 values fall on **2025-11-25**, from
  `2025-11-25T14:57:39.152279` (FES 2024, 2020 slice) to `2025-11-25T15:10:15.833424` (FES 2025,
  2050 slice). The **FES 2024 and FES 2025 resources therefore share one vintage date**, so the
  clock cannot tell you when each edition was first published, and for FES 2024 it is later than
  the edition itself. An `as_of` before 2025-11-25 returns no residential rows, for either
  edition. The CKAN timestamp is a conservative proxy and nothing finer. `TODO: verify` why the
  FES 2024 resources carry a 2025-11-25 modification time. Point-in-time use:
  `WHERE available_at <= :as_of`.
- **Event clock: none.** The temporal recipe is `none`: `timestamp_utc` is the **capture time**
  (2026-10-08, 10:56 UTC), and `event_time` equals it on every row. It is not an observation time
  and not a date inside the data. The only time in the data is the `projection_year` label, a
  model year.

**Units (vendor dictionary, FACTS §4.5).** The registry record carries no structured unit, so the
`Vendor unit` column is blank. The dictionaries for both editions
([2024](https://www.neso.energy/data-portal/local-authority-level-spatial-heat-model-outputs-fes/fes_2024_local_authority_outputs_2050_residential_all_scenarios),
[2025](https://www.neso.energy/data-portal/local-authority-level-spatial-heat-model-outputs-fes/fes_2025_local_authority_outputs_2050_residential_all_scenarios))
establish that every `stock_*` column is the **number of homes (dwellings) or buildings** using
that heating technology. There are no proportion columns and no total column in this table.
`TODO: verify` whether the unit is dwellings or buildings (the evidence allows both), and
whether it is the same quantity as the domestic table's number of buildings before comparing the
two tables. `projection_year` is a dimension, not a measure.

**Sentinels and missing values (FACTS g5, §6.3).** The record declares no null token. **No
residential resource contains a blank cell.** The record marks the edition-specific columns
nullable because the other edition's file lacks them; those nulls are absent columns (see above),
not vendor blanks. The tokens `-`, `N/A`, `NA` and `n/a` occur zero times. **Zeros are values**:
no primary source identifies a zero as a sentinel or as "technology not modelled". Zeros stay as
`0.0`. Do not treat
zero as missing and do not extrapolate a missing authority or year from them. Every cell casts
strictly to float64, and every body `Year` to int64, with zero failures.

**Geography.** `la_code` holds the authority code and `local_authority` the name, stored as-is.
Every residential resource has **371** distinct codes (the same set as the later domestic
slices; the prefix counts are the table under the domestic family), 4 pathways per slice (5 distinct
names across the two editions: Counterfactual in FES 2024 only, Falling Behind in FES 2025 only)
and one sector, so every slice is a full rectangle of 371 x 4 = 1,484 rows. The vendor dictionary states the
geography is **Local Authority Districts from December 2019**. That the code set matches the
domestic table does not establish that the two tables use the same definitions or stock dates.

**Identity and selection.** The entity key is `resource_id`, `edition`, `la_code`,
`projection_year`, `pathway` and `sector`: a **measured guard key** that every complete body
passed with zero duplicated rows. No vendor text declares it. `TODO: verify` the vendor's own
uniqueness rule. `_latest` is `whole_capture` per `resource_id`, as for the domestic family. The
edition map is the seven exact `fes24_...` file names mapped to 2024 and the six exact
`fes25_...` file names mapped to 2025. A FES 2024 slice and the FES 2025 slice for the same year
are separate resources and separate editions; the FES 2025 edition has no 2020 slice.

**Activation (2026-10-15, master `06378b9`, PR #125).** Transformed with window 2026-10-08, one
capture per resource and no prior silver: **19,292 rows**, equal to the planned count, with no
transform failure for this family: FES 2024 **10,388** (7 x 1,484) and FES 2025 **8,904**
(6 x 1,484). Reconcile and coverage as for the domestic family (gridflow
`@.planning/v0.22-RESULTS.md` §SCN-3; RULINGS 838, 839, 842 and 844).

Silver columns beyond the vendor columns are the same ten as for the domestic family
(`edition`, `resource_id`, `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` = `1+e1`).
The two schema epochs are numbered 1 and 2 on this page only. Bronze:
`C:\gridflow-data\bronze\neso_data_portal\fes_la_heat_model_residential\2026\10\08\`. Silver:
`C:\gridflow-data\silver\neso_data_portal\fes_la_heat_model_residential\year=2026\month=10\`, one
Parquet file per capture.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- Edition-driven: the package holds one set of resources per edition. The domestic (FES 2022)
  resources were last modified on 2022-08-31 and the residential (FES 2024 and FES 2025)
  resources on 2025-11-25. The package-level CKAN `metadata_modified` is
  `2025-11-25T15:10:15.968833`. `TODO: verify` when NESO adds the next edition's resources.
- The package notes also describe 2021 data generated for a thought piece. None of the 20
  resources is named for it, and this page makes no claim about it.
- `TODO: verify` whether NESO revises a published file in place. The captured file names carry no
  version part, so the file name gives no hint.
- Captures to date: one per resource (2026-10-08). No scheduled refresh has run yet, so no
  revision behaviour has been observed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `fes_la_heat_model_domestic`: held: TODO: What stock assessment date does `Year` denote in the FES 2022 domestic outputs, and is it a start- or end-of-year snapshot? Is `stock Oil boiler` a number of buildings or a proportion, as the dictionary states? What does a blank hydrogen or hybrid-hydrogen cell in the 2030-2050 slices mean? (unit E-SEM)
- `fes_la_heat_model_residential`: held: TODO: What exact stock assessment date does `Year` represent in the FES 2024 and FES 2025 residential outputs, and is it a start- or end-of-year convention? (unit E-SEM)

Both families are held by the SCN-3 batch records (RULINGS 838, 839, 842 and 844). No gold view
or model feed is planned for either while the hold stands. Under ruling 66 the site page shows
rows with one caveat per table: "NESO states no count date for each year's stock, oil boiler's
basis, or hydrogen blanks." on the domestic table and "NESO states no count date for each year's
stock." on the residential one. Its chart is gridflow's sum of one residential stock column over
the 371 authorities of one FES 2025 pathway, one bar per modelled year. Unit E-SEM must answer the
questions below before the holds can lift.

**`fes_la_heat_model_domestic` (FES 2022):**

1. **The stock assessment date.** What date does `Year` denote, and is it a start-of-year or an
   end-of-year snapshot? The dictionary's "year within the FES scenarios" does not say.
2. **`stock_oil_boiler`.** Is it a number of buildings, as its heading and its siblings imply,
   or a proportion, as the dictionary states?
3. **Blank hydrogen cells.** What does a blank in the hydrogen boiler or hybrid-hydrogen columns
   (stock and proportion) mean in the 2030 to 2050 slices?

**`fes_la_heat_model_residential` (FES 2024 and FES 2025):**

1. **The stock assessment date.** What exact stock assessment date does `Year` represent in the
   FES 2024 and FES 2025 residential outputs, and is it a start-of-year or end-of-year
   convention? "Year within the FES pathway" does not say.

What the vendor text does establish, and what it does not (FACTS §4, §6.3 and g1):

- The dictionaries establish what each stock column counts (buildings for the domestic table,
  dwellings or buildings for the residential one), that domestic proportions are proportions of
  buildings, and that the residential geography is December 2019 districts.
- They do not give the stock date, the oil-boiler quantity, the meaning of a domestic blank, the
  composition of the totals, or the relation between the renamed FES 2024 and FES 2025 columns.
- Matching-edition model notes or a specific NESO clarification would settle the stock-date
  question.

Until the holds lift:

- Do not join either table to an observed series by `projection_year`, or read `Year` as a dated
  count.
- Do not use either table point-in-time beyond its CKAN `last_modified` vintage, which is a
  conservative proxy and nothing finer. The FES 2024 and FES 2025 resources share one vintage
  date.
- Do not sum across editions, across scenarios or pathways, or across the domestic and
  residential tables.
- Do not read the domestic `stock_oil_boiler` as a count, and do not read a blank as zero.
- Do not alias the renamed residential technology columns.

Related holds in the same batch (gridflow `@docs/neso_data_portal/eligibility.md`): the building
heat model example output (@building-heat-model.md), WS1
(@fes-whole-system-gas-supply-data-table-ws1.md) and WS2
(@fes-whole-system-gas-supply-emissions-data-table-ws2.md) are held E-SEM. Within WS1, the 2024
resource is a resource-level `HOLD` and the 2025 resource is an adjudicated failed capture
(ADR-040 entry, RULINGS 839, `DuplicateEntityKeyError`). The three Resource Adequacy tables are eligible.
