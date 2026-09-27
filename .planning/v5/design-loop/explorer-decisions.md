# Explorer page: decisions with Bobbo (2026-09-27)

A new top-level page about gridflow explorer. Purpose (OWNER): "just show the work I have done". Keep it
brief: the technologies (recruiters should see a full-stack developer who builds React front ends) and a
screen demo "similar to the view of the notebook we had earlier on the home page".

## What the explorer is (read 2026-09-27 from `gridflow_explorer`)

- Local-first app over gridflow's silver and gold data. Front end: React 19, TypeScript, Vite, Recharts,
  React Router, its own token design system ("Petrol night", light and dark, same world as this site).
  Backend: FastAPI, Polars, read-only DuckDB per request, reading only through `GridflowClient`.
- Built on `milestone/v0.4` (pushed, not merged to public `main`): a catalogue of 8 sources and 163
  datasets, a page per source, one dataset page template (series as charts, events and reference as
  tables), views found by file glob, about a dozen bespoke dataset views (demand, outages, day-ahead
  benchmark, historic mix, ...). A second batch of views is written and parked before screenshots.
- Not hosted: it runs locally, so the site can only show it, not embed it.
- Public `main` of github.com/EBentham/gridflow-explorer still has the v0.1 look. Open question for the
  build (not the design): the page ships once v0.4 lands on `main`, or links the milestone branch.

## Round 0 (brainstorm)

- **Page shape (proposed, not yet ruled):** opening line and repo link; the screen demo; how it's built
  (front end and backend columns, one flow line, one real code excerpt: a dataset view file); links to
  Architecture and Models.
- **Screen demo: A, real screenshots in a window frame with tabs** (OWNER, 2026-09-27). Not a rebuilt
  HTML copy, not a recording. Dark screenshots in dark mode.
- Pack: `explorer-pack/` (screenshots 1440 wide, light and dark, from the explorer's own shoot tool;
  code excerpts). Left out: the power stack view, which states model misses and failed runs (RULINGS #21,
  the site stays high level on models).
