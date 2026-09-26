# v5 — The site, rebuilt in the locked design (RATIFIED 2026-09-26)

Status: ratified by Bobbo 2026-09-26 ("go with all your recommendations, start phases 22 to 24").
D1-D6 stand as recommended; D5 = the audit proposes families and Bobbo rules per family; D7 = the live
drift check waits for his explicit "run it" once the ENTSO-E key is in his environment. Rulings:
`.planning/RULINGS.md`. Lane, agents and named unknowns: `.planning/v5-EFFORT-PLAN.md`.

## Goal

Every page on the site is rebuilt in the locked "Above ground, below ground" design (`DESIGN.md`,
`site/hifi/assets/tokens.css`, reference board `R3-final`). Every dataset page is rebuilt from scratch on
one new template and states only what has been checked against gridflow code and real silver data:
a short summary, a real chart, what the data is, how it is used, and how to get it.

## Why a data-truth phase comes first (measured 2026-09-26)

- **The site is already wrong in places.** The deployed FUELHH page is a hand-authored override. It says
  the dataset covers "CCGT, coal, nuclear, wind, solar, biomass" and shows a SOLAR fuel pill and a SOLAR
  sample row. But silver has no SOLAR rows (checked for 1-5 Aug 2026), and the canonical vault corrected
  its note on 2026-08-31. The repo's vault mirror, last synced 2026-08-17, still carries the old sentence
  too. 160 mirror notes now differ byte-wise from their canonical note.
- **The vault's own checks are three months old.** The curl and silver-schema validator last ran on
  2026-06-15: 123 curl examples passed, 4 failed and 35 failed auth (ENTSO-E token). For silver schemas,
  110 passed, 37 are hand-written transformers, 14 have no schema table and 1 has no silver section.
  `machine-catalog.json` also dates from 2026-06-15.
- **Local silver covers 125 of 165 datasets:** Elexon 33/33, ENTSO-E 31/49, ENTSO-G 25/33,
  GIE 4/8, NESO 23/34, Open-Meteo 6/6 and NESO Data Portal 3/3. Without silver there is no real chart
  and no real sample.
- **Charts:** `chart-series.json` holds real series for 85 of 165 datasets. It comes from a one-off
  extract (`C:/data_to_seed_gridflow_charts`, 2026-08-16/21), not from silver. Each series plots a
  per-timestamp mean of the first sensible numeric column, which is often meaningless: FUELHH's mean
  across fuel types says nothing. 89 rendered pages still carry "seeded" placeholder charts and 139 say
  "illustrative".
- **The template route has inverted.** 130 of 165 dataset pages are hand-authored overrides in
  `authored-pages/` (ENTSO-E 41, ENTSO-G 33, NESO 33, Elexon 13, GIE 8, Open-Meteo 2). Only 35 run
  through `dataset.html.j2`. The "long tail stays template-driven" rule no longer holds.
- **Planning leakage:** 36 pages carry coming-soon or planned wording, including the 29 NESO Data Portal
  stubs that `build_dataset_stubs_from_landings` manufactures for data gridflow does not ingest.

## Decisions (ratified 2026-09-26)

- **D1. Close v4 and open v5.** v4's goal, a new identity, is met: the design is locked. Its remaining
  phases 19–21 were written for a re-skin on the old lanes (Astra/Sol, T3). This milestone rebuilds
  content as well. Close v4 the lightweight way (a short `v4/V4-CLOSE.md`; tag at v5 cutover) and
  replace ROADMAP §v4, `v4-EFFORT-PLAN.md`, STATE.md and CONTROL.md. All four are stale: STATE still says
  "Phase 17 waiting on refs".
- **D2. Dataset agents write the canonical vault, not HTML.** Page prose and a chart spec live in the
  dataset's note in quant-vault. That repo is in the gridflow zone, so this is a class 2 write on its own
  branch. It re-mirrors with `propagate-vault-mirror`, and the one new template renders every page in CI.
  All 130 `authored-pages/` overrides retire, with no showcase exception: showcase quality comes from
  the template. Writing HTML instead would entrench overrides that CI cannot reproduce from the vault.
- **D3. Real charts only.** Each dataset gets a chart spec: column, filter, grouping, aggregation, chart
  type and window. A new distil step reads C:\gridflow-data\silver directly and writes the committed
  JSON that CI builds from. A dataset with no series shows no chart. The seeded fallback is deleted.
- **D4. The site documents only what gridflow ingests.** Drop the 29 NESO Data Portal stubs and the
  other coming-soon pages. Recount the headline "165 datasets" from the audit so the number matches what
  is documented. Coverage truth lives in gridflow; building more connectors is gridflow work, outside this
  milestone.
