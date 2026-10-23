# Review: national-demand-balancing-mechanism-units (`national_demand_bmus`)

**Verdict: REVISE** (1 major, 7 nits). The page is accurate on everything you asked me to look hardest at. The one major
is a related-dataset note that contradicts the linked note's own hold reason; it is a one-line fix and needs no rebuild of
any artefact.

Checked: author report, canonical note diff against `origin/master` (vault worktree), `cmp` of the mirror (clean, 272 lines,
all CRLF), the sample and notebook artefacts, the built page, the saved NESO catalogue snapshot and field info, bronze, silver,
the connector, the transformer, `gridflow_models`, the 16 October refresh log. Build `--only neso_data_portal/national_demand_bmus`
ran clean (only the unrelated global 37-line warning). Detector `[]`. Server on 9855 was PID 18884, stopped by that PID.

## What I reproduced

1. **Quotes verbatim.** Catalogue snapshot `20261006T195819Z`, package `notes`: "This dataset contains a preliminary list of
   Balancing Mechanism units that make up National Demand." The page quote "a preliminary list of Balancing Mechanism units that
   make up National Demand" is an exact substring. The National Demand quote ("is the sum of metered generation, but excludes
   generation required to meet station load, pump storage pumping and interconnector exports") is exact against field info
   `20261008T114228Z\historic_demand.json`, field `ND`. Nothing else in the saved text says what "preliminary" means; the only
   dictionary field is `BM_Name`, "Name of BM Unit". "Ad hoc" is the package's `Update frequency` extra.
2. **What a row is.** Registry: one column `BM_Name` -> `bm_name`, entity key `bm_name`, `latest: whole_capture`, temporal `none`.
   Bronze CSV: `BM_Name` header, 1,001 data rows, 1,001 distinct, 9,462 bytes equal to `declared_content_length`; the one name
   with a trailing space is `"EEND01 "`. Silver: 1,001 rows, 1,001 distinct.
3. **The join, reproduced with Polars** against `silver/elexon/bmunits_reference` (3,014 rows, `ingested_at` 2026-09-26 19:08:06 UTC;
   bronze fetched 19:08:05): `national_grid_bm_unit` 859, `bm_unit_id` 0, either 859, `bm_unit_name` 17, absent 142. No duplicate
   register rows per matched name, so the notebook's LEFT JOIN keeps 1,001 rows. The 859 matched by Elexon `fuel_type`: 445 none,
   222 WIND, 89 OTHER, 47 CCGT, 16 NPSHYD, 14 NUCLEAR, 12 BIOMASS, 12 OCGT, 2 COAL (sums to 859). Register totals behind cell 5:
   WIND 234, CCGT 61, NUCLEAR 16, NPSHYD 22, and so on. The added note-body sentence is accurate.
4. **No pumped storage or interconnector units.** All 16 register `PS` units (CRUA, DINO, FFES, FOYE) and all 11 interconnector
   units (ten `INT*` types, `INTELEC` has two) are off the list. I also looked inside the 445 matched names with no fuel type
   (id prefixes `2_`, `V_`, `E_`, `T_` only; no `I_` ids, no CRUA/DINO/FFES/FOYE national-grid names), so the claim is not an
   artefact of null fuel types. The note body scopes it to "the register's" units, which is right: the 142 unmatched names
   cannot be classified.
5. **Time.** Silver: one distinct value each. `timestamp_utc` = `event_time` = `capture_written_at` = 2026-10-08 11:12:57.464036 UTC;
   `published_at` = `available_at` = 2026-09-29 13:45:22.344455 UTC (CKAN `last_modified`, sidecar). `casting.py` lines 605 to 607 are the
   `temporal.kind == "none"` branch (line 484 was the `sp_pair` branch, so the body fix is right). `gridflow_models`
   `_DATE_COLUMN_BY_DATASET['national_demand_bmus']` = `timestamp_utc`, so the `data.sql()` lead is correct.
6. **One capture, no 16 October recapture.** Bronze has only `2026/10/08`. The writer inferred the reason from `client.py`
   `iter_members` (lines 1750 to 1770: an upload member whose newest capture carries the live `last_modified` is `unchanged`).
   I confirmed the observation itself: `gridflow\.planning\phases\v0.22-close\refresh-20261016\ingest.log` line 226 reads
   "neso_data_portal/national_demand_bmus: 0 responses ingested, 1 unchanged since newest capture". So the 16 October refresh
   did visit this table and found NESO's file unchanged. (Finding 5.)
7. **Chart.** `type: none` builds with no chart figure, no heading and no gap: the page goes sky, "What it is" / "How it's used"
   side by side, bronze. The `reason` text is not rendered (template follow-up, not a finding). No series file exists and the
   build says 0 template pages carry a distilled series.
8. **Frame and notebook.** Eight names match silver; folded view shows `bm_name`, three timestamps and `bronze_capture_id`
   horizontally; the unfolded view adds `event_time`, `available_at`, `source_run_id`, `dataset_version` (9 columns,
   `shape: (8, 9)`); the guide lists every non-pipeline column and the key first. Notebook JSON from `scripts/run_notebooks.py`,
   6 cells, all read-only, no errors; cell outputs match my numbers; the plot PNG matches `plot_alt` (445 / 222 / 142 / 89 / 47 /
   16 / 14 / 12 / 12 / 2). The join is dated in the lead ("fetched 26 September 2026") and in the alt text, and the page never
   attributes the counts to NESO.
