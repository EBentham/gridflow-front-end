# Dynamic Moderation requirements: author report

One-table page `dynamic-moderation-requirements` (table `dm_requirements`). Writer, 2026-10-18.

## Status

- `gridflow-build --only neso_data_portal/dm_requirements`: success. The stderr warning about 3 dropped "Known issues
  and gotchas" lines is the same one the BR page reported; this note has no such section.
- Detector on `site/hifi/data-sources/neso_data_portal/dynamic-moderation-requirements.html`: `[]`.
- Built page: 0 em dashes, en dashes, middle dots, arrows; no "locally", "our", "live", "now", planning words.
- Canonical note edited with the Edit tool; CRLF kept (358 lines, 358 CR). Vault diff against `origin/master`:
  +120 / -4 (the `page:` block, `updated`, two body spans). Mirror copied and `cmp` equal.
- Artefacts (worktree `C:\gridflow-wt\fe-neso-as-a`):
  `site/hifi/data/series/neso_data_portal/dm_requirements.json` (spec_origin vault, 2 series x 39 points, 78 rows used),
  `site/hifi/data/samples/neso_data_portal/dm_requirements.json` (gridflow-sample, 8 rows),
  `site/hifi/data/notebooks/neso_data_portal/dm_requirements.json` and `dm_requirements-5.png` (run_notebooks.py,
  5 cells, no errors). No staged chart spec or authored override existed.
