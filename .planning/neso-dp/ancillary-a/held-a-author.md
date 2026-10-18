# Held pages, Ancillary services part 1: writer report (2026-10-18)

Four held pages, written per ruling 6 and the template's held mode. Each `page:` block is on the canonical note in
`C:\gridflow-wt\vault-neso-as-a\30-vendors\neso-data-portal\datasets\` (front matter only, insertions only, CRLF
kept) and mirrored byte for byte to `C:\gridflow-wt\fe-neso-as-a\vault\neso_data_portal\` (`cmp` clean on all four).
No series, samples or notebooks were written (a held page has none). No body edits.

| Page | Build `--only` | Detector | Screenshots |
|---|---|---|---|
| `dynamic-containment-4-day-forecast` | `neso_data_portal/dc_forecast_4d`: ok | `[]` | 1440, 390 |
| `long-term-forecasts-for-dc-dm-dr-requirements` | `neso_data_portal/dc_dm_dr_long_term_fc`: ok | `[]` | 1440, 390 |
| `eac-mock-auction-results` | `neso_data_portal/eac_mock_results_summary`: ok | `[]` | 1440, 768, 390 |
| `eac-br-mock-auction-results` | `neso_data_portal/eac_br_mock_results_summary`: ok | `[]` | 1440, 390 |

Screenshots: `.planning\neso-dp\ancillary-a\held-a-shots\` (390 taken through a 390 px iframe). Nothing clipped or
overlapping at any width. Rendered pages: 0 em dashes. Every build also prints a vault-wide warning about three
"Known issues and gotchas" lines the caveat grammar drops; it predates this work and does not fail the build.

## Shared evidence (all four pages)

| Claim | Evidence |
|---|---|
| A request is `package_show`, then an upload's `resources[].url` redirector (downloaded whole, skipped when CKAN `last_modified` matches the newest capture) or a datastore dump | gridflow `connectors/neso_data_portal/client.py` `iter_members` (1658-1780), `_assert_redirector_url` (1182) |
| Dump URL is `https://api.neso.energy/datastore/dump/<resource id>` | `endpoints.py:275` `build_dump_path`; `config/sources.yaml` `base_url`; every dump sidecar's `request_url` |
| Frozen dumps re-checked at most weekly; an identical dump body is not stored again | `client.py:105-107` `_FROZEN_CADENCE = 7 days`, `_frozen_not_due` (2409), `_dump_member` hash suppression (1874-1962) |
| `ingest` and `transform` take `--last 24h` | `cli.py` `ingest` (186) and `transform` (261) `last` option |
| Every request URL on the pages | the bronze sidecar `request_url` of the newest capture of each table, under `C:\gridflow-data\bronze\neso_data_portal\<table>\` |
| Landscape `market` | ancillary-service pages follow the showcase `eac-br-auction-results` (the template demo had defaulted to `power`) |

## 1. Dynamic Containment four-day forecast (`dc_forecast_4d`, `dc_forecast_4d_history`)

| Claim | Evidence |
|---|---|
| Wide table: `Date`, `Service_Type`, `EFA_1` to `EFA_6`; history adds `Forecast_Created`, `Forecast_Target_Date` | registry `dynamic-containment-4-day-forecast.json` epochs |
| MW per EFA block | current dictionary unit MW; history dictionary spells `MWs` but its prose says megawatts (note, Units) |
| Six four-hour EFA blocks, the first from 23:00 UK time the day before | vendor history dictionary table quoted in the note; NESO EAC explainer doc 277671 |
| Codes `DC-H`, `DC-L`, not defined by NESO | note ("vendor's definition of each is not stated"); silver unique values `['DC-H','DC-L']` |
| Daily, as NESO lists it | note, Cadence (vendor metadata "Update Frequency: Daily") |
| NESO renames the files on each upload | sidecars: 2026-10-08 file `f9bf31f0..._patch.csv`, 2026-10-16 file `465d3c60..._patch.csv`; history `b4634e50...` then `da8aac20...` |
| Request URLs are the 2026-10-16 file names (newest capture) | sidecars `raw_20261016T2001*` |
| Reason, current: "NESO does not say whether the slash dates in `Date` are day first or month first." | ledger row (DC-DATE-ORDER); registry hold question |
| Reason, history: "NESO does not say when each archived forecast was first published." | ledger row (DC-HISTORY-ISSUE: "when was each creation-labelled issue published?") |
| Related: `dynamic-containment-data` (DC, DM, DR results), `eac-auction-results` (products `DCH`, `DCL`) | silver `dynamic_containment_dc_dr_dm_results.service` and `eac_results_summary.auction_product` both contain `DCH`, `DCL` |

Changed from the template's demo draft: "eight rows a file" removed (a capture count); the history reason no longer
says "some creation dates are after the upload" (measured on one capture); the title spells "four-day"; scenery
`market`; request URLs moved to the newest capture; related links widened to four.

## 2. DC, DM and DR long-term forecasts (`dc_dm_dr_long_term_fc`, one-table page, `held: <reason>`)

| Claim | Evidence |
|---|---|
| Twelve-month outlook for DC, DM and DR, High and Low | CKAN package notes quoted in the note |
| One row per creation date, target month, service, EFA block and band | registry entity key `forecast_created, forecast_target_month, service_type, efa, interval` |
| `Possibilities` from 0 to 1 for nine bands, `0-200` to `1600-1800` | vendor dictionary comments quoted in the note |
| "NESO expects the day-ahead requirement to change as delivery nears" | CKAN notes: requirements "likely to change after optimisation closer to real time" |
| Monthly, as NESO lists it | vendor metadata "Update frequency: Monthly" |
| Request | sidecar `request_url` `.../download/dx_future_requirement.csv` |
| Reason: "NESO states no unit or boundary rule for the bands, nor when each forecast was published." | ledger row (DX-LT-INTERVAL: band unit, inclusive endpoint, availability of the creation-dated forecast) |
| Related DM and DR: "requirement in MW for each upcoming day" | DM and DR notes: one row per EFA date and product, MW per EFA block |

## 3. EAC mock auction results (eight `eac_mock_results_*` tables)

| Claim | Evidence |
|---|---|
| Test runs of EAC, not real procurement | NESO calls them outcomes of mock auction runs (note, K-AS-3 FACTS 4.1); registry package hold EAC-MOCK-TEST-DATA |
| Response (DC, DM, DR) and reserve services | silver `service_type` `Balancing Reserve, Quick Reserve, Response, Slow Reserve`; products `DCH ... PSR` |
| Tables mirror the real package's headers | note, Families ("the mock headers are identical to the live modern headers") |
| Grain: one row per mock auction, product and delivery window | entity key `auction_id, auction_product, delivery_start`. Not "half-hour": the summary holds 6,336 30-minute and 792 four-hour windows |
| Mock auction numbers repeat across dates | registry hold ("mock ids 1-22 are reused for different dates") |
| Four datastore dumps plus four daily CSV uploads | registry resources (`url_type` datastore and upload) |
| Weekly, as NESO lists it | vendor metadata "Update Frequency: Weekly" |
| Reason, the four populated tables: "Test-run results, not real procurement; NESO does not say which clock their times use." | ledger (EAC-MOCK-CLOCK; package EAC-MOCK-TEST-DATA) |
| Reason, the four daily tables: "As fetched, NESO's file has a header and no rows, so there is no silver table." | ledger ("4 daily resources header-only, no record"); registry families with no `record`, `empty_allowed: true`; bronze 114 to 303 bytes |

## 4. Balancing Reserve mock auction results (four `eac_br_mock_results_*` tables)

| Claim | Evidence |
|---|---|
| Test runs of Balancing Reserve auctions on EAC | NESO package notes (note, K-AS-4 FACTS 8); package hold EAC-BR-MOCK-TEST-DATA |
| Products `PBR`, `NBR`, read as positive and negative reserve, half-hour windows | silver `auction_product`; every summary window is 30 minutes (1,632 of 1,632); the showcase page uses the same reading |
| Resource names "Mock Balancing-Reserve ... 2023-2024" | registry resource names |
| Cadence: "Treated by gridflow as frozen: re-checked at most once a week" | registry `refresh: frozen`; `_FROZEN_CADENCE`. NESO's own "Daily" metadata and its "14th-23rd February 2024 only" notice disagree, so neither is stated |
| Reason: as package 3 | ledger (BR-MOCK-EXPORT-CLOCK; package EAC-BR-MOCK-TEST-DATA) |
| Related `eac-auction-results` "also buy Balancing Reserve" | silver `eac_results_summary.service_type` includes `Balancing Reserve` |

## Unverified or judgement calls (checker, look here)

- **The "As fetched" wording** on the four daily mock tables describes NESO's file as gridflow fetched it on
  2026-10-13. It is scoped, but it is an observation, not a vendor statement.
- **"real" in place of "live"** throughout the mock pages ("the real auctions these runs rehearse"). I avoided
  "live" because of the site rule; check it reads naturally.
- **Commands include `transform`** although no rows are shown: silver is written and held, which is what the
  silver section says. The daily mock tables are ingest only, and the raw-feed note says so.
- **Request URLs for the four-day forecast go stale on the next upload.** The note says NESO renames the files.
- `differs` on the history file: "each labelled with its creation and target date" matches the columns, not a
  vendor promise about every issue.

## Open questions

- Should the date-order hold on `dc_forecast_4d` still stand? See the first defect: the newest capture settles the
  order by the note's own lift condition. I kept the ledger's reason, since lifting a hold is gridflow's ruling.

## Template problems

- Code spans break at their hyphen at 1440 (`1600-` / `1800` in the long-term what-it-is). A nit, not a clip.
- None blocking. The held mode rendered as documented; members with no silver (the daily mock tables) list and link
  without error.

## Defects

- **gridflow, `dc_forecast_4d` hold (DC-DATE-ORDER) may be ready to lift.** The 2026-10-16 capture
  (`bronze/neso_data_portal/dc_forecast_4d/2026/10/16/raw_20261016T200150Z_..._15019bb0.csv`, CKAN `last_modified`
  2026-10-16T13:05:25) has `Date` values `17/10/2026` to `20/10/2026`: unambiguous day first, and the next four days
  after upload, which is the note's stated lift condition ("an unambiguous current-format date is captured and the
  rolling-horizon contract corroborates it"). Needs a seat ruling; the page still shows the hold.
- **Vault, `dynamic-containment-4-day-forecast.md` body is stale on captures.** It says one capture per family
  (2026-10-08), 8 and 12,932 silver rows; silver now holds two captures for both tables (16 and 25,936 rows,
  2026-10-08 and 2026-10-16). The ledger row records the old counts too.
- **Vault, `dynamic-containment-4-day-forecast.md` front matter says `eligibility: "eligible"`** while both families
  are held (the long-term note says the same and explains it is generated from the package registry, which reads
  `eligible`). The package registry status disagrees with its families' holds in both packages.
