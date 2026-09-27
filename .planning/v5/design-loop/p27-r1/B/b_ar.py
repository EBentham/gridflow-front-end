"""B-architecture: the store as a cutaway. Vendor cables come down from the strip into bronze, which is drawn as
daily beds (the newest on top) holding response bodies and their sidecars; silver is rows of columnar Parquet
blocks, one row per dataset directory, one of them striped with vintages; gold holds the SQL views as veins that
rise into silver, and the model outputs as ingots. Every path and view name sits in the keyed index."""
from __future__ import annotations

import math
import random

from b_base import (CLAY, DAY, GOLD, GOLD_DEEP, INK, INK2, OLIVE, PETROL, SILVER, SILVER_DEEP, T_SILVER, W, bg_layer,
                    emit, f, footer, frange, index_list, mark_svg, masthead, page, smooth, strata, wave, wbr)
from b_strip import cable, ring, strip

# ---------------------------------------------------------------- geometry (plate-local unless noted)
HERO_TOP, HERO_H = 100, 250
P = HERO_TOP + HERO_H
S_L = 300                        # the cut
C_B = S_L + 116                  # topsoil / bronze
TITLE_TOP = S_L + 24
TITLE_H = 58
L: dict[str, float] = {}
L["in"] = C_B + 46               # cable rings: gridflow ingest
L["bo"] = L["in"] + 144          # a response body (entry spacing = measured entry height + 26)
L["sc"] = L["bo"] + 182          # its sidecar
C_S = L["sc"] + 166              # bronze / silver
L["tr"] = C_S                    # gridflow transform, on the contact
L["fi"] = L["tr"] + 166          # bed A: a Parquet file
L["vi"] = L["fi"] + 184          # bed B: vintages
ROW_C = L["vi"] + 104
L["vw"] = ROW_C + 59             # the view bracket under bed C
C_G = L["vw"] + 144              # silver / gold
L["bu"] = C_G                    # gridflow build, on the contact
L["sq"] = L["bu"] + 144          # the SQL view veins meet
L["mo"] = L["sq"] + 204          # model-output ingots
PLATE_H = L["mo"] + 190
CAT_H = 700
DEEP_H = 1160
H = P + PLATE_H + CAT_H + DEEP_H

ROW = {"A": L["fi"], "A2": L["fi"] + 92, "B": L["vi"], "C": ROW_C, "D": L["vw"] + 62}
BLOCK_H = 70


def contact_y(y0: float, i: int, x: float) -> float:
    """The strata contact at plate-local y0, matching b_base.strata's wave for contact number i."""
    seed = 0.4 + 1.7 * i
    return y0 + 7 * math.sin(x / 210 + seed) + 7 * .45 * math.sin(x / 73 + seed * 2.3)


# ---------------------------------------------------------------- drawing
def lens(x: float, y: float, w: float, key: bool = False) -> str:
    h = 6.5
    return (f'<path d="M{f(x - w / 2)} {f(y)} C{f(x - w / 4)} {f(y - h)} {f(x + w / 4)} {f(y - h)} {f(x + w / 2)} {f(y)} '
            f'C{f(x + w / 4)} {f(y + h * .8)} {f(x - w / 4)} {f(y + h * .8)} {f(x - w / 2)} {f(y)} Z" fill="{CLAY}" '
            f'stroke="{INK}" stroke-width="{1.2 if key else .9}"></path>')


