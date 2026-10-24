# Held FES pages, part 1: writer round 2 (2026-10-24)

I applied eight of the nine review nits and skipped one. FLX1 is unchanged.

## Gates

- **Mirror:** each changed note was copied to the mirror with `cp`, then checked with `cmp`. All four are clean (building heat model, ED1, ES1, ES2).
- **Line endings:** every line in those four notes is still CRLF.
- **Build:** each changed page was rebuilt with `--only`. All four wrote their pages with no errors.
- **Detector:** `[]` on all four pages.

## Fixes

1. **ED1 hold line** now covers only the files that carry NESO's wording: "NESO's 2023 to 2025 files call annual data fiscal, but not which year a label names." (16 words)
2. **ED1 note body, Holds part 1:** the stale "`TODO: verify` in the ED2 PDFs" now names what is still open: whether each label is the start or end of its period, and the period for the 2026 file.
3. **ES2 raw feed note** now ends with the "Shown:" sentence the other pages have: "Shown: 2023, 2025, 2026." To stay within 30 words, two other parts changed:
   - "each downloaded whole unless its `last_modified` is unchanged" became "downloaded whole when `last_modified` changes", which means the same thing.
   - "its 2026 notes file" became "its 2026 notes".
4. **ES2 cadence: skipped.** "As at 6 October 2026" correctly dates the catalogue snapshot, and the raw feed note already gives the 9 October change. Changing it would add a claim.
5. **ES2 note body, Holds part 3:** "NESO answered the upload half" became "NESO replaced the notes with a supply table on 2026-10-09".
6. **ES2 note body, present tense:**
   - The "Why 2026 is held" bullet now reads "The 2026 body, as captured 2026-10-08, is ...".
   - The HOLD table reason now ends "registry reason, describing the 2026-10-08 capture".
7. **ES1 `what_it_is`:** "NESO says" now covers only NESO's own words: "NESO says the files cover capacity, generation and interconnector flows. Rows run by connection, scenario or pathway and technology."
8. **Building heat model, input-list hold line:** made singular, because there is one identical pair: "One row appears twice and no column tells them apart, so there is no silver table." (16 words)
9. **Building heat model `how_used`:** "months" was an inference, so I dropped it. The line is now "Run the workbook for other buildings and heating systems", which rests on NESO's catalogue text (heating system types and building characteristics).
