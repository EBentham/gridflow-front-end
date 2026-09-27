"""Designer E, "Survey sheets": the shared sheet grammar for the four top pages.

Every sheet descends the same grounds and each ground always holds the same kind of block:
sky (title, answer line, horizon) / topsoil (the plate: drawing right, keyed index left) /
bronze (the register) / silver (the specimen) / gold (reach it from code, then how it is checked) /
deep (what it does not do, where the facts come from, other pages, footer).
Text flows in CSS grid; only decorative strata and the sky drawing are absolutely placed.
"""
from __future__ import annotations

import json
import math
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
PACK = json.loads((OUT.parent / "pack" / "toppages.json").read_text(encoding="utf-8"))
REF = Path(r"C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v4\design-loop\r3-7\R3-final.dc.html")
_REF_LINES = REF.read_text(encoding="utf-8").split('<div class="root"', 1)[1].split("\n")

INK, INK2, MUTED = "#1C2B22", "#3F4A3B", "#5d6a55"
PETROL, DAY, TOPSOIL, ZEBRA, RULE = "#155A6E", "#F6F4EC", "#ECE8DA", "#EFEBDF", "#DFDACA"
CHART, OLIVE, HORIZON, CLAY, KHAKI = "#AFC64E", "#66793B", "#3E8C97", "#C77E3C", "#A39A6A"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
BRONZE_T, SILVER_T, GOLD_T = "#E2CDB3", "#DCE2DF", "#E9DDAF"
CLAY_DEEP, SILVER_DEEP, GOLD_DEEP = "#7C5530", "#5E6E6B", "#8A6F1E"
ONP, ONP2, ONP3 = "#F6F4EC", "#CFE0DC", "#B4D0CD"

G = 290          # the ground line (page y) on every sheet
PLATE_TOP = G + 34 + 33 + 16   # page y of every plate drawing: band padding, heading, heading margin
MAST_H = 56      # masthead band height
L_W, GAP, R_W = 360, 80, 840   # the two columns every sheet shares: words left, drawing right
R_X = 80 + L_W + GAP           # page x of the right column (520)


def f(v: float) -> str:
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- reference pieces (R3-final, reused)
def ref_lines(a: int, b: int) -> str:
    return "\n".join(_REF_LINES[a:b])


GAS_STATION = ref_lines(41, 50)     # x 242..341, base 842
SUBSTATION = ref_lines(95, 101)     # x 853..966, base 937.5
MET_MAST = ref_lines(101, 105)      # x 974..1046, base 936.7, mast at 1018
CONVERTER = ref_lines(105, 112)     # x 1037..1218, base 940.1
GAS_TERMINAL = ref_lines(112, 113)  # x 1240..1406, base 946.2
SOLAR = ref_lines(52, 69)           # x 52..414, base 941
PYLON_D = ("M-18 0 L-5 -96 M18 0 L5 -96 M-5 -96 L-5 -118 M5 -96 L5 -118 M-5 -118 H5 M-14 -28 H14 M-11 -56 H11 "
           "M-8 -80 H8 M-16 -14 L14 -28 M16 -14 L-14 -28 M-13 -42 L11 -56 M13 -42 L-11 -56 M-10 -68 L8 -80 "
           "M10 -68 L-8 -80 M-30 -66 H30 M-24 -92 H24 M-14 -112 H14 M-30 -66 L-5 -60 M30 -66 L5 -60 "
           "M-24 -92 L-5 -86 M24 -92 L5 -86")
for _piece, _start in ((GAS_STATION, "<rect"), (SUBSTATION, "<g transform"), (MET_MAST, "<path"),
                       (CONVERTER, "<g transform"), (GAS_TERMINAL, "<g transform"), (SOLAR, "<path")):
    assert _piece.startswith(_start), _piece[:40]


def place(piece: str, x0: float, y0: float, x: float, y: float, k: float = 1.0) -> str:
    """Move a reference piece whose base point is (x0, y0) so that point lands on (x, y), scaled k."""
    return (f'<g transform="translate({f(x)} {f(y)}) scale({k}) translate({f(-x0)} {f(-y0)})">'
            f'{piece}</g>')


def pylon(x: float, y: float, s: float) -> str:
    return (f'<g transform="translate({f(x)},{f(y)}) scale({s})"><path vector-effect="non-scaling-stroke" '
            f'd="{PYLON_D}"></path></g>')


