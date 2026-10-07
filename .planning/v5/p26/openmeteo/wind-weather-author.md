# openmeteo/wind-weather: author report

Writer, 2026-10-06. Family `wind-weather`, lead `historical_wind`, member `forecast_wind`. Writer port 9862.

## Status

- `gridflow-build --only openmeteo/historical_wind`: clean. It wrote `data-sources/openmeteo/wind-weather.html`, and the two member pages now point to `wind-weather.html#<member>`.
- `detect.mjs --json`: `[]`. The page has 0 em dashes.
- Artefacts, all from their generators:
  - `site/hifi/data/series/openmeteo/historical_wind.json` (gridflow-distil, `spec_origin: vault`, 4 series x 168 points);
  - `site/hifi/data/samples/openmeteo/historical_wind.json` (gridflow-sample, 8 rows x 25 columns);
  - `site/hifi/data/notebooks/openmeteo/historical_wind.json` and `historical_wind-6.png` (scripts/run_notebooks.py, 6 cells, no errors).
- No staged chart spec or authored override existed for either member.
- Mirrors: `vault/openmeteo/historical_wind.md` and `forecast_wind.md` were copied from the vault worktree and are `cmp`-equal. Both are still CRLF.
- Screenshots: 1440, 1024, 768, and 390 (in a 390 px iframe). Everything is visible and nothing overlaps, including the hero turbines, the chart and key, the long request URLs (they wrap inside their boxes), the folded frame, the guide, the notebook panel and the related list.
  - Light only: the site has no dark theme (no `prefers-color-scheme` or `data-theme` in any stylesheet or script).
  - Shots are in `scratchpad/ww-shots/`.
- **Chart:** history member only. `wind_speed_100m_mps`, line chart, hourly, at `beatrice`, `walney`, `hornsea` and `whitelee`, 29 September to 5 October 2025 UTC.

## Can history and forecast share a chart?

No, not honestly with what silver holds.
- The units match (both m/s after the same ÷3.6 conversion).
- But forecast rows keep no model run or issue time. The connector captures none, and the response carries no run field; silver keeps only the fetch time, as `available_at`.
- Both held forecast fetches asked for dates already past:
  - the fetch of 16 Aug asked for `start_date=2026-08-01&end_date=2026-08-06` (silver holds 1 to 5 Aug, because the transform window stopped there);
  - the fetch of 26 Sep asked for `start_date=2026-09-13&end_date=2026-09-22` (bronze `.meta.json`).
- The two hosts also answer from different grid points for the same site (`triton_knoll` archive 53.392, 0.171; forecast 53.443, 0.430).
- An overlay would read as forecast against outturn when it is not.

