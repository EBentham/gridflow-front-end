---
source: "neso_data_portal"
package: "obp-non-bm-reserve-instructions"
dataset_key: "obp_reserve_instructions"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Open Balancing Platform (OBP) - Non-BM Instructions

NESO's log of dispatch instructions sent to **non-BM** service providers through the Open
Balancing Platform (OBP), published as one CSV. The vendor says the file holds instructions "once
instructions have been confirmed by Service Providers", and that cease instructions are always
published whatever their status. It currently covers three services: Non-BM Quick Reserve,
Non-BM Slow Reserve and Non-BM MW Dispatch. The `service_id` values observed are `PQR`, `PSR`
and `RDP`. The vendor's example list for the column also names `NQR` and `NSR`, which do not
occur in the captured file. This file covers only the services currently mastered in OBP (Quick
Reserve, Slow Reserve, MW Dispatch). The vendor says OBP will incrementally master more non-BM
services as they migrate, with less published on its separate ASDP page ("non-bm-ancillary-service-dispatch-platform-asdp-instructions"),
so other non-BM instructions are still published there and are **not** in this file. Use the file
to see **what NESO asked a non-BM unit to do, and when**, for example to study how often and at
what indicative price Quick Reserve is called. For the Balancing Mechanism bid-offer and
acceptance data, see the domain page (@../../../20-domain/markets/gb-balancing-mechanism.md).

A row is an instruction **point**, not a whole instruction. One `instruction_id` groups the points
of one dispatch (`sequence` orders them). The point types, from the vendor dictionary:

- `START`: the start of the dispatch instruction.
- `STOP`: the start of the cease instruction.
- `SPP` (settlement period point): the instant the instruction crosses a settlement period boundary.
- `VP` (vertex point): any other vertex of the instruction's power profile.

The vendor adds that when points overlap, the logging priority is START/STOP, then SPP, then VP.
This is an event table, not a forecast: each row records something that happened, so it carries no
forecast vintage problem. The package has no history file. In the one capture to date the
CSV's point times span about the 12 months before its last-modified time (see Cadence); whether
that is a fixed rolling window is not established.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT
- Package id: `0ba217bb-846b-470e-9717-ff152d97d009`
- Vendor tags: Dispatch, Instructions, MW Dispatch, Non-BM, Quick Reserve, Reserve, Service,
  Slow Reserve, Subscribable

## Files by disposition

The package has one resource.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Non-BM Instructions from OBP | CSV | upload | `dad63c1b-8a8e-47de-9922-7880384ef104` |

