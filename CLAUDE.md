# Gridflow front-end — project guide

Documentation static site for the [gridflow](https://github.com/EBentham/gridflow) ETL pipeline and gridflow-models. Editorial-quiet portfolio aimed at full-stack data-science recruiters in energy trading. **Not a product** — no fake live indicators, no SaaS-style KPIs, no dashboard chrome.

## Session start

Read `.planning/CONTROL.md` first (orchestrator brief: current phase, skill routing, open and locked decisions, cold-start reading order), then `STATE.md`, then `ROADMAP.md`. `PROJECT.md` / `REQUIREMENTS.md` hold context and REQ-IDs; `research/` and `codebase/` hold the maps (read each `SUMMARY` / `STRUCTURE` first).

## Working agreements

- **Never auto-commit** unless the user asks — this overrides the global commit-after-each-passing-test cadence (a docs site has no test-driven rhythm).
- Never commit code to `main` — feature branches + PRs. Conventional commits, one concern per commit. Docs-only commits (`*.md`, `.planning/`, `docs/`) may land on `main` directly (guard exemption, 2026-09-01).

## Commands

```bash
uv run gridflow-serve              # stdlib-only dev server (no build deps required)
uv run gridflow-build              # render vault .md → site/hifi/data-sources/ (needs [build] extra: Jinja2)
uv run gridflow-build --check      # idempotence / content audit; CI fails on drift
uv run gridflow-drift-check        # verify rendered pages against their vault sources
```

CI (`.github/workflows/deploy.yml`) runs `htmlhint` + `lychee` link-checking, then publishes to GitHub Pages — **on push to `main` only; there is no PR-triggered CI.** The merge gate for every PR is a local green `uv run --system-certs --extra build gridflow-build --check` (Avast intercepts TLS). `gridflow-drift-check` calls the vault's **live-API** curl validator — never run it without explicit user confirmation.

## Tech stack

- Static HTML5 + CSS3 + vanilla JS (ES2017+, no transpilation, no modules). One shared stylesheet `site/hifi/assets/theme.css`; runtime chrome injection `site/hifi/assets/site.js` via the body `data-page` / `data-root` / `data-screen-label` attribute contract; deterministic seeded inline-SVG charts `site/hifi/assets/charts.js`.
- Python 3.11+ stdlib-only dev server (`src/gridflow_front_end/serve.py` → `gridflow-serve`). `gridflow-build` (Python + Jinja2 3.1.x, `[build]` extras only) renders vault `.md` → `site/hifi/data-sources/`; generated HTML is gitignored; deploy serves `site/hifi/`.

## Source-of-truth hierarchy — do not invert without explicit discussion

1. **gridflow code** (`<gridflow>/src/gridflow/schemas/*.py`, `silver/**/*.py`, `connectors/**/*.py`) — canonical
2. **Live API responses** (verified by `verify_curl_and_silver_schema.py` in the vault)
3. **Obsidian vault** (`<vault>/30-vendors/<vendor>/datasets/*.md`) — authored docs derived from 1 + 2; **33 active Elexon datasets**
4. **Rendered pages** (`site/hifi/data-sources/<vendor>/<dataset>.html`) — generated from 3 by the build script

`vault/` in this repo is a **generated mirror** of 3 (flat `vault/<vendor>/<slug>.md`; `open-meteo` → `openmeteo` remap). Refresh it only with the `propagate-vault-mirror` skill, after any pending vault reconcile branches have merged; never hand-edit mirror files (fix the canonical vault, then re-sync). `vault/.last_synced_from_vault` records the source vault SHA + UTC sync time.

Cross-repo paths (Windows local): vault `C:\Users\Bobbo\OneDrive\Desktop\Learning\AI\quant-vault\` · gridflow `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\` — both must be present to run `gridflow-build`.

## Locked decisions (don't relitigate)

Editorial / quiet aesthetic (cream + forest-green, Fraunces + Inter + JetBrains Mono) · recruiter-first audience: full-stack data scientist in energy trading · core value: domain depth over polish · v1 Elexon scope **33 datasets** (matches connector + vault) · vault → site direction · templating: Python + Jinja2 (Option B + CI build) · ENTSO-E cross-vendor proof: Generation by PSR type · kill all "live" framing, charts are illustrative snapshots · license MIT.

## Anti-goals

Looking like a SaaS product or dashboard · fake live indicators (timestamps, "X min ago", status badges on unfinished work) · performance metrics / KPIs / uptime badges · Node/Go SSGs (11ty, Astro, Hugo — rejected for Python-first alignment) · hand-authored dataset pages that bypass the build script (one bounded exception: `authored-pages/<vendor>/<slug>.html` showcase overrides; the long tail stays template-driven) · author photos, testimonials, hire-me CTAs.

## Conventions

- HTML filenames: kebab-case slugs, except Elexon dataset codes keep BMRS underscores (`system_prices.html`).
- Dataset page anatomy: hero → metadata grid → stats strip → sticky sidebar → overview → snapshot chart → schema → sample → API tabs → caveats → related.
- Every page carries `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- A11y minimums: `<main>` landmark, `aria-current="page"` on the active nav, distinguishing `aria-label` on the dual `<nav>` (top + sidebar), `aria-hidden="true"` on decorative icons.

## Issues, triage, domain docs

Issues are markdown under `.planning/issues/<feature>/` and `.planning/reconciliation/<vendor>/` — GitHub Issues are not used (`docs/agents/issue-tracker.md`). Labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix` (`docs/agents/triage-labels.md`). Single-context domain docs: one `CONTEXT.md` + `docs/adr/` at the repo root; sibling repos keep their own (`docs/agents/domain.md`).
