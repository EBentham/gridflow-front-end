# System inertia (`system-inertia`): writer's report

One-table package page, lead key `system_inertia` (the manifest is right: one table, one family, no held members).
Canonical note `C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\system-inertia.md` (page block
added, two body edits; 281 lines, all CRLF); mirror `C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\system-inertia.md`
(`cmp` clean). Artefacts: `site\hifi\data\series\neso_data_portal\system_inertia.json`,
`samples\neso_data_portal\system_inertia.json`, `notebooks\neso_data_portal\system_inertia.json` and
`system_inertia-6.png`. No staged chart spec or authored override existed.

## Status

- `gridflow-build --only neso_data_portal/system_inertia`: passes first time on budgets; only the unrelated global
  warning about 35 dropped "Known issues" lines.
- Detector `detect.mjs --json`: `[]`.
- Rendered page text: 0 em or en dashes, arrows, middle dots; no "locally", "held", "our", "since 20", "live", "now",
  "real-time", planning words.
- Screenshots taken at 1440, 1024, 768 and 390 (390 in a 390 px iframe), my server on 9882 started with the batch
  method (PID 20566) and stopped by that PID. Nothing clipped or overlapping: hero and scenery, chart and key, raw feed
  wells, folded frame and guide, notebook panel, related list. At 390 the folded frame shows two columns and the `…`,
  and long keys break inside their wells, as the template intends. Unfolded frame not opened (headless, no click).
  After the first screenshots I added `chart_view.y_min: 60`: the auto floor was 0, which squeezed both lines into the
  top half.

## 1. What one row is

| Claim | Evidence |
|---|---|
| One row = one settlement period of one settlement date, from one financial-year file | Registry `registry/system-inertia.json`: `entity_key` `[resource_id, settlement_date, settlement_period]`, `temporal: sp_pair`, `latest: whole_capture` per `resource_id`; 10 resources, each "GB System Inertia - YYYY-YYYY", one CSV per financial year |
| Columns: `Settlement Date`, `Settlement Period`, `Outturn Inertia`, `Market Provided Inertia`; no split, no forecast, no issue column | Registry epoch header; NESO resource description (catalogue snapshot `20261006T195819Z`): "Estimate of the market provided and outturn inertia for the GB Transmission System per settlement period." |
| Outturn: generators > 15 MW or operating to provide inertia, plus a demand-side estimate | NESO field info (`gridflow\.planning\research\neso-snapshots\field-info\20261008T114228Z\system_inertia.json`): "This is the sum of the estimated inertia of each of the generators with a power output > 15 MW or operating to provide inertia and an estimate of the demand side contribution" |
| Market-provided: same calculation, generator positions recalculated without NESO's actions (trades, BOAs) | Same file: "calculated in the same way as the outturn inertia but with the position of the generators recalculated to remove the impact of actions taken by NGESO", listing "Trades" and "Bid Offer Acceptance (BOAs)" |
| Unit GVA.s, written `GVAs` by NESO | Same file: `"unit": "GVAs"` on both inertia columns; Outturn description "in GVAs". Page prints GVA.s and says "NESO writes GVAs" once |
| Excludes Stability Pathfinder units | Package notes (snapshot): "It does not include the contribution from Stability pathfinder units" |
| Updates paused; catalogue says weekly | Package notes: "Updates to the System Inertia dataset have been temporarily paused while we review and validate the most appropriate data available."; `extras` "Update frequency: Weekly" |
| History from 2017-18 | The 10 resources the catalogue lists, 2017-2018 to 2026-2027 |
| Integers as supplied, no nulls | Registry int64, nullable; silver 0 nulls in both columns over all 10 files |
| Outturn above market-provided on 354 of 365 chart days | Committed series (alt text and key are scoped to the chart window) |

## 2. Times and the clock

