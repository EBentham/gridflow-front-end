# congestion-management: checker review

Family page `congestion-management`. The lead is `redispatching_internal`; the members are `redispatching_cross_border`, `countertrading` and `congestion_management_costs`. Checker: Opus 5.5 · high, 2026-09-29. Screenshot port 9849 (server stopped).

## Verdict: REVISE

There is 1 major finding and 5 nits. The page itself is sound:
- every fact that carries weight was reproduced against code, silver and bronze;
- the chart matches silver point for point;
- the direction loss is stated plainly and scoped.

The only major is stale text in the costs note body, under seat ruling 2. It is a one-line fix and needs no rebuild or re-distil: the page does not render the costs note body.

## Findings

1. **major: `congestion_management_costs.md` body, Known issues, last bullet (lines 183 to 184).**
   - **What is wrong:** the sentence "(On 2026-09-29 the local catalogue had no `silver_entsoe_congestion_management_costs` view, so `data.entsoe.query()` could not be run against this table.)" is stale. Under seat ruling 2, the view now exists.
   - It is also a statement about the local catalogue, which does not belong in a vendor note.
   - **Fix:** delete the parenthetical. Keep the "start the range a day earlier" advice, which is correct: `query()` filters `timestamp_utc >= start 00:00 UTC` (`gridflow_models/.../_get_method_registry.py:94-96`), so a 1 July start misses July's row at 2026-06-30T22:00Z and keeps the false 30 July row.
   - Then re-mirror the note byte for byte.
   - **Evidence:**
     - `tr -d '\r' < congestion_management_costs.md | grep -n "could not be run"` gives line 184.
     - No other note and no page text says `query()` fails: a grep for `catalog|query\(\) fails|raises` over all four notes and the rendered HTML found only this one.
   - The writer's report (`congestion-management-author.md`, `query()` bullet and defect 6) carries the same stale claim. It is not an artefact, but the seat should not paste defect 6 into BACKLOG as still open.

2. **nit: `page.chart_view.caption`, "Replies carry up and down series".**
   - **What is wrong:** it reads as a universal and is broader than the evidence.
     - NL replies do carry both directions.
     - BE silver has 0 quarter-hours where both directions exist.
     - Cross-border and countertrading replies carry `A02` only.
   - The rest of the caption is correct: "silver keeps one per quarter-hour" is a code fact (`h6_market.py:91-99`), and "here every point is the down (`A02`) series" is scoped.
   - **Fix:** "Replies can carry separate up and down series" (or "Netherlands replies carry...").
   - **Evidence:** in the silver-to-bronze join (method under Direction, below), BE rows have `both`=0, `A01only`=119 and `A02only`=62. Bronze reply direction sets: cross-border `{A02}` in 4 of 4, countertrading `{A02}` in 2 of 2.

3. **nit: `page.family.members[redispatching_cross_border].differs` and `[countertrading].differs`.**
   - **"most replies are empty" / "mostly empty replies":** this is a proportion measured on our bronze (4 of 624 and 2 of 72 files are populated). It sits close to the rubric's no-local-coverage rule.
     - The notes do record Acknowledgements ("No matching data found") from live probes as vendor behaviour, so this is defensible.
     - A vendor-behaviour wording avoids the proportion, for example "many replies are an Acknowledgement with no data".
   - **"naming the line" (cross-border):** the line is in the reply's `location.name` (`HORTA DOEL`), which silver drops. Adding "(not kept in silver)" would stop a reader looking for it in the table.
   - **Evidence:** bronze scan: every populated cross-border TimeSeries carries a `location.name`; `h6_market.py:107-117` output columns.

4. **nit: `page.record.fields.quantity_mw`, "holds until the next point".**
   - **What is wrong:** the parser has already forward-filled `A03` points into one row per quarter-hour (`parsers.py:578-600`), so every silver row is its own interval. The phrase suggests the reader must fill forward.
   - **Fix:** "forward-filled from the last point sent (`A03`)".
   - **Evidence:** window silver has 672 rows, one per quarter-hour, with no gaps. Cross-border bronze sends 3 Points per Period, yet silver has 288 quarter-hour rows.

5. **nit (no action unless the seat wants it): `page.raw_feed.note`, "the Netherlands returns under three pairs".**
   - This is true in every populated bronze reply: `GB/NL` gives NL 21 times, `NL/DE-LU` 21, `NL/BE` 16, and 5 more `NL/BE` replies carry both NL and BE series.
   - However, it is an observation of vendor behaviour, not a documented rule. It is acceptable as written; it is noted only because a vendor change would make it stale.

