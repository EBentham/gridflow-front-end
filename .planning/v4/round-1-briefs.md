# v4 design loop — round 1 briefs (2026-09-25)

Canvas: https://claude.ai/artifact/K1sUKPqgomVPcDsarVvXkv · artboards 1440 × 1800 (first screen + next section).
Each variant was written against its own brief below, before any code. Baseline = `landscape-v1.html`
ported as August left it (its 34.6 GW / six-vendor numbers are August's, not current).

## Shared rules (all five)

- Real copy from `site/hifi/index.html`: headline, lede (seven vendors), CTAs, scope facts
  (7 vendors, 165 datasets, 4 markets, 17 years, 3 layers), vendor rows (codes, counts, cadences).
- Real FUELHH mix, 1–5 Aug 2026, mean of 240 settlement periods: Wind 6,408 MW (29%), CCGT 5,639 (26%),
  Nuclear 3,589 (16%), Imports 3,174 (14%), Biomass 2,350 (11%), Other 929 (4%). Slices sum to 22.09 GW;
  index.html's donut centre says 22.0 (flag to Bobbo).
- Any other curve comes from `site/hifi/data/chart-series.json` with its dataset, unit and window stated.
  Never `elexon/fuelhh` as output (it is a per-row mean, not total generation).
- Do-not-use (from the research doc): italic single-word headline accent, tracked caps eyebrows, middle-dot
  meta strings, "→" on links, big-number stats strip, 01/02/03 on non-sequences, one-word period headlines,
  Inter, cards as default container, fake-live framing, KPIs, hire-me CTAs.

## A — Engraved plate (inside electrified-landscape)

- **Attacks backlog:** 1 drawing language, 3 conventional type, 4 cards, 8 plain fuel-mix chrome.
- **Idea:** the landscape redrawn as a one-ink engraving (petrol ink on paper, line-weight hierarchy,
  parallel-hatch fills), chartreuse reserved for energised conductors only. The wordmark is set enormous
  in condensed Bricolage and the pylons stand in front of it.
- **Fuel mix:** no card; a hatched field strip printed as a plate caption ("Plate 1").
- **Next section:** the seven vendors as an engraved map legend, one drawn glyph each.
- **Memorable element:** the wordmark behind the pylon line.

## B — Borehole (inside electrified-landscape)

- **Attacks backlog:** 5 under-used geology, 2 repeated rhythm, 4 cards, 8 fuel-mix chrome.
- **Idea:** the page is a core log. A borehole column runs the full left margin with depth ticks; the hero
  is the surface; scrolling descends gold → silver → bronze and the content sits in the stratum it belongs to.
- **Fuel mix:** drawn as a core sample, fuel shares as layer thicknesses.
- **Next section:** the strata themselves with real table names; Forecasts sit in gold, the catalogue in bronze.
- **Memorable element:** the continuous borehole spine.

## C — Demand horizon (inside electrified-landscape)

- **Attacks backlog:** 7 nothing uniquely gridflow, 6 no motion, 8 fuel-mix chrome, 2 rhythm.
- **Idea:** the ridge line of the landscape IS real data: Elexon NDF national demand, Sat 1 to Wed 5 Aug 2026,
  weekend dip visible. Turbines and pylons stand on the curve. One authored motion: the ridge draws in on
  load (reduced motion respected).
- **Fuel mix:** the foreground land divided into six plots proportional to share.
- **Next section:** seven feeds as a ridgeline stack, one real series per vendor, units stated.
- **Memorable element:** a horizon a domain reader recognises as a demand curve.

## D — Type as instrument (wildcard: no illustration at all)

- **Tests:** whether illustration is the wrong register altogether.
- **Idea:** the fuel mix is the hero, set as type: each fuel's name at a cap height proportional to its
  share (a typographic bar chart). Anybody (variable width) + Martian Mono numerals. Pale steel ground,
  one amber signal. No drawing anywhere.
- **Next section:** 17 years of gas share (NESO historic generation mix) as the one chart, vendors as a
  dense list beneath.
- **Must avoid:** broadsheet hairline columns, near-black + acid accent.

## E — Single-line diagram (wildcard: engineering schematic)

- **Tests:** whether the right register is the engineer's drawing, not the landscape.
- **Idea:** the page is an electrical single-line diagram on drafting film. Navigation is a busbar; the
  fuel mix is six generators feeding the busbar with MW labels; closed breakers in red, open in green
  (UK switching convention). B612 + B612 Mono (cockpit-display face).
- **Next section:** the pipeline as the same diagram: seven vendor feeders into a bronze bus, transformer
  to silver, transformer to gold, DuckDB as the load.
- **Must avoid:** blueprint blue, dark control-room screen.

## Round log

- Round 1 sent 2026-09-25. **Bobbo: B (borehole) is interesting, likes the design, not sure about the
  borehole itself.** → round 2 explores B's look (petrol sky hero, surface strip, page as tinted strata,
  fuel mix as a core, content in its own layer) without the drill column. A, C, D, E and the baseline set
  aside for now (not rejected on record; no comments given).

## Round 2 briefs (all keep: B's palette and type, sky hero, surface strip, core-sample fuel mix)

- **B1 Open section** — the control. Borehole removed, content takes the full grid, layer names ride the
  contact lines at the right edge like section annotations. Tests: was the spine the only problem?
- **B2 Block diagram** — the hero art becomes a textbook geological block: landscape on the top face,
  gold/silver/bronze on the cut faces, labelled along the face. Below it, straight hard-edged bands.
