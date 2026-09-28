# lolpdrm: author report (2026-09-29)

Page: `site/hifi/data-sources/elexon/lolpdrm.html` in the front-end worktree (`scratchpad/p26-elexon`).
Canonical note: `scratchpad/vault-p26-elexon/30-vendors/elexon/datasets/lolpdrm.md` (CRLF kept); mirror
`vault/elexon/lolpdrm.md` is byte-identical (`cmp` clean after the last edit).

## Status

- `gridflow-build --only elexon/lolpdrm`: passes (dataset template, distilled series carried).
- `detect.mjs --json`: `[]`.
- Artefacts: `site/hifi/data/series/elexon/lolpdrm.json` (`spec_origin: vault`, 3 series x 78 points, no
  `unmapped_groups`), `samples/elexon/lolpdrm.json` (`generated_by: gridflow-sample`, 8 rows),
  `notebooks/elexon/lolpdrm.json` + `lolpdrm-5.png` (run by `scripts/run_notebooks.py`, no errors).
- No staged chart spec or authored override existed for lolpdrm (the `rm -f` was a no-op).
- Screenshots checked at 1440, 1024, 768 and a true 390 (390 px iframe), notebook closed and open, frame
  folded and unfolded. Nothing clipped or overlapping. The site has no dark theme (no
  `prefers-color-scheme` or `data-theme` in `site/hifi/assets/`), so there is no dark mode to check.

## The reading chosen, and why

The vendor republishes LOLPDRM through the day, each publish forecasting the coming periods (bronze for
publishes of 2026-09-15: 48 publishes, one per half-hour, each from about 1 h ahead out to 03:30 UTC one or two
days on). Silver does not keep all of them: per bronze day it keeps one row per `(settlement_date,
settlement_period)` (see "Transformer behaviour" below), which in practice leaves two publishes per day, one
near 00:04 UTC (cut to the periods up to 12:30 the same day) and one near 12:05 UTC kept whole (13:00 that day
to 03:30 two days on).

