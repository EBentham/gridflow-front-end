---
source: "neso_data_portal"
package: "short-term-operating-reserve-stor-day-ahead-auction-results"
dataset_key: "stor_da_auction_results"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: STOR day-ahead auction results
  summary: >-
    The tenders in NESO's daily Short Term Operating Reserve (STOR) auction: MW and price offered,
    accepted or rejected, and the clearing price.
  facts:
    vendor: "NESO Data Portal: one uploaded CSV of the daily STOR auction results"
    cadence: "Daily; last auction 30 March 2026, for delivery 31 March; package Not Active (NESO)"
    grain: "One row per tender: a unit's MW and price for one service day"
    history: "Service days 1 April 2021 to 31 March 2026; NESO's file lacks four"
  landscape: market
  what_it_is: >-
    Each row is one tender in NESO's daily day-ahead STOR auction: a unit's MW for a service day's
    availability windows, its availability price and the outcome. Accepted rows add contracted MW and
    clearing price; rejected rows leave both null. NESO's file has no rows for four service days and
    none accepted on five; NESO's notices report two failed auctions.
  how_used:
    - "Daily clearing price, £/MW/h, as STOR availability revenue history, 2021 to 2026"
    - "Each day's merit order: tendered price against outcome, by unit, fuel and company"
    - "Contracted MW per day, set against the buy curve its `buy_curve_id` names"
  chart:
    type: line
    silver: neso_data_portal/stor_da_auction_results
    time: service_delivery_from
    value: market_clearing_price
    filter:
      - {column: status, op: eq, value: Accepted}
    aggregation: max
    time_bucket: 1d
    window: {start: "2025-04-01", end: "2026-03-31"}
    unit: "£/MW/h"
  chart_view:
    title: Clearing price per service day, April 2025 to March 2026
    caption: >-
      Silver `stor_da_auction_results`, `market_clearing_price` in £/MW/h (NESO writes £/MW/Hr): each
      service day's clearing price, the same on every accepted tender that day in NESO's file, 1 April
      2025 to 31 March 2026, the auction's final year.
    alt: >-
      Line chart from neso_data_portal/stor_da_auction_results of the STOR day-ahead clearing price
      per service day, £/MW/h, 1 April 2025 to 31 March 2026, 365 days. It stays under 5 from April
      to June, lowest 0.22 on 1 April, climbs through the summer to 20.48 on 30 September and 21.00
      on 16 October, the highest, runs 1.44 to 20.00 from November to February, and falls to 0.72 to
      6.50 in March.
    x_label: service day, starting 05:00 UK time
    key:
      - {series: market_clearing_price, label: Clearing price, paint: petrol, note: "Highest 21.00 on 16 October 2025, lowest 0.22 on 1 April 2025; median 3.70."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the one CSV downloaded whole unless its
      `last_modified` is unchanged. Its last upload is dated 30 March 2026.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=short-term-operating-reserve-stor-day-ahead-auction-results"
      - "GET https://api.neso.energy/dataset/fb4a9900-9438-47ae-9788-06f490353a89/resource/844a1a65-0a3c-4704-b327-d1685d0c397b/download/stor-da-auction-results.csv"
    commands:
      - {run: gridflow ingest neso_data_portal stor_da_auction_results --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal stor_da_auction_results --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: service_delivery_from, op: eq, value: "2023-11-23T05:00:00Z"}
        - {column: unit_id, op: in, value: [KILLPG-1, SOLUU-1, DIDC03G, SEEL-1, SEVIU-1, DIDC04G, BRIDU-1, LBAR-1G]}
      order_by: [tendered_availability_price, status, unit_id]
      columns: [unit_id, status, tendered_availability_price, market_clearing_price, tendered_mw,
                minimum_acceptable_mw, contracted_mw, service_delivery_from, service_delivery_to, fuel_type,
                bm_nbm, company_name, tender_submission_id, tender_round_id, buy_curve_id]
    key: [tender_submission_id]
    caption: "Service day 23 November 2023 around its 0.30 clearing price; `SEEL-1` was partly accepted."
    fields:
      tender_submission_id: "NESO's unique id for the tender, `TS-` and a number"
      unit_id: "The unit tendered, NESO's id as written; null where NESO leaves it blank"
      status: "`Accepted` or `Rejected`: NESO's outcome for the tender"
      tendered_availability_price: "Availability price the provider tendered, £/MW/h (NESO's unit)"
      market_clearing_price: "Availability price NESO offered an accepted tender, £/MW/h; null if rejected"
      tendered_mw: "MW offered for the service day's availability windows (NESO)"
      minimum_acceptable_mw: "Minimum acceptable MW, by NESO's column name; its dictionary entry is blank"
      contracted_mw: "MW NESO accepted for the windows; null if rejected"
      service_delivery_from: "Service day start, UTC with NESO's `Z`: 05:00 UK time, so 04:00Z in summer"
      service_delivery_to: "Service day end, 05:00 UK time; 23 or 25 hours long at clock changes"
      fuel_type: "The unit's fuel type as NESO writes it"
      bm_nbm: "`BM` for a Balancing Mechanism unit, `NBM` for a non-BM unit (NESO)"
      company_name: "The STOR provider, which NESO says holds a framework agreement"
      tender_round_id: "NESO's id for the tender round, `TRN-` and a number"
      buy_curve_id: "NESO's id for a buy curve, as in its STOR buy-curve package"
      service_name: "Always `Short Term Operating Reserve`, NESO's dictionary says"
      timestamp_utc: "Equals `service_delivery_from`: the service day's start, UTC"
      published_at: "NESO's last-modified time for the whole file, read as UTC; not the auction time"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads the `_latest` view, filtering `timestamp_utc` (the service day's start) with both
      dates included. Times come back in the session's zone; the query cell converts them to UTC.
    cells:
      - |
        import pandas as pd
        df = data.neso_data_portal.query("stor_da_auction_results", "2021-04-01", "2026-03-31")
        for col in ["service_delivery_from", "service_delivery_to", "timestamp_utc"]:
            df[col] = df[col].dt.tz_convert("UTC")
        uk = df.service_delivery_from.dt.tz_convert("Europe/London")
        df["day"] = pd.to_datetime(uk.dt.date)
        pd.DataFrame({"uk_start": uk.dt.strftime("%H:%M"),
            "hours": (df.service_delivery_to - df.service_delivery_from) / pd.Timedelta(hours=1),
        }).value_counts().rename("rows").reset_index()
      - |
        acc = df[df.status == "Accepted"]
        days = acc.groupby("day").agg(clearing=("market_clearing_price", "max"),
            prices=("market_clearing_price", "nunique"),
            dearest_accepted=("tendered_availability_price", "max"),
            contracted_mw=("contracted_mw", "sum"))
        span = pd.date_range("2021-04-01", "2026-03-31")
        pd.Series({"service days in the span": len(span), "with rows in the file": df.day.nunique(),
            "with a tender accepted": len(days), "one clearing price": (days.prices == 1).sum(),
            "clearing = dearest accepted": (days.clearing == days.dearest_accepted).sum()})
      - |
        start = days.index.year - (days.index.month < 4)
        year = [f"{y}-{(y + 1) % 100:02d}" for y in start]
        days.groupby(year).agg(days=("clearing", "size"),
            median_price=("clearing", "median"), top_price=("clearing", "max"),
            mean_contracted_mw=("contracted_mw", "mean")).round(2).rename_axis("year").reset_index()
      - |
        days = days.reindex(span)
        ax = days.contracted_mw.plot(figsize=(8, 3.5), color="#155A6E",
            xlabel="service day, starting 05:00 UK time", ylabel="MW contracted");
    needs: a capture of the results file
    plot_alt: >-
      Line plot of MW contracted per STOR service day, 1 April 2021 to 31 March 2026. Median 1,312 MW
      until 1 April 2025, then 1,696 from 2 April, when NESO's notice raised its requirement to 1,700
      MW. Lowest 50 MW on 20 December 2021; the line breaks where nothing was accepted or NESO's file
      has no rows.
  related:
    - {dataset: neso_data_portal/short-term-operating-reserve-stor-day-ahead-buy-curve, note: "NESO's buy curve for each day's assessment, named by `buy_curve_id`"}
    - {dataset: neso_data_portal/stor-windows, note: "Committed windows for each STOR service day, where STOR must be provided"}
    - {dataset: neso_data_portal/as_industry_notifications_stor_important, note: "Mostly STOR auction delays and failures; two explain gaps in these results"}
    - {dataset: neso_data_portal/eac-auction-results, note: "Slow Reserve auctions; NESO ended STOR day-ahead after launching them"}
---

# Short Term Operating Reserve (STOR) Day Ahead Auction Results

This package is NESO's **result record of the daily Short Term Operating Reserve (STOR) day-ahead auction**.
The vendor's package text says that, as part of Clean Energy Package (CEP) 6.9, NESO runs a daily auction
for the procurement of STOR and that the daily results are published here (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[STOR day-ahead auction results](https://www.neso.energy/data-portal/short-term-operating-reserve-stor-day-ahead-auction-results)).
STOR is a reserve service: a provider tenders MW of capacity that it can make available for the
applicable availability windows of an operational day, and NESO contracts the accepted tenders at a
market clearing availability price. The table answers: who tendered what capacity at what availability
price for which service day, which tenders the auction accepted, how many MW were contracted, and at what
clearing price. For a model it is the **price-and-volume outcome of the STOR availability market**: the
daily clearing price (£/MW/h) is the target, contracted MW the cleared volume, and the unit and fuel
columns give the provider mix. It is a record of **auction outcomes already known**, not a forecast.

**One row is one tender submission for one operational service day.** The vendor defines `Tender
Submission ID` as the unique identifier generated for a tender submission (dictionary entry in
@.planning/research/neso-snapshots/field-info/20261008T114228Z/stor_da_auction_results.json). It is
non-blank and unique across all 121,480 rows (K-AS-5 FACTS, package STOR section), so it is the entity
key. `(Tender Round ID, Unit ID)` also measures unique, but `Unit ID` is blank in 55 rows, so it is not
used. There is **no EFA-block, window or settlement-period column**: the service-day bounds span the whole
operational day, and NESO's STOR guidance says a daily tender covers the applicable availability windows
([STOR service-day guidance](https://www.neso.energy/document/209016/download)). The table is therefore
**not** one row per committed window, and it carries no `run_type`.

**What this package is not.**

- It is **not a window-award table.** To see which committed windows applied on a service day, join the
  reference calendar @./stor-windows.md **on the local delivery date** (the Europe/London date of the
  service day, derived explicitly from the literal UTC instant). That join enriches a service-day row with
  window context; it must never be read as independent awards per window. gridflow provides **no silver
  join** between the two (seat ruling 11 in @.planning/phases/v0.22-K-AS-5/K-AS-5b-SPEC.md); this is a
  consumer-side join.
- It is **not the day-ahead buy curve.** The buy curves are the neighbouring package
  `short-term-operating-reserve-stor-day-ahead-buy-curve` (separate record; `Buy Curve ID` here is only a
  pointer to a curve).
- It is **not a forecast** and carries no issue time (`issue: none`).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| STOR DA Auction Results | CSV | upload | `844a1a65-0a3c-4704-b327-d1685d0c397b` |

This is the package's only resource and it is a CSV upload (served from
[stor-da-auction-results.csv](https://api.neso.energy/dataset/fb4a9900-9438-47ae-9788-06f490353a89/resource/844a1a65-0a3c-4704-b327-d1685d0c397b/download/stor-da-auction-results.csv);
snapshot `last_modified` `2026-03-30T04:28:01.703705`, created `2021-03-31T04:34:03.200882`). There are
**no DOC files** and no held resources in this package. The captured body is 21,263,175 bytes, UTF-8,
CRLF line endings, no BOM, one header and 121,480 data rows, none blank.

## Families

### `stor_da_auction_results`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Service Name | `service_name` | string | — | yes | — | — |
| Tender Round ID | `tender_round_id` | string | — | yes | — | — |
| Buy Curve ID | `buy_curve_id` | string | — | yes | — | — |
| Tender Submission ID | `tender_submission_id` | string | — | no | — | — |
| Service Delivery From | `service_delivery_from` | datetime | `%Y-%m-%d %H:%M:%SZ` | no | UTC | — |
| Service Delivery To | `service_delivery_to` | datetime | `%Y-%m-%d %H:%M:%SZ` | yes | UTC | — |
| Unit ID | `unit_id` | string | — | yes | — | — |
| Company Name | `company_name` | string | — | yes | — | — |
| BM/NBM | `bm_nbm` | string | — | yes | — | — |
| Fuel Type | `fuel_type` | string | — | yes | — | — |
| Tendered MW | `tendered_mw` | float64 | — | yes | — | MW |
| Minimum Acceptable MW | `minimum_acceptable_mw` | float64 | — | yes | — | — |
| Contracted MW | `contracted_mw` | float64 | — | yes | — | MW |
| Tendered Availability Price | `tendered_availability_price` | float64 | — | yes | — | £/MW/Hr |
| Market Clearing Price | `market_clearing_price` | float64 | — | yes | — | £/MW/Hr |
| Status | `status` | string | — | yes | — | — |

- Entity key: `tender_submission_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`service_delivery_from`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks.**

- **Vintage (`ckan_last_modified`).** `available_at` is the CKAN `last_modified` of the captured upload,
  `2026-03-30T04:28:01.703705` for the single capture. It is the **upload time of the file, not the time
  the auction ran**: there is no submission or publication timestamp in the body, and no evidence supports
  an earlier original availability, so the whole 2021 to 2026 history carries one 2026 `available_at`
  (`TODO: verify` the original publication instant of each daily result). The same vintage applies to
  every row; a point-in-time backtest cannot use this table to say when a past result became known.
- **Event time (`utc_instant(service_delivery_from)`).** `timestamp_utc` and `event_time` equal
  `service_delivery_from`, the start of the service day, taken from the literal `Z`. This is a real UTC
  instant: every start and end converts to 05:00 Europe/London on all 121,480 rows (a literal
  04:00 UTC in summer time, 05:00 UTC in winter), so the `Z` agrees with the documented local operational
  day and is not a relabelled local clock (K-AS-5 FACTS clock check C12; seat ruling 10).

**Vendor dictionary versus body.** The dictionary comment for both delivery columns says the format is
`DD/MM/YYYY HH:MM` (example `13/02/2021 05:00`); the served cells are ISO strings with a literal `Z`
(`%Y-%m-%d %H:%M:%SZ`). The body is the authority for parsing; the layout difference is recorded, not
reconciled. The dictionary also gives `Service Name` as always `Short Term Operating Reserve` (a single
distinct value in the silver).

**Units (vendor dictionary only, never inferred from a column name).**

| Silver column | Unit | Source |
|---|---|---|
| `tendered_mw` | MW | dictionary unit entry |
| `contracted_mw` | MW | dictionary unit entry |
| `minimum_acceptable_mw` | MW | the dictionary unit entry is **blank**; the unit comes from the vendor column header "Minimum Acceptable MW" (FACTS: units section) |
| `tendered_availability_price` | £/MW/Hr | dictionary unit entry |
| `market_clearing_price` | £/MW/Hr | dictionary unit entry; the comment says the price is limited to two decimals |

The price unit is the vendor's own £/MW/Hr (an availability price per MW per hour). No conversion or
rescaling is applied, and no MW-to-energy conversion is stated. Identifier columns (`tender_round_id`
format `TRN-XXXX`, `buy_curve_id` format `BCN-XXXXXXXX`, `tender_submission_id` format `TS-XXXXXX`)
and `unit_id` (NGT unit id, stored as served), `company_name`, `bm_nbm`, `fuel_type` carry no unit.
`bm_nbm` takes the values `BM` and `NBM`; `status` takes the values `Accepted` and `Rejected`.

**Typing and sentinels (K-AS-5 FACTS g5, g6).** There is no sentinel token: no `NA`/`N/A`, no negative
numeric value, no thousands separator was observed, and the production CSV reader agreed with a strict
second parse on every row and cell. Blanks stay null and **zeros stay zero**:

| Column | Blank cells (null) |
|---|---:|
| `buy_curve_id` | 328 |
| `unit_id` | 55 |
| `minimum_acceptable_mw` | 243 |
| `contracted_mw` | 58,171 |
| `tendered_availability_price` | 3 |
| `market_clearing_price` | 58,171 |

- **Rejected rows keep null `contracted_mw` and `market_clearing_price`, never zero.** All 58,171
  `Rejected` rows have both null, and no `Accepted` row has a null contracted MW (silver check). A
  consumer must not fill the rejected results with 0: a zero contracted volume and a missing outcome are
  different facts.
- `minimum_acceptable_mw` contains 80 real zeros (maximum zero run 2). They are values, not missing data.

**Service-day length.** Because the service day is the local 05:00 to 05:00 day, its UTC length varies
with clock changes: 120,803 rows span 24 hours, 364 span 23 hours and 313 span 25 hours; no row fails the
local-boundary check. `service_delivery_from` runs `2021-04-01 04:00:00Z` to `2026-03-31 04:00:00Z`,
`service_delivery_to` to `2026-04-01 04:00:00Z`, matching the `stor_windows` calendar span
(`2021-04-01` to `2026-03-31` by local delivery date). `TODO: verify` interval closure: no source states
whether the end instant belongs to the service day.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Not Active

The vendor marks the package "Not Active" and the last service day in the body is 2026-03-31, so the
record is treated as frozen. The package `metadata_modified` is `2026-10-05T11:42:08.113997`.
Publication does not resume: the sibling buy-curve package's `notes` say STOR DA "has been officially
decommissioned following the launch of the new Slow Reserve service in EAC" and that "the final STOR DA
tender was run on 30th March" (catalogue snapshot `20261006T195819Z`, package
`short-term-operating-reserve-stor-day-ahead-buy-curve`); this package's one resource is described as
"STOR DA Auction Results for 30/03/2026".

## Licence and attribution

- Licence: NESO Open Data Licence ([licence text](https://www.neso.energy/data-portal/ngeso-open-licence))
- Attribution: Supported by National Energy SO Open Data

gridflow outputs derived from this package carry the attribution line "Supported by National Energy SO
Open Data".

## Holds

- none

**No resource and no output of this package is held.** The family was specified as eligible at
`utc_instant(service_delivery_from)` with a whole-capture latest policy, so there is no hold question or
hold unit to state (K-AS-5b-SPEC, seat ruling 10; RULINGS 766 ratified, 789 merge). The sibling AS-5b
packages (the ASDP window prices and the ODFM load factors) carry holds; none applies here.

**Open questions that do not hold any output** (K-AS-5 FACTS, carried as non-holding TODOs):

- `TODO: verify` the **original publication instant** of each daily result (see the vintage clock above).
- `TODO: verify` **interval closure** of the service day.
- Publication **does not resume**: NESO decommissioned STOR DA after launching Slow Reserve in EAC, final
  tender 30 March 2026 (see Cadence).
- `TODO: verify` the **unit of `Minimum Acceptable MW`** from a dictionary entry; the dictionary unit
  field is blank and MW rests on the vendor header only.

## Known issues and gotchas

- **Service-day rows, not window awards.** Join @./stor-windows.md on the local delivery date only, and
  only for window context; never treat the join as window-level awards or split the row by window.
- **Derive the local date explicitly.** `service_delivery_from` is 04:00 or 05:00 UTC; the Europe/London
  date of that instant is the delivery date. Do not take the UTC date and do not synthesise timestamps
  from the date.
- **Rejected rows have no outcome.** Null `contracted_mw` and `market_clearing_price` mean the tender was
  not accepted; do not average prices or sum MW as if zeros were present, and do not read null as zero.
- **One `available_at` for all history.** The vintage is the upload time of the file, so the full
  2021 to 2026 history shares a single 2026 `available_at`; do not use it for point-in-time claims.
- **Blank `Unit ID`.** 55 rows have no unit id; key on `tender_submission_id`, not on `(tender_round_id,
  unit_id)`.
- **Identifiers are strings stored as served**: `unit_id`, `tender_round_id`, `buy_curve_id` and the
  submission id are never normalised or cast. The dictionary examples contain trailing tab characters;
  the body values were compared as served, and no served cell carries a tab or a padding space (the
  2026-10-08 capture's raw bytes: no tab, no space beside a comma).
- **Dictionary layout differs from the body** for the delivery timestamps (see above); parse the body
  layout.
- **Size.** The body is 21 MB and the transform is the largest of the batch (peak working set
  735.7 MiB); run it alone.

**Activation (2026-10-13, master `493f9a6`, PR #119).** The AS-5b batch (ASDP, ODFM and this package)
merged triple-green (RULINGS 789: CI green, Sol diff review APPROVE on the first pass, verification
passed) and was activated from the 2026-10-08 capture with `--start/--end 2026-10-08`, with no prior
silver so nothing was overwritten (RULINGS 792). `stor_da_auction_results` produced **121,480 silver rows**,
equal to the spec plan, with 0 recorded failures and 0 excluded rows (batch total 235,148; peak 735.7 MiB
for this family). The batch-wide `reconcile --all --cutoff 2026-10-13` exited 0 over 218 families with 0
gaps. The receipt is in @.planning/v0.22-RESULTS.md section AS-5b; the evidence is
@.planning/phases/v0.22-K-AS-5/K-AS-5-FACTS.md and the spec
@.planning/phases/v0.22-K-AS-5/K-AS-5b-SPEC.md.
