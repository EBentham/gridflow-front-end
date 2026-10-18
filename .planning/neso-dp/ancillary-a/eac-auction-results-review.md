# EAC auction results (`eac-auction-results`): checker review

Checker, 2026-10-18. Rubric `.planning/v5/review-rubric.md`; brief `.planning/v5/author-brief.md` (worktree copy, "Family pages").
Inspection only. Writer's report: `eac-auction-results-author.md`.

## Verdict: REVISE

Two majors, nine nits, no blocker. The data work is sound: the chart reproduces from silver on all 800 points, the three file
shapes are as the page says, the dedup is honest, and all four body corrections are true. The majors are one wrong number in the
chart alt text and one measured property stated as a vendor fact.

Gates I ran: `gridflow-build --only neso_data_portal/eac_results_summary` succeeds (only the global "3 line(s) in Known issues"
warning); `detect.mjs --json` on the page returns `[]`; em dashes in the page 0 (and 0 in the lines the writer added to the
note); mirror `cmp` equal to the canonical note (1,256 of 1,256 lines CRLF). Page grep for `locally`, `held`, `our `, `since 20`,
`% of`, `live`, `real-time`, `planned`, `soon`, middle dot, arrow: clean (the one numeric hit, "190 of the 200 days drawn", is read
from the chart). Notebook JSON is `generated_by: scripts/run_notebooks.py`, 5 cells, no error outputs; sample is
`generated_by: gridflow-sample`; series is `spec_origin: vault`.

## Findings

### 1. MAJOR: the chart alt gives two "medians" that are not the medians of the plotted series
Field path: `page.chart_view.alt`.

The alt says DRL "has the highest median, 17.14" and DRH has "median -10.58". The committed series gives different medians.

Evidence (committed `series/neso_data_portal/eac_results_summary.json`, 200 daily means per series, and an independent Polars
recomputation from silver, which matches all 800 points to 0.0004):
- DRL: median 17.125 (rounds to 17.12 or 17.13), not 17.14.
- DRH: median -10.6115 (rounds to -10.61), not -10.58.
- The writer's `eac4.py` takes the figure from `describe()`, which reports a nearest-rank value (one of the two middle days)
  rather than the median of an even count. 17.14 and -10.58 are each the upper of the two middle values.
- The other numbers in the alt are right: DRL 6.06 on 5 April to 38.07 on 24 June; DCL 1.08 to 12.52 (22 September); DCH 0.05 to
  7.20; DRH below zero on 190 days, lowest -16.52 on 16 October.

Rubric section 2 requires every number in the alt to match the committed series; the writer's report says they match "to the third
decimal", which is true for the extremes but not for these two. Fix: "median 17.13" and "median -10.61", or drop the medians and
say "around 17" and "around -10.6".

### 2. MAJOR: "one auction per delivery day" is presented as a vendor fact; it is a measurement
Field paths: `page.facts.cadence`, `page.what_it_is`, `page.record.fields.auction_id`.

Three places say one auction per delivery day. The canonical note itself says, in "Delivery span of each scope", that this is "a
measured property, not a vendor guarantee" (K-AS-3 FACTS 3.5). NESO's text supports "daily" and the `auctionID` description says
"all products auctioned in the same market" share an id; neither says one auction a day.

Evidence (silver, FY summary plus the current summary, current deduped on the key): 1,080 auction ids on 1,080 consecutive
delivery days from 2023-11-03 to 2026-10-17, no id on two days, no day with two ids. True of these files today, not a rule. The
rubric (section 1, last bullet) allows an "always/every" statement only as a vendor or code rule, or scoped to what the page
shows. A second auction on a day (a rerun, a mock-style correction) would make the cadence line and the field guide wrong, and
`auction_id == "2906"` in the notebook is only safe because of it.

Fix: cadence "Daily auctions (NESO)", and in the field guide "NESO's auction number, kept as text; no day has two in these
files" (14 words or fewer), or drop the universal.

### 3. NIT: other measured universals carry no scope
Field paths: `page.what_it_is`, `page.record.fields.clearing_price`, `page.record.fields.delivery_end`,
`page.family.members[2,5,8,10].differs`.

