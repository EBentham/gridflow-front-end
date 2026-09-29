# entsoe/load-forecasts (family, lead `load_forecast`): checker review

Checker: Opus 5.5 · high, 2026-09-29. Inputs: the four canonical notes in `vault-p26-entsoe` (diffed against
`origin/master`), their mirror copies (`cmp` clean on all four), the committed series, sample and notebook, and the
page built with `gridflow-build --only entsoe/load_forecast`.

## Verdict: REVISE

There is one major finding: the horizon members' loss is accurate but not stated plainly (finding 1). Everything
else is right, apart from four nits. Once finding 1 is fixed this is an APPROVE; the fix touches only prose.

## Findings

1. **major**, `page.family.members[1..3].differs`, plus `page.summary`.
   - **What is wrong.** The loss is stated accurately but in codes, not plainly.
     - The member lines say "silver keeps `A61`, drops `A60`" (weekly) and "silver keeps `A61`" (monthly and
       yearly). The page never says that `A60` and `A61` are the two values the regulation requires, or that one of
       them is lost.
     - A reader has to join "a maximum and minimum per day/week" in `what_it_is` to two bare codes in the raw feed.
     - The hero `summary` says the family holds "week-, month- and year-ahead maxima and minima". That is true of
       ENTSO-E's forecasts, but no gridflow table here holds both values.
     - The seat ruling asks for the loss "stated plainly", as `commercial_schedules` does. Its summary says what is
       dropped and adds "so the day-ahead series is lost".
   - **Evidence (reproduced).** Each A31, A32 and A33 response carries two series, `A60` and `A61` (48 of each per
     table in bronze). Silver keeps `A61` only:
     - weekly: 48 of 48 rows match an `A61` point and none match `A60`;
     - monthly and yearly: 16 of 16 distinct keys match an `A61` point and none match `A60`.
     - Cause: `load_forecast_weekly.py:68` and `load_forecast.py:68` dedup on `(timestamp_utc, area_code)`, and
       `business_type` is not in `output_cols`.
     - Monthly and yearly: 48 rows for 16 distinct keys, at most 6 repeats, with one distinct value per key
       (`group_by(["timestamp_utc","area_code"]).agg(len, n_unique)`).
     - All of this matches the writer's figures and each member line's facts.
   - **Which of min and max is kept.** `A60 < A61` in all 48 pairs of each table. But no repo, vault or quoted
     vendor source names the business-type codes. The `A61` hits in the vault are NTC *document* type `A61`, not
     this. So the page is right not to say which one is kept; keep it that way.
   - **Fix.** Say it in words, within the 14-word `differs` budget. Each example below is 14 words by whitespace,
     which is at the limit, so check with the build:
     - weekly: "`A31`, own schema, per day: of the two values sent, silver keeps only `A61`";
     - monthly: "`A32`, per week: one of two values kept (`A61`); weeks repeat per day fetched";
     - yearly: "`A33`, as monthly: one of two values kept (`A61`); weeks repeat per day fetched".
   - **Summary.** Scope it within 22 words (the current text is 20) so it does not promise both values. For
     example, in 19 words: "ENTSO-E's total load forecasts per bidding zone: day-ahead per interval; week-, month-
     and year-ahead, one of each max-min pair". Alternatively, leave the summary and add a short clause to
     `what_it_is`, which is near its 60-word budget.

2. **nit**, `page.how_used[0]`.
   - "The benchmark a zonal load model has to beat" reads as a point-in-time use. The table holds no fetch from
     before delivery, and the values can change after delivery.
   - Evidence: 2026-09-08 DE-LU was fetched at `raw_20260909T014435Z` and `raw_20260915T195535Z`. 8 of 96 intervals
     differ, by up to 11.0 MW.
   - The caption and `notebook.lead` already carry the caveat, so this is only a nit. Consider "...has to beat, once
     fetched before delivery".

3. **nit**, `page.record.fields.published_at`.
   - "the latest fetch of the day wins" can be read as the latest fetch made on a calendar day.
   - The keep-last runs per `(timestamp_utc, area_code)` within the delivery day's partition (`load_forecast.py:38`
     sorted names, `:68`).
   - Suggest "the latest fetch per interval wins".

4. **nit**, `page.facts.grain`.
   - "One row per bidding zone and interval start" holds for the lead only. Monthly and yearly hold a week up to
     6 times (48 rows, 16 keys).
   - The member lines say so, but a family-level fact could start with "Day-ahead:".

5. **nit**, vault body `load_forecast_weekly.md`, "Publication lag".
   - The Art. 6(2)(c) quote stops at "day-ahead market". The legislation.gov.uk text continues "in the bidding zone
     and be updated when significant changes occur".
   - The dropped clause is the one that matters for revisions. Quote it in full, or mark the cut.

## Checked and correct

- **Regulation text.** I fetched legislation.gov.uk Art. 2 and Art. 6 on 2026-09-29.
  - Art. 2(27) is quoted verbatim in the lead note.
  - Art. 6(1)(b) to (e) and 6(2)(b) to (e) match verbatim, including the monthly wording "which shall include, for
    a given week".
  - The page's paraphrases (`what_it_is`: four forecasts, maximum and minimum per day or week; "generation plus
    imports, minus exports and storage use, losses included") are faithful.
