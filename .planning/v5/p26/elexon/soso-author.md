# soso author report (SO-SO prices)

Writer: Opus 5.5, 2026-09-29. Page `elexon/soso`, landscape `market`.

## Status

- `gridflow-build --only elexon/soso`: green (dataset template); detector `[]`.
- Artefacts regenerated from local silver: `site/hifi/data/series/elexon/soso.json` (gridflow-distil, `spec_origin: vault`),
  `samples/elexon/soso.json` (gridflow-sample, 8 rows), `notebooks/elexon/soso.json` + `soso-5.png` (run_notebooks.py, no errors).
- Mirror `vault/elexon/soso.md` is byte-identical to the vault worktree note (`cmp`).
- No staged chart spec or authored override existed for soso.
- Chart: `line`, trader unit `EWIC_EG`, settlement dates 14 to 18 September 2026 (window 2026-09-13..2026-09-18,
  120 hourly points per series), `group: trade_direction`, `aggregation: mean` (mean of each start hour's contracts
  per direction), unit `£`.
- Screenshots (headless Chrome, own static server on 9734, stopped afterwards): 1440, 1024, 768, and 390 through a
  390 px iframe. Nothing clipped or overlapping: hero scenery, chart and key, raw feed, folded frame and guide,
  notebook panel, related list, stratum corner labels. Light equals dark: the site has no dark theme (no
  `prefers-color-scheme` / `data-theme` in CSS or JS). Not checked: the frame unfolded and the notebook drawer
  opened (headless screenshots cannot click).

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Vendor description "system operator to system operator prices data, filtered by publish time", max range 24 hours (`what_it_is`, `raw_feed.note`) | Elexon API reference for `/datasets/SOSO`, dumped with headless Chrome 2026-09-29 (bmrs.elexon.co.uk/api-documentation/endpoint/datasets/SOSO); quoted in the note body Overview |
| SO-SO services are provided mutually with interconnected TSOs, to adjust interconnector flows closer to real time (`what_it_is`) | Elexon Insights page "SO-SO trade prices" (bmrs.elexon.co.uk/soso-trade-prices), dumped 2026-09-29; quoted in the note body |
| Quantity in MW, price in £ (`what_it_is`, `chart.unit`, caption, `record.fields`) | Same Insights page: table heads "Trade Quantity (MW)", "Trade Price (£)". No per-MWh basis stated anywhere, so the page says "£ as Elexon labels it" |
| `Bid`/`Offer`: Elexon's docs define neither (`what_it_is`, `record.fields.trade_direction`) | API reference defines no response field; its example shows `tradeDirection: "A02"`; Insights page gives no definition. Bronze and silver carry `Bid`/`Offer` only (silver value_counts) |
| Grain/key: settlement date, contract id, direction (`facts.grain`, `record.key`) | `silver/elexon/soso.py:141-144` dedup `["settlement_date","contract_identification"] + "trade_direction"`, keep last; `ENTITY_KEY_COLUMNS` + `OPTIONAL_ENTITY_KEY_COLUMNS` at :26-27 |
| `timestamp_utc` copied from `start_time`; the feed sends no settlement period (`record.fields.timestamp_utc`) | `soso.py:90-108` (period branch only if `settlement_period` present, else `start_time`); bronze records have no `settlementPeriod` (bronze 2026/09/15 file, note's own bronze sample); silver has no `settlement_period` column; `timestamp_utc == start_time` on all rows |
| `end_time` null because `endTime` has no `Z` (`record.fields.end_time`) | `soso.py:118-125` parses with `%Y-%m-%dT%H:%M:%SZ`, `strict=False`; bronze `"endTime":"2026-09-16T22:00:00"`; silver null_count(end_time) = all rows |
| `published_at` is vendor `publishTime`; silver filed by publish window (`record.fields.published_at`, command comment) | `soso.py:62, 127-139`; `silver/elexon/_publication_window.py` (soso in scope: PUBLISH_DATETIME with default params, filtered on `published_at`); gridflow ADR-026 |
| 23-hour request windows; bronze filed by window start day (`raw_feed.note`) | `connectors/elexon/endpoints.py:243-248` `max_chunk_hours=23`; `client.py:93-99` chunk loop; `_fetch_datetime_range` `data_date = start.date()`; sidecars e.g. `bronze/elexon/soso/2026/09/14/*.meta.json` request `publishDateTimeFrom=2026-09-14T22:00:00Z&publishDateTimeTo=2026-09-15T21:00:00Z` |
| Request URL (`raw_feed.requests`) | `build_params` endpoints.py:300-313 (`_to_utc_z` `%Y-%m-%dT%H:%M:%SZ`, `page`); the 14 Sep sidecar above, which is the chunk that holds the eight rows (published 2026-09-15 10:03) |
| Ingest `--end` exclusive; commands start 13 Sep (`raw_feed.commands`) | `client.py` `while current < end`, `chunk_end = min(..., end)`. Settlement date 14 starts at 13 Sep 23:00 UTC (silver: min start_time per settlement date); its rows publish on the 13th. With `--start 2026-09-13 --end 2026-09-19` the chunks start 13 00:00, 13 23:00, 14 22:00 ... 18 18:00 (bronze days 13..18), so transform 13..18 inclusive |
| "September settlement dates start 23:00 UTC" / x_label | silver: settlement_date 14..18 each spans start_time D-1 23:00 to D 22:00 |
| Chart alt and key notes | committed series: bid 344.748..769.604 (345-367 from 22:00 to 04:00 UTC, 769.604 from 04:00 to 10:00, 475.9/476.4/476.5 from 10:00 to 22:00); offer -58.876..-0.045 (-0.045 22:00-04:00; -29.139 on 14th, 17th, 18th; -58.876/-58.585 on 15th/16th); no nulls, 120 points |
| `GL1_EG` carries the same prices in every hour shown (caption) | Polars full join of EWIC_EG vs GL1_EG on (start_time, direction, contract number), settlement dates 14..19: 2288 of 2288 prices equal |
| Eight rows: one Bid and one Offer from four trader units at 2026-09-15 12:00 (`record.caption`); sender/receiver one value, resource provider differs by unit (fields) | the committed sample (visible in the frame) |
| Notebook lead: relation `silver_elexon_soso`, `settlement_date` inclusive, lineage dropped, ordered by `settlement_date` | gridflow `schema_manifest` entry (relation_name `silver_elexon_soso`, designated_date_col `settlement_date`, not APPEND_ONLY so no `_latest`); gridflow_models `research/handles/source.py:401-448` |
| Related: fuelhh carries one signed code per interconnector link | fuelhh silver fuel_type values include INTEW, INTIRL, INTGRNL etc.; fuelhh note line 116 "interconnectors and PS are signed". No mapping from SOSO trader units to fuelhh codes is claimed |

## Note-body corrections (vault note `30-vendors/elexon/datasets/soso.md`)

1. Overview: added a "Vendor wording (read 2026-09-29)" paragraph quoting the API reference and the Insights page
   (definition, 24-hour cap, MW and £ labels, example `A02`, no Bid/Offer definition).
2. Dedup key line: was a placeholder; now `settlement_date, contract_identification, trade_direction` (soso.py:141-144).
3. Point-in-time line: was "`ingested_at` (no native PIT field)"; now `published_at` from `publishTime` (soso.py:127-139),
   silver filed by publish window (ADR-026).
4. Schema table: removed the `settlement_period` row and fixed `timestamp_utc` (copied from `startTime`, soso.py:90-108, :172);
   `trade_direction` "Direction code (sell/buy)" replaced by "`Bid` or `Offer` as sent; undefined"; `trade_price`
   "GBP/MWh" replaced by Elexon's "Trade Price (£)" with no per-unit basis; `end_time` now documented as null (soso.py:118-125);
   added the missing `published_at` row; `ingested_at` is silver transform time (soso.py:146-150), not bronze ingest.
5. Silver sample: removed `settlement_period`, `timestamp_utc` 00:00 corrected to 01:00 (= start_time), `end_time` None,
   added `published_at`.

## Could not verify

- Which side `Bid` and `Offer` are (who buys from whom), and whether a row is an executed trade or a quoted price
  (the per-hour ladder of 25 MW contracts per direction suggests quotes; not stated by Elexon). The page makes no
  claim either way beyond Elexon's own words.
- The price basis (£ per MWh is likely but only "£" is stated); the currency of the Irish-side units (`_EG`, `_SN`).
- Identities behind the EIC-style codes (`10X1001A1001A515`, `10X1001A1001A59Q`, `10X1001A1001A531`,
  `47X000000000386O`, `10XNITSO-12345-O`) and the interconnector behind each trader unit (`EWIC`, `MOYLE`, `GL1`). Not named on the page.
- Publication cadence: nothing from Elexon; locally each hour publishes about 1 h 56 min before it starts. The cadence
  fact says only "No cadence stated by Elexon; contracts here start on the hour".

## Open questions / issues for the seat

- The note body's Overview list of interconnectors (Moyle, IFA, IFA2, BritNed, NSL, ElecLink, NEMO, Greenlink,
  "Eleclink", Viking) is unsourced and lists ElecLink twice; the silver seen here only carries `EWIC`, `MOYLE` and `GL1`
  trader units. Left untouched (no vendor evidence either way); worth a vault fix.
