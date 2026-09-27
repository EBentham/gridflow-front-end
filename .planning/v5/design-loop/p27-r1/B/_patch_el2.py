s = open("b_el.py", encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
rep('HERO_TOP, HERO_H = 100, 300', 'HERO_TOP, HERO_H = 100, 330')
# a jagged mountain line: peaks and saddles joined by near-straight flanks, with the dam across one saddle
a = s.index("MTN = [")
b = s.index("MIDH = [")
s = s[:a] + '''MTN = [(-10, LV["pb"] + 8), (40, LV["pb"] - 30), (92, LV["pb"] - 12), (150, LV["pb"] - 58), (196, LV["pb"] - 4),
       (214, LV["pb"] + 2), (236, LV["pb"] + 2), (254, LV["pb"] - 6), (300, LV["pb"] - 50), (356, LV["pb"] - 22),
       (412, LV["pb"] - 44), (480, LV["pb"] + 4), (560, LV["pb"] + 30), (640, LV["pb"] + 84), (740, LV["pb"] + 150),
       (850, LV["pb"] + 232), (940, S_L - 90), (1010, S_L)]
''' + s[b:]
rep('''def band(pts: list[tuple[float, float]], a: float, b: float, fill: str, op: str = "1", wob: float = 3) -> str:
    xs = frange(a, b, 4)
    top = " ".join(f"L{f(x)} {f(interp(pts, x) + wob * math.sin(x / 37 + len(pts)) + wob * .4 * math.sin(x / 11))}"
                   for x in xs)''',
'''def lin(pts: list[tuple[float, float]], x: float) -> float:
    for (a, ya), (b, yb) in zip(pts, pts[1:]):
        if a <= x <= b:
            t = (x - a) / (b - a)
            return ya + (yb - ya) * (t + .12 * math.sin(math.pi * t))
    return pts[-1][1]


def band(pts: list[tuple[float, float]], a: float, b: float, fill: str, op: str = "1", wob: float = 3,
         jag: bool = False) -> str:
    xs = frange(a, b, 4)
    fn = lin if jag else interp
    top = " ".join(f"L{f(x)} {f(fn(pts, x) + wob * math.sin(x / 37 + len(pts)) + wob * .4 * math.sin(x / 11))}"
                   for x in xs)''')
rep('g.append(band(MTN, -10, 1010, HORIZON, ".5", wob=5))', 'g.append(band(MTN, -10, 1010, HORIZON, ".5", wob=1.2, jag=True))')
# the reservoir: water behind a dam across the saddle between two shoulders
a = s.index("def reservoir() -> str:")
b = s.index("def nuclear(")
s = s[:a] + '''def reservoir() -> str:
    """Pumped storage: a dam across the saddle between two shoulders, its reservoir level just under the crest,
    and a penstock down the mountain face to the power house."""
    y = LV["pb"]
    water = (f'<path d="M190 {f(y - 5)} L262 {f(y - 5)} L258 {f(y - 1)} L194 {f(y - 1)} Z" fill="{HORIZON}"></path>'
             f'<path d="M198 {f(y - 3)} h14 M222 {f(y - 3)} h20" stroke="{DAY}" stroke-width=".8" opacity=".5"></path>')
    dam = (f'<path d="M206 {f(y - 1)} L250 {f(y - 1)} L258 {f(y + 20)} L198 {f(y + 20)} Z" fill="{DAY}" '
           f'stroke="{INK}" stroke-width="1"></path>'
           f'<path d="M204 {f(y + 6)} H252 M202 {f(y + 13)} H255" stroke="{INK}" stroke-width=".6" opacity=".45"></path>'
           f'<path d="M204 {f(y - 1)} H252" stroke="{INK}" stroke-width="1.6"></path>')
    ph_x, ph_y = 300, LV["ga"] + 46
    pen = (f'<path d="M232 {f(y + 20)} C244 {f(y + 70)} 272 {f(ph_y - 80)} {ph_x} {f(ph_y - 14)} '
           f'M236 {f(y + 20)} C248 {f(y + 70)} 276 {f(ph_y - 80)} {ph_x + 4} {f(ph_y - 14)}" stroke="{DAY}" '
           f'stroke-width="1.1" fill="none" opacity=".85"></path>')
    house = (f'<rect x="{ph_x - 10}" y="{f(ph_y - 14)}" width="28" height="14" fill="{DAY}" stroke="{INK}" '
             f'stroke-width=".9"></rect><path d="M{ph_x - 12} {f(ph_y - 14)} H{ph_x + 20}" stroke="{INK}" '
             f'stroke-width="1.6"></path>')
    return water + pen + dam + house


''' + s[b:]
# drop the separate foreground rise: the grid supply point and notice board stand on the near field
a = s.index("    # the foreground rise at the cut")
b = s.index("    gsp_x = 520")
s = s[:a] + '''    bounds = [smooth([(x, near_top(x) + (prof(x) - near_top(x)) * k) for x in frange(-10, 1000, 26)])
              for k in (.38, .7)]
    g.append(f'<path d="{" ".join(bounds)}" stroke="{OLIVE}" stroke-width="1" fill="none" opacity=".42"></path>')
''' + s[b:]
rep('gsp_base = fore_top(560) + 2', 'gsp_base = LV["rm"] + 52')
rep('g.append(noticeboard(438, fore_top(460) + 2, LV["rm"]))', 'g.append(noticeboard(438, LV["rm"] + 50, LV["rm"]))')
rep('lab("notice board", 460, fore_top(460) + 20, INK)', 'lab("notice board", 460, LV["rm"] + 68, INK)')
rep('lab("pumped storage", 150, LV["pb"] + 32, LAB_P, "start")', 'lab("pumped storage", 312, LV["pb"] + 40, LAB_P, "start")')
rep('''INDEX_D = {
    "pb": "What balancing cost each half-hour: system prices, bids and offers accepted, notifications.",
    "ga": "Outturn by fuel type, wind and solar actuals, the wind forecast and availability ahead.",
    "si": "The state of the whole system: frequency, margin, imbalance and loss-of-load probability.",
    "de": "National and transmission demand, as outturn and as forecasts up to 14 days ahead.",
    "rm": "The register of every BM unit, and REMIT messages on outages and unavailability.",
}''', '''INDEX_D = {
    "pb": "What balancing cost each half-hour: prices, and the bids and offers accepted.",
    "ga": "Outturn by fuel type, wind and solar actuals, and availability days ahead.",
    "si": "Frequency, margin, imbalance and loss-of-load probability, system-wide.",
    "de": "National and transmission demand: outturn, and forecasts to 14 days out.",
    "rm": "The register of every BM unit, and REMIT messages on outages.",
}''')
rep('.hero-l .lead{margin:22px 0 0;font-size:21px;line-height:1.5;color:#F6F4EC;max-width:36ch}',
    '.hero-l .lead{margin:20px 0 0;font-size:21px;line-height:1.5;color:#F6F4EC;max-width:40ch}')
open("b_el.py", "w", encoding="utf-8").write(s)
print("ok")
