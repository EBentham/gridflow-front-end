# elexon/mid: checker's review

Checker: Opus 5.5 · high, 2026-09-28. Inputs: vault note (worktree `vault-p26-elexon`, `page:` block and `git diff`),
mirror `vault/elexon/mid.md` (`cmp` identical to the vault note), artefacts in `p26-elexon`, the page rebuilt with
`gridflow-build --only elexon/mid` (green) and `detect.mjs --json` (`[]`), gridflow code, local silver (Polars, read
only), the archived vendor sources the note cites (`C:/gridflow-data/receipts/v2.1-F-5/sources/`).

## Verdict: REVISE

One major (0 blockers, 1 major, 1 nit). The major's root cause is in the chart renderer and affects four other
pages, so it needs a seat ruling rather than a writer-only patch.

## Findings

### 1. major: `page.chart_view.x_label` says the day bands start at 23:00 UTC; the renderer draws and names UTC days

- **What is wrong.** The label reads "settlement date; each starts at 23:00 UTC". The chart's tick marks sit at
  00:00 UTC, and each day name is centred on the UTC day. The band under "19 Sep" therefore runs from 00:00 to
  24:00 UTC on the 19th. That is settlement date 19, period 3, through settlement date 20, period 2, not settlement
  date 19. The first two points (settlement date 15, periods 1 and 2, at 23:00 and 23:30 UTC on the 14th) sit left
  of the first tick.
- **Evidence.**
  - `src/gridflow_front_end/chart_svg.py:214-223`: half-hourly data over at most 16 days take the third branch.
    `t = first_mid = math.ceil(lo / day) * day` is UTC midnight. Each tick is labelled `_day_label(t)` (the UTC date)
    and centred at `(t + min(t + day, hi_edge)) / 2`.
  - Rendered SVG (wide chart): the axis starts at `x0 = 74` (14 Sep 23:00Z, from `M74 18 V410 H884`). The x ticks
    are at `M78.8 410 v6 M194.5 410 v6 …`. One day is 115.7 px, so 4.8 px is one hour and the first tick is
    15 Sep 00:00Z. "15 Sep" is centred at x = 136.7 = `x0` + 13 h (15 Sep 12:00Z, the UTC midday). A settlement-day
    band would put it at `x0` + 12 h = 131.9. "21 Sep" is at 828.6, the midpoint of 21 Sep 00:00Z to the axis end
    at 23:00Z.
- **Scope.** The same label is live on `fuelhh`, `system_prices` and `indo`, which were approved in the pilot, and on
  `agpt` in this batch. The same example is in `page_fields.py:31`. The writer copied the house pattern, so this is
  not a lapse by the writer.
- **Fix: the seat rules between two options.**
  - (a) Anchor the day ticks in `_time_axis` on the series' own day boundary (its first timestamp, 23:00 UTC in BST)
    when the chart is on settlement dates. The label then becomes true on all five pages, and this note needs no
    edit.
  - (b) Relabel all five pages to UTC days, for example `x_label: UTC day; settlement dates start 23:00 UTC`
    (8 words, within the `x_label` budget of 8).
  - Patching this page alone would leave it inconsistent with the other four.

### 2. nit: `page.what_it_is` shortens the qualifying-trade rule

- **What it says.** "short-term trades (half-hour to four-hour products)".
- **What the source says.** The products are "Half Hour, One Hour, Two Hour and Four Hour products traded within eight
  hours of the Submission Deadline" (source 05, line 573).
- **Why it matters.** "Half-hour to four-hour" reads as a range, but there is no three-hour product. The eight-hour
  window, which is what makes the trades short-term, is also dropped.
- **Optional fix.** "half-hour, one-, two- and four-hour products traded within eight hours of gate closure", if the
  budget allows. Otherwise leave it.

## Checked and holding (no finding)

