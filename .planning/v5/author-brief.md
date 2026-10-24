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
- **Nothing clipped or overlapping.** Every drawing, label and caption is fully visible at 1440, 1024,
  768 and 390 in light and dark, in particular scenery tops (turbines), scene edges and
  section-corner labels. Check rendered screenshots of your page at those widths (headless browser, or
  your own preview tab on a free port in 9700-9799), not only the HTML; a long label of yours (a key
  note, a code, a related dataset key) is the usual cause.

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
  - **Several columns of one row** (a wide table: one cost column per reason) are series through
    `values` instead of `value` and `group`, on a line or stacked area. Each item is a column, or
    `{column, series}` to give it a short series key; `chart_view.key` then names each key once.
    Series draw in the listed order; a null cell is missing for its own series only:
    ```yaml
    values:
      - {column: thermal_constraints_cost_gbp, series: thermal}
      - {column: voltage_constraints_cost_gbp, series: voltage}
    ```
- **chart_view.y_min** (optional, a number): the y axis floor, which need not be a tick. Without it
  the axis ends at the tick below the lowest value, so five dates at -£232,717 on a £60M axis floor
  it at -20M; `y_min: -2000000` ends it just below the data. A floor a little below zero also lifts a
  line that sits at zero off the axis, so a gap in it reads as a gap (aggregated BSAD's missing
  2020-21: `y_min: -8`). The build fails a floor above the lowest value drawn. Missing periods are
  always gaps: a line breaks at a null or an absent period, a stacked area at an absent period or one
  where every series is null; neither is joined across the gap or drawn at zero.
