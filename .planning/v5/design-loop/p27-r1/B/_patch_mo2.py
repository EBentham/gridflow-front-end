from pathlib import Path

p = Path(__file__).parent / "b_mo.py"
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('''# terraces (x0, x1, tread y): the merit order, cheapest lowest; the first four hold water
TER = [(-20, 214, SM + 86), (214, 356, SM + 60), (356, 494, SM + 34), (494, 640, SM), (640, 728, SM - 74),
       (728, 806, SM - 168), (806, 1460, TOP_Y)]
WET = 4''',
    '''# terraces (x0, x1, tread y): the merit order, cheapest lowest. The wet ones run up to the marginal terrace,
# whose water sits at SM; the dry tail steepens to the plateau, which runs on under the index.
_XS = [-20, 110, 196, 272, 340, 404, 466, 528, 594, 650, 704, 756, 806]
_YS = [SM + 92, SM + 80, SM + 68, SM + 56, SM + 44, SM + 30, SM + 15, SM, SM - 28, SM - 66, SM - 122, SM - 206]
TER = [(a, b, y) for a, b, y in zip(_XS, _XS[1:], _YS)] + [(806, 1460, TOP_Y)]
WET = 8''')

# mid ridge: a smooth shoulder, the field following it; no hedgerows
a = s.index("    mid = [(-20, wi + 170)")
b = s.index("    # the terraced hillside in front")
s = s[:a] + '''    bench = [(600, so + 16), (660, so + 20), (720, so + 22), (770, so + 26)]
    mid = [(-20, wi + 170), (110, wi + 112), (240, wi + 78), (380, wi + 70), (500, wi + 86), (556, so - 6)] + bench + \\
        [(800, so + 60), (812, TOP_Y + 16)]
    g.append(f'<path d="{ridge(mid, S)}" fill="{HORIZON}"></path>')
    crest = lambda x: wi + 72 + 9 * ((x - 380) / 130) ** 2  # noqa: E731
    for i, tx in enumerate([232, 296, 360, 424, 488]):
        base = crest(tx) + 3
        h = base - wi
        g.append(turbine(tx, base, h, h * .5, ["sp1", "sp2", "sp3"][i % 3], 25 * i + 10))
    # the energised field on the bench, and the panel rows standing in it
    top = smooth(mid[5:11])
    under = smooth([(x, y + 20) for x, y in reversed(mid[5:11])])
    g.append(f'<path d="{top} L{under[1:]} Z" fill="{CHART}"></path>')
    g.append(f'<path d="{top}" stroke="{OLIVE}" stroke-width="1" fill="none"></path>')
    g.append(solar_rows(616, 772, lambda x: so + 18, rows=((0.84, 22), (0.92, 11), (1.0, 0))))

    # a transmission line from the gas plant, up the flank and over towards the city
    pyl = [(628, SM - 104, .46), (500, SM - 200, .38), (400, SM - 290, .31), (318, SM - 370, .25),
           (250, SM - 436, .2), (196, SM - 490, .16)]
    wires = []
    for (xa, ya, sa), (xb, yb, sb) in zip(pyl, pyl[1:]):
        wires.append(spans(tips(xa, ya, sa, -1), tips(xb, yb, sb, 1), 6 * sa))
    g.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.2">'
             + "".join(pylon(x, y, sc_) for x, y, sc_ in pyl) + "</g>")
    g.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".7" fill="none" opacity=".8"></path>')
    PYL0[:] = [pyl[0]]

''' + s[b:]

# plant on the dry tail
a = s.index("    # the dearer terraces carry plant")
b = s.index("    # residual demand: the span of the fill")
s = s[:a] + '''    # the dry tail carries plant: a gas station on the first dry terrace, small peaking units above
    t = TER[WET]
    cx, cy = t[0] + 16, t[2] - TREAD + 3
    g.append(f'<g transform="translate({f(cx)} {f(cy)}) scale(.5) translate({f(-cx)} {f(-cy)})">{ccgt(cx, cy, 1.0)}</g>')
    px, py, ps = PYL0[0]
    g.append(f'<path d="{spans([(cx + 62 * .5, cy - 18)] * 3, tips(px, py, ps, 1), 4)}" stroke="{INK}" '
             f'stroke-width=".7" fill="none" opacity=".8"></path>')
    for k in (WET + 1, WET + 2, WET + 3):
        t = TER[k]
        for ux in (t[0] + 10, t[0] + 30):
            yb = t[2] - TREAD + 3
            g.append(f'<rect x="{f(ux)}" y="{f(yb - 10)}" width="14" height="10" fill="{DAY}" stroke="{INK}" '
                     f'stroke-width=".9"></rect><rect x="{f(ux + 9)}" y="{f(yb - 19)}" width="3.2" height="9" '
                     f'fill="{CLAY}" stroke="{INK}" stroke-width=".8"></rect>')

''' + s[b:]
rep("from b_base import (CHART,", "from b_base import (CHART, pylon, spans, tips,")
rep('''TREAD = 18                       # the tread's visible depth''',
    '''TREAD = 18                       # the tread's visible depth
PYL0: list[tuple[float, float, float]] = []''')
rep('''            "from left to right, the cheapest lowest, each terrace divided by stakes into plots, with gas plant on "
            "the dearer terraces. Water has been let into the four lowest terraces, from the bottom up; a "''',
    '''            "from left to right, the cheapest lowest, each terrace divided by stakes into plots, with gas plant on "
            "the dearer terraces and a line of pylons climbing towards the city. Water has been let into the "
            "lowest terraces, from the bottom up; a "''')
rep('"turbines. On the nearest hill, rows of solar panels.', '"turbines, and on its shoulder rows of solar panels.')
p.write_text(s, encoding="utf-8")
print("ok")
