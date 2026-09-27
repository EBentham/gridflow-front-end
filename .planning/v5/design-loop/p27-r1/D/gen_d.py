"""Phase 27 round 1, designer D, "From the workbench". Emits D-*.dc.html + static/D-*.html.

Every notebook line is real gridflow-models API surface. Card rows were rendered from
gridflow_models/research/handles (Data._repr_html_, SourceClient._repr_html_, HelpCard) on 2026-09-27 and
are copied verbatim into the site's own card chrome. Every number comes from p27/pack/toppages.json.

The homepage generator (r3-7/gen_a.py) is exec'd read-only for its drawing pieces, patterns and CSS.
"""
from __future__ import annotations

import html
import json
import math
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).parent
REF = Path(r"C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v4\design-loop\r3-7\gen_a.py")
PACK = json.loads((HERE.parent / "pack" / "toppages.json").read_text(encoding="utf-8"))

_src = REF.read_text(encoding="utf-8").split("# ================================================================ v4: the purpose")[0]
G: dict = {"__file__": str(REF), "__name__": "gen_ref"}
exec(compile(_src, str(REF), "exec"), G)  # noqa: S102  (read-only reuse of the locked homepage's pieces)

f, smooth, prof = G["f"], G["smooth"], G["prof"]
PETROL, HORIZON, CHART, OLIVE = G["PETROL"], G["HORIZON"], G["CHART"], G["OLIVE"]
INK, DAY, CLAY, KHAKI = G["INK"], G["DAY"], G["CLAY"], G["KHAKI"]
BRONZE, SILVER, GOLD = G["BRONZE"], G["SILVER"], G["GOLD"]
T_GOLD, T_SILVER, T_BRONZE, T_TOP = G["T_GOLD"], G["T_SILVER"], G["T_BRONZE"], G["T_TOP"]
W = 1440
HEIGHTS_FILE = HERE / "heights.json"
HEIGHTS: dict[str, int] = json.loads(HEIGHTS_FILE.read_text()) if HEIGHTS_FILE.exists() else {}


def esc(s: str) -> str:
    return html.escape(s, quote=False)


# ================================================================ the strip (homepage pieces, homepage coordinates)
STRIP_Y0, STRIP_Y1 = 736, 952          # the slice of the homepage coordinate system the strip shows
STRIP_H = STRIP_Y1 - STRIP_Y0


def strip(kind: str) -> str:
    """A low landscape strip built from the locked homepage's drawing pieces, chosen per page."""
    p: list[str] = []
    sea = kind in ("sources", "models")
    far = [(-20, 832), (140, 812), (320, 822), (500, 804), (680, 818), (840, 840), (960, 852), (1100, 846),
           (1240, 836), (1380, 848), (1470, 842)]
    p.append(f'<path d="{smooth(far)} L1470 952 L-20 952 Z" fill="{HORIZON}" opacity=".5"></path>')
    if sea:
        p.append(f'<rect x="760" y="862" width="700" height="60" fill="{HORIZON}"></rect>'
                 f'<rect x="760" y="862" width="700" height="60" fill="{DAY}" opacity=".13"></rect>')
        p.append(f'<path d="M1180 862 C1240 858 1290 855 1340 856 S1410 853 1460 854 V862 Z" fill="{HORIZON}" '
                 f'opacity=".6"></path>')
        waves = " ".join(f"M{x0} {y0} h{ln}" for x0, y0, ln in
                         [(1010, 872, 30), (1120, 876, 22), (1250, 870, 30), (1370, 875, 36), (1180, 884, 20)])
        p.append(f'<path d="{waves}" stroke="{DAY}" stroke-width="1" opacity=".35"></path>')
        for i, ox in enumerate([1060, 1130, 1210, 1290, 1370]):
            p.append(G["turbine"](ox, 878 + (i % 2) * 2, 24, 12, ["sp1", "sp2", "sp3"][i % 3], 19 * i))
    near = [(-20, 858), (110, 838), (240, 830), (380, 842), (520, 834), (660, 848), (800, 868), (900, 890)]
    p.append(f'<path d="{smooth(near)} L900 952 L-20 952 Z" fill="{HORIZON}"></path>')
    tur = {"sources": [0, 1, 2, 3], "elexon": [0, 2, 3, 4], "arch": [0, 1, 3], "models": [0, 1, 2, 3]}[kind]
    for i in tur:
        tx, ty = near[1 + i]
        h = [54, 60, 50, 62, 56][i]
        p.append(G["turbine"](tx, ty + 3, h, h * .5, ["sp2", "sp1", "sp3"][i % 3], 40 * i + 10))
    field = [(-20, 884), (200, 878), (420, 886), (640, 880), (860, 892), (1060, 902), (1260, 906), (1460, 910)]
    bottom = " ".join(f"L{f(x)} {f(prof(x))}" for x in range(1460, -21, -20))
    p.append(f'<path d="{smooth(field)} {bottom} Z" fill="{CHART}"></path>')
    bounds = [smooth([(-20, 900), (400, 896), (800, 906), (1200, 918), (1460, 922)]),
              smooth([(-20, 918), (500, 916), (960, 926), (1460, 932)])]
    p.append(f'<path d="{" ".join(bounds)}" stroke="{OLIVE}" stroke-width="1" fill="none" opacity=".45"></path>')

    def pylon_line(pts: list[tuple[float, float, float]], start: tuple[float, float], end: list[tuple[float, float]]) -> None:
        wires = [G["spans"]([start, (start[0], start[1] - 10), (start[0], start[1] - 18)], G["tips"](*pts[0], -1), 6)]
        for a, b in zip(pts, pts[1:]):
            wires.append(G["spans"](G["tips"](*a, 1), G["tips"](*b, -1), 10))
        wires.append(G["spans"](G["tips"](*pts[-1], 1), end, 8))
        p.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">'
                 + "".join(G["pylon"](*q) for q in pts) + '</g>')
        p.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')

    def substation_at(x: float, s: float = 1.1) -> list[tuple[float, float]]:
        base = prof(x + 50)
        svg, ends = G["substation"](x, base)
        p.append(G["sc"](svg, x, base, s))
        return [(x + (ex - x) * s, base + (ey - base) * s) for ex, ey in ends]

    if kind == "sources":
        ends = substation_at(640)
        pylon_line([(250, 900, .42), (440, 906, .46)], (-20, 872), ends)
        p.append(G["metmast"](860, prof(860), 150))
        p.append(G["sc"](G["converter"](930, prof(990)), 930, prof(990), 1.12))
        p.append(G["sc"](G["gasterminal"](1140, prof(1200)), 1140, prof(1200), 1.2))
    elif kind == "elexon":
        p.append(G["ccgt"](200, 906, .62))
        ends = substation_at(900)
        pylon_line([(420, 902, .44), (640, 910, .5)], (-20, 874), ends)
        p.append(G["sc"](G["battery"](1110, prof(1170)), 1110, prof(1170), 1.15))
        p.append(G["metmast"](1320, prof(1320), 140))
    elif kind == "arch":
        ends = substation_at(560)
        pylon_line([(150, 898, .42), (360, 904, .46)], (-20, 872), ends)
        p.append(G["cable"](f"M{RISER_X} {f(prof(RISER_X) - 6)} V{STRIP_Y1 + 4}"))
        p.append(G["sc"](G["battery"](860, prof(920)), 860, prof(920), 1.1))
        p.append(G["metmast"](1180, prof(1180), 140))
        p.append(G["sc"](G["gasterminal"](1250, prof(1300)), 1250, prof(1300), 1.1))
    else:  # models: the things the models forecast
        p.append(G["solar_farm"]())
        p.append(G["ccgt"](560, 906, .62))
        ends = substation_at(780, 1.0)
        pylon_line([(700, 906, .42)], (612, 884), ends)
    return "\n".join(p)


