# Regional breakdown of FES data (Electricity): writer's report

Page `neso_data_portal/regional-breakdown-of-fes-data-electricity`, lead `fes_regional_demand_active_power`, nine members.
Canonical note `C:\gridflow-wt\vault-neso-fes\30-vendors\neso-data-portal\datasets\regional-breakdown-of-fes-data-electricity.md`
(CRLF kept: 1,009 CRLF of 1,009 line ends), mirrored to `vault\neso_data_portal\` in `C:\gridflow-wt\fe-neso-fes` and `cmp`
clean.

## Gates

- `gridflow-build --only neso_data_portal/fes_regional_demand_active_power`: exit 0. The only warning is the known
  "37 line(s) in Known issues" caveat-grammar one, not from this page.
- Detector `[]`. No em dashes on the page (0), and no "locally", "our copy", "live", "real-time", "planned", "not yet".
- Artefacts, all from silver: `site/hifi/data/series/neso_data_portal/fes_regional_demand_active_power.json` (`spec_origin:
  vault`, 1 series x 6 points, 18,426 rows used, 0 duplicates dropped, 0 nulls dropped);
  `samples/.../fes_regional_demand_active_power.json` (`gridflow-sample`, 8 rows x 17 columns);
  `notebooks/.../fes_regional_demand_active_power.json` + `-4.png` (`run_notebooks.py`, 5 cells, 8.4 s, no errors).
- No staged chart spec or authored override existed for the lead.
- Screenshots at 1440, 1024, 768 and a 390 px iframe (two passes to reach the foot), from my server on 9941 (PID 56547,
  started with its PID echoed, stopped by `kill 56547`). Hero, nine id chips, facts, chart and key, all nine request
  wells, commands, the folded frame and its guide, the notebook panel and the related list are all fully visible.
  Nothing clipped or overlapping. At 390 the frame folds after `scenario` (known follow-up). Light theme only: the site
  has no dark theme.

## The chart and how I reproduced it

Bar chart, `type: bar`: FES 2024 edition (NESO file `fes2024_regional_breakdown_active_power.csv`, `last_modified`
2024-07-15T06:43:07), pathway `HT`. It plots `DemandPk` summed over every location (370 GSPs times seven demand types,
plus 481 direct-connect `T` locations = 3,071 rows per label) for labels 25, 30, 35, 40, 45 and 50, shown as NESO's
financial years 2025/26 to 2050/51 through `group_map`. `dedup` is on the full registry entity key, as a guard only.

Reproduced independently with Polars (lazy scan, selected columns), before distil:

| Label | Sum `DemandPk` (MW) | Committed series |
|---|---:|---:|
| 25 | 57,981 | 57,980.836 |
| 30 | 62,830 | 62,829.669 |
| 35 | 74,639 | 74,638.645 |
| 40 | 90,100 | 90,099.701 |
| 45 | 100,259 | 100,259.034 |
| 50 | 104,054 | 104,053.957 |

The alt text uses these values. "About four fifths" = 104,054 / 57,981 = 1.79. "Fastest between 2035/36 and 2040/41"
= the largest five-year step (+15,461 MW).

Why this reading: it is the practitioner's headline from a regional FES file, projected peak demand growth, and it
shows one edition and one pathway only, so it never mixes editions or reads as history. Why the sum is legitimate:
NESO defines `DemandPk` as "expected demand at the specified location at the time of the highest total demand for the
nation". It is coincident with the national peak, so it adds across locations, and the eight types are components of a
location's demand. 2024 has no blank `DemandPk` cells (the 2021 to 2023 blanks would have made a sum incomplete). It
does contain one small negative residential `DemandPk` value per bar (`KIIN_P`, -0.085 to -0.133 MW), which the sum
includes as published. (Corrected in round 2: `DemandPk` is negative on residential rows only, 146 rows in 2024,
minimum -0.625 MW.)

Why `HT` and its name: the 2024 file carries `EE`, `HE` and `HT`, and this package's dictionary does not decode them
(see defects). The page names it "Holistic Transition" on two pieces of NESO evidence. First, NESO's FES 2024
building-block file (silver `fes_building_blocks_main`, edition 2024, `published_at` 2024-08-02T10:37:06) names its
pathways Holistic Transition, Electric Engagement, Hydrogen Evolution and Counterfactual. Second, NESO's tRESP
dictionaries (field info `20261008T114228Z`, e.g. `tresp_demand_pathways_gsp`) write "Holistic Transition (HT)". The
chart keeps the code `HT` visible in the caption, and the key note says where the name comes from. I chose `HT` over
`EE` and `HE` to match the sibling tRESP generation page, whose single short-term pathway is `tRESP - HT`.

Notebook: `data.sql()` on `silver_neso_data_portal_fes_regional_demand_active_power_latest`. `query()` would filter on
`timestamp_utc`, the capture time, because the record is `temporal: none`. Cell 3 is peak by pathway and label for
2024: EE / HE / HT at 23 = 57,479 / 57,562 / 57,295 and at 50 = 118,551 / 105,854 / 104,054, which match my Polars
sums. Cell 4 is the line plot; `plot_alt` was read off the PNG and these outputs. Cell 5 is HT at label 50 by type for
the three conditions: `T` 3,962 at peak but 29,857 MW at summer afternoon, and `Z` 0 at peak but 8,970 MW at summer
afternoon.

## Captures and editions

Each table has exactly one silver capture per resource, all written 2026-10-08. Silver rows equal the bronze file's
data lines for every one of the 26 read captures. Every family's registry entity key has 0 duplicates. Every bronze
header matches its registry epoch.

| Table | Editions (silver rows) | Bronze-only |
|---|---|---|
| `fes_regional_demand_active_power` | 2021 352,284 · 2022 340,920 · 2023 329,556 · 2024 257,964 | |
| `fes_regional_dg_gt_1mw` (held) | 2021 103,431 · 2022 111,700 · 2023 107,234 · 2024 75,106 | |
| `fes_regional_dg_lt_1mw` (held) | 2021 171,531 · 2022 235,075 · 2023 227,671 · 2024 156,324 | |
| `fes_regional_dsr` | 2021 45,384 · 2022 43,920 · 2023 42,456 | |
| `fes_regional_gsp_info` (held) | 2021 370 · 2023 370 · 2024 373 | 2022 (not valid UTF-8) |
| `fes_regional_storage_gt_1mw` | 2023 14,042 · 2024 10,627 | |
| `fes_regional_storage_gt_1mw_pre2023` | 2022 14,245 | 2021 (preamble, repeated key) |
| `fes_regional_storage_lt_1mw` (held) | 2023 45,510 · 2024 31,248 | |
| `fes_regional_storage_lt_1mw_pre2023` | 2021 39,955 · 2022 46,990 | |

Scenario sets by edition (demand): 2021 `CT LW SP ST`; 2022 and 2023 `CT FS LW ST`; 2024 `EE HE HT`. Labels run 20
to 50 (2021), 21 to 50, 22 to 50, and 23 to 50 (2024). `published_at` for each file is its CKAN `last_modified`. For
the lead: 2021-07-06, 2022-07-15, 2023-08-29 and 2024-07-15.

`dedup:` is set on the chart and the frame (full entity key, `order_by: capture_written_at`) as a guard: no capture
repeats rows today.

## What one row is, per table

- **Demand (lead):** one scenario, one location (`gsp`), one demand type and one year label, with three MW values:
  `DemandPk`, `DemandAM` and `DemandPM`. The year label is a financial start year (NESO: "25" = 2025/26). In 2024, the
  370 GSP locations carry the seven types `C D E H I R Z`, and the 481 direct-connect locations carry only `T`. In 2021
  to 2023 the split is 367 and 272.
- **DSR:** one scenario, GSP and year label: the expected change in demand at winter peak due to demand side response,
  in MW. Editions 2021 to 2023 only.
- **Storage of 1 MW or more (current, 2023 and 2024):** one scenario, technology, `location` and year label (the
  winter starting in that year): `Capacity` (available rate of charge, MW) and demand at three conditions (negative
  means filling, per NESO).
- **Storage of 1 MW or more, pre-2023:** the same columns and meaning, 2022 only. The 2021 file is captured but not
  read.
- **Storage below 1 MW, pre-2023 (2021 and 2022):** one scenario, `etys_location` and year label (no `tech` column),
  with the same four measures.
- **Storage below 1 MW, current (held):** like pre-2023, with `tech` added in 2024.
- **DG above and below 1 MW (held):** one scenario, `tech`, `etys_location` and year label, with capacity and three
  condition values.
- **GSP info (held):** one GSP id per edition, with group, minor FLOP, name, latitude, longitude and comments (raw
  strings).

On "the `_pre2023` tables are a different file shape" (batch brief): this is only partly true. The 2022 storage file
of 1 MW or more has exactly the same header as 2023 and 2024. Its split exists because the 2021 sibling file has a
two-line preamble and cannot be read. The storage-below-1-MW pre-2023 header equals the 2023 current header (neither
has `tech`); only 2024 adds `tech`, and that split is semantic (conflicting dictionaries). The page never sums across
the split. The member lines say "Same columns, 2022 only" and "NESO's later dictionaries differ, so kept apart".

## Body corrections (canonical note)

1. Lead section, scenario codes: replaced "`TODO: verify` the vendor's meaning of each, which neither the registry nor
   FACTS records" with what the field info decodes. Evidence: field info `20261008T114228Z`,
   `fes_regional_demand_active_power.json` (comment "LW: Leading the Way / CT: Consumer Transformation / ST: System
   Transformation / SP: Steady Progression"); `fes_regional_storage_gt_1mw_pre2023.json` and `_lt_1mw_pre2023.json`
   ("FS: Falling Short / CF: Central Forecast"); `fes_building_blocks_main` 2024 pathway names; tRESP "Holistic
   Transition (HT)".
2. Lead section, `type` codes: replaced "`TODO: verify` their meaning" with NESO's decode, from the same demand field
   info ("R = Residential ... T = Transmission direct connects, Z = Electrolysers"). Added that `T` rows sit at their
   own locations (272 in 2021 to 2023, 481 in 2024), measured on silver.
3. Lead section, blanks: added that the `DemandPk` blanks are all on `T` rows at 114 locations per edition (measured).
4. DSR section: replaced the scenario `TODO: verify` with the DSR field info decode (`fes_regional_dsr.json`, 2023
   resource, the same four-code comment) and the `FS` decode.
5. `updated:` 2026-10-10 changed to 2026-10-24.

I did not change the body statement "the page never converts it [the year label] to one [a calendar year]". The site
page labels bars "2025/26" and so on: NESO's own financial-year reading from the dictionary, not a calendar-year
conversion. Flagged for the checker below.

## Held members (one line each, from the registry question and the ledger)

- `fes_regional_dg_gt_1mw`: "NESO's capacity description says below 1 MW, against the file's title of above 1 MW".
- `fes_regional_dg_lt_1mw`: "NESO's 2024 dictionary describes storage, not small generation, and the year label's
  period is unstated".
- `fes_regional_gsp_info`: "NESO states no unit or datum for the positions; its 2022 file is not valid UTF-8". This
  covers both the registry question (coordinate unit and CRS) and the ledger's "2022 UnicodeDecodeError".
- `fes_regional_storage_lt_1mw`: "NESO's 2023 and 2024 dictionaries call some measures generation, not storage; sign
  unsettled".

## Unverified or judgement calls

- The `HT` = Holistic Transition naming is drawn from NESO's other FES files, not from this package. The page says so
  in the key note.
- "Typically a Sunday" for `DemandAM` and `DemandPM` paraphrases NESO's "typically in June-August on a Summer Sunday
  morning" and "Summer Sunday afternoon". The June to August window was dropped for budget.
- `gis-boundaries-for-gb-grid-supply-points` related note says "codes not compared": I did not join these codes to
  that package.

## Lead and page set

The lead is the right choice. Demand is the only member with all four editions and the three-condition demand reading,
and it is eligible. Of the others: DSR has no 2024 edition; storage of 1 MW or more has `wintpk` and `summam` zero in
every row of both editions; the pre-2023 tables are single or old editions. No reorder recommended.

## Defects (pasteable)

- **NESO data portal, regional FES demand and DSR dictionaries (vendor):** the field info for the 2024 demand resource
  `7bd643c0-6aad-41ac-aa59-92b68992d9a4` (snapshot `20261008T114228Z`) decodes `scenario` as LW, CT, ST and SP, the
  2021 set. The 2024 file carries only `EE`, `HE` and `HT`, which nothing in this package decodes. The 2024 storage
  dictionary (`eba5fd0a-...`) titles the column "FES Pathway" with no decode. Pages must name the 2024 pathways from
  NESO's other FES files (FES 2024 building blocks; tRESP "Holistic Transition (HT)").
- **NESO regional demand 2021 to 2023 (vendor data):** `DemandPk` is blank on every row of 114 direct-connect (`T`)
  locations in each of the 2021, 2022 and 2023 files (14,136, 13,680 and 13,224 cells), while `DemandAM` and `DemandPM`
  are filled. 2024 has none. Any cross-edition peak sum is incomplete for 2021 to 2023 unless it says so.
- **NESO regional demand (vendor sign), corrected in round 2:** NESO's dictionary gives no sign convention for demand,
  yet values are negative. `DemandPk` is negative on residential (`R`) rows only: 868 / 210 / 87 / 146 rows (2021 to
  2024), minimum -0.625 MW (2024). `DemandAM` is negative in 2021 on C 248, I 3,934 and R 916 rows, then on R only at
  1,312 / 924 / 174 (2022 to 2024). `DemandPM` is negative in 2021 on I 6,231 rows (minimum -757.855 MW) and R 1,021,
  then on R only at 1,312 / 924 / 678 (2022 to 2024). Rows with any measure negative: 8,542 / 1,312 / 1,011 / 678.
- **Vault note (fixed here):** scenario and type codes were marked `TODO: verify` although NESO's field info decodes
  them. Corrected in the lead and DSR sections. The storage sections keep their scenario `TODO`s; the same field info
  settles `CF`, `CT`, `FS`, `LW` and `ST` there.
- **Batch premise (planning):** the 2022 storage file of 1 MW or more has the same header as the current files. The
  `_pre2023` split there follows from the unreadable 2021 file, not a different shape. Only the below-1-MW 2024 file
  adds a column (`tech`).

## What the checker should look at hardest

1. **The pathway name.** Is naming `HT` "Holistic Transition" in the chart title and key acceptable on the evidence
   above (FES 2024 building blocks + tRESP dictionary), given this package's own dictionary lists only the 2021 codes?
2. **Financial-year labels** ("2025/26") on the bars against the note body's "the page never converts it". NESO's
   dictionary supplies "25" = 2025/26, so I read it as NESO's labelling, not a conversion.
3. **The additivity claim behind the sum**: `DemandPk` coincident with the national peak, summed over locations and
   types (including small negative `R` values and the `T` direct connects).
4. **`demand_pk` guide line**, "some direct connects blank before 2024": is a statement about NESO's files measured on
   silver acceptable?
5. **The 16-word held lines**, especially GSP info, which combines the registry's CRS question with the ledger's 2022
   encoding failure.
