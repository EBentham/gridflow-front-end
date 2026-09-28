# elexon/freq: review

Checker: Opus 5.5 (high), 2026-09-28. Page `site/hifi/data-sources/elexon/freq.html` in the p26-elexon worktree,
note `30-vendors/elexon/datasets/freq.md` in the vault worktree (mirror `vault/elexon/freq.md` byte-identical, `cmp`).

## Verdict: REVISE

No blockers, 1 major, 1 nit. The fix is one wording change.

## Findings

1. **major**, `page.what_it_is`: "Elexon's response includes the sample at the window's end" states a vendor rule
   without hedging.
   - **Why it is an overclaim.** The evidence is only responses gridflow has fetched; no vendor doc says it. The
     code does not enforce it either: it only tolerates it (dedup per date, `silver/elexon/freq.py:83`). This is
     the pilot's overclaim class (a fact the project measured, stated as the vendor's rule; compare INDOD "MWh").
     The rubric's sign-convention rule applies: "if only the project measured it, say so". The "can end" hedge
     covers only the clause that follows, not the vendor claim.
   - **The evidence is consistent.** All 14 bronze responses
     (`C:\gridflow-data\bronze\elexon\freq\2026\{08,09}\*\*.meta.json`, each a 24-hour From/To) hold 5,761
     samples whose last `measurementTime` equals `measurementDateTimeTo`. The note's own live check (1-hour window,
     241 rows) agrees.
   - **Fix.** Scope it as observed, for example "In the responses gridflow has fetched, Elexon includes the sample
     at the window's end, so a day's file can end on the next midnight." Keep it within the word budget.
2. **nit**, `page.notebook.needs` / cell 4 output: the output shows `2026-09-17 01:00:00+01:00` twice (49.970). That
   only happens because the store also held 16 September's file. A reader who ingests only what `needs` and
   `raw_feed.commands` name (17 September) gets that midnight once. The lead says "A midnight in two day files comes
   back twice", which is conditional and true, so nothing is wrong. Optional: say `needs` "16 and 17 September 2026"
   so the output can be reproduced.

## What I checked (evidence)

### Facts (rubric 1)

- **Key and dedup.** `silver/elexon/freq.py:25` `ENTITY_KEY_COLUMNS = ("timestamp_utc",)`; `:83`
  `unique(subset=["timestamp_utc"], keep="last")`, per transform date. `read_bronze` reads only `target_date`'s
  bronze folder (`:27-51`).
- **`timestamp_utc`.** Parsed from `measurementTime` or `reportDateTime` (`:57-78`), UTC. `frequency_hz` is cast
  from `frequency` (`:60,79`).
- **`ingested_at`.** Stamped `datetime.now(UTC)` at transform (`:85-89`). The body correction is right.
- **Schema bounds, fail-soft.** `schemas/elexon.py:213` `Field(ge=49.0, le=51.0)`. `silver/base.py`
  `_validate_against_schema` docstring: "Never raises and never drops a row".
- **Request.** `endpoints.py` `freq`: `/datasets/FREQ`, `PUBLISH_DATETIME`, `measurementDateTimeFrom/To`, with
  pagination. `_to_utc_z` formats `%Y-%m-%dT%H:%M:%SZ`, and `page` is added. The bronze meta for 17 Sep has
  `request_params` `{From: 2026-09-17T00:00:00Z, To: 2026-09-18T00:00:00Z, page: 1}`, the same as
  `raw_feed.requests`.
- **Commands.**
  - `resolve_dates` makes a bare date midnight UTC.
  - `client.py:93-99` loops `while current < end` in chunks of `max_chunk_hours` 24, so ingest 17 to 18 is one
    24-hour call.
  - Transform `--end` is inclusive.
  - freq has no partition offsets and its `read_bronze` reads day D only, so the windows are right.
- **Notebook lead.**
  - `source.py:401-451`: `SELECT * EXCLUDE (...) FROM silver_elexon_freq WHERE ... ORDER BY timestamp_utc`.
  - `_get_method_registry.py:94-96`: TIMESTAMPTZ columns use half-open UTC days, so the end day is whole.
  - The excluded columns are `event_time, available_at, source_run_id, dataset_version`
    (`gridflow/silver/schema_manifest.py:87-92`), which are the lineage columns.
  - The notebook output prints `+01:00`, which backs "Times print in local time".
- **The two measured facts, scoped as required.**
  - *15-second interval.* `facts.cadence` says "as in the rows below". The caption and alt say "every 15-second
    sample from 00:00 to 06:00 UTC on 17 September". Polars: every `diff()` in `freq_20260917.parquet` is 15 s
    (5,760 of 5,760), and 1,440 points in 6 h. Scoped to the rows and the window.
  - *Midnight in two day files.* `facts.grain` says "can sit", and the notebook lead is conditional. It rests on a
    code rule: dedup runs per transform date (`freq.py:83`), and the view is a plain parquet glob. The vendor
    behaviour is in finding 1. Polars over the 14 local files: each runs D 00:00 to D+1 00:00 (5,761 rows), and the
    12 shared midnights have identical values. The page states no local counts.
- **No other "always", "every" or "equal" claims.** "In every hour" in the alt is checked below.

### Chart provenance (rubric 2)

- **Provenance.** Series `generated_by: gridflow-distil`, `spec_origin: vault`, and the spec echo equals the note's
  `page.chart`. No staged spec (`site/hifi/data/chart-specs/elexon/freq.json` is absent), and no authored override.
  The build's digest check passed.