def strip_svg(kind: str) -> str:
    lt, dk = "#E4EFEC", INK
    labels = {
        "sources": [("substation", 690, 864, lt, "middle"), ("met mast", 848, 812, lt, "end"),
                    ("interconnector", 992, 858, lt, "middle"), ("gas terminal", 1215, 882, lt, "middle"),
                    ("offshore wind", 1300, 846, lt, "middle")],
        "elexon": [("gas-fired power station", 236, 826, lt, "middle"), ("substation", 953, 868, lt, "middle"),
                   ("battery storage", 1173, 910, dk, "middle"), ("met mast", 1308, 830, lt, "end")],
        "arch": [("substation", 612, 866, lt, "middle"), ("met mast", 1168, 826, lt, "end")],
        "models": [("solar farm", 232, 862, lt, "middle"), ("gas-fired power station", 556, 826, lt, "start"),
                   ("offshore wind", 1300, 846, lt, "middle")],
    }[kind]
    lab = "".join(f'<text x="{x}" y="{y}" fill="{c}" text-anchor="{a}">{t}</text>' for t, x, y, c, a in labels)
    return (f'<svg class="strip land-svg" width="{W}" height="{STRIP_H}" viewBox="0 {STRIP_Y0} {W} {STRIP_H}" '
            f'aria-hidden="true">{strip(kind)}{lab}</svg>')


# ================================================================ grounds (decorative SVG behind each band)
OVER = 26   # how far a band's ground reaches up over the band above


def ground(kind: str, seed: float, label: str = "") -> str:
    """A stratum's ground: a wavy contact line at the top, tint, hatch, and the italic layer name."""
    fills = {"topsoil": (T_TOP, "p-soil", ".5"), "bronze": (T_BRONZE, "p-brick", ".15"),
             "silver": (T_SILVER, "p-diag", ".22"), "gold": (T_GOLD, "p-stip", ".26"),
             "deep": (PETROL, "p-granite", ".5")}
    fill, pat, op = fills[kind]
    if kind == "topsoil":   # the ground surface of the cut, continuous with the strip above
        pts = [(x, prof(x) - (STRIP_Y1 - OVER)) for x in range(-40, W + 41, 20)]
        top = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
        rootd = top + " " + " ".join(f"L{f(x)} {f(y + 9)}" for x, y in reversed(pts)) + " Z"
        extra = f'<path d="{rootd}" fill="{OLIVE}"></path>'
        line = f'<path d="{top}" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
    elif kind == "deep":
        pts = [(x, 14 + 7 * math.sin(x / 140 + seed) + 5 * math.sin(x / 53 + 2 * seed) + 3 * math.sin(x / 19))
               for x in range(-40, W + 41, 20)]
        top = smooth(pts)
        extra = ""
        line = f'<path d="{top}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path>'
    else:
        pts = [(x, 13 + 6 * math.sin(x / 210 + seed) + 2.7 * math.sin(x / 73 + seed * 2.3))
               for x in range(-40, W + 161, 120)]
        top = smooth(pts)
        extra = ""
        line = f'<path d="{top}" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
    body = f"{top} L{W + 40} 9000 L-40 9000 Z"
    name = (f'<text x="1360" y="{OVER + 30}" text-anchor="end" font-family="Hanken Grotesk" font-style="italic" '
            f'font-size="14" fill="{INK}">{label}</text>') if label else ""
    return (f'<svg class="ground" width="{W}" height="100%" aria-hidden="true"><defs>{G["PATTERNS"]}</defs>'
            f'<path d="{body}" fill="{fill}"></path><path d="{body}" fill="url(#{pat})" opacity="{op}"></path>'
            f'{extra}{line}{name}</svg>')


# ================================================================ notebook pieces
def hl(code: str) -> str:
    """Escape, then tint keywords and string literals the way JupyterLab does."""
    s = esc(code)
    s = re.sub(r'("""[\s\S]*?"""|"[^"\n]*")', lambda m: f'<span class="s">{m.group(0)}</span>', s)
    s = re.sub(r"^(from|import)\b|(?<= )(import)\b", lambda m: f'<span class="k">{m.group(0)}</span>', s, flags=re.M)
    return s


SETUP = "from gridflow_models import setup_notebook\ndata, models, common = setup_notebook()"


def cell(prompt: str, body: str, cls: str = "") -> str:
    return f'<div class="cell{(" " + cls) if cls else ""}"><span class="pr">{prompt}</span>{body}</div>'


def inp(code: str) -> str:
    return f'<pre class="in">{hl(code)}</pre>'


def notebook(tab: str, cells: list[str], aria: str) -> str:
    return (f'<figure class="nb" aria-label="{esc(aria)}"><div class="nb-bar"><span class="nb-tab">{tab}</span>'
            f'<span class="nb-kern">gridflow_models</span></div><div class="nb-body">{"".join(cells)}</div></figure>')


def index_card(title: str, rows: list[tuple[str, str]], hint_label: str, hint: str, cls: str = "") -> str:
    """render_index_card's content in the site's card chrome (the dataset-count suffix omitted, as on the homepage)."""
    dl = "".join(f"<div><dt>{esc(n)}</dt><dd>{esc(d)}</dd></div>" for n, d in rows)
    return (f'<div class="card{(" " + cls) if cls else ""}"><p class="card-h">{esc(title)}</p><dl>{dl}</dl>'
            f'<p class="card-f">{hint_label}: <code>{esc(hint)}</code></p></div>')


# rows as rendered by Data._repr_html_ (2026-09-27)
SRC_LINE = "Work with one data source, e.g. ``data.elexon`` or ``data.entsoe``."
DATA_ROWS = [(s, SRC_LINE) for s in ["elexon", "entsoe", "entsog", "gie_agsi", "gie_alsi", "neso",
                                      "neso_data_portal", "open_meteo"]] + [
    ("list_data_sources", "List the data sources available as ``data.<source>`` handles."),
    ("list_tables", "List every stored table across all sources."),
    ("list_freshness", "Show how up to date every dataset is, across all sources."),
    ("sql", "Run a read-only SQL query against your local store."),
    ("refresh_all", "Fetch the latest rows for every dataset on every source."),
    ("training_set", "Build a training set you can hand to ``models.<id>.validate(...)``."),
    ("imbalance_context", "Read the cross-source imbalance-context view over a date range."),
    ("gb_day_ahead_benchmark", "Read the GB day-ahead benchmark over a settlement-date range."),
]
ELEXON_ROWS = [
    ("list_datasets", "List every dataset this source provides."),
    ("refresh", "Fetch the latest rows for this source, topping up what you have."),
    ("describe", "Show a dataset's columns, sample values, and freshness."),
    ("backfill", "Download history for a dataset and store it locally."),
    ("query", "Read stored rows for a dataset over a date range."),
    ("tail", "Read the most recent rows of a dataset."),
    ("coverage", "Show how up to date each dataset on this source is."),
]


