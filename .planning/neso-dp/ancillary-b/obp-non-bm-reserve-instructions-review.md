# Review: `obp-non-bm-reserve-instructions` (lead `obp_reserve_instructions`)

Checker, 2026-10-23. **Verdict: APPROVE.** 0 blockers, 0 majors, 6 nits.

Gates run: `gridflow-build --only neso_data_portal/obp_reserve_instructions` ok (only the vault-wide "22 lines dropped"
warning); detector `[]`; mirror `cmp` clean; note is CRLF throughout (416 lines, 0 bare LF); no em or en dashes, arrows or
middle dots in the added lines or the rendered page; none of the forbidden words in the rendered page. Screenshots taken
at 1440, 768 and 390 (chart, legend, frame, notebook preview): nothing clipped, no horizontal page scroll at 390 or 768.

## The five points you asked about

1. **Service codes.** The mapping is not an inference: NESO decodes all three, just not on this package. The catalogue
   snapshot `20261006T195819Z` has "Negative Quick Reserve (NQR) and Positive Quick Reserve (PQR)" in the notes of
   `quick-reserve-auction-requirement-forecast`, "Negative Slow Reserve (NSR) and Positive Slow Reserve (PSR)" in the notes
   of `slow-reserve-requirement-forecast`, and "Regional Development Programme (RDP) MegaWatt (MW) Dispatch" in the ASDP
   notes (the OBP package also tags "Quick Reserve", "Slow Reserve", "MW Dispatch"). Local silver agrees: in
   `obp_reserve_avail_price`, `pair_id` is 1 for PQR and -1 for NQR. gridflow code does not decode them. The page may keep
   its `service_id` line as written (finding 1 is a wording nit). The writer's report line "NESO never decodes" is wrong.
2. **Target MW as a difference from PN.** Reproduced, and the page claims none of it: the `target_mw` guide line only
   quotes NESO and says "no sign stated". Against `obp_physical_notifications` (both captures, 8 and 16 October, give
   identical results): 85 STARTs, 72 fall in a PN segment of the same unit, 65 of those on a PN of 0, and 7 on a PN above
   zero (EDFE-8 17:43 PN 4; ENGQR-02 18:44 and 19:03 PN 2; ENGQR-03 17:59, 21:00 and 23:13 on 2026-06-23 and 18:44 on
   2026-07-02, PN 1). All seven START at 0 and rise to 1 or 2. The body paragraph is worded more firmly than that supports
   (finding 2). It is in the vault note only, not rendered.
3. **Times.** No point or issue time falls on 25 to 27 October 2025 or 28 to 30 March 2026 (the 24 distinct days in the
   file: none near either change). Bronze cells have no zone marker (`2025-10-10T10:00:00`). The notebook outputs read
   correctly: after `tz_convert("UTC")` the KILN-01 rows print `20:36:00+00:00` to `21:25:32+00:00`, equal to silver, and the
   plot axis reads 20:40 to 21:30 UTC. Extra support for UTC that the writer did not use: the earlier catalogue snapshot
   (20260820T214455Z) lists the file `instr_20260814163227_qr_sr_nbm.csv`, stamped 16:32:27, and the last point on 14 August
   2026 (BST) is 16:32:00, with nothing between 14 August and 2 October. That is a second BST day where the file stamp sits
   seconds after the last point, so the points are not local clock time.
4. **Chart.** Reproduced from silver (START points, mean `target_price` per UTC day, 10 October 2025 to 2 October 2026):
   Slow 3 days (27 July 169.07, 29 July 120, 5 August 187.804), Quick 19 days (min 119.417 on 20 April, max 160 on 2 October,
   exactly 150.0 on 10 days), MW Dispatch 4 days (-210 on 27 and 30 April, -99 on 20 May, -75 on 16 June). The committed
   series JSON matches on every value; caption, alt and key notes match; `y_min: -240` does not clip -210; units and the
   absence of a stated sign are as NESO has them (dictionary: Target Price £/MWh "Indicative Price", no sign rule). The
   dot-only rendering reads correctly at all widths.
