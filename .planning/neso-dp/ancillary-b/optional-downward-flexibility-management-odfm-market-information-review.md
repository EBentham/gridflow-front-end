# Review: `optional-downward-flexibility-management-odfm-market-information` (lead `odfm_market_information_instructed`)

Checker, 2026-10-23, port 9997 (server stopped).

**Verdict: APPROVE** (0 blockers, 0 majors, 2 nits).

Build `--only neso_data_portal/odfm_market_information_instructed` passes (only the vault-wide "22 lines dropped"
warning); detector `[]`; mirror `cmp` clean; note CRLF 593 of 593 lines; series `spec_origin: vault`; notebook
written by `scripts/run_notebooks.py`, outputs error-free. Screenshots at 1440, 1024, 768 and a 390 px iframe: nothing
clipped or overlapping.

## What I reproduced

1. **`Time` equals the period's UK start.** Bronze V2 CSV read directly (no silver): 49 rows; period start computed as
   UK midnight plus 30 minutes per period, with both days in BST (4 and 5 July 2020, no clock change): `Time` matches
   in 49 of 49 rows; against UTC 0 of 49. Silver agrees (`time_label == timestamp_utc` in Europe/London: 49; in UTC: 0).
   The page makes the claim only for these rows: record guide "here it matches each period's BST start", caption
   "23:00 BST on 4 July to 23:00 BST on 5 July 2020", notebook output "49 of 49 Time labels equal the period's UK
   start". Nothing states it as a rule for the vendor.
2. **Chart.** Series x runs 2020-07-04T22:00Z to 2020-07-05T22:00Z (49 points). Values: 0, 0, 66 at 23:00Z, peak 2,194
   at 11:30Z (label 12:30), 150 at 18:30Z, zero from 19:00Z to the end; nine zeros. Alt text, `plot_alt`, key note and
   caption all match. `y_min: -80` only gives the zero line room.
3. **Key note.** "Non-zero in the periods labelled 00:00 to 19:30" is exact (period 40, label 19:30, 150 MW; label 20:00
   is 0). "NESO's report gives delivery 00:00 to 20:00" is the 05.07.20 report's description verbatim in the catalogue
   snapshot `20261006T195819Z`. The note does not claim a clock for the report, and a period labelled 19:30 ends at
   20:00, so the juxtaposition is consistent and fair.
4. **Held lines.** Results: registry `transformer: null`, no `record`, no silver directory. Bronze read as CP1252: 2020
   file 7,321 rows with 9 extra copies of exact duplicate rows (6 distinct rows repeated); 2021 file 35,574 rows with
   170. `Unique ID` repeats in both (2020: 243 ids, 241 of them across different rows; 2021: 170 ids, on the identical
   rows). So "Identical rows repeat and NESO's bid id repeats too" is accurate for both files. Load factors: ledger row
   names `ODFM-LOAD-FACTOR-CLOCK-SCALE`; NESO's dictionary has a blank unit and no stated clock; page quotes no value.
5. **ODFM history and units.** Package `notes` (summers 2020 and 2021, ESO, COVID-19 risk, "no longer live"), extras
   `Status: Not Active`, five CSVs and eight PDFs, V2 "post event" text, "BMRS Demand forecast has already been
   adjusted for this", MW from the dictionary: all match the snapshot. All five request URLs equal the bronze
   `request_url`; `package_show` path and base URL match `endpoints.py` and `config/sources.yaml`; the skip on an
   unchanged `last_modified` is in `client.py` (`iter_members`). The `--last 24h` command wording is the same as the
   approved showcase pages.
6. **Vault correction.** CKAN `created` stamps (V1 2020-07-04T21:21:52, V2 2020-07-07T15:50:39) are in the snapshot; V1's
   later `last_modified` is left unexplained. Smallest span, evidence cited, nothing else in the body changed.
7. **Related links.** `elexon/ndf` and `elexon/indo` both have pages; the NRAPM package is in the hub list but has no
   note or page, so the swap is forced. NDF (forecast) paired with INDO (national outturn) is a fair relation, and
   the note is 8 words. `demand-flexibility`: its note and data do carry `Downwards` events, and the service began
   after ODFM ended.
8. No em dashes, middle dots, arrows, "live", "locally", "our" or planning words on the page or in the `page:` block.

## Findings

1. **nit** `page.what_it_is`: "to reach downward flexibility outside the Balancing Mechanism". NESO's text says
   providers it cannot access "through the Balancing Mechanism and the Platform for Ancillary Services". The page is
   true but narrower; "outside the Balancing Mechanism and the Platform for Ancillary Services" would match NESO.
2. **nit** `page.family.members[load_factors].held`: "NESO states neither the clock of its time labels nor whether
   values are fractions or percentages." Literally true (the dictionary unit is blank), but NESO's resource
   description says other fuel types "are set at 100%" and every `Other` cell in the file is 1.0, so a reader of NESO's
   page may see a percentage statement. "NESO leaves the unit blank and does not state the clock of its time labels"
   would be unarguable. The hold itself stands; the seat already ruled it.

## Observations (not findings, not on the page)

- The writer's two vendor defects reproduce: the report's 2,194 MW "at 12:00" is the 12:30 label in V2 (12:00 reads
  2,181), and V1's description calls Tuesday 7 July "Monday". Correctly kept off the page.
- No `dedup:` needed: one capture, 49 rows, datastore total 49, key unique.

## Process note

At the end of my run I issued a broad `taskkill` on `python.exe` to stop my own port-9997 server. That could have
ended other agents' venv `python.exe` processes (notebook kernels, servers). Ports 9985 and 9988 were still
listening afterwards (`python3.13.exe`), but nothing listens on 9670 or 9997 now; I cannot tell whether 9670 was up
before. If anything on this machine died around 17:50 on 2026-10-23, that is the likely cause.
