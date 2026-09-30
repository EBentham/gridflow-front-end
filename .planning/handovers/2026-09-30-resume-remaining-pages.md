# Resume here: the remaining dataset pages (written 2026-09-30, end of the 29 Sep session)

Bobbo is away from the desktop for a few days, and work resumes when he's home. **Read this first**, then `agent-prompts.md`
(`.planning/v5/p26/`). Then read the newest RULINGS (#36 to #48) with `python ~/.claude/tools/rulings.py .`.

## Where things stand

- **Live on the site** (each batch: a writer and a checker per page, Opus 5.5 · high; gates green; checked live):
  - **Elexon:** PR #54 (cccf643), 23 of 25 pages.
  - **ENTSO-E:** PR #55 (d284745), 20 of 24 pages.
  - **GIE:** PR #56 (7deb94f), 3 of 4 pages. Bobbo reviewed these on a local build before they went live.
- **Vault:** quant-vault PRs #53 to #57 are merged, so the canonical notes match the mirror for everything that's live.
- **Held blank (7 pages)** wait on gridflow fixes. Their note corrections are parked on held branches, not lost:

  | Page | Ruling | Front-end branch | Vault branch |
  |---|---|---|---|
  | elexon netbsad, nonbm | #37 and before | `v5/p26-elexon-held` | `docs/v5-p26-elexon-held` |
  | entsoe current_balancing_state, procured_balancing_capacity, balancing-energy-bids, outages | #41, #42, #44, #46 | `v5/p26-entsoe-held` | `docs/v5-p26-entsoe-held` |
  | gie unavailability | #43 | `v5/p26-gie-held` | `docs/v5-p26-gie-held` |

- **gridflow fix list:**
  - The vault page `10-projects/gridflow/specs/remediation-from-site-batches.md` (on master) is the tracked copy. It holds item 12 (Elexon 12a to 12i), item 13 (ENTSO-E 13a to 13an) and item 14 (GIE 14a to 14o).
  - A local-only copy sits in gridflow `.planning/BACKLOG.md`, which is gitignored.
  - New defects go to both. The vault branch `docs/gridflow-issues-2026-09-29` is merged, so start a fresh vault docs branch.
- **Next gridflow milestone** (Bobbo): complete the NESO Data Portal connector (BACKLOG item 9). The remediation milestone comes after it, and the held pages go live once their fixes land.

## What's left: 19 pages, in this order

1. **Open-Meteo (3 families):**
   - demand-weather [historical_demand, forecast_demand];
   - wind-weather [historical_wind, forecast_wind];
   - solar-weather [historical_solar, forecast_solar].

   The history runs back to 2021 and the forecasts cover 1 Aug to 22 Sep. This is the cleanest data held.
2. **NESO Data Portal (3 single pages):**
   - historic_generation_mix (930k rows, 2009 to 2026);
   - embedded_wind_solar_forecast (628 rows, 20 Aug to 2 Sep);
   - daily_wind_availability (3,589 rows, 22 Aug to 3 Sep).

   The other 29 packages get pages after the NESO connector milestone.
3. **NESO carbon intensity (5 pages):**
   - national-carbon-intensity (9 members);
   - intensity-statistics;
   - intensity_factors;
   - regional-carbon-intensity (18 members);
   - generation-mix.

   Many members are one-day snapshots or 1 to 2 day forecast windows, so expect "thin but accurate" wording.
4. **ENTSOG (8 pages; physical_flows is already live from the pilot):**
   - nominations-allocations, capacity-by-indicator (10 members), gas-quality, aggregated_physical_flows, cmp, tariffs-and-simulations, reference-data (6 registers) and urgent_market_messages.
   - Risks: the CMP and "available through" tables cover only 31 Jul to 4 Aug, `interruptions` has 0 rows, and several tables are registers with no time axis. Expect one or two holds.

The families and members come from `site/hifi/data/<vendor>.json`. Row counts and windows are in `.planning/v5/DATA-MATRIX.md`.

**Cost:** ENTSO-E took about 11.6M subagent tokens for 24 pages (44 agents), and GIE about 1.9M for 4. Expect 9 to 12M for these 19, about 10 to 12% of a week. Weekly usage was 74% on 30 Sep, and it resets on 5 Oct at 08:00 UTC.

**Open decisions for Bobbo:**
1. Start when he's home, or at a 5-hour reset?
2. Which sources does he review before they go live: all of them, or only ENTSOG (the recommendation)?

## How to run a batch (the process that worked)

1. **Set up worktrees.** Paths are under the new session's scratchpad; the old scratchpad worktrees belong to the ended session.
   - `git -c core.longpaths=true worktree add <scratch>/p26-<vendor> -b v5/p26-<vendor> origin/main`. The front end needs `core.longpaths`, or checkout fails on long `.planning` paths.
   - In quant-vault: `git worktree add <scratch>/vault-p26-<vendor> -b docs/v5-p26-<vendor> origin/master`.
   - In the front-end worktree: `uv sync --system-certs --extra build --extra distil`.
2. **Write the brief.** Copy `.planning/v5/p26/BATCH-gie.md` to `BATCH-<vendor>.md`: paths, pages and ports, known defects to check, shared-worktree rules, carried rulings. Also create a tracker, `.planning/handovers/<date>-<vendor>-batch.md`.
3. **Run writers and checkers.**
   - Use the templates in `agent-prompts.md`: `claude` subagents, `model: opus`, "Effort: high" in the prompt, run in the background.
   - Run up to 10 agents at once, and launch nothing new past about 92% of the 5-hour window (check with `get_usage`).
   - Revisions and re-checks go back to the SAME agents via SendMessage. Fix nits even after an APPROVE; the seat may apply one-word fixes the checker prescribes.
4. **Log defects as they are found.** Every gridflow or data defect goes to the vault remediation page and gridflow BACKLOG, as item 15 onward.
   - Use `.planning/v5/p26/tools/logdefects.py`.
   - A hold gets a RULINGS line (class 3, PROXY-SOURCED) with the reason in plain words.
5. **Review, if Bobbo wants to.** Full-build the worktree and serve its `site/hifi` with a `.claude/launch.json` http.server entry (like `gie-review`, port 9670). Give him the localhost link, not a zip. localhost works only at the desk, and the server dies with the session.
6. **Ship.**
   1. Park the held notes: copy the canonical notes and mirrors aside, and restore them on the ship branches. In the front end that means `git checkout origin/main -- vault/<v>/<ds>.md`, then `git reset`. Then commit them on `v5/p26-<vendor>-held` and `docs/v5-p26-<vendor>-held`, each from its own worktree.
   2. Run the gates (below) in the worktree.
   3. Commit one concern per commit: code fixes first, then `feat(<vendor>): N dataset pages`.
   4. Push and run `gh pr create`. **Wait for the PR check `docs-integrity` to go green** (`gh pr checks <n> --watch`), then squash-merge. On 29 Sep, #55 was merged early (process miss).
   5. Watch main CI and "Deploy to GitHub Pages", then check the live pages: HTTP 200, plus `<svg class="chart` on pages that have a chart.
   6. Commit the vault notes on `docs/v5-p26-<vendor>` and open a vault PR (merge only on Bobbo's word).
   7. Write a RULINGS ship line with the spend (sum of the agents' reported subagent tokens).

## Gates (all must pass before a PR)

- `uv run --system-certs --extra build gridflow-build` (full) and `... gridflow-build --check` (idempotent).
- `uv run --extra build pytest -x -q`. The blank-page test uses `entsoe/current_balancing_state`, which stays blank while held.
- `npx -y htmlhint "site/hifi/**/*.html"` and `lychee --offline --no-progress site/hifi`.
- The detector, by absolute path (worktrees have no `.claude`): `node C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json <page>`.
  - The gate is no non-advisory findings.
  - `em-dash-overuse` is accepted ONLY when EIC `--` padding triggers it.
  - Real em dashes in pages must number 0: `grep -c "—"`.
- `uvx --system-certs ruff check <changed files>` and `ruff format --check <changed files>`. Never run `ruff format src/`, which rewrites unrelated files. The ISC004 at `build.py:1197` predates this work.

## Rulings to carry (content)

- No literal `---` anywhere in a note's front matter (#40). Write EIC dashes as `\x2D` escapes in double-quoted YAML.
- Say what a stamp is, from the code. ENTSO-E `published_at` is the fetch time, not an issue time.
- A point's time is `period start + (position - 1) × resolution`. State cadence "as sent in the responses we hold", never as a vendor rule, and scope observations the same way.
- **Ship with the loss stated** when the chart and sample rows avoid the defect and the page says plainly what silver loses. Examples: commercial_schedules (A07 only), load forecasts (one of max/min), actual_generation_units, forecast_margin (DE-LU left out). **Hold** when silver misleads overall: repeated rows, arbitrary picks, wrong stamps, a lost sign on the main value. Thin but accurate ships (water_reservoirs: FR only, 4 weekly points).
- Units come from code or the vendor, never memory. GIE stock columns are TWh "by our check" (an ENTSOG cross-check), despite `_gwh`.
- No planning words on the site: "yet", "soon", "planned", "coming", "not yet". "Placeholder" is fine as a domain term. No local-data references. Plain English, no bare codes.
- Related links to held pages are allowed (system_prices links to netbsad).

## Gotchas hit this session

- **The guard hook:**
  - It halts on the literal text "rm -rf" anywhere, heredocs included; write files with the Write tool.
  - It blocks deleting a variable path, `git push --force`, and `git -C "$VAR"`; use literal paths.
  - It reads a whole compound command, so split commits across repos into separate calls.
- **Chrome:** wrap every headless Chrome call in `timeout 60` with `--timeout=15000 --virtual-time-budget=5000`. A true 390 check needs a 390 px iframe.
- **Warehouse views:** the warehouse (`C:\gridflow-data\gridflow.duckdb`) can lack views for new silver. Snapshot it first, then run gridflow's `runner.refresh_views(load_settings())`; views only, a class-2 data op, with a RULINGS receipt (#45).
- **Notebooks:** they run with the gridflow_models interpreter via `scripts/run_notebooks.py --dataset <v>/<ds>`.
  - Named-index tables now render aligned (fix 432a2f8).
  - The runner would crash on a Polars frame display (out of scope, unfixed).
- **Vault notes** use CRLF. Edit them with the Edit tool and mirror with `cp`, then check with `cmp`. Never `git stash` in a worktree agents are writing in.
- **Artefacts:** `site/hifi/data/{series,samples,notebooks}/<vendor>/` is committed; the generated HTML is gitignored.

## If the work must run away from the desktop (researched 29 Sep, not set up)

- **Why plain cloud sessions don't fit:**
  - A cloud session attaches ONE GitHub repo, and unattached private repos return 403.
  - `~/.claude` (global rules, agents, hooks, tools, memory) doesn't load there.
  - The data lives only in `C:\gridflow-data`. The four remaining sources need about 156 MB of silver and 487 MB of bronze.
- **Options discussed:**
  - (a) One private "workspace" repo holding the site, gridflow, gridflow-models, the vault notes and that data, with a setup script. Going live waits for the desk, or for a GitHub Action with a token Bobbo creates.
  - (b) A small always-on VM mirroring the desktop, driven by Remote Control.
  - (c) Pause the pages and use the cloud for code-only gridflow work.

  Bobbo chose to wait until he's home.
