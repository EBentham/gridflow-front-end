# lolpdrm: checker re-review 2 (2026-09-29)

**Verdict: APPROVE** (0 blockers, 0 majors, 0 nits). All three findings from `lolpdrm-review.md` are fixed as
"Revision 1" in `lolpdrm-author.md` describes, and nothing else changed.

## Findings from review 1

1. **Major, vault body Known-issues bullet: fixed.** The bullet now reads "file-name order (fetch time, then the
   first 8 hex digits of the body's SHA-256, `bronze/writer.py:33-34,57`; so fixed for a given bronze but
   unrelated to publish time)" (canonical note line 245). This matches `bronze/writer.py:33`
   (`sha256(response.body).hexdigest()[:8]`), `:34` (fetch-time stamp) and `:57`
   (`raw_{ts}_{body_hash}`). The rest of the bullet is unchanged. The author report's "different machines"
   claim is withdrawn.
2. **Nit, `page.summary`: fixed.** It now reads "Forecast, per settlement period, of loss-of-load probability
   and de-rated margin, published on BMRS and republished as each period draws nearer." It no longer attributes
   authorship. "Published on BMRS" is supported by the endpoint (`endpoints.py:225-226`) and the vendor fact.
3. **Nit, `page.facts.cadence`: fixed.** It now reads "Republished through the day, as the feed's publish times
   show". This is scoped to the feed and makes no undocumented "half-hour" claim. It is still true against
   bronze: 37 to 48 distinct `publishTime` per bronze day across all 14 days.

## Nothing else broke

- The canonical note and the mirror are identical (`cmp` clean, CRLF kept). The diff against `origin/master` is
  still 112 insertions and 5 deletions.
- The page fields verified in review 1 are unchanged: each distinctive string occurs exactly once. That covers:
  - the alt values;
  - both key notes;
  - the caption's "Each runs to 03:30 two days on";
  - both commands;
  - `record.key`;
  - `plot_alt`;
  - `notebook.needs`;
  - the body edits (`ingested_at`, SP10 at 03:30, dedup scope, Publication lag).
- The artefacts are untouched: series and samples keep their 00:32 timestamps, the notebook JSON and PNG their
  00:39 ones.
- `gridflow-build --only elexon/lolpdrm` wrote the page (dataset template, one distilled series), and the
  artefact digest check passed. `detect.mjs --json` returned `[]`.
- Rendered-text scan: no hits for locally, held, "since 20", "% of", N rows/days, em dash, middle dot, arrow,
  live, real-time, "Elexon's", random or day-ahead. The only "our " matches are inside words (four, hour).

## Hero check (the summary and cadence changed)

- **1440** (headless Chrome, port 9737): the summary wraps to four lines in the right column above the facts
  table. The Cadence value wraps to two lines. Nothing is clipped or overlapping. The scenery (turbine tops,
  offshore edge, labels) is fully visible.
- **390** (a true 390 px same-origin iframe): the summary runs to four lines and the Cadence value to two.
  The Key wraps cleanly. There is no horizontal overflow (`scrollWidth` equals the client width), and the
  scenery and labels are intact.
- The server on 9737 is stopped.
