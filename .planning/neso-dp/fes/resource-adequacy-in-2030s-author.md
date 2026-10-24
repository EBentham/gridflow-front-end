# Resource Adequacy in the 2030s: writer's report

Page `resource-adequacy-in-2030s`, lead `resource_adequacy_2030s_results`, members `_peak_demand` and `_portfolio`,
all eligible (ledger row: SCN-3, "all 3", nothing held). Built with
`gridflow-build --only neso_data_portal/resource_adequacy_2030s_results`: no errors. Detector `[]`. No em dashes.
Banned-word grep (`locally`, `held`, `our `, `since 20`, `real-time`, `coming soon`) finds nothing in the page.

Files (mine only):
- canonical note `C:\gridflow-wt\vault-neso-fes\30-vendors\neso-data-portal\datasets\resource-adequacy-in-2030s.md`
  (CRLF kept: 430 lines, 430 CRs; diff +144 / -1);
- mirror `C:\gridflow-wt\fe-neso-fes\vault\neso_data_portal\resource-adequacy-in-2030s.md` (`cp` then `cmp`: identical);
- `site/hifi/data/{series,samples}/neso_data_portal/resource_adequacy_2030s_results.json`,
  `site/hifi/data/notebooks/neso_data_portal/resource_adequacy_2030s_results.json` and `-4.png`;
- built page `site/hifi/data-sources/neso_data_portal/resource-adequacy-in-2030s.html`.
No staged chart spec or authored override existed.

## The chart and how I reproduced it

Bar chart, `Portfolio 1`, spotlight year `2035/36`, `weather_conditional_lole_h_year` in hours/year (NESO's dictionary
unit), one bar per historical weather year, sorted by label. Each bar is exactly one silver row (filter on case and
spotlight year, dedup on the entity key, `aggregation: max` over a single row), so nothing is summed or averaged
across weather years. Distil: 1,462 rows read, 34 matched, 34 used, 0 duplicates dropped.

Reproduced with Polars on silver (`pivot(on=spotlight_year, index=historical_weather_year)` for Portfolio 1): 2035/36
is 1.52 (1984/85), 6.23 (1985/86), 0.1 (2000/01) and 0 for the other 31 weather years. The committed series holds the
same three non-zero values; the alt text quotes them. The bar labels print one decimal (1.5, 6.2), the renderer's
formatting.

Why this reading: the results are weather-conditional, and NESO does not say how it weights weather years into a
headline LOLE, so any per-case summary would be our method, not NESO's. One case across every weather year shows the
structure honestly. Caption names the case, the spotlight year with NESO's 1 April to 31 March span, the unit, "one row
per historical weather year, nothing summed", "Modelled" and NESO's file date (last modified 12 December 2025).

The key note quotes NESO's dictionary verbatim for LOLE ("the average number of hours demand exceeds supply across
all simulations"). The column guide adds only NESO's other statement, that the simulations cover 100 randomly selected
forced-outage patterns. EEU's line paraphrases NESO's "average volume of demand exceeds supply" as "average volume by
which demand exceeds supply" (NESO's sentence is ungrammatical). No metric is defined beyond NESO's text, and I nowhere
mention the reliability standard.

Lead choice: the results table is the right lead. `_peak_demand` would chart 34 similar MW bars with no adequacy
reading. `_portfolio` would give a good 15-bar capacity chart, but it is an input, and its column guide would lose
LOLE and EEU. One caution for the seat: the 34-bar chart is the tallest bar chart on the site (the previous largest is
26) and has much empty space to the right at 1440. If that reads badly, the alternative is the same chart for one
weather year across the cases, which needs a `group_map` of 17 long sensitivity names.

## Captures

One bronze capture per table, all on 2026-10-08, and one silver file each:
- results: `raw_20261008T111713Z_71221dca-..._ef3f6cb7.csv`, 1,463 lines (header + 1,462 rows), silver 1,462;
- peak demand: `raw_20261008T111705Z_5ca210f2-..._3e5a1793.csv`, 103 lines, silver 102;
- portfolio: `raw_20261008T111708Z_c2bba528-..._d2ffb943.csv`, 316 lines, silver 315.

No recaptures, so no captures repeat rows. `dedup:` is set on the chart and the frame as a guard only, on the
results entity key (`resource_id, simulation_name, spotlight_year, historical_weather_year`) ordered by
`capture_written_at`. The key is unique across all 1,462 rows (Polars `struct(...).is_unique().all()` is true).
`published_at` is the CKAN `last_modified` of each file (`2025-12-12T12:34:52.812310` for results), read as UTC
(`silver/neso_data_portal/_bronze.py:130`). `timestamp_utc`, `event_time` and `capture_written_at` are the capture time.

## What one row is

- `resource_adequacy_2030s_results`: one case (`Portfolio 1` to `6`, or `Sensitivity 01` to `12`), one spotlight
  year, one historical weather year, with weather-conditional LOLE (hours/year) and EEU (MWh/year). The grid is ragged:
  Portfolios 4 to 6 and seven sensitivities have no 2030/31 rows, and Sensitivity 03 has only 2040/41.
- `resource_adequacy_2030s_peak_demand`: one spotlight year by one historical weather year, peak demand in MW
  (3 by 34 = 102), edition 2025.
- `resource_adequacy_2030s_portfolio`: one portfolio name (`Portfolio 1` to `6` and `Starting point`), one
  technology (15) and one `future_year`, with installed MW and stored MWh (7 by 15 by 3 = 315), edition 2025.

## Evidence table

