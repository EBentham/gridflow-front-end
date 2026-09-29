# uou2t14d: review 1

**Verdict: REVISE.** 0 blockers, 4 majors, 3 nits.

Checked against: `silver/elexon/uou2t14d.py`, `silver/base.py`, `silver/elexon/_publication_window.py`,
`connectors/elexon/{endpoints,client}.py`, `bronze/writer.py`, `schema_manifest.py`, `latest_views.py`,
gridflow_models `research/handles/source.py`; local silver and bronze for 2026-09-21 (read only, Polars);
`bmunits_reference` silver; the committed series, sample and notebook; the built page; the `fou2t14d` note.

## Findings

### 1. major: `page.record.key` (hero "Key") with `page.record.fields.published_at`

**What is wrong.** The page gives the key as `(settlement_date, bm_unit_id, published_at)`, the same shape the sister
page `fou2t14d` uses to mean "every publish kept". Here, gridflow declares and dedups on two columns only:
`ENTITY_KEY_COLUMNS = ("settlement_date", "bm_unit_id")` (`uou2t14d.py:26`, dedup at `:133-136`), applied to one
bronze day at a time. Nothing on the page says that `published_at` is not a dedup column: it only separates rows from
different fetched days. `what_it_is` hints at this, but the Key and the guide line for `published_at` do not.

**Keep the three columns.** A two-column key would be false for the table `query()` returns: local silver has 73,424
repeated `(settlement_date, bm_unit_id)` pairs across files and 0 repeated triples. The code makes the triple hold in
two ways:
- one silver file per bronze day, and day D's bronze holds only publishes from D 00:00 to D+1 00:00;
- the one publish two days share (the D+1 00:00 boundary) is trimmed from day D by the Elexon publication-window
  filter, which runs after `transform()` (`base.py:1638-1642`, `1786-1805`). uou2t14d is in scope: it is not in
  `PUBLICATION_WINDOW_EXEMPT` and uses the default `publishDateTimeFrom/To` parameters (`_publication_window.py:94-117`).

The writer's report says "nothing enforces that". That is incomplete: the filter covers the boundary case whenever day
D+1's bronze proves it owns that publish.

**Fix.** Add the disclosure to the `published_at` field line, within 14 words. For example: "Publish time, from the
vendor `publishTime`, UTC; separates fetched days, not in gridflow's dedup key".

### 2. major: `page.facts.grain`, `page.what_it_is`, `page.raw_feed.note`, `page.record.fields.bm_unit_id`

**What is wrong.** Three fields make a claim that is false for units sent without an Elexon id:
- `facts.grain`: "One row per delivery date and BM unit per fetched day";
- `what_it_is`: "Silver keeps one row per unit and date from each fetched day", right after "per National Grid BM
  unit";
- `raw_feed.note`: "keeps one row per unit and delivery date from each fetched day".

Units sent without `bmUnit` all share a null dedup key. Polars `unique` treats nulls as equal, so one survives per date
and fetched day, and the rest are dropped (`uou2t14d.py:133-136`). The only disclosure is the `bm_unit_id` line, "one
kept per date". It doesn't say the others are dropped, and it should say "per date and fetched day".

**Evidence.**
- Bronze 2026-09-21, 20:00 UTC publish: each forecast date has 555 National Grid units (1,110 rows, sent twice by the
  overlapping windows), 162 of those rows with a null `bmUnit`, so 81 null-id units.
- Silver `uou2t14d_20260921.parquet`: 475 rows per date, and exactly one null `bm_unit_id` per date. It is `WTGRW-1`
  for all 14 dates, and its value (10.0 on 30 September) is WTGRW-1's own.

**Fix.** Add one clause to `what_it_is`: units sent without an Elexon id share one null key, so only one of them
survives per date and fetched day. Tighten the `bm_unit_id` line to match, and scope the grain and `raw_feed.note` the
same way (or point to the caveat). Put no counts on the page: 81 and 555 are from our copy and belong in the body,
which already has them.

