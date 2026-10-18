# Held pages, Ancillary services part 2: checker review (2026-10-18)

Checked against the batch file, standing instructions, the writer's report, the four canonical note diffs against `origin/master`
(front matter insertions only), the mirrors, the built pages, the ledger rows and registry hold questions, gridflow `client.py` and
`endpoints.py`, bronze sidecars and bronze bodies (read only), and part 1's two held reviews.

Gates: `gridflow-build --only neso_data_portal/<lead>` ok on all four; `cmp` canonical note against mirror clean on all four;
detector `[]` on all four; 0 em or en dashes; none of live, now, yet, soon, pending, coming, planned, shipped, real-time, locally,
ruling, ledger, TODO on the pages; no capture dates, row counts or other local figures on the pages (the only counts are vendor
file counts: "14 files", "2013-14 to 2026-27"); 390 view through my own 390 px iframe on port 9978 (stopped): `scrollWidth` equals
viewport width on all four, no element outside the viewport, no clipped or scrolling code blocks, read in slices (ORPS and
Disaggregated) and 1440 (ORPS): nothing clipped or overlapping.

Seat rulings applied: the Disaggregated BSAD title follows the Aggregated page; ORPS linking only to constraint breakdown is fine
(the catalogue holds two voltage packages, `outturn-voltage-costs` and `monthly-utilisation-data-of-voltage-contracted-units`, but
neither is in the page set).

Checked and fine: all request URLs equal the bronze sidecar `request_url` (uploads) or the dump path built from the resource id
(`endpoints.build_dump_path`); `package_show` is `/api/3/action/package_show?id=<package>`; Disaggregated: 8 uploads (2013-14 to
2020-21, the last named `data.csv`) then 6 dumps from 2021-22, as the page says; the 2013-14 and 2026-27 examples are correct;
ASDP's two dump ids are the 2025 and 2026 resources, and the rows really are windows in 2025 (Jan to Dec) and 2026 (Jan to Apr);
"kept only if its body changed" and "at most weekly" match `iter_members` and `_FROZEN_CADENCE`; ORPS workbook and both PDFs are in
bronze under the files family; Elexon DISBSAD `adjustment_action_id` is non-null on every local row; ledger and registry hold
questions match the reasons for contract transfer (identity), Disaggregated (identity), ASDP (unit, plus the clock parenthetical),
ORPS historic (dash and repeated identity), ORPS default (price-input units).

## 1. `contract-transfer-of-obligation` (lead `contract_transfer_obligation`) — APPROVE

1. **nit** `page.how_used[1]`, `page.related[1]`: "EAC" is never spelled out (Enduring Auction Capability). Part 1 flagged the same.
2. **nit** `page.related[2].note`: "The Balancing Reserve requirement those auctions buy against" states a relationship the note
   does not source (the note only calls this log "a side channel to the auction results"). Probably true; "The Balancing Reserve
   requirement forecast" is safe.

## 2. `disaggregated-bsad` (lead `disaggregated_bsad`) — APPROVE

1. **nit** `page.facts.cadence`: "2026-27 is the current, partial year" is true today and false from April 2027, and it is not
   NESO's statement. Suggest "NESO states no update frequency; the newest file is the current financial year".
2. **nit** `page.raw_feed.requests[2]`: the dump example carries no year in its address, and nothing says which year it is. Add
   "(2026-27)" to the note or a comment, or say "the newest year's dump".
3. **nit** `page.how_used[0]`: "Splitting balancing adjustments into system and energy actions per settlement period" is a use the
   note does not state, and sits beside a hold about identical repeated rows (a per-flag split would count them). Low risk.

## 3. `non-bm-ancillary-service-dispatch-platform-asdp-window-prices` (lead `asdp_window_prices`) — APPROVE

1. **nit** `page.facts.cadence`, `page.what_it_is`: "OBP" is used twice and never spelled out (Open Balancing Platform), and
   "Non-BM" is not explained (outside the Balancing Mechanism).
2. **nit** `page.what_it_is`: "Never join ASDP ids to OBP ids" gives no reason. Suggest ending "...: the two use different
   identifier systems" (the note's own reason).

## 4. `obligatory-reactive-power-service-orps-utilisation` (lead `orps_utilisation_reactive`) — REVISE

1. **major** `page.family.members[0].differs`: "April 2020 to December 2024, one column per month" is wrong. The archive carries a
   lead, lag and total column for each of its 57 months (header `Apr 20 -LEAD, Apr 20 - LAG, Apr 20 - TOTAL, ...`, 171 value
   columns). The next member's line ("a lead, lag and total column per month") makes the contrast read as if the archive had one
   value per month. Suggest "April 2020 to December 2024, a lead, lag and total column per month".
2. **major** `page.family.members[0].differs`, `page.raw_feed.note`: the raw feed lists a request for NESO's newer long file
   (`reactive-utilisation-data.csv`, where every month after December 2024 lives) but nothing says it never reaches a silver table.
   The page says "The workbook and PDFs stay in bronze", which names the other bronze-only files and omits this one, so a reader
   will assume the long file feeds the silver table. The note holds it separately (resource-level hold, bronze only; its own
   question is whether one repeated complete row is a publication defect or two real utilisations). That repeated-row problem does
   need a word, but in the raw-feed note, not the 16-word reason (the family's reason should stay the archive-versus-long
   question). Suggest raw_feed.note: "The workbook, the PDFs and the newer long file stay in bronze; the long file repeats a
   complete row." and `differs`: "...and NESO's newer long file, kept in bronze only".
3. **nit** `page.family.members[0].held`: "NESO does not say which is right" turns the hold question (is this archive superseded)
   into a correctness dispute. The ledger also holds on blanks the long file writes as zero. Suggest "NESO's newer long file
   differs from this archive on some values and writes blanks as 0; NESO does not say which to use."
4. **nit** `page.what_it_is`: "lead (absorbed) and lag (produced)" is flat, but the note attributes the reading to the historic
   file's dictionary ("reads leading as absorption"). Suggest "(read as absorbed)" and "(read as produced)".
5. **nit** `page.summary`: "each BM unit" repeats NESO's package wording; the writer's own check found 143 of 243 `unit` names
   absent from the BM unit register. Suggest "each unit".
6. **nit** `page.family.members[1].held`: the `-` code span renders as a bare hyphen ("what a - cell means"), which reads like a
   typo. Suggest "what a dash cell means".
7. **nit** `page.family.members[2].held`: "only £" reads awkwardly and the three symbols are bare. Suggest "NESO gives the three
   power-price inputs only a pound sign, with no denominator."
8. **nit** `page.how_used[1]`: "The default rate" is singular; the table holds two rates (the note: "payment rates under
   different utilisation-factor conditions").

## Defect worth carrying (writer's, confirmed)

`disaggregated-bsad.md` body still says "captured once, on 2026-10-08" and "Only one capture per resource exists"; bronze also holds a
16 October capture of the 2026-27 dump (same resource id, new sidecar). Not a page finding.

## Summary

| Page | Verdict | blocker | major | nit |
|---|---|---|---|---|
| `contract-transfer-of-obligation` | APPROVE | 0 | 0 | 2 |
| `disaggregated-bsad` | APPROVE | 0 | 0 | 3 |
| `non-bm-ancillary-service-dispatch-platform-asdp-window-prices` | APPROVE | 0 | 0 | 2 |
| `obligatory-reactive-power-service-orps-utilisation` | REVISE | 0 | 2 | 8 |
