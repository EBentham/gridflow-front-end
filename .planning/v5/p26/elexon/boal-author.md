# boal (Bid-offer acceptance levels): author report

Writer: Opus 5.5 · high, 2026-09-29. Page `site/hifi/data-sources/elexon/boal.html` in the front-end worktree
(`scratchpad/p26-elexon`). Canonical note `scratchpad/vault-p26-elexon/30-vendors/elexon/datasets/boal.md`, mirror
`vault/elexon/boal.md`, byte-identical (`cmp`), CRLF kept (307 lines before the edits, all CRLF).

## Status

- `gridflow-build --only elexon/boal`: green. `detect.mjs --json`: `[]`.
- Artefacts: `site/hifi/data/series/elexon/boal.json` (`spec_origin: vault`, 2 series x 168 hourly points, 93,471
  acceptances after dedup), `samples/elexon/boal.json` (8 rows, `gridflow-sample`), `notebooks/elexon/boal.json` +
  `boal-5.png` (`run_notebooks.py`, 5 cells, no errors, read-only cells).
- No staged spec or authored override existed for boal (the `rm -f` was a no-op).
- Screenshots (headless Chrome, server on 9731, stopped): 1440, 1024, 768 full page; 390 as six 390 px iframes opened at
  each section anchor (one tall 390 iframe stops painting after ~1,600 px in headless Chrome, so it is not usable). The
  frame was also shot unfolded at 1440 and 390 from a temporary copy with the fold checkbox checked (copy deleted).
  The site has no dark scheme (no `prefers-color-scheme` or theme switch in `site/hifi/assets`), so light only.
- One fix made from the screenshots: `chart.unit` was `acceptances`; at 390 the y-axis title ran off the left edge
  (`chart_svg.py:329` end-anchors the unit at the axis). Changed to `count`, re-distilled, rebuilt: fits at 390 and 768.

## Chart

Stacked area, silver `elexon/boal`, **count of distinct acceptances per hour of `acceptance_time` (UTC), 14 to 20
September 2026**, split by `so_flag`. Spec: `time: acceptance_time`, `dedup: {on: [bm_unit_id, acceptance_number,
acceptance_time], order_by: timestamp_utc}`, `group: so_flag` with `group_map {"true": so_flagged, "false":
not_flagged}` (no unmapped groups), `aggregation: count`, `time_bucket: 1h`, window 14 to 20 Sep. Nothing is summed:
level columns are operating points (not additive), and silver has no segment times, so a per-unit level trace cannot
be drawn honestly. Counting acceptances is additive and unaffected by which segment silver kept (every acceptance keeps
at least one row). The 8 hours with no SO-flagged acceptance come out null in the series and the stacked renderer draws
them as 0 (`chart_svg.py:379`), which is right for a count. Paints: two unpainted hatches (no palette role fits).