def pebble(x: float, y: float, key: bool = False) -> str:
    return (f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="4.2" ry="3.4" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="{1.2 if key else .9}"></ellipse>')


def block(x: float, y: float, cols: int = 5, stripes: int = 0, seed: int = 0) -> str:
    """One Parquet file: a block of columns (one per field), its top slightly uneven like jointed rock."""
    rng = random.Random(seed)
    cw = 6.6
    w = cols * cw
    top = y - BLOCK_H / 2
    out = []
    for c in range(cols):
        cx = x + c * cw
        t = top + rng.uniform(-2.5, 2.5)
        fill = SILVER if c % 2 == 0 else "#B3BFBD"
        out.append(f'<path d="M{f(cx)} {f(top + BLOCK_H)} V{f(t + 1.5)} L{f(cx + cw / 2)} {f(t)} L{f(cx + cw)} {f(t + 1.5)} '
                   f'V{f(top + BLOCK_H)} Z" fill="{fill}"></path>')
    if stripes:
        sh = BLOCK_H / stripes
        for k in range(stripes):
            if k % 2 == 1:
                out.append(f'<rect x="{f(x)}" y="{f(top + k * sh + 3)}" width="{f(w)}" height="{f(sh - 1)}" '
                           f'fill="{SILVER_DEEP}" opacity=".35"></rect>')
        out.append(f'<rect x="{f(x)}" y="{f(top + 2)}" width="{f(w)}" height="{f(sh - 2)}" fill="{DAY}" opacity=".85"></rect>')
        out.append(f'<path d="' + " ".join(f"M{f(x)} {f(top + k * sh + 2)} H{f(x + w)}" for k in range(1, stripes)) +
                   f'" stroke="{INK}" stroke-width=".5" opacity=".6"></path>')
    joints = " ".join(f"M{f(x + c * cw)} {f(top + 2)} V{f(top + BLOCK_H)}" for c in range(1, cols))
    cross = " ".join(f"M{f(x)} {f(yy)} H{f(x + w)}" for yy in (top + BLOCK_H * .38, top + BLOCK_H * .74))
    out.append(f'<path d="{joints}" stroke="{SILVER_DEEP}" stroke-width=".8"></path>')
    out.append(f'<path d="{cross}" stroke="{SILVER_DEEP}" stroke-width=".6" opacity=".55"></path>')
    out.append(f'<rect x="{f(x)}" y="{f(top)}" width="{f(w)}" height="{BLOCK_H}" fill="none" stroke="{INK}" '
               f'stroke-width="1"></rect>')
    return "".join(out)


SHADES = ["#9FADAB", "#AAB7B5", "#B6C1BF", "#97A5A3", "#A4B1AF"]


def bed(y: float, name: str, x0: float, x1: float, seed: int, stripes: int = 0, months=("08", "09"),
        h: float = BLOCK_H, head: bool = False) -> str:
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
        if head:
            out.append(f'<text class="mono sm" x="{f(start)}" y="{f(top(start) - 12)}">year=2026/month={m}/</text>')
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
    src, ds = name.split("/")[0] + "/", name.split("/")[1] + "/"
    out.insert(0, f'<text class="mono" x="{f(x0 - 14)}" y="{f(y - 4)}" text-anchor="end">{src}</text>'
                  f'<text class="mono" x="{f(x0 - 14)}" y="{f(y + 13)}" text-anchor="end">{ds}</text>')
    return "".join(out)


def vein(pts: list[tuple[float, float]], w0: float, w1: float, seed: int = 0) -> str:
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


def ingot(x: float, y: float) -> str:
    return (f'<path d="M{f(x - 13)} {f(y + 5)} L{f(x - 9)} {f(y - 5)} H{f(x + 9)} L{f(x + 13)} {f(y + 5)} Z" '
            f'fill="{GOLD}" stroke="{INK}" stroke-width="1" stroke-linejoin="round"></path>'
            f'<path d="M{f(x - 7)} {f(y - 2)} H{f(x + 4)}" stroke="{DAY}" stroke-width="1" opacity=".7"></path>')


def pile(x: float, y: float, n: int) -> str:
    out, k = [], 0
    rows = [(0, 3), (1, 2), (2, 1)] if n > 3 else [(0, 2), (1, 1)]
    for r, c in rows:
        for j in range(c):
            if k >= n:
                break
            out.append(ingot(x + (j - (c - 1) / 2) * 28, y + 10 - r * 11))
            k += 1
    return "".join(out)


def drawing() -> tuple[str, list[str]]:
    g: list[str] = []
    sk, ends = strip(S_L, ["sub@400", "mast@620", "conv@748", "gas@880"])
    g.append(sk)
    labels: list[str] = []

    # bronze: daily beds, the newest on top; bodies with their sidecars
    rng = random.Random(7)
    beds = list(frange(C_B + 22, C_S - 18, 24))
    bed_lines = []
    for i, by in enumerate(beds):
        pts = [(x, by + 4 * math.sin(x / 210 + .4) + 1.8 * math.sin(x / 73 + 1.3) + (i % 3) * .6)
               for x in range(60, 1000, 40)]
        bed_lines.append(smooth(pts))
    g.append(f'<path d="{" ".join(bed_lines)}" stroke="{INK}" stroke-width=".7" fill="none" opacity=".3"></path>')
    for i, by in enumerate(beds[:-1]):
        mid = by + 12
        for _ in range(rng.choice([1, 2, 2, 3])):
            x = rng.uniform(250, 880)
            g.append(lens(x, mid, rng.uniform(22, 36)) + pebble(x + 24, mid + .5))
    g.append(lens(930, L["bo"], 34, True) + pebble(956, L["bo"] + .5))
    g.append(lens(880, L["sc"], 28) + pebble(934, L["sc"], True))
    labels.append(f'<text class="mono sm" x="96" y="{f(beds[0] + 16)}">2026/08/18/</text>')
    labels.append(f'<text class="mono sm" x="96" y="{f(beds[1] + 16)}">2026/08/17/</text>')
    labels.append(f'<text class="mono sm" x="96" y="{f(beds[-2] + 16)}">2026/08/01/</text>')
    labels.append(f'<text x="96" y="{f(beds[2] + 30)}">one bed per day,</text>'
                  f'<text x="96" y="{f(beds[2] + 47)}">the newest on top</text>')

    # the feed cables, from the strip's assets down through the topsoil to their rings in bronze
    xs_ring = [444, 604, 772, 920]
    for (ex, ey), rx in zip(ends.values(), xs_ring):
        d = smooth([(ex, ey - 4), (ex, ey + 40), (ex + (rx - ex) * .5, (ey + L["in"]) / 2 + 20), (rx, L["in"] - 30),
                    (rx, L["in"])])
        g.append(cable(d))
    for rx in xs_ring:
        g.append(ring(rx, L["in"]))

    # silver: one columnar bed per dataset directory
    g.append(bed(ROW["A"], "elexon/fuelhh/", 270, 962, 1, head=True))
    g.append(bed(ROW["A2"], "entsoe/day_ahead_prices/", 270, 962, 5))
    g.append(bed(ROW["B"], "elexon/system_prices/", 270, 962, 2, stripes=4))
    g.append(bed(ROW["C"], "neso/carbon_intensity/", 270, 962, 3))
    g.append(bed(ROW["D"], "elexon/mid/", 270, 962, 4))
    bx0, bx1 = 270, 962
    by = L["vw"]
    g.append(f'<path d="M{bx0} {f(by - 7)} V{f(by)} H{f(bx1)} V{f(by - 7)} M770 {f(by)} V{f(by + 7)}" '
             f'stroke="{INK}" stroke-width="1.3" fill="none"></path>')
    labels.append(f'<text class="mono sm" x="780" y="{f(by + 17)}">silver_neso_carbon_intensity</text>')

    # gold: two of the SQL views drawn as veins rising into the beds they read; the model outputs as ingots
    jx, jy = 842, L["sq"]
    g.append(vein([(452, ROW["B"] + BLOCK_H / 2 - 4), (444, ROW["C"] + 4), (462, ROW["D"] - 22), (492, ROW["D"] + 38),
                   (560, C_G + 30), (680, jy - 24), (jx, jy)], 2.5, 12, 1))
    g.append(vein([(700, ROW["C"] + BLOCK_H / 2 - 4), (706, L["vw"] + 14), (722, ROW["D"] + 16), (760, C_G + 24),
                   (800, jy - 14), (jx, jy)], 2.5, 10, 2))
    g.append(vein([(jx - 2, jy), (900, jy + 4), (968, jy + 2)], 13, 11, 3))
    g.append(vein([(330, ROW["D"] + BLOCK_H / 2 - 4), (336, C_G + 16), (310, C_G + 70), (262, C_G + 118)], 2.5, 11, 4))
    labels.append(f'<text class="mono sm" x="{jx - 10}" y="{f(jy + 32)}" text-anchor="end">gold_uk_imbalance_context</text>')
    labels.append(f'<text class="mono sm" x="96" y="{f(C_G + 146)}">gold_gb_day_ahead_benchmark</text>')
    for x, name, n in [(200, "forecasts/", 6), (380, "forecast_metrics/", 4), (560, "stack_clearing/", 5),
                       (740, "stack_residual_demand/", 3), (918, "stack_supply_curve_points/", 6)]:
        g.append(pile(x, L["mo"], n))
        labels.append(f'<text class="mono sm" x="{x}" y="{f(L["mo"] + 38)}" text-anchor="middle">{name}</text>')

    g.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="13.5" fill="{INK}">{"".join(labels)}</g>')
    aria = ("A cutaway of gridflow's store. Feed cables come down from the landscape through the topsoil and end at "
            "rings at the top of bronze. Bronze is a stack of thin daily beds, the newest on top, each holding raw "
            "response bodies with a small sidecar beside each one. Below it, silver is five beds of columnar rock, one "
            "per dataset directory: Elexon fuelhh, ENTSO-E day-ahead prices, Elexon system prices (laminated with "
            "vintages), NESO carbon intensity and Elexon MID. Each column is one daily Parquet file and a dashed joint "
            "separates the months. A bracket under the carbon-intensity bed marks one view over a directory. Gold veins "
            "rise from the system-price and carbon-intensity beds and join as one view; a second vein rises from the MID "
            "bed. At the bottom, gold ingots lie in five piles, one per model-output table.")
    svg = (f'<svg class="draw ar-draw" width="{W}" height="{PLATE_H}" viewBox="0 0 {W} {PLATE_H}" role="img" '
           f'aria-label="{aria}">{"".join(g)}</svg>')
    return svg, []


# ---------------------------------------------------------------- marks and entries
def marks() -> dict[str, str]:
    m = {}
    m["in"] = mark_svg(f'<path d="M15 0 V8" stroke="{INK}" stroke-width="4.4"></path><path d="M15 0 V8" stroke="#A5713C" '
                       f'stroke-width="1.5"></path><circle cx="15" cy="12" r="5.2" fill="{DAY}" stroke="{INK}" '
                       f'stroke-width="1.6"></circle><circle cx="15" cy="12" r="1.8" fill="{INK}"></circle>')
    m["bo"] = mark_svg(f'<path d="M0 16 C10 17 20 17 30 16" stroke="{INK}" stroke-width=".7" fill="none" opacity=".4"></path>'
                       f'<path d="M3 10 C8 4 18 4 23 10 C18 15 8 15 3 10 Z" fill="{CLAY}" stroke="{INK}" stroke-width="1.1"></path>'
                       f'<ellipse cx="27" cy="10.5" rx="2.6" ry="2.2" fill="{DAY}" stroke="{INK}" stroke-width=".7"></ellipse>')
    m["sc"] = mark_svg(f'<path d="M0 16 C10 17 20 17 30 16" stroke="{INK}" stroke-width=".7" fill="none" opacity=".4"></path>'
                       f'<path d="M1 10 C4 6 10 6 13 10 C10 13 4 13 1 10 Z" fill="{CLAY}" stroke="{INK}" stroke-width=".7" '
                       f'opacity=".7"></path><ellipse cx="21" cy="10" rx="6" ry="4.8" fill="{DAY}" stroke="{INK}" '
                       f'stroke-width="1.2"></ellipse>')

    def contact(up: str, down: str) -> str:
        return mark_svg(f'<path d="M0 0 H30 V10 C22 7 10 13 0 9 Z" fill="{up}"></path>'
                        f'<path d="M0 9 C10 13 22 7 30 10 V20 H0 Z" fill="{down}"></path>'
                        f'<path d="M0 9 C10 13 22 7 30 10" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
                        f'<rect x=".5" y=".5" width="29" height="19" fill="none" stroke="{INK}" stroke-width=".6" opacity=".4"></rect>')
    m["tr"] = contact("#E2CDB3", "#DCE2DF")
    m["bu"] = contact("#DCE2DF", "#E9DDAF")
    m["fi"] = mark_svg(
        f'<rect x="6" y="1" width="18" height="18" fill="{SILVER}"></rect>'
        f'<rect x="12" y="1" width="6" height="18" fill="#B3BFBD"></rect>'
        f'<path d="M12 2 V19 M18 2 V19" stroke="{SILVER_DEEP}" stroke-width=".8"></path>'
        f'<path d="M6 8 H24 M6 14 H24" stroke="{SILVER_DEEP}" stroke-width=".6" opacity=".55"></path>'
        f'<rect x="6" y="1" width="18" height="18" fill="none" stroke="{INK}" stroke-width="1"></rect>')
    m["vi"] = mark_svg(f'<rect x="6" y="1" width="18" height="18" fill="{SILVER}"></rect>'
                       f'<rect x="6" y="2" width="18" height="3.5" fill="{DAY}"></rect>'
                       f'<rect x="6" y="10" width="18" height="4" fill="{SILVER_DEEP}" opacity=".35"></rect>'
                       f'<path d="M6 6 H24 M6 10 H24 M6 14 H24" stroke="{INK}" stroke-width=".5" opacity=".6"></path>'
                       f'<rect x="6" y="1" width="18" height="18" fill="none" stroke="{INK}" stroke-width="1"></rect>')
    m["vw"] = mark_svg(f'<path d="M2 5 V11 H28 V5 M15 11 V17" stroke="{INK}" stroke-width="1.4" fill="none"></path>')
    m["sq"] = mark_svg(f'<path d="M3 2 C6 8 10 12 16 13 M11 2 C13 7 14 11 16 13 M16 13 C20 14 25 14 30 14" stroke="{INK}" '
                       f'stroke-width="5.4" fill="none" stroke-linecap="round"></path>'
                       f'<path d="M3 2 C6 8 10 12 16 13 M11 2 C13 7 14 11 16 13 M16 13 C20 14 25 14 30 14" stroke="{GOLD}" '
                       f'stroke-width="3.4" fill="none" stroke-linecap="round"></path>')
    m["mo"] = mark_svg(ingot(9, 15) + ingot(22, 15) + ingot(15.5, 5))
    return m


def entries() -> list[dict]:
    m = marks()
    return [
        dict(y=L["in"], mark=m["in"], name="API to bronze", id="gridflow ingest",
             d="Async connectors, one per source, with rate limits and retries from <code>sources.yaml</code> "
               "(Elexon 2 requests a second, ENTSO-E 1)."),
        dict(y=L["bo"], mark=m["bo"], name="A response body",
             id=wbr("bronze/{source}/{dataset}/{YYYY}/{MM}/{DD}/raw_{fetched_at}_{sha256[:8]}.{ext}"),
             d="The bytes as fetched, as json, xml, csv or bin. Written once, never rewritten; filed by data date, "
               "else fetch date."),
        dict(y=L["sc"], mark=m["sc"], name="Its sidecar", id="raw_…{sha256[:8]}.meta.json",
             d="What was asked and what came back: request URL and parameters (credentials masked), HTTP status, "
               "content type, SHA-256, size, page of pages."),
        dict(y=L["tr"], mark=m["tr"], name="Bronze to silver", id="gridflow transform",
             d="One transformer per source and dataset: parse, validate every row against its Pydantic schema, "
               "convert to UTC, deduplicate on the dataset key, write atomically."),
        dict(y=L["fi"], mark=m["fi"], name="A silver file",
             id=wbr("silver/{source}/{dataset}/year={YYYY}/month={MM}/{dataset}_{YYYYMMDD}.parquet"),
             d="Typed Parquet, zstd, one file per day. Every row carries <code>event_time</code>; "
               "<code>available_at</code> supports as-of reads."),
        dict(y=L["vi"], mark=m["vi"], name="Vintages", id="{dataset}_{YYYYMMDD}_run{available_at}.parquet",
             d="Append-only datasets keep every capture: Elexon <code>system_prices</code>, <code>remit</code>, "
               "<code>fou2t14d</code> and the three NESO Data Portal datasets."),
        dict(y=L["vw"], mark=m["vw"], name="Silver views", id="silver_{source}_{dataset}, …_latest",
             d="One DuckDB view per dataset directory. The six append-only datasets add a latest-vintage view."),
        dict(y=L["bu"], mark=m["bu"], name="Silver to gold", id="gridflow build",
             d="Runs the registered gold builders. There is one, <code>system_marginal_price</code>, writing "
               "<code>gold/{name}/year={YYYY}/</code>."),
        dict(y=L["sq"], mark=m["sq"], name="Gold views, in SQL",
             id="gold_uk_imbalance_context, gold_gb_day_ahead_benchmark, gold_eu_gas_storage",
             d="Joins across sources, registered on <code>init</code>: system prices with carbon intensity; the "
               "APXMIDP benchmark; storage by country and day."),
        dict(y=L["mo"], mark=m["mo"], name="Model outputs", id=wbr("gold/{table}/model_slug={slug}/…_{run_id}.parquet"),
             d="Written by gridflow-models into the same root: forecasts, their metrics, and the stack’s clearing, "
               "residual demand and supply-curve points."),
    ]


# ---------------------------------------------------------------- after the plate: the catalogue (gold) and the deep
CATALOGUE = [
    ("silver_{source}_{dataset}", "One view per silver dataset directory"),
    ("silver_{source}_{dataset}_latest", "The latest vintage, for the six append-only datasets"),
    ("silver_{dataset}", "A deprecated one-name alias, skipped where two sources share a dataset name"),
    ("gold_{name}", "One view per gold directory, the model outputs included"),
    ("gold_uk_imbalance_context", "Elexon system prices with NESO carbon intensity, half-hourly"),
    ("gold_gb_day_ahead_benchmark", "Elexon MID, the APXMIDP provider, £/MWh per settlement period"),
    ("gold_eu_gas_storage", "GIE AGSI+ storage by country and gas day"),
    ("pipeline_runs, pipeline_watermarks, quality_reports", "Tables recording each run, how far each dataset has got, "
                                                            "and quality results"),
]
CLI = [("init", "Create the catalogue and register the views", "1209"),
       ("ingest", "Fetch from a vendor API into bronze", "186"),
       ("transform", "Parse, validate and deduplicate bronze into silver", "261"),
       ("build", "Build gold from silver", "306"),
       ("pipeline", "Ingest then transform; with --gold, build too", "485"),
       ("backfill", "Fetch history in chunks", "346"),
       ("export-csv", "Write silver Parquet out as CSV", "438"),
       ("status", "Run history and a quality summary", "584"),
       ("quality", "Run the quality checks and write a report", "677"),
       ("reset", "Delete bronze, silver and gold data and reset the catalogue", "796"),
       ("prune", "Delete partitions older than a retention cutoff", "972")]
NOT_DO = [
    "No scheduler or orchestrator: every run is a command someone types.",
    "No cloud, object store, warehouse, streaming or cluster.",
    "No server, public API or hosted database: local files and one DuckDB file.",
    "No live feed: data lands when someone runs <code>ingest</code>.",
    "No models, forecasts or trading: those live in gridflow-models.",
]


def catalogue() -> str:
    rows = "".join(f'<tr><td class="k">{wbr(a)}</td><td class="m">{b}</td></tr>' for a, b in CATALOGUE)
    return (f'<section class="band ar-cat" aria-labelledby="cat-h" style="height: {CAT_H}px; padding-top: 56px">'
            f'<div class="ar-two"><div class="sec"><h2 id="cat-h">One catalogue file</h2>'
            f'<p><code>gridflow init</code> creates <code>{{data_root}}/gridflow.duckdb</code> and registers a view for '
            f'every silver and gold directory, plus the SQL views. Nothing is copied into it: the views read the '
            f'Parquet where it lies.</p><p>For Python there is a read-only client, '
            f'<code>gridflow.serving.client.GridflowClient</code>.</p></div>'
            f'<table class="tl cat-tl" aria-labelledby="cat-h"><thead><tr><th scope="col">Relation</th>'
            f'<th scope="col">What it is</th></tr></thead><tbody>{rows}</tbody></table></div></section>')


def deep() -> str:
    cli = "".join(f'<tr><td class="k">{v}</td><td class="m">{d}</td><td class="c">cli.py:{ln}</td></tr>'
                  for v, d, ln in CLI)
    nd = "".join(f"<li>{t}</li>" for t in NOT_DO)
    return (f'<section class="band deep ar-deep" aria-labelledby="cmd-h" style="height: {DEEP_H - 250}px; '
            f'padding-top: 112px">'
            f'<div class="ar-two"><div><h2 id="cmd-h">Commands and gates</h2>'
            f'<table class="tl on-p" aria-labelledby="cmd-h"><thead><tr><th scope="col">gridflow …</th>'
            f'<th scope="col">What it does</th><th scope="col">Defined at</th></tr></thead><tbody>{cli}</tbody></table>'
            f'</div><div class="gates"><h3>Checks</h3><p><code>gridflow quality</code> runs five: '
            f'<code>null_rate</code>, <code>time_series_gaps</code>, <code>range_check</code>, <code>row_count</code> and '
            f'<code>duplicates</code>.</p>'
            f'<h3>On every push and pull request</h3><p>gridflow’s CI runs <code>uv lock --check</code>, '
            f'<code>ruff check</code>, <code>ruff format --check</code>, <code>mypy</code> and '
            f'<code>pytest -m "not live"</code>.</p>'
            f'<h3>What gridflow does not do</h3><ul class="nd">{nd}</ul></div></div></section>')


AR_CSS = """.ar-draw text{font-family:"Hanken Grotesk",sans-serif;font-size:13.5px}
.ar-draw text.mono{font-family:"Red Hat Mono",monospace;font-style:normal;font-size:13px;fill:#1C2B22}
.ar-draw text.sm{font-size:12px;fill:#3F4A3B}
.ar-two{display:grid;grid-template-columns:480px minmax(0,1fr);column-gap:96px;align-items:start}
.cat-tl td.k{font-size:14.5px;width:360px;white-space:normal;padding-top:10px;padding-bottom:10px;height:auto;line-height:1.35}
.cat-tl td{height:auto;padding-top:11px;padding-bottom:11px}
.ar-deep h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0 0 22px;color:#F6F4EC}
.tl.on-p{color:#F6F4EC}
.tl.on-p th{color:#CFE0DC;border-bottom-color:#CFE0DC}
.tl.on-p td{border-bottom-color:rgba(207,224,220,.22)}
.tl.on-p td.m{color:#CFE0DC}
.tl.on-p td.c{color:#B4D0CD;font-size:13.5px}
.tl.on-p td.k{font-size:15px}
.gates{padding-top:64px}
.gates h3{font-size:20px;font-weight:700;font-stretch:90%;margin:0 0 6px;color:#F6F4EC}
.gates p{margin:0 0 22px;font-size:15px;line-height:1.6;color:#CFE0DC;max-width:58ch}
.gates code{font-size:13.5px;color:#F6F4EC}
.nd{margin:0;padding:0 0 0 18px;font-size:15px;line-height:1.6;color:#CFE0DC}
.nd li{margin:0 0 6px}
.nd code{font-size:13.5px;color:#F6F4EC}
"""


def build() -> str:
    hero = (f'<section class="band hero" aria-labelledby="h1" style="height: {HERO_H}px">'
            f'<h1 id="h1">How the store is built</h1>'
            f'<div class="lede"><p>gridflow is a local-first Python pipeline (Polars, DuckDB, Pydantic, httpx, Typer) '
            f'with no server. What it fetches lands in three layers under one data root and is catalogued in one DuckDB '
            f'file.</p><p>The code is Apache-2.0.</p></div></section>')
    svg, _ = drawing()
    ents = [dict(e, y=e["y"] - (TITLE_TOP + TITLE_H)) for e in entries()]
    plate = (f'<section class="band" aria-labelledby="pl-h" style="height: {PLATE_H}px">{svg}'
             f'<div class="plate" style="position: relative; padding-top: {TITLE_TOP}px">'
             f'<h2 class="plate-h" id="pl-h" style="grid-column: 1 / -1; height: {TITLE_H}px">The store, cut open</h2>'
             f'{index_list(ents, "Paths, commands and views, keyed to the cutaway")}</div></section>')
    flow = "\n".join([masthead("Architecture"), "<main>", hero, plate, catalogue(), deep(), "</main>",
                      footer(250, 40)])
    c_b, c_s, c_g = P + C_B, P + C_S, P + C_G
    c_d = P + PLATE_H + CAT_H + 40
    bg = bg_layer(H, strata(H, P + S_L, [(c_b, "bronze"), (c_s, "silver"), (c_g, "gold"), (c_d, "deep")],
                            land=True, names=False))
    return page("Architecture", H, bg, flow, AR_CSS)


_ = (INK2, OLIVE, PETROL, T_SILVER, wave, contact_y)

if __name__ == "__main__":
    emit("B-architecture", build())
    print("H", H, "levels", {k: round(v) for k, v in L.items()}, "C_B", C_B, "C_S", C_S, "C_G", C_G)
