# National Demand Balancing Mechanism Units: writer's report, round 2

All eight review findings are fixed in the canonical note
`C:\gridflow-wt\vault-neso-dem\30-vendors\neso-data-portal\datasets\national-demand-balancing-mechanism-units.md`
(275 lines, all CRLF). It is mirrored to `C:\gridflow-wt\fe-neso-dem\vault\neso_data_portal\national-demand-balancing-mechanism-units.md`
and `cmp` is clean. The notebook was re-run because cell 6 changed: 6 cells, 6.8 s, no errors; the outputs of cells 3 to 5
are unchanged. The sample was not regenerated: `select` is unchanged, and the caption and guide are not part of its digest.
`gridflow-build --only neso_data_portal/national_demand_bmus` passes (only the unrelated global 37-line warning).
The detector returns `[]`. The rendered text has 0 em or en dashes, arrows or middle dots, and no "locally", "held",
"now" or "live". As instructed, I started no server and no background process, so there are no new screenshots. The
changes are short text edits that wrap in place, and a plot that lost its y-axis label.

## Fixes

1. **Major, `related[3]` (daily-demand-update):** now reads "Recent `ND` outturn, updated daily by NESO". That note's own
   cadence fact says "Daily, usually by 08:30 UTC, NESO says". The page no longer mentions a forecast tail.
2. **Nit, `related[1]` (historic-demand-data):** now reads "Half-hourly National Demand, which NESO says these units make up",
   so the claim is attributed to NESO.
3. **Nit, `record.fields.bm_name`:** now reads "BM unit name as NESO spells it; matches Elexon's `national_grid_bm_unit`
   where registered" (13 words). This is no longer false for `AG-PEPG01`.
4. **Nit, `record.caption`:** now reads "Eight names picked from the list, alphabetical, among them NESO's dictionary example
   `AG-ADL03E`."
5. **Nit, note body, Cadence:** added the observed fact. The 2026-10-16 refresh reported "1 unchanged since newest capture"
   (gridflow `.planning/phases/v0.22-close/refresh-20261016/ingest.log` line 226; I read it).
6. **Nit, `what_it_is`:** the definition is now sourced: "NESO's Historic Demand Data dictionary defines National Demand:
   it "is the sum of metered generation, ..."". To stay within the 60-word budget, I trimmed "no capacity, fuel or dates"
   to "The file holds unit names only."
7. **Nit, `how_used[2]`:** replaced the use that could not be done today with "See the units' Elexon fuel types by joining
   through the register." Notebook cells 5 and 6 already do this.
8. **Nit, notebook cell 6:** now `ax.set(xlabel="BM units on NESO's list", ylabel="")`. The re-run PNG has no `fuel_type`
   axis label. The bars are unchanged (445, 222, 142, 89, 47, 16, 14, 12, 12, 2), so `plot_alt` still holds.

## Defects

No new defects. The round 1 list stands: `query()` filters on capture time for reference tables; `gridflow-distil`
reports a written series file for a `type: none` spec although it writes none; 142 names are absent from Elexon's
register as fetched on 26 September 2026; the CKAN `size` differs from the delivered body.
