# entsoe/day_ahead_prices: author report

Writer: Opus 5.5 (high), 2026-09-29. Worktrees are as the batch file gives them.

## Status

- **Build:** `uv run --system-certs --extra build gridflow-build --only entsoe/day_ahead_prices` succeeds. It passes the seat's new front-matter `---` check, and the cross-vendor `elexon/mid` related link resolves.
- **Detector:** one finding, the advisory `em-dash-overuse` ("30 em-dashes in body text"). All of it comes from the dash padding inside the EIC codes in the frame: FR 3, NL 5 and BE 5 `--` pairs, times two rows, is 26, plus the four CLI `--start`/`--end` flags. Seat ruling 1 accepts this, and the page's prose has no dashes.
- **Chart:** a line chart of hourly prices for FR, NL, BE and IE-SEM, UTC days 14 to 20 September 2026.
  - FR, NL and BE are hourly means of their quarter-hours; IE-SEM is its own hourly price.
  - DE-LU is left out (see finding 1).
- **Artefacts:** all three were made by the commands.
  - `site/hifi/data/series/entsoe/day_ahead_prices.json`: `spec_origin: vault`, 4 series by 168 points, 2,184 rows used.
  - `site/hifi/data/samples/entsoe/day_ahead_prices.json`: 8 rows.
  - `site/hifi/data/notebooks/entsoe/day_ahead_prices.json` and `day_ahead_prices-5.png`.
- **Cleanup:** there was no staged chart spec or authored override for this dataset.
- **Mirror:** `vault/entsoe/day_ahead_prices.md` is a byte copy of the canonical note (`cmp` clean). The canonical note keeps CRLF on all 339 lines.
- **Screenshots:** taken at 1440, 1024 and 768 in headless Chrome, and at 390 through a 390 px iframe, each "light" and "dark". Nothing is clipped or overlapping: the hero turbines, the chart axes and key, the frame folded behind `…`, the guide, the notebook, the related links and the stratum labels are all fully visible. The site has no dark scheme (no `prefers-color-scheme` in any stylesheet), so the dark captures are identical to the light ones.

## Seat rulings applied

1. **EIC codes.** The eight rows were chosen on merit (FR, NL, BE and IE-SEM at 12:00 and 13:00 UTC on 20 September), and the codes print plainly in the frame. In the front matter, the three dashed EICs appear only as `group_map` keys. They are written with `\x2D` escapes in double-quoted YAML, as in the corrected ruling, for example `"10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC"`.
   - The escape is needed. `30-vendors/scripts/derive_machine_catalog.py:180` and `gridflow_drift_check.py:129` both do `text.split("---", 2)`, so a plain key would cut off their YAML.
   - The filters avoid dashed EICs: `area_code ne "10Y1001A1001A82H"` (DE-LU) plus `currency eq EUR`.
   - The request example uses IE-SEM's EIC. The notebook selects FR with `str.startswith("10YFR")`.
