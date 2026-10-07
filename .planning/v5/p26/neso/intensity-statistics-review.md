# neso/intensity-statistics: review

Checker (Sonnet 5.5 · high), 2026-10-06. Family `intensity-statistics`; lead `intensity_stats`, second member
`intensity_stats_block` (chart, frame and notebook come from the second member, as ruled).

## Verdict: APPROVE

0 blockers, 0 majors, 6 nits. The facts, chart, reproduction claim and thin-data wording all hold. The nits are
worth taking in the same pass but none blocks shipping; finding 1 is the one the seat may want to rule on.

## What I reproduced (all agree with the page)

- **Build and detector.** `gridflow-build --only neso/intensity_stats` wrote `intensity-statistics.html`
  (the one "1 error on pages not rendered by --only" belongs to another page). `detect.mjs --json` returns `[]`.
  0 em dashes, no middle dots or arrows; the only "live" hit is inside "olive" in `plot_alt`.
- **Chart.** Series `neso/intensity_stats` is `spec_origin: vault`, `provenance.silver: neso/intensity_stats_block`,
  rows_matched 14, rows_used 9. Values 168, 146, 77, 113, 65, 61, 60, 84, 164 equal silver
  `average_gco2_kwh` for 13 to 21 Sep; the alt text and every number in it match. The rendered axis runs 0 to 200.
  `chart.silver` and `record.select.silver` both resolve to the block member and read correctly (sample rows
  are the 14 to 21 Sep blocks, `generated_by: gridflow-sample`).
- **"Filed under its first day".** `connectors/neso/carbon_intensity.py:79` sets `data_date=window_start.date()`;
  `_request_specs` makes 14-day chunks (`:21`, `:157`). Bronze sidecars show one request for 1 to 6 Aug (file
  `20260801`) and one for 13 to 22 Sep (file `20260913`), and silver holds exactly those two block files. The
  transform command (`--start 2026-09-13 --end 2026-09-13`, end inclusive per `runner.run_transform`) therefore covers the whole 9-day window.
  Ingest `--end` exclusive: `resolve_dates` takes a bare date as midnight UTC and `build_path` sends it as `to`.
- **Request URLs.** Both match the bronze `request_url` values (path segments only, `_request(path, {})`, no `page`).
- **24 hours.** `DEFAULT_STATS_BLOCK_HOURS = 24` (`endpoints.py:16`, default at `:132`); the only
  `connector.fetch(` call in the package is `runner.py:947` and passes no parameters; the CLI `ingest` has no block option.
  So "gridflow always asks for 24 hours" is a code fact with evidence.
- **Reproduction (14 of 14).** For each daily block, half-hours of `carbon_intensity` silver with start in `[from, to)`
  (48 per day, no null `actual` or `forecast`): max and min equal the max and min of `actual_gco2_kwh`, and `average`
  equals the mean rounded to a whole number (for example 13 Sep: 204/99/168 vs 204/99/168.02; 16 Sep: 152/64/113 vs
  152/64/112.62). Forecast max does not match (13 Sep 217 vs 204). The page states no equality outright; the
  agreement itself appears only in the notebook output (the 13 to 21 Sep window), though `what_it_is` and
  `how_used[1]` lean on it without scoping (finding 4).
- **The lead's row.** Silver `intensity_stats` is one row, 1 to 6 Aug, max 180, average 111, min 37. Over the
  240 actual half-hours, max and min match and the mean is 110.396 (rounds to 110, not 111). The page says nothing
  about this and never shows that row, so nothing on it is wrong; see finding 4 for the wording that brushes it.
- **Notebook.** `generated_by: scripts/run_notebooks.py`, 6 cells, outputs card/df/df/image, no errors; cells are
  read-only. Cell 5's output matches silver. `plot_alt` numbers check against the PNG (max 87 on the 18th to 216 on
  the 21st, min 34 on the 15th to 106 on the 21st, average 168 to 60 then 164) and the colours match the
  `color=` list. `notebook.lead`: `relation_name_by_dataset()` gives `silver_neso_intensity_stats_block` and
  `silver_neso_carbon_intensity`; date column `timestamp_utc` (`schema_manifest.py:246-247`); `query()` end is inclusive; lineage
  columns (`event_time`, `available_at`, `source_run_id`, `dataset_version`) are excluded.
- **Mirrors.** `cmp` of both canonical notes against `vault/neso/intensity_stats.md` and `intensity_stats_block.md`: byte-equal.
  Vault diff against `origin/master` touches only the `page:` block, the Granularity line and `max_query_days`
  bullet in both notes, and the new `block` bullet in the block note; each is evidenced above. No curl change.
- **Screenshots.** Headless Chrome at 1440, 1024 and 768 and a true 390 iframe, every crop read: hero scenery with
  turbine tops, chart, key, raw feed, frame (folded), guide, notebook panel (closed, cells 1 and 2), related list and
  stratum corner labels are fully visible at all four widths; the 390 unit label shows in full. The unfolded frame
  I saw in the browser pane (scrolled to its last columns; the first columns are in the folded captures). The
  opened notebook panel did not render in the pane (screenshots timed out or came back blank), so its output
  cells are checked from the committed JSON, the PNG (read directly, also visible in the DOM) and the built HTML
  text, not from a rendered capture. The site has no dark theme, so the light pass covers both.

