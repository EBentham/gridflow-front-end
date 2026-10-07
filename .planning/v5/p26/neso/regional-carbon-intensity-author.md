# neso/regional-carbon-intensity: author report

Writer: Opus 5.5 (high), 2026-10-06. Family lead `regional_intensity`; 18 members as fixed in `site/hifi/data/neso.json`.

## Status

- **Build:** `gridflow-build --only neso/regional_intensity` succeeds in the shared worktree. That is after the seat raised `FAMILY_MEMBERS` to `(2, 18)`. Before the change, the only error was `regional_intensity: page.family.members: 18 entries; needs 2 to 12`; every other field was inside its budget.
- **Detector:** `detect.mjs --json` returns `[]`. The page has 0 em dashes.
- **Screenshots:** taken at 1440, 1024, 768 and 390. The 390 shot is a true 390 px iframe. Files are in `scratchpad/rci/shots/`.
  - Nothing is clipped or overlapping. The 18 member chips wrap cleanly at every width, long URLs wrap inside their boxes at 390, and the frame folds behind `…` as designed.
  - The site has no dark theme: no `prefers-color-scheme` or `data-theme` anywhere in `theme.css`, `tokens.css` or `site.js`. Light is the only mode.
  - The shots were first taken from a scratch copy with the cap raised, before the seat's change. The seat's official build is byte-identical to that copy (`cmp` passes), so the shots show the real page.
- **Chart:** a line chart of `forecast_gco2_kwh` in gCO2/kWh, from 14 to 20 September 2026, for South Wales (7), London (13), GB (18) and North Scotland (1). It has 4 series of 336 points. Rows are de-duplicated on `[timestamp_utc, regionid]` because the forecast repeats on all nine fuel rows.
- **Recommendation:** ship.

## Artefacts (front-end worktree)

