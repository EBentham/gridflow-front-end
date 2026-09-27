# Phase 25b report notes: the dataset page template and its five-page pilot

Branch `v5/p25b-template` (off `origin/v5/site`), one PR into `v5/site`, left open. The vault branch
is `docs/v5-p25b-pilot` (off quant-vault `origin/master`), with one PR into master, left open. The
mirror copies in `vault/` come from that unmerged vault branch.

## What was built

- `templates/dataset.html.j2`: the locked anatomy. Sky hero with facts and landscape; topsoil prose
  and chart; bronze raw feed; silver record and eight rows; gold notebook; deep related datasets.
  Partials are `_partials/landscape/{power,market,gas,units}.svg.j2`. The family variant lists
  members with their requests, and `redirect.html.j2` points member addresses at the family page.
  Pages without a `page:` block stay on `dataset-legacy.html.j2` until the fan-out.
- Content model, `page_fields.py`:
  - fields: title, summary, facts, landscape, what_it_is, how_used, chart, chart_view, raw_feed,
    record, notebook, related, family;
  - word budgets are in `BUDGET`; the build fails on missing, over-budget or unknown fields;
  - rules: khaki only for OTHER; one key entry per series; requests must be real URLs and commands
    real `gridflow` calls; notebook cells read-only.
- Committed artefacts:
  - chart series: `gridflow-distil`;
  - eight real rows: `gridflow-sample`;
  - executed notebooks: `scripts/run_notebooks.py`, on the gridflow_models venv and kernel, outputs
    stored as data plus PNGs.
  - Each artefact carries a digest of the spec or cells that made it, and the build fails when
    they drift. CI builds without silver, so artefacts are committed, never computed in CI.
- Build-time SVG charts (`chart_svg.py`): stacked-area with signed layers hanging below zero, lines
  that break on gaps, and horizontal bars; a wide and a narrow drawing swap at 760 px.
- Retired for the pilot datasets only: the staged chart specs, and the authored overrides for
  fuelhh, system_prices, indod, bmunits_reference and entsog physical_flows.

## Pilot pages and review verdicts (Opus 5.5 reviewer against `review-rubric.md`)

| Page | Verdict | Notes |
|---|---|---|
| elexon/fuelhh | seat-authored worked example; checked by the page tests and the seat, no separate Opus review | the first page; its facts research ran as a separate read-only agent |
| elexon/system_prices | APPROVE, 4 nits applied | SBP = SSP stated only for the window shown (0 of 88,694 latest rows differ; no vendor rule found) |
| elexon demand-outturn (INDO, ITSDO, INDOD) | REVISE, fixed, then APPROVE | no unit claimed for INDOD (see open items) |
| entsog/physical_flows | REVISE (2 majors, 3 nits), fixed, then APPROVE | "no point filter", not "every point"; far-side reports scoped to this window |
| elexon/bmunits_reference | APPROVE, 2 nits and 2 template notes applied | counts registrations, never sums capacity |

## Cost (list prices, from transcripts)

- Authors: system_prices $6.96, demand family $7.67, physical_flows $7.53, bmunits_reference $6.36.
  The average is $7.13 per page.
- Opus reviewers, re-reviews included: $3.34, $3.01, $3.47, $3.47. The average is $3.32 per page.
- Per dataset, author plus review: about $10.45.
- Pilot total: authors $28.52 plus reviewers $13.29 = $41.81. The fuelhh fact research added $2.81;
  the seat's own authoring and fixes are not itemised.

## Gates (whole branch, final run)

- `uv run --system-certs --extra build gridflow-build --check`: OK, idempotent across 165 pages
  plus 7 hubs.
- pytest: 68 passed. ruff check: clean. ruff format: clean.
- `htmlhint --config .htmlhintrc "site/hifi/**/*.html"`: 177 files, no errors.
- `lychee --no-progress --offline --include-fragments './site/hifi/**/*.html'`: 0 errors. Two
  fragment breaks came in from the base branch (`models/demand-forecast.html` linked to
  `index.html#models`, which the v5 homepage lacks) and were fixed in their own commit.
- `detect.mjs --json`: `[]` on all five pilot pages.
- 390 px, Browser pane emulation: `scrollWidth` 390 and no unclipped overflow on all five. The
  family page first overflowed to 537 px and was fixed in the CSS.
- AA contrast: every visible text node on all five pages passes, the notebook panel included
  (273 to 401 nodes per page). Chart axis text is 7.60:1.
- Local-data grep over the five built pages ("locally", "our copy", row counts, "since 20xx", em
  dash): no hits.

## Flags carried in

- **Licence line (site-wide ruling):** removed from the shared footer in `site/hifi/assets/site.js`.
  No file under `site/hifi` carries licence text.
- **Help card "store it locally":** the wording is gridflow_models' own help text for `backfill`,
  not template text. The build now leaves that row out of the rendered card instead of rewording
  real output. The committed notebook artefacts are unchanged; fixing the wording at source is a
  gridflow_models change.
- **Imbalance volume sign: RESOLVED.** Positive net imbalance volume means the system is short.
  - Sources: Elexon data item N0430 and Elexon's imbalance pricing page. gridflow passes the value
    through unchanged. The evidence is in the main checkout's `.planning/v5/imbalance-sign-finding.md`.
  - The pilot's own check agreed (16 to 22 Sep 2026, 336 latest rows):
    - NIV > 0: mean SSP 189.8; NIV <= 0: mean SSP 67.0; corr 0.695.
    - All 53 negative prices have NIV <= 0.
  - The vault domain note `20-domain/instruments/imbalance-volume.md` is fixed on the vault branch,
    in its own commit citing N0430. Its price and forecasting sections were already right.
  - system_prices page field (14-word budget): "Net imbalance, MWh; positive means the system was
    short, negative long (Elexon N0430)". The full description is in the note body's schema row.
- **SBP equals SSP (carry-in):** checked against code and silver. The two prices are parsed from
  separate fields (`system_prices.py:125`) and differ on 0 of 88,694 latest rows. No vendor rule was
  found, so the page states equality only for the week it charts.
- **Help card dataset count (carry-in):** the page never states a count. The card says 35 while
  `list_datasets()` returns 33 (aliases); that is a gridflow_models bug.

## Open items

- **INDOD unit:** no primary source states it. Elexon's documentation pages render in JavaScript and
  returned nothing; the BMRS page is titled "Daily energy transmitted". The page says it tracks half
  the INDO sum (within 2), and the body calls that a project check.
- **Open research, ENTSOG `meta.count` vs `meta.total`:** every physical_flows bronze body under
  `limit=-1` shows `meta.count` 984 against `meta.total` 1650 (13 Sep: 967 against 1621). We cannot
  tell whether `total` counts rows that are not returned, so the page says "no point filter", not
  "every point". Answering it needs ENTSOG documentation or a live call; no live call was made.
- **gridflow code docstrings, stale:** `schemas/elexon.py:450` says INDOD `timestamp_utc` is midnight
  UTC; the transformer uses UK midnight.
- **Notebook display:** pandas shows `timestamp_utc` in UK time (`+01:00`) in notebook outputs,
  while the eight rows show UTC. The instants are the same; the display comes from gridflow_models.
- **Family pages:** a family's chart draws one member, and the caption says so. Member addresses
  become redirect pointers; the page set follows the families ruling.
- **gridflow-models GitHub links:** the notebook's needs line links both repos. Whether
  gridflow-models is public is for Bobbo to confirm.