Alt numbers from the committed series: totals 80 (2026-09-15T22:00Z) to 1,304 (2026-09-19T15:00Z); SO-flagged max per
hour 66 on the 14th, 283 at 2026-09-19T18:00Z, 188 max on the 20th; SO-flagged min 0 (8 hours).

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Endpoint `/datasets/BOALF`, `from`/`to` params (raw_feed.requests) | `connectors/elexon/endpoints.py:65-71` (`param_style=PUBLISH_DATETIME, from_param="from", to_param="to"`) |
| `...?from=2026-09-13T00:00:00Z&to=2026-09-14T00:00:00Z&page=1` | `build_params` `endpoints.py:300-313` (`_to_utc_z`, `page` always sent); 24 h chunks `client.py:93-99` (`max_chunk_hours=24`); bronze sidecar for 2026-09-19 shows the same shape (`request_params: from, to, page`) |
| Ingest `--end` exclusive | `pipeline/runner.py:479-500` (bare date = midnight UTC); `client.py:96` `while current < end` |
| Transform `--end` inclusive | `pipeline/runner.py:1125-1138` (`date_range(start.date(), end.date())`) |
| Ingest 13 to 21 Sep (`--end 2026-09-22`), transform 13 to 21 | Bronze day D = request window D 00:00 to D+1 00:00 UTC (`data_date = start.date()`, `client.py:314`). Silver file D holds settlement date D periods 3 to 48 and D+1 periods 1 to 3 (Polars on all September files). Chart window is acceptance time 14 to 20 Sep; first silver row per acceptance is between 72 min before and 61 min after `acceptance_time`, so bronze 13 and 21 are needed at the edges. Notebook reads settlement date 19 Sep (bronze 18 and 19) |
| raw_feed.note: summer settlement day starts 23:00 UTC, first periods in previous day's window | `utils/time.settlement_period_to_utc(2026-09-19, 3)` = 00:00 UTC; silver per-file settlement ranges above |
| Grain / key `(settlement_date, settlement_period, bm_unit_id, acceptance_number)` | `silver/elexon/boal.py:26-27` (`ENTITY_KEY_COLUMNS` + optional `acceptance_number`), dedup `boal.py:120-123` |
| what_it_is: Elexon sends each acceptance as segments with a MW level at start and end time | Bronze 2026-09-19: 41,078 records, 16,699 (unit, acceptance) pairs, 1 to 6 records each, each with `timeFrom`/`timeTo`/`levelFrom`/`levelTo`; Elexon BSC glossary "Bid-Offer Acceptance Level" (elexon.co.uk/bsc/glossary/bid-offer-acceptance-level/): MW level at the beginning and end with start and end times |
| "A level is where the unit runs, not a change" | Same glossary page ("MW operational level"); vault note sample `levelFrom 480, levelTo 480` for `T_MRWD-1` |
| Silver keeps one segment per acceptance and period, "the last one received", drops segment times | `boal.py:74-78` renames `timeFrom`/`timeTo`, `boal.py:133-148` `output_cols` omits them; `unique(..., keep="last")` `boal.py:123`. On bronze 2026-09-19, 12,252 silver keys had more than one raw segment; the kept row equals the last in response order in all 12,252 (it was also the earliest by `timeFrom`, because Elexon's order ran backwards in time, but that is response order, not a code rule, so the page does not say "earliest") |
| chart caption: "An acceptance counts once however many rows it has" | The spec's dedup on `(bm_unit_id, acceptance_number, acceptance_time)` is the rule that makes it so. `acceptance_time` (and `so_flag`) are constant per (unit, acceptance number) on every September row (0 pairs with more than one value), so the third key column only guards against a reused number; it splits nothing |
| timestamp_utc: start of the settlement period, not the segment's start | `boal.py:109-118` (`settlement_period_to_utc(settlement_date, settlement_period)`); `event_time == timestamp_utc` on all rows of 2026-09-19 file |
| settlement_period from `settlementPeriodFrom` | `boal.py:61-63`; raw BOALF sends `settlementPeriodFrom`/`settlementPeriodTo`, no `settlementPeriod` |
| settlement_date "as Elexon labels it" | `boal.py:60, 91` (cast only) |
| so_flag meaning (key note; field guide "True when the SO believes a transmission constraint may affect the acceptance") | Elexon, *Imbalance Pricing Guidance* v15.0, 25 June 2020, section 3 ("System Operator Flagging"): for BOAs the SO flags when it believes the BOA may be impacted by a transmission constraint. PDF fetched from elexon.co.uk/bsc/documents/training-guidance/bscguidance-notes/imbalance-pricing/; quote now in the note body's `so_flag` row |
| deem/stor/rr flag lines ("as sent") | `boal.py:67-71`; no meaning claimed |
| acceptance_time "when the system operator issued the acceptance, UTC" | Vault note ("Time the acceptance was issued"); cast `boal.py:102-107` from `...Z` strings |
| "one acceptance can span several periods" | The eight rows: 991 in periods 36 and 37; 993 and 994 in 37 and 38 |
| Eight rows | `T_COALB-2`, 2026-09-19, periods 36 to 38 = exactly 8 rows (`gridflow-sample` wrote 8). `T_COALB-2` is fuel type `OTHER` in `bmunits_reference`, so no technology is named |
| notebook.lead relation and filter | `_relation_name_for_dataset("boal")` = `silver_elexon_boal` (run); `DESIGNATED_DATE_COLS[("elexon","boal")] = "settlement_date"` (`gridflow/silver/schema_manifest.py:116`); `source.py:401-449` inclusive both ends, bitemporal columns excluded |
| plot_alt numbers | Polars on silver settlement date 19 Sep, unique (unit, acceptance): `E_THMRB-1` 201, `E_WHTBB-1` 199, `E_NEWPB-1` 187 ... `E_CHAPB-1` 143 (10th); matches the PNG |
| related: pn, bmunits_reference, disbsad, system_prices | All in `site/hifi/data/elexon.json`; SO-flag on BSAD actions and BOAs feeding imbalance prices: Imbalance Pricing Guidance v15.0 sections 2 and 3 |

## Note-body corrections (canonical note, mirrored)

1. Overview: "National Electricity System Operator (NESO)" to "National Energy System Operator (NESO)".
2. Dedup key: "_inline in transformer_" to the actual key and `keep="last"` within one bronze day (`boal.py:120-123`).
3. `so_flag` row: added the Imbalance Pricing Guidance quote (vendor evidence the page relies on).
4. `bid_offer_level_from` row: added the BSC glossary reading (level at segment start; start and end levels and times).
5. `ingested_at`: "Time ingested into bronze" to "When the silver transform ran" (`boal.py:125-129`).
6. Silver sample `timestamp_utc` for 2026-05-06 period 9: `04:00` to `03:00` UTC (`settlement_period_to_utc` returns 03:00).
7. Known issues: replaced "Long-acceptance records may be deduped against shorter overlapping ones" with the exact
   dropped fields (`timeFrom`, `timeTo`, `settlementPeriodTo`, `amendmentFlag`, `nationalGridBmUnit`) and the one-segment
   dedup; added a labelled measurement (not vendor-documented) that the 2026-09-19 `from`/`to` response ran `timeFrom`
   00:00 to 24:00 inclusive, so a midnight segment sits in two bronze days and two silver files with the same key
   (814 such duplicate keys across the September files, all at 00:00 UTC).

Left alone: em dashes and "Near real-time"/"Several years" in the body (not on the page; unverified, not shown), the
schema table's `float` for levels (Pydantic says `float`; silver stores `Int64` because the transformer never casts).

## Not verified

- What `from`/`to` filter on per Elexon. `_publication_window.py:49-52` calls the override undocumented; the page says
  only "24-hour `from`/`to` windows".
- Whether Elexon's response order (latest segment first) is stable. The page says only "the last one received".
- `deemedBoFlag`, `storFlag`, `rrFlag` meanings: not stated on the page. They were false on every September row, which
  the page does not claim.
- Elexon's historical depth for BOALF: no `history` fact.

## Open questions (for the seat)

- **Silver loses the acceptance profile.** `boal.py` drops `timeFrom`/`timeTo` and keeps one segment per (date, period,
  unit, acceptance); on 19 Sep, 41,078 raw segments became 22,538 silver rows. A gridflow unit to keep segment times
  (and key on `timeFrom`) would make levels usable; the page states the limitation plainly.
- **Cross-file duplicates at midnight UTC** (814 keys in September). `query()` returns both copies; the notebook uses
  `drop_duplicates` on (unit, acceptance) and the chart dedups, so nothing on the page is affected.

## Template problems (not worked around)

1. **The level columns fold at every width.** Frame columns follow silver order; `bid_offer_level_from`/`_to` are
   11th and 12th, so at 1440 they fold behind `…` with `rr_flag`, and unfolded they sit past the box edge (sideways
   scroll). The column that matters most on this page is never visible without scrolling. At 1024 and below
   `acceptance_number` folds too (at 768 and 390 only date, period, timestamp and unit show), so the eight rows look
   alike apart from the period and the caption's acceptance numbers are not visible in the folded frame. The guide lists them, and
   the caption and what_it_is carry the point, but a per-note column order or a "show these first" option would help.
2. **Long `chart.unit` strings clip at 390.** `chart_svg.py:329` end-anchors the unit at `x0 - 10`; a unit wider than the
   left gutter runs off the SVG. Worked within it by using `count`; other pages with a long unit would hit it.
3. At 768 the y-axis title sits within a pixel or two of the top tick label (no overlap).
