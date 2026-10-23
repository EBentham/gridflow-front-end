# Held pages, Balancing costs part 2: writer revision 2 (2026-10-23)

All nine nits from `held-2-review.md` are fixed, and the volume and skip rates note bodies are updated for the 16 October
recaptures. Canonical notes in `C:\gridflow-wt\vault-neso-bc\30-vendors\neso-data-portal\datasets\` (Edit tool, CRLF on every
line: 379/379, 1023/1023, 909/909) are re-mirrored to `C:\gridflow-wt\fe-neso-bc\vault\neso_data_portal\`, and `cmp` is clean on all
three. Diff against `origin/master`: volume +55 -6, monthly +81 -0, skip rates +104 -9 (page blocks plus the body spans
below; nothing else touched).

| Page | Build `--only` | Detector | Rendered text sweep |
|---|---|---|---|
| `daily-balancing-volume-balancing-services-use-of-system` | `daily_balancing_volume`: ok | `[]` | 0 dashes, no banned words, £ intact |
| `bsuos-monthly-forecast` | `bsuos_monthly_forecast_actual_sum`: ok | `[]` | same |
| `skip-rates` | `skip_rates_behind_constraints_bmu`: ok | `[]` | same |

The only build warning is the known vault-wide "Known issues" caveat one. No server was started in this revision. My
part 1 server (PID 33488, port 9923) had already been stopped by its PID. The changes are word-level, so the part 1
screenshots and overflow measurements still describe the layout; I did not retake them.

## The nine nits

| # | Field | Change |
|---|---|---|
| 1.1 | volume `page.summary` | "in eight categories such as ..." becomes "in eight columns, such as energy imbalance, reserve and constraints." |
| 1.2 | volume `page.what_it_is` | "NESO's dictionary describes `SETT_DATE`, titled settlement date, as a payment date." |
| 2.1 + 2.2 | monthly `page.raw_feed.note` | "NESO's `package_show`, then each file whole unless `last_modified` is unchanged (a few shown). Only forecast summary files with a valid UTF-8 header reach silver; everything else is bronze only." (29 words). This covers the 22 forecast-summary files (Mar_20 among them) that share the £ fault, without dates or counts, and no longer reads as if only the archive and PDF are bronze. |
| 2.3 | monthly `page.raw_feed.commands[1].comment` | "forecast summary only; rows not shown" (6-word limit; the suggested wording was 7) |
| 3.1 | skip `members[skip_rates_in_merit_psa].differs` | "a more targeted measure" (NESO's words) replaces "a narrower measure" |
| 3.2 | skip `members[skip_rates_behind_constraints_bmu/_cons].held` | "NESO's dictionary and methodology slides disagree on what the skip rate is a percentage of." |
| 3.3 | skip `page.summary` | "...it passed over, stage by stage, by unit and by technology." (the grain is dropped) |
| 3.4 | skip `page.related[0].note` | "Elexon's accepted bids and offers: the actions taken instead of skipped volume" (the review's 12-word version counts 13 by the build's whitespace rule and failed; this one is 12) |

## Note body updates (16 October recaptures)

**Volume** (`daily-balancing-volume-balancing-services-use-of-system.md`):
- "Bronze at activation": a new bullet records the 2026-2027 recapture
  (`daily_balancing_volume/2026/10/16/raw_20261016T200136Z_e781da74-..._edf40a60.csv`: 639,451 bytes, 9,306 rows to 2026-10-11,
  `last_modified` 2026-10-16T06:39:49). The old bullet now reads "At activation, one capture per resource". The table is
  labelled as the activation state, so its rows stay.
- **New fact, checked by comparing the two captures by date and period:** every earlier key is kept and 480 rows are new, but
  **124 rows on four dates (2026-09-03, 09-04, 09-15, 09-28) changed value**, with no run label. The header also dropped the
  unit brackets (`Energy Imbalance MWh`, not `Energy Imbalance (MWh)`). The "one exact header (H-DV)" line is qualified, and
  the Cadence paragraph now answers its own question: a weekly update rewrites the current-year file and restates earlier
  periods. The new TODO asks which settlement run each restatement reflects.
- The page needs no change: its hold line ("not labelled with a settlement run") is, if anything, strengthened.

**Skip rates** (`skip-rates.md`):
- "Where each family stands": every resource captured on 2026-10-08, "and seven again on 2026-10-16".
- Gotchas, vendor reissues: "at most two captures of each file", "the one pair compared so far shows no silent revision".
- Cadence: the "captured once" paragraph is replaced with the seven recaptures and their row counts and ends. Checked by
  comparing the two captures: the summary and the stage 5 PSA technology file only append (every earlier key identical; 2,304 and
  1,459 new rows). The DSF excess repeats are unchanged (7,830 and 192). The September 2026 and March 2026 files have one capture.
- The two "Eligible ... one capture" lines now say the rows come from the 2026-10-08 capture and that the 2026-10-16 capture
  adds a second silver file (silver checked: one `..._20261016_run...parquet` per recaptured family).
- Not added: the checker's extra coverage detail (August 2026 one day short, October to 15 October). It needs its own check and
  is not a recapture fact. It is left for the seat in Defects.

**Monthly forecast:** no body change; "captured once, on 2026-10-08" is still true.

## Defects (for the seat to paste)

- **Data finding, daily BSUoS volume:** NESO's 2026-27 volume file restates published values between weekly uploads (124
  rows on 3, 4, 15 and 28 September 2026 changed between the 8 and 16 October captures) and renamed its header (unit brackets
  dropped). This supports the no-run-column hold and means a future record cannot assume an append-only file or a fixed header.
  The sibling cost file (`daily_balancing_costs`, also recaptured on 16 October) very likely does the same; I did not check it,
  as it is outside this package. Worth logging in gridflow's backlog and on the vault remediation page.
- **Skip rates coverage (from the review):** the All BM and PSA August 2026 files are one day short of the month's five-minute
  stamps (day not identified). Not on the page; not yet in the note.
- Unchanged from part 1: the package registry status reads `eligible` on all three packages; the manifest leads and members are
  correct.
