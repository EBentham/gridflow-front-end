# Resource adequacy in the 2030s: checker's review

Page `resource-adequacy-in-2030s`, lead `resource_adequacy_2030s_results`, members `_peak_demand` and `_portfolio`.

## Verdict: REVISE

0 blockers, 2 majors, 6 nits. The chart, the dated captions, the NESO definitions, the captures and the anomaly wording
are sound. The two majors are one missing ingest command and one related note that overreaches.

## Findings

1. **Major.** `page.raw_feed.commands` (and the notebook `needs`). The notebook says it needs "NESO's three Resource
   Adequacy in the 2030s files ingested", and cell 6 reads `silver_..._portfolio_latest`. The three commands cover the
   results table (ingest, transform) and the peak demand file (pipeline) only. A reader who runs them has no portfolio
   table and cell 6 fails. Fix: add `gridflow pipeline neso_data_portal resource_adequacy_2030s_portfolio --last 24h`
   (comment of 6 words or fewer, for example "the portfolio file, both steps").
   Evidence: built page "The raw feed" lists three commands; `needs` names three files; cell 6 queries the portfolio view.

2. **Major.** `page.related[1]` (ES1): "FES electricity supply by scenario, NESO's other long-run fleet projection".
   Two overreaches. (a) The ES1 note says it does not establish whether any year column is outturn or projection and
   tells readers not to use the values as either (`future-energy-scenario-electricity-supply-data-table-es1.md`, first
   paragraph). (b) NESO calls the study's cases "portfolios" and "sensitivities"; nothing in NESO's text calls them a
   projection of the fleet. Fix, 12 words or fewer, for example "FES electricity supply by scenario, another NESO
   long-run study".

3. **Nit.** `page.related[0]` (Capacity Market register): "Capacity bought per delivery year, beside these modelled
   2030s portfolios". NESO's register says capacity awarded in auctions (`capacity_market_auction_cost.capacity_awarded`),
   not "bought", and the register's delivery years run 2016/2017 to 2031/2032, so only 2030/31 and 2031/32 touch the
   study. "Beside" invites comparing awarded capacity with the portfolios' installed MW. Suggest "Capacity awarded per
   delivery year; these portfolios give installed MW".

4. **Nit.** `page.related[2]` (interconnector register): "Interconnector projects; three sensitivities cut imports or
   remove new interconnection". The count is right (Sensitivity 08 removes new interconnection, 09 cuts import
   availability by 10%, 10 has no imports; from `simulation_name`). But NESO does not tie the study's interconnection
   assumptions to the register's contracted projects, and the note reads as if it does. Suggest "Contracted interconnector
   projects; Sensitivities 08 to 10 here vary interconnection and imports".

5. **Nit.** `page.related[3]` (historic demand): "Outturn demand history, against the modelled peak demands here". NESO
   does not say which demand the peak demand file measures (national demand, transmission system demand, with or without
   embedded generation), so "against" implies a like-for-like comparison NESO has not stated. Suggest "Outturn demand in
   MW; the demand basis of the modelled peaks is not stated".

6. **Nit.** `page.record.fields.weather_conditional_eeu_mwh_year` and `...lole_h_year`.
   NESO's EEU text is "the average volume of demand exceeds supply across all simulations ... The simulations cover 100
   randomly selected forced outage patterns". The guide prints "NESO: average volume by which demand exceeds supply,
   same 100 patterns": "by which" is the writer's repair of a garbled sentence, yet it is introduced by "NESO:" so it
   reads as NESO's wording. The LOLE line, "NESO's average over 100 random forced-outage patterns", also turns "across all
   simulations that cover 100 patterns" into "average over 100 patterns". Both are close to NESO and not wrong, but
   the brief says nothing beyond NESO's text. Suggest dropping "NESO:" from the EEU line or quoting NESO's words, and
   saying "across simulations covering 100 randomly selected forced-outage patterns" in the LOLE line.

