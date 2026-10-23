# Held pages, Balancing costs part 2: writer report (2026-10-23)

Three held pages, written per ruling 6 and the template's held mode (no chart, frame or notebook). Each `page:` block is on
the canonical note in `C:\gridflow-wt\vault-neso-bc\30-vendors\neso-data-portal\datasets\` (front matter only, insertions
only: 38, 81 and 86 lines; CRLF on every line) and mirrored byte for byte to `C:\gridflow-wt\fe-neso-bc\vault\neso_data_portal\`
(`cmp` clean on all three). No series, samples or notebooks. No body edits.

| Page | Build `--only` | Detector | Screenshots |
|---|---|---|---|
| `daily-balancing-volume-balancing-services-use-of-system` (one table, bronze only) | `neso_data_portal/daily_balancing_volume`: ok | `[]` | 1440, 1024, 768, 390 |
| `bsuos-monthly-forecast` (family of 8) | `neso_data_portal/bsuos_monthly_forecast_actual_sum`: ok | `[]` | 1440, 1024, 768, 390 |
| `skip-rates` (family of 11) | `neso_data_portal/skip_rates_behind_constraints_bmu`: ok | `[]` | 1440, 1024, 768, 390 |

Screenshots: `.planning\neso-dp\balancing-costs\held-2-shots\` (`volume-*`, `monthly-*`, `skip-*`; 390 through a 390 px iframe).
Measured in iframes at 390, 768, 1024 and 1440: `scrollWidth` equals the viewport on all twelve views, no element outside the
viewport, no request well or list scrolls (long URLs wrap). Rendered text: 0 em or en dashes; none of live, now, yet, soon,
pending, coming, planned, shipped, real-time, locally, ruling, ledger, TODO, RULINGS, E-SEM; pound signs render (no mojibake).
No capture dates, row counts or other local figures on any page. The builds print only the known vault-wide warning (35
"Known issues" lines dropped by the caveat grammar); no errors on any page. My server on 9923 was started with its PID recorded
(Windows PID 33488) and stopped by that PID; 9670 not touched.

## Shared evidence (all three pages)

| Claim | Evidence |
|---|---|
| `package_show`, then each upload downloaded whole unless its `last_modified` is unchanged | gridflow `connectors/neso_data_portal/client.py` `iter_members`; every resource in the three packages is `url_type: upload` (registry JSON) |
| Every request URL | bronze sidecar `request_url` of each capture under `C:\gridflow-data\bronze\neso_data_portal\<table>\`; `package_show` as in the approved held pages |
| `ingest` / `transform` with `--last 24h` | same form as the approved held pages (part 1, Ancillary) |
| Hold lines | the ledger row's question for each table (`gridflow\.planning\v0.22-FE-LEDGER.md` rows 66, 69, 70), the registry `eligibility.question` per family, and the seat ruling for the two eligible skip tables |
| Landscape `market` | balancing costs, as part 1 |
| No stale capture fact | bronze checked for every table: the volume 2026-27 file and seven skip files have a second capture (16 October); no page states a capture date, size, row count or "newest capture" |

## 1. Daily BSUoS volume data (`daily_balancing_volume`, bronze only)

Written as the twin of the approved cost page, with that page's review nits applied up front (BSUoS expanded, plain hold
wording, "everything is bronze only", "implied overall cost").

| Claim | Evidence |
|---|---|
| Reason: "Rows are not labelled with a settlement run, so there is no silver table." | ledger row 66 "no record (653)"; registry: no record, `transformer: null`; note "Identity and the blocker" (no run column) |
| BSUoS "recovers the cost of day-to-day operation of the transmission system" | NESO package notes (catalogue snapshot 20261006T195819Z) |
| Eight MWh columns, named | bronze header and vendor dictionary (field-info 20261008T114228Z `daily_balancing_volume.json`: every value column `unit: MWh`) |
| `SETT_DATE` titled settlement date, described as a payment date | same dictionary: title "Settlement Date", description "The Payment Date in relation to an Initial Settlement Run." |
| Cadence weekly; newest file is the current financial year | extras `Update Frequency: Weekly`; resources by financial year, newest 2026-2027 (worded as the approved cost page) |
| History: one file per April-to-March year from 2017-18 | registry resource names "Daily Balancing Volume 2017-2018" to "2026-2027" |
| Requests: `package_show`, 2017-18, 2026-27, workbook | sidecars; "first and newest shown" in the note |
| Commands: ingest `daily_balancing_volume` and `daily_balancing_volume_files` | registry families; workbook `5cb7f9f2` in `_files`, disposition HOLD |
| Related: costs, current charges, constraint breakdown | all in the page set; the costs note covers the same settlement periods |

Left out: NESO's "60 missing settlement periods" (vendor text) and the 70 gaps measured; neither is needed for a held page.

## 2. Monthly BSUoS forecast (family of 8, every table held)

| Claim | Evidence |
|---|---|
| 24-month forecast, monthly, "may not bear relation to ... tariffs" | NESO package notes and disclaimer; extras `Update Frequency: Monthly` |
| By category, with an estimated BSUoS volume; costs in £m | fc_summary dictionary: cost components £m, `Estimated BSUoS Volume` TWh |
| Older files: outturn summaries and COVID demand scenarios | resource descriptions: "Outturn BSUoS for the previous twelve months"; "demand reduction of 5% due to COVID restrictions"; the two COVID forecasts with and without new services |
| Vendor: 142 CSV files, a zipped workbook archive and a PDF | registry: 142 CSV, one `.zip` served under an XLSX label, one PDF |
| History: files from March 2020 | resource names, earliest `Mar_20` |
| `fc_summary` reason: "NESO does not say when each monthly edition was issued, only when its file last changed." | ledger row 69 and registry question (issue instant of each edition; filename month is an edition label; forward-target rule fails) |
| Other seven: "The header's £ is not valid UTF-8, so gridflow keeps these files (this file) in bronze only." | ledger "7 other monthly families no record"; RULINGS 667 in the note. Re-checked on every capture: all 22, 12, 1, 1, 18 and 12 files of the six families are invalid UTF-8, and every invalid byte is `0xA3` in the header row |
| `sum_winter`: "One header £ is not valid UTF-8" | its header mixes valid UTF-8 with a single bare `0xA3` (one invalid byte, in the header) |
| Differs lines | resource names and descriptions in the snapshot; actual summaries 22 files `Mar_20` to December 2021 |
| Commands: ingest and transform `fc_summary`, ingest `_files` | only `fc_summary` has a record; `bsuos_monthly_forecast_files` holds the archive and PDF |
| Related: current charges, fixed tariffs, daily costs, daily forecast | all in the page set |

## 3. Skip rates (family of 11, every table held)

Seat ruling applied: `skip_rates_summary` and `skip_rates_stage5_psa_technology` ship held although the ledger lists them
eligible; their line is the hub's reason in plain words.

| Claim | Evidence |
|---|---|
| A skip: available, better-priced BM volume not taken; LCP Delta method; exclusions by stage | NESO package notes; note's vocabulary (NESO documents 350061, 379301) |
| Cadence daily; some files uploaded monthly | extras `Update frequency: Daily`; descriptions "This dataset is uploaded monthly" (stage 6 PSA), "will be published monthly" (behind constraints BMU) |
| 77 CSV files; three tables as monthly files from December 2024 | registry (77 uploads, three 23-resource families); resource names from December 2024 |
| Behind constraints (2 tables): "NESO's dictionary and methodology presentation disagree on what the skip rate is a percentage of." | registry question CONSTRAINT-RATE-DENOMINATOR |
| Exclusion reasons, stage 6 acceptance, stage 6 PSA: "NESO does not say whether each five-minute time marks the start or end of its slice." | registry question SKIP-DATE-ENDPOINT |
| All BM and PSA detail: "...; some monthly files are partial." | registry questions SKIP-DATE-ENDPOINT plus the coverage questions. Re-checked: the September 2026 files of both hold 30 September only and the PSA March 2026 file stops at 2026-03-24T15:45; none has a newer capture |
| DSF (2 tables): "Identical rows repeat and no column tells them apart, so there is no silver table." | ledger "2 DSF resources no record (exact duplicate rows)". Re-checked on the newest (16 October) captures: 435,526 rows, 427,696 distinct; 7,223 rows, 7,031 distinct |
| Summary and stage 5 PSA technology: "NESO has reissued past rows; the files never say when each row was first published." | seat ruling; NESO resource descriptions record reissues of all published datasets (15/05/2025, 18/11/2025) and a 19/12/2024 update of previous days |
| Related: `elexon/boal`, constraint breakdown | BOAL page is the accepted bids and offers; two tables here are skips behind constraints |

## Unverified or judgement calls (checker, look here)

- **"some monthly files are partial"** on All BM and PSA is a body observation of NESO's files (true on the newest captures)
  rather than a vendor statement. It is in the registry question, so I kept it, without dates. Drop it if the checker prefers
  the endpoint reason alone.
- **"(a few shown)"** on the two family pages, not "first and newest": the newest monthly file changes every month, so a
  "newest" label would go stale. The volume page keeps "first and newest shown", as on the approved cost page.
- **Monthly page: archive and PDF have no URL on the page.** They belong to `bsuos_monthly_forecast_files`, which is not a page
  member, and a family page ignores page-level `requests`. The note names them and a command ingests them.
- **`package_show` appears once per family page** (under the lead member), not under every member, to keep 8 and 11 wells short.
- **Skip rates has two related links.** Nothing else in the page set relates closely.
- **Titles** follow the manifest: "Daily BSUoS volume data" (parallel to "Daily BSUoS cost data"), "Monthly BSUoS forecast",
  "Skip rates".

## Open questions

- None blocking.

## Template problems

- A held family page does not print "Rows not shown" under each member in the raw feed, only under "The silver tables"
  (known since Ancillary part 2; consistent).
- A family page cannot list files that belong to a non-member family (the monthly archive and PDF); see above.

## Defects

- **Vault, `daily-balancing-volume-balancing-services-use-of-system.md` body is stale on captures.** It says one capture per
  resource, all on 2026-10-08, and gives 605,496 bytes, 8,826 rows and vintage 2026-10-03 for 2026-2027. Bronze also holds
  `daily_balancing_volume/2026/10/16/raw_20261016T200136Z_e781da74-6c35-4296-81dd-250cee869c19_edf40a60.csv` (639,451 bytes,
  `ckan_last_modified` 2026-10-16T06:39:49). Same pattern as the cost note (part 1 defect). Not on the page.
- **Vault, `skip-rates.md` body is stale on captures.** It says every resource was captured once, on 2026-10-08. Seven files
  have a 2026-10-16 capture: the October 2026 files of exclusion reasons, All BM and PSA, both DSF files, the summary and the
  stage 5 PSA technology file. The DSF repeat counts are unchanged (7,830 and 192 excess rows). Not on the page.
- **Monthly forecast note** ("every resource captured once, on 2026-10-08") is still true: no newer capture exists.
- **Package registry status reads `eligible`** on all three packages while every table is held or bronze only (known pattern).
- **Manifest lead and member lists are correct** for all three (8 and 11 members match the registry families, `_files` aside);
  no change suggested.
