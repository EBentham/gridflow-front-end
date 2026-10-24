# Held Network charges pages: checker review (2026-10-24)

Checked in `C:\gridflow-wt\fe-neso-nc` and `C:\gridflow-wt\vault-neso-nc` against the writer's report, the catalogue
snapshot of 6 October 2026, the field-info dictionaries, the registry questions (ledger rows 71, 72, 127 and
`eligibility.md` lines 30, 184, 308-315), bronze (2026-10-08) and silver.

## Verdicts

| Page | Verdict |
|---|---|
| `aahedc-tariffs` | APPROVE with nits |
| `gis-boundaries-for-gb-generation-charging-zones` | APPROVE with nits |
| `transmission-network-use-of-system-tnuos-tariffs` | APPROVE with nits |

No blockers, no majors. Seven nits, all optional.

## Mechanical checks (all pass)

- Build `--only` each lead key: wrote, no errors (`aahedc_tariffs`, `gis_gen_charging_zones_files`,
  `tnuos_tariffs_half_hourly_hh_demand`).
- Detector `[]` on all three built pages.
- Each mirror `cmp`s byte-identical to its canonical note (both sides are CRLF; a `cmp` after CR-strip differs only
  because of that, as the writer said). The vault diff against `origin/master` is only the `page:` block, `updated:`,
  and the two GIS body edits.
- Raw-feed download URLs on each page equal the bronze sidecar `request_url` set exactly (1, 2 and 8 URLs). Each page
  also shows the `package_show` URL. Related links all resolve to pages in the set.
- 390 px: iframe `scrollWidth` = `clientWidth` = 390 on all three; the only elements past 390 are the clipped hero
  SVG paths. 1440, 1024 and 768 screenshots read cleanly (TNUoS at 1440 and GIS at 1024 inspected in full).
- Rendered text: no em or en dashes, no local-data paths, no codes (no GZ1, no hold codes), no planning words.
  AAHEDC and TNUoS are each spelled out in the summary; the title carries the acronym first, as on the approved
  BSUoS page.
- Server on 9871 started with its PID recorded (52278) and stopped by that PID; confirmed down. 9670 untouched.

## 1. The held line

