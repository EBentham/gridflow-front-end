# day-ahead-wind-forecast: writer's report

Family page `day-ahead-wind-forecast`, lead `da_wind_forecast_day_ahead` (eligible), members
`da_wind_forecast_day_ahead_bmu` (eligible), `da_wind_forecast_historic_day_ahead` (held),
`da_wind_forecast_historic_day_ahead_bmu` (held). Written 2026-10-24. The manifest's lead and
member list are right (page set `families/34`, same order as the note).

Files:
- canonical note `C:\gridflow-wt\vault-neso-gen\30-vendors\neso-data-portal\datasets\day-ahead-wind-forecast.md`.
  This note is **LF** (0 CRs), and was LF before I touched it: the seat's untouched mirror was LF
  and byte-identical. Line endings kept; the diff is insertions plus scoped replacements.
- mirror `C:\gridflow-wt\fe-neso-gen\vault\neso_data_portal\day-ahead-wind-forecast.md`, `cmp` clean
- `site/hifi/data/series/neso_data_portal/da_wind_forecast_day_ahead.json` (gridflow-distil, `spec_origin: vault`)
- `site/hifi/data/samples/neso_data_portal/da_wind_forecast_day_ahead.json` (gridflow-sample)
- `site/hifi/data/notebooks/neso_data_portal/da_wind_forecast_day_ahead.json` and `-5.png` (run_notebooks.py)
- page `site/hifi/data-sources/neso_data_portal/day-ahead-wind-forecast.html`

No staged chart spec, authored override or earlier artefact existed for this dataset.

Gates: `gridflow-build --only neso_data_portal/da_wind_forecast_day_ahead` wrote the page with no
error. Detector `[]`. Zero em dashes in the page.

