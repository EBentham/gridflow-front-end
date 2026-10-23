# Outturn voltage costs: writer's report (round 2, 2026-10-23)

Answers `outturn-voltage-costs-review.md` (REVISE: 1 major, 6 nits). Every finding fixed in the canonical note
`C:\gridflow-wt\vault-neso-cm\30-vendors\neso-data-portal\datasets\outturn-voltage-costs.md` (433 lines, all CRLF), mirrored to
`C:\gridflow-wt\fe-neso-cm\vault\neso_data_portal\outturn-voltage-costs.md` (`cmp` clean). Notebook re-run with
`scripts/run_notebooks.py` (cell 1 changed; 5 cells, no errors, outputs unchanged in value). Chart spec and record selection
unchanged, so series and sample were not regenerated (build digest checks pass). Build `--only
neso_data_portal/outturn_voltage_costs_main` clean (the 35-line caveat warning is global); detector `[]`; 0 em dashes; the word
"current" no longer appears on the built page. No server or background process started this round.

| # | Finding | Fix |
|---|---|---|
| 1 major | 2025-26 called the "current" file | `family.members[0].differs`: "NESO's newest file, 2025-26: April and May 2025 only; updates paused (October 2026)". Chart caption: "The newest file's months are not drawn." Notebook variable `cur` renamed `newest` |
| 2 | Utilisation-only wording not attributed | `what_it_is`: "NESO notes utilisation costs here are only Obligatory Reactive Power Service payments, allocated per group". `record.fields.utilisation_costs_gbp_m`: "Utilisation costs, £m: per NESO, only Obligatory Reactive Power Service payments, allocated per group" |
| 3 | "never share a month" as a universal | `what_it_is`: "Each file covers one financial year, so none share a month." Notebook lead: "Files are financial years: stack, never add." |
| 4 | Pause undated; file extent unstated | `facts.cadence`: "Monthly, as NESO's catalogue lists it; its October 2026 note says updates are paused" (catalogue snapshot 2026-10-06). Member `differs` now says the file holds April and May 2025 only (NESO datastore total 38 = 2 months x 19 groups; field-info snapshot 20261008T114228Z; both months visible in notebook output) |
| 5 | Chart title read as a total | `chart_view.title`: "Sync and utilisation costs, April 2014 to March 2025" |
| 6 | Notebook lead did not say which column holds the month | Lead: "Take the month from `settlement_month`; `start_utc` is its first settlement period's start, converted from UK time." |
| 7 | "within limits" presented as NESO's wording | `what_it_is`: "the outturn cost of maintaining voltage levels on the network". Canonical body's first sentence corrected the same way (it called "keeping voltage ... within limits" vendor wording; NESO's note says "maintaining voltage levels on the network") |

## Not changed

- Screenshots from round 1 still stand for layout. The changed strings are similar in length or shorter (the member `differs`
  is 13 words, the chart title 9), and no new long tokens were added. Not re-shot because this round allowed no server.
- Defects as in round 1: two tiny negative historical sync costs with no NESO sign convention; the 2025-26 file stalled at May
  2025 under NESO's pause note. No gridflow code defect.

Summary: all 7 review findings fixed (newest file, attributed utilisation wording, file-scoped month claim, dated pause with
April and May 2025, title, month column in the notebook lead, NESO's own voltage wording); build clean, detector `[]`.
