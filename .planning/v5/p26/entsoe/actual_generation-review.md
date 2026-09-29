# entsoe/actual_generation: checker review

Checked 2026-09-29 against the canonical note (vault worktree, diff vs `origin/master`), the committed artefacts, the built page, gridflow code, local silver and bronze (read only), and the vendor's own API documentation.

**Verdict: REVISE.** 1 blocker, 2 majors, 2 nits.

## Findings

### 1. Blocker: `page.record.fields.timestamp_utc` (and body line 235)

- **What is wrong.** The guide reads "period start plus position times resolution". That puts every row one step late.
- **Evidence.** The code computes `timestamp = start_dt + (position - 1) * resolution` (`connectors/entsoe/parsers.py:530`). Worked check: the sample row at 12:00Z on 18 September is position 49 of a PT15M period starting at 00:00Z. The page's formula gives 12:15.
- **Same error in the body.** The silver schema table in the body (note line 235, older text) has the same mistake: "`<Period>` start + position * resolution".
- **Fix.** For example, "Start of the time step: period start plus (position minus 1) steps of `resolution`, UTC". Correct the body cell to `start + (position - 1) * resolution`.

### 2. Major: `page.what_it_is` and `page.how_used` understate the silver defect

- **What is wrong.** `what_it_is` says: "Some types, such as pumped storage, also carry a consumption series; silver keeps one row per key and cannot tell which."
  - "Cannot tell which" never says that `generation_mw` can hold the consumption figure.
  - "Some types, such as pumped storage" undersells the reach.
- **The overclaim in `how_used`.** The second bullet, "Wind and solar outturn to score `wind_solar_forecast` zone by zone", cannot be done from this silver table for NL, where wind and solar are mostly consumption. The first bullet, "Fuel mix ... per continental zone", has the same problem for NL and IE-SEM.
- **Evidence: the defect reproduces exactly.** I re-parsed every bronze file with `parse_timeseries_xml`, renaming `outBiddingZone_Domain.mRID` so the side survives, and joined the result to silver on the key.
  - `connectors/entsoe/parsers.py:289-297` reads both domain tags into `in_domain`.
  - `silver/entsoe/actual_generation.py:80` dedups `(timestamp_utc, area_code, production_type)` with `keep="last"`.
  - Outcomes: 63,984 generation-only rows, all matching; 19,623 both series with silver holding consumption; 11,193 both series with silver holding generation; 2,752 consumption only; 3,279 both equal. Total 100,831, identical to the writer's table.
  - Every TimeSeries in bronze carries `businessType` A01, on both sides.
- **Evidence: how far it reaches.** These are the types where silver holds a consumption value (both-differ-consumption-kept or consumption-only):

  | Zone | Types | Share of the zone's silver rows |
  |---|---|---:|
  | DE-LU | B10 | 4.0% |
  | BE | B10, B18 | 6.3% |
  | FR | B05, B10, B18, B25 | 17.5% |
  | NL | B01, B04, B05, B14, B16, B17, B18, B19, B20 | 56.2% |
  | IE-SEM | B04, B05, B06, B08, B10, B11, B20 | 50.2% |

  - NL solar B16: 1,422 of 2,303 rows. NL wind B18: 1,439 of 2,303. NL wind B19: 1,439 of 2,303.
  - FR B18: 58 of 2,304. BE B18: 45 of 574.
- **Fix.** The counts above are evidence for the seat, not page content. On the page, say what the vendor sends and what silver does, without local counts. For example:
  - `what_it_is`: "ENTSO-E also sends a consumption series for some types (in these responses, pumped storage in DE-LU and BE, and most types in NL and IE-SEM). Silver keeps one row per key, so `generation_mw` can hold the consumption figure, and nothing marks which."
  - `how_used`: scope the wind and solar bullet, for example "Wind and solar outturn to score `wind_solar_forecast`, in zones without a consumption series (DE-LU)". Or drop "zone by zone". Scope the fuel-mix bullet the same way.

### 3. Major: `page.facts.cadence` is stated as a general rule

- **What is wrong.** "Every 15 minutes for DE-LU, FR and NL; half-hourly IE-SEM; hourly BE" reads as a vendor rule.
- **Evidence.** Its only evidence is the `<resolution>` tags in gridflow's bronze responses. The writer's own evidence table cites "bronze `<resolution>` tags 2026-09-15", and silver `resolution` has one value per zone. No vendor document fixes a zone's resolution, and ENTSO-E zones have changed resolution before.
- **Fix.** Scope it to the responses, for example "As sent in these responses: 15-minute steps for DE-LU, FR and NL; half-hourly IE-SEM; hourly BE". The body's Known issues line is already scoped ("in bronze (2026-09-15)"). The `record.fields.resolution` line ("Step as sent") is fine.

### 4. Nit: note body TODOs (Business type row, PSR codes section, B25), sourcing

