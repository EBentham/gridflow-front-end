# Constraint breakdown: checker's review

Page `neso_data_portal/constraint-breakdown` (table `constraint_breakdown`), reviewed 2026-10-18 against the rubric,
gridflow code, local silver (read only), the bronze sidecar and the vendor catalogue and field-info snapshots.

**Verdict: REVISE** (one major, five nits, no blockers). The facts, chart, frame and notebook all reproduce. The one
major is a truncated sentence in the hero's Grain line, which is also the line that tells the reader how to get one
value per date.

## What was checked and held

- Build: `gridflow-build --only neso_data_portal/constraint_breakdown` succeeds. Detector `[]`. Mirror byte-equal to
  the canonical note (`cmp` clean). Em dashes, arrows, middle dots on the page: 0. Rubric section 3 grep on the
  `page:` block (`locally`, `held`, `our `, `since 20`, `rows`, `live`, `now`, `yet`, `soon`): nothing hits.
- Silver: 3,664 rows, 3,480 distinct dates, 11 files. `(date, published_at)` and `(resource_id, date, published_at)`
  are unique over all rows. Only resource `4136a8e2-...` has two captures (184 rows at 2026-10-03 11:00:54.622473 UTC,
  194 rows at 2026-10-16 06:19:42.715908 UTC). `published_at == available_at` on every row.
- Restatement reproduced: six dates differ between the two captures (2026-09-03, 09-04, 09-14, 09-15, 09-28, 10-01).
  2026-09-28 thermal cost 28,998 then 7,873,785 and thermal volume +1,528 then -29,709, exactly as the note says. Voltage
  cost also changed on that date. The 184 older dates all reappear in the newer capture, so a raw read double counts 184
  dates.
- Key: the registry and `generic.py` entity key is `resource_id, date` (uniqueness enforced inside one capture,
  `casting.py:582`). The page's `resource_id, date, published_at` adds the capture axis and says so ("code's entity
  key" in the `resource_id` guide line). Defensible and consistent with the historic generation mix page.
- `_latest` view: `data.neso_data_portal.query("constraint_breakdown", "2017-04-01", "2026-10-11")` returns 3,480 rows,
  3,480 unique dates, newest capture for the restated dates (2026-09-28 reads 7,873,785 and -29,709). The chart's
  `dedup on date, order_by published_at, last` gives the identical values: 3,480 of 3,480 points equal the view's
  `thermal_constraints_cost_gbp`, zero mismatches, no extra or missing date. The lead's "both ends included" holds
  (2026-10-11 is returned for end "2026-10-11").
- Chart spot checks, series against silver (all equal): 2017-04-01 126,043; 2019-12-25 33,405; 2021-11-24 53,018,734;
  2022-07-20 62,073,965; 2023-03-30 -232,717; 2024-06-15 3,958,613; 2026-09-28 7,873,785; 2026-09-30 35,516,446;
  2026-10-11 663,813. The only missing date in 2017-04-01 to 2026-10-11 is 2025-04-08. Five values below zero (2023-03-03,
  2023-03-12, 2023-03-30, 2023-06-02, 2024-12-09), minimum -232,717.
- Alt text: April-year medians 0.23, 0.26, 0.29, 0.41 M (so "£0.2 to £0.4 million" holds) and peaks 7.22, 11.61, 9.49,
  12.59 M ("£7 to £13 million"); spikes 53.0 M (24 Nov 2021) and 62.1 M (20 Jul 2022); medians 3.01, 3.63, 4.32 M from
  April 2024; highest day since is 35.5 M on 30 Sep 2026. All true.
- Chart is labelled thermal only (title, caption, key label, axis note) and is a fair single-series choice: thermal is
  the largest of the four by yearly summed cost in all ten April-to-March years (notebook table, reproduced).
- Four reasons: every cost and volume line in the guide matches NESO's field dictionary (field-info snapshot
  `20261008T114228Z/constraint_breakdown.json`): thermal "flow ... exceeds the capacity of the circuits connecting the
  two regions", voltage "reactive power ... Voltage Control", inertia "BM Actions to increase synchronous generation",
  largest loss with example volume -47450. Units £ and MWh are the dictionary's. Sign undefined by NESO: true (no sign
  statement in the dictionary or notes).
- Day convention: the vendor text says only "The date of the costs/volumes" (field-info `Date`); the package notes say
  nothing about a boundary; gridflow's FACTS lists the window as an open TODO. The page's "day boundary is not stated"
  is true. The code does pick a convention (`casting.py:619-624`, `settlement_period_to_utc(date, 1)`), and the page
  labels it "gridflow's anchor", never as NESO's. Frame values agree (2026-09-04 maps to 2026-09-03 23:00 UTC).
