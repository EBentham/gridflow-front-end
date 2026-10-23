# OBP non-BM physical notifications: writer report, round 2 (2026-10-23)

Every finding in `obp-non-bm-physical-notifications-review.md` is fixed (3 majors, 6 nits), plus the remaining
single-capture wording the seat pointed to.

| Gate | Result |
|---|---|
| Canonical note | edited with the Edit tool; CRLF on all 257 lines; vault diff now 142 insertions, 17 deletions; no "single capture" or "one capture" left |
| Mirror | copied and `cmp` clean |
| `gridflow-build --only neso_data_portal/obp_physical_notifications` | ok (no error lines; only the old vault-wide "22 Known issues lines dropped" warning) |
| Detector | `[]` |
| `plot_alt` in raw HTML | reads "from -17.03 (03:30 to 05:00, 14:00 to 16:00) up to 15.97 from 18:00 to 18:30" |
| Notebook | not rerun: no cell changed (only `lead` and `plot_alt` text) |
| Series, sample | unchanged: the spec and select did not change; the build's digest checks pass |
| Screenshots | not retaken. The seat said to start no server; the guard also halted a PowerShell server start. Round 1 shots stand; the changes are text plus the key legend losing its duplicate code |
| Servers | none running from me; the round 1 server on 9985 is gone (nothing listens there) |

## Fixes

| # | Finding | Fix | Evidence |
|---|---|---|---|
| 1 | Major. Vintage lines stale against the second capture (`Two clocks` 1 and 2, Known issues) | `published_at` and `available_at` are now "one value per capture": 2026-10-08T11:01:24.343784Z on the first capture's 495,086 rows, 2026-10-16T20:31:22.674649Z on all 523,890 of the second; `_latest` carries the newer, so an as-of query before 2026-10-16T20:31:22Z sees no row there. "(one capture exists)" became "beyond the two captures". `capture_written_at` gives both values (11:14:57Z, 20:42:39Z). The Known-issues bullet gives both `last_modified` values | silver: one `available_at` and one `capture_written_at` per file, values as stated |
| 1 (seat) | "single capture" (Scope), "one capture" (cross-capture TODO), "had one capture ... when this was written" (Cadence) | Scope: "in the first capture, of 2026-10-08 (the second ... follows below)"; TODO: "two captures eight days apart show a pure append ..., which does not prove that later amendment or deletion never happens"; Cadence: "gridflow has two captures". Also dated two undated first-capture facts: the 150 late starts (692 in the second capture) and "on the first capture" in Files | silver: 692 windows start after `published_at` in the 2026-10-16 file |
| 2 | Major. "48 whole half-hours" on 26 October 2025 | Now: `EDFE-8`, `EDFE-11`, `EDFE-21` have 119, 50 and 95 windows, each unit's windows covering exactly 24 hours (2025-10-26T00:00 to 10-27T00:00), which fits UTC but cannot exclude local time alone | reproduced: windows 119/50/95, of which 1,800 s 6/47/15, each summing to 86,400 s. My round 1 check counted 24-hour coverage and I misreported it as 48 half-hours |
| 3 | Major. `plot_alt` used window starts for a plot that draws to window ends | "from -17.03 (03:30 to 05:00, 14:00 to 16:00) up to 15.97 from 18:00 to 18:30" | the plot draws start to end; the last -17.03 windows start 04:30 and 15:30 and last 1,800 s |
| 4 | Nit. `how_used[0]` "minute by minute" | "in windows down to a minute" | windows 60 to 1,800 s |
| 5 | Nit. `what_it_is` read as proof of UTC for the whole file | "Times are UTC, NESO says; the text has no zone marker and is not UK local time on 29 March 2026, holding 01:00, which UK clocks skipped." To stay within 60 words I dropped "and validated" (gate closure kept) and "of it" | |
| 6 | Nit. "in absolute values" dropped from NESO's phrase | `how_used[2]`: 'OBP instructions: NESO gives their target MW as "power from PN in absolute values"' (14 words); related note: 'OBP instructions; target MW is "power from PN in absolute values" (NESO)' (12 words) | instructions field info, `Target MW` |
| 7 | Nit. "UK time here" | "UK time on UK machines" | as on the sibling page |
| 8 | Nit. Key showed "GSET-07 GSET-07" | `codes` removed from the three key entries (it is optional, `page_fields.py:266`); the rendered page has no `ds-key__c` element left | |
| 9 | Nit. Note leftovers | Cadence TODO "the rolling window length" became "whether old rows are ever dropped"; the 400,690 counts (lines 146, 243) now say "2026-10-08 capture" with 416,661 of 523,890 for 2026-10-16; the Sentinels zero and negative counts and the Known-issues zero counts are dated "2026-10-08 capture" | silver: 416,661 windows of 1,800 s in the newer file |

## Unchanged from round 1

Chart, frame, notebook cells, raw feed, commands and related targets. Defects as in `-author.md`.

Summary: all 3 majors and 6 nits fixed and the single-capture wording removed; note mirrored and `cmp` clean, build ok, detector `[]`, notebook not rerun (no cell changed).
