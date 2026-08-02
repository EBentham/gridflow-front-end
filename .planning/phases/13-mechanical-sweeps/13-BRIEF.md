# Phase 13 — Mechanical Stream-M sweeps (resume bible)

**Milestone v3 — Recruiter-grade revamp.** Branch `feat/phase-12-exemplar` (all uncommitted).
**Approach (advisor-confirmed, = charter Stream-M/C):** Phase-13 edits are **scripted** — idempotence is a CI gate and background agents timed out twice on this exact work. **Agents do _substantive_ verification** (example-correctness vs the registry + prose coherence by reading sampled pages), not the edits. The creative fleet lands in **14/15**.

## Batch 1 — DONE + verified + all gates green (2026-06-20)
- **Footer:** removed "Documentation site · cream paper" ([site.js:48](../../../site/hifi/assets/site.js)). Counts at `site.js:73` read `6 vendors · 162 datasets` — correct, left as-is.
- **Viewport:** 161 dataset pages `width=1280` → `width=device-width, initial-scale=1` via `v3_sweep.py --only viewport`. Two spellings existed (`" />` ×130, `"/>` ×31 — the two populations); both normalised. 0 residue. `system_prices` + 6 `_landing` hubs were already correct (7).
- **theme.css fold:** appended `fixes.css` (the approved Direction-A spec) to the end of `site/hifi/assets/theme.css` — `--measure:680px` clamp on `.chart`/`.code-wrap`/`pre.code`/`#schema`/`#sample`, grid `minmax(0,1fr)` blowout fixes, `.mono` wrap, chart `height:auto`, AA-contrast `--ink-faint`/`--ink-ghost` (later `:root` wins by cascade = exact approved load order). **Verified on production `entsoe/day_ahead_prices`:** 0 horizontal overflow at **1280px AND 487px**; chart + schema clamp to **680px** instead of stretching the **917px** column (the "figures/tables too wide vs the page" complaint — fixed).
- **Exemplar scaffold MOVED** `site/hifi/exemplar/` → `.planning/phases/12-review-exemplar/exemplar/` — it was the only source of lychee errors (broken relative links from copy depth) and was never meant to ship. Kept as the **Batch-2 pattern reference** (a-quiet = locked Direction A).
- **Gates:** `build --check` idempotent (162 pages + 6 hubs) · `htmlhint` 0 errors · `lychee --offline` **4349 links, 0 errors**.

## Batch 2 — NEXT (examples + honesty; judgment-laden, two-population)
**THE REGISTRY IS AUTHORITATIVE — load it, don't guess (advisor):**
`C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow_models/src/gridflow_models/research/handles/_get_method_registry.py`
- `_DATASET_SOURCE: dict[slug -> source]` and `_DATASETS_INVENTORY: (slug, source, date_col)`. **Slugs == site filenames.** Sources: `elexon, entsoe, entsog, gie_agsi, gie_alsi, neso, open_meteo`.
- Load at script runtime via `importlib` from that path; **fail loud** if absent (never silently fabricate).

**Example swap (D-V3-3):**
- **Python·parquet tab → gridflow-models facade.** Body:
  `from gridflow_models import setup_notebook` / `data, models, common = setup_notebook()` /
  `df = data.<source>.query("<slug>", start, end)` / `data.<source>.describe("<slug>")`. Relabel tab "Python · gridflow-models". Returns **pandas**; NO pip/PyPI/availability claims (local-only v0.1.0).
- **DuckDB·SQL tab → keep + modernize:** `read_parquet('.../silver/<source>/<slug>/**/*.parquet')` → `SELECT * FROM silver_<slug>`. **View name = `silver_<slug>`** — CONFIRMED from package code (`control/discover.py:245` "e.g. `silver_fuelhh`"; `_get_method_registry.py:398` interpolates `silver_{dataset}`). **NOT `silver_<source>_<slug>`** → the exemplar's `silver_entsoe_day_ahead_prices` is WRONG; fix it in the moved exemplar too.
- **source resolution:** `source = _DATASET_SOURCE[slug]`. `gie/` splits per slug (`lng`→`gie_alsi`, rest→`gie_agsi`); `openmeteo/`→`open_meteo`; others = dir name.
- **ORPHANS:** site slugs absent from the registry (registry entsoe=47 vs site=49 — e.g. `commercial_schedules_net_positions`) → **SKIP the facade swap + LOG**. Don't emit a `data.entsoe.query("...")` that would raise. Quantify the orphan set in the dry-run.

