# Author report: `neso_data_portal/historic_generation_mix`

Writer: Opus 5.5 (high), 2026-10-06. Page is single (no family). Screenshot port 9864 (not used: screenshots went over
`file://` with headless Chrome, profile `scratchpad/hgm_chrome`, every call under `timeout 60`).

## Status

- `gridflow-build --only neso_data_portal/historic_generation_mix`: succeeds, no errors.
- `detect.mjs --json`: `[]`. Em dashes in the page: 0. No `→` or middle dots.
- Mirror: canonical `vault-p26-rest/30-vendors/neso-data-portal/datasets/historic-generation-mix.md` copied to
  `p26-rest/vault/neso_data_portal/historic_generation_mix.md`; `cmp` byte-equal; CRLF kept (331 CR on 331 lines at
  first edit). Note diff: page block plus small body spans, no whole-file rewrite.
- Artefacts (front-end worktree): `site/hifi/data/series/neso_data_portal/historic_generation_mix.json`
  (`spec_origin: vault`, 6,477 points), `site/hifi/data/samples/neso_data_portal/historic_generation_mix.json`
  (`gridflow-sample`, 8 rows, 40 columns), `site/hifi/data/notebooks/neso_data_portal/historic_generation_mix.json` +
  `-5.png` (`scripts/run_notebooks.py`, 5 cells, no errors). No staged chart spec or authored override existed.
- Screenshots: `scratchpad/hgm_shots/w{1440,1024,768,390}.png` (+ `_N.png` crops). 390 is a true 390 px iframe
  (`scratchpad/hgm_390.html`). Nothing clipped or overlapping at any width. The site has no dark theme (no
  `prefers-color-scheme` / `data-theme` in CSS, JS or DESIGN.md), so light only.
- **Recommendation: ship.** Thin spots are template limits (below), not data problems.

## Chart

