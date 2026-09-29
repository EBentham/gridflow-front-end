# disbsad: author report

Writer, 2026-09-29. Page `elexon/disbsad` (Disaggregated balancing services adjustment data).

## Status

- `page:` block written in the canonical vault note (vault worktree
  `30-vendors/elexon/datasets/disbsad.md`), copied byte for byte to `vault/elexon/disbsad.md` (cmp identical).
  The mirror was LF before; the copy is CRLF like the vault, so the seat will see a whole-file diff on the mirror.
- Artefacts: `site/hifi/data/series/elexon/disbsad.json` (gridflow-distil, `spec_origin: vault`),
  `samples/elexon/disbsad.json` (gridflow-sample), `notebooks/elexon/disbsad.json` + `disbsad-5.png`
  (scripts/run_notebooks.py, 5 cells, no errors).
- No staged chart spec or authored override existed for disbsad: nothing to delete.
- `gridflow-build --only elexon/disbsad` succeeds; `detect.mjs --json` returns `[]`.
- Screenshots (headless Chrome, own user-data-dirs, static server on 9732, stopped): 1440, 1024, 768 direct;
  390 through a 390 px iframe. Hero scenery (turbine tops), chart, key, raw feed, frame, guide, notebook, related
  and corner labels all fully visible, nothing overlapping. The site has no dark theme (no `prefers-color-scheme`
  or dark tokens anywhere under `site/hifi/assets/`), so light is the only rendering. Only the folded frame
  was captured (headless cannot click the fold); at 1440 the fold hides only pipeline columns, at 768 and 390 it
  folds after `timestamp_utc` / `settlement_period`. The checker should look at the unfolded state.
- `facts.cadence` says "By half-hour settlement period": the time basis of the rows, not a publication
  frequency (nothing evidences how often Elexon publishes DISBSAD).

## Chart

`stacked-area` of `volume` (MWh), summed per half-hour by `component` (service), settlement dates 14 to 19
September 2026 (window 13 to 19 so period 1 of the 14th, at 23:00 UTC on the 13th, is in). Deduplicated on the
transformer key `[settlement_date, settlement_period, adjustment_action_id, component]` (6 repeats dropped).
Series: `system` (bottom, signed), `energy`, `lcm` (negative, hangs below), and `none` (the null-service zero
rows, via `group_null`). The `none` series is all zero and draws nothing; it exists so every half-hour stays on
the x axis. Without it `distil` drops null groups and `_stacked` would draw straight across the many half-hours
with no action (it does not break at time gaps). Paints are hatches: no scenery role covers these services.

