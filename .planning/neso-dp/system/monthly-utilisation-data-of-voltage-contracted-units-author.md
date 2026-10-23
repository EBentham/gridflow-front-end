# Writer report: Monthly utilisation data of voltage contracted units

Package `monthly-utilisation-data-of-voltage-contracted-units`, one table `voltage_units_utilisation` (lead). Front-end
worktree `C:\gridflow-wt\fe-neso-sys`, vault worktree `C:\gridflow-wt\vault-neso-sys`. Writer port 9886.

## Recommendation: HOLD (written as a one-table held page)

The table has **1 silver row from 1 capture**. A full page cannot build:

- `record` is required on a non-held page (`page_fields.py` `REQUIRED`), and `gridflow-sample` refuses anything but
  exactly eight rows (`sample.py:35` `ROWS = 8`, `:160` "select picks N rows; it must pick exactly 8").
- One unit-month gives a chart of one point (a line draws nothing; a bar chart is one bar). Nothing true and useful
  can be drawn over a window.
- The monthly figures are also unclear in meaning: NESO labels a month's total in MVAr (power, not energy) and does
  not say how a month is aggregated; its dictionary examples are positive while its file's absorption is negative.

So the note carries `page.held` with the reason, and no chart, chart view, record or notebook; no artefacts were
generated (the build rejects them on a held page). The seat decides. Ways to un-hold later: more monthly uploads (eight
unit-months are needed for the frame; one unit a month would take until about March 2027), or a template change that
lets a frame show fewer than eight rows when the table has fewer. Either way, the aggregation question stays.

Held reason as written (16 words): "One row in NESO's 9 October 2026 file; how a month's MVAr is totalled is unstated."
The "one row" is the vendor file's content at a dated version (CKAN `last_modified` 2026-10-09T12:57:26), not a
local count; if the checker reads it as a local count, the alternative is the aggregation clause alone: "NESO labels
monthly totals in MVAr, a rate, and does not say how a month is summed."

Build `gridflow-build --only neso_data_portal/voltage_units_utilisation`: page written, no errors on this page
(`anatomy_errors` and `parse_page_fields` both `[]` when run on the note directly; the one error the build reports
"on pages not rendered by --only" is another writer's page). Detector `[]`. Em dashes in the page: 0. Mirror `cmp`
identical, CRLF kept. Screenshots at 1440, 1024, 768 and 390 (390 in a 390 px iframe), server on 9886 started with
its PID recorded and stopped by that PID: nothing clipped or overlapping. The site has no dark theme in its CSS, so
there is no dark view to check.

## The four questions

### 1. What one row is

- **One row = one balancing unit (BMU ID) and one calendar month**, with total injection, total absorption and their
  combined total. gridflow's entity key is `bmu_id, month_and_year` (registry
  `monthly-utilisation-data-of-voltage-contracted-units.json`, `entity_key`). NESO's dictionary names the unit and the
  month but states no key, so the page says "NESO states no key".
- **"Voltage contracted units" in NESO's words:** "the contracted units participating in Voltage 2026 service"
  (resource description, catalogue snapshot `20261006T195819Z`). Package text: "the injection and absorption of
  reactive power utilised by the unit based on the instructions provided by NESO's Control Room".
- **Utilisation measures and units (NESO dictionary, field-info snapshot `20261008T114228Z`):**
  - `Total Injection MVAr`: title "Total injection for the month (LAG MVAr)", unit MVAr, example 198.
  - `Total Absorption MVAr`: "Total absorption for the month (LEAD MVAr)", unit MVAr, example 4312.
  - `Total Injection and Absorption MVAr`: "Total (combination of absorption and injection for the month) (MVAr)",
    described as "the sum of total absorption and injection", unit MVAr, example 4512.
  - `BMU ID`: "Unique ID for the Balancing Units"; `Location`: "The geolocation of the unit" (example England).
- **The row:** `THURB-1,2 & 3`, `Aug-26`, `Thurrock`, injection 296592.1, absorption -708805.6, combined -412213.5.
  Combined equals injection plus absorption, signed (296592.1 - 708805.6 = -412213.5): a net, not the gross the
  dictionary's positive examples suggest. Measured on one row only.

### 2. Times and the clock

- `month_and_year` is a DATE, parsed from `%b-%y` (`Aug-26`) to the first of the month (registry `format`). NESO: "The
  month and year of the utilisation period". **It stands for the whole calendar month of August 2026**, not an instant.
- `timestamp_utc` = `event_time` = the start of settlement period 1 of the month's first day in UTC
  (`silver/neso_data_portal/casting.py:619-626`, `settlement_period_to_utc(value.replace(day=1), 1)`): for this row
  `2026-07-31T23:00:00Z` (August is in BST). Silver row read with Polars.
- `published_at` = `available_at` = CKAN `last_modified` of the file, `2026-10-09T12:57:26.168291`, sent with no
  offset and read as UTC (vintage `ckan_last_modified`, ADR-030). `capture_written_at` 2026-10-10T15:50:55.896317Z.
