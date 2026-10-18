# Held pages, Ancillary services part 2: writer report (2026-10-18)

Four held pages, written per ruling 6 and the template's held mode. Each `page:` block is on the canonical note in
`C:\gridflow-wt\vault-neso-as-b\30-vendors\neso-data-portal\datasets\` (front matter only, insertions only: 32, 34, 34
and 51 lines; CRLF kept on every line) and mirrored byte for byte to `C:\gridflow-wt\fe-neso-as-b\vault\neso_data_portal\`
(`cmp` clean on all four). No series, samples or notebooks (a held page has none). No body edits.

| Page | Build `--only` | Detector | Screenshots |
|---|---|---|---|
| `contract-transfer-of-obligation` (one table) | `neso_data_portal/contract_transfer_obligation`: ok | `[]` | 1440, 390 |
| `disaggregated-bsad` (one table) | `neso_data_portal/disaggregated_bsad`: ok | `[]` | 1440, 390 |
| `non-bm-ancillary-service-dispatch-platform-asdp-window-prices` (one table) | `neso_data_portal/asdp_window_prices`: ok | `[]` | 1440, 390 |
| `obligatory-reactive-power-service-orps-utilisation` (family of 3) | `neso_data_portal/orps_utilisation_reactive`: ok | `[]` | 1440, 390 |

Screenshots: `.planning\neso-dp\ancillary-b\held-b-shots\` (390 through a 390 px iframe; I also read each 390 view in
1600 px slices). Nothing clipped or overlapping at either width. Rendered pages: 0 em dashes; none of live, now, yet,
soon, pending, coming, planned, shipped, real-time, locally. Every build prints the vault-wide warning about 22
"Known issues and gotchas" lines the caveat grammar drops; it is vault-wide, predates this work and does not fail the
build (my edits touch front matter only). My server on 9979 is stopped.

## Shared evidence (all four pages)

| Claim | Evidence |
|---|---|
| A request is `package_show`, then an upload's `resources[].url` (downloaded whole, skipped when `last_modified` matches the newest capture) or a datastore dump (kept only if its body changed) | gridflow `connectors/neso_data_portal/client.py` `iter_members` (1658-1780) docstring and body |
| Every request URL on the pages | the bronze sidecar `request_url` of each capture under `C:\gridflow-data\bronze\neso_data_portal\<table>\`; `package_show` URL from `endpoints.py:49` `CKAN_ACTION_PREFIX` plus the package name |
| `ingest` and `transform` take `--last 24h` | `cli.py` `ingest` (186), `transform` (261); same form as part 1 |
| Landscape `market` | as part 1's ancillary-service pages |
| Hold reasons | registry `eligibility.question` per family (ORPS, ASDP) and the notes' Identity sections (the two bronze-only tables), in plain words |

## 1. Contract transfer of obligation (`contract_transfer_obligation`, one table, bronze only)

| Claim | Evidence |
|---|---|
| A provider can ask NESO to move a Balancing Service contract from a contracted unit to a non-contracted one | vendor wording quoted in the note (opening paragraph) |
| Columns: participant, product, executed MW, clearing price £/MW/h, delivery dates, receiving unit, status | vendor dictionary table in the note; bronze header `registeredAuctionParticipant ... Transfer Status` (10 columns, no id column) |
| Cadence: ad hoc, updated only when a transfer request arrives | vendor metadata "Update frequency: Ad hoc" and package text, both in the note |
| Reason: "Identical rows repeat and no transfer id tells them apart, so there is no silver table." | note, Identity (12 rows, 7 distinct); re-checked on the only capture: 5 excess rows; registry family has no `record`, `transformer: null`; RULINGS 538 |
| "NESO does not say whether rows that repeat exactly are separate transfers, nor what clock the delivery dates use" | note TODOs CONTRACT-TRANSFER-IDENTITY and CONTRACT-TRANSFER-PERIOD |
| Command is ingest only (no transform line) | no record, so a transform writes nothing |
| Related: EAC BR and EAC results "among the tags NESO gives this log"; the BR requirement forecast | package tags in the note (BR Auction Results on EAC, EAC-BR Auction Results, Reserve and Response Auction Results); the note's own reference to the BR requirement forecast |

Left out on purpose: that every captured row is Balancing Reserve, that `auctionUnit` is blank, the swapped
`serviceType`/`auctionProduct` and the date-only labels. All are observations of one capture, not vendor statements.

## 2. Disaggregated BSAD (`disaggregated_bsad`, one table, bronze only)

| Claim | Evidence |
|---|---|
| BSAD is how NESO submits non-BM balancing actions into settlement; this package is per action | note opening; aggregated showcase wording |
| `T` system action, `F` energy action | vendor column table in the note |
| "NESO's methodology numbers each action in its settlement submission, but the portal files carry no such number" | note: the methodology and BSC Section Q require a sequential identity; "The portal CSVs do not publish that identity" |
| "NESO does not define what the cost's sign means" | note TODO DISAGGREGATED-BSAD-COST-SIGN (no vendor cashflow-sign definition) |
| Cadence: "NESO states no update frequency; 2026-27 is the current, partial year" | note Cadence ("The vendor update frequency is not stated"); Files ("2026-27 is the current, partial year") |
| History: one file per April-to-March year, 2013-14 to 2026-27 | registry: 14 resources named "Disaggregated BSAD 2013-14" to "2026-27" |
| Uploads to 2020-21, datastore dumps from 2021-22 | registry `url_type` per resource; sidecar `request_url`s |
| Reason: "Identical rows repeat and no action id tells them apart, so there is no silver table." | note, Identity (all 14 bodies); re-checked on the newest 2026-27 capture (16 October): 10,096 excess rows of 77,444; no `record`; RULINGS 538 |
| Requests shown: `package_show`, the 2013-14 upload, the 2026-27 dump | one example of each kind; 14 files will not fit the four-request limit, and the raw-feed note names both kinds |
| Related `elexon/disbsad`: "each with an action number" | Elexon DISBSAD page field `adjustment_action_id` ("Action number as Elexon sends it in `id`"). I do not claim the two feeds hold the same actions |

## 3. ASDP window prices (`asdp_window_prices`, one table, silver held)

| Claim | Evidence |
|---|---|
| Window-price changes sent by providers of Non-BM STOR and Non-BM Fast Reserve to ASDP | CKAN package notes quoted in the note; `service_type` values in the note |
| Columns: provider, asset, service, window start and end, price, creation time | registry epoch header (8 columns) |
| `EntryID` points to the instruction table but repeats, so it does not identify a row | vendor dictionary "EntryID from Instruction Dispatches"; registry entity key `resource_id, created_time, asset_id` (not `entry_id`) |
| Never join ASDP ids to OBP ids; the services moved to OBP | note: vendor states the migration; "never match, union or join the ASDP identifiers to any OBP identifier" |
| Cadence: NESO lists it as not active | vendor metadata "Update frequency: Not Active" |
| "gridflow re-checks it at most weekly" | registry `refresh: frozen`; `client.py:107` `_FROZEN_CADENCE = timedelta(days=7)`, `_frozen_not_due` (2409) |
| Two calendar-year datastore tables, 2025 and 2026 | registry resource names "Non BM Window Price Change_2025/_2026", both `datastore` |
| Reason: "NESO gives `WindowPrice` no unit, and does not say if times are UTC or UK local." | registry hold question ASDP-WINDOW-PRICE-UNIT, including its note that the times have an undocumented export clock |
| Related: instructions, OBP prices, OBP instructions | note's own related list; all three are in the page set |

## 4. ORPS reactive power utilisation (family of three, every table held)

| Claim | Evidence |
|---|---|
| Grid Code generators must be able to absorb or produce reactive power, which NESO calls on to manage voltage near their connection | vendor package text, note opening |
| Lead = absorbed, lag = produced | "the vendor's historical dictionary reads leading as absorption and lagging as generation/export" (note) |
| "in MVArh as NESO's package text states; the historic file's dictionary says MVAr" | note, historic family's Unit paragraph (the conflict is recorded there, not resolved) |
| Cadence: monthly; updated mid-month with data to two months earlier | vendor "Update Frequency: Monthly"; resource descriptions in the note's Cadence |
| Package: four CSV files, a workbook and two PDFs | registry resources (4 CSV, 1 XLSX, 2 PDF) |
| `orps_utilisation_reactive`: April 2020 to December 2024, plus NESO's newer long file | resource names; the long file `528b03d2` is registered to this family (resource-level HOLD, bronze only) |
| Reason: "NESO's newer long file differs from this archive; NESO does not say which is right." | registry ORPS-REACTIVE-ARCHIVE ("is this archive superseded ...") |
| `orps_utilisation_historic_reactive`: October 2013 to March 2020 | registry epoch header, first column `Oct 13 - LEAD`, last `Mar 20 - TOTAL` |
| Reason: "NESO does not say what a `-` cell means; one unit appears twice, with different values." | registry ORPS-HIST-DASH / ORPS-HIST-IDENTITY. The identity itself is not named (the note withholds it) |
| `orps_utilisation_reactive_default`: monthly inputs and two rates in £/MVArh | note Units table (NESO guidance document 84286: `X = 1`, `X = 0.2` are £/MVArh) |
| Reason: "NESO labels the power-price inputs `HPIm`, `PAPIm` and `PPIm` only £, with no denominator." | registry ORPS-PRICE-INPUT-UNITS |
| Related: constraint breakdown, "which NESO ties to reactive-power balance" | `constraint-breakdown` field note: "Voltage constraints, £: actions for reactive-power balance and regional voltage (NESO)" |

## Unverified or judgement calls (checker, look here)

- **ORPS raw feed lists the held long file** (`reactive-utilisation-data.csv`) under `orps_utilisation_reactive`. It is
  registered to that family and gridflow fetches it, but no silver row comes from it. The member's `differs` names it;
  its own repeated-row hold is not spelled out. The 16-word limit forced one reason per member, and I chose the
  archive's question, since that is the family's hold.
- **Only one related link on ORPS.** I checked the Elexon BM unit register privately: only 100 of the 243 ORPS
  `unit` names match a `national_grid_bm_unit`, so a link implying the units join cleanly would mislead. Nothing else
  in the page set relates.
- **`elexon/disbsad` related note** says Elexon's rows carry an action number. It does not say they are the same
  actions as NESO's files.
- **Titles.** `disaggregated-bsad` follows the Aggregated BSAD showcase ("... balancing services adjustment data"),
  not the manifest name "Disaggregated BSAD". The other three titles match the manifest names.
- **The `-` in a code span** on the ORPS historic reason reads small at 390. It is legible, but a checker may prefer
  wording without a code span.
- **ASDP "kept only if its body changed"** describes dump hash suppression (`_dump_member`); "re-checks at most
  weekly" is the frozen rule. Both apply to this frozen family.

## Open questions

- None blocking. Should a held one-table page with no silver at all (the two bronze-only tables) still carry a
  "silver, typed and validated" stratum? The template shows it, with the reason. That reads correctly to me, but it is
  a template call.

## Template problems

- None blocking. The held mode rendered as documented for one-table pages with no silver directory, and for a family.
- As in part 1, a held family page prints each member's reason only under "The silver tables", not as "Rows not shown"
  under its raw-feed well. This is consistent with part 1's approved pages.

## Defects

- **Vault, `disaggregated-bsad.md` body is stale on captures.** It says "All 14 resources were captured once, on
  2026-10-08" and "Only one capture per resource exists". Bronze now also holds a 2026-10-16 capture of the 2026-27
  dump (`bronze/neso_data_portal/disaggregated_bsad/2026/10/16/raw_20261016T200513Z_2be1a4d1-..._a0dbc7d2.csv`,
  77,444 rows against 71,517 on 8 October: the current year grew, so it is not truncated). Its excess identical rows
  rose from 9,673 to 10,096. The ledger row ("14 resources in bronze") is still true.
- **Package registry status reads `eligible` on all four packages while every table is held or bronze only** (same
  pattern as part 1; the notes explain it as the package registry entry).
- **Manifest lead and member lists are correct** for all four; no change suggested.
