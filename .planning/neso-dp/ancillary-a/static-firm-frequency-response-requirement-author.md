# Static FFR requirement: author report

One-table page `static-firm-frequency-response-requirement` (table `sffr_requirement`). Writer, 2026-10-18.

## Status

- `gridflow-build --only neso_data_portal/sffr_requirement`: page written. The only warning is the known one (3 dropped
  "Known issues and gotchas" lines; this note has no such section).
- Detector on `site/hifi/data-sources/neso_data_portal/static-firm-frequency-response-requirement.html`: `[]`.
- Built page: 0 em or en dashes, middle dots, arrows; no "locally", "live", "now", "our ", "since 20", planning words.
- Canonical note (`C:\gridflow-wt\vault-neso-as-a\30-vendors\neso-data-portal\datasets\static-firm-frequency-response-requirement.md`)
  edited with the Edit tool: 367 lines, 367 CRLF. Diff against `origin/master`: +122 / -2 (the `page:` block, `updated`,
  one inserted body sentence). Mirror `vault/neso_data_portal/static-firm-frequency-response-requirement.md` copied, `cmp` equal.
- Artefacts (front-end worktree `C:\gridflow-wt\fe-neso-as-a`):
  `site/hifi/data/series/neso_data_portal/sffr_requirement.json` (gridflow-distil, spec_origin vault, 1 series x 39 points,
  39 rows read, matched and used),
  `site/hifi/data/samples/neso_data_portal/sffr_requirement.json` (gridflow-sample, 8 rows, 16 columns),
  `site/hifi/data/notebooks/neso_data_portal/sffr_requirement.json` and `sffr_requirement-6.png` (run_notebooks.py, 6 cells,
  no errors). No staged chart spec or authored override existed.
