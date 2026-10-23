# Writer report, round 2: STOR day-ahead auction results

Fixes for every finding in `short-term-operating-reserve-stor-day-ahead-auction-results-review.md` (1 major, 5 nits).
Build `--only neso_data_portal/stor_da_auction_results` exit 0 (budgets pass); detector `[]`; 0 em dashes; mirror
`cmp` identical; note CRLF throughout (369/369). Notebook re-run (cell 4 changed). Series and sample unchanged (the
chart spec and record select did not change; build digest check passes).

## Changes

1. **major: overclaim of "every".**
   - `summary`: "Every tender in ..." is now "The tenders in NESO's daily ... auction".
   - `facts.vendor`: "one uploaded CSV of every daily STOR auction result" is now "one uploaded CSV of the daily STOR
     auction results".
   - `facts.history`: "Service days 1 April 2021 to 31 March 2026; NESO's file lacks four".
   - `what_it_is` (59 words) now ends: "NESO's file has no rows for four service days and none accepted on five;
     NESO's notices report two failed auctions." Checked against `as_industry_notifications_stor_important` silver:
     notice of 2024-08-17 08:20Z ("no bids being accepted", effective 2024-08-18 04:00Z; the 18 August 2024 service day
     has 96 tenders, none accepted) and 2025-02-07 11:20Z ("no bids being accepted. There will be no replacement
     auction"; 8 February 2025 has no rows). To make it fit, the sentence "NESO ended the auction after launching
     Slow Reserve" left `what_it_is`; the EAC related note still says it.
   - `related[2].note` now points at those notices: "Mostly STOR auction delays and failures; two explain gaps in these
     results" (also nit 6).
   - Notebook cell 4 now prints the span: service days in the span 1,826; with rows in the file 1,822; with a tender
     accepted 1,817; one clearing price 1,817; clearing = dearest accepted 1,817. So both "four" and "five" are
     visible in the page's own output. The plot cell reindexes to the same `span`.
   - `plot_alt`: "the line breaks where nothing was accepted or NESO's file has no rows".
2. **nit `chart_view.caption`:** "each service day's clearing price, the same on every accepted tender that day in
   NESO's file" (35 words). Measured, scoped to the file; the notebook shows it.
3. **nit `record.fields.service_delivery_from`:** "Service day start, UTC with NESO's `Z`: 05:00 UK time, so 04:00Z in summer".
   `service_delivery_to` unchanged ("05:00 UK time; 23 or 25 hours long at clock changes").
4. **nit `facts.cadence`:** "Daily; last auction 30 March 2026, for delivery 31 March; package Not Active (NESO)".
5. **nit `plot_alt`, one basis:** medians for both periods: "Median 1,312 MW until 1 April 2025, then 1,696 from 2
   April, when NESO's notice raised its requirement to 1,700 MW. Lowest 50 MW on 20 December 2021". Polars: 1,453
   days to 1 April 2025 median 1,312; 364 days from 2 April 2025 median 1,696. Notice of 2025-04-01 08:00Z: STOR
   day-ahead requirement "increased to 1700MW from the auction on 1 April 2025 (for delivery on 2 April 2025)".
6. **nit `related` notices note:** "Mostly ..." (see 1).

## Visual check

Server on 9988 started in the background with its PID recorded (3030, then 3116) and stopped by that PID
(`kill <pid>`, confirmed by a refused request). Shots of the changed hero, prose and guide at 1440 and 390:
`.planning\neso-dp\ancillary-b\stor-da-auction-shots\stor-da-auction-r2-*.png`. Nothing clipped or overlapping.

## Defects

Unchanged; the missing and no-acceptance days are already logged (20v). No gridflow defect.