Why 14 to 19: these settlement dates carry all three services. Settlement dates 20 and 21 carry only `System`
and zero rows, and the 13th starts at period 3; I did not state any reason for that on the page.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Request: `GET .../datasets/DISBSAD?from=...T00:00:00Z&to=...T00:00:00Z&page=1` (raw_feed.requests) | `connectors/elexon/endpoints.py:73-79` (PUBLISH_DATETIME, `from`/`to`); `build_params` + `_to_utc_z` (`endpoints.py` ~266-315, `%Y-%m-%dT%H:%M:%SZ`, `page`); bronze meta `2026/09/19/raw_..._8184fc11.meta.json` request_url matches the shape |
| 24-hour windows (raw_feed.note) | `max_chunk_hours=24` default (`endpoints.py` ElexonEndpoint); `client.py:93-99` chunk loop |
| Bare dates mean midnight UTC; ingest end exclusive (commands) | `pipeline/runner.py:479-501` "a bare date is midnight UTC"; `client.py:95-99` `while current < end` |
| Transform end inclusive, one bronze day per silver day, no offsets | `runner.py` `run_transform` `date_range(start.date(), end.date())`; `silver/base.py:417` `PARTITION_SOURCE_OFFSETS = (0,)`; `disbsad.py:32-56` reads bronze folder of the target date only |
| Bronze folder = chunk start date | `client.py` `_fetch_datetime_range`: `data_date = start.date()` |
| "Each reply also holds the half-hour starting at `to`, so silver repeats it on neighbouring days" (raw_feed.note, notebook.lead) | Vendor response (source level 2): bronze `2026/09/20` reply for `from=2026-09-20T00:00:00Z&to=2026-09-21T00:00:00Z` holds settlement 2026-09-21 periods 1 to 3 (period 3 starts 00:00Z on the 21st); silver file D spans `timestamp_utc` D 00:00 to D+1 00:00. Transformer dedup runs within one day's frame only (`disbsad.py:118-123`), so the key repeats across files (9 keys in September, all period 3, identical cost) |
| Transform starts a day early: dates begin 23:00 UTC (command comment, x_label) | BST: period 1 of 2026-09-14 is `timestamp_utc` 2026-09-13 23:00 (committed series `x[0]` = `2026-09-13T23:00:00Z`), and sits in bronze/silver day 13 |
| Grain / key: one row per settlement period, action id and service | `disbsad.py:118-123` `unique(subset=[settlement_date, settlement_period, adjustment_action_id, component], keep="last")`; `ENTITY_KEY_COLUMNS` + `OPTIONAL_ENTITY_KEY_COLUMNS` `disbsad.py:26-30` |
| `timestamp_utc` computed from settlement date and period | `disbsad.py:107-116` `settlement_period_to_utc` |
| `adjustment_action_id` from `id`, stored as text | `disbsad.py:71`, `:104-105` cast to Utf8; schema `ElexonDISBSAD.adjustment_action_id: str | None` |
| `so_flag` from `soFlag` | `disbsad.py:72` |
| `stor_flag` from `storFlag` (legacy `storProviderFlag`) | `disbsad.py:73-74` |
| `component` from `service` (legacy `component`) | `disbsad.py:75-76` |
| Null `component` on a period's zero row (fields, key note "No action") | Silver Sept: null-component rows are all id 1, cost 0, volume 0, `so_flag` true; 0 periods have a null row alongside another row; at most one null row per period. Scoped with "here" on the page |
| Cost in £, volume in MWh | Vault note schema table (`cost` GBP, `volume` MWh) and gotcha "Cost field unit: GBP (not GBP/MWh)". Not in gridflow code. Consistent with the frame: cost/volume on 17 Sep P42 System rows is 158 to 186 £/MWh |
| Signs not stated (cost, volume fields; system key note) | Nothing in gridflow code or the vendor text quoted in the note states a sign rule. The domain note `20-domain/instruments/bsad-disbsad.md` asserts "positive = SO paid" with no vendor citation, so not used. The vendor docs page (bmrs.elexon.co.uk/api-documentation/endpoint/datasets/DISBSAD) is JS-rendered; WebFetch returned nothing |
| Energy volumes positive with `so_flag` false "here" (key note) | Silver Sept: all 2442 `Energy` rows have volume > 0, cost > 0, `so_flag` false; series `energy` min 0.1 |
| System -100 to 750 MWh here (key note, alt) | Committed series `system` min -100.0 (2026-09-16T08:00Z), max 750.0 (2026-09-17T17:00Z) |
| Non-BM LCM negative volumes, positive costs, 5.76 MWh at most (key note, alt) | Series `lcm` min -5.76, max -0.173; silver Sept all 1279 `Non-BM LCM` rows volume < 0, cost > 0; the frame shows four |
| Energy 0.1 to 773 MWh, highest on the 14th and 16th (alt) | Series `energy` min 0.1, max 772.85 (2026-09-16T18:00Z); 765.8 on settlement date 14 |
| `Energy`, `System`, `Non-BM LCM` appear here (what_it_is) | Series keys / group_map; silver Sept `component` values |
| Elexon also sends party and asset; gridflow does not keep them (what_it_is) | Bronze records carry `partyId`, `assetId`, `isTendered`; `disbsad.py:68-79` has no mapping and `:133-147` `output_cols` excludes them |
| NETBSAD has one row per period (what_it_is) | `silver/elexon/netbsad.py:136` `unique(subset=[settlement_date, settlement_period])` |
| Notebook relation and filter (notebook.lead) | gridflow_models `research/handles/source.py:401-449`: relation from `_relation_name_for_dataset("disbsad")` = `silver_elexon_disbsad` (checked in the models venv); date column `settlement_date` (`schema_manifest.py:117`); inclusive both ends; `_BITEMPORAL_EXCLUDE` = event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year; ORDER BY date column only (cell sorts) |
| Eight rows (record) | `gridflow-sample`: 17 Sep period 42, ids 1, 2, 50 (System), 51, 52, 53, 83 (Non-BM LCM), 84 (Energy, `so_flag` false). Ids are strings; lexical order matches numeric for this set |
| Notebook `needs` 13 to 19 September | matches the transform window (the 13th holds the 14th's first two periods) |

## Note-body corrections (vault note)

1. **Dedup key**: `_inline in transformer_` replaced with the four columns, `keep="last"`, within one bronze
   day (`disbsad.py:118-123`).
2. **`stor_flag` source field**: `storProviderFlag` only; now `storFlag` (current) / `storProviderFlag`
   (legacy) (`disbsad.py:73-74`). The bronze sample in the note already shows `storFlag`.
3. **`ingested_at`**: "Time ingested into bronze" was wrong; now "when the silver transform ran,
   `datetime.now(UTC)`" (`disbsad.py:125-129`).

Left alone: the curl example (valid for the vendor), the overview prose, the "Publication lag" row, and the
NETBSAD gotcha (see open questions).

## Not verified

- Units (£, MWh) come from the vault note only; no vendor text quoted in the note states them, and the code
  does not. Consistent with the rows (£/MWh ratios around system prices).
- Meaning of `so_flag`, `stor_flag`, the service labels (`Non-BM LCM` in particular) and the cost/volume signs:
  undocumented in the sources; the page names the fields and does not explain them.
- That Elexon's `to` bound is inclusive in general: seen in the responses behind this page; the code calls the
  `from`/`to` semantics undocumented (`silver/elexon/_publication_window.py:53-56`).
- Why settlement dates 20 and 21 carry no `Energy` or `Non-BM LCM` rows in the bronze fetched 2026-09-26
  (publication lag, or no actions): unknown, not stated on the page.

## Open questions for the seat

1. **Midnight half-hour duplicated across silver days** (gridflow). Consecutive 24-hour requests both return the
   half-hour starting at the shared midnight, and the transformer dedups only within one day's frame, so
   `silver_elexon_disbsad` holds period 3 (BST) twice for every settlement date. `query()` returns both copies
   (no `_latest` view). The page dedups in the chart, the rows and the notebook, and says so. Worth a gridflow
   issue: either an exclusive `to` (end at `…T23:59:59Z` or filter on `timestamp_utc < to`), or a dedup across
   `PARTITION_SOURCE_OFFSETS`. The same shape probably affects `netbsad`, `mid` and `boal` (same bare
   `from`/`to` override).
2. **The NETBSAD gotcha in the note body** ("NETBSAD is the aggregate of DISBSAD components") is contradicted by
   local silver: `netbsad` reads 0.0 in every column on 17 Sep periods 40 to 44, while these DISBSAD actions total
   450 to 750 MWh positive volume per period. I left the body line alone (it is `netbsad` domain truth) and made
   no equality claim on the page; the `netbsad` writer should look at it.
3. The `none` key entry shows a hatch swatch for a series that draws nothing. It reads acceptably in the
   screenshots (the note says it is a zero row), but a template option to keep x points without a key entry
   would be cleaner.

## Template notes

- `_stacked` bridges time gaps rather than breaking, unlike `_lines`; any sparse stacked series needs the
  `group_null` workaround used here.
- `run_notebooks.py` `READ_ONLY_VERBS` flags pandas `.drop(`; I used column selection instead. A pandas
  `.drop(columns=...)` is harmless, so the guard may be broader than intended.
- Headless Chrome hung once at 768 with `--virtual-time-budget`; a `timeout 90` wrapper and no virtual-time flag
  worked.

## Revision 1 (answering `disbsad-review.md`, REVISE: 2 majors, 4 nits)

| Finding | Change |
|---|---|
| 1 major, `raw_feed.note` stated the `to` half-hour as a vendor rule | Scoped: "Replies fetched for this page also held the half-hour at `to`, so silver keeps it twice." (26 words). Vault body Known issues gains a dated "measured 2026-09-29" bullet: the nine replies for 13 to 21 Sep 2026 (fetched 2026-09-26) ran D 00:00 to D+1 00:00 UTC inclusive, transformer dedups within one bronze day (`disbsad.py:118-123`), 9 keys held twice, `to` inclusivity undocumented (`_publication_window.py:53-56`). |
| 2 major, £ and MWh unsourced | Vendor source found and quoted in a new body section "Vendor documentation": Elexon, *Imbalance Pricing Guidance* v15.0, 25 June 2020, p. 16: each Balancing Services Adjustment Action has a "Balancing Services Adjustment Cost – value in £ (can be a NULL cost)" and a "Balancing Services Adjustment Volume – value in MWh" (also the SO-Flag and STOR Provider Flag). Text extracted from the PDF with pypdf in a throwaway `uv --with` env. The schema table's `cost`/`volume` rows and the "Cost field unit" gotcha now cite it. Page units stand as written. The guidance states no sign convention for either field (whole-document search), so the page keeps "the sign's meaning is not stated". |
| 3 nit, key note referred to "the note" | System key note now "Signed, -100 to 750 MWh here; the sign's meaning is not stated." |
| 4 nit, grain / "one row per action" vs the relation | No change, as the checker allowed once finding 1 was scoped; the notebook lead, chart and rows all dedup. |
| 5 nit, `plot_alt` "blocks of 100 to 770 MWh" | Now "blocks of up to 770 MWh". |
| 6 nit, body NETBSAD claims contradict the netbsad note | Aligned with the netbsad note's sourced wording: the Overview now says DISBSAD is the individual actions, one of BSAD's two parts per the guidance p. 16, with no vendor text saying NETBSAD derives from it; the "NETBSAD is the aggregate" gotcha is replaced by the guidance reading plus the dated local measurement (netbsad 0.0 on 17 Sep P40 to 44 where these actions total 450 to 750 MWh). |

Checks after the revision: vault note CRLF on all 309 lines; mirror `cmp`-identical; `gridflow-build --only
elexon/disbsad` succeeds; `detect.mjs --json` returns `[]`; the rendered HTML carries the three new strings and no
"no vendor text". No change to the chart spec, series, sample or notebook cells (only `plot_alt` and page words),
so the artefacts and their digests are unchanged. Layout: the edited strings are the same length or shorter, in
places already checked at all four widths.
