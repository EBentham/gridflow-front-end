# Review: STOR committed windows (`stor-windows`, table `stor_windows`)

**Verdict: REVISE** (1 major, 3 nits). Build `--only neso_data_portal/stor_windows` exit 0 (only the template-wide
caveat-grammar warning); detector `[]`; mirror `cmp` identical to the vault note; no em dashes, middle dots, arrows,
"live", "locally" or planning words on the page or in the `page:` block. Screenshots taken by me at 1440, 1024, 768
and a true 390 (390 px iframe), light only: nothing clipped or overlapping; the notebook plot PNG is intact.

## Findings

1. **major** `page.chart_view.caption`: the seat ruling accepts a Season 19 bar chart only if the caption says why that
   season and what a bar counts. The caption says what is counted ("delivery dates counted by `season`") and the window,
   but never why Season 19. Nothing on the page says it is the latest of the five seasons in the file, so the reader
   cannot tell why the other four are absent. Evidence: caption "Silver `stor_windows`, delivery dates counted by
   `season` for Season 19, 1 April 2025 to 31 March 2026. Each key note gives ...". Fix: add the reason, for example
   "the latest of the five seasons in the file", and say a bar is the number of delivery dates in that part. (The
   chart values themselves are correct, see below.)

2. **nit** `page.chart` (no `dedup`): correct today (one capture), but the chart is a count and the series builder reads
   every silver capture. The connector skips only when `last_modified` is unchanged (`client.py` 1751-1767), so the next
   NESO re-upload produces a second full capture and a regenerated series would double every bar. The spec supports
   `dedup: {on: [date], order_by: published_at}` (`chart_spec.py` 296-307), as the checked-facts note for repeating
   captures advises. Consider adding it to the chart and the frame so the committed artefacts stay right on refresh.

3. **nit** `page.record.fields.wd_nwd`, `record.caption` and the report's Defects: in this file `WD` is not "Monday to
   Friday". Saturdays are `WD` (259 of 261), Sundays `NWD` (261 of 261), and the 42 weekday `NWD` dates are all English
   bank holidays. The eight rows on the page include Saturday 29 March 2025 flagged `WD`, with nothing to explain it, and
   the key notes say "Working days". The page claims no rule ("as NESO flags it, not recomputed"), so nothing is false,
   but a reader checking the frame against a calendar will think a row is wrong. Suggest a short scoped note in the guide
   line, for example "Saturdays are `WD` in this file". Related: the writer's report says the 19 September 2022 oddity is
   "Vault note only", but the vault diff (134 insertions, 2 deletions) contains no such line, so it is recorded nowhere
   except the report. The fact itself is right (Monday 19 September 2022, season 16.3, `WD`; every other English weekday
   bank holiday from 2021 to 2026 is `NWD`, 42 dates); add it to the note body or to the seat's data-observation log.

4. **nit** `page.what_it_is`, `record.fields.season`, `chart_view.title`: "part" and "Season N" are gridflow's reading.
   NESO's dictionary says only "Time frame for which the committed STOR windows apply" (example `18.1`) and the package
   notes say "Season 15 to Season 19"; that the digit after the point is one of six parts of a season is inferred from
   the rows (contiguous blocks, six per season) and the writer lists it as unverified. It is a safe inference, but state
   it as what the file shows ("six blocks of dates per season in this file"). Also "Each season part has the same windows
   in all five seasons" is true only per day type (working and non-working days differ inside a part); add "and day type".

## Checked and correct (the four points to look hardest at)

