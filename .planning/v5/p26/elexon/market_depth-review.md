# elexon/market_depth: checker's review

Checker: Opus 5.5 · high, 2026-09-29. Inputs: vault note `30-vendors/elexon/datasets/market_depth.md` in the vault
worktree (its `page:` block and the diff against `origin/master`), the mirror, the three committed artefacts, the built
page, `market_depth-author.md`, gridflow code, local bronze and silver (read only).

## Verdict: APPROVE

Two nits, no blockers, no majors.

## Findings

1. **nit** · `page.raw_feed.note` (evidence trail). The same-day-null clause is allowed (see ruling A below), but its
   evidence is only in local bronze and the writer's report. The vault body does not record it, so the next checker
   cannot verify it from the note. Add one line under "Known issues and gotchas" that cites the capture. For example:
   "A request for the current settlement date returns every period, with nulls from about the current period on.
   Bronze `market_depth/2026/09/01` holds 15 fetches made during 1 September 2026, and the first null period moves
   with fetch time."
   Evidence: see ruling A.

2. **nit** · `page.raw_feed.note` (wording). "null volumes for the day's later periods" is broader than what was sent.
   `indicatedImbalance` was sent for all 48 periods in every same-day fetch. `offerVolume` and `bidVolume` stayed
   populated about four periods longer than the accepted and priced fields: at 11:17 UTC, accepted fields were null
   from SP24 and offer/bid from SP28. Optional tightening: "returned null accepted volumes for the day's later
   periods". It is not wrong as written, because "volumes" does not cover the indicated imbalance.
   Evidence: see ruling A.

## Rulings on the writer's open questions

**A. Same-day nulls in `raw_feed.note`: allowed, keep it.**
- The clause describes the vendor response, not local holdings. It says what Elexon sent to a request. It does not
  say what silver holds, count rows, or describe a gap in our copy.
- It is dated and singular ("seen on 1 September 2026"), not a universal. So rubric §1's bar on measured-on-our-copy
  universals does not apply, and §3's list (held locally, local counts, first/last dates, gaps, coverage) does not
  match it.
- Any reader can reproduce it by requesting today's settlement date. That makes it vendor behaviour, like the note's
  own "Captured live 2026-05-08" bronze sample.
- The evidence is stronger than the writer's single file. `C:\gridflow-data\bronze\elexon\market_depth\2026\09\01`
  holds 15 same-day fetches of `.../market-depth/2026-09-01?page=1`. All 48 periods are in each, and the first null
  moves with the clock:

  | Fetched (UTC) | First null `totalAcceptedOfferVolume` | First null `offerVolume` |
  |---|---|---|
  | 04:15 | SP10 | SP14 |
  | 06:47 | SP15 | SP19 |
  | 07:57 | SP18 | SP21 |
  | 09:13 | SP20 | SP24 |
  | 11:17 | SP24 | SP28 |

  `indicatedImbalance` is never null.
- The clause also matters to the reader. With `keep="last"` over files in fetch order, a same-day fetch that is not
  re-fetched later leaves those nulls in silver.
- The page gives no cause (gate closure fits the timing but is unverified), which is correct.
- The seat can still take a stricter reading. The writer's fallback is to cut the clause after "wins each period".

**B. `record.fields.indicated_imbalance_mwh`: accurate and fair; naming the conflict is better than "as sent" alone.**
- "the column says MWh": the name is `indicated_imbalance_mwh` (`silver/elexon/market_depth.py:64`, and the
  `ElexonMarketDepth` field, `schemas/elexon.py`).
- The `ElexonMarketDepth` docstring's "(all in MWh)" lists bid/offer, accepted and priced accepted volumes. It does not
  list the indicated imbalance, so the column name is the only MWh source for this field. The line names that source
  correctly.
- "gridflow's IMBALNGC schema says MW": `schemas/elexon.py:338`, "indicated_imbalance is in MW".
- The line asserts neither unit. That avoids the pilot's INDOD "MWh" overclaim, and it tells the reader something
  "as sent" would hide.
- Seat follow-up (not a finding for this page): the vault note `30-vendors/elexon/datasets/imbalngc.md:105` gives
  IMBALNGC's `indicated_imbalance` as "MWh", against the schema's MW. When the `indicated-day-ahead` family page is
  written, it should take the same stance as this line, or the two pages will disagree.

**C. Commands: correct.**
- Ingest: `gridflow ingest elexon market_depth --start 2026-09-16 --end 2026-09-22`.
  - A bare `--end` becomes midnight UTC (`pipeline/runner.py:479-500`, `resolve_dates`).
  - `market_depth` is `ParamStyle.DATE_PATH` (`connectors/elexon/endpoints.py:250-254`), so `client.py:89-91` calls
    `_date_range(start, end)`.
  - `_date_range` turns both ends into dates and loops `while current <= end_date` (`client.py:360-373`). So 16 to
    22 September is fetched, the 22nd included, as the comment says.
- Transform: its end is inclusive (`runner.py:1126`, `date_range(start_dt.date(), end_dt.date())` at `:1138`).
- No widening is needed:
  - the transformer has no `PARTITION_SOURCE_OFFSETS`;
  - `read_bronze` reads only the target date's folder (`market_depth.py:31-42`);
  - bronze is partitioned by `data_date` = the path date (`bronze/writer.py:37-40`, `client.py` `data_date=settlement_date`).
- `notebook.needs` "16 to 22 September 2026" matches.

## Checklist

