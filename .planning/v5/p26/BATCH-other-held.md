# Held pages, other vendors (ruling 66): nine pages

Opened 2026-10-24 after the NESO held-rows pass, on the parent's relay of Bobbo's words: the site is a data catalogue,
so held pages show their rows with one plain caveat (16 words or fewer). Facts per page come from gridflow's fixes,
relayed by the parent and recorded in `.planning\neso-dp\BATCH-held-rows.md` (the ENTSOG, GIE, NETBSAD/NONBM and
ENTSO-E paragraphs). Verify every one against local silver before writing it.

- **Agents:** one writer (Opus 5.5 · high) and one checker (Sonnet 5.5 · high) per page; revisions go back to the
  same agents. The seat keeps at most 5 agents running at once, counting the NESO pass.
- **Ship rule:** nothing merges until Bobbo looks. One site PR off `main` and one vault PR off `master`.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-other-held`, branch `feat/other-vendor-held`, off `main` plus the parked
  held notes and artefacts (ENTSO-E, GIE, ENTSOG capacity) and a merge of `feat/neso-dp-template-pass` (PR #60, which
  carries the `caveat:` field, the held-page mode and `raw_feed.sample`; the PR says so until #60 merges). The `.venv`
  is synced with the `build` and `distil` extras.
- **Vault worktree:** `C:\gridflow-wt\vault-other-held`, branch `docs/other-vendor-held`, off quant-vault
  `origin/master` plus the parked held notes (ENTSO-E, GIE, ENTSOG capacity). Notes are
  `30-vendors/<vendor>/datasets/<dataset>.md`, CRLF: edit with the Edit tool. Mirror byte for byte to
  `vault/<vendor>/<dataset>.md` in the front-end worktree and `cmp` (the parked mirrors differ from the notes only in
  line endings; copying fixes that).
- **Elexon parked work:** `netbsad` and `nonbm` notes on vault branch `docs/v5-p26-elexon-held` and site branch
  `v5/p26-elexon-held` (both old and diverged: read them with `git show <branch>:<path>`, never merge them).
- **ENTSOG parked work:** the cmp notes on vault `docs/v5-p26-entsog-gas-held` (same rule).
- **Earlier author reports** for these pages: `.planning\v5\p26\{entsoe,entsog,gie,elexon}\<page>-author*.md` and
  `-review*.md`. They describe the old defects; the fixes below supersede them.
- **gridflow code with the fixes is unmerged.** Read it from the PR branches in the gridflow repo
  `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow` with `git show origin/<branch>:<path>`:
  ENTSO-E `fix/entsoe-balancing-paging` (#130), `fix/entsoe-pt1m-steps` (#131), `fix/entsoe-balancing-silver` (#132);
  ENTSOG `fix/entsog-capacity-cmp` (#129); GIE `fix/gie-unavailability` (#133); Elexon
  `claude/fix-netbsad-nonbm-53c117` (#128). Local silver `C:\gridflow-data\silver\<vendor>\<dataset>\` is already
  rebuilt from them. Read only, Polars, lazy.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v5\p26\other-held\<page>-author.md`
  and `<page>-review.md` (then `-2`, `-3`).
- **Rules:** `.planning\v5\author-brief.md` IN THE FRONT-END WORKTREE (includes "Family pages" and "Caveats and held
  pages (ruling 66)"), `.planning\v5\review-rubric.md`, `DESIGN.md` "Dataset page anatomy",
  `.planning\v5\p26\agent-prompts.md`, and the "Both" section of `.planning\neso-dp\AGENT-PROMPTS.md` (server PID rule,
  scratch subfolders, no turn ending mid-task).
- **Worked examples:** the live ENTSO-E, GIE and Elexon pages on `main` (`vault/<vendor>/`,
  `site/hifi/data-sources/<vendor>/`); the NESO caveat pages approved in `.planning\neso-dp\held-rows\` (`D2-*`,
  `T1-*`, `C1-*`).

## Rules for every page

- Every table with silver rows gets the full anatomy plus at most one caveat; a caveat states vendor facts only
  (gridflow's own gaps go in the note's holds or body).
- Remove every body line that says no values or rows are published or shown, and every line describing a defect the
  fix removed.
- Never print a recomputed value beside the vendor's column. Never sum across units.
- Say "no time zone", not "no clock". Units and time stamps from code or the vendor, never memory.
- Charts and samples only from days the fixed silver covers; say the window in the caption.
- No local-data references, no planning words, no em dashes, no bare codes, British spelling.
- Build `--only <vendor>/<lead>`, no errors, detector `[]` (accepted advisory: the EIC dash count) at
  `C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json`.
- The manifests are the seat's: report a wrong lead or member list, never edit it. No git writes.

## The nine pages

| Page | Vendor | Members (lead first) | Writer port | Checker port |
|---|---|---|---|---|
| `current_balancing_state` | ENTSO-E | single | 9841 | 9845 |
| `procured_balancing_capacity` | ENTSO-E | single | 9842 | 9846 |
| `balancing-energy-bids` | ENTSO-E | `balancing_energy_bids`, `aggregated_balancing_energy_bids` | 9843 | 9847 |
| `outages` | ENTSO-E | `outages_generation`, `_production`, `_consumption`, `_transmission`, `_offshore_grid` | 9844 | 9848 |
| `capacity-by-indicator` | ENTSOG | `firm_available` lead + nine more | 9851 | 9855 |
| `cmp` | ENTSOG | `cmp_auction_premiums`, `cmp_unavailable_firm_capacity`, `cmp_unsuccessful_requests` | 9852 | 9856 |
| `unavailability` | GIE | single | 9853 | 9857 |
| `netbsad` | Elexon | single | 9861 | 9865 |
| `nonbm` | Elexon | single | 9862 | 9866 |

## Tracker

| Page | Writer | Checker | State |
|---|---|---|---|
| `current_balancing_state` | a4cb0fff7df521d95 | | writing |
| `unavailability` (GIE) | aca4443f38f5d0077 | | writing |