**1. Chart.** Silver, filter `date` 2025-04-01 to 2026-03-31 (365 rows), group `season`:
19.1 27, 19.2 112, 19.3 35, 19.4 28, 19.5 91, 19.6 72; committed series `x`/`values` identical; alt text numbers and the
"longest parts 19.2 and 19.5" sentence match. Key-note dates match min/max `date` per label (1 to 27 April 2025; 28 April
to 17 August; 18 August to 21 September; 22 September to 19 October; 20 October to 18 January 2026; 19 January to 31
March 2026). All twelve key-note window pairs match the rows exactly (one window pair per season and day type). Same
windows per part in all five seasons: grouping by (part, day type) gives exactly 1 window form each and `seasons`
nunique 5 on all 12 patterns (notebook cell 4 shows the same). Seasons are contiguous blocks, 30 labels `15.1` to `19.6`;
26 of 30 parts start on a Monday (the four `.1` parts start 1 April). Committed hours 10 to 13.5 on `WD` (6 to 8.5 on
`NWD`). `spec_origin: vault`, digest build check passed.

**2. Times.** All four window columns match `^\d\d:\d\d$` in 1,826 of 1,826 rows, kept as text; no end at or before its
start and window 2 never starts before window 1 ends. NESO's dictionary (field-info snapshot `20261008T114228Z`) gives
no zone or unit; the page claims neither UTC nor UK time ("`HH:MM` text with no zone stated", plot axis "no zone
stated"). `timestamp_utc` = `event_time` = UK midnight of `date` as UTC: `casting.py` 610-630 (`date_sp1` through
`settlement_period_to_utc(date, 1)`); rows show 2025-03-30 00:00Z, 2025-03-30 23:00Z for 31 March, 2025-03-31 23:00Z
for 1 April. `published_at` = `available_at` = 2026-07-27 14:25:54.738965 on every row. Notebook: `query()` relation
`silver_neso_data_portal_stor_windows_latest`, date column `date`, excluded columns `event_time`, `available_at`,
`vintage_policy`, `source_run_id`, `dataset_version`, `month`, `year` (I read the registry in the gridflow_models
venv); the query cell converts `timestamp_utc`, `published_at`, `capture_written_at` from the session zone to UTC, and
its output shows `uk_time` 00:00 on all four rows across the clock change. Notebook written by `run_notebooks.py`,
read-only cells, no error outputs, `plot_alt` matches the PNG (looked at).

**3. Row, flag, auction.** One row per delivery date (`date` unique 1,826 of 1,826; registry key `[date]`). The page's
"windows on each STOR service day where STOR must be provided under its Day Ahead Service Terms" paraphrases NESO's
package notes (catalogue snapshot `20261006T195819Z`) accurately; "Seasons 15 to 19, applicable 1 April 2021 to 1
April 2026", "Ad hoc" and the 27 July 2026 last-modified match the snapshot. The auction link uses NESO's words
("for the availability windows", `Tendered MW` and `Contracted MW`) and does not equate availability windows with
committed windows; gridflow joins neither table. The fourth related note ("NESO ended STOR day-ahead after launching
them") is backed by the sibling auction note (lines 308, 334). The 19 September 2022 flag: confirmed (see finding 3).

**4. Capture.** One silver file, one bronze capture. Bronze: 1,827 lines = header + 1,826, 80,748 bytes =
`declared_content_length` and `body_size_bytes`, SHA-256 `6e5c1515...` matches the sidecar, CRLF, BOM. Parsing the
bronze CSV and comparing with silver gives an identical frame; no duplicated rows; dates continuous from 2021-04-01 to
2026-03-31 with no gap. One `bronze_capture_id` and one `capture_written_at`. Not truncated.

Raw feed: package_show URL and the download URL match the sidecar `request_url`; "downloaded whole unless
`last_modified` is unchanged" matches `client.py` 1751-1767; the `--last 24h` commands and comments match the approved
sibling pages (48 h tolerance, 7 d cap in `client.py`).

## Not findings
- Template notes in the writer's report (no band chart type, key notes wrapping at hyphens, notebook tab truncation,
  caveat-grammar warning) are seat items.
- Body edit (opening paragraph) cites NESO's notes and the auction dictionary and is the smallest span; correct.
- Not checked: dark theme screenshots.
