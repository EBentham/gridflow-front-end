# Dynamic Containment, Regulation and Moderation results: writer report

Page `dynamic-containment-data`, lead `dynamic_containment_dc_dr_dm_results`. Build `--only
neso_data_portal/dynamic_containment_dc_dr_dm_results` clean, anatomy check `[]`, detector `[]`. Screenshots at
1440, 1024, 768 and a 390 px iframe, every section looked at; one clip at 390 (the caption's 52-character table key)
fixed by naming the bare table key. Nothing else clipped or overlapping.

## The headline problem: the lead's `_latest` view is truncated (data defect, not on the page)

The weekly re-check of the frozen package on 2026-10-16 (the daily refresh, gridflow ruling 889) stored a second
results-by-unit capture, `raw_20261016T200702Z_..._5cf75ba8.csv`, 25,461,781 bytes and 224,000 data rows, against the
2026-10-08 capture's 45,481,922 bytes and 397,662 rows. `cmp` reaches the end of the short file at byte 25,461,781
with no earlier difference: it is a byte prefix of the full body, cut on a row boundary (224,000 is seven 32,000-row
chunks of a CKAN datastore dump stream). The dump is ordered by date, so the short capture is complete to EFA date
2023-04-01, partial on 2023-04-02 (458 of 712 rows) and missing 2023-04-03 to 2023-11-02 (214 dates).

`silver_neso_data_portal_dynamic_containment_dc_dr_dm_results_latest` now returns the short capture (224,000 rows,
`capture_written_at` 2026-10-16), so `data.neso_data_portal.query("dynamic_containment_dc_dr_dm_results", ...)`
silently ends at April 2023. Cause in code: `_download_dump` (`connectors/neso_data_portal/client.py` around line
1361) admits any complete-status 200 body; the dump sends no `Content-Length` (`declared_content_length: null`) and
nothing compares the parsed row count with the datastore's `total`. A body that differs from the newest capture's hash
is stored as new (`client.py` around line 1950), and the completion record marks it complete. The other four members
were re-downloaded with identical hashes and not stored.

How the page avoids it, without mentioning local data:
- Chart: `dedup` on (`service`, `efa_date`, `efa`) collapses the two captures (the short rows are byte-equal), one row
  per block. Both captures' rows feed it; rows used 9,023 (4,658 `DCL` and 4,365 `DCH` blocks), as in the full capture.
- Frame: filtered to `capture_written_at < 2026-10-09`, so it shows the complete capture and stays valid if the short
  capture is removed.
- Notebook: the window (20 to 26 June 2022) sits inside the complete part of the short capture, so `query()` returns
  the same 3,318 rows from either capture.

Ship rather than hold: the chart, rows and notebook are right for NESO's data; the defect is in gridflow's capture,
which the seat can fix (remove or quarantine the 2026-10-16 results capture and its silver file, and add a row-count
check). If the seat prefers, a hold until the view is repaired is defensible, since a reader of this page who widens
the notebook window past March 2023 gets short results from our warehouse.

## Lead choice and chart

Results is the right lead: it is the only table with an unambiguous price unit (its own dictionary: "The cleared price
per MW per hour", unit £/MW/h), a vendor date column (`efa_date`) that `query()` filters on, and the reading a
practitioner wants (what each service cleared at, block by block). Block prices are labelled £/MW with no hour basis;
masterdata is a different regime (the 2020 to 2021 daily tender) with fees in £.

Chart: daily unweighted mean of the block clearing price, `DCL` and `DCH`, EFA dates 16 September 2021 to 2 November
2023, £/MW/h. DR and DM are left out (six lines would be unreadable; the caption says so). The x axis is NESO's EFA
date label, not a time, so the local-window ruling does not arise.

## Evidence

| Claim | Evidence |
|---|---|
| One row of results: a unit, service, EFA date and EFA block; key `unit_name, efa_date, efa, service` | Note (FACTS 6.3: unique over 397,662 rows); dedup on the key over both captures gives 397,662 |
| `cleared_volume` MW, `clearing_price` £/MW/h | Saved field info `dynamic_containment_dc_dr_dm_results.json` (unit cells MW and £/MW/h; "The cleared price per MW per hour.") |
| Accepted units only | Dictionary: "volume of response that was accepted"; `cleared_volume` min 1.0 per service (no zero rows) |
| One price per service, date and block | Polars over the 2026-10-08 capture: 19,211 blocks, 0 with more than one `clearing_price`, 0 nulls; notebook `prices` column 1 on every block shown |
| `DCL` to `DMH` meanings | Linear-orders dictionary `MarketName`: "DCL (Dynamic Containment Low Frequency), DCH (... High Frequency), DRL, DRH, DML, DMH ..." |
| Retired; NESO points to EAC | FACTS 6 (package page: no longer updated, directs to EAC); vendor metadata "Update Frequency: Not Active"; `eac_results_summary` carries `DCL`, `DMH` etc. as service type Response |
| Service days 2 October 2020 to 2 November 2023 in NESO's files | Masterdata `delivery_date` 2020-10-02 to 2021-09-15; results `efa_date` 2021-09-16 to 2023-11-02 (FACTS 6) |
| Four datastore tables, one uploaded file | Note "Files by disposition"; sidecar `url_type` datastore for four, masterdata `download/dynamic_containment_masterdata.csv` |
| Requests | Sidecar `request_url` of each member (dump URLs; masterdata resource download URL) |
| Frozen: re-checked at most weekly; unchanged bodies not stored again | `client.py` `_FROZEN_CADENCE = timedelta(days=7)`, `_frozen_not_due`, hash comparison before storing |
| Commands `--last 24h` | Same form as the approved showcase and batch pages; the window end is the frozen cadence clock and partition |
| `efa_date`: "delivery end's date" | Results dictionary: "Equivalent date to the delivery end date in this instance." |
| `efa` 1 to 6, six four-hour blocks a day | Dictionary: "The week is split into 42 blocks, with 6 four-hour blocks each day" |
| `timestamp_utc` is the start of the EFA date in UK time, as UTC | Silver: equals `event_time` on every row (`date_sp1(efa_date)`); 2022-06-25 rows carry 2022-06-24 23:00Z |
| Block: sell orders, executed or rejected, MW negative | Block `status` Executed 478,875 / Rejected 249,919; dictionary "highest-priced sell order executed"; note: `volume` negative on every row |
| Masterdata: daily DC low-frequency tender, fees in £ | Dictionary `Market Name` "Dynamic Containment Low Frequency" (`DC LF`), "24 hours contract", Availability Fee unit £ |
| DCH first on 4 November 2021; DR from 9 April, DM from 7 May 2022 | Results `efa_date` min per service |
| Alt and key numbers | Committed series: `DCL` 17.00 to 31 October 2021, max 77.608 on 2022-06-25, under 2 on 145 of 306 days in 2023, min 0.235 on 2023-04-01; `DCH` from 2021-11-04, deciles 1.08 to 7.34, max 17.438 on 2023-06-15, above `DCL` on 200 of 306 days in 2023 |
| Plot alt | Notebook frame: `DCL` 4.07 to 69.95 on 20 to 24 June, 59.00 or more on 25 and 26 June, 105.00 in block 5 of 25 June; `DCH` 0.80 to 8.90 |
| Held lines | Eligibility report rows for DC-SUMMARY-PRICE-UNIT and DC-LINEAR-PRICE-UNITS; summary dictionary: "The cleared price per MW per hour" with unit £/MW |

## Held members (as printed)

- `dynamic_containment_dc_dr_dm_results_sum`: "NESO's dictionary calls its clearing price per MW per hour but labels it £/MW."
- `dynamic_containment_dc_dr_dm_linear`: "NESO's dictionary labels some curve prices £/MW and others MW, with no hour basis."

## Body corrections (canonical note)

1. "Files by disposition": "Every resource has exactly one capture (2026-10-08)" was false; now says one complete
   capture each, plus the truncated 2026-10-16 results capture and that `_latest` selects it.
2. "Cadence": "The registry refresh is `frozen`, so nothing re-fetches on a schedule" was wrong; now cites
   `client.py` `_FROZEN_CADENCE` and `_frozen_not_due` (re-checked at most every 7 days, identical bodies not stored).
3. Results "Silver" line: two Parquet files (397,662 plus 224,000 rows), not one.
4. Results "Coverage": added the vendor's service-code meanings (linear dictionary) and the one-price-per-block
   measurement, dated.

## Unverified or open

- The delivery text clock (block 1 written as 23:00 the evening before, the same hours in summer and winter) still
  has no vendor statement; the page keeps it as text and states no clock.
- Masterdata `total_cost` equals `availability_fee` x `volume_accepted` x `service_duration` on every accepted row in
  the file, which suggests the fee is £/MW/h; NESO labels it £ only, so the page does not say so.
- Block `block_code` holds `C88` (230,259 rows) and `paradoxically` holds `PRB` (40,349 rows), neither in NESO's
  dictionary (C01/C02; a yes/no flag). Not shown on the page.
- The masterdata `delivery_date` covers the 24 hours from 23:00 UK time the evening before (observed); the member
  line says "October 2020 to September 2021", which holds either way.

## Template problems (seat items)

- A family page does not print `raw_feed.requests` (the `package_show` line); the EAC BR showcase page lacks it too.
- At 390 a long silver key in the chart caption is not wrapped and clips at the right edge; avoided here by naming
  the bare table key.
- At 768 and 390 the notebook preview breaks long names mid-word (already listed).

## Defects

- **gridflow, NESO Data Portal dump capture: truncated datastore dumps are admitted as complete captures.** On
  2026-10-16 the frozen re-check of `dynamic_containment_dc_dr_dm_results` (resource
  `ddc4afde-d2bd-424d-891c-56ad49c13d1a`) stored `bronze/neso_data_portal/dynamic_containment_dc_dr_dm_results/2026/10/16/raw_20261016T200702Z_ddc4afde-d2bd-424d-891c-56ad49c13d1a_5cf75ba8.csv`,
  224,000 rows and 25,461,781 bytes, a byte prefix of the 2026-10-08 body (397,662 rows, 45,481,922 bytes; `cmp`
  EOF on the short file at line 224,001 with no earlier difference). Its hash differed, so it was stored as a new
  capture, transformed, marked complete, and `silver_neso_data_portal_dynamic_containment_dc_dr_dm_results_latest` now
  serves it: EFA dates after 2023-04-02 are missing and 2023-04-02 is partial. `_download_dump` has no completeness
  check (no `Content-Length` on dumps; no comparison with the datastore `total`). Fix: compare the parsed row count
  with `datastore_search?limit=0` `total` (or the field-info `total`) before admitting a dump; then remove or
  quarantine the 2026-10-16 capture and its silver file (snapshot first) and re-run the results view. Check every
  other datastore family for captures since 2026-10-15 whose row count fell.
- **Vault, dynamic-containment-data note:** stale capture count and frozen-cadence description (corrected on this
  branch, see Body corrections).

## Nits fixed (review: APPROVE, 5 nits)

1. `page.raw_feed.note`: now "`package_show`, then each datastore table's whole dump, re-checked at most weekly,
   unchanged bodies not stored; the uploaded masterdata when its `last_modified` changes" (`client.py` around line
   1752: an upload is skipped while its CKAN `last_modified` equals the newest capture's; only dumps follow the 7-day
   cadence).
2. Note body: the results section now says one complete capture (2026-10-08) and one truncated capture (2026-10-16,
   25,461,781 bytes); `Cadence` says one complete capture per resource, results also holding the truncated one.
3. `page.notebook.lead`: "The second cell" is now "The next cell".
4. `page.record.fields.timestamp_utc`: "UK midnight starting the EFA date's calendar day, as UTC; not the block start".
5. `page.family.members[0].differs`: "accepted units only" removed (NESO does not say rejected units are excluded);
   now "Each unit's cleared MW (NESO: the volume accepted) and its block's clearing price, £/MW/h", quoting the
   dictionary's `Cleared Volume` text.

Re-mirrored (`cmp` identical, CRLF intact), rebuilt `--only neso_data_portal/dynamic_containment_dc_dr_dm_results`
with no errors, detector `[]`. Text-only changes; no artefact needed regenerating (build digests pass).

All five review nits fixed; page rebuilt clean with detector [] and the mirror identical.
