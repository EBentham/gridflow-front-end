from pathlib import Path

p = Path(__file__).parent / "gen_C.py"
s = p.read_text(encoding="utf-8")
start = s.index("VENDORS = [")
end = s.index("# measure key:")
new = '''VENDORS = [
    # mark, name, keys, count, publishes, four facts, where to reach it
    ("pylon", "Elexon BMRS", ["elexon"], "33 datasets",
     "Great Britain’s balancing-mechanism data: system prices, generation outturn, BM-unit data, and demand and wind "
     "forecasts.",
     [("Market", "GB electricity"), ("Access", "Public, no key"),
      ("Grain", "Half-hourly settlement periods; FUELINST is 5-minute"),
      ("History held", "From September 2021 for six datasets, August 2026 for the rest")],
     "<code>data.elexon.co.uk/bmrs/api/v1</code>, through <code>connectors/elexon/client.py</code>"),
    ("converter", "ENTSO-E Transparency Platform", ["entsoe"], "[n] datasets",
     "European electricity: day-ahead prices, load, generation by type, cross-border flows, outages, capacity, "
     "transmission allocation and balancing. Its GB day-ahead rows are empty; the GB benchmark comes from Elexon MID.",
     [("Market", "EU electricity: GB, FR, NL, BE, DE-LU and IE-SEM"),
      ("Access", "Key <code>ENTSOE_API_KEY</code>, as <code>securityToken</code>"),
      ("Grain", "15-minute or hourly by zone, as XML"),
      ("History held", "From August 2026; the vendor keeps about five years")],
     "<code>web-api.tp.entsoe.eu</code>, through <code>connectors/entsoe/client.py</code>"),
    ("substation", "NESO Data Portal", ["neso_data_portal"], "[n] datasets",
     "The system operator’s open-data catalogue, served as files through CKAN rather than as a query API. gridflow "
     "reads three of its packages.",
     [("Market", "GB electricity, from the system operator"), ("Access", "Public, no key"),
      ("Grain", "Half-hourly; wind availability daily, per BM unit"),
      ("History held", "Generation mix from January 2009; current file only, no backfill")],
     "<code>api.neso.energy</code>, through <code>connectors/neso_data_portal/client.py</code>"),
    ("ccgt", "NESO Carbon Intensity", ["neso"], "[n] datasets, in five families",
     "GB carbon intensity, national and regional, actual and forecast, with statistics, fuel emission factors and the "
     "generation mix.",
     [("Market", "GB electricity carbon intensity"), ("Access", "Public, no key"), ("Grain", "Half-hourly"),
      ("History held", "Short windows, the longest 30 July to 21 September 2026")],
     "<code>api.carbonintensity.org.uk</code>, through <code>connectors/neso/carbon_intensity.py</code>"),
    ("pipeline", "ENTSO-G Transparency Platform", ["entsog"], "[n] datasets",
     "European gas: physical flows, nominations, allocations, capacities, gas quality, congestion outcomes, "
     "interruptions, tariffs, urgent market messages and the reference inventory.",
     [("Market", "EU gas; the UK’s interconnection points by default"), ("Access", "Public, no key"),
      ("Grain", "Daily, by gas day; tariffs and congestion data periodic"),
      ("History held", "From August 2026; tariffs from October 2025")],
     "<code>transparency.entsog.eu/api/v1</code>, through <code>connectors/entsog/client.py</code>"),
    ("tanks", "GIE AGSI+ and ALSI", ["gie_agsi", "gie_alsi"], "[n] datasets",
     "Underground gas storage across Europe, levels and flows (AGSI+), and LNG terminal data (ALSI).",
     [("Market", "Storage in 9 countries, LNG in 8; GB in both"),
      ("Access", "Key <code>GIE_API_KEY</code> in the <code>x-key</code> header, for both"),
      ("Grain", "Daily, by gas day"), ("History held", "From August 2026")],
     "<code>agsi.gie.eu</code> and <code>alsi.gie.eu</code>, through <code>connectors/gie/client.py</code>"),
    ("metmast", "Open-Meteo", ["open_meteo"], "[n] datasets",
     "Weather for GB power modelling: the ERA5 archive and forecasts, at 7 demand cities, 12 wind sites and 6 solar "
     "sites.",
     [("Market", "Weather inputs for GB power"), ("Access", "Public, free tier"), ("Grain", "Hourly"),
      ("History held", "Archive from September 2021; forecasts from August 2026")],
     "<code>archive-api.open-meteo.com/v1</code> and <code>api.open-meteo.com/v1</code>, through "
     "<code>connectors/openmeteo/client.py</code>"),
]

'''
s = s[:start] + new + s[end:]
R = [
    ('''def vendor_entry(v: tuple) -> str:
    kind, name, keys, count, pub, fx, link = v
    ids = " ".join(f"<code>{k}</code>" for k in keys)
    cnt = count.replace("[n]", '<span class="slot">[n]</span>')
    return (f'<li class="ent"><div>{D.mark(kind)}<h3><a href="#">{name}</a></h3><p class="id">{ids}</p>'
            f'<p class="n">{cnt}</p><p class="go"><a class="more" href="#">{link}</a></p></div>'
            f'<div><p class="acc">{pub}</p>{facts(fx)}</div></li>')''',
     '''def vendor_entry(v: tuple) -> str:
    kind, name, keys, count, pub, fx, reach = v
    ids = " ".join(f"<code>{k}</code>" for k in keys)
    cnt = count.replace("[n]", '<span class="slot">[n]</span>')
    return (f'<li class="ent v-ent"><div>{D.mark(kind)}<h3><a href="#">{name}</a></h3><p class="id">{ids}</p>'
            f'<p class="n"><a href="#">{cnt}</a></p></div>'
            f'<div><p class="acc">{pub}</p>{facts(fx, "four")}<p class="reach">Reached at {reach}.</p></div></li>')'''),
    ('''f'<span class="v r">{v}</span></li>' for s, k, d, v in rows)''', '''f'<span class="v">{v}</span></li>' for s, k, d, v in rows)'''),
    ('''    lede = ('gridflow ingests <span class="slot">[N datasets]</span> from seven vendors, across GB and European power, '
            'gas, weather and carbon. Each vendor has a page listing everything gridflow takes from it, and each dataset '
            'has a page of its own.')''',
     '''    lede = ('gridflow ingests <span class="slot">[N datasets]</span> from seven vendors: GB and European power, gas, '
            'weather and carbon. Each vendor’s page lists all it supplies, and each dataset has a page of its own.')'''),
    ('''.key4 .tl li{grid-template-columns:110px 280px minmax(0,1fr) 180px}''',
     '''.key4 .tl li{grid-template-columns:110px 280px 560px minmax(0,1fr)}
.v-ent{padding:24px 0 26px}
.v-ent .mk{margin:0 0 10px}
.v-ent .acc{margin:0 0 14px}
.facts.four{grid-template-columns:repeat(4,minmax(0,1fr));column-gap:28px}
.reach{margin:10px 0 0;font-size:14px;line-height:1.5;color:#3F4A3B}
.reach code{color:#1C2B22;font-size:13.5px}
.ent .n a{text-decoration-color:#66793B}
.ent .slot,.part .slot{color:#1C2B22;font-weight:600}
.band-in .t{justify-self:start}'''),
]
for a, b in R:
    assert a in s, a[:70]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")

c = Path(__file__).parent / "c.css"
t = c.read_text(encoding="utf-8")
t = t.replace("align-items:end;margin-top:72px}", "align-items:end;margin-top:52px}")
t = t.replace(".horizon{display:block;margin:34px -80px 0}", ".horizon{display:block;margin:22px -80px 0}")
c.write_text(t, encoding="utf-8")
print("patched")
