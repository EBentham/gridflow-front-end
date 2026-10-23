# Writer report, round 2: STOR committed windows

Fixes for every finding in `stor-windows-review.md` (1 major, 3 nits). Build `--only neso_data_portal/stor_windows`
exit 0 (budgets pass; only the template-wide caveat-grammar warning); detector `[]`; 0 em dashes; mirror `cmp`
identical; note CRLF throughout (400/400); vault diff now 141 insertions, 3 deletions. Series and sample re-distilled
(both specs gained `dedup`); values unchanged. Notebook cells unchanged, so not re-run (the build's digest check passes).

## Changes

1. **major, caption: why Season 19 and what a bar counts.** `chart_view.caption` is now "Silver `stor_windows`,
   Season 19, the latest of five in the file, 1 April 2025 to 31 March 2026: each bar counts the delivery dates with
   that `season` label. Key notes give each label's windows, zone unstated." (37 words). Season 19 is the latest of the
   five: labels `15.1` to `19.6`, NESO's notes "Season 15 to Season 19".
2. **nit, dedup.** `dedup: {on: [date], order_by: published_at}` on `page.chart` and on `page.record.select`, so a
   second capture after a NESO re-upload keeps one row per delivery date, from the newest file. Distil provenance:
   `duplicates_dropped: 0`, rows used 365, values 27, 112, 35, 28, 91, 72 as before; the eight rows are the same.
3. **nit, Saturday flag and the 19 September 2022 oddity.**
   - `record.fields.wd_nwd`: "NESO's working-day flag, undefined by NESO; here Saturdays are mostly `WD`, Sundays `NWD`"
     (13 words). NESO gives no definition: the dictionary says only "Working Day/ Non Working Day", and the package
     notes and resource description say nothing about the flag. "Mostly": Saturdays `WD` 259 of 261 (25 December 2021
     and 1 January 2022 are `NWD`); Sundays `NWD` 261 of 261.
   - Note body, Gotchas, "`WD_NWD` is the vendor's flag": added the dictionary wording, the Saturday and Sunday
     counts, that the 42 weekday `NWD` dates are English bank holidays, and that Monday 19 September 2022 (the Queen's
     state funeral, season `16.3`) is the one English bank holiday flagged `WD`.
4. **nit, "part" and "same windows" as gridflow's reading, per day type.**
   - `what_it_is`: "... In this file each season has six blocks of dates, each with fixed windows per day type across
     all five." (59 words in all; to fit, "under its Day Ahead Service Terms" left `what_it_is`; NESO's sentence there now
     reads "NESO says STOR must be provided in them on each service day". The full quote stays in the note body.)
   - `record.fields.season`: "NESO's season label, `15.1` to `19.6`; in this file six date blocks per season".
   - `chart_view.title`: "Delivery dates per season label in Season 19"; `notebook.plot_alt` "for each season label
     of Season 19". No "part" is left on the page.

## Visual check

Server on 9980 started in the background with its PID recorded (6271) and stopped by that PID (`kill 6271`, then a
refused request). Shots of the changed prose, caption and guide at 1440 and 390:
`.planning\neso-dp\ancillary-b\stor-windows-shots\stor-windows-r2-{1440,390}.png`. Nothing clipped or overlapping.

## Defects

- **NESO data observation (not gridflow), now in the vault note body:** NESO's STOR windows file flags Monday
  19 September 2022 (the bank holiday for the Queen's state funeral) as `WD`; every other English weekday bank holiday
  from 2021 to 2026 is `NWD` (42 dates). NESO does not define the flag, so this may be intended. No gridflow fix.
- No gridflow defect.
