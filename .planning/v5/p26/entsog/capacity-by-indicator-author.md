# entsog/capacity-by-indicator: author report

Writer: Opus 5.5 · high, 2026-10-07. Family `capacity-by-indicator`, lead `firm_available`, nine further members (`firm_booked`, `firm_technical`, `interruptible_available`, `interruptible_booked`, `interruptible_total`, `available_through_oversubscription`, `available_through_surrender`, `available_through_uioli_long_term`, `available_through_uioli_short_term`). Built with `--only entsog/firm_available`.

## Recommendation: HOLD

The page is built, accurate and states the loss, but silver misleads overall for this family. Three of the seat's hold triggers apply:

- **Arbitrary picks.** The generic ENTSOG transformer keeps a capacity record only when its validity period starts on the fetched gas day. Interconnector's 30-day record (2 Aug to 1 Sep) and 7-day record (21 to 28 Sep) are kept only because they happen to start on a fetched day. The same operators' other records are dropped every day. National Gas TSO's 2022-2028 Bacton (IUK) exit record is one example.
- **Members with no values.**
  - `firm_technical` holds 0 valued rows (28 not-applicable placeholders).
  - The four "available through" members hold 0 valued rows (55 default-sentence rows each).
- **Repeated rows and wrong-looking stamps** in the four "available through" members:
  - National Gas TSO `ITP-00090` entry appears three times a day (one per adjacent operator in `id`).
  - Every kept row is stamped 22:00 UTC on the previous day, so the 3 Aug partition holds rows dated 2 Aug.

