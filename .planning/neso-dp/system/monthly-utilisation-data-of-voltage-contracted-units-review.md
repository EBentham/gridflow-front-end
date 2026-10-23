# Checker review: `monthly-utilisation-data-of-voltage-contracted-units` (lead `voltage_units_utilisation`), held page

## Verdict: APPROVE (0 blockers, 0 majors, 4 nits)

The held line passes as written; the report's fallback line is not needed. The hold itself is the seat's accepted ruling and is not a finding.

## What I checked

- Gates: `gridflow-build --only neso_data_portal/voltage_units_utilisation` in `C:\gridflow-wt\fe-neso-sys` writes the page with no error for it; detector `[]`; `cmp` of the canonical note against the mirror clean; 0 em or en dashes on the page; none of locally, our, since 20, live, now, yet, soon, pending, planned, shipped, ruling, ledger, TODO on the page ("Rows" appears only in "Rows not shown"); no artefacts exist under `site\hifi\data\{series,samples,notebooks}\neso_data_portal\` for this key, as a held page requires.
- Screenshots at 1440, 768 and 390 (390 in a 390 px iframe) read: nothing clipped or overlapping. The 1024 shot was taken and not opened (same layout as 768). Server on 9896 started with its PID recorded and stopped by that PID; the port no longer answers.
- Note diff against `origin/master`: front matter insertion plus the three-line body addition only; nothing else touched.

## 1. The held line

"One row in NESO's 9 October 2026 file; how a month's MVAr is totalled is unstated."

- **One row, dated:** the bronze body is one header and one data row (173 bytes, matches the sidecar's `declared_content_length` and `body_sha256`). The sidecar's `ckan_last_modified` is `2026-10-09T12:57:26.168291` (sent with no offset; read as UTC it is 13:57 UK time, still 9 October). The catalogue note says updates begin 9th October 2026, and the 8 October field-info snapshot has `total: 0`, so the one-row state first appears with the 9 October change. So the clause is a statement about NESO's file as last modified on that date, not a local-data reference. It names no capture date, count of ours or path. Pass.
- **Aggregation unstated:** the dictionary (field-info snapshot `20261008T114228Z`) says only "The total MVAr injected by the unit for the utilisation month" / "absorption ..." / "The sum of total absorption and injection ..."; the package and resource text say "the total of both injection and absorption ... for the month". None says how samples become a month's total. Pass.
- Plain, no codes, 16 words (the build enforces the budget). No change needed.

## 2. What one row is, and the month label

Reproduced from bronze and silver (Polars, read only): `BMU ID` "THURB-1,2 & 3", `Month and Year` `Aug-26`, `Location` Thurrock, injection 296592.1, absorption -708805.6, combined -412213.5; 296592.1 - 708805.6 = -412213.5. Silver has 1 row: `month_and_year` 2026-08-01 (registry format `%b-%y`), `timestamp_utc` = `event_time` = 2026-07-31T23:00:00Z, `published_at` = `available_at` = 2026-10-09T12:57:26.168291Z. Code agrees: registry `temporal.kind` is `month`; `silver/neso_data_portal/casting.py:619-626` calls `settlement_period_to_utc(value.replace(day=1), 1)`, and `utils/time.py:28-42` starts period 1 at 00:00 UK local, so August (BST) gives 31 July 23:00 UTC. The writer's description is right. NESO's quoted wording ("the contracted units participating in Voltage 2026 service"; "injection and absorption of reactive power utilised by the unit based on the instructions provided by NESO's Control Room"; Location "The geolocation of the unit") matches the 6 October catalogue snapshot and the dictionary. The held page prints none of the times, so nothing on the page depends on them.

## 3. The sign sentence (body, "Sentinels and missing values")

The dictionary examples are 198, 4312 and 4512, all positive; the file has a negative absorption and a negative combined value equal to injection plus absorption. The sentence is true. See nit 4 for its last clause.

## 4. Captures

One bronze capture (`2026/10/10`), one silver file, one row; no 16 October capture exists (the System siblings `system_inertia` and `outturn_voltage_costs_main` also hold only `2026/10/08`). The skip rule the writer cites is real (`client.py:1752-1765`: an upload is skipped when the newest capture carries the same `last_modified`). One caution for the seat, not a page issue: nothing I could read proves a 16 October sweep reached this family, so "NESO's file did not change" is an inference. The page does not state it. NESO's file date on the page is the 9 October change; correct.

## 5. Related links

All four resolve in the page set. `obligatory-reactive-power-service-orps-utilisation` (Grid Code generators, by unit and month) matches that note's own page block; `voltage-requirement` and `constraint-breakdown` match theirs (voltage constraints "for reactive-power balance" is NESO's wording). `outturn-voltage-costs` matches its approved page block on the Constraint management branch ("monthly outturn cost ... £m ... voltage constraint group"). Seat item, not a finding: this worktree's branches were cut before that approval landed (vault merge-base `0ee21a6` against the Constraint management tip `470de50`), so here the `outturn-voltage-costs` note has no `page:` block and its page renders blank until the stack is merged or rebased.

## Findings

1. **nit** `page.how_used[1]`, `page.related[0].note`: pairing this file with the monthly voltage costs is looser than it reads. That package's utilisation costs are, per its note, "only the ORPS payments" allocated per group; it is by constraint group while this file is by unit with no group; and its October 2026 note says updates are paused, so the two share no month. Suggest `how_used[1]`: "Read beside NESO's monthly voltage costs, which are by constraint group, not by unit", and `related[0].note`: "Monthly voltage costs in £m by constraint group, not by unit" (11 words).
2. **nit** `page.facts.grain`, `page.what_it_is`: "one row per unit" and "one unit's month" read the ID as a single unit. The dictionary describes `BMU ID` as "Unique ID for the Balancing Units" (plural; its example is `THURB-1`), and the one row's ID is the composite `THURB-1,2 & 3` (the note body says so; the writer lists it as unverified). Suggest "One row per BMU ID and month; NESO states no key" and "Each row is one BMU ID's month".
3. **nit** `page.summary`: "each unit contracted in its Voltage 2026 service" is hard to parse ("its" could be the unit's). NESO's wording is "contracted units participating in Voltage 2026 service"; suggest "each unit contracted to NESO's Voltage 2026 service".
4. **nit** body, "Sentinels and missing values", last clause: "NESO explains neither" overreaches. The dictionary does say the total is "the sum of total absorption and injection", so a signed total follows once absorption is signed; what NESO leaves unexplained is the sign of absorption. The dictionary's own example total (4512) is also not 198 + 4312 (4510). Suggest "NESO does not explain the negative absorption, and its example total of 4512 is not the sum of its examples 198 and 4312".

## Defects (confirmed from the writer's section)

- Sign convention and unit unclear (examples positive, file's absorption negative, MVAr totals with no stated aggregation): confirmed; keep as a vendor question. Related fact: the approved ORPS page says that package's utilisation is in MVArh per its package text, while this file's dictionary says MVAr.
- One row only: confirmed; re-check after NESO's next monthly upload.