- **What is wrong.** The note marks two things as de facto only, backed by entsoe-py plus the values: "out series = consumption" and the names for B02, B03, B06 and B25. Both carry `TODO: verify`. The vendor's own documentation settles both.
- **Evidence.** ENTSO-E's Postman collection "Transparency Platform Restful API", which the vendor links as its developer documentation (https://documenter.getpostman.com/view/7009892/2s93JtP3F6):
  - Item "16.1.B&C Actual Generation per Production Type" says that `inBiddingZone_Domain` series carry generation values and `outBiddingZone_Domain` series carry consumption values.
  - Its `psrType` parameter lists "B02 = Fossil Brown coal/Lignite; B03 = Fossil Coal-derived gas; ... B06 = Fossil Oil; ... B20 = Other; B25 = Energy storage".
- **Page impact.** Nothing on the page overstates these. The page's names (lignite B02, coal gas B03, oil B06) and the B10 "pumping (consumption)" line are correct against the vendor.
- **Fix.** Replace the two TODOs with this vendor citation. `record.fields.generation_mw` could then cite the vendor rule instead of "checked against bronze". Optionally restore B25's name.

### 5. Nit: `page.chart_view.alt` omits geothermal

- **What is wrong.** The alt text says "oil, waste and other renewables" for a group that also holds B09 geothermal.
- **Evidence.** The key note lists B09, and `group_map` includes it. Harmless, since geothermal is small, but the alt should name what the band sums.

## Checked and clean

- **The chart.**
  - The spec filter is DE-LU (`10Y1001A1001A82H`) with `production_type ne B10`, fixed window 12 to 18 Sep; the caption states the B10 exclusion.
  - I recomputed the groups from silver: 10,079 rows, 15 codes, all mapped, 672 points per group (B12 has 671).
  - The committed series matches silver to 0.0005 MW in every group at every point. `spec_origin: vault`, and there is no staged spec or authored override.
  - Alt values match: biomass 3,580 to 4,402; lignite 4,255 to 12,440; gas 1,337 to 9,625; wind 1,662 to 27,055; solar max 48,938 at 15 Sep 10:30Z; stack 30,118 to 75,594.
  - All DE-LU non-B10 rows are clean: 34,017 of 34,017 match the generation series, and the 12 to 18 Sep window has 10,079 of 10,079. Nothing charted is a consumption value.
- **Sample rows.**
  - The 8 rows (DE-LU, 18 Sep 12:00Z) match silver.
  - B10 4,055.1934 is the consumption series (generation 67.3645). The guide says so, and no other row is affected.
  - The 17:00Z counter-example the writer cites also reproduces: silver 13.78, generation 5,416.94.
- **Notebook.**
  - Written by `run_notebooks.py`, read-only cells, no errors.
  - `.head()` shows DE-LU B01 to B05 at 12 Sep 00:00Z, all clean. The plot is DE-LU B16, clean; the image matches `plot_alt` (daily peaks 22,047 on the 13th to 48,938 on the 15th, 10:00 to 11:45 UTC).
  - The lead matches `gridflow_models` `query()`: `_date_range_predicate` on `timestamp_utc` with inclusive ends, lineage exclude, `ORDER BY timestamp_utc`.
  - I opened the full notebook at 1440 and 390.
- **Raw feed.**
  - The URL matches bronze `request_url`: parameter order, `%Y%m%d%H%M`, host `web-api.tp.entsoe.eu/api`.
  - One request per zone and UTC day (`day_subwindows`, `utils/time.py:123-163`).
  - Ingest `--end 2026-09-19` is exclusive at midnight; transform 12 to 18 is inclusive.
  - `DEFAULT_ZONES` has six zones (`endpoints.py:395`). All 26 GB bronze files are `Acknowledgement_MarketDocument`.
- **Related `elexon/fuelhh`.** The link `../elexon/fuelhh.html` resolves. The page claims no match with it: "which this feed does not carry" and "comes from Elexon `fuelhh`" are both true. The other three related pages resolve too.
- **Gates.** `gridflow-build --only entsoe/actual_generation` passes and the detector returns `[]`. The rendered page has no em dashes, middle dots, arrows, live, now or local-data words.
- **Rendering.**
  - Screenshots at 1440, 1024, 768 and 390; 390 used a 390 px iframe.
  - They covered the hero scenery, chart and key, raw feed, the frame folded and unfolded with its guide, the notebook preview and the opened notebook, related, and every corner label.
  - Nothing is clipped or overlapping. There is no horizontal page overflow; scroll width equals viewport width at every width.
  - The known clip of the notebook filename at 390 is template work (ruling #39).
  - The site has no dark stylesheet, so I checked light only.
- **Mirror.** `vault/entsoe/actual_generation.md` is identical to the canonical note apart from line endings: the mirror is now LF, canonical is CRLF, written at 19:17 after the writer's copy. Re-copy byte for byte after the revision.
