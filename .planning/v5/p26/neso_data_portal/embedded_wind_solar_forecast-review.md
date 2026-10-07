# neso_data_portal/embedded_wind_solar_forecast: review

Checker: Sonnet 5.5 · high, 2026-10-06. Port 9885 (server stopped). Rubric: `.planning/v5/review-rubric.md`.

## Verdict: REVISE

1 blocker, 1 major, 6 nits. The page's single-issue framing, the chart numbers, the time conversion, the append and
`_latest` mechanics, the request URLs and the commands all hold. The blocker is a cadence claim that the vault's own
catalogue snapshot contradicts.

## What I re-derived and confirmed

- **Build and detector:** `gridflow-build --only neso_data_portal/embedded_wind_solar_forecast` succeeds; `detect.mjs --json` returns `[]`.
  Em dashes, arrows and middle dots on the built page: 0. Grep for `locally|held|since 20|% of|live|now|real-time`: no hits (`our ` and `rows` hits are "four" and "the rows below").
- **Mirror:** `cmp` canonical note against `vault/neso_data_portal/embedded_wind_solar_forecast.md`: byte-equal. No staged chart spec or authored override exists.
- **Single issue (silver):** one parquet, 628 rows, one `issue_time` (2026-08-20 21:25 UTC), 628 distinct `event_time`s from 2026-08-20 21:00 UTC to 2026-09-02 22:30 UTC.
  4 periods on 20 Aug (SP45 to 48), then 13 days of 48. So the 628 rows are one issue's target periods, not two weeks of issues. The page never implies otherwise: the caption says "the forecast issue stamped ... every settlement period it covers", the title says "issued 20 August 2026", and "Lead time grows left to right" is correct for one issue. The notebook lead says "the dates match the 20 August 2026 issue".
- **What the issue stamp is:** the vendor's resource filename token (`202608202125_embedded_forecast.csv`), parsed by `silver/neso_data_portal/_bronze.py:42,209-220` with `tzinfo=UTC`, never the fetch clock. Sidecar: `fetched_at` 21:43:41.155, `ckan_last_modified` 21:25:03.319647, `resource_filename` as above. `published_at` equals `ckan_last_modified`, and silver `available_at == published_at` on all rows.
- **Chart:** committed series has 628 points, max 11,182.0 at 2026-08-24 12:00 UTC (SP27, settlement date 24 Aug). `settlement_period_to_utc` (`utils/time.py:28-42`) gives SP1 at 23:00 UTC the previous day in BST, so SP27 starts at 12:00 UTC. The sample row (SP27, `event_time` 12:00, `time_gmt_raw` "12:30") agrees. `time_gmt_raw == (event_time + 30 min)` in HH:MM on all 628 rows.
  Daily maxima by settlement date: 7,808 (21st, 10:00), 9,426, 11,087, 11,182 (24th, 12:00), 10,051, 8,442, 7,255 (27th, 12:30), 7,636, 7,628, 7,615, 7,861, 7,776, 7,539. The alt's peak hours (10:00 to 12:30) and the "7,255 to 7,861 from the 27th" are exact.
