# Resume the v5 cutover (written 2026-09-28 about 00:30, in case usage runs out)

Plan: `.planning/v5/CUTOVER-PLAN.md`. Rulings #30 (blank dataset pages) and #31 (cutover approved, hubs
in "Sections"). Phase 1 runs four builders in parallel; phase 2 integrates, then QA, then the preview;
phase 3 is the cutover PR (Bobbo merges to main).

## Where each unit stood

| Unit | Branch / PR | State |
|---|---|---|
| U1: dataset template, 3a schema, blank pages, hubs, retire old templates | `v5/p25b-template`, PR #42, worktree `.claude/worktrees/agent-a3e553d579e4d88f0` (agent `a3e553d579e4d88f0`) | 3a and brief commits landed; screenshots nearly done; hub and drawing fixes pending |
| U2: Architecture | PR #44 (`v5/p27-architecture`) | DONE, gates green. Watch: index text about 12 px at 1280 |
| U3: Models | PR #43 (`v5/p27-models`) | DONE, gates green. The licence line in `site.js` goes when #42 merges |
| U4: Explorer + nav + home fixes | `v5/p27-explorer`, worktree `agent-a25e07ca9e214e65e` | running (had a headless Chrome port issue) |

## To resume

1. `git fetch`. Run `gh pr list --base v5/site` to see which PRs exist; check each unit's branch head.
2. Any unit without a PR: resume its agent with SendMessage (the ids above) and ask it to finish, gate,
   push and open its PR. If an agent is gone, launch a fresh Opus builder on the same branch with
   `.planning/v5/p27-build/BRIEF.md`.
3. When all four are in, merge into `v5/site` in this order: #42, #43, #44, then Explorer. The seat
   resolves the `site.js` overlap: licence line out, nav gains Explorer, Models goes to `models.html`.
4. Run the clean-checkout gates on `v5/site`:
   - `gridflow-build --check`
   - tests
   - htmlhint
   - lychee `--offline`
   - detect
   - no 390 overflow
5. U5 QA: an inspection-only Opus reviewer screenshots the whole site at 1280, 1440, 1920 and 390, light
   and dark (clipping, overlap, sizing). Route its findings back to the owning unit.
6. Refresh the site preview artifact https://claude.ai/artifact/JBjXGxskWvkQYeFtjAn4R7 from the merged
   `v5/site` build. Show Bobbo.
7. On Bobbo's look, open the cutover PR from `v5/site` into `main`. **Bobbo merges.** Then check the live
   site, tag, and write a close note.
8. Then Phase 26 (the dataset fan-out by vendor batch) fills the blank pages. Also: close PR #34 as
   superseded (PROXY default), and the NESO Data Portal packages are gridflow work (#16).
