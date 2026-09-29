# pn (Physical notifications) author report

Writer: Opus 5.5, 2026-09-29. Screenshot port 9741 (server stopped).

## Status

- `gridflow-build --only elexon/pn`: passes (dataset template, series digest, related pages resolve).
- `detect.mjs --json site/hifi/data-sources/elexon/pn.html`: `[]`.
- Artefacts, all written by the tools from real data:
  - `site/hifi/data/series/elexon/pn.json` (`gridflow-distil`, `spec_origin: vault`, 3 series x 336 points, no nulls);
  - `site/hifi/data/samples/elexon/pn.json` (`gridflow-sample`, 8 rows);
  - `site/hifi/data/notebooks/elexon/pn.json` and `pn-5.png` (`scripts/run_notebooks.py`, 5 cells, no errors).
- No staged spec or authored override existed for `pn`; the `rm -f` was a no-op.
- Vault note is CRLF on all 273 lines; the mirror `vault/elexon/pn.md` is byte-identical (`cmp`). The old mirror
  was LF. After `cp` it is CRLF, like the other batch mirrors (`agws`, `mid`, `windfor`, `boal`).
  `.gitattributes` has `*.md text eol=lf`, so git normalises it on commit.
- Chart: `line`, `level_from` in MW for three BM units (`T_PEMB-11` Pembroke CCGT, `T_DINO-5` Dinorwig pumped
  storage, `T_SGRWO-6` Seagreen offshore wind). It covers every half-hour of settlement dates 16 to 22 September 2026.
  Aggregation is `last` over exactly one row per unit and period, so nothing is summed.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Request is `GET https://data.elexon.co.uk/bmrs/api/v1/datasets/PN?settlementDate=2026-09-20&settlementPeriod=1&page=1` (`raw_feed.requests`) | `endpoints.py:94-98` (`ParamStyle.SETTLEMENT_DATE_PERIOD`, defaults `date_param="settlementDate"`, `period_param="settlementPeriod"`); `build_params` `endpoints.py:291-313` adds `page`. Bronze meta `C:\gridflow-data\bronze\elexon\pn\2026\09\20\raw_20260926T183441Z_979401eb.meta.json`: `request_url` is exactly this URL, `total_pages` 1. |
