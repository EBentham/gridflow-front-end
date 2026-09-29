# capacity-allocated-nominated: re-check

Family page `capacity-allocated-nominated`: lead `total_capacity_allocated`, member `total_nominated_capacity`. Checker: Opus 5.5 · high, 2026-09-29.

This is a focused re-check of the 8 findings in `capacity-allocated-nominated-review.md`, against the writer's report `capacity-allocated-nominated-author-2.md`.

## Verdict: APPROVE

All 8 findings are fixed. Nothing regressed, and there are no new findings.

## Major (finding 1): contract-series loss, fixed

- **`what_it_is`** now says: "GB replies carry three contract series, `A01`, `A06` and `A07`, and silver keeps only `A07`."
  - This matches review 1's reproduction. Every GB/FR, GB/NL and GB/BE nominated reply carries three TimeSeries in the order `A01`, `A06`, `A07`.
  - Silver equals `A07` in 336 of 336 hours per pair.
  - The parser never reads `contract_MarketAgreement.type` (`parsers.py:320-328`), and the dedup key has no contract column (`h6_market.py:91-99`).
  - "GB replies" is fair: GB/IE-SEM returns only Acknowledgements.
- **Member `differs`:** "silver keeps `A07` of three contract series (`A01`, `A06`, `A07`)". This is plain and accurate.
- **Notebook:**
  - The column is renamed `nominated_A07`. The re-run JSON's df header is `["", "timestamp_utc", "allocated", "nominated_A07"]`.
  - The rows are unchanged from the silver-verified values (859, 851, 36, 65, 255, 842 MW).
  - The plot legend reads `nominated_A07`.
- **The exceeds claim is scoped to `A07`:** "Allocated counts only earlier rounds (Art. 12(1)(c)), so `A07` can exceed it."
  - This is true in the window: 37 hours above 725 MW.
  - It also carries the attribution asked for in nit 2.
- **`plot_alt`:** "Nominated A07 (clay)…". Its values are unchanged and were verified in review 1.
- **Code meanings:** `A06` and `A07` meanings appear nowhere. "`A01` (daily)" moved to the lead's `differs` line, where it keeps its code source (`endpoints.py:324`).

## Nits 2 to 8: all fixed

| # | Check | Result |
|---|---|---|
| 2 | Cause attributed to Art. 12(1)(c) in the notebook lead | Fixed |
| 3 | Key note says "replies carry auction category `A04` (hourly), not `A01` (base)" | Fixed. The meanings match `entsoe-codes.md` §5 |
| 4 | Record caption says "either side of 22:00 UTC" | Fixed |
| 5 | Chart caption says "which gridflow repeats hourly (curve type `A03`)" | Fixed |
| 6 | Plot legend is outside the axes and covers no trace | Fixed. PNG is 877×369, checked visually |
| 7 | `how_used[2]` drops "and schedules"; the related note says "Scheduled exchanges (document type A09)" | Fixed. A09 is at `endpoints.py:152-153` |
| 8 | Vault bodies | Fixed. See below |

Finding 8 detail:
- **Nominated tuple row (line 42):** corrected.
- **Silver sample:** marked unverified and tied to the bronze sample's first TimeSeries.
- **2026-05-08 probe record (line 192):** the original wording is restored, with an observation scoped to the 2026-08 and 2026-09 replies.
- **Allocated note line 273:** the old cause is marked as contradicted by bronze.

## Regression checks

- **Mirrors:** both notes are byte-identical to the vault worktree.
- **Build:** `gridflow-build --only entsoe/total_capacity_allocated` succeeds. The chart series and sample were not rerun, and their digests still pass.
- **Detector** (absolute path): only `em-dash-overuse`, the accepted EIC-dash advisory.
- **Rendered text:** 0 em dashes, 0 arrows, 0 middle dots, 0 literal backticks (none in alt or aria text either), and no "live", "locally" or "our". All 7 new wordings are present.
- **Screenshots:** none retaken; this re-check changed no layout. I relied on the writer's timed 1440 and 390 shots, and on my own look at the new plot PNG.