def turbine(x: float, y: float, r: float, hub_h: float, rot0: float, sp: str, fill: str = DAY) -> str:
    """A wind turbine standing on (x, y): the reference's tower, nacelle and blade formula, re-parameterised."""
    hy = y - hub_h
    bw, tw = .058 * r, .026 * r
    blade = (f"M{f(-.042 * r)} 0 C{f(-.087 * r)} {f(-.3 * r)} {f(-.034 * r)} {f(-.76 * r)} 0 {f(-r)} "
             f"C{f(.024 * r)} {f(-.72 * r)} {f(.095 * r)} {f(-.3 * r)} {f(.042 * r)} 0 Z")
    blades = "".join(f'<path d="{blade}" transform="rotate({rot0 + 120 * i:g})" fill="{fill}"></path>' for i in range(3))
    return (f'<path d="M{f(x - bw)} {f(y)} L{f(x - tw)} {f(hy)} L{f(x + tw)} {f(hy)} L{f(x + bw)} {f(y)} Z" '
            f'fill="{fill}"></path>'
            f'<rect x="{f(x - .01 * r)}" y="{f(hy - .05 * r)}" width="{f(.18 * r)}" height="{f(.095 * r)}" '
            f'rx="{f(.037 * r)}" fill="{fill}"></rect>'
            f'<g transform="translate({f(x - .04 * r)},{f(hy)})"><g class="rot {sp}"><circle r="{f(r)}" fill="none">'
            f'</circle>{blades}<circle r="{f(.053 * r)}" fill="{fill}"></circle></g></g>')


def cable(d: str, core: str = BRONZE, w: float = 4.4, cw: float = 1.5) -> str:
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round"></path><path d="{d}" fill="none" stroke="{core}" stroke-width="{cw}" '
            f'stroke-linecap="round" stroke-linejoin="round"></path>')


def cable_end(x: float, y: float, tint: str = BRONZE_T) -> str:
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="6.5" fill="{tint}" stroke="{INK}" stroke-width="2"></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="2.2" fill="{INK}"></circle>')


# ---------------------------------------------------------------- patterns and strata
_PAT = {
    "p-stip": (9, 9, f'<circle cx="2" cy="3" r="1" fill="{GOLD_DEEP}"></circle><circle cx="6.5" cy="7.5" r=".8" fill="{GOLD_DEEP}"></circle>'),
    "p-diag": (8, 8, f'<path d="M0 8 L8 0" stroke="{SILVER_DEEP}" stroke-width=".8"></path>'),
    "p-brick": (24, 12, f'<path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="{CLAY_DEEP}" stroke-width=".8" fill="none"></path>'),
    "p-soil": (23, 17, f'<circle cx="4" cy="5" r=".9" fill="{KHAKI}"></circle><circle cx="15" cy="12" r="1.1" fill="{KHAKI}"></circle><path d="M17 3 h3" stroke="{KHAKI}" stroke-width=".9"></path>'),
    "p-granite": (46, 40, f'<path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path>'),
}
_UID = [0]


def pat(name: str) -> tuple[str, str]:
    """A pattern defined inside the svg that uses it (the canvas may not resolve ids across svgs): (defs, url)."""
    _UID[0] += 1
    pid = f"{name}-{_UID[0]}"
    w, h, body = _PAT[name]
    return (f'<defs><pattern id="{pid}" width="{w}" height="{h}" patternUnits="userSpaceOnUse">{body}</pattern></defs>',
            f"url(#{pid})")


def wave_pts(y0: float, seed: int, amp: float = 4.5, step: float = 180.0, x0: float = -40, x1: float = 1480) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    n = int((x1 - x0) / step) + 1
    return [(x0 + i * (x1 - x0) / n, y0 + rng.uniform(-amp, amp)) for i in range(n + 1)]


def smooth(pts: list[tuple[float, float]]) -> str:
    """Catmull-Rom through the points, written as cubic Beziers."""
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


OFF = 18   # every band's contact line sits 18 px above the band's box, in the band's own svg


