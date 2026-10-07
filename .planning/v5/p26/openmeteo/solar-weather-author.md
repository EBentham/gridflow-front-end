# openmeteo/solar-weather: author report

Writer: Opus 5.5, 2026-10-06. Family `solar-weather`, lead `historical_solar`, member `forecast_solar`.

## Status

- **Build:** `gridflow-build --only openmeteo/historical_solar` is clean and wrote `data-sources/openmeteo/solar-weather.html`.
- **Detector:** `detect.mjs --json` returns `[]`. The page has 0 real em dashes.
- **Recommendation:** ship. The chart, frame and notebook all come from `historical_solar`, which is complete in local silver: 6 sites × 24 hours every day from 2021-09-01 to 2026-09-26, with no duplicate keys and no nulls in any variable. `forecast_solar` appears only as a family member, described from code alone. Its silver problem (Defects A and B) stays off the page.
- **Chart:** a line of `shortwave_radiation_wm2` (GHI, W/m²) for Cornwall and Kent, hourly, 13 to 19 June 2026 UTC. There are 2 series of 168 points, and no aggregation is needed because there is one row per hour and site.
- **Sample rows:** Cornwall, 07:00 to 14:00 UTC on 15 June 2026.
- **Notebook:** reads `historical_solar` for 13 to 19 June 2026, totals each day in kWh/m², and plots Cornwall's direct and diffuse light as a stacked area.
- **Screenshots** (light) at 1440, 1024, 768 and a true 390 iframe are in `scratchpad/shots-solar/`. Nothing is clipped or overlapping. The site has no dark theme: there is no `prefers-color-scheme` or `data-theme` rule in `site/hifi/assets/`, and the forced-dark shots are pixel-identical to the light ones. So there is no separate dark check to make.

## Files written

- Canonical note: `vault-p26-rest/30-vendors/open-meteo/datasets/historical_solar.md`. This adds the `page:` block and makes body corrections.
- Canonical note: `vault-p26-rest/30-vendors/open-meteo/datasets/forecast_solar.md`. Body corrections only.
- Mirrors: `p26-rest/vault/openmeteo/historical_solar.md` and `forecast_solar.md`. Both are byte-equal (`cmp`) and keep CRLF.
- Artefacts (front-end worktree):
  - `site/hifi/data/series/openmeteo/historical_solar.json`: `spec_origin: vault`, sha `f16b1815…`.
  - `site/hifi/data/samples/openmeteo/historical_solar.json`: `generated_by: gridflow-sample`, 8 rows.
  - `site/hifi/data/notebooks/openmeteo/historical_solar.json` and `historical_solar-5.png`: 5 cells, no errors, 1 image.