def df_html(cols: list[str], rows: list[tuple[str, ...]]) -> str:
    head = "<tr><th></th>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"
    body = "".join(f"<tr><th>{i}</th>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for i, r in enumerate(rows))
    return f'<table class="df"><thead>{head}</thead><tbody>{body}</tbody></table>'


def mpl(w: int, h: int, n: int, lines: list[tuple[list[float], str, float]], ylo: float, yhi: float,
        yticks: list[float], xticks: list[tuple[float, str]], xlabel: str, ylabel: str, aria: str,
        band: tuple[list[float], list[float], str] | None = None, legend: list[tuple[str, str]] | None = None) -> str:
    """A matplotlib-style axes drawn in the site's palette: framed axes, outward ticks, a few real ticks."""
    L, R, T, B = 66, 14, 10, 50
    aw, ah = w - L - R, h - T - B

    def X(i: float) -> float:
        return L + i * aw / (n - 1)

    def Y(v: float) -> float:
        return T + (yhi - v) * ah / (yhi - ylo)

    o: list[str] = []
    if band:
        lo, hi, col = band
        d = "M" + " L".join(f"{f(X(i))} {f(Y(v))}" for i, v in enumerate(hi))
        d += " L" + " L".join(f"{f(X(i))} {f(Y(v))}" for i, v in reversed(list(enumerate(lo)))) + " Z"
        o.append(f'<path d="{d}" fill="{col}" opacity=".3"></path>')
    for ys, col, sw in lines:
        d = "M" + " L".join(f"{f(X(i))} {f(Y(v))}" for i, v in enumerate(ys))
        o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"></path>')
    o.append(f'<rect x="{L}" y="{T}" width="{aw}" height="{ah}" fill="none" stroke="{INK}" stroke-width="1"></rect>')
    tk = []
    for v in yticks:
        y = Y(v)
        tk.append(f'<path d="M{L - 4} {f(y)} H{L}" stroke="{INK}" stroke-width="1"></path>'
                  f'<text x="{L - 8}" y="{f(y + 4.5)}" text-anchor="end">{int(v)}</text>')
    for i, lab in xticks:
        x = X(i)
        tk.append(f'<path d="M{f(x)} {T + ah} v4" stroke="{INK}" stroke-width="1"></path>'
                  f'<text x="{f(x)}" y="{T + ah + 19}" text-anchor="middle">{lab}</text>')
    tk.append(f'<text x="{L + aw / 2}" y="{h - 6}" text-anchor="middle">{xlabel}</text>')
    tk.append(f'<text transform="translate(16 {T + ah / 2}) rotate(-90)" text-anchor="middle">{ylabel}</text>')
    if legend:
        lw = 22 + max(len(t) for t, _ in legend) * 7.4 + 24
        lh = 10 + 20 * len(legend)
        tk.append(f'<rect x="{L + 10}" y="{T + 10}" width="{f(lw)}" height="{lh}" fill="{DAY}" stroke="{INK}" '
                  f'stroke-opacity=".3" stroke-width="1" rx="2"></rect>')
        for k, (t, col) in enumerate(legend):
            y = T + 25 + 20 * k
            tk.append(f'<path d="M{L + 20} {y - 4} h22" stroke="{col}" stroke-width="1.8"></path>'
                      f'<text x="{L + 50}" y="{y}">{t}</text>')
    return (f'<svg class="plot" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">'
            + "".join(o) + f'<g font-family="Hanken Grotesk" font-size="12.5" fill="{INK}">{"".join(tk)}</g></svg>')


# ================================================================ shared page parts
NAV = ["Home", "Data sources", "Architecture", "Models", "About"]


def mast(current: str) -> str:
    cur = ' aria-current="page"'
    li = "".join(f'<li><a href="#"{cur if n == current else ""}>{n}</a></li>' for n in NAV)
    return (f'<header class="d-mast"><a class="brand" href="#">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{li}</ul></nav></header>')


def hero(current: str, kind: str, h1: str, lede: str, crumb: str = "") -> str:
    c = f'<p class="crumb"><a href="#">Data sources</a><span aria-hidden="true"> / </span>{crumb}</p>' if crumb else ""
    return (f'<section class="band sky" aria-labelledby="h1">{mast(current)}'
            f'<div class="d-hero"><div>{c}<h1 id="h1">{h1}</h1></div><div class="d-lede">{lede}</div></div>'
            f'{strip_svg(kind)}</section>')


def band(kind: str, inner: str, seed: float, label: str = "", aria: str = "", cls: str = "") -> str:
    a = f' aria-labelledby="{aria}"' if aria else ""
    return (f'<section class="band g-{kind}{(" " + cls) if cls else ""}"{a}>{ground(kind, seed, label)}'
            f'<div class="band-in">{inner}</div></section>')


def footer(joined: bool = False) -> str:
    li = "".join(f'<li><a href="#">{n}</a></li>' for n in NAV)
    g = (f'<svg class="ground flat" width="{W}" height="100%" aria-hidden="true"><defs>{G["PATTERNS"]}</defs>'
         f'<rect width="100%" height="100%" fill="{PETROL}"></rect><rect width="100%" height="100%" '
         f'fill="url(#p-granite)" opacity=".5"></rect></svg>') if joined else ground("deep", 1.0)
    return (f'<footer class="band g-deep foot-band{" joined" if joined else ""}">{g}<div class="band-in d-foot">'
            f'<p class="brand">gridflow</p><p class="d-fnote">An open-source pipeline for UK and European power, gas, '
            f'weather and carbon data, under the Apache-2.0 licence. The models live in <code>gridflow-models</code>.'
            f'</p><nav aria-label="Footer"><ul>{li}</ul></nav></div></footer>')


D_CSS = """.root{background:#ECE8DA}
.band{position:relative}
.band-in{position:relative;z-index:2;padding:0 80px}
.ground{position:absolute;left:0;top:-26px;height:calc(100% + 26px);z-index:1;display:block}
.sky{background:#155A6E;z-index:1}
.d-mast{position:relative;z-index:2;padding:26px 80px 0;display:flex;justify-content:space-between;align-items:baseline;color:#F6F4EC}
.d-mast ul{display:flex;gap:30px;list-style:none;margin:0;padding:0;font-size:15px}
.d-mast ul a{text-decoration:none;color:#CFE0DC}
.d-mast ul a:hover{color:#F6F4EC}
.d-mast ul a[aria-current="page"]{color:#F6F4EC;box-shadow:inset 0 -2px 0 #AFC64E}
.d-hero{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,860px) 374px;justify-content:space-between;align-items:start;padding:52px 80px 0}
.d-hero h1{color:#F6F4EC;font-weight:760;font-stretch:84%;font-size:86px;line-height:.94;letter-spacing:-.022em}
.crumb{margin:0 0 18px;font-size:15px;color:#CFE0DC}
.crumb a{color:#F6F4EC;text-decoration-color:#AFC64E}
.d-lede{padding-top:12px}
.d-lede p{margin:0 0 12px;font-size:17.5px;line-height:1.6;color:#CFE0DC}
.d-lede code{color:#F6F4EC;font-size:.88em}
.strip{display:block;position:relative;z-index:1;margin-top:-6px}
.g-topsoil,.g-bronze,.g-silver,.g-gold{color:#1C2B22}
.d-grid{display:grid;grid-template-columns:minmax(0,1fr) 800px;column-gap:60px;align-items:start}
.d-grid.w7{grid-template-columns:minmax(0,1fr) 720px;column-gap:64px}
.d-grid.hub{grid-template-columns:minmax(0,1fr) 576px;column-gap:64px}
.d-grid.half{grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:64px}
.grps{margin-top:30px}
.d-h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0 0 16px}
.d-p{margin:0 0 14px;font-size:16px;line-height:1.62;color:#3F4A3B;max-width:58ch}
.d-p code,.d-cap code,.ent code,.facts code,.d-list code{font-size:.88em;color:#1C2B22}
.d-p a,.d-cap a{font-weight:600;color:#1C2B22;text-decoration-color:#66793B}
.ents{list-style:none;margin:30px 0 0;padding:0}
.ent{margin:0 0 30px}
.ent h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0}
.ent h3 a{text-decoration-color:rgba(28,43,34,0)}
.ent h3 a:hover{text-decoration-color:#66793B}
.ent .hd{margin:3px 0 6px;font:400 13.5px/1.45 "Red Hat Mono",monospace;color:#155A6E}
.ent .hd code{font-size:13.5px;color:#155A6E}
.ent .de{margin:0;font-size:14.5px;line-height:1.5;color:#3F4A3B;max-width:62ch}
.ent .fa{margin:6px 0 0;font-size:14.5px;line-height:1.5;font-weight:600;color:#1C2B22}
.ent .fa2{margin:3px 0 0;font-size:14px;line-height:1.5;color:#3F4A3B}
.ent.mk{display:grid;grid-template-columns:30px minmax(0,1fr);column-gap:16px}
.ent.mk svg{display:block;margin-top:4px}
.d-cap{margin:12px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:66ch}
.after{margin-top:40px}
.after h3,.facts h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 10px}
.card.wide{max-width:700px}
.card.wide dl div{grid-template-columns:184px minmax(0,1fr)}
.card.wide dd{font-size:13.5px}
.nb-body{padding:16px 24px 18px 8px}
.stream{margin:0;font:400 14px/1.6 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre-wrap;padding:6px 0 0 2px}
.plot{display:block;margin:6px 0 0}
.facts dl{margin:0;border-top:1px solid rgba(28,43,34,.22)}
.facts dl div{display:grid;grid-template-columns:120px minmax(0,1fr);gap:18px;padding:10px 0;border-bottom:1px solid rgba(28,43,34,.22)}
.facts dt{font-weight:600;font-size:14.5px}
.facts dd{margin:0;font-size:14.5px;line-height:1.5;color:#3F4A3B}
.grp{margin:0 0 34px}
.grp h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 8px}
.d-list{list-style:none;margin:0;padding:0;border-top:1px solid rgba(28,43,34,.22)}
.d-list li{display:grid;grid-template-columns:168px minmax(0,1fr);column-gap:18px;align-items:baseline;padding:10px 0 9px;border-bottom:1px solid rgba(28,43,34,.22)}
.d-list .k{font:400 16px/1.5 "Red Hat Mono",monospace;color:#1C2B22}
.d-list .k a{text-decoration-color:rgba(102,121,59,.0)}
.d-list .k a:hover{text-decoration-color:#66793B}
.d-list .v{font-size:14.5px;line-height:1.5;color:#3F4A3B}
.path{margin:18px 0 0;padding:12px 14px;background:rgba(246,244,236,.55);border:1px solid rgba(28,43,34,.3);border-radius:3px;font:400 14px/1.65 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre;overflow:hidden}
.path .t{color:#7C5530}
.fields{margin:14px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:62ch}
.fields code{font-size:.88em;color:#1C2B22}
.lyr{display:grid;grid-template-columns:minmax(0,1fr) 680px;column-gap:80px;align-items:start}
.lyr-cells{position:relative}
.lyr .cell{grid-template-columns:44px minmax(0,1fr)}
.lyr .df{background:#F6F4EC}
.tap{position:absolute;left:-58px;top:0;display:block}
.cable{position:absolute;top:-26px;bottom:0;left:0;width:1440px;height:calc(100% + 26px);z-index:1;pointer-events:none}
.g-deep{color:#F6F4EC}
.g-deep .d-h2{color:#F6F4EC}
.g-deep .d-p{color:#CFE0DC}
.g-deep .d-p code,.g-deep .d-list code{color:#F6F4EC}
.g-deep .d-list{border-top-color:rgba(207,224,220,.22)}
.g-deep .d-list li{border-bottom-color:rgba(207,224,220,.22)}
.g-deep .d-list .k{color:#F6F4EC}
.g-deep .d-list .v{color:#CFE0DC}
.g-deep h3{color:#F6F4EC;font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 8px}
.deep-grid{display:grid;grid-template-columns:minmax(0,640px) minmax(0,520px);justify-content:space-between;align-items:start}
.foot-band{padding:0}
.ground.flat{top:0;height:100%}
.joined .d-foot{padding-top:10px;border-top:1px solid rgba(207,224,220,.22);margin:0 80px;padding-left:0;padding-right:0}
.d-foot{display:grid;grid-template-columns:auto minmax(0,560px) auto;justify-content:space-between;align-items:baseline;gap:40px;padding-top:58px;padding-bottom:56px;color:#F6F4EC}
.d-foot .brand{margin:0;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:24px}
.d-fnote{margin:0;font-size:14.5px;line-height:1.55;color:#CFE0DC}
.d-fnote code{color:#F6F4EC;font-size:.9em}
.d-foot ul{display:flex;gap:24px;list-style:none;margin:0;padding:0;font-size:14.5px}
.d-foot a{color:#CFE0DC;text-decoration:none}
.d-foot a:hover{color:#F6F4EC}
"""


def board(slug: str, title: str, current: str, parts: list[str]) -> tuple[str, str]:
    h = HEIGHTS.get(slug, 4000)
    body = "\n".join(parts[:-1])
    foot = parts[-1]
    dc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{G["FONTS"]}
<style>
{G["CSS"]}{D_CSS}</style>
</helmet>
<div class="root" style="width: {W}px; height: {h}px; overflow: hidden; position: relative">
<main>
{body}
</main>
{foot}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""
    return dc, G["static"](dc)


def ent(name: str, handle: str, desc: str, fact: str, extra: str = "", mark: str = "") -> str:
    inner = (f'<h3><a href="#">{name}</a></h3><p class="hd">{handle}</p><p class="de">{desc}</p>'
             f'<p class="fa">{fact}</p>{extra}')
    if mark:
        return f'<li class="ent mk">{mark}<div>{inner}</div></li>'
    return f'<li class="ent">{inner}</li>'


# ================================================================ 1. data sources
def page_sources() -> list[str]:
    lede = ('<p>gridflow ingests [N datasets] from seven vendors: GB and European electricity, gas, weather and '
            'carbon intensity. Five need no API key; ENTSO-E and GIE each need one.</p>')
    V = [
        ("Elexon BMRS", "<code>data.elexon</code>",
         "GB balancing-mechanism data: system prices, generation outturn, BM-unit data, and demand and wind forecasts.",
         "[n] datasets, mostly half-hourly settlement periods, no API key"),
        ("ENTSO-E", "<code>data.entsoe</code>",
         "European electricity: day-ahead prices, load, generation by type, cross-border flows, outages and balancing.",
         "[n] datasets, XML responses, API key required"),
        ("ENTSO-G", "<code>data.entsog</code>",
         "European gas: physical flows, nominations, capacities, gas quality and tariffs at interconnection points.",
         "[n] datasets, daily by gas day, no API key"),
        ("GIE AGSI+ and ALSI", "<code>data.gie_agsi</code> and <code>data.gie_alsi</code>",
         "EU gas storage levels and flows (AGSI+), and LNG terminal inventory and send-out (ALSI).",
         "[n] datasets, daily by gas day, one API key for both"),
        ("NESO Carbon Intensity", "<code>data.neso</code>",
         "GB national and regional carbon intensity, actual and forecast, with fuel emission factors and the "
         "generation mix.", "[n] datasets, half-hourly, no API key"),
        ("NESO Data Portal", "<code>data.neso_data_portal</code>",
         "Files from NESO&#8217;s open-data catalogue, including the GB generation mix by fuel since 2009, solar "
         "included.", "[n] datasets, the portal&#8217;s current file only, no API key"),
        ("Open-Meteo", "<code>data.open_meteo</code>",
         "Weather for GB power modelling: ERA5 archive and forecasts at 7 demand cities, 12 wind sites and 6 solar "
         "sites.", "[n] datasets, hourly, no API key"),
    ]
    ents = "".join(ent(*v) for v in V)
    left = (f'<h2 class="d-h2" id="src-h">One handle per source</h2>'
            f'<p class="d-p">The catalogue is organised by vendor, and in the <code>gridflow-models</code> notebook each '
            f'vendor is a handle on <code>data</code>. GIE has two, one for storage and one for LNG, so seven vendors '
            f'give eight handles. Every handle answers the same seven verbs.</p>'
            f'<ul class="ents" aria-label="Vendors">{ents}</ul>')
    cells = [
        cell("[1]:", inp(SETUP)),
        cell("[2]:", inp("data")),
        cell("[2]:", index_card("data", DATA_ROWS, "Discover datasets", "data.elexon.list_datasets()", "wide"), "out"),
    ]
    aria = ("A notebook, catalogue.ipynb, on the gridflow_models kernel. Cell 1 runs setup_notebook. Cell 2 shows "
            "the data handle's help card: one row for each of the eight sources (elexon, entsoe, entsog, gie_agsi, "
            "gie_alsi, neso, neso_data_portal, open_meteo), then the cross-source verbs list_data_sources, list_tables, "
            "list_freshness, sql, refresh_all, training_set, imbalance_context and gb_day_ahead_benchmark.")
    right = (notebook("catalogue.ipynb", cells, aria) +
             '<div class="after"><h3>Finding a dataset</h3>'
             '<p class="d-p">Each vendor page lists its datasets by theme. Each dataset has its own page: what it '
             'measures, its grain and units, the silver schema, sample rows and the caveats.</p>'
             '<p class="d-p">A dataset keeps one name throughout. <code>system_prices</code> is the gridflow key, '
             '<code>silver_elexon_system_prices</code> is its DuckDB view, and '
             '<code>data.elexon.query("system_prices", start, end)</code> reads it in a notebook.</p></div>')
    main = band("bronze", f'<div class="d-grid pad">{f"<div>{left}</div><div>{right}</div>"}</div>', 0.4, "bronze",
                "src-h")
    return [hero("Data sources", "sources", "Where the data comes from", lede), band("topsoil", "", 0, cls="thin"),
            main, footer()]


# ================================================================ 2. Elexon hub
ELEXON_GROUPS = [
    ("Prices and balancing", [
        ("system_prices", "System sell price and system buy price per settlement period"),
        ("market_depth", "Settlement market depth per settlement period"),
        ("mid", "Market index data; its APXMIDP provider is the GB day-ahead benchmark"),
        ("boal", "Bid/offer acceptance levels (BOALF; replaces the deprecated BOAL)"),
        ("pn", "Physical notifications, per BM unit and settlement period"),
        ("disbsad", "Disaggregated balancing services adjustment data"),
        ("netbsad", "Net balancing services adjustment data"),
        ("soso", "SO-SO prices (cross-border interconnector trading)")]),
    ("Generation and availability", [
        ("fuelhh", "Half-hourly generation outturn by fuel type (no solar)"),
        ("fuelinst", "Instantaneous generation outturn by fuel type"),
        ("agpt", "Actual aggregated generation per type (B1620)"),
        ("agws", "Actual or estimated wind and solar generation (B1630)"),
        ("windfor", "Wind generation forecast"),
        ("fou2t14d", "Generation availability by fuel type, 2 to 14 days ahead"),
        ("uou2t14d", "Generation availability by BM unit, 2 to 14 days ahead"),
        ("nonbm", "Non-BM STOR generation")]),
    ("Demand", [
        ("indo", "Initial national demand outturn"),
        ("itsdo", "Initial transmission system demand outturn"),
        ("indod", "Initial national demand outturn, daily total"),
        ("atl", "Actual total load per bidding zone (B0610)"),
        ("ndf", "National demand forecast, day ahead"),
        ("ndfd", "National demand forecast, 2 to 14 days ahead"),
        ("tsdf", "Transmission system demand forecast"),
        ("tsdfd", "Transmission system demand forecast, 2 to 14 days ahead"),
        ("inddem", "Day and day-ahead indicated demand")]),
    ("System indicators", [
        ("indgen", "Day and day-ahead indicated generation"),
        ("imbalngc", "Indicated imbalance"),
        ("melngc", "Indicated margin"),
        ("lolpdrm", "Loss of load probability and de-rated margin"),
        ("freq", "System frequency"),
        ("temp", "Temperature data")]),
    ("Reference and messages", [
        ("bmunits_reference", "All BM unit reference data"),
        ("remit", "REMIT outage and unavailability messages")]),
]


def page_elexon() -> list[str]:
    assert sum(len(r) for _, r in ELEXON_GROUPS) == 33
    lede = ('<p>GB balancing-mechanism data from Elexon&#8217;s Insights API: system prices, generation outturn, '
            'BM-unit data, and demand and wind forecasts. [n] datasets, and no API key is needed.</p>')
    grps = "".join(
        f'<div class="grp"><h3 id="g{i}">{name}</h3><ul class="d-list" aria-labelledby="g{i}">'
        + "".join(f'<li><span class="k"><a href="#">{k}</a></span><span class="v">{v}</span></li>' for k, v in rows)
        + '</ul></div>' for i, (name, rows) in enumerate(ELEXON_GROUPS))
    left = (f'<h2 class="d-h2" id="ds-h">Datasets by theme</h2>'
            f'<p class="d-p">Each name is the gridflow key: the page, the silver view '
            f'<code>silver_elexon_&lt;key&gt;</code> and the notebook call all use it.</p><div class="grps">{grps}</div>')
    pts = PACK["series"]["elexon_hub"]["points"]
    vals = [v for _, v in pts]
    xt = [(i, m[:4]) for i, (m, _) in enumerate(pts) if m.endswith("-01")]
    plot = mpl(478, 280, len(vals), [(vals, HORIZON, 1.6)], 3000, 12200, [4000, 6000, 8000, 10000, 12000], xt,
               "settlement_date", "MW",
               "Line plot of monthly mean wind generation_mw from Elexon FUELHH, September 2021 to August 2026, in MW: "
               "it swings between about 3,700 MW in summer months and about 11,600 MW in winter, highest in "
               "January 2026.")
    q = 'df = data.elexon.query(\n    "fuelhh", "2021-09-01", "2026-08-31")'
    p4 = ('wind = df[df.fuel_type == "WIND"]\n'
          'day = common.pd.to_datetime(wind.settlement_date)\n'
          'by_month = wind.groupby(day.dt.to_period("M"))\n'
          'by_month.generation_mw.mean().plot(ylabel="MW")')
    cells = [
        cell("[1]:", inp(SETUP)),
        cell("[2]:", inp("data.elexon")),
        cell("[2]:", index_card("data.elexon", ELEXON_ROWS, "Discover datasets", "data.elexon.list_datasets()"), "out"),
        cell("[3]:", inp(q)),
        cell("[4]:", inp(p4)),
        cell("[4]:", f'<div><p class="stream">&lt;Axes: xlabel=&#x27;settlement_date&#x27;, ylabel=&#x27;MW&#x27;&gt;</p>'
                     f'{plot}</div>', "out"),
    ]
    aria = ("A notebook, elexon.ipynb, on the gridflow_models kernel. Cell 2 shows the data.elexon help card with its "
            "seven verbs: list_datasets, refresh, describe, backfill, query, tail and coverage. Cell 3 queries fuelhh "
            "from 1 September 2021 to 31 August 2026; cell 4 groups the wind rows by month and plots the mean.")
    facts = [
        ("API", "<code>https://data.elexon.co.uk/bmrs/api/v1</code>, no key"),
        ("Market", "GB electricity"),
        ("Grain", "Half-hourly settlement periods, 1 to 50 a day (46 or 50 when the clocks change). FUELINST is "
                  "instantaneous, every 5 minutes; some datasets are daily publications or 2 to 14-day forecasts."),
        ("Prices", "<code>system_prices</code> carries a single imbalance price: SSP equals SBP on every "
                   "latest-vintage row from 1 September 2021 to 22 September 2026."),
        ("Benchmark", "The APXMIDP provider in <code>mid</code> is the GB day-ahead benchmark, read through "
                      "<code>gold_gb_day_ahead_benchmark</code>."),
        ("Solar", "FUELHH has no solar rows. GB solar outturn is in the NESO Data Portal&#8217;s "
                  "<code>historic_generation_mix</code>."),
    ]
    fdl = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in facts)
    right = (notebook("elexon.ipynb", cells, aria)
             + '<p class="d-cap">The plot in [4]: monthly mean of the half-hourly wind rows in '
               '<code>elexon/fuelhh</code> (<code>generation_mw</code>, MW), September 2021 to August 2026. It is a '
               'mean per row, not total output.</p>'
             + f'<div class="facts after"><h3 id="feed-h">The feed</h3><dl aria-labelledby="feed-h">{fdl}</dl></div>')
    main = band("bronze", f'<div class="d-grid hub pad"><div>{left}</div><div>{right}</div></div>', 1.3, "bronze", "ds-h")
    return [hero("Data sources", "elexon", "Elexon BMRS", lede, "Elexon BMRS"), band("topsoil", "", 0, cls="thin"),
            main, footer()]


