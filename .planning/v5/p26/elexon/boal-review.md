# boal (Bid-offer acceptance levels): review

Checker: Opus 5.5 · high, 2026-09-29. Inputs: canonical note in the vault worktree (`git diff origin/master`), mirror
`vault/elexon/boal.md` (byte-identical, `cmp`), committed artefacts, built page, writer's report `boal-author.md`.

## Verdict: APPROVE

No findings above nit. 3 nits, 1 note on the writer's report.

## Findings

1. **nit**: `page.facts.grain` ("One row per settlement period, BM unit and acceptance"), and `page.what_it_is`
   ("Silver keeps one segment per acceptance and settlement period").
   - **What:** both hold for each transform run: `boal.py:120-123` is `unique(subset=[settlement_date,
     settlement_period, bm_unit_id, acceptance_number], keep="last")` over one bronze day. They do not hold for the
     relation `query()` reads. A segment starting exactly at 00:00 UTC comes back in two adjacent `from`/`to`
     windows (the note body's new "Midnight boundary" bullet), so its key is written to two silver files.
   - **Evidence (Polars over all 14 local silver files):**
     - 539 keys appear twice (1,078 rows). Every one is at `timestamp_utc` 00:00 UTC and sits in two files, and both
       copies carry the same levels (0 keys with differing `bid_offer_level_from`/`_to`).
     - The notebook's own query (settlement date 19 Sep) returns 22,553 rows for 22,488 distinct keys.
   - **Why only a nit:** the rubric allows a code rule with evidence, and this is one. The copies are the same
     segment, not a second one, so "one segment" stays true in substance. Nothing the page shows is affected: the
     chart dedups on (unit, acceptance, acceptance time) and the notebook plot on (unit, acceptance).
   - **Fix (optional):** no page change is needed. The seat already holds the writer's open question (a gridflow
     unit to dedup across files or make the window half-open).
2. **nit**: note body, Known issues, the `settlementPeriodFrom`/`settlementPeriodTo` bullet.
   - **What:** it says the five dropped fields are "renamed at `silver/elexon/boal.py:74-77`". Only `timeFrom`,
     `timeTo`, `nationalGridBmUnit` and `amendmentFlag` are in the rename map there (`boal.py:74-77`).
     `settlementPeriodTo` is never renamed; it is dropped only because `output_cols` leaves it out
     (`boal.py:133-148`).
   - **Fix:** "(four renamed at `boal.py:74-77`; all five absent from `output_cols` at `boal.py:133-148`)", or
     similar.
3. **nit**: note body, Overview, "National Electricity System Operator" corrected to "National Energy System
   Operator".
   - The correction is right, but it cites no evidence. Rubric 7 asks every body correction to cite some. A
     citation is enough; no text change is needed.

## Note on the writer's report (no severity; not on the page or in the note)

- The report's "814 such duplicate keys across the September files" does not reproduce. I count 539 duplicate keys
  (1,078 rows) across all 14 local files (1 to 5 Aug and 13 to 21 Sep); the September files alone cannot hold more.
  Neither the page nor the note body carries the number, so there is nothing to fix. The seat should use 539/1,078 if
  it writes the gridflow follow-up.

## What I checked (all pass)

**Focus 1: the segment dedup.**
- Code:
  - `boal.py:74-77` renames `timeFrom`/`timeTo`, and `output_cols` (`boal.py:133-148`) omits them, so segment times
    never reach silver.
  - `boal.py:120-123` keeps one row per (date, period, unit, acceptance), `keep="last"`.
  - boal is exempt from the publication-window filter (`silver/elexon/_publication_window.py:49`). `VINTAGE_PER_BRONZE_FILE`
    and `LOCKSTEP_BRONZE_READ` default to False, so it takes the plain `read_bronze` → `transform` path
    (`base.py:1180-1191`), with no further dedup.
- Data (bronze `2026/09/19/raw_20260926T183427Z_eef2ab34.json`):
  - 41,078 records, 16,699 (unit, acceptance) pairs with 1 to 6 segments each.
  - 22,538 distinct silver keys, and 12,252 of them have more than one segment.
  - The silver file `boal_20260919.parquet` has 22,538 rows.
  - The row silver kept equals the positionally last raw row for all 22,538 keys (0 level mismatches).
  - `settlementPeriodFrom` is the period containing `timeFrom` for all 41,078 segments, so "Half-hour the kept
    segment starts in" is right.
- Page wording: `what_it_is` states the limit plainly: one segment kept, "the last one received", segment times
  dropped, "the full profile cannot be rebuilt". It gives no cause and claims no impact beyond that.

**Focus 2: the chart.**
- Spec: `aggregation: count`, `dedup on [bm_unit_id, acceptance_number, acceptance_time]`, `time: acceptance_time`,
  1 h buckets, fixed window 14 to 20 Sep, grouped by `so_flag`. No level column is read.
- `acceptance_time` and `so_flag` are constant per (unit, acceptance) across all local silver (0 pairs with more than
  one value), so each acceptance counts exactly once.
