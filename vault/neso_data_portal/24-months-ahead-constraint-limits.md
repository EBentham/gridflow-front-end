---
source: "neso_data_portal"
package: "24-months-ahead-constraint-limits"
dataset_key: "constraint_limits_24m"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-23
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: NESO does not map its week numbers to dates, nor say when each week was forecast.
  title: 24-month constraint limits
  summary: >-
    NESO's forecast capability, in MW, of twelve main transmission boundaries, week by week for
    the next 24 months.
  facts:
    vendor: "NESO Data Portal, package `24-months-ahead-constraint-limits`: one CSV file, two diagrams"
    cadence: "Monthly, as NESO lists it; each upload replaces the file"
    grain: "Each row: a year and week number, with twelve boundary columns in MW"
  landscape: market
  what_it_is: >-
    A boundary splits the transmission network in two. Each column is what NESO's dictionary
    calls the boundary capability, in MW, for one boundary code such as SCOTEX or ESTEX. Rows carry
    only a year and a week number, which NESO numbers 1 to 52, and no dates. Two NESO diagrams
    locate the boundaries.
  how_used:
    - The capability side of a boundary, set against forecast flows across it
    - How a boundary's capability is expected to change, week by week
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then each file whole unless its `last_modified` is
      unchanged. The CSV's name carries the upload month; the two diagrams stay in bronze.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=24-months-ahead-constraint-limits"
      - "GET https://api.neso.energy/dataset/d515b4a9-60a1-489c-a126-004efc04f121/resource/3c359e33-3dac-4bdd-87d1-efbf4cbc2f07/download/24-months-ahead-constraint-limit_oct26.csv"
      - "GET https://api.neso.energy/dataset/d515b4a9-60a1-489c-a126-004efc04f121/resource/a9bafbd9-b393-4a5b-bc6f-09d6cdeea583/download/ew_network_constraint_diagram.pdf"
      - "GET https://api.neso.energy/dataset/d515b4a9-60a1-489c-a126-004efc04f121/resource/bf4e1174-9aa7-4c0d-b444-5d22785053eb/download/scotland_network_constraint_diagram.pdf"
    commands:
      - {run: gridflow ingest neso_data_portal constraint_limits_24m --last 24h, comment: whole file to bronze}
      - {run: gridflow transform neso_data_portal constraint_limits_24m --last 24h, comment: "the capture's date to silver"}
      - {run: gridflow ingest neso_data_portal constraint_limits_24m_files --last 24h, comment: the two network diagrams}
  related:
    - {dataset: neso_data_portal/day-ahead-constraint-flows-and-limits, note: "Day-ahead limits and forecast flows; ten boundary codes match exactly"}
    - {dataset: neso_data_portal/24-months-ahead-constraint-cost-forecast, note: "NESO's monthly constraint cost forecast over a similar two years"}
    - {dataset: neso_data_portal/thermal-constraint-costs, note: "Outturn thermal constraint costs; SCOTEX and ESTEX appear in both"}
    - {dataset: neso_data_portal/operational-transparency-forum-network-congestion-data, note: "Weekly forecast and actual boundary limits, under different codes"}
---

# 24 Months Ahead Constraint Limits

NESO's long-horizon forecast of **constraint limits for the main boundaries of the GB
transmission system**, one row per week, published on the Open Data Portal as a single CSV. The
vendor describes it as constraint limits in megawatts for the main boundaries "on weekly basis for
24 months ahead", refreshed monthly. It is a **weekly** table refreshed monthly, not a monthly
table (gridflow `@.planning/phases/v0.22-K-CON/K-CON-FACTS.md` g1 / CON-7). Each row is a
(year, week number) label plus twelve boundary columns. The vendor's dictionary defines each
boundary column as the "boundary capability" for that boundary code, in MW. A boundary is a
cut across the transmission network that can carry only so much power. When forecast flow across
it exceeds its capability, NESO must constrain generation or demand, which is what drives the
constraint costs in the same publisher group. A model of constraint risk or of forward
constraint cost would use this table as the capability side of the boundary balance, alongside
the flow forecasts in @day-ahead-constraint-flows-and-limits.md and the realised costs in
@thermal-constraint-costs.md. **The silver output is held** (unit E-SEM): the vendor does not say
how its year and week labels map to calendar dates, and it does not say whether each monthly
upload was issued before every week it covers. Until that is answered the table is useful for
inspection, not for point-in-time use. See Holds.

- Publisher group: Constraint management
- Registry group: constraint-management · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| 24 Months ahead constraint limits | CSV | upload | `3c359e33-3dac-4bdd-87d1-efbf4cbc2f07` |

