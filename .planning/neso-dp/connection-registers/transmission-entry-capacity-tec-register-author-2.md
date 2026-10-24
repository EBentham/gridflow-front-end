# Transmission Entry Capacity (TEC) register: writer's round 2

Fixes for the checker's review (1 major, 4 nits) under the seat's rulings. Canonical note edited with the Edit tool
(CRLF kept, 538/538), mirrored and `cmp` identical. Build `--only neso_data_portal/tec_register`: OK. Detector `[]`.
Em dashes: 0. No artefact changed (all edits are page words, not the chart spec or notebook cells).

1. **Major, `page.what_it_is`:** added one dated, plain sentence with no codes: "This page stops at NESO's 5 October
   2026 file: gridflow cannot read the dates in its 16 October file." Kept within 60 words by trimming the rest.
2. **Nit, `page.chart_view.caption` and `alt`:** the label no longer implies the future. Caption: "Contracted
   increases, not built capacity; some effective dates are already past. No value is negative." Alt: "contracted
   TEC increases in MW, some with effective dates already past". No new number added (the 96-row, 17,057 MW share
   is not visible in the chart or rows, so it is worded, not stated).
3. **Nit, TEC definition:** the unattributed "MW a customer is contracted to inject into the transmission system"
   sentence is gone; `what_it_is` now opens "NESO's list of projects holding Transmission Entry Capacity contracts",
   which is the package description's own wording. The round 1 evidence-table row attributing the definition to the
   package description was wrong; this replaces it.
4. **Nit, `page.record.fields.plant_type`:** "several are joined by semicolons" (no lone `;`).
5. **Nit, `page.notebook.needs`:** now "NESO's TEC register file of 5 October 2026", so the reader sees which file the
   outputs come from; `what_it_is` and the raw feed note say why a newer file does not load.

Unchanged by ruling: the `cumulative_total_capacity_mw` guide line ("in these rows, the running total to this
stage").