6. **nit: `page.facts.grain`, "One row per interval start, `in_Domain` zone, `out_Domain` zone and business type".**
   - **What is wrong:** this matches the dedup key (`h6_market.py:91-99`) for the lead and the two other quantity members. For costs, the dedup runs per daily partition, so the table holds each key once per partition: 744 rows for 24 keys.
   - `what_it_is` already says silver copies costs into every daily partition, so a careful reader can reconcile the two.
   - **Fix (optional):** add "per daily partition" or "(costs: per daily partition)".

## What was checked and held

### Direction (look-hard 1), reproduced

- **Method:** I parsed all 168 bronze XML files with gridflow's own `parse_timeseries_xml(value_tag="quantity")` and grouped by key plus `flow_direction`, then left-joined `A01` and `A02` onto silver by `(timestamp_utc, in_area_code, out_area_code, business_type)`.
- **Parsed rows:** 22,431 rows give 2,101 keys and 4,021 key+direction pairs. No key+direction has two values.
- **NL:** 1,728 rows, all equal to `A02`. `A01` is present for all 1,728 and differs in 1,013.
- **Chart window (15 to 21 Sep):** 672/672 equal `A02`, and `A01` differs in 476.
- **BE:** 181 rows. 119 are `A01`-only (8 Sep 86, 15 Sep 21, 17 Sep 12), 62 are `A02`-only (4 Aug 16, 5 Aug 46), and none has both.
- **What this confirms:**
  - The key note "The up (`A01`) series for the same quarter-hours is not in silver" is accurate, plain and scoped to the chart's quarter-hours.
  - `what_it_is`, "Up and down arrive as separate series; silver keeps no direction column", holds against `parsers.py:316-319` and `h6_market.py:107-117`.
  - The up/down reading of `A01`/`A02` is a code fact (`activated_balancing_qty.py:24`).
- The lead note's Known-issues bullet matches the numbers above.

### Units (look-hard 2)

