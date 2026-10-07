# entsog/gas-quality: re-review

Checker: Sonnet 5.5 · high, 2026-10-07. Answers `gas-quality-author-2.md` against `gas-quality-review.md` (2 majors, 7 nits).

## Verdict: APPROVE

Both majors are fixed and reproduce; every nit the writer took is correct; nothing regressed. No findings above nit, and no new findings.

## Majors

1. **`record.fields.timestamp_utc`: fixed.** The line now reads "Gas-day start from `periodFrom`, in UTC; placeholders send an earlier one" (rendered on the page). Reproduced in silver: `entsog/gcv` has 56 rows at 04:00 UTC (valued) and 42 at 03:00 UTC, and the 42 are exactly the `is_na` 1 rows (placeholder hour set is `['03:00']`).
2. **`gcv.md` "Repeated values": fixed.** The bullet now says Interconnector's six rows (13 to 18 Sep) each carry their own `lastUpdateDateTime`: 6 rows, 6 distinct stamps in silver. For National Gas TSO it says gas days 14 and 15 Sep share 2026-09-18 15:54:29 UTC and 18, 19 and 20 Sep share 2026-09-23 17:02:50 UTC, with the value changing from 11.6429 to 11.6927 and 11.6136, and reads the stamp as a batch time. Silver: National Gas TSO has 11 distinct stamps over 14 gas days (GNI 14; Interconnector 14 over its 28 rows, entry and exit sharing a stamp per day). The "re-sent, not one record" inference is gone for National Gas TSO. The wobbe and methane notes' repeated-value bullets are about Interconnector only and stay correct.

## Nits

- **Key note, `bacton_iuk_entry`** ("Interconnector's report; within 0.02 of National Gas TSO's except 14.253 on the 20th, sent `Confirmed`."): accepted. Interconnector's 20 Sep row is `Confirmed`; putting it on the value, not the whole report, is right because 15 Sep is `Provisional`. Wraps cleanly at 1440 and 390.
- **`differs` for methane, hydrogen, oxygen**: "only" removed and the exit zero stated; the exit is 0.0 on every row of all three. Wobbe keeps its "only", backed by the operators' own placeholder remarks. Accepted.
- **Register units bullet** in `gcv.md`: reproduced from `operator_point_directions` silver: `MJ/Sm3` for National Gas TSO at ITP-00005 exit, ITP-00207 exit and ITP-00090; `kWh/Nm3` for Interconnector and GNI (GNI's remark cites ISO 13443:1996(E)); `kWh/m3(n)` for BBL company. Accepted; page unchanged, as suggested.
- **`summary`** ("Daily gross calorific value and methane content at Bacton and Moffat, plus Wobbe index, hydrogen and oxygen at Bacton, from ENTSOG."): true (GCV and methane values exist at Moffat only for GNI; the other three come only from Bacton IUK). Accepted.
- **`is_cmp_relevant`**: CMP now expanded. Accepted.
- Overlapping chart lines and the folded frame at 390 px: template matters for the seat, not findings, as the coordinator ruled.

## Regression checks

- `gridflow-build --only entsog/gcv`: succeeds, `wrote: data-sources/entsog/gas-quality.html`; no over-budget field; artefact digests pass (series, sample and notebook untouched).
- `detect.mjs --json` (absolute path) on the page: `[]`.
- `cmp` against the vault worktree notes: byte-equal for all five (`gcv`, `wobbe_index`, `methane_content`, `hydrogen_content`, `oxygen_content`). The four non-lead notes are unchanged against the first review.
- Rubric greps on the rendered text (`locally`, `held`, `our`, `since 20`, `% of`, `live`, `now`, `yet`, `soon`, `planned`, `coming`, real-time, digits plus `rows`/`days`, em dash, arrow, middle dot): nothing (the one `days` hit is the caption's ", gas days 13 to 21 September" followed by "rows", not a count).
- Screenshots retaken by me after the edits: 1440 (hero, chart and key) and 390 in a true 390 px iframe (hero with the new summary, chart and key). Nothing clipped or overlapping. Server on 9894 stopped; 9670 untouched.

One-line summary: APPROVE; both majors fixed and reproduced from silver, all taken nits correct, build, detector and mirrors clean.
