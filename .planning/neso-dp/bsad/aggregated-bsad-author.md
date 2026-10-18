# Aggregated BSAD page: author report

Page: `neso_data_portal/aggregated-bsad` (single table `aggregated_bsad`). Written 2026-10-18 by the writer agent.

- Canonical note: `C:\gridflow-wt\vault-dfs\30-vendors\neso-data-portal\datasets\aggregated-bsad.md` (CRLF kept; edited with the Edit tool).
- Mirror: `<fe-neso>\vault\neso_data_portal\aggregated-bsad.md`, byte-equal (`cmp` clean after the last edit).
- Artefacts (all new, untracked, under `<fe-neso>\site\hifi\data\`):
  - `series\neso_data_portal\aggregated_bsad.json` (`spec_origin: vault`)
  - `samples\neso_data_portal\aggregated_bsad.json` (`generated_by: gridflow-sample`)
  - `notebooks\neso_data_portal\aggregated_bsad.json` and `aggregated_bsad-6.png` (from `scripts/run_notebooks.py`)
- Gates:
  - Build: `gridflow-build --only neso_data_portal/aggregated_bsad` wrote `data-sources/neso_data_portal/aggregated-bsad.html` with no errors.
  - Detector: `detect.mjs --json` returns `[]`. The page has 0 em dashes.
- Screenshots: 1440, 1024, 768, and 390 through a 390 px iframe, served on port 9913 (server stopped). Nothing is clipped or overlapping.
  - The site has no dark theme. No `prefers-color-scheme` or `data-theme` rule exists in `site/hifi/assets/` or `DESIGN.md`, so light is the only rendering.
  - Shots are in the scratchpad at `bsad\shots\`.
- No staged chart spec or authored override existed for this dataset.

## What one row is

- **Grain:** one row per (`resource_id`, `settlement_date`, `settlement_period`) and capture.
  - `resource_id` is the CKAN id of the financial-year file.
  - Registry `aggregated-bsad.json`: `entity_key`, `latest: whole_capture`, `latest_partition: resource_id`, `vintage: capture_fallback`.
- **Value columns:** eight net adjustment terms with vendor units from the dictionary (saved field info `field-info/20261008T114228Z/aggregated_bsad.json`):
  - `ebca` and `esca` in £;
  - `ebva`, `sbva`, `esva` and `ssva` in MWh;
  - `bpa` and `spa` in £/MWh.
- **No BSAD flags:** there are no buy/sell flags and no action, contract or party identifier. The headers in both epochs carry only date, period and the eight terms. Buy versus sell exists only as separate columns: `ebca`/`ebva`/`sbva`/`bpa` for buy, `esca`/`esva`/`ssva`/`spa` for sell.
- **Coverage:**
  - Silver holds 10 of the 13 vendor files: 2016-17 to 2019-20, and 2021-22 to 2026-27.
  - 2013-14 and 2014-15 failed with `UnicodeDecodeError`.
  - 2020-21 failed with `DuplicateEntityKeyError`.
  - NESO publishes no 2015-16 file.
  - The page says this in `facts.history`, in the chart caption and in the x label, and never implies the failed years are covered.

## Evidence table

| Claim on the page | Evidence |
|---|---|
| Vendor text: BSAD submits actions outside the BM to the BSC, which governs imbalance settlement; "updated twice daily" | CKAN `notes` for `aggregated-bsad` in `gridflow/.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json` (extracted with `p7.py`) |
| NESO lists files from 2013-14, none for 2015-16 | Same snapshot: 13 resources, from FY 2013-14 to 2026-27, with no 2015-16 resource |
| gridflow loads 2016-17 onward except 2020-21 | Silver: 11 parquet files over 10 resource ids, none for `ec526741…` (2020-21), `d39fcf5e…` or `44851379…`. Note's ADR-040 failure table (RULINGS 748/749/760) |
| 2020-21 "repeats 11 periods, so gridflow refuses it" | Note's ADR-040 failure table (11 all-zero repeated rows, `DuplicateEntityKeyError`); FACTS section 3 [C03] |
| Key `resource_id, settlement_date, settlement_period` | Registry `connectors/neso_data_portal/registry/aggregated-bsad.json` `entity_key`. Latest view unique on it: 167,376 = 167,376 (Polars) |
| Units £, MWh, £/MWh | Saved field info `aggregated_bsad.json` (`info.unit`); epoch 1 headers `EBCA (£)` and so on in the registry |
| Six cost and volume terms "superseded, carried as zero (BSC)" | K-AS-4-FACTS line 248, citing the BSC interface definition document part 1 (v57.0). In silver, all six plus `spa` have 0 non-zero and 0 null values (Polars) |
| Sign convention of `bpa`/`spa` not stated by NESO | Field info gives only title and unit. K-AS-4-FACTS lines 344, 445 and 958 leave monetary and aggregate signs as TODO |
| `timestamp_utc` is the period start, computed from date and period | Registry `temporal: sp_pair`. Silver: `timestamp_utc == event_time` on every row. 2026-01-15 period 33 = 16:00 UTC |
| `published_at` null; `available_at` is the capture write time | `connectors/neso_data_portal/skeleton.py:80` (`capture_fallback` gives null and the capture time); `silver/neso_data_portal/generic.py:435` (`available_at=ctx.capture_written_at`). Silver: 0 non-null `published_at` |
| Requests: `package_show`, upload redirector URL, `/datastore/dump/<id>` | `client.py` `iter_members` (1658-1780): one `package_show`, a datastore member goes to `_download_dump`, an upload to `_capture_member` through `resource.url`. `endpoints.py:275` `build_dump_path`. URLs from the snapshot |
| An upload is skipped if `last_modified` is unchanged; a dump is kept only if its body changed | `client.py` 1754-1766 (upload skip on `ckan_last_modified`); `_dump_member` 1944-1949 (body sha256 equals the newest capture, so `unchanged`) |
| `--last 24h` for ingest and transform | `client.py` `_assert_window_admissible`: a window ending more than 48 h ago is refused, and the error text points at `--last 24h`. Same commands as the reviewed `historic_generation_mix` page |
| Notebook lead: `silver_neso_data_portal_aggregated_bsad_latest`, filtered on `settlement_date`, both ends, lineage dropped | `gridflow_models` `_validate_dataset_for_source` returns `settlement_date`; `_relation_name_for_dataset` returns the view name; `_BITEMPORAL_EXCLUDE` = `event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year` |
| Chart: daily max `bpa`, 1 April 2016 to 15 October 2026, peak 159.55 on 2017-01-16, three days over 60 (all early 2017), break 2020-03-31 to 2021-04-01, four non-zero days after 2023-10-20 (2024-05-24, 2024-08-13, 2025-10-24, 2026-01-15), zero from April 2026 | Committed series: 3,485 points. Values read back from the JSON in Python |
| Sample: 2026-01-15 periods 33 to 40, `bpa` 10.65 ×6, 9.15, 0.0 | Committed sample rows |
| Notebook outputs: periods set per year from April (890, 580, 413, 292, then 423, 412, 119, 25, 27, 0; no 2020 row) and the evening block peaking at 309 in period 36 | Committed notebook JSON and PNG, read back |
| Related: `elexon/netbsad` terms "with names like these eight" | NESO dictionary descriptions ("Net Buy Price Cost Adjustment (Energy)" and so on) against the Elexon silver columns `net_buy_price_cost_adjustment_energy` … `sell_price_price_adjustment`. Names only: the mapping is not verified (see below) |

## Body corrections (canonical note)

The note's "one capture per resource" is stale. Silver also holds a **second capture of the 2026-27 dump**:

- `available_at` 2026-10-16 18:38 UTC, 9,600 rows, settlement dates 2026-04-01 to 2026-10-17.
- Its 9,168 periods shared with the 2026-10-08 capture are identical in every value column (full join; 432 differing rows, all new periods).
- It has 56 rows ahead of the capture (2026-10-16 periods 41 to 48 and all of 2026-10-17), all zero.

Smallest-span fixes:

1. A new paragraph, **Later capture (2026-10-16)**, after the file table: counts, identity of the shared periods, and the latest-view total of 167,376 rows (176,544 across both captures), with the Polars check cited.
2. **Two clocks, Vintage:** added the 2026-10-16 capture time beside the 2026-10-08 one.
3. **Two clocks, Event time:** coverage end changed from 2026-10-08T22:30Z to 2026-10-17T22:30Z, with the old end kept in brackets.
4. **Rows ahead of their capture:** added the 56 rows of the new capture.
5. **Cadence:** "one capture per resource (all 2026-10-08)" now says a second 2026-27 capture appended 432 periods and changed none.
6. **Known issues, same `available_at`:** added the 2026-10-16 capture time.

Nothing else in the body changed.

## Not verified

- **The BSC interface document's "superseded, carried as zero" wording.** I relied on K-AS-4-FACTS line 248, which cites it. I did not read the Elexon document.
- **How BPA enters the imbalance price.** NESO's text says only that BSAD is submitted to the BSC, whose rules govern imbalance settlement. The page says that much and links `elexon/system_prices`. It does not claim BPA is added to SBP, because no vendor text in the note states it. The note's opening "so that they can be reflected in the imbalance cash-out prices" is the note's own paraphrase, not NESO's words. I left it, but it is unsourced.
- **The NESO aggregated terms to Elexon NETBSAD mapping** (note `TODO: verify`). Elexon NETBSAD silver (2026-08-01 to 2026-09-22) is all zero in all eight terms, and so is NESO's for the same dates. That is consistent but proves nothing, so the page says "similar names" only.
- **What a non-zero `bpa` means economically.** It comes in constant blocks over consecutive periods (for example 0.78 over periods 15 to 22 on 2025-10-24), which looks like forward-contract adjustments. The sibling package `balancing-services-adjustment-data-forward-contracts` (silver `bsad_forward_contracts`) could test this. The page does not claim it.

## Open questions

- **Chart choice.** Net BSAD cost or volume per day, as the brief suggested, would be a flat zero line (all six terms are zero), so the chart is the daily maximum of `bpa`.
  - The checker should confirm a 10-year daily line is the reading a trader wants.
  - The alternative is a recent window, which would be flat zero since 15 January 2026.
- **x axis.** The x axis is `settlement_date` (Date) rather than `timestamp_utc`, so each point is one settlement day with no BST split.

## Template problems

None blocking.

- **Build warning.** Each `--only` run prints `WARNING: 3 line(s) in 'Known issues and gotchas' sections could not be placed by the caveat grammar and were dropped`.
  - The dataset template does not render that section, so nothing is lost on the page.
  - The lines are the note's multi-line bold bullets. The format predates this edit.
- **Long view name wraps mid-word at 390.** `silver_neso_data_portal_aggregated_bsad_la|test` breaks mid-word in the notebook lead. This is the template's wrapping of long code; nothing is clipped.

## Defects

Paste as is.

- **neso_data_portal / aggregated-bsad vault note stale after the 2026-10-16 capture (fixed on branch `docs/neso-dp-dfs-page`).**
  - Silver gained a second capture of the 2026-27 dump (`aggregated_bsad_20261016_run2026-10-16T18-38-07…parquet`, 9,600 rows to settlement date 2026-10-17).
  - The note still said one capture per resource, coverage to 2026-10-08 and 29 forward rows.
  - The shared 9,168 periods are unchanged, so no revision was observed. Severity: low (documentation).
- **neso_data_portal / aggregated-bsad vendor file defects (already recorded under ADR-040, RULINGS 748/749/760; no new entry needed).**
  - FY 2013-14 and 2014-15 uploads are not UTF-8 (`UnicodeDecodeError`).
  - FY 2020-21 upload repeats 11 all-zero periods (`DuplicateEntityKeyError`).
  - NESO publishes no FY 2015-16 file.
  - FY 2014-15 is partial (to 2014-06-02).
  - The page states the load gaps plainly.
- **gridflow-front-end build: caveat-grammar warning on `aggregated-bsad.md`.** 3 "Known issues and gotchas" lines are dropped by the caveat parser on every `--only neso_data_portal/aggregated_bsad` build. Harmless for the new template, but the warning is noise. Severity: nit.
- **gridflow-front-end worktree `.venv` lacks `tzdata`.** Polars `min()` on a tz-aware UTC column raises `ZoneInfoNotFoundError: 'No time zone found with key UTC'` in `fe-neso\.venv`.
  - Distil and sample still worked for this page (Date time axis).
  - A spec using `timestamp_utc` as its time column in this venv may fail.
  - I used gridflow's venv for analysis. Severity: low (environment).
- **Observation (not this dataset, unconfirmed as a defect).** Elexon `netbsad` silver holds 49 rows per settlement date (2026-09-14 to 2026-09-21), for example period 3 of 2026-09-20 twice with different `ingested_at`. It may be the normal append-only capture; whoever owns `elexon/netbsad` should check.

## Revision 1

Response to review 1 (REVISE: 1 major, 4 nits) and the seat ruling.

Gates after the revision:

- `gridflow-build --only neso_data_portal/aggregated_bsad` succeeds; the only message is the caveat warning above.
- `detect.mjs --json` returns `[]`; the page has 0 em dashes.
- Mirror `cmp` is clean. The note keeps CRLF on all 434 lines.
- Re-screenshotted the chart section at 1440, 768 and 390 (iframe): nothing is clipped, and the key note fits beside or under the chart.
- No artefact needed re-running: the spec, sample select and notebook cells are unchanged.

| Finding | Fix |
|---|---|
| 1 (major): the 2020-21 gap reads as zero | Fixed in words, renderer untouched (seat ruling). The chart spec has no y floor key (`chart_spec._ALLOWED_KEYS`), so I could not move the axis off zero. **Key note** now: "No data April 2020 to March 2021: that flat stretch is the axis, not zero." **Caption** now ends "No data April 2020 to March 2021 (file fails to load); that stretch is the axis, not zero." **Alt** now says "No line April 2020 to March 2021, only the axis: that file fails to load." The x label "no file loaded for 2020-21" stays. The old key note on the sign convention was dropped; the `bpa` and `spa` guide lines still say NESO does not state it. |
| 2 (nit): "superseded, carried as zero (BSC)" was a paraphrase | I tried to read the BMRA Service Description myself: two web searches, and a fetch of the bscdocs v25.0 page, which returned only its table of contents. Since I could not read the text, I did not cite it. `what_it_is` now says "The six cost and volume terms are zero in every row shown"; the six guide lines are now name and unit only, for example "Energy buy cost adjustment, £ (NESO)". The note body's FACTS-sourced sentence is unchanged. |
| 3 (nit): "back-tests" without the capture-time caveat | `how_used[0]` is now "NESO's buy price adjuster per settlement period, for imbalance price studies." |
| 4 (nit): `notebook.needs` implied every file loads | Now "one capture of each file from 2016-17 on; 2020-21 will not load". |
| 5 (nit, optional): what BPA is | Not applied. The checker's source was a model-summarised read of Elexon's glossary that the checker flagged as unconfirmed, and I have no readable vendor text for the formula or the "added when short" rule. The page keeps to what NESO states. |

### Editing note

- An Edit `replace_all` on the six guide lines merged the unquoted lines, because their line endings went with the match. That broke the YAML, and one build failed with orphan-artefact errors.
- I rewrote that six-line segment with a byte-level script that writes CRLF explicitly, then checked that LF and CRLF counts match.
- No other lines were affected (`git diff --numstat`: 125 added, 6 removed, the same body spans as before).

## Nit fix

`notebook.needs` is now "a capture of NESO's yearly files from 2016-17", so the template line reads "...with a capture of NESO's yearly files from 2016-17 ingested." The 2020-21 loss stays in the caption and key note. Build clean, detector `[]`, mirror `cmp` clean.
