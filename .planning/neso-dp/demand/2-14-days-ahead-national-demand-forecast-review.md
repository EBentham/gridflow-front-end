# 2-14-days-ahead-national-demand-forecast: checker's review

Verdict: **APPROVE** (4 nits, no blocker, no major).

Run by the checker, 2026-10-24. Build `--only neso_data_portal/national_demand_fc_2_14d_days_ahead` wrote the page with no
error; detector `[]`; mirror `cmp` clean against the canonical note; zero em dashes, middle dots or arrows in the page and in
the `page:` block; no "locally", "our copy" or planning words. Screenshots taken at 1440, 1024, 768 and 390 (390 through a
390 px iframe slice), light only; nothing clipped or overlapping, the chart's x ticks thin to alternate dates at 390 and
the key stacks below, the frame scrolls inside its box. Server on 9854 started with its PID recorded (28445) and stopped
by that PID; confirmed down. Dark mode not captured.

## What I reproduced

1. **The 151 rows (bronze 2026-10-16, read only).** 6,133 bytes, 151 data lines, 151 unique `(daysahead, targetdate,
   cardinalpoint)`. Target dates 18 to 30 Oct, leads 2 to 14. 18 to 24 Oct: 12 points each with `3C` P 1700-1800 and `4B`
   P 1830-2000. 25 Oct: 12 points, `3C` gone, `DP` P 1700-1800 (`EM`) added, `4B` becomes F 2100-2100, `1A` widens from
   200-230 to 100-230, `1S` still present. 26 to 30 Oct: 11 points (`1S` gone as well). 7 x 12 + 12 + 5 x 11 = 151. The
   writer's table is exact. `4B` is F 2100 on all six days from 25 Oct; `Om` sits on `L04` (F 400) on 30 Oct.
2. **Chart.** Silver filtered to `published_at >= 2026-10-16`, `f_point in (EM, Om)`, dedup `[targetdate, f_point]` by
   `published_at`: 13 dates, evening and overnight values equal the committed series exactly (evening 33,421 ... 36,330;
   overnight 20,147 ... 20,467); silver holds two captures (307 rows; `published_at` 2026-10-08 08:45:03.632388 and
   2026-10-16 15:19:59.536755), so the filter does the real work and dedup is a guard (drops 0). In the 16 Oct file every
   date has exactly one `EM` and one `Om`; `EM` equals that day's maximum and `Om` its minimum on all 13 dates, on both
   sides of the clock change. Alt text and plot_alt numbers all match; 24 Oct 2026 is a Saturday. Notebook output (26
   rows, `published_at` shown as `+00:00`) and the saved PNG match the committed series; the notebook JSON came from
   `scripts/run_notebooks.py`, no error output, all cells read only.
3. **`EM`/`Om` attribution.** This package's `F_Point` dictionary entry lists the four labels without codes (confirmed in
   field-info `20261008T114228Z`); the 1-day, 2-day and 7-day dictionaries carry the pairing comment word for word as the
   writer quotes it ("Overnight minimum (OM) ... half hour ending 00:30 and 07:30"; "Evening peak (EM) ... half hour
   ending 17:00 and 24:00"). The key notes say "as NESO's day-ahead dictionaries define it", which is honest about whose
   definition it is. The definition's windows are not zone-stamped by NESO; the data fit (the `EM` row always falls in
   1700-2000 raw, `Om` in 400-730), so the page's statements hold across the clock change.
4. **Archive claim.** Archive 16 Oct capture (371,933 rows): 28 publication days 2026-09-19 to 2026-10-16 each have exactly
   one `forecast_timestamp` (09:44:59Z to 09:45:07Z); 12, 16 and 18 Sep have two (09:45Z and about 16:20Z); older days
   with two: 305 of 2,147. Current file 16 Oct (stamp 15:19:59) against the archive's only 16 Oct issue
   (`2026-10-16T09:45:03Z`): same 151 keys, 44 equal, 107 differ. 8 Oct: current file (08:45:03) against the 09:45:02Z
   issue: 156 of 156 equal. The 8 Oct archive's 370,700 rows are all present unchanged; 1,233 added = eight issues
   (156, 156, 156, 155, 154, 153, 152, 151). The "no key repeats" and group counts in the body (283,147 and 44,393; no lead
   and target after 2 Oct with two issues) reproduce.
