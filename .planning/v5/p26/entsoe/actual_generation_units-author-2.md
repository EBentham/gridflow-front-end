# entsoe/actual_generation_units: author response to review 1

Writer: Opus 5.5, 2026-09-29. Addresses `actual_generation_units-review.md` (REVISE, 2 blockers, 3 nits). Seat ruling: the page ships with the plant-not-unit defect stated, but every value shown or recommended must be honest.

## Fixes

### 1. Blocker, `page.record` (caption, select, fields)

I replaced the eight pumped-storage rows with eight clean rows: Dutch plants that send exactly one nested generation unit and no consumption series.
- Filter: `timestamp_utc` = 2026-09-18T18:00:00Z and `unit_mrid` in the eight EICs below, ordered by `production_type`, `unit_mrid`.

| Plant EIC | Unit | Type | MW |
|---|---|---|---|
| `49W000000000048S` | Elsta 1 | B04 | 46.0 |
| `49W0000000000512` | Unit 10 | B04 | 435.74675 |
| `49W000000000069K` | Claus C | B04 | 388.98 |
| `49W000000000074R` | FLEVO 5 | B04 | 475.71725 |
| `49W000000000094L` | Pergen 2 | B04 | 108.6885 |
| `49W000000000078J` | NLROTTETH__1 | B05 | 0.0 |
| `49W000000000102B` | Maasvlakte 3 | B05 | 1038.75 |
| `49W000000000054X` | Borssele 30 | B14 | 470.65525 |

- Evidence: `scratchpad/agu_r2a.py`. Every row is in the clean class of the reproduction (one generation series for the plant at that instant). Each plant has one nested unit and zero `outBiddingZone` series across all 19 bronze days, so each row equals the unit's output.
- `record.caption`: "Eight Dutch plants that send one generation unit each, 18:00 UTC on 18 September 2026."
- `fields.generation_mw`: "MW (`MAW`): the plant's one series here; elsewhere may be another unit's or consumption".
- `fields.production_type`: "ENTSO-E production type (PSR) code: B04 gas, B05 hard coal, B14 nuclear", replacing the B10 line.
- `fields.resolution`: "Step as sent (`PT60M` here, `PT15M` in FR); each point holds until the next".
- The defect examples (Grand Maison, Cheylas) stay in the note body's Known issues. The page states the mechanism in `what_it_is`, `grain` and the guide.

### 2. Blocker, `page.how_used`

Both uses are now scoped to the charted plants. Their cleanliness was verified by the checker and by me: one nested unit, no consumption series, all rows clean.
- "Hourly dispatch of the charted Dutch plants, nuclear baseload against coal and gas."
- "Load factors for the charted plants, against `installed_capacity_units` on the same EIC."

No French or general "single-unit" advice remains.

### 3. Nit, `page.summary`

"individual power plants" is now "individual generating units", which matches A73 and `what_it_is`.

### 4. Nit, `page.related[1].note`

It now reads "Names the plant EICs, which this table leaves empty".

### 5. Nit, vault body, Point-in-time field

It now reads "within seconds of gridflow's request (across the 60 data files in bronze 2026-08/09, 11.7 s before to 0.2 s after bronze `fetched_at`; ...)". I reproduced the checker's bound myself: min -11.669 s, max +0.198 s over 60 files.

## Unchanged

The chart, its series and the notebook cells are unchanged. The notebook `.head()` shows BE zeros; the checker accepted them as honest, since the multi-unit plants there are all-zero.

## Gates

- The canonical note was edited with the Edit tool and is still LF, like HEAD. The mirror is byte-identical (`cmp`).
- `gridflow-sample` was regenerated (new `select_sha256`). The series and notebook needed no regeneration because their specs and cells did not change.
- `gridflow-build --only entsoe/actual_generation_units` passes.
- `detect.mjs --json` at its absolute path shows only the accepted `em-dash-overuse` advisory (EIC padding). The page has 0 real em dashes.
- Screenshots after the fix, at 1440 and 390 (390 through the iframe), in `scratchpad/agu-shots2/`. The frame and guide are clean, with `unit_mrid` and `generation_mw` in view at 390. I made one last text-only edit to `fields.resolution` after the shots, then rebuilt and ran the detector. The port 9825 server is stopped.

Summary: both blockers are fixed (eight clean Dutch single-unit rows, uses scoped to the charted plants), the three nits are fixed, and the build and detector are green.
