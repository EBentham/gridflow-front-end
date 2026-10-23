---
source: "neso_data_portal"
package: "daily-balancing-volume-balancing-services-use-of-system"
dataset_key: "daily_balancing_volume"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze"
eligibility: "eligible"
page:
  held: Rows are not labelled with a settlement run, so there is no silver table.
  title: Daily BSUoS volume data
  summary: >-
    NESO's balancing volume for each settlement period, in MWh, in eight columns, such as energy
    imbalance, reserve and constraints.
  facts:
    vendor: "NESO Data Portal: one CSV file per financial year, and a workbook"
    cadence: "Weekly, as NESO lists it; the newest file is the current financial year"
    grain: "Each row: settlement date and period, with eight volume columns in MWh"
    history: NESO lists one file per April-to-March year from 2017-18
  landscape: market
  what_it_is: >-
    The Balancing Services Use of System (BSUoS) charge recovers the cost of day-to-day operation
    of the transmission system. These files give the balancing volume per settlement period in
    eight MWh columns: energy imbalance, frequency control offers and bids, positive reserve,
    constraint offers and bids, negative reserve and other. NESO's dictionary describes
    `SETT_DATE`, titled settlement date, as a payment date.
  how_used:
    - The energy behind each balancing category, half hour by half hour
    - An implied overall cost per MWh, with the cost package for the same periods
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then each yearly file whole unless `last_modified`
      is unchanged (first and newest shown). Everything is bronze only; the workbook lists NESO's
      missing settlement periods.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=daily-balancing-volume-balancing-services-use-of-system"
      - "GET https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/a9b63a05-da9a-4a49-bcf4-13326720ce80/download/q1_vol_fy1718.csv"
      - "GET https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/e781da74-6c35-4296-81dd-250cee869c19/download/q1_vol_fy2627.csv"
      - "GET https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/5cb7f9f2-0c76-4c5c-90f9-8720de1fc85f/download/missing_dates_periods.xlsx"
    commands:
      - {run: gridflow ingest neso_data_portal daily_balancing_volume --last 24h, comment: "every yearly file, bronze only"}
      - {run: gridflow ingest neso_data_portal daily_balancing_volume_files --last 24h, comment: the missing-periods workbook}
  related:
    - {dataset: neso_data_portal/daily-balancing-costs-balancing-services-use-of-system, note: "The costs, in £, for the same settlement periods"}
    - {dataset: neso_data_portal/current-balancing-services-use-of-system-bsuos-data, note: "The BSUoS charges that recover these balancing costs, per settlement run"}
    - {dataset: neso_data_portal/constraint-breakdown, note: "NESO's daily constraint costs by reason, beside these constraint volumes"}
---

# Daily Balancing Services Use of System (BSUoS) Volume Data

A half-hourly table of the **energy volumes, in MWh, behind the day-to-day balancing of the GB
transmission system**, split into eight action categories: energy imbalance, frequency control
offers and bids, positive reserve, constraint offers and bids, negative reserve, and an "other"
bucket. It is the volume companion to the cost file in
@./daily-balancing-costs-balancing-services-use-of-system.md. The cost file prices the same
categories in pounds, and this file gives the energy-volume side. Together they let you ask
how much balancing energy NESO bought in each settlement period and, by dividing, what an
average MWh of each category cost. The package sits under the BSUoS charge. NESO says the
charge recovers the cost of day-to-day operation of the transmission system, is paid by
generators and suppliers, and is calculated daily as a flat tariff for all users. The tariff
and the per-period charge live in @./current-balancing-services-use-of-system-bsuos-data.md,
and the constraint slice is also published daily in @./constraint-breakdown.md.

Despite the word "Daily" in the title, the body is **settlement-period grain** (one row per
settlement date and period) with one wide column per category. The vendor publishes it as one
CSV per financial year (April to March), from 2017-2018 to the current year, plus a workbook
that lists settlement periods absent from the series.

**Read this first.** This family is **captured in bronze but not loaded to silver**. It has
**no registry record**, so no transformer runs. There are no silver rows, no silver views and
no `_latest` view. The reason is in RULINGS 653 (following the RULINGS 538 precedent): the body
has no settlement-run column, and every other BSUoS settlement family in this vendor carries
`run_type` in its key. See "Identity and the blocker" below. **No data values are published on
this page.** Only the schema, counts and vendor definitions are.

