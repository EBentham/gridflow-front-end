---
source: "neso_data_portal"
package: "nsl"
dataset_key: "nsl"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: "NESO does not say rows are unchanged since upload, and archive days and versions are undefined."
  title: North Sea Link transfer limits
  summary: >-
    NESO's hourly limits on flow each way over the North Sea Link interconnector, in MW, with reasons.
  facts:
    vendor: "NESO Data Portal, package `nsl`: a current datastore table and an archive CSV"
    cadence: "Daily, NESO says; one upload a day, at 10:30 GMT in October 2026"
    grain: "Each row: one hour's import and export limits; current rows add upload time"
    history: "NESO's files label hours from 5 October 2022: archive, then the current table"
  landscape: power
  what_it_is: >-
    NESO says it submits these to interconnector capacity calculations, capping GB imports and
    exports, in hourly MW; final capacity can be lower. It says it publishes only restrictions,
    yet its October 2026 files hold many No Restriction rows. It calls them Net Transfer
    Capacity (NTC) restrictions. Every row is day-ahead.
  how_used:
    - Which hours NESO restricted the link, by direction, from the stated reason
    - "A feature for flow and price models: when NESO restricted the link"
    - Set beside the final capacity the link's trading facilitator publishes
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, the current table's dump and the archive CSV. Fetched
      16 October 2026, the table kept every row fetched 8 October unchanged, plus new ones.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=nsl"
      - "GET https://api.neso.energy/datastore/dump/9db51c01-922d-413d-8b67-3938fdc14bdb"
      - "GET https://api.neso.energy/dataset/7bf2e43d-1a24-4a0e-95b0-6ba4eba3daa9/resource/33646e05-1af1-41b5-a056-9e95fb9f0534/download/archived_nsl_link_ntc_data.csv"
    commands:
      - {run: gridflow ingest neso_data_portal nsl --last 24h, comment: "changed files to bronze"}
      - {run: gridflow transform neso_data_portal nsl --last 24h, comment: "the current table to silver"}
  related:
    - {dataset: neso_data_portal/historic-demand-data, note: "North Sea Link's half-hourly flow, in NESO's historic demand files"}
    - {dataset: neso_data_portal/viking, note: "The same NESO limits on Viking Link, with intraday auctions too"}
    - {dataset: neso_data_portal/nemolink, note: "The same NESO limits on NemoLink, with intraday auctions too"}
    - {dataset: neso_data_portal/day-ahead-power-exchange-prices-nordpool, note: "GB's hourly day-ahead price, beside each hour's day-ahead limit"}
---

# North Sea Link - NESO's Net Transfer Capacity

This package holds the restrictions NESO applies to **North Sea Link (NSL)**, the GB–Norway
interconnector. Each row is one hourly operational period with two directional
maximums in MW: the most power that may flow **to GB** (import) and **from GB** (export),
each with a reason text. The package notes say these are "the values submitted by NESO to
the interconnector capacity calculation processes which restrict the maximum GB import and
export interconnector flows", submitted "in MW per hourly time period". They are **limits
NESO submits, not measured flows and not the final capacity**. The vendor note says final
capacity is calculated from NESO's values, the connected system operator's values and the
interconnector's own capability, so it "may be lower than the NESO values shown here", and
the final figures are on the interconnector's trading facilitator's website. The notes also
say values are published only where NESO applied a restriction: "If there are no values,
NESO has not applied a restriction." The files also list unrestricted hours: most current-table
rows carry the reason `No Restriction` (see Sentinels), so a row is an hour NESO gave a limit
for, restricted or not. Use this package to see when and why the GB side
constrained NSL's day-ahead capacity, for example as a feature for GB–Norway flow or
GB price models, alongside measured flows such as the `NSL_FLOW` column of
@./historic-demand-data.md. Sibling packages with the same shape: @./eleclink.md and
@./nemolink.md (current dump plus archive in one family), @./viking.md, @./ifa.md,
@./ifa2.md; the link list is in @./interconnector-register.md.

