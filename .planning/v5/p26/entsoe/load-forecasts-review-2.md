# entsoe/load-forecasts (family, lead `load_forecast`): checker re-review

Checker: Opus 5.5 · high, 2026-09-29. This answers `load-forecasts-author-2.md` and re-checks the findings of
`load-forecasts-review.md`. Inputs: the canonical lead note and the three member notes in `vault-p26-entsoe`, their
mirror copies, the page rebuilt with `--only entsoe/load_forecast`, and fresh screenshots.

## Verdict: APPROVE

There are no findings. The major and all four nits are fixed, and nothing regressed.

## Round-1 findings

1. **major (the loss in plain words): fixed.**
   - **`page.summary`** now reads "...day-ahead per interval; week-, month- and year-ahead with one of two values
     kept." The "maxima and minima" promise is gone: the string no longer appears in the rendered page.
   - **`page.what_it_is`** now reads "gridflow keeps one of each pair (`A61`); no quoted source says which". It
     follows the regulation's "a maximum and minimum per day; month- and year-ahead, per week".
   - **Member lines.** All three now say in words that one of the regulated maximum and minimum is kept:
     - weekly: "of the regulated maximum and minimum, silver keeps one (`A61`)";
     - monthly and yearly: "one of maximum and minimum kept (`A61`); weeks repeat per day fetched".
   - **Accuracy.** Round 1 established `A61` on 48 of 48 weekly rows, and on 16 of 16 distinct monthly and yearly
     keys, with 48 rows and at most 6 repeats. The code is unchanged (`load_forecast_weekly.py:68`,
     `load_forecast.py:68`), and so is silver.
   - **Max or min.** The page still never says whether `A61` is the maximum or the minimum. That matches the
     evidence: no source names the business-type codes.
   - **Art. 2(27) paraphrase.** It now reads "Total load: generation plus imports, minus exports and storage use".
     Dropping "losses included" leaves the defining clause of Art. 2(27) intact, so this is not an error.
2. **nit, `how_used[0]`: fixed.** It now reads "...once fetched before delivery", which removes the point-in-time
   reading.
3. **nit, `record.fields.published_at`: fixed.** It now reads "the latest fetch per interval wins", which matches the
   keep-last on `(timestamp_utc, area_code)`.
4. **nit, `facts.grain`: fixed.** It now reads "Day-ahead: one row per bidding zone and interval start, from the
   latest fetch".
5. **nit, weekly body "Publication lag": fixed.** The Art. 6(2)(c) quote now runs in full, through "in the bidding
   zone and be updated when significant changes occur". This matches legislation.gov.uk verbatim.

## Regression checks

- **Build.** `uv run --system-certs --extra build gridflow-build --only entsoe/load_forecast` wrote
  `data-sources/entsoe/load-forecasts.html`. The only warnings are for other datasets.
- **Detector.** `node C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json <absolute page path>`
  returns only the accepted `em-dash-overuse` advisory (56, from EIC padding).
  - The rendered page has 0 "—", 0 "·" and 0 "→".
- **Artefacts unchanged.**
  - The series, sample and notebook JSON keep their round-1 timestamps (21:05 and 21:06).
  - The series keeps `spec_sha256` `ae64285...`, and the build's digest check passes.
- **Other fields unchanged.** The chart caption, alt, `raw_feed`, commands, `record.caption`, `notebook.lead`,
  `plot_alt` and `related` all carry their round-1 text.
- **Mirrors.** All four are byte-identical to the canonical notes (`cmp`), and all four notes are still CRLF.
- **Screenshots.**
  - Headless Chrome, each call under `timeout 60`, on its own port (9845, since stopped). Port 9670 was not
    touched.
  - Shot at 1440 (hero, raw feed with all four member lines, frame and guide) and at 390 through a 390 px iframe
    (hero, "What it is", "How it's used", the member lines and the commands).
  - The new prose wraps cleanly. Nothing is clipped or overlapping.

Summary: APPROVE. The loss now reads in plain words in the summary, "What it is" and all three member lines; the
four nits are fixed; the build passes and the detector shows only the accepted advisory.
