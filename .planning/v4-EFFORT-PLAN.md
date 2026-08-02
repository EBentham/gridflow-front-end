# v4 — Full rebrand · EFFORT-PLAN

Created 2026-08-02 alongside ROADMAP § v4. Per-phase ceremony tiers; unit-pickup
resourcing plans confirm-or-escalate these pre-assigned tiers rather than re-deriving.
Tiers govern WHICH stages run, never how many review passes — reviews run to convergence
(stop only when a pass comes back clean or nit-only).

| Phase | Tier | Justification | Pipeline notes |
|---|---|---|---|
| 17 Identity directions | **T2** | Bounded design freedom; deliverables are DESIGN.md docs, no production code; wrong choices cheap to reverse pre-exemplar | Orchestrator (fable seat) mines refs inline; grill each DESIGN.md against the brief; **user checkpoint replaces Sol review** (taste is the user's — not model-reviewable) |
| 18 Exemplar + gate | **T2** | Creative code bounded by the DESIGN.mds; 2 pages × 2-3 directions; user gate is the ultimate review | Executor per direction with browser screenshot loop; design-critique + accessibility-review skill passes per candidate; **Sol diff review on the WINNING direction only** (its code becomes the phase-19 spec), to convergence |
| 19 Theme rebuild + recruiter path | **T3** | Shared layer (`theme.css` × 172 pages) + open design execution + changes what lands on disk site-wide | Full pipeline: planner → grill → Sol plan review to convergence → executor (**opus · high** per T3) → verifier (**opus · high**) → Sol diff review to convergence; diff re-review whenever fixes touch production code |
| 20 Long-tail fleet | **T2** | Per-page application prescribed by the locked spec; volume not judgment; silent-failure class = facts drift | Staggered background batches on disjoint page sets (D-V3-6 pacing); objective verification fleet (facts-accuracy · consistency · gates — not taste); Sol diff review per batch to convergence |
| 21 Consistency + a11y + ship | **T1** | Fix-prescribed mechanical sweeps + gate suite | Executor → gates (build --check · htmlhint · lychee) → Sol diff review |

Agent rows use pinned frontmatter defaults (gsd-executor / gsd-verifier **sonnet · high**,
gsd-planner **opus · high**) except phase 19's per-spawn **opus · high** upgrades noted
above. gsd-phase-researcher spawns only for named unknowns (none currently named).

**What could push effort higher:** a 4th direction at 17/18; the user gate rejecting all
directions (re-enter 17); phase 19 colliding with the 172 authored pages' inline `style`
attributes — if the new identity requires per-page structural edits beyond `theme.css` +
sweepable patterns, 19 grows toward a second fleet phase (re-present resourcing, don't
silently expand).
