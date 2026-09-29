# elexon/windfor: author report

Writer, 2026-09-28. Page: `site/hifi/data-sources/elexon/windfor.html` (front-end worktree `p26-elexon`).

## Status

- `gridflow-build --only elexon/windfor`: passes. `detect.mjs --json`: `[]`.
- Canonical note edited in the vault worktree (`30-vendors/elexon/datasets/windfor.md`, CRLF kept: 254 lines, 254 CRLF). Mirror `vault/elexon/windfor.md` is byte-identical (`cmp`).
- Artefacts, all from real data: `site/hifi/data/series/elexon/windfor.json` (`gridflow-distil`, `spec_origin: vault`), `samples/elexon/windfor.json` (`gridflow-sample`), `notebooks/elexon/windfor.json` + `windfor-5.png` (`scripts/run_notebooks.py`; 5 cells, no errors, read-only).
- No staged spec or authored override existed for windfor (`rm -f` was a no-op).
- Chart: `line`, three issues published on 20 Sep 2026 (03:30, 12:30, 23:30 UTC), grouped on `published_at`. Fixed window of target hours 20 to 22 Sep, 69 hourly points each, from 00:00 UTC on the 20th to 20:00 UTC on the 22nd.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Silver has only `timestamp_utc`, `latest_forecast_mw`, `published_at` plus pipeline columns; no `settlement_date`, `settlement_period` or `initial_forecast_mw` (record.fields, note body) | `pl.read_parquet_schema` over all 1850 silver files: one schema, `(timestamp_utc, latest_forecast_mw, published_at, data_provider, ingested_at, event_time, available_at, source_run_id, dataset_version)`. Transformer selects only present columns: `silver/elexon/wind_forecast.py:175-186` |
| The raw `/datasets/WINDFOR` row is `dataset, publishTime, startTime, generation` (integer), with no settlement fields and no initial/latest split | Elexon OpenAPI (Insights.Api; local copy `scratchpad/swagger.json`, captured 2026-09-27), schema `Insights.Api.Models.Responses.Generation.DatasetRows.WindGenerationForecast`. Local bronze `2026/09/20/raw_20260926T183115Z_6e2dbbfd.json`: key set `{dataset, publishTime, startTime, generation}` |
| `timestamp_utc` is the target hour from vendor `startTime` (fields, notebook) | `wind_forecast.py:133-140` (the `start_time` branch; `has_sp` is false because no settlement fields arrive). Every `timestamp_utc` minute is 0 (value_counts on the 20 Sep file) |
| `published_at` is the vendor `publishTime`, UTC | `wind_forecast.py:96-97, 146-151` |
| `latest_forecast_mw` comes from `generation`; MW only by gridflow's column name, and the feed sends no unit (what_it_is, fields) | `wind_forecast.py:95` (`generation` -> `latest_forecast_mw`), `:142-144` (cast Float64). The OpenAPI row schema has no unit field |
| Key `(timestamp_utc, published_at)`; grain is one row per target hour and issue time (facts.grain, record.key) | Dedup `wind_forecast.py:160-165` (settlement fields absent, so `["timestamp_utc", "published_at"]`, keep last). Polars: 0 duplicates of `(timestamp_utc, published_at)` across Aug to Sep 2026 |
| "Up to eight issues a day, per Elexon's API docs" (summary, facts.cadence) | OpenAPI descriptions of `/forecast/generation/wind` and its variants: published by NGESO up to 8 times a day at 03:30, 05:30, 08:30, 10:30, 12:30, 16:30, 19:30 and 23:30. Silver 14 to 26 Sep: 8 publish times a day at exactly those clock times (UTC) |
| "covers wind farms the ESO can see through operational metering" (what_it_is) | Same OpenAPI descriptions: "wind farms which are visible to the ESO and have operational metering" |
| "those charted, all published on 20 September, run to 20:00 UTC on the 22nd" (what_it_is) | Visible in the chart: series `x` ends `2026-09-22T20:00:00Z`. Each 20 Sep issue: tmax 2026-09-22 20:00 UTC |
| Request URL (raw_feed.requests) | `endpoints.py:152-156` (PUBLISH_DATETIME), `client.py:93-99` (24 h chunks, `max_chunk_hours=24`), `endpoints.py:300-313` (`_to_utc_z`, `page`). Matches bronze `.meta.json` `request_params` exactly |
| "a day's bronze holds the issues published that day" (raw_feed.note) | `client.py` `_fetch_datetime_range`: `data_date = start.date()` (chunk start). Meta `data_date: 2026-09-20` for the 20 Sep window. Silver file `windfor_20260920` holds only `published_at` on 20 Sep (8 issues x 73 rows = 584) |
| Ingest `--start 2026-09-20 --end 2026-09-21`, end exclusive | `runner.resolve_dates`: a bare date means midnight UTC. PUBLISH_DATETIME loops `while current < end` (`client.py:95-99`), so one window 20 Sep 00:00 to 21 Sep 00:00. No `PARTITION_SOURCE_OFFSETS` in the transformer; silver day D reads only bronze day D (`read_bronze(target_date)`) |
| Transform `--start 2026-09-20 --end 2026-09-20`, end inclusive | `runner.run_transform` docstring "Window end (date taken, inclusive)"; `date_range(start.date(), end.date())` |
| Chart numbers (alt, key note): all three peak at 20,629 at 01:00 on the 20th; lows 4,769 / 4,017 / 3,449 early on the 21st; each later issue lower from 02:00 to 23:00 on the 21st; ends 2,815 / 2,287 / 1,603; 4,106 against 6,338 at 12:00 UTC on the 21st | Read from the committed `series/elexon/windfor.json` (script output in session). The strict ordering 03:30 > 12:30 > 23:30 holds for 22 hours on the 21st, 02:00 to 23:00, and not at 00:00 or 01:00. The alt is scoped to that span |
| "Where lines meet, the later issue repeats hours already begun" (caption) | Committed series: all three equal only for 20 Sep 00:00 to 03:00 (begun before the 03:30 issue). 12:30 equals 23:30 exactly for 20 Sep 00:00 to 12:00 (begun before 12:30) and diverges from 13:00. Scoped to the chart |
| Eight rows: target 21 Sep 12:00 UTC, one per 20 Sep issue, 6,338 down to 4,106 (record.caption) | `samples/elexon/windfor.json` rows |
| Notebook lead: relation `silver_elexon_windfor`, filtered on `timestamp_utc`, whole UTC days, both ends included, lineage dropped | gridflow_models registry: relation `silver_elexon_windfor`, date column `timestamp_utc`, type TIMESTAMPTZ. `_date_range_predicate` uses half-open UTC `[start 00:00, end+1 00:00)` (`_get_method_registry.py:62-96`). `_BITEMPORAL_EXCLUDE` = `event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year`. Windfor is not APPEND_ONLY, so there is no `_latest` view |
| Notebook `df.published_at.dt.day == 20` selects exactly the 20 Sep issues | The query covers targets 20 to 22 Sep. Issues covering those hours are published 18 to 23 Sep (each spans 20:00 UTC D-1 to 20:00 UTC D+2), all in September |
| plot_alt numbers: start near 20,300 (20,316), lows 3,400 to 4,800 on the 21st (3,449 to 4,769), end 1,603 to 2,815 | Pivot of the 20 Sep file (all eight issues); matches the notebook PNG |
| Related: FUELHH has a WIND code per settlement period; AGWS is "actual or estimated" wind (onshore, offshore) per settlement period; FUELINST is 5-minute outturn by fuel; NDF is a demand forecast | fuelhh note/page (WIND code). OpenAPI `/generation/actual/per-type/wind-and-solar` ("actual or estimated ... Wind Onshore or Wind Offshore ... per settlement period"). `elexon.json` page set; the fuelinst and temp pages |

