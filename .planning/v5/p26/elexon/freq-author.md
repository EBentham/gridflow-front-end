# elexon/freq: author report

Writer: Opus 5.5 (high), 2026-09-28. Page: `site/hifi/data-sources/elexon/freq.html` in the p26-elexon worktree.

## Status

- `gridflow-build --only elexon/freq`: passes for freq. The first runs failed only on another writer's
  `temp: page.raw_feed.note: 32 words` error (the build checks the whole vendor). A retry succeeded once
  that was fixed: "wrote: data-sources/elexon/freq.html (dataset template)".
- `detect.mjs --json`: `[]`.
- Mirror `vault/elexon/freq.md`: byte-identical to the vault worktree note (`cmp`). The note is still CRLF
  (`file` reports CRLF line terminators).
- Artefacts:
  - `site/hifi/data/series/elexon/freq.json`: `gridflow-distil`, `spec_origin: vault`, 1,440 points;
    provenance `rows_matched 1441`, `duplicates_dropped 1`.
  - `site/hifi/data/samples/elexon/freq.json`: `gridflow-sample`, 8 rows.
  - `site/hifi/data/notebooks/elexon/freq.json` and `freq-5.png`: `scripts/run_notebooks.py`, 5 cells, no
    errors.
- No staged chart spec and no authored override existed for freq in the worktree, so there was nothing
  to delete.

## Chart

- Type: `line` of `frequency_hz`, native 15-second samples, not aggregated (`aggregation: last`, one
  value per timestamp).
- Window: 17 September 2026, 00:00 to 06:00 UTC. The spec uses `window` 2026-09-17 plus the filter
  `timestamp_utc ge 00:00Z, lt 06:00Z`, and dedups on `timestamp_utc` because the midnight sample sits in
  two day files.
- Series: low 49.755 Hz at 03:13:15 UTC, high 50.208 Hz at 01:00:15 UTC. I read both values from the
  committed series JSON.

## Template problems: fixed by the seat (commit a0e18d9)

My first pass reported two renderer problems. The seat fixed both, merged the fix into this branch,
and I rebuilt:

1. **Zero baseline.** Line charts used to force a zero baseline (`chart_svg.py` `_lines`, formerly line
   377), which drew frequency flat on a 0 to 60 axis. The axis now fits the data:
   - wide chart: 49.7 to 50.3 Hz, in steps of 0.1;
   - narrow (390) chart: 49.6 to 50.4 Hz, in steps of 0.2.
2. **Time ticks.** The time axis used to tick only at midnights. It now carries hourly ticks:
   - wide chart: 00:00 to 05:00;
   - narrow (390) chart: 00:00, 02:00 and 04:00.

Rewording after the fix (coordinator request):
- **Caption:** the sentence about the zero-start axis is removed. I first wrote "The axis spans only 49.7
  to 50.3 Hz", then removed that too, because the narrow chart's axis runs 49.6 to 50.4.
- **Alt:** now describes the drawn shape without a width-specific range: "on an axis spanning a few
  tenths of a hertz either side of 50. The line wanders either side of 50 Hz in every hour, peaking at
  50.208 Hz at 01:00:15 UTC. Its lowest point is a dip to 49.755 Hz at 03:13:15 UTC, back above 49.9 Hz
  by 03:17:30."
- **Checked against the committed series:** in each of the six hours, min < 50 < max. The first value
  above 49.9 after the low is 49.911 at 03:17:30.

