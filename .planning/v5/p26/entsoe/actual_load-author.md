# entsoe/actual_load: author report

Writer: Opus 5.5 · high, 2026-09-29. The page is `entsoe/actual_load` ("Actual total load by zone").

## Status

- **Canonical note:** `vault-p26-entsoe/30-vendors/entsoe/datasets/actual_load.md`.
  - It has the `page:` block and five body corrections.
  - It keeps CRLF (292 of 292 lines).
  - The mirror `p26-entsoe/vault/entsoe/actual_load.md` is byte-identical (`cmp` clean).
- **Artefacts:** all three were written by the tools, from real data.
  - `site/hifi/data/series/entsoe/actual_load.json`: `gridflow-distil`, `spec_origin: vault`.
  - `site/hifi/data/samples/entsoe/actual_load.json`: `gridflow-sample`.
  - `site/hifi/data/notebooks/entsoe/actual_load.json` and `actual_load-5.png`: `scripts/run_notebooks.py`, 5 cells, no errors.
  - No staged chart spec or authored override existed, so there was nothing to delete.
- **Build and detector:**
  - `gridflow-build --only entsoe/actual_load` succeeds. Its "5 error(s) on pages not rendered by --only" belong to other authors' pages.
  - `detect.mjs --json` returns one advisory finding, `em-dash-overuse` ("43 em-dashes in body text"). All 43 counts are 39 runs of `--` padding inside the FR, NL and BE EIC codes (frame and notebook head) and the four CLI flags `--start`/`--end`. None is in prose.
  - Seat ruling 1 accepts this finding.
- **Seat rulings applied (2026-09-29):**
  1. The EIC codes are written plainly. The frame is back to all four zones at 11:00 and 11:15 UTC on 15 Sep. The notebook head is back to `df[[...]].head()` over all zones. I had first picked DE-LU-only rows to get the detector to `[]`; that is now reverted.
  2. The `published_at` guide line reads "Fetch-time stamp: the response's `createdDateTime`, within seconds of the request".
- **Screenshots:**
  - Widths 1440, 1024 and 768 in headless Chrome; 390 by CDP emulation and by a 390 px iframe.
  - The frame was checked folded and unfolded, and the notebook drawer open.
  - There is no horizontal overflow (scrollWidth equals innerWidth at every width). Nothing is clipped or overlapping in the hero scenery, chart, key note, frame, guide, notebook or stratum labels.
  - The site has no dark scheme: no `prefers-color-scheme` rule in `tokens.css` or `theme.css`, and no toggle. So only the one theme was checked.
- **Chart:** a `line` of DE-LU (`10Y1001A1001A82H`) total load in MW, every 15-minute value, UTC days 14 to 20 September 2026 (Monday to Sunday; 672 points).

## Evidence