- The value reads "as sent" everywhere: `MWH` for A63 (caption, alt, `plot_alt`, the lead's `differs`, the guide, the notebook y-label "MWH as sent", the chart axis "MWH") and `MAW` for A91 (countertrading `differs`).
- There is no standalone "MW" in the page block or the rendered HTML; the only matches are the column name `quantity_mw`.
- **Bronze:** `quantity_Measurement_Unit.name` is `MWH` on all 279 internal and 6 cross-border TimeSeries, and `MAW` on all 12 countertrading TimeSeries.

### Costs (look-hard 3)

- **Silver, reproduced:**
  - 744 rows = 24 distinct keys × 31 copies; every key's count is 31, and key+value pairs number 24.
  - 9 keys at 2026-07-30T22:00Z duplicate July's values.
  - That leaves 15 real values, matching the writer's table, for example NL July `A46` 16,882,788.28.
- **The page never counts copies or shows a costs row.**
  - `what_it_is`, "which silver copies into every daily partition", is a code fact: the event-window exemption (`_event_window.py:201-204` and the `CongestionManagementCostsTransformer` with no `EVENT_WINDOW_FILTER`), per-partition dedup (`h6_market.py:91-99`), and the vendor returning the whole month per daily request (the note's live-probe callout).
  - "some months gain a false second point" is a code fact: `_add_months` clamps and steps from the UTC start (`parsers.py:54-63, 76-93`), and the `A03` fill runs until `timestamp >= end_dt` (`parsers.py:578-600`).
- **The note rule "any month following a shorter month is affected" checks out by hand:** Mar, May, Jul, Oct and Dec are affected; Jan, Feb, Apr, Aug and Nov are not.

### Chart (look-hard 4)

- **Provenance:** the committed series is `spec_origin: vault`, 1 series (`netherlands`) × 672 points, unit `MWH`, aggregation `last`, window 15 to 21 Sep. There is no staged spec under `chart-specs/entsoe/` and no authored override.
- **Against silver:** an outer join of the series with silver NL rows in the window gives 672 rows, 0 value mismatches and 0 nulls.
  - Min 0, max 84.0 at 18 Sep 19:00 to 19:45.
  - Zero runs: 15 Sep 00:00 to 04:45, 07:00 to 07:45, 15:00 to 15:45 and 18:00 to 22:45; 16 Sep 04:00 to 07:45 and 15:00 to 22:45; 21 Sep 15:00 to 23:45.
  - Daily minima on 17 to 20 Sep: 38.75, 63.75, 62.5 and 32.5.
  - Every number in the alt and `plot_alt` is correct.
- **Point-time and cadence wording:**
  - The `timestamp_utc` line says "period start plus (position minus 1) times resolution", matching `parsers.py:530/582`.
  - Cadence reads "quarter-hourly (`PT15M`) as sent", and resolution reads "`PT15M` in these rows".
  - The x-label is "UTC, quarter-hours".

### Thin members (look-hard 5)

- Silver:
  - cross-border: 288 rows, NL to BE only, 2026-07-06 22:00 to 07-09 21:45 UTC, values 0 to 1.25;
  - countertrading: 12 FR to DE-LU quarter-hours on 22 and 25 Sep, values 300 and 150;
  - costs: 15 real values.
- The page shows none of these members' data and states no trend. The member `differs` lines are request-shape facts. Plainness is acceptable; see nit 3 for wording.

### Rest of the rubric

- **Requests:** host, path, parameter names and order match bronze `.meta.json` `request_url` and `endpoints.py:164-189`.
  - Internal, cross-border and countertrading use `zone_pair` over `_FLOW_PAIRS` (`client.py:40-49`, `211-227`).
  - Costs uses `zone` with `in_Domain == out_Domain` over `DEFAULT_ZONES` (six, `endpoints.py:395`).
  - The `%2D` encoding follows the precedent on `total_capacity_allocated` and `cross_border_flows`.
- **Commands:** ingest 15 to 22 (end excluded) and transform 15 to 21 (end included) fit the writer's `day_subwindows` evidence, and there are no `PARTITION_SOURCE_OFFSETS`.
- **`notebook.lead`:** matches `source.py:401-451`: relation `silver_entsoe_redispatching_internal`, `timestamp_utc`, both ends inclusive via the half-open UTC instant, bitemporal columns excluded, pandas.
- **Notebook outputs:** per-day `above_zero` and `peak` (48/80.00, 48/70.50, 96/82.75, 96/84.00, 96/71.50, 96/71.25, 60/66.25) equal my Polars per-day table. There are no errors.
- **Artefact origin:** the samples JSON has `generated_by: gridflow-sample`, and the notebook JSON has `generated_by: scripts/run_notebooks.py`. The notebook has no `refresh`, `backfill` or ingest call and no error output.
- **Frame:** the eight rows are real (NL, 18 Sep 18:15 to 20:00). The guide covers every non-pipeline column, key columns first.
- **Build and detector:**
  - `gridflow-build --only entsoe/redispatching_internal` exits 0 with no deferred error now.
  - Its only warnings are the three legacy "silver schema rows empty" lines.
  - The detector shows only the accepted `em-dash-overuse` advisory (EIC padding).
- **Leakage and filler:** a grep of the rendered page for locally, held, "our ", "since 20", rows, "% of", "N days", live, now, real-time, em dash, `→` and `·` finds only template strings (the frame aria-label and the help card). `related` notes are all 12 words or fewer.
- **Vault body edits:** all four diffs against `origin/master` are small, cite `file:line`, and replace synthetic samples with real rows. The only problem is finding 1.
- **Mirrors:** `cmp` shows all four notes byte-identical to `vault/entsoe/`.

### Screenshots

- **Method:** CDP headless Chrome at 1440, 1024, 768 and 390, using a true device-metrics viewport, every call under `timeout 60`.
- **Nothing clipped or overlapping.** `scrollWidth` equals the width at every size, including with the frame unfolded (`#fx`) and the notebook open. I looked at the hero scenery with the turbine tops whole, the chart and key, the raw-feed boxes (the long `%2D` parameters wrap inside their boxes at 390), the frame folded and unfolded, the guide, the notebook panel with the plot loaded (690 px at 1440, 300 px at 390), related, and every stratum's corner label.
- The `[3]` output table at 390 sits in `.df-wrap` with `overflow-x: auto` (300 against 547 px), so it scrolls rather than clips. The `.ipynb` tab clip at 390 is the known template item.
- The site defines no dark theme, so light and dark render the same.
- Some captures loaded only part of the page (`readyState` stuck at `loading`, with connection resets in the server log from killed Chrome processes). That is a serving artefact of my local server, not a page fault; complete loads render all six strata.
