# openmeteo/wind-weather: review

Checker (Sonnet 5.5 · high), 2026-10-06. Family `wind-weather`, lead `historical_wind`, member `forecast_wind`.

## Verdict: APPROVE

No blockers, no majors, 4 nits. Every factual sentence on the page, every chart number, both request URLs, both commands and the notebook lead reproduce from gridflow code, silver, bronze and the Open-Meteo docs. The two nits that matter (1 and 2) are in the defect text and the vault body, not the page.

## Checks run

- `gridflow-build --only openmeteo/historical_wind` in the front-end worktree: clean (wrote `data-sources/openmeteo/wind-weather.html`).
- `detect.mjs --json` on the page: `[]`. Em dashes on the page: 0. Grep for `locally|held|our |since 20|% of|real-time|live|now|yet|soon|planned`: only false hits inside words (`hour`, `four`).
- Mirrors: `cmp` of both canonical notes against `vault/openmeteo/` is byte-equal. No staged chart spec or authored override exists for the family.
- Series: `gridflow-distil`, `spec_origin: vault`, window 2025-09-29 to 2025-10-05, 672 rows used (4 sites x 168 hours), `null_values_dropped: 0`.
- Sample: `generated_by: gridflow-sample`. Notebook: `generated_by: scripts/run_notebooks.py`, 6 cells, no error output, every cell read-only, `source: open_meteo`.
- Screenshots (headless Chrome, a static server on 9882, one on 9790 for wrappers; both stopped): 1440, 768 and a true 390 px iframe, all sections; 1024 covered by the author's shots and my 768 and 1440 runs. Light only (site has no dark theme). Looked at hero turbines, chart and key, both request boxes (long `hourly=` strings wrap inside their boxes), folded frame, guide, related list. I also unfolded the frame in the browser pane (it scrolls horizontally inside its box, nothing clipped) and opened the notebook (cards, `.head()` table, shear output and the plot image all render). Nothing clipped or overlapping at any width.

## Verified against the sources (all pass)

