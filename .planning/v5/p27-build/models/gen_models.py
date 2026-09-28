"""Build ``site/hifi/models.html`` from the locked Models boards (``design-loop/models-r2``), responsive.

The drawing parts, the copy and the desktop layout come from the locked board generator (``models-r2/gen.py``,
imported as ``B``). The board is one fixed 1440 frame (and one 390 frame); the page folds them into three
compositions that share one index in the DOM:

* ``d`` desktop, 1440 px and wider: the board's layout at 1:1, with the sky and strata drawn out to 2560 px
  wide so nothing ends at the frame edge; the drawing stays centred.
* ``m`` mid, 1100 to 1439 px: the same drawing scaled to the page width. The index keeps its type size, so its
  levels are laid out from entry heights measured at 1100 px and divided by the scale there.
* ``p`` phone and tablet, below 1100 px: the 390 board's drawing at 1:1 (the land drawn on to 1200 px), the
  index widening beside it; below 390 px the drawing scales down, so its layout is measured at 360 px.

Each drawing gets real top room in its viewBox (the distant turbines' blades), never ``overflow: visible``.

Usage (from the worktree root)::

    uv run --no-project python .planning/v5/p27-build/models/gen_models.py [--port 9741]

It needs the design-loop folder in the main checkout (``MAIN`` below) and a static server on ``--port`` serving
``site/hifi``; it measures with headless Chrome, writes the page twice and prints the checks.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path

MAIN = Path(r"C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end")
DL = MAIN / ".planning" / "v5" / "design-loop"
sys.path.insert(0, str(DL / "p27-r1" / "A"))
sys.path.insert(0, str(DL / "models-r2"))

import frame  # noqa: E402
import gen as B  # noqa: E402  the locked board generator; main() is not run
import hp  # noqa: E402
import scenery as sn  # noqa: E402
from hp import f, smooth  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
SITE = ROOT / "site" / "hifi"
OUT = SITE / "models.html"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PETROL, HORIZON, CHART, OLIVE = B.PETROL, B.HORIZON, B.CHART, B.OLIVE
INK, DAY, CLAY, BRONZE, SILVER, GOLD = B.INK, B.DAY, B.CLAY, B.BRONZE, B.SILVER, B.GOLD
T_GOLD, T_SILVER, T_TOP, FAR = B.T_GOLD, B.T_SILVER, B.T_TOP, B.FAR
W, PW = B.W, B.PW
cab, terminal, joint, run, fan, stack, splice = B.cab, B.terminal, B.joint, B.run, B.fan, B.stack, B.splice
wave_y = B.wave_y

# horizontal extents of each drawing (user units); the board frames are 0..1440 and 0..390
DXA, DXB = -560, 2000          # desktop: centred on 720, fills viewports up to 2560 wide at 1:1
MXA, MXB = -40, 1480           # mid: only 0..1440 is in the viewBox
PXA, PXB = -100, 1200          # phone: 0..390 is the board; the land runs on for tablet widths
TOP = 40                       # top room above the board's y 0: the far turbines' blade tips reach y -28

MID_MIN, PH_MIN = 1100, 360    # the narrowest width each scaled composition is laid out for

# the patterns each drawing uses, with ids made unique per drawing (three drawings share the page)
PATS = "\n".join(ln for ln in hp.PATTERNS.splitlines() if re.search(r'id="p-(stip|diag|soil)"', ln))


def own_ids(svg: str, pfx: str) -> str:
    return svg.replace('id="p-', f'id="{pfx}-').replace("url(#p-", f"url(#{pfx}-")


# =============================================================== the ground, drawn out sideways
def wave_d(y0: float, amp: float, seed: float, w: int, xa: float, xb: float) -> str:
    """The board's contact line (``B.wave_d``), with the same points, run on past both ends."""
    step = 120 if w > 500 else 60
    x = -40
    while x > xa - 40:
        x -= step
    pts = []
    while x <= xb + step + 40:
        pts.append((x, wave_y(y0, amp, seed, x, w)))
        x += step
    return smooth(pts)


