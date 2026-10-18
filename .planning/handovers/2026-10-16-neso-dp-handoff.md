# Hand-off: NESO Data Portal catalogue on the site (2026-10-16, pre-compact)

## The task (from the control-room overseer, local_cfeb0e27-0adb-45b6-ad22-0f051dfdc714)

Put gridflow v0.22's NESO Data Portal catalogue on the site (front-end BACKLOG item 1): all 131 packages under
NESO's 16 Data Groups, each a published page or visibly held. Step 1: design with Bobbo (UI-design rule:
variants, he picks and mixes, lock in DESIGN.md and tokens). Step 2: batches FE-0 to FE-8 in the front-end
lane (Opus executes, subagents allowed, no Sol/Astra, no plan/diff review; gates before each merge:
`gridflow-build --check`, htmlhint, lychee, impeccable `detect.mjs`; a branch and PR per batch). Done = every
package on the site, gates green, PRs merged, a deploy record (Pages run id, deployed SHA, live URL, date,
gate exits) for the gridflow seat's acceptance ledger. Then tell the overseer (SendMessage to the id above).

Contract files (gridflow repo, `..\gridflow\`): `.planning/milestones/v0.22-ROADMAP.md` §Front-end track
(line ~864), `.planning/v0.22-FE-LEDGER.md` (one row per package; now ~137 lines, the 6 "E (pilot)" rows
landed: tec/interconnector/embedded registers etc.), `.planning/milestones/v0.22-ACCEPTANCE.md` (conditions,
expected totals by group, deploy-evidence table). Catalogue snapshot:
`.planning/research/neso-catalog-20261006T195819Z/catalog-snapshot.json` (131 packages; group =
`organization.title`; portal order = alphabetical). Vault: `quant-vault/30-vendors/neso-data-portal/datasets/`
(137 notes, one per package, frontmatter `dataset_keys` lists its tables).

## Bobbo's rulings in this session (record them in RULINGS.md at the next commit)

1. The Carbon Intensity API hub (`neso`) stays separate. Only the Data Portal hub (`neso_data_portal`, 3 pages
   today) grows to 131 packages in 16 groups.
2. Held packages are listed in their group with a plain one-line factual reason. No "coming soon", no unit codes.
3. **Superseded by 6.** (Was: a lighter catalogue page per package.)
4. Showcases with full write-ups: Demand Flexibility Service (current package `demand-flexibility`), Balancing
   Reserve auctions (`eac-br-auction-results`), Aggregated BSAD (`aggregated-bsad`), Constraint breakdown.
5. Round 1 rejected: "none look amazing". The hub must not be a long vertical list. He wants a **diagram of the
   16 groups that you click to expand**. The dataset pages must match the existing site exactly: the "What it is
   and how it's used" section split with the facts table on the right, a chart with talk, raw feed, schema and
   sample rows with the fold-out `…` expander (not a scrolling frame), and the notebook as on live pages.
6. **Every package page uses the full locked anatomy.** Held parts say why: what it is plus the facts table,
   then the raw feed with its files; the schema section lists the tables and says in one plain line why the rows
   are not shown. No chart and no notebook for held tables.
7. Staffing for round 2 is approved: **5 hub-variant agents, Opus 5.5 · xhigh, one variant each**, plus **the DFS
   page built through the real template** by one writer (Opus 5.5 · high) and one checker (Sonnet 5.5 · high).
   Estimate given: about 3-5M tokens for the hub round, 0.3-0.5M for DFS.
8. Process lesson: round 1 was built inline by the seat. That was wrong. Design variants and pages go to
   agents, per v5 (`.planning/v5-EFFORT-PLAN.md` Agents table; `.planning/v5/p26/agent-prompts.md`).

## Done so far

- Pushed front-end `main` (18b9357, a docs-only backlog commit) to origin.
- Round 1 canvas (rejected, reference only): https://claude.ai/artifact/FgTGeQEcnU542b6gL8GqmX. Sources are in
  this session's scratchpad `canvas/project/`.
- Data built in scratchpad (`...\a46469c2-19b0-4f57-b2d5-81c7c1abca22\scratchpad\`): `hubdata.py` joins the
  snapshot with the FE-LEDGER into `canvas/project/neso-packages.json` (group, title, slug, status pub/held,
  file count, formats, a generic held reason); `dfs-daily-cost.json` (accepted DFS cost per delivery day,
  Live rows of `demand_flexibility_utilisation_summary`, day offset from 2024-11-29, £k, event type n/d/u).
  Rerun `hubdata.py` from the gridflow repo root: the ledger has grown since.
- Status at the time: 59 packages with eligible output, 61 held, 11 not in the ledger (3 of them are the existing
  pages; 6 have since landed as "E (pilot)").
- Shared note for the session group:
  `C:\Users\Bobbo\AppData\Roaming\Claude\side-session-notes\local_cfeb0e27-0adb-45b6-ad22-0f051dfdc714\front-end-neso-dp.md`.

## Facts checked (use them; two earlier descriptions were wrong)

- Constraint breakdown: per day, cost (£) and volume (MWh) for four reasons: largest loss, inertia, voltage,
  thermal. Not "constraints, reserve, response, energy".
- `market_provided_inertia`: the same estimate with NESO's trades and bid-offer acceptances removed from
  generator positions (a counterfactual), not "the part the market provided". Unit GVAs. NESO has paused updates.
- DFS current package: archive season 2024-11-29 to 2026-03-27, current from 2026-04-14 (adds event_id,
  event_type Upwards/Downwards, UTC labels). Keys: summary and requirement `resource_id, delivery_date,
  window_from, service_requirement_type`; report adds `dfs_unit_id`. Notification is archive-only. Requirement is
  held (no publication time). Summary procured/cost = sum of the report's Accepted rows (never add them). Rejected
  rows' `dfs_procured_mw` is the bid. Event 141 (2026-10-05, 17:00-20:00 local): 500 MW asked each window;
  accepted 48.5, 50.1, 181.1, 182.0, 20.7, 19.9 MW; 45 accepted bids at 18:00.
- The real ingest CLI for the catalogue: `gridflow ingest neso_data_portal --all` (ADR-033). The per-package
  command is unverified.
- The existing NESO DP hub intro has mojibake ("NESOâ€™s") in `site/hifi/data/neso_data_portal.json`. Fix it in FE-0.

## Open plumbing question (resolve before spawning the DFS writer)

The build maps one mirror note `vault/<vendor>/<dataset>.md` per dataset key, with families in
`site/hifi/data/<vendor>.json` (`families[]` slug/title/members, lead carries the `page:` block; build with
`--only <vendor>/<lead>`). v0.22 vault notes are **one per package**, covering several dataset keys. Decide how a
package note maps to a family page (mirror name = lead key? a package-note loader?), and check
`page_fields.py` `FAMILY_MEMBERS = (2, 18)` against packages with more tables (skip-rates has 9 families; EAC
auction results 11). This is FE-0 plumbing in `build.py` (2,164 lines; `load_manifest`, `manifest_families`,
`page_view`, `blank_view`, `_hub_rows`). Also: the hub needs groups for 16 Data Groups, and
`hub.html.j2` gets whatever layout Bobbo picks.

## Next steps

1. Write the round-2 hub brief: a shared file with the real data (rerun `hubdata.py`), the site's
   `theme.css`/`tokens.css`/`hubs.css`/`site.js`, the landscape partials, DESIGN.md rules, and the five distinct
   ideas (one per agent): (1) groups drawn as parts of the landscape scenery; (2) a single-line diagram with each
   group a feeder off a busbar; (3) groups as seams in the geological section; (4) groups along the market's time
   horizon, years ahead to settlement; (5) a mosaic sized by package count. Each must use the site's own CSS and
   chrome and expand a group's packages on click, with held rows per ruling 2. Agents: `claude`, `model: opus`,
   prompt starts "Effort: xhigh", background, own scratch folder each. Then the seat publishes one page
   comparing them (HTML artifact with the site CSS as files, not the Design canvas) and Bobbo picks.
2. In parallel, after the plumbing question: set up a front-end worktree (branch off main) and a vault worktree
   (`docs/...` off quant-vault origin/master), a one-page BATCH file modelled on `.planning/v5/p26/BATCH-rest.md`,
   then spawn the DFS writer (Opus · high, writer family-page prompt from `agent-prompts.md`) and the checker
   (Sonnet · high).
3. After the picks: lock in DESIGN.md + tokens, then FE-0 (hub restructure, 16 groups, plumbing), then the batches.
   Writers per page as in v5; held pages per ruling 6.
