# Phase 12 — HANDOFF (resume bible across /compact)

**Written:** 2026-06-20. **Read this first on resume**, then `12-BRIEF.md` + `FINDINGS.md`.

## Where we are
- **Milestone v3 — Recruiter-grade revamp.** Phase 12 (Review + Exemplar) **DONE**.
- **GATE PASSED 2026-06-20: user picked Direction A (Quiet refinement).** A = keep the calm cream/forest editorial look, apply the fixes, NO bold retheme. (Directions B-magazine and C-research were the alternatives — not chosen; their dirs/CSS can be deleted.)
- **Branch:** `feat/phase-12-exemplar`. All changes UNCOMMITTED. Never commit to main. Don't commit unless user asks.
- **Next:** Phase 13 (mechanical Stream-M sweeps, using A as the locked spec) → 14/15 (staggered Stream-C creative polish) → 16 (ship).

## Locked decisions
- D-V3-1..6 in `12-BRIEF.md` (theme=explore→**A chosen**; honesty cut; all-162 phased recruiter-first; exemplar-first gate **passed**; gridflow-models facade = `data.<source>.query("<slug>", start, end)` / `.describe(...)`, returns **pandas**, local-only **no pip/PyPI claims**; adaptive ~24h pacing).
- **mailto = `e.bentham31231@gmail.com` is CORRECT** (home-05 resolved — leave it).
- **NEW user feedback (2026-06-20): footer "Documentation site · cream paper" — USER DISLIKES IT.** Injected by `site/hifi/assets/site.js:48` on every page (review finding **site-02**). **Priority fix in Phase 13** — replace with one substantive line or remove. Adjacent: `site.js:73` hardcoded "6 vendors / 162 datasets" counts (site-01).

