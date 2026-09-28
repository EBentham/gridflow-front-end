# netbsad: author report

Writer for `elexon/netbsad` (Net balancing services adjustment data), 2026-09-29.

## Status

- `page:` block written in the canonical note
  (`vault-p26-elexon/30-vendors/elexon/datasets/netbsad.md`). Mirror copied byte for byte to
  `p26-elexon/vault/elexon/netbsad.md` (`cmp` clean). Both files are LF. The batch file says CRLF, but
  the note, the mirror and the main-repo mirror all have 0 CRLF lines, and `.gitattributes` sets
  `*.md eol=lf`. Before my first copy the worktree mirror differed at byte 4; the copy replaced it.
- No staged spec and no authored override existed for netbsad, so nothing was deleted.
- Artefacts: `site/hifi/data/series/elexon/netbsad.json` (gridflow-distil, `spec_origin: vault`,
  1 series, 336 points, 7 duplicates dropped), `samples/elexon/netbsad.json` (gridflow-sample,
  8 rows, 17 columns), `notebooks/elexon/netbsad.json` plus `netbsad-6.png`
  (`scripts/run_notebooks.py`, 6 cells, no errors).
- `gridflow-build --only elexon/netbsad` renders the page. The final run printed "3 error(s) on
  pages not rendered by --only"; those are other writers' pages. `detect.mjs --json` returns `[]`.
- Screenshots were taken at 1440, 1024 and 768 (headless Chrome, port 9733, server stopped) and at
  390 (a 390 px iframe), plus the frame unfolded at 1440 and 768. The site has no dark theme: nothing
  in the CSS, templates or DESIGN.md uses `prefers-color-scheme` or `data-theme`, so the dark captures
  are identical to the light ones. Scratch copies are in `scratchpad/netbsad/shots/`.

## The one thing to look at hardest: every value is 0

Every NETBSAD value on disk is `0.00`, in all eight terms and every period, in both bronze and
silver (686 bronze records, 2026-08-01 to 2026-09-22). The vendor sends these zeros: the raw bronze
JSON reads `"buyPricePriceAdjustment":0.00` and so on, so this is not a rename or parse fault. The
chart is a line of `buy_price_price_adjustment` that is flat at 0. The caption, the key note, the
alt text, the record caption and a notebook cell (`(df.filter(like="adjustment") != 0).sum()`,
all 0) all say so, each scoped to "this window" or "here". None of them gives a cause.

