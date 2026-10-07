# neso/national-carbon-intensity: review 2

Checker: Sonnet 5.5 · high, 2026-10-06. Focused re-check of `national-carbon-intensity-author-2.md` against `national-carbon-intensity-review.md`.

## Verdict: APPROVE

The major is fixed in all nine notes, all eight nits are fixed, and nothing regressed. 0 blocker, 0 major, 0 nit open.

## The major (finding 1): fixed

- All nine canonical notes (`30-vendors/neso/datasets/<member>.md` in the vault worktree) no longer say "ex-ante feature" as advice. `grep -n -i "ex-ante"` returns exactly one hit per member note, and each hit is the corrected Modelling-notes sentence ("NESO's forecast as served at fetch time, not an issued forecast: NESO sends no issue time and silver keeps the latest fetch per partition ... so do not treat it as a verified ex-ante feature. Use `actual_gco2_kwh` as an ex-post target or label.").
  - Lead `carbon_intensity.md`: Modelling notes at line 251 and the Gold leakage note at line 223 ("The view's comment calls the forecast column the ex-ante feature, but silver holds it as served at fetch time, not as issued (see Known issues), so it is not a verified ex-ante value.").
  - The other eight carry the same Modelling-notes sentence with a link to `carbon_intensity.md` for the Known-issues bullet.
- The statement is accurate: no issue time in the bronze body (keys `from`, `to`, `intensity{forecast, actual, index}`), `silver/neso/carbon_intensity.py:485` `unique(keep="last")` over bodies in fetch order, `silver/base.py:711` `APPEND_ONLY = False`, no NESO entry in `silver/latest_views.py`.
- The diff of each member note against `origin/master` shows only the intended spans (Modelling notes sentence, plus the earlier Dedup key, `intensity_today`, `intensity_date`, fw24h/fw48h and `intensity_current` edits).
- The gold view SQL comment is not edited and is logged in the writer's Defects section as a gridflow-side item, as ruled.

## The eight nits

| # | Field | Status | Evidence |
|---|---|---|---|
| 2 | `page.notebook.needs` | fixed | Built page reads "Needs gridflow and gridflow-models installed, with carbon_intensity for 14 to 20 September 2026 ingested." No literal backticks. |
| 3 | `chart_view.key[0].codes` | fixed | `codes` removed (optional field); legend reads "Estimated actual" at 1440 and 390. |
| 4 | `raw_feed.note` | fixed | "In responses checked, the first half-hour ends at `from`, the last at `to` (undocumented)." 27 words, within budget. An observation with the scope stated; matches the bronze captures (193, 241 and 433 half-hours). |
| 5 | fw24h, fw48h, pt24h `differs` | fixed | "From the half-hour ending at `from`, 24 hours on; past half-hours carry actuals" (13 words), "...48 hours on; NESO forecasts two days ahead" (14), "Back 24 hours, to the half-hour ending at `from`" (9). Matches the captures (49, 97 and 49 half-hours; first or last one ends at `from`). |
| 6 | `intensity_today` `differs`; notes | fixed | "No inputs; today's UK-day half-hours, actuals null until NESO estimates them" (11). `intensity_today.md` Historical depth and `intensity_date.md` parameter now say "UK day ... seen in BST only"; the capture span quoted (2026-09-26 23:00 to 2026-09-27 22:30 UTC; 2026-08-01 returned 07-31 23:00 to 08-01 22:30) matches bronze. |
| 7 | `intensity_period` `differs` | fixed | "gridflow calls once per period: 48 a day, 46 or 50 at clock changes" (14 words); it now attributes the loop to gridflow (`_settlement_period_count`). |
| 8 | `page.how_used[2]` | fixed | "Comparing NESO's forecast with its estimated actual, the forecast as served at fetch." No longer frames it as a forecast-error study. |
| 9 | `chart_view.caption` | fixed | "one value per half-hour" removed; caption is now two sentences naming dataset, unit, window and the forecast's location. |

## Regression checks

- `gridflow-build --only neso/carbon_intensity`: success, wrote `data-sources/neso/national-carbon-intensity.html`; the chart digest check passed (spec unchanged, series and sample and notebook unchanged: 336 points, same alt numbers).
- `detect.mjs --json` (absolute path) on the page: `[]`. Em dashes, arrows and middle dots in the page and in the front matter: 0. Planning words and local-data words in the front matter: none. Every `differs` is 14 words or fewer.
- `cmp` between each canonical note and `vault/neso/<member>.md`: clean for all nine (`carbon_intensity`, `intensity_at`, `intensity_current`, `intensity_date`, `intensity_fw24h`, `intensity_fw48h`, `intensity_period`, `intensity_pt24h`, `intensity_today`).
- Screenshots (headless Chrome, `timeout 60`, `--timeout=15000 --virtual-time-budget=5000`): 1440 full page and a true 390 px iframe. The hero, chart (unit label fully visible at 390), legend, raw-feed block with the reworded note and `differs` lines, frame, guide and notebook entry all wrap cleanly with nothing clipped or overlapping. My server on 9887 is stopped; 9670 was not touched.

## Open items

None for the page. The gold view comment (`gold/views/uk_imbalance_context.sql`, about lines 33 to 41) remains a gridflow-side defect, logged by the writer.

One line: APPROVE, the ex-ante advice is corrected in all nine notes, the eight nits are fixed, and the build, detector, mirrors and renders show no regression.
