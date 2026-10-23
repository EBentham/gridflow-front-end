# OBP reserve availability and utilisation price: writer report, round 2 (2026-10-23)

All four findings of `obp-reserve-availability-utilisation-price-review.md` fixed.

| Gate | Result |
|---|---|
| `gridflow-build --only neso_data_portal/obp_reserve_avail_price` | ok (only the vault-wide "22 Known issues lines dropped" warning) |
| Detector | `[]` |
| Mirror | `cmp` clean; CRLF on every line, 0 bare LF |
| Rendered page | 0 em or en dashes |
| Notebook | not re-run: no cell changed (only the lead); the build's notebook digest check passes |
| Sample, series | unchanged (select and chart spec untouched) |
| Screenshots | re-taken at 1440, 1024, 768, 390 in `obp-reserve-avail-shots\`; the longer key note wraps cleanly at 1024 and 390, nothing clipped. Port 9986 server stopped |

## Fixes

1. **major, `page.record.fields.service_id`.** Now: "`PQR`, `NQR`, `PSR`: Positive Quick, Negative Quick, Positive Slow
   Reserve (NESO); no `NSR` here". Quotes re-checked in catalogue snapshot `20261006T195819Z`:
   `quick-reserve-auction-requirement-forecast` "Quick Reserve, separated into Negative Quick Reserve (NQR) and Positive
   Quick Reserve (PQR)"; `slow-reserve-requirement-forecast` "Slow Reserve, separated into Negative Slow Reserve (NSR)
   and Positive Slow Reserve (PSR)". Note body: the `service_id` bullet now quotes both and says this package's own
   dictionary does not expand the codes; the `TODO: verify` is gone. The Holds paragraph drops the code definitions from
   its open list and points to the Columns section. Labels unchanged. My round-1 "inference" wording is withdrawn.
2. **nit, `page.notebook.lead`.** "cell one converts to UTC" became "the query cell converts them to UTC" ("first query
   cell" put the lead at 36 words, one over budget). On the page the query is the only cell after setup that converts.
3. **nit, note body counts.** Scoped to the 8 October capture: service counts (with the 16 October figures beside them:
   `PQR` 60,000, `NQR` 18,877, `PSR` 81,518), the `pair_id` counts, and the zero-MW and zero-price counts. "60 distinct
   IDs in the capture" became "in each capture" (60 in both, checked). The ranges bullet holds for both and is unchanged.
4. **nit, `page.chart_view.key[0].note`.** Now "171.48 to 322.33 in July, a few high offers lifting 18 July; 237.19 to
   279.08 from September" (18 words). Checked: on 18 July 550 Positive Slow Reserve half-hours with MW above zero, median
   190.68; 31 from `ARLS-01` at 2,038.68 to 2,042.09 and 6 from `HULL-01` near 1,196; without the offers of 1,000 and more
   the day's mean is 208.27. I left the figure 2,000 off the page, since no chart point, row or notebook output shows it;
   the note says "a few high offers" instead.

## Defects

No new ones. The round-1 Defects section stands.
