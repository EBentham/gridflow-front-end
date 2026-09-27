# Pickup: evening of 2026-09-27 (before compaction)

Seat: Opus 5.5 at high, this same chat. Keep it thin: read this file, then the decision files it names.
Chat-only rules from Bobbo: plain English, one decision at a time, show options side by side in the picker
https://claude.ai/artifact/MpySKZLbpbe6VmCz4pcuzV (source `<scratch>\compare\index.html`, static boards in
`<scratch>\compare\boards\`, made with `<scratch>\compare\strip.py <out> <board.dc.html>...`, which prints heights;
add a `MODES.<key>` entry, set `let mode=`, republish with the new board files). `<scratch>` =
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad`.

## Locked today (all recorded in RULINGS #18-24 and the decision files)

- Dataset page: `DESIGN.md` "Dataset page anatomy"; `.planning/v5/design-loop/p24-decisions.md`.
- Architecture: `arch-decisions.md`, boards `arch-r2/` (pandas notebook read in stop 7; scope line "runs under"
  an orchestrator because `gridflow build` exits 0 on failure, gridflow BACKLOG 11).
- Models: `models-decisions.md`, boards `models-r2/` (converging cables; high level, RULINGS #21; status from
  code and manifest, #22; "still in development" line).
- Data sources and Elexon vendor hub: direction A (`p27-decisions.md`). Homepage approved earlier (#17).
- Site-wide: no licence line anywhere (#23); removed from `site.js` on the pilot branch and from the boards.
- Build note: drawings need top room in the viewBox (distant turbines were clipped; boards use overflow:visible).

## Running when compacted

- **Dataset template + five-page pilot** (background Opus agent, worktree
  `.claude/worktrees/agent-a3e553d579e4d88f0`, branch to be `v5/p25b-template` off origin/v5/site). Pages:
  fuelhh, system_prices, entsog physical_flows, bmunits_reference, demand-outturn family (indo/itsdo/indod).
  system_prices APPROVED; demand family REVISE (INDOD MWh unit only project-checked; "within rounding"); two
  reviews pending. Commits so far include `3d2077b` (licence line out of site.js). It will open a front-end PR
  into v5/site and a vault PR (vault worktree `<scratch>\vault-p25b`, branch `docs/v5-p25b-pilot`), both left OPEN.
  When it reports: read its final message and `.planning/v5/P25B-REPORT-notes.md` on the branch only; then SHOW
  Bobbo the five built pages (browser pane from the worktree's site on a local port, plus a published private
  artifact of the pages with their assets so he can open them on PC or phone), with the questions it raised:
  imbalance-volume sign conflict in the vault domain note; INDOD unit; SBP=SSP scoped to the window; author cost
  about $7-7.70 per dataset. Then confirm or adjust the fan-out plan (per dataset author + Opus reviewer,
  vendor batches, one PR per batch; about 73 pages, roughly $500-700) before launching after the weekly reset.

## Next: the gridflow explorer top page (spec it now, with Bobbo)

- Bobbo's ask: a new top-level page telling readers about gridflow explorer. Purpose: "just show the work I have
  done". Not very detailed: a brief section on the underlying technologies (he wants recruiters to see he is a
  full-stack developer who builds front ends with React), and a screen demo of what the explorer looks like,
  "similar to the view of the notebook we had earlier on the home page" (the homepage notebook showcase: a
  faithful, real-content rendering of the app's UI rather than a screenshot).
- First: read the explorer milestone to understand what it is and its objectives. Repo:
  `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow_explorer`, `.planning/` has `ROADMAP.md`, `STATE.md`,
  `RULINGS.md`, `HANDOFF-2026-09-26-explorer-milestone.md`, `P4-forecast-screen-SPEC.md`, `milestones/`,
  `phases/`. Read via one Explore/claude agent that distils into a short file (stack, screens, objectives, what
  is built vs designed), not the whole tree in the seat. Also note open PR #34 (cross-link the explorer app).
- Then brainstorm with Bobbo (a few directions, recommendation first), record in
  `.planning/v5/design-loop/explorer-decisions.md`, then a small design round (one or three Opus designers) into
  the picker. Rules: DESIGN.md (no planning leakage about unbuilt explorer features; describe what exists), no
  licence line, real content only.

## Budget

At 20:10 local the weekly window was about 81-85% (resets 2026-09-28 09:00 local); the 5-hour window reset at 20:40.