**The writer's flag 1: the three MIDS claims.** All three are stated directly in source 05, Elexon's "Market Index
Definition Statement Review 2025", last updated 24 September 2025. That page calls itself "the current MIDS"
(line 571).
- **Volume-weighted average, volume the sum.** Line 570 says the MIV "is calculated as the sum of the traded volume
  across the selected products and timebands". It also says "the MIP is the volume weighted average price of the
  trades".
- **Both zero below 25 MWh.** Line 570: "Where the MIV does not meet the ILT, the MIP and MIV default to zero".
  Lines 775 and 842 put the threshold at 25 MWh.
- **Day-ahead auction carries no weight.** The Table 1.1 row "Day Ahead Auction A" is 0 in every timeband
  (lines 690 onwards). Line 916 says the product "has '0' weighting".
- **The 2026 version.** No newer vendor document is archived. The page states the rule without dating it, so the
  missing 2026 confirmation is not a page defect.
- **Seat item.** The owner's class-3 ruling on these citations is still pending at the gridflow_models v2.1 close
  (note body, Modelling notes).

**The writer's flag 2: the alt text's "lowest -3.26".** The alt text does not pin -3.26 to the 19th. It says "dips
just below zero on the 17th, 18th and 19th (lowest -3.26)". -3.26 is the lowest of those three days under either
reading. Polars on APXMIDP, settlement dates 15 to 21:

| Day | Min by settlement date | Min by UTC day |
|---|---|---|
| 17th | -2.25 | -2.25 |
| 18th | -0.5 (period 48) | -3.26 |
| 19th | -3.26 (period 1, 18 Sep 23:00Z) | -2.24 |

The rest of the alt is the same under both readings:
- 46.33 to 212.39 on the 15th and 117.77 to 206.12 on the 16th;
- -19.03 at 20 Sep 15:00Z;
- 197.83 at 20:00Z;
- 134.98 to 207.07 on the 21st.

**Facts against code.**
- **Grain and key.** `unique(subset=[settlement_date, settlement_period, data_provider_id], keep="last")`
  (`silver/elexon/mid.py:122-125`). There are 0 duplicate keys over all 1,842 silver files, and the only provider
  codes are `APXMIDP` and `N2EXMIDP` (Polars `scan_parquet` group-by).
- **`timestamp_utc`.** Computed from settlement date and period by `settlement_period_to_utc`: period 1 is 00:00 UK
  local time (`mid.py:111-120`, `utils/time.py:28-42`).
- **Period range.** 1 to 50 in the schema, 46 or 50 on clock-change days.
- **Provider field.** `data_provider_id` is renamed from `dataProvider`, or from `dataProviderId` in legacy data
  (`mid.py:83-84`).

**Raw feed.**
- **Endpoint.** `/datasets/MID` uses `PUBLISH_DATETIME` with `from`/`to` (`endpoints.py:80-86`). Times are formatted
  `%Y-%m-%dT%H:%M:%SZ` and `page` is sent. The client makes 24-hour chunks while `current < end`
  (`client.py:93-99`, `max_chunk_hours = 24`).
- **URL.** Matches the bronze sidecar `bronze/elexon/mid/2026/09/20/raw_20260926T183137Z_6a438c16.meta.json` exactly.
- **Ingest window.** 14 to 22 with an exclusive end fetches partitions 14 to 21. That covers silver days 15 to 21
  under `PARTITION_SOURCE_OFFSETS = (-1, 0)` (`mid.py:28`).
- **Transform window.** 15 to 21, inclusive.

**Chart provenance.**
- **Series.** `series/elexon/mid.json` has `spec_origin: vault` and a spec equal to `page.chart`. It has 336 points,
  `rows_matched` 336, min -19.03 at 2026-09-20T15:00Z and max 212.39 at 2026-09-15T17:30Z.
- **Build and staging.** The build's digest check passes. No staged spec or authored override exists.
- **Title and caption.** They match the filter (APXMIDP, settlement dates 15 to 21), the unit and the aggregation
  (`last`, one row per timestamp).
