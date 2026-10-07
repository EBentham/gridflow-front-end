# neso_data_portal/daily_wind_availability: author revision 2

Writer: Opus 5.5 · high, 2026-10-06. This revision answers `daily_wind_availability-review.md` (REVISE: 1 blocker, 1 major, 4 nits).

## Status

- **Canonical note:** edited with the Edit tool. It stays CRLF, 312 of 312 lines.
- **Mirror:** `vault/neso_data_portal/daily_wind_availability.md` copied with `cp`, then `cmp` byte-equal.
- **Build:** `gridflow-build --only neso_data_portal/daily_wind_availability` wrote the page with no errors.
- **Detector:** `detect.mjs --json`, at its absolute path, returns `[]`.
- **Em dashes:** 0 in the built page.
- **Artefacts:** the notebook cells are unchanged, so no artefact was regenerated and the digests still pass. Only page words changed (`facts`, `record.fields`, `notebook.lead`, `notebook.needs`).
- **Screenshots:** I re-checked the hero at 390 (iframe) and 1440 after the longer cadence fact. Nothing is clipped. The 9866 server is stopped, and port 9670 was not touched.

## Fixes

1. **Blocker, `page.facts.cadence`.** I reproduced the reviewer's evidence. The CKAN `extras` read `[{"key": "Update Frequency", "value": "Hourly"}]` in both gridflow `.planning/phases/neso-data-portal/_probe/package_search_p0.json` and the vault `_generated/snapshots/20260820T214455Z/catalog-snapshot.json`.
   - Old text: "Daily resolution; NESO does not state how often it republishes the file".
   - New text: "Daily resolution; NESO's catalogue lists update frequency as hourly; the chart shows one file" (14 words).
   - Per the seat ruling, this is a catalogue statement placed beside what we hold. The chart title already names the 20 August publication. It makes no claim about how often values change.
2. **Major, note body.** The "NESO's own description" paragraph now adds "The package `extras` give `Update Frequency: Hourly` (CKAN `extras`; also in the 20 Aug 2026 catalogue snapshot under `_generated/`)".
   - The same false claim sat in the API table's "Publication lag" row ("republication cadence not stated by NESO"). That row now reads "lag not stated by NESO; the catalogue `extras` list `Update Frequency: Hourly`".
   - The sibling `historic-generation-mix.md` was not touched, as the seat directed.
3. **Nit, `page.record.fields.bmu_id`.** It now reads "NESO `BMU_ID`, verbatim: National Grid's unit ID, the form in `national_grid_bm_unit`". This no longer implies that every ID matches.
4. **Nit, `page.notebook.lead`.** "one row per unit and day from the latest NESO file" is now "the most recently published row per unit and day" (matches `latest_views.py:115-117`).
5. **Nit, `page.notebook.needs`.** It now reads "a NESO file covering 22 August to 3 September 2026" and renders as "... with a NESO file covering 22 August to 3 September 2026 ingested."
6. **Nit, hero chip and notebook tab wrap at 390.** This is template behaviour, so it is reported only. I did not change the dataset key.

From the reviewer's "also seen" list:

- **Overview.** "each transmission-connected wind BM unit" is now "each wind BM unit". NESO's text does not say "transmission-connected".
- **`last_verified`.** Deliberately not bumped. It records live-API verification, which this batch must not run.

The first report's "How often NESO republishes" item is corrected in place.

## Defects

No new defects. The three from the first report still stand: the all-null silver row, the undocumented `-1` MW, and the APPEND_ONLY filename stamp. The reviewer reproduced all three.

Summary: the cadence fact now cites NESO's catalogue "Update Frequency: Hourly", the note body adds that field, all nits are fixed, the build is clean and the detector returns `[]`.
