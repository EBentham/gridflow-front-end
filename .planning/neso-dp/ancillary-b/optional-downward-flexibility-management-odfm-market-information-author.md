# Writer report: `optional-downward-flexibility-management-odfm-market-information` (lead `odfm_market_information_instructed`)

Writer, 2026-10-23, port 9987 (server stopped).

**Status:** build `--only neso_data_portal/odfm_market_information_instructed` passes (only the vault-wide "22 lines
dropped" warning); detector `[]`; mirror `cmp` clean; note CRLF throughout (593 of 593 lines). Screenshots at 1440, 1024,
768 and a 390 px iframe in `.planning\neso-dp\ancillary-b\odfm-shots\`: nothing clipped or overlapping. The site has no
dark theme (no `prefers-color-scheme` rule in `theme.css`, `tokens.css` or `site.js`), so light and dark render the same.

Files: canonical note `C:\gridflow-wt\vault-neso-as-b\30-vendors\neso-data-portal\datasets\optional-downward-flexibility-management-odfm-market-information.md`
and its mirror; `site\hifi\data\{series,samples}\neso_data_portal\odfm_market_information_instructed.json`;
`site\hifi\data\notebooks\neso_data_portal\odfm_market_information_instructed.json` and `-5.png`; the built page.

## The four questions

1. **What ODFM was, and what a row is.** NESO's package text (catalogue snapshot `20261006T195819Z`): in its role as ESO,
   with COVID-19 restrictions risking long low-demand periods during 2020-22, it ran ODFM "across the summer periods in
   2020 and 2021"; "The service is no longer live"; ODFM reached downward flexibility from providers it could not access
   through the Balancing Mechanism or the Platform for Ancillary Services. Extras `Status: Not Active`.
   **An instructed row is not per unit and carries no price.** It is one national number per settlement period:
   `settlement_date` (`Date`, `%d/%m/%Y`), `settlement_period` (1..50 guard), `time_label` (`Time`, raw text),
   `odfm_instructed_mw` (float64). NESO's dictionary: unit `MW`, "ODFM instructed in MW", type integer; no sign stated.
   Values here are 0 to 2,194, nine of them 0. The V2 description says it is the "forecast volume of ODFM instructed",
   republished "post event" after a process failure on 4 July. Unit, price, window, MW per bid live only in the results
   files (bronze only: `Price (£/MW/hr)`, `Allocated Registered Service Volume (MW)`, start and cease times labelled BST).
2. **Time columns.** `Date` is `dd/mm/yyyy`, `Time` is `HH:MM`, neither has a zone marker (bronze line 2:
   `47,0,23:00,04/07/2020`). `timestamp_utc` = `event_time` = `settlement_period_to_utc(date, period)` (gridflow
   `utils/time.py:28`, `silver/neso_data_portal/casting.py:611`): period 1 starts 00:00 UK local. In all 49 rows the
   `Time` label equals the period's UK local start (notebook output: "49 of 49"), BST, so 1 hour ahead of UTC. 4 and 5
   July 2020 are not clock-change days; no row is near one. The page claims BST only for these rows ("here"). The
   notebook converts `timestamp_utc` to UTC after `query()`, and its plot axis reads UTC.
3. **Captures and repeats.** One resource loaded, one capture (bronze `raw_20261008T111532Z_5c507a16...csv`, 49 data
   lines). NESO's datastore `total` is 49 (field-info snapshot `20261008T114228Z`), so no truncation. One
   `published_at`, one `bronze_capture_id`, one `resource_id`; (`settlement_date`, `settlement_period`) unique. No
   repeated rows, so no `dedup:`.
4. **Held members.** Load factors: "NESO states neither the clock of its time labels nor whether values are fractions or
   percentages." (from the ledger question on clock and scale). Results: confirmed ingest only (registry
   `transformer: null`, no `record`; no silver directory). "Identical rows repeat and NESO's bid id repeats too, so there
   is no silver table." Measured: 2020 file 7,321 rows with 9 exact duplicate rows; 2021 file 35,574 rows with 170;
   `Unique ID` repeats 250 and 170 times (CP1252 read).

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Summary, history, what_it_is: summers 2020 and 2021, ESO, COVID-19 risk, outside the BM | Package `notes`, snapshot `20261006T195819Z` |
| Cadence: Not Active, service ended | Extras `Status: Not Active`; notes "no longer live" |
| Vendor: five CSV files, eight PDFs | Snapshot resources: Results 2020, Results 2021, Instructed V1, V2, Load Factors (CSV); 8 PDFs |
| Forecast MW, republished after the day to correct errors | V2 resource description |
| Key `resource_id, settlement_date, settlement_period` | Registry `entity_key` |
| Chart: 49 points, 0 to 2,194, 66 at 23:00 UTC, peak 11:30 UTC, 150 at 18:30, zero from 19:00 | Committed series values (checked against silver) |
| Key note: non-zero 00:00 to 19:30 labels; report gives delivery 00:00 to 20:00 | Silver rows; 05.07.20 report description "for delivery on 5th July 2020 between 00:00 – 20:00" |
| Related NDF: BMRS demand forecast already adjusted | V1 and V2 descriptions: "The BMRS Demand forecast has already been adjusted for this." |
| how_used: report lists technologies | 05.07.20 report description (wind, solar, load banks, energy from waste, biomass, CHP, demand turn up) |
| `query()` reads `_latest`, filters `settlement_date` inclusive, orders by it | gridflow_models `_get_method_registry.py:62-96`, `source.py:401-451`; manifest: date col `settlement_date` (DATE), relation `silver_neso_data_portal_odfm_market_information_instructed_latest` |
| Raw requests | Bronze `request_url` of each capture; `package_show` via `endpoints.py:255` against `https://api.neso.energy` |
| `published_at` 8 July 2020, read as UTC | Silver; `ckan_last_modified` 2020-07-08T13:37:56.620172 |

## Body corrections

- Resolved the note's `TODO: verify` on upload order: the CKAN `created` stamps (V1 2020-07-04T21:21:52, V2
  2020-07-07T15:50:39, snapshot `20261006T195819Z`) give the order; V1's later `last_modified` is left unexplained, as
  the catalogue states no reason. Smallest span; nothing else in the body changed. `updated:` set to 2026-10-23.

