s = open("b_el.py", encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
rep('''    for i, x in enumerate([372, 432, 492, 552, 612, 672]):
        h = 64 - (i % 2) * 4
        base = interp(MIDH, x) + 3 * math.sin(x / 37 + len(MIDH)) + 1.2 * math.sin(x / 11) + 2
        g.append(turbine(x, LV["ga"] + h + .1 * h / 80, h, h * .5, ["sp1", "sp2", "sp3"][i % 3], 22 * i + 5)
                 if abs(base - (LV["ga"] + h)) < 30 else "")''',
'''    for i, x in enumerate([372, 432, 492, 552, 612, 672]):
        base = interp(MIDH, x) + 3 * math.sin(x / 37 + len(MIDH)) + 1.2 * math.sin(x / 11) + 3
        h = (base - LV["ga"]) / (1 + .1 / 80)
        g.append(turbine(x, base, h, 31, ["sp1", "sp2", "sp3"][i % 3], 22 * i + 5))''')
rep('''<p>Grouped as the drawing is. Most datasets are queried by publish time; the store holds five years of '
           f'the six with history back to September 2021.</p>''',
    '''<p>Grouped as in the drawing above. Six datasets reach back to September 2021 in the store; most of '
           f'the rest start in August 2026.</p>''')
rep('    lab("town", 690, highest - 12, INK) if False else None\n', '')
open("b_el.py", "w", encoding="utf-8").write(s)
