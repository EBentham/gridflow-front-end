# Capacity Market Register: writer's report (round 1)

Page `capacity-market-register`, lead `capacity_market_auction_static`, eight members, none held (ledger row: all 8
eligible, held none). Front-end worktree `C:\gridflow-wt\fe-neso-emr`, vault worktree `C:\gridflow-wt\vault-neso-emr`.

**Status:** `gridflow-build --only neso_data_portal/capacity_market_auction_static` clean; detector `[]`; em dashes 0;
mirror `cmp` identical; note still CRLF. The manifest's lead and member list are right.

Files: the canonical note (page block + body fixes), its mirror, and
`site/hifi/data/{series,samples}/neso_data_portal/capacity_market_auction_static.json`,
`site/hifi/data/notebooks/neso_data_portal/capacity_market_auction_static.json` and `-5.png`. No staged spec or
authored override existed.

## The chart, and how it was reproduced

Bar chart from the lead table: `clearing_price_gbp_per_kw_per_year` per auction, one bar per auction, 24 bars.

- Filter `not_null` on the price: a bar draws null as 0 (`chart_svg._bars`: `float(v or 0)`), so the three null
  auctions (2022-23 T-4, 2027-28 T-1, 2030-31 T-4) are dropped, and the caption says so.
- `dedup` on `auction_name`, ordered by `published_at`. The lead has one capture, so it is a guard.
- `group_map` shortens NESO's names to "2016-17 TR" style. `sort: label` gives delivery-year order. `aggregation: last`
  works on one row per auction.
- Unit `£ per kW per year`. That is NESO's column heading ("Clearing Price_GBP per kW per year"). The dictionary
  `unit` field says only `£`, and its comment says `£kW/year`.
- No time axis. Capture time is never used.

**Reproduce.** `pl.scan_parquet(silver/neso_data_portal/capacity_market_auction_static/**)`, select `auction_name` and
`clearing_price_gbp_per_kw_per_year`, then drop nulls. That gives 24 rows, and they equal the committed series exactly:
- highest: 75.0 (2022-23 T-1), 65.0 (2027-28 T-4), 63.0 (2026-27 T-4)
- lowest: 0.77 (2019-20 T-1), 1.0 (2020-21 T-1)
- T-4 range: 8.4 (2021-22) to 65.0
- 2029-30 T-4: 27.1

Provenance: rows_read 27, rows_used 24, duplicates 0, `spec_origin: vault`.

## The captures (every one checked, Polars lazy)

| Table | Captures (written; CKAN `last_modified`) | Rows | Header | Repeats |
|---|---|---|---|---|
| auction_static (lead) | 2026-10-08; 2026-09-09 | 27 | one epoch | single capture |
| auction_cost | 2026-10-08; 2026-09-09 | 192 | one epoch | single |
| de_rating_factors | 2026-10-08; 2026-09-09 | 890 | one epoch | single |
| unit_cmu | 2026-10-08 (10-07); 2026-10-16 (10-14) | 18,200 / 18,200 | same | 18,185 rows identical across both |
| unit_cmu_history | 2026-10-08 (10-07); 2026-10-16 (10-14) | 72,166 / 72,282 | same | all 72,166 recur |
| components | 2026-10-08 (10-07); 2026-10-16 (10-14) | 29,849 / 29,849 | same | 29,803 identical |
| component_history | 2026-10-08 (10-07); 2026-10-16 (10-14) | 7,460 / 7,488 | same | all 7,460 recur |
| component_history_pre | 2026-10-08; 2026-07-15 | 1,918,503 | one epoch | single; read lazily, columns selected |

The auction-level files were not fetched again on 16 October because the connector skips an upload whose live
`last_modified` equals its newest capture's (`connectors/neso_data_portal/client.py` ~1752-1766). The chart and frame
read only the lead, so `dedup` is a guard there. The notebook reads `_latest` views (`whole_capture`), so it sees no
repeats.

## What one row is in each table

- **auction_static (lead):** one auction: clearing price, target MW, awarded MW, base period, termination-fee rates 1
  to 9 and penalty caps as text. Entity key `auction_name`.
- **auction_cost:** one auction and delivery year: MW awarded and forecast cost in £. Key (`auction_name`,
  `delivery_year`). Checked on all 192 rows:
  - `forecast_cost_gbp` = `capacity_awarded` × clearing price × 1000;
  - each auction's first-delivery-year MW equals the lead's `total_volume_of_agreements_awarded`.
- **de_rating_factors:** one factor per auction and generating technology class.
- **unit_cmu:** one application per auction. Key (`auction_name`, `application_id`). It holds
  `secondary_trading_contact_telephone` and `secondary_trading_contact_email`, plus applicant, agent and
  security-interest names.
- **unit_cmu_history:** one changed CMU attribute (`previous`, `latest`) per change type and change date.
- **components:** one auction, application and component; small components are aggregated from 22 July 2026. It
  holds `location_and_post_code`.
- **component_history / _pre:** one changed component attribute, after and before the aggregation. The pre file
  logs "Location and Post Code" changes (570,933 rows).

## Personal data (hard rule 1)

- The frame, guide and chart read only the lead, which has no contact, name or postcode column.
- The notebook selects only these columns:
  - static: auction name, price, target, awarded, base period;
  - CMU: `primary_fuel_type`, `COUNT(*)`, `SUM(auction_acquired_capacity_obligation)`;
  - cost: auction name, delivery year, MW.
