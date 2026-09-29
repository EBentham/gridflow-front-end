# indicated-day-ahead (lead `indgen`; `inddem`, `imbalngc`, `melngc`): review

Checker, 2026-09-29. Inputs: the `page:` block and body diffs in the vault worktree
(`git diff origin/master -- 30-vendors/elexon/datasets/{indgen,inddem,imbalngc,melngc}.md`), the
three committed artefacts and the built page in the front-end worktree, gridflow code, local silver and
bronze (read only, Polars), and the four Elexon BSC glossary pages the notes link.

## Verdict: REVISE

One major, three nits. Everything else passes (see "Checked and passed").

## Findings

### 1. major: `page.family.members[imbalngc].differs`, `page.family.members[melngc].differs`, `page.facts.grain`, `page.notebook.lead`

**What is wrong.** The page never says that `imbalngc` and `melngc` silver keep one of the 18 zone rows per
half-hour, the one the API lists last. It says only:
- "IMBALNGC and MELNGC keep no zone" (`facts.grain`);
- "silver drops the zone column" (both `differs`).

"Drops the zone column" is a true code fact. But it reads as if the zones were rolled up into a national
figure, when in fact one row per key is kept by API order. `notebook.lead` then calls the output "the
00:17 UTC publish's national rows". Cell 3 can filter `boundary == "N"` only for `indgen`, `inddem` and
`tsdf`; for `imbalngc` and `melngc` the `if "boundary" in df` branch is skipped. So "national" for those
two rests on our copy's row order, not on the code. This is the pilot's overclaim pattern: the code
guarantees one row in API order, and our copy happens to hold `N`. The brief (item 2) requires the page
to state this exactly.

**Evidence.**
- `silver/elexon/imbalngc.py:117`:
  `df.unique(subset=["settlement_date", "settlement_period"], keep="last")`, with no sort before it.
  `boundary` is not in `output_cols` (`:127-135`). `melngc.py` is identical at `:116` and `:126-134`.
- Bronze, read only: each day is one file, listed newest publish first (`publishTime` never increases
  down the file, for all four datasets on 16 and 17 Sep).
- Replicating the dedup on bronze with
  `unique(subset=["settlementDate","settlementPeriod"], keep="last")["boundary"].value_counts()` gives
  `{'N': 103}` for `imbalngc` and `melngc` on both 16 and 17 Sep. So `N` survives here only because
  of that row order.
- The indgen dedup key is not unique across files: over indgen silver, the 3-column key has 14,076
  distinct values against 25,956 rows. The 4-column key with `published_at` is unique (25,956).

**Fix.** The budgets are tight:

| Field | Words used |
|---|---|
| `facts.grain` | 14 of 14 |
| `raw_feed.note` | 28 of 30 |
| `differs` | 12 and 13 of 14 |
| `notebook.lead` | about 33 of 35 |
| `what_it_is` | about 52 of 60 |

Only `what_it_is` has real room. Suggested wording:
- `differs` (14 words each):
  - `imbalngc`: "`INDGEN` minus transmission demand forecast, MW; silver keeps the zone row listed last, unlabelled";
  - `melngc`: "Summed MELs minus national demand forecast; silver keeps the zone row listed last, unlabelled".
- `notebook.lead`: scope "national" to the three tables the cells filter. Alternatively, add to
  `what_it_is` "In silver, IMBALNGC and MELNGC keep one zone row per half-hour, whichever the API lists
  last (`N` in this window)". That is within budget, and "in this window" makes the `N` observation
  visible on the page rather than a universal.

### 2. nit: `page.chart_view.alt`

"Both peak at 18:30 UTC, at 33,220 and 31,228 MW" does not name which value belongs to which publish.
The numbers are right: `same_day` max is 33,220 at 18:30 and `day_ahead` max is 31,228 at 18:30, from
the committed series. But the alt introduced the 10:48 publish first, so a reader could pair them the
wrong way round. Suggested: "at 33,220 (00:17) and 31,228 MW (10:48)".