2. **`published_at`.** The guide says "Response `createdDateTime`, stamped within seconds of the fetch; not the auction time". The note body says the same.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Relation `silver_entsoe_day_ahead_prices`, date column `timestamp_utc` (`notebook.lead`) | `_validate_dataset_for_source` / `_relation_name_for_dataset` run in the gridflow_models venv returned `timestamp_utc silver_entsoe_day_ahead_prices` |
| Both ends included, as UTC days; returned in the session's time zone, Europe/London (`notebook.lead`) | Read-only run of `query('day_ahead_prices','2026-09-14','2026-09-20')`: dtype `datetime64[us, Europe/London]`, min `2026-09-14 01:00+01:00` (00:00 UTC), max `2026-09-21 00:45+01:00` (23:45 UTC on the 20th), 2,856 rows. The notebook's `.head()` prints `+01:00`. |
| Lineage columns dropped; ordered by the date column only | `research/handles/source.py:401-445` (`SELECT *{exclude} … ORDER BY {date_col}`); `_BITEMPORAL_EXCLUDE` = event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year |
| Key `timestamp_utc, area_code` (`record.key`) | `silver/entsoe/day_ahead_prices.py:83` `df.unique(subset=["timestamp_utc","area_code"], keep="last")` |
| `timestamp_utc` = period start + (position−1) × resolution, UTC | `connectors/entsoe/parsers.py:527-531` |
| `area_code` = `in_Domain.mRID` as sent | `parsers.py:289-297`; transformer renames `in_domain` to `area_code` (`day_ahead_prices.py:59`) |
| Points the vendor omits repeat the previous one (`record.fields.price_eur_mwh`) | `parsers.py:533-601`: curve type A03 forward-fill. Every bronze series seen is `curveType A03`; the FR delivery-day-16 series declares 95 points and silver holds 96 quarter-hours. |
| `currency` is authoritative over the `_eur_` column name | `schemas/entsoe.py:13-20` docstring; `day_ahead_prices.py:67-81` |
| Currency EUR, unit MWh | Bronze `currency_Unit.name` EUR and `price_Measure_Unit.name` MWH on every series of the 15 Sep captures. The silver `currency` column is EUR for every row of every zone, and the chart spec filters `currency eq EUR`. |
| `resolution` `PT15M` or `PT60M`; FR, NL, BE and DE-LU in quarter-hours and IE-SEM hourly, 14 to 20 Sep 2026 (`what_it_is`) | Silver group-by: FR, NL, BE and DE-LU are all PT15M (96 per UTC day); IE-SEM is PT60M (24 per day). The bronze `<resolution>` tags agree. |
| `published_at` is the response `createdDateTime`, within seconds of the fetch | `day_ahead_prices.py:93-94`, `_published_at.py`. Bronze `raw_20260921T095934Z_87ec5c76.xml` has `createdDateTime 2026-09-21T09:59:33Z` and its meta has `fetched_at 09:59:34.26`. Silver rows for delivery on 19 and 20 Sep carry `published_at` of 21 Sep 09:59 to 10:01. |
| GB returns Acknowledgement 999, no data (`what_it_is`) | GB is requested (`endpoints.py:395` `DEFAULT_ZONES`). Bronze `…/2026/09/15/raw_20260921T095930Z_a7bdcf36.xml` is an `Acknowledgement_MarketDocument` with Reason code 999, text "No matching data found for Data item ENERGY_PRICES [12.1.D] (10YGB----------A, 10YGB----------A)…", HTTP 200. Silver has no GB rows. |
| DE-LU sends two numbered sequences (their meaning is not in the document); silver keeps whichever the document lists last (`what_it_is`, caption) | Bronze DE-LU documents carry two TimeSeries per delivery day, with `classificationSequence_AttributeInstanceComponent.position` 1 and 2 and different prices (for 15 Sep 22:00Z, 219.74 against 219.01). The parser does not read the tag (`parsers.py:284-388`), and dedup keeps the last (`day_ahead_prices.py:83`). The two are mixed in silver: on 14 Sep, 87 quarter-hours match sequence 1 and 8 match sequence 2; on 15 Sep, 8 and 88; on 16 to 20 Sep, all sequence 1. Sequence order in the documents varies (`[2,1,1,2]`, `[1,2,2,1]`, `[2,1,2,1]`). The largest gap between sequences on 14 Sep is 322 EUR/MWh. Scripts: `scratchpad/seqcheck.py`, `dupcheck.py`. |
| FR, BE and IE-SEM duplicates are harmless (why they are charted) | `dupcheck.py` over 25 bronze days: FR, BE and IE-SEM sometimes send two series per delivery day, always with identical prices. NL always sends one. DE-LU sends two distinct sequences in 75 delivery-day documents and sequence 2 alone in 10. |
| Request URL (`raw_feed.requests`) | Bronze meta `request_url` gives this order: `documentType=A44&periodStart=…&periodEnd=…&in_Domain=…&out_Domain=…&securityToken=<redacted>` (`client.py:288-309`, `_domain_params` :550-551). Host from `config/sources.yaml:164`. |
| One call per zone and UTC day (`raw_feed.note`) | `client.py:131-168` `day_subwindows`; `_build_unit_tasks` :246-263 loops `DEFAULT_ZONES` |
| Replies hold whole delivery days from 22:00 UTC; transform keeps rows inside the requested day | Bronze periods run `2026-09-14T22:00Z` to `2026-09-15T22:00Z` and on to `…16T22:00Z` for a 15 Sep request. `EVENT_WINDOW_FILTER = True` (`day_ahead_prices.py:26`; `silver/base.py:686-698`, HALF_OPEN exclusion of rows outside `[periodStart, periodEnd)`). |
| Ingest `--end 2026-09-21` is exclusive; transform `--end 2026-09-20` is inclusive; no widening | `runner.resolve_dates` (a bare date is midnight UTC) and `day_subwindows` (an end at midnight excludes that date). `PARTITION_SOURCE_OFFSETS` defaults to `(0,)` (`silver/base.py:417`) and is not overridden. |
| Cadence: "Daily, ahead of each delivery day" | The vault note's "Publication lag ~12:55 CET D-1 for D". Bronze captures from the afternoon hold the next delivery day. DE-LU sequence 2 sometimes arrives alone, so the wording avoids "once". |
| Chart numbers (alt, caption) | Committed series: FR max 305.82 (14 Sep 18:00), NL max 400.0 and BE max 441.735 (14 Sep 17:00), lowest -3.053 (NL, 20 Sep 11:00). IE-SEM ranges from 1.095 (19 Sep 04:00) to 359.165 (20 Sep 08:00), and 147 to 359 on 20 Sep. FR, NL and BE fall to about zero at midday on 19 and 20 Sep. |
| Eight rows (`record.caption`) | Sample JSON: IE-SEM 217.665 and 211.91 (PT60M); BE -0.76 and -0.92, FR -1.0 and -1.0, NL -3.04 and -2.15 (PT15M) |
| Notebook plot (`plot_alt`) | `day_ahead_prices-5.png` viewed: FR quarter-hours about -1.3 to 333 (raw silver min -1.29, max 333.17), IE-SEM 1 to 359. On the 20th, FR sits near zero from early morning to mid-afternoon while IE-SEM peaks at 359. |
| Related: `elexon/mid` is the GB market index price | Elexon page set; the build resolved it |

