# Handoff: v4 design loop (2026-09-26)

For the next seat picking up the v4 site redesign. Method: interactive design loop with Bobbo (Opus 5.5 · high),
variants on a Claude Design canvas, no pipeline until the look is locked (see
`design-capability-research-2026-09-25.md` § Ruling). Round-by-round log with every brief and verdict:
`round-1-briefs.md` (same folder). Nothing here is committed (repo rule: never auto-commit).

## Where things are

- **Canvas:** https://claude.ai/artifact/K1sUKPqgomVPcDsarVvXkv (private to Bobbo). Rows: round 1 (baseline + A–E),
  round 2 (B1–B5), round 3 (R3-1/2/3 + R3-3 v2), row 5 "Chosen design" (R3-v3-A/B/C). Always `read`
  `project/canvas.json` right before publishing: Bobbo's editor saves change it.
- **Working files:** session scratchpad
  `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\ac992240-285c-4da8-b171-cc11c165a9de\scratchpad\`
  (`canvas/project/` = what is published; `r3/r3-N/` = each agent's folder with its `gen.py`).
  **Backup in repo:** `.planning/v4/design-loop/` (SHARED.md, all published boards + canvas.json, and the
  r3-5 generator for the chosen page).
- **Agent brief shared by every design agent:** `design-loop/SHARED.md` (design system, content sources, honesty
  rules, do-not-use list, .dc.html format rules, verification recipe). Reuse it for any new agent.

## Decisions (Bobbo)

1. Direction: **"Above ground, below ground"** (R3-3): petrol sky; the physical grid of the energy transition
   drawn above ground (wind, solar, batteries, data centre, interconnector, pylons); gridflow's data layers
   below (bronze → silver → gold) joined by cables from the assets gridflow has feeds for. Palette: petrol
   #155A6E, horizon #3E8C97, chartreuse #AFC64E, olive #66793B, ink #1C2B22, daylight #F6F4EC, clay #C77E3C,
   khaki #A39A6A, medallion bronze/silver/gold. Type: Bricolage Grotesque / Hanken Grotesk / Red Hat Mono.
   The repo CLAUDE.md "cream + Fraunces" locked decision is superseded (not yet edited).
2. Theme: energy transition (renewables, net zero, data centres, emerging electricity-market trends), as
   drawing and framing only; gridflow has no data-centre / battery / EV data.
3. A purpose section right after the fuel mix: gridflow is a research platform; the pipeline exists to
   support quantitative work on power markets.
4. **No planning leakage anywhere on the site** (no planned/shipped labels, F-codes, "one shipped, four
   planned"), no needless filler captions. Saved as feedback memory `no-planning-leakage-on-site`.
5. Removed: "typed, partitioned, deduped" under silver; "bedrock"; gold now reads "Gold data is cleaned,
   joined and ready to use" / "Served as DuckDB views."
6. The "SQL or Python: pick one" section is replaced by **"Run it all from a notebook"**, a showcase of
   the gridflow-models workbench (`setup_notebook()` → `data` / `models` / `common`; seven shared verbs per
   source; help cards; tab completion). **Variant A (drawn JupyterLab session) picked.**

## LOCKED 2026-09-26

The design is locked: reference board `R3-final.dc.html` (canvas row 8), spec `DESIGN.md` (repo root),
tokens `site/hifi/assets/tokens.css`, CLAUDE.md updated. Items 1 and 3 of "Next after the lock" are done
(Design System artifact mirror not yet). Next: item 2, the real repo exemplar. Front-end lane (OWNER
2026-09-26): Opus executes, no Sol/Astra, no plan/diff review; gates `gridflow-build --check`, htmlhint,
lychee, detect.mjs; branch + PR. Nothing committed yet.

## In flight at handoff (historical)

Agent building in `r3/r3-6/` (brief in the chat; outputs):
- `R3-v4-base.dc.html` = R3-v3-A + notebook tab renamed `fuelhh_analysis.ipynb` + a `df[[...]].head()` cell
  with REAL silver FUELHH rows (2026-08-01 SP1: BIOMASS 2367.0, CCGT 9789.0, COAL 0.0, INTELEC 402.0,
  INTEW -532.0; 4,800 rows for 1–5 Aug).
- `R3-v4-P1/P2/P3.dc.html`: three variants of the purpose section only (P1 merit-order stack centrepiece,
  P2 the market questions each model answers, P3 small-multiples specimens per model). Bobbo dislikes
  the current node-and-arrow flow diagram. Next: verify (detector, markup, diff-only-in-section), publish as
  a new canvas row, get his pick.

## Open items for Bobbo

- NEW COPY awaiting approval (purpose section): "The pipeline and the catalogue are the means; the models
  are the point." / "The aim is a price forecast: the input that trading research starts from." Plus the
  notebook-section intro and whatever the P-variants add.
- Model status truth: gridflow_models `notebooks/README.md` says wind + solar are trained, stack is
  constructive, SMP is hybrid; the live homepage still says "planned". Moot on the page now (no status),
  but relevant to case-study pages.
- The live homepage donut says 22.0 GW; its slices sum to 22.09 (designs use 22.1).

## Next after the purpose-section pick (the lock)

1. `DESIGN.md` (palette roles, type scale, layout rules, drawing language, chart language, component
   conventions, personality, do-not-use list incl. the no-planning rule) + `tokens.css`.
2. Real repo exemplar: the homepage and one flagship dataset page (probably `elexon/fuelhh`) as site
   HTML/CSS in the existing build (`site/hifi/assets/theme.css`, `site.js` chrome, `build.py` Jinja
   templates for the 165 dataset pages).
3. Update the repo CLAUDE.md locked-decisions line; mirror DESIGN.md as a Design System artifact.
4. Roll out to the rest of the site through the unit pipeline (templates first, then hubs, architecture,
   models, About).

## Gotchas learned

- The in-app browser is not signed in to claude.ai: verify boards via static copies
  (`sed` recipe in SHARED.md) served by a temporary `v4-canvas-static` entry in `.claude/launch.json`
  (remove it after). Screenshots often stall: measure rects with JavaScript, or shift the page with a CSS
  transform instead of scrolling.
- Background design agents sometimes stop without a final report or stall on a server they started:
  check their folder's file times, then SendMessage them to wrap up, or verify the file yourself.
- `.dc.html`: no self-closing SVG tags, no `{{`, fixed-size root equal to `$preview`.
- A canvas editor save (2026-09-26, after v14) moved v5-B's whole `<main>` into v5-C: B went blank, C
  showed both sections stacked. Restored both from the scratch copies (v18). After Bobbo reports a board
  looks wrong, first `list` the artifact's files and compare sizes with `canvas/project/`.
