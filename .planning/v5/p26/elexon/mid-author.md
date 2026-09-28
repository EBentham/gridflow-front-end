# elexon/mid: writer's report

Writer: Opus 5.5 · high, 2026-09-28. Page: `site/hifi/data-sources/elexon/mid.html` (front-end worktree `p26-elexon`).

## Status

- `gridflow-build --only elexon/mid`: green (the one warning is `fuelinst`'s, not this page's).
- `detect.mjs --json`: `[]`.
- Artefacts, all from real data:
  - `site/hifi/data/series/elexon/mid.json` (`spec_origin: vault`, 336 points);
  - `site/hifi/data/samples/elexon/mid.json` (`generated_by: gridflow-sample`, 8 rows by 13 columns);
  - `site/hifi/data/notebooks/elexon/mid.json` and `mid-5.png` (`scripts/run_notebooks.py`, 5 cells, no errors).
- No staged spec or authored override existed for `mid`; the `rm -f` was a no-op.
- Mirror `vault/elexon/mid.md` is a byte copy of the vault note (`cmp` clean). **Heads-up for the seat:** the old mirror was an LF copy of an older body, so the mirror diff is a whole-file rewrite (CRLF, plus the vintage-policy and citation sections that were already in the canonical note).
- Chart: `line`, `market_index_price` for `APXMIDP` only, settlement dates 15 to 21 September 2026, one value per half-hour (`aggregation: last`, one row per timestamp after the filter). Window `2026-09-14..2026-09-21` on `timestamp_utc`, with the `settlement_date` filter because the settlement day starts at 23:00 UTC in BST.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Two providers, `APXMIDP` and `N2EXMIDP` (`what_it_is`) | Vendor param doc in the note: `dataProviders` "If no data provider is selected both will be displayed". Silver, all years: only those two codes, no null `data_provider_id` (Polars group-by over all 1,842 files). |
| Price is the volume-weighted average of qualifying short-term trades (half-hour to four-hour products); volume is their sum; the day-ahead auction has no weight; below 25 MWh both default to zero (`what_it_is`, `record.fields`) | MIDS citations in the note's Modelling notes (#05, #03, CP1359 change log). |
| Grain: one row per settlement period and provider; key `(settlement_date, settlement_period, data_provider_id)` (`facts.grain`, `record.key`) | `gridflow/silver/elexon/mid.py:122-125`, `unique(subset=[settlement_date, settlement_period, data_provider_id], keep="last")`. 0 duplicate keys in silver. |
| `timestamp_utc` is the start of the half-hour, computed from settlement date and period | `mid.py:111-120` calls `utils/time.py:28-42` `settlement_period_to_utc` (SP1 = 00:00 UK local). |
| Period 1 to 48; 46 or 50 on clock-change days | `schemas/elexon.py:193` (`ge=1, le=50`); `utils/time.py:28-42`. |
| `data_provider_id` "as sent (`dataProvider`)" | `mid.py:83-84` renames `dataProvider` (current) and `dataProviderId` (legacy). |
| x label "each starts at 23:00 UTC" | BST in September; series first point is `2026-09-14T23:00:00Z` for settlement date 15. |
| Caption: `N2EXMIDP` sends price 0 and volume 0 in every period shown | Polars over settlement dates 15 to 21 Sep, `N2EXMIDP`: price == 0 in 336/336 rows, volume == 0 in 336/336 rows. Scoped to "every period shown". |
| Alt numbers | Committed series: min -19.03 at `2026-09-20T15:00Z`, max 212.39 (`2026-09-15T17:30Z`). Per settlement date: 15th 46.33 to 212.39; 16th 117.77 to 206.12; 17th min -2.25; 18th min -0.5; 19th min -3.26 (`2026-09-18T23:00Z`, SP1 of the 19th); 20th max 197.83 at 20:00Z; 21st 134.98 to 207.07. |
| Request URL | `connectors/elexon/endpoints.py:80-86` (`/datasets/MID`, `from`/`to`), `endpoints.py:267-277` (`%Y-%m-%dT%H:%M:%SZ`), `endpoints.py:312-313` (`page`), `client.py:93-99` (24-hour chunks). It matches bronze sidecar `bronze/elexon/mid/2026/09/20/raw_…meta.json` `request_params {from: 2026-09-20T00:00:00Z, to: 2026-09-21T00:00:00Z, page: 1}`. |
| "windows of period start time" (`raw_feed.note`) | Vendor param doc in the note: `from`/`to` = "start time or settlement date". Bronze partition 20 holds `startTime` 20T23:00Z to 21T00:00Z rows (settlement date 21, SP1 to 3), so filtering is by start time. |
| "reading the day before too" | `mid.py:28` `PARTITION_SOURCE_OFFSETS = (-1, 0)`. |
| Ingest `--start 2026-09-14 --end 2026-09-22`, end exclusive | `client.py:93-99` `while current < end`; bronze partitions 14 to 21 are needed for silver days 15 to 21 under offsets (-1, 0). |
| Transform `--start 2026-09-15 --end 2026-09-21` (inclusive) | Brief and rubric semantics; matches the fuelhh worked example. |
| Notebook lead: relation `silver_elexon_mid`, both providers, `settlement_date` inclusive both ends, lineage dropped, ordered by `settlement_date` only | gridflow_models `_relation_name_for_dataset('mid') == 'silver_elexon_mid'` (run); `research/handles/source.py:401-451` (`query`, `ORDER BY {date_col}`, EXCLUDE of `_BITEMPORAL_EXCLUDE` = event_time, available_at, vintage_policy, source_run_id, dataset_version); gridflow `silver/schema_manifest.py:131` date column `settlement_date`. |
| Eight rows | `samples/elexon/mid.json`: 2026-09-20 SP32 to 35 for both providers. APXMIDP -12.14, -19.03, 38.19, 103.7; N2EXMIDP 0.0 and 0.0 throughout. |
| `plot_alt` | Read from the rendered `mid-5.png`, cross-checked against the series. |

