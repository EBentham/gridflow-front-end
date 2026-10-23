# Held pages, Constraint management part 1: writer report (2026-10-23)

Four one-table held pages, written per ruling 6 and the template's held mode (no chart, frame or notebook). Each `page:`
block is on the canonical note in `C:\gridflow-wt\vault-neso-cm\30-vendors\neso-data-portal\datasets\` (Edit tool, CRLF on
every line: 218/218, 296/296, 310/310, 362/362), mirrored byte for byte to `C:\gridflow-wt\fe-neso-cm\vault\neso_data_portal\`
(`cmp` clean on all four). No series, samples or notebooks. `updated:` moved to 2026-10-23 on all four because the bodies
changed (every package had a 16 October recapture; see each section).

| Page | Build `--only` | Detector | Screenshots |
|---|---|---|---|
| `24-months-ahead-constraint-cost-forecast` | `neso_data_portal/constraint_cost_fc_24m`: ok | `[]` | 1440, 1024, 768, 390 |
| `24-months-ahead-constraint-limits` | `neso_data_portal/constraint_limits_24m`: ok | `[]` | 1440, 1024, 768, 390 |
| `constraint-management-intertrip-service-information-cmis` | `neso_data_portal/cmis_intertrip`: ok | `[]` | 1440, 1024, 768, 390 |
| `day-ahead-constraint-flows-and-limits` | `neso_data_portal/da_constraint_flows_limits`: ok | `[]` | 1440, 1024, 768, 390 |

Screenshots: `.planning\neso-dp\constraint-mgmt\held-1-shots\` (`cost-*`, `limits-*`, `cmis-*`, `dayahead-*`; 390 through a
390 px iframe). I looked at the CMIS 390 and day-ahead 1440 views: long request URLs wrap, nothing is clipped, no chart, frame or
notebook, one "Rows not shown" entry under "The silver tables". I did not measure `scrollWidth` numerically this time; the
checker should. Rendered text on all four: 0 em or en dashes, arrows, middle dots or replacement characters; none of live, now,
yet, soon, pending, coming, planned, shipped, real-time, locally, ruling, ledger, TODO, RULINGS, E-SEM; £ renders. No capture
date, size or row count on any page. The builds print only the known vault-wide warning (35 "Known issues" lines dropped by the
caveat grammar). My server on 9903 was started from Bash with its PID recorded (15040, Windows 34724) and stopped by that PID;
9670 not touched. (A first attempt via PowerShell `Start-Process` was blocked by the guard before it ran; nothing started.)

## Shared evidence

| Claim | Evidence |
|---|---|
| `package_show`, then each upload downloaded whole unless `last_modified` is unchanged | gridflow `connectors/neso_data_portal/client.py` `iter_members` (as the approved held pages); every resource here is `url_type: upload` (registry JSON) |
| Every request URL | bronze sidecar `request_url` of the newest capture of each file under `C:\gridflow-data\bronze\neso_data_portal\<family>\`; `package_show` as in the approved pages |
| `ingest` / `transform` with `--last 24h` | same form as the approved held pages |
| Hold lines | the registry `eligibility.question` of each family (the ledger rows 50, 51, 52, 137 only name the topic) |
| One-table pages | `site/hifi/data/neso_data_portal.json` `package_tables` maps each slug to its one table; titles follow `names` |
| Landscape `market` | as the other constraint and cost pages |
| No stale capture fact on a page | every package has a 2026-10-16 capture; no page states a capture date, size, row count or "newest capture"; the two monthly CSVs and the day-ahead diagrams changed file name, so the page shows the 16 October URL and says the name changes |

## 1. 24-month constraint cost forecast (`constraint_cost_fc_24m`)

| Claim | Evidence |
|---|---|
| Reason: "Since NESO renamed the column, the file has no unit, and the metadata's £m is unconfirmed." | registry question (currency unit; confirm GBP million); package notes announce `Constraint Cost (£m)` to `Constraint Cost` on 9 September 2026; both captures' header is `Month,Constraint Cost`; field-info 20261008T114228Z gives title `Constraint Cost (£m)`, unit `£m` (valid UTF-8 `C2 A3` in the bytes) |
| Scope: thermal, voltage, stability boundaries plus voltage requirements; excludes inertia and largest loss of infeed | NESO package notes (snapshot 20261006T195819Z), paraphrased with "In NESO's words" |
| One figure per month, no split by boundary, no range | header has two columns; note body |
| Cadence monthly; each upload replaces the file | extras `Update frequency: Monthly`; one resource id, file name `sept26` then `oct26` |
| Grain "labelled like Dec-25" | field-info example `Dec-25`, format MMM-YY |
| Request URL `..._oct26.csv` | sidecar of `raw_20261016T192117Z_...c46bbd3e.csv` |
| Related: constraint breakdown, thermal costs, voltage costs, 24-month limits | all in the page set; voltage requirements are in this forecast's scope |

**Body corrections:** the 16 October capture added to the files bullet (oct26 URL, 360 bytes, 24 rows, same unitless header,
`last_modified` 2026-10-09T09:30:58); the vintage and event-time clocks now give both captures; the month-label paragraph adds
the second capture's span (2026-11-01 to 2028-10-01, same one-month lead); "With a single capture to date, no revision
behaviour has been observed" replaced: the two captures share 23 months and the figure differs on all 23 (no values stated);
the activation paragraph's "no later monthly capture had landed" replaced with the second silver file (24 rows; 48 in silver).

## 2. 24-month constraint limits (`constraint_limits_24m`)

| Claim | Evidence |
|---|---|
| Reason: "NESO does not map its week numbers to dates, nor say when each week was forecast." | registry question (week calendar; is each upload issued before every target week) |
| Boundary capability in MW per boundary code | field-info: "Boundary capability for <code>", unit MW on all twelve |
| Week number "1 to 52", no dates | field-info `Week No` description "(1-52)"; header has no date column |
| Two diagrams locate the boundaries | DOC resources (`constraint_limits_24m_files`); note body |
| "A boundary is a cut across the transmission network" | note body prose (not a NESO quote); see Unverified |
| Requests: `package_show`, `..._oct26.csv`, both PDFs | sidecars (CSV 16 October; PDFs 8 October, not recaptured because unchanged) |
| Related: ten codes match day-ahead; SCOTEX and ESTEX also in thermal | recomputed on bronze and silver 2026-10-23: 10 and 2 exact matches |

**Body corrections:** the 16 October capture added (oct26, 7,409 bytes, 105 rows, same header, vintage 2026-10-09T09:29:34);
the clocks and the key paragraph cover both captures; "Captures to date: one (2026-10-08). No scheduled refresh has run yet."
replaced, and the TODO on revisions answered: **a monthly upload revises, not only extends.** The window moved four weeks (2026
week 40 to 2028 week 40, then 2026 week 44 to 2028 week 44); of the 101 weeks in both, 30 rows changed (102 cells). The
activation paragraph records the second silver file (105 rows).

## 3. Constraint management intertrip service (`cmis_intertrip`)

| Claim | Evidence |
|---|---|
| Reason: "Times carry +00:00 though NESO says GB local time, and the newer fee has conflicting units." | registry question (clock reading; newer fee £/MWh or £/SP); package notes "Time values are all given in local time in GB"; every arming time in both 2026-27 captures ends `+00:00` (83 of 83) |
| "NESO's dictionary describes £/MWh but gives the unit as £ per settlement period" | field-info 2026-27: description "The arming fee rate (in £/MWH)", unit `£/SP` |
| Armed to intertrip schemes to manage constraints; indicative cost | NESO resource descriptions |
| Cadence: monthly, shortly after each month's payments | extras `Update frequency: Monthly`; package note on payment in arrears |
| History: yearly files from 2022-2023 | resource names |
| "Headers differ by year, and changed again in October 2026" | two declared epochs; NESO's 2026-27 description announced a rename for 9 October 2026; the 16 October capture carries it |
| Requests: `package_show`, 2022-2023 and 2026-2027 files, "first and newest shown" | sidecars |
| Only an ingest command, no transform | see Open questions |
| Related: thermal costs, constraint breakdown, `elexon/bmunits_reference` | dictionary comment "BMU ID as registered with ESO" |

**Body corrections and new facts:** the 2026-27 file was recaptured on 16 October (6,484 bytes, 83 rows, `last_modified`
2026-10-14T11:02:57) under a **third header**: `BMU ID,Arming Date Time,Disarming Date Time,Current Arming Fee,Cost for this
utilisation,B6 or EC5 ` (trailing space; NESO announced `B6 or EC5 boundary`; no units left in the header). The transform raised
`HeaderEpochError` and wrote nothing (gridflow `.planning/phases/v0.22-close/refresh-20261016/DRIFT.md` and `reconcile.log`).
By position against the 8 October capture: the same 83 keys and **3 rows with a changed cost**, so NESO restates published
costs in the current-year file. Added as a new "A third header" paragraph; the old "possible third epoch, not a captured one"
sentence removed; the Cadence block and "live year" sentence updated; the reference to the day-ahead hold says "first capture".

## 4. Day-ahead constraint flows and limits (`da_constraint_flows_limits`, capture failed)

| Claim | Evidence |
|---|---|
| Reason: "Some boundary and half-hour pairs repeat, some with different values, so there is no silver table." | registry question (row grain) and the failure record (ruling 632: 1,436 excess rows, 44 key groups with differing values); the 16 October capture repeats the same 1,436 excess (1,392 whole-row) |
| Flow modelled day ahead from wind, generation and demand forecasts; not revised after publication; 22 April 2024 change | NESO resource description and field-info `Flow_MW` |
| Limit in MW; flow has no unit given | field-info: `Limit_MW` unit MW, `Flow_MW` unit blank (the page gives no flow unit) |
| Positive flow direction on the diagrams | NESO package notes |
| History: past three years plus the current year; earlier on request | NESO package notes |
| Cadence "Daily (Weekdays)"; each upload is the whole archive | extras; the 16 October capture contains every distinct row of the first plus 6,794 new keys |
| Grain: boundary code and half hour (GMT/BST) | field-info: title "Date (GMT/BST)", "settlement period (half hourly) basis" |
| Requests: `package_show`, the CSV, both `-oct2026` diagrams | sidecars of the 16 October captures |
| Related: ten codes with the 24-month limits, five with thermal costs | recomputed 2026-10-23 (ESTEX, SCOTEX, SEIMP, SSHARN, SWALEX for thermal) |

**Body corrections:** item 1 of "Five things" adds the 16 October capture (740,443 rows), which fails the same way and is a
reconcile gap, not an adjudication; "captured once" replaced; a second capture table added (CSV 28,324,304 bytes, 740,443 rows,
vintage 2026-10-16T15:42:40; both diagrams re-issued as `...-boundaries-oct2026.pdf`, 525,665 and 346,472 bytes); identity,
vintage and silver-layout lines cover two captures; the forward-target paragraph adds 738,687 of 740,443 targets before the second
vintage; the diagrams family answers its versioning TODO (new name per issue); the Cadence paragraph records append-only growth
between the two captures (no key dropped; earliest target still 2023-01-01) and keeps the year-boundary TODO.

## Unverified or judgement calls (checker, look here)

- **Limits `what_it_is`, "A boundary is a cut across the transmission network."** This is the note's own definition, not a
  NESO quote. Drop it if the checker wants vendor words only; the next sentence carries NESO's "boundary capability".
- **CMIS and day-ahead pages show no `transform` command.** The CMIS transform currently fails on the 2026-27 file's new header
  and the day-ahead transform fails on duplicate keys, so I showed ingest only (day-ahead says "bronze only"; the CMIS raw-feed
  note does not say "bronze only" because older CMIS files do have silver). The cost and limits pages keep the transform line,
  which works.
- **Request URLs use the 16 October file names** (`oct26`, `-oct2026`). They will change monthly; each raw-feed note says the
  name carries the upload month (cost, limits). The day-ahead note does not say it of its diagrams (word budget); the CSV name is
  stable.
- **CMIS hold line** compresses two questions; "conflicting units" refers to the dictionary's £/MWh description against its
  £/SP unit. The newest header now has no unit at all.
- **Cost hold line** says the metadata's £m is unconfirmed: the registry's "undecodable symbol" reading is not reproduced in the
  field-info bytes, which hold a valid £. The hold stands on the missing confirmation, not on a garbled byte.
- **Overflow at 390** checked by eye on the screenshots only, not measured.

## Open questions

- None blocking. Seat: keep or drop the transform line on held pages whose transform currently fails (I dropped it).

## Template problems

- None new.

## Defects (pasteable)

- **gridflow, `cmis_intertrip`:** NESO renamed the 2026-27 file's columns (`Current Arming Fee`, `Cost for this utilisation`,
  `B6 or EC5 ` with a trailing space, not the announced `B6 or EC5 boundary`); the 16 October capture fails `HeaderEpochError`
  (already in `refresh-20261016/DRIFT.md`). New fact for the remediation unit: the same capture **restates the cost on 3 of 83
  published rows** with unchanged keys, and the fee column has lost its unit, which weakens the fee-unit evidence further.
- **gridflow, `constraint_limits_24m`:** monthly uploads revise earlier weeks (30 of 101 overlapping rows, 102 cells, between
  `sept26` and `oct26`). `whole_capture` handles it, but it settles the note's revision TODO and matters for any forward-target
  ruling.
- **gridflow, `constraint_cost_fc_24m`:** every overlapping month (23 of 23) changed between the September and October uploads
  (expected for a re-forecast; recorded in the note).
- **gridflow, `da_constraint_flows_limits`:** the 16 October capture fails like the first (same 1,436 excess rows) but is a daily
  reconcile gap, not adjudicated; each weekday refresh will add another failing whole-archive capture (about 28 MB each).
- **Vault, all four notes, were stale on captures** (each said one capture); fixed in this batch's vault branch.
- **Vault, cost forecast note vs registry:** the registry says the metadata shows an undecodable symbol before `m`; the
  field-info bytes hold a valid £. Worth a line in the remediation page so the hold question is asked correctly.
- **Package registry status reads `eligible`** on all four packages while each family is held (known pattern).
- **Manifest:** all four are one-table pages and the `package_tables` entries are correct; no change suggested.
