# soso review (SO-SO prices)

Checker: Opus 5.5, 2026-09-29. Page `elexon/soso`, note `30-vendors/elexon/datasets/soso.md` (vault worktree,
diff against `origin/master`), artefacts and built page in the `p26-elexon` worktree.

**Verdict: REVISE** (2 major, 3 nit). The facts, chart provenance, units and commands all hold. What needs work
is the rendered notebook at 390 and a frame that hides the price.

## Findings

1. **major** · `page.notebook.cells[2]` · At 390 cell [5] breaks into one-character columns, and at 768 it wraps raggedly.
   The continuation lines are hand-aligned under the open parenthesis, with about 32 and 41 leading spaces before
   `values=` and `ylim=`. In a 390 px code box the indentation eats the whole line width, so
   `ylim=(-100, 1000), figsize=(8, 3.5))` renders one letter per line down about 40 lines, and `values="trade_price"`
   and `aggfunc="mean"` split mid-word. At 768 the same lines wrap raggedly but stay readable.
   Evidence: headless Chrome, page in a 390 px iframe with the notebook opened (`nbfull390.png`, cell [5]); 768
   (`nb768.png`). `grep -E "^ {28,}[a-z]"` finds 2 such lines in `soso.md` (lines 105, 107) and 0 in `fuelhh`,
   `system_prices`, `mid`, `agpt`, `market_depth` and `lolpdrm`. Fix: break the arguments onto lines with a
   4-space hanging indent (or drop `ylim`/`figsize`), then rerun `run_notebooks.py`.

2. **major** · `page.record.select` · The frame folds `trade_price` and `trader_unit` behind `…` at every width,
   even 1440. The eight rows exist to show the price per direction per trader unit, and the caption says "one Bid
   and one Offer from each of four trader units". The visible columns are `settlement_date` through
   `trade_direction` at 1440, through `sender_identification` at 1024, and `settlement_date` only at 390, so a reader
   sees neither a price nor a trader unit without unfolding. `record.select.columns` (now on main, print order;
   `sample.py:111-117`) fixes it. For example, `columns: [settlement_date, contract_identification, trade_direction,
   trader_unit, trade_price, trade_quantity_mw]` keeps the key first. Then regenerate with `gridflow-sample`. The
   fields map follows frame order, so reorder `record.fields` to match. Evidence: 1440, 1024, 768 and 390
   screenshots; column header offsets measured in the browser (the fold box is 1123 px wide, and `trade_price`
   starts at x = 1458).

3. **nit** · `page.chart_view.caption` · The mean is sound, but the caption could say what it averages. In every
   hour shown each direction of `EWIC_EG` is a ladder of eight 25 MW contracts at evenly stepped prices, so the
   hourly mean is the ladder's midpoint and equals the MW-weighted mean. The ladder spans up to 52.05 on Bid and
   4.28 on Offer, and the line hides that spread. Consider "mean of the hour's eight 25 MW `Bid` (and `Offer`)
   contracts". The key notes already say "Mean over the hour's Bid contracts". Evidence: Polars on silver,
   `EWIC_EG`, settlement dates 14 to 18: `n` = 8 in all 240 (hour, direction) groups, `trade_quantity_mw` = 25.0
   in every row, max (max - min) = 52.05 Bid and 4.28 Offer. The 12:00 ladder on 15 Sep runs 460.29 to 492.51 in
   8 steps.

4. **nit** · `page.record.fields.sender_identification`, `receiver_identification` · "one value in all eight rows"
   repeats what the frame shows (rubric 4: no line repeats the frame). Say what the code is instead, or leave it at
   "Sender party code, as sent".

5. **nit** · `page.notebook.cells[1]` · At 768 and 390 the `.head()` output puts `trade_price`, the column the cell
   exists for, past the right edge of its scroll box (`.df-wrap { overflow-x: auto }`, so it scrolls and is not
   lost). Dropping `contract_identification` from the head keeps the price in view.

## What I checked and found true

- **Bid/Offer (focus 1).** No import/export, buy/sell or side reading anywhere in `summary`, `what_it_is`,
  `how_used`, `chart_view`, `record.fields` or `related`. The page says "Elexon's docs define neither" and that is
  true. Elexon's OpenAPI spec (`data.elexon.co.uk/swagger/v1/swagger.json`, `SoSoPricesDatasetRow`) gives
  `tradeDirection` only an example, `"A02"`, and no description. The Insights page's `tradeDirection` column is headed
  "Trade Direction" with no definition (Insights bundle `main.a722c2cc.js`). The Insights prose defines SO-SO
  services, not the sides. Silver carries `Bid`/`Offer` only (10128 each). The 15 Sep 12:00 rows show why no
  reading is safe: `EWIC_EG` Bid 492.51 > Offer -61.02, but `EWIC_NG` Bid 89.07 < Offer 306.54.