## Note-body corrections (vault note, smallest span)

1. **Dedup key**: was "_inline in transformer_", now `(settlement_date, settlement_period, data_provider_id)` with the citation `mid.py:122-125`.
2. **Point-in-time field**: was "`ingested_at` (no native PIT field)", now "none from the vendor; `available_at` follows the vintage policy below (`mid.py:29-41`)".
3. **`ingested_at` row**: was "Time ingested into bronze", now the silver transform time (`mid.py:127-131`, `datetime.now(UTC)`).
4. **Silver sample**: `timestamp_utc` for 2026-05-06 SP9 was `04:00Z`, now `03:00Z` (BST: SP1 = 23:00Z the day before; bronze sample `startTime` 03:00Z). The placeholders `"..."` for `data_provider_id` and `market_index_price` are now `APXMIDP` and `105.43`, taken from the note's own bronze sample.
5. **Gotcha, providers**: was "(APXMIDP, NORDPOOLMIDP). Silver dedup does not currently include `data_provider_id`". Now: two providers, `APXMIDP` and `N2EXMIDP`, and dedup does include the provider (`mid.py:122-125`). The Modelling-notes sentence that pointed at the old gotcha now says it was corrected.
6. **Gotcha, partition grain**: "On-disk MID silver has not been rebuilt yet … can still see doubled rows" was stale. It now says the silver was rebuilt 2026-09-07, and I re-checked 0 duplicate keys over all 1,842 silver files on 2026-09-28. This agrees with the note's own Vintage policy section.

Front matter: the `page:` block was added. `last_verified` was left at 2026-09-07; the seat can decide whether to bump it.

## Not verified

- **Which MIDS version applies in 2026.** The MIDS facts come from citations to v9.0 and the 2025 review. The note itself carries `TODO: the MIDS version in force for Aug–Sep 2026 is not archived`.
- **The APXMIDP to EPEX mapping.** It is not stated on the page, deliberately.
- **Overview sentence.** "used by the BSC to derive the Power Exchange Reference Price" was left alone, not checked, and not used on the page.
- **Dark mode.** The site has no dark theme: no `prefers-color-scheme` or `data-theme` in `theme.css`, `tokens.css`, `dataset.css` or `site.js`. Light and dark render the same.

## Screenshots

