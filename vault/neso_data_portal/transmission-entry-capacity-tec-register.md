---
source: "neso_data_portal"
package: "transmission-entry-capacity-tec-register"
dataset_key: "tec_register"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-16
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Transmission Entry Capacity (TEC) register

The TEC register is NESO's list of projects that hold a contract for Transmission Entry
Capacity (TEC). TEC is the amount of generation capacity, in MW, that a customer is
contracted to inject into the National Electricity Transmission System (NETS). The package
description says the list covers existing and future projects, both directly connected to
the NETS and embedded projects that make use of it. In market terms it is the transmission
connection queue and contracted-capacity position: which projects exist, where they
connect, what they are built from (wind, storage, gas, nuclear and so on), how many MW are
already connected, how many MW are contracted to arrive or leave, and from which date.
It is the forward-looking supply-side counterpart to operational data. A model of future
capacity, congestion or build-out can use it, but only as a contract position and not as a
dispatch or availability series.

> **Not a time series.** The file is a snapshot of the contracted position on the day it
> was published. A row is a project (or a project stage), not a period. Nothing in the
> file says when a row was first added, so any "as of" use rests on the capture clock
> below, not on `MW Effective From`.

The package description (catalogue snapshot `20261006T195819Z`) carries two notices that
bind how rows are read:

- **Gate column.** Following changes to CUSC paragraphs 6.30.3.2 and 6.35.2, the register
  carries a `Gate` column from 21 November 2025, saying whether an agreement is Gate 1 or
  Gate 2. It is filled only once an agreement is countersigned, and is blank until then.
- **Aggregation and duplicates.** Capacity across stages and technology types "is
  currently presented in aggregate, which may result in duplicate entries". The vendor
  says it intends to split capacity by stage and technology later. NESO also warns that
  some data corrections may take longer than usual while a temporary data-change governance
  process is in place for Connections Reform.

The data comes from a CKAN upload-file package on the NESO Open Data Portal
(@../README.md). **Status: eligible.** The silver output is published; there is no hold
on this package. Its siblings from the same pilot, @./interconnector-register.md and
@./embedded-register.md, share the register layout. The hold on the day-ahead demand
forecast performance pairing (RULINGS 591, 596) belongs to a different package and does
not bind this one.

- Publisher group: Connection registers
- Registry group: connection-registers · archetype: REG
- CKAN package id: `cbd45e54-e6e2-4a38-99f1-8de6fd96d7c1` (1 resource, `num_resources: 1`)
- Vendor page: https://www.neso.energy/data-portal/transmission-entry-capacity-tec-register

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| TEC Register | CSV | upload | `17becbab-e3e8-473f-b303-3806f43a6a10` |

There are no DOC, CATALOGUE-ONLY, GIS or held resources in this package.

### Resource download links

The URL is the `request_url` in the bronze sidecar of the capture (capture date 2026-10-08):