# ================================================================ 3. architecture
def tap(core: str, tint: str) -> str:
    """The dataset's cable tapping a cell: a short run from the riser to a terminal by the first prompt."""
    return (f'<svg class="tap" width="58" height="40" viewBox="0 0 58 40" aria-hidden="true">'
            f'<path d="M18 20 H40" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"></path>'
            f'<path d="M18 20 H40" stroke="{core}" stroke-width="1.5"></path>'
            f'<circle cx="44" cy="20" r="6.5" fill="{tint}" stroke="{INK}" stroke-width="2"></circle>'
            f'<circle cx="44" cy="20" r="2.2" fill="{INK}"></circle></svg>')


RISER_X = 640   # page x of the vertical cable (the gutter between prose and cells)


def riser(core: str, top_splice: bool = False, end_at: int | None = None) -> str:
    y2 = f"{end_at}" if end_at is not None else "100%"
    sp = ""
    if top_splice:
        sp = (f'<rect x="{RISER_X - 9}" y="8" width="18" height="36" rx="9" fill="{core}" stroke="{INK}" '
              f'stroke-width="1.6"></rect><path d="M{RISER_X - 9} 18 H{RISER_X + 9} M{RISER_X - 9} 34 H{RISER_X + 9}" '
              f'stroke="{INK}" stroke-width="1" opacity=".5"></path>')
    return (f'<svg class="cable" aria-hidden="true">'
            f'<line x1="{RISER_X}" y1="0" x2="{RISER_X}" y2="{y2}" stroke="{INK}" stroke-width="4.4" '
            f'stroke-linecap="round"></line>'
            f'<line x1="{RISER_X}" y1="0" x2="{RISER_X}" y2="{y2}" stroke="{core}" stroke-width="1.5"></line>{sp}</svg>')


