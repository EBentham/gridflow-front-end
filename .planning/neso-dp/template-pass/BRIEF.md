# Template pass: fix the dataset-template limits the NESO showcase batch hit

Approved by Bobbo 2026-10-18 (ruling 62, `.planning/neso-dp/OVERNIGHT-PLAN.md` Step 1). One agent, Opus 5.5 · high.
You change the build and template only; you write no dataset page and edit no vault note.

## Where

- Worktree: `C:\gridflow-wt\fe-template`, branch `feat/neso-dp-template-pass` off `origin/main` (d327b76). Work only
  here. Never touch the main checkout or any other worktree.
- Code: `src/gridflow_front_end/` (`build.py`, `chart_spec.py`, `chart_svg.py`, `distil.py`, `page_fields.py`),
  `templates/dataset.html.j2`, `site/hifi/assets/*.css`, `tests/`.
- The full build needs the vault mirror in this repo (`vault/`), the gridflow repo
  (`C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\`) and local silver (`C:\gridflow-data\silver\`, read only).
  Build: `uv run --system-certs --extra build gridflow-build` (all pages) or `--only <vendor>/<key>`.
- The showcase author reports that found these limits, for detail and reproduction:
  `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\{dfs,eac-br,bsad,constraint}\*-author.md`
  ("Template problems" sections).
- Preview server for your own checks: port 9931 (`uv run gridflow-serve` on a free port, or `python -m http.server`).

## The fixes

1. **Several columns of one row as chart series.** Today a chart plots one `value`; series come only from a `group`
   column. Add a spec option (for example `values: [col, ...]` with labels) that unpivots a wide table's columns into
   series, working with the existing chart types (line, stacked-area). Test case: `constraint_breakdown`'s four
   reasons (largest loss, inertia, voltage, thermal; cost columns), silver
   `C:\gridflow-data\silver\neso_data_portal\constraint_breakdown\`.
2. **Y-axis floor.** `chart_svg.nice_ticks` floors `lo` a whole step below zero for tiny negatives (constraint
   breakdown: five dates down to -£232,717 push the axis to -20M). Either make the floor smarter (only add a negative
   step when the negative is a real share of a step) or add a spec key (`y_min`) — your call, say why. Also make it
   possible for a data gap to read as a gap rather than as a line along zero (Aggregated BSAD's 2020-21 gap sits on
   the axis line): if the series has missing periods, the line should break, not join or drop to zero.
3. **Related links to a hyphenated package page.** `page_fields._DATASET_RE` (`^[a-z0-9_]+/[a-z0-9_]+$`) rejects a
   package slug like `neso_data_portal/aggregated-bsad`. Allow package page slugs (vendor dir stays as is), and make
   the link resolve to the right page; reject a slug that names no page in the page set, as now.
4. **`notebook.needs` sentence.** The template renders "with {needs} ingested." (`templates/dataset.html.j2:219`);
   two writers wrote a clause there and produced broken grammar. Either reword the template so any short noun phrase
   reads well, or validate the field (reject verbs/clauses, e.g. a value containing "ingested", a semicolon, or a
   leading verb) so the build fails with a clear message. Prefer validation plus keeping the sentence, so every other
   page stays byte-identical; tell the writer what is allowed in the error message and in `page_fields.py`'s doc block.
5. **Two raw files per family member.** `page.family.members[].request` is one string, and `request_lines` /
   `_url_row` handle one URL. Package tables often have a current and an archive file. Allow a member to list more
   than one request (a list), each wrapped like the single one. Bobbo's ruling 6 says held tables are "listed with
   their raw files".
6. **Time axis on long spans.** For spans over 400 days `chart_svg._time_axis` ticks only on 1 January (a 19-month
   chart shows one tick). Add quarterly or half-yearly ticks so a span from about 13 months to about 4 years gets at
   least 3 labelled ticks; keep the current yearly ticks for longer spans.
7. **Long names at 390 px.** The family variant heading (`build.py` ~1489, `"key": f"{doc.vendor_id}/{mem.dataset}"`,
   printed at `templates/dataset.html.j2:139`) is not passed through `_breakable`, so
   `neso_data_portal/eac_br_results_sell_orders` overruns the gutter at 390. Long tokens inside the command wells
   (`.ds-well .nw { white-space: nowrap }`, `command_row`) also clip at 390. Fix both so nothing clips at 390 px and
   nothing changes at 768 px and up.

## Byte-identical rule

Every page whose note does not use a new option must render byte-identical to `origin/main`. Before you change code,
build all pages and copy `site/hifi/` (generated pages) to your scratch folder as the baseline. After, build again and
diff the whole tree. Report every page that differs and why (fix 7 may deliberately change pages; fix 6 may change
charts on long-span pages; list each). Do not touch hub or landing layout.

## Gates (all must pass; report each exit code)

- `uv run --system-certs --extra build pytest -q` (add tests for every fix: spec validation, unpivot, floor, gap,
  related slug, needs validation, multi-request, ticks, breakable heading)
- `uv run --system-certs --extra build gridflow-build --check`
- `htmlhint --config .htmlhintrc 'site/hifi/**/*.html'`
- `lychee --offline --include-fragments './site/hifi/**/*.html'`
- `node .claude/skills/impeccable/scripts/detect.mjs --json <page>` on the four showcase pages
  (`site/hifi/data-sources/neso_data_portal/{demand-flexibility,eac-br-auction-results,aggregated-bsad,constraint-breakdown}.html`)
  — must stay `[]`.

## Demonstrate, don't ship notes

Show fixes 1 and 2 on the real data in a scratch copy only: copy `vault/neso_data_portal/constraint-breakdown.md` and
`aggregated-bsad.md` to your scratch folder, add the new options there, render them to a scratch output, and save
screenshots or the rendered HTML in `.planning/neso-dp/template-pass/` (in the MAIN checkout path
`C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\template-pass\`). Do not commit any change
under `vault/` (it is a mirror of the canonical vault; the seat updates the two showcase notes later on a vault
branch).

## Authoring docs

Update `.planning/v5/author-brief.md` (in your worktree) and the doc block in `chart_spec.py` / `page_fields.py`
so the next writers know the new options: `values`, the floor/gap behaviour, related package slugs, the `needs`
rule, member request lists.

## Git

Commit on `feat/neso-dp-template-pass` in the worktree, conventional commits, one concern per commit (a fix with its
tests is one commit). End each message with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Do not push,
do not open a PR, do not merge; the seat does that.

## Report

Write `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\template-pass\REPORT.md`: per fix,
what changed (file:line), the new authoring syntax with an example, tests added; the byte-diff list; gate exits; demo
file paths; anything you could not do. Plain English, no planning codes. Final message: under 150 words, the report
path first.
