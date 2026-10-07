# openmeteo/demand-weather: writer report

Writer: Opus 5.5 · high, 2026-10-06. Family lead `historical_demand`, member `forecast_demand`.

## Status

- **Build:** `gridflow-build --only openmeteo/historical_demand` wrote `data-sources/openmeteo/demand-weather.html` with no errors for this page. The build also reports 1 to 2 errors "on pages not rendered by --only". Those belong to the other Open-Meteo writers' pages, which are still in progress.
- **Detector:** `detect.mjs --json` returns `[]`. The page has 0 em dashes. Grepping for local-data words found nothing.
- **Mirror:** both canonical notes were copied to `vault/openmeteo/` and `cmp` shows them equal. They are CRLF, edited with the Edit tool.
- **Artefacts** (all regenerated from real data):
  - `site/hifi/data/series/openmeteo/historical_demand.json`: `spec_origin: vault`, 2 series x 365 points, 17,520 rows used.
  - `site/hifi/data/samples/openmeteo/historical_demand.json`: eight real rows.
  - `site/hifi/data/notebooks/openmeteo/historical_demand.json` and `historical_demand-5.png`: 5 cells, no errors.
  - No staged spec or authored override existed for this dataset.
- **Screenshots:** light only, because the site has no dark theme (established in the ENTSO-E capacity writer report).
  - Widths: 1440, 1024, 768 and 390. The 390 shots used a 390 px iframe captured in 1,800 px offset windows, because full-height headless captures stop painting partway down.
  - Checked: hero scenery, chart and key, raw feed and both member URLs, commands, frame and guide, notebook panel, related links and every stratum's corner label.
  - Nothing is clipped or overlapping.
  - Files: `scratchpad/shots-dw/w{1440,1024,768,390}-{0,1800,3600[,5400]}.png`.
  - The server on port 9861 was stopped. Port 9670 was not touched.
  - The notebook drawer was not opened in a capture. Its degree-day table has 8 columns, but it sits in `.df-wrap { overflow-x: auto }` (`theme.css:431`), so at 390 it scrolls inside its box.
- **Late wording change:** `how_used[2]` now reads "Forward weather from `forecast_demand`, fetched ahead of the hours it covers". The earlier wording ("for a day-ahead demand forecast") recommended rows that silver cannot vouch for. Rebuilt; the detector is still `[]`.
- **For the checker:** the chart alt says "351 of the 365 days". The rubric's digits-plus-days grep will catch it. It is a count from the committed series (365 points), not a local-coverage claim.

## The chart, and why history and forecast do not share it

- **What it shows:** a line chart from silver `open_meteo/historical_demand`, value `temperature_2m_c`, filtered to `location in [london, glasgow]`.
  - Aggregation: `mean` with `time_bucket: 1d`, i.e. the mean of the 24 hourly instants in each UTC day.
  - Window: fixed, 1 September 2025 to 31 August 2026, unit °C.
  - Paint: London clay, Glasgow horizon.
- **History and forecast cannot share a chart:**
  - The spec reads one silver table.
  - The two members come from different hosts and different grid cells. For example, London is at 51.4938, -0.1630 on the archive and 51.5115, -0.1308 on the forecast host.
  - Silver `forecast_demand` keeps no model run time.
  - Every forecast fetch behind the local rows ran after most or all of its window. A line running from history into forecast would suggest a continuity and a forecast skill that the data does not have.
  - The caption says `forecast_demand` is not drawn and why.

## Evidence table

