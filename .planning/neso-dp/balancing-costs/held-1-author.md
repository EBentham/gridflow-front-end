# Held pages, Balancing costs part 1: writer report (2026-10-23)

Four held one-table pages, written per ruling 6 and the template's held mode (no chart, frame or notebook). Each `page:` block
is on the canonical note in `C:\gridflow-wt\vault-neso-bc\30-vendors\neso-data-portal\datasets\` (front matter only,
insertions only: 33, 31, 35 and 39 lines; CRLF on every line) and mirrored byte for byte to
`C:\gridflow-wt\fe-neso-bc\vault\neso_data_portal\` (`cmp` clean on all four). No series, samples or notebooks. No body edits.

| Page | Build `--only` | Detector | Screenshots |
|---|---|---|---|
| `bsuos-fixed-tariffs` | `neso_data_portal/bsuos_fixed_tariffs`: ok | `[]` | 1440, 1024, 768, 390 |
| `gb-system-inertia-bid-and-offer-costs` | `neso_data_portal/inertia_bid_offer_costs`: ok | `[]` | 1440, 1024, 768, 390 |
| `balancing-services-use-of-system-bsuos-daily-forecast` | `neso_data_portal/bsuos_daily_forecast`: ok | `[]` | 1440, 1024, 768, 390 |
| `daily-balancing-costs-balancing-services-use-of-system` | `neso_data_portal/daily_balancing_costs`: ok | `[]` | 1440, 1024, 768, 390 |

Screenshots: `.planning\neso-dp\balancing-costs\held-1-shots\` (390 through a 390 px iframe). Measured in iframes at 390, 768,
1024 and 1440: `scrollWidth` equals viewport width on all four, no element outside the viewport, no clipped or scrolling block
(the long request URLs wrap). Rendered text: 0 em or en dashes; none of live, now, yet, soon, pending, coming, planned, shipped,
real-time, locally, ruling, ledger, TODO. No capture dates, row counts or other local figures. My server on 9922 was started
with its PID recorded and stopped by that PID; 9670 not touched. Every `--only` build also reports errors "on pages not rendered
by --only, left for the full build" (2 to 4, from the other writer's in-progress package); none is on my pages.

## Shared evidence (all four pages)

| Claim | Evidence |
|---|---|
| One `package_show`, then each upload downloaded whole unless its `last_modified` matches the newest capture | gridflow `connectors/neso_data_portal/client.py` `iter_members` docstring (1658-1690); every resource here is `url_type: upload` (registry) |
| Every request URL | bronze sidecar `request_url` of each capture under `C:\gridflow-data\bronze\neso_data_portal\<table>\`; `package_show` as in the approved held pages |
| `ingest` / `transform` with `--last 24h` | same form as the approved Ancillary held pages (`cli.py`) |
| The weekly frozen re-check is not mentioned | `_frozen_not_due` (client.py 2409) applies to datastore dumps only; all files here are uploads |
| "BSUoS ... recovers the cost of day-to-day operation of the transmission system" | NESO package text of `daily-balancing-costs-...` (catalogue snapshot 20261006T195819Z) |
| Landscape `market` | balancing costs, as the showcase `constraint-breakdown` |

## 1. BSUoS fixed tariffs (`bsuos_fixed_tariffs`, silver held)

| Claim | Evidence |
|---|---|
| Fixed tariffs "forecasted and set by the revenue team"; updated "when tariffs are published" | NESO package notes; extras `Update frequency: Biannual` |
| Rate in £/MWh for a range of settlement dates | vendor dictionary: "First/Final settlement date the tariff relates to", "BSUoS Tariff in £/MWh" (note) |
| Stage "such as draft or final" | vendor dictionary comment "Final or Draft Tariff" (the body has a third stage; not named, as it is a body observation) |
| Grain: one tariff at one publication stage with its published date | registry entity key `publication, fixed_tariff_title, published_date` |
| Reason: "NESO dates each publication but not when each row appeared, nor whether old rows change." | registry `eligibility.question` (issue clock, availability at Published Date, whether rows are immutable); ledger "publication date not an evidenced issue instant" |
| Commands: ingest and transform | the family has a record, so transform writes (held) silver, as on the approved ASDP page |
| Related: current charges, monthly forecast, daily forecast | all in the page set; the note links the current charge files; monthly is a 24-month rolling forecast (its note); daily forecast ended April 2023 (NESO note) |

## 2. System inertia bid and offer costs (`inertia_bid_offer_costs`, silver held)

| Claim | Evidence |
|---|---|
| Indicative average daily price for BM accepted offers tagged for inertia, including the bid actions required | NESO package notes, near verbatim |
| Method A, B, C definitions | NESO package notes |
| "using all bid prices, not only accepted ones" | NESO: "represent all bid prices in each category and not necessarily the accepted bid price" |
| Cadence "Ad hoc, as NESO lists it" | extras `Update frequency: Ad hoc` |
| Grain: one row per day | registry entity key `date` |
| Reason: "NESO's units disagree, £/GVA or £ per GVAs, and it never says what a zero means." | registry hold question (dictionary £/GVA against package text £ per GVAs; averaging-day window; zero values); ledger "£/GVA vs £/GVAs". The day window is dropped for the 16-word limit |
| Related: constraint breakdown | its field `increasing_system_inertia_cost_gbp`: "Increasing system inertia, £" |

Left out on purpose: the coverage dates (2019-04-01 to 2022-03-31) and the October 2022 `last_modified`. Both are measured
from the capture, not stated by NESO, and the second would go stale on a re-upload.

## 3. Daily BSUoS forecast (`bsuos_daily_forecast`, bronze only)

| Claim | Evidence |
|---|---|
| Half-hourly forecast charge = forecast cost over forecast volume | NESO package notes |
| "may bear no relation to later tariffs" | NESO disclaimer |
| Not active; not updated from April 2023, after CMP361 | NESO note and extras `Update Frequency: Not Active` |
| History: files 2018-19 to 2022-23, data from December 2018 | registry resource names; NESO resource description "data being present from December 18" |
| "Each file mixes historic and future values" | NESO resource descriptions "historic and future ... charge forecast" |
| Units £, MWh, £/MWh | header text and dictionary (note) |
| Reason: "Rows carry no settlement run to key them by, and the header's £ is not UTF-8." | ledger "no run column; bodies invalid UTF-8"; header byte `0xA3` checked in all five bronze files (`od`: octal 243); family has no `record` |
| Requests: `package_show`, 2018-19 and 2022-23 files ("first and last shown") | sidecars; five files need more than the four-request limit |

## 4. Daily BSUoS cost data (`daily_balancing_costs`, bronze only)

| Claim | Evidence |
|---|---|
| Per settlement period, six £ columns | vendor resource descriptions ("On a settlement period basis"); bronze headers; dictionary units £ (note) |
| `SETT_DATE` described as a payment date, titled settlement date | note, Known issues (vendor dictionary) |
| Cadence weekly; newest file is the current financial year | extras `Update Frequency: Weekly`; resources by financial year, newest 2026-2027 (worded as the approved Disaggregated BSAD page) |
| History: one file per April-to-March year from 2017-18 | registry resource names |
| Reason: "Rows carry no settlement run to key them by, so there is no silver table." | ledger "no record (no settlement-run column)"; registry `transformer: null`, no record |
| Workbook bronze only, ingested by `daily_balancing_costs_files` | registry: `bfd081bc` in family `daily_balancing_costs_files`, disposition HOLD; sidecar URL |
| Requests: `package_show`, 2017-18, 2026-27, workbook | sidecars; "first and newest shown" in the note |
| Related: volume, current charges, constraint breakdown, daily forecast | all in the page set; volume covers the same periods (its note) |

## Unverified or judgement calls (checker, look here)

- **The hold line for the forecast and the cost data** says "no settlement run to key them by". It is the ledger's reason, in
  plain words; a reader who does not know runs gets the term explained on the current-charges page, which is linked.
- **Cost data `how_used[1]`**: "An implied cost per MWh, with the volume package for the same periods". The note proposes this
  use; I avoided "by category" because the volume file has eight categories against six here.
- **The missing-periods workbook** is named in the raw-feed note without saying it lists fewer gaps than the files show (60
  against 70 measured). The 70 is a local measurement, so I left it off.
- **Inertia has one related link.** `system-inertia` and `system-inertia-cost` are the natural links but have no page yet (the
  build rejected both). Add them when the System group is built.
- **Titles.** "BSUoS fixed tariffs", "System inertia bid and offer costs", "Daily BSUoS forecast", "Daily BSUoS cost data"
  follow the manifest names, shortened to six words or fewer.

## Open questions

- None blocking.

## Template problems

- None. Held mode rendered as documented for one-table pages with and without silver.

## Defects

- **Vault, `daily-balancing-costs-balancing-services-use-of-system.md` body is stale on captures.** It says the newest capture is
  2026-10-08 and that "only the 2026-2027 resource changed in October 2026". Bronze also holds a 2026-10-16 capture of the
  2026-27 file (`raw_20261016T200131Z_1d040751-...`, `ckan_last_modified` 2026-10-16T06:39:44, 774,080 bytes against 733,417),
  so the per-resource table (bytes, rows, vintage) is out of date for that file. Not a page finding; same pattern as the
  Disaggregated BSAD defect in part 2.
- **Package registry status reads `eligible` on all four** while every table is held or bronze only (known pattern).
- **Manifest lead and member lists are correct** for all four (one table each); no change suggested.
