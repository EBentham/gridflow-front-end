---
source: "neso_data_portal"
package: "day-ahead-constraint-flows-and-limits"
dataset_key: "da_constraint_flows_limits"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: Boundary and half-hour pairs repeat; NESO leaves 99999 limits, the flow's unit and clock changes unexplained.
  title: Day-ahead constraint flows and limits
  summary: >-
    NESO's day-ahead limit, in MW, and forecast flow for each main transmission boundary and half
    hour, kept as a rolling archive.
  facts:
    vendor: "NESO Data Portal, package `day-ahead-constraint-flows-and-limits`: one CSV file, two diagrams"
    cadence: "Daily (Weekdays), as NESO lists it; each upload is the whole archive"
    grain: "Each row: a boundary code and half hour (GMT/BST), with limit and flow"
    history: NESO keeps the past three years plus the current year; earlier on request
  landscape: market
  what_it_is: >-
    NESO models each boundary's flow the day before, from its wind, generation and demand
    forecasts, and gives the boundary's limit in MW beside it. The flows are not revised after
    publication. From 22 April 2024 they no longer allow for constraint mitigation actions, so
    earlier rows are not like for like. NESO's diagrams show each boundary's positive flow
    direction.
  how_used:
    - How close NESO expected each boundary to run to its limit, a day ahead
    - Congestion risk by boundary, as an input to constraint cost models
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then each file whole unless its `last_modified` is
      unchanged. Every upload repeats the whole archive. The diagrams are re-issued under new names.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=day-ahead-constraint-flows-and-limits"
      - "GET https://api.neso.energy/dataset/cf3cbc92-2d5d-4c2b-bd29-e11a21070b26/resource/38a18ec1-9e40-465d-93fb-301e80fd1352/download/day-ahead-constraints-limits-and-flow-output-v1.5.csv"
      - "GET https://api.neso.energy/dataset/cf3cbc92-2d5d-4c2b-bd29-e11a21070b26/resource/bb6d6ec6-16d9-4be5-b32c-1a70c09fd871/download/ew-network-diagram-da-limit-boundaries-oct2026.pdf"
      - "GET https://api.neso.energy/dataset/cf3cbc92-2d5d-4c2b-bd29-e11a21070b26/resource/3eb74046-3ffa-40c3-a541-b3cb00a44b1f/download/scotland-network-diagram-da-limit-boundaries-oct2026.pdf"
    commands:
      - {run: gridflow ingest neso_data_portal da_constraint_flows_limits --last 24h, comment: "the whole archive, bronze only"}
      - {run: gridflow ingest neso_data_portal da_constraint_flows_limits_files --last 24h, comment: the two network diagrams}
    sample:
      table: da_constraint_flows_limits
      file: day-ahead-constraints-limits-and-flow-output-v1.5.csv
      caveat: Times carry no offset; NESO does not say whether each starts or ends its half hour.
  related:
    - {dataset: neso_data_portal/24-months-ahead-constraint-limits, note: "NESO's weekly limits, 24 months ahead; ten boundary codes match exactly"}
    - {dataset: neso_data_portal/thermal-constraint-costs, note: "Outturn thermal constraint costs; five boundary codes match exactly"}
    - {dataset: neso_data_portal/operational-transparency-forum-network-congestion-data, note: "Weekly forecast and actual boundary limits, under different codes"}
    - {dataset: neso_data_portal/constraint-breakdown, note: "NESO's daily constraint costs and volumes, split by reason"}
---

# Day Ahead Constraint Flows and Limits

This package is NESO's day-ahead snapshot of **limits and power flows across the
transmission-network constraint boundaries**, in half-hourly steps. For each constraint group
(a named boundary such as ESTEX or SCOTEX, drawn on the package's two network diagrams) and
each settlement-period timestamp, the CSV gives the boundary's `Limit_MW` (the maximum power
that can flow through it) and `Flow_MW` (the forecast flow). The vendor says the flows are
calculated at the day-ahead stage, from the next day's wind forecast, generation dispatch and
demand forecast, and modelled in power-system software. They are the forecast position after
day-ahead energy scheduling and are not revised after publication. The diagrams show an arrow
for the positive direction of flow across each boundary, which is the only sign convention the
vendor gives (so negative flows are valid values, not errors). It answers "how close did NESO
expect each boundary to run to its limit the day before?", which is a congestion-risk
input for GB constraint-cost and redispatch modelling, not a measurement of what happened.

