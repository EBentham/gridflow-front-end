# Writer report: `day-ahead-power-exchange-prices-nordpool` (table `nordpool_da_prices`)

Writer, Trading batch, 2026-10-23. Port 9861 (server PID 11052, started with the batch method, stopped by that PID).

**Status:** full page written, build `--only neso_data_portal/nordpool_da_prices` clean, detector `[]`, 0 em dashes.
No hold recommended: the rows support an honest page as long as it does not compose a delivery instant, and it doesn't.

## Files (mine only)

- Canonical note: `C:\gridflow-wt\vault-neso-trd\30-vendors\neso-data-portal\datasets\day-ahead-power-exchange-prices-nordpool.md`
  (`page:` block plus two body corrections; CRLF kept)
- Mirror: `C:\gridflow-wt\fe-neso-trd\vault\neso_data_portal\day-ahead-power-exchange-prices-nordpool.md` (`cmp` identical)
- Artefacts: `site\hifi\data\series\neso_data_portal\nordpool_da_prices.json`,
  `samples\neso_data_portal\nordpool_da_prices.json`, `notebooks\neso_data_portal\nordpool_da_prices.json` and `-5.png`
- Built page: `site\hifi\data-sources\neso_data_portal\day-ahead-power-exchange-prices-nordpool.html`
- There was no staged chart spec or authored override for this dataset to retire.

## The four questions

**1. What one row is.** One hourly price for one delivery date and one one-hour period. There is no area column and no
currency column. The price is in £/MWh. NESO's package text: "These are published in £/MWh". The dictionary titles
the column "Price (GBP)" and describes it as the auction price for the delivery period. The publisher is Nord Pool,
republished by NESO. In NESO's words the resource "returns the Day-Ahead price data published by Nord Pool each day for
GB", and the package says the prices are "available from exchanges such as Nord Pool". The resource is named "N2EX GB
Day-Ahead Price".

**2. The clock.**
- NESO's dictionary calls `Date` the "Delivery Date". It titles `Delivery Period` "Delivery Period (GMT)", described as
  "Day ahead Hourly Delivery periods in HH:MM - HH:MM format".
- gridflow keeps both columns: `date` is parsed as a Date and `delivery_period` stays a string. The temporal recipe is
  `none`, so `timestamp_utc` = `event_time` = `available_at` = `capture_written_at`, which is the capture time.
  `published_at` is null.
- The page says exactly that and builds no delivery instant. The chart is per date. The frame shows the raw labels. The
  notebook plots the mean price by GMT hour label.
- The rows support reading `date` as the GMT date of the labelled hour (report only, not on the page):
  - Under the mapping date plus GMT start, every step is exactly one hour (44,471 steps in the 16 Oct capture).
  - Every complete date has 24 labels, including all ten clock-change dates from 2021-10-31 to 2026-03-29.
  - Both capture edges fall on a UK-day boundary in summer time: the file starts at 2021-09-20 `22:00 - 23:00` and the
    captures end at `21:00 - 22:00` on 2026-10-08 and 2026-10-17. Under date plus GMT start, both end at 22:00 UTC.
  - The mean price by label for 2023 onwards puts the morning ramp at label 06 in Dec to Feb but at label 05 in Jun to
    Aug. That is one hour earlier in summer, as GMT labels would show.
- The page itself states only NESO's GMT label and what the eight rows show.
- `query()` filters `timestamp_utc` (`_DATE_COLUMN_BY_DATASET['nordpool_da_prices'] == 'timestamp_utc'`, relation
  `silver_neso_data_portal_nordpool_da_prices_latest`), which is the capture time here. The notebook therefore uses
  `data.sql()` on `_latest` and converts the capture time with `AT TIME ZONE 'UTC'`.

**3. Captures, truncation and repeats.**

| Capture (`capture_written_at`) | Silver rows | Bronze CSV lines minus header | Dates | Complete 24-hour dates | Partial edges |
|---|---:|---:|---:|---:|---|
| 2026-10-08 11:14:21Z | 44,256 | 44,256 | 1,845 | 1,843 | 2021-09-20 (2 rows), 2026-10-08 (22) |
| 2026-10-16 20:42:05Z | 44,472 | 44,472 | 1,854 | 1,852 | 2021-09-20 (2), 2026-10-17 (22) |

