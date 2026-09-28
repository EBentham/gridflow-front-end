"""Architecture board 2, "The specimen": one row is the protagonist.

A compact section drawing of the whole system sits under the sky; below it the row's journey shows the one object
changing form stop by stop, with stop 5 drawn large as a timeline of its two versions.

Every fact, label and snippet comes from ``arch-pack`` (ARCH-PACK.md / pack.json). Lines this board adds that are
not pack wording are registered through ``N()`` and listed in the notes.

Usage: gen.py            probe (headless Chrome on 127.0.0.1:9703), then write the board at the measured height
"""
from __future__ import annotations

import html
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
A_DIR = HERE.parent.parent / "p27-r1" / "A"
sys.path.insert(0, str(A_DIR))

import frame  # noqa: E402
import hp  # noqa: E402
import scenery as sn  # noqa: E402
from hp import _frange, f, smooth  # noqa: E402

NAME = "arch-2"
PORT = 9703
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W = 1440

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, CLAY, KHAKI, MUTED = "#1C2B22", "#F6F4EC", "#C77E3C", "#A39A6A", "#5d6a55"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_BRONZE, T_TOP = "#E9DDAF", "#DCE2DF", "#E2CDB3", "#ECE8DA"
FAR, MIDR = "#297382", "#378390"
ON_SKY = "#F6F4EC"

GH = "https://github.com/EBentham/gridflow/blob/master/"
GHT = "https://github.com/EBentham/gridflow/tree/master/"
GM = "https://github.com/EBentham/gridflow-models/blob/main/"

NEW: list[str] = []


def N(s: str) -> str:
    """Register a line of copy that is not pack wording (for the notes)."""
    NEW.append(s)
    return s


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def gl(path: str, base: str = GH, short: bool = False) -> str:
    shown = path
    if short:
        shown = path.removeprefix("src/gridflow/") if base in (GH, GHT) else path.removeprefix("src/")
    return f'<a class="p" href="{base}{path}"><code>{esc(shown).replace("/", "/<wbr>")}</code></a>'


# =============================================================== code wells
SQL_KW = (r"CREATE OR REPLACE VIEW|SELECT|FROM|WHERE|AND|ORDER BY|QUALIFY|ROW_NUMBER|row_number|OVER|PARTITION BY|"
          r"DESC NULLS LAST|DESC|CASE|WHEN|THEN|ELSE|END|DATE|TIMESTAMPTZ|AS|TABLE|IF NOT EXISTS|CREATE|"
          r"PRIMARY KEY|NOT NULL|DEFAULT")
PY_KW = r"from|import|with|as"


def hl(code: str, lang: str) -> str:
    s = esc(code)
    if lang == "sql":
        pat = re.compile(r"('[^'\n]*')|\b(" + SQL_KW + r")\b")
        return pat.sub(lambda m: f'<span class="s">{m.group(1)}</span>' if m.group(1)
                       else f'<span class="k">{m.group(2)}</span>', s)
    if lang == "py":
        pat = re.compile(r'(#[^\n]*)|("[^"\n]*")|\b(' + PY_KW + r')\b')

        def rep(m: re.Match[str]) -> str:
            if m.group(1):
                return f'<span class="c">{m.group(1)}</span>'
            if m.group(2):
                return f'<span class="s">{m.group(2)}</span>'
            return f'<span class="k">{m.group(3)}</span>'
        return pat.sub(rep, s)
    if lang == "json":
        pat = re.compile(r'("[^"\n]*")(\s*:)?')
        return pat.sub(lambda m: m.group(0) if m.group(2) else f'<span class="s">{m.group(1)}</span>', s)
    return s


def well(code: str, lang: str = "text", cls: str = "", title: str = "", marks: tuple[str, ...] = ()) -> str:
    body = hl(code.strip("\n"), lang)
    for mk in marks:
        body = body.replace(mk, f'<mark class="sp">{mk}</mark>')
    t = f'<p class="wt">{title}</p>' if title else ""
    return f'{t}<pre class="well {cls}">{body}</pre>'


NUM = re.compile(r"^-?[\d.]+$")


def out_table(cols: list[str], rows: list[list[str]], mark: set[tuple[int, int]], cls: str = "",
              label: str = "output") -> str:
    ncls = ' class="n"'
    head = "".join(f'<th scope="col"{ncls if all(NUM.match(r[i]) for r in rows) else ""}>{c}</th>'
                   for i, c in enumerate(cols))
    body = ""
    for ri, r in enumerate(rows):
        cells = ""
        for ci, v in enumerate(r):
            n = ' class="n"' if NUM.match(v) else ""
            vv = f'<mark class="sp">{v}</mark>' if (ri, ci) in mark else v
            cells += f"<td{n}>{vv}</td>"
        body += f"<tr>{cells}</tr>"
    return (f'<div class="res {cls}" role="region" aria-label="{label}" tabindex="0"><table class="rt">'
            f'<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')


# =============================================================== drawing: geometry
S = 300                       # the ground surface in the drawing
H0 = S - 128                  # sea horizon
XA, XB = 776, 884             # the coasts
SEA = S + 6
LANES = [160 + 48 * i for i in range(8)]
LX = 540                      # label column in the drawing
DX, DRX, DRY = 348, 100, 13    # the catalogue drum
MX = 830                      # gridflow_models riser


def prof(x: float) -> float:
    return S + 3 * math.sin(x / 190 + .6) - 2 * math.sin(x / 83 + 1.3)


def cut(x: float) -> float:
    y = prof(x)
    if XA < x < XB:
        t = (x - XA) / (XB - XA)
        ramp = min(1.0, t / .22, (1 - t) / .22)
        ramp = ramp * ramp * (3 - 2 * ramp)
        y += ramp * (34 + 2 * math.sin(x / 17))
    return y


# the sources, west to east: (registered name, label, cable x, label x, label y, label anchor, label on sky)
SOURCES = [
    ("elexon", "Elexon", 205, 213, S - 70, "middle"),
    ("neso", "NESO carbon intensity", 340, 330, S - 124, "middle"),
    ("neso_data_portal", "NESO Data Portal", 550, 550, S - 88, "middle"),
    ("open_meteo", "Open-Meteo", 700, 684, S - 108, "end"),
    ("entsoe", "ENTSO-E", 955, 958, S - 74, "middle"),
    ("entsog", "ENTSO-G", 1090, 1092, S - 60, "middle"),
    ("gie_agsi", "GIE AGSI", 1202, 1204, S - 58, "middle"),
    ("gie_alsi", "GIE ALSI", 1356, 1352, S - 72, "middle"),
]
CONN = {
    "elexon": "src/gridflow/connectors/elexon/client.py",
    "entsoe": "src/gridflow/connectors/entsoe/client.py",
    "entsog": "src/gridflow/connectors/entsog/client.py",
    "neso": "src/gridflow/connectors/neso/carbon_intensity.py",
    "neso_data_portal": "src/gridflow/connectors/neso_data_portal/client.py",
    "gie_agsi": "src/gridflow/connectors/gie/client.py",
    "gie_alsi": "src/gridflow/connectors/gie/client.py",
    "open_meteo": "src/gridflow/connectors/openmeteo/client.py",
}


def pipestation(x: float, base: float) -> str:
    """A gas entry point: two buried mains rising through valves, a metering kiosk."""
    out = []
    for px, w, h in ((x, 40, 26), (x + 50, 30, 18)):
        d = (f"M{f(px)} {f(base + 2)} V{f(base - h + 8)} Q{f(px)} {f(base - h)} {f(px + 8)} {f(base - h)} "
             f"H{f(px + w - 8)} Q{f(px + w)} {f(base - h)} {f(px + w)} {f(base - h + 8)} V{f(base + 2)}")
        out.append(f'<path d="{d}" stroke="{INK}" stroke-width="7" fill="none"></path>'
                   f'<path d="{d}" stroke="{KHAKI}" stroke-width="4" fill="none"></path>')
        vx = px + w / 2
        out.append(f'<path d="M{f(vx)} {f(base - h - 3)} V{f(base - h - 11)} M{f(vx - 6)} {f(base - h - 11)} '
                   f'H{f(vx + 6)}" stroke="{INK}" stroke-width="1.6"></path>'
                   f'<rect x="{f(vx - 4)}" y="{f(base - h - 5)}" width="8" height="10" fill="{CLAY}" stroke="{INK}" '
                   f'stroke-width=".9"></rect>')
    out.append(f'<rect x="{f(x + 88)}" y="{f(base - 20)}" width="22" height="20" fill="{DAY}" stroke="{INK}" '
               f'stroke-width="1"></rect><path d="M{f(x + 86)} {f(base - 20)} H{f(x + 112)}" stroke="{INK}" '
               f'stroke-width="2"></path><rect x="{f(x + 93)}" y="{f(base - 13)}" width="7" height="13" fill="{INK}" '
               f'opacity=".75"></rect>')
    return "\n".join(out)


def landscape() -> str:
    hp.Y["surf"] = S
    p: list[str] = []
    sea = f"M700 {H0} H990 V{SEA + 40} H700 Z"
    p.append(f'<path d="{sea}" fill="{HORIZON}"></path>')
    p.append(sn.ridge([(-20, S - 198), (140, S - 222), (320, S - 208), (500, S - 228), (640, S - 206),
                       (700, S - 170), (744, S - 138), (762, S - 128)], S - 30, FAR))
    p.append(sn.ridge([(926, S - 128), (960, S - 150), (1060, S - 188), (1200, S - 178), (1330, S - 198),
                       (1460, S - 186)], S - 30, FAR))
    p.append(sn.wavelets([(806, H0 + 12, 26), (852, H0 + 20, 20), (828, H0 + 40, 30), (812, H0 + 70, 22),
                          (858, H0 + 96, 28), (820, H0 + 122, 18)]))
    for i, (ox, oh) in enumerate([(812, 20), (838, 23), (864, 20)]):
        p.append(hp.turbine(ox, H0 + 7 + (i % 2) * 2, oh, oh * .5, ["sp1", "sp2", "sp3"][i % 3], 23 * i))
    near = [(-20, S - 166), (80, S - 184), (200, S - 192), (330, S - 176), (450, S - 196), (590, S - 182),
            (690, S - 160), (750, S - 140), (790, S - 122)]
    p.append(sn.ridge(near, S - 60, HORIZON))
    for i, (tx, ty) in enumerate(near[1:6]):
        hgt = [62, 68, 58, 70, 64][i]
        p.append(hp.turbine(tx, ty + 3, hgt, hgt * .5, ["sp2", "sp1", "sp3"][i % 3], 40 * i + 10))
    p.append(sn.ridge([(900, S - 128), (990, S - 140), (1110, S - 150), (1240, S - 144), (1360, S - 160),
                       (1460, S - 150)], S - 40, MIDR))
    gb_top = [(-20, S - 138), (160, S - 146), (340, S - 136), (520, S - 144), (650, S - 134), (730, S - 104),
              (762, S - 58), (774, S - 14), (XA + 4, SEA)]
    p.append(sn.field(gb_top, prof, -20, XA + 4,
                      [[(-20, S - 112), (300, S - 116), (560, S - 108), (720, S - 86)],
                       [(-20, S - 80), (400, S - 84), (700, S - 62)], [(200, S - 44), (500, S - 48), (740, S - 34)]]))
    eu_top = [(XB - 4, SEA), (XB + 8, S - 40), (920, S - 88), (1000, S - 102), (1160, S - 112), (1280, S - 104),
              (1460, S - 98)]
    p.append(sn.field(eu_top, prof, XB - 4, 1460,
                      [[(920, S - 76), (1200, S - 82), (1460, S - 78)], [(930, S - 40), (1250, S - 46), (1460, S - 42)]]))
    return "\n".join(p)


