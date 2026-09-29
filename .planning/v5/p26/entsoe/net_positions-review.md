# entsoe/net_positions: checker review

Checker: Opus 5.5 · high, 2026-09-29. Inputs: the canonical note diffed against quant-vault `origin/master` (vault worktree `vault-p26-entsoe`), the mirror (`cmp` identical), the three artefacts, the page rebuilt with `gridflow-build --only entsoe/net_positions`, gridflow code, local silver (Polars, read only), and bronze XML and meta files (read only).

## Verdict: APPROVE

There are no blocker or major findings, and the four nits below are optional polish. The writer's sign correction is right, and the page scopes the direction reading honestly.

## What I verified (evidence)

**Sign and direction (focus 1).**
- Silver holds 5,376 rows. `quantity_mw` runs from 1.5 to 14,619.9, so no value is negative. `h6_market.py:81-88` only casts the value (`pl.col(...).cast(pl.Float64)`).
- 0 rows have both sides `REGION_CODE` or neither side. 0 (timestamp, zone) pairs have more than one row.
- The probe `entsoe_A25_net_positions_FR_20260601.xml:19-20` has `in_Domain` `REGION_CODE-----` and `out_Domain` `10YFR-RTE------C`, with 11,433.7 MW at position 1. A large FR position with FR on the `out_Domain` side fits FR as an exporter.
- I reproduced the writer's hourly join exactly: signed position (zone on `out_area_code` counts as export, positive) against `actual_generation` minus `actual_load`.

| Zone | Hours | Correlation | Sign agreement | Mean position | Mean gen minus load |
|---|---|---|---|---|---|
| DE-LU | 312 | 0.892 | 0.888 | -413 | -442 |
| BE | 312 | 0.413 | 0.949 | -3,277 | -2,920 |
| FR | 312 | 0.523 | 0.962 | 4,925 | 9,053 |
| NL | 312 | 0.630 | 0.439 | 2,046 | -5,342 |

- Against the day-ahead price minus the four-zone mean, the correlation is DE-LU -0.45, NL -0.38, BE -0.30 and FR -0.01. Exporting zones price below the mean.
- **NL's 44% does not make the reading unsafe for the NL rows on the page.**
  - NL's correlation with generation minus load is positive (+0.63). Its price correlation has the same sign as DE-LU's and BE's.
  - The residual (position minus generation-minus-load) averages +7,387 MW with a standard deviation of 4,126. That is a level offset in NL's `actual_generation` coverage.
  - A reversed reading would give negative correlations on both checks.
- **The page makes no NL direction claim.**
  - The only NL rows are two raw-code lines in the notebook's `.head(8)` output, with no direction label.
  - The chart, frame and plot are DE-LU only.
  - The general reading is marked "(a project reading)" in `what_it_is` and `record.fields`. Both key notes say the check is against DE-LU generation minus load, and the body says "checked for DE-LU".
  - This is the rubric's own pattern for a project-measured sign, so there is no finding.
- entsoe-py is not installed locally, so the writer's corroboration from it could not be checked. It is not cited on the page or in the note.

**The chart (focus 2).**
- `series/entsoe/net_positions.json` has `spec_origin: vault`, 2 × 672 points, `rows_matched` 1,344 and `rows_used` 672. There is no staged spec and no authored override.
- I joined the series to silver DE-LU rows (zone on either side, 14 to 20 Sep). The maximum absolute difference is 0.0 for both bands, and the band not in use is null.
- Every number in the alt checks out:
  - importing max 11,428.3 at 2026-09-14T17:30Z;
  - the 14th has 10 exporting points, max 852.2;
  - the 16th is 96 of 96 importing;
  - exporting max 13,218.9 at 2026-09-19T10:45Z;
  - the 20th is 96 of 96 exporting, max 12,714.2.
- The midday exports on the 15th and the 17th to 19th and the evening or night imports match the hour table. On the 17th and 18th there are also late-evening exports, and "mostly" covers them.
- Every DE-LU bronze XML for 14 to 20 Sep carries 96 `<position>` points under curve type A03. The A03 forward-fill branch (`parsers.py`) therefore adds no rows, and "as sent" holds.
- The filter pair (`in_area_code` and `out_area_code` each in {DE-LU, `REGION_CODE-----`}) selects exactly the DE-LU rows. `sum` runs over one row per quarter-hour.
- The caption states the dataset, unit, window, zone and "one row each". It explains why one band shows at a time and why both sit above zero. The meaning of each band is in the key; see nit 1.
- The day labels are centred on each day (SVG `text x` 131.9 to 826.1, 115.7 px apart).

**The note corrections (focus 3).**
- **Mirrored codes.** The request mirrors the zone into both parameters (`client.py:257`, `out_domain=mrid if doc_type.domain_style == "zone"`). The response does not mirror it: see the probe lines 19-20, and the silver `out_area_code` values above, which are never equal to `in_area_code`. The correction is right.
- **Fake GB sample.** GB and IE-SEM return a Reason 999 acknowledgement: 28 of the 84 bronze XMLs have no data, which is 14 days × 2 zones. Silver has only DE-LU, BE, FR and NL. No negative value exists, and there is no `PT60M`. The replacement row matches silver exactly (2026-09-17T07:00Z, `REGION_CODE-----` then DE-LU, 2059.1, `published_at` 18:16:48).
- **Day-ahead only, all PT15M.**
  - `endpoints.py:286-296` always sends `contract_MarketAgreement.Type=A01`, and the probe echoes `auction.type` A01 and `contract_MarketAgreement.type` A01.
  - Silver's `resolution` and `business_type` values are only `PT15M` / `B09` (5,376 rows).
  - The page words cadence as "in the responses gridflow holds" and `resolution` as "`PT15M` here", following ruling #39.

