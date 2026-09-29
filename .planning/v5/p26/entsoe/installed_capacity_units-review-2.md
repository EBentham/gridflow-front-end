# installed_capacity_units: checker re-review

Checker: Opus 5.5 (high), 2026-09-29. This re-checks the fixes in `installed_capacity_units-author-2.md` against `installed_capacity_units-review.md`, reading the canonical note in `vault-p26-entsoe`. The mirror is byte-identical to it (`cmp`).

## Verdict: APPROVE

No findings remain above nit.

## Review 1 findings

### 1. major, scope: fixed

- **`page.what_it_is`** now reads "gridflow asks per UTC day; the replies received each carried the whole year, so silver holds one copy per fetch, told apart by `published_at`."
  - The per-day request is a code fact (`client.py:162`, `day_subwindows`). The whole-year reply is now scoped to the replies received.
  - The ambiguous "Each ingest day" is gone.
- **`page.notebook.lead`** now reads "In the replies received each fetch added a full copy, so keep each unit's latest `published_at`."
  - Dropping "(the year start)" costs nothing, because `record.fields.timestamp_utc` still gives it.
  - The rest of the lead still matches `query()`.
- The rendered page has neither old phrasing and all three scoped phrasings (facts, raw feed, what it is, lead).

### 2. nit, B08 provenance: fixed

- `chart_view.key[smaller].note` now reads "B08 peat per entsoe-py (IE-SEM's West Offaly, Edenderry, Lanesboro), with marine, solar, waste and storage."
- The source is now on the page. The three unit names are vendor data from the 2026 document, not a local statistic (silver: exactly three B08 units, all `10Y1001A1001A59C`, matching review 1).
- The body's `production_type` schema row states the entsoe-py-only basis.

### 3. nit, related wording: fixed

- The note now reads "Output per unit, keyed on the same kind of unit EIC (`unit_mrid`)".
- This is a source-field fact. A73 bronze (`actual_generation_units/2026/09/08/*.xml`) carries `registeredResource.mRID` (for example `17W100P100P0318E`), which is the same element A71 maps to `unit_mrid` (`parsers.py:351-352`).
- It is 12 words or fewer.

### 4. nit, sample `ingested_at`: fixed

- The body sample now has `"ingested_at": "2026-09-15T20:09:28.630326+00:00"`. This equals the silver ABRBO row in `installed_capacity_units_20260914.parquet` that review 1 read.

### Extra: "365 requests": fixed

- Known issues now says "about 365 requests per zone (differing only in `periodStart`/`periodEnd`); if each returns the same document, as all replies seen so far did, that is 365 silver copies."
- This is accurate and scoped.

## Regression checks

- **Build.** `gridflow-build --only entsoe/installed_capacity_units` wrote the page. There are no budget, digest or related errors, and the three warnings belong to other datasets. The chart spec, sample select and notebook cells are unchanged, so the digests still pass.
- **Detector.** `detect.mjs --json`, run at its absolute path, gives one `em-dash-overuse` advisory (92 hits from EIC `--` padding). This is accepted under ruling #39.
- **Characters.** The rendered page has 0 em dashes, arrows or middots.
- **Screenshots** (CDP, `file://`, inside `timeout 60`, port 9670 not touched):
  - At 1024 (key in three columns) and at a true 390, the new B08 note wraps cleanly, and the key, raw feed, frame header, notebook and related datasets show nothing clipped or overlapping.
  - `scrollWidth` equals `innerWidth` at both widths.
  - The only clip is the known `.ipynb` tab at 390 (ruling #39).

Summary: all review 1 findings (1 major, 3 nits) and the "365 requests" wording are fixed and verified, the build and detector are clean, and nothing regressed, so installed_capacity_units is APPROVED.