**Five things to know before using any of it.**

1. **The one data family is held (unit E-SEM) and its capture failed.** The single CSV capture
   (2026-10-08, 733,649 data rows) was adjudicated **failed** under ADR-040 (RULINGS 632): the
   archive repeats `(Constraint Group, target timestamp)` keys, so the duplicate-key guard raises
   `DuplicateEntityKeyError` and nothing is written. The second capture (2026-10-16, 740,443
   data rows) fails the same way and is reported as a reconcile gap (gridflow
   `@.planning/phases/v0.22-close/refresh-20261016/DRIFT.md`). **Silver holds 0 rows for this package**
   (RULINGS 635; no `da_constraint_flows_limits` directory exists under
   `C:/gridflow-data/silver/neso_data_portal/`). Bronze holds the immutable CSV and the two PDFs.
   This note gives schema, counts and clocks and no data values or ranges. Under ruling 66
   (2026-10-24) the site page shows the header and first eight lines of the CSV as fetched, and
   no table.
2. **It is a rolling historical archive, not just the next day.** The vendor says the file is
   limited to the past three years plus the current year (for 2026, records from 2023 through
   2026 inclusive) and earlier data is available on request. The captured body is consistent
   with that. Each row is a day-ahead forecast for a target time; the file carries no issue or
   publication column, so the instant each archived row became available is not evidenced.
3. **No temporal recipe.** `timestamp_utc` would be gridflow's capture time. The target time is
   kept as a raw string column (`date_time_gmt_bst_raw`) because the period endpoint and the
   treatment of the repeated autumn hour are undocumented.
4. **The meaning of `Flow_MW` has changed inside the archive.** The vendor says that from
   22 April 2024 the flows no longer consider expected constraint mitigation or optimisation
   actions; before that date they did, because the collating software changed. Rows either side
   of that date are not like for like.
5. **The sibling constraint tables use different, overlapping boundary codes.** Codes are stored
   exactly as published and never merged (see "Boundary codes" below).

Related packages in the same publisher group:
@./24-months-ahead-constraint-limits.md (weekly boundary limits, 24 months ahead),
@./thermal-constraint-costs.md (outturn costs by constraint group),
@./operational-transparency-forum-network-congestion-data.md (weekly forecast and actual
boundary limits) and @./voltage-requirement.md. The shared research for the whole constraint
batch is gridflow `@.planning/phases/v0.22-K-CON/K-CON-FACTS.md` (section 4 for this package,
section 8 for the cross-table boundary codes).

- Publisher group: Constraint management
- Registry group: constraint-management · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Day Ahead Constraint Flows and Limits | CSV | upload | `38a18ec1-9e40-465d-93fb-301e80fd1352` |

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Network Diagram England & Wales | PDF | upload | `bb6d6ec6-16d9-4be5-b32c-1a70c09fd871` |
| Network Diagram Scotland | PDF | upload | `3eb74046-3ffa-40c3-a541-b3cb00a44b1f` |

