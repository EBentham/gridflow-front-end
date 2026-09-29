# entsoe/actual_generation_units: checker re-review

Checker: Opus 5.5, 2026-09-29. Re-checks `actual_generation_units-review.md` against
`actual_generation_units-author-2.md`. Scripts: `scratchpad/agu-review/r10.py`. Shots:
`scratchpad/agu-review/shots2/`. My own port was 9848, now stopped; I did not touch port 9670.

## Verdict: APPROVE

0 blockers, 0 majors, 0 nits. Both blockers and all three nits are fixed, and nothing regressed.

## Blockers

### 1. Sample rows: fixed

- **Selection.** `record.select` now keeps `timestamp_utc` = 2026-09-18T18:00:00Z and eight NL
  plant EICs, ordered by `production_type`, `unit_mrid`. The caption reads "Eight Dutch plants that
  send one generation unit each, 18:00 UTC on 18 September 2026."
- **Reproduction** (`r10.py`, on my own bronze parse with the nested unit and side attached).
  - Every one of the eight plants is in `10YNL----------L`, sends exactly one nested unit and sends
    0 `outBiddingZone` series across all 19 bronze days.
  - All 3,542 of their silver rows are in the clean class.
  - At 18:00 each has one series, and its value equals silver and the regenerated sample
    (`generated_by: gridflow-sample`, new `select_sha256`):

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

  All eight are PT60M. The 0.0 is a real series value, not a defect.
- **Guide lines.** All three revised lines are correct:
  - `generation_mw`: "the plant's one series here; elsewhere may be another unit's or consumption".
  - `production_type`: B04 gas, B05 hard coal, B14 nuclear (the ENTSO-E PSR codes).
  - `resolution`: "`PT60M` here, `PT15M` in FR; each point holds until the next" (A03, `parsers.py:578-601`).
- **No wrong value is shown as correct.** The page has no pumped-storage, B10 or Grand Maison rows
  left.

### 2. `how_used`: fixed

Both uses are now scoped to the charted plants:
- "Hourly dispatch of the charted Dutch plants, nuclear baseload against coal and gas."
- "Load factors for the charted plants, against `installed_capacity_units` on the same EIC."

Review 1 showed those three plants are clean on all 19 days. `installed_capacity_units` silver holds
all three EICs: Claus 1,304 MW, Maasvlakte 1,070 MW, Borssele 30 485 MW. The page no longer contains
the phrase "single-unit".

## Nits: all fixed

- `page.summary` now reads "individual generating units".
- `page.related[1].note` now reads "Names the plant EICs, which this table leaves empty".
- The vault body's Point-in-time line now reads "within seconds", with the 11.7 s before to 0.2 s
  after bound over 60 files. That matches my review-1 measurement.

## Regression checks

- The mirror is byte-identical to the canonical note (`cmp`).
- `gridflow-build --only entsoe/actual_generation_units` passes.
- `detect.mjs --json` at its absolute path shows only the accepted `em-dash-overuse` advisory (EIC
  padding).
- The page text has 0 em dashes, 0 arrows, 0 middle dots, and no "locally", "held", "our" or
  "since 20".
- The chart spec, series and notebook are unchanged from review 1, where they matched silver.
- Screenshots at 1440 and 390 (390 through the iframe): the frame, caption and guide are fully
  visible, and `unit_mrid` and `generation_mw` stay in view at 390.

Summary: APPROVE. The eight sample rows are verified-clean Dutch single-unit plants, the uses are
scoped to the charted plants, the three nits are fixed, and the build and detector are green.
