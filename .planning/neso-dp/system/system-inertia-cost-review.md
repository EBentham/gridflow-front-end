# System inertia cost (`system-inertia-cost`): checker's review

**Verdict: REVISE.** 0 blockers, 1 major, 5 nits. Every number on the page reproduces from silver and the build is clean. The
one major is the seat's own condition: the page does not state NESO's unit disagreement plainly. The zero-price gap is stated
plainly.

Checked in `C:\gridflow-wt\fe-neso-sys` (branch `feat/neso-dp-system`) and `C:\gridflow-wt\vault-neso-sys`. Build
`--only neso_data_portal/system_inertia_cost` passes (only the unrelated global warning about 35 dropped Known-issues lines);
detector `[]`; mirror `cmp` clean; no staged chart spec or authored override exists (the underscore-named HTML is the usual
redirect stub); manifest lead is right. Rendered text has no em or en dash, arrow or middle dot (non-ASCII characters are
only the pound sign, the template's apostrophe and ellipsis, and the frame's mu). My server on 9893 was started with the
batch method (shell PID 1858, Windows PID 2480), stopped by that PID, port confirmed free.

## What I reproduced (Polars, silver `system_inertia_cost`, 9 files)

| Check | Result |
|---|---|
| Rows and captures | 3,281 rows, 3,281 distinct dates, 0 null prices; nine Parquet files, one per resource, all written 8 October 2026. Bronze holds one folder (`2026/10/08`) of 10 CSVs and sidecars, no recapture. Bronze row counts equal silver for the nine admitted files (365, 365, 366, 365, 361, 362, 366, 365, 366); the tenth (2026-27) is `Settlement Date,Cost_per_GVAs` plus one data row. Body sizes equal the sidecars' `body_size_bytes` and `declared_content_length` (spot-checked 2024-25: 5,725) |
| Missing dates | Exactly the seven the note lists (2021-11-24 to 26, 2021-12-08, 2022-05-16, 2022-05-17, 2022-08-18) |
| Chart series | Silver 1 April to 30 June 2025, 91 days, equals the committed series element for element; `x` runs 2025-04-01 to 2025-06-30. 61 priced, 30 zero in runs of 5, 1, 1, 6, 3, 4, 2, 2, 3, 2, 1 (one to six). Priced min 1,427 (12 April), max 9,366 (17 June), median 2,969; 15 May 7,714; every day 21 May to 17 June is priced (19 and 20 May, 18 to 20 June are zero) |
| Alt text, key note, caption | Every figure, date and count matches. The 2025-26 file's `published_at` is 2026-04-10 09:06:09.725049 UTC (sidecar `ckan_last_modified` agrees), so "last modified 10 April 2026" is right. `duplicates_dropped` 0, `files` 9, `rows_read` 3,281 |
| Window fairness | The quarter is priced on 67% of days. Across the eight quarters from April 2024 the share runs from 22% to 71%, so this is the second or third most-priced quarter, not the extreme. The 30 zero days are drawn and stated in the key; the notebook's per-year table (7 days above zero in 2017-18 up to 195 in 2024-25, 174 in 2025-26) gives the wider picture. The 58,570 day (25 July) lies outside the window, as the writer says; it appears only in the notebook plot text. Fair enough as a chart; see nit 5 for the one thing it leaves implicit |
| Per-year table | Output equals silver for every row: days 365/365/366/365/361/362/366/365/365 (the query ends 31 March 2026, so 1 April 2026 is excluded), above zero 7/77/87/146/124/131/164/195/174, medians and maxima identical |
| Times | In all 3,281 rows `timestamp_utc` converted to Europe/London is 00:00 on the row's own `settlement_date` (0 mismatches, 0 non-midnight). `event_time` equals `timestamp_utc` and `available_at` equals `published_at` on every row. Code: `casting.py` `date_sp1` calls `settlement_period_to_utc(date, 1)`; `utils/time.py` starts period 1 at 00:00 UK local. Frame: 30 March 2025 00:00 UTC, 31 March 2025 at 23:00 UTC the evening before (spring clock change on 30 March, 2025), 1 April 23:00 UTC the day before; caption right. Notebook output shows the same with `+00:00` after the query cell's `tz_convert("UTC")` |
| Sample frame | The eight rows equal silver on date, price, `timestamp_utc`, `resource_id`, `bronze_capture_id`; the file boundary is on 1 April 2025 (91947c0c to a6a52241). Opened in the browser pane: all 11 columns present behind a horizontal scroll with the fold marker at the end, nothing clipped |
| Raw feed | `package_show?id=system-inertia-cost`; the three download URLs equal the sidecars' `request_url` (2017 `inertia_costs17.csv`, 2025 and 2026 `inertia_costs.csv`) |
| `query()` | Relation from the schema manifest, `settlement_date` is a DATE column so `BETWEEN` has both ends inclusive; `BITEMPORAL_EXCLUDE` drops `event_time`, `available_at`, `source_run_id`, `dataset_version`, so "lineage columns dropped" is right |
| Layout | Browser pane and iframes at 1440, 768 and 390: document `scrollWidth` never exceeds the viewport (1009 of 1024, 1425 of 1440, 753 of 768, 375 of 390); chart, key and frame fully visible, at 390 the chart is 339 px wide with its key beneath |

