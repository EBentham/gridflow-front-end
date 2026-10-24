---
source: "neso_data_portal"
package: "outturn-voltage-costs"
dataset_keys: ["outturn_voltage_costs_historical", "outturn_voltage_costs_main"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Voltage costs by constraint group
  summary: >-
    NESO's monthly outturn cost of maintaining network voltage, in £m: sync and utilisation costs
    for each of 19 voltage constraint groups.
  facts:
    vendor: "NESO Data Portal, package Voltage System Costs (`outturn-voltage-costs`)"
    cadence: "Monthly, as NESO's catalogue lists it; its October 2026 note says updates are paused"
    grain: One row per settlement month and voltage constraint group
    history: "Financial-year files from April 2014, as NESO's catalogue lists them"
  landscape: market
  what_it_is: >-
    NESO's post-month report of the outturn cost of maintaining voltage levels on the network, per
    voltage constraint group (NESO's voltage requirement areas). Sync costs are balancing mechanism
    and trade costs of running units; NESO notes utilisation costs here are only Obligatory Reactive
    Power Service payments, allocated per group. Each file covers one financial year, so none share a month.
  how_used:
    - "Monthly voltage cost per region, as one line of balancing-cost history."
    - "Which groups drive voltage spend, and whether through sync or utilisation cost."
    - "Place each group on a map from NESO's coordinates column."
  chart:
    type: stacked-area
    silver: neso_data_portal/outturn_voltage_costs_historical
    time: settlement_month
    values:
      - {column: utilisation_costs_gbp_m, series: utilisation}
      - {column: sync_costs_gbp_m, series: sync}
    dedup: {"on": [settlement_month, voltage_constraint_group], order_by: capture_written_at}
    aggregation: sum
    window: {start: "2014-04-01", end: "2025-03-31"}
    unit: "£m"
  chart_view:
    title: Sync and utilisation costs, April 2014 to March 2025
    caption: >-
      Silver `outturn_voltage_costs_historical`, £m: each settlement month's sync and utilisation
      costs summed over NESO's 19 voltage constraint groups and stacked, April 2014 to March 2025.
      The newest file's months are not drawn.
    alt: >-
      Stacked area chart from neso_data_portal/outturn_voltage_costs_historical, in £m per
      settlement month summed over 19 groups, April 2014 to March 2025: utilisation costs below,
      sync costs on top. To March 2021 the total runs from 5.55 in February 2015 to 24.71 in April
      2020, when sync reaches 18.30. Utilisation then climbs to 41.98 in October 2022, when the
      total peaks at 64.60, and falls back to 9.74 to 14.92 in 2024-25. Sync exceeds utilisation
      in 10 months of 2023-24 and peaks at 40.73 in April 2024.
    x_label: settlement month, as NESO labels each row
    key:
      - {series: sync, label: Sync costs, codes: "Sync Costs (£m)", paint: clay, note: "NESO: balancing mechanism and trade costs of running units. Highest 40.73, April 2024."}
      - {series: utilisation, label: Utilisation costs, codes: "Utilisation Costs (£m)", paint: petrol, note: "Obligatory Reactive Power Service payments only (NESO). From 3.91 in February 2020 to 41.98 in October 2022."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each file downloaded whole unless its
      `last_modified` is unchanged. Each financial year is its own file; dates select nothing.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=outturn-voltage-costs"
    commands:
      - {run: gridflow pipeline neso_data_portal outturn_voltage_costs_main --last 24h, comment: "the 2025-26 file"}
      - {run: gridflow pipeline neso_data_portal outturn_voltage_costs_historical --last 24h, comment: "eleven yearly files; also the chart"}
  record:
    select:
      silver: neso_data_portal/outturn_voltage_costs_main
      filter:
        - {column: settlement_month, op: eq, value: "2025-05-01"}
        - {column: voltage_constraint_group, op: in, value: ["Dumfries & Galloway", E ENGLAND, EAST MIDLANDS, S WALES, SE ENGLAND, SOUTH YORKS, SW ENGLAND, W CORRIDOR]}
      dedup: {"on": [settlement_month, voltage_constraint_group], order_by: capture_written_at}
      order_by: [voltage_constraint_group]
      columns: [settlement_month, voltage_constraint_group, sync_costs_gbp_m, utilisation_costs_gbp_m, coordinates, timestamp_utc, published_at]
    key: [settlement_month, voltage_constraint_group]
    caption: "Eight of the 19 groups in May 2025, from NESO's 2025-26 file; zeros as written."
    fields:
      settlement_month: "NESO's month label, written as its first day; it stands for the whole month"
      voltage_constraint_group: "NESO's voltage requirement area, kept exactly as written, mixed case included"
      sync_costs_gbp_m: "Sync costs, £m (NESO's unit): balancing mechanism and trade costs of running units"
      utilisation_costs_gbp_m: "Utilisation costs, £m: per NESO, only Obligatory Reactive Power Service payments, allocated per group"
      coordinates: "NESO's map point for the group, kept as text; NESO states no coordinate system"
      timestamp_utc: "Start of the month's first settlement period, UTC; gridflow's anchor, not a measurement"
      published_at: "NESO's last-modified time for the whole file, read as UTC; one per capture"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote the capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads each file's `_latest` view, filtering `settlement_month`, both ends included.
      Take the month from `settlement_month`; `start_utc` is its first settlement period's start,
      converted from UK time. Files are financial years: stack, never add.
    cells:
      - |
        import pandas as pd
        hist = data.neso_data_portal.query("outturn_voltage_costs_historical", "2024-04-01", "2025-03-31")
        newest = data.neso_data_portal.query("outturn_voltage_costs_main", "2025-04-01", "2025-05-31")
        df = pd.concat([hist, newest], ignore_index=True)
        df["settlement_month"] = pd.to_datetime(df.settlement_month)
        df["start_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
        months = pd.to_datetime(["2024-10-01", "2024-11-01", "2025-03-01", "2025-04-01", "2025-05-01"])
        df[(df.voltage_constraint_group == "SE ENGLAND") & df.settlement_month.isin(months)][["settlement_month", "start_utc", "sync_costs_gbp_m", "utilisation_costs_gbp_m"]]
      - |
        year = df[df.settlement_month < "2025-04-01"]
        by_group = year.groupby("voltage_constraint_group")[["sync_costs_gbp_m", "utilisation_costs_gbp_m"]].sum()
        by_group.assign(total=by_group.sum(axis=1)).sort_values("total", ascending=False).head(6).round(2).reset_index()
      - |
        monthly = df.groupby("settlement_month")[["utilisation_costs_gbp_m", "sync_costs_gbp_m"]].sum()
        monthly.index = monthly.index.strftime("%b %Y")
        ax = monthly.plot.bar(stacked=True, figsize=(8, 3.5), color=["#155A6E", "#C77E3C"],
                              xlabel="settlement month; the last two are from the 2025-26 file",
                              ylabel="£m, summed over the 19 groups")
        ax.legend(["Utilisation costs", "Sync costs"]);
    needs: the historical yearly files and the 2025-26 file
    plot_alt: >-
      Stacked bar plot of each settlement month's utilisation and sync costs, in £m summed over the
      19 groups, April 2024 to May 2025; the last two months come from the 2025-26 file. The total
      falls from 51.28 in April 2024 to 12.76 in February 2025, then rises to 39.94 in May 2025.
      Utilisation stays between 9.74 and 15.27.
  related:
    - {dataset: neso_data_portal/constraint-breakdown, note: "NESO's daily voltage constraint cost: one figure a day, not by group"}
    - {dataset: neso_data_portal/thermal-constraint-costs, note: "Daily thermal constraint costs by group: the other constraint NESO reports"}
    - {dataset: neso_data_portal/obligatory-reactive-power-service-orps-utilisation, note: "The reactive power service whose payments NESO says utilisation costs are"}
    - {dataset: neso_data_portal/voltage-requirement, note: "Planned overnight voltage units per group; no documented key joins the two"}
  family:
    slug: outturn-voltage-costs
    members:
      - dataset: outturn_voltage_costs_main
        differs: "NESO's newest file, 2025-26: April and May 2025 only; updates paused (October 2026)"
        request: "GET https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/073f9ffa-05d5-47e5-8835-e1ac31b7656d/download/voltagecsv-2025_26.csv"
      - dataset: outturn_voltage_costs_historical
        differs: "Eleven financial-year files, 2014-15 to 2024-25; the four newest are listed"
        request:
          - "GET https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/bb3b4ea5-39f4-4fe4-b0e2-5b341908b186/download/voltagecsv-2021_22.csv"
          - "GET https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/81a7db68-0a24-4ce9-a374-f0ffced588b0/download/voltagecsv-2022_23.csv"
          - "GET https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/6165d7d4-54cf-4e47-91e4-b487e8225e5a/download/voltagecsv-2023_24.csv"
          - "GET https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/3eced73f-b7e6-4974-8d3c-3ebd48eba74c/download/voltagecsv-2024_25.csv"
---

# Voltage System Costs

NESO's monthly record of the **outturn cost of maintaining voltage levels on the network**
(vendor wording, captured package notes: the "post monthly report provides outturn system
costs for maintaining voltage levels on the network"). Holding voltage needs the right balance of
reactive power injection and absorption in real time (vendor notes). Each row is one calendar
month for one **voltage constraint group** (a voltage requirement area; the vendor ships a network
diagram of these areas, see DOC below) and carries two costs in millions of pounds: `Sync Costs
(£m)` and `Utilisation Costs (£m)`, plus a `Coordinates` geopoint string for the group. Per the
vendor dictionary, sync costs are the balancing-mechanism and trade costs of running units, and
utilisation costs are the voltage ancillary-service costs. The vendor note adds that the
utilisation costs here are **only the ORPS payments, allocated per voltage constraint group**
(ORPS is the Obligatory Reactive Power Service, named in the registry package
`obligatory-reactive-power-service-orps-utilisation`; `TODO: verify` which payment components
the allocation covers, as the captured vendor text does not spell it out). The package is useful as a regional, monthly history of what
voltage support cost, to be read alongside the thermal constraint costs
(@thermal-constraint-costs.md) and the voltage requirement series (@voltage-requirement.md). It is
**outturn, not a forecast**, and carries no issue or publication column.

**Vendor update pause.** The captured package notes (catalogue snapshot 2026-10-06) say the
dataset update is paused while NESO works on improvements, that the data is "not displaying in
full at present", and that data for all months will be available once the update is complete.
The newest month gridflow holds is 2025-05-01. `TODO: verify` with NESO when updates resume and
whether the months after 2025-05 will arrive as a new resource or as a replacement of the
2025-2026 file.

Neither family is held. Both are eligible and both are on silver.

- Publisher group: Constraint management
- Registry group: constraint-management · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Historical Outturn Voltage Costs 2014-2015 | CSV | upload | `fae5a592-deb4-4c66-8d51-d6ef450ccd95` |
| Historical Outturn Voltage Costs 2015-2016 | CSV | upload | `035ab58a-7b96-4e10-bf51-cf3a7e64f6a0` |
| Historical Outturn Voltage Costs 2016-2017 | CSV | upload | `f9a80c9d-586b-4139-8371-436cc07d1ef3` |
| Historical Outturn Voltage Costs 2017-2018 | CSV | upload | `118a9d4e-17a3-4606-bb30-4ed1d2abe722` |
| Historical Outturn Voltage Costs 2018-2019 | CSV | upload | `27454f2f-591d-4222-a288-cc2f0fcc4250` |
| Historical Outturn Voltage Costs 2019-2020 | CSV | upload | `1b02d2ec-8d0f-4244-9828-9eac5d9c3c67` |
| Historical Outturn Voltage Costs 2020-2021 | CSV | upload | `1b47a532-9f22-49c1-ae2a-d84dcc6d7408` |
| Historical Outturn Voltage Costs 2021-2022 | CSV | upload | `bb3b4ea5-39f4-4fe4-b0e2-5b341908b186` |
| Historical Outturn Voltage Costs 2022-2023 | CSV | upload | `81a7db68-0a24-4ce9-a374-f0ffced588b0` |
| Historical Outturn Voltage Costs 2023-2024 | CSV | upload | `6165d7d4-54cf-4e47-91e4-b487e8225e5a` |
| Historical Outturn Voltage Costs 2024-2025 | CSV | upload | `3eced73f-b7e6-4974-8d3c-3ebd48eba74c` |
| Outturn Voltage Costs 2025-2026 | CSV | upload | `073f9ffa-05d5-47e5-8835-e1ac31b7656d` |

The first eleven resources (financial years 2014-15 to 2024-25) map to the family
`outturn_voltage_costs_historical`. The twelfth, "Outturn Voltage Costs 2025-2026", maps to the
separate family `outturn_voltage_costs_main`. Each resource is one financial-year file; they are
disjoint slices, not revisions of one another.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Network Diagram | PDF | upload | `ec0669de-e67a-4601-831e-3d3f4ed6406e` |

The Network Diagram is a vendor PDF showing the voltage requirement areas (vendor resource
description: "A network diagram of Voltage Requirement Area"). It is retained as documentation
(family `outturn_voltage_costs_files`, catalogue only). It is not parsed and has no silver.

Download links (from the 2026-10-06 catalogue snapshot; the stable handle is the resource id,
not the URL):

| Resource | Download | Captured file | Bytes | Data rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| 2014-2015 | [voltagecsv-2014_15.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/fae5a592-deb4-4c66-8d51-d6ef450ccd95/download/voltagecsv-2014_15.csv) | `raw_20261008T111616Z_fae5a592-deb4-4c66-8d51-d6ef450ccd95_7a56317e.csv` | 14,912 | 228 | `2024-05-24T13:55:17.240734` |
| 2015-2016 | [voltagecsv-2015_16.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/035ab58a-7b96-4e10-bf51-cf3a7e64f6a0/download/voltagecsv-2015_16.csv) | `raw_20261008T111618Z_035ab58a-7b96-4e10-bf51-cf3a7e64f6a0_f95af6ec.csv` | 15,126 | 228 | `2024-05-24T13:56:19.823004` |
| 2016-2017 | [voltagecsv-2016_17.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/f9a80c9d-586b-4139-8371-436cc07d1ef3/download/voltagecsv-2016_17.csv) | `raw_20261008T111621Z_f9a80c9d-586b-4139-8371-436cc07d1ef3_6d27efae.csv` | 15,235 | 228 | `2024-05-24T14:14:50.794083` |
| 2017-2018 | [voltagecsv-2017_18.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/118a9d4e-17a3-4606-bb30-4ed1d2abe722/download/voltagecsv-2017_18.csv) | `raw_20261008T111624Z_118a9d4e-17a3-4606-bb30-4ed1d2abe722_f6256da5.csv` | 15,187 | 228 | `2024-05-24T14:17:30.934760` |
| 2018-2019 | [voltagecsv-2018_19.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/27454f2f-591d-4222-a288-cc2f0fcc4250/download/voltagecsv-2018_19.csv) | `raw_20261008T111626Z_27454f2f-591d-4222-a288-cc2f0fcc4250_7d6913e4.csv` | 15,358 | 228 | `2024-05-24T14:18:45.922196` |
| 2019-2020 | [voltagecsv-2019_20.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/1b02d2ec-8d0f-4244-9828-9eac5d9c3c67/download/voltagecsv-2019_20.csv) | `raw_20261008T111629Z_1b02d2ec-8d0f-4244-9828-9eac5d9c3c67_5b0b2331.csv` | 15,352 | 228 | `2024-05-24T09:56:46.687355` |
| 2020-2021 | [voltagecsv-2020_21.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/1b47a532-9f22-49c1-ae2a-d84dcc6d7408/download/voltagecsv-2020_21.csv) | `raw_20261008T111631Z_1b47a532-9f22-49c1-ae2a-d84dcc6d7408_1f550d55.csv` | 15,501 | 228 | `2024-05-24T09:52:13.103712` |
| 2021-2022 | [voltagecsv-2021_22.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/bb3b4ea5-39f4-4fe4-b0e2-5b341908b186/download/voltagecsv-2021_22.csv) | `raw_20261008T111634Z_bb3b4ea5-39f4-4fe4-b0e2-5b341908b186_0251b8f6.csv` | 15,299 | 228 | `2024-05-24T09:51:14.529174` |
| 2022-2023 | [voltagecsv-2022_23.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/81a7db68-0a24-4ce9-a374-f0ffced588b0/download/voltagecsv-2022_23.csv) | `raw_20261008T111636Z_81a7db68-0a24-4ce9-a374-f0ffced588b0_32365a66.csv` | 15,094 | 228 | `2024-05-24T09:50:05.710366` |
| 2023-2024 | [voltagecsv-2023_24.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/6165d7d4-54cf-4e47-91e4-b487e8225e5a/download/voltagecsv-2023_24.csv) | `raw_20261008T111639Z_6165d7d4-54cf-4e47-91e4-b487e8225e5a_ab60d687.csv` | 15,387 | 228 | `2024-05-24T09:45:06.429818` |
| 2024-2025 | [voltagecsv-2024_25.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/3eced73f-b7e6-4974-8d3c-3ebd48eba74c/download/voltagecsv-2024_25.csv) | `raw_20261008T111641Z_3eced73f-b7e6-4974-8d3c-3ebd48eba74c_b494b559.csv` | 14,973 | 228 | `2025-04-29T15:42:04.442764` |
| 2025-2026 (main) | [voltagecsv-2025_26.csv](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/073f9ffa-05d5-47e5-8835-e1ac31b7656d/download/voltagecsv-2025_26.csv) | `raw_20261008T111645Z_073f9ffa-05d5-47e5-8835-e1ac31b7656d_da93654c.csv` | 2,670 | 38 | `2025-06-23T11:40:39.592575` |
| Network Diagram (DOC) | [network-diagram.pdf](https://api.neso.energy/dataset/8df6dd77-315f-465e-a8d9-ce0492853050/resource/ec0669de-e67a-4601-831e-3d3f4ed6406e/download/network-diagram.pdf) | `raw_20261008T111612Z_ec0669de-e67a-4601-831e-3d3f4ed6406e_f6e7918f.pdf` | 284,629 | n/a | `2020-10-05T15:56:43.491317` |

CKAN `last_modified` values are emitted without an offset and read as UTC (gridflow
`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Every resource is an `upload`.

## Families

### `outturn_voltage_costs_files`

- Kind: files · archetype: SER · refresh: monthly · empty allowed: no
- files: catalogue only

The Network Diagram PDF only. No CSV reader, record, entity key or `_latest` table.

### `outturn_voltage_costs_historical`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Month | `settlement_month` | date | `voltagecsv-2014_15.csv` → `%d/%m/%Y`; `voltagecsv-2015_16.csv` → `%Y-%m-%d`; `voltagecsv-2016_17.csv` → `%Y-%m-%d`; `voltagecsv-2017_18.csv` → `%Y-%m-%d`; `voltagecsv-2018_19.csv` → `%Y-%m-%d`; `voltagecsv-2019_20.csv` → `%Y-%m-%d`; `voltagecsv-2020_21.csv` → `%Y-%m-%d`; `voltagecsv-2021_22.csv` → `%Y-%m-%d`; `voltagecsv-2022_23.csv` → `%Y-%m-%d`; `voltagecsv-2023_24.csv` → `%Y-%m-%d`; `voltagecsv-2024_25.csv` → `%d/%m/%Y` | no | — | — |
| Voltage Constraint Group | `voltage_constraint_group` | string | — | no | — | — |
| Sync Costs (£m) | `sync_costs_gbp_m` | float64 | — | yes | — | £(m) |
| Utilisation Costs (£m) | `utilisation_costs_gbp_m` | float64 | — | yes | — | £(m) |
| Coordinates | `coordinates` | string | — | yes | — | — |

- Entity key: `resource_id`, `settlement_month`, `voltage_constraint_group`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: month (`settlement_month`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

### `outturn_voltage_costs_main`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Month | `settlement_month` | date | `%d/%m/%Y` | no | — | — |
| Voltage Constraint Group | `voltage_constraint_group` | string | — | no | — | — |
| Sync Costs (£m) | `sync_costs_gbp_m` | float64 | — | yes | — | £(m) |
| Utilisation Costs (£m) | `utilisation_costs_gbp_m` | float64 | — | yes | — | £(m) |
| Coordinates | `coordinates` | string | — | yes | — | — |

- Entity key: `settlement_month`, `voltage_constraint_group`
- Latest: `whole_capture`
- Temporal recipe: month (`settlement_month`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**One header, two families.** All twelve CSVs share the same five-column header, so there is a
single header epoch. They are split into two independent families because the date
representation differs by file. The historical family reads each file's `Settlement Month` with an
exact per-filename format map (no fallback): `%d/%m/%Y` for the 2014-15 and 2024-25 files and
`%Y-%m-%d` for the nine between. A file whose name is not in the map fails loudly rather than
being guessed. The main family reads its single file with the scalar `%d/%m/%Y`. The family split is not a vendor distinction: the 2024-25 file is still labelled "Historical"
by the vendor and the 2025-2026 file is not. Main does **not** duplicate the newest historical
year: the measured month and group keys shared between main and every historical resource are
**0**.

**The two clocks for these families.**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified`
   of the captured resource (equality checked on every silver row on 2026-10-10). Ten
   historical files (2014-15 to 2023-24) share the date 2024-05-24 (at different times of day,
   for example the 2014-15 file at `13:55:17` and the 2023-24 file at `09:45:06`). The 2024-25 file is
   `2025-04-29T15:42:04`. The main file is `2025-06-23T11:40:39`. The files carry **no issue or
   publication column**: nothing says when an individual month first became public. A 2024
   vintage on a 2014 month is therefore a late upper bound on availability, not a
   publication time. `TODO: verify` whether the 2024-05-24 bulk timestamps reflect a
   re-upload of the whole history; the captured vendor text does not say.
2. **Event time (`month`).** The temporal recipe is `month` on `settlement_month`. The vendor
   dictionary describes the date as the first day of the month standing for the **whole
   month**. `timestamp_utc` = `event_time` is the engine's month anchor, the start of the
   month's first UK settlement period, **not** a measured instant and not an issue date. For
   example, April 2014 anchors at `2014-03-31T23:00:00Z` (British Summer Time) and March 2025 at
   `2025-03-01T00:00:00Z`. Equality of `timestamp_utc` and `event_time` was checked on every
   silver row on 2026-10-10. Read the month from `settlement_month`, not from the instant.

**Units (vendor dictionary only, as cited in FACTS).**

- `Sync Costs (£m)` → `sync_costs_gbp_m`: **£(m)**, millions of pounds, declared in the
  dictionary unit field. Vendor meaning: the balancing-mechanism and trade costs of running
  units.
- `Utilisation Costs (£m)` → `utilisation_costs_gbp_m`: **£(m)**, millions of pounds, declared
  in the dictionary unit field. Vendor meaning: the voltage ancillary-service costs, stated in the
  package note to be only the ORPS payments allocated per group.
- `Coordinates` → `coordinates`: a vendor geopoint string kept exactly as supplied. The
  inspected dictionary establishes no coordinate-reference-system contract (`TODO: verify` the
  CRS before splitting it into numeric latitude and longitude columns).
- `settlement_month` is a period label and `voltage_constraint_group` an identifier. Neither
  carries a unit.

**Grain and volume.** One row per (month, voltage constraint group). Each historical file holds
228 rows (12 months × 19 groups). The main file holds 38 rows (2 months × 19 groups). The
historical series covers 132 months, `2014-04-01` to `2025-03-01`, in 19 groups; main covers
`2025-04-01` and `2025-05-01`. `TODO: verify` why the 2025-2026 file stops at May 2025 beyond
the vendor update-pause note above.

**Group labels (identifiers).** Group names are stored exactly as supplied, with no case,
punctuation or alias normalisation. The same 19 labels appear in every file:

```text
Dumfries & Galloway
E CORRIDOR
E ENGLAND
EAST MIDLANDS
HUMBER
LONDON
MERSEY
N WALES
NE SCOTLAND
NW ENGLAND
NW SCOTLAND
S CENTRAL
S WALES
SE ENGLAND
SOUTH YORKS
SW ENGLAND
W CORRIDOR
W MIDLANDS
W SCOTLAND
```

The mixed casing (`Dumfries & Galloway` against upper-case elsewhere) is the vendor's. Do not
normalise it, and key any join to the Network Diagram or to the voltage requirement series on the
exact string. `TODO: verify` how these labels map to the zones and members in
@voltage-requirement.md; the two series do not share a documented key.

**Sentinels and missing values (FACTS g5).** The records declare no null token.

- No blank cell, `-1`, `N/A`, `NA`, numeric thousands separator, currency symbol or percent
  sign was found in either cost column. Commas inside `Coordinates` are part of the geopoint
  string, not number formatting. No silver column is null in either family (checked
  2026-10-10).
- **Zero is a real value.** Historical bodies contain 1,394 zero sync costs and 142 zero
  utilisation costs; the longest consecutive file-order runs are 13 and 2. The main body
  contains 16 zero sync costs and 2 zero utilisation costs, with longest runs of 5 and 1. All
  zeros are preserved as numeric zero (`TODO: verify` VOLTAGE-COST-ZERO: no inspected source
  assigns a special meaning to zero, for example a group with no cost against a group not
  reported). gridflow makes no claim about what a zero means.
- **Two historical sync costs are below zero** (silver, checked 2026-10-23): `-3.81e-06`
  (NE SCOTLAND, 2015-11-01, 2015-16 file) and `-0.00613381` (HUMBER, 2021-02-01, 2020-21 file).
  No utilisation cost and no main-file value is below zero. The vendor dictionary states no sign
  convention for either cost column, so gridflow keeps the values as written.

**Identity and selection.** The month and group pair is measured unique inside every file and
across all eleven historical files, with zero duplicate excess, so none of the captures needed
adjudication. `TODO: verify` that NESO guarantees the key; no vendor text says so. Because the
historical files are separate annual resources, the historical family's `_latest` is
`whole_capture` partitioned by `resource_id`: a fresh capture of a resource replaces that
resource as a whole and leaves the other ten untouched, and the entity key carries
`resource_id` (ADR-039). Main has a single resource, so it needs no partition and its key is
the pair alone.

**Activation (2026-10-10, master `4d06b9f`, PR #105).** Transformed from the 2026-10-08
captures (twelve CSVs, no prior silver): `outturn_voltage_costs_historical` **2,508** silver rows
(11 × 228) and `outturn_voltage_costs_main` **38** rows, both equal to the planned counts.
Nothing was overwritten. The gridflow verification (13 of 13 truths, `status: passed`) ran the
production transformers over a scratch copy of bronze and matched both figures. Reconcile
`--all --cutoff 2026-10-10` exited 0 with 113 families, 0 gaps and 0 stale (gridflow
`@.planning/v0.22-RESULTS.md` section SYS-1; RULINGS 640, 642, 646 and 647). Silver is stored
as one Parquet file per capture under `silver/neso_data_portal/<family>/year=2026/month=10/`
(eleven for historical, one for main). Silver columns beyond the vendor columns: `resource_id`
(historical only), `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`,
`event_time`, `available_at`, `source_run_id`, `dataset_version` (`1+e1` on every row; the
`e1` is the engine version, not the header epoch). Timestamps are tz-aware UTC.

**Classification.** Monthly outturn cost; no column is a forecast, so the forward-target test of
RULINGS 529 does not apply to this package. These families are not in the SYS-1 hold set.

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Monthly
- Captures to date: one per resource (2026-10-08). No scheduled refresh has run yet.

The vendor labels the update frequency Monthly, but the package note says updates are paused
(see above), and the newest month held is 2025-05-01, with the newest file last changed on
2025-06-23. The nominal cadence therefore does not describe the actual publication. `TODO:
verify` whether past-year files are ever restated after first publication; only repeated
captures compared row by row can show this.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

No family and no resource of this package is held, and no capture is adjudicated failed. This is
the registry's status (gridflow `@docs/neso_data_portal/eligibility.md`: package
`outturn-voltage-costs` eligible, 12 silver resources, 1 DOC, 0 held) and the SYS-1 activation result.
The open `TODO: verify` items above (key guarantee, meaning of zero, ORPS scope, CRS of
`Coordinates`, resumption of updates) are documentation gaps, not hold questions, and none
blocks use of the silver rows.
