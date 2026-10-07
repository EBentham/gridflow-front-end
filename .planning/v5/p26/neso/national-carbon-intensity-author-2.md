# neso/national-carbon-intensity: author revision 2

Writer: Opus 5.5 · high, 2026-10-06. This responds to `national-carbon-intensity-review.md` (REVISE: 0 blocker, 1 major,
8 nits). All nine findings are fixed.

## Status

- `gridflow-build --only neso/carbon_intensity`: success. It wrote `data-sources/neso/national-carbon-intensity.html`.
  The first rebuild failed on a budget (the `intensity_period` `differs` line was 15 words); it was shortened and
  rebuilt clean.
- `detect.mjs --json` (absolute path): `[]`. Em dashes in the page: 0.
- The chart spec is unchanged, so the series is not re-distilled. The digest check passed in the build. The sample and
  notebook are unchanged.
- **Mirrors:**
  - All nine canonical notes were edited with the Edit tool, keeping CRLF (0 LF-only lines in each).
  - Each was copied to `vault/neso/<member>.md`, and `cmp` is clean for all nine.
- **Screenshot check:** 390 iframe on port 9867 (`nci_shots/r2_w390.png`, crop `r2_390_chart.png`).
  - The legend reads "Estimated actual" without the repeated code.
  - The chart unit label "gCO2/kWh" is fully visible after the seat's `chart_svg.py` fix.
  - The new how-used, caption and raw-feed lines wrap cleanly.
  - My temporary server ran under `timeout 120`. Port 9670 was not touched.

## Fixes

| # | Severity | Field | Was | Now |
|---|---|---|---|---|
| 1 | major | `carbon_intensity.md` body, Gold "Leakage note" | "...; use the forecast column as the ex-ante feature." | "The view's comment calls the forecast column the ex-ante feature, but silver holds it as served at fetch time, not as issued (see Known issues), so it is not a verified ex-ante value." |
| 1 | major | Modelling notes, **all nine notes** (the same templated sentence was in every member) | "Use `forecast_gco2_kwh` as an ex-ante feature and..." | "`forecast_gco2_kwh` is NESO's forecast as served at fetch time, not an issued forecast: NESO sends no issue time and silver keeps the latest fetch per partition (see Known issues [in carbon_intensity]), so do not treat it as a verified ex-ante feature. Use `actual_gco2_kwh`..." |
| 2 | nit | `page.notebook.needs` | `` `carbon_intensity` for 14 to 20 September 2026 `` (literal backticks rendered) | `carbon_intensity for 14 to 20 September 2026` (plain; checked in the built page) |
| 3 | nit | `page.chart_view.key[0].codes` | `actual` (rendered "Estimated actual actual") | removed (optional field) |
| 4 | nit | `page.raw_feed.note` | "Responses run from the half-hour ending at `from` to the one ending at `to` (a project check)." | "In responses checked, the first half-hour ends at `from`, the last at `to` (undocumented)." (29 words in all) |
| 5 | nit | `family.members` fw24h, fw48h, pt24h `differs` | "The 24/48 hours after `from`...", "The 24 hours before `from`" | "From the half-hour ending at `from`, 24 hours on; past half-hours carry actuals"; "From the half-hour ending at `from`, 48 hours on; NESO forecasts two days ahead"; "Back 24 hours, to the half-hour ending at `from`" |
| 6 | nit | `family.members[intensity_today].differs` | "today's half-hours" | "today's UK-day half-hours" |
| 6 | nit (caution a) | `intensity_today.md` Historical depth; `intensity_date.md` `date` parameter | "GB settlement day" | "UK day ... (seen in BST only)" |
| 7 | nit | `family.members[intensity_period].differs` | "One call per settlement period: 48 a day, 46 or 50 at clock changes" | "gridflow calls once per period: 48 a day, 46 or 50 at clock changes" (a gridflow loop, not a NESO rule) |
| 8 | nit | `page.how_used[2]` | "Forecast-error studies, with the forecast as served at fetch time, not as issued." | "Comparing NESO's forecast with its estimated actual, the forecast as served at fetch." |
| 9 | nit | `page.chart_view.caption` | "..., one value per half-hour." | phrase removed |

Evidence for every fix is the review's own, re-read against the code and silver from the first report:

- Per-partition keep-last dedup: `silver/neso/carbon_intensity.py:485`.
- Overwrite-per-date writes: `silver/base.py:711`, `:2610-2640`.
- Bronze partition = window start: `connectors/neso/carbon_intensity.py:79`.
- Period loop: `_settlement_period_count` (`:167-177`) and `:141-143`.
- Range captures: 193, 241 and 433 half-hours.
- Date captures: 23:00 to 22:30 UTC, in BST only.

## Defects (paste as is; in addition to the first report's)

- **gridflow, gold view comment (medium, docs and leakage):**
  - `gold/views/uk_imbalance_context.sql` (the leakage comment and the `COMMENT ON COLUMN` for
    `carbon_intensity_actual_gco2_kwh`, about lines 33-41) tells users to "use the forecast column" as the ex-ante
    feature.
  - Silver `silver_neso_carbon_intensity` holds NESO's forecast as served at the latest fetch: no issue time,
    overwrite-per-partition (`APPEND_ONLY = False`, `silver/base.py:711`), `unique(keep="last")` over bodies in fetch
    order (`silver/neso/carbon_intensity.py:485`).
  - A backfilled forecast is therefore not a verified ex-ante value.
  - Fix: reword the view comment to "forecast as served at fetch time; not a vintaged ex-ante forecast", or capture the
    NESO forecast append-only with the fetch stamp as vintage.
  - The vault notes are corrected in this branch; the code is left for gridflow.
- **Vault, fixed in this branch:**
  - All nine `neso` national-intensity notes' Modelling notes, and the `carbon_intensity` Gold leakage note, presented
    `forecast_gco2_kwh` as the ex-ante feature, contradicting the no-vintage behaviour.
  - `intensity_today` and `intensity_date` now say "UK day (seen in BST only)" in place of "GB settlement day".

## Still unverified (unchanged from the first report)

- The index cut-offs.
- Which forecast run NESO serves for a past half-hour.
- The `[from, to]` end-inclusive convention: observed in captures, undocumented by NESO.
- `intensity_current`'s "current" semantics.
- The date routes' behaviour in GMT and on clock-change days.

One line: All nine review findings are fixed: the "ex-ante" advice is corrected in all nine notes and the eight nits
are reworded within budget; the notes are mirrored byte for byte, the build is clean and the detector returns `[]`.
