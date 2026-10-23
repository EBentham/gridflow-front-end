# OBP reserve availability and utilisation price: writer report (2026-10-23)

Page `obp-reserve-availability-utilisation-price`, one table, lead `obp_reserve_avail_price`. The manifest's lead and
member are right (`package_tables`: slug to `obp_reserve_avail_price`).

| Gate | Result |
|---|---|
| `gridflow-build --only neso_data_portal/obp_reserve_avail_price` | ok (only the vault-wide "22 Known issues lines dropped" warning). One intermediate run reported "1 error on pages not rendered by --only"; not my page, and gone on the final run |
| Detector | `[]` |
| Canonical note vs mirror | `cmp` clean; CRLF on all 337 lines, 0 bare LF; vault diff 156 insertions, 9 deletions |
| Rendered page | 0 em or en dashes, arrows or middle dots; none of live, now, yet, soon, planned, shipped, real-time, locally, held, ledger, TODO, our, "since 20", "% of", "N rows". The "N days" hits are key notes counting chart points ("240 on 11 days", "300 on 14 days") |
| Screenshots | `.planning\neso-dp\ancillary-b\obp-reserve-avail-shots\` at 1440, 1024, 768 (slices plus full) and 390 (through a 390 px iframe). Nothing clipped or overlapping. Light only: the site has no dark theme |
| Server | my 9986 server is stopped; 9670 not touched |

Artefacts (no staged spec or authored override existed):
- `site\hifi\data\series\neso_data_portal\obp_reserve_avail_price.json`: `spec_origin: vault`, 3 series x 107 days, 103,143 rows used, 94,259 cross-capture duplicates dropped by the spec's dedup.
- `site\hifi\data\samples\neso_data_portal\obp_reserve_avail_price.json`: `gridflow-sample`, 8 rows, 16 columns.
- `site\hifi\data\notebooks\neso_data_portal\obp_reserve_avail_price.json` and `-6.png`: `run_notebooks.py`, 6 cells, no errors.

## The four questions

1. **What one row is.** One unit, one half-hour window (`time_from` to `time_to`, 1,800 s in every row), one service
   (`service_id`) and one band (`pair_id`): the MW the provider declared available for that service at gate closure
   (`availability_power`, NESO: "MW available for the service at Gate Closure for the Time From/To Period") and the
   utilisation price for it (`utilisation_price`, NESO: "Utilisation Price available for the service at Gate Closure
   for the Time From/To Period"). NESO's resource text: declared by service providers, published "once declarations
   have been accepted and validated by OBP system by gate closure", "continuously published throughout the day".
   `pair_id`: NESO's "Band specifying the MW and Price", comment "For positive service, pair would be +1; for
   negative, it would be -1". In both captures `NQR` rows carry only -1 and `PQR`/`PSR` only +1 (notebook cell two
   shows `[-1]`, `[1]`, `[1]`); one band per unit, window and service (the 3-column keys are unique too). `data` is
   always `AV` (NESO: fixed value). NESO never decodes `PQR`/`NQR`/`PSR`/`NSR`; the page labels them Positive Quick,
   Negative Quick and Positive Slow Reserve (see Unverified).
2. **Time columns.** `Time From`/`Time To` are spelled `YYYY-MM-DDTHH:MM:SS` with no zone marker in every cell of both
   captures (awk over all 310,704 data lines: 0 non-matching). NESO's dictionary gives unit "UTC" with examples ending
   in `Z`; the registry reads them as UTC. Unlike the instructions file, these rows DO test it: the file spans both UK
   clock changes, and on 29 March 2026, when UK clocks went from 01:00 to 02:00, it has windows starting 01:00 and
   01:30 (three rows each, notebook cell three), times that did not exist in UK local time; 26 October 2025 has 48
   windows and no repeated key. So the text is not UK local time, and fits UTC. Two corroborations, both observations:
   the file-name number equals the UK settlement period of the last window read as UTC (`_27` for 12:00 UTC on
   8 October, `_46` for 21:30 UTC on 16 October), and all 74 instruction STARTs that find a declaration for the same
   unit, service and half-hour (both as UTC) carry the identical price. The page says "Times are UTC, NESO says; the
   text has no zone marker"; the evidence is in the note body. The workbench returns the TIMESTAMPTZ columns in the
   session zone (Europe/London), so the lead says so and cell one converts `time_from`, `time_to` and `timestamp_utc`
   to UTC.
3. **Units and signs.** From NESO's dictionary only (field-info snapshot `20261008T114228Z`): `Availability Power` MW,
   `Utilisation Price` £/MWh (a per-energy price, not £/MW/h). No sign convention for the price; the page says "no
   sign stated". Observed: `NQR` prices are negative on 1,194 rows and reach -10,000; `PQR` reaches 10,000; both
   extremes only on 0 MW rows of `EDFE-11`/`EDFE-8` between 18 and 25 November 2025 (note body). The ±10,000 appears on
   the page only through the notebook's summary output ("Prices reach ±10,000" in the lead).
4. **Duplicates, overlap, truncation.** Two captures, both whole files ending in a newline:
   8 October (`av_20261008_27`, 150,309 rows, 10,215,008 bytes) and 16 October (`av_20261016_46`, 160,395 rows,
   10,900,128 bytes). The newer is larger, so no truncation; build from `_latest` (16 October). Both start at
   2025-10-09T10:00:00. The 16 October file is a strict superset: all 150,309 earlier keys present with identical
   `time_to`, MW and price; the 10,086 new rows all start after the earlier file's last window. 0 duplicate keys and
   0 duplicate rows within either capture. Silver holds both captures, so the chart spec and the frame select dedup on
   the entity key by `published_at` (the chart dropped 94,259 cross-capture copies).

## Chart choice

Line, mean `utilisation_price` per UTC day by service over rows with `availability_power > 0`, 1 July to 15 October
2026 (all three services declare every day there; Positive Slow Reserve starts 8 May 2026 and the earlier months are
few units). Filtering out 0 MW rows also removes the ±10,000 rows. Unweighted by MW, stated in the caption. Rejected: a
full-year line (November's mean of a few units runs to 500 to 1,000, flattening the rest); total MW per window (put in
the notebook plot instead, so the page shows both columns).

## Evidence

| Claim (page field) | Evidence |
|---|---|
| summary, `what_it_is`: MW available at gate closure and a utilisation price, per half-hour, Quick and Slow Reserve, non-BM, on OBP | package notes and resource description (catalogue snapshot `20261006T195819Z`); dictionary descriptions of `Availability Power`, `Utilisation Price`, `Time From/To` |
| "NESO publishes them once OBP has accepted and validated them" | resource description: "once declarations have been accepted and validated by OBP system by gate closure" |
| "`pair_id` +1 marks a positive service, -1 a negative one" | dictionary comment on `Pair ID` |
| "Times are UTC, NESO says; the text has no zone marker" | dictionary unit "UTC"; registry `zone: UTC`; bronze cells such as `2026-10-14T17:00:00` |
| facts.vendor "one CSV, republished under a new file name" | registry one resource, `url_type: upload`; file names `av_20261006_44`, `av_20261008_27`, `av_20261016_46` |
| facts.cadence "Ad hoc, NESO says, and published through the day" | extras "Update frequency: Ad hoc"; notes "continuously published throughout the day" |
| facts.grain; Key | registry `entity_key: [unit_id, time_from, pair_id, service_id]` |
| chart caption | spec: filter `availability_power gt 0`, dedup on the key by `published_at`, `aggregation: mean`, `time_bucket: 1d` on `time_from` (UTC), window 2026-07-01 to 2026-10-15 inclusive (`distil.py` adds a day to the end) |
| alt and key notes | committed series: slow min 171.48 (4 Jul), max 322.327 (18 Jul), 237.191 to 279.083 from 1 Sep; quick 200.118 (12 Jul) to 240, 240 on 11 days 13 to 28 Jul, 203.25 to 208.379 from 2 Aug to 29 Sep, 218.294 to 221.76 after; negative 300 on 14 days 13 to 28 Jul, otherwise 154.286 to 287.143 |
| key labels Positive/Negative | inference: dictionary examples `PQR, NQR, PSR, NSR`, the `pair_id` comment, and `NQR` = -1 only (notebook output) |
| raw requests | `package_show` as on the approved upload pages; the download URL is the 16 October capture's `request_url` (bronze sidecar) |
| raw note "downloaded whole unless its `last_modified` is unchanged" | `client.py` `iter_members`, the upload skip at about lines 1751 to 1767 |
| commands `--last 24h` | same form as the approved upload pages; silver partitions by capture date |
| frame caption | sample rows: window 2026-10-14T17:00 UTC; `ENGQR-05` has `NQR` (-1, 180.0) and `PQR` (+1, 140.0) |
| field `service_id` | values in this file `PQR`, `NQR`, `PSR`; dictionary example adds `NSR`; no expansion anywhere |
| field `time_to` "30 minutes after `time_from` in these rows" | the eight rows |
| field `data` | dictionary: fixed value "AV" |
| field `timestamp_utc` | registry `temporal: utc_instant` on `time_from`; equality on every silver row (0 mismatches) |
| field `published_at` "one per capture" | registry `vintage: ckan_last_modified`; one value per capture in silver |
| notebook lead | `_latest` = every row of the newest complete capture (`latest_views.py`, `whole_capture`); generic NESO date column `timestamp_utc`; `_date_range_predicate` half-open UTC bounds, end date included; outputs printed `+00:00` after conversion |
| notebook outputs | NQR `[-1]`, 11 units, 49 MW top, -10000 to 300; PQR `[1]`, 19, 49, 0 to 10000; PSR `[1]`, 40, first 2026-05-08 05:00, 55, 0 to 2599.04; 29 March windows 00:30, 01:00, 01:30, 02:00 with 3 rows and 3 units each |
| `plot_alt` | Polars sums for 14 October 2026: PSR 201 to 207 to 04:30, 177, 147 from 06:00, 237 from 09:30 to 13:30, 140 from 14:00 to 19:30, then 169, 155, 173; PQR 3 to 5; NQR 0 to 6 |
| related | all four slugs in the page set; instruction units overlap (21 of 24) |

## Body corrections (canonical note, smallest spans)

1. **File name token.** Added the observation that the number is the UK settlement period of the last window read as
   UTC (27 and 46), marked not documented. The `TODO` stays.
2. **Second capture.** Added a "Captured again" bullet for the 16 October capture (rows, bytes, stamps).
3. **Vintage.** "For the one capture to date" became "For the first capture", plus the 16 October vintage.
4. **Event time.** Added the clock-change evidence (29 March 01:00 and 01:30 windows; 26 October 48 windows) and that
   no cell in either capture has a zone marker.
5. **Mixed horizon.** Replaced "no repeated same-resource capture exists yet" with the two-capture comparison (no
   revision or removal, no roll-off over eight days); the `TODO` narrows to longer spans.
6. **Value ranges.** Added where the ±10,000 sit (0 MW rows, two units, 18 to 25 November 2025).
7. **New bullet: against the OBP instructions** (project check): 21 of 24 units, RDP missing; 74 of 85 STARTs match a
   declaration and all 74 prices are equal.
8. **Identity.** Cross-capture identity now records the two-capture result; longer-run identity stays `TODO`.

## Unverified

- **Service codes.** NESO never decodes `PQR`, `NQR`, `PSR`, `NSR`. The labels Positive Slow, Positive Quick and
  Negative Quick Reserve rest on the dictionary's examples, the `pair_id` comment and the data. If the checker wants it
  softer, the key labels can read the codes only.
- **What a negative utilisation price means** for a negative service, and whether ±10,000 is a cap, floor or default.
- **Which gate closure** NESO means; the 16 October capture holds windows up to an hour after its `last_modified`.
- **Retention.** Both captures start at 2025-10-09T10:00; whether NESO ever trims the head is unknown.
- The notebook needs a capture from 16 October 2026 on; a later capture would hold the same rows only if NESO keeps
  them.

## Open questions

None blocking.

## Template problems (seat items)

1. **Folded frame at 390 px** shows only two columns (`unit_id`, `service_id`) before `…`, whatever the order; the
   values sit behind the fold on phones. At 768 and wider, price and MW show (I put them third and fourth).
2. Known: the notebook tab label is truncated with an ellipsis at 390 px.
3. Both distil and sample read every silver file, so a `whole_capture` table with several captures needs an explicit
   dedup in the spec and select; without one the chart would average each row twice. Worth a build check or a
   default to the newest capture for `whole_capture` tables.

## Defects

- **NESO data: ±10,000 £/MWh utilisation prices on 0 MW rows.** Package `obp-reserve-availability-utilisation-price`,
  units `EDFE-11` and `EDFE-8`, windows 18 to 25 November 2025: `NQR` -10000 on 75 rows, `PQR` 10000 on 37, all with
  `availability_power` 0. NESO documents no cap, floor or placeholder. gridflow keeps them as published (correct);
  consumers averaging prices must filter 0 MW rows. Recorded in the note.
- **NESO metadata: "Ad hoc" against "continuously published throughout the day"** (already in the note; repeated
  for the backlog only if not logged).
- **gridflow front-end (seat item): distil and sample read all silver captures of a `whole_capture` table.** Without
  a dedup the chart and frame would double-count every row present in both captures (94,259 here). This page sets the
  dedup; other `whole_capture` pages with two or more captures should be checked.
- **gridflow_models (known, logged with the instructions page):** `query()` returns TIMESTAMPTZ columns in the session
  zone; the notebook converts.
- **Vault note (fixed here):** stale single-capture statements (vintage, revision `TODO`, cross-capture identity).