**Point time and cadence (focus 4).**
- `record.fields.timestamp_utc` reads "period start plus (position minus 1) times resolution". That matches `parsers.py` (`timestamp = start_dt + (position - 1) * resolution`) and the ruling.
- `published_at` is described as "Response `createdDateTime` ... a fetch-time stamp". This matches `_published_at.py`: DE-LU's 17 Sep `createdDateTime` is 18:16:48Z and the bronze `fetched_at` is 18:16:48.02Z.

**Other checks.**
- `raw_feed.requests` equals the bronze meta `request_url` for DE-LU on 2026-09-17, parameter for parameter and in the same order.
- Commands:
  - Ingest `--end 2026-09-21` resolves to midnight (`runner.resolve_dates`), and `day_subwindows` (`utils/time.py:123`) excludes that date.
  - Transform uses `date_range(start.date(), end.date())`, so its end date is included (`runner.py:1138`).
  - The dataset has no partition offsets.
- `notebook.lead` matches `source.py` `query()`: the `timestamp_utc` date column, `_date_range_predicate` with inclusive ends, the bitemporal exclude, and `ORDER BY` on the date column only.
- The notebook JSON was written by `scripts/run_notebooks.py`, every cell is read-only and no output is an error. The image matches `plot_alt`: it starts at -4,147, falls to about -11,400 on the 14th's evening, peaks 8,403 on the 15th to 13,219 on the 19th, stays below zero on the 16th and above zero on the 20th. `needs` equals the command window.
- The sample has `generated_by: gridflow-sample`, 8 real rows, and the caption matches them (flip at 07:00). There is a guide line for every non-pipeline column, key columns first.
- The build succeeds. The detector returns only the accepted `em-dash-overuse` advisory (66, from EIC padding), and the rendered page has 0 `—`.
- Leakage grep: no `locally`, `held`, `our `, `since 20`, digit+rows/days, `live`, `now`, `→` or `·`. The four related notes are 12 words or fewer and all links resolve.
- Screenshots at 1440, 1024, 768 and 390 (390 in an iframe inside a 500 px window), with the frame unfolded and the notebook open, plus folded shots at 1440 and 390. Port 9820; the server has been stopped.
  - Nothing is clipped or overlapping, and there is no horizontal overflow (scrollWidth ≤ width at every width).
  - The turbine tops are visible and the stratum labels are clear.
  - The unfolded frame and the notebook `.head(8)` output scroll inside their `overflow-x: auto` boxes (`.fw`, `.df-wrap`), which is by design.
  - The site has no `prefers-color-scheme` rules, so light is the only theme.
  - The DE-LU hyphen break in the key note at 390 is the template item the writer already reported.

## Findings

1. **nit** · `page.chart_view.caption`
   - **Issue:** The caption explains why one band shows and why both are above zero, but not what separates the bands. That only appears in the key ("DE-LU as out_Domain" / "as in_Domain").
   - **Evidence:** caption text in the note diff.
   - **Suggested fix:** A clause such as "the band is set by which side of the row holds DE-LU (a project reading)" would make the caption stand alone. It fits the budget if "one row each" is trimmed.

2. **nit** · `page.raw_feed.note`
   - **Issue:** "GB and IE-SEM return no-data acknowledgements in every response gridflow holds" is a statement about local bronze (28 of 28 files).
   - **Evidence:** The seat's "responses we hold" wording (ruling #39) was granted for cadence. GB also has vendor-side evidence in the note: the 2026-05-08 live probe and the note's own SDAC explanation for GB.
   - **Suggested fix:** Consider "GB and IE-SEM return no-data acknowledgements" without the local universal. Otherwise, leave it for the seat to rule as covered by #39.

3. **nit** · note body, "Silver layer" header
   - **Issue:** `**Point-in-time field**: none` is now inconsistent with the corrected silver sample, which carries `published_at`, and with the silver schema (`published_at` is a column, `h6_market.py:106-117`).
   - **Evidence:** The writer noted it and left it alone.
   - **Suggested fix:** A one-word fix (`published_at`, the response `createdDateTime`).

4. **nit** · note body, parameter-tuple row "domain-param-name" and the first "Known issues" bullet
   - **Issue:** "`in_Domain` only ... connector mirrors `out_Domain` to `in_Domain`" and "Set `in_Domain` only" are not corrected. The connector sends both `in_Domain` and `out_Domain` set to the zone (`client.py:257`, `_domain_params` `domain_style == "zone"`; bronze `request_url`).
   - **Evidence:** The corrected silver-schema paragraph now says so correctly, so the body disagrees with itself.
   - **Scope:** This text is pre-existing, not on the page, and optional.