- No staged chart spec or authored override existed for Open-Meteo, so there was nothing to delete.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Six sites, Cornwall to Norfolk (`what_it_is`, `fields.location`) | `connectors/openmeteo/endpoints.py:88-95` `SOLAR_LOCATIONS`: east_anglia_norfolk 52.62/1.05, wiltshire_somerset, kent, cornwall 50.30/-5.00, sussex, oxfordshire. The comment there reads "approximate centroids; see ADR-020". |
| Twelve variables, the same on archive and forecast | `endpoints.py:141-154` `SOLAR_HOURLY_VARS`, wired to both datasets at `:186-195`. `forecast.py:61-69` subclasses the historical transformer unchanged. |
| Panel tilted 35° due south | `endpoints.py:163-166` `_SOLAR_GTI_PARAMS = (("tilt","35"),("azimuth","0"))`. The vendor docs say "0° south, -90° east, 90° west, ±180 north". The bronze sidecars for both datasets (2026-08-16 and 2026-09-26 fetches) record `tilt=35&azimuth=0`. The midday GTI/GHI median is 1.09 to 1.79 in every month of history and 1.15 to 1.40 in the forecast, never below 0.8. |
| One row per UTC hour and site; key `[timestamp_utc, location]` | `silver/openmeteo/historical.py:258` `df.unique(subset=["timestamp_utc","location"], keep="last")`. Polars: 0 duplicate keys in either table, 144 rows on every day. |
| Stamps are UTC | `client.py:115` sends `"timezone": "UTC"`; `historical.py:229-233` parses `time` and applies `replace_time_zone("UTC")`. The bronze response reports `"timezone":"GMT"`, `utc_offset_seconds: 0`. |
| Irradiance is the mean over the hour ending at the stamp (caption, x_label, fields) | Vendor variable table (open-meteo.com/en/docs and /historical-weather-api, read 2026-10-06): "Preceding hour mean" for shortwave, direct, diffuse, DNI and GTI. `shortwave_radiation` is "Shortwave solar radiation as average of the preceding hour". The quote is now in the note body. |
| Temperature, cloud cover and snow depth are values at the stamp; snowfall is the preceding hour's total in cm of snow, not water | Vendor table: "Instant" for temperature_2m, cloud_cover*, snow_depth. Snowfall is a "Preceding hour sum", described as "Snowfall amount of the preceding hour in centimeters. For the water equivalent in millimeter, divide by 7." |
| Cloud layers: low up to 3 km, mid 3 to 8 km, high above 8 km | Vendor table: "Low level clouds and fog up to 3 km altitude"; "from 3 to 8 km"; "from 8 km altitude". |
| Latitude and longitude are the vendor's grid cell, not the requested point | Vendor docs: "WGS84 of the center of the weather grid-cell … might be a few kilometres away from the requested coordinate". `historical.py:68-69` copies the top-level `latitude`/`longitude`. In silver, Cornwall is 50.298767/-5.061493 in the archive and 50.30215/-5.004654 in the forecast, against the requested 50.30/-5.00. |
| The archive host by default blends ECMWF IFS, ERA5 and ERA5-Land (`family.differs`) | The connector sends no `models` (`client.py:109-118`). Vendor: "The default Best Match combines IFS HRES, ERA5 and ERA5-Land seamlessly." |
| Cadence: "archive ERA5 data 5 days late, IFS without delay" | Vendor table: ERA5 and ERA5-Land "Daily with 5 days delay"; ECMWF IFS "Every 6 hours with no delay". |
| History: "Archive from 1940 (ERA5); forecasts up to 16 days ahead" | Vendor: ERA5 "1940-present"; `forecast_days` "0-16". |
| Silver keeps no model run time | The `SolarWeather` columns have no run field. `forecast.py:65` sets `VINTAGE_POLICY = None`, and `available_at` equals the bronze `written_at` (for example 2026-08-16 13:29:15.57). |
| `forecast_solar` "its own grid cells" (`family.differs`; **checker: look hardest here**) | The vendor says the response coordinates are the centre of the grid cell "used to generate this forecast", which differs by model. The forecast host routes to NWP models and the archive host serves IFS/ERA5/ERA5-Land, at different vendor-stated resolutions (9 km IFS, 25 km ERA5). The specific difference (Cornwall 50.2988/-5.0615 against 50.3022/-5.0047) was observed in bronze and silver, so the wording rests on the vendor's definition plus that observation. It matches the demand-weather sibling's wording. |
| `forecast_solar` "one value per hour, no run time" (`family.differs`) | The same dedup, inherited. Read path: `historical.py:183-197` takes the exact partition, else the nearest earlier one within 35 days (`base.py:2337-2365`). |
| Raw request URLs | Copied from the recorded `request_url` in the bronze sidecars, with `%2C` shown as commas: param order `latitude, longitude, hourly, start_date, end_date, timezone, tilt, azimuth`, and floats formatted `50.3` and `-5.0`. The archive window was changed to the chart week. The forecast URL is the real recorded 13 to 22 Sep request. |
| Ingest `--end` is fetched; transform `--end` is inclusive | `pipeline/runner.py:479-501` makes a bare date midnight UTC. `client.py:113-114` `strftime("%Y-%m-%d")` sends both ends as vendor dates, and Open-Meteo `end_date` is inclusive. The 2026-09-13 sidecar (`end_date=2026-09-22`) returned 240 hours. `runner.py:947` makes one `fetch` per window, with no chunking. |
| "Bronze sits under the window's start date" | `client.py:131` `data_date=start.date()`. The sidecar path `…/2026/09/13/` holds a 13 to 22 Sep window. |
| Notebook lead: relation, date column, both ends, lineage dropped | gridflow_models `research/handles/source.py:401-451`: `SELECT * EXCLUDE(...)`, filtered on the manifest date column `timestamp_utc` (`silver/schema_manifest.py:287`), both ends inclusive. `BITEMPORAL_EXCLUDE` (`schema_manifest.py:77-85`) drops event_time, available_at, vintage_policy, source_run_id and dataset_version. The table is not APPEND_ONLY, so the relation is `silver_open_meteo_historical_solar`. |
| Chart alt numbers | From the committed series. Cornwall peaks at 903 (13th, 13:00) and 901 (14th), then 696, 494, 281, 550 and 447. Kent peaks at 877 (13th), then 866, 762, 817, 703, 818 and 860. Both are 0 at night. |
| Plot alt | `historical_solar-5.png`. Cornwall's daily kWh/m² in the notebook output runs 8.17, 8.36, 4.64, 2.40, 2.30, 3.45, 3.16. |
| Related: `elexon/agpt` has solar | `vault/elexon/agpt.md` page: "including solar"; `codes: Solar`. |
| Related: NESO embedded solar forecast | silver `neso_data_portal/embedded_wind_solar_forecast` has the column `embedded_solar_forecast`. |
| Related: historical_demand has global irradiance only | `DEMAND_HOURLY_VARS` (`endpoints.py:99-109`) holds `shortwave_radiation` and no other irradiance. |
| Related: historical_wind has cloud cover at three heights | `WIND_ARCHIVE_VARS` (`endpoints.py:113-127`) holds `cloud_cover_low/mid/high`. |