- `site/hifi/data/series/neso/regional_intensity.json`: `spec_origin: vault`; 1,344 rows used.
- `site/hifi/data/samples/neso/regional_intensity.json`: from `gridflow-sample`, 8 rows, 17 columns.
- `site/hifi/data/notebooks/neso/regional_intensity.json` and `regional_intensity-6.png`: from `scripts/run_notebooks.py`. 6 cells ran with no errors and 1 image.
- `site/hifi/data-sources/neso/regional-carbon-intensity.html`: built.
- No staged chart spec or authored override existed for this family.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| One row per half-hour, region and fuel; key `timestamp_utc, regionid, shortname, postcode, fuel` (facts.grain, record.key) | `silver/neso/carbon_intensity.py:450-457` (one row per `generationmix` entry), `:618-621` (dedup subset). Silver: 109,188 rows = 674 half-hours × 18 regions × 9 fuels. |
| Forecast repeats on every fuel row (chart caption, `forecast_gco2_kwh` field) | `carbon_intensity.py:439-445` puts the region's `intensity` on every mix row. Silver: per (half-hour, region), `n_unique(forecast)` = 1 and `n_unique(index)` = 1. |
| Region ids: 1 to 14 DNO areas, 15 to 17 England, Scotland, Wales, 18 GB (what_it_is, `regionid` field) | Silver `regionid, dnoregion, shortname` distinct: 1 Scottish Hydro … 14 UKPN South East, 15 England, 16 Scotland, 17 Wales, 18 GB. NESO docs (fetched 2026-10-06) name 15, 16, 17 and 3. The vault README's "regionid mixes two grains" note says the same. |
| No `actual` on regional routes (what_it_is, `actual_gco2_kwh` field) | All 19 regional bronze bodies have 0 `"actual"` keys (grep). `actual_gco2_kwh` is null on every row of all 18 members. The NESO API docs' regional examples show `forecast` and `index` only (WebFetch of carbon-intensity.github.io/api-definitions). The page words it as "NESO's regional examples carry …", not as a vendor rule. |
| gCO2/kWh (chart unit, fields) | gridflow column names `forecast_gco2_kwh` and `actual_gco2_kwh` (`carbon_intensity.py:598-599`). The NESO docs page states no unit (see Unverified). Same wording as the national page. |
| Five bands, `very low` to `very high`; cut-offs not sent | Silver distinct `intensity_index`: very low, low, moderate, high, very high. No threshold field in any body. |
| Generation mix in percent, from `perc`; nine fuels | `carbon_intensity.py:454, 602`. Silver fuels: biomass, coal, gas, hydro, imports, nuclear, other, solar, wind. Per region-half-hour sums run 99.7 to 100.2. |
| `timestamp_utc` from `from`, `period_end_utc` from `to` | `carbon_intensity.py:596-597`. Every row is 30 minutes long. |
| `postcode` is an empty string, not null, on non-postcode routes | `carbon_intensity.py:610-614` (`fill_null("")`). Silver `regional_intensity`: 0 null, 109,188 empty. |
| Cadence: forecasts up to two days ahead | Vault `endpoints.md` "Official constraints": "Public forecast horizon is up to two days ahead of real time." |
| "regional routes (beta)" | Endpoint category `Carbon Intensity - Regional beta` (`connectors/neso/endpoints.py:158`ff). The NESO docs header says "Regionalbeta". |
| Request URL and commands (raw_feed) | Bronze sidecar `regional_intensity/2026/09/13/raw_20260926T174340Z_4411da80.meta.json`: `request_url` `…/regional/intensity/2026-09-13T00:00Z/2026-09-22T00:00Z`. `runner.resolve_dates` treats a bare date as midnight UTC. `endpoints.py:12,298-299` format the `from`/`to`. `carbon_intensity.py:149-161` chunk at 14 days (`_MAX_DAYS_PER_REQUEST`). |
| Transform the window's first day only | Connector `data_date=window_start.date()` (`connectors/neso/carbon_intensity.py:79`). The silver exact-read docstring is at `silver/neso/carbon_intensity.py:87-154`. Silver file `regional_intensity_20260913.parquet` holds 12 Sep 23:30 to 21 Sep 23:30. `runner.run_transform` loops `date_range(start, end)` inclusive (`runner.py:1138`). |
| First half-hour ends at `from`, last at `to` (raw_feed.note) | The 13 to 22 Sep request returned 433 half-hours, 12 Sep 23:30 to 21 Sep 23:30 starts. The 1 to 6 Aug request returned 241, 31 Jul 23:30 to 5 Aug 23:30. Scoped "in these responses". |
| Member defaults `RG10` → region 12; region id 13 London | `endpoints.py:13-14`. Silver: every postcode member is `regionid 12, South England, RG10`; every regionid member is `13, UKPN London, London`. |
| Snapshot members return one half-hour | Silver `regional_current`: 1 timestamp (27 Sep 00:00), 18 regions. England, Scotland, Wales, postcode and regionid snapshots: 1 timestamp, 1 region each. Sidecar `fetched_at` 2026-09-27T00:33:05Z. |
| GB (18) differs from the national route's forecast (key note, scoped "checked by the project") | Join with `neso/carbon_intensity` on 674 shared half-hours: \|GB − national forecast\| max 173, mean 9.2; \|GB − national actual\| max 17, mean 3.9. Recorded in the lead note's Known issues. |
| Chart alt and key notes | Committed series: South Wales 6 (20 Sep 14:30) to 390 (20 Sep 22:00), below London at 14 half-hours (midday on 15 and 20 Sep). London 39 to 246, GB 30 to 197. North Scotland 0 at all 336 points. 17 to 19 Sep daily maxima: London 131, 116, 144; GB 95, 83, 95. |
| Eight rows | `gridflow-sample` with filter `timestamp_utc = 2026-09-17T16:30Z`, `fuel = wind`, `regionid in [1,5,7,11,13,15,17,18]` gives 8 rows showing all five bands, DNO areas, two nations and GB. |
| Notebook lead | `gridflow_models` `query()`: relation `silver_neso_regional_intensity`, date column `timestamp_utc`, inclusive ends (`source.py:401-445`, `schema_manifest.py:251`). Excluded columns: `event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year`. |
| plot_alt | Silver gas share 14 to 20 Sep: South Wales 1.3 (20 Sep 14:30) to 98.9 (20 Sep 22:00); London 4.8 to 59.7; GB 4.2 to 44.8; North Scotland 0. |
| Members are the same data by different routes (report only) | On shared (half-hour, region, fuel) cells, forecast, index and percentage differ by exactly 0 in every comparison: the 11 window members against `regional_intensity` or `regional_intensity_pt24h`, and the 5 snapshot members against `regional_current`. The August window members were all fetched within about 2 minutes on 16 Aug, so this shows agreement between routes, not stability over time. |

## Body corrections (vault worktree, mirrored and `cmp`-checked to `vault/neso/`)

