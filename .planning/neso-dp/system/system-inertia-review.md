# System inertia (`system-inertia`): checker's review

**Verdict: APPROVE.** 0 blockers, 0 majors, 3 nits. Every number on the page reproduces from silver.

Checked in `C:\gridflow-wt\fe-neso-sys` (branch `feat/neso-dp-system`) and `C:\gridflow-wt\vault-neso-sys`. Build
`--only neso_data_portal/system_inertia` passes (only the unrelated global warning about 35 dropped Known-issues lines);
detector `[]`; mirror `cmp` clean; note is 281 lines, all CRLF; no dash, arrow or middle dot inside the `page:` block or
the rendered page; no staged spec or authored override exists; manifest lead (`system-inertia` to `system_inertia`) is
right.

## What I reproduced (Polars, lazy, silver `system_inertia`, 10 files)

| Check | Result |
|---|---|
| Chart series vs silver | Daily `min` per settlement date, 1 Apr 2025 to 31 Mar 2026: 365 days, both series equal the committed series file element for element, `x` equal too. 17,520 window rows (= `rows_used` 35,040 over two columns); `duplicates_dropped` 0 |
| Outturn lows | 107 (21 Feb 2026) to 252 (5 Jan 2026), median 125 |
| Market-provided lows | 71 (4 May 2025) to 248 (5 Jan 2026), median 101 |
| Outturn higher | 354 days; lower on 4 (2025-10-13, 2025-11-07, 2026-01-19, 2026-03-07, by 1 to 4); equal on 7 |
| Alt text, key notes, caption | All figures, dates and the 354 of 365 match. Window, unit, aggregation and file date (last modified 20 May 2026) match the spec and the sidecar |
| Notebook plot alt | "107 to 150 on most days" (288 of 365 are 150 or under); October peak 228 (14 Oct); January 252; market "often 75 to 100" (171 of 365); meets at peaks (252/248, 228/218). Image viewed, agrees |
| Periods per day | Window: 363 at 48, one at 46 (30 Mar 2025), one at 50 (26 Oct 2025); notebook output says the same |
| Clock | Every spring day 2018-2026 has 46, every autumn day 2017-2025 has 50, except 2022-10-30 (periods 1 and 2 only). 2017-03-26 and 2026-10-25 are outside coverage. Sorted `timestamp_utc` steps: 162,402 gaps of 30 min, 20 of 1,410 and one of 1,470 (the 21 short days); no repeated instant over 162,424 rows |
| Frame, 26 Oct 2025 | Period 1 = 2025-10-25 23:00 UTC, 2 = 23:30, 3 = 00:00, 5 = 01:00, 6 = 01:30, 49 = 23:00, 50 = 23:30 on 26 Oct; values 120/89 etc. equal silver. Spring day 30 Mar 2025: 46 periods, 00:00 to 22:30 UTC. Code path `utils/time.py` `settlement_period_to_utc` (step applied to SP1's UTC instant) via `casting.py` `sp_pair` |
| Lineage | `event_time` = `timestamp_utc` and `available_at` = `published_at` on all rows; sidecar `ckan_last_modified` 2026-05-20T10:37:49.212185 = frame `published_at`, read as UTC per the code's D-15 comment in `_bronze.py` |
| Unfolded frame | Opened in the browser pane: all 13 columns present, 8 rows, horizontal scroll, "…" end column, nothing clipped; the guide covers the key columns, `timestamp_utc`, both inertia columns, `published_at`, `bronze_capture_id`, `capture_written_at` and skips only `event_time`, `available_at`, `source_run_id`, `dataset_version`, as the approved pages do |
| Notebook JSON | Written by `scripts/run_notebooks.py`; six cells, no errors, read-only; outputs equal silver (index 9984 = 208 days x 48, period 1 at 23:00 UTC). Lead matches `query()`: relation `silver_..._latest`, `settlement_date` DATE so `BETWEEN` both ends, lineage columns excluded |
| Raw feed | Request URLs equal the bronze sidecars' `request_url` (package 8f3cd0ce, resources 096d2e9f and 3ff8b466, `inertia.csv`); commands and note wording match the approved NESO pages |
| Layout | Browser pane at 1440, iframes at 1440/1024/768/390: document `scrollWidth` never exceeds the viewport; chart, key, frame and guide checked at 1440 and 390, nothing clipped. Detector `[]` |

## The questions you asked

1. **Chart:** reproduced exactly; notes and alt text agree with the series file. The five low-outturn days and the 21
   two-period days lie entirely outside the window (window lows start at 107; none of the 21 dates falls in April 2025
   to March 2026), so neither appears on the chart or in the frame.
2. **One row / NESO's words:** one settlement period of one settlement date from one yearly file, key `resource_id`,
   `settlement_date`, `settlement_period` (registry). "Market-provided" paraphrases NESO's field text ("calculated in the
   same way as the outturn inertia but with the position of the generators recalculated to remove the impact of actions
   taken by NGESO", listing Trades and Bid Offer Acceptances) faithfully; the Stability Pathfinder exclusion, the
   "temporarily paused" note and "Weekly" are all in the package text. NESO's unit string is `GVAs`; the page prints GVA.s
   and says "NESO writes GVAs" once, which agrees with the sibling inertia-cost note.
3. **Clock:** correct and scoped; the caption and guide state the convention, the numbers come from the rows shown.
4. **Body edits:** all three verified against silver and each is the smallest span.
   - Sparse days: all 21 carry only periods 1 and 2; 2022-10-30 is the 2022-23 one. True.
   - Period range: "except 2022-10-30" is true.
   - Whole low days: 2022-03-19, 2022-06-08, 2023-01-05, 2023-09-30, 2026-06-01 have outturn below 100 in 48, 46, 48, 46,
     46 periods; day lows 50, 54, 52, 44, 43 ("43 to 54" right); neighbouring days' lows are 109 to 207 ("109 to 207"
     right). They are a clean cluster: the next-worst day has 14 periods below 100. Market-provided lows 51, 72, 52, 49,
     59 match the Defects text. Neutral wording ("NESO gives no reason") and a TODO.

## Findings

1. **nit** `page.how_used[0]`: "how far NESO's actions lifted them above the market outcome" states a direction. The
   data do not support "always": outturn is below market-provided in 13,616 of 162,424 periods (769 of 17,520 in the
   chart window) and on 4 chart days' lows; NESO and the note body say the actions "added or removed". Suggest "how far
   NESO's actions moved them from the market outcome".
2. **nit** note body, "Units and value semantics": "Clock-change days carry 46 or 50 periods; ordinary days 48" was left
   unedited (the writer flagged it) and now disagrees with the two edited bullets. Add the same "except 2022-10-30"
   clause for consistency. Not on the public page.
3. **nit** `page.record.fields.outturn_inertia` and `market_provided_inertia`: "GVA.s (NESO)" attributes the spelling to
   NESO, who write "GVAs". Harmless given the "NESO writes GVAs" line in `what_it_is`; optional.

## Not findings

- Notebook panel cell numbers differ from the runner's (setup cell, help card), already a seat item.
- `chart_view.y_min: 60` leaves the axis floor unlabelled below 100; reads fine.
- Unverified by me: NESO's reason for the low and two-period days, and whether NESO revises closed years (one capture each).

## Process

My server: PID 32984 on port 9892 (started with the batch method, output to /dev/null), stopped by that PID only after
confirming its command line. No file written except this review. No git writes, ingest or live API.
