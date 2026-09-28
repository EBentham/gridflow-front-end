claude-opus-5-5

# Models page content check (p27-r1 draft A-models vs gridflow_models)

Checked 2026-09-27 against gridflow_models `main` at `1404300` (2026-09-27 19:46 +0100) and gridflow `master` at `2822d38`. The draft is `p27-r1/canvas/project/A-models.dc.html` (text and aria extracted) and its generator `p27-r1/A/p_models.py`. Every score was reproduced read-only from its stored record: the manifest (a copy of `data/gridflow_models.duckdb`), `data/models/*/validation_record.json`, and gold Parquet under `C:\gridflow-data\gold\`. Nothing was written, trained or refreshed. Paths are relative to gridflow_models unless marked gridflow.

## Read this first: two findings that change the page

**A. Ruling #15's premise changed today.** Ruling #15 (2026-09-27T11:41Z) says wind and solar are shown "as they stand (never trained)". That was true when it was written. Since then, gridflow_models `1e3584f` (15:46) and `6c6a63d` (19:31) landed, and both models were fitted on the real store and scored in a walk-forward backtest:

- `data/models/wind_lgbm_quantile_v1/20260927T145057Z-FAILED/validation_record.json`: median pinball 416.7 MW (gate 500 passes), CRPS skill over its baseline 0.161 (passes), 90% coverage 0.722 (fails; the gate is 0.90 ± 0.05), 0 crossings.
- `data/models/solar_lgbm_quantile_v1/20260927T183348Z-FAILED/validation_record.json`: median pinball 290.4 MW on daylight rows (gate 300 passes), skill 0.193 (passes), 90% coverage 0.712 (fails), 0 crossings.

Neither run wrote a manifest row (`WIND-TRAIN.md`, `SOLAR-TRAIN.md` in `.planning/phases/v2.3-H-{2,3}-*/receipts/`; gridflow_models RULINGS #1001, #1006). Neither has anything in gold. `models.list()` reports both as `unregistered` (`src/gridflow_models/research/handles/models.py:186-222`). The gridflow_models milestone that ran these is at a stop awaiting Bobbo's ratification (gridflow_models RULINGS #1007).

Recommended ruling (yes/no for Bobbo): **yes**, re-rule #15 to "show wind and solar as unregistered: scored once, no version registered, nothing in gold", and hold the gate-failing scores off the page until he rules otherwise. The pack follows this. The scores sit in `pack.json` under `held`, never under `scores`. "Never trained" must not ship: it is now false.

**B. The chain the seat described is the code path, but not what the published run did.** The seat's description is confirmed as design. Demand, wind and solar quantile forecasts go into a Monte Carlo sampler that draws residual demand (1,000 draws, components independent). Signed netting is subtracted. Each draw is cleared against the stack built for that half-hour, and the draws' prices give the SMP quantiles. The stack is constructive with no learning, and SMP has a no-op fit. However:

- The only published SMP run, `41de423cfc0b421e` (policy `smp_headline_perfect_prog_v2`), wires demand, wind and solar as `kind: realised` outturn datasets (`configs/models/fundamentals_smp/gb_v1.yaml:45-62`). The runtime wraps each one in `RealisedQuantileAdapter` (`src/gridflow_models/backtest/smp_runtime.py:780-796`), which sets every quantile to the observed value (`src/gridflow_models/estimators/fundamentals_smp/realised.py:36-79`).
- With every quantile equal, the sampler's interpolation has zero slope, so all 1,000 draws are identical (`estimators/fundamentals_smp/sampler.py:125-177`). The output is one clearing price per half-hour, not a distribution. The card says so: coverage "does not establish probabilistic calibration" (`docs/MODEL_CARDS/fundamentals_smp_gb_v1.md:71-73`).
- The forecast route exists in code (`EstimatorInputConfig`, `src/gridflow_models/backtest/smp_config.py:66-76`; loaded through `_validated_estimator`, `smp_runtime.py:797-808`). It needs a registered manifest bundle, which wind and solar do not have, so the forecast-fed chain has never run.

So the drawing should run the SMP's residual-demand cable from the three **outturn datasets** (`elexon/indo`, `elexon/fuelhh` WIND, `neso_data_portal/historic_generation_mix` solar), not from the three forecast models. The draft generator already knew this ("The SMP model has no cable: its published headline clears the stack against realised inputs", `p_models.py:3-4`). The seat's answer in `models-decisions.md:10-14` needs this correction. `pack.json` carries every edge with `exercised_in_published_run`, and all three forecast-to-SMP edges are `false`.

Page-wide rule check: the draft has no em dashes, arrows or middle dots in visible copy, no eyebrows, and no planning words. It does carry local-data counts in the SMP table ("816 periods", "17,520 periods"); drop them.

## 1. Hero: "Five models, from demand to the day-ahead price"

Says: five models; lede "gridflow-models is a separate library that reads gridflow's DuckDB catalogue and Parquet. It holds models for demand, wind and solar, a GB merit-order stack, and a model that clears the stack into a day-ahead price. It does not produce orders." Link "Read the model cards".

Wrong or stale:
- "Five models" is countable (demand v1 and v2 count as one model; six configs under `configs/models/`), but it is exactly the five-siblings framing Bobbo asked to lose (`models-decisions.md:14-15`). Use a headline without a count.
- "reads gridflow's DuckDB catalogue and Parquet": both are true, but for different jobs. Training and backtests read gridflow's silver Parquet directly, "without importing gridflow modules" (`src/gridflow_models/data/gridflow_source.py:1, 45-46`). The notebook `data.*` surface wraps gridflow's `GridflowClient` over `gridflow.duckdb` (`src/gridflow_models/research/_pandas_client.py:1-26`). Fine as a one-liner.

Fine: "does not produce orders" (`CONTEXT.md:248-251`: the workbench "produces forecasts and Stack Model outputs; it does not produce orders, positions, or P&L attribution"). The model cards exist (`docs/MODEL_CARDS/`, six files).

Verdict: KEEP WITH FIXES. Drop the count and say the chain in one sentence.

## 2. The sky drawing (substation, wind farm, solar farm, plant fleet)

Says: pylons into a substation for national demand; a wind farm; a solar farm; the plant fleet in merit order (biomass, nuclear, CCGT, OCGT); labels "onshore wind", "wind farm".

Checks:
- Demand target is INDO, GB transmission-metered national demand (`configs/models/day_ahead/lgbm_demand_v1.yaml:10-14`). A substation fits.
- Wind target is FUELHH WIND, metered and post-curtailment (`docs/MODEL_CARDS/wind_lgbm_quantile_v1.md:3`). The 12 weather sites are 8 offshore and 4 onshore (`src/gridflow_models/features/generation_sites.py:29`: dogger_bank, hornsea, east_anglia, triton_knoll, walney, gwynt_y_mor, beatrice, seagreen, highland_central, borders_crystalrig, whitelee, pen_y_cymoedd). The "onshore wind" ridge label undersells an offshore-heavy set. Neutral "wind farm" is fine.
- Solar target is NESO's estimate of embedded solar, "mostly embedded and unmetered" (`docs/MODEL_CARDS/solar_lgbm_quantile_v1.md:16-18, 116-118`). A solar farm is an acceptable icon.
- Plant fleet: the stack prices CCGT, COAL, NUCLEAR, BIOMASS and OCGT (`configs/engineering/plant_technology.yaml:47-100`). Biomass and nuclear carry zero fuel cost by assumption, so they sit at the bottom of the published stack (`configs/models/stack/gb_v1.yaml:33-39`). Coal is missing from the drawing; that is optional.

Verdict: KEEP (Bobbo's keep). Relabel the ridge from "onshore wind" to plain "wind".

## 3. Cables and the silver inputs band

Says, per cable: demand reads `elexon/indo` (target) and `open_meteo/historical_demand` (weather, version 2); wind reads `elexon/fuelhh` (WIND, the target), `open_meteo/historical_wind` (12 sites) and `elexon/windfor` (benchmark); solar reads `elexon/fuelhh` (SOLAR, the target) and `open_meteo/historical_solar` (6 sites); stack reads `elexon/bmunits_reference`, `elexon/remit` and `elexon/fou2t14d` (derating). SMP has no cable.

Wrong or stale:
- Solar target: now `neso_data_portal/historic_generation_mix`, column `solar`, pinned to one capture (`configs/models/solar/lgbm_quantile_v1.yaml:16-24`, from `6c6a63d`). `elexon/fuelhh` SOLAR is no longer read.
- Wind `elexon/windfor` "benchmark": the config lists it under `benchmarks:` (`configs/models/wind/lgbm_quantile_v1.yaml:92-96`), but the card says WINDFOR is "neither the fitted baseline nor a gate" and is not like-for-like (forecast weather, pre-curtailment) (`docs/MODEL_CARDS/wind_lgbm_quantile_v1.md:19, 42`). Call it "reference".
- Stack inputs are incomplete. The curve also depends on `data/manual/commodities.csv` for gas, coal and carbon prices, labelled synthetic in config (`configs/models/stack/gb_v1.yaml:21-28`), and on `configs/engineering/plant_technology.yaml` for efficiencies and emissions. Neither is a gridflow dataset, so they should not be drawn as silver taps. They belong in the text.
- `elexon/fou2t14d` "derating": right for the published headline, which uses FOU2T14D derating (card `fundamentals_smp_gb_v1.md:445-448`, ladder `configs/backtest/price_formation_ladder_v2.yaml:31-37`). Coverage is partial: 144 of 816 headline periods, with the rest falling back per fuel (`fundamentals_smp_gb_v1.md:474`). Outside that profile the code treats FOU2T14D as cross-validation only (`src/gridflow_models/estimators/stack/plant_universe.py:1000-1011`).
- `entsoe/installed_capacity_units` is read, but only as a logged cross-check, and it cannot match keys (`plant_universe.py:1078-1100`). Correctly absent from the drawing.
- SMP needs a cable of its own. It reads realised `elexon/indo`, `elexon/fuelhh` (WIND plus signed NPSHYD hydro, ten interconnectors, OTHER and pumped storage) and `neso_data_portal/historic_generation_mix` solar, and is scored against `elexon/mid` APXMIDP (`configs/models/fundamentals_smp/gb_v1.yaml:45-122`). See finding B.

Fine: `elexon/indo` target (`lgbm_demand_v1.yaml:10-14`); `open_meteo/historical_demand` for v2 only (`lgbm_demand_v2.yaml:29-30`); `open_meteo/historical_wind`, 12 sites (`lgbm_quantile_v1.yaml:26-36`; `generation_sites.py:29`); `open_meteo/historical_solar`, 6 sites (`solar/lgbm_quantile_v1.yaml:34-44`; `generation_sites.py:50`); `elexon/bmunits_reference` and `elexon/remit` (`stack/gb_v1.yaml:12-17`).

Verdict: KEEP WITH FIXES (Bobbo's keep). Fix the solar tap, add the SMP cable from the outturn datasets, and call WINDFOR a reference.

## 4. Day-ahead demand entry

Says: "GB national demand outturn, half-hourly in MW, forecast a day ahead. LightGBM quantile regression, one model per quantile from 0.05 to 0.95, sorted so they never cross, with a conformal outer band. Version 2 adds weather and calendar features." Table: "Walk-forward backtest, 12 folds of 30 days, 1 September 2024 to 22 August 2026", with v1 pinball 711.04 MW / coverage 0.893 and v2 599.72 MW / 0.883. Note "v2 is scored with actual weather standing in for the forecast, so its score is optimistic." Chart of v1 fold 12, 20 and 21 August 2026, run `a55a829bc51c40b2`, "forecast issued at noon the day before". Handles `models.demand_forecast`, `models.demand_forecast_v2`.

Scores (all real, reproduced):
- v1 711.04 MW / 0.893: gold `forecast_metrics` run `a55a829bc51c40b2`, scope `run`, `pinball_q0.5` 711.043568, `coverage_nominal90` 0.893341, gates pass, `vintage_kind` issued, policy `v1_day_anchored_noon_d1`. It matches manifest version `20260827T081123Z` exactly (`validation_record.json`), and the card calls it the honest headline (`docs/MODEL_CARDS/day_ahead_lgbm_demand_v1.md:246-285`). The latest v1 manifest row, `20260829T184619Z`, re-registers identical metrics and the same estimator hash under a new config hash.
- v2 599.72 MW / 0.883: gold run `b367a742aa544f8f`, `vintage_kind` perfect_prog, `perfect_prog_caveat` true (card `day_ahead_lgbm_demand_v2.md:44-53`). Note: the registered v2 version `20260903T202038Z` scores 584.89 / 0.890 in its own record, but the card says "No metric on this card is derived from it" (`day_ahead_lgbm_demand_v2.md:240-247`). Keep 599.72.
- Window: both runs score 12 separate 30-day folds spread from 2024-09-01 12:00Z to 2026-08-22 00:00Z (fold starts read from `validation_record_predictions.parquet`). "12 folds of 30 days, 1 September 2024 to 22 August 2026" is right, but the folds are spaced about two months apart, not contiguous. Consider "12 thirty-day test windows between ...".
- Chart: gold `forecasts` run `a55a829bc51c40b2`, fold 12, 96 half-hours, values 17,466 to 31,583 MW (matches the aria). Issued 12:00 UTC the day before, correct.

Wrong or stale:
- "Version 2 adds weather and calendar features": v1 already has calendar features (`day_ahead_lgbm_demand_v1.md:18-20`). v2 adds population-weighted temperature and wind speed, an effective temperature and a winter-season term (`day_ahead_lgbm_demand_v2.md:74-100`). Say "adds weather".
- "sorted so they never cross": right about the emitted output. The raw heads do cross, and are sorted at output (`day_ahead_lgbm_demand_v1.md:101-106`). Fine.

Fine: LightGBM, one regressor per quantile, 0.05 to 0.95 (`lgbm_demand_v1.yaml:22-23`); conformal (CQR) widening of the outer band (`lgbm_demand_v1.yaml:35-38`; card :108-116); the v2 caveat (card :21-40).

Not for copy: gold also holds one issued v2 forecast (run `1e5e904884c74bb9`, `v2_live_issue_fixed`) with no scored comparison. It invites "live" framing, so leave it out.

Verdict: KEEP WITH FIXES. The best-evidenced block on the page; fix "and calendar" and loosen the window phrasing.

## 5. Wind generation entry

Says: "GB wind outturn, half-hourly in MW, a day ahead. LightGBM quantile regression on weather at 12 sites, benchmarked against WINDFOR." Status line: "A configuration, a model card and a training dataset exist. There are no forecasts or scores in gold." Handle `models.wind_forecast`.

Wrong or stale:
- The status line is stale (finding A). Say that it was scored once, fell short of the coverage gate, and has no registered version. "No forecasts or scores in gold" is still true.
- "benchmarked against WINDFOR": the scored baseline is a binned power curve on fleet mean hub-height wind speed (`configs/models/wind/lgbm_quantile_v1.yaml:56-60`). WINDFOR is a reference only.
- "GB wind outturn": more exactly, metered, post-curtailment FUELHH WIND (card :3).

Fine: LightGBM quantile heads (`lgbm_quantile_v1.yaml:42-50`); 12 sites (`generation_sites.py:29`); 24 h horizon (`lgbm_quantile_v1.yaml:16`); handle `wind_forecast` (`lgbm_quantile_v1.yaml:98`).

Verdict: KEEP WITH FIXES. The status is the fix, and it waits on the #15 ruling.

## 6. Solar generation entry

Says: "GB solar, half-hourly, a day ahead. LightGBM quantile regression on weather at 6 sites, benchmarked against persistence." Status line: "Its configured target, elexon/fuelhh SOLAR, holds no rows. A configuration and a model card exist; there are no forecasts or scores in gold." Handle `models.solar_forecast`.

Wrong or stale:
- The target is NESO's embedded-solar estimate, `neso_data_portal/historic_generation_mix.solar` (`configs/models/solar/lgbm_quantile_v1.yaml:16-24`). The whole FUELHH sentence is stale.
- "benchmarked against persistence": the config has no `benchmarks:` block. The scored baseline is a binned curve on national mean irradiance, banded by sun elevation (`lgbm_quantile_v1.yaml:62-69`). Persistence is a receipt reference only (card :106-109).
- The status line is stale (finding A).
- Scored on daylight rows only (`lgbm_quantile_v1.yaml:61`), which matters if a score is ever shown.

Fine: 6 sites (`generation_sites.py:50`); LightGBM quantile heads; handle `solar_forecast` (`lgbm_quantile_v1.yaml:101`).

Verdict: KEEP WITH FIXES. Rewrite the target and status.

## 7. GB merit-order stack entry

Says: "The GB supply curve for one settlement period: units ranked by short-run marginal cost, cumulative MW against GBP/MWh, floored at −500." "It is built when called, with nothing to train. It is scored through the SMP model, and its curves are kept in gold with each SMP run." Handle `models.stack.build(as_of)`.

Checks:
- Supply curve ranked by short-run marginal cost with cumulative capacity: correct (`src/gridflow_models/estimators/stack/model.py:126-146`; card `stack_gb_v1.md:11-17`).
- "floored at −500": correct (`configs/models/stack/gb_v1.yaml:9-10`). In the published headline the floor binds in 98 of 816 half-hours (gold `stack_clearing`, `price_mechanism = 'floor'`).
- "nothing to train": correct. `ConstructiveModel` has no `fit_one_fold` (`src/gridflow_models/core/protocols.py:47-55`).
- "curves are kept in gold with each SMP run": only when the backtest is run with `--publish` (card `stack_gb_v1.md:251-256`), and the 13 diagnostic runs wrote no supply points (`.planning/milestones/v2.0-RESULTS.md:187`). Say "with the published SMP run".
- The status per `models.list()` is `unregistered`, which is true of every configured model without a manifest row. The honest kind is "constructive".
- The copy omits that fuel and carbon prices are synthetic (`stack/gb_v1.yaml:24-28`). The SMP caption carries this; the stack text should too.

Fine: handle `models.stack.build(as_of)` (`src/gridflow_models/research/handles/model.py:1389`) and `.clear(as_of, demand_mw)` (:1398).

Verdict: KEEP WITH FIXES.

## 8. Fundamentals SMP entry and chart

Says: "Clears the stack against realised residual demand (demand less wind, solar and signed netting) for every half-hour, and scores the price against Elexon MID APXMIDP, the GB day-ahead benchmark." Table: headline 18 August to 3 September 2026, mean bias −151.80, MAE 151.80; 13 monthly runs, 5 May 2025 to 4 May 2026, mean bias −69.81, MAE 72.84. "In the headline run every period is under-predicted." Handle `models.fundamentals_smp.backtest(...)`. Chart of daily means with a caption naming perfect prognosis, synthetic fuel, the APXMIDP mix and the floor.

Scores (all real, reproduced from gold joined to silver `elexon/mid` APXMIDP, latest vintage per period):
- Headline run `41de423cfc0b421e`, policy `smp_headline_perfect_prog_v2`: mean bias −151.8012, MAE 151.8012, clearing below APXMIDP in every period. Matches the card (`fundamentals_smp_gb_v1.md:450-453`).
- Diagnostic, 13 runs under `smp_diagnostic_perfect_prog_v2`: mean bias −69.8117, MAE 72.8413. Matches the card (:453) and `v2.0-RESULTS.md:192-195`. The results file calls it "outage-blind" and "inventory-anachronistic", and says "It is not the headline" (`v2.0-RESULTS.md:196-197`). If it stays on the page it needs that caveat; otherwise cut the row.
- Chart: 17 daily means; model −136.0 to 78.4, APXMIDP 89.7 to 166.8. Matches the aria.

Wrong or stale:
- "816 periods" and "17,520 periods" are local counts; drop them from copy.
- The text never says the output is one price per half-hour. "Probabilistic" must not be claimed for the published run (finding B).
- "the GB day-ahead benchmark": gridflow's gold view is literally named `gold_gb_day_ahead_benchmark` (gridflow `src/gridflow/gold/views/gb_day_ahead_benchmark.sql:1-24`), and the caption already says APXMIDP mixes day-ahead and intraday. Fine together.

Fine: the realised-residual formula (`gb_v1.yaml:45-114`; card :50-65); perfect prognosis and synthetic fuel (card :468-471); the −500 floor; the no-op fit (`src/gridflow_models/estimators/fundamentals_smp/model.py:115-131`); the handle `backtest` (`research/handles/model.py:1647`).

Verdict: KEEP WITH FIXES. Add the one-price-per-half-hour sentence, drop the counts, and caveat or cut the diagnostic row.

## 9. "Reading the scores" and "In a notebook"

Says: every score is a backtest held in gold; pinball at q0.5 is half the MAE of the median, in MW; coverage is the share inside the 5 to 95% band; the demand gates are pinball ≤ 1,500 MW, coverage 0.90 ± 0.05 and no crossings. Code: `setup_notebook()`, `models.list()`.

Checks: all correct. Pinball at 0.5 is `0.5 × mean|y − q|` (`src/gridflow_models/validation/metrics.py:15`); the gates are at `configs/models/day_ahead/lgbm_demand_v1.yaml:77-84`; `setup_notebook` is at `src/gridflow_models/research/notebook_setup.py:278` and exported at `src/gridflow_models/__init__.py:5`; `models.list()` is at `research/handles/models.py:176`. Every score shown is in gold.

Note: the gates text covers demand only. Wind and solar use different gates (skill ≥ 0.05, median pinball ≤ 500 or 300 MW), and the SMP has no gates. That is fine while only demand and SMP scores show.

Verdict: KEEP. A candidate to fold into the demand block to declutter.

## 10. Footer

Not model content; not checked beyond the models link.

## Missing, and worth one line each

1. The published SMP output is one price per half-hour: realised inputs, degenerate quantiles (finding B).
2. Netting beyond wind and solar: signed hydro, ten interconnectors, OTHER and pumped storage come out of demand before clearing (`gb_v1.yaml:83-114`). This is the "signed netting" the draft mentions without explaining.
3. Demand v1 uses no weather at all. Its features are calendar terms plus demand already published by noon the day before (`day_ahead_lgbm_demand_v1.md:16-40`). That leakage discipline, per-row publication checks against the issue time, is the strongest recruiter signal in the repo. One line is worth it.

## Round-1 pack (`p27-r1/pack/TOPPAGES.md` section c) is stale on

- Wind and solar "What exists" (lines 354-355): both have now been scored and fell short of the coverage gate.
- Solar target "successor ... authorised, not yet configured" (line 355): now configured.
- The notebooks README (`notebooks/README.md:47-57`, last edited 2026-05-31) still says "trained" for wind and solar, and says SMP "loads four component models from the manifest". The latter is wrong for the published all-realised route (card `fundamentals_smp_gb_v1.md:31-35`: "constructs the stack directly from configuration without opening a manifest"). DESIGN.md names this README as the status source, but its model lines are stale; the code (`models.list()`, the manifest) wins.