| Claim on the page | Evidence |
|---|---|
| Seven cities, London to Belfast; requested points | `connectors/openmeteo/endpoints.py:55-64` (`DEMAND_LOCATIONS`, comment "Major UK population centres") |
| Nine hourly variables requested, same set on both hosts | `endpoints.py:99-109`, `:169-177` |
| One GET per city; params `latitude, longitude, hourly, start_date, end_date, timezone=UTC` in that order; archive vs forecast host chosen by `historical` prefix | `connectors/openmeteo/client.py:88-116`, `endpoints.py:200-201`; bronze sidecar `request_url` for london (2026-09-26 fetch) matches |
| `end_date` is inclusive, so the ingest `--end` date is fetched | `client.py:114` formats `end` as a date; `runner.py:485-500` passes a bare date as midnight UTC unchanged; note param table "Inclusive end of the window"; the 2026-09-13 fetch with `end_date=2026-09-22` returned 240 hours ending `2026-09-22T23:00` |
| Bronze sits under the window's start date; transform reads the day's own partition, else the nearest earlier one | `client.py:131` `data_date=start.date()`; `bronze/writer.py:36-46`; `silver/openmeteo/historical.py:178-212`; `silver/base.py:2337-2365` (35-day lookback) |
| Transform `--end` inclusive | `runner.py:1126,1138` |
| Grain and key: one row per UTC hour and city | `historical.py:258` `unique(subset=["timestamp_utc","location"], keep="last")`; silver has 0 duplicate keys in either table |
| `timestamp_utc` is the vendor `time`, requested in UTC | `historical.py:229-234` (parse, `replace_time_zone("UTC")`), `client.py:115`; bronze `utc_offset_seconds: 0` |
| Instants vs preceding-hour sums and means | Open-Meteo Historical Weather API docs (read 2026-10-06, quoted in the note body): temperature, humidity, pressure, wind and snow depth are "Instant"; precipitation and snowfall are "Preceding hour sum"; shortwave radiation is "Preceding hour mean" |
| Units °C, km/h to m/s, °, %, mm, W/m², hPa, cm, m | Vendor `hourly_units` in every bronze body (london, 4 forecast files); `historical.py:143-176` (km/h divided by 3.6, pure renames) |
| Snowfall is cm of snow, not water equivalent | Docs: "Snowfall amount of the preceding hour in centimeters. For the water equivalent in millimeter, divide by 7" |
| `hdd_k` = max(15.5 - T, 0); `cdd_k` = max(T - 22.0, 0); air density from pressure and temperature, dry air | `historical.py:45-50,272-292` |
| Latitude and longitude are what Open-Meteo returns, not the requested point | `historical.py:68-77` (response `latitude`/`longitude`); the rows show 52.47803, -1.840149 against the requested 52.4862, -1.8904 |
| Archive default blends ECMWF IFS, ERA5 and ERA5-Land; connector sends no `models` | Docs: "The default Best Match combines IFS HRES, ERA5 and ERA5-Land seamlessly"; `client.py:109-116` has no `models` |
| Cadence "ERA5 part arrives about 5 days late" | Docs: ERA5 and ERA5-Land "Daily with 5 days delay"; IFS "Every 6 hours with no delay" (both in the note body now) |
| History: archive from 1940 (ERA5); forecasts up to 16 days ahead | Docs (ERA5 1940 to present); note's Historical depth row and forecast param table (`forecast_days` max 16) |
| Forecast keeps no run time; a re-fetch overwrites | `forecast.py:33-41` (`VINTAGE_POLICY = None`, same transform); `schemas/weather.py` `DemandWeather` has no run column; dedup at `historical.py:258`; silver `available_at` equals the fetch time for every forecast day |
| Connector sends any date window, past ones included | `client.py:109-116` (start and end unchanged, no clamp to the fetch time) |
| Notebook lead: relation, date column, inclusive ends, lineage dropped | `gridflow_models` `_RELATION_NAME_BY_DATASET["historical_demand"] = silver_open_meteo_historical_demand`; manifest date column `timestamp_utc` (TIMESTAMPTZ, `schema_manifest.py:286`); `source.py:401-449` inclusive end, `_BITEMPORAL_EXCLUDE` |
| Alt numbers (16.4 and 14.5 °C start; lows -1.3 and -2.5 on 5 Jan; peaks 30.4 °C on 26 Jun and 20.6 °C on 25 Jun; London warmer on 351 of 365 days) | Committed series JSON, computed in Python |
| Plot alt numbers (-5.8 °C Manchester 01:00 on 6 Jan; Cardiff 11.5 °C at 20:00 on 11 Jan; end 8.9 to 10.1 °C) | Silver for 5 to 11 Jan 2026, Polars |
| Eight rows: Birmingham, 16:00 to 23:00 UTC on 8 Jan 2026, snowfall 0 rising to 3.29 cm | `gridflow-sample` output |

## Body corrections (canonical notes; mirrors copied)

`historical_demand.md`:
1. **Overview, first sentence.**
   - Before: "observations derived from the ECMWF ERA5 reanalysis at 7 GB population centres".
   - After: Open-Meteo's archive, whose default Best Match "combines IFS HRES, ERA5 and ERA5-Land seamlessly". The connector sends no `models`. The docs link and read date are added.
   - "7 GB" becomes "7 UK", with a note that Belfast is outside GB, citing `endpoints.py:55`.
2. **API table, Publication lag.** Added the docs' per-model delays: ERA5 5 days, IFS no delay.
3. **Silver schema.**
   - `precipitation_mm`: changed to "summed over the hour before the stamp".
   - `shortwave_radiation_wm2`: changed to "averaged over the hour before the stamp".
   - `snowfall_cm`: changed from "New-snow water equivalent per hour, cm" to cm of snow, not water equivalent.
   - Each row quotes the docs.

`forecast_demand.md`:
1. **Overview.** "7 GB" becomes "7 UK", with the same Belfast note.
2. **Silver schema.** The same three column meanings, each citing the forecast docs.
3. **Known issues, "Forecast vintages overwritten".** Made precise from the code:
   - The value kept is the latest fetch in the one bronze partition read for that day (`historical.py:178-212,258`).
   - The connector sends `start_date`/`end_date` unchanged (`client.py:109-116`). Silver therefore cannot tell hours that were already past at fetch time from hours forecast ahead.

I left everything else in both bodies as it was. Both notes still use many em dashes, but only in body text that the page does not render.

## Not verified

