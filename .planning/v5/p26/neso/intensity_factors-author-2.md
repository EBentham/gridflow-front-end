# neso/intensity_factors: author revision 2

Writer: Opus 5.5 (high), 2026-10-06. Answers `intensity_factors-review.md` (REVISE: 0 blockers, 2 majors, 4 nits). All six findings are fixed. The only edits are to the `page:` block of the canonical note; no body or artefact changes. The chart spec is untouched, so no re-distil was needed.

## Fixes

| # | Severity | Field | Before | After |
|---|---|---|---|---|
| 1 | major | `how_used[2]` | "Spotting a revised factor: silver keeps the newest fetch, bronze keeps each one." | Removed. `raw_feed.note` is kept as is, as the review asked. |
| 2 | major | `how_used[0]` | "Weighting a fuel mix into gCO2/kWh; `generation` needs gas and imports mapped first." | "Approximate mix weighting; `generation` lumps gas and imports, so assume one factor each." (13 words) |
| 3 | nit | `how_used[1]` | "A per-fuel emissions lookup for merit-order or dispatch models." | "A per-fuel factor lookup for approximate carbon-intensity features." This is the note's own Modelling-notes framing. |
| 4 | nit | `summary`, `facts.grain` | "... each fuel type, in gCO2/kWh: one table of 14 fuels."; "One row per fuel (`fuel`), its factor in gCO2/kWh" | "... each fuel type, labelled gCO2/kWh by gridflow: one table of 14 fuels." (20 words); "One row per fuel (`fuel`), its factor labelled gCO2/kWh by gridflow" |
| 5 | nit | `related[2]` (`elexon/fuelhh`) | "Half-hourly generation in MW by Elexon fuel-type code" | "Splits gas by cycle and imports by interconnector, closer to these factors" (12 words). The review checked the split in `fuelhh` silver: `CCGT`, `OCGT`, `INTNED`, `INTFR`, `INTIRL` and others. |
| 6 | nit | `facts.cadence` | "The whole table per call; `sources.yaml` declares it weekly" | "One call returns the whole table; gridflow's schedule fetches it weekly" (`config/sources.yaml:626-629`) |

Notes on the choices:
- **`how_used` now has two items.** That is inside the build's 2-to-3 rule. I did not add a third use, because every candidate either rests on unverified revision behaviour or needs the `fuelhh` interconnector mapping. That mapping covers only some interconnectors, so it would need its own evidence.
- **The "assume one factor each" wording (finding 2)** states the gap without naming a method. The chart beside it shows the spread the assumption has to choose from: gas 394 or 651, imports 53 to 474.

## Checks run

- Canonical note edited with the Edit tool. 218 lines, all CRLF.
- Mirror: `cp` to `vault/neso/intensity_factors.md`, then `cmp` equal.
- `uv run --system-certs --extra build gridflow-build --only neso/intensity_factors`: wrote the page with no errors. This time there were no out-of-scope sibling errors either.
- `node C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json <abs path>/site/hifi/data-sources/neso/intensity_factors.html`: `[]`.
- Em dashes 0.
- Leakage grep (`locally|held|our|live|now|real-time|yet|soon|planned|coming|static|merit-order`): no hits. The one "revised" left is in `raw_feed.note`, kept per the review.
- All five new phrases are present in the rendered HTML.
- Screenshots (headless Chrome, every call under `timeout 60`, 390 as a 390 px iframe, my port 9869 server stopped; 9670 untouched):
  - 1440: hero, topsoil, related list.
  - 390: hero, topsoil, chart, raw feed.
  - Nothing clipped or overlapping.
  - Files: `scratchpad/if_shots/v2_1440_top.png`, `v2_1440_low.png`, `v2_390_m.png`.

## Unchanged

- Chart, series, sample and notebook artefacts.
- Note body.
- Defects section of the first report. The review's added observation goes to the seat: `neso/intensity_stats` states gCO2/kWh as fact in its related note.

All six review findings fixed in the page block; mirror byte-equal, build clean, detector [].

**Nits fixed (review 2, 2026-10-07):** `how_used[0]` now names its result: "Approximate carbon intensity of a mix; `generation` lumps gas and imports, so assume factors." (14 words). Canonical note edited (218 lines, all CRLF), mirror `cp` then `cmp` equal, `gridflow-build --only neso/intensity_factors` wrote the page with no errors, detector `[]`, em dashes 0.
