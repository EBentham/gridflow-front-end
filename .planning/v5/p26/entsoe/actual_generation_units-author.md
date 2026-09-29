# entsoe/actual_generation_units: author report

Writer: Opus 5.5, 2026-09-29. Screenshot port 9825 (server stopped).

## Status

- Canonical note: `vault-p26-entsoe/30-vendors/entsoe/datasets/actual_generation_units.md`. It has a `page:` block plus body corrections. The note was LF at HEAD and is still LF, so the diff covers only the edits. The mirror `p26-entsoe/vault/entsoe/actual_generation_units.md` is byte-identical (`cmp`).
- Artefacts, all from real data:
  - `site/hifi/data/series/entsoe/actual_generation_units.json`: `spec_origin: vault`, 3 series by 168 hourly points, 504 rows used.
  - `samples/entsoe/actual_generation_units.json`: 8 rows.
  - `notebooks/entsoe/actual_generation_units.json` and `-5.png`: 5 cells, no errors.
- No staged chart spec or authored override existed for this dataset.
- `gridflow-build --only entsoe/actual_generation_units` passes. The three content warnings belong to other datasets.
- `detect.mjs --json`: one finding, `em-dash-overuse`, advisory. It counts the rendered EIC dash padding and is accepted under ruling #39. The page has 0 real em dashes, 0 "→" and 0 middle dots.
- Screenshots: 1440, 1024, 768 and 390 (390 through a 390 px iframe) in `scratchpad/agu-shots/`. Tiles viewed: the hero at all four widths; the chart at all four; the frame and guide at 1440, 768 and 390 after the column reorder; the notebook at 1440, 1024, 768 and 390; related at 1440 and 390.
  - Final wording edits made after the shots: the plot_alt end point, and the `unit_mrid` guide now reads "the nested generation units' EICs and names are dropped". They were rebuilt and detected, not re-shot; each changes one line of text only.
  - Nothing is clipped. The only exception is the known notebook filename clip at 390, which ruling #39 leaves to the seat.
  - After a first pass at 768, I moved `unit_mrid` and `generation_mw` to the front of `record.select.columns`. The folded frame now shows both columns at every width.
  - Dark mode: the site has no dark theme (no `color-scheme` or `prefers-color-scheme` rule in `site/hifi/assets` or `templates`), so dark renders the same as light.

## Coverage (the rows establish this)

- gridflow requests six zones (`DEFAULT_ZONES`, one request per zone per UTC day; `client.py:160-168`, `249-262`).
- Bronze days: 1 to 5 August and 8 to 21 September 2026, 19 days. 13 and 14 September were fetched twice.
- FR, BE and NL return `GL_MarketDocument`. GB, DE-LU and IE-SEM return Ack 999 every day.
- Silver: 229,612 rows, 2026-08-01 00:00 to 2026-09-21 23:45 UTC.

| Zone | Rows | Plant EICs | Generation units (nested) | PSR types | Resolution |
|---|---|---|---|---|---|
| FR `10YFR-RTE------C` | 200,160 | 110 | 150 | B01, B04, B05, B06, B10, B11, B12, B14, B18, B20 | PT15M |
| BE `10YBE----------2` | 13,610 | 32 | 44 | B01, B04, B10, B14, B18, B20, B25 | PT60M |
| NL `10YNL----------L` | 15,842 | 33 | 39 | B01, B04, B05, B14 | PT60M (Maasstroom PT15M) |

- By type, the largest groups are B14 (105,284 rows, 60 plants) and B04 (51,680 rows, 58 plants).
- No plant EIC appears in two zones or under two types.
- Values are never negative. FR consumption-side values are at most 241.5 MW.

## Keys and the collision (reproduced with numbers)

The structure, from bronze:
- `registeredResource.mRID` is the plant, a production unit. A95 `generation_units_master_data` (queried with `BusinessType` B11, "production unit" per the A95 note) lists these EICs under plant names, for example `17W100P100P02756` "GRAND MAISON", `49W000000000069K` "Claus" and `17W100P100P0273A` "CHEYLAS".
- Each `<TimeSeries>` also nests `MktPSRType/PowerSystemResources/{mRID,name}`, the generation unit (GRAND MAISON 1 to 12, COO 1 T to COO 3 T, and so on). No nested EIC appears in A95.
- Each nested EIC belongs to exactly one plant. 30 plants carry more than one nested unit: BE 8, FR 17, NL 5.

