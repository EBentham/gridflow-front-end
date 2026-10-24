# Embedded register: author report, round 2

Answers `embedded-register-review.md` (REVISE: 2 majors, 4 nits) under the seat's rulings. Text-only changes in the
canonical note; chart spec, frame select and notebook cells unchanged (series re-distilled with an unchanged digest,
sample and notebook untouched).

**Gates:** `gridflow-build --only neso_data_portal/embedded_register` passes; detector `[]`; 0 em dashes in the built
page; mirror `cp` + `cmp` identical; note CRLF throughout (482 of 482 lines).

## Fixes

1. **Major, sign (ruling 1).** The sign is now our reading wherever it appears on the page:
   - guide `mw_increase_decrease`: "MW to connect or be removed (NESO); negative read by us as a removal";
   - chart caption: "One negative 5.5 MW entry is read as a removal (70 + (-5.5) = 64.5) and netted." (the worked
     case, `PRO-000902`: 70.0 connected, -5.5, 64.5 cumulative, the same in both captures);
   - wind key: "`Wind Onshore`, net of one negative 5.5 MW entry (Paul's Hill), read as a removal.";
   - frame caption: "16 October file: a staged pair, a negative entry, Gates 1 and 2, `NGET`'s project."
   No line calls -5.5 a plain decrease. "At a future date" is dropped from the guide line (it sat beside a 2022 date).
2. **Major, running total (ruling 2).** TEC phrasing in both places:
   - guide `cumulative_total_capacity_mw`: "NESO: total across all stages; in these rows, the running total to this
     stage" (identical to the TEC page);
   - how-used: "Sum `mw_connected` and `mw_increase_decrease`; in these rows the cumulative is a running total."
     (the checker's longer suggestion is over the 14-word budget).
3. **Nit, dates on the page.** Guide `mw_effective_from`, where a reader uses the dates: "Contracted date (NESO);
   16 October file: 129 already past, one 40 MW row blank" (14 words, dated to the file).
4. **Nit, stale and unscoped counts (body).** Gotcha 5 now scopes "215 blanks on `Built` rows, 2 dated `Built` rows"
   to the 2026-10-08 capture and gives the 16 October figures (216 and 1, `PRO-000902`), naming why: `PRO-000886`
   moved its 49.95 MW from contracted to connected and lost its 2022-02-15 date (reproduced in silver). The profile
   paragraph's "All 215 blank effective dates" now opens "In this capture".
5. **Nit, sign in the body.** The `MW Increase / Decrease` dictionary entry and gotcha 4 now say NESO states no sign
   and that removal is our reading, citing `PRO-000902` (70 + (-5.5) = 64.5) in both captures.
6. **Nit, mixed key.** "Any plant type naming several, joined by `;`: mostly storage with solar or wind, some with
   `Demand`."

Not done: new screenshots. Every change is wording in lines that already render at all four widths (the longest new
line, the wind key note, is shorter than the round-1 mixed note it sits beside).

## Defects

None new. The round-1 items stand: the `NGET` row in a register NESO calls Scottish; 129 past-dated rows and one
undated 40 MW non-built row against the dictionary comment; no capture of any file between 8 and 16 October 2026.
New observation for the vault only (not a defect): between the two files `PRO-000886` moved 49.95 MW from
`MW Increase / Decrease` to `MW Connected` and its date went blank, consistent with NESO's comments on both columns.
