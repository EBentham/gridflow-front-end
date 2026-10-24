# Held Carbon intensity pages, round 2: writer report (2026-10-24)

This round applies the five seat rulings on `held-review.md` (APPROVE with nits). Notes were edited in `C:\gridflow-wt\vault-neso-ci` with the Edit tool, keeping CRLF: 298, 247, 267 and 320 lines, 0 bare LF. Each note was copied to the mirror and `cmp` is clean on all four. `gridflow-build --only neso_data_portal/<key>` rebuilt all four pages with no errors, and the detector returns `[]` on each. The rendered `<main>` text has no dashes, arrows or middle dots and no banned words. No artefacts. No new screenshots: the text changes are the same length or shorter in the same fields.

## Fixes

1. **Shared first clause (ruling 1).** No change. All four lines still open with "No row says when NESO first published it", balancing actions included.

2. **Regional hold line (ruling 2).** The negative-values question fits:
   - `page.held` is now "No row says when NESO first published it; half-hour labels and negative values are unexplained." (15 words.) It names all three registry questions: issue and revision, where a label sits in its half hour, and negatives.
   - `what_it_is` now spells out the label question: "One column per region gives NESO's forecast; NESO does not say whether each time starts or ends its half hour." The negatives sentence stays. The dropped clause ("from machine-learning models and metered generation, NESO says") made room. The field is now 59 words.

3. **What the change is measured against (ruling 3).** `what_it_is` on balancing actions, country and national no longer says "had changed values for half hours past on 8 October". It now says:
   - balancing actions and country: "NESO's 16 October 2026 file changed values its 8 October file gave for past half hours."
   - national: the same sentence with "actuals".

   Word counts are 60, 52 and 59.

4. **Country count (ruling 4).** The note body's "Identity" bullet now gives both readings:
   - nine targets (04:30 to 09:00; England 4, Wales 9) carry labels before the first file's stamp of 09:10:31;
   - read as period starts, as the note does, the 09:00 half hour was still running, so eight (04:30 to 08:30; England 3, Wales 8) had ended.

   I re-derived both counts from bronze (`ci-held-writer\eight.py`). Neither count appears on the page.

5. **Sentences equating the CSVs with the API (ruling 5).** Each is now attributed to gridflow's probe with its date, or cut:
   - **National intro:** "It is the bulk file of the same series that the Carbon Intensity API's national routes serve" is replaced. NESO's text does not say this; its PDF only opens with the API. gridflow's own probe of 2026-10-09 (LIVE-PROBE) found forecast and actual equal on all 675 overlapping periods. In the clocks paragraph, "The seat's live probe" becomes "The seat's probe of 2026-10-09 (local silver, no network)".
   - **Country intro:** "It is the country tier of the Carbon Intensity service: regions 15, 16 and 17" is replaced. NESO's text does not link the package to the API. gridflow's 2026-10-09 probe matched 2,167 of 2,169 values to regions 15, 16 and 17, and the note calls that the project's measurement, not a NESO statement. The clocks paragraph gains the probe date. The references line "the live counterpart for region ids 15–17" becomes "gridflow's 2026-10-09 probe matched this file to its region ids 15–17".
   - **Regional intro:** "the bulk-file view of the same regional model behind the Carbon Intensity API's `/regional` endpoints" is replaced. The methodology PDF (May 2024) describes the API's regional forecasts. No values have been compared, because the API silver starts after this file's populated targets end.
   - **Regional crosswalk intro:** it now says the mapping matches names only (K-CI-FACTS §3.2 and the 2026-10-09 probe), no values were compared, and the PDF's API covers 17 regions against this file's 14 columns. This also covers the checker's nit 7.

## Not changed

Two nits were optional or taste: nit 8 ("Dates select nothing") and nit 9 (the `market` landscape). The balancing actions registry question is still a seat item (Defects in `held-author.md`). Round 1's report gave the country count as "9"; this report supersedes it with "nine by label, eight by period end".
