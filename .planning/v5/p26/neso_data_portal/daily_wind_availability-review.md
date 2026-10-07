# neso_data_portal/daily_wind_availability: review

Checker: Sonnet 5.5 · high, 2026-10-06. Screenshot port 9886 (server stopped).

## Verdict: REVISE

One blocker (a cadence claim that NESO's own catalogue contradicts). One major (the same wrong claim reaches the
canonical note's evidence trail, see finding 2). Everything else checked clean.

Findings: 1 blocker, 1 major, 4 nits.

## Findings

1. **Blocker. `page.facts.cadence`** (also `page.summary`-adjacent: author report "Not verified"). The page says
   "NESO does not state how often it republishes the file". NESO does state it. The CKAN package record for
   `daily-wind-availability` carries `extras: [{"key": "Update Frequency", "value": "Hourly"}]`.
   - Evidence: `gridflow/.planning/phases/neso-data-portal/_probe/package_search_p0.json`, the very file the note
     cites as NESO's description, record `name == "daily-wind-availability"`, `extras` =
     `[{'key': 'Update Frequency', 'value': 'Hourly'}]`. It is repeated in the 20 Aug 2026 catalogue snapshot,
     `quant-vault/30-vendors/neso-data-portal/_generated/snapshots/20260820T214455Z/catalog-snapshot.json`
     lines 1477-1489 (`"Update Frequency"` / `"Hourly"`), taken the same evening as the capture.
   - The writer quoted `notes` and the resource `description` from that record but did not read `extras`.
   - Fix: state the vendor field, scoped to where it appears, for example "Daily resolution; NESO's catalogue lists
     the update frequency as hourly". Keep it as a catalogue statement, not a measured cadence (the file we hold is
     one capture). Also drop the "NESO does not state it" line from the author report's open items.

2. **Major. Canonical note, `Overview` / `page.facts` provenance, and the sibling note.** The vault note's new
   "NESO's own description" paragraph is presented as the vendor's description but omits the vendor's one cadence
   field, which is what produced finding 1. The sibling note `30-vendors/neso-data-portal/datasets/historic-generation-mix.md`
   line 14 makes the same claim ("NESO republishes the whole file, at no stated interval"), and the same probe record
   for `historic-generation-mix` has `extras = [{'key': 'Update Frequency', 'value': 'Hourly'}]`. The seat should have
   the `historic_generation_mix` checker confirm and fix it; `embedded-wind-and-solar-forecasts` carries only
   `Status: Live` in `extras`, so "no stated interval" is correct there.
   - Fix for this note: add "Update Frequency: Hourly (CKAN `extras`)" to the NESO description paragraph.

3. **Nit. `page.record.fields.bmu_id`.** "matches Elexon's `national_grid_bm_unit`" is unscoped. Reproduced
   counts: of the 276 distinct `bmu_id` in silver, 231 are in `elexon/bmunits_reference.national_grid_bm_unit` (all
   231 have `fuel_type == WIND`) and 0 are in `bm_unit_id` (45 absent, for example `ACHYW-1`, `AKGLW-1`,
   `BENBW-2`). The page never states a count, which is right, but "matches" reads as all of them. Suggest "is
   National Grid's unit ID, the form in Elexon's `national_grid_bm_unit`". `what_it_is` ("The project matched ...")
   is correctly scoped.

4. **Nit. `page.notebook.lead`.** "one row per unit and day from the latest NESO file". The `_latest` view keys on
   `(bmu_id, availability_date)` and takes the latest `published_at` per key (`silver/latest_views.py:115-117`), so with
   several captures a day can come from an older file if the newer one dropped it. Say "the most recently published
   row per unit and day".

5. **Nit. `page.notebook.needs`.** "with NESO's file of 20 August 2026 ingested". Accurate to what was run, but the
   reader cannot ingest that file (`client.py:1340-1349` refuses a past window; the page itself says NESO serves
   only the current file), and later captures cover shifted days, so the 22 Aug to 3 Sep query returns nothing for a
   fresh reader. This is the writer's own open question; I am not rating it above nit because the wording is honest.
   A reader-facing phrasing such as "a NESO file covering 22 August to 3 September 2026" says the same without
   promising the unobtainable.

6. **Nit. Hero chip at 390 px (template, report only).** The dataset id chip breaks mid-word
   (`neso_data_portal/daily_wind_availabilit` / `y`). It is a wrap, not a clip or overlap. Same for the notebook tab
   (`daily_wind_availabili…`), already reported by the writer.

Also seen, not findings: the vault `Overview` still says "the MW each transmission-connected wind BM unit expects to
have available", where "transmission-connected" is not in NESO's quoted text (body only, not on the page);
front matter `last_verified: 2026-08-19` was not bumped after the 2026-10-06 body edits.