Not a defect, for the record: at 390 px the unit label "Hz" has a glyph box 2 px above the narrow
SVG's top edge. The SVG has `overflow: visible`, and the label draws whole.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Endpoint and params: `/datasets/FREQ`, `measurementDateTimeFrom`/`To`, paginated (`raw_feed.requests`) | `connectors/elexon/endpoints.py:103-110` |
| One 24-hour window per call; ingest loops `while current < end` (`raw_feed.note`, ingest comment) | `connectors/elexon/client.py:93-99`, `endpoints.py:40` `max_chunk_hours: int = 24` (freq does not override it) |
| Request formatted as `2026-09-17T00:00:00Z ... &page=1`, with no `format` param | bronze meta `C:\gridflow-data\bronze\elexon\freq\2026\09\20\raw_20260926T183331Z_d91c4d1b.meta.json`: `request_params` has only From, To and page |
| The response includes the sample at the `To` instant (`what_it_is`, `facts.grain`) | the same bronze body: the first record is `measurementTime` 2026-09-21T00:00:00Z for a From/To of 20T00:00 to 21T00:00; `total_pages: 1` |
| Each silver day file runs D 00:00:00 to D+1 00:00:00, so a midnight appears in two files, with equal values where both files exist (`facts.grain`, `notebook.lead`) | Polars read of the 14 files: each has 5,761 rows, from D 00:00 to D+1 00:00; the 12 duplicated midnights have identical `frequency_hz`. The page says "can sit", scoped. |
| Dedup on `timestamp_utc` runs per transform date only | `silver/elexon/freq.py:83` `df.unique(subset=["timestamp_utc"], keep="last")`; `read_bronze(target_date)` reads one bronze day, `freq.py:27-51` |
| `timestamp_utc` is parsed from `measurementTime` (or `reportDateTime`) as sent, UTC (`record.fields`) | `freq.py:57-81` |
| `frequency_hz` comes from `frequency`, cast to Float64 (`record.fields`) | `freq.py:60, 79` |
| The schema bounds values to 49.0 to 51.0 Hz; a breach is counted, not dropped (`what_it_is`, fields) | `schemas/elexon.py:213` `Field(ge=49.0, le=51.0)`; `silver/base.py:2022-2029` "Never raises and never drops a row" |
| Key `timestamp_utc` | `freq.py:25` `ENTITY_KEY_COLUMNS = ("timestamp_utc",)` |
| No partition source offsets; transform day D reads bronze day D (the commands' window) | `silver/base.py:417` default `(0,)`; freq does not override it |
| Transform `--end` is inclusive | `pipeline/runner.py:1125-1138` "date taken, inclusive", `date_range(start, end)` |
| CLI form `gridflow ingest elexon freq --start --end` | `cli.py:186-190` (source and dataset positional; `--start`/`--end` options) |
| Cadence of 15 seconds (`facts.cadence`) | visible in the eight rows (03:12:30, 03:12:45, and so on); the page scopes it to "as in the rows below" |
| `query("freq", ...)` reads `silver_elexon_freq`, filters `timestamp_utc` as half-open UTC days (the end day whole), orders by it and drops lineage (`notebook.lead`) | `gridflow_models/research/handles/source.py:401-455`; `_get_method_registry.py:94-96`; `_relation_name_for_dataset('freq')` returned `silver_elexon_freq`, date column `timestamp_utc` (run); `schema_manifest.py:119` |
| The view is a plain parquet glob, so the midnight comes back twice (`notebook.lead`) | `gridflow/storage/duckdb.py:444-447` `SELECT * FROM read_parquet(..., hive_partitioning=true, union_by_name=true)`; notebook cell 4 output shows `2026-09-17 01:00:00+01:00` twice with 49.970 |
| "Times print in local time" (`notebook.lead`) | notebook output timestamps are `+01:00`; the plot's axis runs 01:00 to 01:00 |
| Chart low and high, alt and key note | series JSON: min 49.755 at `2026-09-17T03:13:15Z`, max 50.208 at `2026-09-17T01:00:15Z`, 1,440 points |
| `plot_alt`: 49.755 to 50.219 Hz, lowest just after 04:00 on the UTC+1 clock | Polars over 17 Sep: min 49.755 at 03:13:15 UTC, max 50.219 at 07:05:30 UTC; the PNG was viewed |
| Record caption: eight consecutive samples through the chart's lowest value | sample JSON rows 03:12:30 to 03:14:15, including 49.755 at 03:13:15 |
| Related pages resolve | the build passed; `site/hifi/data/elexon.json` lists fuelinst, boal, system_prices and indo |

## Note-body corrections (vault note, smallest spans)

1. API table, "Publication lag": "~2-second sampling, exposed as 1-minute aggregates" became "samples are
   15 seconds apart as returned (bronze response for 2026-09-20: 5,761 samples ...). Elexon's own
   statement of the interval not verified."
2. Silver schema, `timestamp_utc`: the note said "Derived from (settlement_date, settlement_period) via
   `utils/time.settlement_period_to_utc`", which is wrong. It now says: parsed from `measurementTime` (or
   `reportDateTime`) as sent, citing `freq.py:57-78`.
3. Silver schema, `frequency_hz`: added that validation is fail-soft (`silver/base.py:2022-2029`).
4. Silver schema, `ingested_at`: "Time ingested into bronze" became "Stamped when the silver transform
   runs (`freq.py:85-89`)".
5. Known issues:
   - "~5760 samples per 3-hour window" became "per 24-hour window", citing the 2026-09-20 bronze
     response (5,761 samples for a 24-hour From/To).
   - Added a "Midnight in two day files" bullet, with the evidence above.

I left the curl example, the em dashes elsewhere in the body, the changelog and the "Historical bronze
re-ingest required" bullet unchanged.

## Unverified