- gridflow `docs/endpoints/elexon.md:565-580` describes soso with `Up`/`Down` directions, 500 MW rows and "Daily";
  none of that matches the feed. Not cited. `endpoints.py:242` calls the 1-day cap "undocumented"; Elexon's reference
  now states "maximum range of 24 hours". Candidate gridflow doc fixes.
- `end_time` is always null in silver because of the `Z`-only parse format: a gridflow transformer bug
  (the same pattern may hit other Elexon transformers that parse naive vendor times).
- `_NG` trader units split each hour's 16 contracts across one or two interconnectors, so they draw as fragments per
  unit; that is why the chart uses `EWIC_EG`, which has eight Bid and eight Offer contracts in every charted hour.

## Final checks

- A contract id never carries both directions on one settlement date (Polars: max n_unique(trade_direction) per (settlement_date, contract_identification) = 1), so "one row per contract" agrees with the three-column key.
- Final build `--only elexon/soso` green and detector `[]` after the last wording edits (caption and how_used "carries"/"under").

## Template notes

- None blocking. At 768 and 390 the frame folds before `trade_direction`, a key column; expected fold behaviour.
- The `market` landscape draws turbines, a substation and battery storage; fine for this page.

## Revision 1 (answers `soso-review.md`, 2 major, 3 nit)