The template draws from the lead's table anyway. The caption says forecast rows are not drawn and why.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| 12 locations, 8 offshore and 4 onshore, approximate centres from capacity registers (`what_it_is`) | `connectors/openmeteo/endpoints.py:66-85` (`WIND_LOCATIONS`, comments by region); `gridflow/docs/DECISION_LOG/ADR-020` ("approximate centroid drawn from public capacity registers (TEC, DUKES...)") |
| Grain: one row per hour and location; key `(timestamp_utc, location)` (`facts.grain`, `record.key`) | `silver/openmeteo/historical.py:258` `df.unique(subset=["timestamp_utc","location"], keep="last")`. Silver has 0 duplicate keys in either member (Polars). |
| Hourly, stamped in UTC (`facts.cadence`, `timestamp_utc` field) | `client.py:115` sends `timezone=UTC`. Responses carry `"timezone":"GMT","utc_offset_seconds":0` (bronze). `historical.py:229-234` parses `hourly.time` and tags it UTC. |
| Wind speed and gusts converted from km/h to m/s | `historical.py:143-150` `_UNIT_CONVERSIONS` (factor 1/3.6). Responses' `hourly_units` say `km/h` (bronze). Vendor docs: default `wind_speed_unit` is `kmh`. |
| Speeds are instant values at the stamp; precipitation is summed over the hour before (field lines) | Open-Meteo docs, fetched 2026-10-06. Forecast page: wind speed "Instant"; precipitation "sum of the preceding hour"; `wind_gusts_10m` "maximum of the preceding hour". Archive page: gusts "of the indicated hour". So the gust line says only "for the stamped hour". |
| History has 10 m and 100 m only; the forecast adds 80, 120, 180 m (`what_it_is`, family `differs`) | `endpoints.py:113-138` (`WIND_ARCHIVE_VARS`, `WIND_FORECAST_VARS`). Silver schemas: history 18 measured columns, forecast 24 (Polars `collect_schema`). |
| The archive answers with Open-Meteo's default model blend, not pure ERA5 (`raw_feed.note`, family `differs`, related note) | `client.py:109-116` sends no `models`. Vendor docs: "The default Best Match combines IFS HRES, ERA5 and ERA5-Land seamlessly." |
| Forecast keeps no model run or issue time (`what_it_is`, `caption`, `differs`) | `client.py:109-132` (no run capture; `RawResponse` carries only `fetched_at`); `WindWeather` has no run column (`schemas/weather.py:75-110`). The response body has no run or model field (bronze). |
| Air density is derived by gridflow from surface pressure and 2 m temperature (field) | `historical.py:282-292` `(surface_pressure*100)/(287.05*(T+273.15))` |
| Latitude and longitude are the grid point the vendor answered with, not the request's (fields) | `historical.py:68-77` takes the response's top-level `latitude`/`longitude`. Silver `hornsea` holds 53.884, 1.737 for the request 53.88, 1.79. |
| One request per location; bronze files each response under the window's first day (`raw_feed.note`) | `client.py:88-95` (one gather per location), `client.py:131` `data_date=start.date()`. Bronze `forecast_wind__hornsea/2026/09/13/` holds the 13 to 22 Sep window. |
| Request URLs (`raw_feed.requests`, `family.members[].request`) | Parameter order and `%2C` encoding copied from the bronze `.meta.json` `request_url` (archive: hornsea, 2025-01-13; forecast: hornsea, 2026-09-13). Window dates changed for the archive example only. |
| `ingest --end` is fetched (`commands` comment) | `pipeline/runner.py:479-501` (a bare date is midnight UTC) and `runner.py:947` (passes `end_dt` through). `client.py:114` formats it as `end_date`. Bronze shows 744 hours for `start_date=2025-01-13&end_date=2025-02-12` and 240 hours for 13 to 22 Sep, so the end day is included. |
| Transform reads the window from the first-day partition (commands work) | `historical.py:183-197` (exact partition, else covering); `silver/base.py:2337-2365` (nearest earlier partition, up to 35 days back) |
| `query()` reads `silver_open_meteo_historical_wind` on `timestamp_utc`, whole UTC days with both ends included; drops lineage and `vintage_policy`; `ingested_at` stays (`notebook.lead`) | gridflow_models `_get_method_registry.py:62-96` (half-open TIMESTAMPTZ predicate). Registry printout: date column `timestamp_utc`, relation `silver_open_meteo_historical_wind`, exclude `('event_time','available_at','vintage_policy','source_run_id','dataset_version','month','year')` |
| `notebook.source: open_meteo` | `artefacts.py:86-88`. Without it the help-card cell ran `data.openmeteo` and failed with AttributeError. |
| Chart numbers (`alt`, Beatrice key note) | Committed series. Lows: beatrice 0.417 (00:00, 29 Sep), walney 0.5 (02:00, 29 Sep), hornsea 0.361 (08:00, 30 Sep). Before 2 Oct the maximum is 15.167 (beatrice). Peaks on 3 Oct: walney 26.972 (16:00), whitelee 26.389 (17:00), beatrice 34.861 (23:00); hornsea 24.417 (12:00, 4 Oct). Last values 10.056, 12.528, 12.333, 11.917. |
| Key notes "Irish Sea", "Southern North Sea", "Scotland" | `endpoints.py` region comments (lines 68, 73, 79) |
| Key note "Moray Firth" (Beatrice) | ADR-020 ("Moray Firth / Forth (Beatrice, Seagreen)"); `endpoints.py:76` says "Moray / Forth" |
| `plot_alt` | The executed plot `historical_wind-6.png`, viewed, plus daily maxima from silver: up to 18.6 m/s on 2 Oct (whitelee); on 4 Oct whitelee runs 10.4 to 18.6 and the offshore three 17.8 to 27.3 |
| Related pages resolve | `site/hifi/data/elexon.json` (fuelhh, agws, windfor); `openmeteo.json` (historical_solar). The build passed. |

## Body corrections (vault worktree, both mirrored)

`historical_wind.md`:
1. **Overview.** The "from the ECMWF ERA5 reanalysis" claim is replaced by: Open-Meteo's archive API, with no `models` sent (`client.py:109-116`), whose default Best Match the vendor docs say "combines IFS HRES, ERA5 and ERA5-Land seamlessly". Dated 2026-10-06.
2. **Archive limitation paragraph.** "silver shape is identical between archive and forecast" was false. The transformer writes only its own variable list's columns (`historical.py:296-313`), so the history table has no 80, 120 or 180 m columns.
3. **Silver schema table.**
   - The six 80/120/180 m rows said "always null on this dataset"; they now say "column not written on this dataset".
   - `precipitation_mm` "mm/hr" now reads "mm, sum of the preceding hour (vendor docs)".