## Note-body corrections (vault note, smallest spans)

1. **Overview**: "published per settlement period. Each row carries an initial-issue forecast and a latest-issue forecast in MW" was wrong. It now says the forecast is hourly and reissued up to 8 times a day (OpenAPI `/forecast/generation/wind`), and gives the row fields and the absence of the initial/latest split (OpenAPI `DatasetRows.WindGenerationForecast`). The unverified "canonical ... benchmarked" sentence was left as is.
2. **Publication lag**: "Multiple publishes per day" became "Up to 8 issues a day (Elexon OpenAPI, `/forecast/generation/wind`)".
3. **Dedup key**: the "_inline in transformer_" placeholder became `(timestamp_utc, published_at)`, keep last (`wind_forecast.py:160-165`). It also notes that the silver file date is the publish-window date (`connectors/elexon/client.py:314`, `wind_forecast.py:60-84`).
4. **Silver schema table**:
   - `settlement_date`, `settlement_period` and `initial_forecast_mw` are marked as not written (`:175-186`);
   - `timestamp_utc` source is `startTime` (`:133-140`), not `settlement_period_to_utc`;
   - `latest_forecast_mw` source is `generation` only;
   - `published_at` is typed UTC (`:146-151`);
   - `ingested_at` is the silver transform time (`:167-173`), not the bronze ingest time.