1. **major, `notebook.cells[2]`:** the hand-aligned continuation lines are gone. `pivot_table(` and `.plot(` now break
   after the open parenthesis, with a 4-space hanging indent. Notebook re-run (`run_notebooks.py`, no errors). At 390
   cell [5] wraps as ordinary lines: no one-letter columns.
2. **major, `record.select`:** added `columns: [trader_unit, trade_price, trade_direction, contract_identification,
   settlement_date, trade_quantity_mw]` and re-ran `gridflow-sample`. The same eight rows now lead with trader unit
   and price: both are in view at 390 (the first two columns), and at 1280 everything through `timestamp_utc` fits.
   `record.fields` is reordered to the new frame order. The guide still lists the key columns under "Identifies a row".
3. **nit, caption:** now "the mean of each start hour's eight 25 MW `Bid` contracts, and of its eight `Offer`
   contracts" (the checker verified n = 8 and 25.0 MW in all 240 hour-direction groups). "`GL1_EG` carries the same
   prices here" keeps the claim scoped. 40 words.
4. **nit, sender/receiver lines:** "one value in all eight rows" removed. Each line now names the vendor field
   (`senderIdentification`, `receiverIdentification`). `resource_provider` also lost "it differs by trader unit
   here", which repeated the frame.
5. **nit, `.head()` output:** the cell is now `df[["trade_direction", "trade_price"]].head()`. At 390 the price column
   sits inside the box (three columns overflowed it; two fit).

Checks: vault note and mirror are byte-identical (`cmp`). `gridflow-build --only elexon/soso` is green and the
detector returns `[]`. Screenshots at 1280 and 390 (390 px iframe) were taken through a same-origin wrapper that
opens the notebook drawer. The wrapper was served by my own server on 9734, now stopped. Nothing is clipped or
overlapping in the hero, chart, raw feed, frame, guide, notebook cells [1] to [5] or the related list. The series is
unchanged: the chart spec was not edited, so no re-distil was needed.
