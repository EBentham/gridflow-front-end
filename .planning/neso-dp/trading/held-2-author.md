# Held Trading pages, part 2: writer report (2026-10-23)

Three held pages, written in the author brief's held mode and under ruling 6. None has a chart, frame or notebook, and no
series, sample, notebook, chart-spec or authored-override file exists for any of the keys (checked).

Each `page:` block is on its canonical note in `C:\gridflow-wt\vault-neso-trd\30-vendors\neso-data-portal\datasets\`.
Each is mirrored byte for byte to `C:\gridflow-wt\fe-neso-trd\vault\neso_data_portal\`, and `cmp` is clean on all three.

**Line endings:** all three notes are still CRLF. The CR count equals the line count: GTMA 438, IC 314, upcoming 322.
The vault diff touches only the new `page:` blocks and `updated:`, which is now 2026-10-23. I made no body edits.

| Page | Build `--only` | Detector | `parse_page_fields` / `anatomy_errors` |
|---|---|---|---|
| `historic-gtma-grid-trade-master-agreement-trades-data` (family, `held: true`) | `neso_data_portal/gtma_trades_data`: wrote, no errors | `[]` | `[]` / `[]` |
| `interconnector-requirement-and-auction-summary-data` | `neso_data_portal/ic_requirement_auction`: wrote, no errors | `[]` | `[]` / `[]` |
| `upcoming-trades` | `neso_data_portal/upcoming_trades`: wrote, no errors | `[]` | `[]` / `[]` |

The builds print only the known repo-wide "Known issues" warning (37 lines dropped).

**Rendered `<main>` text of all three, checked by script:**
- No em or en dashes.
- None of: live, now, real-time, yet, soon, pending, planned, shipped, coming, locally, ruling, ledger, TODO, held, TRD,
  or the hold-question codes.
- "coming" was hit once on upcoming trades (in `how_used`). I reworded it to "settlement periods ahead".
- The viewport meta and `<main>` are present, and each page has one "Rows not shown" block.
- No capture date, byte size, local row count or local first or last date appears.

**Screenshots:** light mode at 1440, 1024 and 768, and at 390 through a 390 px iframe, in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\held-trd2-writer\shots\`.
The 390 views are also cut into `*-390-band*.png`.
- I read GTMA at 1440 and 390, IC at 768 and 390, and upcoming trades at 390.
- Nothing is clipped or overlapping. The long request URLs, the PDF address, the GTMA member keys and the long related
  slugs all wrap.
- Dark mode was not checked: headless flags do not switch the palette.

**Server:** started from Bash on 9863 (PID 13717) and stopped by that PID. Port 9670 was not touched.

## Shared evidence

| Claim | Evidence |
|---|---|
| Rows-not-shown lines | Each comes from the registry hold question for its table (`registry/<package>.json`) and from ledger rows 74, 76 and 78. For GTMA, the seat ruling decides which question applies (below). |
| Request lines | Copied exactly from the sidecar `request_url` of each capture. `package_show` takes the form used on the approved pages. |
| Dump kept only if its body changed; upload skipped when its newest capture carries the live `last_modified` | gridflow `connectors/neso_data_portal/client.py`: `iter_members` 1658-1780 (upload skip 1755-1766), `_dump_member` 1874-1950 (body-hash suppression 1942-1949). None of the three is `refresh: frozen`, so the weekly rule does not apply. |
| Commands | The family keys come from the registry. The form `--last 24h` matches the approved held pages. `ic_requirement_auction_files` is `kind: files`, catalogue only, and has no transformer. |
| Vendor text | Catalogue snapshot `gridflow/.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json`: package notes, extras, resource names and descriptions |
| Dictionaries | Saved field info at `gridflow/.planning/research/neso-snapshots/field-info/20261008T114228Z/{gtma_trades_data,gtma_trades_data_pre,gtma_trades_fy,ic_requirement_auction,upcoming_trades}.json`, plus FACTS sections 3.3-3.5, 3.7 and 3.9 |
| Related targets exist | Every NESO slug is in `site/hifi/data/neso_data_portal.json`. `elexon/soso` and `elexon/fuelhh` are in `elexon.json`. The build resolved all of them. |

## 1. Historic GTMA trades (`gtma_trades_data` lead, `gtma_trades_data_pre`, `gtma_trades_fy`)

### Seat ruling and the two eligible tables

The ledger (row 74) lists `gtma_trades_data` (five of its six files) and `gtma_trades_data_pre` as eligible. The page
is held by seat ruling, following the approved plan and the hub.

Like skip rates, each of these two tables gets one true NESO fact that bears on reading its rows. The hub's reason for
this package is the units ("the cost columns' units are not stated"). That is not true of these two tables: their
dictionaries give `Cost` in £. So I used the unit fact that is true of them, the volume unit:
- **`gtma_trades_data` (15 words):** "NESO's package text says `Volume` is MW, its dictionary MWh; the 2020-21 file repeats
  rows."
- **`gtma_trades_data_pre` (15 words):** "NESO's package text says `Volume` is MW; this file's dictionary says MWh, a trade's
  total."

Neither line claims that gridflow holds the table on that question, so neither misstates the ledger.

Sources:
- The package notes say "the volume in MW". The upload dictionaries give `Volume`, "Total volume for the trade", unit
  MWh. This is in the saved field info for both families and in FACTS section 3.3, which also cites NESO's 2015-16
  dictionary.
- The canonical note itself leaves this open ("`TODO: verify` with NESO which is intended").
- "The 2020-21 file repeats rows" is NESO's 2020-21 upload, which gridflow carves out at resource level. That upload has
  `last_modified` 2021-04-06 and repeats ten identifiers as identical full rows (registry resource HOLD; FACTS section
  3.3). I gave no count on the page.

**Checker:** if the seat prefers the generic "the files never say when each trade was first published", it is also
true. The uploads have no issue column, and the file dates (2020-12-09 and 2021-06-06) are later than every trade they
list (FACTS HISTORIC-GTMA-AVAILABILITY). I chose the unit fact because it is closer to the hub's reason.

### `gtma_trades_fy`

The line reuses the approved enactment wording, unchanged (16 words): "`Cost` is labelled £/h, but NESO describes it as a
total: volume times price times duration." The saved FY dictionary gives `Cost` as £/h, with the description "Total
cost to Nationalgrid ESO for the trade" and the comment "Cost = Volume * Price * Duration". These match the three
enactment dictionaries.

### Evidence

| Claim | Evidence |
|---|---|
| Summary: GTMA trades since April 2015 | Package notes: "historic GTMA (Grid Trade Master Agreement) trades conducted since April 2015" |
| Vendor: seven files, six datastore tables | Registry and snapshot: 7 upload CSVs (six yearly plus Pre June 2021) and 6 datastore dumps (FY 21-22 to FY 26-27) |
| Cadence: monthly; current file each morning, 06:00 to 06:00 | Package notes: "updated on a monthly basis shortly after the start of the month"; "The live data file is refreshed every morning to capture the trades occurred between D-1 06:00 and D 06:00". "Live" is reworded as "current". |
| Grain: one trade, start and end in UTC | Upload dictionary: "Trade start date time (UTC)". FY dictionary: "Start time of the trade in UTC format". |
| History: yearly tables to 2026-27 | Snapshot resource names |
| What it is: identifier, UTC window, volume, price, cost, system flag; total MWh to June 2021; average MW and a reason from 2021-22 | Field info for all three families (`Reason` exists in FY only). NESO's default warning is in the notes: "post-delivery things can change, for example counterparties can default ... the data may not be updated retrospectively". |
| Differs: six yearly files 2015-16 to 2020-21, first and newest shown | Registry: six `gtma_trades_data` uploads, including the 2020-21 HOLD resource, which bronze keeps. The shown URLs are the 2015-16 and 2020-21 sidecars. |
| Differs: one file NESO names Pre June 2021 | Resource name "Historic GTMA Trades Data - Apr 2021 - Mar 2022 (Pre June 2021)" |
| Differs: FY tables, average MW, reason and note | FY dictionary. The shown dumps are FY 21-22 (`11a2f532`) and FY 26-27 (`e7a8abae`). |
| Raw-feed note | `iter_members`: uploads are skipped on an unchanged `last_modified`, and dumps are kept on a changed body |
| Related: upcoming trades | Resource description: "all upcoming GTMA ... trades due to be delivered" |
| Related: contract enactment | Enactment package notes (trading team weighs trades against contracts). This is the reverse of that page's approved GTMA link. |
| Related: IC auctions | IC package notes: a counterparty must have a GTMA in place with NESO |

`page.title` "Historic GTMA trades" is the manifest's family title. `facts.vendor` carries NESO's package title. I did
not use the 52-character slug there, so that it cannot overflow at 390.

## 2. Interconnector requirement and auction summary (`ic_requirement_auction`)

**Reason (16 words):** "NESO updates each lot in place with its auction result; the file keeps no earlier state."
- It comes from the ledger question: lots are mutable forward requirements, later overwritten with outcomes; what was
  available when?
- "In place" and "updates" are NESO's own description: "the information for a given requirement (lot) will be updated
  to include ...".
- "Keeps no earlier state": the dump has one row per `Auction Lot ID` (FACTS section 3.7, T06).

| Claim | Evidence |
|---|---|
| Title | Manifest name "Interconnector requirement and auction summary" |
| Six interconnectors; flows into or out of GB; constraints or margin; ad hoc auctions; qualified counterparties; requirement not firm; updated with volumes per interconnector and prices; GTMA needed | Package notes |
| Cadence "Ad hoc" | Extras `Update Frequency: Ad hoc`; notes "run ad hoc across the day" |
| Vendor: one datastore table and a market notice PDF | Registry: SILVER datastore `6a928369`; DOC upload `74b56acb`, described as a market notice of a limit on NESO's within-day trading from 20 May 2026 |
| Grain: one lot, later updated | Dictionary `Auction Lot ID`; notes |
| Uses: clearing, best and average prices; volume per interconnector | Dictionary: `Clearing Price`, `Best Price`, `VWA Price` and the six per-interconnector volumes |
| Requests | Sidecars: dump `6a928369`; PDF download URL |
| Third command, the PDF family | Registry `ic_requirement_auction_files`, `kind: files`. Bronze holds the PDF. |
| Related `elexon/soso` | The SO-SO page: SO-SO prices for trades across GB interconnectors |
| Related `elexon/fuelhh` | The FUELHH fuel types include INTFR, INTIFA2, INTNED, INTNEM, INTELEC and INTVKL |

No `history` fact: NESO gives no start date for this table.

## 3. Upcoming trades (`upcoming_trades`)

**Reason (16 words):** "NESO labels `Volume` MWh but multiplies it by duration for cost, and gives `Last_Updated` no clock."
This covers both halves of the ledger question:
- `Volume` is titled "Average Volume" with unit MWh, while the `Cost` comment is "Cost = Price * Volume * Duration".
- `Last_Updated` has unit "N/A" and no zone.

The "no clock" wording follows the approved older balancing table.

| Claim | Evidence |
|---|---|
| Upcoming trades due to be delivered; ten-minute refresh; forecast balancing requirements at minimum cost; provisional, correctable after confirmation, not to be relied on | Package notes and resource description |
| GTMA trades | Resource description: "upcoming GTMA ... trades" |
| One row per trade and settlement period | Dictionary: `Date` and `SP` are per trade. The registry key is `(id, date, sp)`. |
| Volume, price, cost, system flag, reason | Dictionary |
| "Each capture is the whole list as it stood" | Registry `latest: whole_capture`; the dump leg replaces the whole body |
| Related links | GTMA: the delivered history (FACTS section 3.9, citing NESO trading material). Enactment and IC: as above. |

No `history` fact: the table is a rolling list.

## Unverified

- Whether NESO has added or renamed resources since the 6 October snapshot. I made no live call. The facts name tables
  as NESO named them then.
- Whether every upload file's dictionary says MWh. Only the 2020-21 and pre-June dictionaries are saved, and FACTS
  cites the 2015-16 one. The gtma_trades_data line says "its dictionary", as the note does.

## Open questions for the seat

1. **GTMA eligible-table lines.** I used the unit disagreement rather than the "first published" reason (see section
   1). Raise either one at the PR with the seat ruling.
2. **Stale capture statements in the notes, not corrected.** All three canonical notes say one capture exists
   (2026-10-08). Bronze now also holds 2026-10-16 captures of the following, and silver has the 16 October runs for each:
   - GTMA FY 25-26 and FY 26-27
   - the IC dump
   - upcoming trades

   The page states none of this. Rewriting those passages is a data-fact refresh across many sentences (the cadence,
   key and hold sections lean on "one capture"). It is not a code-proved correction, so I left it for the seat or a vault
   reconcile.

## Template problems

None new. The family template prints the per-member reasons once, in the silver block, as on the approved enactment
family page.

## Defects

- **NESO, Historic GTMA, package text against dictionary:** the package notes say "the volume in MW". The upload
  dictionaries (2015-16 to Pre June 2021) give `Volume` as "Total volume for the trade" in MWh, and the FY dictionaries
  give an average in MW. Already in the note as a TODO.
- **NESO, Historic GTMA 2020-21 upload:** ten identifiers (`ES00104406` to `ES00104415`) appear twice as identical full
  rows (`last_modified` 2021-04-06). This is unchanged and already a resource-level HOLD.
- **NESO, Historic GTMA FY tables:** `Cost` is labelled £/h against a "Total cost" description, the same as the
  enactment dictionaries. FY 21-22 and FY 22-23 share nine identical rows (adjudicated). Both are unchanged.
- **NESO, Historic GTMA FY 25-26: a closed year was revised (new, data).** Between the 2026-10-08 and 2026-10-16
  captures, the FY 25-26 dump (`bd8a822f`, trades from April 2025 to March 2026) changed:
  - 192 new trade ids were added, and none were removed.
  - 1,245 rows were replaced by 1,437 different rows; the header is the same.

  This means NESO edits and extends a past year's table months after it closed. It supports the note's open question
  on retrospective changes, and it is evidence for any future hold or availability ruling. The note's "no revision
  between captures has been observed" is now out of date.
- **NESO, IC requirement and auction:** `System Flag` does not say which letter means system and which energy. Its
  `ckan_last_modified` stays at 2023-01-23 while the body changes: the 2026-10-16 capture differs from the 2026-10-08
  one at the same stamp. Already in the note as TODOs.
- **NESO, upcoming trades:** the dictionary spells GTMA as "GMTA", labels `Volume` MWh while calling it an average, and
  gives `Last_Updated` no zone. Already in the note.
- **gridflow:** none found. The registry, sidecars, connector and notes agree. The only exception is the stale "one
  capture" statements in the three vault notes (documentation only; open question 2).
- **Manifest:** the lead and members are right. They are `gtma_trades_data`, then `gtma_trades_data_pre`, then
  `gtma_trades_fy`; `ic_requirement_auction`; and `upcoming_trades`. The registry lists `gtma_trades_fy` first, but the
  manifest order (upload lead) matches the page. `ic_requirement_auction_files` is correctly absent from
  `package_tables`, and its PDF appears in the raw feed with its own command.

## Revision: out-of-date "one capture" statements corrected (coordinator request, 2026-10-23)

All three canonical notes now date every capture-specific fact to its capture and add the 2026-10-16 facts. Each was
measured from bronze row by row (read only) and from the silver run row counts.

I started no server or background process for this revision. It changed no page field, and no page line depends on a
single capture:
- The GTMA "repeats rows" line is about NESO's 2020-21 file (`last_modified` 2021-04-06).
- The interconnector line ("keeps no earlier state") holds in both captures and is now directly evidenced.
- The upcoming-trades line comes from the dictionary.

**GTMA** (`historic-gtma-grid-trade-master-agreement-trades-data.md`):
- The FY table now has a 2026-10-16 column. FY 25-26 went from 32,289 to 32,481 rows (3,259,744 bytes); FY 26-27 from
  20,551 to 22,530 (2,225,763 bytes).
- **FY 25-26, a closed year:** NESO added 192 trades, all delivering on 5 and 6 January 2026, each with `Last_Updated`
  2026-10-13T12:15:31. It also filled a blank `Reason` on 1,245 rows, with `Last_Updated` on 2026-10-13. `Volume`,
  `Price` and `Cost` did not change on any shared id.
- **FY 26-27:** 2,062 trades were added and 83 removed (deliveries 12 to 17 August 2026); 712 rows changed in `Reason`
  and `Last_Updated` only.
- The FY vintage range now includes the 16 October `written_at`. The `Reason` and `Note` blank counts are dated to the
  8 October captures.
- In Cadence: the "one per resource" line is replaced. The open question on whether a refresh rewrites rows became a
  stated, measured fact, with "how often" left open.

**Interconnector auctions** (`interconnector-requirement-and-auction-summary-data.md`):
- A second dump row in the files table: 2026-10-16, 28,439 rows, 5,278,600 bytes, sha `d1fc25d1`. The CKAN
  `last_modified` is unchanged at 2023-01-23, so that stamp does not move when the body changes.
- 111 lots were added and none removed. The only two changed rows are the two lots that started after the 8 October
  capture (`2026_10_08-11_43-1` and `-2`):
  - Their blank outcome columns were filled: clearing, best and VWA prices; cleared and bid volumes; volume per
    interconnector.
  - `System Flag` changed from `null` to `F`.
  - `Published DateTime` moved from 10:44:55 to 11:20:10.

  This is a measured case of the overwrite in the hold question, now cited in Holds.
- Dated to their capture: the blank counts, the reversed and equal windows, the vintage, and the key counts (4,767
  auctions on 16 October).

**Upcoming trades** (`upcoming-trades.md`):
- The bronze table now has two columns. The 16 October capture has 48 rows: 3 trades × 16 periods (periods 47 and 48
  of 16 October, then 1 to 14 of 17 October).
- The forward-target property holds in both captures: 48 of 48 starts fall after the 20:47:33 `written_at`.
- `(id, sp)` and `(id, date, sp)` are unique in both captures.
- The two captures share no trade id, so in-place amendments are still unmeasurable; the TODO now says why.
- Disappearance after delivery: the captures agree with it but do not measure it.
- The second sidecar's `ckan_last_modified` (11:00:16, nearly ten hours before the fetch) is recorded against NESO's
  stated ten-minute refresh.

**Gates:**
- CRLF kept, with CR count equal to line count: GTMA 463, IC 335, upcoming 335.
- All three are mirrored, and `cmp` is clean.
- `--only` rebuilt `gtma_trades_data`, `ic_requirement_auction` and `upcoming_trades`, with no errors.
- The detector returns `[]` on all three.
- The rendered text has no dashes and no banned words. "capture" appears only in the approved command comment and the
  upcoming-trades raw-feed note, and neither depends on a single capture.
- No new screenshots: the page fields are unchanged.

**Open question 2 above is resolved by this revision.** New NESO data defects:
- GTMA FY 25-26: NESO added trades to, and edited rows of, a closed year's table in October 2026.
- GTMA FY 26-27: NESO removed 83 past trades.
- Interconnector auctions: `ckan_last_modified` does not move when the body changes.

No gridflow defect.