| Claim (page field) | Evidence |
|---|---|
| Document A65, process A16, requested with `outBiddingZone_Domain` (facts.vendor, raw_feed.requests) | gridflow `connectors/entsoe/endpoints.py:31-33` (`EntsoeDocType("A65","A16",...,domain_style="out_bidding_zone")`); `client.py:558-559` maps that to `outBiddingZone_Domain` |
| Article 6.1.A (facts.vendor, what_it_is) | The note's Overview says `ACTUAL_TOTAL_LOAD_R3`, Article 6.1.A. The vendor's 999 text in bronze reads "Data item ACTUAL_TOTAL_LOAD_R3 [6.1.A]" |
| Request URL and parameter order (raw_feed.requests) | `client.py:_fetch_document` builds `documentType`, `periodStart`, `periodEnd`, domain, `processType`, `securityToken`. A bronze sidecar confirms it: `2026/09/14/raw_20260921T100146Z_*.meta.json` has `request_url` `...api?documentType=A65&periodStart=202609140000&periodEnd=202609150000&outBiddingZone_Domain=10Y1001A1001A82H&processType=A16&securityToken=<redacted>` |
| `periodStart` / `periodEnd` format `yyyyMMddHHmm` | `endpoints.py:403` `ENTSOE_DT_FORMAT = "%Y%m%d%H%M"` |
| One call per zone and UTC day (what_it_is, raw_feed.note) | `client.py:162` `day_subwindows(start, end)`, and the task loop over `DEFAULT_ZONES` at `client.py:249`; `utils/time.py:123` gives clamped UTC calendar days with an exclusive end |
| gridflow asks for six zones (what_it_is) | `endpoints.py:395` `DEFAULT_ZONES = ["GB","FR","NL","BE","DE-LU","IE-SEM"]`; no override in `config/sources.yaml` |
| GB gets code 999 (what_it_is, related `elexon/indo` note) | The note's API section and Known issues ("GB returns Acknowledgement 999"). Bronze agrees: every GB file is an `Acknowledgement_MarketDocument` with `<code>999</code>` "No matching data found" (26 of 26) |
| IE-SEM gets code 999 "on the days charted" (what_it_is) | Bronze: IE-SEM `10Y1001A1001A59C` returned 999 in 26 of 26 files, and that includes every day from 14 to 20 Sep. The page scopes the claim to the days charted |
| Ingest end is exclusive; transform end is inclusive (raw_feed.commands) | `pipeline/runner.py:479-500`: a bare date is midnight UTC. `day_subwindows` excludes an end that falls at midnight. `run_transform` iterates `date_range(start.date(), end.date())`, inclusive (`runner.py:1126,1138`) |
| No widening of the ingest window | `silver/base.py:417` `PARTITION_SOURCE_OFFSETS = (0,)`, not overridden in `actual_load.py`. `EVENT_WINDOW_FILTER = True` (`actual_load.py:26`) keeps only rows in the partition's own `[periodStart, periodEnd)` |
| Grain and key (facts.grain, record.key) | `actual_load.py:65` `unique(subset=["timestamp_utc","area_code"], keep="last")` |
| `timestamp_utc` = period start plus (position − 1) × resolution (record.fields) | `parsers.py:530` and `582` |
| `area_code` = EIC as sent (record.fields) | `parsers.py:293-297` takes `outBiddingZone_Domain.mRID` into `in_domain`; `actual_load.py` renames it to `area_code` with no remap |
| `load_mw` = the point's `quantity`, unit `MAW` (record.fields) | `actual_load.py:40` `value_tag="quantity"`, rename at `:59`. Bronze has `<quantity_Measure_Unit.name>MAW</...>` |
| `resolution` as sent (record.fields, facts.cadence) | `parsers.py:437-438`; `PT15M` in every GL document for 14 to 20 Sep (probe of 28 documents) and in all four zones' rows shown |
| `published_at` is a fetch-time stamp, the response's `createdDateTime`, within seconds of the request (record.fields; seat ruling 2) | `actual_load.py:76` `with_published_at` reads document `<createdDateTime>` (`_published_at.py`). Across all 104 GL documents in bronze, `createdDateTime` minus sidecar `fetched_at` runs from −3.5 s to +0.1 s |
| Chart series: 672 points, 35,310.541 to 65,453.589 MW | Committed `series/entsoe/actual_load.json`: `rows_used` 672, `x` 2026-09-14T00:00Z to 2026-09-20T23:45Z |
| Alt: weekday lows 41 to 44 GW and peaks 63 to 65 GW, 06:45 to 08:45 UTC; weekend peaks 52 and 51 GW; Sunday 35 GW the week's low | Per-day min and max from the committed series: 14th 41,214 / 64,825 (08:45); 15th 44,106 / 64,154 (06:45); 16th 44,259 without the dip / 65,454 (08:15); 17th 43,637 / 63,314 (06:45); 18th 40,632 / 63,023 (07:45); 19th 37,304 / 52,363; 20th 35,311 / 50,910. The alt rounds the 18th's 40.6 to "41" |
| Key note: a one-interval drop to 39.4 GW at 23:15 UTC on the 16th, as sent | Series: 23:00 46,282.371; 23:15 39,435.413; 23:30 45,556.621. Bronze `2026/09/16/raw_20260921T100306Z_*.xml` position 94 is `39435.41266`, so this is the vendor's value, not a gridflow artefact. Positions 1 to 96 are all declared, so there is no forward-fill |
| No forward-fill in the charted week | All 28 GL documents from 14 to 20 Sep declare 96 `<Point>` elements (probe) |
| Frame: all four zones with rows, 11:00 and 11:15 UTC on 15 Sep (DE-LU 60,430.67916; BE 11,673.01; FR 49,653.39; NL 4,094.801 at 11:00) | Committed `samples/entsoe/actual_load.json` (`gridflow-sample`); NL at 11:00 is its lowest value of the charted week |
| Notebook lead: relation `silver_entsoe_actual_load`, filter on `timestamp_utc`, both ends included, lineage dropped, local-time printing | `_get_method_registry._relation_name_for_dataset("actual_load")` returns `silver_entsoe_actual_load`. gridflow `schema_manifest.py:149` gives the date column `timestamp_utc`. `source.py:401-445` builds an inclusive range predicate. `_BITEMPORAL_EXCLUDE` covers `event_time`, `available_at`, `vintage_policy`, `source_run_id`, `dataset_version`, `month` and `year`. The notebook head prints `2026-09-14 01:00:00+01:00` |
| plot_alt: DE-LU 35 to 65 GW, FR 31 to 51 GW, BE and NL 4 to 12 GW, NL lows near midday, about 4,100 MW on the 15th | Silver probe for 14 to 20 Sep: DE-LU 35,311 to 65,454; FR 31,368 to 50,605; BE 6,809 to 11,901; NL 4,095 (11:00 UTC on the 15th) to 11,972. NL's daily minima fall between 09:45 and 14:00 UTC. The PNG shows the same shapes |
| `related` pages resolve | The build's related check passes: `entsoe/load_forecast` (lead of `load-forecasts`), `entsoe/actual_generation`, `entsoe/day_ahead_prices` and `elexon/indo` (lead of `demand-outturn`) |
| `load_forecast`, `actual_generation` and `day_ahead_prices` requested "for the same zones" | All three loop over `DEFAULT_ZONES` (`client.py:249`) with their own domain style (`endpoints.py:30-45`) |

