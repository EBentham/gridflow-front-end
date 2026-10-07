# neso/intensity-statistics: author report

Writer, 2026-10-06. Family `intensity-statistics`; members `intensity_stats` (lead, carries `page:`) and
`intensity_stats_block`. Built with `gridflow-build --only neso/intensity_stats`; detector `[]`; 0 em dashes.

## Status

- **Build:** clean. It wrote `data-sources/neso/intensity-statistics.html`; `intensity_stats.html` and
  `intensity_stats_block.html` are pointers to it.
- **Detector:** `[]`, with no advisories at all.
- **Artefacts:** all three generated from real data.
  - `site/hifi/data/series/neso/intensity_stats.json`: `spec_origin: vault`, silver `neso/intensity_stats_block`, 9 points.
  - `site/hifi/data/samples/neso/intensity_stats.json`: `generated_by: gridflow-sample`, silver `neso/intensity_stats_block`.
  - `site/hifi/data/notebooks/neso/intensity_stats.json` plus `intensity_stats-6.png`, written by `run_notebooks.py`. 6 cells, no errors.
- **Mirror:** `vault/neso/intensity_stats.md` and `vault/neso/intensity_stats_block.md` are copied from the vault worktree and `cmp`-equal.
- **Staged spec / authored override:** neither existed for these datasets, so there was nothing to delete.
- **Chart:** a line of NESO's daily `average_gco2_kwh` from `intensity_stats_block`, 13 to 21 September 2026,
  9 points, in gCO2/kWh. The axis starts at 0.
- **Departure from the brief (sanctioned by the task text, flagged for the seat):** the chart, frame and notebook
  come from the **second** member's table, not the lead's.
  - Why: the lead `intensity_stats` holds one row (a 5-day summary), which cannot carry a chart or eight sample rows.
  - How: `chart.silver` and `record.select.silver` are both set explicitly to `neso/intensity_stats_block`, and the
    caption says the chart shows the block member. Distil, sample and build all accept this.
  - No earlier page charts another member's table. The gie and openmeteo cases are vendor-slug remaps, not member switches.
  - **Suggestion for the seat:** reorder `site/hifi/data/neso.json` so that `intensity_stats_block` leads the family.
    I could not edit that file.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Routes `/intensity/stats/{from}/{to}` and `/{from}/{to}/{block}` (facts.vendor, family.request) | `connectors/neso/endpoints.py:119-133` |
