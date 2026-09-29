# entsoe/water_reservoirs: writer report

Writer: Opus 5.5 · high, 2026-09-29. Screenshot port 9833 (server stopped).

**Status**
- **Build:** `gridflow-build --only entsoe/water_reservoirs` passes with no errors. The three content warnings are for other datasets.
- **Detector:** one advisory finding only, `em-dash-overuse` ("43 em-dashes"). It counts the `------` padding in `10YFR-RTE------C`. The rendered page has 0 real em dashes, so this is accepted under ruling #39/#40.
- **Tests:** `test_dataset_page.py::test_a_page_without_a_page_block_is_blank` now fails, as expected. It uses this page as its blank example (lines 202 to 211), and I did not edit it; the seat swaps it at PR time. The rest of the suite passes: 100 passed, 1 deselected.

## Files written

- **Canonical note:** `vault-p26-entsoe/30-vendors/entsoe/datasets/water_reservoirs.md`, with the `page:` block and the body corrections below.
  - CRLF is kept (274 CR for 274 LF).
- **Mirror:** `p26-entsoe/vault/entsoe/water_reservoirs.md`, byte-identical (checked with `cmp`).
  - The mirror used to be LF; the copy brings in CRLF, like the other 20 mirrors.
- **Series:** `site/hifi/data/series/entsoe/water_reservoirs.json`.
  - Written by `gridflow-distil`, `spec_origin: vault`.
  - 4 points; 14 duplicates were dropped.
- **Sample:** `site/hifi/data/samples/entsoe/water_reservoirs.json`, written by `gridflow-sample`, 8 rows.
- **Notebook:** `site/hifi/data/notebooks/entsoe/water_reservoirs.json` and `water_reservoirs-5.png`.
  - Written by `scripts/run_notebooks.py`.
  - Every cell is read-only, and no cell raised an error.
- **Staged files:** no staged chart spec or authored override existed.
- **Built page:** `site/hifi/data-sources/entsoe/water_reservoirs.html`.

## Evidence table

