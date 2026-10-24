# NESO Data Portal pages: Carbon intensity

Opened 2026-10-24 under the approved plan (ruling 62) and the resume (ruling 65). 4 held pages, one writer and one
checker, one branch and one PR stacked on Electricity Market Reform. `historic-generation-mix` already has its page.
Bobbo looks at the pages before merge.

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-ci`, branch `feat/neso-dp-carbon-intensity`, cut from
  `feat/neso-dp-emr`. Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-ci`, branch `docs/neso-dp-carbon-intensity`, cut from
  `docs/neso-dp-emr`. Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (keep each note's line
  endings; Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\carbon-intensity\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: the Interconnectors held batches
  (`interconnectors\held-*.md`) and the Generation held batches (`generation\held-*.md`).

## The pages

| # | Page (slug) | Members | Writer port | Checker port |
|---|---|---|---|---|
| H | Held: `carbon-intensity-of-balancing-actions` (`ci_balancing_actions`), `country-carbon-intensity-forecast` (`country_ci_forecast`), `national-carbon-intensity-forecast` (`national_ci_forecast`), `regional-carbon-intensity-forecast` (`regional_ci_forecast`) | every table held | 9921 | 9931 |

Known risks:
- **Held on the ledger's question:** the files don't say when each row was first published
  (`C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\.planning\v0.22-FE-LEDGER.md` and the eligibility report
  `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\docs\neso_data_portal\eligibility.md`). The four pages share the
  question: keep the shared wording the same.
- **Two NESO carbon intensity sources:** the Carbon Intensity API has its own hub on the site and stays separate
  (ruling 57). A page may link the API hub as a related page where NESO's text ties them; never merge or equate the
  two sources' numbers without a cited NESO statement.
- **PDF files** (methodology documents) in the raw feed: list them as NESO gives them; do not summarise their contents
  beyond NESO's own catalogue text unless the PDF is read and cited.
- **Held pages:** one plain line per table on why rows are not shown, covering the whole table, no codes, no
  local-data references (dated NESO facts only).

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own packages' files; never `git add`
or commit (the seat commits). Do not end your turn until your report or review is written. Correct out-of-date
note-body statements yourself when the data proves them wrong.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| H | a057fdca986005d8a | a71f8c32a052eb729 | APPROVED with nits x4, nits with writer; 20cb logged; held lines share the first clause, second halves follow each table's question (seat, PROXY-SOURCED) |