All reproduced and true today, none a vendor rule:
- "Current and archive files share no rows; the daily file repeats current rows": 0 shared keys between current and FY for the
  summary (126,684 incl. two captures against 92,728), by unit (1,517,450 against 1,900,738) and buy orders (145,786 against
  323,894); the sell dump shares 0 of 31.7M archive keys; every daily key is in its current table for all four tables; the
  two daily captures share no key with each other. The current and FY files also meet with no gap (FY ends delivery start
  2026-03-31T21:30, current starts 2026-03-31T22:00). The page says this plainly and never suggests adding a daily file, as asked.
  But a month-end move of sell rows into an archive, or NESO re-cutting the financial year, would change it (the note's own
  TODO). Say "in NESO's files today" or word it as a rule for the reader ("never add a daily file to its current table"), which is
  advice and needs no measurement.
- "0 where nothing cleared" (`clearing_price`): 0 of 6,706 FY and 0 of 32,521 current zero-MW rows have a non-zero price. True, measured.
- "response windows are EFA blocks": the note says window edges match the EFA boundaries with 0 mismatches, a measurement.

### 4. NIT: notebook lead explains the filter but not why, and the output is in UK time
Field path: `page.notebook.lead`.

The lead says `query()` filters `timestamp_utc` "by UTC date, so the first cell keeps one auction". Verified in code: gridflow_models
`_DATE_COLUMN_BY_DATASET["eac_results_summary"] == "timestamp_utc"`, relation `silver_neso_data_portal_eac_results_summary_latest`,
`_date_range_predicate` is `>= start 00:00Z AND < end+1 00:00Z`, and the registry gives `timestamp_utc` = `delivery_start`. So 16 to 17
October returns auction 2906 (starts 16T22:00Z to 17T18:00Z, fully inside) plus the windows of 2905 that start on 16 October UTC,
and `auction_id == "2906"` is the right cut. The selection is correct. Two gaps for a reader:
- It never says a delivery day crosses two UTC dates, which is the reason a date window mixes auctions.
- The cell output prints `2026-10-16 23:00:00+01:00`, UK time (the 22:00Z window), while the lead and the frame speak of UTC.
Fix: "A delivery day spans two UTC dates, so a date window also returns part of the neighbouring auction; the first cell keeps auction
2906. Times print in UK time." Also say the first cell reads the current table only.

### 5. NIT: the page offers sell-order bid stacks but says nothing about how `query()` treats that table
Field paths: `page.how_used[1]`, `page.notebook.lead`.

`eac_results_sell_orders` is temporal `none`: `timestamp_utc == capture_written_at` on every row (checked on the 2026-10-08 dump,
588,221 rows, and the 2026-10-16 dump, 1,259,746 rows, 1 distinct value each). A `query()` date window therefore returns all rows
or none (up to 33.5M), not a delivery window. The notebook never touches sell orders, so nothing on the page is wrong, but the
how-used line invites it. One clause in the lead: "For sell orders use `data.sql`: `query()` filters on capture time."

### 6. NIT: the notebook plot paints DRH and DML with colours that mean something else in the chart above
Field paths: `page.notebook.cells[2]` (colour list), `page.notebook.plot_alt`.

The chart above paints DRH olive (`#66793B`). The notebook plot uses the order DCH, DCL, DMH, DML, DRH, DRL against
`#3E8C97, #155A6E, #AFC64E, #66793B, #7C5530, #C77E3C`, so DML is olive and DRH is the brown `#7C5530`. DRL, DCL and DCH agree. Swap the
fourth and fifth entries (DML bronze `#7C5530`, DRH olive `#66793B`) and the colours stay constant across the page.

### 7. NIT: the plot alt describes five of the six lines, and the last month is partial
Field path: `page.notebook.plot_alt`.

Reproduced in Polars (FY plus deduped current, response rows, monthly mean by UTC month of `delivery_end`): DRL 6.53 (2024-03) to 19.63
(2026-09) and highest every month; DRH below zero every month, -0.31 (2025-06) to -11.40 (2026-05); DCH, DCL and DMH between -1.43
(DMH 2026-05) and 5.37 (DCL 2025-01). All true. DML (2.51 in 2024-02 to 10.79 in 2026-09, the second highest line in every month) is
not described. October 2026 in the last row and in the plot is a part month (to the 17th); neither the lead nor the alt says so.
The cell 4 outputs (2023-11, 2024-11, 2025-11, 2026-10 rows) all match my recomputation.

