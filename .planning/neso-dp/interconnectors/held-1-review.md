# Held Interconnector pages, part 1: checker review (2026-10-24)

Checked against the batch file, standing instructions, the writer's report, the four canonical note diffs against `origin/master` (vault worktree `C:\gridflow-wt\vault-neso-ic`), the mirrors, the built pages, the ledger rows (`eleclink`, `ifa`, `ifa2`, `brit-ned`) and `eligibility.md`, the catalogue snapshot `20261006T195819Z` (package titles, notes, extras, resource descriptions), gridflow `client.py` (`iter_members`), `config/sources.yaml`, the IC-2H records in `v0.22-RESULTS.md` and the renamed BritNed test, and every bronze sidecar and body for the six keys plus all 187 BritNed bodies (read only, Polars, gridflow venv, scratch in `ic-h1-checker`).

Gates I reran: `cmp` of each canonical note against its mirror is clean on all four; `gridflow-build --only neso_data_portal/<lead>` for `ifa_itl`, `ifa2_ifa_itl`, `eleclink` and `brit_ned` wrote each page with no errors; detector `[]` on all four built pages; no series, sample or notebook artefact exists for any of the six keys (all held); rendered `<main>` has no em or en dashes, arrows or middle dots, and none of live, real-time, soon, pending, planned, shipped, locally, ruling, ledger, TODO, held, yet, E-SEM (the only "capture" hits are the approved command comment "the capture's date to silver"); viewport meta present; every internal link in the four `<main>` blocks resolves to a built file; titles and meta descriptions carry no local counts or planning words. `eleclink.html` is the only ElecLink page (no pointer file beside it) and renders as a one-table page with its three requests and one hold line; `brit_ned.html` is the usual pointer to `brit-ned.html#brit_ned`. Screenshots (port 9831): 1440 for IFA and ElecLink, 390 through a 390 px iframe for BritNed and IFA2. I read ElecLink 1440 and BritNed 390: nothing clipped or overlapping, long URLs wrap, hold lines sit under their tables. I did not look at 1024, 768 or dark mode myself. Server stopped by its own process id (32100, command line matched on port 9831); 9670 untouched.

## Verdicts

| Page | Verdict | blocker | major | nit |
|---|---|---|---|---|
| `ifa` | REVISE | 0 | 1 | 3 (4, 5, 6) |
| `ifa2` | REVISE | 0 | 1 | 4 (4, 5, 7, 8) |
| `eleclink` | REVISE | 0 | 1 | 3 (4, 9, 10) |
| `brit-ned` | REVISE | 0 | 1 | 3 (11, 12, 13) |

One shared major (finding 1) and one note-body correction (finding 2) cause all four verdicts; each is a short wording fix. Everything else is nit. Numbers in the verdict table list the finding numbers that apply to each page.

## Reproduced from bronze (read only)

