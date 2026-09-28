# Dataset fan-out: Elexon batch (21 pages)

Opened 2026-09-28 on Bobbo's "start the Elexon batch". Plan and cost: about $10.45 per page for the
writer and checker (pilot measure), Opus 5.5 · high for both roles, at most about 8 agents at once.

## Where things are

- **Front-end worktree** (build, artefacts, mirror): `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\p26-elexon`
  - branch `v5/p26-elexon`, off `main` at `8cd3d26`;
  - `.venv` synced with the `build` and `distil` extras.
- **Vault worktree** (canonical notes): `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\vault-p26-elexon`
  - branch `docs/v5-p26-elexon`, off quant-vault `origin/master`;
  - notes are at `30-vendors/elexon/datasets/<dataset>.md` (CRLF: edit with the Edit tool).
- **Mirror copy:** `vault/elexon/<dataset>.md` in the front-end worktree, copied byte for byte from the vault note
  after every edit.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v5\p26\elexon\`
  - the writer's report is `<page>-author.md`;
  - the checker's is `<page>-review.md`, then `<page>-review-2.md` and so on for re-checks.
- **Rules:**
  - writer: `.planning/v5/author-brief.md`;
  - checker: `.planning/v5/review-rubric.md`;
  - look and anatomy: `DESIGN.md`, "Dataset page anatomy", in the main repo.
- **Worked examples**, their notes in `vault/elexon/` and pages under `site/hifi/data-sources/elexon/`:
  - `fuelhh`, a stacked area;
  - `system_prices`, a price line;
  - `bmunits_reference`, a register with no time axis;
  - `demand-outturn`, a family page led by `indo`.
- **Data truth:** `.planning/v5/DATA-MATRIX.md` holds each dataset's row (grain, key, coverage). Local silver is at
  `C:\gridflow-data\silver\elexon\<dataset>\` and is read-only.

## The 21 pages

| Group | Pages | Screenshot port |
|---|---|---|
| 1 | `mid`, `fuelinst`, `agpt`, `freq`, `temp` | 9711 to 9715 |
| 2 | `agws`, `windfor`, `atl`, `lolpdrm`, `demand-forecasts` (family: lead `ndf`; `ndfd`, `tsdf`, `tsdfd`) | 9721 to 9725 |
| 3 | `boal`, `disbsad`, `netbsad`, `soso`, `market_depth` | 9731 to 9735 |
| 4 | `pn`, `nonbm`, `fou2t14d`, `uou2t14d`, `remit` | 9741 to 9745 |
| 5 | `indicated-day-ahead` (family: lead `indgen`; `inddem`, `imbalngc`, `melngc`) | 9751 |

Families: the lead's note carries the `page:` block, as in the brief's "Family pages" section. The slug and members
are fixed in `site/hifi/data/elexon.json`.

## Shared-worktree rules (several writers work in the one worktree at once)

- Touch only your own dataset's files:
  - its vault note and its mirror copy;
  - `site/hifi/data/{series,samples,notebooks}/elexon/<dataset>*`;
  - its built page.
- Never edit the template, CSS, Python, `elexon.json` or another dataset's files. Report a template problem instead of
  working around it.
- A DuckDB lock or a busy notebook kernel means another writer is running: wait a minute and run it again.
- For screenshots, use headless Chrome (`C:\Program Files\Google\Chrome\Application\chrome.exe --headless=new
  --screenshot ...`) with your own `--user-data-dir` under the scratchpad, or a static server on your assigned
  port. Stop any server you start.
- No git commands in either repo. The seat commits, mirrors and merges.

## Seat follow-ups found during the batch

- **Weather scenery.** No landscape fits a weather reading (`temp`, and later the Open-Meteo pages). The hero
  scenery labels say "generation data". This needs a weather landscape or a neutral label (template work).
- **`--only` validates every note.** A build of one page fails on another writer's half-finished note.
  Writers retry; it is worth scoping the check to the page that was asked for.