| One call per settlement period of each date, 46, 48 or 50 (`raw_feed.note`) | `client.py:184-188`: `period_count = settlement_periods_in_day(settlement_date)`, `for period in range(1, period_count + 1)`; the docstring at `client.py:167` says 46/48/50. |
| Ingest `--end` date is fetched; ingest and transform share the window 16 to 22 Sep (`raw_feed.commands`) | `pipeline/runner.py:497-500`: a bare `--end` becomes midnight UTC. `client.py:360-372` `_date_range` loops `while current <= end_date` on `.date()`, so 22 Sep is fetched. Bronze is filed by `data_date=settlement_date` (meta above). `pn.py` has no `PARTITION_SOURCE_OFFSETS`, so the default is `(0,)` (`silver/base.py:417`), and period 1 (23:00 UTC the evening before) sits in its own settlement date's partition: no widening. |
| Silver keeps one segment per unit and period, the last one received, and drops the times (`what_it_is`, `facts.grain`, `record.fields.level_from/level_to`) | `pn.py:58-64`: `column_mapping` has no `timeFrom`/`timeTo`/`nationalGridBmUnit`. `pn.py:98-101`: `unique(subset=[settlement_date, settlement_period, bm_unit_id], keep="last")`. `pn.py:111-120`: `output_cols` has no times. `read_bronze` reads files in `sorted()` name order (`raw_<fetch timestamp>_...`), so "last" is the last one received. |
| Elexon sends each unit's period as segments with a start and end time and a MW level at each (`what_it_is`) | Bronze keys: `dataset, settlementDate, settlementPeriod, timeFrom, timeTo, levelFrom, levelTo, nationalGridBmUnit, bmUnit`. On 2026-09-20, 119,471 non-null unit-periods: 114,782 have one 30-minute segment; the rest have 2 to 6 segments. Example SP10 `2__BCMRO002`: 03:30-03:31 0 to -42, 03:31-03:32 -42 to -42, 03:32-03:33 -42 to -41, 03:33-03:59 -41, 03:59-04:00 -41 to 0. Silver row: `0.0 / -42.0` (visible in the eight rows). |
| "Here each kept segment starts its period" (`chart_view.caption`, scoped to the window) | Bronze-to-silver join for settlement dates 16 to 22 Sep: every non-null silver row equals the latest capture's segment whose `timeFrom` equals `timestamp_utc`. The one exception is 48 rows on 2026-09-21: two supplier units, `2__DSTAT008` and `2__NSTAT005`, 24 periods each, absent from the latest capture and kept from an earlier one. All three charted units match in every period. |
| BSC definition, "export or import ... absent any acceptances" (`summary`, `what_it_is`) | Elexon glossary, https://www.elexon.co.uk/glossary/physical-notification/, quoted verbatim in the note's Overview (added). |
| Sign not stated (`chart_view.key[dinorwig].note`) | The Elexon glossary PN and Import entries were read 2026-09-29; neither states which sign is export. The vault domain notes (`20-domain/markets/gb-balancing-mechanism.md`, `20-domain/concepts/bm-units.md`) say nothing about sign. The page describes negative values as shape only. |
| Unit identities: Pembroke 11 CCGT, Dinorwig 5 PS, Seagreen 6 WIND (`chart_view.key`) | Silver `elexon/bmunits_reference`: `T_PEMB-11` "Pembroke Unit 11", CCGT; `T_DINO-5` "Dinorwig 5", PS; `T_SGRWO-6` "Seagreen1 Offshore WF 6", WIND. |
| Alt numbers (`chart_view.alt`) | Committed series: Pembroke min 0, max 435. Near 430 on 16 Sep (steps up 05:00-05:30 UTC, to 0 at 22:00 UTC), 0 until the 20 Sep ramp (123 at 17:00 UTC, 411 at 17:30 UTC), then 219 to 435. Dinorwig min -293 (2026-09-18 09:30 UTC), max 300. Seagreen min 1, max 354 (19th), 353 on the 20th, 2 on the 22nd. |
| Notebook plot alt (`notebook.plot_alt`) | `pn-5.png` as rendered, the same `T_DINO-5` values: 300 blocks on six of seven evenings plus the morning of the 18th; stretches of -257 to -293 on the 17th, 18th, 19th and 20th; a -263 dip on 22 Sep 04:00 UTC. |
| `timestamp_utc` is the half-hour start, computed from date and period (`record.fields`) | `pn.py:86-95` `settlement_period_to_utc`. `settlement_period_to_utc(2026-09-20, 1)` = 2026-09-19 23:00 UTC. |
| `bm_unit_id`: units sent without one share a null row per period (`record.fields`) | Bronze 2026-09-20: 2,208 records with `bmUnit` null, 46 per period, each with only `nationalGridBmUnit` (for example `IVG-VKL1`, `IBG-ENGI1`, `COALD-1`, `BENTB-1`). Silver 2026-09-20: 48 null `bm_unit_id` rows, one per period. The mechanism is a code fact: the dedup subset includes `bm_unit_id`, and polars `unique` treats nulls as equal. |
| Notebook lead: relation `silver_elexon_pn`, `settlement_date` inclusive, lineage dropped, ordered by `settlement_date` only | gridflow_models `_RELATION_NAME_BY_DATASET["pn"]` = `silver_elexon_pn`; `DESIGNATED_DATE_COLS[("elexon","pn")]` = `settlement_date` (`gridflow/silver/schema_manifest.py:136`). `source.py:401-451`: `_date_range_predicate` is inclusive, `EXCLUDE` covers `_BITEMPORAL_EXCLUDE` (`event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year`), `ORDER BY settlement_date`. |
| Eight rows: 2026-09-20, SP10, one kept segment each (`record.caption`) | `samples/elexon/pn.json`: 8 rows, all `2026-09-20`, period 10, `timestamp_utc` 03:30 UTC. |
| Related: `uou2t14d` is each unit's declared available output 2 to 14 days ahead | Vault `uou2t14d.md` Overview; `silver/elexon/uou2t14d.py:26,74` (key `settlement_date, bm_unit_id`, `output_usable_mw`). |

## Note-body corrections (canonical vault note)

