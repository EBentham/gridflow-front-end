# elexon/market_depth: writer's report

Writer: Opus 5.5 · high, 2026-09-29. Page: `site/hifi/data-sources/elexon/market_depth.html` (front-end worktree `p26-elexon`).

## Status

- `gridflow-build --only elexon/market_depth`: green. The build reports 2 errors on pages it did not render; they are other writers' pages.
- `detect.mjs --json`: `[]`.
- Artefacts, all made from real data:
  - `site/hifi/data/series/elexon/market_depth.json`: `spec_origin: vault`, 1 series of 336 points, `rows_used` 336, 0 nulls dropped.
  - `site/hifi/data/samples/elexon/market_depth.json`: `generated_by: gridflow-sample`, 8 rows by 16 columns.
  - `site/hifi/data/notebooks/elexon/market_depth.json` and `market_depth-5.png`: written by `scripts/run_notebooks.py`, 5 cells, no errors.
- No staged spec or authored override existed, so the `rm -f` did nothing.
- The mirror `vault/elexon/market_depth.md` is a byte copy of the vault note (`cmp` clean). The note is LF, not CRLF.
- Chart: `line` of `total_accepted_offer_volume_mwh`, one value per half-hour, `aggregation: last`.
  - Filter: `settlement_date` 16 to 22 September 2026. Window: `2026-09-15..2026-09-22`, the same as `system_prices`, so the two pages line up.
  - Silver has exactly one row per `(settlement_date, settlement_period)`: 768 rows, 768 unique keys. So there is no `dedup` and `last` changes nothing.
- The eight rows are 2026-09-20, periods 26 to 33, the same half-hours as the `system_prices` sample.

## What this page adds to system_prices

