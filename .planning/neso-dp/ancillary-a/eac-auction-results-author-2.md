# EAC auction results (`eac-auction-results`): author revision 1

Writer, 2026-10-18, answering `eac-auction-results-review.md` (REVISE: 2 majors, 9 nits).

## Status

`gridflow-build --only neso_data_portal/eac_results_summary` succeeds (only the global "3 line(s) in Known issues"
warning); detector `[]`; 0 em dashes in the page and 0 in the lines I added to the note (the note's original schema
tables carry some). The note has 1,256 lines, all CRLF; the mirror `cmp` is equal. The notebook was re-run because its
plot cell changed (5 cells, no errors). The chart spec and record select are unchanged, so the series and sample digests
still pass. The vault diff against `origin/master` is 190 insertions and 11 deletions.

## Majors

1. **Alt medians** (`page.chart_view.alt`): every alt figure recomputed from the committed series with
   `statistics.median`. DRL median is 17.125 (written "about 17.1", which avoids a half-way rounding), and DRH median is
   -10.6115 (written -10.61). Unchanged and rechecked: DRL 6.06 (5 April) to 38.067 (24 June); DCL 1.077 to 12.523
   (22 September); DCH 0.045 to 7.202; DRH below zero on 190 of 200 days, lowest -16.52 (16 October).
2. **"One auction per delivery day"** is removed from all three places, because NESO states no such rule:
   - `facts.cadence`: "Daily auctions, and NESO updates the files daily (its package text)". The source is the notes'
     "daily auction results" and the extra "Update frequency: Daily".
   - `what_it_is`: "in daily EAC auctions".
   - `record.fields.auction_id`: "NESO's auction number, kept as text; shared by the products auctioned together",
     from the dictionary's "All products auctioned in the same market".

## Nits

3. **Unscoped universals.**
   - `what_it_is` now reads "In NESO's files current and archives cover separate periods; the daily file repeats
     current rows: never add it."
   - `clearing_price`: "signed; 0 in the NSR row, nothing cleared" (the zero is visible in the frame).
   - `delivery_end`: "four hours for response, half an hour for reserve here" (no EFA claim).
   - `cleared_volume`: "0 means nothing cleared" (a definition, not a measurement).
   - The four daily `differs` lines now give advice from NESO's "latest auction only" text ("never add it/them to the
     current table") in place of the measured "repeats rows".
4. **Notebook lead:** "A delivery day spans two UTC dates and `query()` filters by UTC date, so the first query keeps
   one auction (printed in UK time). `data.sql` then joins the FY and current summaries." (32 words.)
5. **Sell orders and `query()`:** `how_used[1]` is now "Sell-order bid stacks (MW against price limit) via
   `data.sql`; `query()` filters capture time". The lead had no room left within its 35-word budget.
6. **Plot colours:** the list is now DCH `#3E8C97`, DCL `#155A6E`, DMH `#AFC64E`, DML `#7C5530`, DRH `#66793B`,
   DRL `#C77E3C`, so DRL, DCL, DCH and DRH match the chart's clay, petrol, horizon and olive.
7. **Plot alt:** now covers DML (second every month, 2.51 to 10.79) and says the last month is partial ("to 17 October
   2026 (October partial)"). Polars (`eac11.py`) confirms DRL is the top line and DML the second in all 36 months.
8. **Stale spans in `differs`:**
   - The summary line now ends "current financial year".
   - Sell orders now read "this month's dump plus monthly archives".
9. **History:** "Response from `2023-11-02T23:00:00` (FY2023 archive); NESO puts earlier response in another package".
   No reserve start dates are given, because no vendor line supports them.
10. **Vault body:**
    - The "Delivery span of each scope" heading is now dated "at the 2026-10-08 capture". It also says the 2026-10-16
      capture extends the dumps to `2026-10-17T21:30:00` and holds 1,080 auction IDs on 1,080 days (`eac7.py`), and
      points to Cadence.
    - Front matter `updated` is now 2026-10-18.
11. **Notebook tab label truncates at 390:** this is a template matter for the seat. Nothing changed here.

## Rendering

All changes are text of the same or shorter length, plus the plot's colours. The rendered page grep finds no "per
delivery day", 17.14, -10.58, "35 monthly" or "from April 2026". "Repeats" now appears only inside the scoped
`what_it_is` sentence. The new plot PNG shows DRH in olive and DML in brown, with the legend above the axes. I did not
re-shoot the four widths, because nothing that sets width changed.

## Defects

Unchanged from `eac-auction-results-author.md` "Defects".
