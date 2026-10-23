# OBP non-BM physical notifications: writer report (2026-10-23)

Page `obp-non-bm-physical-notifications`, one table, lead `obp_physical_notifications`. The manifest's lead and member are
right.

| Gate | Result |
|---|---|
| `gridflow-build --only neso_data_portal/obp_physical_notifications` | ok. The vault-wide "22 Known issues lines dropped" warning predates this work. The last runs also report "1 error(s) on pages not rendered by --only": that error is on another page (most likely the availability page another writer is editing now), not this one |
| Detector | `[]` |
| Canonical note vs mirror | `cmp` clean; CRLF on all 257 lines; vault diff 134 insertions, 9 deletions |
| Rendered page | 0 em or en dashes, arrows or middle dots; none of live, now, yet, soon, planned, shipped, real-time, locally, held, ledger, TODO, "our ", "since 20", "% of". The only "rows" hits are the template heading and the help card |
| Screenshots | `.planning\neso-dp\ancillary-b\obp-physical-notifications-shots\`: 1440, 1024, 768 (slices plus full page) and 390 (through a 390 px iframe). Nothing clipped or overlapping. Light only: the site has no dark theme |
| Server | my 9985 server is stopped; 9670 not touched |

Artefacts (no staged spec or authored override existed):
- `site\hifi\data\series\neso_data_portal\obp_physical_notifications.json`: `spec_origin: vault`, 3 series x 48 half-hours, 144 rows used, 144 duplicates (the older capture's copies) dropped by the dedup.
- `site\hifi\data\samples\neso_data_portal\obp_physical_notifications.json`: `gridflow-sample`, 8 rows, 14 columns, all from the 2026-10-16 capture.
- `site\hifi\data\notebooks\neso_data_portal\obp_physical_notifications.json` and `-6.png`: `run_notebooks.py`, 6 cells, no errors.

## The four questions

1. **What one row is, and how it relates to the instructions.** One row is one window of one unit's PN: `Unit ID`,
   `Time From` with `Level From`, `Time To` with `Level To` (NESO dictionary: "Window Start Datetime", "PN at Gate
   Closure for window start time in MW", and the same for the end). NESO's datastore copy declares the key
   (`datastore_unique_keys: ["Unit ID", "Time From"]`); gridflow's entity key is the same. Windows run 60 to 1,800 s; in
   the 2026-10-16 capture none crosses a `:00`/`:30` boundary and none overlaps another of the same unit (body only, not
   on the page). On the instructions, NESO's own words only: the PN package notes point to the instructions and
   availability packages as "Additional transparency data for Non-BM Reserve services mastered by OBP", and the
   instructions dictionary gives `Target MW` as "Power from PN in absolute values". The page says exactly that ("NESO
   gives target MW as power from the PN", "whose target MW NESO describes as power from PN"). The rows: 21 of the 24
   instructed units have PN rows (the three `RDP` units do not), and all 60 availability units do. That stays in the
   note body. NESO's PN `Unit ID` description is word for word the instructions' one, which is why it says "instruction".
2. **Time columns.** `Time From` and `Time To` are `YYYY-MM-DDTHH:MM:SS` with no zone marker (bronze cells such as
   `2025-10-08T16:00:00`); NESO's unit is "UTC", its examples end in `Z`. The rows rule out UK local time on one day:
   on 29 March 2026 (UK clocks skipped 01:00 to 02:00) five units carry contiguous windows starting `01:00:00` and
   `01:30:00`; notebook cell 3 prints those 10 rows. 26 October 2025 (clocks back) has three units, each with 48 whole
   half-hours: fits UTC, cannot exclude local time alone. One more fitting observation (body only): both captures end
   about 1 h 29 min after `last_modified`. The page says "Times are UTC, NESO says: the text has no zone marker but
   holds 01:00 on 29 March 2026, which UK clocks skipped." The workbench returns `time_from`, `time_to` and
   `timestamp_utc` as `datetime64[us, Europe/London]` (checked: first row `2026-09-21 01:00:00+01:00` for a 21
   September query); the lead says so and cell one converts to UTC.
3. **MW and signs (NESO dictionary only).** Both levels are MW, "PN at Gate Closure". No sign convention is stated;
   the page says "no sign stated" and "NESO states no sign". Levels run -49.9 to 50 in both captures. Body adds: 37 of
   101 units declare both signs, 51 declare zero on every row (2026-10-16 capture).
4. **Duplicates, overlap, truncation.** Two captures: 2026-10-08 (495,086 rows, `last_modified` 11:01:24) and
   2026-10-16 (523,890 rows, `last_modified` 20:31:22). Bronze line counts match (header plus rows; both end in a
   newline). 0 duplicate keys in each. Compared on the key: all 495,086 earlier rows reappear with the same `time_to`
   and levels, none is missing, and the 28,804 new rows all start at or after `2026-10-08T12:30:00`, the earlier file's
   last end. So it is a pure append, no truncation; `_latest` (newest complete capture) is right. Both files start at
   `2025-10-08T16:00:00`, which refutes the note's "rolling window of about 12 months" over that interval. The chart
   and the sample both read every silver file, so both carry `dedup: {on: [unit_id, time_from], order_by:
   published_at}`; this keeps the newer capture's copy, matching `_latest`.

## Chart choice

A line chart of `level_from` per half-hour start for three units (`GSET-07`, `GSET-04`, `GSET-02`), 21 September 2026
UTC, `mean` over a 30-minute bucket. On that day every window of these three units is exactly 1,800 s with
`level_from == level_to` (checked), so each bucket holds one row and the mean is that row's level; the caption says
"Every window here is a whole half-hour with equal start and end levels; the sloped joins are drawing only". It shows
the signed values and the flat half-hour blocks. A cross-unit sum was rejected: the filter grammar cannot keep one
window per half-hour, so units with minute windows would be double counted. The notebook plot draws each window from its
start level to its end level for `GSET-07` and `AFFR-1`, which shows the sub-half-hour shape the chart cannot.

## Evidence

| Claim (page field) | Evidence |
|---|---|
| summary, `what_it_is`: PN declared by providers to OBP for non-BM units | package notes "NESO publishes Non-BM Physical Notifications (PN) data declared by Service Providers to Open Balancing Platform (OBP) system" (snapshot `20261006T195819Z`) |
| "NESO publishes those OBP accepted and validated by gate closure" | resource description: "once declarations have been accepted and validated by OBP system by gate closure" |
| "Each row is one window of it, with levels at both ends" | field info `20261008T114228Z/obp_physical_notifications.json`: Window Start/End, Level From/To |
| "Times are UTC, NESO says ... holds 01:00 on 29 March 2026" | field info unit "UTC"; registry `zone: UTC`; silver: 5 units, 10 windows starting 01:00 and 01:30 on 2026-03-29, contiguous (no gap found 2026-03-28 12:00 to 03-30 12:00 except 06:30 to 07:00); notebook cell 3 output |
| facts.vendor "one CSV, republished under a new file name" | registry one resource, `url_type: upload`; three file names: `pn_20261006_44_nbm.csv` (snapshot), `pn_20261008_27_nbm.csv`, `pn_20261016_46_nbm.csv` (sidecars' `resource_filename`) |
| facts.cadence | extras "Update frequency: Ad hoc"; notes "continuously published throughout the day" |
| facts.grain, key | dictionary; registry `entity_key: [unit_id, time_from]`; CKAN `datastore_unique_keys` |
| how_used 3 "whose target MW NESO describes as power from PN" | instructions field info, `Target MW`: "Power from PN in absolute values." |
| chart caption | spec: filter `unit_id in [...]`, dedup, `aggregation: mean`, `time_bucket: 30m`, window 2026-09-21; silver: those three units on that day have 48 rows each, all 1,800 s, `level_from == level_to` |
| key notes and alt | committed series: gset07 -17.032 at 03:30, 04:00, 04:30, 14:00 to 15:30 (-15.823 at 13:30), 15.435 at 06:30, 15.087 at 16:30, 15.973 at 18:00, 12.497 at 20:00; gset04 -6 at 03:30 to 04:30 and 13:30 to 15:30, 6 at 06:30, 16:30, 18:30; gset02 -3 at 03:30, 04:00, 13:30, 14:00, 3 at 16:30 |
| raw requests | `package_show` (CKAN action, as the approved upload pages show); the upload URL is the 2026-10-16 sidecar's `request_url` |
| raw note "downloaded whole unless its `last_modified` is unchanged" | `client.py` `iter_members` 1752 to 1767 |
| commands `--last 24h`, "window must end recently" | `client.py:1543` (`_HISTORICAL_WINDOW_TOLERANCE` 48 h, line 130); same form as the approved upload pages |
| frame caption and rows | sample: `AFFR-1`, 09:00 to 11:30 UTC, 2026-09-21, eight contiguous windows (1,800, 60, 1,680, 60, 1,800, 1,800, 60, 1,740 s), levels 0 and -2 |
| field `time_to` "NESO does not say whether the end belongs to it" | dictionary states only "Window End Time" |
| field `level_to` "path between unstated" | dictionary states only the two levels |
| field `data` | dictionary "Fixed value \"PN\"" |
| field `timestamp_utc` | registry temporal `utc_instant` on `time_from`; silver `timestamp_utc == time_from` on all rows of both files |
| field `published_at` "read as UTC; one per capture" | registry `vintage: ckan_last_modified`; one value per file, `2026-10-16 20:31:22.674649 UTC` for sidecar `2026-10-16T20:31:22.674649` |
| notebook lead | manifest: relation `silver_neso_data_portal_obp_physical_notifications_latest`, `designated_date_col='timestamp_utc'`, TIMESTAMPTZ; `_get_method_registry.py` `_date_range_predicate` (half-open UTC, end date included); lineage columns dropped (checked: 10 columns returned); `Europe/London` dtype checked |
| notebook outputs | cell 2: 13 units with both signs on 2026-09-21, `GSET-07` -17.0323 to 15.9734, `AFFR-1` -4 to 2; cell 3: 10 rows at 01:00 and 01:30 UTC on 2026-03-29 |
| `plot_alt` | the plot: `GSET-07` changes only at half-hour starts (all its windows are 1,800 s), -17.03 to 15.97 at 18:00; `AFFR-1` levels -4, -2, 0, 2 with 60 s windows |
| related | the instructions dictionary text above; availability silver shares all 60 of its units; `elexon/pn` is in the page set (Elexon BM physical notifications). All three resolve in the build |

## Body corrections (canonical note, smallest spans)

1. **Scope:** added the 2026-10-16 capture and that it still starts at `2025-10-08T16:00:00` (grew, did not roll).
2. **Typing:** added the 29 March 2026 clock-change test, the 26 October 2025 observation, and the
   last-modified-to-last-window observation (marked as fitting, not proof).
3. **Sentinels:** added the per-unit sign split (37 both signs, 51 always zero; 2026-10-16 capture).
4. **Files:** the file-name TODO resolved (three names recorded; a stable path is still unknown); added the second
   bronze capture path, hash, size and row count.
5. **Field meanings:** the `Unit ID` wording is the instructions dictionary's; added the unit overlap with the
   instructions and availability silver (TODO kept).
6. **Identity:** "The vendor guarantees no key" was wrong: CKAN declares `datastore_unique_keys` (`Unit ID`,
   `Time From`) with `datastore_append_or_update: true`. Added the cross-capture comparison (pure append; one interval
   does not prove immutability). Replaced "the file is a rolling window of about the last 12 months" with what the
   captures show.
7. **Row counts:** one Parquet file became one per capture (two, 495,086 and 523,890 rows).
8. **Cadence:** "gridflow has one capture" updated with the second capture.
9. **Known issues, segments:** added no-boundary-crossing, no overlap, and 37,502 level jumps between contiguous
   windows (2026-10-16 capture).

## Unverified

- **UTC across the whole file.** The rows exclude UK local time only on 29 March 2026; elsewhere UTC rests on NESO's
  dictionary.
- **Interpolation inside a window** and whether the end instant belongs to it: NESO states neither. The notebook plot
  draws straight lines between the two levels and says so in `plot_alt`.
- **Sign convention:** undocumented.
- **Whether NESO ever trims old rows:** two captures eight days apart only.
- **Why `GSET-*` units move in step** (same blocks on 2026-09-21): not stated on the page; no grouping is claimed.

## Open questions

None blocking.

## Seat note on service codes (2026-10-23)

Checked against the seat's note that NESO does decode `PQR`, `NQR`, `PSR`, `NSR` and `RDP`: this page, its note and
this report never claim otherwise. The page names no service code; the note body and this report mention "the three
`RDP` units" only to say they have no PN rows.

## Template problems (seat items)

1. **`gridflow-distil` and `gridflow-sample` read every silver file, not the `_latest` view.** For a `whole_capture`
   table with overlapping captures, a spec without `dedup` doubles every row (a `sum` or `count` chart would be wrong,
   and the sample can pick the same row twice). This page dedups on the key, newest `published_at` wins. Other
   multi-capture NESO pages should be checked.
2. Known items seen again: the notebook tab label clips at 390 px; the frame folds at 768 px (mitigated by putting
   the levels first).

## Defects

- **gridflow front-end tooling: chart and sample read all captures** (already in the batch file's "Checked facts";
  listed here only for this page's evidence). `src/gridflow_front_end/distil.py` `_scan` (line
  164) and `sample.py` `_scan` (line 51) scan every Parquet file under the table, so a `whole_capture` NESO table with
  more than one capture is double counted unless the spec adds `dedup`. `obp_physical_notifications` has two
  overlapping captures (2026-10-08 and 2026-10-16); its spec dedups on `(unit_id, time_from)` by `published_at`.
- **NESO data: one half-hour missing for every unit on 29 March 2026.** All five units present that day (`ENGQR-01`,
  `-02`, `-03`, `-05`, `ANSC-101`) have no window from 06:30 to 07:00 UTC; each runs to 06:30 and resumes at 07:00.
  Not the clock change (it fell at 01:00 UTC). Vendor gap, kept as published.
- **NESO docs: the PN `Unit ID` description is copied from the instructions dictionary** ("Registered Unit ID
  associated with the corresponding instruction"). Cosmetic; recorded in the note.
- **gridflow_models (already logged as 20r):** `query()` returns TIMESTAMPTZ columns in the session zone
  (`Europe/London`). The page's lead tells the reader and cell one converts.
- **Vault note (fixed here):** stale "single capture", "rolling window of about the last 12 months" and "the vendor
  guarantees no key"; the file-name TODO is resolved.