| Claim | Result |
|---|---|
| Current tables: 11,566 to 11,782 (IFA), 7,752 to 7,920 (IFA2), 24,359 to 24,599 (ElecLink) rows between the 8 and 16 October 2026 captures; same header; every 8 October row present unchanged in the 16 October table (full-row anti-join 0); 0 same-key rows with changed values; 216, 168 and 240 new rows, all with upload time after the first capture (IFA `2026-10-08T17:30:05` to `2026-10-15T17:30:05`, IFA2 `17:45:08` to `17:45:05`, ElecLink `2026-10-08T14:30:05` to `2026-10-16T14:30:05`); target range to `2026-10-16 21:00` (IFA, IFA2) and `2026-10-17 21:00` (ElecLink) | Reproduced. |
| IFA and IFA2 current tables hold only `Intraday 1` to `Intraday 4` in both captures (no Day Ahead); ElecLink holds `Day Ahead` and `Intraday 1` to `Intraday 3` | Reproduced. |
| "Nearly every hour is already past": targets before the capture 11,556 of 11,566 then 11,781 of 11,782 (IFA); 7,742 of 7,752 then 7,919 of 7,920 (IFA2); 24,337 of 24,359 then 24,574 of 24,599 (ElecLink); rows with target before their own upload 818 then 824, 676 both, 1,292 both | Reproduced. |
| 491, 330 and 1,025 distinct upload instants in the 16 October tables | Reproduced. |
| Archives: IFA 11,401 rows, 475 operational days `20221014` to `20241219`, every day opens `23:00` in file order, 2 labels carry `(a)`/`(b)`; IFA2 7,680 rows, 320 days `20221013` to `20241219`, every day opens `23:00`; ElecLink archive 8,472 rows, 297 operational dates `20221107` to `20240924`, days open `22:00 to 23:00` (203) or `23:00 to 00:00` (94), versions `001` to `004`; no upload or issue column in any archive. Headers are `Operational Date (YYYY-MM-DD) & Time GMT/BST (HH:MM - HH:MM)` (IFA, IFA2) and `Operational Date`, `Version`, `Hourly Time Period (GMT)` (ElecLink) | Reproduced. |
| No archive body was captured on 16 October (one sidecar per archive key, all dated 8 October); client skips an upload whose newest capture carries the live `last_modified`; dump kept only if its body differs | Reproduced (`iter_members` docstring, `client.py` lines 1661 to 1672 and 1752 to 1760). |
| BritNed: 187 bodies in bronze, header epochs 1 (first file, columns in the other order, "Restiction" typo), 3, 1, 180, 2; 19,153 rows in total; `20221012 04:00 - 05:00` appears twice with `1050` and `1,007`; the `20241016` body fails strict UTF-8 at byte `0xa0` (position 2826); snapshot lists 187 files `20221012` to `20260923`; CKAN `created` is seven days after the file's name date for 175 of 187 (range 2 to 14) | Reproduced. |
| BritNed IC-2H: master `6085571`, `UnicodeDecodeError` re-record, reconcile exit 0 with 10 adjudicated; test `test_the_0xa0_capture_is_adjudicated` exists (`tests/unit/test_neso_ic2_records.py:963`) | Reproduced; both failed captures are settled in gridflow, so the note corrections are right. |
| NESO text: package titles "IFA/IFA2 - NESO's Intraday Transfer Limit", "ElecLink - NESO's Net Transfer Capacity", "BritNed - NESO's Intraday Trading Limit"; IFA and IFA2 current resources "Intraday Transfer Limit restrictions", archives "Network Transfer Capacity restrictions"; ElecLink both resources "Net Transfer Capacity restrictions"; BritNed every resource "Intraday Transfer Limit restrictions"; extras "Ad hoc" (IFA, IFA2, BritNed) and "Daily" (ElecLink); identical notes text in all four | Reproduced. |
| Commands: all six keys exist in `config/sources.yaml` (lines 795, 915, 978 to 981); `--last` is accepted | Reproduced. |
| Requests: dump and archive URLs equal the sidecar `request_url` for each key; `package_show` is the connector form | Reproduced. |
| Related pages exist and say what the notes say: `entsoe/net_transfer_capacity` ("across a border"), `entsoe/dc_link_intraday_transfer_limits` ("The GB and NL pair is BritNed"), `historic-demand-data` (2026 header has `IFA_FLOW`, `IFA2_FLOW`, `BRITNED_FLOW`, `ELECLINK_FLOW`), `system-operating-plan-sop` ("expected availability and output by technology and interconnector") | Reproduced. |

## Focus 1: the "Rows not shown" lines

- **Dump line** (IFA, IFA2: "Nearly every hour is already past, and NESO does not say rows are unchanged since upload."): accurate (counts above), covers the whole current table, equal to the ledger and eligibility question (past targets; no statement that a row is unchanged since its upload time), plain, no codes, no local-data reference. It is 16 words (budget 16). "Already past" has no reference point on the page (finding 4).
- **Archive line** (IFA, IFA2) and **BritNed line** ("Hour labels have no defined day or clock, and no row says when NESO issued it."): accurate for every archive row and every BritNed row (no body has an issue column; every labelled day opens at 23:00 in file order except a handful of malformed labels the note records), covers the whole table, equal to the ledger (rollover, GMT/BST, `(a)`/`(b)`; no issue time). Plain, no codes, no local-data reference. For BritNed's two newest files the column header does say "GMT"; the ledger's question is the mapping between GMT, BST and the day label, which the line covers, so I leave it.
- **ElecLink line** ("NESO does not say current rows are unchanged since upload, or define archive days and versions."): accurate, covers both files, plain, no codes. It is 16 words, not 15 as the writer's report and the launch prompt say (still inside the budget). It leaves out the dump half the other pages carry (rows are for hours already past) and the archive's rollover, so it does not use the shared wording where the questions agree (finding 3).

## Focus 2: ITL and NTC wording

