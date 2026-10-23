---
source: "neso_data_portal"
package: "daily-balancing-costs-balancing-services-use-of-system"
dataset_key: "daily_balancing_costs"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze"
eligibility: "eligible"
---

# Daily Balancing Services Use of System (BSUoS) Cost Data

Ten annual CSVs of **balancing cost by settlement period**, one file per financial year from
April 2017, plus one workbook listing settlement periods the vendor says are missing. Despite
the name "Daily", the body is settlement-period grain: each row is one settlement date and
settlement period, with six **wide** category columns (Energy Imbalance, Frequency Control,
Positive Reserve, Negative Reserve, Constraints, Other). Category is carried by column name;
there is no long-form category column. The vendor describes the package as the cost of
day-to-day operation of the transmission system, recovered through the BSUoS charge from
generators and suppliers (gridflow
`@.planning/phases/v0.22-K-BAL-1/K-BAL-1-FACTS.md` BAL-1c). Use it as a historical record of
what the system operator spent on each balancing category, period by period, next to the
sibling volume package (@daily-balancing-volume-balancing-services-use-of-system.md) and the
BSUoS charge package (@current-balancing-services-use-of-system-bsuos-data.md).

**There is no silver output for this package.** The bodies carry no settlement-run column, so
no key that includes `run_type` can be built, and gridflow's record model cannot generate a
constant run column. The family stays ingest-only (RULINGS 653, the same no-record disposition
as RULINGS 538). This page therefore describes the bronze files and the reason silver is
absent. It publishes no data values.

- Publisher group: Balancing costs
- Registry group: balancing · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Daily Balancing Costs 2017-2018 | CSV | upload | `a84e4ccb-18e2-474e-a34a-47b835772f17` |
| Daily Balancing Costs 2018-2019 | CSV | upload | `2be31033-829f-4030-94d6-58f2fdf76312` |
| Daily Balancing Costs 2019-2020 | CSV | upload | `723dd577-985b-4ceb-ab98-95a5df32584f` |
| Daily Balancing Costs 2020-2021 | CSV | upload | `7bcd8e25-c148-4cdb-b46f-394f88b92db5` |
| Daily Balancing Costs 2021-2022 | CSV | upload | `8d89e8ee-85d7-4395-813e-a9233b3bdb7c` |
| Daily Balancing Costs 2022-2023 | CSV | upload | `2a48ee67-a7f5-4d29-b223-a92f1d289224` |
| Daily Balancing Costs 2023-2024 | CSV | upload | `5eb3f06d-26ed-4e04-81a0-ce8c02ecd11e` |
| Daily Balancing Costs 2024-2025 | CSV | upload | `527a5f40-942b-416b-99df-81a51c30d041` |
| Daily Balancing Costs 2025-2026 | CSV | upload | `46183ba7-48df-4318-9b4b-06828348d46e` |
| Daily Balancing Costs 2026-2027 | CSV | upload | `1d040751-f77f-4641-9130-d49f8cbfe54f` |

The registry routes all ten CSVs to the `daily_balancing_costs` family, but that family has
`transformer: null`, so the SILVER label records the intended routing and **no silver rows
exist** (nothing under `C:/gridflow-data/silver/neso_data_portal/` for this family; the
eligibility report lists it as ingest-only). Each resource below is captured in bronze as
`raw_<stamp>_<resource_id>_<hash>.csv` with a `.meta.json` sidecar under
`C:/gridflow-data/bronze/neso_data_portal/daily_balancing_costs/2026/10/08/` (newest capture,
2026-10-08). All are `url_type: upload`. Row counts are body rows excluding the header.

