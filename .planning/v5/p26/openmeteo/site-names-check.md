# Weather-map site names: check against sources

Checked 2026-10-07. The names come from `SITE_NAMES` in `src/gridflow_front_end/map_svg.py`. The coordinates come from gridflow `src/gridflow/connectors/openmeteo/endpoints.py`. Distances are haversine, from the configured point to the published centroid or turbine position named in the note. This was a read-only check: no code or data was changed.

**Scope.** The brief expected about eight names. `SITE_NAMES` has 9 unverified wind names and 6 solar names, so all 15 were checked. The 3 names already verified and the 7 demand cities are listed for completeness.

**Result.** All 15 names are spelled correctly; no name needs changing. One coordinate is wrong: `triton_knoll`. Its point sits about 28 km west of the Triton Knoll array, and the Humber Gateway wind farm is nearer.

## Wind

| Slug | Display name | Verdict | Source | Coordinate note |
|---|---|---|---|---|
| dogger_bank | Dogger Bank | OK | Operator: https://doggerbank.com/ ("Dogger Bank Wind Farm", phases A/B/C). Positions: thewindpower.net, https://www.thewindpower.net/windfarm_en_10776_dogger-bank-a.php | (54.95, 1.95) lies inside the zone, between Dogger Bank B (54.980, 1.680; 17.6 km) and Dogger Bank A (54.770, 1.910; 20.2 km). The name is the project-family name, which suits a zone point. |
| hornsea | Hornsea | OK | Operator: Ørsted, https://orsted.com/en/media/newsroom/news/2022/08/20220831559011 ("Hornsea 1", "Hornsea 2", "the Hornsea zone"). Position: Wikipedia, https://en.wikipedia.org/wiki/Hornsea_Wind_Farm | 0.6 km from the published centroid (53.885, 1.791). A family/zone name; Ørsted writes the projects as "Hornsea 1/2/3". |
| east_anglia | East Anglia | OK | Operator: ScottishPower Renewables, https://www.scottishpowerrenewables.com/pages/east_anglia_one_background.aspx ("East Anglia ONE", "East Anglia THREE"). Positions: thewindpower.net (EA ONE, EA ONE North, EA THREE) | (52.50, 2.50) is a mid-zone point, not on a built array. East Anglia ONE North (consented, unbuilt; 52.37, 2.42) is 15.4 km away; East Anglia ONE (operating; 52.23, 2.48) is 30.1 km; East Anglia THREE (52.70, 2.86) is 33.0 km. No other wind farm is nearer. A family name: the operator capitalises the project numbers ("ONE", "THREE"), which doesn't affect the bare "East Anglia". |
| triton_knoll | Triton Knoll | OK (name). **COORDINATE FLAG** | Operator: RWE, https://www.tritonknoll.co.uk/ ("Triton Knoll Offshore Wind Farm", "20 miles off the coast of Lincolnshire"). Position: 4C Offshore, https://www.tgs4c.com/windfarms/triton-knoll-united-kingdom-uk30.html (lat 53.47846), and thewindpower.net, https://www.thewindpower.net/windfarm_en_16751_triton-knoll-wind-farm.php (53°28'44.3"N 0°50'13.1"E) | The configured point (53.45, 0.42) is **27.8 km west** of the array (53.478, 0.837), in open water about 17 km off Donna Nook. The nearest wind farm is **Humber Gateway** (53.644, 0.293; Wikipedia), 23.1 km away, so the point is closer to a different farm than to Triton Knoll. One web-search summary also gave 53.2123, 0.8616, which disagrees on latitude. Two sources (4C Offshore and thewindpower.net) agree on 53.48. Either way the array is about 0.84 E, at least 28 km east of the configured 0.42 E, so the flag stands. That is about two ERA5 0.25° cells off. The label is right, but the point does not sit on the farm. The fix belongs in gridflow (`WIND_LOCATIONS` to about 53.48, 0.84) and would change the bronze series, so it is out of scope for this site-only check. |
| walney | Walney | OK | Operator: Ørsted, https://orsted.co.uk/energy-solutions/offshore-wind/our-wind-farms/walney-extension. Position: Wikipedia, https://en.wikipedia.org/wiki/Walney_Wind_Farm | 0.5 km from the Walney 1/2 centroid (54.044, -3.522). Walney Extension lies just west. A family name covering Walney 1, 2 and Extension. |
| beatrice | Beatrice | OK | Operator: https://beatricewind.com/ ("BEATRICE", "Beatrice Offshore Windfarm Ltd"). Turbine positions: BOWL Weekly Notice of Operations, Rev 17, 4 Sep 2017 (operator PDF, text extracted and checked), https://beatricewind.com/_files/ugd/22cf9a_c1d8c058f4e24a749030b47f2a6338c1.pdf | 1.3 km from turbine BE-E9 (58°15.817'N 2°54.665'W) and 2.8 km from BE-D8. The point is outside the Moray East boundary, whose western edge is about 4–5 km east at that latitude (corners from Moray East documents). Wikipedia's infobox point (58.13, -3.07; 17.9 km away) is the old Beatrice oil-field and demonstrator area, not the 588 MW array, so it is not a fair test. |
| seagreen | Seagreen | OK | Operator: https://www.seagreenwindenergy.com/ ("Seagreen", "Seagreen Offshore Wind Farm", "around 27km from the coast of Angus"). Positions: Global Energy Monitor (56.6355, -1.9266) and Wikipedia, https://en.wikipedia.org/wiki/Seagreen_Offshore_Wind_Farm (56.588, -1.741) | 5.1 km from the Global Energy Monitor point and 11.6 km from the Wikipedia point. Inch Cape and Neart na Gaoithe are further south-west, so Seagreen is the nearest farm. |
| highland_central | Central Highlands | OK (region label, not an operator name) | Global Energy Monitor: https://www.gem.wiki/Dunmaglass_wind_farm (57.2515, -4.2558), https://www.gem.wiki/Farr_wind_farm (57.3339, -4.1030) | (57.20, -4.40) is in the Monadhliath wind-farm cluster south-east of Loch Ness. The nearest named farm is Dunmaglass (SSE, 10.4 km); Stronelairg and Farr are nearby. A region descriptor, so the operator-spelling test does not apply. If the owner prefers a named site, "Monadhliath" is the most precise geographic label, but nothing requires a change. |
| whitelee | Whitelee | OK | Operator: ScottishPower Renewables, https://www.scottishpowerrenewables.com ("Whitelee Windfarm", one word). Position: Wikipedia, https://en.wikipedia.org/wiki/Whitelee_Wind_Farm (55.6728, -4.2856) | 2.1 km from the centroid. Note on house style: ScottishPower writes "Whitelee Windfarm", one word. The bare "Whitelee" avoids the question and is correct. |
| gwynt_y_mor | Gwynt y Môr | OK (pre-verified) | Not rechecked | Not rechecked. |
| pen_y_cymoedd | Pen y Cymoedd | OK (pre-verified) | Not rechecked | Not rechecked. |
| borders_crystalrig | Crystal Rig | OK (pre-verified) | Not rechecked | Not rechecked. |

