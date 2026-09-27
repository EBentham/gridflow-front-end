s = open("b_el.py", encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
rep('''       (850, LV["pb"] + 232), (940, S_L - 90), (1010, S_L)]''',
    '''       (850, LV["pb"] + 232), (930, LV["pb"] + 330), (990, S_L - 30), (1016, S_L - 14)]''')
rep('''MIDH = [(-10, LV["ga"] + 110), (120, LV["ga"] + 86), (240, LV["ga"] + 74), (330, LV["ga"] + 66), (470, LV["ga"] + 64),
        (620, LV["ga"] + 70), (720, LV["ga"] + 110), (840, LV["ga"] + 180), (940, S_L - 70), (1010, S_L)]''',
    '''MIDH = [(-10, LV["ga"] + 110), (120, LV["ga"] + 86), (240, LV["ga"] + 74), (330, LV["ga"] + 66), (470, LV["ga"] + 64),
        (620, LV["ga"] + 70), (720, LV["ga"] + 112), (820, LV["ga"] + 200), (910, LV["ga"] + 300), (975, S_L - 30),
        (1004, S_L - 14)]''')
rep('''        (560, LV["de"] + 64), (700, LV["de"] + 58), (840, LV["de"] + 64), (940, LV["de"] + 90), (1000, S_L - 13),
        (W + 20, S_L - 13)]''',
    '''        (560, LV["de"] + 64), (700, LV["de"] + 58), (840, LV["de"] + 64), (926, LV["de"] + 84), (958, LV["de"] + 150),
        (984, S_L - 20), (996, S_L - 12)]''')
rep('''    g.append(band(MTN, -10, 1010, HORIZON, ".5", wob=1.2, jag=True))''',
    '''    g.append(band(MTN, -10, 1016, HORIZON, ".5", wob=1.2, jag=True))''')
rep('''    g.append(band(MIDH, -10, 1010, HORIZON))''', '''    g.append(band(MIDH, -10, 1004, HORIZON))''')
rep('''    xs = frange(-10, W + 20, 4)
    top = " ".join(f"L{f(x)} {f(near_top(x))}" for x in xs)''',
    '''    xs = frange(-10, 996, 4)
    top = " ".join(f"L{f(x)} {f(near_top(x))}" for x in xs)''')
# the sea east of the coast, running on under the index column
rep('''    tl, highest = town(560, near_top)''',
    '''    sea_y = S_L - 14
    sea = f"M960 {f(sea_y)} H{W + 20} V{f(S_L + 12)} H960 Z"
    g.append(f'<path d="{sea}" fill="{HORIZON}"></path><path d="{sea}" fill="{DAY}" opacity=".13"></path>')
    rip = " ".join(f"M{f(x)} {f(sea_y + 5 + (i % 2) * 4)} h{12 + (i % 3) * 8}" for i, x in enumerate(frange(1004, W, 38)))
    g.append(f'<path d="{rip}" stroke="{DAY}" stroke-width="1" opacity=".35"></path>')
    g.append(f'<path d="M{f(xs[-1])} {f(near_top(xs[-1]))} L{f(xs[-1] + 2)} {f(S_L + 12)}" stroke="none"></path>')
    tl, highest = town(560, near_top)''')
open("b_el.py", "w", encoding="utf-8").write(s)
print("ok")