- Screenshots at 1440, 1024, 768 and a true 390 px iframe, every section looked at (hero scenery, chart and key, raw feed,
  frame and guide, notebook panel, related, stratum corner labels): nothing clipped or overlapping. Shots in the scratchpad
  `sffr-req-writer\` (`f-<width>.png`, `s-<width>-<n>.png`). The first 1440 capture painted blank below the frame heading (a
  headless paint glitch); a retake at a shorter window rendered the whole page.
- My server on 9948 stopped. 9670 not touched. No git.

## Data truth

- **Captures.** One bronze capture (2026-10-08T11:17:40Z, body 1,650 bytes, 39 data rows, sha256 `151d3950...` matching the
  sidecar), one silver file. No newer capture exists, so the truncated-capture risk does not apply.
- **What one row is, and the key.** 39 rows, 39 distinct `efa_date`, 23 September to 31 October 2026, consecutive (every
  step one day). `service` is `SFFR` on all 39 rows. Registry `entity_key: [efa_date]`, `latest: whole_capture`. One row is
  one EFA date with six EFA block columns; unlike DM and DR there is one service, so the key is `efa_date` alone.
- **Units.** MW on `EFA1` to `EFA6` from NESO's dictionary (`field-info/20261008T114228Z/sffr_requirement.json`: unit `MW`,
  "Our requirement for the service (before overholding) for this EFA", example `250`). Registry dtype float64.
- **Issue time versus delivery window.** The file has no issue column (registry `issue: {kind: none}`). `published_at` is
  the file's CKAN last-modified read as UTC (`vintage: ckan_last_modified`; silver 2026-09-22 14:48:22.737387 UTC, equal
  to the sidecar `ckan_last_modified`), one value on every row. Delivery: each EFA date starts 23:00 UK time the evening
  before (NESO's dictionary comment "EFA Date starts at 23:00 D-1 running through to 23:00"); `timestamp_utc` is UK
  midnight of the date in UTC (registry `date_sp1(efa_date)`; silver 23 Sep gives 22 Sep 23:00 UTC, 25 Oct gives 24 Oct
  23:00 UTC, 26 Oct gives 26 Oct 00:00 UTC). The page never calls `published_at` an issue time.
- **Earlier editions.** Not kept: each date appears once and the file is one replacement view (`whole_capture`). Whether
  NESO drops past dates or amends values at its monthly update is unknown from one capture; the page claims neither.
- **Values.** Every one of `efa1` to `efa6` holds only 250.0 on all 39 dates, no nulls (234 block values). The page says so
  plainly in the caption, key note and alt, scoped to "the file" / "this file". No trend is drawn or implied.
- **Block boundaries.** NESO's SFFR auction results (silver `sffr_auction_results_main`, newest capture published
  2026-10-16, which has more rows than the 2026-10-08 one, so it is not truncated) label `efa` 1 to 6 with
  `delivery_start`/`delivery_end` 23:00 previous date to 03:00, then 03:00, 07:00, 11:00, 15:00, 19:00 to 23:00, on 23
  September 2026 (BST, so the labels are UK local, not UTC) and unchanged on the clock-change dates 2025-03-30, 2025-10-26
  and 2026-03-29. That is the basis for the `efa1`..`efa6` lines and is now in the note body.

## The page in one paragraph

Chart: line, `efa1` per `efa_date` grouped by `service` (one series, `SFFR`, petrol), filtered to the 22 September file,
window 23 September to 31 October 2026, `y_min: 0`; flat at 250 MW on all 39 dates. Caption, key note and alt say every block
on every date in the file is 250 MW. Frame: eight dates (first two, 24 to 27 October around the clock change, last two),
every block column, `timestamp_utc` and `published_at` in view at 1440. Notebook: `data.sql` on `_latest`, a one-line summary
(first, last, 39 dates, file time in UTC), min/max/count per block (all 250/250/39), block starts in UTC around 25 October
(block 1 from 22:00 UTC on 24 October, 5.0 hours), and a step plot at block starts in UTC.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Key `efa_date`; one row per EFA date, six block columns (facts, record.key) | registry `static-firm-frequency-response-requirement.json` (`entity_key: [efa_date]`, header `EFA_DATE,Service,EFA1..EFA6`); silver 39 distinct of 39 |
| NESO's forecast of the SFFR it needs (summary, what_it_is) | catalogue snapshot `20261006T195819Z`: notes "This dataset will contain our forecasted requirements for Static Firm Frequency Response."; resource description says the same for Static FFR |
| File titled Static Firm Frequency Response Requirement (what_it_is) | sidecar `resource_name`; snapshot resource name |
| Updated monthly (facts, what_it_is) | snapshot extras `Update frequency: Monthly`; registry `refresh: monthly` |
| Bought in a daily auction (facts, what_it_is) | sibling package notes "results from daily auction for static FFR" (same snapshot); package tags Day-ahead Auction |
| One CSV file, no archive (facts) | snapshot `num_resources: 1`; registry one resource |
| MW before overholding (caption, fields, what_it_is) | field-info `sffr_requirement.json` (each EFA column: unit `MW`, "before overholding") |
| Blocks from 23:00 the evening before, UK clock (what_it_is, fields, caption) | dictionary comment on `EFA_DATE`; SFFR auction results `delivery_start` labels (above) |
| Block 1 lasts 3 or 5 hours at clock changes (what_it_is) | wall-clock 23:00 to 03:00 every date (auction labels on clock-change dates); notebook cell 5: 25 Oct block 1 starts 2026-10-24 22:00 UTC, 5.0 h. Same wording as the approved DM and DR pages |
| `SFFR` on every row of this file (service) | silver `value_counts`: SFFR 39; dictionary "SFFR = Static Firm Frequency Response" |
| 250 MW in every block on all 39 dates (caption, key note, alt, plot_alt) | silver unique of each `efa1`..`efa6` is `[250.0]`, 0 nulls; notebook cell 4 (250/250/39 per block); series file 39 x 250.0 |
| `timestamp_utc` UK midnight of the date in UTC; block 1 an hour earlier (field, record caption) | registry `temporal: date_sp1(efa_date)`; silver values above; sample rows 25 Oct 23:00, 26 Oct 00:00 |
| `published_at` the file's last-modified read as UTC (field, how_used) | registry `vintage: ckan_last_modified`; silver = sidecar |
| Raw requests | sidecar `request_url`; `package_show?id=<package>` as on the approved DM, DR and QR pages |
| `--last 24h`; dates select nothing; skip when `last_modified` unchanged (raw note, commands) | `client.py:1474-1545` (window must end within 48 h), `client.py:1750-1765` (unchanged skip); same lines as the approved DM, DR, QR pages |
| `query()` reads the same `_latest` view on `efa_date` (notebook lead) | gridflow_models: `_relation_name_for_dataset('sffr_requirement')` = `silver_neso_data_portal_sffr_requirement_latest`; `_DATE_COLUMN_BY_DATASET['sffr_requirement']` = `efa_date` |
| Plot from 22:00 on 22 September to 19:00 on 31 October UTC (plot_alt) | 23 Sep block 1 23:00 BST = 22:00 UTC; 31 Oct block 6 19:00 GMT = 19:00 UTC; PNG viewed |
| Compare with cleared SFFR in the auction results; join on EFA date and block, not `timestamp_utc` (how_used) | note Modelling notes ("for comparison with procured volumes"; "join on `efa_date` plus the block column, not on `event_time`") and Gotchas; auction results carry `date` and `efa` |
| Related: auction results carry cleared MW and clearing price per EFA date and block | silver `sffr_auction_results_main` columns `date`, `efa`, `accepted_volume`, `clearing_price` |
| Related: DM and DR same EFA block layout, low and high products | note Gotchas (same `EFA_DATE` plus `EFA1`-`EFA6` shape); approved DM and DR pages (`DML`/`DMH`, `DRL`/`DRH`) |
| Related: `elexon/freq` | service name (Firm Frequency Response); same line as the approved DR page |

## Body corrections (canonical note)

1. Clocks paragraph: after "`TODO: verify` those boundaries against NESO's EAC guidance before anyone composes block
   instants." inserted one sentence: NESO's own SFFR auction results label the same six blocks (`delivery_start`,
   `delivery_end` per `efa`: 23:00 previous date to 03:00, then four-hour blocks to 23:00, UK local wall clock), unchanged on
   the clock-change dates 2025-03-30, 2025-10-26 and 2026-03-29 (silver `sffr_auction_results_main`, capture published
   2026-10-16, read 2026-10-18). The TODO is kept (EAC guidance itself was not read).
2. Front matter `updated` 2026-10-13 to 2026-10-18.

No existing sentence changed. The body's other facts (one capture, 39 rows, 250 everywhere, sha, sizes, clocks) re-checked
and true.

## Unverified

- Whether NESO drops past dates or amends values at each monthly update (one capture). The page claims neither.
- What "before overholding" adds before comparing with procured volume. The page states the vendor's words only.
- Report only, not on the page: summing `accepted_volume` per date and block in the auction results over 23 September to
  17 October gives 114.4 to 256.2 MW (median 229.7) against the 250 MW requirement.

## Open questions

1. A second capture after NESO's next monthly update would show replace-versus-append behaviour. Worth keeping the package on
   the periodic capture.
2. The chart is a flat single line; the seat's DR ruling (flat values said plainly) is followed. If the seat prefers no
   chart for a constant table, that is a template choice.

## Template problems (report only)

- At 768 and 390 the folded frame hides `timestamp_utc`, so the record caption's clock-change point needs unfolding (known item).
- Notebook preview wraps long names mid-word at 390 (known item).
- The notebook's grouped outputs carry the runner's leading blank column (known item; cells 3 to 5 here).

## Checker: look hardest at

- The `efa1`..`efa6` block times and "block 1 lasts 3 or 5 hours at clock changes": based on the dictionary comment plus the
  SFFR auction results' delivery labels (body sentence 1), and notebook cell 5.
- "Every block on every date in the file is 250 MW" (caption, key note, alt): scoped to the file.
- The record caption "from 26 October `timestamp_utc` is 00:00 UTC, not 23:00" against the sample rows.
- The how-used join bullet: the auction results' `date` and `efa` columns as the join keys.

## Defects

- No new gridflow or data defect on this package. The table has a single complete capture.
- Sibling note (not touched): the SFFR auction results' `delivery_start` and `delivery_end` are naive strings in UK local
  wall-clock time; whoever writes that page should check how they are described.

## Nits fixed (after the checker's APPROVE with 4 nits)

1. **Body indentation.** The inserted Clocks sentence now carries the paragraph's two-space indent (it no longer breaks the item).
2. **The `TODO: verify` on block boundaries is resolved.** The sentence now reads "NESO's own SFFR auction results confirm those
   boundaries for this service: ..." (same evidence: `delivery_start`/`delivery_end` per `efa`, UK local wall clock, unchanged
   on 2025-03-30, 2025-10-26 and 2026-03-29; silver `sffr_auction_results_main`, capture published 2026-10-16). What stays
   open is said plainly: "NESO's EAC guidance itself was not read; SFFR is not an EAC product." Nothing in the note now
   composes block instants, so no TODO is needed for that.
3. **`record.fields.timestamp_utc`** now "Calendar date `efa_date` at UK midnight, in UTC; block 1 begins an hour before"
   (13 words). The checker's suggested wording was 18 words, over the 14-word budget; this keeps "calendar date" so it cannot
   be read as the EFA day's 23:00 start.
4. **`how_used[1]`** now "Join those results on EFA date and block number (`efa`), not on `timestamp_utc`."

Re-checked: canonical note CRLF kept (367 lines, 367 CRLF), mirror `cmp` equal; `gridflow-build --only
neso_data_portal/sffr_requirement` wrote the page (known dropped-caveat warning only); detector `[]`; 0 em or en dashes,
middle dots, arrows; both new page lines present in the built HTML. Artefacts unchanged (no chart, sample or notebook field
touched; digests pass). No server started; 9670 untouched; no git.