- Vendor quotes: "can occasionally be changed post event ... would be refreshed" is verbatim in the catalogue notes
  (`catalog-snapshot.json`). Package title "Constraint Breakdown Costs and Volume" and `Update Frequency: Weekly` match.
- Raw feed: the second request URL matches the 2026-10-16 bronze sidecar `request_url`. The "downloaded whole unless
  `last_modified` unchanged" description matches `client.py` `iter_members` (1752-1768). `--last 24h` pattern is the
  one already on the historic generation mix page.
- Notebook JSON written by `scripts/run_notebooks.py`, read-only cells, no error outputs. The plot_alt values
  reproduce: voltage max 5,388,141 on 2026-06-14, inertia max 2,936,665 on 2026-07-26, largest loss zero on all 194
  dates, total max 35.68 M on 2026-09-30, thermal at least half of the day's total on 159 of 194 dates.
- Screenshots at 1440, 1024, 768 and a true 390 px iframe: hero scenery, chart, folded and unfolded frame (opened
  through the `#fx` checkbox), guide, opened notebook with table and plot, related list. Nothing clipped or overlapping.
  The site has no dark scheme, so dark equals light.
- Related notes are 8 to 11 words and resolve. Body edits are small, dated and cite evidence.

## Findings

1. **major** `page.facts.grain` (hero, "Grain" row): "One row per date and capture; the latest view keeps the newest
   file's" stops mid-sentence. It is the line that tells the reader why a date can appear twice and how to get one
   row per date, so a cut-off clause matters here. Nothing on the page says in plain words that a read of silver can
   return the same date twice and that the `_latest` view (what the notebook queries) returns one row per date.
   Evidence: rendered page at every width reads "...keeps the newest file's"; silver has 184 dates twice (only the
   six restated ones differ). Fix: finish it, for example "One row per date and capture; the `_latest` view keeps the
   newest capture of each yearly file", and optionally add "read it for one value per date" to `raw_feed.note` or
   `what_it_is`. The notebook lead and chart caption already describe the view correctly, so no overclaim exists
   today.

2. **nit** `page.chart_view.key[0].note` and `page.notebook`: "The largest of the four reasons in every April-to-March
   year" is true on summed cost, but the note does not say "by summed cost", and the 2026 row of the notebook table is
   a part year (1 April to 11 October). Evidence: notebook table, thermal 1,449.0 M for 2026 against 1,956.0 M for
   2025. Suggest "by summed cost in every April-to-March year, 2026 part-year".

3. **nit** `page.record.fields.reducing_largest_loss_cost_gbp`: "zero here" has no clear scope. It is zero in the
   eight rows and across the open year (plot_alt says so), but the guide line reads like a property of the column.
   Suggest "zero in these rows" or drop the clause (the plot_alt already carries it).

4. **nit** `page.chart_view.caption`: "NESO's file has no 8 April 2025" is a gap seen in the captured 2025-26 file
   (364 body rows, bronze and silver agree). It is a vendor-file fact, so it is allowed, but it is only as of the
   capture (that file's `last_modified` is 2026-04-07 and it has not been re-captured). Optional: "NESO's 2025-26 file
   has no row for 8 April 2025." Not a rubric breach.

5. **nit** Chart axis (template, seat matter, not the writer's): the five negative values (largest -232,717, 0.4% of the
   62 M peak) pull the axis floor to -20 M, so the lowest 20% of the plot is empty, and the top is 80 M for a 62 M
   peak. The picture is honest but wasteful, as the writer reported. No page change needed.

6. **nit** Canonical note body, stale unscoped sentences the writer left after the 2026-10-16 capture (not on the page):
   line 198 "Every resource was captured once, on 2026-10-08", line 264 bold "Eligible. Silver: 3,470 rows, 18
   columns" (the "Measured on silver (2026-10-10)" table beneath it is dated and fine), lines 414-415 "Gridflow
   captured every resource once, on 2026-10-08". Resource `4136a8e2-...` now has two captures, so these contradict the
   corrected "open year" paragraph. Evidence: silver `published_at` count per resource, one resource at 2. Suggest
   adding "at activation" to each, or re-measuring.

## Seat matters, not findings

Single chart column per table, hyphenated slugs in `related`, and the axis floor are template limits the writer
reported correctly. The chosen series (daily thermal cost) is a fair single-series choice and is labelled as thermal
only.
