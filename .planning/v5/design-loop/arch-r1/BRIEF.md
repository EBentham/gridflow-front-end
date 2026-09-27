# Architecture page, round 1 (shared brief for three designers)

You are one of three designers working in parallel on the gridflow docs site's Architecture page, each from a
different direction (yours is in your prompt). Read this brief fully, then the files it names.

Repo (READ ONLY except your own folder; never commit, branch or push):
`C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end` (below `<repo>`). Design-loop folder:
`<repo>\.planning\v5\design-loop\` (below `<dl>`). Write ONLY inside `<dl>\arch-r1\<N>\`.

## Read, in order

1. `<dl>\arch-direction.md`: the agreed content direction (binding: page order, what each section holds, cuts).
2. `<dl>\arch-pack\ARCH-PACK.md` and `pack.json`: the verified copy, labels, links and real snippets. **Every
   fact, label and snippet on your board comes from the pack.** You may shorten or reorder its wording; you
   may not add claims. Its "Cut: do not say" list is binding.
3. `<repo>\DESIGN.md` and `<repo>\site\hifi\assets\tokens.css`: the locked design system and do-not-use list.
4. The top-page language Bobbo picked, direction A "Sections": boards
   `<dl>\p27-r1\canvas\project\A-*.dc.html` (read A-data-sources and A-vendor-elexon for the chrome, rhythm and
   section anatomy; A-architecture is a rejected page, look at it only to avoid it), generator code in
   `<dl>\p27-r1\A\` (reuse `frame.py`, `scenery.py`, `crop.py` helpers if useful), notes `A-notes.md`.
   Your page must sit with those pages as one site: same masthead, nav, type scale, section rhythm and foot.
5. `<repo>\.planning\v4\design-loop\SHARED.md`: the .dc.html board format and the verification recipe.
6. For context on what Bobbo rejected in the old page: `<repo>\site\hifi\architecture.html` and
   `<dl>\arch-content-check.md`.

## The page's job

Show a full-stack data-science recruiter in energy trading that Bobbo designs and builds production-quality
data systems. In about a minute: the whole system in one picture; one hard problem handled properly
(revisions: what was known, and when); evidence it stays correct; where to look in the code.

## What to build

One board, `arch-<N>.dc.html`, 1440 px wide, the whole page (masthead to foot), root height = `$preview`
exactly. Sections in the direction's order: opening + scope line; the system drawing with its keyed index;
the row's journey (7 stops, stop 5 highlighted); how it stays correct; where to look.

- Wrap each of the five sections in an element with `data-section="opening|drawing|journey|correct|look"`
  (the picker crops by it so Bobbo can compare and comment section by section).
- **The drawing** is the centrepiece and the hardest part: accurate, in the site's "above ground, below
  ground" language, never a node-and-arrow flowchart, never a literal borehole or drill column. Sources above
  ground, cables into bronze, silver, gold, readers at the foot; gridflow_models links to `models.html`, and
  shows what the pack says about how it reads gridflow (notebooks through the client; training and backtests
  read silver files directly). Labels on the drawing are short; the keyed index carries the lines and GitHub
  links (DESIGN.md "Keyed index").
- **The journey** shows the real object at each stop from the pack (command, request, bronze file and
  sidecar, the silver vintages, the `_latest` choice between 9.56 and 110.00, the gold row, the Polars read).
  Stop 5 is the hero moment. Code in Red Hat Mono in the site's code treatment.
- **How it stays correct** is short: five one-line rules plus run tracking and CI, no more than about one
  screen at 1440.
- **Where to look** is slim, about ten links.
- It must plausibly reflow to 390 px later: no absolutely positioned text outside the drawing's SVG; wide code
  and tables scroll inside their own container. The drawing may be an SVG that scales, with the keyed index
  as HTML beside or below it.

## Rules

DESIGN.md is binding: no em dashes, no tracked all-caps eyebrows, no middle-dot strings, no "→", no italic or
coloured single headline word, no stat strips, no cards as default container, no planning words, no
local-data references, AA contrast, Red Hat Mono only for code, paths, column names and values.

## Verify, then report

Run SHARED.md's verification recipe on your board: impeccable detector
`node C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.claude\skills\impeccable\scripts\detect.mjs --json <board>`
returns `[]`; measure layout numerically in your OWN browser tab if you have browser tools (serve your folder
on a port in 9700-9799, stop the server after). Never kill or stop other processes. The harness blocks files
named REPORT.md: your report is your FINAL MESSAGE (under 250 words, first line your model ID), also saved as
`<dl>\arch-r1\<N>\<N>-notes.md`: board path and height, the idea in one sentence, how the drawing and the
journey work, any pack wording you changed, detector result, anything you could not do.