def ground(Y: dict, w: int, prof, amp: tuple[float, float], xa: float, xb: float, top: float) -> tuple[str, str]:
    """``B.ground`` from xa to xb, with the sky starting at y ``top`` (the top room)."""
    S, Hd = Y["S"], Y["Hd"]
    st = 8 if w > 500 else 4
    x0 = -40
    while x0 > xa - 40:
        x0 -= st
    surf = [(x, prof(x)) for x in range(x0, int(xb) + 41, st)]
    surf_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    tail = f" L{f(xb + 40)} {f(Hd + 10)} L{f(x0)} {f(Hd + 10)} Z"
    o = [f'<rect x="{f(xa - 40)}" y="{f(top)}" width="{f(xb - xa + 80)}" height="{f(S + 60 - top)}" '
         f'fill="{PETROL}"></rect>']
    fills = [f'<path d="{surf_d}{tail}" fill="{T_TOP}"></path><path d="{surf_d}{tail}" fill="url(#p-soil)" '
             f'opacity=".5"></path>']
    lines = []
    for y0, a, seed, fill, pid, op in ((Y["CS"], amp[0], 2.1, T_SILVER, "p-diag", ".22"),
                                       (Y["CG"], amp[1], 4.0, T_GOLD, "p-stip", ".26")):
        d = wave_d(y0, a, seed, w, xa, xb)
        fills.append(f'<path d="{d}{tail}" fill="{fill}"></path><path d="{d}{tail}" fill="url(#{pid})" '
                     f'opacity="{op}"></path>')
        lines.append(d)
    root = surf_d + " " + " ".join(f"L{f(x)} {f(y + (8 if w > 500 else 6))}" for x, y in reversed(surf)) + " Z"
    fills.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    ink = (f'<path d="{surf_d}" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
           f'<path d="{" ".join(lines)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    return "".join(o + fills), ink


# =============================================================== desktop sky (B.landscape_desk, drawn on)
def landscape_desk(S: float) -> tuple[str, str]:
    hp.Y["surf"] = S
    p = []
    far = [(-600, S - 282), (-400, S - 256), (-200, S - 272),
           (-20, S - 250), (160, S - 280), (360, S - 262), (560, S - 286), (760, S - 258), (960, S - 276),
           (1160, S - 250), (1320, S - 270), (1460, S - 256),
           (1640, S - 276), (1840, S - 258), (2040, S - 280)]
    p.append(sn.ridge(far, S - 60, FAR))
    near0 = [(-20, S - 214), (110, S - 238), (250, S - 246), (400, S - 226), (560, S - 250), (720, S - 232),
             (880, S - 214), (1040, S - 228), (1220, S - 208), (1460, S - 220)]
    near = ([(-600, S - 224), (-440, S - 240), (-280, S - 222), (-150, S - 232)] + near0
            + [(1640, S - 236), (1820, S - 216), (2020, S - 230)])
    p.append(sn.ridge(near, S - 60, HORIZON))
    for i, (tx, ty) in enumerate(near0[2:6]):
        hgt = [56, 62, 54, 60][i]
        p.append(hp.turbine(tx, ty + 3, hgt, hgt * .5, ["sp2", "sp3", "sp1"][i % 3], 29 * i + 5))
    top = [(-620, S - 146), (-420, S - 136), (-220, S - 148),
           (-20, S - 142), (200, S - 150), (420, S - 138), (640, S - 148), (860, S - 136), (1080, S - 146),
           (1280, S - 134), (1460, S - 140),
           (1660, S - 146), (1860, S - 136), (2060, S - 144)]
    p.append(sn.field(top, hp.prof, -620, 2060,
                      [[(-620, S - 112), (-20, S - 116), (400, S - 120), (900, S - 110), (1460, S - 114),
                        (2060, S - 118)],
                       [(-620, S - 88), (-20, S - 84), (500, S - 90), (1000, S - 80), (1460, S - 86),
                        (2060, S - 82)],
                       [(-620, S - 46), (-20, S - 48), (600, S - 52), (1200, S - 44), (1460, S - 48),
                        (2060, S - 50)]]))
    # the pylon line runs on to the left: two more towers where the board's wires left its frame
    pls = [(x, hp.prof(x) - 2, .62) for x in (-482, -212, 58)]
    sub_x, sub_s = 128, 1.1
    sb = hp.prof(sub_x + 50)
    sub_svg, ends = hp.substation(sub_x, sb)
    ends = [(sub_x + (ex - sub_x) * sub_s, sb + (ey - sb) * sub_s) for ex, ey in ends]
    p.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">'
             + "".join(hp.pylon(*pl) for pl in pls) + "</g>")
    p.append(hp.sc(sub_svg, sub_x, sb, sub_s))
    edge = [(DXA - 60, y) for _x, y in hp.tips(*pls[0], -1)]
    wires = [hp.spans(edge, hp.tips(*pls[0], -1), 14), hp.spans(hp.tips(*pls[0], 1), hp.tips(*pls[1], -1), 14),
             hp.spans(hp.tips(*pls[1], 1), hp.tips(*pls[2], -1), 14), hp.spans(hp.tips(*pls[2], 1), ends, 9)]
    p.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')
    for i, (tx, hh) in enumerate([(468, 150), (560, 136), (640, 124)]):
        p.append(hp.turbine(tx, hp.prof(tx), hh, hh * .5, ["sp1", "sp2", "sp3"][i], 25 + 40 * i))
    p.append(sn.solar_farm_at(690, 900, hp.prof))
    bx, bb = 944, hp.prof(980)
    for dx, r in ((0, 22), (50, 22)):
        p.append(f'<path d="M{f(bx + dx)} {f(bb)} A{r} {r} 0 0 1 {f(bx + dx + 2 * r)} {f(bb)} Z" fill="{BRONZE}" '
                 f'stroke="{INK}" stroke-width="1"></path>'
                 f'<path d="M{f(bx + dx + 6)} {f(bb - 8)} A{r - 6} {r - 8} 0 0 1 {f(bx + dx + 2 * r - 6)} {f(bb - 8)}" '
                 f'stroke="{DAY}" stroke-width=".8" opacity=".35" fill="none"></path>')
    p.append(sn.nuclear(1052, hp.prof(1110)))
    p.append(hp.ccgt(1222, hp.prof(1260), .92))
    ox, ob = 1360, hp.prof(1380)
    p.append(f'<rect x="{ox}" y="{f(ob - 18)}" width="44" height="18" fill="{CLAY}" stroke="{INK}" stroke-width=".9"></rect>'
             f'<rect x="{ox + 30}" y="{f(ob - 40)}" width="8" height="22" fill="{DAY}" stroke="{INK}" stroke-width=".9"></rect>'
             f'<path d="M{ox + 4} {f(ob - 11)} H{ox + 26}" stroke="{DAY}" stroke-width=".8" stroke-dasharray="3 3"></path>')
    labels = [("substation", 184, S - 72, "middle"), ("wind farm", 384, S - 98, "end"),
              ("solar farm", 796, S - 74, "middle"), ("biomass", 990, S - 50, "middle"),
              ("nuclear", 1100, S - 88, "middle"), ("CCGT", 1250, S - 120, "middle"), ("OCGT", 1360, S - 58, "end")]
    lab = "".join(f'<text x="{x}" y="{f(y)}" text-anchor="{a}">{t}</text>' for t, x, y, a in labels)
    return "\n".join(p), lab


