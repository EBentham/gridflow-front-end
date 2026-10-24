# NESO Data Portal pages: Network charges

Opened 2026-10-24 under the approved plan (ruling 62) and the resume (ruling 65). 3 held pages, one writer and one
checker, one branch and one PR stacked on Connection registers. Bobbo looks at the pages before merge.

The plan counted the GIS charging-zone package as a full page. It has no silver table (bronze ZIP and GeoJSON only), so
it ships held, as the ETYS boundaries and DNO licence-area packages did in System (seat, PROXY-SOURCED).

## Where things are

- **Front-end worktree:** `C:\gridflow-wt\fe-neso-nc`, branch `feat/neso-dp-network-charges`, cut from
  `feat/neso-dp-connection-registers`. Read `.planning\v5\author-brief.md` in this worktree.
- **Vault worktree:** `C:\gridflow-wt\vault-neso-nc`, branch `docs/neso-dp-network-charges`, cut from
  `docs/neso-dp-connection-registers`. Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` (keep each
  note's line endings; Edit tool).
- **Mirror:** `vault\neso_data_portal\<slug>.md` in the front-end worktree; the seat made the first copy; `cp` and
  `cmp` after every edit.
- **Page set:** the seat added every package below to `site/hifi/data/neso_data_portal.json`; never edit it.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\network-charges\`.
- **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`. Worked examples: the System held batch
  (`BATCH-system.md` row H, reports `system\held-*.md`: the DNO licence-area GIS page) and the Interconnectors held
  batches (`interconnectors\held-*.md`).

## The pages

| # | Page (slug) | Members, lead first | Writer port | Checker port |
|---|---|---|---|---|
| H | Held: `aahedc-tariffs` (`aahedc_tariffs`), `gis-boundaries-for-gb-generation-charging-zones` (`gis_gen_charging_zones_files`, bronze only), `transmission-network-use-of-system-tnuos-tariffs` (8 tables: `tnuos_tariffs_half_hourly_hh_demand`, `_non_half_hourly_nhh_demand`, `_embedded_export`, `_transmission_demand`, `_onshore_generator`, `_local_offshore_generator`, `_local_substation_tariff`, `_onshore_local_circuit`) | every table held | 9861 | 9871 |

Known risks:
- **Tariff tables are held** on the ledger's question: the files don't say when each tariff was issued
  (`C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\.planning\v0.22-FE-LEDGER.md` and the eligibility report
  `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\docs\neso_data_portal\eligibility.md`). Keep the AAHEDC and TNUoS
  wording the same where the question is the same.
- **GIS charging zones:** NESO's text says 27 zones; the GeoJSON has 28 features. Claim no equivalence between them;
  state both, dated, if at all. Cut coordinate-system wording unless the file states it (DNO precedent).
- **Held pages:** one plain line per table on why rows are not shown, covering the whole table, no codes, no
  local-data references (dated NESO facts only). Spell out AAHEDC and TNUoS once.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged. Keep strictly to your own packages' files; never `git add`
or commit (the seat commits). Do not end your turn until your report or review is written. Correct out-of-date
note-body statements yourself when the data proves them wrong.

## Tracker

| # | Writer | Checker | State |
|---|---|---|---|
| H | ac3e2546998f4ced8 | | writing |