7. **Nit.** `page.chart_view.title` and `caption`. Modelled status is in the hero, "What it is" and the caption, but the
   title ("Portfolio 1 loss of load by weather year, 2035/36") could be read as outturn, and the caption's "Modelled;"
   sits mid-line. The page also never says what Portfolio 1 is; NESO's resource description says the sensitivities are
   deviations from Portfolio 1, which is the reason to chart it. Suggest "Portfolio 1 modelled loss of load by weather
   year, 2035/36" and a clause in `what_it_is` that NESO's sensitivities are deviations from Portfolio 1.

8. **Nit (template).** Bar labels print one decimal: the chart shows 1.5 and 6.2, while the alt, the frame and silver say
   1.52 and 6.23. Already noted by the writer; seat item.

## Chart (items 1 and 2)

- Reproduced from silver with Polars: Portfolio 1, 2035/36: 34 rows, one per weather year 1984/85 to 2017/18; non-zero
  values are 1984/85 1.52, 1985/86 6.23, 2000/01 0.1; the other 31 are 0. Committed series is identical
  (`rows_read 1462, rows_matched 34, rows_used 34, duplicates_dropped 0`, `spec_origin: vault`). Alt text, key note and
  caption match. The bars are single rows, nothing summed.
- Dating and framing: caption and `published_at` give 12 December 2025 (CKAN `last_modified` 2025-12-12T12:34:52.812310
  for the results file); "Modelled" is stated; unit is NESO's `hours/year`; the key note quotes NESO's dictionary
  correctly (truncated at "all simulations", which the caption completes).
- Size: 1,200 px tall at 1440 (about 85% of the width empty, 31 zero labels), 358 by 1,211 px at 390. It is legible at
  both widths, no label clips, no overlap. **Recommendation: keep the 34-bar chart.** The page's finding is that loss of
  load sits in three weather years and the zeros are real values, which only the weather-year view shows. The
  alternative (one weather year across cases) needs a weather year chosen after the fact (1985/86, the only year with LOLE
  above zero in all 17 cases of 2035/36, running from 0.9 to 49.84 hours/year), 17 long sensitivity names via
  `group_map`, and would overstate typical results. If the seat wants it later, it should be a second chart, not a swap.

## Definitions (item 3)

Against NESO's dictionary (`field-info/20261008T114228Z/resource_adequacy_2030s_results.json`): the key note quotes
LOLE's first clause verbatim; "Loss of Load Expectation" and "Expected Energy Unserved" are NESO's expansions; units
hours/year and MWh/year are NESO's; the 1 April to 31 March span is NESO's spotlight-year comment; "used to generate
supply and demand" follows NESO ("suppy" typo not copied); "sensitivity capacities excluded" follows NESO's resource
description. No reliability standard or weighting is mentioned. See finding 6 for the two small paraphrase points.

## Anomaly (item 5)

Reproduced: every EEU value is a multiple of 10 (min non-zero 10.0); every LOLE is a whole hundredth; two rows have LOLE
above zero and EEU 0 (Sensitivity 08, 2040/41, 1996/97, 0.02; Sensitivity 09, 2035/36, 2012/13, 0.01); no row has EEU
above zero with LOLE 0; zero counts 1,195 (LOLE) and 1,197 (EEU) match the note. The page does not mention any of this.
The note body words it as an observation scoped to the capture, says it "fits" rounding, says NESO states no rounding and
carries `TODO: verify`. Nothing is presented as NESO's rule. Good.

## The rest (item 6)

- Facts verified: cadence "Once in 2 years" (catalogue extras), package created 2025-12-11T13:04:12, files last modified
  11 and 12 December 2025, six portfolios, twelve sensitivities, three spotlight years, 34 weather years, 1,462 / 102 /
  315 rows, frame shape (8, 14), `published_at` is the CKAN `last_modified`, and the "downloaded whole unless
  `last_modified` is unchanged" line (`client.py:1751-1767`). Request URLs match the catalogue resource URLs.
- Frame and guide: eight real rows, caption accurate, key columns first, guide covers every non-pipeline column, no line
  repeats the frame.
