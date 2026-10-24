# negative-reserve-active-power-margin-nrapm-forecast: checker's review

Checker, 2026-10-24. Verdict: **REVISE** (1 major, 6 nits, 0 blockers). The data, chart, commands, holds and Scotland claim all reproduce; the one
major is a two-word overclaim in the national member line.

Checked: note diff against `origin/master` (vault worktree), `cmp` of the mirror (identical; every line CRLF), series, sample and notebook
artefacts, the built page (rebuilt with `--only neso_data_portal/nrapm_forecast_national_daily_days`: no errors; detector `[]`), silver read with
Polars from the gridflow venv, bronze sidecars and headers, catalogue snapshot `20261006T195819Z`, field-info `20261008T114228Z`, registry JSON,
`cli.py` `pipeline`, the ledger row and `eligibility.md` rows 214 to 217. Screenshots at 1440, 1024 and 768; 390 checked numerically (see nit 7).
Server on 9813 started with PID 33188 recorded, stopped by that PID, confirmed down.

## Findings

1. **major** `page.family.members[0].differs` ("The whole system: MW away from a system-level NRAPM, days 2 to 14"). NESO's wording is "System
   Level" (field title and resource description) and "National" (resource and package names); it never says "whole". "The whole system" tells the
   reader the national figure covers Scotland too, which contradicts the page's own next line ("link to national unstated") and the note body
   ("Whether the Scotland calculation is a component of the national one is undocumented"). Evidence: catalogue resource description "Forecast
   Megawatt (MW) away from risk of system level NRAPM ... for overnight daily minimum 1B and daily minimum 3B"; no text in the package notes,
   resource descriptions or dictionary relates the two. Suggest "National, system-level: MW away from a system-level NRAPM, days 2 to 14".

2. **nit** `page.title`, `page.summary`. The hero reads "Negative reserve margin (NRAPM) forecast" and the summary "negative reserve margin risk";
   NESO's term is "Negative Reserve Active Power Margin", and the page set (hub) title is "Negative reserve active power margin (NRAPM)
   forecast", so hub and hero disagree. The title budget is 6 words (`page_fields.py` line 176), which the full name overruns by one. Option:
   "Negative reserve active power margin forecast" (6 words) with the acronym kept in `what_it_is`, and the full name spelled in the summary.

3. **nit** `page.what_it_is`. "NESO says a negative reserve active power margin (NRAPM) arises when too little flexibility is available". NESO's
   package notes say the *warning* "may be issued if there is insufficient flexibility available to ensure that generation matches demand during
   low demand periods". Closer: "NESO issues a system NRAPM warning when ..." The rest of the sentence (request for more flexible parameters, risk
   of emergency instructions) matches the notes.

4. **nit** `page.related[0]` ("Demand forecast for the same days, with `1B` and `3B` trough windows") and `how_used[1]`. NESO gives no `1B`/`3B`
   window in the NRAPM package, and the page says so, but this note invites reading the demand file's windows as NRAPM's. The demand note itself
   records that a code alone is not a stable point (on 2026-10-30 the overnight-minimum flag sits on `L04`, not `1B`). Reword to "Demand forecast
   for the same days, by cardinal point" (no window claim). Seat items, not findings: `daily-opmr` has no `page:` block yet, so that link lands on a
   blank hero until the held-page batch writes it; `system-operating-plan-sop` is itself a held page.

5. **nit** notebook plot (cell 4, `nrapm_forecast_national_daily_days-4.png`). The y axis starts near 3,000 MW, not zero, while the page chart
   starts at zero (`y_min: 0`); the legend labels read `national_mw 1B` with no gloss. `plot_alt` numbers are all correct. Optional: set the lower
   y limit to 0 and label the legend "national 1B overnight" / "3B daily".

6. **nit** canonical note body, cosmetic. The "Sign" paragraph now carries one very long line (`MW); its other 25 rows are positive. All 26 rows ...
   The reading "a`) and "Identity and selection" has a one-word dangling line ("No"). The "Why this family is eligible" paragraph still quotes only
   the 8 October vintage and first target date without saying "first capture"; it remains true for the 16 October file (earliest target anchor
   2026-10-17T23:00Z against a vintage of 2026-10-16T08:00Z). The writer's report says 567 CRLF lines; the note has 565, all CRLF, mirror identical.

7. **nit** process. My 390 px iframe screenshot truncated after the chart (virtual-time render), so I measured instead: at a 390 px viewport
   `scrollWidth == clientWidth == 390`, no overflow outside the scrolling frame. The 1440, 1024 and 768 screenshots show nothing clipped or overlapping;
   the frame unfolds to all 11 columns with horizontal scroll. Dark mode not checked (same as the writer).

## What I reproduced (all correct)

- **Row and key.** Silver: 52 rows per daily table, 42 distinct `(date, cp)`; 26 per capture, one row per date and `1B`/`3B`. Registry
  `entity_key [date, cp]`; the page's `Key: date, cp, published_at` follows the approved 2-14 day demand page. `1B` "overnight daily minimum" and `3B`
  "daily minimum" are NESO's words (resource and field descriptions); the page labels and the cp field line quote them and say no clock window is given.