## Note-body corrections (canonical vault note)

1. **Bronze path pattern.** Was `raw_<uuid>.xml`. Now `raw_<YYYYMMDDTHHMMSSZ>_<hash>.xml` with a `.meta.json` sidecar. Evidence: `bronze/writer.py:57`, and the files on disk.
2. **Bronze granularity.** Was "One file per (zone, query window)". Now one file per (zone, UTC day), because the connector splits a window into calendar days. Evidence: `client.py:162`.
3. **Point-in-time field.** Was "none". Now `published_at` from the document `createdDateTime`. It fell within 4 s of the request in the 104 documents checked, so it is the response time, not the TSO's publish time. Evidence: `silver/entsoe/actual_load.py:76`, and the bronze probe.
4. **Silver schema table.**
   - Added the missing `published_at` row. Evidence: `actual_load.py:78-86` `output_cols`, and `schemas/entsoe.py:46`.
   - On the `timestamp_utc` row, noted that the responses are `curveType` A03 and that omitted positions are forward-filled. Evidence: `parsers.py:533-596`.
5. **Known issues.** Added one bullet: IE-SEM (`10Y1001A1001A59C`, in `DEFAULT_ZONES` at `endpoints.py:395`) returned 999 in all 26 bronze files on hand, dated 2026-08-01 to 2026-09-20.

I did not touch the curl example: it is valid for the vendor, and only the parameter order differs from the connector.

## Not verified

