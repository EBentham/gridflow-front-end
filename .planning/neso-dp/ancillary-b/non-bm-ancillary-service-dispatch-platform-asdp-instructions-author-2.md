# ASDP dispatch instructions: writer round 2 (2026-10-18)

Answers `non-bm-ancillary-service-dispatch-platform-asdp-instructions-review.md` and the seat's rulings on it. All 3
majors and 3 nits are fixed. I changed only the canonical note (page block and two body spans, CRLF kept on all 569
lines) and mirrored it (`cmp` clean). The chart spec and notebook cells did not change, so the series and notebook did
not need re-running; the build's digest check confirms the committed artefacts still match.

| Gate | Result |
|---|---|
| `gridflow-build --only neso_data_portal/asdp_instructions` | ok (the one round-2 run that failed was `what_it_is` at 61 words; trimmed to 60) |
| Detector | `[]` |
| Rendered page | 0 em or en dashes; none of live, now, yet, soon, planned, held, locally, "since 20" |
| Screenshots | `asdp-instructions-shots\r2-*` (1440, 768, 390 in six slices through a 390 px iframe). Nothing clipped or overlapping. My 9983 server is stopped; 9670 not touched |

## Majors

1. **`what_it_is`, time spelling scoped by period (seat ruling).** Now: "Times are text: ending in `Z` in 2020, no zone
   marker from 2021." No claim that either form is UTC or UK local time. The frame field's "not UK local time here"
   stays scoped to the rows shown, as the review allowed.
2. **Chart caption says why March 2022 and scopes the bursts (seat ruling).** Now: "Silver
   `neso_data_portal/asdp_instructions`, instructions per start date as written, March 2022: picked as the month with
   most STOR instructions. That month, Fast Reserve has rows daily and STOR comes in bursts. Rows without a start are
   not counted." Re-checked: by start month, STOR is 403 in March 2022, then 179 (June 2021) and 114 (April 2022). The
   yearly fall is in the notebook lead ("STOR falls from 776 in 2022 to 26, 6, 1 and 1"), which the notebook's per-year
   table shows, and in the note body (Service vocabulary: "By start year (2020 to 2026, rows with a start), STOR is
   122, 680, 776, 26, 6, 1 and 1"). To fit the lead's 35 words I cut "so no clock is assumed": "cut from the text as
   written" still says it.
3. **Body sentence on the other spring changes corrected.** Reproduced: on 28 March 2021 the cease columns have 1 row in
   01:00 to 01:59 (entry 5574) and on 30 March 2025 they have 6 (entries 54370 to 54375); 27 March 2022, 26 March 2023
   and 31 March 2024 have none in any column; starts and dispatch stamps have none on any of those five dates. The
   paragraph now says the check narrows the clock for three files: the March 2026 body (starts and stamps, 17 each in
   the skipped hour), and the March 2021 and March 2025 bodies' cease columns. The other three test nothing. The TODO
   stays open. The page says nothing about these other files.

## Nits

4. **RDP times in the guide.** `instruction_start_date_time`: "Ramp-up start (RDP: dispatch sent); no zone marker, and
   not UK local time here". `instruction_cease_date_time`: "Cease ramp-down end (NESO; RDP: when the cease was sent), as
   written". Both follow NESO's field info in the note's Units table.
5. **`what_it_is` universal.** "Each row gives" is now "Most rows give". To stay within budget, "NESO publishes an
   instruction once its provider confirms it" became "NESO publishes instructions once providers confirm them".
6. **`mw`.** "MW dispatched, as NESO states it; NESO states no sign".

## Defects

No new ones. The round 1 defects stand: the September 2020 gap in `EntryID`, and two seat items for the template
(`time_text` is parsed strictly before filters; no weekly or monthly bucket). The body now records the clock evidence
for three files instead of one.
