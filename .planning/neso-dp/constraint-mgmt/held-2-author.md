# Held pages, Constraint management part 2: writer report (2026-10-23)

Two one-table held pages, written per ruling 6 and the template's held mode (no chart, frame or notebook). Each `page:`
block is on the canonical note in `C:\gridflow-wt\vault-neso-cm\30-vendors\neso-data-portal\datasets\` (Edit tool, CRLF on
every line: 313/313 and 178/178), mirrored byte for byte to `C:\gridflow-wt\fe-neso-cm\vault\neso_data_portal\` (`cmp`
clean on both). No series, samples or notebooks. `updated:` moved to 2026-10-23 on both because the bodies changed (both
packages have a 16 October recapture; see each section).

| Page | Build `--only` | Detector | Screenshots |
|---|---|---|---|
| `operational-transparency-forum-network-congestion-data` | `neso_data_portal/otf_network_congestion`: ok | `[]` | 1440, 1024, 768, 390 |
| `voltage-requirement` | `neso_data_portal/voltage_requirement`: ok | `[]` | 1440, 1024, 768, 390 |

Screenshots: `.planning\neso-dp\constraint-mgmt\held-2-shots\` (`otf-*`, `voltage-*`; 390 through a 390 px iframe). I looked
at OTF 1440 and voltage 390: long request URLs and the long ORPS related slug wrap, nothing is clipped, one "Rows not shown"
entry under "The silver tables". I did not measure `scrollWidth`; the checker should. Rendered text on both: 0 em or en
dashes, arrows, middle dots or replacement characters; none of live, now, yet, soon, pending, coming, planned, shipped,
real-time, locally, ruling, ledger, TODO, RULINGS, E-SEM. No capture date, size or row count on either page. Builds print only
the known vault-wide warning (35 "Known issues" lines dropped). Server on 9904 started from Bash (PID 16815 recorded), stopped
by that PID; 9670 not touched. The two temporary 390 iframe wrappers were served from `site/hifi/h2w-frame-*.html` and
deleted straight after; `git status` shows only the two mirror notes changed for my packages.

## Shared evidence

| Claim | Evidence |
|---|---|
| `package_show`, then each upload whole unless `last_modified` is unchanged | gridflow `connectors/neso_data_portal/client.py` `iter_members`, as the approved held pages; every resource here is `url_type: upload` (registry JSON) |
| Request URLs | bronze sidecar `request_url` of the newest capture of each file under `C:\gridflow-data\bronze\neso_data_portal\<family>\` |
| `ingest` / `transform` with `--last 24h` | same form as the approved held pages; both transforms work (the 16 October refresh drained one silver file each, `refresh-20261016/reconcile.log` lines 248 and 265) |
| Hold lines | registry `eligibility.question` of each family (ledger rows 53 and 55 name only the topic) |
| One-table pages; titles | `neso_data_portal.json` `package_tables` and `names` ("OTF network congestion", "Voltage requirement") |
| Landscape `market` | as the other constraint pages |
| No stale capture fact on a page | both packages have a 2026-10-16 capture; neither page states a date, size or row count. OTF shows the 16 October file name and says the name carries the upload date |

## 1. OTF network congestion (`otf_network_congestion`)

| Claim | Evidence |
|---|---|
| Reason: "NESO does not explain its dates, how actuals are derived, or when forecasts were issued." (15 words) | registry question: is Date a week start, week end or reporting label; how are actuals calculated; when was each forecast issued. Field-info 20261008T114228Z: `Date` description empty |
| Weekly constraint limits in MW, eleven major boundaries, rolling six months back and forward, "as presented in OTF" | NESO package notes and resource description (snapshot 20261006T195819Z); field-info unit `MW` on all 22 value columns |
| Each boundary has an actual and a forecast column; `B6`, `B15` | registry header (11 labels x Actual/Forecast) |
| "the later rows carry a forecast only" | both captures: 26 later rows have every Actual blank, Forecast populated on all 53 |
| Cadence weekly; each upload replaces the file | extras `Update frequency: Weekly`; one resource id, name `07-10-2026` then `14-10-2026`, window rolled one week |
| Grain: one date, actual and forecast column per boundary | header; `date` unique in both captures |
| Request URL `..._14-10-2026.csv` | sidecar of `raw_20261016T204255Z_..._972b8047.csv` |
| Related: 24-month limits, day-ahead flows and limits ("under other codes"), thermal costs, constraint breakdown | note: no exact code shared with any neighbour; NESO's OTF document aliases `B6 (SCOTEX)`, `B15 (ESTEX)` |

**Body corrections (16 October capture, `otf_constraint_data_14-10-2026.csv`, 5,705 bytes, 53 rows, `last_modified`
2026-10-14T09:21:36):** intro span covers both captures (2026-04-18 to 2027-04-18 for the second); second capture added to
Files and the file-name paragraph (three names now); vintage clock gives both; the hold-question facts give both captures'
figures (37 Saturdays and 16 Sundays in the second; same 8-day step; same 26 on or before vintage and 27 after; last Actual
the Saturday three days after a Wednesday vintage, both times); "A single capture cannot show..." replaced by a measured
**Revisions** paragraph; blanks, identity, silver shape (two files), a second-capture receipt, Cadence (three Wednesday uploads;
each replaces the whole window) and the Holds bullet updated. Also fixed the related-pages bullet: the day-ahead package's 16
October capture fails too.

New facts for the hold (measured 2026-10-23, bronze, read only): the window rolled forward one week (2026-04-11 dropped,
2027-04-18 added); of 52 shared dates, 13 rows and 28 cells changed: 11 Actual cells of 2026-10-17 filled from blank, **3
Actual cells of 2026-10-03 restated** (`B6`, `B6a`, `B9`), and 14 Forecast cells on 11 dates from 2027-01-03 to 2027-04-11.
No Forecast on a date on or before either vintage changed.

## 2. Voltage requirement (`voltage_requirement`)

| Claim | Evidence |
|---|---|
| Reason: "NESO leaves unstated which nights each range covers, each group's area and when rows were issued." (16 words) | registry question: overnight window and endpoint inclusivity, reversed ranges, what each `V_` code covers, whether Last Updated is an issue time. Reversed ranges dropped from the line for the budget (as part 1 compressed CMIS) |
| Number of voltage machines per group, next weekend and the following Monday to Friday | NESO package notes ("voltage machine required for a given voltage group for upcoming weekend and following Monday to Friday"); resource name "Week Ahead Overnight" |
| "actual requirement is likely to change ... may optimise further closer to the time" | package notes ("further optimisation can be carried out towards real time"), paraphrased without the banned phrase |
| Codes such as `V_Mersey`; a map without a code list | bronze `Group` values; group-map PDF labels differ; no crosswalk (note body) |
| Cadence weekly; each upload is the whole file, earlier plans included | extras `Update Frequency: Weekly`; both captures hold plans back to 2021 under one file name; second keeps every key of the first |
| Grain: group and date range, count and update time | header; field-info "No. of Units might be required", "Datetime of last update" |
| Requests: `package_show`, the CSV, group map and introduction PDFs (cap is four; deep dive omitted, the note says so) | sidecars (CSV 16 October; PDFs 8 October, unchanged on 16 October per `ingest.log` line 330) |
| Related: outturn voltage costs, ORPS utilisation, constraint breakdown, 24-month cost forecast | all in the page set; the cost forecast's NESO scope includes voltage requirements (part 1) |

**Body corrections (16 October capture, same file name, 290,643 bytes, 5,257 rows, `last_modified` 2026-10-16T11:52:51):**
row count and second capture added to the hold paragraph and Files; "the captured body" made "each captured body" (key,
dedup); reversed ranges given per capture with their two ranges; activation receipt gains a second-capture line; Cadence gains a
measured two-capture comparison: cumulative file, 0 keys dropped or changed, 36 added (four ranges by nine groups), a missed 9
October upload whose rows survive, each upload a Saturday-to-Monday and a Tuesday-to-Friday range, landing on Fridays.

New facts (measured 2026-10-23):
- **`Last Updated` may be UK local time labelled `Z`.** In each capture the newest 18 rows carry `last_updated` 57 to 58
  minutes after CKAN `last_modified` (14:19Z/14:20Z against 13:22:22 UTC; 12:50Z against 11:52:51 UTC). Read as BST they fall
  2 to 3 minutes before the upload. Added to the note as a `TODO: verify`.
- **Probable year slip:** 18 rows start 2020-07-31 and 2020-08-02 with `last_updated` 2021-07-30T15:22Z; every other row starts
  on or after 2021-03-20, and no row starts 2021-07-31 or 2021-08-02. Added to the note as a `TODO: verify`.

## Unverified or judgement calls (checker, look here)

- **OTF `what_it_is`, "the later rows carry a forecast only".** A structural fact of NESO's file, not a local count; drop it if
  the checker reads it as local data.
- **OTF title "OTF network congestion"** follows `names`; "OTF" is expanded in `what_it_is`, not the summary.
- **Voltage hold line** omits the reversed-range question (budget). The `Last Updated` zone finding strengthens "when rows were
  issued" but is not on the page (domain truth not settled).
- **Voltage request list** shows two of three PDFs; the raw-feed note says "two shown".
- **Voltage related ORPS note** paraphrases that page's own summary; not checked against ORPS silver.
- Overflow at 390 checked by eye only.

## Open questions

- None blocking.

## Template problems

- None new.

## Defects (pasteable)

- **gridflow, `voltage_requirement`:** `Last Updated` is parsed as UTC from its literal `Z`, but in both captures the newest
  rows sit 57 to 58 minutes after CKAN `last_modified`; read as BST they precede it by 2 to 3 minutes. Likely UK local time
  mislabelled `Z` (a one-hour shift in BST rows). Add to the hold question and the remediation page.
- **gridflow, `voltage_requirement`:** 18 rows (two ranges by nine groups) start 2020-07-31 and 2020-08-02 with `last_updated`
  2021-07-30; probably 2021 plans keyed as 2020. Stored as published; ask NESO.
- **gridflow, `voltage_requirement`:** the file is cumulative (0 keys dropped or changed between the 2 and 16 October uploads,
  36 added), so a missed weekly upload loses no rows so far; `whole_capture` is safe.
- **gridflow, `otf_network_congestion`:** NESO restates published Actuals (3 cells of 2026-10-03 between the 7 and 14 October
  uploads) and revises far-dated Forecasts; past-dated Forecasts did not change in this pair. Settles the note's
  second-capture TODO; matters for any forward-target ruling.
- **Vault, both notes, were stale on captures** (each described one capture); fixed in this batch's vault branch.
- **Package registry status reads `eligible`** on both packages while each family is held (known pattern).
- **Manifest:** both are one-table pages and the `package_tables` entries are correct; no change suggested.
