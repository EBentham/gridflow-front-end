# 7-day-ahead-national-forecast: checker's review

Family page `7-day-ahead-national-forecast`, lead `national_forecast_7d_day_ahead_demand`, held member
`national_forecast_7d_historic_day_ahead`. Checked 2026-10-24 in `C:\gridflow-wt\fe-neso-dem` against the canonical note in
`C:\gridflow-wt\vault-neso-dem`.

## Verdict: APPROVE

No blockers, no majors, three nits. The chart, the hold line, the capture counts, the archive observations, the notebook
and the frame all reproduce.

Gates I ran: `gridflow-build --only neso_data_portal/national_forecast_7d_day_ahead_demand` wrote the page, no error (the
only warning is the shared "Known issues" caveat-grammar line). Detector `[]`. Zero em dashes in the page and in the
`page:` block. Mirror `cmp` clean with the vault note (544 of 544 lines CRLF; the `origin/master` blob is LF, so the diff is
clean of line-ending churn). Series `spec_origin: vault`. No staged chart spec or authored override. Screenshots at 1440,
1024, 768 and 390 (390 through a 390 px iframe); nothing clipped or overlapping; at 390 the longest bar labels start about
14 px from the edge, as on the 1-day page. Server on 9853 started with its PID recorded; the Git Bash `$!` PID did not match
the Windows process, so I stopped the one listener on my own port 9853 by its Windows PID (25068) and confirmed the port is
free. Nothing else was touched.

## Findings

1. **nit, `page.what_it_is` (last clause: "the file skips from June 2018 to April 2023").** The clause is true and is a fact
   about NESO's published file, not about local holdings (see point 4), but it is written as an undated standing fact. NESO
   can backfill the archive, and the observation comes from two dated captures. Date it ("in the file as of 16 October 2026,
   target dates skip from June 2018 to April 2023") or say "its target dates skip". It also leaves out four single missing
   days (2023-04-17, 2024-08-28, 2024-12-14, 2026-09-07); fine for a page sentence, but "skips" alone could be read as the
   only gap.
2. **nit, note body "Holds" paragraph (about line 532).** "This page therefore publishes the archive's schema, row count and
   clock recipes only, not its data values or ranges." The page now states the archive's target-date coverage (a range) in
   `what_it_is`, and the note's Files section lists it, so the sentence is stale next to the page. Say "not its forecast
   values or time stamps". The approved 1-day page also describes archive structure ("recent target dates have one issue
   each"), so the page wording is allowed; only the note sentence needs aligning.
3. **nit, `page.family.members[1].differs` ("Every seven-day-ahead forecast NESO has kept since 2018") beside the gap clause.**
   A reader meets "since 2018" and then "skips from June 2018 to April 2023" two sections apart. "NESO has kept" makes it
   technically consistent and matches the 1-day wording, so change it only if you edit finding 1 anyway (for example
   "Seven-day-ahead forecasts from NESO's archive, each with a forecast time stamp").

## Answers to the seat's points

1. **Package name versus file.** Both current captures hold exactly one target date and 12 rows: the 2026-10-08 capture (file
   `ng_demand_7da_20261014.csv`, target 14 October) and the 2026-10-16 capture (`ng_demand_7da_20261023.csv`, target 23
   October); 578 bytes and 12 data rows each, `DAYSAHEAD` 7 on every row, no row repeated, each target seven days after the
   vintage date. The page says it plainly: "The current file holds one target date", the member line "Newest publication only:
   one target date, seven days on; the file name carries it", and the chart is a bar per cardinal point of one day, not a bar
   per day. The name does not mislead.
2. **Chart.** Reproduced from the bronze CSV and from silver (both captures, 24 rows, `targetdate == 2026-10-23`, dedup on
   `targetdate, cardinalpoint` by `published_at`): 12 bars, 0 duplicates dropped, `rows_read` 24, `rows_used` 12. Values equal
   the committed series and the page: 22,507 / 21,902 / 21,867 / 19,613 / 19,192 / 28,223 / 30,121 / 26,736 / 25,825 / 31,090 /
   32,182 / 22,304 MW. Trough 19,192 (`1B`, 430 to 730), peak 32,182 (`4B`, 1830 to 2000). The file's CKAN stamp is
   `2026-10-16T15:15:01.261954`, which silver reads as UTC, so "15:15 on 16 October, read as UTC" is right. 23 October 2026 is
   a Friday. All 12 `group_map` labels match the 23 October windows in the file (the 14 October windows are identical);
   `sort: label` gives true time-of-day order. Alt text and `plot_alt` are true to the series (30,121 over 08:30-12:00, 25,825
   over 13:30-16:30, 22,304 at 24:00; the notebook PNG shows the same bars). The `02:00-02:30 peak` (21,867) below the
   `01:00-01:30 trough` (21,902) is explained by the key note. The held archive is never charted. The caption's "labelled UTC
   in its dictionary but unconfirmed" is accurate: both 7-day dictionaries say "Time UTC".
3. **Hold line.** "Forecast time stamps end in Z, but NESO does not confirm UTC; the field is undocumented." The ledger row only
   names the question unit (E-SEM); the question text is the registry's: "FORECAST_TIMESTAMP has no vendor definition and its
   zone is undocumented (values carry Z); whether it is the immutable issue instant". The field-info dictionary lists
   `FORECAST_TIMESTAMP` as type `timestamp` with no title, description, example or unit, so "undocumented" is true; every
   value ends in `Z` (all 15,811 rows). The first clause is the 1-day line word for word; the second correctly drops the
   1-day's email-recovery clause, which does not apply here. It does not name the "issue instant" question, as on the 1-day
   page. The writer's note-body fix is right: the old quoted question ("sit after the file's CKAN `last_modified` when read as
   UTC") is false for this archive. In both captures the newest labels (`2026-10-07T12:47:45Z`, `2026-10-16T11:21:21Z`) are
   before that capture's `last_modified` (`15:15:13` and `15:15:09`). The note's Holds line now equals the registry question
   word for word.
4. **Archive facts.** Reproduced from bronze (both captures; `TARGETDATE` is `YYYY-MM-DD` in this file, `YYYYMMDD` in the
   current one; the registry has an epoch for each):
   - Gap: target dates 2018-04-01 to 2018-06-28 (89 dates), none for 2019 to 2022, then daily from 2023-04-08; single missing
     days 2023-04-17, 2024-08-28, 2024-12-14, 2026-09-07. Identical in both captures. "Skips from June 2018 to April 2023" is
     correct. It is a dated observation of NESO's published file, not a local-holdings statement (nothing on the page names a
     capture count, a path or local silver), so it is allowed in kind; finding 1 is about dating it. NESO's own wording is "All
     historic 7 day ahead demand forecasts from 2018 to the most recent forecast", and the page attributes that.
   - April 2018: targets 1, 2, 3 and 5 April (12 rows each, 48 rows) are stamped `2018-05-18T11:42:55Z` to `11:51:13Z`, 43 to
     47 days after the day they forecast. 15,750 rows are labelled seven days before their target, 13 (target 2018-05-01) six
     days before. Matches the note.
   - Append: capture 1 has 15,703 rows, capture 2 has 15,811; every row of capture 1 is in capture 2 unchanged (anti-join 0)
     and the 108 added rows are 9 target dates (15 to 23 October) x 12, one label each.
   - Current versus archive: all 12 rows of the 14 October current file equal the archive's rows on lead, target, point, value
     and window (label `2026-10-07T12:47:45Z`, in both archive captures); all 12 of the 23 October file equal the 16 October
     archive (label `2026-10-16T11:21:21Z`). So, unlike the 1-day package, the archive matches the current file exactly in both
     captures. One label per target date and one row per (target, point) in both captures; zero nulls.