def water_and_near() -> str:
    xs = [x / 2 for x in range(2 * XA, 2 * XB + 1)]
    wet = [(x, cut(x)) for x in xs if cut(x) > SEA + .5]
    water = (f"M{f(wet[0][0])} {SEA} " + " ".join(f"L{f(x)} {f(y)}" for x, y in wet[::3] + [wet[-1]])
             + f" L{f(wet[-1][0])} {SEA} Z")
    out = [f'<path d="{water}" fill="{HORIZON}"></path>'
           f'<path d="M{f(wet[0][0])} {SEA} H{f(wet[-1][0])}" stroke="{DAY}" stroke-width="1.2" opacity=".6"></path>',
           sn.monopile_turbine(830, SEA, cut(830), 92, "sp1", 30)]
    return "\n".join(out)


def assets() -> str:
    p = []
    p.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">'
             f'{hp.pylon(96, prof(96) - 2, .56)}</g>')
    sub_x, sub_s = 150, 1.1
    sb = prof(sub_x + 50)
    sub_svg, ends = hp.substation(sub_x, sb)
    ends = [(sub_x + (ex - sub_x) * sub_s, sb + (ey - sb) * sub_s) for ex, ey in ends]
    p.append(hp.sc(sub_svg, sub_x, sb, sub_s))
    wires = [hp.spans([(-20, S - 140), (-20, S - 152), (-20, S - 162)], hp.tips(96, prof(96) - 2, .56, -1), 6),
             hp.spans(hp.tips(96, prof(96) - 2, .56, 1), ends, 8)]
    p.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')
    p.append(hp.ccgt(304, prof(340), .95))
    p.append(sn.solar_farm_at(462, 640, prof))
    p.append(hp.metmast(700, prof(700), 132))
    p.append(hp.sc(hp.converter(918, prof(960)), 918, prof(960), 1.0))
    p.append(pipestation(1040, prof(1090)))
    p.append(hp.gasterminal(1150, prof(1200)))
    p.append(hp.sc(sn.lng_terminal(1296, prof(1356)), 1296, prof(1356), .86))
    return "\n".join(p)


# =============================================================== drawing: below ground
def wave_d(y0: float, amp: float, seed: float) -> str:
    return smooth(hp.wave(y0, amp, seed))


def wave_y(y0: float, amp: float, seed: float, x: float) -> float:
    return y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3)


def run(x0: float, y0: float, d: float, lane: float, y1: float, r: float = 12) -> str:
    if abs(x0 - lane) < .5:
        return f"M{f(x0)} {f(y0)} V{f(y1)}"
    r = min(r, abs(x0 - lane) / 2, (d - y0) / 2)
    s = -1 if lane < x0 else 1
    return (f"M{f(x0)} {f(y0)} V{f(d - r)} Q{f(x0)} {f(d)} {f(x0 + s * r)} {f(d)} H{f(lane - s * r)} "
            f"Q{f(lane)} {f(d)} {f(lane)} {f(d + r)} V{f(y1)}")


def housing(x: float, y: float) -> str:
    return (f'<rect x="{f(x - 10)}" y="{f(y)}" width="20" height="30" rx="2" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="1.4"></rect><path d="M{f(x - 5)} {f(y + 9)} H{f(x + 5)} M{f(x - 5)} {f(y + 14)} '
            f'H{f(x + 5)} M{f(x - 5)} {f(y + 19)} H{f(x + 5)}" stroke="{INK}" stroke-width=".8" opacity=".55"></path>')


def doc(x: float, y: float, w: float, h: float, fill: str) -> str:
    c = min(6.0, w / 3)
    lines = " ".join(f"M{f(x + 3)} {f(y + 7 + 4 * k)} H{f(x + w - 4)}" for k in range(int((h - 9) / 4)))
    return (f'<path d="M{f(x)} {f(y)} H{f(x + w - c)} L{f(x + w)} {f(y + c)} V{f(y + h)} H{f(x)} Z" fill="{fill}" '
            f'stroke="{INK}" stroke-width=".9" stroke-linejoin="round"></path>'
            f'<path d="{lines}" stroke="{INK}" stroke-width=".6" opacity=".4"></path>')


def filestack(x: float, y: float) -> str:
    """Two captures: each a raw body with its .meta.json sidecar."""
    out = []
    for dx, dy in ((-9, 0), (-3, 7)):
        out.append(doc(x + dx - 6, y + dy, 17, 22, DAY))
        out.append(doc(x + dx + 8, y + dy + 9, 10, 13, T_TOP))
    return "".join(out)


def slab(x: float, y: float, fill: str, n: int = 2) -> str:
    out = []
    for k in range(n):
        yy = y + k * 11
        out.append(f'<rect x="{f(x - 20)}" y="{f(yy)}" width="40" height="9" fill="{fill}" stroke="{INK}" '
                   f'stroke-width=".9"></rect>')
        out.append(f'<path d="{" ".join(f"M{f(x + c)} {f(yy + 1)} V{f(yy + 8)}" for c in (-10, 0, 10))}" '
                   f'stroke="{INK}" stroke-width=".6" opacity=".38"></path>')
    return "".join(out)


def drum_top_y(x: float, top: float) -> float:
    return top - DRY * math.sqrt(max(0.0, 1 - ((x - DX) / DRX) ** 2))


def drum(top: float, bot: float) -> str:
    l, r = DX - DRX, DX + DRX
    body = (f'<path d="M{f(l)} {f(top)} V{f(bot)} A{DRX} {DRY} 0 0 0 {f(r)} {f(bot)} V{f(top)} Z" fill="{DAY}" '
            f'stroke="{INK}" stroke-width="1.5"></path>')
    lid = (f'<ellipse cx="{DX}" cy="{f(top)}" rx="{DRX}" ry="{DRY}" fill="{DAY}" stroke="{INK}" '
           f'stroke-width="1.5"></ellipse>')
    bands = "".join(f'<path d="M{f(l)} {f(y)} A{DRX} {DRY} 0 0 0 {f(r)} {f(y)}" stroke="{INK}" stroke-width=".8" '
                    f'fill="none" opacity=".45"></path>' for y in (top + 38, top + 80))
    return body + lid + bands


# reader glyphs, each drawn from its top-left corner
def g_cli(x: float, y: float) -> str:
    return (f'<rect x="{f(x)}" y="{f(y)}" width="92" height="58" rx="3" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="1.5"></rect><path d="M{f(x)} {f(y + 11)} H{f(x + 92)}" stroke="{INK}" '
            f'stroke-width="1.2"></path><rect x="{f(x + .75)}" y="{f(y + .75)}" width="90.5" height="10" rx="2" '
            f'fill="{INK}"></rect>'
            f'<path d="M{f(x + 9)} {f(y + 22)} l6 5 l-6 5 M{f(x + 20)} {f(y + 32)} H{f(x + 66)} M{f(x + 9)} '
            f'{f(y + 44)} H{f(x + 48)}" stroke="{INK}" stroke-width="1.4" fill="none"></path>')


def g_client(x: float, y: float) -> str:
    out = [f'<rect x="{f(x)}" y="{f(y)}" width="84" height="58" rx="3" fill="{DAY}" stroke="{INK}" '
           f'stroke-width="1.5"></rect>',
           f'<rect x="{f(x + 1)}" y="{f(y + 1)}" width="82" height="13" fill="{T_TOP}"></rect>',
           f'<path d="M{f(x)} {f(y + 14)} H{f(x + 84)}" stroke="{INK}" stroke-width="1.2"></path>']
    for k in range(3):
        yy = y + 14 + k * 14.5
        if k % 2 == 0:
            out.append(f'<rect x="{f(x + 1)}" y="{f(yy + .5)}" width="82" height="14" fill="#EFEBDF"></rect>')
    out.append(f'<path d="M{f(x + 28)} {f(y + 1)} V{f(y + 57)} M{f(x + 56)} {f(y + 1)} V{f(y + 57)}" '
               f'stroke="{INK}" stroke-width=".7" opacity=".4"></path>')
    out.append(f'<path d="{" ".join(f"M{f(x + c)} {f(y + 8 + r * 14.5)} h14" for c in (8, 36, 64) for r in range(4))}" '
               f'stroke="{INK}" stroke-width="1.6" opacity=".7"></path>')
    return "".join(out)


def g_notebook(x: float, y: float) -> str:
    return (f'<rect x="{f(x)}" y="{f(y)}" width="92" height="58" rx="3" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="1.5"></rect><rect x="{f(x + .75)}" y="{f(y + .75)}" width="90.5" height="9" rx="2" '
            f'fill="{INK}"></rect><rect x="{f(x + 6)}" y="{f(y + 3)}" width="22" height="7" fill="{DAY}"></rect>'
            f'<rect x="{f(x + 20)}" y="{f(y + 16)}" width="64" height="12" fill="{T_TOP}" stroke="{INK}" '
            f'stroke-width=".7"></rect><rect x="{f(x + 20)}" y="{f(y + 34)}" width="64" height="16" fill="{T_TOP}" '
            f'stroke="{INK}" stroke-width=".7"></rect><path d="M{f(x + 6)} {f(y + 23)} h9 M{f(x + 6)} {f(y + 43)} h9 '
            f'M{f(x + 24)} {f(y + 22)} h34 M{f(x + 24)} {f(y + 40)} h48 M{f(x + 24)} {f(y + 45)} h26" '
            f'stroke="{INK}" stroke-width=".9" opacity=".55"></path>')


def g_models(x: float, y: float) -> str:
    xs = [x + 12 + 8 * i for i in range(10)]
    mid = [y + 38 - 14 * math.sin(i / 3.2) + i * .6 for i in range(10)]
    wid = [3 + 1.6 * i for i in range(10)]
    band = (f"M{f(xs[0])} {f(mid[0] - wid[0])} " + " ".join(f"L{f(a)} {f(m - w_)}" for a, m, w_ in zip(xs, mid, wid))
            + " " + " ".join(f"L{f(a)} {f(m + w_)}" for a, m, w_ in reversed(list(zip(xs, mid, wid)))) + " Z")
    line = "M" + " L".join(f"{f(a)} {f(m)}" for a, m in zip(xs, mid))
    return (f'<rect x="{f(x)}" y="{f(y)}" width="96" height="58" rx="3" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="1.5"></rect><path d="{band}" fill="{HORIZON}" opacity=".35"></path>'
            f'<path d="{line}" stroke="{INK}" stroke-width="1.4" fill="none"></path>'
            f'<path d="M{f(x + 8)} {f(y + 8)} V{f(y + 51)} H{f(x + 90)}" stroke="{INK}" stroke-width="1" '
            f'fill="none"></path>')


