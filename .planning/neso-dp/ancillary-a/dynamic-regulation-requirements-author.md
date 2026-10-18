# Dynamic Regulation requirements: author report

One-table page `dynamic-regulation-requirements`, lead `dr_requirements`. Writer, 2026-10-18.

## Status

- `gridflow-build --only neso_data_portal/dr_requirements`: success (the "3 lines in Known issues and gotchas" warning
  comes from other notes; this note has no such section).
- Detector on `site/hifi/data-sources/neso_data_portal/dynamic-regulation-requirements.html`: `[]`. Built page: 0 em
  or en dashes, middle dots, arrows; no `locally`, `our`, `since 20`, `now`, `live`, planning words.
- Canonical note (vault worktree) edited with the Edit tool; CRLF kept (258 lines, 258 CR); diff against
  `origin/master` +121 / -1 (the `page:` block and `updated`). Mirror copied, `cmp` equal.
- Artefacts (front-end worktree): `site/hifi/data/series/neso_data_portal/dr_requirements.json` (spec_origin vault,
  2 series x 39 points), `samples/neso_data_portal/dr_requirements.json` (gridflow-sample, 8 rows),
  `notebooks/neso_data_portal/dr_requirements.json` and `dr_requirements-6.png` (run_notebooks.py, 4 cells after setup
  and help card, no errors). No staged chart spec or authored override existed.
