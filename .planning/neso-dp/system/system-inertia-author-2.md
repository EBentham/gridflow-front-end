# System inertia (`system-inertia`): writer's report, round 2

Fixes for the three nits in `system-inertia-review.md` (verdict APPROVE). Canonical note
`C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\system-inertia.md` (281 lines, all CRLF); mirror
`C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\system-inertia.md`, `cmp` clean.

## Fixes

1. `page.how_used[0]`: "how far NESO's actions lifted them above the market outcome" is now "how far NESO's actions
   moved them from the market outcome". No direction is claimed, because outturn is below market-provided in 13,616 of
   162,424 periods (the checker's count).
2. Note body, "Units and value semantics": "Clock-change days carry 46 or 50 periods" now adds "except 2022-10-30,
   which carries only periods 1 and 2", matching the two Known issues bullets edited in round 1.
3. `page.record.fields`: `outturn_inertia` now reads "GVA.s (NESO writes GVAs)"; `market_provided_inertia` ends
   "GVA.s" with no attribution. Nothing on the page attributes the spelling "GVA.s" to NESO.

## Gates

- `gridflow-build --only neso_data_portal/system_inertia`: passes. These are word changes only, so the series,
  sample and notebook digests are unchanged and nothing was re-distilled or re-run.
- Detector `[]`. The rendered page contains neither "lifted" nor "GVA.s (NESO)".
- No server or background process was started this round. Screenshots were not retaken: two guide lines and one
  how-used line changed, with lengths close to the originals.

## Defects

None new. The two NESO data defects from round 1 stand: five whole low days, and 21 days with only periods 1 and 2.