| Path times formatted `YYYY-MM-DDTHH:MMZ`, no query params, no `page` | `endpoints.py:12`, `:298-299`; connector `_request(path, {})` `connectors/neso/carbon_intensity.py:68` |
| Request URLs on the page | Bronze sidecars: `.../stats/2026-08-01T00:00Z/2026-08-06T00:00Z` and `.../stats/2026-09-13T00:00Z/2026-09-22T00:00Z/24` |
| `block` is always 24 (what_it_is, raw_feed.note, differs) | `DEFAULT_STATS_BLOCK_HOURS = 24` `endpoints.py:16`, endpoint default `:132`; runner calls `connector.fetch(ds, ds_start, end_dt)` with no params `pipeline/runner.py:947`; no CLI option in `cli.py` ingest signature `:186-200` |
| Requests at most 14 days (facts.cadence, raw_feed.note, differs) | `_MAX_DAYS_PER_REQUEST = 14` `connectors/neso/carbon_intensity.py:21`, chunk loop `:149-164` |
| Ingest `--end` is the exclusive `to` instant; bare date = midnight UTC | `runner.resolve_dates` `pipeline/runner.py:479-501` ("a bare date is midnight UTC"); `to_dt = end` in `build_path` `endpoints.py:299` |
| Transform `--start 2026-09-13 --end 2026-09-13` covers the whole 9-day window | Bronze is filed under `data_date=window_start.date()` (`carbon_intensity.py:79`). Silver reads the exact partition only (`silver/neso/carbon_intensity.py` `_bronze_files` docstring, `:87-140`). The 9 Sep rows are all in `silver/.../month=09/intensity_stats_block_20260913.parquet` |
| Key `(timestamp_utc, period_end_utc)` | `df.unique(subset=["timestamp_utc", "period_end_utc"], keep="last")` `silver/neso/carbon_intensity.py:501-528` |
| `timestamp_utc` = vendor `from`, `period_end_utc` = vendor `to`, read as UTC | `_parse_neso_datetime` `silver/neso/carbon_intensity.py:643-649`: format `%Y-%m-%dT%H:%MZ`, `replace_time_zone("UTC")`, `strict=False` (an unparseable value would become null; none are null here). Bronze bodies and silver rows agree |
| `max_/average_/min_gco2_kwh` = vendor `max/average/min`; `intensity_index` = `index` | `_extract_stats_rows` `:345-361`, `_transform_stats` `:501-528` |
| Unit gCO2/kWh | Column names chosen by the transformer (`*_gco2_kwh`), schema `CarbonIntensityStats` `schemas/neso.py:39-45`, vault Overview |
| Index is one of five bands `very low` to `very high` | Vault `30-vendors/neso/datasets/carbon_intensity.md:78` ("One of very low, low, moderate, high, very high in docs") |
| `query()` relation, date column, inclusive ends, lineage dropped (notebook.lead) | `research/handles/source.py:401-444`. NESO transformers are not `APPEND_ONLY` (no hit in `silver/neso/carbon_intensity.py`), so the relation is the base view. The date column is `timestamp_utc`: `silver/schema_manifest.py:246-247` |
| Chart values 168, 146, 77, 113, 65, 61, 60, 84, 164 (alt) | Committed series `values`, x 2026-09-13 to 2026-09-21 |
| Frame rows, with min 34 (15th) and max 216 (21st) | Committed sample; silver |
| Notebook comparison shows max and min equal and average = rounded actual mean, 13 to 21 Sep | Notebook cell 5 output (9 rows: e.g. 168.0 vs 168.02, 146.0 vs 145.73, 164.0 vs 163.98) |
| plot_alt numbers | Notebook image and the cell 5 output: max 87 (18th) to 216 (21st); min 34 (15th) to 106 (21st); average 168 to 60, ends 164 |
| `generation` is half-hourly fuel shares (related note) | Silver `neso/generation`: every row spans 30 min; per-timestamp share sums are 99.8 to 100.2 |
| `intensity_factors` in gCO2/kWh (related note) | `factor_gco2_kwh` `silver/neso/carbon_intensity.py` `_transform_factors` |
| Statistics are national (related note) | Endpoint category `"Statistics - National"` `endpoints.py:121,128` |

## Coverage and what a row is (not public; for the seat)

- **`intensity_stats`**: one row.
  - It is a 5-day summary from 2026-08-01 00:00Z to 2026-08-06 00:00Z: max 180, average 111, min 37, `moderate`.
  - It came from one request (`fetched_at` 2026-08-16).
  - A row is **one request chunk**, at most 14 days. A longer ingest window gives one row per chunk, not one
    summary of the whole window.
- **`intensity_stats_block`**: 14 rows, all 24-hour blocks starting at 00:00 UTC.
  - 1 to 5 Aug: 5 rows, from a request for 1 Aug 00:00Z to 6 Aug 00:00Z.
  - 13 to 21 Sep: 9 rows, from a request for 13 Sep 00:00Z to 22 Sep 00:00Z.
  - The gridflow request windows set which blocks exist. The blocks started at midnight because the windows did.
    I did not verify how the vendor aligns blocks when the window starts at another time.
- **Thin data:** the page never states row counts or holdings. It shows one fixed 9-day window, one point a day,
  and makes no trend claim.

## Reproducibility against `carbon_intensity` (observation, not a vendor rule)

