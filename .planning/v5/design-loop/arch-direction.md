# Architecture page: content direction (agreed with Bobbo, 2026-09-27)

Evidence for every correction: `arch-content-check.md` (same folder). This file is the brief for the content
pack and the three designers. Nothing here is copy yet; the content pack writes and verifies the copy.

## The page's job

Show a full-stack data-science recruiter in energy trading that Bobbo can design and build a production-quality
data system. In about a minute a reader should get four things:

1. The whole system in one picture.
2. One hard problem handled properly: revisions, or knowing what was known, and when.
3. Evidence it stays correct: validation counts, quality checks, run tracking, tests.
4. Where to look in the code.

## Page order

1. **Opening.** One-sentence lede (the current one is accurate: raw responses in bronze, cleaned typed tables
   in silver, joins in gold, all readable from one embedded DuckDB file). Then one scope line: what gridflow
   deliberately does not do (no scheduler, no server, no cloud, no live feed; every run is one CLI command).
   No stat strip, no hard-coded counts.
2. **The system drawing (centrepiece, new).** In the site's "above ground, below ground" language, not a
   node-and-arrow flowchart (banned in DESIGN.md):
   - above ground: the eight vendor sources on the grid (Elexon, ENTSO-E, ENTSO-G, NESO carbon intensity,
     NESO Data Portal, GIE AGSI, GIE ALSI, Open-Meteo; verify the list against `config/sources.yaml`);
   - cables down into the strata, bronze then silver then gold, each boundary labelled with the real mechanism
     there (async httpx with a per-source rate-limit semaphore and tenacity retries; raw bytes plus a
     `.meta.json` sidecar, atomic writes; typed Polars transformers, fail-soft validation counts, every row
     stamped `available_at` / `source_run_id` / `dataset_version`; DuckDB views over Hive-partitioned
     Parquet, `_latest` views; gold SQL views and builders);
   - the readers at the bottom: the CLI, `GridflowClient` (read-only, returns Polars), notebooks, and
     **gridflow_models**, which reads through `GridflowClient`. The gridflow_models part links to the Models
     page (Bobbo: "link it to the Models page in some form").
   - A keyed index beside the drawing names each part; each entry links to its file on GitHub.
   - Every label verified against the code. None of the old diagram's wrong labels (Parquet bronze,
     Pydantic-validated bronze, `query` verb, MLflow, PuLP dispatch, materialised views).
3. **The row's journey (keep and expand; absorbs the old "Bronze, Silver, Gold" section).** One real Elexon
   system_prices row from the CLI call to a Polars DataFrame, showing the real object at each stop:
   CLI call, connector request, the raw bronze file and sidecar (real path shape), the silver row with its
   vintage stamps (append-only, one file per vintage), **the `_latest` view choosing the winning revision
   (the highlighted stop: what was known, and when; per-dataset publication-lag rules described as a
   mechanism, no lag figure)**, the gold row (`system_marginal_price`: spread = buy minus sell), then a
   `from gridflow.serving.client import GridflowClient` read into Polars. The layer contract (what each
   layer guarantees) is stated inside the relevant stops, not as a separate section. Every code snippet must
   run against the real code (correct import, canonical view names, no run_type filter on live rows).
4. **How it stays correct (the old principles, much smaller).** About five one-line rules, each with a file
   reference, plus a line on run tracking (`pipeline_runs`, watermarks, `quality_reports`, the `quality`
   verb) and CI (lock check, ruff, mypy, pytest without live tests). Candidates: raw bytes are kept, so any
   silver table rebuilds without calling the vendor; re-runs are safe; schema drift is counted and reported,
   never silently dropped; every row carries when it could first have been known; one embedded file
   database, no server. No absolutes the code contradicts ("nothing is ever deleted", "fails loudly",
   "identical in CI").
5. **Where to look (slim repo map).** About ten entries, "where to look for X", each a link to the file on
   GitHub. No counts, no phantom files. The designers show it; Bobbo decides after seeing it whether the
   drawing's links make it redundant.

Cut: the old system diagram, the stat strip, the standalone Bronze/Silver/Gold section, "pandas, DuckDB
WASM, Tableau".

## Rules that bind

DESIGN.md and tokens.css; the top-page language Bobbo picked (A, `p27-r1/canvas/project/A-*.dc.html`,
generator `p27-r1/A/`); no em dashes, eyebrows, middle-dot strings, "→", italic headline words, planning
leakage or local-data references; Red Hat Mono only for code, paths, column names and values.

## Next

1. Content pack: one Opus agent writes `arch-pack/` (verified copy for every drawing label, keyed index entry,
   journey stop with its real snippet, rule and repo-map entry, each with file:line), runs the journey's
   snippets against real silver, and flags anything it cannot verify.
2. Three Opus designers, different takes on the drawing and the journey, same pack, side by side in the
   picker, each section commentable. Bobbo picks and mixes.