On all 18 notes, 3 lines each (6 changed lines):

1. **Silver sample.** The sample paired `regionid 13, UKPN London` with `postcode "RG10"`. No route does that.
   - Postcode routes now show `12 / SSE South / South England / RG10`.
   - `regional_intensity_postcode` now shows `dnoregion ""`.
   - England, Scotland and Wales now show regions 15, 16 and 17.
   - All other routes now show `13 / London / postcode ""`.
   - Evidence: silver region labels per member; `endpoints.py:13`.
2. **Schema row `postcode`.** Changed from "Nullable Yes; when returned or requested" to "empty string, not null, on every other route" (`carbon_intensity.py:610-614`).
3. **Known issues `actual`.** Changed from "can be null or absent, especially before post-period estimates" to "Regional responses carry no `actual` … null on every regional row". Evidence: bronze grep and the NESO docs examples.

Lead `regional_intensity.md` only: two Known-issues bullets.

- Window edges and bronze ownership.
- Region 18 differs from the national forecast (the project check, with numbers).

`regional_intensity_postcode.md` only: one sentence. The 16 Aug `RG10` body had no `dnoregion`, so silver writes `""`.

## Unverified

- **Unit.** The NESO API docs page, as fetched, states no unit. gCO2/kWh rests on gridflow's column names and the domain convention, the same basis as the national page.
- **Band thresholds.** Measured bands are 0 to 24, 25 to 89, 90 to 169, 170 to 229 and 230 and above. These are not checked against the vendor and are not on the page.
- **Region table.** The docs region-list section did not come through in the fetch. Ids 1 to 14 rest on the `dnoregion` names in the rows.
- **"Current" half-hour.** `/regional` fetched at 00:33:05 UTC returned 00:00 to 00:30, the half-hour that had just ended. The page says "the one NESO serves as current" and does not say "the present half-hour".
- **Forecast vintage.** Whether NESO revises regional forecasts after the period is unknown. All the August bodies were fetched on 16 Aug, two weeks after the periods they cover.

## Open questions

1. Is the key note "checked by the project, it is not the national route's `forecast`" acceptable without numbers on the page? The numbers are in the vault body only.
2. Should the snapshot members (one half-hour each) also be dated on the page? They carry no chart or frame, so I left them undated in `differs`.

## Template problems

- `FAMILY_MEMBERS = (2, 12)` rejected this family's 18 members, which `neso.json` fixes. The seat raised it to `(2, 18)`, and the build now passes.

## Defects

Paste into the backlog as is:

- **NESO vault README stale V1 note** (`quant-vault/30-vendors/neso/README.md`, "Latent silver bug logged for follow-up"):
  - It says the five period-keyed regional datasets have null intensity, index, fuel and percentage in silver. That has been fixed since V2-FIX-02.
  - Silver now has 0 null `forecast_gco2_kwh`, `fuel` and `generation_percentage` on all five datasets (checked 2026-10-06).
  - Fix: mark the note resolved.
- **Schema comment contradicts transformer** (`gridflow/src/gridflow/schemas/neso.py:68-74` against `silver/neso/carbon_intensity.py:610-614`):
  - The schema says all-regions routes "carry it through as null". The transformer writes `postcode` as `""` (`fill_null("")`).
  - Silver `regional_intensity` has 0 null and 109,188 empty `postcode` values.
  - Fix: align the comment with the transformer, or emit null.
- **Vendor shape: `regional_intensity_postcode` omits `dnoregion`** (observation; no code defect):
  - `/regional/intensity/{from}/{to}/postcode/RG10` (body of 16 Aug) has no `dnoregion` on its region object. The fw24h, fw48h and pt24h postcode bodies do have one.
  - Silver therefore holds `dnoregion ""` for that member.
- **Possible national forecast anomaly, for the national page's writer and the seat** (`neso/carbon_intensity`, unverified whether vendor or gridflow):
  - 8 of 674 half-hours have national `actual − forecast` above 60 gCO2/kWh. All 8 fall at 19:30, 04:00 or 04:30 UTC.
  - For example, 21 Sep 19:30 has forecast 38 against actual 203, and 15 Sep 19:30 has 28 against 136.
  - Regional GB (18) for those half-hours sits close to the national actual: 211 against 203, and 140 against 136.
  - Needs a check of the national bronze body before anyone treats it as a defect.
