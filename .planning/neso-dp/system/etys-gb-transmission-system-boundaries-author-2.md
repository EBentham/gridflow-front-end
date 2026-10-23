# ETYS GB transmission system boundaries: writer report, round 2

These are fixes for the checker's review `etys-gb-transmission-system-boundaries-review.md` (REVISE: 2 major, 2 nit).
The seat accepted the hold (PROXY-SOURCED).

## Fixes

1. **Major, `page.how_used[1]`.** The line now reads "Look up a boundary by its name, such as B6 or B7". It no longer
   says the file locates boundaries in NESO's constraint reporting. My round-1 report line "It claims no mapping" is
   withdrawn for that bullet.
2. **Major, Known issues contradiction.** The first bullet now reads "Treat the shapes as opaque". It says the file
   holds one name per feature (measured, pointing to Catalogue facts), and it claims neither that the lines are
   geographically correct nor that they are the boundaries in NESO's constraint tables. The Overview's "gridflow
   claims no geometry meaning" stays, as the checker suggested.
3. **Nit, 2024 against mar25.** `page.what_it_is` now says: "Its title says 2024; the file is named mar25, and NESO does
   not say why."
   - The quoted phrase is attributed on its own ("... path data" for the transmission system boundaries used in
     ETYS 2024, NESO says).
   - "shown on its Interactive Webmap" and "not latitude and longitude" were dropped to stay inside the 60-word
     budget.
   - `page.summary` now reads "names and paths, which NESO lists for ETYS 2024", so 2024 is not stated as fact.
4. **Nit, source of the B6 and B7 line.** The Known issues bullet now gives the source of `related[0]`: the thermal
   constraint costs note (`@30-vendors/neso-data-portal/datasets/thermal-constraint-costs.md`), quoting NESO's
   Operational Transparency Forum slides of 24 June 2026 (document 383631, with its link, "Transparency | Network
   Congestion" table, `B6 (SCOTEX)`, `B7 (SSHARN)`). It also says plainly that the deck is not evidence that this
   file's `B6` and `B7` are the same boundaries. `related[0]` is unchanged and now agrees with `how_used`.

## Gates

- The canonical note is CRLF (168 CRLF out of 168 lines). The mirror is copied and `cmp` passes.
- `gridflow-build --only neso_data_portal/etys_boundaries_files` wrote the page with no errors. The repo-wide warning
  that 35 caveat lines were dropped predates this page.
- The detector returns `[]`. The rendered text has no em or en dashes.
- No screenshots this round: the coordinator said not to start a server. The changes only shorten two prose fields
  and one list item; the round-1 and checker screenshots showed no clipping.

## Defects

None new.
