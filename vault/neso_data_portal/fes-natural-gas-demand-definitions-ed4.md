---
source: "neso_data_portal"
package: "fes-natural-gas-demand-definitions-ed4"
dataset_key: "fes_ed4_gas_demand_defs"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-15
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# FES: Pathways to Net Zero – Natural Gas demand definitions Data table (ED4)

This package is the **codebook for NESO's natural-gas demand tables** in the Future Energy
Scenarios (FES) series. The package notes say the FES publish "data tables containing the GB
FES values for natural gas and residential heat demand"; ED4 holds the definitions of the
items in those tables, not projections. Each CSV is one **edition** of the FES (2023, 2024,
2025, and a 2026 file whose name starts `10yo2026`; the 2026 tables are the Ten Year
Outlook). Each file has three columns and no projection years: `Item no.` (a number that
identifies the item), `Description` (the item's name) and `Definition` (what it covers). The
items are the aggregate gas-demand lines (industry, commercial, transport, residential,
electricity generation, shrinkage, hydrogen production, exports, and the peak 1-in-20 day,
plus a total line from 2025). The vendor's own dictionary calls `Item no.` the "Unique Key"
and ties each description to an ED3 data item. See
@30-vendors/neso-data-portal/datasets/fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3.md.

gridflow keeps the four files as **reference rows**: no unpivot, no projection year, no
value. Silver holds **42 rows from 4 resources** (2023: 10 · 2024: 10 · 2025: 11 · 2026: 11).
This family is **eligible** (not held): it carries no numeric measure and no year label, so
the open questions that hold the ED3 and ED7 tables (what a year header denotes, what a blank
projection cell means, the scale of `number`, `uptake` and `stock`) do not apply to it. Those holds still stand on
the ED3/ED7 families; reading an ED4 definition does not settle them (see Holds).

**Edition is a dimension.** Each edition is a separate, complete set of definitions, and the
text of a given item changes between editions (see What changed between editions). Never
merge editions into one codebook, and read a definition against the ED3 file of the same
edition.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Natural Gas demand definitions (ED4) 2023 | CSV | upload | `60a8299f-9ba1-4663-9ece-8005a8a42fa2` |
| Natural Gas demand definitions (ED4) 2024 | CSV | upload | `a014dfba-0728-448a-a2cc-d34fec0703af` |
| Natural Gas demand definitions (ED4) 2025 | CSV | upload | `74485527-6c09-4c1a-bf8c-8569810eb918` |
| Natural Gas demand definitions (ED4) 2026 | CSV | upload | `b5ae9932-2ce9-42f0-a820-15a13f0eedd0` |

There are no DOC, catalogue-only or held resources in this package: all four resources are
CSV and all four are transformed to silver.

### Resource detail

Package `fes-natural-gas-demand-definitions-ed4` (CKAN id
`af30ab4c-eb46-487c-80bd-84a57d7d5f18`) has **4 resources** in the 2026-10-06 catalogue
snapshot (all CSV, all `url_type: upload`). `last_modified` is the CKAN value in that
snapshot. Download links are the snapshot's resource URLs; `size` is null in the snapshot, so
the byte counts below are from the captured bronze bodies.

| Edition | Disposition | File | Bytes | Raw data rows | CKAN `last_modified` | Download |
|---|---|---|---:|---:|---|---|
| 2023 | SILVER | `fes2023_ed4_v001.csv` | 1,515 | 10 | 2023-07-10T03:31:27.976626 | [CSV](https://api.neso.energy/dataset/af30ab4c-eb46-487c-80bd-84a57d7d5f18/resource/60a8299f-9ba1-4663-9ece-8005a8a42fa2/download/fes2023_ed4_v001.csv) |
| 2024 | SILVER | `fes2024_ed4_v001.csv` | 1,570 | 10 | 2024-07-15T06:40:17.398169 | [CSV](https://api.neso.energy/dataset/af30ab4c-eb46-487c-80bd-84a57d7d5f18/resource/a014dfba-0728-448a-a2cc-d34fec0703af/download/fes2024_ed4_v001.csv) |
| 2025 | SILVER | `fes2025_ed4_v006.csv` | 2,062 | 11 | 2025-12-10T16:56:34.330431 | [CSV](https://api.neso.energy/dataset/af30ab4c-eb46-487c-80bd-84a57d7d5f18/resource/74485527-6c09-4c1a-bf8c-8569810eb918/download/fes2025_ed4_v006.csv) |
| 2026 | SILVER | `10yo2026_ed4_v001.csv` | 2,488 | 11 | 2026-09-16T14:59:52.804239 | [CSV](https://api.neso.energy/dataset/af30ab4c-eb46-487c-80bd-84a57d7d5f18/resource/b5ae9932-2ce9-42f0-a820-15a13f0eedd0/download/10yo2026_ed4_v001.csv) |

- **Edition comes from the file name, corroborated by the resource name.** Each file name and
  its catalogue resource name (`Natural Gas demand definitions (ED4) <year>`) agree on the
  year. gridflow stamps `edition` from the file name (`edition_by_filename`), not from
  `last_modified`, the version token or the capture date.
- **The version token differs by file** (`v001`, `v001`, `v006`, `v001`), which shows NESO
  re-uploads files under the same slot (the 2025 file is at `v006`). The vendor publishes no
  revision policy; `TODO: verify` whether a published edition is revised in place.
- **The catalogue tags and title are stale.** The package still carries the tag `FES2023`,
  and the 2023 and 2024 resource descriptions say the tables cover "natural gas and
  residential heat demand" while the 2025 and 2026 descriptions say "natural gas demand".
  gridflow reads edition from the file name, so none of this is used.

## Families

### `fes_ed4_gas_demand_defs`

- Kind: tabular · archetype: SCN · refresh: adhoc · empty allowed: no

Schema, epoch 1 (one header, identical in all four files):

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Item no. | `item_no` | int64 | — | no | — | — |
| Description | `description` | string | — | no | — | — |
| Definition | `definition` | string | — | no | — | — |

Silver also carries the standard provenance columns written to every silver row: `edition`
(int64), `resource_id`, `timestamp_utc`, `published_at`, `available_at`, `event_time`,
`bronze_capture_id`, `capture_written_at`, `source_run_id`, `dataset_version` (the value is
`1+e1` on every row: record version 1, epoch 1). None is null in any column.

- Entity key: `resource_id`, `edition`, `item_no`
- Latest: `whole_capture` per `resource_id`
- Edition: `fes2023_ed4_v001.csv` → 2023; `fes2024_ed4_v001.csv` → 2024; `fes2025_ed4_v006.csv` → 2025; `10yo2026_ed4_v001.csv` → 2026
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### Shape and counts

Each resource is exactly one header epoch and exactly one edition. Counts are from the
2026-10-08 silver (matching the activation receipt, RULINGS 833) and the pre-merge profile.

| Edition | Resource | Raw data rows | Silver rows | `item_no` range | Cells with an embedded newline | Cells with a comma |
|---|---|---:|---:|---|---:|---:|
| 2023 | `60a8299f-…` | 10 | 10 | 1–10 | 0 | 6 |
| 2024 | `a014dfba-…` | 10 | 10 | 1–10 | 0 | 6 |
| 2025 | `74485527-…` | 11 | 11 | 1–11 | 1 | 2 |
| 2026 | `b5ae9932-…` | 11 | 11 | 1–11 | 0 | 4 |
| | **Total** | **42** | **42** | | | |

Every file decodes strictly as UTF-8; the 2024 file starts with a byte-order mark, which the
reader handles. Every `item_no` casts to int64 and is unique within each file (zero duplicate
keys); no blank row occurs in any ED4 file, so raw rows equal silver rows. The one embedded
newline is in the 2025 item 10 definition.

#### Items

The same ten items run through all four editions in the same order (item numbers 1–10), with
an eleventh total line added from 2025. Labels are as published, including the trailing space
that items 7 and 8 carry in every edition (kept, not trimmed). Definitions are summarised
here, not quoted; read the silver `definition` text for the exact wording.

| `item_no` | `description` (as published) | What the definition says (summary) |
|---:|---|---|
| 1 | Annual end-use gas demand from industry | Gas used in industry, including gas for electricity generation by distribution-connected CHP and CCGT plants, and industrial gas use fitted with carbon capture |
| 2 | Annual end-use gas demand from the commercial sector | Commercial-sector gas, excluding gas burnt for electricity by peaking/flexible plants |
| 3 | Gas end-use demand for transport | Transport-sector gas, including networked CNG and non-networked LNG |
| 4 | Total end-use residential gas demand | Residential gas, including heating and cooking (NDM1 load band) |
| 5 | Total gas demand (gas NTS connected only) for electricity generation | Gas for power stations connected to the gas transmission network |
| 6 | LDZ connected peaking/flexible plants (estimated) | Gas for electricity generation by flexible/peaking plants on the distribution networks |
| 7 | Total (NTS+LDZ) gas shrinkage | Gas shrinkage from the transmission and distribution networks |
| 8 | Hydrogen Production - Natural Gas Demand (2023, 2024) · Hydrogen Production: Natural Gas Demand (2025, 2026) | Gas used to produce hydrogen by steam methane reforming (the 2026 text adds auto thermal reforming) |
| 9 | Gas exported from GB | Gas export to Ireland and Continental Europe |
| 10 | Total GB Peak 1-in-20 Demand | Total daily GB gas demand on a cold day expected once every 20 years (see Peak item and gas year) |
| 11 | Total GB Gas Demand (Excluding exports and shrinkage) (2025, 2026 only) | A sum of other items, given as a formula (see What changed between editions) |

The item 8 description label changes punctuation between 2024 and 2025 (hyphen to colon);
that is the only description label that differs across editions.

#### What changed between editions

- **Item 11 appears from 2025.** Its definition is a formula over item numbers, not prose:
  the 2025 file sums items 1, 2, 3, 4, 5, 6 and 8; the 2026 file sums items 1, 2, 4, 5, 6 and
  8. The numbers refer to `item_no` within the same edition. gridflow stores the formula as
  published and does not evaluate it.
- **Item 3 (transport) is not additive in 2026.** The 2026 definition says transport mixes
  non-networked LNG and networked CNG, so it must not be added to the other components to get
  total networked gas demand, because the networked part is counted inside commercial demand
  (item 2). The 2026 item 11 formula omits item 3 while the 2025 formula includes it, which is
  consistent with that definition. Do not carry the 2025 formula over to a 2026 table.
- **Item 5, electricity generation, 2026.** The 2026 definition says the outlook now
  includes additional gas demand for gas-fired power generation that is likely to arise from
  electricity-network constraints, that the earlier (2025) ten-year forecast did not include
  it in the annual gas demands in the data workbook, and that the earlier forecast for power
  generation is therefore **not directly comparable** with the 2026 Ten Year Outlook. Do not
  line up item 5 across the 2025 and 2026 editions as one series. The 2026 text is inconsistent
  within itself about which earlier forecast it means: one sentence calls the excluded forecast
  "FES 2026 10 Year Forecast" and the next calls it "FES25 10 Year Forecast". `TODO: verify`
  with NESO which edition it means.
- **Wording revisions.** Definitions of the other items are reworded between editions
  (spelling corrections, expanded abbreviations, added cross-references such as "see item no.
  6"). gridflow keeps each edition's text as published and does not diff them.

#### Peak item and gas year

Item 10, `Total GB Peak 1-in-20 Demand`, is defined in every edition as a daily demand on a
1-in-20 cold day and states that its data are in **gas years**: the label year is the year in
which the gas year **starts in October**, so a label of 2022 is gas year 2022/23, running
1 October 2022 to 30 September 2023 (the 2023 and 2024 files use 2022 as the example; the
2025 and 2026 files use 2023, gas year 2023/24). This statement applies to **that item
only**. It does not make the annual gas or heat measures in ED3 or ED7 gas-year or
October-start measures; their year semantics are held (see Holds).

The 2025 definition of item 10 adds that one input to the peak-day analysis is a forecast of
gas demand for power generation which, unlike the rest of FES modelling (which assumes
unconstrained networks), includes an estimate of extra gas-fired generation arising from
electricity-network constraints. The 2026 item 10 text does not repeat it; the 2026 item 5
text carries a related network-constraint statement (above).

The unit of the peak value is the `units` column of the ED3 row, not anything in ED4. In the
captured ED3 combined files the peak item is labelled `GWh` in the 2023 file and `GWh/day` in
the 2024 file and in the later gas-summary files. gridflow keeps the unit as published and
does not rewrite it. See the ED3 page.

#### Silver sample

Two silver rows from the 2025 edition (provenance columns omitted; the vendor `definition` is
truncated here for the page and is longer in silver):

```python
[
    {"edition": 2025, "item_no": 4, "description": "Total end-use residential gas demand",
     "definition": "Gas used in the residential sector, including for heating and cooking (using NDM1 gas load band)."},
    {"edition": 2025, "item_no": 11, "description": "Total GB Gas Demand (Excluding exports and shrinkage)",
     "definition": "= 1+2+3+4+5+6+8"},
]
```

#### Clocks

Two clocks, separate and not to be mixed (ADR-030, ADR-042):

1. **Vintage (`published_at` = `available_at`):** the CKAN `last_modified` of the captured
   resource. It is when NESO last changed that file, not when the vendor wrote the
   definitions. Verified in silver: `published_at` equals `available_at` on every row.
   - 2023: 2023-07-10T03:31:27.976626Z
   - 2024: 2024-07-15T06:40:17.398169Z
   - 2025: 2025-12-10T16:56:34.330431Z
   - 2026: 2026-09-16T14:59:52.804239Z
2. **Event time:** the temporal recipe is **`none`**. These are reference definitions with
   no dated instant, so there is no row-level event time. `timestamp_utc` (and `event_time`,
   which equals it on every row) is the **capture time** of the bronze file, here 2026-10-08
   10:54:18 UTC (2023), 10:54:21 (2024), 10:54:24 (2025) and 10:54:27 (2026). It carries no
   information about the period a definition applies to.

`edition` is stamped from the file name, independent of both clocks; it is not an issue time.
Point-in-time queries bound `available_at <= as_of` per capture; that bound is on the
vintage clock, not on the capture time. Every file was captured on 2026-10-08, after its
`last_modified`, so `available_at <= as_of` does not prove that the bytes held now were the
bytes NESO published by then (ADR-039); `TODO: verify` whether NESO edits a file in place
without bumping `last_modified`. Nothing here shows it either way.

#### Units

None. ED4 has no numeric measure column and no unit column. `item_no` is an **identifier**,
not a measure: do not sum, average or chart it, and do not give it a physical unit. A
definition may name a quantity, but a unit is taken only from the vendor dictionary, never
inferred from a description. The unit of an ED3 or ED7 value is the `units` column of that
row, as published. Those labels are not all physical units: the 2023/2024 combined table uses
`number` and `uptake` alongside TWh, GW, GWh and GWh/day, and the 2025/2026 ED7 heat table
uses `uptake` and `stock` alongside TWh and GW. The scale, basis and denominator of `number`,
`uptake` and `stock` are undocumented, so they are held on the ED3 and ED7 pages (unit
E-SEM); do not convert them or treat them as physical quantities. ED4 itself carries none of
these labels.

#### Missing values and sentinels

- **No sentinels.** The tokens `-`, `N/A`, `NA`, `n/a` (and `#N/A`, `NULL`, `null`, `NaN`)
  occur zero times as a whole cell in any ED4 file. There is no null-token rule and no
  whitespace trim on cell values. Silver has no null in any column. The word `N/A` in a
  vendor dictionary page is metadata, not a body sentinel.
- **No numeric zeros or blank projection cells.** The "blank projection cells are null,
  zeros are values" rule of the other SCN pages has nothing to apply to here: there are no
  projection cells.

#### Join to ED3

ED4 is the codebook for the ED3 natural-gas summary. The join is on **edition and label**,
not on a numeric key:

- ED3 has no `item_no` column, so the link is the `description` text. Measured on 2026-10-08
  silver labels only (no ED3 values read): in both 2025 and 2026, all 11 distinct ED4
  `description` labels equal the 11 distinct `description` labels of the same-edition ED3
  natural-gas summary exactly (11 of 11, no trimming needed). For 2023 and 2024 the ED3
  descriptions sit inside the combined gas-and-heat table and the match was not measured;
  `TODO: verify` before treating ED4 as a complete key to the 2023 and 2024 ED3 gas rows.
- Join on edition: an ED4 row of one edition describes the ED3 file of the same edition. Do
  not apply a 2025 definition to 2023 data.
- The ED3/ED7 package holds three tables: the 2023/2024 combined gas and residential heat
  summary, the 2025/2026 natural-gas summary (ED3) and the 2025/2026 heat-demand summary
  (ED7). The later two split the earlier one, but not row for row. ED4 defines the gas items
  only; it does not define ED7 technology rows. **Aggregate gas demand and technology-level
  heat demand are never added, and editions are never summed.** Any reconciliation needs
  same-edition coverage, unit and aggregation rules from NESO.
- `scenario` and `pathway` are separate columns in the ED3/ED7 silver (2023 and 2026 files
  say Scenario, 2024 and 2025 say Pathway); they are never merged. ED4 has neither column.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

One CSV per annual FES edition, so a new resource appears about once a year (editions in the
snapshot: 2023, 2024, 2025, 2026). Each resource was captured once, on 2026-10-08. Package
`metadata_modified` in the 2026-10-06 snapshot is 2026-09-16T14:59:52.869392. The registry
captured each resource once, so a change to a published file's `last_modified` between
captures has not been observed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

The package is `eligible` in the registry and the family is eligible in the eligibility
report (gridflow `@docs/neso_data_portal/eligibility.md`). This is a reference record with no
temporal meaning, so the year-period and blank-cell questions do not arise here. The ED3 and
ED7 families it describes **are held** (unit E-SEM) and stay held; nothing in an ED4
definition resolves them. The ED3 and ED7 pages carry the hold questions. Residual items on
ED4 itself, none of them a hold:

1. **Vendor uniqueness.** Settled: the vendor dictionary calls `Item no.` the "Unique Key"
   and every file has zero duplicate item numbers, so the entity key rests on a
   vendor-declared identity (plus `resource_id` and `edition` for provenance).
2. **Comparability of item 5 across 2025 and 2026.** The vendor warns the 2026 electricity
   generation gas demand is not comparable with the earlier forecast (see What changed
   between editions). Preserve edition labels; do not splice the two editions.
3. **Join completeness for 2023 and 2024.** See Join to ED3.

No gold view or gridflow_models consumer reads this family; it appears only in the registry
record, `_frozen_keys.json` and the `config/sources.yaml` ingest schedule (RULINGS 555: no
gold feed for the docs wave of this package).

## Links

- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/fes-natural-gas-demand-definitions-ed4.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- Reader: gridflow `@src/gridflow/silver/csv_bronze.py`
- ADRs: gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (clocks),
  `@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md` (records and holds),
  `@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md` (per-resource `_latest`),
  `@docs/DECISION_LOG/ADR-042-neso-scenario-unpivot-and-edition.md` (edition)
- Sibling (the tables these definitions explain, held): @30-vendors/neso-data-portal/datasets/fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3.md
- Package page: [NESO Data Portal – ED4](https://www.neso.energy/data-portal/fes-natural-gas-demand-definitions-ed4)
- Vendor README: @../README.md
