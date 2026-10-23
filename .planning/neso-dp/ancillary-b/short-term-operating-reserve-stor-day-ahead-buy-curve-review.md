# Review: STOR day-ahead buy curve (`stor_da_buy_curve`)

**Verdict: REVISE** (2 majors, 4 nits; no blockers).

Checked: build `--only neso_data_portal/stor_da_buy_curve` exit 0 (only the template-wide caveat warning); detector `[]`; mirror `cmp`
identical to the vault note (424 CRLF lines, body untouched: the diff against `origin/master` is 138 added lines, all in `page:`);
0 em dashes, middle dots or arrows in the page and the `page:` block; page viewed at 1440 and 390 (390 through a 390 px iframe) on my
own server on port 9999 (started from Python with its PID recorded, stopped by that PID, port confirmed down): hero, prose, chart,
frame, guide, notebook and notebook plot are not clipped or overlapping, no horizontal scroll at 390. Every number below was
re-derived with Polars (read only) from the one silver capture of each table, the bronze sidecar, the catalogue snapshot
`20261006T195819Z` and the field-info snapshot `20261008T114228Z`.

## Confirmed (no finding)

- **Chart.** Max of `availability_price` per UK service day, 1 April 2025 to 31 March 2026: 365 days, no gaps, min 6.82
  (29 March 2026), max 33.53 (19 March 2026), median 9.83; the committed series equals my values point for point. UTC date equals UK
  date on all 5,475 rows (starts are 04:00Z in months 4 to 9, 05:00Z in months 11 to 2, March and October mix both), so the UTC
  bucket is safe. Alt and key note hold: April to November minimum 7.52, monthly peaks 15.62 to 22.63; December 6.91 to 13.81;
  January peak 26.24 on the 20th; March 6.82 to 33.53. MW is 1,700 on 364 days of the window and 1,260 on 1 April 2025 only (the
  change is on 2 April 2025). `spec_origin: vault`, digest check passes. Caption names dataset, unit, window and aggregation.
- **Notebook step curves.** The four days: 1 April 2021 1,311 MW at 6.78; 1 April 2025 1,260 at 13.08; 16 October 2025 1,700 at
  21.50; 19 March 2026 1,700 at 33.53 (all as `plot_alt`). The plot (vertical at x = MW from 0 to the price, flat at the price from
  the MW back to 0) matches "flat at its price from 0 MW to its MW, then drops to zero". The sort order (price ascending, MW
  descending) is right for all four, including 1 April 2025 whose rows are listed in a different order.
- **One row, one curve.** 5,475 rows = 5,475 distinct `buy_curve_step_id`; 1,825 curves, one per UK service day, three points
  each; 1,825 of 1,825 are {(Q,0), (Q,P), (0,P)} with Q and P non-zero; the only missing day in the 1,826-day span is 17 August
  2022; three curves list their points in reverse (`BCN-00000007`, `-00000176`, `-00001499`). No negative values; 1,825 zero MW
  and 1,825 zero price vertices. Notebook cell 4 output (1,825 four times) is right.
- **Times.** All starts and ends are 05:00 Europe/London; 5,445 rows span 24 h, 15 span 23 h, 15 span 25 h (cell 3 output right).
  28 March 2026 runs 05:00Z to 04:00Z (23 hours; UK clocks went forward on 29 March). `timestamp_utc` = `event_time` =
  `effective_from_date`; `published_at` = `available_at` = 2026-03-30 04:22:46.013246 on every row. `query()`: date column
  `timestamp_utc`, bounds `>= start` and `< end + 1 day` UTC (`_get_method_registry.py` 95-96), so both ends are included;
  session-zone times converted by the cell (output shows 05:00 UK on every row).
- **Per-year table (cell 5).** Re-derived: days 365/364/366/365/365; MW low/high 1310/1640, 1340/1343, 1211/1311, 1210/1313,
  1260/1700; median price 9.01, 16.37, 7.85, 8.14, 9.83; top price 205.48, 250.69, 55.62, 184.62, 33.53; accepted days
  362/362/365/363/365 (1,817); contracted above MW 63/103/158/243/141 (708). All 328 result rows with a blank `buy_curve_id` are
  Rejected, so no accepted tender is dropped by the join.
- **Raw feed.** The second request URL equals the bronze sidecar `request_url`; `package_show` by package name; the hash TXT is
  its own family `stor_da_buy_curve_files` (registry, bronze folder); `--last 24h` matches the approved sibling.
- **Eight rows.** Match silver (`BCS-5632` to `5639`); `generated_by: gridflow-sample`.
- **No local data.** No "locally", "held", "our", row counts or coverage statistics in the `page:` block; numbers are vendor facts,
  code facts, chart values or notebook output. Related notes are 12 words or fewer.