def band_bg(kind: str, seed: int) -> str:
    top = smooth(wave_pts(OFF, seed))
    body = top + " L1480 20000 L-40 20000 Z"
    fill, pat_name, op = {"topsoil": (TOPSOIL, "p-soil", .5), "bronze": (BRONZE_T, "p-brick", .15),
                     "silver": (SILVER_T, "p-diag", .22), "gold": (GOLD_T, "p-stip", .26),
                     "deep": (PETROL, "p-granite", .5)}[kind]
    defs, url = pat(pat_name)
    g = [defs, f'<path d="{body}" fill="{fill}"></path>', f'<path d="{body}" fill="{url}" opacity="{op}"></path>']
    if kind == "topsoil":
        pts = wave_pts(OFF, seed)
        low = [(x, y + 9) for x, y in reversed(pts)]
        band = smooth(pts) + " L" + " L".join(f"{f(x)} {f(y)}" for x, y in low) + " Z"
        g.append(f'<path d="{band}" fill="{OLIVE}"></path>')
        g.append(f'<path d="{top}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    elif kind == "bronze":
        g.append(f'<path d="{top}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    elif kind == "deep":
        g.append(f'<path d="{top}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path>')
    return f'<svg class="bg" width="1440" aria-hidden="true">{"".join(g)}</svg>'


def sub_contact(seed: int) -> str:
    """A dotted contact inside one stratum (as the reference draws them), between two blocks on the same ground."""
    d = smooth(wave_pts(10, seed, amp=3.5, step=240))
    return (f'<svg class="subc" width="1440" height="20" viewBox="0 0 1440 20" aria-hidden="true"><path d="{d}" '
            f'stroke="{INK}" stroke-width="1" stroke-dasharray="2 6" fill="none" opacity=".55"></path></svg>')


# ---------------------------------------------------------------- the sky
def land_top(x: float) -> float:
    t = min(max((x - 520) / 880, 0), 1)
    return G - 5 - 17 * (t * t * (3 - 2 * t))


def sky_svg(assets: str, labels: list[tuple[float, float, str, str]], aria: str) -> str:
    """Petrol sky, a low ridge rising to the right, energised land, then the page's own assets."""
    h = G + 16
    back = [(-20, G - 8), (400, G - 14), (700, G - 30), (960, G - 58), (1180, G - 72), (1320, G - 66), (1460, G - 78)]
    front = [(-20, G - 4), (500, G - 9), (820, G - 26), (1060, G - 44), (1260, G - 50), (1460, G - 40)]
    land_pts = [(x, land_top(x)) for x in range(-20, 1481, 20)]
    land = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in land_pts) + f" L1480 {h} L-20 {h} Z"
    g = [f'<path d="{smooth(back)} L1460 {h} L-20 {h} Z" fill="{HORIZON}" opacity=".5"></path>',
         f'<path d="{smooth(front)} L1460 {h} L-20 {h} Z" fill="{HORIZON}"></path>',
         f'<path d="{land}" fill="{CHART}"></path>',
         f'<path d="M-20 {f(G - 1)} C300 {f(G - 3)} 700 {f(G - 8)} 1460 {f(G - 14)}" stroke="{OLIVE}" '
         f'stroke-width="1" fill="none" opacity=".45"></path>',
         assets]
    t = "".join(f'<text x="{f(x)}" y="{f(y)}" fill="{c}" text-anchor="middle">{esc(s)}</text>' for x, y, s, c in labels)
    g.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="13.5">{t}</g>')
    return (f'<svg class="layer sky-art" width="1440" height="{h}" viewBox="0 0 1440 {h}" role="img" '
            f'aria-label="{esc(aria)}">{"".join(g)}</svg>')


# the horizon pieces every sheet can use, placed on the land at x
def a_substation(x: float, k: float = 1.0) -> tuple[str, float]:
    return place(SUBSTATION, 853, 937.5, x, land_top(x + 56 * k) + 1, k), 853


def a_met_mast(x: float, k: float = .82) -> str:
    return place(MET_MAST, 1018, 936.7, x, land_top(x) + 1, k)


def a_converter(x: float, k: float = .9) -> str:
    return place(CONVERTER, 1037, 940.1, x, land_top(x + 90 * k) + 1, k)


def a_gas_terminal(x: float, k: float = .9) -> str:
    return place(GAS_TERMINAL, 1240, 946.2, x, land_top(x + 83 * k) + 1, k)


def a_gas_station(x: float, k: float = 1.0) -> str:
    return place(GAS_STATION, 242, 842, x, land_top(x + 50 * k) + 1, k)


def a_solar(x: float, k: float = .5) -> str:
    return place(SOLAR, 52, 941, x, land_top(x + 180 * k) + 2, k)


def catenary(pts: list[tuple[float, float]], sag: float = 12) -> str:
    """Three conductors hung between consecutive attachment points (x, y of the top crossarm)."""
    d = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        for dy in (0, 14, 24):
            mx = (x1 + x2) / 2
            d.append(f"M{f(x1)} {f(y1 + dy)} Q{f(mx)} {f(max(y1, y2) + dy + sag)} {f(x2)} {f(y2 + dy)}")
    return f'<path d="{" ".join(d)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>'


# ---------------------------------------------------------------- page chrome
NAV = [("Home", "home"), ("Data sources", "ds"), ("Architecture", "arch"), ("Models", "models"), ("About", "about")]


def masthead(current: str, level: str = "page") -> str:
    items = "".join(f'<li><a href="#"{f" aria-current=\"{level}\"" if key == current else ""}>{name}</a></li>'
                    for name, key in NAV)
    return (f'<header class="mast"><a class="brand" href="#">gridflow</a><nav aria-label="Primary"><ul>{items}'
            f'</ul></nav></header>')


def sky(title: str, answer: str, back: str | None = None) -> str:
    b = f'<p class="back"><a href="#">{back}</a></p>' if back else ""
    return (f'<section class="sky" aria-labelledby="t-h"><div class="in">{b}<h1 id="t-h">{title}</h1>'
            f'<p class="ans">{answer}</p></div></section>')


def band(kind: str, seed: int, inner: str, cls: str = "", label: str | None = None) -> str:
    lab = f' aria-labelledby="{label}"' if label else ""
    return (f'<section class="band {kind} {cls}"{lab}>{band_bg(kind, seed)}<div class="in">{inner}</div></section>')


def rail(hid: str, head: str, gloss: str | None = None) -> str:
    gl = f'<p class="gl">{gloss}</p>' if gloss else ""
    return f'<div class="rail"><h2 id="{hid}">{head}</h2>{gl}</div>'


def block(hid: str, head: str, gloss: str | None, content: str) -> str:
    return f'<div class="blkr">{rail(hid, head, gloss)}<div class="cnt">{content}</div></div>'


def swatch(kind: str, w: int = 46, h: int = 30) -> str:
    fill, pat_name = {"bronze": (BRONZE_T, "p-brick"), "silver": (SILVER_T, "p-diag"), "gold": (GOLD_T, "p-stip")}[kind]
    defs, url = pat(pat_name)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">{defs}'
            f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" fill="{fill}"></rect>'
            f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" fill="{url}" opacity=".45"></rect>'
            f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" fill="none" stroke="{INK}" stroke-width="1.5">'
            f'</rect></svg>')


