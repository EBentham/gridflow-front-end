# Phase 24, round 1: the dataset page (shared brief for all five variant designers)

You are one of five designers working in parallel on the same page template, each from a different
direction (yours is in your prompt). Read this file fully, then the files it names.

Paths:
- Repo (READ ONLY; never edit, commit or push): `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end`
- Scratch: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\p24\`
  (below: `<p24>`). Write ONLY inside your own folder `<p24>\<LETTER>\`.

## What is locked (binding, do not relitigate)

- The design: `<repo>\DESIGN.md` and `<repo>\site\hifi\assets\tokens.css`. Read both fully. Palette, type,
  drawing language, strata, components, content rules and the do-not-use list all bind.
- The reference page: the locked homepage `<repo>\.planning\v4\design-loop\r3-7\R3-final.dc.html`
  (generator `gen_b.py` beside it). Your dataset page must read as the same site: same masthead, same
  petrol sky, same strata language, same notebook/DataFrame components where you use them. Reuse its
  SVG pieces and CSS where they fit.
- The artboard format, honesty rules and verification recipe: `<repo>\.planning\v4\design-loop\SHARED.md`
  § "Honesty rules", § "Do-not-use", § "The .dc.html artboard format", § "Verify before you report".
  (That file was the homepage brief: ignore its round history and its content section; this file replaces
  them. Its colour hexes are superseded by tokens.css where they differ.)
- The frontend-design skill: `<repo>\.claude\skills\frontend-design\SKILL.md`.

## The job

Design the ONE template every dataset page on the site will use (about 165 pages, later folded into
families). The page is documentation for one dataset that gridflow ingests. It must say only what has
been checked against gridflow code and real silver data: a short summary, a real chart, what the data
is, how it is used, and how to get it. Readers: data scientists and recruiters in energy trading who want
to judge in seconds whether the author knows this data.

Render your template for all four specimens. The template must hold for every one:
1. `elexon/fuelhh`: generation by fuel type, half-hourly (the main specimen)
2. `elexon/system_prices`: a price series with negative prices
3. `entsog/physical_flows`: a sparse daily gas flow
4. `elexon/bmunits_reference`: a reference table with no time axis (no time chart; show what is honest)

## Content: the fact pack is your only source of facts

`<p24>\pack\SPECIMENS.md` and `<p24>\pack\specimens.json`: schema, sample rows, chart series (with
dataset, unit, window and aggregation), the exact workbench call, the raw endpoint, caveats, related
datasets. Every number, column name, code and claim on your boards comes from the pack. The current
site pages for these datasets contain errors (e.g. the FUELHH page claims solar): never copy from them.
Prose (the one-liner, "what it is", "how it's used") you write yourself from the pack's facts, within
your word budgets; domain uses must be generic and true (e.g. "residual-demand features for a price
model"), never a claim about a specific firm or a number not in the pack. List every prose line you
wrote in your report as NEW COPY.

Starting proposal for the content model (Bobbo will cut it; you may cut, merge, reorder or add, and
must justify each change in one line):
- one line on what the dataset is
- a real chart with dataset, unit and window
- "What it is" in 60 words or fewer
- "How it's used", as 2 to 3 domain uses
- a compact fact list: grain, cadence, history, publication lag, units
- the silver schema
- sample rows, styled as the homepage DataFrame
- how to get it: the `data.<source>.query(...)` workbench call (exactly as in the pack) plus the raw
  endpoint
- up to three real caveats
- related datasets

Site chrome: masthead and nav as on R3-final, with "Data sources" as the current page; a breadcrumb or
vendor back-link if your direction needs one; footer from R3-final. No planning leakage: no "coming
soon", no planned/shipped labels, no phase codes, no counts of future work.

## Boards to write

Four files in `<p24>\<LETTER>\`, named exactly `<LETTER>-fuelhh.dc.html`, `<LETTER>-system-prices.dc.html`,
`<LETTER>-physical-flows.dc.html`, `<LETTER>-bmunits-reference.dc.html`. Each 1440 px wide, height what
the page needs (at most 5200 px; the root's fixed height and `$preview` must match exactly). Same template
across the four; only the data changes (and whatever the shape forces, e.g. no time chart for the
reference table: say how the template handles it).

The page must plausibly reflow to 390 px later (Phase 25b builds it in real HTML): prefer compositions
that collapse to one column; do not rely on absolute positioning for text blocks.

## Verify, then report

Run SHARED.md's verification recipe on all four boards (detector must return `[]` for each; measure
layout numerically if you have browser tools, use a port in 9500-9599 and stop the server after).

The harness blocks subagent writes of files named REPORT.md, so your report is your FINAL MESSAGE
(under 300 words; also try saving it as `<p24>\<LETTER>\<LETTER>-notes.md`), first line your model ID:
- the board paths and each board's height
- the one idea of your direction, in one sentence
- **CONTENT MODEL**: the ordered list of blocks with a word budget for each (this is what Bobbo will lock)
- how the template handles the no-time-axis and sparse cases
- every NEW COPY line, verbatim
- detector result per board; how layout was verified
- anything you could not do
