from __future__ import annotations

from pathlib import Path

p = Path(__file__).parent / "gen_e.py"
s = p.read_text(encoding="utf-8")


def rep(a: str, b: str, cnt: int = 1) -> None:
    global s
    n = s.count(a)
    assert n == cnt, (n, a[:90])
    s = s.replace(a, b)


# BM units: labels either side of the bar, more room for the enlarged bars
rep('    by, bh = 34, 26\n', '    by, bh = 26, 24\n')
rep('''        f'<text x="{f(xt + 10)}" y="{by - 12}"><tspan class="nm">2,515</tspan><tspan class="an" dx="5">with no fuel type '
        f'(null)</tspan></text>',''',
    '''        f'<text x="{PR}" y="{by - 10}" text-anchor="end"><tspan class="nm">2,515</tspan><tspan class="an" dx="5">with '
        f'no fuel type (null)</tspan></text>',''')
rep('''        f'<text x="{PL}" y="{by - 12}"><tspan class="nm">499</tspan>''',
    '''        f'<text x="{PL}" y="{by - 10}"><tspan class="nm">499</tspan>''')
rep('''        f'<text x="{LX + 12}" y="{by + 20}"><tspan class="nm">3,014</tspan>''',
    '''        f'<text x="{LX + 12}" y="{by + 17}"><tspan class="nm">3,014</tspan>''')
rep('    top = 92\n    pitch, h = 15, 10\n', '    top = 76\n    pitch, h = 16.2, 11\n')
rep('''    labs.append(f'<text x="{LX + 12}" y="{top + 9.5}"><tspan class="an">the 499, by code</tspan></text>')
    labs.append(f'<text x="{LX + 12}" y="{top + 27}"><tspan class="an">INT* is ten codes</tspan></text>')''',
    '''    labs.append(f'<text x="{LX + 12}" y="{top + 9}"><tspan class="an">the 499, by code;</tspan></text>')
    labs.append(f'<text x="{LX + 12}" y="{top + 26}"><tspan class="an">INT* is ten codes</tspan></text>')''')
rep("labs.append(t_text(cx0 + v * kc + 7, y + 9, str(v), \"start\"))",
    "labs.append(t_text(cx0 + v * kc + 7, y + 9.5, str(v), \"start\"))")
rep("labs.append(f'<text class=\"cd\" x=\"{cx0 - 10}\" y=\"{f(y + 9)}\" text-anchor=\"end\">{esc(code)}</text>')",
    "labs.append(f'<text class=\"cd\" x=\"{cx0 - 10}\" y=\"{f(y + 9.5)}\" text-anchor=\"end\">{esc(code)}</text>')")

# ENTSOG endpoint: break the query string so it stays inside the margin
rep('''"GET https://transparency.entsog.eu/api/v1/operationalData\\n    ?limit=-1&"
                                         "timeZone=UCT&from=YYYY-MM-DD&to=YYYY-MM-DD&indicator=Physical%20Flow&periodType=day",''',
    '''"GET https://transparency.entsog.eu/api/v1/operationalData\\n    ?limit=-1&"
                                         "timeZone=UCT&from=YYYY-MM-DD&to=YYYY-MM-DD\\n    &indicator=Physical%20Flow"
                                         "&periodType=day",''')

# captions to two lines
rep('''        cap=(f'{code("entsog/physical_flows")} silver, GWh/d, every gas day held locally (1 to 5 August, 13 to 21 '
             'September 2026). One native value a gas day as National Gas TSO reports it; nothing averaged or '
             'interpolated, and the line breaks where there are no rows.'),''',
    '''        cap=(f'{code("entsog/physical_flows")} silver, GWh/d, every gas day held locally. One native value a gas day '
             'as National Gas TSO reports it; nothing averaged or interpolated, and the line breaks where there are no '
             'rows.'),''')
rep('''        cap=(f'{code("elexon/bmunits_reference")} silver, count of BM units, snapshot of 26 September 2026. No time '
             'axis, so the figure shows what the registry holds: all 3,014 units to scale, then the 499 with a fuel type '
             'by code. Counts only; capacities are not additive.'),''',
    '''        cap=(f'{code("elexon/bmunits_reference")} silver, count of BM units, snapshot of 26 September 2026. No time '
             'axis: all 3,014 units to scale, then the 499 with a fuel type by code. Counts only; capacities are not '
             'additive.'),''')
p.write_text(s, encoding="utf-8")
print("patched")
