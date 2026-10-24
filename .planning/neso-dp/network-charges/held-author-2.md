# Held Network charges pages: writer report, round 2 (2026-10-24)

These are fixes for `held-review.md` (APPROVE with nits on all three pages), applied under the seat's four rulings.

## Seat rulings

1. **Charging zones, the empty feature.**
   - `what_it_is`: ", one with no geometry" is cut. The page no longer mentions the empty feature anywhere, and there
     is no separate sentence about it ("if at all").
   - The sentence is now "Both files, last modified May 2022, contain 28 features and state WGS 84 coordinates in
     degrees." `what_it_is` is 57 words.
   - Note body: the bullet's closing sentence now says the site page gives NESO's 27 and the files' 28 in separate
     sentences, without linking them, and does not mention the empty feature. The measured facts about the empty
     feature stay in the note body.
2. **AAHEDC, `how_used[1]`.** It now reads "How far the final rate moved from its draft, financial years 2025 to 2027"
   (14 words). Silver has a Draft row only for 2025, 2026 and 2027; 2022 to 2024 are Final only.
3. **TNUoS, the shared clause on the two longer held lines.**
   - **`tnuos_tariffs_transmission_demand`:** "NESO dates each publication but not when each row appeared; the unmetered
     band's units conflict." (15 words)
   - **`tnuos_tariffs_onshore_local_circuit`:** "NESO dates each publication but not when each row appeared; some
     substation names end in whitespace." (16 words)
   - The review's suggested local-circuit line ("... end in spaces or tabs.") is 18 words, not 16, so it fails the
     budget. "Whitespace" covers the 73 trailing spaces and the 5 tabs in one word.
   - The first clause is now identical on all eight members and on AAHEDC.
4. **Other nits.**
   - **Nit 4, charging zones, applied:** "NESO calls the boundaries indicative; its charging documents prevail where the
     two disagree." This fixes the ambiguous "they" and adds no claim.
   - **Nit 6, TNUoS `facts.grain`, applied:** "Row key: financial year, stage, publication date, and zone, site, band or
     substation type" (14 words). The review's wording would be 15 words in the old frame, so I reframed it to fit.
   - **Nit 7, skipped:** "TNUoS is the charge that recovers the cost of the GB transmission network" would add a
     cost-recovery claim that NESO's catalogue text does not make (ruling 4).
   - **Nit 2:** no change; the review asked for none.

## Gates

- `cp` and `cmp` clean on all three notes. The vault notes are still CRLF on every line (274, 139 and 632).
- `parse_page_fields` and `anatomy_errors`: `[]` on all three. Every held line is 16 words or fewer (15, 15, 15, 15,
  15, 15, 15, 16).
- `gridflow-build --only` for `aahedc_tariffs`, `gis_gen_charging_zones_files` and
  `tnuos_tariffs_half_hourly_hh_demand`: all wrote, no errors.
- The detector returns `[]` on all three.
- Rendered text: 0 em or en dashes and none of the banned words (including held and hold). "geometry" does not appear
  on the charging-zones page.
- No new screenshots. The changes are short prose swaps of equal or shorter length, and the round 1 screenshots and the
  checker's showed no clipping.

## Defects

None new.