- 24 Months ahead constraint limits → `constraint_limits_24m`.
  Download as captured: [24-months-ahead-constraint-limit_sept26.csv](https://api.neso.energy/dataset/d515b4a9-60a1-489c-a126-004efc04f121/resource/3c359e33-3dac-4bdd-87d1-efbf4cbc2f07/download/24-months-ahead-constraint-limit_sept26.csv).
  The file name carries a month token (`sept26`) and changes with each monthly upload, so the
  stable handle is the resource id, not the URL. CKAN datastore active. The month token is not a
  documented issue instant (FACTS g2). The vendor describes the file as constraint limits for the
  main boundaries on a weekly basis, updated monthly.
  Captured: `raw_20261008T091545Z_3c359e33-3dac-4bdd-87d1-efbf4cbc2f07_3eef5064.csv`,
  7,406 bytes, 105 data rows, one header epoch, CKAN `last_modified`
  `2026-09-10T09:48:47.500911`, `url_type: upload`.
  Captured again on 2026-10-16 as
  [24-months-ahead-constraint-limit_oct26.csv](https://api.neso.energy/dataset/d515b4a9-60a1-489c-a126-004efc04f121/resource/3c359e33-3dac-4bdd-87d1-efbf4cbc2f07/download/24-months-ahead-constraint-limit_oct26.csv):
  `raw_20261016T192121Z_3c359e33-3dac-4bdd-87d1-efbf4cbc2f07_720763a1.csv`, 7,409 bytes, 105 data
  rows, the same header, CKAN `last_modified` `2026-10-09T09:29:34.943764` (bronze sidecar).

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| E&W network constraint diagram | PDF | upload | `a9bafbd9-b393-4a5b-bc6f-09d6cdeea583` |
| Scotland network constraint diagram | PDF | upload | `bf4e1174-9aa7-4c0d-b444-5d22785053eb` |

- E&W network constraint diagram: [ew_network_constraint_diagram.pdf](https://api.neso.energy/dataset/d515b4a9-60a1-489c-a126-004efc04f121/resource/a9bafbd9-b393-4a5b-bc6f-09d6cdeea583/download/ew_network_constraint_diagram.pdf)
  (CKAN `last_modified` 2025-06-16T16:01:22.793115). Captured:
  `raw_20261008T091551Z_a9bafbd9-b393-4a5b-bc6f-09d6cdeea583_3eb6baa9.pdf`, 408,523 bytes.
- Scotland network constraint diagram: [scotland_network_constraint_diagram.pdf](https://api.neso.energy/dataset/d515b4a9-60a1-489c-a126-004efc04f121/resource/bf4e1174-9aa7-4c0d-b444-5d22785053eb/download/scotland_network_constraint_diagram.pdf)
  (CKAN `last_modified` 2025-06-16T16:15:38.707866). Captured:
  `raw_20261008T091549Z_bf4e1174-9aa7-4c0d-b444-5d22785053eb_0d7e4010.pdf`, 236,575 bytes.

Both diagrams are catalogue only (family `constraint_limits_24m_files`): no silver output. They
locate the named boundaries on the network and are reference evidence for the boundary codes
below. They are **not** a date calendar for the week labels (FACTS PDF disposition). All bytes
above are filesystem measurements from the bronze inventory (FACTS §1).

## Families

### `constraint_limits_24m`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| YEAR | `year_vendor` | int64 | — | no | — | — |
| Week No | `week_no` | int64 | — | no | — | — |
| DRESHEX1 | `dreshex1` | int64 | — | yes | — | MW |
| ESTEX | `estex` | int64 | — | yes | — | MW |
| FLOWSTH | `flowsth` | int64 | — | yes | — | MW |
| GM_SNOW5A | `gm_snow5a` | int64 | — | yes | — | MW |
| HARSPNBLY | `harspnbly` | int64 | — | yes | — | MW |
| NKILGRMO | `nkilgrmo` | int64 | — | yes | — | MW |
| SCOTEX | `scotex` | int64 | — | yes | — | MW |
| SEIMPPR2 | `seimppr2` | int64 | — | yes | — | MW |
| SSE_GRM | `sse_grm` | int64 | — | yes | — | MW |
| SSEN_S | `ssen_s` | int64 | — | yes | — | MW |
| SSE_SP2 | `sse_sp2` | int64 | — | yes | — | MW |
| SSHARN3 | `ssharn3` | int64 | — | yes | — | MW |

- Entity key: `year_vendor`, `week_no`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM).** This family's silver output exists but is not eligible for publication or
point-in-time use. This page gives schema, row counts and structural counts only. It gives no
data values, samples or ranges. See Holds.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file. For the 2026-10-08 capture that is
   `2026-09-10T09:48:47.500911`, and for the 2026-10-16 capture `2026-10-09T09:29:34.943764`;
   CKAN emits both without an offset. gridflow reads them as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). The 105 silver rows of
   each capture share its one vintage (checked on both silver files, 2026-10-23). The file has **no issue
   column** and the record's issue recipe is `none`: no row carries its own issue time. The
   vintage says when the file last changed. It does **not** say that every week in the file
   was forecast on that date.
2. **Event time (`none`).** The record has no temporal recipe, so `timestamp_utc` = `event_time`
   = the **capture time** (`capture_written_at`), not any week's start. Checked on every silver
   row on 2026-10-10: `timestamp_utc` equals `capture_written_at` and `event_time`, and
   `available_at` equals `published_at`. The target period is carried only by the raw
   `year_vendor` and `week_no` columns. No date is derived from them, because the week
   calendar is not established (see below). Do not read `timestamp_utc` on this family as a
   target time.

**Key and coverage (FACTS §2).** The measured key `(year_vendor, week_no)` is unique in each
capture: 105 rows, 105 distinct keys, zero duplicate excess (both captures). `TODO: verify` the vendor's
identity guarantee. The label coverage spans calendar years 2026 to 2028, consistent with the
24-month horizon the vendor names. The vendor describes `YEAR` as "Time series - Year" and `Week
No` as "the week number (1-52) for which the limit is applicable" (field-info). Neither column
has a physical unit. They are calendar identifiers. `year_vendor` is named so because `year` is
a reserved silver name (Hive partition column) (VERIFICATION deviation 1).

**Week calendar (unresolved).** `TODO: verify` the week-numbering convention (the vendor does not
say ISO), the week start and end dates, how the year boundary is handled and the timezone. The
labels indicate a forward horizon, but labels alone do not prove the target instants, so the
strict forward-target test (RULINGS 529) cannot be completed. Do not manufacture a month start,
and do not apply an ISO-week conversion.

**Boundary columns (vendor dictionary).** The twelve value columns are
`DRESHEX1, ESTEX, FLOWSTH, GM_SNOW5A, HARSPNBLY, NKILGRMO, SCOTEX, SEIMPPR2, SSE_GRM, SSEN_S,
SSE_SP2, SSHARN3`. The field-info describes each as "Boundary capability for <code>" with unit
**MW** (field-info `constraint_limits_24m.json:43` to `:175`). Whether a value is a firm
capability, a transfer limit net of outages, or something else is not defined beyond that
phrase. `TODO: verify` the vendor's definition of "boundary capability".

**Header rename (vendor notice).** The package description announces that four column ids change
on 9 September 2026: `GM+ SNOW5A` becomes `GM_SNOW5A`, `SSE+GRM` becomes `SSE_GRM`, `SSEN-S`
becomes `SSEN_S` and `SSE-SP2` becomes `SSE_SP2`. The captured file (vintage 2026-09-10)
already carries the new spellings, and the record's single header epoch uses them. The field-info
text still reads "Boundary capability for GM+ SNOW5A", so the dictionary descriptions lag the
renamed headers. A capture carrying the pre-rename spellings is not a declared epoch of this
record. `TODO: verify` whether the vendor will restate older uploads under the new ids. If an
older-header capture appears, it needs its own declared epoch. It must not be relabelled.

**Boundary identifiers (FACTS §8, CON-1).** Codes are stored exactly as the vendor writes them,
with no case change, punctuation replacement or aliasing. Exact intersections with the other
constraint tables, on raw strings:

| Pair | Size | Exact intersection |
|---|---:|---|
| This table / day-ahead flows and limits | 10 | `DRESHEX1, ESTEX, FLOWSTH, GM_SNOW5A, HARSPNBLY, NKILGRMO, SCOTEX, SSEN_S, SSE_SP2, SSHARN3` |
| This table / OTF network congestion | 0 | none |
| This table / thermal constraint costs | 2 | `ESTEX, SCOTEX` |

Set sizes: 12 here, 31 day-ahead, 11 OTF, 6 thermal. The vendor's OTF documentation presents
aliases such as `B6 (SCOTEX)`, `B7 (SSHARN)`, `FLOWSTH (B9)`, `LE1 (SEIMP)` and `B15 (ESTEX)`.
These are reference relationships, not storage normalisation rules. Do not merge near-identical
codes across tables: `SSE_GRM` / `SSE_GRMO`, `SEIMPPR2` / `SEIMPPR21` / `SEIMPPR23` /
`SEIMPPR33` / `SEIMP`, `SSHARN3` / `SSHARN` / `SSHARN7` / `SHARN`, `SSE_SP2` / `SSE_SP` /
`SSE-SP`, `DRESHEX1` / `DRESHEX`. `TODO: verify` a vendor crosswalk, with applicability dates,
for the boundary codes whose membership is not defined. See also
@operational-transparency-forum-network-congestion-data.md.

**Units (vendor dictionary only).** The twelve boundary columns are **MW**, each declared in the
vendor dictionary (field-info, lines above). `year_vendor` and `week_no` carry no physical
unit (FACTS T01/T02). No unit was inferred from a column name.

**Sentinels and missing values (FACTS g5).** The record declares no null token. In the one
capture, no blank, `-1`, `NA`, `N/A`, numeric zero or `99999` was observed in any column. That
establishes absence in this capture, not a vendor sentinel policy. The boundary columns are
nullable in silver; any future blank stays a null, and no value is converted. `TODO: verify`
the vendor's missing-value convention.

**Activation (2026-10-10, master `49f7c1a`, PR #104).** Transformed at cutoff 2026-10-08 (one
capture): **105 silver rows**, equal to the planned count. No prior silver existed, so nothing
was overwritten. The silver file is `year=2026/month=10/…parquet` under
`C:/gridflow-data/silver/neso_data_portal/constraint_limits_24m/`. Reconcile
`--all --cutoff 2026-10-08` exited 0 with 105 families, 0 gaps (gridflow
`@.planning/v0.22-RESULTS.md` §CON; RULINGS 630, 632, 634, 635). The first daily refresh
(2026-10-16) wrote a second silver file (105 rows) from the October upload (checked 2026-10-23).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1, epoch 1).

### `constraint_limits_24m_files`

- Kind: files · archetype: FC · refresh: monthly · empty allowed: no
- files: catalogue only

This family captures the two network constraint diagrams (see DOC above). It has no silver
output and no clocks beyond each file's CKAN `last_modified`. It has no record.

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Monthly
- Monthly: captured once per refresh run. The vendor updates the file monthly and gridflow keeps
  only the newest capture whole (`latest: whole_capture`).

The captured file's CKAN `last_modified` is 2026-09-10, about four weeks before the 2026-10-08
capture, which is consistent with a monthly cadence. A later monthly upload replaces the previous
one in the vendor's file, and gridflow's `whole_capture` selection treats the newest capture as
the whole table. Captures: two, on 2026-10-08 (`sept26`, vintage 2026-09-10) and 2026-10-16
(`oct26`, vintage 2026-10-09).

- **A monthly upload revises, not only extends.** Compared row by row on bronze (2026-10-23): the
  label window moved four weeks, from 2026 week 40 to 2028 week 40 in `sept26` to 2026 week 44
  to 2028 week 44 in `oct26` (four weeks dropped, four added). Of the 101 weeks in both, 30 rows
  changed in at least one boundary column (102 cells). No values are stated while the hold
  stands. Whether every upload revises in this way is `TODO: verify` over more captures.
- `TODO: verify` whether the vendor publishes the file at a fixed point in the month.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `constraint_limits_24m`: held: TODO: what week-numbering convention, week start/end, year-boundary handling and timezone do YEAR/Week No denote, and is each monthly upload a forecast issued before every target week? NESO's dictionary states neither. (unit E-SEM)

The hold is a seat ruling (RULINGS 632, PROXY-SOURCED, ratified at milestone close). Two things
are missing, and either one alone would block point-in-time use:

1. **The week calendar.** The table gives a year and a week number and nothing else. There is
   no date column, and the vendor's dictionary does not map the pair to dates, so the target
   period of each row is unknown. The record therefore has temporal `none` and keeps the raw
   `year_vendor` and `week_no` columns.
2. **The issue clock.** There is no issue or publication column. The CKAN vintage is only the
   date the file last changed. Without the calendar, gridflow cannot show that every target
   week lay after the vintage, so the CKAN vintage cannot be accepted as a conservative proxy
   for the missing issue time. This is the same forward-target test applied to the other
   forecast families (RULINGS 529).

Unit E-SEM must answer both questions with NESO. Until then the silver output stays out of
published artifacts and out of any point-in-time query. Row counts and the schema are fine to
state, and this page states no values. This family is the only CSV in its package.
