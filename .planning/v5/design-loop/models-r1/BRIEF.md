# Models page, round 1 of the polish (shared brief for three designers)

You are one of three designers working in parallel on the gridflow docs site's Models page, each from a
different direction (yours is in your prompt). Read this brief fully, then the files it names.

Repo (READ ONLY except your own folder; never commit, branch or push):
`C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end` (`<repo>`). Design loop: `<repo>\.planning\v5\design-loop\`
(`<dl>`). Write ONLY inside `<dl>\models-r1\<N>\`.

## Read, in order

1. `<dl>\models-decisions.md`: Bobbo's feedback and rulings (binding).
2. `<dl>\models-pack\MODELS-PACK.md` and `pack.json`: the verified content, including the chain as nodes and
   edges. Every fact, label and number on your board comes from the pack. You may shorten; you may not add.
3. The page Bobbo picked in round 1: `<dl>\p27-r1\canvas\project\A-models.dc.html`, generator
   `<dl>\p27-r1\A\p_models.py` (reuse `frame.py`, `scenery.py`, `hp.py` helpers from `<dl>\p27-r1\A\`), notes
   `A-notes.md`. Also look at `A-data-sources.dc.html` and the locked architecture page
   `<dl>\arch-r2\arch-r2.dc.html` so the Models page sits with them as one site.
4. `<repo>\DESIGN.md`, `<repo>\site\hifi\assets\tokens.css`, and `<repo>\.planning\v4\design-loop\SHARED.md`
   (board format and verification recipe).

## What Bobbo wants

- **Keep the top:** the sky with its images (demand, wind, solar, the plant fleet) and the cables running from
  each image to the model that uses it. That is the part he likes.
- **Less clutter.** Round 1 A is too busy.
- **High level.** Each model: what it does in a line, what feeds it, how it connects to the others. At most a
  light headline score where the pack has a validated one (demand). No inner workings: no gates, coverage
  failures, artefact names, fold counts or version histories. He will extend the page later.
- **Show the true chain**, not five sibling models: the demand, wind and solar forecasts, the merit-order stack
  (constructive, nothing to fit) and fundamentals SMP, which clears residual demand through the stack. Follow
  the pack exactly on what the published SMP run fed in (recorded demand, wind and solar).

## Boards

`<N>-models.dc.html` at 1440 wide (whole page, masthead to foot) and `<N>-models-390.dc.html` (phone), root
height = `$preview` exactly. Wrap sections in `data-section="..."` (the picker crops by it). Links: models to
their GitHub paths from the pack (github.com/EBentham/gridflow-models, private for now, link anyway).

## Rules

DESIGN.md is binding: no em dashes, eyebrows, middle dots, "→", italic headline words, stat strips, cards as
default container, planning words (planned, trained, live, in service, coming), local-data references; AA
contrast; Red Hat Mono only for code, names and values.

## Verify, then report

Detector `node <repo>\.claude\skills\impeccable\scripts\detect.mjs --json <board>` returns `[]` on both boards;
measure in your OWN browser tab (port 9700-9799, stop the server after); never kill or stop other processes.
The harness blocks REPORT.md: your report is your FINAL MESSAGE (under 200 words, first line your model ID),
also saved as `<N>-notes.md`: boards and heights, the idea in one sentence, what you cut from round 1, new copy
verbatim, detector results, anything not done.