| Claim | Evidence |
|---|---|
| Chart numbers (alt, key note, plot_alt) | Polars on `silver/open_meteo/historical_wind`, 29 Sep to 5 Oct 2025: Beatrice max 34.861 m/s at 2025-10-03 23:00 UTC; Walney max 26.972 (3 Oct 16:00); Whitelee 26.389 (3 Oct 17:00); Hornsea 24.417 (4 Oct 12:00). Lows: Beatrice 0.417 (29 Sep 00:00), Walney 0.5 (29 Sep 02:00), Hornsea 0.361 (30 Sep 08:00). Max before 2 Oct is 15.167 (Beatrice, 1 Oct 06:00), so "at or below 15.2 to the end of 1 October" holds. Last values 10.056, 12.528, 12.333, 11.917, so "10.1 and 12.5" holds. 4 Oct: Whitelee 10.4 to 18.6, offshore three 17.8 to 27.3 (plot_alt "about 18 to 27", "10 to 19"). Max before 3 Oct across the four is 18.56, so "under about 19" holds. Beatrice is also the highest of all 12 sites in the window, so "the highest point" is true under either reading. |
| Units are really m/s | The connector never sends `wind_speed_unit` (`client.py:109-118`; wind `extra_params` is empty, `endpoints.py:178-185`). Vendor default is `kmh` (docs, fetched today). Bronze `hourly_units` say `km/h`. Bronze Beatrice 2025-10-03T23:00 `wind_speed_100m` is 125.5 km/h; 125.5 / 3.6 = 34.861 = silver. Silver conversion is `historical.py:143-150`. |
| Time stamps | `client.py:115` sends `timezone=UTC`; bronze answers `"timezone":"GMT","utc_offset_seconds":0`; `historical.py:229-234` parses `hourly.time` and tags it UTC. Docs: speeds, direction and gusts are "Instant" in the archive valid-time column; archive gusts text is "of the indicated hour"; precipitation is "sum of the preceding hour". The page's gust wording ("for the stamped hour") stays within both. |
| Key | `historical.py:258` `unique(subset=["timestamp_utc","location"], keep="last")`. Silver has 533,376 rows and 533,376 distinct keys (history), 4,320 and 4,320 (forecast). |
| 12 sites, 8 offshore, 4 onshore, approximate centres from capacity registers | `endpoints.py:66-85` and ADR-020 ("approximate centroid drawn from public capacity registers (TEC, DUKES...)"). |
| Request URLs, parameter order, `%2C` encoding | Match bronze `.meta.json` `request_url` for both hosts (hornsea 53.88, 1.79). Forecast example 2026-09-13 to 2026-09-22 is a real stored request. |
| `ingest --end` is fetched | `runner.py:481-502` (bare date is midnight UTC) and `client.py:114` (`end_date` is `end.strftime`). Bronze `2025-01-13..2025-02-12` holds 744 hourly points. |
| Transform from the first-day partition | `historical.py:183-197`, `base.py:2337-2365` (nearest earlier partition up to 35 days). A reader who ingests 29 Sep to 5 Oct gets one partition `2025/09/29` and the transform reads it for each later day. |
| Default model blend, not ERA5 | No `models` parameter anywhere in the request (`client.py:109-118`, no `extra_params` for wind). Archive docs, fetched today: "The default Best Match combines IFS HRES, ERA5 and ERA5-Land seamlessly." Quote is exact. |
| History has no 80/120/180 m columns at all | `WIND_ARCHIVE_VARS` (`endpoints.py:113-127`); `_output_columns` writes only that list's columns (`historical.py:296-313`). Silver history schema: no `*_80m`, `*_120m`, `*_180m`. Forecast schema has all six and they are 100% non-null in the stored rows. The archive docs list only 10 m and 100 m wind. |
| Forecast keeps no model run or issue time | `client.py:123-132` records `fetched_at` only; the response keys are `latitude, longitude, generationtime_ms, utc_offset_seconds, timezone, timezone_abbreviation, elevation, hourly_units, hourly` (no run or model field); `WindWeather` has no run column. The page says exactly this and nothing more. |
| Both stored forecast fetches asked for days already past | Bronze `forecast_wind__hornsea`: fetched 2026-08-16T13:28:59Z for `start_date=2026-08-01&end_date=2026-08-06`; fetched 2026-09-26T17:44:47Z for `2026-09-13..2026-09-22`. Same pattern at all 12 locations (24 partitions). True. The page does not state it, and does not imply history and forecast join (see below). |
| Forecast host answers from a different grid point | Hornsea: archive 53.884, 1.737; forecast 53.887, 1.806. Beatrice: 58.2425, -2.9605 vs 58.2633, -2.8760. The guide line ("the grid point Open-Meteo answered with, not the request's") is true. |
| Air density | `historical.py:282-292`, dry-air formula from `surface_pressure * 100 / (287.05 * (T + 273.15))`; values 1.13 to 1.20 in the frame are sane. |
| Notebook lead | gridflow_models `_get_method_registry.py` `_date_range_predicate`: TIMESTAMPTZ columns use `>= start 00:00Z and < (end + 1 day) 00:00Z`, so whole UTC days, both ends included. Lineage exclusion list is `bitemporal_exclude()` (same wording as the other leads). |
| How used | gridflow_models `estimators/wind/weather_assembly.py` builds a wind perfect-prog set from `open_meteo/historical_wind` (10 m and 100 m speed, 100 m direction, air density over the twelve sites) joined to FUELHH WIND. The 100 m / 10 m ratio is derivable from silver and varies by hour (min 1.02, max 1.49 at Beatrice that week), so the shear bullet is deliverable. |
| Related notes | All 12 words or fewer. AGWS has `Wind Offshore` and `Wind Onshore` rows (`vault/elexon/agws.md:11,20`). Solar archive request also sends no `models`, so "same archive and model blend" holds. |
| Vault vendor facts in `forecast_wind.md` | Update frequencies (IFS every 6 hours, ICON every 3, GFS every hour) match the forecast docs. The vintage bullet is right: rows are read from the exact day's partition else the nearest earlier one, files sorted by fetch time, `keep="last"`. |

## Findings