9. **Rendering.** Browser pane at 1440, 1024, 768 and 390 (390 emulated as a mobile viewport): no sideways scroll at any width
   (`scrollWidth` equals `clientWidth`), hero scenery and labels whole, prose, raw-feed wells, frame, notebook with plot, and
   related list all fully visible, nothing overlapping. Rendered text has no em or en dashes, arrows, middle dots, "locally",
   "held", "our", "since 20", "live", "now"; "rows" appears only in template text. Related links resolve (all four slugs are in
   the page sets).

## Findings

1. **major** `page.related[3].note` (daily-demand-update): "Recent `ND` outturn with a short forecast tail" contradicts that
   note's own hold. The forecast (`F`) rows in that file carry zero national and transmission demand; the page there is held
   precisely because NESO does not say what the zero means (`daily-demand-update.md`, `page.held`, lines 11 and 196 to 197).
   The forecast tail in that file is of embedded wind and solar, not of `ND`. A reader following the link from this page would
   expect a forecast of `ND`. The author's report says this note "leans on that note's own description", but the sibling's
   description is about embedded generation. Fix, 12 words or fewer: "Recent `ND` outturn, updated daily by NESO" (or "NESO's recent
   `ND` outturn, refreshed daily").

2. **nit** `page.related[1].note` (historic-demand-data): "the `ND` these units make up" states the composition as gridflow's
   fact. The canonical note body deliberately leaves the rule as `TODO: verify` (whether these are the metered units summed into
   ND or on the demand side), and `how_used[1]` attributes it correctly ("units NESO says make up National Demand"). Suggest
   "Half-hourly National Demand, which NESO says these units make up" (10 words).

3. **nit** `page.record.fields.bm_name`: "Elexon lists this form as `national_grid_bm_unit`" is not true of one of the eight frame rows
   a reader can see: `AG-PEPG01` is among the 142 names absent from both Elexon identifier columns. Suggest "BM unit name as
   NESO spells it; Elexon's register keeps this form in `national_grid_bm_unit`, though not every name is in it".

4. **nit** `page.record.caption`: "Eight names, alphabetical" reads as the first eight in the file (the file is alphabetical and
   the notebook's `df.head()` shows `ABRBO-1` second, which the frame omits). Say "Eight names picked from the list, in alphabetical
   order, among them ...".

5. **nit** note body, Cadence: "still the only one on 2026-10-23" is supported, but the note gives only the skip rule. The observed
   fact is stronger and citable: the 2026-10-16 refresh reported this table "unchanged since newest capture" (gridflow
   `.planning/phases/v0.22-close/refresh-20261016/ingest.log` line 226). One clause saying so would let a reader see NESO's
   `last_modified` was unchanged on 16 October, not only that the code would skip it. Nothing on the page needs to change.

6. **nit** `page.what_it_is`: the National Demand definition is quoted without saying where it comes from. It is the `ND` field
   description in NESO's Historic Demand Data dictionary, not text from this package. A reader who looks in this package's
   metadata will not find it. Either name the source ("In NESO's Historic Demand Data dictionary, National Demand ...") or
   leave it; word budget permitting.

7. **nit** `page.how_used[2]` ("Track units joining or leaving the list between NESO's uploads"): only one capture exists and the
   note body keeps `TODO: verify` on whether NESO replaces this resource in place or adds a new one beside it. It is a fair
   prospective use, but it is the only one of the three that cannot be done today. Optional: "Compare the list across NESO's
   uploads once more than one is captured" is wordier; leaving it is fine.

8. **nit** notebook cell 6 plot (artefact `national_demand_bmus-6.png`): the y-axis carries the leftover label `fuel_type` beside
   categories that include "no fuel type" and "not in register". `ax.set_ylabel("")` removes it. This changes the notebook cell
   text and PNG, so only do it if the notebook is being re-run anyway; otherwise accept.

## Accepted, not findings

- The added body sentence (fuel-type counts and no `PS` or interconnector units) is true, dated ("same snapshot, checked 2026-10-23"),
  labelled as a check of the same snapshot, scoped to "the register's" units, and says NESO states no rule. Acceptable as an
  addition next to the composition `TODO`. Body edits 1 and 2 are the smallest spans and cite code.
- The `units` scenery draws an interconnector although none are on the list. It is the template's fixed scenery for the `units`
  landscape (alt text: "registered units of different kinds"), not a claim about this list.
- Raw-feed commands (`--last 24h`, "whole file; window must end recently") are identical to the approved grid supply points page.
- Out-of-scope seat items noted by the writer (chart `reason` not rendered, `gridflow-distil` miscount for `type: none`,
  headless-Chrome tall-window artefact) are not findings. The `query()` capture-time defect and the 142 unmatched names are
  correctly logged as defects/open questions, not stated as NESO errors.