**Can history and forecast share a chart?** No, for two reasons.

1. The spec takes one `silver` table, so it cannot overlay two tables.
2. More importantly, every local `forecast_solar` row was fetched 4 to 16 days after its target hour, so an overlay would compare after-the-fact values from the forecast host with the archive, not forecast skill.

The caption says `forecast_solar` is not drawn. The page never implies forecast skill or continuity.

## Body corrections (smallest spans, with evidence)

`historical_solar.md`:

1. **Overview:** "observations from the ECMWF ERA5 reanalysis" was wrong on two counts: these are model values, not observations, and the source is the default blend. The text now says "values from Open-Meteo's archive", and quotes the vendor's Best Match sentence with the URL.
2. **Endpoint table, publication lag:** "~5 days (ERA5 cadence)" became the per-model delays from the vendor, plus the observed no-null fetch of 2026-09-27 00:10.
3. **New paragraph after the hourly variable list, "What a time stamp covers":** vendor quotes for preceding-hour means and sums, the instant variables, the cloud-layer heights, and UTC.
4. **Schema rows:**
   - `latitude`/`longitude` are the grid-cell centre (vendor quote and the Cornwall values).
   - `snowfall_cm` was "New-snow water equivalent per hour, cm". It is cm of snow, not water equivalent (vendor: divide by 7).
5. **Silver sample:** the lat/lon values for Cornwall and Norfolk are replaced with the real grid-cell values.
6. **Known issue "ERA5 reanalysis lag … may return null trailing values":** replaced with the model-dependent lag and the observed no-null recent fetch.

`forecast_solar.md`:

1. **Endpoint table, publication lag:** "Real-time — refreshed every ~1 hour" became the per-model update intervals from the vendor, noting that no model is pinned and the response names no run.
2. **Point-in-time line:** "overwritten on re-ingest" became "on re-transform", with a pointer to the rule.
3. The same "What a time stamp covers" paragraph, in short form.
4. The same `latitude`/`longitude` and `snowfall_cm` schema fixes. The sample lat/lon now holds the forecast grid cells (Cornwall, Kent).
5. **Known issue "On-disk GTI is north-facing (known-wrong)":** this was stale. The azimuth=180 silver is gone: local silver holds only the 2026-08-16 and 2026-09-26 fetches, both `azimuth=0`, with GTI/GHI evidence. The bullet is rewritten.
6. **Known issue "Each silver build replaces … with the latest fetch":** this was imprecise. The bullet now gives the exact-or-nearest-earlier partition rule, with file:line, and notes that `available_at` is the bronze write time.
7. **New bullet "Past dates are fetched as asked":** this records that every local row was fetched after its target hour (Defect A).

Left untouched, out of scope but stale:

- The "Net-new at F7.5 … backfill required / No bronze on disk" lines in both notes. Bronze and silver now exist from 2021.
- The vintage-policy section's "~5 days" premise. See the open questions.

## Could not verify

- **Whether IFS-filled recent archive hours are revised when ERA5 arrives.** If they are, re-fetching the same past week can change values with no vintage kept. Nothing in the repo or the vendor text I read settles it.
- **What `/v1/forecast` returns for a past `start_date`.** Archived runs stitched together? Which model? The vendor docs point to a separate "Historical Forecast API" for archived runs. Not needed for the page, because no forecast rows are shown.
- **Which NWP models the best-match router picks for these GB grid cells.** The response does not say.
- **Request URL commas:** the page shows commas decoded. httpx actually sends `%2C`, and the vendor accepts both. The demand-weather page does the same.

## Open questions for the seat

1. **Archive vintage policy.** The historical vintage policy (`historical.py:316-329`, ADR-031) reconstructs `available_at = event_time + 5 days`, citing an ERA5-only cadence. With the default blend including IFS HRES (no delay), the premise is shaky:
   - The +5 d stamp is conservative, which is safe against leakage.
   - But the values for recent hours may be IFS rather than ERA5, and may differ from what a later fetch returns.

   Worth a research unit. The page states only vendor facts.
