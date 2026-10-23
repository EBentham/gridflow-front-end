# Review: `day-ahead-power-exchange-prices-nordpool` (table `nordpool_da_prices`)

Checker, Trading batch, 2026-10-23. Port 9864 (server PID 12326, stopped by that PID).

**Verdict: REVISE.** 1 major, 4 nits. No blockers. The chart, clock handling, frame and notebook all reproduce; the one
major is an overclaim about Elexon's market index price.

Build `--only neso_data_portal/nordpool_da_prices`: clean. Detector: `[]`. Mirror `cmp`: identical. 0 em dashes, en
dashes, middle dots or arrows in the `page:` block or the built page. Screenshots at 1440, 1024, 768 and a 390 px
iframe, plus the unfolded frame (the `fx` toggle) and the open notebook drawer: nothing clipped or overlapping (the
unfolded frame scrolls sideways inside its own well, as the template intends).

## Findings

1. **Major** `page.how_used[2]` and `page.related[0].note` (elexon/mid): "A check on Elexon's half-hourly GB market
   index price" and "a check on these hours" overclaim. The mirrored Elexon page (`vault/elexon/mid.md`, `what_it_is`)
   says the market index price is a volume-weighted average of half-hour, one-, two- and four-hour products traded
   within eight hours of the deadline, and that "Day-ahead auction trades carry no weight". So the day-ahead auction
   price is not an input to, and not a like-for-like check on, that series. The canonical note's own cross-check
   (body, "Cross-checks") says the comparisons "do not establish identical products": `APXMIDP` joined 43,679 hours
   with 6 exact matches and a mean absolute difference of about 18.0 £/MWh; `N2EXMIDP` is almost all zeros. The two
   lines also point in opposite directions (this series checks MID; MID checks these hours). Suggested wording: a
   series to compare with Elexon's half-hourly market index price, a different product.
2. **Nit** `page.chart_view.caption`: "Each date runs 00:00 to 24:00 GMT." states a span for the date, which sits close
   to the batch's "never present a composed delivery instant". What the rows support is the label set: every plotted
   date carries the 24 labels `00:00 - 01:00` to `23:00 - 00:00`, which NESO titles "Delivery Period (GMT)".
   Suggested: "Each date carries 24 hourly labels, `00:00 - 01:00` to `23:00 - 00:00`, which NESO gives as GMT."