| Claim (page) | Evidence |
|---|---|
| Spotlight year runs 1 April to 31 March | NESO field dictionary comment, all three tables (`gridflow/.planning/research/neso-snapshots/field-info/20261008T114228Z/*.json`) |
| LOLE and EEU definitions, 100 forced-outage patterns, units hours/year and MWh/year | results field dictionary, same snapshot |
| Historical weather year "used to generate supply and demand" | results dictionary ("suppy" sic) |
| Weather years 1984/85 to 2017/18; six portfolios, twelve sensitivities | silver labels; visible in the chart and notebook |
| Cadence "Once in 2 years" | catalogue snapshot `20261006T195819Z`, package extras |
| Files last modified 11 and 12 December 2025 | CKAN `last_modified` of the three resources (same snapshot); `published_at` in silver |
| NESO created the package on 11 December 2025 | package `metadata_created` 2025-12-11T13:04:12 |
| Portfolio file excludes sensitivity capacities | NESO resource description: "deviations from Portfolio 1 and are not included" |
| Peak demand for "NESO's 2025 study" | NESO resource description: "the 2025 resource adequacy study" |
| Request URLs | registry ids and package id; download names from the CKAN resource `url`; `package_show` in `client.py:971-990` |
| Download skipped when `last_modified` is unchanged | `client.py:1751-1767` |
| `query()` filters on capture time, so `data.sql()` | batch "Checked facts" (remediation 20at); same lead as the approved tRESP pages |
| Notebook outputs | `run_notebooks.py`: 6 cells, no errors; outputs checked against Polars (Portfolio 1 counts 4/3/4 weather years with LOLE above zero; NaN for Portfolios 4 to 6 in 2030/31) |
| Sensitivity relations in the related note (08 removes new interconnection, 09 and 10 cut imports) | `simulation_name` labels |

## Body corrections

One addition in the results "Content" paragraph after "Do not read a zero as missing": every EEU value is a whole
multiple of 10 MWh and every LOLE value a whole hundredth of an hour. Two rows carry a LOLE above zero with an EEU
of 0 (`Sensitivity 08`, 2040/41, 1996/97, 0.02 h; `Sensitivity 09`, 2035/36, 2012/13, 0.01 h). That fits EEU
rounded to 10 MWh, and it is marked `TODO: verify` because NESO states no rounding. Evidence:
`(eeu % 10 == 0).all()` is true and the minimum non-zero EEU is 10.0. The existing counts (1,195 zero LOLE cells,
1,197 zero EEU cells, 29 and 257 zeros in the portfolio file, trailing space in `Other LDES `) all reproduce. No other
body statement is contradicted by code or data.

## Unverified and open

- The body's "the report is dated July 2025" has no source in the snapshots I read. I left it in the body and kept it
  off the page.
- What `Starting point` is in the portfolio file (NESO does not define it). It is not shown on the page.
- Whether historical weather years follow the April to March convention. The page calls them "a label only" and
  never gives them a span.
- How NESO weights weather years for a headline LOLE or EEU. The page computes no per-case summary. Notebook cell 3
  counts the weather years with LOLE above zero, which is a count of rows, not a metric.

## Screenshots

Headless Chrome on port 9943 (PID recorded, stopped by PID) at 1440, 1024 and 768: hero, scenery, chart, wells,
frame, guide, notebook and related all fully visible, nothing clipped. For 390, the brief's iframe method painted only
down to the chart caption (a capture problem: the iframe stopped painting). A direct 390 window lays out wider than
390. So I checked 390 in the browser pane at an emulated 390 by 844, numerically: `scrollWidth` is 390, no
non-SVG element overflows outside a clipping container, and every text in the narrow chart lies inside it (16 to 374
px). Only the hero scenery overflows, inside its clipped SVG, as on every page. At 390 the frame folds after
`spotlight_year`, as the template does. Dark: under `prefers-color-scheme: dark` the page keeps its light palette
(body background unchanged), so the dark view matches the light one. Screenshots are in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\ra-writer\`.

## Template problems

- The 390 iframe screenshot method stops painting partway down this page (tall page with a 1,200 px narrow chart).
  Checkers may hit the same thing.
- Bar value labels round to one decimal, so a 0.01 h bar would print "0". Not visible here, where every non-zero
  value is at least 0.1.

## What the checker should look at hardest

1. The metric wording: the key note, both column-guide lines for LOLE and EEU, and `what_it_is` against NESO's
   dictionary text. Nothing may go beyond NESO.
2. The chart is one case and one spotlight year, with nothing aggregated. Confirm the caption and alt against the
   committed series: 34 bars, three above zero.
3. The `related` notes, especially the interconnector register ("three sensitivities cut imports or remove new
   interconnection") and the Capacity Market line ("Capacity bought per delivery year"), for overclaim.
4. The notebook's cell 3 output and plot alt against the run (counts per portfolio and spotlight year; the plot's
   1984/85 and 1985/86 values).
5. The body addition on EEU rounding (scoped to the 2026-10-08 capture, marked TODO).

## Defects

- None in gridflow code found for this package.
- Data note (NESO file, for the vault remediation page if wanted): in `resource_adequacy_2030s_results`, two rows have
  LOLE above zero with EEU 0 (`Sensitivity 08` 2040/41 1996/97 0.02 h; `Sensitivity 09` 2035/36 2012/13 0.01 h).
  All EEU values are multiples of 10 MWh, which suggests rounding NESO does not document. This is a vendor
  presentation question, not a gridflow defect.
- NESO dictionary typo: "suppy" in the results `Historical weather year` description (vendor text; quoted nowhere on
  the page).
