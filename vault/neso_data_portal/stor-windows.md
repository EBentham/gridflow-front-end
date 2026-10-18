---
source: "neso_data_portal"
package: "stor-windows"
dataset_key: "stor_windows"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Short Term Operating Reserve (STOR) Windows

This package is NESO's **Short Term Operating Reserve (STOR) Windows** table: a **dated reference calendar**
that maps each delivery date to a season identifier, a working-day or non-working-day flag and two
**committed STOR windows** (a start and an end clock label for each). The vendor dictionary describes the
`Season` column as the "time frame for which the committed STOR windows apply", and the window columns as
the start and end times for "delivery window 1" and "delivery window 2". STOR is one of NESO's reserve
ancillary services. This table carries the schedule of windows, not procured volumes, prices, utilisation or
outturn: nothing in it is a measured quantity. Background on the half-hour grid behind the date anchor:
@../../../20-domain/concepts/settlement-period.md. `TODO: verify` how a committed window relates to the STOR
availability and utilisation payments and to the sibling STOR auction results; this page makes no such claim.

Each row is one **delivery date**. The window number is carried by the wide column names (`Window 1 ...`,
`Window 2 ...`); it is not a row field. In the one capture there are **1,826 rows, one per calendar day from
2021-04-01 to 2026-03-31, with no missing day**, and every cell is populated.

