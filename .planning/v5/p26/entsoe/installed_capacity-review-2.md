# entsoe/installed_capacity: re-check (review 2)

Checker: Opus 5.5 · high, 2026-09-29. This is a focused re-check of `installed_capacity-author-2.md`
against the findings in `installed_capacity-review.md`.

- **Port:** my own server on 9846, now stopped. The server on 9670 was not touched.
- **Screenshots:** in `scratchpad/icr/r2_*.png`.

## Verdict: APPROVE

All five findings (1 major, 4 nits) are resolved, and nothing has regressed.

## The major (finding 1, the notebook's pivot output): resolved

- **The cell** (`page.notebook.cells[1]`) now maps the EIC codes to zone names and flattens the header:
  `.rename(columns=zones).rename_axis(index=None, columns=None)`.
  - The EIC dashes are `\x2D`-escaped inside a double-quoted string (ruling #40).
  - The front matter has no bare `---`: the delimiters are at lines 1 and 133, and the `---` at line 146 is in the body.
- **Notebook JSON:**
  - It was written by `scripts/run_notebooks.py`.
  - Cell 4's `columns` are `['', 'DE-LU', 'BE', 'FR', 'NL']`, with 4 values per row.
  - No cell has an error output.
- **Rendered `<thead>`:** `<th></th><th>DE-LU</th><th>BE</th><th>FR</th><th>NL</th>`.
- **B14 row:** `<th>B14</th><td>NaN</td><td>2056.000</td><td>62990.00000</td><td>486.0</td>`.
  - DE-LU B14 is empty (NaN), which agrees with "no B14".
  - BE 2,056, FR 62,990 and NL 486 match silver.
  - B01 is 8855.90 / 846.099 / 1434.93 / 418.0, and B07 is 0.00 / NaN / NaN / 0.0, as in silver.
- **Screenshots:**
  - At 1440 (`r2_1440_nb1.png`), every header sits over its own column.
  - At 390 (`r2_390_nbA.png`, `r2_390_nbB.png`), the table overflows into `.df-wrap`. That element has `overflow-x: auto` (398/285), so FR and NL scroll into view and are not clipped. The page's own `scrollWidth` stays 375.
- **Plot cell:** it now maps only the PSR codes.
  - The new image (724×316) shows the same bars.
  - `plot_alt` still holds: DE-LU solar about 104k, DE-LU onshore wind about 68k, FR nuclear about 63k, no DE-LU nuclear bar, and every BE bar under 12k.

## The nits: resolved

2. **`facts.cadence`** now reads "One `P1Y` point per year, as sent in these responses". "weekly" appears 0 times in the rendered text.
3. **"single annual snapshot"** now appears in `what_it_is` ("a single annual snapshot, one MW figure per type"), once in the rendered text.
4. **`notebook.lead`** now says "The 2026 row is stamped 31 December 2025 whatever day you ingest, so query that day, then drop per-file duplicates".
   - This is correct against `query()` (whole UTC days of `timestamp_utc`, both ends included).
   - It is consistent with `needs` ("one day of 2026, for example 14 September").
5. **Scoping in `what_it_is`:**
   - "GB and IE-SEM return no-data acknowledgements in these responses".
   - "the 2026 document has DE-LU B07 at 0, no B14".
   - Both are scoped, and both remain true against bronze and silver.

## Regression checks

- **Build:** `gridflow-build --only entsoe/installed_capacity` rendered the page with no errors. The series and sample digests still pass: the chart spec and `record.select` are unchanged.
- **Detector:** `detect.mjs --json` at its absolute path returns only the accepted `em-dash-overuse` advisory (`advisory: true`, the EIC `--` padding).
- **Mirror and line endings:**
  - The mirror is `cmp`-identical to the canonical note.
  - The note has 293 CRLF line endings and 0 LF-only lines.
- **Rendered text:** 0 em dashes, 0 `→`, 0 middle dots. No hits for `locally`, `held`, `our`, `live`, `now`, `since 20` or `% of`.
- **Screenshots:** the revised hero facts and `what_it_is` at 1440 and 390 (`r2_1440_nb2.png`, `r2_390_hero.png`) wrap cleanly, with nothing clipped.

Summary: APPROVE. The pivot now has one header row (DE-LU, BE, FR, NL), each over its own values, and DE-LU B14 is empty; all four nits are fixed; the build is green and the detector reports only the accepted advisory.
