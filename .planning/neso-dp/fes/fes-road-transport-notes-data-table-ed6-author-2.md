# FES road transport notes (ED6): writer's report (round 2)

Fixes for the round 1 review (REVISE: 1 major, 6 nits), following the seat rulings. `type: none` is kept.

**Gates:**
- **Build:** `--only neso_data_portal/fes_ed6_road_transport_notes` has no errors.
- **Detector:** `[]`, with 0 em dashes in the page.
- **Mirror:** `cp` then `cmp` shows it identical.
- **Line endings:** the note stays LF (0 CRLF).
- **Artefacts:** the frame selection is unchanged, so the sample and notebook artefacts are unchanged.

## Major: the rows-to-ED5 claim

- **Re-derived from silver**, comparing ED6 `category` with the distinct same-edition ED5 labels in the matching column (labels only, no ED5 values):
  - matches: 24 of 27 (2023), 23 of 27 (2024), 24 of 26 (2025) and 24 of 26 (2026);
  - unmatched: `# Vehicles - Hydrogen` under `Fuel` in every edition (the label is in ED5 `data_item`);
  - unmatched: `V2G Maximum Capacity available at Peak` (2024 to 2026);
  - unmatched: `# Vehicles` and `Reference data` (2023, 2024).

  This agrees with the checker and with the note's own per-column counts (22+1+1, 21+1+1, 21+1+2, 21+1+2).
- **`what_it_is`:** now reads "Each row gives an ED5 column name (`Data Item`, `Fuel` or `Peak/Annual/Minimum`), a value NESO names under it, and NESO's note. Most values match a same-edition ED5 label: 24 of 27, 23 of 27, 24 of 26 and 24 of 26, 2023 to 2026." (58 words). "one of its values" is gone.
  - The per-edition counts follow the seat ruling.
  - To make room I dropped "often with a formula of other items" and the Ten-Year Outlook sentence. The `edition` guide line still says 2026 is the Ten-Year Outlook file.
- **`record.fields.category`:** "A value NESO names under that column; most, not all, match an ED5 label". The trailing-space clause is gone (nit 7).
- **`facts.grain`:** "One note per column name and value NESO lists, per edition". It no longer says "ED5 column and value", and ED5 is no longer used before it is introduced.
- **`how_used[0]`:** "Read what a road transport data item counts or measures, and NESO's formula".
- **`how_used[1]`:** "Read NESO's definitions of `Peak` and `Annual`, which the 2025 and 2026 files give". This scopes the item to the editions that have an `Annual` note.
- **`related[0]`:** "The road transport table these notes support", which is NESO's own relation ("a file supporting those data tables").
- **Body, "Join to ED5":** added the totals and the four unmatched labels by edition, dated 2026-10-24. The `TODO: verify` is kept.

## Nits

1. **Hydrogen guide wording (`record.fields.column_name`):** "ED5 column name; NESO files the `# Vehicles - Hydrogen` count under `Fuel`".
2. **V2G and HGV expanded once:** `how_used[2]` now reads "... such as vehicle-to-grid (V2G) scope" (the first use of V2G in page prose). `record.fields.description` reads "NESO's note; 2025's V2G notes add heavy goods vehicles and buses at depots". "at depots" covers both NESO wordings ("depot charged" and "parked at the depot").
3. **Body revision list:** it is now marked as not exhaustive: "the main revisions are below; smaller edits (a capital letter, a typo fixed, "including" to "includes", "is" to "would be") are not listed".
4. **`package_show` added to `raw_feed.requests`**, matching ED4's shape:
   - The requests are now `package_show?id=fes-road-transport-notes-data-table-ed6` plus the 2023, 2025 and 2026 CSVs. The 2024 file was dropped for the four-request cap.
   - The note reads "From NESO's CKAN portal: one `package_show`, then four CSVs, each downloaded whole unless its `last_modified` is unchanged. Shown: 2023, 2025 and 2026; edition comes from the file name." This is word for word the ED4 note.
5. **ED1 related note:** "2023 and 2024 notes: reference data not used in ED1's Peak/Annual/Minimum". NESO's text is "Data is not used in the calculation of Peak/Annual/Minimum in ED1".
6. **Trailing-space line:** dropped from the `category` guide, since no frame row shows a trailing space.

## Not changed

- `type: none` (seat ruling).
- The frame rows, caption, `record.select` and notebook cells.
- The template seat items from round 1 (the long text column folds at every width, the `none` reason is not rendered, the generic hero scene).

## Defects (pasteable)

- **NESO FES road transport notes (ED6) against ED5 (labels only, same edition):**
  - `# Vehicles - Hydrogen` sits under `Fuel` in ED6, but ED5 has it as a `data_item` label.
  - The ED6 `V2G Maximum Capacity available at Peak` has no ED5 label of that spelling (2024 to 2026).
  - The 2023 and 2024 ED6 values `# Vehicles` and `Reference data` match no ED5 label.

  This is vendor labelling, not a gridflow code defect. It is recorded in the note's "Join to ED5" section, and the `TODO: verify` remains.