def page_arch() -> list[str]:
    lede = ('<p>gridflow is a local-first Python pipeline built on Polars, DuckDB, Pydantic and httpx, run from a '
            'Typer command line. There is no server, scheduler or cloud: data lands when someone runs a command.</p>'
            '<p>This page follows one dataset, Elexon <code>system_prices</code>, from the API response to the view '
            'a notebook reads.</p>')
    top = (f'<div class="lyr pad-s"><div><h2 class="d-h2" id="fol-h">Follow one dataset down</h2>'
           f'<p class="d-p">Each layer below shows where <code>system_prices</code> is stored and the notebook cell '
           f'that reads it. The cells are one <code>gridflow-models</code> session, run from top to bottom.</p></div>'
           f'<div class="lyr-cells">{tap(BRONZE, T_TOP)}{cell("[1]:", inp(SETUP))}</div></div>')
    # bronze
    bpath = ('bronze/elexon/system_prices/2026/09/22/\n'
             '  raw_<span class="t">{fetched_at:%Y%m%dT%H%M%SZ}</span>_<span class="t">{sha256[:8]}</span>.json\n'
             '  raw_<span class="t">{fetched_at:%Y%m%dT%H%M%SZ}</span>_<span class="t">{sha256[:8]}</span>.meta.json')
    b_in = ('summary = data.elexon.backfill(\n'
            '    "system_prices", "2026-09-19", "2026-09-22", yes=True)')
    bronze = (f'<div class="lyr pad"><div><h2 class="d-h2" id="b-h">Bronze keeps the response as it arrived</h2>'
              f'<p class="d-p">The Elexon connector fetches the API response and writes its bytes once, never rewritten, '
              f'as <code>.json</code>, <code>.xml</code>, <code>.csv</code> or <code>.bin</code> by content type. A '
              f'sidecar beside it records the request. Files are partitioned by the data&#8217;s date, or by the fetch '
              f'date when that is unknown.</p>'
              f'<pre class="path" aria-label="Bronze file path pattern">{bpath}</pre>'
              f'<p class="fields">Sidecar fields: <code>source</code>, <code>dataset</code>, <code>fetched_at</code>, '
              f'<code>written_at</code>, <code>data_date</code>, <code>request_url</code>, <code>request_params</code> '
              f'(credentials masked), <code>api_version</code>, <code>http_status</code>, <code>content_type</code>, '
              f'<code>body_sha256</code>, <code>body_size_bytes</code>, <code>page</code>, <code>total_pages</code>.</p>'
              f'</div><div class="lyr-cells">{tap(BRONZE, T_BRONZE)}{cell("[2]:", inp(b_in))}'
              f'<p class="d-cap">For each chunk of days, <code>backfill</code> runs <code>gridflow ingest</code> and '
              f'then <code>gridflow transform</code>, so this one cell fills bronze and silver. Nothing is fetched '
              f'without <code>yes=True</code>; Elexon is called at most twice a second.</p></div></div>')
    # silver
    spath = ('silver/elexon/system_prices/year=2026/month=09/\n'
             '  system_prices_20260922_run<span class="t">{available_at}</span>.parquet')
    sql = ('data.sql("""\n'
           '    SELECT settlement_date,\n'
           '           round(avg(system_sell_price), 2) AS ssp_mean\n'
           '    FROM silver_elexon_system_prices_latest\n'
           "    WHERE settlement_date BETWEEN '2026-09-19' AND '2026-09-22'\n"
           '    GROUP BY settlement_date ORDER BY settlement_date\n'
           '""")')
    sp = {d: v for d, v in PACK["series"]["data_sources_landing"]["points"]}
    rows = [(d, f"{sp[d]:.2f}") for d in ("2026-09-19", "2026-09-20", "2026-09-21", "2026-09-22")]
    silver = (f'<div class="lyr pad"><div><h2 class="d-h2" id="s-h">Silver is typed, checked and deduplicated</h2>'
              f'<p class="d-p">One transformer per dataset reads a day of bronze, validates every row against a '
              f'Pydantic schema, converts time to UTC, drops duplicates on the dataset&#8217;s key and writes Parquet '
              f'compressed with zstd.</p>'
              f'<p class="d-p"><code>system_prices</code> is append-only: each capture is kept under its own '
              f'<code>_run</code> suffix, and the <code>_latest</code> view picks the newest vintage for each '
              f'settlement period.</p>'
              f'<pre class="path" aria-label="Silver file path pattern">{spath}</pre>'
              f'<p class="fields">Every silver table checked carries <code>event_time</code>. The tables sampled also carry '
              f'<code>available_at</code>, <code>published_at</code>, <code>ingested_at</code>, '
              f'<code>source_run_id</code> and <code>dataset_version</code>, so a read can be made as of a point in '
              f'time.</p></div>'
              f'<div class="lyr-cells">{tap(SILVER, T_SILVER)}{cell("[3]:", inp(sql))}'
              f'{cell("[3]:", df_html(["settlement_date", "ssp_mean"], rows), "out")}'
              f'<p class="d-cap">Daily means of the system sell price in £/MWh, over the latest vintage of each of the '
              f'48 settlement periods.</p></div></div>')
    # gold
    hc = ('<div class="card hc"><div class="hc-h"><p class="hc-n">data.imbalance_context()</p>'
          '<p class="hc-s">Read the cross-source imbalance-context view over a date range.</p></div>'
          '<div class="hc-b"><pre class="hc-sig">imbalance_context(start: &#x27;date | str&#x27;, end: '
          '&#x27;date | str&#x27;) -&gt; &#x27;pd.DataFrame&#x27;</pre><p class="hc-sec">Parameters</p><dl>'
          '<div><dt>start<span>: date | str</span></dt><dd>Start of the range, inclusive. A date or '
          '&quot;YYYY-MM-DD&quot;.</dd></div>'
          '<div><dt>end<span>: date | str</span></dt><dd>End of the range, inclusive.</dd></div></dl>'
          '<p class="hc-sec rt">Returns</p><p class="hc-r">A DataFrame of imbalance-context rows for the range, '
          'time-ordered.</p></div></div>')
    views = [("gold_uk_imbalance_context", "Elexon system prices with NESO carbon intensity, half-hourly"),
             ("gold_gb_day_ahead_benchmark", "Elexon MID APXMIDP in £/MWh, per settlement period"),
             ("gold_eu_gas_storage", "GIE AGSI+ storage by country and day")]
    vl = "".join(f'<li><span class="k">{k}</span><span class="v">{v}</span></li>' for k, v in views)
    gold = (f'<div class="lyr pad"><div><h2 class="d-h2" id="g-h">Gold is ready to query</h2>'
            f'<p class="d-p"><code>gridflow init</code> registers every silver and gold directory as a view in '
            f'<code>gridflow.duckdb</code>, beside three tables that log runs, watermarks and quality reports. Three '
            f'SQL views ship with gridflow:</p><ul class="d-list v2" aria-label="Gold SQL views">{vl}</ul>'
            f'<p class="d-p after-s"><code>gridflow build</code> runs gridflow&#8217;s own gold builder, '
            f'<code>system_marginal_price</code>. <code>gridflow-models</code> writes its forecasts and scores into the '
            f'same gold root, and they register as views too.</p></div>'
            f'<div class="lyr-cells">{tap(GOLD, T_GOLD)}{cell("[4]:", inp("data.imbalance_context"))}'
            f'{cell("[4]:", hc, "out")}'
            f'<p class="d-cap">A bare verb renders its help card; called with a start and an end, it returns '
            f'<code>gold_uk_imbalance_context</code> as a DataFrame.</p></div></div>')
    cli = [("init", "Create the DuckDB catalogue and register the views"),
           ("ingest", "Fetch from a vendor API into bronze"),
           ("transform", "Bronze to silver: parse, validate, deduplicate"),
           ("build", "Silver to gold"),
           ("pipeline", "Ingest then transform, and build with <code>--gold</code>"),
           ("backfill", "Fetch history in chunks"),
           ("export-csv", "Write silver Parquet out as CSV"),
           ("status", "Run history and a quality summary"),
           ("quality", "Run the quality checks and write a report"),
           ("reset", "Delete bronze, silver and gold data and reset the catalogue"),
           ("prune", "Delete partitions older than a retention cutoff")]
    cl = "".join(f'<li><span class="k">{k}</span><span class="v">{v}</span></li>' for k, v in cli)
    deep = (f'<div class="deep-grid pad"><div><h2 class="d-h2" id="c-h">Commands and checks</h2>'
            f'<p class="d-p">Every run is a <code>gridflow</code> command.</p>'
            f'<ul class="d-list cli" aria-label="gridflow commands">{cl}</ul></div>'
            f'<div class="chk"><h3>Quality checks</h3><p class="d-p"><code>gridflow quality</code> runs five checks '
            f'on a dataset (null rate, time-series gaps, value ranges, row counts and duplicates) and writes the '
            f'results to <code>quality_reports</code>.</p>'
            f'<h3>Gates</h3><p class="d-p">gridflow&#8217;s CI runs on every push and pull request: '
            f'<code>uv lock --check</code>, <code>ruff check</code>, <code>ruff format --check</code>, '
            f'<code>mypy</code> and <code>pytest -m "not live"</code>.</p>'
            f'<p class="d-p">This site is rendered from the dataset notes by <code>gridflow-build</code>; '
            f'<code>gridflow-build --check</code>, htmlhint and lychee run before GitHub Pages publishes it.</p>'
            f'<h3>Not in gridflow</h3><p class="d-p">No scheduler: every run is a command. No server, cloud or hosted '
            f'database: local files and one DuckDB file. No models or trading: forecasts live in '
            f'<code>gridflow-models</code>.</p></div></div>')
    return [hero("Architecture", "arch", "Three layers on one machine", lede),
            f'<section class="band g-topsoil" aria-labelledby="fol-h">{ground("topsoil", 0)}{riser(BRONZE)}'
            f'<div class="band-in">{top}</div></section>',
            f'<section class="band g-bronze" aria-labelledby="b-h">{ground("bronze", .4, "bronze")}{riser(BRONZE)}'
            f'<div class="band-in">{bronze}</div></section>',
            f'<section class="band g-silver" aria-labelledby="s-h">{ground("silver", 2.1, "silver")}'
            f'{riser(SILVER, True)}<div class="band-in">{silver}</div></section>',
            f'<section class="band g-gold" aria-labelledby="g-h">{ground("gold", 4.0, "gold")}'
            f'{riser(GOLD, True, HEIGHTS.get("arch_gold_end", 120))}<div class="band-in">{gold}</div></section>',
            f'<section class="band g-deep" aria-labelledby="c-h">{ground("deep", 1.0)}<div class="band-in">{deep}'
            f'</div></section>', footer(joined=True)]


