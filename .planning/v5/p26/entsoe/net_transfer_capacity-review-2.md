# entsoe/net_transfer_capacity: checker re-review (after Revision 1)

Checker: Opus 5.5 · high, 2026-09-29. This re-checks the six findings in `net_transfer_capacity-review.md` against the revised canonical note, the mirror and the rebuilt page, and looks for anything the revision broke.

## Verdict: APPROVE

There are no findings above nit. One nit carries over for the seat (item 6).

## Findings from review 1, re-checked

1. **Blocker, `page.related[3].note`: resolved.**
   - It now reads "Prices at the continental and Irish ends; none for GB" (10 words).
   - This is true for the six silver pairs:
     - `day_ahead_prices` holds IE-SEM, DE-LU, BE, FR and NL, and no GB;
     - GB returns Reason 999 (`day_ahead_prices.md:177`).
   - The rendered page shows it in the related list at 1440 and 390.
2. **Major, body `## Modelling notes`: resolved.** Every figure matches my reproduction from review 1:
   - 1.04 × NTC is now scoped to "hours with NTC above zero", with the GB-BE exception at 1.11 (889 against 804);
   - GB from NL has 286 hours at NTC 0, with flow positive in 259, "mostly about 0.06 MW", plus 86.5 MW at 13:00 and 374 MW at 19:00 UTC on 2026-09-19;
   - NL-DE-LU has 141 of 432 hours above NTC, by up to 2,560 MW;
   - utilisation is now "undefined at NTC 0".
3. **Nit, body `### Cross-zonal parameters`: resolved.**
   - The direction check now names GB-FR, GB-BE and GB-NL. It says GB-IE-SEM "neither confirms nor contradicts" (flow up to 153 MW against NTC of 400 to 1,413).
   - It gives the 19 days as 2026-08-01 to 08-05 and 2026-09-08 to 09-21.
   - The count is 42 of 42, with 13 and 14 September fetched twice. This matches the bronze tally: 21 ACK files for each FR pair.
4. **Nit, `page.what_it_is`: resolved.** The line now reads 'FR to BE and FR to DE-LU returned "No matching data found" in the responses received'. It is scoped like `facts.cadence`, quotes the vendor's text, and carries no count.
5. **Nit, the writer's report: resolved.** It now says 42 of 42 (Revision 1, item 5).
6. **Nit, dead domain link: carried to the seat.**
   - `../../../20-domain/markets/net-transfer-capacity.md` is still missing from `20-domain/markets/`.
   - It is not on the page, and the report leaves it for the seat, as review 1 suggested.

## Regression checks

- **Page block.** `what_it_is` and `related[3]` are the only page-block changes. The chart spec, key, alt text, record, fields and notebook are unchanged.
- **Artefacts.** The series, samples and notebook JSON are untouched (19:31 and 19:33 timestamps), and the build's digest check passes.
- **Line endings and mirror.**
  - The canonical note is still CRLF (325 CR, 325 LF).
  - The diff against `origin/master` is 140+/8-, not a whole-file rewrite.
  - The mirror `vault/entsoe/net_transfer_capacity.md` is byte-identical (`cmp`).
- **Build.** `gridflow-build --only entsoe/net_transfer_capacity` passes: "rendered only ['entsoe/net_transfer_capacity']".
- **Detector.** `detect.mjs --json` returns only the accepted `em-dash-overuse` advisory ("142 em-dashes", EIC padding and `--` flags).
- **Text checks.** The rendered page has 0 em dashes, en dashes, arrows or middle dots. The local-data grep hits only template strings (the frame's aria-label "8 rows") and "hour by hour".
- **Layout.**
  - CDP shots use a static server on 9823, since stopped, with Chrome under `timeout 60`.
  - At 1440, 1024 and 768, folded and unfolded, `scrollWidth` equals `innerWidth` and nothing sits outside the viewport.
  - A 390 px same-origin iframe gives `scrollWidth` 390.
  - I looked at the longer "What it is" block at 390 and 1024 and at the related list at 390. Nothing is clipped or overlapping.
- **Unchanged template notes from review 1.** These are not findings:
  - the lazy-loaded notebook plot is blank in full-page captures but renders in view;
  - there is no dark theme;
  - the `.df-wrap` scroller at 390 has no `tabindex`;
  - the `contract_MarketAgreement.Type=A01` wrap at 390;
  - the notebook tab label clip.