All four pages follow NESO's own text for their package. IFA and IFA2: "Intraday Transfer Limit (ITL) and, in its archive, Network Transfer Capacity (NTC) restrictions" is exactly NESO's resource wording. ElecLink: "Net Transfer Capacity (NTC)" is NESO's title and both resource descriptions. BritNed: "Intraday Transfer Limit (ITL)" is NESO's resource wording; NESO's package title says "Intraday Trading Limit". The page does not mention the title variant (the note does), which is a fair budget call. The launch prompt's "interconnector transfer limit" gloss appears nowhere on the pages. No finding.

## 1. Shared: the pages say rows exist for hours NESO restricted, but the tables list unrestricted hours too

1. **major** (all four pages) `page.summary` ("in MW for each hour it restricts", also the hero line and meta description), `page.how_used[0]` ("Hours when NESO restricted the link"), `page.how_used[1]` ("the hours NESO capped the link") and `page.what_it_is` ("No row means no restriction"): these tell a reader that a row marks a restricted hour. The files say otherwise. The archives list every hour of every day: IFA 11,401 rows over 475 days (474 days of 24 and one of 25), IFA2 7,680 rows over 320 days (24 each), ElecLink 24 rows for every operational date, auction and version, BritNed 144 to 169 rows per six or seven days. The current tables list most hours as unrestricted: reason `No Restriction` in the "to GB" direction on 10,741 of 11,782 IFA rows, 7,477 of 7,920 IFA2 rows and 23,354 of 24,599 ElecLink rows (the "from GB" direction 5,196, 3,903 and 18,822), and in both directions on 4,866, 3,682 and 18,429 rows. The IFA and IFA2 archives leave the reason blank on 3,922 of 11,401 and 2,822 of 7,680 rows and give "System Security" on the rest; BritNed leaves it blank on 8,436 of 19,009 rows that decode as UTF-8. The current tables do not list every hour either (IFA 10,582 distinct target hours across a 15,983-hour span), so "every hour" is also wrong. NESO's own note ("Values will only be published where a restriction has been applied") is contradicted by its files. "No row means no restriction" reads as NESO's rule on the page; it can stay if attributed, but with the rest it hides that most rows are unrestricted. The ElecLink archive's `No Restriction` label and the vault note (IFA: "Explicit `No Restriction` reasons appear, so a missing row and a 'no restriction' row are different things") show the writer saw this. Fix, for example: summary "NESO's hourly limits on flow each way over IFA, an interconnector between GB and France, in MW, with reasons." (19 words, budget 22); `how_used[0]` "Hours NESO restricted the link, by direction, with its stated reason" stays true only if rows are filtered, so say "Which hours NESO restricted the link, by direction, from the stated reason"; `how_used[1]` "A feature for flow and price models: when NESO restricted the link"; in `what_it_is` replace "No row means no restriction." with a plain statement of what the files hold ("Many rows say No Restriction" for IFA, IFA2 and ElecLink; for BritNed and the IFA archives, "Many rows give no reason"). Check each against its word budget (60 for `what_it_is`).

2. **major** (note bodies) `ifa2.md` lines 68 to 73 ("Each row is a NESO restriction... NESO publishes a value only where it applied a restriction. An hour with no row means NESO applied no restriction"), `eleclink.md` lines 56 to 60 and `brit-ned.md` line 61 state NESO's rule as gridflow fact; the data above contradict it for the files they describe (`ifa.md` has the same opening paragraph, and line 302 already records the `No Restriction` rows). Attribute the sentence to NESO ("the package notes say") and add the measured fact (rows for unrestricted hours; reason `No Restriction` on N of M rows in the 16 October table, blank reason on N rows of the archive) with a date. This is a stale statement the data proves wrong, which the batch file asks the writer to correct.

## 2. `ifa` (lead `ifa_itl`) - REVISE

3. **note** (not a finding) `page.family.members[0].held`: "already past" has no reference point (the hour was past when gridflow fetched the file); it is the shared line, so I leave it to the seat. `[1].held` is fine.
4. **nit** `page.raw_feed.note` (also IFA2, ElecLink): "The 16 October 2026 table keeps every 8 October row unchanged." is accurate (anti-join 0, 0 changed same-key rows) but "table" is the dump as gridflow fetched it on those two days, which the page never says, and it leaves out that 216 (IFA), 168 (IFA2) or 240 (ElecLink) rows were added, so "keeps ... unchanged" could be read as "nothing changed". Plainer: "NESO's table as fetched on 16 October 2026 holds every row fetched on 8 October, unchanged, plus new ones." Check the 30-word note budget (the current note is about 28 words; drop "if `last_modified` moved" detail or the commas if needed).
5. **nit** `page.related[0]` ("a newer GB and France link"; IFA2 page: "the older GB and France link"): true, but it is general knowledge, not NESO or gridflow text, and the report says so. Either attribute nothing ("another GB and France link") or leave as the seat prefers.
6. **nit** note body, Activation paragraph (`ifa.md` line 313): "one capture per family at the time" is now dated; fine. The Coverage and Hold-question edits are right.

