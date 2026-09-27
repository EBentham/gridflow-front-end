from __future__ import annotations

from pathlib import Path

p = Path(__file__).with_name("gen_d.py")
s = p.read_text(encoding="utf-8")
R = [
    # one-liners at two lines
    ('''        one=("Half-hourly GB generation outturn in MW: one value per settlement period for each of Elexon’s fuel-type "
             "codes, interconnectors and pumped storage included."),''',
     '''        one="Half-hourly GB generation outturn in MW: one value per settlement period for each Elexon fuel-type code.",'''),
    ('''        one=("The register of Balancing Mechanism units: id, name, fuel type, registered capacity, lead party and GSP "
             "group, held as one snapshot with no time axis."),''',
     '''        one=("The register of Balancing Mechanism units (id, name, fuel type, capacity, lead party, GSP group), held as "
             "one snapshot."),'''),
    # fuelhh what-it-is, one line shorter
    ('''            ("What it is", "<p>Elexon’s outturn by fuel type. Each half-hour settlement period has one row per "
             "fuel-type code, in MW. The codes mix plant types (CCGT, NUCLEAR, WIND, BIOMASS) with pumped storage (PS) "
             "and ten interconnectors (INT*). The week queried here is 336 half-hours of 20 codes: 6,720 rows.</p>"),''',
     '''            ("What it is", "<p>Elexon’s outturn by fuel type: each half-hour settlement period has one row per "
             "fuel-type code, in MW. The codes mix plant types (CCGT, NUCLEAR, WIND) with pumped storage (PS) and ten "
             "interconnectors (INT*). The week queried here is 336 half-hours of 20 codes: 6,720 rows.</p>"),'''),
    # URLs broken at their parameters
    ('''"GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH?publishDateTimeFrom=<UTC Z>"
                 "&publishDateTimeTo=<UTC Z>&page=<n>"''',
     '''"GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH\\n"
                 "    ?publishDateTimeFrom=<UTC Z>&publishDateTimeTo=<UTC Z>&page=<n>"'''),
    ('''"GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/"
                 "{YYYY-MM-DD}?page=<n>"''',
     '''"GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/{YYYY-MM-DD}\\n"
                 "    ?page=<n>"'''),
    ('''"GET https://transparency.entsog.eu/api/v1/operationalData?limit=-1&timeZone=UCT"
                 "&from=YYYY-MM-DD&to=YYYY-MM-DD&indicator=Physical%20Flow&periodType=day"''',
     '''"GET https://transparency.entsog.eu/api/v1/operationalData\\n"
                 "    ?limit=-1&timeZone=UCT&from=YYYY-MM-DD&to=YYYY-MM-DD\\n"
                 "    &indicator=Physical%20Flow&periodType=day"'''),
    ('.in.wrap{white-space:pre-wrap;word-break:break-all}\n', ''),
    ('''<pre class="in wrap">''', '''<pre class="in">'''),
    # footer: the deep stratum carries granite marks, as on the homepage
    ('''def footer(H: int) -> str:
    edge = [(x, 26 + 9 * math.sin(x / 140 + 1) + 6 * math.sin(x / 53 + 2) + 4 * math.sin(x / 19))
            for x in range(-40, W + 41, 20)]
    d = smooth(edge)
    svg = (f'<svg class="edge" width="{W}" height="52" viewBox="0 0 {W} 52" aria-hidden="true">'
           f'<rect x="0" y="0" width="{W}" height="52" fill="{DAY}"></rect>'
           f'<path d="{d} L{W + 40} 60 L-40 60 Z" fill="{PETROL}"></path>'
           f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path></svg>')''',
     '''FOOT_H = 212


def footer(H: int) -> str:
    edge = [(x, 26 + 9 * math.sin(x / 140 + 1) + 6 * math.sin(x / 53 + 2) + 4 * math.sin(x / 19))
            for x in range(-40, W + 41, 20)]
    d = smooth(edge) + f" L{W + 40} {FOOT_H + 4} L-40 {FOOT_H + 4} Z"
    gran = (f'<pattern id="p-granite" width="46" height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 '
            f'M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1">'
            f'</path></pattern>')
    svg = (f'<svg class="edge" width="{W}" height="{FOOT_H}" viewBox="0 0 {W} {FOOT_H}" aria-hidden="true">'
           f'<defs>{gran}</defs><rect x="0" y="0" width="{W}" height="{FOOT_H}" fill="{DAY}"></rect>'
           f'<path d="{d}" fill="{PETROL}"></path><path d="{d}" fill="url(#p-granite)" opacity=".5"></path>'
           f'<path d="{smooth(edge)}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path></svg>')'''),
    ('''.deep{position:relative;background:#155A6E;color:#F6F4EC}
.edge{display:block}
.deep-in{display:flex;justify-content:space-between;align-items:center;padding:30px 80px 56px}''',
     '''.deep{position:relative;height:212px;color:#F6F4EC}
.edge{position:absolute;left:0;top:0;display:block}
.deep-in{position:relative;display:flex;justify-content:space-between;align-items:center;padding:84px 80px 0}'''),
]
for a, b in R:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
print("patched", len(R))
