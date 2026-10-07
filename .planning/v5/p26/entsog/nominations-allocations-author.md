# entsog/nominations-allocations: author report

Writer: Opus 5.5 · high, 2026-10-06. Family `nominations-allocations`, lead `nominations`, members `renominations`,
`allocations`. Built with `--only entsog/nominations`.

## Status

- `gridflow-build --only entsog/nominations`: passes. The only warnings are the build's generic "no Pydantic class
  declared" notices that every generic ENTSOG table gets.
- `detect.mjs --json` on `nominations-allocations.html`: `[]`. Em dashes in the page: 0. The rubric greps (locally,
  held, our, since 20, % of, live, now, yet, soon, digits plus rows or days) find nothing.
- Mirrors: all three notes copied with `cp` and checked with `cmp` (byte-equal, CRLF kept, diffs are line-level).
- Artefacts: `site/hifi/data/series/entsog/nominations.json` (`spec_origin: vault`),
  `samples/entsog/nominations.json`, `notebooks/entsog/nominations.json` plus `nominations-5.png`. There was no
  staged chart spec and no authored override to retire.
- Screenshots (light) at 1440, 1024, 768 and 390: `scratchpad\nomalloc_shots\s_<width>_light_<n>.png`.
  - **One clip, at 390 only:** the chart's y-axis tick labels (`150,000,000`, `100,000,000`, `50,000,000`) lose
    their leading digits off the left edge. 1440, 1024 and 768 show them in full. This is a template problem (see
    below); my files cannot fix it honestly.
  - Everything else is fully visible at every width: the hero and its scenery, the chart key, the three wrapped
    request URLs, the commands, the folded frame and its guide, the notebook and related.
- **Dark mode:** the site has no dark theme. No stylesheet or script carries `prefers-color-scheme` or
  `data-theme`, and `--force-dark-mode` renders the same as light. So light is the only check.
- Static server: port 9872, started with `timeout 1200`, so it stops itself. The owner's server on port 9670 was not
  touched.

**Recommendation:** ship once the 390 tick clip is fixed in the renderer; until then, a hold on that one major.
The content and the data are sound.

## What the data is (answers to "look hardest at")

- **Why only 98 rows.**
  - Bronze holds 14 gas days per member: 1 to 5 August and 13 to 21 September 2026. Silver has exactly those 14
    days. The gap is ingest coverage, not silver loss.
  - The connector sends nine `pointDirection` filters (`connectors/entsog/endpoints.py:24-34`). Every response
    returns 7 rows. The two BBL company filters (`UK-TSO-0004ITP-00063entry`/`exit`, Julianadorp/Balgzand) never
    return anything.
  - So 14 × 7 = 98 per member.
- **What one row is.** One vendor record per gas day, operator, point and direction.
  - Silver dedups on the vendor `id`, `keep="last"`, per daily bronze read (`silver/entsog/generic.py:193-199`).
  - The `id` concatenates indicator, period, keys and unit. So `(timestamp_utc, operator_key, point_key,
    direction_key)` is unique: 98 rows, and 98 distinct `id` values in nominations and renominations.
  - No duplicates.
- **Allocations quirk.** `id` has only 59 distinct values over 98 rows. National Gas TSO's three rows are vendor
  not-applicable placeholders:
  - an `id` with no date that recurs every day;
  - `value` sent as `""`, which becomes null;
  - `isNA` 1;
  - `periodFrom` 05:00+02:00, so 03:00 UTC;
  - `lastUpdateDateTime` 2025-02-20.

  Dedup runs per day, so each day keeps one. Nothing is lost or repeated, but the allocations table has two
  `timestamp_utc` values per day.
- **Units.**
  - `unit` is `kWh/d` on every row of all three members.
  - The generic transformer does not convert `value` (unlike `physical_flows`, which converts to GWh/d). `value`
    is cast to Float64 with `strict=False` (`generic.py:189-191`).
