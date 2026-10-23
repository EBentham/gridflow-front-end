# ASDP dispatch instructions: checker review (2026-10-18)

Page `non-bm-ancillary-service-dispatch-platform-asdp-instructions`, lead `asdp_instructions`, checker port 9993.

**Verdict: REVISE.** 0 blockers, 3 majors, 3 nits. The numbers and the time-zone scoping of the sample rows are sound; the
three majors are wording that overreaches or fails the seat's condition, plus one false sentence in the vault note body.

## What passed

| Check | Result |
|---|---|
| Build `--only neso_data_portal/asdp_instructions` | ok (only the vault-wide "22 line(s) dropped" warning) |
| Detector | `[]` |
| Mirror vs canonical note | `cmp` clean |
| Chart reproduced from silver (74,137 rows, 70 files) | March 2022 starts: 1,027 rows in one file. Fast Reserve per day `[8,42,57,8,8,5,21,48,28,23,21,24,33,33,22,18,22,8,16,39,11,19,10,9,5,11,14,10,13,26,12]`, STOR on 9 days `[9,85,41,55,108,40,14,41,10]` (1st, 8th to 13th, 15th, 17th); both identical to the committed series. Alt text correct: Fast Reserve 5 (6th and 25th) to 57 (3rd); STOR up to 108 on the 11th; total highest on the 8th at 133 (next is the 11th at 129) |
| The `dispatch_date_time_stamp >= 2021-01-01` filter | Drops exactly the 2,724 June to December 2020 rows (dispatch stamp before 2021 = 2,724 = rows spelled with a space and `Z`), plus the 109 null-stamp rows. Matched rows 71,304. Inside March 2022 it removes nothing (0 rows with a pre-2021 stamp, 0 null stamps among March starts); the 4 rows with no start are the ones the caption says are not counted. The build parsed without error |
| Sample rows (29 March 2026) | Real (`gridflow-sample`). Five of the eight start 01:03, 01:03, 01:08, 01:08, 01:33; clocks went forward at 01:00 GMT that day. The 37 rows 73420 to 73456 run in unbroken time order through 01:xx; 17 dispatch stamps fall in 01:00 to 01:59 |
| "Not UK local time here" | Supported by those rows and scoped to them; the page never calls the times UTC or UK local |
| MW | Positive in all 74,123 non-null rows (3 to 100; 4 to 7 on the 14 `RDP_NEGATIVE` rows); the page says only "NESO states no sign" |
| Row identity | (`resource_id`, `entry_id`) has 0 duplicates; `entry_id` is unique across all 74,137 rows (1 to 74,647) |
| Instruction-number gap | 510 missing numbers, 360 of them 19 to 378, between August 2020 (ends 18) and October 2020 (starts 379); no September 2020 resource. Note body wording is right and hedged |
| Per-year notebook table | 2020 to 2026 Fast Reserve 2,602 / 10,798 / 9,900 / 8,927 / 15,537 / 18,330 / 6,308, STOR 122 / 680 / 776 / 26 / 6 / 1 / 1, RDP 0 / 0 / 0 / 1 / 2 / 11 / 0, mean prices all reproduce |
| `plot_alt` | 2025 Fast Reserve by hour: hour 2 = 372 (fewest), hour 6 = 1,318 (most), hours 15 to 18 = 943, 1,024, 1,009, 992; the picture matches |
| Vendor facts | `EntryID` "Sequential Number", type Integer; start, cease and stamp wording; RDP utilisation price; "always Non-Tendered" for RDP; all match the saved field info. Epoch 1 (to October 2021) has null asset, provider and tendered; request ids for June 2020, November 2021 and April 2026 match the resource table |
| Screenshots | Own captures at 1440, 768 and a 390 px iframe (chart and silver sections): nothing clipped or overlapping; chart hatches distinguish the two series; the legend repeats the service name in plain and code type (template, seat item) |
| Public copy | No em dashes, middle dots, arrows, "live", "now", "held", "locally", "since 20", "% of", no planning words |
| Server | my 9993 server stopped; 9670 untouched |

## Findings

1. **major** `page.what_it_is`: "Times are text with no zone marker."
   False for the six June to December 2020 files. In all four time columns, 2,724 rows are spelled `YYYY-MM-DD HH:MM:SSZ`
   (for example `2020-06-25 01:49:00Z`, `2020-06-25 01:47:36Z`); NESO's own dictionary example is also `2019-01-30 07:26:16Z`.
   The writer's evidence ("naive `T` spelling in every file from January 2021") covers 64 of 70 files, so the universal
   is wrong for the other 6. Fix: scope it, for example "Times are text; the files from January 2021 carry no zone marker
   (the 2020 files end in Z)", and still claim nothing about what clock either uses. The record field
   `instruction_start_date_time` ("text with no zone ... here") is correctly scoped and needs no change.

2. **major** `page.chart_view.caption` (seat ruling not met).
   The seat accepted a one-month chart "if the caption says why that month and claims nothing about other months". The
   caption gives no reason for March 2022 and its last sentence ("Fast Reserve has rows every day; STOR comes in
   bursts.") is unscoped. The notebook table shows why the choice matters: STOR instructions were 680 in 2021 and 776 in
   2022, then 26, 6, 1 and 1, so an unscoped reading would leave a visitor thinking STOR is routinely called. Fix: say
   the month was picked because both services appear in it, and scope both clauses to the month ("In this month Fast
   Reserve has rows every day and STOR comes in bursts"), with no statement about other months.

3. **major** Canonical note, "The raw time columns" body correction (vault `30-vendors/neso-data-portal/datasets/...asdp-instructions.md`,
   mirrored): "The other five spring changes in the naive files have no row in that hour, so they test nothing" is false.
   The start and dispatch columns have no row in that hour on those dates, but the cease columns do:
   - 28 March 2021: entry 5574, start 00:38:00, cease 01:12:48, cease stamp 01:11:13 (1 row in each cease column).
   - 30 March 2025: entries 54370 to 54375, all start 00:47:00, cease 01:20:00 to 01:28:36, cease stamps 01:18:45 to
     01:27:45 (6 rows in each cease column).
   Reproduced with `str.starts_with("<date>T01")` on `instruction_cease_date_time` and `cease_date_time_stamp`
   (2021-03-28: 1 and 1; 2025-03-30: 6 and 6; 2022, 2023 and 2024: 0). Fix the sentence to say which columns have rows, or
   widen the measured check: those two files also show cease times inside the skipped hour, so the same inference
   applies to them for the cease columns. The page's "here" scoping stays correct either way, and the TODO stays open.

4. **nit** `page.record.fields.instruction_start_date_time` and `instruction_cease_date_time`: the vendor definitions differ
   for RDP (start is when the dispatch was sent to the unit via the network operator; cease is when the cease was sent),
   and the guide covers the RDP difference only for the price. Add "RDP: when sent" or scope the line to the two reserve
   services.

5. **nit** `page.what_it_is`: "Each row gives start and cease times, MW, an indicative price". 109 rows have no start,
   MW or price and 203 have no cease time. "Each instruction" or "usually" avoids the universal. The caption already says
   rows with no start are not counted.

6. **nit** `page.record.fields.mw`: "MW dispatched (NESO's unit)" is unclear; NESO states the unit as MW. Suggest "MW
   dispatched, as NESO states it; NESO states no sign".