| Resource | Download | Bytes | Rows | Vintage `ckan_last_modified` | Header epoch |
|---|---|---:|---:|---|---|
| 2017-2018 | [q1_cost_fy1718.csv](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/a84e4ccb-18e2-474e-a34a-47b835772f17/download/q1_cost_fy1718.csv) | 1,100,388 | 17,520 | 2022-09-28T16:02:28.295736 | old order, `%d/%m/%Y` |
| 2018-2019 | [q1_cost_fy1819.csv](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/2be31033-829f-4030-94d6-58f2fdf76312/download/q1_cost_fy1819.csv) | 1,340,159 | 17,493 | 2024-03-04T14:40:43.156956 | new order, `%Y-%m-%d` |
| 2019-2020 | [q1_cost_fy1920.csv](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/723dd577-985b-4ceb-ab98-95a5df32584f/download/q1_cost_fy1920.csv) | 1,144,160 | 17,557 | 2022-09-28T15:50:27.312532 | old order, `%d/%m/%Y` |
| 2020-2021 | [q1_cost_fy2021.csv](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/7bcd8e25-c148-4cdb-b46f-394f88b92db5/download/q1_cost_fy2021.csv) | 1,152,561 | 17,511 | 2022-09-28T15:36:16.188755 | old order, `%d/%m/%Y` |
| 2021-2022 | [q1_cost_fy2122.csv](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/8d89e8ee-85d7-4395-813e-a9233b3bdb7c/download/q1_cost_fy2122.csv) | 1,393,242 | 17,518 | 2024-03-04T14:41:45.817232 | new order, `%Y-%m-%d` |
| 2022-2023 | [q1_cost_fy2223.csv](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/2a48ee67-a7f5-4d29-b223-a92f1d289224/download/q1_cost_fy2223.csv) | 1,390,897 | 17,519 | 2023-04-05T07:59:33.016990 | new order, `%Y-%m-%d` |
| 2023-2024 | [q1_cost_fy2324.csv](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/5eb3f06d-26ed-4e04-81a0-ce8c02ecd11e/download/q1_cost_fy2324.csv) | 1,402,355 | 17,566 | 2024-04-07T13:21:09.292095 | new order, `%Y-%m-%d` |
| 2024-2025 | [q1_cost_fy2425.csv](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/527a5f40-942b-416b-99df-81a51c30d041/download/q1_cost_fy2425.csv) | 1,429,537 | 17,512 | 2025-05-14T11:10:46.981006 | new order, `%Y-%m-%d` |
| 2025-2026 | [q1_cost_fy2526.csv](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/46183ba7-48df-4318-9b4b-06828348d46e/download/q1_cost_fy2526.csv) | 1,470,668 | 17,516 | 2026-04-07T10:24:13.342330 | new order, `%Y-%m-%d` |
| 2026-2027 | [q1_cost_fy2627.csv](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/1d040751-f77f-4641-9130-d49f8cbfe54f/download/q1_cost_fy2627.csv) | 733,417 | 8,826 | 2026-10-03T11:18:19.357113 | new order, `%Y-%m-%d` |

The ten resources total 166,538 body rows. Annual resources are disjoint on
`(settlement date, settlement period)` and contain no duplicate pairs (FACTS C03). The
2026-2027 resource is the in-progress year; `TODO: verify` its last settlement date and the
vendor's publication lag, neither of which the captured evidence records.

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Missing Settlement Periods since January 2017 | XLSX | upload | `bfd081bc-9642-4ed6-9f37-60c5cbe26bef` | missing-period list (60 SETT_DATE/SETT_PERIOD pairs) — no child record while the parent family has none; the list does not cover all 70 measured gaps. (BAL-1) |
| ↳ Missing_Dates_Periods | — | — | HOLD: missing-period list (60 SETT_DATE/SETT_PERIOD pairs) — no child record while the parent family has none; the list does not cover all 70 measured gaps. (BAL-1) | — |

