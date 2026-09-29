# congestion-management: author response to review 1

Writer: Opus 5.5 · high, 2026-09-29. This answers `congestion-management-review.md`, which found 1 major and 5 nits. The major and nits 2, 3, 4 and 6 are fixed; nit 5 is left as written, as the review allowed.

## Status

- **Notes:** I edited the canonical `redispatching_internal.md` (page block) and `congestion_management_costs.md` (body). All four notes are byte-identical to `vault/entsoe/`, with CRLF kept: 304/304, 177/177, 171/171 and 211/211 lines.
- **Artefacts:** not rerun. The chart spec, `record.select` and notebook cells are unchanged, so the digests still match.
- **Build:** `gridflow-build --only entsoe/redispatching_internal` passes with no deferred error.
- **Detector** (absolute path): only `em-dash-overuse`, the accepted EIC-padding advisory.
- **Rendered page:** 0 em dashes and 0 literal backticks. Each of the five new wordings appears once.
- **Screenshots:** none retaken. Only short strings changed, all within existing lines, and the layout did not change. I did not touch the port 9670 server.

## Findings and fixes

| # | Severity | Fix | Words |
|---|---|---|---|
| 1 | major | Costs note, Known issues, last bullet: the stale parenthetical about the missing view is deleted. The "start a day earlier" advice stays, now with the query run through `data.entsoe.query()` (the view exists after the seat's refresh). **1 to 31 July:** 465 rows, only the 30 Jul 22:00 (false July) and 31 Jul 22:00 (August) stamps, so July's real row is missing. **From 30 June:** 744 rows, 24 distinct keys. | none |
| 2 | nit | `chart_view.caption`: "Netherlands replies carry separate up and down series; silver keeps one per quarter-hour, and here every point is the down (`A02`) series." | 37/40 |
| 3 | nit | Cross-border `differs`: "`businessType=A46`; one border pair per series; the named line is not kept in silver". Countertrading `differs`: "`A91`; many replies are an Acknowledgement; data carries `B03`, one point per quarter-hour, `MAW`". Both proportions are gone. | 14/14, 14/14 |
| 4 | nit | `record.fields.quantity_mw`: "As sent (`MWH`); direction not recorded; forward-filled from the last point (`A03`)". | 12/14 |
| 5 | nit | `raw_feed.note`, "the Netherlands returns under three pairs": left as written. The review found it true in every populated reply and needed no action. | none |
| 6 | nit | `facts.grain`: "One row per interval start, zone pair, business type; costs once per daily partition". | 14/14 |

## Report correction

- In `congestion-management-author.md`, defect 6 (the missing catalogue views) is now marked RESOLVED by the seat's view refresh. It should not go into BACKLOG as open.
- Its `query()` coverage bullet described the catalogue as it was on the first pass. This file supersedes it.
- Defects 1 to 5 stand. The query run above re-confirms defects 3 and 4 through `query()`: the 30 Jul 22:00 false row is returned 279 times, with every month-row repeated once per daily partition.

## Summary

The stale costs-note parenthetical is gone and replaced by a working `query()` check, and nits 2, 3, 4 and 6 are fixed within budget. Mirrors are identical, the `--only` build passes and the detector shows only the accepted advisory.