## Note-body corrections (canonical note, smallest spans)

1. **Rate limit.** "configured at 1 req/s" becomes 6 req/s, citing `config/sources.yaml:167`. The "treat 1 req/s as polite" advice is kept.
2. **Point-in-time field.** "none" becomes `published_at`, the response `createdDateTime` (`day_ahead_prices.py:93-94`). The line adds that it matches the fetch time (09:59:33Z against a 09:59:34Z fetch), not the auction.
3. **Silver schema table.**
   - `price_eur_mwh` note: now "price per MWh in `currency`", the legacy name, and the A03 forward-fill (`schemas/entsoe.py:13-20`, `parsers.py:533-601`).
   - Added the missing `published_at` row.
4. **Known issues, 15-minute zones.** "DE-LU and a growing list" now reads: FR, NL, BE and DE-LU send PT15M and IE-SEM sends PT60M, in the September 2026 captures, with the bronze path cited.
5. **Known issues, "dedup is sufficient".** Corrected for DE-LU: the two classification sequences, the order-dependent `keep="last"` (`:83`), the silver mix counts, and FR, BE and IE-SEM duplicates being identical. It states that the document does not say what the sequences are.

Left unchanged:
- The curl example (it is right for the vendor).
- The "No revisions" sentence.
- The Elexon `system_prices` pointer for GB (see open questions).
- The illustrative silver sample block.

## Findings for the seat

1. **gridflow defect (DE-LU prices are order-dependent).** `DayAheadPricesTransformer` dedups on `(timestamp_utc, area_code)` and the parser drops `classificationSequence_AttributeInstanceComponent.position`. DE-LU silver therefore mixes two different price sequences, chosen by document order, with gaps up to 322 EUR/MWh in a quarter-hour. The page states this and keeps DE-LU out of the chart and the rows. A fix belongs in gridflow: carry the sequence in the key, or keep one sequence deliberately.
   - **Ruling needed:** ship this page with the caveat, or hold it until gridflow is fixed. I recommend shipping: the four charted zones are sound and the caveat is real domain depth.
