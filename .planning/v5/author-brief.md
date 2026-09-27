# Dataset page author brief (v5 Phases 25b and 26)

Calibrated on the 25b pilot (fuelhh, system_prices, entsog physical_flows, bmunits_reference, and the
demand outturn family). One author agent writes one dataset page (or one family page). A reviewer then
checks it against `review-rubric.md`. You write only your own dataset's files.

## What you produce

1. **The `page:` block** in the dataset's canonical vault note (front matter), following the content
   model in `src/gridflow_front_end/page_fields.py` (module docstring = the field list; `BUDGET` = the word
   budgets). The worked example is `vault/elexon/fuelhh.md`: copy its shape.
2. **Corrected vault facts** in the same note's body, where your research shows the note is wrong
   (for example a wrong source field, a stale time example). Fix the smallest span, cite `file:line`.
3. **The chart spec** (`page.chart`, data only) and its words (`page.chart_view`).
4. **Three committed artefacts**, made by the commands below from real data, never by hand:
   `site/hifi/data/series/`, `samples/` and `notebooks/<vendor>/<dataset>.*`.
5. **The page built** with `gridflow-build --only <vendor>/<dataset>` and the detector at `[]`.
6. **A report** (your final message): an evidence table (claim, evidence), what you corrected in the
   note body, anything you could not verify, and open questions.

## Sources of truth, in order

