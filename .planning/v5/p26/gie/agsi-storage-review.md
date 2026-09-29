# agsi-storage: checker review

Family page `agsi-storage` (lead `storage`, member `storage_reports`). Checker: Opus 5.5, 2026-09-29.
Inputs: the canonical notes in `vault-p26-gie` diffed against `origin/master`, the mirror (`cmp` clean for both notes), the three artefacts, the built page, the writer's report, gridflow code, local silver (read only), and the bronze meta.

## Verdict: REVISE

One major (the notebook breaks at 390). The facts, the chart, the frame and the units all hold against code and silver. The rest are nits.

## What was checked and holds

- **Units (the brief's first question).** I reproduced the ratio. For consecutive gas days, (injection - withdrawal) / (day-on-day change in `gas_in_storage_gwh`) has a median of 989 to 1,001 for every entity, the EU included (DE 13 to 14 Sep: 0.2822 against 282.14).
  - I also settled which side is mislabelled, with a cross-check inside the repo. Italy's AGSI net injection matches local ENTSOG `physical_flows` (exits minus entries at `UGS - IT - Snam Rete Gas/STOGIT`, `.../Stogit Adriatica` and `Italgasstorage (IT)`) within about 4% on all 14 overlapping gas days (13 Sep: 522.04 against 525.19; 20 Sep: 489.18 against 481.14).
  - ENTSOG's `flow_gwh_per_day` is converted from the vendor-sent unit through an explicit factor table, and unknown units are dropped (`silver/entsog/physical_flows.py:27-68,197-250`).
  - So the AGSI flows are GWh per gas day, and the stock-scale columns are TWh. Every unit the page states is supported. The page states no stock unit, and the vault body's "not GWh" is now backed.
- **Coverage and levels.**
  - `storage`: 9 countries x 15 gas days, all `entity_level = country`. GB is null in every numeric column except `consumption_full_pct = 0.0`, with status `N`.
  - `storage_reports`: 15 rows, `aggregate_type` / `eu` / `EU`, `country_code = ""`, `country_name` null.
  - The EU is not the sum of the countries: WGV 1,131.5658 against 899.4094; gas in storage on 22 Sep 794.8308 against 632.8453.
  - No text or chart sums across levels. The chart filters five country codes, and `last` over one row per country and gas day is a pass-through.
- **Chart.** The committed series equals silver exactly for DE, IT, NL, FR and AT over 13 to 22 Sep, and the alt values are right (IT 84.66 to 86.03, FR 76.74 to 81.09, AT 67.1 to 67.87 on the 21st then 67.81, DE 55.81 to 56.99, NL 52.55 to 56.26). "No two lines cross" is true.
  - The five largest by working gas volume on 22 Sep: DE 247.494, IT 203.4249, NL 144.0428, FR 123.8779, AT 100.2789.
  - The series has `spec_origin: vault`, there is no staged spec under `chart-specs/gie`, and the build's digest check passes.
- **Gas day and time stamps.**
  - `gas_day` is the vendor's `gasDayStart` (`agsi.py:158`), and `event_time` is gas_day at 06:00 UTC (`silver/base.py:383-400`; silver shows `2026-09-22 06:00 UTC`).
  - `gas_day_end` minus `gas_day` is exactly 1 day at 00:00 UTC on every row (`agsi.py:56-57,193`).
  - `updated_at` comes from a zoneless bronze stamp (`"updatedAt":"2026-09-25 18:11:53"`) that is read as UTC (`agsi.py:59-62`).
  - Nothing is called a publish or issue time.
  - The cadence uses the seat's wording ("as sent in the responses we hold").
- **Requests and commands.** The bronze meta `request_url` values are `...api?country=AT&date=2026-09-22&page=1&size=300` and `...api?type=EU&date=2026-09-22&page=1&size=300`.
  - The CLI signature is `ingest <source> <dataset> --start --end` (`cli.py:186-190`).
  - The ingest end is fetched: `resolve_dates` makes a bare date midnight UTC, and `gas_day_range` is inclusive on `.date()` (`endpoints.py:182-193`).
  - Bronze is filed by gas day (`data_date`), with no offsets.
  - The runner passes no scope (`runner.py:947`), so `storage_reports` is EU only (`client.py:177-194`).
- **Frame and guide.** The eight rows are real (`generated_by: gridflow-sample`, 22 Sep, BE left out) and every value matches silver.
  - `storage_pct_full` equals stock / WGV x 100 rounded to 2 dp on every row (0 mismatches).
  - Net withdrawal is within 0.09 of withdrawal minus injection.
  - `consumption_full_pct` matches stock / consumption to 0.005.
  - Contracted + available divided by WGV is 1.000 for AT, ES, FR, IT, NL and PL, 1.027 for DE and 0.96 for BE.
  - `covered_capacity` is 100 on all 120 non-GB rows, and `trend` equals the daily change in pct to within 0.01.
  - `info` is `"[]"` on every row. Status on 22 Sep: NL `E`, GB `N`, the rest `C`.
  - The key matches the dedup key (`agsi.py:233-241`).
- **Notebook.** The notebook is JSON from `run_notebooks.py`, read-only, with no errors. The lead matches `query()`: `BETWEEN ? AND ?` on DATE `gas_day` (`_get_method_registry.py:62-91`), bitemporal columns excluded (`source.py:441-449`), relation `silver_gie_agsi_storage` (`schema_manifest.py:230`).
  - `plot_alt` values match silver (FR min -759.2 on the 20th; DE -71.7 on the 15th, -711.1 on the 19th, -1.0 on the 22nd; NL -429.5; every DE, FR, IT and NL point is below 0).
- **Build and gates.** `gridflow-build --only gie/storage` wrote `agsi-storage.html`. The only warnings are the known ones for other datasets. `detect.mjs --json` returns `[]`.
- **Leakage and filler.** A grep of the rendered text for `locally|held|our |since 20|rows|% of|live|now|—|–|→|·` finds only allowed uses ("sample rows", "country rows", "these rows" and the help card).
- **Layout (real Chrome, measured).** At 1440, 1024, 768 and 390 the page has no horizontal scroll (`scrollWidth` at most the viewport).
  - The frame folds correctly (10, 6, 5 and 3 visible columns plus `…`) and scrolls inside `.fw` when unfolded.
  - No chart text overflows its SVG, except the `%` unit label at 390, which sits 2 px above the box with `overflow: visible` and is fully drawn.
  - The hero scenery, the chart, the raw feed and the related band are clean in the screenshots.
  - My headless Chrome shots did not apply the container-query fold, so every frame claim above rests on the browser measurements, not those shots.

## Findings

1. **major**, `page.notebook.cells[2]` (the plot cell; rendered cell `[5]`). At 390 the continuation line breaks one character per line.
   - **What is wrong.** The cell's second line starts with a 33-space hanging indent (`                                 color=["#155A6E", ...])`). Under `white-space: pre-wrap` in a 300 px code box, that leaves about 5 characters per line, and `color=[...]` prints as a vertical column of single characters.
   - **Evidence.** Measured in real Chrome with the notebook open: the `pre.in` is 300 px wide and **1,183 px tall** at 390 (about 57 lines at 20.8 px). At 768 it is 157 px, and at 1024 and 1440 it is 88 px. The headless 390 shot (`seg_390_u1_5.png`) shows the broken column. The writer's 390 check did not open the notebook.
   - **Fix.** This is author-fixable and needs no template change. Drop the hanging indent, for example `colors = ["#155A6E", "#66793B", "#3E8C97", "#C77E3C"]` on its own line, then `net[["DE", "FR", "IT", "NL"]].plot(ylabel=..., figsize=(8, 3.5), color=colors)`. Then rerun `run_notebooks.py` and rebuild.

2. **nit**, `page.what_it_is` (last sentence). The wording is correct but not plain.
   - **What is wrong.** "Gas in storage moves by net injection divided by 1,000, though both are named `_gwh`" has no clear referent for "both", because net injection is not a column (`injection_gwh` and `net_withdrawal_gwh` are). A recruiter has to work out that this means a unit mismatch.
   - **Evidence.** The ENTSOG cross-check above now puts the unit in evidence, so the page can name it as a project check. For example: "Stock columns (`gas_in_storage_gwh`, `working_gas_volume_gwh`) are TWh despite the name: checked against the GWh flows and ENTSOG; compare countries by `storage_pct_full`."
   - **Related.** The `gas_in_storage_gwh` and `working_gas_volume_gwh` guide lines can say "TWh by our check" in the same way. This also answers the writer's open question 1.

3. **nit**, vault bodies, `storage.md` and `storage_reports.md` (the `gas_in_storage_gwh` row and Known issues).
   - **What is wrong.** The body says "GIE's unit is unconfirmed here" and "GIE's own unit statement is not in our sources", while the `working_gas_volume_gwh` row asserts "not GWh" and the flows bullet asserts "GWh per gas day" with no cited evidence.
   - **Fix.** Cite the ENTSOG cross-check (IT storage points, 14 gas days, within about 4%; `silver/entsog/physical_flows.py:27-68`) where the flows are called GWh, and state the stocks as TWh by that check. That makes the rows consistent and evidenced.

4. **nit**, `page.chart_view.caption` ("GB sends no values") and `page.family.members[0].differs` ("GB's values are null").
   - **What is wrong.** GB is not empty. It sends `-` placeholders, which the transformer nulls, plus `"consumptionFull":"0"`, which lands as `consumption_full_pct = 0.0`, along with status `N` and `info` `[]`. In the rubric's terms, "sends no values" is close to "sends placeholders".
   - **Evidence.** A GB silver null count shows 0 nulls in `consumption_full_pct`, and the bronze body sends `"consumptionFull":"0"`.
   - **Suggested fix.** Caption: "GB sends placeholders, no storage values". Differs: "GB's storage values are null".

5. **nit**, `page.related[2]` (`gie/lng`).
   - **What is wrong.** "LNG terminal stocks and send-out, from GIE's ALSI" says what the dataset is, not how it relates (rubric 6).
   - **Suggested fix.** For example: "LNG send-out feeds the same national gas balances as storage".

6. **nit**, `page.related[0]` (`gie/unavailability`). The seat should know this link points at a page held blank (ruling 43). There is precedent: the shipped `system_prices` and `disbsad` link to the held `netbsad`. Keep it or swap it, as the seat prefers.

7. **nit**, `page.notebook.cells[2]` (the plot colours and legend). This is the clash the writer repainted out of the chart.
   - **What is wrong.** DE (`#155A6E`) and IT (`#3E8C97`) are two teals, and in the notebook plot they cross on 14, 17 and 21 Sep. The default legend (upper right) also sits over DE's final rise to -1.0 on the 22nd.
   - **Evidence.** `storage-5.png`.
   - **Fix.** This can be done in the same rewrite as finding 1: give IT or DE a non-teal colour, and add `legend(loc="lower left")` or similar.

8. **nit, optional**, `page.record.fields.gas_day`. "gridflow labels its `event_time` 06:00 UTC" is true, but a reader may take 06:00 UTC as the gas day's start. The vault's gas-day concept page puts the EU gas day at 06:00 CET/CEST. The vault body already says it is "a project convention, not the vendor's start instant". The guide line could add "a project label, not the start" if the word budget allows.

## Defects (for the seat to log; they confirm and extend the writer's)

- **gie_agsi storage / storage_reports: stock columns are TWh, not GWh (confirmed).** The writer's 1,000x finding is now anchored to an external unit.
  - AGSI IT net injection (`injection_gwh - withdrawal_gwh`) matches ENTSOG `physical_flows` exits minus entries at the Italian UGS points (GWh/d, converted from the vendor unit) within about 4% on 14 gas days (2026-08-01 to 05 and 09-13 to 21).
  - So `injection_gwh`, `withdrawal_gwh` and `net_withdrawal_gwh` are GWh per gas day, and `gas_in_storage_gwh`, `working_gas_volume_gwh`, `consumption_gwh`, `contracted_capacity_gwh_per_day` and `available_capacity_gwh_per_day` are TWh.
  - The vault GIE README ("stocks and flows are GWh") is wrong. The rename or rescale needs a DATASET_VERSION major bump, and `gold_eu_gas_storage` carries the same names.
- The rest as in the writer's report: `storage_reports` is EU only from the CLI, `schema_cls = None`, the `gas_day_end` 00:00 UTC label, and `updated_at` read as UTC.
