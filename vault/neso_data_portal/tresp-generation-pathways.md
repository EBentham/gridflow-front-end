---
source: "neso_data_portal"
package: "tresp-generation-pathways"
dataset_keys: ["tresp_generation_pathways_gsp", "tresp_generation_pathways_la_england", "tresp_generation_pathways_la_scotland", "tresp_generation_pathways_la_wales", "tresp_generation_pathways_resp_region"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: tRESP generation pathways
  summary: >-
    NESO's projected installed generation and storage capacity, 23 building blocks by area and
    year to 2050, for distribution network planning.
  facts:
    vendor: "NESO Data Portal: five pathway CSVs, one per geography"
    cadence: "Ad hoc (NESO); files last modified 30 January 2026, as at 6 October 2026"
    grain: "One row per building block, area, pathway and year: MW installed at 31 March"
    history: "NESO created the package, version 1.0, on 28 January 2026"
  landscape: power
  what_it_is: >-
    The transitional Regional Energy Strategic Plan (tRESP) is, NESO says, "the first output from
    NESO's Regional Energy Strategic Plan (RESP) team". Its pathways give installed MW at 31 March
    for 23 generation and storage blocks, one pathway to 2035, then three to 2050, by RESP region,
    GSP area and local authority.
  how_used:
    - "NESO says DNOs will use it for their ED3 plans, 2028 to 2033"
    - "Regional solar, wind and battery capacity paths for long-horizon scenario models"
    - "Compare a region's installed MW across the three pathways after 2035"
  chart:
    type: bar
    silver: neso_data_portal/tresp_generation_pathways_resp_region
    value: value
    filter:
      - {column: building_block_id, op: eq, value: Gen_BB012}
      - {column: pathway, op: eq, value: "tRESP - HT"}
      - {column: projection_year, op: in, value: [2025, 2030, 2035, 2040, 2045, 2050]}
    dedup: {"on": [resource_id, building_block_id, resp_region, pathway, projection_year], order_by: capture_written_at}
    group: projection_year
    aggregation: sum
    sort: label
    unit: MW
  chart_view:
    title: Large solar capacity projected, tRESP Holistic Transition, 2025 to 2050
    caption: >-
      Silver `tresp_generation_pathways_resp_region`, block `Gen_BB012` (solar, 10 kW and over),
      pathway `tRESP - HT`, projected MW installed at 31 March, summed over every RESP nation and
      region, every fifth year. Two other pathways branch from it at 2035.
    alt: >-
      Horizontal bar chart of projected large solar (block Gen_BB012) installed at 31 March under the tRESP
      Holistic Transition pathway, in MW, summed over the RESP nations and regions, one bar every
      fifth year: 2025 12,778; 2030 28,738; 2035 44,345; 2040 55,089; 2045 60,905; 2050 64,451.
      Capacity grows about fivefold, fastest before 2035.
    key:
      - {series: value, label: Large solar, codes: Gen_BB012, paint: chartreuse, note: "NESO's block for solar of 10 kW and over (G99)"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the table's file downloaded whole, unless
      its `last_modified` is unchanged. Dates select nothing; silver keeps every capture.
    commands:
      - {run: gridflow ingest neso_data_portal tresp_generation_pathways_resp_region --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal tresp_generation_pathways_resp_region --last 24h, comment: "the capture's date to silver"}
      - {run: gridflow pipeline neso_data_portal tresp_generation_pathways_gsp --last 24h, comment: "the GSP file, both steps"}
  record:
    select:
      filter:
        - {column: building_block_id, op: eq, value: Gen_BB012}
        - {column: resp_region, op: eq, value: South_west}
        - {column: projection_year, op: in, value: [2025, 2034, 2035, 2036]}
      dedup: {"on": [resource_id, building_block_id, resp_region, pathway, projection_year], order_by: capture_written_at}
      order_by: [projection_year, pathway]
      columns: [building_block_id, resp_region, pathway, projection_year, value, unit, resource_id,
                published_at, timestamp_utc]
    key: [building_block_id, resp_region, pathway, projection_year, resource_id]
    caption: "South West large solar around 2035, where one pathway becomes three; 2035 appears under each."
    fields:
      building_block_id: "Block id; all 23 match a Future Energy Scenarios (FES) id; definitions not compared"
      resp_region: "RESP nation or region, in NESO's spelling, such as `South_west` or `Wales`"
      pathway: "Holistic Transition (HT) to 2035, then also Electric Engagement (EE) and Hydrogen Evolution (HE)"
      projection_year: "Year the value is for: MW installed at 31 March, per NESO"
      value: "MW; vehicle-to-grid (`Srg_BB005`) is zero or negative, no sign stated; FES: \"MW availability\""
      unit: "Unit text; NESO's dictionary defines it as \"Capacity installed (MW)\""
      resource_id: "CKAN file id; with block, region, pathway and year, the entity key"
      published_at: "NESO's last-modified time for the file, read as UTC"
      timestamp_utc: "When gridflow captured the file, UTC; the table has no event time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, which here is the capture time, so these cells use
      `data.sql()` on the `_latest` views, naming the vendor columns to leave lineage out.
    cells:
      - |
        solar = data.sql("""
            SELECT pathway, projection_year, SUM(value) AS mw
            FROM silver_neso_data_portal_tresp_generation_pathways_resp_region_latest
            WHERE building_block_id = 'Gen_BB012'
            GROUP BY pathway, projection_year
        """)
        wide = solar.pivot(index="projection_year", columns="pathway", values="mw")
        wide.loc[2033:2037].round(1)
      - |
        ax = wide.plot(figsize=(8, 3.5), color=["#155A6E", "#8A9A2B", "#B5651D"],
                       xlabel="year, installed at 31 March", ylabel="large solar, MW, all regions");
      - |
        gsp = data.sql("""
            SELECT pathway, SUM(value) AS gsp_mw
            FROM silver_neso_data_portal_tresp_generation_pathways_gsp_latest
            WHERE building_block_id = 'Gen_BB012' AND projection_year = 2050
            GROUP BY pathway
        """).set_index("pathway")
        gsp.join(wide.loc[2050].rename("region_mw")).round(1)
    needs: NESO's tRESP generation files by RESP region and GSP area
    plot_alt: >-
      Line plot of projected large solar (block Gen_BB012) installed at 31 March, MW, summed over the RESP
      regions, 2025 to 2050. One line rises from 12,778 in 2025 to 44,345 in 2035, then three:
      Holistic Transition reaches 64,451 in 2050, Electric Engagement 56,903 and Hydrogen
      Evolution 56,546.
  related:
    - {dataset: neso_data_portal/tresp-demand-pathways, note: "The demand blocks, the block list and the GSP area names"}
    - {dataset: neso_data_portal/gis-boundaries-for-gb-grid-supply-points, note: "NESO's GSP boundaries and lookup; tRESP draws its own GSP areas"}
    - {dataset: neso_data_portal/gis-boundaries-for-gb-dno-license-areas, note: "Boundaries of the DNO licence areas the GSP pathway file names"}
  family:
    slug: tresp-generation-pathways
    members:
      - dataset: tresp_generation_pathways_resp_region
        differs: "Per RESP nation and region, the coarsest geography"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=tresp-generation-pathways"
          - "GET https://api.neso.energy/dataset/7f30dbc0-5d71-412a-b4f3-7e852ff7dfa7/resource/f295b8b5-8022-433d-b07f-b75b729fb199/download/tresp_pathways_generation_storage_by_resp_region_published.csv"
      - dataset: tresp_generation_pathways_gsp
        differs: "Per tRESP GSP area (`tresp_gsp_area`; GSP group in Scotland), with `dno_licence_area`"
        request: "GET https://api.neso.energy/dataset/7f30dbc0-5d71-412a-b4f3-7e852ff7dfa7/resource/970b7a25-6086-4b07-b109-b01ae43ae78c/download/tresp_pathways_generation_storage_published.csv"
      - dataset: tresp_generation_pathways_la_england
        differs: "Indicative, per English local authority: ONS `lad24cd` and `lad24nm` at 31 December 2024"
        request: "GET https://api.neso.energy/dataset/7f30dbc0-5d71-412a-b4f3-7e852ff7dfa7/resource/d20aec73-01df-486d-a1aa-390c9cab2976/download/la_england_pathways_generation_storage_published.csv"
      - dataset: tresp_generation_pathways_la_scotland
        differs: "Indicative, per Scottish local authority: ONS `lad24cd` and `lad24nm` at 31 December 2024"
        request: "GET https://api.neso.energy/dataset/7f30dbc0-5d71-412a-b4f3-7e852ff7dfa7/resource/38379002-1fcf-461a-beb1-2b15b555f994/download/la_scotland_pathways_generation_storage_published.csv"
      - dataset: tresp_generation_pathways_la_wales
        differs: "Indicative, per Welsh local authority: ONS `lad24cd` and `lad24nm` at 31 December 2024"
        request: "GET https://api.neso.energy/dataset/7f30dbc0-5d71-412a-b4f3-7e852ff7dfa7/resource/62275682-ed2c-44e8-aede-8404b19f3d67/download/la_wales_pathways_generation_storage_published.csv"
---

# Transitional Regional Energy Strategic Plan (tRESP) - Generation Pathways

NESO's **tRESP generation and storage pathways**: projected installed capacity, in MW, of 23
distributed generation and storage technologies ("building blocks") for each year 2025 to 2050,
under three pathways, cut five ways by geography. tRESP is the Transitional Regional Energy
Strategic Plan, NESO's bridge from existing distribution planning to the full Regional Energy
Strategic Plan (RESP) approach, and its pathways inform DNO network planning. They are tRESP
adaptations of the Future Energy Scenarios (FES) pathways, not interchangeable FES-edition
outputs (gridflow `@.planning/phases/v0.22-K-SCN-1/K-SCN-1-FACTS.md` §SCN-1a). The package holds
five CSVs, one per geography: per Grid Supply Point (GSP) area, per RESP nation and region, and
per local authority for England, Scotland and Wales. All five share one long layout (building
block, geography, pathway, year, unit, value). The GSP file also carries the DNO licence area.
The question these files answer is where, and how fast, NESO's planning scenarios put distributed
generation and storage capacity (solar, onshore wind, CHP, batteries, vehicle-to-grid and so on)
over the next 25 years. In a model they are a slow-moving structural input for regional
capacity, not a forecast of output or price. They suit scenario analysis and long-horizon
capacity features (@../../../20-domain/modelling/renewable-and-demand-forecasting.md), and need
the point-in-time handling in @../../../20-domain/modelling/point-in-time-correctness.md.

The pathways are **projections, not time series of observations**. The three pathways are:

| Body value | Vendor meaning | Year labels in the capture |
|---|---|---|
| `tRESP - HT` | Holistic Transition | 2025 to 2050 |
| `tRESP - EE` | Electric Engagement | 2035 to 2050 |
| `tRESP - HE` | Hydrogen Evolution | 2035 to 2050 |

NESO describes one short-term HT pathway that branches into the three long-term pathways. The
boundary year 2035 therefore appears under all three pathways. That is by design, not a duplicate
to remove. Pathway meanings are from NESO's package pages ([generation package](https://www.neso.energy/data-portal/tresp-generation-pathways),
[demand package](https://www.neso.energy/data-portal/tresp-demand-pathways)), as cited in the
FACTS file. All five generation families are **eligible and published to silver**. Nothing in
this package is held. The sibling demand package is a different matter: its five pathway families
are held (unit E-SEM) on a question about the annual-energy interval (see the Holds section).
This page does not cover demand (@tresp-demand-pathways.md).

- Publisher group: Generation
- Registry group: generation · archetype: SCN

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| tRESP Generation Pathways per Grid Supply Point Area | CSV | upload | `970b7a25-6086-4b07-b109-b01ae43ae78c` |
| tRESP Generation Pathways per RESP Nation and Region | CSV | upload | `f295b8b5-8022-433d-b07f-b75b729fb199` |
| tRESP Indicative Generation Pathways per Local Authority for England | CSV | upload | `d20aec73-01df-486d-a1aa-390c9cab2976` |
| tRESP Indicative Generation Pathways per Local Authority for Scotland | CSV | upload | `38379002-1fcf-461a-beb1-2b15b555f994` |
| tRESP Indicative Generation Pathways per Local Authority for Wales | CSV | upload | `62275682-ed2c-44e8-aede-8404b19f3d67` |

All five resources are SILVER. The package has no DOC, GIS, COVERED or HOLD resource and no
`_files` family (gridflow `@docs/neso_data_portal/eligibility.md`). The geography GIS files and
the building-block and GSP-name workbook that go with tRESP are published in the **demand**
package, not this one. Each file below is a plain upload, `url_type: upload`. The stable handle
is the resource id. Every file is one CSV with one header epoch and one capture to date
(2026-10-08), whose CKAN `last_modified` is **2026-01-30**. The five CSVs were last modified
within about ten minutes of each other that day.

| Family | Download (as captured) | Bytes | Data rows | CKAN `last_modified` | Captured |
|---|---|---:|---:|---|---|
| `tresp_generation_pathways_gsp` | [tresp_pathways_generation_storage_published.csv](https://api.neso.energy/dataset/7f30dbc0-5d71-412a-b4f3-7e852ff7dfa7/resource/970b7a25-6086-4b07-b109-b01ae43ae78c/download/tresp_pathways_generation_storage_published.csv) | 19,194,150 | 308,154 | 2026-01-30T08:36:50.063067 | 2026-10-08 11:40:10Z |
| `tresp_generation_pathways_resp_region` | [tresp_pathways_generation_storage_by_resp_region_published.csv](https://api.neso.energy/dataset/7f30dbc0-5d71-412a-b4f3-7e852ff7dfa7/resource/f295b8b5-8022-433d-b07f-b75b729fb199/download/tresp_pathways_generation_storage_by_resp_region_published.csv) | 862,604 | 14,674 | 2026-01-30T08:34:24.152349 | 2026-10-08 11:40:26Z |
| `tresp_generation_pathways_la_england` | [la_england_pathways_generation_storage_published.csv](https://api.neso.energy/dataset/7f30dbc0-5d71-412a-b4f3-7e852ff7dfa7/resource/d20aec73-01df-486d-a1aa-390c9cab2976/download/la_england_pathways_generation_storage_published.csv) | 23,829,011 | 394,864 | 2026-01-30T08:31:42.342845 | 2026-10-08 11:40:14Z |
| `tresp_generation_pathways_la_scotland` | [la_scotland_pathways_generation_storage_published.csv](https://api.neso.energy/dataset/7f30dbc0-5d71-412a-b4f3-7e852ff7dfa7/resource/38379002-1fcf-461a-beb1-2b15b555f994/download/la_scotland_pathways_generation_storage_published.csv) | 2,654,428 | 42,688 | 2026-01-30T08:28:56.090445 | 2026-10-08 11:40:18Z |
| `tresp_generation_pathways_la_wales` | [la_wales_pathways_generation_storage_published.csv](https://api.neso.energy/dataset/7f30dbc0-5d71-412a-b4f3-7e852ff7dfa7/resource/62275682-ed2c-44e8-aede-8404b19f3d67/download/la_wales_pathways_generation_storage_published.csv) | 1,766,450 | 29,348 | 2026-01-30T08:27:52.691429 | 2026-10-08 11:40:21Z |

File names and bytes are from the captured sidecars and the FACTS inventory (A-GG, A-GR, A-GE,
A-GS, A-GW). None of the captured file names or resource names carries an annual edition or
version token. gridflow therefore records **no edition** for tRESP (`edition_by_filename` null)
and does not infer one from the publication date or from the FES edition the pathways were built
on. `TODO: verify` the vendor's release or version identifier for tRESP, which a future record
would need if NESO publishes a second tRESP release under a new file.

## Families

All five families share the same record shape: **already long**, so no unpivot. `Year` is read as
an ordinary `int64` column renamed `projection_year`. `Value` is an ordinary `float64`. `Unit`
is kept as a row column. Every column in every family is non-nullable. The record is version 1,
read as strict UTF-8, one header epoch, `dataset_version` `1+e1`. The five families differ only
in their geography column(s). The vendor columns and silver names are in the schema tables below.

**The two clocks (all five families).**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` are the CKAN
   `last_modified` of the captured resource, 2026-01-30 for all five (times in the table above).
   CKAN emits it without an offset and gridflow reads it as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). It is the only clock that says
   when a row could have been known. The as-of cutoff for this package is `available_at`
   (RULINGS 597, reading A). So an as-of date earlier than 2026-01-30T08:27Z sees none of these
   rows, and one on or after 2026-01-30T08:37Z sees all of them. Each file is captured whole.
2. **Event time (temporal recipe `none`).** The record declares no temporal column. The pathway
   file has no timestamp that names an observation instant, so `timestamp_utc` is the **capture
   time**, and `event_time` equals `timestamp_utc` on every silver row (checked 2026-10-10). It
   is **not** the time the capacity applies to. The time the value applies to is the
   `projection_year` column, a plain integer, and is not turned into an instant by gridflow.

**What `projection_year` means.** The vendor dictionary for `Year` reads, in the captured
datastore field information, "the year against which the Pathway value has been provided for,
with volume at 31 March". For installed capacity (every generation row) that dates the value as
the installed MW **at 31 March of the labelled year**. gridflow does not synthesise a date from
it. The year label is shared by the whole row, so joins on a year should be on the integer.
`TODO: verify` whether the vendor's 31 March reading is a calendar-year or a financial-year
convention for any attribute other than installed capacity (the FES methodology document, [tRESP
Pathways Methodology and Detailed Design](https://www.neso.energy/document/376101/download),
contains no `calendar` or `financial` statement in the portion the research checked, SC
`RESEARCH.md`). This matters little for installed MW at a stated date, and it is the open
question that holds the demand package.

**Units.** Only from the vendor dictionary as cited in FACTS (g4). Every generation row has
`Unit` = `MW`, defined by the vendor as **installed capacity** ("Capacity installed (MW)"). The
`Unit` column holds the literal text `MW` on every row of every family. The same unit holds for
all 23 blocks. The block definitions workbook (published in the demand package, silver table
`tresp_building_block_definitions`) gives the unit as "Capacity Installed (MW)" for all of them,
and names each block. gridflow keeps `unit` as a column rather than assigning a scalar unit to
`value`.

**Building blocks (all five families).** 23 distinct `Building_block_id` values. They are not
contiguous (`Gen_BB014`, `Gen_BB017` and `Gen_BB020` to `Gen_BB022` are absent from the body),
and names are from the vendor's block-definitions sheet:

| Block | Technology (vendor sheet) |
|---|---|
| `Gen_BB001`, `Gen_BB002` | Non-renewable CHP, at least 1 MW and under 1 MW |
| `Gen_BB003` | Micro CHP, domestic (G98/G83) including gas |
| `Gen_BB004` | Renewable engines: landfill gas, sewage gas, biogas |
| `Gen_BB005`, `Gen_BB006` | Non-renewable engines, diesel and gas (non-CHP) |
| `Gen_BB007` | Fuel cells |
| `Gen_BB008`, `Gen_BB009` | Open-cycle and combined-cycle gas turbines (non-CHP) |
| `Gen_BB010` | Biomass and energy crops (including CHP, biomass conversions) |
| `Gen_BB011` | Waste incineration (including CHP) |
| `Gen_BB012`, `Gen_BB013` | Solar, large (G99, 10 kW and over) and small (G98/G83, under 10 kW) |
| `Gen_BB015`, `Gen_BB016` | Onshore wind, at least 1 MW and under 1 MW |
| `Gen_BB018` | Hydro (not pumped hydro) |
| `Gen_BB019` | Geothermal |
| `Gen_BB023` | Hydrogen |
| `Srg_BB001` to `Srg_BB005` | Storage: non-domestic batteries, domestic batteries (G98), pumped hydro, other, vehicle-to-grid |

Block IDs are stored as published, with no normalisation. A cross-check by exact ID against the
FES block definitions (FACTS g4) found all 23 generation and storage IDs in the FES 2021 to 2025
definition sheets, 22 of 23 in the 2020 sheet (`Gen_BB023` missing), 22 of 23 in the FES 2020
main table, 21 of 23 in the 2021 main table (`Gen_BB003` and `Gen_BB007` missing), and 23 of 23
in the 2022 to 2025 main tables. Matching IDs do not prove that a definition is unchanged between
FES and tRESP. `TODO: verify` the vendor's correspondence between tRESP and FES block
definitions before joining on block ID across the two.

**Sentinels, zeros, negatives and missing values (FACTS g5).** Every column of every family has
**zero** literal blank, `-`, `N/A`, `NA` or `n/a` cells. No null token is declared. Every `Year`
casts to Int64 and every `Value` to Float64 under strict casting, with no failures, and silver
has no nulls. **Zeros are real values and are kept.** Zeros are very common, because most
technologies are absent from most areas in most years. There is no sentinel convention to
handle. The measured zero counts and longest consecutive zero runs in physical body order are
below. They are observations, not vendor missing-value declarations. `TODO: verify` that NESO
means zero capacity (not "not modelled") when it publishes a zero.

| Family | `value` = 0 (rows) | Longest zero run |
|---|---:|---:|
| `tresp_generation_pathways_gsp` | 158,974 | 3,759 |
| `tresp_generation_pathways_la_england` | 134,498 | 17,182 |
| `tresp_generation_pathways_la_scotland` | 14,794 | 2,305 |
| `tresp_generation_pathways_la_wales` | 8,126 | 1,624 |
| `tresp_generation_pathways_resp_region` | 2,034 | 638 |

**Negative values.** Negative values exist in all five families, and **only** in block
`Srg_BB005` (vehicle-to-grid). The counts are 13,280 (GSP), 17,168 (England), 1,856 (Scotland),
1,276 (Wales) and 638 (RESP region), across all three pathways. The most negative value in the
RESP-region file is on the order of minus 8,400 MW and in the GSP file on the order of minus
1,800 MW. The dictionary's unit for this block is "Capacity installed (MW)", and
no vendor source in the research says what a negative installed capacity means for
vehicle-to-grid (net import, charging, or a sign convention). The block is zero or negative on
every row (the GSP file has 118 exact zeros), never positive. FES's own block definitions
(silver `fes_building_blocks_block_definitions`, checked 2026-10-24) give `Srg_BB005` the unit
"MW availability" in every edition from 2021 on ("MW" in 2020), not installed capacity. This is
not a cast failure.
gridflow does not clip, flip or drop them. `TODO: verify` the sign convention of `Srg_BB005`
before summing storage blocks or computing totals across blocks. Summing `value` across blocks
mixes this block's negatives with positive capacities from the rest.

**Identity and selection (g3).** Every full body has **zero duplicate keys and zero null key
cells** on the vendor-column key (block, geography code, pathway, year). That is the entity key
in the schema tables with `resource_id` added. No NESO text states the composite as a uniqueness
guarantee (the dictionaries describe the dimensions only). `TODO: verify` a vendor-declared
revision key. The consequence is the conservative `_latest` of `whole_capture` per `resource_id`:
the newest capture of a resource wins as a whole, and editions of a resource are never merged
row by row. There is one resource and one capture per family at present, so each silver table
holds exactly one capture.

**Pathway coverage by family** (rows; identical grid in each file, verified from silver):

| Family | HT (2025 to 2050) | EE (2035 to 2050) | HE (2035 to 2050) | Total |
|---|---:|---:|---:|---:|
| GSP | 138,138 | 85,008 | 85,008 | 308,154 |
| England LA | 177,008 | 108,928 | 108,928 | 394,864 |
| Scotland LA | 19,136 | 11,776 | 11,776 | 42,688 |
| Wales LA | 13,156 | 8,096 | 8,096 | 29,348 |
| RESP region | 6,578 | 4,048 | 4,048 | 14,674 |

**Release dating and historical years.** The vintage is 2026-01-30, but the HT pathway starts at
year label 2025, so its 2025 rows are dated 31 March 2025, which is before the vintage. Whether
those rows are modelled starting positions or observed capacity is not stated in the research
evidence. `TODO: verify` this before using the 2025 rows as an observed baseline. A backtest
should treat the whole file as becoming known on 2026-01-30 and should not treat the 2025 rows
as known earlier, whatever they represent.

### `tresp_generation_pathways_gsp`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building_block_id | `building_block_id` | string | — | no | — | — |
| tRESP_GSP_area | `tresp_gsp_area` | string | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Value | `value` | float64 | — | no | — | — |
| Unit | `unit` | string | — | no | — | Capacity installed (MW) |
| DNO_licence_area | `dno_licence_area` | string | — | no | — | — |

- Entity key: `resource_id`, `building_block_id`, `tresp_gsp_area`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Activation (2026-10-10): **308,154** silver rows, equal to the planned count. The geography is
`tRESP_GSP_area`, NESO's tRESP feeding-area identifier, with GSP-group treatment in Scotland.
The file has 231 distinct areas, and the set of 231 codes is exactly the set in the supporting
workbook's GSP-name sheet (silver `tresp_gsp_area_names` in the demand package), with no
unmatched code on either side (FACTS C11). gridflow stores the code as published. It is **not**
evidenced as an EIC code or as an identifier interchangeable with the regional-FES GSP
identifier, so do not join to regional FES on it. `DNO_licence_area` has 14 distinct values
(NGED East Midlands, South Wales, South West and West Midlands; NPg Northeast and Yorkshire;
SP ENW; SPEN Manweb and SPD; SSEN SHEPD and South; UKPN Eastern, London and South East). The
vendor gives no code standard for it. In the 2026-10-08 capture each of the 231 areas carries
exactly one DNO licence area (checked 2026-10-24, silver); no NESO text states it as a rule.

### `tresp_generation_pathways_la_england`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building_block_id | `building_block_id` | string | — | no | — | — |
| LAD24CD | `lad24cd` | string | — | no | — | — |
| LAD24NM | `lad24nm` | string | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Unit | `unit` | string | — | no | — | Capacity installed (MW) |
| Value | `value` | float64 | — | no | — | — |

- Entity key: `resource_id`, `building_block_id`, `lad24cd`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Activation (2026-10-10): **394,864** silver rows, equal to the planned count. Note the column
order differs from the GSP and RESP-region files: `Unit` comes before `Value` here. Select by
name, never by position. `LAD24CD` and `LAD24NM` are the ONS local authority district codes and
names **as at 31 December 2024**, per the vendor dictionary. The file has 296 distinct codes.
Both code and name are kept, and the code is used in identity. The files are labelled
"indicative" by NESO for the local authority cuts. NESO's resource description (catalogue
snapshot `20261006T195819Z`) says why: the pathways "are defined at the larger tRESP GSP area,
and DNOs will disaggregate within those areas to network assets in each local authority", so
the values are "indicative approximate values" and "should not be used as a target for planning".

### `tresp_generation_pathways_la_scotland`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building_block_id | `building_block_id` | string | — | no | — | — |
| LAD24CD | `lad24cd` | string | — | no | — | — |
| LAD24NM | `lad24nm` | string | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Unit | `unit` | string | — | no | — | Capacity installed (MW) |
| Value | `value` | float64 | — | no | — | — |

- Entity key: `resource_id`, `building_block_id`, `lad24cd`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Activation (2026-10-10): **42,688** silver rows, equal to the planned count. 32 distinct
`LAD24CD` codes, ONS as at 31 December 2024. Same header as the England file.

### `tresp_generation_pathways_la_wales`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building_block_id | `building_block_id` | string | — | no | — | — |
| LAD24CD | `lad24cd` | string | — | no | — | — |
| LAD24NM | `lad24nm` | string | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Unit | `unit` | string | — | no | — | Capacity installed (MW) |
| Value | `value` | float64 | — | no | — | — |

- Entity key: `resource_id`, `building_block_id`, `lad24cd`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Activation (2026-10-10): **29,348** silver rows, equal to the planned count. 22 distinct
`LAD24CD` codes, ONS as at 31 December 2024. Same header as the England file.

### `tresp_generation_pathways_resp_region`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Building_block_id | `building_block_id` | string | — | no | — | — |
| RESP_region | `resp_region` | string | — | no | — | — |
| Pathway | `pathway` | string | — | no | — | — |
| Year | `projection_year` | int64 | — | no | — | — |
| Value | `value` | float64 | — | no | — | — |
| Unit | `unit` | string | — | no | — | Capacity installed (MW) |

- Entity key: `resource_id`, `building_block_id`, `resp_region`, `pathway`, `projection_year`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Activation (2026-10-10): **14,674** silver rows, equal to the planned count. 11 distinct
`RESP_region` values, kept in the vendor's spelling and underscore style: Central_england,
East, East_midlands, Greater_london, North_east_and_yorkshire, North_west, Scotland,
South_east, South_west, Wales, West_midlands. The region labels refer to the published RESP
nation and region areas (the boundary GIS file is in the demand package). The vendor dictionary
names no external code standard. `TODO: verify` any code standard for the region labels, and
whether the 11 region boundaries tile Great Britain without overlap as geometry. The values rule
out double counting: the region, GSP and local authority cuts agree at the total (see
"Cross-geography consistency" below), though NESO states no geometry rule.

**Cross-geography consistency.** The five cuts are published as separate files and gridflow
does not reconcile them. NESO's package text says the generation pathways are provided "per
RESP nation and region, as well as on an indicative basis per local authority across Great
Britain". Measured on the 2026-10-08 capture (checked 2026-10-24, silver, all 1,334 block,
pathway and year groups): the 231 GSP areas sum to the 11 RESP regions' total to within 1e-11 MW,
and the three local authority files together sum to the same total to within 0.0004 MW. Within
a nation they do not match: the Scottish local authorities differ from the `Scotland` region by
up to 44.9 MW, the Welsh ones from `Wales` by up to 60.0 MW, and the English file from the nine
English regions by up to 72.2 MW (the three differences net out at the total), consistent with NESO's note
that the local authority values are indicative splits of GSP areas. Treat the regions and GSP
areas as two cuts of one total; do not roll local authorities up to a RESP nation.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad-hoc

The vendor states ad-hoc updates and gives no schedule. The one capture to date (2026-10-08)
shows a CKAN `last_modified` of 2026-01-30, so the files were about eight months old at capture.
Each capture holds only the file as it stood at capture time. gridflow keeps the vintage of each
capture, so a later NESO overwrite of the same resource arrives as a new capture with a new
`available_at`, and the 2026-01-30 vintage stays in silver beside it (separate
`resource_id`/capture, never merged). `TODO: verify` whether NESO overwrites a resource in place
or adds a new resource when it issues a new tRESP release, and the vendor's publication schedule.
Captures to date: one per family, all on 2026-10-08. No scheduled refresh has run yet. Checked
2026-10-24: the 2026-10-16 portal recapture took no tRESP generation file; bronze and silver
hold the 2026-10-08 capture alone.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

All five generation families are **eligible**: single-resource whole-capture records with no
measured structural, cast or uniqueness blocker (FACTS, SCN-1a). Activation (2026-10-10, master
`0bc09a0`, PR #100) transformed all five to silver at cutoff 2026-10-08 with no prior silver, and
the row counts equal the planned counts: 308,154, 394,864, 42,688, 29,348 and 14,674. Reconcile
(`--all`, cutoff 2026-10-08) reported exit 0, 85 families, 0 gaps and 0 stale (gridflow
`@.planning/v0.22-RESULTS.md` §SCN-1a; RULINGS 603, 605, 609, 610). The `TODO: verify` notes in
this page are open vendor questions, not holds. They do not block publication of these current
bodies.

For contrast, the sibling **demand** package (@tresp-demand-pathways.md) holds all five of its
pathway families, unit E-SEM, on one question: what interval the `Year` label covers for the
annual-energy (GWh) building blocks (the financial year to 31 March, the calendar year or
another interval), and which FES definition applies to the suffixed demand IDs. That question
does not apply to installed-capacity MW and does not hold this package. Related points in the
demand package: its old building-block sheet is held on a table-boundary question, and its two
GPKG files are GIS.
