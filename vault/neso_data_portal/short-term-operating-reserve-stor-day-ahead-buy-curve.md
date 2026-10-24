---
source: "neso_data_portal"
package: "short-term-operating-reserve-stor-day-ahead-buy-curve"
dataset_key: "stor_da_buy_curve"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-14
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: STOR day-ahead buy curve
  summary: >-
    NESO's buy curve for the Short Term Operating Reserve (STOR) day-ahead auction: the maximum MW
    and availability price for each day's assessment.
  facts:
    vendor: "NESO Data Portal: one uploaded CSV of NESO's daily STOR buy curves"
    cadence: "Daily curves, the last for 31 March 2026; NESO marks the package Not Active"
    grain: "One row per point: three points draw each service day's curve"
    history: "Service days 1 April 2021 to 31 March 2026, bar 17 August 2022"
  landscape: market
  what_it_is: >-
    NESO bought STOR in day-ahead auctions and published the buy curves used to assess them; its
    file has no curve for 17 August 2022. Each curve is three points, MW against availability price,
    drawing one step. NESO's hash file, shared before each auction, showed it had set the volume and
    price cut-offs. NESO decommissioned STOR day-ahead after launching Slow Reserve.
  how_used:
    - "Each day's maximum availability price, £/MWh, beside its clearing price in £/MW/Hr"
    - "NESO's maximum MW requirement per service day, and the dates it changed"
    - "Joined to auction results on `buy_curve_id` to read each day's tenders against it"
  chart:
    type: line
    silver: neso_data_portal/stor_da_buy_curve
    time: effective_from_date
    value: availability_price
    aggregation: max
    time_bucket: 1d
    window: {start: "2025-04-01", end: "2026-03-31"}
    unit: "£/MWh"
  chart_view:
    title: Maximum availability price, April 2025 to March 2026
    caption: >-
      Silver `stor_da_buy_curve`, `availability_price` in £/MWh (NESO's header): the price of each
      service day's one-step curve, the highest of its three points, 1 April 2025 to 31 March 2026.
      MW is 1,700 every day but 1 April 2025 (1,260).
    alt: >-
      Line chart from neso_data_portal/stor_da_buy_curve of the STOR buy curve's maximum availability
      price per service day, £/MWh, 1 April 2025 to 31 March 2026, 365 days. From April to November it never
      falls below 7.52 and peaks between 15.62 and 22.63 each month. December runs 6.91 to 13.81,
      January peaks at 26.24 on the 20th, and March spans 6.82 on the 29th, the lowest, to 33.53 on
      the 19th, the highest.
    x_label: service day, starting 05:00 UK time
    key:
      - {series: availability_price, label: Maximum availability price, paint: petrol, note: "Highest 33.53 on 19 March 2026, lowest 6.82 on 29 March 2026; median 9.83."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the one CSV downloaded whole unless its
      `last_modified` is unchanged. NESO's hash TXT is a separate key, `stor_da_buy_curve_files`,
      with no silver.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=short-term-operating-reserve-stor-day-ahead-buy-curve"
      - "GET https://api.neso.energy/dataset/0eb97ab8-61bd-4ac2-9619-10d80ae50e77/resource/8abc71ba-4484-4683-be68-5bc241b6ae7a/download/stor-da-auction-buy-curve-report.csv"
    commands:
      - {run: gridflow ingest neso_data_portal stor_da_buy_curve --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal stor_da_buy_curve --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: buy_curve_step_id, op: in, value: [BCS-5632, BCS-5633, BCS-5634, BCS-5635, BCS-5636, BCS-5637, BCS-5638, BCS-5639]}
      order_by: [buy_curve_step_id]
      columns: [buy_curve_id, effective_from_date, mw, availability_price, buy_curve_step_id,
                effective_to_date, buy_curve_name, service_catalog, curve_to_be_applied_to]
    key: [buy_curve_step_id]
    caption: "28 March 2026 (23 hours) and 29 March whole; two of 30 March's three points."
    fields:
      buy_curve_step_id: "NESO's unique id for one point of a curve, `BCS-` and a number"
      buy_curve_id: "NESO's id for the service day's curve, `BCN-` and a number"
      effective_from_date: "Service day start, UTC with a `Z`: 05:00 UK time, so 04:00Z in summer"
      mw: "MW at this point; NESO: the maximum MW for the maximum price"
      availability_price: "Availability price at this point, £/MWh as NESO's column header writes it"
      effective_to_date: "Service day end, likewise; 23 or 25 hours after the start at clock changes"
      buy_curve_name: "`BCN-Short Term Operating Reserve-` and the curve id's number"
      service_catalog: "The service the curve is for, `Short Term Operating Reserve` (NESO)"
      curve_to_be_applied_to: "The service windows the curve applies to (NESO's dictionary)"
      timestamp_utc: "Equals `effective_from_date`: the service day's start, UTC"
      published_at: "NESO's last-modified time for the whole file, read as UTC; not the curve's"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads the `_latest` view, filtering `timestamp_utc` (the service day's start) with both
      dates included. Times come back in the session's zone; the query cell converts them to UTC.
    cells:
      - |
        import pandas as pd
        df = data.neso_data_portal.query("stor_da_buy_curve", "2021-04-01", "2026-03-31")
        for col in df.select_dtypes("datetimetz"):
            df[col] = df[col].dt.tz_convert("UTC")
        uk = df.effective_from_date.dt.tz_convert("Europe/London")
        df["day"] = pd.to_datetime(uk.dt.date)
        pd.DataFrame({"uk_start": uk.dt.strftime("%H:%M"),
            "hours": (df.effective_to_date - df.effective_from_date) / pd.Timedelta(hours=1),
        }).value_counts().rename("rows").reset_index()
      - |
        def one_step(c):
            q, p = c.mw.max(), c.availability_price.max()
            return set(zip(c.mw, c.availability_price)) == {(q, 0), (q, p), (0, p)}
        curves = df.groupby("day").agg(curve=("buy_curve_id", "first"),
            curves=("buy_curve_id", "nunique"), points=("mw", "size"),
            mw=("mw", "max"), price=("availability_price", "max"))
        curves["one_step"] = df.groupby("day")[["mw", "availability_price"]].apply(one_step)
        pd.Series({"service days in the file": len(curves),
            "with one curve": (curves.curves == 1).sum(),
            "with three points": (curves.points == 3).sum(),
            "points (MW, 0), (MW, price), (0, price)": curves.one_step.sum()})
      - |
        res = data.neso_data_portal.query("stor_da_auction_results", "2021-04-01", "2026-03-31")
        acc = res[res.status == "Accepted"].groupby("buy_curve_id").contracted_mw.sum()
        j = curves.join(acc, on="curve")
        j["contracted_above_mw"] = j.contracted_mw > j.mw
        start = j.index.year - (j.index.month < 4)
        j.groupby([f"{y}-{(y + 1) % 100:02d}" for y in start]).agg(days=("curve", "size"),
            mw_low=("mw", "min"), mw_high=("mw", "max"), median_price=("price", "median"),
            top_price=("price", "max"), days_accepted=("contracted_mw", "count"),
            contracted_above_mw=("contracted_above_mw", "sum")).rename_axis("year").reset_index()
      - |
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 3.5))
        for day, colour in zip(["2021-04-01", "2025-04-01", "2025-10-16", "2026-03-19"],
                               ["#155A6E", "#7A8B2E", "#B5562F", "#4F7FA8"]):
            c = df[df.day == day].sort_values(["availability_price", "mw"], ascending=[True, False])
            ax.plot(c.mw, c.availability_price, marker="o", color=colour, label=day)
        ax.set(xlabel="MW", ylabel="availability price, £/MWh", xlim=(0, 1800), ylim=(0, None))
        ax.legend(title="service day", fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1));
    needs: captures of the buy-curve and auction-results files
    plot_alt: >-
      Step curves of four STOR service days, MW against availability price in £/MWh. Each is flat at
      its price from 0 MW to its MW, then drops to zero: 1,311 MW at 6.78 on 1 April 2021, 1,260 at
      13.08 on 1 April 2025, 1,700 at 21.50 on 16 October 2025 and 1,700 at 33.53 on 19 March 2026.
  related:
    - {dataset: neso_data_portal/short-term-operating-reserve-stor-day-ahead-auction-results, note: "The tenders each day's curve assessed, linked on `buy_curve_id`"}
    - {dataset: neso_data_portal/stor-windows, note: "Committed windows for each STOR service day, where STOR must be provided"}
    - {dataset: neso_data_portal/as_industry_notifications_stor_important, note: NESO's notices of STOR auction delays and failures}
    - {dataset: neso_data_portal/eac-auction-results, note: "Slow Reserve auctions; NESO ended STOR day-ahead after launching them"}
---

# Short Term Operating Reserve (STOR) day ahead buy curve

This package is NESO's **record of the daily buy curve used to assess the STOR day-ahead auction**. The
vendor's package text says that, as part of Clean Energy Package (CEP) 6.9, NESO runs a daily auction for
the procurement of STOR, and that "the buy curve used in the daily assessment process is available here"
(CKAN package `notes`, @.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[package page](https://www.neso.energy/data-portal/short-term-operating-reserve-stor-day-ahead-buy-curve)).
A buy curve is NESO's own demand-side price schedule: the most NESO is prepared to pay for availability
at each quantity of reserve, against which the tendered supply is compared. The vendor's assessment
guidance describes a separate curve for each operational day and a comparison against the supply curve
([assessment principles](https://www.neso.energy/document/222391/download)). For a model the table is the
**price ceiling NESO set for the STOR availability market each service day**, an input to explaining
auction clearing, not an outcome.

**One row is one vertex (step) of one buy curve for one operational service day.** The capture holds
**1,825 curves, each with exactly 3 rows (vertices), 5,475 rows in all**, one curve per service day from
2021-04-01 to 2026-03-31 with one day missing (below). The vendor defines `Buy Curve Step Id` as the unique
identifier for each buy curve step (dictionary entry in
@.planning/research/neso-snapshots/field-info/20261008T114228Z/stor_da_buy_curve.json), and all 5,475
values are distinct, so it is the entity key. `Buy Curve ID` repeats 3 times per curve and is not a row
key. There is no auction-date, EFA-block, window or settlement-period column; `Curve to be applied to` is
the single value `Service Period - All Operational Day windows` on every row.

**What this package is not.**

- It is **not capacity.** The rows are points on a price curve. In a concrete curve the three vertices
  read 1311 MW at 0 GBP/MWh, 1311 MW at 6.78 GBP/MWh and 0 MW at 6.78 GBP/MWh (the shape of curve
  `BCN-00000000`, shown for how the vertices read, not as a series). **Never sum `mw` across a curve's
  vertices or across curves**: that counts the geometry of the curve as additional capacity.
- It is **not the auction outcome.** Awards, contracted MW and clearing prices are in the neighbouring
  package @./short-term-operating-reserve-stor-day-ahead-auction-results.md. The two are linked on
  `Buy Curve ID` for context only (see Relationship below); their measures are not additive and their price
  units differ.
- It is **not a forecast** and carries no issue time (`issue: none`).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| STOR DA Auction Buy Curve Report | CSV | upload | `8abc71ba-4484-4683-be68-5bc241b6ae7a` |

Download: [stor-da-auction-buy-curve-report.csv](https://api.neso.energy/dataset/0eb97ab8-61bd-4ac2-9619-10d80ae50e77/resource/8abc71ba-4484-4683-be68-5bc241b6ae7a/download/stor-da-auction-buy-curve-report.csv).
The resource was created `2021-03-31T04:36:13.129484` and last modified `2026-03-30T04:22:46.013246`
(catalog snapshot). The sole captured body (bronze capture `20261008T112735Z`) is 1,036,153 bytes, UTF-8,
one header and 5,475 data rows, SHA-256 `d240b64959131ea92ed68c60874d08e32d5297683842f28370eb7f2dcf2b05d0`.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| STOR Day Ahead Buy Curve Hash | TXT | upload | `1eacef3e-c7e5-4ce2-a1e3-c667f39c0a17` |

Download: [2026-03-31_hash.txt](https://api.neso.energy/dataset/0eb97ab8-61bd-4ac2-9619-10d80ae50e77/resource/1eacef3e-c7e5-4ce2-a1e3-c667f39c0a17/download/2026-03-31_hash.txt).
Created `2021-03-30T13:44:25.445284`, last modified `2026-03-29T14:58:45.199060`; captured as 64 bytes
(bronze `20261008T112739Z`, SHA-256 `f4b567dc86b178d3701a9f8e5819346eeb4fecc9f7a2fb08ea4a0c816802943b`).
It is kept as a catalogue-only DOC file: no silver is built from it. See the hash section below for what it
is and is not.

## Families

### `stor_da_buy_curve`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Buy Curve Name | `buy_curve_name` | string | — | yes | — | Text |
| Service Catalog | `service_catalog` | string | — | yes | — | Text |
| Curve to be applied to | `curve_to_be_applied_to` | string | — | yes | — | Text |
| Effective From Date | `effective_from_date` | datetime | `%Y-%m-%d %H:%M:%SZ` | no | UTC | ISO-8601 |
| Effective To Date | `effective_to_date` | datetime | `%Y-%m-%d %H:%M:%SZ` | yes | UTC | ISO-8601 |
| Buy Curve Step: Buy Curve Step Id | `buy_curve_step_id` | string | — | no | — | text |
| MW | `mw` | float64 | — | yes | — | integer |
| Availability Price (£/MWh) | `availability_price` | float64 | — | yes | — | Number |
| Buy Curve: Buy Curve ID | `buy_curve_id` | string | — | yes | — | Text |

- Entity key: `buy_curve_step_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`effective_from_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

Silver also carries the engine columns `timestamp_utc`, `event_time`, `published_at`, `available_at`,
`bronze_capture_id`, `capture_written_at`, `source_run_id` and `dataset_version` (17 columns in all).

**The two clocks.**

- **Vintage (`ckan_last_modified`).** `available_at` (and `published_at`) is the CKAN `last_modified` of
  the captured upload, `2026-03-30T04:22:46.013246` for the single capture, identical on all 5,475 rows.
  It is the **upload time of the cumulative file, not the time each curve was set**: the body has no issue
  or publication column, so the whole 2021 to 2026 history carries one 2026 `available_at`
  (`TODO: verify` the original publication instant of each daily curve). A point-in-time backtest cannot
  use this table to say when a past curve became known. The vendor's advance-commitment hash (below) hints
  that curves were committed before each auction, but it does not prove that each historical row existed at
  its effective date.
- **Event time (`utc_instant(effective_from_date)`).** `timestamp_utc` and `event_time` equal
  `effective_from_date`, the start of the validity day, taken from the literal `Z`. This is a real UTC
  instant: every start converts to **05:00 Europe/London** on all 5,475 rows (04:00 UTC in summer time,
  05:00 UTC in winter), agreeing with NESO's documented local operational-day boundary
  ([STOR operational guidance](https://www.neso.energy/document/209016/download), availability section),
  so the `Z` is not a relabelled local clock. `effective_to_date` is the end of the same day and is not a
  publication date.

**Validity span and clock changes.** `effective_from_date` runs `2021-04-01 04:00:00Z` to
`2026-03-31 04:00:00Z` and `effective_to_date` runs `2021-04-02 04:00:00Z` to `2026-04-01 04:00:00Z`.
Because the day is the local 05:00 to 05:00 day, its UTC length varies: **5,445 rows span 24 hours, 15 span
23 hours and 15 span 25 hours** (5 clock changes in each direction times 3 vertices). Examples from the
body: `2021-10-30 04:00:00Z` to `2021-10-31 05:00:00Z` (25 hours) and `2022-03-26 05:00:00Z` to
`2022-03-27 04:00:00Z` (23 hours). Do not assume 24 hours. `TODO: verify` interval closure: no source says
whether the end instant belongs to the service day.

**Vendor dictionary versus body.**

- The dictionary example for both date columns is `2021-04-01T04:00:00` (ISO-8601 without `Z`); the
  served cells are `%Y-%m-%d %H:%M:%SZ`. The body is the authority for parsing.
- The dictionary example for `Buy Curve Name` is date-bearing
  (`BCN-Short Term Operating Reserve-2021-04-01 04:00:00Z-2021-04-02 04:00:00Z`); the served names are
  `BCN-Short Term Operating Reserve-NNNNNNNN` with the same number as the `Buy Curve ID`, and there is one
  distinct name per curve (1,825). Treat the name as a label; key on `buy_curve_step_id`.
- The dictionary types `MW` as integer; gridflow reads it as `float64` per the registry record.

**Units (vendor dictionary and header only, never inferred from a column name).**

| Silver column | Unit | Source |
|---|---|---|
| `mw` | MW | vendor column header "MW"; dictionary description "Maximum MW associated with maximum prices listed in the availability price field"; the dictionary `unit` entry is the type label `integer` |
| `availability_price` | GBP/MWh | the vendor header literally reads `Availability Price (£/MWh)`; NESO's assessment guidance gives the alternative-action price in the same unit |
| `effective_from_date`, `effective_to_date` | UTC instant | dictionary unit ISO-8601 |

**The price unit is GBP per MWh, not the auction results' GBP per MW per hour.** The sibling results
package states its availability and clearing prices in £/MW/Hr; do not carry that unit across to this
curve, and do not compute a price comparison between the two without stating the conversion
(`TODO: verify` how NESO relates the curve's £/MWh to the tender £/MW/Hr in the assessment). No
MW-to-energy conversion is stated by the vendor. The curve columns `buy_curve_name`, `service_catalog`,
`curve_to_be_applied_to`, `buy_curve_id` and `buy_curve_step_id` are dimensionless labels
(`service_catalog` is `Short Term Operating Reserve`; `buy_curve_step_id` is `BCS-NNNN`, `buy_curve_id`
is `BCN-NNNNNNNN`).

**Value ranges (silver).** `mw` runs 0 to 1,700 and `availability_price` 0 to 250.69. There are no null
cells in any column.

**Typing and sentinels (K-DFS FACTS g5, g6).** There is no sentinel token: no blank, no negative number,
no `NA`/`N/A`, no percentage or thousands formatting and no padded cell was observed, and the production
CSV reader agreed with a strict second parse on every row and cell. **Zeros are values:** `mw` has 1,825
zeros and `availability_price` has 1,825 zeros, each with a maximum run of 2 consecutive rows. They are the
curve's own vertices (a zero-quantity vertex and a zero-price vertex), not missing data; do not treat zero
as null or drop those rows.

### `stor_da_buy_curve_files`

- Kind: files · archetype: EVT · refresh: frozen · empty allowed: no
- files: catalogue only

This family catalogues the hash TXT (DOC). It produces no silver table.

#### The hash TXT: a vendor commitment, not a checksum of this CSV

The captured TXT contains a single 64-hexadecimal-character string with no trailing newline:
`f138651b6385d49a8aedc82c28b5194b93f36b5d3cbdfc4178dc2fa90385ed91`. The published filename is
`2026-03-31_hash.txt`. The vendor's resource documentation describes it as an advance commitment to the
volume and price cutoffs of the auction and says the date in the filename is the service-delivery date
([hash resource](https://www.neso.energy/data-portal/short-term-operating-reserve-stor-day-ahead-buy-curve/stor_day_ahead_buy_curve_hash)).
The package text adds that the last hash file was uploaded on 29 March 2026, the final file submitted to
the portal. The filename date 2026-03-31 is the last effective date in the curve CSV.

It does **not** say that the string is a checksum of the cumulative buy-curve CSV, nor which algorithm
or preimage produced it. Diagnostic digests of the captured CSV bytes (SHA-256
`d240b64959131ea92ed68c60874d08e32d5297683842f28370eb7f2dcf2b05d0`, SHA3-256
`09fe578c2f1ff9ae48e1f6dc13a3e861a576efa798bfabd878ef08002e9de025`) match neither, so equality is ruled
out under those tests only, not the validity of the vendor's commitment. A 64-hex-character length fits
several digest algorithms and identifies none. `TODO: verify` the hash algorithm; `TODO: verify` the exact
preimage (what is hashed and in what layout). Until both are documented, the file is a DOC and is **not**
used to verify the CSV.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Not Active

The package text records that STOR day-ahead has been decommissioned following the launch of the Slow
Reserve service in the Enduring Auction Capability (EAC): the final STOR DA tender was run on 30 March 2026.
That agrees with the last curve in the body (validity day 2026-03-31) and with the frozen refresh. The
package `metadata_modified` is `2026-04-10T14:53:22.493821` and no later data is expected.

## Licence and attribution

- Licence: NESO Open Data Licence ([licence text](https://www.neso.energy/data-portal/ngeso-open-licence))
- Attribution: Supported by National Energy SO Open Data

gridflow outputs derived from this package carry the attribution line "Supported by National Energy SO
Open Data".

## Holds

- none

**No resource and no output of this package is held.** The CSV family is eligible at
`utc_instant(effective_from_date)` with a whole-capture latest policy and key `buy_curve_step_id`: the
temporal column is a real UTC instant (checked against the documented local boundary) and the key is
vendor-documented and measured unique, so there is no clock or key hold to state. The TXT is a DOC file
with no output to hold (K-DFS-a-SPEC; RULINGS 801, 803, 804 and 807).

**Open questions that do not hold any output** (K-DFS FACTS, carried as non-holding TODOs):

- `TODO: verify` **MISSING-CURVE-DATE**: the start-date sequence lacks `2022-08-17`, the only gap in 1,826
  calendar days from 2021-04-01 to 2026-03-31 inclusive (1,825 curves). A vendor explanation or a
  corrected report would settle it. gridflow does not manufacture that day's curve.
- `TODO: verify` the **hash algorithm** and **hash preimage** (above).
- `TODO: verify` the **original publication instant** of each daily curve (vintage clock above).
- `TODO: verify` **interval closure** of the validity day.

## Relationship to the auction results (context join only)

The curve is NESO's assessment input; the results are the provider tender outcomes of the same auctions
(@./short-term-operating-reserve-stor-day-ahead-auction-results.md). Measured on `Buy Curve ID` between
this capture and the results capture (K-DFS FACTS, DFS-f):

| Measure | Count |
|---|---:|
| Auction-result rows | 121,480 |
| Distinct non-blank result Curve IDs | 1,818 |
| Of those, found in this curve report | 1,818 |
| Result rows whose start and end bounds match the curve | 121,152 |
| Result rows with a blank `buy_curve_id` | 328 |
| Joined rows with differing boundaries | 0 |
| Curve IDs with no result rows | 7 |

Every non-blank result link resolves to a curve with identical bounds; the 328 unjoined result rows have
an absent identifier, not an unknown curve. gridflow provides **no silver join** between the two (K-DFS-a
spec); the join is consumer-side, for assessment context. Obtain awards, contracted MW and clearing
prices from the result rows, and preserve the missing links and the 7 curve-only days rather than
dropping them. For window context, @./stor-windows.md can be joined consumer-side on the local delivery date
(Europe/London, derived explicitly from the literal UTC instant); `TODO: verify` day-by-day calendar
coverage against it, as only the 2021-04-01 to 2026-03-31 span is documented there.

## Known issues and gotchas

- **Vertices, not capacity.** Never sum `mw` within a curve or across curves; filter and read it per
  `buy_curve_id` ordered by step.
- **Price unit.** `availability_price` is GBP/MWh; the auction results use GBP/MW/h. They are not
  interchangeable.
- **Zeros are real.** 1,825 zero-MW and 1,825 zero-price vertices are part of the curve.
- **Service-day length varies** (23, 24 or 25 hours); derive the local date from the instant explicitly
  and never synthesise timestamps from a date.
- **One `available_at` for all history.** The vintage is the upload time of the cumulative file; do not
  use it for point-in-time claims.
- **`2022-08-17` has no curve.** Do not interpolate or copy a neighbouring day.
- **`Buy Curve ID` is not a row key** (1,825 distinct over 5,475 rows); `(Curve ID, MW)` is not unique
  either (3,650 distinct), and only `buy_curve_step_id` (or `(Curve ID, MW, price)`, 5,475 distinct) is.
  The key is the vendor Step ID.
- **Header encoding.** The bronze header carries the single pound sign in `Availability Price (£/MWh)`.
  An earlier draft carried a mojibake spelling; the registry record uses the correct header.
- **The hash file is a vendor commitment, not a checksum.** Do not use it to validate the CSV.

**Activation (2026-10-14, master `c5ad993`, PR #121).** The DFS-a batch (the four Demand Flexibility
Service families and this package) merged triple-green (RULINGS 807: CI green, Sol diff review APPROVE on
the first pass, verification passed) and was activated from the 2026-10-08 capture with no prior silver, so
nothing was overwritten (RULINGS 808, 809). `stor_da_buy_curve` produced **5,475 silver rows**, equal to the
spec plan, with no excluded rows; the batch total was 25,059 rows, and the one recorded transform failure
was the Demand Flexibility archive utilisation report (not this package). The batch-wide
`reconcile --all --cutoff 2026-10-13` exited 0 over 227 families with 0 gaps, and coverage was clean (1,385
captured, 0 missing, 0 unfrozen). The receipt is in @.planning/v0.22-RESULTS.md section DFS-a; the
evidence is @.planning/phases/v0.22-K-DFS/K-DFS-FACTS.md and the spec
@.planning/phases/v0.22-K-DFS/K-DFS-a-SPEC.md.