PAGES = {
    "ds": ("bronze", "Data sources", "Seven vendors and every dataset gridflow ingests, filed by vendor."),
    "arch": ("silver", "Architecture", "How a response becomes a table: bronze, silver, gold and the commands between them."),
    "models": ("gold", "Models", "Five forecasting models built on the warehouse, and the evidence for each."),
}


def other_pages(current: str) -> str:
    items = "".join(f'<li><a href="#">{swatch(k)}<h3>{name}</h3><p>{desc}</p></a></li>'
                    for key, (k, name, desc) in PAGES.items() if key != current)
    n = sum(1 for key in PAGES if key != current)
    return f'<ul style="grid-template-columns: repeat({n}, minmax(0, 1fr))">{items}</ul>'


def deep(current: str, limits: list[str], sources: list[tuple[str, str]]) -> str:
    lim = "".join(f"<li>{x}</li>" for x in limits)
    src = "".join(f'<li><span class="sw">{a}</span><span class="sp">{b}</span></li>' for a, b in sources)
    inner = (block("lim-h", "What it does not do", None, f'<ul class="lim">{lim}</ul>')
             + block("src-h", "Where these facts come from", None, f'<ul class="src">{src}</ul>')
             + block("oth-h", "Other pages", None, f'<div class="oth">{other_pages(current)}</div>'))
    return band("deep", 71, inner, "det")


