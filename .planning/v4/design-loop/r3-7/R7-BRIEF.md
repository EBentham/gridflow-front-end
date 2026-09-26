# Round 7 brief: three layouts of the merit-order-stack purpose section (read fully)

Read `<scratch>\r3\SHARED.md` first (design system, honesty rules, do-not-use list, .dc.html rules,
verification recipe). This file overrides it where they differ.

## Where we are
Bobbo picked the page `<scratch>\r3\r3-6\R3-v4-P1.dc.html` (1440 x 5919). EVERYTHING on it is locked except the
purpose section: "A personal research platform for UK and European power markets" (h2 at y 1414; its
drawing block `p1-draw` runs y 1584 to about 2318; the next section starts at y 2515). He likes P1's idea,
the merit-order supply stack as the centrepiece, but called its LAYOUT "a bit mid". Your job: one new
layout of that section, per your own brief (in your prompt). The other two designers get different briefs.

## How to build it
- Copy `<scratch>\r3\r3-6\gen.py` and `demand_fan.json` into your own folder and work there. `page(purpose)`
  (gen.py ~line 1196) renders the whole page around a purpose-section string; `p1()` (~line 1450) and
  `stack_draw()` (~line 1397) are the current version. Write your own function and emit
  `<your-folder>\R3-v5-<letter>.dc.html`.
- Outside the purpose section the output must be byte-identical to R3-v4-P1 apart from CSS you add and
  anything in the shared background SVG that sits inside the section band. Prove it with a diff and report it.
- Keep the page at 5919 high if you can. If the section truly needs more room, shift everything below it
  down uniformly (the strata, cables and every later block), and report the new height.

## Content (keep; you may re-word only as noted)
- The h2 (verbatim) and the two approved-pending lines: "The warehouse exists to support quantitative work.
  The pipeline and the catalogue are the means; the models are the point." and "The aim is a price
  forecast: the input that trading research starts from."
- The five models, each with its id in Red Hat Mono: day-ahead demand `day_ahead.lgbm_demand.v1`, wind
  generation `wind.lgbm_quantile.v1`, solar generation `solar.lgbm_quantile.v1`, merit-order supply curve
  `stack.gb.v1` (`GBStackModel.build(as_of)` returns a `SupplyCurve`, GB plant in merit order, cheapest
  first), fundamentals SMP forecaster `fundamentals_smp.gb.v1` (Monte Carlo draws of residual demand, each
  cleared against the curve, build a price distribution; backtested against ENTSO-E day-ahead prices).
  Residual demand = demand less wind and solar. One "See the case study" link (demand model).
- The logic the drawing must make legible: demand, wind and solar forecasts combine into residual demand;
  residual demand crosses the stack; where it crosses sets the price; repeated draws give a distribution.
- Tranche order (from stack.gb.v1): biomass, nuclear, CCGT, coal, OCGT; pumped storage and
  interconnectors are netted out of demand, not stacked. Tranche colours follow the scenery palette in
  SHARED.md (CCGT = clay, nuclear = petrol, other/biomass as P1 chose).

## Honesty (hard)
- Stack widths, heights and costs are DRAWN, not data. No numeric scales, no £/MWh or MW numbers on the
  stack, no invented prices. Axis words ("price", "capacity") are fine.
- The only real model output available is the demand fan in `demand_fan.json` (gold forecast run
  a55a829bc51c40b2, fold 12, issued noon the day before, 1-5 Aug 2026, quantiles 0.05-0.95 plus `actual`
  = Elexon INDO). Use it only if your brief calls for it, with dataset, unit and window stated.
- Bobbo dislikes filler lines. Do NOT add a caption like "An illustration, drawn without scales"; the
  absence of numbers carries that. If you think a disclosure is needed, say so in your report instead.
- No planned / shipped / trained / status words, no F-codes, no node-and-arrow flowchart (he rejected it).

## Report (under 200 words)
File path, page height, the layout idea in one line, diff proof, detector result (`[]` required), how you
checked layout (numeric rect checks at 1440 wide; stop any server you start), every NEW COPY line verbatim.
