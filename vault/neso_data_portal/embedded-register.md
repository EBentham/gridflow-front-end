---
source: "neso_data_portal"
package: "embedded-register"
dataset_key: "embedded_register"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-16
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Embedded Register

The **Embedded Register** is NESO's list of **embedded generation projects in Scotland** that are
either connected or contracted to connect (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). The two Scottish
transmission owners are named in the `Host TO` column (`SHET` and `SPT`). Each row is one project, or one **stage** of a staged project, with its connected
capacity, capacity contracted to connect or be removed later, the cumulative contracted total, the
date a change is contracted to take effect, the project's build status, its plant type and, since
November 2025, its connection **Gate**. `TODO: verify` the vendor's exact definition of "embedded";
the package notes do not define it.

The resource description says the file "contains the latest version of the Embedded Register
including all changes up to publication" and is updated "twice weekly on Tuesdays and Fridays". It
is therefore a **registry snapshot, not a time series**: the vendor describes each file as the latest
version of the register. gridflow holds a single capture, so how a project that leaves the register
appears (or whether it simply drops out of the next file) is not shown; `TODO: verify`. For modelling it is a pipeline
view of future Scottish embedded capacity, useful as a leading indicator of where distributed supply
and storage is contracted to arrive. It is a sibling of the transmission-connected registers
(@./transmission-entry-capacity-tec-register.md) and the interconnector register
(@./interconnector-register.md), and it should be read with the vendor's own caveat that status
classifications are produced "as far as we are aware" and carry no NESO authority (see the `Project Status` entry under the vendor dictionary and the gotchas below).

As of the query time (2026-10-16T18:37Z) gridflow holds **one capture** (taken 2026-10-08) and the
silver has **561 rows**. The package is **eligible**: nothing is held, so values may be used. This
page still gives only schema, counts and aggregate profiles, not row-level values.

