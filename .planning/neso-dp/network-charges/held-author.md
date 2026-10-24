# Held Network charges pages: writer report (2026-10-24)

I wrote three held pages in the author brief's held mode (ruling 6). None has a chart, frame or notebook, and no
artefacts were made. Each `page:` block is on the canonical note in
`C:\gridflow-wt\vault-neso-nc\30-vendors\neso-data-portal\datasets\` and is copied byte for byte to
`C:\gridflow-wt\fe-neso-nc\vault\neso_data_portal\` (`cmp` clean on all three after the last edit). `updated:` is now
2026-10-24 on all three.

**Line endings.** The three vault notes are CRLF in the working tree (every line; `core.autocrlf` true, index LF). The
Edit tool kept CRLF. `git diff --stat` in the vault worktree shows only my lines (139 insertions, 5 deletions), with no
whole-file rewrite. The front-end mirror carries `text eol=lf`, so git warns "CRLF will be replaced by LF" on the mirror
copies; its diff is the same 139/5. (An earlier count of mine wrongly read 0 CR; `tr -cd '\r' | wc -c` gives CR =
lines.)

| Page | Build `--only` | Detector | Content model |
|---|---|---|---|
| `aahedc-tariffs` | `neso_data_portal/aahedc_tariffs`: wrote, no errors | `[]` | `parse_page_fields` and `anatomy_errors`: `[]`; `what_it_is` 60 words |
| `gis-boundaries-for-gb-generation-charging-zones` | `neso_data_portal/gis_gen_charging_zones_files`: wrote, no errors | `[]` | `[]`; `what_it_is` 59 |
| `transmission-network-use-of-system-tnuos-tariffs` (family, `held: true`) | `neso_data_portal/tnuos_tariffs_half_hourly_hh_demand`: wrote, no errors | `[]` | `[]`; `what_it_is` 60 |

Rendered text of all three, checked by script:
- 0 em or en dashes, arrows or middle dots.
- None of live, now, real-time, yet, soon, pending, planned, shipped, coming, locally, ruling, ledger, TODO, RULINGS,
  E-SEM, held, our, "since 20xx", or digits followed by rows or days. One "hold" ("hold 28 features") was changed to
  "contain".
- The viewport meta and `<main>` are present.
- There is one "Rows not shown" block per page, listing every table with its reason.

**Screenshots.** Light mode at 1440, 1024 and 768, and at 390 through a 390 px iframe (whole page, plus 1,400 px
sections for reading). They are in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\nc-held-writer\shots\`.
I read the TNUoS page at 1440 and 390, the charging zones and AAHEDC at 390:
- Nothing is clipped or overlapping.
- The eight member keys in the TNUoS hero wrap, as do the request URLs and command lines.

**Server.** Started twice from Bash on 9861 with `python -m http.server ... & echo $!` (PIDs 50967, then 51070). Each
was stopped by that PID and confirmed down; 9670 was not touched. I did not check dark mode, because headless flags do
not switch the palette.

## Shared evidence

| Claim | Evidence |
|---|---|
| Upload files: one `package_show` per command, then each file downloaded whole unless `last_modified` is unchanged | gridflow `connectors/neso_data_portal/client.py` `iter_members` (lines 1658-1780). The `frozen` refresh only gates datastore dumps, so it does not affect these uploads. |
| One dataset per command; `--last 24h` form | `cli.py` `ingest`/`transform` (lines 186-300); same form as the approved held pages |
| Request URLs | bronze sidecar `request_url` of each 2026-10-08 capture (one capture per family; there are no later captures) |
| Vendor wording (notes, descriptions, update frequency) | catalogue snapshot `.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json` (gridflow repo) |
| Hold questions | registry `record.eligibility.question` of each family; ledger rows 71, 72 and 127; `docs/neso_data_portal/eligibility.md` lines 30, 184 and 308-315 |
| Related targets exist | all are in the `groups` of `site/hifi/data/neso_data_portal.json`; the build resolved them |

## Shared held line (AAHEDC and six TNUoS tables)

"NESO dates each publication but not when each row appeared, nor whether old rows change." (15 words)

- This is word for word the approved `bsuos-fixed-tariffs` held line. That page's hold has the same substance: no issue
  instant behind the published date, and no proof that old rows are unchanged.
- It is used unchanged on AAHEDC and on six TNUoS tables, as the batch file asks.
- Source: the registry question ("no publication instant; what was available when ...; a publication date alone does not
  establish availability at midnight") and each note's "What is not established" ("nor is it shown that an old row is
  never rewritten in place").
- Measured on silver: each row carries only a `published_date` (a day). HH demand, for example, holds 43 distinct
  (stage, year, date) groups. These include up to five Forecast publication dates per financial year, from 2020-08-31
  to 2026-05-11, all in one file last modified 2026-05-12. The file itself shows nothing about when each row reached the
  portal.

The two TNUoS tables whose hold question adds a second question keep the same first clause, shortened to fit 16 words:
- **`tnuos_tariffs_transmission_demand`:** "NESO dates each publication, not when rows appeared; its documents give the
  unmetered band conflicting units." (16 words) This is the registry's second question, TDR-UNMETERED-UNIT: the
  dictionary says p/kWh per day; the final tariff statement says p/kWh/annum in its summary and p/kWh in its table.
- **`tnuos_tariffs_onshore_local_circuit`:** "NESO dates each publication, not when rows appeared; some substation names end
  in spaces or tabs." (16 words) This is the registry's padded-name question. Measured on silver: 78 names are padded,
  73 ending in a space and 5 in a tab, with none padded at the start.

## 1. AAHEDC tariffs (`aahedc_tariffs`, one-table held page)

| Claim | Evidence |
|---|---|
| Name spelled out once (summary) | package title |
| Draft and Final stages only; three tariff columns in pence per kWh | silver `publication_type` = {Draft, Final}; vendor dictionary unit "Pence per kilowatt hour" (note "Units") |
| Financial year runs April to March and is named by its ending year | dictionary example "2024 for financial year 2023/24" (note) |
| "the date NESO published them" | dictionary: "Date when this tariff was published" |
| Revenue team forecasts and sets the tariffs | package notes ("forecasted and set by the revenue team at National Grid ESO") |
| Every 6 months; updated when tariffs are published | extras "Update frequency: Every 6 months"; notes "bi annual (when tariffs are published)" |
| Grain: one financial year's tariffs at one stage, with its published date | entity key (stage, year, published date); 9 of 9 distinct |
| Related: TNUoS "forecast and set by the same NESO team" | both packages' notes name the revenue team |
| Related: BSUoS fixed "also published by stage with a publication date" | approved BSUoS page grain and summary |

Body corrections: none. I re-checked the note's counts (9 rows; 6 Final, 3 Draft), its vintage (2026-07-15) and its
"every financial year starts on or before the vintage" (the latest, FY 2027, starts 2026-04-01). All hold.

## 2. TNUoS generation charging zones (`gis_gen_charging_zones_files`, one-table held page)

**Held line (16 words):** "Two map files, kept whole; gridflow reads no rows from them and builds no silver table." This
follows the ETYS precedent ("One zipped shapefile, kept whole; ..."). The package is eligible; it ships held only because
it has no silver table (seat, PROXY-SOURCED).

| Claim | Evidence |
|---|---|
| 27 zones, each with its own tariffs; the count may change; boundaries shift as substations are added; indicative; the CUSC, tariff reports and charging statements prevail | package notes. On the page these are "NESO's notes, as read in October 2026" (the snapshot of 6 October). This follows the SOP checker's advice to say "as read" rather than give the snapshot date as NESO's. |
| Both files last modified 16 May 2022 | sidecar `ckan_last_modified` `2022-05-16T15:06:19` and `15:07:09`, the same as the snapshot |
| 28 features in each file, one with no geometry | measured on bronze (2026-10-24): GeoJSON feature 0 is a `MultiPolygon` with no coordinates; shapefile record 1 is shape type 0 (null). The other 27 have one polygon each. |
| `id`, `layer` and `path` attributes | GeoJSON properties and the note's facts table |
| "state WGS 84 coordinates in degrees" | **stated by the files**: the `.prj` is `GEOGCS["GCS_WGS_1984", ... UNIT["Degree", ...]]`; the GeoJSON `crs` is `urn:ogc:def:crs:OGC:1.3:CRS84`. The batch rule cuts coordinate-system wording unless the file states it, and here it does. |
| Ad hoc | extras "Update frequency: Ad hoc" |
| Related: DNO licence areas "NESO points to for TNUoS demand zone maps" | package notes: "For the TNUoS demand zones shapefiles, please refer to ... gis-boundaries-for-gb-dno-license-areas" |
| Related: TNUoS onshore generator tariffs "for each generation zone" | dictionary `Zone_No` "Generation Zone 1 - 27" (TNUoS note) |

**27 against 28, no equivalence claimed.** `what_it_is` gives NESO's 27 (as read in October 2026), then the files' 28
features, one empty (May 2022), in separate sentences with no link between them. `grain` gives the 28 only.

**Body corrections** (both measured on the 2026-10-08 bronze, 2026-10-24):
- **The 27-against-28 bullet.** It now records that in both files the first feature has no geometry and carries `id` 1
  and `layer` `GZ1`, so `id` 1 appears twice. The other 27 are `id` 1 to 27 and `GZ1` to `GZ27`. The `TODO: verify` is
  narrowed to why the empty feature is there, and a sentence says what the site page states.
- **The shapefile header's minimum y of 0.0.** It is now noted as consistent with the null first record counted at
  (0, 0), whose x range already spans 0. This is marked "consistent, not proven", and the header is still recorded as
  published.

## 3. TNUoS tariffs (family of 8, lead `tnuos_tariffs_half_hourly_hh_demand`, `held: true`)

The members are in page-set order. Each has one request (its sidecar `request_url`) and a held line (above). There is no
top-level `raw_feed.requests`, as on the Pathfinder page: the template does not render them on family pages.

| Member | `differs` | Evidence |
|---|---|---|
| HH demand | zone 1 to 14: peak, year-round and floored tariffs, £/kW | dictionary "Demand Zones 1 - 14"; columns Peak, YearRound, HHTariff(Floored) "£ per kW" (the small-generator adjustment is left out for length) |
| NHH demand | zone 1 to 14: zonal and floored, p/kWh | columns `NHH_Zonal`, `NHHTariff(Floored)`, "Pence per kWh" |
| Embedded export | by demand zone: locational, avoided GSP infrastructure and floored, £/kW | dictionary "Demand (Embedded Export) Zones 1 - 14"; AGIC = Avoided GSP Infrastructure Costs (resource description) |
| TDR | by band, £ per site per day except unmetered supplies | dictionary unit "p/kWh for sites of unmetered supplies; OR £/site for all other final demand sites", description "TDR tariffs per day" |
| Onshore generator | zone 1 to 27: peak, year-round, residual and small-generator discount, £/kW | dictionary "Generation Zone 1 - 27"; columns and "£ per kW" |
| Local offshore generator | each generator's local substation, circuit and embedded transmission tariffs, £/kW | resource description (Substation, Circuit, ETUoS); dictionary "£/kW" |
| Local substation | generators' tariff by voltage, substation capacity and redundancy, £/kW | resource description ("tariffs for the Generators"); dictionary "Capacity of the Substations", "Redundancy of the Substation"; £/kW from NESO's statement (document 367801, cited in the note) |
| Onshore local circuit | by named substation, £/kW | key `substation_name`; "£ per kW" |

| Page claim | Evidence |
|---|---|
| Name spelled out once (summary) | package title |
| Revenue team forecasts and sets them | package notes |
| Quarterly; updated when tariffs are published | extras "Update Frequency: Quarterly"; notes |
| Each row is one stage (forecast, draft or final) of a financial year's tariffs, with its publication date | every family's key starts (publication, year_fy, published_date); all eight have all three stages in silver |
| "Follow NESO's forecasts for one charging year from release to final tariff" | several Forecast publication dates per year in each file (HH demand: FY 2026 has five Forecast dates, then Draft and Final) |
| Related: AAHEDC, BSUoS fixed, charging zones, DNO areas | as above |

Body corrections: none. The note's per-family counts, year ranges and stage sets match silver: years 2021 to 2031 (TDR
2024 to 2031, substation 2027 to 2028); every family has Draft, Final and Forecast.

## Unverified

- **Charging zones:** why the empty feature exists. No vendor statement was found. The page states it as a file fact
  only.
- **TNUoS:** "price use of the GB transmission network by generation and demand" paraphrases the package name and the
  generation and demand split of the files. NESO's catalogue text does not define TNUoS.
- **AAHEDC:** who pays the charge. The page does not say; the note's TODO stays.

## Open questions for the seat

1. **Shared held line.** I reused the approved BSUoS fixed-tariffs wording rather than inventing a third phrasing, so
   all three tariff packages read the same. If the seat wants AAHEDC and TNUoS to name the mixed stages too, the
   16-word cap leaves no room for both.
2. **The empty feature on the page.** "28 features, one with no geometry" is true of both files and useful to anyone
   loading them. It sits beside NESO's 27 without linking them, but a reader may infer the link. If the seat reads the
   batch rule strictly, cut ", one with no geometry" from `what_it_is` (it would then be 56 words).
3. **Transform commands on held tables.** As on the SOP and BSUoS fixed pages, AAHEDC and TNUoS show `transform` as well
   as `ingest`. Silver exists for all nine tables.

## Template problems

None new. The family page lists the eight members' files in the raw feed and prints each reason under "Rows not shown".
The member list in the raw feed does not repeat the reasons, which matches the Pathfinder page.

## Defects

- **NESO, GIS Boundaries for GB Generation Charging Zones (files last modified 2022-05-16):** the first feature in both
  files has no geometry: an empty `MultiPolygon` in the GeoJSON, a null shape (type 0) in the shapefile. It carries
  `id` 1 and `layer` `GZ1`, so `id` 1 appears twice. This is probably why the files hold 28 features against NESO's 27
  zones, and why the shapefile header's minimum y is 0.0. The `path` attribute holds the author's local paths
  (`C:/Temp/MyQGISFiles/...`).
- **NESO, same package notes:** the DNO licence-area cross-reference still points at the old
  `api.nationalgrideso.com` host.
- **NESO, TNUoS (already in the note, still present in the 2026-10-08 capture):**
  - the TDR header is double-encoded (`TDR Tariff in Â£/(Site Day)`);
  - 78 local-circuit substation names are padded (73 with a trailing space, 5 with a tab);
  - `Published_Date` in the local-circuit file mixes `DD/MM/YYYY` and `YYYY/MM/DD`;
  - 161 wholly blank rows (offshore generator 113, local substation 48);
  - the unmetered TDR band's unit conflicts between the dictionary and the tariff statement.
- **gridflow:** none. The registry, sidecars, silver, connector and committed GIS facts agree with the bronze. The
  committed `gis-facts.json` records 28 features but not the empty one; this is a gap, not an error.
- **Manifest:** the leads and members are right: `aahedc_tariffs`; `gis_gen_charging_zones_files`; the TNUoS family's
  eight members in page-set order, led by `tnuos_tariffs_half_hourly_hh_demand`. `package_tables` has no TNUoS entry,
  which is right for a family page.
- **For the seat (not a defect):** `C:\gridflow-wt\vault-neso-nc`'s DNO licence-area note differs from the front-end
  mirror in line endings only (CRLF working tree against the mirror's LF). The content is identical with CRs stripped.