## Not verified / observations (not on the page)

- NESO's 05.07.20 report description gives "1288MW at 05:00, 2045MW at 10:00 and 2194MW at 12:00". The V2 rows labelled
  05:00 and 10:00 match (1,288 and 2,045), but 12:00 reads 2,181; 2,194 is the 12:30 row. The report predates V2
  (12:15 versus 13:37 on 8 July). Kept off the page.
- V1's description says the new version was uploaded "Monday 07/07/2020"; 7 July 2020 was a Tuesday (V2 `created` is
  2020-07-07). Vendor text slip; not on the page.
- Why the file stops at period 47 of 5 July remains the note's open TODO.

## Open questions

- None blocking. The related link to the NRAPM package was swapped for `elexon/indo` because that package has no page
  in the page set (the hub lists it, but the build says it has no page).

## Template problems

- None new. The long `_latest` relation name in the notebook lead wraps mid-word at 1440 and 390 (as on other pages).

## Defects

- **ODFM 5 July 2020 report and V2 file disagree on the peak time (data, vendor).** NESO's 05.07.20 Market Information
  Report description gives 2,194 MW "at 12:00"; the V2 instructed-volume file has 2,181 MW at `Time` 12:00 (period 25)
  and 2,194 MW at 12:30 (period 26). The 05:00 and 10:00 figures match. No gridflow change; worth a line in the vault
  note's Known issues if a reader compares the two.
- **V1 resource description weekday slip (vendor text).** "uploaded on Monday 07/07/2020": 7 July 2020 was a Tuesday.
  Cosmetic; no gridflow change.
