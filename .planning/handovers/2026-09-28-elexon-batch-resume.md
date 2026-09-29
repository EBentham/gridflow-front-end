# Resume the Elexon batch (resumed 2026-09-29; this note is the live tracker)

Batch brief: `.planning/v5/p26/BATCH-elexon.md`. Reports: `.planning/v5/p26/elexon/<page>-author.md`,
`-review.md`, `-review-2.md`. Resumed 2026-09-29. **Group 1 is approved** (mid, fuelinst, agpt, freq, temp). The preview is https://claude.ai/artifact/EYadKREQi3RnpufNwTH6Wf, waiting for Bobbo's look.

## Where the work lives

- **Front-end worktree:** `<scratch>\p26-elexon`, branch `v5/p26-elexon`. It includes main up to `3ee5b52`, and the
  writers' work in progress is checkpointed and pushed.
- **Vault worktree:** `<scratch>\vault-p26-elexon`, branch `docs/v5-p26-elexon`, checkpointed and pushed.
- `<scratch>` = `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad`.
  If it is ever cleared, both branches are on GitHub: recreate the worktrees from them.

## Per page (agent ids resume with SendMessage; transcripts are saved)

| Page | State at pause | Writer id | Checker id | Next |
|---|---|---|---|---|
| mid | APPROVED (re-check 3) | a7f628925ccf40d3d | a58c68c8a08822ca9 | done |
| temp | APPROVED | ae1512e0f404e146d | a175573d9dc677e6f | done |
| freq | APPROVED (review 2) | a757523f18b8872ee | ac2da42890daacdbe | done |
| fuelinst | APPROVED, nits applied | ac17b80233d655e7c | a3c074b63838c4512 | done |
| agpt | APPROVED, nits applied | ac08817af5dc65b24 | ae15bf21016303925 | done |
| agws | checker running | a02a65646052893e2 | a11c80668abbefdce | act on the verdict |
| windfor | checker running | a1ab63925783acd9e | a17288a5f3e21ed79 | act on the verdict |
| atl | revision 1 done (gaps now break); checker running | ae4cecd8c31375b94 | aa5264d2b291ec745 | act on the verdict |
| lolpdrm | APPROVED (review 2) | a9a809d3db7a3003d | a0485269512755d5d | done |
| demand-forecasts (family, lead ndf) | APPROVED (review 2); column order set (build it with `--only elexon/ndf`: the family slug renders nothing) | abf8f9353b1213246 | a47d843864370aaca | done |
| boal | APPROVED; column order set (Revision 3) | a31536a58a5a3b972 | adc1711149f93ffb3 | done |
| disbsad | APPROVED (review 2) | a5b3f85429c8bcd8c | aebe91340cd8e1a7c | done |
| market_depth | APPROVED, nits applied | aa46a54294f5cafaa | a8ccdd8aa4d55aa88 | done |
| netbsad | written; HELD, not in the batch PR (every field is 0 across 674 periods while DISBSAD shows up to 773 MWh: likely a gridflow parse bug) | a5e765b85bf3eff9a | — | research unit first, then check and publish |
| soso | APPROVED (review 2) | a41b75f70f9993f96 | a3d57de07ebfc9143 | done |
| pn | APPROVED (review 2), nits applied | a1f13e90b72f5b8c5 | a1f47734a4b13c4d3 | done |
| nonbm | written; HELD (ruling #37): silver repeats one record (1 Apr, period 22) and the connector likely sends `publishDateTimeFrom/To` where the API lists `from`/`to`; the fixed 8-row sample also fails | acc464ee4405621aa | — | gridflow research unit, then a sampler that accepts fewer rows, then check and publish |
| fou2t14d | written (72 hourly publishes for 24 Sep, CCGT/wind/nuclear); checker running | a8d7b6b1894c6c155 | a2b14d08df16b6c0d | act on the verdict |
| uou2t14d | written (one publish, 3 units, 23 Sep to 5 Oct); checker running | a0a9e27c09f4cd6ff | a29dfe5ba88e4765f | act on the verdict |
| remit, indicated-day-ahead (family) | not started | — | — | launch writers under the throttle |

If a restart kills a running agent, check its report file and the vault note first, then resume it by id.

## Throttle (Bobbo 2026-09-29)

- At most **2 agents at once** once the current wave drains. No launches above about **85% of the 5-hour window** (75% at about 00:30 UTC on 2026-09-29, reset 04:00 UTC);
  set a timer to resume at the reset. Check with `get_usage` as agents finish. Queued work waits in this table.

**USAGE PAUSE (00:45 UTC 2026-09-29, 5-hour window at 81%):** no launches until the reset at 04:00 UTC. A timer
resumes the batch at about 04:05 UTC. Only the soso checker (a3d57de07ebfc9143) was still running at the pause.

**Rulings 2026-09-29:** #35 column order approved (build `record.select.columns`, then have the boal and
demand-forecasts writers use it). #36 autonomous: ship the Elexon batch PR to main once all its pages are approved and
the gates are green, with no preview wait.

