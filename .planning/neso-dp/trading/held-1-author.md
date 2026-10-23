# Held Trading pages, part 1: writer report (2026-10-23)

I wrote three held pages using the author brief's held mode and ruling 6. None has a chart, frame or notebook, and no
series, sample or notebook artefact exists for any of the keys. Each `page:` block is on the canonical note in
`C:\gridflow-wt\vault-neso-trd\30-vendors\neso-data-portal\datasets\`. Each is mirrored byte for byte to
`C:\gridflow-wt\fe-neso-trd\vault\neso_data_portal\`, and `cmp` is clean on all three.

**Line endings:** all three notes are CRLF; after the edits, the CR count equals the line count (516, 517 and 284). The
vault diff touches only the new blocks, `updated:` (now 2026-10-23) and one SSEL body span.

| Page | Build `--only` | Detector | Content-model check |
|---|---|---|---|
| `balancing-services-contract-enactment` (family, `held: true`) | `neso_data_portal/bs_contract_enactment_balancing`: wrote, no errors | `[]` | `parse_page_fields` and `anatomy_errors`: `[]` |
| `index-linked-contract-volume` | `neso_data_portal/index_linked_contract_volume`: wrote, no errors | `[]` | `[]` |
| `super-stable-export-limit-contract-enactment` | `neso_data_portal/ssel_contract_enactment`: wrote, no errors | `[]` | `[]` |

The builds print only the known repo-wide "Known issues" warning (37 lines dropped).

Rendered `<main>` text of all three, checked by script:
- 0 em or en dashes.
- None of live, now, real-time, yet, soon, pending, planned, shipped, coming, locally, ruling, ledger, TODO, held, TRD,
  COST-DIMENSION or LEGACY-BS-CLOCK.
- The viewport meta and `<main>` are present.
- There is one "Rows not shown" block per page, listing each table with its reason.
- No capture date, byte size or row count appears.

NESO's own text says "Live data file is refreshed ..."; the page words it as "current file" to keep "live" off the page.

**Screenshots:** light mode at 1440, 1024 and 768, and 390 through a 390 px iframe (whole page plus three full-scale
bands each). They are in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\held-trd1-writer\shots\`.
- Nothing is clipped or overlapping.
- The ZIP download URLs, member keys and the ODFM related slug wrap at 390 and 768.

**Server:** started from Bash on 9862 (PID 11213) and stopped by that PID; 9670 was not touched. Dark mode was not
checked, because headless flags do not switch the palette.

## Shared evidence

| Claim | Evidence |
|---|---|
| Held lines | registry `eligibility.question` on each record (`registry/<package>.json`); ledger rows 73, 75, 77 |
| `Cost` labelled £/h, comment "Cost = Volume * Price * Duration", described as total cost | saved field info `field-info/20261008T114228Z/{bs_contract_enactment_balancing,index_linked_contract_volume,ssel_contract_enactment}.json`; identical in all three |
| Datastore dump downloaded each run and kept only if its body is byte-identical to the newest capture | gridflow `connectors/neso_data_portal/client.py` `iter_members` (1658-1780), `_dump_member` (1874-1950) |
| Frozen-class dump re-checked at most weekly (index-linked, refresh `frozen`) | `client.py:105-107` `_FROZEN_CADENCE = 7 days`, `_frozen_not_due` (2409-2440); registry `refresh: frozen` |
| ZIP upload skipped when its newest capture carries the live `last_modified` | `client.py` 1752-1766 |
| Request lines | sidecar `request_url` of each 2026-10-08 capture, copied exactly; `package_show` form as on approved pages |
| Commands | family keys from the registry; `--last 24h` form as on approved held pages; `_files` families are `kind: files`, no transformer |
| Vendor text (notes, resource names and descriptions, extras) | catalogue snapshot `.planning/research/neso-catalog-20261006T195819Z/catalog-snapshot.json` (gridflow repo) |
| Related targets exist | every slug is in `site/hifi/data/neso_data_portal.json` (checked by script); the build resolved all |
| Captures | bronze holds only the 2026-10-08 captures for all six families; there is no later recapture |

## 1. Balancing services contract enactment (`bs_contract_enactment_balancing` lead, `bs_contract_enactment_balancing_service`)

**Reasons:**
- **Yearly tables (13 words):** "NESO labels `Cost` £/h but defines it as volume times price times duration."
- **Older table (16 words):** "Start times are dates only, and NESO gives no clock for the end and update times."

| Claim | Evidence |
|---|---|
| Trading team weighs trades and balancing services, days to hours ahead, and enacts the most cost-effective; e.g. constraint management in Scotland, reactive power; usually no physical exchange of power or energy; only enactments by the trading team | package notes |
| "current file refreshes every ten minutes" | package notes ("Live data file is refreshed every ten minutes") |
| Six datastore tables and one ZIP; yearly tables FY 21-22, 22-23, 23-24, 25-26, 26-27, none for 24-25 | snapshot resources; registry |
| Modern columns: `Cost`, `SO_Flag` (system security or balancing), `Reason`; times "in UTC format" | field info; bronze headers (13 columns in all five yearly bodies) |
| Older table: every `Start Time` is date only | bronze: 79 of 79 cells match `YYYY-MM-DD`; vendor datastore type `date` |
| No clock for end and update times | field info: unit "N/A" for `End Time` and `Last Updated`; bronze: all 79 carry a time of day, no zone suffix |
| The ZIP's two files share the older table's columns | bronze ZIP: 2 members, both headed `Record,Counterparty,Unit,Start Time,End Time,Volume,Price,Notes,Last Updated` |
| Requests | sidecars: dumps `84837a48...` (FY 21-22, first) and `183ecdfb...` (FY 26-27, newest); legacy dump `f75a1dcb...`; ZIP download URL |

**Layout choices:**
- The family template shows only each member's own requests. The archive ZIP (gridflow family
  `bs_contract_enactment_files`, not a page member) is therefore listed under the older table, whose layout its files
  share; the member's `differs` says so.
- The third command ingests it, with the comment "the archive ZIP, bronze only".
- The modern member shows the first and newest of five dumps, and its `differs` says "first and newest shown".

**Body corrections:** none needed. The note's counts, clocks and holds still match bronze and the registry, and there
has been no capture since 2026-10-08.

## 2. Index-linked contract enactments (`index_linked_contract_volume`)

**Reason (13 words):** "NESO labels `Cost` £/h but defines it as volume times price times duration."

| Claim | Evidence |
|---|---|
| Can be used to meet the voltage requirement; normally enacted in the morning ahead of the power exchange auction; paid the agreed strike price, compensated if the spread is negative, positive spread deducted; spread from outturn market indices | package notes |
| No update frequency | snapshot extras carry only `Status` |
| gridflow re-checks each table at most weekly | registry `refresh: frozen`; `client.py` frozen rule |
| Four yearly tables FY 21-22 to FY 24-25, and one ZIP | snapshot resources |
| ZIP holds older files of volumes by date and settlement period | bronze ZIP: 134 members; 132 CSVs headed `Date,SP,...` (five header variants), and 2 workbooks named `.csv` |
| Requests | sidecars: `package_show`; dumps `8f694d01...` (FY 21-22) and `9b72a2f5...` (FY 24-25); ZIP URL |

**Body corrections:** none needed.

## 3. Super SEL contract enactments (`ssel_contract_enactment`)

**Reason (15 words):** "From 2021-22, NESO labels `Cost` £/h but defines it as volume times price times duration."

| Claim | Evidence |
|---|---|
| Lowers the minimum generating level (SEL) of a synchronised generator, decreasing the sum of minimum levels; need not change energy output; enacted by a trading instruction; BM dispatch to the new level if required; refreshed every 10 minutes when data changes | package notes |
| "From July 2020, NESO says" | 20-21 resource description "Data from July 2020" |
| Yearly tables 2020-21 to 2025-26, six datastore tables | snapshot resources |
| The 2020-21 table gives `Reduction (MW)` and `Price (£/MW/hr)`; later tables use the 13 enactment columns | bronze headers of all six bodies |
| "From 2021-22" in the reason | bronze: the FY 21-22 body is the first with the `Cost` header |
| Start and end in UTC | modern field info ("UTC format"); the legacy dictionary as quoted in the note (that dictionary is not in the saved field info) |
| Requests | sidecars: `package_show`; dumps `835d50b9...` (2020-21), `bf9ca254...` (2021-22), `8e7168fa...` (2025-26, newest) |

**Body correction:**
- The note read `dataset_version` `1+e1` as "record version 1, epoch 1" and carried a `TODO: verify` on whether
  epoch-2 rows should read `1+e2`.
- The code settles it. gridflow `silver/neso_data_portal/generic.py:501` composes
  `f"{record.version}+e{ENGINE_VERSION}"`, with `ENGINE_VERSION = "1"` at line 107. The suffix is therefore the generic
  engine version, not the header epoch, and `1+e1` is right for both layouts.
- I rewrote that span and removed the TODO.

## Unverified

- **SSEL:** the 2020-21 table's UTC clock rests on the note's quotation of the legacy dictionary. The saved field info
  covers only the newest resource.
- **All three:** whether NESO has added resources since the 6 October 2026 catalogue snapshot (for example an SSEL
  2026-27 or index-linked 2025-26 table). I made no live call. The facts name tables "as NESO names them" and give no
  "latest" claim.
- **Index-linked:** whether the power exchange auction NESO means is the day-ahead auction the related Nord Pool page
  covers. The related note says only that NESO enacts these contracts before "the auction".

## Open questions for the seat

1. **Where the ZIP goes on the family page.** The ZIP request sits under the older-table member, because the template
   prints only member requests on a family page. If the seat prefers it under the yearly member, there is room for
   it, at four requests.
2. **SSEL 2020-21 rows.** The whole record is held on the `Cost` question, although the 2020-21 rows have no `Cost`
   column. The reason says "From 2021-22", so a reader can see that the hold comes from the later layout. Releasing
   the 2020-21 rows separately would need a registry change and is not a page decision.
3. **ODFM related link.** It rests on NESO tagging Super SEL "Downward Regulation". If the seat finds that too loose,
   drop it: the page keeps two related links.

## Template problems

None new. The template drops the per-variant "Rows not shown:" line on held family pages, so the reasons print once,
in the silver block. That matches the approved Stability Pathfinder page.

## Defects

- **NESO, Balancing Services Contract Enactment:** the legacy resource "Balancing Service Contract Enactment 21-22 (Pre
  June 2021)" has start dates from 2021-04-01 to 2023-03-25, well after its label. Its `Start Time` column has
  datastore type `date`, so every start (79 of 79) has lost its time of day, while the dictionary calls it a "Start
  date time". Already in the note.
- **NESO, Balancing Services Contract Enactment:** the portal lists no FY 24-25 resource (snapshot 2026-10-06). The
  years run 21-22, 22-23, 23-24, 25-26 and 26-27. Already in the note as a TODO.
- **NESO, three enactment packages (and GTMA FY):** the data dictionary labels `Cost` £/h while describing it as total
  cost, "Cost = Volume * Price * Duration". The same text is in all three saved dictionaries. This is the hold
  question, and it is unchanged.
- **NESO, Index Linked Contracted Energy Volume archive ZIP:** 2 of 134 members are Excel workbooks named `.csv`
  (`Contract Volume 2021-05-16.csv` and `2021-05-20.csv`). The file names misspell "Historic" as "Histroic". Already in
  the note.
- **gridflow, documentation only (fixed here):** the SSEL vault note misread `dataset_version` `1+e1` as an epoch
  number and carried a stale TODO. The code (`generic.py:501`) makes it the engine version. No code defect.
- **gridflow:** none otherwise. The registry, sidecars, bronze and connector agree.
- **Manifest:** the leads and members are right: `bs_contract_enactment_balancing` then
  `bs_contract_enactment_balancing_service`; `index_linked_contract_volume`; `ssel_contract_enactment`. The ZIP
  families `bs_contract_enactment_files` and `index_linked_contract_volume_files` are not in `package_tables`. That is
  correct for catalogue-only file families, and their ZIPs appear in the raw feed with their own ingest commands.