def footer() -> str:
    defs, url = pat("p-granite")
    return (f'<footer class="foot"><svg class="bg" width="1440" aria-hidden="true">{defs}<rect width="1440" height="400" '
          f'fill="{url}" opacity=".5"></rect></svg><div class="in"><p><a class="brand" href="#">gridflow</a>'
          '</p><p>This site is MIT licensed. gridflow itself is Apache-2.0.</p><p class="fl"><a href="#">GitHub</a>'
          '<a href="#">About</a></p></div></footer>')


# ---------------------------------------------------------------- CSS
CSS = """body{margin:0}
.root{background:#155A6E;color:#1C2B22;font:400 16px/1.6 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.root a{color:inherit;text-decoration-thickness:1.5px;text-underline-offset:4px;text-decoration-color:#66793B}
.root a:focus-visible{outline:2px solid #AFC64E;outline-offset:3px;border-radius:2px}
.root h1,.root h2,.root h3{font-family:"Bricolage Grotesque",sans-serif;margin:0;font-optical-sizing:auto}
.root code{font-family:"Red Hat Mono",monospace;font-size:.9em}
.layer{position:absolute;left:0;top:0}
.defs{position:absolute;width:0;height:0;overflow:hidden}
.mast{position:relative;z-index:2;height:56px;box-sizing:border-box;padding:26px 80px 0;display:flex;justify-content:space-between;align-items:baseline;color:#F6F4EC}
.brand{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:24px;letter-spacing:-.01em;text-decoration:none}
.mast ul{display:flex;gap:30px;list-style:none;margin:0;padding:0;font-size:15px}
.mast ul a{text-decoration:none;color:#CFE0DC}
.mast ul a:hover{color:#F6F4EC}
.mast ul a[aria-current]{color:#F6F4EC;box-shadow:inset 0 -2px 0 #AFC64E}
.sky{position:relative;z-index:1;height:234px}
.sky .in{padding:30px 80px 0}
.sky h1{color:#F6F4EC;font-weight:760;font-stretch:84%;font-size:64px;line-height:.94;letter-spacing:-.022em;max-width:980px;width:fit-content}
.sky .ans{margin:18px 0 0;max-width:540px;font-size:17.5px;line-height:1.58;color:#CFE0DC}
.sky .ans code{color:#F6F4EC;font-size:.88em}
.sky .back{margin:-26px 0 8px;font-size:15px;line-height:18px}
.sky .back a{color:#CFE0DC;text-decoration-color:#AFC64E}
.sky .back a:hover{color:#F6F4EC}
.land-t{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:13.5px}
.rot{transform-box:fill-box;transform-origin:center;animation:spin 17s linear infinite}
.sp2{animation-duration:13s}
.sp3{animation-duration:21s}
@keyframes spin{to{transform:rotate(360deg)} }
@media (prefers-reduced-motion: reduce){.rot{animation:none} }
.band{position:relative}
.band>.bg{position:absolute;left:0;top:-18px;height:calc(100% + 40px);display:block;z-index:0}
.band>.in{position:relative;z-index:1}
.plate>.in{padding:34px 80px 30px}
.root .ph{font-size:30px;font-weight:700;font-stretch:90%;letter-spacing:-.012em;line-height:1.1;margin:0 0 16px}
.pgrid{display:grid;grid-template-columns:360px 840px;column-gap:80px;align-items:start}
.ix{list-style:none;margin:0;padding:0}
.ix li{display:grid;grid-template-columns:30px minmax(0,1fr);column-gap:14px;box-sizing:border-box;overflow:hidden}
.ix .mk{display:block;margin-top:2px}
.ix h3{font-size:20px;font-weight:700;font-stretch:90%;line-height:1.1;letter-spacing:-.005em}
.ix h3 a{text-decoration-color:rgba(102,121,59,0)}
.ix h3 a:hover{text-decoration-color:#66793B}
.ix .id{margin:2px 0 0;font:400 13px/1.35 "Red Hat Mono",monospace;color:#155A6E}
.ix .d{margin:2px 0 0;font-size:14.5px;line-height:1.36;color:#3F4A3B}
.ix .f{margin:1px 0 0;font-size:13.5px;line-height:1.38;font-weight:600;color:#1C2B22}
.ix .keys{margin:3px 0 0;font:400 13.5px/1.5 "Red Hat Mono",monospace;color:#1C2B22}
.ix .keys a{text-decoration-thickness:1px;text-underline-offset:3px;text-decoration-color:rgba(102,121,59,.55)}
.ix .keys a:hover{text-decoration-color:#66793B}
.pfig{margin:0}
.pfig svg{display:block;overflow:visible}
.pfig figcaption,.fig figcaption{margin:12px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:66ch}
.pfig figcaption code,.fig figcaption code{font-size:13px;color:#1C2B22}
.det>.in{padding:96px 80px 88px}
.blkr{display:grid;grid-template-columns:360px 840px;column-gap:80px;align-items:start}
.blkr+.blkr{margin-top:80px}
.subc{display:block;margin:76px -80px 70px}
.rail h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em}
.rail .gl{margin:16px 0 0;font-size:15px;line-height:1.58;color:#3F4A3B;max-width:34ch}
.rail .gl code{font-size:13.5px;color:#1C2B22}
.reg{list-style:none;margin:0;padding:0;border-bottom:1px solid rgba(28,43,34,.25)}
.reg>li{display:grid;grid-template-columns:196px minmax(0,1fr);column-gap:32px;padding:20px 0 22px;border-top:1px solid rgba(28,43,34,.25)}
.reg h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 6px}
.reg h3 a{text-decoration-color:rgba(102,121,59,0)}
.reg h3 a:hover{text-decoration-color:#66793B}
.reg .sk{margin:0;font:400 13.5px/1.5 "Red Hat Mono",monospace;color:#155A6E}
.reg .n{margin:8px 0 0;font-size:14.5px;font-weight:600;color:#1C2B22}
.reg .pub{margin:0 0 8px;font-size:15.5px;line-height:1.55;color:#1C2B22;max-width:64ch}
.reg dl{margin:0}
.reg dl div{display:grid;grid-template-columns:84px minmax(0,1fr);column-gap:14px;padding:2px 0}
.reg dt{font-weight:600;font-size:14px;line-height:1.5;color:#1C2B22}
.reg dd{margin:0;font-size:14px;line-height:1.5;color:#3F4A3B}
.reg dd code{font-size:13px;color:#1C2B22}
.tg+.tg{margin-top:34px}
.tg h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 10px}
.tl{list-style:none;margin:0;padding:0;border-top:1px solid rgba(28,43,34,.25)}
.tl li{display:grid;grid-template-columns:176px 212px minmax(0,1fr);column-gap:20px;align-items:baseline;min-height:40px;box-sizing:border-box;padding:8px 0 7px;border-bottom:1px solid rgba(28,43,34,.22)}
.tl .k{font:400 16px/1.5 "Red Hat Mono",monospace;color:#1C2B22}
.tl .k a{text-decoration-color:rgba(102,121,59,.55)}
.tl .c{font:400 13px/1.5 "Red Hat Mono",monospace;color:#3F4A3B}
.tl .t{font-size:14.5px;line-height:1.5;color:#3F4A3B}
.fig{margin:0}
.fig svg{display:block}
.lc{list-style:none;margin:0;padding:0;border-bottom:1px solid rgba(28,43,34,.25)}
.lc li{display:grid;grid-template-columns:232px minmax(0,1fr);column-gap:36px;align-items:start;padding:24px 0 26px;border-top:1px solid rgba(28,43,34,.25)}
.lc h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 7px}
.lc p{margin:0;font-size:14.5px;line-height:1.5;color:#3F4A3B}
.lc p code{font-size:13px;color:#1C2B22}
.well{margin:0;background:#ECE8DA;border:1px solid rgba(28,43,34,.18);border-radius:3px;padding:9px 14px;font:400 14.5px/1.72 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre;overflow:hidden}
.well .k{color:#155A6E;font-weight:500}
.well .s{color:#7C5530}
.well .c{color:#5d6a55}
.ck{margin:0;border-bottom:1px solid rgba(28,43,34,.25)}
.ck div{display:grid;grid-template-columns:232px minmax(0,1fr);column-gap:36px;padding:17px 0 18px;border-top:1px solid rgba(28,43,34,.25)}
.ck dt{font-weight:600;font-size:15.5px;line-height:1.5;color:#1C2B22}
.ck dt code{font-size:14px;font-weight:500}
.ck dd{margin:0;font-size:15px;line-height:1.58;color:#3F4A3B;max-width:62ch}
.ck dd code{font-size:13.5px;color:#1C2B22;white-space:nowrap}
.cfig{margin:34px 0 0}
.dfw{display:inline-block;margin:30px 0 0;background:#F6F4EC;border:1px solid rgba(28,43,34,.34);border-radius:3px;padding:6px 8px 8px}
.df{border-collapse:collapse;font:400 14px/1 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;color:#1C2B22}
.df caption{caption-side:top;text-align:left;padding:4px 12px 8px;font:500 14px/1.3 "Red Hat Mono",monospace;color:#155A6E}
.df th,.df td{padding:7px 12px;text-align:right;white-space:nowrap}
.df thead th{font-weight:600;border-bottom:1px solid #1C2B22;vertical-align:bottom}
.df tbody th{font-weight:600;text-align:left}
.df tbody tr:nth-child(odd){background:#EFEBDF}
.dnote{margin:12px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:66ch}
.card{border:1px solid rgba(28,43,34,.34);border-radius:3px;overflow:hidden;background:#F6F4EC}
.card-h{margin:0;padding:9px 14px;background:#ECE8DA;border-bottom:1px solid rgba(28,43,34,.2);font:500 15px/1.2 "Red Hat Mono",monospace;color:#155A6E}
.card dl{margin:0;padding:7px 8px 8px}
.card dl div{display:grid;grid-template-columns:170px minmax(0,1fr);gap:14px;padding:3px 8px;border-radius:2px}
.card dl div:nth-child(odd){background:#EFEBDF}
.card dt{font:400 13.5px/1.5 "Red Hat Mono",monospace;color:#155A6E}
.card dd{margin:0;font-size:14px;line-height:1.5;color:#1C2B22}
.cards{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:28px;align-items:start}
.deep .rail h2{color:#F6F4EC}
.lim,.src{list-style:none;margin:0;padding:0;border-bottom:1px solid rgba(207,224,220,.22)}
.lim li{padding:14px 0 15px;border-top:1px solid rgba(207,224,220,.22);font-size:15.5px;line-height:1.58;color:#F6F4EC;max-width:66ch}
.lim code,.src code{color:#F6F4EC;font-size:13.5px}
.src li{display:grid;grid-template-columns:232px minmax(0,1fr);column-gap:36px;padding:12px 0 13px;border-top:1px solid rgba(207,224,220,.22);font-size:14.5px;line-height:1.55}
.src .sw{color:#F6F4EC;font-weight:600}
.src .sp{color:#CFE0DC}
.oth ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:40px}
.oth a{display:block;text-decoration:none;color:#F6F4EC}
.oth svg{display:block;margin:4px 0 12px}
.oth h3{font-size:20px;font-weight:700;font-stretch:90%;margin:0 0 4px;text-decoration:underline;text-decoration-color:rgba(175,198,78,0);text-underline-offset:4px}
.oth a:hover h3{text-decoration-color:#AFC64E}
.oth p{margin:0;font-size:14.5px;line-height:1.5;color:#CFE0DC}
.foot{position:relative;background:#155A6E}
.foot>.bg{position:absolute;left:0;top:0;width:1440px;height:100%;display:block}
.foot>.in{position:relative;display:grid;grid-template-columns:360px minmax(0,1fr) auto;column-gap:80px;align-items:baseline;margin:0 80px;padding:30px 0 46px;border-top:1px solid rgba(207,224,220,.22);color:#B4D0CD;font-size:14px}
.foot p{margin:0}
.foot .brand{font-size:20px;color:#F6F4EC}
.foot .fl{display:flex;gap:24px}
.foot .fl a{color:#F6F4EC;text-decoration-color:#AFC64E}
"""


