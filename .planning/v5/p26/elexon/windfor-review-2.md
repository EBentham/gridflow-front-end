# elexon/windfor: checker re-review (after Revision 1)

Checker, 2026-09-29. I rebuilt the page with `gridflow-build --only elexon/windfor` before judging.

## Verdict: APPROVE

No findings above nit. All three findings from `windfor-review.md` are fixed.

## Earlier findings

1. **Major 1, "hourly" with no source: fixed.**
   - "Hourly" is gone from `summary`.
   - The dataset-level fields now say "target time": `facts.grain` ("One row per target time and issue time"),
     `raw_feed.note`, `record.fields.timestamp_utc` and `notebook.lead`.
   - `what_it_is` now limits the hourly step to the charted issues ("The issues charted ... give one figure per
     hour"), which the chart shows.
   - "Target hour" stays only where it describes data shown on the page: the chart caption, `x_label`,
     `record.caption` and the alt.
   - Body Overview: the OpenAPI citation now covers only the reissue schedule. It adds that the docs do not state
     the target interval, and that silver's target times fall on the hour. That is a vault body note, it is not
     rendered, and it is labelled as a silver observation.
   - The silver-table row for `timestamp_utc` now reads "The target time".
   - The rendered page text contains no "hourly".
2. **Major 2, the alts missed the real lows: fixed.** Each value below was checked against the committed
   `series/elexon/windfor.json` (spec digest `e061f98c...` unchanged, 207 rows used) and silver
   `windfor_20260920.parquet`.
   - `chart_view.alt`:
     - peak 20,629 at 01:00 on the 20th;
     - first trough 4,769 / 4,017 / 3,449 early on the 21st;
     - recovery 6,734 / 6,249 / 5,684 later on the 21st (14:00, 20:00, 22:00);
     - lows 2,286 / 1,961 / 1,500 at 17:00 or 18:00 on the 22nd;
     - ends 2,815 / 2,287 / 1,603;
     - strict ordering holds from 02:00 to 23:00 on the 21st.

     All of these match.
   - `notebook.plot_alt`, over the eight issues:
     - start 20,316 ("near 20,300");
     - troughs 3,449 to 4,769 on the 21st;
     - recoveries 5,684 to 6,734;
     - minima 1,500 to 2,286 at 17:00 to 19:00 on the 22nd ("evening").

     All of these match silver and the plot PNG.
3. **Nit, caption: fixed.** The caption now reads "Lines coincide only on hours begun before the earlier issue: all
   three to 03:00 on the 20th, the later two to 12:00." That is exact against the series:
   - all three issues are equal for 20 Sep 00:00 to 03:00;
   - `issue_0330 == issue_2330` over the same hours;
   - `issue_1230 == issue_2330` for 00:00 to 12:00;
   - no other exact equalities.

   The caption still states the dataset, unit, window and issues.

## Nothing else broke

- The build passes, and `detect.mjs --json` returns `[]`.
- The chart spec, series, sample and notebook cells are unchanged, so the artefact digests still hold.
- The mirror is byte-identical to the vault note, which is CRLF.
- The page block has no "locally", "held", local counts, em dashes, middle dots or arrows.
- Screenshots at 1440, 1024, 768 and 390 (headless Chrome over CDP, true 390) cover the hero, the what-it-is text
  and chart, the raw feed, and the notebook. Nothing is clipped or overlapping, and `scrollWidth == innerWidth` at
  every width. The shots are in `scratchpad/windfor-review-shots/r2/`.
- My servers on 9727 and 9728 are stopped.

## Seat notes carried from the first review (not findings)

- `ElexonWindForecast` and the static `ENTITY_KEY_COLUMNS` still describe the settlement-coordinate shape.
- DATA-MATRIX's `vs` column compares the vault with pydantic, not with the silver files.
- The `group_map` keys depend on how Polars prints a datetime.