- The workbench `query()` would filter on `month_and_year` (DATE; `silver/neso_data_portal/generic.py:480`,
  `silver/date_columns.py:48`) and return times in the session zone; with no notebook on a held page, no conversion
  cell was written.

### 3. Captures, row counts and repeats

| Capture (bronze) | Bytes | Data rows | Header |
|---|---|---|---|
| `2026/10/10/raw_20261010T155055Z_e13539d0-..._556901ab.csv` | 173 | 1 | the six-column header of epoch 1 |

- One capture, one silver file, one row: no truncation and no repeats. No `dedup:` is needed; there is no chart or
  frame spec to carry one.
- **No 16 October recapture.** The bronze folder holds only 2026/10/10; the sibling System tables (`system_inertia`,
  `outturn_voltage_costs_main`) hold only 2026/10/08. The client downloads a file only when its `last_modified`
  differs from the newest capture (`connectors/neso_data_portal/client.py:1752-1765`), so an unchanged file yields no
  new capture.

### 4. Chart

None: one unit-month cannot make a true, useful chart over a window. Held page, so no chart section.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| `held`: one row in NESO's 9 October 2026 file | bronze CSV above (1 data row); meta `ckan_last_modified` 2026-10-09T12:57:26.168291 |
| `held`, `what_it_is`: month totals labelled MVAr, aggregation unstated | field-info snapshot units MVAr; no aggregation text in dictionary or package notes; note TODO SYS0-AGGREGATION |
| `summary`, `what_it_is`: units contracted in Voltage 2026, on Control Room instructions | resource description and package notes, catalogue snapshot `20261006T195819Z` |
| `what_it_is`: injection (lag), absorption (lead), the two combined | dictionary titles "LAG MVAr", "LEAD MVAr", "combination of absorption and injection" |
| `what_it_is`: dictionary examples positive, file's absorption negative | examples 198, 4312, 4512; file -708805.6 |
| `facts.vendor` | catalogue title "Monthly Utilisation data of Voltage Contracted units"; one resource, CSV |
| `facts.cadence`: monthly; updates from 9 October 2026 | extras "Update frequency: Monthly"; notes "Updates to this dataset will begin from 9th October 2026" |
| `facts.grain`: one row per unit and month; NESO states no key | registry `entity_key`; dictionary has no key statement |
| `raw_feed.note`, `requests` | `client.py` `_package_show` (:971) then whole download, skip when `last_modified` unchanged (:1752-1765); URL from bronze meta `request_url` |
| `raw_feed.commands`: `--last 24h`, "window must end recently" | `client.py:1474-1557` refuses a window ending over 48 h back (current snapshot only); same form as approved `system-inertia` |
| `how_used`, `related` | `outturn-voltage-costs` (approved, £m by voltage constraint group), ORPS page ("Grid Code generators ... reactive power", by unit and month), `voltage-requirement` (machines needed overnight by voltage group), `constraint-breakdown` note copied from the approved ORPS page; all four in the page set |

## Body corrections

- Added two sentences to "Sentinels and missing values": the dictionary's examples are all positive (198, 4312,
  4512), so the file's negative absorption and signed total do not follow them; NESO explains neither (cites the
  field-info snapshot). Nothing else in the body was wrong against code or silver: the month anchor
  (2026-07-31T23:00Z), clocks, silver columns, the combined-equals-sum check, the composite BMU ID and the file name
  change all match.
- Not changed: the body's "Holds: none" refers to gridflow's eligibility (silver is eligible), not the page. If the
  seat keeps the page held, it may want one line there saying the site page is held for thin rows.

## Unverified

- Whether "MVAr" totals are summed MVAr samples, MVArh, or something else (NESO is silent).
- Whether NESO guarantees one row per unit and month, and whether later uploads replace or add months.
- What `THURB-1,2 & 3` covers (three units reported as one row is a reading of the label, not stated by NESO); the page
  does not mention it.

## Open questions for the seat

1. Hold now (as written), or add template support for a frame of fewer than eight rows so a one-row table can ship
   with `type: none` for the chart?
2. Is "One row in NESO's 9 October 2026 file" acceptable public copy (a dated vendor fact), or use the
   aggregation-only reason?

## Template problems

- A table with fewer than eight rows cannot have a full page: `gridflow-sample` needs exactly eight and `record` is
  required. There is no way to show a short table's real rows.

## Defects

- **NESO data, voltage contracted units utilisation (`voltage_units_utilisation`): sign convention and unit unclear.**
  NESO's dictionary gives all three monthly totals in MVAr with positive examples (injection 198, absorption 4312,
  total 4512, the total described as the sum of absorption and injection), but the published file (CKAN
  `last_modified` 2026-10-09T12:57:26) writes absorption as negative (-708805.6) and the total as the signed net
  (-412213.5). A monthly total in MVAr (power) has no stated aggregation; values of hundreds of thousands suggest a sum
  of samples or MVArh. Disposition: vendor question; keep values and unit as published; site page held.
- **NESO data, same table: one row only.** The first populated file holds one unit for one month (August 2026), too
  few for a page frame. Re-check after NESO's next monthly upload.
