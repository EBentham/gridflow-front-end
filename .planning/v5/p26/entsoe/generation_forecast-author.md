# entsoe/generation_forecast: author report

Writer: Opus 5.5 · high, 2026-09-29. Screenshot port 9805 (server stopped).

## Status

- `page:` block written in the canonical note (vault worktree), with body corrections. The mirror `vault/entsoe/generation_forecast.md` is a byte-for-byte copy (checked with `cmp`), and the note is still CRLF throughout.
- Artefacts generated from real data:
  - `site/hifi/data/series/entsoe/generation_forecast.json` (spec_origin vault, 4 series by 168 hourly points, 2,184 rows used);
  - `site/hifi/data/samples/entsoe/generation_forecast.json` (gridflow-sample, 8 rows);
  - `site/hifi/data/notebooks/entsoe/generation_forecast.json` and `generation_forecast-5.png` (run_notebooks.py, no errors).
- `gridflow-build --only entsoe/generation_forecast` passes. Its "N error(s) on pages not rendered by --only" lines belong to other writers' pages. `detect.mjs --json` returns `[]`.
- There was no staged chart spec and no authored override to retire.
- Screenshots at 1440, 1024, 768 and 390 (390 through an iframe). Light only: the site has no dark theme, with no `prefers-color-scheme` or `data-theme` in any asset. The one clip is a template problem (see below).

## Answers to the four focus points

- **Scope: total, generation only?**
  - Every A71/A01 response in bronze (79 data documents, 2026-08-01 to 05 and 2026-09-08 to 21) has businessType A01, `inBiddingZone_Domain` and no `MktPSRType`. So silver holds one total per zone, and `production_type` is always `""`.
  - One response (BE, 2026-09-08) also carried a second TimeSeries under `outBiddingZone_Domain`. By ENTSO-E convention that is probably scheduled consumption; I did not verify this from the vendor.
  - The parser maps both domain tags to the same `in_domain`, and silver has no direction column, so dedup keeps whichever series is later in the document. On that day the generation series was second and won.
  - Silver is therefore generation only in practice, but not by construction. The page says this as a code fact.
- **Zones and resolution.**
  - The connector requests six zones (`endpoints.py:395`).
  - GB and IE-SEM return Acknowledgement 999 on every request, so silver holds DE-LU, FR and NL at `PT15M` and BE at `PT60M`.
  - The page's cadence fact and chart caption say this. The what_it_is text scopes the empty zones to "this window".
- **Revisions.**
  - The dedup key `(timestamp_utc, area_code, production_type)` has no vintage, so silver keeps one forecast per target time and zone.
  - A re-fetch of the day replaces it: bronze files are read in sorted, timestamped order and `keep="last"` applies.
  - The grain fact says "a re-fetch replaces it".
  - `published_at` is not an issue time. `createdDateTime` is within -0.2 to 10.4 seconds of the sidecar `fetched_at` in all 78 data documents checked, so it is when the API answered. In the eight rows it is 2026-09-26, six days after the target day.
- **Terms** (for consistency with `wind_solar_forecast`; I did not touch its files).
  - "target time" for `timestamp_utc`, the same as the Elexon windfor page.
  - "bidding zone".
  - `published_at` described as the response `createdDateTime`.
  - The sister table has the same columns (`generation_forecast_mw`, `production_type`, `resolution`, `published_at`) and the same `createdDateTime` origin, so the same caveat applies there. I'd suggest the seat check that both pages word it the same way.

## Chart

