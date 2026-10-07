# neso/national-carbon-intensity: author report

Writer: Opus 5.5 · high, 2026-10-06. Family page; lead `carbon_intensity`, members `intensity_at`, `intensity_current`,
`intensity_date`, `intensity_fw24h`, `intensity_fw48h`, `intensity_period`, `intensity_pt24h`, `intensity_today`. Port 9867.

## Status

- `gridflow-build --only neso/carbon_intensity`: success. It wrote `data-sources/neso/national-carbon-intensity.html`, and the
  eight member pages point to `national-carbon-intensity.html#<member>` (checked on `intensity_today.html`).
- `detect.mjs --json`: `[]`, with no advisories. Real em dashes in the built page: 0. Middle dots: 0. Arrows: 0.
- The local-data grep (`locally|held|our |since 20|N rows|N days|yet|planned|soon|live|now`) found only false positives:
  "half-hour", the vendor's "14 days a call", and the template's "8 rows of 11 columns".
- **Artefacts** (all tool-written):
  - `site/hifi/data/series/neso/carbon_intensity.json`: `spec_origin: vault`, 1 series, 336 points, 14 to 20 Sep.
  - `site/hifi/data/samples/neso/carbon_intensity.json`: `gridflow-sample`, 8 rows.
  - `site/hifi/data/notebooks/neso/carbon_intensity.json` and `carbon_intensity-6.png`: `run_notebooks.py`, 6 cells,
    no errors.
- **Build housekeeping:**
  - The final `--only neso/carbon_intensity` build reports "1 error(s) on pages not rendered by --only, left for the full
    build". It is not this page and not `intensity_stats`. It is another NESO family still being written.
  - Checking that, I also ran `--only neso/intensity_stats` once. That re-rendered `intensity-statistics.html` from its
    writer's current note. I edited nothing of theirs, but their built page was regenerated.
- No staged chart spec or authored override existed for `neso/carbon_intensity`, so there was nothing to delete.
- **Notes and mirrors:**
  - All nine canonical notes were edited in the vault worktree with the Edit tool.
  - CRLF is kept: 0 LF-only lines in every note.
  - Each note was copied to `vault/neso/<member>.md`, and `cmp` is clean for all nine.
  - The vault worktree diff also shows `intensity_stats*.md`. Those changes are another writer's, not mine.
- **Screenshots**, under scratchpad `nci_shots/`:
  - `w1440.png`, `w1024.png`, `w768.png`, plus `w390.png` through a 390 px iframe. Cropped parts are `w<width>_NN.png`.
  - Light only, because the site has no dark theme.
  - Everything is fully visible except one template problem: the chart's unit label "gCO2/kWh" loses its "g" at 390
    (see Template problems).
- **Recommendation: ship.**
  - The snapshot members are thin, but the page states them by route, with no counts and no trend.
  - The chart and the frame come from the lead's continuous 2026-09-13 capture.
  - No repeated rows or wrong stamps appear on the page.
  - The vintage loss is stated plainly: there is no issue time, and the forecast is "as served at fetch time".

## What one row is, and whether the members are the same data

