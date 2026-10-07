# openmeteo/solar-weather: author revision 2

Writer: Opus 5.5, 2026-10-06. This revision answers `solar-weather-review.md` (REVISE: 1 blocker, 1 major, 7 nits) and the seat's instruction.

## Status

- **Build:** `gridflow-build --only openmeteo/historical_solar` succeeds.
- **Detector:** `detect.mjs --json` (absolute path) returns `[]`. The page has 0 em dashes.
- **Mirrors:** `historical_solar.md` and `forecast_solar.md` are byte-equal to the canonical notes (`cmp`), and CRLF is kept.
- **Artefacts:** unchanged. The chart spec, the record select and the notebook cells are untouched, so the series, sample and notebook digests still pass.
- **Screenshots:** light, taken again at 1440, 1024, 768 and a true 390 iframe, in `scratchpad/shots-solar2/`. The encoded `%2C` URLs wrap inside their code blocks, and nothing is clipped. Server on 9863 started and stopped; 9670 was not touched.

## Fixes

| # | Review finding | Change |
|---|---|---|
| 1 | **Blocker:** the forecast loss is not stated | **`what_it_is` now reads:** "`forecast_solar` reads the forecast host for any dates gridflow sends; every stored row was fetched days after its hour, so they are after-the-fact values, not forecasts. No model run is kept." (59 words in total.)<br>**`family.members[forecast_solar].differs` now reads:** "Forecast host, own grid cells; no run time; every row fetched after its hour" (14 words).<br>**Reproduced:** `available_at - timestamp_utc` runs from 90.7 h to 373.5 h; 0 rows are at or before their hour. The page gives no figure, only "days after its hour", which holds from 3.8 days up. |
| 2 | **Major:** uses that silver cannot deliver | **`how_used[2]`:** "Forward irradiance for a day-ahead solar forecast…" became "The forecast member's request and columns, a template for capturing real forecasts."<br>**`summary`:** "as archive history and as forecasts" became "archive history, plus forecast-host values fetched after the hour".<br>**`facts.history`:** "forecasts up to 16 days ahead" became "the Forecast API serves up to 16 days ahead". |
| 3 | **Nit:** stale body text | **`historical_solar.md`:**<br>- H1 "(ERA5 archive, …)" became "(Open-Meteo archive, …)".<br>- "For near-real-time use [forecast_solar]" now points to the forecast counterpart and says its stored rows were all fetched after their hour.<br>- The vintage-policy lag row now says the ERA5 premise is the one this page stated until 2026-10-06, and is superseded because the archive blend includes ECMWF IFS (no delay). The policy itself is unchanged pending the research unit (Defect OMd).<br>**`forecast_solar.md`:**<br>- The "Forecast-skill backtests" note now says no stored row has a positive lead time.<br>- A status line says the day-ahead and nowcast notes describe what the host can serve when fetched ahead of time.<br>- `available_at` is now "the time gridflow stored the response, an ingest-run stamp, not a model run time", replacing "the bronze write time", as the review advised. |
| 4 | **Nit:** IFS not expanded; ERA5-Land omitted (`facts.cadence`) | "Hourly; archive ERA5 and ERA5-Land 5 days late, ECMWF IFS without delay" (12 words). |
| 5 | **Nit:** `related[1].note` quantity | "NESO's embedded solar output forecast, to compare with irradiance". |
| 6 | **Nit:** alt "at zero each night" | Now "at or near zero each night". Kent carries 1.0 W/m² at some 04:00 stamps. |
| 7 | **Nit:** decoded commas in the URLs | All three requests (`raw_feed.requests[0]` and both `family.members[].request`) now carry `%2C`, exactly as the bronze sidecars record them. Note: the demand-weather sibling still shows commas, so the seat may want one convention across the three pages. |
| 8 | **Nit:** frame caption | "Cornwall, 07:00 to 14:00 UTC, 15 June 2026; under low cloud, diffuse exceeds direct from 08:00." (16 words). Checked against the rows: diffuse is above direct from 08:00 to 14:00, and direct is higher only at 07:00. |
| 9 | **Nit:** no solar scenery in the hero | Not fixable by the author. `landscape` accepts only `power`, `market`, `gas` and `units`, and the drawing is the seat's. Left as a design question for the seat. |

## Notes for the re-check

- The member headings in the raw feed no longer repeat the key in capitals (`openmeteo/historical_solar HISTORICAL_SOLAR` in revision 1). That changed outside my files, so my template problem 2 is resolved.
- The statement about stored rows in `what_it_is` and `family.differs` is a deliberate local-data fact, sanctioned by the seat's ship condition. It is the only one on the page.
- Defects OMa to OMe in `solar-weather-author.md` are unchanged.
  - OMa now covers its scope from sidecars: `forecast_wind` has the same two after-the-hour fetches.
  - `forecast_demand` also has 2026-09-03 and 09-04 fetches that reach a few days ahead.

**Summary:** blocker, major and nits fixed. The page now says every stored `forecast_solar` row was fetched after its hour and claims no forecast use. Build clean, detector `[]`, mirrors byte-equal.

## Follow-up: URL convention (seat ruling)

The seat ruled for plain commas in the `hourly=` lists on all three Open-Meteo pages, so the request well can wrap after each comma. The `%2C` change from fix 7 is reverted: 33 replacements, all in the three request URLs of the `historical_solar.md` page block. The note bodies had no `%2C`.

- Both mirrors are byte-equal again (`cmp`), and CRLF is kept.
- `gridflow-build --only openmeteo/historical_solar` succeeds.
- `detect.mjs --json` returns `[]`.
- The page has 0 `%2C` and 0 em dashes.
