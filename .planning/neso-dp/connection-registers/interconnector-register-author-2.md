# Interconnector register: writer report, round 2 (2026-10-24)

Response to `interconnector-register-review.md` (REVISE: one major, four nits) and the seat's rulings. All fixes are in
the canonical note `C:\gridflow-wt\vault-neso-cr\30-vendors\neso-data-portal\datasets\interconnector-register.md`
(CRLF 421 of 421 lines), copied to the mirror and `cmp` identical. Notebook rerun; build
`--only neso_data_portal/interconnector_register` clean; detector `[]`. The chart spec and record selection did not
change, so the series and sample files did not change.

## Fixes

1. **Major, `page.record.fields.mw_import_total`.** Now "NESO: import contracted across all stages, firm TEC, MW;
   Moyle rows read 475, 500". The "across all stages" wording is attributed to NESO, and Moyle's two values are given
   as the frame shows them (stage 1, then stage 2, 16 October file), with no explanation of the difference.
   `mw_export_total` gets the same treatment: "NESO: export contracted across all stages, MW; Moyle rows read 500, 500".
2. **Nit, basis for the Moyle overlap.** The caption now gives the basis: "Moyle counts once, by its stage 2 row: its
   500 MW matches the TEC NESO gives Moyle." `what_it_is` now says the stage rows "read as cumulative", so it describes
   what the rows show rather than stating a NESO rule.
3. **Nit, import over export.** Key note: "Construction is NESO's Under Construction/Commissioning. Import is NESO's
   firm TEC; export totals by status run higher" (export by status is 4,135 / 11,097 / 26,904 / 1,470, each above the
   import figure, and is shown in notebook cell 4).
4. **Nit, Moyle's past dates.** `page.record.fields.mw_effective_from`: "Contracted effective date, future only per
   NESO; Moyle's 16 October rows show 2022". The line is dated and gives no explanation.
5. **Nit, stale first-capture lines in the note body.** The "Silver as of 2026-10-16" section now opens with "First
   capture only (the 5 October 2026 file)" and points to the "Second capture" subsection. The capture bullet, the
   NeuConnect effective-date clause and the Gate bullet are each marked first capture, with the 16 October values.
   **Notebook cell 5** now takes its span from the data, `range(year.min(), year.max() + 1)`, instead of hard-coding
   2027 to 2037. Today's output is unchanged (2027 to 2037, 2034 at 0), so `plot_alt` stands.

## Not re-checked

No new screenshots this round. Only wording changed: the guide lines, the caption and the key note are wrapping text,
and the chart, frame and notebook layout are as reviewed (nothing clipped at 1440, 1024, 768, 390 in round 1).

## Round 2 nit (after approval)

- `page.chart_view.caption`: the Moyle basis now names its source and date: "its 500 MW matches Moyle's TEC in
  NESO's package description (captured 6 October 2026)" (catalogue snapshot 20261006T195819Z). Caption is 40 words, at
  budget. Only the caption changed; mirror `cmp` identical, build clean, detector `[]`.