- Publisher group: Connection registers
- Registry group: connection-registers · archetype: REG
- Package page: [embedded-register](https://www.neso.energy/data-portal/embedded-register)

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Embedded Register | CSV | upload | `68b6f3a1-e1bf-403b-9062-0269fc758d77` |

The package has one resource, a CSV with disposition SILVER. It has no DOC or catalogue-only
resources and no `_files` family.

Download link and the one capture (a CKAN upload resource). Size, CKAN `last_modified` and hash come
from the capture sidecar under `C:/gridflow-data/bronze/neso_data_portal/embedded_register/2026/10/08/`.

| File | Bytes | Data rows | CKAN `last_modified` | Captured (UTC) |
|---|---:|---:|---|---|
| [embedded-register-05-october-2026.csv](https://api.neso.energy/dataset/4b0e109c-aa23-45ac-86c1-0bda557d1aab/resource/68b6f3a1-e1bf-403b-9062-0269fc758d77/download/embedded-register-05-october-2026.csv) | 92,325 | 561 | 2026-10-06T10:47:45.071632 | 2026-10-08T10:36:47.628831 |

**Bronze body (full scan, 2026-10-16).** Valid UTF-8 with a **UTF-8 BOM**, CRLF line endings
(562 lines: one header and 561 data rows), one header row, body sha256 prefix `2feb369e` (full digest
in the sidecar, equal to the declared `Content-Length` of 92,325 bytes). The profiler (ADR-036) found
the same 561 rows. The file name carries a date, 05 October 2026, one day before the CKAN
`last_modified` of 2026-10-06; `TODO: verify` what the name date records.

## Families

### `embedded_register`

- Kind: tabular · archetype: REG · refresh: daily · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Project Name | `project_name` | string | — | yes | — | — |
| Customer Name | `customer_name` | string | — | yes | — | — |
| Connection Site | `connection_site` | string | — | yes | — | — |
| Stage | `stage` | float64 | — | yes | — | number |
| MW Connected | `mw_connected` | float64 | — | yes | — | MW |
| MW Increase / Decrease | `mw_increase_decrease` | float64 | — | yes | — | MW |
| Cumulative Total Capacity (MW) | `cumulative_total_capacity_mw` | float64 | — | yes | — | MW |
| MW Effective From | `mw_effective_from` | date | `%Y-%m-%d` | yes | — | yyyy-mm-dd |
| Project Status | `project_status` | string | — | yes | — | — |
| HOST TO | `host_to` | string | — | yes | — | — |
| Plant Type | `plant_type` | string | — | yes | — | — |
| Project ID | `project_id` | string | — | yes | — | — |
| Project Number | `project_number` | string | — | no | — | — |
| Gate | `gate` | float64 | — | yes | — | — |

- Entity key: `project_number`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks.**

- **Vintage** is `ckan_last_modified`. `published_at` and `available_at` both equal the CKAN
  `last_modified` of the captured file, here **2026-10-06T10:47:45.071632Z**. A point-in-time query
  (`WHERE available_at <= :as_of`) therefore sees a capture only from the moment NESO updated the
  file, not from the moment gridflow fetched it.
- **Event time** is `none`. The temporal recipe is `none`, so `timestamp_utc` (and the silver
  `event_time`) is the **capture time**, here 2026-10-08T10:36:47.633836Z. It is not a property of
  the project. A register has no observation instant. The only date in the body, `MW Effective From`,
  is a contractual date for a future change and stays a plain `date` column.

**One header epoch.** The record accepts one exact header, the 14 columns above (record version 1,
`dataset_version` `1+e1`). The package notes say a **Gate** column was added from 21 November 2025,
so earlier files presumably lacked it. gridflow holds no earlier capture, so a body without `Gate` is
not a known epoch and would fail the header match loudly rather than load. `TODO: verify` whether
NESO retains or serves the earlier layout.

**What the columns mean (vendor dictionary).** Descriptions and comments come from NESO's saved field
info for the resource (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/embedded_register.json`, 2026-10-08).
The dictionary's `info.label` and `info.notes` are empty, as for the whole catalogue.

- **`Project Name`**, **`Customer Name`**, **`Connection Site`**: free text. "Name of Generation
  Project", "Name of Generator", "Name of Generation Connection Site". Stored as supplied (no normalisation).
- **`Stage`**: unit "number". Staged capacity: how much capacity the customer will connect and when,
  in chunks aligned to the build or to reinforcement works. The vendor comment says the field "is only
  completed if the project is staged otherwise it will be empty". The body carries it as text like
  `1.00` and silver types it `float64`. It is an ordinal label, not a measurement.
- **`MW Connected`**: unit **MW**. "Amount of capacity currently connected to the National Grid". Vendor
  comment: the field "will state 0MW until the project is built and connected". `0` is a real value, the
  vendor's way of saying not yet connected.
- **`MW Increase / Decrease`**: unit **MW**. "Amount of capacity contracted to connect or be removed at
  a future date". Vendor comment: it "will state 0MW unless the capacity is due to increase or
  decrease". A negative value is a contracted removal.
- **`Cumulative Total Capacity (MW)`**: unit **MW**. "Total amount of capacity contracted across all
  Stages". See the staged-project gotcha below.
- **`MW Effective From`**: dictionary type `date`, unit string `yyyy-mm-dd`. "Date on which Connection is
  contracted to be effective from". Vendor comment: it "will only include dates for future connections
  or increase/decreases to capacity, otherwise this field will be empty". No time of day and no time
  zone are given, so silver keeps a calendar `date` and builds no instant from it. The dictionary
  example (`31/10/2032`) uses day-first order, but the bronze body uses `YYYY-MM-DD` (for example, the
  first cell is in the form `2030-10-31`), which is what the record's format `%Y-%m-%d` parses. This
  differs from the TEC register, whose body uses `dd/mm/yyyy`.
- **`Project Status`**: "Indicates what stage the Project is at in it's build cycle" (vendor spelling).
  Vendor comment: the classifications rest on information NESO has "ascertained from the customer or
  from another source" and NESO holds "no authority" over them; they are produced on an "as far as we
  are aware" basis.
- **`HOST TO`**: "Indicates which Transmission Owner (TO) is responsible for the connection", `SHET` or
  `SPT` per the vendor comment.
- **`Plant Type`**: "Indicates the fuel type contracted to connect". Multi-technology projects hold
  several values joined by a semicolon (see below).
- **`Project ID`**: "Unique Project Identifier". Vendor comment: the reference is **case sensitive**.
- **`Project Number`**: "Unique Project Number". Vendor comment: where a project has more than one
  stage, the number is followed by a dash and the stage number, for example the dictionary's
  `PRO-000630-1`. The resource description says NESO plans to phase out Project ID in favour of
  Project Number and will keep both "until the end of this year" (the text carries no year; the
  snapshot is from 2026, `TODO: verify` which year is meant).
- **`Gate`**: dictionary unit `n/a`, type number. "Indicates which Gate the Project is contracted at".
  Vendor comment: it is filled only once a signed Gate 1 or Gate 2 contract is countersigned, and
  until then "all existing contracted projects will appear blank". Blank is therefore "no countersigned
  Gate contract", not a missing observation. The package notes tie the column to CUSC paragraphs
  6.30.3.2 and 6.35.2 and the Connections Reform process.

**Identity and selection (ADR-036, ADR-039).**

- The entity key is `project_number`, with `latest: whole_capture`. The registry (ADR-036) recorded the
  documented identifier as **measured unique** in the captured body, in contrast to the TEC register,
  where `PRO-000053` occupies two non-identical rows. In silver on 2026-10-16: **561 rows, 561 distinct
  `project_number`**.
- `project_id` is **not** a row key. There are 544 distinct values across the 561 rows. The 17 extra
  rows come from 14 projects that have more than one stage row: those 14 `project_id` values cover
  31 rows, and every one of the 31 has a `Stage` value and a dashed `Project Number`. All other rows
  (530) have no stage and a plain `PRO-nnnnnn` number. The 14 staged projects hold stages 1 to 5.
- Case: the 544 distinct IDs are also 544 distinct after lowercasing, so no two projects differ only by
  case in this capture. Never fold case, since the vendor says the reference is case sensitive.
- `_latest` is `whole_capture`: the newest complete capture, so a project missing from a later file is
  gone from `_latest` too. No cross-capture identity stability is established (only one capture
  exists). `TODO: verify` that `Project Number` is stable for one project across publications, for
  example when a project gains a stage and its number gains a suffix.

**Sentinels and missing values (FACTS g5).** The full-body scan found no cell equal to `NA`, `N/A`, `-1`,
`99999`, `-` or `null`, and no padded cell. The record declares no null tokens, and nothing is mapped
to null by token. Empty cells are the only missingness. Exact blanks and zero counts:

| Column | Blank cells | Cells equal to zero |
|---|---:|---:|
| `Stage` | 530 | 0 |
| `MW Connected` | 0 | 345 |
| `MW Increase / Decrease` | 0 | 215 |
| `Cumulative Total Capacity (MW)` | 0 | 0 |
| `MW Effective From` | 215 | n/a (date) |
| `Gate` | 464 | 0 |
| every other column | 0 | n/a (text) |

Silver nulls equal the blank counts above (2026-10-16), so nothing was dropped, imputed or excluded. A
zero in `MW Connected` or `MW Increase / Decrease` is the vendor's stated "0MW" convention and is kept
as a real zero, never converted to null.

**Row counts and profile (silver, queried 2026-10-16T18:37Z).**

| Measure | Value |
|---|---:|
| Rows | 561 |
| Distinct `project_number` | 561 |
| Distinct `project_id` | 544 |
| Staged rows (non-blank `stage`) | 31 |
| `HOST TO` = `SHET` / `SPT` | 352 / 209 |
| `Gate` = 1 / 2 / blank | 56 / 41 / 464 |
| `Project Status`: Scoping | 255 |
| `Project Status`: Built | 217 |
| `Project Status`: Consents Approved | 58 |
| `Project Status`: Awaiting Consents | 26 |
| `Project Status`: Under Construction/Commissioning | 5 |
| Rows with `MW Connected` > 0 | 216 |
| Rows with `MW Increase / Decrease` > 0 / < 0 | 345 / 1 |
| Distinct `MW Effective From` values | 141 |
| `MW Effective From` range | 2019-10-31 to 2036-10-31 |
| `MW Effective From` before the 2026-10-08 capture | 138 |

All 215 blank effective dates sit on `Built` rows; 2 `Built` rows do carry a date. No `Built` row has a
Gate. Gate 1 appears on `Scoping` and `Awaiting Consents` rows only; Gate 2 appears on `Scoping`,
`Awaiting Consents`, `Consents Approved` and `Under Construction/Commissioning` rows. `Plant Type` has
25 distinct values, led by `Wind Onshore` (196 rows), `Energy Storage System` (131) and
`PV Array (Photo Voltaic/solar)` (71). Values with a semicolon are multi-technology (for example, storage
combined with solar or wind, and `Demand;`-prefixed combinations): gridflow stores the string whole and
does not split it. `TODO: verify` the vendor's full list of plant types; none is published.

**Activation (2026-10-08, master `29b563c`, PR #85).** The profiler pilot (unit E, ADR-036) froze the
record and the activation transformed the 2026-10-08 capture with
`gridflow transform neso_data_portal embedded_register --start 2026-10-08 --end 2026-10-08` (cutoff
2026-10-08, the newest bronze partition). There was no prior silver, so nothing was overwritten and no
snapshot was taken. Silver holds **561 rows**, equal to the capture's data rows, with 0 excluded; the
reconcile over the six pilot families (`--cutoff 2026-10-08`) exited 0 with 0 gaps, and the base view
and `_latest` both counted 561 rows (RULINGS 503/504, gridflow `@.planning/v0.22-RESULTS.md` section E).
The package is **eligible** (it is one of the three eligible pilot registers). No later ruling changes
this family: a search of RULINGS for the family key finds nothing after the activation, and rulings 591
and 596 concern the demand-forecast families, not this register. Ruling 879 closed the docs gaps that
this page fills.

Silver layout: one Parquet file under
`C:/gridflow-data/silver/neso_data_portal/embedded_register/year=2026/month=10/`. The `year=`/`month=`
partition is the **capture** date, not any project date. Columns (22): the 14 vendor columns, then
`timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`,
`available_at`, `source_run_id` and `dataset_version`. All timestamps are tz-aware UTC. No gold view or
builder reads this family; only the generated base and `_latest` views exist.

**Gotchas.**

1. **Do not sum `Cumulative Total Capacity (MW)` across rows.** It is the total "across all Stages". For
   staged projects the value repeats and grows from one stage row to the next: 17 of the 31 staged rows
   have a cumulative total that is not `MW Connected` plus `MW Increase / Decrease`, and the stage rows of
   one project look like a running total. `TODO: verify` the vendor's exact arithmetic (running total
   versus project total) before using any capacity sum for a staged project. Sum within one stage
   column only after choosing a stage deliberately.
2. **The vendor warns of duplicate entries.** The package notes say capacity across stages and technology
   types is "presented in aggregate, which may result in duplicate entries", and that NESO intends to
   split capacity by stage and technology later. A future capture may change the row grain.
3. **Unstaged "second lines".** The resource description says some projects have two lines without stage
   numbers, usually meaning a built project that is adding another type of generation, and that the second
   line "will fall away" once built. This capture shows no `project_id` with two unstaged rows
   (`project_number` is unique), but a later capture might.
4. **A negative `MW Increase / Decrease` is a contracted removal.** One row (a built project) carries a
   decrease. Do not clip it.
5. **Blank means different things per column.** Blank `Stage` = unstaged, blank `Gate` = no countersigned
   Gate contract, blank `MW Effective From` = no future change dated (all 215 blanks are on `Built` rows; 2 of the 217
   `Built` rows do carry a date).
6. **Dictionary example mismatches.** The `Project ID` example in the dictionary has 15 characters; every
   captured value has 18. The date example is day-first; the body is ISO. Trust the body, as the record
   does.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Twice weekly

The resource description says Tuesdays and Fridays. The registry polls daily, so most polls should find
the file unchanged. `TODO: verify` that an unchanged body adds no new capture (the EF activation, RULINGS
519, recorded "unchanged since newest capture" skips for other families). The one
capture on disk was taken 2026-10-08 and holds the file NESO modified on Tuesday 2026-10-06. At query
time (2026-10-16T18:37Z) bronze still holds that single capture, although two later Tuesday/Friday
updates (2026-10-09 and 2026-10-13) would be expected by the vendor's stated cadence. `TODO: verify`
whether NESO actually published them, and whether the daily refresh has captured them yet (a refresh
was running concurrently when this page was written).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

The family is eligible and nothing is held. The open items are `TODO: verify` points, not holds: the
exact effective instant and zone of `MW Effective From` (unit E-SEM, the semantics research unit for the pilot families; the
column stays a calendar date and no timestamp is built from it), the vendor's staged-capacity
arithmetic, and the stability of `Project Number` across captures. Each would need more captures or a
vendor statement.
