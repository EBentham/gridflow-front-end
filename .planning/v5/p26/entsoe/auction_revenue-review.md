# entsoe/auction_revenue: review

Checker: Opus 5.5 · high, one agent, one advisor call. Inputs: the canonical note (diffed against quant-vault `origin/master` in `vault-p26-entsoe`; the mirror is byte-identical by `cmp`), the three artefacts, the built page, the writer's report, gridflow at `2822d38`, local silver and bronze (read only), gridflow_models `source.py`. Screenshots: headless Chrome through a 9824 static server with an iframe wrapper at 1440, 1024, 768 and 390, notebook open and frame unfolded (`scratchpad/arrev-shots/`). The server is stopped.

## Verdict: REVISE

1 blocker, 0 major, 4 nits.

## Findings

1. **blocker**: `page.summary` and `page.what_it_is`.
   - **What is wrong.** Both lines give the auctions and their revenue to ENTSO-E:
     - `summary` says "Revenue from ENTSO-E's daily explicit capacity auctions".
     - `what_it_is` says "ENTSO-E's revenue from explicit capacity auctions on a border".
     ENTSO-E neither runs these auctions nor earns the money. It publishes the figure on the Transparency Platform. The revenue belongs to the TSOs and interconnector owners.
   - **Evidence.** The note's own overview, which the writer left unchanged, says "Revenue earned by TSOs from explicit cross-border capacity auctions" (note body, `## Overview`). The page contradicts its source on the one domain fact a trading reader will notice first.
   - **Fix.** For example: "TSO revenue from the daily explicit capacity auctions on GB's borders with the Netherlands and Belgium, as published by ENTSO-E", and "Revenue from explicit capacity auctions on a border (Article 12.1.A), as ENTSO-E publishes it, …".

2. **nit**: `page.raw_feed.note` ("Of eight pairs, only GB with NL and GB with BE have returned a series") and `page.record.fields.in_area_code` ("GB on both borders with revenue").
   - **What is wrong.** "Have returned" describes gridflow's own fetches (224 bronze files, 1 to 5 Aug and 13 to 21 Sep), which reads close to a local-coverage statement.
   - **Evidence.** The claim is true of every bronze file. The six other pairs answer `Acknowledgement_MarketDocument` Reason 999, "No matching data found for Data item AUCTION_REVENUE [12.1.A]".
   - **Fix.** State it as the vendor's answer, for example "the other six pairs answer 'no matching data'", or scope it like the cadence line ("in the responses gridflow holds").

3. **nit**: `page.facts.grain` ("One row per hour, `in_Domain` zone and `out_Domain` zone") and `page.record.key`.
   - **What is wrong.** This is the intended grain, but not what the table or `query()` returns. The key is unique within one silver file only.
   - **Evidence.** Across files, 552 of 744 keys appear twice. The caption and notebook lead disclose this, so the page is not misleading overall.
   - **Fix.** Scope the grain, for example "One row per hour and zone pair in each silver file (most hours sit in two)", or leave it and accept the tension.

4. **nit**: note body, `## Known issues`, new bullet "(2026-09 silver: 1,296 rows, 744 keys)".
   - **What is wrong.** The count is mislabelled. 1,296 rows and 744 keys cover all 14 silver files, including the five August files (432 rows). September alone is 864 rows.
   - **Evidence.** Polars over `C:\gridflow-data\silver\entsoe\auction_revenue\**\*.parquet`: 14 files; the August files hold 96+96+72+72+96 rows. The mechanism in the bullet is correct.
   - **Fix.** Write "(silver, Aug and Sep 2026: 1,296 rows, 744 keys)".

5. **nit**: the note body cites no vendor source for A03 (`record.fields.amount_eur`, key note "repeated (A03)").
   - **What is wrong.** The writer's "not verified" item is now settled (see check C below), but the note gives no vendor citation for it.
   - **Fix.** Optional: add one line to the body citing ENTSO-E, "Introduction of different Timeseries possibilities (curvetypes) with ENTSO-E electronic documents" v1.4, §4.3: "only the position where a block change occurs is provided" and "The value of the Qty remains constant within each Block".

## Checked, not findings (the four focus items)

**A. Duplicates: reproduced; the page is correct.**
- Silver has 1,296 rows and 744 unique `(timestamp_utc, in_area_code, out_area_code)` keys. Adding `business_type` also gives 744.
- 552 keys sit in two files and 192 in one. Every duplicate pair has exactly one `amount_eur` value and comes from two different files.
- Each file D spans D-1 22:00Z to D+1 21:00Z (96 rows, or 72 on 3 and 4 Aug).
- **Cause confirmed:**
  - `silver/entsoe/_event_window.py:210` classes `auction_revenue` as EXEMPT, "inferred EXEMPT … own probes real EMPTY, not independently confirmed".
  - `AuctionRevenueTransformer` (`h6_market.py:245-247`) leaves `EVENT_WINDOW_FILTER` at the base default of False (`base.py:686`).
  - The transformer's `.unique(...)` (`h6_market.py:91-99`) works within one partition only.
- `query()` (`source.py:441-450`) is a plain `SELECT * … WHERE … ORDER BY`, with no dedup.
- **How each part of the page handles it:**
  - The caption says "Most hours sit in two silver files; one copy is kept".
  - The lead says "Most hours arrive twice … drop duplicates before summing".
  - The chart spec dedups (series provenance: 1,296 read, 672 matched, 336 dropped, 336 used).
  - The sample `select.dedup` gives one row per hour and pair.
  - Notebook cell 3 runs `drop_duplicates(subset=key)` before the head and the sum. The head's index (0, 1, 4, 5, 8…) shows the dropped copies.
- "Most" is sound under the page's own commands: delivery day 21 lands in file 20 only.