**The silver output is eligible and not held.** Single capture, 1,826 rows (the activation transform log prints no failure lines for this family).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: REG
- Package page: [Short Term Operating Reserve (STOR) Windows](https://www.neso.energy/data-portal/stor-windows)
  (CKAN package name `stor-windows`, id `d7371697-0a03-43a9-a3f3-572d06b25e59`; tags: Ancillary Services,
  Procurement, STOR, Short, Subscribable; package `metadata_modified` 2026-07-27T14:25:54.770607)
- Attribution: Supported by National Energy SO Open Data

## Files by disposition

The package has **one resource**, an uploaded CSV: **1 SILVER, 0 DOC, 0 HOLD**. There are **no DOC files, so
there are no document downloads**. The resource is fetched from its upload URL:

- [STOR Windows](https://api.neso.energy/dataset/d7371697-0a03-43a9-a3f3-572d06b25e59/resource/90d4a1a4-d311-4a22-9138-84cb7ead2599/download/stor_committed_windows.csv)
  · CSV · resource id `90d4a1a4-d311-4a22-9138-84cb7ead2599` · filename `stor_committed_windows.csv` ·
  `url_type` upload · CKAN `last_modified` 2026-07-27T14:25:54.738965 (as recorded in the capture sidecar
  `request_params.ckan_last_modified`). The sidecar declares a content length of 80,748 bytes; the CKAN
  resource declares no hash.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| STOR Windows | CSV | upload | `90d4a1a4-d311-4a22-9138-84cb7ead2599` |

## Families

### `stor_windows`

- Kind: tabular · archetype: REG · refresh: adhoc · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%d/%m/%Y` | no | — | — |
| Season | `season` | string | — | yes | — | — |
| WD_NWD | `wd_nwd` | string | — | yes | — | — |
| Window 1 Start Time | `window_1_start_time` | string | — | yes | — | — |
| Window 1 End Time | `window_1_end_time` | string | — | yes | — | — |
| Window 2 Start Time | `window_2_start_time` | string | — | yes | — | — |
| Window 2 End Time | `window_2_end_time` | string | — | yes | — | — |

- Entity key: `date`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** One row per delivery date, a calendar of which committed windows apply on that day. `date`
is unique in the capture (1,826 distinct dates, 0 duplicate excess) and is the registry key. No vendor
guarantee of a primary key or of revision identity was found, so the key is a measured property of one
capture, not a vendor contract (`TODO: verify` vendor uniqueness and revision identity).

**Vendor dictionary** (CKAN resource field info, snapshot `20261008T114228Z`, as read in the batch research,
@.planning/phases/v0.22-K-AS-2/K-AS-2-FACTS.md in the gridflow checkout, and the vendor's
[STOR Windows resource page](https://www.neso.energy/data-portal/stor-windows/stor_windows)):

| Column | Vendor description | Vendor unit |
|---|---|---|
| `Date` | "Delivery date" | none |
| `Season` | "Time frame for which the committed STOR windows apply"; vendor type `number`, example `18.1` | none |
| `WD_NWD` | "Working Day/ Non Working Day" | none |
| `Window 1 Start Time` | "Start time for delivery window 1" | none |
| `Window 1 End Time` | "End time for delivery window 1" | none |
| `Window 2 Start Time` | "Start time for delivery window 2" | none |
| `Window 2 End Time` | "End time for delivery window 2" | none |

**Units.** The vendor dictionary gives **no unit for any column** (the unit field is empty for all seven), and
none is inferred from a column name. `Season` is a **categorical schedule identifier, not a physical
measurement**: the vendor types it as a number, but gridflow keeps it as a **string** (`15.1` is a label, not
a decimal; arithmetic on it is meaningless). The four window columns are clock labels, not durations.

**Sentinels and lexical rules.** The body is read with strict UTF-8 and no null-token map. Across the
complete body no cell is blank (0 nulls in every column of the silver output), and no `-1`, `NA`, `N/A`, `NULL`
or `NaN` token, numeric thousands separator, percent suffix, padded body cell or zero run was observed
(FACTS g5; the STOR capture is listed there as having no blank cells). A blank cell would become null, never a
default, and the strings are preserved byte for byte. The body carries a leading **UTF-8 BOM**; the existing
CSV reader handles it and the first header is read as `Date`. The reader-equivalence check passed (FACTS C04,
C06).

**Clocks.** Two clocks, stated separately:

- **Vintage.** The record's vintage is `ckan_last_modified`: `available_at` equals `published_at`, which is the
  CKAN `last_modified` of the captured upload (2026-07-27T14:25:54.738965, read as UTC, ADR-030/ADR-035).
  Every row carries that same instant. The body has **no issue or production column** (`issue: none`), so there
  is no per-row publication time: the vintage is the file's last-modified, and the capture was taken about
  73 days after NESO last modified the file.
- **Event time.** `date_sp1(date)`: `timestamp_utc` and `event_time` are the start of settlement period 1 of
  `date`, that is Europe/London midnight of the delivery date converted to UTC (silver: `date` 2021-04-01
  gives 2021-03-31T23:00:00Z; 2025-03-30, before the clock change, gives 2025-03-30T00:00:00Z; 2025-03-31
  gives 2025-03-30T23:00:00Z). This is a **date-label anchor only**: it is the start of the delivery date,
  **not** the start of window 1 or window 2. The four window columns stay **raw `HH:MM` strings**; the engine
  does not compose a date plus clock label into an instant, and no window start or end timestamp is derived.
  The date format is `%d/%m/%Y` (day first).

**Window clock (not established).** NESO's STOR operational guidance establishes a local operational-day clock
and discusses the published firm windows in that context
([NESO STOR system guidance, availability section](https://www.neso.energy/document/209016/download)), but
applying this to the committed-window labels in this CSV is a contextual inference; the resource dictionary
does not state the clock. `TODO: verify` that the `HH:MM` labels are local (Europe/London) clock times.

**Whole-capture semantics.** `latest` is `whole_capture`: the table is a dated calendar and one capture is the
whole view. Only one capture exists, so amendment-in-place and dropped-date behaviour are not measured
(`TODO: verify`). The registry record allows an empty capture; the one capture is not empty.

**Coverage and content (single capture).**

| Item | Value |
|---|---|
| Date range | 2021-04-01 to 2026-03-31, 1,826 distinct dates, 0 missing calendar days |
| `WD_NWD` | `WD` 1,521 rows, `NWD` 305 rows; vendor flags preserved, not recomputed from weekdays |
| `Season` | 30 distinct tokens: `15.1` to `15.6`, `16.1` to `16.6`, `17.1` to `17.6`, `18.1` to `18.6`, `19.1` to `19.6` |
| Midnight-crossing window | none (rows with end at or before start: 0 for both windows) |

Observed window forms (start–end), with the number of dates carrying each in the capture:

| Window | Observed start–end pairs (dates) |
|---|---|
| Window 1 | `06:00–13:00` (908); `06:30–14:00` (468); `10:30–13:30` (174); `06:30–13:00` (145); `10:30–13:00` (69); `10:00–14:00` (32); `10:30–12:30` (30) |
| Window 2 | `16:00–22:00` (613); `16:00–20:30` (373); `16:30–20:30` (299); `17:30–22:00` (174); `17:00–22:00` (120); `19:00–22:00` (116); `16:00–19:30` (82); `16:30–20:00` (49) |

These are one capture's observations, not vendor limits. The seasons are schedule identifiers; the mapping of
season token to calendar span and to window form is not documented in the dictionary (`TODO: verify`).

## Bronze capture

One capture exists (2026-10-08), so there is no capture-pair history. The measured bronze body:

| Item | Value |
|---|---|
| Bronze file | `C:/gridflow-data/bronze/neso_data_portal/stor_windows/2026/10/08/raw_20261008T112743Z_90d4a1a4-d311-4a22-9138-84cb7ead2599_6e5c1515.csv` |
| Format | CSV, strict UTF-8 with BOM, header as the vendor column list above |
| Size and rows | 80,748 bytes (matches `declared_content_length`) · 1,826 data rows |
| SHA-256 | `6e5c151571e001e29b29d581e3f0dd7d464c2058b35e7483ec6b6fd09d82b73a` (matches the sidecar) |
| Sidecar `fetched_at` | `2026-10-08T11:27:43.091353+00:00` |
| Sidecar `written_at` | `2026-10-08T11:27:43.094353+00:00` |
| HTTP | 200, `text/csv`, one page |
| Empty-capture marker | false |

Silver lives at `C:/gridflow-data/silver/neso_data_portal/stor_windows/year=2026/month=10/` (partitioned by
capture month), one Parquet file for this capture with **1,826 rows**. Columns: the seven data columns above,
then the system columns `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`,
`event_time`, `available_at`, `source_run_id`, `dataset_version` (`1+e1`).

Activation (RULINGS 731, 2026-10-13): the transform for `--start/--end 2026-10-08`, with no prior silver, gave
1,826 rows for this family, equal to the plan (batch total 241,160 rows over 11 families; the transform log prints no
failure lines, and the spec plans none). The reconcile run over all families (cutoff 2026-10-12) exited 0 with 170 families, 0 gaps, 47
adjudicated and 0 stale; none of the adjudications concerns this package. Merge: PR #113, `fccbdeb`
(RULINGS 730).

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The vendor gives no schedule for the committed-window calendar. The one capture ends on 2026-03-31 although
the file was last modified on 2026-07-27, so how far ahead of the delivery date, or how often, windows are
published is not measured (`TODO: verify`). No rate limit or pagination for the upload download was found in
the documentation read: `TODO: verify`.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow
outputs derived from this package carry the attribution line above.

## Holds

- none

The `stor_windows` output is not held. Open items that do not hold the output but limit what can be claimed:

- `TODO: verify` **STOR-COMMITTED-WINDOW-ROLLOVER / CLOSURE**: a committed-window CSV example crossing midnight,
  or resource-specific vendor instructions on rollover and endpoint closure. No window in the capture crosses
  midnight; the literal times are retained and nothing parses them, so no parsing or key blocker follows.
- `TODO: verify` **STOR-CSV-CLOCK**: the service-level local-clock evidence is contextual, not an explicit clock
  declaration on this CSV. Consequence: no datetime composition from the window labels.
- `TODO: verify` vendor uniqueness and revision identity for `date`.
- `TODO: verify` amendment-in-place and dropped-date behaviour between captures.

## Gotchas

- **The temporal anchor is not a window time.** `event_time` is local midnight of the delivery date. Joining on
  it as if it were a window start is wrong. Use `date` plus the raw window strings, and apply a clock only
  once the window clock above is established.
- **`season` is a string, not a number.** The vendor types `Season` as a number (example `18.1`); gridflow
  keeps the label (`15.1` to `19.6`). Do not parse, round or compare it as a decimal.
- **`WD_NWD` is the vendor's flag.** Do not recompute working-day status from the weekday; bank holidays and
  other non-working days are whatever NESO flagged. Values observed: `WD`, `NWD`.
- **Dictionary examples are not data.** The dictionary gives one example per window column: `18:00` (Window 1
  Start), `19:00` (Window 1 End), `20:00` (Window 2 Start) and `21:00` (Window 2 End). Each example does not
  occur in its own column of the captured body (0 rows each). The same strings do occur in other columns:
  `19:00` as Window 2 Start in 116 rows (the `19:00–22:00` pair) and `20:00` as Window 2 End in 49 rows (the
  `16:30–20:00` pair). The observed forms are the tables above.
- **Wide windows, two only.** Window 1 and window 2 are separate columns of one row. A third window, or a
  day without a window, cannot be represented and does not occur in the capture.
- **DST days.** The anchor is Europe/London midnight, so on DST dates the UTC instant is 23:00 the previous day
  (British Summer Time) or 00:00 (Greenwich Mean Time); the date itself is unaffected. Window lengths on a
  clock-change day are not interpreted (`TODO: verify` if the windows are ever composed).
- **Point-in-time use.** Select with `available_at <= :as_of`. `available_at` is the file's CKAN last-modified,
  so a later capture of an amended calendar carries a later vintage; do not backdate it. Dates in the capture
  precede the vintage (the calendar ends 2026-03-31, the vintage is 2026-07-27), so this is a record of
  committed windows already past at the vintage, not a forward look.
- **Day-first dates.** `Date` is `dd/mm/yyyy` (`%d/%m/%Y`).
- **No `run_type`.** The package has no settlement-run dimension; none is fabricated.

## Modelling notes

Use the table as a lookup of the committed STOR windows in force on a delivery date, joined on `date` (not on
`event_time`), taking the whole capture as one point-in-time vintage. Because the capture ends 2026-03-31, a
later window calendar needs a later capture; ingest cadence is `adhoc`, so any capture schedule would be a
later scope decision (`TODO`). Do not turn the window strings into timestamps until the window clock and the
rollover rule are settled (see Holds). See @../../../20-domain/concepts/settlement-period.md for the half-hour
grid behind the `date_sp1` anchor.

## Links

- Package page: [Short Term Operating Reserve (STOR) Windows](https://www.neso.energy/data-portal/stor-windows)
- Resource page: [STOR Windows](https://www.neso.energy/data-portal/stor-windows/stor_windows)
- Upload: [stor_committed_windows.csv](https://api.neso.energy/dataset/d7371697-0a03-43a9-a3f3-572d06b25e59/resource/90d4a1a4-d311-4a22-9138-84cb7ead2599/download/stor_committed_windows.csv)
- STOR system guidance cited by the batch research: [document 209016](https://www.neso.energy/document/209016/download)
- Licence: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence)
- Registry record: `src/gridflow/connectors/neso_data_portal/registry/stor-windows.json` (gridflow checkout)
- Eligibility report: `docs/neso_data_portal/eligibility.md` (gridflow checkout)
- Batch evidence: @.planning/phases/v0.22-K-AS-2/K-AS-2-FACTS.md, @.planning/phases/v0.22-K-AS-2/K-AS-2-SPEC.md and @.planning/v0.22-RESULTS.md (gridflow checkout)
- Related: @./ancillary-services-important-industry-notifications.md (the STOR notification family, `as_industry_notifications_stor_important`)
- Domain: @../../../20-domain/concepts/settlement-period.md
