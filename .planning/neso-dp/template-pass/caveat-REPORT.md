# Caveat field and raw samples: template pass report (ruling 66)

Branch `feat/neso-dp-template-pass` (PR #60), worktree `C:\gridflow-wt\fe-template`. Three commits, not pushed.

## Field spec

**`caveat:`** is one plain line naming a table's open question. It is printed with the rows. The budget is 16 words, the same as `held`, and is checked by `anatomy_errors`.

| Where | Field | Allowed when |
|---|---|---|
| One-table page | `page.caveat` | The page is not held and has no family. |
| Family page | `page.family.members[i].caveat` | The page is not held, and the member has no `held:`. |
| Held page (raw sample) | `page.raw_feed.sample.caveat` (required) | The page is held. |

A page or member with a caveat is a full page or member. Chart, frame, column guide, notebook and their artefacts all work as normal, and only the line is added. The build rejects:

- a page-level `caveat` on a family page;
- a `caveat` on a held page;
- a member with both `held` and `caveat`;
- a caveat over 16 words.

Page-level `held:` is unchanged. It stays for packages with no silver rows (bronze only, files only, licence carve-outs), and it still fails on any chart, sample, notebook or locations file. A member-level `held:` on a normal family page still prints "Rows not shown: ...". Use it for a bronze-only member of a mixed family.

One-table page:

```yaml
page:
  # ...the full anatomy: chart, chart_view, record, notebook, related...
  caveat: NESO's files carry no publication time, so these rows are the latest file.
```

Family page (a mixed package: one table with rows, one bronze only):

```yaml
page:
  # ...full anatomy for the frame's table (the lead, or record.select.silver)...
  family:
    slug: eac-mock-auction-results
    members:
      - {dataset: eac_mock_results_summary, differs: Each auction's summary, request: "GET https://...",
         caveat: "Mock auction data, not real procurement; the timestamps' clock is not stated."}
      - {dataset: eac_mock_results_daily_summary, differs: The daily summary, request: "GET https://...",
         held: Mock auction data; NESO's daily files hold headers only.}
```

Inside a `{...}` member entry, a caveat that holds a comma must be quoted. Unquoted, YAML splits it and the build fails on an unknown key.

Ruling 66's example caveat is 23 words, which is over the budget. The brief tells writers to trim it, for example to "NESO's files carry no publication time, so these rows are the latest file." (13 words).

## Where it renders

All three placements use existing classes only. There is no new CSS or colour, and no label, badge or status word.

- **One-table page:** a second `<p class="spec__cap">` just above the frame, under the frame's own caption.
- **Family page:** a `<p class="ds-variants__d">` under the member in the raw feed, beside what differs. If the frame shows that member's table, the caveat also prints above the frame. The frame's table is matched with `artefacts.sample_silver`.
- **Raw sample:** a `<figure class="ds-raw-sample">` in the bronze stratum, after the commands well. It holds:
  - a heading (`ds-variants__h`), for example "The header and first eight rows of `file.csv`, as fetched";
  - the caveat (`ds-variants__d`);
  - a `ds-well` with one line per row, wrapping after commas.

  `ds-raw-sample` has no CSS rules of its own.

One limit to know: a family page still shows one frame, chart and notebook, for one table. Other members with rows get their caveat line under the member but no frame of their own. Giving every member a frame would be a separate anatomy change.

## Raw-only answer

**Yes, added this round.** A held page can now show the header and first eight lines of one bronze file, exactly as NESO sent it, together with its caveat:

```yaml
page:
  held: Rows repeat and there is no settlement-run column.
  raw_feed:
    sample:
      table: daily_balancing_costs     # optional; default the page's table (a family's lead)
      file: q1_cost_fy2627.csv         # optional; NESO's file name; default the newest capture
      caveat: Rows repeat with no run column, so revisions cannot be told apart.
```

- **Generating it:** `gridflow-sample --dataset <vendor>/<key>` (distil extra, `--bronze-path` or `$GRIDFLOW_BRONZE_PATH`) reads `C:\gridflow-data\bronze` read only. It writes `site/hifi/data/raw-samples/<vendor>/<key>.json` with a digest of the table and file choice. The reader is the stdlib module `src/gridflow_front_end/raw_sample.py`.
- **Build checks:** the build fails on a missing raw sample, a stale digest, or a leftover raw sample on a page that does not ask for one. Only a held page may carry one.
- **Which files:** only CSV and text files can be sampled; xlsx, NUL bytes and lines over 4000 characters are rejected. Windows-1252 files (the BSUoS forecasts) are read as such, and the encoding is recorded. A header-only file prints as "the file holds no rows".
- **Checked on real bronze, read only:**
  - `daily_balancing_costs`: UTF-8, 9 lines;
  - `bsuos_monthly_forecast_summary`: read as cp1252;
  - `eac_mock_results_daily_summary`: header only;
  - `contract_transfer_obligation`: read without problems.
- **Not for licence carve-outs:** levelised cost of hydrogen and the GIS boundaries keep `held` with no sample. The template cannot tell a carve-out apart, so writers must not add `raw_feed.sample` there.
- **Name the file:** writers should name `file` whenever a table has more than one file. Captures from one ingest share a fetch time, so "newest" is arbitrary among them. For example, `bsuos_monthly_forecast_summary` picked a 2021 file.

## Commits

1. `2bd1b11` feat(page): a caveat line for rows that carry an open question. Covers `page_fields.py`, `build.py` and `dataset.html.j2`, plus tests.
2. `e6b6fda` feat(page): a held page may show one raw file's first rows. Covers the new `raw_sample.py`, the artefact path and digest, the bronze path, the `gridflow-sample` hook, the build check and the template block, plus tests.
3. `b1859d0` docs(planning): author brief on converting held pages to caveats. This is `.planning/v5/author-brief.md`; the `page_fields.py` docstring is updated in commits 1 and 2.

New tests:

- **`tests/test_dataset_page.py`:**
  - the caveat renders just above the frame on fuelhh, with all artefacts and no errors;
  - a page without a caveat renders as before;
  - family member caveats render on demand-outturn.
- **`tests/test_package_pages.py`:**
  - the caveat budget and where a caveat may stand;
  - member caveat rules;
  - a held page plus a sample, notebook or locations file still fails;
  - the raw sample's fields, the reader (newest or named file, cp1252, errors), rendering, the header-only case, and stale, missing or leftover files.

## Gate results

All five gates were run in the worktree on the committed state:

| Gate | Result |
|---|---|
| `uv run --system-certs --extra build pytest -x -q` | 217 passed |
| `uv run --system-certs --extra build gridflow-build` | 77 pages, 7 hubs and the landing written |
| `uv run --system-certs --extra build gridflow-build --check` | OK, idempotent |
| `htmlhint --config .htmlhintrc 'site/hifi/**/*.html'` | 198 files, no errors |
| `lychee --no-progress --offline --include-fragments './site/hifi/**/*.html'` | 0 errors |

**Byte differences: none.** The whole `site/hifi` tree was snapshotted before any change and compared after each commit with `diff -rq`. It is identical, including `demand-flexibility.html`, the one page with a member-level `held`. No note on this branch uses the new fields yet, so no page changed.

Ruff is clean on every file I touched, apart from formatting and lint findings that were already there (`page_fields.py` formatting, one ISC004 in `build.py`).

The new markup (caveat page, family page, raw-sample page) was rendered to the scratchpad and passes htmlhint. It has not been looked at in a browser: the browser pane cannot open local files. Demo pages:

- `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\demo-site\data-sources\elexon\demo-caveat.html`
- `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\demo-site\data-sources\elexon\demo-family.html`
- `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\demo-site\data-sources\elexon\demo-raw.html`
