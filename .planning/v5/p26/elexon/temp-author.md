# elexon/temp: author report

Writer: Opus 5.5, 2026-09-28. Page: `site/hifi/data-sources/elexon/temp.html` (front-end worktree `p26-elexon`).

## Status

- Canonical note: `vault-p26-elexon/30-vendors/elexon/datasets/temp.md` (page block added, body corrected). Mirror
  `p26-elexon/vault/elexon/temp.md` is byte-identical (`cmp` clean).
- No staged spec or authored override existed for temp (nothing to delete).
- Artefacts: `site/hifi/data/series/elexon/temp.json` (`spec_origin: vault`, 1 series x 9 points),
  `samples/elexon/temp.json` (`gridflow-sample`, 8 rows x 9 columns), `notebooks/elexon/temp.json` + `temp-5.png`
  (`run_notebooks.py`, 5 cells, no errors).
- `gridflow-build --only elexon/temp`: succeeds. `detect.mjs --json`: `[]`.
- Chart: `line`, `temperature` against `measurement_date` (a Date axis), measurement dates 13 to 21 September 2026,
  one point per date (dedup on `measurement_date` by `timestamp_utc`, `last`; 0 duplicates dropped in this window).
- Landscape: not set; Elexon pages default to `power` (`build.py:1374`). None of power/market/gas/units fits a
  temperature reading exactly.

## Evidence

