# Balancing Reserve requirement forecast: checker re-review

Re-check of `balancing-reserve-auction-requirement-forecast` after the writer's round 2
(`balancing-reserve-auction-requirement-forecast-author-2.md`). Checker, 2026-10-18.

## Verdict: APPROVE

0 blockers, 0 majors, 0 nits on the page. The four template items stay with the seat.

## Majors from round 1

1. **No one-day claim: fixed.** The page now says only that NESO replaces the day-ahead file daily:
   `what_it_is` "the day-ahead refinement, in a file NESO replaces daily"; `notebook.lead` "...the newest capture,
   because NESO replaces the file daily and a dated `query()` finds rows only for the day it holds" (a statement about
   what a dated query can return, not about the file's contents); lead member `differs` "Day-ahead forecast; NESO
   replaces the file daily". Built page: zero hits for "holds one", "next service", "one per day".
2. **EAC join bullet: fixed and correct.** `how_used[1]` reads "To join EAC results, convert
   `service_window_start_time` from UK local time to UTC." Re-derived against `eac_results_summary.delivery_start`
   (UTC): for the 9 October requirement, converting the local label by the one-hour BST offset matches 48 of 48 windows
   with a mean absolute difference of 2.6 MW to cleared `PBR`; reading the label as UTC gives 43.0 MW. The bullet no
   longer implies a window-label join the EAC table does not have.

## Nits from round 1

- 3 (medium-term held line): now "Its table includes the archive file, and NESO does not say when archived forecasts
  were published." Grammatical after "Rows not shown:", no longer reads as a separate archive member, still true to the
  hold question (no publication instant). Fixed.
- 7 (caption, EFA): caption adds "from 23:00 the evening before"; key note "Steps only at the four-hour EFA block
  edges from 23:00 this day: 200 to 600 MW." Data agree (steps at 03:00, 07:00, 11:00, 15:00, 19:00). Fixed.
- 8 (hash prefix): `raw_feed.note` says the name's hash prefix can change, matching the note body's "can change".
  Fixed.
- 9 (`service_window`): "spring drops `5`, `6`, autumn adds `5x`, `6x`" is true in the archive: 46 windows without
  `5`/`6` on 2024-03-31, 2025-03-30 and 2026-03-29; 50 windows with `5`, `6`, `5x` on 2024-10-27 and 2025-10-26. Fixed.
- Body paragraph reflow: done, wording unchanged.
- 4, 5, 6 and 10 (768 frame shows no MW column until unfolded; unfolded frame scrolls sideways; notebook preview splits
  names; series file stamps local labels with `Z`) are template items for the seat, as the writer reported. Not page
  findings. I confirmed none of them reaches a reader as a wrong statement on this page.

## Regression checks

- `gridflow-build --only neso_data_portal/br_auction_requirement_fc_da`: exit 0, page written, artefact digest checks pass
  (series, sample and notebook files untouched).
- Detector at `C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs
  --json` on the built page: `[]`.
- `cmp` canonical note against the mirror: identical. Vault diff against `origin/master` shows only the intended changes
  (the `page:` block, `updated`, the two body paragraphs).
- Built page greps: no em or en dashes, middle dots, arrows, "locally", "our", "live", "now", planning words.
- Looked at a true 390 px viewport after the edits (what it is, how it's used, caption, chart key notes, raw feed note,
  member lines and held lines): `scrollWidth` 390, nothing clipped or overlapping.
- The server I started on 9961 is stopped. I did not touch 9670.
