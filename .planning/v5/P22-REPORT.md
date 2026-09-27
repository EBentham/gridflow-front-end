claude-opus-5-5

# Phase 22 data truth: report (2026-09-27, overnight + 07:15 resume)

**Status: complete; one gate outstanding by design.** Matrix, ingest with receipts, proposals and the discrepancy list are written. The live validator / drift check was NOT run (RULINGS #5, D7); its offline half (vault schema tables vs gridflow schemas) is in the matrix. `machine-catalog.json` was re-derived offline and committed on vault branch `docs/v5-p22-machine-catalog` (4f37e04, off `master`; not pushed or merged; worktree in the session scratchpad). **Owed by the seat:** the class-2 RULINGS line for tonight's ingest. `.planning/RULINGS.md` is outside this agent's write scope and was being edited by another agent.

Outputs (`.planning/v5/`): `DATA-MATRIX.md`/`.json` · `PROPOSALS.md` · `DISCREPANCIES.md`/`.json` · `ingest-receipts/` (39 receipts + `_ingest-log.jsonl`) · `scripts/` (`build_data_matrix.py` and `find_discrepancies.py` are offline and rerunnable; `ingest_missing.py` makes live calls).

## Starting numbers: reproduced?

| claim | result | method |
|---|---|---|
| 125/165 with local silver | **126** | parquet present under `C:\gridflow-data\silver`. `neso/intensity_factors` was first written 2026-09-26 18:43 BST, after the 18:15 BST measurement, so NESO was 24/33, not 23/34 |
| 165 datasets | yes: 165 vault notes | `git ls-tree master 30-vendors/*/datasets`, excluding `neso/README.md` |
| 85 chart series | yes | `chart-series.json` `series` keys |
| 130 authored overrides | yes | `authored-pages/*/*.html` minus `_landing.html` |
| 36 coming-soon / planned | text match yes; **real count 29** | the `>Planned<` match gives 36, but 7 hits are the outage-type value "Planned" in ENTSO-E/ENTSO-G/GIE sample data; only the 29 NESO Data Portal stubs are planning leakage |
| 160 mirror notes differ | vs the vault **working tree** yes; **content differs for 20** | 138 of 160 differ only by CRLF (the vault's Windows checkout) and 2 by unmerged edits on the vault's current branch. Against `master` blobs, 20 differ |

**NESO 34 / 33 / 23:** 34 files = 33 dataset notes + `README.md`. 33 pages = one per note. The "23" silver tables were really 24 (above); the other 9 were never-ingested snapshot endpoints. All 33 have silver now.

**Registry vs vault on the 165:** 163 agree (in `sources.yaml` + silver transformer + note). NESO Data Portal notes use hyphenated slugs but map 1:1 via `dataset_key`. `entsoe/activated_balancing_qty` has a transformer but no `sources.yaml` entry (ingest rejects it). `entsoe/commercial_schedules_net_positions` is vault-only and titled "Deprecated". The site adds 29 stub pages that neither the vault nor gridflow has.

## Matrix headline (final, 06:16Z)

- Silver: **149/165** (Elexon 33/33, ENTSO-E 36/49, ENTSO-G 32/33, GIE 6/8, NESO 33/33, Open-Meteo 6/6, NDP 3/3).
- Vault schema table vs gridflow code: 48 match · 74 differ only by `published_at`/`ingested_at` (systemic, added after the June validator run) · 25 differ substantively (21 ENTSO-G) · 14 have no schema table · 1 has no silver section · 1 range notation (fine) · 2 have nothing to compare. The 14 and the 1 match the June validator's counts.
- Mirror: 145 byte-identical to `master`, 20 behind.

## Ingest (class 2): 39 datasets, one attempt + one retry each

- **ok: 23.** ENTSO-E 5: `aggregated_balancing_energy_bids` 768 rows, `countertrading` 12, `outages_offshore_grid` 4, plus two found only by a month-aligned retry: `congestion_management_costs` 744 (monthly cadence) and `redispatching_cross_border` 288 (6–9 Jul). ENTSO-G 7 (six reference sets of 27–1,225 rows, urgent market messages 133). GIE 2 (about, 1,665 each). NESO 9 (snapshots, 1–162 rows).
- **Vendor has no data: 12.** 11 ENTSO-E datasets answered with Acknowledgement 999 on 22–25 Sep and again over 1 Jul – 31 Aug (62–496 requests each). ENTSO-G `interruptions` returned "No result found" for Jan–Sep 2026.
- **Not ingestable: 2** (`activated_balancing_qty`, `commercial_schedules_net_positions`: "Unknown ENTSO-E dataset").
- **gridflow behaviour: 2.** GIE `news` has 2.6 MB of real bronze but 0 silver rows. Cause unconfirmed; the candidate is the transform's date-window filter (read from code, not reproduced). `news_item` depends on `news`.
- No auth failures (gridflow reads its own `.env`; no key value was read or written). Nothing pre-existing was overwritten, so no snapshot was needed; no bronze was deleted.
- **Caveat:** `C:\gridflow-data\gridflow.duckdb` was locked by another process (a scheduled transform), so runs used a scratch catalogue via `GRIDFLOW_DUCKDB_PATH`. Tonight's run log and watermarks are not in the shared DB, and the new tables get DuckDB views only at the next `gridflow init`. Parquet readers are unaffected.

## Proposals for Bobbo (details and reasons in PROPOSALS.md)

- **Families (D5):** 23 families, all recommended yes (4 of them "lean yes"). Elexon 3 (indicated NGC, demand outturn, demand forecasts). ENTSO-E 5 (load-forecast horizons, outages, congestion management, allocated/nominated capacity, balancing bids). NESO 4 (national intensity ×9, regional ×18, generation mix ×3, stats ×2). ENTSO-G 6 (capacity ×10, gas quality ×5, nominations/allocations, CMP, reference ×6, tariffs). GIE 2. Open-Meteo 3 forecast/historical pairs. FUELHH, `actual_generation` and `physical_flows` stay singletons.
- **Page set (D4):** drop the 29 NDP stubs, 11 empty ENTSO-E datasets, 2 unwired ENTSO-E datasets and ENTSO-G `interruptions`; hold GIE news ×2 (unpublished). **149 datasets documented: 73 pages with families, 149 without.**
- **Headline:** replace "165 datasets" with **"149 datasets"** (landing: "149 datasets on 73 pages"). Phase 26 falls to 73 author/review units.

## Discrepancies for Phase 26 (DISCREPANCIES.md)

- FUELHH page: SOLAR sample row, "solar" in the prose, "All 16 codes". Silver has 21 codes (including INTGRNL, INTVKL and INTELE) and no SOLAR.
- 9 ENTSO-E pages show GB (`10YGB`) values where silver has none. ENTSO-E silver zones are DE-LU, BE, FR, NL and IE-SEM; GB appears only as one side of a border.
- 139 pages carry seeded/illustrative charts; 27 chart series average across fuel/zone/unit.
- 20 stale mirror notes (FUELHH, MID, the system_prices premise correction, ITSDO > INDO, ENTSO-G PIT fields).
- Candidate vault units: `published_at`/`ingested_at` missing from 74 schema tables; 14 notes with no schema table; 1 with no silver section; the catalogue script's missing NDP slug map; 39 curl examples not passing in June.
- Candidate gridflow units: wire `activated_balancing_qty` into `sources.yaml`; the GIE news transform.

## Five rows for the seat to spot-check

1. `elexon/fuelhh`: 1,686,317 rows, 2021-09-01 → 2026-09-26, 21 `fuel_type` values, no SOLAR. Check silver `elexon\fuelhh` (group by `fuel_type`), `authored-pages/elexon/fuelhh.html` (its "All 16 codes" list and sample rows), and vault `master:30-vendors/elexon/datasets/fuelhh.md` line 22. The row count moves if the scheduled transform runs again.
2. `neso/intensity_factors`: the 125 → 126 explanation. Check the mtime of `silver\neso\intensity_factors\intensity_factors.parquet` (2026-09-26 18:43 local).
3. `entsoe/actual_load`: 9,191 rows; `area_code` values are DE-LU/BE/FR/NL with no 10YGB, yet `site/hifi/data-sources/entsoe/actual_load.html` samples GB.
4. `entsoe/redispatching_cross_border`: 0 → 288 rows only on the retry. Check `ingest-receipts/entsoe__redispatching_cross_border.md` and `silver\entsoe\redispatching_cross_border`.
5. `entsoe/commercial_schedules_net_positions`: vault-only, no silver section, absent from `config/sources.yaml` and the silver registry. Its vault title ends "- Deprecated".

Unfinished / not done: live validator (awaits Bobbo's "run it"); the RULINGS line (seat); merging the vault catalogue branch (seat). Spend was not metered by this agent.
