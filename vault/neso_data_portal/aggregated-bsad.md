---
source: "neso_data_portal"
package: "aggregated-bsad"
dataset_key: "aggregated_bsad"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Aggregated Balancing Services Adjustment Data (BSAD)

Balancing Services Adjustment Data (BSAD) is how the System Operator reports the cost and volume of balancing
actions taken **outside the Balancing Mechanism** to the Balancing and Settlement Code (BSC), so that they can
be reflected in the imbalance cash-out prices. The vendor's package text describes it as the data used to
submit balancing actions to the BSC for actions "outside of the balancing mechanism" and points to the BSAD
methodology statement (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[Aggregated BSAD](https://www.neso.energy/data-portal/aggregated-bsad); methodology
[BSAD methodology statement](https://www.neso.energy/document/110891/download)). This package is the
**aggregated** flavour: **one row per settlement period**, carrying the net adjustment terms (energy and system
volumes, energy cost, and a buy and a sell price adjuster) and **no individual action**. The per-action flavour
is the sibling package @./disaggregated-bsad.md, and the forward-contract flavour is
@./balancing-services-adjustment-data-forward-contracts.md. Background:
@../../../20-domain/instruments/bsad-disbsad.md (the Elexon-side NETBSAD / DISBSAD pair, @../../elexon/datasets/netbsad.md;
`TODO: verify` how the NESO aggregated columns map onto the Elexon NETBSAD fields before treating the two as the
same quantity).

**What a model gets from it, and what it does not.**

- The only column that carries information in the captured data is the **buy price adjuster `bpa`**: it is non-zero
  in 3,181 of the 166,944 loaded rows (2016 to 2026). **Every cost and volume column (`ebca`, `ebva`, `sbva`, `esca`,
  `esva`, `ssva`) and the sell price adjuster `spa` is exactly zero in every loaded row.** Zero is a published
  value, not a missing one, and gridflow keeps every column. The BSC interface documentation explains why the
  superseded energy and system adjustment fields continue to be carried as zero; it does not license dropping the
  columns (K-AS-4-FACTS section 3, BSC interface definition document part 1).
- It is a set of **settlement-period event records, not forecasts**: `issue: none`, no forecast issue time, no
  `run_type`, no revision column. gridflow never invents a settlement run and **never deduplicates on (date, period)
  alone**; the identity is (`resource_id`, `settlement_date`, `settlement_period`).
- The methodology permits **amended and post-event submissions**, so the published values are not an immutable
  record and no original submission instant is published (see Known issues).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Aggregated BSAD 2013-14 | CSV | upload | `d39fcf5e-32f9-4e44-a69d-b622effc165d` |
| Aggregated BSAD 2014-15 | CSV | upload | `44851379-3eeb-426f-81ea-a4bc34f6edbb` |
| Aggregated BSAD 2016-17 | CSV | upload | `15950c77-8f7d-4d12-8f29-25eaab6a5155` |
| Aggregated BSAD 2017-18 | CSV | upload | `6ecea816-d98a-4174-80b2-1536765fe711` |
| Aggregated BSAD 2018-19 | CSV | upload | `8d56ca90-0258-4380-b12d-88bf7a9606d7` |
| Aggregated BSAD 2019-20 | CSV | upload | `cfb65cd4-e41c-4587-9c78-31004827bee6` |
| Aggregated BSAD 2020-21 | CSV | upload | `ec526741-f629-4620-9e31-d14da373392e` |
| Aggregated BSAD 2021-22 | CSV | dump | `6fee3fb4-6cff-4c32-b22e-e39d1b16b03e` |
| Aggregated BSAD 2022-23 | CSV | dump | `412e22d3-542f-4811-8f13-40537193022f` |
| Aggregated BSAD 2023-24 | CSV | dump | `36070f3e-3d73-4776-8fb3-da9e76d4bf82` |
| Aggregated BSAD 2024-25 | CSV | dump | `604e265b-ec58-4655-b467-988e2ed5d82d` |
| Aggregated BSAD 2025-26 | CSV | dump | `06a87c3d-d214-469b-84d6-ad05d745433c` |
| Aggregated BSAD 2026-27 | CSV | dump | `44d1e962-1791-4f33-957b-9f090ffc4359` |

All 13 resources are dispositioned `SILVER` and are **CSV**. The package has **no documentation (DOC) files**: the
catalogue snapshot of 2026-10-06 lists 13 resources and every one is a data file, so there is no DOC download to
link. The data files are one resource per financial year (April to March), each downloadable from the URL the
vendor publishes (CKAN, @.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json):

| Financial year | Download | Silver rows | Loaded? |
|---|---|---:|---|
| 2013-14 | [bs_netbsd_01-04-2013_31-03-2014.csv](https://api.neso.energy/dataset/69c869a5-e6c6-4f48-852b-395a05882ef9/resource/d39fcf5e-32f9-4e44-a69d-b622effc165d/download/bs_netbsd_01-04-2013_31-03-2014.csv) | 0 | **No: recorded failure** (`UnicodeDecodeError`) |
| 2014-15 | [bs_netbsd_01-04-2014_31-03-2015.csv](https://api.neso.energy/dataset/69c869a5-e6c6-4f48-852b-395a05882ef9/resource/44851379-3eeb-426f-81ea-a4bc34f6edbb/download/bs_netbsd_01-04-2014_31-03-2015.csv) | 0 | **No: recorded failure** (`UnicodeDecodeError`); also only part of the year |
| 2015-16 | none published | 0 | **Not in the vendor catalogue** |
| 2016-17 | [bs_netbsd_01-04-2016_31-03-2017.csv](https://api.neso.energy/dataset/69c869a5-e6c6-4f48-852b-395a05882ef9/resource/15950c77-8f7d-4d12-8f29-25eaab6a5155/download/bs_netbsd_01-04-2016_31-03-2017.csv) | 17,520 | Yes |
| 2017-18 | [bs_netbsd_01-04-2017_31-03-2018.csv](https://api.neso.energy/dataset/69c869a5-e6c6-4f48-852b-395a05882ef9/resource/6ecea816-d98a-4174-80b2-1536765fe711/download/bs_netbsd_01-04-2017_31-03-2018.csv) | 17,520 | Yes |
| 2018-19 | [bs_netbsd_01-04-2018_31-03-2019.csv](https://api.neso.energy/dataset/69c869a5-e6c6-4f48-852b-395a05882ef9/resource/8d56ca90-0258-4380-b12d-88bf7a9606d7/download/bs_netbsd_01-04-2018_31-03-2019.csv) | 17,520 | Yes |
| 2019-20 | [bs_netbsd_01-04-2019_31-03-2020.csv](https://api.neso.energy/dataset/69c869a5-e6c6-4f48-852b-395a05882ef9/resource/cfb65cd4-e41c-4587-9c78-31004827bee6/download/bs_netbsd_01-04-2019_31-03-2020.csv) | 17,568 | Yes |
| 2020-21 | [data.csv](https://api.neso.energy/dataset/69c869a5-e6c6-4f48-852b-395a05882ef9/resource/ec526741-f629-4620-9e31-d14da373392e/download/data.csv) | 0 | **No: recorded failure** (`DuplicateEntityKeyError`) |
| 2021-22 | [datastore dump](https://api.neso.energy/datastore/dump/6fee3fb4-6cff-4c32-b22e-e39d1b16b03e) | 17,520 | Yes |
| 2022-23 | [datastore dump](https://api.neso.energy/datastore/dump/412e22d3-542f-4811-8f13-40537193022f) | 17,520 | Yes |
| 2023-24 | [datastore dump](https://api.neso.energy/datastore/dump/36070f3e-3d73-4776-8fb3-da9e76d4bf82) | 17,568 | Yes |
| 2024-25 | [datastore dump](https://api.neso.energy/datastore/dump/604e265b-ec58-4655-b467-988e2ed5d82d) | 17,520 | Yes |
| 2025-26 | [datastore dump](https://api.neso.energy/datastore/dump/06a87c3d-d214-469b-84d6-ad05d745433c) | 17,520 | Yes |
| 2026-27 | [datastore dump](https://api.neso.energy/datastore/dump/44d1e962-1791-4f33-957b-9f090ffc4359) | 9,168 | Yes (year in progress; to 2026-10-08) |

**Ten of the 13 resources load, giving 166,944 silver rows** (activation 2026-10-08, window
`2026-10-08..2026-10-08`, no prior silver; @.planning/v0.22-RESULTS.md section AS-4a; RULINGS 760). **Three
resources are recorded failures, not holds**: the 2013-14 and 2014-15 uploads (`UnicodeDecodeError`) and the
2020-21 upload (`DuplicateEntityKeyError`). They stay unloaded with their failure records, and the failures were
adjudicated for reconciliation under ADR-040 (RULINGS 748, 749; family section below). The three unloaded bronze
bodies hold 38,093 populated logical rows; the 13 bodies hold 205,057 logical rows in total, of which 20 are wholly
blank rows removed by the reader (5 each in the 2016-17 to 2019-20 uploads), so 205,057 - 38,093 - 20 = 166,944.
The 2020-21 resource's own description says "financial year 2019-20" (a vendor labelling error; the file name is
`data.csv`).

## Families

### `aggregated_bsad`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1 (the epoch 1 units sit in the header names, shown in the vendor column, so the separate unit column
is left blank; the epoch 2 headers are bare, so its unit column is filled from the vendor dictionary):

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `settlement_date` | date | `%d/%m/%Y` | no | — | — |
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| EBCA (£) | `ebca` | float64 | — | yes | — | — |
| EBVA (MWh) | `ebva` | float64 | — | yes | — | — |
| SBVA (MWh) | `sbva` | float64 | — | yes | — | — |
| BPA (£/MWh) | `bpa` | float64 | — | yes | — | — |
| ESCA (£) | `esca` | float64 | — | yes | — | — |
| ESVA (MWh) | `esva` | float64 | — | yes | — | — |
| SSVA (MWh) | `ssva` | float64 | — | yes | — | — |
| SPA (£/MWh) | `spa` | float64 | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `settlement_date` | date | `%Y-%m-%d` | no | — | — |
| SettlementPeriod | `settlement_period` | int64 | — | no | — | — |
| EBCA | `ebca` | float64 | — | yes | — | £ |
| EBVA | `ebva` | float64 | — | yes | — | MWh |
| SBVA | `sbva` | float64 | — | yes | — | MWh |
| BPA | `bpa` | float64 | — | yes | — | £/MWh |
| ESCA | `esca` | float64 | — | yes | — | £ |
| ESVA | `esva` | float64 | — | yes | — | MWh |
| SSVA | `ssva` | float64 | — | yes | — | MWh |
| SPA | `spa` | float64 | — | yes | — | £/MWh |

- Entity key: `resource_id`, `settlement_date`, `settlement_period`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`settlement_date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Header epochs.** Epoch 1 (the 2016-17 to 2020-21 uploads; the 2020-21 file reads under this header but fails on duplicates, below) uses the upload header with
`(£)`, `(MWh)` and `(£/MWh)` suffixes, `Settlement Period` with a space, and dates as `dd/mm/yyyy`. Epoch 2 (the
2021-22 to 2026-27 datastore dumps) uses bare names, `SettlementPeriod`, and ISO dates `yyyy-mm-dd`; its unit
column above is filled from the vendor dictionary (via K-AS-4-FACTS), not from the header, and is not a registry field. The two epochs also differ in **column
order** (epoch 1 has `SBVA, BPA, ESCA, ESVA, SSVA, SPA` after `EBVA`; both orders map by source name). Each epoch
declares one scalar date format, so no per-file date map is needed. A **third, older header** (`Date, Settlement
Period, EBCA (£), EBVA (MWh), ESCA (£), ESVA (MWh), SBVA (MWh), SSVA (MWh), BPA (£/MWh), SPA (£/MWh)`) appears only
in the 2013-14 and 2014-15 uploads. It is **deliberately not frozen**: those two bodies are not valid UTF-8 and fail
before header matching, and the profiler's replacement-character copy of the header is not trustworthy (K-AS-4-FACTS
section 3, epoch A-H0; seat ruling 4). Silver names are harmonised across the two admitted epochs (one dtype per
name), and every value column is `float64`; the profiler's all-zero-derived integer types were rejected because
all-zero columns do not establish an integral domain. `settlement_period` is bounded `1..50` (not 1..48); no other
bound exists. A header outside the two epochs fails loudly.

**Silver also carries** the engine-stamped columns `resource_id` (the key partition), `timestamp_utc` (equal to
`event_time` for this family; verified for all 166,944 rows), `published_at` (null on every row), `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version` (observed `1+e1` on every
row).

**Two clocks.**

- **Vintage (when it was known): `available_at` = gridflow capture time**, the `written_at` of the bronze sidecar,
  not the CKAN `last_modified`. The family mixes upload and datastore resources, and the record model forbids the
  CKAN `last_modified` vintage on a family that holds a datastore resource (check V-8), so it uses
  `capture_fallback`. The CKAN `last_modified` is therefore **not** used here: it is 2019-2021 for the upload
  resources, 2022-2023 for two dumps and null for the 2023-24 to 2026-27 dumps. Every loaded row carries a
  `available_at` of 2026-10-08 (08:13 to 08:16 UTC), a capture time and not a publication time. A point-in-time
  query (`WHERE available_at <= :as_of`) therefore sees **no** history before 2026-10-08. `published_at` is null.
  `TODO: verify` the original submission or publication instant of each period; none is published.
- **Event time: `event_time` = start of the settlement period**, computed by the established `sp_pair` recipe from
  `settlement_date` and `settlement_period` on the **Europe/London settlement clock** and converted to tz-aware UTC
  at the silver boundary. Example: 2016-04-01 period 1 is 2016-03-31T23:00Z (British Summer Time), so a UTC-looking
  reading of the date alone would be an hour wrong in summer. The vendor dictionary says the date is "given in
  (Coordinated Universal Time) UTC or UTC+1 during British Summer Time" and that period 1 runs 00:00-00:30; the date
  is a settlement-day label, not an issue instant. The silver data covers `event_time` 2016-03-31T23:00Z to
  2026-10-08T22:30Z. Period lengths vary on clock-change days: **9 long days with 50 periods** (2016-10-30,
  2017-10-29, 2018-10-28, 2019-10-27, 2021-10-31, 2022-10-30, 2023-10-29, 2024-10-27, 2025-10-26) and **9 short
  days with 46 periods** (2017-03-26, 2018-03-25, 2019-03-31, 2020-03-29, 2022-03-27, 2023-03-26, 2024-03-31,
  2025-03-30, 2026-03-29) are present and valid; nothing is dropped. Background:
  @../../../20-domain/concepts/settlement-period.md.
- **Rows ahead of their capture.** 29 loaded rows (2026-10-08 periods 20 to 48) have an `event_time` after their
  `available_at`: they are periods that had not yet started when the 2026-27 file was captured at 08:15 UTC. All 29
  have a zero `bpa`. The vintage never claims earlier availability than the capture, so these are safe for a
  point-in-time query, and no forward-only exemption is needed (seat ruling 5). `TODO: verify` what the vendor
  publishes for a not-yet-started period (a forward submission or a placeholder zero).

**Units (vendor dictionary only; nothing converted).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/aggregated_bsad.json) and the dictionary page
([aggregated BSAD dictionary](https://www.neso.energy/data-portal/aggregated-bsad/aggregated_bsad_2026-27)):

| Silver | Vendor title (dictionary) | Unit |
|---|---|---|
| `ebca` | Energy Buy Cost Adjustment (net buy price cost adjustment, energy) | £ |
| `ebva` | Energy Buy Volume Adjustment (net buy price volume, energy) | MWh |
| `sbva` | System Buy Volume Adjustment (net buy price volume adjustment, system) | MWh |
| `bpa` | Buy Price Adjuster | £/MWh |
| `esca` | Energy Sell Cost Adjustment (net sell price cost adjustment, energy) | £ |
| `esva` | Energy Sell Volume Adjustment (net sell price volume adjustment, energy) | MWh |
| `ssva` | System Sell Volume Adjustment (net sell price volume adjustment, system) | MWh |
| `spa` | Sell Price Adjuster | £/MWh |
| `settlement_period` | Settlement Period | ordinal, no physical unit |

The units are the vendor dictionary's (saved field info), as cited in K-AS-4-FACTS (unit rows T02 to T18): `ebca` and
`esca` are `£`, `bpa` and `spa` are `£/MWh`, the volume columns are `MWh`. The pound sign is corroborated by the
epoch 1 upload headers (`EBCA (£)`, `BPA (£/MWh)` and so on), which are the vendor's own text; the saved field-info
file stores it as UTF-8, but tools that decode a legacy upload header lossily show it as a replacement character, so
read the pound sign from the dictionary or FACTS, not from a re-decoded header. Costs are £ per settlement period,
volumes are MWh per settlement period, prices are £/MWh. No unit is inferred from a column name. The registry
record's columns carry no unit field, so the per-column units for epoch 2 are documented only here and in FACTS, not
in the registry JSON.

**Sentinels and typing (K-AS-4-FACTS g5, g6).** No populated cell contains `NA`, `N/A`, a thousands separator, a
percent sign, an embedded quote, comma or newline, and the production CSV reader agreed with a strict second parse on
every row and cell. **No new token is mapped to null.** Blanks stay null (none in the loaded data); **zeros stay
zero**; no sign is flipped and no non-negativity bound is applied (`TODO: verify` the sign convention, below). The
loaded data has no null in any value column. The 2016-17 to 2019-20 uploads end in wholly blank rows (5 each, 20 in
all) that the reader removes and counts; this is not an exclusion.

**Identity and selection.** The measured grain is one row per settlement period per resource. Across the 78
resource-pair comparisons there are **zero shared settlement pairs**, so the resources are disjoint financial years
and no overlap adjudication is needed. `resource_id` stays in the key (the family is resource-partitioned, ADR-039
resource-grain extension), and `latest` is the whole capture of each resource, so a re-capture of a resource replaces
that resource's rows and no other. The loaded resources hold 17,520 settlement pairs each (17,568 for leap years
2019-20 and 2023-24), and 9,168 for the year in progress; all 166,944 rows are unique on the key.

**Recorded failures (ADR-040, ruling 748, ratified in 749).**

| Resources | Cause | Reason | Question for NESO |
|---|---|---|---|
| 2013-14 and 2014-15 uploads | `UnicodeDecodeError` | Each carries a standalone `0xA3` header byte, so neither is valid UTF-8 and both fail under the record's declared encoding. 2013-14 also repeats 18 identical rows; 2014-15 covers only 2014-04-01 to 2014-06-02 (3,024 rows). | Which text encoding do the 2013-14 and 2014-15 Aggregated BSAD uploads use, and can NESO republish them in UTF-8 (and say whether 2014-15 is complete)? |
| 2020-21 upload | `DuplicateEntityKeyError` | The file repeats 11 settlement periods (all-zero rows: 10 on 27/06/2020, periods 1 to 7 and 9 to 11, and 1 on 05/07/2020, period 1), each identical on every column to its twin, so no key is lossless and the duplicate guard fails the capture. | Are the repeated all-zero rows on 27/06/2020 and 05/07/2020 a publication defect, and can NESO publish a corrected 2020-21 file? |

The research recommended a resource-level HOLD for the two legacy uploads; the seat ruled instead that they be
**recorded failures under ADR-040**, as the `brit_ned` encoding failure was, so that a UTF-8 republication re-enters
loudly rather than staying silently held (seat ruling 2, ratified in RULINGS 749). A cp1252 reading recovers the pound
sign, but that does not prove the vendor's encoding and **no per-resource encoding is introduced**. Nothing is
deduplicated, repaired, re-decoded or value-keyed, and the 2020-21 file is not "fixed" by picking a row. Activation
confirmed all three failures at the expected cause (RULINGS 760), and reconciliation of all families then exited 0 with
0 gaps, adjudicating the five failed captures of this package and the forward-contract package together.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The vendor's package text says the dataset "gets updated twice daily"; the registry assumes daily. gridflow has **one
capture per resource** (all 2026-10-08), so the true refresh rhythm, whether a refresh appends to or replaces a file,
whether past financial years are ever amended, and what an amendment looks like are unmeasured. `TODO: verify` by
comparing later captures with the hash-pinned bodies (K-AS-4-FACTS section 2.1). The older financial years carry
CKAN `last_modified` dates of 2019 to 2023 (null for the last four dumps), so the vendor has not touched the upload
files since then, but that is a vendor stamp, not a gridflow measurement.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow outputs derived
from this package carry the attribution line "Supported by National Energy SO Open Data".

## Holds

- none

**No output of this package is held.** The package and its family are eligible, and no hold question or hold unit
applies. The three failed captures above are recorded failures (reconciled and adjudicated, not published and not
silently skipped), not a hold on the family.

**Open questions that do not hold any output** (K-AS-4-FACTS, carried as non-holding TODOs):

- `TODO: verify` the **legacy encoding**: the 2013-14 and 2014-15 uploads, question above.
- `TODO: verify` the **repeated 2020-21 rows** (10 on 27/06/2020 and 1 on 05/07/2020, all zero): question above.
- `TODO: verify` why there is **no 2015-16 resource** (AGGREGATED-BSAD-2015-16). The catalogue snapshot lists 13 resources and
  none is for 2015-16; the dataset page also reports 13 files, so this is a vendor publication gap in the evidence, not
  a profiler or registry omission. NESO's archived resource listing or a vendor reply would settle it. The disaggregated
  package does carry a 2015-16 file (@./disaggregated-bsad.md), which makes the aggregated gap more notable.
- `TODO: verify` the **2014-15 coverage**: the file is labelled for the whole financial year but holds only
  2014-04-01 to 2014-06-02. It would still be partial if it were republished in UTF-8, unless NESO says otherwise.
- `TODO: verify` the **sign convention** of the aggregate cost and volume columns. The sign of individual adjustment
  volumes (buy versus sell) is documented for the disaggregated data; the monetary signs and the aggregate signs are
  not, and the captured aggregate data is all zero apart from `bpa`. Values are kept as published: no sign correction and
  no non-negativity bound is applied.
- `TODO: verify` the **original publication or submission instant** and the **revision behaviour**: the methodology
  permits amended and post-event submissions, but the files carry no issue, revision or run column, so
  immutable availability at an original submission time is not established.
- `TODO: verify` the **date description**: the dictionary example for `Date` is timestamp-shaped
  (`2019-01-04T00:00:00`), but both body formats are date-only (`dd/mm/yyyy` and `yyyy-mm-dd`); gridflow parses the
  bodies as they are.

**Known issues and gotchas.**

- **Four financial years are absent from silver.** 2013-14, 2014-15, 2015-16 and 2020-21 have no rows, so the history
  is 2016-04-01 to 2026-10-08 with a **gap from 2020-04-01 to 2021-03-31** (only the first quarter of calendar 2020,
  from the 2019-20 file, is present). Per-calendar-year counts that include 2020 are partial; do not read the low
  2020 `bpa` activity as a real change.
- **Constant columns.** Seven of the eight value columns are identically zero; a model that scales or correlates them
  will divide by a zero variance. Only `bpa` varies (maximum 159.55 £/MWh in the loaded data, 3,181 non-zero rows,
  falling from 755 in 2016 to a few dozen or fewer a year since 2024: 25 in 2024, 8 in 2025, 19 in 2026 to date). Whether the zeros mean "no adjustment" or "no longer
  reported" is not stated (`TODO: verify`).
- **Same `available_at` for all history.** Every row carries the 2026-10-08 capture time, so a backtest cannot use this
  table to say when a past adjustment became known.
- **Date format differs by file kind.** `dd/mm/yyyy` in the uploads, ISO in the dumps; handled per epoch. The 50-period
  autumn days are real, not duplicates.
- **Not the disaggregated data.** The aggregated rows are net terms for the settlement period; there is no action,
  contract or party identifier, and the aggregated figures cannot be reconciled to the per-action package row by row.
  The disaggregated package has no silver record (its bodies repeat complete rows), so nothing here can be rebuilt
  from it.

Related pages: @./disaggregated-bsad.md, @./balancing-services-adjustment-data-forward-contracts.md,
@../../../20-domain/instruments/bsad-disbsad.md, @../../../20-domain/markets/imbalance-price.md.
