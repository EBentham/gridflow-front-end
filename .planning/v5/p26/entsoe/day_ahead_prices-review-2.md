# entsoe/day_ahead_prices: checker re-review (Revision 1)

Checker: Opus 5.5 (high), 2026-09-29. This re-checks the four findings in `day_ahead_prices-review.md` against the revised
vault note (diffed against quant-vault `origin/master`). It also checks that the rebuilt page has not broken anything.

## Verdict: REVISE

Three of the four fixes are right. The cadence fix introduces a new wrong detail.

## Findings

### 1. major: `page.facts.cadence`

- **What is wrong.** The new text reads "Daily; afternoon replies here already held the next delivery day". No bronze
  reply was fetched in the afternoon.
  - The replies that held a delivery day that had not yet begun were all fetched at 19:53 UTC on 15 Sep, which is
    21:53 CEST, in the evening. There are five of them, for FR, NL, BE, DE-LU and IE-SEM, each holding delivery day 16.
  - The only other such reply is DE-LU at 09:58 UTC on 21 Sep. It held part of day 22, from sequences `[2,1,2]`, while
    FR, NL, BE and IE-SEM fetched at the same time did not.
- **Evidence.**
  - Every `bronze/entsoe/day_ahead_prices/2026/*/*/raw_*.meta.json` was scanned, comparing `fetched_at` with the
    `<end>` of each period, minus 24 hours.
  - Fetch hours across all bronze are 23, 00, 03, 19, 09 and 10 UTC, so there are no afternoon captures at all.
- **Fix.** Drop or correct the time of day. For example: "Daily; replies fetched the evening before already held the
  next delivery day". Alternatively: "Daily; a reply already held the next delivery day before it began".
- **Severity.** Major rather than blocker. The substance is true: the next delivery day was available before it began.
  Only the qualifier "afternoon" is wrong.

## Fixes confirmed

1. **Rate limit (was major).** The note body now reads "codebase configured at 1 req/s (`config/sources.yaml:192`)".
   That matches `origin/master` `config/sources.yaml:192`, `rate_limit_per_second: 1`. Resolved.
2. **Cadence (was major).** It is now scoped to the responses, but see finding 1 above.
3. **"lists last" (was nit).**
   - `what_it_is` now reads "whichever the latest reply lists last".
   - The body bullet adds the latest reply and the name-order concatenation in `read_bronze` (`:36`).
   - Both are correct against my earlier re-simulation: 96 of 96 match on 14 to 16 Sep. Resolved.
4. **A03 scoping (was nit).** `record.fields.price_eur_mwh` now reads "omitted points repeat the previous one (curve
   type A03)". Resolved.
5. **Point-time rule (seat note).** `record.fields.timestamp_utc` now reads "`start + (position - 1) × resolution`".
   That matches `parsers.py:530` (`start_dt + (position - 1) * resolution`). Correct.

## Regression checks

- **Mirror.** `vault/entsoe/day_ahead_prices.md` is byte-identical to the canonical note (`cmp` clean), and CRLF is
  kept.
- **Unchanged sections.** Nothing else in the `page:` block changed: chart spec, chart view, raw feed, record select,
  notebook and related.
- **Artefacts.** Series, sample and notebook are unchanged, with timestamps from 19:06 to 19:11.
- **Build.** `gridflow-build --only entsoe/day_ahead_prices` succeeds, so the artefact digests still match.
- **Detector.** `detect.mjs` returns only the accepted em-dash advisory.
- **Rendered text.**
  - The new guide lines and `what_it_is` render as written.
  - No dashes, arrows or middle dots are added.
  - "×" is not on the banned list.
- **Layout.** At 390 (Browser pane) the page's scroll width is 390. The hero facts and the column guide wrap without
  clipping.