5. **Hold lines.** Half-hourly: ledger question is whether `GDATETIME` labels the half-hour end (DST-day behaviour
   unobserved); the page line asks only start-or-end. The dictionary does state the clock (`CTIME` "GB timezone",
   `GDATETIME` "GMT/UTC regardless"), so dropping the clock from the line is right. Archive: ledger "zone undocumented ...
   no vendor definition"; this file's dictionary leaves every attribute of `FORECAST_TIMESTAMP` empty; the line equals the
   7-day page's line word for word, which matches the ledger's identical wording for 2-day and 7-day. Both lines are plain,
   no codes, no local data.
6. **Half-hourly file in bronze 16 Oct.** 625 rows; 49 on 2026-10-25 (`CTIME` 30, 100, 130, 130, 200 with `GDATETIME`
   23:30, 00:00, 00:30, 01:30, 02:00; no 01:00Z row); 612 of 625 rows agree with `DATE` and `CTIME` through Europe/London,
   the other 13 are the `2400` rows. As the writer says. Extra check: for all 151 cardinal-point rows the value equals the
   half-hourly value at `CTIME` = start (fixed points), or the max (P) or min (T) over `CTIME` in start..end inclusive. So
   `differs` "The same forecast as a half-hourly curve" is sound, and the match supports the end-label reading without
   settling it (the hold stands).
7. **Other.** Requests equal the three 2026-10-16 sidecar `request_url`s. Cadence and archive history quote the catalogue
   snapshot `20261006T195819Z` correctly ("updated twice daily, at 09:20 and 14:20"; "from 2020 to the most recent
   forecast"; earliest archive forecast stamp 2020-09-22). Units: MW from this package's own dictionary. Frame: 8 real rows
   (`gridflow-sample`), guide covers every non-pipeline column, key columns first, the `4B` example visible in the frame
   (24 Oct P 1830-2000, 26 Oct F 2100). Note-body edits: ranges 17,358 to 36,082 and 17,303 to 37,809, blank `f_point`
   104 of 156 and 99 of 151, no zeros, vintages for half-hourly (15:21:36.457364) and archive (15:21:30.359237), 307 base
   rows and 151 `_latest`: all reproduce. Related links resolve (build) and each note is 12 words or fewer.

## Findings

1. **nit** `page.what_it_is` ("the set changed at the October clock change"): "the set" is ambiguous (a reader may take it
   as the set of forecasts). The plain fact is that NESO swapped some cardinal points for others from 25 October (and
   days from 26 October carry 11 points, not 12). Suggest "the set of cardinal points changed at the October clock
   change". The frame and the `cardinalpoint` guide line already show the swap (3C to DP, 4B changing meaning), so this
   is a wording tidy, not a missing statement.
2. **nit** `page.what_it_is` ("recently it keeps one of each day's two updates"): "recently" is undated and the archive
   does keep both updates on some earlier days (12, 16 and 18 Sep 2026 have two issues). The evidence supports "one a day
   from 19 September to 16 October 2026". Suggest dating the observation as a NESO file fact ("from mid-September 2026
   it has kept one issue a day"); within the word budget it should fit by trimming elsewhere. The claim is true and not
   over-claimed as to which update.
3. **nit** `page.record.fields.f_point` and `page.chart_view.key[].note`: the field line pairs `Om`, `DM`, `Dm`, `EM` with
   their meanings unattributed, but this package's own dictionary does not pair them; the key notes attribute to "NESO's
   day-ahead dictionaries" (which means the 1-day, 2-day and 7-day ones, so naming them would be clearer). The writer
   verified `EM` and `Om` only; `DM` and `Dm` are consistent with the sibling windows (`2A` P 830-1200, `3B` T 1330-1630)
   but not tested against a day maximum or minimum. Suggest "(as NESO's 1-day, 2-day and 7-day dictionaries pair them)"
   on the field line or the key note, wording permitting.
4. **nit** `page.chart_view.caption` ("From 25 October the evening peak window is 17:00-18:00, not 18:30-20:00"): states
   raw windows without "as NESO writes them", which the approved 1-day caption carries because NESO's zone is disputed.
   The relative statement is true either way; adding the phrase keeps the two pages consistent.

## Observations (not findings)

- The title "Two-week national demand forecast" reads as a 14-day horizon; the hero line says 2 to 14 days. Seat's call on
  a family naming pattern; the writer already raised it.
- The 16 Oct current file puts target 26 Oct `Om` at 17,303 MW, the series low (a Monday below Sunday's 18,468 and about
  3,000 below Tuesday's 20,316). The archive's morning issue the same day had 18,305 for that date and point. It is
  NESO's published value and the page states it as such; worth putting in the NESO question packet if the seat wants to.
- Not checked: dark mode screenshots; the notebook's outputs were checked from the committed JSON and PNG, not by re-running
  the kernel (inspection only).
