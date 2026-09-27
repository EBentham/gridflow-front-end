from pathlib import Path

p = Path(__file__).parent / "b_ar.py"
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


BED = '''SHADES = ["#9FADAB", "#AAB7B5", "#B6C1BF", "#97A5A3", "#A4B1AF"]


def bed(y: float, name: str, x0: float, x1: float, seed: int, stripes: int = 0, months=("08", "09"),
        h: float = BLOCK_H) -> str:
    """One silver dataset directory as a bed of columnar-jointed rock: each column one daily Parquet file
    (widths vary with file size), a stronger joint between month partitions, and for an append-only dataset
    thin laminae, one per vintage, the newest on top."""
    rng = random.Random(seed)
    top = lambda x: y - h / 2 + 2.2 * math.sin(x / 47 + seed) + 1.2 * math.sin(x / 13 + seed)  # noqa: E731
    bot = lambda x: y + h / 2 + 2.4 * math.sin(x / 53 + seed * 2) + 1.2 * math.sin(x / 17)  # noqa: E731
    out = []
    span = (x1 - x0 - 16 * (len(months) - 1)) / len(months)
    x = x0
    month_joints = []
    for mi, m in enumerate(months):
        start = x
        end = x + span
        while x < end - 4:
            w = min(rng.uniform(11, 21), end - x)
            if end - (x + w) < 9:
                w = end - x
            tilt = rng.uniform(-2.2, 2.2)
            fill = rng.choice(SHADES)
            out.append(f'<path d="M{f(x)} {f(top(x))} L{f(x + w)} {f(top(x + w))} L{f(x + w + tilt)} {f(bot(x + w + tilt))} '
                       f'L{f(x + tilt)} {f(bot(x + tilt))} Z" fill="{fill}" stroke="{SILVER_DEEP}" stroke-width=".7"></path>')
            for _ in range(rng.choice([1, 1, 2])):
                cy = rng.uniform(y - h * .3, y + h * .32)
                out.append(f'<path d="M{f(x + .6)} {f(cy)} L{f(x + w - .6)} {f(cy + rng.uniform(-2.5, 2.5))}" '
                           f'stroke="{SILVER_DEEP}" stroke-width=".6" opacity=".6"></path>')
            x += w
        out.append(f'<text class="mono sm" x="{f(start)}" y="{f(bot(start) + 17)}">month={m}/</text>')
        if mi < len(months) - 1:
            month_joints.append(x + 8)
            x += 16
    if stripes:
        lam = h / (stripes + .5)
        for k in range(stripes):
            y0 = y - h / 2 + 4 + k * lam
            pts = [(xx, y0 + 1.5 * math.sin(xx / 61 + k)) for xx in range(int(x0), int(x1) + 1, 20)]
            d = smooth(pts)
            if k == 0:
                band_d = d + " L" + smooth([(xx, yy + lam * .6) for xx, yy in reversed(pts)])[1:] + " Z"
                out.append(f'<path d="{band_d}" fill="{DAY}" opacity=".75"></path>')
            out.append(f'<path d="{d}" stroke="{INK}" stroke-width=".6" fill="none" opacity=".55"></path>')
    for jx in month_joints:
        out.append(f'<path d="M{f(jx)} {f(top(jx) - 8)} L{f(jx + 1)} {f(bot(jx) + 8)}" stroke="{INK}" stroke-width="1.1" '
                   f'stroke-dasharray="3 3"></path>')
    xs = list(frange(x0, x1, 8))
    outline = ("M" + " L".join(f"{f(xx)} {f(top(xx))}" for xx in xs) + " L" +
               " L".join(f"{f(xx)} {f(bot(xx))}" for xx in reversed(xs)) + " Z")
    out.append(f'<path d="{outline}" fill="none" stroke="{INK}" stroke-width="1.1"></path>')
    out.insert(0, f'<text class="mono" x="{f(x0)}" y="{f(top(x0) - 10)}">{name}</text>')
    return "".join(out)


'''

VEIN = '''def vein(pts: list[tuple[float, float]], w0: float, w1: float, seed: int = 0) -> str:
    """A vein: an irregular intrusion that thins towards its tip (the first point) and thickens in gold."""
    rng = random.Random(seed)
    samples = []
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        for t in (0, .25, .5, .75):
            samples.append((xa + (xb - xa) * t, ya + (yb - ya) * t))
    samples.append(pts[-1])
    left, right = [], []
    n = len(samples)
    for i, (x, y) in enumerate(samples):
        j = min(i + 1, n - 1)
        k = max(i - 1, 0)
        dx, dy = samples[j][0] - samples[k][0], samples[j][1] - samples[k][1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        wv = (w0 + (w1 - w0) * i / (n - 1)) * (1 + .22 * math.sin(i * 1.7 + seed)) / 2
        left.append((x + nx * wv, y + ny * wv))
        right.append((x - nx * wv, y - ny * wv))
    poly = smooth(left) + " L" + smooth(list(reversed(right)))[1:] + " Z"
    out = []
    for i in range(3, n - 2, 5):
        x, y = samples[i]
        ang = rng.uniform(-2.6, -.5) if rng.random() < .5 else rng.uniform(.5, 2.6)
        ln = rng.uniform(10, 18)
        br = (f"M{f(x)} {f(y)} q{f(math.cos(ang) * ln * .5)} {f(math.sin(ang) * ln * .7)} "
              f"{f(math.cos(ang) * ln)} {f(math.sin(ang) * ln)}")
        out.append(f'<path d="{br}" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"></path>'
                   f'<path d="{br}" stroke="{GOLD}" stroke-width="1.6" fill="none" stroke-linecap="round"></path>')
    out.append(f'<path d="{poly}" fill="{GOLD}" stroke="{INK}" stroke-width="1.1" stroke-linejoin="round"></path>')
    out.append(f'<path d="{smooth(pts)}" stroke="{GOLD_DEEP}" stroke-width=".8" fill="none" stroke-dasharray="1.5 4" '
               f'opacity=".6"></path>')
    return "".join(out)


'''

