# entsoe/forecast_margin: checker review

**Verdict: REVISE.** 2 majors, 2 nits. The facts, chart provenance, build and screenshots are sound. Both majors concern the sign loss: suggested uses that silver can't deliver, and one place where DE-LU's value shows unflagged.

## Findings

1. **major, `page.how_used[2]` and `page.how_used[0]`.** Silver can't deliver either use today. `ForecastMarginTransformer` drops `business_type` (`silver/entsoe/forecast_margin.py:75-83`), so every silver value is non-negative (Polars `forecast_margin_mw.min()` = 180.0 over all 48 rows).
   - `how_used[2]`, "Flagging a zone whose TSO sends a negative margin (A92) for the year", needs the sign outright, and the line doesn't say silver lacks it. `what_it_is` ends "Silver drops it" two items earlier, but the bullet itself reads as a supported use.
   - `how_used[0]`, "Comparing neighbouring zones' expected adequacy for the coming year, one MW figure each", also needs the sign for the zone set the page names. From silver, DE-LU (+4,126) ranks above FR (1,500) and BE (180), when it is the only zone in deficit.
   - The seat ruling makes this a major.

   **Fix:** for `[2]`, drop the bullet or say plainly that it needs bronze. The writer's fallback works, for example "Flagging a zone whose TSO sends a negative margin (A92); silver drops the sign, so read bronze". For `[0]`, scope it, for example "... one MW figure each; DE-LU's sign must come from bronze". `how_used[1]` (a generic model input) can stay.

2. **major, `page.notebook.cells[1]` output and `page.notebook.lead`.** Cell 4 prints the deduplicated frame with `DE-LU 4126.000` beside FR 1500, BE 180 and NL 41891.044 (notebook artefact, cell n=4 output). Nothing in the cells or the lead says this value is really negative; the lead mentions only per-file duplicates. `plot_alt` does explain it, but it is alt text and a sighted reader never sees it. This breaks the seat ruling that the page never shows DE-LU's value as positive. The sample frame is fine by contrast: it must print real silver rows, and its `record.caption` flags "DE-LU's 4,126 is sent as negative (A92)". **Fix:** either drop DE-LU before the display in cell 4, as cell 5 already does, or add a clause to the lead ("silver holds DE-LU's A92 margin unsigned, as 4,126"). Then rerun `run_notebooks.py`.

3. **nit, `page.what_it_is`.** The Art. 2(30) quote closes after "maximum total load", but the definition goes on: "taking into account the forecast of total generation capacity, the forecast of availability of generation and the forecast of reserves contracted for system services". The words quoted are verbatim (legislation.gov.uk `eur/2013/543/article/2/adopted`, point 30, checked) and the meaning holds. Still, the cut is unmarked. Add "..." inside the quote, or say "defines it as, in part, ...". The note body carries the full text.

4. **nit, `page.chart_view.caption`.** "Each silver file repeats it; one copy is kept." The repeat is vendor behaviour measured on our 12 files: each one-day request returned the whole year's document. It isn't a code rule, because the transformer only dedups within a file (`forecast_margin.py:62`). `raw_feed.note` scopes the same fact with "In these responses"; the caption doesn't. Scope it, for example "These silver files each repeat it; one copy is kept."

## What I checked (no finding)

- **Sign loss, reproduced.**
  - **Bronze:** of 72 files, 48 are `GL_MarketDocument`. DE-LU (`10Y1001A1001A82H`) is `businessType` A92 with `quantity` 4126 in all 12 of its replies; BE, FR and NL are A91 in all 36 of theirs. Example: `bronze/entsoe/forecast_margin/2026/09/14/raw_20260915T201814Z_45ecfc97.xml`.
  - **Parser:** reads `businessType` (`parsers.py:308-309`) and emits `business_type` (`:453`).
  - **Transformer:** its `output_cols` omit it (`forecast_margin.py:75-83`).
  - **Silver:** DE-LU is 4126.0 in all 12 files, and silver holds no negative value.
  - **Meanings:** A91 is "Positive forecast margin" and A92 "Negative forecast margin" (entsoe-py `mappings.py` BSNTYPE, which mirrors the ENTSO-E code list; the v29r0 PDF URL now returns 404).
  - **Column guide:** "unsigned: the A91 or A92 sign is dropped" is accurate.
  - **Chart:** leaves DE-LU out, and the caption says why in plain words.