- Download: [missing_dates_periods.xlsx](https://api.neso.energy/dataset/d13d78fc-60d9-4f4d-87b6-e25a20f669c0/resource/bfd081bc-9642-4ed6-9f37-60c5cbe26bef/download/missing_dates_periods.xlsx)
  (CKAN `last_modified` 2025-08-08T09:51:17.477156). Captured as
  `raw_20261008T100424Z_bfd081bc-9642-4ed6-9f37-60c5cbe26bef_9e601263.xlsx`, 11,076 bytes,
  family `daily_balancing_costs_files`.
- The workbook has one tabular sheet, `Missing_Dates_Periods`, header `SETT_DATE`,
  `SETT_PERIOD` in row 1, data in `A2:B61`: **60 unique pairs**, none of which occurs in the
  daily CSVs. It is a list of absent observations, not documentation, so it is not DOC. The
  sibling volume package carries a byte-identical workbook (same SHA-256 body hash), so the
  same list appears in both packages (FACTS C05).
- The hold question (E-SEM): what exception-list semantics, date recipe, identity, run scope
  and selection policy should a child record for this list carry? It cannot be frozen while
  the parent family has no record. The hold is on an exception list of coordinates, so there
  are no values or units attached to it; the pairs are settlement coordinates only.
- The vendor package note says 60 periods are missing from 1 January 2017. The captured CSVs
  show **70** missing pairs (table under Known issues). The workbook is therefore not a
  complete completeness guarantee.

## Families

### `daily_balancing_costs`

- Kind: tabular · archetype: SER · refresh: weekly · empty allowed: no
- ingest-only: no silver yet

**No silver record, and why.** The bodies have no run column. The dictionary phrase "Initial
Settlement Run" does not establish that a generated value should be `II`, and a `ColumnSpec`
has no constant or source-generation field (`run_type_column` must reference an existing
string output in the entity key, validation V-5; `record.py` lines 131, 524, 690 in FACTS).
The settlement-style key `(sett_date, sett_period, run_type)` that every sibling BSUoS family
uses therefore cannot be expressed. Keying on date and period alone would break the
settlement-key rule. Silver stays absent rather than silently dedup or invent a run
(RULINGS 653; precedent RULINGS 538, where a vendor body that no key could safely identify also
got no record). Merge and activation confirm it: PR #106 squash `1ccb467` (RULINGS 655) and
activation of 9 other families with this one left record-less (RULINGS 656;
`@.planning/v0.22-RESULTS.md` section BAL-1). Settlement needs a vendor run identifier plus an
approved constant-column mechanism, a corrected run-bearing body, or a ruling that changes the
run-key requirement for this publication. `TODO: verify` which of the three NESO or the project
chooses.

Bronze columns (vendor headers, as captured; every header is internally homogeneous within its
epoch):

| Vendor column | Unit (vendor dictionary) | Notes |
|---|---|---|
| `SETT_DATE` | date | See the date-definition conflict below |
| `SETT_PERIOD` | settlement-period index, dimensionless | Intervals begin on an hour or half-hour |
| `Energy Imbalance` | £ | Imbalance-related cost; costs can be signed |
| `Frequency Control` | £ | Response and fast reserve |
| `Positive Reserve` | £ | Reserve energy for demand changes or generation shortfalls |
| `Negative Reserve` | £ | Flexibility to reduce generation or increase demand against unforeseen imbalance |
| `Constraints` | £ | Actions protecting network equipment and meeting secure-operation requirements |
| `Other` | £ | Otherwise-uncategorised balancing-mechanism actions plus general, non-delivery and reconciliation costs |

Two header epochs exist. Only the column order after the date and period differs, plus the
date text format:

| Epoch | Resources | Category order after the pair | Date format |
|---|---|---|---|
| Old | 2017-2018, 2019-2020, 2020-2021 | Energy Imbalance; Frequency Control; Positive Reserve; Negative Reserve; Constraints; Other | `%d/%m/%Y` |
| New | 2018-2019 and 2021-2022 onward | Energy Imbalance; Frequency Control; Positive Reserve; Constraints; Negative Reserve; Other | `%Y-%m-%d` |

Any future record must choose its date format per epoch and must not carry the ISO-only format
onto the old-order files (FACTS BAL-1c).

### `daily_balancing_costs_files`

- Kind: files · archetype: SER · refresh: weekly · empty allowed: no
- files: catalogue only

Holds the missing-periods workbook above. It has no transformer and no child record.

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Weekly

The weekly label is the vendor's, but each resource's `ckan_last_modified` moves only when
NESO re-uploads that file. Seven of the ten annual CSVs last changed between September 2022 and April 2024,
and only the 2026-2027 resource changed in October 2026 (table above). Treat the closed
financial years as effectively static unless the vendor republishes them (the 2018-2019 and
2021-2022 files both show a CKAN `last_modified` of 2024-03-04).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none

The generated list above reports no package-level holds. The only HOLD disposition is the
workbook shown under Files by disposition. The absence of a silver record is a no-record
disposition, not a hold on a published output.

## Two clocks

Bronze-only package, so no silver `timestamp_utc` or `available_at` exists. The clocks a record
would carry are:

1. **Vintage (`ckan_last_modified`).** Every resource is `url_type: upload`, so the vintage for
   a capture is that resource's CKAN `last_modified` (sidecar field `ckan_last_modified`),
   not the capture-time fallback. `available_at` would equal it. CKAN emits it without an
   offset; gridflow reads it as UTC
   (`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Per-resource values are in
   the table above. There is no issue column in the body, so the issue recipe would be `none`.
2. **Event time.** The temporal recipe for a future record is **proposed, not frozen**:
   `sp_pair(sett_date, sett_period)`, the start of the settlement period. It is a candidate
   only, because `SETT_DATE` is titled a settlement date while the vendor dictionary also
   describes it as a payment date (see Known issues). `TODO: verify` which the date is before
   claiming an independently evidenced event clock. No `none` recipe applies. Since no silver
   exists, no `timestamp_utc` is published for this family at all.

## Units and sentinels

Units come only from the vendor field dictionary (FACTS BAL-1c; `F(daily_balancing_costs)`
lines 43, 55, 67, 79, 91, 103): all six category columns are **£**. The package-level resource
prose mentions cost per MWh, which conflicts with the per-column dictionary; the column-level
unit governs. `SETT_PERIOD` is an index, not a physical quantity. Signed cost values are
expected for Energy Imbalance.

Sentinel handling (FACTS g5): no uncastable numeric tokens, comma-formatted numbers, currency
symbols, percentage values, blanks or `NA`/`N/A` tokens were measured in any of the ten
bodies, and the numeric casts all passed. Zero values occur, including long runs of consecutive
zeros in the Negative Reserve, Constraints and Positive Reserve columns. Zeros are numbers.
Nothing in the vendor material makes zero, or any other value, a missing-data marker, so no
sentinel is mapped to null. The `-1` pattern found in the sibling volume package does not
apply here. `TODO: verify` the vendor's meaning for zero where no definition exists.

## Known issues and gotchas

- **No run column.** Rows are not labelled with a settlement run (II, SF or RF), unlike every
  BSUoS charge package. Do not assume the "Initial Settlement Run" wording in a dictionary
  means `II`.
- **`SETT_DATE` definition conflict.** The title says settlement date, the dictionary
  describes a payment date, and the resource grain is the settlement period. `TODO: verify`.
- **Wide, not long.** Six category columns per row; the "Daily" name does not mean one row per day.
- **Missing settlement periods.** The captured CSVs lack 70 date/period pairs, measured against
  the GB clock-change calendar (so 46- and 50-period days are counted correctly). The workbook
  lists only 60 and none of them appears in the CSVs. How the other 10 relate to the vendor
  list is not established (`TODO: verify`).

  | Resource year | Missing pairs |
  |---|---:|
  | 2017-2018 | 0 |
  | 2018-2019 | 27 |
  | 2019-2020 | 11 |
  | 2020-2021 | 9 |
  | 2021-2022 | 2 |
  | 2022-2023 | 1 |
  | 2023-2024 | 2 |
  | 2024-2025 | 8 |
  | 2025-2026 | 4 |
  | 2026-2027, through captured end | 6 |
  | **Total** | **70** |

- **Row counts are not 17,520 a year.** The 2017-2018 file has 17,520 rows (365 days × 48);
  other years vary with the gaps above and the clock-change days (46 and 50 periods).
- **Resource names and file names are by financial year**, April to March, starting
  1 April 2017.
- **Values may be revised.** The 2018-2019 and 2021-2022 files both carry a CKAN
  `last_modified` of 2024-03-04, long after their financial years. Whether any values changed is `TODO: verify`; there is no stable revision key,
  so a re-capture is a new vintage.
- **Date text differs between epochs** (day-first slashes vs ISO), see Families.
- **Vendor note about the data.** NESO describes charges as calculated daily as a flat tariff
  for all users and says the costs are provided "on a daily basis in a annual file" (vendor
  catalogue text, not a verified statement about the body grain).

## Implementation delta

- **`run_type`**: sibling BSUoS records declare `run_type_column`; this family cannot, because
  the body has no run column and the record model has no constant-column mechanism. No record
  exists by ruling (RULINGS 653).
- **Registry disposition vs silver**: the registry labels the ten CSVs `SILVER`, but the family
  has `transformer: null`. The label is a routing statement, not evidence of silver data.
  Reality: no silver exists.
- **Workbook child**: the registry HOLD reason carries the 60-pair / 70-gap wording (updated by
  BAL-1 and tested).
- **Vendor dictionary vs title**: `SETT_DATE` payment-date wording against the settlement-date
  title, unresolved.

## Modelling notes

TODO. No model consumes this package, and no silver exists to feed one. Candidate uses once a
run-bearing key exists: category-level balancing-cost targets by settlement period, to be
joined with the sibling volume package (same coordinates) for an implied cost-per-MWh by
category. Do not join it to settlement-run data on `(date, period)` alone.

## Links

- [Official dataset page](https://www.neso.energy/data-portal/daily-balancing-costs-balancing-services-use-of-system) (`TODO: verify` the URL resolves; derived from the package name)
- Registry record: `@src/gridflow/connectors/neso_data_portal/registry/daily-balancing-costs-balancing-services-use-of-system.json`
- Eligibility report: `@docs/neso_data_portal/eligibility.md`
- Batch evidence: `@.planning/phases/v0.22-K-BAL-1/K-BAL-1-FACTS.md`, `@.planning/phases/v0.22-K-BAL-1/VERIFICATION.md`
- Activation receipt: `@.planning/v0.22-RESULTS.md` (section BAL-1); rulings 538, 653, 655, 656 in `@.planning/RULINGS.md`
- ADRs: `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`, `@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md`
- Sibling pages: @daily-balancing-volume-balancing-services-use-of-system.md, @current-balancing-services-use-of-system-bsuos-data.md

Supported by National Energy SO Open Data
