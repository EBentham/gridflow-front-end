# Balancing Reserve auction results (`eac-br-auction-results`): checker review

Checker, 2026-10-18. Rubric `.planning/v5/review-rubric.md`; brief `.planning/v5/author-brief.md`. Inspection only.

## Verdict: REVISE

Two majors, seven nits. No blocker: every fact on the page that I re-derived is true, the chart reproduces from silver, and the
date convention is better supported than the writer claims. The majors are a reading trap in the NBR line and a command list
that cannot produce the notebook it advertises.

Gates run: `gridflow-build --only neso_data_portal/eac_br_results_summary` succeeds (it reports one error on a page it did not
render, `aggregated_bsad` alt over budget, not this page); `detect.mjs --json` on the page returns `[]`; full `pytest -q` in the
worktree 153 passed (a first run showed 3 failures while another writer's files were mid-edit; the re-run was green). Mirror
`cmp` equal to the canonical note, 485 of 485 lines CRLF, vault diff is 147 insertions and 0 deletions. Page grep for
`locally`, `held`, `our `, `since 20`, `% of`, digits before `rows`/`days`, em dash, middle dot, arrow, `live`, `now`, `yet`:
clean.

## Findings

### 1. MAJOR: the flat NBR line reads as a £0 price, but it is mostly "nothing was bought"
Field paths: `page.chart_view.key[1].note`, `page.chart_view.alt`, `page.chart_view.caption`.

The key note says "£0 on every day from 4 December 2024 in this chart" and the alt says NBR "is 0 on every day from 4
December 2024". Both are true of the plotted means, but the chart is an unweighted mean over windows and NESO records
`clearing_price` 0 in windows where `cleared_volume` is 0. A reader sees free negative reserve; the data says almost none
was bought. Neither the caption nor the key says that a 0 price is recorded where nothing cleared, and that the mean includes
those windows. The writer knew (report, "Open questions": "NBR cleared MW occasionally at £0 ... the chart shows price only, so
this is not on the page").

Evidence (Polars on silver `eac_br_results_summary`, UTC reading, UK day 23:00 to 23:00):
- NBR, 4 December 2024 to 29 October 2025: 330 days; 328 have 0 MW cleared in every window; the 2 others are the only days
  with any MW, last on 2025-08-20. 15,823 of 15,840 windows cleared 0 MW; max price on every one of those days is 0.0.
- PBR has the same effect on a smaller scale: 913 windows on 139 days have price 0 with MW cleared (genuine £0 clears), and
  they sit inside the mean. Example 2024-03-14: 25% of windows at 0, daily mean 4.04 against 5.39 over the non-zero windows.
- The sample frame already shows the pattern (NBR rows 0.0 MW at 0.0), so a sentence about it is not local data.

Fix: say in the caption that NESO records price 0 where nothing cleared and that the mean includes those windows, and reword
the NBR key note so it does not read as a price ("NBR line is 0 from 4 December 2024; nothing is recorded as cleared at a
price in those windows" or similar, within the key-note budget). Keep numbers to what the chart or frame shows.

### 2. MAJOR: `raw_feed.commands` does not produce what `notebook.needs` and cell 4 require
Field paths: `page.raw_feed.commands`, `page.notebook.needs`, `page.notebook.cells[1]`.

The three commands are `ingest` and `transform` of `eac_br_results_summary`, then `transform` of `eac_br_results_sell_orders`.
But each of the four tables is its own family key with its own single resource, so `ingest ... eac_br_results_summary` fetches
the summary dump only. Consequences:
- `notebook.needs` says "a capture of the summary and by-unit tables", and cell 4 reads
  `silver_neso_data_portal_eac_br_results_by_unit_latest`, but no command ingests or transforms `eac_br_results_by_unit`. A
  reader following the page has no by-unit silver and cell 4 fails.
- `transform ... eac_br_results_sell_orders` has no preceding `ingest` for it, and nothing on the page reads sell-orders silver.

Evidence: registry `src/gridflow/connectors/neso_data_portal/registry/eac-br-auction-results.json` (four `families`, each
resource has `"family": "<own key>"`); `client.py` `iter_members` docstring "Capture one family"; `config/sources.yaml:892-895`
(four separate datasets). The `request` lines under `family.members` correctly show four separate dump URLs, which makes the
single-table commands more misleading.

Fix: add `ingest` and `transform` for `eac_br_results_by_unit` (the notebook's second table); for the other two members give
`ingest` plus `transform` pairs or drop the lone sell-orders transform. Comments stay at 6 words or fewer; check the commands
budget in `page_fields.py`.

### 3. NIT: measured-on-our-copy universals marked "(checked)"
Field paths: `page.what_it_is`, `page.chart_view.caption`, `page.record.fields.clearing_price`, `page.related[0].note`,
`page.family.members[1..2].differs`.

I reproduced every one, so none is wrong:
- Buy, sell and by-unit executed MW each sum to the summary's `cleared_volume`: buy 57,216 of 57,216 windows; sell (all order
  types) 57,216 of 57,216 (98 windows have no sell rows and cleared 0 MW); by-unit 39,673 windows with unit rows all equal, the
  other 17,543 windows cleared 0 MW (0 windows with MW cleared and no unit rows).
- By-unit row equals that unit's summed sell-order executed MW: 621,111 of 621,111; no duplicate (`auction_unit`, product,
  window); no sell group with MW above 0 is missing from by-unit.
- Every buy, sell and by-unit row carries its window's summary `clearing_price`: one distinct price per window in each table,
  equal to the summary's everywhere (buy 57,216 windows, sell 57,118, by-unit 39,673).
- All 157 distinct `auction_unit` values are in `elexon/bmunits_reference` `national_grid_bm_unit`; 0 match `bm_unit_id`.
- 596 auctions, each on exactly one day, no day with two auctions.

They are structural facts of a frozen whole-table dump, not statistics about our holdings, and the DFS page carries the same
kind of claim. But rubric 1 (last bullet) says universals are a vendor or code rule or scoped to what the page shows, and
"(checked)" does not say on what. Promote this to major if you read the rubric strictly; otherwise scope each ("in the NESO
archive") and drop the bare "(checked)". Also note the by-unit sum only equals the summary where unit rows exist (0 MW windows
have none); "sum to the summary's cleared MW" is accurate but incomplete for a reader who joins on window.

### 4. NIT: the date convention is sound but the page shows none of the evidence; "UK time" and "(checked)" need care
Field paths: `page.chart_view.caption`, `page.chart_view.x_label`; canonical note body, paragraph "The clock is undocumented".

The UTC reading is supported. Checked on silver:
- All 596 auctions: the first window is `23:00` in the string for 176 GMT days and `22:00` for 420 BST days; 46 windows on
  2024-03-31 (auction 189) and 2025-03-30 (1109), 50 on 2024-10-27 (746) and 2025-10-26 (2081); every other auction has 48;
  every window is 30 minutes; consecutive days, no gaps.
- Under the UTC reading, 596 distinct days and none with two auctions. Under a "UK local strings, day starts 23:00" reading the
  same assignment puts 1 or more auctions across two days (an auction splits on BST days), so the check does discriminate.
- Independent corroboration the writer did not use: per auction, the latest sell `order_entry_time` falls at about 07:00 to
  07:14 in the strings on BST days and about 08:00 to 08:11 on GMT days, 14h 45m before the first window every time. The
  companion package says the auction runs at 08:15 (zone unstated). That is 08:15 UK time written as UTC. This is the strongest
  single piece of evidence; consider adding it to the note body (not the page).

Honesty: the page says "NESO states no clock" (`record.fields.delivery_start`), "Window times are text with no stated clock" and
"reading ... as UTC", which is adequate. Two small things:
- "Days run 23:00 to 23:00 UK time" presents the zone as given; NESO's companion text gives "23:00 to 23:00" and says the zone is
  not restated (vault `balancing-reserve-auction-requirement-forecast.md`, TODO). The UK-time day is the writer's inference, same
  as the UTC reading. The caption is honest only because "reading ... as UTC" follows.
- "(checked)" after "each auction lands on one day" is read by most people as checking the clock; it checks internal
  consistency. Suggest "(consistent with how the strings shift at the clock changes)" or drop it.
- Body: the paragraph still says "Consumers must not read these strings as UTC or as UK local time" and then the added
  "Evidence toward it" sentence has no clear antecedent for "it". Make the body say the page reads them as UTC as a working
  convention, so the note and the page do not contradict.

### 5. NIT: `PBR`/`NBR` expansion is stated as NESO's own
Field paths: `page.what_it_is`, `page.record.fields.auction_product`.

The vendor dictionaries for all three tables with `auctionProduct` say only "Service Type Identifier [NBR,PBR]"
(`.planning/research/neso-snapshots/field-info/20261008T114228Z/eac_br_results_*.json`); no vendor text we hold expands the
codes. The companion package spells "Positive Balancing Reserve" and "Negative Balancing reserve" without the codes. The
reading is almost certainly right, and the data supports PBR: for windows whose start string matches the companion forecast
archive's `service_window_start_time`, PBR cleared MW correlates 0.86 with `positive_balancing_reserve_requirement_mw` (28,604
windows; means 426 against 428 MW). NBR does not tie to the negative requirement (mean cleared 41 MW against 981 MW required),
so NBR rests on exclusion and on the companion naming. Suggest the field line says the dictionary lists the codes only
("`PBR` or `NBR`; read as positive or negative Balancing Reserve, NESO's dictionary lists only the codes"), within 14 words.

### 6. NIT: `facts.history` and `cadence` leave an obvious question open
Field paths: `page.facts.history`, `page.facts.cadence`.

The history span (`2024-03-12T23:00:00` to `2025-10-29T22:30:00`) is our measurement of one capture of a frozen dump, not a
vendor statement, though it matches the silver min and max exactly. The cadence line says "NESO says daily" (true: the CKAN
package says "updated daily in the morning", extras "Update frequency: Daily") while the chart stops on 29 October 2025, with no
reason given. The body already carries the likely reason (the newer EAC package's Balancing Reserve rows start at
`2025-10-29T23:00:00Z`). Either say the archive ends there and later auctions are in NESO's newer EAC package, or leave the
cadence at "one auction per delivery day" and drop "NESO says daily" so the page does not imply a table that is still growing.

### 7. NIT: the "28,370 sell orders executed with 0 MW" is explained, and the writer's defect entry is wrong
Field paths: author report "Could not verify" and "Defects"; `page.how_used[1]`, `page.family.members[3].differs`.

Reproduced: 28,370 sell rows have `status` EXECUTED (27,322) or PARTIALLY_EXECUTED (1,048) with `executed_quantity` 0. All 28,370
have `quantity` 0 (zero filtered by `quantity > 0` gives 0 rows). The raw bronze CSV carries the same values from NESO (auction
152, order 2548829: `quantity` 0.0, `status` EXECUTED, `executedQuantity` 0.0, `clearingPrice` 1.42), so this is vendor data
(zero-MW orders), not a gridflow or silver defect. The report's "gridflow / data (sell orders)" defect should not go to the
BACKLOG as written. Also, the sell-order status does not imply MW: "MW offered against price limit, with the outcome" is fine,
but a reader building bid stacks from `status` would count zero-MW orders. Optional: add "status can read executed on a 0 MW
order" to the sell-orders note or `differs` if the word budget allows.

### 8. NIT: `time_text` code review (`distil.py`, `chart_spec.py`, tests)
Correctness is fine; findings are polish.

Verified correct:
- `_time_from_text`: parse, `replace_time_zone("UTC")`, `convert_time_zone(zone)`, `replace_time_zone(None)`, subtract `hours=starts`,
  `truncate("1d")`. With `starts: -1` this is local time plus 1 hour, so a 23:00 UK start lands on the next date; BST edges
  (22:00 UTC) and the 46- and 50-window days land on the right date. Reproduced from silver independently with a different
  expression: the committed series matches my daily means for all 596 days and both products (max absolute difference 0.0005,
  the series' rounding), and every `x` date equals my day.
- Other charts: `_scan` returns early only when `time` and `time_text` are both present; no other spec has `time_text`, so no
  other path changes. `time_text` is added to `_ALLOWED_KEYS` and rejected for bar charts. Full `pytest -q` is 153 passed.
- The test `test_text_times_go_to_the_uk_day_that_starts_at_2300` is meaningful: both edges of a GMT day and of a BST day, and the
  next day's first window, against hand-checked means.

Polish (none blocks):
- A bad zone name is not caught by `validate_spec` (`time_text.day.zone` is only checked as a non-empty string); it fails inside
  Polars at distil time with a Polars error rather than a `DistilError`/spec error. Same for a format that does not match the
  data (`strict=True` raises a Polars `ComputeError`).
- `day` with a sub-day `time_bucket` is accepted and silently gives daily points.
- No test for `time_text` without `day`, nor for a failing parse. The committed series labels each UK delivery day
  `...T00:00:00Z` (a UTC instant), harmless on a date axis but worth a docstring sentence.

### 9. NIT: small wording
Field paths: `page.chart_view.title`, `page.notebook.cells[0]`.
- The chart title says "BR clearing price"; the abbreviation is not spelt out in the title and the page H1 says "Balancing
  Reserve". "Balancing Reserve" would fit the title budget.
- Cell 3's output columns `PBR_mw` and `NBR_mw` are the mean MW per window, not a daily total, and nothing says so; a reader
  could take 449.73 for MW per day. Rename to `PBR_mean_mw` or say it in `notebook.lead` (the lead does not describe cell 3).

## What I checked and found correct

- **Chart provenance:** `spec_origin: vault`, digest matches (build passes), no staged spec, window 2024-03-13 to 2025-10-29
  fixed, 596 days, 2 series, 57,216 rows used, 0 nulls dropped. Window end matches the newest silver row: last
  `delivery_start` `2025-10-29T22:30:00` is the last window of the 29 October day under the stated convention; first
  `2024-03-12T23:00:00` is the first window of 13 March.
- **Spot checks against silver (daily mean, £/MW/h):** PBR 2024-03-13 9.579; 2024-03-31 2.538 (46 windows); 2024-07-04 1.470 (the
  minimum); 2024-10-27 4.523 (50 windows); 2024-12-13 40.471; 2025-01-21 51.542 (the maximum); 2025-10-29 3.910. NBR maximum 1.543
  on 2024-05-25; 1.366 on 2024-12-03, the last day above 0; 0.0 on every day from 2024-12-04. 92.1% of PBR days between 2 and 10
  (page says 92% in the report; the alt says "mostly between about 2 and 10", fine). Alt text and key note match the series.
- **What the mean averages:** the caption says "unweighted mean of each delivery day's half-hour clearing prices"; that is exactly
  what `distil` does (mean over the rows per day and product, no volume weights). See finding 1 for the zero-price windows.
- **Facts:** grain and key (0 duplicate keys; registry `entity_key`); units MW and £/MW/h from the vendor dictionary
  (`clearedVolume` MW, `clearingPrice` £/MW/h); one auction per delivery day; every window 30 minutes; `timestamp_utc` is the
  single capture time `2026-10-08 10:26:23.903043+00:00` and `published_at` is null in all 57,216 rows; the four dump URLs match
  the bronze sidecars and the registry resource ids; `package_show` URL matches `build_action_url`; `_latest` views and
  `query()` filtering on `timestamp_utc` confirmed with the gridflow_models interpreter (`_DATE_COLUMN_BY_DATASET` gives
  `timestamp_utc` for the summary and by-unit); frozen weekly re-fetch is `client.py` `_FROZEN_CADENCE`.
- **Notebook:** written by the runner, 5 cells, every cell read-only (`data.sql` selects), no errors; cell 3 means match my
  silver numbers (auctions 943 to 955: PBR 12.99, 37.63, 51.54, 26.70, 8.46, 4.63, 6.54, all NBR 0.0); cell 4 `units_mw` equals
  `cleared_volume` for 16:00 to 17:30; `plot_alt` values reproduce (6.85 for the first 8 windows to 02:30, 0 at 06:00 and
  06:30, 179.99 at 17:00 and 17:30, 84.99 at 22:30). `needs` disagrees with the commands: finding 2.
- **Sample rows:** real silver rows (`generated_by: gridflow-sample`), the eight rows show both products and the price step; the
  guide has a line for every non-pipeline column, key columns first.
- **Render:** screenshots taken myself with headless Chrome. 1440, 1024 and 768 folded (the full page, sliced); 1440 unfolded
  with the notebook open; 390 folded and unfolded with the notebook open, through a 390 px iframe. Hero, scenery tops, the
  chart, the frame (folded and unfolded), the guide, the notebook panel and the stratum corner labels are fully visible; member
  headings and keys now break at 390 (the seat's `_breakable` fix is in the built page). Dark scheme: none exists
  (`prefers-color-scheme` appears in no stylesheet), so one rendering covers both. The x axis showing only "2025" is a template
  matter per the seat's ruling.
