# entsog/gas-quality: author report

Writer: Opus 5.5 · high, 2026-10-07. Family `gas-quality`, lead `gcv`, members `wobbe_index`, `methane_content`, `hydrogen_content`, `oxygen_content`. Built with `--only entsog/gcv`.

## Recommendation: SHIP (thin but accurate)

The held capacity page's silver loss does **not** apply here. Every bronze record survives to silver, for all five members:

| Member | Bronze records (valued) | Silver rows (valued) |
|---|---|---|
| gcv | 98 (56) | 98 (56) |
| wobbe_index | 126 (28) | 126 (28) |
| methane_content | 42 (42) | 42 (42) |
| hydrogen_content | 28 (28) | 28 (28) |
| oxygen_content | 28 (28) | 28 (28) |

The reason: gas-quality records are one gas day long. `periodFrom` is the fetched day, so `partition_records_to_target_date` (`silver/entsog/generic.py:157-161,332`) keeps them all. Counts match DATA-MATRIX (98, 126, 42, 28, 28).

The family has three oddities. The page states them plainly and avoids misstating any of them.

- **Interconnector's exit side is 0.** Its Bacton (IUK) exit sends `value` 0 on every row of all five members. The chart filters it out with `value > 0` and the caption says so.
- **One implausible GCV.** On 20 Sep, Interconnector's GCV of 14.253 conflicts with National Gas TSO's 11.6136 for the same point. It also conflicts with Interconnector's own Wobbe index (see Defects). The chart shows the point, the key note names it, and the eight rows show it beside National Gas TSO's figure. The page asserts no cause.
- **Wobbe is mostly placeholders.** Only Interconnector sends Wobbe values; seven of the nine filters return not-applicable placeholders.

## Status

- **Build:** `gridflow-build --only entsog/gcv` passes.
  - All 28 warnings are the generic "no Pydantic class" notices.
  - `wrote: data-sources/entsog/gas-quality.html`; the five member pointers were rewritten.
- **Detector:** `detect.mjs --json` returns `[]`. Em dashes in the page: 0.
- **Rubric greps** on the rendered text find nothing: locally, held, our, since 20, % of, live, now, yet, soon, planned, coming, real-time, digits plus rows or days, →, middle dot, em dash.
- **Mirrors:** all five notes copied with `cp` and checked with `cmp`: byte-equal, CRLF on every line (446, 285, 248, 247, 247 lines).
- **Artefacts** (no staged chart spec or authored override existed):
  - `site/hifi/data/series/entsog/gcv.json` (`spec_origin: vault`, 3 series × 9 points, 27 rows used).
  - `samples/entsog/gcv.json` (`gridflow-sample`, ran cleanly; this family has no partition dtype drift).
  - `notebooks/entsog/gcv.json` plus `gcv-5.png` (`scripts/run_notebooks.py`, 5 cells, no errors).