1. **nit** (defect text in `wind-weather-author.md`, "Defects" section; also the "Can history and forecast share a chart?" bullets). Three details in text that will be pasted into the backlog are off:
   - "fetch of 16 Aug asked for 1 to 5 Aug". The request was `start_date=2026-08-01&end_date=2026-08-06` (144 hourly points per location). Silver holds 1 to 5 Aug only, because the transform window stopped there, so 6 Aug is in bronze but not in silver.
   - "Fix: capture a run or issue stamp (or at least the fetch time as a key column)". Silver already keeps the fetch time as the pipeline column `available_at` (forecast rows: 2026-08-16 13:28:59.754 against the sidecar `fetched_at` 13:28:59.507; 2026-09-26 17:44:47.67 against 17:44:47.41). What is missing is a model run or issue time, and the fetch stamp is not part of the key. Say so, or the backlog item will propose something that already exists.
   - "`triton_knoll`... It may be a land cell." Both hosts return `elevation: 0.0` for that site (archive 53.392, 0.171; forecast 53.443, 0.430), which points to a sea or coastal cell, not inland. Its 100 m / 10 m median ratio is 1.57 (the onshore sites run 1.64 to 1.71 over the full history; offshore 1.17 to 1.26). Keep it as an unexplained odd site, not as a land-cell claim.
   The page itself says none of these, so this does not block the page.

2. **nit** (vault body, `historical_wind.md`). The Overview now says "not pure ERA5", but the same note still says ERA5 in the H1 (line 134, "ERA5 archive"), the facts table ("Publication lag ... ERA5 reanalysis cadence", line 176), line 303 ("ERA5 archive values are stable"), the vintage-policy paragraph (lines 410 to 417) and the known-issues bullets (lines 446 to 450, "ERA5 grid-cell snapping"). The smallest-span rule is respected, but the note now contradicts itself. At least the H1 should read "archive" with no ERA5 (the docs' own 5-day delay applies to ERA5 and ERA5-Land only; IFS has none). The author already flagged the stale "net-new at F7.5 ... No bronze on disk" lines; trim those too.

3. **nit** (`page.chart_view.caption` and `page.chart_view.key[0].note`). The page does not say why these four sites and this week. Nothing is false: the four sit on three coasts, one onshore, and the week holds the series' sharpest event (Beatrice 34.9 m/s). Seagreen (33.1 m/s) is higher than the other three drawn, and `triton_knoll` is left out (the site with the odd grid point). "Four of the 12" is honest as written; no change needed. Do not add a cause (a named storm) because nothing in the sources states one.

4. **nit** (`page.record.caption`). "at eight of the 12 locations, by name" has no clear meaning: the rows are sorted alphabetically by `location`. Say "in alphabetical order" or drop "by name".

## Notes for the seat (not findings)

- The wording "Forecast rows are not drawn: they keep no issue time" is accurate and plain, and the page never presents the forecast member as forecasts of anything or draws the two on one chart. The sharper reason (every stored forecast request was for hours already past, so nothing held was a forecast of its hour) is a code fact the page does not need; it is in the defect text and the `forecast_wind.md` body bullet "Past windows are fetched like future ones", both correct. The `differs` line ("keeps no model run or issue time") is the more precise phrasing; `what_it_is` and the caption say "no issue time", which is consistent.
- The vendor docs' "Historical Forecast API" and "Single Runs API" (past forecast runs as issued) exist; not used by gridflow and not on the page. Worth a vault line if forecast skill is ever wanted.
- Template and hub issues (uppercased member codes in the family heading, ERA5 wording in `openmeteo.json`, blank line before the long `hourly=` parameter) are left to the seat as instructed.
- The notebook help card on the page lists `refresh`, `describe`, `query`, `tail`, `coverage` and `list_datasets` but not `backfill`, which is in the executed JSON. Template rendering, not this page.

## Defects found by the checker (for the backlog, as found)

- **open_meteo `forecast_wind` stored fetch window is wider than the silver window.** The 2026-08-16 fetch asked for 2026-08-01 to 2026-08-06 (144 hours per location); silver holds 1 to 5 Aug, so the last day is in bronze only. Cause: the transform ran for 5 days. Harmless to the page; relevant to any reconciliation of bronze against silver.
- **open_meteo `triton_knoll` archive grid point is 18 km west-south-west of the request and unexplained.** Archive answers 53.392, 0.171 and the forecast host 53.443, 0.430 for the request 53.45, 0.42; both report elevation 0.0. Its 100 m / 10 m ratio behaves like an onshore site. Check which cell and whether `cell_selection=sea` is wanted.