| Claim (field) | Evidence |
|---|---|
| Endpoint `/datasets/TEMP`, `PUBLISH_DATETIME` style (`raw_feed.requests`) | `gridflow/connectors/elexon/endpoints.py:157-160` |
| Request params `publishDateTimeFrom`/`To` formatted `%Y-%m-%dT%H:%M:%SZ`, plus `page` | `endpoints.py:267-277` (`_to_utc_z`), `endpoints.py:300-313` (`build_params`); bronze sidecar `bronze/elexon/temp/2026/09/14/*.meta.json` `request_url` matches the page's URL exactly |
| 24-hour publish windows; ingest `--end` is exclusive | `client.py:93-98` (`chunk_delta = max_chunk_hours` default 24, `while current < end`); `endpoints.py:39` default 24 |
| Transform `--end` inclusive; one silver file per bronze date; no source offsets | brief; `silver/base.py:417` `PARTITION_SOURCE_OFFSETS = (0,)`; `base.py:2633-2654` filename per `target_date`; `temp.py:27-35` reads only `bronze/<target_date>` |
| `timestamp_utc` is the vendor `publishTime` (`record.fields`, `facts.grain`, `what_it_is`) | `temp.py:58-59` rename, `temp.py:80-84` parse; fallback to `measurement_date` only if no publish field (`temp.py:70-74`) |
| Key `timestamp_utc` (`record.key`) | `temp.py:25` `ENTITY_KEY_COLUMNS = ("timestamp_utc",)`, `temp.py:96` `unique(subset=["timestamp_utc"], keep="last")` |
| `measurement_date` from `measurementDate`, cast to Date | `temp.py:60`, `temp.py:93-94` |
| The response sends only `dataset`, `measurementDate`, `publishTime`, `temperature`; no unit field; no `normal`/`low`/`high` | bronze `2026/09/14/raw_*.json` body; note's own bronze sample (captured 2026-05-08); silver schema has no `normal_temperature`/`low_temperature`/`high_temperature` columns |
| °C | gridflow `docs/endpoints/elexon.md:761` ("Temperatures in °C"); stated on the page as "gridflow's docs give °C", with "the feed sends no unit" |
| 13 September's reading was published on the 14th at 09:06 UTC (`chart_view.key[0].note`, `what_it_is`, `raw_feed.note`, `record.caption`) | visible in the eight rows (row 1: `2026-09-14 09:06:00 UTC`, `2026-09-13`, 17.7); bronze `2026/09/14` holds it, bronze `2026/09/13` is `{"data":[]}` |
| "One reading per measurement date" (`facts.cadence`, `summary`, "daily") | resolution, not a publication schedule: `measurement_date: date` in `ElexonTemp` (`schemas/elexon.py:861`); the page never says Elexon publishes once a day (the 13 Sep publish window was empty and the 14th's carried two readings) |
| "most shown published at 15:45 UTC" (`facts.cadence`) | 7 of the 8 rows shown have publish time 15:45 UTC |
| `ingested_at` is silver transform time (body fix) | `temp.py:98-103` `datetime.now(UTC)` |
| `query()` reads `silver_elexon_temp`, filters on `timestamp_utc`, both end dates included, lineage dropped (`notebook.lead`) | gridflow `silver/schema_manifest.py:140` `("elexon","temp"): "timestamp_utc"`; temp not APPEND_ONLY (`base.py:711` default) so no `_latest` view (`schema_manifest.py:18-65`); `gridflow_models/research/handles/_get_method_registry.py:94-96` TIMESTAMPTZ half-open `[start 00:00Z, end+1 00:00Z)`; `source.py:440-451` EXCLUDE bitemporal, `ORDER BY` date col |
| "14 to 21 September brings readings for 13 to 21" (`notebook.lead`) | notebook plot shows 9 points, measurement dates 13 to 21; head output row 1 `2026-09-14 09:06:00+00:00`, `2026-09-13`, 17.7 |
| Chart values in `alt` and `plot_alt` (17.7, 18.6, 18.3, 16.0, 17.1, 16.0) | committed series `x` 2026-09-13..21, `values` [17.7, 18.6, 18.3, 16.9, 16.6, 16.0, 17.1, 16.6, 16.0]; PNG `temp-5.png` checked by eye |
| Related: Open-Meteo demand feeds are 2 m temperature at seven UK cities (ERA5 reanalysis / forecast) | `vault/openmeteo/historical_demand.md:13-15,148`; `forecast_demand.md:13-14`. "UK", not "GB": the list includes Belfast |
| Related pages resolve | build passes (it fails on an unresolvable related dataset); `elexon/ndf` resolves to the `demand-forecasts` family, the Open-Meteo members to `demand-weather` |

## Note-body corrections (canonical note)

1. Overview: removed the claim that the dataset publishes seasonal-normal, low and high reference values; now says
   the `/datasets/TEMP` response carries only `dataset`, `measurementDate`, `publishTime`, `temperature` (bronze
   sample in the note).
2. Silver layer, Point-in-time field: was "`ingested_at` (no native PIT field)"; now `timestamp_utc`, the vendor
   `publishTime` (`temp.py:58-59`).
3. Silver schema, `timestamp_utc` notes: was "Derived from (settlement_date, settlement_period) via
   `settlement_period_to_utc`" (wrong); now the publish instant parsed as `%Y-%m-%dT%H:%M:%SZ`, fallback, and the
   dedup consequence (`temp.py:58-59,70-74,80-84`).
4. Silver schema, `normal_temperature`/`low_temperature`/`high_temperature` notes: appended that the response does
   not carry them and they are written only if bronze does (`temp.py:62-64,86-88,116`). Rows kept: the schema and
   transformer still declare them.
5. Silver schema, `ingested_at`: was "Time ingested into bronze"; now silver transform time (`temp.py:98-103`).
6. Silver sample: replaced the three `"..."` normal/low/high keys with `measurement_date` (the columns silver
   actually writes).
7. Known issues, "Daily resolution": now says the row key is the publish time and records the 13 September late
   publication (bronze `2026/09/14`; the 13th's window returned `{"data":[]}`).

## Not verified

- What the reading represents (a GB average, which stations, what weighting) and whether it is a daily mean. Elexon's
  documentation pages (`bmrs.elexon.co.uk/api-documentation/endpoint/datasets/TEMP`, the BSC BMRS data catalogue)
  render only with JavaScript; WebFetch returned no content. The page therefore says only "Elexon's temperature data
  (TEMP)" and "daily temperature reading", never "GB average".
- The unit as a vendor fact: the page attributes °C to gridflow's docs and says the feed sends no unit.
- Vendor history depth (the note says "Several years" without a source): no `facts.history`.
- Why the 13 September reading came the next morning, and whether Elexon ever republishes a measurement date. The
  page states only what the rows show; the chart spec's dedup would keep the later publication if one existed.
- The body's line "Reference temperatures (normal/low/high) are seasonal climatology, not forecasts" and the
  Overview's "used by NESO in demand-forecasting calibration" are unsourced; left untouched (not on the page).

## Open questions

- gridflow `docs/endpoints/elexon.md:748-761` still claims normal/low/high columns and "forecast bounds": that is a
  gridflow docs fix, not a front-end one.
- `_publication_window.py:43-47` lists temp as exempt because it "collapses the publication dimension"; the page
  follows the code as it stands (publish time is the key).

## Screenshots (1440, 1024, 768, 390)

- 1440, 1024, 768: headless Chrome full-page captures, cut into segments and read. Hero scenery (turbine tops,
  offshore wind label), chart, key note, raw-feed blocks, frame, guide, notebook panel, stratum corner labels and
  related list all fully visible; nothing overlaps.
- 390: headless Chrome's minimum window lays out wider than 390, so the direct capture clipped on the right (a tool
  artefact). Re-captured via a 390 px iframe: everything wraps and is fully visible. In the Browser pane at a true
  390 viewport, `scrollWidth` equals 390 and no element in `body` (outside the scroll regions) extends past the edge.
- Frame folded and unfolded (the `#fx` toggle), measured in the pane at 1440 and 390: no header overlaps, no clipped
  cells, the unfolded columns scroll inside the frame region and the page itself does not overflow.
- Dark mode: the site has no dark theme (no `prefers-color-scheme` or dark rules in `site/hifi/assets/*.css` or
  `site.js`), so light is the only rendering.

## Template problems (reported, not worked around)

1. The line chart's y-axis always included 0 for all-positive data, squeezing 16.0 to 18.6 into the top fifth.
   **Resolved** by the coordinator's fix (commit a0e18d9, `chart_svg.py:397-399`: a line far from zero is drawn to
   its own range). Rebuilt 2026-09-28 with `--only elexon/temp`: build green, detector `[]`, mirror re-copied and
   byte-identical; the wide and narrow SVGs' y ticks now read 15, 16, 17, 18, 19. `chart_view.caption` and `alt`
   never mentioned zero or the range, so they are unchanged.

