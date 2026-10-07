# entsog/aggregated_physical_flows: author report

Writer: Opus 5.5 · high, 2026-10-07. Single page, `entsog/aggregated_physical_flows`. Built with `--only entsog/aggregated_physical_flows`.

## Recommendation: SHIP

The held capacity page's silver loss does **not** apply here. Every bronze record reaches silver:

| | Bronze records | Silver rows |
|---|---|---|
| 2026-08/09, 14 gas days (1 to 5 Aug, 13 to 21 Sep) | 42 (3 a day) | 42 (3 a day) |

Each aggregate record is one gas day long. Its `periodFrom` (06:00+02:00) has the fetched day as its local date, so `partition_records_to_target_date` (`silver/entsog/generic.py:157-161,332`; `silver/entsog/datetime.py:56-87,191-213`) keeps every record. In winter the offset would be +01:00 (05:00 UTC); the local date still equals the bronze day, so there is no loss then either. The partitions share one schema, the key is unique, and every `timestamp_utc` is 04:00 UTC. The 38-day gap between 5 Aug and 13 Sep is ingest coverage, not silver loss. Counts match DATA-MATRIX (42, 1 Aug to 21 Sep).

The data is thin, but it is accurate: one zone, one operator, one direction and three adjacent systems. The page says plainly that only five aggregates are requested, that three return rows, and that storage is entry only.

## Status

- **Build:** `gridflow-build --only entsog/aggregated_physical_flows` passes. The only warnings are the generic "no Pydantic class" notices. Output: `wrote: data-sources/entsog/aggregated_physical_flows.html (dataset template)`.
- **Detector:** the only finding is the `em-dash-overuse` advisory ("98 em-dashes"), which is accepted.
  - The text has 22 "--" runs: 18 are zone codes (`UK---------`, `UK-NI------`, in the request URL and the `bz_key` guide line and frame) and 4 are CLI flags (`--start`, `--end`). The prose has no dashes.
  - Real em dashes in the page: **0**.
- **Rubric greps** on the rendered text (locally, held, our, since 20, % of, live, now, yet, soon, planned, coming, real-time, digits followed by rows or days, →, middle dot, em dash): no hits.
- **Mirror:** copied with `cp` and checked with `cmp` after every edit, byte-equal, CRLF kept. Front matter has no literal `---`: the dash runs in the URL and the `bz_key` line are `\x2D` escapes in double-quoted strings (ruling 40). YAML round-trip asserted.
- **Artefacts:** no staged chart spec and no authored override existed.
  - `site/hifi/data/series/entsog/aggregated_physical_flows.json`: `spec_origin: vault`, 3 series × 9 points, 27 rows used out of 42 matched.
  - `site/hifi/data/samples/entsog/aggregated_physical_flows.json`. **Read this:** see "Sample artefact" below.
  - `site/hifi/data/notebooks/entsog/aggregated_physical_flows.json` plus `aggregated_physical_flows-6.png`. Written by `scripts/run_notebooks.py`: 6 cells (setup, help card, 4 own), no errors.
- **Sample artefact:** `gridflow-sample` cannot print any eight rows of this table.
  - `points_names` holds `|`-separated names on every row, for example `Isle of Grain|Milford Haven`.
  - `polars_text` (`src/gridflow_front_end/sample.py:67-87`) splits Polars' markdown table on `|` and fails: "a value contains '|'; Polars' table cannot be read back". No `record.select` can drop a column.
  - Following the capacity precedent, I ran `gridflow-sample`'s own `main()` from `scratchpad\apf\sample_pipe.py`. Only one thing changed: `polars_text` is wrapped so that `|` in String columns becomes U+E000 before Polars prints and is restored after the cells are read back. The selection, the payload code and `generated_by: gridflow-sample` are all the tool's own.
  - **The seat should fix `polars_text` (template problem 1) and rerun `gridflow-sample --dataset entsog/aggregated_physical_flows`.** I did not edit any Python.