def drawing_desk(Y: dict, cls: str, pfx: str, xa: float, xb: float, view: tuple[float, float] | None) -> str:
    """``B.drawing_desk`` with the land drawn from xa to xb and TOP of sky above the board's y 0.

    ``view`` is the viewBox x range (defaults to xa..xb)."""
    S, CS, T0, CG, Hd = Y["S"], Y["CS"], Y["T0"], Y["CG"], Y["Hd"]
    hp.Y["surf"] = S
    land, sky_lab = landscape_desk(S)
    top, ink = ground(Y, W, hp.prof, (8, 7), xa, xb, -TOP)
    o = [top, land, ink]
    lab: list[str] = []
    LD, LW, LS, LF = B.LD, B.LW, B.LS, B.LF
    lanes = [LD, LW, LS, LF]
    for i, (x0, lane) in enumerate(zip(B.ORIG, lanes)):
        o.append(cab(run(x0, hp.prof(x0) + 12, S + 36 + 13 * i, lane, wave_y(CS, 8, 2.1, lane, W)), BRONZE))
    for lane in lanes:
        o.append(cab(f"M{lane} {f(wave_y(CS, 8, 2.1, lane, W))} V{f(wave_y(CG, 7, 4.0, lane, W))}", SILVER))
    taps = [(LD, T0, "elexon/indo"), (LW, T0, "elexon/fuelhh"), (LS, T0, "neso_data_portal/"),
            (LF, T0, "elexon/bmunits_reference"), (LF, T0 + 27, "elexon/remit"), (LF, T0 + 54, "elexon/fou2t14d")]
    for x, y, code in taps:
        o.append(joint(x, y))
        lab.append(f'<text x="{x + 14}" y="{f(y + 4.5)}" class="m">{code}</text>')
    lab.append(f'<text x="{LS + 14}" y="{f(T0 + 21)}" class="m">historic_generation_mix</text>')
    yR, yK, yM = Y["R"], Y["K"], Y["M"]
    sp_w, sp_h = 88, 54
    parts = []
    for lane, key, kind in ((LD, "D", "demand"), (LW, "W", "wind"), (LS, "Sl", "solar")):
        yp = Y[key]
        ys = yp - 42
        o.append(cab(f"M{lane} {f(wave_y(CG, 7, 4.0, lane, W))} V{f(ys)}", CHART))
        o.append(cab(run(lane, ys, ys + 16, lane + 50, yp, 10), GOLD))
        parts.append(fan(kind, lane + 24, yp, sp_w, sp_h))
        parts.append(terminal(lane + 50, yp))
        parts.append(joint(lane, ys))
    SW, SH = 76, 22
    yc = yR + 4
    o.append(cab(f"M{LD} {f(Y['D'] - 42)} V{f(yc - 92)} C{LD} {f(yc - 40)} {LW - 20} {f(yc - 52)} {LW - 20} {f(yc + 2)}",
                 CHART))
    o.append(cab(f"M{LW} {f(Y['W'] - 42)} V{f(yc + 2)}", CHART))
    o.append(cab(f"M{LS} {f(Y['Sl'] - 42)} V{f(yc - 92)} C{LS} {f(yc - 40)} {LW + 20} {f(yc - 52)} {LW + 20} "
                 f"{f(yc + 2)}", CHART))
    ly = yc - 104
    lab += [f'<text x="{LD + 12}" y="{f(ly)}">recorded demand</text>',
            f'<text x="{LW + 12}" y="{f(ly)}">recorded wind</text>',
            f'<text x="{LS + 12}" y="{f(ly)}">recorded solar</text>']
    mx, mw, mh = 476, 204, 112
    smp_svg, xc, yprice = stack(mx, yM, mw, mh, smp=True)
    base = yM + .12 * mh + .74 * mh
    o.append(cab(run(LW, yc + SH - 2, yM - 36, xc, base, 12), CHART))
    lab.append(f'<text x="{LW + 12}" y="{f(yc + SH + 32)}">residual demand</text>')
    kx, kw, kh = LF - 78, 156, 76
    o.append(cab(f"M{LF} {f(wave_y(CG, 7, 4.0, LF, W))} V{f(yK)}", CHART))
    sx = mx + mw - 30
    o.append(cab(run(LF, yK + kh, yM - 36, sx, yM, 12), CHART))
    lab.append(f'<text x="{LF - 12}" y="{f((yK + kh + yM - 36) / 2 + 4)}" text-anchor="end">'
               f'supply curve per half-hour</text>')
    lab.append(f'<text x="{mx - 10}" y="{f(yprice + 4)}" text-anchor="end">price</text>')
    parts.append(splice(LW, yc, SW, SH))
    parts.append(stack(kx, yK, kw, kh)[0])
    parts.append(terminal(LF, yK))
    parts.append(smp_svg)
    parts.append(cab(f"M{f(xc)} {f(yM - 2)} V{f(base)}", CHART))
    parts.append(terminal(sx, yM))
    parts.append(terminal(xc, base, T_TOP, 4.6))
    for lane in lanes:
        parts.append(frame.sleeve(lane, wave_y(CS, 8, 2.1, lane, W), T_SILVER))
        parts.append(frame.sleeve(lane, wave_y(CG, 7, 4.0, lane, W), T_GOLD))
    for x0 in B.ORIG:
        parts.append(terminal(x0, hp.prof(x0) + 12, "#E2CDB3"))
    va, vb = view if view else (xa, xb)
    vh = Hd + TOP
    par = ' preserveAspectRatio="xMidYMin slice"' if cls == "dr--d" else ""
    svg = (f'<svg class="dr {cls}" width="{f(vb - va)}" height="{f(vh)}" viewBox="{f(va)} {-TOP} {f(vb - va)} {f(vh)}"'
           f'{par} role="img" aria-label="{B.draw_aria()}"><defs>{PATS}</defs>\n' + "\n".join(o + parts)
           + f'\n<g class="lab sky">{sky_lab}</g><g class="lab">' + "".join(lab) + "</g></svg>")
    return own_ids(svg, pfx)