- **Time stamps.**
  - `timestamp_utc` is a copy of `period_from` (`generic.py:185-187`). For every valued row that is `periodFrom`
    06:00+02:00 as sent, which is 04:00 UTC. That matches the vault's gas-day concept note (06:00 CET/CEST, 04:00
    UTC in summer).
  - `period_to` is the next day's 04:00 UTC.
  - `last_update_date_time` is the vendor's `lastUpdateDateTime`, parsed to UTC. It is a vendor stamp, not an issue
    or fetch time, and the pipeline does not use it for vintage.
  - `ingested_at` is the silver transform time (`generic.py:201-206`).
  - Pandas in the notebook shows the same instants in UK time (05:00+01:00).
- **`lastUpdateDateTime` against gas-day start** (scoped to 2026-08/09 bronze; placeholders excluded):

  | Member | Interconnector | National Gas TSO | GNI |
  |---|---|---|---|
  | Nominations | +9 h to +34 h | +12 h to +21 h | −14 h to +5 h |
  | Renominations | +26 h to +52 h | +84 h to +85 h | +35 h to +45 h |
  | Allocations | +28.5 h to +52 h | (placeholders only) | +36 h to +170 h |

  So "day-ahead" (the old vault wording) is not what the stored nomination is. GNI's remark calls it the "Latest
  Aggregate Transporter Nomination available at the time of publishing".
- **Can the members be compared?** Yes: same seven keys, same 14 gas days, same 04:00 UTC start. The allocation
  placeholders are the exception. Observations, scoped to these 14 days:
  - Renomination equals allocation exactly for Interconnector (both sides) and for GNI's Moffat entry.
  - Nomination is much lower than renomination on most days. Moffat (IE) entry on 13 September: 81.3 against
    180.1 GWh/d.
  - The two operators' nominations for the same IUK flow differ. On 21 September National Gas TSO's exit is
    91,153,956 kWh/d and Interconnector's entry is 112,753,956 (shown in the eight rows). From 15 to 19 September
    National Gas TSO sends 0 or null while Interconnector sends 10,224,000. Their renominations agree.
- **Against `physical_flows`.** Renomination is within 0.4 GWh/d of physical flow at Moffat (IE) entry and Bacton
  (BBL) exit, 13 to 21 September (largest gap 0.33 GWh/d, Moffat, 14 September). Bacton (IUK) on 21 September is the exception: renomination 185.9 against
  physical flow 175.2 GWh/d, from National Gas TSO's exit report. Interconnector's reverse exit on the 21st is
  renominated and allocated at 10.87 GWh/d, but its physical flow is 0.
- **Moffat.**
  - The connector asks National Gas TSO only for `ITP-00090` **entry**, a virtual reverse point. Its allocation
    remark reads "Virtual Point, currently Moffat is only Unidirectional exit".
  - National Gas TSO's real Moffat exit (present in `physical_flows`) is never requested for these indicators.
    Its nomination at `ITP-00090` entry is null on every row.
  - The Moffat flow shows here only as GNI's `ITP-00495` entry.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Nine filters per request; request URL as built (`raw_feed.requests`, `family.members[].request`) | `endpoints.py:24-34,71-92,263-287`; `request_url` in bronze `.meta.json` for 2026-09-21, copied verbatim |
