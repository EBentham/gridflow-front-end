# entsog/reference-data: checker review

Checker: Sonnet 5.5 · high, 2026-10-07. Page family `reference-data` (lead `operators`; members `balancing_zones`,
`connection_points`, `interconnections`, `aggregate_interconnections`, `operator_point_directions`).

## Verdict: REVISE

0 blockers, 4 majors, 9 nits. The chart, request URLs, keys, the six mirrors and the vault schema tables are right. The
majors are about what the page leaves out or overstates for the members that are not the lead.

## What I checked and found sound

- **Integrity:** each of the six registers has one bronze file (27 Sep 2026, fetched 00:30 UTC), `meta.total` equals the
  bronze record count equals the silver row count (557, 48, 788, 194, 27, 1,225), and `id` is unique in every one.
  Silver reads the newest capture only (`generic.py` `NEWEST_VOUCHED`, `paths[:1]`).
- **Chart:** recomputed `operator_type_label` counts: TSO 154, SSO 108, H2FO 104, ESO 86, LSO 51, ETO 12, PSO 10, and
  the seven others 7+7+6+5+3+3+1 = 32. Matches `series/entsog/operators.json` (`spec_origin: vault`, rows_used 557) and
  the alt text. Build ran clean; `detect.mjs --json` returned `[]`; real em dashes 0.
- **Requests:** all six `raw_feed.requests` equal the bronze sidecar `request_url` verbatim.
- **Mirrors:** `cmp` on all six notes, vault worktree against `vault/entsog/`, is byte-equal.
- **Vault body edits:** I compared the silver-schema tables of all six notes with the parquet dtypes. Every type cell
  matches. The curl examples are untouched. The `hasData` correction matches ENTSOG's API manual v2.1 section 2.4.7 and
  the `/connectionPoints` correction matches section 2.2 (I read `entsog_api_manual.txt`).
- **Sample rows:** all eight operators match silver cell for cell. The differences are print formatting only (true and
  false for bool, whitespace trimmed by the markdown table, `|` masked). The generation route is not a finding.
- **Defects reproduced** (bronze and silver):
  - `timestamp_utc` is null on 1,225 of 1,225 `operator_point_directions` rows and 194 of 194 `interconnections` rows.
    `validFrom` is null on every record in both; `generic.py:51-59` picks `valid_from` first and `:185-187` copies it.
  - `silver/schema_manifest.py:210,217` names `timestamp_utc` as the date column of both, so `query()` filters on an
    all-null column.
  - Interconnections `lastUpdateDateTime` is `Sep 27 2026  2:18AM` with no offset; `datetime.py:43-44` labels it UTC,
    giving 02:18 UTC against a fetch at 00:30:35 UTC. Directions' stamp is `2026-09-27T02:09:37+02:00`.
  - Operators: 547 of 557 share `2026-09-27T00:13:00+02:00`. The ten others run from 2014 to 2025.
- **Seat notes:** the 1440 column-guide squeeze is real (meanings wrap in about 100 px at 1440); left for the seat. No
  horizontal overflow at 1440, 1024, 768 or 390 (numeric check of every element outside a scroll box). The unfolded frame
  scrolls inside its own box (49,694 px wide, 136 columns) and no cell clips its text.

## Findings

1. **major** `page.family.members[interconnections|operator_point_directions].differs`, `page.what_it_is`,
   `page.notebook.lead`. **The page never says that two members cannot be read with `query()`.**
   - `timestamp_utc` is null on every row of `operator_point_directions` and `interconnections`, and gridflow_models
     `query()` filters on it (`research/handles/source.py:401-440`; `schema_manifest.py:210,217`), so
     `data.entsog.query("operator_point_directions", ...)` and `query("interconnections", ...)` can never return a row.
   - The only treatment on the page is the notebook lead, which covers `operators` alone. The explanation is in the vault
     note body, which a site reader does not see.
   - The page also does not say that the other three members (`balancing_zones`, `connection_points`,
     `aggregate_interconnections`) are queried by `ingested_at`, which is the silver write time, not any vendor date
     (`schema_manifest.py:193,200,204`).
   - Evidence: `silver/entsog/{operator_point_directions,interconnections}` `timestamp_utc.null_count()` equals the row
     count; the page text never says that `timestamp_utc` is null, and mentions `query` and `ingested_at` only in the operators lead.
   - Fix: say it in the `differs` lines (14-word limit) and in `notebook.lead`, for example "`query()` returns no rows;
     read it with `data.sql()`", and one clause in the lead that the three registers without a vendor date use
     `ingested_at`.

