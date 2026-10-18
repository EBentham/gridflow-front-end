# Constraint breakdown: writer's report

Page `neso_data_portal/constraint-breakdown` (single table `constraint_breakdown`), written 2026-10-18.

## Status

- Build: `uv run --system-certs --extra build gridflow-build --only neso_data_portal/constraint_breakdown` succeeds,
  no content errors. (The "3 lines in Known issues and gotchas" warning is global; this note has no such section.)
- Detector: `detect.mjs --json site/hifi/data-sources/neso_data_portal/constraint-breakdown.html` returns `[]`. Em
  dashes in the page: 0.
- Mirror: `vault/neso_data_portal/constraint-breakdown.md` is byte-equal to the canonical note (`cmp` clean, CRLF
  kept, 0 bare LF).
- Artefacts (all from real data): `site/hifi/data/series/neso_data_portal/constraint_breakdown.json` (spec_origin
  vault), `site/hifi/data/samples/neso_data_portal/constraint_breakdown.json`,
  `site/hifi/data/notebooks/neso_data_portal/constraint_breakdown.json` and `constraint_breakdown-5.png`.
- Screenshots: headless Chrome at 1440, 1024 and 768, and 390 through an iframe, plus the built-in browser pane for
  the opened notebook and the unfolded frame. Nothing clipped or overlapping. The site has no dark scheme (no
  `prefers-color-scheme` or `data-theme` rule in `site/hifi/assets/`), so "dark" renders identical to light.
- No staged chart spec or authored override existed for this dataset.

## Chart

Line, `thermal_constraints_cost_gbp` in £, one value per date (dedup on `date`, newest `published_at`, aggregation
`last`), window 1 April 2017 to 11 October 2026, 3,480 points. x is the vendor `date` column itself (a `Date`, so no
UTC bucketing shifts BST days). Why thermal alone: the chart spec takes one `value` column and series only come from
a `group` column, and this table is wide (one column per reason), so the four reasons cannot be stacked or overlaid
(template limitation below). Thermal is the largest reason in every April-to-March year; the notebook prints the
yearly sums of all four and stacks all four for the open year, so the page still shows every reason. £ and MWh never
share an axis.

## Evidence table