# ================================================================ 4. models
def mark(kind: str) -> str:
    """The homepage's keyed-index marks (gen_b), shape-distinct at 30 x 18."""
    if kind == "smp":
        rows = [3, 7, 12, 9, 4]
        body = (f'<g fill="{GOLD}">' + "".join(f'<rect x="{25 - v * 1.7:.1f}" y="{2 + i * 3}" width="{v * 1.7:.1f}" '
                                                f'height="2.4"></rect>' for i, v in enumerate(rows)) + '</g>'
                f'<path d="M26 1 V17" stroke="{INK}" stroke-width="1.4"></path>')
    elif kind == "stack":
        body = (f'<rect x="1" y="12" width="7" height="5" fill="{PETROL}"></rect>'
                f'<rect x="8" y="8" width="13" height="9" fill="{CLAY}"></rect>'
                f'<rect x="21" y="3" width="8" height="14" fill="{CLAY}"></rect>'
                f'<path d="M1 12 H8 V8 H21 V3 H29" fill="none" stroke="{INK}" stroke-width="1.4"></path>')
    elif kind == "solar":
        body = (f'<rect x="1" y="6" width="10" height="6" fill="{OLIVE}" opacity=".5"></rect>'
                f'<rect x="11" y="6" width="10" height="6" fill="{CHART}"></rect>'
                f'<rect x="21" y="6" width="8" height="6" fill="{HORIZON}" opacity=".3"></rect>'
                f'<rect x="7" y="3" width="8" height="12" fill="{CHART}" opacity=".38" stroke="{INK}" '
                f'stroke-width=".6"></rect><path d="M11 1 V17" stroke="{INK}" stroke-width="1.6"></path>')
    elif kind == "wind":
        body = (f'<rect x="1" y="6" width="13" height="6" fill="{OLIVE}" opacity=".5"></rect>'
                f'<rect x="14" y="6" width="15" height="6" fill="{HORIZON}"></rect>'
                f'<rect x="7" y="3" width="14" height="12" fill="{HORIZON}" opacity=".38" stroke="{INK}" '
                f'stroke-width=".6"></rect><path d="M14 1 V17" stroke="{INK}" stroke-width="1.6"></path>')
    else:
        body = (f'<rect x="1" y="6" width="22" height="6" fill="{OLIVE}" opacity=".5"></rect>'
                f'<rect x="17" y="3" width="12" height="12" fill="{OLIVE}" opacity=".38" stroke="{INK}" '
                f'stroke-width=".6"></rect><rect x="20" y="3" width="6" height="12" fill="{OLIVE}" opacity=".8"></rect>'
                f'<path d="M23 1 V17" stroke="{INK}" stroke-width="1.6"></path>')
    return f'<svg width="30" height="18" viewBox="0 0 30 18" aria-hidden="true">{body}</svg>'