- **Chart values.**
  - The committed series is `x [nl, fr, be]`, `values [41891.044, 1500.0, 180.0]`, `rows_read` 48, `rows_matched` 36 (3 zones × 12 files), `duplicates_dropped` 33, `rows_used` 3. The 12 daily repeats aren't summed.
  - Silver: one distinct value per zone across all 12 files (FR 1500.0, BE 180.0, NL 41891.044). One `timestamp_utc`, 2025-12-31 23:00 UTC; `resolution` P1Y. No charted zone is negative in bronze: all three are A91.
  - `spec_origin: vault`, no staged spec, no authored override. The build's digest check passes.
  - Alt text and title match the series. Khaki is unused.
- **Definition and unit.**
  - The Art. 2(30) and Art. 8(1) wording in the page and the body match legislation.gov.uk (fetched this session).
  - `quantity_Measure_Unit.name` is `MAW` in every bronze data reply; the page says MW (`MAW`).
- **Coverage.**
  - All 24 acknowledgements are code 999 "No matching data found ... YEAR_AHEAD_FORECAST_MARGIN_R3 [8.1]": 12 for `10YGB----------A` and 12 for `10Y1001A1001A59C`, one per request day.
  - The `raw_feed.note` wording is accurate ("one GET per bidding zone and UTC day, for six zones": `client.py:162` `day_subwindows`, `endpoints.py:395` `DEFAULT_ZONES`).
  - The cadence "One `P1Y` point per year, as sent in these responses" is scoped correctly.
- **Request and commands.**
  - The `raw_feed.requests` URL matches the bronze `.meta.json` `request_url` exactly, parameter for parameter and in the same order.
  - Ingest end is excluded (`utils/time.py` `day_subwindows`, `[start, end)`). Transform end is included. Bronze day `2026/09/14` feeds silver `forecast_margin_20260914`.
- **Fields.**
  - `timestamp_utc` is the period start (`parsers.py:527-528`, `_advance_calendar` with n = position - 1). 23:00 UTC on 31 Dec is midnight CET.
  - `published_at` is described as a fetch-time stamp, per ruling #39.
  - The key `(timestamp_utc, area_code, published_at)` is unique on 48 of 48 rows.
- **Sample.** `gridflow-sample`, 8 rows: `published_at >= 2026-09-15T20:18:01Z`. The rows match silver.
- **Notebook.**
  - `run_notebooks.py`, read-only cells, no errors.
  - The lead matches `query()` (`gridflow_models/.../handles/source.py:401-450`: relation by name, inclusive ends, type-aware TIMESTAMPTZ predicate, bitemporal columns excluded).
  - `plot_alt` matches the PNG: BE's 180 bar is invisible and its label shows.
- **Related.** `installed_capacity`, `load_forecast_yearly` and `actual_load` silver all hold DE-LU, BE, FR and NL. The year claims fit: `installed_capacity`'s only `timestamp_utc` is 2025-12-31 23:00 UTC (Polars `unique()`), the same stamp.
- **Leakage and filler.**
  - The rendered text has 0 em dashes, 0 middle dots and 0 arrows.
  - No local-data wording: the only "our " hit is inside "four".
  - The body additions cite `file:line` and fix narrow spans. The mirror is byte-identical to the canonical note (`cmp`).
- **Gates.** `gridflow-build --only entsoe/forecast_margin` is green. `detect.mjs` returns only the accepted `em-dash-overuse` advisory from EIC padding.
- **Screenshots.**
  - **How taken:** headless Chrome under `timeout 60` with `--timeout=15000 --virtual-time-budget=5000`, served on 127.0.0.1:9860 (server stopped afterwards).
  - **Coverage:** full pages at 1440, 1024, 768, and 390 through a 390 px iframe, each with the frame folded and unfolded and the notebook open.
  - **Scroll width:** equals the viewport at every width.
  - **Result:** nothing is clipped or overlapping. At 390 the frame and the cell 4 output scroll inside their own regions (`.fw`, `.df-wrap` `overflow-x: auto`).
  - **Dark mode:** the site has none, so light only.
  - **Files:** `scratchpad/fmrev/shots/`.
