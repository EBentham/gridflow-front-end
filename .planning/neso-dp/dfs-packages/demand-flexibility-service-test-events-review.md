# Demand Flexibility Service 2022/23 test events: checker's review

Page `demand-flexibility-service-test-events` (lead `dfs_test_events_utilisation_report_sum`). Checker, 2026-10-23.

## Verdict: REVISE (2 majors, 2 nits; no blockers)

The chart reproduces from silver on every point, the clock wording does not over-claim, the captures are clean and the
build and detector pass. The two majors are one wrong phrase in the chart alt text and the held-member line, which
needs the same narrowing the approved 2023/24 page got.

## Findings

1. **Major**: `page.chart_view.alt`: "the last two days settle 0.725 and 1.01 MW" is wrong. The last two test days on
   the chart are 23 March (settled mean 235.695 MW) and 28 March (1.01 MW); 0.725 MW is 21 March, the third from last.
   The numbers are in the series, the date claim is not. Evidence: series file `settled` (last five values 11.5,
   231.355, 0.725, 235.695, 1.01 for 14 March to 28 March); silver per-day means agree. The key note ("1.01 MW or less
   on 21 and 28 March") is right. Suggested: "settled falls to 0.725 MW on 21 March and 1.01 on 28 March".

2. **Major** (seat may downgrade; same finding as 2023/24 round 1): `page.family.members[3].held` ("NESO does not say
   when each window's requirement was first published") is stronger than the evidence, and the page's own notices
   member contradicts it. The notices file has a `Requirement Published` notice for every one of the 19 test dates,
   posted the day before at 14:30 (text: "A DFS Service Requirement has been published for tomorrow"). Silver
   `dfs_test_events_service_update_industry`: 40 notices = 19 `Requirement Published` (19 distinct posting dates, each
   exactly one day before a test date: 14 Nov to 15 Nov, 21 Nov to 22 Nov ... 27 Mar to 28 Mar), 20 `Anticipated
   Requirement Notice` (10:00, one at 10:30), 1 `Test DFS Requirement not issued` (22 January, which has no test
   date). The dictionary's `Type` text says "Published at around 14:30 GMT when a requirement for DFS has been
   published". So a per-date publication time does exist here. What the ledger's question actually holds on is
   narrower: the requirement file has no publication time of its own (note Holds: 38 of 40 windows start on or before
   the file's stamp; ledger "no publication time, 814"), and the notices carry no window or event id, so they cannot
   be tied to a requirement edition. Suggested line, identical to the approved 2023/24 wording: "The requirement file
   has no publication time; the notices give one only per date." (Per-date only: the notices name no windows.) The
   rendered page shows the line as "Rows not shown: NESO does not say when each window's requirement was first
   published."

3. **Nit**: `page.chart_view.key[1].note` ("above the requirement on 19 January and 15 March") is true of the daily
   means the chart draws, not of every window: on 21 February the 18:00 window accepted 252.42 MW against a 250 MW
   requirement (day mean 249.39, under it). The chart shows that day just below, so a reader is not misled, but the
   note reads as an exclusive list. Suggested: "on average above the requirement on 19 January and 15 March".

4. **Nit**: `page.record.fields.dfs_required` ("Requirement NESO published for the window, MW") shows the held table's
   figure through the summary column. Same point as 2023/24 nit 2; the summary column equals the requirement file on
   every window (checked: all 40 windows, same MW), the wording is NESO's own ("Published requirement for DFS event"),
   and the approved 2023/24 page kept the same line. Flagged only so the ruling is knowing; no change needed if the
   seat keeps the approved wording.

## What I checked and found right

**Chart (series file against silver).** Reproduced with Polars from the one silver capture: for each of the 19 test
dates the mean over the day's windows of `dfs_required`, `dfs_procured` and `settled_volume` matches the committed
series to float rounding (largest difference 5.7e-14); the 19 x dates match. Day window counts are two on 18 dates and
four on 12 December, as the caption says. `spec_origin: vault`, spec sha present, `duplicates_dropped` 0, 40 rows read,
120 values used.
- Averaging is a fair, stated measure here. All three columns are MW per half-hour window (power, not energy), so
  the sum across a day's windows would be a meaningless number and the mean is the right daily figure. The caption
  says "averaged over its half-hour windows (two; four on 12 December)"; the unit and window are stated. The
  requirement is constant within every date (1 distinct value per date), so its mean is the requirement itself.
  Nothing is stacked or added across series or tables; the three lines stay separate.
- Key notes and alt against the series: requirement 25 to 300 MW (28 March 25, 12 December and 23 March 300) ✓;
  settled above accepted on the first five days (15 Nov to 12 Dec) and below on 12 of the 14 later days (exceptions
  13 and 21 February) ✓; "133.39 against 75.9 MW on 15 November" ✓; accepted peak 268.33 on 15 March ✓; settled peak
  269.0 on 21 February ✓; 0.725 (21 March) and 1.01 (28 March) as values ✓ (the date phrasing is finding 1).
- The steep segments (30 to 31 January: accepted 187.61 to 19.84, requirement 250 to 100; 14 to 15 March: accepted
  13.61 to 268.33) join two consecutive calendar days and both ends are true daily means, not an interpolation. They
  read as ramps because the renderer joins only dates one day apart and leaves every other gap as unjoined dots. I do
  not count it as misleading: x axis label says "days without a test absent", the dots carry the information, and
  the per-window frame shows the 14 and 15 March windows with their own values. It is the writer's already-listed
  template item (a points-only option), so a seat item.
- Rendered at 1440, 1024, 768 and 390: y axis from 0, MW labelled, dots and key legible, nothing clipped (the 28
  March dots sit just inside the right edge). Hero scenery, strata corner labels, folded and unfolded frame and
  guide, notebook panel and related links all fully visible at all four widths. Known template items only (folded
  frame shows two key columns at 390).

**28 March 2023 clock.** NESO's dictionary marks `From`/`To` (summary, report) and `From GMT`/`To GMT` (requirement)
with comment `GMT` and the notice `Type` text says "around 10:00 GMT" and "around 14:30 GMT". Clocks went forward on
26 March 2023, so the two 28 March windows (labels 18:00 and 18:30) and the 27 March notices (labels 10:00 and 14:30)
fall in British Summer Time; no other row does. The page says exactly two things: the frame caption "28 March is in
British Summer Time" (a date fact) and the guide "GMT in its dictionary; kept as text" on `window_from` and
`window_to`. It never says whether NESO's labels on that day are GMT or UK local time. `timestamp_utc` is 00:00 UK
time on `date` (silver: 38 rows at 00:00Z, the two 28 March rows at 2023-03-27 23:00Z), and the guide says so with the
23:00 note; the frame and notebook output show 23:00 UTC. The chart uses `time: date`, so 28 March plots on 28 March.
The 10:00 GMT in the `d0_*` lines is NESO's own dictionary wording. No over-claim.

**Held requirement line against the ledger.** The ledger row (DFS-b, test events: "requirement (no publication time,
814)") and the note's Holds text hold on "when was each requirement first published". The page's held line states more
than that (finding 2); no requirement number is hidden: the requirement file's MW equal the summary's `dfs_required`
on all 40 windows, which is the same disclosure the approved 2023/24 page makes.

**Captures.** One bronze CSV and one silver file per table, all written 8 October 2026 (bronze names
`raw_20261008T1006xxZ`); no `2026/10/16` partition anywhere in bronze or silver for any of the four. Line counts of the
bronze CSVs are 41, 740, 41, 41 (header plus 40, 739, 40, 40) and silver rows are 40, 739, 40, 40. One
`bronze_capture_id`, one `published_at` and one `capture_written_at` per table. The sidecar `request_url` for each
table equals the family `request` line on the page (resource ids `e4804faf`, `fc466b76`, `a2dd7992`, `000066dc`).
Keys are distinct: summary 40/40 on (`date`, `window_from`); report 739/739 on (`date`, `window_from`, `unit`). The
`dedup:` guard is written with the key quoted (`{"on": [...]}`) on both the chart and the frame in the note; the
distilled series spec carries `on`, and it drops nothing.

**One row in each member.** Summary: one half-hour test window (40 rows, 19 dates). Report: one bid of one DFS unit
in one window (739; 613 Accepted over 34 units at £3,000/MWh; 126 Rejected over 11 units, £3,000 to £6,000/MWh,
matching notebook cell 4). Notices: one notice by posting date, time label and type (40). Requirement: one window
(40, held). Units MW, £ and £/MWh agree with the field-info snapshot (`20261008T114228Z`). `dfs_procured` equals the
report's Accepted MW summed to NESO's two-decimal rounding on all 40 windows (largest difference 0.0046 MW), which is
what the guide says ("the report's Accepted bids summed"). Cost: 7 MW x £3,000 x 0.5 h = £10,500 on the 28 March
windows, as published.

**Test against live.** Package notes say the dataset covers "the test service (not live events)" and point to the
live-events dataset; the page says only that live events are a separate package and "never add them" in the related
note. The catalogue cadence is `Not Active`; resource `last_modified` is 27 March 2023 for the requirement and the
notices and 27 July 2026 for the report and summary, as the cadence line says.

**Frame, notebook, related.** The frame's eight rows are real (`generated_by: gridflow-sample`, shape (8, 18)); the
guide covers every non-pipeline column, key columns first; the caption names the four dates and says 28 March is in
British Summer Time. Notebook JSON written by `scripts/run_notebooks.py`, five cells, no errors, read-only cells. The
`query()` lead matches `source.py:401` (relation `_latest`, `date` column, inclusive ends, bitemporal lineage columns
dropped). Cell 3 shows 28 March `timestamp_utc` 2023-03-27 23:00:00+00:00 and the UTC `published_at`. Plot alt against
silver: accepted 7.0 to 270.69 MW, settled 0.72 to 269.2, 17 of 40 windows above the line, both 15 November windows
(74.31/125.36 and 77.49/141.42) ✓. Related pages resolve: `demand-flexibility` ("from winter 2024/25": archive starts
29 November 2024 ✓), `demand-flexibility-service` ("Test and Live rows in one table" ✓, 12 words), the live-events
page, and `elexon/system_prices`; every note 12 words or fewer.

**Mechanics.** Mirror `cmp` clean. The note is CRLF on every line (569 of 569; the writer's 559 is a miscount,
immaterial). The diff against `origin/master` is 134 insertions, 0 deletions, the `page:` block only, so no body
edits to check. Build `--only neso_data_portal/dfs_test_events_utilisation_report_sum`: no errors (the 37-line Known
issues warning is global). Detector `[]`. In the rendered text: no em dashes, middle dots or arrows, none of `locally`,
`held`, `our`, `since 20`, `% of`; "rows" appears only in generic copy; "live" only as NESO's event type. Commands
(`gridflow pipeline neso_data_portal <dataset> --last 24h`, two lines) are the same form as the approved 2023/24 page.
Server on 9876 started with a recorded PID and stopped by that PID (port closed after).

## Notes, not findings

- The writer's observation about the sibling live-events block writing `dedup: {on: [...]}` unquoted is not this
  page's file; this page quotes it correctly. Worth the seat passing to the live-events checker.
- The unfolded frame prints `bids_accepted_total_cost` as `111467.0` etc.: Polars' own display, true to the tool.