2. **Forecast-host coordinates.** The forecast host returns different grid cells from the archive (Cornwall is about 4 km apart). Any model that pairs `forecast_solar` with `historical_solar` mixes two locations per "site". The page states this in `family.differs` ("its own grid cells").
3. **Landing card.** The hub copy (`openmeteo.json` landing, "ERA5 at 6 solar sites") is not mine to edit. It says ERA5 where the archive is the default blend. Consider "archive at 6 solar sites".

## Template problems (report only, not worked around)

1. **Raw feed URL formatter:** a long query value (`&hourly=…`) is set off by an empty line and an extra indent, compared with the other params. This shows at every width (1440 screenshot, raw feed). It is cosmetic. It probably affects every Open-Meteo page, and any URL with one long parameter.
2. **Family member heading** prints the dataset key and then the key again upper-cased (`openmeteo/historical_solar HISTORICAL_SOLAR`). For Elexon that second token is the vendor code (NDF). For Open-Meteo it is just the key in capitals, which reads like a code that does not exist.
3. **The `notebook.source` override is required for this vendor:** without `source: open_meteo` the runner calls `data.openmeteo` and fails, because the site vendor id differs from the gridflow source. The demand-weather block I saw in the shared vault worktree had no `source:` line. Worth a check by the seat, or a vendor-level default in `artefacts.notebook_source`. The manifest already carries `"notebook": {"source": "open_meteo"}`.
4. **The `power` landscape draws only wind, gas and interconnector scenery,** with no solar, on a solar page. This is a design question, not a defect.

## Defects

Paste-ready rows for the remediation list (`| # | Dataset(s) | Defect | Next step |`); the seat assigns the item number.

| # | Dataset(s) | Defect | Next step |
|---|---|---|---|
| OMa | forecast_solar, forecast_wind (same two fetches: hornsea sidecars 2026-08-16 for 1 to 6 Aug, 2026-09-26 for 13 to 22 Sep); forecast_demand partly (it also has 2026-09-03 and 09-04 fetches for 20 Aug to 6 Sep, a few days ahead) | No local row is a forecast made in advance. Silver holds only 1 to 5 Aug and 13 to 22 Sep 2026. Their bronze was fetched on 2026-08-16 (`start_date=2026-08-01&end_date=2026-08-06`) and on 2026-09-26 (`start_date=2026-09-13&end_date=2026-09-22`), 4 to 16 days after the target hours. The rows are whatever `/v1/forecast` returns for past dates, and `available_at` (the bronze write time) is after the hour. A model trained on them as forecasts would leak hindsight. | Schedule forward-looking forecast ingests (start = today), or fetch archived runs from the vendor's Historical Forecast API. Until then, label `forecast_solar` silver as after-the-fact values, not forecasts. T1 data op + research. |
| OMb | forecast_solar, forecast_demand, forecast_wind | No model run or issue time is kept, and the partition read does not mean "latest fetch wins". Silver day D reads the exact bronze partition D, else the nearest earlier one within 35 days (`silver/openmeteo/historical.py:183-197`, `silver/base.py:2337-2365`), then `unique(keep="last")` within it (`historical.py:258`). So a newer fetch filed under an earlier start date never replaces an existing exact partition. Lead time can't be recovered, and forecast skill can't be backtested. | Keep each fetch as a vintage (append-only plus a latest view, keyed on fetch time and target hour), and record the response's model and run if the vendor exposes them. T2. |
| OMc | forecast_solar (connector) | The connector sends any `start_date`/`end_date` to `/v1/forecast` (`connectors/openmeteo/client.py:107-116`), with no guard against past windows and no `models` pin. This is how OMa arose silently. | Refuse or warn on a forecast window that starts before today, or route past windows to the Historical Forecast API; consider pinning `models`. T1. |
| OMd | historical_solar (also historical_demand, historical_wind) | The archive vintage policy's +5 day lag assumes ERA5-only cadence (`historical.py:316-329`, ADR-031). The connector sends no `models`, so the archive answers with its default blend of IFS HRES, ERA5 and ERA5-Land (vendor docs). A fetch at 2026-09-27 00:10 UTC returned non-null values through 2026-09-26 23:00, which ERA5 cannot supply. Recent hours may be IFS values that differ on re-fetch, with no vintage kept. | Research unit: does the archive revise IFS-filled hours when ERA5 lands? Then either pin `models=era5` (or similar) for a stable archive, or keep vintages for the trailing window. Update the ADR-031 premise. T1 + research. |
| OMe | forecast_solar vault note (fixed on `docs/v5-p26-rest`) | The note claimed the on-disk forecast GTI was north-facing and known-wrong (OM-04). That silver is gone: current silver is all `azimuth=0`, with midday GTI/GHI from 1.15 to 1.40. The note's "Each silver build replaces … with the latest fetch" was also imprecise (see OMb). | Corrected in this branch's note body. Close the OM-04 forecast caveat. Docs only. |
