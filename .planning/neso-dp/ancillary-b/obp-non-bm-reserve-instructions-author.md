# OBP non-BM dispatch instructions: writer report (2026-10-18)

Page `obp-non-bm-reserve-instructions`, one table, lead `obp_reserve_instructions`. The manifest's lead and member are
right (`package_tables`: slug to `obp_reserve_instructions`).

| Gate | Result |
|---|---|
| `gridflow-build --only neso_data_portal/obp_reserve_instructions` | ok (only the vault-wide "22 Known issues lines dropped" warning, which predates this work) |
| Detector | `[]` |
| Canonical note vs mirror | `cmp` clean; CRLF throughout; vault diff 157 insertions, 5 deletions |
| Rendered page | 0 em or en dashes, arrows or middle dots; none of live, now, yet, soon, planned, shipped, real-time, locally, held, ledger, TODO, our, "since 20", "% of", "N rows". The one "N days" hit is the key note "19 days", a count of the chart's dots |
| Screenshots | `.planning\neso-dp\ancillary-b\obp-reserve-instructions-shots\` at 1440, 1024, 768 (slices plus full page) and 390 (through a 390 px iframe). Nothing clipped or overlapping. Light only: the site has no dark theme |
| Server | my 9984 server is stopped; 9670 not touched |

Artefacts (no staged spec or authored override existed):
- `site\hifi\data\series\neso_data_portal\obp_reserve_instructions.json`: `spec_origin: vault`, 3 series over 24 days, 85 START rows used of 422.
- `site\hifi\data\samples\neso_data_portal\obp_reserve_instructions.json`: `gridflow-sample`, 8 rows, 19 columns.
- `site\hifi\data\notebooks\neso_data_portal\obp_reserve_instructions.json` and `-6.png`: `run_notebooks.py`, 6 cells, no errors.

## The four questions

1. **What one row is, and the ASDP relation.** One row is one point of an instruction (START, STOP, SPP or VP);
   `instruction_id` groups an instruction's 4 to 7 points and `sequence` orders them (NESO dictionary). Each instruction
   is for one unit and one service. On ASDP, NESO's own words only. The OBP package notes say OBP "will incrementally
   master more non-BM services, and less will be mastered by ASDP". The ASDP package notes say its services "have now
   migrated to the OBP system", and its extras say "Update Frequency: Not Active" (catalogue snapshot
   `20261006T195819Z`). The rows agree but prove no replacement. ASDP has no OBP service code; its last start is
   17 April 2026 (Fast Reserve), and its last RDP is November 2025. OBP has Quick Reserve from October 2025 and RDP from
   27 April 2026. One RDP unit, `UKPN-002`, appears in both. The page says "takes over ... step by step" and "its ASDP
   page says they have moved", and nothing more.
2. **Time columns.** `Point Datetime` and `Issue Datetime` are spelled `YYYY-MM-DDTHH:MM:SS` with no zone marker in
   every cell. NESO's dictionary gives the unit as "UTC", with examples ending in `Z`. No row falls on either UK clock
   change in the span (26 October 2025, 29 March 2026), so the rows cannot test it, and none falls in a skipped hour.
   One observation fits UTC without proving it (on 2 October 2026, in BST: last point 06:44:00, file name stamp
   06:44:26, CKAN `last_modified` 06:44:33). The page says "Times are UTC, NESO says" and "the file's text has no zone
   marker". Separately, the workbench returns these TIMESTAMPTZ columns in the session zone, so the notebook prints
   `+01:00` on this machine until converted. The lead says so and cell one converts `point_datetime` to UTC.
3. **Units and signs (NESO dictionary only).** `Target MW` is in MW, described as "Power from PN in absolute values".
   `Target Price` is in £/MWh, described as "Indicative Price". No sign convention is stated for either, and the page
   says "no sign stated" for both. In this file, MW runs 0 to 24 and prices run -210 to 197.85. All five RDP
   instructions have negative prices (-210, -210, -210, -99, -75).
4. **Duplicates, overlap, truncation.** There is one resource and one capture: bronze `2026/10/08`, 422 data lines plus
   a header, ending in a newline, matching the profile (`rows: 422`, `ends_with_newline: true`). Silver has 422 rows. No
   later capture exists. `client.py` 1752 to 1767 skips an upload whose newest capture carries the live
   `last_modified`, which fits a file unchanged since 2 October, but I cannot confirm that without a live call. So
   there is no truncation risk here. `instruction_point_id` is unique (422), and so is (`instruction_id`, `sequence`).
   There are 0 duplicate rows apart from the key and 0 duplicate (instruction, type, time). There is no cross-file
   overlap: ASDP shares no service code or id space with OBP, and the ASDP page's related note says never join ids.

## Chart choice

The chart is a line (dot) chart: the mean `target_price` of START points per UTC day, by service, over the whole file
(10 October 2025 to 2 October 2026). I set `y_min: -240`. With 19, 3 and 4 days per series, each renders as dots; one
short segment joins 9 and 10 May. It shows the column with the sign question (RDP below zero) and how often each
service is called. MW was rejected for the chart because `Target MW`'s reference is unsettled (below). A raw unbucketed
line breaks at every point, since the renderer's step is the smallest gap, 1 second.

## Evidence

| Claim (page field) | Evidence |
|---|---|
| summary, `what_it_is`: dispatch and cease instructions via OBP for Quick, Slow Reserve and MW Dispatch | OBP package notes ("hosts Non-BM Quick Reserve, Non-BM Slow Reserve Service and Non-BM MW Dispatch Service Instructions data"), snapshot `20261006T195819Z` |
| "NESO publishes confirmed instructions, and every cease" | resource description: "once instructions have been confirmed by Service Providers (cease instructions are always published regardless of the instruction status)" |
| "OBP takes over non-BM services from ASDP step by step; its ASDP page says they have moved" | OBP notes, "incrementally master more non-BM services, and less will be mastered by ASDP"; ASDP notes, "have now migrated to the OBP system" |
| "Times are UTC, NESO says" | field info `.planning/research/neso-snapshots/field-info/20261008T114228Z/obp_reserve_instructions.json`: `Point Datetime` and `Issue Datetime` unit "UTC"; registry `zone: UTC` |
| facts.vendor "one CSV, republished under a new file name" | registry one resource, `url_type: upload`; file name `instr_20261002064426_qr_sr_nbm.csv` embeds a generation stamp (note, Files) |
| facts.cadence "Ad hoc, NESO says, and published through the day" | extras "Update frequency: Ad hoc"; notes "continuously published throughout the day" |
| facts.grain, key | dictionary: Instruction ID "can be used to group together all points"; Instruction Point ID "Unique Key for the reporting entry"; registry `entity_key: [instruction_point_id]` |
| chart caption: mean of START per UTC day, £/MWh, window, "NESO states no sign" | spec: filter `instruction_point_type eq START`, `aggregation: mean`, `time_bucket: 1d` on `point_datetime` (UTC), window 2025-10-10 to 2026-10-02; field info shows no sign rule |
| key notes and alt | committed series. slow: 169.07 (27 Jul), 120 (29 Jul), 187.804 (5 Aug). quick: 19 values, min 119.417 (20 Apr), max 160 (2 Oct 2026), exactly 150 on 10 (2 Dec, 27 Mar, 17 Apr, 9, 10, 12, 19 May, 6 Jun, 27 Jul, 30 Jul). rdp: -210 (27 and 30 Apr), -99 (20 May), -75 (16 Jun) |
| key labels: `PQR` Quick, `PSR` Slow, `RDP` MW Dispatch | **inference** (see Unverified): NESO lists the three services and the codes `PQR, NQR, PSR, NSR, RDP` but never decodes them; ASDP's notes name "Regional Development Programme (RDP) MegaWatt (MW) Dispatch" |
| raw requests | `package_show` (CKAN action, as the approved upload pages show); the upload URL is the captured `request_url` in the bronze sidecar |
| raw note "downloaded whole unless its `last_modified` is unchanged" | `client.py` `iter_members` 1752 to 1767 |
| commands `--last 24h` | same form as the approved upload pages (industry notifications, BSAD forward contracts); silver partitions by capture date (`year=2026/month=10` holds points from 2025) |
| frame caption: two instructions, Slow Reserve 29 July 2026, Quick Reserve 14 August 2026 with its STOP missing | sample rows: 7371155 (`ENPR-01`, `PSR`, sequences 1 to 4) and 7541953 (`ENGQR-05`, `PQR`, sequences 1, 2, 3, 5; point ids 18824128 to 18824130 then 18824132) |
| field `sequence` "here one skips 4, its missing STOP" | the same rows |
| field `instruction_id` "not in time order" | per day: 3191870 to 3193911 on 2025-10-10, 2035280 to 2035500 on 2025-12-02, 855832 to 855943 on 2026-10-02 |
| field `instruction_point_type` | dictionary: "START is the start of Dispatch instruction, STOP is the start of Cease instruction, SPP ... crosses a SP, VP ... any other angle/vertex point" |
| field `point_datetime` "UTC (NESO); the file's text has no zone marker" | field info unit UTC; profile `naive_datetime` shapes; bronze cells such as `2025-10-10T10:00:01` |
| field `target_mw` | dictionary text quoted exactly; unit MW |
| field `target_price` "can change at an `SPP`" | the frame does not show this; the rows do: 8 of 85 instructions change price, always at an SPP (for example 3191870: 110.79, then 118.83 at 10:30, 120.56 at 11:00, 116.88 at 11:30) |
| field `issue_datetime` | dictionary: "Time at which Dispatch instruction is sent to Provider; available for START and STOP instruction points" |
| field `instruction_status` | dictionary: "ACCEPTED, PROXY ACCEPTED; available for START and STOP"; `REJECTED` on 1 row (6425772, a STOP) |
| field `published_at` "one per capture" | registry `vintage: ckan_last_modified`; one value on all 422 rows |
| notebook lead | manifest: relation `silver_neso_data_portal_obp_reserve_instructions_latest`, `designated_date_col='timestamp_utc'`, TIMESTAMPTZ; `source.py` 437 to 440 inclusive end via `_date_range_predicate`; `control/inspect.py:85` "in the session timezone (Europe/London on UK hosts)"; first run printed `2026-08-05 21:36:00+01:00` for 20:36 UTC |
| notebook outputs | PQR 73 instructions, 14 units, 110.79 to 180.00; PSR 7, 7, 120.00 to 197.85; RDP 5, 3, -210.00 to -75.00; KILN-01's five points |
| `plot_alt` | 5 August 2026 rows: KILN-01 VP 14 MW at 20:44:45, back to 0 at 21:25:32; Quick units reach 0 at 21:07:15 to 21:08:00; Slow units at 21:12:02 to 21:29:00; others 1 to 3 MW |
| related | ASDP note's own "never join ids"; dictionary "Power from PN"; the availability table shares 21 of the 24 units (all but the three RDP units). All three slugs are in the page set |

## Body corrections (canonical note, smallest spans)

1. **Opening paragraph.** The note said other non-BM instructions "are still published there [ASDP] and are **not** in
   this file". That is stale. NESO's ASDP page now says its services "have now migrated to the OBP system" and lists
   itself as "Not Active". I replaced the clause with that, and with the fact that ASDP's monthly files (to April 2026)
   hold the earlier instructions, including Fast Reserve and STOR, which this file lacks.
2. **Event time.** Added: no point or issue time falls on either clock-change day in the span, so the rows cannot test
   UTC. Also added the one fitting observation (file name stamp and CKAN `last_modified`), marked as not proof.
3. **Units, `Target MW` TODO.** Added the project check against the physical-notifications silver. 72 of 85 STARTs fall
   inside a PN segment of the same unit. Seven Quick Reserve STARTs sit on a PN of 1 to 4 MW and still read 0, then rise
   to 1 or 2. For those rows it behaves as a difference from PN. The RDP units have no PN rows, and their profile runs
   the other way (3.922, then 0, then 4.052), so the TODO stays open for RDP.
4. **Units, identifiers.** "gridflow stores all three opaque identifiers as strings" became "both IDs". `sequence` is
   `int64` (registry).
5. **Identity and selection.** Added four facts. Four instructions have no STOP, which is why STOP is 81 against
   START's 85. Neither id runs in time order. One SPP is off the half-hour grid. A STOP on a boundary carries no SPP,
   which fits NESO's logging priority.

## Unverified

- **Service codes.** NESO never decodes `PQR`, `PSR` and `RDP`. The page maps them to Quick Reserve, Slow Reserve and
  MW Dispatch. The basis is NESO's list of the three services this file hosts plus the code letters, and the ASDP notes'
  "Regional Development Programme (RDP) MegaWatt (MW) Dispatch". If the checker wants this softer, the `service_id`
  line can read "`PQR`, `PSR` or `RDP`, NESO's codes for its three services".
- **The UTC clock.** It rests on NESO's dictionary alone; no row tests it.
- **`Target MW`'s reference for RDP**, and what a negative RDP price means. The page says only "no sign stated".
- **Why no 2026-10-16 capture exists** (most likely the upload skip on an unchanged `last_modified`; not confirmed
  without a live call).

## Open questions

None blocking.

## Template problems (seat items)

1. **Notebook preview and hanging indents.** At 390 px the notebook preview keeps a continuation line's leading spaces
   and then wraps character by character. A call aligned under its opening bracket rendered as a one-character column.
   I worked around it with a 4-space hanging indent; the renderer could collapse or cap leading spaces when it wraps.
2. **No dot chart for irregular events.** A line chart with no `time_bucket` uses the smallest x gap (1 second here) as
   its step, so per-event data draws as isolated dots. This page buckets to a day instead.
3. Known items seen again: the folded frame at 768 px (mitigated by putting the value columns first), and the notebook
   tab label clipping at 390 px.

## Defects

- **NESO data: four Quick Reserve instructions have no STOP point.** Package `obp-non-bm-reserve-instructions`,
  instructions `7541953`, `7542155`, `7542224` and `7542315` (units ENGQR-05, -06, -01, -03), all starting
  2026-08-14T16:00. Each skips `sequence` 4 and one `instruction_point_id` (for example 18824130, then 18824132). NESO
  says cease instructions are always published regardless of status. This is a vendor data gap; gridflow keeps the rows
  as published. Recorded in the note's Identity paragraph.
- **NESO data: one SPP is off the settlement-period grid.** Instruction `7452940` (ARTH-01, Slow Reserve) has an `SPP`
  at 2026-08-05T20:46:00, at the same instant as a `VP`. The other 87 SPPs fall on :00 or :30. Minor; recorded in the
  note.
- **NESO data: ids are not monotone in time.** `instruction_id` is 3.19 million in October 2025, 2.04 million in
  December 2025 and 0.86 million in October 2026, and `instruction_point_id` also falls between those dates. Consumers
  must order by `point_datetime`, then `sequence`. Not a gridflow bug; recorded in the note.
- **gridflow_models (usability, possibly known):** `data.<source>.query()` returns TIMESTAMPTZ columns in the DuckDB
  session zone (Europe/London here, so `+01:00` in BST). `control/inspect.py` converts to UTC but `query()` does not.
  The page's lead tells the reader, and the notebook converts.
- **Vault note (fixed here):** the stale claim that other non-BM instructions are still published on the ASDP page.
