---
source: "neso_data_portal"
package: "outturn-voltage-costs"
dataset_keys: ["outturn_voltage_costs_historical", "outturn_voltage_costs_main"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Voltage System Costs

NESO's monthly record of the **outturn cost of keeping voltage on the transmission network within
limits** (vendor wording, captured package notes: the "post monthly report provides outturn system
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
