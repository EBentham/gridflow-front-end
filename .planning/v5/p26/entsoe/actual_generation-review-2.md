# entsoe/actual_generation: checker re-review (Revision 1)

Checked 2026-09-29 against `actual_generation-review.md`. I re-read the canonical note's `page:` block and body, rebuilt the page, ran the detector and looked at screenshots.

**Verdict: APPROVE.** No blockers or majors remain. There are 2 new nits, and the writer may take them or leave them.

## Prior findings

1. **Blocker, row-time formula: fixed.** `page.record.fields.timestamp_utc` now reads "period start plus (position minus 1) times `resolution`", which matches `parsers.py:530`. The body silver schema cell now reads `start + (position - 1) * resolution` and cites the line.
2. **Major, defect understated: fixed.**
   - `what_it_is` now says that `generation_mw` "may be the consumption figure, unmarked". It lists no zones, so it cannot go stale against the per-zone table.
   - The `how_used` fuel-mix bullets are scoped to DE-LU. The DE-LU fuel mix without B10 is clean: 34,017 of 34,017 rows.
   - The wind and solar bullet is scoped to "where no consumption series is sent".
   - `record.fields.generation_mw` now reads "may be the consumption series; B10 here is pumping load". That is true for the B10 row (4,055.1934 is the out series) and agrees with the vendor rule.
3. **Major, cadence stated as a rule: fixed.** `facts.cadence` now begins "As sent in these responses:".
4. **Nit, vendor citation: fixed.**
   - **Attribution is accurate.** I read both statements on 2026-09-29 from the ENTSO-E Postman collection, fetched as JSON from the documenter API behind https://documenter.getpostman.com/view/7009892/2s93JtP3F6.
     - Item "16.1.B&C Actual Generation per Production Type" says that `inBiddingZone_Domain` series carry generation values and `outBiddingZone_Domain` series carry consumption values.
     - The `psrType` list gives B02 Fossil Brown coal/Lignite, B03 Fossil Coal-derived gas, B06 Fossil Oil, B20 Other and B25 Energy storage.
   - **The citation is usable.** The URL is the vendor's public developer documentation, and the note's paraphrase is faithful. The page does render client-side, so a reader needs a browser, as the note says.
5. **Nit, alt omits geothermal: fixed.** The alt text now reads "oil, waste, geothermal and other renewables".

## New nits

1. **Nit, note body PSR codes section, B07 and B08 source.**
   - **What is wrong.** "B07 Fossil Oil shale and B08 Fossil Peat are from entsoe-py `mappings.py` ... only (de facto)" is inaccurate.
   - **Evidence.** The same Postman `psrType` list names both: "B07 = Fossil Oil shale; B08 = Fossil Peat".
   - **Fix.** Attribute them to the vendor list too. Neither appears on the page.
2. **Nit, `page.facts.cadence`, wrap.**
   - **What is wrong.** At 1440 the value wraps inside the zone code: "15-minute DE-" then "LU".
   - **Evidence.** The browser breaks at the hyphen. Nothing is clipped, but the zone name splits.
   - **Fix (optional).** Reorder so DE-LU does not fall at the line end, for example "As sent in these responses: DE-LU, FR and NL 15-minute; IE-SEM half-hourly; BE hourly".

## Regression checks

- **Gates.** `gridflow-build --only entsoe/actual_generation` passes and the detector returns `[]`.
- **Artefacts unchanged** (series 19:06; sample and notebook 19:04). The chart spec, `record.select` and notebook cells did not change, so the digests still match. The alt text change needs no re-distil.
- **Mirror.** `vault/entsoe/actual_generation.md` is byte-identical to the canonical note (`cmp` clean, both CRLF).
- **Rendered page greps.** No local-data words, em dashes, middle dots, arrows, live or now.
- **Screenshots.**
  - 1440: hero, facts, "What it is" and "How it's used", frame and guide, notebook preview.
  - 390 (390 px iframe): hero, facts, "What it is".
  - The longer cadence value and guide lines fit with no clipping or overlap at either width.
