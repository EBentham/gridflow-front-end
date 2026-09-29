# entsoe/generation_forecast: review

Checker: Opus 5.5 · high, 2026-09-29. Screenshot port 9807 (server stopped).

## Verdict: REVISE

Two findings above nit: one blocker, one major. Both are one-clause edits to the `page:` block. Everything else checked out, including every focus item.

## Findings

1. **blocker** · `page.record.fields.timestamp_utc`
   - **What is wrong:** "period start plus position times resolution" is one step late.
     - The parser computes `start_dt + (position - 1) * resolution` (`gridflow/connectors/entsoe/parsers.py:530`, and the A03 fill at `:590`).
     - A reader following the guide would place position 1 at start plus 15 minutes.
   - **Evidence:**
     - Bronze `2026/09/08/raw_20260915T200937Z_a582bbc5.xml`, TimeSeries mRID 2, period start `2026-09-08T00:00Z`, `PT60M`: position 9 has quantity 102.9925.
     - Silver BE 2026-09-08: `08:00 UTC = 102.9925` and `09:00 UTC = 0.0` (position 10). So position 9 maps to 08:00, which is (9 - 1) × 1 h.
   - **Fix:**
     - For example, "Target time the forecast is for: start of the step, from the period start and point position, UTC", or "... period start plus (position minus 1) steps, UTC".
     - The body's Silver schema row (`Period start + position * resolution`, pre-existing) has the same error. Fix it in the same pass, citing `parsers.py:530`.
   - **Seat note:** `actual_generation` (`page.record.fields.timestamp_utc`) and `cross_border_flows` in this batch carry the same wording. `actual_load` has it right. The batch should converge on one wording.

2. **major** · `page.facts.cadence`
   - **What is wrong:** "Every 15 minutes for DE-LU, FR and NL; hourly for BE" is an unscoped universal, measured on our copy of the responses.
   - **Evidence:**
     - Silver `group_by(area_code).agg(resolution.unique())` gives A82H, FR and NL `["PT15M"]` and BE `["PT60M"]`, over 2026-08 and 09 only.
     - No vendor doc in the note states per-zone resolutions. Zone resolutions have changed at the vendor over time (the note's own old sample said `PT60M` for DE-LU).
     - The author scoped the same fact everywhere else: `what_it_is` says "this window", the body says "in 2026-08/09 responses", and the caption describes the charted window. Only the hero fact stands bare.
   - **Fix:** scope it, for example "Every 15 minutes for DE-LU, FR and NL, hourly for BE, in these responses", or state it as the step sent: "Step as sent: `PT15M` or `PT60M`, per zone".

## Checked and correct

- **`published_at` (ruling #39):**
  - `record.fields.published_at` reads "Response `createdDateTime`; here within seconds of gridflow's fetch, not an issue time". It is scoped with "here" and never called an issue time.
  - Over the 78 data documents in bronze, `fetched_at - createdDateTime` ranges from -0.21 s to 10.43 s, and `createdDateTime - data_date` from 1 to 15 days.
  - The eight rows show 2026-09-26 18:14 for 20 September targets.
  - The body's "leak-proof forecast issue time" is removed.
- **Zone handling:**
  - `parsers.py:289-297` maps `outBiddingZone_Domain.mRID` into `in_domain`.
  - `generation_forecast.py:75` runs `unique([timestamp_utc, area_code, production_type], keep="last")` over `sorted(glob("raw_*.xml"))` (`:40`).
  - Only one document has an `outBiddingZone_Domain` series: BE on 2026-09-08, with TS1 out and TS2 in.
  - Silver BE 08:00 is 102.9925, which is TS2 and not TS1's 623.51. The later series wins, as `what_it_is` and `fields.area_code` say.
  - `production_type` is `""` for every zone, and 0 bronze files contain `MktPSRType`.
- **Chart:**
  - The committed series has `spec_origin: vault` and no staged spec (`chart-specs/entsoe/` is absent).
  - It is 4 series × 168 hourly points. `rows_used` 2184 = 3 × 672 quarter-hours + 168 BE hours.
  - Independent Polars hourly means (`dt.truncate("1h")`, mean) match the committed values to within 0.0005 MW for all four zones. Quarter-hours per bucket are `[4]` for DE-LU, FR and NL and `[1]` for BE.
  - The caption says "shown as hourly means; BE is sent hourly". The BE key note says "Sent hourly, so no averaging."
- **Alt and plot_alt numbers:**
  - DE-LU daily hourly peaks run from 59,500 (14th, 11:00) to 77,208 (17th, 10:00), with all peaks at 10:00 or 11:00. Daily lows run from 30,584 to 44,632.
  - FR runs from 36,908 to 63,638, with weekend maxima of 46,733 and 48,542 (19th and 20th are Saturday and Sunday).
  - NL runs from 7,362 to 14,432, with its daily minimum between 09:00 and 13:00 on six of the seven days.
  - BE runs from 2,033 to 7,742.
  - For plot_alt, DE-LU quarter-hour peaks run from 59,597 (14th) to 77,609 (17th), all between 10:15 and 11:15, with lows from 30,443 to 44,567. The PNG matches.
- **Raw feed:**
  - The request URL matches the bronze sidecar `request_url` in parameter order.
  - The ingest end is exclusive: `day_subwindows` drops a midnight end, so 14 to 21 fetches the 14th to the 20th.
  - The transform end is inclusive.
  - There are no `PARTITION_SOURCE_OFFSETS` for this dataset.
  - GB and IE-SEM acknowledgements cover every day from 14 to 20 September, so "for this window ... came back empty" holds.
- **Notebook:**
  - The lead matches `_date_range_predicate`: half-open at end + 1 day on TIMESTAMPTZ `timestamp_utc`, the relation `silver_entsoe_generation_forecast`, and the bitemporal exclude.
  - Every cell is read-only, with no errors, and `.head()` shows all four zones.
- **Build, detector and mirror:**
  - `gridflow-build --only entsoe/generation_forecast` exits 0.
  - `detect.mjs` gives only the accepted `em-dash-overuse` advisory: 43 counts, all from EIC padding and `--start`/`--end`.
  - The rendered text has no em dash, en dash, "→" or middle dot.
  - The mirror is `cmp`-identical to the canonical note, which is CRLF.
  - The front matter holds no literal `---` except the fences, and `group_map` uses `\x2D` escapes (ruling #40).
- **Local data and leakage:**
  - The grep for `locally`, `held`, `our `, `since 20`, `rows`, `% of` and "N rows/days" finds only "hour" and "four", plus template help-card text.
- **Sample:** `generated_by: gridflow-sample`, the eight rows match silver, and the guide covers every non-pipeline column with the key columns first.
- **Visuals (light only; the site ships no dark theme):**
  - I looked at 1440, 1024, 768 and 390 (390 in an iframe): the hero and turbine tops, the chart and key, bronze, the frame folded and unfolded, the guide, the notebook and its outputs, the corner labels, and related.
  - Nothing is clipped or overlapping.
  - At 390 the notebook tab truncates to "generation_forecast.i…" and `gridflow_models` is fully visible, so the seat's `theme.css:394-395` fix works.

Report note (not a page finding): the author report's "Seat ruling applied" section says the `\x2D` escapes were reverted to plain codes. The note is in fact in ruling #40 form, with escapes, so the report is stale on that point.
