# neso_data_portal/daily_wind_availability: re-check (review 2)

Checker: Sonnet 5.5 · high, 2026-10-06. Focused re-check of `daily_wind_availability-review.md` against
`daily_wind_availability-author-2.md`. Screenshot port 9886 (server stopped). Port 9670 not touched.

## Verdict: APPROVE

No findings above nit; no new findings.

## Previous findings

1. **Blocker, `page.facts.cadence`: resolved.** Now "Daily resolution; NESO's catalogue lists update frequency as
   hourly; the chart shows one file". Accurate: the CKAN `extras` read `Update Frequency: Hourly` (checked in the
   gridflow probe and the 20 Aug 2026 catalogue snapshot in review 1). It is attributed to NESO's catalogue and is
   not a measured cadence. It does not imply that values change hourly: "update frequency" is NESO's label and the
   second clause says only that the chart shows one file, which the chart title ("published 20 August 2026") shows.
   Rendered in the built hero at 1440 and at a true 390 iframe: three lines, nothing clipped.
2. **Major, note body: resolved.** The "NESO's own description" paragraph now ends "The package `extras` give
   `Update Frequency: Hourly`", and the API table's "Publication lag" row no longer says the cadence is unstated
   ("lag not stated by NESO; the catalogue `extras` list `Update Frequency: Hourly`"). The sibling
   `historic-generation-mix` note is routed separately and was left out, as instructed.
3. **Nit, `record.fields.bmu_id`: resolved.** "NESO `BMU_ID`, verbatim: National Grid's unit ID, the form in
   `national_grid_bm_unit`". No longer implies every ID matches (231 of 276 do; the page states no count).
4. **Nit, `notebook.lead`: resolved.** "the most recently published row per unit and day", matching
   `latest_views.py:115-117` (key `(bmu_id, availability_date)`, latest by `available_at`).
5. **Nit, `notebook.needs`: resolved.** Renders "with a NESO file covering 22 August to 3 September 2026 ingested".
   No longer promises the unobtainable 20 Aug file.
6. **Nit, 390 px ID chip and notebook tab wrap:** template, seat's; not a finding (as instructed).

## "transmission-connected" removal

Correct. The overview now reads "the MW each wind BM unit expects to have available on a given day". NESO's quoted
text (package `notes`, resource `description`) says only "wind generator availability" and "technical availability of
the wind farms"; neither says transmission-connected. Nothing on the page used the word.

## Regression check

- `gridflow-build --only neso_data_portal/daily_wind_availability`: succeeds (artefact digests pass; the series, sample
  and notebook JSON were not regenerated and the cells are unchanged).
- `detect.mjs --json` on the built page (absolute path): `[]`.
- Mirror `vault/neso_data_portal/daily_wind_availability.md` is byte-equal (`cmp`) to the canonical note.
- Built page: 0 em dashes; the rendered Cadence, Needs and notebook-lead text match the note.
- Vault diff against `origin/master` shows only the intended spans changed (cadence, `bmu_id` field, lead, needs,
  overview word, description paragraph, publication-lag row); chart spec, chart words, raw feed and rows are
  untouched from review 1, which verified them (totals recomputed, 231 of 276 / 0 of 276 IDs, null row 3,589 / 3,588).

Summary: APPROVE; the cadence blocker and note-body major are fixed with accurate catalogue wording, all nits are
resolved, "transmission-connected" was rightly removed, and build, detector, mirror and screenshots are clean.