Line, `solar` daily mean (mean of each UTC day's 48 half-hours), 1 Jan 2009 to 25 Sep 2026, deduplicated to the newest
capture per `timestamp_utc` (`dedup on timestamp_utc, order_by published_at`, which matches the `_latest` view), so
every point comes from the capture published 2026-09-26 18:19:36 UTC. Unit MW. `max_points: 6500`.

Why this chart: the spec takes one value column plus a group column and buckets up to 1 day, so the wide 11-column mix
cannot be stacked (template problem 1). `carbon_intensity` was rejected because NESO gives it no unit. `solar` is
the column this dataset supplies against fuelhh, and the subject of the note's G-1 section. The notebook plot shows
the full stacked mix for 19 to 25 Sep 2026 instead.

## Evidence table

| Claim on the page | Evidence |
|---|---|
| One row per half-hour and capture; key `(timestamp_utc, published_at)`; latest view keeps one | `silver/neso_data_portal/historic_generation_mix.py` `ENTITY_KEY_COLUMNS`, `APPEND_ONLY`, `VINTAGE_PER_BRONZE_FILE`; `silver/latest_views.py:124-126` key `timestamp_utc`. Silver: 3 captures (309,161 / 309,931 / 310,931 rows = 930,023), 0 duplicate keys |
| `timestamp_utc` is UTC | Transformer docstring; `_probe/datastore_historic-generation-mix.json` `DATETIME.info.description` "given in UTC" |
| Start of the half-hour ("start matched against fuelhh") | Measured, not vendor: 26 Sep capture vs fuelhh latest, 1 Jun to 26 Sep 2026, 5,650 half-hours. Lag 0: `wind == WIND` 98.5%, `nuclear == NUCLEAR` 96.7%, `hydro == NPSHYD` and `storage == max(PS,0)` mean abs diff 0. Lag ±30 min: wind MAE 239 MW, gas 357 MW (lag 0: 15 MW, 9 MW) |
| Each capture is a complete half-hour grid (not on page; supports the chart's "48 half-hours") | Every capture: rows == (last-first)/30min+1, no off-grid minutes, no gap ≠ 30 min. Bronze CSVs: `DATETIME` n_unique == rows in all 3 files |
| "From 1 January 2009, as NESO states" | `_probe/show_historic-generation-mix.json`: notes "This dataset contains data from 1 January 2009"; resource description "from the 1st of Jan 2009 through to today". Now quoted in the note body |
| NESO republishes the whole file; no stated interval | `fetch()` docstring (one whole-file snapshot per call); note "Publication lag: TODO, not stated" |
| NESO cleanses and republishes history | CKAN notes "subject to change due to a data cleansing process" (transformer docstring) |
| Transmission solar farms and batteries in `other`; net-negative values curtailed at zero; pumped storage (net) in `storage` | CKAN package notes (probe JSON; also quoted in the note's G-1 section, retrieved 2026-09-25) |
| MW units | Resource description "Data points are either MW or %"; datastore `_perc` fields unit "%" |
| `carbon_intensity`: "CO2 per kWh consumed, as NESO describes it; the file states no unit" | Datastore field `unit: ""`, description "how much Carbon dioxide emissions are produced per kilowatt hour of electricity consumed" |
| `generation` = NESO's sum of the eleven source columns | Datastore description lists the 11; measured within 3 MW on every row of the 26 Sep capture |
| `wind` is without embedded wind | `GENERATION` description sums "wind, wind embedded" separately |
| `wind_emb`: NESO titles it Wind EMB, no description | Datastore field `title: "Wind EMB"`, `description: ""` |
| low_carbon / renewable / fossil "NESO's examples" | Datastore descriptions ("e.g. ...") quoted, nothing more claimed |
| `zero_carbon`: "here below NESO's described sum of wind, solar, hydro, nuclear" | Eight rows: e.g. 09-05 11:00 zero_carbon 16,695 vs wind 11,059 + solar 11,617 alone = 22,676 |
| `zero_carbon_pct`: "here not `zero_carbon` over `generation`, and above `low_carbon_pct`" | Eight rows: 87.2 to 92.2 vs computed 39.7 to 45.8; `low_carbon_pct` 81.6 to 83.4 |
| `_pct` = column over `generation` | Measured within 0.06 points for all 14 non-zero-carbon `_pct` columns, every row (26 Sep capture) |
| `generation_pct` 100 in these rows | Eight rows (also every row of the capture) |
| `published_at` = NESO's last-modified time for the file, read as UTC | `silver/neso_data_portal/_bronze.py:72-73,130,192-206` (`ckan_last_modified`, naive read as UTC, D-15); sidecar `ckan_last_modified: 2026-09-26T18:19:36.497453` = silver value |
| Raw requests | `endpoints.py` (`package_show`, `id=historic-generation-mix`), `config/sources.yaml:756` base URL; second URL is the resource `url` recorded in bronze sidecar `2026/09/26/raw_20260926T182820Z_daf7180c.meta.json` `request_url` |
| "Dates select nothing" | `client.py` `fetch()` docstring: "The window is **not a selector** (D-16)"; one package_show + one download per call |
| `--last 24h` on both commands; "window must end recently" | `client.py:1274-1350` `_assert_window_admissible`: end ≤ now+5 min, end ≥ now−48 h, span ≤ 7 days; bronze partition = `end.date()`. `runner.resolve_dates`: `--last` gives `(now−24h, now)`; `run_transform` iterates `date_range(start.date(), end.date())`, so it covers the ingest's partition |
| Chart window, aggregation, dedup | Series JSON `provenance`: rows_used 310,896, duplicates_dropped 619,092, time_bucket 1 day, window fixed 2009-01-01..2026-09-25 |
| Alt numbers | Series: zero 2009 to 2012; first > 0 on 2013-01-01 (110 MW); yearly max 613 (2013), 2,045 (2015), 3,174 to 3,475 (2017 to 2022), 5,444 (2026-07-12); yearly minima ≤ 153 MW; last 2,426 MW |
| Eight rows | `gridflow-sample`: 2026-09-05 11:00 to 12:30 UTC, captures 09-05 22:15 and 09-26 18:19. Solar revised +56 to +369 MW, imports −112 to −195 MW, carbon_intensity also revised |
| Notebook lead | gridflow_models `research/handles/source.py:401-445` (`query`), `_get_method_registry.py:62-96` (TIMESTAMPTZ: half-open UTC days, end day included), relation map → `silver_neso_data_portal_historic_generation_mix_latest`, `_BITEMPORAL_EXCLUDE` (event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year). Output prints `2026-09-19 01:00:00+01:00` (= 00:00 UTC), hence "Times print in local time" (freq precedent) |
| Plot alt numbers | `_latest`-equivalent 19 to 25 Sep: generation 22,707 to 38,306 MW; solar max 13,127 (20th 12:00); wind daily means 15.2 GW (19th), 11.4 GW (20th), 3.8/2.9 GW (21st/22nd); gas daily means 9.2/12.2 GW (21st/22nd) |
| Related: INDO "excludes almost all solar" per NESO | Note's G-1 section: NESO OTF, 22 Jan 2025 |
| Related: fuelhh has no solar code | fuelhh note (Bobbo ruling 2026-08-31, zero solar rows) |

## Body corrections (canonical note)

1. **Historical depth row:** added the vendor quotes and the probe file as evidence (was an unsourced paraphrase).
2. **Silver schema row (`gas … fossil`):** "`carbon_intensity` is gCO2/kWh" replaced with: no unit in NESO's field
   metadata, the vendor's description, "values fit gCO2/kWh, unconfirmed". Evidence: datastore probe `unit: ""`.
3. **"Cross-checked against Elexon" bullet:** the settlement-convention test and the TIME_GMT corroboration run on
   `embedded_wind_solar_forecast`, not this dataset (`tests/integration/test_neso_data_portal_mocked_e2e.py:633-735`,
   `EMB_DATASET`). This dataset's `timestamp_utc` is the raw `DATETIME`, never derived from a settlement pair. Added
   the fuelhh alignment measurement (start of period) and the `imports` per-link finding.
4. **New known-issues bullets:** vendor package notes (seasonal decomposition, pumped storage NET in STORAGE,
   net-negative curtailed at zero); grid, keys and revisions between captures (measured); derived-column composition
   (storage inside low_carbon and renewable; zero_carbon and zero_carbon_pct irregular).
5. **Modelling notes:** "`solar` before ~2011" replaced with "zero before 2013-01-01, `biomass` zero before
   2017-11-01" (measured, 26 Sep 2026 capture).

`last_verified` left at 2026-09-25 (the seat may bump it). The illustrative bronze and silver samples were left as
they are: they are labelled illustrative.

## Could not verify

- Whether `solar` is embedded solar only. The G-1 section rates this a deduction. The page says only that it excludes
  transmission-connected solar farms (vendor fact) and never calls it embedded or estimated.
- Start versus end of period from NESO. The page scopes it as "matched against fuelhh".
- `carbon_intensity` unit.
- NESO's republication cadence (three captures: 2026-08-20, 09-05, 09-26 published; not stated by NESO).
- Why `zero_carbon` / `zero_carbon_pct` behave as they do, and why `biomass` is zero before Nov 2017 and `solar` before 2013.
- That `wind` is transmission-metered wind. It matches fuelhh `WIND` on most half-hours since June 2026, but the page
  says only "without embedded wind".
- The notebook drawer contents were checked from the JSON and the PNG, not from an opened drawer screenshot (headless
  Chrome does not click).

## Open questions (for the seat)

1. Should `chart_spec` gain a wide-table option (several value columns unpivoted into series) so this page can show
   the stacked mix? Until then the chart shows `solar` only.
2. A multi-year axis has no year labels (template problem 2). Ship as is, or wait for a renderer fix?
3. NESO says BESS and transmission-solar splits arrive "later in 2026". When they do, the `other` and `solar` key
   notes and guide lines will need re-checking against the new capture.

## Template problems (report only; nothing worked around)

1. **Wide tables cannot be charted as a mix.** `chart_spec` takes one `value` column plus a `group` column, and
   `time_bucket` stops at `1d` (no monthly). This dataset is one column per fuel, so no stacked area is possible.
2. **Multi-year time axis has no years.** `chart_svg.py:_time_axis` (span > 120 days) puts a tick on every 1st of the
   month labelled `"{day} {Mon}"`. At 1440 px the axis shows 18 "1 Jan" labels with no year and a comb of monthly
   tick marks. At 390 px it thins to every 53rd tick, giving "1 Jan, 1 Jul, 1 Jan, 1 Jul". Needs year labels (and
   yearly ticks) for spans over about two years. The caption, x_label ("UTC day, 2009 to 2026") and alt carry the
   years meanwhile.
3. **390 px frame hides the second key column.** At 390 only `timestamp_utc` stays unfolded, so the eight rows read
   as four duplicated pairs. `published_at` (the other key column) folds behind `…`. This affects any two-column key.
4. Long identifiers in the notebook lead (`silver_neso_data_portal_historic_generation_mix_latest`) break mid-word at
   1440 (narrow lead column). Cosmetic.
5. Tooling: the front-end `.venv` has no `tzdata`, so Polars `.to_list()` / `.min()` on a UTC datetime raises
   `ZoneInfoNotFoundError`. Distil and sample avoid it; ad hoc checks need `strftime`.

## Defects

Paste as is. Vendor-side items are data defects (gridflow carries NESO's values unchanged); none needs a gridflow
code change.

- **NESO historic_generation_mix: `zero_carbon_pct` is not `zero_carbon / generation`.** In the capture published
  2026-09-26 18:19:36 UTC, `zero_carbon_pct` exceeds `low_carbon_pct` on 204,578 of 310,931 rows, and differs from
  `100*zero_carbon/generation` by up to 69 points. Example: 2026-09-05 11:00 UTC, zero_carbon_pct 92.2, computed
  45.8, low_carbon_pct 83.4. Every other `_pct` column matches its MW column over `generation` within 0.06 points.
  Vendor data; undocumented. Consumers should not use `zero_carbon_pct`. Logged in the vault note.
- **NESO historic_generation_mix: `zero_carbon` does not match its description.** The description is "wind, solar,
  hydro, nuclear". Through 2018 the column equals nuclear + wind + hydro + biomass + storage (includes biomass, omits
  `wind_emb` and `solar`). It fits no fixed sum in recent years, and it changed between the 5 Sep and 26 Sep 2026
  captures for the same half-hours by 58 to 327 MW. Vendor data.
- **NESO historic_generation_mix: storage counted in `low_carbon` and `renewable`.** `low_carbon` = nuclear + wind +
  wind_emb + hydro + biomass + solar + storage and `renewable` = wind + wind_emb + hydro + solar + storage (within
  2 MW, every row). The vendor descriptions do not list storage. Vendor documentation gap.
- **NESO historic_generation_mix: structural zeros.** `solar` is 0 in every half-hour before 2013-01-01 and `biomass`
  before 2017-11-01 (26 Sep 2026 capture). NESO gives no reason. Treat them as structural in models; do not
  backfill.
- **NESO historic_generation_mix: `carbon_intensity` has no unit.** The datastore field unit is empty, and the
  resource description says "Data points are either MW or %", which is wrong for this column. The vault previously
  asserted gCO2/kWh without a source (corrected).
- **NESO historic_generation_mix: `imports` is per-link imports, not net flow floored.** Against fuelhh (Jun to Sep
  2026), `imports` tracks the sum of each interconnector's positive flow (MAE 36 MW), not the net of all links
  floored at zero (MAE 1,369 MW). The vendor note "All Net-Negative values are curtailed at zero" reads as per
  category. Consumers netting flows must not read `imports` as net imports.
- **Vault (fixed in this branch): the historic_generation_mix note credited the embedded-forecast settlement test to
  this dataset.** `tests/integration/test_neso_data_portal_mocked_e2e.py:633-735` runs on
  `embedded_wind_solar_forecast` only. No test covers this dataset's period convention. Suggest a gridflow test (or
  a documented measurement) pinning `DATETIME` as period start, mirroring the TIME_GMT tripwire.
- **gridflow_models (presentation, may be logged already): `query()` prints `timestamp_utc` in session local time**
  (`2026-09-19 01:00:00+01:00` for 00:00 UTC). The same instant, but a column named `_utc` printing BST confuses
  readers. Seen on freq, indo, remit and this page.