| Claim | Evidence |
|---|---|
| One row = one date of one capture of one yearly file; code identity `resource_id, date` | registry `connectors/neso_data_portal/registry/constraint-breakdown.json` (`entity_key: [resource_id, date]`, `latest: whole_capture`, `latest_partition: resource_id`) |
| Page key `resource_id, date, published_at` | silver holds every capture; `(date, published_at)` unique over all 3,664 rows (Polars `is_unique`); an upload member is only re-downloaded when its `last_modified` changes (`client.py` `iter_members`, ~1740-1760), so each capture of a resource has its own `published_at` |
| Four reasons, cost £ and volume MWh each | registry header (8 value columns); vendor dictionary units quoted in the note (Units section) |
| `date` is NESO's date; day boundary not stated by NESO | note quotes the vendor: "the date of the costs/volumes"; no code or vendor statement of the accounting window |
| `timestamp_utc` = start of SP1 of `date`, GB local midnight as UTC | `silver/neso_data_portal/casting.py` ~619-624 (`settlement_period_to_utc(value, 1)` for `date_sp1`); rows: 2017-04-01 -> 2017-03-31T23:00Z, 2024-03-31 -> 2024-03-31T00:00Z, 2024-10-27 -> 2024-10-26T23:00Z |
| `published_at` = CKAN last_modified read as UTC | bronze sidecar `ckan_last_modified` "2026-10-16T06:19:42.715908" -> silver `2026-10-16 06:19:42.715908 UTC`; `published_at == available_at` on every row |
| Ten yearly April-to-March files from 2017-18 | registry resource names "Constraint Breakdown 2017-2018" to "2026-2027" (vendor catalogue) |
| Weekly update frequency | note, "Vendor metadata (snapshot extras, verbatim): Update Frequency: Weekly" |
| NESO says tags can change after the event and data is refreshed | note quotes the vendor ("can occasionally be changed post event", "would be refreshed") |
| Restatement shown in the eight rows | silver, both captures of resource `4136a8e2-...`: six dates differ (2026-09-03, 09-04, 09-14, 09-15, 09-28, 10-01); e.g. 09-28 thermal cost 28,998 -> 7,873,785, thermal volume 1,528 -> -29,709 |
| Volumes signed, sign undefined by NESO | note: vendor dictionary example `-47450`, no sign definition |
| Requests | `package_show`: `endpoints.py:49` `CKAN_ACTION_PREFIX = "/api/3/action"`, `_package_show(family.package)` with package `constraint-breakdown`; download URL from the 2026-10-16 bronze sidecar `request_url` |
| Commands `--last 24h` | `client.py` `_assert_window_admissible` refuses an ingest `end` more than 48 h stale; same pattern as the approved historic generation mix page |
| `query()` relation and filter | probed in gridflow_models: date column `date`, relation `silver_neso_data_portal_constraint_breakdown_latest` (newest complete capture per resource, view SQL read from DuckDB), `ORDER BY date`, EXCLUDE `event_time, available_at, source_run_id, dataset_version` (+ partition cols); timestamps return as Europe/London |
| Chart alt values | committed series: medians 0.23/0.26/0.29/0.41 M (Apr 2017 to Mar 2021), peaks 7.22 to 12.59 M then 53.02 M (2021-11-24), 62.07 M (2022-07-20); medians 3.01/3.63/4.32 M from Apr 2024; max of open year 35.52 M (2026-09-30); 5 values < 0, min -232,717 (2023-03-30) |
| Key note "largest of four reasons every April-to-March year" | notebook output table (thermal column largest in every row 2017 to 2026) |
| plot_alt values | silver, open year: voltage max 5,388,141 (2026-06-14), inertia max 2,936,665 (2026-07-26), largest loss 0 on all 194 dates, total max 35.68 M on 2026-09-30; thermal at least half the day's total on 159 of 194 dates ("most days") |
| 2025-04-08 absent | silver: only missing date in 2017-04-01..2026-10-11 |

## Body corrections (canonical note)

1. "Seven things", item 1: "Silver holds 3,470 rows, one per date, 2017-04-01 to 2026-10-01" is stale. Now: "At
   activation silver held 3,470 rows ...; a 2026-10-16 capture of the 2026-27 file added 194 rows, to 2026-10-11".
   Evidence: silver now 3,664 rows, 3,480 distinct dates, 11 files; the 11th is
   `constraint_breakdown_20261016_run2026-10-16T19-21-13...parquet`.
2. "The open year": resolved the `TODO: verify` that NESO updates the same resource id. Observed 2026-10-16: same id,
   `last_modified` 2026-10-16T06:19:42.715908, 194 rows to 2026-10-11, a second capture; listed the six restated
   dates with one example. Evidence: bronze `2026/10/16/raw_20261016T192113Z_4136a8e2-..._466196a8.meta.json`; silver
   comparison of the two captures.
3. Front matter `updated:` 2026-10-10 -> 2026-10-18.

Left as is: the "Measured on silver (2026-10-10)" block (dated, true at its date), including "every date unique across
the whole silver set" and "every capture_written_at is 2026-10-08", which no longer hold for raw silver but are scoped
to that date. The seat may want them re-dated.

## Not verified

- The day boundary of NESO's `date` (settlement day, UTC day or other): the page says NESO does not state it.
- The meaning of the volume sign, whether £ is nominal, and whether the four reasons are exclusive or exhaustive
  (all `TODO: verify` in the note; the page claims none of them).
- Whether the last dates (for example 11 October 2026 at £0.66 M against £18 to £23 M on the two days before) are
  incomplete or real; the caption says only that recent dates can still be restated.
- `-0.0` in the notebook table (2023-24 largest loss) is a genuine tiny negative sum (one negative-cost date), printed
  as pandas prints it.

## Open questions for the checker and seat

- Key: I used `resource_id, date, published_at` (code identity plus the capture). The historic generation mix page
  used `[timestamp_utc, published_at]`; a reviewer may prefer `[date, published_at]` because dates never repeat
  across files. `resource_id` folds at narrow widths but stays in the guide's key list.
