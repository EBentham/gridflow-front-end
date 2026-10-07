# openmeteo/solar-weather: review

Checker: Sonnet 5.5 · high, 2026-10-06. Family `solar-weather`, lead `historical_solar`, member `forecast_solar`.

## Verdict: REVISE

The chart, the sample frame, the notebook and every vendor fact on the historical side check out. The page does
not meet the seat's condition for shipping the forecast member with its loss stated: it never says that no
`forecast_solar` row was fetched before its target hour, and three fields still present the member as a forecast feed.

Counts: 1 blocker, 1 major, 7 nits.

## Findings

### 1. Blocker: the forecast loss is not stated (`page.what_it_is`, whole page)

The seat's ruling lets `forecast_solar` ship with its loss stated "plainly and prominently enough that no reader
would treat these rows as forecasts with lead time". The page's only statement is the last sentence of
`what_it_is`: "Silver keeps no model run time, so a forecast row's lead time is unknown." That is not the loss, and it
points the wrong way: it implies each row has a lead time that nobody recorded. The lead time is known to be
negative. Every stored row was fetched after its target hour. The author found this (author report, "Can history and
forecast share a chart?" and Defect OMa) and then chose to keep it off the page ("Its silver problem ... stays off
the page").

Evidence (all reproduced):

- Silver `forecast_solar` has 2,160 rows: 1 to 5 Aug and 13 to 22 Sep 2026, six sites, 24 hours a day. In Polars,
  `available_at - timestamp_utc` runs from 90 h to 373 h, so no row has a non-negative lead.
- The two bronze sidecars confirm it: `fetched_at` 2026-08-16T13:29:15Z for `start_date=2026-08-01&end_date=2026-08-06`,
  and 2026-09-26T17:44:01Z for `start_date=2026-09-13&end_date=2026-09-22`. Silver `available_at` is an ingest-run
  stamp from the same two runs (13:29:15 to 13:29:16 on 16 Aug, 17:44:01 on 26 Sep), a fraction of a second after the
  sidecar `written_at`; the forecast transformer applies no reconstruction (`VINTAGE_POLICY = None`,
  `silver/openmeteo/forecast.py`). I did not trace the exact derivation in `silver/base.py`, so the page should not
  say `available_at` is "the bronze write time"; "the time gridflow stored the response, not a model run time" is safe.
- The connector sends any window it is given to `/v1/forecast` with no guard against past dates
  (`connectors/openmeteo/client.py`, `_fetch_location`).

What the page needs, in the hero fields a reader sees first (`summary` or `what_it_is`, plus the family line for
`forecast_solar`): a plain sentence that the forecast host returns whatever it holds for the dates asked, that
gridflow's connector sends any dates, so a row fetched after its hour is an after-the-fact value rather than a
forecast made in advance, and that `available_at` is the time gridflow stored the response, not a model run time.
Prefer this code-rule framing (a code fact) in `what_it_is`. The family line is the seat-sanctioned place for the
plain statement about the stored rows: "Forecast host and its own grid cells; one value per hour, no run time,
fetched after the hour". It stays inside the 14-word budget only if trimmed, so shorten the first half.

On the figure: the author report and the note say "4 to 16 days". The measured spread from target hour to write time
is 3.75 to 15.5 days (90 h to 373 h). If a number goes on the page, either use these or say "days after the hour".

### 2. Major: the page suggests uses silver cannot deliver (`page.how_used[2]`, `page.summary`, `page.facts.history`)

- `how_used[2]`: "Forward irradiance for a day-ahead solar forecast, from `forecast_solar`." Silver holds no row fetched
  before its hour, so it cannot supply forward irradiance. This is the "use silver can't deliver" case.
- `summary`: "... as archive history and as forecasts." The second half describes the vendor's API, not what the
  stored table contains.
- `facts.history`: "forecasts up to 16 days ahead" is a true vendor fact (`forecast_days` 0 to 16) but sits in the
  hero beside a member whose stored rows have no lead. It needs the loss beside it, or it should say "the Forecast
  API serves up to 16 days ahead".

Suggested fix: reword `how_used[2]` to what silver can do ("Irradiance values for hours already passed, from
`forecast_solar`, as the forecast host returned them") or drop it and keep the two historical uses. Reword `summary` to say the forecast member holds after-the-fact values.

### 3. Nit: stale ERA5 and near-real-time wording left in the canonical note body (`historical_solar.md`)

The corrections the author made are right (see "Verified" below). Residual instances of the old claims remain:

- line 134, H1: "Historical Solar Weather (ERA5 archive, GB capacity-weighted sites)".
- line 161: "For near-real-time use [forecast_solar]". With finding 1 this is wrong.
- lines 391 and 398, the vintage-policy section: lag "5 days ... from this page's '~5 days behind real time' ERA5
  reanalysis cadence". The author deleted that sentence from the lag row, so the citation now points at text that
  is gone. The author logged the premise as Defect OMd, so the seat may accept leaving it until the research unit.
- `forecast_solar.md` lines 305 to 310 ("Day-ahead solar-PV modelling", "Pair against historical_solar at matching
  lead times") promise lead-time features the silver cannot provide.

None of these text spans render on the page.

### 4. Nit: unexpanded acronym and mixed facts in the hero (`page.facts.cadence`)

"Hourly values; archive ERA5 data 5 days late, IFS without delay": the vendor figures are right (ERA5 and ERA5-Land
"5 days delay", IFS "No delay", vendor docs table), but "IFS" is never expanded on the page and ERA5-Land is omitted
from the "5 days late" clause. The `family.members[0].differs` line names "ECMWF IFS", so the hero could match it.

### 5. Nit: `page.related[1].note` describes the wrong quantity

"NESO's embedded solar forecast, a benchmark for an irradiance model". The NESO series is a generation forecast in MW,
not irradiance. Something like "NESO's embedded solar output forecast, to compare with irradiance" fits (9 words).

### 6. Nit: alt text "Both lines sit at zero each night" (`page.chart_view.alt`)

Kent carries 1.0 W/m² at the 04:00 stamp on several nights of the series (for example index 4, 13 June). Say "at or
near zero".

### 7. Nit: request URLs show decoded commas (`page.raw_feed.requests`, `page.family.members[].request`)

The bronze sidecars record `hourly=temperature_2m%2Cshortwave_radiation...`; the page shows commas. The vendor accepts
both and the author disclosed it. Same convention as the demand-weather sibling, so consistent, not wrong.

### 8. Nit: frame caption (`page.record.caption`)

"under low cloud, mostly diffuse light" holds for the eight rows in total (direct sums to 1,063 W/m², diffuse to
2,445), but the first row (07:00) has direct 190 above diffuse 75. Acceptable as written; mention only if the seat is
tightening captions.

### 9. Nit: hero scenery has no solar element on a solar page

Seat design question (author template problem 4), recorded here for completeness. The hero at all four widths shows
wind, gas station, substation, interconnector. Nothing is clipped or overlapping.

## Verified (no finding)

Facts and chart provenance:

- **Chart series.** The committed series (`spec_origin: vault`, sha `f16b1815...`) equals silver exactly: 168 hourly
  `shortwave_radiation_wm2` values per site, Cornwall and Kent, 13 to 19 June 2026 UTC (`vals == series.values` is
  True for both). Daily peaks: Cornwall 903, 901, 696, 494, 281, 550, 447; Kent 877, 866, 762, 817, 703, 818, 860.
  Every number in the alt text matches (903 and 877 at 13:00 on the 13th; Cornwall 281 to 696 from the 15th; Kent 703
  to 860 from the 15th). The notebook kWh/m² table matches silver sums (Cornwall 8.17, 8.36, 4.64, 2.40, 2.30, 3.45,
  3.16).
- **"Mean over the hour ending at its stamp."** Vendor docs (open-meteo.com/en/docs and /historical-weather-api, read
  today): `shortwave_radiation` "Shortwave solar radiation as average of the preceding hour", the five irradiance
  variables are "Preceding hour mean", temperature, cloud cover and snow depth are "Instant". The physics agrees: for
  Cornwall on the 13th the stamp 21:00 holds 5 W/m² and 05:00 holds 18, which an instantaneous value could not give
  at sunset (about 20:40 UTC) and a sunrise hour after about 04:10 UTC would give far more; a clear-sky cosine model
  with the preceding-hour average tracks the profile, the instantaneous one does not.
- **Variable name.** The connector requests `shortwave_radiation`, which `_PURE_RENAMES` maps to
  `shortwave_radiation_wm2` (`endpoints.py` `SOLAR_HOURLY_VARS`, `silver/openmeteo/historical.py`).
- **Grid cells.** All six sites differ between hosts in silver (Cornwall archive 50.298767 / -5.061493, forecast
  50.30215 / -5.004654; the other five also differ, one value per site in each table). "Its own grid cells" holds, and the
  vendor defines the response coordinate as the cell "used to generate this forecast".
- **Archive blend.** The connector sends no `models` (`client.py` `_fetch_location`, params: latitude, longitude,
  hourly, start_date, end_date, timezone, tilt, azimuth). Vendor: "The default Best Match combines IFS HRES, ERA5 and
  ERA5-Land seamlessly"; delays ERA5 and ERA5-Land 5 days, IFS none; ERA5 from 1940. The old "ERA5 reanalysis
  observations" and "~5 days (ERA5 cadence)" claims are corrected in `historical_solar.md` (overview, endpoint table,
  known issues) and the real-time claim in `forecast_solar.md`'s endpoint table.
- **Snowfall.** Both notes now say cm of snow, not water equivalent, with the vendor's "divide by 7"; the page's
  `snowfall_cm` line says the same.
- **Cloud layers and radiation wording** match the vendor text (low up to 3 km, mid 3 to 8 km, high from 8 km; DNI on
  the normal plane; direct and diffuse on the horizontal plane).
- **Request and commands.** Parameter order, host, path and float formatting match the sidecars. `ingest --end`
  2026-06-19 sends `end_date=2026-06-19`, so it is fetched (`runner.py` `resolve_dates`, `client.py`). An explicit
  `--start` is not moved by a watermark (`run_ingest`, non-incremental window). Bronze sits under the start date
  (`data_date=start.date()`); silver days 14 to 19 June read the covering 13 June partition.
- **Notebook.** `query()` filters `timestamp_utc`, both ends inclusive, orders by it, excludes the bitemporal columns
  (`gridflow_models/research/handles/source.py` `query`), relation `silver_open_meteo_historical_solar`. Five cells,
  no errors, one image; `needs` matches the commands; the plot alt matches silver (direct about 800 of about 900
  at midday on the 13th and 14th, diffuse the larger part from the 15th).
- **Build and gate.** `gridflow-build --only openmeteo/historical_solar` succeeds; `detect.mjs --json` returns `[]`.
  Both mirrors are byte-equal to the canonical notes (`cmp`). The page has 0 em dashes, 0 en dashes, no "live", "now",
  "locally", "held", "our ", "since 20", "yet", "soon", "planned" or "coming", and no percent-of or rows-of numbers.
- **Frame and guide.** `generated_by: gridflow-sample`, eight rows, `shape: (8, 23)`; the guide has a line for each of
  the 16 non-pipeline columns in frame order, key columns first.
- **Chart spec retired.** `site/hifi/data/chart-specs/openmeteo/` and `authored-pages/openmeteo/` do not exist in the worktree.
- **Layout.** Looked at 1440, 1024, 768 and a true 390 px iframe (light; the site has no dark theme), and at the
  unfolded frame and the opened demo notebook at 1440, 768 and 390. Nothing is clipped or overlapping; the chart
  and legend are fully visible at every width and the long `hourly` value wraps inside the code block. The unfolded
  frame scrolls sideways inside its wrapper (`.ds-dfs`, `overflow-x: auto` in `theme.css`), so the cut at the right edge
  is the scroll region, not clipping.
- **Related.** `elexon/agpt` carries `Solar`; `historical_demand` requests only `shortwave_radiation`;
  `historical_wind` requests the three cloud layers. Each note is 12 words or fewer.

## Could not verify

- Whether the archive revises IFS-filled recent hours when ERA5 arrives, and what `/v1/forecast` returns for past
  dates: neither is documented in the sources read. The author lists both as unknowns; neither changes the page once
  finding 1 is fixed.
