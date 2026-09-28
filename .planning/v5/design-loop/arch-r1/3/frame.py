"""Designer 3, architecture round 1: the shared frame (adapted from p27-r1/A/frame.py, direction A "Sections").

Text is laid out in flow (sections, CSS grid). Only SVG layers are absolute: the strata background and the plate's
drawing. Two passes: pass 1 renders the page with a probe script, headless Chrome reports the rects of every section
(``data-st``) and every keyed-index title (``data-t``); pass 2 draws the strata, parts and leaders to those numbers.
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
MEAS_F = HERE / "measure.json"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9713
W = 1440

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, CLAY, KHAKI, MUTED = "#1C2B22", "#F6F4EC", "#C77E3C", "#A39A6A", "#5d6a55"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_BRONZE, T_TOP = "#E9DDAF", "#DCE2DF", "#E2CDB3", "#ECE8DA"
SOFT = "#3F4A3B"
ONP, ONP2, ONP3 = "#F6F4EC", "#CFE0DC", "#B4D0CD"
TINT = {"bronze": T_BRONZE, "silver": T_SILVER, "gold": T_GOLD}

NAV = ["Home", "Data sources", "Architecture", "Models", "About"]

BASE_CSS = """body{margin:0}
.root{background:#155A6E;color:#1C2B22;font:400 16px/1.6 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.root a{color:inherit;text-decoration-thickness:1.5px;text-underline-offset:4px;text-decoration-color:#66793B}
.root a:focus-visible{outline:2px solid #AFC64E;outline-offset:3px;border-radius:2px}
.root h1,.root h2,.root h3{font-family:"Bricolage Grotesque",sans-serif;margin:0;font-optical-sizing:auto}
.root code{font-family:"Red Hat Mono",monospace;font-size:.9em}
.layer{position:absolute;left:0;top:0}
main{position:relative;display:block}
.mast{display:flex;justify-content:space-between;align-items:baseline;padding-top:26px;color:#F6F4EC;line-height:1.6}
.brand{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:24px;letter-spacing:-.01em}
.root .brand{text-decoration:none}
.mast ul{display:flex;gap:30px;list-style:none;margin:0;padding:0;font-size:15px}
.mast ul a{text-decoration:none;color:#CFE0DC}
.mast ul a:hover{color:#F6F4EC}
.mast ul a[aria-current="page"]{color:#F6F4EC;box-shadow:inset 0 -2px 0 #AFC64E}
.st{position:relative;box-sizing:border-box;padding:0 80px}
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


def footer() -> str:
    links = "".join(f'<li><a href="#">{n}</a></li>' for n in ["Data sources", "Architecture", "Models", "About",
                                                               "GitHub"])
    return (f'<footer class="st st-deep"><div class="foot"><a class="brand" href="#">gridflow</a>'
            f'<ul>{links}</ul><p>This site is MIT-licensed. gridflow is Apache-2.0.</p></div></footer>')


# ---------------------------------------------------------------- strata
SEEDS = {"bronze": (7, .4), "silver": (8, 2.1), "gold": (7, 4.0)}
PAT = {"bronze": ("p-brick", ".15"), "silver": ("p-diag", ".22"), "gold": ("p-stip", ".26")}


def contact_pts(name: str, y0: float) -> list[tuple[float, float]]:
    amp, seed = SEEDS[name]
    return hp.wave(y0, amp, seed)


def contact_y(name: str, y0: float, x: float) -> float:
    amp, seed = SEEDS[name]
    return y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3)


def rough(y0: float) -> list[tuple[float, float]]:
    return [(x, y0 + 9 * math.sin(x / 140 + 1) + 6 * math.sin(x / 53 + 2) + 4 * math.sin(x / 19))
            for x in range(-40, W + 41, 20)]


def strata_svg(H: int, sky: float, surf: list[tuple[float, float]], contacts: list[tuple[str, float]]) -> str:
    """The section behind the page: petrol sky, the cut, then each named band from its contact down."""
    surf_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    root = surf_d + " " + " ".join(f"L{f(x)} {f(y + 9)}" for x, y in reversed(surf)) + " Z"
    tail = f" L{W + 40} {H + 10} L-40 {H + 10} Z"
    out = [f'<rect x="0" y="0" width="{W}" height="{f(sky + 80)}" fill="{PETROL}"></rect>',
           f'<path d="{surf_d}{tail}" fill="{T_TOP}"></path>',
           f'<path d="{surf_d}{tail}" fill="url(#p-soil)" opacity=".5"></path>']
    lines, deep = [], None
    for name, y in contacts:
        if name == "deep":
            deep = rough(y)
            continue
        d = smooth(contact_pts(name, y))
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
        out.append(f'<path d="{smooth(deep)}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round">'
                   f'</path>')
    return (f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">'
            f'<defs>{PATTERNS}</defs>' + "\n".join(out) + "</svg>")


def cable(d: str, core: str = BRONZE, sheath: float = 4.4, corew: float = 1.5) -> str:
    return hp.cable(d, core, sheath, corew)


def terminal(x: float, y: float, tint: str = T_BRONZE, r: float = 6.5) -> str:
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{tint}" stroke="{INK}" stroke-width="2"></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r / 3)}" fill="{INK}"></circle>')


def joint(x: float, y: float, r: float = 4.6) -> str:
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{INK}"></circle>'


def sleeve(x: float, y: float, fill: str) -> str:
    """A splice sleeve where a cable crosses a contact: the core changes colour here."""
    return (f'<rect x="{f(x - 7)}" y="{f(y - 17)}" width="14" height="34" rx="7" fill="{fill}" stroke="{INK}" '
            f'stroke-width="1.6"></rect><path d="M{f(x - 7)} {f(y - 8)} H{f(x + 7)} M{f(x - 7)} {f(y + 8)} '
            f'H{f(x + 7)}" stroke="{INK}" stroke-width="1" opacity=".5"></path>')


def drop(x0: float, y0: float, x1: float, y1: float, ya: float, yb: float, step: float = 6) -> str:
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


# ---------------------------------------------------------------- page shell + measurement
PROBE = """<pre id="m"></pre><script>
window.addEventListener('load',function(){Promise.all(['760 86px "Bricolage Grotesque"','720 42px "Bricolage Grotesque"','700 30px "Bricolage Grotesque"','400 16px "Hanken Grotesk"','600 16px "Hanken Grotesk"','italic 400 14px "Hanken Grotesk"','400 14px "Red Hat Mono"','500 14px "Red Hat Mono"'].map(function(q){return document.fonts.load(q)})).then(function(){return document.fonts.ready}).then(function(){setTimeout(function(){
var root=document.querySelector('.root').getBoundingClientRect(),o={secs:{},t:{},H:0};
document.querySelectorAll('[data-st]').forEach(function(s){var r=s.getBoundingClientRect();o.secs[s.dataset.st]=[r.top-root.top,r.height];});
document.querySelectorAll('[data-t]').forEach(function(e){var r=e.getBoundingClientRect();o.t[e.dataset.t]=[r.left-root.left,r.top-root.top,r.right-root.left,r.bottom-root.top];});
o.H=document.querySelector('main').getBoundingClientRect().bottom-root.top;
o.fonts=Array.from(document.fonts).filter(function(x){return x.status==='loaded'}).map(function(x){return x.family+' '+x.weight+' '+x.style}).join('|');
var over=[];document.querySelectorAll('main p,main li,main h1,main h2,main h3,main dd,main dt,main pre,main figcaption,main code,main td,main th').forEach(function(e){var cs=getComputedStyle(e);if(e.scrollWidth>e.clientWidth+1&&cs.overflow!=='visible'&&cs.overflowX!=='auto')over.push((e.className||e.tagName)+':'+e.textContent.slice(0,30));var r=e.getBoundingClientRect();if(r.right-root.left>1362&&!e.closest('.mast'))over.push('WIDE '+(e.className||e.tagName)+':'+Math.round(r.right-root.left)+':'+e.textContent.slice(0,30));});
var scr=[];document.querySelectorAll('pre,.scroll').forEach(function(e){if(e.scrollWidth>e.clientWidth+1)scr.push((e.className||e.tagName)+':'+(e.scrollWidth-e.clientWidth)+':'+e.textContent.slice(0,40));});
o.over=over;o.scroll=scr;
document.getElementById('m').textContent=JSON.stringify(o);},500);});});
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
                          "--virtual-time-budget=9000", "--dump-dom",
                          f"http://127.0.0.1:{PORT}/static/_m_{name}.html?v={time.time_ns()}"],
                         capture_output=True, text=True, encoding="utf-8", timeout=120)
    m = re.search(r'<pre id="m">(.*?)</pre>', out.stdout, re.S)
    if not m or not m.group(1).strip():
        raise RuntimeError(f"probe failed for {name}: {out.stderr[-400:]}")
    data = json.loads(m.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                      .replace("&quot;", '"'))
    p.unlink()
    return data


def check(out: str) -> None:
    body_only = out.split('<script type="text/x-dc"')[0]
    assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
    assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), "self-closing tag"
    assert "#A9C7C4" not in out.upper(), "banned colour"
    for ch, why in (("\u2014", "em dash"), ("\u2013", "en dash"), ("\u2192", "arrow"), ("\u00b7", "middle dot")):
        assert ch not in body_only, why