- I recomputed the series independently from silver:
  - 93,471 acceptances in 168 hours, matching the series sums (77,507 + 15,964).
  - Totals run from a minimum of 80 (15 Sep 22:00) to a maximum of 1,304 (19 Sep 15:00).
  - SO-flagged counts: 0 to 66 on the 14th, peak 283 at 19 Sep 18:00, at most 188 on the 20th, and 8 hours at 0.
  - Every alt number matches.
- The 8 null SO-flagged hours render as 0 (`chart_svg.py:379`), which is right for a count.
- Provenance and paint:
  - `spec_origin: vault`, and the digest passes in the build.
  - No staged spec or authored override exists.
  - The paints are two unpainted hatches, with no khaki.

**Focus 3: the seven note-body corrections.**
- (1) NESO name: correct; see nit 3.
- (2) Dedup key: matches `boal.py:120-123`.
- (3) `so_flag` quote: verbatim in Elexon *Imbalance Pricing Guidance* v15.0, 25 June 2020, which I fetched.
- (4) Level reading: the Elexon BSC glossary "Bid-Offer Acceptance Level" says "MW level of operation at the
  beginning and at the end", with start and end times.
- (5) `ingested_at`: stamped at transform time, `boal.py:125-129`.
- (6) 2026-05-06 period 9 is 03:00 UTC (BST: period 1 starts 23:00 UTC the day before).
- (7) The dropped fields are right (see nit 2 for the citation). The midnight-boundary bullet reproduces: bronze 19
  `timeFrom` runs from 19 Sep 00:00 to 20 Sep 00:00 inclusive, with 66 segments at 20 Sep 00:00. It is labelled as
  measured.
- There are no other body edits.

**Facts.**
- Raw request: `/datasets/BOALF` with `from`, `to` and `page` (`endpoints.py:65-71, 300-313`), in 24 h chunks with
  `while current < end` (`client.py:93-99`). This matches the bronze sidecar's `request_url`.
- Commands: a bare date is midnight UTC (`runner.py:479-500`), and transform dates are inclusive
  (`runner.py:1125-1138`).
  - Ingest 13 to 22 Sep, with an exclusive end, fetches bronze 13 to 21. Transform 13 to 21 covers every
    acceptance-time edge of the chart.
  - `notebook.needs` (13 to 21 September) agrees.
- `notebook.lead`: `query()` reads `silver_elexon_boal` with an inclusive predicate on `settlement_date` and drops the
  bitemporal columns (`gridflow_models/research/handles/source.py:401-449`, `schema_manifest.py:116`).
- `plot_alt`: `E_THMRB-1` 201, `E_WHTBB-1` 199, `E_NEWPB-1` 187, and `E_CHAPB-1` 143 in tenth place all reproduce.
- `record.caption`: the filter gives exactly 8 rows. 991 sits in periods 36 and 37; 993 and 994 in 37 and 38; 992
  only in 37. 995 spans 38 and 39, but the caption does not claim otherwise.
- Cadence: traces to the note body's "Publication lag: Near real-time as acceptance instructions are issued".
- Related notes:
  - disbsad has `so_flag` (`disbsad.py:72`), and the guidance says BSAD actions are SO-flagged too.
  - bmunits_reference has `fuel_type`, `registered_capacity_mw` and `company_name` (`bmunits.py:98-102`).
  - All four notes are 12 words or fewer.

**No local data, leakage and filler.**
- A grep of the rendered page text found no "locally", "held", "our", "since 20", "% of" or row/day counts. The
  "rows" hits are the caption's "however many rows it has" and the template's help card.
- There are no em dashes, middle dots, arrows, "live", "now" or planning labels.

**Build.**
- `gridflow-build --only elexon/boal` is green, and `detect.mjs --json` returns `[]`.
- The samples file has `generated_by: gridflow-sample`.
- The notebook JSON came from `run_notebooks.py`, and its cells are read-only with no error outputs.
- The column guide has 12 lines for the 12 non-pipeline columns, key columns first.

**Screenshots** (headless Chrome, port 9736, server stopped):
- 1440, 1024 and 768 full page. 390 as seven 390 px iframes at the page top and at `what-h`, `chart-h`, `raw-h`,
  `sv-h`, `gd-h` and `rel-h`.
- Nothing is clipped or overlapping at any width: hero turbines, scene edges, the chart's y-axis title (`count`) and
  ticks, the key notes, the code blocks, the frame and guide, the notebook panel, the corner labels and the related
  list.
- The site has no dark scheme (no `prefers-color-scheme` or `data-theme` in `site/hifi/assets`), so these are light
  only.
- The frame folds the level columns at every width. That is the known template limit, so it is not a finding. I did
  not shoot the frame unfolded.

## Method disclosure

- For the 390 check I wrote a temporary iframe harness, `site/hifi/_rev390.html`, into the front-end worktree's
  served folder. I deleted it straight after the screenshot and confirmed it is gone.
- Scratch scripts and screenshots are in the scratchpad (`boal_chk*.py`, `boal-rev/`).
- The Imbalance Pricing Guidance PDF was fetched to the session's tool-results folder to verify the quote.
- No other files were written. I ran no ingest, no live API and no git commands.