- **No issue time.**
  - The GL_MarketDocument header (`2026/09/15/raw_20260921T100501Z_7528aa55.xml`) has mRID, `revisionNumber` 1,
    type, process, sender, receiver, `createdDateTime` and `time_Period`. None of it is an issue time.
  - Silver `published_at` over 14 to 20 Sep runs from 2026-09-21 10:04:43 to 10:06:17. The sidecar `fetched_at` is
    10:04:59 against `createdDateTime` 10:04:58.
  - The caption ("as ENTSO-E served them on 21 September, after delivery; the document carries no issue time"),
    `notebook.lead` ("as fetched ... not as issued") and the `published_at` guide line ("Fetch time
    (`createdDateTime`), not an issue time") are accurate and follow ruling #39.
  - The code comment calling it an issue time (`_published_at.py:3-8`) is the known seat item, and the page does
    not repeat it.
- **Chart.**
  - The committed series has `spec_origin: vault`, `aggregation: last`, and a 14 to 20 Sep window. It holds 672
    points for each of DE-LU, FR, NL and BE, and its values match silver to within 0.0005 MW (3-dp rounding). There
    are no duplicate keys in the window, and every row is `PT15M`.
  - Alt text, recomputed:
    - DE-LU: weekday daily peaks 63.0, 62.7, 63.4, 63.4 and 61.8 GW; weekend peaks 52.0 and 51.5; low 37,214 at
      2026-09-20 01:45 UTC.
    - FR: 31,300 to 51,801.
    - NL: low 7,563 at 19 Sep 13:30 UTC, high 13,256.
    - BE: 6,778 to 11,340.
    - 14 Sep 2026 is a Monday, so the weekday and weekend labels hold.
  - The point time "period start plus (position minus 1) times resolution" matches `parsers.py:530,582`.
  - The 15-minute cadence is scoped as "in every response charted" or "as charted", as ruling #39 asks.
  - The palette is line paints only: no khaki and no hatches needed.
- **Requests and commands.**
  - The four URLs match the sidecar `request_url` parameter order byte for byte (A01 on 15 Sep; A31 and A32 on
    14 Sep). The endpoints are `endpoints.py:34,127-135`.
  - Ingest `--end 2026-09-21` is exclusive (`day_subwindows`, `client.py:162`), and transform `--end 2026-09-20` is
    included. This is the same form as the approved `actual_load`.
  - `forecast_margin` is A70/A33 (`endpoints.py:136-137`), so its related note is right.
- **Frame and guide.**
  - The sample was written by `gridflow-sample` and holds 8 real rows at 11:00 and 11:15 UTC on 15 Sep. The 15 Sep
    files declare all 96 points, so none of these rows is forward-filled.
  - Key columns come first, with no pipeline-column lines and no repeats.
- **Notebook.**
  - Written by `scripts/run_notebooks.py`, with read-only cells and no errors.
  - Recomputed from silver: MAE is DE-LU 1,257, BE 295, FR 595 and NL 1,707 MW.
    - NL daily maxima: 6,602 (15th 10:15 UTC), 6,030 (18th 09:45) and 6,698 (20th 11:00).
    - DE-LU runs from -4,186 (17th 03:00 UTC) to 4,157 (16th 23:15 UTC, just after midnight on the plot's UTC+1
      clock). It is a single spike in the PNG.
    - FR runs from -1,893 to 2,234; BE from -1,078 to 935.
  - `plot_alt` matches the plot.
- **Vault bodies.** Reproduced:
  - weekly: `P1D`, 22:00 UTC and `A61` on 48 of 48 rows;
  - monthly and yearly: `P7D`, 48 rows for 16 keys, up to 6 repeats;
  - yearly against monthly: DE-LU and NL differ on 8 of 8 pairs, FR and BE on 0 of 8;
  - the 8 Sep double fetch: 8 intervals, 11 MW;
  - `_advance_calendar` for `P1M` and `P1Y` (`parsers.py:76-93,523-528`).
  - The corrections are scoped and cite code. The curl examples are untouched.
- **Local-data grep.** "code 999 on the days charted" and "gridflow's GB calls ... returned code 999" use the same
  wording as the approved `actual_load` page. Nothing else hits.
- **Gates.**
  - `gridflow-build --only entsoe/load_forecast` wrote `data-sources/entsoe/load-forecasts.html`.
  - `detect.mjs --json` returns only the accepted `em-dash-overuse` advisory (56, from EIC padding and CLI flags).
  - The rendered page has no "—", "·" or "→".
- **Screenshots.**
  - Headless Chrome with its own profile, each call under `timeout 60`, through a sized iframe served on port 9845
    (since stopped).
  - Shot at 1440, 1024, 768 and 390: hero scenery and turbines, chart and key, the four member request blocks, the
    frame folded and unfolded, the guide, the open notebook drawer with its plot, and related.
  - Nothing is clipped or overlapping. The URL wrap and frame fold at 390 are template behaviour.
  - The unfolded frame scrolls horizontally past `ingested_at` at every width. Its `.fw` wrapper is
    `overflow-x: auto` (`assets/dataset.css:14`), so this is template scrolling, not clipping.
  - Light only: `theme.css` and `tokens.css` have no `prefers-color-scheme` or `data-theme` rule, so there is no
    dark theme to shoot.