- **Screenshots** (light; the site has no dark theme), taken at 1440, 1024 and 768, and at 390 in a true 390 px iframe:
  - Location: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\gq\shots\s_<width>_<n>.png` (full pages: `full_<width>.png`).
  - Nothing is clipped or overlapping, at any width: the hero and scenery, the five member chips (wrapping at 390 and 768), the facts, the chart with ticks 11 to 15 and its key, all five request URLs, the commands, the folded frame and guide, the notebook and related.
  - The unfolded frame was not screenshotted; it uses the same template as the approved nominations page.
  - Three prose fixes came after the shots, each about the same length, so the shots are not retaken:
    - the alt text and one key note, with figures rounded to the committed series;
    - `what_it_is`, now "Some filters return not-applicable placeholders…", scoped because two GCV filters return nothing and the content indicators send no placeholders;
    - the `value` guide line, which now notes Interconnector's exit 0.
  - Static server on 9874 was started with `timeout 1200`, so it stops itself. Port 9670 was not touched.

## What the data is (the "look hardest at" answers)

- **What one row is.** One vendor record per gas day, operator, point and direction.
  - `periodFrom` to `periodTo` is one gas day: 06:00+02:00 to 06:00+02:00 next day, as sent, which is 04:00 UTC to 04:00 UTC.
  - Silver dedups on the vendor `id`, `keep="last"`, per daily bronze read (`generic.py:193-199`).
  - `(timestamp_utc, operator_key, point_key, direction_key)` is unique in all five tables (0 duplicate groups). No repeated rows.
- **Points requested.** Nine `pointDirection` filters (`connectors/entsog/endpoints.py:24-34`), one `from=to=D` request per gas day (`client.py:78-102`). What comes back, per response, on all 14 days:

  | Member | Records | Valued | Placeholders | Filters returning nothing | `meta.count` / `meta.total` |
  |---|---|---|---|---|---|
  | gcv | 7 | Interconnector IUK entry, IUK exit (0); National Gas TSO IUK exit; GNI Moffat (IE) entry | GNI Moffat (IE) exit; National Gas TSO Bacton (BBL) exit; BBL company Julianadorp exit | BBL company entry; National Gas TSO Moffat `ITP-00090` entry | 7 / 8 |
  | wobbe_index | 9 | Interconnector IUK entry, IUK exit (0) | the other seven | none | 9 / 9 |
  | methane_content | 3 | Interconnector IUK entry, exit (0); GNI Moffat (IE) entry | none | six | 3 / 6 |
  | hydrogen_content, oxygen_content | 2 | Interconnector IUK entry, exit (0) | none | seven | 2 / 4 |

- **Coverage.** Bronze and silver both hold 14 gas days: 1 to 5 August and 13 to 21 September 2026. The 38-day gap is ingest coverage, not silver loss.
- **Units.** Taken from the rows' `unit` column:
  - `kWh/Nm3` on every gcv and wobbe_index row;
  - `% (mol/mol)` on every methane, hydrogen and oxygen row.

  The generic transformer does not convert (`generic.py:189-191` casts `value` to Float64, `strict=False`). Nothing in the rows, the vault or the code states reference conditions (combustion or metering temperature). The page says the response states none. The chart axis carries one unit, `kWh/Nm3`.
- **Gas day as stored.**
  - `timestamp_utc` is a copy of `period_from` (`generic.py:185-187`): the gas-day start, 04:00 UTC for every valued row.
  - Placeholders send an earlier `periodFrom`, so they land at different stamps: 05:00+02:00 is 03:00 UTC, and GNI's Wobbe placeholders send 04:00+02:00, which is 02:00 UTC. So gcv has two stamps per gas day and wobbe_index three.
  - `last_update_date_time` is the vendor's `lastUpdateDateTime`, in UTC. The pipeline does not use it.
  - `ingested_at` is the silver transform time (`generic.py:201-206`).
- **`lastUpdateDateTime` against gas-day start** (all 2026-08/09 valued rows):
  - GNI: +25 to +28.6 h.
  - Interconnector: +28.6 to +51.8 h.
  - National Gas TSO: +83.8 to +133 h.
- **`flowStatus`:**
  - GNI and National Gas TSO: `Provisional` on every row.
  - Interconnector: `Confirmed`, except 15 September, which is `Provisional`.
  - Placeholders: an empty string.
- **Physical plausibility (observation, scoped to 2026-08/09).**
  - GCV of 11.43 to 11.87 kWh/Nm3 at all three valued points, apart from 20 Sep, is in the normal range for H-gas. Wobbe of 14.49 to 14.90 kWh/Nm3 is too.
  - The two reports of Bacton (IUK), National Gas TSO's exit and Interconnector's entry, agree within 0.02 on 13 of 14 days. The largest gap is 0.0197, on 19 Sep.
  - 20 Sep: Interconnector 14.253 (`Confirmed`, updated 2026-09-21 08:48 UTC) against National Gas TSO 11.6136.
  - Interconnector's own GCV/Wobbe pair implies a relative density, (GCV/W)², of 0.9149 that day, against 0.6229 to 0.6346 on its other 13 days. The 14.253 is inconsistent with its own Wobbe.
  - Methane: GNI 87.68 to 88.70 %, Interconnector 84.868 to 90.086 %.
  - Hydrogen 0 to 0.01 % and oxygen 0 to 0.006 %, Interconnector only.
- **Flat runs.**
  - From 13 to 18 Sep, National Gas TSO sends 11.6429 and Interconnector 11.645 (GCV), 14.653 (Wobbe, to the 19th), 85.39 (methane) and 0.005 (hydrogen).
  - Interconnector's rows each have their own `lastUpdateDateTime`. National Gas TSO's do not: gas days 14 and 15 Sep share one stamp, and 18 to 20 Sep share another (corrected after review; see `gas-quality-author-2.md`). Unexplained.
- **Thin members.** Hydrogen and oxygen are one operator at one point, with values of 0.01 or less. Their `differs` lines say exactly who reports and add no trend words.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| No silver loss (whole page; no hold) | Bronze-against-silver table above (script `scratchpad\gq\cmp_bs.py`); `generic.py:157-161,332` |
| Request URLs, nine filters, `+` encoding (`raw_feed.requests`, `family.members[].request`) | `request_url` in each member's bronze `.meta.json` for 2026-09-21, copied verbatim; `endpoints.py:24-34,95-125` |
| One request per gas day; ingest `--end` exclusive, transform `--end` inclusive | `client.py:78-102`; same commands as the approved nominations page |
| `meta.total` can exceed records returned (`raw_feed.note`) | gcv 7/8, methane 3/6, hydrogen and oxygen 2/4 in every body |
| Units `kWh/Nm3` and `% (mol/mol)`, unconverted; no reference conditions (`what_it_is`, `differs`, fields, chart unit) | Silver `unit` column on all rows; `generic.py:189-191`; no reference-condition text in rows, vault or code |
| Grain and key (`facts.grain`, `record.key`) | Dedup on `id` (`generic.py:193-199`); 0 duplicate 4-tuples in all five tables |
| x_label "gas day, starting 04:00 UTC" | Every charted row is at 04:00 UTC; `generic.py:185-187` |
| Placeholders with remarks (`what_it_is`, `item_remarks`, `is_na`, `value` lines) | gcv silver: 42 rows with `is_na` 1, null `value`, remarks as quoted in the vault |
| Chart: filter `value > 0`, group by operator, three series (caption) | Series provenance: 42 rows matched, 27 used; `UK-TSO-0003` exit is 0 on all 14 rows |
| Alt text and key-note numbers | Committed series: moffat_ie 11.87, 11.83, 11.76, 11.82, 11.79, 11.8, 11.82, 11.83, 11.84; bacton_iuk_exit 11.643 ×6, 11.693, 11.614, 11.59; bacton_iuk_entry 11.645 ×6, 11.673, 14.253, 11.602 |
| "within 0.02 of National Gas TSO's except 14.253 on the 20th" | Silver gaps 0.0021 (13 to 18), 0.0197 (19), 2.6394 (20), 0.0118 (21) |
| "Provisional throughout" (GNI and National Gas TSO key notes) | `flow_status` `Provisional` on all 14 rows of each |
| "GNI's Moffat exit is a not-applicable placeholder" | gcv `IE-TSO-0002`/`ITP-00495` exit: `is_na` 1 on all 14 rows |
| Wobbe `differs`: "only Interconnector sends values, National Gas TSO publishes GCV instead" | wobbe_index silver: valued rows only `UK-TSO-0003`; National Gas TSO `item_remarks` "…we publish GCV and not WI…" |
| Methane, hydrogen and oxygen `differs` | Silver operator/point/direction sets in the table above |
| Eight rows and caption | Sample: gas days 20 and 21 Sep, `value` not null, 4 rows a day, shape (8, 42) |
| Field lines: `is_cmp_relevant` "kept as text", `item_remarks`, `is_na` "1 on placeholders" | gcv silver dtypes (`is_cmp_relevant` String, `is_na` Int64) and placeholder rows |
| `notebook.lead` (relation, date column, ends included, lineage dropped) | gridflow `silver/schema_manifest.py:208,215,219,225` (`timestamp_utc` for all five); same `query()` path as the approved nominations page |
| `plot_alt` | Notebook output table (cell 4): Wobbe 14.653 to the 19th, 14.901, 14.613; GCV 11.645 to the 18th, 11.673, 14.253, 11.602; image `gcv-5.png` |
| Related: nominations share the same nine filters | `endpoints.py:118-125` (every operational dataset except physical_flows) |

## Body corrections (all five notes, smallest spans)

Applied by `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\gq\fix_notes.py`: count-asserted replacements, CRLF kept, schema tables and samples generated from silver.

1. **Overview, first line.**
   - "(kWh per cubic metre)" and "volume fraction" become the units as sent: `kWh/Nm3`, and `% (mol/mol)` (a molar fraction). "No reference conditions in the response" is added.
   - Also added: which operators send values in 2026-08/09, Interconnector's exit at 0, and National Gas TSO's "GCV not WI" remark (Wobbe note).
   - The generic "daily `periodFrom`/`periodTo`" paragraph is correct for this family and is left alone.
2. **Publication lag row.** "Same-day for `Provisional`; revised within ~1 week" was copied from physical flows. It becomes "Not vendor-documented here", with each member's scoped `lastUpdateDateTime` lags and `flowStatus` facts.
3. **Dedup key.** The 4-tuple becomes the vendor `id`, `keep="last"` (`generic.py:193-199`), with the 4-tuple's uniqueness as an observation.
4. **Point-in-time field.** `last_update_date_time` becomes "none used by the pipeline" (`generic.py:181-183,201-206`).
5. **Silver schema.**
   - gcv and wobbe: regenerated in silver's order, with these fixes:
     - added `timestamp_utc`;
     - fixed the broken `id | str | int` and `data_set | str | int` cells (`data_set` is Int64);
     - `is_na` is Int64, not str;
     - `is_cmp_relevant` is str, not bool;
     - `id_point_type` is Int64;
     - six all-null columns are Null dtype.
   - wobbe gains `point_type`, `id_point_type` and `is_archived`, which its silver has.
   - methane, hydrogen and oxygen said "Schema is generic and dynamic". Each now has its real table: `is_na`, `item_remarks`, `general_remarks` and `booking_platform_label` are Null dtype, and `is_cmp_relevant` is bool.
6. **Silver sample.**
   - gcv showed a May record with `+02:00` stamps. Wobbe showed a placeholder with `+02:00` stamps and `"value": ""`. The three contents said "(empty validation window)".
   - Each now shows a real 21 Sep silver row in UTC: National Gas TSO IUK exit (gcv), Interconnector IUK entry (wobbe, hydrogen, oxygen) and GNI Moffat (IE) entry (methane).
7. **Known issues.** Added:
   - requested against returned, per member, with the placeholder remarks quoted;
   - Interconnector's zero exit;
   - for gcv, the two Bacton (IUK) reports and the 20 Sep outlier with the relative-density check, the flat 13 to 18 Sep run, and two stamps per gas day;
   - for wobbe, three stamps per gas day, unstable placeholder `id` suffixes and the flat 14.653 run;
   - for methane, the flat 85.39 run.
8. **Implementation delta** (gcv, wobbe). "Live API returns the indicator name in `meta.fields`" is wrong: `meta.fields` lists field names. The indicator is echoed in `meta.query.indicator`, and the constant is cited at `endpoints.py:95-115`.
9. **Modelling notes.** "Filter on `flowStatus == 'Confirmed'`" becomes:
   - drop placeholders (`is_na == 1`) and Interconnector's zero exit rows;
   - a `Confirmed` filter keeps Interconnector only, because GNI and National Gas TSO are always `Provisional`.

Bronze samples and curl examples are left unchanged. They are valid vendor examples; the contents' empty-response sample is a real vendor case for that single filter. The broken link `20-domain/markets/gas-nominations.md` predates this work and is left alone.

## Not verified

- **Reference conditions** for `kWh/Nm3` (combustion and volume temperature). Not in the response, the vault or the code. The page says the response states none.
- **Whether 0 on Interconnector's exit means "no flow" or "not measured".** No remark accompanies it. The page and vault call it "not a gas-quality measurement" and leave it out of the chart.
- **Why 14.253 on 20 Sep.** It is inconsistent with National Gas TSO's figure and with Interconnector's own Wobbe; it is not confirmed as an error by ENTSOG.
- **Why values repeat from 13 to 18 Sep** at both operators.
- **What `meta.total` counts** (8, 6, 4 against 7, 3, 2). This is the same open question as the sibling pages.
- **The domain meaning of the Wobbe index range** and of H-gas specification. Plausibility is stated only as an observation in this report, never on the page.

## Open questions

1. Should silver (or a gold view) drop not-applicable placeholders and Interconnector's zero exit rows, or flag them?
2. Should the connector stop requesting the filters that never return gas quality (BBL company entry, National Gas TSO Moffat `ITP-00090` entry)? Or should it request National Gas TSO's Moffat exit, which is the same question as the nominations page raised?
3. Does the 20 Sep GCV get raised with ENTSOG or Interconnector, or just flagged in the vault (done)?

## Template problems

1. **Overlapping lines.** National Gas TSO's and Interconnector's Bacton (IUK) series differ by 0.002 from 13 to 18 Sep, so the later-drawn line hides the earlier one. The key note states National Gas TSO's 11.643 so a reader is not misled. A renderer offset or hollow markers would help. Minor.
2. **Family charts read one silver table** (known). The natural cross-member reading, GCV against Wobbe at one point, lives in the notebook.
3. **Build warnings name the wrong module** ("gridflow.schemas.elexon" for ENTSOG), as before. There is also no dark theme to check.

## Defects

- **[vendor data, observation] Interconnector GCV on gas day 2026-09-20 is implausible.**
  - Interconnector (`UK-TSO-0003`) Bacton (IUK) `ITP-00005` entry sends GCV 14.253 kWh/Nm3 (`Confirmed`, `lastUpdateDateTime` 2026-09-21T08:48:29Z).
  - National Gas TSO's exit report for the same point and day is 11.6136.
  - Interconnector's own Wobbe index that day (14.901) gives a relative density of (14.253/14.901)² = 0.915, against 0.623 to 0.635 on its other 13 days in 2026-08/09.
  - Silver keeps it as sent. Flag for a vendor query and a gold-layer plausibility check.
- **[vendor data, observation] Interconnector sends 0 for its Bacton (IUK) exit on every gas-quality indicator.**
  - GCV, Wobbe, methane, hydrogen and oxygen: `value` 0, `Confirmed`/`Provisional`, on all 14 gas days of 2026-08/09.
  - Zero is not a gas-quality measurement; it should be filtered or flagged in silver or gold.
- **[gridflow silver, observation] Gas-quality placeholders are kept, at earlier stamps.**
  - `entsog/gcv` has 3 not-applicable placeholders a day: GNI `ITP-00495` exit, National Gas TSO `ITP-00207` exit and BBL company `ITP-00063` exit. `entsog/wobbe_index` has 7 a day.
  - All carry `isNA` 1 and `value` `""`, which becomes null.
  - Their `periodFrom` is earlier than valued rows: 03:00 UTC, and 02:00 UTC for GNI in wobbe. So gcv has two `timestamp_utc` values per gas day and wobbe_index three.
  - Wobbe placeholder ids alternate their `_NA<n>` suffix between days (for example `_NA0`/`_NA4` for National Gas TSO Bacton (BBL) exit), so `id` is not stable across days.
- **[gridflow connector] Gas-quality filters that return nothing.**
  - `UK-TSO-0004ITP-00063entry` returns nothing for GCV, and the same for `UK-TSO-0001ITP-00090entry` (`endpoints.py:24-34`).
  - Methane, hydrogen and oxygen return only Interconnector (plus GNI for methane).
  - National Gas TSO's real Moffat exit is never requested; this is the same defect as logged for nominations.
- **[vendor, open research] `meta.total` exceeds `meta.count` under `limit=-1`.** gcv 8 against 7, methane 6 against 3, hydrogen and oxygen 4 against 2, in every 2026-08/09 body. This is the same question as physical_flows and nominations.
- **[vendor data, observation] Identical values re-sent on consecutive days.**
  - 13 to 18 Sep 2026: National Gas TSO GCV 11.6429; Interconnector GCV 11.645, methane 85.39 and hydrogen 0.005; Interconnector Wobbe 14.653 to 19 Sep.
  - Interconnector's rows each have their own `lastUpdateDateTime`. National Gas TSO's stamps are shared across gas days (see `gas-quality-author-2.md`). Unexplained.
- **[vault, fixed in this branch] All five gas-quality notes were wrong in several places:**
  - units ("kWh per cubic metre", "volume fraction");
  - a physical-flows publication lag;
  - the dedup key (a 4-tuple, not `id`) and the point-in-time field;
  - broken `id`/`data_set` schema cells, a missing `timestamp_utc` and wrong dtypes, with Wobbe missing three columns;
  - "generic and dynamic" or empty schemas and samples on the three content notes;
  - `+02:00` silver samples, with Wobbe showing a placeholder;
  - the `meta.fields` claim;
  - the `flowStatus == 'Confirmed'` advice.

  All are corrected with code citations.
