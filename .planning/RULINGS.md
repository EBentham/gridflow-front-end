# gridflow-front-end — seat rulings (from v5, 2026-09-26)

One line per ruling. `OWNER` = Bobbo typed it. `PROXY-SOURCED` = the seat ruled it under autonomous mode
(classes 1-3); every PROXY-SOURCED line is a veto slot at the milestone close. Evidence, never intention.
Earlier milestones keep their decisions phase-local (`phases/`, `docs/adr/`).

| # | when (UTC) | unit | source | ruling |
|---|---|---|---|---|
| 1 | 2026-09-26T17:15Z | design | OWNER | Homepage design locked: canvas v5-B chosen, final board R3-final; DESIGN.md and site/hifi/assets/tokens.css written; CLAUDE.md locked line updated. Bobbo will rewrite the About copy himself. |
| 2 | 2026-09-26T17:15Z | milestone | OWNER | "go with all your recommendations, start phases 22 to 24": v5 ratified (v5/MILESTONE.md). D1 v4 closed, v5 opened. D2 dataset agents write the canonical vault; the 130 authored overrides retire. |
| 3 | 2026-09-26T17:15Z | milestone | OWNER | Same ratification: D3 real charts only via a new silver distil, seeded fallback deleted. D4 the site documents only what gridflow ingests; NESO Data Portal stubs dropped. D6 integration branch v5/site, one cutover. |
| 4 | 2026-09-26T17:15Z | D5 | OWNER | Near-duplicate endpoint variants become family pages: the Phase 22 audit proposes the families and Bobbo rules on each one. |
| 5 | 2026-09-26T17:15Z | D7 | PROXY-SOURCED (class 1, ratified text) | The live drift check is not approved by the ratification: D7 itself required his explicit yes. It waits for "run it" with his ENTSO-E key set; Phase 22 proceeds without it. |
| 6 | 2026-09-26T17:15Z | git | PROXY-SOURCED (class 2, seat interpretation) | Commit authority for v5: commits and PRs into v5/site as the plan describes, plus docs-only commits to main. The cutover merge to main stays Bobbo's. Veto slot. |
| 7 | 2026-09-26T17:15Z | seat | PROXY-SOURCED (class 2, routing) | The OWNER front-end lane (2026-09-26) governs v5: Opus 5.5 executes, no Sol/Astra, no tiers. The seat is a plain chat, not /jarvis (unit-pipeline). This seat: claude-opus-5-5. |
| 8 | 2026-09-26T23:16Z | milestone | OWNER | "everything that can be done autonomously, done autonomously" while he sleeps: overnight run is 22, 23, 25a (design-independent pipeline) and round 1 of the 24 and 27 loops. 25b waits for the 24 lock. |
| 9 | 2026-09-27T00:31Z | 25a | PROXY-SOURCED (class 2, delegated merge) | PR #40 chart pipeline squash-merged into v5/site (c9da254) after seat re-ran the gates green. Detail: v5/P25A-MERGE.md |
| 10 | 2026-09-27T06:17Z | 22 | PROXY-SOURCED (class 2, data op) | Live gridflow ingest of 39 datasets without silver: 23 ok, 12 vendor-empty, 2 unconfigured, 2 GIE news 0 rows; silver 126 to 149/165; nothing overwritten. Receipts: v5/ingest-receipts/ |
| 11 | 2026-09-27T06:17Z | 22 | PROXY-SOURCED (class 1, gate) | Seat spot-checked five DATA-MATRIX rows against silver, code and vault; all match. Matrix handed to Bobbo with PROPOSALS.md for family and page-set rulings. |
| 12 | 2026-09-27T11:41Z | D5 | OWNER | Families: accept all 23 proposed in v5/PROPOSALS.md; each family is one page listing its variants. |
| 13 | 2026-09-27T11:41Z | D4 | OWNER | Page set: the site documents only datasets gridflow ingests with local data; NESO Data Portal stubs, empty and unconfigured datasets dropped, GIE news held. |
| 14 | 2026-09-27T11:41Z | D4 | OWNER | Headline dataset count is computed by the build from the pages it renders (149 today), never hand-typed. |
| 15 | 2026-09-27T11:41Z | 27 | OWNER | Wind and solar models are shown as they stand (never trained); the gridflow_models README fix is separate work. |
| 16 | 2026-09-27T11:41Z | gridflow | OWNER | gridflow adds all 29 NESO Data Portal packages (separate gridflow work, not blocking v5); each gets a page once its data lands. |
| 17 | 2026-09-27T11:46Z | 23 | OWNER | Homepage approved on desktop ('looks amazing, I am happy with it'), copy as written; PR #41 squash-merged into v5/site (18e98b2) after seat re-ran gates on the merge result. Phone look not possible; mobile rough edges queued. |
| 18 | 2026-09-27T15:36Z | 24 | OWNER | Dataset page schema and sample rows: option 4 'One record, then many' (one real row as the schema, then an eight-row table of only the differing columns). |
| 19 | 2026-09-27T17:04Z | 24 | OWNER | Dataset page design locked ('looks good, lock it'): layout A, A's chart, schema option 4, demo notebook drawer. Anatomy in DESIGN.md; next is the template and a five-dataset pilot. |
| 20 | 2026-09-27T17:49Z | 27 | OWNER | Architecture page design locked ('lock it'): round 2 of 'The specimen', desktop and phone boards in arch-r2, pandas notebook read, scope line 'runs under' an orchestrator. |
| 21 | 2026-09-27T19:17Z | 27 | OWNER | Models page stays high level for now: each model's job, inputs and chain, light headline scores at most; no inner workings, no gate or coverage failures. Supersedes #15's 'never trained' wording. |
| 22 | 2026-09-27T19:17Z | 27 | OWNER | Model status on the site follows gridflow_models code and manifest, not notebooks/README.md, until that README is fixed. |
| 23 | 2026-09-27T19:50Z | 27 | OWNER | Models page: design 2 'Converging cables', minus the no-orders line and the notebook section, plus a short in-development note. No licence line anywhere on the site. |
| 24 | 2026-09-27T20:10Z | 27 | OWNER | Models page design locked ('looks good'): round 2 of 'Converging cables', desktop and phone boards in models-r2, turbine clipping fixed. |
| 25 | 2026-09-27T20:45Z | 25b | OWNER | Dataset rollout cost accepted: about $7 per page for the author, plus an Opus reviewer, for the remaining pages. |
| 26 | 2026-09-27T20:45Z | 25b | OWNER | Imbalance-volume sign: an Opus agent investigates (Elexon docs, gridflow code, the rows) and concludes; pages state no sign until then. |
| 27 | 2026-09-27T20:49Z | 25b | PROXY-SOURCED (class 1, Opus investigator) | Imbalance volume: positive NIV = system short, negative = long (Elexon N0430 and imbalance pricing page; gridflow passes it through; a year of rows fits). Vault domain note corrected on the pilot's vault branch; system_prices page states it. |