| One request per gas day and indicator | `client.py:78-102` (`day_subwindows`, one `from=to=D` call per covered day) |
| Ingest `--end 2026-09-22` exclusive, transform `--end 2026-09-21` inclusive | Same connector path as `physical_flows` (the half-open `day_subwindows`); same lines as the live physical_flows page |
| Silver keeps `value` and `unit` unconverted (`raw_feed.note`, `what_it_is`, fields) | `generic.py:175-236`: no unit logic; `unit` is `kWh/d` on all 294 rows |
| Grain and key (`facts.grain`, `record.key`) | Dedup on `id` (`generic.py:193-199`); 98 unique 4-tuples per member |
| `timestamp_utc` is the gas-day start from `periodFrom` in UTC | `generic.py:181-187`, `datetime.py:26-45`; bronze `periodFrom` `2026-09-21T06:00:00+02:00`, silver 04:00 UTC |
| x_label "gas day, starting 04:00 UTC" | Every charted row starts 04:00 UTC |
| `last_update_date_time` is the vendor's `lastUpdateDateTime` in UTC | `generic.py:34-50,181-183`; not referenced in `silver/base.py` |
| GNI's remark "latest aggregate nomination or renomination available when published" (`what_it_is`, `differs`) | Silver `item_remarks` on IE-TSO-0002 rows only; other operators send null |
| "BBL company is asked for Julianadorp, not Bacton, and returns no rows here" (key note) | Filter `UK-TSO-0004ITP-00063…`; the physical_flows register labels `ITP-00063` "Julianadorp (GTS) /Balgzand (BBL)"; 0 rows in all 42 bronze bodies |
| "gridflow asks National Gas TSO only for Moffat entry, null here" (key note) | `endpoints.py:33`; nominations `UK-TSO-0001`/`ITP-00090` entry: 14 of 14 null |
| National Gas TSO sends only not-applicable allocation rows (`family.members[2].differs`) | Allocations: all 42 `UK-TSO-0001` rows have `is_na` 1, null `value` and item remarks as quoted |
| Allocations carry a flow status | Allocations `flow_status`: `Provisional`/`Confirmed` (Interconnector, GNI); nominations and renominations `""` |
| Chart values, alt, key-note numbers | Committed series: moffat_ie 45,664,771 (19th) to 95,147,913 (15th), 90,763,437 on the 21st; bacton_bbl 100,104,000 (14th), 12,000,000 (19th), 77,088,000 (21st); bacton_iuk 0, null on the 17th, 91,153,956 on the 21st |
| "Interconnector's own entry report for the 21st is 112,753,956" (key note) | Eight rows, row 6 (`1.12753956e8`) |
| Notebook plot_alt numbers | Notebook output table: renominated = allocated, 180,146,144 (13th), 131,501,901 (19th), 180,105,551 (21st); nominated 45,664,771 to 95,147,913 |
| `notebook.lead` (relation, date column, ends included, lineage dropped) | gridflow `silver/schema_manifest.py:195,216,221` (`timestamp_utc`); `gridflow_models/research/handles/source.py:401-451` |
| Related: `firm_booked` uses the same nine filters | `endpoints.py:118-125` (every operational dataset except physical_flows) |

## Body corrections (all three notes, smallest spans)

1. **Overview line.**
   - "Day-ahead notifications of intended capacity use", "Updated nominations submitted intra-day…" and "Final
     capacity quantities confirmed…" are replaced with what the rows are: gas quantities in kWh/d, not capacity.
   - The new lines carry GNI's remark wording and the scoped `lastUpdateDateTime` ranges above.
   - The allocations line adds its flow status and points to the placeholders.
2. **Publication lag row.** "Same-day for `Provisional` flow status; revised within ~1 week" was copied from
   physical flows. It is replaced, per member, with "not vendor-documented here" plus the scoped bronze lags and the
   `flowStatus` facts.
3. **Dedup key.** It was the 4-tuple; it is now the vendor `id`, `keep="last"` (`generic.py:193-199`), with the
   4-tuple's uniqueness stated as an observation.
4. **Point-in-time field.** It was `last_update_date_time`. It is now "none used by the pipeline", with what
   `last_update_date_time` and `ingested_at` are (`generic.py:181-183,201-206`).
5. **Silver schema table.**
   - Added the missing `timestamp_utc` row.
   - Fixed the broken `id | str | int` cell, which split the table, and `data_set` (Int64).
   - Notes on `value` (not converted, `""` becomes null) and `unit`.
   - Allocations: added the missing `point_type`, `id_point_type` and `is_archived`, which silver carries.
6. **Silver sample.** `period_from`, `period_to` and `last_update_date_time` were shown with `+02:00`; silver
   holds UTC, so they are converted. In allocations, `"value": ""` becomes `null`.
7. **Known issues.** Added:
   - requested against returned (nine filters, seven rows, the BBL filters, `meta.count` against `meta.total`);
   - the Moffat virtual-reverse request;
   - for allocations, the placeholder rows and the `is_cmp_relevant` String dtype.
