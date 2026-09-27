# Models page content pack

Built 2026-09-27 by claude-opus-5-5 from gridflow_models `main` at `1404300` and gridflow `master` at `2822d38`. Every score was reproduced read-only from its stored record (manifest, validation records, gold Parquet); the method and the corrections to the draft are in `models-content-check.md`. Machine-readable twin: `pack.json`, which also carries commit permalinks with line anchors. Source of both: `_build_pack.py` (edit and re-run; it lints the copy).

**Copy rules applied and checked by `_build_pack.py`:** no em or en dashes, no arrows, no middle dots, no planning words (planned, shipped, trained, live, in service, coming), no local row counts, no invented numbers; job lines up to 20 words. Links point at `main` of the private gridflow-models repo; paths marked local are gitignored stores and have no link. Red Hat Mono for everything in backticks.

**Two things to know before designing** (full reasoning in `models-content-check.md`):

1. The price chain runs from the recorded outturns, not from the forecast models. The SMP code can take forecasts, but the only published run used recorded demand, wind and solar, so it gives one price per half-hour. Draw the SMP cable from the three datasets, not from the three models.
2. Wind and solar were fitted and scored once on 2026-09-27 and failed the coverage gate. Ruling #15 (never trained) needs re-ruling; the status copy below assumes the recommended yes, and their scores are held.

## 1. Opening

**Headline.** From demand to a day-ahead price

**Lede.** gridflow-models is a separate Python library that reads gridflow's silver tables. It forecasts GB demand, wind and solar, builds the GB supply stack, and clears demand against that stack for a day-ahead price.

**The chain in one line.** Demand less wind and solar is residual demand; the price is where residual demand meets the supply stack.

**What the published run did.** The published price run uses recorded demand, wind and solar rather than the forecasts, so it gives one price per half-hour.

**Optional.** The price model also accepts the three forecasts in place of the recorded values.

**Scope line.** It produces forecasts and prices for research. It does not produce orders, positions or P&L.

Designer note (not copy): Headline drops the count on purpose: Bobbo asked for the chain, not five siblings (models-decisions.md).

Designer note (not copy): optional_capability_line describes code that exists (EstimatorInputConfig) but has never run; use it only if the page needs to explain why the forecast models sit above the price. Leave it out if in doubt.

