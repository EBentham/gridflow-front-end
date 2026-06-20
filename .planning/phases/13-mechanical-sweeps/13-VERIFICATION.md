# Phase 13 — Batch 2 verification + honesty backlog

## Verdict: Batch 2 (facade examples + cite-strip) is CLEAN
- **~13-agent Workflow** (`wlhic8j33`): 11 returned + 2 adversarial agents died on the documented stream-idle-timeout (gie-split, orphan) → re-checked deterministically, both **correct**.
- **172 page-checks → 0 sweep-introduced issues.** GIE split correct (`lng`→`gie_alsi`, rest→`gie_agsi`); orphan `commercial_schedules_net_positions` correctly skipped (no fabricated facade, cites stripped, old example retained); reference-table variants (`bmunits_reference`, `intensity_factors`, `operators`, …) all map to `silver_<slug>`.
- **1 finding — pre-existing content, not a sweep artifact:** `neso/intensity_factors.html` caveat #04 has a self-referential dangling cross-reference ("see Caveats #04" pointing at itself for LCA factors that don't exist). All sweep checks on that page pass. → fix in 14/15.

## Batch 3 — remaining MECHANICAL honesty (uniform; do in Phase 13)
Locked by D-V3-2; these are what Direction A removed but Batch 2's cite-strip didn't cover:
- **snapshot-note `Static snapshot · live wiring planned`** — 130 files (uniform `<div class="snapshot-note …">`). +1 orphan variant (`Placeholder snapshot · dataset removed — see commercial_schedules`). NB "live wiring planned" greps to 161 files — **~30 occurrences sit outside the snapshot-note div**; inspect those contexts before scripting.
- **fake `24h` / `7d` / `30d` chart toggle chips** — 72 files (decorative fake controls; no JS behind them).
- Decide neutralization wording (exemplar used "illustrative shape, seeded" for the chart caption; snapshot-note → an honest static-snapshot line with no future-framing).
- Validate on BOTH populations (Elexon hand-authored vs generated) before the script, same as Batch 1/2.

## Deferred to 14/15 — JUDGMENT (inline / per-page; mechanical removal would mangle)
- **Inline class refs**, ~5/page on all 172 pages: `EntsoeDayAheadPrice`, `…Transformer` mid-sentence ("validated against X, written via Y"); these are grammatical objects — need prose rewrite.
- **"Defined in `gridflow/schemas/<v>.py · <Class>` (lines NN–MM)"** schema-intro lines (line numbers = the "code versions" the user called out).
- **`TRANSFORMER` / `PARQUET PATH` metadata cells** — structured; decide keep-as-architecture vs remove (PARQUET PATH is borderline-useful; TRANSFORMER class path is a clear internal-code ref).
- **Dated "Verified against vendor docs on `<YYYY-MM-DD>`"** — 40 files, inline prose → undate / reword.
- **"Real-time"** — 27 files, context-dependent.
- **neso/intensity_factors caveat #04** self-referential cross-ref.

## Tooling note
2 of 13 verification agents died on stream-idle-timeout (same infra issue as the content agents in Phase 12). For risk-area adversarial checks, a deterministic grep re-check is faster + reliable than re-spawning.
