---
source: "neso_data_portal"
package: "obp-non-bm-reserve-instructions"
dataset_key: "obp_reserve_instructions"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: OBP non-BM dispatch instructions
  summary: >-
    Dispatch and cease instructions NESO sent to non-BM units through its Open Balancing Platform
    (OBP), one row per point of each instruction.
  facts:
    vendor: "NESO Data Portal: one CSV, republished under a new file name"
    cadence: "Ad hoc, NESO says, and published through the day"
    grain: "One row per instruction point; `instruction_id` groups an instruction's points"
  landscape: market
  what_it_is: >-
    Instructions NESO sent to non-BM units through OBP for Positive Quick Reserve, Positive Slow
    Reserve and MW Dispatch. NESO says OBP takes over non-BM services from ASDP gradually; its ASDP page says
    they have moved. Each instruction is a run of points with target MW and indicative price.
    NESO publishes confirmed instructions, and every cease. Times are UTC, NESO says.
  how_used:
    - How often NESO calls Positive Quick and Slow Reserve, and which units
    - Indicative price per instruction, and where it changes at a settlement period
    - Instructed MW profiles, point by point, from ramp to cease
  chart:
    type: line
    silver: neso_data_portal/obp_reserve_instructions
    time: point_datetime
    value: target_price
    filter:
      - {column: instruction_point_type, op: eq, value: START}
    group: service_id
    group_map: {PQR: quick, PSR: slow, RDP: rdp}
    series_order: [slow, quick, rdp]
    aggregation: mean
    time_bucket: 1d
    window: {start: "2025-10-10", end: "2026-10-02"}
    unit: £/MWh
  chart_view:
    title: Indicative price at instruction start, per day
    caption: >-
      Silver `neso_data_portal/obp_reserve_instructions`, mean `target_price` of the START points
      per UTC day, £/MWh, 10 October 2025 to 2 October 2026. A dot is a day with instructions;
      days without draw nothing. NESO states no sign.
    alt: >-
      Dot chart from neso_data_portal/obp_reserve_instructions of the mean indicative price at
      instruction starts per UTC day, by service, 10 October 2025 to 2 October 2026, in £/MWh. Positive
      Quick Reserve has 19 days, from 119.42 on 20 April 2026 to 160 on 2 October 2026, and 150 on 10
      of them. Positive Slow Reserve has three days, 27 and 29 July and 5 August 2026: 169.07, 120 and 187.80.
      MW Dispatch is below zero on four days: -210 on 27 and 30 April, -99 on 20 May, -75 on 16 June.
    x_label: UTC day of the START point
    y_min: -240
    key:
      - {series: slow, label: Positive Slow Reserve, codes: PSR, paint: olive, note: "Three days, July and August 2026: 120 to 187.80."}
      - {series: quick, label: Positive Quick Reserve, codes: PQR, paint: petrol, note: "19 days; 150 on 10 of them."}
      - {series: rdp, label: MW Dispatch, codes: RDP, paint: clay, note: "Below zero on all four days: -210 to -75."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the one CSV downloaded whole unless its
      `last_modified` is unchanged. The file name changes with each publication.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=obp-non-bm-reserve-instructions"
      - "GET https://api.neso.energy/dataset/0ba217bb-846b-470e-9717-ff152d97d009/resource/dad63c1b-8a8e-47de-9922-7880384ef104/download/instr_20261002064426_qr_sr_nbm.csv"
    commands:
      - {run: gridflow ingest neso_data_portal obp_reserve_instructions --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal obp_reserve_instructions --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: instruction_id, op: in, value: ["7371155", "7541953"]}
      order_by: [instruction_id, sequence]
      columns: [sequence, instruction_point_type, point_datetime, target_mw, target_price,
                instruction_id, issue_datetime, instruction_status, unit_id, service_id,
                instruction_point_id]
    key: [instruction_point_id]
    caption: "Two instructions: Positive Slow Reserve, 29 July 2026; Positive Quick Reserve, 14 August, no STOP."
    fields:
      instruction_point_id: "NESO's unique key for each point, kept as text (its dictionary says integer)"
      instruction_id: "Groups one instruction's points (NESO); kept as text, not in time order"
      sequence: "Point order within the instruction; here one skips 4 and has no STOP"
      instruction_point_type: "`START`, `STOP` (cease starts), `SPP` (crosses a settlement period) or `VP` (vertex)"
      point_datetime: "When the point falls, UTC (NESO); the file's text has no zone marker"
      target_mw: "MW, \"power from PN in absolute values\" (NESO); no sign stated"
      target_price: "Indicative price, £/MWh (NESO); can change at an `SPP`; no sign stated"
      issue_datetime: "When NESO sent the instruction, UTC; START and STOP points only"
      instruction_status: "On START and STOP points; NESO lists `ACCEPTED`, `PROXY ACCEPTED`; `REJECTED` also appears"
      unit_id: "The non-BM unit instructed, as NESO registers it"
      service_id: "`PQR` Positive Quick Reserve, `PSR` Positive Slow Reserve or `RDP` MW Dispatch (NESO)"
      timestamp_utc: "Equals `point_datetime`, the point's UTC instant"
      published_at: "The CSV's portal last-modified time, read as UTC; one per capture"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_neso_data_portal_obp_reserve_instructions_latest`,
      filtered on `timestamp_utc` (the point time), both ends included. Times come back in the
      session's zone, UK time on UK machines; the first query cell converts `point_datetime` to UTC.
    cells:
      - |
        df = data.neso_data_portal.query(
            "obp_reserve_instructions", "2025-10-10", "2026-10-02")
        df["point_datetime"] = df.point_datetime.dt.tz_convert("UTC")
        df = df.sort_values(["timestamp_utc", "instruction_point_id"])
      - |
        starts = df[df.instruction_point_type == "START"]
        starts.groupby("service_id").agg(instructions=("instruction_id", "count"),
            units=("unit_id", "nunique"), lowest_price=("target_price", "min"),
            highest_price=("target_price", "max")).reset_index()
      - |
        call = df[df.timestamp_utc.between("2026-08-05 20:30Z", "2026-08-05 21:30Z")]
        call = call.sort_values(["unit_id", "sequence"])
        call.loc[call.unit_id == "KILN-01", ["service_id", "sequence", "instruction_point_type",
            "point_datetime", "target_mw", "target_price"]]
      - |
        ax = None
        for unit, g in call.groupby("unit_id"):
            ax = g.plot(x="point_datetime", y="target_mw", label=unit, marker=".", ax=ax,
                        figsize=(8, 3.5))
        ax.set(xlabel="point time, UTC, 5 August 2026", ylabel="target MW")
        ax.legend(ncol=3, fontsize=8);
    needs: a capture of NESO's OBP instructions file
    plot_alt: >-
      Line plot of target MW against point time, UTC, for the nine units NESO instructed at 20:36 on
      5 August 2026. KILN-01 ramps to 14 MW by 20:44:45 and is back at 0 by 21:25:32. The others
      sit at 1 to 3 MW; Positive Quick Reserve units reach 0 by 21:08, Positive Slow Reserve units
      between 21:12 and 21:29.
  related:
    - {dataset: neso_data_portal/non-bm-ancillary-service-dispatch-platform-asdp-instructions, note: "ASDP, NESO's earlier platform for non-BM instructions; never join its ids"}
    - {dataset: neso_data_portal/obp-non-bm-physical-notifications, note: "Each unit's PN; NESO gives `Target MW` as power from it"}
    - {dataset: neso_data_portal/obp-reserve-availability-utilisation-price, note: "Availability and utilisation prices for OBP reserve units"}
---

# Open Balancing Platform (OBP) - Non-BM Instructions

NESO's log of dispatch instructions sent to **non-BM** service providers through the Open
Balancing Platform (OBP), published as one CSV. The vendor says the file holds instructions "once
instructions have been confirmed by Service Providers", and that cease instructions are always
published whatever their status. It currently covers three services: Non-BM Quick Reserve,
Non-BM Slow Reserve and Non-BM MW Dispatch. The `service_id` values observed are `PQR`, `PSR`
and `RDP`. The vendor's example list for the column also names `NQR` and `NSR`, which do not
occur in the captured file. NESO decodes the codes on other packages (catalogue snapshot
`20261006T195819Z`): "Negative Quick Reserve (NQR) and Positive Quick Reserve (PQR)"
(`quick-reserve-auction-requirement-forecast`), "Negative Slow Reserve (NSR) and Positive Slow
Reserve (PSR)" (`slow-reserve-requirement-forecast`) and "Regional Development Programme (RDP)
MegaWatt (MW) Dispatch" (the ASDP package). This file covers only the services currently mastered in OBP (Quick
Reserve, Slow Reserve, MW Dispatch). The vendor says OBP will incrementally master more non-BM
services as they migrate, with less published on its separate ASDP page ("non-bm-ancillary-service-dispatch-platform-asdp-instructions").
That ASDP page now says the non-BM services it published "have now migrated to the OBP system" and
lists itself as "Not Active" (catalogue snapshot `20261006T195819Z`, package notes and extras). Its
monthly files (to April 2026) hold the earlier instructions, including Fast Reserve and STOR, which
are **not** in this file. Use the file
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
   unit, not on the syntax. The rows cannot test it at a clock change: no point or issue time falls
   on 26 October 2025 or 29 March 2026, the two UK clock changes inside the capture's span
   (checked 2026-10-18). Two observations fit UTC without proving it, both on BST days. On
   2 October 2026 the last point is `06:44:00`, the file name stamp `instr_20261002064426` reads
   06:44:26, and CKAN `last_modified` (read as UTC, ADR-030) is 06:44:33. An earlier publication,
   `instr_20260814163227_qr_sr_nbm.csv` with `last_modified` `2026-08-14T16:32:39` (gridflow
   `@.planning/phases/neso-data-portal/_probe/package_search_p0.json`), is stamped 16:32:27, and
   the last point on 14 August 2026 is `16:32:00`, with no point between that day and 2 October.
   Both times the stamp sits seconds after the last point, which UK local point times would not
   give. Verified on all 422 silver rows: `timestamp_utc` and `event_time`
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
  absolute MW level or a difference from the unit's PN. Project check (2026-10-18, against the
  silver of @obp-non-bm-physical-notifications.md, its 2026-10-08 and 2026-10-16 captures, which
  give the same values here; not a vendor statement): all 80 Positive Quick and Slow Reserve
  STARTs read 0 MW. 72 of the 85 START points fall inside a PN segment of the same unit, 65 of
  them on a PN of 0, which cannot tell the two readings apart. Seven Positive Quick Reserve STARTs
  on three units sit on a PN above zero and still read 0, then rise: `EDFE-8` at 2025-10-10T17:43
  (PN 4 MW, target 0 then 2), `ENGQR-02` at 18:44 and 19:03 on 2025-12-02 (PN 2, target 0 then
  1), and `ENGQR-03` three times on 2026-06-23 and once on 2026-07-02 (PN 1, target 0 then 1). An
  absolute level would not read 0 there, but seven rows on three units settle nothing: both PN
  captures postdate the instructions, so a PN revised afterwards cannot be ruled out, and one row
  fits the difference reading less neatly (`EDFE-21`, instruction `3193911`, target 10 MW from
  2025-10-10T17:20:03, while its PN steps from 0 to 10 at 17:30). The
  three RDP units (`UKPN-002`, `NGED-004`, `NGED-005`) have no PN rows, and their profiles run the
  other way (for example 3.922 at START, 0 through the instruction, 4.052 after the STOP), so the
  TODO stays open for RDP.
- `Target Price` → **£/MWh**. Dictionary: "Indicative Price". It is an indicative price, not a
  settled price.
- `Sequence`, `Instruction ID`, `Instruction Point ID`: dimensionless identifiers or counts.
  The dictionary types the two IDs as integers; gridflow stores both IDs
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
Checked 2026-10-18: four instructions have no STOP, which is why STOP (81) trails START (85).
They are `7541953`, `7542155`, `7542224` and `7542315` (Quick Reserve, all starting
2026-08-14T16:00); each skips `sequence` 4 and one `instruction_point_id` (for example `18824130`
then `18824132`), though NESO says cease instructions are always published. Neither id runs in
time order: `instruction_id` is 3191870 to 3193911 on 2025-10-10, 2035280 to 2035500 on
2025-12-02 and 855832 to 855943 on 2026-10-02, and `instruction_point_id` is 12315145 or more on 2025-10-10 but 2136469 to 2137475
on 2025-12-02; order by `point_datetime`, then `sequence`. One `SPP` is off the half-hour grid
(`ARTH-01`, instruction `7452940`, 2026-08-05T20:46:00, logged at the same instant as a `VP`);
the other 87 fall on :00 or :30. An instruction whose STOP falls on a boundary has no `SPP` there
(for example `7371155`, STOP at 2026-07-29T10:30:00), which fits the vendor's logging priority
(START/STOP, then SPP, then VP).
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