5. **What a row is, the missing STOPs, ASDP.** Confirmed: 85 instructions, points per instruction 4 (25), 5 (42), 6 (14),
   7 (4); `instruction_point_id` unique (422) and (`instruction_id`, `sequence`) unique. STOP 81 against START 85: the four
   instructions without a STOP are 7541953, 7542155, 7542224, 7542315 (ENGQR-05, -06, -01, -03), each starting 2026-08-14
   16:00, each skipping `sequence` 4 and one point id. One off-grid SPP (7452940, 20:46:00) and the other 87 on :00 or :30.
   8 instructions change price, always at an SPP (12 changes). Id ranges per day are as the note states. ASDP wording is
   faithful to NESO's text ("will incrementally master more non-BM services, and less will be mastered by ASDP"; "have now
   migrated to the OBP system"; extras "Update Frequency: Not Active"), and the note's "monthly files (to April 2026) ...
   Fast Reserve and STOR" matches ASDP silver (Fast Reserve to 2026-04-17, STOR to 2026-01-15, RDP_NEGATIVE to 2025-11-12).

## Findings

1. **nit** `page.chart_view.key[*].label`, `page.record.fields.service_id`. NESO's own names are "Positive Quick Reserve" and
   "Positive Slow Reserve", and the dictionary lists NQR and NSR as well (absent from this file). "Quick Reserve" and "Slow
   Reserve" are the package's umbrella names, so this is true as written; "Positive" would be more exact if the budget
   allows. Optionally cite the decode in the note body (the three snapshot quotes above) so the mapping is not left looking
   inferred.
2. **nit** Note body, Units paragraph (`Target MW`, the project check). The seven rows reproduce, but "For those rows
   `Target MW` behaves as a difference from PN, not an absolute level" is firmer than seven STARTs on three units can
   carry: PN is a later capture and could have been revised after the instruction, and the PN files give two captures with
   the same values, so they do not test that. One row does not fit the difference reading neatly: EDFE-21 instruction 3193911
   (START 17:20, target 10) sees its PN go from 0 to 10 at 17:30, equal to the target. The paragraph already says "not a vendor
   statement" and keeps the TODO open, so a softer clause is enough, for example "reads 0 at a START where the PN is above
   zero on these seven rows, which an absolute level would not". Also say which PN capture was used. Supporting fact the
   paragraph could add: all 80 Quick and Slow Reserve STARTs read 0 MW (the note already counts 80 zero STARTs). The five
   RDP STARTs do not (3.9 to 4.6 MW, then 0), which the paragraph covers.
3. **nit** `page.notebook.lead`. "cell one converts to UTC": the page numbers the setup cell [1] and the conversion [2] in the
   preview and [3] in the full notebook, and only `point_datetime` is converted (`timestamp_utc` and `issue_datetime` stay in
   the session zone). Suggest "the first query cell converts `point_datetime` to UTC".
4. **nit** `page.record.fields.sequence`: "here one skips 4, its missing STOP". The rows show a skipped sequence number and
   an instruction with no STOP; they do not show that the skipped point was the STOP. "here one skips 4 and has no STOP"
   states only what is visible. The frame caption ("its STOP missing") is fine.
5. **nit** `page.related[0].note`: "ASDP, the platform these services move from". ASDP silver carries only Non-BM STOR, Non-BM
   Fast Reserve and RDP_NEGATIVE; it has no Quick Reserve or Slow Reserve rows, and Quick Reserve is 363 of the 422 rows
   here, starting 10 October 2025. NESO's OBP text does say Slow Reserve and MW Dispatch "migrate from ASDP", so this is a
   nit, and it echoes the already-approved ASDP page ("where these moved"). A safer line, 11 words: "ASDP, NESO's earlier
   platform for non-BM instructions; never join its ids".
6. **nit** Writer report (not the page): "NESO never decodes PQR, PSR and RDP" and the line recommending a softer
   `service_id` wording is unnecessary given point 1 above; do not carry "inferred" into the ledger or the Defects list.

## Not findings, for the seat

- The approved ASDP note (line 520) still says the OBP page's vendor text "says some non-BM instructions are still published
  on ASDP". That reads as the old OBP wording; it is outside this package.
- Template items the writer listed (hanging-indent wrap in the notebook preview at 390, dot chart without a bucket, folded
  frame at 768, tab label clipping) were not re-raised.
- Chart legend glyphs show a line with dots while the chart draws dots only; a template matter.
