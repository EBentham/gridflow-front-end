# Dataset page, round 2: the schema and sample rows section (shared brief for five designers)

You are one of five designers working in parallel on ONE section of the dataset page, each from a
different direction (yours is in your prompt). Read this brief fully, then the files it names.

Paths:
- Repo (READ ONLY; never edit, commit or push): `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end`
- Round-1 work: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\p24\`
  (below: `<p24>`). Write ONLY inside your own folder `<p24>\r2-schema\<N>\`.

## What is decided (binding)

Bobbo picked **direction A, "The section"** (`<p24>\A\`: boards `A-*.dc.html`, generator `gen_A.py`,
`content.py`, `a.css`, notes `A-notes.md`). Read A fully: your section must slot into A's page. In A the
page descends through the strata, and the schema and sample rows sit in the **silver** stratum
(`--silver-tint` ground, diagonal hatch in `--silver-deep`, wavy contact lines above and below). The
design system is binding: `<repo>\DESIGN.md`, `<repo>\site\hifi\assets\tokens.css`, the do-not-use list,
and the .dc.html format and verification recipe in `<repo>\.planning\v4\design-loop\SHARED.md`.

Bobbo's verdict on A's current schema and sample rows: **"I am not a huge fan of this formatting / style.
Let's improve it."** Your job is a better version of that one section.

Other rulings that bind this section:
- **No local-data references anywhere.** No "held locally", no local row counts, no local date ranges, no
  "rows in August", no "snapshot of <date> on this machine". The sample rows are real example rows (fine);
  their caption must not talk about the local store. History, where mentioned, is what the vendor's API
  provides, and only if evidenced.
- No caveats section on the page (removed). A fact a reader needs to read the table correctly (e.g. a
  signed column) belongs in that column's meaning, briefly.
- Everything else in DESIGN.md (no em dashes, no planning leakage, no filler, Red Hat Mono only for code,
  column names, dtypes and values).

## Facts

Only from the fact pack: `<p24>\pack\SPECIMENS.md` and `specimens.json` (schema: column, dtype, meaning;
8 real sample rows; key columns; lineage columns). A's `content.py` has A's wording of the column meanings
(reuse or improve, never add unverified claims).

## Boards to write

One board per specimen, containing ONLY the silver stratum section as it would sit in A's page (with its
contact lines at top and bottom, the section heading and everything inside the stratum), 1440 px wide,
height as the content needs (root height = `$preview` exactly):
`<N>-fuelhh.dc.html`, `<N>-system-prices.dc.html`, `<N>-physical-flows.dc.html`,
`<N>-bmunits-reference.dc.html` in `<p24>\r2-schema\<N>\`.

It must hold for every shape: fuelhh (long format, one row per period and fuel), system_prices (price
columns plus vintages), physical_flows (many descriptive columns, nulls), bmunits_reference (a register,
no time axis, many string columns). It must also plausibly reflow to 390 px later (no absolutely
positioned text; a wide table may scroll inside its own container).

## Verify, then report

Run SHARED.md's verification recipe on every board (detector `[]`; measure layout numerically in your OWN
browser tab if you have browser tools, a port in 9700-9799, stop the server after; never kill other
processes). The harness blocks files named REPORT.md: your report is your FINAL MESSAGE (under 250 words,
first line your model ID), also saved as `<p24>\r2-schema\<N>\<N>-notes.md`: board paths and heights, the
idea in one sentence, the section's content model with word budgets, NEW COPY lines verbatim, detector
results, anything you could not do.