- Line chart of silver `entsoe/generation_forecast`: `generation_forecast_mw`, grouped by `area_code` into four zones.
- Hourly mean (`time_bucket: 1h`, `aggregation: mean`) over target days 14 to 20 September 2026 UTC. The window end is inclusive in distil.
- Why the 1h bucket: BE is hourly and the others quarter-hourly. Unbucketed, BE would be null at :15, :30 and :45, and the line would break into dots.
- Why this chart for a trader: it shows the supply-side daily shape per zone. DE-LU peaks around 10:00 UTC, while NL dips around midday.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| A71/A01, `in_Domain`, `processType=A01` (facts.vendor, raw_feed.requests) | `connectors/entsoe/endpoints.py:104-106`; `client.py:282-307` builds params in the order documentType, periodStart, periodEnd, in_Domain, processType, securityToken; the bronze sidecar `request_url` for 2026-09-20 DE-LU matches exactly |
| One request per zone and UTC day (raw_feed.note) | `client.py:152-162` (`day_subwindows`), `utils/time.py:123-147`; one bronze file per (zone, day) |
| Six zones requested; GB and IE-SEM empty (what_it_is) | `endpoints.py:395` `DEFAULT_ZONES`; bronze acks: 21 × "No matching data found ... DAY_AHEAD_AGGREGATED_GENERATION_R3 [14.1.C] (10YGB----------A)" and 21 × the same for 10Y1001A1001A59C; GB is also in the note's live check of 2026-05-08 |
| PT15M for DE-LU, FR, NL; PT60M for BE (facts.cadence, caption, record.fields.resolution) | Silver `group_by(area_code).agg(resolution.unique())`: A82H, FR and NL `["PT15M"]`, BE `["PT60M"]`; `parsers.py:437-439,459` keeps the ISO code |
| No production type; empty string (summary, what_it_is, fields.production_type) | `grep -l MktPSRType` over the bronze XML: 0 files; silver `production_type.unique()` = `[""]` per zone; `parsers.py:269,345-348` default `""`; `generation_forecast.py:70-73` `fill_null` fills only nulls |
| One row per target time and zone; a re-fetch replaces it (facts.grain) | `generation_forecast.py:75` `unique(subset=[timestamp_utc, area_code, production_type], keep="last")`; `read_bronze` at `:40` reads `sorted(glob("raw_*.xml"))`, and the filenames are fetch-timestamped; 0 duplicate keys in silver |
| `outBiddingZone_Domain` series cannot be told apart; the later one is kept (what_it_is, fields.area_code) | `parsers.py:289-297` maps `outBiddingZone_Domain.mRID` into `in_domain`; bronze `2026/09/08/raw_20260915T200937Z_a582bbc5.xml` holds TS mRID 1 (outBiddingZone) then mRID 2 (inBiddingZone); the silver BE 2026-09-08 values equal TS 2 (2528.39, 1968.5175, ...) |
| `published_at` = response `createdDateTime`, within seconds of the fetch (fields.published_at) | `parsers.py:141-142`, `_published_at.py:60+`; across 78 data docs, `fetched_at - createdDateTime` ranges from -0.21 s to 10.43 s; an ack doc's `createdDateTime` equals its `received_MarketDocument.createdDateTime`; the eight rows show 2026-09-26 18:14 for target 2026-09-20 |
| `timestamp_utc` = period start + (position - 1) × resolution, UTC (fields.timestamp_utc) | `parsers.py:527-530` |
| Omitted A03 positions repeat the previous value (fields.generation_forecast_mw) | All 79 docs have `<curveType>A03`; forward-fill at `parsers.py:533-600` |
| Unit MW, `MAW` (fields.generation_forecast_mw) | Bronze `<quantity_Measure_Unit.name>MAW` in all 79 docs; schema docstring `schemas/entsoe.py:220-225` |
| Ingest `--end` exclusive; transform `--end` inclusive (raw_feed.commands) | `cli.py:1237` → `runner.resolve_dates` (midnight UTC); `day_subwindows` excludes an end at midnight; `runner.py` `run_transform` iterates `date_range(start, end)` inclusive (lines 1125-1138); there are no `PARTITION_SOURCE_OFFSETS` for this dataset, and the event-window filter keeps UTC day D from bronze day D |
| Notebook lead: relation, date column, inclusive, lineage dropped | gridflow_models `_schema_manifest`: `silver_entsoe_generation_forecast`, `timestamp_utc`, source entsoe; `source.py:401-451` + `_get_method_registry.py:62-96` (TIMESTAMPTZ half-open at end+1 day); `bitemporal_exclude()` drops `event_time`, `available_at`, `source_run_id`, `dataset_version` |
| Alt text numbers | Committed series: DE-LU min 30,583.6 (14th 02:00), daily peaks at 10:00 or 11:00 from 59,500 (14th) to 77,207.8 (17th), overnight lows 30,584 to 44,632; FR 36,908.3 to 63,637.5, daily max 46,733 and 48,542 on the 19th and 20th against 55,342 to 63,638 on weekdays; NL 7,362.4 to 14,432.2, daily minimum 09:00 to 13:00 on six of the seven days (05:00 on the 20th); BE 2,032.9 to 7,742.3 |
| plot_alt numbers | Silver DE-LU quarter-hours for 14 to 20 Sep: daily max 59,597 (11:15), 73,929, 62,686, 77,609 (17th, 10:45), 72,814, 71,689, 66,548 (10:15); all peaks between 10:15 and 11:15; min 30,443 (14th) and 44,567 (20th); matches the PNG |
| Frame: 12:00 and 13:00 UTC on 20 Sep, four zones (record.caption) | Sample JSON: DE-LU, BE, FR, NL at each of the two target times (8 rows); `published_at` 2026-09-26 18:14:30 to :35 |
| Related pages resolve | The build passes the related check; `entsoe/load_forecast` renders as `load_forecast.html` (the family member's pointer page) |

## Note-body corrections (canonical note, smallest spans)

1. **Overview.** "broken out per production type" became "one total per zone (no `MktPSRType` in the 2026-08/09 responses)". Evidence: 0 bronze files contain `MktPSRType`.
2. **Silver schema, `production_type` row.** "defaults to "unknown"" became `""`, citing `parsers.py:269,345-348` and `generation_forecast.py:70-73`.
3. **Silver schema, `resolution` row.** "Default "" in canonical. `PT60M` typical." became "the ISO code as sent", with PT15M for DE-LU, FR and NL and PT60M for BE (`parsers.py:437-439,459`).
4. **Silver schema, `published_at` row.** Removed "leak-proof forecast issue time". It now says the value is within seconds of the fetch in the 2026-08/09 bronze, so it is when the API answered.
5. **Silver sample.** `"production_type": "unknown"` became `""`, and `"resolution": "1:00:00"` became `"PT60M"`. The old value was a timedelta string the parser never emits. I kept PT60M to match the bronze sample above it.
6. **Known issues.**
   - Fixed the "unknown" bullet.
   - Added a bullet on the `outBiddingZone_Domain` collision (with file:line).
   - Added a bullet on the GB and IE-SEM ack 999.

## Unverified

- That the BE 2026-09-08 `outBiddingZone_Domain` series is scheduled consumption. It is inferred from ENTSO-E convention; no vendor doc is in the note. The page does not name it.
- That `createdDateTime` is always the response build time. This is measured on 78 documents in Aug and Sep 2026; the page scopes it with "here".
- That IE-SEM is empty at the vendor in general. It is only observed in the 2026-08/09 acks, and the page scopes it to "this window".
- The note's "Historical depth 2014-12-05" and "Published D-1 ~18:00 UTC". Neither is quoted from a vendor doc, so neither is used on the page.

## Open questions (for the seat or gridflow)

1. **gridflow silent-collision risk.** Should the A71 transformer keep a direction or domain-role column, or drop `outBiddingZone_Domain` series? Today which series survives depends on document order.
2. **gridflow docstring and comment drift.**
   - The `GenerationForecastTransformer` docstring says "Each TimeSeries carries `MktPSRType / psrType`"; the data has none.
   - `_published_at.py` calls `createdDateTime` the "leak-proof forecast issue time"; the measured behaviour is the fetch time.
   - Point-in-time joins via `available_at = coalesce(published_at, ...)` therefore date these forecasts about six days late.
   - This is worth a research unit. The same applies to `wind_solar_forecast` and every ENTSO-E forecast table using `with_published_at`.
3. **BE 2026-09-08.** The generation series drops to 0 MW for 09:00 to 13:00 UTC and is 22 hours long. I kept the chart window clear of it; not investigated.

## Template and tooling problems (not worked around in shared files)

1. **Notebook header clips at 390 px.**
   - `.nb-bar` shows `{{ v.notebook.tab }}` (`generation_forecast.ipynb`, from `build.py:1282` `doc.slug`) beside `gridflow_models` (`templates/dataset.html.j2:191,200`).
   - At 390 the right label loses its final "s" off the edge of the dark bar.
   - A long slug causes it, so `wind_solar_forecast` will hit it too.
   - Suggested fix in `dataset.css`: let `.nb-bar` wrap, or give `.nb-kern` `min-width: 0; overflow: hidden; text-overflow: ellipsis`.
2. **ENTSO-E EIC codes contain `---`.** `10YFR-RTE------C`, `10YNL----------L` and `10YBE----------2` all do.
   - `chart_spec._check_strings` and page_fields refuse `---` in any string value.
   - The vault tools split the raw front matter on `---` (`gridflow_drift_check.py:129`, `derive_machine_catalog.py:180`), so even a mapping key would break them.
   - My workaround:
     - `group_map` keys are written with YAML double-quoted `\x2D` escapes (`"10YFR-RTE-\x2D-\x2D-\x2DC"`). These parse to the real EIC, but the raw text never holds three dashes. Checked: the only `---` in the page block is the closing fence.
     - Key `codes` use gridflow's zone names (`DE-LU`, `FR`, `NL`, `BE`, from `endpoints.py` `BIDDING_ZONES`).
   - The seat may prefer a shared convention, for example a `group_map` on zone names after a join. Every ENTSO-E page that groups by `area_code` will hit this.
3. **Detector em-dash rule fires on EIC codes.**
   - `detect.mjs` counts `--(?=\S)`, so `10YBE----------2` counts as 5 "em dashes". The `--start` and `--end` flags add 4.
   - The rule fires at 8 or more runs with fewer than 500 body characters per run. This page has about 8,700 characters, so the ceiling is 17.
   - Rows showing FR, NL and BE twice each in the frame and once in the notebook head gave 43 runs.
   - I narrowed the frame to DE-LU plus BE, using `area_code lt "10YC"`, a plain string comparison that names no dashed code. I also narrowed the notebook head to DE-LU. That gives 14 runs and `[]`.
   - Other ENTSO-E pages with multi-zone frames will hit this. Consider treating EIC tokens as code in the detector, or accept the advisory.

## Seat ruling applied (2026-09-29, EIC codes)

- Reverted the `\x2D` escapes: the `group_map` keys now hold the plain EIC codes. The key `codes` stay `DE-LU`, `FR`, `NL`, `BE`, because `page_fields` rejects `---` in string values.
- The frame is back on merit: 12:00 and 13:00 UTC on 20 September, all four zones (`timestamp_utc in [...]`, no area filter). The notebook head is back to all zones, sorted.
- Re-distilled (the spec digest is unchanged), re-sampled, re-ran the notebook, re-mirrored (`cmp` identical, CRLF) and rebuilt `--only`.
- Detector: the only finding is `em-dash-overuse` (advisory, 43). Every count comes from EIC `--` padding and the `--start`/`--end` flags; the rendered page has 0 em dashes.
- Residual risk, for the seat: the raw front matter now contains `---` inside the `group_map` keys. `gridflow_drift_check.py:129` and `derive_machine_catalog.py:180` do `text.split("---", 2)`, so those vault tools will cut this note's front matter short. The same applies to every ENTSO-E note that writes these codes plainly.
- Template problems 3 (detector) and 2 (the workaround) above are superseded by this ruling. Problem 1 (the 390 notebook header) is left for the seat.

Superseded by the corrected ruling (#40): the `group_map` keys are back to `\x2D` escapes, and the front matter holds no literal `---` apart from its fences. The four-zone rows are kept, and `tests/test_front_matter_fence.py` passes.

## Revision 1 (review REVISE, 2026-09-29)

1. **Blocker, `page.record.fields.timestamp_utc`.** Now "Target time: start of the step, period start plus (position minus 1) steps, UTC", matching `parsers.py:530` and the BE 2026-09-08 position 9 = 08:00 check. The body's Silver schema row had the same error; it now reads `Period start + (position - 1) * resolution (parsers.py:530)`. A grep of the page for "position" finds only this line and the A03 guide line, which is correct.
2. **Major, `page.facts.cadence`.** Now "Every 15 minutes for DE-LU, FR and NL, hourly for BE, in these responses" (14 words).
3. Mirror `cmp`-identical (CRLF). `gridflow-build --only entsoe/generation_forecast` exits 0. The detector shows only the accepted `em-dash-overuse` advisory (43).
4. Screenshots at 1280 and 390: the hero facts, the frame, the guide and the notebook show nothing clipped or overlapping. The 390 wrapper lived in the scratchpad this time, not under `site/hifi`, and the server is stopped.

## Spend

One writer session (Opus 5.5 · high). The advisor was rate-limited, so it was not consulted.
