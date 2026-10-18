# Template pass: report (seat's record of the agent's final message, 2026-10-18)

The agent could not write this file itself; this is its final report, recorded by the seat. Branch
`feat/neso-dp-template-pass` (11 commits off d327b76). The new authoring syntax is documented in
`.planning/v5/author-brief.md` on that branch (commit 42bde03) and in the doc blocks of `chart_spec.py` and
`page_fields.py`.

## Fixes

- **Wide tables:** a chart spec can list several columns of one row as series (`values`).
- **Axis floor:** a note may set `chart_view.y_min`. A key, not an automatic floor, so no existing chart changes.
  Missing periods break the line, and stacked areas now break at gaps too.
- **Related links:** a package page slug such as `neso_data_portal/aggregated-bsad` is accepted.
- **Notebook needs:** a clause there fails the build with a message saying what to write.
- **Raw files:** a family member may list up to four requests.
- **Long spans:** half-yearly or quarterly ticks on spans of one to three years.
- **Long names at 390 px:** keys and file ids in wells break on phones only. The variant heading was already fixed on
  main.
- **Held pages:** `held: true` (or a one-line reason per member). No chart, frame or notebook; the silver section lists
  the tables with why their rows are not shown; the hub links them normally.

## Pages that changed against main

Demand flexibility and Balancing Reserve auction results (ticks and wells), seven other pages (wells), and
`theme.css`. Every other page is byte-identical.

## Gates (agent's run, all exit 0)

pytest 204 passed · `gridflow-build --check` · htmlhint · lychee · detector `[]` on the four showcase pages.

## Demo

`demo/`: before and after screenshots of constraint breakdown (four reasons stacked) and Aggregated BSAD (floor and
gap), a held demo page (Dynamic Containment 4-day forecast), rendered HTML and the scratch notes.

## Open

The showcase notes (constraint breakdown, Aggregated BSAD) need updating on a vault branch to use the new options.