- **Which model the archive's Best Match uses over GB, and when.** For example, whether recent hours come from IFS and are later replaced by ERA5. If they are replaced, the historical note's line "ERA5 archive values are stable once published" may not hold for the newest days. I did not put this on the page.
- **What the forecast host returns for hours that were already past at fetch time.** The docs mention "past_days" and a separate Historical Forecast API but do not say how the forecast endpoint fills a past `start_date`. The page says only what the code shows.
- **The forecast note's claims about models and refresh rate:**
  - The router "typically ECMWF, GFS, or ICON". The docs say only "the highest-resolution applicable model is selected automatically".
  - "Refreshed every ~1 hour".
  - I left both unedited and kept them off the page.
- **Wind direction convention** (from or to). The page says only "degrees".

## Open questions for the seat

1. **The hub `openmeteo.json` describes the cities wrongly.** The `intro` says "GB demand cities", and `landing.start` says "ERA5 at 7 demand cities". Belfast is not in GB, and the archive is not ERA5-only. That file is the seat's, so I did not edit it.
2. **Chart choice.** A year of daily means at two cities shows the seasonal driver clearly. If Bobbo prefers all seven cities, the notebook plot already shows them for one January week.

## Template problems (seat's files; not worked around)

1. **The raw-feed URL formatter breaks inside words.** In a request box, the long `hourly=` value starts on a new line with an extra indent and wraps mid-word (`precipitatio/n` at 1440, `relative_hu/midity` at 768). Every Open-Meteo page will show this.
2. **The family member header shows an invented upper-case code** (`HISTORICAL_DEMAND`, `FORECAST_DEMAND`). The code seems to be built from the dataset key, as with Elexon codes. Open-Meteo has no such vendor codes, so it reads as a made-up code.
3. **`notebook.source` is required for this vendor.** Without it, the help-card cell calls `data.openmeteo` (the site vendor name) and fails with `AttributeError`. Setting `notebook.source: open_meteo` fixes it. Other Open-Meteo writers need the same line.
4. **The front-end `.venv` has no `tzdata`.** Ad hoc Polars reads of tz-aware columns in that venv raise `ZoneInfoNotFoundError: 'No time zone found with key UTC'`. `gridflow-distil` and `gridflow-sample` still worked. I ran my probes with the gridflow_models interpreter.

## Defects

Pasteable for the gridflow backlog and the vault remediation page:

- **open_meteo/forecast_demand (and forecast_wind, forecast_solar, which use the same code): no forecast run time, so leakage is possible.**
  - `ForecastDemandWeather` sets `VINTAGE_POLICY = None` and inherits the `(timestamp_utc, location)` dedup (`silver/openmeteo/forecast.py:33-41`, `historical.py:258`). The schema has no run or issue column, so each re-fetch silently replaces the last.
  - The connector passes `start_date`/`end_date` straight from `--start`/`--end` (`connectors/openmeteo/client.py:109-116`), with no clamp to the fetch time.
  - Local bronze shows every forecast fetch ran after most or all of its window:
    - 1 to 6 Aug, fetched 16 Aug.
    - 20 Aug to 6 Sep, fetched 3 Sep.
    - 21 Aug to 9 Sep, fetched 4 Sep.
    - 13 to 22 Sep, fetched 26 Sep.
  - So silver "forecasts" are mostly values returned after the hour. They cannot support lead-time or skill work, and as day-ahead features they would leak.
  - Fix direction:
    - Store the fetch or run time in the key, or add a run column.
    - Ingest forecasts only forward of the fetch time.
    - Consider the Historical Forecast API or Single Runs API for backfills.
- **open_meteo forecast tables: the value kept depends on partition layout as well as fetch time.**
  - `read_bronze` reads only the day's own window-start partition if it has files, else the nearest earlier one (`historical.py:178-212`, `base.py:2337-2365`).
  - A newer fetch whose window started on an earlier day is therefore ignored for any day that has its own partition. "Latest fetch wins" holds only within one partition.
- **Vault (both demand notes, probably the solar notes too): `snowfall_cm` was documented as "New-snow water equivalent per hour, cm".**
  - The vendor docs say snowfall is cm of snow over the preceding hour, and is not water equivalent.
  - Corrected in both demand notes on `docs/v5-p26-rest`. Check `historical_solar.md` and `forecast_solar.md`, which also carry `snowfall_cm`.
- **Vault and hub: the demand cities were called "GB", and the archive "ERA5".**
  - `DEMAND_LOCATIONS` includes Belfast, which is in Northern Ireland and outside GB (the code comment says UK).
  - The archive default blends IFS HRES, ERA5 and ERA5-Land.
  - Corrected in both demand notes. `site/hifi/data/openmeteo.json` (`intro`, `landing.start`) still says both.
- **The historical vintage policy assumes 5 days for all rows.**
  - `_historical_vintage_policy` uses a 5-day lag (`historical.py:316-329`). The docs give ERA5 a 5-day delay but IFS no delay.
  - The reconstructed `available_at` (hour + 5 days, on 301,560 rows before 1 Aug 2026) is a labelled assumption. The vintage-policy rule text already says "ASSUMPTION", so this is recorded for the record and is not a blocker.