- **Append and `_latest`:** `APPEND_ONLY` and `VINTAGE_PER_BRONZE_FILE` (`embedded_wind_solar_forecast.py:131-132`); `LATEST_VIEW_SPECS` key `(settlement_date, settlement_period)`, default order `available_at` DESC (`latest_views.py:131-133` and the `LatestViewSpec` default). Dedup `unique(subset=ENTITY_KEY_COLUMNS, keep="last")` at line 266. All as the page says.
- **Notebook:** `gridflow_models` manifest maps the dataset to `silver_neso_data_portal_embedded_wind_solar_forecast_latest`, date column `settlement_date`; `_BITEMPORAL_EXCLUDE` is `event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year`. The lead matches. Cells are read-only; the JSON was written by `scripts/run_notebooks.py`; no error outputs. `plot_alt`: fourth hump is 24 Aug at 11,182 MW; wind min 263, max 2,483. Both correct.
- **Requests and commands:** `package_show?id=embedded-wind-and-solar-forecasts` is `CKAN_ACTION_PREFIX` plus `id` only (`client.py:802-833`, `endpoints.py`). The second URL equals the sidecar `request_url`. `--last 24h` gives `(now-24h, now)`; bronze partitions on `end.date()` (`client.py:1444`); transform covers start date to end date inclusive. A fixed historical window is refused (`SNAPSHOT_ONLY`, `_assert_window_admissible`), so the `--last 24h` commands are the only valid form.
- **Bronze and silver body corrections:** the new bronze sample rows match the real file `raw_20260820T214341Z_c90ad5f2.csv` byte for byte. The bronze path `raw_<fetched_at>_<8 hex of body sha256>` matches `bronze/writer.py` (`filename = f"raw_{ts}_{body_hash}.{ext}"`) and the real file. The silver sample row matches silver (857, 6417, 0, 23301, `published_at` 21:25:03.319647). One path-pattern error: finding 3.
- **Screenshots (looked at each):** 1440, 1024, 768 full page, and 390 in a 390 px iframe by section (chart, raw feed, frame folded, column guide, notebook, related). Nothing clipped or overlapping. Hero scenery tops, corner labels and the chart axis are fully visible. The unfolded frame (opened in the browser pane) scrolls and shows all 14 columns. The site has no dark theme. At 390 the folded frame shows only the two key columns before the fold; that is template behaviour, not a finding. The hero key chip wraps at 390 in this build (seat's known template item, ignored).

## Findings

### 1. BLOCKER: `page.facts.cadence`: "Issue cadence unstated by NESO" is false

- **Wrong:** NESO does state a cadence and a horizon. The vault's own catalogue snapshot, taken the same day as the capture, carries the package description.
- **Evidence:** `quant-vault/30-vendors/neso-data-portal/_generated/snapshots/20260820T214455Z/catalog-snapshot.json`, package `embedded-wind-and-solar-forecasts`, field `notes`:
  "NESO publishes at a half-hourly resolution the embedded ... wind and solar forecast from within day up to 14 days ahead. This forecast gets updated on an hourly basis."
  The archive resources are described as "All half hourly 0-14 day ahead embedded wind and solar forecasts published during <year>".
  The author report says the "CKAN catalogue snapshot carries no description" and lists cadence and horizon as "Unverified"; both are wrong. The canonical body still says "Issue cadence TODO (not stated)" (note line 138), also stale.
- **Fix (seat to choose):** (a) cite the vendor, as NESO's own claim: `cadence: NESO's catalogue entry says hourly updates; each file's name carries its issue instant`; or (b) just drop "unstated by NESO" and keep the filename clause, if the seat's rule "cadence as sent in the responses we hold, never as a vendor rule" is read to bar even an attributed vendor statement. Either way the current wording must go. Correct note body line 138 the same way, citing the snapshot. The horizon "up to 14 days ahead" is also citable (the 20 Aug issue runs about 13 days).
- **Read with finding 8:** the hourly sentence and NESO's "moved to its new forecast system, use the Jun - Dec dataset" notice sit in the same `notes` field, so the cadence statement may describe the successor system. The current resource is still updating (issue 21:25 on 20 Aug), so the page is not wrong on that account today; the seat needs both facts together.
- **Note:** the resource-level description in the same snapshot says "daily resolution", which contradicts the half-hourly data; do not quote that sentence.

### 2. NIT: `page.how_used[2]`: "scoring successive issues" needs the base view and accumulated captures, neither said on the page

- Structurally silver can deliver it: `APPEND_ONLY` with `issue_time` in the key keeps every captured issue, and the note body endorses "use the full base view keyed by `issue_time` for revision studies" (note line 267). Two caveats are missing from the page:
  - The page's own notebook reads `_latest` (newest issue per period), so that route cannot compare issues; the base view `silver_neso_data_portal_embedded_wind_solar_forecast` can.
  - Successive issues build up only as the ingest is repeated: `SNAPSHOT_ONLY` (D-35) and `_assert_window_admissible` refuse historical windows ("Backfill is not available", note line 260), and NESO's yearly archive resources, which hold every published issue, are not ingested (note line 137).
- Fix (optional): "Forecast error: scoring each captured issue against NESO's embedded outturn estimates, once its periods have passed." Rated nit because the page already says silver "appends every captured issue"; the seat may rule it a major under its "no use silver can't deliver" test, since a reader following the page's notebook cannot do it.
- Uses 1 and 2 are supported (the `elexon/indo` note states NESO's embedded wind and solar estimates are in neither `INDO` nor `ITSDO`).

### 3. MAJOR (vault body, rubric 7): silver path pattern `run<available_at>` is wrong

- **Wrong:** the canonical note now says `..._run<available_at>.parquet`. The real file is `embedded_wind_solar_forecast_20260820_run2026-08-20T21-43-41.158795-00-00.parquet`. The stamp is the bronze sidecar's `written_at` (21:43:41.158795), not the `available_at` column (21:25:03.319647, equal to `published_at`).
- **Evidence:** `silver/base.py` per-file loop (about lines 1005-1067): `available_at = self._timestamp_from_sidecar(...)` is passed to `_write_silver`. That function prefers `written_at` over `fetched_at` (`base.py:104-125`). Sidecar: `written_at 2026-08-20T21:43:41.158795+00:00`. The author's evidence table and report repeat "`run<available_at>`".
- **Fix:** `..._<YYYYMMDD>_run<bronze written_at, ISO with ":" and "+" replaced by "-">.parquet`, noting it is distinct from the `available_at` column. The rest of the corrected pattern (`year=<YYYY>/month=<MM>`, capture-date part) is right.

### 4. NIT: `page.chart_view.alt`: "Nights sit at or near zero (63 at most ...)" has no night window

- Between 21:00 and 02:30 UTC the maximum is 63 MW (2026-08-25 23:30 UTC), as stated. But the dawn ramp starts before sunrise: 03:30 UTC on 29 Aug is 144 MW (4 at 03:00, 380 at 04:00), and 03:30 UTC on each day from 27 Aug to 2 Sep is 123 to 144 MW. A reader taking "night" to include 03:30 finds 144.
- Fix: name the hours ("between 21:00 and 03:00 UTC") or drop the parenthesis. 63 MW is also invisible at the chart's scale.

### 5. NIT: `page.chart_view.caption` and `alt`: "stamped 21:25 UTC" states the zone as fact

- The filename token carries no zone; gridflow reads it as UTC, corroborated against `ckan_last_modified` (21:25:03) but not a vendor statement (`_bronze.py:209`, "read as UTC"). `what_it_is` and the guide say "read as UTC"; the caption and alt do not. Suggest "stamped 21:25 (read as UTC)" in one of them, or leave if the seat accepts the single qualification in `what_it_is`.

### 6. NIT: `page.facts.grain` / `record.key`: one row per key holds per capture, not across captures

- Reasoned from code, not reproduced (one capture held): ingest has no identical-body skip (`bronze/writer.py` hashes the body only for the file name and sidecar), the silver file name carries the microsecond `written_at`, and `_write_silver` does no cross-file dedup. Two captures of the same issue therefore append two rows per key to the base view. `_latest` (the page's route) is unaffected. The author logged this as "to verify"; keep it in the defects list. No page edit needed unless the seat wants the grain scoped to "per capture".

### 7. NIT (vault body): bronze sample note states `TIME_GMT` convention flatly

- The new note text "`TIME_GMT` is half an hour after each period's start, UTC" is a measurement on one capture and sits above the note's own "undocumented ... corroborated non-bindingly" lines. Add "on this capture".

### 8. NIT (open question for the seat): NESO's catalogue notice about a new forecast system

- The same `notes` field says: "NESO have moved the data source to its new forecast system. We recommend that customers now use the 'Jun - Dec' dataset." The "Jun - Dec" resource is `Embedded Solar and Wind Forecast Archive 2026 (Jun - Dec)`. The current resource gridflow ingests is still updated (issue 21:25 on 20 Aug, `metadata_modified` 21:27), so no page sentence is false. But the vendor's recommendation and what it means for the "current" resource are not recorded anywhere. Record it in the note body and the backlog; the page needs no line unless the seat establishes the current file is superseded.

## Defects (paste as is)

- **gridflow, docstring (low):** `silver/neso_data_portal/embedded_wind_solar_forecast.py` module docstring ("rolling day-ahead forecast ... republished ... several times a day") and `silver/latest_views.py:128-129`. The issue runs about 13 days ahead, so "day-ahead" is wrong; NESO's catalogue entry says "from within day up to 14 days ahead ... updated on an hourly basis", so the cadence now has a vendor citation (`30-vendors/neso-data-portal/_generated/snapshots/20260820T214455Z/catalog-snapshot.json`, package `notes`). Fix: drop "day-ahead", cite the notes field.
- **gridflow, to verify (medium if real):** two ingests that capture the same issue add duplicate `(settlement_date, settlement_period, issue_time)` keys to the base view (no identical-body skip, no cross-file dedup, run stamp is microsecond `written_at`). Reasoned from code, not reproduced. Given NESO's stated hourly updates, a user ingesting more often than hourly would hit this routinely.
- **gridflow, naming (low):** `BaseSilverTransformer._write_silver(..., available_at=...)` receives the bronze sidecar `written_at` (via `_timestamp_from_sidecar`), while the silver column `available_at` is `published_at` for this dataset. The file stamp and the column share a name but differ (21:43:41.158795 against 21:25:03.319647 on the one capture), which is what led the author's body correction astray (finding 3). Rename the parameter (for example `run_stamp_at`) or document it; the other two NESO Data Portal pages will hit the same trap.
- **Vault, stale body (this review):** `embedded-wind-and-solar-forecasts.md` "Issue cadence TODO (not stated)" is contradicted by the catalogue snapshot's package `notes`; the silver path pattern says `run<available_at>` where the stamp is the bronze `written_at`.
- **Vendor, open question:** the package notes recommend the "Jun - Dec" resource after a move to a new forecast system (finding 8). The resource description also says "daily resolution" for half-hourly data.
- **Vendor data observation (author's, confirmed):** the 20 Aug 21:25 UTC issue carries 1 to 63 MW of embedded solar in the small hours after 24 and 25 Aug (63 at 23:30 UTC on the 25th) and 1 to 2 MW scattered on later nights. Silver passes it through unchanged.
- **Front-end template (seat's):** hero key chip, already known; no new template problem from this page.
