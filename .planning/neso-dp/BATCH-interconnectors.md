# NESO Data Portal pages: Interconnectors

Opened 2026-10-24 under the approved plan (ruling 62) and the resume (ruling 65). 7 held pages, no full pages, one branch
and one PR stacked on Generation. Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-ic`, branch `feat/neso-dp-interconnectors`, cut from
  `feat/neso-dp-generation`. Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-ic`, branch `docs/neso-dp-interconnectors`, cut from
  `docs/neso-dp-generation`. Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (keep each note's line
  endings; Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it. ElecLink
  and North Sea Link are named after their one table (`eleclink`, `nsl`); the seat's build fix (4d306a3) lets the page
  stand in for the table's pointer page. Build them with `--only neso_data_portal/eleclink` and `.../nsl`.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\interconnectors\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: approved held pages in
  `BATCH-demand.md`, `BATCH-generation.md` and `BATCH-trading.md` (their `held-*-review.md` files).

## The pages

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| H1 | Held: `brit-ned` (`brit_ned`, 185 resources), `eleclink` (`eleclink`), `ifa` (`ifa_itl`, `ifa_da_id_weekly_itls`), `ifa2` (`ifa2_ifa_itl`, `ifa2_ifa_da_id_weekly_itls`) | every table held | 9821 | 9831 |
| H2 | Held: `nemolink` (`nemolink_ntc`, `nemolink_intraday`, `nemolink_nemo_da_id_weekly_ntcs`), `nsl` (`nsl`), `viking` (`viking_ntc`, `viking_link_ntc`) | every table held | 9822 | 9832 |

Known risks:
- **Every table is held** on the ledger's time-semantics questions (`C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\.planning\v0.22-FE-LEDGER.md`
  and the eligibility report `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\docs\neso_data_portal\eligibility.md`).
  The seven pages share a shape (capacity limits: ITL, NTC, by direction and time frame): keep the shared wording the
  same where the questions agree.
- **BritNed:** 185 resources; one failed capture was adjudicated in gridflow; read the note before stating coverage.
- **NSL:** current file only; the archive capture was adjudicated failed.
- **Held pages:** one plain line per table on why rows are not shown, covering the whole table, no codes, no
  local-data references (dated NESO facts only). Spell out ITL and NTC once.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own packages' files; never `git add`
or commit (the seat commits). Do not end your turn until your report or review is written. Correct out-of-date
note-body statements (for example "only one capture") yourself when the data proves them wrong.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| H1 | a62fc78e8e26ffa05 | | writing |
| H2 | | | not started |