- **Unit and sign.** Dictionary `unit: "MW"` on both daily value columns; no sign text anywhere in NESO's package, resource or dictionary text; the
  single negative is national `1B` 2026-10-10 = -2,862 (8 October file). The page says only that NESO does not define the sign. Correct.
- **Chart.** Series equals silver for the 16 October file (`published_at` 2026-10-16 08:00:44.528954 UTC), 18 to 30 October, national `3B`
  15,819 ... 20,104 (19 Oct) ... 7,914 (24 Oct) ... 19,204 and `1B` 11,670 ... 13,067 ... 3,363 ... 9,777; `y_min` 0; MW. The 18 to 22 October overlap: 10
  shared `(date, cp)` rows, all 10 differ in both national and Scotland (for example national `1B` 22 Oct 11,509 then 11,041; `3B` 17,901 then 15,723).
  Distil provenance `rows_read 52, rows_used 26, duplicates_dropped 0`: the `published_at >= 2026-10-16` filter does the work, `dedup` is a guard. Frame dedup on
  `[date, cp, published_at]` keeps both 22 October rows as intended. Alt text: `3B` above `1B` on all 13 dates (true), peak 20,104 on 19 Oct, trough 7,914 on
  Saturday 24 Oct (24 Oct 2026 is a Saturday), ends 19,204; `1B` peak 13,067, low 3,363, ends 9,777. All match.
- **Times.** `timestamp_utc == event_time` on all 104 daily rows; 23:00Z through 25 Oct (BST), 00:00Z from 26 Oct. `published_at` = CKAN `last_modified`
  read as UTC; no issue column. Field lines for both are right. Bronze: sizes 660/664 (national), 649/649 (Scotland), 1,745/1,742 and 1,747/1,747 (weekly);
  every header identical across the two captures; 26 and 55 data rows. Request URLs on the page equal all four sidecars' `request_url`.
- **Commands.** `cli.py` `pipeline` takes `source`, one `dataset` and `--last`; two commands (limit three), one per daily table, comment text correct.
  The same `gridflow pipeline neso_data_portal <key> --last 24h` form is on approved pages (`demand-flexibility-service-test-events`,
  `current-balancing-services-use-of-system-bsuos-data`, `eac-auction-results`); the 2-14 day demand page uses ingest plus transform. Both are precedent.
  The raw-feed note is the approved wording.
- **Scotland against national** (not over-claimed). 16 October files: national `1B` 3,363 below Scotland 4,369 on 24 Oct, and 4,185 below 4,268 on 26 Oct
  (also true on 10, 11 and 13 Oct in the 8 October files); elsewhere national is larger, and no value is equal. No NESO text relates the two series. The
  page says only "link to national unstated" (see finding 1 for the "whole system" wording) and, in the notebook alt, "below Scotland's 4,369" on 24 Oct.
  Scotland range 4,032 (23 Oct `3B`) to 6,827 (30 Oct `3B`): correct.
- **Weekly holds.** Both hold lines ("The load factor and probability columns have no NESO unit or scale, and their labels disagree.") match the registry
  question and the ledger and eligibility rows 216 and 217 ("no vendor unit or scale ... titles and descriptions contradict each other"); field-info shows
  `unit: ""` on both value columns, the national column titled "Scotland Level" and the probability description swapped. The weekly tables hold only those two
  value columns plus week and date, so the line covers the whole table. No codes or planning words.
- **`35W27` and body corrections.** Silver: week `35W27` is 2027-09-04 (Saturday, 8 Oct file) and 2027-08-30 (Monday, 15 Oct file) in both weekly tables;
  first file steps 6/7/8 days, second adds 2 and 13; 110 rows, 57 keys, 53 shared; spans 2026-10-25 to 2027-11-07 and 2026-11-01 to 2027-11-14. The daily
  corrections (two captures, vintages, "one negative" scoped to 8 Oct, identity unique within a body) all match silver. Each edit cites a check date and
  changes the smallest span; no unrelated rewrite.
- **Notebook.** JSON from `scripts/run_notebooks.py`, no error outputs, cells read-only (the `refresh`/`backfill` strings are the template's
  `data.neso_data_portal` method listing, not calls). Output: 26 rows, all the 16 October capture, `+00:00` stamps (session-zone conversion shown).
  `plot_alt` numbers (20,104, 7,914, 3,363, 4,369, 4,032, 6,827) reproduce. `tail()` orders newest target date first and drops the bitemporal columns
  (`handles/source.py` 453-489); the output holding only the latest capture confirms the `_latest` claim.
- **Rubric greps.** No em dashes, middle dots, arrows, "locally", "our copy", "live", planning words or counts of future work on the page. `related` notes are
  12 words or fewer; the weekly wind link is supported by NESO's weekly resource description.
- **Manifest.** Lead and member list correct.

## Defects (pasteable)

- NESO weekly NRAPM files move week `35W27` between publications (Saturday 2027-09-04 in the files last modified 2026-10-08, Monday 2027-08-30 in those
  last modified 2026-10-15; steps of 2 and 13 days in the second); gridflow's `(date, week_number)` key does not follow a week across captures. Confirmed
  here against silver for both weekly tables.
- Carried over, still open: national daily datastore `total: 52` against a 26-row upload.
- NESO dictionary `Date` examples are day-first (`25/03/2020`) while the files send `YYYY-MM-DD`.