- **Caption claim about `N2EXMIDP`.** Price 0 and volume 0 in 336 of 336 periods of the window.
- **Paint.** `petrol` for a price line.

**Sample rows.**
- **Source.** `samples/elexon/mid.json` has `generated_by: gridflow-sample`: 8 rows, settlement date 2026-09-20,
  periods 32 to 35, both providers.
- **Caption claim.** APXMIDP goes -12.14, -19.03, 38.19, 103.7, so it does turn from negative to positive.
- **Guide.** It has one line per non-pipeline column, key columns first.

**Notebook.**
- **Artefact.** Written by `scripts/run_notebooks.py`. The cells are read-only (query, `.head()`, plot) and none of the
  outputs has an error.
- **`notebook.lead`.** It matches `query()` (`gridflow_models/research/handles/source.py:401-451`): relation
  `silver_elexon_mid`, `settlement_date` inclusive at both ends, bitemporal columns excluded, `ORDER BY settlement_date`.
- **`plot_alt`.** It matches `mid-5.png` and the hourly UTC-day profile: near zero around midday on the 17th and
  18th, most of the 19th and 20th until 15:30Z, low -19, then 135 to 207 on the 21st.
- **`notebook.needs` "15 to 21 September" against ingest 14 to 22.** Not filed. The brief's own `needs` example ("20
  to 26 September 2026") is fuelhh's transform window while its ingest is 19 to 28, and `system_prices` does the
  same. The page follows the brief.

**No local data, leakage or filler.**
- **Grep.** The `page:` block and the rendered text contain no `locally`, `held`, `our`, `since 20`, digit-rows or
  digit-days, `% of`, em dash, middle dot, arrow, "live" or "real-time". The only hit is "rows come ordered", which
  describes the method.
- **Related notes.** Each is 8 words.

**Vault body edits.** All six are the smallest span and correct:
- dedup key: `mid.py:122-125`;
- point-in-time field: `mid.py:29-41`;
- `ingested_at` as the transform time: `mid.py:127-131`;
- the silver sample `timestamp_utc` 03:00Z: in BST, period 9 is 03:00Z;
- the providers gotcha;
- the rebuilt-silver gotcha, re-verified with 0 duplicates.

**Nothing clipped or overlapping.**
- **Folded state.** My own headless Chrome shots at 1440, 1024 and 768 and a 390 iframe (served on port 9716):
  - hero scenery (turbine tops, labels) fully visible;
  - chart and axis labels, key, raw wells and frame intact;
  - guide, notebook and related list intact;
  - no page-level horizontal scroll.
- **Open state (frame unfolded, notebook open).** Measured in my own pane tab at 1024 and 390, because the pane's
  screenshots wedged:
  - `scrollWidth` equals the viewport;
  - no text outside the viewport except inside the intended scrollers `.fw` and `.df-wrap`;
  - the only overflow-hidden overflows are hero scenery paths running off the scene edge.
- **Dark mode.** There is no dark theme: none of `site/hifi/assets/*.css` or `*.js` contains `prefers-color-scheme`
  or `data-theme`.

## Seat notes (not findings against this page)

- **Notebook `df` header shifted one column** (`build.py` ~1225): known, the seat's.
- **Landing blurb.** The main repo's `site/hifi/data/elexon.json:59` calls `mid` "market index, the GB day-ahead
  benchmark". Source 05, line 916 says the day-ahead auction "has '0' weighting" in the index, so the writer's
  suggested rewording is backed.
- **768 and 390 frame fold.** At 768 the frame folds `data_provider_id` and the price, and at 390 everything after
  `settlement_period`, so the column that matters shows only when the frame is unfolded. That is the fold rule, not
  this page's choice.
- **Mirror.** The mirror diff is a whole-file rewrite (the old mirror was LF), as the writer reported.