- Notebook: outputs match silver (Portfolio 1 counts 4, 3, 4; NaN for Portfolios 4 to 6 in 2030/31 because they have no
  rows; peak demand top six; capacity pivot). Plot alt matches (1984/85 3.97, 1.52, 0.36; 1985/86 4.98, 6.23, 5.63; every
  other value 0.1 or less). All cells read-only; lead sentence correctly explains `data.sql()`.
- Note-body correction: one addition, smallest span, evidence reproduced. Still unverified and left in the body: "the
  report is dated July 2025" (no source in the snapshots); not on the page.
- Mirror `cmp` identical. Build `--only neso_data_portal/resource_adequacy_2030s_results` succeeded. Detector `[]`.
- Leakage grep on the built page (locally, held, our, since 20, rows, % of, days, live, now, real-time, planned, em dash,
  middle dot, arrow): nothing in page copy ("rows" only in the template's table caption and help card).
- Screenshots: headless Chrome at 1440, 1024 and 768 (hero scenery, chart, wells, frame, guide, notebook, related all
  fully visible, no clipping). At 390 in the browser pane: `scrollWidth` 390, no element outside a clipping container, all
  69 chart texts inside the chart's 16 to 374 px. Dark mode not checked (writer reports the page keeps its light palette).
  My server (PID 59262, port 9953) was stopped by PID.

## Defects (pasteable)

- None in gridflow code. Vendor data note: LOLE above zero with EEU 0 in two rows, all EEU values multiples of 10 MWh
  (see above); a vendor presentation question.

## Round 2

**Verdict: APPROVE** (0 blockers, 0 majors, 1 new nit). Rebuilt `--only neso_data_portal/resource_adequacy_2030s_results`:
no errors. Detector `[]`. Mirror `cmp` identical (430 lines, 430 CRs). Checked against the rebuilt page text; layout
unchanged, so no new screenshots and no server was started.

1. Missing portfolio command: **fixed.** The page now has one `gridflow pipeline neso_data_portal <dataset> --last 24h`
   per table. Valid as written: `pipeline` takes `source`, an optional `dataset` and `--last`
   (`cli.py:484-493`); `resolve_datasets` returns the single named dataset (`pipeline/runner.py:513-544`); all three keys
   exist under `neso_data_portal` in `config/sources.yaml:1029-1031`. Ingest and transform run in one window, so the
   three commands produce the results, peak demand and portfolio silver tables that cells 2 to 6 read through their
   `_latest` views, matching `needs`.
2. ES1 related note: **fixed.** "FES electricity supply by scenario or pathway, a separate NESO study" makes no
   projection or fleet claim, and "scenario or pathway" is the ES1 note's own wording.
3. Capacity Market: **fixed** ("Capacity awarded per delivery year; these portfolios give installed MW").
4. Interconnector: **fixed** ("Contracted interconnectors; Sensitivities 08 to 10 here vary interconnection and
   imports"); 08, 09 and 10 are the three that change interconnection or imports.
5. Historic demand: **fixed** ("Half-hourly outturn demand; NESO does not state the modelled peaks' demand basis").
6. Column guide: **fixed.** EEU now quotes NESO verbatim ("average volume of demand exceeds supply across all
   simulations", a substring of NESO's dictionary text); LOLE reads "averaged across simulations covering 100 randomly
   selected forced-outage patterns", which follows NESO's two sentences. "by which" and the unquoted "NESO:" repair are
   gone.
7. Title and Portfolio 1: **fixed.** Title says "modelled"; the caption has "NESO's modelled weather-conditional LOLE";
   `what_it_is` states the sensitivities deviate from Portfolio 1, which NESO's portfolio resource description says.
8. Bar labels at one decimal: template item for the seat, unchanged.

New nit (not blocking): `page.what_it_is` ends "six portfolios and twelve sensitivities, whose capacities deviate from
Portfolio 1 (NESO)". "Whose" can be read as covering the six portfolios too, and Portfolios 2 to 6 are not deviations.
NESO says only that the sensitivity capacities are deviations. Suggest "twelve sensitivities (NESO: their capacities
deviate from Portfolio 1)".
