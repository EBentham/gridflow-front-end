# Resume the v5 cutover (updated 2026-09-28 about 02:45; the weekly limit hit 99%, resets 09:00)

Plan: `.planning/v5/CUTOVER-PLAN.md`. Rulings #30 (blank dataset pages) and #31 (cutover approved, hubs
in "Sections").

## Done

- **Phase 1:** all four units are done, each with an open PR into `v5/site`:
  - #42 dataset template (3a schema, 68 blank pages plus 5 pilots, landing and 7 hubs, old templates retired);
  - #43 Models;
  - #44 Architecture;
  - #45 Explorer, plus the nav (Explorer; Models goes to `models.html`), the homepage fixes, and
    `models/demand-forecast.html` retired.
- **Integration branch `v5/cutover-integration`** (pushed; local worktree at
  `<scratch>\integ`) merges all four onto `origin/v5/site`. The one conflict (demand-forecast deleted) is
  resolved.
- **Gates green on it:**
  - build `--check` idempotent (73 pages + 7 hubs);
  - 68 tests;
  - htmlhint on 184 files;
  - lychee `--offline` with 0 errors;
  - detect `[]` on 184 files.
- The site preview artifact https://claude.ai/artifact/JBjXGxskWvkQYeFtjAn4R7 shows this integrated build
  (version 4). A local server is on :9661 (launch config `cutover-site`).
- **QA report:** `.planning/v5/QA-CUTOVER.md`, with 1 blocker, 3 majors and 10 minors.

## Next (after the 09:00 reset)

1. **One Opus fixer on `v5/cutover-integration`** (the worktree above), fixing from `QA-CUTOVER.md`:
   - **B1 (blocker):** the home phone rule in `theme.css` (`@media (max-width:699.98px) .landscape svg`
     `aspect-ratio` and `margin-left`) breaks the `.ds-land` / `.hub-land` hero drawings at phone width.
     Scope the rule to the home figure.
   - **M1:** the Data sources chart axis text is 9-10 px.
   - **M2:** counts disagree: home says 165 datasets and 7 vendors, the build says 149, and the Explorer
     page says "eight sources".
     - Home's numbers must come from the build or match it (#14).
     - Check the per-vendor cadence claims against the code.
     - Home's silver/gold example names must be real relation names.
   - **M3:** Architecture legend and labels are 10-12 px at 1280.
   - **Minors m1-m7, m9, m10:**
     - blank pages should also drop the site footer;
     - the explorer crop cuts through a text line;
     - the physical_flows x-axis;
     - the frames that overflow instead of folding into `…` (a 3a spec violation);
     - code boxes need a scroll cue or wrapping;
     - the orphaned "it" in the Data sources headline;
     - the ITP label break;
     - the BM units axis title.
     m8 (12 px mono) is optional.
   Commit per fix, then re-run all gates.
2. **Quick re-QA** of the pages the fixes touched (same method, 390 and 1280 at least).
3. **Republish the preview:** use the artifact `url` above with `file_path` =
   `<scratch>\integ\site\hifi\index.html` and root at that folder. **Show Bobbo.**
4. **On Bobbo's OK:** merge `v5/cutover-integration` into `v5/site`; PRs #42-#45 then show as merged, so
   comment on each. Open the cutover PR from `v5/site` into `main`. **Bobbo merges.** Then check the live
   site, tag, write a close note, and close PR #34 as superseded (PROXY default).
5. **Then Phase 26:** the dataset fan-out fills the blank pages (author and reviewer per dataset, vendor
   batches; the brief and rubric are on #42 at `.planning/v5/author-brief.md` and `review-rubric.md`,
   already updated to 3a).