- Screenshots at 1440, 1024, 768 and a 390 px iframe, every section looked at: nothing clipped or overlapping. At 768
  the folded frame still shows all six block columns. The site has no dark scheme (no `prefers-color-scheme` in
  `site/hifi/assets/*.css`). Shots in the session scratchpad `dm-shots\` (f-*.png full, s-<width>-<n>.png slices).
- Server on 9943 stopped. 9670 not touched.

## The page in one paragraph

The data are thin and flat: silver holds one capture of NESO's file (CKAN `last_modified` 2026-09-22 14:48:12 UTC),
39 EFA dates (23 September to 31 October 2026) times `DMH`/`DML`, and every date carries the same six block values
(`DMH` 570, 510, 510, 510, 510, 570; `DML` 530, 500, 500, 530, 500, 530 MW). The page says so and invents no trend.
Chart: line, `efa_date` on x, `efa1` grouped by `service`, filtered to that file's `published_at`, `y_min: 0`: two
flat lines, 570 and 530 MW, captioned as block 1 only. Frame: both services on the first and last dates, the autumn
clock-change date 25 October and 26 October (shows `timestamp_utc` moving from 23:00 to 00:00 UTC). Notebook:
`data.sql` on the `_latest` view, a per-service summary (first, last, count, file time in UTC), the distinct block
profiles (two rows), and a bar plot of the six blocks for the first EFA date, which is the page's most informative
reading.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Key `efa_date`, `service`; `_latest` whole capture | registry `src/gridflow/connectors/neso_data_portal/registry/dynamic-moderation-requirements.json` (`entity_key`, `latest: whole_capture`) |
| One row per EFA date and service, six block columns (grain) | registry epoch header `EFA_DATE, Service, EFA1..EFA6`; silver 78 rows, 78 distinct keys |
| MW, "before overholding" (fields, caption, what_it_is) | vendor dictionary `.planning/research/neso-snapshots/field-info/20261008T114228Z/dm_requirements.json:39-43` (and each EFA column): unit `MW`, "Our requirement for the service (before overholding) for this EFA" |
| `Service` dictionary text describes Dynamic Regulation (service field) | same file lines 27-30: "DR-L = Dynamic Regulation Low, DR-H = Dynamic Regulation High", example `DR-L`; silver values only `DMH`, `DML` |
| `DML` low, `DMH` high; frequency response service | K-AS-1-FACTS line 142 (EAC guidance Appendix A product codes); note body para 1-2 |
| "latest view", updates published in the same file; Ad hoc; one file, no archive (facts, what_it_is) | catalogue snapshot `20261006T195819Z`: resource description "This dataset provides our latest view of our requirements for the Dynamic Moderation Service, any updates to our requirements will be published here."; extras `Update frequency: Ad hoc`; `num_resources: 1` |
| Block boundaries 23:00 (previous date) to 03:00, then four-hour blocks to 23:00, UK local; block 1 is 3 h in spring, 5 h in autumn (fields, what_it_is, caption) | K-AS-1-FACTS §5.1 lines 442-470 (NESO EAC explainer Appendix B; DC history dictionary FI 51-111; elapsed hours 24/23/25, EFA 1 4/3/5) |
| `timestamp_utc` = UK midnight of `efa_date` in UTC; block 1 an hour earlier | registry `temporal: date_sp1(efa_date)`; `silver/neso_data_portal/casting.py:609-628` (`settlement_period_to_utc(date, 1)`); silver 2026-10-25 -> 2026-10-24 23:00 UTC, 2026-10-26 -> 2026-10-26 00:00 UTC. Block 1 opens 23:00 local the previous date, always one local hour before local midnight; clocks change at 01:00 UTC, after it |
| `published_at` = file last-modified read as UTC | registry `vintage: ckan_last_modified`; `silver/neso_data_portal/_bronze.py:192-206` (naive CKAN stamp read as UTC, corroborated, not a vendor contract); sidecar `ckan_last_modified` 2026-09-22T14:48:12.082389 = silver |
| Chart: 2 series x 39 points, DMH 570, DML 530 (alt, key notes) | committed series: x 2026-09-23..2026-10-31 (39), DMH {570.0}, DML {530.0} |
| Raw requests | sidecar `request_url` of the only capture; `package_show` as on the BR and showcase pages |
| `--last 24h` ingest/transform; dates select nothing; skip if `last_modified` unchanged | `connectors/neso_data_portal/client.py:1474-1545` (window end not future, not over 48 h stale), `client.py:1752-1765` (upload skip on unchanged `last_modified`); same as the approved BR page |
| `query()` reads `silver_neso_data_portal_dm_requirements_latest`, `efa_date BETWEEN` inclusive (notebook lead) | resolved in the models interpreter: `_DATE_COLUMN_BY_DATASET['dm_requirements'] = efa_date`, relation `..._dm_requirements_latest`; `_get_method_registry.py:58-96`; gridflow `silver/date_columns.py:59` (`efa_date` DATE) |
| Related: EAC results carry `DML`/`DMH` MW and price per EFA block | silver `eac_results_summary`: products DMH, DML, delivery 2026-03-31 22:00 to 2026-10-17 18:00 UTC in four-hour blocks, `cleared_volume`, `clearing_price` |
| How used: EAC join needs the UK start time converted to UTC | joined requirement to `eac_results_summary` by converting `delivery_start` to Europe/London and assigning blocks from 23:00: 300 of 300 (date, service, block) matches over 25 dates (23 Sep to 17 Oct) |
| Related: DR sibling uses `DRL`/`DRH` in the same layout | silver `dr_requirements` services `DRH`, `DRL`; FACTS line 434 (wide `EFA1`-`EFA6` beside `EFA_DATE`) |
| Related: long-term outlook as band weights | held page note `long-term-forecasts-for-dc-dm-dr-requirements` what_it_is (nine bands, `Possibilities` 0 to 1) |
| Related: `elexon/freq` is system frequency | `vault/elexon/freq.md` summary |

## Body corrections (canonical note)

1. "Clocks", event-time bullet: the `TODO: verify` on the EFA block boundaries is settled by evidence already in the
   batch research: K-AS-1-FACTS §5.1 quotes NESO's EAC explainer Appendix B and the DC history dictionary for the
   boundaries and gives the 3 h / 5 h block 1 on clock-change dates. Replaced the TODO sentence with the boundaries
   and the citation.
2. "Value ranges": added one sentence that each service carries one block profile on all 39 dates of the capture,
   with the values (silver, 2026-10-18), kept as a one-capture observation.
3. Front matter `updated` 2026-10-13 to 2026-10-18.

Nothing else in the body changed. The body's capture facts (one capture, 2026-10-08) are still true: bronze and silver
hold only that capture.

## Unverified

- Whether NESO drops past dates, amends values in place or keeps the horizon length: one capture only. The page says
  only what NESO says ("latest view", updates "published here") and claims no history.
- How the requirement relates to what NESO buys in the EAC auction (note body TODO). Cleared `DMH`/`DML` MW sits close
  to the requirement per block over 23 September to 17 October (for example `DMH` block 1 cleared 569 to 590 against
  570; `DML` block 3 cleared 300 to 500 against 500), and sometimes above it, which fits "before overholding" but is
  not stated by NESO. Not on the page: the how-used bullet says only to compare them.
- The `Service` dictionary error was read from the 2026-10-06 field-info snapshot; not rechecked against the live
  portal (no live calls).

## Open questions

1. A second capture of this file would answer the replace-in-place and horizon questions and make a richer chart
   (requirement by issue). Worth adding the package to a periodic capture if NESO changes it.
2. Chart choice: the template cannot put the six blocks on the x axis (`values` is for time charts only; a bar chart
   takes one value column), so the chart shows block 1 over dates and the notebook plots the block profile. If the
   seat prefers a different block or a `values` chart for one service, say so; the latter draws overlapping lines
   (four of `DMH`'s six blocks are 510 MW).

## Template problems (report only)

- No template-level way to chart a wide table's columns as categories (block profile). Not worked around.
- The notebook preview wraps long identifiers mid-word at 390 (`silver_neso_data_portal_dm_re` / `quirements_latest`),
  already listed under the batch file's template follow-ups. Nothing is clipped.

## Checker: look hardest at

- The flat chart: caption, key notes and alt say block 1 only and "on all 39 dates here"; confirm it reads as a
  statement about this file, not a vendor rule.
- `efa1` field line ("spring change 3 hours, autumn 5") and `timestamp_utc` ("block 1 starts an hour earlier") across
  clock-change dates.
- The `service` field line on the copied Regulation dictionary text.
- The how-used EAC join bullet against `eac_results_summary.delivery_start`.

## Defects

- Vendor documentation: NESO's column dictionary for `dm_requirements` (`Service`) describes Dynamic Regulation
  (`DR-L`, `DR-H`, example `DR-L`) while the file carries `DML` and `DMH`. Already recorded in the note's Gotchas and
  K-AS-1-FACTS (line 142); no new gridflow defect.
- No new gridflow or data defect found on this package.

## Nits fixed (after the checker's APPROVE with 6 nits)

1. `chart_view.key[0].note` (DMH): now "570 MW on all 39 dates here; every block repeats on every date in this file."
   (Polars: service plus `efa1`..`efa6` groups into 2 groups of 39.)
2. `record.fields.service`: "`DML` (low) or `DMH` (high); NESO's column dictionary lists Dynamic Regulation's `DR-L`,
   `DR-H`" (field-info lines 27-30).
3. `record.fields.efa1`: now "Block 1, 23:00 to 03:00 UK time, MW before overholding (NESO)", matching blocks 2 to 6.
   The clock-change length moved to `what_it_is` ("block 1 lasts 3 or 5 hours at clock changes", FACTS §5.1).
4. `record.fields.timestamp_utc`: "UK midnight starting calendar date `efa_date`, in UTC; block 1 starts an hour
   earlier". `record.caption`: "First and last dates; around 25 October's clock change `timestamp_utc` goes from
   23:00 to 00:00 UTC." (silver: 25 Oct 23:00 UTC on the 24th, 26 Oct 00:00 UTC).
5. `what_it_is`: names the file's title once, "titled Indicative DM Requirements and called its latest view" (resource
   name in the catalogue snapshot and the sidecar). 59 words.
6. `how_used[2]`: the unsourced "feature for response price models" bullet is replaced with what the note supports
   (Modelling notes: "Use the whole capture as one point-in-time vintage"; Clocks: `available_at` = `published_at`):
   "Point-in-time studies: each capture is one vintage, stamped with the file's `published_at`."

Re-checked: canonical note CRLF kept (358 lines, 358 CR), mirror `cmp` equal; `gridflow-build --only
neso_data_portal/dm_requirements` succeeds (only the known dropped-caveat warning); detector `[]`; built page has no em
or en dashes, middle dots or arrows; a 390 px view of the changed lines shows nothing clipped. Artefacts unchanged (no
chart, sample or notebook field was touched). My 9943 server stopped; 9670 untouched; no git.

Summary: all six nits fixed in wording only; the page builds clean, detector `[]`, mirror equal.
