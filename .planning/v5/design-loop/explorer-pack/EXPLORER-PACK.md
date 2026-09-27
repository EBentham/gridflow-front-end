# Explorer page: verified content pack (2026-09-27)

Every fact, label and number on a board comes from here or from the screenshots. You may shorten; you
may not add.

## What it is

- gridflow explorer is a web app for browsing everything gridflow collects: GB and European energy-market
  data from eight public sources (Elexon BMRS, ENTSO-E, NESO Carbon Intensity, NESO Data Portal, ENTSO-G,
  GIE AGSI+, GIE ALSI, Open-Meteo), plus the tables gridflow builds from them (gridflow gold).
- It opens on a catalogue of every source, grouped Electricity, Gas and Weather. Each source has a page;
  each dataset family has a page. Time series get charts; event feeds and reference tables get tables.
  Generation mix and System prices are pinned in the side rail.
- It runs on the owner's machine against gridflow's own store: it is not hosted. It reads the data
  read-only; the only thing it writes is gridflow's catalogue when it asks gridflow to fill a gap.
- Principles it was built to (its product brief): the data is the loudest thing on screen; settlement
  time is native (UK clock, half-hour settlement periods, 46/48/50 on clock-change days); gaps and
  caveats are shown plainly; every axis carries a unit; it works in light and dark.
- Repo: https://github.com/EBentham/gridflow-explorer (public).

## How it's built (verified from `package.json`, `backend/pyproject.toml`, the source tree)

**Front end:** React 19, TypeScript, Vite, Recharts for charts, React Router. No component kit, no CSS
framework: its own design tokens (CSS custom properties), light and dark themes, one shared chart theme.
- One dataset page template with three bodies: series (chart), events (filterable table), reference
  (plain table).
- Each dataset view is a small typed folder, `src/views/<source>/<family>/`, found by a file glob: adding
  a view is adding a folder, with no central list to edit. Example excerpt: `code/market-index-price.index.tsx`
  (quote at most ~15 lines, real lines only).
- Its own screenshot tool (headless Chrome via puppeteer-core) takes every screen in light and dark; the
  screenshots in this pack come from it.

**Backend:** Python, FastAPI (on uvicorn), Polars, DuckDB opened read-only per request. It reads gridflow
only through gridflow's own client (`GridflowClient`), never raw file paths. Endpoints serve the source
manifest, a dataset's rows and its coverage, forecast runs from the gold forecast store, and a job
endpoint that runs gridflow's ingestion to fill a missing range.

**Flow (for a line or drawing):** browser (React) -> FastAPI -> GridflowClient -> DuckDB over gridflow's
silver and gold tables.

## Screenshots (`shots/`, 1440 wide, full page height; light and dark of each)

| file stem | what it shows |
|---|---|
| `catalogue` | the landing catalogue: petrol band with the eight sources plus gridflow gold, then Electricity, Gas, Weather columns |
| `source-elexon` | the Elexon source page: its dataset families |
| `generation-mix` | pinned screen: GB generation stacked by fuel |
| `system-prices` | pinned screen: system sell and buy prices |
| `historic-mix` | NESO historic generation mix, 2009 to 2026, with carbon intensity and a mix-by-year table |
| `demand-outturn` | Elexon demand outturn |
| `outages` | ENTSO-E outages, unavailable capacity per interval |
| `market-index-price` | Elexon market index price (the view whose code is in `code/`) |

Left out on purpose: the power stack view (it states model misses and failed runs; the site keeps models
high level).
