"""Designer A, "Sections": the shared frame for the four top pages.

Text is laid out in flow (sections, CSS grid). Only SVG layers are absolute: the strata background, the landscape
in the sky, the cables. Two passes: pass 1 renders each page with a probe script, headless Chrome reports the rects
of every section and cable terminal (``data-t``), and pass 2 draws the strata and cables to those numbers.
Drawing pieces come from the locked homepage generator (``hp.py`` is a copy of r3-7/gen_a.py with its two data
loads removed).
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import time
from pathlib import Path

import hp
from hp import f, smooth

HERE = Path(__file__).parent
PACK = json.loads((HERE.parent / "pack" / "toppages.json").read_text(encoding="utf-8"))
MEAS_F = HERE / "measure.json"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9617
W = 1440

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, CLAY, KHAKI, MUTED = "#1C2B22", "#F6F4EC", "#C77E3C", "#A39A6A", "#5d6a55"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_BRONZE, T_TOP = "#E9DDAF", "#DCE2DF", "#E2CDB3", "#ECE8DA"
SOFT = "#3F4A3B"
TINT = {"bronze": T_BRONZE, "silver": T_SILVER, "gold": T_GOLD}
CORE = {"bronze": BRONZE, "silver": SILVER, "gold": GOLD}

NAV = ["Home", "Data sources", "Architecture", "Models", "About"]

# every line of copy a page adds (not taken verbatim from the pack) is registered here for the notes
COPY: dict[str, list[str]] = {}


def T(page: str, s: str) -> str:
    COPY.setdefault(page, []).append(s)
    return s


# ---------------------------------------------------------------- CSS
BASE_CSS = """body{margin:0}
.root{background:#155A6E;color:#1C2B22;font:400 16px/1.6 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.root a{color:inherit;text-decoration-thickness:1.5px;text-underline-offset:4px;text-decoration-color:#66793B}
.root a:focus-visible{outline:2px solid #AFC64E;outline-offset:3px;border-radius:2px}
.root h1,.root h2,.root h3{font-family:"Bricolage Grotesque",sans-serif;margin:0;font-optical-sizing:auto}
.root code{font-family:"Red Hat Mono",monospace;font-size:.9em}
.layer{position:absolute;left:0;top:0}
main{position:relative;display:block}
.st{position:relative;box-sizing:border-box;padding:0 80px}
.sky{position:relative;box-sizing:border-box;padding:0 80px}
.mast{display:flex;justify-content:space-between;align-items:baseline;padding-top:26px;color:#F6F4EC;line-height:1.6}
.brand{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:24px;letter-spacing:-.01em}
.root .brand{text-decoration:none}
.mast ul{display:flex;gap:30px;list-style:none;margin:0;padding:0;font-size:15px}
.mast ul a{text-decoration:none;color:#CFE0DC}
.mast ul a:hover{color:#F6F4EC}
.mast ul a[aria-current="page"]{color:#F6F4EC;box-shadow:inset 0 -2px 0 #AFC64E}
.hero{display:grid;grid-template-columns:860px 374px;column-gap:46px;margin-top:64px;align-items:start}
.hero h1{color:#F6F4EC;font-weight:760;font-stretch:84%;font-size:86px;line-height:.94;letter-spacing:-.022em}
.crumb{margin:0 0 18px;font-size:15px;line-height:1.4;color:#B4D0CD}
.crumb a{color:#CFE0DC;text-decoration-color:#AFC64E}
.lede{padding-top:14px}
.lede p{margin:0 0 14px;font-size:17.5px;line-height:1.6;color:#CFE0DC;max-width:58ch}
.lede p.lead{color:#F6F4EC}
.lede .n{color:#F6F4EC;font-weight:600}
.lede code{color:#F6F4EC;font-size:.86em}
.alt{font-weight:600;color:#F6F4EC;text-decoration-color:#AFC64E}
.root .alt{text-decoration-color:#AFC64E}
.facts{margin:4px 0 0}
.facts div{display:grid;grid-template-columns:96px minmax(0,1fr);column-gap:14px;padding:7px 0;border-top:1px solid rgba(207,224,220,.22)}
.facts dt{font-size:14px;line-height:1.45;color:#B4D0CD}
.facts dd{margin:0;font-size:14.5px;line-height:1.45;color:#F6F4EC}
.facts code{font-size:13.5px}
.land-svg text,.lab text{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:13.5px}
.sec h2,.st h2.big{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0 0 16px}
.st h2.fig-h{font-size:30px;font-weight:700;font-stretch:90%;line-height:1.1;letter-spacing:-.012em;margin:0 0 8px}
.sec p,.st p.body{margin:0 0 14px;font-size:16px;line-height:1.62;color:#3F4A3B;max-width:58ch}
.st p code,.st li code,.st dd code{color:#1C2B22}
.cap{margin:8px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:66ch}
.more{font-weight:600;color:#1C2B22}
.chart{display:block;overflow:visible}
.chart text{font-family:"Hanken Grotesk",sans-serif;font-size:13px;fill:#3F4A3B}
.chart text.dl{font-style:italic;font-size:13.5px;fill:#1C2B22}
.well{margin:0;background:#ECE8DA;border:1px solid rgba(28,43,34,.18);border-radius:3px;padding:10px 14px;font:400 14.5px/1.7 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre;overflow:hidden}
.well .s{color:#7C5530}
.well .k{color:#155A6E;font-weight:500}
.well .c{color:#5d6a55}
.st-deep{color:#F6F4EC}
.foot{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:baseline;column-gap:40px;padding:44px 0 56px;border-top:1px solid rgba(207,224,220,.22)}
.foot ul{display:flex;gap:28px;list-style:none;margin:0;padding:0;font-size:15px}
.foot ul a{color:#CFE0DC;text-decoration:none}
.foot ul a:hover{color:#F6F4EC;text-decoration:underline;text-decoration-color:#AFC64E}
.foot p{grid-column:1 / -1;margin:14px 0 0;font-size:14px;color:#B4D0CD}
.rot{transform-box:fill-box;transform-origin:center;animation:spin 17s linear infinite}
.sp2{animation-duration:13s}
.sp3{animation-duration:21s}
@keyframes spin{to{transform:rotate(360deg)} }
@media (prefers-reduced-motion: reduce){.rot{animation:none} }
"""

FONTS = hp.FONTS
PATTERNS = hp.PATTERNS


def masthead(current: str) -> str:
    li = "".join(f'<li><a href="#"{" aria-current=\"page\"" if n == current else ""}>{n}</a></li>' for n in NAV)
    return (f'<header class="mast"><a class="brand" href="#">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{li}</ul></nav></header>')


def footer(page: str) -> str:
    links = "".join(f'<li><a href="#">{n}</a></li>' for n in ["Data sources", "Architecture", "Models", "About",
                                                               "GitHub"])
    return (f'<footer class="st st-deep" data-st="deep"><div class="foot"><a class="brand" href="#">gridflow</a>'
            f'<ul>{links}</ul><p>{T(page, "This site is MIT-licensed. gridflow is Apache-2.0.")}</p></div></footer>')


# ---------------------------------------------------------------- strata
def contact(y0: float, amp: float, seed: float) -> list[tuple[float, float]]:
    return hp.wave(y0, amp, seed)


def rough(y0: float) -> list[tuple[float, float]]:
    return [(x, y0 + 9 * math.sin(x / 140 + 1) + 6 * math.sin(x / 53 + 2) + 4 * math.sin(x / 19))
            for x in range(-40, W + 41, 20)]


SEEDS = {"bronze": (7, .4), "silver": (8, 2.1), "gold": (7, 4.0)}
PAT = {"bronze": ("p-brick", ".15"), "silver": ("p-diag", ".22"), "gold": ("p-stip", ".26")}


def strata_svg(H: int, sky: float, surf: list[tuple[float, float]], contacts: list[tuple[str, float]],
               beds: list[float] | None = None, labels: bool = True, top_fill: str = T_TOP) -> str:
    """The section behind the page: petrol sky, the cut, then each named band from its contact down."""
    surf_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    root = surf_d + " " + " ".join(f"L{f(x)} {f(y + 9)}" for x, y in reversed(surf)) + " Z"
    tail = f" L{W + 40} {H + 10} L-40 {H + 10} Z"
    out = [f'<rect x="0" y="0" width="{W}" height="{f(sky + 60)}" fill="{PETROL}"></rect>',
           f'<path d="{surf_d}{tail}" fill="{top_fill}"></path>',
           f'<path d="{surf_d}{tail}" fill="url(#p-soil)" opacity=".5"></path>']
    lines, deep = [], None
    for name, y in contacts:
        if name == "deep":
            deep = rough(y)
            continue
        amp, seed = SEEDS[name]
        pts = contact(y, amp, seed)
        d = smooth(pts)
        pid, op = PAT[name]
        out.append(f'<path d="{d}{tail}" fill="{TINT[name]}"></path><path d="{d}{tail}" fill="url(#{pid})" '
                   f'opacity="{op}"></path>')
        lines.append(d)
    if deep:
        gd = smooth(deep)
        out.append(f'<path d="{gd}{tail}" fill="{PETROL}"></path>'
                   f'<path d="{gd}{tail}" fill="url(#p-granite)" opacity=".5"></path>')
    out.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    out.append(f'<path d="{surf_d}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    if lines:
        out.append(f'<path d="{" ".join(lines)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    if deep:
        out.append(f'<path d="{smooth(deep)}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path>')
    for yb in beds or []:
        out.append(f'<path d="{smooth(hp.wave(yb, 4, yb / 97, 160))}" stroke="{INK}" stroke-width="1" '
                   f'stroke-dasharray="2 6" fill="none" opacity=".55"></path>')
    if labels:
        lab = "".join(f'<text x="1360" y="{f(y + 30)}" text-anchor="end">{n}</text>'
                      for n, y in contacts if n != "deep")
        out.append(f'<g font-family="Hanken Grotesk" font-style="italic" font-size="14" fill="{INK}">{lab}</g>')
    return (f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">'
            f'<defs>{PATTERNS}</defs>' + "\n".join(out) + "</svg>")


def cable(d: str, core: str = BRONZE, sheath: float = 4.4, corew: float = 1.5) -> str:
    return hp.cable(d, core, sheath, corew)


def terminal(x: float, y: float, tint: str = T_BRONZE, r: float = 6.5) -> str:
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{tint}" stroke="{INK}" stroke-width="2"></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r / 3)}" fill="{INK}"></circle>')


def joint(x: float, y: float) -> str:
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="4.6" fill="{INK}"></circle>'


def sleeve(x: float, y: float, fill: str, vertical: bool = True) -> str:
    """A splice sleeve where a cable crosses a contact: the core changes colour here."""
    if vertical:
        return (f'<rect x="{f(x - 7)}" y="{f(y - 17)}" width="14" height="34" rx="7" fill="{fill}" stroke="{INK}" '
                f'stroke-width="1.6"></rect><path d="M{f(x - 7)} {f(y - 8)} H{f(x + 7)} M{f(x - 7)} {f(y + 8)} '
                f'H{f(x + 7)}" stroke="{INK}" stroke-width="1" opacity=".5"></path>')
    return (f'<rect x="{f(x - 17)}" y="{f(y - 7)}" width="34" height="14" rx="7" fill="{fill}" stroke="{INK}" '
            f'stroke-width="1.6"></rect>')


def drop(x0: float, y0: float, x1: float, y1: float, ya: float, yb: float, step: float = 8) -> str:
    """A buried cable: straight down from (x0, y0), an S-bend between ya and yb onto x1, straight down to y1."""
    pts = [(x0, y0), (x0, ya)]
    y = ya + step
    while y < yb:
        t = (y - ya) / (yb - ya)
        s = t * t * (3 - 2 * t)
        pts.append((x0 + (x1 - x0) * s, y))
        y += step
    pts.append((x1, yb))
    return smooth(pts) + f" V{f(y1)}"


def contact_y(name: str, y0: float, x: float) -> float:
    amp, seed = SEEDS[name]
    return y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3)


# ---------------------------------------------------------------- charts
def ticks_text(items: list[tuple[float, float, str]], anchor: str = "middle") -> str:
    return "".join(f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}">{s}</text>' for x, y, s in items)


def fmt(v: float) -> str:
    return f"{v:,.0f}"


# ---------------------------------------------------------------- page shell + measurement
PROBE = """<pre id="m"></pre><script>
window.addEventListener('load',function(){Promise.all(['760 86px "Bricolage Grotesque"','720 42px "Bricolage Grotesque"','400 16px "Hanken Grotesk"','600 16px "Hanken Grotesk"','italic 400 14px "Hanken Grotesk"','400 14px "Red Hat Mono"','500 14px "Red Hat Mono"'].map(function(q){return document.fonts.load(q)})).then(function(){return document.fonts.ready}).then(function(){setTimeout(function(){
var root=document.querySelector('.root').getBoundingClientRect(),o={secs:{},t:{},H:0};
document.querySelectorAll('[data-st]').forEach(function(s){var r=s.getBoundingClientRect();o.secs[s.dataset.st]=[r.top-root.top,r.height];});
document.querySelectorAll('[data-t]').forEach(function(e){var r=e.getBoundingClientRect();o.t[e.dataset.t]=[r.left-root.left,r.top-root.top,r.right-root.left,r.bottom-root.top];});
o.H=document.querySelector('main').getBoundingClientRect().bottom-root.top;
o.fonts=Array.from(document.fonts).filter(function(x){return x.status==='loaded'}).map(function(x){return x.family+' '+x.weight+' '+x.style}).join('|');
var over=[];document.querySelectorAll('main p,main li,main h1,main h2,main h3,main dd,main dt,main pre,main figcaption,main code').forEach(function(e){if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='visible')over.push((e.className||e.tagName)+':'+e.textContent.slice(0,30));var r=e.getBoundingClientRect();if(r.right-root.left>1362&&!e.closest('.mast'))over.push('WIDE '+(e.className||e.tagName)+':'+Math.round(r.right-root.left)+':'+e.textContent.slice(0,30));});
o.over=over;
document.getElementById('m').textContent=JSON.stringify(o);},400);});});
</script>"""


def shell(title: str, css: str, body: str, H: int, probe: bool = False) -> str:
    return f"""<!doctype html>
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
{FONTS}
<style>
{BASE_CSS}{css}</style>
</helmet>
<div class="root" style="width: {W}px; height: {H}px; overflow: hidden; position: relative">
{body}
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


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    s = re.sub(r"<script type=\"text/x-dc\".*?</script>\n", "", s, flags=re.S)
    return s


def measure(name: str, html_text: str) -> dict:
    p = HERE / "static" / f"_m_{name}.html"
    p.write_text(static(html_text), encoding="utf-8")
    out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--window-size=1440,4000",
                          "--virtual-time-budget=9000", "--dump-dom", f"http://127.0.0.1:{PORT}/_m_{name}.html?v={time.time_ns()}"],
                         capture_output=True, text=True, encoding="utf-8", timeout=120)
    m = re.search(r'<pre id="m">(.*?)</pre>', out.stdout, re.S)
    if not m or not m.group(1).strip():
        raise RuntimeError(f"probe failed for {name}: {out.stderr[-400:]}")
    data = json.loads(m.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
    p.unlink()
    return data


def check(out: str) -> None:
    body_only = out.split('<script type="text/x-dc"')[0]
    assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
    assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), "self-closing tag"
    assert "#A9C7C4" not in out.upper(), "banned colour"
    assert "\u2014" not in body_only, "em dash"
    assert "\u2192" not in body_only, "arrow"
