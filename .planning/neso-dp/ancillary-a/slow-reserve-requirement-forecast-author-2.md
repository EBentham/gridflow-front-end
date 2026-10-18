# Slow Reserve requirement forecast: author report, round 2

Fixes for `slow-reserve-requirement-forecast-review.md` (REVISE: 1 major, 3 nits). Writer, 2026-10-18.

## Fixes

1. **Major, `page.chart_view.caption` and `page.chart_view.alt`:** both now say the negative requirement is 1,800 MW.
   Caption: "Silver `slow_reserve_requirement_fc`, MW: the positive requirement, mean of each service day's windows,
   23 September to 31 October 2026, file last modified 22 September 2026, split by production date. Negative, not
   drawn, is also 1,800 MW in every window." (37 words, within 40.) Alt adds: "The negative requirement is the same,
   1,800 MW throughout." Evidence unchanged: silver unique negative `[1800.0]` on all 1,874 rows.
2. **Nit, `page.record.fields.service_window`:** "`1` to `48`; 25 October adds `5x`, `6x`; NESO's dictionary omits
   `5`, `6`". This keeps the 25 October scope and gives the same warning as the Quick Reserve page (NESO's dictionary
   comment: "for BST to GMT clock change day there is no service window 5 or 6").
3. **Nit, `page.facts.cadence`:** "Updated monthly (NESO's catalogue); each auction is daily", the approved Quick
   Reserve wording. The catalogue says the auction is daily and the data set is updated monthly.
4. **Nit, `page.notebook.lead`:** "Reads the `_latest` view, the newest capture, with `data.sql` so the cells see every
   day the file holds; `query()` reads the same view but takes a date range." This matches `_RELATION_NAME_BY_DATASET`
   (`..._fc_latest`) and `_date_range_predicate` (`service_delivery_date BETWEEN`).

## Re-checks

- Canonical note edited with the Edit tool; CRLF kept; vault diff against `origin/master` still +124 / -4. Mirror
  copied, `cmp` equal.
- `gridflow-build --only neso_data_portal/slow_reserve_requirement_fc`: success, within every word budget (only the
  known dropped-caveat warning). Artefact digests pass: series, sample and notebook files untouched (no chart, select or
  cell changed).
- Detector: `[]`. Built page: 0 em dashes; the four new strings are present.
- I looked at a 390 px iframe and 1440 after the edits (caption, key, frame, guide): nothing clipped or overlapping.
- I served on 9946 and stopped it. 9670 not touched. No git writes.
