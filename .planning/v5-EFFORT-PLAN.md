# v5 — Site rebuild · EFFORT-PLAN

Ratified with `v5/MILESTONE.md` on 2026-09-26. **Lane: front-end (OWNER 2026-09-26).** Opus 5.5 executes,
subagents are allowed, no Sol/Astra, no tiers, no plan or diff review in the ceremony sense. Bobbo
validates visually. The deterministic gates run before every merge into `v5/site`:
- `uv run --system-certs --extra build gridflow-build --check`
- htmlhint and lychee
- `node .claude/skills/impeccable/scripts/detect.mjs --json <page>` returns `[]`
- no horizontal overflow at 390 px
- AA contrast

The one extra review is the objective Phase-26 dataset reviewer, which Bobbo asked for.

## Agents

| Role | Agent | Model · effort | Writes |
|---|---|---|---|
| Seat (orchestrates, rules, re-mirrors, commits, merges into `v5/site`) | this chat | Opus 5.5 · high | planning files, branches |
| Phase 22 data truth (matrix script, ingest, receipts) | `claude` (background) | Opus 5.5 · high (in prompt) | `v5/DATA-MATRIX.*`, C:\gridflow-data via `gridflow ingest` |
| Phase 23 foundation + homepage build | `claude` (background, worktree on `v5/site`) | Opus 5.5 · high (in prompt) | `site/hifi/**` on `v5/site` only |
| Design variants (24, 27) | `claude` | Opus 5.5 · xhigh (in prompt) | own scratch folder only |
| Template and chart pipeline (25), top-page builds (27) | `claude` or seat | Opus 5.5 · high | `v5/site` |
| Dataset author (26) | `dataset-page-author` (new, pinned; created in 25 as a `~/.claude` zone unit) | Opus 5.5 · high | its own canonical vault note + chart spec |
| Dataset reviewer (26) | `dataset-page-reviewer` (new, pinned; Bash inspection-only mandate) | Opus 5.5 · high | its review file only |

Never `general-purpose`. Fan-out search goes to `Explore` (haiku · low).

## Per phase: named unknowns and gates

**22 Data truth** (background agent; the seat reads the matrix, not the transcript)
- Unknowns:
  - Which of the ~40 datasets without local silver can be ingested (auth, retired endpoints, volume).
  - Where family boundaries fall (D5).
  - Why NESO has 34 vault notes but 33 pages and 23 silver tables.
  - Whether gridflow's registry agrees with the vault on the 165.
  - What the fresh validator says. That needs Bobbo's "run it" and his ENTSO-E key (D7).
- Output:
  - `v5/DATA-MATRIX.md` and `.json`, one row per dataset.
  - Ingest receipts (counts before and after, and a snapshot of anything overwritten).
  - Proposed families and page set for Bobbo to rule.
  - Per-dataset discrepancy list (input to 26).
- Gate: the seat spot-checks 5 rows against source by hand before handing the matrix to Bobbo.

**23 Foundation + homepage** (background agent in a worktree on `v5/site`)
- Unknowns:
  - How the absolute 1440 composition reflows at 390 and 768 (landscape, strata, the merit-order
    drawing, the notebook).
  - How the `site.js` chrome contract (`data-page` / `data-root` / `data-screen-label`) carries over.
  - Inline versus external SVG for the big drawings.
  - Font loading.
- Gate: the full gate list above, plus one mobile look with Bobbo.

**24 Dataset page design loop** (the seat with Bobbo, interactive; same method as the homepage loop)
- Specimens (all have local silver):
  - `elexon/fuelhh`
  - `elexon/system_prices` (price series)
  - `entsog/physical_flows` (daily gas flow)
  - `elexon/bmunits_reference` (no time axis)
- Unknowns:
  - The content model and word budgets.
  - Which chart types the fleet needs.
  - The "how to get it" cell. It must be the real gridflow-models call, `data.<source>.query("<dataset>",
    start, end)`, with the source handles taken from `gridflow_models/research/handles`.
- Agent brief base: `v4/design-loop/SHARED.md`.
- Output: an anatomy section in DESIGN.md. It replaces the repo CLAUDE.md "Dataset page anatomy" line.

**25a Chart pipeline + plumbing** (overnight; background agent in a worktree on `v5/site`)
- Unknowns:
  - Which silver columns and aggregations make a meaningful chart per dataset shape. The agent picks
    sensible defaults for the 4 Phase-24 specimens only; per-dataset specs are Phase 26 author work.
  - How the distil handles datasets with no time axis.
  - Where page fields sit in the vault note, which must not break `propagate-vault-mirror` or
    `gridflow-drift-check` parsing.
- Gate: `gridflow-build --check` green; pages with no series render no chart (no seeded shape); the NESO
  Data Portal stubs gone.

**24 and 27 round 1** (overnight; variant agents, the seat publishes canvases)
- 24: about 5 variants × the 4 specimens on a new canvas.
- 27: about 5 variants each for the data-sources landing, architecture and models (three more canvases,
  or rows on one).
- No picks are made overnight. The seat does not iterate past round 1 without Bobbo.

**25b to 28**: unknowns are named when the phase is picked up. The pilot in 25 measures the real cost per
dataset before 26 commits to its fan-out.

## Rollup (rough; replaced by measured actuals)

| Work | Estimate |
|---|---|
| 22 data truth (one agent + ingest) | ~1-2M tokens |
| 23 foundation + homepage (one build agent, 1-2 revision rounds) | ~1-2M |
| 24 dataset loop (~5 variants × 1-3 rounds; round 1 overnight) | ~2-4M |
| 25a chart pipeline + plumbing (overnight) | ~1-2M |
| 27 round 1 (3 pages × ~5 variants, overnight) | ~3-4M |
| 25b template + pilot | ~2-3M |
| 26 fan-out (~250-400k per dataset) | ~40-65M at 165 pages; ~25-40M with families |
| 27 later loop rounds + builds | ~3-6M |
| 28 cutover | ~1M |

The seat records actual spend as a RULINGS line at each phase close.

## Git discipline

- **Commit authority (seat interpretation of "go with all your recommendations", 2026-09-26):**
  - Commits and PRs into `v5/site` as the plan describes.
  - Docs-only commits to `main` (guard-exempt).
  - The cutover merge to `main` stays Bobbo's.
- **Branch setup order:**
  1. Commit the docs to `main`.
  2. Create `v5/site` from `main`.
  3. Commit `tokens.css` on `v5/site`.
  4. Only then spawn the Phase-23 agent, with `isolation: "worktree"`.
- **No checkouts in the shared working tree** while other phases use it.
- **Vault edits** (22 systemic units, 26 authors) go on quant-vault `docs/` branches. The mirror syncs
  only through `propagate-vault-mirror`, after those branches merge.
