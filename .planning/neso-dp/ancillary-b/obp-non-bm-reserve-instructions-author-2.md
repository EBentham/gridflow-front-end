# OBP non-BM dispatch instructions: writer round 2 (2026-10-23)

This round answers `obp-non-bm-reserve-instructions-review.md` (APPROVE, 6 nits) and the coordinator's message. All six
are fixed. I changed only the canonical note: the page block plus two body paragraphs, with one paragraph extended. I
mirrored it (`cmp` clean; 430 lines, all CRLF, 0 bare LF). No chart spec, sample select or notebook cell changed, so I
did not re-run the series, sample or notebook. The build's digest check confirms the committed artefacts still match.

| Gate | Result |
|---|---|
| `gridflow-build --only neso_data_portal/obp_reserve_instructions` | ok (one round-2 run failed on `what_it_is` at 62 words; "step by step" became "gradually") |
| Detector | `[]` |
| Rendered page | 0 em or en dashes, arrows or middle dots; none of the forbidden words |
| Screenshots | `obp-reserve-instructions-shots\r2-full-{1440,1024,768,390}.png` and `r2-chart-{1440,390}.png`. The longer key labels fit at every width, and the frame caption wraps cleanly. My 9984 server is stopped; 9670 not touched |

## Fixes

1. **Service names (finding 1; coordinator).** NESO does decode the codes, on sibling packages. Catalogue snapshot
   `20261006T195819Z` has "Negative Quick Reserve (NQR) and Positive Quick Reserve (PQR)"
   (`quick-reserve-auction-requirement-forecast`) and "Negative Slow Reserve (NSR) and Positive Slow Reserve (PSR)"
   (`slow-reserve-requirement-forecast`). The ASDP notes have "Regional Development Programme (RDP) MegaWatt (MW)
   Dispatch". I re-grepped the snapshot for both decodes. "Positive" now appears wherever the page names the services:
   - `what_it_is`
   - `how_used[0]`
   - key labels "Positive Slow Reserve" and "Positive Quick Reserve"
   - chart `alt`
   - `plot_alt`
   - frame caption: "Two instructions: Positive Slow Reserve, 29 July 2026; Positive Quick Reserve, 14 August, no STOP."
   - `service_id`: "`PQR` Positive Quick Reserve, `PSR` Positive Slow Reserve or `RDP` MW Dispatch (NESO)"

   The note body's opening paragraph now quotes the three decodes with their packages.
2. **`Target MW` against PN (finding 2; coordinator).** I softened the body paragraph to what the rows show. It now
   names both PN captures (2026-10-08 and 2026-10-16, which give the same values). It adds that all 80 Positive Quick
   and Slow Reserve STARTs read 0 MW, and that 72 STARTs fall in a PN segment, 65 of them on a PN of 0. It then names
   the seven STARTs on three units that read 0 on a PN above zero, and says "an absolute level would not read 0 there,
   but seven rows on three units settle nothing". Two reasons follow: both PN captures postdate the instructions, so a
   PN revised afterwards cannot be ruled out; and EDFE-21's instruction `3193911` fits the difference reading less
   neatly. I reproduced that row: target 10 MW from 2025-10-10T17:20:03, PN 0 until 17:30, then 10. The TODO stays open.
   The page still only quotes NESO.
3. **Notebook lead (finding 3; coordinator).** "cell one converts to UTC" is now "the first query cell converts
   `point_datetime` to UTC". It is still 35 words: "with both ends included" became "both ends included".
4. **`sequence` field (finding 4).** Now "Point order within the instruction; here one skips 4 and has no STOP".
5. **Related ASDP note (finding 5).** Now "ASDP, NESO's earlier platform for non-BM instructions; never join its ids", the
   checker's wording.
6. **Report correction (finding 6).** My round-1 report was wrong to say "NESO never decodes `PQR`, `PSR` and `RDP`",
   and wrong to list the mapping under Unverified. NESO decodes all three on sibling packages (item 1). Nothing about the
   codes being inferred belongs in the ledger or the Defects list.

## Added: the second clock case (checker's point 3)

The body's time paragraph now gives two BST observations that fit UTC without proving it:
- **2 October 2026:** last point 06:44:00, file stamp 06:44:26, `last_modified` 06:44:33.
- **14 August 2026:** file `instr_20260814163227_qr_sr_nbm.csv` (stamp 16:32:27, `last_modified`
  `2026-08-14T16:32:39`) against a last point of 16:32:00 that day, with no point between 14 August and 2 October.

The August file is in gridflow's portal probe, `.planning/phases/neso-data-portal/_probe/package_search_p0.json`. I
confirmed its name and `last_modified` there. The silver gives the last point (instruction `7542155`, VP at 16:32:00).
In both cases the stamp sits seconds after the last point, which UK local point times would not give. The page still
says only "Times are UTC, NESO says".

## Defects

There are no new defects, and the round 1 data defects stand:
- four Quick Reserve instructions on 14 August 2026 have no STOP;
- one SPP is off the half-hour grid;
- the ids do not run in time order;
- the workbench returns times in the session's zone.

The seat item the checker raised is outside this package: the approved ASDP note (line 520) still says OBP's vendor text
puts some non-BM instructions on ASDP.

OBP instructions page: all six review nits fixed, NESO's own service names used, body tightened; build ok, detector `[]`.