**Template problem (not worked around):** the chart renderer gives a constant-zero series a y-axis of
0 to 1.0 and draws the line exactly on the x-axis, where the axis hides it (a zoomed crop at 1440
shows no visible petrol line). The chart therefore looks empty apart from the axes. There is no NaN
and the SVG is valid; the path sits at y=410, the baseline. Possible fixes are seat work: pad a
constant series' domain symmetrically (for example -1 to 1), or draw the series after the axis.
The alternative I rejected is `chart: {type: none}`, which removes the figure, its caption and its
key entirely (build.py:1723 and the `v.chart` gate in the template). A reviewer may raise the hidden
line under rubric 5 ("overlapping"). It is a renderer behaviour, not a label of mine.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| One row per settlement period (`facts.grain`, `record.key`) | `silver/elexon/netbsad.py:136` `unique(subset=["settlement_date","settlement_period"], keep="last")`; `ENTITY_KEY_COLUMNS` at `:26-29` |
| Half-hourly, by settlement period (`facts.cadence`) | `schemas/elexon.py:820` `settlement_period: int = Field(ge=1, le=50)`; the rows are one per period |
| Eight terms: per side one net cost (energy), two net volume (energy, system), one price adjustment (`summary`, `what_it_is`, `record.fields`) | `netbsad.py:77-86` rename map; silver schema holds exactly those 8 (Polars `read_parquet` schema) |
| BPA is added to the system buy price when short, SPA to the sell price when long; BPA is in £/MWh (`what_it_is`, `fields`, `related`) | Elexon *Imbalance Pricing Guidance* v15.0 (25 June 2020) p.11: "The BPA is added when the net imbalance of the Transmission System is short. The SPA is added when ... long"; p.29 worked example "System Buy Price = 30 + 6.50 = £36.50/MWh". Quoted in the note body under "Vendor documentation" |
| Net imbalance decides which applies (`related` system_prices note) | Same guidance p.29: "BPA is used when ... short (and the NIV is positive), and the SPA ... long (and the NIV is negative)"; `system_prices` has `net_imbalance_volume` |
| Sent by the system operator (`summary`) | Elexon glossary (BPA, EBVA): "The amount sent by the Transmission Company ..."; guidance p.11 "The SO submits ..." |
| DISBSAD lists the individual actions (`what_it_is`, `related`) | Guidance p.11 and p.28: BSAD is split into "Balancing Services Adjustment Actions" ("disaggregated BSAD") and BPA/SPA; the SO submits "an individual Balancing Services Adjustment Action" per service |
| Request URL (`raw_feed.requests`) | `connectors/elexon/endpoints.py` `netbsad` (`/datasets/NETBSAD`, `from`/`to`); `build_params` + `_to_utc_z` give `...T00:00:00Z`; `page` is added (`supports_pagination`). Matches the bronze sidecar `request_params` `{"from":"2026-09-20T00:00:00Z","to":"2026-09-21T00:00:00Z","page":1}` |
| 24-hour windows from midnight UTC (`raw_feed.note`) | `client.py` PUBLISH_DATETIME loop, `max_chunk_hours=24`; `runner.resolve_dates` gives a bare date as midnight UTC |
| Replies here also carry the half-hour starting at `to`, so silver repeats it (`raw_feed.note`, `notebook.lead`) | Each of the 14 silver partitions has 49 rows running from D 00:00Z to D+1 00:00Z; 12 key duplicates across partitions; distil dropped 7 in the window. Scoped as "here" because the vendor semantics of `from`/`to` are undocumented (`_publication_window.py:61-64`) |
| Ingest `--start 2026-09-14 --end 2026-09-22`, the end is exclusive | `client.py` `while current < end`; the last chunk is 21 Sep 00:00Z to 22 Sep 00:00Z |
| Transform `--start 2026-09-14 --end 2026-09-21`, starting early | `runner.run_transform` `date_range(start, end)` is inclusive; silver day D reads bronze day D only (`netbsad.py:31-37`); settlement date 15 Sep periods 1 and 2 (14 Sep 23:00Z and 23:30Z) live in partition 14 |
| x_label "each starts at 23:00 UTC" | BST window; series `x[0]` = `2026-09-14T23:00:00Z` |
| Chart: 336 points, all 0 (caption, alt, key note) | series JSON: 1 series, 336 values, min 0.0, max 0.0, x from 2026-09-14T23:00Z to 2026-09-21T22:30Z |
| "as are the other seven terms" / "the SPA and the six cost and volume terms" | Polars over silver, settlement dates 15 to 21, all 8 columns: `(col != 0).sum() == 0`; the notebook cell output shows 0 for each |
| Record: 2026-09-21 periods 33 to 40, all eight terms 0 | sample JSON, 8 rows; dedup applied |
| `notebook.lead`: relation `silver_elexon_netbsad`, filter on `settlement_date` inclusive, lineage dropped | gridflow_models `_RELATION_NAME_BY_DATASET["netbsad"] == "silver_elexon_netbsad"` (no `_latest`); `schema_manifest.py:134` date column; `source.py:401-451` (`_date_range_predicate`, `_present_bitemporal_exclude_clause`, `ORDER BY settlement_date`) |
| `notebook.needs` 14 to 21 September matches the commands | the ingest/transform windows above |
| `timestamp_utc` from settlement date and period | `netbsad.py:125-134` `settlement_period_to_utc` |

## Note-body corrections (smallest spans)