# =============================================================== phone sky (B.landscape_phone, drawn on)
def landscape_phone(S: float) -> tuple[str, str]:
    pprof = B.pprof_for(S)
    p: list[str] = []
    far = [(-140, S - 104), (-20, S - 96), (70, S - 108), (160, S - 98), (250, S - 110), (330, S - 100),
           (410, S - 106), (490, S - 98), (570, S - 110), (650, S - 100), (730, S - 108), (810, S - 96),
           (890, S - 106), (970, S - 100), (1050, S - 110), (1130, S - 102), (1240, S - 106)]
    p.append(sn.ridge(far, S - 30, FAR))
    near0 = [(-20, S - 78), (60, S - 88), (140, S - 92), (220, S - 82), (300, S - 90), (410, S - 84)]
    near = ([(-140, S - 86)] + near0 + [(500, S - 90), (590, S - 80), (680, S - 88), (770, S - 82), (860, S - 92),
                                        (950, S - 84), (1040, S - 90), (1130, S - 80), (1240, S - 86)])
    p.append(sn.ridge(near, S - 30, HORIZON))
    for i, (tx, ty) in enumerate(near0[1:5]):
        hgt = [26, 30, 24, 28][i]
        p.append(hp.turbine(tx, ty + 2, hgt, hgt * .5, ["sp2", "sp3", "sp1", "sp2"][i], 29 * i + 5))
    fld = [(-140, S - 58), (-20, S - 56), (90, S - 60), (200, S - 54), (300, S - 60), (410, S - 56),
           (520, S - 60), (630, S - 54), (740, S - 60), (850, S - 56), (960, S - 60), (1070, S - 54),
           (1180, S - 58), (1260, S - 56)]
    p.append(sn.field(fld, pprof, -140, 1260,
                      [[(-140, S - 40), (-20, S - 40), (200, S - 42), (410, S - 38), (620, S - 42), (830, S - 38),
                        (1040, S - 42), (1260, S - 40)],
                       [(-140, S - 20), (-20, S - 20), (220, S - 22), (410, S - 18), (620, S - 22), (830, S - 18),
                        (1040, S - 22), (1260, S - 20)]]))
    hp.Y["surf"] = S
    sub_svg, _e = hp.substation(10, pprof(40))
    p.append(hp.sc(sub_svg, 10, pprof(40), .5))
    for i, (tx, hh) in enumerate([(84, 64), (106, 58), (126, 52)]):
        p.append(hp.turbine(tx, pprof(tx), hh, hh * .5, ["sp1", "sp2", "sp3"][i], 25 + 40 * i))
    farm = sn.solar_farm_at(0, 120, lambda _x: 0.0)
    p.append(f'<g transform="translate(152 {f(pprof(190))}) scale(.62)">{farm}</g>')
    bb = pprof(240)
    for bx in (228, 244):
        p.append(f'<path d="M{bx} {f(bb)} A8 8 0 0 1 {bx + 16} {f(bb)} Z" fill="{BRONZE}" stroke="{INK}" '
                 f'stroke-width=".8"></path>')
    p.append(hp.sc(sn.nuclear(266, pprof(290)), 266, pprof(290), .4))
    p.append(hp.sc(hp.ccgt(330, pprof(344), .92), 330, pprof(344), .4))
    ob = pprof(372)
    p.append(f'<rect x="362" y="{f(ob - 8)}" width="20" height="8" fill="{CLAY}" stroke="{INK}" stroke-width=".7"></rect>'
             f'<rect x="375" y="{f(ob - 18)}" width="4" height="10" fill="{DAY}" stroke="{INK}" stroke-width=".7"></rect>')
    labs = [("substation", 16, S - 124, "start", 32, S - 30), ("wind farm", 110, S - 140, "middle", 110, S - 60),
            ("solar farm", 190, S - 124, "middle", 190, S - 44), ("power stations", 306, S - 140, "middle", 306, S - 44)]
    lab = "".join(f'<text x="{x}" y="{f(y)}" text-anchor="{a}" class="v">{t}</text>' for t, x, y, a, _lx, _ly in labs)
    lead = " ".join(f"M{lx} {f(y + 6)} V{f(ly)}" for _t, _x, y, _a, lx, ly in labs)
    p.append(f'<path d="{lead}" stroke="{DAY}" stroke-width=".8" opacity=".75"></path>')
    return "\n".join(p), lab


