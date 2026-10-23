---
source: "neso_data_portal"
package: "thermal-constraint-costs"
dataset_keys: ["thermal_constraint_costs", "thermal_constraint_costs_xlsx"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Thermal Constraint Costs

This package is NESO's record of **outturn system costs for thermal constraints**, one number
per day for each of six named constraint groups. The catalogue describes a thermal constraint
as arising when "the amount of energy that would flow naturally from one region to another exceeds
the capacity of the circuits connecting the two regions", and the vendor field dictionary
describes the cost column as "the daily spend in GBP for the constraint". What that spend is
composed of (which actions or payments it counts, and on which side of a boundary) is not
stated in the vendor material: `TODO: verify` with NESO. Each row is one settlement date, one
constraint group and a rounded integer `daily_cost_gbp`. It is a backward-looking (outturn,
not forecast) daily cost series by constraint group. It carries no issue time and is not
a cost per MWh.

**Seven things to know before using it.**

1. **Two silver families, one package.** `thermal_constraint_costs` reads the five yearly CSV
   files for 2022-23 to 2026-27; `thermal_constraint_costs_xlsx` reads the `Data` sheet of the
   two older workbooks (2019-20 and 2020-21). Their schemas and keys are identical and they
   never overlap (0 shared keys), so a continuous series needs both.
2. **One CSV resource is a resource-level HOLD: 2021-22** (unit E-SEM). Its cost cells include
   thousands separators (360 of them) and the strict integer cast refuses them. It has bronze
   only, no silver, and this page shows none of its values. The silver series therefore has a
   **year-long gap: 2021-04-01 to 2022-03-31 by the file's title** (see Holds).
3. **Two clocks, and the event clock is a real date.** `timestamp_utc` is the start of settlement
   period 1 of the `settlement_date` in GB local time (23:00 UTC the previous evening in BST,
   00:00 UTC in GMT), **not** the capture time. The vintage is the CKAN `last_modified` of each
   file, which differs per file and is `available_at`.
4. **`available_at` is the file's vintage, so it can be later than a row's true first
   publication.** NESO states a weekly update, and only one capture per file exists
   (2026-10-08). The current-year file's earlier rows were presumably public before its
   2026-10-03 vintage, but nothing captured proves when (`TODO: verify` NESO's append
   behaviour). Pre-dating a row to its date would be wrong;
   using `available_at` is the safe, conservative reading.
5. **Zeros and negative costs are real values.** Most cells are zero
   and 21 cells are negative. Nothing in the vendor material defines zero as
   missing or negative as an error, so none is nulled (`TODO: verify` the vendor meaning of
   negatives).
6. **Constraint group codes are stored exactly as published** (`ESTEX`, `SCOTEX`, `SEIMP`,
   `SSE-SP`, `SSHARN`, `SWALEX`). Do not normalise, and do not merge `SSE-SP` with the
   similarly named `SSE_SP`/`SSE_SP2` of the day-ahead and limits tables.
7. **One calendar day is missing** from the 2025-26 CSV (2025-04-08, all six groups).

The shared research is gridflow `@.planning/phases/v0.22-K-CON/K-CON-FACTS.md` (section 6 and
section 8) and the verification is `@.planning/phases/v0.22-K-CON/VERIFICATION.md`. Sibling
constraint-management packages: @./day-ahead-constraint-flows-and-limits.md,
@./24-months-ahead-constraint-limits.md,
@./operational-transparency-forum-network-congestion-data.md and the forecast counterpart
@./24-months-ahead-constraint-cost-forecast.md. Settlement-day background:
@../../../20-domain/concepts/settlement-period.md.

- Publisher group: Constraint management
- Registry group: constraint-management · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Thermal Constraint Costs 19-20 | XLSX | upload | `d195f1d8-7d9e-46f1-96a6-4251e75e9bd0` |
| ↳ Data | — | — | SILVER `thermal_constraint_costs_xlsx` |
| ↳ Map | — | — | DOC |
| ↳ Network Diagram E&W | — | — | DOC |
| ↳ Network Diagram Scot | — | — | DOC |
| ↳ Dates | — | — | DOC |
| Thermal Constraint Costs 20-21 | XLSX | upload | `a4302916-85af-4a4d-8171-1bdf8f0697a7` |
| ↳ Data | — | — | SILVER `thermal_constraint_costs_xlsx` |
| ↳ Map | — | — | DOC |
| ↳ Network Diagram E&W | — | — | DOC |
| ↳ Network Diagram Scot | — | — | DOC |
| ↳ Dates | — | — | DOC |
| Thermal Constraint Costs Data 22-23 | CSV | upload | `476b8d39-5eda-425c-9756-73ddfd36dc4d` |
| Thermal Constraint Costs Data 23-24 | CSV | upload | `75c9c564-af38-4421-a461-a612a6921212` |
| Thermal Constraint Costs Data 24-25 | CSV | upload | `27df75fd-6233-466c-beed-3e6e2261e6b1` |
| Thermal Constraint Costs Data 25-26 | CSV | upload | `407f3e9d-5c38-4a64-98f5-923dc4d64fb2` |
| Thermal Constraint Costs Data 26-27 | CSV | upload | `c730b788-4328-43dc-9f84-27fd3adeda59` |

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Constraint Map | PNG | upload | `29d824c5-9ea9-4520-943d-3e61913cd8ff` |
| Network Diagram England & Wales | PNG | upload | `57673696-39ac-4f65-81a2-983577ff7249` |
| Network Diagram Scotland | PNG | upload | `2f3e8b4e-a46b-4e14-8a58-9f6a0891d855` |

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Thermal Constraint Costs Data 21-22 | CSV | upload | `4357dd3b-5c7a-4caa-8d1a-8cf848521143` | the 2021-22 body has 360 comma-formatted Daily Cost (GBP) values (written with thousands separators) that fail the strict int64 cast, and the record has no lexical-number mechanism; re-disposition only after a declared lexical-number mechanism, or a corrected NESO upload (a new last_modified) (E-SEM) |

**Reading the disposition tables.** All 11 resources are `url_type: upload`. "SILVER" for a
workbook means its `Data` sheet is read to silver; its other four sheets (`Map`,
`Network Diagram E&W`, `Network Diagram Scot`, `Dates`) are DOC and are not read (their
contents are described only as auxiliary material by the earlier workbook research, X-R; the
`Dates` sheet's purpose is `TODO: verify`). The three PNGs are reference images with no tabular
content. The single HOLD resource has bronze only.

**Downloads and captures.** Every resource was captured once, on 2026-10-08, from
`api.neso.energy`. Bronze is under
`C:/gridflow-data/bronze/neso_data_portal/thermal_constraint_costs/2026/10/08/` (the six CSVs)
and `.../thermal_constraint_costs_files/2026/10/08/` (the two workbooks and three PNGs), one
body and one `.meta.json` sidecar per resource. Sizes are physical body sizes and row counts
are table rows over the complete body (FACTS); the package was created in the catalogue on
2019-10-31, last had its metadata changed on 2026-10-03, has no version string and carries
seven tags (Constraints, Costs, Diagrams, Network, Outturn, Subscribable, Thermal). Licence id
`ESO`, "NESO Open Data Licence". Package page:
[Thermal Constraint Costs](https://www.neso.energy/data-portal/thermal-constraint-costs).

| Resource | Role | Download | Bytes | Body rows | CKAN `last_modified` |
|---|---|---|---:|---:|---|
| Data 21-22 | HOLD | [outturn-system-costs-2021-2022.csv](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/4357dd3b-5c7a-4caa-8d1a-8cf848521143/download/outturn-system-costs-2021-2022.csv) | 48,560 | 2,190 (not read to silver) | 2022-04-08T15:22:06.203234 |
| Data 22-23 | SILVER | [outturn-system-costs-2022-2023.csv](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/476b8d39-5eda-425c-9756-73ddfd36dc4d/download/outturn-system-costs-2022-2023.csv) | 47,648 | 2,190 | 2023-04-17T16:03:55.101783 |
| Data 23-24 | SILVER | [outturn-system-costs-2023-2024.csv](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/75c9c564-af38-4421-a461-a612a6921212/download/outturn-system-costs-2023-2024.csv) | 47,559 | 2,196 | 2024-04-04T10:31:42.196846 |
| Data 24-25 | SILVER | [outturn-system-costs-2024-2025.csv](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/27df75fd-6233-466c-beed-3e6e2261e6b1/download/outturn-system-costs-2024-2025.csv) | 48,348 | 2,190 | 2025-04-04T15:20:03.256759 |
| Data 25-26 | SILVER | [outturn-system-costs-2025-2026.csv](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/407f3e9d-5c38-4a64-98f5-923dc4d64fb2/download/outturn-system-costs-2025-2026.csv) | 47,908 | 2,184 | 2026-04-07T10:00:55.940094 |
| Data 26-27 | SILVER | [outturn-system-costs-2026-2027.csv](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/c730b788-4328-43dc-9f84-27fd3adeda59/download/outturn-system-costs-2026-2027.csv) | 24,827 | 1,104 | 2026-10-03T11:17:46.430939 |
| Thermal Constraint Costs 19-20 | SILVER (`Data` sheet) | [map-of-outturn-system-costs-19-20.xlsx](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/d195f1d8-7d9e-46f1-96a6-4251e75e9bd0/download/map-of-outturn-system-costs-19-20.xlsx) | 1,383,884 | 1,464 (`Data` sheet) | 2020-06-12T14:41:30.987252 |
| Thermal Constraint Costs 20-21 | SILVER (`Data` sheet) | [map-of-outturn-system-costs-20-21.xlsx](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/a4302916-85af-4a4d-8171-1bdf8f0697a7/download/map-of-outturn-system-costs-20-21.xlsx) | 1,402,077 | 2,190 (`Data` sheet) | 2021-04-21T14:57:58.768221 |
| Constraint Map | DOC | [map.png](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/29d824c5-9ea9-4520-943d-3e61913cd8ff/download/map.png) | 76,930 | — | 2021-05-19T10:01:43.341129 |
| Network Diagram England & Wales | DOC | [network-diagram-ew.png](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/57673696-39ac-4f65-81a2-983577ff7249/download/network-diagram-ew.png) | 2,572,723 | — | 2019-11-05T09:47:30.481417 |
| Network Diagram Scotland | DOC | [network-diagram-scotland.png](https://api.neso.energy/dataset/f0055054-c55c-4068-a01c-61da4334e58f/resource/2f3e8b4e-a46b-4e14-8a58-9f6a0891d855/download/network-diagram-scotland.png) | 1,611,646 | — | 2019-11-05T09:49:20.597767 |

- **gridflow captures the uploaded file**, not a CKAN datastore dump, so the vintage is
  `ckan_last_modified` (ADR-030, ADR-033). The CSV resources report an active datastore and the
  workbooks and PNGs do not, but that does not change what is captured.
- **The Constraint Map** labels the six boundary codes (FACTS C11: `SSE-SP`, `SCOTEX`, `SSHARN`,
  `SWALEX`, `SEIMP`, `ESTEX`); the two network diagrams locate them. They are the only
  documentation of what each code covers that gridflow has captured; the full membership of each
  group is `TODO: verify`.
- **The 2020-21 workbook's `last_modified` (2021-04-21)** is later than the end of the year it
  covers (2021-03-31) by about three weeks; the 2019-20 workbook's (2020-06-12) is about
  ten weeks after its year end. These are the genuine captured vintages and are not replaced
  by the financial year.

## Families

**What applies to all three families.**

*Identity and selection.* Each resource is one financial year (1 April to 31 March; the 2019-20
workbook starts on 2019-08-01 and the 2026-27 CSV runs from 2026-04-01 to the most recent
published day, 2026-10-01 at the 2026-10-03 vintage). Each capture is a whole file, so the
record sets `latest` to `whole_capture` per `resource_id` (`latest_partition: resource_id`):
the six CSV and two workbook partitions are independent, and a later NESO re-upload of any
resource adds a new whole capture that `_latest` takes for that resource only. A family-wide
newest capture would have kept just one year (ADR-039). Bronze is never edited. The entity key
`resource_id, settlement_date, constraint_group` is unique in every complete body (zero
duplicate excess), and no key occurs in two resources, in either family. NESO states no
uniqueness guarantee (`TODO: verify` vendor identity guarantee); it affects nothing today
because selection is by whole capture, not by key.

*The two clocks (every family).*

1. **Vintage: `ckan_last_modified`.** `published_at` and `available_at` are the CKAN
   `last_modified` of the captured file, both equal on every row (measured), and different per
   resource (listed above). It is not the capture time and not the settlement date (ADR-030).
   An as-of query is `WHERE available_at <= :as_of`. No issue column exists (`issue.kind:
   none`) and none is appropriate: the data is retrospective outturn.
2. **Event time: `date_sp1(settlement_date)`.** `timestamp_utc` and `event_time` (equal on every
   row, measured) are the **start of settlement period 1 of the settlement date, in GB local
   time, converted to UTC**. Measured: `2022-04-01` has `timestamp_utc` `2022-03-31T23:00Z`
   (BST, local midnight is 23:00 UTC), and `2024-03-31`, the spring clock-change day with the
   day still in GMT at midnight, has `2024-03-31T00:00Z`. It is a **day anchor, not an
   instant**: the cost belongs to the whole settlement day. The anchor is an engine convention
   (FACTS section 1), not a vendor statement; the vendor only says the date is "the date the
   constraint costs belong to", so whether the vendor's day boundary is the GB-local settlement
   day is `TODO: verify`. The silver column `settlement_date` is the vendor date, unchanged.
   Capture time is in `capture_written_at` (2026-10-08).

*Units (vendor dictionary only, as cited in FACTS).* `Daily Cost (GBP)` has dictionary unit
**GBP** (written `£`) and the description states it is the daily spend for the constraint, an
**integer (rounded)**. `Settlement Date` has dictionary unit `ISO 8601`. `Constraint Group` has
no unit. The dictionary does not say whether amounts are nominal or inflation-adjusted
(`TODO: verify`). Units are never inferred from a column name.

*Sentinels and missing values (FACTS g5).* NESO declares no null token and none of the listed
literal tokens (`NA`, `N/A`, `-1`) occurs in any silver resource; no cost cell is blank. A **zero**
is a zero and a **negative** is a negative: no vendor source defines either as missing or
erroneous, so neither is converted to null. The only malformed numbers are the thousands
separators in the held 2021-22 file.

*Silver layout.* Parquet files under
`C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`, one file per capture,
written by one run each between `2026-10-08T11-38-34` and `2026-10-08T11-38-52`. The
`year=`/`month=` partition is the **capture** date. Lineage columns appended to the vendor
columns: `resource_id`, `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version`
(the workbook family adds `child_id` and `child_crc32` before them). All timestamps are
tz-aware UTC. `dataset_version` reads `1+e1` on every capture; what `e1` encodes is not
established here (`TODO: verify`).

*Constraint group codes (FACTS section 8).* Six codes, stored as published, each with the same
row count in each family (1,644 per code in the CSV family, 609 in the workbook family). The
codes are named transmission boundaries; vendor and map evidence give geographic meanings for
them, and the OTF documentation presents `B6 (SCOTEX)`, `B7 (SSHARN)`, `LE1 (SEIMP)` and
`B15 (ESTEX)` as aliases. Those are reference relationships, not storage rules. Exact-string
overlap with other constraint-management tables (FACTS section 8, measured on raw strings):

| Pair | Overlap with this package's six codes |
|---|---|
| Day-ahead flows and limits | 5: `ESTEX`, `SCOTEX`, `SEIMP`, `SSHARN`, `SWALEX` |
| 24-month constraint limits | 2: `ESTEX`, `SCOTEX` |
| OTF network congestion | 0 |

`SSE-SP` does not match the day-ahead table's `SSE_SP` and `SSE_SP2`; whether they are the same
boundary is `TODO: verify` and they are never merged by gridflow. Whether the six groups are
additive or overlap (so that a sum across groups could double-count a cost) is also
`TODO: verify`.

### `thermal_constraint_costs`

- Kind: tabular · archetype: SER · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Date | `settlement_date` | date | `%Y-%m-%d` | no | — | ISO 8601 |
| Constraint Group | `constraint_group` | string | — | no | — | — |
| Daily Cost (GBP) | `daily_cost_gbp` | int64 | — | yes | — | £ |

- Entity key: `resource_id`, `settlement_date`, `constraint_group`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: date_sp1 (`settlement_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible. Silver: 9,864 rows, 12 columns, from five of the six resources** (the 2021-22
resource is held and has no silver). Measured on silver (2026-10-10):

| Resource (financial year) | Rows | Settlement dates | `published_at` = `available_at` | Zero costs | Negative costs | `timestamp_utc` range (first / last day anchor) |
|---|---:|---|---|---:|---:|---|
| 22-23 | 2,190 | 2022-04-01 to 2023-03-31 (365 days) | 2023-04-17T16:03:55.101783 | 1,738 | 6 | 2022-03-31T23:00Z / 2023-03-30T23:00Z |
| 23-24 | 2,196 | 2023-04-01 to 2024-03-31 (366 days) | 2024-04-04T10:31:42.196846 | 1,770 | 0 | 2023-03-31T23:00Z / 2024-03-31T00:00Z |
| 24-25 | 2,190 | 2024-04-01 to 2025-03-31 (365 days) | 2025-04-04T15:20:03.256759 | 1,548 | 7 | 2024-03-31T23:00Z / 2025-03-30T23:00Z |
| 25-26 | 2,184 | 2025-04-01 to 2026-03-31 (364 of 365 days) | 2026-04-07T10:00:55.940094 | 1,578 | 7 | 2025-03-31T23:00Z / 2026-03-30T23:00Z |
| 26-27 | 1,104 | 2026-04-01 to 2026-10-01 (184 days) | 2026-10-03T11:17:46.430939 | 680 | 1 | 2026-03-31T23:00Z / 2026-09-30T23:00Z |

Every capture's `capture_written_at` is 2026-10-08 (11:38:34 to 11:38:46 UTC). No cost is null
in any resource. The six groups are present on every settlement date present (six rows per
day). Zero-run lengths in physical body order (FACTS) are 66, 72, 30, 57 and 16 for the five
silver resources, longest consecutive; zeros are heavy (62 to 81 percent of cells in
each resource) and are vendor values, not missing data. The vendor does not state what a
zero cost means for a day (no recorded constraint action, or no cost attributed;
`TODO: verify`). The 21 negative cells are kept as published; a negative is a published
number, and the vendor gives no explanation (`TODO: verify` whether they are credits,
re-attributions or corrections).

*The missing day.* The 2025-26 body has no rows for 2025-04-08, for any of the six groups
(2,184 rows is 364 days times six). It is a gap in the vendor body, not a gridflow exclusion
(bronze and silver agree). Whether NESO omitted the day or has no costs to report is
`TODO: verify`; do not zero-fill it, because zero is a stated value in this series.

*The open year.* The 26-27 file ended at 2026-10-01 at its 2026-10-03 vintage, i.e. it lags
the vintage by two days; later weekly refreshes will re-upload the same resource with a new
`last_modified`, adding a new whole capture that supersedes this one for that resource
(`TODO: verify` that NESO updates the same resource id rather than adding a new one). The
next financial-year resource (2027-28) does not exist yet and would need a new registry
resource entry.

### `thermal_constraint_costs_files`

- Kind: files · archetype: SER · refresh: weekly · empty allowed: no
- files: catalogue only

A catalogue-only family: it holds no silver and no record. It exists so that the two workbooks
and three PNGs are captured into bronze (`thermal_constraint_costs_files/2026/10/08/`) and the
workbooks' `Data` sheets can be routed to `thermal_constraint_costs_xlsx` through the
`siblings` link in the workbook record. The PNGs are DOC.

### `thermal_constraint_costs_xlsx`

- Kind: tabular · archetype: SER · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Date | `settlement_date` | date | `%Y-%m-%d %H:%M:%S` | no | — | — |
| Constraint Group | `constraint_group` | string | — | no | — | — |
| Daily Cost (GBP) | `daily_cost_gbp` | int64 | — | yes | — | — |

- Entity key: `resource_id`, `settlement_date`, `constraint_group`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: date_sp1 (`settlement_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible. Silver: 3,654 rows, 14 columns, from the `Data` sheet of the two workbooks.** The
reader is `xlsx` (header row 1, columns `A:C`), the workbook child of
`thermal_constraint_costs_files`, with the other four sheets of each workbook left as DOC.
Same three vendor columns as the CSV family; the 12 CSV silver columns plus `child_id` (always
`Data`) and `child_crc32`.

| Resource (financial year) | Rows | Settlement dates | `published_at` = `available_at` | Zero costs | Negative costs |
|---|---:|---|---|---:|---:|
| 19-20 workbook | 1,464 | 2019-08-01 to 2020-03-31 (244 days) | 2020-06-12T14:41:30.987252 | 1,138 | 0 |
| 20-21 workbook | 2,190 | 2020-04-01 to 2021-03-31 (365 days) | 2021-04-21T14:57:58.768221 | 1,782 | 0 |

Six rows per day in both, no null cost, no formulas in the `Data` cells (FACTS C4), cost values
integral. `timestamp_utc` ranges are `2019-07-31T23:00Z` to `2020-03-30T23:00Z` and
`2020-03-31T23:00Z` to `2021-03-30T23:00Z`.  The 2019-20 body begins on 2019-08-01, not 1 April
(NESO does not say why, `TODO: verify`).

*Date format.* The workbook stores the date as an Excel serial with a date style; the reader
(`pl.read_excel`, calamine) emits it as `YYYY-MM-DD HH:MM:SS`, which is the frozen record
format (`%Y-%m-%d %H:%M:%S`) and why this differs from the CSV family's `%Y-%m-%d`. The silver
`settlement_date` is a `date`.

*Unit caveat.* The workbooks have no data dictionary, so the vendor unit column is empty. The
header text says `Daily Cost (GBP)` and the package description speaks of outturn system costs,
and the same-named CSV column has dictionary unit GBP, but carrying that unit across to the
workbook values is an inference from identical headers, not a vendor statement
(`TODO: verify` with NESO). The two workbook years do not overlap any CSV key, so the equality
of values on overlap, which would have corroborated the unit, could not be tested (0
overlapping keys against all 12,054 CSV keys; FACTS C4).

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Weekly

The weekly statement is the vendor's. The captured `last_modified` dates show the older years'
files last changed in the spring after their year end (April 2022, 2023, 2024, 2025 and 2026
for the CSVs; June 2020 and April 2021 for the workbooks) and the open 2026-27 file last
changed on 2026-10-03, which is consistent with a weekly update of the current year only.
Gridflow captured every resource once, on 2026-10-08, from the portal sweep; the activation
cutoff was 2026-10-08. A scheduled weekly re-ingest would add a new capture of the 2026-27 file
and leave the others unchanged unless NESO re-uploads them.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none at family level (one resource-level HOLD, below)

No family output is held: both silver families are eligible. There is one **resource-level
HOLD**, shown in the HOLD table above:

1. **`Thermal Constraint Costs Data 21-22`** (`4357dd3b-5c7a-4caa-8d1a-8cf848521143`; vintage
   2022-04-08T15:22:06.203234; unit E-SEM). The body has 360 `Daily Cost (GBP)` cells written
   with thousands separators, and the strict int64 cast refuses them. The record model has no
   lexical-number mechanism (comma removal would be a silent rewrite of vendor text, and
   falling back to float would change the declared dtype). The cause is formatting, not
   fractional costs, so it is a resource HOLD and not an ADR-040 failed adjudication
   (RULINGS 608). The vendor's own dictionary example for the cost column also uses thousands
   separators, so the format appears to be a vendor convention that NESO applied in this file
   only (`TODO: verify` why the 2022-23 and later files are plain integers). The held body is
   in bronze (2,190 rows) and has **no silver**; this page does not show its values.
   Re-disposition needs a declared lexical-number mechanism in the record model, or a corrected
   NESO upload with a new `last_modified`.

Consequence for use: the silver series is continuous from 2019-08-01 to 2021-03-31 (workbooks),
absent for the 2021-22 financial year, and continuous again from 2022-04-01 (CSVs), apart from
the single missing day 2025-04-08. A model using this series must treat 2021-22 as unavailable
and must not interpolate it.

**Activation (2026-10-10, master `49f7c1a`, PR #104).** The frozen records merged triple-green
(CI pass twice, Sol diff review APPROVE on pass 1 with no findings, VERIFICATION passed 7 of 7
records; RULINGS 634) and were activated with cutoff 2026-10-08, no prior silver, nothing
overwritten (RULINGS 635). Row counts equal the plan: `thermal_constraint_costs` 9,864 (2,190 /
2,196 / 2,190 / 2,184 / 1,104; the 2021-22 resource held) and `thermal_constraint_costs_xlsx`
3,654 (1,464 / 2,190). Reconcile `--all --cutoff 2026-10-08` exited 0 (105 families, 0 gaps,
15 adjudicated, 0 stale, peak 2,120.9 MiB) (gridflow `@.planning/v0.22-RESULTS.md`, section
CON). No engine, reader or record-model change was needed. The workbook family is new in this
batch; its date format is the measured calamine spelling, frozen by a fixture test.

No gold view or model consumes this package as of 2026-10-10 (RULINGS 638: no CON package
feeds the gold views or the models).

References: gridflow `@.planning/phases/v0.22-K-CON/K-CON-FACTS.md` (section 6, section 8, g4,
g5), `@.planning/phases/v0.22-K-CON/K-CON-SPEC.md` (sections 5 and 6),
`@.planning/phases/v0.22-K-CON/VERIFICATION.md`, `@.planning/RULINGS.md` (608, 630, 632, 634,
635),
`@src/gridflow/connectors/neso_data_portal/registry/thermal-constraint-costs.json`,
`@docs/neso_data_portal/eligibility.md`,
`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`,
`@docs/DECISION_LOG/ADR-033-neso-registry-upload-leg.md`,
`@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md` and
`@docs/DECISION_LOG/ADR-040-neso-reconcile-adjudication.md`.
