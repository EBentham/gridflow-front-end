# entsoe/actual_generation: writer report

Written 2026-09-29. Canonical note: vault worktree `30-vendors/entsoe/datasets/actual_generation.md` (CRLF, 316 lines). Mirror: `vault/entsoe/actual_generation.md` in the front-end worktree, byte-identical (`cmp` clean).

## Status

- Build `gridflow-build --only entsoe/actual_generation`: passes. Detector `[]`.
- Artefacts: `series/entsoe/actual_generation.json` (distil, `spec_origin: vault`, 9 series by 672 points, 10,079 rows used), `samples/entsoe/actual_generation.json` (gridflow-sample, 8 rows), `notebooks/entsoe/actual_generation.json` plus `actual_generation-5.png` (run_notebooks, 5 cells, no errors).
- No staged chart spec or authored override existed for this dataset.
- Chart: stacked area, DE-LU only, B10 excluded, every quarter-hour of 12 to 18 September 2026 UTC.

## Headline finding: gridflow defect (silent generation/consumption collapse)

ENTSO-E A75 sends a separate consumption TimeSeries for some production types, tagged `outBiddingZone_Domain.mRID` instead of `inBiddingZone_Domain.mRID`. Both carry `businessType` A01 in bronze.

- The parser reads both tags into the same `in_domain` field (`connectors/entsoe/parsers.py:289-297`).
- The transformer's dedup key `(timestamp_utc, area_code, production_type)` has no side, with `keep="last"` (`silver/entsoe/actual_generation.py:80`).
- So where both series exist, silver keeps one figure and nothing records which.

Measured by re-parsing all 24 bronze days with gridflow's own parser, with the out tag renamed so the side survives, joined to silver:

| Outcome | Rows |
|---|---:|
| Silver = generation, no consumption series | 63,984 (every one matches exactly) |
| Both series; silver holds consumption where generation differs | 19,623 |
| Both series; silver holds generation | 11,193 |
| Consumption series only | 2,752 |
| Both series, equal values | 3,279 |
| Total silver rows | 100,831 |

- **Which side wins is effectively arbitrary.** It changes day by day: DE-LU B10 holds generation on 1 to 5 August and on 7, 9, 11 and 13 September, and consumption on every other day through 20 September.
- **Worst case is NL.** From 2 September, silver's NL B04 (gas) shows about 140 MW of consumption against more than 7,000 MW of generation.
- **Affected types** (bronze 2026-09-15):

  | Zone | Types with a consumption series |
  |---|---|
  | DE-LU | B10 |
  | FR | B05, B10, B18, B25 |
  | BE | B10 |
  | NL | all ten types |
  | IE-SEM | eight types |

- **Example.** DE-LU B10 at 2026-09-18 12:00Z: silver 4,055.19 MW is the consumption series; generation was 67.36 MW. At 17:00Z the same day, silver shows 14 MW while generation was 5,417 MW.

**Page consequence.** The chart is clean by construction: DE-LU with B10 excluded is 34,017 of 34,017 rows matching generation. The silver table is not safe for any other zone, or for B10 anywhere.

