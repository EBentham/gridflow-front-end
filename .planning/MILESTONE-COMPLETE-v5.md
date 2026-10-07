# v5 — The site, rebuilt in the locked design: complete and deployed

**Closed:** 2026-10-07 · **Final deploy:** `aa723a7` (tag `v5-complete`) · **Live:** https://ebentham.github.io/gridflow-front-end/

The `v5` tag marks the cutover (`fffc826`, PR #46). It was pushed before the dataset fan-out, so it stays where it is.
`v5-complete` marks the close.

## What shipped

- **Design and top pages.** The "Above ground, below ground" design (`DESIGN.md`, `site/hifi/assets/tokens.css`) covers
  the homepage, the data-sources landing, 7 vendor hubs, architecture and models. Cutover was PR #46.
- **Dataset pages.** 149 datasets sit on 73 pages, rendered from vault `page:` blocks by `templates/dataset.html.j2`.
  Each page has charts from committed silver extracts, a Polars sample frame and a column guide.

| Batch | PR | Pages |
|---|---|---|
| Elexon | #54 (`cccf643`) | 19 pages |
| ENTSO-E | #55 (`d284745`) | 20 pages |
| GIE | #56 (`7deb94f`) | 3 pages |
| Open-Meteo, NESO Data Portal, NESO, ENTSOG | #57 (`c2c6027`) | 17 pages |
| Triton Knoll caption | #58 (`aa723a7`) | correction |

- **Weather-locations map** on the three Open-Meteo pages (ruling 50). Site names are verified in
  `v5/p26/openmeteo/site-names-check.md`.
- **Vault.** The canonical notes and remediation list were merged via quant-vault PRs, including #59 and #61.
  The mirror is byte-equal with them.

## Held pages: blank until gridflow fixes silver

| Page | Ruling |
|---|---|
| Elexon netbsad, nonbm | 37 |
| ENTSO-E current balancing state, procured balancing capacity, balancing-energy bids, outages | 41, 42, 44, 46 |
| GIE unavailability | 43 |
| ENTSOG capacity-by-indicator | 52 |
| ENTSOG cmp | 53 |

- The defects are logged in gridflow `.planning/BACKLOG.md` items 12 to 18 and in the vault page
  `10-projects/gridflow/specs/remediation-from-site-batches.md`.
- The capacity-by-indicator work is parked on `v5/p26-entsog-gas-held` and `docs/v5-p26-entsog-gas-held`.

## For Bobbo at close

- **RATIFIED 2026-10-07 (ruling 56).** ~~Ratify the proxy-sourced rulings~~ in `.planning/RULINGS.md`. Each is a seat or agent call made under
  autonomous mode: 5, 6, 7, 9, 10, 11, 27, 36 to 47, 52, 53. Paste: "I ratify the v5 proxy-sourced rulings listed in
  MILESTONE-COMPLETE-v5.md", or name any to revisit.

## Carried forward

- **gridflow:** remediation items 12 to 18 unblock the held pages. Row 15h moves the Triton Knoll coordinate onto
  the array and re-fetches its weather (T1).
- **Ruff:** ISC004 in `build.py` and format drift in three files, pre-existing.
- **Vault README drift:** `10-projects/gridflow-front-end/README.md` still describes the pre-v5 site and needs a
  real pass.
- **Workflow lesson:** a background agent stalled for about 3 hours waiting on its own background poll. Agent
  briefs should ask for checks to run synchronously.
