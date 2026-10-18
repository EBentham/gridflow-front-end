# NESO Data Portal: the remaining 124 package pages (overnight run)

Approved by Bobbo 2026-10-18 ("Looks good. Approved", ruling 62). Start from a FRESH session: read this file, then
`BATCH-dfs.md` (paths, rules, worked facts), `handovers/2026-10-16-neso-dp-handoff.md` (rulings 1-8) and RULINGS 57-62.

## Where things stand

- Live on main: the plot-plan hub (all 131 packages, 16 groups) and 7 package pages: the 4 showcases
  (`demand-flexibility`, `eac-br-auction-results`, `aggregated-bsad`, `constraint-breakdown`, PR #59, b3963da)
  and the 3 older single-table pages. Canonical notes merged: quant-vault PR #63 (be22305).
- The build reads one note per package: manifest `families[].note` (multi-table) or `package_tables` (single table);
  artefacts and `--only` keys use the lead table key. Adding a package = mirror its note byte for byte + one
  manifest entry; the hub links a package as soon as it is in the page set.
- Package data per group (title, slug, NESO description, pub or held, held reason):
  `.planning/neso-dp/neso-packages.json` (snapshot of 2026-10-18).
  The ledger is the source: `..\gridflow\.planning\v0.22-FE-LEDGER.md`.

## Step 1: template pass (one Opus 5.5 · high agent, its own branch and PR)

Fix the four limits the showcase batch hit, before any page work:
1. A chart can plot only one column of a wide table: allow several columns of one row as series (constraint
   breakdown's four reasons is the test case).
2. No y-axis floor setting: five small negatives pushed constraint breakdown's axis to -20M; the 2020-21 gap on
   Aggregated BSAD sits on the axis line.
3. Related links can't name a hyphenated package page slug.
4. `notebook.needs` is slotted before a fixed "ingested": either make the template sentence robust or validate the
   field so a clause can't be written there (two writers fell into it).
Also: on spans over 400 days the x axis labels only 1 January; at 390 px long command lines clip. Every other page
must stay byte-identical unless a fix deliberately changes it (report each difference).

## Step 2: pages, one data group per branch and PR, balancing groups first

| Order | Group | Full pages | Held pages |
|---|---|---|---|
| 1 | Ancillary services | 21 | 8 |
| 2 | Balancing costs | 1 | 7 |
| 3 | Constraint management | 2 | 6 |
| 4 | System | 7 | 3 |
| 5 | Demand Flexibility Service | 3 | 0 |
| 6 | Trading | 1 | 6 |
| 7 | Demand | 6 | 7 |
| 8 | Generation | 5 | 5 |
| 9 | Interconnectors | 0 | 7 |
| 10 | Connection registers | 3 | 0 |
| 11 | Network charges | 1 | 2 |
| 12 | Electricity Market Reform | 1 | 0 |
| 13 | Carbon intensity | 0 | 4 |
| 14 | FES: Pathways to Net Zero | 5 | 11 |
| 15 | Strategic Energy Planning | 1 | 0 |
| 16 | Data Portal changes and known issues | 1 | 0 |
| | **Total** | **58** | **66** |

Large groups (Ancillary services) may split into two PRs.

**Staffing (approved):**
- Full page: one writer (`claude`, model opus, prompt starts "Effort: high") + one checker (`claude`, model sonnet,
  "Effort: high"). Revisions and re-checks go back to the same two agents. Prompts: `.planning/v5/p26/agent-prompts.md`,
  as adapted in this session's showcase prompts (see the four author reports for what they covered).
- Held pages: one Opus · high writer per batch of about 5 held packages in the same group + one Sonnet · high checker
  per batch. Held page = full anatomy minus rows (ruling 6): what it is + facts table, raw feed with its files, the
  tables listed with one plain line on why rows are not shown; no chart, sample or notebook.
- Seat (the fresh session): briefs, rules on findings, commits, opens PRs, logs defects. Never writes pages itself.

**Pace and limits:** 2 to 3 agents at once, rolling, overnight. Read `get_usage` before every launch; at 98% weekly
(all models) park until the reset. Measured on the showcase batch: a full page costs about 1% of the weekly
allowance; a held batch of 5 about 1.5%; the whole run about 80% of one week, roughly 10 nights at 6 to 8 full pages
a night. The seat rotates at a group boundary when its own context passes 250k.

**Gates per PR:** `pytest -q`, `gridflow-build --check`, `htmlhint --config .htmlhintrc 'site/hifi/**/*.html'`,
`lychee --offline --include-fragments './site/hifi/**/*.html'`, impeccable `detect.mjs` on every new page
(`.claude/skills/impeccable/scripts/detect.mjs --json <page>`). Merge only after Bobbo looks at the group's pages in
the morning (serve the worktree's `site/hifi`, open the pages in his Chrome).

**Defects:** every gridflow or data defect a writer or checker finds goes, as found, into gridflow
`.planning/BACKLOG.md` (item 19/20 area) and the vault page `10-projects/gridflow/specs/remediation-from-site-batches.md`
(next free 20x row), committed on the vault batch branch.

**Done:** all 131 packages have pages, PRs merged, deploy green; send the control-room overseer
(`local_cfeb0e27-0adb-45b6-ad22-0f051dfdc714`) the deploy record (Pages run id, deployed SHA, live URL, date, gate exits).