The package has two CSV resources: a live **current dump** (the datastore, header renamed
on 2026-09-17) and a frozen **archive upload** (2022-10 to 2024-09). gridflow registers both
in one family, `nsl`. Only the current dump is in silver: the archive repeats one whole row,
so no field key can identify its rows and its capture is an adjudicated failed capture
(ADR-040). The silver output is **held** (unit E-SEM; see Holds), so this page gives schema,
row counts, clocks and missingness only, never data values or ranges of values.

- Publisher group: Interconnectors
- Registry group: interconnectors · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Archived NSL NTC Data | CSV | upload | `33646e05-1af1-41b5-a056-9e95fb9f0534` |
| NSL NTC Data | CSV | dump | `9db51c01-922d-413d-8b67-3938fdc14bdb` |

Both resources carry the SILVER disposition in the registry, but only one produces silver.
Downloads and the 2026-10-08 capture of each (sizes, URLs and CKAN `last_modified` from each
sidecar under `C:/gridflow-data/bronze/neso_data_portal/nsl/2026/10/08/`); the current dump was
captured again on 2026-10-16 (below), the archive was not. "Epoch" uses
this page's numbering (the schema tables below).

| Resource | Download | Epoch | Bytes | Data rows | CKAN `last_modified` | Silver |
|---|---|---:|---:|---:|---|---|
| NSL NTC Data (current) | [datastore dump](https://api.neso.energy/datastore/dump/9db51c01-922d-413d-8b67-3938fdc14bdb) | 1 | 1,600,640 | 17,784 | 2026-09-17T08:57:32.333754 | **17,784 rows** |
| Archived NSL NTC Data | [archived_nsl_link_ntc_data.csv](https://api.neso.energy/dataset/7bf2e43d-1a24-4a0e-95b0-6ba4eba3daa9/resource/33646e05-1af1-41b5-a056-9e95fb9f0534/download/archived_nsl_link_ntc_data.csv) | 2 | 1,030,220 | 16,632 | 2024-11-27T13:26:08.527346 | **none** — failed capture, adjudicated |

- **Current dump** (`raw_20261008T111450Z_9db51c01-…_18c54e33.csv`, `url_type: datastore`).
  Loaded normally. The catalogue resource was created 2024-09-23; its description reads
  "NESO's Net Transfer Capacity restrictions submitted to Day-ahead and Intraday auctions".
  CKAN `metadata_modified` at capture was 2026-10-08T10:40:04.892567.
- **Current dump, second capture (2026-10-16; bronze and silver read 2026-10-24)**
  (`raw_20261016T204234Z_9db51c01-…_c6c86a80.csv`, 1,617,906 bytes, 17,976 rows, the same
  header and request URL, CKAN `last_modified` still 2026-09-17T08:57:32.333754,
  `metadata_modified` 2026-10-16T10:40:09.149592). Every one of the 17,784 rows of the
  2026-10-08 body is present with identical values (no key missing, no key with a changed value,
  no full row missing). 192 rows are new: one upload a day, 2026-10-09 to 2026-10-16, each at
  10:30 GMT (`10:30:06` to `10:30:16`), for target hours 2026-10-09 22:00 to 2026-10-17 21:00 UTC;
  749 distinct upload times in all, all rows still `Day Ahead`, no target before its own upload
  time, 17,951 targets before the capture. So between these two captures NESO only appended; that
  does not show rows are never revised, and the hold stands. Silver holds a second Parquet file of
  17,976 rows (`available_at` 2026-10-16T20:42:34.768654Z), which `_latest` takes for the dump's
  `resource_id`. The archive's `last_modified` had not moved, so the 2026-10-16 run did not
  download it (gridflow `client.py` `iter_members`).
- **Archive upload** (`raw_20261008T111452Z_33646e05-…_0519d13a.csv`, `url_type: upload`,
  created 2024-11-27). Note the filename says `nsl_link`, not `nsl`. The body has 16,632 rows
  but only 16,631 distinct complete rows: one whole row appears twice (the 2023-10-29,
  `DayAhead`, version `001`, `22:00 to 23:00` row; CSV records at physical lines 7,825 and
  7,849). A second key group on the `20221030` label shares date, auction, version and hour
  but differs in its export value. Under the family key the capture therefore has 4 rows in
  2 colliding groups, and the transform fails it with `DuplicateEntityKeyError` and writes
  nothing (gridflow `@.planning/phases/v0.22-K-IC-1/post-merge/transform.log`). This is by
  design: gridflow never deduplicates and never adds a row index (K-IC-1 spec §B). The
  failure is recorded in the ADR-040 ledger,
  gridflow `@src/gridflow/connectors/neso_data_portal/registry/_reconcile_adjudications.json`,
  as `family: nsl`, `category: failed`, `cause: DuplicateEntityKeyError`, ruling 565, with the
  open question, verbatim: "Is the repeated 2023-10-29 DayAhead 22:00–23:00 row a publication
  defect, and which value set is authoritative?" Reconcile reports it **adjudicated**, not an
  open gap (RULINGS 567).

There are no DOC resources in this package (two CSVs only), so there is no document to
download. The vendor's package page is [nsl](https://www.neso.energy/data-portal/nsl) and the
archive's dictionary page is
[archived_nsl_ntc_data](https://www.neso.energy/data-portal/nsl/archived_nsl_ntc_data) (empty
dictionary, FACTS T03).

## Families

### `nsl`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data Upload Time GMT | `data_upload_time_gmt` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | ISO 8601 |
| Auction Type | `auction_type` | string | — | yes | — | — |
| Operational Period Start Date and Time GMT | `operational_period_start_gmt` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | ISO 8601 |
| Flow in MW To GB | `flow_to_gb_mw` | float64 | — | yes | — | MW |
| Reason For Restriction To GB | `reason_for_restriction_to_gb` | string | — | yes | — | — |
| Flow in MW From GB | `flow_from_gb_mw` | float64 | — | yes | — | MW |
| Reason For Restriction From GB | `reason_for_restriction_from_gb` | string | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Operational Date | `operational_date` | string | — | yes | — | — |
| Auction Type | `auction_type` | string | — | yes | — | — |
| Version | `version` | string | — | yes | — | — |
| Hourly Time Period (GMT) | `hourly_time_period` | string | — | yes | — | — |
| Flow (MW) To GB | `flow_to_gb_mw` | float64 | — | yes | — | — |
| Flow (MW) From GB | `flow_from_gb_mw` | float64 | — | yes | — | — |
| Reason For Reduction | `reason_for_restriction` | string | — | yes | — | — |

- Entity key: `resource_id`, `issue_time`, `auction_type`, `operational_period_start_gmt`, `operational_date`, `hourly_time_period`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Epochs and resources.** Page epoch 1 is the current dump's header (FACTS "M"); page epoch 2
is the archive's header (FACTS "A"). Each epoch belongs to exactly one resource. The two
epochs share `auction_type`, `flow_to_gb_mw` and `flow_from_gb_mw`; every other column exists
in one epoch only and is null on the other epoch's rows. Because only epoch 1 is loaded,
`operational_date`, `version`, `hourly_time_period` and `reason_for_restriction` are null on
all 17,784 silver rows (measured 2026-10-09).

The current resource's description announced a column-id rename "on 17th September 2026":
`Data Upload Time (GMT)` → `Data Upload Time GMT`, `Operational Period Start Date & Time (GMT)`
→ `Operational Period Start Date and Time GMT`, `Flow (MW) To GB` → `Flow in MW To GB`,
`Flow (MW) From GB` → `Flow in MW From GB`. Only the post-rename header was captured, so the
record has no pre-rename current epoch; none is invented (FACTS IC1-4).

**The two clocks for this family:**

1. **Vintage (`capture_fallback`).** `available_at` is gridflow's **capture time**, the
   bronze sidecar `written_at`, labelled as such; `published_at` is null. This is **not**
   the `ckan_last_modified` vintage used by upload-only NESO families. Record rule V-8 gives
   any family holding a datastore resource `capture_fallback`. The dump's CKAN
   `last_modified` (2026-09-17T08:57:32, the documented column-rename date, three weeks
   before capture) does not evidence when the rows gridflow holds became available
   (gridflow `@docs/DECISION_LOG/ADR-035-neso-datastore-dump-leg.md`; K-IC-1 spec §B; FACTS
   T09). The CKAN `last_modified` values in the resource table are sidecar metadata only.
   Checked against silver on 2026-10-09: one `available_at` on all 17,784 rows,
   2026-10-08T11:14:50.796409Z, equal to `capture_written_at`; `published_at` null on every
   row.
   - **Issue time is a data column, not an availability.** Epoch 1 declares issue
     `data_column(data_upload_time_gmt)`: the vendor dictionary defines `Data Upload Time`
     as the "Date and time that data was published" (GMT; FACTS T01). `issue_time` equals
     `data_upload_time_gmt` on every row; the capture holds 741 distinct publication
     instants. gridflow does **not** backdate `available_at` to it: NESO does not state
     that a dump row is unchanged since its upload time, so an older row's values may have
     been revised before capture (FACTS g2; ADR-035). The archive (epoch 2) has no issue
     column; `Version` is not an issue time.
   - FACTS records that the upload-time labels on inspected DST transitions move between
     `11:30` (winter) and `10:30` (summer) GMT. That is consistent with a fixed UK-local
     publication time, but it is an **inference**, not an availability contract.
2. **Event time (temporal `none`).** The record has no temporal recipe, so **`timestamp_utc`
   is the capture time** (2026-10-08T11:14:50.796409Z) and `event_time` equals it on every
   row. It is **not** the hour the limit applies to. The reason is record rule V-3: a
   temporal column must exist in every epoch, and the archive has no UTC instant (FACTS T07).
   The target hour lives in the data column `operational_period_start_gmt`:
   - It is the **start** of a one-hour period in GMT/UTC. The dictionary: "Hourly Operational
     Period Start Datetime for which restriction applies", and a period of
     `2022-10-20T22:00:00` "means the period of time between 2022-10-20T22:00:00 and
     2022-10-20T23:00:00" (FACTS T02).
   - The DST check confirms GMT, not UK local time: on every transition the 24 distinct
     target hours fall on one UTC date, but would span 23 or 25 hours by London date
     (FACTS IC1-3, C-DST):

     | Transition | Distinct target hours by UTC date | Same targets by Europe/London date |
     |---|---:|---:|
     | 2024-10-27 | 24 | 25 |
     | 2025-03-30 | 24 | 23 |
     | 2025-10-26 | 24 | 25 |
     | 2026-03-29 | 24 | 23 |

   - Silver coverage (2026-10-09): 17,784 distinct target hours, 2024-09-24 22:00 →
     2026-10-09 21:00 UTC, all on whole hours (0 off-hour starts). Every target is after its own upload time.
     Relative to the capture, 17,750 targets were already past and 34 were future.
   - The archive's time columns are **raw labels**, kept as strings: `Operational Date`
     (date-shaped, all parse `%Y%m%d`, but the dictionary is empty) and
     `Hourly Time Period (GMT)` (e.g. `22:00 to 23:00`). How an hour attaches to an
     operational date is undocumented. The labels are irregular around clock changes:
     autumn dates carry 25 rows with `22:00 to 23:00` repeated, spring dates carry 23 with
     `22:00` absent (FACTS IC1-3). Archive labels run `20221005` to `20240924`. `TODO: verify`
     the archive's operational-date calendar and rollover (FACTS T03).

**Units (vendor dictionary only).** Epoch 1 units come from the current resource's field info
(gridflow `@.planning/research/neso-snapshots/field-info/20261008T114228Z/nsl.json`): both
directional flows have unit `MW`, described as "Maximum flow in this direction"; both time
columns have unit `ISO 8601`; `Auction Type` and the reason columns have unit `N/A`
(categorical). The dictionary types the flows as integer; silver stores them as `float64`
(the record's dtype). The **archive dictionary is empty**, so epoch 2 has no dictionary unit
and the generated table shows "—". Its flows are MW on the evidence FACTS cites (T05/T06,
g4): the vendor header text `Flow (MW)` and the package notes ("submitted in MW per hourly
time period"). `Version` has no documented unit or meaning; it is kept as the raw string
(e.g. `001`), never used as an issue time or for ordering. `TODO: verify` the archive
`Version` contract (FACTS T04).

**Direction (FACTS IC1-1).** `flow_to_gb_mw` is the **import** limit (Norway → GB) and
`flow_from_gb_mw` the **export** limit (GB → Norway). Each is a non-negative directional
maximum, not one signed net-flow series; gridflow never signs or nets them. A signed
convention would be a downstream derived definition. No local ENTSO-E series validates these
limits: gridflow's ENTSO-E silver has no GB–Norway rows
(@../../entsoe/datasets/net_transfer_capacity.md is the related ENTSO-E dataset). An
exploratory FACTS comparison used an Ireland area code by mistake and is excluded.

**Auction type.** Every row in both resources is the day-ahead category: `Day Ahead` in the
current dump, `DayAhead` in the archive. Raw spellings are preserved, so the two are
different strings; never whitespace-compact them. The dictionary also lists intraday
auctions (example `Intraday2`), but none appears in the captures (FACTS IC1-2).

**Sentinels and missing values (FACTS g5).** The vendor declares no sentinel, and the record
has no null-token map.

- The directional columns hold no negative values, no `-1`, no non-numeric text and no
  blanks, in either resource. No cell holds a literal `NA` or `N/A`. The dictionary's `N/A`
  comments and units are metadata, not CSV tokens.
- **Zeros stay numeric zero.** No vendor source defines zero as missing, so zero is never
  converted to null or filled with a nameplate capacity.
- **Blank reasons → null**, with no reason invented. The current dump has no blank reason
  cells (0 nulls in either reason column, silver 2026-10-09); the archive has 1,705.
- **Absent rows mean "no NESO restriction"**, per the package notes; that is NESO's word,
  not something the files show. Do not fill gaps with zero, a nameplate capacity or a
  reconstructed limit. The files also list unrestricted hours with the reason `No Restriction`
  (bronze read 2026-10-24): in the 16 October current table 17,952 of 17,976 rows To GB and
  17,592 From GB; in the archive 6,959 of 16,632, plus 1,705 blank reasons.

**Identity and selection (ADR-039).** The family key is the union of each epoch's grain plus
`resource_id`:

- Epoch 1: `(issue_time, auction_type, operational_period_start_gmt)`. This is the vendor's
  own catalogue primary key, which still uses the pre-rename spellings
  (`Data Upload Time (GMT)`, `Auction Type`, `Operational Period Start Date & Time (GMT)`); the
  resource description maps them to the current header (FACTS T08). Measured unique on all
  17,784 silver rows. Record rule V-4 puts `issue_time` in the key because epoch 1 declares
  an issue.
- Epoch 2: `(operational_date, auction_type, hourly_time_period)`, a measured grain, not a
  vendor key. It fails on the archive (see Files by disposition).
- `resource_id` is **not a vendor column**: the engine stamps each row with its capture's
  sidecar resource UUID. On a row, the other epoch's key columns are null.
- `_latest` is `whole_capture` **per `resource_id`** (`latest_partition: resource_id`), so a
  capture of one resource never displaces the other's rows. Today only the current dump has
  a row set.
- Do not dedup on target hour alone: each upload time is a separate issued row.
  `TODO: verify` whether NESO revises a row in place after its `Data Upload Time`.

**Overlap.** The archive's labels end at `20240924 23:00`; the current dump starts at
2024-09-24 22:00 UTC. FACTS found 2 shared keys under literal labels and 0 under a
hypothetical date rollover, with no equal value pairs (FACTS IC1-4). Because the
operational-date calendar is unresolved, cross-resource precedence is `TODO: verify`; it is
moot while the archive is unloaded.

**Activation (2026-10-09, master `6cccc4e`, PR #95).** The frozen record merged
triple-green (RULINGS 566) and was activated with cutoff 2026-10-08 and no prior silver
(RULINGS 567). `nsl` silver has **17,784 rows**, the current resource only, equal to the
plan. The archive capture failed with `DuplicateEntityKeyError` as designed, so the nsl
transform exits 1. Reconcile `--all --cutoff 2026-10-08` exited 0: 69 families, 0 gaps, 6
adjudicated (including this archive) (gridflow `@.planning/v0.22-RESULTS.md` §IC-1).

Silver layout: one Parquet file per capture under
`C:/gridflow-data/silver/neso_data_portal/nsl/year=2026/month=10/` (the activation file, then
the 2026-10-16 capture's, 17,976 rows). The `year=`/`month=`
partition is the **capture** date, not the target date. Columns (21): the 11-column vendor
union (the 7 epoch-1 columns, then `operational_date`, `version`, `hourly_time_period`,
`reason_for_restriction`); then `issue_time`, `resource_id`, `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and
`dataset_version` (`1+e1`). All timestamps are tz-aware UTC.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

The current dump is the live resource. The archive's CKAN `last_modified` is 2024-11-27, and
the vendor says nothing about whether it will change again. The publication time of day is not stated by the vendor (see the
inference under Vintage). The current dump has two captures (2026-10-08, 2026-10-16) and the
archive one (2026-10-08). Between the two dump captures NESO added one upload a day at 10:30
GMT and changed no earlier row (see Files by disposition). `TODO: verify` whether a later dump
revises earlier rows; eight days of appends only is not a guarantee.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `nsl`: held: TODO: the dump returns past targets (rows before the capture) and NESO does not state that a row is unchanged since its `Data Upload Time GMT`, so historical issued limits are not evidenced, and the archive's Operational Date calendar / rollover and Version meaning are undocumented. (unit E-SEM)

The silver output exists on disk, but it is **held**: it is not eligible for publication or
for point-in-time model use until unit E-SEM answers the question above (RULINGS 565; held
at activation, RULINGS 567). The hold has three parts:

1. **Historical immutability (FACTS g2).** The dump returns 17,750 past targets alongside
   34 future ones (2026-10-08 capture; 17,951 and 25 on 2026-10-16). Each row carries a publication time, but NESO does not say the values
   are unchanged since then. Without that, a past row cannot be treated as the limit issued
   at its upload time. Settles it: a NESO revision or retention statement, or immutable
   per-issue files.
2. **Archive operational-date calendar and rollover (FACTS T03).** The archive dictionary is
   empty and the clock-change days are irregular, so its labels cannot be turned into
   instants.
3. **Archive `Version` meaning (FACTS T04).**

Separately from the hold, the archive's duplicate row keeps that resource out of silver
until NESO answers the adjudication question above. Lifting the hold would not load it.

References: gridflow `@.planning/phases/v0.22-K-IC-1/K-IC-1-FACTS.md` (§nsl, g1–g5,
IC1-1–IC1-6), `@.planning/phases/v0.22-K-IC-1/K-IC-1-SPEC.md`,
`@src/gridflow/connectors/neso_data_portal/registry/nsl.json`,
`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`,
`@docs/DECISION_LOG/ADR-035-neso-datastore-dump-leg.md`,
`@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md`,
`@docs/DECISION_LOG/ADR-040-neso-reconcile-adjudication.md`.
