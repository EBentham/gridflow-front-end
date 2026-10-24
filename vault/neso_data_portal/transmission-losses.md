---
source: "neso_data_portal"
package: "transmission-losses"
dataset_keys: ["transmission_losses_financial_year", "transmission_losses_main"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Transmission losses
  summary: >-
    Energy lost on GB's three transmission networks, in TWh, by month and by financial year, as
    NESO measures it after the event.
  facts:
    vendor: "NESO Data Portal, package Transmission Losses: two CSV files"
    cadence: "Monthly file updated monthly, financial-year file annually, NESO says"
    grain: "Each row: one month, or one financial year, of losses"
    history: "Months from April 2013 and years from 2013-14, in NESO's files"
  landscape: power
  what_it_is: >-
    Losses in TWh on the networks of National Grid Electricity Transmission (England and Wales),
    Scottish Power Transmission and Scottish Hydro Electric Transmission, with a GB total. NESO
    monitors them after the event: they turn on where generation runs, chiefly the north-south
    balance. A second file gives NESO's own total for each financial year.
  how_used:
    - The long-run scale and trend of GB transmission losses
    - How losses split between the English and Welsh network and the Scottish networks
  chart:
    type: stacked-area
    silver: neso_data_portal/transmission_losses_main
    time: month_vendor
    time_text: {format: "%b-%y"}
    values:
      - {column: nget, series: nget}
      - {column: spt, series: spt}
      - {column: shetl, series: shetl}
    dedup: {"on": [month_vendor], order_by: capture_written_at}
    aggregation: last
    window: {start: "2013-04-01", end: "2026-07-31"}
    unit: TWh
  chart_view:
    title: Monthly transmission losses by network, April 2013 to July 2026
    caption: >-
      Silver `neso_data_portal/transmission_losses_main`, TWh per month, April 2013 to July 2026.
      August 2026 (0.14 TWh, in the rows below) is left out; NESO does not say it is complete.
    alt: >-
      Stacked area chart from neso_data_portal/transmission_losses_main of monthly transmission
      losses in TWh, April 2013 to July 2026: NGET at the bottom and most of every month, then SPT
      and SHETL. Monthly totals run 0.33 to 0.73 TWh from 2013 to 2019, higher in winter than
      summer. The highest month in the window is 0.97 TWh in January 2023 and the lowest is 0.23
      TWh in March 2022. SPT and SHETL are the two thinner bands on top.
    x_label: NESO's month label; no day boundary stated
    key:
      - {series: shetl, label: SHETL, codes: SHETL, paint: hatch-dots, note: "Scottish Hydro Electric Transmission's network"}
      - {series: spt, label: SPT, codes: SPT, paint: hatch-cross, note: "Scottish Power Transmission's network"}
      - {series: nget, label: NGET, codes: NGET, paint: hatch-lines, note: "National Grid Electricity Transmission: England and Wales"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each file, downloaded whole unless its
      `last_modified` is unchanged.
    commands:
      - {run: gridflow ingest neso_data_portal transmission_losses_main --last 24h, comment: "changed file; swap in either key"}
      - {run: gridflow transform neso_data_portal transmission_losses_main --last 24h, comment: "the capture's date to silver"}
  family:
    slug: transmission-losses
    members:
      - dataset: transmission_losses_main
        differs: "One row per month, labelled like `Apr-13`, with its financial year"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=transmission-losses"
          - "GET https://api.neso.energy/dataset/ec5a1356-f6dd-40a1-b714-dbdad3ed00af/resource/fddc307d-fc5a-458d-809f-2ad9a697b142/download/monthly-losses.csv"
      - dataset: transmission_losses_financial_year
        differs: "One row per financial year (`2013-14`); columns `sum_of_` plus the monthly names, TWh"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=transmission-losses"
          - "GET https://api.neso.energy/dataset/ec5a1356-f6dd-40a1-b714-dbdad3ed00af/resource/c0cd9512-4f8a-468e-8823-7c8238dcb9b9/download/financial-year-losses.csv"
  record:
    select:
      filter:
        - {column: month_vendor, op: in, value: [Aug-19, Aug-20, Aug-21, Aug-22, Aug-23, Aug-24, Aug-25, Aug-26]}
      dedup: {"on": [month_vendor], order_by: capture_written_at}
      order_by: [month_vendor]
      columns: [month_vendor, gb_totals, nget, spt, shetl, financial_year, published_at, timestamp_utc]
    key: [month_vendor]
    caption: "Every August from 2019 to 2026; August 2026 is far below the rest."
    fields:
      month_vendor: "NESO's month label, like `Aug-26`, kept as text; no day boundary or zone stated"
      gb_totals: "NESO's GB total for the month, TWh"
      nget: "England and Wales transmission losses, TWh (National Grid Electricity Transmission)"
      spt: "Scottish Power Transmission system losses, TWh"
      shetl: "Scottish Hydro Electric Transmission system losses, TWh"
      financial_year: "NESO's financial year label; the file puts April to March under each"
      published_at: "NESO's last-modified time for the file, read as UTC; one per capture"
      timestamp_utc: "When gridflow captured the file, UTC; not the month the row describes"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, the capture time here, so these cells use `data.sql()`
      on the `_latest` views: the months in order, then NESO's yearly file as published.
    cells:
      - |
        months = data.sql("""
            SELECT financial_year, month_vendor, nget, spt, shetl, gb_totals
            FROM silver_neso_data_portal_transmission_losses_main_latest
            ORDER BY strptime(month_vendor, '%b-%y')
        """)
        months.tail()
      - |
        years = data.sql("""
            SELECT financial_year, sum_of_nget, sum_of_spt, sum_of_shetl, sum_of_gb_totals
            FROM silver_neso_data_portal_transmission_losses_financial_year_latest
            ORDER BY financial_year
        """)
        years
      - |
        ax = years.plot.bar(x="financial_year", y="sum_of_gb_totals", legend=False,
                            color="#155A6E", figsize=(8, 3.5), xlabel="financial year",
                            ylabel="NESO's GB total, TWh");
    needs: NESO's two transmission losses files
    plot_alt: >-
      Bar chart of NESO's yearly GB transmission losses in TWh, 2013-14 to 2025-26, from its
      financial-year file. 5.23 to 5.65 each year to 2018-19 except 4.85 in 2016-17, the lowest;
      6.51 to 6.87 from 2019-20 to 2021-22; 8.18 in 2022-23, the highest; then 7.15, 7.54 and
      6.85.
  related:
    - {dataset: elexon/fuelhh, note: "Generation by fuel; NESO says where generation runs drives losses"}
    - {dataset: neso_data_portal/historic-demand-data, note: "GB demand by half hour, for scale"}
---

# Transmission Losses

This package gives the energy lost on the GB electricity transmission system. NESO
measures it after the event and publishes it as two small CSV tables. The monthly table
(`transmission_losses_main`) has one row per calendar month from April 2013. The annual table
(`transmission_losses_financial_year`) has one row per financial year from 2013-14. Both
tables split the losses by the three transmission-owner areas, using the vendor dictionary's
names:

- **NGET** (National Grid Electricity Transmission): England and Wales.
- **SPT** (Scottish Power Transmission).
- **SHETL** (Scottish Hydro Electric Transmission).

Both also carry a **GB total**. Every loss value is an energy volume in **TWh**.

The package notes explain what drives losses. They depend on where generation runs, chiefly
the north–south balance and the level of Scottish exports to England and Wales. Interconnector
flows, part-loaded plant, demand and the network's configuration and voltage profile matter
too. NESO says it finds future losses hard to forecast, because most of these factors are
outside its control. It monitors losses after the event. Its notes say other actions may
indirectly lower losses, but it generally does not dispatch plant to minimise them, because
optimising for losses would be likely to raise costs significantly.

Use this package for the long-run scale and trend of transmission losses, or for the split
between the English and Welsh network and the two Scottish networks. The Elexon ITSDO page
suggests losses may be one contributor to a flat gap of about 1–2.2 GW between
transmission-level demand (ITSDO) and FUELHH generation plus net interconnector flow, measured
on 24 July 2026. The cause is unconfirmed there (a TODO on that page)
(@../../elexon/datasets/itsdo.md). The resolution is monthly at best, so this
package cannot give settlement-period losses.

Both families have silver output and **neither is held**. Two cautions apply. The annual table
is **not** an exact sum of the monthly table (see the reconciliation note below). Silver's
`timestamp_utc` is the capture time, not the month or year the row describes.

- Publisher group: Demand
- Registry group: demand · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Financial Year Losses | CSV | upload | `c0cd9512-4f8a-468e-8823-7c8238dcb9b9` |
| Transmission Losses | CSV | upload | `fddc307d-fc5a-458d-809f-2ad9a697b142` |

Download links and the single capture of each resource. The sizes, CKAN `last_modified`
values and filenames come from the capture sidecars under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`. Data rows equal silver rows
(activation receipt, RULINGS 541).

| Resource | Family | File | Bytes | Data rows | CKAN `last_modified` | Captured (`written_at`, UTC) |
|---|---|---|---:|---:|---|---|
| Transmission Losses | `transmission_losses_main` | [monthly-losses.csv](https://api.neso.energy/dataset/ec5a1356-f6dd-40a1-b714-dbdad3ed00af/resource/fddc307d-fc5a-458d-809f-2ad9a697b142/download/monthly-losses.csv) | 6,559 | 161 | 2026-09-25T13:27:36.411183 | 2026-10-08T11:39:37.187111 |
| Financial Year Losses | `transmission_losses_financial_year` | [financial-year-losses.csv](https://api.neso.energy/dataset/ec5a1356-f6dd-40a1-b714-dbdad3ed00af/resource/c0cd9512-4f8a-468e-8823-7c8238dcb9b9/download/financial-year-losses.csv) | 763 | 13 | 2026-06-04T09:14:02.612393 | 2026-10-08T11:39:33.612377 |

The bronze filenames are
`raw_20261008T113937Z_fddc307d-fc5a-458d-809f-2ad9a697b142_ced65f50.csv` (monthly) and
`raw_20261008T113933Z_c0cd9512-4f8a-468e-8823-7c8238dcb9b9_bd49c7bd.csv` (annual). Each body's
SHA-256 matches its sidecar (gridflow
`@.planning/phases/v0.22-K-DEM-2/K-DEM-2-FACTS.md` §1, C-M). Both resources are CKAN
datastore-active in the 2026-10-06 catalogue snapshot. gridflow captures the uploaded file,
not the datastore. The package has only these two resources: no DOC resources and no `_files`
family (FACTS §1).

## Families

### `transmission_losses_financial_year`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Financial Year | `financial_year` | string | — | yes | — | — |
| Sum of NGET | `sum_of_nget` | float64 | — | yes | — | TWh |
| Sum of SPT | `sum_of_spt` | float64 | — | yes | — | TWh |
| Sum of SHETL | `sum_of_shetl` | float64 | — | yes | — | TWh |
| Sum of GB totals | `sum_of_gb_totals` | float64 | — | yes | — | TWh |

- Entity key: `financial_year`, `sum_of_nget`, `sum_of_spt`, `sum_of_shetl`, `sum_of_gb_totals`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What a row is.** One row per financial year: 13 rows and 13 distinct labels, from `2013-14`
to `2025-26`, in the form `YYYY-YY`. The resource description calls these the "Financial Year
Losses for the transmission system", updated annually. Each loss column's dictionary
description reads "… losses for the financial year in question". The monthly rows that share
an FY label are April to March of that year, with no mismatches (FACTS §7, C-S). That shows how
the rows are grouped. It does not give a timezone or a timestamp for the year.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file, 2026-06-04T09:14:02.612393. CKAN emits it without an
   offset, and gridflow reads it as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). Silver was checked on
   2026-10-09: all 13 rows carry that one value, with `available_at = published_at`. There is
   no issue time (issue recipe `none`).
   - The vintage says when the **file** last changed, not when any year's figure was first
     published. A point-in-time query (`available_at <= as_of`) with an as-of before
     2026-06-04 sees no annual rows.
   - Accepted residual (ADR-039 FM-12): the file changed on 2026-06-04 but was captured on
     2026-10-08. So `available_at <= as_of` does not prove the bytes gridflow holds are the
     ones published at that instant. An earlier version may have been overwritten before
     capture.
2. **Event time (temporal recipe `none`).** `timestamp_utc` and `event_time` are both the
   **capture time** (2026-10-08T11:39:33.612377 UTC on every row). They are **not** the
   financial year the row describes. The year lives only in `financial_year`, as text.
   NESO's label gives no start instant or timezone for a financial year, so gridflow does not
   invent one (FACTS §7 T01; gridflow
   `@docs/DECISION_LOG/ADR-036-neso-profiler-and-pilot-records.md`). `TODO: verify` the
   vendor's financial-year boundary convention (start instant and zone) before building an
   annual time axis from the label.

**Units (vendor dictionary only).** All four loss columns are **TWh**. That is the `unit` of
each field in the saved `datastore_search` dictionary (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/transmission_losses_financial_year.json`
lines 31, 43, 55, 67; FACTS §7, g4). These are energy volumes, not percentages or MW. Convert
them before relabelling. `Financial Year` has an empty unit: it is a category.

**Sentinels and missing values (FACTS g5).** The full body has no blanks, `-1`, `NA`, `N/A` or
zero loss values, and no zero runs. Silver has zero nulls in every column. The record declares
no null-token map, and none is needed.

**Identity.** The entity key is every column. It is a conservative within-capture duplicate
guard, not a vendor identity (FACTS §1, §7 T02). `financial_year` alone is unique in the full
body (13 of 13). `TODO: verify` that NESO guarantees one row per financial year; only then
could the key shrink to `financial_year`. `_latest` is `whole_capture`: the newest complete
capture replaces the whole table. A value NESO revises in a later upload arrives as a new
capture, not as a key collision.

**Published GB total.** `Sum of GB totals` equals the sum of the three owner columns in 8 rows
and differs in 5, by at most 0.004 TWh (FACTS §7, C-S). Use the published total; do not
recompute it.

### `transmission_losses_main`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Financial Year | `financial_year` | string | — | yes | — | — |
| Month | `month_vendor` | string | — | yes | — | — |
| NGET | `nget` | float64 | — | yes | — | TWh |
| SPT | `spt` | float64 | — | yes | — | TWh |
| SHETL | `shetl` | float64 | — | yes | — | TWh |
| GB totals | `gb_totals` | float64 | — | yes | — | TWh |

- Entity key: `financial_year`, `month_vendor`, `nget`, `spt`, `shetl`, `gb_totals`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What a row is.** One row per calendar month: 161 rows and 161 distinct `Month` labels, from
`Apr-13` to `Aug-26` (labels in the form `%b-%y`). They fall under 14 `Financial Year` labels,
`2013-14` to `2026-27`. Each complete year has 12 months; `2026-27` has 5 so far (April to
August 2026). The newest month, `Aug-26`, has a GB total of 0.1412 TWh, below every earlier
month (the next lowest is `Mar-22`, 0.234) and every earlier August (0.349 to 0.628), in a file
last modified 2026-09-25 (silver, 2026-10-24). NESO does not say whether its newest month is
complete. `TODO: verify` whether `Aug-26` is a part-month that a later upload fills in. The
resource description says the file holds "monthly volumes of transmission losses" for the
three transmission systems, updated monthly. There is no region-code column:
the areas are the column headings. Do not read them as GSP or DNO codes (FACTS §6).

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file, 2026-09-25T13:27:36.411183, read as UTC (ADR-030).
   Silver was checked on 2026-10-09: all 161 rows carry that one value, with
   `available_at = published_at`. There is no issue time (issue recipe `none`).
   - As with the annual table, the vintage is the file's last change, not each month's first
     publication. An as-of before 2026-09-25 sees no monthly rows.
   - The two families have different vintages. An as-of between 2026-06-04 and 2026-09-25 sees
     the annual table but no monthly rows; an as-of before 2026-06-04 sees neither.
   - The ADR-039 FM-12 residual applies here too: the file changed on 2026-09-25 and was
     captured on 2026-10-08.
2. **Event time (temporal recipe `none`).** `timestamp_utc` and `event_time` are both the
   **capture time** (2026-10-08T11:39:37.187111 UTC on every row). They are **not** the month
   the row describes. The month lives only in `month_vendor`, kept as the vendor's text label
   (for example `Apr-13`). `%b-%y` parses the label, but it does not prove that the month
   starts at a first-day midnight in any particular zone. Casting it to a date would invent a
   day (FACTS §6 T01). `TODO: verify` the vendor's month boundary convention (start instant and
   zone) before building a monthly time axis from the label. The site page's chart is the one
   exception: to draw its axis it places each month at the first day of its label (`time_text`
   `%b-%y`), for the chart only, and its x label says NESO states no day boundary. Silver keeps
   the label as text, and the boundary and zone stay unverified.