4. **Paragraph after the table.** "they are always null" now says the columns are absent, citing `historical.py:296-313`.

`forecast_wind.md`:
1. **Publication lag.** "refreshed every ~1 hour by the upstream NWP router" (unverified) is replaced by the vendor docs' per-model update frequencies (IFS 6 h, ICON 3 h, GFS 1 h).
2. **`precipitation_mm`.** Same unit fix as above.
3. **"Forecast vintages overwritten".** "replaces ... with the latest fetch" was not guaranteed. It now says the row comes from the partition the transform reads (the exact day, else the nearest earlier one), latest fetch within it. A newer fetch filed under an earlier start date does not win.
4. **New bullet.** Past windows are fetched like future ones, and the response names no model run.

Not changed (stale but not wrong for the page): the "net-new at F7.5 ... backfill required / No bronze on disk" lines in `historical_wind.md` (Overview and Implementation delta). Bronze and silver now exist. The seat may want them trimmed.

## Not verified

- **Gust timing on the archive endpoint.** The archive docs say "of the indicated hour"; the forecast docs say "maximum of the preceding hour". The page stays neutral ("for the stamped hour").
- **Which model actually answered a given archive hour.** The response names none. Recent hours may come from IFS HRES rather than ERA5, which matters for the vintage policy's 5-day lag assumption.
- **Why `triton_knoll`'s archive grid point (53.392, 0.171) is about 18 km west-south-west of the requested 53.45, 0.42.** Both hosts report `elevation: 0.0` for it, so a land cell is not shown. The cause is not established.
- **The vendor history depth** ("since 1940") was not used. The `facts.history` field is omitted.

## Open questions for the seat

1. Is a forecast member whose held rows were all fetched after their hours fine as "thin but accurate"? The page never calls them forecasts of anything and says no issue time is kept. I recommend ship. The defect goes to the backlog.
2. Should the hub copy in `openmeteo.json` change? The intro "the ERA5 archive", landing "ERA5 at 12 wind sites" and "forecast at the same wind sites" all overstate (see template problems). This is the seat's file.

## Template problems (not worked around)

- **Uppercased member codes.** The family member heading prints the dataset id uppercased as if it were a vendor code (`openmeteo/historical_wind HISTORICAL_WIND`, `... FORECAST_WIND`). That is right for Elexon (`NDF`), but meaningless for Open-Meteo. It probably affects every Open-Meteo, NESO and ENTSOG family.
- **Long query parameter wrapping.** The request formatter puts a blank line before the long `&hourly=...` parameter and indents it one step deeper than the other parameters. It is readable and not clipped at any width, but looks odd.
- **`openmeteo.json` hub and landing text** claims ERA5 outright and calls the forecast member "forecast at the same wind sites". Suggested: "archive (default model blend)" and "forecast-host rows at the same wind sites".
- **Notebook source.** Open-Meteo notes need `page.notebook.source: open_meteo`; the vendor id `openmeteo` is not a `data.` handle. Worth telling the solar-weather writer.

## Defects (paste into the gridflow backlog as is)