3. **Nit** `page.how_used[1]` and `page.related[2].note`: "continental" does not fit the ENTSO-E page, whose areas
   (per its mirrored note and the canonical note's cross-check) are Ireland, Germany, Belgium, France and the
   Netherlands; GB returns no data. Ireland is not continental. Suggested: "European day-ahead prices" or
   "ENTSO-E day-ahead prices".
4. **Nit** `page.chart_view.alt`: "105 in 2026" is the median of 2026 up to 16 October, not the year. Say "so far in
   2026" or "2026 to 16 October". The other three yearly medians are full years.
5. **Nit** canonical note body (not on the site): the edit fixing "only one capture" is right and cites evidence,
   but nearby statements still read as present-tense single-capture facts. "The two clocks", point 2 says
   `timestamp_utc` = the capture time `2026-10-08T11:14:21.282381Z`, "Both columns equal it on every row". With the
   second capture, the 16 October file (which holds all 44,472 rows in `_latest`) carries
   `2026-10-16T20:42:05.239349Z`. Cadence says the CKAN `last_modified` precedes "the newest delivery date in the
   body (2026-10-08)"; the newest is now `2026-10-17`. "Delivery-period labels" and "Value range" give 1,845 dates and
   44,255 steps without saying they are the first capture's. Smallest fix: date those sentences to the 8 October
   capture, or give the 16 October figures (1,854 dates, 44,471 steps, 2026-10-17 with 22 rows).

## What I reproduced (all from local silver, Polars, read only)

- **Captures.** 44,256 rows (8 Oct) and 44,472 rows (16 Oct). The later is a strict superset: 44,256 shared keys with
  0 price differences, 216 only in the later, 0 only in the earlier. `(date, delivery_period)` unique in each.
- **Dedup.** After keeping the latest capture per key there are 44,472 rows. Without the guard, the daily means
  differ from the guarded ones by up to 1.56 £/MWh (shared hours counted twice), so the `dedup:` setting matters and
  works. Provenance `duplicates_dropped` 44,254 (44,256 less the two 2021-09-20 rows outside the window) and
  `rows_used` 44,448 (1,852 x 24) both check out.
- **Series.** 1,852 points, 21 September 2021 to 16 October 2026, no missing date. All 1,852 values match my own
  daily means to the series' three decimals (0 mismatches). Peak 574.816 on 2022-08-26, then 570.94 on 2022-12-12.
  Lowest 0.387 on 2025-10-04. 68 days above 300, between 2021-10-15 and 2022-12-16. Yearly medians 90.34, 73.08,
  81.67, 104.56 (2026 to 16 October). Key note and alt text agree with these.
- **Daily mean on clock-change days.** Fair here: every plotted date, including all ten change dates (2021-10-31,
  2022-03-27, 2022-10-30, 2023-03-26, 2023-10-29, 2024-03-31, 2024-10-27, 2025-03-30, 2025-10-26, 2026-03-29), has
  exactly 24 labels, `00:00 - 01:00` to `23:00 - 00:00`. So each mean covers the same 24 labels and 23- or 25-hour
  days never arise. The caveat is that these are NESO's GMT-labelled dates, not UK local days; the page says GMT in
  the caption and the axis label, which is sufficient.
- **Clock.** The page states only NESO's labels (delivery date, one-hour GMT period) and "builds no delivery time".
  `timestamp_utc` = `capture_written_at` on every row of both captures; `published_at` null on all 88,728 rows.
  Registry `temporal: {kind: none}`. Nothing on the page or in the notebook builds an instant. (Finding 2 is the one
  sentence that comes close.)
- **Frame, 26 October 2025.** 24 labels that day, one per hour. The eight rows (00:00 to 08:00) are 0.0, -0.49, -0.58,
  -1.86, -2.45, -1.76, 0.93, 4.79: five below zero, one zero. Matches the caption and the sample file
  (`generated_by: gridflow-sample`). The unfolded frame shows all 11 columns; the guide covers every column except the
  four pipeline ones, key columns first.
- **Notebook** (`scripts/run_notebooks.py`, `data.sql` on `silver_neso_data_portal_nordpool_da_prices_latest`).
  Outputs have no errors. Cell 3 gives the eight rows with `captured_utc` 2026-10-16 20:42:05.239349. Cell 4 gives
  24 labels on 1,852 dates, 2 on 1, 22 on 1, equal to my counts. Cell 5 plot means recomputed: 102.6 (06:00), 77.6
  (12:00), 77.8 (13:00), 129.7 (18:00), 91.2 (23:00); `plot_alt` matches the PNG. The lead is right:
  the designated date column for `nordpool_da_prices` in `gridflow_models`' schema manifest is `timestamp_utc`, and
  `_latest` is `whole_capture` (newest capture wins).
- **NESO's words.** Catalogue snapshot `20261006T195819Z`: resource description "This data file returns the Day-Ahead
  price data published by Nord Pool each day for GB." (the page quotes a substring); package notes "These are
  published in £/MWh"; extras "Update frequency: Daily"; field info `Date` "Delivery Date in YYYY-MM-DD format",
  "Delivery Period (GMT)", `Price` "Auction price for the delivery period ... (GBP)". Resource name ` N2EX GB
  Day-Ahead Price`.
- **Requests and commands.** `package_show?id=` and `https://api.neso.energy/datastore/dump/<resource id>` match the
  sidecar `request_url` and `endpoints.py`; "kept only if its body changed" matches `_dump_member`
  (`body_sha256 == basis.body_sha256` returns `unchanged`); commands and comments are identical in form to the
  approved dump pages (`aggregated-bsad`).
- **Body edits.** The two canonical-note body edits (second capture added under Files, "Only one capture exists"
  changed to two) are minimal and match the bronze sidecar and the Polars comparison above.
- **No local data.** No `locally`, `held`, row counts or coverage figures on the page. The only dated capture reference
  is "from the file captured on 16 October 2026" in the chart caption, which the rubric asks for.

## Observations, not findings

- The writer's report says both capture edges "fall on a UK-day boundary in summer time". They do not: the file
  starts at 2021-09-20 22:00 and the captures end at 21:00 - 22:00, so the edges sit at 22:00 UTC, which is 23:00 BST
  but midnight CEST. It reads like a Nord Pool delivery-day edge converted to GMT labels. This is report-only (the
  page claims nothing from it) and does not change the daily-mean verdict, but the canonical note's sentence that the
  evidence supports "UTC intervals rather than a UK-local or CET/CEST clock" is about the labels, not the day
  boundaries, and may be worth one line of care at the next vendor check.
- Template: the chart key renders the series name followed by the code chip ("Daily mean price" `price`), repeating
  the idea on a single-series chart. Seat item.