# ---------------------------------------------------------------- charts
def axis_text(x: float, y: float, s: str, anchor: str = "middle", fill: str = INK2) -> str:
    return f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" fill="{fill}">{esc(s)}</text>'


def line_chart(w: int, h: int, n: int, ymin: float, ymax: float, yticks: list[tuple[float, str]],
               xticks: list[tuple[float, str]], series: list[dict], aria: str, band: tuple | None = None,
               zero: bool = False, ylab: str = "", ml: int = 64, mr: int = 150, mt: int = 18, mb: int = 34) -> str:
    """A plain time chart: ink axis, a few real ticks, direct labels at the right end. x is an index 0..n-1."""
    pw, ph = w - ml - mr, h - mt - mb
    X = lambda i: ml + i * pw / (n - 1)  # noqa: E731
    Y = lambda v: mt + (ymax - v) / (ymax - ymin) * ph  # noqa: E731
    g = []
    if band:
        lo, hi, fill, op = band[:4]
        d = "M" + " L".join(f"{f(X(i))} {f(Y(v))}" for i, v in enumerate(hi))
        d += " L" + " L".join(f"{f(X(i))} {f(Y(v))}" for i, v in reversed(list(enumerate(lo)))) + " Z"
        g.append(f'<path d="{d}" fill="{fill}" opacity="{op}"></path>')
    if zero:
        g.append(f'<path d="M{ml} {f(Y(0))} H{ml + pw}" stroke="{INK}" stroke-width=".8" opacity=".6"></path>')
    for s in series:
        d = "M" + " L".join(f"{f(X(i))} {f(Y(v))}" for i, v in enumerate(s["v"]))
        g.append(f'<path d="{d}" fill="none" stroke="{s["c"]}" stroke-width="{s.get("w", 1.6)}" '
                 f'stroke-linejoin="round" stroke-linecap="round"></path>')
    # axes
    g.append(f'<path d="M{ml} {mt - 6} V{mt + ph} H{ml + pw}" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    t = []
    for v, lab in yticks:
        g.append(f'<path d="M{ml - 5} {f(Y(v))} H{ml}" stroke="{INK}" stroke-width="1"></path>')
        t.append(axis_text(ml - 9, Y(v) + 4.5, lab, "end"))
    for i, lab in xticks:
        g.append(f'<path d="M{f(X(i))} {mt + ph} V{mt + ph + 5}" stroke="{INK}" stroke-width="1"></path>')
        t.append(axis_text(X(i), mt + ph + 22, lab))
    if ylab:
        t.append(axis_text(ml + 8, mt + 2, ylab, "start", INK))
    g.append(f'<g font-family="Hanken Grotesk" font-size="13">{"".join(t)}</g>')
    lab = []
    for s in series + ([{"label": band[4], "v": band[1], "c": band[2], "ly": band[5]}] if band and len(band) > 4 else []):
        if s.get("label"):
            ly = s.get("ly", Y(s["v"][-1]))
            lab.append(f'<text x="{f(ml + pw + 10)}" y="{f(ly + 4.5)}" fill="{INK}">{esc(s["label"])}</text>')
    g.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="13.5">{"".join(lab)}</g>')
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">'
            + "".join(g) + "</svg>")


