# entsog/reference-data: writer report

Family `reference-data`. The lead is `operators`; the other members are `balancing_zones`, `connection_points`,
`interconnections`, `aggregate_interconnections` and `operator_point_directions`. Writer: Opus 5.5 · high, 2026-10-07.

## Status

**Recommendation: ship. No hold.**

- **Silver integrity:** every member matches its bronze record count and the vendor's `meta.total`. Each register
  has one capture, with no repeats and no losses.
- **Date filter:** the date-window filter behind the two HELD reports does not touch these registers.
  - They are `requires_dates=False`, so `date_window_dataset=False` (`endpoints.py:207-258`; `generic.py:331-332`).
- **Build:** `gridflow-build --only entsog/operators` passes. It wrote `data-sources/entsog/reference-data.html` plus
  the six member pointers.
- **Detector:** `detect.mjs --json` returns `[]`. The page has 0 real em dashes.
- **Chart:** a bar chart of operators counted by `operator_type_label`, from the capture fetched 27 September 2026.
  There is no time axis.
- **Sample:** made with `gridflow-sample`'s own `main()` through the precedent `|` mask
  (`scratchpad\refdata\sample_pipe.py`, a copy of `scratchpad\apf\sample_pipe.py`).
  - Every operator row has `|` in `operator_tooltip`.
  - The sample must be regenerated once `sample.py` handles `|`.

## Files written

- **Canonical vault notes** (vault worktree):
  - `30-vendors/entsog/datasets/operators.md`: the `page:` block plus body corrections.
  - Body corrections only: `balancing_zones.md`, `connection_points.md`, `interconnections.md`,
    `aggregate_interconnections.md`, `operator_point_directions.md`.
- **Mirrors:** `vault/entsog/<same six>.md` in the front-end worktree.
  - Copied with `cp`; `cmp` shows all six byte-equal.
  - The mirrors were stale only in line endings before the copy.
- **Artefacts:**
  - `site/hifi/data/series/entsog/operators.json` (`gridflow-distil`, `spec_origin: vault`).
  - `site/hifi/data/samples/entsog/operators.json` (`generated_by: gridflow-sample`, 8 rows × 135 columns).
  - `site/hifi/data/notebooks/entsog/operators.json` (`scripts/run_notebooks.py`, 5 cells, no errors, no plot).
