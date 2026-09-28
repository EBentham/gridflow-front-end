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
| lolpdrm | writer running | a9a809d3db7a3003d | — | launch the checker |
| demand-forecasts (family, lead ndf) | writer running | abf8f9353b1213246 | — | launch the checker |
| boal | writer running | a31536a58a5a3b972 | — | launch the checker |
| disbsad | writer running | a5b3f85429c8bcd8c | — | launch the checker |
| netbsad, soso, market_depth, group 4, group 5 | not started | — | — | launch writers |

If a restart kills a running agent, check its report file and the vault note first, then resume it by id.

## Seat items

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
