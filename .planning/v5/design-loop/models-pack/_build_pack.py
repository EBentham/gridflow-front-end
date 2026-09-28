"""Build the Models page content pack (pack.json and MODELS-PACK.md) from one source.

Edit the data here and re-run: `python _build_pack.py`. The script lints every copy field
(no em or en dashes, arrows, middle dots, planning words; job lines up to 20 words) and
fails loudly if a rule breaks. Evidence and provenance fields are not copy and are not linted.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
GM = "https://github.com/EBentham/gridflow-models/blob/main/"
GF = "https://github.com/EBentham/gridflow/blob/master/"
GM_COMMIT = "1404300601dac6c28f107fea5152f8cb3ca4e88e"
GF_COMMIT = "2822d38952937ebb7ebad3d0f92abda644514408"


def ev(path: str, lines: str | None, note: str, repo: str = "gm") -> dict[str, str]:
    """One evidence item with a GitHub link (line anchors when given)."""
    base = GM if repo == "gm" else GF
    commit = GM_COMMIT if repo == "gm" else GF_COMMIT
    anchor = ""
    if lines:
        a, _, b = lines.partition("-")
        anchor = f"#L{a}" + (f"-L{b}" if b else "")
    root = base.split("/blob/")[0]
    return {
        "repo": "gridflow_models" if repo == "gm" else "gridflow",
        "path": path,
        "lines": lines or "",
        "note": note,
        "url": f"{base}{path}",
        "permalink": f"{root}/blob/{commit}/{path}{anchor}",
    }


def local(path: str, note: str) -> dict[str, str]:
    """A local, gitignored record (manifest, artefact store, gold). No link: it is not in the repo."""
    return {"repo": "local (gitignored, read only)", "path": path, "lines": "", "note": note, "url": "", "permalink": ""}


def view(source: str, dataset: str, latest: bool = False) -> str:
    v = f"silver_{source}_{dataset}"
    return v + (f" (also {v}_latest)" if latest else "")


# ---------------------------------------------------------------- opening
OPENING = {
    "headline": "From demand to a day-ahead price",
    "lede": ("gridflow-models is a separate Python library that reads gridflow's silver tables. It forecasts GB "
             "demand, wind and solar, builds the GB supply stack, and clears demand against that stack for a "
             "day-ahead price."),
    "chain_line": ("Demand less wind and solar is residual demand; the price is where residual demand meets the "
                   "supply stack."),
    "published_run_line": ("The published price run uses recorded demand, wind and solar rather than the "
                           "forecasts, so it gives one price per half-hour."),
    "optional_capability_line": "The price model also accepts the three forecasts in place of the recorded values.",
    "scope": "It produces forecasts and prices for research. It does not produce orders, positions or P&L.",
    "notes": [
        "Headline drops the count on purpose: Bobbo asked for the chain, not five siblings (models-decisions.md).",
        "optional_capability_line describes code that exists (EstimatorInputConfig) but has never run; use it only "
        "if the page needs to explain why the forecast models sit above the price. Leave it out if in doubt.",
    ],
    "evidence": [
        ev("src/gridflow_models/data/gridflow_source.py", "1-46", "training and backtests read gridflow silver Parquet directly, without importing gridflow"),
        ev("src/gridflow_models/research/_pandas_client.py", "1-26", "the notebook data surface wraps gridflow's GridflowClient over gridflow.duckdb"),
        ev("CONTEXT.md", "248-251", "the workbench produces forecasts and stack outputs; it does not produce orders, positions or P&L"),
        ev("src/gridflow_models/estimators/fundamentals_smp/sampler.py", "121-124", "residual = demand minus wind minus solar"),
        ev("configs/models/fundamentals_smp/gb_v1.yaml", "45-62", "published config: demand, wind and solar are kind: realised"),
        ev("src/gridflow_models/backtest/smp_config.py", "55-76", "a component may be realised or a registered estimator (model_id, version)"),
    ],
}

# ---------------------------------------------------------------- shared evidence
SMP_MODEL = "src/gridflow_models/estimators/fundamentals_smp/model.py"

MODELS = [
    {
        "id": "demand",
        "name": "Day-ahead demand",
        "model_ids": ["day_ahead.lgbm_demand.v1", "day_ahead.lgbm_demand.v2"],
        "drawing": "substation and pylons",
        "job": "Forecasts GB national demand for every half-hour of the next day, as a spread of quantiles in MW.",
        "method": ("LightGBM quantile regression, one model per quantile from 0.05 to 0.95, with a conformal "
                   "widening of the outer band. Version 1 uses calendar terms and demand already published at "
                   "issue time; version 2 adds weather."),
        "status_code": {
            "manifest_status": "validated (v1: 21 versions, latest 20260829T184619Z; v2: 1 version, 20260903T202038Z)",
            "models_list": "validated",
            "kind": "probabilistic estimator, fitted per walk-forward fold",
        },
        "status_line": "Both versions pass their gates and are validated. The scores come from stored walk-forward backtests.",
        "inputs": [
            {"dataset": "elexon/indo", "gridflow_view": view("elexon", "indo"), "column": "initial_demand_outturn_mw",
             "role": "target, and demand lags published by noon the day before", "versions": "v1, v2", "cable": True},
            {"dataset": "open_meteo/historical_demand", "gridflow_view": view("open_meteo", "historical_demand"),
             "column": "temperature_2m_c, wind_speed_10m_mps",
             "role": "observed weather at seven city sites (Belfast weighted zero), standing in for a forecast",
             "versions": "v2", "cable": True},
            {"dataset": "open_meteo/forecast_demand", "gridflow_view": view("open_meteo", "forecast_demand"),
             "column": "temperature_2m_c, wind_speed_10m_mps",
             "role": "forecast weather used only when v2 issues a forecast; not used by any score", "versions": "v2",
             "cable": False},
        ],
        "output": {"copy": "Seven quantiles of demand per half-hour, in MW.",
                   "gold_views": ["gold_forecasts", "gold_forecast_metrics"]},
        "handles": ["models.demand_forecast", "models.demand_forecast_v2"],
        "scores": [
            {"label": "Version 1", "pinball_q0_5_mw": 711.04, "coverage_90": 0.893, "gates": "pass",
             "window_copy": "12 thirty-day test windows between 1 September 2024 and 22 August 2026",
             "provenance": {"store": "gold forecast_metrics, scope run", "run_id": "a55a829bc51c40b2",
                            "exact": {"pinball_q0.5": 711.043568003626, "coverage_nominal90": 0.8933414890742027},
                            "vintage_kind": "issued", "vintage_policy_id": "v1_day_anchored_noon_d1",
                            "manifest_version": "20260827T081123Z (20260829T184619Z re-registers identical metrics)",
                            "record": "data/models/day_ahead_lgbm_demand_v1/20260827T081123Z/validation_record.json"}},
            {"label": "Version 2", "pinball_q0_5_mw": 599.72, "coverage_90": 0.883, "gates": "pass",
             "window_copy": "the same 12 test windows",
             "caveat_copy": "Version 2 is scored with observed weather standing in for the forecast, so its score is optimistic.",
             "provenance": {"store": "gold forecast_metrics, scope run", "run_id": "b367a742aa544f8f",
                            "exact": {"pinball_q0.5": 599.7244473831543, "coverage_nominal90": 0.8830351340308341},
                            "vintage_kind": "perfect_prog", "vintage_policy_id": "v2_perfect_prog_day_anchored_noon_d1",
                            "note": ("The registered v2 version 20260903T202038Z scores 584.89 / 0.890 in its own record; "
                                     "the card derives no metric from it. Show 599.72.")}},
        ],
        "held": [],
        "evidence": [
            ev("configs/models/day_ahead/lgbm_demand_v1.yaml", "10-38", "target elexon/indo; quantiles 0.05 to 0.95; CQR calibration"),
            ev("configs/models/day_ahead/lgbm_demand_v1.yaml", "77-84", "gates: pinball q0.5 at most 1500 MW, coverage 0.90 within 0.05, monotonicity"),
            ev("configs/models/day_ahead/lgbm_demand_v2.yaml", "16-49", "adds open_meteo/historical_demand (scored) and open_meteo/forecast_demand (issuing)"),
            ev("docs/MODEL_CARDS/day_ahead_lgbm_demand_v1.md", "16-40", "v1 features: calendar and issue-legal demand lags, no weather"),
            ev("docs/MODEL_CARDS/day_ahead_lgbm_demand_v1.md", "246-285", "711.043568 / 0.893341 is the headline, published as gold run a55a829bc51c40b2"),
            ev("docs/MODEL_CARDS/day_ahead_lgbm_demand_v2.md", "20-53", "perfect-prognosis caveat; 599.724447 / 0.883035, run b367a742aa544f8f"),
            ev("docs/MODEL_CARDS/day_ahead_lgbm_demand_v2.md", "74-100", "v2 additions: population-weighted weather, effective temperature, season term"),
            ev("src/gridflow_models/estimators/day_ahead/weather_assembly.py", "72", "WEATHER_SITES: seven sites"),
            local("data/models/day_ahead_lgbm_demand_v1/20260827T081123Z/validation_record.json", "711.043568, 0.893341, gates pass"),
            local("C:/gridflow-data/gold/forecast_metrics/", "runs a55a829bc51c40b2 and b367a742aa544f8f, scope run"),
        ],
    },
    {
        "id": "wind",
        "name": "Wind generation",
        "model_ids": ["wind.lgbm_quantile.v1"],
        "drawing": "wind farm",
        "job": "Forecasts GB metered wind output for every half-hour of the next day, from weather at twelve wind farm sites.",
        "method": ("LightGBM quantile regression on hub-height wind speed, direction and air density at twelve "
                   "sites, scored against a fitted power-curve baseline. Elexon's WINDFOR forecast is kept as a "
                   "reference."),
        "status_code": {
            "manifest_status": "none (no manifest row)",
            "models_list": "unregistered",
            "kind": "probabilistic estimator; one fitting run on 2026-09-27 failed the coverage gate (-FAILED artefact)",
        },
        "status_line": ("Scored once in a walk-forward backtest. Its 90% band was too narrow to pass the coverage "
                        "gate, so no version is registered."),
        "status_line_note": "Pending Bobbo's re-ruling of #15 (its 'never trained' premise is now false). See models-content-check.md, finding A.",
        "inputs": [
            {"dataset": "elexon/fuelhh", "gridflow_view": view("elexon", "fuelhh"), "column": "generation_mw",
             "filter": "fuel_type = WIND", "role": "target: metered, post-curtailment GB wind", "cable": True},
            {"dataset": "open_meteo/historical_wind", "gridflow_view": view("open_meteo", "historical_wind"),
             "column": "10 m and 100 m wind speed, 100 m direction, air density",
             "role": "observed weather at twelve sites (eight offshore, four onshore), standing in for a forecast",
             "cable": True},
            {"dataset": "elexon/windfor", "gridflow_view": view("elexon", "windfor"), "column": "latest_forecast_mw",
             "role": "reference only: Elexon's own wind forecast, compared in the evidence report, never a model input",
             "cable": False},
        ],
        "output": {"copy": "Seven quantiles of wind output per half-hour, in MW.", "gold_views": []},
        "handles": ["models.wind_forecast"],
        "scores": [],
        "held": [
            {"why_held": "gate-failing run, not registered, nothing in gold; ruling #15 needs re-ruling first",
             "pinball_q0_5_mw": 416.7, "coverage_90": 0.722, "skill_crps_vs_baseline": 0.161,
             "gates": "skill pass, median pinball pass (limit 500), coverage FAIL (0.90 within 0.05), monotonicity pass",
             "window": "8 thirty-day folds, 2 October 2021 to 25 September 2026, perfect prognosis",
             "record": "data/models/wind_lgbm_quantile_v1/20260927T145057Z-FAILED/validation_record.json"},
        ],
        "evidence": [
            ev("configs/models/wind/lgbm_quantile_v1.yaml", "10-37", "target elexon/fuelhh WIND; features open_meteo/historical_wind"),
            ev("configs/models/wind/lgbm_quantile_v1.yaml", "56-60", "baseline: binned power curve on fleet_v100adj_mean"),
            ev("configs/models/wind/lgbm_quantile_v1.yaml", "80-99", "gates (skill, pinball 500, coverage, monotonicity); WINDFOR under benchmarks"),
            ev("src/gridflow_models/features/generation_sites.py", "29", "WIND_SITES: twelve sites"),
            ev("docs/MODEL_CARDS/wind_lgbm_quantile_v1.md", "21-46", "results: failed on coverage only, no manifest row; WINDFOR not like-for-like"),
            ev(".planning/phases/v2.3-H-2-wind-trained/receipts/WIND-TRAIN.md", None, "seat receipt of the real-store run"),
            ev("src/gridflow_models/research/handles/models.py", "176-222", "models.list(): no manifest entry means status 'unregistered'"),
            local("data/models/wind_lgbm_quantile_v1/20260927T145057Z-FAILED/validation_record.json", "416.70, 0.7220, skill 0.1612; passes_gates false"),
        ],
    },
    {
        "id": "solar",
        "name": "Solar generation",
        "model_ids": ["solar.lgbm_quantile.v1"],
        "drawing": "solar farm",
        "job": "Forecasts GB embedded solar output for every half-hour of the next day, from weather at six solar sites.",
        "method": ("LightGBM quantile regression on irradiance, cloud and sun position at six sites, fitted and "
                   "scored on daylight half-hours against an irradiance-curve baseline. The target is NESO's "
                   "estimate of embedded solar, not every GB solar generator."),
        "status_code": {
            "manifest_status": "none (no manifest row)",
            "models_list": "unregistered",
            "kind": "probabilistic estimator; one fitting run on 2026-09-27 failed the coverage gate (-FAILED artefact)",
        },
        "status_line": ("Scored once in a walk-forward backtest. Its 90% band was too narrow to pass the coverage "
                        "gate, so no version is registered."),
        "status_line_note": "Pending Bobbo's re-ruling of #15. See models-content-check.md, finding A.",
        "inputs": [
            {"dataset": "neso_data_portal/historic_generation_mix",
             "gridflow_view": view("neso_data_portal", "historic_generation_mix", latest=True), "column": "solar",
             "filter": "one pinned capture (published_at 2026-09-26T18:19:36Z)",
             "role": "target: NESO's embedded solar estimate", "cable": True},
            {"dataset": "open_meteo/historical_solar", "gridflow_view": view("open_meteo", "historical_solar"),
             "column": "irradiance (GHI, DNI, diffuse, GTI), temperature, cloud cover",
             "role": "observed weather at six sites, standing in for a forecast", "cable": True},
        ],
        "output": {"copy": "Seven quantiles of solar output per half-hour, in MW.", "gold_views": []},
        "handles": ["models.solar_forecast"],
        "scores": [],
        "held": [
            {"why_held": "gate-failing run, not registered, nothing in gold; ruling #15 needs re-ruling first",
             "pinball_q0_5_mw": 290.4, "coverage_90": 0.712, "skill_crps_vs_baseline": 0.193,
             "gates": "skill pass, median pinball pass (limit 300, daylight rows), coverage FAIL, monotonicity pass",
             "window": "8 thirty-day folds, 2 October 2021 to 25 September 2026, daylight rows only, perfect prognosis",
             "record": "data/models/solar_lgbm_quantile_v1/20260927T183348Z-FAILED/validation_record.json"},
        ],
        "evidence": [
            ev("configs/models/solar/lgbm_quantile_v1.yaml", "16-45", "target neso_data_portal/historic_generation_mix solar, pinned; open_meteo/historical_solar"),
            ev("configs/models/solar/lgbm_quantile_v1.yaml", "61-69", "daylight scoring mask; binned irradiance-curve baseline"),
            ev("configs/models/solar/lgbm_quantile_v1.yaml", "89-99", "gates: skill, pinball 300, coverage, monotonicity; no benchmarks block"),
            ev("src/gridflow_models/features/generation_sites.py", "50", "SOLAR_SITES: six sites"),
            ev("docs/MODEL_CARDS/solar_lgbm_quantile_v1.md", "1-20", "status and target provenance; NESO series is embedded solar"),
            ev("docs/MODEL_CARDS/solar_lgbm_quantile_v1.md", "86-120", "results: failed on coverage only, no manifest row"),
            ev(".planning/phases/v2.3-H-3-solar-trained/receipts/SOLAR-TRAIN.md", None, "seat receipt of the real-store run"),
            local("data/models/solar_lgbm_quantile_v1/20260927T183348Z-FAILED/validation_record.json", "290.37, 0.7124, skill 0.1930; passes_gates false"),
        ],
    },
    {
        "id": "stack",
        "name": "GB merit-order stack",
        "model_ids": ["stack.gb.v1"],
        "drawing": "the plant fleet: biomass, nuclear, CCGT, OCGT",
        "job": "Builds the GB supply curve for one half-hour: available plant ranked by short-run marginal cost, in cumulative MW.",
        "method": ("Built on request from the unit register, outage notices and fuel prices, with nothing to fit. "
                   "Fuel and carbon prices are synthetic. Clearing prices are floored at −500 GBP/MWh."),
        "status_code": {
            "manifest_status": "none (constructive models are not registered)",
            "models_list": "unregistered",
            "kind": "constructive (ConstructiveModel: build(), no fit_one_fold)",
        },
        "status_line": "Constructive: it is rebuilt for each half-hour and has no parameters to fit.",
        "inputs": [
            {"dataset": "elexon/bmunits_reference", "gridflow_view": view("elexon", "bmunits_reference"),
             "role": "unit register: identity, technology and capacity", "cable": True},
            {"dataset": "elexon/remit", "gridflow_view": view("elexon", "remit", latest=True),
             "role": "outage notices known at decision time, which cut unit availability", "cable": True},
            {"dataset": "elexon/fou2t14d", "gridflow_view": view("elexon", "fou2t14d", latest=True),
             "role": "fuel-level availability, used to derate units in the published run where it covers the period",
             "cable": True},
            {"dataset": "entsoe/installed_capacity_units", "gridflow_view": view("entsoe", "installed_capacity_units"),
             "role": "logged cross-check only; its keys do not match Elexon units, so it never shapes the curve",
             "cable": False},
            {"dataset": "data/manual/commodities.csv (not a gridflow dataset)", "gridflow_view": "",
             "role": "gas, coal and carbon prices, synthetic", "cable": False},
            {"dataset": "configs/engineering/plant_technology.yaml (not a gridflow dataset)", "gridflow_view": "",
             "role": "efficiency, emissions and fuel per technology", "cable": False},
        ],
        "output": {"copy": "A supply curve: each unit's available MW and marginal cost, sorted, with cumulative MW.",
                   "gold_views": ["gold_stack_supply_curve_points (written with the published SMP run)"]},
        "handles": ["models.stack.build(as_of)", "models.stack.clear(as_of, demand_mw)"],
        "scores": [],
        "scores_note": "No score of its own. It is scored only through the SMP model.",
        "held": [],
        "evidence": [
            ev("src/gridflow_models/estimators/stack/model.py", "1-16", "constructive merit-order supply curve"),
            ev("src/gridflow_models/estimators/stack/model.py", "126-146", "build: plant universe, fuel prices, marginal cost, sort and cumsum"),
            ev("src/gridflow_models/core/protocols.py", "47-55", "ConstructiveModel: built from inputs, no fit_one_fold"),
            ev("configs/models/stack/gb_v1.yaml", "9-43", "floor −500; inputs; commodity prices labelled synthetic; zero fuel for biomass and nuclear"),
            ev("src/gridflow_models/estimators/stack/plant_universe.py", "1-10", "four datasets read"),
            ev("src/gridflow_models/estimators/stack/plant_universe.py", "1078-1100", "ENTSO-E cross-check is log-only and cannot match keys"),
            ev("configs/backtest/price_formation_ladder_v2.yaml", "31-37", "FOU2T14D derating profile used by the published headline"),
            ev("docs/MODEL_CARDS/stack_gb_v1.md", "251-260", "publication is opt-in with --publish"),
            ev("src/gridflow_models/research/handles/model.py", "1389-1398", "workbench build(as_of) and clear(as_of, demand_mw)"),
        ],
    },
    {
        "id": "smp",
        "name": "Fundamentals SMP",
        "model_ids": ["fundamentals_smp.gb.v1"],
        "drawing": "stack crossed by a demand line (the draft's smp mark)",
        "job": "Clears residual demand against the stack every half-hour for a GB day-ahead price, scored against Elexon's market index.",
        "method": ("Residual demand is demand less wind and solar, less signed hydro, interconnector, OTHER and "
                   "pumped storage flows. The price is the marginal cost where that demand meets the stack, "
                   "floored at −500 GBP/MWh."),
        "status_code": {
            "manifest_status": "none",
            "models_list": "unregistered",
            "kind": "hybrid probabilistic estimator with a no-op fit; published backtest runs in gold",
        },
        "status_line": ("It has nothing to fit. Its published run clears recorded demand, wind and solar, so each "
                        "half-hour gets one price, not a spread."),
        "inputs": [
            {"dataset": "elexon/indo", "gridflow_view": view("elexon", "indo"), "column": "initial_demand_outturn_mw",
             "role": "recorded demand", "cable": True},
            {"dataset": "elexon/fuelhh", "gridflow_view": view("elexon", "fuelhh"), "column": "generation_mw",
             "role": "recorded wind, plus signed hydro, ten interconnectors, OTHER and pumped storage", "cable": True},
            {"dataset": "neso_data_portal/historic_generation_mix",
             "gridflow_view": view("neso_data_portal", "historic_generation_mix", latest=True), "column": "solar",
             "role": "recorded embedded solar", "cable": True},
            {"dataset": "stack.gb.v1 (model)", "gridflow_view": "", "role": "supply curve for each half-hour",
             "cable": True},
            {"dataset": "elexon/mid", "gridflow_view": view("elexon", "mid") + "; gold_gb_day_ahead_benchmark",
             "column": "market_index_price", "filter": "data_provider_id = APXMIDP",
             "role": "the price it is scored against", "cable": True},
        ],
        "output": {"copy": "A price per half-hour in GBP/MWh, as seven quantiles; in the published run all seven are equal.",
                   "gold_views": ["gold_stack_clearing", "gold_stack_residual_demand", "gold_stack_supply_curve_points"]},
        "handles": ["models.fundamentals_smp.backtest(...)"],
        "scores": [
            {"label": "Published run", "mean_bias_gbp_mwh": -151.80, "mae_gbp_mwh": 151.80,
             "window_copy": "18 August to 3 September 2026, every half-hour",
             "note_copy": "Every half-hour clears below the market index.",
             "caveat_copy": [
                 "A perfect-prognosis backtest: recorded demand, wind and solar stand in for forecasts.",
                 "Fuel and carbon prices are synthetic.",
                 "APXMIDP mixes day-ahead and intraday trades.",
                 "Clearing is floored at −500 GBP/MWh, which pulls some daily means below zero.",
             ],
             "provenance": {"store": "gold stack_clearing joined to silver elexon/mid APXMIDP (latest per period)",
                            "run_id": "41de423cfc0b421e", "vintage_policy_id": "smp_headline_perfect_prog_v2",
                            "exact": {"mean_bias": -151.8012, "mae": 151.8012, "median_bias": -95.3409},
                            "periods_scored": 816, "periods_below_benchmark": 816, "floor_binding_periods": 98,
                            "card": "docs/MODEL_CARDS/fundamentals_smp_gb_v1.md:443-453"}},
            {"label": "Year diagnostic", "mean_bias_gbp_mwh": -69.81, "mae_gbp_mwh": 72.84,
             "window_copy": "5 May 2025 to 4 May 2026, in monthly runs",
             "caveat_copy": ["A diagnostic that sees almost no outages and uses one fixed plant register for the whole year, so it is not the headline."],
             "use": "optional; recommended cut to declutter, or show only with its caveat",
             "provenance": {"store": "gold stack_clearing, 13 runs", "vintage_policy_id": "smp_diagnostic_perfect_prog_v2",
                            "exact": {"mean_bias": -69.8117, "mae": 72.8413}, "periods_scored": 17520,
                            "results": ".planning/milestones/v2.0-RESULTS.md:190-197"}},
        ],
        "held": [],
        "evidence": [
            ev(SMP_MODEL, "1-18", "combines demand, wind, solar and stack; no-op fit (ADR-038)"),
            ev(SMP_MODEL, "115-131", "fit_one_fold records component hashes only"),
            ev(SMP_MODEL, "137-146", "predict: component quantiles, N residual draws, stack per period, clear, quantiles"),
            ev(SMP_MODEL, "217-285", "the inference loop"),
            ev("src/gridflow_models/estimators/fundamentals_smp/sampler.py", "1-11", "Monte Carlo residual demand under marginal independence"),
            ev("src/gridflow_models/estimators/fundamentals_smp/sampler.py", "125-177", "inverse-CDF sampling; flat quantiles give identical draws"),
            ev("src/gridflow_models/estimators/fundamentals_smp/realised.py", "36-79", "realised adapter: every quantile equals the observed value"),
            ev("src/gridflow_models/backtest/smp_runtime.py", "778-808", "realised roles use the adapter; estimator roles need a registered bundle"),
            ev("configs/models/fundamentals_smp/gb_v1.yaml", "45-122", "realised components, 1,000 draws, signed netting, APXMIDP target"),
            ev("docs/MODEL_CARDS/fundamentals_smp_gb_v1.md", "21-35", "headline route is all-realised and opens no manifest"),
            ev("docs/MODEL_CARDS/fundamentals_smp_gb_v1.md", "71-73", "degenerate quantiles: coverage does not establish calibration"),
            ev("docs/MODEL_CARDS/fundamentals_smp_gb_v1.md", "443-477", "v2.0 published headline and limitations"),
            ev("src/gridflow/gold/views/gb_day_ahead_benchmark.sql", "1-24", "gold view over Elexon MID APXMIDP", repo="gf"),
            local("C:/gridflow-data/gold/stack_clearing/", "run 41de423cfc0b421e and 13 diagnostic runs, reproduced"),
        ],
    },
]

# ---------------------------------------------------------------- chain (for the drawing)
NODES = [
    {"id": "src_demand", "type": "source_image", "label": "Substation", "drawing": "pylons into a substation"},
    {"id": "src_wind", "type": "source_image", "label": "Wind farm", "drawing": "wind farm"},
    {"id": "src_solar", "type": "source_image", "label": "Solar farm", "drawing": "solar farm"},
    {"id": "src_fleet", "type": "source_image", "label": "Power stations", "drawing": "biomass, nuclear, CCGT, OCGT"},
    {"id": "ds_indo", "type": "dataset", "label": "elexon/indo", "gridflow_view": "silver_elexon_indo"},
    {"id": "ds_hist_demand", "type": "dataset", "label": "open_meteo/historical_demand", "gridflow_view": "silver_open_meteo_historical_demand"},
    {"id": "ds_fuelhh", "type": "dataset", "label": "elexon/fuelhh", "gridflow_view": "silver_elexon_fuelhh"},
    {"id": "ds_hist_wind", "type": "dataset", "label": "open_meteo/historical_wind", "gridflow_view": "silver_open_meteo_historical_wind"},
    {"id": "ds_hgm", "type": "dataset", "label": "neso_data_portal/historic_generation_mix", "gridflow_view": "silver_neso_data_portal_historic_generation_mix"},
    {"id": "ds_hist_solar", "type": "dataset", "label": "open_meteo/historical_solar", "gridflow_view": "silver_open_meteo_historical_solar"},
    {"id": "ds_bmu", "type": "dataset", "label": "elexon/bmunits_reference", "gridflow_view": "silver_elexon_bmunits_reference"},
    {"id": "ds_remit", "type": "dataset", "label": "elexon/remit", "gridflow_view": "silver_elexon_remit"},
    {"id": "ds_fou", "type": "dataset", "label": "elexon/fou2t14d", "gridflow_view": "silver_elexon_fou2t14d"},
    {"id": "ds_mid", "type": "dataset", "label": "elexon/mid (APXMIDP)", "gridflow_view": "silver_elexon_mid; gold_gb_day_ahead_benchmark"},
    {"id": "ext_fuel", "type": "non_gridflow_input", "label": "Fuel and carbon prices (synthetic)", "gridflow_view": ""},
    {"id": "m_demand", "type": "model", "label": "Day-ahead demand", "status": "validated"},
    {"id": "m_wind", "type": "model", "label": "Wind generation", "status": "unregistered"},
    {"id": "m_solar", "type": "model", "label": "Solar generation", "status": "unregistered"},
    {"id": "m_stack", "type": "model", "label": "GB merit-order stack", "status": "constructive"},
    {"id": "step_residual", "type": "step", "label": "Residual demand"},
    {"id": "m_smp", "type": "model", "label": "Fundamentals SMP", "status": "no-op fit"},
]


def edge(a: str, b: str, label: str, kind: str, exercised: bool, note: str = "") -> dict[str, object]:
    return {"from": a, "to": b, "label": label, "kind": kind, "exercised_in_published_run": exercised, "note": note}


EDGES = [
    edge("src_demand", "ds_indo", "national demand outturn", "cable", True),
    edge("src_demand", "ds_hist_demand", "weather at seven city sites", "cable", True, "version 2 only"),
    edge("src_wind", "ds_fuelhh", "metered wind", "cable", True),
    edge("src_wind", "ds_hist_wind", "weather at twelve sites", "cable", True),
    edge("src_solar", "ds_hgm", "embedded solar estimate", "cable", True),
    edge("src_solar", "ds_hist_solar", "weather at six sites", "cable", True),
    edge("src_fleet", "ds_bmu", "unit register", "cable", True),
    edge("src_fleet", "ds_remit", "outage notices", "cable", True),
    edge("src_fleet", "ds_fou", "fuel-level availability", "cable", True),
    edge("ds_indo", "m_demand", "target and lags", "feeds", True, "gold run a55a829bc51c40b2 (v1)"),
    edge("ds_hist_demand", "m_demand", "weather (version 2)", "feeds", True, "gold run b367a742aa544f8f (v2)"),
    edge("ds_fuelhh", "m_wind", "target (WIND)", "feeds", True, "scored run failed the coverage gate; nothing in gold"),
    edge("ds_hist_wind", "m_wind", "weather", "feeds", True, "as above"),
    edge("ds_hgm", "m_solar", "target (solar)", "feeds", True, "scored run failed the coverage gate; nothing in gold"),
    edge("ds_hist_solar", "m_solar", "weather", "feeds", True, "as above"),
    edge("ds_bmu", "m_stack", "units", "feeds", True),
    edge("ds_remit", "m_stack", "availability", "feeds", True),
    edge("ds_fou", "m_stack", "derating", "feeds", True, "published run only; covers part of the window"),
    edge("ext_fuel", "m_stack", "marginal cost", "feeds", True, "not a gridflow dataset; keep in text, not as a silver tap"),
    edge("ds_indo", "step_residual", "recorded demand", "feeds", True),
    edge("ds_fuelhh", "step_residual", "recorded wind and signed netting", "feeds", True),
    edge("ds_hgm", "step_residual", "recorded solar", "feeds", True),
    edge("m_demand", "step_residual", "demand forecast", "forecast_route", False,
         "supported by code (EstimatorInputConfig); never run. Do not draw."),
    edge("m_wind", "step_residual", "wind forecast", "forecast_route", False,
         "cannot run: no registered version. Do not draw."),
    edge("m_solar", "step_residual", "solar forecast", "forecast_route", False,
         "cannot run: no registered version. Do not draw."),
    edge("step_residual", "m_smp", "residual demand", "feeds", True, "1,000 draws; identical in the published run"),
    edge("m_stack", "m_smp", "supply curve per half-hour", "feeds", True),
    edge("ds_mid", "m_smp", "scored against", "scored_against", True),
]

CHAIN = {
    "summary": ("Designed chain (code): demand, wind and solar forecasts, sampled into residual demand, cleared "
                "through the stack for a probabilistic price. Published run: the three recorded outturns replace "
                "the forecasts, so the price is one value per half-hour."),
    "drawing_rule": ("Draw only edges with exercised_in_published_run true. The SMP residual-demand cable "
                     "branches off the same three datasets the forecast models learn from (elexon/indo, "
                     "elexon/fuelhh, neso_data_portal/historic_generation_mix), not off the models. No dashed "
                     "'not yet' edges (DESIGN.md)."),
    "exercised_meaning": ("exercised_in_published_run: for edges into the SMP (residual demand, stack, benchmark), "
                          "whether published run 41de423cfc0b421e used it; for every other edge, whether the "
                          "model's stored scored run used it (demand in gold; wind and solar in -FAILED records)."),
    "nodes": NODES,
    "edges": EDGES,
    "confirmed": {
        "stack_constructive_no_learning": True,
        "smp_no_op_fit": True,
        "forecasts_to_residual_to_stack_to_probabilistic_smp": "true as the code path; false for the published run",
    },
}

READING = {
    "heading": "Reading the scores",
    "copy": ("Every score here is a backtest held in gold. Pinball loss at the median is half the mean absolute "
             "error of the median forecast, in MW. Coverage is the share of outturns inside the 5 to 95% band. A "
             "demand version passes when median pinball is at most 1,500 MW, coverage is within 0.05 of 0.90 and "
             "no quantiles cross. Price scores are in GBP/MWh against Elexon's APXMIDP market index."),
    "evidence": [
        ev("src/gridflow_models/validation/metrics.py", "15", "pinball_loss"),
        ev("configs/models/day_ahead/lgbm_demand_v1.yaml", "77-84", "demand gates"),
    ],
}

CHARTS = [
    {"id": "demand_band", "title_copy": "Demand forecast against outturn, 20 and 21 August 2026",
     "caption_copy": ("Version 1: the median inside its 5 to 95% band, and the outturn from elexon/indo. Issued at "
                      "noon UTC the day before."),
     "dataset": "gold forecasts, run a55a829bc51c40b2, fold 12", "unit": "MW",
     "window": "2026-08-20T00:00Z to 2026-08-21T23:30Z", "points": 96,
     "verified": "96 rows; values 17,466 to 31,583 MW; issued_at 12:00 UTC on the previous day",
     "series_source": "p27-r1/pack/toppages.json series.models_landing_demand"},
    {"id": "smp_daily", "title_copy": "Daily mean price, 18 August to 3 September 2026",
     "caption_copy": ("Model clearing against APXMIDP, daily means of every half-hour in the published run. "
                      "Recorded demand, wind and solar stand in for forecasts; fuel and carbon prices are synthetic; "
                      "APXMIDP mixes day-ahead and intraday trades; the −500 GBP/MWh floor pulls some daily means "
                      "below zero."),
     "dataset": "gold stack_clearing run 41de423cfc0b421e joined to silver elexon/mid APXMIDP", "unit": "GBP/MWh",
     "window": "2026-08-18 to 2026-09-03", "points": 17,
     "verified": "model daily means −136.0 to 78.4; APXMIDP 89.7 to 166.8",
     "series_source": "p27-r1/pack/toppages.json series.models_landing_smp"},
]

WORKBENCH = {
    "heading_copy": "In a notebook",
    "code": "from gridflow_models import setup_notebook\ndata, models, common = setup_notebook()\nmodels.list()",
    "note": ("models.list() shows demand v1 and v2 as validated and the other four as unregistered, which "
             "matches this pack."),
    "evidence": [
        ev("src/gridflow_models/research/notebook_setup.py", "278", "setup_notebook"),
        ev("src/gridflow_models/__init__.py", "5", "exported at package top level"),
        ev("src/gridflow_models/research/handles/models.py", "176-222", "models.list() columns and status rule"),
    ],
}

UNVERIFIED = [
    "APXMIDP's exact vendor definition (the SMP card says its contemporary definition is unverified). Say only that it mixes day-ahead and intraday trades.",
    "That NESO's embedded solar series is PV_Live-derived: a deduction in the solar card, not a vendor statement. Keep it off the page.",
    "How well twelve wind sites and six solar sites represent the GB fleet: the cards call it unestablished. No representativeness claim.",
    "FOU2T14D and REMIT historical reach depends on a vendor backfill the SMP card calls unverified. Do not claim full outage coverage.",
    "The v2 demand gain (about 15.7%) is one run with no significance test and is an upper bound under perfect prognosis. Do not print it as an improvement figure.",
    "notebooks/README.md model lines (last edited 2026-05-31) say wind and solar are 'trained' and SMP 'loads four component models from the manifest'. Both are stale against the code. Do not quote.",
]

NEEDS_RULING = [
    {"question": ("DESIGN.md says model status truth lives in gridflow_models notebooks/README.md, but its model "
                  "lines (last edited 2026-05-31) are stale: wind and solar 'trained', SMP 'loads four component "
                  "models from the manifest'. This pack takes status from the manifest and models.list() instead. "
                  "Let code and manifest win until the README is fixed?"),
     "recommended": "yes",
     "copy_if_yes": "No copy change; the status lines in this pack already follow the code.",
     "evidence": "models-content-check.md, last section; DESIGN.md content rules"},
    {"question": ("Ruling #15 says wind and solar are shown as never trained. Since 2026-09-27 15:46 both were "
                  "fitted and scored once and failed the coverage gate (no manifest row, nothing in gold). Show them "
                  "as unregistered, scored once, with the scores held off the page?"),
     "recommended": "yes",
     "copy_if_yes": "Scored once in a walk-forward backtest. Its 90% band was too narrow to pass the coverage gate, so no version is registered.",
     "evidence": "models-content-check.md finding A; gridflow_models RULINGS #1001, #1006, #1007"},
]

META = {
    "built": "2026-09-27",
    "model": "claude-opus-5-5",
    "gridflow_models": {"repo": "https://github.com/EBentham/gridflow-models", "default_branch": "main",
                        "commit": GM_COMMIT, "private": True},
    "gridflow": {"repo": "https://github.com/EBentham/gridflow", "default_branch": "master", "commit": GF_COMMIT},
    "limits": {"job_words": 20},
    "copy_fields": "headline, lede, chain_line, published_run_line, optional_capability_line, scope, job, method, "
                   "status_line, output.copy, window_copy, note_copy, caveat_copy, title_copy, caption_copy, "
                   "READING.copy, heading_copy",
}

# ---------------------------------------------------------------- lint
BANNED_CHARS = {"\u2014": "em dash", "\u2013": "en dash", "\u2192": "arrow", "\u00b7": "middle dot"}
BANNED_WORDS = re.compile(r"\b(planned|shipped|trained|live|in service|coming|soon)\b", re.I)


def copy_strings() -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for k in ("headline", "lede", "chain_line", "published_run_line", "optional_capability_line", "scope"):
        out.append((f"opening.{k}", OPENING[k]))
    for m in MODELS:
        for k in ("name", "job", "method", "status_line"):
            out.append((f"{m['id']}.{k}", m[k]))
        out.append((f"{m['id']}.output", m["output"]["copy"]))
        for x in m["inputs"]:
            out.append((f"{m['id']}.input.role", x["role"]))
        if "scores_note" in m:
            out.append((f"{m['id']}.scores_note", m["scores_note"]))
        for s in m["scores"]:
            for k in ("window_copy", "note_copy"):
                if k in s:
                    out.append((f"{m['id']}.score.{k}", s[k]))
            cav = s.get("caveat_copy", [])
            for c in [cav] if isinstance(cav, str) else cav:
                out.append((f"{m['id']}.score.caveat", c))
    for n in NODES:
        out.append((f"node.{n['id']}", n["label"]))
    for e in EDGES:
        out.append((f"edge.{e['from']}>{e['to']}", str(e["label"])))
    out.append(("reading", READING["copy"]))
    for c in CHARTS:
        out.append((f"chart.{c['id']}.title", c["title_copy"]))
        out.append((f"chart.{c['id']}.caption", c["caption_copy"]))
    for r in NEEDS_RULING:
        out.append(("ruling.copy_if_yes", r["copy_if_yes"]))
    return out


def lint() -> list[str]:
    errs: list[str] = []
    for where, text in copy_strings():
        for ch, name in BANNED_CHARS.items():
            if ch in text:
                errs.append(f"{where}: {name}")
        if m := BANNED_WORDS.search(text):
            errs.append(f"{where}: banned word '{m.group(0)}'")
    for m in MODELS:
        n = len(m["job"].split())
        if n > 20:
            errs.append(f"{m['id']}.job: {n} words")
    return errs


# ---------------------------------------------------------------- markdown
def md_ev(items: list[dict[str, str]]) -> str:
    rows = []
    for e in items:
        loc = f"{e['path']}:{e['lines']}" if e["lines"] else e["path"]
        if e["url"]:
            rows.append(f"- [`{loc}`]({e['url']}) ({e['repo']}): {e['note']}")
        else:
            rows.append(f"- `{loc}` ({e['repo']}): {e['note']}")
    return "\n".join(rows)


def md() -> str:
    L: list[str] = []
    L.append("# Models page content pack\n")
    L.append(f"Built 2026-09-27 by claude-opus-5-5 from gridflow_models `main` at `{GM_COMMIT[:7]}` and gridflow "
             f"`master` at `{GF_COMMIT[:7]}`. Every score was reproduced read-only from its stored record (manifest, "
             "validation records, gold Parquet); the method and the corrections to the draft are in "
             "`models-content-check.md`. Machine-readable twin: `pack.json`, which also carries commit permalinks "
             "with line anchors. Source of both: `_build_pack.py` (edit and re-run; it lints the copy).\n")
    L.append("**Copy rules applied and checked by `_build_pack.py`:** no em or en dashes, no arrows, no middle "
             "dots, no planning words (planned, shipped, trained, live, in service, coming), no local row counts, "
             "no invented numbers; job lines up to 20 words. Links point at `main` of the private "
             "gridflow-models repo; paths marked local are gitignored stores and have no link. Red Hat Mono for "
             "everything in backticks.\n")
    L.append("**Two things to know before designing** (full reasoning in `models-content-check.md`):\n")
    L.append("1. The price chain runs from the recorded outturns, not from the forecast models. The SMP code can "
             "take forecasts, but the only published run used recorded demand, wind and solar, so it gives one "
             "price per half-hour. Draw the SMP cable from the three datasets, not from the three models.")
    L.append("2. Wind and solar were fitted and scored once on 2026-09-27 and failed the coverage gate. Ruling #15 "
             "(never trained) needs re-ruling; the status copy below assumes the recommended yes, and their "
             "scores are held.\n")

    L.append("## 1. Opening\n")
    L.append(f"**Headline.** {OPENING['headline']}\n")
    L.append(f"**Lede.** {OPENING['lede']}\n")
    L.append(f"**The chain in one line.** {OPENING['chain_line']}\n")
    L.append(f"**What the published run did.** {OPENING['published_run_line']}\n")
    L.append(f"**Optional.** {OPENING['optional_capability_line']}\n")
    L.append(f"**Scope line.** {OPENING['scope']}\n")
    for n in OPENING["notes"]:
        L.append(f"Designer note (not copy): {n}\n")
    L.append("Evidence:\n" + md_ev(OPENING["evidence"]) + "\n")

    L.append("## 2. The chain, for the drawing\n")
    L.append(f"{CHAIN['summary']}\n")
    L.append(f"**Drawing rule.** {CHAIN['drawing_rule']}\n")
    L.append("Confirmed: the stack is constructive with no learning; the SMP model has a no-op fit. The claim "
             "'demand, wind and solar forecasts give residual demand, sampled and run through the stack for a "
             "probabilistic SMP' is true of the code path and false of the published run.\n")
    L.append(f"{CHAIN['exercised_meaning']}\n")
    L.append("| From | To | Label | Kind | Used in a stored run | Note |")
    L.append("|---|---|---|---|---|---|")
    lab = {n["id"]: n["label"] for n in NODES}
    for e in EDGES:
        L.append(f"| {lab[e['from']]} | {lab[e['to']]} | {e['label']} | {e['kind']} | "
                 f"{'yes' if e['exercised_in_published_run'] else 'no'} | {e['note']} |")
    L.append("")

    L.append("## 3. The models\n")
    for i, m in enumerate(MODELS, 1):
        L.append(f"### 3.{i} {m['name']}\n")
        L.append(f"- Model ids: {', '.join(f'`{x}`' for x in m['model_ids'])}. Drawing: {m['drawing']}.")
        L.append(f"- **Job:** {m['job']}")
        L.append(f"- **Method:** {m['method']}")
        sc = m["status_code"]
        L.append(f"- **Status as the code states it:** manifest `{sc['manifest_status']}`; `models.list()` "
                 f"says `{sc['models_list']}`; {sc['kind']}.")
        L.append(f"- **Status line (copy):** {m['status_line']}")
        if "status_line_note" in m:
            L.append(f"  - Designer note: {m['status_line_note']}")
        L.append(f"- **Output:** {m['output']['copy']}" +
                 (f" Gold views: {', '.join(f'`{g}`' for g in m['output']['gold_views'])}." if m["output"]["gold_views"] else " Nothing in gold."))
        L.append(f"- **Workbench:** {', '.join(f'`{h}`' for h in m['handles'])}")
        L.append("")
        L.append("| Input | gridflow view | Column / filter | Role | Cable |")
        L.append("|---|---|---|---|---|")
        for x in m["inputs"]:
            colf = " ; ".join(v for v in (x.get("column", ""), x.get("filter", "")) if v)
            L.append(f"| `{x['dataset']}` | {('`' + x['gridflow_view'] + '`') if x['gridflow_view'] else 'n/a'} | "
                     f"{colf} | {x['role']} | {'yes' if x['cable'] else 'no'} |")
        L.append("")
        if m["scores"]:
            L.append("**Scores (real, with provenance):**\n")
            for s in m["scores"]:
                if "pinball_q0_5_mw" in s:
                    L.append(f"- {s['label']}: median pinball **{s['pinball_q0_5_mw']:.2f} MW**, 90% coverage "
                             f"**{s['coverage_90']:.3f}**, gates {s['gates']}. Window: {s['window_copy']}.")
                else:
                    L.append(f"- {s['label']}: mean bias **{s['mean_bias_gbp_mwh']:.2f}**, MAE "
                             f"**{s['mae_gbp_mwh']:.2f}** GBP/MWh. Window: {s['window_copy']}.")
                if "note_copy" in s:
                    L.append(f"  - Copy: {s['note_copy']}")
                cav = s.get("caveat_copy")
                if cav:
                    for c in [cav] if isinstance(cav, str) else cav:
                        L.append(f"  - Caveat (copy): {c}")
                if "use" in s:
                    L.append(f"  - Use: {s['use']}")
                p = s["provenance"]
                L.append(f"  - Provenance: {json.dumps(p, ensure_ascii=False)}")
            L.append("")
        elif "scores_note" in m:
            L.append(f"**Scores:** {m['scores_note']}\n")
        else:
            L.append("**Scores:** none on the page.\n")
        if m["held"]:
            for h in m["held"]:
                L.append(f"**Held, not copy** ({h['why_held']}): median pinball {h['pinball_q0_5_mw']} MW, 90% "
                         f"coverage {h['coverage_90']}, skill over baseline {h['skill_crps_vs_baseline']}; "
                         f"{h['gates']}; {h['window']}; record `{h['record']}`.\n")
        L.append("Evidence:\n" + md_ev(m["evidence"]) + "\n")

    L.append(f"## 4. {READING['heading']}\n")
    L.append(f"{READING['copy']}\n")
    L.append("Designer note: a candidate to fold into the demand block to declutter.\n")
    L.append("Evidence:\n" + md_ev(READING["evidence"]) + "\n")

    L.append("## 5. Charts\n")
    for c in CHARTS:
        L.append(f"**{c['title_copy']}** ({c['id']})\n")
        L.append(f"- Caption (copy): {c['caption_copy']}")
        L.append(f"- Data: {c['dataset']}; unit {c['unit']}; window {c['window']}; {c['points']} points; "
                 f"arrays in `{c['series_source']}`.")
        L.append(f"- Verified: {c['verified']}.\n")

    L.append(f"## 6. {WORKBENCH['heading_copy']}\n")
    L.append("```python\n" + WORKBENCH["code"] + "\n```\n")
    L.append(f"{WORKBENCH['note']}\n")
    L.append("Evidence:\n" + md_ev(WORKBENCH["evidence"]) + "\n")

    L.append("## 7. Needs a ruling\n")
    for r in NEEDS_RULING:
        L.append(f"- {r['question']} Recommended: **{r['recommended']}**. Copy if yes: \"{r['copy_if_yes']}\" "
                 f"({r['evidence']})")
    L.append("")
    L.append("## 8. Unverified (keep off the page)\n")
    for u in UNVERIFIED:
        L.append(f"- {u}")
    L.append("")
    return "\n".join(L)


def main() -> int:
    errs = lint()
    if errs:
        print("LINT FAILED:\n" + "\n".join(errs))
        return 1
    pack = {"meta": META, "opening": OPENING, "chain": CHAIN, "models": MODELS, "reading_scores": READING,
            "charts": CHARTS, "workbench": WORKBENCH, "needs_ruling": NEEDS_RULING, "unverified": UNVERIFIED}
    (HERE / "pack.json").write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (HERE / "MODELS-PACK.md").write_text(md(), encoding="utf-8")
    print(f"ok: {len(copy_strings())} copy strings linted; wrote pack.json and MODELS-PACK.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
