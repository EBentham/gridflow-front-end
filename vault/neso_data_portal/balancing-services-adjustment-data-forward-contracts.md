---
source: "neso_data_portal"
package: "balancing-services-adjustment-data-forward-contracts"
dataset_key: "bsad_forward_contracts"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Balancing Services Adjustment Data (BSAD) Forward Contracts

This package is NESO's half-hourly record of **forward-contract balancing adjustments**, one row per
GB settlement period. Balancing Services Adjustment Data (BSAD) is how NESO reports to the Balancing and
Settlement Code (BSC) the balancing actions it takes **outside the Balancing Mechanism**; the vendor's
package text says it covers those off-mechanism actions and links the BSAD methodology statement
(CKAN package `notes`, @.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json;
[BSAD methodology](https://www.neso.energy/document/110891/download)). The catalogue also describes the
package as updated twice daily; the registry refresh is daily (see Cadence).

**Despite the name, this is not a contract list.** No column of any captured header identifies a
contract, action, trade or party. Every row is a **settlement-period aggregate** of six adjustment
variables as the vendor defines them (K-AS-4 FACTS section 4: "aggregated forward-contract adjustment
variables"): BCA, BSA and BVA on the buy side and SCA, SSA and SVA on the sell side (vendor meanings in the
Units table below). It is not an individual-trade record. `TODO: verify` whether and how these variables
feed the imbalance price or the priced balancing cost and volume; the reviewed vendor text does not say, and
the direction of each adjustment is unresolved (see FORWARD-BSAD-SIGN-CONVENTION under Known issues).

**What this package is not.**

- It is **event data, not a forecast**: `issue: none`, no forecast exemption applies, and there is **no
  `run_type`** and no settlement-run or revision column (the registry therefore never deduplicates on
  `(date, period)`; identity is `resource_id` + date + period).
- It is **not the aggregated BSAD** (a different table with different columns, see
  @./aggregated-bsad.md) and **not the disaggregated BSAD** (action-level rows, see
  @./disaggregated-bsad.md, ingest-only). Do not add or join these tables on date and period without
  reading each page.
- It is **not delivered in one table**: the vendor publishes one resource per financial year (April to
  March), 11 resources from 2016-17 to 2026-27, and gridflow keeps them as one family partitioned by
  resource.

See @../../../20-domain/concepts/settlement-period.md and
@../../../20-domain/markets/imbalance-price.md for the market context.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| BSAD Forward Contracts 2016-17 | CSV | upload | `30ba12a9-9a9e-4dbb-a69e-ad256d274b04` |
| BSAD Forward Contracts 2017-18 | CSV | upload | `16fe508d-27da-4282-b8af-1fa519b6f480` |
| BSAD Forward Contracts 2018-19 | CSV | upload | `0e7f8536-b449-4f04-a5f5-d08e8121c8c4` |
| BSAD Forward Contracts 2019-20 | CSV | upload | `7ce8164f-0f0c-4940-b821-ca232e2eefaf` |
| BSAD Forward Contracts 2020-21 | CSV | upload | `5d0f2119-1ba6-4d7d-8db5-ea4e23720aa9` |
| BSAD Forward Contracts 2021-22 | CSV | dump | `c435e464-f4d5-4ec2-b8f5-693416e22baa` |
| BSAD Forward Contracts 2022-23 | CSV | dump | `38f74f2c-f735-46fb-8e26-32545011a310` |
| BSAD Forward Contracts 2023-24 | CSV | dump | `56e8e727-3ef9-4b0a-bd06-756cbf5df2fc` |
| BSAD Forward Contracts 2024-25 | CSV | dump | `93f9bdde-1fd9-4619-99e2-d1c5e38239e1` |
| BSAD Forward Contracts 2025-26 | CSV | dump | `9382cd2a-656d-4a0a-a82e-eb26cd8bf7f7` |
| BSAD Forward Contracts 2026-27 | CSV | dump | `449c73a6-a7fd-4166-91f0-3dd1a0e0bb14` |

All 11 resources are disposition **SILVER** (family `bsad_forward_contracts`). There are **no DOC files**
in this package. The package's own page link is `https://extranet.nationalgrid.com/BSAD/` (CKAN `url`).
Each resource has one bronze capture (2026-10-08); the table below gives the vendor download location, the
CKAN `last_modified` the catalogue showed on 2026-10-06, the header epoch, and what happened at the
activation transform (@.planning/v0.22-RESULTS.md section AS-4a; RULINGS 759, 760).

| Resource (FY) | Download | CKAN `last_modified` | Header epoch | Silver rows | Outcome |
|---|---|---|---|---:|---|
| 2016-17 | [CSV upload](https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/30ba12a9-9a9e-4dbb-a69e-ad256d274b04/download/bs_forwardcontract_01-04-2016_31-03-2017.csv) | 2019-12-13T13:00:26 | 1 | 0 | **failed**: `DuplicateEntityKeyError` (ADR-040 adjudicated) |
| 2017-18 | [CSV upload](https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/16fe508d-27da-4282-b8af-1fa519b6f480/download/bs_forwardcontract_01-04-2017_31-03-2018.csv) | 2019-12-13T13:00:03 | 1 | 17,520 | loaded |
| 2018-19 | [CSV upload](https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/0e7f8536-b449-4f04-a5f5-d08e8121c8c4/download/bs_forwardcontract_01-04-2018_31-03-2019.csv) | 2019-12-13T12:59:35 | 1 | 17,520 | loaded |
| 2019-20 | [CSV upload](https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/7ce8164f-0f0c-4940-b821-ca232e2eefaf/download/bs_forwardcontract_01-04-2019_31-03-2020.csv) | 2020-04-02T19:09:59 | 1 | 17,568 | loaded |
| 2020-21 | [CSV upload](https://api.neso.energy/dataset/ca51d03a-53e8-4397-aee1-2f40f9973b96/resource/5d0f2119-1ba6-4d7d-8db5-ea4e23720aa9/download/data.csv) | 2021-11-25T18:16:36 | 1 | 0 | **failed**: `DuplicateEntityKeyError` (ADR-040 adjudicated) |
| 2021-22 | [datastore dump](https://api.neso.energy/datastore/dump/c435e464-f4d5-4ec2-b8f5-693416e22baa) | 2022-03-31T12:40:18 | 2 | 17,520 | loaded |
| 2022-23 | [datastore dump](https://api.neso.energy/datastore/dump/38f74f2c-f735-46fb-8e26-32545011a310) | 2023-01-23T16:28:36 | 2 | 17,520 | loaded |
| 2023-24 | [datastore dump](https://api.neso.energy/datastore/dump/56e8e727-3ef9-4b0a-bd06-756cbf5df2fc) | none (null) | 2 | 17,568 | loaded |
| 2024-25 | [datastore dump](https://api.neso.energy/datastore/dump/93f9bdde-1fd9-4619-99e2-d1c5e38239e1) | none (null) | 2 | 17,520 | loaded |
| 2025-26 | [datastore dump](https://api.neso.energy/datastore/dump/9382cd2a-656d-4a0a-a82e-eb26cd8bf7f7) | none (null) | 2 | 17,520 | loaded |
| 2026-27 | [datastore dump](https://api.neso.energy/datastore/dump/449c73a6-a7fd-4166-91f0-3dd1a0e0bb14) | none (null) | 2 | 9,168 | loaded (in progress year) |

Total **149,424 silver rows** from 9 resources, 0 validation failures, 0 rows excluded (the reader
counted and removed wholly blank trailing rows in the 2017-18 to 2019-20 uploads, 15 in total; that is a
faithful read of empty rows, not an exclusion). Silver covers settlement days `2017-04-01` to
`2026-10-08`; **the 2016-17 and 2020-21 financial years are absent** because their captures failed
(see Holds).

## Families

### `bsad_forward_contracts`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `settlement_date` | date | `%d/%m/%Y` | no | — | — |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| BCA (£) | `bca` | float64 | — | yes | — | — |
| BSA (MWh) | `bsa` | float64 | — | yes | — | — |
| BVA (MWh) | `bva` | float64 | — | yes | — | — |
| SCA (£) | `sca` | float64 | — | yes | — | — |
| SSA (MWh) | `ssa` | float64 | — | yes | — | — |
| SVA (MWh) | `sva` | float64 | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `settlement_date` | date | `%Y-%m-%d` | no | — | — |
| SettlementPeriod | `settlement_period` | int64 | — | no | — | — |
| BCA | `bca` | float64 | — | yes | — | £ |
| BSA | `bsa` | float64 | — | yes | — | MWh |
| BVA | `bva` | float64 | — | yes | — | MWh |
| SCA | `sca` | float64 | — | yes | — | £ |
| SSA | `ssa` | float64 | — | yes | — | MWh |
| SVA | `sva` | float64 | — | yes | — | MWh |

- Entity key: `resource_id`, `settlement_date`, `settlement_period`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`settlement_date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Epochs.** Epoch 1 (the profiler's F-H0) is the uploaded financial years 2016-17 to 2020-21: header
`Date, Settlement Period, BCA (£), BSA (MWh), BVA (MWh), SCA (£), SSA (MWh), SVA (MWh)` with dates as
`dd/mm/yyyy`. Epoch 2 (F-H1) is the datastore years 2021-22 onward: `Date, SettlementPeriod, BCA, BSA,
BVA, SCA, SSA, SVA` with dates as `yyyy-mm-dd`. The epochs differ in column names, not only in transport.
A header outside the two epochs fails loudly. The silver names are harmonised across the epochs and every
value column is `float64` (not the profiler's integer drafts). `settlement_period` is bounded `1..50`.

**The two clocks.**

- **Vintage clock (when gridflow could have known the row).** `ckan_last_modified` is **not** used for
  this family: it mixes upload and datastore resources and the rule (V-8) forbids it for a family holding a
  datastore resource. The record uses `capture_fallback`, so `available_at` is the gridflow capture time
  (sidecar `written_at`): every silver row carries a 2026-10-08 `available_at` and `published_at` is null.
  The CKAN `last_modified` values in the table above are recorded for reference only (four of the
  datastore resources have none). A backtest therefore cannot use this table to say when a past adjustment
  became known; **original submission time is not published** (`TODO: verify` whether NESO or the BSC
  retain it).
- **Event clock (the temporal recipe).** `sp_pair(settlement_date, settlement_period)`: `event_time`
  (equal to `timestamp_utc` in silver) is the **UTC start instant of the GB settlement period**. The
  settlement day is the UK local day, period 1 starts at 00:00 local (the vendor dictionary: "Settlement
  period 1 runs from 00:00-00:30"), and the pair is converted to UTC at the silver boundary. In silver this
  gives, for example, 2023-10-29 period 1 at `2023-10-28T23:00Z` and period 50 at `2023-10-29T23:30Z`.
  Of the populated rows, 27 have a period start after their capture time (the open 2026-27 year), so no
  forward-only exemption is claimed.

**Settlement periods and daylight saving.** Periods are `1..50`, not `1..48`. Silver holds 8 autumn
days of 50 periods (2017-10-29, 2018-10-28, 2019-10-27, 2021-10-31, 2022-10-30, 2023-10-29, 2024-10-27,
2025-10-26), 8 spring days of 46 (2018-03-25, 2019-03-31, 2020-03-29, 2022-03-27, 2023-03-26, 2024-03-31,
2025-03-30, 2026-03-29), and 48 otherwise; the 2019-20 and 2023-24 years have 17,568 rows (leap years).
The 2020-21 autumn and spring days are absent with the failed 2020-21 capture.

**Units (vendor dictionary only, never inferred from a column name).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/bsad_forward_contracts.json, K-AS-4 FACTS
section 4):

| Silver column | Vendor meaning | Unit |
|---|---|---|
| `bca` | Net buy price cost adjustment | £ |
| `bsa` | Gross volume purchased (trades) | MWh |
| `bva` | Net buy price volume adjustment | MWh |
| `sca` | Net sell price cost adjustment | £ |
| `ssa` | Gross volume sold (trades) | MWh |
| `sva` | Net sell price volume adjustment | MWh |

`settlement_period` is an ordinal with no unit. The epoch-1 header suffixes `(£)` / `(MWh)` agree with
the dictionary; the generated epoch-1 schema table shows no unit because the unit is read from the
dictionary, not the header. The dictionary text says the date is "Given in UTC or UTC+1 during British
Summer Time", which is the UK settlement-day convention used above.

**Typing and sentinels (K-AS-4 FACTS g5, g6).** Zeros are real values and stay zero; blank cells would
stay null (none occur in the loaded silver). There is **no sentinel token**: no `NA` / `N/A`, no padded or
separator-bearing number, no percent sign, no embedded quote, comma or newline. Values are kept exactly as
published, **signed**; no bounds, sign flip, abs or netting is applied. One cell is a literal `-1` (see
Known issues). All captured bodies are valid UTF-8.

**Row counts per family in silver:** 149,424 (9 resources; the two failed captures would have added
17,522 and 17,536 populated rows).

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The vendor text says the package updates twice daily (CKAN `notes`). gridflow holds **one capture per
resource** (all 2026-10-08), so the real rhythm, whether a financial-year resource is extended in place
each day for the current year (2026-27 had 9,168 rows to 2026-10-08, with 27 period starts after the
capture), and whether earlier years are ever amended or deleted are unmeasured: `TODO: verify` by
comparing later complete captures with the hash-pinned bodies (K-AS-4 FACTS section 2.2). The BSAD
methodology permits corrections and later inclusion of contracts, so earlier rows may be revised.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow
outputs derived from this package carry the attribution line "Supported by National Energy SO Open Data".

## Holds

- none

**No output of this package is held**: the family is eligible and its loaded values are published. Two
captures are **adjudicated failures** (ADR-040 `failed`, ruling 748, ratified 749), unloaded and kept with
their failure records; this is not a hold on the family. Reconcile `--all` at cutoff 2026-10-12 was clean
with the 5 captures of AS-4a adjudicated across both BSAD families (RULINGS 760, 198 families, 0 gaps).

| Capture | Cause | Why |
|---|---|---|
| 2016-17 (`30ba12a9-...`, hash prefix `f0aeb0c5`) | `DuplicateEntityKeyError` | repeats 2 settlement periods with identical rows (17,522 populated rows, 17,520 distinct pairs) |
| 2020-21 (`5d0f2119-...`, hash prefix `070a68c3`) | `DuplicateEntityKeyError` | repeats 16 settlement periods with **conflicting values**, no revision label or precedence rule (17,536 rows, 17,520 distinct pairs) |

For 2020-21 the repeated 2020-08-25 period 1 appears once with non-zero buy and sell volumes and once with
every column zero; the same conflict occurs for the next repeated period (K-AS-4 FACTS section 4). gridflow
**never deduplicates, picks the last row, adds value columns to the key or invents an occurrence index**.

Ledger questions (carried verbatim as non-holding `TODO:`s):

- `TODO: verify` which value set is authoritative for the repeated 2020-21 settlement periods (for
  example 25/08/2020 period 1), and what the repeated identical 2016-17 row means.

**Known issues and gotchas.**

- **Two financial years are missing from silver** (2016-17 and 2020-21), above. A consumer of a long
  history must treat 2016-04-01 to 2017-03-31 and 2020-04-01 to 2021-03-31 as not loaded rather than zero.
- **Sign convention unresolved.** `TODO: verify` FORWARD-BSAD-SIGN-CONVENTION: the reviewed sources do not
  settle the sign of every historical aggregate variable or every negative gross-volume correction. The
  split buy and sell columns are not a signed individual-action volume. No nonnegative bound, sign flip or
  netting recipe is applied, and none should be assumed.
- **A literal `-1` in `bsa`.** One cell: 2024-25 resource, 2025-01-08 period 39, `bsa = -1.0`. No vendor
  source defines it as missing. It stays numeric `-1.0`, not null. `TODO: verify` FORWARD-BSA-MINUS-ONE:
  signed correction or sentinel.
- **Blank trailing rows in the 2017-18 to 2019-20 uploads** (five per body, 15 removed);
  they are empty rows, not data.
- **Mixed vintage is capture time, not publication time**: see the two clocks. The 2026-10-08 `available_at`
  applies to all history.
- **No `run_type`, no revision column.** Never deduplicate on `(date, period)`; the resource partition is
  the only disambiguator, and measured settlement pairs are disjoint across the resources (zero shared
  pairs in the 55 pair comparisons across all 11 resources in FACTS section 4; silver's 149,424 rows hold
  149,424 distinct settlement date and period pairs), so no overlap adjudication is needed.
- **The package name is misleading** (see Overview): no contract, trade or party identifier exists in the
  data.
- **Related but different tables.** The aggregated BSAD (@./aggregated-bsad.md) carries different columns
  and has its own encoding and duplicate-key failures and an unresolved sign question; the disaggregated
  BSAD (@./disaggregated-bsad.md) is ingest-only. The three BSAD tables were activated together in AS-4a
  (the third has no silver record); do not sum or join them without reading their pages.
