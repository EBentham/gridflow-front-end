# 2-day-ahead-demand-forecast: checker's review

Family page `2-day-ahead-demand-forecast`, lead `demand_forecast_2d_day_ahead`, held member
`demand_forecast_2d_historic_day_ahead`. Checked 2026-10-24 in `C:\gridflow-wt\fe-neso-dem` against the canonical note in
`C:\gridflow-wt\vault-neso-dem`.

## Verdict: REVISE

One major (a sentence in the note body's Cadence section is false), one nit. The page itself is right: the archive-start
sentence, the chart, the hold line, units, counts, notebook and frame all reproduce.

Gates I ran: `gridflow-build --only neso_data_portal/demand_forecast_2d_day_ahead` wrote the page with no error (the only
warning is the vault-wide "known issues" grammar one). Detector `[]`. Mirror `cmp` clean with the vault note. Zero em
dashes in the page. Word budgets by my own count: `what_it_is` 60 (60), caption 40 (40), lead 35 (35). Series
`spec_origin: vault`.

## Findings

1. **major, note body, Cadence section (line 469 to 470 of the canonical note, mirrored).** "between the two captures it
   added every target date 2026-10-10 to 2026-10-18, none of which gridflow captured from the current file." The second
   half is false for 2026-10-18: the 2026-10-16 capture of the current file is exactly target 2026-10-18 (bronze
   `ng_demand_2da_20261018.csv`, `TARGETDATE` 20261018, 12 rows). Only 10 to 17 October were not captured from the current
   file (9 days added, 8 of them never seen there; 9 October was in the earlier archive). The sentence's point (a missed
   day in the current family is not recovered by the current file, the archive fills it later) is fine; the claim as
   written contradicts the note's own Files and Correspondence sections.
   Fix: "it added every target date 2026-10-10 to 2026-10-18; gridflow had captured only 2026-10-18 of those from the
   current file."

2. **nit, `page.notebook.cells[0]`.** The first cell converts `timestamp_utc` and `capture_written_at` to UTC, but the
   cell's output frame selects neither, so two of the three conversions do nothing visible. The lead sentence ("converts
   them to UTC") is true, so this is style only. Either trim the loop to `published_at` or keep it as the pattern the
   page tells the reader to use; not a blocker.

## Answers to the seat's points

