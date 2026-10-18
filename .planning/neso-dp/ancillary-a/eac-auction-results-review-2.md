# EAC auction results (`eac-auction-results`): checker re-review (revision 1)

Checker, 2026-10-18. Focused re-check of `eac-auction-results-author-2.md` against `eac-auction-results-review.md` (2 majors, 9 nits).

## Verdict: REVISE

Both original majors are fixed and ten of the eleven nits are closed. One new major came in with the revision: a rewording turned a
true "mostly four hours" into a false "four hours". It is a one-word fix.

Gates run myself: `gridflow-build --only neso_data_portal/eac_results_summary` succeeds; `detect.mjs --json` returns `[]`; 0 em dashes in
the page; mirror `cmp` equal to the canonical note; series and sample files unchanged (19:43), notebook JSON and PNG re-run at 20:02
(`generated_by: scripts/run_notebooks.py`, 5 cells, no error outputs). Rendered text no longer contains "per delivery day", 17.14, -10.58,
"35 monthly" or "from April 2026".

## New finding

### 1. MAJOR: `delivery_end` now says response windows are four hours; five days are 3 or 5 hours
Field path: `page.record.fields.delivery_end` ("Window end, UTC; four hours for response, half an hour for reserve here").

The original "mostly four hours" was right and the review did not ask to change it (only the EFA claim was a measured universal). Silver
(FY plus current summary): response windows are 38,850 at 4 h, 18 at 3 h (2024-03-31, 2025-03-30, 2026-03-29) and 12 at 5 h
(2024-10-27, 2025-10-26). "Four hours for response" is false for those 30 rows, and the table the guide describes includes them. Fix:
"mostly four hours for response, half an hour for reserve" (still within 14 words).

## Majors from review 1

1. Alt medians: fixed. Alt now says DRL "about 17.1" (true median 17.125) and DRH "median -10.61" (true -10.6115). Recomputed from the committed
   series and from silver: DRL 6.06 (5 April) to 38.07 (24 June), DCL 1.08 to 12.52 (22 September), DCH 0.05 to 7.20, DRH below zero on 190
   days, lowest -16.52 (16 October); all match, series unchanged.
2. "One auction per delivery day": gone from `facts.cadence`, `what_it_is` and `auction_id`; no other place on the page (grep). The replacements:
   - "Daily auctions, and NESO updates the files daily (its package text)": the note quotes NESO's package text ("daily auction results will now be
     published", catalogue snapshot 20261006T195819Z) and the extra "Update frequency: Daily" (note line 1174). Accurate.
   - "shared by the products auctioned together": paraphrase of the NESO dictionary line "All products auctioned in the same market"
     (`field-info/20261008T114228Z/eac_results_summary.json`, `auctionID` description). Accurate, but that sentence is not in the note
     (the note carries only "unique auction identifier"). The source is real; see nit A.

## Nits from review 1

3. Scoping: `what_it_is` is now "In NESO's files current and archives cover separate periods; the daily file repeats current rows: never add it." True (0 shared
   keys current/FY for summary, by unit, buy orders; every daily key in its current table) and scoped. The daily `differs` lines now give advice. EFA claim removed;
   `cleared_volume` "0 means nothing cleared" is a definition; `clearing_price` "0 in the NSR row" is visible in the frame. Closed, except the new finding 1.
4. Notebook lead: now says a delivery day spans two UTC dates, `query()` filters by UTC date, the first query keeps one auction, printed in UK time. Matches the
   code (`timestamp_utc`, `_date_range_predicate`) and the output (`+01:00`). Closed (see nit B on one word).
5. Sell orders: `how_used[1]` now says via `data.sql`, `query()` filters capture time. True (`timestamp_utc == capture_written_at` on every row). Closed.
6. Plot colours: DML bronze `#7C5530`, DRH olive `#66793B`; the new PNG shows DRH olive, DML brown, matching the chart. Closed.
7. Plot alt: now names DML ("second, 2.51 to 10.79", true: second line in all 36 months, rechecked) and "October partial". The cell outputs are unchanged and still match
   my recomputation. Closed.
8. `differs`: "current financial year" and "this month's dump plus monthly archives". Closed.
9. History: "Response from 2023-11-02T23:00:00 (FY2023 archive); NESO puts earlier response in another package". Closed.
10. Body: "Delivery span of each scope" is dated "at the 2026-10-08 capture" and points to Cadence; the "1,080 auction IDs on 1,080 days" it adds is true. `updated` is 2026-10-18. Closed.
11. Notebook tab label at 390: template item, no finding.

## New nits

A. The "All products auctioned in the same market" dictionary line is not in the canonical note; add it to the "Column meanings" `auctionID` text so the page's source is in the vault.
B. Notebook lead: "`data.sql` then joins the FY and current summaries" describes a `UNION ALL`; "stacks" is the accurate word.

## 390 view

Through a 390 px iframe, first screens (hero, facts, what it is, how it's used, chart, key, start of raw feed) fully visible, no overflow; the rewritten
how-used line and Cadence/History facts wrap cleanly. Nothing that sets width changed elsewhere; earlier 390 checks of the frame, notebook and related list still stand.