2. **major** `page.record.fields.last_update_date_time`, `page.record.caption`, `page.family.members[interconnections]`.
   **Naive ENTSOG time stamps are labelled UTC, and the page says they were converted.**
   - The guide says "ENTSOG's update stamp converted to UTC". For the 2014 row (the headline row of the caption, the first
     row of the frame) it was not converted. Bronze holds `'Sep  1 2014 12:16AM'` for `TR-TSO-0003`, with no offset.
     `datetime.py:43-44` calls it UTC. If it is local time, as the interconnections stamp demonstrably is (a 02:18 stamp after a 00:30 UTC fetch;
     response `meta.timezone` says CET), the instant is 2014-08-31 22:16 UTC (inferred, CEST in September), a day
     earlier than the `2014-09-01 00:16:00 UTC` shown. The finding does not depend on that inference: the guide says
     "converted" and this row was only labelled. The other ten older stamps carry offsets and are correct.
     Command: count of distinct `lastUpdateDateTime` formats in the operators bronze gives 10 offset strings and this one.
   - Interconnections has the same defect on every row (stamp 2 h late) and the page does not mention it. A reader who
     takes `last_update_date_time` from that member gets a wrong instant.
   - The writer's Defects list and the report cover the interconnections case but not the operators row.
   - Fix: reword the guide line to say the stamp is converted only where ENTSOG sends an offset, and say in the caption or
     the interconnections `differs` line that its stamp is local time labelled UTC.

3. **major** `page.what_it_is` ("are what flow, capacity and tariff rows key on"), related note of `entsog/physical_flows`.
   **Unscoped universal that the writer's own join contradicts.**
   - Reproduced: 986 distinct (operator, point, direction) tuples in silver `physical_flows`; 39 are absent from
     `operator_point_directions` (546 of 13,764 rows). Examples: `BE-TSO-0001 ITP-00065`, `BG-TSO-0001 ITP-00292/00515`,
     `DE-TSO-0003 ITP-00518`.
   - The writer reported this as an open question but left the sentence unscoped. The cause is unknown, so the page cannot
     say flow rows always resolve.
   - Fix: "Flow, capacity and tariff rows carry the same operator, point and direction keys", with no claim that every
     triple is in this register.

4. **major** `page.record.fields` (129 lines) and `page.record.caption`. **The column guide mostly restates names and
   hides that its meanings are inferred.**
   - Count in the note: 34 lines "Free-text remark on X", 20 "Whether X applies or is offered", 6 "The operator's own wording
     for X", 17 "Operator profile: X". That is 77 of 129 lines (60 %) that restate the column name, which is the rubric's
     no-filler rule (section 6).
   - The page says ENTSOG defines none of the *dates* (`what_it_is`), and three lines say the manual does not define a
     field (`participates`, `last_update_date_time`, `include_umm_in_acer_rss_feed`). It never says that ENTSOG defines no
     response field, so a reader takes `b_m_*_is_applied`, `multi_annual_contracts_is_available`, `grid_*`, and the
     `tso_*_remarks` columns as vendor definitions. They are read from field names and a few values. I confirmed in the
     manual text that it lists parameters only, with no field definitions.
   - The build requires a line per column (`build.py:1110-1116`), so the length itself is forced by the template; the
     writer flagged this. The seat should decide between a group line in the content model and a narrower frame.
   - Fix within the content model: state once, where the reader sees the guide (`record.caption` or `what_it_is`), that
     ENTSOG defines none of these fields and the lines are read from names and values; keep each remark line to the
     distinguishing fact (for example, "Free-text remark on the maintenance link" can stay, but the 20 "Whether" lines can
     share one pattern and drop the repeated opening).

## Nits