| Claim | Evidence |
|---|---|
| `timestamp_utc` = start of the period: settlement day starts 00:00 UK local, periods step 30 min of real time | `utils/time.py:28` `settlement_period_to_utc`; applied in `silver/neso_data_portal/casting.py:611-632` for `sp_pair` |
| NESO's periods follow the UK settlement day (scoped to the rows) | Silver: every spring clock-change day 2018-2026 has 46 periods and every autumn one 50, except 2022-10-30 (periods 1 and 2 only). Sorted `timestamp_utc` steps exactly 30 min across all 162,424 rows, except across the 21 short days (20 gaps of 1,410 min, one of 1,470); no repeated instant |
| Frame: 26 October 2025 period 1 = 2025-10-25 23:00 UTC, period 50 = 2025-10-26 23:30 UTC | The eight sample rows; notebook cell output |
| `event_time` = `timestamp_utc`; `available_at` = `published_at` = CKAN `last_modified` | Silver: 0 differences on all rows; registry `vintage: ckan_last_modified`; sidecar `ckan_last_modified` 2026-05-20T10:37:49.212185 for the 2025-26 file equals the frame's `published_at` |
| Workbench | `query()` reads `silver_neso_data_portal_system_inertia_latest`, date column `settlement_date` typed DATE, so `BETWEEN start AND end` (both included) (`_get_method_registry.py:62-96`, checked in the gridflow_models venv); lineage columns excluded (`source.py` `_present_bitemporal_exclude_clause`). Returns session-zone times (batch checked fact); the query cell converts `timestamp_utc` to UTC and its output shows `+00:00` |

## 3. Captures, truncation, repeats

One capture per file, all on 8 October 2026 (bronze `system_inertia/2026/10/08/`, 10 CSVs + sidecars). **No 16 October
recapture** exists for this package. Silver: one Parquet per file, all written 2026-10-08.

| File (FY) | Bronze rows | Silver rows | Body bytes = declared length | Distinct (date, period) | `last_modified` |
|---|---:|---:|---|---:|---|
| 2017-18 | 17,520 | 17,520 | 399,754 = 399,754 | 17,520 | 2021-07-01 10:44:28 |
| 2018-19 | 17,520 | 17,520 | 399,736 = 399,736 | 17,520 | 2021-07-01 10:56:25 |
| 2019-20 | 17,568 | 17,568 | 400,831 = 400,831 | 17,568 | 2021-07-01 10:58:44 |
| 2020-21 | 17,520 | 17,520 | 399,509 = 399,509 | 17,520 | 2021-07-01 11:00:55 |
| 2021-22 | 17,520 | 17,520 | 399,607 = 399,607 | 17,520 | 2022-04-04 10:31:22 |
| 2022-23 | 17,472 | 17,472 | 398,352 = 398,352 | 17,472 | 2023-04-04 15:40:55 |
| 2023-24 | 17,476 | 17,476 | 398,001 = 398,001 | 17,476 | 2024-04-11 07:51:13 |
| 2024-25 | 17,520 | 17,520 | 397,652 = 397,652 | 17,520 | 2025-05-14 09:56:49 |
| 2025-26 | 17,520 | 17,520 | 397,021 = 397,021 | 17,520 | 2026-05-20 10:37:49 |
| 2026-27 | 4,788 | 4,788 | 108,079 = 108,079 | 4,788 | 2026-07-27 14:01:47 |

