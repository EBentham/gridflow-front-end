# v5 cutover: swap the live site to the new pages (plan, 2026-09-27 late, awaiting Bobbo's yes)

Ask (OWNER): "swap over the site to the new html pages, and the five datasets we have done. Remaining
datasets can just be a blank page for now. We will batch them tomorrow."

This compresses Phase 27's builds and Phase 28's ship into one run tonight. Phase 26 (the dataset fan-out)
follows tomorrow and fills the blank pages.

## What goes live

| Page | Source of truth | Work |
|---|---|---|
| Home | built (#41) | fix the turbine through the "gas-fired power station" label; phone fixes (nav wrap at 360, chart text size, code block scroll, the "Each cable below" copy); Models and Explorer links |
| Architecture | locked boards `arch-r2/` | build as one responsive page |
| Models | locked boards `models-r2/` | build as one responsive page; retire `models/demand-forecast.html` (#21: high level) |
| Explorer | locked boards `explorer-r1/2/` with wording B | build as one responsive page; real screenshots as site assets |
| Data sources + 7 vendor hubs | direction A "Sections" (p27 round 1) | render from the build with the new look |
| 5 pilot dataset pages | PR #42 | switch the silver section to locked 3a |
| every other dataset page | the build | "blank": petrol hero with the dataset's name and id, breadcrumb, nothing else (no "coming soon" wording: planning-leakage rule) |
| old theme, old templates, `authored-pages/` | | deleted (Phase 28) |

## Units, agents, cost

Front-end lane (OWNER 2026-09-26): Opus executes, no Sol/Astra, no tiers, no plan or diff review; the
deterministic gates run; Bobbo validates visually. All agents run on Opus 5.5 at high effort.

| Unit | Agent | Branch | Est. |
|---|---|---|---|
| U1: dataset template to 3a; blank pages for the rest; hubs in direction A; delete the old templates and overrides | the pilot agent (resumed; owns `build.py` and the templates) | `v5/p25b-template` (PR #42) | $30-45 |
| U2: Architecture page | new builder | `v5/p27-architecture` off `v5/site` | $20-30 |
| U3: Models page | new builder | `v5/p27-models` off `v5/site` | $10-15 |
| U4: Explorer page, plus the shared chrome and home fixes (the only unit that edits `site.js` and `index.html`) | new builder | `v5/p27-explorer` off `v5/site` | $15-25 |
| U5: whole-site QA at 1280, 1440, 1920 and 390, light and dark: clipping, overlap, sizing when opened directly | new reviewer (inspection-only Bash) | none (writes one report) | $10-15 |
| Seat | this chat | merges into `v5/site`, clean-checkout gates, preview, cutover PR | context only |

- **Total:** about $85-130.
- **Usage:** weekly was 92% at 22:05. The ten agents run since 20:10 used about 8%. This plan may take
  most of what is left.
- **If the cap lands mid-run:** every unit commits as it goes, and the seat resumes it after the 09:00 reset.
- **Order:** U1 to U4 run in parallel in their own worktrees. U5 runs on the merged `v5/site`.

### Conflict rules

- Each top-page builder puts its page CSS in its own file, `assets/<page>.css`. `theme.css` only
  changes for shared fixes, and only U4 makes those.
- Only U4 edits `site.js` (the nav gains Explorer; Models goes to `models.html`) and `index.html`.
- U1 already dropped the licence line from `site.js`. The seat resolves that one-line overlap at merge.
- Drawings follow the standing checks: give the viewBox top room, keep objects uncropped at every width,
  and let nothing clip.

## Gates (every unit, then the merged `v5/site` from a clean checkout)

- `uv run --system-certs --extra build gridflow-build --check`
- tests
- htmlhint
- lychee `--offline`, as CI runs it
- `detect.mjs` returns `[]`
- AA contrast
- no page scroll at 390
- U5's report shows no clipping or overlap

Never run `gridflow-drift-check`.

## Merge path

1. U1 to U4 each open a PR into `v5/site`. The seat merges on green gates plus Bobbo's look at the
   integrated preview. `v5/site` is not `main`.
2. The seat opens the cutover PR from `v5/site` into `main`. **Bobbo merges it**, and CI renders and
   deploys to GitHub Pages.
3. The seat checks the live site: the nav, five pilot pages, a blank page and the hubs.
4. The seat tags the cutover and writes a short close note.

## Defaults the seat takes (PROXY-SOURCED; Bobbo confirms at close)

- Explorer in the top nav on every page.
- The explorer screenshots keep the app's own "held locally" text: it is the real interface; the rule
  targets site prose.
- The explorer link goes to the public repo root.
- Close PR #34 (explorer cross-link) as superseded by the Explorer page.

## Asked of Bobbo

1. **Hubs:** build the Data sources landing and vendor hubs from direction A as it stands (recommended),
   or keep the current hub layouts for tonight?
2. **Blank pages:** the name and id in the hero and nothing else (recommended)?