- No truncation. Each silver count equals its bronze body, and NESO's own `datastore_search` total on 2026-10-08 13:19Z
  was 44,256 (field-info snapshot).
- The 16 Oct recapture is a strict superset. All 44,256 hours of the first capture are present with identical prices
  (0 differ), plus 216 later hours through `2026-10-17` `21:00 - 22:00`.
- `(date, delivery_period)` is unique within each capture. There are no nulls, every label is `HH:00 - HH:00`, and
  every label spans one hour.
- The chart and frame both set `dedup: {on: [date, delivery_period], order_by: capture_written_at}` as a guard.
  Distil's provenance reports `duplicates_dropped: 44254` (the first capture's rows inside the window) and
  `rows_used: 44448` (1,852 × 24).

**4. Chart.**
- Line chart of the daily mean of the 24 hourly prices labelled with each date, in £/MWh, from 21 September 2021 to
  16 October 2026 (1,852 points). These are the complete dates in the newest capture.
- The caption says it is a plain mean over the 24 GMT-labelled hours, from the file captured on 16 October 2026.
- `y_min: -25` lifts the 0.39 low off the axis.
- Values (from the committed series):
  - Peak 574.82 on 2022-08-26, then 570.94 on 2022-12-12.
  - All 68 days above 300 fall between 2021-10-15 and 2022-12-16.
  - Lowest 0.39 on 2025-10-04; overall median 92.37.
  - Yearly medians 2023 to 2026: 90.34, 73.08, 81.67 and 104.56 (2026 runs to 16 Oct).

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Nord Pool's GB day-ahead auction price, republished by NESO (`summary`, `what_it_is`) | Catalogue snapshot `20261006T195819Z`: resource description "This data file returns the Day-Ahead price data published by Nord Pool each day for GB"; package notes. Field-info `20261008T114228Z/nordpool_da_prices.json`: Price "Auction price for the delivery period" |
| £/MWh | Package notes "These are published in £/MWh"; dictionary unit "GBP" |
| Delivery date; one-hour GMT period (`facts.grain`, `record.fields`) | Field-info: `Date` "Delivery Date in YYYY-MM-DD format"; `Delivery Period` title "Delivery Period (GMT)", "Day ahead Hourly Delivery periods" |
| Key `date, delivery_period` | Registry `day-ahead-power-exchange-prices-nordpool.json` `entity_key`; unique in both captures (Polars) |
| "Daily in NESO's catalogue" | Snapshot extras `Update frequency: Daily` |
| gridflow builds no delivery time; `timestamp_utc` is capture time | Registry `temporal: {kind: none}`; silver: `timestamp_utc` equals `capture_written_at` on every row of both captures |
| `published_at` null | `silver/neso_data_portal/completion.py:239-254` (set only under `ckan_last_modified`; datastore requires `capture_fallback`, `:240`); registry `vintage: capture_fallback`; silver null count 88,728 of 88,728 |
| Requests | `endpoints.py:51` `DATASTORE_DUMP_PREFIX`, `client.py:1388` dump built from the registry id; sidecar `request_url` `https://api.neso.energy/datastore/dump/4f27eea5-...`; `package_show` per `client.py:971-981` |
| "kept only if its body changed" | `client.py` `_dump_member`: `body_sha256 == basis.body_sha256` returns `unchanged` (daily family, so no frozen stamp) |
| Commands `--last 24h` | Same form as the approved datastore-dump pages (`aggregated-bsad`, `bsad-forward-contracts`) |
| Chart numbers | Committed series `nordpool_da_prices.json` (`spec_origin: vault`), values listed above |
| Frame: 26 Oct 2025, five negatives and one zero | Sample file rows: 0.0, -0.49, -0.58, -1.86, -2.45, -1.76, 0.93, 4.79 |
| Notebook outputs | 24 labels on 1,852 dates, 2 on 1, 22 on 1; plot means 103 (06:00), 78 (12:00, 13:00), 130 (18:00), 91 (23:00), recomputed in Polars as 102.6, 77.6, 77.8, 129.7, 91.2 |
| `query()` date column | `gridflow_models` `_get_method_registry._DATE_COLUMN_BY_DATASET`: `timestamp_utc` |