No truncation (bronze body = NESO's declared length; bronze rows = silver rows), no repeats within or across files
(162,424 rows, 162,424 distinct date-period pairs; the years do not overlap; no date missing from 2017-04-01 to
2026-07-26). `dedup: {on: [settlement_date, settlement_period], order_by: capture_written_at}` is set on the chart
and the frame as a guard (`duplicates_dropped: 0`); `capture_written_at` so a future recapture of the same file
version, which would share `published_at`, still keeps the newest.

## 4. Chart

`system_inertia`, line, two series through `values` (`outturn_inertia`, `market_provided_inertia`), `time:
settlement_date`, `aggregation: min` per settlement day, each column on its own, window 1 April 2025 to 31 March 2026
(the 2025-26 file, the newest complete year; every day has 46, 48 or 50 periods), 365 points per series, unit GVA.s,
`y_min: 60`.

Series (committed file): outturn daily low 107 to 252, median 125, lowest 107 on 2026-02-21, highest 252 on
2026-01-05; market-provided daily low 71 to 248, median 101, lowest 71 on 2025-05-04, highest 248 on 2026-01-05.
Outturn higher on 354 days, lower on 4 (2025-10-13, 2025-11-07, 2026-01-19, 2026-03-07, by 1 to 4), equal on 7.
Why it is useful: the outturn floor sits near 110 to 120 while the market-provided floor falls to 71 to 100, which is
NESO's own definition of the difference (its actions) read at each day's lowest point. The caption says the lows are
taken separately (they can fall in different periods); it states no cause beyond NESO's definitions.

Frame: 26 October 2025 (clocks back), periods 1 to 6, 49, 50: shows period 1 at 23:00 UTC the evening before, period
5 at 01:00 UTC (the repeated local hour) and period 50. Notebook (6 cells, 6.6 s, no errors): the clock-change day's
periods 1, 2, 49, 50 in UTC; periods per day in the window (48: 363 days, 50: 1, 46: 1); min, median and max of the
daily lows (matching the chart); a plot of the daily lows.

## Body corrections

1. Known issues, "Sparse days": added that each sparse day carries periods 1 and 2 only, and that the 2022-23 one is
   the autumn clock-change day 2022-10-30 (silver, `group_by(settlement_date)`).
2. Known issues, "Settlement period range": "Spring and autumn clock-change days have 46 and 50 periods" now adds
   "except 2022-10-30, which carries only periods 1 and 2". Not changed: the Units bullet's "Clock-change days carry
   46 or 50 periods" (same point; left to keep the edit small; the seat may prefer the same clause there).
3. Known issues: new bullet "Whole low days" (five days, numbers below) with a TODO for NESO.

## Unverified

- Whether the five whole low days and the 21 short days are NESO errors or real: NESO says nothing. Neither is in the
  chart window or the frame.
- Whether NESO revises a closed year's file on re-upload: one capture per file exists.
- "Times come back in UK time" relies on the batch's checked fact; I saw only the converted output.
- The catalogue snapshot's `size` for the 2024-25 file is 15,357 bytes, while the body NESO served is 397,652
  (= its declared content length). CKAN metadata, not used on the page.

## Open questions and template problems

- None blocking. The notebook panel on the page numbers the query cell `[2]` (the setup cell is `[1]`, the help card
  is not shown) while the runner prints it as `In [3]`; I worded the lead without cell numbers. The frequency page's
  lead says "cell 3" and "cell 5", which a reader of that page's panel would count differently (seat item).

## Defects

- **NESO data: five whole days of implausibly low system inertia.** `system_inertia` silver (bronze 2026-10-08):
  on 2022-03-19, 2022-06-08, 2023-01-05, 2023-09-30 and 2026-06-01, `outturn_inertia` is below 100 GVA.s in 46 to 48
  periods (day lows 50, 54, 52, 44, 43; 2022-03-19 runs 50 to 76 all day) while the days either side have lows of 109
  to 207. `market_provided_inertia` falls with it (lows 51, 72, 52, 49, 59). Silver accepts them (no range rule on the
  inertia columns). Question for NESO: are these valid estimates? Until answered, a consumer taking daily or annual
  minima gets them.
- **NESO data: 21 days carry only settlement periods 1 and 2**, including the autumn clock-change day 2022-10-30
  (2022-23 file); also 2023-09-26 and 2023-10-11 (2023-24) and 18 days from 2026-05-18 to 2026-06-28, mostly every
  other day (2026-27). The note's INERTIA-SPARSITY TODO covers the count; this adds that the kept periods are always
  1 and 2, which reads like a truncated day rather than a sparse one.