2. **What the sequences are is not in the repo.** Sequence 1 equals the NL price at the same quarter-hour (219.74 at 15 Sep 22:00Z), so it looks like the coupled price. Sequence 2 sometimes arrives alone (10 documents), suggesting an earlier publication. Neither is verified; the page does not guess. This is research for a later piece of work.

## Unverified

- **Cadence.** "Daily, ahead of each delivery day" rests on the vault note's publication-lag line and the bronze timing. No vendor document is quoted.
- **Whether `in_Domain` always equals `out_Domain` in the reply.** Only the request is shown on the page.
- **Historical depth ("~5 years").** Not stated on the page, since there is no vendor evidence.

## Open questions

1. DE-LU: ship with the caveat or hold? This is the seat's call; recommendation above.
2. The note's modelling advice "Use Elexon `system_prices` for GB" points at imbalance prices, not a day-ahead reference. Elexon `mid` looks closer; the page's related link uses `mid`. I left the body alone because this is domain judgement, not a code fact.
3. `cadence` has no vendor quote. Keep it, or drop it to vendor and grain only?

## Revision 1 (after `day_ahead_prices-review.md`, REVISE with 2 majors and 2 nits)

1. **Major, rate limit (body).** Restored "codebase configured at 1 req/s", now citing `config/sources.yaml:192`.
   - My mistake: I had read `gridflow/.tmp/validation-7day-20260511/config/sources.yaml`, a gitignored copy.
   - Body correction 1 above is withdrawn.
   - The evidence-table host citation should read `config/sources.yaml:189`; the value is unchanged.
2. **Major, `page.facts.cadence`.** Now reads "Daily; afternoon replies here already held the next delivery day". It is scoped to the responses we hold. Evidence: the 15 Sep 19:53 UTC fetch holds delivery day 16, from 15 Sep 22:00 UTC.
3. **Nit, `page.what_it_is` and the body bullet.** "whichever the document lists last" now reads "whichever the latest reply lists last". The body adds that `read_bronze` concatenates every capture in name order (`day_ahead_prices.py:36`).
4. **Nit, `record.fields.price_eur_mwh`.** Now scoped: "omitted points repeat the previous one (curve type A03)".
5. **Batch rule.** `record.fields.timestamp_utc` now reads "Start of the price period, UTC: `start + (position - 1) × resolution`" (`parsers.py:530`).

Gates:
- Canonical note CRLF on all 340 lines; no literal `---` in the front matter.
- Mirror `cmp` clean.
- `gridflow-build --only entsoe/day_ahead_prices` succeeds; the detector shows only the accepted EIC-dash advisory.
- Series, sample and notebook are unchanged (neither the chart spec nor `record.select` changed).
- Screenshots at 1280 (headless Chrome, `timeout 60`) and 390 (390 px iframe): nothing is clipped or overlapping.

## Template problems (not worked around, except as noted)

1. **One bad note blocks every writer's distil.** `gridflow-distil --dataset X` validates every note (`distil.py:479-489`), so another writer's mid-edit note (`cross_border_flows`) blocked my distil until they fixed it. Suggest scoping validation to `--dataset`.
2. **Emphasis inside inline code.** Markdown in guide lines turns `` `_eur_` `` into italic "eur" in code font, with the underscores lost. I reworded around it; the renderer should protect code spans before applying emphasis.
3. **Dashed EICs need escapes in the front matter.** EICs with dash padding (FR, NL, BE) cannot appear in front matter unescaped. `group_map` keys needed `\x2D` escapes, and `chart_view.key.codes` uses gridflow's own zone keys (FR, NL, BE, IE-SEM from `endpoints.py:379-392`) instead of EICs. A `group_map` keyed by some fence-safe form would be cleaner.
4. **Mixed resolutions cannot share a chart unbucketed.** The renderer shares one x grid across series and breaks a line at every null (`chart_svg.py:350-368`), so an hourly series beside quarter-hour series draws as dots. This forced `time_bucket: 1h`. A per-series step would allow raw quarter-hours beside hourly zones.