- **Coverage of the check:** `neso/carbon_intensity` silver has all 48 half-hours on each day of both windows, with
  no null `actual_gco2_kwh` and no null `forecast_gco2_kwh`.
- **24-hour blocks (14 of 14):** I took half-hours whose start falls in `[from, to)`.
  - `max` and `min` equal the max and min of `actual_gco2_kwh` exactly.
  - `average` equals the mean of `actual_gco2_kwh` rounded to a whole number.
  - The forecast values do not match: for example, 13 Sep has forecast max 217 against vendor 204.
  - I brute-forced 36 window conventions (lower and upper offsets of -30, 0 and +30 minutes, each bound inclusive or
    exclusive). Only `[from, to)` on period starts, and its equivalent "periods ending in `(from, to]`", fit all 14 rows.
- **5-day `intensity_stats` row:** `max` 180 and `min` 37 match the actual values.
  - Its `average` of 111 does not match: the mean of the 240 actual half-hours is 110.40, which rounds to 110.
  - No convention I tried gives 111 except adding the 31 Jul 23:30 half-hour (110.63), and that convention breaks the
    block rows.
  - The mean of the five daily block averages is 110.2, and the median is 110. Neither gives 111.
  - Both datasets were fetched 4 seconds apart on 16 Aug, so the two do not differ by vintage.
  - The page states no mechanism for this and keeps every agreement claim inside the notebook's 9-day window.
- **Index:** in these 15 rows the index follows the band of the average under the half-hourly series' bands as
  observed (`low` up to 89, `moderate` from 90). Every block with an average of 84 or less is `low`; every block from
  111 up is `moderate`, including the 21 Sep block with max 216. This is an observation only and is not on the page.

## Body corrections (both notes)

1. **Bronze "Granularity"** (both notes):
   - Was: "One file per API call; range and daily routes may produce one file per chunk/day/period." That was vague
     and missed the point the transform command relies on.
   - Now: one file per request window of at most 14 days, filed under the window's first day
     (`connectors/neso/carbon_intensity.py:79`); silver reads only that partition.
2. **Implementation delta, `max_query_days`** (both notes):
   - Was: the connector "chunks with `max_query_days: 14`".
   - Corrected: the connector uses its own constant `_MAX_DAYS_PER_REQUEST = 14` (`:21`, loop `:149-164`), which
     matches the YAML value.
   - Lead note only: added that one `intensity_stats` row summarises one chunk.
3. **Block note, new Implementation delta bullet:** `block` is always 24 hours (`endpoints.py:16`, `:132`;
   `pipeline/runner.py:947`; no CLI option).

Left alone (nits, listed here, not rewritten):
- **Both notes, "Known issues"** keep two bullets copied from the half-hourly notes:
  - "Actual carbon intensity values can be null or absent…". The stats tables have no `actual` field.
  - "For `intensity_period`, GB clock-change days…". This does not apply here.
- **Both notes:** the "Historical depth" TODO and "Publication lag: Derived from available intensity observations"
  are unevidenced. Neither is on the page.
- **Block note:** the bronze and silver samples show one 24-hour record covering a whole day, which is consistent
  with block 24. That is fine.
- **Both notes:** the silver schema tables omit the lineage columns (`event_time`, `available_at`, `source_run_id`,
  `dataset_version`). These are pipeline columns.

## Unverified

- **Which values the vendor statistics summarise** (actual or forecast): the vault quotes no vendor text on this.
  - The page says only "the fields do not say which half-hourly values they summarise; the notebook checks them".
  - I did not fetch the vendor docs page.
- **The 5-day average of 111 against 110.40:** the vendor's method for multi-day windows is unknown.
- **Block alignment for a window that does not start at a block boundary, or whose length is not a multiple of the
  block:** never requested, so unknown.
- **The vendor's index band thresholds:** not quoted in the vault, so not stated on the page.

## Open questions (for the seat)

1. Reorder `neso.json` so `intensity_stats_block` leads this family? That would make the "chart from the lead's
   table" rule hold literally.