- Publisher group: Balancing costs
- Registry group: balancing · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Daily Balancing Volume 2017-2018 | CSV | upload | `a9b63a05-da9a-4a49-bcf4-13326720ce80` |
| Daily Balancing Volume 2018-2019 | CSV | upload | `0481067a-8a0e-465a-85a1-79482fca9307` |
| Daily Balancing Volume 2019-2020 | CSV | upload | `e1043731-cc07-4e41-89a4-596316a663e8` |
| Daily Balancing Volume 2020-2021 | CSV | upload | `b097d727-5adf-4c7c-98e5-4f8914b0f524` |
| Daily Balancing Volume 2021-2022 | CSV | upload | `539cc579-37e1-4b6f-94e5-c26f9ec9be70` |
| Daily Balancing Volume 2022-2023 | CSV | upload | `0cb9b169-a14a-4d1f-b08a-273b21519465` |
| Daily Balancing Volume 2023-2024 | CSV | upload | `66984a1a-4b02-4dd7-9183-425babf23b02` |
| Daily Balancing Volume 2024-2025 | CSV | upload | `62760005-e3bc-4a27-8207-2a2c035055d0` |
| Daily Balancing Volume 2025-2026 | CSV | upload | `ef47829c-4916-4a6d-8554-257b6241026a` |
| Daily Balancing Volume 2026-2027 | CSV | upload | `e781da74-6c35-4296-81dd-250cee869c19` |

The ten CSVs carry the registry disposition `SILVER` → `daily_balancing_volume`. That is the
**intended** target. It is **not realised**: the family has `transformer: null` and no record
(see the blocker below). The package has **no DOC, GIS or COVERED files**.

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Missing Settlement Periods since January 2017 | XLSX | upload | `5cb7f9f2-0c76-4c5c-90f9-8720de1fc85f` | missing-period list (60 SETT_DATE/SETT_PERIOD pairs) — no child record while the parent family has none; the list does not cover all 70 measured gaps. (BAL-1) |
| ↳ Missing_Dates_Periods | — | — | — | HOLD: missing-period list (60 SETT_DATE/SETT_PERIOD pairs) — no child record while the parent family has none; the list does not cover all 70 measured gaps. (BAL-1) |

### Downloads

Every download URL below is the registry/snapshot resource URL (catalogue snapshot
`20261006T195819Z`). The package id is `252b7bd1-7452-41bf-9b60-540cb1c0751a`.

