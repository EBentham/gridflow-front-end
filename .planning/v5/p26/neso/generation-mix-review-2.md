# Re-check: `neso/generation-mix`

Checker: Sonnet 5.5 (high), 2026-10-06. Answers `generation-mix-author-2.md` against `generation-mix-review.md`.
Screenshot port 9891 (static server, stopped afterwards; 9670 untouched).

## Verdict: APPROVE

Both majors are fixed and the fixes reproduce. Nits 3 to 8, 10 and 11 are resolved; nit 9 is left alone as the seat ruled.
Two new nits below, neither above nit. Nothing regressed.

## Regression checks

- `gridflow-build --only neso/generation` succeeds; `detect.mjs --json` (absolute path) on `generation-mix.html` returns `[]`.
- `cmp` of the three canonical notes against `vault/neso/{generation,generation_current,generation_pt24h}.md`: all byte-equal.
  Member notes unchanged since the first review.
- Series, sample and notebook files carry the same times as in the first review (20:13 to 20:17); the chart spec and `record.select`
  are untouched, and the build's digest checks pass.
- Em dashes, arrows, middle dots, en dashes on the page: 0. Literal backticks printing: 0 (the `needs` line now reads "with generation
  for 14 to 20 September 2026 ingested").
- Screenshots (headless Chrome, `timeout 60`) at 1440 and a true 390 px iframe: the longer key notes, the new solar note, the
  `what_it_is` paragraph and the caption wrap cleanly; nothing clipped or overlapping.

## The two majors

1. **Offset scope (was major): fixed.** The offset now appears only as "Gas, wind, imports and biomass track metered data 30 minutes
   later (checked); solar's timing is not placed" (`what_it_is`), "gas, wind, imports and biomass track fuelhh 30 minutes later
   (a project check)" (caption), the same fuels in the `timestamp_utc` guide line and the fuelhh related note (11 words). The `solar`
   key note reads "Timing not placed: fits the Data Portal's solar at zero lag, not 30 minutes later (checked)". Reproduced:
   level MAE against portal `solar_pct` 1.01 at zero lag, 1.51 at +30 and 1.50 at -30; differenced correlation 0.94 at zero against
   0.91 at +/-30. I also tested the one scoped fuel I had not run against fuelhh: the mix's `imports` against fuelhh's summed
   per-link imports, differenced correlation 0.01/0.39/0.09/**0.91**/0.09 at -60/-30/0/+30/+60 minutes. The vault body offset bullet
   now carries these numbers, says the portal's `solar` is unanchored, and says not to shift `solar` with the metered fuels.
2. **`imports` (was major): fixed.** Key note: "Not net of exports, but about 1.9 points below the Data Portal's per-link total on
   average (checked)". The over-read clause is gone. Reproduced at the +30 alignment, 674 half-hours: mean -1.86 points, MAE 1.88,
   p95 4.40 against portal `imports_pct`; portal `imports` equals fuelhh's summed per-link imports (MAE 9.9 MW); regression
   coefficient on exports -0.065. The body bullet adds the 42-of-213 zero half-hours with per-link imports of 2 to 1,250 MW, as
   measured. The note now agrees with the approved portal page ("each link's imports summed").

## The nits

- **3** `raw_feed.note`: now "A request for 14 to 21 September returns rows stamped 13 September 23:30 to 20 September 23:30 UTC
  (checked)". Consistent with the bronze I checked (request `13T00:00Z/22T00:00Z` returned `from` 12 Sep 23:30 to 21 Sep 23:30).
  Resolved. (The "(checked)" is on the analogous held window, not on that exact call; see new nit B.)
- **4** "match" is now "track" everywhere; the placed fuels are named. Resolved.
- **5** `how_used[1]`: "A solar share, and a wind share including embedded wind, which fuelhh lacks." Resolved.
- **6** `needs` backticks gone. Resolved.
- **7** "undocumented" became "No NESO source cited here defines the total" (see new nit A). The `other` key note now reads "tracks the
  Data Portal's other, which NESO says holds batteries and transmission solar (checked)"; the portal page says exactly that, and
  the fit reproduces (MAE 0.43 points, mean +0.33; differenced correlation 0.78 at +30 against 0.08 at zero). Resolved.
- **8** `record.caption`: "all fuels but `other`". Resolved.
- **9** No edit, as the seat rules. Resolved.
- **10** Schema-table line now points to Known issues. Resolved.
- **11** `x_label` is "UTC day, as NESO stamps it". Resolved.

## New nits (do not block)

- **A. `page.what_it_is` and `page.record.fields.generation_percentage`: "No NESO source cited here defines the total".** The page
  cites no sources, so "cited here" points at nothing the reader can see. "NESO's published material we draw on does not define
  the total" or simply "NESO does not say what the total is" (the latter is a stronger claim than the writer can back without
  reading the live docs) would read better. Optional.
- **B. `page.raw_feed.note`: "(checked)" on a window that was not run.** The checked calls are 13 to 22 September and 1 to 6 August;
  14 to 21 September follows the same rule but was not itself requested. Optional: "a request for 13 to 22 September returned rows
  stamped 12 September 23:30 to 21 September 23:30 (checked)", which is the held call.

## Defects

The two additions from the first review stand as written, and the writer's wording of them in `generation-mix-author-2.md` is accurate.
