# Demand Flexibility Service 2023/24: checker's review

Page `demand-flexibility-service` (lead `dfs_utilisation_report_sum`). Checker, 2026-10-23.

## Verdict: REVISE (1 major, 2 nits; no blockers)

The one major is the wording of the held-member line. Everything else I tried to break held: the series reproduces
from silver, the clock claims are right, the captures are clean, the build and detector are clean.

## Findings

1. **Major** (seat may downgrade): `page.family.members[3].held` ("NESO does not say when each window's requirement was
   first published") is stronger than the evidence, and the page's own notification member contradicts it on its face.
   The notification file has, for all 16 delivery dates, a "Requirement Published" notice with an issued date and time
   (for example 29 November 2023: notice issued 28 November 14:30; 21 March 2024: issued the same day 12:00), and the
   family line for that member reads "Notices that a requirement may be, or has been, published for a date". What the
   ledger's question actually holds on is narrower: the requirement file has no publication time of its own, and the
   notices carry no event id, so they cannot be tied to a requirement edition (the note's Holds text: "when was each
   requirement first published, and does NESO retain earlier requirement editions?"; ledger row DFS-b: "requirements (no
   publication time)"). Evidence: silver `dfs_industry_notification`, 30 rows, 16 `Requirement Published` for 16
   distinct `requirement_for` dates; catalogue notes: the notification file "will indicate when the NESO anticipates
   publishing a DFS service requirement". Suggested line (14 words): "The requirement file has no publication time of its
   own; the notices give one only per date."

2. **Nit**: `page.record.fields.dfs_required_mw` ("Requirement NESO published for the window, MW") puts the held table's
   numbers on the page (frame, and notebook output). The summary's `dfs_required_mw` equals the requirement table's
   `dfs_required_mw` on all 32 windows (joined on delivery date and window start; 0 differences; same `window_to` and
   type). The note body explicitly allows the summary column ("a separate published summary column and is not the
   requirement table"), and the wording follows NESO's own dictionary ("Published DFS Service Requirement for service
   window"), so this is not a fault by the rubric. I flag it only so the seat rules knowingly: the page shows a
   requirement figure for each of 8 windows while holding the requirement file. If the seat wants a cleaner line,
   "Requirement for the window as the summary reports it, MW" avoids implying a publication claim.

3. **Nit**: `page.chart_view.alt`: "Test days to 17 January sit between about £0.59 million and £1.56 million. Both fall
   from 2 February". "Both" follows a range of two figures, so it can be read as the two bounds rather than the two
   series. Numbers are right. Suggest "Both series fall from 2 February".

## What I checked and found right

**Chart (series file against silver).** Reproduced from silver with Polars: 16 delivery dates, per-day sums of the
summary's `dfs_provider_bids_accepted_total_cost_gbp` and `settled_cost_gbp` match the committed series on every point
(for example 29 Nov accepted £3,031,162, settled £2,299,489; 1 Dec £3,573,586 and £2,464,136; 29 Feb £84,947 and
£73,863; 1 Mar £15,911 and £15,276).
- Summing over a day's windows is valid: one table, one capture (`bronze_capture_id` 1, `published_at` 1 distinct),
  32 rows, key (`delivery_date`, `window_from`) unique, `duplicates_dropped` 0 in the series provenance. Both columns
  are per-window £ amounts (accepted cost reconciles to bids x price x 0.5 h within £0.50), so they add across a day's
  windows. Nothing is added across tables and the two lines are never combined.
- Each date carries one type only (1 type per date), so a day's sum never mixes Live and Test. Live = 29 Nov and 1 Dec,
  the only two Live days; the rest Test. Live days are the top two on both series.
- Key notes: highest accepted £3,573,586 on 1 December ✓; settled above accepted on 7 of 16 days ✓ (15 Dec, 19 Dec,
  17 Jan, 2 Feb, 8 Feb, 2 Mar, 14 Mar). Alt: Test days to 17 January span £593,446 (settled, 12 Dec) to £1,557,000
  (accepted, 5 Dec) ✓; from 29 February all days under £90,000 (max £84,947) ✓; lowest 1 March ✓. Title, caption, unit
  (£), window and aggregation (sum) match the spec; `spec_origin: vault`, build digest check passes. Rendered chart at
  1024 and 390: y axis from 0, £ labelled, dots legible, nothing clipped.

**Clock.** Every summary and report row falls between 2023-11-16 and 2024-03-21; notices run 2023-11-15 to 2024-03-21.
Clocks went back on 29 October 2023 and forward on 31 March 2024, so no row is in British Summer Time (0 rows on or after
31 March in summary, report or notices). `timestamp_utc` is 00:00Z on all 32 summary rows. Windows run 16:30 to 19:00.
NESO's field dictionary marks `From`, `To` and `Notification Issued Time` as "GMT" in the comment field (summary, report,
requirement, notification), so "GMT in its dictionary" is accurate and appears on both window columns. `published_at`
"read as UTC" is ADR-030 D-15. The unfolded frame and the notebook output show 00:00 UTC and `+00:00` with window labels
as text; the notebook conversion is trivial here and the lead says so honestly ("Times come back in UK time, so the
first cell converts them to UTC").

**One row in each member (against NESO text and silver).** Summary: one window (32 rows; 26 Test, 6 Live). Report: one
bid outcome per DFS unit per window (1,220 distinct keys; 946 Accepted, 274 Rejected; 59 units, 25 participants).
Notification: one notice (30; 28 Test, 2 Live; 16 Requirement Published, 14 Anticipated Requirement Notice).
Requirement: one window (32). Units MW, £, £/MWh match the field-info snapshot. `dfs_procured_mw` equals the report's
Accepted MW summed on all 32 windows (max difference 0.0). Settled above accepted MW on 12 of 32 windows, all Test (0 of
the 6 Live), as the notebook plot alt says (six Live at 449 to 487 accepted and 299 to 358 settled; Test 56 to 523).

**Captures.** One bronze file and one silver file per table, all written 8 October 2026; no 2026/10/16 partition; row
counts 30 / 32 / 1,220 / 32 match the files (header plus rows); request URLs in the sidecars equal the family
`request` lines. No repeated rows; the `dedup:` guard is on both the chart and the frame and drops nothing.

**Related and known issues.** Related pages resolve (build ok); the 2022/23 Live and Test pages are 2022/23 series
(Live sum 23 to 24 January 2023, Test 15 November 2022 to 27 March 2023); the successor page is the one NESO's package
notes point to; the notes are 12 words or fewer. The swapped `From` entry in the requirement dictionary (`unit` 17:00,
`example` HH:MM) is as the note says; the regional columns sum to `total` on 1,133 of 1,220 rows (87 do not), as the
note says. Neither is printed on the page (the page's known-issues text is not rendered, a template matter) and the
page says nothing wrong about either.

**Mechanics.** Mirror `cmp` clean; the note is CRLF throughout (589 of 589 lines); the diff against `origin/master` is
the `page:` block only, no body edits. Build `--only neso_data_portal/dfs_utilisation_report_sum`: no errors (the 37-line
Known issues warning is global). Detector `[]`. 0 em dashes in the built page; no `locally`, `our`, `since 20` or local
row counts in the page text. Commands (`gridflow pipeline <source> <dataset> --last 24h`) are a real CLI command, the
same form used by the approved EAC pages. Notebook JSON written by the runner, read-only cells, no errors; plot alt
matches the real plot. At 390 px no horizontal page overflow (scrollWidth 390); the notebook tab label ends in an
ellipsis (known template item). Server on 9874 started with a recorded PID and stopped by that PID.

## Notes, not findings

- The frame prints accepted cost as `1.052833e6` for the first row: that is Polars' own float display, true to the
  tool.
- The writer's report says the note is 586 lines; it is 589. Immaterial.