| Resource | Disposition | Download |
|---|---|---|
| TEC Register (CSV) | SILVER → `tec_register` | [tec-register-05-october-2026.csv](https://api.neso.energy/dataset/cbd45e54-e6e2-4a38-99f1-8de6fd96d7c1/resource/17becbab-e3e8-473f-b303-3806f43a6a10/download/tec-register-05-october-2026.csv) |

The filename carries a date, so it will change when the vendor replaces the file. The stable
handle is the resource id, not the URL. The resource is also loaded into the CKAN
Datastore (`datastore_active: true`, 2,196 records at the 2026-10-08 field-info call), and
its field dictionary is the source of the units below. gridflow downloads the uploaded
file; it does not read the Datastore.

## Families

### `tec_register`

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
| MW Effective From | `mw_effective_from` | date | `%d/%m/%Y` | yes | — | yyyy-mm-dd |
| Project Status | `project_status` | string | — | yes | — | — |
| Agreement Type | `agreement_type` | string | — | yes | — | — |
| HOST TO | `host_to` | string | — | yes | — | — |
| Plant Type | `plant_type` | string | — | yes | — | — |
| Project ID | `project_id` | string | — | yes | — | — |
| Project Number | `project_number` | string | — | yes | — | — |
| Gate | `gate` | float64 | — | yes | — | number |

- Entity key: `project_name`, `customer_name`, `connection_site`, `stage`, `mw_connected`, `mw_increase_decrease`, `cumulative_total_capacity_mw`, `mw_effective_from`, `project_status`, `agreement_type`, `host_to`, `plant_type`, `project_id`, `project_number`, `gate`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### The two clocks

- **Vintage clock: `ckan_last_modified`.** `published_at` and `available_at` both equal the
  CKAN `last_modified` of the resource at capture. CKAN gives this value without an
  offset; gridflow reads it as UTC (ADR-030 D-15, corroborated rather than
  vendor-documented). The resource is `url_type=upload`, so this is the upload time of the
  file, not a time attached to any row. The one capture has `2026-10-06T10:47:29.757067Z`.
  Use `available_at`, not `mw_effective_from`, to decide what was known when.
- **Event time, recipe `none`.** `timestamp_utc` (and `event_time`, copied from it) is the
  **capture time**: the bronze write instant, `2026-10-08T11:38:27.452947Z`, identical on
  every row. It is not a contract, connection or effective date. The register has no
  event time of its own. Its one date column, `mw_effective_from`, is kept as a native
  `date` and is not converted to a timestamp, because the vendor gives no time of day or
  timezone. TODO: verify whether any exact UTC effective instant is defined; until then no
  timestamp conversion of `mw_effective_from` is made.
- **No issue clock.** The epoch has issue `{"kind": "none"}`. This is not a forecast
  archive.

Engine columns after the 15 vendor columns: `timestamp_utc`, `published_at`,
`capture_written_at`, `event_time`, `available_at` (Datetime µs, UTC), `bronze_capture_id`,
`source_run_id`, `dataset_version` (String). Silver dtypes are as in the table above.
`dataset_version` is `1+e1` (record version 1, epoch 1).

#### Units and value rules

Units come only from the vendor field dictionary (Datastore field info, 2026-10-08):

- `mw_connected`, `mw_increase_decrease`, `cumulative_total_capacity_mw`: **MW**.
- `stage`, `gate`: unit `number`. They are small integer labels, not quantities. Silver
  holds them as float64 only because the record types them `numeric`; every populated value
  is a whole number (stage 1 to 5, gate 1 or 2).
- `mw_effective_from`: the dictionary gives unit `yyyy-mm-dd`, but **all 1,831 populated
  bronze dates are `dd/mm/yyyy`** (the dictionary's own example is `31/10/2032`). The
  record parses `%d/%m/%Y`. The dictionary format is wrong for the file; the file wins.
- Text columns (`project_name` and the rest) carry unit `n/a`.

Sentinels and blanks (no substitution is applied; the record declares none):

- **Blank means null.** Blank `Stage`, `Gate` and `MW Effective From` cells become nulls.
  Vendor meaning, from the dictionary comments: `Stage` is "only completed if the project is
  staged", `Gate` is blank until a Gate 1 or Gate 2 contract is countersigned, and
  `MW Effective From` is "otherwise empty" when there is no future connection or change.
  The dictionary does not say whether a blank `Gate` also covers a project with no signed
  contract of either kind. TODO: verify the meaning of blank `Gate` beyond the vendor
  comment.
- **`0` is a real value, not a missing marker.** The dictionary says `MW Connected` "will
  state 0MW until the project is built and connected" and `MW Increase / Decrease` "will
  state 0MW unless the TEC is due to increase or decrease". Zeros are kept as 0.0.
  No negative value is present in any of the three MW columns.
- No string cell is empty. Names and identifiers carry no leading or trailing whitespace.
  The CSV starts with a UTF-8 byte-order mark, which the reader strips; the first header
  matches `Project Name`.

#### Measured structure (silver read with Polars, 2026-10-16T18:37Z)

One capture is in silver (one Parquet file, `year=2026/month=10`), so every figure below
describes that capture. A daily refresh may add captures; the counts then change.

| Measure | Value |
|---|---|
| Rows | 2,196 (equals the activation count, RULINGS 504; reconcile 0 gaps) |
| Distinct `project_id` | 2,054 |
| Distinct `project_number` | 2,195 |
| Distinct `connection_site` | 1,247 |
| Rows with `stage` set | 262 (stage 1: 121, 2: 121, 3: 15, 4: 4, 5: 1) |
| Rows with `gate` set | 883 (gate 1: 771, gate 2: 112); 1,313 blank |
| Rows with `mw_effective_from` null | 365, all with `project_status = Built` |
| `mw_effective_from` range | 2020-10-01 to 2039-10-31 |
| Rows dated before the capture date | 104 |
| `mw_connected > 0` | 370 rows (368 Built, 1 Under Construction/Commissioning, 1 Consents Approved) |
| `mw_connected = 0` | 1,826 rows |
| `cumulative_total_capacity_mw = 0` | 26 rows |

Categorical columns (observed values, counts):

- `project_status`: Scoping 1,386 · Built 381 · Consents Approved 213 · Awaiting Consents
  172 · Under Construction/Commissioning 44. The dictionary defines Scoping, Awaiting
  Consents and Consents Approved; it does not define the other two.
- `agreement_type`: Direct Connection 1,740 · Embedded 456. See the delta note below.
- `host_to`: NGET 1,281 · SPT 458 · SHET 442 · OFTO 15 (the dictionary lists exactly these
  four).
- `plant_type`: 58 distinct values (40 semicolon-joined, 18 single-technology; Polars
  `n_unique`, silver queried 2026-10-16, one capture, 2,196 rows). Many are **semicolon-joined lists** of technologies
  (for example storage with solar), not single categories. The most common single-technology
  values are Energy Storage System 733, Wind Onshore 318, Wind Offshore 139 and CCGT 51.
  Splitting on `;` is a consumer decision; the silver column keeps the vendor string.

#### Identity, duplicates and `_latest`

- **Project identity is documented; row identity is not.** `Project ID` is the vendor's
  "Unique Project Identifier" and is case sensitive. `Project Number` is the "Unique
  Project Number"; when a project has more than one stage the number is followed by a dash
  and the stage number. A project can legitimately occupy several rows.
- **One project, several rows.** 122 `project_id` values occur in more than one row (107
  twice, 11 three times, 3 four times, 1 five times), 142 excess rows in all. In this
  capture every staged row has a stage-suffixed `project_number` (262 of 262), and no
  project has both staged and unstaged rows.
- **The cumulative column is not a stage-repeated total.** For 120 of the 121 staged
  projects `cumulative_total_capacity_mw` differs between the stage rows. The dictionary
  says it is the "total amount of capacity contracted across all Stages", which this does
  not obviously match. TODO: verify with the vendor how `Cumulative Total Capacity (MW)`
  is built for staged rows.
- **The columns are not an accounting identity.** `cumulative_total_capacity_mw` differs
  from `mw_connected + mw_increase_decrease` in 135 rows (134 of them staged). The vendor
  does not state that relation, so do not assume it.
- **One unresolved duplicate key.** `project_number` is unique except for one pair,
  `PRO-000053` (Immingham): the same `project_id`, a blank stage and the same plant type,
  but different capacities, status, effective date and gate (one row Built with 1,268 MW
  connected and no date, one Scoping with a 50 MW increase from 2027-07-01 and gate 1).
  The rows are not identical duplicates, and the pair is the only reason no
  `(project_number)` or `(project_id, stage)` key is unique. Adding `plant_type` does not
  help. No column set in the file is a unique key: the declared entity key (all 15 vendor
  columns) is unique in this capture only because no two rows are identical.
- **`_latest` is `whole_capture`.** With no evidenced row identity, key-latest is not safe.
  The newest capture is the latest view and rows dropped from a later file disappear from
  it (the vendor says unstaged rows can later fold into the overall project). Base and
  `_latest` both have 2,196 rows (RESULTS §E). TODO: verify cross-capture stability of
  `project_id` and `project_number` once a second capture exists; only one capture has been
  measured, so stability is unproven.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Twice weekly
- The publisher group description says the registers show "the latest contracted position,
  published twice weekly". Daily refresh is gridflow's polling cadence. TODO: verify the
  skip rule for an unchanged file on this family (other families report "unchanged since
  newest capture"). Only one capture (2026-10-08) existed at query time.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none

This package has no held output. Registry eligibility is `eligible` and the eligibility
report (`docs/neso_data_portal/eligibility.md`) lists 1 SILVER resource and 0 DOC, GIS or
HOLD resources. The open items above are `TODO: verify` notes on semantics, not holds.

## Known issues and gotchas

- **Dictionary date format is wrong.** The dictionary says `yyyy-mm-dd`; the file is
  `dd/mm/yyyy` (1,831 of 1,831 populated values). A reader that trusts the dictionary
  silently mis-parses days as months.
- **`Agreement Type` values differ from the dictionary.** The dictionary comment says
  "Directly Connected or Embedded"; the file carries `Direct Connection` and `Embedded`.
  Filter on the file's values.
- **Past effective dates are normal.** 104 rows carry an effective date before the capture
  date. The dictionary says the contracted date stays in place until the project is Built
  and Connected. Do not treat a past date as an error or as proof the capacity is live.
- **A future date does not mean the MW are connected.** `mw_connected` is the capacity
  currently connected; `mw_increase_decrease` is capacity due to arrive or leave at
  `mw_effective_from`. A model of installed capacity needs the status column too.
- **`plant_type` is a list.** Multi-technology projects are one row with `;`-joined values.
  Summing MW by technology on the raw string double-counts or mis-buckets.
- **Duplicates are by design.** The vendor says capacity across stages and technologies is
  "presented in aggregate", so a project can appear on several rows. Summing
  `cumulative_total_capacity_mw` over all rows overstates it. Whether the stage rows
  overlap is not established (TODO above).
- **Status is not authoritative.** The dictionary says NESO holds no authority on the
  status classes: they are "as far as we are aware", from the customer or public sources.
- **Case-sensitive IDs.** `Project ID` is case sensitive; do not lower-case or normalise it.
  Project and customer names are stored as-is.
- **The dump is a replacement, not a log.** The vendor file shows the current contracted
  position only. Removed projects are not marked. To see history, compare captures by
  `available_at`.

## Implementation delta

- **`MW Effective From` format**: docs say `yyyy-mm-dd`, the record has `%d/%m/%Y` — the
  record matches the file (all 1,831 populated values), so the record is right and the
  dictionary is stale.
- **`Agreement Type`**: docs say "Directly Connected or Embedded", the file has `Direct
  Connection` / `Embedded` — the file is the evidence. No code depends on the string.
- **`Gate`**: present in the file and the record from the vendor's 21 November 2025
  change. The vendor says the column is added from that date, so a file from before it would lack
  `Gate`; the record has one header epoch, so such a file would not match it. TODO: verify whether older captures exist and need a
  second epoch. The sweep found only the 2026-10-08 capture.
- **Stage and gate dtype**: the vendor type is `number`, the record types them `float64`
  and not an integer type. Values are whole numbers; the choice is the record's, not a
  vendor statement.
- **Event time**: no source defines one. The recipe is `none`, so `timestamp_utc` is the
  capture time by construction (ADR-034 engine rule), not a vendor field.

No other discrepancies found between the dictionary, the registry record and the file.

## Modelling notes

- **Use.** A forward view of contracted transmission-connected capacity: build-out
  scenarios, the pipeline of storage versus wind versus gas, regional (`host_to`,
  `connection_site`) concentration and queue maturity (`project_status`, `gate`). It is not
  an operational or dispatch series.
- **Point in time.** Filter with `WHERE available_at <= :as_of`. Only one capture exists
  at present, so no history is available yet; history will grow with each new capture.
- **Likely features.** `mw_connected` for the built base; `mw_increase_decrease` and
  `mw_effective_from` for the near-term pipeline; `plant_type` split on `;`; `project_status`
  as a maturity filter.
- **Filters before use.** De-duplicate or aggregate by `project_id` knowing the aggregation
  caveat above; exclude or flag the `PRO-000053` pair; do not sum `cumulative_total_capacity_mw`
  across the stage rows of a project.
- **Related data.** @./interconnector-register.md and @./embedded-register.md (same layout);
  @./capacity-market-register.md for the Capacity Market side of the same fleet.
- Modelling use inside gridflow_models is not yet designed. TODO.

## Evidence

All paths are in the gridflow checkout unless noted. Counts were read on 2026-10-16 at
about 18:37Z, from silver with Polars.

- `.planning/v0.22-RESULTS.md` §E: activation receipt (cutoff 2026-10-08, 2,196 rows,
  reconcile 0 gaps, base equals `_latest`). The TEC register was activated in §E; the
  §BS bootstrap covered three other families (`daily_wind_availability`,
  `historic_generation_mix`, `embedded_wind_solar_forecast`) and not this one.
- `.planning/RULINGS.md`: 494 (BS, other families), 504 (E activation, the binding ruling
  for this page), 879 (docs wave). Rulings 591 and 596 concern the held gold pairing of
  another package and do not bind here.
- `.planning/phases/v0.22-E-profiler-pilot/RESEARCH.md` §1 (dictionary types, date
  format), §2 (`MW Effective From` is a date with no time or zone), §3 (identifier counts
  and the Immingham pair) and `VERIFICATION.md` (pilot record matches the plan).
- `src/gridflow/connectors/neso_data_portal/registry/transmission-entry-capacity-tec-register.json`:
  the registry record.
- `docs/neso_data_portal/eligibility.md`: generated eligibility report.
- `docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (D-15, naive CKAN time read
  as UTC) and `docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md`.
- Vendor field dictionary:
  `.planning/research/neso-snapshots/field-info/20261008T114228Z/tec_register.json`.
- Catalogue snapshot: `.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json`
  (package description, group description, extras, licence).
- Bronze: `C:/gridflow-data/bronze/neso_data_portal/tec_register/2026/10/08/` (CSV and
  sidecar: request URL, `ckan_last_modified`, 421,694 bytes, sha256 `9f1a922c…`).
- Silver: `C:/gridflow-data/silver/neso_data_portal/tec_register/year=2026/month=10/`.
- Vendor overview: @../README.md.
