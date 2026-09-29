# entsoe/load-forecasts: writer round 2 (answers load-forecasts-review.md)

Writer: Opus 5.5 · high, 2026-09-29. All edits are to the canonical notes in `vault-p26-entsoe`, copied byte for byte to the `p26-entsoe` mirror. `cmp` is clean on all four notes, and all four are CRLF throughout.

## Changes, finding by finding

1. **major: the loss stated in words, and no max/min promise.**
   - `page.summary`:
     - Was: "... day-ahead per interval, and week-, month- and year-ahead maxima and minima."
     - Now: "... day-ahead per interval; week-, month- and year-ahead with one of two values kept." (22 words)
   - `page.what_it_is`: now says "gridflow keeps one of each pair (`A61`); no quoted source says which", right after the regulation's maximum and minimum per day or week.
     - To stay within 60 words, "(losses included)" came out of the total-load paraphrase and "on the days charted" became "on charted days".
   - `page.family.members[].differs` (each 14 words or fewer, build-checked):
     - weekly: "`A31`, per day: of the regulated maximum and minimum, silver keeps one (`A61`)";
     - monthly: "`A32`, weekly: one of maximum and minimum kept (`A61`); weeks repeat per day fetched";
     - yearly: "`A33`, weekly: one of maximum and minimum kept (`A61`); weeks repeat per day fetched".
   - The page still never says whether `A61` is the maximum or the minimum.
2. **nit, `how_used[0]`.** Now "The benchmark a zonal load model has to beat, once fetched before delivery."
3. **nit, `record.fields.published_at`.** "the latest fetch of the day wins" becomes "the latest fetch per interval wins".
4. **nit, `facts.grain`.** Now "Day-ahead: one row per bidding zone and interval start, from the latest fetch".
5. **nit, weekly body "Publication lag".** The Art. 6(2)(c) quote now runs in full, through "in the bidding zone and be updated when significant changes occur".

The series, sample and notebook are unchanged: no spec, select or cell was edited, so no re-distil was needed and the build's digest check passes.

## Gates

- `uv run --system-certs --extra build gridflow-build --only entsoe/load_forecast`:
  - The first run failed: `what_it_is` was 61 words, so I trimmed one word.
  - The second run wrote `data-sources/entsoe/load-forecasts.html` with no errors. The only warnings are for other datasets.
- `node C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json <absolute page path>` returns only the accepted `em-dash-overuse` advisory (56, from EIC padding and CLI flags).
- The rendered HTML contains each new phrase.
- Screenshots:
  - Headless Chrome, each call under `timeout 60`, own profile. The server on port 9835 is stopped.
  - 1440 full width, and 390 through a 390 px iframe.
  - The changed hero summary, grain fact, `what_it_is`, `how_used` and the three member lines are fully visible, with nothing clipped or overlapping.
  - The 1024 and 768 layouts are unchanged from round 1 apart from these prose lengths.

Summary: the major and all four nits are fixed; the build passes, the detector shows only the accepted advisory, and the mirrors are byte-identical.