**§1 Facts: pass.**
- Request URL:
  - host and path from `endpoints.py:250-254` and `_fetch_date_path` (`client.py`, `f"{endpoint.path}/{date}"`);
  - `page=1` from `build_params`, where pagination defaults to on;
  - bronze sidecar `request_url` for 2026-09-20 is the same string.
- Grain and key: `market_depth.py:113`, `unique(subset=[settlement_date, settlement_period], keep="last")`, runs over
  rows read from `sorted(glob("raw_*.json"))` (`:42`).
  - Filenames are `raw_{fetched_at:%Y%m%dT%H%M%SZ}_{sha8}` (`writer.py`), so "from the latest response" and "the most
    recently fetched response wins" are correct.
  - The window has 336 rows and 336 unique keys.
- Derived columns:
  - `timestamp_utc` is `settlement_period_to_utc` (`:102-111`); the window's first point is `2026-09-15 23:00 UTC`,
    so the x label "each starts at 23:00 UTC" is right for BST.
  - `settlement_period` is `ge=1, le=50`.
- `what_it_is`: the metadata list IMBALNGC, BOD, DISEBSP, DISPTAV matches bronze 2026-09-20 `metadata.datasets`.
  "in MWh by gridflow's schema" is the `ElexonMarketDepth` docstring.
- Notebook lead: `query()` (gridflow_models `research/handles/source.py:401-451`) reads `silver_elexon_market_depth`
  on `settlement_date` with both ends included, ends with `ORDER BY {date_col}`, and drops the bitemporal columns. The
  wording is the house phrasing used by `system_prices`.
- Universals are all scoped to what the page shows:
  - "negative in this window": `total_accepted_bid_volume_mwh` max -42.78 over 16 to 22 September;
  - "negative in these rows" and "zero in periods 26 and 33 here": checked against the eight rows.

**§2 Chart provenance: pass.**
- Series header: `spec_origin: vault`, `spec_sha256` present, 336 rows used, 0 nulls dropped. The build's digest check
  passed.
- No staged spec at `site/hifi/data/chart-specs/elexon/market_depth.json`, and no authored override.
- The title and caption state the dataset, MWh, the window and "one value per half-hour". `last` is a no-op on unique
  keys.
- Every number in the alt text matches silver, grouped by settlement date:
  - 16th: 441.5 to 2,817.8;
  - 17th to 19th: 1,278.2 to 3,752.7, peak SP38 on the 19th at 17:30 UTC;
  - 20th: 2,840.9 to 238.9 (SP48);
  - 21st: 211.3 to 1,362.5;
  - 22nd: 0.0 to 724.2.
- `plot_alt` bids for the 17th to 19th are -1,748.7 to -4,233.6. It matches.
- Paint is `petrol` for a volume line. No khaki, no clipping, nothing summed.

**§3 No local data: pass** (ruling A covers the one case). Grepping the `page:` block and the rendered text for the
§3 terms found only "half-hour", "four" and "these rows" (the eight rows).

**§4 Build and structure: pass.**
- `uv run --system-certs --extra build gridflow-build --only elexon/market_depth` rendered the page.
- `detect.mjs --json`: `[]`.
- The mirror is identical to the vault note (`cmp`).
- The sample is `generated_by: gridflow-sample`, 8 rows by 16 columns, and the caption claim holds in all eight rows:
  accepted offers 1,242.5 to 1,544.8, accepted bids -2,246.2 to -2,826.9.
- The guide has 10 lines, keys first, and none for the pipeline columns.
- The notebook is `generated_by: scripts/run_notebooks.py`. All cells are read-only, there are no errors, and the
  `.head()` output and plot are present.
- The related link `imbalngc.html` exists in the worktree as a pointer that refreshes to
  `indicated-day-ahead.html#imbalngc`.

**§5 Clipping: pass.**
- Method: my own screenshots on port 9739 (server stopped), with the page in an iframe at 1440, 1024, 768 and a true
  390, frame unfolded and notebook open.
- Folded frame checked at 1440 and 390.
- No horizontal overflow: `scrollWidth` equals the iframe width minus the scrollbar at every width, open and closed.
- Hero scenery (turbine tops, pylons, labels), chart and x label, key note, raw-feed wells, frame, guide, notebook
  plot and legend, and the related list are fully visible.
- The site has no dark theme (no `prefers-color-scheme` in any stylesheet), so light covers both.

**§6 Leakage and filler: pass.**
- No planning labels, no em dashes, no middle dots, no arrows, no "live".
- `related` notes are 12 words or fewer and say how the datasets relate.

**§7 Vault body edits: pass.** Each edit is a small span with a citation:
- the Overview and Known-issues dataset list (bronze metadata);
- the `ingested_at` row (`market_depth.py:115-120`);
- the `indicated_imbalance_mwh` row (`schemas/elexon.py:338`);
- the silver sample `timestamp_utc`, `2026-05-05T23:00:00+00:00`, and the real column names and values taken from
  the note's own bronze sample;
- the bronze path pattern (`bronze/writer.py`).

The curl example is untouched.

**Distinct from `system_prices`: yes.**
- The shared window (16 to 22 September) and the shared sample rows (2026-09-20, SP26 to 33) are a deliberate
  alignment: that page shows those periods' negative prices, this one shows accepted bids outweighing offers in the
  same periods.
- Everything else differs:
  - value column (`system_sell_price` against `total_accepted_offer_volume_mwh`);
  - `how_used` (price target against volume features);
  - column guide;
  - notebook plot (offers and bids together);
  - related list.

Known template limits, not findings: the chart draws one column, and the frame folds the accepted-bid columns.
