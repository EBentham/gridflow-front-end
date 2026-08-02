# Phase 12 — Review + Exemplar (v3 kickoff)

**Milestone:** v3 — Recruiter-grade revamp
**Started:** 2026-06-20
**Status:** IN PROGRESS — multi-agent review launched; exemplar next; **GATED on user sign-off** before any autonomous scaling.

## v3 goal
Transform the deployed site from "looks a bit AI-generated" into a polished, refined, honest editorial front-end for energy-trading recruiters. Phased to all 162 dataset pages + 6 hubs at gold standard; recruiter path first.

## Locked decisions (kickoff interview 2026-06-20)
- **D-V3-1 Theme** — explore **2-3 refreshed Claude Design directions** on the exemplar; user picks one to scale. Keep editorial spirit (cream + forest-green, Fraunces / Inter / JetBrains Mono).
- **D-V3-2 Honesty cut** — strip: future/roadmap framing ("coming in v3", "planned", stage chips); version numbers / build-version strings; in-the-weeds **internal code-class refs** (e.g. `gridflow.silver.elexon.fuelhh.FuelHHTransformer`); stale example dates/URLs.
- **D-V3-3 Code examples** — keep **DuckDB · SQL** (modernize to `SELECT * FROM silver_<slug>`); **replace Python · parquet** with gridflow-models `data.<source>.query("<slug>", start, end)` / `.describe("<slug>")`. Frame as a **data-access layer — NO pip/PyPI/availability claims** (package is local-only v0.1.0).
- **D-V3-4 Focus** — all 162 eventually, **phased**: recruiter path (home → architecture → 6 hubs → ~12 flagship datasets) first; long tail later.
- **D-V3-5 Gate** — **exemplar-first**: build homepage + 1 flagship dataset page (default: `system_prices`) fully transformed, in 2-3 directions; user signs off before any autonomous scaling.
- **D-V3-6 Pacing** — **adaptive** staggered execution over ~24h; a scheduled task re-wakes the orchestrator each window, dispatches ~8-10 background agents on **disjoint page sets**, backs off on usage signals. (Applies to phases 14-15.)

## gridflow-models facts (verified 2026-06-20 — local repo `C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow_models`)
- Import: `from gridflow_models import setup_notebook` → `data, models, common = setup_notebook()`
- `data.<source>.query("<slug>", start, end)` → **pandas** DataFrame; `data.<source>.describe("<slug>")` → schema DataFrame. Dataset is a **string** arg (not `data.elexon.fuelhh`).
- Sources: `elexon`, `entsoe`, `entsog`, `gie_agsi`, `gie_alsi`, `neso`, `open_meteo`. (Site uses unified `gie` / `openmeteo` — map per dataset.)
- Underneath: still `read_parquet('.../silver/<source>/<slug>/**/*.parquet')` wrapped as DuckDB `silver_<slug>` views — so **DuckDB · SQL stays accurate**.
- Maturity: **local-only, NOT on PyPI, v0.1.0** (README stale; code is mature). pandas not Polars.

## Work-stream split (the load-bearing reframe)
- **Stream M — mechanical/cross-cutting:** deterministic sweep script(s) (the `d22-retrofit.py` pattern) + `theme.css` edits. Example-tab swap, honesty sweep, wide-figure/table fix. Fast, exact, uniform. NOT agent work.
- **Stream C — creative/per-page:** multi-agent, staggered over ~24h. De-AI-ify, content rewrite, per-page polish, theme application.

## Phase map
12 Review + Exemplar (gate) → 13 Mechanical sweeps (M) → 14 Recruiter-path polish (C, staggered) → 15 Long-tail polish (C, staggered) → 16 Consistency + a11y + ship.

## Phase 12 actions
- **A. Review** — workflow `v3-site-review`: 12 auditors (surface × lens) → adversarial verify → `FINDINGS.md` backlog + recommended revamp direction.
- **B. Exemplar** — homepage + `system_prices`, fully transformed (honest, gridflow-models examples, fixed formatting) in 2-3 Claude Design directions.
- **C. Gate** — present `FINDINGS.md` + exemplar; user picks a direction + signs off.

## Outputs
- `.planning/phases/12-review-exemplar/FINDINGS.md` — verified review backlog (Stream M + Stream C, recruiter-path-first)
- Exemplar pages (on a branch) in 2-3 directions for sign-off