- **Frame column order, on purpose:** `record.select.columns` prints `timestamp_utc`, `adjacent_systems_key` and `direction_key`, then `value`, `unit`, `count_point_presents`, `last_update_date_time` and `flow_status`, and only then the constant key columns `bz_key` and `operator_key`. At 1440 those two fold behind the ellipsis so that the stamp stays in view, following the brief's "name the columns that matter" rule. The guide still lists all five key columns first, under "Identifies a row".
- **Screenshots** (light only; the site has no dark theme), at 1440, 1024 and 768, and at 390 in a true 390 px iframe:
  - Location: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\apf\shots\`.
  - Files: `s_<width>_<n>.png`, contact sheets `sheet_390.png`, `sheet_768.png` and `sheet_1024.png`, and full pages `full_<width>.png`.
  - Nothing is clipped or overlapping at any width. That covers the hero and scenery (turbines whole), the facts with the Key, the chart (ticks 0 to 500M, x labels 13 to 21 Sep, the x_label), the three key entries, the request URL, the commands, the folded frame (8 columns at 1440, 4 at 768, 1 at 390), the guide, the notebook panel and related.
  - At 390 the long `pointDirection` wraps mid-token. This is the known template behaviour (capacity report, template problem 3).
  - The unfolded frame was not screenshotted; it uses the same template as nominations.
  - The static server on 9875 was started under `timeout 1500` and stops itself; 9670 was not touched. I removed the temporary 390 iframe helper `site/hifi/w390-apf.html` from the worktree.

## What the data is (the "look hardest at" answers)

- **Requested filters.** The connector sends five `pointDirection` filters in the aggregate-zone form `bzKey + operatorKey + directionKey + adjacentSystemsKey` (`connectors/entsog/endpoints.py:46-54`). The code calls them "deliberately narrow for GB zone data":
  - `UK---------IE-TSO-0001entryTransmissionUK-NI------` and the matching `exit` (GNI (UK), British zone, adjacent NI transmission);
  - `UK---------UK-TSO-0001entry` + `LNG Terminals`, `Production` and `Storage` (National Gas Transmission).
- **What comes back.** Every response returns three records: National Gas Transmission entry from `LNG Terminals`, `Production` and `Storage`. Both GNI (UK) filters return nothing, on all 14 days. Both are valid combinations in ENTSOG's `aggregate_interconnections` register (`id` `6UKUK---------IE-TSO-0001entry/exitTransmissionUK-NI------`). `meta.count` is 3 against `meta.total` 6 in every body: the same open question as the sibling pages.
- **What is not requested.** The `aggregate_interconnections` register (snapshot ingested 2026-09-27) lists 17 British-zone aggregates. The connector requests 5, so 12 are never asked for:
  - Storage exit;
  - `Distribution` and `Final Consumers` exits;
  - `Transmission` entry;
  - every cross-border aggregate (Ireland, Ireland+NI, Netherlands, IUK) in both directions.

  The table is therefore not a zone balance. The page says only that storage exit is not requested; the vault body lists the rest.
- **What one row is.** ENTSOG's daily physical flow for one balancing zone (`bz_key`), operator, direction and adjacent system. Each row also carries `points_names` (the points it covers) and `count_point_presents`.
- **Key and dedup.**
  - Dedup is on the vendor `id`, `keep="last"`, per daily bronze read (`generic.py:193-199`).
  - `id` joins data set, country, zone, operator, direction, adjacent system, midnight-UTC date labels (`2026-09-21T00:00:00+00:00…`, which differ from `periodFrom`) and the indicator.
  - The 5-tuple `(timestamp_utc, bz_key, operator_key, direction_key, adjacent_systems_key)` has 0 duplicate groups.
  - Days: 3 rows on each of 14 gas days, none missing within 1 to 5 Aug or 13 to 21 Sep, none repeated.
- **Units.** `unit` is `kWh/d` on all 42 rows. The generic transformer does not convert: `generic.py:189-191` casts `value` (and `count_point_presents`, `_NUMERIC_NAMES` `:80-93`) to Float64 and leaves units alone. The chart axis is kWh/d with compact ticks. `physical_flows` converts to GWh/d, and the page says so.
- **Gas day as stored.**
  - `timestamp_utc` is a copy of `period_from` (`generic.py:185-187`): the gas-day start, sent as 06:00+02:00, which is 04:00 UTC on every row. The x_label is scoped to "starting 04:00 UTC here".
  - `last_update_date_time` is the vendor's `lastUpdateDateTime` in UTC, not used by the pipeline. `ingested_at` is the silver transform time (`generic.py:201-206`). No stamp is a publication or issue time.
- **`lastUpdateDateTime`.** It falls 108 to 158 h after the gas-day start. All three rows of a gas day share one stamp. Gas day 16 Sep shares 14 Sep's stamp (2026-09-20 16:30:29 UTC), and 21 Sep shares 19 Sep's (2026-09-25 17:42:15 UTC), which is visible in the eight rows. Unexplained.
- **`flowStatus`.** `Provisionnal` (the vendor's spelling) on every row. The point-level rows say `Provisional`.
- **What "aggregated" means.** Neither the canonical note nor the vendor README or endpoints.md quotes any ENTSOG definition. The only vendor words are `dataSetLabel` `Aggregates`, `pointsNames` and `countPointPresents`. The page therefore defines nothing beyond those words and the project check below, and the vault body says no definition is quoted. I did not read the API PDF.
- **Aggregate against the sum of `physical_flows` points (observation, project check).**
  - For every one of the 42 rows, `value` equals the sum of `flow_gwh_per_day` × 10^6 over the `pointsNames` points' National Gas TSO (`UK-TSO-0001`) entry rows in `entsog/physical_flows` for the same gas day. The largest absolute difference is 0.0 (exact to the kWh).
  - All 13 named points (Production 4, Storage 7, LNG 2) exist in `physical_flows` at 04:00 UTC.
  - The notebook reproduces this for 13 to 21 September ("largest gap, GWh/d": 0.0 for all three systems). The caption ("as the notebook shows") and `what_it_is` ("in the notebook, each equals its points' sum there") are both scoped to that output.
- **`countPointPresents` against `pointsNames`.**
  - Storage names 7 points (Aldbrough, Avonmouth LNG, Cheshire Storage, Hatfield Moor Storage, Hole House Farm, Hornsea, Humbly Grove), but `countPointPresents` is 6.
  - Avonmouth LNG (`LNG-00053`) is in `physical_flows` at the same 04:00 UTC stamp with `value` null as sent (`flowStatus` `Provisional`, no remark) on all 14 days.
  - So the count appears to cover points that sent a value; Burton Point counts while sending 0. ENTSOG does not say this. LNG (2 names, 2) and Production (4 names, 4) agree.
  - The guide line states only what the rows show: "6 for storage, which names seven points".
- **Teesside.** `pointsNames` lists Teesside under `Production`; in `physical_flows` it is `LNG-00007`, whose vendor `pointType` is "Aggregated production point - TP ExtEU", so the placement is consistent (explained in round 2).
- **Storage zeros.** Storage entry is 0 as sent on 6 of 14 days (corrected in round 2) (15 and 18 to 20 Sep in the chart window). Every named storage point sends 0 on those days (Avonmouth null). This is entry into the zone only; injection would be the unrequested Storage exit aggregate. The page says "0" and "entry from storage only", never "no withdrawal" or "net".
- **How this differs from `physical_flows`**, stated on the page in `what_it_is`, the caption and related:
  - one row covers several points, by adjacent system, against one row per point and operator;
  - values stay in kWh/d, against GWh/d;
  - gridflow sends five zone filters, against no filter at all for the point-level fetch.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| No silver loss; ship (whole page) | Bronze 3 records/day × 14 days = 42; silver 42 rows, 1 schema; `generic.py:157-161,332`; `datetime.py:191-213` (local date of `periodFrom`) |
| Request URL (`raw_feed.requests`) | `request_url` in bronze `2026/09/21/raw_20260926T174539Z_2698b090.meta.json`, copied verbatim (`Physical+Flow`, `LNG+Terminals`, `%2C`) |
| "One request per day … five zone filters" (`raw_feed.note`) | `client.py:78-102` (`day_subwindows`, one `from=to=D` call per covered day); `endpoints.py:48-54,168-180` |
| "the two GNI (UK) filters for Northern Ireland return no rows" | All 14 bronze bodies: 3 records, none with `IE-TSO-0001`; `aggregate_interconnections` silver lists both combinations |
| Commands: ingest `--end 2026-09-22` exclusive, transform `--end 2026-09-21` inclusive | `day_subwindows` half-open (`utils/time.py:123-153`); same as the approved physical_flows and nominations pages |
| "Silver keeps `value` and `unit` unconverted"; kWh/d (summary, `what_it_is`, `unit` line, chart unit) | `generic.py:189-191`; `unit` `kWh/d` on 42/42 rows |
| Grain and key (`facts.grain`, `record.key`) | Dedup on `id` (`generic.py:193-199`); 5-tuple 0 duplicate groups |
| x_label "gas day, starting 04:00 UTC here"; `timestamp_utc` line | `generic.py:185-187`; all 42 rows at 04:00 UTC |
| "three return rows, all National Gas Transmission entry: production, storage and LNG terminals" (`what_it_is`) | Silver `operator_key` UK-TSO-0001 ×42, `operator_label` "National Gas Transmission", `direction_key` entry ×42, three `adjacent_systems_key` values |
| "in the notebook, each equals its points' sum there" (`what_it_is`); "Each value equals its named points' sum in `physical_flows`, as the notebook shows" (caption) | Notebook cell 5 output: largest gap 0.0 for LNG Terminals, Production and Storage over 13 to 21 Sep; my 42-row join (all exact) |
| Chart alt and key-note numbers | Committed series: production 322,977,312; 356,287,010; 427,221,235; 442,996,575; 449,602,261; 452,816,220; 434,975,163; 433,035,977; 383,537,205. Storage 134,058,118; 72,026,868; 0; 23,003,243; 16,008,476; 0; 0; 0; 378,788,337. LNG 54,248,476; 63,905,474; 71,911,354; 71,944,652; 54,259,575; 54,254,024; 54,248,476; 54,248,476; 113,764,382 |
| Key notes: production and LNG point names | Silver `points_names` (Bacton (UKCS)\|Barrow\|Burton Point\|Teesside; Isle of Grain\|Milford Haven) |
| "Storage exit is not requested" (key note, `how_used`) | `endpoints.py:48-54` (entry only for storage); register lists `UK-TSO-0001 exit Storage` |
| `count_point_presents` line "6 for storage, which names seven points" | Eight rows: storage `count_point_presents` 6.0 and the seven names in `points_names` |
| `last_update_date_time` line "one stamp per gas day here" | Eight rows: one stamp per gas day; silver `n_unique` = 1 per day on all 14 days |
| `flow_status` line `Provisionnal` | Silver `flow_status` `Provisionnal` ×42 |
| `data_set` "`1`", `data_set_label` `Aggregates`, `year`/`month`/`day` as text, month without a leading zero | Silver dtypes (String) and values ("1", "Aggregates", "9") |
| `id` line "zone, operator, direction, system and dates joined" | Silver `id` `1AggregatesUKUK---------UK-TSO-0001entryLNG Terminals2026-09-21T00:00:00+00:002026-09-22T00:00:00+00:00Physical Flow` |
| `adjacent_systems_key` "`Production` or `Storage` here" | The eight rows' values; no ENTSOG definition is given, so the line states only what the rows show |
| `notebook.lead` (two relations, `timestamp_utc`, ends included, lineage dropped) | `silver/schema_manifest.py:194` (`timestamp_utc`); same `query()` path as the approved pages; both queries ran |
| `plot_alt` | `aggregated_physical_flows-6.png` (axis offset 1e8) and cell 4 output table, same values as the series |
| Eight rows and caption | Sample: gas days 18 to 21 Sep, `Production` and `Storage`, shape (8, 34); LNG rows are excluded by the filter, and the caption says so |
| Related: physical_flows in GWh/d; register pages | `physical_flows` silver `flow_gwh_per_day`, `unit` GWh/d; `entsog.json` lists `aggregate_interconnections`, `balancing_zones` and `connection_points` (reference-data family) |

## Body corrections (canonical note, smallest spans)

Applied by `scratchpad\apf\fix_note.py`: count-asserted replacements, CRLF kept, with the schema table and sample generated from silver.

1. **Overview.**
   - Added what a record is, with the unit and `pointsNames`/`countPointPresents`.
   - Added "No ENTSOG definition of the aggregate is quoted here".
   - Added the project check (value equals the sum of the named points in `physical_flows`, 42/42).
   - Added a pointer that only five aggregates are requested.
2. **Historical depth** TODO becomes "Not vendor-documented here".
3. **Publication lag** TODO becomes "Not vendor-documented here", with the scoped `lastUpdateDateTime` lag (108 to 158 h, one stamp per gas day) and `Provisionnal`.
4. **Query parameters.**
   - Added the `indicator` and `periodType` rows the connector sends (`endpoints.py:168-180`).
   - The `pointDirection` example said "see Working curl example", but the curl sends none. It is now a real filter, with `endpoints.py:46-54`.
5. **Dedup key.** "`(id)` if present, else all non-`timestamp_utc` columns" becomes the vendor `id`, `keep="last"` (`generic.py:193-199`), with the 5-tuple's uniqueness. Added a **Bronze read filter** line (none dropped, 42/42).
6. **Point-in-time field.** `last_update_date_time` becomes "none used by the pipeline" (`generic.py:181-183,201-206`).
7. **Silver schema.** Regenerated in silver's column order:
   - added `timestamp_utc`;
   - fixed the broken `id | str | int` and `data_set | str | int` cells that split the table;
   - noted `count_point_presents` as text cast to Float64 and `unit` unconverted;
   - replaced a raw `|` in a cell with words.
8. **Silver sample.** It was a bronze-shaped record (+02:00 stamps, `"count_point_presents": "2"` string, May dates). It is now a real 21 Sep silver row in UTC.
9. **Known issues.**
   - `adjacentSystemsKey` bullet: added `Final Consumers`, `Transmission` and the `Transmission<bzKey>` forms from the register.
   - The generic `pointDirection` bullet (`operatorKey + pointKey + directionKey`) contradicted the aggregate-form bullet above it. It now says `/aggregatedData` uses the aggregate form.
   - Added: requested against returned; not requested (17 against 5); the sum identity (project check); `countPointPresents` against `pointsNames`; Teesside under `Production`; shared update stamps; zero storage entry.
10. **Modelling notes** TODO becomes four notes: unit conversion, storage is entry only, provisional and late stamps, how to join to the points.

Left unchanged: the bronze sample and curl example (valid vendor examples, though the curl sends no `indicator` or `pointDirection`), and the "Indicator: `Physical Flow` (only indicator served by `/aggregatedData`)" row, which is not verified (see below). I also left the inapplicable boilerplate bullets that apply to other families (`isCamRelevant` casing, `directionKey` casing in CMP): they are true of ENTSOG, harmless here, and outside the smallest span.

## Not verified

- **ENTSOG's definition of an aggregate**, and of `countPointPresents`. Neither is quoted anywhere I read. The page uses only the vendor field names and the measured sum.
- **"`Physical Flow` is the only indicator served by `/aggregatedData`"** (vault API table). This is pre-existing and was not checked.
- **What `meta.total` 6 counts** against `meta.count` 3.
- **Why the two GNI (UK) NI filters return nothing** (no flow at that boundary, or a reporting gap).
- ~~Why Teesside sits under Production~~: explained by the vendor `pointType` (round 2).
- **Whether a later fetch revises values.** Every row is `Provisionnal`, and no re-fetch exists to compare.
- **Why gas days share update stamps** (16 with 14 Sep, 21 with 19 Sep).
- **The unfolded frame** was not screenshotted.

## Open questions

1. Should the connector request more of the zone's 17 aggregates? Storage exit, distribution and final-consumer exits and the interconnection aggregates would make a zone balance possible. Should it drop the two NI filters that never return?
2. Should the page wait for a wider request set to show a storage net or a zone balance, or ship as is? My recommendation is ship: the page is accurate about what it holds.
3. Should `flow_status` `Provisionnal` be normalised to `Provisional` in silver, or kept as sent (current behaviour)?

## Template problems

1. **`gridflow-sample` cannot print a table whose values contain `|`** (major for this page; it blocks the official sample). `sample.py:67-87` reads Polars' ASCII_MARKDOWN table back by splitting on `|`. `points_names` contains `|` on every row, and `record.select` has no way to drop a column.
   - Suggested fix: mask `|` in String columns before printing and restore it in the parsed cells, as `scratchpad\apf\sample_pipe.py` does; or build the cells with `pl.Config` formatting per column instead of parsing the table.
   - The committed sample must be regenerated with the fixed tool.
2. **The long `pointDirection` query parameter wraps mid-token at 390** (cosmetic, as in the capacity report).
3. **Build warnings name the wrong module** ("gridflow.schemas.elexon" for ENTSOG), as other writers reported. There is also no dark theme to check.

## Defects

- **[front-end tool] `gridflow-sample` fails when any value contains `|`.** `src/gridflow_front_end/sample.py:67-87` (`polars_text`) splits Polars' markdown table on `|`. `entsog/aggregated_physical_flows.points_names` is `|`-separated on every row, so no eight rows can be sampled ("a value contains '|'; Polars' table cannot be read back"). The committed `samples/entsog/aggregated_physical_flows.json` was produced by the tool's own `main()` with `|` masked during printing, and must be regenerated once `polars_text` is fixed.
- **[gridflow connector, scope] `aggregated_physical_flows` requests 5 of the 17 British-zone aggregates, and 2 of the 5 never return.**
  - `DEFAULT_AGGREGATED_POINT_DIRECTIONS` (`connectors/entsog/endpoints.py:48-54`) asks for National Gas TSO entry from LNG Terminals, Production and Storage, plus GNI (UK) entry and exit at the NI transmission boundary.
  - In 2026-08/09 bronze (14 gas days), both GNI (UK) filters return no record, though both exist in `aggregate_interconnections`. `meta.count` is 3 against `meta.total` 6.
  - Never requested: Storage exit, Distribution and Final Consumers exits, Transmission entry, and every cross-border aggregate (Ireland, Ireland+NI, Netherlands, IUK) in both directions.
  - The table cannot give a zone balance or net storage flow.
- **[vendor data, observation] `countPointPresents` is below the number of `pointsNames`.** British zone Storage entry names 7 points, but `countPointPresents` is 6 on all 14 gas days of 2026-08/09. Avonmouth LNG (`LNG-00053`) sends a null physical flow at point level on every one of those days. Undocumented meaning.
- ~~Teesside listed under `Production`~~: withdrawn in round 2; vendor `pointType` "Aggregated production point - TP ExtEU" explains it.
- **[vendor data, observation] Shared `lastUpdateDateTime` across gas days.** Gas day 2026-09-16 carries the same stamp as 2026-09-14 (2026-09-20 16:30:29 UTC); 2026-09-21 the same as 2026-09-19 (2026-09-25 17:42:15 UTC). All three records of a gas day share one stamp. Unexplained.
- **[vendor data, observation] `flowStatus` `Provisionnal`** (vendor spelling) on every aggregate record, against `Provisional` on the point-level rows. Kept as sent in silver.
- **[vault, fixed in this branch] The aggregated_physical_flows note was wrong or empty in several places:**
  - TODO historical depth, publication lag and modelling notes;
  - a broken `id | str | int` / `data_set | str | int` schema table with no `timestamp_utc`;
  - a bronze-shaped silver sample with +02:00 stamps;
  - "point-in-time field `last_update_date_time`";
  - a `pointDirection` bullet giving the `/operationalData` point form, which contradicted the aggregate form;
  - no `indicator`/`periodType` parameters;
  - no statement of what is requested against returned.

  All are corrected with code citations.
