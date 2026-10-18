# Phase 2 FFR auction results (`phase-2-ffr-auction-results-summary`): review

Checker, port 9969 (server stopped), 2026-10-18. Lead `ffr_phase2_auction_phase_resultsbyunit` (seat ruling d9a2f0f; `resultsum` and
`blockorders` held per the registry, ledger mismatch is defect 20l: not a finding).

## Verdict: APPROVE

0 blockers, 0 majors, 5 nits. Build `--only neso_data_portal/ffr_phase2_auction_phase_resultsbyunit` clean (the "3 lines dropped"
caveat warning is another note: `_extract_caveats` on this note drops 0). Detector `[]`. Page has 0 em dashes, middle dots, arrows
or en dashes. Mirror `cmp` identical; canonical note 1,252 of 1,252 lines CRLF.

## Nits

1. **nit** `page.family.members[resultsbyunit, resultsum, blockorders, linearorders].differs` ("three trial years"). The trial's
   results run 7 December 2019 to 30 November 2021 (about two years). What there are three of is NESO's yearly files
   (`masterdata-2019-2020`, `-2020-2021`, `-2021-2022`, split at 3/4 April). A reader beside the hero's "7 December 2019 to
   30 November 2021" will count two. Suggest "three yearly files". Evidence: silver `efa_date` per capture 2019-12-07..2020-04-03,
   2020-04-04..2021-04-02, 2021-04-03..2021-11-30.
2. **nit** `page.raw_feed.commands[2].comment` ("both into one table") and the held lines of `results_sum` / `results_unit`
   ("its rows join the results summary / results by unit table"). True, and the page never says add or sum, but "both into one
   table" and "join" are the two places a reader could take the weekly and yearly files as additive. In silver the base table holds
   both copies (69,207 rows = 69,006 yearly + 201 weekly; 201 keys twice, 0 differ in price, volume, cancellation note or company)
   and `_latest` keeps one. Suggest "both files, repeated rows collapse to one" and "its rows load into the ... table and repeat the
   yearly rows".
3. **nit** `page.notebook.needs` ("the by-unit yearly and weekly files"). The cells query 24 to 30 July 2021, which only the
   2021-2022 yearly file holds (silver capture of `feafb7ab` covers 2021-04-03..2021-11-30; the weekly covers 27 to 30 November
   2021 only). The weekly is not needed. Suggest "a capture of the 2021-2022 by-unit file".
4. **nit** `page.notebook.cells[1]` (`cleared_mw`). The block table's LFS block 1 total of 98 MW includes the two rows the frame
   shows with NESO's cancellation note (2 x 20 MW) and the unshown ninth unit (UF_GBD13, 2 MW; 96 shown + 2 = 98). The page rightly
   draws nothing about the note, but a summed figure over rows it has just flagged invites a question. Either say in
   `notebook.lead` that the sum includes rows NESO marks cancelled, or leave as is.
5. **nit** vault body, "Weekly and master exports" linear row and the author-report line: `order_entry_time` differs by dropped
   seconds, not only spelling (weekly `2021-11-25 10:59:07`, master `25/11/2021 10:59`). Body correction 3 says "spelling". Page
   unaffected.

## Checked and correct (the four things asked about)

1. **Chart.** Series `gridflow-distil`, `spec_origin: vault`, spec digest passes, no staged spec left. Recomputed from silver (latest
   `published_at` per service, date, block; mean per date): DLH 715 days, 1.00 on 2021-03-12, 11.347 on 2021-02-09, median 7.87;
   LFS 718 days, 3.235 on 2020-08-19, 4.10 on 2020-09-05 and 06, median 4.058; DLH above LFS on 686 of 715. Every alt figure
   matches (3.235 reads as 3.24). Gaps: raw bronze CSV has 0 rows for 20 to 26 March 2021 and 0 DLH rows for 1 to 3 September
   2021 (LFS present), so the gaps are NESO's. Rendered paths: DLH 469+158+88 = 715 points in three segments, LFS 469+249 = 718 in
   two; recomputed y pixels match. "Cleared": 0 rows with cleared volume at or below 0, so every charted block cleared. One price
   per block: 8,529 service/date/block groups, 0 with two prices. Unit £/MW/h is the by-unit dictionary's.
