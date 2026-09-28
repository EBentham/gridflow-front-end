claude-opus-5-5

# Schema designer 4, "One record, then many"

Boards (1440 wide, root height = `$preview`), in `p24\r2-schema\4\`:
- `4-fuelhh.dc.html` 1281 px
- `4-system-prices.dc.html` 1459 px
- `4-physical-flows.dc.html` 1391 px
- `4-bmunits-reference.dc.html` 1373 px

Source: `gen4.py` + `content4.py` + `s4.css`; values from `polars_vals.py` -> `vals.json` (Polars 1.40 formatting, run with gridflow's venv). Static copies (SHARED.md sed recipe) in `static\`, captures in `shots\`.

## Idea
One real row, laid out field by field, IS the schema. The eight sample rows then hang from the same spine as a DataFrame carrying only the columns that differ, so nothing is shown twice.

## Content model (silver stratum; word budgets)
1. h2 "Schema and sample rows" + relation line (25 words or fewer; A's wording).
2. h3 "One row, field by field" + key note (A's, 10 words).
3. Record, schema order, one line per column: name (hangs left of the spine, key square on the spine), value in a daylight frame (Red Hat Mono, as Polars prints it), dtype, meaning (14 words or fewer).
4. Lineage label (16 words or fewer), then the lineage columns of the same row, framed on topsoil, each with a meaning of 14 words or fewer.
5. h3 "Eight rows" + caption (16 words or fewer, specific) + template note (17 words).
6. DataFrame, 8 rows: only schema columns whose values differ; codes in mono, names and numbers in Hanken tabular; the record's row bold with a pointer in the key-square gutter. Narrow tables (fuelhh) take the caption beside them.

Record rows chosen to exercise the hard column: fuelhh PS (-1454.0, signed); prices SP29 (-49.9); flows Bacton (IUK) exit (its double-report pair is the next row; the null is in the table); bmunits E_ABERDARE (null fuel type).

## NEW COPY (verbatim)
Template: "One row, field by field" / "Eight rows" / "Added to every row by the silver base transformer; query() leaves these out." / "Only the schema columns that differ between rows are shown. The marked row is the one above." / "Same on every row"
Lineage meanings: event_time "Event instant: the row’s time column, else the target date"; available_at "When the row became knowable: published_at, else the ingest time"; source_run_id "Id of the pipeline run that wrote the row"; dataset_version "Transformer version stamped on the row"; vintage_policy "Which rule produced available_at".
Captions: fuelhh "All eight rows are settlement date 2026-09-26, period 25: 8 of its 20 codes." / prices "Settlement date 2026-09-20, periods 22 to 29, one version each." / flows "Gas day 2026-09-21 at GB points; every row starts at 04:00 UTC." / bmunits "Eight units, chosen across id prefixes."
Meanings changed from A: prices system_sell_price "SSP, GBP/MWh; can be negative"; net_imbalance_volume "NIV, MWh; signed, sign convention undocumented"; run_type "Always null: this endpoint has no such field". Flows timestamp_utc "Start of the operator’s gas day; operators start at different hours"; point_key "ENTSOG point id"; point_label "Point name"; operator_key "Reporting operator; both sides of a point report, so a flow can appear twice"; operator_label "Operator name"; flow_gwh_per_day "GWh/d, normalised from the vendor unit; a missing flow stays null"; unit "Same on every row, after normalisation"; ingested_at "When the silver transform ran; not declared in the schema class". bmunits bm_unit_id "Elexon BM unit id"; fuel_type "Vendor fuel type; null for most units"; gsp_group_id "GSP group; nullable"; national_grid_bm_unit "National Grid unit id; not an ENTSO-E EIC". Every data_provider: "Same on every row". All other meanings are A's.

## Verification
- detect.mjs --json on the four sed copies: `[]` each.
- Measured in my own tab (port 9746) with fonts loaded at 1440: root height = `$preview`; content ends 72 px above the silver/gold contact; 0 overlapping text boxes; nothing outside x 80..1360 except the strata and cable layers; no clipped cells; every table fits 1040 px without scrolling.
- Contrast: everything on the silver ground uses ink or `--ink-2`; `--muted` only for null inside daylight frames.

## Could not do / open
- The shared browser pane rendered at quarter scale, so visual checks used headless Edge captures (`shots\`).
- "equal to SSP on every row" (A's wording) is a measured claim across the fetched history; keep or soften at review.
- Reflow to 390 px: a `@media (max-width: 760px)` block stacks each record line (name and dtype, then value, then meaning) and the table scrolls in its own container. It is not verified at 390.