**B. Direction: no overclaim.**
- `what_it_is` says "Rows keep the ordered pair as sent; which direction an amount covers is not stated".
- The key codes say `out_Domain NL/BE`. `out_area_code` is "the zone across the border". `how_used` says "GB to continent price spread", which is a spread and states no direction.
- No other line states a flow direction.
- Related `cross_border_flows` "same pair orientation" holds: its silver GB pairs all have `in_area_code` GB, from the shared `_FLOW_PAIRS` (`client.py:40-49`).

**C. Forward-filled A03 blocks: summing is sound, not a blocker.**
- **Parser.** `parsers.py:533-600` emits every position from 1 to the period end and repeats the last declared record on each omitted position.
- **Vendor.** ENTSO-E curvetypes guide v1.4 (eepublicdownloads.entsoe.eu), §3 and §4.3: A03 "only the position where a block change occurs is provided … useful in cases where the quantity is stable". The Qty "remains constant within each Block", and each interval's time step is start + (Pos−1) × resolution. An omitted position therefore carries the previous per-interval value, not a share of a block total. `entsoe-py` reads A03 the same way (reindex, then `ffill`).
- **Bronze.** Declared `price.amount` values behave like price × MW per hour: 10.12, 20.24, 30.36, 40.48, 50.6, 60.72, 202.4 and 2024 are multiples of 10.12. Values repeated by the fill (30.36, 37.77, 30.33, 51.6) also appear as single declared hours elsewhere.
- **No daily figure is repeated per hour in the charted window.**
  - The only Periods with a single point are value 0: NL delivery days 13 to 19 Sep and BE delivery day 22.
  - The longest non-zero fills are one to two hours of tens of EUR, for example BE delivery day 21: 1:30.36, 4:678.04, 5:30.33, then 7:0 to the end.
  - Even read as block totals, the plotted daily sums would move by under 100 EUR.

**D. Coverage and chart: match silver.**
- **Coverage.**
  - `business_type` is B07 on all 1,296 rows, and `resolution` is `PT60M` on all of them.
  - There are two pairs, GB→NL (672 rows) and GB→BE (624).
  - EUR is sent in `currency_Unit.name`; the transformer's `output_cols` (`h6_market.py:107-117`) drop it.
  - The request pins `businessType=B07` and `contract_MarketAgreement.Type=A01` (`endpoints.py:233-242`).
- **Window.** 14 Sep 22:00Z ≤ t < 21 Sep 22:00Z, with 168 points per border and no nulls.
- **NL.** Zero until 19 Sep 22:00Z (first non-zero value 152.79). The delivery-day-20 maximum is 14,711.94, and the peak is 115,433.72 at 21 Sep 11:00Z.
- **BE.** Peaks of 81,197.76 at 15 Sep 11:00Z, 78,442.32 at 16 Sep 11:00Z and 13,209.6 at 18 Sep 11:00Z. The maxima on delivery days 17, 19, 20 and 21 are 206.4, 1,403.52, 4,367.85 and 678.04.
- The alt text and both key notes agree with these values.
- **Notebook `plot_alt` against Polars daily sums (Brussels date).**
  - BE: 247,325.98, 381,570.69, 654.39, 50,966.23, 6,170.56, 11,218.26 and 829.78.
  - NL: 0 on five days, then 41,270.54 and 660,097.84.
  - These match `plot_alt`, and the PNG matches too.

## Other rubric items verified

- **`raw_feed.requests`.** Matches the connector and bronze meta `request_url` exactly: parameter order, `yyyymmddHHMM`, and the token placeholder.
- **Commands.**
  - `day_subwindows` (`utils/time.py:123`) makes `--end` an exclusive midnight. Ingest 14 to 21 therefore fetches UTC days 14 to 20.
  - `PARTITION_SOURCE_OFFSETS = (0,)` is not overridden. Transform 14 to 20 (inclusive) covers delivery days 15 to 21.
  - `notebook.needs` ("14 to 20 September 2026") agrees.
- **Lead.** Matches `query()`: `silver_entsoe_auction_revenue`, `timestamp_utc`, inclusive ends, lineage excluded.
- **Artefacts.**
  - The series has `spec_origin: vault` and no staged spec or authored override exists.
  - The sample is `generated_by: gridflow-sample` with 8 real rows.
  - The notebook is `generated_by: scripts/run_notebooks.py`. Its cells are read-only, and there are no error outputs.
- **Build and detector.** `gridflow-build --only entsoe/auction_revenue` passes. The detector reports only the accepted `em-dash-overuse` advisory (174 hits, all from EIC padding). The page has 0 `—`, 0 `→` and 0 `·`.
- **Leakage grep.** Clean. The `rows` hits are in the section heading, "in these rows" and the help card.
- **Rendering.**
  - Nothing is clipped at 1440, 1024, 768 or 390: hero turbines, chart, key, corner labels, frame and guide, notebook, related list.
  - `scrollWidth` equals the width at all four sizes.
  - Elements the probe flagged past the viewport are inside scroll boxes, not clipped:
    - the unfolded `table.pl` sits in `.fw { overflow-x: auto }` (`dataset.css:14`);
    - the notebook `head()` table at 390 sits in `.df-wrap { overflow-x: auto }` (`theme.css:431`).
  - The stylesheets carry no `prefers-color-scheme` rules, so dark and light render identically and the light captures cover both.
  - The wrapped `contract_MarketAgreement.Type=A01` line at 390 is template behaviour.
- **Related.** All four resolve, and each note is 12 words or fewer. `total_capacity_allocated` silver holds the same two ordered pairs.
- **Body edits.** Each cites `file:line` or bronze and fixes a small span (apart from nit 4's label). `amount_eur` from `price.amount` (`h6_market.py:130`) is correct, and the old `Point.quantity` was wrong.