**Units (vendor dictionary only).** `NGET`, `SPT`, `SHETL` and `GB totals` are all **TWh**, the
`unit` of each field in the saved dictionary (gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/transmission_losses_main.json`
lines 43, 55, 67, 79; FACTS §6, g4). The dictionary describes them as:

- `NGET`: England and Wales transmission system losses.
- `SPT`: Scottish Power Transmission system losses.
- `SHETL`: Scottish Hydro Electric Transmission system losses.
- `GB totals`: Great Britain transmission system losses.

These are energy volumes, not percentages or MWh-valued fields. `Financial Year` and `Month`
have empty units.

**Sentinels and missing values (FACTS g5).** The full body has no blanks, `-1`, `NA`, `N/A` or
zero loss values, and no zero runs. Silver has zero nulls in every column. The record declares
no null-token map.

**Identity.** The entity key is every column, as a conservative within-capture duplicate guard
(FACTS §6 T02). `month_vendor` alone is unique in the full body (161 of 161). `TODO: verify`
that NESO guarantees one row per month. `_latest` is `whole_capture`, so each new upload
replaces the whole table.

**Published GB total.** `GB totals` equals the sum of the three owner columns in 98 rows and
differs in 63, by at most 0.001 TWh (FACTS §6, C-S). Use the published total; do not recompute
it.

**Monthly versus annual: the tables do not reconcile exactly.** Both tables give the same
owner and GB measures, but the annual figures are **not** the sum of the captured monthly
figures. Every financial year with an annual row has 12 monthly rows, and there are no
annual-only years. Yet only 2 corresponding cells match exactly, and no year matches in every
column (FACTS §7, C-B/C-S, decimal arithmetic on the raw CSV values). Annual minus summed
monthly, in TWh:

| FY | NGET | SPT | SHETL | GB total |
|---|---:|---:|---:|---:|
| `2013-14` | 0.000393018 | 0.000059964 | -0.000027723 | -0.001574741 |
| `2014-15` | -0.00013459 | -0.000904788 | -0.000487193 | -0.000526571 |
| `2015-16` | 0.000267205 | -0.002292489 | 0.00068866 | -0.001336624 |
| `2016-17` | -0.00073254 | 0.002273472 | -0.001229831 | 0.001311101 |
| `2017-18` | -0.000878946 | 0.000615226 | 0.000050965 | -0.002212755 |
| `2018-19` | -0.000448961 | -0.000737883 | 0.001423194 | 0.00023635 |
| `2019-20` | 0.0003089 | -0.0018271 | -0.0017818 | -0.0003 |
| `2020-21` | 0.00193263 | 0.00045636 | -0.000265283 | 0.000123707 |
| `2021-22` | -0.065716232 | 0.018140504 | -0.001894488 | -0.048470215 |
| `2022-23` | 0.175071677 | 0.030474991 | 0.016976308 | 0.221522977 |
| `2023-24` | 0.001 | 0.000 | 0.001 | 0.000 |
| `2024-25` | 0.0262 | 0.0033 | 0.0019 | 0.0316 |
| `2025-26` | -0.0063 | -0.0009 | -0.0003 | -0.0076 |

Most years differ by thousandths of a TWh, but 2021-22 and 2022-23 differ by much more. For
example, the 2022-23 monthly GB losses sum to 7.954 TWh, while the annual table reports
8.175522977 TWh. The five `2026-27` monthly rows have no annual counterpart yet.

`TODO: verify` the reconciliation method: why NESO's annual figures differ from the monthly
sums (revisions, precision, or different calculation inputs). Until NESO documents it:

- do not call the differences rounding;
- do not derive one table from the other;
- do not substitute one table's values for the other's.

Both native tables are kept as published.

**Implementation delta (vendor dictionary vs record).**

- The dictionary types `Financial Year` as `year` and `Month` as `yearmonth`. The physical
  datastore type of both is `text`. The record keeps both as `string`, because no instant or
  zone is evidenced (FACTS §6–7 T01). A profiler proposal to cast `Month` to a date was not
  adopted; it would have invented a day. (The site chart's first-day placement is drawing only;
  see the monthly family's event-time item.)
- The dictionary types the loss fields `numeric`. The record casts them to nullable `float64`.
- The dictionary describes `GB totals` as Great Britain losses. The published total does not
  always equal the sum of the owner columns (see "Published GB total" above).

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Monthly

The package extra says monthly. The monthly resource's description agrees ("updated on a
monthly basis"). The annual resource's description says it is "updated on an annual basis",
but the registry refreshes it monthly along with the rest of the package.

At the 2026-10-08 capture, the monthly file ran to `Aug-26` and was last modified on
2026-09-25. That suggests a lag of about a month. The annual file was last modified on
2026-06-04, two months after 2025-26 ended. `TODO: verify` the publication lag and day of month
for both files, and whether a monthly upload also revises earlier months. Only more captures,
compared pair by pair, can show this; one capture of each resource exists to date. The
package notes give no update time.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- none

Both families are eligible and unheld. RULINGS 538 ruled them eligible in the
demand-reference batch, and RULINGS 541 recorded the activation on 2026-10-09 with cutoff
2026-10-08: `transmission_losses_main` 161 rows and `transmission_losses_financial_year` 13
rows, both as planned. No prior silver existed and nothing was overwritten. Reconcile across
all families reported 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` "DEM-2").

The open `TODO: verify` items above are open questions, not holds:

- the month and financial-year boundary conventions;
- vendor uniqueness of the month and year labels;
- the monthly-versus-annual reconciliation method;
- the publication lag.

None of them changes a published value. Each limits how the data may be joined or derived:
do not treat either label as an instant in any zone or join on it as one (the site chart's
first-day placement draws an axis only), and do not derive one table from the other.