The chart (GNI's one-day Moffat (IE) entry records, all kept) and the eight rows avoid misstatement, and the page says what silver drops. But a reader of nine of the ten members gets mostly placeholders. Ship once the silver fix (Defect 1) lands and the artefacts are regenerated. **The sample artefact must be regenerated anyway** (see Status).

## Status

- **Build:** `gridflow-build --only entsog/firm_available` passes.
  - The only warnings are the generic "no Pydantic class" notices and other vendors' empty-schema notices.
  - `wrote: data-sources/entsog/capacity-by-indicator.html`; the nine member pointers were rewritten.
- **Detector:** `detect.mjs --json` returns `[]`. Em dashes in the page: 0.
- **Rubric greps** on the rendered text (locally, held, our, since 20, % of, live, now, yet, soon, planned, coming, real-time, digits plus rows or days, →, middle dot) find nothing. Every "row" hit is the guide, `shape` or the "no capacity made available' rows" member lines.
- **Mirrors:** all ten notes copied with `cp` and checked with `cmp`: 10 of 10 byte-equal, CRLF kept.
- **Artefacts:**
  - `site/hifi/data/series/entsog/firm_available.json` (`spec_origin: vault`, 1 series × 9 points).
  - `samples/entsog/firm_available.json`.
  - `notebooks/entsog/firm_available.json` plus `firm_available-5.png`.
  - There was no staged chart spec and no authored override to retire.
- **Sample artefact, read this:** `gridflow-sample` cannot read `entsog/firm_available` silver.
  - `_scan` (`src/gridflow_front_end/sample.py:51-62`) scans every partition with the newest file's schema. `capacity_booking_status` is Null dtype in the 21 Sep partition and String in older ones, so `collect()` fails with "data type mismatch for column capacity_booking_status: incoming: String != target: Null".
  - No `record.select` can avoid it, and every sibling with real values drifts the same way. Distil succeeds only because it projects four columns.
  - To build and screenshot a reviewable page, I ran `gridflow-sample`'s own `main()` from `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\cap\sample_relaxed.py` with only `_scan` replaced by a per-file `pl.concat(how="diagonal_relaxed")`, column order kept from the newest file. Same select, same eight real silver rows, same payload code, `generated_by: gridflow-sample`.
  - **The seat should fix `_scan` (template problem 1) and rerun `gridflow-sample --dataset entsog/firm_available`.** I did not edit any Python.
- **Screenshots** (light; the site has no dark theme) at 1440, 1024 and 768, and 390 in a true 390 px iframe: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\cap\shots\s_<width>_<n>.png` and contact sheets `sheet_390_b.png`, `sheet_1024.png`, `sheet_768.png`.
  - Nothing is clipped or overlapping: the hero, the ten member chips (wrapped at 390), facts, scenery, chart and ticks (`140M` to `180M`), key, all ten request URLs, commands, the folded frame, the guide, the notebook and related.
  - One cosmetic template quirk at 390: `&indicator=Available+through+Surrender` wraps mid-word after an empty line (template problem 3).
  - The static server on 9873 is stopped; 9670 was not touched.

## What the data is (the "look hardest at" answers)

- **What one row is.**
  - A row is one vendor capacity record: a value valid from `periodFrom` to `periodTo` for one operator, point and direction.
  - It is not a per-gas-day measurement. In 2026-08/09 bronze, validity runs from one day (GNI Moffat entry, the not-applicable placeholders) through weeks (Interconnector) to decades (BBL company 2015/2018 to 2048).
  - The connector sends one request per gas day (`client.py:78-102`), and ENTSOG returns the record that covers that day.
- **Key and dedup.**
  - Dedup is on the vendor `id`, `keep="last"`, per daily bronze read (`generic.py:193-199`).
  - Firm and interruptible: `id` joins indicator, keys, unit and the period dates. Placeholders use a fixed `2026-01-012027-01-01_NA<n>` range. The 4-tuple `(timestamp_utc, operator_key, point_key, direction_key)` is unique in all six tables.
  - "Available through": `id` is dateless and names an adjacent operator. The 4-tuple repeats five times per table (National Gas TSO `ITP-00090` entry ×3 a day, ids ending `IE-TSO-0001`, `IE-TSO-0002`, `UK-TSO-0002`).
- **The silver loss (the headline).**
  - `GenericEntsogJsonTransformer` sets `date_window_dataset = endpoint.requires_dates` (`generic.py:332`).
  - It then runs `partition_records_to_target_date` on each bronze file (`:157-161`), keeping a record only when the local date of its `periodFrom` equals the bronze day (`datetime.py:56-87`, `:191-213`).
  - `tariffs` and `tariff_simulations` are exempt for exactly this reason (`generic.py:297-306`, VTA-ENTSOG-TARIFF-01); capacity indicators are not.
  - 2026-08/09, bronze records (with a value) against silver rows (with a value):

    | Member | Bronze | Silver |
    |---|---|---|
    | firm_available | 126 (84) | 59 (17) |
    | firm_booked | 126 (84) | 59 (17) |
    | firm_technical | 126 (98) | 28 (0) |
    | interruptible_available | 126 (112) | 21 (7) |
    | interruptible_booked | 126 (112) | 20 (6) |
    | interruptible_total | 126 (112) | 21 (7) |
    | available_through_oversubscription / surrender / uioli_long_term | 70 (15) each | 55 (0) each |
    | available_through_uioli_short_term | 55 (0) | 55 (0) |

  - Which values survive in firm_available and firm_booked: GNI Moffat (IE) entry on all 14 days (one-day records), plus Interconnector Bacton (IUK) entry on 1 and 2 Aug and exit on 21 Sep.
- **Coverage windows, stated plainly.**
  - Firm and interruptible bronze and silver hold 14 gas days: 1 to 5 August and 13 to 21 September 2026.
  - The four "available through" members hold 5 bronze days, 1 to 5 August. Their kept rows are stamped 22:00 UTC the previous day, hence DATA-MATRIX's "31 Jul to 4 Aug".
  - Silver row counts match DATA-MATRIX (59, 59, 28, 21, 20, 21, 55 × 4).
- **Points requested.** Nine `pointDirection` filters (`endpoints.py:24-34`). Unlike nominations, every filter returns one record per day for firm and interruptible (BBL company's `ITP-00063` included). `meta.count` equals `meta.total` (9; 14; 11 for UIOLI short-term) in every body, so there is no `total` > `count` question here.
- **Placeholders.**
  - Firm Available and Firm Booked placeholders come from National Gas TSO `ITP-00090` entry ("Virtual Point, currently Moffat is only Unidirectional exit"), National Gas TSO `ITP-00207` exit ("Virtual Point, currently BBL is only Unidirectional entry") and GNI `ITP-00495` exit ("Not currently systemised in TSO System"). Firm Technical has only the two National Gas TSO placeholders. Interruptible has GNI `ITP-00495` entry ("Firm Only").
  - All carry `isNA` 1, `value` `""` (null in silver) and `periodFrom` 05:00+02:00, which is 03:00 UTC, an hour before valued rows.
- **Units.** `unit` is `kWh/d` on every firm and interruptible row. On every kept "available through" row it is `""`; the dropped valued records there are `kWh/d`. The generic transformer does not convert (`generic.py:189-191` only casts `value` to Float64, `strict=False`).
- **Time stamps.**
  - `timestamp_utc` is a copy of `period_from` (`generic.py:185-187`): the start of the record's validity, in UTC. That is 04:00 UTC for valued rows (06:00+02:00 as sent) and 03:00 UTC for placeholders. On "available through" sentence rows it is 22:00 UTC (00:00+02:00, zero-length period).
  - `last_update_date_time` is the vendor's `lastUpdateDateTime` in UTC, not used by the pipeline. Placeholders carry 2025-02-20.
  - `ingested_at` is the silver transform time (`generic.py:201-206`).
  - No stamp is a publication or issue time.
- **Indicator semantics.** The notes quote no ENTSOG definition; their overview lines are authored paraphrases. The only vendor wording is the "available through" `defaultSentence`: "Currently no capacity has been made available on this point through the application of the congestion-management procedures". The page avoids definitions beyond indicator names, the default sentence and the observed identity below.
- **Available = technical − booked (observation only).**
  - Firm: it holds exactly on every valued point and gas day in 2026-08/09 bronze (6 valued points × 14 days). In silver only GNI Moffat entry has both sides daily: available + booked = 433,368,000 on all 14 days, and the notebook prints it for 13 to 21 Sep.
  - Interruptible: no such identity. At GNI Moffat exit, Interruptible Total equals Interruptible Booked (0 to 160,001) while Available is about 80,000,000. At BBL company Julianadorp entry, Total and Booked are 0 while Available is 494,400,000.
  - Reported in the vault as project checks; the page shows only the firm sum, which is visible in the notebook.
- **Partition dtype drift.** A column that is all-null in a day's response is written as Null in that partition and String elsewhere:
  - `capacity_booking_status` in firm_available and firm_booked;
  - six columns in the interruptible tables (`is_unlimited`, `interruption_type`, `restoration_information`, `capacity_type`, `capacity_booking_status`, `is_cam_relevant`).

  `pl.read_parquet` over a member's glob fails, and so does the sampler. `data.entsog.query()` (DuckDB) reads them fine.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Request URL, nine filters, `+` encoding (`raw_feed.requests`, `family.members[].request`) | `request_url` in bronze `.meta.json` for 2026-09-21 (firm, interruptible) and 2026-08-05 ("available through"), copied verbatim; `endpoints.py:24-34,95-125,263-287` |
| One request per gas day; ingest `--end` exclusive, transform `--end` inclusive | `client.py:78-102` (`day_subwindows`, one `from=to=D` call per day); same lines as the approved nominations page |
| "Silver keeps a record only when its period starts on the fetched gas day" (`what_it_is`, caption, `differs`) | `generic.py:157-161,332`; `datetime.py:56-87,191-213`; the bronze-against-silver table above |
| "records valid over a period, from one day to decades" (`what_it_is`, `facts.cadence`) | Bronze `periodFrom`/`periodTo`: GNI one-day; BBL company 2015-10-30 / 2018-01-01 to 2048-12-13 |
| `value` and `unit` unconverted; kWh/d (summary, `raw_feed.note`, fields) | `generic.py:189-191`; `unit` `kWh/d` on all 59 lead rows |
| Grain and key (`facts.grain`, `record.key`) | Dedup on `id` (`generic.py:193-199`); 4-tuple unique in lead silver (0 duplicate groups) |
| `timestamp_utc` = start of validity from `periodFrom`, UTC; x_label "starting 04:00 UTC" | `generic.py:181-187`; all nine charted rows at 04:00 UTC |
| Chart values and alt text | Committed series: 145,654,424; 162,488,829; 170,379,342; 170,371,375; 170,379,481; 170,299,881; 170,746,545; 170,746,023; 163,891,514 |
| "GNI sends a one-day record each day" (caption, `differs`) | Lead silver: GNI `ITP-00495` entry `period_to` = `period_from` + 1 day on all 14 rows |
| Key note "firm available plus firm booked is 433,368,000 every day here" | Notebook cell 4 output: `available_plus_booked` 433368000.0 on all nine days |
| `plot_alt` numbers | Notebook output: booked 287,713,576 (13th), 262,621,455 to 263,068,119 (15th to 20th), 269,476,486 (21st); available 145,654,424 to 170,746,545, 163,891,514 (21st) |
| `notebook.lead` (relation, date column, ends included, lineage dropped) | Same `query()` path as the approved nominations page (`schema_manifest.py`, `gridflow_models/research/handles/source.py:401-451`); `query()` ran on both members |
| Eight rows and caption | Sample: 2 Aug and 21 Sep at `ITP-00005`, `ITP-00090`, `ITP-00495`; shape (8, 42) |
| Field lines `is_unlimited` "kept as text", `is_cmp_relevant` "kept as text", `original_period_from` "set only on the placeholders here", "empty or null here" | Lead silver dtypes (String) and the eight rows' values |
| "available through" members hold only "no capacity made available" rows (`differs`) | 55 of 55 rows with `is_default_sentence` true in each of the four tables; `default_sentence` text as quoted |
| `how_used[2]` "ENTSOG's statement of whether congestion management released any capacity" | The vendor `defaultSentence` field |
| Related: nominations share the same filters | `endpoints.py:118-125` (every operational dataset except physical_flows gets `DEFAULT_POINT_DIRECTIONS`) |

## Body corrections (all ten notes, smallest spans, applied by `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\cap\fix_notes.py` with count-asserted replacements)

1. **Overview, generic paragraph:** "Records carry the daily `periodFrom` / `periodTo` window" becomes "a `periodFrom` / `periodTo` window (for capacity, the record's validity period, from one day to decades)".
2. **Overview, first line:** one member-specific sentence appended.
   - Firm available and booked: the technical-minus-booked identity, as a project check.
   - Firm technical: every valued record starts before the fetched day, so only placeholders survive.
   - Interruptible available and total: the GNI and BBL observations above.
   - Interruptible booked: mostly long-period records.
   - The four "available through": the vendor `defaultSentence`, quoted.
3. **Publication lag row:** "Same-day for `Provisional` flow status; revised within ~1 week" (copied from physical flows) becomes "Not vendor-documented here", with the validity-period note and `flowStatus` empty.
4. **Dedup key:** the 4-tuple becomes the vendor `id`, `keep="last"` (`generic.py:193-199`), with the 4-tuple's uniqueness (or, for "available through", its repetition) as an observation. Added a **Bronze read filter** line.
5. **Point-in-time field:** `last_update_date_time` becomes "none used by the pipeline", with what `last_update_date_time` and `ingested_at` are (`generic.py:181-183,201-206`).
6. **Silver schema table** regenerated from the members' parquet schemas, in silver's column order.
   - Fixed the broken `id | str | int` and `data_set | str | int` cells, which split the table.
   - Added the missing `timestamp_utc` row.
   - Corrected dtypes: `is_unlimited` str, `is_na` Int64, `is_cmp_relevant` str, `id_point_type` Int64, `is_archived` and `interruption_calculation_remark` Null.
   - Drift columns are noted as drift.
   - `firm_technical` no longer lists `point_type`/`id_point_type`/`is_archived`, which its silver lacks.
   - "Available through" now lists `dataset`, `is_default_sentence` and `default_sentence`, and drops the eight columns its silver lacks.
7. **Silver sample:** each note showed a bronze-shaped record with `+01:00`/`+02:00` stamps. Nine of the ten showed a record silver would drop (validity starting 2020 to 2025, such as National Gas TSO's 2022-2028 Bacton (IUK) exit record). Each is replaced with a real row from that member's silver, in UTC.
8. **Known issues:** added bullets on:
   - the silver drop, with code lines and per-member 2026-08/09 counts;
   - the placeholders (firm, interruptible) or the default-sentence rows, the repeated 4-tuple and the dropped 472 kWh/d records ("available through");
   - requested against returned;
   - partition dtype drift.
9. **Implementation delta:** "No documented discrepancies ... `meta.fields`" becomes a pointer to the silver retention issue. The indicator constant is cited at `endpoints.py:95-115`; `meta.fields` lists field names, not the indicator.
10. **Modelling notes:** "Filter on `flowStatus == 'Confirmed'`" becomes `flow_status` empty, then drop placeholders or sentence rows, and treat `value` as applying over `period_from` to `period_to`.

Bronze samples and curl examples are left unchanged; they are valid vendor examples. The broken link `20-domain/markets/gas-nominations.md` predates this work and is left alone.

## Not verified

- **ENTSOG's own definitions** of technical, booked, available, interruptible total and the four "available through" mechanisms. None is quoted in the vault. The page uses indicator names, the default sentence and one observed identity only.
- **Why one 472 kWh/d record appears under three mechanisms.** It is the same value and the same `lastUpdateDateTime` under oversubscription, surrender and UIOLI long-term at National Gas TSO Bacton (IUK) exit, next to a "no capacity made available" sentence for the same point and day.
- **Whether `dataSet` 5 (sentence rows) against 1 (valued) has a documented meaning.**
- **Whether a later fetch changes a stored capacity record.** No re-fetch exists to compare.
- **The unfolded frame** was not screenshotted. Same template as nominations, where the reviewer measured it.

## Open questions

1. Should capacity indicators join `_DATE_WINDOW_EXEMPT`, or should silver expand each validity record to the fetched gas day? Exempting keeps every record but stamps it with its validity start, which may predate the window. Restamping to the bronze day, with the record's period kept in `period_from`/`period_to`, would give one row per gas day per point. This decides what the chart and the key should be after the fix.
2. Should the "available through" default-sentence rows be filtered out of silver, or flagged and kept?
3. Should the family page hold until the fix, or ship as thin-but-honest? My recommendation is hold (see the top of this report).

## Template problems

1. **`gridflow-sample` cannot read silver whose partitions disagree on a column's dtype** (major for this page; it blocks the official sample). `sample.py:51-62` uses one `scan_parquet` with the newest file's schema. ENTSOG generic tables drift (Null against String) by day. Suggested fix: read per file and `pl.concat(..., how="diagonal_relaxed")`, keeping the newest file's column order (what `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\cap\sample_relaxed.py` does), or cast Null columns to the supertype. Likely to hit `gas-quality`, `cmp` and other generic ENTSOG families.
2. **Family charts read only the lead's table.** This family's most useful reading is technical against booked against available at one point. Technical is absent from silver, and booked lives in another table, so the notebook carries the firm sum. Not a defect.
3. **A long query parameter wraps mid-word after an empty line at 390** (`&indicator=Available+through+Surrender`). Cosmetic.
4. **The build warnings name the wrong module** ("gridflow.schemas.elexon" for ENTSOG), as reported by the nominations writer. There is also no dark theme to check.

## Defects

- **[gridflow silver, HIGH] Generic ENTSOG silver drops capacity records whose validity starts before the fetched gas day.**
  - `GenericEntsogJsonTransformer` sets `date_window_dataset = endpoint.requires_dates` (`silver/entsog/generic.py:332`) and filters each bronze file with `partition_records_to_target_date` (`:157-161`; `silver/entsog/datetime.py:56-87,191-213`). It keeps a record only if the local date of `periodFrom` equals the bronze day.
  - Capacity indicators return validity records (one day to 2015-2048), so most are discarded. 2026-08/09:
    - `firm_technical`: 126 bronze records, 98 valued, became 28 silver rows with 0 values.
    - `firm_available` and `firm_booked`: 84 valued became 17.
    - `interruptible_*`: 112 valued became 6 to 7.
    - The four `available_through_*`: 15 valued became 0 (silver keeps only default-sentence rows).
  - What survives depends on whether a record happens to start on a fetched day (Interconnector's 30-day and 7-day records).
  - The same class as VTA-ENTSOG-TARIFF-01, already exempted for `tariffs` and `tariff_simulations` (`generic.py:297-306`).
  - Candidate fix: add the ten capacity datasets to the exemption with a per-gas-day restamp, or expand each validity record to the fetched day.
  - Affects all ten members of `entsog/capacity-by-indicator`.
- **[gridflow silver] Generic ENTSOG partition dtypes depend on the day's response.**
  - A column that is all-null in one day's body is written as Null dtype in that partition and String in others: `capacity_booking_status` in `firm_available` and `firm_booked`, and six columns in each `interruptible_*` table.
  - `pl.read_parquet` over the table glob fails with "data type mismatch". `generic.py` coerces no dtypes. (Same family of issue as the allocations `is_cmp_relevant` String/Boolean split.)
- **[gridflow silver, observation] Not-applicable placeholders kept, stamped an hour earlier.**
  - National Gas TSO `ITP-00090` entry and `ITP-00207` exit, GNI `ITP-00495` exit (firm), and GNI `ITP-00495` entry (interruptible) send `isNA` 1, `value` `""` and `periodFrom` 05:00+02:00.
  - They land at 03:00 UTC against 04:00 UTC for valued rows, with a fixed-range `_NA<n>` id that recurs daily.
  - As sent; worth a filter or flag.
- **[gridflow silver] "Available through" default-sentence rows.**
  - They carry lowercase `dataset` "5", so silver has a `dataset` column and no `data_set`.
  - They have a zero-length period at 00:00+02:00, so `timestamp_utc` is 22:00 UTC the previous day and the 2026-08-03 partition holds rows dated 2 August.
  - National Gas TSO `ITP-00090` entry appears three times a day (one per adjacent operator in `id`), so the 4-tuple repeats.
  - They carry no value, and are the only rows silver keeps for these four indicators.
- **[vendor, open research] One 472 kWh/d annual record under three mechanisms.**
  - National Gas TSO Bacton (IUK) exit, 2025-10-01 to 2026-10-01, value 472 kWh/d, identical `lastUpdateDateTime`, sent under Available through Oversubscription, Surrender and UIOLI long-term.
  - On the same point and day ENTSOG also sends the "Currently no capacity has been made available" default sentence. Unexplained.
- **[front-end tool] `gridflow-sample` fails on partition dtype drift** (`src/gridflow_front_end/sample.py:51-62`). The committed `samples/entsog/firm_available.json` was produced by the same `main()` with a relaxed reader and must be regenerated once `_scan` is fixed.
- **[vault, fixed in this branch] All ten capacity notes were wrong in several places:**
  - dedup key (a 4-tuple, not `id`);
  - point-in-time field;
  - a physical-flows publication lag;
  - "daily" `periodFrom`/`periodTo`;
  - broken `id | str | int` and `data_set` schema cells, a missing `timestamp_utc`, about six wrong dtypes per note, and columns listed that silver lacks;
  - silver samples showing bronze `+02:00` stamps, nine of them records silver drops;
  - the `flowStatus == 'Confirmed'` modelling advice.

  All are corrected with code citations.
