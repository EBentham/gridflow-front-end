s = open("b_ds.py", encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:60], s.count(a))
    s = s.replace(a, b)

rep('LV["eg"] = S_L + 76            # the pipeline, trenched into the North Sea bed',
    'LV["eg"] = S_L + 56            # the pipeline, trenched into the North Sea bed')
rep('LV["gie"] = LV["eg"] + SP + 4  # the storage caverns in the salt',
    'LV["gie"] = LV["eg"] + SP + 20  # the storage caverns in the salt')
rep('PLATE_H = LV["gie"] + 120', 'PLATE_H = LV["gie"] + 104')
rep('SEAS = [(0, 44), (176, 224), (646, 792)]          # Atlantic, Irish Sea, North Sea: x ranges of open water',
    'SEAS = [(178, 222), (646, 796)]                   # Irish Sea, North Sea: x ranges of open water')
# full-width ridges, descending to the flat Continent before the index column
rep('''FAR = [(-10, S_L - 96), (70, S_L - 150), (150, S_L - 136), (230, LV["dp"] + 150), (300, LV["dp"] + 66),
       (376, LV["dp"] + 50), (446, LV["dp"] + 46), (516, LV["dp"] + 52), (590, LV["dp"] + 104),
       (680, LV["dp"] + 196), (780, LV["dp"] + 270), (880, S_L - 110), (950, S_L - 44), (1000, S_L)]
MID = [(196, S_L), (250, LV["ci"] + 190), (300, LV["ci"] + 106), (360, LV["ci"] + 92), (430, LV["ci"] + 100),
       (500, LV["ci"] + 132), (570, LV["ci"] + 200), (640, S_L - 60), (700, S_L)]''',
'''FAR = [(-10, LV["dp"] + 250), (110, LV["dp"] + 190), (250, LV["dp"] + 96), (376, LV["dp"] + 50),
       (470, LV["dp"] + 46), (560, LV["dp"] + 70), (690, LV["dp"] + 150), (820, LV["dp"] + 250),
       (930, LV["dp"] + 350), (1000, S_L - 40), (1030, S_L)]
MID = [(-10, LV["ci"] + 224), (120, LV["ci"] + 190), (240, LV["ci"] + 120), (330, LV["ci"] + 90),
       (420, LV["ci"] + 98), (520, LV["ci"] + 140), (640, LV["ci"] + 196), (780, LV["ci"] + 240),
       (900, LV["ci"] + 290), (970, S_L - 30), (1010, S_L)]''')
rep('NEAR_IE = [(44, S_L - 6), (70, S_L - 24), (140, S_L - 30), (176, S_L - 6)]',
    'NEAR_IE = [(-10, S_L - 34), (60, S_L - 40), (140, S_L - 28), (178, S_L - 6)]')
rep('NEAR_GB = [(224, S_L - 6),', 'NEAR_GB = [(222, S_L - 6),')
rep('NEAR_EU = [(792, S_L - 6),', 'NEAR_EU = [(796, S_L - 6),')
rep('''            if a == 0:
                return S_L + 34 + 3 * math.sin(x / 9)
            t = (x - a) / (b - a)
            depth = 30 if a == 176 else NS_DEPTH
            return S_L + 6 + depth * math.sin(math.pi * t) ** .5 + 2 * math.sin(x / 13)''',
'''            t = (x - a) / (b - a)
            depth = 20 if a == 178 else NS_DEPTH
            return S_L + 4 + depth * math.sin(math.pi * t) ** .28 + 1.5 * math.sin(x / 13)''')
rep('g.append(poly(FAR, -10, 1000, HORIZON, ".5"))', 'g.append(poly(FAR, -10, 1030, HORIZON, ".5"))')
rep('''    g.append(turbine(70, interp(FAR, 70) + 2, 30, 15, "sp2", 40))
    g.append(turbine(112, interp(FAR, 112) + 2, 28, 14, "sp3", 80))''',
'''    for x, h, sp in [(86, 30, "sp2"), (128, 28, "sp3"), (170, 30, "sp1")]:
        g.append(turbine(x, interp(FAR, x) + 2 * math.sin(x / 31) + 2, h, h * .5, sp, x % 90))''')