def terminal(x: float, y: float, tint: str = T_BRONZE, r: float = 5.5) -> str:
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{tint}" stroke="{INK}" stroke-width="1.8"></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r / 3)}" fill="{INK}"></circle>')


def cab(d: str, core: str) -> str:
    if core == CHART:
        return hp.cable(d, core, 5.2, 2.3)
    return hp.cable(d, core, 4.4, 1.5)


def drawing_svg(b: dict) -> str:
    C1, C2, C3, G0, R, BOT, Hd = b["C1"], b["C2"], b["C3"], b["G0"], b["R"], b["BOT"], b["Hd"]
    TAP = C3 - 44
    DT, DB = C3 - 62, C3 + 60
    o: list[str] = [f'<rect x="0" y="0" width="{W}" height="{S + 80}" fill="{PETROL}"></rect>', landscape()]
    # ground: topsoil from the surface down, then each stratum from its contact
    surf = [(x, cut(x)) for x in range(-40, W + 41, 8)]
    surf_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    tail = f" L{W + 40} {Hd + 10} L-40 {Hd + 10} Z"
    o.append(f'<path d="{surf_d}{tail}" fill="{T_TOP}"></path><path d="{surf_d}{tail}" fill="url(#p-soil)" '
             f'opacity=".5"></path>')
    root = surf_d + " " + " ".join(f"L{f(x)} {f(y + 8)}" for x, y in reversed(surf)) + " Z"
    o.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    lines = []
    for y0, (amp, seed), fill, pid, op in ((C1, (7, .4), T_BRONZE, "p-brick", ".15"),
                                           (C2, (8, 2.1), T_SILVER, "p-diag", ".22"),
                                           (C3, (7, 4.0), T_GOLD, "p-stip", ".26")):
        d = wave_d(y0, amp, seed)
        o.append(f'<path d="{d}{tail}" fill="{fill}"></path><path d="{d}{tail}" fill="url(#{pid})" '
                 f'opacity="{op}"></path>')
        lines.append(d)
    dbot = wave_d(BOT, 6, 1.3)
    o.append(f'<path d="{dbot}{tail}" fill="{DAY}"></path>')
    lines.append(dbot)
    o.append(water_and_near())
    o.append(f'<path d="{surf_d}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    o.append(f'<path d="{" ".join(lines)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    o.append(assets())

    # ---- topsoil: one cable per source, nested so none cross, each to its own connector
    HT = C1 - 64
    for i, (key, _lab, x, *_r) in enumerate(SOURCES):
        lane = LANES[i]
        core = CHART if key == "elexon" else BRONZE
        o.append(cab(run(x, prof(x) + 12, S + 30 + 9 * i, lane, HT), core))
    for i, (key, _lab, x, *_r) in enumerate(SOURCES):
        o.append(terminal(x, prof(x) + 12))
    # ---- connector to bronze: raw bytes plus a sidecar
    for i, lane in enumerate(LANES):
        core = CHART if i == 0 else BRONZE
        o.append(cab(f"M{lane} {f(HT + 30)} V{f(C1 + 40)}", core))
        o.append(housing(lane, HT))
        o.append(frame.sleeve(lane, wave_y(C1, 7, .4, lane), T_BRONZE))
        o.append(filestack(lane, C1 + 38))
    # ---- bronze to silver: typed transformers
    for i, lane in enumerate(LANES):
        core = CHART if i == 0 else SILVER
        o.append(cab(f"M{lane} {f(C1 + 72)} V{f(C2 + 44)}", core))
        o.append(frame.sleeve(lane, wave_y(C2, 8, 2.1, lane), T_SILVER))
    # ---- silver: views to the catalogue (hairlines, plain views), the builder's own cable to gold
    hair = []
    for i, lane in enumerate(LANES):
        tx = DX - 63 + 18 * i
        hair.append(f"M{lane} {f(C2 + 66)} L{f(tx)} {f(drum_top_y(tx, DT))}")
    hair.append(f"M{f(LANES[0] + 20)} {f(C3 + 58)} L{f(DX - DRX)} {f(C3 + 44)}")
    o.append(f'<path d="{" ".join(hair)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".7"></path>')
    o.append(cab(f"M{LANES[0]} {f(C2 + 66)} V{f(C3 + 46)}", CHART))
    o.append(frame.sleeve(LANES[0], wave_y(C3, 7, 4.0, LANES[0]), T_GOLD))
    for i, lane in enumerate(LANES):
        o.append(slab(lane, C2 + 44, SILVER))
    o.append(slab(LANES[0], C3 + 46, GOLD))
    # ---- readers at the foot
    cx = 80 + 46
    o.append(cab(f"M{f(cx)} {f(G0)} V{f(C3 + 124)} Q{f(cx)} {f(C3 + 112)} {f(cx + 12)} {f(C3 + 112)} "
                 f"H{f(DX - 54)} Q{f(DX - 42)} {f(C3 + 112)} {f(DX - 42)} {f(C3 + 100)} V{f(DB)}", BRONZE))
    o.append(cab(f"M{f(420)} {f(G0)} V{f(DB)}", CHART))
    o.append(cab(f"M{f(720)} {f(G0 + 30)} H{f(484)}", BRONZE))
    o.append(cab(f"M{f(1040)} {f(G0 + 30)} H{f(MX + 12)} Q{f(MX)} {f(G0 + 30)} {f(MX)} {f(G0 + 18)} V{f(TAP)}",
                 SILVER))
    o.append(frame.sleeve(MX, wave_y(C3, 7, 4.0, MX), T_SILVER))
    o.append(terminal(MX, TAP, T_SILVER))
    o.append(drum(DT, DB))
    o.append(g_cli(80, G0))
    o.append(g_client(400, G0))
    o.append(g_notebook(720, G0))
    o.append(g_models(1040, G0))

    # ---- labels (short; the keyed index carries the lines)
    lab: list[str] = []
    for key, name, x, lx, ly, anc in SOURCES:
        lab.append(f'<text x="{lx}" y="{f(ly)}" text-anchor="{anc}" class="v">{name}</text>')
    mid_views = (C2 + 70 + DT) / 2
    lab += [
        f'<text x="{LX}" y="{f(HT - 22)}">async requests, capped and retried</text>',
        f'<text x="{LX}" y="{f(HT + 20)}">connectors</text>',
        f'<text x="{LX}" y="{f(C1 + 26)}">raw bytes plus a sidecar</text>',
        f'<text x="{LX}" y="{f(C1 + 60)}">bronze: raw responses by date</text>',
        f'<text x="{LX}" y="{f(C2 + 26)}">typed transformers stamp every row</text>',
        f'<text x="{LX}" y="{f(C2 + 60)}">silver: typed Parquet, Hive-partitioned</text>',
        f'<text x="{LX}" y="{f(mid_views + 4)}">DuckDB views over Parquet</text>',
        f'<text x="{MX - 14}" y="{f(TAP - 4)}" text-anchor="end">{N("reads silver Parquet directly,")}</text>',
        f'<text x="{MX - 14}" y="{f(TAP + 13)}" text-anchor="end">{N("as of a time")}</text>',
        f'<text x="{LX}" y="{f(C3 + 60)}">gold: a builder and SQL views</text>',
        f'<text x="{DX}" y="{f(DT + 26)}" text-anchor="middle" class="m b">gridflow.duckdb</text>',
        f'<text x="{DX}" y="{f(DT + 60)}" text-anchor="middle" class="m s">silver_{{source}}_{{dataset}}</text>',
        f'<text x="{DX}" y="{f(DT + 103)}" text-anchor="middle" class="m s">gold_uk_imbalance_context</text>',
        f'<text x="{LANES[0]}" y="{f(C3 + 88)}" text-anchor="middle" class="m s">system_marginal_price</text>',
    ]
    aria = N("Section drawing of gridflow. Above ground, the vendor sources stand as the assets they report on: "
             "Elexon at a substation, NESO carbon intensity at a gas-fired power station, the NESO Data Portal at a "
             "solar farm and Open-Meteo at a met mast on the British side; ENTSO-E at a converter station, ENTSO-G at "
             "a gas entry point, GIE AGSI at storage tanks and GIE ALSI at an LNG terminal across the sea. A cable "
             "runs down from each through its own connector into bronze, where each response is kept as a file with a "
             "sidecar; transformers carry each on into silver Parquet. Plain views gather every silver dataset into "
             "one DuckDB file that straddles silver and gold; the Elexon cable also runs on to the gold builder. At "
             "the foot, the gridflow command and GridflowClient read that file, notebooks read through the client, "
             "and gridflow_models reads silver Parquet directly as of a time.")
    return (f'<svg class="dr" width="{W}" height="{Hd}" viewBox="0 0 {W} {Hd}" role="img" aria-label="{aria}">'
            f'<defs>{hp.PATTERNS}</defs>\n' + "\n".join(o) + '\n<g class="lab">' + "".join(lab) + "</g></svg>")


# =============================================================== keyed index
def mk(kind: str) -> str:
    """A small mark copied from the drawing part an entry names."""
    w, h = 34, 22
    inner = ""
    if kind == "term":
        inner = terminal(17, 11, T_BRONZE, 6)
    elif kind == "cable":
        inner = cab("M3 11 H31", BRONZE)
    elif kind in ("sl-b", "sl-s"):
        fill = T_BRONZE if kind == "sl-b" else T_SILVER
        core = BRONZE if kind == "sl-b" else SILVER
        inner = cab("M2 11 H32", core) + frame.sleeve(17, 11, fill, vertical=False)
    elif kind in ("b", "s", "g"):
        fill, pid, pat = {"b": (T_BRONZE, "k-b", '<pattern id="k-b" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" fill="none"></path></pattern>'),
                          "s": (T_SILVER, "k-s", '<pattern id="k-s" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" stroke="#5E6E6B" stroke-width=".8"></path></pattern>'),
                          "g": (T_GOLD, "k-g", '<pattern id="k-g" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" fill="#8A6F1E"></circle></pattern>')}[kind]
        inner = (f"<defs>{pat}</defs><rect x=\".75\" y=\".75\" width=\"{w - 1.5}\" height=\"{h - 1.5}\" fill=\"{fill}\"></rect>"
                 f"<rect x=\".75\" y=\".75\" width=\"{w - 1.5}\" height=\"{h - 1.5}\" fill=\"url(#{pid})\" opacity=\".5\"></rect>"
                 f"<rect x=\".75\" y=\".75\" width=\"{w - 1.5}\" height=\"{h - 1.5}\" fill=\"none\" stroke=\"{INK}\" stroke-width=\"1.5\"></rect>")
    elif kind == "hair":
        inner = f'<path d="M3 3 L17 19 M12 3 L17 19 M22 3 L17 19 M31 3 L17 19" stroke="{INK}" stroke-width=".9" fill="none"></path>'
    elif kind == "drum":
        inner = (f'<path d="M5 5 V17 A12 3.5 0 0 0 29 17 V5 Z" fill="{DAY}" stroke="{INK}" stroke-width="1.3"></path>'
                 f'<ellipse cx="17" cy="5" rx="12" ry="3.5" fill="{DAY}" stroke="{INK}" stroke-width="1.3"></ellipse>')
    return f'<svg class="mk" width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">{inner}</svg>'


def entry(mark: str, name: str, line: str, links: str) -> str:
    return (f'<li class="ke">{mk(mark)}<div><h3 class="kn">{name}</h3><p class="kl">{line}</p>'
            f'<p class="kk">{links}</p></div></li>')


def index_groups() -> dict[str, str]:
    srcs = " ".join(f'<a href="{GH}{CONN[k]}"><code>{k}</code></a>' for k, *_r in SOURCES)
    g: dict[str, str] = {}
    g["sky"] = (
        entry("term", "The sources",
              "Each registered source has its own connector; <code>gie_agsi</code> and <code>gie_alsi</code> "
              "share one file, and every connector module is imported from one list in <code>pipeline/runner.py</code>.",
              f'<span class="srcs">{srcs}</span>'))
    g["top"] = (
        entry("cable", "Async requests, capped and retried",
                "One async httpx client per source; a semaphore caps requests in flight; tenacity retries with "
                "jittered backoff.",
                gl("src/gridflow/connectors/base.py", short=True) + " " + gl("src/gridflow/utils/retry.py", short=True)))
    g["bronze"] = (
        entry("sl-b", "Raw bytes plus a sidecar",
              "Each response is stored byte for byte with a <code>.meta.json</code> sidecar; both land by temp file "
              "and atomic rename.", gl("src/gridflow/bronze/writer.py", short=True))
        + entry("b", "Bronze: raw responses by date",
                "<code>bronze/{source}/<wbr>{dataset}/<wbr>{YYYY}/{MM}/{DD}/<wbr>raw_{fetched_at}_{hash8}.json</code>, "
                "one file per response page.", gl("src/gridflow/bronze/writer.py", short=True)))
    g["silver"] = (
        entry("sl-s", "Typed transformers stamp every row",
              "One Polars transformer per dataset: strict types, UTC, Pydantic checks counted not raised, then "
              "<code>available_at</code>, <code>source_run_id</code>, <code>dataset_version</code>.",
              gl("src/gridflow/silver/base.py", short=True) + " " + gl("src/gridflow/silver/elexon/system_prices.py", short=True))
        + entry("s", "Silver: typed Parquet, Hive-partitioned",
                "<code>silver/{source}/<wbr>{dataset}/<wbr>year=YYYY/<wbr>month=MM/</code>; append-only datasets keep "
                "one file per capture, suffixed <code>_run{capture time}</code>.",
                gl("src/gridflow/storage/paths.py", short=True) + " " + gl("src/gridflow/silver/base.py", short=True))
        + entry("hair", "DuckDB views over Parquet",
                "One view per dataset over <code>read_parquet</code> with Hive partitioning; append-only datasets also "
                "get a <code>_latest</code> view.",
                gl("src/gridflow/storage/duckdb.py", short=True) + " " + gl("src/gridflow/silver/latest_views.py", short=True)))
    g["gold"] = (
        entry("drum", "One file: <code>gridflow.duckdb</code>",
              "Views over the Parquet, plus the <code>pipeline_runs</code>, <code>pipeline_watermarks</code> and "
              "<code>quality_reports</code> tables. No server.", gl("src/gridflow/storage/duckdb.py", short=True))
        + entry("g", "Gold: a builder and SQL views",
                "Polars builder <code>system_marginal_price</code>; SQL views <code>gold_uk_imbalance_context</code>, "
                "<code>gold_gb_day_ahead_benchmark</code>, <code>gold_eu_gas_storage</code>.",
                gl("src/gridflow/gold/system_marginal_price.py", short=True) + " " + gl("src/gridflow/gold/views", GHT, short=True)))
    return g


def readers() -> str:
    verbs = " ".join(f"<code>{v}</code>" for v in ["init", "ingest", "transform", "build", "pipeline", "backfill",
                                                    "export-csv", "status", "quality", "reset", "prune"])
    cols = [
        ("The gridflow command", f'<span class="verbs">{verbs}</span>', gl("src/gridflow/cli.py", short=True)),
        ("<code>GridflowClient</code>, read-only, returns Polars",
         "<code>from gridflow.serving.client import GridflowClient</code>: <code>query</code>, "
         "<code>get_system_prices</code>, <code>get_imbalance_context</code>, <code>get_gas_storage</code> and more.",
         gl("src/gridflow/serving/client.py", short=True)),
        ("Notebooks", "Any notebook can open a <code>GridflowClient</code>; the gridflow_models workbench notebooks "
                      "do, through their setup helper.",
         gl("src/gridflow_models/research/notebook_setup.py", GM, short=True)),
        ("gridflow_models, reading as of a time",
         "Training and backtests read silver Parquet directly, keeping only rows whose <code>available_at</code> is at "
         "or before the as-of time.",
         gl("src/gridflow_models/data/gridflow_source.py", GM, short=True) + ' <a class="more" href="models.html">'
         + N("The Models page") + "</a>"),
    ]
    li = "".join(f'<li><h3 class="kn">{n}</h3><p class="kl">{t}</p><p class="kk">{k}</p></li>' for n, t, k in cols)
    return f'<ul class="rdx" data-g="readers">{li}</ul>'


# =============================================================== stop 5: the timeline
def timeline() -> str:
    Wt, Ht = 1200, 372
    k, x0 = 22.5, 130

    def X(h: float) -> float:
        return x0 + k * h

    t1 = 5 + 48.75 / 60                     # 2026-09-08 17:48:45
    t2 = 24 + 5 + 44.4833 / 60              # 2026-09-09 17:44:29
    tc1 = 9 + 44.05 / 60                    # bronze fetch 2026-09-08 21:44:03
    tq = 24.0                               # the as-of time, 2026-09-09 12:00
    XC2, XL, XE = 1040.0, 1150.0, 1190.0    # second capture (16 Sep), the _latest read, the right edge
    L1, L2, AX = 128, 204, 290
    o: list[str] = []
    # lanes: every row stays in the base view
    o.append(f'<path d="M{f(X(t1))} {L1} H{XE} M{f(X(t2))} {L2} H{XE}" stroke="{INK}" stroke-width="1.3"></path>')
    # the winner at each moment
    o.append(f'<rect x="{f(X(t1))}" y="{L1 - 12}" width="{f(X(t2) - X(t1))}" height="24" rx="2" fill="{CHART}" '
             f'stroke="{INK}" stroke-width="1.5"></rect>')
    o.append(f'<rect x="{f(X(t2))}" y="{L2 - 12}" width="{f(XE - X(t2))}" height="24" rx="2" fill="{CHART}" '
             f'stroke="{INK}" stroke-width="1.5"></rect>')
    o.append(f'<path d="M{f(X(t2))} {L1 + 12} V{L2 - 12}" stroke="{INK}" stroke-width="2"></path>')
    # time hairlines from each row's available_at to the axis
    o.append(f'<path d="M{f(X(t1))} {L1 + 12} V{AX} M{f(X(t2))} {L2 + 12} V{AX}" stroke="{INK}" stroke-width=".8" '
             f'opacity=".55"></path>')
    # axis with a break between 10 and 16 September
    o.append(f'<path d="M{x0} {AX} H{f(X(36) + 14)} M{f(X(36) + 34)} {AX} H{XE}" stroke="{INK}" '
             f'stroke-width="1.5"></path>')
    bx = X(36) + 24
    o.append(f'<path d="M{f(bx - 9)} {AX + 7} l6 -14 M{f(bx + 1)} {AX + 7} l6 -14" stroke="{INK}" '
             f'stroke-width="1.5"></path>')
    ticks = [(0, "12:00", "8 Sep"), (6, "18:00", ""), (12, "00:00", "9 Sep"), (18, "06:00", ""), (24, "12:00", ""),
             (30, "18:00", ""), (36, "00:00", "10 Sep")]
    tk = " ".join(f"M{f(X(h))} {AX} v6" for h, *_ in ticks)
    o.append(f'<path d="{tk}" stroke="{INK}" stroke-width="1.2"></path>')
    txt: list[str] = []
    for h, hh, day in ticks:
        txt.append(f'<text x="{f(X(h))}" y="{AX + 22}" text-anchor="middle" class="tk">{hh}</text>')
        if day:
            txt.append(f'<text x="{f(X(h))}" y="{AX + 40}" text-anchor="middle" class="tk">{day}</text>')
    txt.append(f'<text x="{XE}" y="{AX + 22}" text-anchor="end" class="tk">UTC</text>')
    # the two bronze captures, at their fetch times
    for cx, stamp in ((X(tc1), "20260908T214403Z"), (XC2, "20260916T190532Z")):
        o.append(doc(cx - 6, AX + 5, 12, 15, DAY))
        txt.append(f'<text x="{f(cx)}" y="{AX + 58}" text-anchor="middle">{N("bronze capture")}</text>')
        txt.append(f'<text x="{f(cx)}" y="{AX + 75}" text-anchor="middle" class="m">{stamp}</text>')
    # values on the bars, the available_at of each row beneath
    txt.append(f'<text x="{f(X(t1) + 12)}" y="{L1 + 4.5}" class="m v">system_sell_price 9.56</text>')
    txt.append(f'<text x="{f(X(t2) + 12)}" y="{L2 + 4.5}" class="m v">system_sell_price 110.0</text>')
    txt.append(f'<text x="{f(X(t1) + 7)}" y="{L1 + 32}" class="m">available_at 2026-09-08 17:48:45 UTC</text>')
    txt.append(f'<text x="{f(X(t2) + 7)}" y="{L2 + 32}" class="m">available_at 2026-09-09 17:44:29 UTC</text>')
    txt.append(f'<text x="0" y="{L1 + 5}">{N("first version")}</text>')
    txt.append(f'<text x="0" y="{L2 + 5}">{N("revision")}</text>')
    txt.append(f'<text x="{f(X(t2) + 14)}" y="{L1 - 8}">{N("still in")} <tspan class="m">silver_elexon_system_prices'
               f'</tspan></text>')
    # the as-of read (consumer side) and the _latest view
    xq = X(tq)
    o.append(f'<path d="M{f(xq)} 60 V{AX}" stroke="{INK}" stroke-width="1.5"></path>'
             f'<circle cx="{f(xq)}" cy="{L1}" r="8" fill="none" stroke="{INK}" stroke-width="2"></circle>')
    txt.append(f'<text x="{f(xq)}" y="30" text-anchor="middle">{N("as-of read at")} <tspan class="m">'
               f'2026-09-09 12:00 UTC</tspan></text>')
    txt.append(f'<text x="{f(xq)}" y="49" text-anchor="middle">{N("as gridflow_models applies it")}</text>')
    txt.append(f'<text x="{f(xq + 14)}" y="{L1 - 20}">{N("returns")} <tspan class="m">9.56</tspan></text>')
    o.append(f'<path d="M{XL} 60 V{L2}" stroke="{INK}" stroke-width="1.5"></path>'
             f'<circle cx="{XL}" cy="{L2}" r="8" fill="none" stroke="{INK}" stroke-width="2"></circle>')
    txt.append(f'<text x="{XE}" y="30" text-anchor="end" class="m">silver_elexon_system_prices_latest</text>')
    txt.append(f'<text x="{XE}" y="49" text-anchor="end">{N("the current best value")}</text>')
    txt.append(f'<text x="{XL - 14}" y="{L2 - 20}" text-anchor="end">{N("returns")} <tspan class="m">110.0</tspan>'
               f'</text>')
    aria = N("Timeline of the two versions of Elexon system_prices for settlement date 2026-09-08, period 37, "
             "from 8 September 12:00 to 10 September 00:00 UTC, then 16 September. The first version, 9.56, is "
             "available from 17:48:45 on 8 September; the revision, 110.0, from 17:44:29 on 9 September. Both rows "
             "stay in the base view. An as-of read at 12:00 on 9 September returns 9.56; the _latest view returns "
             "110.0. The bronze captures were fetched at 21:44:03 on 8 September and 19:05:32 on 16 September.")
    return (f'<svg class="tl" width="{Wt}" height="{Ht}" viewBox="0 0 {Wt} {Ht}" role="img" aria-label="{aria}">'
            + "".join(o) + '<g class="lab">' + "".join(txt) + "</g></svg>")


# =============================================================== journey
SWATCH = {
    "sky": (PETROL, ""), "top": (T_TOP, "p-soil"), "bronze": (T_BRONZE, "p-brick"), "silver": (T_SILVER, "p-diag"),
    "gold": (T_GOLD, "p-stip"),
}


def part(kind: str) -> tuple[str, str, float]:
    """A copy of one drawing part: (svg inner, viewBox, display width at 30 px high)."""
    if kind == "cli":
        return g_cli(1, 1), "0 0 94 60", 47
    if kind == "conn":
        return cab("M12 -6 V44", CHART) + housing(12, 4), "-2 -2 28 42", 20
    if kind == "files":
        return filestack(18, 1), "0 0 38 32", 36
    if kind == "slab":
        return slab(22, 5, SILVER), "0 0 44 28", 47
    if kind == "drum":
        return (f'<path d="M4 9 V27 A20 5 0 0 0 44 27 V9 Z" fill="{DAY}" stroke="{INK}" stroke-width="1.5"></path>'
                f'<ellipse cx="24" cy="9" rx="20" ry="5" fill="{DAY}" stroke="{INK}" stroke-width="1.5"></ellipse>'
                f'<path d="M4 18 A20 5 0 0 0 44 18" stroke="{INK}" stroke-width=".8" fill="none" opacity=".45"></path>'
                ), "0 0 48 34", 42
    if kind == "gold":
        return slab(22, 5, GOLD), "0 0 44 28", 47
    return g_client(1, 1), "0 0 86 60", 43


def form_tag(kind: str, text: str) -> str:
    inner, vb, w = part(kind)
    return (f'<p class="form"><svg width="{w}" height="30" viewBox="{vb}" aria-hidden="true">{inner}</svg>'
            f'<span>{text}</span></p>')


def sleeve_mark(fill: str) -> str:
    return (f'<svg class="slv" width="20" height="40" viewBox="0 0 20 40" aria-hidden="true">'
            f'{frame.sleeve(10, 20, fill)}</svg>')


def stop(n: int, stratum: str, form: str, head: str, body: str, links: str, obj: str, cls: str = "",
         sleeve: str = "", wide: str = "") -> str:
    sl = sleeve_mark(sleeve) if sleeve else ""
    wd = f'<div class="swide">{wide}</div>' if wide else ""
    return (f'<li class="stop {cls}">{sl}<span class="jn" aria-hidden="true">{n}</span>'
            f'<div class="stx">{form_tag(stratum, form)}<h3>{head}</h3><p>{body}</p><p class="lk">{links}</p></div>'
            f'<div class="sob">{obj}</div>{wd}</li>')


def journey() -> str:
    s1 = well("gridflow ingest elexon system_prices --start 2026-09-08 --end 2026-09-08\n"
              "gridflow transform elexon system_prices --start 2026-09-08 --end 2026-09-08", "text")
    s2 = well("GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/2026-09-08?page=1",
              "text", "sm")
    body = """{
  "metadata": { "datasets": ["DISEBSP"] },
  "data": [
    {
      "settlementDate": "2026-09-08",
      "settlementPeriod": 37,
      "startTime": "2026-09-08T17:00:00Z",
      "createdDateTime": "2026-09-08T17:48:45Z",
      "systemSellPrice": 9.56,
      "systemBuyPrice": 9.56,
      "priceDerivationCode": "N",
      "netImbalanceVolume": -1467.4127825220955
    }
  ]
}"""
    side = """{
  "source": "elexon",
  "dataset": "system_prices",
  "fetched_at": "2026-09-08T21:44:03.540996+00:00",
  "written_at": "2026-09-08T21:44:03.546999+00:00",
  "data_date": "2026-09-08",
  "request_url": "https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/2026-09-08?page=1",
  "request_params": { "page": 1 },
  "api_version": "v1",
  "http_status": 200,
  "content_type": "application/json; charset=utf-8",
  "body_sha256": "3a7fca5829bdc6b15878ab19659625b6d52cdfcb6abec67094e828e44a18571f",
  "body_size_bytes": 39466,
  "page": 1,
  "total_pages": 1
}"""
    s3 = ('<div class="pair"><div>'
          + well("data/bronze/elexon/system_prices/2026/09/08/\n  raw_20260908T214403Z_3a7fca58.json\n"
                 "  raw_20260908T214403Z_3a7fca58.meta.json\n  raw_20260916T190532Z_4c2c01b2.json\n"
                 "  raw_20260916T190532Z_4c2c01b2.meta.json", "text", "sm", N("The folder for 8 September"))
          + "</div><div>"
          + well(body, "json", "sm", f'<code>raw_20260908T214403Z_3a7fca58.json</code>, {N("excerpt")}',
                 ("9.56",))
          + '</div></div>')
    s3w = well(side, "json", "sm", "<code>raw_20260908T214403Z_3a7fca58.meta.json</code>")
    cols4 = ["settlement_date", "settlement_period", "system_sell_price", "system_buy_price", "available_at",
             "vintage_policy", "source_run_id", "dataset_version"]
    rows4 = [["2026-09-08", "37", "9.56", "9.56", "2026-09-08 17:48:45 UTC", "vendor",
              "494e780a-a127-4fa8-b371-25caf146c094", "2.0.0"],
             ["2026-09-08", "37", "110.0", "110.0", "2026-09-09 17:44:29 UTC", "vendor",
              "494e780a-a127-4fa8-b371-25caf146c094", "2.0.0"]]
    s4 = (well("data/silver/elexon/system_prices/year=2026/month=09/\n"
               "  system_prices_20260908_run2026-09-08T21-44-03.546999-00-00.parquet\n"
               "  system_prices_20260908_run2026-09-16T19-05-32.981753-00-00.parquet", "text")
          + well("SELECT settlement_date, settlement_period,\n       system_sell_price, system_buy_price,\n"
                 "       available_at, vintage_policy, source_run_id, dataset_version\n"
                 "FROM silver_elexon_system_prices\n"
                 "WHERE settlement_date = DATE '2026-09-08' AND settlement_period = 37\nORDER BY available_at;",
                 "sql", "join"))
    s4w = (f'<p class="wt">{N("The two rows it returns")}</p>'
           + out_table(cols4, rows4, {(0, 2), (0, 3), (1, 2), (1, 3)}))
    # stop 5
    asof = ('<div class="qa">' + well("SELECT settlement_date, settlement_period,\n       system_sell_price, available_at\n"
                 "FROM silver_elexon_system_prices\n"
                 "WHERE settlement_date = DATE '2026-09-08'\n  AND settlement_period = 37\n"
                 "  AND available_at <= TIMESTAMPTZ '2026-09-09 12:00:00+00'\n"
                 "QUALIFY row_number() OVER (\n    PARTITION BY settlement_date, settlement_period\n"
                 "    ORDER BY available_at DESC\n) = 1;", "sql", "q", N("The as-of read, as gridflow_models applies it"))
            + "</div>" + out_table(["settlement_date", "settlement_period", "system_sell_price", "available_at"],
                        [["2026-09-08", "37", "9.56", "2026-09-08 17:48:45 UTC"]], {(0, 2)}, "side"))
    latest = ('<div class="qa">' + well("SELECT settlement_date, settlement_period,\n       system_sell_price, system_buy_price, available_at\n"
                   "FROM silver_elexon_system_prices_latest\n"
                   "WHERE settlement_date = DATE '2026-09-08'\n  AND settlement_period = 37;", "sql", "q",
                   N("The _latest view"))
              + "</div>" + out_table(["settlement_date", "settlement_period", "system_sell_price", "system_buy_price",
                           "available_at"], [["2026-09-08", "37", "110.0", "110.0", "2026-09-09 17:44:29 UTC"]],
                          {(0, 2), (0, 3)}, "side"))
    ddl = well('CREATE OR REPLACE VIEW "silver_elexon_system_prices_latest" AS\n'
               'SELECT * FROM "silver_elexon_system_prices"\nQUALIFY ROW_NUMBER() OVER (\n'
               '    PARTITION BY "settlement_date", "settlement_period"\n'
               '    ORDER BY "available_at" DESC NULLS LAST,\n'
               "             CASE \"run_type\" WHEN 'II' THEN 1 WHEN 'SF' THEN 2 WHEN 'R1' THEN 3\n"
               "                  WHEN 'R2' THEN 4 WHEN 'R3' THEN 5 WHEN 'RF' THEN 6\n"
               "                  WHEN 'DF' THEN 7 ELSE 0 END DESC\n) = 1",
               "sql", "", N("How the _latest view is defined"))
    s5 = (f'<figure class="tlf">{timeline()}<figcaption><code>elexon/system_prices</code>, settlement date '
          f'2026-09-08, period 37: {N("the two rows of")} <code>silver_elexon_system_prices</code> '
          f'{N("placed at their")} <code>available_at</code>, {N("and the two bronze captures at their fetch times. The marked path is what was known at each moment: 9.56 until the revision. Times are UTC; the axis skips from 10 to 16 September.")}'
          f'</figcaption></figure>'
          f'<div class="q2">{asof}</div><div class="q2">{latest}</div>')
    cols6 = ["settlement_date", "settlement_period", "system_buy_price", "system_sell_price", "spread",
             "abs_imbalance", "hour_of_day", "day_of_week"]
    s6 = (well("gridflow build system_marginal_price --start 2026-09-08 --end 2026-09-08", "text")
          + well('(pl.col("system_buy_price") - pl.col("system_sell_price")).alias("spread")', "py", "",
                 N("The spread column, in the builder")))
    s6w = ('<p class="wt">' + N("The gold row for period 37, from") + ' <code>SystemMarginalPriceBuilder.build()</code></p>'
           + out_table(cols6, [["2026-09-08", "37", "110.0", "110.0", "0.0", "346.717783", "17", "2"]],
                       {(0, 2), (0, 3), (0, 4)}))
    s7 = (well('import polars as pl\n\nfrom gridflow.serving.client import GridflowClient\n\n'
               'with GridflowClient() as gf:\n    prices = gf.get_system_prices("2026-09-08", "2026-09-08")\n\n'
               'print(\n    prices.filter(pl.col("settlement_period") == 37).select(\n'
               '        "settlement_date", "settlement_period", "system_sell_price", "system_buy_price",\n'
               '        pl.col("available_at").dt.convert_time_zone("UTC"),\n    )\n)', "py")
          + out_table(["settlement_date", "settlement_period", "system_sell_price", "system_buy_price",
                       "available_at"], [["2026-09-08", "37", "110.0", "110.0", "2026-09-09 17:44:29 UTC"]],
                      {(0, 2), (0, 3)}, "join df", "Polars DataFrame"))

    lag = ("<p class=\"lag\"><strong>Publication-lag rule, as a mechanism.</strong> When a vendor gives no publication "
           "time, a dated per-dataset rule estimates when each value could first have been known, for history before a "
           "set cutover. On datasets that declare one, each row records which applied: <code>vendor</code>, the rule's "
           "name, or <code>ingest-clock</code>.</p>")
    stops = [
        stop(1, "cli", N("at the foot: a command"), "One command starts the run",
             "Nothing runs on a timer. Someone runs <code>ingest</code> to fetch a day from Elexon into bronze, then "
             "<code>transform</code> to turn that bronze into silver. Both take a source, a dataset and a date range.",
             gl("src/gridflow/cli.py"), s1),
        stop(2, "conn", N("in the connector: a request"), "The connector calls Elexon",
             "The Elexon connector puts the settlement date in the URL path and follows the pages. A per-source "
             "semaphore caps requests in flight, and tenacity retries timeouts, network errors and HTTP errors with "
             "jittered backoff.",
             gl("src/gridflow/connectors/elexon/client.py") + " " + gl("src/gridflow/connectors/elexon/endpoints.py"),
             s2),
        stop(3, "files", N("in bronze: a file and its sidecar"), "Bronze keeps the raw bytes",
             "The response is saved byte for byte, in a folder for the date it describes, beside a "
             "<code>.meta.json</code> sidecar recording the request, status and body hash. Fetching the same day again "
             "adds a second file next to the first.", gl("src/gridflow/bronze/writer.py"), s3, sleeve=T_BRONZE, wide=s3w),
        stop(4, "slab", N("in silver: two typed rows"), "Silver keeps every version",
             "Each bronze capture becomes its own typed Parquet file, named for when it was captured, and both prices "
             "are kept. Every row is checked against a Pydantic schema and stamped with <code>available_at</code> "
             "(Elexon's publication time), <code>source_run_id</code> and <code>dataset_version</code>.",
             gl("src/gridflow/silver/elexon/system_prices.py") + " " + gl("src/gridflow/silver/base.py"), s4, wide=s4w,
             sleeve=T_SILVER),
        (f'<li class="stop s5"><svg class="band" aria-hidden="true" width="100%" height="100%"><rect width="100%" '
         f'height="100%" fill="{T_SILVER}"></rect><rect width="100%" height="100%" fill="url(#p-diag-j)" opacity=".22">'
         f'</rect></svg>{edge("top")}{edge("bot")}<span class="jn" aria-hidden="true">5</span>'
         f'<div class="hx"><div class="stx">{form_tag("drum", N("in the catalogue: the latest choice"))}'
         f'<h3>The latest view picks a winner</h3>'
         f'<p><code>silver_elexon_system_prices_latest</code> keeps one row per settlement period: the latest '
         f'<code>available_at</code> wins, ties go to the later settlement run. The base view keeps both, so a backtest '
         f'can ask what was known at any moment: here, 9.56 until the revision.</p>'
         f'{lag}<p class="lk">{gl("src/gridflow/silver/latest_views.py")} '
         f'{gl("src/gridflow/silver/base.py")}</p></div><div class="ddl">{ddl}</div></div>'
         f'<div class="sob">{s5}</div></li>'),
        stop(6, "gold", N("in gold: a gold row"), "Gold adds derived columns",
             "The <code>system_marginal_price</code> builder reads the latest version of each period and adds spread "
             "(buy minus sell), absolute imbalance, hour of day and ISO day of week. Buy and sell are equal in this "
             "period, so spread is 0.0.", gl("src/gridflow/gold/system_marginal_price.py"), s6, sleeve=T_GOLD,
             wide=s6w),
        stop(7, "client", N("at the foot: a Polars DataFrame"), "Read it into Polars",
             "<code>GridflowClient</code> opens the DuckDB file read-only and returns Polars DataFrames. "
             "<code>get_system_prices</code> reads the <code>_latest</code> view, so each settlement period comes back "
             "once, with <code>available_at</code> kept so you know which version you hold.",
             gl("src/gridflow/serving/client.py"), s7),
    ]
    tag = (f'<dl class="tag"><div><dt>{N("Source and dataset")}</dt><dd><code>elexon</code>, <code>system_prices</code>'
           f'</dd></div><div><dt>{N("Settlement date")}</dt><dd><code>2026-09-08</code></dd></div>'
           f'<div><dt>{N("Settlement period")}</dt><dd><code>37</code></dd></div>'
           f'<div><dt>{N("Versions")}</dt><dd><mark class="sp">9.56</mark>, then <mark class="sp">110.00</mark></dd>'
           f'</div></dl>')
    pats = ('<svg width="0" height="0" class="defs" aria-hidden="true"><defs>'
            '<pattern id="p-diag-j" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" '
              'stroke="#5E6E6B" stroke-width=".8"></path></pattern>'
              '<pattern id="p-brick-j" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 '
              'V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" fill="none"></path></pattern>'
              '<pattern id="p-stip-j" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" '
              'fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" fill="#8A6F1E"></circle></pattern>'
              f'<pattern id="p-soil-j" width="23" height="17" patternUnits="userSpaceOnUse"><circle cx="4" cy="5" '
              f'r="1.2" fill="{KHAKI}"></circle><circle cx="15" cy="12" r="1.3" fill="{KHAKI}"></circle></pattern>'
              "</defs></svg>")
    return (f'<section class="jr" data-section="journey" aria-labelledby="h-jr">{pats}'
            f'<div class="jh"><h2 id="h-jr">{N("One row, from the command to a DataFrame")}</h2>'
            f'<p class="intro">The example row throughout: Elexon <code>system_prices</code>, settlement date '
            f'2026-09-08, period 37. Two captures of the same day hold two versions: first published at 9.56, then '
            f'110.00 a day later. {N("Its route is the chartreuse cable in the drawing.")}</p>{tag}</div>'
            f'<ol class="stops">{"".join(stops)}</ol></section>')


def edge(which: str) -> str:
    pts = hp.wave(14, 7, 2.1 if which == "top" else 5.2)
    d = smooth(pts)
    if which == "top":
        fill = f'<path d="{d} L{W + 40} -4 L-40 -4 Z" fill="{DAY}"></path>'
    else:
        fill = f'<path d="{d} L{W + 40} 40 L-40 40 Z" fill="{DAY}"></path>'
    return (f'<svg class="edge {which}" width="{W}" height="30" viewBox="0 0 {W} 30" aria-hidden="true">{fill}'
            f'<path d="{d}" stroke="{INK}" stroke-width="1.5" fill="none"></path></svg>')


# =============================================================== correct, look
def correct() -> str:
    rules = [
        ("Raw responses are kept, so any silver table can be rebuilt without calling the vendor again.",
         "src/gridflow/bronze/writer.py"),
        ("Re-runs are safe: every file lands by temp file and atomic rename, never half-written.",
         "src/gridflow/storage/parquet.py"),
        ("Rows that fail validation are still written, counted, and the run is marked completed with warnings.",
         "src/gridflow/silver/base.py"),
        ("Each row gridflow writes carries <code>available_at</code>: vendor publication time if given, else a dated "
         "estimate or gridflow's clock.", "src/gridflow/silver/base.py"),
        ("One embedded DuckDB file is the catalogue; <code>GridflowClient</code> opens it read-only, and there is no "
         "server.", "src/gridflow/storage/duckdb.py"),
    ]
    li = "".join(f'<li><p>{t}</p><p class="lk">{gl(p)}</p></li>' for t, p in rules)
    ddl = well("""CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id          VARCHAR PRIMARY KEY,
    source          VARCHAR NOT NULL,
    dataset         VARCHAR NOT NULL,
    operation       VARCHAR NOT NULL,
    started_at      TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at    TIMESTAMP WITH TIME ZONE,
    status          VARCHAR NOT NULL,
    rows_in         INTEGER DEFAULT 0,
    rows_out        INTEGER DEFAULT 0,
    rows_skipped    INTEGER DEFAULT 0,
    duration_seconds FLOAT,
    error_message   VARCHAR,
    parameters      VARCHAR
)""", "sql", "sm")
    return (f'<section class="cor" data-section="correct" aria-labelledby="h-cor"><h2 id="h-cor">'
            f'{N("How it stays correct")}</h2><div class="cg"><ol class="rules">{li}</ol><div class="ops">'
            f'<h3>{N("Run tracking")}</h3><p>Every ingest, transform and build writes a row to '
            f'<code>pipeline_runs</code> with its status, row counts and any error, and each silver row\'s '
            f'<code>source_run_id</code> points back to it. Incremental ingest resumes from '
            f'<code>pipeline_watermarks</code>. <code>gridflow quality</code> runs row-count, null-rate, gap and '
            f'duplicate checks and writes them to <code>quality_reports</code>.</p>{ddl}'
            f'<p class="lk">{gl("src/gridflow/observability.py")} {gl("src/gridflow/quality/checks.py")}</p>'
            f'<h3>CI</h3><p>On every push and pull request, gridflow\'s CI checks the lockfile, runs ruff lint and format '
            f'checks, mypy over <code>src/gridflow</code>, and pytest with live-API tests excluded.</p>'
            f'<p class="lk">{gl(".github/workflows/ci.yml")}</p></div></div></section>')


def look() -> str:
    rows = [
        ("Which sources and endpoints are configured", [("config/sources.yaml", GH)]),
        ("How a connector requests, limits and retries", [("src/gridflow/connectors/base.py", GH),
                                                          ("src/gridflow/utils/retry.py", GH)]),
        ("How raw responses are stored", [("src/gridflow/bronze/writer.py", GH)]),
        ("How bronze becomes silver: validation, timestamps, file names", [("src/gridflow/silver/base.py", GH)]),
        ("A complete transformer, Elexon system prices", [("src/gridflow/silver/elexon/system_prices.py", GH)]),
        ("How the latest version is chosen", [("src/gridflow/silver/latest_views.py", GH)]),
        ("The catalogue, its views and run tables", [("src/gridflow/storage/duckdb.py", GH)]),
        ("Gold builders and SQL views", [("src/gridflow/gold/system_marginal_price.py", GH),
                                         ("src/gridflow/gold/views", GHT)]),
        ("Reading data into Polars", [("src/gridflow/serving/client.py", GH)]),
        ("Run tracking and quality checks", [("src/gridflow/observability.py", GH),
                                             ("src/gridflow/quality/checks.py", GH)]),
        ("How gridflow_models reads gridflow as of a time", [("src/gridflow_models/data/gridflow_source.py", GM)]),
    ]
    li = "".join(f'<li><span class="lw">{w}</span><span class="lp">{"".join(gl(p, b) for p, b in ps)}</span></li>'
                 for w, ps in rows)
    return (f'<section class="look" data-section="look" aria-labelledby="h-look"><h2 id="h-look">'
            f'{N("Where to look")}</h2><ul class="map">{li}</ul></section>')


def rough_edge() -> str:
    pts = frame.rough(22)
    d = smooth(pts)
    return (f'<svg class="redge" width="{W}" height="44" viewBox="0 0 {W} 44" aria-hidden="true">'
            f'<path d="{d} L{W + 40} -4 L-40 -4 Z" fill="{DAY}"></path>'
            f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path></svg>')


# =============================================================== page
CSS = """.sky{position:relative;box-sizing:border-box;padding:0 80px 30px;background:#155A6E}
.hero{display:grid;grid-template-columns:780px 440px;column-gap:60px;margin-top:64px;align-items:start}
.hero h1{color:#F6F4EC;font-weight:760;font-stretch:84%;font-size:86px;line-height:.94;letter-spacing:-.022em}
.lede{padding-top:10px}
.lede p{margin:0 0 14px;font-size:17.5px;line-height:1.6;color:#CFE0DC;max-width:58ch}
.lede p.lead{color:#F6F4EC}
.drawing{background:#155A6E}
.dhead{padding:0 80px 6px;display:grid;grid-template-columns:minmax(0,1fr) 460px;column-gap:60px;align-items:end}
.dhead p{margin:10px 0 0}
.ksky .ke{margin:0}
.ksky .kn{color:#F6F4EC}
.ksky .kl{color:#CFE0DC}
.ksky .kl code,.ksky .srcs code{color:#F6F4EC}
.root .ksky a{text-decoration-color:#AFC64E}
.ksky .srcs{margin-top:6px}
.dhead h2{font-size:30px;font-weight:700;font-stretch:90%;line-height:1.1;letter-spacing:-.012em;color:#F6F4EC}
.dhead p{margin:0;font-size:15px;line-height:1.5;color:#CFE0DC;max-width:58ch}
.dgrid{display:grid;grid-template-columns:1440px}
.dgrid>svg,.dgrid>.dov{grid-area:1 / 1}
.dr{display:block}
.dr .lab text,.tl .lab text{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:13.5px;fill:#1C2B22}
.dr .lab text.v{font-size:14px;font-weight:500}
.dr .lab text.m,.tl .lab text.m,.tl .lab tspan.m{font-family:"Red Hat Mono",monospace;font-style:normal;font-size:12.5px}
.dr .lab text.b{font-size:13.5px;font-weight:500}
.dr .lab text.s{font-size:11.5px;fill:#3F4A3B}
.dov{position:relative}
.kidx{list-style:none;margin:0;padding:0}
.kg{box-sizing:border-box;margin-left:900px;width:460px;padding:18px 0 0;overflow:hidden}
.kg.kg-top{padding-top:110px}
.ke{display:grid;grid-template-columns:34px minmax(0,1fr);column-gap:14px;margin:0 0 13px}
.ke .mk{margin-top:2px}
.kn{font-family:"Hanken Grotesk",sans-serif;font-size:15.5px;font-weight:650;line-height:1.35;margin:0}
.root .kn{font-family:"Hanken Grotesk",sans-serif}
.kl{margin:3px 0 0;font-size:13.5px;line-height:1.5;color:#3F4A3B}
.kk{margin:4px 0 0;font-size:13px;line-height:1.5;display:flex;flex-wrap:wrap;column-gap:14px;row-gap:2px}
.kk code,.kl code,.srcs code,.verbs code,.kn code{font-size:12.5px;color:#1C2B22}
.srcs{display:flex;flex-wrap:wrap;column-gap:14px;row-gap:2px}
.verbs{display:flex;flex-wrap:wrap;column-gap:10px;row-gap:0}
.rdx{list-style:none;margin:0;padding:0 80px;display:grid;grid-template-columns:repeat(4,290px);column-gap:40px;box-sizing:border-box}
.rdx li{margin:0}
.p{overflow-wrap:anywhere}
.more{font-weight:600;font-size:14px;color:#1C2B22}
mark.sp{background:#AFC64E;color:#1C2B22;padding:0 2px;border-radius:2px}
.jr{position:relative;background:#F6F4EC;padding:40px 0 0}
.defs{position:absolute;width:0;height:0}
.jh{padding:0 80px 24px 160px;display:grid;grid-template-columns:600px 1fr;column-gap:80px;align-items:end}
.jh h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0 0 14px;grid-column:1 / -1;max-width:22ch}
.intro{margin:0;font-size:17.5px;line-height:1.6;color:#3F4A3B;max-width:58ch}
.intro code{color:#1C2B22}
.tag{margin:0;align-self:end}
.tag div{display:grid;grid-template-columns:150px minmax(0,1fr);column-gap:14px;padding:7px 0;border-top:1px solid rgba(28,43,34,.22)}
.tag div:last-child{border-bottom:1px solid rgba(28,43,34,.22)}
.tag dt{font-size:14px;line-height:1.45;color:#3F4A3B}
.tag dd{margin:0;font-size:14.5px;line-height:1.45}
.tag code{font-size:13.5px}
.stops{list-style:none;margin:0;padding:0;position:relative;z-index:0}
.stops::before{content:"";position:absolute;left:101.8px;top:30px;bottom:120px;width:4.4px;background:#1C2B22;z-index:2}
.stops::after{content:"";position:absolute;left:103.25px;top:30px;bottom:120px;width:1.5px;background:#AFC64E;z-index:2}
.stop{position:relative;display:grid;grid-template-columns:80px 340px 40px 820px;padding:40px 80px;align-items:start}
.stop>.stx{grid-column:2;grid-row:1}
.stop>.sob{grid-column:4;grid-row:1}
.stop>div{position:relative;z-index:1;min-width:0}
.jn{grid-column:1;grid-row:1;position:relative;margin:45px 0 0 10px;box-sizing:content-box;width:24px;height:24px;border:2px solid #1C2B22;border-radius:50%;background:#F6F4EC;font:700 13px/24px "Hanken Grotesk",sans-serif;text-align:center;color:#1C2B22;z-index:3;font-variant-numeric:tabular-nums}
.slv{position:absolute;left:94px;top:-20px;z-index:3}
.form{display:flex;align-items:center;gap:12px;margin:0 0 12px;font-style:italic;font-size:14px;line-height:1.3;color:#3F4A3B}
.form svg{flex:none}
.stx h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;margin:0 0 10px;letter-spacing:-.005em}
.stx p{margin:0 0 12px;font-size:16px;line-height:1.62;color:#3F4A3B;max-width:58ch}
.stx p code,.stx2 p code{color:#1C2B22}
.lk{display:flex;flex-wrap:wrap;column-gap:14px;row-gap:2px;font-size:13px}
.root .lk{font-size:13px;margin:0}
.lk code{font-size:12.5px}
.sob{display:grid;row-gap:12px;min-width:0}
.well{overflow-x:auto;margin:0}
.well.sm{font-size:13px}
.wt{margin:0 0 -6px;font-size:13.5px;line-height:1.4;color:#3F4A3B}
.wt code{font-size:12.5px;color:#1C2B22}
.join{margin-top:-12px;border-top-left-radius:0;border-top-right-radius:0;border-top:0}
.pair{display:grid;grid-template-columns:1fr 1fr;column-gap:12px;row-gap:12px}
.swide{grid-column:2 / -1;grid-row:2;display:grid;row-gap:12px;min-width:0;margin-top:18px;position:relative;z-index:1}
.pair>div{display:grid;row-gap:12px;min-width:0;align-content:start}
.pair .well{font-size:13px;line-height:1.65}
pre.out{margin:-12px 0 0;background:#F6F4EC;border:1px solid rgba(28,43,34,.3);border-radius:0 0 3px 3px;padding:8px 14px;font:400 13.5px/1.6 "Red Hat Mono",monospace;color:#1C2B22;overflow-x:auto;white-space:pre}
.res{overflow-x:auto;background:#F6F4EC;border:1px solid rgba(28,43,34,.3);border-radius:3px;width:fit-content;max-width:100%;box-sizing:border-box}
.res.join{border-top:1px solid rgba(28,43,34,.3);margin-top:0}
.rt{border-collapse:collapse;font:400 12px/1 "Red Hat Mono",monospace;color:#1C2B22;white-space:nowrap}
.rt th,.rt td{padding:8px 6px;text-align:left}
.rt th.n,.rt td.n{text-align:right}
.rt thead th{font-weight:500;border-bottom:1px solid #1C2B22}
.rt tbody tr:nth-child(even){background:#EFEBDF}
.res.df{border:1.5px solid #1C2B22}
.hero5{}
.stop.s5{padding:96px 80px 100px;margin:32px 0}
.band{position:absolute;left:0;top:0;z-index:0}
.edge{position:absolute;left:0;z-index:0}
.edge.top{top:-2px}
.edge.bot{bottom:-2px;transform:scaleY(-1)}
.stop.s5>.hx{grid-column:2 / -1;grid-row:1}
.stop.s5>.sob{grid-column:2 / -1;grid-row:2}
.hx{position:relative;z-index:1;display:grid;grid-template-columns:470px 700px;column-gap:30px;align-items:start;margin-bottom:34px}
.hx .ddl{margin-top:34px}
.hx .ddl .well{font-size:12.5px;line-height:1.65}
.stx .lag{margin:18px 0 12px;font-size:15px;line-height:1.6;color:#3F4A3B}
.stx .lag strong{color:#1C2B22;font-weight:650}
.stop.s5 .sob{position:relative;z-index:1}
.tlf{margin:0 0 8px}
.tl{display:block;overflow:visible}
.tl .lab text.v,.tl .lab text.m.v{font-size:13px;font-weight:500}
.tl .lab text.tk{font-style:normal;font-size:13px;fill:#3F4A3B}
.tlf figcaption{margin:14px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:92ch}
.tlf figcaption code{color:#1C2B22;font-size:.88em}
.q2{display:grid;grid-template-columns:470px 700px;column-gap:30px;align-items:start;margin-top:26px}
.qa,.ddl{display:grid;row-gap:12px;min-width:0;align-content:start}
.ddl{margin-top:26px}
.well.q{font-size:12.5px;line-height:1.65}
.res.side{margin-top:26px}
.cor{background:#F6F4EC;padding:30px 80px 90px}
.cor h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0 0 30px;padding-top:36px;border-top:1px solid rgba(28,43,34,.22)}
.cg{display:grid;grid-template-columns:640px 560px;column-gap:80px;align-items:start}
.rules{margin:0;padding:0;list-style:none;counter-reset:r}
.rules li{padding:14px 0 16px;border-top:1px solid rgba(28,43,34,.22)}
.rules li:last-child{border-bottom:1px solid rgba(28,43,34,.22)}
.rules p{margin:0;font-size:17.5px;line-height:1.5;color:#1C2B22;max-width:52ch}
.rules p.lk{margin-top:6px}
.ops h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;margin:0 0 8px}
.ops h3+p{margin-top:0}
.ops p{margin:0 0 14px;font-size:15.5px;line-height:1.6;color:#3F4A3B;max-width:62ch}
.ops p code{color:#1C2B22}
.ops .well{margin:0 0 10px;font-size:12px;line-height:1.5}
.ops .lk{margin:0 0 30px}
.deep{position:relative;background:#155A6E;color:#F6F4EC}
.deep .gran{position:absolute;left:0;top:0;z-index:0}
.deep>*:not(.gran){position:relative;z-index:1}
.redge{display:block}
.look{padding:40px 80px 70px}
.look h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0 0 26px;color:#F6F4EC}
.map{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;column-gap:60px;grid-auto-flow:column;grid-template-rows:repeat(6,auto)}
.map li{display:grid;grid-template-columns:250px minmax(0,1fr);column-gap:20px;align-items:baseline;min-height:44px;padding:10px 0;box-sizing:border-box;border-top:1px solid rgba(207,224,220,.22)}
.lw{font-size:15px;line-height:1.4;color:#CFE0DC}
.lp{display:flex;flex-direction:column;row-gap:2px}
.lp a{color:#F6F4EC;text-decoration-color:#AFC64E}
.root .lp a{text-decoration-color:#AFC64E}
.lp code{font-size:13.5px}
.deep .st{position:relative;z-index:1}
"""

PROBE = """<pre id="m"></pre><script>
window.addEventListener('load',function(){Promise.all(['760 86px "Bricolage Grotesque"','720 42px "Bricolage Grotesque"','400 16px "Hanken Grotesk"','600 16px "Hanken Grotesk"','italic 400 14px "Hanken Grotesk"','400 14px "Red Hat Mono"','500 14px "Red Hat Mono"'].map(function(q){return document.fonts.load(q)})).then(function(){return document.fonts.ready}).then(function(){setTimeout(function(){
var root=document.querySelector('.root').getBoundingClientRect(),o={g:{},secs:{},H:0,over:[]};
document.querySelectorAll('[data-g]').forEach(function(e){var h=0;Array.prototype.forEach.call(e.children,function(c){var r=c.getBoundingClientRect(),cs=getComputedStyle(c);h=Math.max(h,r.bottom-e.getBoundingClientRect().top+parseFloat(cs.marginBottom));});o.g[e.dataset.g]=Math.ceil(h);});
document.querySelectorAll('[data-section]').forEach(function(s){var r=s.getBoundingClientRect();o.secs[s.dataset.section]=[Math.round(r.top-root.top),Math.round(r.height)];});
o.H=Math.ceil(document.querySelector('main').getBoundingClientRect().bottom-root.top);
document.querySelectorAll('main p,main li,main h1,main h2,main h3,main dd,main dt,main pre,main figcaption,main .res').forEach(function(e){if(e.scrollWidth>e.clientWidth+1)o.over.push((e.className||e.tagName)+':'+(e.scrollWidth-e.clientWidth)+':'+e.textContent.slice(0,40));var r=e.getBoundingClientRect();if(r.right-root.left>1361&&!e.closest('.mast'))o.over.push('WIDE '+(e.className||e.tagName)+':'+Math.round(r.right-root.left)+':'+e.textContent.slice(0,30));});
document.getElementById('m').textContent=JSON.stringify(o);},500);});});
</script>"""


def bands(m: dict) -> dict:
    g = m.get("g", {})
    b: dict = {}
    b["C1"] = S + max(g.get("top", 230) + 28, 236)
    b["C2"] = b["C1"] + max(g.get("bronze", 180) + 26, 176)
    b["C3"] = b["C2"] + max(g.get("silver", 290) + 26, 290)
    b["G0"] = b["C3"] + max(g.get("gold", 180) + 26, 170)
    b["R"] = b["G0"] + 58
    b["RX"] = b["R"] + 22
    b["BOT"] = b["RX"] + g.get("readers", 170) + 36
    b["Hd"] = b["BOT"] + 26
    return b


def body(m: dict) -> str:
    NEW.clear()
    b = bands(m)
    groups = index_groups()
    kg = (f'<ul class="kidx">'
          f'<li class="kg kg-top" data-g="top" style="height:{b["C1"] - S}px"><ul class="kidx">{groups["top"]}</ul></li>'
          f'<li class="kg" data-g="bronze" style="height:{b["C2"] - b["C1"]}px"><ul class="kidx">{groups["bronze"]}</ul></li>'
          f'<li class="kg" data-g="silver" style="height:{b["C3"] - b["C2"]}px"><ul class="kidx">{groups["silver"]}</ul></li>'
          f'<li class="kg" data-g="gold" style="height:{b["G0"] - b["C3"]}px"><ul class="kidx">{groups["gold"]}</ul></li>'
          f"</ul>")
    rd = readers()
    ov = (f'<div class="dov"><div style="height:{S}px"></div>{kg}'
          f'<div style="height:{b["RX"] - b["G0"]}px"></div>{rd}</div>')
    opening = (f'<section class="sky" data-section="opening">{frame.masthead("Architecture")}'
               f'<div class="hero"><h1>{N("How gridflow is built")}</h1><div class="lede">'
               f'<p class="lead">Raw API responses land in bronze, cleaned and typed tables settle in silver, and '
               f'cross-source joins and derived columns sit in gold; one embedded DuckDB file reads silver and gold.</p>'
               f'<p>gridflow has no scheduler, no server, no cloud and no live feed: every run is a gridflow command '
               f'someone starts, and vendor data arrives only when one runs.</p></div></div></section>')
    drawing = (f'<section class="drawing" data-section="drawing" aria-labelledby="h-draw"><div class="dhead">'
               f'<div><h2 id="h-draw">{N("The whole system, in section")}</h2>'
               f'<p>{N("Sources above ground; bronze, silver and gold below; the readers at the foot. Each part is keyed to its file on GitHub. The chartreuse cable is the route of the row followed below.")}</p></div>'
               f'<ul class="kidx ksky" data-g="sky">{groups["sky"]}</ul></div><div class="dgrid">{drawing_svg(b)}{ov}</div></section>')
    gran = ('<svg class="gran" width="100%" height="100%" aria-hidden="true"><defs><pattern id="p-gran-d" width="46" '
            'height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 '
            f'v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path></pattern></defs>'
            '<rect width="100%" height="100%" fill="url(#p-gran-d)" opacity=".5"></rect></svg>')
    deep = f'<div class="deep">{gran}{rough_edge()}{look()}{frame.footer("arch")}</div>'
    return opening + drawing + journey() + correct() + deep


def shell(inner: str, H: int, probe: bool) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Architecture</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{hp.FONTS}
<style>
{frame.BASE_CSS}{CSS}</style>
</helmet>
<div class="root" style="width: {W}px; height: {H}px; overflow: hidden; position: relative">
<main>
{inner}
</main>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
{PROBE if probe else ""}</body>
</html>
"""


def measure(html_text: str) -> dict:
    p = HERE / "static" / "_probe.html"
    p.write_text(frame.static(html_text), encoding="utf-8")
    out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--window-size=1440,4000",
                          "--virtual-time-budget=9000", "--dump-dom",
                          f"http://127.0.0.1:{PORT}/_probe.html?v={time.time_ns()}"],
                         capture_output=True, text=True, encoding="utf-8", timeout=120)
    mm = re.search(r'<pre id="m">(.*?)</pre>', out.stdout, re.S)
    if not mm or not mm.group(1).strip():
        raise RuntimeError(f"probe failed: {out.stderr[-400:]}")
    p.unlink()
    return json.loads(html.unescape(mm.group(1)))


def reuse(H: int) -> None:
    """Rebuild from the saved band measurements at a given root height (measured in a browser tab)."""
    m1 = json.loads((HERE / "measure.json").read_text(encoding="utf-8"))["m1"]
    out = shell(body(m1), H, False)
    frame.check(out)
    (HERE / f"{NAME}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static" / f"{NAME}.html").write_text(frame.static(out), encoding="utf-8")
    (HERE / "copy-new.json").write_text(json.dumps(list(dict.fromkeys(NEW)), ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    print("reuse H", H, "bands", bands(m1))


def main() -> None:
    if len(sys.argv) > 2 and sys.argv[1] == "--reuse":
        reuse(int(sys.argv[2]))
        return
    m1 = measure(shell(body({}), 9000, True))
    print("pass1 g", m1["g"])
    m2 = measure(shell(body(m1), 9000, True))
    print("pass2 g", m2["g"], "H", m2["H"], "secs", m2["secs"])
    for o in m2["over"]:
        print("  over", o)
    H = m2["H"]
    out = shell(body(m1), H, False)
    frame.check(out)
    (HERE / f"{NAME}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static" / f"{NAME}.html").write_text(frame.static(out), encoding="utf-8")
    (HERE / "copy-new.json").write_text(json.dumps(list(dict.fromkeys(NEW)), ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    (HERE / "measure.json").write_text(json.dumps({"m1": m1, "m2": m2, "bands": bands(m1)}, indent=1),
                                       encoding="utf-8")
    print("H", H, "bands", bands(m1))


if __name__ == "__main__":
    main()