**True of the files.** "NESO dates each publication": every file has a `Published_Date` (AAHEDC dictionary: "Date
when this tariff was published"; TNUoS "Date tariffs were published"). "Not when each row appeared": the column is a
day with no time, and in each family one `last_modified` covers the whole file (the AAHEDC final for 2027 is dated
2026-07-15, the file's own `last_modified` day). "Nor whether old rows change": each note carries the open point that
a published row may be revised in place; only one capture exists per file, so nothing contradicts it.

**Consistent with the ledger and eligibility.** The registry question is "no publication instant; what was available
when; a publication date alone does not establish availability at midnight". The line says the same thing in plain
words and is word for word the approved fixed-BSUoS line. It does not claim the files carry no date at all, which
would have been false.

Extra lines, checked:
- **Demand residual (unmetered band).** Silver has an `Unmetered` band. The dictionary's tariff unit reads "p/kWh for
  sites of unmetered supplies; OR £/site for all other final demand sites" and its description says UMS sites are
  "in p/kWh per day"; the note quotes the final tariff statement (document 376336) as p/kWh/annum in its summary and
  p/kWh in its table. "Its documents give the unmetered band conflicting units" is accurate. The member line "£ per
  site per day except unmetered supplies" matches the dictionary header `£/(Site Day)`.
- **Local circuit (padded names).** Bronze CSV, 4,647 rows: 78 rows with a padded `Substation_Name`, 73 ending in a
  space and 5 in a tab, none padded at the start (293 distinct raw names against 290 trimmed). Silver agrees (78).
  "Some substation names end in spaces or tabs" is true.

Nits:
1. **Held wording differs on two TNUoS members** (`tnuos_tariffs_transmission_demand`,
   `tnuos_tariffs_onshore_local_circuit`). They say "not when rows appeared" where the other six say "not when each row
   appeared", and drop "nor whether old rows change", though the question is the same. The 16-word cap forces a cut;
   a closer fit keeps the first clause identical: "NESO dates each publication but not when each row appeared; the
   unmetered band's units conflict." (15 words) and "...; some substation names end in spaces or tabs." (16 words).
2. **The line leaves out the mixed-stage half of the hold** (how forecast, draft and final rows should be treated).
   The writer flagged this; it is the approved BSUoS trade-off, so no change needed.

## 2. Charging zones

Verified on bronze (both files captured 2026-10-08, `ckan_last_modified` 2022-05-16T15:06:19 and 15:07:09):
- GeoJSON: 28 features. Feature 0 is a `MultiPolygon` with `coordinates: []`, `id` 1, `layer` `GZ1`. The other 27 each
  have one polygon, `id` 1 to 27 and `layer` `GZ1` to `GZ27`, so `id` 1 and `GZ1` appear twice. Properties are exactly
  `id`, `layer`, `path`.
- Shapefile: 28 records (`.dbf` 28); record 1 is shape type 0 (null), the rest type 5; the first two `.dbf` rows are
  both `1` / `GZ1`. Header box minimum y is 0.0 and x spans -6.96 to 1.76, as the note says.
- WGS 84: the `.prj` is `GCS_WGS_1984` with unit Degree; the GeoJSON `crs` is `urn:ogc:def:crs:OGC:1.3:CRS84`. NESO's
  own resource descriptions state no CRS here, but the files do, so "state WGS 84 coordinates in degrees" is correct as
  worded (the files state it, not NESO).
- NESO's text (snapshot of 6 October 2026): 27 generation zones each with a set of zonal tariffs; the count may change;
  boundaries flex when a substation is added; "indicative"; CUSC, tariff reports and charging statements take
  precedence. All four page statements trace to it.

**27 against 28.** The page never says the 28 features are the 27 zones, or that the empty feature explains the gap:
the 27 is dated ("as read in October 2026"), the 28 belongs to files "last modified May 2022", and they sit in
separate sentences. The note body's "no equivalence" bullet is intact and now records the facts above. So the answer
to "does it claim an equivalence" is no.

Nits:
3. **Adjacency invites an inference.** "27 zones ... Both files ... contain 28 features, one with no geometry" lets a
   reader do 27 + 1. The inference happens to match bronze, but the page does not state it, and the empty duplicate
   `GZ1` is not mentioned. If the seat wants zero room for it, cut ", one with no geometry" (the writer's own option,
   56 words). Keeping it is defensible: it is a true, useful file fact.
4. **Second NESO sentence is undated.** "NESO calls them indicative; where they disagree, its charging documents
   prevail" follows the dated "as read in October 2026" sentence but has no date of its own, and "they" can read as
   the boundaries or the documents. Optional: "NESO calls the boundaries indicative; its charging documents prevail
   where the two disagree."

Held line, facts and related links all check out (TNUoS tariffs: Zone_No "Generation Zone 1 - 27"; DNO areas: NESO's
notes point there for the TNUoS demand zone shapefiles; grid supply points and ETYS as other NESO GIS packages).

## 3. AAHEDC tariffs

Silver 9 rows: 6 Final and 3 Draft, financial years 2022 to 2027, 9 distinct on (type, year, date). Columns: total,
Shetland and excluding-Shetland tariffs, unit "Pence per kilowatt hour". Cadence "Every 6 months" and "revenue
team ... forecasted and set" are the catalogue's words. Related TNUoS and BSUoS notes are accurate.

Nit:
5. **`how_used[1]` overstates.** "How far each year's final rate moved from its draft": only 2025, 2026 and 2027
   have a draft; 2022 to 2024 have a final only. Suggest "How far a final rate moved from its draft, where NESO
   published one".

## 4. TNUoS tariffs (family of 8)

Per-member `differs` lines checked against the dictionaries and silver columns: HH (peak, year-round, floored, zone 1
to 14, £ per kW), NHH (zonal, floored, p/kWh), embedded export (locational, AGIC, floored; `PhasedResidual` omitted,
which NESO says no longer applies), TDR (bands, £/(Site Day) except unmetered), onshore generator (zone 1 to 27; peak,
year-round, residual, small-generator discount), offshore (Substation, Circuit, ETUoS = "Embedded Transmission Use of
System Tariff" in the catalogue), local substation (voltage, capacity, "Redundancy of the Substation"; £/kW comes from
the cited tariff statement, since the dictionary unit is empty), local circuit (substation name). All eight have
Forecast, Draft and Final in silver; years 2021 to 2031 except TDR 2024 to 2031 and substation 2027 to 2028.
Cadence "Quarterly" matches the catalogue. The body needed no corrections.

Nits:
6. **Facts `grain` is loose for the local substation table.** Its key is voltage, substation capacity and connection
   type, which is not obviously a "zone, site or band". Low stakes; "zone, site, band or substation type" would be
   exact.
7. **"TNUoS tariffs price use of the GB transmission network"** is the writer's paraphrase (flagged in the report as
   unverified). The note's own definition is cost recovery for owning and operating the network. Consider "TNUoS is
   the charge that recovers the cost of the GB transmission network" if the seat wants the page to follow the note.

## Writer's report

Accurate on every figure I re-measured. One loose phrase: "78 names are padded" is 78 rows (73 + 5), which is how
the note's body states it ("78 cells"); the public page makes no count, so no page effect.

## Defects (gridflow or data)

None new. The registry, sidecars, silver and bronze agree with the pages. The committed `gis-facts.json` records 28
features but not the empty one, as the writer noted (a gap, not an error).