**Checked and correct.** The frame's row 8 (`null`, `"WTGRW-1"`, 10.0) is real. The chart filters on three non-null
ids and the notebook prints no counts, so no count or chart on the page includes the null row.

### 3. major: `page.notebook.cells[0]`, `page.notebook.lead`, `page.notebook.needs`

**What is wrong.** The page's own commands do not reliably produce the page's own notebook. The first cell hard-codes
`df.published_at == "2026-09-21 20:00:00+00:00"`, but the publish silver keeps is set by bronze file order:
- bronze files are named `raw_<fetch second>_<body sha256[:8]>` (`bronze/writer.py:31-32,57`);
- the six 4-hour chunks are fetched concurrently (`client.py:94-105`, `asyncio.gather`);
- the survivor is the last row of the last-sorted file (`uou2t14d.py:40,136`).

Local silver shows the kept publish changing by fetched day: 16:00 (13 Sep), 08:00 (14 Sep), 20:00 (15, 16, 19, 20,
21 Sep), 12:00 (17, 18 Sep). A reader whose 20:00 to 24:00 file does not sort last gets an empty `pub`, an empty
pivot, and an error from `.plot()`.

**Fix (noted or fixed, the writer's choice).** Select by publish date instead of hour:
`pub = df[df.published_at.dt.strftime("%Y-%m-%d") == "2026-09-21"]`. Checked on local silver for delivery dates
23 September to 5 October: 6,175 rows, one publish (20:00), 0 repeated `(settlement_date, bm_unit_id)`. This works
because the 23:00 publish adds only 6 October, outside the window, and the boundary publish is dated the 22nd. Then
reword the lead ("the publish kept from the 21 September fetch") and `plot_alt`, and rerun the notebook.

### 4. major: `page.notebook.cells[2]` (plot) and `page.notebook.plot_alt`

**What is wrong.** The plot hides Heysham's zero run. pandas `pivot` orders the columns alphabetically, so `T_HEYM11`
is drawn first and `T_PEHE-1` (orange) is drawn over it at 0 from 23 to 29 September. `uou2t14d-5.png` shows no petrol
line before the 30th, only orange at zero. `plot_alt` says "T_HEYM11 is 0, then steps...", which the image does not
show, and neither the alt nor the lead mentions the overlap. Around 30 September, `T_HEYM11` (262) and `T_SGRWO-6`
(256) also nearly coincide in two close teals.

**Fix.** Any one of these:
- draw Heysham last: `wide[["T_PEHE-1", "T_SGRWO-6", "T_HEYM11"]]`, with the colour list reordered to match;
- give the lines distinct styles, for example `style=["-", "--", "-"]`;
- say in `plot_alt` that its zero run lies under `T_PEHE-1`.

**Checked and acceptable.** The site chart has the mirror overlap (Peterhead's zero run under Heysham), but both key
notes state the zero in words.

### 5. nit: vault body, "Dedup key" and "Known issues"

The corrected paragraph explains the file-order survivor but leaves out the second mechanism: the publication-window
filter (`base.py:1638-1642`, `1761-1805`) can drop a surviving D+1 00:00 publish from day D after the dedup. Add one
sentence citing it.

### 6. nit: vault body, API table "Publication lag"

The cell says bronze for 2026-09-21 "holds a publish every hour, 00:00 to 23:00 UTC". The 20:00 to 24:00 window also
returns the 22 September 00:00 publish: the first `publishTime` in `raw_20260926T183410Z_59ab15a1.json` is
`2026-09-22T00:00:00Z`, so windows include both ends. Say so, or write "00:00 to 23:00, plus 00:00 on the 22nd".

### 7. nit: `page.record.fields.settlement_date`

"Delivery date forecast, from the vendor `forecastDate`" reads as a forecast of a date. The sister page says "Delivery
date the forecast is for, from the vendor `forecastDate`". Align the wording. Do not copy the sister's "a London date"
unless its checker confirms it.

## Checked and correct

**Chart provenance.** The committed series has `spec_origin: vault`, a spec digest that matches (build green),
`rows_matched: 39` (3 units by 13 dates), `aggregation: last`, and one row per unit and date after the publish filter,
so nothing is summed. No staged spec or authored override exists. Values match silver and bronze exactly:
- Peterhead (`T_PEHE-1`): 0 from 23 to 29 September, then 1,180;
- Heysham (`T_HEYM11`): 0 to the 29th, then 262, 360, 476, and 498 from 3 October;
- Seagreen 6 (`T_SGRWO-6`): 89, 299, 135, 195, 228, 194, 277, 256, 178, 165, 162, 172, 172.

The alt text, key notes, caption and title match these values.

**Names and paints.** Unit names match the `bmunits_reference` register ("Peterhead Block 1", "Heysham 1 Generator 1",
"Seagreen1 Offshore WF 6", shortened to "Seagreen 6" as on the approved `pn` page). Fuel types are CCGT, NUCLEAR and
WIND. Paints are clay, petrol and horizon, which are the gas, nuclear and wind roles (`page_fields.py:187-195`); no
khaki. The notebook's hex colours map to the same units.

**Raw feed and commands.**
- The request URL matches the bronze meta `request_url`.
- The ingest `--start 2026-09-21 --end 2026-09-22` makes six 4-hour windows (`client.py:94-98`,
  `max_chunk_hours=4`), all written to bronze day 21; there are exactly six files.
- The transform `--start/--end 2026-09-21` is inclusive, and `PARTITION_SOURCE_OFFSETS` is the default `(0,)`.

**Notebook lead.** It matches the code: relation `silver_elexon_uou2t14d`, date column `settlement_date`
(`schema_manifest.py:143`), no `_latest` view (`latest_views.py` registers `fou2t14d` only), both ends inclusive,
lineage columns excluded, and the result returned as pandas (`source.py:401-451`).

**Field guide.** The lines for `timestamp_utc` (`uou2t14d.py:125-131`), `output_usable_mw`, `national_grid_bm_unit`
(the `T_` prefix is quoted from the vendor) and `fuel_type` are correct.

**Local data and wording.** The page block and the rendered page have no local-data references (grep hits were only
"delivery" and the vendor's "planned outages"). No planning labels, no em dashes, no middle dots. Related notes are 12
words or fewer.

**Build and detector.** `gridflow-build --only elexon/uou2t14d` is green, and `detect.mjs --json` returns `[]`. The
mirror is byte-identical to the vault note.

**Samples and notebook artefacts.** The sample has `generated_by: gridflow-sample` and 8 real rows. The notebook
artefact was made by `scripts/run_notebooks.py`: read-only calls, no errors, and the outputs match silver.

**Vault body edits.** The Overview, Dedup key, point-in-time field, schema rows, sample and Known issues edits are each
backed by code or bronze, apart from nits 5 and 6.

**Rendering.** Screenshots at 1440, 1024, 768 and 390 (390 in a 390 px iframe) show nothing clipped or overlapping:
- the hero scenery, the stratum corner labels, the chart and its key, the frame folded and unfolded (13 columns in a
  horizontal scroll box), the guide, the inline notebook with the plot, and related datasets;
- at 390 the hero shows only the scene's right half, which the shared template does, not this page's content.

The site has no dark scheme (no `prefers-color-scheme` or `data-theme` in `site/hifi/assets/`), so light and dark are
the same.

**Consistency with `fou2t14d`.** Shared terms match: "delivery date", "publish", "Output Usable", the MW line, the
`timestamp_utc` line, and related notes that mirror each other. Two differences are justified by the code: 4-hour
windows here against 24-hour windows there, and no latest view here. Nit 7 is the only wording gap.