The code:
- The parser's `MktPSRType` branch reads only `psrType` (`parsers.py:345-348`).
- `unit_mrid` is taken from `registeredResource.mRID` (`351-352`).
- `registeredResource.name` (`353-354`) is absent from every response, so `unit_name` is "" on all 339,674 parsed rows.
- `outBiddingZone_Domain.mRID` is read into `in_domain` alongside generation (`289-297`).
- Dedup is `unique(["timestamp_utc", "area_code", "unit_mrid"], keep="last")` (`silver/entsoe/actual_generation_units.py:69-72`).

Reproduction:
- I re-parsed all 126 bronze files with `gridflow.connectors.entsoe.parsers.parse_timeseries_xml(value_tag="quantity")` and applied the transformer's event window and dedup in parse order.
- The result is 229,612 rows, matching silver with 0 extra rows, 0 missing rows and 0 value mismatches. Scripts: `scratchpad/agu_p2.py` and `agu_p4.py`.
- There are 339,674 parsed in-window points. 29,950 of them are the duplicate fetch of 13 and 14 September. That leaves 309,724 distinct series points, of which 80,112 are dropped by the plant key.

Classification of the 229,612 silver rows:

| Class | Rows |
|---|---|
| Plant had one series at that instant, generation (clean) | 137,358 (BE 10,170, FR 113,418, NL 13,770) |
| FR: only a consumption-side series at that instant | 56,214 |
| Several series, all equal (11,387 of them all zero) | 11,404 |
| Several series, values differ: one of several generation units kept | 15,102 |
| Several series, values differ: a consumption figure kept | 6,340 |
| Several series, values differ: a generation figure kept while consumption or other units differ | 3,194 |

Generation against consumption for one generation unit:
- FR sends `outBiddingZone` series for 79 of its 110 plants, across B01, B04, B05, B06, B10, B11, B12, B14, B18 and B20.
- In the pivot by nested unit, no generation unit ever has both sides at the same instant (0 of 309,724 points). Each unit's step is one side or the other: 199,723 generation points and 72,917 consumption points in FR.
- So for a single-unit FR plant the value is unambiguous, but its sign and meaning are lost. Unlike 13a, generation is never overwritten by the same unit's consumption. The overwrite is across units of the same plant.

Worked example, 2026-09-18 18:00 UTC. These are the page's eight rows plus the raw series:
- Grand Maison `17W100P100P02756`: silver 129.77 MW, which is GRAND MAISON 9. Six of its 12 units generated a total of 772.0 MW.
- Cheylas `17W100P100P0273A`: silver 0.11 MW, which is CHEYLAS 1 on the consumption side. CHEYLAS 2 generated 228.64 MW.
- Montezic: silver 199.84 MW against a two-unit total of 399.73 MW.
- Revin: 172.22 MW against 551.96 MW.
- Coo II `22WCOOXII000070C`: 212.3 MW against 635.98 MW.
- Super Bissorte: 0.17 MW, a consumption figure.
- Coo I (154.94 MW) and Plate-Taille (34.565 MW) are right: one running unit and a single-unit plant.

## Chart

- Line chart of three NL single-unit plants, 14 to 20 September 2026 UTC, hourly, one line each, nothing summed:
  - Borssele `49W000000000054X` (B14);
  - Maasvlakte `49W000000000102B` (B05);
  - Claus `49W000000000069K` (B04).
