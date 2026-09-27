# Architecture page: decisions with Bobbo (2026-09-27)

Picker: https://claude.ai/artifact/MpySKZLbpbe6VmCz4pcuzV (Architecture mode) · boards `arch-r1/<N>/`

## Round 1

- **System drawing: 2, "The specimen"** (OWNER).
- **Stop 7 (the read at the end of the journey): read into pandas through the gridflow_models notebook
  module instead of Polars through `GridflowClient`** (OWNER). Verified read-only 2026-09-27:

  ```python
  from gridflow_models import setup_notebook

  data, models, common = setup_notebook()
  df = data.elexon.query("system_prices", "2026-09-08", "2026-09-08")
  ```

  Returns a `pandas.DataFrame`, 48 rows (one per period, latest version), period 37 = 110.0 for both prices,
  `run_type` NaN. Timestamps come back in local time (+01:00); convert or say so on the page. Source:
  `gridflow_models/research/__init__.py` (pandas at the notebook boundary, ADR-031),
  `research/_pandas_client.py`, usage in `notebooks/data_layer/01_elexon.py:39-41, 190`.
- **Everything else from 2 as well** (OWNER): journey, opening, how it stays correct, where to look.
- **Scope line reworded** (OWNER, option 1 of three): "Every stage is one command that is safe to re-run
  and records its own run, so it drops into any orchestrator, such as cron, Airflow or Dagster, as a task."
  Replaces "no scheduler, no server, no cloud, no live feed", which read as a list of shortcomings. Each
  clause must be verified against the code before it ships (exit codes, safe re-runs, run tracking).
- Fix whatever goes forward: design 1's GitHub links are rendered as dict text (generator bug); no design
  has a 390 px layout yet.