The two pages share a request shape: one call per settlement date, with the date in the path. `system_prices` gives each period's price and NIV; `market_depth` gives the volumes for the same periods. The notebook plots accepted offers and accepted bids together, which the chart cannot (see the template problems below).

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Request `GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/market-depth/2026-09-20?page=1` (`raw_feed.requests`) | `connectors/elexon/endpoints.py:249-254` (path, `DATE_PATH`); `client.py:246-258` (`f"{endpoint.path}/{settlement_date.isoformat()}"`, `build_params(endpoint, page=page)`); `endpoints.py:306-313` (DATE_PATH adds no query date; `page` because pagination defaults to True). Bronze sidecar `bronze/elexon/market_depth/2026/09/20/raw_20260926T182937Z_09842900.meta.json`: `request_url` is exactly this URL, `total_pages` 1. |
| Ingest `--start 2026-09-16 --end 2026-09-22`, "the end date is fetched" | `client.py:89-91` (DATE_PATH loops `_date_range`); `client.py:360-373` `_date_range`, `while current <= end_date`. |
| No widening of the ingest window | The transformer has no `PARTITION_SOURCE_OFFSETS` (`silver/elexon/market_depth.py`, whole file). Bronze is partitioned by `data_date` = the settlement date in the path (`bronze/writer.py:37-40`, `client.py:275`). `read_bronze` reads only the target date's folder (`market_depth.py:31-55`). |
| Transform `--start 2026-09-16 --end 2026-09-22` | The transform end is inclusive (brief and rubric); it matches the silver window and `needs`. |
| Grain "One row per settlement period, from the latest response"; key `(settlement_date, settlement_period)` | `market_depth.py:113` `unique(subset=[settlement_date, settlement_period], keep="last")` over rows read from `sorted(glob("raw_*.json"))` (`:42`). Bronze filenames are `raw_{fetched_at:%Y%m%dT%H%M%SZ}_{sha8}` (`bronze/writer.py:33-34,57`), so sorted order is fetch order and "last" is the latest fetch. Silver: 768 rows, 768 unique keys. |
| "The most recently fetched response wins each period" (`raw_feed.note`) | As in the row above. |
| "a same-day request returned null volumes for the day's later periods (seen on 1 September 2026)" (`raw_feed.note`) | Bronze `market_depth/2026/09/01/raw_20260901T111746Z_2cd8ac54.json`, fetched 11:17:46 UTC on 1 September: all 48 periods present. From period 24 the four accepted and priced fields are sent as JSON `null`; from period 28 `offerVolume` and `bidVolume` are too. `indicatedImbalance` is present for all 48. The note gives no cause. |
| "The response's metadata lists four datasets: IMBALNGC, BOD, DISEBSP and DISPTAV" (`what_it_is`, `related` imbalngc) | `metadata.datasets` in bronze 2026-09-20 and 2026-09-01, and in the note's own 2026-05-06 bronze sample. I do not map columns to source datasets. |
| Volumes "in MWh by gridflow's schema" | `schemas/elexon.py:606-610` docstring ("all in MWh") and the `_mwh` column names (`market_depth.py:61-71`). Stated as gridflow's labelling, not as a vendor fact. |
| Indicated imbalance unit is unsettled (`record.fields.indicated_imbalance_mwh`) | The market-depth column is named `_mwh`, but gridflow's `ElexonImbalNGC` docstring gives IMBALNGC's `indicated_imbalance` in MW (`schemas/elexon.py:336-339`). So the page names the conflict and asserts neither unit. |
| `timestamp_utc` is the start of the half-hour, computed from settlement date and period; periods 1 to 48, 46 or 50 on clock-change days | `market_depth.py:102-111` → `utils/time.py:28-42` (SP1 = 00:00 UK local; 30-minute steps). `schemas/elexon.py:615` `ge=1, le=50`. |
| x label "each starts at 23:00 UTC" | BST; the series' first point is `2026-09-15T23:00:00Z` for settlement date 16. |
| Caption: accepted bids "are negative in this window" | Polars, settlement dates 16 to 22: `total_accepted_bid_volume_mwh` min -4,233.6 (17th 18:30 UTC), max -42.8 (22nd 21:30 UTC); no zero or positive value. |
| Chart alt numbers | Committed series, grouped by settlement date: 16th 441.5 to 2,817.8; 17th 1,573.3 to 3,513.2; 18th 1,278.2 to 2,703.5; 19th 1,762.1 to 3,752.7 (max, 17:30 UTC on the 19th); 20th 2,840.9 (01:30 UTC) to 238.9 (22:30 UTC); 21st 211.3 to 1,362.5; 22nd 0.0 (one point, 11:30 UTC) to 724.2. |
| `plot_alt` | Read from the rendered `market_depth-5.png` and checked against silver: 17th to 19th offers 1,278 to 3,753, bids -1,749 to -4,234; the 21st and 22nd are both near zero. |
| Record caption "periods 26 to 33, when accepted bids outweighed accepted offers" | Sample rows: accepted offers 1,242.5 to 1,544.8; accepted bids -2,246.2 to -2,826.9; in all eight rows the bids are larger in magnitude. |
| Fields "negative in these rows", "zero in periods 26 and 33 here" | Sample rows: `bid_volume_mwh` -65,509.5 to -67,386.0; `priced_accepted_bids_volume_mwh` 0.0 in periods 26 and 33 and non-zero in 27 to 32. |
| Notebook lead: `silver_elexon_market_depth`, `settlement_date`, both ends included, lineage dropped, ordered by `settlement_date` only | gridflow_models, run: `_RELATION_NAME_BY_DATASET['market_depth'] == 'silver_elexon_market_depth'`, `_DATE_COLUMN_BY_DATASET['market_depth'] == 'settlement_date'`, `_BITEMPORAL_EXCLUDE = (event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year)`. `research/handles/source.py:401-451` (inclusive predicate, `ORDER BY {date_col}`). Not `_latest`: `APPEND_ONLY` defaults to False (`silver/base.py:711`). |
| Related `boal`, `imbalngc`, `mid`, `system_prices` have pages | They are in the `site/hifi/data/elexon.json` page set, and the build resolved all four. `imbalngc` is the first related link to a non-lead family member: `build.py:1350` links `imbalngc.html`, and that generated pointer page exists and redirects to `indicated-day-ahead.html#imbalngc`. |
| Key note "Accepted bids, in the same table, are below zero in this window" | Scoped to the window, as in the caption row above. |

## Note-body corrections (vault note, smallest span)

1. **Overview.** The note said "Market depth aggregates BOALF, DISBSAD, and IMBALNGC". It now says the response's `metadata.datasets` lists IMBALNGC, BOD, DISEBSP and DISPTAV, citing bronze 2026-09-20 and the note's own bronze sample.
2. **Known issues bullet.** "Aggregates BOALF/DISBSAD/IMBALNGC" is now "Built from IMBALNGC/BOD/DISEBSP/DISPTAV (the response's `metadata.datasets`)". The don't-double-count advice is kept.
3. **`ingested_at` row.** "Time ingested into bronze" is now the silver transform time, `datetime.now(UTC)` (`market_depth.py:115-120`).
4. **`indicated_imbalance_mwh` row.** Added the unit conflict: MWh by column name, MW in gridflow's `ElexonImbalNGC` (`schemas/elexon.py:338`).
5. **Silver sample.**
   - `timestamp_utc` for 2026-05-06 SP1 was `00:00Z`; it is now `2026-05-05T23:00:00+00:00` (BST, `utils/time.py:28-42`).
   - The two placeholder keys, `total_adjustment_sell/buy_volume_mwh`, are not silver columns. They are now `priced_accepted_offers/bids_volume_mwh`, with the values from the note's own bronze sample (0.0 and -469.39166666666665).
6. **Bronze path pattern.** `raw_<uuid>.json` is now `raw_<fetched_at>_<sha256[:8]>.json` (`bronze/writer.py:33-34,57`).

Front matter: I added the `page:` block. I left `last_verified` at 2026-05-08 for the seat to decide.

## Not verified

