# Current BSUoS charges: writer's report, round 2

All four nits from `current-balancing-services-use-of-system-bsuos-data-review.md` are fixed. The canonical note is still
CRLF (diff: 157 insertions, 2 deletions against the base). The mirror is identical (`cmp`). `gridflow-build --only
neso_data_portal/current_bsuos_ii` is clean. Detector `[]`. Em dashes: 0.

| # | Field | Fix |
|---|---|---|
| 1 | `how_used[2]`; notebook cell 5 `ylabel`; `plot_alt` | Use line now reads "Compare the actual cost and recovery columns row by row, as NESO publishes them." The plot's y label is "actual BSUoS cost per row, £". `plot_alt` opens "the actual BSUoS cost on each settlement-period row". The notebook was re-run because the cell changed. Its numbers are unchanged. |
| 2 | `record.select` | Added `dedup: {"on": [settlement_date, settlement_period, run_type], order_by: published_at}`. Sample regenerated: still eight rows, same values. |
| 3 | `family.members[current_bsuos_historic_ii].differs` | Now reads "Yearly files: no rows 18 April 2024 to 31 March 2025; April 2025 twice". Vault body: one sentence added to the "Historic II resource names" bullet stating the gap, checked 2026-10-23 (the 2023-2024 file ends 2024-04-17, the 2025-2026 file starts 2025-04-01). |
| 4 | `family.members[current_bsuos_historic_rf].differs` | Now reads "Reconciliation Final yearly files; two periods 27 March 2022 never had are dropped". |

Screenshots were not retaken. Every change is wording in sections already checked at all four widths, and the two
member lines are shorter than before. No server was started this round.

## Defects (additions to round 1)

5. **Vendor, Historic II coverage (low):** NESO's Historic II files have no Interim Initial rows for settlement days
   2024-04-18 to 2025-03-31. The file labelled 2024-2025 (`current_ii_bsuos_data.csv`) holds only 2025-04-01 to
   2025-04-13, and those rows repeat the 2025-2026 file. Settlement Final and Reconciliation Final cover that year. Add
   it to the existing vendor question on the mislabelled upload.
6. **Observation (checker's, not examined):** the Settlement Final cap workbook's `half_hourly_charge` differs from the
   historic SF `half_hourly_charge` on some joined keys (maximum £437,039), while the price matches exactly.
