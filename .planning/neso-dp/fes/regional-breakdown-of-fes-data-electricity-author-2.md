# Regional breakdown of FES data (Electricity): writer's report, round 2

This answers `regional-breakdown-of-fes-data-electricity-review.md` (REVISE: 2 majors, 6 nits) and the seat's rulings.
All edits are on the canonical note in `C:\gridflow-wt\vault-neso-fes` (CRLF kept, 1,016 of 1,016 line ends) and in my
round-1 report. The chart spec, sample and notebook are unchanged, so no artefact was regenerated (the build's digest
check passes).

## Gates

- `gridflow-build --only neso_data_portal/fes_regional_demand_active_power`: exit 0. The only warning is the known
  37-line caveat-grammar one.
- Detector `[]`. No em dashes on the page.
- Mirror `cp` + `cmp`: clean.
- Rendered check at 1440 and in a 390 px iframe: the new title, caption and longer key note wrap cleanly with nothing
  clipped. Server on 9941, PID 59203, stopped by that PID.

## Fixes

1. **Major, the `HT` name.**
   - `chart_view.title` is now "Summed peak demand projected, FES 2024 HT, 2025/26 to 2050/51". The code is unnamed
     in the title.
   - `key[0].note` is now "`HT`, read as Holistic Transition from NESO's FES 2024 pathway names (2 August 2024); not
     decoded here".
   - The alt text says "pathway HT (read as Holistic Transition)".
   - `record.fields.scenario` says plainly "NESO's dictionary here decodes only 2021's `LW`, `CT`, `ST`, `SP`".
   - Note body (lead section): the tRESP sentence no longer says "abbreviate". It now says the FES 2024 building-block
     file carries full names and no codes; that the tRESP dictionaries (last modified 2026-01-30, tRESP pathways, not a
     FES edition) write "Holistic Transition (HT)"; and that `HT` is therefore read as Holistic Transition by its
     initials, with NESO not decoding it for this package.
2. **Major, report counts.**
   - Round-1 report "Defects" now gives the measured counts, re-run on silver today:
     - `DemandPk` is negative on residential rows only: 868 / 210 / 87 / 146 (2021 to 2024), minimum -0.625 MW.
     - `DemandAM` in 2021: C 248, I 3,934, R 916; then R only at 1,312 / 924 / 174.
     - `DemandPM` in 2021: I 6,231 (minimum -757.855 MW), R 1,021; then R only at 1,312 / 924 / 678.
     - Rows with any measure negative: 8,542 / 1,312 / 1,011 / 678.
   - The chart paragraph now says each bar includes one negative residential value (`KIIN_P`, -0.085 to -0.133 MW).
   - No note-body line carried the wrong counts; the body has no negative-value counts.
3. **Nit, "summed".** The title begins "Summed peak demand", and the key label is "Summed peak demand". The caption
   says "gridflow's sum over every location and type".
4. **Nit, negative residential values on the page.** The caption, beside the bars that include them and dated by
   "NESO's file of 15 July 2024" in the same sentence, now ends: "one tiny negative residential value per bar
   included". Reproduced: exactly one negative `R` row per bar, `KIIN_P`, at every one of labels 25 to 50.
5. **Nit, blank peaks dated.** `record.fields.demand_pk` is now "MW at national winter peak; 114 direct connects
   blank in 2021 to 2023 files". The 17:00 to 18:00 window was dropped for budget; the AM and PM lines keep theirs.
6. **Nit, all eight type codes.** One guide line cannot hold eight decodes in 14 words (the budget counts tokens
   split on whitespace). The split:
   - `record.fields.type`: "`C` commercial, `E` EVs, `I` industrial, `R` residential, `H` heat pumps, `D` district
     heat".
   - `record.caption`: "GSP `ABHA1`'s seven types and direct connect `B_EXTRA_35` (`T`); `Z` is electrolysers; 2024
     `HT`, label 50" (16 words).
   - All eight are decoded beside the frame they label. The lead's raw-feed line still names all eight in NESO's order.
7. **Nit, year-label body wording.** "Six things to know" item 2 now adds "the site chart shows NESO's own
   financial-year reading (`25` = 2025/26, the demand dictionary)". "The year label" paragraph adds that the chart
   labels bars with NESO's own financial-year reading, not a converted year.
8. **Nit, history line.** `facts.history` is now "The package was created on 6 July 2021".

## Unchanged

Chart spec, `record.select`, notebook cells, related links, member lines and held lines. The checker found these sound.
