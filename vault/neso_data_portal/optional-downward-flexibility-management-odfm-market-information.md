---
source: "neso_data_portal"
package: "optional-downward-flexibility-management-odfm-market-information"
dataset_keys: ["odfm_market_information_instructed", "odfm_market_information_load_factors", "odfm_market_information_results"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Optional Downward Flexibility Management (ODFM) Market Information

Optional Downward Flexibility Management (ODFM) was a **temporary** service NESO (then the Electricity System
Operator) ran to balance the system when demand was unusually low. The vendor's package text explains that during
2020-22 COVID-19 restrictions risked longer low-demand periods, so a service was put in place "across the summer
periods in 2020 and 2021" to give the control room downward flexibility it could not reach through the Balancing
Mechanism or the Platform for Ancillary Services, and that **the service is no longer live** (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[ODFM dataset](https://www.neso.energy/data-portal/optional-downward-flexibility-management-odfm-market-information)).
The package is a frozen record of that service: the weekly **assessment results** (who bid, at what price, accepted
or rejected), one day of **instructed volume**, the **load factors** used to compare bids, and PDF market reports
and requirement papers. It is a historical curiosity rather than a live feed, and it answers questions such as "how
much downward flexibility did the control room instruct on 5 July 2020" and "what did providers bid".

**What gridflow holds, in one place.**

- **Instructed volumes (silver, eligible):** the **V2** republication only, 49 half-hour rows for 4-5 July 2020.
  The first upload (V1) is a resource-level HOLD (below).
- **Load factors (silver, held):** loaded and queryable as rows and schema, but the output is held on the question of
  clock and scale (below). No data value from this family is published on this page.
- **Market results (bronze only, no silver):** the two result files are ingested into bronze but **not tabled**:
  both repeat complete rows, so no key passes the duplicate guard and the family has **no record** (RULINGS 538
  precedent).
- **Reports and papers (8 PDFs):** catalogue only (DOC); they are primary sources for scope, assessment and units.

The three CSV families do **not share a row key and are never joined** (see Known issues). Background for the
settlement-period convention used by the instructed volumes: @../../../20-domain/concepts/settlement-period.md.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Market Information Results 2020 | CSV | upload | `cfd349e9-7f36-480d-abb5-a740d8a6ea16` |
| Market Information Results 2021 | CSV | upload | `45e60798-da66-4734-bf9e-178efd49657c` |
| ODFM Instructed Volume for 05-07-2020 V2 | CSV | upload | `5c507a16-d2f3-44df-b1bb-98acc0d74e1c` |
| ODFM Load Factors | CSV | upload | `e6146148-c862-49f6-9c7f-52dc2b3e7086` |

Only two of these four resources reach a silver table. **V2 instructed volumes** (49 rows) and **ODFM Load
Factors** (240 rows, held) are loaded. The two **Market Information Results** files carry the `SILVER` disposition
in the registry but the family has no record, so they are ingested to bronze and **produce no silver rows**
(`ingest-only`, @docs/neso_data_portal/eligibility.md).

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Market Information Report - General Information | PDF | upload | `14958cfe-d8a3-4319-ace1-60351c2b7056` |
| Market Information Report for 05.07.20 | PDF | upload | `b6f57985-df24-4207-83fa-2f1dc6a949f8` |
| Market Information Report for 10.05.20 | PDF | upload | `b435a5d1-9d94-477e-bf50-b99a7693d65c` |
| Market Information Report for 22.05.20 | PDF | upload | `5ebec109-4cbf-4792-88d6-18feef004f9c` |
| Market Information Report for 23.05.20 | PDF | upload | `8348d8b3-3156-4e40-bdd5-ac5215564735` |
| Market Information Report for 24.05.20 | PDF | upload | `0ffd097f-b4c9-42e9-954f-0f68c6773577` |
| ODFM Requirement - Summer 2021 | PDF | upload | `430861fa-3ffc-4e8b-80b1-06e3ebe19007` |
| Requirements paper | PDF | upload | `a79a55d8-206f-43bc-94c6-4fda04b33cae` |

The eight documents are catalogue-only (family `odfm_market_information_files`): they are kept in bronze as the
vendor's own explanation of scope, assessment process and units, and are not parsed. Download links (vendor URLs from
the catalogue snapshot of 2026-10-06; the vendor's last-modified stamp is the date in the third column):

| Document | Download | CKAN last modified |
|---|---|---|
| Market Information Report - General Information | [mir-general-information.pdf](https://api.neso.energy/dataset/23ec7a9f-6220-4d1e-9099-e9195a2ed177/resource/14958cfe-d8a3-4319-ace1-60351c2b7056/download/mir-general-information.pdf) | 2020-06-10 |
| Market Information Report for 10.05.20 | [200510-odfm-mir.pdf](https://api.neso.energy/dataset/23ec7a9f-6220-4d1e-9099-e9195a2ed177/resource/b435a5d1-9d94-477e-bf50-b99a7693d65c/download/200510-odfm-mir.pdf) | 2020-05-13 |
| Market Information Report for 22.05.20 | [mir_200522.pdf](https://api.neso.energy/dataset/23ec7a9f-6220-4d1e-9099-e9195a2ed177/resource/5ebec109-4cbf-4792-88d6-18feef004f9c/download/mir_200522.pdf) | 2020-05-27 |
| Market Information Report for 23.05.20 | [mir_200523.pdf](https://api.neso.energy/dataset/23ec7a9f-6220-4d1e-9099-e9195a2ed177/resource/8348d8b3-3156-4e40-bdd5-ac5215564735/download/mir_200523.pdf) | 2020-05-27 |
| Market Information Report for 24.05.20 | [mir_200524.pdf](https://api.neso.energy/dataset/23ec7a9f-6220-4d1e-9099-e9195a2ed177/resource/0ffd097f-b4c9-42e9-954f-0f68c6773577/download/mir_200524.pdf) | 2020-05-27 |
| Market Information Report for 05.07.20 | [200705-odfm-mir.pdf](https://api.neso.energy/dataset/23ec7a9f-6220-4d1e-9099-e9195a2ed177/resource/b6f57985-df24-4207-83fa-2f1dc6a949f8/download/200705-odfm-mir.pdf) | 2020-07-08 |
| Requirements paper | [odfm-requirements-paper-external.pdf](https://api.neso.energy/dataset/23ec7a9f-6220-4d1e-9099-e9195a2ed177/resource/a79a55d8-206f-43bc-94c6-4fda04b33cae/download/odfm-requirements-paper-external.pdf) | 2020-05-19 |
| ODFM Requirement - Summer 2021 | [ofdm-requirement-paper.pdf](https://api.neso.energy/dataset/23ec7a9f-6220-4d1e-9099-e9195a2ed177/resource/430861fa-3ffc-4e8b-80b1-06e3ebe19007/download/ofdm-requirement-paper.pdf) | 2021-04-28 |

What the documents say (vendor resource descriptions, and the captured documents as read for K-AS-5-FACTS):

- **General Information** distinguishes *dispatched* weeks (a report for each dispatched day, including registered
  units and acceptance or rejection decisions) from *non-dispatched* weeks (a same-format CSV with the rejected rows
  and the reason no requirement existed, excluding units unavailable all week). This is why a result row's report
  period label is **not** universally a single delivery day.
- **The daily Market Information Reports** (10, 22, 23, 24 May and 5 July 2020) describe, per instruction day, the
  volume NESO instructed, the delivery window and the assessment outcome. The 5 July 2020 report states that the
  forecast volume confirmed by providers rose during the day; it is the narrative companion of the instructed-volume
  file. The report for 10 May explains how effective price is assessed as service price divided by forecast load
  factor and discusses load factors in percentage terms (a fact that bears on the load-factor hold).
- **Requirements paper** names typical low-demand overnight periods and explicitly allows other periods and
  day-ahead assessment; it is **not** a fixed daily service window. **Requirement - Summer 2021** is the 2021
  equivalent.

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| ODFM Instructed Volume for 05-07-2020 | CSV | upload | `f0a52698-5f80-4fb7-ad64-ede99015195f` | TODO: ODFM-INSTRUCTED-V1 — the first "ODFM Instructed Volume for 05-07-2020" upload has 46 unnamed trailing header cells (a frozen header cannot hold repeated blank names) and every Settlement Period label is one period behind its Time label (49 of 49 rows); NESO's V2 republication corrects the periods and changes 36 of the 49 instructed volumes, and V2 is the loaded version. Is V1 withdrawn, or does it carry a different meaning? (v0.22-K-AS-5b) |

Download for the held V1 upload (kept in bronze, not loaded):
[odfm-instructed-volume-for-05-07-2020.csv](https://api.neso.energy/dataset/23ec7a9f-6220-4d1e-9099-e9195a2ed177/resource/f0a52698-5f80-4fb7-ad64-ede99015195f/download/odfm-instructed-volume-for-05-07-2020.csv)
(CKAN last modified 2020-07-08T13:42:03; 3,578 bytes, 49 rows). The vendor's own description of V1 says a new version
was uploaded and tells users to use "ODFM Instructed Volume for 05-07-2020 V2". This is a **resource-level HOLD**,
not an ADR-040 recorded failure (RULINGS 607 precedent; seat ruling 5): the cause is a header shape that cannot be
frozen plus wrong period labels, not an allow-listed failure class. V1 and V2 are **never unioned** and never
de-duplicated against each other.

## Families

### `odfm_market_information_files`

- Kind: files · archetype: EVT · refresh: frozen · empty allowed: no
- files: catalogue only

The 8 PDF documents above. No parsing, no silver, no clocks.

### `odfm_market_information_instructed`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Settlement Period | `settlement_period` | int64 | — | no | — | — |
| ODFM Instructed MW | `odfm_instructed_mw` | float64 | — | yes | — | MW |
| Time | `time_label` | string | — | yes | — | — |
| Date | `settlement_date` | date | `%d/%m/%Y` | no | — | — |

- Entity key: `resource_id`, `settlement_date`, `settlement_period`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: sp_pair (`settlement_date`, `settlement_period`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What a row is.** One half-hour of the **system-level ODFM volume NESO instructed** for Sunday 5 July 2020 (the
vendor description: "the ODFM instructed volume for Sunday. The BMRS Demand forecast has already been adjusted for
this"). The V2 description explains why the file exists: after a process failure in sending enactment
communications to providers on 4 July, the volume first shared on the portal contained errors, so NESO
**re-published the forecast volume of ODFM instructed after the event**. There is no unit, provider or region
column: the quantity is a single national number per half-hour. The market report states that the instructed
forecast volume is a different quantity from the sum of accepted registered capacity, so summing result capacity is
not a reconstruction of this column.

**Two clocks.**

- **Vintage (when it was known): `ckan_last_modified`.** `available_at` = `published_at` = the CKAN `last_modified`
  of the V2 capture, **2020-07-08T13:37:56.620172Z**, identical on all 49 rows. No issue column exists in the file
  and nothing guarantees the file was unchanged since that instant, so this is a conservative availability stamp.
  The gridflow capture happened later (2026-10-08T11:15:32Z) and is recorded in `capture_written_at`, but it is
  not the vintage. `TODO: verify` the order of the two uploads: V1's CKAN stamp (2020-07-08T13:42:03) is later than
  V2's (13:37:56) even though V1's description says the new version came later.
- **Event time: `event_time` = `timestamp_utc` = start of the settlement period**, from the established `sp_pair`
  recipe on the Europe/London settlement clock, converted to tz-aware UTC at the silver boundary. 4-5 July 2020 is
  British Summer Time, so settlement period 1 of 5 July starts at 2020-07-04T23:00Z, and period 47 (Time label
  `23:00`) on 4 July starts at 2020-07-04T22:00Z. The loaded rows are **periods 47 and 48 of 4 July and periods 1
  to 47 of 5 July** (49 rows), so `event_time` runs from 2020-07-04T22:00Z to 2020-07-05T22:00Z. Period 48 of 5
  July is absent; `TODO: verify` why the file stops there. Both days have 48 periods (no clock change); the range
  check is `settlement_period` `1..50`, never `1..48`.

The `Time` column is kept as a raw corroborating string (`time_label`). On V2 all 49 Time and Settlement Period
pairs agree with each other; on V1 all 49 disagree by one period (the V1 hold). The settlement-period anchor, not the
`Time` label, supplies the instant.

**Units (vendor dictionary only).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/odfm_market_information_instructed.json):

| Silver | Vendor title and description (dictionary) | Unit |
|---|---|---|
| `settlement_period` | Settlement Period: "a period of 30 minutes beginning on the hour or the half-hour" | ordinal, no physical unit |
| `odfm_instructed_mw` | ODFM Instructed MW: "ODFM instructed in MW" | MW |
| `time_label` | Time: "time of when instruction took place" (dictionary type `time`, example `23:00`) | none stated |
| `settlement_date` | Date: "date of ODFM" (dictionary example `05/07/2020`) | calendar date |

The dictionary types `ODFM Instructed MW` as an integer; gridflow types it `float64` because an integer-only domain
is not established (a column type is a measured fact about this body, not a vendor guarantee). No unit is inferred
from a column name, and nothing is converted.

**Sentinels and typing (K-AS-5-FACTS g5, g6).** No blanks, `NA` tokens, thousands separators or non-numeric cells in
the loaded body. **Zero is a published value**: 9 of the 49 rows are exactly 0 MW and are kept as zero (they are not
nulls, and they are not dropped). The loaded range is 0 to 2,194 MW. The body is valid UTF-8 and parses faithfully;
no trim, no token map and no bounds are applied apart from `settlement_period` `1..50`. The header the reader
returns is `Settlement Period, ODFM Instructed MW, Time, Date` (V2's raw header has a trailing space on three names,
`ODFM Instructed MW `, `Time ` and `Date `, which the reader strips; `Settlement Period` is clean).

**Identity and selection.** The entity key is `(resource_id, settlement_date, settlement_period)` with
`latest_partition: resource_id`. The research key was (`date`, `settlement_period`); `resource_id` was added because
the record model requires an `sp_pair` key to strictly contain the pair and the hard rule forbids keying settlement
data on (date, period) alone (seat ruling 6, AS-4a BSAD precedent). The family cannot silently merge V1 and V2: V1
is excluded at resource level, so the key never has to disambiguate versions.

### `odfm_market_information_load_factors`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Datetime | `datetime` | string | — | no | — | — |
| Scottish Hydro Wind | `scottish_hydro_wind` | float64 | — | yes | — | — |
| Scottish Power Wind | `scottish_power_wind` | float64 | — | yes | — | — |
| Electricity North West Wind | `electricity_north_west_wind` | float64 | — | yes | — | — |
| NPG North East Wind | `npg_north_east_wind` | float64 | — | yes | — | — |
| NPG Yorkshire Wind | `npg_yorkshire_wind` | float64 | — | yes | — | — |
| SP Manweb Wind | `sp_manweb_wind` | float64 | — | yes | — | — |
| WPD West Midlands Wind | `wpd_west_midlands_wind` | float64 | — | yes | — | — |
| WPD East Midlands Wind | `wpd_east_midlands_wind` | float64 | — | yes | — | — |
| UKPN East Anglia Wind | `ukpn_east_anglia_wind` | float64 | — | yes | — | — |
| UKPN London Wind | `ukpn_london_wind` | float64 | — | yes | — | — |
| WPD South Wales Wind | `wpd_south_wales_wind` | float64 | — | yes | — | — |
| WPD South West Wind | `wpd_south_west_wind` | float64 | — | yes | — | — |
| SSE South Wind | `sse_south_wind` | float64 | — | yes | — | — |
| UKPN South East Wind | `ukpn_south_east_wind` | float64 | — | yes | — | — |
| Scottish Hydro Solar | `scottish_hydro_solar` | float64 | — | yes | — | — |
| Scottish Power Solar | `scottish_power_solar` | float64 | — | yes | — | — |
| Electricity North West Solar | `electricity_north_west_solar` | float64 | — | yes | — | — |
| NPG North East Solar | `npg_north_east_solar` | float64 | — | yes | — | — |
| NPG Yorkshire Solar | `npg_yorkshire_solar` | float64 | — | yes | — | — |
| SP Manweb Solar | `sp_manweb_solar` | float64 | — | yes | — | — |
| WPD West Midlands Solar | `wpd_west_midlands_solar` | float64 | — | yes | — | — |
| WPD East Midlands Solar | `wpd_east_midlands_solar` | float64 | — | yes | — | — |
| UKPN East Anglia Solar | `ukpn_east_anglia_solar` | float64 | — | yes | — | — |
| UKPN London Solar | `ukpn_london_solar` | float64 | — | yes | — | — |
| WPD South Wales Solar | `wpd_south_wales_solar` | float64 | — | yes | — | — |
| WPD South West Solar | `wpd_south_west_solar` | float64 | — | yes | — | — |
| SSE South Solar | `sse_south_solar` | float64 | — | yes | — | — |
| UKPN South East Solar | `ukpn_south_east_solar` | float64 | — | yes | — | — |
| Scottish Hydro Other | `scottish_hydro_other` | float64 | — | yes | — | — |
| Scottish Power Other | `scottish_power_other` | float64 | — | yes | — | — |
| Electricity North West Other | `electricity_north_west_other` | float64 | — | yes | — | — |
| NPG North East Other | `npg_north_east_other` | float64 | — | yes | — | — |
| NPG Yorkshire Other | `npg_yorkshire_other` | float64 | — | yes | — | — |
| SP Manweb Other | `sp_manweb_other` | float64 | — | yes | — | — |
| WPD West Midlands Other | `wpd_west_midlands_other` | float64 | — | yes | — | — |
| WPD East Midlands Other | `wpd_east_midlands_other` | float64 | — | yes | — | — |
| UKPN East Anglia Other | `ukpn_east_anglia_other` | float64 | — | yes | — | — |
| UKPN London Other | `ukpn_london_other` | float64 | — | yes | — | — |
| WPD South Wales Other | `wpd_south_wales_other` | float64 | — | yes | — | — |
| WPD South West Other | `wpd_south_west_other` | float64 | — | yes | — | — |
| SSE South Other | `sse_south_other` | float64 | — | yes | — | — |
| UKPN South East Other | `ukpn_south_east_other` | float64 | — | yes | — | — |

- Entity key: `datetime`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**This output is HELD** (see Holds). It is loaded into silver for the record (240 rows, 51 columns: `datetime`,
the 42 region by technology columns, and the 8 engine-stamped columns) but is not published, and **this page quotes
no data value or value statistic for it** (the label coverage below is the key, not a value column).

**What a row is.** A forecast time label with wide regional by technology load-factor fields: 14 distribution
network regions (the DNO regions in the column names) each for **Wind**, **Solar** and **Other** (14 x 3 = 42 value
columns). The vendor dictionary describes the wind and solar value columns as "the load factor forecast for each DNO region" (the Other columns: "… excluding Wind and Solar") and
leaves the unit field blank. The vendor's resource description adds that the file is updated and rows are appended
each time the service is instructed, that load factors for wind and solar are variable, and that all other fuel
types are set at 100% for all periods (vendor text; it is not a definition of the exported numeric scale, and
whether an "Other" cell reads `100` or `1` is exactly the held question). The market report explains effective-price
assessment as service price divided by forecast load factor and discusses load factors in percentage terms.

**Two clocks.**

- **Vintage: `ckan_last_modified`.** `available_at` = `published_at` = the CKAN `last_modified` of the capture,
  **2020-07-20T15:17:53.063674Z**, identical on every row. The file grows over time (rows are appended), and only one
  capture exists, so how earlier versions looked is unmeasured.
- **Event time: none.** The temporal recipe is `none`: **`timestamp_utc` is the gridflow capture time**
  (`capture_written_at`, 2026-10-08T11:15:36Z), the same on every row, and `event_time` is not derived from the
  `Datetime` label. Do not read `timestamp_utc` as the forecast instant. The `Datetime` label (a string spelled
  `%d/%m/%Y %H:%M`, unique across the 240 rows) is kept raw because the file does not state its time zone or its
  period start or end convention. As labels the span is 2020-05-09 23:00 to 2020-07-05 22:30, with discontinuous
  coverage of event periods; the label is not a UTC instant.

**Units.** None stated by the vendor (dictionary unit blank). The values are loaded **as published, unscaled**: no
percentage conversion, no clipping and no rescaling of any column. The unit and the scale are the held question.

**Sentinels and typing (g5, g6).** Every value cell is numeric and none is blank. The body is valid UTF-8, with no
embedded quote, comma or newline in any data cell. Zeros and any other values are kept exactly as published.

**Identity.** `datetime` is measured unique across the 240 rows (no vendor guarantee of a stable key is stated;
`TODO: verify`). There is no `resource_id` in the key because the family has a single resource.

### `odfm_market_information_results`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no
- ingest-only: no silver yet

**No record, no transformer, no silver.** The two result files (2020: 7,321 CSV rows; 2021: 35,574 CSV rows; 42,895 in
all) are captured into bronze byte-for-byte and are **ingested but not
tabled**. Both bodies repeat complete rows (**9 exact duplicate rows** in the 2020 file, **170** in the 2021 file),
and the `Unique ID` column also collides, so no key built from vendor columns passes the duplicate guard. Adding
columns cannot help, because exact duplicates repeat every vendor value. The outcome is the RULINGS 538 pattern (no
record, registry untouched, ingest-only), seat ruling 9. Nothing is de-duplicated, numbered or repaired.

What the bodies contain, from the vendor dictionary (@.planning/research/neso-snapshots/field-info/20261008T114228Z/odfm_market_information_results.json):

| Vendor column | Dictionary description | Unit |
|---|---|---|
| Unique ID | "The ID for the submitted bid in the auction" | none |
| Contracted Unit ID | "The unique identifier for the specific unit bidding into the market" | none |
| Applicant/Agent | provider that submitted the bid | none |
| Price | "The price for the provision of the service" | £/MW/hr |
| Allocated Registered Service Volume | "The total capacity of the bidding unit" | MW |
| Technology type | type of unit bidding in | none |
| Start time (BST), Cease time (BST) | time delivery commenced and ended | hh:mm, labelled BST |
| Start date, Cease Date | date delivery commenced and ended | dd.mm.yyyy |
| GSP, DNO | Grid Supply Point; Distribution Network Operator | none |
| Accept/Reject | "Was the bid accepted or rejected" | none |
| Reasons | reason code for the acceptance or rejection | none |
| Date | "Date the bid was made for" | none |

Facts relevant to anyone who later wants a record:

- **Encoding.** Both bodies fail strict UTF-8. A strict CP1252 decoding parses faithfully (it preserves the currency
  sign in the price header), but that is measured evidence, not a vendor charset declaration (`TODO: verify` the
  vendor encoding).
- **Report period.** The older file's `Date` column mixes day/month labels and week-range prose; the later file uses
  dotted calendar dates. It is a report-target label, not an issue time, and not universally one calendar day (see
  the General Information document). The older `Unique ID` also contains spreadsheet-style numeric day tokens.
- **Clocks.** Start and cease clocks are explicitly labelled BST by the vendor, but composing them with the dotted
  dates into instants is not done here. No issue column exists.
- **Reasons** holds categorical codes and the word `Accept`; acceptance vocabulary has case variants.

The vintage metadata is retained: the 2020 file's CKAN last modified is 2020-11-06T10:53:58 and the 2021 file's is
2021-11-01T11:58:18 (vendor description: each new week is appended to the end of the file). Because there is no
record there is no event time, no `available_at` and no silver clock for this family.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Status: Not Active

The service is no longer live and the registry treats the package as frozen. While live, the vendor appended rows to
the load-factor and result files (each instruction and each week). gridflow has **one capture per resource** (all
2026-10-08), so whether any file was later amended is unmeasured. Activation (RULINGS 792, window
`2026-10-08..2026-10-08`, no prior silver, @.planning/v0.22-RESULTS.md section AS-5b): instructed volumes 49 rows
and load factors 240 rows loaded, 0 recorded transform failures, all exit 0. The V1 upload and the result files are
not transformed. Reconciliation of all families (`reconcile --all`) exited 0 with 0 gaps. The records merged in
PR #119 (RULINGS 789, unit v0.22-K-AS-5b).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow outputs
derived from this package carry the attribution line "Supported by National Energy SO Open Data".

## Holds

- `odfm_market_information_load_factors`: held: TODO: ODFM-LOAD-FACTOR-CLOCK-SCALE — the ODFM load-factor upload does not state the time zone or the period start / end convention of its Datetime labels, nor whether its values are fractional factors or percentage numbers (the market report discusses load factors in percentage terms); which clock and which scale does it publish? (unit v0.22-K-AS-5b)

**Reading the hold.** Two things are unknown about the same file, and either would block publication: the clock
of the `Datetime` labels (which is why event time is `none`) and the scale of the values (fractions versus
percentage numbers, which is why they are loaded unscaled). A vendor dictionary stating both would settle it. Until
then the family is held: its rows exist in silver but nothing from it is published, no value is quoted here, and
nothing is rescaled.

**Resource-level hold (not a family hold).** `ODFM Instructed Volume for 05-07-2020` (V1,
`f0a52698-5f80-4fb7-ad64-ede99015195f`) is held at resource level on `ODFM-INSTRUCTED-V1` (reason in the HOLD table
above). It does not hold the instructed-volume family: V2 is loaded and eligible.

**Open questions that do not hold any output** (K-AS-5-FACTS, carried as non-holding TODOs):

- `TODO: verify` **ODFM-2020-FINAL-TERM**. NESO's contemporaneous consultation response states that the service terms
  ended on 31 August 2020 with a provision to extend by a month
  ([NESO consultation response](https://www.neso.energy/document/172631/download)). The final operative terms and any
  exercised extension were not established, so no row is clipped to an assumed service window and literal report
  dates are kept.
- `TODO: verify` **ODFM-JOIN-CONTRACT**. A vendor definition of forecast-period clocks and a unit-to-region and
  technology mapping would be needed for any analytical join between the three families (see Known issues).
- `TODO: verify` **ODFM-RESULTS-ROW-ID**. A distinct row identity or a corrected results body from the vendor would
  allow a key; today none exists.
- `TODO: verify` the vendor encoding of the two result files (CP1252 is a measured candidate only).
- `TODO: verify` the meaning of the mixed report-period `Date` labels in the 2020 results file.

**Known issues and gotchas.**

- **Only one day of instructed volume.** The instructed-volume family is 49 half-hours on 4-5 July 2020. It is not a
  time series of the service and cannot support a statistical model; the other instruction days appear only in the
  PDF reports.
- **V1 is not a typo-fix of V2.** V2 changes 36 of the 49 volumes, not just the period labels. Comparing versions on
  the faulty V1 settlement-period key would confuse corrections with dropped or new targets. gridflow keeps V2 only
  and never unions or de-duplicates the versions. Never deduplicate settlement data on (date, period) alone.
- **`timestamp_utc` means different things in the two loaded families.** In the instructed family it is the start of
  the settlement period (a real event instant); in the load-factor family it is the **capture time** (not an event
  instant). Do not use it to align the two.
- **No safe join across the three CSV families.** Instructed volumes are system-level date and period observations;
  load factors are regional forecasts at datetime labels; results are unit bids and decisions for daily or weekly
  report periods. A raw `Time` and `Date` label overlap between the instructed volumes and the load-factor labels
  matches 48 of the 49 instructed labels, but that is a diagnostic label overlap only: it does not establish matching
  time zone, issue time or unit-level allocation. Summing accepted capacity is not instructed MW.
- **Load-factor clock and scale are undocumented** (the hold). Do not treat the `Datetime` string as UTC, and do not
  multiply or divide the values.
- **Results exist in bronze only.** Anything that needs unit-level prices or acceptance decisions must read the PDFs
  or wait for a distinct row identity from the vendor.
- **Silver vintage is the vendor stamp, not the capture.** `available_at` is the 2020 CKAN `last_modified` for the
  instructed volumes. A point-in-time query (`WHERE available_at <= :as_of`) therefore sees them from 2020-07-08 even
  though gridflow captured them in 2026.
- **Silver layout.** Both loaded families are written under the activation run's `year=2026/month=10` partition,
  which is the capture month, not the event month.

Related pages: @../../../20-domain/concepts/settlement-period.md, @./aggregated-bsad.md (the AS-4a `sp_pair` plus
`resource_id` key precedent).

## Silver sample

Two instructed-volume rows (V2; the family that is eligible). The engine-stamped columns `bronze_capture_id`
and `source_run_id` are omitted for width; `dataset_version` is `1+e1` on every row.

```python
[
    {
        "settlement_period": 47,
        "odfm_instructed_mw": 0.0,
        "time_label": "23:00",
        "settlement_date": date(2020, 7, 4),
        "resource_id": "5c507a16-d2f3-44df-b1bb-98acc0d74e1c",
        "timestamp_utc": datetime(2020, 7, 4, 22, 0, tzinfo=UTC),
        "event_time": datetime(2020, 7, 4, 22, 0, tzinfo=UTC),
        "published_at": datetime(2020, 7, 8, 13, 37, 56, 620172, tzinfo=UTC),
        "available_at": datetime(2020, 7, 8, 13, 37, 56, 620172, tzinfo=UTC),
        "capture_written_at": datetime(2026, 10, 8, 11, 15, 32, 392120, tzinfo=UTC),
    },
    {
        "settlement_period": 1,
        "odfm_instructed_mw": 66.0,
        "time_label": "00:00",
        "settlement_date": date(2020, 7, 5),
        "resource_id": "5c507a16-d2f3-44df-b1bb-98acc0d74e1c",
        "timestamp_utc": datetime(2020, 7, 4, 23, 0, tzinfo=UTC),
        "event_time": datetime(2020, 7, 4, 23, 0, tzinfo=UTC),
        "published_at": datetime(2020, 7, 8, 13, 37, 56, 620172, tzinfo=UTC),
        "available_at": datetime(2020, 7, 8, 13, 37, 56, 620172, tzinfo=UTC),
        "capture_written_at": datetime(2026, 10, 8, 11, 15, 32, 392120, tzinfo=UTC),
    },
]
```

No sample is given for the load-factor family (held; no data values published) or the results family (no silver).

## Gold layer and modelling

None implemented. No gold view or Parquet builder consumes this package, and no gridflow_models model uses it. The
instructed volumes are a one-day record of a downward-flexibility action the vendor says is already reflected in the
BMRS demand forecast for that day; `TODO: verify` any intended modelling use. The load factors must stay out of any
model until the hold is lifted.

## Links

- [Official dataset page](https://www.neso.energy/data-portal/optional-downward-flexibility-management-odfm-market-information)
- Registry record: @src/gridflow/connectors/neso_data_portal/registry/optional-downward-flexibility-management-odfm-market-information.json
- Eligibility report: @docs/neso_data_portal/eligibility.md
- Evidence: @.planning/phases/v0.22-K-AS-5/K-AS-5-FACTS.md, @.planning/phases/v0.22-K-AS-5/K-AS-5b-SPEC.md,
  @.planning/v0.22-RESULTS.md (section AS-5b); rulings 765, 766, 789, 792 (and 538, 607 for the no-record and V1 hold
  precedents) in @.planning/RULINGS.md
- Domain: @../../../20-domain/concepts/settlement-period.md