| Claim (where) | Evidence |
|---|---|
| Only France returns data (what_it_is, raw_feed.note) | 126 bronze XML files: 19 are `GL_MarketDocument`, all with `in_Domain=10YFR-RTE------C`. The other 107 are `Acknowledgement_MarketDocument`, "No matching data found for Data item AGGREGATE_FILLING_RATE_OF_WATER_RESERVOIRS_R3 [16.1.D]", for GB, NL, BE, DE-LU and IE-SEM, plus FR on 14 Sep and 21 Sep in the 15 Sep and 26 Sep runs. All 18 silver rows have `area_code = 10YFR-RTE------C`. |
| Six zones, one GET per zone per UTC day (raw_feed.note) | `endpoints.py:395` `DEFAULT_ZONES = [GB, FR, NL, BE, DE-LU, IE-SEM]`; `client.py:249` loops over them; `client.py` `fetch()` uses `day_subwindows` (`utils/time.py:123`), one sub-window per UTC day. |
| Request URL (raw_feed.requests) | Parameter order `documentType, periodStart, periodEnd, in_Domain, processType, securityToken` (`client.py:286-310`). This matches bronze `meta.json` `request_url`, e.g. `2026/08/01/raw_20260816T134644Z_81962bd1.meta.json`. `ENTSOE_DT_FORMAT = "%Y%m%d%H%M"` (`endpoints.py:403`). |
| A one-day request returns the week containing its start (raw_feed.note, caption, grain) | FR `periodStart=202608010000` and `202608020000` both return `Period` 2026-07-26T22:00Z to 2026-08-02T22:00Z. `202608030000` returns 2026-08-02T22:00Z to 2026-08-09T22:00Z. `202609080000` to `202609130000` all return 2026-09-06T22:00Z to 2026-09-13T22:00Z. `202609140000` to `202609200000` (26 Sep run) return 2026-09-13T22:00Z to 2026-09-20T22:00Z. |
| Timestamp is the week start; point time rule (record.fields.timestamp_utc) | `parsers.py:530`: `start_dt + (position - 1) * resolution`. Every FR document has one `Point`, `position` 1, `P7D`, so `timestamp_utc` equals the Period start. 22:00 UTC Sunday is Monday 00:00 CEST. |
| Weekly average, MWh (summary, what_it_is, reservoir_mwh line) | Reg. 543/2013 Art. 16(1)(d): "aggregated weekly average filling rate of all water reservoir and hydro storage plants (MWh) per bidding zone" (https://www.legislation.gov.uk/eur/2013/543/article/16, read 2026-09-29). The acknowledgements name data item `[16.1.D]`. Every FR XML carries `<quantity_Measure_Unit.name>MWH`. The quote is now in the note body. |
| Unit not stored (record.fields.reservoir_mwh) | The parser's TimeSeries loop (`parsers.py:286-360`) has no branch for `quantity_Measure_Unit.name`. The silver schema (`schemas/entsoe.py:265-273`) has no unit column. |
| `area_code` from `inBiddingZone_Domain.mRID` | `parsers.py:292` maps it to `in_domain`. `water_reservoirs.py` renames `in_domain` to `area_code`. |
| Dedup key per file; repeats across files (facts.grain, record.key, caption, notebook.lead) | `water_reservoirs.py:59`: `unique(subset=["timestamp_utc", "area_code"], keep="last")`, per `read_bronze(target_date)`, so per partition. Silver has 18 rows over 4 distinct `(timestamp_utc, area_code)` pairs. The 26 Jul week appears ×2 (files 0801, 0802), 2 Aug ×3 (0803 to 0805), 6 Sep ×6 (0908 to 0913) and 13 Sep ×7 (0914 to 0920). Values are identical within a week; only `published_at`, `ingested_at` and `source_run_id` differ. |
| `published_at` is a fetch-time stamp | `water_reservoirs.py:70` `with_published_at` parses `createdDateTime`. In bronze, `createdDateTime` 2026-08-16T13:46:44Z against `meta.json` `fetched_at` 13:46:44.73 (ruling #39). |
| `resolution` is as sent, `P7D` | `parsers.py:459` stores the ISO code. The silver value is `P7D` in all 18 rows. |
| `ingested_at` (vault body) | `water_reservoirs.py:61` `datetime.now(UTC)` at transform time. |
| Chart values (alt, key) | Series JSON `x` = 2026-07-26T22Z, 08-02T22Z, 09-06T22Z, 09-13T22Z; values 2,261,238, 2,191,776, 1,989,272, 1,952,966. |
| Points drawn mid-week (x_label, alt) | `chart_svg.py:234` (`hi_edge = hi + step`, each value covers its interval) and `:444-454` (`plot.X(t + half)`). Seen in the screenshots. |
| Line breaks between 2 Aug and 6 Sep | `chart_svg.py:357` breaks the line where the gap exceeds 1.5 × the smallest step (7 d). The gap here is 35 d. |
| `query()` behaviour (notebook.lead) | `gridflow_models/.../source.py:401-451`: filters on the designated date column (`schema_manifest.py:191` gives `timestamp_utc`), inclusive whole-day ends via `_date_range_predicate`, `EXCLUDE` of `BITEMPORAL_EXCLUDE` (event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year), `ORDER BY` date column only. The view is a plain `read_parquet` glob (`storage/duckdb.py:445`), so there is no dedup. |
| Notebook outputs (plot_alt) | Cell 4: 4 rows, values as above, `published_at` in UTC. The PNG shows two segments, about 2,261 to 2,192 GWh and 1,989 to 1,953 GWh, with a break (`asfreq("7D")` gives NaN weeks). |
| Commands window | Each day D's request returns the week containing D 00:00 UTC. Ingest days 27 Jul to 14 Sep (`--end 2026-09-15`, exclusive per `day_subwindows`) give weeks stamped 26 Jul 22:00 to 13 Sep 22:00. Transform `--end` is inclusive. No `PARTITION_SOURCE_OFFSETS`. `needs` matches: 27 July to 14 September. |
| Related: FR has B10, B11 and B12 | Polars on silver: `actual_generation` FR has B10, B11 and B12 rows; `installed_capacity` FR has B10, B11 and B12 rows. |

## Body corrections (canonical note, smallest spans)

1. **Overview:** added the vendor definition. It quotes Reg. 543/2013 Art. 16(1)(d) and 16(2)(d) with the URL, tied to the acknowledgement's data item `[16.1.D]`.
2. **API table, publication lag:** "weekly publication, T+~1 week" is now "third working day after the week (Reg. 543/2013 Art. 16(2)(d))".
3. **Dedup key:** now says the key holds within one silver file only (`water_reservoirs.py:59`), and each daily file repeats its week (bronze 0801 and 0802 evidence).
   - **Point-in-time field:** `ingested_at` is now `published_at` (`water_reservoirs.py:70`).
4. **Silver schema:**
   - `timestamp_utc` source is now the point-time rule (`parsers.py:530`).
   - Added a `published_at` row.
   - `ingested_at` is now "Silver transform time (`water_reservoirs.py:61`)".
5. **Silver sample:** `"resolution": "7 days, 0:00:00"` is now `"P7D"` (`parsers.py:459`).
   - The sample stays an illustrative NO-1 row, although NO-1 is not a zone gridflow requests.
   - I did not invent a `published_at` value for it.
6. **Gotcha "30-day window minimum":** amended. FR one-day requests return the containing week (bronze `2026/08/01`). The May ES probe stands as recorded.
7. **Gotcha "GB / DE-LU / IE-SEM EMPTY":** added that NL and BE also acknowledge no data in gridflow's Aug and Sep 2026 bronze, and FR is the only default zone that returns a document.
8. **Gotcha "some zones report percentage":** marked unverified (no source). The parser does not read the unit.
9. **Implementation delta:** "the caller must pass a Nordic / Iberian zone via `**params`" is false.
   - `client.py:249` loops over `DEFAULT_ZONES` unconditionally.
   - `client.py:306` forwards only `optional_params`, and A72 declares none (`endpoints.py:113`).

## Not verified

- **Level or average.** The claim rests on the regulation text: Art. 16(1)(d) says "weekly average". The XML does not say which.
- **Source of the regulation text.** I read the UK-retained copy on legislation.gov.uk because EUR-Lex returned an empty page to the fetcher. The wording should match the EU original, but I could not confirm it against EUR-Lex.
- **Coverage beyond FR.** The note's hydro-zone list (NO, SE, ES, IT, AT, CH, DK-2) is untested by gridflow, because the connector cannot request those zones.
- **Winter stamps.** "22:00 UTC on a Sunday" is scoped to these rows. In winter the stamp would be 23:00 UTC by the same local-midnight logic, but no winter row exists.
- **Request-to-week mapping.** "A one-day request returns the week containing its start" is seen in every FR response held (Aug and Sep 2026). It is not a documented vendor rule, and the page scopes it to "the responses gridflow holds".

## Open questions (for the seat)

1. **Hold or ship this thin page.** It has one zone and four weekly points, and the chart shows two 2-point segments.
   - The caption says "No weeks stamped 9 to 30 August are drawn". That describes what is drawn, not local coverage, but a checker could read it as a local-gap statement.
   - The alternative is a 2-point window (6 to 13 September) with no break. I judged the 4-point version more useful to a reader.
2. **`record.key` choice.** I used `[timestamp_utc, area_code, published_at]`, not the transformer's `(timestamp_utc, area_code)`, because the shown rows repeat on the code key.
   - `facts.grain` says the code key holds per silver file.
   - If the seat prefers the code key in the frame, the grain line already carries the caveat.
3. **Float display.** The frame prints `reservoir_mwh` as `2.261238e6`. That is Polars' own float display, not something I chose.

## Template observations (no change made)

- **Line placement.** The line renderer places each point at the middle of its interval (`chart_svg.py:444-454`). For weekly data this puts the dot about 3.5 days after `timestamp_utc`, so the x_label says "points drawn mid-week". This is fine, but authors of other interval-stamped pages (P1M, P1Y lines) may misdescribe it.
- **No dark theme.** No `prefers-color-scheme` or `data-theme` rules exist in `site/hifi/assets`. The rubric's "light and dark" check therefore has only one mode to check.
- **Notebook panel.** The panel shows only cells 1 and 2 at every width, and the rest is behind "Open the demo notebook". This is standard template behaviour.

## Screenshots

Headless Chrome, `timeout 60`, `--timeout=15000 --virtual-time-budget=5000`, served on 127.0.0.1:9833. The 390 check used a 390 px iframe in a 500 px window. Files are under the scratchpad at `wr-shots/`: `w1440/w1024/w768/w390.png`, with slices `s1440_*.png` and `c1024_*`, `c768_*`, `c390_*`.

At every width, nothing is clipped or overlapping:
- the hero scenery, including the turbine tops;
- the facts table and the key row;
- the chart axis labels and the key note;
- the stratum corner labels;
- the request and commands blocks (commands wrap at 768 and 390);
- the folded frame and its guide;
- the notebook header, where `water_reservoirs.ipynb` and `gridflow_models` both fit at 390;
- the related notes.

## What the checker should look hardest at

1. **The key.** The code dedup `(timestamp_utc, area_code)` holds only per silver file. The page states this in `facts.grain`, the chart caption, the record caption and the notebook lead, and uses `published_at` as the third key column. Re-derive it: `pl.read_parquet(glob).group_by("timestamp_utc", "area_code").len()` gives 2, 3, 6 and 7.
2. **Thin-data wording.** Check that the caption's "No weeks stamped 9 to 30 August are drawn" reads as a description of the chart, not a local-coverage statement.
3. **"Weekly average" rests on the regulation quote now in the note body.** Check that the quote and the `[16.1.D]` link are enough evidence.
4. **x placement.** Check that the alt, x_label and key note agree: stamped at the week start, drawn mid-week.

## Defects (pasteable)

- **gridflow: silver not unique on its dedup key across files (water_reservoirs).**
  - The transformer dedups `(timestamp_utc, area_code)` per bronze day (`silver/entsoe/water_reservoirs.py:59`).
  - The connector sends one-day requests, and ENTSO-E returns the whole containing `P7D` week, so every daily partition repeats the week.
  - Local silver has 18 rows for 4 distinct weeks.
  - Consumers (`gridflow_models` `query()`) get duplicates unless they dedup on `published_at`.
  - Fix options: a week-aligned request window, or a cross-partition latest view.
- **gridflow: A72 zones fixed to a GB-centric list, only FR publishes.**
  - `DEFAULT_ZONES` (`connectors/entsoe/endpoints.py:395`) is used unconditionally (`client.py:249`).
  - `**params` cannot add a zone, because A72 has no `optional_params` (`client.py:306`, `endpoints.py:113`).
  - In bronze for Aug and Sep 2026, GB, NL, BE, DE-LU and IE-SEM return no-data acknowledgements on every request.
  - The hydro-rich zones (NO, SE, ES, IT, AT, CH) are unreachable.
- **gridflow: `quantity_Measure_Unit.name` never parsed.**
  - `parsers.py:286-360` has no branch for it, so silver `reservoir_mwh` asserts MWh without carrying the unit.
  - This matters if the vault's unsourced "some zones report percentage filling" is ever true.
- **gridflow (minor): within-file keep order.**
  - `unique(keep="last")` at `water_reservoirs.py:59` relies on `sorted(glob("raw_*.xml"))` order (`water_reservoirs.py:33`), not on `published_at`.
  - A re-run on the same day kept the later file (13 Sep partition) only because the filenames sort by fetch time.
- **Vault (fixed in this batch):** the note claimed a Nordic zone can be passed via `**params`, and the silver sample showed `resolution` as `7 days, 0:00:00`. Both are corrected, with citations.

## Nits fixed (after review APPROVE, `water_reservoirs-review.md`)

1. **`page.record.select.columns`:** now `[timestamp_utc, area_code, published_at, reservoir_mwh, resolution]`.
   - The sample was regenerated with `gridflow-sample`; the JSON column order is now `timestamp_utc, area_code, published_at, ...`.
   - Screenshot at 768 (`wr-shots/n768_frame.png`): the frame shows `timestamp_utc`, `area_code` and `published_at` before the fold, so the eight rows are told apart.
   - At 390 only `timestamp_utc` fits (template behaviour, as the review records).
2. **`page.how_used[1]`:** "Comparing each week with the same week a year earlier, as Article 16 intends." is now "Comparing a week with the same week a year earlier, both years ingested."
   - This drops the intent claim and signals that the prior-year figure is not in the rows.
3. **`page.chart_view.key[0].note`:** now "Weekly average in MWh, stamped at the week's start, Monday 00:00 Paris (22:00 UTC Sunday in CEST)."

Checks after the fixes:
- **Canonical note:** edited with Edit; CRLF kept (274 CR for 274 LF).
- **Mirror:** copied; `cmp` shows it identical.
- **Build:** `gridflow-build --only entsoe/water_reservoirs` gives no errors.
- **Detector:** only the accepted advisory `em-dash-overuse` (EIC padding).
- **Rendered HTML:** has 0 "Article 16 intends", 1 "22:00 UTC Sunday in CEST" and 1 "both years ingested".
- **Servers:** my 9833 server is stopped; I did not touch 9670.

Summary: all three nits are fixed and the note is mirrored; the sample was regenerated, and the build and detector are clean.
