# Phase 25a merge record (2026-09-27)

Seat re-verification on the PR head before merge: build --check OK (165 pages + 7 hubs), 53 tests passed, htmlhint 0 errors (176 files), lychee 4065 OK / 0 errors, charts.js has no seeded generator; 130 'seed'/'Illustrative snapshot' hits are authored overrides retired in 25b. Squash-merged PR #40 into v5/site as c9da254. Agent spend: 386k subagent tokens.

## Agent report

claude-opus-5-5
# Phase 25a: chart pipeline and build plumbing

**Status:** done. PR https://github.com/EBentham/gridflow-front-end/pull/40 (base `v5/site`, head `v5/p25a-chart-pipeline`, not merged). The branch was cut from `b3b4892` (verified).

## Commits
- `8c5f0e0` chore: ruff config (line-length 100) and a small format fix in serve.py and `__init__`.py
- `e19c5ef` feat(build): chart spec schema and vault page fields (`chart_spec.py`, `page_fields.py`, `paths.py`, pyproject, uv.lock, tests)
- `e6969a6` feat(distil): the `gridflow-distil` command (`distil.py`, tests)
- `0d0c080` feat(data): the 4 staged specs and their distilled series
- `6ae81b3` feat(charts): seeded shapes removed; new `series` and `bars` renderers
- `e85cf00` feat(build): renders distilled charts; seeded fallback and stub generator removed
- `ac94f7c` fix(templates): vendor hub no longer claims "illustrative snapshot"

## Gates (actual output)
- `uv run --system-certs --extra build gridflow-build --check`: exit 0, "OK: idempotent across 165 pages + 7 hubs."
- `uv run --system-certs --extra build --extra distil pytest -x -q`: "53 passed"
- `uvx --system-certs ruff check src tests`: "All checks passed!"
- `uvx --system-certs ruff format --check src tests`: "13 files already formatted"
- Seeded markers: grep for `Illustrative snapshot|Deterministic seeded|"seed"|data-chart` over the 35 template pages and 7 hubs found 0 hits. `charts.js` has no SHAPES, rng or Math.random; its one "seeded" hit is the header comment saying there is no seeded fallback.
- NESO Data Portal stubs: `data-sources/neso_data_portal/` holds only the 3 real pages. The hub has 0 "Planned" or coming-soon hits.
- `htmlhint --config .htmlhintrc "site/hifi/**/*.html"`: "Scanned 176 files, no errors found"
- `lychee --no-progress --offline --include-fragments './site/hifi/**/*.html'`: 4065 OK, 0 errors, 427 excluded
- `gridflow-drift-check`: not run (live API, forbidden by the brief).
- Browser check on a local server:
  - The 4 specimens, rendered through the template, draw 6, 1 and 3 lines plus 19 bars, with no NaN.
  - The homepage and data-sources sparklines and donut still draw.
  - A seed-only authored chart is now hidden.

## Decisions
1. **Spec location and format.** YAML front matter, one `page:` key with `summary`, `what_it_is`, `how_used`, `caveats` and `chart`. All names are in `page_fields.py`.
   - Why not a fenced block: the drift check's curl extractor runs any fenced block containing "curl".
   - Both vault scripts already `yaml.safe_load` the front matter, and the mirror copies it verbatim.
   - `---` is rejected in page strings, because the vault scripts split the note on it.
   - PyYAML is added to the `[build]` extra.
2. **Staging.** The 4 specs live in `site/hifi/data/chart-specs/`. A vault `page.chart` wins over a staged spec, with a NOTE.
3. **Build gate.** The build fails on:
   - an invalid spec
   - a spec with no series
   - an orphan spec or series
   - a stale spec digest
4. **No time axis.** These get `type: bar` (a category-shaped series with no window). `type: none` plus a `reason` means no chart.
5. **The specimens:**
   - fuelhh: summed by fuel group, last 7 days.
   - system_prices: deduplicated to the latest published row, last 7 days.
   - entsog: National Gas TSO exit flow at Bacton (BBL), Bacton (IUK) and Moffat, daily, last 14 days.
   - bmunits: registered capacity summed by fuel type. Only 499 of 3014 units declare a fuel type, and the provenance records this.
6. **The NESO Data Portal hub** renders from its manifest instead of the authored landing, which linked 29 non-ingested packages. The lede and stats no longer count unbuilt packages; the authored file is kept.
7. **Stale generated HTML is pruned** each build, so local output matches CI.
8. **chart-series.json and chart_data.py.** `chart-series.json` is left in place but no longer read (DESIGN.md and the homepage cite it); delete it at cutover. `chart_data.py` and `--refresh-chart-data` are deleted.

## Re-verify (run from the PR checkout)
```
uv run --system-certs --extra build gridflow-build --check
uv run --system-certs --extra build --extra distil pytest -x -q
uvx --system-certs ruff check src tests
uvx --system-certs ruff format --check src tests
htmlhint --config .htmlhintrc "site/hifi/**/*.html"
lychee --no-progress --offline --include-fragments './site/hifi/**/*.html'
grep -rlE 'Illustrative snapshot|"seed"' site/hifi/data-sources/*.html
ls site/hifi/data-sources/neso_data_portal/
uv run --system-certs --extra distil gridflow-distil --dry-run
```

## Open issues
- **No new chart is visible on the built site yet.** All 4 specimens are authored overrides, so none of their charts show until 25b retires the overrides. The 35 template pages lost their old mean-of-first-column charts and now show none. The 42 authored overrides with seed opts now draw nothing.
- **system_prices silver has exact duplicate rows** per timestamp (695 in September). The spec deduplicates them; enforcing the dedup key in silver is gridflow work.
- **Silver changed during the run.** Phase 22's ingest was writing to silver (fuelhh now ends 2026-09-26). The committed series are a snapshot; re-run the distil before merging if a fresher window is wanted.
- **25b:** restyle the chart section and renderers, render the `page:` fields, add word budgets, retire the overrides.
- **Phase 26:** write `page:` into the notes, then re-mirror, distil and commit the series with each batch, and delete the staged specs.
- **Process note:** my first local commit accidentally swept in earlier-staged deletions. I rewound the unpushed branch (`git reset` to `8c5f0e0`) and recommitted cleanly; nothing was force-pushed.