## What I verified (all clean unless listed above)

**Chart (the focus).**
- Recomputed from silver with Polars: 276 units, 13 availability days (22 Aug to 3 Sep 2026), 13 rows per unit, 0
  duplicates on the key, one `published_at` (2026-08-20 21:20:07.510686 UTC), all MW whole numbers (max 440).
  Daily sums over `availability_mw >= 0`: 25,744 / 25,968 / 25,751 / 25,786 / 25,598 / 25,665 / 25,381 / 25,381 /
  25,381 / 26,215 / 26,474 / 26,474 / 26,474. Identical to the committed series; min 25,381, max 26,474.
- The only negative values are `ASHWW-1`, -1 on all 13 days (13 rows). Including it moves every total down 1 MW. The
  filter excludes it and the caption says so. Series provenance: `rows_read` 3,589, `rows_matched`/`rows_used` 3,575
  (3,589 - 1 null row - 13 `ASHWW-1`), `duplicates_dropped` 0.
- Series `spec_origin: vault`, `spec` matches the note's `page.chart`; no staged spec or authored override exists.
- Alt text numbers (25,744, 25,968, 25,381 for 28 to 30, 26,215 on 31, 26,474 for 1 to 3 Sep) and `plot_alt` ("between
  25,381 and 25,968 to 30 August") match the series.
- "The MW axis does not start at zero" is true: rendered axis 25,250 to 26,750 at 1440 (seen), 25,000 to 27,000 at 390
  (seen). The caption names no number, so it holds at every width. The notebook plot does start at zero
  (`ylim=(0, 30000)`, seen in `-5.png`), which the page does not contradict.

**Unit IDs.** 231 of 276 on `national_grid_bm_unit`, 0 of 276 on `bm_unit_id` (3,014-row register; `T_ABRBO-1` is the
`bm_unit_id` of `ABRBO-1`). The same IDs also appear in `elexon/uou2t14d.national_grid_bm_unit` (232 of 276), so the
related-dataset join advice holds.

**NESO quotes.** Package `notes`: "wind generator availability in megawatts (MW) at a daily resolution for 2-14 days
ahead"; resource `description`: "technical availability of the wind farms rather than what they are able to actually
produce based on wind speed". Both support "2 to 14 days ahead" and "technical availability". The file's days (22 Aug
to 3 Sep) are D+2 to D+14 from its 20 Aug publication. NESO's text never uses the word "forecast"; calling it NESO's
forecast is a fair reading of "ahead" and the summary does not put the word in NESO's mouth beyond that (not rated).

**Null trailing row and stamps.** Silver holds 3,589 rows, 3,588 real: one row has null `bmu_id`,
`availability_date`, `availability_mw`, `timestamp_utc`, `event_time` with valid `published_at`/lineage. The bronze
file ends `...,206\n\r\n` (a final line holding only CR), `csv_bronze.py:123-128` reads the body with `pl.read_csv` and
no blank-row drop, and `base.py` validation is fail-soft (never drops a row). Silver filename stamp
`run2026-08-20T21-43-33.257005-00-00` equals the bronze sidecar `written_at` (21:43:33.257005), not `available_at`
(21:20:07.510686); `base.py:2616-2625` docstring says the suffix is `available_at`, so the writer's defect stands. The
page states neither, correctly. The page and notebook never touch the null row (query filters on `availability_date`).

**Other facts.** `published_at` = sidecar `ckan_last_modified` read as UTC (sidecar `2026-08-20T21:20:07.510686`);
`timestamp_utc` = SP1 of the GB day (31 Aug to 2026-08-30 23:00 UTC); key `(bmu_id, availability_date, published_at)`
with `APPEND_ONLY`; request URLs match the sidecar `request_url` and `endpoints.py`; ingest `--last 24h` and the
historical-window refusal match `client.py`; bronze partition is `end.date()` UTC so the transform window is right.
Notebook lead matches `query()` (the `_latest` relation, `availability_date`, inclusive). No test of "use silver cannot
deliver": the three `how_used` lines are all deliverable from the `_latest` view of one or more captures.

**Structure and look.** `gridflow-build --only neso_data_portal/daily_wind_availability` succeeds; `detect.mjs --json`
returns `[]`; mirror `cmp` byte-equal to the canonical note; no em dashes, arrows or middle dots in the built page;
rubric section 3 grep finds nothing local. Notebook JSON is `generated_by: scripts/run_notebooks.py`, read-only cells,
no error outputs. Screenshots by me at 1440, 1024, 768 and a true 390 iframe (cropped in 4): hero scenery, chart, key,
raw-feed boxes (long redirector URL wraps), frame folded and unfolded (scrolls sideways when unfolded, by design),
column guide, notebook panel, related list: nothing clipped or overlapping.