**Cite-strip (D-V3-2) — SAFE in Phase 13 (inspected, evidence-backed):**
- The `cite`/`src-cite` spans are **TRAILING provenance tags** — they sit at the END of schema-table cells (after "Source: `<vendor field>`.") and caveat boxes, NOT mid-sentence. Removing the span leaves grammatical prose with honest **vendor-field** provenance. This is the advisor's "self-contained → safe in 13" branch.
- Regex: remove `<span class="(?:cite|src-cite)">[^<]*</span>` → `''`. **2042 spans across 129 pages** (all non-Elexon; the 33 Elexon pages have none). Internal class-path refs (`schemas/entsoe.py L15`, `silver/...py L69`, `connectors/...py::ENDPOINTS`) are **confined to these spans**, so this == the internal-code-ref honesty cut.
- Minimal removal (span only, no greedy leading-whitespace) = zero word-join risk; leftover trailing space before `</td>`/`</p>` is invisible.

**Other honesty (safe element-removal — still TODO: inspect the element forms first):** stage/"planned" chips, version/build strings, snapshot-notes, dated "verified" lines that are their own nodes. Likely safe whole-element removal; confirm shapes on both populations before scripting.

**MUST DO before writing the example sweep:** read the current Python + DuckDB **tab markup** in BOTH `authored-pages/entsoe/day_ahead_prices.html` (generated) AND `authored-pages/elexon/fuelhh.html` (hand-authored) — structures may differ; one regex won't fit both blindly.

**SACRED REFS in v3:** `fuelhh`/`system_prices` are **no longer frozen** — the new a-quiet exemplar is the gold standard. Sweep them too (bring to the new standard); just verify them most carefully.

## Verification (THIS is where agents earn their keep in 13)
After Batch 2 applies: a **Workflow** fans out ~8–10 agents across disjoint page cohorts to **read sampled pages** and verify: (a) example `source`/`slug` correct per registry, (b) DuckDB view = `silver_<slug>`, (c) no prose mangled by the cite-strip, (d) no honesty leaks remain, (e) orphans handled. Substantive (reads pages), not a re-grep of what the script guarantees. Then re-run the 3 gates.

## Tooling / gotchas
- Script: `.planning/phases/13-mechanical-sweeps/v3_sweep.py` — idempotent, churn-free LF I/O (`open(..., newline="")`), `--apply` / `--only`. viewport implemented + applied; add registry loader + example + honesty sweeps.
- Gates (no `gridflow-build` console script in venv; call `main` directly; `uv` not on Git Bash PATH):
  - `.venv/Scripts/python.exe -c "from gridflow_front_end.build import main; raise SystemExit(main(['--check']))"`
  - `htmlhint --config .htmlhintrc 'site/hifi/**/*.html'`
  - `lychee --offline --include-fragments 'site/hifi/**/*.html'`
- Build reads `authored-pages/` (source) → `site/hifi/data-sources/` (gitignored). **Edit `authored-pages/`, not generated output.**
- **Preview-server CSS caching:** the preview/dev server serves the updated file, but the browser caches `theme.css` from before an edit. To verify CSS changes, cache-bust the `<link>` (`link.href = link.href.split('?')[0] + '?cb=' + Date.now()`) then re-measure — a stale read shows empty `--measure` / `maxWidth:none` even when the server is correct.
- Screenshots via MCP preview wedge (30s timeout); verify layout numerically with `preview_eval` (scrollWidth − clientWidth, computed `maxWidth`).