def drawing_phone(Y: dict) -> str:
    """``B.drawing_phone`` with the land drawn from PXA to PXB (the cables, parts and levels unchanged)."""
    S, CS, CG, Hd = Y["S"], Y["CS"], Y["CG"], Y["Hd"]
    pprof = B.pprof_for(S)
    land, sky_lab = landscape_phone(S)
    top, ink = ground(Y, PW, pprof, (5, 5), PXA, PXB, 0)
    o = [top, land, ink]
    parts: list[str] = []
    k = .78
    PL, PORIG = B.PL, B.PORIG
    for i, (x0, lane) in enumerate(zip(PORIG, PL)):
        o.append(cab(run(x0, pprof(x0) + 9, S + 18 + 9 * i, lane, wave_y(CS, 5, 2.1, lane, PW), 8), BRONZE, k))
    for lane in PL:
        o.append(cab(f"M{lane} {f(wave_y(CS, 5, 2.1, lane, PW))} V{f(wave_y(CG, 5, 4.0, lane, PW))}", SILVER, k))
    for i, lane in enumerate([PL[0], PL[1], PL[2], PL[3], PL[3], PL[3]]):
        parts.append(joint(lane, Y[f"t{i}"] + 9, 3.8))
    yR, yK, yM = Y["R"], Y["K"], Y["M"]
    fw, fh = 34, 22
    for lane, key, kind in ((PL[0], "D", "demand"), (PL[1], "W", "wind"), (PL[2], "Sl", "solar")):
        yp = Y[key] + 4
        ys = yp - 26
        o.append(cab(f"M{lane} {f(wave_y(CG, 5, 4.0, lane, PW))} V{f(ys)}", CHART, k))
        o.append(cab(run(lane, ys, ys + 10, lane + 16, yp, 6), GOLD, k))
        parts.append(fan(kind, lane + 5, yp, fw, fh, 1.2))
        parts.append(terminal(lane + 16, yp, T_GOLD, 3.8))
        parts.append(joint(lane, ys, 3.6))
    SW, SH = 46, 14
    yc = yR + 6
    o.append(cab(f"M{PL[0]} {f(Y['D'] - 22)} V{f(yc - 56)} C{PL[0]} {f(yc - 24)} {PL[1] - 12} {f(yc - 30)} "
                 f"{PL[1] - 12} {f(yc + 2)}", CHART, k))
    o.append(cab(f"M{PL[1]} {f(Y['W'] - 22)} V{f(yc + 2)}", CHART, k))
    o.append(cab(f"M{PL[2]} {f(Y['Sl'] - 22)} V{f(yc - 56)} C{PL[2]} {f(yc - 24)} {PL[1] + 12} {f(yc - 30)} "
                 f"{PL[1] + 12} {f(yc + 2)}", CHART, k))
    mx, mw, mh = 44, 104, 60
    smp_svg, xc, _yp = stack(mx, yM + 4, mw, mh, 1.3, smp=True)
    base = yM + 4 + .12 * mh + .74 * mh
    o.append(cab(run(PL[1], yc + SH - 2, yM - 16, xc, base, 7), CHART, k))
    kx, kw, kh = 88, 58, 34
    ky = yK + 4
    o.append(cab(run(PL[3], wave_y(CG, 5, 4.0, PL[3], PW), ky - 16, 130, ky, 6), CHART, k))
    sx = mx + mw - 14
    o.append(cab(run(130, ky + kh, yM - 16, sx, yM + 4, 6), CHART, k))
    parts.append(splice(PL[1], yc, SW, SH, 1.3))
    parts.append(stack(kx, ky, kw, kh, 1.3)[0])
    parts.append(terminal(130, ky, T_GOLD, 3.8))
    parts.append(smp_svg)
    parts.append(cab(f"M{f(xc)} {f(yM + 2)} V{f(base)}", CHART, k))
    parts.append(terminal(sx, yM + 4, T_GOLD, 3.8))
    parts.append(terminal(xc, base, T_TOP, 3.4))
    for lane in PL:
        cy = wave_y(CS, 5, 2.1, lane, PW)
        parts.append(hp.sc(frame.sleeve(lane, cy, T_SILVER), lane, cy, .6))
        cy = wave_y(CG, 5, 4.0, lane, PW)
        parts.append(hp.sc(frame.sleeve(lane, cy, T_GOLD), lane, cy, .6))
    for x0 in PORIG:
        parts.append(terminal(x0, pprof(x0) + 9, "#E2CDB3", 3.8))
    svg = (f'<svg class="dr dr--p" width="{PXB - PXA}" height="{f(Hd)}" viewBox="{PXA} 0 {PXB - PXA} {f(Hd)}" '
           f'role="img" aria-label="{B.draw_aria()}"><defs>{PATS}</defs>\n' + "\n".join(o + parts)
           + f'\n<g class="lab sky">{sky_lab}</g></svg>')
    return own_ids(svg, "mp")


