# congestion-management: checker re-check (review 2)

Family page `congestion-management`, lead `redispatching_internal`. Checker: Opus 5.5 · high, 2026-09-29. This is a focused re-check of `congestion-management-author-2.md` against `congestion-management-review.md`. I left the port 9670 server running and wrapped every Chrome call in `timeout 60`.

## Verdict: APPROVE

No findings above nit remain.

## The major, finding 1: fixed

- **The stale sentence is gone.**
  - `congestion_management_costs.md` no longer says the catalogue had no view or that `query()` could not be run.
  - A grep for `catalog|could not be run|view` over the note returns nothing.
  - The body text was the only place this problem appeared.
- **The new query receipt is reproduced exactly.** I applied `query()`'s own predicate (`_get_method_registry.py:94-96`: `timestamp_utc >= start 00:00Z AND < (end + 1 day) 00:00Z`) to silver `congestion_management_costs` with Polars.
  - **1 to 31 Jul:** 465 rows. Only two stamps appear: 2026-07-30T22:00Z (279 rows = 9 false keys × 31) and 2026-07-31T22:00Z (186 rows = the 6 August keys × 31). July's real row, stamped 2026-06-30T22:00Z, is not returned.
  - **From 30 Jun:** 744 rows and 24 distinct keys, including the 279 rows stamped 2026-06-30T22:00Z.
- **Mirrors:** all four canonical notes are byte-identical to `vault/entsoe/` (`cmp`).

## The nits

- **Finding 2, `chart_view.caption`: fixed.** It now reads "Netherlands replies carry separate up and down series". That is true of every populated reply containing NL: 63 of 63 carry both `A01` and `A02`.
- **Finding 3, member `differs`: fixed.**
  - Cross-border: "the named line is not kept in silver" (`h6_market.py:107-117`).
  - Countertrading: "many replies are an Acknowledgement; data carries `B03`...". Both proportions are gone.
- **Finding 4, `record.fields.quantity_mw`: fixed.** It now reads "As sent (`MWH`); direction not recorded; forward-filled from the last point (`A03`)", which matches `parsers.py:578-600`.
- **Finding 5, `raw_feed.note`:** left as written, as review 1 allowed.
- **Finding 6, `facts.grain`: fixed.** It now reads "One row per interval start, zone pair, business type; costs once per daily partition". This matches the dedup key (`h6_market.py:91-99`) and the costs copies (24 keys × 31).

## No regression

- **Build:** `gridflow-build --only entsoe/redispatching_internal` exits 0. The only output is the three legacy "silver schema rows empty" warnings; there is no error.
- **Detector** (absolute path): only `em-dash-overuse`, advisory, the accepted EIC-padding item.
- **Rendered HTML:**
  - Each new wording appears once.
  - The old wordings are absent: "most replies", "mostly empty", "holds until the next point" and "Replies carry up".
  - There are 0 em dashes.
- **Layout (CDP, `file://`, no server started):**
  - `scrollWidth` equals the width at 390 and 1440, with the frame unfolded.
  - The 1440 document grew from 4,820 to 4,864 px because the longer caption and grain lines wrap.
  - The screenshot of the hero facts, the "What it is" block and the chart caption shows the new grain and caption lines wrapping cleanly, with nothing clipped or overlapping.
- **Artefacts:** the chart spec, `record.select` and the notebook cells are unchanged, and the build's digest check passes. The writer's claim that no re-distil was needed holds.

The major is fixed and its new `query()` receipt reproduced (465 rows for 1 to 31 Jul; 744 rows and 24 keys from 30 Jun), all four nits are fixed, the build and detector are clean, and nothing regressed: APPROVE.