- Why these three: each sends exactly one nested generation unit and never a consumption series, and every one of their rows is in the clean class (456, 404 and 404 rows). The window has all 24 hours for all three; 11 and 12 September and the last two hours of 10 and 21 September are missing for Maasvlakte and Claus. `aggregation: mean` with no bucket equals the value as sent, because there is one row per plant and hour.
- Paint: nuclear petrol and gas clay (defaults); coal takes an explicit `olive`.
- Key labels use the A95 plant names (installed_capacity_units shows the same names). The notes give the nested unit names from bronze.
- Series ranges: nuclear 468.863 to 475.221 MW, coal 197.25 to 1,041.25 MW, gas 130.28 to 1,151.62 MW. The alt text is checked against the committed series.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| A73, process type A16, `in_Domain` | `endpoints.py:107-112`; bronze `request_url` |
| Six zones; GB, DE-LU, IE-SEM no-data acknowledgements (`what_it_is`) | `client.py:249-262` `DEFAULT_ZONES`; bronze Ack 999 text "ACTUAL_GENERATION_OUTPUT_PER_UNIT_R3 [16.1.A]" on all 19 days |
| Summary "for Belgium, France and the Netherlands" | bronze: only those three zones return data |
| Cadence "15-minute FR; hourly BE and most NL plants" (as sent) | bronze `<resolution>`: FR PT15M, BE PT60M, NL PT60M except Maasstroom PT15M |
| Grain: plant EIC, not generation unit | `parsers.py:345-352`; bronze nesting; A95 silver names the outer EIC as the plant |
| "a plant with several units keeps one unit's figure" | dedup `actual_generation_units.py:69-72`; the reproduction above |
| "FR's consumption series land in `generation_mw` unmarked" | `parsers.py:289-297`; FR bronze has 60 `outBiddingZone` series on 2026-09-15; silver has no side column |
| `timestamp_utc` = start + (position - 1) x resolution | `parsers.py:530`, `582` (ruling #39) |
| "points repeat until the next declared one" | `curveType` A03 on every series; `parsers.py:533-601`. Example: Claus has 20 declared points on the 19th and 24 silver rows |
| `area_code` from either domain tag | `parsers.py:289-297` |
| `unit_name` empty: the parser skips nested names | `parsers.py:345-348`, `353-354`; 0 of 339,674 rows carry a name |
| `published_at` = `createdDateTime`, fetch-time | `_published_at.py`; 2026-09-18 FR created 18:24:24Z, fetched 18:24:24.48Z; BE 18:24:25Z and 18:24:25.94Z |
| B10 = hydro pumped storage | entsoe-codes.md §6 (as cited in the actual_generation note) |
| Request URL | bronze meta `request_url`, 2026-09-18 NL, key redacted |
| Ingest end exclusive, transform end inclusive, no offsets | `client.py:160-168` `day_subwindows`; `EVENT_WINDOW_FILTER = True`; 0 out-of-window rows; same pattern as the approved actual_generation page |
| Notebook lead | `research/handles/source.py:401-448`: relation from `_relation_name_for_dataset`, inclusive date predicate, bitemporal columns excluded, `ORDER BY timestamp_utc` only |
| Related: installed_capacity_units uses the same plant EIC | A71 silver holds all three chart EICs (Claus 1,304 MW, Maasvlakte 1,070 MW, Borssele 30 485 MW), and 162 of 175 plant EICs |
| Related: generation_units_master_data names the plant EIC | A95 silver: `49W000000000069K` "Claus" and others |
| Related: elexon/pn | Elexon PN is GB per-BM-unit notified output; GB sends nothing here |

## Body corrections (canonical note)

1. Live verification: added a bullet recording the bronze days that return data (FR, BE, NL) and Ack 999 (GB, DE-LU, IE-SEM), with the fetch dates.
2. Bronze: "one `<TimeSeries>` per generation unit" now reads per generation unit and side, with the plant in `registeredResource.mRID`, the unit in `PowerSystemResources`, and every series `businessType` A01 and `curveType` A03. It adds that FR sends `outBiddingZone` series and BE and NL do not. The A75 consumption-side meaning is cited through the actual_generation note, and I say that no A73 vendor text was found.
3. Dedup key: added the citation and "plant EIC, no unit, no side".
4. Point-in-time field: "`ingested_at` (optional)" now reads "none in effect; `published_at` is a fetch-time stamp", with the timing evidence.
5. Schema table:
   - `timestamp_utc`: "position * resolution" now reads "(position - 1)" (`parsers.py:530`), with a note on A03 repeating.
   - `area_code`: both domain tags.
   - `unit_mrid`: plant EIC; the nested unit is not read.
   - `unit_name`: always "" and why.
   - `generation_mw`: last series read.
   - `resolution`: as sent, replacing "typical PT60M".
   - Added the missing `published_at` row.
   - `ingested_at`: stamped at transform time (`74-79`).
6. Silver sample: replaced a fabricated GB row (`48WSTN0000ABRBON`, "ABRBO", resolution "1:00:00"; GB returns no data) with a real silver row: NL Borssele, 2026-09-18 18:00Z, 470.65525 MW.
7. Known issues: added the defect bullet with the reproduction numbers and the worked example, plus a `unit_name` bullet.

## Unverified

- No ENTSO-E text defines `outBiddingZone_Domain` for A73. The consumption reading rests on the A75 Postman citation in the actual_generation note, plus the values: B10 up to 237 MW, pumping scale, and B14 up to 94 MW, auxiliary scale. The page says "consumption series", as the approved 13a page does for A75.
- No vendor text found that `registeredResource` = production unit and `PowerSystemResources` = generation unit for A73. The evidence is structural: bronze nesting, A95 (B11 production-unit register) and A71 listing the outer EIC with the plant name.
- The note's "Historical depth 2014-12-05" and "Publication lag T+~1h" were not checked. They are not on the page.

## Open questions for the seat

- Hold or ship? The chart, the eight rows and the words are sound: the chart uses only clean plants, and the frame is honest about the collision. But 40% of silver rows are not a single generation-unit value, so a user cannot trust arbitrary rows. The page states this plainly, as the 13a page did. I recommend shipping it with the defect logged.
- `how_used` has two entries. A third use (FR reactor-by-reactor output) would need a caveat that an idle reactor shows its consumption, so I left it out.

## Template problems

None new. The notebook filename clip at 390 is the known seat item.

## Defects (pasteable: gridflow BACKLOG and the vault remediation page)

**entsoe/actual_generation_units: one row per plant, not per generation unit, and no side (found 2026-09-29, p26 page author).**
A73 sends one `<TimeSeries>` per generation unit and side. The plant EIC is in `registeredResource.mRID`; the generation unit's EIC and name are in `MktPSRType/PowerSystemResources`.

What the code does:
- The parser reads only `psrType` from `MktPSRType` (`connectors/entsoe/parsers.py:345-348`), so the unit EIC and name are dropped.
- It reads `outBiddingZone_Domain.mRID` into the same `in_domain` as generation (`parsers.py:289-297`).
- The transformer dedups on `(timestamp_utc, area_code, unit_mrid)` keep-last (`silver/entsoe/actual_generation_units.py:69-72`).

The result is one row per plant and instant: whichever series was read last, with nothing recording which.

Reproduction: re-parsing all 19 bronze days with the gridflow parser and the transformer's dedup matches silver exactly (229,612 rows, 0 value mismatches). Of those rows:
- 137,358 are clean (the plant's only series);
- 56,214 (FR) are a consumption figure with no generation series at that instant;
- 15,102 are one of several generation units' differing figures;
- 6,340 (FR) are one unit's consumption figure while other series differ;
- 3,194 (FR) are generation kept while other series, some of them consumption, differ;
- 11,404 had several equal series (11,387 zero).

In total, 80,112 series points are dropped.

Scope:
- 30 plants send several generation units: BE 8, FR 17 (Grand Maison 12), NL 5.
- 79 of FR's 110 plants send consumption series. BE and NL send none.

Example, 2026-09-18 18:00Z:
- Grand Maison `17W100P100P02756`: silver 129.77 MW, while six of its twelve units generated 772.0 MW.
- Cheylas `17W100P100P0273A`: silver 0.11 MW (CHEYLAS 1 consumption), while CHEYLAS 2 generated 228.64 MW.

Fix: read the nested generation unit EIC and name, add them and the side (or a signed value) to the schema and the dedup key. This is the same fix class as BACKLOG 13a (`actual_generation`).

**entsoe/actual_generation_units: `unit_name` always empty (found 2026-09-29).**
The parser reads `registeredResource.name` (`parsers.py:353-354`), which A73 responses never carry: 0 of 339,674 parsed rows have one. The names are in `MktPSRType/PowerSystemResources/name` (for example "GRAND MAISON 9"). The fix is part of the item above. Plant names are available from `generation_units_master_data`.

**Vault note (fixed in this branch):** the silver sample was a fabricated GB row (`unit_name` "ABRBO", resolution "1:00:00"), but GB returns Ack 999. It is replaced with a real NL row.
