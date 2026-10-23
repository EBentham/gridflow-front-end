# Held pages, Constraint management part 2: writer report, round 2 (2026-10-23)

All nine nits from `held-2-review.md` are fixed, in the `page:` blocks only; the note bodies are unchanged. Canonical notes were edited with the Edit
tool (CRLF on every line: 313/313 and 177/177), mirrored byte for byte to `C:\gridflow-wt\fe-neso-cm\vault\neso_data_portal\`, and `cmp` is clean
on both.

| Page | Build `--only` | Detector |
|---|---|---|
| `operational-transparency-forum-network-congestion-data` | `neso_data_portal/otf_network_congestion`: ok | `[]` |
| `voltage-requirement` | `neso_data_portal/voltage_requirement`: ok | `[]` |

Rendered text on both: 0 em or en dashes, arrows, middle dots or replacement characters, and none of the banned words. Every new phrase is present
in the built HTML. Builds print only the known vault-wide "Known issues" warning. I took no new screenshots because only short text changed. No
server was started this round.

## Fixes

| # | Field | Was | Now |
|---|---|---|---|
| 1 | congestion `how_used[0]` | "Forecast boundary limits set against the actual limit NESO later reported" | "Forecast boundary limits compared with the actual limit for the same week" |
| 2 | congestion `what_it_is` | "...leaves the date column undescribed, and the later rows carry a forecast only." | "...leaves the date column undescribed. Rows after the latest actual carry a forecast only." (own sentence, so it no longer reads as the dictionary's claim) |
| 3 | congestion `raw_feed.note` | "The file's name carries the upload date." | "The file's name carries a date and changes with each upload." |
| 4 | congestion `related[0]`, `related[1]` | "under other codes" | "with different boundary codes" |
| 5 | voltage `what_it_is`, `summary` | Monday to Friday nights stated in the page's own voice | `what_it_is`: "NESO describes the plans as covering the next weekend and the following Monday to Friday, and says the actual requirement is likely to change" (55 words). `summary`: "...in each voltage group, in its week-ahead plan." (no night claim) |
| 6 | voltage `held` | "NESO leaves unstated which nights each range covers, each group's area and when rows were issued." | the checker's line: "NESO leaves unstated what each range covers (some run backwards), each group's area and issue times." (16 words, budget passes) |
| 7 | voltage `raw_feed.note` | "Three PDFs (an introduction, a deep dive and the group map) stay in bronze; two shown." | "Three PDFs stay in bronze; the deep dive is not listed." |
| 8 | voltage `facts.cadence` | "each upload is the whole file, earlier plans included" | "Weekly, as NESO lists it; the file holds earlier plans as well" |
| 9 | voltage `related[0]` | "What NESO spent on voltage actions, the cost side of these plans" | "What NESO spent keeping voltage within limits, by voltage group" |

## Side effects

- The voltage `what_it_is` drops "it may optimise further closer to the time" to stay inside 60 words. The NESO caution that the requirement is
  likely to change is kept.

## Defects

Unchanged from `held-2-author.md` (the checker reproduced all of them).