1. **Archive start.** True, reproduced from bronze (read only). Both archive captures start at target 2023-04-03 (first
   data row `2,2023-04-03,22135,1F,F,30,30,NA,2023-04-01T15:37:36Z`; 1,285 target dates to 2026-10-09 in the first
   capture, 1,294 to 2026-10-18 in the second). NESO's resource description (catalogue snapshot `20261006T195819Z`,
   resource `24abd271`) reads "All historic 2 day ahead demand forecasts from 2018 to the most recent forecast", so the
   attribution is verbatim in substance. For contrast the 1-day archive really does start 2018-01-02 in both its
   captures, so the 1-day page's "holds day-ahead forecasts from 2018" is true and the 2-day page's counterweight is a
   genuine difference between the two files, not a copied claim. The wording is a NESO fact with a date ("its October
   2026 file"), not a local count and not a reference to local storage: the page states what NESO's published file
   contained when read in October 2026, and both captures (8 and 16 October) agree. It is plain and allowed. It is also
   consistent with the 1-day sentence ("NESO describes the archive as all day-ahead forecasts from 2018"): the 2-day
   page uses the same opening, then adds the dated fact. "With one issue per target date" is true of this file (one
   `FORECAST_TIMESTAMP` per date on all 1,285 and all 1,294 dates), unlike the 1-day file, so the dropped "though
   published twice daily" clause is right. Keep it; the fallback (drop the clause) is not needed.
2. **Chart.** Reproduced from bronze, both current captures (24 rows), `targetdate == 2026-10-18`, dedup on
   `targetdate, cardinalpoint`: 12 bars, 0 dropped. Values match the series file and alt text exactly: 24,559 / 23,572 /
   23,687 / 21,855 / 20,147 / 22,262 / 24,938 / 24,008 / 23,887 / 31,620 / 33,421 / 24,390. Trough 20,147 (`1B`, 430 to
   730), peak 33,421 (`4B`, 1830 to 2000). All 12 `group_map` labels match the 18 October windows in the file (`3C`
   1700 to 1800, `4B` 1830 to 2000; on 9 October they were 1700 to 1830 and 1900 to 2000). `sort: label` gives true
   time-of-day order (matches the series `x`). The chart is horizontal, so "Horizontal bar chart" in the alt is right.
   Alt walk is true ("near 24,000 into the afternoon" = 24,008 and 23,887; it skips the 31,620 bar, as the 1-day alt
   skips bars). Caption: 18 October 2026 is a Sunday; file stamped 15:15:01 on 16 October, read as UTC, matches the
   sidecar and silver `published_at`. Key note correct. Held rows never charted.
3. **Hold line.** "Forecast time stamps end in Z, but NESO does not confirm UTC." matches the registry question for the
   2-day historic family ("zone is undocumented (values carry Z but sit after the file's CKAN last_modified ...);
   whether it is the immutable issue instant") and is the 1-day line's first clause word for word. The 1-day registry
   question carries "some timestamps are vendor-documented email-recovery times"; the 2-day one does not, and the 2-day
   archive dictionary has no recovery text (searched: 0 matches; the 1-day dictionary has one). Dropping the clause is
   right. Evidence for the Z oddity reproduces: newest labels `2026-10-07T16:08:54Z` against file stamp 15:15:12
   (about 54 min after) and `2026-10-16T15:54:18Z` against 15:15:09 (39 min after). The ledger row gives only the unit
   code (E-SEM), not the wording.
4. **Units and counts.** `FORECASTDEMAND` unit `MW` in the 2-day current dictionary (and the archive dictionary); the
   1-day current dictionary has `DAYSAHEAD` unit "2" and `FORECASTDEMAND` unit blank with descriptions that say "2 day
   ahead", so the 1-day file is the copy and the 2-day one the original. Captures: current 578 bytes, 12 rows each,
   targets 20261009 and 20261018, no row repeated; archive 970,225 then 977,389 bytes, 14,608 then 14,716 rows; all
   14,608 earlier rows present unchanged in the second capture (anti-join: 0), 108 added (9 target dates, 10 to 18 Oct,
   12 each, one issue each). `F_Point`: `NA` 3,479 (targets 2023-04-03 to 2024-07-13, both captures), blanks 5,987 then
   6,059; blanks 8 of 12 in each current capture. Coverage detail true: 2026-09-02 absent; 9 to 12 points per date
   (497 dates with 12, 783 with 11, 13 with 10, 1 with 9); a `DP` code the current files lack. Windows change on 12
   October 2026, as the note says. Every archive label falls exactly two calendar days before its target (all 14,716
   rows). Vintages 12 s and 8 s apart true.
5. **Notebook, frame, row, links, body.** Notebook output: three read-only cells, no error, table of 12 rows in start-time
   order with `published_at` `2026-10-16 15:15:01.350931+00:00` (session-zone conversion shown correct); the plot is the
   committed picture, labelled `0030 1F` to `2400 4C`, and `plot_alt` values (20,147 at 0430 1B; 33,421 at 1830 4B after
   31,620 at 1700 3C) match it. Unfolded frame: 8 rows by 16 columns including lineage, in file order (a subsequence of
   NESO's order: 1F, 1S, 1B, 2A, 2B, 3B, 3C, 4B), all four `F_Point` labels present; values equal bronze. One row is one
   target date and cardinal point per publication (key includes `published_at`), correct. Related: the 1-day and 2 to 14
   day pages (12 points x 13 days = 156 current rows plus a half-hourly file, per the ledger), Elexon `ndfd` (vault note:
   daily forecast for each date 2 to 14 days ahead, covers D+2) and `indo` all exist and the reasons are true; the 7-day
   page not being linked is a seat choice. Request URLs match the sidecars. Body corrections re-derived true except
   finding 1; the intro now attributes NESO's "from 2018" and states the 2023-04-03 start, and no stale "one capture"
   statements remain.

## Rendering

Screenshots at 1440 and 768 (hero, chart, raw feed, frame and guide, notebook, related): nothing clipped or overlapping;
chart bars and labels legible. I did not repeat 1024 and 390 (the writer's shots cover them and the template is
unchanged). Server on 9852 started with its PID recorded and stopped by that PID; the port is no longer listening.

## Defects (pasteable)

- **NESO 2-day-ahead archive coverage (vendor/data):** the description says "from 2018", the file starts at target
  2023-04-03 (1-day archive: 2018-01-02), with 2026-09-02 missing and 9 to 12 points per date. A backtest from this
  archive has no 2018 to March 2023 history. No gridflow change.
- **NESO 2-day-ahead archive time stamps (already the hold question):** newest `FORECAST_TIMESTAMP` (...Z) is 39 to 54
  minutes after the file's CKAN `last_modified` read as UTC in both captures. For the NESO question packet.
- **NESO dictionaries (vendor):** the 1-day current dictionary is a copy of the 2-day one; the 2-day original puts
  "1930" in `CP_END_TIME`'s unit field and calls the clocks "Time UTC" against the archive's UK time.