- **Grain and key:**
  - One row per half-hour, keyed `timestamp_utc` (the vendor's `from`, the period start). `period_end_utc` is the
    vendor's `to`, 30 minutes later on every row of all nine members.
  - The transformer dedups `unique(subset=["timestamp_utc"], keep="last")` (`silver/neso/carbon_intensity.py:485`).
  - That dedup runs **within one target date's bronze partition only**:
    - `_bronze_files` reads only the exact partition (`:141-154`).
    - The bronze partition date is the request window's first day (`connectors/neso/carbon_intensity.py:79`).
    - Silver is overwrite-per-date (`APPEND_ONLY = False`, `silver/base.py:2610-2640`).
    - No NESO latest view exists (`silver/latest_views.py` has none).
- **Same series by different routes (project check, not a vendor statement).** I joined each member's silver to
  `carbon_intensity` on `timestamp_utc`:

  | Member | Shared half-hours | `forecast`, `actual`, `index` diffs |
  |---|---|---|
  | `intensity_at` | 1 of 1 | 0 |
  | `intensity_date` | 239 of 240 | 0 |
  | `intensity_period` | 239 of 240 | 0 |
  | `intensity_fw24h` | 49 of 49 | 0 |
  | `intensity_fw48h` | 97 of 97 | 0 |
  | `intensity_pt24h` | 1 of 49 | 0 |

  - `intensity_date` against `intensity_period`: 240 shared, identical in every field.
  - `intensity_current` against `intensity_today`: the shared half-hour (2026-09-26 23:30 UTC) matches exactly:
    104 / 118 / `moderate`.
  - The page says only the code fact ("choose half-hours differently and parse to the same columns"). It does not
    state the measured agreement as a universal.
- **Coverage per member** (report only, never on the page):

  | Member | Rows | Half-hour starts (UTC) | Fetched |
  |---|---|---|---|
  | `carbon_intensity` | 674 | Two disjoint windows: 2026-07-31 23:30 to 08-05 23:30 (241), and 09-12 23:30 to 09-21 23:30 (433) | 2026-08-16 and 2026-09-26 |
  | `intensity_at` | 1 | 2026-07-31 23:30 | |
  | `intensity_current` | 1 | 2026-09-26 23:30 | 2026-09-27 00:19:11 UTC |
  | `intensity_date` | 240 | 07-31 23:00 to 08-05 22:30 (5 UK days × 48) | |
  | `intensity_period` | 240 | Same as `intensity_date`, from 240 one-period calls | |
  | `intensity_fw24h` | 49 | 07-31 23:30 to 08-01 23:30 | 2026-08-16 |
  | `intensity_fw48h` | 97 | 07-31 23:30 to 08-02 23:30 | 2026-08-16 |
  | `intensity_pt24h` | 49 | 07-30 23:30 to 07-31 23:30 | |
  | `intensity_today` | 48 | 2026-09-26 23:00 to 09-27 22:30 | 2026-09-27 00:32:55 UTC |

  - DATA-MATRIX's "674 rows, 31 Jul to 21 Sep" is the two disjoint windows above, not continuous coverage.
  - In `intensity_fw24h` and `intensity_fw48h`, every `actual` is filled, because the fetch came 15 days after the
    periods.
  - In `intensity_today`, `actual` is null on 46 of 48 rows. Only 23:00 and 23:30 carry actuals.
- **The from/to convention** (bronze sidecars and silver):
  - The range route returns every half-hour whose **end** lies in `[from, to]`, both included.
  - `/intensity/2026-08-01T00:00Z/2026-08-06T00:00Z` returned 241 half-hours, 07-31 23:30 to 08-05 23:30.
  - `/intensity/2026-09-13T00:00Z/2026-09-22T00:00Z` returned 433.
  - `fw24h`, `fw48h` and `pt24h` from `2026-08-01T00:00Z` behave the same way: 49, 97 and 49 half-hours, starting or
    ending with the half-hour that ends at `from`.
  - `intensity_at` at `2026-08-01T00:00Z` returned the 23:30 to 00:00 half-hour. This matches the code description
    "record ending at a datetime" (`endpoints.py:87`) and the vault's endpoints.md.
  - NESO's docs say only "between the {from} and {to} datetimes" and "All times provided in UTC". The page labels the
    convention "a project check".
- **Date routes use the GB settlement day, not the UTC date.**
  - `/intensity/date/2026-08-01` returned 2026-07-31 23:00 to 08-01 22:30 UTC.
  - `/intensity/date`, fetched 2026-09-27 00:32 UTC, returned 2026-09-26 23:00 to 09-27 22:30 UTC.
- **Stamps:**
  - NESO sends no issue or publish time.
  - `available_at` is the bronze sidecar timestamp under `--reingest` (the 1 Aug partition: 14:23:04.760263 =
    sidecar `written_at`), else the transform clock (`silver/base.py:1181-1183`; the September captures show
    `available_at` 7 to 15 ms before `ingested_at`).
  - `ingested_at` is the transform clock (`_add_common_columns`, `:664-671`).
  - The page never calls either stamp an issue time.
- **Forecast versus actual, and later fetches:**
  - `actual` is null for half-hours NESO has not estimated (`intensity_today`).
  - A re-fetch into the **same** partition replaces earlier values: bodies are read in filename (fetch-time) order and
    deduped keep-last. For example, the 1 Aug partition holds two bodies (13:16 to 5 Aug, 14:23 to 6 Aug), and the
    193 shared half-hours are identical.
  - So silver keeps no forecast vintage. A later fetch fills `actual`, and the forecast is whatever NESO served at
    that fetch.
- **Index bands:**
  - The vendor names are very low, low, moderate, high and very high (`schemas/neso.py:12` `IntensityIndex`; the vault
    quotes the docs).
  - The cut-offs are not in the response, and NESO's API docs give none.
  - Only `low`, `moderate` and `high` occur in silver.
  - In `carbon_intensity`, the index partitions cleanly by `actual`: low 34 to 89, moderate 90 to 169, high 170 to
    216, with no overlap. By `forecast` it does not: `moderate` covers forecast 28 to 179.
  - In `intensity_today`, where `actual` is null, the index follows the forecast (low 42 to 85, moderate 91 to 122).
  - The page says only "in these rows it tracks `actual`", which is visible in the eight rows: the 19:30 forecast of
    28 is `moderate` with an actual of 136, and the 21:00 forecast of 114 is `low` with an actual of 84.

## Evidence table

| Claim on the page | Evidence |
|---|---|
| Unit gCO2/kWh | Column names `forecast_gco2_kwh` and `actual_gco2_kwh` (`schemas/neso.py:34-35`, transformer `:478-479`); vault Overview. NESO's docs do not state the unit in the excerpt fetched. |
| Grain: one row per half-hour, keyed by its start in UTC | Transformer `:476` (`from` becomes `timestamp_utc`) and `:485` (dedup); `period_end_utc - timestamp_utc` = 30 min on all rows of all nine members |
| Bands "very low to very high"; the response carries no cut-offs | `schemas/neso.py:12`; vault silver schema note; the response holds only `index` (transformer `_extract_intensity_rows` `:327-342`); NESO API docs give no thresholds (WebFetch of carbon-intensity.github.io/api-definitions) |
| "NESO sends no issue time, so silver cannot say which forecast run" | The response fields are `from`, `to` and `intensity{forecast, actual, index}` only (`:333-341`); no `published_at` is emitted, so `available_at` is the ingest scalar (`base.py:2095-2140`) |
| "The nine routes choose half-hours differently and parse to the same columns" | `endpoints.py:46-117`: all nine are `ParserFamily.INTENSITY` and share `_transform_intensity` |
| `how_used`: `intensity_fw48h` looks 48 hours ahead | `endpoints.py:97-103` path `/intensity/{from_dt}/fw48h`, "forward 48 hours" |
| Chart: line, `actual_gco2_kwh`, UTC days 14 to 20 Sep 2026 | Series: 336 points, `rows_used` 336, `null_values_dropped` 0, window fixed 2026-09-14 to 2026-09-20 |
| Alt numbers | From the committed series: opens at 194 at 00:00 on the 14th, dips to 183 at 02:00, reaches the window maximum of 195 at 05:00 (an earlier draft wrongly said "194 to 195 until 05:00", fixed after advisor review); at 11:00 UTC, 34, 117, 35, 42, 39 and 38 (15th to 20th); at 18:00 UTC, 156 (15th), 76 (18th), 164 (20th); last point 138 at 23:30 on the 20th; minimum 34, maximum 195 |
| Raw request `GET .../intensity/2026-09-14T00:00Z/2026-09-21T00:00Z` | `build_path` with `NESO_DATETIME_FORMAT` `%Y-%m-%dT%H:%MZ` (`endpoints.py:12, 289-312`); the client is relative to base `https://api.carbonintensity.org.uk`; the real sidecar `request_url` has the same form (`.../2026-09-13T00:00Z/2026-09-22T00:00Z`) |
| "Up to 14 days a call" | `_MAX_DAYS_PER_REQUEST = 14` (connector `:21`, chunking `:149-161`); vault README quoting the docs; NESO docs "maximum date range is limited to 14 days" |
| "Responses run from the half-hour ending at `from` to the one ending at `to` (a project check)" | Three bronze range captures and their silver (see above) |
| Commands: ingest `--start 2026-09-14 --end 2026-09-21`; transform `--start 2026-09-14 --end 2026-09-14` | Explicit dates are passed straight to `fetch()` (`runner.py:479-501, 947`); a 7-day window is one request (`:149-161`), written to bronze partition 2026-09-14 (`:79`). Transform iterates `date_range(start.date(), end.date())` (`runner.py:1138`) and reads only the exact partition (transformer `:141-154`), so the one date holds the whole window. A wider transform would log "covered-but-not-owned" for 15 to 20 Sep. |
| Frame: 8 rows, 15 Sep 18:00 to 21:30 UTC | `gridflow-sample` output (above); `select.columns` order |
| `forecast_gco2_kwh` "as served at fetch" | No vintage column; keep-last overwrite per partition (see above) |
| `actual_gco2_kwh` "null until NESO estimates it" | `intensity_today`: 46 of 48 null at a 00:32 UTC fetch; vault "often null before actuals publish" |
| `intensity_index` "in these rows it tracks `actual`" | The eight rows: 19:30 (28 / 136, moderate) and 21:00 (114 / 84, low) |
| Notebook lead | gridflow_models: relation `silver_neso_carbon_intensity`, date column `timestamp_utc` (TIMESTAMPTZ), half-open UTC instants with the end day inclusive (`_date_range_predicate`); excludes `event_time`, `available_at`, `vintage_policy`, `source_run_id`, `dataset_version`, `month`, `year` |
| Notebook outputs | `head()` from 2026-09-14 00:00 UTC (198 / 194 high); absolute error: count 336, mean 9.6, max 108 |
| `plot_alt` | The PNG (inspected): lines overlap; near 200 at the start of the 14th; the deepest single-half-hour drop is 28 at 19:30 on the 15th against an actual of 136 (the notebook max error of 108 = 136 - 28) |
| Family `differs`: `intensity_at` "the record ending at `from`" | `endpoints.py:87`; capture |
| Family `differs`: `intensity_current` "the half-hour NESO serves as current" | `endpoints.py:50`; deliberately not "the half-hour under way", because the 00:19 UTC capture returned 23:30 to 00:00 |
| Family `differs`: `intensity_date` "that UK day's half-hours" | Rows 23:00 to 22:30 UTC per date (BST) |
| Family `differs`: `intensity_period` "48 a day, 46 or 50 at clock changes" | `_settlement_period_count` (connector `:167-177`) and the loop at `:141-143` |
| Family `differs`: fw24h "past half-hours come back with actuals" | fw24h call for 2026-08-01, fetched 08-16: `actual` on all 49 rows |
| Family `differs`: fw48h "NESO forecasts up to two days ahead" | Vault `endpoints.md`: "Public forecast horizon is up to two days ahead of real time" |
| Family `differs`: `intensity_today` "actuals null until NESO estimates them" | Capture above |
| Related: `elexon/system_prices` gold view join | `gold/views/uk_imbalance_context.sql:29` `LEFT JOIN silver_neso_carbon_intensity ci` on `timestamp_utc` |
| Related: `neso/intensity_stats` "maximum, average and minimum national intensity over a range" | `_transform_stats` (`:501-532`); `endpoints.py:119-125` |
| Related: `neso/generation` "fuel mix ... for the same half-hours" | `endpoints.py:148-154`; `GenerationMix` keyed by `timestamp_utc` and fuel |
| Related: `neso/regional_intensity` "the same measure by region and nation" | `RegionalIntensity` has the same `forecast_gco2_kwh` / `actual_gco2_kwh` columns; vault README (`regionid` 15 to 17 are nations, 18 is GB) |

## Body corrections (canonical notes; mirrored)

1. **All nine notes, `**Dedup key**`:**
   - Was: `(timestamp_utc)`.
   - Now: `(timestamp_utc)`, scoped to one silver date partition. The line adds that nothing dedups across partitions
     and that the partition date is the request window's first day.
   - Cites `silver/neso/carbon_intensity.py:485` and `connectors/neso/carbon_intensity.py:79`.
2. **`intensity_today.md`, "Historical depth":**
   - Was: "Current UTC date", which is wrong.
   - Now: the current GB settlement day, with the capture's span (2026-09-26 23:00 to 09-27 22:30 UTC, fetched 00:32
     UTC).
   - A UTC date would start at 00:00 UTC; the rows start at 23:00 UTC the day before.
   - (The advisor suggested leaving this as unverifiable. The row span settles it, so I corrected it.)