**Column order shipped** (PR #53, `e6d44f4`, merged into the batch worktree at `5881dae`, 11:15 UTC). Follow-up: boal
and demand-forecasts writers set `record.select.columns`, re-sample, rebuild.

**Held pages at PR time:** restore `vault/elexon/{netbsad,nonbm}.md` from origin/main in the site PR and leave out their
artefacts, so both stay blank. The vault PR needs the same care: their `page:` blocks must not reach canonical master
until unheld (the next mirror sync would publish them).

**Next, in order:** act on the fou2t14d and uou2t14d verdicts, writers for remit and
indicated-day-ahead. Keep at most 2 agents at a time and stop launching at about 85% of the 5-hour window. Then group
2 onwards gets a batch PR into main, after Bobbo's look at the preview (republish
https://claude.ai/artifact/EYadKREQi3RnpufNwTH6Wf from `<scratch>\p26-elexon\site\hifi`, file list in
`<scratch>\elexon-preview-files.json`). netbsad stays blank (held).

## Seat items

- **gridflow data loss (from boal):** the silver transform keeps only the last segment per acceptance and settlement
  period and drops the segment times (`boal.py:74-78, 120-148`). On 19 Sep, 41,078 raw segments became 22,538 silver
  rows, so silver cannot rebuild an acceptance's MW profile. This is gridflow work (a connector or transform fix);
  the page states it plainly.
- **lolpdrm publish choice:** which publish silver keeps depends on bronze file-name order (fetch time, then a
  hash of the body: `bronze/writer.py:33,57`), so it is deterministic but not necessarily the latest publish. The
  writer's "differs between machines" claim was wrong (checker). Worth a gridflow look.
- **netbsad note:** two off-by-one page numbers in its Imbalance Pricing Guidance citations (disbsad checker).
  Fix when netbsad is unheld.
- **NETBSAD all zeros (held page):** every NETBSAD field reads 0 in silver across 674 periods where DISBSAD has
  actions. Check whether the gridflow connector or transformer reads the right fields before publishing
  `netbsad` (class-3 hold: its page stays blank on the live site).
- **gridflow data loss (from pn):** silver drops PN segment times (as with boal), and about 46 units per period
  arrive without a `bmUnit` id and are merged by the dedup into one null row per period. This is gridflow work.
- **gridflow duplicates (from disbsad):** silver stores the midnight half-hour twice across neighbouring days
  (the same pattern as freq and fuelinst). Pages drop the repeat. This is gridflow work (per-day windows include
  the end instant).
- **Chart spec takes one value column** (market_depth): a wide table cannot chart two of its columns (accepted
  offers and bids) as two series. Template work.
- **Frame fold order (hit by boal and demand-forecasts):** the sample frame folds from the right in silver's column
  order, so the columns that matter (boal MW levels; demand and `published_at`) hide behind `…` and the rows look
  identical. Proposed: an optional `record.select.columns` (a Polars `.select` order, pipeline columns still
  last), which touches the locked 3a design ("as silver prints"), so Bobbo rules first. Then rebuild both pages.

- **gridflow gap (from nonbm):** the connector sends `publishDateTimeFrom/To`; the vault's API table lists `from`/`to`.
  Thirteen windows (May, Aug) all returned the same 1 Apr record. Needs a research unit against the live parameters.
- **gridflow (from uou2t14d):** silver dedups on `(settlement_date, bm_unit_id)` per bronze day with no `published_at`,
  so one hourly publish survives per fetched day, chosen by file order; null-id units collapse (80 of 81 dropped per date).
- **Vault glossary** (`20-domain/glossary.md:123-124`) calls FOU2T14D "by BM Unit"; it is by fuel type (fou2t14d writer).
- **Sampler takes exactly 8 rows** (`sample.py:109`): a dataset with fewer distinct rows cannot build. Template work.

- **gridflow discrepancy (from windfor):** silver `windfor` has no `settlement_date`, `settlement_period` or
  `initial_forecast_mw` and is keyed on `(timestamp_utc, published_at)`. That contradicts the pydantic schema and the
  data matrix's "match" verdict, but every silver and bronze file agrees with it. This is gridflow work: raise it
  there. Also, the windfor chart series names depend on Polars' text form of the issue times, so a Polars upgrade could
  break a `gridflow-distil` re-run (CI is unaffected).

- **Shipped:** #48 (home scenery), #49 (notebook table headers, line baselines, hour ticks, axis decimals),
  #50 (settlement-date axes on UK midnight), #51 (lines break at absent periods; `--only` scoped), #52 (no label on the
  axis-closing midnight). All are merged to main and deployed.
- **ATL missing periods:** 130 of 336 half-hours absent in the chart week, mostly before midday. Why is unknown, so
  this needs a research unit (vendor behaviour or connector), not a guess on the page.
- **Headless Chrome floors at 500 px:** a true 390 needs a 390 px iframe (atl writer). Tell the next writers.
- **Weather scenery:** `temp` (and later Open-Meteo) has no weather landscape, and the hero says "generation data".
- **`elexon.json`:** the MID blurb is corrected in the worktree, and it ships with the batch PR.
- **Go-live per group:** wait for Bobbo's preview look. He has not ruled on auto-merge.