Checked and fine: `facts` (current table plus archive CSV; "Ad hoc, NESO says" is NESO's extras; "labels hours from 14 October 2022" is the archive's first label; grain), `differs` lines (current table: upload time, auction, hour start in GMT; archive: operational date plus GMT/BST range, no upload time, matches the headers), the two requests (equal to sidecars), both `pipeline` commands, `what_it_is` terms (NESO's own ITL and NTC wording), related links 2 to 4. Note body corrections: second-capture paragraph (file name, 1,097,358 bytes, 11,782 rows, `last_modified` unchanged, 216 new rows, 491 upload instants, auctions `Intraday 1` to `4`, second silver file) all reproduced.

## 3. `ifa2` (lead `ifa2_ifa_itl`) - REVISE

7. **nit** note body, `ifa2.md` lines 223 and 310: both Activation paragraphs say "one capture" with no "at the time", and the second-capture paragraph follows at 315. Add "at activation".
8. **nit** `page.raw_feed.note` and `page.related[0]`: as findings 4 and 5.

Checked and fine: the facts ("from 13 October 2022" is the archive's first label), both hold lines, requests, commands, ITL and NTC wording, related links; note corrections: target range to 16 October, 7,919 of 7,920 and 676 in both captures, second-capture paragraph (733,375 bytes, 7,920 rows, 168 new, 330 upload instants), "323 distinct upload timestamps (330 on 2026-10-16)": reproduced.

## 4. `eleclink` (one table, two resources) - REVISE

9. **nit** `page.held` (see Focus 1): drops "most hours are already past" and the archive's rollover, so it differs from the IFA and IFA2 wording where the dump question is identical, and it is 16 words not 15. Suggest the shared dump half plus the archive half only if the budget allows; for example "NESO does not say rows are unchanged since upload, and archive days and versions are undefined." (15 words) keeps the whole table but still lacks "past"; the seat can choose.
10. **nit** `page.what_it_is`: "Archive rows add an operational date and version." is true (header and 297 dates, versions `001` to `004`) but reads as extra detail; fine. No change needed beyond finding 1.

Checked and fine: one-table page renders correctly as `eleclink.html` with no separate pointer page; `facts` ("Daily, NESO says" is NESO's extras; "from 7 November 2022" is the archive's first label; grain "for one auction" matches Auction Type), three requests (equal to sidecars), `ingest` then `transform` commands, "NESO calls them Net Transfer Capacity (NTC)", related links. Note body: coverage row to `2026-10-17T21:00Z`, hold counts (24,574 of 24,599 and 1,292), second-capture paragraph (2,239,019 bytes, 24,599 rows, 240 new, 1,025 upload instants, the archive not refetched because its stamp had not moved) reproduced; the archive's `_latest` counts (8,472) match.

## 5. `brit-ned` (one table, 187 weekly files) - REVISE

11. **nit** `page.raw_feed.note` ("Shown: first, 20241016, newest. The first repeats an hour with two values; 20241016 is not UTF-8; neither loads."): "first" and "newest" do not say which file (the first is `20221012`, the newest `20260923`), and "loads" is gridflow jargon the page has not defined. Plainer: "Shown: the first file (20221012), 20241016 and the newest (20260923). The first lists one hour twice with two values; 20241016 is not UTF-8; gridflow loads neither." Check the 30-word budget.
12. **nit** `page.facts.vendor` ("187 weekly CSV files") is undated while `facts.history` carries "NESO's list, 6 October 2026"; the count is NESO's list on that day. Date it or leave it to the history line. The files hold six or seven days each (144 to 169 rows), so "weekly" is NESO's file naming; fine.
13. **nit** `page.related[3]` ("The same NESO limits on IFA, with an upload time per row"): only IFA's current table has an upload time per row; the archive does not. Say "IFA's current table has an upload time per row".

Checked and fine: both failed captures are described correctly (the page says only that neither loads; the note now says both are adjudicated since IC-2H on 10 October 2026); ITL wording follows resource text; cadence "files usually appear seven days after their named date" (175 of 187); history dates; four requests (the three file URLs equal sidecars); commands; related links 1 to 3. Note body corrections (intro, resource-table row, 20241016 bullet, activation paragraph, holds) all reproduced against gridflow code and results; no "open gap" statement left that IC-2H contradicts (lines 496, 711 are dated history with the IC-2H result added).

## Defects to carry (writer's, confirmed, plus mine)

- NESO, all four packages: NESO's note says values are published only where a restriction was applied; its files list hours with reason `No Restriction` (most current-table rows), blank reasons (IFA and IFA2 archives, BritNed) and every hour of every day in the archives. (Mine; extends the writer's list.)
- NESO, IFA, IFA2, ElecLink current tables: only appended between the 8 and 16 October 2026 fetches (216, 168, 240 rows); rows with target before their own upload persist (824, 676, 1,292). Confirmed.
- NESO, IFA and IFA2 current tables: only `Intraday 1` to `4` appear. Confirmed.
- NESO, four packages: NTC expanded two ways; BritNed title "Trading" against "Transfer" in resources. Confirmed.
- NESO, BritNed: `20221012` repeats `04:00 - 05:00` with two values; `20241016` has two `0xA0` bytes; first file's columns are in the other order with a "Restiction" typo in the header. Confirmed (the typo and column order are extra).
- gridflow planning (seat item): `v0.22-FE-LEDGER.md` row `brit-ned` still says "B-ENC open → IC-2H"; the batch file says one failure adjudicated; both are adjudicated. Confirmed. No gridflow code defect found; no template problem found; the manifest leads and members are right.

---

# Round 2 re-check (2026-10-24)

Scope: only what changed in the writer's round-2 section. Reran `cmp` (clean on all four), `gridflow-build --only neso_data_portal/<lead>` (each page written, no errors) and the detector (`[]` on all four). I read the rebuilt `<main>` text and the round-2 note diffs against `origin/master`, and reproduced the new counts from bronze (read only, Polars and the csv module, scratch in `ic-h1-checker`). No new screenshots (the text only got shorter; layout unchanged from round 1). The round-1 server is already stopped.

## Verdicts

| Page | Verdict | blocker | major | nit |
|---|---|---|---|---|
| `ifa` | REVISE | 0 | 1 (R2-1) | 2 (R2-3, R2-4) |
| `ifa2` | REVISE | 0 | 1 (R2-1) | 2 (R2-3, R2-4) |
| `eleclink` | APPROVE | 0 | 0 | 2 (R2-3, R2-5) |
| `brit-ned` | APPROVE | 0 | 0 | 3 (R2-3, R2-6, R2-7) |

## Round-1 findings, status

| Round 1 | Status |
|---|---|
| 1 (summary, how_used, "No row means no restriction") | Fixed on all four pages. Summaries now read "NESO's hourly limits on flow each way over the <Link> interconnector, in MW, with reasons." (meta description follows). `how_used[0..1]` read "Which hours NESO restricted the link, by direction, from the stated reason" and "when NESO restricted the link". NESO's rule is attributed ("It says it publishes only restrictions, yet ..."). IFA and IFA2 still have one wrong clause, R2-1. |
| 2 (note bodies state NESO's rule as fact) | Fixed in `ifa.md`, `ifa2.md`, `eleclink.md` and `brit-ned.md`: each now attributes the rule to the package notes and adds a dated measurement. Counts reproduced below. One wording slip in `brit-ned.md`, R2-6. |
| 3 (ElecLink hold line) | Rewritten; see R2-5. |
| 4 (raw-feed note, IFA, IFA2, ElecLink) | Fixed: "Fetched 16 October 2026, the table kept every row fetched 8 October unchanged, plus new ones." |
| 5 (newer and older GB and France link) | Fixed: "another GB interconnector". |
| 6, 7 (Activation "at activation") | Fixed in `ifa2.md` (both paragraphs); `ifa.md` already said "at the time". |
| 11 to 13 (BritNed raw feed, vendor date, IFA related line) | Fixed: "Shown: 20221012 (first), 20241016, 20260923 (newest). 20221012 gives one hour two values; 20241016 is not UTF-8; gridflow loads neither."; "(6 October 2026)" on the vendor line; "NESO's IFA limits; its current table has an upload time per row". |

## Reproduced counts (round-2 note bodies)

| Claim | Result |
|---|---|
| 16 October current tables, reason `No Restriction`: to GB 10,741 of 11,782 (IFA), 7,477 of 7,920 (IFA2), 23,354 of 24,599 (ElecLink); from GB 5,196, 3,903, 18,822; both directions 4,866, 3,682, 18,429 | Reproduced. |
| IFA archive 11,401 rows over 475 days, reason blank on 3,922 and `System Security` on the other 7,479; IFA2 archive 7,680 rows over 320 days of 24, blank on 2,822 and `System Security` on 4,858 | Reproduced. |
| ElecLink archive: 24 hours for each of 353 operational date, auction and version groups; `No Restriction` on 3,120 of 8,472 rows | Reproduced. |
| BritNed: 19,129 non-empty rows across the 187 bodies (the 144 rows of `20241016` read as Windows-1252); `System Security` on 10,663, blank on 8,466; 24 rows on 792 of 797 labelled days (25 on 3, 23 on 2) | Reproduced. |
| Round-1 dump counts, new-row counts, unchanged rows, upload instants | Unchanged and still reproduced. |

## Country names

No built page (the whole HTML, not only `<main>`) contains France, Netherlands, French or Dutch: 0 hits on all four. The summaries name only the link; sibling related lines say "another GB interconnector"; the ENTSO-E lines read "ENTSO-E's forecast capacity across each GB border, all links together" and "ENTSO-E's intraday limits on GB's DC links, one direction per series" (the second matches the ENTSO-E page's own wording about GB's DC links). Satisfied. The note bodies still open with "a GB-France interconnector" and the like; that is not on any page and is the seat's call for the vault, as the writer says.

## Findings

R2-1. **major** (`ifa`, `ifa2`) `page.what_it_is`: "yet its October 2026 files list every archive hour". The archives list every hour only of the days they label. IFA labels 475 days across a 798-day span (323 days have no rows; longest gap 21 days after 30 April 2024). IFA2 labels 320 days across 799 (479 days with no rows; longest gap 96 days after 20 November 2023). A reader will take "every archive hour" as every hour of the archive's period, which is wrong. It also overstates the contradiction with NESO's rule (a missing day is consistent with "no restriction"). The note body is right ("the archive lists every hour of each labelled day"); the page needs the same limit. Suggest "list 24 hours for every day they cover" in place of "list every archive hour", and check the 60-word budget.

R2-3. **nit** (all four) `page.what_it_is`: "yet" is meant as the conjunction, but it is on the banned-word list for public copy ("not yet") and the checker's grep flags it on all four pages. "but" says the same.

R2-4. **nit** (`ifa`, `ifa2`) `page.what_it_is`: the sentence now does three jobs (NESO's rule, the contradiction, the names ITL and NTC) and "It calls them" has lost its antecedent after the "yet" clause. "NESO calls these limits Intraday Transfer Limit (ITL) and, in the archive, Network Transfer Capacity (NTC) restrictions" would be unambiguous if the budget allows.

R2-5. **nit** (`eleclink`) `page.held`: "NESO does not say rows are unchanged since upload, and archive days and versions are undefined." is 16 words, not 15 (the writer's report and the coordinator's brief say 15). That is inside the budget of 16, so no change is needed. It covers both files and is accurate. It no longer says "current" or "already past"; the ledger's question is covered by "unchanged since upload" plus the archive half, so I accept it (the "past" half is a seat call, as the writer says).

R2-6. **nit** (`brit-ned.md`, Rules paragraph): "the reason is `System Security` on 10,663 of the 19,129 non-blank rows across the 187 bodies and blank on the other 8,466" contradicts itself, because the 19,129 include the 8,466 blank-reason rows. Say "of the 19,129 rows". The counts are right.

R2-7. **nit** (`brit-ned`) `page.what_it_is`: "yet many rows in its files give no reason" assumes a blank reason means unrestricted, which NESO does not say. The files do give 24 rows for 792 of 797 days; "its files list 24 hours for most days and many rows give no reason" states only what they show. Also `facts.history` "Files named 12 October 2022 to 23 September 2026, NESO lists" reads oddly; "..., from NESO's list" is plainer.

Checked and fine in round 2: the three-line `how_used` lists, the shared opener ("capping GB imports and exports, in hourly MW; final capacity can be lower" follows NESO's note), the four raw-feed notes, the related lines, titles and meta descriptions (no local counts, planning words or country names), internal links, the cmp gate, detector `[]`.
