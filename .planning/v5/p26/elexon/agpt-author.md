# agpt: author report

Page: `elexon/agpt`, "Actual generation per type". Writer: Opus 5.5 · high, 2026-09-28.

## Status

- `page:` block written in the canonical note (vault worktree `30-vendors/elexon/datasets/agpt.md`),
  copied byte for byte to `vault/elexon/agpt.md` (`cmp` clean).
- Artefacts, all from real silver: `site/hifi/data/series/elexon/agpt.json` (gridflow-distil,
  `spec_origin: vault`, 9 series x 336 points, 3,696 rows used, 0 duplicates dropped),
  `site/hifi/data/samples/elexon/agpt.json` (gridflow-sample, 8 rows x 15 columns),
  `site/hifi/data/notebooks/elexon/agpt.json` + `agpt-5.png` (run_notebooks.py, 5 cells, no errors).
- No staged spec and no authored override existed for agpt (nothing to delete).
- `gridflow-build --only elexon/agpt`: succeeds. `detect.mjs --json`: `[]`.
- Chart: stacked area, settlement dates 14 to 20 September 2026 (the only complete 7-day run in local
  silver; silver files run 13 to 21 Sep plus 1 to 5 Aug).

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Grain and key: one row per `settlement_date`, `settlement_period`, `psr_type` (facts.grain, record.key) | `silver/elexon/agpt.py:26` ENTITY_KEY_COLUMNS; `:114-117` `unique(subset=[...], keep="last")` |
| B1620 (facts.vendor) | `connectors/elexon/endpoints.py:163-166` description "Actual Aggregated Generation Per Type (B1620)" |
| Every 30 minutes (facts.cadence) | settlement-period grain; one `document_id` per period in silver (11 rows each, 672 docs over 7,392 rows) |
| `psr_type` is a readable label, not a code (what_it_is, record.fields) | `agpt.py:62` renames `psrType` as is; silver values `Biomass`, `Fossil Gas`, ..., `Wind Onshore`; vault Known issues |
| "A recent half-hour carries 11 types"; includes Solar, Wind Offshore, Wind Onshore, no interconnectors (what_it_is) | silver `psr_type.value_counts()`: exactly 11 labels, 672 rows each; row set for 2026-09-20 period 48 shows 11 |
| FUELHH lacks solar and the wind split; FUELHH PS is signed (what_it_is, key notes, related) | `vault/elexon/fuelhh.md` what_it_is ("There is no solar code", "pumped storage (PS), whose sign...", single `WIND` code) |
| `settlement_date` is the vendor label (record.fields) | `agpt.py:59,80` rename + cast; no recomputation (contrast fuelhh 2.0.0) |
| `settlement_period` 1 to 48; 46 or 50 on clock-change days | `schemas/elexon.py:539` `Field(ge=1, le=50)`; GB calendar |
| `timestamp_utc` computed from settlement date and period (record.fields, x_label) | `agpt.py:87-96` `settlement_period_to_utc(settlement_date, settlement_period)`; vendor `startTime` not used |
| `generation_mw` from vendor `quantity` | `agpt.py:63` |
| `business_type`, `document_id`, `document_revision` as sent | `agpt.py:64-66` |
| Wind and solar business types differ "in these rows"; one document carries all eight rows "here" | sample rows: `Wind generation`, `Solar generation`, `Production`; single id `NGET-EMFIP-AGPT-0921260059` |
| `published_at` "here after midnight UTC, the next day" (record.fields, raw_feed.note) | sample rows: settlement 2026-09-20 period 48, `timestamp_utc` 22:30 UTC, `published_at` 2026-09-21 00:59:02 UTC |
| Request URL (raw_feed.requests) | `endpoints.py:163-166` PUBLISH_DATETIME; `client.py:93-99` 24 h chunks; `endpoints.py:300-313` `publishDateTimeFrom/To` via `_to_utc_z`, `page` added; same shape the fuelhh page uses |
| Bronze filed by publish day (raw_feed.note) | `client.py:314` `data_date = start.date()`; `bronze/writer.py:37-47` partition by `data_date` |
| ingest `--start 2026-09-14 --end 2026-09-22`, end exclusive | `client.py:95-99` `while current < end`; settlement 14 Sep period 1 (13 Sep 23:00 UTC) published 01:29 on the 14th; settlement 20 Sep periods 47-48 published on the 21st (silver file `agpt_20260921` holds settlement 2026-09-20 periods 47-48) |
| transform `--start 2026-09-14 --end 2026-09-21`, inclusive, "by publish day" | no `PARTITION_SOURCE_OFFSETS` in `agpt.py` (base default `(0,)`, `silver/base.py:417`); silver file D = bronze day D; silver 14..21 covers settlement 14..20 complete |
| notebook.lead: relation, date column, inclusive, lineage dropped | gridflow_models `_get_method_registry`: `agpt` -> `settlement_date`, `silver_elexon_agpt`; `handles/source.py:434-451` `BETWEEN` inclusive; `_BITEMPORAL_EXCLUDE` = event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year |
| notebook.needs "14 to 21 September 2026" | matches the commands' transform window |
| Chart spec: filter `settlement_date` 14..20, window 13..20 on `timestamp_utc`, sum by group | `distil.py:271-278` fixed window, end day inclusive; series file `window` 13..20, 336 x-points from 2026-09-13T23:00Z to 2026-09-20T22:30Z |
| Chart dedup on key ordered by `published_at` | defensive only (a re-issue on a later day would land in another silver file); 0 dropped |
| x_label "each starts at 23:00 UTC" | BST window; first x-point 2026-09-13T23:00Z |
| Alt numbers: nuclear 3.3-3.7 GW, gas 1.5-12.1, wind up to 20.2 (2.2-4.6 for a day from the 17th), solar up to 10.1 on the 20th, PS up to 1.2, total 12.4-33.8, none below zero | committed series min/max: nuclear 3279/3737, gas 1460/12101, wind 2245/20223, solar 0/10099 at 2026-09-20T13:00Z, ps 0/1211, total 12401/33774, coal_oil 0/0 |
| Caption caveat: wind 2.2-4.6 GW for a day from 15:30 UTC on the 17th; FUELHH wind does not dip | AGPT silver 2026-09-17 15:30 to 2026-09-18 15:30 UTC: offshore 117-288 MW, offshore+onshore 2245-4625 MW; FUELHH silver `WIND` same half-hours 11,704-16,879 MW; all AGPT rows revision 1. A project comparison, stated as such; cause not asserted |
| Key notes: PS "zero or above in this window"; coal and oil "zero in every half-hour of this window" | committed series ps min 0, coal_oil 0/0 |
| plot_alt | `agpt-5.png` viewed; solar daily maxima 6,059 to 10,099 MW; offshore 117-288 MW during the dip, about 11,000 MW after |
| related entsoe/actual_generation "empty for GB" | `vault/entsoe/actual_generation.md:63` GB returns "No matching data found for AGGREGATED_GENERATION_PER_TYPE_R3 [16.1.B&C]"; `:152` |
| related agws "actual or estimated"; atl "same B-series group" | `endpoints.py:162` comment "ENTSO-E / B-series datasets (AGPT, AGWS, ATL)", `:168-176` descriptions (B1630, B0610) |
| elexon/agws, elexon/atl, entsoe/actual_generation have pages | `site/hifi/data/elexon.json`, `entsoe.json` page sets; build resolved them |

