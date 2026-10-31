---
source: "neso_data_portal"
package: "capacity-market-register"
dataset_keys: ["capacity_market_auction_cost", "capacity_market_auction_static", "capacity_market_component_history", "capacity_market_component_history_pre", "capacity_market_components", "capacity_market_de_rating_factors", "capacity_market_unit_cmu", "capacity_market_unit_cmu_history"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Capacity Market Register
  summary: >-
    NESO's register of GB Capacity Market auctions: clearing prices, target and awarded capacity,
    cost per delivery year, units and their components.
  facts:
    vendor: "NESO Data Portal, package `capacity-market-register`: eight CSV files"
    cadence: "Weekly, NESO's stated update frequency; gridflow skips unchanged files"
    grain: "Lead table: one row per Capacity Market auction"
  landscape: market
  what_it_is: >-
    The EMR Delivery Body keeps a register for every Capacity Market auction (NESO). The eight
    files give each auction's terms and clearing price, MW awarded and forecast cost per delivery
    year, de-rating factors, each unit's application (CMU) and its components, and weekly change
    logs. The CMU files hold contact details; this page never shows them.
  how_used:
    - Clearing price and awarded MW per auction, as capacity revenue in a plant model
    - "Our sum of NESO's per-auction MW awarded per delivery year; NESO gives no total"
    - "Unit obligations by fuel or technology via `data.sql`; `query()` filters capture time"
  chart:
    type: bar
    silver: neso_data_portal/capacity_market_auction_static
    filter:
      - {column: clearing_price_gbp_per_kw_per_year, op: not_null}
    dedup: {on: [auction_name], order_by: published_at}
    group: auction_name
    group_map:
      "2016-17 (TR) Transitional Capacity Auction": "2016-17 TR"
      "2017-18 (T-1) One Year Ahead Capacity Auction": "2017-18 T-1"
      "2017-18 (TR) Transitional Capacity Auction": "2017-18 TR"
      "2018-19 (T-1) One Year Ahead Capacity Auction": "2018-19 T-1"
      "2018-19 (T-4) Four Year Ahead Capacity Auction": "2018-19 T-4"
      "2019-20 (T-1) One Year Ahead Capacity Auction": "2019-20 T-1"
      "2019-20 (T-4) Four Year Ahead Capacity Auction": "2019-20 T-4"
      "2020-21 (T-1) One Year Ahead Capacity Auction": "2020-21 T-1"
      "2020-21 (T-4) Four Year Ahead Capacity Auction": "2020-21 T-4"
      "2021-22 (T-1) One Year Ahead Capacity Auction": "2021-22 T-1"
      "2021-22 (T-4) Four Year Ahead Capacity Auction": "2021-22 T-4"
      "2022-23 (T-1) One Year Ahead Capacity Auction": "2022-23 T-1"
      "2022-23 (T-3) Three Year Ahead Capacity Auction": "2022-23 T-3"
      "2023-24 (T-1) One Year Ahead Capacity Auction": "2023-24 T-1"
      "2023-24 (T-4) Four Year Ahead Capacity Auction": "2023-24 T-4"
      "2024-25 (T-1) One Year Ahead Capacity Auction": "2024-25 T-1"
      "2024-25 (T-4) Four Year Ahead Capacity Auction": "2024-25 T-4"
      "2025-26 (T-1) One Year Ahead Capacity Auction": "2025-26 T-1"
      "2025-26 (T-4) Four Year Ahead Capacity Auction": "2025-26 T-4"
      "2026-27 (T-1) One Year Ahead Capacity Auction": "2026-27 T-1"
      "2026-27 (T-4) Four Year Ahead Capacity Auction": "2026-27 T-4"
      "2027-28 (T-4) Four Year Ahead Capacity Auction": "2027-28 T-4"
      "2028-29 (T-4) Four Year Ahead Capacity Auction": "2028-29 T-4"
      "2029-30 (T-4) Four Year Ahead Capacity Auction": "2029-30 T-4"
    value: clearing_price_gbp_per_kw_per_year
    aggregation: last
    sort: label
    unit: "£ per kW per year"
  chart_view:
    title: Clearing price by auction, delivery years 2016-17 to 2029-30
    caption: >-
      Silver `capacity_market_auction_static`, NESO's file of 9 September 2026: each auction's
      clearing price, £ per kW per year (NESO's column heading), labelled by first delivery year and
      auction type. No price, so not drawn: 2022-23 T-4, 2027-28 T-1, 2030-31 T-4.
    alt: >-
      Horizontal bar chart from neso_data_portal/capacity_market_auction_static, NESO's file of 9
      September 2026: clearing price in £ per kW per year for 24 Capacity Market auctions, in
      delivery-year order from 2016-17 TR to 2029-30 T-4. The highest is 75 (2022-23 T-1), then 65
      (2027-28 T-4) and 63 (2026-27 T-4); the lowest are 0.77 (2019-20 T-1) and 1 (2020-21 T-1).
      Four-year-ahead prices run from 8.4 (2021-22) to 65; the 2029-30 T-4 cleared at 27.1.
    key:
      - {series: clearing_price_gbp_per_kw_per_year, label: Clearing price, paint: petrol, note: "TR is NESO's Transitional auction; T-1, T-3 and T-4 run one, three and four years ahead."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each file's download; a file whose
      `last_modified` has not changed is skipped. The four weekly files carry an upload date in
      their names.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=capacity-market-register"
      - "GET https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/784fa703-1460-42cd-a8bb-fba4dcabac8d/download/capacity-market-auction-static-data.csv"
    commands:
      - {run: gridflow pipeline neso_data_portal capacity_market_auction_static --last 24h, comment: "auction terms, bronze then silver"}
      - {run: gridflow pipeline neso_data_portal capacity_market_auction_cost --last 24h, comment: "cost per delivery year (notebook)"}
      - {run: gridflow pipeline neso_data_portal capacity_market_unit_cmu --last 24h, comment: "the CMU register (notebook)"}
  record:
    select:
      filter:
        - {column: auction_name, op: in, value: ["2025-26 (T-4) Four Year Ahead Capacity Auction",
                                                  "2026-27 (T-1) One Year Ahead Capacity Auction",
                                                  "2026-27 (T-4) Four Year Ahead Capacity Auction",
                                                  "2027-28 (T-1) One Year Ahead Capacity Auction",
                                                  "2027-28 (T-4) Four Year Ahead Capacity Auction",
                                                  "2028-29 (T-4) Four Year Ahead Capacity Auction",
                                                  "2029-30 (T-4) Four Year Ahead Capacity Auction",
                                                  "2030-31 (T-4) Four Year Ahead Capacity Auction"]}
      dedup: {on: [auction_name], order_by: published_at}
      order_by: [auction_name]
      columns: [auction_name, clearing_price_gbp_per_kw_per_year, total_volume_of_agreements_awarded,
                auction_target_capacity_mw, base_period_for_the_agreement, termination_fee_1_rate,
                termination_fee_2_rate, termination_fee_3_rate, termination_fee_4_rate,
                termination_fee_5_rate, termination_fee_6_rate, termination_fee_7_rate,
                termination_fee_8_rate, termination_fee_9_rate, annual_penalty_cap,
                monthly_penalty_cap, published_at]
    key: [auction_name, published_at]
    caption: "Eight auctions for delivery from 2025-26 to 2030-31, NESO's 9 September 2026 file."
    fields:
      auction_name: "NESO's name: first delivery year, auction type in brackets, then the title"
      published_at: "CKAN's last-modified time of the file the row came from, read as UTC"
      clearing_price_gbp_per_kw_per_year: "Clearing price, £ per kW per year (NESO's heading); null where NESO gives none"
      total_volume_of_agreements_awarded: "Capacity Agreements awarded, MW, rounded to three decimal places (NESO)"
      auction_target_capacity_mw: "The auction's target capacity, MW, as in the Electricity Capacity Report (NESO)"
      base_period_for_the_agreement: "Base period for calculating capacity payments (NESO); null here on T-1 and 2030-31 T-4"
      termination_fee_1_rate: "Termination fee 1 rate as NESO writes it, text such as `£5000 /MW`"
      termination_fee_2_rate: "Termination fee 2 rate, £ per MW, kept as NESO's text"
      termination_fee_3_rate: "Termination fee 3 rate, £ per MW, kept as NESO's text"
      termination_fee_4_rate: "Termination fee 4 rate, £ per MW, kept as NESO's text"
      termination_fee_5_rate: "Termination fee 5 rate, £ per MW, kept as NESO's text"
      termination_fee_6_rate: "Fee 6 rate as text; in these rows only 2027-28 T-1 and 2030-31 T-4"
      termination_fee_7_rate: "Termination fee 7 rate, £ per MW, kept as NESO's text"
      termination_fee_8_rate: "Termination fee 8 rate, £ per MW, kept as NESO's text"
      termination_fee_9_rate: "Termination fee 9 rate, £ per MW, kept as NESO's text"
      annual_penalty_cap: "Annual penalty cap, a percentage kept as NESO's text (`100%` here)"
      monthly_penalty_cap: "Monthly penalty cap, a percentage as text; NESO's dictionary gives no description"
      timestamp_utc: "When gridflow wrote the capture, UTC; not an auction or delivery date"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      The auction file has no auction date and `query()` filters on capture time, so each cell reads
      a `_latest` view with `data.sql`. The CMU cell selects fuel and obligation only, never names or
      contacts.
    cells:
      - |
        auctions = data.sql("""
            SELECT auction_name, clearing_price_gbp_per_kw_per_year AS price,
                   auction_target_capacity_mw AS target_mw,
                   total_volume_of_agreements_awarded AS awarded_mw,
                   base_period_for_the_agreement AS base_period
            FROM silver_neso_data_portal_capacity_market_auction_static_latest
            ORDER BY auction_name""")
        auctions[auctions.auction_name.str.contains("(T-4)", regex=False)]
      - |
        units = data.sql("""
            SELECT primary_fuel_type, COUNT(*) AS units,
                   SUM(auction_acquired_capacity_obligation) AS obligation_mw
            FROM silver_neso_data_portal_capacity_market_unit_cmu_latest
            WHERE auction_name = '2029-30 (T-4) Four Year Ahead Capacity Auction'
              AND capacity_agreement_awarded = 'Yes'
            GROUP BY primary_fuel_type ORDER BY obligation_mw DESC""")
        units.loc[len(units)] = ["total", units.units.sum(), units.obligation_mw.sum()]
        units.round(3)
      - |
        cost = data.sql("""
            SELECT auction_name, delivery_year, capacity_awarded
            FROM silver_neso_data_portal_capacity_market_auction_cost_latest""")
        cost["auction"] = cost.auction_name.str.extract(r"\((T-\d|TR)\)")[0]
        mw = cost.pivot_table(index="delivery_year", columns="auction",
                              values="capacity_awarded", aggfunc="sum")
        ax = mw[["T-4", "T-3", "T-1", "TR"]].plot.bar(
            stacked=True, width=0.85, figsize=(8, 3.5),
            color=["#155A6E", "#3E8C97", "#AFC64E", "#C77E3C"],
            xlabel="delivery year", ylabel="MW awarded, summed over auctions")
        ax.legend(ncol=4, loc="lower center", bbox_to_anchor=(0.5, 1.0), frameon=False);
    needs: a capture of the auction, auction cost and CMU tables
    plot_alt: >-
      Stacked bar plot of our sum, per delivery year, of NESO's MW awarded by every auction, split by
      auction type; NESO gives no per-year total. 2016/2017 sums to 803 MW (TR only). Each delivery
      year from 2017/2018 to 2029/2030 sums to between 54,746 and 62,325 MW. Later years fall from
      23,754 MW in 2030/2031 to 1,167 MW in 2043/2044.
  related:
    - {dataset: neso_data_portal/transmission-entry-capacity-tec-register, note: "TEC contracts behind the CMU table's TEC deferral columns"}
    - {dataset: neso_data_portal/interconnector-register, note: "Contracted interconnectors; the CMU table lists interconnector units by link"}
    - {dataset: neso_data_portal/embedded-register, note: "Embedded projects in Scotland; CMU rows mark each unit Transmission or Distribution"}
    - {dataset: elexon/lolpdrm, note: "Elexon's de-rated margin per settlement period, a short-run adequacy measure"}
  family:
    slug: capacity-market-register
    members:
      - dataset: capacity_market_auction_static
        differs: "One row per auction: clearing price, target and awarded MW, fee rates"
        request: "GET https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/784fa703-1460-42cd-a8bb-fba4dcabac8d/download/capacity-market-auction-static-data.csv"
      - dataset: capacity_market_auction_cost
        differs: "One row per auction and delivery year: MW awarded and forecast cost, £"
        request: "GET https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/b1b58919-eaa4-40ea-80df-3d3e526f8223/download/capacity-market-auction-capacity-and-cost.csv"
      - dataset: capacity_market_unit_cmu
        differs: "One row per unit application per auction; holds contact columns, never shown here"
        request: "GET https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/25a5fa2e-873d-41c5-8aaf-fbc2b06d79e6/download/cmu_20261014.csv"
      - dataset: capacity_market_unit_cmu_history
        differs: "One changed CMU attribute per row, previous and latest; contact changes included"
        request: "GET https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/cd034839-73e7-4c37-b4e5-6ebea25627d8/download/cmu_changes_20261014.csv"
      - dataset: capacity_market_components
        differs: "One row per auction, application and component; small ones aggregated from 22 July 2026"
        request: "GET https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/790f5fa0-f8eb-4d82-b98d-0d34d3e404e8/download/component_20261014.csv"
      - dataset: capacity_market_component_history
        differs: "Component changes after the 22 July 2026 aggregation, logged from 29 July"
        request: "GET https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/62bca39c-d4f0-4cd6-b2ff-8ef42dca7f23/download/component_changes_20261014.csv"
      - dataset: capacity_market_component_history_pre
        differs: "Component changes before aggregation, frozen after 22 July 2026; never union the two"
        request: "GET https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/015453e0-c73c-416a-901d-623f914c8e70/download/component_changes_20260715.csv"
      - dataset: capacity_market_de_rating_factors
        differs: One de-rating factor per auction and generating technology class
        request: "GET https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/d94ff98d-39ba-40d6-9672-7433de0631ac/download/capacity-market-de-rating-factors.csv"
---

# Capacity Market Register

The Capacity Market Register (CMR) is the public record of GB's Capacity Market. The
Capacity Market pays providers to commit capacity for a delivery year, with agreements
won in auctions (general market context, not from the vendor dictionary). The package description says the EMR Delivery Body must create and keep
a register for every Capacity Market auction. Each register records every application
made to the Delivery Body before the auction, who won a Capacity Agreement, and any
enduring obligations. The package holds eight CSV files at three levels:

- **Auction level:** awarded capacity and forecast cost per auction and delivery year,
  static auction terms (clearing price, target capacity, termination-fee rates, penalty
  caps), and de-rating factors per generating technology class.
- **Unit level:** the Capacity Market Unit (CMU) register (one row per application per
  auction, with agreement, milestone and capacity fields) and the Components register
  (the physical parts behind each CMU).
- **Change logs:** week-on-week attribute changes for CMUs and for components. Each row
  gives the previous and latest published value of one attribute.

Models can use it for the capacity side of GB adequacy: de-rated capacity per unit and
technology, clearing prices, agreement terms and the timing of new-build milestones and
terminations. The package description also points to the vendor's own summary of
clearing prices and aggregate volumes on the Capacity Market Portal Knowledge site:
https://emrdeliverybody.nationalenergyso.com/IG/s/article/Auction-Results-and-De-rating-Factors-Summary-Data-Workbook.

> **Component aggregation boundary (vendor notice, package description).** From
> **22 July 2026**, components below **30 kW** are aggregated per Generating Technology
> Class per CMU, with extra aggregation for permitted on-site generating units. Components
> of 30 kW or more are still listed one by one. A `Number of Components` column was added
> to the Components file. The old component change log was renamed "Component History -
> Pre Aggregation" and is no longer changed after 22 July 2026. A new "Component History"
> file, filled from **29 July 2026**, logs changes after aggregation. The two histories
> are separate silver families and must not be unioned as one series (see
> `capacity_market_component_history_pre` below).

The data comes from a CKAN upload-file package on the NESO Open Data Portal
(@../README.md). **Status: eligible.** All eight silver outputs are published; none is
held (RULINGS 521). This page gives schema, row counts and measured structure. It quotes
no row values: the CMU file includes contact telephone and email columns and the names of
applicants, agents and security-interest holders.

- Publisher group: Electricity Market Reform
- Registry group: electricity-market-reform · archetype: REG

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Capacity Market Auction Capacity and Cost | CSV | upload | `b1b58919-eaa4-40ea-80df-3d3e526f8223` |
| Capacity Market Auction Static Data | CSV | upload | `784fa703-1460-42cd-a8bb-fba4dcabac8d` |
| Capacity Market De-Rating Factors | CSV | upload | `d94ff98d-39ba-40d6-9672-7433de0631ac` |
| Capacity Market Unit (CMU) | CSV | upload | `25a5fa2e-873d-41c5-8aaf-fbc2b06d79e6` |
| Capacity Market Unit (CMU) History | CSV | upload | `cd034839-73e7-4c37-b4e5-6ebea25627d8` |
| Component History | CSV | upload | `62bca39c-d4f0-4cd6-b2ff-8ef42dca7f23` |
| Component History - Pre Aggregation | CSV | upload | `015453e0-c73c-416a-901d-623f914c8e70` |
| Components | CSV | upload | `790f5fa0-f8eb-4d82-b98d-0d34d3e404e8` |

There are no DOC, CATALOGUE-ONLY or excluded resources in this package.

### Resource download links

URLs are the `request_url` in each capture's bronze sidecar (capture date 2026-10-08):

| Resource | Disposition | Download |
|---|---|---|
| Capacity Market Auction Capacity and Cost (CSV) | SILVER → `capacity_market_auction_cost` | [capacity-market-auction-capacity-and-cost.csv](https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/b1b58919-eaa4-40ea-80df-3d3e526f8223/download/capacity-market-auction-capacity-and-cost.csv) |
| Capacity Market Auction Static Data (CSV) | SILVER → `capacity_market_auction_static` | [capacity-market-auction-static-data.csv](https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/784fa703-1460-42cd-a8bb-fba4dcabac8d/download/capacity-market-auction-static-data.csv) |
| Capacity Market De-Rating Factors (CSV) | SILVER → `capacity_market_de_rating_factors` | [capacity-market-de-rating-factors.csv](https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/d94ff98d-39ba-40d6-9672-7433de0631ac/download/capacity-market-de-rating-factors.csv) |
| Capacity Market Unit (CMU) (CSV) | SILVER → `capacity_market_unit_cmu` | [cmu_20261007.csv](https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/25a5fa2e-873d-41c5-8aaf-fbc2b06d79e6/download/cmu_20261007.csv) |
| Capacity Market Unit (CMU) History (CSV) | SILVER → `capacity_market_unit_cmu_history` | [cmu_changes_20261007.csv](https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/cd034839-73e7-4c37-b4e5-6ebea25627d8/download/cmu_changes_20261007.csv) |
| Component History (CSV) | SILVER → `capacity_market_component_history` | [component_changes_20261007.csv](https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/62bca39c-d4f0-4cd6-b2ff-8ef42dca7f23/download/component_changes_20261007.csv) |
| Component History - Pre Aggregation (CSV) | SILVER → `capacity_market_component_history_pre` | [component_changes_20260715.csv](https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/015453e0-c73c-416a-901d-623f914c8e70/download/component_changes_20260715.csv) |
| Components (CSV) | SILVER → `capacity_market_components` | [component_20261007.csv](https://api.neso.energy/dataset/0b3ab475-5622-4465-8825-9d35d03bb28b/resource/790f5fa0-f8eb-4d82-b98d-0d34d3e404e8/download/component_20261007.csv) |

The four weekly files (CMU, CMU History, Component History, Components) have the upload
date in their filename, and the filename changes each week. The catalogue snapshot
`20261006T195819Z` listed them as `*_20260930.csv`; the 2026-10-08 capture fetched
`*_20261007.csv`. The stable handle is the resource id, not the URL. The three
auction-level files have undated, stable filenames. The pre-aggregation history keeps its
frozen `component_changes_20260715.csv`.

The package has these 8 resources and no others (`num_resources: 8`, CKAN package id
`0b3ab475-5622-4465-8825-9d35d03bb28b`). All 8 are also loaded into the CKAN Datastore
(`datastore_active: true`); their field dictionaries are the source of the units below.
gridflow downloads the uploaded files; it does not read the Datastore.

## Families

**Common to all eight families.**
- **Captures.** Each family has one header epoch. The three auction-level families and the
  pre-aggregation history have one bronze body (captured 2026-10-08). The four weekly
  families have a second (captured 2026-10-16, CKAN `last_modified` 2026-10-14) with the
  same header: CMU 18,200 rows, CMU History 72,282, Components 29,849, Component History
  7,488. Every row of the first CMU History and Component History capture recurs in the
  second, so a read across captures must deduplicate or use the `_latest` view. Whether
  the schema stays stable over time is not established.
- **Vintage clock: `ckan_last_modified`.** `published_at` and `available_at` both equal
  the CKAN `last_modified` of the resource at capture. CKAN gives this value without an
  offset; gridflow reads it as UTC (ADR-030 D-15, corroborated rather than
  vendor-documented). Every resource is `url_type=upload`, so this is the file's upload
  time, not a release time for any one row. Each family's value is given below.
- **No issue clock.** Every epoch has issue `{"kind": "none"}`. None of these files is a
  forecast archive.
- **Event time, recipe `none`.** `timestamp_utc` (and `event_time`, copied from it) is the
  **capture time**: the bronze write instant, the same on every row. It is not an
  auction, delivery or agreement date (`src/gridflow/silver/neso_data_portal/casting.py:605`,
  `src/gridflow/silver/base.py:2232`).
- **Event time, recipe `date_sp1(change_date)`** (the three change logs).
  `timestamp_utc` is the start of settlement period 1 of `change_date` on the London
  clock, so London local midnight in UTC (`casting.py:620`). Observed in silver:
  `T00:00Z` for a GMT date and `T23:00Z` the day before for a BST date. It anchors the
  civil date the change was first reported. It is **not** a release instant; the
  intraday timing is not documented.
- **Point-in-time use.** Use `available_at`, not `change_date` or the CMU date columns,
  to decide what was known when. A change dated D enters silver only with the capture
  whose file contains it.
- **Keys are capture-uniqueness guards.** No vendor source guarantees that a row keeps the
  same identity across uploads, so every family uses `_latest = whole_capture`: the newest
  capture is the latest view and dropped rows are not carried forward.
- **Silver path:** `C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`,
  one Parquet file per family. Engine columns after the vendor columns: `timestamp_utc`,
  `published_at`, `capture_written_at`, `event_time`, `available_at` (Datetime µs, UTC),
  `bronze_capture_id`, `source_run_id`, `dataset_version` (String). The three change logs
  also carry `change_date` as a Date.
- **Activation:** cutoff 2026-10-08 under RULINGS 524/525. Every row count below equals the
  planned count, and reconcile `--cutoff 2026-10-08` found 0 gaps for these families.
- **Where the generated "Vendor unit" column says less than the dictionary.** It shows each
  field's `unit` entry only. Three cases need the dictionary comment as well, and are
  covered per family below: the clearing price (`£`, but the basis is £/kW/year), the
  agreement-length columns (`Number`, but the comments give years) and the de-rating
  factor (unit field blank).

### `capacity_market_auction_cost`

- Kind: tabular · archetype: REG · refresh: weekly · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Name | `auction_name` | string | — | yes | — | — |
| Delivery Year | `delivery_year` | string | — | yes | — | — |
| Capacity Awarded | `capacity_awarded` | float64 | — | yes | — | MW |
| Forecast Cost_GBP | `forecast_cost_gbp` | float64 | — | yes | — | £ |

- Entity key: `auction_name`, `delivery_year`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Column meanings.** One row per auction and delivery year; the vendor describes the grain
this way (catalogue snapshot). `Capacity Awarded` is capacity awarded in the auction for
that delivery year. `Forecast Cost_GBP` is the forecast cost, which the dictionary relates
to the awarded capacity and the auction clearing price.

**Units (vendor field dictionary, `field-info/20261008T114228Z/capacity_market_auction_cost.json`).**
`Capacity Awarded` is **MW** (line 46). `Forecast Cost_GBP` is **£** (line 58). Values are
not rescaled. `Delivery Year` is a year label and stays a string. Agreements can run over
several delivery years, so no date is derived from it (K-CI-FACTS §2.6 g1).

**Two clocks.**
1. **Vintage `ckan_last_modified`:** `published_at` = `available_at` =
   2026-09-09T11:54:02.061035Z.
2. **Event time `none`:** `timestamp_utc` is the capture time, 2026-10-08T09:14:15.921895Z
   on every row. It is not an auction or delivery date.

**Identity.** `(auction_name, delivery_year)` guard: 192 distinct pairs, 0 duplicates, 0
missing in the captured body.
- TODO: verify whether NESO guarantees one stable row per auction and delivery year
  across uploads.

**Sentinels and nulls (K-CI-FACTS §2.6 g5).** The captured body has no blanks, no sentinel
spellings and no numeric zeros. That does not define how future blanks should be read.
The columns stay nullable, so a blank would load as null, not zero.

**Silver output.** **192 rows** from
`raw_20261008T091415Z_b1b58919-…_eda39a73.csv` (14,873 bytes).

### `capacity_market_auction_static`

- Kind: tabular · archetype: REG · refresh: weekly · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Name | `auction_name` | string | — | yes | — | — |
| Clearing Price_GBP per kW per year | `clearing_price_gbp_per_kw_per_year` | float64 | — | yes | — | £ |
| Base Period for the Agreement | `base_period_for_the_agreement` | string | — | yes | — | — |
| Auction Target Capacity_MW | `auction_target_capacity_mw` | float64 | — | yes | — | MW |
| Total Volume of Agreements Awarded | `total_volume_of_agreements_awarded` | float64 | — | yes | — | MW |
| Termination Fee 1 Rate | `termination_fee_1_rate` | string | — | yes | — | £ per MW |
| Termination Fee 2 Rate | `termination_fee_2_rate` | string | — | yes | — | £ per MW |
| Termination Fee 3 Rate | `termination_fee_3_rate` | string | — | yes | — | £ per MW |
| Termination Fee 4 Rate | `termination_fee_4_rate` | string | — | yes | — | £ per MW |
| Termination Fee 5 Rate | `termination_fee_5_rate` | string | — | yes | — | £ per MW |
| Termination Fee 6 Rate | `termination_fee_6_rate` | string | — | yes | — | £ per MW |
| Termination Fee 7 Rate | `termination_fee_7_rate` | string | — | yes | — | £ per MW |
| Termination Fee 8 Rate | `termination_fee_8_rate` | string | — | yes | — | £ per MW |
| Termination Fee 9 Rate | `termination_fee_9_rate` | string | — | yes | — | £ per MW |
| Annual Penalty Cap | `annual_penalty_cap` | string | — | yes | — | % |
| Monthly Penalty Cap | `monthly_penalty_cap` | string | — | yes | — | % |

- Entity key: `auction_name`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Column meanings.** One row per auction, with the auction's fixed terms. `Base Period for
the Agreement` is the period used to calculate capacity payments; the dictionary example
is an interval string, but the captured values read `Winter 2012/2013` to
`Winter 2024/2025`. The termination-fee and penalty-cap columns are the auction's
rates. `Monthly Penalty Cap` is a percentage, not a time column.

**Units (vendor field dictionary, `field-info/20261008T114228Z/capacity_market_auction_static.json`; K-CI-FACTS §2.7 g4).**

| Column | Unit | Dictionary line |
|---|---|---|
| Clearing Price_GBP per kW per year | **£ per kW per year.** The `unit` field says only `£`; the per-kW-per-year basis comes from the dictionary comment (`£kW/year`) and the renamed heading documented in the catalogue | 34 |
| Auction Target Capacity_MW | MW | 58 |
| Total Volume of Agreements Awarded | MW | 70 |
| Termination Fee 1–9 Rate | £ per MW, kept as the vendor's formatted text | 82–178 |
| Annual Penalty Cap | %, kept as text | 190 |
| Monthly Penalty Cap | %, kept as text | 202 |

`Base Period for the Agreement` stays a string.
- TODO: verify whether the base-period interval includes its end points and any intraday
  convention. The inspected sources do not say; a vendor agreement-period specification
  would settle it.

**Two clocks.**
1. **Vintage `ckan_last_modified`:** `published_at` = `available_at` =
   2026-09-09T11:51:45.161649Z.
2. **Event time `none`:** `timestamp_utc` is the capture time, 2026-10-08T09:14:19.659695Z
   on every row.

**Identity.** `auction_name` guard: 27 distinct non-missing names, 0 duplicates.
- TODO: verify that NESO guarantees a stable, unique auction name.

**Sentinels and nulls (K-CI-FACTS §2.7 g5).** Blank cells in the captured body: clearing
price, target capacity and awarded volume 3 each; base period 14; Termination Fee 3–5 3
each; Termination Fee 6–9 25 each; Termination Fee 1–2 none. Blanks stay null and are never replaced by zero.
- TODO: verify whether each blank means "not applicable to this auction" or "not
  available".

**Silver output.** **27 rows** from `raw_20261008T091419Z_784fa703-…_2b0e779b.csv`
(4,319 bytes).

### `capacity_market_component_history`

- Kind: tabular · archetype: REG · refresh: weekly · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Name | `auction_name` | string | — | yes | — | — |
| Application ID | `application_id` | string | — | yes | — | — |
| CMU ID | `cmu_id` | string | — | yes | — | — |
| Component ID | `component_id` | string | — | yes | — | — |
| Type | `type` | string | — | yes | — | — |
| Delivery Year | `delivery_year` | string | — | yes | — | Year |
| Attribute | `attribute` | string | — | yes | — | — |
| Previous | `previous` | string | — | yes | — | — |
| Latest | `latest` | string | — | yes | — | — |
| Change Type | `change_type` | string | — | yes | — | — |
| Change Date | `change_date` | date | `%Y-%m-%d` | no | — | — |

- Entity key: `auction_name`, `application_id`, `cmu_id`, `component_id`, `type`, `delivery_year`, `attribute`, `previous`, `latest`, `change_type`, `change_date`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`change_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Column meanings.** The week-on-week log of component-level changes **after** the
22 July 2026 aggregation; the vendor says it is filled from 29 July 2026. Each row is one
changed attribute of one component. `Previous` is the value last published and `Latest`
the updated value (dictionary lines 106 and 118). `Change Type` marks the kind of change
(line 130), and `Change Date` is the date the change was first reported on the CMR
(line 142).

**Units.** `Previous` and `Latest` are mixed-type text: their meaning and unit depend on
`Attribute`, so no unit applies to the column. Numeric- and date-looking strings stay as
strings. `Delivery Year` is a year label. The ID columns are identifiers.

**Two clocks.**
1. **Vintage `ckan_last_modified`:** `published_at` = `available_at` =
   2026-10-07T14:26:38.881535Z.
2. **Event time `date_sp1(change_date)`:** `timestamp_utc` is London midnight of
   `change_date`, in UTC (see "Common to all eight families"). `change_date` spans
   2026-07-29 to 2026-10-07 with 11 distinct dates; in silver `timestamp_utc` runs
   2026-07-28T23:00Z to 2026-10-06T23:00Z because these dates are in BST. It is the
   reporting date, not a release instant. (First capture; the 2026-10-16 capture runs to
   2026-10-14 with 12 distinct dates.)

**Identity.** Every column is the guard (0 full-row duplicates). 7,460 rows cover 212
distinct CMU IDs and 593 distinct Component IDs. The shorter composite `(Auction Name,
Application ID, CMU ID, Component ID, Attribute, Change Type, Change Date)` was also unique
in the capture (7,460 distinct, 0 missing), but it is a measurement, not a vendor key.
- TODO: verify whether NESO has a change-event identifier.

**Sentinels and nulls (K-CI-FACTS §2.11 g5).** By change type: `New` 4,937 rows, all with
blank `Previous`; `Removed` 2,499 rows, all with blank `Latest`; `Detail` 24 rows. These
blanks are the absent side of a change, as the dictionary's descriptions of Previous,
Latest and change types support. Numeric-looking strings and zeros are kept as written.

**Silver output.** **7,460 rows** from `raw_20261008T091423Z_62bca39c-…_a619ea93.csv`
(1,215,696 bytes); **7,488 rows** from `raw_20261016T192048Z_62bca39c-…_56ddfdff.csv`
(1,220,265 bytes).

### `capacity_market_component_history_pre`

- Kind: tabular · archetype: REG · refresh: weekly · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Name | `auction_name` | string | — | yes | — | — |
| Application ID | `application_id` | string | — | yes | — | — |
| CMU ID | `cmu_id` | string | — | yes | — | — |
| Component ID | `component_id` | string | — | yes | — | — |
| Type | `type` | string | — | yes | — | — |
| Delivery Year | `delivery_year` | string | — | yes | — | Year |
| Attribute | `attribute` | string | — | yes | — | — |
| Previous | `previous` | string | — | yes | — | — |
| Latest | `latest` | string | — | yes | — | — |
| Change Type | `change_type` | string | — | yes | — | — |
| Change Date | `change_date` | date | `%Y-%m-%d` | no | — | — |

- Entity key: `auction_name`, `application_id`, `cmu_id`, `component_id`, `type`, `delivery_year`, `attribute`, `previous`, `latest`, `change_type`, `change_date`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`change_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Column meanings.** The component-level change log from **before** the 22 July 2026
aggregation. The vendor says no changes are made to this file after that date. Its
header is exactly the same as `capacity_market_component_history`, and the column
meanings are the same.

**Not one series with `capacity_market_component_history` (K-CI-FACTS §3.3 CI-3).** Over
the full bodies of both files:

| Check | Result |
|---|---|
| Same ordered header | yes |
| Shared distinct Component IDs | 325 |
| Shared distinct CMU IDs | 105 |
| Shared `change_date` values | 0 |
| `change_date` span, pre | 2025-12-10 .. 2026-07-15 (27 distinct) |
| `change_date` span, post | 2026-07-29 .. 2026-10-07 (11 distinct; first capture; to 2026-10-14, 12 distinct, in the second) |

The same header and some shared IDs do not mean the same entity grain. After the boundary
a Component ID can be an aggregate, not the original component. Keep the two families
separate. A combined history must keep a column saying which aggregation regime each row
belongs to, and must not assume a component before 22 July maps to an aggregate after it.
- TODO: verify whether NESO publishes a crosswalk from pre-aggregation components to
  post-aggregation aggregate IDs, and whether identifiers persist across the boundary.

**Units.** As for `capacity_market_component_history`: `Previous`/`Latest` are mixed-type
text whose meaning depends on `Attribute`.

**Two clocks.**
1. **Vintage `ckan_last_modified`:** `published_at` = `available_at` =
   2026-07-15T10:09:26.879666Z, the file's last upload before the freeze (the capture
   URL is `component_changes_20260715.csv`). Because the vendor no longer changes the
   file, this vintage should not move in later captures.
2. **Event time `date_sp1(change_date)`:** London midnight of `change_date`, in UTC.
   `change_date` spans 2025-12-10 to 2026-07-15 with 27 distinct dates. The vendor's
   freeze statement concerns the file, not when individual rows became available.

**Identity.** Every column is the guard (0 full-row duplicates over 1,918,503 rows). The
profiler's shorter candidates are **not** unique:

```text
(Application ID, Component ID, Attribute): distinct 1,406,711; duplicate excess 511,792
(CMU ID, Component ID, Attribute):         distinct 1,315,544; duplicate excess 602,959
```

The longer composite used for the post-aggregation history was unique (1,918,503 distinct),
but no vendor source guarantees it. The body has 255,664 distinct Component IDs and 1,572
distinct CMU IDs.
- TODO: verify whether NESO has a change-event identifier.

**Sentinels and nulls (K-CI-FACTS §2.12 g5).** By change type: `First Release` 957,119 rows
and `New` 739,404 rows, all with blank `Previous`; `Removed` 201,976 rows, all with blank
`Latest`. The body also has 15 literal `N/A` values in `Latest` and 6 Component IDs that
are the string `000000`. Both are kept as written; identifiers are never normalised and `N/A`
is not turned into null.
- TODO: verify what NESO means by those `N/A` values and zero Component IDs.

**Silver output.** **1,918,503 rows** from
`raw_20261008T091431Z_015453e0-…_dab8d99a.csv` (291,237,571 bytes). The transform peaked
at 1,788.0 MiB, the most of any family in the batch (`.planning/v0.22-RESULTS.md` §CI).

### `capacity_market_components`

- Kind: tabular · archetype: REG · refresh: weekly · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Name | `auction_name` | string | — | yes | — | — |
| Application ID | `application_id` | string | — | yes | — | — |
| CMU ID | `cmu_id` | string | — | yes | — | — |
| Delivery Year | `delivery_year` | string | — | yes | — | Year |
| Component ID | `component_id` | string | — | yes | — | — |
| Type | `type` | string | — | yes | — | — |
| Generating Technology Class | `generating_technology_class` | string | — | yes | — | — |
| Permitted On Site Generating Unit | `permitted_on_site_generating_unit` | string | — | yes | — | — |
| Primary Fuel of Component | `primary_fuel_of_component` | string | — | yes | — | — |
| Connection or DSR Capacity | `connection_or_dsr_capacity` | float64 | — | yes | — | MW |
| De Rated Capacity | `de_rated_capacity` | float64 | — | yes | — | MW |
| Pre Refurbishing De Rated Capacity | `pre_refurbishing_de_rated_capacity` | float64 | — | yes | — | MW |
| Post Refurbishing De Rated Capacity | `post_refurbishing_de_rated_capacity` | float64 | — | yes | — | MW |
| Generating Capacity of On Site Generating Unit | `generating_capacity_of_on_site_generating_unit` | float64 | — | yes | — | MW |
| Description of CMU Components | `description_of_cmu_components` | string | — | yes | — | — |
| Location and Post Code | `location_and_post_code` | string | — | yes | — | — |
| OS Grid Reference | `os_grid_reference` | string | — | yes | — | — |
| Number of Components | `number_of_components` | int64 | — | yes | — | — |

- Entity key: `auction_name`, `application_id`, `component_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Column meanings.** The register of the physical components behind each CMU, one row per
auction, application and component. After the 22 July 2026 aggregation, a row can stand
for many small components. The vendor builds an aggregate Component ID from the CMU, the
generating technology and, where it applies, the permitted on-site fuel (dictionary line
70), so it is an aggregate identity, not an original component ID. `Number of Components`
is the count of components the row stands for; rows that are not aggregated have 1
(line 226; vendor aggregation notice). The literal text `Aggregated` in the description,
location and OS grid reference columns is a documented category (lines 190, 202, 214), not
a missing-value marker.

**Units (vendor field dictionary, `field-info/20261008T114228Z/capacity_market_components.json`; K-CI-FACTS §2.13 g4).**
All capacity columns are **MW**: Connection or DSR Capacity (line 130), De Rated Capacity
(142), Pre and Post Refurbishing De Rated Capacity (154, 166), Generating Capacity of On
Site Generating Unit (178). `Number of Components` is an integer count. The other columns
are identifiers, categories, descriptions or spatial-reference text. In the capture,
`Number of Components` ranges from 1 to 60,664, with 29,628 rows equal to 1 and 96
distinct values.

**Two clocks.**
1. **Vintage `ckan_last_modified`:** `published_at` = `available_at` =
   2026-10-07T13:03:44.960185Z.
2. **Event time `none`:** `timestamp_utc` is the capture time, 2026-10-08T09:14:35.042277Z
   on every row. `Delivery Year` is a year label, not a timestamp.

**Identity (K-CI-FACTS §2.13, §3.3 CI-3).** Every row has a CMU ID, but a meaningful
Component ID is not always given.

```text
Component ID alone:                          distinct 11,939; duplicate excess 17,910
(Auction Name, Component ID):                distinct 28,536; duplicate excess  1,313
(Component ID, Delivery Year):               distinct 26,101; duplicate excess  3,748
(Auction Name, Application ID, Component ID): distinct 29,849; duplicate excess      0
```

The last is the guard. Two of its keys have the literal Component ID `N/A`.
- TODO: verify that NESO guarantees stable, unique component identities, and what a
  missing Component ID means.

**Sentinels and nulls (K-CI-FACTS §2.13 g5).**
- Literal `N/A` in Component ID (2 rows), description (221) and location (457). Component
  ID is also the string `000000` on 11 rows. All are kept as written; IDs are never normalised.
- Capacity blanks are common: Connection or DSR Capacity 24,246 blanks, De Rated Capacity
  24,378. They stay null and are never filled with zero.
- TODO: verify, field by field, when a blank capacity means "not applicable" and when it
  means "not available".

**Silver output.** **29,849 rows** from `raw_20261008T091435Z_790f5fa0-…_2d9e9dba.csv`
(8,329,415 bytes); **29,849 rows** from `raw_20261016T192053Z_790f5fa0-…_e67bdb73.csv`
(8,329,645 bytes).

### `capacity_market_de_rating_factors`

- Kind: tabular · archetype: REG · refresh: weekly · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Name | `auction_name` | string | — | yes | — | — |
| Primary Fuel Type | `primary_fuel_type` | string | — | yes | — | — |
| Generating Technology Class | `generating_technology_class` | string | — | yes | — | — |
| De Rating Factor | `de_rating_factor` | float64 | — | yes | — | — |

- Entity key: `auction_name`, `generating_technology_class`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Column meanings.** One de-rating factor per auction and generating technology class.
The dictionary describes it as a multiplier applied to connection capacity to get de-rated
capacity, with a decimal example (`0.915`; dictionary line 58). `Primary Fuel Type` and
`Generating Technology Class` are categories.

**Units.** The dictionary's `unit` field for `De Rating Factor` is blank. The vendor
describes a multiplier between two capacities, so a dimensionless fraction is an
**inference**, not a stated unit. Silver keeps the number as supplied, with no percent
conversion or other rescaling.
- TODO: verify that NESO confirms the factor is a dimensionless fraction (K-CI-FACTS §2.8
  T01, medium confidence).

**Two clocks.**
1. **Vintage `ckan_last_modified`:** `published_at` = `available_at` =
   2026-09-09T11:52:54.749384Z.
2. **Event time `none`:** `timestamp_utc` is the capture time, 2026-10-08T09:14:38.881107Z
   on every row. There is no date column.

**Identity.** `(auction_name, generating_technology_class)` guard: 890 distinct non-missing
pairs, 0 duplicates. `primary_fuel_type` is not needed for uniqueness in this capture.
- TODO: verify that NESO guarantees one stable factor per auction and technology class.

**Sentinels and nulls (K-CI-FACTS §2.8 g5).** No blanks or missing-value markers in the
captured body. Seven factors are numeric zero (none adjacent in file order). They are kept
as values.
- TODO: verify whether a zero factor is a real zero de-rating or a vendor exception.

**Silver output.** **890 rows** from `raw_20261008T091438Z_d94ff98d-…_b8ec6223.csv`
(74,304 bytes).

### `capacity_market_unit_cmu`

- Kind: tabular · archetype: REG · refresh: weekly · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Name | `auction_name` | string | — | yes | — | — |
| Application ID | `application_id` | string | — | yes | — | — |
| CMU ID | `cmu_id` | string | — | yes | — | — |
| Type | `type` | string | — | yes | — | — |
| Auction | `auction` | string | — | yes | — | — |
| Delivery Year | `delivery_year` | string | — | yes | — | Year |
| Name of Applicant | `name_of_applicant` | string | — | yes | — | — |
| Agent Name | `agent_name` | string | — | yes | — | — |
| CM Unit Name | `cm_unit_name` | string | — | yes | — | — |
| Parent Company | `parent_company` | string | — | yes | — | — |
| Secondary Trading Contact_Telephone | `secondary_trading_contact_telephone` | string | — | yes | — | — |
| Secondary Trading Contact_Email | `secondary_trading_contact_email` | string | — | yes | — | — |
| Transmission or Distribution | `transmission_or_distribution` | string | — | yes | — | — |
| CM Unit Type | `cm_unit_type` | string | — | yes | — | — |
| CM Unit Category | `cm_unit_category` | string | — | yes | — | — |
| Primary Fuel Type | `primary_fuel_type` | string | — | yes | — | — |
| CMU Technology | `cmu_technology` | string | — | yes | — | — |
| Storage Facility | `storage_facility` | string | — | yes | — | — |
| Pre Qualification Decision | `pre_qualification_decision` | string | — | yes | — | — |
| Opt Out Status | `opt_out_status` | string | — | yes | — | — |
| Opt Out Reason | `opt_out_reason` | string | — | yes | — | — |
| Maximum Obligation Period | `maximum_obligation_period` | float64 | — | yes | — | Number |
| Unproven DSR | `unproven_dsr` | string | — | yes | — | — |
| New Build Yet to Satisfy FCM | `new_build_yet_to_satisfy_fcm` | string | — | yes | — | — |
| Connection Agreement Deferral Declaration | `connection_agreement_deferral_declaration` | string | — | yes | — | — |
| TEC Deferral | `tec_deferral` | string | — | yes | — | — |
| Amount of Credit Cover | `amount_of_credit_cover` | float64 | — | yes | — | £ |
| Planning Consents Conditions | `planning_consents_conditions` | string | — | yes | — | — |
| Connection or DSR Capacity | `connection_or_dsr_capacity` | float64 | — | yes | — | MW |
| Proven DSR Capacity | `proven_dsr_capacity` | float64 | — | yes | — | MW |
| DSR Bidding Capacity | `dsr_bidding_capacity` | float64 | — | yes | — | MW |
| De Rated Capacity | `de_rated_capacity` | float64 | — | yes | — | MW |
| Pre Refurbishing De Rated Capacity | `pre_refurbishing_de_rated_capacity` | float64 | — | yes | — | MW |
| Post Refurbishing De Rated Capacity | `post_refurbishing_de_rated_capacity` | float64 | — | yes | — | MW |
| Pre Refurbishing CMU Status | `pre_refurbishing_cmu_status` | string | — | yes | — | — |
| Anticipated De Rated Capacity | `anticipated_de_rated_capacity` | float64 | — | yes | — | MW |
| Anticipated Pre Refurbishing De Rated Capacity | `anticipated_pre_refurbishing_de_rated_capacity` | float64 | — | yes | — | MW |
| Anticipated Post Refurbishing De Rated Capacity | `anticipated_post_refurbishing_de_rated_capacity` | float64 | — | yes | — | MW |
| Date of Issue of DSR Test Certificate | `date_of_issue_of_dsr_test_certificate` | date | `%d/%m/%Y` | yes | — | — |
| DSR Test Method | `dsr_test_method` | string | — | yes | — | — |
| CMU confirmed entry into Auction | `cmu_confirmed_entry_into_auction` | string | — | yes | — | — |
| Duration of Capacity Agreement in First Bidding Round | `duration_of_capacity_agreement_in_first_bidding_round` | float64 | — | yes | — | Number |
| Pre Refurbishment Bidding Status | `pre_refurbishment_bidding_status` | string | — | yes | — | — |
| Capacity Agreement Awarded | `capacity_agreement_awarded` | string | — | yes | — | — |
| Duration of Capacity Agreement Awarded | `duration_of_capacity_agreement_awarded` | float64 | — | yes | — | Number |
| Unique Agreement Identifier | `unique_agreement_identifier` | string | — | yes | — | — |
| Registered Holder | `registered_holder` | string | — | yes | — | — |
| Date of Issue of Capacity Agreement | `date_of_issue_of_capacity_agreement` | date | `%d/%m/%Y` | yes | — | — |
| Term of the Capacity Agreement | `term_of_the_capacity_agreement` | float64 | — | yes | — | Number |
| Delivery Years for which Agreement Valid | `delivery_years_for_which_agreement_valid` | string | — | yes | — | — |
| Auction Acquired Capacity Obligation | `auction_acquired_capacity_obligation` | float64 | — | yes | — | MW |
| Is FCM required | `is_fcm_required` | string | — | yes | — | — |
| Date for Financial Commitment Milestone | `date_for_financial_commitment_milestone` | date | `%d/%m/%Y` | yes | — | — |
| Is Connection Agreement required | `is_connection_agreement_required` | string | — | yes | — | — |
| Date for provision of deferred Connection Agreement | `date_for_provision_of_deferred_connection_agreement` | date | `%d/%m/%Y` | yes | — | — |
| Subject to a Minimum Completion Requirement | `subject_to_a_minimum_completion_requirement` | string | — | yes | — | — |
| Subject to Substantial Completion Milestone | `subject_to_substantial_completion_milestone` | string | — | yes | — | — |
| Long Stop Date for the Minimum Completion Requirement | `long_stop_date_for_the_minimum_completion_requirement` | date | `%d/%m/%Y` | yes | — | — |
| Earliest Date SCM is expected to be achieved | `earliest_date_scm_is_expected_to_be_achieved` | date | `%d/%m/%Y` | yes | — | — |
| Latest Date SCM is expected to be achieved | `latest_date_scm_is_expected_to_be_achieved` | date | `%d/%m/%Y` | yes | — | — |
| Is copy of Grid Connection Agreement required | `is_copy_of_grid_connection_agreement_required` | string | — | yes | — | — |
| Date for provision of deferred TEC | `date_for_provision_of_deferred_tec` | string | — | yes | — | — |
| Termination Fee 1 Rate | `termination_fee_1_rate` | string | — | yes | — | £ per MW |
| Termination Fee 2 Rate | `termination_fee_2_rate` | string | — | yes | — | £ per MW |
| Termination Fee 3 Rate | `termination_fee_3_rate` | string | — | yes | — | £ per MW |
| Termination Fee 4 Rate | `termination_fee_4_rate` | string | — | yes | — | £ per MW |
| Termination Fee 5 Rate | `termination_fee_5_rate` | string | — | yes | — | £ per MW |
| Annual Penalty Cap | `annual_penalty_cap` | string | — | yes | — | % |
| Monthly Penalty Cap | `monthly_penalty_cap` | string | — | yes | — | % |
| Legal Name of any Person with a Security Interest | `legal_name_of_any_person_with_a_security_interest` | string | — | yes | — | — |
| Nature of the Security Interest | `nature_of_the_security_interest` | string | — | yes | — | — |
| Capacity Agreement has been Terminated | `capacity_agreement_has_been_terminated` | string | — | yes | — | — |
| Date of Termination of Capacity Agreement | `date_of_termination_of_capacity_agreement` | date | `%d/%m/%Y` | yes | — | — |
| List of Traded Capacity Obligations | `list_of_traded_capacity_obligations` | string | — | yes | — | — |
| Period for which the transfer applies | `period_for_which_the_transfer_applies` | string | — | yes | — | — |
| Capacity obligation Summary | `capacity_obligation_summary` | string | — | yes | — | — |
| Beta Value | `beta_value` | string | — | yes | — | — |
| Has Capacity Agreement been Suspended | `has_capacity_agreement_been_suspended` | string | — | yes | — | — |

- Entity key: `auction_name`, `application_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Column meanings.** One row per application per auction. `Application ID` is
system-generated and combines the application type, delivery year and CMU ID (dictionary
line 34). `CMU ID` is defined by the provider (line 46). `Delivery Year` is the first
delivery year of the auction (line 82). The rest covers the applicant, the unit's type,
fuel and technology, prequalification and opt-out, capacities, credit cover, agreement
award and term, milestones, termination fees, penalty caps, security interests,
termination, traded obligations and suspension.

**Units (vendor field dictionary, `field-info/20261008T114228Z/capacity_market_unit_cmu.json`; K-CI-FACTS §2.9 g4).**
- **MW:** Connection or DSR Capacity (line 358), Proven DSR Capacity (370), DSR Bidding
  Capacity (382), De Rated Capacity (394), Pre and Post Refurbishing De Rated Capacity
  (406, 418), Anticipated De Rated Capacity (442), Anticipated Pre and Post Refurbishing
  De Rated Capacity (454, 466), Auction Acquired Capacity Obligation (622).
- **£:** Amount of Credit Cover (334).
- **Years:** Maximum Obligation Period (274), Duration of Capacity Agreement in First
  Bidding Round (514), Duration of Capacity Agreement Awarded (550), Term of the Capacity
  Agreement (598). The `unit` field says `Number`; the dictionary comments say these are
  lengths in years.
- **£ per MW, kept as text:** Termination Fee 1–5 Rate (766–814).
- **%, kept as text:** Annual and Monthly Penalty Cap (826, 838).
- `Beta Value`: the dictionary says only "Used for Stress Event" (line 934). It is kept as
  text, and all 18,200 cells are blank in this capture.
  - TODO: verify the meaning and unit of `Beta Value`.
- `Delivery Years for which Agreement Valid`, `Period for which the transfer applies` and
  `Capacity obligation Summary` contain intervals but stay text; they do not give a
  single event time.

**Date columns (K-CI-FACTS §2.9 g1).** These are civil dates (no time or zone), parsed
`%d/%m/%Y`. Every non-blank value in each column parsed, and each column has values whose
first part is above 12, which fixes the day-first order:

| Column | Vendor meaning | Dictionary line |
|---|---|---|
| Date of Issue of DSR Test Certificate | Certificate issue date | 478 |
| Date of Issue of Capacity Agreement | Agreement issue date | 586 |
| Date for Financial Commitment Milestone | Latest submission date | 646 |
| Date for provision of deferred Connection Agreement | Latest submission date | 670 |
| Long Stop Date for the Minimum Completion Requirement | Latest submission date | 706 |
| Earliest Date SCM is expected to be achieved | Expected earliest milestone date | 718 |
| Latest Date SCM is expected to be achieved | Expected latest milestone date | 730 |
| Date of Termination of Capacity Agreement | Termination date | 886 |

`Date for provision of deferred TEC` (line 754) stays a **string**. It has only 2 non-blank
values, and neither has a first part above 12, so day-first and month-first cannot be told
apart.
- TODO: verify the date order of `Date for provision of deferred TEC` before casting it.

The "issue" dates are about certificates and agreements, not about when this file was
released. None of these dates is an availability clock.

**Two clocks.**
1. **Vintage `ckan_last_modified`:** `published_at` = `available_at` =
   2026-10-07T13:21:26.523270Z.
2. **Event time `none`:** `timestamp_utc` is the capture time, 2026-10-08T09:14:42.633112Z
   on every row. The date columns above describe different events per row, so none is
   used as event time.

**Identity (K-CI-FACTS §2.9, §3.3 CI-3).** `CMU ID` is present on every row but does not
identify one:

```text
(Auction Name, Application ID): distinct 18,200; duplicate excess   0
CMU ID:                         distinct 13,459; duplicate excess 4,741
(Auction Name, CMU ID):         distinct 18,178; duplicate excess  22
(CMU ID, Delivery Year):        distinct 17,607; duplicate excess 593
```

`(auction_name, application_id)` is the guard.
- TODO: verify that NESO guarantees `Application ID` stays unique and unchanged across
  uploads.

**Sentinels and nulls (K-CI-FACTS §2.9 g5).** Many optional fields are blank. Examples:
Date of Issue of Capacity Agreement 8,883 blanks; Amount of Credit Cover 1,962 blanks and
14,896 zeros; Auction Acquired Capacity Obligation 8,883 blanks and 1,144 zeros. The
dictionary comments allow blanks in some status fields, such as termination and
suspension. Zeros are kept as values; blanks stay null and are never filled with zero.
- TODO: verify, field by field, when a blank means "not applicable", "not available" or a
  zero quantity.

**Silver output.** **18,200 rows**, 78 vendor columns plus 8 engine columns, from
`raw_20261008T091442Z_25a5fa2e-…_9d91a949.csv` (8,762,136 bytes); **18,200 rows** from
`raw_20261016T192058Z_25a5fa2e-…_3ecf866a.csv` (8,762,629 bytes).

### `capacity_market_unit_cmu_history`

- Kind: tabular · archetype: REG · refresh: weekly · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Auction Name | `auction_name` | string | — | yes | — | — |
| Application ID | `application_id` | string | — | yes | — | — |
| CMU ID | `cmu_id` | string | — | yes | — | — |
| Type | `type` | string | — | yes | — | — |
| Delivery Year | `delivery_year` | string | — | yes | — | Year |
| Attribute | `attribute` | string | — | yes | — | — |
| Previous | `previous` | string | — | yes | — | — |
| Latest | `latest` | string | — | yes | — | — |
| Change Type | `change_type` | string | — | yes | — | — |
| Change Date | `change_date` | date | `%Y-%m-%d` | no | — | — |

- Entity key: `auction_name`, `application_id`, `cmu_id`, `type`, `delivery_year`, `attribute`, `previous`, `latest`, `change_type`, `change_date`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`change_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Column meanings.** The week-on-week log of CMU attribute changes. Each row is one changed
attribute of one CMU application: `Previous` is the value last published and `Latest` the
updated value (dictionary lines 94 and 106). `Change Type` marks the kind of change
(values include `First Release`, `New` and `Removed`), and `Change Date` is the date the
change was first reported on the CMR (line 130).

**Contact values.** The CMU's contact columns are logged here too: rows whose `Attribute` is
`Secondary Trading Contact - Email`, `Secondary Trading Contact_Email`, `Secondary Trading
Contact - Telephone` or `Secondary Trading Contact_Telephone` carry email addresses and
telephone numbers in `Previous` and `Latest`. Never print those rows. The same goes for
`Name of Applicant`, `Agent Name`, `Registered Holder`, `Parent Company` and `Legal Name of
any Person with a Security Interest` (a name can be a sole trader's), and, in the component
logs and Components, for `Location and Post Code` and `OS Grid Reference`. Several attributes
appear under two spellings (for example `Connection / DSR Capacity` and `Connection or DSR
Capacity`), so filter on every spelling.

**Units.** `Previous` and `Latest` are mixed-type text whose meaning and unit depend on
`Attribute`; they stay strings, including numeric- and date-looking values. `Delivery
Year` is a year label.

**Two clocks.**
1. **Vintage `ckan_last_modified`:** `published_at` = `available_at` =
   2026-10-07T13:25:45.859603Z.
2. **Event time `date_sp1(change_date)`:** `timestamp_utc` is London midnight of
   `change_date`, in UTC. `change_date` spans 2025-12-10 to 2026-10-07 with 48 distinct
   dates; in silver `timestamp_utc` runs from 2025-12-10T00:00Z (GMT) to
   2026-10-06T23:00Z (BST). It is the reporting date, not a release instant, and the time
   of day is not documented.

**Identity.** Every column is the guard (0 full-row duplicates). 72,166 rows cover 3,821
distinct CMU IDs; a CMU appears in many change rows. The shorter composite `(Auction Name,
Application ID, CMU ID, Attribute, Change Type, Change Date)` was also unique (72,166
distinct, 0 missing), but it is a measurement, not a vendor key.
- TODO: verify whether NESO has a change-event identifier.

**Sentinels and nulls (K-CI-FACTS §2.10 g5).** `Previous` is blank on 32,292 `First Release`
rows and 12,839 `New` rows. `Latest` is blank on 3,535 of the 3,537 `Removed` rows. Most
blanks are therefore the absent side of a change. `Previous`/`Latest` stay text and no
global null rule is applied.
- TODO: verify the exact blank meaning per change type, including the 2 `Removed` rows
  whose `Latest` is not blank.

**Silver output.** **72,166 rows** from `raw_20261008T091446Z_cd034839-…_2ac01092.csv`
(10,930,659 bytes); **72,282 rows** from `raw_20261016T192102Z_cd034839-…_de714a50.csv`
(10,951,069 bytes), `change_date` to 2026-10-14 (49 distinct).

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Weekly

What the captures show so far:
- **Weekly files** (CMU, CMU History, Component History, Components): CKAN `last_modified`
  was 2026-09-30 in the catalogue snapshot and 2026-10-07 at capture, with the filename
  date moving from `20260930` to `20261007`. The 2026-10-16 capture fetched `*_20261014.csv`
  with `last_modified` 2026-10-14. This fits a weekly re-upload.
- **Auction-level files** (Auction Capacity and Cost, Auction Static Data, De-Rating
  Factors): CKAN `last_modified` was 2026-09-09 both in the snapshot and at capture. They
  change less often than weekly.
  - TODO: verify what triggers an update of the auction-level files (for example a new
    auction or prequalification round).
- **Component History - Pre Aggregation:** last modified 2026-07-15 and frozen by the
  vendor's notice.
- TODO: verify the vendor's upload day and time of day. Two weekly captures cannot establish it.
- No scheduled gridflow refresh exists yet (OWNER 457–460), so new captures need a manual
  sweep.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence URL from the catalogue: https://www.neso.energy/data-portal/ngeso-open-licence
(`license_id: ESO`). The CKAN author and maintainer fields are empty; the publishing
organisation is Electricity Market Reform, described as data administered by the EMR
Delivery Body.

## Holds

- none

Detail:
- **Nothing in this package is held.** RULINGS 521 (PROXY-SOURCED seat, 2026-10-09) made
  the eight capacity-market tables eligible. `docs/neso_data_portal/eligibility.md` lists
  all eight families as silver, eligible, `whole_capture` (lines 60–67), and the package as
  eligible with 8 families and 0 held (line 349).
- **The open TODOs on this page do not hold any output.** The safe choices are already in
  the record: unresolved dates and rates stay strings, blanks stay null, IDs and `N/A`
  markers are kept as written, and no unit is rescaled.
- **Held outputs in the same batch** are on the carbon-intensity pages, held on E-SEM
  questions under RULINGS 521: @./national-carbon-intensity-forecast.md,
  @./regional-carbon-intensity-forecast.md, @./country-carbon-intensity-forecast.md and
  @./carbon-intensity-of-balancing-actions.md.
- **Activation.** Merged as PR #88 (`1ceeaab`) under RULINGS 523. Activation, reconcile and
  coverage under RULINGS 524 to 526 (`.planning/v0.22-RESULTS.md` §CI).

## Evidence

All paths are in the gridflow checkout unless noted.
- `.planning/phases/v0.22-K-CI/K-CI-FACTS.md`: §1 inventory and clock rule, §2.6–§2.13
  family facts, §3.3 CI-3 identities and aggregation boundary, §3.5 g1–g5, commands
  C1/C3/C4/C6.
- `.planning/phases/v0.22-K-CI/LIVE-PROBE.md`: seat measurement for the carbon-intensity
  families; nothing in it changes this package.
- `.planning/v0.22-RESULTS.md` §CI: activation receipt and row counts.
- `.planning/RULINGS.md`: 521 and 523–526.
- `src/gridflow/connectors/neso_data_portal/registry/capacity-market-register.json`: the
  registry record.
- `docs/neso_data_portal/eligibility.md`: generated eligibility report.
- `docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`: D-15, naive CKAN time read
  as UTC.
- Vendor field dictionaries:
  `.planning/research/neso-snapshots/field-info/20261008T114228Z/capacity_market_*.json`.
- Catalogue snapshot: `.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json`
  (package description, aggregation notice, resource list).
- Bronze sidecars: `C:/gridflow-data/bronze/neso_data_portal/capacity_market_*/2026/10/08/*.meta.json`
  (capture URLs, `ckan_last_modified`, body sizes).
- Silver: `C:/gridflow-data/silver/neso_data_portal/capacity_market_*/` (row counts, clock
  values, `change_date` spans read with Polars on 2026-10-09).
- Vendor page: https://www.neso.energy/data-portal/capacity-market-register.
- Vendor overview: @../README.md.
