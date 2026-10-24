# Held Interconnector pages, part 1: writer report (2026-10-24)

Packages: `brit-ned` (`brit_ned`), `eleclink` (`eleclink`), `ifa` (`ifa_itl` lead, `ifa_da_id_weekly_itls`),
`ifa2` (`ifa2_ifa_itl` lead, `ifa2_ifa_da_id_weekly_itls`). Every table held. Vault worktree
`C:\gridflow-wt\vault-neso-ic`, front-end worktree `C:\gridflow-wt\fe-neso-ic`. Nothing staged or committed.

## Gates

| Gate | Result |
|---|---|
| `cmp` canonical note against mirror | clean on all four |
| CRLF kept | 0 bare LF in all four notes |
| `gridflow-build --only neso_data_portal/<lead>` (`ifa_itl`, `ifa2_ifa_itl`, `eleclink`, `brit_ned`) | each wrote its page (dataset template), no errors; only the repo-wide "Known issues" warning |
| Detector `detect.mjs --json` | `[]` on `ifa.html`, `ifa2.html`, `eleclink.html`, `brit-ned.html` |
| Artefacts | none written (held); no staged spec or authored override existed for any key |
| Rendered `<main>` text | no em or en dashes, arrows or middle dots; none of live, real-time, soon, pending, planned, shipped, locally, ruling, ledger, TODO, held, yet, E-SEM, "since 20"; every internal link resolves to a built file; viewport meta present |
| Hold lines | 15, 16 (IFA), 15, 16 (IFA2), 15 (ElecLink), 16 (BritNed) words; budget 16 |
| Screenshots | 1440, 1024, 768 and 390 (390 px iframe) for all four pages on port 9821, in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\ic-h1-writer\shots\`. I looked at IFA 1440, BritNed 390 (top and middle) and ElecLink 768: nothing clipped or overlapping; long dataset URLs and the BritNed related slugs wrap. Light mode only; dark not checked. Server started in Bash with its PID recorded (40964), stopped by that PID; 9670 untouched. |

## Shared wording (reusable for NemoLink, NSL, Viking)

- Title: "<Link> transfer limits".
- Summary: "NESO's limits on flow each way over <Link>, an interconnector between GB and <country>, in MW for each hour it restricts."
- `what_it_is` opener (NESO package notes, identical in all four packages): "NESO says it submits these values to interconnector capacity calculations: the most power that may flow into GB (import) and out of GB (export), in MW per hour. Final capacity, on the trading facilitator's website, can be lower. No row means no restriction." Then one sentence spelling out the term the package uses, as NESO's own text does (see below).
- `how_used`: "Hours when NESO restricted the link, by direction, with its stated reason"; "A feature for flow and price models: the hours NESO capped the link"; "Set beside the final capacity the link's trading facilitator publishes".
- Current datastore table (dump) hold: "Nearly every hour is already past, and NESO does not say rows are unchanged since upload."
- Archive or label-only table hold: "Hour labels have no defined day or clock, and no row says when NESO issued it."
- Raw feed note for dump plus archive: "From NESO's CKAN portal: `package_show`, the current table's dump, kept if changed, and the archive CSV if `last_modified` moved. The 16 October 2026 table keeps every 8 October row unchanged."
- Commands: `pipeline` per member on a two-table family (as the approved 14-day wind page); `ingest` then `transform` on a one-table page.

**ITL and NTC, as NESO writes them.** The launch prompt glosses ITL as "interconnector transfer limit"; NESO never uses that phrase. Its text (catalogue snapshot `20261006T195819Z`) says: IFA and IFA2 package titles "NESO's Intraday Transfer Limit", current resource descriptions "Intraday Transfer Limit restrictions", archive descriptions "Network Transfer Capacity restrictions"; ElecLink package title "NESO's Net Transfer Capacity" and both resource descriptions "Net Transfer Capacity restrictions"; BritNed package title "NESO's Intraday Trading Limit", every resource description "Intraday Transfer Limit restrictions". So the pages say "Intraday Transfer Limit (ITL)" (IFA, IFA2, BritNed), "Network Transfer Capacity (NTC)" for the IFA and IFA2 archives, and "Net Transfer Capacity (NTC)" for ElecLink. NESO expands NTC two ways across packages; the pages follow each package. The BritNed "Trading" title variant is left off the page (budget); it is in the note.

## Evidence (all packages)

| Claim | Evidence |
|---|---|
| NESO notes: values submitted to capacity calculations, restrict max GB import and export, MW per hourly period; final capacity may be lower, on the trading facilitator's website; no values means no restriction | catalogue snapshot `notes` for all four packages (identical text) |
| Cadence: "Ad hoc" (IFA, IFA2, BritNed), "Daily" (ElecLink) | snapshot `extras` |
| Dump keeps body only if changed; upload skipped when newest capture carries the live `last_modified` | gridflow `connectors/neso_data_portal/client.py` `iter_members` docstring (lines 1661-1672), `_dump_member` |
| Request URLs | equal to the sidecar `request_url` of each capture; `package_show` is the connector form (approved pages) |
| Keys exist | `config/sources.yaml` lines 795 (`brit_ned`), 915 (`eleclink`), 978-981 (IFA2, IFA) |
| `pipeline`, `ingest`, `transform` take `--last` | `cli.py` `pipeline` options (line 485 on) |
| Second dump captures 2026-10-16: IFA 11,782 rows, IFA2 7,920, ElecLink dump 24,599; same header, CKAN `last_modified` unchanged (2026-09-17); every 8 October row present unchanged (full-row anti-join 0; 0 same-key rows with changed values); 216, 168, 240 rows added, all uploaded after the first capture | Polars on the bronze bodies (script `ic-h1-writer\dumps.py`) |
| "Nearly every hour is already past": IFA 11,556 of 11,566 (8 Oct) and 11,781 of 11,782 (16 Oct) targets before capture; IFA2 7,742 of 7,752 and 7,919 of 7,920; ElecLink 24,337 of 24,359 and 24,574 of 24,599 | same script |
| Rows with target before own upload: IFA 818 then 824; IFA2 676 both; ElecLink 1,292 both | same script |
| Archive labels: IFA 20221014 to 20241219, IFA2 20221013 to 20241219, ElecLink 20221107 to 20240924; every labelled day opens at 23:00 in file order (IFA 475 of 475 days, IFA2 320 of 320); ElecLink archive days open at `22:00 to 23:00` (203) or `23:00 to 00:00` (94); ElecLink versions `001` to `004`; no upload or issue column in any archive | `ic-h1-writer\arch.py` on the bronze bodies |
| Current tables start 2024-12-19 23:00 UTC (IFA, IFA2), 2024-09-25 22:00 UTC (ElecLink) | dumps script |
| Silver: second Parquet file per dump (11,782; 7,920; 24,599 rows), archives one file each | `ic-h1-writer\silver.py` (read only) |
| Related pages exist and say what the notes say: `entsoe/net_transfer_capacity` (forecast capacity across a border), `entsoe/dc_link_intraday_transfer_limits` ("The GB and NL pair is BritNed"), `historic-demand-data` (columns `IFA_FLOW`, `IFA2_FLOW`, `BRITNED_FLOW`, `ELECLINK_FLOW` in the 2026 header), `system-operating-plan-sop` (`britned_temx/teol/temi`, "expected reference-program flows") | built pages and notes in the front-end worktree; bronze header |

## `ifa` (lead `ifa_itl`)

Page: family, `held: true`; members `ifa_itl` (current table) and `ifa_da_id_weekly_itls` (archive), each with its hold line above. History fact: "NESO's files label hours from 14 October 2022: archive, then the current table".

Body corrections (vault note `ifa.md`):
- Coverage paragraph: current target range dated to the 8 October capture, plus "to `2026-10-16 21:00`" in the 16 October capture.
- Hold question: counts dated to the 8 October capture, with the 16 October counts added.
- Activation: "one capture per family" now "at the time".
- New paragraph "Second capture of `ifa_itl`": file, bytes, rows, header, unchanged `last_modified`, append-only result, 216 new rows and their upload and target ranges, 491 upload instants, auctions still Intraday 1 to 4 only, second silver file; archive has no second capture.

## `ifa2` (lead `ifa2_ifa_itl`)

Same shape as IFA; history from 13 October 2022. Related: IFA described as "the older GB and France link" (IFA dates from 1986, IFA2 from 2021; general fact, not NESO text).

Body corrections (`ifa2.md`): event-time paragraph target range extended to the 16 October capture; hold question counts dated with 16 October values; new "Second capture" paragraph (733,375 bytes, 7,920 rows, 168 new, 330 upload instants); cadence "323 distinct upload timestamps (330 on 2026-10-16)".

## `eleclink` (one table, two resources)

Page: one-table held page; `held` covers both resources ("NESO does not say current rows are unchanged since upload, or define archive days and versions."). `what_it_is` names the archive's operational date and version so the hold reads. Three requests (`package_show`, dump, archive).

Body corrections (`eleclink.md`): hold question counts dated with 16 October values; coverage table extended to `2026-10-17T21:00Z`; new "Second capture of the dump" paragraph (2,239,019 bytes, 24,599 rows, 240 new, 1,025 upload instants, auctions unchanged; the 16 October run fetched no archive body, so its stamp had not moved; `_latest` per resource now 24,599 + 8,472).

## `brit-ned` (one table, 187 weekly files)

Page: one-table held page. Raw feed shows `package_show`, the first file (20221012), 20241016 and the newest (20260923); the note says the first repeats an hour with two values and 20241016 is not UTF-8, so neither loads (both adjudicated in gridflow). Cadence "Ad hoc, NESO says; files usually appear seven days after their named date": CKAN `created` is seven days after the name date for 175 of 187 resources (range 2 to 14). History dated to NESO's 6 October 2026 list. Every labelled day in every body opens at 23:00 in file order (797 of 797 day blocks, malformed labels excluded); not on the page.

Coverage, as the batch asked: 187 resources, 185 load; both failures are now **adjudicated**, not one. IC-2H (merged 2026-10-10, master `6085571`, RULINGS 584, 585) added `UnicodeDecodeError` to the ADR-040 allowlist and a `failed` ledger entry for 20241016; reconcile then exited 0, 0 open, 10 adjudicated (`v0.22-RESULTS.md` §IC-2H). No BritNed body was captured on 16 October.

Body corrections (`brit-ned.md`), all stale since IC-2H:
- Intro: "(still an open reconcile gap)" now "an open reconcile gap at activation, adjudicated since IC-2H on 2026-10-10".
- Resource table row 20241016: "failed, open gap (`ComputeError`; IC-2H)" now "failed, adjudicated (`UnicodeDecodeError` since IC-2H)".
- 20241016 bullet: rewritten in the past tense for activation, then what IC-2H did, the ledger question, reconcile result; the cited test is renamed in gridflow to `test_the_0xa0_capture_is_adjudicated` (`tests/unit/test_neso_ic2_records.py:963`).
- Activation paragraph: one sentence added with the post-IC-2H reconcile result.
- Holds: "stays out until IC-2H" now "until NESO answers its encoding question (adjudicated by IC-2H)".

## Not verified

- Whether the 16 October run attempted the IFA and IFA2 archive keys at all (no bronze, no run log read). For ElecLink the archive skip is inferred from the client rule because the same family run captured the dump.
- That the 2026-10-06 catalogue still lists 187 BritNed files today (no live call); the page dates the count.
- Dark mode at any width.

## Open questions and template notes

- The batch file says "one failed capture was adjudicated" for BritNed; both are adjudicated now (seat item for the batch file and the front-end ledger row, which still says "B-ENC open").
- The launch prompt's "interconnector transfer limit" gloss does not match NESO's wording; the pages use NESO's (above). The next batch should check NemoLink, NSL and Viking resource text the same way: NESO may write NTC either way.
- No template problem found. The manifest leads and members are right.

## Defects

- NESO, all four packages: NESO expands NTC as "Network Transfer Capacity" (IFA and IFA2 archive descriptions) and "Net Transfer Capacity" (ElecLink title and resources); BritNed's title says "Intraday Trading Limit" while its resources say "Intraday Transfer Limit".
- NESO, IFA, IFA2, ElecLink current tables: between the 8 and 16 October 2026 dumps NESO only appended (216, 168, 240 rows); no row changed. Not proof of immutability; the hold stands. Rows whose target hour precedes their own upload time persist (IFA 824, IFA2 676, ElecLink 1,292 on 16 October).
- NESO, IFA and IFA2 current tables: only `Intraday 1` to `Intraday 4` appear in both captures, though NESO describes day-ahead and intraday auctions.
- NESO, BritNed: the 20221012 file gives `20221012 04:00 - 05:00` twice with different values; the 20241016 file carries two `0xA0` bytes (not UTF-8); the 20230118 file's download name is `ifa2-da-id-weekly-itls-20230118.csv`. Already in the note and the ledger; carried.
- Vault (fixed here): `brit-ned.md` described the 20241016 failure as an open reconcile gap after IC-2H closed it.
- gridflow / planning (not fixed, seat item): `v0.22-FE-LEDGER.md` row `brit-ned` still says "B-ENC open → IC-2H"; the batch file says one failure adjudicated. No gridflow code defect found.

## Round 2 (2026-10-24): fixes for `held-1-review.md` and the seat's country ruling

Gates after the changes: `cmp` of each note against its mirror is clean on all four; 0 bare LF in all four notes; `gridflow-build --only neso_data_portal/<lead>` (`ifa_itl`, `ifa2_ifa_itl`, `eleclink`, `brit_ned`) writes each page with no errors; detector `[]` on all four. The rendered `<main>` text has no em or en dashes, arrows or middle dots. It has none of live, real-time, soon, pending, planned, shipped, locally, ruling, ledger, TODO, held, E-SEM, France, Netherlands, "No row" or "capped". Every internal link resolves. I took no new screenshots: the text only got shorter, and the layout is the same as round 1.

**Finding 1 (major, all four pages): rows marked as restricted hours.** I reproduced the checker's counts from bronze (`ic-h1-writer\reasons.py`, `hours.py`). On the 16 October tables, `No Restriction` is the reason for flow to GB on 10,741 of 11,782 IFA rows, 7,477 of 7,920 IFA2 rows and 23,354 of 24,599 ElecLink rows. The ElecLink archive gives `No Restriction` on 3,120 of 8,472 rows. The IFA and IFA2 archives leave the reason blank on 3,922 and 2,822 rows. BritNed leaves it blank on 8,466 of 19,129 rows. The archives give 24 rows for every labelled day (IFA 474 days plus one of 25; IFA2 320; ElecLink 353 date, auction and version groups). BritNed gives 24 rows on 792 of 797 file-days.
- `summary` (and so the meta description): "NESO's hourly limits on flow each way over the <Link> interconnector, in MW, with reasons."
- `how_used[0]`: "Which hours NESO restricted the link, by direction, from the stated reason". `how_used[1]`: "A feature for flow and price models: when NESO restricted the link".
- `what_it_is`: "No row means no restriction" is gone. NESO's rule is now attributed and the dated fact follows. IFA and IFA2 say "It says it publishes only restrictions, yet its October 2026 files list every archive hour and many No Restriction rows." ElecLink says "...hold many No Restriction rows." BritNed says "...yet many rows in its files give no reason." The page carries no local counts. The shared opener is now "NESO says it submits these to interconnector capacity calculations, capping GB imports and exports, in hourly MW; final capacity can be lower." I dropped the import and export glosses to fit the 60-word budget.

**Finding 2 (major, note bodies).** `ifa.md`, `ifa2.md`, `eleclink.md` and `brit-ned.md` now attribute "published only where a restriction applied" to the package notes. Each adds the measured, dated fact with counts (bronze read 2026-10-24) as listed above. `ifa2.md`: "Each row is a NESO restriction" now reads "Each row is a NESO limit".

**Nits.**
- ElecLink `held`: now "NESO does not say rows are unchanged since upload, and archive days and versions are undefined." (15 words; the checker's wording). It covers both files. It still leaves out "past", which no longer fits the budget alongside the archive half. That is a seat call.
- Raw-feed note (IFA, IFA2, ElecLink): "From NESO's CKAN portal: `package_show`, the current table's dump and the archive CSV. Fetched 16 October 2026, the table kept every row fetched 8 October unchanged, plus new ones." I dropped the "kept if changed" and `last_modified` detail to fit the budget. I used "kept", not "held", so the checker's banned-word grep stays clean.
- BritNed raw-feed note: "Shown: 20221012 (first), 20241016, 20260923 (newest). 20221012 gives one hour two values; 20241016 is not UTF-8; gridflow loads neither."
- BritNed related IFA line: "NESO's IFA limits; its current table has an upload time per row".
- BritNed `facts.vendor` is dated "(6 October 2026)"; `history` now reads "Files named 12 October 2022 to 23 September 2026, NESO lists".
- `ifa2.md`: both Activation paragraphs now say "one capture at activation".
- "Newer" and "older" link wording: replaced (see the country ruling below).
- `ifa_itl` and `ifa2_ifa_itl` hold lines ("already past"): left unchanged, as the checker suggested, for the seat to decide.

**Seat ruling (country names).** Neither NESO's package text (titles, notes, resource descriptions) nor NESO's interconnector register (16 October 2026 capture: link, customer, landing substation, MW) names a far-end country. K-IC-1-FACTS and K-IC-2-FACTS take the countries as given and cite no source. So all four page blocks drop France and the Netherlands:
- The summaries name only the link ("the IFA interconnector").
- The sibling related lines say "another GB interconnector".
- The ENTSO-E NTC line now reads "ENTSO-E's forecast capacity across each GB border, all links together".
- The BritNed ENTSO-E line now reads "ENTSO-E's intraday limits on GB's DC links, one direction per series". The ENTSO-E page states "The GB and NL pair is BritNed", but that is gridflow's own page, not NESO's text.

The note bodies still say "GB–France" and "GB–Netherlands" in their opening paragraphs. Those lines are not on the pages. Rewording them is a seat call for the vault.

**Defects added this round:**
- NESO, all four packages: NESO's notes say values are published only where a restriction was applied. Its files list unrestricted hours instead: reason `No Restriction` on most current-table rows (flow to GB) and on 3,120 ElecLink archive rows, blank reasons in the IFA and IFA2 archives and BritNed, and 24 rows a day in every archive. Confirmed (the checker's finding).
- NESO, all four packages: no NESO text states the far-end country of these links. The vault notes and FACTS files assume it without a source.
