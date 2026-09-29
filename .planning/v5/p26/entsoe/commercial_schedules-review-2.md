# entsoe/commercial_schedules: checker re-review (Revision 1)

Checker: Opus 5.5 · high, 2026-09-29. Inputs:
- the canonical note, diffed again against `origin/master` (the mirror matches it byte for byte);
- the page, rebuilt with `--only`;
- the artefacts, checked by digest;
- the ENTSO-E code list PDF, which I opened and extracted myself in round 1 (`pdftotext`, section 3.8).

## Verdict: APPROVE

All seven round-1 findings are fixed. The revision broke nothing, and I found nothing new above a nit.

## Round-1 findings

1. **Blocker, `page.facts.grain`: fixed.** It now reads "One row per interval start, `in_Domain` zone, `out_Domain` zone and `businessType` (only `A06` here)". That is four columns, matching the dedup at `h6_market.py:91-98` and the Key line. It is 14 words, within budget, and "here" scopes the observed value.
2. **Major, `page.chart_view.key[belgium].note`: fixed.** It now reads "Moves with Elexon's INTNEM imports (project check), not hour for hour; …". No correlation figure appears on the page. The France note is unchanged, which I allowed.
3. **Nit, day-ahead loss: fixed.** `what_it_is` now ends "keeps `A05`, listed last (project check), so the day-ahead series is lost."
4. **Nit, `A05` citation: fixed and accurate.**
   - The page says "(total, in ENTSO-E's code list)" and no longer mentions entsoe-py.
   - The body cites "ENTSO-E Code Lists v29r0, section 3.8 `ContractTypeList`". It quotes `A05` "Total", "the sum of all capacity contract types for the period covered", and `A01` "Daily".
   - This matches the PDF: the definition reads in full "This is the sum of all capacity contract types for the period covered." The body quotes it without the leading "This is", inside quotation marks. The URL is the one I fetched.
   - The body scopes the source as the generic EDI list, not the A09 guide.
   - It adds "on FR to DE-LU `A05` is sometimes lower". I reproduced this from bronze with the contract type kept: 442 of 1,824 FR to DE-LU points have `A05` below `A01`, by up to 2,368.5 MW. FR to BE has 3 such points; the other five pairs have none.
5. **Nit, `page.record.fields.quantity_mw`: fixed.** It now reads "MW of the last-listed series, `A05` here; A03 points repeat until the next".
6. **Nit, `page.chart_view.alt`: fixed.** It now reads "Belgium moves between zero and 1,055 MW, and reaches 660 MW at most on the 17th." The other alt edit, "dipping below 210 MW daily", is still true: the daily minima are 205, 173, 153, 153, 153, 25 and 0.
7. **Nit, body correlation construction: fixed.** It now says "against the positive part of the summed Elexon flows, hourly". That construction reproduces 0.853 to 0.940.

## Regression checks

- **Only the edited fields changed.** Nothing else in the `page:` block or the body changed from round 1, and no chart, select or notebook field was touched.
- **Artefacts are unchanged.** The digests equal round 1:
  - series `spec_sha256` `ea4854c1…`;
  - sample `select_sha256` `749c05f1…`;
  - notebook `cells_sha256` `685233fa…`.
  - The build's digest check passes.
- **Build and detector.**
  - `gridflow-build --only entsoe/commercial_schedules` exits 0.
  - `detect.mjs` returns only the accepted `em-dash-overuse` advisory from EIC padding.
- **Rendered text.** It has no em dashes, arrows, middle dots, "locally" or "entsoe-py". The new phrases each render once.
- **Screenshots.**
  - I used static server port 9819 at 1440, 1024, 768 and 390, folded, and at 390 unfolded.
  - The first 1440 and 1024 captures read short (the known first-navigation timing issue), so I retook them.
  - The longer grain line wraps cleanly in the facts table at every width.
  - The Belgium key note and `what_it_is` wrap without clipping or overlap, and the hero turbines and corner labels are intact.
  - The server is stopped, with no listeners on 9819 or 10819.

## Nit (no action needed)

- The grain names the vendor tag `businessType`, while the Key lists the silver column `business_type`. This follows the page's existing `in_Domain`/`in_area_code` convention, so leave it.