def page_models() -> list[str]:
    lede = ('<p><code>gridflow-models</code> is a separate library. It reads gridflow&#8217;s DuckDB views and '
            'Parquet files, and writes its forecasts and scores back into gold.</p>'
            '<p>It holds five models, from half-hourly demand to a fundamentals price, and it places no orders.</p>')
    M = [
        ("Day-ahead demand", "<code>day_ahead.lgbm_demand.v1</code>, <code>.v2</code>",
         "GB national demand outturn (Elexon INDO), half-hourly in MW, 24 hours ahead. LightGBM quantile regression, "
         "one model per quantile, with a conformal outer band; v2 adds weather and calendar inputs.",
         "v1: pinball loss 711.04 MW at the median; 89.3% of outturns inside the 90% band.",
         '<p class="fa2">Scored over 12 walk-forward folds, September 2024 to August 2026. v2 scores 599.72 MW on the '
         'same folds with actual weather standing in for forecasts, so its score is optimistic.</p>', "demand"),
        ("Wind generation", "<code>wind.lgbm_quantile.v1</code>",
         "GB wind outturn (Elexon FUELHH wind), half-hourly in MW, 24 hours ahead. LightGBM quantile regression on "
         "weather at 12 wind sites, benchmarked against WINDFOR.",
         "It has a model card and a training dataset. No forecasts or scores are stored.", "", "wind"),
        ("Solar generation", "<code>solar.lgbm_quantile.v1</code>",
         "Configured on Elexon FUELHH solar, 24 hours ahead, with weather at 6 solar sites and a persistence "
         "benchmark.",
         "FUELHH has no solar rows, so the configured target is empty and no forecasts or scores exist.", "", "solar"),
        ("GB merit-order stack", "<code>stack.gb.v1</code>",
         "The GB supply curve for a settlement period as known at a decision time: BM units ranked by short-run "
         "marginal cost, built from the BM unit register, REMIT availability, fuel and carbon prices and plant "
         "parameters. It is built, not fitted.",
         "It has no score of its own; it is scored through the fundamentals SMP model.", "", "stack"),
        ("Fundamentals SMP", "<code>fundamentals_smp.gb.v1</code>",
         "Clears the stack against realised residual demand (national demand less wind, solar and netting) to give a "
         "half-hourly day-ahead price, scored against Elexon MID APXMIDP.",
         "Headline backtest, 18 August to 3 September 2026 (816 periods): mean bias −151.80 £/MWh, and every period "
         "under-predicts.",
         '<p class="fa2">Realised inputs stand in for forecasts, fuel and carbon prices are synthetic, the clearing '
         'price has a −500 £/MWh floor, and APXMIDP mixes day-ahead and intraday trades.</p>', "smp"),
    ]
    ents = "".join(ent(n, h, d, fa, ex) for n, h, d, fa, ex, _ in M)
    left = (f'<h2 class="d-h2" id="m-h">Five models, six handles</h2>'
            f'<p class="d-p">In a notebook each model is a handle on <code>models</code>. Demand has two versions, so '
            f'five models give six handles.</p><ul class="ents" aria-label="Models">{ents}</ul>')
    fc = PACK["series"]["models_landing_demand"]["points"]
    act = [p[1] for p in fc]
    q05, q50, q95 = [p[2] for p in fc], [p[3] for p in fc], [p[4] for p in fc]
    xt = [(0, "Aug 20"), (24, "12:00"), (48, "Aug 21"), (72, "12:00")]
    plot = mpl(622, 320, len(fc), [(q50, OLIVE, 1.8), (act, INK, 1.5)], 16000, 33000,
               [18000, 20000, 22000, 24000, 26000, 28000, 30000, 32000], xt, "delivery_time", "MW",
               "Line plot of GB national demand, 20 to 21 August 2026 in UTC, in MW: the outturn and the median "
               "day-ahead forecast run close together between about 17,500 and 31,600 MW, inside a shaded band from "
               "the 5% to the 95% quantile.",
               band=(q05, q95, OLIVE), legend=[("actual", INK), ("q_0.5", OLIVE)])
    sql = ('fc = data.sql("""\n'
           '    SELECT delivery_time, actual, "q_0.05", "q_0.5", "q_0.95"\n'
           '    FROM gold_forecasts\n'
           "    WHERE run_id = 'a55a829bc51c40b2'\n"
           "      AND delivery_time &gt;= '2026-08-20'\n"
           "      AND delivery_time &lt; '2026-08-22'\n"
           '    ORDER BY delivery_time\n'
           '""")')
    p4 = ('ax = fc.plot(x="delivery_time", y=["actual", "q_0.5"], ylabel="MW")\n'
          'ax.fill_between(fc.delivery_time, fc["q_0.05"], fc["q_0.95"],\n'
          '                alpha=.3);')
    cells = [
        cell("[1]:", inp(SETUP)),
        cell("[2]:", inp("print(models)")),
        cell("[2]:", '<p class="stream">Models(models=[&#x27;demand_forecast&#x27;, &#x27;demand_forecast_v2&#x27;, '
                     '&#x27;fundamentals_smp&#x27;, &#x27;solar_forecast&#x27;, &#x27;stack&#x27;, '
                     '&#x27;wind_forecast&#x27;])</p>', "out"),
        cell("[3]:", f'<pre class="in">{hl_sql(sql)}</pre>'),
        cell("[4]:", inp(p4)),
        cell("[4]:", plot, "out"),
    ]
    aria = ("A notebook, models.ipynb, on the gridflow_models kernel. Cell 2 prints the models handle: demand_forecast, "
            "demand_forecast_v2, fundamentals_smp, solar_forecast, stack and wind_forecast. Cell 3 reads run "
            "a55a829bc51c40b2 from gold_forecasts for 20 and 21 August 2026; cell 4 plots the outturn and median "
            "forecast with the 5% to 95% band shaded.")
    right = (notebook("models.ipynb", cells, aria)
             + '<p class="d-cap">The plot in [4]: day-ahead demand v1, walk-forward fold 12, GB national demand in MW, '
               '20 to 21 August 2026 (UTC). The line pair is the outturn and the median forecast; the shading runs from '
               'the 5% to the 95% quantile. Source: gold <code>forecasts</code>, run <code>a55a829bc51c40b2</code>.</p>')
    main = f'<div class="d-grid w7 pad">{f"<div>{left}</div><div>{right}</div>"}</div>'
    gv = [("gold_forecasts", "Quantile forecasts beside the outturn, per delivery half-hour"),
          ("gold_forecast_metrics", "Scores per run and per walk-forward fold"),
          ("gold_stack_clearing", "Fundamentals SMP clearing prices per settlement period"),
          ("gold_stack_residual_demand", "The residual demand each SMP run clears against"),
          ("gold_stack_supply_curve_points", "The supply-curve points behind each cleared period")]
    gl = "".join(f'<li><span class="k">{k}</span><span class="v">{v}</span></li>' for k, v in gv)
    defs = [("Pinball loss", "The mean quantile loss at the median (q 0.5), in MW for demand. It equals half the mean "
                             "absolute error of the median forecast."),
            ("Coverage", "The share of outturns inside the band from the 5% to the 95% quantile. A calibrated band "
                         "covers 90%."),
            ("Gates", "A model passes when its pinball loss at the median is at most 1,500 MW, its coverage is within "
                      "0.90 ± 0.05, and no quantiles cross.")]
    dd = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in defs)
    gold = (f'<div class="d-grid half pad"><div><h2 class="d-h2" id="o-h">Where the outputs land</h2>'
            f'<p class="d-p">Forecasts and scores are written to gold as Parquet, partitioned by model, and read back '
            f'through DuckDB views.</p><ul class="d-list wide" aria-label="Model output views">{gl}</ul></div>'
            f'<div class="facts"><h3 id="sc-h">How a forecast is scored</h3><dl aria-labelledby="sc-h">{dd}</dl></div>'
            f'</div>')
    return [hero("Models", "models", "Models that read the warehouse", lede),
            band("topsoil", main, 0, aria="m-h", cls="top-main"),
            band("gold", gold, 4.0, "gold", "o-h"), footer()]