- **Long spans** tick on 1 January when three or more fall inside, else every half year or quarter
  ("Jul 2024", "2025", "Jul"); nothing to set.
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
  double-reported flow). The rows print as a Polars frame, as silver prints them; columns past the
  1280 px budget fold behind `…` (the pipeline columns always do). `record.mark` is no longer used.
  `select.columns` (ruling #35) sets the print order, like a Polars `.select`: the named columns come first and
  the rest follow in silver's order. Name the columns that matter (a level, a value, `published_at`) so they stay
  in view when the frame folds. The column guide then follows that order.
- **record.key**: the columns that identify a row; the frame marks them with a square and the guide
  lists them first.
- **record.fields**: the column guide, one line per column in frame order, 14 words or fewer, from the
  code. No lines for the pipeline columns every table carries (`data_provider`, `ingested_at`,
  `event_time`, `available_at`, `source_run_id`, `dataset_version`, and `vintage_policy` where
  present): the build ignores them. No relation line, no fold note, no filler.
- **record.caption**: one line after `shape: (8, n)` saying which eight rows these are.
- **notebook.cells**: after the template's setup cell and `data.<source>` help card, 2 to 4 cells:
  the query (`data.<source>.query("<dataset>", start, end)`, or `data.sql(...)` for a table with no
  time axis, because `query()` filters on a date column), `.head()` of the key columns, one plot or,
  with no time axis, one non-time output (`value_counts()`). Read-only calls only. Check which
  relation and date column `query()` uses before you write the lead. `query()` orders rows by its date
  column only, so rows within a day come back unordered: sort by `timestamp_utc` before plotting.
- **notebook.needs**: the window the reader must ingest ("20 to 26 September 2026", or "the BM unit
  register"). It is printed inside "Needs gridflow and gridflow-models installed, with <needs>
  ingested.", so it must be a short noun phrase: the build rejects a `;`, a full stop at the end, the
  word ingest, a leading verb (run, download, use ...) or a clause word (will, fails, is ...). A loss
  or caveat goes in `what_it_is` or the chart caption, not here.
- **related**: up to 4 datasets that have pages (`site/hifi/data/<vendor>.json` lists them), each with
  a reason of 12 words or fewer. Say how they relate, not what they are called. Name a table key
  (`elexon/fuelhh`, which links to its page or its family's pointer) or a page slug from the page set
  (`neso_data_portal/aggregated-bsad`, a package or family page, linked directly). A slug that names
  no page fails the build.

## Commands (run from the front-end worktree root)

```
# after editing the canonical note, copy it byte for byte into the repo mirror
cp <vault-worktree>/30-vendors/<vendor-dir>/datasets/<dataset>.md vault/<vendor>/<dataset>.md
# retire the staged spec and the authored override for your dataset, if present (plain delete; the seat stages it)
rm -f site/hifi/data/chart-specs/<vendor>/<dataset>.json authored-pages/<vendor>/<dataset>.html
# artefacts, from real data (read only)
uv run --system-certs --extra distil gridflow-distil --dataset <vendor>/<dataset>
uv run --system-certs --extra distil gridflow-sample --dataset <vendor>/<dataset> [--dry-run]   # also a held page's raw sample
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

## Caveats and held pages (ruling 66)

The site is a data catalogue: a table with silver rows shows them, even when a question about them is
open. Ruling 66 supersedes ruling 6's "no rows for held tables".

- **A table with silver rows and an open question** (the date order, the clock, a unit, when a row was
  first published) gets a full page plus one plain caveat line: `caveat:`.
- **A table with no silver rows** (gridflow keeps the raw files only: "no table: bronze only", "files
  only") or a **licence carve-out** stays `held:`, with its reason.

### Converting a held page that has silver rows

1. Remove `page.held`, and remove `held:` from every family member that has a silver table.
2. Add `chart` and `chart_view` (or `chart: {type: none, reason: ...}` where no chart fits), `record`
   and `notebook`, exactly as for a full page, then make the artefacts (`gridflow-distil`,
   `gridflow-sample`, `scripts/run_notebooks.py`). The Key line in the hero comes back with `record`.
3. Add the caveat:
   - on a one-table page, `page.caveat: <line>`;
   - on a family page, `caveat: <line>` on each member whose rows have the question.

   A member with no silver table keeps its member-level `held: <reason>`, and the page as a whole is no
   longer held. A member may not carry both `held` and `caveat`, and a page-level `caveat` on a family
   page fails the build.

```yaml
page:                                  # one-table page: full anatomy, plus
  caveat: NESO's files carry no publication time, so these rows are the latest file.
page:                                  # family page: per member
  family:
    members:
      - {dataset: eac_mock_results_summary, differs: Each auction's summary, request: "GET https://...",
         caveat: "Mock auction data, not real procurement; the timestamps' clock is not stated."}
      - {dataset: eac_mock_results_daily_summary, differs: The daily summary, request: "GET https://...",
         held: Mock auction data; NESO's daily files hold headers only.}
```

Inside a `{...}` member entry, quote a caveat that holds a comma, as above; unquoted, YAML splits it at
the comma and the build fails on an unknown key. The caveat is one plain sentence of 16 words or
fewer, the same budget as `held`. It names the open
question and what it means for the rows a reader sees. Ruling 66's own example runs to 23 words, so
trim it, for example to "NESO's files carry no publication time, so these rows are the latest file." (13
words). Do not add a "Caveat:" label, a status word, "live" or a planning code: the page prints the line
as you write it.

**Where it prints.** A one-table page prints the caveat just above the frame, under its caption. A
family member's caveat prints under the member in the raw feed, beside what differs. If the frame shows
that member's table, the caveat also prints above the frame. The frame, chart and notebook show one
table, the lead's or `record.select.silver`. Point the frame at the member whose rows say the most, and
say in the chart caption if the chart shows one member.

### Held pages (no silver rows)

A package with no silver table at all is a held page: the full anatomy minus rows. Mark the lead note
`page.held: true` on a family page, where each member gives its own `held:` reason (16 words or fewer).
On a one-table page, write `page.held: <reason>`. Write the hero and facts (no Key line: it comes from
`record`), `what_it_is`, `how_used`, the raw feed with each table's files, and `related`. Do not write
`chart`, `chart_view`, `locations`, `record`, `notebook` or `caveat`. Commit no series, sample or
notebook: the build fails on any of them. The page lists each table under "The silver tables" with its
reason, and has no gold stratum. The hub links it like any other page.

```yaml
page:
  held: true
  family:
    slug: eac-mock-auction-results
    members:
      - {dataset: eac_mock_results_daily_summary, differs: The daily summary, request: "GET https://...",
         held: Mock auction data; NESO's daily files hold headers only.}
```

**A raw sample on a held page.** If the raw files may be shown (not a licence carve-out), a held page
can show the header and first eight lines of one bronze file, exactly as NESO sent it, in the raw feed.
Add a caveat that names the question keeping the table unpublished:

```yaml
page:
  held: Rows repeat and there is no settlement-run column.
  raw_feed:
    note: ...
    requests: ["GET https://..."]
    commands: [...]
    sample:
      table: daily_balancing_costs       # optional: default the page's table (a family's lead)
      file: q1_cost_fy2627.csv           # optional: NESO's file name; default the newest capture
      caveat: Rows repeat with no run column, so revisions cannot be told apart.
```

Then run `uv run --system-certs --extra distil gridflow-sample --dataset <vendor>/<key> --dry-run` to
see the lines, and run it again without `--dry-run` to write
`site/hifi/data/raw-samples/<vendor>/<key>.json`. It reads `C:\gridflow-data\bronze` read only and
writes nothing there. Name `file` whenever more than one file is kept. Files from one ingest share a
capture time, so "newest" is arbitrary among them. Only CSV and text files can be sampled. Windows-1252
files (the BSUoS forecasts) are read as such. A file with a header and no rows prints as "the file
holds no rows". A raw sample is only for a held page. A page with silver rows shows its frame.

## Family pages (v5 D5)

The family's lead member's note carries the page; `page.family` lists every member with what differs
(14 words or fewer) and its raw request. A member with several files (a current and an archive file)
gives `request` as a list of up to four; each prints as its own rows of the member's well:
`request: ["GET https://.../dump/<current>", "GET https://.../dump/<archive>"]`. A member with no
silver table adds `held:` with the reason (16 words or fewer); the raw feed prints it under the member
as "Rows not shown: <held>". A member whose rows carry an open question adds `caveat:` instead (see
"Caveats and held pages"). Other members keep no `page:` block: their addresses become
pointers to `<family-slug>.html#<member>`. The chart, frame and notebook come from the lead's silver
table; say so in the caption if the chart shows one member. The family's slug and members are fixed in
`site/hifi/data/<vendor>.json` (the page set); `page.family` must name the same slug and members, and
only the lead (the first member there) carries a `page:` block. Until it does, the family page renders
blank: the hero's name and the member ids, nothing else.