- **open_meteo forecast_* keep no forecast run or issue time, and accept past windows.**
  - `connectors/openmeteo/client.py:109-132` sends `start_date`/`end_date` straight from `--start`/`--end` and records only `fetched_at`. `WindWeather`, `DemandWeather` and `SolarWeather` have no run column.
  - Every held `forecast_wind` row was requested after its hour:
    - fetch 2026-08-16 13:28 UTC for `start_date=2026-08-01&end_date=2026-08-06` (silver holds 1 to 5 Aug; 6 Aug is in bronze only because the transform stopped at the 5th);
    - fetch 2026-09-26 17:44 UTC for `start_date=2026-09-13&end_date=2026-09-22`.
  - Silver already keeps the fetch time as the pipeline column `available_at`. What is missing is the model run or issue time; and because the fetch stamp is not in the key, only one fetch per hour and site survives.
  - Silver cannot support forecast-skill use. Fix: capture the model run (or use Open-Meteo's run-specific endpoints), and refuse or flag windows that end before the fetch.
- **Open-Meteo forecast vintage depends on bronze partition layout, not fetch time.**
  - `BaseOpenMeteoTransformer.read_bronze` (`silver/openmeteo/historical.py:183-197`) reads the exact-day partition, else `_find_covering_bronze_partition` (`silver/base.py:2337-2365`), which returns only the nearest earlier partition with files.
  - A newer fetch filed under an earlier start date loses to an older fetch in a nearer partition.
  - A day covered only by an earlier, wider window is dropped when a nearer partition without that day exists.
  - Affects all six Open-Meteo datasets.
- **open_meteo historical_* are not pure ERA5.**
  - The connector pins no `models` (`client.py:109-116`). The vendor docs say the archive default "combines IFS HRES, ERA5 and ERA5-Land seamlessly".
  - Code docstrings (`endpoints.py`, `silver/openmeteo/historical.py`, `schemas/weather.py`) and the vintage policy rule (`historical.py:316-329`, "ERA5 reanalysis cadence") assume ERA5.
  - Recent hours may be IFS values that change on refetch. Either pin `models=era5` (or `era5_seamless`) or document the blend and revisit the 5-day lag assumption.
- **open_meteo historical_wind: `triton_knoll` answers from a grid point about 18 km west-south-west of the request** (silver 53.391914, 0.171429 against the request 53.45, 0.42; the forecast host answers 53.442745, 0.4297638). Both hosts report `elevation: 0.0`. The cause is not established; check which cell the archive picks and why it is so far from the request.
- **Backfill comment wrong for Open-Meteo.** `cli.py:412` says "chunk_end is the exclusive API boundary", but Open-Meteo's `end_date` is fetched inclusive. Bronze shows 744 hours for 2025-01-13 to 2025-02-12, so each backfill chunk overlaps the next by one day. This is harmless (the exact partition wins), but the comment misleads.
- **Vault (fixed in this batch's vault branch).**
  - `historical_wind.md` claimed ERA5, "always null" hub-height columns and the same silver shape as the forecast.
  - `forecast_wind.md` claimed a ~1 hour refresh and latest-fetch-wins vintages.
  - Both gave precipitation as "mm/hr".

## Nits fixed (review `wind-weather-review.md`, APPROVE with 4 nits)

1. **Defects text and the "share a chart" bullets.**
   - The August fetch is now `start_date=2026-08-01&end_date=2026-08-06`, checked in bronze `forecast_wind__hornsea/2026/08/01/*.meta.json`. Silver holds 1 to 5 Aug.
   - The forecast defect now says silver already keeps the fetch time as `available_at`. What is missing is the model run or issue time, and the fetch stamp is not in the key.
   - The `triton_knoll` item now states only the grid point's distance (about 18 km west-south-west of the request). Both hosts report `elevation: 0.0`; the land-cell claim and the shear comparison are dropped, here and in "Not verified".
2. **`historical_wind.md` body: ERA5 brought in line with the Overview.**
   - H1 is now "(archive, GB capacity-weighted sites)".
   - The depth row names the blend's ERA5 component.
   - The publication-lag row gives the vendor docs' per-model delays (ERA5 and ERA5-Land 5 days, IFS HRES none) and says the response names no model.
   - The archive-limitation lead now reads "The archive".
   - The point-in-time line drops "ERA5 archive values are stable".
   - The vintage paragraph now reads "Archive rows". Its lag row notes the 5-day figure is the code's assumption, since IFS HRES has no delay.
   - The known-issues bullets "ERA5 reanalysis lag" and "ERA5 grid-cell snapping" are now "Archive lag" and "Grid-cell snapping".
   - The stale "net-new ... backfill required" (Overview) and "No bronze on disk" (Implementation delta) lines are trimmed.
   - ERA5 now appears only as a named component of the blend.
3. **`page.chart_view.caption` now says why these four sites and this week:** "Four of 12 sites (three offshore coasts, one onshore) over a week from near calm to 34.9." Every term is visible in the chart and key:
   - the region notes come from the `endpoints.py` comments and ADR-020;
   - the lows (0.361 to 0.5 m/s) and the peak (34.861) come from the committed series.
   - No cause is named. "hourly" was dropped to stay within the 40-word budget; the x-axis label still says "hour, UTC".
4. **`page.record.caption`:** "by name" is now "in alphabetical order" (the frame is ordered by `location`).

Checks after the fixes:
- Both canonical notes were copied to `vault/openmeteo/` and `cmp`-equal; still CRLF.
- `gridflow-build --only openmeteo/historical_wind` is clean.
- `detect.mjs --json` gives `[]`; em dashes on the page: 0.
- The chart spec and the record selection are unchanged, so the series, sample and notebook artefacts did not need regenerating, and the build's digest checks pass.
- No git writes, no paths deleted, and port 9670 was not touched.

**Summary:** all 4 review nits are fixed (defect text, the ERA5 wording in the vault body, the caption's reason for the site and week choice, the record caption), and the page still builds clean with detector `[]`.