3. **`intensity_fw24h.md` and `intensity_fw48h.md`, "Publication lag":**
   - Was: "Forecast product up to 24/48 hours ahead".
   - Now: the forecast horizon, plus the fact that a past `{from}` also returns estimated actuals, and that the first
     half-hour is the one ending at `{from}`.
   - Evidence: the 2026-08-01 calls fetched 2026-08-16 (49 and 97 rows, all with `actual`).
4. **`intensity_date.md`, `date` parameter:** I added "a GB settlement day, not a UTC date", with the real span for
   `2026-08-01`.
5. **`intensity_current.md`, Known issues:** a new bullet. The one capture (00:19 UTC) returned the half-hour that had
   just ended (23:30 to 00:00). "Current" is NESO's choice.
6. **`carbon_intensity.md`, Known issues:** two new bullets.
   - The `[from, to]` end-inclusive convention, with the real 241-row example. Adjacent windows and 14-day chunks
     therefore share their boundary half-hour across partitions (`connectors/neso/carbon_intensity.py:149-161`).
   - No issue time: `available_at` is the sidecar stamp or the transform clock (`silver/base.py:1181-1183`), and a
     re-fetch replaces values, so there is no forecast vintage.

Left alone:

- The 2024 bronze and silver samples are illustrative but well-formed (the real shape matches).
- The curl examples are correct for the vendor.
- The Modelling notes and gold section call the forecast ex-ante. That is logged as a defect, not rewritten.