- **D5. Near-duplicate endpoint variants become family pages (your call; I lean yes).** For example,
  about 25 of NESO's 34 datasets are the same carbon-intensity data sliced by window, region or postcode.
  One page per family, with the variants listed on it, reads better and costs less. The audit proposes
  families for every vendor and you rule on each.
- **D6. One integration branch, one cutover.** All v5 work goes to `v5/site` through per-unit PRs.
  `main` keeps serving the current site until the whole site is rebuilt, then one PR goes to main and
  deploys. Shipping page by page would leave the live site half old and half new for weeks.
- **D7. Live API check.** Phase 22 re-runs `gridflow-drift-check`, which hits live vendor APIs; per the
  repo rule it runs only on your explicit yes. For the 35 ENTSO-E checks, the key must be in your
  environment. You set that, not me.

## Phases

Numbering continues the project's global sequence (v4 was 17–21).

### Phase 22 — Data truth: provenance matrix (overnight, autonomous)

- Scripted, not agent-heavy. For each dataset it records: connector in gridflow; silver schema in code;
  silver data present (rows, first and last date); canonical vault note (last_verified, sections
  present); mirror in sync; vault silver-schema table against the gridflow schema; chart series; authored
  override; stub.
- Re-derive `machine-catalog.json`. Re-run the validator (D7).
- Ingest the missing silver (about 40 datasets) with live `gridflow ingest`, a class 2 data op with
  receipts. Datasets that cannot be ingested (auth, retired endpoints) go to D4.
- Propose the family groupings (D5) and the final page set.
- **Output:** `v5/DATA-MATRIX.md` + `.json`, the page set ruled on, and a discrepancy list per dataset.
  The discrepancy list feeds Phase 26; per-dataset facts are fixed there, not here. Systemic vault gaps
  (the 14 notes with no schema table and the missing silver section) become their own vault units.

### Phase 23 — Foundation + homepage in real HTML (overnight, autonomous; your look before merge)

- New `theme.css` on `tokens.css`, a new `site.js` chrome (masthead, nav, footer) and the strata as
  reusable full-bleed sections with SVG contact lines. The homepage is built from `R3-final`, responsive
  at 390 / 768 / 1440. The About section keeps its layout and your new copy slots in when ready.
- One mobile look with you (the canvas is desktop-only). This is not a full loop.
- **Gate:** detector `[]`, htmlhint, lychee, AA contrast, no horizontal overflow at 390, and your visual
  check.

### Phase 24 — Dataset page design loop (round 1 overnight; picks with you; the critical path)

- Round 1 (about 5 variants on a new canvas) is built overnight, so it is waiting when you wake. Then the
  same method as the homepage: you pick and mix, iterate, lock. The specimen is
  `elexon/fuelhh`. Every variant is also rendered for three awkward datasets: a price series
  (`system_prices`), a sparse daily gas flow (an ENTSO-G flow) and a table with no time axis (a
  reference or master-data set). The template must hold for all of them before 165 pages depend on it.
- It locks the **content model** with word budgets. My starting proposal for you to cut:
  - one line on what the dataset is
  - a real chart with dataset, unit and window
  - "What it is" in 60 words or fewer
  - "How it's used", as 2–3 domain uses
  - a compact fact list: grain, cadence, history, publication lag, units
  - the silver schema
  - sample rows, styled as the homepage DataFrame
  - how to get it: the `data.<source>.query(...)` workbench call plus the raw endpoint
  - up to three real caveats
  - related datasets
- **Output:** an anatomy section added to DESIGN.md. It replaces the repo CLAUDE.md "Dataset page
  anatomy" line.

### Phase 25 — Template, chart pipeline, pilot (split at the design lock)

- **25a, design-independent (overnight, autonomous).** None of this depends on how the page looks:
  - the chart spec schema (column, filter, grouping, aggregation, chart type, window)
  - the new distil step that reads C:\gridflow-data\silver and writes the committed JSON (D3)
  - build plumbing that reads page fields from the vault note
  - removing the seeded-chart fallback and the stub generator (D4)
  - one PR into `v5/site`
- **25b, after the Phase 24 lock.** The new `dataset.html.j2` and vendor partials from the locked
  design. The content-field names and budgets come from the lock. The `authored-pages/` overrides are
  removed. The two pinned agents are created (their briefs depend on the content model).
- **Pilot (in 25b):** 5 datasets go through the Phase 26 author/review loop (fuelhh plus four of different
  shapes). You read all 5. The author brief and review rubric are calibrated. The pilot also measures
  real cost per dataset before the fan-out is committed.

### Phase 26 — Dataset fan-out (agentic, vendor by vendor)