**Downloads and captures.** All three resources have `url_type: upload` and were first captured
on 2026-10-08, from `api.neso.energy` (sizes and CKAN `last_modified` from each sidecar under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`; URLs from the catalogue
snapshot `20261006T195819Z`), and all three again on 2026-10-16 (second table). The package was
created on 2019-11-05.

| Resource | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---:|---:|---|
| Day Ahead Constraint Flows and Limits | [day-ahead-constraints-limits-and-flow-output-v1.5.csv](https://api.neso.energy/dataset/cf3cbc92-2d5d-4c2b-bd29-e11a21070b26/resource/38a18ec1-9e40-465d-93fb-301e80fd1352/download/day-ahead-constraints-limits-and-flow-output-v1.5.csv) | 28,054,626 | 733,649 | 2026-10-07T17:28:41.804546 |
| Network Diagram England & Wales (DOC) | [ew-network-diagram-da-limit-boundaries2026.pdf](https://api.neso.energy/dataset/cf3cbc92-2d5d-4c2b-bd29-e11a21070b26/resource/bb6d6ec6-16d9-4be5-b32c-1a70c09fd871/download/ew-network-diagram-da-limit-boundaries2026.pdf) | 442,083 | n/a | 2026-07-10T11:05:51.346242 |
| Network Diagram Scotland (DOC) | [scotland-network-diagram-da-limit-boundaries2026.pdf](https://api.neso.energy/dataset/cf3cbc92-2d5d-4c2b-bd29-e11a21070b26/resource/3eb74046-3ffa-40c3-a541-b3cb00a44b1f/download/scotland-network-diagram-da-limit-boundaries2026.pdf) | 335,479 | n/a | 2026-07-10T11:04:48.337491 |

Captured again on 2026-10-16 (sidecars under `.../<family>/2026/10/16/`). Both diagrams were
re-issued under new file names; the CSV keeps its name:

| Resource | Download | Bytes | Data rows | CKAN `last_modified` |
|---|---|---:|---:|---|
| Day Ahead Constraint Flows and Limits | [day-ahead-constraints-limits-and-flow-output-v1.5.csv](https://api.neso.energy/dataset/cf3cbc92-2d5d-4c2b-bd29-e11a21070b26/resource/38a18ec1-9e40-465d-93fb-301e80fd1352/download/day-ahead-constraints-limits-and-flow-output-v1.5.csv) | 28,324,304 | 740,443 | 2026-10-16T15:42:40.975426 |
| Network Diagram England & Wales (DOC) | [ew-network-diagram-da-limit-boundaries-oct2026.pdf](https://api.neso.energy/dataset/cf3cbc92-2d5d-4c2b-bd29-e11a21070b26/resource/bb6d6ec6-16d9-4be5-b32c-1a70c09fd871/download/ew-network-diagram-da-limit-boundaries-oct2026.pdf) | 525,665 | n/a | 2026-10-13T15:19:44.151022 |
| Network Diagram Scotland (DOC) | [scotland-network-diagram-da-limit-boundaries-oct2026.pdf](https://api.neso.energy/dataset/cf3cbc92-2d5d-4c2b-bd29-e11a21070b26/resource/3eb74046-3ffa-40c3-a541-b3cb00a44b1f/download/scotland-network-diagram-da-limit-boundaries-oct2026.pdf) | 346,472 | n/a | 2026-10-16T11:26:01.320200 |

- **The CSV is also a CKAN datastore table** (field info records `datastore_active`; the
  datastore total of 733,649 equals the CSV data-row count). gridflow captures the uploaded
  file, not the datastore dump, so `url_type` is `upload` and the vintage is
  `ckan_last_modified` (ADR-030, ADR-033).
- **The two PDFs are network diagrams (DOC).** They locate the constraint boundaries and show
  the positive flow direction. The England and Wales diagram names the FLOWSTH, GM+SNOW5A,
  HARSPNBLY, DRESHEX1, ESTEX, ESTEX3, ESTEX4, DUNSELEX, CANDUNEX, CANSELEX, NINSELEX,
  BOLSELEX1, SEIMPPR23 and SSHARN3 groups; the Scotland diagram names SSE + GRMO, NKILGRMO,
  SCOTEX, SSE-SP2 and SSE N-S (vendor resource descriptions). They are reference documents, not
  a replacement for a code crosswalk, and they are not loaded to silver.
- **Resource-level facts the vendor gives.** Update frequency is "Daily (Weekdays)". The CSV's
  file name carries a version token (`v1.5`); `TODO: verify` whether NESO changes the file
  name or the layout when it bumps that version, since the record accepts only the one header
  epoch below.

## Families

*Identity and selection.* One resource, two captures (2026-10-08 and 2026-10-16), one header
epoch, the same header in both (`dataset_version` `1+e1` would apply). The record sets `latest` to `whole_capture`; a later NESO re-upload would
add a new whole capture and `_latest` would take it whole, and a bronze capture is never
edited. The entity key is the tuple in the family block below, which **is not unique on the
captured body** (see "Why the capture failed"). The archive is never deduplicated, no ordinal
key is invented, and no value column is added to the key.

*The two clocks.*

1. **Vintage: `ckan_last_modified`.** `published_at` and `available_at` are the CKAN
   `last_modified` of the captured file, both equal: **2026-10-07T17:28:41.804546** for the first
   capture and 2026-10-16T15:42:40.975426 for the second (ADR-030). It is not the capture time and not the target time. An as-of query is
   `WHERE available_at <= :as_of` (RULINGS 597). This is the vintage of the whole file: a
   re-upload re-stamps every row, including rows for targets years in the past, so
   `available_at` says nothing about when a particular archived forecast was first issued.
2. **Event time: none.** The record has `temporal: none`, so `timestamp_utc` is the capture
   time and `event_time` equals it on every row (capture 2026-10-08T09:16:59 UTC). It carries no
   information about the target time. The target time is the vendor `Date_ Time GMT_BST`
   column, kept raw as a string. Do not use `timestamp_utc` for a time axis. The vendor
   describes the target as a date and time on the GMT/BST clock at settlement-period
   (half-hourly) grain. The vendor dictionary states the spelling as `MM/DD/YYYY HH:MM`, but its
   own example and the captured body use a year-first form, and the body mixes a spelling with
   seconds and a spelling that stops at minutes (counts below); `TODO: verify` the intended
   format with NESO. Which end of the half hour the timestamp denotes, and how the repeated hour
   of an autumn clock change is represented, are both undocumented (the hold).

*Units (vendor dictionary only).* `Limit_MW` is **MW** (dictionary unit, "the maximum amount of
power that can flow through a constraint boundary"). `Flow_MW` has **no unit in the vendor
dictionary** (the unit field is blank; the column title is just "Flow"). The `_MW` in the
column identifier suggests MW, but a unit is never taken from a column name, so the `Flow_MW`
unit is `TODO: verify` with NESO (part of the hold). The vendor dictionary types `Limit_MW`
as integer and `Flow_MW` as a generic number; the record casts both to int64, and `TODO:
verify` that every `Flow_MW` cell is integral, because no silver exists on which the cast has
been exercised.

*Sentinels and missing values (FACTS g5).* NESO declares no sentinel or null token.
Observed on the body, by column: `Limit_MW` has blank cells, numeric zeros and the value
`99999`; `Flow_MW` has blank cells, numeric zeros, `-1` and other negative values; neither
column has `NA` or `N/A`. Handling, which is the same whatever NESO later says:

- Blank cells are nullable (both value columns are `nullable: yes`).
- Zeros are zeros and are never converted to null or filled.
- `99999` and `-1` are **not** converted to null and not interpreted. They are stored as
  published until NESO defines them. `-1` in `Flow_MW` cannot be assumed to be a missing-value
  token: flows are signed, and other negative flows exist.
- `TODO: verify` with NESO the meaning of blank cells and of `99999` in `Limit_MW`.
- The record has no null-token map.

*Boundary codes.* `Constraint Group` is stored exactly as published: no case change,
punctuation replacement or alias. The body has **31 distinct codes**, several of which
are near-spellings of one another or of codes in other constraint tables. The codes are a
join hazard, so none is ever merged:

- The captured spelling differs from the diagram text for some groups (for example an
  underscore where a diagram has a plus sign or a hyphen); `TODO: verify` the exact
  code-to-boundary crosswalk with NESO. The 31 observed codes outnumber the 14 + 5 named in
  the diagram descriptions, and the vendor's own column description says "the ten most important
  boundaries are included in this data file". The count disagreement is unexplained
  (`TODO: verify`).
- Variants that must never be merged without a vendor crosswalk with applicability dates:
  `SSHARN` / `SSHARN3` / `SSHARN7` / `SHARN`; `SEIMP` / `SEIMPPR21` / `SEIMPPR23` /
  `SEIMPPR33`; `SSE_SP` / `SSE_SP2`; `SSE_GRMO` against the `SSE_GRM` of
  @./24-months-ahead-constraint-limits.md; `DRESHEX1` against `DRESHEX`.
- Overlap with the sibling tables by exact raw string (FACTS section 8): 10 codes in common
  with the 24-months-ahead limits table (12 codes), 5 with thermal constraint costs (6 codes),
  and 0 with the network-congestion table (11 labels). The exact code set is in FACTS
  section 8. Codes here are constraint-group names, not EIC codes
  (@../../../20-domain/concepts/eic-codes.md) and not BM unit ids; never join them to either.

*Silver layout.* None for this package. A held family that loaded would write one Parquet file
per family under `C:/gridflow-data/silver/neso_data_portal/da_constraint_flows_limits/`,
partitioned `year=`/`month=` by capture date, with the lineage columns `resource_id`,
`timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`,
`available_at`, `source_run_id`, `dataset_version` appended to the vendor columns.

### `da_constraint_flows_limits`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Constraint Group | `constraint_group` | string | — | no | — | — |
| Date_ Time GMT_BST | `date_time_gmt_bst_raw` | string | — | no | — | — |
| Limit_MW | `limit_mw` | int64 | — | yes | — | MW |
| Flow_MW | `flow_mw` | int64 | — | yes | — | — |

- Entity key: `constraint_group`, `date_time_gmt_bst_raw`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Silver: 0 rows. HELD (E-SEM). Capture adjudicated failed (ADR-040).** Under ruling 66
(2026-10-24) the site page shows the header and first eight lines of the 16 October 2026 capture
of the CSV, as fetched, and no table. The
source header is `Constraint Group`, `Date_ Time GMT_BST` (note the space after the
underscore), `Limit_MW`, `Flow_MW`; the vendor header contains no unit text. The record has
one epoch; the first capture's body is 733,649 data rows, 28,054,626 bytes, UTF-8 (the second:
740,443 rows, 28,324,304 bytes). Both vendor
value columns are blank on some rows. Vintage if it had loaded: `published_at` = `available_at`
= 2026-10-07T17:28:41.804546 UTC; `timestamp_utc` = 2026-10-08T09:16:59.217830 UTC.

**Why the capture failed (RULINGS 632, `_reconcile_adjudications.json`).** On the full body:

- The target timestamp has two spellings, **649,074 rows with seconds and 84,575 stopping at
  minutes**; one strict format would have to be verified against both.
- The key `(constraint_group, raw timestamp)` has **732,213 distinct values across 733,649
  rows, so 1,436 duplicate excess rows**. Of these, **1,392 are whole-row duplicates** (the
  extra rows repeat every source column) and the remaining excess comes from **44 key groups
  whose Limit_MW or Flow_MW differ between the repeated rows**. The two kinds have different
  causes (checked on both captures, 2026-10-23). All 44 value-differing groups are the repeated
  autumn hour: 01:00 and 01:30 on 2024-10-27 and 2025-10-26, 11 boundaries each, so a fold rule
  would separate them. The 1,392 whole-row duplicates are two whole repeated days: 2025-08-12 at
  11 boundaries (528 excess rows) and 2026-08-19 at 18 boundaries (864), which no fold rule
  explains. The whole-row duplicates persist when rows with blank limit and flow are excluded.
  On both captures 8,166 `Limit_MW` cells are `99999` and 3,365 `Flow_MW` cells are blank.
- Adding the value columns to the key therefore does not make it unique, and no vendor-column
  key is lossless. gridflow does not deduplicate bronze and does not invent an ordinal key.
- The engine's duplicate guard raises `DuplicateEntityKeyError` on the repeated keys, which is
  an ADR-040 allowlisted failure class. The batch's transform run failed this capture and wrote
  nothing (`@.planning/phases/v0.22-K-CON/post-merge/transform.log`); the adjudication entry
  records it as `failed` so reconcile treats it as known, not as a gap (reconcile
  `--all --cutoff 2026-10-08`: exit 0, 105 families, 0 gaps, 15 adjudicated, 0 stale).

**The forward-target test also fails (RULINGS 529).** The record has no issue column
(`issue: none`). Of 733,649 rows, **732,332 have a target calendar date strictly before the
vintage date**, so the file is a retrospective forecast archive, not a forward-only one, and the
CKAN vintage cannot be read as availability-at-issue for those rows. This is independent of the
duplicate-key failure: even a clean load would stay held. The 2026-10-16 capture is the same:
738,687 of 740,443 targets fall before its vintage date, and its key repeats on the same 1,436
excess rows (1,392 whole-row duplicates), so it fails the same guard (checked on bronze, 2026-10-23).

### `da_constraint_flows_limits_files`

- Kind: files · archetype: FC · refresh: daily · empty allowed: no
- files: catalogue only

This is the catalogue family for the two PDF network diagrams (DOC). It has no silver output
and no record. Bronze holds two captures of each diagram, 2026-10-08 and 2026-10-16. NESO
re-issued both in October 2026 under new names (`...-boundaries-oct2026.pdf`, vintages
2026-10-13 and 2026-10-16), so the diagrams are versioned in the file name and the download URL
changes with each issue (`TODO: verify` whether the boundary list in the diagram text follows
the data).

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Daily (Weekdays)

The registry refresh is daily and the vendor says weekdays. gridflow has captured the package
twice: 2026-10-08 (the portal sweep) and 2026-10-16 (the first daily refresh). The file is a
rolling window re-uploaded whole, and each refresh adds a new whole capture with a new vintage
and the same duplicate-key hazard; the hold and the failure apply to each such capture until
NESO answers the questions below. Between the two captures the file only grew: every distinct
row of the first is in the second, no key was dropped, and 6,794 new keys were added (targets
now to 2026-10-17; the earliest is still 2023-01-01). Checked on bronze, 2026-10-23. Whether the
three-year window drops its oldest year at a year boundary in one step (so that rows disappear
from the latest file) is `TODO: verify`; no year boundary has passed between captures.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `da_constraint_flows_limits`: held: TODO: what period start/end and DST-fold treatment does the target timestamp denote, what are Flow_MW's unit and the meaning of blanks and 99999, and what row grain makes the archive unique? The archive has no issue column (RULINGS 529 fails: 732,332 targets precede the vintage). (unit E-SEM)

The hold is one family-level question with four parts (all **domain-truth questions** about
vendor semantics; gridflow does not guess them):

1. **Period endpoint and fold.** Does the target timestamp mark the start or end of the
   half-hour settlement period, and how does the file represent the repeated hour on the
   autumn clock-change day (and the missing hour in spring)? The vendor says only "GMT/BST" and
   half-hourly. Settles it: a NESO statement of the period convention and fold treatment.
2. **`Flow_MW` unit.** The dictionary unit is blank. Settles it: a NESO dictionary entry.
3. **Blanks and `99999`.** What blank cells in either value column and the value `99999` in
   `Limit_MW` mean, and whether `-1` in `Flow_MW` is a real flow or a token. Settles it: a NESO
   missing-value definition.
4. **Row grain.** What makes the archive unique when `(Constraint Group, target timestamp)`
   repeats, including 44 key groups that differ in value: a period start or end, a fold
   occurrence, or a version of the forecast? Settles it: a corrected file or a row identifier
   from NESO. Until then the capture stays unloaded with its failure record (ADR-040).

Nothing from this package is published or available to models. The registry hold is per
family, and the family has no rows; the two DOC PDFs are not held (catalogue only).

**Activation (2026-10-10, master `49f7c1a`, PR #104).** The frozen records merged triple-green
(CI pass twice, Sol diff review APPROVE with no findings, VERIFICATION passed at `60109ad`;
RULINGS 634) and were activated with cutoff 2026-10-08, no prior silver (RULINGS 635). The
planned and the observed result for this package is the same: 0 silver rows, from the one
failed capture. No engine change was needed. The record, the failure record and the registry hold were
checked against the committed registry JSON (gridflow `@.planning/phases/v0.22-K-CON/VERIFICATION.md`).

References: gridflow `@.planning/phases/v0.22-K-CON/K-CON-FACTS.md` (sections 4 and 8, g1 to
g5, T01 to T04), `@.planning/phases/v0.22-K-CON/K-CON-SPEC.md` (section 3),
`@.planning/v0.22-RESULTS.md` (section CON), `@.planning/RULINGS.md` (529, 630, 632, 634, 635),
`@src/gridflow/connectors/neso_data_portal/registry/day-ahead-constraint-flows-and-limits.json`,
`@src/gridflow/connectors/neso_data_portal/registry/_reconcile_adjudications.json`,
`@docs/neso_data_portal/eligibility.md`,
`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`,
`@docs/DECISION_LOG/ADR-033-neso-registry-upload-leg.md`,
`@docs/DECISION_LOG/ADR-040-neso-reconcile-adjudication.md`.
Vendor pages: [package](https://www.neso.energy/data-portal/day-ahead-constraint-flows-and-limits),
[resource dictionary](https://www.neso.energy/data-portal/day-ahead-constraint-flows-and-limits/day_ahead_constraint_flows_and_limits).
