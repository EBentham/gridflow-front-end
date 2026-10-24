# Resource Adequacy in the 2030s: writer's round 2

These fixes answer the checker's review (`resource-adequacy-in-2030s-review.md`, REVISE: 2 majors, 6 nits) and the
seat's rulings.

The rebuild with `--only neso_data_portal/resource_adequacy_2030s_results` passes. The first attempt failed on
`what_it_is` at 62 of 60 words, which is fixed. The detector returns `[]` and the page has 0 em dashes. The canonical
note keeps CRLF (430 lines, 430 CRs). I copied it to the mirror and `cmp` reports it identical. The chart spec, sample
rows and notebook cells are unchanged, so the series, sample and notebook artefacts stand as committed. The build's
digest check passed.

## Fixes

1. **Major, raw-feed commands (ruling 1).** gridflow's CLI has no package-level ingest. `ingest`, `transform` and
   `pipeline` each take one optional `dataset` argument or `--all`, and `--all` runs every dataset for the whole
   `neso_data_portal` source, not this package (`gridflow/src/gridflow/cli.py:186-193`, `261-268`, `485-493`).
   The template allows three commands, so I replaced the old ingest, transform and pipeline lines with one
   `gridflow pipeline ... --last 24h` per table:
   - `resource_adequacy_2030s_results`, commented "results file; window must end recently";
   - `resource_adequacy_2030s_peak_demand`, commented "the peak demand file, both steps";
   - `resource_adequacy_2030s_portfolio`, commented "the portfolio file, both steps".

   The notebook's `needs` ("NESO's three Resource Adequacy in the 2030s files") now matches the commands, and cell 6's
   portfolio view is covered. `pipeline` resolves one window for both stages (`cli.py:485-560`), which is the form
   the approved tRESP page uses.
2. **Major, ES1 related note (ruling 2).** The note now reads "FES electricity supply by scenario or pathway, a
   separate NESO study". It makes no claim about outturn or projection, and it does not call this study's portfolios a
   fleet projection. The ES1 note's own opening says its rows are "GB FES values for electricity Supply" by scenario
   or pathway.
3. **Nit, Capacity Market note.** Now "Capacity awarded per delivery year; these portfolios give installed MW".
4. **Nit, interconnector note.** Now "Contracted interconnectors; Sensitivities 08 to 10 here vary interconnection
   and imports". The register page describes interconnectors holding NESO connection contracts.
5. **Nit, historic demand note.** Now "Half-hourly outturn demand; NESO does not state the modelled peaks' demand
   basis".
6. **Nit, column guide paraphrases.** Both lines now follow NESO's dictionary:
   - LOLE: "Hours/year demand exceeds supply, averaged across simulations covering 100 randomly selected
     forced-outage patterns".
   - EEU: `MWh/year; NESO: "average volume of demand exceeds supply across all simulations"; same 100 patterns`.
     NESO's words are quoted verbatim, with no repair.
7. **Nit, chart title and Portfolio 1.**
   - Title: "Portfolio 1 modelled loss of load by weather year, 2035/36".
   - Caption: "Modelled;" moved into the sentence ("NESO's modelled weather-conditional LOLE").
   - `what_it_is`: now ends "...twelve sensitivities, whose capacities deviate from Portfolio 1 (NESO). Modelled, not
     history." This is NESO's portfolio resource description ("Capacities used for uncertainty and sensitivity
     analysis ... are deviations from Portfolio 1"). The spotlight-year span is now in brackets to stay within budget.
8. **Nit, bar labels at one decimal.** A template item for the seat; no change on my side.

The 34-bar chart is kept (ruling 3).

## Checks

The rendered page contains each new string once (spot grep). It no longer contains "long-run", "fleet projection"
or "by which". Screenshots were not retaken: only text inside existing wells and lines changed, and the chart drawing
did not change.

## Defects

None new. The vendor data note from round 1 stands: two results rows have LOLE above zero with EEU 0, and every EEU
value is a multiple of 10 MWh.
