# Constraint breakdown: checker's re-review (Revision 1)

**Verdict: APPROVE.** The major and the four fixable nits are fixed, the axis floor stays a template matter, and the
changed lines introduce nothing new.

## Gates

- `gridflow-build --only neso_data_portal/constraint_breakdown`: succeeds, no content errors.
- Detector on the rendered page: `[]`. Em dashes 0, arrows 0 (rendered page); 0 em dashes in the `page:` block.
- Mirror `vault/neso_data_portal/constraint-breakdown.md` byte-equal to the canonical note (`cmp` clean).
- Artefacts untouched (the writer changed words only; the chart series, sample and notebook inputs are unchanged, and
  the build's digest checks pass).

## The six findings

1. **Major, `page.facts.grain`: fixed.** Rendered hero now reads "One row per date and capture; read the `_latest`
   view for one per date". The sentence is complete, says a date can appear more than once, and names the view that
   returns one row per date. That claim is true: the view returns 3,480 rows for 3,480 dates (checked in round 1), and
   the notebook lead and chart caption describe the same view.
2. **Nit, key note: fixed.** "Largest of the four by summed cost in every April-to-March year (2026 part-year). Below
   zero on five dates." Matches the notebook table (thermal largest in all ten rows by yearly sum; 2026 is 1 April to
   11 October) and the series (five values below zero).
3. **Nit, `reducing_largest_loss_cost_gbp` guide line: fixed.** "Reducing largest loss, £: cutting the largest credible
   loss (NESO); zero in these rows." Scoped to the rows; all eight rows show 0.0 when the frame is unfolded. "Cutting"
   is a fair paraphrase of NESO's dictionary ("reduce the level of the generation or demand that comprises the largest
   loss").
4. **Nit, caption: fixed.** "NESO's 2025-26 file has no row for 8 April 2025." Scoped to the file; true of the captured
   body (364 rows, the only missing date in the window).
5. **Nit, axis floor: the template reasoning holds.** The five negatives (largest -232,717) set the floor at -20 M
   because `chart_svg.nice_ticks` floors the low end to a whole step; the page cannot change that without hiding or
   clipping the negatives, which the author brief forbids. No page change is right. Already reported to the seat as a
   template problem.
6. **Nit, stale body sentences: fixed.** "At activation" added to the "Downloads and captures" line, the bold
   "Eligible. Silver at activation: 3,470 rows" line and the Cadence paragraph, which now also points to the
   2026-10-16 second capture (true: the 2026-27 resource has two captures in silver). The remaining 3,470 figures are
   inside the dated "Measured on silver (2026-10-10)" block or scoped by "at activation", so none is stale.

## New findings

None. The changed lines are within their word budgets (the build passes), contain no local counts or dates beyond the
dated, scoped body text, no planning words, and no dashes. The page's facts, chart and notebook values were not touched
and still match silver as checked in round 1.