The practitioner reading: how the de-rated margin forecast for the evening peak moves between a forecast about
a day ahead and one on the day. The chart plots `derated_margin_mw` from the three noon publishes of 13, 14 and
15 September, grouped by `published_at`. Where consecutive publishes overlap (13:00 to 03:30 next day), the
same evening appears twice, about 24 h apart: at 17:30 UTC on the 14th the later publish is 1,750 MW lower; at
17:00 on the 15th it is 1,747 MW higher. LOLP is not charted: in these publishes it is at most 4.4e-6 (visible
in the eight rows), so it cannot share an axis with MW; the eight rows carry it instead.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| title/summary: forecast per settlement period of LOLP and de-rated margin, republished as each period nears | `schemas/elexon.py:710-722` (fields, docstring); bronze 2026-09-15 has 26 publishes carrying period 2026-09-16 17:00 (lol2.py scan); chart shows the same period in two publishes |
| facts.vendor: dataset LOLPDRM | `connectors/elexon/endpoints.py:225-226` path `/datasets/LOLPDRM` |
| facts.cadence: repeated through the day; each publish names its half-hour publishing period | vendor field `publishingPeriodCommencingTime` in the note's bronze sample (02:30 for a 02:34 publish) and in bronze; notebook output shows 00:06 and 12:04 publishes on the same day |
| facts.grain: one row per settlement period from each day's publishes | `silver/elexon/lolpdrm.py:31-45` reads one bronze day; `:120` `unique(subset=[settlement_date, settlement_period], keep="last")`; `silver/base.py:417` `PARTITION_SOURCE_OFFSETS = (0,)`; bronze day = chunk start date `connectors/elexon/client.py:314` |
| Key: settlement_date, settlement_period, published_at | across all silver, `group_by(date, period, published_at)` has 0 duplicates; `group_by(date, period)` alone has 528 keys with 2 rows and 60 with 3 (a period is kept once per bronze day that forecast it) |
| what_it_is: LOLP unitless, 0 to 1 | `schemas/elexon.py:713,721` (`Field(ge=0.0, le=1.0)`, "unitless probability in [0, 1]") |
| what_it_is: de-rated margin "system margin after de-rating capacity for unavailability risk" | `schemas/elexon.py:714-715` docstring, quoted as the schema's words |
| what_it_is: the feed sends no unit; gridflow's column says MW | bronze records carry `deratedMargin` with no unit field (note's bronze sample; bronze 2026-09-15); column name `derated_margin_mw` `lolpdrm.py:67` |
| chart: 3 noon publishes, window 13 to 17 Sep, `aggregation: last`, one value per (period, publish) | committed series `provenance.rows_matched = rows_used = 234`, 3 x 78 points, `silver_first` 2026-09-13T13:00Z, `silver_last` 2026-09-17T03:30Z |
| chart_view.caption: each runs to 03:30 two days on; periods from 13:00 on the 14th and 15th appear twice | series: pub_13 13:00 13th to 03:30 15th; pub_14 13:00 14th to 03:30 16th; pub_15 13:00 15th to 03:30 17th |
| alt: lows 4,998 (16:30 13th), 8,389 (17:30 14th), 7,773 (16:30 16th); highest 26,302 (02:30 17th); later publish 1,750 lower at 17:30 on 14th, 1,747 higher at 17:00 on 15th | committed series: pub_13 min 4998.457, pub_14 min 8388.98, pub_15 min 7772.727, pub_15 max 26302.14; 10138.974 - 8388.98 = 1749.99; 13130.808 - 11384.242 = 1746.57 |
| key notes: 8,389 vs 10,139 at 17:30 on 14th; 13,131 vs 11,384 at 17:00 on 15th | committed series values above |
| raw_feed.note: 12-hour publish windows, the widest it accepts | `endpoints.py:219-229` comment and `max_chunk_hours=12` (24 h returns HTTP 400, exactly 12 h returns 200); note gotcha, live-verified 2026-07-30 |
| raw_feed.note: a day's bronze holds that day's publishes | `client.py:93-99` chunks from `--start` midnight UTC in 12 h steps; `client.py:314` `data_date = start.date()` |
| raw_feed.requests | `client.py:311-320` + `endpoints.py:277` format `%Y-%m-%dT%H:%M:%SZ`; bronze `.meta.json` `request_params` for 2026-09-15: `publishDateTimeFrom`, `publishDateTimeTo`, `page=1` in that order, no `format` |
| raw_feed.commands: ingest `--start 2026-09-13 --end 2026-09-16`, end exclusive | `pipeline/runner.py:479-500` (bare date = midnight UTC); `client.py:96` `while current < end` |
| raw_feed.commands: transform `--start 2026-09-13 --end 2026-09-15` | transform end inclusive (brief); no source offsets (`base.py:417`) so days 13 to 15 need only bronze 13 to 15 |
| record.caption: periods 37 to 40 on 14 Sep, from the 13 and 14 Sep noon publishes | sample rows: `published_at` 2026-09-13 12:04:53 and 2026-09-14 12:05:03 for each of SP 37 to 40 |
| record.fields.timestamp_utc: period start in UTC derived from date and period | `lolpdrm.py:93-102`, `utils/time.py:28-42`; SP38 on 14 Sep = 17:30 UTC (BST) |
| record.fields.settlement_period: 1 to 48; 46 or 50 on clock-change days | `utils/time.py:31-34`; schema `le=50` |
| record.fields.published_at: from `publishTime`, UTC | `lolpdrm.py:64,106-111` |
| record.fields.loss_of_load_probability: the schema expects 0 to 1 | `schemas/elexon.py:721`; validation is fail-soft (note: invalid rows logged, never dropped), hence "expects", not "guaranteed" |
| notebook.lead: relation `silver_elexon_lolpdrm`, filtered on `settlement_date` both ends included, not de-duplicated, lineage dropped | gridflow_models `research/handles/source.py:401-448` (`BETWEEN` on date col, no dedup, `SELECT * EXCLUDE`); `_get_method_registry.py:90-91`; `schema_manifest.py:128` date col; `relation_name_by_dataset()['lolpdrm']` = `silver_elexon_lolpdrm`; `bitemporal_exclude()` does not include `published_at` |
| notebook.needs: publishes of 13 to 15 September 2026 | query spans settlement dates 13 to 17; those rows come from publishes of 13 to 15, the ingest window above |
| plot_alt: six lines (00:06, 12:04 on 13th; 00:04, 12:05 on 14th and 15th); midnight lines stop at 12:30 UTC; lows near 5,000 (13th) and 7,800 (16th); highest near 26,300 early 17th | `lolpdrm-5.png` and silver: the 00:0x publishes hold periods 01:00 to 12:30 only |
| related.melngc: indicated margin per settlement period | melngc silver columns `settlement_date`, `settlement_period`, `indicated_margin` |
| related.ndf, system_prices, windfor | pages exist (`elexon.json` groups/families); notes state how to read them together, no causal claim |