# =============================================================== the index (one list, three sets of levels)
NODE = {"dem": "D", "wind": "W", "solar": "Sl", "res": "R", "stack": "K", "smp": "M"}


def pct(y: float, h: float) -> str:
    return f"{100 * y / h:.4f}".rstrip("0").rstrip(".") + "%"


def brk(inner: str) -> str:
    """Break opportunities in long codes, as the phone board sets them (desktop keeps codes whole in CSS)."""
    if len(inner.replace("<wbr>", "")) < 16 or "<wbr>" in inner:
        return inner
    return re.sub(r"([_/.])", r"\1<wbr>", inner)


def codes(s: str) -> str:
    return re.sub(r"<code>((?:[^<]|<wbr>)+)</code>", lambda m: f"<code>{brk(m.group(1))}</code>", s)


def index_html(L: dict) -> str:
    """The taps (phone only), the keyed model entries and the in-development line, levelled per composition."""
    yd, ym, yp = L["d"]["Y"], L["m"]["Y"], L["p"]["Y"]
    hd, hm, hpp = yd["Hd"] + TOP, ym["Hd"] + TOP, yp["Hd"]

    def at(kd: float, km: float, kp: float) -> str:
        return f"--td:{pct(kd + TOP, hd)};--tm:{pct(km + TOP, hm)};--tp:{pct(kp, hpp)}"

    taps = []
    for key, code in B.TAPS:
        c = code.replace("/", "/<wbr>").replace("_generation", "_<wbr>generation")
        taps.append(f'<li class="tp" data-h="{key}" style="--tp:{pct(yp[key], hpp)}">{B.mk("tap")}'
                    f'<p><code>{c}</code></p></li>')
    ents = []
    for key, mark, name, lines, ids in B.entries():
        n = NODE[key]
        body = "".join(f'<p class="{c}">{codes(t)}</p>' for c, t in lines)
        lk = f'<p class="kk">{codes(B.links(ids))}</p>' if ids else ""
        ents.append(f'<li class="ke" data-h="{key}" style="{at(yd[n] - 5, ym[n] - 5, yp[n] - 5)}">{B.mk(mark)}'
                    f'<div><h2 class="kn">{name}</h2>{body}{lk}</div></li>')
    dev = (f'<p class="dev" data-h="dev" style="{at(yd["NB"], ym["NB"], yp["NB"])}">'
           "The modelling is still in development; this page will grow with it.</p>")
    return ('<div class="dov">\n'
            f'<ul class="taps" aria-label="The silver datasets the cables read">{"".join(taps)}</ul>\n'
            f'<ul class="kidx" aria-label="The models, keyed to the drawing">\n' + "\n".join(ents) + "\n</ul>\n"
            f"{dev}\n</div>")