| Resource | Download |
|---|---|
| Daily Balancing Volume 2017-2018 | [q1_vol_fy1718.csv](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/a9b63a05-da9a-4a49-bcf4-13326720ce80/download/q1_vol_fy1718.csv) |
| Daily Balancing Volume 2018-2019 | [q1_vol_fy1819.csv](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/0481067a-8a0e-465a-85a1-79482fca9307/download/q1_vol_fy1819.csv) |
| Daily Balancing Volume 2019-2020 | [q1_vol_fy1920.csv](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/e1043731-cc07-4e41-89a4-596316a663e8/download/q1_vol_fy1920.csv) |
| Daily Balancing Volume 2020-2021 | [q1_vol_fy2021.csv](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/b097d727-5adf-4c7c-98e5-4f8914b0f524/download/q1_vol_fy2021.csv) |
| Daily Balancing Volume 2021-2022 | [q1_vol_fy2122.csv](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/539cc579-37e1-4b6f-94e5-c26f9ec9be70/download/q1_vol_fy2122.csv) |
| Daily Balancing Volume 2022-2023 | [q1_vol_fy2223.csv](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/0cb9b169-a14a-4d1f-b08a-273b21519465/download/q1_vol_fy2223.csv) |
| Daily Balancing Volume 2023-2024 | [q1_vol_fy2324.csv](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/66984a1a-4b02-4dd7-9183-425babf23b02/download/q1_vol_fy2324.csv) |
| Daily Balancing Volume 2024-2025 | [q1_vol_fy2425.csv](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/62760005-e3bc-4a27-8207-2a2c035055d0/download/q1_vol_fy2425.csv) |
| Daily Balancing Volume 2025-2026 | [q1_vol_fy2526.csv](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/ef47829c-4916-4a6d-8554-257b6241026a/download/q1_vol_fy2526.csv) |
| Daily Balancing Volume 2026-2027 | [q1_vol_fy2627.csv](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/e781da74-6c35-4296-81dd-250cee869c19/download/q1_vol_fy2627.csv) |
| Missing Settlement Periods since January 2017 (HOLD) | [missing_dates_periods.xlsx](https://api.neso.energy/dataset/252b7bd1-7452-41bf-9b60-540cb1c0751a/resource/5cb7f9f2-0c76-4c5c-90f9-8720de1fc85f/download/missing_dates_periods.xlsx) |

- Package metadata (catalogue snapshot): created 2020-05-07, last modified 2026-10-03T11:18:24
  (the same instant as the newest resource's `last_modified`); author "National Grid Electricity
  System Operator"; tags Balancing, Bsuos, Daily, Subscribable, Volume; licence id `ESO`.
- Vendor dataset page: <https://www.neso.energy/data-portal/daily-balancing-volume-balancing-services-use-of-system>.
  TODO: verify the portal page slug (taken here from the package name, as for sibling pages).
- **Implementation delta, reconciled.** The registry JSON gives the package `eligibility:
  eligible` and the ten CSVs a `SILVER` disposition. The eligibility report
  (`docs/neso_data_portal/eligibility.md`) lists the family `daily_balancing_volume` as
  "ingest-only (no silver output)" and `daily_balancing_volume_files` as "catalogue only". The
  code has no record. The three agree once you read RULINGS 653 and 538: eligibility (licence and
  format) is satisfied, `SILVER` shows the intended target, and the missing run column alone
  keeps a record from being written. The registry's HOLD reasons for the workbook and its child
  use an ordinary UTF-8 em dash, and the wording is as shown above.

## Families

### `daily_balancing_volume`

- Kind: tabular · archetype: SER · refresh: weekly · empty allowed: no
- ingest-only: no silver yet

Bronze schema at activation, one exact header across all ten CSVs (header H-DV; the 2026-10-16
recapture of 2026-2027 drops the unit brackets, see "Bronze at activation"), 10 columns:
`SETT_DATE`, `SETT_PERIOD`, `Energy Imbalance (MWh)`, `Frequency Control Offers (MWh)`,
`Frequency Control Bids (MWh)`, `Positive Reserve (MWh)`, `Constraint Offers (MWh)`,
`Constraint Bids (MWh)`, `Negative Reserve (MWh)`, `Other (MWh)`. Dates are `%Y-%m-%d` in every
resource. There is no settlement-run column.

| Vendor column | Dtype | Format | Vendor unit | Vendor definition (paraphrased) |
|---|---|---|---|---|
| `SETT_DATE` | date | `%Y-%m-%d` | — (dictionary `unit: ""`) | Titled "Settlement Date"; described as "the Payment Date in relation to an Initial Settlement Run". TODO: verify which date this is (see clocks). |
| `SETT_PERIOD` | integer | — | — (dictionary `unit: ""`) | A 30-minute period beginning on the hour or half-hour. The vendor comment says the first day of BST has 46 periods and the first day of GMT has 50. |
| `Energy Imbalance (MWh)` | number | — | MWh | Difference between energy generated in real time, energy consumed in the same period, and energy sold ahead for it. Signed. |
| `Frequency Control Offers (MWh)` | number | — | MWh | Offers that lift a unit's output so it can provide high-frequency response (mostly needed overnight). |
| `Frequency Control Bids (MWh)` | number | — | MWh | Response bid volume, set by the unit's synchronised position and its upper and lower output limits. |
| `Positive Reserve (MWh)` | number | — | MWh | Operating-reserve volume from the half-hourly reserve requirement and market length, less synchronised headroom. Zero when there is enough headroom or the market is long. |
| `Constraint Offers (MWh)` | number | — | MWh | Submitted offers on a unit to increase its output. |
| `Constraint Bids (MWh)` | number | — | MWh | Submitted bids on a unit to reduce its output. |
| `Negative Reserve (MWh)` | number | — | MWh | Flexibility to reduce generation or increase demand, held to cover unforeseen swings in demand or in demand-side PV and wind. |
| `Other (MWh)` | number | — | MWh | BM actions not covered by the other categories, plus general costs, non-delivery and reconciliation. |

Units come only from the vendor dictionary (K-BAL-1-FACTS BAL-1c; the field-info snapshot
`20261008T114228Z`). No unit is inferred from a column name. The dictionary's text for
`Energy Imbalance` speaks of a "monthly energy imbalance cost", which reads like wording copied
from the cost file. TODO: verify with NESO that the volume column is half-hourly energy in MWh.

The silver column names, types and temporal recipe for this family are **not proposed on this
page**: there is no record, so nothing exists in silver under any name.

#### Bronze at activation

| Resource (financial year) | Bytes | Rows | Vendor `last_modified` (vintage) | Captured (UTC) |
|---|---:|---:|---|---|
| 2017-2018 | 1,166,420 | 17,520 | 2022-10-15T16:36:52 | 2026-10-08T10:04:28 |
| 2018-2019 | 1,169,021 | 17,493 | 2024-03-04T14:42:26 | 2026-10-08T10:04:30 |
| 2019-2020 | 1,207,805 | 17,557 | 2022-09-28T16:18:11 | 2026-10-08T10:04:33 |
| 2020-2021 | 1,203,628 | 17,511 | 2022-09-28T16:18:59 | 2026-10-08T10:04:35 |
| 2021-2022 | 1,180,394 | 17,518 | 2024-03-04T14:44:24 | 2026-10-08T10:04:38 |
| 2022-2023 | 1,173,675 | 17,519 | 2023-04-05T07:59:40 | 2026-10-08T10:04:41 |
| 2023-2024 | 1,170,749 | 17,566 | 2024-04-07T13:21:15 | 2026-10-08T10:04:44 |
| 2024-2025 | 1,179,809 | 17,512 | 2025-05-14T11:11:13 | 2026-10-08T10:04:48 |
| 2025-2026 | 1,206,277 | 17,516 | 2026-04-07T10:24:18 | 2026-10-08T10:04:50 |
| 2026-2027 (to the capture date) | 605,496 | 8,826 | 2026-10-03T11:18:24 | 2026-10-08T10:04:53 |
| **Total** | **11,263,274** | **166,538** | | |

- **Recapture, 2026-10-16.** The 2026-2027 resource was captured again at 2026-10-16T20:01:36Z
  (`daily_balancing_volume/2026/10/16/raw_20261016T200136Z_e781da74-6c35-4296-81dd-250cee869c19_edf40a60.csv`):
  639,451 bytes, 9,306 rows to 2026-10-11, vendor `last_modified` 2026-10-16T06:39:49. Compared
  with the 2026-10-08 capture it keeps every earlier date and period, adds 480 rows, and **changes
  values in 124 rows** on four dates (2026-09-03, 09-04, 09-15 and 09-28), with no run label. Its
  header also drops the brackets around the unit (`Energy Imbalance MWh`, not
  `Energy Imbalance (MWh)`), so header H-DV no longer holds for this file. The other nine
  resources and the workbook still have one capture each. The table above is the activation state.
- At activation, one capture per resource, all `url_type: upload`, all under
  `C:/gridflow-data/bronze/neso_data_portal/daily_balancing_volume/2026/10/08/`. The files are
  named `raw_<stamp>_<resource_id>_<hash>.csv` and each has a `.meta.json` sidecar (SHA-256 of
  the body recorded). Full names are in K-BAL-1-FACTS, "Daily balancing volume" (DV1 to DV10).
- Full-body census (FACTS C02, C03): the settlement date and period pair is unique within each
  resource, and the annual resources are disjoint.
- **Silver: none.** The family was not transformed at the BAL-1 activation (window
  2026-10-08 to 2026-10-10). There is no silver directory and no row count. The reconcile
  (`--all --cutoff 2026-10-10`: exit 0, 122 families, 0 gaps) records it as ingest-only
  (v0.22-RESULTS section "BAL-1", RULINGS 656).

#### The two clocks (proposed, not applied)

No record exists, so neither clock is stamped on any row. The FACTS research proposes the
following for a future record.

- **Vintage clock (`ckan_last_modified`).** `available_at` = `published_at` = the CKAN
  `last_modified` of the resource at the moment gridflow captured it, taken from each capture's
  sidecar (listed in the table above). Every row of one capture would carry the same value.
  The resources are uploads and the body has no issue-time column (issue recipe `none`). The
  vendor does not claim the tables are immutable, so the vintage says when the file was last
  replaced, not when any period's volume became known. The 2017-2022 annual files carry
  vintages from 2022-09 to 2024-03 (see the table above), but TODO: verify whether NESO restates volumes in past years.
- **Event clock (candidate only).** The candidate recipe is the settlement-period pair
  (`sp_pair(sett_date, sett_period)`), with the engine's period arithmetic giving the
  half-hour start. Because there is no record, today **no event time exists in silver at all**
  (and the FACTS research did not propose `none`). TODO: verify what `SETT_DATE` means. Its
  title says settlement date, but its dictionary description calls it a payment date in
  relation to an Initial Settlement Run, and the resources are annual files at settlement-period
  grain. Until that is settled, the candidate is not an independently evidenced event clock.
  The vendor gives no timezone for the date; the volume dictionary refers to GMT/BST
  clock-change days, which implies GB local settlement days. TODO: verify the timezone.

Settlement periods follow the 1 to 50 range: 46 on the spring clock-change day, 50 on the
autumn one.

#### Units

Every value column is **MWh** per the vendor dictionary. `SETT_DATE` and `SETT_PERIOD` carry no
unit. The dictionary's `Energy Imbalance`, `Frequency Control Bids`, `Constraint Bids` and
`Negative Reserve` entries show signed (negative) example values, so those columns are signed.

#### Sentinels and missing values

Full-body census (FACTS g5, C08, C09):

- Numeric cast failures, comma-formatted numbers, currency symbols and percentage tokens:
  **none**. Blank cells and literal `NA` / `N/A`: none are reported for this family.
  TODO: verify the blank and literal-token counts for this family. FACTS lists zero for numeric
  tokens but does not state blank counts for the volume bodies.
- **Numeric `-1` occurs** in five columns: `Energy Imbalance` 2 rows, `Frequency Control Bids`
  26, `Constraint Bids` 48, `Negative Reserve` 89, `Other` 5. No NESO source identifies `-1`
  as a missing-value marker. Treat it as an ordinary signed number: preserve it, do not null it.
- **Long runs of exact zeros** exist (maximum consecutive runs within one resource: constraint
  offers 465, constraint bids 420, negative reserve 351). Zero is a real category value in
  these bodies, not evidence of missing data. No null mapping is proposed.

#### Gaps in the series

The measured gaps in the captured CSVs total **70 missing settlement-period pairs** (FACTS
BAL-1c, C04 and C08), counted against the GB clock-change calendar:

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
| 2026-2027, to the capture date | 6 |
| **Total** | **70** |

The vendor's workbook (below) lists only **60** pairs, and none of those 60 occurs in either
daily CSV family. The workbook is therefore **not** a complete account of the gaps. Do not use it
as a completeness guarantee. The costs file has the same 70 gaps per resource year.

#### Identity and the blocker

- **Candidate grain.** `(SETT_DATE, SETT_PERIOD)` is unique in every resource and disjoint across
  the annual resources (FACTS C03). The vendor names this grain but declares no key constraint.
- **The blocker.** The body carries **no settlement-run column**. The vendor's only run reference
  is the phrase "Initial Settlement Run" in the `SETT_DATE` description, and that does not establish
  that every value is from the Initial (`II`) run. Every BSUoS settlement family in this vendor keys
  on `run_type` (`II` Interim Initial, `SF` Settlement Final, `RF` Reconciliation Final), because a
  settlement day is recomputed in successive runs and the same date and period then appears
  more than once with different values. gridflow never dedups settlement data on date and period
  alone (project rule), and a record's `run_type_column` must name an **existing** string column
  that is part of the entity key. The record model has no way to generate a constant column. A
  record keyed on date and period alone would therefore break the rule, and a made-up constant
  run would invent a vendor fact.
- **Ruling.** RULINGS 653 (T1 spec K-BAL-1-SPEC): daily costs and volume get **no record**, class 3,
  on the RULINGS 538 precedent. The family stays ingest-only.
- **What settles it** (FACTS BAL-1a): (a) NESO publishes a run-bearing body or states the run of
  the file; (b) a vendor run identifier plus a separately approved constant-column mechanism in
  the record model; or (c) an explicit ruling changing the run-carriage rule for this
  publication. TODO: verify with NESO which settlement run the volumes come from.
- Repo pin: `tests/unit/test_neso_bal1_records.py::test_the_daily_families_are_reported_ingest_only_and_the_files_holds_carry_the_reason`
  fails if the eligibility report stops listing the family as ingest-only, or if the workbook
  stops being HOLD with the 60-pairs / 70-gaps reason.

### `daily_balancing_volume_files`

- Kind: files · archetype: SER · refresh: weekly · empty allowed: no
- files: catalogue only

This family holds the one workbook, `Missing Settlement Periods since January 2017`
(resource `5cb7f9f2-0c76-4c5c-90f9-8720de1fc85f`, XLSX, upload). It is **catalogue only** and
its disposition is `HOLD`: there is no child record while the parent family has none.

| Property | Value |
|---|---|
| Sheet | `Missing_Dates_Periods` (tabular, populated) |
| Header | `SETT_DATE`, `SETT_PERIOD` at row 1 |
| Data bounds | `A2:B61`: 60 data rows |
| Unique pairs | 60 |
| Overlap with the CSV observations | none (the 60 pairs are absent from both daily CSV families) |
| Bytes | 11,076 |
| Capture | `C:/gridflow-data/bronze/neso_data_portal/daily_balancing_volume_files/2026/10/08/raw_20261008T100457Z_5cb7f9f2-0c76-4c5c-90f9-8720de1fc85f_9e601263.xlsx` |
| Vendor `last_modified` (vintage) | 2025-08-08T09:48:20 |
| Body SHA-256 prefix | `9e601263` (identical to the costs package's workbook) |

- The sheet is data, not documentation, so it is not DOC. It is a list of absent observations,
  so no value-bearing CSV covers it, and it is not COVERED either.
- The costs package ships a byte-identical workbook. A future cross-package COVERED nomination
  could rely on that, but it still needs a nominated covering output and the ADR-037 harness.
- **Clocks (not applied).** Vintage would be `ckan_last_modified` from the sidecar. The event
  clock would be a settlement-period pair if the sheet is ever given a record. TODO: freeze a
  child contract: exception-list semantics, date recipe, identity, run scope and selection
  policy. Only then can SILVER routing replace the HOLD.
- No unit applies. The sheet has no value columns.

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Weekly

The vendor catalogue says weekly. At activation the newest resource's `last_modified` was
2026-10-03, while the other nine resources' dates run from 2022-09-28 to 2026-04-07. Each capture
is its own vintage. The 2026-10-16 recapture of the 2026-2027 file (`last_modified`
2026-10-16T06:39:49) shows a weekly update **rewrites** the current-year file: it appends new
periods and also restates earlier ones (124 rows on four September dates changed). TODO: verify
with NESO which settlement run each restatement reflects.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: <https://www.neso.energy/data-portal/ngeso-open-licence>. Any derived output must
carry the attribution line above verbatim.

## Holds

- **Family hold (no record).** `daily_balancing_volume` has no silver output. The block is
  structural (the body has no run column, RULINGS 653), not an E-SEM semantics question, and it
  is settled by one of the three routes under "Identity and the blocker". No data values are
  published on this page.
- **File hold.** The missing-period workbook (`daily_balancing_volume_files`) is held until a
  child record exists. The hold question is how the exception list should be modelled
  (semantics, date recipe, identity, run scope, selection policy). Unit: BAL-1.
- **Open semantics questions for NESO** (not holds on a published output, because nothing is
  published): the meaning of `SETT_DATE` (settlement date or payment date), the settlement run
  of the volumes, the timezone of the date, and the blank-cell policy. Each appears above as a
  `TODO: verify`.

## References

- @../README.md — NESO Data Portal vendor page (CKAN, file-download model)
- @./daily-balancing-costs-balancing-services-use-of-system.md — the cost companion (same run-carriage blocker, same 70 gaps, byte-identical workbook)
- @./current-balancing-services-use-of-system-bsuos-data.md — the run-keyed BSUoS charge files (II, SF, RF)
- @./constraint-breakdown.md · @./bsuos-fixed-tariffs.md — BSUoS siblings from the same batch
- gridflow `docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (vintage clock), `ADR-034-neso-generic-silver-engine.md` (generic engine, `_latest`), `ADR-037` (COVERED harness), `ADR-039` / `ADR-040` (whole-capture identity, adjudication)
- gridflow `.planning/phases/v0.22-K-BAL-1/K-BAL-1-FACTS.md` (BAL-1a, BAL-1c, g1 to g5, "Daily balancing volume", "`daily_balancing_volume_files`") and `VERIFICATION.md`
- gridflow `.planning/v0.22-RESULTS.md` section "BAL-1"; RULINGS 538, 653, 655, 656
- gridflow registry `src/gridflow/connectors/neso_data_portal/registry/daily-balancing-volume-balancing-services-use-of-system.json`; eligibility report `docs/neso_data_portal/eligibility.md`