## Findings

1. **nit** `page.notebook.needs` with `page.raw_feed.commands`: the page tells the reader to have half-hourly
   intensity ingested but gives no command for it. Downgraded from major after a precedent check: every shipped
   page whose notebook queries a second dataset names both in `needs` and commands only its own dataset
   (`elexon/atl` needs ATL and INDO, commands ATL only; `elexon/indo`, `elexon/ndf`, `entsoe/load_forecast` and
   `entsoe/total_capacity_allocated` the same). This page follows that house pattern.
   - `needs` reads "NESO block statistics and half-hourly intensity, 13 to 21 September 2026 ingested", and notebook
     cell 3 calls `data.neso.query("carbon_intensity", ...)`, but both commands are for `intensity_stats_block`.
     A reader who follows the two commands has no `silver_neso_carbon_intensity` rows, so cells 3 and 5 fail or
     return nothing. The comparison is the point of the notebook and the second use in `how_used`.
   - Silver delivers it (the notebook ran with output): `carbon_intensity` is filed the same way (bronze sidecar
     `intensity/2026-09-13T00:00Z/2026-09-22T00:00Z`, `data_date` 2026-09-13; silver file `carbon_intensity_20260913`),
     so `gridflow ingest neso carbon_intensity --start 2026-09-13 --end 2026-09-22` and
     `gridflow transform neso carbon_intensity --start 2026-09-13 --end 2026-09-13` would work.
   - The cap is 3 commands (`COMMANDS_COUNT = (1, 3)`), so the four lines do not fit. Optional: keep the house
     pattern, or let the seat rule on a three-line set. The writer verified nothing about the half-hourly
     transform; I did (above), so those two commands would be safe to state if the seat wants them.

2. **nit** `page.chart_view.caption`: "each day's maximum and minimum are in the frame below" is not true of the
   13th. The frame shows eight rows, 14 to 21 Sep (`record.select.filter`); the 13th's 204 and 99 appear only in the
   notebook. Say "the maximum and minimum for 14 to 21 September are in the frame below".

3. **nit** `page.facts.cadence` (and `page.family.members[0].differs`, `raw_feed.note` are fine): "one summary per
   window of at most 14 days" sits in a vendor-facts row and reads as an API limit. NESO allows 30 days
   (`30-vendors/neso/README.md:68`, `endpoints.md:78`); 14 is gridflow's chunk (`_MAX_DAYS_PER_REQUEST`). Suggest
   "gridflow asks for windows of at most 14 days (NESO allows 30)" or drop the number from `cadence`.

4. **nit** `page.what_it_is` and `page.how_used[1]`: scoping of the reproduction.
   - "the notebook checks them" reads as though the notebook settles which half-hourly values the fields summarise
     and covers both members. It sets the block member beside daily `actual` figures for 13 to 21 Sep only (no
     forecast comparison), and the lead's own row (average 111 against an actual-based 110.40) does not reproduce.
   - `how_used[1]` ("recompute each day's maximum, mean and minimum") is unscoped. Suggest saying the notebook
     compares the block figures with daily `actual` values for 13 to 21 September, and that max, min and the rounded
     mean agree there. The 5-day mismatch is already in the writer's Defects section.

5. **nit** units: every `gCO2/kWh` on the page (summary, `what_it_is`, `chart.unit`, caption, guide lines, axis) rests
   on gridflow's own `*_gco2_kwh` column names (code, so it meets the brief). Neither stats note quotes a vendor
   sentence, and the vendor docs page as I retrieved it states no unit for the statistics routes. The sibling
   `intensity_factors` note in this batch says exactly that ("the response states no unit"), and the related line
   "in the same gCO2/kWh unit" asserts the equality as fact. Not wrong, but inconsistent across the batch; the seat
   should rule once for the NESO carbon intensity pages (state it as gridflow's label, or add a body evidence line).
   The same applies to "one of five from `very low` to `very high`", whose only vault evidence is in
   `carbon_intensity.md:203`, not in these notes.

6. **nit** vault bodies (both notes, "Known issues"): the two copied bullets are false for the stats routes ("Actual
   carbon intensity values can be null or absent", which these tables have no field for, and the `intensity_period`
   clock-change line). The writer left them and reported it; fix when the notes are next touched. The
   `related[1]` note on `neso/generation` ("to see what moved a block's average") is also a loose use: the
   `intensity_factors` note says the shares need gas and imports mapped before they weight into gCO2/kWh. Suggest
   "Half-hourly fuel mix shares for the same days".

## Not findings

- Chart from the second member and the caption saying so; chart unit clip at 390 (the seat's rulings).
- The writer's report says all key columns show at 1024 and wider. In my captures `period_end_utc` (a key column)
  folds behind `…` at 1024 and 768 and only `timestamp_utc` shows at 390; it shows at 1440. That is the template's
  fold, the guide still lists it, and nothing is clipped.
- The two `raw_feed.requests` entries are not rendered separately (the member requests are); harmless duplication.
- 5-day average 111 against 110.40 and the missing block option are gridflow or vendor questions, already in the
  writer's Defects.