- **No capping claim.** The page says "NESO's maximum MW requirement" (NESO's dictionary words on the price field) and never says
  contracts stay within it. Contracted MW above the curve MW on 708 of 1,817 days, up to 401 MW, confirmed.

## Findings

1. **major** `page.how_used[0]` and `page.notebook.cells[4]`. The curve price is in £/MWh (NESO's column header, "Availability
   Price (£/MWh)"); the results' prices are £/MW/Hr (NESO's dictionary unit entry on both price columns). The page puts them side
   by side: the first how-used line reads "Each service day's price cut-off, £/MWh, beside that day's STOR clearing price" and
   never names the clearing price's unit, and cell 5 computes `clearing <= price` and prints a `clearing_at_or_below` column
   (362 of 362, ..., 365 of 365), the unit caveat living only in a code comment. The canonical note's own body says "do not
   compute a price comparison between the two without stating the conversion" and keeps a `TODO: verify` on how NESO relates the
   curve's £/MWh to the tender £/MW/Hr; NESO gives no relation, so the page acts against the note it renders from. The
   comparison is numerically sensible (the two are dimensionally the same if £/MWh is read as per MW per hour; clearing is below
   the curve price on 1,814 days and equal on 3, never above, median 16% of it) but that is the writer's reading, not NESO's.
   Answer to the writer's open question: not acceptable as it stands. Fix, either: (a) drop `clearing_at_or_below` from cell 5
   (regenerate the notebook JSON; `plot_alt` is unaffected) and reword the how-used line, for example "Each service day's price
   cut-off, £/MWh, read against that day's clearing price, which NESO writes in £/MW/Hr"; or (b) keep the column and say in
   `notebook.lead` that NESO writes £/MWh here and £/MW/Hr on the results and does not say how they relate, so the cell compares
   the figures as written. Either way use NESO's spelling `£/MW/Hr` (the sibling writes "£/MW/h (NESO writes £/MW/Hr)"); the cell
   comment has `£/MW/h` alone.
2. **major** `page.facts.vendor` (and `page.what_it_is`). "one uploaded CSV of every daily STOR buy curve" overclaims: NESO's file
   has no curve for 17 August 2022, which the page's own `facts.history` ("bar 17 August 2022") says two lines below, so the hero
   contradicts itself. This is the same "every" overclaim the sibling's review raised as a major. `what_it_is` "published the buy
   curve used to assess each day" has the same reach. Fix: "one uploaded CSV of NESO's daily STOR buy curves" and, in
   `what_it_is`, "assess the days" or add "(its file has no curve for 17 August 2022)".
3. **nit** `page.what_it_is`, last sentence. "NESO ended it after launching Slow Reserve." follows the hash-file sentence, so "it"
   reads as the hash file. NESO's package notes say STOR day-ahead was decommissioned following the launch of Slow Reserve; say
   "NESO ended the STOR day-ahead auction after launching Slow Reserve."
4. **nit** `page.facts.cadence`. "NESO marks the file Not Active": "Update Frequency: Not Active" is an extra on the package
   (catalogue snapshot `extras`), not on the file; the sibling's review fixed the same wording. Use "NESO marks the package Not
   Active".
5. **nit** `page.record.fields.effective_from_date` (and `effective_to_date`). "UTC as NESO writes it, with a `Z`: 05:00 UK time"
   states one start hour; in summer the served start is 04:00Z (months 4 to 9 are all 04:00Z), and the notebook prints only the UK
   start. The eight rows show both (28 March 05:00Z, 29 March 04:00Z) but nothing says why. Add "04:00Z in summer time" or "the
   `Z` time moves with the UK clock change".
6. **nit** `page.summary`, `page.chart_view.title`, `page.chart_view.key[0].label`, `page.how_used[0]`. The curve's price is
   called "price cut-off" throughout. NESO's words for the field are "Maximum availaibility price associated with maximum MW
   requirement"; "volume and price cut offs" is NESO's description of what the separate hash file commits to. That the curve's MW
   and price are those cut-offs is a reasonable reading, not something NESO's catalogue text states (the assessment-principles PDF
   was not read). Cheapest fix: keep "cut-off" in the hash sentence only and title the chart in NESO's terms ("Maximum
   availability price per service day"), or say once in `what_it_is` that the curve's MW and price read as those cut-offs.

## Not findings

- Template: no dark scheme; notebook tab truncation at 390; unlabeled index column in cell 3 and 5 outputs; the 22-line caveat
  warning; a step or x-y chart type for curves (the writer's template item).
- Writer report only (not on the page): "ratio 0.82 to 1.30" for contracted MW over curve MW is wrong at the low end: my minimum
  is 0.037 (median 1.00, maximum 1.299 as stated, 708 days above 1, up to 401 MW over, all re-derived). Correct it if the figure
  is reused in a vault TODO.
- Defects to log (NESO data, no gridflow fault): no curve for 17 August 2022; three curves listed in reverse point order;
  contracted MW above the curve's "maximum MW requirement" on 708 of 1,817 service days (vault TODO beside the unit-relation
  one). Bronze equals NESO's datastore total, so nothing was lost in gridflow. No gridflow defect found.