5. **nit** `page.record.fields.operator_logo_url`: "URL of the operator's logo on ENTSOG's site". Of 188 non-empty values,
   5 are on the operators' own sites (`transportgas-srbija.rs`, `icgb.eu`, `moraviags.cz`, `prisma-capacity.eu`), and 369
   of 557 are the empty string. Say "usually on ENTSOG's site; blank for most operators".

6. **nit** `page.record.fields.operator_label`: "Short operator name, as sent". It is cut at 20 characters in the
   vendor response (65 rows are exactly 20 characters, for example `Power2MethanolAnvers`, `Aggregated Counterpa`). Say so
   in the guide, since people join on labels.

7. **nit** `page.record.fields.gas_day_start_hour`: "ENTSOG states no time zone". Three operators state one in
   `gas_day_start_hour_remarks` (`BG-TSO-0001` "EET", `PT-TSO-0001` "WET", `FI-TSO-0001` "Starts at 0 a.m. Finnish time").
   Reword: "no time zone field; a few operators name one in the remarks".

8. **nit** `page.record.fields.b_m_daily_imbalance_tolerance_is_information` (and the other `_is_information` lines): the
   column often carries the tolerance size itself ("1.5%", "24 MWh/d per Balance Group", "Range 3% - 20%"), not text
   "beside a flag". Say it holds the tolerance as the operator wrote it.

9. **nit** `page.chart_view.key[5].note`: "balance parties" should be "balance responsible parties" (the vendor's
    `operator_type_label_long` is "Balance Responsible Party").

10. **nit** Chart y-axis labels at 390 px: "Production operators" starts 2 px from the viewport edge and "Hydrogen operators"
    8 px, outside the 16 px gutter and the SVG box (`getBoundingClientRect`, label left 2 and 8 against SVG left 16).
    `.chart` is `overflow: visible` (`theme.css:573`) and the screenshot shows both labels whole, so nothing is clipped, but the labels spill into the gutter. Shorter labels ("Production", "Hydrogen") would fix it.

11. **nit** `page.family.members[interconnections].differs` and `page.how_used[2]`. "Links from a UK exit system to an
    entry system" is accurate to the request but incomplete: 27 of 194 rows have a storage, production or LNG from-side,
    16 have null `from_operator_key` and `from_direction_key`, 190 of 194 end in the UK, and only 4 cross the border
    (`ITP-00061` BE, `ITP-00090` IE, `ITP-00207` NL, `ITP-00222` IE). Imports into GB are not here (the request sends
    `fromCountryKey=UK`). "Finding the operator on the far side of a GB interconnection point" is served by
    `operator_point_directions.adjacent_operator_key`, present on all 1,225 rows, so the page should name that member.
    The writer's key table ("unique, no nulls") is wrong for interconnections (nulls in two key columns); it is not on
    the page.

12. **nit** `page.family.members[balancing_zones|connection_points].differs`. ENTSOG's response meta echoes
    `isDeactivated: '0'` (balancing zones) and `IsInvalid: False` (connection points), which gridflow does not send, so
    ENTSOG applies them by default and deactivated zones and invalid points are not in these registers. The page does not
    say so. This is the vendor's default shown in the response meta, not a documented rule, so word it that way.

13. **nit** `page.how_used[1]` ("Building the `pointDirection` keys gridflow sends for operational data requests"). True as a
    use of the register, but gridflow does not build the keys: `connectors/entsog/endpoints.py:24-34` and `:48-54` are
    hand-written tuples (`DEFAULT_POINT_DIRECTIONS`, `DEFAULT_AGGREGATED_POINT_DIRECTIONS`) and no code reads these
    silver tables. Say the request lists are written by hand from these values.

## Not findings

- `hasData=1` on `/operators` is stated as undocumented for that endpoint; the response still lists 557 operators across 14
  types, consistent with the caption.
- `facts.cadence` ("`sources.yaml` declares each weekly") matches `config/sources.yaml` (all six `schedule: "weekly"`).
- The notebook ran without errors, uses `data.sql()` on `silver_entsog_operators`, has no write calls, and its outputs
  (UK operators head, type counts 154, 108, 104, 86, 51, 12, 10, ...) match silver.
- Related notes are 12 words or fewer; no planning words, local-count phrases, em dashes or middle dots on the page.