Screenshots (light) at 1440, 1024, 768 and 390 (390 through a 390 px iframe, in four offset
slices because a single tall iframe stopped painting part way), in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\daw-writer\`
(`shot-<w>.png`, sections `c<w>-<n>.png`, 390 slices `d390-<n>a/b.png`). Nothing clipped or
overlapping: the four member keys wrap in their chips, the long request URLs and the three
commands wrap inside their wells, the frame folds behind `…` and the guide reads cleanly. The site
has no dark theme (as the Demand reports found). Server on 9801 started with its PID recorded
(29291) and stopped by that PID only.

## What one row is

| Member | One row | Quantity (unit from NESO's dictionary) |
|---|---|---|
| `da_wind_forecast_day_ahead` (national, current) | one settlement period of the next UK day: `datetime_gmt`, `date`, `settlement_period` | `incentive_forecast` MW, `capacity` MW (total operational wind) |
| `da_wind_forecast_day_ahead_bmu` (current) | one settlement period and one wind BM unit (`generator_name`, `generator_full_name`, `region`) | `wind_forecast` MW, `capacity` MW (the unit's) |
| `da_wind_forecast_historic_day_ahead` (held) | one target period and one `Forecast_Timestamp` label | same as national |
| `da_wind_forecast_historic_day_ahead_bmu` (held) | one target period, BM unit and `Timestamp` (UK time) issue, per yearly resource | same as BMU |

Half-hourly, not hourly: 48 periods per day in every capture; the dictionary's settlement-period
wording and the timestamps agree on half-hours.

**BMU against national: they sum.** In both captures, per period, the 231 unit `wind_forecast`
values sum to the national `incentive_forecast` within 0.497 MW (96 periods; the national figure is
whole MW, so it is the rounded sum), and the unit capacities sum to 25,365.8 against 25,366
(8 Oct) and 25,500.8 against 25,501 (16 Oct). NESO's BMU resource description says the file holds
"the windfarms which are used to produce NESO's national day ahead wind forecast". The page says
the sum holds "in NESO's files of 8 and 16 October 2026", and the notebook's second cell shows it
on the reader's own capture (`units per period: [231]`, `largest national minus unit sum, MW: 0.497`).

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Operational metered wind forecast, MW (`summary`, `what_it_is`) | Catalogue snapshot `20261006T195819Z`, resource `b2f03146`: "This is the NESO's day ahead operational metered wind forecast; the wind power forecast is in megawatts (MW)." |
| Daily, 09:00 to 09:15 clock time (`facts.cadence`) | same description: "Publication frequency: daily. Publication time: between 09:00 and 09:15 (clock time)." Stated as NESO's. |
| Archives from 2018 (`facts.history`, historic `differs`) | resource `7524ec65`: "All historic day ahead wind forecasts from 2018 to the most recent forecast"; BMU dumps "All historic day ahead BMU-level wind forecasts produced for <year>", 2018 to 2025. National archive silver starts 2018-04-16T23:00Z (UK 17 Apr 2018). |
| BMU file covers the farms of the national forecast (`what_it_is`) | resource `90e581e9` description, quoted above. |
| Units sum to national, nearest MW (`what_it_is`) | Polars on both captures (above); visible in notebook cell 2 output. |
| MW for `incentive_forecast`, `capacity`, `wind_forecast` | field-info `20261008T114228Z`: current national `Capacity` and `Incentive_forecast` unit MW (description of `Incentive_forecast` blank); historic: "Wind incentive forecast for day ahead produced for each half hourly settlement period", MW; BMU `Wind_Forecast` MW. |
| `datetime_gmt` is UTC period start (`record.fields`, x label) | dictionary unit "UTC ISO 8601"; registry `zone: UTC`, `temporal: utc_instant`; silver: SP1 of 17 Oct = 2026-10-16 23:00 UTC = 00:00 BST, and `timestamp_utc == datetime_gmt` on every row of both captures. |
| "period 1 ends 00:30 UK time" (`settlement_period` field) | current national dictionary: "Settlement period 1 represents the half hour ending 00:30 UK Time." |
| `published_at` = CKAN last-modified read as UTC, no issue time | registry `vintage: ckan_last_modified`, `issue: none`; ADR-030; silver equals sidecar `ckan_last_modified` (08:40:07.850057 and 08:40:07.867477). |
| Capacity "the same in every row here" | the eight rows all show 25501.0 (frame). |
| `tail()` reads `_latest`, lineage dropped, session zone | gridflow_models `source.py:453` (`ORDER BY timestamp_utc DESC LIMIT n`); `_validate_dataset_for_source` returns `timestamp_utc`, relation `silver_neso_data_portal_da_wind_forecast_day_ahead_latest` (probed with the gridflow_models interpreter). Notebook output shows UTC after `tz_convert`. |
| Requests (member `request`) | bronze sidecars of the 2026-10-16 captures (`request_url`); the BMU archive's two dumps from the 2026-10-08 and 2026-10-16 sidecars. Connector `client.py`: one `package_show`; upload files skipped when `last_modified` is unchanged (`:1752-1765`); dumps downloaded each run and skipped when the body hash matches the newest capture (`:1884-1949`). |
| Commands | `cli.py` `ingest`/`transform`/`pipeline` each take one dataset and `--last`; same `--last 24h` form as the approved Demand forecast and embedded-wind pages. The BMU file needs its own silver for the notebook, and three commands is the cap, so it gets one `pipeline` line (one window for both stages is fine here: a NESO capture's partition is the window's end date, which the same window transforms). |
| Held lines | ledger row and registry questions (below). |
| Related | `elexon.json` has `windfor` and `agws`; `neso_data_portal.json` has `14-days-ahead-operational-metered-wind-forecasts` and `daily_wind_availability` (the live page's table key). Reasons from those pages' own summaries. |

## Times and the clock (current files, scoped to their rows)

| Capture | Member | CKAN `last_modified` (read as UTC) | Target day (UK) | Rows | Target span, UTC |
|---|---|---|---|---:|---|
| 2026-10-08 09:17Z | national | 2026-10-08T08:40:07.850057 | 2026-10-09 | 48 | 2026-10-08 23:00 to 2026-10-09 22:30 |
| 2026-10-16 19:22Z | national | 2026-10-16T08:40:07.867477 | 2026-10-17 | 48 | 2026-10-16 23:00 to 2026-10-17 22:30 |
| 2026-10-08 09:17Z | BMU | 2026-10-08T08:35:11.947478 | 2026-10-09 | 11,088 | same |
| 2026-10-16 19:22Z | BMU | 2026-10-16T08:35:11.316089 | 2026-10-17 | 11,088 | same |

Every target starts after its file's vintage in both captures (the forward-target rule holds for the
16 October capture too). Both target days are BST, so each starts at 23:00 UTC the evening before;
the frame's caption and the chart caption say so. Note: 08:40 fails NESO's stated 09:00 to 09:15
window under either reading (08:40 UK time is before it; 08:40 UTC is 09:40 BST, after it).

## Held archives: one line each

- `da_wind_forecast_historic_day_ahead`: "Forecast time stamps carry no zone, and many fall at or after
  the period forecast." (15 words). Registry/ledger question: `Forecast_Timestamp` has no vendor zone
  and no offset; 192 targets carry two labels; about 14k labels fall at or after target start; when
  each value was available is undefined. The precedent's "end in Z" clause does not fit here: these
  values carry no `Z` (only the dictionary example does).
- `da_wind_forecast_historic_day_ahead_bmu`: "NESO gives each forecast's UK publication time, but nothing
  shows the values unchanged since." (14 words). Registry question: the dictionary gives `Timestamp`
  as a UK-time publication instant, but no source shows the archived values are unchanged since.

For the group's sibling forecast pages: the national archive's line is shaped by its own question
(no zone, late labels); a BMU or per-farm archive with a vendor publication stamp takes the second
form.

## Captures, row counts, repeats

| Member | Capture | Bronze rows | Silver rows | Against the earlier capture |
|---|---|---:|---:|---|
| national | 2026-10-08 | 48 | 48 | |
| national | 2026-10-16 | 48 | 48 | new target day; no `datetime_gmt` repeated (96 unique of 96) |
| BMU | 2026-10-08 | 11,088 | 11,088 | |
| BMU | 2026-10-16 | 11,088 | 11,088 | same 231 units, 10 regions; no (`datetime`, `generator_name`) repeated |
| historic national | 2026-10-08 | 148,825 | 148,825 | |
| historic national | 2026-10-16 | 149,209 | 149,209 | all 148,825 earlier rows unchanged; 384 added (UK days 9 to 16 Oct, 48 each) |
| historic BMU, 7 resources | 2026-10-08 only | 18,770,814 | same | 16 Oct ingest log: "7 unchanged since newest capture" |
| historic BMU, 2025 | 2026-10-08 | 3,136,000 | 3,136,000 | **truncated** (see Defects) |
| historic BMU, 2025 | 2026-10-16 | 3,683,474 | 3,683,474 | all 3,136,000 earlier rows unchanged; completes to 2025-12-31 23:30Z |

The BMU archive was never loaded whole: per-file counts and coverage came from parquet metadata
and statistics; only the two 2025 files were scanned, lazily, with selected columns.

The chart and frame read both national captures (96 rows); the `date` filter picks 48 (chart) and 8
(frame). `dedup: {"on": [datetime_gmt], order_by: published_at}` is set on both as a guard
(`duplicates_dropped: 0` today); it keeps the later file if one target day is ever captured twice.

## Chart

Line, `incentive_forecast` against `timestamp_utc`, filter `date == 2026-10-17`, window 2026-10-16
to 2026-10-17, one point per settlement period (48), MW, `y_min: 0`. From 11,425 at 23:00 UTC on the
16th (the day's highest) to 10,119 at 05:30, 10,214 at 07:30, 9,479 at 15:00, 9,619 at 18:00 and
8,966 at 22:30 (lowest). The key note gives operational capacity, 25,501 MW, which the frame shows.
I left capacity off the chart: a flat 25,501 line would add nothing the frame does not show, and an
axis from zero already shows the forecast as a share of the scale honestly. Held rows are never
charted.

## Body corrections (canonical note)

- Intro: national bullet now says 48 periods in each of the two captures; BMU bullet adds the
  measured sum relation (dated, with numbers); the historic national bullet now quotes NESO ("all
  historic day ahead wind forecasts from 2018 ...") instead of asserting "every forecast since 2018".
- Downloads: added the 2026-10-16 file names and CKAN stamps. "Captures to date (one per resource,
  all 2026-10-08)" retitled to the 2026-10-08 captures, and a new 2026-10-16 recapture table added
  (citing the ingest log for the seven unchanged dumps).
- National family: vintage "for the one capture" and "All 48 rows share it" replaced with both
  vintages; event time extended to the 16 Oct capture; forward-target, sentinel and identity
  paragraphs scoped to both captures; activation adds base table 96, `_latest` 48.
- BMU family: both vintages and target spans; forward-target for 16 Oct; "The capture has 231
  generators" now each capture; new paragraph "Relation to the national file (measured, not
  vendor-stated)"; zero counts given per capture (16 Oct: 96 zero capacity cells over two units,
  288 zero forecasts, 192 beside positive capacity); activation adds base 22,176.
- Historic national: vintage per capture; label counts scoped to 8 Oct plus the 16 Oct figures
  (3,015 labels, 148,825 one-label targets, the same 192 two-label targets, 14,181 and 13,899 late
  rows); new paragraph "Recent labels sit a day after publication"; activation adds the recapture.
- Historic BMU: `available_at` check scoped to the 8 Oct captures; a recapture row in the per-resource
  table; new paragraph "The 2026-10-08 capture of 2025 was cut short"; activation adds the recapture.
- Cadence: 16 Oct added to the morning stamps; the "is 2025 still appended to" TODO resolved (the
  growth was the truncation); "One capture per resource exists to date" replaced with two captures and
  the national archive's append observation, TODO narrowed to rewrite-versus-append.

Not changed: the Holds section's verbatim registry questions, front matter `updated:` (precedent
left it), the WINDFOR cross-check paragraph.

## Unverified

- Whether older `Forecast_Timestamp` labels follow the same "a day after publication" pattern the
  384 recent rows show. Two captures cannot settle it.
- What "incentive" means in `Incentive_forecast` (the note's TODO stands). The page says only "NESO
  calls it the incentive forecast".
- Whether NESO's 09:00 to 09:15 window describes the forecast run or is out of date (stamps are
  08:35 to 08:45 under either reading).

## Open questions

- Related is capped at 4. I chose Elexon `windfor` (the benchmark), Elexon `agws` (outturn to score
  against), the 14-day metered wind page (same fleet, longer horizon) and `daily_wind_availability`
  (per-unit, beside the BMU file). `embedded_wind_solar_forecast` is left out; the seat may swap it in
  for `agws` or the availability page.
- The notebook uses `tail()` with no dates (like the approved Demand pages) so a reader's own capture
  reproduces it; the BMU call passes `n = 20_000` to cover a whole day of units (11,088 today). The
  siblings can reuse cells 1 and 3 with their table key.

## Template problems

- Three commands is the cap; a family page whose notebook reads two members needs four lines
  (ingest and transform for each), so I used `gridflow pipeline` for the second member. Worth a
  higher cap for family pages, or a ruling that `pipeline --last` is fine for NESO captures.
- A comma inside an unquoted flow-mapping value (`comment: the unit file, both steps`) splits into
  a stray key; distil reported it clearly (`unknown key(s) ['both steps']`). Not a bug, but worth a
  line in the author brief.
- At 390 the hero scenery shows only the substation, interconnector and offshore turbines (onshore
  turbines are cropped by the template's responsive scene). Not clipped mid-drawing; template
  behaviour.

## Defects

- **gridflow, silent failure (same class as BACKLOG 20i): truncated datastore dump admitted as a
  complete capture.** The 2026-10-08 capture of `da_wind_forecast_historic_day_ahead_bmu` resource
  `81413643-508e-4358-8414-c87e7c4bcc43` (labelled 2025) holds exactly 3,136,000 rows and stops part
  way through 2025-11-07T22:00Z (38 of 210 units; every other period has 209 to 211). The 2026-10-16
  recapture keeps all 3,136,000 rows unchanged and runs to 2025-12-31T23:30Z (3,683,474 rows, 365
  labels). Sidecar `declared_content_length: null` and CKAN `metadata_modified` unchanged
  (2026-07-20T09:09:48), so nothing at capture time flagged it. `_latest` is now right (per-resource
  newest capture), but the K-GEN-1 FACTS figures (3,136,000 rows, 311 labels, "is 2025 still appended
  to?") rest on the short body. The 20i sweep as written ("captures since 2026-10-15 with falling row
  counts") would not find this one: the short capture came first and the next count rose. Suggest the
  sweep compare every dump capture's row count with the datastore `total`. (Note body corrected.)
- **NESO, historic national wind archive (vendor/data):** the 384 rows appended between 2026-10-08
  and 2026-10-16 are labelled `<target day>T08:45:00`, a day after the forecast was published: the
  9 October values equal the current file published 2026-10-08 08:40 (read as UTC), yet carry
  `2026-10-09T08:45:00`. For these rows the label is the archive's append time, not the forecast
  time, so a backtest that trusts `Forecast_Timestamp` would see each forecast a day late and after
  its target day began. Bears on the existing hold question; no gridflow change.
- **NESO, dictionaries (vendor, already in the note):** the current national dictionary leaves
  `Incentive_forecast`'s description blank and describes `Capacity` as the windfarm's; the current
  BMU dictionary calls `Generator_Name` "Anonymised" though the names are BM unit IDs. For the NESO
  question packet if not there.
- No other gridflow code defect found.
