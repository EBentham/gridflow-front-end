---
source: "neso_data_portal"
package: "short-term-operating-reserve-stor-day-ahead-auction-results"
dataset_key: "stor_da_auction_results"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
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
record is treated as frozen. The package `metadata_modified` is `2026-10-05T11:42:08.113997`;
`TODO: verify` whether NESO intends to resume publication (the package text describes a daily auction).

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
- `TODO: verify` whether publication **resumes** (vendor status "Not Active").
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
  the body values were compared as served (`TODO: verify` that no served identifier carries trailing
  whitespace).
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