1. **Overview**: added the verbatim BSC glossary definition with its URL and read date, plus a line that the
   glossary gives no sign rule. This is the evidence for the page's definition and sign wording.
2. **Silver schema, `bm_unit_id`**: Nullable changed from "No" to "Yes (in practice)". Added the null-`bmUnit`
   units and their collapse into one row per period (`pn.py:58-64,98-101`).
3. **Silver schema, `level_from` / `level_to`**: changed "at start/end of period" to "of the kept segment".
4. **Silver schema, `ingested_at`**: changed "Time ingested into bronze" to the silver transform time
   (`pn.py:103-108`, `datetime.now(UTC)`).
5. **Silver sample**: `timestamp_utc` for 2026-05-06 SP24 changed from 11:30 to 10:30 UTC.
   `settlement_period_to_utc(2026-05-06, 24)` returns 10:30; the bronze sample's `timeFrom` 10:59 to `timeTo`
   11:00 agrees.
6. **Known issues**:
   - "iterates periods 1..50" became 1..N from `settlement_periods_in_day` (`client.py:184-188`).
   - The "Stop-on-empty ... breaks early" bullet was wrong. An empty page 1 skips only that period and the loop
     continues; an empty later page raises (`client.py:207-220`). The bullet was replaced.
   - Added a bullet on the kept segment and the dropped segment times, with the 16 to 22 Sep check and the
     `2__BCMRO002` example.
7. **Implementation delta**: "iterates periods 1..50" became 1..N (46/48/50), with citations.

The curl example was left unchanged (it is valid for the vendor), and so was `last_verified`.

## Unverified

- PN sign convention (which sign is export). It is not in the sources quoted, so the page says so and does not
  interpret Dinorwig's negative stretches as pumping.
- Whether the vendor's response order reliably lists a unit's period-start segment last. It held for 16 to 22 Sep
  apart from the re-capture case, but it is not a code or vendor rule. The page scopes the claim with "Here".
- Vault "Publication lag: ~hour before delivery (gate closure)". Not checked and not used on the page.

## Open questions and findings for the seat (gridflow, not front-end)

1. **Silver loses the PN level path.** `pn.py` drops `timeFrom`/`timeTo` and keeps one segment per unit and period.
   On 2026-09-20, 4,690 unit-periods had 2 to 6 segments, and `level_to` of the kept segment is often not the
   period's end level (`2__BCMRO002` SP10 reads -42 but ends the period at 0). A BM-unit dispatch model needs the
   full path. This would be a gridflow unit: add `time_from`/`time_to` to the key and schema, plus a
   `DATASET_VERSION` bump.
2. **Silent unit loss on null `bmUnit`.** 46 units per period arrive with only `nationalGridBmUnit`, many of them
   interconnector units (`I?G-*`, `I?D-*`). Silver keeps one arbitrary one of them as a null-key row and drops
   `nationalGridBmUnit`. `ElexonPN.bm_unit_id: str` is declared non-null but not enforced on this path.
   `uou2t14d.py` already maps `nationalGridBmUnit`, so there is a precedent.
3. `ElexonPN` has no `DATASET_VERSION` override; silver carries `1.0.0`.

## Template problems

None blocking. Two observations:

- At 768 and 390, the unfolded frame and the notebook's DataFrame output scroll horizontally inside
  `.df-wrap { overflow-x: auto }`. That is by design, but a reviewer may read it as clipping.
- The line renderer plots each value at the middle of its half-hour (`chart_svg.py` `_lines`: `plot.X(t + half)`),
  while `level_from` here is the level at the half-hour's start. The shift is sub-pixel at this scale, and the
  page does not claim a plotting position.

## Screenshots checked (light only; the site has no dark theme)

Headless Chrome, full page at 1440, 1024 and 768; 390 through a 390 px iframe. Each width was shot twice: as
served, and as a scratch copy with the notebook drawer opened and the frame unfolded (`#fx` checked).

- Hero scenery (turbines, "transmission lines", "substation", "battery storage"), the chart and its key, the raw
  feed, the frame and guide, the notebook drawer and related datasets: nothing clipped or overlapping at any width.
- The `market` landscape has no "generation data" label problem.

I also ran one read-only `git status` in the worktree to list my artefacts. No other git commands were run.