# ---------------------------------------------------------------- assembly
FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800"
         "&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500&amp;display=swap")


def page(title: str, current: str, sky_art: str, body: str, height: int, extra_css: str = "", level: str = "page") -> str:
    root = (f'<div class="root" style="width: 1440px; height: {height}px; overflow: hidden; position: relative">'
            f'{sky_art}{masthead(current, level)}<main>{body}</main>{footer()}</div>')
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{FONTS}" rel="stylesheet">
<style>
{CSS}{extra_css}</style>
</helmet>
{root}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":{height}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""
    body_only = out.split('<script type="text/x-dc"')[0]
    assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
    assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), "self-closing tag"
    assert "\u2014" not in body_only, "em dash in markup"
    assert "#A9C7C4" not in body_only.upper(), "retired petrol text colour"
    return out


def static(out: str) -> str:
    s = out.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    s = re.sub(r'<script type="text/x-dc".*?</script>\n?', "", s, flags=re.S)
    # the static copy is for the detector and the browser; the viewport meta is what the site will carry
    return s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">')


HEIGHTS_FILE = HERE / "heights.json"


def height_for(name: str, default: int) -> int:
    if HEIGHTS_FILE.exists():
        return int(json.loads(HEIGHTS_FILE.read_text()).get(name, default))
    return default


def write(name: str, out: str) -> None:
    (OUT / f"{name}.dc.html").write_text(out, encoding="utf-8")
    (OUT / "static").mkdir(exist_ok=True)
    (OUT / "static" / f"{name}.html").write_text(static(out), encoding="utf-8")


_ = (math, MUTED, ZEBRA, RULE, SILVER, GOLD, BRONZE, CLAY, ONP, ONP3, MAST_H, R_W, R_X)