5. **Units, frame, notebook, links.** MW comes from the current file's own dictionary (`FORECASTDEMAND`, unit `MW`), so no
   "from the archive" note is needed. The national demand definition and "daily, between 16:15 and 17:00 (clock time)" match
   the catalogue snapshot resource text. The unfolded frame shows 8 of 12 rows and all 16 columns including lineage;
   `published_at` `2026-10-16 15:15:01.261954 UTC` and `timestamp_utc` `2026-10-22 23:00:00 UTC` (23 October is BST) equal
   silver. The notebook has setup, a discovery cell and two cells; output has no error, the table shows 12 rows in start-time
   order with `published_at` `2026-10-16 15:15:01.261954+00:00` (the session-zone conversion took effect), and the bar plot is
   the committed PNG. The `tail()` lead is accurate (`_latest` is `whole_capture`, newest target first). Related links: the
   1-day page, the 2 to 14 day page, `elexon/ndfd` and `elexon/indo` are in the manifest and the reasons are true. Raw requests
   match the bronze `request_url` of the 2026-10-16 captures; the commands use `--last 24h`, as the approved 1-day page does.

## Observations, not findings

- `raw_feed.note` says "each daily upload replaces the current file", while the note body keeps a `TODO: verify` on that. Both
  captures and the file-name history support it, and the approved 1-day page says the same, so I left it.
- The writer's remark that the 2 to 14 day package's 2026-10-16 capture has 151 rows rather than 156 is for that page's
  checker; I did not check it.

## Defects (pasteable)

- **NESO 7-day-ahead archive (vendor/data):** the file described as "all historic 7 day ahead demand forecasts from 2018" has
  target dates 2018-04-01 to 2018-06-28 and then resumes on 2023-04-08, with single days also missing (2023-04-17,
  2024-08-28, 2024-12-14, 2026-09-07). Identical in the 8 and 16 October captures. For the NESO question packet.
- **NESO 7-day-ahead archive (vendor/data):** `FORECAST_TIMESTAMP` for targets 2018-04-01, 04-02, 04-03 and 04-05 (48 rows) is
  `2018-05-18T11:42:55Z` to `11:51:13Z`, 43 to 47 days after the day forecast; 13 rows for 2018-05-01 are six days ahead.
  The label is not always an issue time. Evidence for the held question; no gridflow change.
- No gridflow code defect found.