2. Should someone fetch the Carbon Intensity API definitions page to settle actual against forecast? If yes, the
   quote goes into both notes' bodies, and the page could then state it as a vendor fact.

## Template problems

1. **Long y-axis units are clipped at 390 px.**
   - Cause: the narrow chart frame has `x0=50` (`chart_svg.py:175`), and the unit label is right-anchored at
     `x0 - 10` (`chart_svg.py:334`).
   - Effect: "gCO2/kWh" loses its leading "g" at the left edge of the SVG at 390. It is fine at 768 and wider.
   - Scope: the same will happen to every page whose unit is longer than about 5 characters. That includes the other
     NESO pages (`gCO2/kWh`), `EUR/MWh`, `GWh/d` and `W/m²`.
   - My spec cannot avoid it, because the unit is correct. The fix needs a template change: left-anchor the unit at
     x = 0 in the narrow frame, or widen `x0`.
2. The family page's bronze stratum shows only `family.members[].request`. My two `raw_feed.requests` lines are
   required by the build but not shown. They duplicate the member requests, so this is harmless; noted for the seat.

## Screenshots

- Headless Chrome on port 9868, at 1440, 1024 and 768, plus a true 390 iframe. The server is stopped.
- The site has no dark-mode styles (no `prefers-color-scheme` or `data-theme` in `tokens.css`, `theme.css` or
  `site.js`), so the light pass covers both modes.
- **Checked at every width:** hero scenery (turbine tops visible), chart, key, raw feed, frame and guide, notebook
  panel, related links, and the stratum corner labels.
- **One finding:** the 390 unit label (template problem 1).
- **Frame fold:** at 768 the frame shows timestamp, average, max and min, and folds `intensity_index` and
  `period_end_utc`. At 1024 and wider, all key columns show.
- **390 re-capture:** after I reordered the frame columns, a second 390 capture stopped painting at the frame (a
  headless iframe quirk). The first full 390 capture already covered the frame, guide, notebook and related links.
  The reorder changes nothing visible at 390, where only `timestamp_utc` fits before the fold.

## Commands against notebook `needs`

- `notebook.needs` names half-hourly intensity, but `raw_feed.commands` ingests only the block member. The build caps
  commands at 3, so they cannot cover both tables.
- A reader running the notebook would also run these two commands. `carbon_intensity` is filed under the request's
  first day in the same way:
  - `gridflow ingest neso carbon_intensity --start 2026-09-13 --end 2026-09-22`
  - `gridflow transform neso carbon_intensity --start 2026-09-13 --end 2026-09-13`
- I did not verify the half-hourly transform's partitioning for this window. Silver holds a 12 Sep 23:30 row, so check
  that before stating these commands publicly.

## Defects

- **gridflow (connector/runner), dataset parameter cannot be set:** `neso/intensity_stats_block` always requests
  24-hour blocks.
  - `DEFAULT_STATS_BLOCK_HOURS = 24` (`src/gridflow/connectors/neso/endpoints.py:16`, `:132`).
  - `pipeline/runner.py:947` calls `connector.fetch(ds, ds_start, end_dt)` with no params, and the `gridflow ingest`
    CLI has no block option.
  - So the vendor's documented 1 to 24 hour block cannot be requested, and the dataset is in effect "daily statistics".
  - Severity: low (a capability gap, not wrong data).
  - Fix: expose `--param block=N`, or document that the block is fixed.
- **Vendor or method question, `neso/intensity_stats`:** the whole-window `average` does not reproduce from
  half-hourly `actual_gco2_kwh`.
  - Window 2026-08-01T00:00Z to 2026-08-06T00:00Z: vendor 111; the mean of the 240 actual half-hours is 110.40.
  - `max` and `min` match, and all 14  24-hour block averages reproduce to the rounded actual mean.
  - The data is not wrong; the vendor's averaging method for multi-day windows is undocumented in the vault.
  - Severity: info.
  - Action: a research note, or a vendor-doc quote in the vault.