- **What ENTSO-E's "total load" includes** (network losses, pumped-storage consumption, auxiliary load). Neither the vault (note, `20-domain/concepts/`), the gridflow code nor the silver data quotes a vendor definition. The note links `20-domain/concepts/system-load.md`, but that file does not exist in the vault worktree. The page says only that this "is ENTSO-E's definition, not stated here".
- **Note body claims the page does not use:** "Publication lag ~1 hour", "Historical depth ~5 years", "Revisions within ~24 hours", and "Some smaller zones still publish PT60M". None of them has evidence; they are left in the body as they were.
- **Elexon comparison.** GB is not in the data (code 999), so the page makes no match or equivalence claim with `indo`. The note's Modelling notes still say Elexon `indo` is the "same physical signal". That is unverified, and the two definitions probably differ (INDO is transmission-level demand). I left the body line alone; see the open questions.
- **Cause of the 23:15 UTC dip on 16 Sep, and of NL's midday troughs.** Both are shown or described as sent, with no cause given.

## Open questions for the seat

1. **The NL outlier outside the window.** NL (`10YNL----------L`) has a 72.716 MW row at 2026-08-02 11:00 UTC, and 94 rows below 3,000 MW on 1 to 4 Aug and 6 to 7 Sep, all around midday. These are outside the charted week, so the page does not mention them. They look like a vendor-side data issue (or a load definition that nets off embedded solar) worth a research unit before anyone models NL load.
2. **The note's "same physical signal" line.** Should it be struck or labelled unverified in a separate vault-hygiene pass?
3. **The missing domain note.** `20-domain/concepts/system-load.md` is linked from the note but missing. It would be the natural home for a quoted vendor definition of total load (Regulation 543/2013).
4. **Gaps outside the window.** DE-LU has 72 of 96 rows on 2026-09-07, and NL has 95 of 96 on 2026-09-09. The page doesn't mention them; they are recorded here only.

## Template and tool problems (reported, not worked around in shared files)

1. **`---` inside EIC codes blocks per-zone charts.**
   - FR (`10YFR-RTE------C`), NL (`10YNL----------L`) and BE (`10YBE----------2`) contain `---`.
   - `chart_spec._check_strings` (`chart_spec.py:111-121`) and `page_fields` (`page_fields.py:379`, `:492`) reject `---` anywhere in a page string, chart value or notebook cell. So a `group_map` from EIC to zone label, a filter on those zones, or a key `codes` naming them cannot be written.
   - This is why the chart shows DE-LU alone (its EIC has no dashes) and the notebook plots all four zones.
   - The same limit will hit other ENTSO-E pages with per-zone series: `day_ahead_prices`, `actual_generation`, `cross_border_flows`, `load_forecast` and others.
   - Suggested fixes:
     - reject only a line that is exactly `---`, which is what actually breaks front-matter parsing; or
     - let the chart spec map zones through the connector's short names (`BIDDING_ZONES`).
2. **`detect.mjs` counts `--` inside EIC codes as em dashes.**
   - The regex `--(?=\S)` in `engines/regex/detect-text.mjs:314` fires on data.
   - Seat ruling 1 accepts the advisory finding, so the page prints the codes plainly and the detector reports 43.
   - A permanent fix would give every ENTSO-E page a true `[]`: skip `<code>`, `<pre>` and frame table cells in the em-dash analyser, or ignore runs of three or more hyphens.
3. **Minor.** The copied `shot.mjs` CDP script names its Chrome profile under `%TEMP%` by timestamp. I left the folder in place, as the rules say.

## Checker, look hardest at

- `what_it_is`: "GB, and IE-SEM on the days charted, get ... code 999". The IE-SEM half rests on bronze evidence scoped to the charted days, not on a vendor statement.
- `record.fields.published_at`: "within seconds of the request". This follows seat ruling 2 and the bronze measurement over 104 documents (−3.5 s to +0.1 s).
- The chart shows DE-LU while the title says "by zone". The build's `---` fence check forces this (template problem 1), and the notebook plot carries all four zones.
