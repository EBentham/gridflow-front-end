# Phase 13 — Batch 2 verification + honesty backlog

## Verdict: Batch 2 (facade examples + cite-strip) is CLEAN
- **~13-agent Workflow** (`wlhic8j33`): 11 returned + 2 adversarial agents died on the documented stream-idle-timeout (gie-split, orphan) → re-checked deterministically, both **correct**.
- **172 page-checks → 0 sweep-introduced issues.** GIE split correct (`lng`→`gie_alsi`, rest→`gie_agsi`); orphan `commercial_schedules_net_positions` correctly skipped (no fabricated facade, cites stripped, old example retained); reference-table variants (`bmunits_reference`, `intensity_factors`, `operators`, …) all map to `silver_<slug>`.
- **1 finding — pre-existing content, not a sweep artifact:** `neso/intensity_factors.html` caveat #04 has a self-referential dangling cross-reference ("see Caveats #04" pointing at itself for LCA factors that don't exist). All sweep checks on that page pass. → fix in 14/15.

## Batch 3 — MECHANICAL honesty — DONE (2026-06-20)
Locked by D-V3-2; what Direction A removed but Batch 2's cite-strip didn't cover. Applied + gated:
- **snapshot-note** `Static snapshot · live wiring planned` → **`Static snapshot · illustrative, seeded`** — 161 files. Two wrapper populations (130 generated `.snapshot-note` + 31 Elexon inline-styled) carried the identical text, so a text replace covered both. (Orphan's own note left untouched.)
- **fake chart time-toggle chips** removed — labels vary per page (24h/7d/30d, 1y/3y/5y, 12mo, 90d…), so anchored on the **bare `row gap-8` wrapper holding 2+ time-label chips**; the functional example tab row (`row gap-8 mb-16`) is preserved. Validated in-memory on both populations + a year-toggle page (chips 3→0, tab row intact); 0 toggle rows remain.
- Verification: deterministic (residue 0, idempotent across all 4 sweeps, htmlhint 172/0 structural, gates green) — uniform low-risk transforms didn't warrant another agent wave.
- **`Real-time` NOT swept** — inspection showed it is overwhelmingly factual data-cadence prose ("real-time (operator-reported)", "Real-time fuel mix"), not site-live framing → 14/15 judgment.

**→ Phase 13 (mechanical Stream-M) COMPLETE.** Three commits: batch 1 (viewport/measure/footer), batch 2 (examples/cites), batch 3 (snapshot/toggles).

## Deferred to 14/15 — JUDGMENT (inline / per-page; mechanical removal would mangle)
- **Inline class refs**, ~5/page on all 172 pages: `EntsoeDayAheadPrice`, `…Transformer` mid-sentence ("validated against X, written via Y"); these are grammatical objects — need prose rewrite.
- **"Defined in `gridflow/schemas/<v>.py · <Class>` (lines NN–MM)"** schema-intro lines (line numbers = the "code versions" the user called out).
- **`TRANSFORMER` / `PARQUET PATH` metadata cells** — structured; decide keep-as-architecture vs remove (PARQUET PATH is borderline-useful; TRANSFORMER class path is a clear internal-code ref).
- **Dated "Verified against vendor docs on `<YYYY-MM-DD>`"** — 40 files, inline prose → undate / reword.
- **"Real-time"** — 27 files, context-dependent.
- **neso/intensity_factors caveat #04** self-referential cross-ref.

## Tooling note
2 of 13 verification agents died on stream-idle-timeout (same infra issue as the content agents in Phase 12). For risk-area adversarial checks, a deterministic grep re-check is faster + reliable than re-spawning.