## The questions you asked

1. **What one row is.** One settlement day from one financial-year file, key `resource_id` plus `settlement_date` (registry
   `entity_key`, `temporal: date_sp1`). The page's method sentence matches NESO's package notes steps 1 to 3 (offers
   tagged inertia summed for the day, shortfall in GVA.s summed over the day's periods, divided) and the worked examples
   (£2,250 and £2,361 per GVA.s). "A rate, not a day's spend" is right. "Whole pounds" follows the integer field type and
   the registry's int64. See finding 1 for the unit wording.
2. **Chart.** Reproduced exactly (table above); notes and alt agree with the series file.
3. **Times.** Correct and scoped to the rows (table above).
4. **Captures.** One per file on 8 October 2026, 3,281 rows across nine files, no repeated dates, the 2026-27 file held at
   resource level (registry `HOLD`, reason matches the page: its one date `01/04/2026` cannot pass the shared ISO format
   and does not settle day or month order). `dedup: {on: [settlement_date], order_by: published_at}` is on both the chart
   and the frame as a guard and drops nothing. The note's conditional overlap (the held row would repeat 1 April 2026,
   which the 2025-26 file already carries as its 366th row) is stated as conditional. Correct.
5. **Outlier and cross-check.** 25 July 2025 is 58,570 per GVA.s; the next five values are 14,650, 14,399, 13,041, 12,694
   and below, so "four times the next highest" (3.998) holds, and 24 and 26 July are zero. The Known issues bullet is
   hedged correctly ("a small denominator could produce it, but nothing inspected says so"; no claim of error). The 128
   disagreements reproduce exactly when spend is tested as non-zero: on the 3,280 dates shared with `constraint_breakdown`
   (latest capture per date), zero price with zero spend 2,117, priced with non-zero spend 1,035, priced with no spend 70,
   zero price with non-zero spend 58 (2,117 + 1,035 + 70 + 58 = 3,280). The one date not shared is 2025-04-08. The count
   is stated accurately in the writer's Defects section and appears nowhere on the public page, which is right. See
   finding 6 for how it should be worded when pasted.

## Seat condition: do both shared gaps appear?

- **Zero days: yes, plainly.** `what_it_is` ends "NESO does not say what a zero means"; the caption adds "The zeros are
  NESO's own values"; the key says "zero on 30 of 91 days". Nothing on the page explains or guesses a meaning.
- **Unit text: not plainly** (finding 1). The page says "£ per GVA.s (NESO writes £ per GVAs)". That reads as a spelling
  remark, not as NESO disagreeing with itself.

