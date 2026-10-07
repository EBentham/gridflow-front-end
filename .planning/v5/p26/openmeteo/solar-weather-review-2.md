# openmeteo/solar-weather: re-check

Checker: Sonnet 5.5 · high, 2026-10-06. Re-check of `solar-weather-review.md` against `solar-weather-author-2.md`.

## Verdict: APPROVE

No findings above nit, and no new nits. The blocker, the major and all seven nits are resolved. Nothing regressed.

## 1. Blocker and major

**Blocker (forecast loss stated): resolved.**

- `page.what_it_is` now says: "`forecast_solar` reads the forecast host for any dates gridflow sends; every stored row
  was fetched days after its hour, so they are after-the-fact values, not forecasts. No model run is kept." It is in
  the first block under the hero, in plain English, and says both halves of the loss (after the hour, no run kept).
- `page.family.members[forecast_solar].differs` now says: "Forecast host, own grid cells; no run time; every row
  fetched after its hour" (14 words). It shows above the forecast request in the raw feed at 1440 and 390.
- Reproduced from silver (2,160 rows, six sites, 1 to 5 Aug and 13 to 22 Sep): `available_at - timestamp_utc` runs
  from 90.73 h to 373.49 h, and 0 rows are at or before their hour. "Days after its hour" holds from 3.8 days up, as the
  writer says. The page gives no figure, so none can be wrong.
- This is the one local-data statement on the page, sanctioned by the seat's ship condition. The grep of the rendered
  page for `locally`, `held`, `our `, `since 20`, `yet`, `soon`, `planned`, `coming`, `until`, `live`, `now`,
  `real-time` returns 0 for each.

**Major (uses silver cannot deliver): resolved.**

- `how_used[2]` is now "The forecast member's request and columns, a template for capturing real forecasts." It claims
  no forecast use of the stored rows.
- `summary` now reads "archive history, plus forecast-host values fetched after the hour."
- `facts.history` now reads "the Forecast API serves up to 16 days ahead", which is the vendor fact (`forecast_days`
  0 to 16), attributed to the API and not to the stored table. With the loss stated directly under the hero, it no
  longer misleads.

## 2. The seven nits

| # | Nit | Status |
|---|---|---|
| 3 | Stale ERA5 and near-real-time text in the note bodies | Fixed. `historical_solar.md` H1 is now "(Open-Meteo archive, ...)"; "near-real-time" is gone (grep: 0); the vintage-policy lag row says the ERA5 premise is superseded by the IFS blend and the policy is unchanged pending research (Defect OMd). `forecast_solar.md` says no stored row has a positive lead time, marks the day-ahead and nowcast notes as describing what the host can serve when fetched ahead, and says `available_at` is "the time gridflow stored the response, an ingest-run stamp, not a model run time" (the wording I advised, not an unverified "write time"). |
| 4 | `facts.cadence` unexpanded IFS, ERA5-Land omitted | Fixed: "Hourly; archive ERA5 and ERA5-Land 5 days late, ECMWF IFS without delay". Matches the vendor table. |
| 5 | `related[1].note` wrong quantity | Fixed: "NESO's embedded solar output forecast, to compare with irradiance" (9 words). |
| 6 | Alt text "at zero each night" | Fixed: "at or near zero each night". Kent holds 1.0 W/m² at some 04:00 stamps. |
| 7 | Decoded commas in the URLs | Closed by the seat ruling (plain commas on all three Open-Meteo pages). The page has 0 `%2C`; the long `hourly=` list wraps after commas at 1440 and 390. Not a finding. |
| 8 | Frame caption "mostly diffuse light" | Fixed: "Cornwall, 07:00 to 14:00 UTC, 15 June 2026; under low cloud, diffuse exceeds direct from 08:00." True against the rows (direct 190 over diffuse 75 at 07:00 only; diffuse above direct from 08:00 to 14:00; low cloud 87 to 100%). |
| 9 | Hero has no solar scenery | Design question for the seat, as the coordinator said. Not a finding. |

## 3. Regression check

- `gridflow-build --only openmeteo/historical_solar` succeeds; `detect.mjs --json` (absolute path) returns `[]`.
- Both mirrors are byte-equal to the canonical notes (`cmp`).
- The chart spec, sample and notebook are unchanged and their digests still pass; the page has 0 em dashes, en dashes,
  arrows or middle dots.
- Screenshots re-taken at 1440 and a true 390 px iframe (light; the site has no dark theme): the revised
  `what_it_is`, the three uses, the chart, both raw-feed requests, the frame caption, the column guide, the notebook
  and the related list are fully visible, with nothing clipped or overlapping. Member headings no longer repeat the key
  in capitals. My server on port 9883 is stopped; port 9670 was not touched.
- Two small points that are not findings: `historical_solar.md` line 392 still opens the vintage-policy section with
  "ERA5 archive rows emit no vendor `published_at`" (true of the vendor response, harmless), and the note body keeps
  the "Day-ahead solar-PV modelling" bullet under the historical modelling notes, which describes backtesting use.
  Neither renders on the page.

## One-line summary

APPROVE: the forecast loss is stated plainly in `what_it_is` and the family line (90.7 to 373.5 h, none at or before the hour), no use line claims forecast use, all nits are fixed, and the build, detector and mirrors are clean.
