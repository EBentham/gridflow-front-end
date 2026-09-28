# Models page: decisions with Bobbo (2026-09-27)

Base: round-1 direction A (`p27-r1/canvas/project/A-models.dc.html`, generator `p27-r1/A/p_models.py`).
Picker: https://claude.ai/artifact/MpySKZLbpbe6VmCz4pcuzV ("Models page (as it stands)").

## Feedback on A as it stands (OWNER)

- **Keep:** the top, the cables running from each source image (demand, wind, solar, plant fleet) to the models.
- **Fix:** it looks cluttered.
- Asked how fundamentals SMP differs from the GB merit-order stack. Seat's answer (to be confirmed by the
  content check): the stack (`stack.gb.v1`, GBStackModel) is a constructive supply curve with no learning;
  fundamentals SMP (`fundamentals_smp.gb.v1`) composes the demand, wind and solar forecasts into residual
  demand, samples it, and runs it through the stack for a probabilistic price (`estimators/fundamentals_smp/model.py`
  docstring: no-op fit, refuses stale components). The page should show the chain (forecasts into the stack
  into SMP), not five sibling models.

## Plan (agreed)

1. Content check: one agent verifies every claim on A-models against gridflow_models, writes
   `models-content-check.md` (NEXT, started 2026-09-27).
2. Three designs, side by side by section, keeping the cables; launch after the weekly reset if budget is tight.

## After the content check (OWNER, 2026-09-27)

- **High level for now** (RULINGS #21): the page shows each model's job, its inputs (the cables) and how the
  models chain; at most light headline scores; no inner workings. Extend later when the modelling matures.
- Wind and solar: no mention of the failed 90% band or the coverage gate; describe what they do. Supersedes
  #15's "never trained" wording.
- Status follows the code and the manifest, not `notebooks/README.md` (RULINGS #22).
- Designers launched the same evening (not after the weekly reset): three directions, `models-r1/`.

## Round 1 pick (OWNER, 2026-09-27)

- **Design 2, "Converging cables"** (`models-r1/2/`), with three changes:
  1. Remove the line saying it does not produce orders, positions or P&L.
  2. Remove the notebook section at the bottom; in its place a short line along the lines of "this is still
     in development" (his explicit wording choice, overriding DESIGN.md's no-planning-leakage default for this
     one line).
  3. Remove "This site is MIT-licensed. gridflow is Apache-2.0." (site-wide, asked twice: no licence line on
     any page; it also sits in `site.js` on v5/site and on the locked architecture boards).
- Fix (2026-09-27, Bobbo spotted it): the distant turbines' blades were clipped at the drawing SVG's top edge,
  so the petrol sky looked like it sat in front of them. Boards now set `.dr{overflow:visible}` (models-r2 and
  arch-r2). When building the real pages, give the drawing top room in its viewBox instead, so nothing relies on
  overflow and no ridge wider than the page can cause sideways scroll.

## LOCKED (OWNER, 2026-09-27)

- `models-r2/models-r2.dc.html` (1440) and `models-r2-390.dc.html` locked as they stand ("looks good"),
  including the turbine fix. Generator `models-r2/gen.py`. The opening keeps "It produces forecasts and prices
  for research." Next: build as `site/hifi/models.html` on a branch into `v5/site` (phase 27).