## Revision 1 (answers `temp-review.md`)

Elexon's own description was read verbatim: the TEMP docs page renders in a real browser (the Browser pane,
JavaScript on), a documentation page, not a data API call. Text as shown at
https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/TEMP on 2026-09-28:

> "This endpoint provides the average degree celsius value measured at midday deemed to be representative of the
> temperature for Great Britain. Data is gathered from 6 weather stations. Default output will be the last 31 days.
> Values are received from 5pm each day."

The same page's response schema lists `dataset`, `measurementDate`, `publishTime`, `temperature` and no unit field.
Note that Elexon's wording is **not** "daily average" (the checker's search-summary text): it is a six-station average
of a value measured at midday. The page follows Elexon's words.

1. **major, °C from gridflow's docs.** Fixed. The quote and URL are in the note body (Overview). "gridflow's docs" is
   gone from `what_it_is`, `chart_view.caption` and `record.fields.temperature` (0 hits in the rendered page).
   - `what_it_is`: "the average °C value measured at midday for Great Britain, gathered from six weather stations ...
     the response has no unit field".
   - `caption`: "°C (Elexon's unit)".
   - `record.fields.temperature`: "Elexon's six-station average, °C, measured at midday; the response sends no unit".
   - The chart unit, notebook `ylabel` and `plot_alt` keep °C, now a vendor fact.
2. **major, "one reading per measurement date".** Fixed. Every per-date universal is removed.
   - `summary`: "Elexon's midday temperature for Great Britain, averaged over six weather stations, with the date it
     is for and its publish time."
   - `facts.cadence`: "Measured at midday, per Elexon; most shown published at 15:45 UTC" (the 15:45 part is scoped to
     the rows shown).
   - `what_it_is`: "Each row carries the date it is for and its publish time".
   - `caption`: "one point per measurement date", which describes the chart and holds by the spec's dedup; "the latest
     publication of each" is kept.
   - `facts.grain` is unchanged ("One row per publish time, each carrying its measurement date"), from the code key.
   - `how_used` keeps "a daily temperature feature" and "each measurement date's reading". Both describe use, not a
     rule about the data.
3. **nit, wrong cause in `what_it_is`.** Fixed: "gridflow fetches and dates each row by its publish time, so 13
   September's reading, published the next morning, arrives with the 14th."
4. **nit, hero scenery alt says "generation data" (seat).** No writer change. `landscape` stays unset because no
   option fits a weather reading. This is for the seat.
5. **nit, Open-Meteo related notes.** Fixed; both notes now say how the datasets relate.
   - `openmeteo/historical_demand`: "City-level hourly temperature to set against this six-station GB value".
   - `openmeteo/forecast_demand`: "City-level temperature forecasts, available before this GB value is published".

Checks after revision:
- The canonical note stays CRLF throughout (260 LF, 260 CR). The mirror was re-copied and is byte-identical (`cmp`).
- `gridflow-build --only elexon/temp` succeeds. `detect.mjs --json` returns `[]`.
- The chart, frame and notebook artefacts are unchanged: no spec, select or cell edits, and the build's digest checks
  pass.

Not stated on the page, for the record:
- Elexon says "Values are received from 5pm each day". The rows show publish times of 15:45 UTC (16:45 BST) and one
  at 09:06 UTC. The page makes no claim about Elexon's publication schedule.

## Revision 2 (the `temp-review-2.md` nit)

- `how_used[1]`: was "Heating and cooling degree days, from each measurement date's reading". Now "Proxy degree days:
  this midday reading stands in for the usual daily mean.", because degree days normally use a daily mean and Elexon
  describes a midday value. Mirror re-copied (byte-identical, still CRLF). `--only elexon/temp` built; detector `[]`.