- Window ends at 11 October 2026, the newest capture's last date. Ending at 30 September would avoid the freshest,
  most revisable days but drop the restated early-October values the eight rows show.

## Template problems (report, not worked around)

1. The chart spec cannot plot a wide table's several value columns as series (one `value`; series only from a
   `group` column). A stacked daily cost by reason, the natural chart here, is impossible without an unpivot option
   (for example `values: [col, ...]` turned into a group).
2. The y axis floor drops a whole tick step for a tiny negative: five dates down to -£232,717 make the axis run to
   -20M, so about a fifth of the plot is empty below zero (`chart_svg.nice_ticks` floors `lo` to the step). Honest,
   but wasteful; a floor that only adds a step when the negative exceeds a fraction of it would fix it.
3. `page.related[].dataset` must match `^[a-z0-9_]+/[a-z0-9_]+$`, so a package page slug with a hyphen
   (`aggregated-bsad`) cannot be named; I used the table key `neso_data_portal/aggregated_bsad`, which links through
   the redirect pointer `aggregated_bsad.html` to `aggregated-bsad.html#aggregated_bsad`.

## Defects

- **neso_data_portal / constraint_breakdown: vault note's silver counts stale after the 2026-10-16 refresh.** The
  "Measured on silver (2026-10-10)" block still says every date is unique across silver and every
  `capture_written_at` is 2026-10-08; raw silver now holds two captures of the 2026-27 file (3,664 rows, 3,480 dates,
  to 2026-10-11). Items 1 and The open year were corrected on branch `docs/neso-dp-dfs-page`; the dated block needs a
  re-measure or an explicit "as of activation" label.
- **neso_data_portal / constraint_breakdown: NESO restates published dates between uploads (data behaviour, not a
  gridflow bug).** The 2026-10-16 upload of the 2026-27 file changed six dates already in the 2026-10-03 upload
  (2026-09-03, 09-04, 09-14, 09-15, 09-28, 10-01), including a sign flip of thermal volume on 2026-09-28 (1,528 ->
  -29,709) and thermal cost 28,998 -> 7,873,785. Anything consuming this family must read the `_latest` view or
  dedup on `date` by `published_at`; a naive read of raw silver double counts 184 dates.
- **front end / chart spec: no way to chart a wide table's columns as series** (template problem 1 above).
- **front end / chart renderer: y axis floors a full step below zero for tiny negatives** (template problem 2 above).
- **front end / page fields: related-dataset pattern rejects hyphenated package slugs** (template problem 3 above).

## Revision 1 (after `constraint-breakdown-review.md`, REVISE: 1 major, 5 nits)

1. **Major, `page.facts.grain`:** now "One row per date and capture; read the `_latest` view for one per date"
   (13 words). It says why a date can appear twice and how to get one row per date.
2. **Nit, key note:** "Largest of the four by summed cost in every April-to-March year (2026 part-year). Below
   zero on five dates." (18 words).
3. **Nit, `record.fields.reducing_largest_loss_cost_gbp`:** "zero here" scoped to "zero in these rows"; to stay
   within 14 words, "actions shrinking" became "cutting".
4. **Nit, caption:** "NESO's 2025-26 file has no row for 8 April 2025"; "still" dropped to stay within 40 words.
5. **Nit, axis floor:** agreed it is a template matter. No page change, already reported as template problem 2.
6. **Nit, stale body sentences:** "at activation" added to "Downloads and captures" (line 198), the bold
   "Eligible. Silver ..." line (264), and the Cadence paragraph, which also now points to the 2026-10-16 second
   capture.

Checks: CRLF kept (0 bare LF), mirror `cmp` clean, `gridflow-build --only neso_data_portal/constraint_breakdown`
clean (the first rebuild failed on a 15-word guide line, which is fixed), detector `[]`, 0 em dashes. All four new
phrasings appear in the rendered HTML, and the hero was re-checked at 1440 and 390 with nothing clipped. Artefacts
are unchanged: no chart, sample or notebook input changed.