- A grep of the built page and all three artefacts finds no `contact`, `email`, `telephone`, `applicant`,
  `post_code` or `@`, and no phone-number pattern.
- The page says contact columns exist and are never shown: `what_it_is`, plus the unit_cmu and unit_cmu_history
  `differs` lines.

## Notebook (`data.sql`; `query()` filters capture time on a temporal-`none` table)

1. The T-4 auctions from the static `_latest` view: 13 rows.
2. Agreements awarded in the 2029-30 T-4, by `primary_fuel_type`, with a total row. Gas leads with 23,476.917 MW from
   175 units. The total, 40,108.608 MW from 691 units, equals the lead's awarded volume.
3. Stacked bar plot of `capacity_awarded` per delivery year by auction type, from the cost `_latest` view. Years
   2017/2018 to 2029/2030 hold 54,746 to 62,325 MW. Later years hold only agreements from earlier auctions: 23,754 MW
   in 2030/2031 down to 1,167 MW in 2043/2044. `plot_alt` was read off the output.

## Body corrections (canonical note, smallest spans)

1. "One capture so far" was out of date. It is now **Captures**: the four weekly families have a second capture
   (2026-10-16, `last_modified` 2026-10-14) with the same header, the row counts above, and history rows that recur.
   Evidence: silver files and sidecars `bronze/.../2026/10/16/*.meta.json`.
2. Stale code citations:
   - `casting.py:437` is now `casting.py:605` (temporal `none`, `timestamp_utc` = `capture_written_at`);
   - `casting.py:453` is now `casting.py:619` (`date_sp1`).
3. Base period: the dictionary example is an interval string, but the captured values read `Winter 2012/2013` to
   `Winter 2024/2025` (silver, notebook output).
4. CMU History: a new **Contact values** paragraph. Rows whose `attribute` is any of four spellings carry emails and
   telephone numbers in `previous`/`latest`:
   - `Secondary Trading Contact - Email` (6,216 rows) and `Secondary Trading Contact_Email` (1,438);
   - `Secondary Trading Contact - Telephone` (5,366) and `Secondary Trading Contact_Telephone` (366).

   The paragraph also notes that attributes come in two spellings.
5. Cadence: the 2026-10-16 capture fetched `*_20261014.csv` with `last_modified` 2026-10-14.

## Unverified, and open questions

- Dark mode not screenshotted: headless rendered light only.
- At 1440, headless captured nothing below the chart (blank, probably scroll-reveal). I checked those sections at
  1024, 768 and 390.
- Why 2022-23 T-4, 2027-28 T-1 and 2030-31 T-4 have no price. The 2022-23 T-4 still has 1,126 CMU applications. The
  page states no cause.
- CMU obligations summed per auction fall slightly below the lead's awarded volume for older auctions (for example
  2020-21 T-4: 52,359.0 against 52,425.3). They match exactly for 2028-29 and 2029-30. The cause is unknown and the
  page does not claim either way.
- Is summing `capacity_awarded` across auctions per delivery year the right total? I believe agreements for one year
  from different auctions add, but NESO does not say so. The plot alt says "summed across auctions" and claims no total
  meaning.

## Template problems (seat items)

- **Bar value labels round to two significant figures** (`fmt_num`). Prices read 28 for £27.50, 22 for £22.50 (it
  rounds half to even), 7.0 for 6.95 and 36 for 35.79. For a price chart, a fixed two-decimal label would read better.
  The alt gives exact values.
- A bar spec has no way to colour bars by a second column (auction type), unless every category gets its own key
  entry. I labelled the type in the category name instead.

## Defects (paste into the backlog)

- **Privacy, CMU change log.** `capacity_market_unit_cmu_history` logs contact emails and telephone numbers in
  `previous`/`latest` under four attribute spellings (13,386 rows). Any gridflow_models `describe()` or `tail()` of
  this table, or of `capacity_market_unit_cmu`, would print them. Suggest a documented exclusion or masking at the
  workbench layer. Not verified by running `describe()`, deliberately.
- **Vendor data: attribute spellings.** The CMU and component change logs use two spellings for the same attribute:
  - `Connection / DSR Capacity` vs `Connection or DSR Capacity`;
  - `Pre-Qualification Decision` vs `Pre Qualification Decision`;
  - `Transmission / Distribution` vs `Transmission or Distribution`;
  - `Permitted on-Site Generating Unit` vs `Permitted On Site Generating Unit`;
  - the contact attributes above.

  Any filter on `attribute` must list both.
- **Vault note staleness (fixed on the branch):** the capture count, the `casting.py` line numbers and the CMU
  History contact values, as above.

## What the checker should look at hardest

1. **Personal data.** Grep the page and the three artefacts; open the notebook outputs. Confirm no cell can surface
   contact rows.
2. **Chart against silver.** Check the 24 values and the three dropped nulls. Check the unit wording against NESO's
   heading and dictionary.
3. **Guide claims scoped "here":**
   - base period null on the T-1 rows;
   - fee 6 only on 2027-28 T-1 and 2030-31 T-4;
   - `100%` annual cap.
4. **The capture table above,** and the `Captures` body edit.
5. **The notebook's sum across auctions per delivery year** (open question above). Also check that `pipeline --last
   24h` lines are acceptable for a package whose auction files rarely change: a run fetches nothing new when
   `last_modified` is unchanged.