def hl_sql(sql: str) -> str:
    """The SQL cell is already HTML-escaped where needed; tint the triple-quoted literal only."""
    return re.sub(r'"""[\s\S]*?"""', lambda m: f'<span class="s">{m.group(0)}</span>', sql)


EXTRA_CSS = """.pad{padding-top:74px;padding-bottom:96px}
.pad-s{padding-top:46px;padding-bottom:70px}
.thin .band-in{height:64px}
.top-main .pad{padding-top:58px}
.hc{max-width:620px}
.hc-h{padding:9px 14px;background:#ECE8DA;border-bottom:1px solid rgba(28,43,34,.2)}
.hc-n{margin:0;font:500 15px/1.2 "Red Hat Mono",monospace;color:#155A6E}
.hc-s{margin:5px 0 0;font-size:14px;line-height:1.4;color:#3F4A3B}
.hc-b{padding:10px 14px 12px}
.hc-sig{margin:0 0 10px;padding:7px 10px;background:#ECE8DA;border-radius:3px;font:400 13px/1.5 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre-wrap}
.hc-sec{margin:0 0 5px;font-size:13.5px;font-weight:600;color:#3F4A3B}
.hc-sec.rt{margin-top:10px;padding-top:9px;border-top:1px solid rgba(28,43,34,.2)}
.hc dl{margin:0;padding:0}
.hc dl div{grid-template-columns:150px minmax(0,1fr)}
.hc dt span{color:#5d6a55}
.hc-r{margin:0;font-size:14px;line-height:1.45;color:#1C2B22}
.d-list.v2 li{grid-template-columns:250px minmax(0,1fr)}
.d-list.v2 .k{font-size:14.5px}
.d-list.wide li{grid-template-columns:270px minmax(0,1fr)}
.d-list.wide .k{font-size:14.5px}
.d-list.cli li{grid-template-columns:120px minmax(0,1fr);padding:8px 0 7px}
.d-list.cli .k{font-size:15px}
.after-s{margin-top:18px}
.chk{padding-top:8px}
.chk h3{margin-top:22px}
.chk h3:first-child{margin-top:0}
.lyr .d-cap{margin-left:54px}
.g-gold .facts dl{border-top-color:rgba(28,43,34,.3)}
"""
D_CSS += EXTRA_CSS

PAGES = {
    "data-sources": ("Data sources", "Data sources", page_sources),
    "vendor-elexon": ("Elexon BMRS", "Data sources", page_elexon),
    "architecture": ("Architecture", "Architecture", page_arch),
    "models": ("Models", "Models", page_models),
}

if __name__ == "__main__":
    (HERE / "static").mkdir(exist_ok=True)
    for slug, (title, cur, fn) in PAGES.items():
        dc, st = board(slug, title, cur, fn())
        body_only = dc.split('<script type="text/x-dc"')[0]
        assert "{{" not in body_only and "}}" not in body_only, f"template-hole syntax in {slug}"
        assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), f"self-closing tag in {slug}"
        (HERE / f"D-{slug}.dc.html").write_text(dc, encoding="utf-8")
        (HERE / "static" / f"D-{slug}.html").write_text(st, encoding="utf-8")
        print(slug, HEIGHTS.get(slug, 4000))