- **What the spec applies.** Filter `timestamp_utc` from 00:00Z (inclusive) to 06:00Z (exclusive), dedup on
  `timestamp_utc`, `aggregation: last`, no time bucket. Provenance: 1,441 rows matched, 1 duplicate dropped, 1,440
  used. Title, caption ("Hz, every 15-second sample from 00:00 to 06:00 UTC ... unaggregated") and `x_label` match
  what the spec applies.
- **Values.**
  - Series min 49.755 at 03:13:15Z and max 50.208 at 01:00:15Z. Polars on silver agrees, and so does the key note.
  - Per-hour min and max for hours 0 to 5: (49.837, 50.166), (49.848, 50.208), (49.805, 50.187),
    (49.755, 50.157), (49.822, 50.097), (49.837, 50.092). Each hour crosses 50, so "either side of 50 Hz in
    every hour" holds.
  - The first value above 49.9 after the low is 49.911 at 03:17:30, as the alt says.
- **Chart as drawn after today's renderer fix.**
  - Wide SVG ticks: `49.7` to `50.3` in steps of 0.1, `Hz`, `00:00` to `05:00` hourly.
  - Narrow SVG: `49.6` to `50.4` in steps of 0.2, with `00:00`, `02:00` and `04:00`.
  - The alt's "an axis spanning a few tenths of a hertz either side of 50" fits both, and the caption carries no
    axis claim. There is no zero baseline.
- **Palette.** One line, `petrol`, code `FREQ`. There is no khaki and nothing is summed.

### No local data (rubric 3)

- The grep of the `page:` block and the rendered text for `locally|held|our |since 20|% of|N rows|N days` matches
  only "as in the rows below", which refers to the eight shown rows.
- Every number is in the chart, the eight rows, the notebook output, or the code (49.0 and 51.0 bounds).

### Build and structure (rubric 4)

- `uv run --system-certs --extra build gridflow-build --only elexon/freq` printed "wrote: data-sources/elexon/freq.html
  (dataset template)" and "rendered only ['elexon/freq']".
- `detect.mjs --json` returned `[]`.
- **Samples.** `generated_by: gridflow-sample`. The eight rows run 03:12:30 to 03:14:15 and include the low 49.755,
  as the caption says. The guide has `timestamp_utc` (key, first) and `frequency_hz`. `data_provider` and
  `ingested_at` are pipeline columns and have no lines.
- **Notebook.**
  - `generated_by: scripts/run_notebooks.py`, with 5 read-only cells (setup, help card, `query`, `.head()`,
    `plot`) and no errors.
  - I viewed `freq-5.png`: 49.755 to 50.219 Hz, and the line runs 01:00 to 01:00 on the UTC+1 clock. The lowest
    dip is just after 04:00 on that clock (03:13 UTC). The daily max 50.219 at 07:05:30 UTC matches Polars.
    `plot_alt` is right.

### Clipping and overlap (rubric 5)

Screenshots are in `scratchpad/freq-review-shots/`:
- Headless Chrome full-page shots at 1440, 1024 and 768 (`full-*.png`).
- CDP-driven shots at true widths 1440, 1024, 768 and 390 (`open-*.png`), with the notebook opened and the frame
  unfolded.

What they show:
- `scrollWidth` equals the viewport at all four widths, folded and open.
- No element sits outside the viewport except inside scroll containers.
- No chart `<text>` sits outside its SVG.
- By eye:
  - the hero scenery (turbine tops, scene labels), chart, key, raw feed, frame and guide are fully visible, with
    no overlap;
  - so are the open notebook (help card, table, plot) and the related list;
  - the stratum corner labels ("bronze, the response as fetched" and the rest) are fully visible.
- At 390:
  - the frame and the notebook's `.head()` table scroll inside their own boxes, as designed;
  - the 390 hero shows the right-hand part of the scene, which is template behaviour.

Light only: `site/hifi/assets` has no `prefers-color-scheme` or `data-theme`, so no dark mode exists.

### Leakage and filler (rubric 6)

- No em dashes, en dashes, middle dots or arrows in the `page:` block or the rendered page (checked by code point).
- No "live", "now" or "real-time", no planning labels, and no filler.
- Related notes are 12 words or fewer and say how each dataset relates.
- "Every five minutes" for fuelinst: the gaps between successive `timestamp_utc` values in
  `fuelinst_20260921.parquet` are all 5 minutes (288 of 288).

### Vault body edits (rubric 7)

- Each edit fixes a small span and cites evidence:
  - the `timestamp_utc` source (the old settlement-period derivation was wrong);
  - fail-soft bounds;
  - `ingested_at`;
  - "per 24-hour window";
  - the new midnight bullet;
  - the "Publication lag" row, which replaces the unsupported "~2-second sampling, 1-minute aggregates".
- Every cited count matches bronze (20 Sep response: 5,761 samples, 00:00 to the next 00:00).
- The curl example, changelog and other bullets are untouched.

## Outside this page (for the seat, not findings)

- **Folded notebook numbering.** The folded notebook preview labels the query cell `[2]`. Opened, the same cell is
  `[3]`, and the help card is `[2]`. This is template behaviour, not a freq defect.
- **Stale body bullet.** "Historical bronze re-ingest required" looks stale. Every local FREQ bronze meta uses
  `measurementDateTimeFrom/To` and returns the requested window. The author left it alone, correctly: it is not
  their edit.
