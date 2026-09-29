# Dataset fan-out: GIE batch (4 pages: AGSI+ storage and ALSI LNG)

Opened on 2026-09-29 after the 19:50 UTC usage reset. Bobbo: "Let's do the GIE AGSI+ and ALSI data source next."

- **Agents:** each page gets a writer and a checker, both Opus 5.5 · high.
- **Concurrency:** up to 10 agents at once, shared with the rest of the ENTSO-E batch. No launches after the 5-hour window passes about 92%.
- **Shipping (ruling #36):** the batch goes to main once every page is approved and the gates are green. Held pages stay blank.

## Where things are

- **Front-end worktree** (build, artefacts, mirror): `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\p26-gie`
  - Branch `v5/p26-gie`, cut from `main`. The `.venv` is synced with the build and distil extras.
- **Vault worktree** (canonical notes): `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\vault-p26-gie`
  - Branch `docs/v5-p26-gie`, cut from quant-vault `origin/master`.
  - Notes live at `30-vendors/gie/datasets/<dataset>.md`. Edit them with the Edit tool, which keeps their line endings.
- **Mirror:** `vault/gie/<dataset>.md` in the front-end worktree. After every edit, copy it byte for byte from the canonical note.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v5\p26\gie\`
  - Writer: `<page>-author.md`.
  - Checker: `<page>-review.md`, then `-review-2.md` and so on for re-checks.
- **Rules:**
  - Writer: `.planning/v5/author-brief.md`.
  - Checker: `.planning/v5/review-rubric.md`.
  - Look and anatomy: `DESIGN.md`, section "Dataset page anatomy".
- **Worked examples:** the live Elexon pages (notes in `vault/elexon/`) and the approved ENTSO-E pages (notes in the ENTSO-E worktree `p26-entsoe/vault/entsoe/`):
  - `fuelhh`: a stacked area.
  - `system_prices`: a price line.
  - `bmunits_reference`: a register with no time axis.
  - `demand-forecasts`: a family led by `ndf`.
  - `remit`: an event register.
- **Data truth:**
  - The gie rows of `.planning/v5/DATA-MATRIX.md`.
  - Local silver, read only:
    - `C:\gridflow-data\silver\gie_agsi\<dataset>\`
    - `C:\gridflow-data\silver\gie_alsi\lng\`
  - gridflow code: `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\src\gridflow\` (`connectors/gie/`, `silver/gie/`, `schemas/`). Read only.

## The 4 pages

| Page | Members (lead first) | Writer port | Checker port |
|---|---|---|---|
| `agsi-storage` | storage, storage_reports | 9851 | 9855 |
| `agsi-reference` | about_listing, about_summary | 9852 | 9856 |
| `lng` | lng (ALSI) | 9853 | 9857 |
| `unavailability` | unavailability | 9854 | 9858 |

Families are fixed in `site/hifi/data/gie.json`, and the lead's note carries the `page:` block. Build a family with
`--only gie/<lead>` (for example `--only gie/storage`), because the family slug renders nothing. `news` and `news_item`
have no page (no silver rows); leave them alone.

## Known gridflow defects to check (gridflow `.planning/BACKLOG.md` item 8)

- **8b, unavailability.** The per-day overlap filter in `silver/gie/agsi.py` (about lines 705 to 708) looked for the
  wrong field names. Every day therefore held all 341 outages.
  - A fix is on the unmerged gridflow branch `fix/silver-agsi-unavailability-overlap` (`80bad68`). Local silver was
    built without it.
  - The data matrix shows 1,705 rows on one date (2026-08-16).
  - Reproduce what silver actually holds before writing anything. If the rows repeat outages day after day, recommend
    a hold, and the seat decides.
- **8c.** The unavailability vault note names the wrong natural key; (facility, start, end) identifies an outage. The
  note also mis-types the silver columns, which are strings. Correct the note body from the code.

## Shared-worktree rules

- **Your files only:**
  - your dataset's vault notes and their mirror copies;
  - `site/hifi/data/{series,samples,notebooks}/gie/<dataset>*`;
  - your built page.

  Never edit the template, CSS, Python, `gie.json` or another dataset's files. Report a template problem instead.
- **Contention:** a DuckDB lock or a busy notebook kernel means another agent is running. Wait a minute, then retry.
- **Screenshots:**
  - Use headless Chrome with your own `--user-data-dir` under the scratchpad, or a static server on your port.
  - **Wrap every Chrome call in `timeout 60`, with `--timeout=15000 --virtual-time-budget=5000`.**
  - A true 390 check needs a 390 px iframe.
  - Stop any server you start.
- **Cleanup:** never delete a directory whose path is built from a variable, because the guard halts you. Leave Chrome profile folders in place.
- **Samples:** `gridflow-sample` needs eight rows. `record.select.columns` sets the print order; put the columns that tell rows apart first.
- **Thin data:** state a handful of rows or a narrow window plainly, in domain terms, and never invent a trend. If the rows can't support a page, say so and the seat decides whether to hold it.
- **Defects:** report every gridflow or data defect in your final message, and in a "Defects" section of your report
  written so it can be pasted into the backlog as is. The seat logs them.
- **No git** in either repo. The seat commits, mirrors and merges.

## Seat rulings carried over from the ENTSO-E batch

- **No literal `---` in front matter** (ruling #40). The vault's scripts split on it, and the build rejects it. Write any dashes as `\x2D` escapes in a double-quoted string. Write them plainly in sample rows and the note body.
- **Time stamps:** say what a stamp truly is, from the code. Never call a fetch or ingest stamp a publish or issue time.
- **Gas days:** state the gas-day convention gridflow actually stores (read the code and the vault's GIE README). Don't assert one from memory.
- **Cadence:** state it as "as sent in the responses we hold", not as a rule.
- **Detector:** the gate is no non-advisory findings. The em-dash-overuse advisory is accepted only when codes or CLI flags trigger it and the prose itself uses no dashes.
- **Units:** storage and LNG columns come in different units (energy, flow per day, volume of LNG). Read each charted
  column's unit from the code or the vault note, never from memory, and never mix units on one axis.
