# Held pages, Ancillary services part 2: checker re-review (2026-10-18)

Re-checked against `held-b-author-2.md`, the diffs of the four canonical notes against `origin/master` (front matter only), the
rebuilt pages, gridflow registry and local silver (read only).

Gates: `gridflow-build --only neso_data_portal/<lead>` ok on all four; detector `[]` on all four; `cmp` canonical note against
mirror clean on all four; 0 em or en dashes; none of live, now, yet, soon, pending, coming, planned, shipped, real-time, locally,
ruling, ledger, TODO; no dates or row counts on the pages; 390 view through my own 390 px iframe on port 9978 (stopped): no
horizontal scroll, no element outside the viewport, no clipped block on any of the four, ORPS read in a slice. Port 9670 untouched.

## The two ORPS majors

1. **Archive columns: fixed.** Lead member: "Lead, lag, total by month, April 2020 to December 2024, plus the long file";
   historic: "Lead, lag and total by month, October 2013 to March 2020". True to the headers (lead, lag and total for each month in
   both files).
2. **Long file in bronze: fixed in substance.** Raw-feed note: "Bronze only: the workbook, PDFs and newer long file, which repeats
   a complete row." Checked against code and data. Registry: resource `528b03d2` has `disposition.kind: HOLD` (ORPS-REACTIVE-LONG-DUPLICATE,
   it repeats one complete row twice), family `orps_utilisation_reactive`. Local silver for that family is 243 rows, one
   `bronze_capture_id`, and it is the archive capture (`a61c6c26...b9e76522.csv`); the long file's capture contributes no row.
   The workbook and both PDFs are in bronze under the files family. So the note is exactly right.

**The seat's possible contradiction.** The two lines say different true things, not opposite ones: the member line lists what the
member's requests fetch (the archive and the long file), the note says what is kept (the long file only in bronze). It is not a
factual contradiction, and the note settles the point on the same page. But "Lead, lag, total by month, April 2020 to December 2024,
plus the long file" reads on its own as a description of the table's coverage, and a reader who stops there will think the long file
is in it. I would still change it (nit, not a blocker): "Lead, lag, total by month, April 2020 to December 2024; long file bronze
only" is 14 words, the budget the writer cited.

## The 15 nits

| Finding | State |
|---|---|
| Contract 1, EAC | fixed: "Enduring Auction Capability (EAC)" at first use |
| Contract 2, unsourced relation | fixed: "The Balancing Reserve requirement forecast" |
| Disaggregated 1, stale "current" | fixed: "the newest file is the current financial year" (still relative, but true whenever read) |
| Disaggregated 2, which dump | fixed: "(2013-14 and 2026-27 shown)", matching the two file requests |
| Disaggregated 3, unstated use | fixed: "Cost and volume of individual balancing actions outside the Balancing Mechanism" |
| ASDP 1, OBP and Non-BM | fixed: "Open Balancing Platform" in cadence, "(OBP)" at first use in `what_it_is`, "(outside the Balancing Mechanism)" |
| ASDP 2, reason for no join | fixed: "The Open Balancing Platform (OBP) uses other ids: never join the two." (the note's reason) |
| ORPS 3, held reason | fixed in kind (no longer "which is right"; blanks as 0 named); see new nit 1 |
| ORPS 4, lead and lag | fixed: "(read as absorbed)", "(read as produced)" |
| ORPS 5, "BM unit" | fixed: "each unit" |
| ORPS 6, dash | fixed: "what a dash cell means" |
| ORPS 7, pound sign | fixed: "only a pound sign, with no denominator" |
| ORPS 8, two rates | fixed: "The two default rates NESO pays ... in £/MVArh" |
| the three shortened for budgets | ASDP "Each row gives provider, asset, service, window, price and creation time" (drops "start and end": fine); ORPS "Grid Code generators must be able to ..." (fine); ORPS "Another table holds default payment rate inputs" (fine) |

## New nits (none blocks)

1. **nit** `family.members[0].held`: "Some long-file values differ, with 0 for blanks" no longer says from what. "Some long-file values differ from this archive, and it writes
   blanks as 0; NESO does not say which file to use" is the plain version (watch the 16-word limit; "differ from this archive's" can
   replace "Some long-file values differ" at the same length if "with 0 for blanks" is kept short).
2. **nit** `family.members[0].differs`: see the member line above; suggested wording within 14 words.

## Verdicts

| Page | Verdict |
|---|---|
| `contract-transfer-of-obligation` | APPROVE |
| `disaggregated-bsad` | APPROVE |
| `non-bm-ancillary-service-dispatch-platform-asdp-window-prices` | APPROVE |
| `obligatory-reactive-power-service-orps-utilisation` | APPROVE |

0 blockers, 0 majors, 2 nits. Both majors and all 15 nits are fixed; the long file feeds no silver table, so the raw-feed note is
correct and the member line is only ambiguous, not wrong.