8. **Modelling notes.** "Filter on `flowStatus == 'Confirmed'`" is replaced:
   - nominations and renominations: `flow_status` is always `""`;
   - allocations: drop `is_na == 1` first.

The curl examples are left unchanged; they are valid for the vendor.

## Not verified

- **What ENTSOG's `meta.total` counts.** It is 14 (allocations: 8) against `count` 7 under `limit=-1`, in all 42
  bodies. This is the same open question as the physical_flows pilot (`P25B-REPORT-notes.md:112-114`). The page
  names the requested filters and never claims "all points".
- **The domain meaning of nomination, renomination and allocation** (EU network-code definitions). The page avoids
  definitions beyond GNI's row remark and the rows' own fields.
- **`dataSet` and `isCamRelevant`/`isCmpRelevant` semantics.** The guide says "as sent". The CAM/CMP expansions are
  the standard ENTSOG acronyms, not quoted from a vendor doc in the note.
- **Whether a later fetch changes a stored nomination.** `lastUpdateDateTime` suggests operators keep updating, but
  no re-fetch exists to compare against.

## Open questions

1. Should the connector request `UK-TSO-0001ITP-00090exit` (National Gas TSO's real Moffat direction) instead of,
   or as well as, `entry`?
2. Should it request BBL company at `ITP-00207` Bacton (BBL) rather than `ITP-00063` Julianadorp, which returns
   nothing for these indicators?
3. Should the chart axis for kWh/d datasets be scaled? See template problem 1.

## Template problems

1. **Tick labels clip at 390** (major under rubric §5).
   - Cause: `chart_svg.fmt_num` prints full integers (`150,000,000`), and the narrow frame's left margin (`fr.x0`)
     is too small for 11-character labels.
   - The chart spec has no scale or unit-conversion key, so a kWh/d series cannot be shown in GWh/d without
     misstating the unit.
   - Possible fixes (seat's call): compact tick labels (`150M`); a left margin sized from the widest label; or a
     `scale` key in `chart_spec` that divides the value and declares the derived unit.
   - Likely to hit other ENTSOG generic pages too (capacity, tariffs), all in raw kWh/d.
2. **A zero series sits on the x axis.** National Gas TSO's IUK zeros overlap the axis line, so the 17 September
   null shows only as a missing dot. The key note states it. A renderer that offsets or draws a zero line on top
   would help. Minor.
3. **Family charts read one silver table.** This family's most useful reading is nomination against renomination
   against allocation at one point. That cannot be charted, so the notebook carries it. Not a defect; a limit
   worth knowing.
4. **Build warnings name the wrong module.** They say "no Pydantic class declared in gridflow.schemas.elexon" for
   ENTSOG datasets, which is cosmetic.
5. **There is no dark theme.** The anatomy rule "light and dark" cannot be checked.

## Defects

- **[gridflow connector] Moffat requested in the wrong direction for National Gas TSO.**
  - `connectors/entsog/endpoints.py:33` requests `UK-TSO-0001ITP-00090entry`, a virtual reverse point.
  - ENTSOG's allocation remark: "Virtual Point, currently Moffat is only Unidirectional exit".
  - Effects in 2026-08/09 silver: the nominations value is null on all 14 days, and allocations are N/A
    placeholders.
  - National Gas TSO's real Moffat exit is never fetched for any non-physical-flow indicator. `physical_flows`
    carries `UK-TSO-0001`/`ITP-00090` exit.
  - Candidate fix: add or switch to `UK-TSO-0001ITP-00090exit`.
- **[gridflow connector] The BBL company filters return nothing.**
  - `UK-TSO-0004ITP-00063entry`/`exit` (`endpoints.py:29-30`, Julianadorp/Balgzand) return no rows in all 42
    nominations, renominations and allocations bodies for 2026-08/09.
  - BBL company's Bacton side, `ITP-00207`, is not requested.
- **[gridflow silver] Generic ENTSOG dtypes depend on response content.**
  - Allocations' not-applicable placeholder rows send `""` for boolean fields, so silver `is_cmp_relevant` is
    String in allocations but Boolean in nominations and renominations. `is_na` is Int64 against Null.
  - A day whose response lacks placeholders would write different dtypes into the same table's partitions.
  - `silver/entsog/generic.py` casts only numeric-looking columns and coerces no booleans.
- **[gridflow silver, observation] Allocation placeholders are kept with a different gas-day start.**
  - The N/A rows (`isNA` 1, `periodFrom` 05:00+02:00) become `timestamp_utc` 03:00 UTC, while valued rows sit at
    04:00 UTC. So `entsog/allocations` has two `timestamp_utc` values per gas day.
  - Their dateless `id` recurs every day.
  - As sent by the vendor; worth a filter or flag in silver.
- **[vendor, open research] `meta.total` exceeds `meta.count` under `limit=-1`.** 14 against 7 for
  nominations and renominations, 8 against 7 for allocations, in every 2026-08/09 body. Same question as the
  physical_flows `984/1650`.
- **[vault, fixed in this branch] All three ENTSOG notes were wrong in several places.** They stated the wrong
  dedup key (a 4-tuple, not `id`), "day-ahead" or "capacity" semantics, a physical-flows publication lag, `+02:00`
  stamps in the silver sample and a broken `id` schema cell. The allocations schema omitted three columns. All are
  corrected with code citations.
- **[front-end template] Chart y-tick labels clip at 390 for values of 100 million or more** (`chart_svg.fmt_num`
  plus the narrow left margin); there is no unit-scaling key in `chart_spec`.

## Nits fixed (review 2026-10-06, APPROVE with 9 nits)

Rebuilt with `--only entsog/nominations` after the seat's compact-tick fix: build passes, detector `[]`, 0 em dashes. All three notes mirrored with `cp` and checked with `cmp` (byte-equal, CRLF kept). The notebook was re-run with `scripts/run_notebooks.py`; series and sample are unchanged. The 390 tick clip from my first report is resolved by the seat's fix (the reviewer measured `0`, `50M`, `100M`, `150M`, nothing clipped). My edits after it are prose only and were not re-screenshotted.

1. **BBL company loss placement.** `what_it_is` now says "BBL company's two return no rows", next to the nine filters (59 of 60 words).
2. **`meta.total`.** `raw_feed.note` now says the response's `meta.total` can exceed the records returned, unexplained (30 of 30 words). It gives no counts, because the 14-against-7 figures come from our own responses; they stay in the vault Known issues and the defect log.
3. **Notebook in UK time.** Cell 2 converts `timestamp_utc` to UTC (`.dt.tz_convert("UTC")`) before printing and plotting. The table now reads `2026-09-13 04:00:00+00:00`, matching the chart.
4. **Commands against `needs`.** The CLI takes one dataset per call, and the page allows at most three command lines. Both comments now end "repeat per member".
5. **Allocations `differs`.** Now "Allocated quantity, flow status; National Gas TSO sends only not-applicable placeholders at 03:00 UTC" (14 words). The dtype detail stays in the vault.
6. **Key against `id`.** The `id` guide line now reads "Vendor record id, the deduplication key: indicator, dates, keys and unit joined". `record.key` stays the four columns as the practitioner's key.
7. **Vault schema and wording.**
   - `id_point_type` changed to Int64 in nominations and renominations.
   - `is_na` changed to Null dtype in nominations and renominations, and to Int64 in allocations.
   - `is_cmp_relevant` changed to `str` in allocations, with a note.
   - The allocations Known issues now says "no gas-day date, only a fixed 2026-2027 range".
   - The broken link `20-domain/markets/gas-nominations.md` predates this work and is left for the seat (the target does not exist in the vault).
8. **Alt text.** It now includes Bacton (BBL)'s rise to 91,224,000 on the 20th.
9. **Domain readings.**
   - Renominations `differs` now uses GNI's remark wording ("latest aggregate renomination when published") instead of "the revision of the nomination".
   - "a virtual reverse point" is removed from the nominations and renominations Known issues, leaving the vendor remark itself.
   - "(revised)" is removed from the renominations overview.
   - The chart key note never used "virtual reverse", so it is unchanged.

Summary: all 9 nits fixed; build passes, detector `[]`, mirrors byte-equal, and the notebook prints UTC.