1. Overview: removed "NETBSAD is computed from the disaggregated DISBSAD components." It had no
   citation. Replaced it with the vendor's two-part description of BSAD, and added a "Vendor
   documentation (quoted 2026-09-29)" subsection with the guidance and glossary quotes and their URLs.
2. Silver schema intro: "emits both ... exactly one set is populated per row" is wrong. `netbsad.py:167`
   keeps only the columns present, so silver from current bronze has the 8 and no legacy columns
   (they are absent, not null).
3. `ingested_at`: was "Time ingested into bronze". It is the silver transform time
   (`netbsad.py:138-142`).
4. Silver sample: replaced with a real row (2026-09-21 period 33). The old sample showed the legacy
   columns and gave `timestamp_utc` 04:00Z for 6 May period 9; in BST that period starts at 03:00Z.
5. Known issues: replaced "Computed from DISBSAD" with three notes: (a) the vendor does not say
   NETBSAD sums DISBSAD; (b) the 00:00 UTC half-hour repeats across partitions and nothing trims it
   (`PUBLICATION_WINDOW_EXEMPT`); (c) all terms are zero in every captured record, and in the same
   periods silver `disbsad` has non-zero action volumes (see below).

Left alone and flagged for the seat: the V2-FIX changelog describes the 8 columns as "cost vs volume
x energy vs system x buy vs sell", which does not match the actual set (it is a history entry that
quotes a code comment at `netbsad.py:61-64`). Also left: the bronze path pattern `raw_<uuid>.json`
(files on disk are `raw_<UTC stamp>_<hash>.json`) and "Publication lag: Same cadence as system
prices" (unverified).

## The DISBSAD disagreement (coordinator heads-up, reproduced)

Polars, both silver tables deduped on their keys and joined on settlement date and period: 674
shared periods. DISBSAD summed per period, component and `so_flag` gives Energy (so_flag false)
-450 to 772.85 MWh, non-zero in 167 groups; System (so_flag true) -600 to 750 MWh, non-zero in 229;
plus small Non-BM LCM, PQR and PSR. NETBSAD is 0 in every term for all of those periods (for
example 2026-09-16 period 39: DISBSAD Energy cost 179,218.06; NETBSAD `net_buy_price_*` 0.0). The
page makes no relation claim beyond the vendor's "DISBSAD lists the individual actions" and gives
no cause. The note body records the observation, dated. The glossary formula for EBVA, "aggregated
volume of relevant Balancing Services purchased for energy balancing less sold", makes the
disagreement worth a research unit.

## Not verified

- Units of the six net cost and volume terms, and their sign conventions. The vendor sources I read
  give none, so the page states no unit for them; only BPA and SPA carry £/MWh.
- What the API's `from`/`to` filter on (the code calls it undocumented). The boundary repeat is
  stated as observed here, not as a vendor rule.
- Whether NETBSAD is ever non-zero today. The page states no history.
- `dedup keep="last"` in the transformer runs over files sorted by name (`raw_<stamp>_<hash>`). If
  two captures of one day disagree, which one wins depends on the stamp. No disagreement exists in
  local data (all zeros).

## Open questions

1. Chart: keep the flat line with its caption (my choice), wait for a renderer fix to the
   constant-series axis, or rule `type: none`?
2. Should a research unit take the NETBSAD versus DISBSAD disagreement (EBVA formula against DISBSAD
   Energy volumes), and the question of whether NETBSAD's net terms have been zero for long?
3. The hero draws the `market` landscape as turbines, pylons, a substation and battery storage, the
   same drawing as the power pages. That is scenery and not mine; noted only.

## Template observations

- Constant series: the y-domain defaults to 0 to 1 and the line is hidden under the x-axis (above).
- At 390 the notebook code wraps mid-identifier (`sort_valu` / `es(`). Nothing is clipped; it is the
  template's wrapping.
- Unfolded frame: `.fw { overflow-x: auto }` scrolls horizontally by design; nothing is clipped.
