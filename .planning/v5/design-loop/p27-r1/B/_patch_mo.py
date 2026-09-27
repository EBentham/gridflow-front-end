from pathlib import Path

p = Path(__file__).parent / "b_mo.py"
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('''L["wi"] = L["de"] + 206          # turbine hubs: wind
L["so"] = L["wi"] + 180          # panel rows: solar
L["st"] = L["so"] + 180          # the top terrace wall: the stack
L["rd"] = L["st"] + 196          # the fill's span: residual demand
L["sm"] = L["rd"] + 130          # the water level on the marginal terrace: SMP''',
    '''L["wi"] = L["de"] + 192          # turbine hubs: wind (spacing = measured entry height + 26)
L["so"] = L["wi"] + 191          # panel rows: solar
L["st"] = L["so"] + 200          # the top terrace wall: the stack (the plateau edge runs between)
L["rd"] = L["st"] + 194          # the fill's span: residual demand
L["sm"] = L["rd"] + 112          # the water level on the marginal terrace: SMP''')
rep("GOLD_H = 1790", "GOLD_H = 1930")
rep("TREAD = 14 ", "TREAD = 18 ")
rep('det.append(f\'<path d="{tread}" fill="#8FC0C4"></path>\')', 'det.append(f\'<path d="{tread}" fill="#86BCC2"></path>\')')

# ---- the sky: far ridge with the city, the wind ridge with a solar bench on its shoulder, hedgerows
a = s.index("    # far ridge: the city on its crest")
b = s.index("    # the terraced hillside in front")
s = s[:a] + '''    # far ridge: the city on its crest, falling away east behind the plateau
    de = L["de"]
    far = [(-20, de + 50), (80, de + 38), (240, de + 32), (420, de + 34), (560, de + 46), (660, de + 120),
           (740, de + 300), (800, TOP_Y + 30)]
    g.append(f'<path d="{ridge(far, S)}" fill="#2E7682"></path>')
    cg = lambda x: de + 36 + 3 * math.sin(x / 90)  # noqa: E731
    g.append(city(92, cg))

    # the wind ridge; its eastern shoulder is a bench of solar rows
    wi, so = L["wi"], L["so"]
    mid = [(-20, wi + 170), (110, wi + 112), (240, wi + 78), (380, wi + 70), (500, wi + 84), (580, so + 6),
           (650, so + 22), (760, so + 24), (812, TOP_Y + 16)]
    g.append(f'<path d="{ridge(mid, S)}" fill="{HORIZON}"></path>')
    crest = lambda x: wi + 72 + 9 * ((x - 380) / 130) ** 2  # noqa: E731
    for i, tx in enumerate([232, 296, 360, 424, 488]):
        base = crest(tx) + 3
        h = base - wi
        g.append(turbine(tx, base, h, h * .5, ["sp1", "sp2", "sp3"][i % 3], 25 * i + 10))
    # the energised field under the panels
    fld = [(598, so + 16), (650, so + 24), (760, so + 26), (790, so + 40)]
    g.append(f'<path d="{smooth(fld)} L{f(800)} {f(so + 64)} L{f(590)} {f(so + 40)} Z" fill="{CHART}"></path>')
    g.append(solar_rows(620, 770, lambda x: so + 24 + 3 * math.sin(x / 40), rows=((0.82, 22), (0.91, 11), (1.0, 0))))
    # hedgerows and trees on the ridge's west flank: a drawn texture, nothing keyed
    rng = random.Random(5)
    hed = []
    for k, (ya, yb, xe) in enumerate([(wi + 150, wi + 120, 300), (wi + 210, wi + 170, 420), (wi + 280, wi + 230, 520),
                                      (wi + 360, wi + 300, 560), (wi + 450, wi + 380, 540)]):
        pts = [(-20, ya), (xe * .5, (ya + yb) / 2 + 6), (xe, yb)]
        hed.append(f'<path d="{smooth(pts)}" stroke="#2E7682" stroke-width="1.6" fill="none" '
                   f'stroke-linecap="round"></path>')
        for _ in range(4 + k):
            t = rng.uniform(.05, .95)
            x = -20 + t * (xe + 20)
            y = ya + (yb - ya) * t + 6 * math.sin(t * math.pi) - 3
            r = rng.uniform(4, 7)
            hed.append(f'<circle cx="{f(x)}" cy="{f(y - r * .6)}" r="{f(r)}" fill="#2E7682"></circle>')
    g.append("".join(hed))

''' + s[b:]