## Unverified

- **Index cut-offs.** NESO's thresholds appear neither in the vault nor in the API docs. The project only sees that
  `index` partitions by `actual` in `carbon_intensity` and by forecast where `actual` is null. The page gives no
  thresholds.
- **Which forecast run `forecast` holds once a half-hour has passed.** NESO does not document it. No two fetches of the
  same half-hour at different lead times are held: every overlap compared was fetched after the fact, or within
  minutes. Whether the forecast for a past half-hour can change between fetches is unknown.
- **The `[from, to]` end-inclusive convention** is observed in every range and window capture, but NESO does not state
  it. The page says "a project check".
- **`intensity_current`'s "current" semantics.** One capture returned the just-ended half-hour. It could be a NESO
  update lag rather than a rule.
- **Whether `/intensity/date/{date}` returns 46 or 50 half-hours on clock-change days.** No clock-change date is held.
  Only `intensity_period`'s 46/50 loop is a code fact.
- **The unit.** It comes from code column names and the vault Overview. NESO's API docs page, as fetched, does not
  print "gCO2/kWh".

## Open questions (for the seat)

1. **Chart choice.** `chart_spec` takes one `value`, so the chart shows the estimated actual only. The forecast is in
   the frame and the notebook plot. If the seat prefers the forecast line (which shows the single-half-hour drops), it
   is a one-field change plus new words.
