# System inertia cost (`system-inertia-cost`): writer's report, round 2

All six review findings are fixed in the canonical note
`C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\system-inertia-cost.md`, mirrored to
`C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\system-inertia-cost.md` (`cmp` clean; LF, as committed).
`gridflow-build --only neso_data_portal/system_inertia_cost` writes the page with no errors of its own. The build
also reports "1 error(s) on pages not rendered by --only", which comes from another writer's notes in progress in
the shared worktree (`gis-boundaries-...` and `stability-midterm-...` are mid-edit), not this page. Detector `[]`.
Rendered text: 0 em or en dashes, arrows or middle dots. No notebook cell changed (only `plot_alt`), so the notebook
was not re-run; the build's notebook digest check passes. No server or background process started this round.

## Fixes

1. **major, `page.what_it_is`: NESO's unit disagreement now stated plainly.** New text (60 words): "NESO divides the
   day's cost of Balancing Mechanism offers tagged for inertia by the day's inertia shortfall summed over settlement
   periods: a rate, not a total. NESO's unit text varies: £ per GVAs in its notes and field unit, £ per GVA in its
   description, £/GVA.s in its worked method, used here. NESO does not say what a zero means." Sources: package notes
   open "(in £ per GVAs)" and use "£/GVA.s" in step 3 and both worked examples (catalogue snapshot
   `20261006T195819Z`); field info `20261008T114228Z\system_inertia_cost.json`: unit "£ per GVAs", description
   "(£ per GVA)". To fit the budget, I dropped the sentence on tagging (most likely main reason, best endeavours) and
   "whole pounds"; neither is load-bearing elsewhere on the page. Chart unit `£/GVA.s` and the field guide's "£ per
   GVA.s" now follow from the stated choice. My round-1 report said the notes write £/GVA.s; they write both, as above.
   Body fix with it (the review's aside): the Units bullet credited "(£ per GVA)" to the legacy dictionary; it now
   says the epoch-2 field description reads "(£ per GVA)" (field-info snapshot of the 2026 resource), and the notes
   give "£ per GVAs" then "£/GVA.s".
2. **nit, `page.raw_feed.note` and `commands[0].comment`.** "The 2026-27 file is not loaded" is now "The 2026-27 file
   stays in bronze: its one date, `01/04/2026`, breaks its filename's date format." (bronze holds its 45-byte capture;
   the resource-level hold keeps it from silver). Ingest comment restored to the sibling wording "whole files; window
   must end recently" (`client.py` `_assert_window_admissible`, check 4 bounded by `max_incremental_lookback_hours`).
3. **nit, `page.notebook.plot_alt`.** "then near 3,000 to 4,000" is now "then mostly about 2,000 to 5,000" (review's
   figures: 437 of 533 priced days, April 2023 to March 2026, fall in 2,000 to 5,000).
4. **nit, `page.how_used[2]`.** Now "Counting the days each financial year that carry a price above zero."
5. **nit, `page.chart_view.caption`.** Added "Most other quarters have more zero days." (40 words). Checked on silver:
   of the 36 whole quarters from April 2017 to March 2026, 34 others have a larger share of zero days than April to
   June 2025 (33%), one has a smaller share. The chart series is unchanged, so no re-distil.
6. **nit, report Defects wording.** Reworded below: "non-zero" spend, framed as a question for NESO, with the
   25 July figure the review supplied.

## Defects (replaces round 1's section)

- **NESO data: one isolated extreme inertia price.** `system_inertia_cost` silver (bronze 2026-10-08, 2025 resource
  `a6a52241-1774-48d8-935f-2bef0d843e18`): 2025-07-25 carries `cost_gbp_per_gvas` 58,570 £/GVA.s, four times the
  highest value on any other day in any file (14,650 on 2022-03-09); 24 and 26 July are zero. The column has no range
  rule. For context, `constraint_breakdown` shows £16,170 (27 MWh) of "increasing system inertia" spend that day
  against £133,709 on 27 July: a small spend fits a small shortfall behind the 58,570 but does not prove it.
  Question for NESO: is the value valid? Until it is answered, any yearly mean or max of this table is driven by one
  day. Logged in the note's Known issues.
- **NESO metadata: unit text varies for one quantity.** The `Cost_per_GVAs` dictionary entry's unit is "£ per GVAs"
  while its description says "(£ per GVA)"; the package notes open with "£ per GVAs" and then use "£/GVA.s" in the
  method and worked examples. Settled for this table by the worked method (ruling 642) and stated on the page.
  Question for NESO: confirm £ per GVA.s and correct the description.
- **NESO data: what a zero price means is undocumented (known, INERTIA-COST-ZERO).** Evidence for the question, not
  an error in either table: the price (accepted offers tagged inertia over the day's shortfall) and the constraint
  breakdown's `increasing_system_inertia_cost_gbp` (spend on actions raising inertia, 8 negative values) are not
  defined to coincide. On the 3,280 dates both carry (latest capture per date), a zero price meets zero spend on
  2,117 and a non-zero price meets non-zero spend on 1,035; on 70 a non-zero price meets zero spend and on 58 a zero
  price meets non-zero spend. Question for NESO: what does a zero price mean, and why do the two differ on those days?