- Elexon's documented sampling interval and publication lag. The Swagger page is JS-rendered (the content
  brief says so), and I made no live calls. The page states 15 seconds only as seen in the rows.
- The "statutory 49.5 to 50.5 Hz" band in the note's Overview. It is not in code or in a quoted vendor
  doc, so the page does not use it. I left it in the body because I have no evidence against it.
- The note's "Historical depth: Several years": no evidence, so the page carries no `history` fact.

## Open questions

- Should gridflow dedup the midnight sample across day files, or should the connector request To = D
  23:59:45? That is a gridflow data-shape question, out of scope here.
- There is no dark theme in `site/hifi/assets` (no `prefers-color-scheme` or dark tokens), so screenshots
  are light only.

## Screenshots checked

Re-check after the fix (1440 and 390, as requested):
- **1440** (headless Chrome, fresh profile, and my own Browser tab):
  - the chart draws 49.7 to 50.3 Hz with hourly ticks;
  - the line, key, caption and x_label are fully visible;
  - no overflow and no chart text outside its SVG.
- **390** (headless shot of the chart region):
  - the narrow chart draws 49.6 to 50.4 Hz with 00:00, 02:00 and 04:00 ticks;
  - the key sits below the chart;
  - the headless shot renders wider than 390, the same artefact as before, so the numeric check at a
    true 390 (next bullet) is authoritative.
- **True 390 × 844** (my own Browser tab, `tab-4`):
  - `scrollWidth` is 390 and no element sits outside the viewport;
  - every chart label ("49.6" to "50.4", "Hz", "00:00", "02:00", "04:00", x_label) sits inside the 358 px
    SVG.
- Viewport reset, tab closed, server on 9714 stopped.

First pass, before the fix:

- **Headless Chrome, full page** (`scratchpad/freq-shots/`) at 1440, 1024 and 768:
  - the hero scenery (turbine tops, scene labels), chart, key, raw feed, frame and guide, notebook
    (folded), related list and stratum corner labels are all fully visible;
  - the only visual problem is the flat line (template problem 1).
- **The 390 headless shot was wrong.** It rendered wider than 390 (Chrome's minimum window width), so I
  re-measured in my own Browser tab at a true 390 × 844:
  - `scrollWidth` is 390 and no element sits outside the viewport except inside scroll containers;
  - the chart and key are visible;
  - with the notebook open and the frame unfolded (`#fx`), the table (1,603 px) scrolls inside its
    `overflow: auto` wrapper;
  - the plot PNG is served at 703 × 334 and shown 300 px wide.
- **Disclosure:** my first Browser-pane call navigated and resized the shared fronted tab, which the
  `temp` writer was using (port 9715), before I switched to my own tab (`tab-1`). I made no other
  change to that tab.
- The chart key's `codes` is `FREQ` (it was `frequency`, which rendered as "Frequency frequency").
- **Same checks at 768, 1024 and 1440** (notebook open, frame unfolded): no overflow, and no chart text
  outside its SVG. Viewport reset to desktop, tab closed, and my server on 9714 stopped.

## Revision 1 (checker REVISE, `freq-review.md`)

1. **Major, `page.what_it_is`.** The sentence "Elexon's response includes the sample at the window's end"
   is now "In responses gridflow has fetched, Elexon includes the sample at the window's end, so a day's
   file can end on the next midnight."
   - This scopes the claim to what was measured. No Elexon doc states it.
   - To stay within the 60-word budget I trimmed two phrases, with no change of meaning: "Elexon's
     measured" became "Measured", and "keeps each sample's `measurementTime`" became "keeps
     `measurementTime`". The block is now 58 words.
2. **Nit, `page.notebook.needs`.** `needs` is now "16 and 17 September 2026", so the notebook's duplicate
   midnight (cell 4) can be reproduced.
   - To keep `needs` and the commands in agreement, `raw_feed.commands` now reads
     `ingest --start 2026-09-16 --end 2026-09-18` ("bronze; two 24-hour windows") and
     `transform --start 2026-09-16 --end 2026-09-17`.
   - `raw_feed.requests` still shows the 17 September call as its example.
   - The notebook cells are unchanged, so the notebook was not re-run.

Checks after the revision:
- the mirror is `cmp`-identical, and the note is still CRLF;
- `gridflow-build --only elexon/freq` printed "wrote: data-sources/elexon/freq.html", with no errors from
  other pages this time;
- `detect.mjs --json`: `[]`;
- the rendered page shows the new `what_it_is` sentence and "16 and 17 September 2026 ingested.".

Screenshots were not re-taken: the edits are a few words of prose in sections already checked at all four
widths.