2. **The cross-partition duplicate (Defects 1).** It cannot appear in the page's window, because the chart and frame
   read one partition. If gridflow confirms it, the vault Known-issues bullet already describes it.

## Template problems

1. **The chart unit label clips at 390 px.**
   - `chart_svg.py:334` draws the unit `text-anchor="end"` at `x0 - 10`, left of the plot frame.
   - "gCO2/kWh" is wider than the left margin at 390, so its "g" is cut at the SVG's left edge (`nci_shots/w390_01.png`,
     zoom `z390_unit.png`).
   - 768, 1024 and 1440 are fine.
   - Any unit about as long or longer will do the same; I did not measure the exact threshold.
   - Suggested fix: anchor the unit `start` at the SVG's left padding, or widen the left margin from the unit's
     length.
   - Major under rubric 5. An author cannot fix it honestly, because the unit is the code's.
2. **Only one value column per chart.** Already logged by the `embedded_wind_solar_forecast` author. A forecast-versus-
   actual pair cannot be drawn. An optional `values: [col, ...]` that melts to `group` would fix it.
3. **The notebook plot cell's `<Axes: ...>` repr** shows as a text output before the image. This is cosmetic and the
   same on other pages (no trailing `;` convention).
4. **The y-axis top tick runs past the data** (250 at 1440, 300 at 390, against a maximum of 195). This is the
   renderer's nice-number rounding; harmless.

