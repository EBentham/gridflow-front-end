# BSAD forward contracts page: author report, revision 1

Response to review 1 (REVISE: 2 majors, 5 nits) and the seat rulings. Written 2026-10-18.

## Gates after the revision

- `gridflow-build --only neso_data_portal/bsad_forward_contracts` succeeds. Its only message is the caveat-grammar warning, which is a seat item.
- `detect.mjs --json` returns `[]`. The page has 0 em or en dashes, middle dots or arrows.
- The mirror `cmp` is clean, and the canonical note keeps CRLF on all 393 lines.
- No artefact was re-run, because the chart spec, sample select and notebook cells are unchanged. `notebook.needs` is a page field, and the build's digest checks pass.
- I re-screenshotted the hero, "What it is", "How it's used" and the chart at 390 (390 px iframe). Nothing is clipped. The page text confirms the new `what_it_is`, `how_used[1]` and `needs` wording, and that the old capture sentence is gone.

## Findings

| Finding | Fix |
|---|---|
| 1 (major): `what_it_is` cited our captures | Replaced with the seat's wording: "NESO's current-year file can show its newest days as zero and fill them in a later upload." It has no dates or counts. To stay within 60 words I also dropped "taken" and folded nit 7's optional point in: "Each row is a settlement-period total, not a contract: net buy and sell price adjustments, cost (£) and volume (MWh), and gross volumes traded." |
| 2 (major): body said silver covers to 2026-10-08 | Now reads "Silver covers settlement days `2017-04-01` to `2026-10-08` at activation (`2026-10-17` with the later capture below)". The body agrees with the Later capture paragraph. |
| 3 (nit): the "never deduplicate" bullet stood beside a chart that deduplicates | The bullet now gives both figures: 149,424 distinct pairs "at activation", and the latest view's 149,856 rows holding 149,856. It adds: "The site chart deduplicates on `(date, period)` by `available_at` only because of that disjointness: it keeps the newest capture of each resource." |
| 4 (nit): "populated" rows after capture | The text now says "non-blank rows" and adds "all of them zero in every value column". Checked with Polars: 27 and 55 rows, 0 with a non-zero value. |
| 5 (nit): "as the methodology's later inclusion of contracts allows" | Dropped, because I cannot quote the source. It now reads "(observed; `TODO: verify` the cause with NESO)". |
| 6 (nit): `notebook.needs` lacked the 2020-21 exception | Now "a capture of NESO's yearly files from 2017-18 except 2020-21". It renders as "...with a capture of NESO's yearly files from 2017-18 except 2020-21 ingested." |
| 7 (nit): `how_used[1]` implied when trades were struck | Now "Which settlement periods carry the forward buying and selling." The optional "settlement-period total, not a contract" wording is in `what_it_is` (see finding 1). |

Nothing else in the note changed.

## Defects

No new defects. The defects in the first report stand. The vault-note defect now covers the coverage line fixed here.