### 3. nit: `page.related[elexon/ndf].note`

"National demand forecast that MELNGC subtracts from summed MELs" matches the glossary's term
("the National Demand Forecast made by the System Operator"). But nobody has checked that it is the
BMRS `NDF` dataset: gridflow holds no MEL data, and the writer flagged this as unverified. It is
acceptable as a term match. I record it so the seat sees the caveat survived review.

### 4. nit (template, not the writer): notebook code at 390 px

At 390, cell 3 wraps mid-token: `tz_conv` / `ert("UTC")` and `tz_conver` / `t("UTC")`. Nothing is
clipped, so this is not a rubric 5 failure. The code block breaks words at any character, which is
template CSS. It is clean at 768 and above.

## Checked and passed

| Check | Evidence |
|---|---|
| INDGEN = sum of positive PNs (exporting units), half-hour average MW, per System Zone and national | Glossary `indicated-generation`, fetched 2026-09-29, quoted as the page states |
| INDDEM = sum of negative PNs (importing units), so negative | Glossary `indicated-demand`. Bronze `demand` max is −45 (16 Sep) and −41 (17 Sep); 0 positive rows |
| IMBALNGC = INDGEN minus the Transmission System Demand forecast; not INDGEN + INDDEM | Glossary `indicated-imbalance`. Bronze join on publish, date, period and boundary: max abs `imbalance − (generation − tsdf.demand)` is 38 (16 Sep, `N`), 334 (17 Sep, `N`) and ≤148 for zones; median abs `imbalance − (generation + demand)` is 8,526 to 9,425 at `N` |
| MELNGC = sum of submitted MELs minus the National Demand Forecast; larger means more spare | Glossary `indicated-margin`. Not reproducible (no MEL data). The page states only the vendor definition |
| No sign rule claimed for imbalance | The page states only the definition. The body's code-docstring sign (`schemas/elexon.py:336-339`) is labelled as code |
| Grain: one row per half-hour, zone and UTC publish day (indgen, inddem) | `indgen.py:114-117` (3-column key, `keep="last"`, unsorted). Silver: 3-column key plus file is unique (25,956). Each file holds 2 publishes (00:17 and about 10:48) |
| Key `(settlement_date, settlement_period, boundary, published_at)` | Unique over indgen silver: 25,956 of 25,956 |
| `boundary` = `N` + `B1`..`B17` | Silver `value_counts`: 18 values, 1,442 rows each |
| Chart: indgen, `N`, SD 17 Sep, 10:48 16 Sep and 00:17 17 Sep publishes | Series vs silver: 0 mismatches. `day_ahead` has 38 points from 04:00 (25,781); `same_day` has 45 from 00:30 (25,277). `rows_used` 83 = 38 + 45, `aggregation: last` over one row per point, so nothing is summed across publishes. The caption names both publishes, boundary, unit and settlement date |
| Key note: 10:48 starts at 04:00, and silver keeps another 16 Sep publish earlier | Silver file 20260916 at `N`, SD 17: the 00:17 16 Sep publish covers 23:00 to 03:30 (10 rows) and 10:48 covers 04:00 to 22:30 (38). The bronze 10:48 publish itself covers 23:00 to 22:30 (48 rows), so dedup explains the gap |
| Key note: 00:17 17 Sep starts at 00:30 | Silver file 20260917, 00:17: 45 rows from 00:30. It is the day's earliest publish, so any earlier row would have survived |
| Alt numbers | Within 1,122 (diff −1,122 at 05:00) to 06:30. From 07:00, `same_day` > `day_ahead` at every point, max +5,992 at 11:30. `day_ahead` min 22,495 at 13:00. Peaks at 18:30 |
| Frame rows and caption | Period 36 (16:30 UTC), `N`/`B1`/`B6`/`B9` × both publishes. Only 2 files hold SD 17 at 16:30 (the 15 Sep 10:50 publish stops at 03:30), so "both kept publishes" is right. `generated_by: gridflow-sample` |
| Column guide | One line per non-pipeline column, key columns first, frame order. Meanings match the code (`settlement_period_to_utc`, `generation`, `publishTime`) |
| `raw_feed.requests` | `endpoints.py:200-209` (paths), `build_params` sends only from/to + `page`. Bronze meta `request_url` for 16 Sep matches, apart from `%3A` encoding (same as the approved `ndf` page) |
| `raw_feed.commands` | `client.py` `while current < end`, 24 h chunks: ingest 16 to 18 gives publish days 16 and 17. Transform 16 to 17 inclusive. No `PARTITION_SOURCE_OFFSETS` override (base default `(0,)`), and `read_bronze` reads only the target day |
| Cadence "About every 30 minutes" | Bronze has 47 distinct `publishTime` values per UTC day (16 and 17 Sep), at about :16 to :18 and :46 to :48 |
| `notebook.lead` query semantics | `gridflow_models/.../handles/source.py:401-450`: date column `settlement_date` (`schema_manifest.py`), inclusive ends, bitemporal lineage columns excluded |
| Notebook outputs and `plot_alt` | Recomputed from silver at 00:17 `N`: 45 rows 00:30 to 22:30. TSDF max 33,351 at 18:00; melngc min 24,475 at 18:30; imbalngc min −1,026 at 07:30 and max 6,430 at 22:30; the check gives −62 / 0. Written by `scripts/run_notebooks.py`, read-only cells, no errors |
| Related | pn, tsdf, lolpdrm are correct against the glossary and data; ndf is nit 3. All ≤12 words |
| No local data / leakage | The grep over the page block and rendered text for `locally`, `held`, `our `, `since 20`, `N rows/days`, `% of`, em dash, middle dot, arrow, live/now/real-time found only "half-hour" and "national rows" (not counts) |
| Build and detector | `gridflow-build --only elexon/indgen`: green, wrote `indicated-day-ahead.html`. `detect.mjs --json`: `[]` |
| Staged spec and override | No `site/hifi/data/chart-specs/elexon/` and no authored override. Series `spec_origin: vault` |
| Mirror | `cmp` of all four `vault/elexon/*.md` against the vault worktree: identical |
| Body edits | Each cites `file:line` or a glossary link and fixes its span only. Checked: `timestamp_utc` 04:00 → 03:00 (P9 in BST = 03:00Z); `ingested_at` is transform time (`indgen.py:119-124`); dedup keys; `boundary` `B1`..`B17`; "latest wins" → earliest publish (bronze order confirmed); imbalngc unit MW (`schemas/elexon.py:338`); melngc "de-rated" removed. "A half-hour recurs in up to three publish days' files" is confirmed: SD 17 is in files 15, 16 and 17 |

## Screenshots

- **Set-up.**
  - Headless Chrome, each call under `timeout 60` with `--timeout=15000 --virtual-time-budget=5000`.
  - Served from the worktree's `site/hifi` on 127.0.0.1:9752 by a scratch server that exits by itself.
  - Wrapper pages put the page in an iframe of exactly 1440, 1024, 768 and 390 px.
  - An "open" set checks `#fx`, which unfolds the frame, and clicks `.ds-open`, which opens the notebook.
  - Shots and profiles are in `scratchpad/ida-check/`.
- **Result.** Nothing is clipped or overlapping at any width:
  - the hero title, chips, facts, scenery tops (turbines) and labels;
  - chart axes, both key notes and the x-label;
  - the four member requests and the commands;
  - the frame, folded (`…` column) and unfolded (scrolls inside its box);
  - the guide, the notebook's help card, table, check output and plot;
  - the stratum corner labels and related.
- **Dark mode was not shot separately.** The site has no dark theme: 0 matches for
  `prefers-color-scheme` or `data-theme` across `site/hifi/assets/*.css` and `*.js`.
