# elexon/freq: re-check 1

Checker: Opus 5.5 (high), 2026-09-29. This re-check covers the writer's "Revision 1" (`freq-author.md`), on the
worktree after merging main (`a9bd431`, which brings in `165ce0a`: lines break at absent periods, and `--only`
fails only on its own page).

## Verdict: APPROVE

No blockers, no majors, no nits.

## Previous findings

1. **major, `page.what_it_is`: fixed.** The sentence now reads "In responses gridflow has fetched, Elexon includes
   the sample at the window's end, so a day's file can end on the next midnight."
   - This scopes the claim to what we observed (14 of 14 bronze responses, plus the note's live check).
   - The two trims keep the meaning: "Measured GB system frequency", and "keeps `measurementTime` and `frequency`"
     (`freq.py:57-61`).
   - The rendered page shows the new text.
2. **nit, `page.notebook.needs`: fixed.** It now reads "16 and 17 September 2026" and renders as "Needs gridflow and
   gridflow-models installed, with 16 and 17 September 2026 ingested."
   - With 16 September's file present, the view's plain parquet glob returns 17 September 00:00 from two files.
   - That matches the duplicate row in cell 4's output.

## Widened commands, checked against the code

- **Ingest.** `gridflow ingest elexon freq --start 2026-09-16 --end 2026-09-18`:
  - `runner.resolve_dates` makes each bare date midnight UTC.
  - `client.py:93-99` (`PUBLISH_DATETIME`, `max_chunk_hours` 24) loops `while current < end`. That gives two calls,
    16T00Z to 17T00Z and 17T00Z to 18T00Z.
  - `_fetch_datetime_range` files each call under `data_date = start.date()`, so the bronze lands in folders 16
    and 17.
  - The comment "bronze; two 24-hour windows" is right.
- **Transform.** `gridflow transform elexon freq --start 2026-09-16 --end 2026-09-17`:
  - the end is inclusive, so it transforms days 16 and 17;
  - `FreqTransformer.read_bronze` reads only day D's folder, and no partition offsets apply;
  - so it writes `freq_20260916.parquet` and `freq_20260917.parquet`, which is what `needs` names.
- **Request example.** `raw_feed.requests` still shows the 17 September call. It is one of the two calls, so it is
  still correct.

## Nothing else broke

- **Build.** `uv run --system-certs --extra build gridflow-build --only elexon/freq` printed "wrote:
  data-sources/elexon/freq.html (dataset template)" and "rendered only ['elexon/freq']".
- **Detector.** `detect.mjs --json` returned `[]`.
- **Mirror.** `vault/elexon/freq.md` is `cmp`-identical to the vault note, which is still CRLF.
- **Artefacts.** The series is still `spec_origin: vault`, with 1,440 points used, and there is no staged spec. The
  build's digest check passed, and the chart, record and notebook cells are unchanged.
- **Chart after the merged renderer change.**
  - The data line is still one path: 1 `M`, 1,439 `L` in both the wide and narrow SVGs. The window has no absent
    period, so there is no break.
  - The ticks are unchanged: wide 49.7 to 50.3 with hourly 00:00 to 05:00, narrow 49.6 to 50.4 with 00:00, 02:00
    and 04:00.
  - The caption, alt and key note still match.
- **Characters.** No em dashes, middle dots or arrows in the page (checked by code point).
- **Widths.** CDP at true widths 1440, 1024, 768 and 390, with the notebook folded and then open with the frame
  unfolded:
  - `scrollWidth` equals the viewport at every width;
  - no element sits outside the viewport outside a scroll container;
  - no chart text sits outside its SVG.
- **By eye.** I viewed the revised "What it is", the chart and the raw feed at 390 and 1440, and all are fully
  visible. The shots are in `scratchpad/freq-review-shots/open-*.png` and `r2-*.png`, and the server on 9720 is
  stopped.