2. **The two spellings.** Weekly files are registry resources `edfb5b8f`, `5cce4cb6`, `a9659701`, `87ee8fc4` (dated 26.11.2021);
   all 20 request URLs on the page equal the bronze sidecar `request_url`s and sit under the right member. Equality, measured:
   by-unit 201 weekly keys all in the master, no value differs (delivery strings only). Block order: 379 weekly rows equal, as a
   multiset, the 379 master rows delivering 2021-11-26 23:00 to 2021-12-03 23:00 on the nine columns the body names (a 20-column
   comparison differs only on `block_code_prm`, which is also collapsed). Linear: 84 pairs equal on efa, executed volume, p1..v4,
   member, portfolio, user, currency, delivery end; differ in `order_id`, `order_period_id`, `trade_id` (full vs `1E+14`) and
   `order_entry_time`. Summary: 84 weekly keys, all duplicated in the masters, one value each. `results_sum` / `results_unit`
   load into `resultsum` / `resultsbyunit` (registry `siblings`; silver captures of the weekly files present in those tables;
   `generic.py` reads `(dataset, *siblings)` bronze). Body edits 2 to 5 verified (linear masters sci-notation on 4,284 and 2,940
   rows, 2019-2020 master 1,008 rows clean). Commands match the connector: `iter_members` fetches each family's own resources,
   `--last 24h` window is admissible, same form as the approved Dynamic Containment page. The page never says to add the files
   (see nit 2 for wording).
3. **Held lines.** Archive lines match registry questions (no dictionary, price unit and clock unknown; summary archive dates and
   blocks undocumented). ZIP contents: two files each (22 and 29 November 2019), seven linear files 2019-11-22 to 2020-01-03, up
   to 16 points. 22 November 2019 by-unit hold is the registry's collision (UF_LJP12, 2019-11-24, EFA 11, DLH, volumes 0 and 10,
   same price). `resultsum` and `blockorders` lines match the registry questions.
4. **Sample rows and notebook.** Eight rows equal silver (UF_GBD02, 03, 05, 06, 12, 14, 15, UF_KWP01; the ninth is UF_GBD13);
   cancellation note on UF_GBD14 and 15 only. All 14 shown columns have a guide line (key first); the four pipeline columns have
   none. Guide text agrees with the dictionaries ("Equivalent date to the delivery end date", cleared volume "accepted as per the
   cleared price", "Whether or not the bid has been cancelled") and with code (`timestamp_utc` 2021-07-23 23:00 UTC = UK midnight
   of 24 July). Notebook written by `scripts/run_notebooks.py`, 5 cells read-only, no errors. `query()` reads
   `silver_neso_data_portal_ffr_phase2_auction_phase_resultsbyunit_latest`, date column `efa_date`, `BETWEEN` both ends, drops
   the lineage columns. Outputs recomputed: block 1 LFS 9 units, 98 MW, one price 5.40; LFS 5.40 in each day's first two blocks and
   3.40 otherwise (blocks 1,2,7,8,...,37,38); DLH 5.04 (27 July, block 20) to 11.22 (27 July, block 21); DLH absent in blocks 6,
   12, 18, 24, 30, 36, 40, 42. Notebook tab, aria text and hero chip all name the by-unit lead.

## Other

- Facts: 16 CSV and four ZIP (registry); "Not Active" (note line 1089); last changed 2021-03-31 to 2022-03-18 (sidecars); "42
  blocks, 6 four-hour blocks each day" quoted from the dictionary; DLH and LFS names from the dictionary; linear member is NATIONAL
  GRID ESO on all 84 and 8,232 rows; block orders Executed or Rejected, volumes negative. Related notes 10 to 11 words each; DC
  results from 16 September 2021, SFFR from 1 April 2023, EAC from November 2023 agree with those pages.
- No local data on the page beyond the standard frame pipeline columns; no planning words, no "live".
- Screenshots (1440, 1024, 768, a 390 px iframe): nothing clipped or overlapping in hero, chart, raw feed, frame (folded and
  unfolded), notebook, related. At 768 the folded frame hides `cancelled` and at 390 the notebook tab label clips: both known
  template items.
- Writer's defects section is accurate: 20l-style registry hold mismatch and the linear-master identifier collapse are real.
