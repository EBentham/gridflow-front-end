# Held Interconnector pages, part 2: checker review (2026-10-24)

Checker for `nemolink`, `nsl`, `viking`. Read only: bronze and silver through Polars (lazy), builds `--only neso_data_portal/{nemolink_ntc,nsl,viking_ntc}` in `C:\gridflow-wt\fe-neso-ic`, detector, screenshots. Server on port 9832 started in Bash (PID 42520 is the MSYS PID; the listener was Windows PID 34444, stopped by that PID; 9670 untouched). Scratch: `scratchpad\ic-h2-checker\`.

## Verdicts

| Page | Verdict |
|---|---|
| `nemolink` | **REVISE** (1 and 2 below must be fixed) |
| `nsl` | **REVISE** (1, 3 must be fixed) |
| `viking` | **REVISE** (1 must be fixed) |

Counts: 0 blocker, 3 major (findings 1 to 3), 6 nit (findings 4 to 9). Everything else the brief asked about holds: second-capture numbers reproduce exactly, the ingest-only command is real and right, mirrors are byte-identical, builds are clean, detector is `[]` on all three, related links resolve, 390 and 1440 renders are clean.

## Findings

### 1. MAJOR (all three pages): "restricts / no row means no restriction" is false against the files

Fields: `page.summary` ("in MW for each hour it restricts"; NemoLink, NSL, Viking), `page.what_it_is` ("No row means no restriction"; all three), `page.how_used[0]` ("Hours when NESO restricted the link, by direction, with its stated reason") and `how_used[1]` ("the hours NESO capped the link"; all three). Note bodies repeat it: `nemolink.md` lines 89-92 ("Absence means no restriction"), `nsl.md` lines 58-62 and 280-282, `viking.md` lines 68-70, 75-77 and 331-333.

NESO's package note does say values are only published where a restriction applied. The files contradict it: unrestricted hours are listed, with the reason text "No Restriction", and some archives list hours with a blank reason. Counts (bronze, read only):

| File | Rows | "No Restriction" reason | Blank reason |
|---|---:|---|---:|
| NemoLink current table, 16 Oct | 16,031 | 13,778 (To GB), 9,823 (From GB) | 0 |
| NemoLink daily archive | 11,280 | 1,752 | 0 |
| NemoLink weekly archive | 1,344 | 0 | 457 |
| NSL current table, 16 Oct | 17,976 | 17,952 (To GB), 17,592 (From GB) | 0 |
| NSL archive | 16,632 | 6,959 | 1,705 |
| Viking current table, 16 Oct | 20,087 | 20,014 (To GB), 19,000 (From GB) | 0 |
| Viking archive | 6,456 | 6,360 | 0 |

So on NSL 99.9 per cent of To GB rows in the current table are "No Restriction"; "the hours NESO capped the link" describes a few dozen rows, not the table. A row marks an hour NESO gave a limit for, restricted or not. The absence of an hour proves nothing the page can state, and NESO's sentence should be attributed, not asserted.

Fix (same wording on all three and on batch 1's pages, which the seat says have the same major): summary "NESO's limits on flow each way over <Link>, in MW for each hour it lists"; what_it_is "NESO says it publishes a value only where it applied a restriction, yet the files also list hours marked No Restriction" (or drop the sentence); how_used bullet 1 "Each hour's import and export limit, by direction, with NESO's stated reason (including No Restriction)"; bullet 2 "A feature for flow and price models: the hours with a binding limit, picked out by reason". Fix the note bodies the same way (the NemoLink note already admits `No Restriction` rows at line 455, so it contradicts its own page).

### 2. MAJOR (`nemolink`): "an interconnector between GB and Belgium" is not NESO text, and the note says so

Field: `page.summary`. The 6 October 2026 catalogue snapshot (`gridflow\.planning\research\neso-snapshots\20261006T195819Z\catalog-snapshot.json`) contains zero mentions of Belgium, Norway or Denmark anywhere. The `nemolink.md` body (lines 94-98) states "The far end of the link is not named in the NESO package" and carries `TODO: verify the counterpart system operator from a NESO source`; the page contradicts its own note. The only support is ENTSO-E's GB/Belgium border comparison, which the note calls partial.

Recommend dropping the country: "NESO's limits on flow each way over the NemoLink interconnector, in MW for each hour it lists." The same applies to NSL ("Norway") and Viking ("Denmark"), whose notes state the country in body text with no NESO source (nit 4 below); the seat should settle one rule for all seven pages with batch 1's France and Netherlands.

### 3. MAJOR (`nsl`): hold line replaces the ledger's archive question with a load defect

Field: `page.held` ("NESO does not say current rows are unchanged since upload, and the archive repeats a row."). The ledger and `eligibility.md` (line 223) hold NSL on two questions: the dump returns past targets and NESO does not say rows are unchanged since upload (covered), and the archive's operational-date calendar, rollover and `Version` meaning are undocumented (dropped). The repeated row is a separate fact (reproduced: 16,632 rows, 16,631 distinct) that keeps the archive out of silver; it is not a time-semantics question, and fixing it would leave the calendar question open. ElecLink's identical one-table shape (dump plus archive) uses "NESO does not say current rows are unchanged since upload, or define archive days and versions." Use that line, word for word, for consistency with batch 1 and NemoLink's `nemolink_ntc`. The repeat may stay as a fact elsewhere, not as the reason.

### 4. NIT (`nsl`, `viking`): far ends

See 2; if the seat keeps country names on some pages, `nemolink.md` needs its body line changed to say where the country comes from.

### 5. NIT (`nsl`): upload clock reads as a standing schedule

Field: `page.facts.cadence` "uploads at 10:30 GMT each day, 9 to 16 October 2026". True for those days (8 new upload times, 10:30:06 to 10:30:16) and the clock is genuine GMT, but over the whole file the time moves with the clocks (10:30 April to October, 11:30 November to March, across two years). The dated clause is honest, but "each day" invites a standing reading. Suggest "Daily, NESO says; one upload a day, at 10:30 GMT in October 2026".

### 6. NIT (`nsl`): "NESO's October 2026 files hold day-ahead rows only"

Field: `page.what_it_is`. True (both dumps and the archive hold only day-ahead rows) but not an October fact: the whole current table and archive are day-ahead only. Say "NESO's current table and archive hold day-ahead rows only."

### 7. NIT (`viking`): related note

Field: `page.related[2].note` "with two more archive tables". NemoLink has two archive CSVs and Viking has one; "two more" reads as plus two. Suggest "with two archive files and an undated intraday table".

### 8. NIT (`nemolink`): the ingest-only command is right but unexplained

Field: `page.raw_feed.commands[2]`. `gridflow ingest neso_data_portal nemolink_intraday --last 24h` is a real command (`cli.py` `ingest`, `--last` option; the dataset key is in `config/sources.yaml`). The reasoning holds: reproduced from bronze, the 16 October capture (1,145 bytes) has byte-identical rows to 8 October with three headers renamed (`Hourly Time Period GMT`, `Flow in MW To GB`, `Flow in MW From GB`; `Reason For Reduction` unchanged), the registry record has one epoch with the old header (`registry/nemolink.json`), `casting.epoch_for` raises `HeaderEpochError` on any exact mismatch, and `refresh-20261016\DRIFT.md` lists it. Silver holds only the 8 October file. The comment "undated table, bronze only" says nothing of why a reader would not use `pipeline` as on its siblings; one clause would help ("silver pending the renamed columns"). Seat call.

### 9. NIT (shared with batch 1): raw-feed sentence

"The 16 October 2026 table keeps every 8 October row unchanged." True (0 of 15,623, 17,784 and 19,775 rows missing or changed; 408, 192 and 312 appended; headers equal) but it describes two gridflow captures, not a NESO fact; it is also the shared line on batch 1's pages. Seat to decide once. Also the one-table command comments differ slightly between ElecLink ("the capture's date to silver") and NSL ("the current table to silver"); harmless.

## What I checked and found right

- **Second-capture paragraphs, all three notes:** reproduced. NemoLink dump 15,623 to 16,031 (+408 over 17 new upload times, eight 09:30, seven 20:11, one 16:10, one 10:30; 668 distinct; targets 2026-10-07 22:00 to 2026-10-17 21:00; 16,005 of 16,031 targets past; 1,684 before own upload); NSL 17,784 to 17,976 (+192, eight at 10:30, 749 distinct, 17,951 past, none before own upload; 8 October 17,750 and 34); Viking 19,775 to 20,087 (+312, 13 times: eight 09:30, three 16:30, two 02:30; 837 distinct; 20,062 past; 431 before own upload). No full row missing, no key missing, columns equal. File sizes 1,484,249, 1,617,906, 1,809,697 bytes. Silver: third NemoLink file 16,031 rows, second NSL and Viking files 17,976 and 20,087 rows, capture times as written; intraday has only the 8 October silver file.
- **Facts tables:** cadences match the snapshot extras (Daily, Daily, Ad hoc); history dates match archive labels (weekly 20221012 to 20221216; NemoLink daily archive 20221216 to 20240923; NSL from 20221005; Viking from 20231229 to 20240924); member `differs` lines match each header; requests equal each sidecar's `request_url`; vendor lines right (two datastore tables and two archive CSVs for NemoLink).
- **NTC naming:** NemoLink's weekly and intraday descriptions say "NGESO's Network Transfer Capacity"; the rest say "Net Transfer Capacity". Page text is right.
- **Other hold lines** against the ledger: NemoLink weekly and Viking archive (shared archive line), Viking current table (shared dump line), NemoLink intraday (no date, name and lifecycle unexplained) match their questions; none carries a code or local-data reference. NemoLink current-plus-archive uses ElecLink's line.
- **Related links:** every href resolves to a built page; the stated relations hold (NEMO, NSL and VIKING flow columns in historic demand; `NEMO Volume` and `VKL Volume` in the auction summary; NSL has no such column and is not linked to it). "With intraday auctions too" holds (dumps carry Intraday 1 to 4).
- **NSL page:** `nsl.html` renders as a one-table page with no pointer page; lead chip `neso_data_portal/nsl`; three requests listed.
- **Build and render:** all three builds wrote their page with no errors; detector `[]` on `nemolink.html`, `nsl.html`, `viking.html`; screenshots NSL 1440 and NemoLink 390 (390 px iframe) clean, long URLs wrap, nothing clipped. Other widths not re-shot (writer did); dark mode not checked.
- **Rendered text:** no em dashes, no planning words, no codes, British spelling.

---

# Round 2 re-check (2026-10-24)

Rebuilt `--only neso_data_portal/{nemolink_ntc,nsl,viking_ntc}`: each wrote its page, no errors. Detector `[]` on `nemolink.html`, `nsl.html`, `viking.html`. Mirrors `cmp` clean. Rendered `<main>` text has no country name, no "restricts.", no "No row means", no "repeats", no dashes or arrows, no planning words, with one exception (nit 10). No new screenshots (text-only changes in the same fields). The port 9832 server from round 1 stays stopped.

## Verdicts

| Page | Verdict |
|---|---|
| `nemolink` | **APPROVE** (nit 10 to apply) |
| `nsl` | **APPROVE** (nit 10 to apply) |
| `viking` | **APPROVE** (nits 10 and 11 to apply) |

## Round 1 findings, rechecked

1. **Restriction claim (was major): fixed.** Summary is now "NESO's hourly limits on flow each way over the <Link> interconnector, in MW, with reasons". `what_it_is` attributes NESO's note and gives the counter-fact ("It says it publishes only restrictions, yet its October 2026 files hold many No Restriction rows"), word for word the opener on ElecLink, IFA and IFA2; true on all three (the NemoLink and NSL archives and all three current tables carry `No Restriction`). `how_used` matches batch 1's three lines. Note bodies now attribute NESO's sentence and give counts. I reproduced every count from bronze: NemoLink 13,778 To GB and 9,823 From GB of 16,031, both on 8,628, archive 1,752 of 11,280, weekly 457 blank reasons and no `No Restriction`; NSL 17,952 and 17,592 of 17,976, archive 6,959 of 16,632 plus 1,705 blank; Viking 20,014 and 19,000 of 20,087, archive 6,360 of 6,456; intraday none. The NSL and Viking cadence sentences ("most rows are marked No Restriction") are true.
2. **Countries (was major): fixed on the pages.** None of the three pages names Belgium, Norway or Denmark. The note bodies still say GB-Norway and GB-Denmark in prose; they do not render, and the writer flagged them.
3. **NSL hold line (was major): fixed, and true for the NSL archive question.** The line is "NESO does not say rows are unchanged since upload, and archive days and versions are undefined", identical to ElecLink and NemoLink's `nemolink_ntc`. The ledger question for the NSL archive is the operational-date calendar and rollover and the meaning of `Version` (ledger row and `eligibility.md` line 223); the archive carries an operational date and versions 001 to 004 and NESO defines neither. The repeated row stays in the note only, which is fine.
4. **Far ends in note bodies (nit): left as is**, acceptable under the ruling (not rendered).
5. **NSL cadence (nit): fixed** ("one upload a day, at 10:30 GMT in October 2026").
6. **NSL day-ahead (nit): fixed** ("Every row is day-ahead"; true of both dumps and the archive).
7. **Viking related (nit): fixed** ("NESO's limits on NemoLink, with two archives and an undated table"; true: two archive CSVs and the undated intraday table).
8. **NemoLink intraday command comment (nit): fixed** ("bronze only: NESO renamed its columns"); command itself unchanged and right.
9. **Raw-feed sentence (nit): fixed as two fetches** ("Fetched 16 October 2026, the current table ... held every row fetched 8 October unchanged, plus new ones"; verified 0 rows missing or changed on all three). See nit 10 on the verb.

## New findings

10. **NIT (all three, field `page.raw_feed.note`): "held" should be "kept".** The writer says "held" is batch 1's wording, but ElecLink, IFA and IFA2 in the vault worktree now read "the table kept every row fetched 8 October unchanged". "Held" is also the batch's planning word for these very pages, and it is the only banned-list hit in the rendered text. Change "held" to "kept" on `nemolink`, `nsl` and `viking`.
11. **NIT (`viking.md` body, not rendered): leftover over-claim.** Line 76 still reads "hours when the GB system operator capped Viking imports or exports, and the reason it gave" as the use of the table, while most rows are `No Restriction`. Suggest "each hour's directional limit, and the reason NESO gave (often No Restriction)". Not a page issue.

## Consistency with batch 1 (vault worktree as at this check)

Same: summary shape, `what_it_is` opener, three `how_used` lines, archive hold line, current-table hold line, one-table hold line, `landscape`, `pipeline`/`ingest` forms, "Fetched 16 October 2026" raw-feed shape. Differs only in the raw-feed verb (nit 10) and the one-table command comments (ElecLink "the capture's date to silver" against NSL "the current table to silver"), which are harmless.