### 8. NIT: time-bound counts and spans in `differs` go stale
Field paths: `page.family.members[0].differs` ("from April 2026"), `members[9].differs` ("35 monthly archives").

Both true now (the current dump starts at 2026-03-31T22:00Z; the sell archives run `202311` to `202609`, 35 files). Both change on a schedule
(next financial year, next month end). Prefer "from the start of the current financial year" and "one archive per month".

### 9. NIT: the reserve products join the auction later than the history line suggests
Field paths: `page.facts.history`, `page.what_it_is`.

"From 2023-11-02T23:00:00" is right for the table and for response. Silver first appearances: response 2023-11-02, Quick Reserve
2024-12-03, Balancing Reserve 2025-10-29, Slow Reserve 2026-03-31. The page's present-tense "response and reserve ... in one auction"
and a single history date read as if all six services run from 2023. Only the response start has a vendor basis (NESO's note); keep
to "response from 2023-11-02T23:00:00" and leave the reserve dates out unless a vendor line is found.

### 10. NIT: vault body left partly stale beside the new second-capture text; front matter date not moved
Field path: canonical note, "Delivery span of each scope", and front matter `updated`.

The writer corrected four capture statements (below, all true) but the paragraph just above Cadence still reads as current:
current dumps "to `2026-10-08T21:30:00`", "1,071 auction IDs and 1,071 delivery days", sell dump "(8 auctions)", daily files
"`2026-10-07T22:00:00` to `2026-10-08T21:30:00`". After the 16 October capture these are 1,080, delivery to 2026-10-17, and a daily file on auction 2906.
Either date-stamp the paragraph ("at the 2026-10-08 capture") or update it. `updated: 2026-10-13` is unchanged; the note was edited on 2026-10-18.

### 11. NIT: notebook tab label truncates at 390 (template)
Field path: rendered notebook panel (`eac_results_summary.ipynb`).

Through a 390 px iframe and in the pane at 390 the tab reads `eac_results_summary.i...`. Not the writer's to fix; the filename
is fixed by the dataset key. A template matter for the seat if it should not truncate.

## What I checked and found correct

### Chart (your item 1)
- Series reproduces from silver on all 800 points (max difference 0.0003, the series rounding). Days spot-checked by hand: 5 April
  (DRL 6.06, DRH 7.053), 24 June (DRL 38.067, DCH 7.202), 3 May (DCL 1.077), 16 October (DRH -16.52) and 17 October (DRH -15.21).
- Aggregate: mean of six four-hour windows per product per day (n = 6 for every product and day, 200 days). "Daily mean" is a fair reading for a
  price that is one uniform value per equal-length window, and the caption states it ("each day's mean of its six four-hour windows").
  Inside the window every block is four hours (the clock changes are 29 March and 25 October). No zero-MW windows exist for the four
  plotted products, so the BR showcase's "0 price where nothing cleared" trap does not apply here.
- Day convention: `time: delivery_end`, bucket 1d. The UTC date of `delivery_end` equals the 23:00-to-23:00 UK day on every
  response row (38,880 rows, clock-change days included, which I re-derived). The caption and x label state the day and that
  NESO's times are UTC; NESO's own wording for a delivery day matches (auction 2661 is 1 April, starting 22:00Z on 31 March).
- Units: NESO's field info (`.planning/research/neso-snapshots/field-info/20261008T114228Z/eac_results_summary.json`): `clearingPrice`
  unit "£/MW/h", `clearedVolume` unit "MW". Vendor facts, not a project check.
- Four-colour limit: DM is off the chart; the caption says "Dynamic Containment and Regulation only (the notebook has all six
  products)" and the key names the four products drawn. Accepted per the seat ruling.

### Dedup and the 2026-10-16 capture (your item 3)
- The silver summary holds two captures (61,884 rows on 2026-10-08, 64,800 on 2026-10-16). The chart's 9,384 matched rows reduce to
  4,800 after dedup on `auction_id, auction_product, delivery_start`, newest capture last: 4,584 copies dropped, which is exactly the
  191 earlier days x 24 rows. 0 of the 4,584 keys differ in `clearing_price` between captures, so the dedup removes identical copies and
  changes no value. The page says nothing about captures (no local data), which is right; the spec carries the dedup openly.