## Note-body corrections (canonical note, smallest spans)

1. Overview: "the day-ahead reliability metrics published per settlement period" to "reliability forecasts per
   settlement period, republished through the day (see Publication lag)". Evidence: bronze 2026-09-15.
2. Publication lag: "Day-ahead publication." replaced with the observed republish pattern (dated to bronze of
   2026-09-15, "vendor docs not re-checked").
3. Dedup key: added ", within one bronze day only (see Known issues)". Evidence: `lolpdrm.py:31-45,120`.
4. Silver schema, `ingested_at`: "Time ingested into bronze." to "Stamped at silver transform time,
   `datetime.now(UTC)` (`silver/elexon/lolpdrm.py:122-126`)."
5. Silver sample `timestamp_utc` for SP10 on 2026-05-07: `04:30:00+00:00` to `03:30:00+00:00`
   (`utils/time.py:28-42`; SP1 in BST starts 23:00 UTC the day before; matches the bronze sample's
   `startTime` 03:30).
6. Known issues: new bullet on the per-bronze-day `keep="last"` dedup and its consequences, plus that
   `publishingPeriodCommencingTime` is renamed then dropped and `startTime` is not carried.

The curl example (`format=json`, 3 h window) is valid for the vendor and was left alone.

## Transformer behaviour (open question for gridflow, not fixed here)

`lolpdrm.py` concatenates the bronze day's files in `sorted(glob("raw_*.json"))` order (`:42`); file names
share the run timestamp and end in a random 8-hex suffix, so the order of the day's two 12-hour chunk files is
arbitrary. Bronze rows arrive newest publish first. `unique(..., keep="last")` (`:120`) with no sort on
`published_at` therefore keeps the earliest publish carrying each period in whichever file is read last:
- usual case (00-12 file first): ~00:04 publish for periods to 12:30 that day, ~12:05 publish for the rest;
- flipped order (seen for 2026-08-02, 08-05, 09-19): ~00:04 publish to 03:30 next day, then ~11:04.

So silver is neither "latest publish" nor a fixed lead time, and a re-transform can keep different publishes
on different machines. The page states only the code facts (one row per period from each day's publishes) and
names the publishes it charts; it never says "latest" or "day-ahead". Worth a gridflow issue: sort by
`published_at` before dedup (or keep every publish, as windfor does) and bump `DATASET_VERSION` (still the base
default `1.0.0`, `base.py:708`).

## Unverified

- Elexon or NESO documentation of LOLPDRM cadence and horizons: not quoted anywhere in the repo or vault, so the
  page gives no cadence count and no horizon rule, only what the chart and rows show. No `history` fact.
- Any link from LOLP to the reserve scarcity price in imbalance pricing: nothing in the repo evidences it, so
  the page does not claim it (`system_prices` is related only as "to test against").
- The vault Overview's definitions ("probability that demand exceeds available generation"; "available MW
  above expected demand after de-rating intermittent capacity") are not in code; the page uses the schema
  docstring's wording instead. Left in the note body, unverified.
- Bronze records carry `dataset: "LOLPDM"` although the path is `LOLPDRM`; not surfaced on the page.

## Open questions

1. The transformer dedup above (gridflow issue candidate).
2. Series paints: clay, petrol, horizon (the windfor precedent). Petrol and horizon are close where the
   14th and 15th publishes overlap; readable at all widths, but olive for `pub_15` would separate them more.
   Taste call for Bobbo.

## Template observations (no workaround made)

- At 768 and 390 the frame folds everything after `settlement_period`/`timestamp_utc` behind `…`, so the
  column that matters (`loss_of_load_probability`) is only seen unfolded; unfolded, the frame scrolls sideways.
  This is the template's fold rule, same on every page.
- At 390 the notebook's `head()` frame scrolls sideways inside `.df-wrap` (template behaviour).
- `head()` was narrowed to three columns so it fits at 1024 and 1440; the notebook legend is placed outside
  the axes so it does not cover the 15 September line's overnight high.

## Screenshots

Scratchpad `lol-shots/`: `p<width>-o0-*.png` (notebook closed), `p<width>-o1-*.png` (notebook open) for 1440,
1024, 768 and 390 (390 via a 390 px iframe in `lol-shots/wrap.html`), `u768-*.png`, `u390-*.png`,
`u1440-*.png` (frame unfolded). Static server on 9724 stopped. Headless Chrome used its own profile
(`scratchpad/lol-chrome`).
