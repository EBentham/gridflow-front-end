# neso_data_portal/embedded_wind_solar_forecast: review 2

Checker: Sonnet 5.5 · high, 2026-10-06. Re-check of `embedded_wind_solar_forecast-review.md` against `embedded_wind_solar_forecast-author-2.md`. Port 9885 (server stopped; 9670 untouched).

## Verdict: APPROVE

Nothing above nit. The blocker and the major are fixed and verified; all six first-round nits are fixed or ruled; no regression. Four new nits, all optional wording.

## Verification

**Blocker (cadence): fixed.**
- `facts.cadence` now reads "NESO's catalogue says hourly updates, within day to 14 days ahead; one issue charted". It matches the package `notes` in `quant-vault/30-vendors/neso-data-portal/_generated/snapshots/20260820T214455Z/catalog-snapshot.json` ("from within day up to 14 days ahead ... updated on an hourly basis"), is attributed to NESO, and sits beside what the chart shows.
- Note body, Publication lag row: quotes the same `notes`, marks it a vendor statement not observed, and records the resource description's "daily resolution" contradiction. Accurate.
- "Unstated" appears nowhere on the built page; "TODO (not stated)" is gone from the cadence row (the one remaining `TODO` is the unrelated Modelling notes heading).

**"Jun - Dec" notice (seat ruling): wording accurate, plain, not speculative.**
- `what_it_is`: "gridflow reads the resource "Embedded Solar and Wind Forecast" ... NESO's catalogue says the data moved to a new forecast system and recommends its "Jun - Dec" 2026 archive resource." The source sentence is "NESO have moved the data source to its new forecast system. We recommend that customers now use the 'Jun - Dec' dataset." The page makes no claim about which resource is stale or live. Resource name is `endpoints.py:118` and the sidecar `resource_name`.
- Note body Known issues bullet quotes the notice verbatim, names the archive resource in full, cites `endpoints.py:118`, gives the 21:25:03 last-modified, and says the live-forecast question is open. Accurate.
- Only nit: nit 1 below.

**Docstring wording: none remains.** Built-page grep for `day-ahead`, `several times`: no hits except the `entsoe/wind_solar_forecast` related note ("Day-ahead ... forecasts for other zones; none for GB"), which describes ENTSO-E's own process (confirmed against `vault/entsoe/wind_solar_forecast.md`: GB answers with an acknowledgement and no data). No `day-ahead` or `several times` in the canonical note body either.

**Silver path (major): fixed.** The note now says the run stamp is the bronze sidecar `written_at` via `_timestamp_from_sidecar`, not the `available_at` column (= `published_at`), and cites the real file `..._20260820_run2026-08-20T21-43-41.158795-00-00.parquet`. Checked in code: `_SIDECAR_TIMESTAMP_KEYS` (`silver/base.py:102-107`, `available_at, written_at, ...`; this sidecar has no `available_at` key), the call at `base.py:1019`, `_write_silver(..., available_at=available_at)` at 1067, and the `":"` and `"+"` to `"-"` replacement in `_write_silver`. Citations are right.

**First-round nits:**
- 2 `how_used[2]`: reworded; supported (nit 3 below).
- 4 `chart_view.alt`: "Periods starting 21:00 to 02:30 UTC stay at or near zero (63 at most, at 23:30 UTC on the 25th)". Recomputed on silver: maximum over period starts with hour >= 21 or <= 2 is 63.0 at 2026-08-25 23:30 UTC. Correct and the window is named.
- 5 caption and alt: "stamped 21:25, read as UTC" / "stamped 21:25 (read as UTC)". Done.
- 6 grain: no edit, my option; the defect stays logged. Accepted.
- 7 bronze sample note: "on this capture, `TIME_GMT` is half an hour after each period's start, UTC". Done.
- 8 notice: recorded on the page and in the body. Done.

**No regression:**
- `gridflow-build --only neso_data_portal/embedded_wind_solar_forecast`: success. `detect.mjs --json`: `[]`. Em dashes, arrows, middle dots: 0. No `locally|held|since 20|yet|soon|planned|coming|live|real-time`.
- `cmp` canonical note against the mirror: byte-equal. Chart spec, sample and notebook cells unchanged in the note diff (series, samples and notebook artefacts were not touched; the digest check passes in the build).
- Screenshots looked at: 1440 (hero, topsoil, chart, start of raw feed) and a true 390 px iframe (hero, topsoil, how it's used). The hero key chip wraps at 390 (the seat's template fix is in), and nothing is clipped or overlapping; the longer cadence line wraps cleanly in the fact list.

## New nits (all optional)

1. **`page.what_it_is`:** "recommends its "Jun - Dec" 2026 archive resource". NESO's words are "the 'Jun - Dec' dataset"; matching it to the resource `Embedded Solar and Wind Forecast Archive 2026 (Jun - Dec)` is reasonable (it is the only resource with that label in the snapshot) but is the writer's mapping, and "its" is ambiguous. Either "recommends its "Jun - Dec" dataset" or leave as is.
2. **`page.facts.cadence`:** "within day to 14 days ahead" is clipped from NESO's "from within day up to 14 days ahead". Plainer: "from within the day to 14 days ahead".
3. **`page.how_used[2]`:** "from the base view" names a thing the page never shows (the notebook reads `_latest`). A reader cannot act on it. Plainer: "from the table that keeps every issue" or similar; fine to leave.
4. **`page.record.fields` units:** the forecast lines say "MW in gridflow's code" but the capacity lines say "MW" flat, and the sentence that NESO states no unit was dropped from `what_it_is` to fit the budget. Code does name all four columns `_MW_COLUMNS`, so the figure is allowed; adding "in gridflow's code" to the two capacity lines would make the four lines consistent.

Summary: APPROVE; the cadence blocker and the silver-path major are fixed and verified against the catalogue snapshot and `silver/base.py`, the "Jun - Dec" notice is accurately and plainly worded, build and detector are clean, the mirror is byte-equal, the 390 hero wraps with nothing clipped, and four optional wording nits remain.
