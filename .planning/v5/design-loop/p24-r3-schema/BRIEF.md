# Dataset page, round 3: the schema and sample rows (three variations of option 3)

You are one of three designers, each taking a different direction (yours is in your prompt). Read this
brief fully, then the files it names.

Paths:
- Repo (READ ONLY): `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end` (`<repo>`).
- `<p24>` = `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\p24`.
  Write ONLY inside `<p24>\r3-schema\<N>\`.

## Where we are

- Round 2 made five designs of the silver section; round 2's brief is `<p24>\r2-schema\BRIEF.md` and it
  still binds (strata ground, rulings, facts only from `<p24>\pack\SPECIMENS.md` and `specimens.json`,
  every dataset shape must hold). Read it.
- Bobbo first picked option 4 ("one record, then many"). Built on real pages it reads as hard to follow:
  see the built page `...\scratchpad\pilot-artifact\data-sources\elexon\fuelhh.html` (silver section).
  He found it cluttered, faint and hard to read.
- **He now prefers option 3, "As the data scientist sees it"**: `<p24>\r2-schema\3\` (boards
  `3-*.dc.html`, generator `gen3.py`, `polars_repr.py`, `s3.css`, notes `3-notes.md`). Quote: "I like the
  idea of displaying the data in a table, as it looks in silver. That is quite intuitive. We just need to
  figure out a way to annotate it such that it's not too cluttered, and it's easy to read and understand."
  Option 3 put each column's meaning above it as a staircase; that is the part to rethink.

## The job

Keep the heart of option 3: the rows shown as a Polars frame, as they look in silver (shape line, column
name over its real Polars dtype, the rows, Polars' own box drawing). Find an annotation that tells a
newcomer what each column means, which columns identify a row, and what the lineage columns are, while
the frame stays the clearest thing on screen. Legibility first: body text at least 14 px, table text at
least 13 px, AA contrast on the silver ground (the built page's grey labels failed this).

## Boards

As round 2: the silver section only, 1440 wide, one board per specimen:
`<N>-fuelhh.dc.html`, `<N>-system-prices.dc.html`, `<N>-physical-flows.dc.html`,
`<N>-bmunits-reference.dc.html`, plus a phone board `<N>-fuelhh-390.dc.html`. Root height = `$preview`
exactly. A wide frame may scroll sideways inside its own container; the page must not.

## Rules and report

DESIGN.md is binding (no em dashes, eyebrows, middle dots, arrows as text, planning words, local-data
references, licence line; Red Hat Mono only for code, names, dtypes and values). Nothing clipped or
overlapping at any width. Detector `node <repo>\.claude\skills\impeccable\scripts\detect.mjs --json
<board>` returns `[]` on every board. Measure in your OWN browser tab (port 9700-9799, stop your server
after); never touch other tabs or processes. Your FINAL MESSAGE (under 200 words, first line your model
ID), also saved as `<N>-notes.md`: boards and heights, the idea in one sentence, new copy verbatim,
detector results, anything not done.