Checked at 1440, 1024 and 768 (headless Chrome, full page) and at a true 390. Headless Chrome on Windows won't make a 390-wide window and crops the right edge, so for 390 I loaded the page in a 390-px iframe and confirmed `scrollWidth == 390` with no element outside the viewport. I also checked the open states: frame unfolded (`#fx` checked) and notebook opened. Findings:

- The hero scenery (turbines, labels), the chart, the x label, the key, the raw wells, the frame and guide, the notebook and the related list are fully visible at every width.
- The unfolded frame and the notebook `df` scroll inside their own boxes, which is the intended behaviour.
- The 768 frame folds `data_provider_id` and the price behind `…`. That is the 1280-px budget rule, not a defect.

Note for the seat: the shared Browser pane tab switched to another writer's page (`freq`, port 9714) between two of my calls. One of my scripts clicked the frame-fold checkbox and the notebook button on their page, which is UI state only, with no files changed. I stopped using the pane after that. Other writers may want to avoid the pane too.

## Template and data-file problems (not worked around)

1. **Notebook `df` header is shifted one column (all pages).** `src/gridflow_front_end/build.py:1225-1229` writes `<tr><th></th>` and then a `<th>` for every entry of `out["columns"]`. `run_notebooks.py` already puts `""` (the index name) first in `columns`, so the header has 7 cells over 6-cell rows. Every value sits one column left of its header, and the last header (`market_index_volume` here) has no values. The main repo's built `system_prices.html` and `fuelhh.html` show the same doubled `<th></th><th></th>`. Fix: drop the leading literal `<th></th>`, or skip `columns[0]` when it is `""`.
2. **Landing blurb contradicts the vendor.** `site/hifi/data/elexon.json` landing `start` calls `mid` "market index, the GB day-ahead benchmark". The MIDS citations in the note say the day-ahead auction carries weight 0, so MID is a short-horizon index. Suggested wording: "market index price and volume, per provider".

## Open questions for the checker

- `notebook.needs` says "15 to 21 September 2026", but the ingest command runs 14 to 22. This follows the fuelhh and system_prices worked examples, where `needs` is the silver window.
- `APXMIDP` only in the chart: the reason is in the caption, and the frame shows both providers side by side.

## Revision 1 (2026-09-28, after `mid-review.md`: REVISE, 1 major, 1 nit)

- **Major (x axis bands).** Fixed on the seat's side: the renderer now ticks on UK midnight for settlement-date axes. I
  left `x_label` unchanged, as instructed. In the rebuilt SVG the axis runs from `x0 = 74` (14 Sep 23:00Z) and the
  ticks are at 74, 189.7, 305.4 … 884, one settlement day (115.7 px) apart. Each day name is centred at `x0 + 12 h`
  of its band ("15 Sep" at 131.9), so the bands are settlement dates 15 to 21, and "each starts at 23:00 UTC" is
  now true. Checked in a 1440 headless render: 7 bands, nothing clipped.
- **Alt and caption re-checked against the new bands.** No change needed: both already describe settlement dates.
  - The lowest of the 17th to 19th is -3.26, which is settlement date 19, period 1 (18 Sep 23:00Z). It now sits
    inside the "19 Sep" band.
  - -19.03 at 15:00 UTC on the 20th and 197.83 that evening are both in the "20 Sep" band.
  - The ranges for the 15th, 16th and 21st are by settlement date.
  - `plot_alt` describes the notebook's matplotlib plot, which is on a UTC axis, so it is unaffected.
- **Nit (`page.what_it_is`).** Rewritten to give the products and the time limit in full: "the volume-weighted
  average of half-hour, one-, two- and four-hour products traded within eight hours of the submission deadline, and
  the volume their sum. Day-ahead auction trades carry no weight; below 25 MWh, both default to zero." It is 59
  words, within the budget of 60. I used "submission deadline" rather than "gate closure" because that is the
  source's own term (source 05, line 573).
- **Rebuild and checks.** `gridflow-build --only elexon/mid` is green, `detect.mjs` returns `[]`, and the mirror
  re-copy matches (`cmp` clean). None of the artefacts needed regenerating: the chart spec, the sample rows and the
  notebook cells are unchanged.