- Non-BM Instructions from OBP → `obp_reserve_instructions`. CKAN datastore active; the
  datastore's declared unique key is `Instruction Point ID`. Download as captured:
  [instr_20261002064426_qr_sr_nbm.csv](https://api.neso.energy/dataset/0ba217bb-846b-470e-9717-ff152d97d009/resource/dad63c1b-8a8e-47de-9922-7880384ef104/download/instr_20261002064426_qr_sr_nbm.csv).
  The file name embeds a generation timestamp and changes with each publication, so the stable
  handle is the resource id, not the URL.
  Captured: `raw_20261008T111504Z_dad63c1b-8a8e-47de-9922-7880384ef104_87489f2e.csv` (bronze
  `2026/10/08/`), 33,217 bytes, 422 data rows, one header epoch, sha256
  `87489f2e4e7b59ff2cbf92f6b6014b0678cb1ac5da8d84bbe98f4a20ac26e4d9`.

There are no DOC, HOLD or ignored resources in this package.

## Families

### `obp_reserve_instructions`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Instruction ID | `instruction_id` | string | — | yes | — | — |
| Sequence | `sequence` | int64 | — | yes | — | — |
| Unit ID | `unit_id` | string | — | yes | — | — |
| Service ID | `service_id` | string | — | yes | — | — |
| Instruction Point Type | `instruction_point_type` | string | — | yes | — | — |
| Issue Datetime | `issue_datetime` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC |
| Point Datetime | `point_datetime` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC |
| Target MW | `target_mw` | float64 | — | yes | — | MW |
| Target Price | `target_price` | float64 | — | yes | — | £/MWh |
| Instruction Point ID | `instruction_point_id` | string | — | no | — | — |
| Instruction Status | `instruction_status` | string | — | yes | — | — |

- Entity key: `instruction_point_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`point_datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource: `2026-10-02T06:44:33.852998` for the one capture to
   date. CKAN emits it without an offset, and gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All 422 silver rows
   share this one vintage (verified on the silver Parquet, 2026-10-13). The record's issue
   recipe is `none`. `Issue Datetime` is **not** the vintage and not a generic issue clock (see
   below).
2. **Event time (`utc_instant` on `point_datetime`).** `timestamp_utc` = `event_time` =
   `point_datetime`, the instant of the instruction point, with no shift. The vendor dictionary
   states `Point Datetime` is UTC and gives the example `2025-07-02T10:05:00Z`, but the CSV cells
   carry no offset suffix (`2025-10-10T10:00:01`). The UTC reading rests on the vendor's stated
   unit, not on the syntax. Verified on all 422 silver rows: `timestamp_utc` and `event_time`
   equal `point_datetime`. Points are not on a half-hour grid: START/STOP can fall on any minute,
   and a VP can sit one second after its START (for example `2025-10-10T10:00:00` then
   `2025-10-10T10:00:01`).

The two clocks are far apart. Point times in the capture run `2025-10-10T10:00:00Z` to
`2026-10-02T06:44:00Z`, while the vintage is `2026-10-02T06:44:33Z`. Every one of the 422 point
times is on or before the vintage, so no row is stamped as available earlier than the
instruction point it describes. The vintage is a conservative proxy and is later than the real
publication moment. The vendor says the file is "continuously published throughout the day", but
the real first-publication time of each row is not recorded. Treat `available_at` as an upper
bound on when you could first have seen a row.

**Why this family is eligible.** It is an event/instruction log whose rows are things that already
happened at their `point_datetime`, with the CKAN vintage as a conservative availability proxy. It
is not a forecast, so there is no forward-target test to pass. All 422 rows have a point time on
or before the vintage.

**`Issue Datetime` is a nullable data column, not an issue recipe.** The vendor defines it as the
time the dispatch instruction is sent to the provider, "available for START and STOP instruction
points". It is UTC. It is blank on 259 of 422 rows, all of the 168 `VP` and 88 `SPP` rows plus 3
`STOP` rows. It is kept as a nullable UTC datetime. It is never propagated from a START row to the
other points of the same instruction, and never used as `available_at`. A generic issue recipe
would fail on the blanks, and the vendor publishes confirmed instructions, so dispatch issuance
does not prove when the row's later confirmation status existed.

**Units (vendor dictionary only).**

- `Target MW` → **MW**. Dictionary: "Power from PN in absolute values", where PN is the unit's
  Physical Notification. The dictionary does not say whether this is a delta or an absolute
  level, and the phrase is easy to misread. `TODO: verify` whether `Target MW` is an
  absolute MW level or a difference from the unit's PN.
- `Target Price` → **£/MWh**. Dictionary: "Indicative Price". It is an indicative price, not a
  settled price.
- `Sequence`, `Instruction ID`, `Instruction Point ID`: dimensionless identifiers or counts.
  The dictionary types the two IDs as integers; gridflow stores all three opaque identifiers
  as **strings**, byte-equal to the file, so leading zeros and widths are never lost. `Sequence`
  is `int64`.
- No MW-to-MWh or price-unit conversion is made or implied.

**Sentinels and missing values (FACTS g5).** No null token is declared and nothing is mapped.

- Blank `Issue Datetime` and blank `Instruction Status` stay null. Status is blank on the same
  259 rows (`VP`, `SPP` and 3 `STOP` rows are all blank; every `START` has a status).
- Zeros stay zero: `target_mw = 0` on 175 rows (observed, not a vendor rule: 80 `START` rows,
  85 `VP` rows, 5 `SPP` and 5 `STOP`; the last point of 80 of the 85 instructions is 0). The longest run of consecutive zeros is 8 rows.
- Negative prices are real: `target_price` runs from -210 to 197.85 £/MWh in the capture, with no
  null. `target_mw` runs 0 to 24 MW, with no null. Do not clip or treat negatives as missing.
- No min/max bounds are imposed and no value is converted.

**Categoricals observed.**

| Column | Values (rows) |
|---|---|
| `instruction_point_type` | VP 168 · SPP 88 · START 85 · STOP 81 |
| `service_id` | PQR 363 · PSR 34 · RDP 25 |
| `instruction_status` | blank 259 · ACCEPTED 162 · REJECTED 1 |

The dictionary says `Instruction Status` is "ACCEPTED, PROXY ACCEPTED" for START and STOP
points, and that a proxy status is when the control room accepts or rejects on behalf of the
service provider. The capture has `ACCEPTED` and `REJECTED` and no `PROXY ACCEPTED`. `TODO:
verify` the full status vocabulary. The listed examples and the observed values disagree, so do
not build a closed enum from either.

**Identity and selection.** The entity key is `instruction_point_id`, which the vendor describes
as the "Unique Key for the reporting entry", and which is also the datastore's declared unique
key. It is unique in the capture (422 distinct values), a capture-level duplicate guard.
`instruction_id` + `sequence` also passes the guard (85 distinct instructions, 4 to 7 points
each). Every row is one point, and `unit_id` takes 24 distinct values. Unit IDs are vendor-registered
non-BM identifiers (for example `EDFE-8`) and are stored as published, with no normalisation.
`_latest` is `whole_capture`: the newest capture replaces the previous one as a whole. Measured
uniqueness is a guard. It does not prove the vendor never amends a point or its status later.
`TODO: OBP-INSTRUCTION-IMMUTABILITY` — no repeated capture of this resource exists yet, so
whether reported points or statuses are later amended or removed is not established.
Cross-capture identity of a point is likewise unproven.
`TODO: INTERVAL-CLOSURE` — no reviewed source says whether the span between two points is
closed or open at its ends. Point instants are kept as published and no interval convention is
imposed.

**Activation (2026-10-13, master `638b427`, PR #115).** Transformed with window
`2026-10-08..2026-10-08` (one capture, no prior silver, so nothing was overwritten): **422
silver rows**, equal to the planned count, 0 validation failures, 0 rows excluded. Reconcile
`--all --cutoff 2026-10-12` exited 0 with 191 families, 0 gaps (gridflow
`@.planning/v0.22-RESULTS.md` §AS-3b; RULINGS 736, 737, 738, 751, 752). The sibling OBP
packages `obp-non-bm-physical-notifications` and
`obp-reserve-availability-utilisation-price` were activated in the same batch. The 7 held
outputs of the batch (the four EAC mock families and three ORPS families) are other packages and
do not affect this one.

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1, epoch 1).

A worked instruction (silver rows of `instruction_id` 3191870, unit `EDFE-8`, service `PQR`;
`timestamp_utc` is omitted because it equals `point_datetime`):

| `sequence` | `instruction_point_type` | `issue_datetime` | `point_datetime` | `target_mw` | `target_price` | `instruction_point_id` | `instruction_status` |
|---:|---|---|---|---:|---:|---|---|
| 1 | START | 2025-10-10 09:52:00 | 2025-10-10 10:00:00 | 0.0 | 110.79 | `12315528` | ACCEPTED |
| 2 | VP | null | 2025-10-10 10:00:01 | 2.0 | 110.79 | `12315529` | null |
| 3 | SPP | null | 2025-10-10 10:30:00 | 2.0 | 118.83 | `12316826` | null |
| 4 | SPP | null | 2025-10-10 11:00:00 | 2.0 | 120.56 | `12315152` | null |
| 5 | SPP | null | 2025-10-10 11:30:00 | 2.0 | 116.88 | `12315153` | null |
| 6 | STOP | null | 2025-10-10 11:38:00 | 2.0 | 116.88 | `12316848` | null |
| 7 | VP | null | 2025-10-10 11:38:00 | 0.0 | 116.88 | `12316849` | null |

Note the START issue time (09:52) precedes its point time (10:00) by eight minutes, the STOP
carries no issue time in this instance, and STOP and the trailing VP share one `point_datetime`.
Because of that, do not assume `point_datetime` is unique within an instruction.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- The vendor describes the file as continuously updated through the day. The resource's CKAN
  `last_modified` in the 2026-10-06 catalogue snapshot is `2026-10-02T06:44:33.852998`, and the
  capture on 2026-10-08 carries that same `last_modified`: the file was unchanged between the
  snapshot and the capture. The "Ad hoc" label and the "continuously published" description do
  not match this observed gap of days between updates. `TODO: verify` the real update cadence.
- The one captured body spans about 11.7 months before its `last_modified` (point times
  2025-10-10T10:00 to 2026-10-02T06:44, a 356.9-day span); a single capture does not show a rolling-window rule. If it is one,
  then under `whole_capture` history older than the newest body lives only in older captures,
  and a later capture would not re-supply points that have rolled out of the window.
  `TODO: verify` the vendor's retention rule, which is not stated.

## Licence and attribution

- Licence: NESO Open Data Licence
  ([licence text](https://www.neso.energy/data-portal/ngeso-open-licence))
- Attribution: Supported by National Energy SO Open Data

## Holds

- none

Nothing is held for this package. Both its resource and its family are eligible, and the hold
questions that apply to the rest of the AS-3b batch (the EAC mock clock and test-data labels, and
the ORPS identity, archive and price-input questions) concern other packages. The open
`TODO:` items above (`OBP-INSTRUCTION-IMMUTABILITY`, `INTERVAL-CLOSURE`, the `Target MW`
reference and the status vocabulary) are documented uncertainties that do not block publication.

## Links

- [NESO Open Data Portal package](https://www.neso.energy/data-portal/obp-non-bm-reserve-instructions)
- [Vendor field dictionary for the resource](https://www.neso.energy/data-portal/obp-non-bm-reserve-instructions/non-bm_instructions_from_obp)
- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/obp-non-bm-reserve-instructions.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- Batch facts: gridflow `@.planning/phases/v0.22-K-AS-3/K-AS-3-FACTS.md` §7, §9
- Sibling OBP pages: @obp-non-bm-physical-notifications.md ·
  @obp-reserve-availability-utilisation-price.md
- Domain: @../../../20-domain/markets/gb-balancing-mechanism.md