## Defects (paste as is)

- **gridflow, NESO silver, to verify (medium if real):**
  - The Carbon Intensity range and window routes return every half-hour whose end lies in `[from, to]`, both ends
    included. `/intensity/2026-08-01T00:00Z/2026-08-06T00:00Z` returned 241 half-hours, from 2026-07-31 23:30 UTC.
  - Each request's rows go to the bronze partition of the window's first day (`connectors/neso/carbon_intensity.py:79`).
  - The silver transformer dedups `timestamp_utc` only within one partition (`silver/neso/carbon_intensity.py:141-154`,
    `:485`), and no NESO latest view exists (`silver/latest_views.py`).
  - So the boundary half-hour of two adjacent ingests (for example `--end 2026-09-22` then `--start 2026-09-22`), and of
    the 14-day chunks of one long ingest (`:149-161`), lands twice in `silver_neso_carbon_intensity` and the other
    `neso/intensity_*` views. It is then duplicated by the `gold_uk_imbalance_context` LEFT JOIN
    (`gold/views/uk_imbalance_context.sql:29`).
  - The no-input routes (`intensity_today`, `intensity_current`) can do the same: their partition is the CLI `--start`
    date, not the day returned. The 2026-09-27 `intensity_today` capture sits in partition 2026-09-26.
  - Reasoned from code and observed request semantics. Not reproduced locally: the held partitions are disjoint (674
    unique of 674).
- **gridflow and vault docs, leakage (medium):**
  - `gold/views/uk_imbalance_context.sql` comments and the vault `carbon_intensity` Modelling notes present
    `forecast_gco2_kwh` as the ex-ante feature.
  - But NESO sends no issue time, and silver keeps one value per half-hour from the latest fetch: partition overwrite
    (`APPEND_ONLY = False`) with `unique(keep="last")` over bodies in fetch order.
  - A backfilled `forecast` is "as served at fetch", with no evidence that it equals what was known before the
    half-hour.
  - Fix: document the caveat, or capture the forecast append-only with the fetch stamp as vintage.
- **gridflow, schema (low):** `IntensityIndex` (`schemas/neso.py:12`) is defined but unused. `CarbonIntensity.intensity_index`
  is a plain `str` with default `""`, so an unknown or missing band is not caught.
- **Vendor data observation (no gridflow action):**
  - NESO's national `forecast` has isolated single-half-hour drops, with normal neighbours.
  - 2026-09-15 19:30 UTC: 28 against actual 136.
  - 2026-09-21 19:30: 38 against 203.
  - 2026-09-20 19:30: 61 against 149.
  - 2026-09-14 19:30: 65 against 144.
  - 2026-08-01 04:00 and 04:30: 46 and 31 against 118 and 113.
  - 2026-09-18 05:00: 38 against 87.
  - All were fetched after the fact. They recur at 19:30 UTC. Silver passes them through. The page shows the 15 Sep
    one in the frame and the plot alt, with no cause given.
- **Vault, fixed in this branch:**
  - `intensity_today` "Historical depth: Current UTC date" was wrong: it is the GB settlement day, 23:00 to 22:30 UTC in
    BST.
  - `intensity_fw24h` and `intensity_fw48h` called the routes a "forecast product", but a past `from` returns actuals.
  - All nine notes gave the dedup key without its per-partition scope.
  - All corrected with citations (see Body corrections).
- **Planning data (no action):** DATA-MATRIX "carbon_intensity 674 rows, 2026-07-31 to 2026-09-21" is two disjoint
  captures (241 + 433 half-hours), not continuous coverage.
- **Front-end template:** `chart_svg.py:334` end-anchors the y unit label left of the plot frame. "gCO2/kWh" clips at
  390 px.