# =============================================================== page
FONTS = ('  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@'
         '12..96,75..100,200..800&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:'
         'wght@400;500&amp;display=swap">\n')


def page(L: dict, probe: str = "") -> str:
    op = B.OP
    h1 = html.escape(op["headline"], quote=False).replace("day-ahead price", '<span class="nw">day-ahead price</span>')
    desc = ("gridflow-models forecasts GB demand, wind and solar, builds the GB merit-order supply stack, and clears "
            "residual demand against it for a day-ahead price.")
    d = drawing_desk(L["d"]["Y"], "dr--d", "md", DXA, DXB, None)
    m = drawing_desk(L["m"]["Y"], "dr--m", "mm", MXA, MXB, (0, W))
    p = drawing_phone(L["p"]["Y"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Models: from demand to a day-ahead price · gridflow</title>
  <meta name="description" content="{desc}">
{FONTS}  <link rel="stylesheet" href="assets/theme.css">
  <link rel="stylesheet" href="assets/models.css">
</head>
<body data-page="model" data-root="" data-screen-label="04 Models">
  <main id="main">
    <section class="stratum stratum--sky m-open" aria-labelledby="m-h">
      <div class="wrap m-hero">
        <h1 class="h-hero m-hero__h" id="m-h">{h1}</h1>
        <div class="m-hero__lede">
          <p class="lead">{html.escape(op["lede"], quote=False)}</p>
          <p>{html.escape(B.SCOPE, quote=False)}</p>
        </div>
      </div>
    </section>
    <section class="m-chain" aria-label="The chain, in section">
{d}
{m}
{p}
{index_html(L)}
    </section>
  </main>
  <script src="assets/site.js"></script>
{probe}</body>
</html>
"""


def check(out: str) -> None:
    assert "\u2014" not in out and "\u2192" not in out, "em dash or arrow"
    assert "overflow:visible" not in out.replace(" ", ""), "overflow visible"
    low = out.lower()
    for bad in ("licen", "mit-licensed", "apache", "local data", "planned", "shipped", "phase "):
        assert bad not in low, f"banned wording: {bad}"
    ids = re.findall(r'\sid="([^"]+)"', out)
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, f"duplicate ids {dup}"


# =============================================================== measuring
PROBE = """<script>
window.addEventListener('load',function(){Promise.all(['720 23px "Bricolage Grotesque"','760 86px "Bricolage Grotesque"','400 15px "Hanken Grotesk"','600 15px "Hanken Grotesk"','italic 400 14px "Hanken Grotesk"','400 13px "Red Hat Mono"']
.map(function(q){return document.fonts.load(q)})).then(function(){return document.fonts.ready}).then(function(){setTimeout(function(){
var W=document.documentElement.clientWidth,o={w:W,h:{},hit:[],over:[],clip:[],docW:document.documentElement.scrollWidth};
var vis=function(e){return e.getClientRects().length>0&&getComputedStyle(e).display!=='none'&&getComputedStyle(e.parentElement).display!=='none';};
document.querySelectorAll('[data-h]').forEach(function(e){if(vis(e))o.h[e.dataset.h]=Math.ceil(e.getBoundingClientRect().height);});
var ks=[].slice.call(document.querySelectorAll('.tp,.ke,.dev')).filter(vis);
for(var i=0;i<ks.length;i++)for(var j=i+1;j<ks.length;j++){var a=ks[i].getBoundingClientRect(),b=ks[j].getBoundingClientRect();if(a.left<b.right&&b.left<a.right&&a.top<b.bottom-.5&&b.top<a.bottom-.5)o.hit.push(ks[i].dataset.h+'x'+ks[j].dataset.h);}
var dr=[].slice.call(document.querySelectorAll('.dr')).filter(function(e){return getComputedStyle(e).display!=='none';});
o.dr=dr.map(function(e){return e.getAttribute('class');});
var sec=document.querySelector('.m-chain').getBoundingClientRect();o.secH=Math.round(sec.height);
var last=ks[ks.length-1].getBoundingClientRect();o.devGap=Math.round(sec.bottom-last.bottom);
document.querySelectorAll('main *').forEach(function(e){if(e.closest('svg'))return;var r=e.getBoundingClientRect();if(r.width>0&&(r.right>W+.5||r.left<-.5)&&!e.matches('.m-chain'))o.over.push((e.className||e.tagName)+':'+Math.round(r.left)+'..'+Math.round(r.right));
if(e.scrollWidth>e.clientWidth+1&&!e.matches('.m-chain,svg'))o.clip.push((e.className||e.tagName)+':'+(e.scrollWidth-e.clientWidth)+':'+e.textContent.slice(0,30));});
o.over=o.over.slice(0,20);o.clip=o.clip.slice(0,20);
var doc=window.parent!==window?parent.document:document;var pre=doc.createElement('pre');pre.id='m';pre.textContent=JSON.stringify(o);doc.body.appendChild(pre);},700);});});
</script>
"""


def measure(L: dict, port: int, width: int) -> dict:
    """Measure at an exact page width: headless Chrome keeps windows at least 500 wide, so the page loads in an
    iframe of that width and posts its findings to the harness."""
    probe_file = SITE / "_probe_models.html"
    harness = SITE / "_probe_harness.html"
    probe_file.write_text(page(L, PROBE), encoding="utf-8")
    harness.write_text(f'<!doctype html><html><body style="margin:0"><iframe src="_probe_models.html?v={time.time_ns()}" '
                       f'width="{width}" height="3000" style="border:0;display:block"></iframe></body></html>',
                       encoding="utf-8")
    try:
        for attempt in range(3):
            try:
                out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                                      f"--window-size={max(width, 600) + 40},3100", "--virtual-time-budget=15000",
                                      "--dump-dom", f"http://127.0.0.1:{port}/_probe_harness.html?v={time.time_ns()}"],
                                     capture_output=True, text=True, encoding="utf-8", timeout=120)
            except subprocess.TimeoutExpired:
                continue
            mm = re.search(r'<pre id="m">(.*?)</pre>', out.stdout, re.S)
            if mm:
                return json.loads(html.unescape(mm.group(1)))
        raise RuntimeError(f"probe failed at {width}")
    finally:
        probe_file.unlink()
        harness.unlink()


def layouts(hmid: dict | None, hph: dict | None) -> dict:
    """The three layouts. Desktop is the board's (its measured heights); mid and phone come from the heights
    measured at their narrowest widths, in drawing units (divided by the drawing's scale there)."""
    board = json.loads((DL / "models-r2" / "measure.json").read_text(encoding="utf-8"))
    hd = board["desktop"]["h"]
    km, kp = MID_MIN / W, PH_MIN / PW
    hm = {k: math.ceil(v / km) for k, v in (hmid or hd).items()}
    hq = {k: math.ceil(v / kp) for k, v in hph.items()} if hph else board["phone"]["h"]
    return {"d": {"Y": B.layout(hd, False)}, "m": {"Y": B.layout(hm, False)}, "p": {"Y": B.layout(hq, True)}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9741)
    ap.add_argument("--check", nargs="*", type=int,
                    default=[360, 390, 430, 600, 768, 1024, 1099, 1100, 1280, 1439, 1440, 1920])
    a = ap.parse_args()
    L = layouts(None, None)
    m1 = measure(L, a.port, MID_MIN)
    p1 = measure(L, a.port, PH_MIN)
    L = layouts(m1["h"], p1["h"])
    m2 = measure(L, a.port, MID_MIN)
    p2 = measure(L, a.port, PH_MIN)
    if m2["h"] != m1["h"] or p2["h"] != p1["h"]:
        print("WARNING heights moved between passes", m1["h"], m2["h"], p1["h"], p2["h"])
    out = page(L)
    check(out)
    OUT.write_text(out, encoding="utf-8", newline="\n")
    print("wrote", OUT, len(out.encode("utf-8")), "bytes")
    print("mid h @", MID_MIN, json.dumps(m2["h"]), "phone h @", PH_MIN, json.dumps(p2["h"]))
    print("Y", json.dumps({k: v["Y"] for k, v in L.items()}))
    print("desk h (board)", json.dumps(json.loads((DL / "models-r2" / "measure.json").read_text())["desktop"]["h"]))
    todo = list(a.check)
    for w in todo:
        try:
            r = measure(L, a.port, w)
        except RuntimeError as e:
            print("   ", e, "(retrying last)")
            if todo.count(w) < 2:
                todo.append(w)
            continue
        print(w, "dr", r["dr"], "docW", r["docW"], "secH", r["secH"], "devGap", r["devGap"], "h", json.dumps(r["h"]))
        for k in ("hit", "over", "clip"):
            if r[k]:
                print("   ", k, r[k])


if __name__ == "__main__":
    main()