**Recommendation to the seat.**
- Ship the page as written, since every stated fact is scoped and the chart is clean.
- Open a gridflow fix unit: carry the side (in/out domain) into the silver key, or split consumption into its own column. `generation_forecast` has the same parser path, and its sibling page already says so.
- Whether to hold the page until the fix lands is your call. I recommend no hold.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Vendor A75 / A16 (`facts.vendor`) | `connectors/entsoe/endpoints.py:37-43`; bronze meta `request_params` |
| Cadence PT15M DE-LU/FR/NL, PT30M IE-SEM, PT60M BE (`facts.cadence`, `record.fields.resolution`) | bronze `<resolution>` tags 2026-09-15, all five files; silver `resolution` one value per zone |
| Grain / key (`facts.grain`, `record.key`) | dedup `actual_generation.py:80` |
| "B01 biomass to B25" (`what_it_is`) | code list v36r0 cache (gridflow `.planning/audit/2026-05-31-vendor-truth-audit/vendor-docs/entsoe-codes.md` §6) for B01; B25 named nowhere on the page |
| gridflow requests six zones (`what_it_is`) | `DEFAULT_ZONES` `endpoints.py:395`; loop `client.py:249` |
| GB returns a no-data acknowledgement (`what_it_is`) | bronze 2026-09-15 `raw_20260921T100644Z_30c7aec1.xml`: `Acknowledgement_MarketDocument`, reason 999 "No matching data found ... (10YGB----------A)"; note's own live check 2026-05-08 |
| Some types carry a consumption series; silver cannot tell which (`what_it_is`, caption, `area_code` field) | parsers.py:289-297, actual_generation.py:80, bronze tags; measurement above |
| Chart: DE-LU, B10 excluded, 12 to 18 Sep UTC, codes summed per group | spec filter/window; distil `window` fixed and inclusive of end date (`distil.py:270-278`) |
| Alt values: biomass 3.6 to 4.4 GW, lignite 4.3 to 12.4, gas 1.3 to 9.6, wind 1.7 to 27.1, solar peak 48.9 on 15th, stack 30.1 to 75.6 | committed series min/max (biomass 3580/4402, lignite 4255/12440, gas 1337/9625, wind 1662/27055, solar max 48938 at 2026-09-15T10:30Z, stacked total 30118/75594) |
| Key notes: B18+B19 summed; B06/B09/B15/B17 names; B11/B12 names; B20 undocumented contents | group_map; code names per PSR section of the note |
| Request URL and parameter order (`raw_feed.requests`) | bronze meta `request_url` for DE-LU 2026-09-15: `documentType, periodStart, periodEnd, in_Domain, processType, securityToken`; `ENTSOE_DT_FORMAT` `%Y%m%d%H%M` |
| One request per zone and UTC day (`raw_feed.note`) | `client.py` `fetch()` `day_subwindows` loop; `utils/time.py:123-163` |
| Ingest `--end 2026-09-19` exclusive (`raw_feed.commands`) | bare date = midnight UTC (`runner.resolve_dates`), `day_subwindows` excludes the end date; `max_query_days` is not read by the ENTSO-E connector |
| Transform 12 to 18 inclusive; no neighbour-day reads | `PARTITION_SOURCE_OFFSETS` default `(0,)` (`silver/base.py:417`); `EVENT_WINDOW_FILTER = True` trims to `[periodStart, periodEnd)` (`base.py:1862-1913`) |
| Eight rows; B10 4,055.1934 is the consumption figure (`record.fields.generation_mw`) | gridflow-sample output; bronze re-parse: out series 4055.1934, in series 67.3645 at 2026-09-18T12:00Z |
| 16 codes at that instant (`record.caption`) | silver DE-LU 2026-09-18 12:00Z has 16 production_type rows |
| `timestamp_utc` = period start + (position-1) x resolution | `parsers.py:527-531` |
| `area_name` from EIC lookup | `actual_generation.py:66-72`, `connectors/entsoe/area_codes.py` |
| `published_at` = createdDateTime, a fetch-time stamp (ruling 2) | `actual_generation.py:90-91`, `_published_at.py`; DE-LU 2026-09-15 createdDateTime 10:06:50Z vs bronze `fetched_at` 10:06:51.8Z |
| Notebook lead: relation, `timestamp_utc`, both ends inclusive, lineage dropped | `gridflow_models/research/handles/source.py:401-451` (`_date_range_predicate`, `_present_bitemporal_exclude_clause`); schema_manifest `("entsoe","actual_generation"): "timestamp_utc"` |
| Plot alt: solar peaks 22,047 MW (13th) to 48,938 MW (15th), peaks 10:00 to 11:45 UTC | silver DE-LU B16 daily max for 12 to 18 Sep |
| Related pages resolve | build passes (resolution check) |

## Note-body corrections (each cites evidence in the note)

1. **Business type row.** It said "A04 = consumption / A03 = generation". Bronze shows `A01` on every series; the side is the domain tag. The out-equals-consumption reading is marked `TODO: verify` against API guide §16.1.B&C.
2. **Point-in-time field.** It said "none (keep=last by sort)". It now says `published_at` exists but is a fetch-time stamp (ruling 2); dedup keeps the last row read.
3. **Silver schema table.**
   - `area_code`: both tags feed it.
   - `area_name`: populated.
   - `production_type`: points to the PSR list.
   - `generation_mw`: carries the caveat.
   - Added rows for `resolution`, `published_at` and `ingested_at`, which were missing.
