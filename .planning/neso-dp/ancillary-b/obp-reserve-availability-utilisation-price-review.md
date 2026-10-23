# Review: `obp-reserve-availability-utilisation-price` (lead `obp_reserve_avail_price`)

Checker, 2026-10-23. **Verdict: REVISE.** 0 blockers, 1 major, 3 nits.

Gates run: `gridflow-build --only neso_data_portal/obp_reserve_avail_price` ok (only the vault-wide "22 lines dropped"
warning); detector `[]`; mirror `cmp` clean; no em or en dashes, arrows or middle dots in the rendered page; none of the
forbidden words (the "rows" hits are the frame caption, the guide and notebook source). Screenshots at 1440 and 390 (390
through a 390 px iframe): chart, legend, frame, guide and notebook panel fully visible, no horizontal scroll. My port 9996
server is stopped.

## The four points you asked about

1. **Service labels.** NESO does decode them, just not on this package. Catalogue snapshot `20261006T195819Z`
   (`gridflow\.planning\research\neso-snapshots\20261006T195819Z\catalog-snapshot.json`):
   - `quick-reserve-auction-requirement-forecast`, resource description: "Quick Reserve, separated into Negative Quick
     Reserve (NQR) and Positive Quick Reserve (PQR)".
   - `slow-reserve-requirement-forecast`, notes: "Slow Reserve, separated into Negative Slow Reserve (NSR) and Positive Slow
     Reserve (PSR)".
   So `NQR` = Negative Quick Reserve is NESO's own wording, and the chart and key labels (Positive Slow, Positive Quick,
   Negative Quick Reserve) match the source; they are not inferences. This package's own dictionary and notes do not decode
   them (field-info snapshot `20261008T114228Z`: Service ID example "PQR, NQR, PSR, NSR", nothing more). Silver agrees with
   the signs: `NQR` carries only -1, `PQR` and `PSR` only +1 in both captures. The page's "NESO ... decodes none" is wrong
   (finding 1).
2. **Chart.** Reproduced from silver (both captures, 310,704 rows; dedup on the entity key keeping the newest `published_at`
   leaves 160,395; filter `availability_power > 0`; mean `utilisation_price` per UTC day by service; `time_from` from 1 July
   to 15 October 2026 inclusive). 103,143 rows used (matches the series provenance). Every one of the 3 x 107 points equals
   the committed series to within 0.0005 (rounding); min, max and count in the alt text and key notes all match (slow
   171.48 to 322.327, quick 200.118 to 240, negative 154.286 to 300). No row is counted twice: without the dedup the window
   would use 197,402 rows and daily means move by up to 1.84 GBP/MWh, so the spec's dedup is doing real work. The frame
   selection dedups the same way, and the notebook reads `_latest`, one capture. The 16 October file is a strict superset:
   0 of 150,309 earlier keys missing, 0 differences in `time_to`, MW or price, 10,086 new rows, all starting after 12:00 UTC
   on 8 October; 0 duplicate keys inside either file.
3. **Times.** The claim is scoped to what the rows show. On 29 March 2026 (UK clocks 01:00 to 02:00) silver has windows
   starting 00:30, 01:00, 01:30 and 02:00 UTC, 3 rows and 3 units each, so the text cannot be UK local time; 26 October 2025
   has 48 windows and 0 duplicate keys. Every `time_from` is on :00 or :30; `time_to` minus `time_from` is 1,800 s in every
   row. NESO's dictionary gives unit "UTC" with examples ending `Z` (the CSV text has no `Z`), so "Times are UTC, NESO says;
   the text has no zone marker" is true as worded. Notebook outputs print `+00:00` after `tz_convert("UTC")` and equal
   silver (cells 4 and 5 reproduced; the 14 October MW sums reproduce and the `plot_alt` numbers fit them). The file-name
   number (27, 46) is the UK settlement period of the last window read as UTC: correct arithmetic (13:00 BST is period 27,
   22:30 BST is 46); it sits in the note body only, marked not documented.
4. **Units, signs, extremes.** MW for `availability_power` and GBP/MWh for `utilisation_price` are NESO's dictionary units;
   "no sign stated" is accurate (no sign comment on the price). The `pair_id` comment is NESO's. The ±10,000 rows are all on
   0 MW: `NQR` -10000 on 75 rows (EDFE-8 37, EDFE-11 38), `PQR` 10000 on 37 (EDFE-11), 18 to 25 November 2025. Inside the
   chart window no row is at that size, and MW > 0 prices there run 108 to 2,599.04, so nothing at ±10,000 reaches the chart
   or can distort it. All 1,194 negative prices are `NQR` (75 of them the -10000 rows). The note's other counts reproduce:
   74 of 85 instruction STARTs match a declaration with an equal price, 21 of 24 units, 60 rows after the 16 October vintage.

## Findings

1. **major** `page.record.fields.service_id`: "`PQR`, `NQR` or `PSR` in this file; NESO also lists `NSR` and decodes none".
   False: NESO spells out all four codes in the catalogue text of the Quick Reserve and Slow Reserve requirement forecast
   packages (quotes above), and both are among this page's related datasets. Suggested line: "`PQR`, `NQR` or `PSR` in this
   file: Positive Quick, Negative Quick and Positive Slow Reserve in NESO's forecast notes; `NSR` is its Negative Slow
   Reserve" (trim to the field budget). The key labels, chart and `what_it_is` are fine as written. Same correction in the
   note body: the `service_id` bullet ("The vendor text does not expand the codes ... `TODO: verify` against a vendor
   definition") and the Holds paragraph ("`PQR`/`NQR`/`PSR`/`NSR` code definitions"): say the codes are decoded in the two
   forecast packages' text and not in this package's dictionary; drop the TODO or narrow it to "no definition inside this
   package".
2. **nit** `page.notebook.lead`: "cell one converts to UTC". On the page the setup cell is [1] and the conversion is [2] in
   the preview and [3] in the full notebook. Suggest "the first query cell converts the time columns to UTC".
3. **nit** Note body, Columns section: "Service IDs in the capture: `PQR` 58,384 rows, `NQR` 18,381, `PSR` 73,544", "`pair_id`
   `1` in 131,928 rows and `-1` in 18,381", "60 distinct IDs", and the zero-MW and zero-price counts describe the 8 October
   capture only; the note now has two. Say "in the 8 October capture" (after dedup the 16 October file has `PQR` 60,000,
   `PSR` 81,518, `NQR` 18,877). The ranges bullet (0 to 55 MW, -10000 to 10000) holds for both.
4. **nit** `page.chart_view.key[0].note` / caption: the Positive Slow Reserve peak of 322.33 on 18 July is a mean over 550
   half-hours whose prices run 157.08 to 2,042.09 (median 190.85), so a few high offers lift the line well above the usual
   170 to 250. The caption already says "unweighted by MW"; if the budget allows, a clause such as "a few offers near 2,000
   lift 18 July" tells a reader why that day spikes. Optional.

## Not findings

- The folded frame at 390 px showing two columns and the clipped notebook tab label are listed template items.
- The writer's report line "NESO never decodes `PQR`, `NQR`, `PSR`" and the "inferred" fallback in its Unverified list are
  superseded by finding 1; do not carry "inferred" into the ledger.
- The seat item the writer raised (distil and sample read every silver capture of a `whole_capture` table) is confirmed:
  94,259 duplicates would be double counted; this page is correct because its spec dedups.
