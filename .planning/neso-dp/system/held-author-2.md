# Held System pages: writer report, round 2 (2026-10-23)

These are fixes for `held-review.md`: DNO and SOP were APPROVE with 6 nits each; Stability Pathfinder was REVISE with 1
major and 3 nits. The DNO coordinate-system wording follows the seat ruling (PROXY-SOURCED).

## Stability Pathfinder

1. **Major: what the utilisation report holds.**
   - `page.what_it_is` now says the two reports give, "for every unit and settlement period", the declared
     availability and "its instruction code, mostly none, with any start or cease times and an `Inertia` figure of no
     stated unit". It is 60 words.
   - `family.members[1].differs` now reads "Every unit and settlement period: instruction code, mostly `No`, start or
     cease times, `Inertia`". It is 14 words.
   - The summary now says "any instructions its control room gave them".
   - Evidence: the checker's counts (for example 123,929 of 123,987 rows are `No` in the 2026-2027 file) and the note's
     "`No` rows carry an inertia figure".
2. **Nit, `how_used[1]`.** It now reads "Compare with NESO's Stability Y-1 utilisation report". The inertia-estimate
   pairing is gone.
3. **Nit, `related[2]`.** It now reads "Price of inertia bought through Balancing Mechanism offers, not by contract".
   `related[0]` now says NESO's GB inertia estimate "leaves Pathfinder units out". The source is the system inertia
   note: "The vendor states the dataset does not include the contribution of Stability Pathfinder units."
4. **Nit, note body.** "Six of the eight captures" is now "Six of the first eight captures (2026-10-08)".

## DNO licence area boundaries

1. **Seat ruling on finding 1.**
   - "in British National Grid coordinates" is cut from `what_it_is`, so the page names no coordinate system.
   - The request lines stay.
   - In "Files by disposition", the note's sentence about the CRS is replaced. It now says the page prints NESO's
     download requests as plain text, which carry no file content (seat ruling, PROXY-SOURCED, consistent with ruling
     477), and that the page names no coordinate reference system. The note's "does not contain ... coordinate
     reference systems" is true again.
2. **Nit, editions.** It now reads "in two editions, `20200506` (with a PDF map) and `20240503` (with a PNG map)".
3. **Nit, disclaimer.** It now reads "Western Power Distribution first shared them, with a warning that they are
   probably a little outdated".
4. **Nit, held line.** It now reads "Western Power Distribution supplied the boundaries; NESO does not say it is
   authorised to license them." It is 16 words.
5. **Nit, raw-feed note.** It now ends "the 2024 edition's three are listed" (28 words). The note already says "each of
   six files".
6. **Template.** This is a seat item; no change.

## System operating plan

1. **Nit, date on the notices.** The date is gone. The line now reads "NESO's package notes carry quality and
   publishing-difficulty notices."
2. **Nit, technology figures.**
   - `summary`: "... margins, and availability and output by technology, in MW" (22 words).
   - `what_it_is`: "expected availability and output by technology and interconnector".
   - `how_used[1]`: "Expected availability and output by technology and interconnector, cardinal point by cardinal point".
3. **Nit, raw-feed note.** It now reads "one `package_show` per command, then the table's whole datastore dump, kept only if
   its body changed, or each PDF unless its `last_modified` is unchanged" (28 words).
4. **Nit, related.**
   - The Quick Reserve link is dropped, because it is a separate product.
   - **Not applied:** switching `historic_generation_mix` and `embedded_wind_solar_forecast` to hyphenated slugs. Those
     keys are the pages' own slugs:
     - They are listed in the page set's `names` and in the landing's `start` list.
     - The main repo's built `historic_generation_mix.html` is a full dataset page (title "GB generation mix by fuel"),
       not the `redirect.html.j2` output.
     - Nine approved notes already link `neso_data_portal/historic_generation_mix`.
     - `historic-generation-mix` and `embedded-wind-and-solar-forecasts` are not in the page set.
5. **Nit, note body "Hold question" and "Quality notes".**
   - "Hold question" now says every target "in the first capture (2026-10-08)" precedes that capture.
   - "Quality notes" now says "up to each capture's date (and, in the second capture, one target past it)".
6. **Nit, coverage table.** The intro and column header now say "first capture (2026-10-08)". The "every target
   precedes" paragraph under it is scoped the same way.

## Gates

- The three notes are still LF, as round 1 explains. Each is mirrored, and `cmp` is clean on all three.
- `parse_page_fields` and `anatomy_errors`: `[]` on all three. `what_it_is` is 55, 60 and 59 words; every held line is
  16 words.
- `gridflow-build --only` for `gis_dno_license_areas_files`, `stability_pathfinder_availability_report` and
  `system_operating_plan`: all wrote with no errors.
- The detector returns `[]` on all three.
- Rendered text has 0 em or en dashes, none of the banned words (including "held"), and no "British National Grid",
  "EPSG" or "October 2026".
- No screenshots this round: I was told not to start a server. The changes are prose of similar length; round 1 and
  the checker's screenshots showed no clipping.

## Defects

None new. The round-1 NESO defects stand, and the checker confirmed them.