- **Unit (focus 2).** "£" is sourced. The Insights table headers in Elexon's bundle are
  `tradeQuantity:"Trade Quantity (MW)"` and `tradePrice:"Trade Price (\xa3)"`, and no per-MWh basis appears. The
  body's table row replacing "GBP/MWh" is right.
- **Chart (focus 3).** `spec_origin: vault`, the build's digest check passes, and no staged spec or override
  exists. Filter `trader_unit = EWIC_EG`, settlement dates 14 to 18, `group: trade_direction`, `aggregation: mean`,
  and the caption states all of it. `rows_used` 1920 = 5 × 24 × 16; 120 points per series, no nulls. The alt and
  both key notes match the committed series exactly: Bid 344.748 to 366.545 from 22:00 to 04:00, 769.604 from 04:00
  to 10:00, 475.924/476.4/476.524 from 10:00 to 22:00; Offer -0.045 overnight, -29.139 on the 14th, 17th and 18th,
  -58.876/-58.585 on the 15th and 16th. "`GL1_EG` carries the same prices in every hour shown" holds: a full join
  on (start_time, direction, contract number) gives 1920 of 1920 prices equal, and 240 of 240 hourly means equal.
- **Vendor quotes.** The API reference text ("system operator to system operator prices data, filtered by publish
  time… maximum range of 24 hours") is verbatim in the OpenAPI spec. The Insights prose quoted in the note is
  verbatim on `bmrs.elexon.co.uk/soso-trade-prices` (dumped with the data host blocked, so no data call was made).
- **Grain and key.** Dedup is `settlement_date, contract_identification (+ trade_direction)`, keep last
  (`soso.py:141-144`). Silver has 0 duplicate keys, and 0 even without direction.
- **Derived columns.** `timestamp_utc == start_time` on all 20256 rows, and there is no `settlementPeriod` in
  bronze (keys checked on the 14 Sep file). `end_time` is null on all rows and bronze `endTime` has no `Z`
  (`"2026-09-15T23:00:00"`, parse at `soso.py:118-125`). `published_at` comes from `publishTime`, and soso is in
  publication-window scope (`_publication_window.py`, ADR-026 exists in `gridflow/docs/DECISION_LOG`).
- **Raw feed.** The URL matches `build_params` and the 14 Sep sidecar `request_params`. Ingest `--end` is exclusive
  (`resolve_dates`: bare date = midnight UTC; `client.py:96-99` `while current < end`). With `--start 2026-09-13` the
  chunks start 13 00:00, 13 23:00, 14 22:00 … 18 18:00, and bronze is filed by `start.date()` (`client.py:314`), so
  transform 13 to 18 is right. The ingest window covers every publish: settlement dates 14 to 18 publish from
  13 Sep 21:03 to 18 Sep 20:03 UTC.
- **Sample and notebook.** The eight rows are `generated_by: gridflow-sample` and match the caption and field lines
  (one sender, one receiver, four resource providers). The notebook came from `scripts/run_notebooks.py` with
  read-only cells and no errors. The lead matches `query()`: `schema_manifest` date column `settlement_date`,
  inclusive predicate, bitemporal EXCLUDE, `ORDER BY` date column. `needs` agrees with the commands. `plot_alt`
  matches the rendered plot.
- **Build and detector.** `gridflow-build --only elexon/soso` is green and `detect.mjs --json` returns `[]`. The
  mirror is byte-identical to the vault note (`cmp`).
- **No local data, leakage or filler.** No hits for `locally`, `held`, `since 20`, `% of`, row or day counts, em
  dash, middle dot or arrow. "our" only matches inside "hour", and "real time" is Elexon's own phrase for the SO-SO
  adjustment. Related notes are 12 words or fewer and say how each dataset relates.
- **Body edits (rubric 7).** Each edit cites `file:line` (the lines are checked above) or the vendor page, and each
  fixes the smallest span. The curl example is untouched.
- **Screenshots.** Taken at 1440, 1024 and 768 full page, and 390 in a 390 px iframe, with the frame unfolded and
  the notebook opened at 1440, 768 and 390. The site has no dark theme (no `prefers-color-scheme` or `data-theme`
  in `assets/`). Apart from findings 1, 2 and 5, nothing is clipped or overlapping: hero scenery tops, chart,
  key, raw feed, guide, corner labels and related list are all clean.

## For the seat (not the writer's)

- The note body's Overview interconnector list (ElecLink twice, unsourced) predates this page; the writer flagged
  it. Silver in this window carries only the `EWIC`, `GL1` and `MOYLE` trader units.
- gridflow: `endpoints.py:242` calls the 24-hour cap "undocumented", but Elexon's spec now states it. `end_time` is
  always null because of the `Z`-only parse (transformer bug).
