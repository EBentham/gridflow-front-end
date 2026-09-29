# Notebook render fixes: named-index DataFrames, lead code wrap

Worktree `scratchpad/p26-entsoe`, branch `v5/p26-entsoe`. Not committed.

## Bug 1: headers one column right on a named-index DataFrame

**Cause.** pandas `to_html()` gives a frame a second header row when its index has a name: row 1 is
`[columns.name or "", *labels]` and row 2 is `[index.name, "", ...]`. `scripts/run_notebooks.py`
`dataframe()` collects every `<th>` in `<thead>` into one flat list, so a pivot is stored as
`["zone", "DE", "FR", "ts", "", ""]`. `_output_html` in `build.py` expected `len(columns) == width + 1`.
Otherwise it assumed the corner cell was missing and prepended `<th></th>`. The result was one header
row of 7 cells, with `DE` over the `FR` values. A frame whose index alone is named
(`set_index` / `groupby`) is hit the same way. A frame whose columns axis alone is named has one row
and was already correct.

**Diff.**
- `src/gridflow_front_end/build.py` `_output_html`, `df` branch: added a `tr()` row helper. When there
  are rows and `len(columns)` is a whole multiple (above one) of `width + 1`, the list is cut back into
  header rows of `width + 1`, which reproduces pandas' two-row header. The single-row path is unchanged
  and now goes through `tr()`: `tr(cols)` or `tr(["", *cols])` emits the same bytes as before.
- `site/hifi/assets/theme.css`: `.df thead tr:not(:last-child) th { border-bottom: 0; }`, so the ink
  rule sits only under the last header row. Tables with one header row are unaffected.
- The stored JSON shape and `scripts/run_notebooks.py` are untouched, so no notebook needs re-running.
- New `tests/test_notebook_named_index.py`: literal pandas 3.0.2 `to_html()` for four cases: pivot
  with both axes named, index named only, columns named only, and plain. Each is parsed with the
  runner's own three regex lines and rendered. The tests assert that every row has 3 cells, that `DE`
  and `FR` sit in the same columns as `1.5` and `2.00`, that the pivot keeps
  `[["zone","DE","FR"],["ts","",""]]`, and that the plain frame's full HTML matches a literal.

**Reproduction.** Replaying the old logic on the same inputs gives one header row,
`['', 'zone', 'DE', 'FR', 'ts', '', '']`, with `DE` in column 2 and its value in column 1. That is the
reported misalignment, so the new tests fail on the old code.

**Byte-identity.** Old and new renderers were compared side by side on all 47 stored `df` outputs in
`site/hifi/data/notebooks/**`: 0 differ. (A first before/after hash run flagged
`entsoe/forecast_margin.json`, but another agent had rewritten that file between the two runs. It
holds a plain one-row frame, and the old-vs-new comparison clears it.)

**installed_capacity rebuild.**
`uv run --system-certs --extra build gridflow-build --only entsoe/installed_capacity` wrote the page.
Its pivot renders as one header row, `['', 'DE-LU', 'BE', 'FR', 'NL']`, over rows such as
`['B01', '8855.90', '846.099', '1434.93000', '418.0']`, correctly aligned. It still clears axis names,
so the named case is covered by the tests above.

**Polars.** Polars `_repr_html_` (1.40.1) is `<small>shape</small>` plus a `<thead>` whose second row
is dtypes in `<td>`, with no `<th>` in body rows. The renderer is not involved: `dataframe()` in the
runner would raise `IndexError` on it (`re.findall("<th>...", row)[0]`) before anything is stored. Every
stored output has pandas' corner cell, so Polars frames never reach `_output_html` today.
**Gap (not fixed, out of scope):** a notebook cell that displays a Polars DataFrame crashes
`run_notebooks.py` with an uncaught `IndexError` rather than the script's own `RuntimeError`. MultiIndex
columns (`<th colspan=...>`) would also be missed by the `<th>` regex.

## Bug 2: inline code in the notebook lead overflows at 390 px

The notebook lead is the direct-child `<p>` of `.ds-gold .ds-lead` (`templates/dataset.html.j2`); the
bronze section shares `.ds-lead`. New rule in `theme.css`:
`.ds-gold > .ds-lead > p code { overflow-wrap: anywhere; }`. It does not reach the bronze lead or `.ds-need`.

Measured on `entsoe/generation_units_master_data` at 390x844, served from the worktree on a
temporary port with theme.css cache-busted. The lead code computes `overflow-wrap: anywhere`, the
bronze lead code stays `normal`, and the document scrollWidth is 390. The longest current token,
`silver_entsoe_generation_units_master_data` (42 chars), ends at 368 px against the paragraph's
374 px, so it fits either way. A synthetic 69-char call ends at 368 px with the rule and 426 px
without it.

## Results

- `uv run pytest -x -q`: 1 failed, 65 passed. The failure is the expected
  `tests/test_dataset_page.py::test_a_page_without_a_page_block_is_blank`, because
  `entsoe/water_reservoirs` is now written. Left alone.
- `uv run pytest -q` (full): 1 failed (the same test), 106 passed. New tests: 7 passed, with
  `test_notebook_table.py`.
- `uvx ruff` 0.16.9 (not in the project venv). `ruff format --check` on build.py and the new test
  passes. `ruff check` on the new test passes. On build.py, `ruff check` reports one pre-existing ISC004
  at `_fold_css` line 1197, present before this change and not touched. The baseline format diff in
  build.py was inside the rewritten `df` header block and is gone.
