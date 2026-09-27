# gridflow design: "Above ground, below ground"

Locked 2026-09-26 by Bobbo after the v4 design loop (seven rounds; log in `.planning/v4/round-1-briefs.md`).
The reference page is the homepage board `R3-final` on the design canvas
(https://claude.ai/artifact/K1sUKPqgomVPcDsarVvXkv, private). Its source and generator are backed up in
`.planning/v4/design-loop/`. Tokens: `site/hifi/assets/tokens.css`. This file and the tokens change together.

## What it is

A documentation site for gridflow (ETL for UK and European power, gas, weather and carbon data) and
gridflow-models (probabilistic forecasting). It is aimed at recruiters and practitioners in energy
trading. It should read as real documentation made by someone who knows the domain: modern, technical,
clean and drawn with care. It must never look like a SaaS product or a dashboard.

## The idea

Each page is a **geological section**. Above ground, under a petrol sky, stands the physical grid of the
energy transition, drawn: wind turbines, solar, batteries, a data centre, an interconnector and pylons.
Below ground are gridflow's data layers, as strata. Cables run from the assets gridflow has feeds for,
down to the vendor that publishes that data.

| Stratum | Ground | Texture | Holds |
|---|---|---|---|
| Sky | petrol | none | masthead, hero, landscape |
| Topsoil | `--topsoil` | khaki speckle | the GB fuel mix, the research-platform section |
| Bronze | `--bronze-tint` | brick hatch in `--clay-deep` | raw vendor feeds, the catalogue |
| Silver | `--silver-tint` | diagonal hatch in `--silver-deep` | cleaned, typed tables |
| Gold | `--gold-tint` | stipple in `--gold-deep` | DuckDB views, the notebook workbench |
| Deep | petrol | granite marks in horizon | About, footer |

Strata meet on gently wavy contact lines, never on straight rules. Each layer's content sits inside its
own layer. Other pages keep the same descent: a page's subject decides which stratum it sits in, and a
page can use one stratum instead of all six.

## Colour

Use the tokens in `tokens.css`. The roles:

- **Petrol** is the sky and the deep. **Daylight** is the reading ground. **Ink** is text and every drawn line.
- **Chartreuse** is energy. Use it for the primary button, the focus ring, the active nav underline and
  energised land. It is never a text colour on daylight.
- **Olive** is for link underlines (`text-decoration-color`). It is never body text (4.37:1).
- **The scenery is the categorical palette:** wind = horizon, solar = chartreuse, gas = clay,
  nuclear = petrol, imports = olive, biomass = bronze, other = khaki. Every chart uses these; no other
  series colours.
- On petrol, text uses `--on-petrol` (7.0:1), `--on-petrol-2` (5.6:1) and `--on-petrol-3` (4.7:1).
  The canvas used #A9C7C4 (4.29:1); do not bring it back.
- Checked on daylight: `--ink-2` 8.5:1, `--muted` 5.2:1, petrol text 7.0:1. `--ink-2` on every stratum
  tint is at least 6.0:1.

## Type

- **Bricolage Grotesque** for display. Use its axes: wdth 80–92 and wght 650–800 for headings, with
  optical sizing on. **Hanken Grotesk** for body, with tabular numerals everywhere. **Red Hat Mono** only
  for code, dataset codes, table names, model ids and file names, never as decorative micro-labels.
- The scale is in `tokens.css`. The hero is 86 px, tight (line-height .94), condensed (wdth 84).
  Section heads are 42 px, and the two big set pieces (research platform, About) are 50–56 px.
- Labels on drawings are Hanken italic at 13.5–14 px, set lower-case like a hand-annotated plate
  ("residual demand", "less wind").
- Body measure is at most 58ch; captions at most 66ch.
- On phones, headings step down with `clamp()`: hero 44–86 px, section 30–42 px.

## Layout

- Desktop is designed at 1440 with 80 px side margins (1280 of content). Phones use a 16 px gutter with
  no horizontal scroll.
- Compositions are asymmetric: a left text column against a wide drawing, an index column keyed to a
  drawing, blocks staggered along the cables. Avoid centred stacks and equal card grids.
- The canvas positions blocks absolutely. The site must build the same composition with CSS grid and flow
  so it reflows. The strata become full-bleed section backgrounds whose contact lines are SVG edges.
- Default to no containers. Content sits on the ground. The only framed objects are real UI: the notebook
  window, help cards, DataFrames and input wells (border 1–1.5 px ink, radius 3–4 px, no shadows).

## Drawing language

- Flat ink line drawing: 1.5–1.6 px ink outlines with flat fills from the palette. Texture comes only
  from pattern hatches (speckle, brick, diagonal, stipple, granite) at low opacity. No gradients,
  glows, blur or shadows.
- Drawn objects are real infrastructure (turbines, panels, containers, a data-centre block, converter
  station, lattice pylons, catenary cables). There are no people, leaves, globes or hands.
- Drawings of the energy transition (data centres, batteries, EVs) are scenery and framing only.
  gridflow holds no such datasets, and no copy may imply that it does.
- **Motion:** one moment only, the turbine rotors turning slowly (13–21 s a revolution), stopped under
  `prefers-reduced-motion`.

## Charts

- Real data only. Every chart names its dataset, unit and window in the caption or the axis.
  Series come from `site/hifi/data/chart-series.json` or the silver/gold stores, never invented.
  Caveats that must stay true: chart-series values are per-timestamp means across rows, and
  `elexon/fuelhh` values are per-row means, never total output.
- **Schematic drawings** (the merit-order stack, the residual-demand draws) carry no numbers and no
  scales, and the missing numbers carry that honestly. Do not add "illustrative" captions.
- Captions describe what the line shows, never a cause nobody has verified.
- Chart chrome is minimal: ink axis, a few real ticks, no gridlines unless reading values needs them,
  no legends where direct labels fit.

## Components (as on the reference page)

- **Masthead:** the brand in Bricolage 800. Nav is 15 px `--on-petrol-2`; the current page has an inset
  2 px chartreuse underline and `aria-current="page"`.
- **Buttons:** primary is chartreuse with ink text, 12×20 padding and radius 3. Secondary is a text link
  with a chartreuse underline. Outlined links on petrol (About) have a 1.5 px `--on-petrol-2` border
  that goes solid on hover.
- **Links:** underline 1.5 px, offset 4 px, olive decoration on daylight. Focus is a 2 px chartreuse
  outline with offset 3.
- **Entries** (vendors, models, pillars): h3 23 px, one description line at 14.5 px `--ink-2`, one fact
  line at 600 weight. Never cards.
- **Table lists:** mono 16 px rows 44 px high with hairline rules.
- **Notebook** (workbench showcase): an ink tab bar, daylight body, `In [n]` prompts in `--muted`
  mono, topsoil input wells, help cards with an alternating definition list, DataFrames with right-aligned
  tabular cells and zebra rows, a completion popup in ink and daylight, and a matplotlib-style plot
  output. Everything shown must be real API surface from gridflow-models and real data.
- **Keyed index:** a narrow column whose entries carry a small mark copied from the drawing part they
  name, aligned level with that part.

## Dataset page anatomy (locked 2026-09-27)

One template for every dataset page. The page descends through the strata, top to bottom. Reference boards:
`.planning/v5/design-loop/` (round-1 A in the p24 canvas, `p24-r2-schema/4/`, `p24-r2-notebook/1/`);
decisions and their reasons: `.planning/v5/design-loop/p24-decisions.md`.

1. **Petrol hero:** dataset name, a one-line description, then the quick facts beneath it (vendor, cadence,
   grain, key, history only where the vendor's API evidences it).
2. **Topsoil: what it is and how it is used,** short prose, then the chart with its key beside it. Signed
   series (interconnectors, pumped storage) stack above zero when positive and hang below when negative;
   codes the palette doesn't cover are drawn unpainted with distinct ink hatches; khaki means only the vendor
   code OTHER. A caveat that matters for reading the chart goes in its caption.
3. **Bronze: the raw feed,** the vendor's raw URL and the gridflow CLI call that ingests it.
4. **Silver: schema and sample rows, "one record, then many":** one real row laid out field by field (name,
   value, dtype, meaning; key columns marked; the row's lineage columns under one label) is the schema; then
   "Eight rows", a compact table of only the schema columns that differ between rows, with the record's row
   marked. Values formatted by Polars.
5. **Gold: the workbench call,** then the "Open the demo notebook" button. It reveals, in place, a notebook
   in the homepage notebook style: `setup_notebook()`, the source's help card, `data.<source>.query(...)`,
   `.head()` of the key columns, one plot (a register with no time axis reads the table with `data.sql(...)`
   and shows a non-time output instead). Every output is real. "Copy notebook" copies the code only, ready to
   paste into Jupyter. One line says what the notebook needs installed and ingested.
6. **Foot:** the deep petrol band holds only related datasets. No caveats section, no GitHub or licence line.

No local-data references anywhere on the page: no "held locally", local row counts or local date ranges.

## Content rules

- Honesty is hard: no invented stats, no fake-live framing ("live", "now", timestamps, pulsing dots),
  no KPIs or uptime badges, no hire-me CTAs, testimonials or author photo.
- **No planning leakage:** no planned / shipped / trained / in-service labels, no phase or forecast
  codes, no counts of future work, no dashed "not built yet" styling. Describe what exists, neutrally.
- **No filler:** cut captions that restate the obvious or explain the method of a chart that needs no
  explaining.
- Punctuation: no em dashes; use commas, colons or parentheses.
- Model status truth lives in gridflow_models `notebooks/README.md`, not in old site copy.

## Do not use

Tracked all-caps eyebrows; middle-dot meta strings; "→" on links or buttons; big-number stat strips;
01/02/03 on things that are not a sequence; one-word period headlines; an italic or coloured single word
in a headline; Inter, Roboto, Arial, Fraunces or system stacks; cards as the default container, identical
rounded cards, soft grey shadows; gradient washes, glow, bloom; leaves, foliage, globes, hands, cartoon
people; hexagons; purple; coloured border-left callouts; cream plus serif; a literal borehole or drill
column; node-and-arrow flowcharts.

## Open

- The About section copy will be rewritten by Bobbo; the layout is locked.
- Pending copy approvals from the loop are listed in `.planning/v4/round-1-briefs.md`.
- Gate for every page: `node .claude/skills/impeccable/scripts/detect.mjs --json <page>` returns `[]`.
