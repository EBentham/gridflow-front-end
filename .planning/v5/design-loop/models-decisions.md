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