## Note-body corrections (canonical vault note)

1. `ingested_at` row: "Time ingested into bronze" -> stamped at silver transform (`agpt.py:119-124`).
2. Silver sample `timestamp_utc` for 2026-05-06 period 4: `01:30` -> `00:30` (BST; matches the bronze
   sample's `startTime` 00:30Z and `settlement_period_to_utc`).
3. Known issue "latest revision wins": the transformer never compares `document_revision`; it keeps
   the last row per key in bronze file order (`raw_{ts}_{hash}`, `bronze/writer.py:57`) within one
   publish-day partition (`agpt.py:114-117`). Rewritten to say so.
4. Silver path pattern: added that `YYYYMMDD` is the bronze publish-window day, not the settlement date
   (`client.py:314`, no offsets).
5. Publication lag row: kept the vendor line, appended the project measurement (149 min after
   `timestamp_utc` on every row, so periods 47-48 fall in the next UTC day's window), labelled as
   measured, not a vendor statement.
6. New Known issues bullet: the 17-18 Sep 2026 wind dip with numbers, cause unverified, not checked
   against the live API.

## Not verified

- Why AGPT wind collapses for 24 hours on 17-18 Sep 2026 while FUELHH does not (vendor fault, a missing
  unit set, or later revision). No live API call was allowed; all local rows are revision 1.
- Whether AGPT pumped storage can ever be negative (Elexon does not say; this window has none).
- The 149-minute publish lag is measured on local silver only, not a vendor rule. The page states the
  lag only through the visible row (period 48 published 00:59 UTC next day).
- What `Other` holds; stated as undocumented.
- Dark mode: the site has no dark theme (`prefers-color-scheme` appears in no stylesheet and not in
  DESIGN.md), so only the light rendering exists.

## Open questions

- gridflow code: `schemas/elexon.py:533-535` docstring says `psr_type` is an EIC B-code; silver holds
  labels. Not my file; worth a gridflow issue.
- gridflow code: a revision published on a later day would give a second row for the same key in a
  different silver file, and `query()` would return both. Not seen locally (0 cross-file duplicate
  keys), but the transformer's dedup cannot prevent it.
- Taste: wind offshore and onshore are summed into one band to stay within 9 key entries while keeping
  coal and oil visible as a zero band. The split is carried by `what_it_is`, the eight rows and the
  notebook plot. The alternative is to split wind and filter out coal and oil.
- Window choice: the only complete week in local silver contains the wind anomaly. I kept it with a
  caption caveat rather than pick a window to avoid it.

## Tooling notes for the seat (no template problems found)

- The worktree `.venv` has no `tzdata`: `gridflow-distil` / `gridflow-sample` fail on any UTC datetime
  `.min()`. I ran them with `uv run --with tzdata --system-certs --extra distil ...` (ephemeral overlay,
  shared venv untouched).
- Headless Chrome `--window-size=390` lays out at about 500 px (minimum window width) and crops; I
  rendered 390 inside a 390 px iframe instead. The browser pane's screenshots came back blank, so the
  open notebook and unfolded frame were checked by overflow measurement at all four widths plus
  headless shots of a scratch copy with the drawer unhidden and the fold checkbox checked.
- Mirror line endings: the vault note is CRLF, the committed mirror LF; `.gitattributes` has
  `*.md text eol=lf`, so the `cp` normalises on add.

## Screenshots checked

1440, 1024, 768, 390 (light only; no dark theme exists): hero scenery (turbines, offshore wind, labels),
chart and key (longest codes "Hydro Run-of-river and poundage" and "Fossil Hard coal, Fossil Oil" fit,
the latter about 16 px from the 390 gutter), raw feed, frame folded and unfolded (horizontal scroller,
page width equals viewport), column guide, notebook closed and open, related. Nothing clipped or
overlapping. One fix made from this: the plot cell's continuation indent wrapped mid-token at 390,
now a hanging indent.

## Revision 1 (2026-09-29, after `agpt-review.md`: APPROVE, 4 nits)

All four nits applied in the canonical note, then copied to the mirror (`cmp` clean, CRLF kept).

1. **Caption** (`page.chart_view.caption`): the FUELHH comparison is now labelled as the project's
   own check: "Wind reads 2.2 to 4.6 GW for a day from 15:30 UTC on the 17th; the project found no
   such dip in FUELHH." "Cause unverified" is gone (no cause is asserted). The first sentence is
   tightened to "types summed per group", keeping the caption within its 40-word budget.
2. **`Other` key note**: "Elexon's own type" became "The vendor's Other type; what it holds is
   undocumented."
3. **Wind tag**: dropped `tag: wind`, so no label sits on the step up at 16:00 UTC on 18 Sep. The
   key still names the band.
4. **Note body, local measurements removed**:
   - the Publication lag row is back to the vendor line only;
   - the "Wind dip, 17-18 Sep 2026" Known issues bullet is deleted;
   - "Only revision 1 seen in silver as of 2026-09-28" is deleted from the revision bullet.

   The code-based corrections stay: `ingested_at`, the sample `timestamp_utc`, the dedup order and
   the silver file date. The lag and dip measurements, and the reviewer's AGWS agreement (identical
   dip in AGWS silver), now live only in this report as evidence.

Checks:

- `gridflow-build --only elexon/agpt` is green (no `--with tzdata` needed now).
- `detect.mjs --json` returns `[]`.
- The series, sample and notebook artefacts are unchanged; the build digest check passes.
- Screenshots at 1440 and a true 390 (390 px iframe): the caption, key and chart show nothing clipped
  or overlapping.

Template observation: since the main merge, the 390 x-axis shows a trailing "21" tick at the domain
end, next to "20". The chart ends at 23:00 UTC on the 20th, the start of settlement date 21. The two
labels do not overlap, but the tick labels a day with no data. This belongs to the seat, and I have
not worked around it.