## Body corrections (canonical note)

1. **Files, SILVER:** after "The datastore response was a single page." I added the second capture. That is
   `raw_20261016T204205Z_..._13ef1d85.csv`: 1,575,939 bytes and 44,472 rows, with `written_at` 2026-10-16T20:42:05Z.
   It holds the first capture's hours with identical prices plus 216 more, and its sidecar still has CKAN
   `last_modified` 2026-09-21. Evidence: bronze sidecar and the Polars comparison above.
2. **Cadence:** "Only one capture exists to date." became "Two captures exist (2026-10-08 and 2026-10-16; see Files)."

I made no other body edits. The rest of the body (GMT labels, 24 labels per date, value range -54.17 to 2,000.05, 591
negatives, 63 zeros, two `-1.000000` rows) still holds on the 16 Oct capture.

## Screenshots

- Taken at 1440, 1024 and 768, and at 390 in a 390 px iframe. They are in
  `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\nordpool-writer\shots\`
  (`c-*.png` are the crops).
- Nothing is clipped or overlapping: hero, turbines, the facts table (the package slug wraps cleanly at 390), the chart
  and its key, the raw feed wells, the folded frame and guide, the notebook panel and the related links.
- Dark: the site has no dark theme (no `prefers-color-scheme` or `data-theme` in `theme.css`, `tokens.css` or
  `site.js`), so light is the only rendering. Chrome's dark flag produced the same page.
- I did not screenshot the unfolded frame or the open notebook drawer. They are interactive.

## Unverified

- Whether NESO or Nord Pool ever restates a past hour's price. The two captures agree on every shared hour, but that
  proves nothing about the vendor's policy. This is on the page only as "newest capture" wording.
- When NESO appends each day's prices: CKAN `last_modified` has not moved since 2026-09-21.
- That the two `-1.000000` prices are genuine auction results (the vault TODO still stands). They are not on the page.
- The reading of `date` as the GMT date of the hour rests on measurement plus NESO's GMT period label. NESO's dictionary
  says only "Delivery Date".

## Open questions

- The ledger caveat "delivery instant not composed" stands. If the seat wants an hourly chart, gridflow first needs the
  date plus interval-label temporal recipe (rulings 572 and 588).
- Related: no interconnector page is in the page set, so I used `elexon/mid`, `elexon/system_prices` and
  `entsoe/day_ahead_prices`. The held `interconnector-requirement-and-auction-summary-data` could be a fourth link if
  the seat wants one.

## Template problems

None found.

## Defects

- **gridflow: no temporal recipe for a date plus hourly interval label.** For `neso_data_portal/nordpool_da_prices`,
  `timestamp_utc` is the capture time because no recipe composes `date` + `delivery_period` (GMT `HH:MM - HH:MM`) into
  an instant (registry `temporal: none`; rulings 572 and 588).
  - Consequence: `data.neso_data_portal.query("nordpool_da_prices", start, end)` filters and orders by the capture
    time, so a delivery-date window returns everything or nothing. This is the same class as remediation 20at.
  - Workaround on the page: `data.sql` on `_latest`.
  - Proposed fix: a `date_interval_utc(date, interval_label)` recipe, with the registry record version bumped.
- **NESO metadata: CKAN `last_modified` is stale on a growing file.** Resource `4f27eea5-7038-4f73-9740-e3e4ad47c26a`
  still reports `last_modified` 2026-09-21T12:38:33 on the 2026-10-16 capture, whose body grew by 216 hours. Its
  `metadata_modified` was 2026-10-16T11:30:13. gridflow already ignores this field for dump families (ADR-035), so this
  is for the vendor remediation page only.
- **Vault (fixed in this branch):** the Nord Pool note said only one capture existed; a second capture on 2026-10-16
  was transformed to silver.