- **Vault (both stats notes), stale copied text:** the "Known issues" section carries two bullets that do not apply
  to the stats routes:
  - "Actual carbon intensity values can be null or absent…": the stats tables have no actual field.
  - The `intensity_period` clock-change note.
  - Severity: nit.
  - Fix: delete them in the canonical vault.
- **Front-end template:** narrow-frame y-axis unit clipped at 390 px for units longer than about 5 characters
  (`src/gridflow_front_end/chart_svg.py:175`, `:334`).
  - Seen on `neso/intensity-statistics` ("gCO2/kWh").
  - Severity: minor (the "Nothing clipped" rule).

## Nits fixed (2026-10-07, after review APPROVE with 6 nits)

Nit 1 (`notebook.needs` with no `carbon_intensity` command): no change, per the seat's ruling that it matches the
precedent on shipped pages.

2. **`chart_view.caption`:** now reads "the frame below holds 14 to 21 September's maximum and minimum". The frame's
   rows start on the 14th, and the 13th's values appear only in the notebook. I also added "(gridflow's label)" after
   the unit (see 5). 38 words.
3. **`facts.cadence`:** now reads "On request; gridflow asks for windows of at most 14 days (NESO allows 30)".
   - Evidence for 30: `30-vendors/neso/README.md:68`.
   - Evidence for 14: `_MAX_DAYS_PER_REQUEST`, `connectors/neso/carbon_intensity.py:21`.
4. **Scope of the reproduction claim:**
   - `what_it_is` ends "the notebook sets 13 to 21 September's blocks beside daily `actual` figures" (59 words).
   - `how_used[1]` now reads "Cross-checking `carbon_intensity`: 13 to 21 September's daily `actual` extremes and
     rounded means agree." It names the window and no longer reads as a general rule; the lead's 5-day row is not
     claimed.
5. **Unit and band attribution:** I took the sibling `intensity_factors` wording.
   - `summary` and `what_it_is` say "labelled gCO2/kWh by gridflow".
   - The caption adds "(gridflow's label)".
   - Guide lines:
     - `average_gco2_kwh`: "gCO2/kWh is gridflow's label, the response states none".
     - `max_gco2_kwh` and `min_gco2_kwh`: "same gridflow label".
   - `related` `intensity_factors`: "under the same gCO2/kWh label", where it had said "the same unit".
   - `intensity_index` guide: "NESO's band; the API docs list five, `very low` to `very high`".
   - Body evidence in both notes:
     - A new Known issues bullet: bronze bodies send bare numbers with no unit, and `gCO2/kWh` is gridflow's column
       label (`_transform_stats`, `silver/neso/carbon_intensity.py:501-528`).
     - The `intensity_index` schema row now records the five docs bands and points to `carbon_intensity.md`'s
       `intensity_index` row.
   - The chart's axis unit, `chart.unit` and the alt texts keep "gCO2/kWh" as the axis label.
6. **Vault bodies, both notes, "Known issues":** deleted the two copied bullets that do not apply to the stats routes
   (the null-actual line and the `intensity_period` clock-change line). Also took the reviewer's suggestion for the
   `related` `neso/generation` note: "Half-hourly fuel mix shares for the same days".

Checks:
- **Mirror:** both canonical notes copied to `vault/neso/` and `cmp`-equal.
- **Build:** `gridflow-build --only neso/intensity_stats` is clean, with no budget or digest errors.
- **Detector and dashes:** `detect.mjs --json` returns `[]`; 0 em dashes.
- **Rendered text:** every revised phrase is present in the rendered page.
- **Artefacts:** the chart spec, the row selection and the notebook cells are unchanged, so the series, sample and
  notebook artefacts did not need regenerating, and the build's digest check passed.
- **Screenshots:** not retaken. The changes are prose inside existing text slots, which wrap.