- **Built page:** `site/hifi/data-sources/entsog/reference-data.html`.
- **Retired:** nothing. No staged chart spec or authored override existed for any member.
- **Screenshots** (light only: the site has no dark theme; `--force-dark-mode` and `preferredColorScheme=0` render the
  same as light), all under `...\scratchpad\refdata\shots\`:
  - `w1440.png`, `w1024.png`, `w768.png`;
  - `w390.png`, a true 390 px iframe;
  - crops: `check_frame.png`, `w1440_chart.png`, `m768.png`, `m390_0.png` to `m390_6.png`.
- **Scratch scripts:** `...\scratchpad\refdata\` (`body_edits.py`, `insert_page.py`, `page.yaml`, `fix2.py`, `fix3.py`).
- **Server:** the static server on 9878 is stopped, and the 390 harness file I put in `site/hifi` is deleted.

## Integrity check (first, as asked)

| Member | Bronze files | Bronze records | `meta.total` | Unique `id` | Identical records | Silver rows |
|---|---|---|---|---|---|---|
| operators | 1 (27 Sep 00:30:59 UTC) | 557 | 557 | 557 | 0 | 557 |
| balancing_zones | 1 | 48 | 48 | 48 | 0 | 48 |
| connection_points | 1 | 788 | 788 | 788 | 0 | 788 |
| interconnections | 1 | 194 | 194 | 194 | 0 | 194 |
| aggregate_interconnections | 1 | 27 | 27 | 27 | 0 | 27 |
| operator_point_directions | 1 | 1,225 | 1,225 | 1,225 | 0 | 1,225 |

How silver handles these registers:

- It reads the newest bronze capture only: `BronzeReadSelection.NEWEST_VOUCHED` (`generic.py:106-116`), `paths[:1]`
  (`:128-129`) and the reverse-sorted rglob (`:252-259`).
- It overwrites one file, `silver/entsog/<ds>/<ds>.parquet` (`:284`; `silver/base.py:834`).
- So there are no per-day copies, unlike tariffs. The tariffs ruling (identical copies ship if stated) does not arise.

## Keys, grain and joins

### Key of each register

| Member | One row is | Key (unique, no nulls) | Vendor `id` | `dataSet` |
|---|---|---|---|---|
| operators | an operator | `operator_key` (557) | `1` + operatorKey | 1 |
| connection_points | a main map point | `point_key` (788) | `2` + pointKey | 2 |
| balancing_zones | a balancing zone | `bz_key` (48) | `3` + bzKey | 3 |
| interconnections | point × exit-side operator and direction × entry system | `(point_key, from_operator_key, from_direction_key, to_system_label)` (194) | `4Interconnections…` | 4 |
| operator_point_directions | operator × point × direction | `(operator_key, point_key, direction_key)` (1,225) | `5` + op + point + dir (+ adjacent op) | 5 |
| aggregate_interconnections | zone × operator × direction × adjacent system | `(bz_key, operator_key, direction_key, adjacent_systems_key)` (27) | `6` + country + bz + op + dir + adjacent | 6 |

### Join coverage (observation; distinct keys, 27 Sep 2026 capture)

Every operator key resolves in `operators` from each of these:

- `operator_point_directions`: 53/53.
- `balancing_zones.bz_manager_key`: 36/36.
- `aggregate_interconnections`: 4/4.
- Interconnections from-side 17/17 and to-side 19/19.
- Every data table: physical_flows 48/48, nominations 3/3, tariffs 37/37, cmp_* 47/30/50.

The data tables' `(operator, point, direction)` tuples, looked up in `operator_point_directions`:

- nominations, allocations and renominations 7/7, gcv 7/7, wobbe 9/9, firm_technical 2/2 resolve fully.
- So do tariffs 321/321 and cmp_auction_premiums 963/963, cmp_unavailable 572/572, cmp_unsuccessful 994/994.
- **physical_flows: 947/986.** The 39 tuples absent include `DE-TSO-0009` at several ITPs, `BE-TSO-0001 ITP-00065`
  and `BG-TSO-0001 ITP-00292/00515/PRD-00170`. This is an open question below.

Points and zones:

- **Directions to `connection_points`:** 653/717 direction points resolve.
  - The 64 missing are operator-specific sub points, for example `ITP-00006` Oberkappel (OGE) and `ITP-00495` Moffat
    (GNI side).
  - ENTSOG's API manual (v2.1, section 2.2) explains it: `/connectionPoints` returns the main points only, and
    `/operatorPointDirections` is the source for all points.
  - The other way round, 653/788 connection points appear in the directions register. The rest are mostly storage,
    LNG and non-EU points, consistent with the directions register being filtered to points with data.
- **Interconnections:**
  - from-side tuples resolve in directions 157/176; to-side 32/55. The gaps are LSO and SSO sides, such as
    `UK-SSO-0007 UGS-00421 entry`.
  - Points: `point_key` resolves in `connection_points` 174/174, from-side points 163/168, to-side points 41/47.
- **Aggregates:** `aggregated_physical_flows` aggregate keys resolve in `aggregate_interconnections` 3/3. The
  connector's `DEFAULT_AGGREGATED_POINT_DIRECTIONS` (`endpoints.py:48-54`) are these registers' ids without the
  `6UK` prefix.

## Dates in the registers (what they mean)

ENTSOG's API manual (v2.1, 11 Jul 2018) defines **none** of the registers' date fields. I read it in full: 11 pages,
PDF from the link in the notes, extracted to `scratchpad\entsog_api_manual.txt`.

**operators**

- `lastUpdateDateTime` is sent with an offset (`2026-09-27T00:13:00+02:00`) and converted correctly.
- 547 of 557 operators share one stamp, 2026-09-26 22:13 UTC. Ten carry older stamps, from 2014-09-01
  (`TR-TSO-0003` Leviathan TSO) to 2025-10-15.
- So it is not a per-operator edit date. DATA-MATRIX's "2014 to 2026" is this stamp's range, not register history.
- `timestamp_utc` is a copy of it (first match in `_TIMESTAMP_PRIORITY`, `generic.py:51-59,185-187`). The page says so
  and never presents it as history.

**operator_point_directions**

- `validFrom` and `validTo` are sent null on all 1,225 records (bronze checked).
- `lastUpdateDateTime` is one stamp on every record (`2026-09-27T02:09:37+02:00`).
- `tpTsoValidFrom` and `tpTsoValidTo` are text dates such as `2013-10-01` and `2099-12-31`. They stay String.
- `virtualizedCommerciallySince` and `virtualizedOperationallySince` are text dates, null on most rows.
- `timestamp_utc` copies `valid_from` (it outranks `last_update_date_time`), so it is **null on every row**.

**interconnections**

- `validFrom` and `validto` (the vendor's spelling) are null on all 194.
- `lastUpdateDateTime` arrives as `Sep 27 2026  2:18AM` with no offset. Silver labels it UTC (`datetime.py:43-44`),
  which gives 02:18 UTC, later than the bronze fetch at 00:30:35 UTC. So it is local time (CEST) stamped as UTC,
  2 h late.
- `timestamp_utc` is null on every row.

**balancing_zones**

- `replacedSince` is a text date with offset (for example `2021-10-01T00:00:00+02:00` for GASPOOL and NCG replaced by
  `DE-THE`). It is not in `_DATETIME_COLUMNS`, so it stays String.
- Replaced zones still carry `is_deactivated` `0`.

**connection_points, aggregate_interconnections:** no date fields.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Six referential registers, each fetched whole in one call with no dates (`what_it_is`, `raw_feed.note`) | `endpoints.py:207-258` (`reference=True`, no `requires_dates`); `client.py:75-76` single request; `build_params` adds no `from`/`to` (`:271-281`); sidecars show one request each, `page: 1, total_pages: 1` |
| Request URLs (`raw_feed.requests`, `family.members[].request`) | Sidecar `request_url` of each bronze file, verbatim (for example `operators?limit=-1&timeZone=UCT&hasData=1`); `default_params` at `endpoints.py:221,238,247,256` |
| Bronze filed under the UTC fetch day | `data_date=None` for reference (`client.py:76`); `bronze/writer.py:39` falls back to `fetched_at.date()`; `fetched_at` is `datetime.now(UTC)` (`connectors/base.py:40`); bronze folder `2026/09/27`, `fetched_at` 2026-09-27T00:30Z |
| `transform` rewrites one silver file from the newest capture | `generic.py:106-116,128-129,252-259,284`; `pipeline/runner.py:1138,1153-1158` (each target date rescans the tree) |
| Commands: `ingest` with no dates; `transform --start/--end` one day | `cli.py:186-258` (dates optional; the connector ignores them for reference endpoints); `runner.py:1138` inclusive date range |
| Operators lists storage, LNG, hydrogen and electricity operators as well as gas TSOs (`what_it_is`, chart) | `operator_type_label` counts: TSO 154, SSO 108, H2FO 104, ESO 86, LSO 51, ETO 12, PSO 10, DSO 7, ENA 7, UTI 6, BRP 5, NWO 3, ASO 3, USO 1; long labels from `operator_type_label_long` |
| ENTSOG documents `hasData` for point directions only (caption, family differs) | API manual v2.1, section 2.4.7 ("Get only the TSO points"): keeps the directions of TSOs that publish REG715 data; the section on `/operators` does not mention it |
| Directions are what flow, capacity and tariff rows key on (`what_it_is`, related) | Join coverage above; the connector's `pointDirection` is `operatorKey+pointKey+directionKey` (`endpoints.py:22-34`); manual section 2.4.7 says `pointDirection` values come from the directions API |
| Connection points are main points only; ENTSOG leaves sub points out (family differs) | API manual v2.1, section 2.2, `/connectionPoints` row |
| Interconnections: exit system to entry system, `fromCountryKey=UK` sent | Manual section 2.2 `/interconnections` row; `endpoints.py:247`; all 194 rows `from_country_key = UK`; entry-side infrastructure includes Distribution 128, Storage 20, Final Consumers 2 |
| Aggregate interconnections: UK zones, operator, direction, adjacent system, `countryKey=UK` | Manual section 2.2 row; `endpoints.py:256`; 27 rows over `bz_key` `UK---------`, `UK-IUK-----`, `UK-NI------` |
| Balancing zones: one per `bz_key`, manager and successor | 48 unique `bz_key`; `bz_manager_key`, `replaced_by`, `replaced_since` columns |
| Silver keeps the newest capture only | `generic.py:128-129`; one bronze file per register |
| ENTSOG's API manual defines none of the registers' dates | Full read of the manual text (`scratchpad\entsog_api_manual.txt`); no field definitions at all, only parameters |
| Chart counts: 154, 108, 104, 86, 51, 32, 12, 10 (alt) | Committed series `series/entsog/operators.json` `values` |
| Gas TSOs key note: includes BBL company and PTL | Sample rows `UK-TSO-0004` "BBL" (`operator_country_key` NL, type TSO) and `UK-TSO-0002` "PTL" (TSO) |
| Seven other types: DSO, ENA, UTI, BRP, NWO, ASO, USO, with plain names | `operator_type_label_long`: Distribution System Operator, Energy Association, Utility Company, Balance Responsible Party, News organization, Artificial Operator, Upstream System Operator |
| `operator_key` prefix can differ from country (guide) | Sample `UK-TSO-0004` → `NL`; the notebook output shows `IE-TSO-0001` → `UK` |
| `operator_country_key`: ENTSOG's `UK`, not ISO `GB`; `--` for none | Values `UK` (34 rows); `---ASO-0001` has `--`; EIC codes say `GB` (`21X-GB-A-A0A0A-7`) |
| `tso_eic_code`: sent with the operator profile, null without one | The 57 operators with `gas_day_start_hour` are the 57 with `tso_eic_code`; sample rows match |
| `operator_tooltip`: long name and EIC joined by `|`; EIC can be blank | Sample `National Gas Transmission|21X-GB-A-A0A0A-7`, `ITM Power (Trading) Ltd|`, and Centrica's tooltip carries `23X--140117CSL-X` while `tso_eic_code` is null |
| `gas_day_start_hour`: as sent, no time zone stated | National Gas TSO and PTL `5`, Interconnector and BBL `6`; the manual says nothing; values are Int64 by Polars inference |
| `last_update_date_time` / `timestamp_utc` (guide, caption "2014 update stamp") | Bronze `2026-09-27T00:13:00+02:00` becomes 2026-09-26 22:13 UTC; sample `TR-TSO-0003` 2014-09-01 00:16 UTC; `generic.py:185-187` |
| `id` = register digit then operator key; silver keeps the last per `id` | `id` `1UK-TSO-0001`; `generic.py:193-199` (`unique(subset=["id"], keep="last")`) |
| Null-typed columns (`operator_country_flag`, `tso_display_name`, `tso_short_name`, `tso_long_name`) | Silver dtype `Null`; bronze null on all 557 |
| Legal-reference remark columns | Single value on all rows, for example `Regulation (EU) 2017/460, Article 29&30 Information` |
| Notebook lead: `query()` filters on `timestamp_utc`, a copy of the update stamp; `data.sql()` used | gridflow `silver/schema_manifest.py` `("entsog","operators"): "timestamp_utc"`; gridflow_models `source.py:401-448`; the notebook ran with no errors |
| Related: nominations requested by operator, point and direction keys | `endpoints.py:24-34,122` (`DEFAULT_POINT_DIRECTIONS` for every operational dataset except physical_flows) |
| Related: aggregated_physical_flows requested by keys from aggregate_interconnections | `endpoints.py:48-54,177` against `aggregate_interconnections.id` values |
| Related: tariffs per operator and point; operator profiles carry tariff units | tariffs keys resolve in directions 321/321; operators `firm_capacity_tariff_unit` and similar |

## Body corrections (all six notes, CRLF kept, each tagged "CORRECTED 2026-10-07")

Late fixes after the advisor review (rebuilt; detector `[]`; mirrors `cmp` clean):

- the operators `differs` line is scoped to "returned with `hasData=1`";
- the record caption says "seven UK-linked" (PTL is Northern Ireland, so not "GB");
- the `operator_label` and `operator_logo_url` tails, which counted things not visible in the eight rows, are dropped;
- the interconnections dedup line names its `id` form (`4Interconnections` + point, systems, operator, direction).

1. **Silver path** (all six):
   - Was: `{data_root}/silver/entsog/<ds>.parquet`.
   - Now: `{data_root}/silver/entsog/<ds>/<ds>.parquet`.
   - Evidence: `silver/base.py:834`, `generic.py:284`; on disk.
2. **Dedup key** (all six):
   - Was: "`(id)` if present, else inventory key (e.g. `point_key`, `operator_key`)".
   - Now: vendor `id`, keep last; without `id` the subset would be every column but `timestamp_utc`. Silver reads only
     the newest capture.
   - Evidence: `generic.py:193-199,112-116,128-129,252-259`.
3. **`hasData=1` gotcha** (all six):
   - Was: "filters out points/operators without any operational data… loses validity-period rows…".
   - Now: the manual (section 2.4.7) documents it for directions only (TSOs publishing REG715 data). It is undocumented
     for `/operators`, whose response still lists storage, LNG, hydrogen and electricity operators. The dormant-rows
     claim is marked unverified.
4. **Point-in-time field:**
   - `operators`: `timestamp_utc` is a copy of `last_update_date_time`, which is undefined by ENTSOG and shared by 547
     of 557 rows, and is not history.
   - `operator_point_directions`: `timestamp_utc` copies `valid_from`, which is null throughout, so `query()` returns
     no rows. Also the update stamp and the `tp_tso_*` text dates.
   - `interconnections`: the same null `timestamp_utc`, plus the naive `lastUpdateDateTime` stamped as UTC, 2 h late.
5. **Overview:**
   - `connection_points`: main points only, per the manual. `interconnections`: exit system to entry system, not
     "bidirectional between two transmission systems". Entry sides include distribution and storage;
     `fromCountryKey=UK` is sent.
6. **Query parameter table rows for `hasData`** (`operators`, `operator_point_directions`): reworded to the manual.
7. **Silver schema tables** (mechanical, from the silver parquet schema):
   - Type cells corrected where silver differs:
     - booleans listed as `str`;
     - `gas_day_start_hour` and `id_point_type` `int`;
     - `grid_conversion_factor_capacity_default` and `grid_gross_calorific_value_default_value_to` `float`;
     - `tp_tso_conversion_factor` `str` (was float);
     - `is_single_operator` `str` (was bool);
     - all-null fields `null (sent null)`.
   - Added a `timestamp_utc` row (operators, directions, interconnections) and one lineage row (`event_time`,
     `available_at`, `source_run_id`, `dataset_version`).
   - Counts: operators 28 cells, connection_points 3, interconnections 9, aggregate_interconnections 1,
     operator_point_directions 10, balancing_zones 0.

Not changed:

- Curl examples, bronze samples, silver samples and the Implementation delta.
- The "Publication lag: vendor inventory updates daily" rows (unverified, not mine to rewrite).

## Could not verify

- What `hasData=1` does on `/operators`. The manual documents it only for directions, and I cannot call the live API.
  The page says only that it is sent and documented for directions.
- What `participates`, `membership_label` `EUC`, and `include_umm_in_acer_rss_feed` mean. ENTSOG's manual defines no
  response fields; the guide says "as sent" or "not defined".
- The time zone of `gas_day_start_hour`. National Gas TSO `5` and Interconnector/BBL `6` fit local gas days (05:00 UK,
  06:00 CET), but nothing states it, and the page does not claim it.
- Whether the shared `lastUpdateDateTime` is a platform-wide refresh time. Likely, but undocumented; the page says only
  "often one shared stamp".

## Open questions

1. **Physical flows absent from the directions register:** 39 of 986 physical_flows (operator, point, direction)
   tuples are not in the `hasData=1` directions register.
   - Two possible causes: directions that left the register between the flow window (31 Jul to 21 Sep) and the 27 Sep
     capture, or flows reported under directions `hasData=1` filters out.
   - A capture without `hasData` would tell. I did not run one: no live API.
2. **`connection_points` scope:** should it be described to readers as "main points" only (as I did, from the
   manual), given that every operational table keys on directions-register points?
3. **Interconnection stamp:** is the interconnections `last_update_date_time` worth fixing in gridflow, given it is a
   register stamp? It is wrong by 2 h and labelled UTC. See Defects.

## Template problems (seat's files; not worked around except as noted)

1. **The 1440 column guide squeezes meanings into about 150 px.**
   - Cause: `site/hifi/assets/dataset.css:42`, `.guide dl { grid-template-columns: max-content minmax(0, 1fr) }`.
   - In the two-group layout at 1440 (`:39`, `fit-content(620px) minmax(0, 1fr)`), the "Other columns" `dt` track
     sizes to the longest silver name. `b_m_additional_cumulated_imbalance_tolerance_is_information` is 61 characters,
     about 490 px of mono.
   - The meanings wrap 4 to 7 lines each. Code tokens longer than about 18 characters overflowed the column into the
     gutter.
   - Workaround (content only): I reworded 12 meanings to keep long identifiers out (for example "the update stamp"
     rather than `last_update_date_time`). Nothing now overflows or clips. 1024, 768 and 390 lay out fine.
   - Suggested fix: cap the `dt` track (`minmax(0, 30ch)` with `overflow-wrap: anywhere`, as the 390 rule already
     does), or drop to one group above a column-name length.
2. **At 390, long column names wrap mid-identifier.** For example `b_m_hourly_imbalance_tolerance_is_informatio` / `n`.
   It is legible; this is the same as the tariffs report.
3. **`gridflow-sample` cannot print values containing `|` or newlines.**
   - `sample.py:67-87` splits Polars' markdown table on `|`; multi-line strings also split a row over several lines.
   - All 557 operator rows have `|` (`operator_tooltip`, `b_m_penalties`), and 16 have newlines in remark columns.
   - I used the precedent `|` mask and chose eight newline-free rows. `IE-TSO-0001` was dropped for a newline in
     `daily_contracts_remarks`.
   - Regenerate the sample once `polars_text` is fixed.
4. **Wide registers force very long guides.** Operators has 135 columns, so 129 guide lines are required
   (`build.py:1110-1116`). Most are vendor free-text remarks. A "remarks columns, as sent" group line would read
   better, but the content model has none.
5. **No dark theme exists.** "Light and dark" cannot be checked (as other writers reported).

## Defects (pasteable)

- **[gridflow silver] ENTSOG reference `timestamp_utc` null on every row for `operator_point_directions` and
  `interconnections`; `query()` returns nothing.**
  - Cause: `_TIMESTAMP_PRIORITY` (`silver/entsog/generic.py:51-59`) picks `valid_from` before `last_update_date_time`.
    ENTSOG sends `validFrom` null on all 1,225 direction records and all 194 interconnection records (27 Sep 2026
    bronze), so `timestamp_utc` (`:185-187`) is null throughout.
  - Effect: `silver/schema_manifest.py` declares `timestamp_utc` as both tables' date column, so gridflow_models
    `data.entsog.query("operator_point_directions"| "interconnections", …)` can never return a row.
  - Fix: skip all-null candidates, or give reference registers `ingested_at` like the other four.
- **[gridflow silver] Naive ENTSOG timestamps stamped as UTC: interconnections `last_update_date_time` 2 h late.**
  - `/interconnections` sends `lastUpdateDateTime` as `Sep 27 2026  2:18AM` with no offset.
  - `silver/entsog/datetime.py:43-44` (`parsed.replace(tzinfo=UTC)`) labels it UTC, giving 02:18 UTC. The bronze fetch
    was 00:30:35 UTC, and the same night's direction stamps are `+02:00`, so the value is CEST local time.
  - The fallback formats (`:17-23`) need ENTSOG's zone (the response `meta.timezone` says `CET`).
- **[gridflow silver, minor] `interconnections.validto`.** The vendor spelling is `validto`, which is not in
  `_DATETIME_COLUMNS` (`generic.py:34-50`). It would stay text if ever populated (null today).
- **[gridflow silver, minor] Date-shaped text left as String:**
  - `balancing_zones.replaced_since` (offset datetimes);
  - `operator_point_directions.tp_tso_valid_from`/`tp_tso_valid_to` (dates, with `2099-12-31` and `9999-12-31`
    sentinels);
  - `virtualized_commercially_since` and `virtualized_operationally_since`.
  - None is in `_DATETIME_COLUMNS`.
- **[front-end tool] `gridflow-sample` fails on `|` or newlines in any value.**
  - `src/gridflow_front_end/sample.py:67-87`. `entsog/operators` has `|` on every row (`operator_tooltip`) and
    newlines in 16 rows.
  - The committed `samples/entsog/operators.json` was made by the tool's own `main()` with `|` masked
    (`scratchpad\refdata\sample_pipe.py`). Regenerate once fixed.
- **[front-end template] Column guide `dt` track sizes to the longest name.** `site/hifi/assets/dataset.css:42`
  (`max-content`). At 1440 a 61-character silver column name leaves about 150 px for meanings on
  `entsog/reference-data`; long code tokens overflow.
- **[DATA-MATRIX] `entsog/operators` "2014-09-01 to 2026-09-26" is not coverage.** It is the range of ENTSOG's
  `lastUpdateDateTime`, and 547 of 557 rows share 2026-09-26 22:13 UTC. Relabel or drop the first and last dates for
  reference registers.
- **[vault, fixed in this branch] Six reference notes:**
  - wrong silver path (missing the dataset folder), wrong dedup wording;
  - `hasData` gotcha contradicted by ENTSOG's manual;
  - "per-row update timestamps" for directions and interconnections (actually one shared stamp, and `timestamp_utc`
    null);
  - schema tables missing `timestamp_utc` and the lineage columns, with booleans and ints listed as `str`.
- **[observation, open] 39 of 986 physical_flows (operator, point, direction) tuples are absent from the `hasData=1`
  directions register** (27 Sep capture). Examples: `DE-TSO-0009` at `ITP-00006`, `-00498`, `-00513`;
  `BE-TSO-0001 ITP-00065`. Cause unknown (see Open questions 1).

## What the checker should look hardest at

1. **The 129-line column guide:**
   - Each meaning is from vendor field names and values "as sent", because ENTSOG defines no response fields.
   - Check that none overclaims, especially `participates`, `membership_label`, `gas_day_start_hour`,
     `include_umm_in_acer_rss_feed`, and the `*_is_information` lines.
2. **The family `differs` lines:** `interconnections` and `aggregate_interconnections` are UK-filtered requests, not
   European registers. `connection_points` is main points only.
3. **The caption's `hasData` sentence and the 1440 guide layout** (template problem 1).
