# NESO Data Portal: showing the rows of held tables (ruling 66)

Opened 2026-10-24. Bobbo: the site is a data catalogue, so show as much as can honestly be shown and do not omit
datasets for weak reasons. This supersedes ruling 6's "no rows for held tables". Each package below is fixed on the
branch that already holds its page, in stack order; the PRs update when the seat pushes. Nothing merges until Bobbo looks.

The template is in place on every branch (PR #60, `.planning/neso-dp/template-pass/caveat-REPORT.md`): a `caveat:`
line (16 words or fewer) for a table with rows and an open question, and a raw sample (first eight lines of one bronze
file, as fetched) for a held page with no silver table. Read "Caveats and held pages (ruling 66)" in
`.planning\v5\author-brief.md` IN YOUR FRONT-END WORKTREE before anything else.

## What to do with each table

| The table | What the page does |
|---|---|
| Has silver rows and an open question (`held` in gridflow) | Full anatomy (chart where an honest one exists, frame, column guide, notebook, artefacts) plus one `caveat:` naming the question. Remove `held`. |
| Eligible in gridflow (no hold) | Full anatomy, no caveat. Remove `held`. |
| No silver table (bronze only), in a family with a silver table | Member keeps `held:`, reworded to the corrected reason. |
| Package with no silver table at all, not a licence carve-out | Page stays held; correct the `held:` reason; add `raw_feed.sample` (name the `file:`) with its caveat; run `gridflow-sample` (distil extra, read-only bronze). |
| Licence carve-out (levelised cost of hydrogen, GIS DNO licence areas) | Page stays held, no sample; correct the reason only. |

**Corrected reasons:** `C:\Users\Bobbo\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\side-session-notes\local_6dc4c8e9-5890-4ee4-a8ce-724b6948acce\neso-held-reasons-corrected.md`
(the gridflow registry's hold question per table, branch `claude/neso-dp-known-at-time-70aa93` in
`C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow`). Check each against the ledger
`C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\.planning\v0.22-FE-LEDGER.md` and the rows; if they disagree,
use what the code and rows prove and say so in your report. The old reasons ("the files don't say when each row was
first published" on almost everything) were wrong for most tables: never keep one without checking it.

**The chart and the question:** a chart must not lean on the field the question is about as if it were settled. If
dates may be day-first or month-first, or a week calendar is undefined, chart something that does not depend on it,
or use `type: none`. If the unit is unknown, the axis says what NESO's column is called and the caveat says the unit is
not stated; never invent one. Mock auction data is labelled mock in the caption. Forecasts with no issue time are
never drawn as what was known at the time.

**Caveat wording:** one plain sentence, 16 words or fewer, no label, no codes, no planning words, no local-data
references; dated NESO facts only. Keep the wording the same across a batch where the question is the same (for
example the interconnector limit tables, the TNUoS tariff tables). Family pages show one frame: give each member
with rows its own caveat; the frame shows the lead or `record.select.silver`.

**Tariff tables (parent, 2026-10-24):** fixed BSUoS tariffs, AAHEDC and all eight TNUoS tables carry a per-row
Published Date, but a date with no time, and NESO does not say older rows stay unchanged after it; use the rewritten
rows in the corrected-reasons file for their caveats.

**Old body lines (B1 review):** the held notes' bodies say "no data values are published" in several places. On a
page that now shows rows, remove or correct every such line (a major finding otherwise). On a page that stays held
with a raw sample, say it shows the file's first lines as fetched and no table.

## Where things are

| Branch key | Front-end worktree | Vault worktree |
|---|---|---|
| as-a | `C:\gridflow-wt\fe-neso-as-a` (`feat/neso-dp-ancillary-a`) | `C:\gridflow-wt\vault-neso-as-a` (`docs/neso-dp-ancillary-a`) |
| as-b | `C:\gridflow-wt\fe-neso-as-b` (`feat/neso-dp-ancillary-b`) | `C:\gridflow-wt\vault-neso-as-b` |
| bc | `C:\gridflow-wt\fe-neso-bc` (`feat/neso-dp-balancing-costs`) | `C:\gridflow-wt\vault-neso-bc` |
| cm | `C:\gridflow-wt\fe-neso-cm` (`feat/neso-dp-constraint-management`) | `C:\gridflow-wt\vault-neso-cm` |
| sys | `C:\gridflow-wt\fe-neso-sys` (`feat/neso-dp-system`) | `C:\gridflow-wt\vault-neso-sys` |
| trd | `C:\gridflow-wt\fe-neso-trd` (`feat/neso-dp-trading`) | `C:\gridflow-wt\vault-neso-trd` |
| dem | `C:\gridflow-wt\fe-neso-dem` (`feat/neso-dp-demand`) | `C:\gridflow-wt\vault-neso-dem` |
| gen | `C:\gridflow-wt\fe-neso-gen` (`feat/neso-dp-generation`) | `C:\gridflow-wt\vault-neso-gen` |
| ic | `C:\gridflow-wt\fe-neso-ic` (`feat/neso-dp-interconnectors`) | `C:\gridflow-wt\vault-neso-ic` |
| nc | `C:\gridflow-wt\fe-neso-nc` (`feat/neso-dp-network-charges`) | `C:\gridflow-wt\vault-neso-nc` |
| ci | `C:\gridflow-wt\fe-neso-ci` (`feat/neso-dp-carbon-intensity`) | `C:\gridflow-wt\vault-neso-ci` |
| fes | `C:\gridflow-wt\fe-neso-fes` (`feat/neso-dp-fes`) | `C:\gridflow-wt\vault-neso-fes` |

Canonical notes `30-vendors\neso-data-portal\datasets\<slug>.md` in the vault worktree (keep line endings; Edit tool);
mirror `vault\neso_data_portal\<slug>.md` in the front-end worktree; `cp` and `cmp` after every edit. Never edit the
page set; if a lead is wrong for the frame, say so (the seat reorders). The original batch reports for each page are
in `.planning\neso-dp\<group>\` (and the tracker in `BATCH-<group>.md`): read them, they hold checked facts.
**Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\neso-dp\held-rows\<batch>-<slug>-author.md`
and `-review.md`. **Standing instructions:** `.planning\neso-dp\AGENT-PROMPTS.md`.

## Batches

Silver: Y = a silver table exists locally (`C:\gridflow-data\silver\neso_data_portal\<table>`), - = none.

| Batch | Branch | Packages (tables: silver) | Writer port | Checker port |
|---|---|---|---|---|
| A1 | as-a | `dynamic-containment-4-day-forecast` (`dc_forecast_4d` Y, `_history` Y); `eac-mock-auction-results` (buy, by unit, summary, sell: Y; four daily tables: -); `eac-br-mock-auction-results` (four tables Y); `long-term-forecasts-for-dc-dm-dr-requirements` (Y) | 9981 | 9801 |
| A2 | as-b | `contract-transfer-of-obligation` (-, raw sample); `disaggregated-bsad` (-, raw sample); `non-bm-ancillary-service-dispatch-platform-asdp-window-prices` (Y); `obligatory-reactive-power-service-orps-utilisation` (three tables Y) | 9982 | 9802 |
| B1 | bc | `bsuos-fixed-tariffs` (Y); `daily-balancing-costs-balancing-services-use-of-system` (-, raw sample); `balancing-services-use-of-system-bsuos-daily-forecast` (-, raw sample, cp1252); `daily-balancing-volume-balancing-services-use-of-system` (-, raw sample); `gb-system-inertia-bid-and-offer-costs` (Y) | 9983 | 9803 |
| B2 | bc | `bsuos-monthly-forecast` (`fc_summary` Y; seven others -); `skip-rates` (eight Y including two eligible, `summary` and `stage5_psa_technology`; `in_merit_psa_dsf_unit` and `stage5_dsf_technology` -) | 9984 | 9804 |
| C1 | cm | `24-months-ahead-constraint-cost-forecast` (Y); `24-months-ahead-constraint-limits` (Y); `constraint-management-intertrip-service-information-cmis` (Y); `day-ahead-constraint-flows-and-limits` (-, raw sample); `operational-transparency-forum-network-congestion-data` (Y); `voltage-requirement` (Y) | 9985 | 9805 |
| S1 | sys | `gis-boundaries-for-gb-dno-license-areas` (carve-out, reason only); `stability-pathfinder-service-information` (utilisation Y; availability -, empty); `system-operating-plan-sop` (Y) | 9986 | 9806 |
| T1 | trd | `balancing-services-contract-enactment` (two Y); `historic-gtma-grid-trade-master-agreement-trades-data` (`gtma_trades_fy` Y; `gtma_trades_data` and `_pre` eligible); `index-linked-contract-volume` (Y); `interconnector-requirement-and-auction-summary-data` (Y); `super-stable-export-limit-contract-enactment` (Y); `upcoming-trades` (Y) | 9987 | 9807 |
| D1 | dem | `day-ahead-half-hourly-demand-forecast-performance` (Y); `daily-demand-update` (Y); `demand-profile-dates` (-, raw sample); `historic-demand-data` (Y) | 9988 | 9808 |
| D2 | dem | `long-term-2-52-weeks-ahead-national-demand-forecast` (Y); `school-holiday-percentages` (Y); `transmission-losses` (two tables, both eligible: no caveat) | 9989 | 9809 |
| G1 | gen | `14-days-ahead-wind-forecasts` (two Y); `daily-opmr` (Y); `weekly-opmr` (Y); `weekly-wind-availability` (Y); `wind-bmu-boa-volumes` (Y) | 9990 | 9810 |
| I1 | ic | `brit-ned`; `eleclink`; `ifa` (two); `ifa2` (two): all Y | 9991 | 9811 |
| I2 | ic | `nemolink` (three); `nsl`; `viking` (two): all Y | 9992 | 9812 |
| N1 | nc | `aahedc-tariffs` (Y); `transmission-network-use-of-system-tnuos-tariffs` (eight Y) | 9993 | 9813 |
| CI1 | ci | `carbon-intensity-of-balancing-actions`; `country-carbon-intensity-forecast`; `national-carbon-intensity-forecast`; `regional-carbon-intensity-forecast`: all Y | 9994 | 9814 |
| F1 | fes | `building-heat-model` (example output Y; list input -); `fes-electricity-demand-summary-data-table-ed1`; `future-energy-scenario-electricity-supply-data-table-es1`; `fes-european-electricity-supply-data-table-es2`; `fes-flexibility-data-table-data-table-flx1`: Y | 9995 | 9815 |
| F2 | fes | `fes-natural-gas-residential-and-non-domestic-i-c-heat-demand-summary-data-table-ed3` (three Y); `fes-road-transport-summary-data-table-ed5`; `fes-whole-system-gas-supply-data-table-ws1`; `fes-whole-system-gas-supply-emissions-data-table-ws2`; `local-authority-level-spatial-heat-model-outputs-fes` (two Y): Y; `levelised-cost-of-green-hydrogen` (carve-out, reason only) | 9996 | 9816 |
| R1 | bc, sys | Fixed defects (gridflow PR #134): `current-balancing-services-use-of-system-bsuos-data` (day-first files now read; branch bc) and `system-frequency-data` (2014: all 12 files, repeated October hour by `dtm_occurrence`; branch sys): take off the defect caveats and notes, refresh artefacts from the re-transformed silver | 9997 | 9817 |

Not in scope: held packages that are document-only file groups (ETYS boundaries, GIS charging zones, SSEP shapefiles)
keep their pages as they are.

## Rules

**Processes (hard rule):** start a server only in a way that records its PID, and stop only that PID. Never kill
processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`).

`.planning/v5/p26/BATCH-rest.md` "Shared-worktree rules" and "Seat rulings carried over", and `BATCH-dfs.md`
"Bobbo's rulings for NESO package pages", apply unchanged, except that ruling 66 replaces "no rows for held tables".
Keep strictly to your own packages' files; never `git add` or commit (the seat commits). Other agents may share a
worktree: if the build stops on another package's files, check your own built page and say so. Do not end your turn
until your report or review is written. Checked facts in `BATCH-ancillary-b.md` apply: set `dedup:` when captures
repeat rows; on a table with no event time use `data.sql()`; the column guide accepts only the lead table's columns.

## Tracker

| Batch | Writer | Checker | State |
|---|---|---|---|
| A1 | a012e047532732e92 | a4ec36bb8e74245fd | APPROVED x4 (round 2); committed (site 8cff52a); merged into ancillary part 2; 20cn logged |
| A2 | a9f952220257ebd0a | af25be4d62dca5b4a | APPROVED x4 (round 2); committed (vault, then mirror and artefacts f95709e); 20cm logged |
| B1 | a12aa2a2d21abdba4 | aac52199c23c016ff | APPROVED x5; committed (vault 96396ba, site be9a3f6); 20cl logged |
| B2 | a948627e0bfe2b68d | aaf248079da8934b8 | APPROVED x2 (round 2); committed (site 8a9f6fe); leads reordered; 20co logged |
| C1 | ad75c58a68842e8b6 | aa4a892ba7c0e0bd4 | APPROVED x6 (round 2); committed (site 43a7188); 20cp logged |
| S1 | a7ab77ada40837869 | a0a8c6d80773615fa | APPROVED x3; committed (site 5a00070, 733b52c); Pathfinder lead reordered (7342b43) |
| T1 | abf6b4cf3ba85c1a5 | a335a0dc2e2350249 | APPROVED x6 (round 2); committed (site e3a1ca9); pushed; 20cq logged |
| D1 | ac29ae2189289eb20 | a1587b1603e0092f5 | APPROVED x4 (round 2); committed (site bb1ee8d); demand pushed, parent told; 20cr logged |
| D2 | a6529fae660c4ff74 | aaa229431fb8d7d45 | APPROVED x3 (round 2); committed on dem |
| G1 | af234cffef25e4fa7 | adaa14b1da19ee956 | APPROVED x5, nits fixed; committed (site 5ed280c); pushed; parent told |
| I1 | a475c72bb4c6ca14f | a1fdee2150037abad | written; in joint review with I2 (IFA, IFA2 draw Intraday 1; BritNed no chart; NESO upload gaps 11 and 12 Oct) |
| I2 | a85a78f0c3de4f450 | a1fdee2150037abad | written; seat ruled its chart rule (Day Ahead as fetched, rows uploaded before their hour) for all seven pages; Viking lead reordered (b79c573), regenerated; one checker will review I1 and I2 together |
| N1 | a0ac37967725c0a93 | | writing |
| CI1 | ace01fca13556e033 | | writing |
| F1 | a34676c0e232141b9 | | writing |

Pace raised 2026-10-24 ~13:25Z (Bobbo via the parent): 5 agents at once, aim about 50% of weekly usage over 36 hours;
park at 98% weekly. After NESO: ruling 66 on the seven blank other-vendor pages (ENTSO-E balancing-energy bids, current
balancing state, procured balancing capacity, outages; ENTSOG capacity-by-indicator and cmp; GIE unavailability), one
writer and one checker each, one branch and PR off main plus the vault PR. Added 2026-10-24 ~15:10Z (parent):
Elexon `netbsad` and `nonbm`, same staffing, after gridflow's fix (gridflow PR #128, unmerged; local silver re-ingested).
NETBSAD: no parser bug; Elexon publishes zeros almost always, non-zero buy-price adjustments on only four days since
January 2024 (24 May 2024, 13 Aug 2024, 24 Oct 2025, 15 Jan 2026; 19 periods on 15 Jan, 1.49 to 10.65 GBP/MWh);
balancing actions appear in DISBSAD; seven duplicate boundary rows in the January week (backlog 12e); chart 15 Jan 2026.
NONBM: the connector sent parameters Elexon ignores (fixed); silver 741 distinct rows (12-19 Jan and 25 Mar-2 Apr
2026); Elexon stopped publishing after 1 Apr 2026 10:04 UTC (SP22); each day's file holds what was published that UTC
day, so it starts with the previous day's last half-hour; most periods 0 (17, 28, 11 MW on 15 Jan 2026 SP25-27).
Verify all of this against silver before writing.
GIE `unavailability` (parent, ~15:45Z): fixed in gridflow PR #133 (unmerged; local silver re-transformed): typed, keyed,
one row per outage notice per calendar day, new `outage_date` column; 1-5 Aug went from 1,705 rows to 76. Write it
without the defect caveat; remaining caveats: timestamps carry no time zone (GIE's reporters mix UTC and local), units
unstated, an outage running 06:00 to 06:00 appears on two calendar days, the August capture has 13 of 16 pages.

ENTSOG (parent, ~16:45Z): `capacity-by-indicator` and `cmp` fixed in gridflow PR #129 (unmerged, CI green; local silver
re-written from bronze). Day D's silver keeps every record whose validity overlaps gas day D (06:00-06:00 Brussels);
`timestamp_utc` is the record's own start if inside that gas day, else the gas-day start; record id + timestamp_utc
unique (firm_technical 28 rows/0 values -> 126/98; auction premiums 0 -> all 54 a day; unavailable firm capacity 25 on
one day -> 291 a day; null timestamps gone, 18c). capacity-by-indicator: no defect caveat (say
`available_through_uioli_short_term` holds only the "no capacity" sentences). cmp: caveat the six mixed units on auction
premiums and that it is unconfirmed which price the unit applies to (18u). Parked notes on `v5/p26-entsog-gas-held` /
`docs/v5-p26-entsog-gas-held`; the three cmp vault notes can now be corrected. Write both from current silver.

**Fixed in gridflow PR #134 (unmerged; local silver re-transformed):** current BSUoS day-first files (remediation 20y)
and system frequency 2014 (20ao: 12 of 12 files, the repeated October hour told apart by `dtm_occurrence`). Their
pages' defect caveats and notes come off in a small follow-up batch. The DC 4-day forecast's month-first 2022 issue is
still misread: keep that caveat.
