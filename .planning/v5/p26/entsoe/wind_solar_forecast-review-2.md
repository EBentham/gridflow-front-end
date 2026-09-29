# entsoe/wind_solar_forecast: review 2 (re-check of Revision 1)

Reviewer: Opus 5.5 · high, checker. I re-checked the four findings of `wind_solar_forecast-review.md` against the revised vault note (diffed against quant-vault `origin/master`), the mirror, the rebuilt page and fresh screenshots.

## Verdict: APPROVE

0 blockers, 0 majors, 1 optional nit. All four findings are fixed, and the revision broke nothing.

## Prior findings

1. **major (body gotcha and silver sample): fixed.**
   - The gotcha now reads "A69 carries B16 (solar), B18 (wind offshore) and B19 (wind onshore); the September 2026 responses for DE-LU, FR, NL and BE each carry all three". The B17 clause and "only B19" are gone. This matches silver (`group_by(area_code, production_type)` over 14 to 20 Sep) and bronze.
   - The silver sample is now two real rows, and every value matches silver and the committed sample JSON:
     - DE-LU B16, 0.0 at 2026-09-14 22:00;
     - DE-LU B19, 3458.69357 at the same time;
     - `resolution` "PT15M" and `published_at` 2026-09-21 10:07:59 on both.
2. **nit (`published_at` "within a second"): fixed.** It now reads "within seconds of the sidecar `fetched_at`", consistent with ruling #39 and the measured gaps of up to about 2 s.
3. **nit (A03 fill): fixed.**
   - `raw_feed.note` now says "`gridflow transform` fills the vendor's A03 blocks, keeping one value per target time, zone and code within that day". This is true: `read_bronze` calls the parser inside transform, and the fill is at `parsers.py:533-600`.
   - A new body gotcha states the same with the code cite, which is correct.
4. **nit (cadence as a rule): fixed.**
   - `facts.cadence` now reads "Day-ahead; interval from the response's `resolution`, PT15M or PT60M in these responses".
   - The body gotcha now says, scoped to 14 to 20 Sep: DE-LU, FR and NL send PT15M; BE and IE-SEM send PT60M. Silver agrees.

## New finding

1. **nit (optional)**: note body, `## Known issues and gotchas`, the resolution bullet, "ENTSO-E states no rule".
   - This is a negative claim about the vendor docs with no source quoted. "The note quotes no vendor rule" would say only what is known.
   - It is body text, not a page field, and it does not block.

## Regression checks

- **Mirror:** `vault/entsoe/wind_solar_forecast.md` is byte-identical to the vault note, with CRLF on all 285 lines. The front matter has no literal `---` (ruling #40).
- **Unchanged parts:** the chart spec, `chart_view`, `record` and notebook are the same as in review 1.
- **Build:** `gridflow-build --only entsoe/wind_solar_forecast` passes, including the budgets and artefact digests.
- **Detector:** `detect.mjs --json` returns only the accepted em-dash advisory (30, from EIC padding and CLI flags). The page text has no em dash, "→" or middle dot.
- **Screenshots:** the changed hero cadence fact and raw-feed note at 1440, 768 and 390 (390 in an iframe). Nothing is clipped or overlapping.
  - At 1440, direct headless shots stopped painting below about 1,550 px, the same flake the writer reported. A 1440 iframe wrapper rendered the raw-feed section fully.
