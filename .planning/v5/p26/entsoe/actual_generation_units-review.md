# entsoe/actual_generation_units: checker review

Checker: Opus 5.5, 2026-09-29. Port 9848 (servers stopped). Scripts and shots in
`scratchpad/agu-review/` (`r1.py` to `r9.py`, `shots/`).

## Verdict: REVISE

2 blockers, 0 majors, 3 nits.

The defect is real and the page's account of it is accurate. The chart is clean. The two blockers
are both about showing or recommending defect values as if they were correct.

## Findings

### 1. Blocker: `page.record.caption` (and `page.record.fields.generation_mw`): six of the eight rows are wrong values, unlabelled

**What is wrong.** The frame shows the nine B10 plants at 18:00 UTC on 18 September, minus Coche.
The caption only says "Eight of the nine pumped-storage plants at 18:00 UTC on 18 September 2026."
A reader sees each row as that plant's output. Six of the eight are not the plant's output:

| Plant | Row | What the row actually is |
|---|---|---|
| Grand Maison `17W100P100P02756` | 129.77 | GRAND MAISON 9 only; six units made 772.0 MW |
| Cheylas `17W100P100P0273A` | 0.11 | CHEYLAS 1 consumption; CHEYLAS 2 generated 228.64 MW |
| Super Bissorte `17W100P100P02764` | 0.17 | SUPER BISSORTE 2 consumption; unit 4 generated 0.06 MW |
| Montezic `17W100P100P02772` | 199.84 | one of two running units; 399.73 MW in total |
| Revin `17W100P100P02780` | 172.22 | one of three running units; 551.96 MW in total |
| Coo II `22WCOOXII000070C` | 212.3 | one of three running units; 635.98 MW in total |

Coo I (154.94, the only running unit of three) and Plate-Taille (34.565, a single unit) do equal the
plant's output.