# the dimension line reads on the teal ridge in day colour
rep('''    g.append(f'<path d="M{x0} {f(TER[0][2] - TREAD - 4)} V{f(y - 9)} M{f(x1)} {f(SM - TREAD - 4)} V{f(y - 9)}" '
             f'stroke="{INK}" stroke-width="1" stroke-dasharray="2 3"></path>')
    g.append(f'<path d="M{x0} {f(y)} H{f(x1)} M{x0} {f(y - 7)} V{f(y + 7)} M{f(x1)} {f(y - 7)} V{f(y + 7)}" '
             f'stroke="{INK}" stroke-width="1.6"></path>')
    g.append(f'<path d="M{x0 + 10} {f(y - 4)} L{x0 + 1} {f(y)} L{x0 + 10} {f(y + 4)} M{f(x1 - 10)} {f(y - 4)} '
             f'L{f(x1 - 1)} {f(y)} L{f(x1 - 10)} {f(y + 4)}" stroke="{INK}" stroke-width="1.6" fill="none"></path>')''',
    '''    g.append(f'<path d="M{x0} {f(TER[0][2] - TREAD - 4)} V{f(y + 9)} M{f(x1)} {f(SM - TREAD - 4)} V{f(y + 9)}" '
             f'stroke="{DAY}" stroke-width="1" stroke-dasharray="2 3"></path>')
    g.append(f'<path d="M{x0} {f(y)} H{f(x1)} M{x0} {f(y - 7)} V{f(y + 7)} M{f(x1)} {f(y - 7)} V{f(y + 7)}" '
             f'stroke="{DAY}" stroke-width="1.6"></path>')
    g.append(f'<path d="M{x0 + 10} {f(y - 4)} L{x0 + 1} {f(y)} L{x0 + 10} {f(y + 4)} M{f(x1 - 10)} {f(y - 4)} '
             f'L{f(x1 - 1)} {f(y)} L{f(x1 - 10)} {f(y + 4)}" stroke="{DAY}" stroke-width="1.6" fill="none"></path>')''')

# shorter entries
rep('''             d="GB national demand outturn (<code>elexon/indo</code>), half-hourly, 24 hours ahead. LightGBM quantile "
               "regression; v2 adds weather and calendar.",''',
    '''             d="GB national demand outturn (<code>elexon/indo</code>), half-hourly, 24 hours ahead; v2 adds weather "
               "and calendar.",''')
rep('''             d="Constructive, with no training step: units from <code>bmunits_reference</code> ranked by short-run "
               "marginal cost, availability from REMIT, a floor at −500 £/MWh.",''',
    '''             d="Constructive, with no training step: units from <code>bmunits_reference</code> ranked by short-run "
               "marginal cost, down to a floor of −500 £/MWh.",''')

# the notebook: shorter comments so nothing clips
a = s.index('NB = """')
b = s.index('def deep()')
s = s[:a] + '''NB = """<span class="c">from</span> gridflow_models <span class="c">import</span> setup_notebook
data, models, common = setup_notebook()

models.list()                        <span class="k"># id, family, version, status</span>
models.demand_forecast.predict(...)  <span class="k"># also train, validate</span>
models.stack.build(as_of)
models.stack.clear(as_of, demand_mw)
models.fundamentals_smp.backtest(...)
data.gb_day_ahead_benchmark(start, end)"""


''' + s[b:]
p.write_text(s, encoding="utf-8")
print("ok")