- **B3 Dipping beds** — strata tilt and rise to the right with bedding lines; content zig-zags from side to
  side to stay inside its layer. Tests: can the strata give the page movement instead of stacked slabs?
- **B4 Quarry benches** — the ground is cut into steps; each layer's exposed face is on the left and its
  content sits on the bench, so the page descends diagonally.
- Round 2 verdict (Bobbo): "None of those 5 look amazing, but I like the general colours, fonts, design
  style." New steer: the energy theme (renewables, net zero, data centres, emerging electricity-market
  trends). Round 3 = the full existing homepage redesigned three ways, by three parallel Opus agents with
  independent briefs (shared context: scratchpad `r3/SHARED.md`): **R3-1 panorama** (the new grid drawn,
  the scene doubles as the fuel-mix legend), **R3-2 transition** (the 2009-2026 gas share as the horizon,
  data-led), **R3-3 section** (physical grid above ground, data layers below, joined by cable).
- Round 3 delivered 2026-09-26 (canvas row 4): R3-panorama 1440x5973, R3-transition 1440x7060, R3-section
  1440x5138; detector clean on all. Agent finding: the NESO historic-mix series points are ~54-day means,
  not sampled half-hours. R3-3 caption reworded (it implied Open-Meteo is met-mast data). Each agent's NEW
  COPY lines await Bobbo's approval. **Pick (Bobbo, 2026-09-26): R3-3 "Above ground, below ground"** is
  the direction. Ask: add a section that makes the purpose explicit (a research platform whose pipeline
  exists to support quantitative work and trading research; he liked R3-2's "The warehouse exists to
  support quantitative work" framing). **R3-section-v2 delivered 2026-09-26** (canvas row 4, 1440x5343):
  purpose section right after the fuel mix, merged with the models list as a data-to-price-forecast flow.
  NEW COPY pending approval: "The pipeline and the catalogue are the means; the models are the point." /
  "The aim is a price forecast: the input that trading research starts from."
- **2026-09-26 (Bobbo): R3-section-v2 is THE design; it will be extended to the full site.** Fixes for all
  pages: no planning leakage (no planned/shipped labels, F-codes), cut the "typed, partitioned, deduped"
  filler under the silver tables, replace the "Joined, analysis-ready views in gold" wording, drop "bedrock".
  The "SQL or Python: pick one" section is to be replaced by a showcase of the gridflow-models notebook
  workbench (`setup_notebook()` → `data` / `models` / `common` handles, seven shared verbs per source,
  help cards, tab completion). Building R3-v3-A/B/C (identical except that section) in scratchpad `r3/r3-5`.
  Found: gridflow_models `notebooks/README.md` lists wind and solar models as trained, so the site's
  "planned" labels were also stale.
- **B5 Quiet strata** — docs-grade restraint: daylight page, each layer reduced to one full-bleed textured
  band that carries its name and table names; content sits on plain ground between.
- **2026-09-26 (Bobbo): notebook variant A picked.** Tweaks: notebook named `fuelhh_analysis.ipynb`, add a
  `df.head()`-style cell (real silver FUELHH rows). Next round: lock everything, three variants of the
  purpose section only (he dislikes the node-and-arrow flow). Building R3-v4-base + P1/P2/P3 in `r3/r3-6`.
  Handoff: `HANDOFF-design-loop-2026-09-26.md`; file backup: `design-loop/`.
- **Row 6 published 2026-09-26 (canvas v12):** R3-v4-base (notebook tab `fuelhh_analysis.ipynb`, `df.head()`
  cell with real silver FUELHH rows) + P1 merit-order stack / P2 model questions / P3 specimens, all
  1440x5919 and differing from base only in the purpose section. Detector `[]`, no leak words. P3's demand
  fan is real: gold forecast run a55a829bc51c40b2, fold 12, issued noon D-1, actual = Elexon INDO. The
  other P3 panels and P1's stack are drawn without scales and say so. Awaiting Bobbo's pick.
- **2026-09-26 (Bobbo): P1 merit-order stack picked, layout "a bit mid".** Row 7 published (canvas v14):
  v5-A panorama stack, v5-B clearing a distribution, v5-C the forecast assembled (C's top line = real
  median demand forecast for 4 Aug 2026, peak 28.1 GW, run a55a829bc51c40b2). All 1440x5919, identical to P1
  outside the section, detector `[]`. Brief: `design-loop/r3-7/R7-BRIEF.md`. Awaiting pick.
- **2026-09-26 (Bobbo): v5-B leads.** He asked why wind and solar were absent and what the histograms
  mean (answered from fundamentals_smp model.py/sampler.py: 1,000 independent residual-demand draws, one
  stack, quantiles of cleared prices). Revision published (canvas v20): demand, wind and solar bars with
  spreads feed the residual-demand histogram. NEW COPY: "residual demand", "less solar", "less wind",
  "demand"; index: "Demand less wind and solar: 1,000 draws, each a demand draw less a wind draw and a
  solar draw."
- **LOCKED 2026-09-26 (Bobbo): v5-B is the design.** Last edits: a notebook `[5]` cell plotting real
  silver FUELHH WIND (240 half-hours, 1-5 Aug 2026, 788 to 14,316 MW) via
  `df[df.fuel_type == "WIND"].plot(...)`, and the catalogue's "Each line is one dataset..." note removed.
  Reference board `R3-final.dc.html` (1440x6317, canvas v21, row 8). `DESIGN.md` (repo root) and
  `site/hifi/assets/tokens.css` written; repo CLAUDE.md locked-decisions line updated. Bobbo will rewrite
  the About copy himself.