The only hint is the `generation_mw` guide line, "last series read for the plant; may be
consumption". That is a column caveat. It does not tell the reader that these rows are wrong.
The `actual_generation` precedent labelled its defect rows in the guide ("B10 here is pumping
load"). The seat's rule for this page is that defect examples must be labelled as such.

**Evidence.**
- `r4.py`: bronze parsed with `parse_timeseries_xml(value_tag="quantity")`, with each series'
  `MktPSRType/PowerSystemResources/{mRID,name}` and its in/out domain tag attached through the
  series `mRID`. The table above is filtered to `production_type == "B10"` at 2026-09-18 18:00Z,
  with in-side values summed per plant.
- Silver shows the same eight values (`r1.py`).

**Fix.** Either option works:
- Keep these rows (they show the defect well) and label them. For example, set `record.caption`
  (16-word budget) to "Pumped storage, 18:00 UTC 18 September 2026: six of these rows are not the
  plant's output." Then make the `generation_mw` line name one case, for example "here Grand
  Maison's 129.77 is one of six running units".
- Or choose eight clean rows (NL or BE single-unit plants) and keep the defect in the prose.

### 2. Blocker: `page.how_used[0]` and `page.how_used[1]`: "single-unit plants" is not a safe filter, and silver cannot pick those plants out

**What is wrong.** Both uses tell the reader that single-unit plants are sound: "Hourly dispatch of
single-unit plants" and "Load factors for single-unit plants". That holds in BE and NL, but not in
France:
- 65 of France's 93 single-unit plants also send consumption series.
- All 56,214 "only a consumption series" rows belong to single-unit FR plants. They include B14
  nuclear rows up to 94.39 MW and B20 rows up to 241.5 MW. A load factor built on those plants
  would count idle-time consumption as output.

Silver also cannot tell the reader which plants have one unit, because the nested unit EIC is
dropped. `generation_units_master_data` does not list the nested units either (author report).

**Evidence.** `r7.py`: group the parsed points by (zone, plant) and count distinct nested units.

| Zone | Single-unit plants | With consumption series |
|---|---|---|
| BE | 24 | 0 |
| FR | 93 | 65 |
| NL | 28 | 0 |

- Single-unit rows by class: FR has 113,418 clean rows and 56,214 consumption-only rows. BE and NL
  single-unit rows are all clean.
- Maxima of the kept consumption values: B14 94.39 MW, B20 241.5 MW, B04 25.85 MW.

**Fix.** Scope both uses to what is clean and identifiable. For example: "Hourly dispatch of Dutch
single-unit plants, nuclear baseload against coal and gas", with the load-factor use limited the
same way. Or tie it to the charted plants. Do not recommend French plants without the
consumption caveat.

### 3. Nit: `page.summary`: "realised output of individual power plants"

A73 is per generation unit, which is what `what_it_is` says. Silver rows are plant-keyed but are
not plant totals (finding 1), so "individual power plants" in the headline promises plant output.
"individual generating units" matches the vendor and `what_it_is`.

### 4. Nit: `page.related[1].note`: "Names each plant EIC"

`generation_units_master_data` silver names 174 of the 175 plant EICs in this table (`r9.py`). "Names
the plant EICs, which this table leaves empty" avoids the universal.

### 5. Nit: vault body, **Point-in-time field**: "within about a second of gridflow's request"

Across all 60 data files, `createdDateTime` falls between 11.7 s before and 0.2 s after the bronze
`fetched_at` (`r8.py`). The page's "within seconds" is right; the body should say the same.

## Checked and correct

- **Six-way breakdown, reproduced exactly** (`r2.py`, `r3.py`). I parsed the 126 bronze files
  myself and applied the transformer's keep-last dedup on
  `(timestamp_utc, in_domain, unit_mrid)`:
  - The result matches silver: 229,612 rows, 0 extra, 0 missing, 0 value mismatches.
  - Points: 339,674 parsed, 29,950 duplicate-fetch points, 309,724 distinct series points, 80,112
    dropped by the plant key.
  - Classes: clean 137,358 (BE 10,170, FR 113,418, NL 13,770), FR consumption only 56,214, several
    equal 11,404 (11,387 all zero), one of several generation units 15,102, consumption kept
    6,340, generation kept with consumption present 3,194.
  - Structure: 30 multi-unit plants (BE 8, FR 17, NL 5); 79 of 110 FR plants send consumption
    series; no nested unit appears under two plants; no unit sends both sides at one instant.
- **18 September example.** Grand Maison silver 129.77 = GRAND MAISON 9, six units sum to 772.0.
  Cheylas 0.11 = CHEYLAS 1 on the `outBiddingZone` side, CHEYLAS 2 made 228.64. Montezic, Revin,
  Coo II, Super Bissorte, Coo I and Plate-Taille are also as the author states.
- **Defect statement** (`what_it_is`, `grain`, `unit_mrid`, `area_code` and `generation_mw`
  lines). It is accurate and plain, with the same register as the approved `actual_generation`
  page: a multi-unit plant keeps one unit's figure, and FR consumption lands in `generation_mw`
  unmarked.
- **Chart plants.** Borssele `49W000000000054X`, Maasvlakte `49W000000000102B` and Claus
  `49W000000000069K` each send exactly one nested unit (Borssele 30, Maasvlakte 3, Claus C), always
  on the `inBiddingZone` side, across all 19 days held (456, 404 and 404 rows, all in the clean
  class). BE and NL send no consumption series at all. In 14 to 20 Sep each plant has 168 hourly
  rows (PT60M) and no duplicate keys. The chart has one line per plant and nothing summed.
- **Committed series against silver.** Coal and gas match exactly. Nuclear differs only by
  3-decimal rounding (max 0.0005 MW).
  - Ranges: nuclear 468.863 to 475.221, coal 197.25 to 1,041.25, gas 130.28 to 1,151.62.
  - The alt text's dips (300.5 on the 15th, 300.25 on the 17th, 197.25 on the 18th), the 896.5
    on the 19th, Claus 133.28 to 1,151.62 through the 16th, at most 393.72 on the 17th to 19th, and
    829.82 on the 20th are all as shown. `plot_alt` matches the notebook PNG.
  - `spec_origin: vault`, no staged spec, no override.
- **Wording.**
  - `timestamp_utc`: "(position minus 1)" matches `parsers.py:530` and `582`, and A03 repetition
    matches `578-601`.
  - Cadence is scoped "as sent in these responses": FR PT15M, BE PT60M, NL PT60M except Maasstroom
    PT15M.
  - `published_at` is described as a fetch-time stamp.
  - `unit_name`: 0 non-empty of 229,612 silver rows and 0 of 339,674 parsed rows. The parser reads
    `registeredResource.name` (`parsers.py:353-354`), which A73 never sends; `MktPSRType` yields only
    `psrType` (`345-348`).
  - Parser citations `289-297`, `345-354` and transformer `69-72` and `74-79` are correct.
- **Raw feed.** The request matches the bronze `request_url` (param order and `in_Domain`) and
  `endpoints.py` A73/A16. The ingest end is exclusive (`utils/time.py` `day_subwindows`, `[start,
  end)`), the transform end is inclusive, and no offsets are needed.
- **Notebook.** The lead matches `query()` (manifest relation, inclusive date predicate, bitemporal
  exclude, `ORDER BY` date column). It was written by `scripts/run_notebooks.py`, every cell is
  read-only, and there are no errors. The `.head()` rows are BE zeros (three clean, two "several
  equal" at 0).
- **Build and detector.** `gridflow-build --only entsoe/actual_generation_units` passes. The
  detector shows only the accepted EIC-dash advisory. The mirror is byte-identical to the vault
  note (`cmp`).
- **Local-data grep.** The page and the `page:` block have no "held", "locally", "our", row or day
  counts, em dashes, arrows or middle dots.
- **Screenshots** (headless Chrome at 1440, 1024, 768, and 390 through an iframe; unfolded frame at
  1440 and 390 through a same-origin wrapper). Nothing is clipped or overlapping. The unfolded
  frame scrolls inside its own container and the page has no horizontal overflow. The notebook
  filename clip at 390 is the known seat item.