- **Vendor meaning of each column.** Elexon's own definitions were not available offline, and I made no live call. This covers what "offer volume" and "priced accepted" mean, and whether `offerVolume` is summed from BOD. The guide gives each column's field name and gridflow unit, nothing more.
- **Vendor unit of `indicatedImbalance`.** It is MWh by column name and MW in gridflow's IMBALNGC schema. Market depth's values also differ from local IMBALNGC captures for the same periods (for example SP1 on 2026-09-20: 2,038 here; 5,798 and 7,037 in IMBALNGC). Which IMBALNGC vintage feeds market depth is undocumented.
- **Why same-day values are null.** The page states the observation and gives no cause. Gate closure is plausible but unverified.
- **"Point-in-time field: `ingested_at` (no native PIT field)"** in the body. I left it. `ingested_at` is transform time, and `available_at` comes from `silver/base.py` (`datetime.now(UTC)`, or the bronze sidecar on reingest). Deciding whether this line should name `available_at` is the seat's call.
- **"Historical depth" and "Publication lag"** in the body are unevidenced. I left them alone and used neither on the page.
- **Dark mode.** As `mid-author.md` found, the site has no dark theme, so light and dark render the same.

## Screenshots

- **Method:**
  - 1440, 1024 and 768: headless Chrome, full page, cropped into sections and looked at.
  - True 390: the page in a 390 px iframe on a same-origin wrapper page (my own server on port 9735, now stopped).
  - Open states: a script clicked the frame-fold checkbox (`#fx`) and "Open the demo notebook".
- **Overflow:** `documentElement.scrollWidth` equals the viewport at 390, 768 and 1440, closed and open. The only elements outside the viewport are hero scenery SVG paths, which the hero crops by design.
- **Hero:** the scenery (turbines, pylons, labels), title, facts and key are fully visible at every width.
- **Chart:** fully visible, with its x label and key.
- **Raw feed:** the URL and commands wrap inside their wells at 390.
- **Frame:** it folds after `total_accepted_offer_volume_mwh` at 1440 and after `settlement_period` at 390. Unfolded, it scrolls inside its box.
- **Guide, notebook (open) and related list:** fully visible. The notebook `df` output is correctly aligned, and the plot's legend sits below the axes, clear of the lines.
- **Related notes:** they wrap cleanly.

## Template problems (not worked around)

1. **A wide table can chart only one column.** `chart_spec` takes a single `value` column, and several series need a `group` column. Market depth is wide: offers and bids are separate columns, with no category column. So the chart shows accepted offers only, and the caption and key note point to the notebook, which plots both. An option such as `values: [col, ...]` (unpivot before grouping) would let the chart show accepted offers above zero and accepted bids below it. The same limit will hit other wide tables.
2. **The frame cannot choose its columns.** `record.select` has no column list, so the frame keeps silver's order. The column the caption is about (`total_accepted_bid_volume_mwh`) sits behind the `…` fold at every width. The reader must unfold to see it.

## Open questions for the checker

- **The same-day null observation in `raw_feed.note`.** It is dated and scoped ("seen on 1 September 2026"), rests on a bronze file, and states no cause. It is the one place where a local capture informs page wording. Rule on whether it is a vendor-behaviour observation (allowed) or a description of local holdings (not allowed). If it is not allowed, the fallback is to cut the second clause and keep "The most recently fetched response wins each period."
- **The indicated-imbalance guide line.** It names a unit conflict inside gridflow rather than a unit. Check that this is the right way to report it, rather than simply "as sent".

## Revision 1 (2026-09-29, after `market_depth-review.md`: APPROVE with 2 nits)

- **Nit 1, evidence trail.** I added one bullet under the vault body's "Known issues and gotchas", "Same-day requests return nulls for later periods". It says the following:
  - A request for the current settlement date returns all 48 periods. The accepted and priced fields are sent as JSON `null` from a period that moves with fetch time.
  - `offerVolume`/`bidVolume` stay populated about four periods longer, and `indicatedImbalance` is sent for every period.
  - It cites bronze `market_depth/2026/09/01`: 15 fetches. The first null accepted period is SP10 at 04:15 UTC, SP18 at 07:57 to 08:14 UTC, SP20 at 09:13 UTC and SP24 at 11:17 UTC; for offer/bid it is SP14, SP21 to 22, SP24 and SP28.
  - It also cites `market_depth.py:42,113` for the latest fetch winning, and says the vendor does not document this.
  - Before writing it, I re-checked every fetch with a Python pass over the 15 bronze bodies.
- **Nit 2, wording.** `page.raw_feed.note` now says "returned null accepted volumes for the day's later periods". That is 30 words, inside the budget.
- **Checks:** the vault note was copied to the mirror (`cmp` clean). `gridflow-build --only elexon/market_depth` is green and `detect.mjs --json` returns `[]`. The rendered page carries the new wording. No artefact was re-generated: the chart spec and `record.select` are unchanged.