1. gridflow code, `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\src\gridflow\`: `schemas/*.py`,
   `silver/<vendor>/<dataset>.py` (the transformer, its `DATASET_VERSION`, dedup, derived columns,
   `PARTITION_SOURCE_OFFSETS`), `silver/base.py` (lineage columns), `connectors/**` (the raw request),
   `cli.py` and `runner.py` (the commands and their `--start`/`--end` semantics), `config/sources.yaml`.
2. Local silver, `C:\gridflow-data\silver\<vendor>\<dataset>\`, READ ONLY, with Polars.
3. gridflow_models, `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow_models\`: what
   `data.<source>.query(...)` reads, filters on and drops (`source.py`, `_get_method_registry.py`,
   gridflow `schema_manifest.py`).
4. The vault note. It is derived from 1 and 2 and is sometimes stale: the code wins.

## Content rules (the reviewer checks every one)

- **No local-data references anywhere**: no "held locally", no local row counts, no local first or
  last dates, no "since we started ingesting", no gap descriptions of local holdings. History appears
  only as what the vendor publishes, and only with evidence (a vendor doc quoted in the note, a code
  comment citing the vendor). No evidence, no history fact.
- **A number is allowed only if** it is a vendor fact, a code fact, or a value visible in the chart or
  the rows the page shows (the eight rows, the notebook outputs). "Stacked, but 133 MW at most here"
  is fine: it is in the chart. "4,052 negative half-hours since 2021" is not.
- Captions describe what the chart shows (dataset, unit, window, aggregation) and any caveat needed to
  read it. Never a cause nobody has verified. No filler, no restating the obvious.
- Sign conventions: say what the code or vendor says; if only the project measured it, say so
  ("checked against demand; Elexon does not state it"); if nobody knows, say it is undocumented.
- No em dashes (use commas, colons, parentheses). No planning labels (planned, shipped, phase codes).
  No "live", "now", "real-time". No marketing words.
- Plain, specific English. British spelling. Code, columns, codes and dataset keys in backticks.

## Field notes (what the pilot learned)

- **title**: the plain name of the data, 6 words or fewer ("Generation by fuel type").
- **facts**: vendor ("Elexon BMRS, dataset FUELHH"), cadence, grain. The page adds **Key** from
  `record.key`. Add `history` only with vendor evidence.
- **landscape**: `power` (generation), `market` (prices, balancing), `gas` (gas flows, storage, LNG),
  `units` (registers of units). Scenery only.
- **chart** (`chart_spec.py` docstring): pick the reading a practitioner wants, not the first numeric
  column. Use a fixed window (`window: {start, end}` plus a filter on the vendor's own date column when
  its day does not start at 00:00 UTC). Types:
  - `stacked-area` for parts of a whole; signed series stack above zero when positive and hang below
    when negative (the renderer does this; never clip or `abs()`).
  - `line` for prices, flows, a few series; nulls and time gaps break the line (never interpolate).
  - `bar` for a table with no time axis (counts or a sum by category; `group_null` keeps nulls as a
    category). Never sum a non-additive column (registered capacity per registration is not additive).
- **chart_view.key**: one entry per series, in the order the reader should read them (top of the stack
  first). Paint: the scenery palette by role (`wind`, `solar`, `gas`, `nuclear`, `imports`, `biomass`,
  `other` default automatically). Codes the palette does not cover are unpainted: `hatch-lines`,
  `hatch-cross`, `hatch-dots`, `hatch-vertical`. **Khaki is the vendor code OTHER only.** A price or
  flow line takes `petrol`, `horizon`, `olive` or `clay` by meaning. `tag` puts a short italic label on
  a thick band (optional).
- **chart_view.alt**: describe the actual shape with real values read from the committed series.
- **raw_feed.requests**: the exact URL gridflow's connector sends (host, path, every parameter as the
  code formats it, including `page` if it sends one), with a real example window. Not the vault's curl
  example if the connector differs.
- **raw_feed.commands**: exact CLI. `gridflow ingest` writes bronze only; `gridflow transform` writes
  silver (its `--end` is an inclusive date). The ingest `--end` depends on how the connector builds its
  requests: for time-window endpoints (`publishDateTimeFrom/To`, `from/to`) it is an exclusive instant;
  for endpoints with one call per date in the path (`/system-prices/<date>`) `client.py` `_date_range`
  loops `while current <= end_date`, so the end date is fetched. Read the connector; do not assume.
  Then widen the ingest window where silver day D reads other bronze days:
  `PARTITION_SOURCE_OFFSETS` (fuelhh: ingest 19 to 28 Sep, transform 20 to 26 Sep), or, with no
  offsets, a settlement day whose first period is published the evening before (INDO in BST: ingest
  from the day before). Prefer separate `ingest` and `transform` lines to `gridflow pipeline`, whose one
  window transforms an end date that has no bronze. Comments are 6 words or fewer.
- **record.select**: a filter (plus `order_by`, and `dedup` for append-only tables) that picks exactly
  eight real rows, chosen to show the column that matters most (a signed value, a null, a
  double-reported flow). `record.mark` names the one row laid out field by field.
- **record.fields**: one meaning per schema column (not the lineage columns, which the template
  explains), 14 words or fewer, from the code. `data_provider`: "Same on every row: <vendor>".
- **notebook.cells**: after the template's setup cell and `data.<source>` help card, 2 to 4 cells:
  the query (`data.<source>.query("<dataset>", start, end)`, or `data.sql(...)` for a table with no
  time axis, because `query()` filters on a date column), `.head()` of the key columns, one plot or,
  with no time axis, one non-time output (`value_counts()`). Read-only calls only. Check which
  relation and date column `query()` uses before you write the lead. `query()` orders rows by its date
  column only, so rows within a day come back unordered: sort by `timestamp_utc` before plotting.
- **notebook.needs**: the window the reader must ingest ("20 to 26 September 2026", or "the BM unit
  register").
- **related**: up to 4 datasets that have pages (`site/hifi/data/<vendor>.json` lists them), each with
  a reason of 12 words or fewer. Say how they relate, not what they are called.

## Commands (run from the front-end worktree root)

```
# after editing the canonical note, copy it byte for byte into the repo mirror
cp <vault-worktree>/30-vendors/<vendor-dir>/datasets/<dataset>.md vault/<vendor>/<dataset>.md
# retire the staged spec and the authored override for your dataset, if present (plain delete; the seat stages it)
rm -f site/hifi/data/chart-specs/<vendor>/<dataset>.json authored-pages/<vendor>/<dataset>.html
# artefacts, from real data (read only)
uv run --system-certs --extra distil gridflow-distil --dataset <vendor>/<dataset>
uv run --system-certs --extra distil gridflow-sample --dataset <vendor>/<dataset> [--dry-run]
C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow_models\.venv\Scripts\python.exe scripts/run_notebooks.py --dataset <vendor>/<dataset>
# the page
uv run --system-certs --extra build gridflow-build --only <vendor>/<dataset>
node C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json site/hifi/data-sources/<vendor>/<dataset>.html
```

Edit notes with the Edit tool, not `sed -i`: vault notes are CRLF and `sed` strips it, which turns
the mirror diff into a whole-file rewrite. `--only <family lead>` also rewrites the members' pointers.

The build fails on a missing or over-budget field, a key entry per series missing, a stale artefact
digest, an unresolvable related dataset, or a leftover authored override: fix and rerun. Word
budgets and required fields are in `anatomy_errors`. If the notebook runner hits a DuckDB lock
(another author's kernel), run it again.

## Never

Run `gridflow ingest`, `transform`, `pipeline`, `backfill`, `reset` or `prune`; write under
`C:\gridflow-data`; call a live vendor API; run `gridflow-drift-check`; run git commit, push, checkout,
stash or branch in either repo (the seat commits); edit any file that is not your dataset's (the
template, CSS and Python are the seat's; report a template problem instead of working around it);
kill processes.

## Family pages (v5 D5)

The family's lead member's note carries the page; `page.family` lists every member with what differs
(14 words or fewer) and its raw request. Other members keep no `page:` block: their addresses become
pointers to `<family-slug>.html#<member>`. The chart, record and notebook come from the lead's silver
table; say so in the caption if the chart shows one member.
