# Phase 27, round 1: the top pages (shared brief for all five variant designers)

You are one of five designers working in parallel, each from a different direction (yours is in your
prompt). Read this file fully, then the files it names.

Paths:
- Repo (READ ONLY; never edit, commit or push): `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end`
- Scratch: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\p27\`
  (below: `<p27>`). Write ONLY inside your own folder `<p27>\<LETTER>\`.

## What is locked (binding)

- The design: `<repo>\DESIGN.md` and `<repo>\site\hifi\assets\tokens.css`. Read both fully.
- The reference page: the locked homepage `<repo>\.planning\v4\design-loop\r3-7\R3-final.dc.html`
  (generator `gen_b.py` beside it). Your pages must read as the same site: same masthead and nav, petrol
  sky, strata language, entries (never cards), notebook component where you use one. Reuse its SVG pieces.
- Format, honesty rules, verification recipe: `<repo>\.planning\v4\design-loop\SHARED.md` § "Honesty
  rules", § "Do-not-use", § "The .dc.html artboard format", § "Verify before you report" (ignore its round
  history and content section; tokens.css supersedes its hexes).
- The frontend-design skill: `<repo>\.claude\skills\frontend-design\SKILL.md`.
- For reference only (a different page type, not yours to copy): the dataset-page variants in
  `...\scratchpad\p24\A..E\` show how other designers carried the system onto a documentation page.

## The fact pack is your only source of facts

`<p27>\pack\TOPPAGES.md` and `<p27>\pack\toppages.json`: vendors, dataset lists, architecture (layers,
paths, formats, views, CLI), the five models with their true status and metrics, and the chart series you
may draw. Never copy from the current site pages. Key rulings already in the pack you must respect:
- Do NOT show the 29 NESO Data Portal stubs, un-ingestable or deferred datasets, or anything "planned".
- The headline dataset count is pending Bobbo's page-set ruling: write it as a visible placeholder
  `[N datasets]` (and per-vendor `[n]` where counts may change), never a number you choose.
- Model status: show what exists (the wind and solar models have never been trained, whatever the
  notebooks README says; demand has two versions). Neutral wording: no planned / shipped / trained labels,
  no F-codes, no counts of future work, no dashed "not built yet" styling.
- Any chart: real series from the pack only, stating dataset, unit and window; carry the SMP caption the
  pack requires if you draw it.

## Boards to write (one direction across all four, so the pages feel like one site)

In `<p27>\<LETTER>\`, named exactly:
1. `<LETTER>-data-sources.dc.html`: the data-sources landing (every vendor gridflow ingests, how to find a
   dataset, how the catalogue is organised).
2. `<LETTER>-vendor-elexon.dc.html`: the vendor-hub pattern, rendered for Elexon (33 datasets, grouped as
   the pack groups them). The pattern must also hold for a vendor with 3 datasets: say how.
3. `<LETTER>-architecture.dc.html`: bronze, silver, gold, the build and the gates, with real names.
4. `<LETTER>-models.dc.html`: a landing for the five models.
Each 1440 px wide, height what the page needs (at most 6000 px; root height = `$preview` exactly). Prefer
compositions that collapse to one column at 390 px later; no absolutely positioned text blocks.
Do NOT draw node-and-arrow flowcharts for the architecture (do-not-use list): use the strata and drawings.

## Verify, then report

Run SHARED.md's verification recipe on all four boards (detector `[]` each; measure layout numerically if
you have browser tools, a port in 9600-9699, and open your OWN browser tab; stop your server after).

The harness blocks files named REPORT.md: your report is your FINAL MESSAGE (under 350 words, first line
your model ID; also save it as `<p27>\<LETTER>\<LETTER>-notes.md`):
- board paths and heights
- the one idea of your direction, in one sentence
- per page, the ordered blocks (content model) in one line each
- every NEW COPY line, verbatim (in the notes file if long; summarise in the message)
- detector result per board; how layout was verified; anything you could not do