rep('g.append(poly(MID, 196, 700, HORIZON))', 'g.append(poly(MID, -10, 1010, HORIZON))')
# salt: one continuous bed under the whole section and the index column
rep('''    top = [(330, gy + 6), (400, gy - 20), (470, gy - 44), (540, gy - 50), (610, gy - 44), (690, gy - 30),
           (760, gy - 38), (850, gy - 52), (920, gy - 46), (980, gy - 20), (1004, gy + 2)]
    bot = [(1004, gy + 4), (980, gy + 30), (920, gy + 44), (850, gy + 48), (760, gy + 42), (690, gy + 40),
           (610, gy + 44), (540, gy + 44), (470, gy + 36), (400, gy + 20), (330, gy + 8)]
    sd = smooth(top) + " L" + smooth(bot)[1:] + " Z"''',
'''    top = [(x, gy - 40 - 14 * math.exp(-((x - 548) / 70) ** 2) - 18 * math.exp(-((x - 876) / 80) ** 2)
            + 4 * math.sin(x / 57)) for x in range(-40, W + 41, 24)]
    bot = [(x, gy + 70 + 6 * math.sin(x / 90 + 1) + 3 * math.sin(x / 31)) for x in range(W + 40, -41, -24)]
    sd = smooth(top) + " L" + smooth(bot)[1:] + " Z"''')
rep('''    for cx, w, h in [(528, 22, 66), (566, 18, 58), (838, 24, 72), (880, 20, 64), (920, 17, 54)]:
        g.append(cavern(cx, gy + 2, w, h))''',
'''    for cx, w, h in [(530, 22, 70), (568, 18, 60), (840, 24, 76), (882, 20, 66), (922, 17, 56)]:
        g.append(cavern(cx, gy + 2, w, h))''')
rep('''    pipe = ([(tb_x + 14, tb_base - 2), (tb_x + 30, S_L + 16), (624, S_L + 30)] +
            [(x, seabed(x) + 8) for x in frange(660, 780, 12)] +
            [(812, S_L + 30), (850, S_L + 14), (et_x + 12, et_base - 2)])''',
'''    pipe = ([(tb_x + 14, tb_base - 2), (tb_x + 40, S_L + 12), (610, S_L + 26), (640, S_L + 36)] +
            [(x, seabed(x) + 8) for x in frange(664, 780, 12)] +
            [(802, S_L + 36), (834, S_L + 24), (858, S_L + 10), (et_x + 12, et_base - 2)])''')
rep('''    cable = ([(cv_x + 30, cv_base - 2), (cv_x + 40, S_L + 12), (640, S_L + 18)] +
             [(x, seabed(x) - 3) for x in frange(662, 778, 12)] + [(800, S_L + 16), (ce_x + 24, ce_base - 2)])''',
'''    cable = ([(cv_x + 30, cv_base - 2), (cv_x + 44, S_L + 8), (632, S_L + 16), (650, seabed(650) - 2)] +
             [(x, seabed(x) - 3) for x in frange(664, 780, 12)] + [(794, seabed(794) - 2), (806, S_L + 12),
                                                                  (ce_x + 24, ce_base - 2)])''')
rep('lab("wind and sunlight", 520, LV["om"] - 40, LAB_P)', 'lab("weather", 520, LV["om"] - 38, LAB_P)')
rep('lab("Ireland", 110, S_L - 8, INK)', 'lab("Ireland", 100, S_L - 9, INK)')
rep('lab("the Continent", 858, S_L - 8, INK)', 'lab("the Continent", 1000, S_L - 1, INK)')
rep('lab("North Sea", 719, SEA_Y + 22, LAB_P)', 'lab("North Sea", 721, SEA_Y + 17, LAB_P)')
rep('lab("interconnector", 719, seabed(719) - 10, LAB_P)', 'lab("interconnector", 721, seabed(721) - 8, LAB_P)')
rep('lab("gas pipeline", 719, LV["eg"] + 26, INK)', 'lab("gas pipeline", 721, LV["eg"] + 24, INK)')
rep('lab("salt, with gas storage caverns", 700, gy + 5, INK)', 'lab("salt, with gas storage caverns", 720, gy + 5, INK)')
rep('d="The GB balancing mechanism: prices, outturn, BM units, demand and wind forecasts."',
    'd="The GB balancing mechanism: prices, outturn, BM units and forecasts."')
rep("The drawing cuts across the system from the Atlantic to the Continent.",
    "The drawing cuts across the system from Ireland to the Continent.")
rep('aria = ("A section through the energy system from the Atlantic, across Ireland, the Irish Sea',
    'aria = ("A section through the energy system from Ireland, across the Irish Sea')
open("b_ds.py", "w", encoding="utf-8").write(s)
print("ok")