## Findings

1. **major** `page.what_it_is` (also `page.record.fields.cost_gbp_per_gvas`, `page.chart.unit`): the seat's condition that the
   page state NESO's unit disagreement is not met. NESO uses three forms for this one quantity: the package notes open with
   "(in £ per GVAs)" and then use "£/GVA.s" in step 3 and in both worked examples; the field dictionary's unit is
   "£ per GVAs" while its description says "(£ per GVA)" (`field-info\20261008T114228Z\system_inertia_cost.json`;
   catalogue snapshot `20261006T195819Z`, `notes`). The page prints "£ per GVA.s" everywhere and mentions only that "NESO
   writes £ per GVAs". A reader cannot tell that NESO's own text varies, that one variant drops the time dimension (GVA
   against GVA.s), or why the page chose GVA.s. The held sibling page is held for exactly this. Suggested replacement of
   the parenthesis, within budget: "NESO's own text varies: £ per GVAs in the field unit, £ per GVA in its description,
   £/GVA.s in the worked method; this page uses £ per GVA.s, the unit that method gives." The writer's report also says
   "the package notes write £/GVA.s", which omits the notes' opening "£ per GVAs".
2. **nit** `page.raw_feed.note` and `.commands[0].comment`: "The 2026-27 file is not loaded" sits beside a request list
   whose third URL is that file and a command comment "every yearly file to bronze". The file is downloaded (bronze holds it,
   `raw_20261008T113816Z_6295f4ed..._1f7fa566.csv`, 45 bytes, one row) and only held back from silver. Say "downloaded but not read into silver". The approved sibling pages also keep "window must end recently"
   on the ingest comment (ingest refuses a window ending more than 48 hours ago, `client.py`
   `_assert_window_admissible`); here it is dropped. Optional.
3. **nit** `page.notebook.plot_alt`: "then near 3,000 to 4,000" overstates how tight the later years are. From April 2023 to
   March 2026 only 202 of 533 priced days (38%) fall in 3,000 to 4,000; 437 (82%) fall in 2,000 to 5,000; median 3,454,
   5th to 95th percentile 1,812 to 5,853. Suggest "mostly between about 2,000 and 5,000". The other two ranges hold
   ("mostly" 1,000 to 3,000 to March 2021: 71%; 5,000 to 10,000 from October 2021 to March 2023: 66%; image viewed and agrees).
4. **nit** `page.how_used[2]`: "How many days each financial year carry a price above zero." is a question, not a use, and
   "year carry" should be "year carries". Suggest "Counting the days each financial year that carry a price above zero."
5. **nit** `page.chart_view.caption`: nothing on the chart says that other quarters are priced less often (22% to 71% over
   the last eight quarters) or that a 58,570 day sits just outside the window. The notebook text covers both, so this is
   optional: one clause such as "Other quarters have more zero days." would stop the quarter reading as typical.
6. **nit** writer's report, Defects (not public): the third item says 128 dates "disagree" with the constraint
   breakdown. The count is right, but the two tables are not defined to coincide (price: accepted offers tagged inertia over
   shortfall; breakdown: spend on actions raising synchronous generation, `increasing_system_inertia_cost_gbp`, which has 8
   negative values), so when pasted into the backlog it should say "non-zero" rather than "with spend" and frame it as a
   question for NESO, not an error in either table. Worth adding for the 25 July question: that day's constraint-breakdown
   inertia spend is £16,170 (27 MWh) against £133,709 on 27 July; a small spend fits a small shortfall behind the
   58,570 but does not prove it.

Also noted, body only, not public and not a finding: the Units bullet says "the legacy dictionary's description omits the
's' in one phrase". The snapshot shows the epoch-2 field description itself ("2026" resource) reads "(£ per GVA)", so the
attribution to the legacy dictionary is imprecise. Fix with finding 1 if the note is touched again.