4. **New "PSR codes" subsection.** The official list via the gridflow audit cache, plus entsoe-py for the codes the cache omits, marked `TODO: verify`.
5. **Known issues.**
   - Resolution by zone: was "DE/AT/FR PT15M, others PT60M"; now matches bronze.
   - `published_at` "not surfaced": corrected.
   - `area_name` "not populated": corrected.
   - "Code keeps both rows": false. Replaced with the defect paragraph and its measurement.
6. **Implementation delta.**
   - `psrType` "not in optional_params": it is (`endpoints.py:37-43`).
   - `area_name` "unfilled": it is filled.

Left alone: the silver sample block still shows `area_name: ""` (a dated May example); the Overview; the GB "post-Brexit" cause sentence (a claim in the body, not on the page).

## Unverified

- **PSR names for B02, B03 and B06.** They come from entsoe-py (de facto), not the vendor PDF. The gridflow cache omits them, the ENTSO-E knowledge-base page returned 403, and the explorer's `codes.ts` agrees with entsoe-py. They appear on the page as lignite (B02), coal gas (B03) and oil (B06), in the chart key only.
  - B25's name has been dropped from the page (`what_it_is` now reads "B01 biomass to B25"), because the front-end brief `content-briefs/entsoe/_landing.md:262` calls it "Not specified" while entsoe-py says "Energy storage".
- **`outBiddingZone_Domain` means consumption.** This is corroborated de facto by entsoe-py `parsers.py` (`CONSUMPTION_ELEMENT = "outBiddingZone_Domain.mRID"` gives "Actual Consumption") and by the values (B10 high at midday when solar peaks and near zero at the evening peak). It is still not checked against the API guide itself; the note carries a TODO. The B10 guide line ("pumping (consumption) figure, checked against bronze") rests on this.
- **"B20 Other: what it holds is undocumented."** No vendor definition was found.

## Open questions for the seat

1. **Hold or ship, given the defect?** Recommend ship, plus a gridflow fix unit, as above.
2. **Token placeholder.** Siblings differ: `generation_forecast` uses `$ENTSOE_API_KEY`, `actual_load` uses `<your-entsoe-api-key>`. I used `$ENTSOE_API_KEY`, as in the note's curl. Pick one for the batch.
3. **One missing B12 point.** DE-LU B12 has no quarter-hour at 01:45 UTC on 15 September (about 54 MW). The hydro band dips by that much there, which is invisible at chart scale. I did not mention it on the page, since it is a local holdings gap.

## Template or tooling problems

- **Distil validates every note before writing any.** Another writer's `cross_border_flows` note (EIC codes containing `---`) blocked my distil for several minutes. One bad note blocks all authors.
  - The `---` guard also collides with legitimate EIC codes such as `10YFR-RTE------C` and `10YGB----------A` in spec filter values. This page avoids them only because DE-LU's code has no dashes. Ruling 1 covers the detector side, not this guard.
- **Headless Chrome drops tall screenshots.** With a 7,000 to 9,000 px window, rendering stopped at the bronze corner label ("bronze, the r") at 1440 and 390. Shorter windows (4,400 px, or 1,200 px iframe bands) render everything. This is a screenshot artefact, not the page. The checker should use short windows.
- **The 390 frame shows only its first column** before the fold, so the B10 row's value is not visible at phone width (template behaviour, same as the Elexon pages).
- The gold corner label sits tight above the notebook panel at 1440 but is not clipped (template).

## Screenshots checked (light only; the site has no dark theme stylesheet)

1440, 1024, 768 and 390 (390 via iframe bands): hero scenery, chart, key, raw feed, commands, frame and guide, notebook panel, related, and each stratum's corner label. Nothing clipped or overlapping.

## Batch rulings applied

- **Ruling 1, as corrected (no literal `---` in front matter; `\x2D` escapes for EIC codes there):** nothing to escape. The front matter's only EIC code is `10Y1001A1001A82H`, and a grep of the front matter finds no `---`. The body keeps codes plain. Detector `[]`.
- **Ruling 2 (`published_at` is a fetch-time stamp):** `record.fields.published_at` and three body lines reworded.

## Line endings

The canonical note stays CRLF. The mirror copy is byte-for-byte, so it is CRLF too, where the old mirror was LF. Git in the vault worktree reports `i/lf w/crlf` with `core.autocrlf=true`, so the committed form normalises. Flagged only so the seat is not surprised by a whole-file diff if the front-end repo does not normalise.
