# Transmission Entry Capacity (TEC) register: writer's report

Page `transmission-entry-capacity-tec-register`, one table `tec_register` (eligible), lead key
`neso_data_portal/tec_register`. Writer, 2026-10-24.

## Status

- Build `uv run --system-certs --extra build gridflow-build --only neso_data_portal/tec_register`: OK (the
  "37 line(s) in Known issues ... dropped" warning is the build's global caveat-grammar notice, not this page).
- Detector `detect.mjs --json`: `[]`. Em dashes on the page: 0.
- Canonical note `C:\gridflow-wt\vault-neso-cr\30-vendors\neso-data-portal\datasets\transmission-entry-capacity-tec-register.md`
  (CRLF kept: 538 CRLF / 538 LF), mirrored to `C:\gridflow-wt\fe-neso-cr\vault\neso_data_portal\`, `cmp` identical.
- Artefacts (all from real data): `site/hifi/data/series/neso_data_portal/tec_register.json` (gridflow-distil,
  `spec_origin: vault`), `samples/neso_data_portal/tec_register.json` (gridflow-sample),
  `notebooks/neso_data_portal/tec_register.json` + `tec_register-5.png` (run_notebooks.py, 5 cells, no errors).
- Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe), static server on 9841 started with a
  recorded PID and stopped by that PID. Fixes made from them: the bar label "Pumped storage, others" clipped at
  390 (now "Pumped and others"); backticks showed literally in a key `codes` string; a codes line ran to the
  edge at 1024 (Tidal moved to the note). The site has no dark theme (no `prefers-color-scheme` in
  `theme.css` or `tokens.css`), so the dark capture is identical to light.

## What one row is (stated plainly)

One row is a project that holds a TEC contract, or one stage of a staged project (NESO: "Stage refers to Staged
TEC", stage-suffixed `Project Number`). TEC is "the amount of generation capacity ... contracted to inject" into
the NETS (package description). Each row carries: `mw_connected` (MW connected; 0 until built), 
`mw_increase_decrease` (MW "contracted to connect or be removed at a future date"), `cumulative_total_capacity_mw`
(NESO: "total ... across all Stages"; measured: a running total through the stages), `mw_effective_from`,
`project_status`, `plant_type` (`;`-joined lists for mixed sites), `connection_site`, `host_to`, `agreement_type`,
`gate`, `project_id`, `project_number`. Units: MW for the three MW columns, `number` for stage and gate (vendor
dictionary). Dates: the only vendor date is `mw_effective_from`, "Date on which Connection is contracted to be
effective from"; NESO keeps it "until the project is Built & Connected therefore past dates may still be seen";
empty when no future connection or change. `timestamp_utc` is the capture time, `published_at` the CKAN
`last_modified` of the file read as UTC.

## Captures, row counts, repeats

| Capture | File | CKAN last_modified | Rows | Header | In silver |
|---|---|---|---|---|---|
| bronze 2026-10-08 11:38Z | `tec-register-05-october-2026.csv` | 2026-10-06T10:47:29.757067 | 2,196 (2,196 distinct) | 15 cols, `Gate` | yes, the only capture |
| bronze 2026-10-16 20:47Z | `tec-register-16-october-2026.csv` | 2026-10-16T18:04:05.092073 | 2,226 (2,226 distinct) | identical 15 cols | no: date cast fails |

No repeated rows in silver (one capture; 2,196 distinct over all 15 vendor columns). The chart and frame filter
`published_at = 2026-10-06T10:47:29.757067` (dates every count to NESO's file) and carry `dedup:` on all 15
entity-key columns ordered by `capture_written_at` as a guard against a recapture of the same file
(distil: `duplicates_dropped: 0`).

## Chart and frame

- Chart: bar, `mw_increase_decrease` summed by `plant_type` grouped into eight buckets, every row of the file named
  for 5 October 2026 (uploaded 6 October). Values (series file): storage alone 176,055.23; solar with storage
  139,876.70; other combinations 119,201.08; wind alone 106,795.18; gas alone 29,594.00; pumped and others
  10,720.10; nuclear alone 7,620.00; solar alone 6,938.61; total 596,800.9 MW. Additive: every row's increment is
  its own (stage increments do not overlap, see evidence), no negatives. The cumulative column is deliberately not
  summed. Mixed `;` lists are not split (NESO does not split their MW); the key says so.
- Frame: eight rows of the same file: Almondell Lodge (Embedded, Built with 0 MW connected, gate 2, past date
  2024-04-30), the Immingham pair `PRO-000053` (Built 1,268 MW; Scoping +50 MW, cumulative 1,318), Springwell
  stages 1 to 3 (400/800/1,600 running total), Zenobe Blackhillock stages 1 and 2 (200 Built, +100 MW, 300).
- Notebook (`data.sql` on `silver_neso_data_portal_tec_register_latest`): MW connected and due by status
  (Scoping 484,036.22 MW due; Built 82,011.71 MW connected), a check that the cumulative column is the running
  total of `mw_connected + mw_increase_decrease` over stages (262 staged rows, max gap 0.01 MW), and a stacked bar
  of GW due by contracted effective year and status, labelled as contract dates, not history.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| TEC definition, existing and future, direct and embedded (`what_it_is`) | Catalogue snapshot `20261006T195819Z`, package `notes` |
| Twice weekly, Tuesdays and Fridays (`facts.cadence`) | Same snapshot, resource description: "updated twice weekly on Tuesdays and Fridays"; extras `Update Frequency: Twice weekly` |
| "each file replaces the last" | Resource description "latest version of the TEC Register including all changes up to publication"; one resource (`num_resources: 1`), filename changes, resource id fixed (both sidecars) |
| Aggregation may duplicate entries | Package description note 1 |
| Grain: project or stage | Dictionary `Stage` and `Project Number` comments; silver 262 staged rows, all stage-suffixed |
| Key `project_number`, with Immingham exception | Dictionary "Unique Project Number"; silver: 2,195 distinct of 2,196, pair `PRO-000053`; resource description on "two separate lines without numbers" |
| Running total in `cumulative_total_capacity_mw` (field, notebook) | Polars on silver: 259 of 262 staged rows exact, all within 0.01 MW; notebook output `count 262.00, max 0.01` |
| No negative `mw_increase_decrease` | Polars: 0 rows < 0 in silver; field and caption scoped "here" |
| `mw_connected` 0 until built | Dictionary comment |
| Past effective dates kept until built | Dictionary comment on `MW Effective From` |
| Status not authoritative | Dictionary comment ("as far as we are aware") |
| Gate 1 or 2, blank until countersigned | Dictionary comment; package description |
| `agreement_type` values vs dictionary | Silver values `Direct Connection`, `Embedded`; dictionary "Directly Connected or Embedded" |
| `host_to` NGET, SHET, SPT, OFTO | Dictionary comment; silver values |
| `published_at` is file last_modified read as UTC | Registry `vintage: ckan_last_modified`; ADR-030 D-15; silver value equals sidecar `ckan_last_modified` |
| `timestamp_utc` is the capture time | Registry `temporal: none`; silver value 2026-10-08 11:38:27.452947 = sidecar `written_at` |
| Requests (`raw_feed.requests`) | `client.py` `iter_members` (`package_show` then download); download URL = 2026-10-08 sidecar `request_url` |
| Unchanged file not re-downloaded (`raw_feed.note`) | `client.py` `iter_members`: upload member with matching `last_modified` yields `unchanged` |
| 16 October file writes dates year first; transform fails (`raw_feed.note`) | Bronze 2026-10-16 CSV: 1,858 of 1,858 populated dates `yyyy-mm-dd`, 0 `dd/mm/yyyy`; registry format `%d/%m/%Y`; `casting.py:267-268` strict strptime; gridflow `.planning/phases/v0.22-close/refresh-20261016/DRIFT.md` row `tec_register | str→date cast` |
| Commands `--last 24h` | Same CLI form as the approved NESO register pages (dm_requirements); `_assert_window_admissible` refuses an end more than 48 h stale |
| `query()` filters `timestamp_utc`, so `data.sql` (`notebook.lead`) | Batch "Checked facts" (remediation 20at); `_latest` view read in the notebook run |
| Chart numbers and alt | Committed series file values; alt rounds them |
| Plot alt | Notebook PNG; Polars pivot by year and status (2037 90.19 GW, 2033 84.42 GW, 2025 4.79 GW, no 2021 rows) |
| Related | embedded-register header (same columns minus `Agreement Type`, registry); interconnector-register header (import/export columns); tresp-generation-pathways summary; bmunits_reference `registered_capacity_mw` |

## Body corrections (canonical note)

1. Units and value rules, `mw_effective_from`: added that the 2026-10-16 capture writes `yyyy-mm-dd` (1,858 of
   1,858) with two-decimal MW and stage values, and fails the record's strict `%d/%m/%Y` cast, so it is not in
   silver (casting.py:267-268; DRIFT.md).
2. Identity: replaced "The cumulative column is not a stage-repeated total ... TODO" with the measured running-total
   rule (259/262 exact, 262/262 within 0.01 MW), scoped as measured on the 2026-10-08 capture, not a vendor rule.
3. Identity: "The columns are not an accounting identity" now explains the 135 rows (134 staged running totals, plus
   the Immingham Scoping row = 1,268 + 50).
4. Identity: the Immingham pair is explained by NESO's resource description (two unnumbered lines, second "will fall
   away"); the 2026-10-16 file numbers them `PRO-000053-1`/`-2` and `Project Number` is unique there.
5. `_latest`: replaced the cross-capture stability TODO with the bronze comparison (2,192 numbers in both keep their
   `project_id`; 3 numbers and 1 id dropped, 34 numbers and 29 ids added); silver vintages still one.
6. Cadence: added "Tuesdays and Fridays" (resource description) and replaced the skip-rule TODO with the code rule
   (`iter_members`); bronze holds two captures, silver one.
7. Known issues: "Dictionary date format is wrong" became "The date format changed between files"; the duplicates
   bullet no longer says stage overlap is unestablished.
8. Implementation delta: date-format and `Gate` bullets updated for the second capture.
9. Modelling notes: "Only one capture exists" replaced with one silver vintage, the second failing the transform.
10. Front matter `updated:` 2026-10-16 to 2026-10-24.

## Unverified

- How a TEC decrease is written in `MW Increase / Decrease` (negative or not): no negative value exists in either
  file; the page says only "none negative here".
- Whether NESO files after 16 October 2026 keep the year-first format (only two captures exist).
- The meaning of a blank `Gate` beyond the dictionary comment (existing TODO, untouched).

## Open questions for the seat

- Ship or hold: I recommend ship with the loss stated. Silver is accurate for the one capture it holds, the chart,
  frame and notebook are dated to that file, and the raw feed note says plainly that the newer file fails the
  transform. A reader who ingests today cannot reproduce the notebook until the record accepts both date formats;
  the notebook `needs` line says only "a capture of the TEC register file".
- Key: `record.key: [project_number]` is the vendor's "Unique Project Number"; the frame shows the one exception
  (Immingham) and the guide says so. gridflow's own entity key is all 15 columns, which is not useful as a Key line.

## Template problems

- None blocking. Minor: a key `codes` string is printed as code, so backticks inside it appear literally (worked
  around by removing them).

## Defects (pasteable)

- **gridflow / neso_data_portal `tec_register`: date format change breaks the transform.** NESO's TEC register file
  of 16 October 2026 (`tec-register-16-october-2026.csv`, CKAN last_modified 2026-10-16T18:04:05Z, 2,226 rows, header
  unchanged) writes `MW Effective From` as `yyyy-mm-dd` (1,858 of 1,858 populated) and numbers with two decimals;
  the 5 October file wrote `dd/mm/yyyy`. The registry record parses `%d/%m/%Y` only and `casting.py:267-268` casts
  strictly, so the capture fails and silver stays at the 2026-10-08 capture. Already listed in
  `.planning/phases/v0.22-close/refresh-20261016/DRIFT.md` (`tec_register | str→date cast`); this adds the
  diagnosis. Fix: accept both `%d/%m/%Y` and `%Y-%m-%d` for this column (an `alt_formats`-style list for `date`
  dtype; today `alt_formats` is handled only on the datetime path), then re-transform the 2026-10-16 capture.
  The header is unchanged, so a new header epoch cannot select the format. Check `embedded_register` and
  `interconnector_register`, which share the layout and publisher.
- **Vault note (fixed here):** the cumulative-column TODO and the Immingham "unresolved duplicate" were answerable from
  the data and NESO's resource description; corrected in the canonical note.