DRAW = '''    # silver: one columnar bed per dataset directory
    g.append(bed(ROW["A"], "elexon/fuelhh/", 250, 962, 1))
    g.append(bed(ROW["B"], "elexon/system_prices/", 250, 962, 2, stripes=4))
    g.append(bed(ROW["C"], "neso/carbon_intensity/", 250, 962, 3))
    g.append(bed(ROW["D"], "elexon/mid/", 250, 962, 4))
    bx0, bx1 = 250, 962
    by = ROW["C"] + BLOCK_H / 2 + 28
    g.append(f'<path d="M{bx0} {f(by - 7)} V{f(by)} H{f(bx1)} V{f(by - 7)} M606 {f(by)} V{f(by + 7)}" '
             f'stroke="{INK}" stroke-width="1.3" fill="none"></path>')
    labels.append(f'<text class="mono sm" x="616" y="{f(by + 18)}">silver_neso_carbon_intensity</text>')

    # gold: two of the SQL views drawn as veins rising into the beds they read; the model outputs as ingots
    jx, jy = 842, L["sq"]
    g.append(vein([(452, ROW["B"] + BLOCK_H / 2 - 4), (446, ROW["C"] + 6), (470, ROW["D"] - 20), (500, ROW["D"] + 40),
                   (570, C_G + 36), (680, jy - 34), (jx, jy)], 2.5, 12, 1))
    g.append(vein([(690, ROW["C"] + BLOCK_H / 2 - 4), (700, ROW["D"] + 10), (730, C_G + 24), (790, jy - 22), (jx, jy)],
                  2.5, 10, 2))
    g.append(vein([(jx - 2, jy), (900, jy + 4), (968, jy + 2)], 13, 11, 3))
    g.append(vein([(330, ROW["D"] + BLOCK_H / 2 - 4), (334, C_G + 20), (300, C_G + 90), (250, C_G + 150)], 2.5, 11, 4))
    labels.append(f'<text class="mono sm" x="{jx - 10}" y="{f(jy + 32)}" text-anchor="end">gold_uk_imbalance_context</text>')
    labels.append(f'<text class="mono sm" x="120" y="{f(C_G + 178)}">gold_gb_day_ahead_benchmark</text>')
    for x, name, n in [(200, "forecasts/", 6), (380, "forecast_metrics/", 4), (560, "stack_clearing/", 5),
                       (740, "stack_residual_demand/", 3), (918, "stack_supply_curve_points/", 6)]:
        g.append(pile(x, L["mo"], n))
        labels.append(f'<text class="mono sm" x="{x}" y="{f(L["mo"] + 38)}" text-anchor="middle">{name}</text>')

'''

a = s.index("def row(y: float, name: str")
b = s.index("def vein(")
s = s[:a] + BED + s[b:]
a = s.index("def vein(")
b = s.index("def ingot(")
s = s[:a] + VEIN + s[b:]
a = s.index("    # silver: rows of Parquet blocks")
b = s.index("    g.append(f'<g font-family=\"Hanken Grotesk\" font-style=\"italic\"")
s = s[:a] + DRAW + s[b:]
rep('ROW = {"A": L["fi"], "B": L["vi"], "C": L["vw"] - 64, "D": L["vw"] + 64}',
    'ROW = {"A": L["fi"], "B": L["vi"], "C": L["vw"] - 66, "D": L["vw"] + 62}')
rep("    rows = [(0, 3), (1, 2), (2, 1)]\n", "    rows = [(0, 3), (1, 2), (2, 1)] if n > 3 else [(0, 2), (1, 1)]\n")
rep("vintages, NESO carbon intensity and ENTSO-E day-ahead prices)", "vintages, NESO carbon intensity and Elexon MID)")
rep('join in gold as one view. At the bottom, gold ingots lie in piles for forecasts, forecast metrics and stack "\n'
    '            "clearing.")',
    'join in gold as one view; a second vein rises into the MID row. At the bottom, gold ingots lie in five "\n'
    '            "piles, one per model-output table.")')
p.write_text(s, encoding="utf-8")
print("ok")