## What's built + VERIFIED (the exemplar = the Phase-13 spec)
- **`site/hifi/exemplar/fixes.css` = THE STREAM-M CSS SPEC** (verified **0 horizontal overflow at desktop AND 390px mobile**). Contents:
  - `--measure: 680px`; clamp `.chart`/`.code-wrap`/`pre.code` to it (dataset pages).
  - `#schema`/`#sample` → `overflow-x:auto; max-width:--measure` (wide tables scroll the section).
  - `.mono { overflow-wrap: anywhere }` (long paths/URLs wrap, let grid shrink).
  - `[data-chart] svg, .chart svg { height:auto }` (kill letterboxing).
  - Contrast tokens: `--ink-faint:#6f685a`, `--ink-ghost:#8b8374` (AA on cream).
  - `@media(min-width:721px)`: `.page-layout` `220px minmax(0,1fr)`; `.related-grid` + API `1fr 1fr` → `minmax(0,1fr)...` (fixes min-content blowout).
  - `@media(max-width:720px)`: `.page-layout` `minmax(0,1fr)`; `[style*="min-width: 340px"]`→0; `[style*="1.35fr 1fr"]`→`1fr` (theme.css's own mobile overrides MISS the shipped inline format — the real hero is `1.35fr 1fr` not `1fr auto`; card is `min-width: 340px` WITH a space).
- **Direction A pages (the LOCKED PATTERN to replicate):**
  - `site/hifi/exemplar/a-quiet/index.html` + `a-quiet/day_ahead_prices.html`.
  - Verified: dataset page rendered clean (editorial, contained); homepage eval-verified (0 overflow, 2 aligned tabs, no vaporware, facade present, no broken GridflowClient).
  - **Content edits applied on A (replicate these site-wide in 13):** facade tab swap; DuckDB SQL modernized to `silver_entsoe_day_ahead_prices` view; 6 headings varied (no more "What this dataset is."); all `cite` spans + class-path/`schemas.py Lnn` refs stripped (sed prototype worked); snapshot-note removed; fake 24h/7d/30d toggles removed; chart caption honest ("illustrative shape, seeded"); dated/`fetch deferred` hero line cleaned; homepage vaporware 4-model block cut; "Real-time"→non-live.
  - **Exemplar head/path note:** the exemplar pages link `/assets/theme.css` (real, via `../../assets/`) + a SEPARATE `/exemplar/fixes.css` and set absolute/`../../` asset paths. In PRODUCTION (Phase 13), fold `fixes.css` INTO `theme.css` so normal pages keep their existing relative links + just get the viewport swap + the example/honesty sweeps. (The exemplar's separate fixes.css + path tweaks were scaffolding to render under `/exemplar/`.)
- B/C exemplars (`b-magazine*`, `c-research*`) — NOT chosen; safe to delete.

## Phase 13 — mechanical Stream-M sweep (script over 162 pages + theme.css), from FINDINGS (37 M):
1. **Viewport**: `content="width=1280"` → `content="width=device-width, initial-scale=1"` on the 161 authored dataset pages (`system_prices.html` already correct = template).
2. **Fold fixes.css into theme.css** (the spec above, with breakpoint scoping intact).
3. **Examples**: Python·parquet/polars tab → gridflow-models facade; keep+modernize DuckDB·SQL (`read_parquet(...)`→`silver_<source>_<slug>`). Source-slug map: site `gie`→`gie_agsi`/`gie_alsi`, `openmeteo`→`open_meteo`, others unchanged. Homepage too (kill GridflowClient + pandas tabs).
4. **Honesty strip** (sed pattern proven): `<span class="cite">`/`src-cite` (~2042), `gridflow.silver...Transformer` class paths, `schemas/*.py Lnn`, `V2-FIX-04`/`gridflow v0.7`, `.planning/` paths, snapshot-note "live wiring planned" (161), "1 shipping · N planned"/"Planned · Fn" chips, "vendor-doc fetch deferred"/"extended registration" asides, stale `2026-05/06` dates + example-URL params→placeholders, "Verified against vendor docs: <date>"→undated, "Real-time"→non-live, **footer "cream paper" + counts (site.js:48,73)**.
5. **charts.js**: Path B GB-Coal stack rendered on EU/gas pages (charts-01); unused uptime heatmap (charts-03).
- Gate: `gridflow-build --check` idempotent + `htmlhint` + `lychee --offline` green (CI contract). The build reads `authored-pages/` → `site/hifi/data-sources/` (generated, gitignored). Edit `authored-pages/` (source), not built output.

## Phase 14/15 — Stream-C creative (staggered ~24h):
- Per-page voice/cadence, de-AI-ify, content depth; home-02 model section, design-04 skills, sources-01 earliest-date reconciliation, elexon-05/entsoe-05 honesty, design-01/02 voice. (19 C findings in FINDINGS.md.)
- **Build `.planning/v3/page-manifest.json` first** (every page: vendor/group/tier/status) = the durable disjoint backlog the scheduled task consumes.
- Staggered: a scheduled task (CronCreate/scheduled-tasks MCP) re-wakes orchestrator ~every 2-3h → dispatch ~8-10 background agents on disjoint page sets → adaptive back-off → keep CI green. Recruiter-path tier first (home, architecture, 6 hubs, ~12 flagship), then long tail.

## INFRA GOTCHAS (cost hours — heed these)
- **Background agents repeatedly died on "API Error: Stream idle timeout"** (~5min, after reading large files; 2 failures). Did content edits by hand instead. If delegating in 13+: keep agent tasks SMALL/incremental (frequent output) or use Workflow with tight per-agent scope; expect some deaths.
- **Dev server is single-threaded** (`http.server.HTTPServer`); rapid preview reload-loops WEDGE it. Use clean single navigations.
- **MCP Claude_Preview renderer wedges**: eval-navigation stops sticking (path stays "/"); screenshots time out / `UnknownVizError`. Verify layout via numeric `preview_eval` (scrollWidth vs clientWidth) instead. For VISUAL checks, have the USER open live URLs.
- **MCP preview servers are EPHEMERAL** (drop between turns → "Server not found"). Port **8765** had a STALE process (couldn't rebind).
- **`uv` is NOT on the Git Bash PATH.** Use the venv python directly: `.venv/Scripts/python.exe`.

## SERVER RIGHT NOW
- Persistent dev server launched via Bash `run_in_background` on **port 8780** (`.venv/Scripts/python.exe -u src/gridflow_front_end/serve.py --no-open --port 8780`), serving `site/hifi`. Exemplar URLs work there (user is browsing). If dropped on resume: re-run that command. (Ignore stale 8765 processes.)

## Files this phase (branch feat/phase-12-exemplar, uncommitted)
- `.planning/phases/12-review-exemplar/{12-BRIEF.md, FINDINGS.md, 12-HANDOFF.md, d22-retrofit.py(ref)}`
- `.planning/CONTROL.md`, `.planning/STATE.md` (v3 kickoff notes)
- `site/hifi/exemplar/` (fixes.css, b-magazine.css, c-research.css, a-quiet/, b-magazine/, c-research/)

## IMMEDIATE next actions on resume
1. Confirm 8780 server up (`curl -s -o /dev/null -w "%{http_code}" http://localhost:8780/exemplar/a-quiet/index.html`); restart if needed.
2. **Fix footer "cream paper" (site.js:48)** — user explicitly flagged.
3. Plan + execute Phase 13 mechanical sweeps (5 sweeps above) using fixes.css + A pages as the spec; fold fixes.css→theme.css; verify CI gates.
4. Then page-manifest + the staggered Phase 14/15.