- Body correction 1 (the 16 October refresh captured the four dumps and four daily files again, skipped 44 archives): gridflow
  `.planning/phases/v0.22-close/refresh-20261016/ingest.log` lines 136 to 146 show 1 ingested for each of the four dumps and four daily
  files and "3 unchanged" for each FY family and "35 unchanged" for sell orders (9 + 35 = 44). True.
- Body correction 2 (every earlier key kept with identical values; dumps extended, not re-trimmed): I compared capture 1 to capture 2
  on every non-lineage column: summary 61,884 of 61,884, by unit 1,444,630, buy orders 139,306, sell dump 588,221 on key and on status, quantity,
  price limit, executed quantity, clearing price and acceptance ratio: 0 keys missing and 0 value differences in each. Newest delivery
  start in each is 2026-10-17T21:30. The sell dump starts at 2026-09-30T22:00 in both captures and shares 0 keys with the 31.7M
  archive rows. The daily files each hold one auction (2865 on 8 October, 2906 on 16 October) with no key in common between
  captures, for all four daily tables.
- Body correction 3 (3-hour and 5-hour rows are the clock-change days): response windows are 38,850 x 4 h, 18 x 3 h, 12 x 5 h. The odd ones are
  block 1 (starts 23:00 UK) of delivery days 2024-03-31, 2025-03-30, 2026-03-29 (3 h) and 2024-10-27, 2025-10-26 (5 h), six products each. True.
  Reserve is 118,648 rows all 1,800 s.
- Body correction 4 (two captures so far, no earlier row changed or dropped from a dump; archives one capture): consistent with the
  above and with the sell archives having one capture each (37 sell files: 2 dump captures plus 35 archives).

### The three shapes (your item 2)
Read the page for any suggestion of adding or joining wrongly: none. The summary's FY archives end where the current table begins; the
notebook unions them (`UNION ALL`) because they are disjoint, and says so. The daily files are described as repeating the current rows.
FY plus current is 1,080 auctions on 1,080 consecutive days with no gap. `_latest` is the newest whole capture, so cell 4 does not double count
the pre-8 October rows (relations are one capture per table; FY is resource aware).

### Facts, requests, commands, local data
- All 19 member request URLs equal a bronze sidecar `request_url` for their family (script check, 0 mismatches); the `package_show` line
  matches `client.py` `_package_show` / `_ckan_action("package_show", id=...)`. "Unchanged archives are skipped" is `client.py`
  `iter_members` (an upload whose newest capture carries the live `last_modified` yields `unchanged`).
- `raw_feed.commands`: two `pipeline ... --last 24h` lines for the summary and the FY summary, which cover exactly what `notebook.needs`
  ("the current and FY summary tables") and cells 2 to 4 read. Comments are 6 words or fewer.
- Field guide matches registry types and NESO's dictionary: `timestamp_utc` = `delivery_start` (registry temporal `utc_instant`,
  column `delivery_start`); `published_at` null (vintage `capture_fallback`); service names `Response`, `Quick Reserve`, `Slow Reserve`,
  `Balancing Reserve` all occur in silver.
- Related notes are 12 words or fewer. The `dynamic-containment-data`, `eac-br-auction-results` and `eac-mock-auction-results` lines follow the
  note's "What this package is not" and NESO's package text.
- No local counts, dates or gaps beyond what the chart, the eight rows and the notebook outputs show.

### Rendering
Screenshots at 1440, 1024 and 768 (headless Chrome, full page) and at 390 through a 390 px iframe, plus the built-in pane at 390
(frame unfolded, notebook opened) and 1024 (frame unfolded). Hero chips (11, wrap at 390), scenery, chart and key, raw-feed wells (long
upload URLs wrap), frame and guide, notebook outputs and plot, related list: fully visible. Document scroll width equals the
viewport at 390; no non-SVG element passes the viewport outside its own scroll box (the frame and the notebook tables scroll inside
their panels, as the template does). The site has no dark scheme. One finding: nit 11.

## On the writer's open questions
- Four products instead of six: accepted (seat ruling); the colour limit is real and the caption is honest.
- Reliance on the 2026-10-16 capture: safe. Both the spec and the sample dedup on the key, and I found no key with differing values.