- Screenshots at 1440, 1024, 768 and a true 390 px iframe (scratchpad `dr-shots\`), plus the expanded notebook at 1024
  in a browser tab: nothing clipped or overlapping; page `scrollWidth` 1009 at 1024. Server on 9944 stopped.

## The page in one paragraph

The data is thin and flat, and the page says so. One capture of one file (NESO last modified 2026-09-22 14:48:17 UTC)
holds 78 rows: 39 EFA dates, 2026-09-23 to 2026-10-31 with no gap, times `DRL` and `DRH`; all 468 block cells are
480.0 MW. Chart: line, x = `efa_date`, EFA block 1 per product, pinned to that file by `published_at`, `y_min: 0`;
both lines flat at 480 MW and coincident (the renderer dashes the later line over the earlier, which the key notes
and alt describe). Frame: both products on the first and last EFA dates, the clock-change date 25 October and 26
October, which shows `timestamp_utc` moving from 23:00 UTC to 00:00 UTC. Notebook: `data.sql` on `_latest`, a
per-product date range, min/max/count over all six blocks (480/480/234 each), the block starts converted from UK local
to UTC for 25 October (block 1 from 22:00 UTC, 5 hours), and a step plot in UTC.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| One row per EFA date and product; key `efa_date`, `service` | registry `connectors/neso_data_portal/registry/dynamic-regulation-requirements.json` (`entity_key`); silver: 78 rows, 78 distinct keys, every date has 2 rows |
| Six block columns, MW, "before overholding" | NESO data dictionary captured in gridflow `docs/neso_data_portal/profile/families/dr_requirements.json` `field_info`: each `EFA1`..`EFA6` "Our requirement for the service (before overholding) for this EFA", unit `MW` |
| `DRL` low, `DRH` high; dictionary writes `DR-L`, `DR-H` | same `field_info.Service`: "DR-L = Dynamic Regulation Low / DR-H = Dynamic Regulation High"; body values `DRL`/`DRH` (silver value counts 39 each) |
| EFA blocks on the UK clock from 23:00 the evening before; edges 03:00, 07:00, 11:00, 15:00, 19:00, 23:00; block 1 is 3 h in spring, 5 h in autumn | gridflow `.planning/phases/v0.22-K-AS-1/K-AS-1-FACTS.md` §5.1 (NESO EAC explainer Appendix B; DC history dictionary); note body "Column semantics". Corroborated: silver `eac_results_summary` `DRL`/`DRH` deliveries start 22:00, 02:00, 06:00, 10:00, 14:00, 18:00 UTC in BST (23:00, 03:00 ... local); notebook cell 5 gives block 1 of 25 Oct 2026 = 5.0 h |
| "latest view", "updates published here"; ad hoc; one file, no archive | vendor resource description and package metadata quoted in the note body; registry lists one resource, `url_type` upload |
| `timestamp_utc` = UK midnight opening the EFA date, in UTC; block 1 an hour earlier | registry `temporal: date_sp1(efa_date)`; `silver/neso_data_portal/casting.py:619-626` (`settlement_period_to_utc(date, 1)`); silver: 25 Oct gives 2026-10-24 23:00 UTC, 26 Oct gives 2026-10-26 00:00 UTC; `silver/date_columns.py` comment "a label anchor, not an EFA or window start" |
| `published_at` = file last-modified, read as UTC | registry `vintage: ckan_last_modified`; `silver/neso_data_portal/_bronze.py:130,193`; sidecar `ckan_last_modified` 2026-09-22T14:48:17.409242 equals silver |
| Chart values, alt, key notes ("480 MW on all 39 dates") | committed series: DRH {480.0} x 39, DRL {480.0} x 39, x 2026-09-23 to 2026-10-31 |
| Coincident lines drawn dashed | `chart_svg.py:572-590` (a dot chart dashes a series where it lands on an earlier one); zoomed render shows clay dashes over petrol |
| `query()` reads `silver_neso_data_portal_dr_requirements_latest`, `efa_date` DATE BETWEEN | models interpreter: `_relation_name_for_dataset("dr_requirements")`, `_validate_dataset_for_source` gives `efa_date`; `_get_method_registry.py` `_date_range_predicate` |
| Raw requests | sidecar `request_url` (2026-10-08 capture); `package_show?id=` as on the approved NESO pages |
| `--last 24h`, whole file, `last_modified` skip, dates select nothing | `connectors/neso_data_portal/client.py:1474+` (window admissibility), `client.py:1752-1765` (unchanged skip); same commands as the approved Balancing Reserve and Aggregated BSAD pages |
| Related: EAC cleared `DRL`/`DRH` per EFA block | silver `eac_results_summary` products `DRL`, `DRH`, four-hour deliveries |
| Related: long-term page wording | that page's approved summary ("twelve-month outlook ... weights over requirement bands") |

## Body corrections (canonical note)

Only front matter `updated` 2026-10-13 to 2026-10-18. The body is accurate against code and silver: bronze still holds
the single 2026-10-08 capture, so "Only one capture of the resource exists" and the amendment TODOs stand.

## Unverified

- That `DRL` is the low-frequency side and `DRH` the high-frequency side (note body wording): not on the page, which
  says only "low" and "high" as NESO's dictionary does.
- Whether NESO keeps earlier editions anywhere: the package has no archive resource; how a later version amends or
  drops dates is unmeasured with one capture. The page claims only that NESO publishes updates in the same file.
- Report only, not on the page: cleared `DRL` in EAC results sits at 478 to 480 MW against this 480 MW requirement;
  cleared `DRH` is mostly 500 MW (480 to 500), above the 480 MW figure. That may reflect overholding; nobody has
  verified it.

## Open questions

1. A chart of two coincident flat lines is honest but says little beyond "480 MW". `type: none` exists in the spec
   schema but no note uses it, so I kept a chart that shows the horizon and the level. The seat may prefer otherwise.
2. When a second capture lands, the chart and rows stay pinned to the 22 September file by their `published_at`
   filter; the notebook reads whatever `_latest` holds.

## Template problems (report only, nothing worked around)

- The notebook output parser (`scripts/run_notebooks.py` `dataframe`) flattens pandas' two-row header when the index
  is named (a `groupby` result), so the index name appears as an extra column and the column list is longer than each
  row (seen in the committed EAC results and DM notebooks, for example `['', 'first', 'last', 'dates',
  'published_utc', 'service', '', '', '', '']`). I avoided it on this page with `.reset_index()`.
- Known items confirmed on this page: the notebook preview breaks `silver_neso_data_portal_dr_requirements_latest`
  mid-word at 390; at 768 and 390 the folded frame shows only the first block columns until unfolded.

## Checker: look hardest at

- The key notes and alt describe the coincident lines ("the low product's line runs along it", "dashed over the high
  line"): confirm against the render.
- `efa1` field line "spring change 3 hours, autumn 5" and the `timestamp_utc` line across 25 and 26 October.
- The notebook lead's reason for `data.sql` over `query()`.

## Defects

- No gridflow or data defect found on this package.
- Template: the notebook runner's dataframe parser reads a named index header (a groupby output) as extra columns;
  the committed EAC results and DM notebook outputs carry the misaligned header.
