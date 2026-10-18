# EAC auction results (`eac-auction-results`): author revision 2

Writer, 2026-10-18, answering `eac-auction-results-review-2.md` (REVISE: 1 major, 2 nits).

## Status

`gridflow-build --only neso_data_portal/eac_results_summary` succeeds. The detector returns `[]`, and the page has 0 em
dashes. The note has 1,257 lines, all CRLF; the mirror `cmp` is equal. No notebook cell changed (only the lead), so the
notebook was not re-run. The series and sample are unchanged.

## Fixes

1. **Major** (`page.record.fields.delivery_end`): now "Window end, UTC; mostly four hours for response, half an hour
   for reserve" (13 words). Response windows on the five clock-change days run 3 or 5 hours: 18 rows at 3 h, 12 at
   5 h, 38,850 at 4 h.
2. **Nit A** (canonical note, "Column meanings", `auctionID`): added NESO's dictionary line "All products auctioned in
   the same market", cited to `field-info/20261008T114228Z/eac_results_summary.json`. This puts the source of the
   `auction_id` field line in the vault.
3. **Nit B** (`page.notebook.lead`): "`data.sql` then stacks the FY and current summaries" (it is a `UNION ALL`).

The rendered page carries both new phrases. Nothing that sets width changed, so I did not re-take the screenshots.

## Defects

Unchanged from `eac-auction-results-author.md` "Defects".