Evidence:
- [`src/gridflow_models/data/gridflow_source.py:1-46`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/data/gridflow_source.py) (gridflow_models): training and backtests read gridflow silver Parquet directly, without importing gridflow
- [`src/gridflow_models/research/_pandas_client.py:1-26`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/research/_pandas_client.py) (gridflow_models): the notebook data surface wraps gridflow's GridflowClient over gridflow.duckdb
- [`CONTEXT.md:248-251`](https://github.com/EBentham/gridflow-models/blob/main/CONTEXT.md) (gridflow_models): the workbench produces forecasts and stack outputs; it does not produce orders, positions or P&L
- [`src/gridflow_models/estimators/fundamentals_smp/sampler.py:121-124`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/fundamentals_smp/sampler.py) (gridflow_models): residual = demand minus wind minus solar
- [`configs/models/fundamentals_smp/gb_v1.yaml:45-62`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/fundamentals_smp/gb_v1.yaml) (gridflow_models): published config: demand, wind and solar are kind: realised
- [`src/gridflow_models/backtest/smp_config.py:55-76`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/backtest/smp_config.py) (gridflow_models): a component may be realised or a registered estimator (model_id, version)

## 2. The chain, for the drawing

Designed chain (code): demand, wind and solar forecasts, sampled into residual demand, cleared through the stack for a probabilistic price. Published run: the three recorded outturns replace the forecasts, so the price is one value per half-hour.

**Drawing rule.** Draw only edges with exercised_in_published_run true. The SMP residual-demand cable branches off the same three datasets the forecast models learn from (elexon/indo, elexon/fuelhh, neso_data_portal/historic_generation_mix), not off the models. No dashed 'not yet' edges (DESIGN.md).

Confirmed: the stack is constructive with no learning; the SMP model has a no-op fit. The claim 'demand, wind and solar forecasts give residual demand, sampled and run through the stack for a probabilistic SMP' is true of the code path and false of the published run.

exercised_in_published_run: for edges into the SMP (residual demand, stack, benchmark), whether published run 41de423cfc0b421e used it; for every other edge, whether the model's stored scored run used it (demand in gold; wind and solar in -FAILED records).

| From | To | Label | Kind | Used in a stored run | Note |
|---|---|---|---|---|---|
| Substation | elexon/indo | national demand outturn | cable | yes |  |
| Substation | open_meteo/historical_demand | weather at seven city sites | cable | yes | version 2 only |
| Wind farm | elexon/fuelhh | metered wind | cable | yes |  |
| Wind farm | open_meteo/historical_wind | weather at twelve sites | cable | yes |  |
| Solar farm | neso_data_portal/historic_generation_mix | embedded solar estimate | cable | yes |  |
| Solar farm | open_meteo/historical_solar | weather at six sites | cable | yes |  |
| Power stations | elexon/bmunits_reference | unit register | cable | yes |  |
| Power stations | elexon/remit | outage notices | cable | yes |  |
| Power stations | elexon/fou2t14d | fuel-level availability | cable | yes |  |
| elexon/indo | Day-ahead demand | target and lags | feeds | yes | gold run a55a829bc51c40b2 (v1) |
| open_meteo/historical_demand | Day-ahead demand | weather (version 2) | feeds | yes | gold run b367a742aa544f8f (v2) |
| elexon/fuelhh | Wind generation | target (WIND) | feeds | yes | scored run failed the coverage gate; nothing in gold |
| open_meteo/historical_wind | Wind generation | weather | feeds | yes | as above |
| neso_data_portal/historic_generation_mix | Solar generation | target (solar) | feeds | yes | scored run failed the coverage gate; nothing in gold |
| open_meteo/historical_solar | Solar generation | weather | feeds | yes | as above |
| elexon/bmunits_reference | GB merit-order stack | units | feeds | yes |  |
| elexon/remit | GB merit-order stack | availability | feeds | yes |  |
| elexon/fou2t14d | GB merit-order stack | derating | feeds | yes | published run only; covers part of the window |
| Fuel and carbon prices (synthetic) | GB merit-order stack | marginal cost | feeds | yes | not a gridflow dataset; keep in text, not as a silver tap |
| elexon/indo | Residual demand | recorded demand | feeds | yes |  |
| elexon/fuelhh | Residual demand | recorded wind and signed netting | feeds | yes |  |
| neso_data_portal/historic_generation_mix | Residual demand | recorded solar | feeds | yes |  |
| Day-ahead demand | Residual demand | demand forecast | forecast_route | no | supported by code (EstimatorInputConfig); never run. Do not draw. |
| Wind generation | Residual demand | wind forecast | forecast_route | no | cannot run: no registered version. Do not draw. |
| Solar generation | Residual demand | solar forecast | forecast_route | no | cannot run: no registered version. Do not draw. |
| Residual demand | Fundamentals SMP | residual demand | feeds | yes | 1,000 draws; identical in the published run |
| GB merit-order stack | Fundamentals SMP | supply curve per half-hour | feeds | yes |  |
| elexon/mid (APXMIDP) | Fundamentals SMP | scored against | scored_against | yes |  |

## 3. The models

### 3.1 Day-ahead demand

- Model ids: `day_ahead.lgbm_demand.v1`, `day_ahead.lgbm_demand.v2`. Drawing: substation and pylons.
- **Job:** Forecasts GB national demand for every half-hour of the next day, as a spread of quantiles in MW.
- **Method:** LightGBM quantile regression, one model per quantile from 0.05 to 0.95, with a conformal widening of the outer band. Version 1 uses calendar terms and demand already published at issue time; version 2 adds weather.
- **Status as the code states it:** manifest `validated (v1: 21 versions, latest 20260829T184619Z; v2: 1 version, 20260903T202038Z)`; `models.list()` says `validated`; probabilistic estimator, fitted per walk-forward fold.
- **Status line (copy):** Both versions pass their gates and are validated. The scores come from stored walk-forward backtests.
- **Output:** Seven quantiles of demand per half-hour, in MW. Gold views: `gold_forecasts`, `gold_forecast_metrics`.
- **Workbench:** `models.demand_forecast`, `models.demand_forecast_v2`

| Input | gridflow view | Column / filter | Role | Cable |
|---|---|---|---|---|
| `elexon/indo` | `silver_elexon_indo` | initial_demand_outturn_mw | target, and demand lags published by noon the day before | yes |
| `open_meteo/historical_demand` | `silver_open_meteo_historical_demand` | temperature_2m_c, wind_speed_10m_mps | observed weather at seven city sites (Belfast weighted zero), standing in for a forecast | yes |
| `open_meteo/forecast_demand` | `silver_open_meteo_forecast_demand` | temperature_2m_c, wind_speed_10m_mps | forecast weather used only when v2 issues a forecast; not used by any score | no |

**Scores (real, with provenance):**

- Version 1: median pinball **711.04 MW**, 90% coverage **0.893**, gates pass. Window: 12 thirty-day test windows between 1 September 2024 and 22 August 2026.
  - Provenance: {"store": "gold forecast_metrics, scope run", "run_id": "a55a829bc51c40b2", "exact": {"pinball_q0.5": 711.043568003626, "coverage_nominal90": 0.8933414890742027}, "vintage_kind": "issued", "vintage_policy_id": "v1_day_anchored_noon_d1", "manifest_version": "20260827T081123Z (20260829T184619Z re-registers identical metrics)", "record": "data/models/day_ahead_lgbm_demand_v1/20260827T081123Z/validation_record.json"}
- Version 2: median pinball **599.72 MW**, 90% coverage **0.883**, gates pass. Window: the same 12 test windows.
  - Caveat (copy): Version 2 is scored with observed weather standing in for the forecast, so its score is optimistic.
  - Provenance: {"store": "gold forecast_metrics, scope run", "run_id": "b367a742aa544f8f", "exact": {"pinball_q0.5": 599.7244473831543, "coverage_nominal90": 0.8830351340308341}, "vintage_kind": "perfect_prog", "vintage_policy_id": "v2_perfect_prog_day_anchored_noon_d1", "note": "The registered v2 version 20260903T202038Z scores 584.89 / 0.890 in its own record; the card derives no metric from it. Show 599.72."}

Evidence:
- [`configs/models/day_ahead/lgbm_demand_v1.yaml:10-38`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/day_ahead/lgbm_demand_v1.yaml) (gridflow_models): target elexon/indo; quantiles 0.05 to 0.95; CQR calibration
- [`configs/models/day_ahead/lgbm_demand_v1.yaml:77-84`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/day_ahead/lgbm_demand_v1.yaml) (gridflow_models): gates: pinball q0.5 at most 1500 MW, coverage 0.90 within 0.05, monotonicity
- [`configs/models/day_ahead/lgbm_demand_v2.yaml:16-49`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/day_ahead/lgbm_demand_v2.yaml) (gridflow_models): adds open_meteo/historical_demand (scored) and open_meteo/forecast_demand (issuing)
- [`docs/MODEL_CARDS/day_ahead_lgbm_demand_v1.md:16-40`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/day_ahead_lgbm_demand_v1.md) (gridflow_models): v1 features: calendar and issue-legal demand lags, no weather
- [`docs/MODEL_CARDS/day_ahead_lgbm_demand_v1.md:246-285`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/day_ahead_lgbm_demand_v1.md) (gridflow_models): 711.043568 / 0.893341 is the headline, published as gold run a55a829bc51c40b2
- [`docs/MODEL_CARDS/day_ahead_lgbm_demand_v2.md:20-53`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/day_ahead_lgbm_demand_v2.md) (gridflow_models): perfect-prognosis caveat; 599.724447 / 0.883035, run b367a742aa544f8f
- [`docs/MODEL_CARDS/day_ahead_lgbm_demand_v2.md:74-100`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/day_ahead_lgbm_demand_v2.md) (gridflow_models): v2 additions: population-weighted weather, effective temperature, season term
- [`src/gridflow_models/estimators/day_ahead/weather_assembly.py:72`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/day_ahead/weather_assembly.py) (gridflow_models): WEATHER_SITES: seven sites
- `data/models/day_ahead_lgbm_demand_v1/20260827T081123Z/validation_record.json` (local (gitignored, read only)): 711.043568, 0.893341, gates pass
- `C:/gridflow-data/gold/forecast_metrics/` (local (gitignored, read only)): runs a55a829bc51c40b2 and b367a742aa544f8f, scope run

### 3.2 Wind generation

- Model ids: `wind.lgbm_quantile.v1`. Drawing: wind farm.
- **Job:** Forecasts GB metered wind output for every half-hour of the next day, from weather at twelve wind farm sites.
- **Method:** LightGBM quantile regression on hub-height wind speed, direction and air density at twelve sites, scored against a fitted power-curve baseline. Elexon's WINDFOR forecast is kept as a reference.
- **Status as the code states it:** manifest `none (no manifest row)`; `models.list()` says `unregistered`; probabilistic estimator; one fitting run on 2026-09-27 failed the coverage gate (-FAILED artefact).
- **Status line (copy):** Scored once in a walk-forward backtest. Its 90% band was too narrow to pass the coverage gate, so no version is registered.
  - Designer note: Pending Bobbo's re-ruling of #15 (its 'never trained' premise is now false). See models-content-check.md, finding A.
- **Output:** Seven quantiles of wind output per half-hour, in MW. Nothing in gold.
- **Workbench:** `models.wind_forecast`

| Input | gridflow view | Column / filter | Role | Cable |
|---|---|---|---|---|
| `elexon/fuelhh` | `silver_elexon_fuelhh` | generation_mw ; fuel_type = WIND | target: metered, post-curtailment GB wind | yes |
| `open_meteo/historical_wind` | `silver_open_meteo_historical_wind` | 10 m and 100 m wind speed, 100 m direction, air density | observed weather at twelve sites (eight offshore, four onshore), standing in for a forecast | yes |
| `elexon/windfor` | `silver_elexon_windfor` | latest_forecast_mw | reference only: Elexon's own wind forecast, compared in the evidence report, never a model input | no |

**Scores:** none on the page.

**Held, not copy** (gate-failing run, not registered, nothing in gold; ruling #15 needs re-ruling first): median pinball 416.7 MW, 90% coverage 0.722, skill over baseline 0.161; skill pass, median pinball pass (limit 500), coverage FAIL (0.90 within 0.05), monotonicity pass; 8 thirty-day folds, 2 October 2021 to 25 September 2026, perfect prognosis; record `data/models/wind_lgbm_quantile_v1/20260927T145057Z-FAILED/validation_record.json`.

Evidence:
- [`configs/models/wind/lgbm_quantile_v1.yaml:10-37`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/wind/lgbm_quantile_v1.yaml) (gridflow_models): target elexon/fuelhh WIND; features open_meteo/historical_wind
- [`configs/models/wind/lgbm_quantile_v1.yaml:56-60`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/wind/lgbm_quantile_v1.yaml) (gridflow_models): baseline: binned power curve on fleet_v100adj_mean
- [`configs/models/wind/lgbm_quantile_v1.yaml:80-99`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/wind/lgbm_quantile_v1.yaml) (gridflow_models): gates (skill, pinball 500, coverage, monotonicity); WINDFOR under benchmarks
- [`src/gridflow_models/features/generation_sites.py:29`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/features/generation_sites.py) (gridflow_models): WIND_SITES: twelve sites
- [`docs/MODEL_CARDS/wind_lgbm_quantile_v1.md:21-46`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/wind_lgbm_quantile_v1.md) (gridflow_models): results: failed on coverage only, no manifest row; WINDFOR not like-for-like
- [`.planning/phases/v2.3-H-2-wind-trained/receipts/WIND-TRAIN.md`](https://github.com/EBentham/gridflow-models/blob/main/.planning/phases/v2.3-H-2-wind-trained/receipts/WIND-TRAIN.md) (gridflow_models): seat receipt of the real-store run
- [`src/gridflow_models/research/handles/models.py:176-222`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/research/handles/models.py) (gridflow_models): models.list(): no manifest entry means status 'unregistered'
- `data/models/wind_lgbm_quantile_v1/20260927T145057Z-FAILED/validation_record.json` (local (gitignored, read only)): 416.70, 0.7220, skill 0.1612; passes_gates false

### 3.3 Solar generation

- Model ids: `solar.lgbm_quantile.v1`. Drawing: solar farm.
- **Job:** Forecasts GB embedded solar output for every half-hour of the next day, from weather at six solar sites.
- **Method:** LightGBM quantile regression on irradiance, cloud and sun position at six sites, fitted and scored on daylight half-hours against an irradiance-curve baseline. The target is NESO's estimate of embedded solar, not every GB solar generator.
- **Status as the code states it:** manifest `none (no manifest row)`; `models.list()` says `unregistered`; probabilistic estimator; one fitting run on 2026-09-27 failed the coverage gate (-FAILED artefact).
- **Status line (copy):** Scored once in a walk-forward backtest. Its 90% band was too narrow to pass the coverage gate, so no version is registered.
  - Designer note: Pending Bobbo's re-ruling of #15. See models-content-check.md, finding A.
- **Output:** Seven quantiles of solar output per half-hour, in MW. Nothing in gold.
- **Workbench:** `models.solar_forecast`

| Input | gridflow view | Column / filter | Role | Cable |
|---|---|---|---|---|
| `neso_data_portal/historic_generation_mix` | `silver_neso_data_portal_historic_generation_mix (also silver_neso_data_portal_historic_generation_mix_latest)` | solar ; one pinned capture (published_at 2026-09-26T18:19:36Z) | target: NESO's embedded solar estimate | yes |
| `open_meteo/historical_solar` | `silver_open_meteo_historical_solar` | irradiance (GHI, DNI, diffuse, GTI), temperature, cloud cover | observed weather at six sites, standing in for a forecast | yes |

**Scores:** none on the page.

**Held, not copy** (gate-failing run, not registered, nothing in gold; ruling #15 needs re-ruling first): median pinball 290.4 MW, 90% coverage 0.712, skill over baseline 0.193; skill pass, median pinball pass (limit 300, daylight rows), coverage FAIL, monotonicity pass; 8 thirty-day folds, 2 October 2021 to 25 September 2026, daylight rows only, perfect prognosis; record `data/models/solar_lgbm_quantile_v1/20260927T183348Z-FAILED/validation_record.json`.

Evidence:
- [`configs/models/solar/lgbm_quantile_v1.yaml:16-45`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/solar/lgbm_quantile_v1.yaml) (gridflow_models): target neso_data_portal/historic_generation_mix solar, pinned; open_meteo/historical_solar
- [`configs/models/solar/lgbm_quantile_v1.yaml:61-69`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/solar/lgbm_quantile_v1.yaml) (gridflow_models): daylight scoring mask; binned irradiance-curve baseline
- [`configs/models/solar/lgbm_quantile_v1.yaml:89-99`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/solar/lgbm_quantile_v1.yaml) (gridflow_models): gates: skill, pinball 300, coverage, monotonicity; no benchmarks block
- [`src/gridflow_models/features/generation_sites.py:50`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/features/generation_sites.py) (gridflow_models): SOLAR_SITES: six sites
- [`docs/MODEL_CARDS/solar_lgbm_quantile_v1.md:1-20`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/solar_lgbm_quantile_v1.md) (gridflow_models): status and target provenance; NESO series is embedded solar
- [`docs/MODEL_CARDS/solar_lgbm_quantile_v1.md:86-120`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/solar_lgbm_quantile_v1.md) (gridflow_models): results: failed on coverage only, no manifest row
- [`.planning/phases/v2.3-H-3-solar-trained/receipts/SOLAR-TRAIN.md`](https://github.com/EBentham/gridflow-models/blob/main/.planning/phases/v2.3-H-3-solar-trained/receipts/SOLAR-TRAIN.md) (gridflow_models): seat receipt of the real-store run
- `data/models/solar_lgbm_quantile_v1/20260927T183348Z-FAILED/validation_record.json` (local (gitignored, read only)): 290.37, 0.7124, skill 0.1930; passes_gates false

### 3.4 GB merit-order stack

- Model ids: `stack.gb.v1`. Drawing: the plant fleet: biomass, nuclear, CCGT, OCGT.
- **Job:** Builds the GB supply curve for one half-hour: available plant ranked by short-run marginal cost, in cumulative MW.
- **Method:** Built on request from the unit register, outage notices and fuel prices, with nothing to fit. Fuel and carbon prices are synthetic. Clearing prices are floored at −500 GBP/MWh.
- **Status as the code states it:** manifest `none (constructive models are not registered)`; `models.list()` says `unregistered`; constructive (ConstructiveModel: build(), no fit_one_fold).
- **Status line (copy):** Constructive: it is rebuilt for each half-hour and has no parameters to fit.
- **Output:** A supply curve: each unit's available MW and marginal cost, sorted, with cumulative MW. Gold views: `gold_stack_supply_curve_points (written with the published SMP run)`.
- **Workbench:** `models.stack.build(as_of)`, `models.stack.clear(as_of, demand_mw)`

| Input | gridflow view | Column / filter | Role | Cable |
|---|---|---|---|---|
| `elexon/bmunits_reference` | `silver_elexon_bmunits_reference` |  | unit register: identity, technology and capacity | yes |
| `elexon/remit` | `silver_elexon_remit (also silver_elexon_remit_latest)` |  | outage notices known at decision time, which cut unit availability | yes |
| `elexon/fou2t14d` | `silver_elexon_fou2t14d (also silver_elexon_fou2t14d_latest)` |  | fuel-level availability, used to derate units in the published run where it covers the period | yes |
| `entsoe/installed_capacity_units` | `silver_entsoe_installed_capacity_units` |  | logged cross-check only; its keys do not match Elexon units, so it never shapes the curve | no |
| `data/manual/commodities.csv (not a gridflow dataset)` | n/a |  | gas, coal and carbon prices, synthetic | no |
| `configs/engineering/plant_technology.yaml (not a gridflow dataset)` | n/a |  | efficiency, emissions and fuel per technology | no |

**Scores:** No score of its own. It is scored only through the SMP model.

Evidence:
- [`src/gridflow_models/estimators/stack/model.py:1-16`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/stack/model.py) (gridflow_models): constructive merit-order supply curve
- [`src/gridflow_models/estimators/stack/model.py:126-146`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/stack/model.py) (gridflow_models): build: plant universe, fuel prices, marginal cost, sort and cumsum
- [`src/gridflow_models/core/protocols.py:47-55`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/core/protocols.py) (gridflow_models): ConstructiveModel: built from inputs, no fit_one_fold
- [`configs/models/stack/gb_v1.yaml:9-43`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/stack/gb_v1.yaml) (gridflow_models): floor −500; inputs; commodity prices labelled synthetic; zero fuel for biomass and nuclear
- [`src/gridflow_models/estimators/stack/plant_universe.py:1-10`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/stack/plant_universe.py) (gridflow_models): four datasets read
- [`src/gridflow_models/estimators/stack/plant_universe.py:1078-1100`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/stack/plant_universe.py) (gridflow_models): ENTSO-E cross-check is log-only and cannot match keys
- [`configs/backtest/price_formation_ladder_v2.yaml:31-37`](https://github.com/EBentham/gridflow-models/blob/main/configs/backtest/price_formation_ladder_v2.yaml) (gridflow_models): FOU2T14D derating profile used by the published headline
- [`docs/MODEL_CARDS/stack_gb_v1.md:251-260`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/stack_gb_v1.md) (gridflow_models): publication is opt-in with --publish
- [`src/gridflow_models/research/handles/model.py:1389-1398`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/research/handles/model.py) (gridflow_models): workbench build(as_of) and clear(as_of, demand_mw)

### 3.5 Fundamentals SMP

- Model ids: `fundamentals_smp.gb.v1`. Drawing: stack crossed by a demand line (the draft's smp mark).
- **Job:** Clears residual demand against the stack every half-hour for a GB day-ahead price, scored against Elexon's market index.
- **Method:** Residual demand is demand less wind and solar, less signed hydro, interconnector, OTHER and pumped storage flows. The price is the marginal cost where that demand meets the stack, floored at −500 GBP/MWh.
- **Status as the code states it:** manifest `none`; `models.list()` says `unregistered`; hybrid probabilistic estimator with a no-op fit; published backtest runs in gold.
- **Status line (copy):** It has nothing to fit. Its published run clears recorded demand, wind and solar, so each half-hour gets one price, not a spread.
- **Output:** A price per half-hour in GBP/MWh, as seven quantiles; in the published run all seven are equal. Gold views: `gold_stack_clearing`, `gold_stack_residual_demand`, `gold_stack_supply_curve_points`.
- **Workbench:** `models.fundamentals_smp.backtest(...)`

| Input | gridflow view | Column / filter | Role | Cable |
|---|---|---|---|---|
| `elexon/indo` | `silver_elexon_indo` | initial_demand_outturn_mw | recorded demand | yes |
| `elexon/fuelhh` | `silver_elexon_fuelhh` | generation_mw | recorded wind, plus signed hydro, ten interconnectors, OTHER and pumped storage | yes |
| `neso_data_portal/historic_generation_mix` | `silver_neso_data_portal_historic_generation_mix (also silver_neso_data_portal_historic_generation_mix_latest)` | solar | recorded embedded solar | yes |
| `stack.gb.v1 (model)` | n/a |  | supply curve for each half-hour | yes |
| `elexon/mid` | `silver_elexon_mid; gold_gb_day_ahead_benchmark` | market_index_price ; data_provider_id = APXMIDP | the price it is scored against | yes |

**Scores (real, with provenance):**

- Published run: mean bias **-151.80**, MAE **151.80** GBP/MWh. Window: 18 August to 3 September 2026, every half-hour.
  - Copy: Every half-hour clears below the market index.
  - Caveat (copy): A perfect-prognosis backtest: recorded demand, wind and solar stand in for forecasts.
  - Caveat (copy): Fuel and carbon prices are synthetic.
  - Caveat (copy): APXMIDP mixes day-ahead and intraday trades.
  - Caveat (copy): Clearing is floored at −500 GBP/MWh, which pulls some daily means below zero.
  - Provenance: {"store": "gold stack_clearing joined to silver elexon/mid APXMIDP (latest per period)", "run_id": "41de423cfc0b421e", "vintage_policy_id": "smp_headline_perfect_prog_v2", "exact": {"mean_bias": -151.8012, "mae": 151.8012, "median_bias": -95.3409}, "periods_scored": 816, "periods_below_benchmark": 816, "floor_binding_periods": 98, "card": "docs/MODEL_CARDS/fundamentals_smp_gb_v1.md:443-453"}
- Year diagnostic: mean bias **-69.81**, MAE **72.84** GBP/MWh. Window: 5 May 2025 to 4 May 2026, in monthly runs.
  - Caveat (copy): A diagnostic that sees almost no outages and uses one fixed plant register for the whole year, so it is not the headline.
  - Use: optional; recommended cut to declutter, or show only with its caveat
  - Provenance: {"store": "gold stack_clearing, 13 runs", "vintage_policy_id": "smp_diagnostic_perfect_prog_v2", "exact": {"mean_bias": -69.8117, "mae": 72.8413}, "periods_scored": 17520, "results": ".planning/milestones/v2.0-RESULTS.md:190-197"}

Evidence:
- [`src/gridflow_models/estimators/fundamentals_smp/model.py:1-18`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/fundamentals_smp/model.py) (gridflow_models): combines demand, wind, solar and stack; no-op fit (ADR-038)
- [`src/gridflow_models/estimators/fundamentals_smp/model.py:115-131`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/fundamentals_smp/model.py) (gridflow_models): fit_one_fold records component hashes only
- [`src/gridflow_models/estimators/fundamentals_smp/model.py:137-146`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/fundamentals_smp/model.py) (gridflow_models): predict: component quantiles, N residual draws, stack per period, clear, quantiles
- [`src/gridflow_models/estimators/fundamentals_smp/model.py:217-285`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/fundamentals_smp/model.py) (gridflow_models): the inference loop
- [`src/gridflow_models/estimators/fundamentals_smp/sampler.py:1-11`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/fundamentals_smp/sampler.py) (gridflow_models): Monte Carlo residual demand under marginal independence
- [`src/gridflow_models/estimators/fundamentals_smp/sampler.py:125-177`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/fundamentals_smp/sampler.py) (gridflow_models): inverse-CDF sampling; flat quantiles give identical draws
- [`src/gridflow_models/estimators/fundamentals_smp/realised.py:36-79`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/estimators/fundamentals_smp/realised.py) (gridflow_models): realised adapter: every quantile equals the observed value
- [`src/gridflow_models/backtest/smp_runtime.py:778-808`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/backtest/smp_runtime.py) (gridflow_models): realised roles use the adapter; estimator roles need a registered bundle
- [`configs/models/fundamentals_smp/gb_v1.yaml:45-122`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/fundamentals_smp/gb_v1.yaml) (gridflow_models): realised components, 1,000 draws, signed netting, APXMIDP target
- [`docs/MODEL_CARDS/fundamentals_smp_gb_v1.md:21-35`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/fundamentals_smp_gb_v1.md) (gridflow_models): headline route is all-realised and opens no manifest
- [`docs/MODEL_CARDS/fundamentals_smp_gb_v1.md:71-73`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/fundamentals_smp_gb_v1.md) (gridflow_models): degenerate quantiles: coverage does not establish calibration
- [`docs/MODEL_CARDS/fundamentals_smp_gb_v1.md:443-477`](https://github.com/EBentham/gridflow-models/blob/main/docs/MODEL_CARDS/fundamentals_smp_gb_v1.md) (gridflow_models): v2.0 published headline and limitations
- [`src/gridflow/gold/views/gb_day_ahead_benchmark.sql:1-24`](https://github.com/EBentham/gridflow/blob/master/src/gridflow/gold/views/gb_day_ahead_benchmark.sql) (gridflow): gold view over Elexon MID APXMIDP
- `C:/gridflow-data/gold/stack_clearing/` (local (gitignored, read only)): run 41de423cfc0b421e and 13 diagnostic runs, reproduced

## 4. Reading the scores

Every score here is a backtest held in gold. Pinball loss at the median is half the mean absolute error of the median forecast, in MW. Coverage is the share of outturns inside the 5 to 95% band. A demand version passes when median pinball is at most 1,500 MW, coverage is within 0.05 of 0.90 and no quantiles cross. Price scores are in GBP/MWh against Elexon's APXMIDP market index.

Designer note: a candidate to fold into the demand block to declutter.

Evidence:
- [`src/gridflow_models/validation/metrics.py:15`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/validation/metrics.py) (gridflow_models): pinball_loss
- [`configs/models/day_ahead/lgbm_demand_v1.yaml:77-84`](https://github.com/EBentham/gridflow-models/blob/main/configs/models/day_ahead/lgbm_demand_v1.yaml) (gridflow_models): demand gates

## 5. Charts

**Demand forecast against outturn, 20 and 21 August 2026** (demand_band)

- Caption (copy): Version 1: the median inside its 5 to 95% band, and the outturn from elexon/indo. Issued at noon UTC the day before.
- Data: gold forecasts, run a55a829bc51c40b2, fold 12; unit MW; window 2026-08-20T00:00Z to 2026-08-21T23:30Z; 96 points; arrays in `p27-r1/pack/toppages.json series.models_landing_demand`.
- Verified: 96 rows; values 17,466 to 31,583 MW; issued_at 12:00 UTC on the previous day.

**Daily mean price, 18 August to 3 September 2026** (smp_daily)

- Caption (copy): Model clearing against APXMIDP, daily means of every half-hour in the published run. Recorded demand, wind and solar stand in for forecasts; fuel and carbon prices are synthetic; APXMIDP mixes day-ahead and intraday trades; the −500 GBP/MWh floor pulls some daily means below zero.
- Data: gold stack_clearing run 41de423cfc0b421e joined to silver elexon/mid APXMIDP; unit GBP/MWh; window 2026-08-18 to 2026-09-03; 17 points; arrays in `p27-r1/pack/toppages.json series.models_landing_smp`.
- Verified: model daily means −136.0 to 78.4; APXMIDP 89.7 to 166.8.

## 6. In a notebook

```python
from gridflow_models import setup_notebook
data, models, common = setup_notebook()
models.list()
```

models.list() shows demand v1 and v2 as validated and the other four as unregistered, which matches this pack.

Evidence:
- [`src/gridflow_models/research/notebook_setup.py:278`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/research/notebook_setup.py) (gridflow_models): setup_notebook
- [`src/gridflow_models/__init__.py:5`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/__init__.py) (gridflow_models): exported at package top level
- [`src/gridflow_models/research/handles/models.py:176-222`](https://github.com/EBentham/gridflow-models/blob/main/src/gridflow_models/research/handles/models.py) (gridflow_models): models.list() columns and status rule

## 7. Needs a ruling

- DESIGN.md says model status truth lives in gridflow_models notebooks/README.md, but its model lines (last edited 2026-05-31) are stale: wind and solar 'trained', SMP 'loads four component models from the manifest'. This pack takes status from the manifest and models.list() instead. Let code and manifest win until the README is fixed? Recommended: **yes**. Copy if yes: "No copy change; the status lines in this pack already follow the code." (models-content-check.md, last section; DESIGN.md content rules)
- Ruling #15 says wind and solar are shown as never trained. Since 2026-09-27 15:46 both were fitted and scored once and failed the coverage gate (no manifest row, nothing in gold). Show them as unregistered, scored once, with the scores held off the page? Recommended: **yes**. Copy if yes: "Scored once in a walk-forward backtest. Its 90% band was too narrow to pass the coverage gate, so no version is registered." (models-content-check.md finding A; gridflow_models RULINGS #1001, #1006, #1007)

## 8. Unverified (keep off the page)

- APXMIDP's exact vendor definition (the SMP card says its contemporary definition is unverified). Say only that it mixes day-ahead and intraday trades.
- That NESO's embedded solar series is PV_Live-derived: a deduction in the solar card, not a vendor statement. Keep it off the page.
- How well twelve wind sites and six solar sites represent the GB fleet: the cards call it unestablished. No representativeness claim.
- FOU2T14D and REMIT historical reach depends on a vendor backfill the SMP card calls unverified. Do not claim full outage coverage.
- The v2 demand gain (about 15.7%) is one run with no significance test and is an upper bound under perfect prognosis. Do not print it as an improvement figure.
- notebooks/README.md model lines (last edited 2026-05-31) say wind and solar are 'trained' and SMP 'loads four component models from the manifest'. Both are stale against the code. Do not quote.
