# v3 voice diagnosis — where the site actually reads "AI-generated"

**Headline:** most of the prose is already good. This is targeted surgery, not a wholesale rewrite. The machine-feel is concentrated in a few specific places, and the biggest one isn't bad sentences — it's *sameness across pages*.

## Home page (read in full) — voice is mostly strong, light touch only
**Already good (leave it):**
- Hero lede — "Models for demand, wind, solar, and clearing prices sit one layer above." Confident, specific, human.
- Architecture-preview — "Backfills are idempotent. … Bitemporal — every row carries both event-time and ingestion-time so point-in-time queries are trivial." Reads like an engineer, not a generator.
- Scope strip, snapshot card ("Static snapshot · illustrative"), **About section** (user: leave it — it's good).

**The one real tell:**
- **Pillar 2 (Catalogue)** is the outlier — promotional + listy where the other two pillars are terse: *"…162 datasets, every one documented here at full fidelity. Each dataset carries schema, queries, and caveats."* Pillars 1 and 3 are one crisp line; this one over-explains and self-congratulates ("full fidelity"). → tighten to match the register of its neighbours.

**Minor:** "Pydantic v2 contracts" — a version-ish ref (borderline against the no-versions rule; probably fine as a stack name, flagging it).

## Dataset pages (the stated concern — "some of the actual datasets") — 3 tells, only one is "bad prose"
1. **Cross-page sameness = the dominant tell.** Individual overviews are often knowledgeable (day-ahead: "the price counterpart that implicit-auction net_positions clear simultaneously against"). But 162 pages share one rhythm and the same connective scaffolding — "It is sourced from … The raw XML lands in bronze, is validated against …, and written to …". Read one, you've heard all 162. *Uniformity itself reads as machine-made*, even when each page is fine.
2. **Internal-code scaffolding** — `TRANSFORMER` cells, "Defined in `schemas/…py` (lines NN)", inline `…Transformer` refs. Reads like generated provenance, not authored docs. (Already queued for removal — Phase 13 deferred backlog.)
3. **Thin long-tail.** Flagships have depth; the long tail likely leans harder on templated phrasing (to confirm while sampling).

## What this means for the plan
- **Home:** a light, targeted edit (tighten pillar 2; leave hero/arch/about), not a rewrite. I'll do it and show you as the voice gold-standard.
- **Datasets:** the exemplar→fleet plan stands, but the fleet's real jobs are **(a) break the cross-page sameness** (vary openers/cadence so pages stop sharing one rhythm), **(b) strip the code scaffolding**, **(c) deepen the thin ones** — all under the hard facts rule: reorganize/sharpen, invent no claim not supported by the page/vault/gridflow.
- Net: the site is in better shape than "looks AI-generated" implies. The win is consistency-breaking + honesty + selective depth, not mass prose replacement.