- **Per dataset:** an Opus 5.5 author agent, then an Opus 5.5 reviewer, with up to 2 fix rounds.
- **Author inputs:** the locked content model; DESIGN.md content rules; the canonical note; the
  gridflow connector and schema code; local silver (sample, range); and its matrix row.
- **Author outputs:**
  - corrected vault facts, with evidence for each change
  - the page fields, within budget
  - the chart spec
  - the page built locally, with the detector at `[]`
- **Reviewer:** objective checks only, because a same-family review is weak on taste. It checks:
  - every factual claim against code and silver
  - chart provenance
  - word budgets
  - leakage and filler
  - the build and the detector
- The verdict is APPROVE or REVISE with findings. You sample about 3 pages per vendor batch (best,
  worst, random), not all of them.
- **Order:** Elexon (33) first, then ENTSO-E, NESO, ENTSO-G, GIE, Open-Meteo, NESO Data Portal. Per
  batch: commit the vault branch, re-mirror, `gridflow-build --check`, PR into `v5/site`.
- **Run as Workflow batches.** The default workflow size is under 10 agents, so batches are 3–4 datasets
  per run, unless you raise the limit from a terminal session.

### Phase 27 — Top pages: loops, then builds (loops can run while 26 runs in the background)

- **27a. Data-sources landing + the vendor hub pattern (7 hubs).**
- **27b. Architecture** (bronze, silver, gold, the build and the gates).
- **27c. Models.** Today there is only the demand case study; the "Models" nav points at it.
  - Build a models landing covering the five models, plus per-model pages.
  - Sources: gridflow_models `notebooks/README.md`, the model cards and gold `forecast_metrics`.
  - Status truth comes from that README, never old site copy.
- Each is one design loop with you, then an Opus build. Round 1 of all three loops is built overnight,
  so the variants are waiting alongside Phase 24's.

### Phase 28 — Cutover and ship

- Site-wide sweep: detector on every page, htmlhint, lychee, AA, 390 overflow, and
  `gridflow-build --check` idempotent.
- Delete the old theme, the templates and `authored-pages/`.
- One PR from `v5/site` to main, deploy, tag, and a short close note.

**Order (OWNER 2026-09-27, "everything that can be done autonomously, done autonomously"):**
- **Overnight, with no input from you:**
  - 22 (matrix, ingest, family proposals)
  - 23 (homepage build; its PR waits for your look)
  - 25a (chart pipeline and plumbing)
  - round 1 of the 24 and 27 loops (variants waiting on canvases)
- **Morning, with you:**
  - rule families and the page set (22)
  - look at the homepage on mobile (23)
  - pick and lock the dataset page (24)
  - picks for the 27 loops
- **Then:**
  - 25b (template from the lock + the 5-dataset pilot)
  - you read the pilot
  - 26 fan-out
  - 27 builds (after 23 merges)
  - 28 needs 26 and 27

Phase 25 cannot finish overnight: its template is the Phase 24 lock, and that is your pick.

## Lane and resourcing (front-end lane, OWNER 2026-09-26: Opus executes, no Sol/Astra, no tiers)

| Role | Agent | Model · effort |
|---|---|---|
| Seat: orchestrates, merges, re-mirrors, commits per batch | this chat | Opus 5.5 · high |
| Design variants (4 loops) | `claude`, effort in prompt | Opus 5.5 · xhigh |
| Builds (23, 25, 27) | `claude` or seat | Opus 5.5 · high |
| Dataset author (new pinned agent; writes only its own vault note + chart spec) | `dataset-page-author` | Opus 5.5 · high |
| Dataset reviewer (new pinned agent; Bash inspection-only; writes only its review file) | `dataset-page-reviewer` | Opus 5.5 · high |
| Matrix scripting, ingest | seat | Opus 5.5 · high |

The two new agents are created in Phase 25 as a `~/.claude` zone unit (the author is a new
state-mutating agent). These are rough estimates; the pilot replaces them with measured cost:
- **Fan-out:** about 250–400k tokens per dataset (author, reviewer, and a fix round on about half).
  That is about 40–65M tokens for 165 pages, or 25–40M if D5 folds the variants into families.
- **Four design loops:** about 6–12M, judging by the homepage loop.
- **Builds and audit:** about 3–5M.
- This would be the largest agent spend the project has run.

## Loose ends (listed, not solved)

- PR #34 (cross-link the gridflow-explorer app) has been open since 2026-08-15: merge or close
  before cutover.
- Branches `feat/v4-identity` and `chore/v4-planning-wip` (the August DESIGN drafts) are superseded.
- The design-loop record in `.planning/v4/` is uncommitted (docs-only, so it can go to main).