## Solar

Solar sites are capacity-weighted regional points (ADR-020), not named farms, so the operator-spelling test does not apply. A row is OK if the point falls inside the named region. Each point was reverse-geocoded with OpenStreetMap Nominatim (`https://nominatim.openstreetmap.org/reverse?format=json&lat=<lat>&lon=<lon>&zoom=10`).

| Slug | Display name | Verdict | Source | Coordinate note |
|---|---|---|---|---|
| east_anglia_norfolk | Norfolk | OK (region label) | Nominatim (52.62, 1.05) | "South Norfolk, Norfolk". |
| wiltshire_somerset | Wiltshire and Somerset | OK (region label) | Nominatim (51.20, -2.50) | Falls in **Somerset** (Mendip, near Shepton Mallet), about 15 km west of the Wiltshire border. The label names a two-county cluster, so it is acceptable, but the point is not in Wiltshire. |
| kent | Kent | OK (region label) | Nominatim (51.20, 0.70) | "Ashford, Kent". |
| cornwall | Cornwall | OK (region label) | Nominatim (50.30, -5.00) | "Kernow / Cornwall", near Truro. |
| sussex | Sussex | OK (region label) | Nominatim (50.95, -0.10) | "Lewes, East Sussex", close to the West Sussex border. The bare "Sussex" covers both counties. |
| oxfordshire | Oxfordshire | OK (region label) | Nominatim (51.75, -1.25) | "Oxford, Oxfordshire", the city centre. |

## Demand cities (low priority)

All seven coordinates are standard city-centre points (London 51.5074, -0.1278; Birmingham; Manchester; Leeds; Glasgow; Cardiff; Belfast) and all names are spelled correctly. One point to note: **Belfast** is in Northern Ireland, which is on the all-island Single Electricity Market, not the GB grid. That is fine because the map says "UK and Ireland". However, if any page copy describes the demand set as GB demand weather, Belfast doesn't fit that description. This is a copy check only, not a name change.

## Follow-up (not done here; read-only task)

- `triton_knoll` coordinate: the change is in gridflow `WIND_LOCATIONS`, moving to about (53.48, 0.84), and needs a re-fetch of the bronze series. This should be logged to the gridflow BACKLOG and the vault remediation page, following the defect-logging convention.
