# Dataset page design loop: decisions with Bobbo (2026-09-27)

Picker: https://claude.ai/artifact/MpySKZLbpbe6VmCz4pcuzV · round-1 canvas https://claude.ai/artifact/7tkS1ydY8QWLvhC8LXbcsT

## Decision 1: overall layout (OWNER)

- **Base: A, "The section".** The page descends through the strata: chart and prose in topsoil, raw endpoint
  in bronze, schema and sample in silver, workbench call in gold.
- **Demo notebook:** a button at the bottom reveals a hidden notebook in D's style. The cells must paste
  into Jupyter and run as-is. Verify every cell before shipping.
- **No local-data references anywhere:** no "held locally", no local row counts, no local date ranges.
  History means what the vendor's API provides (e.g. "Elexon publishes from 2015"), only where evidenced.
  The same rule applies to "What it is".
- **Keep the raw vendor URL** in "how to get it".
- **Schema and sample rows: redesign.** Bobbo is not a fan of the round-1 formatting.
- **Foot:** the deep petrol band holds only related datasets. Remove the "Source on GitHub" and "MIT
  license" footer line.
- **Remove the caveats section** (A's "What to watch for"). Any caveat that matters for reading the chart
  goes in the chart caption instead.

## Decision 2: chart (OWNER)

- **A's chart:** in the topsoil with a key beside it. Signed series (interconnectors, pumped storage) stack
  above zero when positive and hang below when negative. Fuel codes the palette doesn't cover are drawn
  unpainted with distinct ink hatches, and khaki means only the vendor code OTHER.

## Decision 3: schema and sample rows (OWNER)

- **4, "One record, then many"** (`<scratch>\p24\r2-schema\4\`, generator `gen4.py`, `content4.py`,
  `s4.css`, notes `4-notes.md`): one real row laid out field by field (name, value, dtype, meaning, key
  squares; the row's lineage columns under one label) is the schema; then "Eight rows" as a compact table
  showing only the schema columns that differ between rows, with the record's row marked. Values formatted
  by Polars. Open from its notes: A's "equal to SSP on every row" on system_prices needs checking before
  round 2; the 390 px reflow is written but untested.

## Decision 4: demo notebook content (OWNER, 2026-09-27)

- **Option 2: through gridflow and the gridflow_models notebook module** ("to show off my notebooks
  module"): `from gridflow_models import setup_notebook`, `data, models, common = setup_notebook()`,
  `data.<vendor>.query("<dataset>", start, end)` returning pandas, as on the architecture page. Chosen over
  raw vendor API cells and over two tabs.
- Constraint found 2026-09-27: `github.com/EBentham/gridflow` is public (branch master), but
  `github.com/EBentham/gridflow-models` is PRIVATE, and gridflow-models resolves gridflow as a sibling path
  (`[tool.uv.sources] gridflow = { path = "../gridflow" }`). "Paste it and it runs" for a reader needs the
  repo public and setup cells (clone both side by side, `uv sync`, `gridflow init`, an ingest of the window).
  Bobbo's ruling: keep links pointing at gridflow-models on GitHub even though it is private for now. He
  will soon split the notebook module into its own PUBLIC repo (gridflow-models stays private); the demo
  notebook's setup cells then install from that repo. Until its name exists, setup cells are written against
  the current package and flagged for a one-line update.
- Later the same day (OWNER): **no setup cells at all** (no clone, uv, init or ingest); the notebook starts at
  `setup_notebook()`. One designer drafts it ("it's not difficult"): the inline drawer in the gold stratum,
  `<scratch>\p24\r2-notebook\1\`. The sheet and recipe directions were stopped.

## Decision 5: demo notebook panel, and the lock (OWNER, 2026-09-27)

- The drawer draft (`p24-r2-notebook/1/`) as it stands: homepage notebook style, opens in place in the gold
  stratum, one "Copy notebook" button (code only), the "Needs ... ingested" line kept.
- **Dataset page design LOCKED** ("looks good, lock it"). Anatomy written into `DESIGN.md` "Dataset page
  anatomy". Next: the template and a five-dataset pilot (25b).
- Carry into 25b: check "SBP equals SSP on every row" (system_prices) against code before it ships; test the
  schema section's 390 px reflow; gridflow_models help card says "35 datasets" while `list_datasets()`
  returns 33 (the page omits the count; the mismatch is a gridflow_models bug).

## Decision 2b: facts and how to get it (OWNER)

- Keep A's for both: quick facts in the petrol hero under the one-liner; the raw feed and CLI in bronze and
  the workbench call in gold, plus the demo-notebook button.