5. **Silver sample**: the placeholder row with `issue_time` and settlement fields became a real row (21 Sep 12:00 target, 03:30 issue, from the 20 Sep silver file).
6. **Known issues**: the stale "`initial_forecast_mw` vs `latest_forecast_mw`" bullet now says revisions are rows keyed by `published_at`, and that `initial_forecast_mw` is never written.

Not changed: the curl example (`publishDateTime...` with `format=json`, valid for the vendor); `last_verified` (I did not re-run the live validator); pre-existing em dashes elsewhere in the body.

## Unverified

- **Hourly interval**: the vendor docs I read give publish times and metering scope but do not state the target interval. "Hourly" (summary, grain, what_it_is) is what the rows and chart show: every `startTime` is on the hour, 1 h steps, 73 per issue. It is not a quoted vendor rule.
- **Unit**: Elexon's OpenAPI row carries no unit. "MW" rests only on gridflow's column name, and the page says so.
- **Timezone of the vendor's eight publish times**: Elexon lists clock times without a zone. In silver in September (BST) they appear as those exact times in UTC. The page does not state the zone.
- The pattern "an hour's value freezes at the first issue published after it begins" holds for the 20 Sep issues. It is only claimed as far as the chart shows (the caption's "repeats hours already begun"), not as a rule.

## Open questions

- **Spec fragility for the seat**: `page.chart.group` is `published_at`, a tz-aware datetime. The `group_map` keys (`"2026-09-20 03:30:00.000000+00:00"`) are the string Polars' `.cast(pl.String)` produced under the pinned version in `distil.py`. A re-distil under a Polars that formats datetimes differently would miss the map, and the build would then fail on `chart_view.key`. CI is unaffected (it reads the committed series). A `chart_spec` option to group on a formatted time would remove this.

- The `ElexonWindForecast` pydantic schema and `ENTITY_KEY_COLUMNS` still describe the settlement-coordinate shape, which this endpoint never produces. The DATA-MATRIX "vs =" verdict compares the vault table with pydantic, not actual silver, so it missed this. Worth a gridflow docs or schema cleanup? (Not in scope here.)
- The OpenAPI is a local scratchpad copy dated 2026-09-27. If the checker wants the quote re-sourced, the live Swagger UI is linked in the note.

## Screenshots and template observations

- Headless Chrome via CDP with its own profile in the scratchpad; static server on 9722, now stopped. Shots are in `scratchpad/windfor-shots/`:
  - full page folded (`L-*`) and with the frame unfolded (`F-*`), at 1440, 1024, 768 and 390;
  - the notebook drawer open with the lazy plot loaded (`N-*`, `NC-390`), at 1440, 1024, 768 and 390.
- I looked at every tile. The `L-*` and `F-*` captures predate the last notebook-cell edit (the filter became `published_at.dt.day == 20`); `N-1024` and `NC-390` show the final cell.
- **Nothing clipped or overlapping in my content.** Scenery tops, corner labels, chart key and notes, the 390 code wrap and related notes are all fully visible. No horizontal page overflow at any width (`scrollWidth == innerWidth`).
- **No dark mode exists on the site**: no `prefers-color-scheme` or `data-theme` in `site/hifi/assets/*.css|js`, so "dark" renders identically to light.
- **Known template issues, ignored as instructed**: the notebook df header shift, and the line y-axis starting at 0 (here the floor is 0 anyway because min < max/2).
- **Template notes, not worked around**:
  - At 390 the frame folds every column after `timestamp_utc`, so `latest_forecast_mw` (the column that matters) sits behind the `…`. This is the width rule (`data-w="390"`), same as other pages.
  - The unfolded frame and the notebook df scroll sideways inside their own boxes at narrow widths.
  - Notebook df output shows pandas' unordered index labels (DuckDB returns rows unordered within the date filter). They changed between runs (7, 1, ... then 15, 9, ...). Values are identical.

## Revision 1 (2026-09-29, answering `windfor-review.md`)

1. **Major 1, "hourly" had no vendor or code source.** I did not cite a vendor source; every dataset-level use is now scoped to what the page shows.
   - `summary`: "hourly" removed.
   - `facts.grain`: "One row per target time and issue time".
   - `what_it_is`: "The issues charted, all published on 20 September, give one figure per hour and run to 20:00 UTC on the 22nd".
   - `raw_feed.note`: "one row per target time and issue".
   - `record.fields.timestamp_utc`: "Target time the forecast is for, ...".
   - `notebook.lead`: "`timestamp_utc`, the target time ... every stored issue for those days".
   - Body Overview: the OpenAPI citation now sits after "reissued up to 8 times a day". It adds: "The docs read do not state the target interval; the target times in gridflow's silver fall on the hour." The row is "one target time (`startTime`)". The silver-table `timestamp_utc` row reads "The target time".
   - Unchanged, as the checker allowed: "target hour(s)" where it describes shown data (chart caption, `x_label`, `record.caption`, alt).
2. **Major 2, the alts named the wrong minimum.** Both are re-derived from the committed series and the 20 Sep silver file (the checker's figures are confirmed).
   - `chart_view.alt`: peak 20,629 at 01:00 on the 20th; first trough 4,769 / 4,017 / 3,449 early on the 21st; recovery 6,734 / 6,249 / 5,684; lows 2,286 / 1,961 / 1,500 at 17:00 or 18:00 on the 22nd; ends 2,815 / 2,287 / 1,603. The ordering sentence (02:00 to 23:00 on the 21st) is kept.
   - `notebook.plot_alt`: eight issues, dip to 3,449 to 4,769 early on the 21st, recover to 5,684 to 6,734, lows of 1,500 to 2,286 MW on the evening of the 22nd, at 17:00 to 19:00.
3. **Nit, the caption.** It now reads: "Silver `elexon/windfor`, MW, target hours 20 September 00:00 to 22nd 20:00 UTC: three of that day's eight issues. Lines coincide only on hours begun before the earlier issue: all three to 03:00 on the 20th, the later two to 12:00." This matches the checker's exact-equality results.

No change to the chart spec, series, sample or notebook cells, so no artefacts were regenerated. `raw_feed.note` was reworded to stay within 30 words: "each day's bronze holds that day's issues".

**Checks after the merge of main:**
- The note was re-copied to the mirror (`cmp` identical; 255 lines, 255 CRLF).
- `gridflow-build --only elexon/windfor` passes; `detect.mjs --json` returns `[]`; the rendered page has no "hourly".
- Screenshots at 390, 768, 1024 and 1440 (`scratchpad/windfor-shots/R1-*`) show no horizontal overflow. The new caption and the chart render without clipping at 390 and 1440. The series has no time gaps, so the merged gap-breaking renderer draws the same three unbroken lines.
- The static server on 9722 is stopped.
