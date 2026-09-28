"""Designer 1, "The drawer": the demo notebook opens inline in the gold stratum and pushes the deep foot down.

Every cell and output comes from <name>_analysis.ipynb, executed for real by run_cells.py on the gridflow_models
kernel. The notebook markup and CSS are the homepage's (.planning/v5/p23-homepage/gen_home.py, theme.src.css);
the gold and deep strata follow designer A (p24/A/gen_A.py, a.css). Emits 1-<name>.dc.html + static/ copies.
"""
from __future__ import annotations

import base64
import html
import json
import math
import re
import struct
import sys
from pathlib import Path

import nbformat

HERE = Path(__file__).parent
REPO = Path(r"C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end")
TOKENS = (REPO / "site" / "hifi" / "assets" / "tokens.css").read_text(encoding="utf-8")
TOKENS = re.sub(r"/\*.*?\*/", "", TOKENS[TOKENS.index(":root"):], flags=re.S)
HEIGHTS_F = HERE / "heights.json"
HEIGHTS = json.loads(HEIGHTS_F.read_text(encoding="utf-8")) if HEIGHTS_F.exists() else {}

INK, PETROL, HORIZON = "#1C2B22", "#155A6E", "#3E8C97"
T_GOLD, T_SILVER, GOLD_DEEP, SILVER_DEEP = "#E9DDAF", "#DCE2DF", "#8A6F1E", "#5E6E6B"
GH = "https://github.com/EBentham"


def f(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def smooth(pts: list[tuple[float, float]]) -> str:
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


def wave(w: int, y0: float, amp: float, seed: float, step: int = 120) -> list[tuple[float, float]]:
    return [(x, y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3))
            for x in range(-40, w + step + 41, step)]


def granite_edge(w: int, y0: float) -> list[tuple[float, float]]:
    return [(x, y0 + 9 * math.sin(x / 140 + 1) + 6 * math.sin(x / 53 + 2) + 4 * math.sin(x / 19))
            for x in range(-40, w + 41, 20)]


# ---------------------------------------------------------------- stratum textures (tiles as CSS backgrounds)
def tile(svg: str) -> str:
    return "url(\"data:image/svg+xml," + svg.replace("#", "%23").replace('"', "'") + "\")"


STIPPLE = ('<svg xmlns="http://www.w3.org/2000/svg" width="9" height="9"><g fill="#8A6F1E" opacity=".26">'
           '<circle cx="2" cy="3" r="1"/><circle cx="6.5" cy="7.5" r=".8"/></g></svg>')
DIAG = ('<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8"><path d="M0 8 L8 0" stroke="#5E6E6B" '
        'stroke-width=".8" opacity=".22"/></svg>')
GRANITE = ('<svg xmlns="http://www.w3.org/2000/svg" width="46" height="40"><path d="M8 8 h8 M12 4 v8 M30 26 h8 '
           'M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="#3E8C97" stroke-width="1.1" '
           'opacity=".5"/></svg>')

_UID = [0]


def contact_svg(w: int, kind: str) -> str:
    """A full-bleed contact strip: silver over gold ("sg") or gold over deep petrol ("gd")."""
    _UID[0] += 1
    u = _UID[0]
    h = 34
    if kind == "sg":
        line = smooth(wave(w, 17, 7, 4.0))
        top, bot, pt, pb, sw = T_SILVER, T_GOLD, f"d{u}", f"s{u}", 1.5
    else:
        line = smooth(granite_edge(w, 17))
        top, bot, pt, pb, sw = T_GOLD, PETROL, f"s{u}", f"g{u}", 2
    below = f"{line} L{w + 40} {h + 2} L-40 {h + 2} Z"
    defs = (f'<pattern id="d{u}" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" '
            f'stroke="{SILVER_DEEP}" stroke-width=".8" opacity=".22"></path></pattern>'
            f'<pattern id="s{u}" width="9" height="9" patternUnits="userSpaceOnUse"><g fill="{GOLD_DEEP}" '
            f'opacity=".26"><circle cx="2" cy="3" r="1"></circle><circle cx="6.5" cy="7.5" r=".8"></circle></g>'
            f'</pattern><pattern id="g{u}" width="46" height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 '
            f'M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" '
            f'stroke-width="1.1" opacity=".5"></path></pattern>')
    return (f'<svg class="contact" width="{w}" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="none" '
            f'aria-hidden="true"><defs>{defs}</defs>'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="{top}"></rect>'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#{pt})"></rect>'
            f'<path d="{below}" fill="{bot}"></path><path d="{below}" fill="url(#{pb})"></path>'
            f'<path d="{line}" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"></path></svg>')


# ---------------------------------------------------------------- the executed notebooks, re-rendered
KW = r"\b(from|import|as|def|return|for|in|if|else|lambda)\b"


def hl(code: str) -> str:
    """Escape, then tint keywords and string literals (the homepage's two token colours)."""
    out, pos = [], 0
    for m in re.finditer(r'"[^"\n]*"', code):
        out.append(re.sub(KW, r'<span class="k">\1</span>', html.escape(code[pos:m.start()], quote=False)))
        out.append(f'<span class="s">{html.escape(m.group(0), quote=False)}</span>')
        pos = m.end()
    out.append(re.sub(KW, r'<span class="k">\1</span>', html.escape(code[pos:], quote=False)))
    return "".join(out)


def help_card(raw: str, handle: str) -> str:
    """The real SourceClient._repr_html_ card: verbs and one-liners in its order, its discovery footer.
    The header's " · 35 datasets" count is left off, as on the homepage (middle dot; 35 disagrees with the
    33 rows list_datasets() returns)."""
    rows = re.findall(r'flex:0 0 170px[^>]*>([^<]+)</div><div[^>]*>([^<]+)</div>', raw)
    foot = re.search(r'(Discover datasets:)\s*<code[^>]*>([^<]+)</code>', raw)
    assert rows and foot, "help card shape changed"
    dl = "".join(f"<div><dt>{html.unescape(n)}</dt><dd>{html.escape(html.unescape(d), quote=False)}</dd></div>"
                 for n, d in rows)
    return (f'<div class="card"><p class="card-h">{handle}</p><dl>{dl}</dl>'
            f'<p class="card-f">{foot.group(1)} <code>{foot.group(2)}</code></p></div>')


def df_table(raw: str) -> str:
    """pandas' own to_html output, kept cell for cell, in the homepage .df markup."""
    head = re.findall(r"<th>(.*?)</th>", raw.split("</thead>")[0])
    body = raw.split("<tbody>")[1]
    rows = re.findall(r"<tr>(.*?)</tr>", body, flags=re.S)
    thead = "<tr><th></th>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>"
    trs = []
    for r in rows:
        idx = re.findall(r"<th>(.*?)</th>", r)[0]
        cells = re.findall(r"<td>(.*?)</td>", r)
        trs.append(f"<tr><th>{idx}</th>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    return f'<div class="df-wrap"><table class="df"><thead>{thead}</thead><tbody>{"".join(trs)}</tbody></table></div>'


def png_size(b: bytes) -> tuple[int, int]:
    return struct.unpack(">II", b[16:24])


def outputs(cell: nbformat.NotebookNode, alt: str) -> str:
    parts: list[str] = []
    for o in cell.outputs:
        d = o.get("data", {})
        if o.output_type == "error":
            sys.exit(f"cell {cell.execution_count} raised {o.ename}")
        if "image/png" in d:
            b = base64.b64decode(d["image/png"])
            w, h = png_size(b)
            parts.append(f'<img src="data:image/png;base64,{d["image/png"]}" width="{w}" height="{h}" '
                         f'alt="{html.escape(alt, quote=True)}">')
        elif "text/html" in d and "<table" in d["text/html"]:
            parts.append(df_table(d["text/html"]))
        elif "text/html" in d and "flex:0 0 170px" in d["text/html"]:
            parts.append(help_card(d["text/html"], cell.source.strip()))
        elif "text/plain" in d:
            parts.append(f'<pre class="txt">{html.escape(d["text/plain"], quote=False)}</pre>')
    return "".join(parts)


def notebook(spec: dict, sfx: str) -> str:
    nb = nbformat.read(HERE / f"{spec['slug']}_analysis.ipynb", as_version=4)
    rows = []
    for c in nb.cells:
        n = c.execution_count
        rows.append(f'<div class="cell"><span class="pr">[{n}]:</span><pre class="in">{hl(c.source)}</pre></div>')
        out = outputs(c, spec["plot_alt"])
        if out:
            cls = "fig" if ("<img" in out or out.startswith('<pre class="txt">')) else ""
            body = f'<div class="{cls}">{out}</div>' if cls else out
            rows.append(f'<div class="cell out"><span class="pr">[{n}]:</span>{body}</div>')
    src = "\n\n".join(c.source for c in nb.cells) + "\n"
    return (f'<figure class="nb" id="nb-{sfx}" aria-label="{html.escape(spec["nb_aria"], quote=True)}">'
            f'<div class="nb-bar"><span class="nb-tab">{spec["slug"]}_analysis.ipynb</span>'
            f'<span class="nb-kern">gridflow_models</span></div>'
            f'<div class="nb-body">{"".join(rows)}</div>'
            f'<textarea class="nb-src" id="src-{sfx}" readonly hidden aria-label="The notebook as Python">'
            f'{html.escape(src, quote=False)}</textarea></figure>')


def call_nb(spec: dict, sfx: str) -> str:
    """Designer A's workbench call, shown while the drawer is shut."""
    cells = [(1, "from gridflow_models import setup_notebook\ndata, models, common = setup_notebook()"),
             (2, spec["call"])]
    rows = "".join(f'<div class="cell"><span class="pr">[{n}]:</span><pre class="in">{hl(s)}</pre></div>'
                   for n, s in cells)
    return (f'<figure class="nb nb-call" id="call-{sfx}" aria-label="The setup cell, then {html.escape(spec["call"])}"'
            f'{" hidden" if sfx.endswith("o") else ""}><div class="nb-bar"><span class="nb-tab">{spec["slug"]}.ipynb'
            f'</span><span class="nb-kern">gridflow_models</span></div><div class="nb-body">{rows}</div></figure>')


# ---------------------------------------------------------------- page fragments
OPEN_L, SHUT_L = "Close the demo notebook", "Open the demo notebook"


def fragment(spec: dict, sfx: str, is_open: bool, w: int) -> str:
    hid = "" if is_open else " hidden"
    rel = "".join(f'<li><a href="#"><code>{k}</code></a><p>{b}</p></li>' for k, b in spec["related"])
    need = (f'Needs <a href="{GH}/gridflow">gridflow</a> and <a href="{GH}/gridflow-models">gridflow-models</a> '
            f'installed, with {spec["need"]} ingested.')
    return (f'<div class="sv" aria-hidden="true"></div>{contact_svg(w, "sg")}'
            f'<section class="st-gold" aria-labelledby="gd-{sfx}"><p class="unit" aria-hidden="true">gold, served to '
            f'the notebook</p><div class="split"><div class="lead"><h2 id="gd-{sfx}">Query it from a notebook</h2>'
            f'<p>{spec["gold_note"]}</p>'
            f'<div class="ctl"><button class="btn" type="button" aria-expanded="{str(is_open).lower()}" '
            f'aria-controls="demo-{sfx} tools-{sfx}" data-call="call-{sfx}">{OPEN_L if is_open else SHUT_L}</button>'
            f'<div class="tools" id="tools-{sfx}"{hid}><button class="btn-2" type="button" data-copy="{sfx}">'
            f'Copy notebook</button><p class="status" id="st-{sfx}" role="status"></p>'
            f'<p class="need">{need}</p></div></div></div>'
            f'<div class="nbcol">{call_nb(spec, sfx)}<div class="demo" id="demo-{sfx}"{hid}>{notebook(spec, sfx)}'
            f'</div></div></div></section>{contact_svg(w, "gd")}'
            f'<section class="st-deep" aria-labelledby="rl-{sfx}"><div class="split"><h2 id="rl-{sfx}">Related '
            f'datasets</h2><ul class="rel">{rel}</ul></div></section>')


JS = """(function () {
  var shut = "%s", open = "%s";
  function setOpen(btn, on) {
    btn.setAttribute("aria-expanded", on ? "true" : "false");
    btn.textContent = on ? open : shut;
    btn.getAttribute("aria-controls").split(" ").forEach(function (id) {
      document.getElementById(id).hidden = !on;
    });
    var call = document.getElementById(btn.getAttribute("data-call"));
    if (call) call.hidden = on;
  }
  Array.prototype.forEach.call(document.querySelectorAll("button[aria-controls]"), function (btn) {
    btn.addEventListener("click", function () { setOpen(btn, btn.getAttribute("aria-expanded") !== "true"); });
  });
  Array.prototype.forEach.call(document.querySelectorAll("button[data-copy]"), function (btn) {
    btn.addEventListener("click", function () {
      var sfx = btn.getAttribute("data-copy");
      var src = document.getElementById("src-" + sfx), status = document.getElementById("st-" + sfx);
      var code = src.value;
      function selectIt() {
        src.hidden = false;
        src.focus();
        src.select();
        var ok = false;
        try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
        if (ok) { src.hidden = true; btn.focus(); }
        status.textContent = ok ? "Copied." : "Selected. Copy it with your keyboard.";
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(function () {
          src.hidden = true;
          status.textContent = "Copied.";
        }, selectIt);
      } else {
        selectIt();
      }
    });
  });
})();""" % (SHUT_L, OPEN_L)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800'
         '&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500'
         '&amp;display=swap" rel="stylesheet">')

CSS = TOKENS + """
body{margin:0}
.root{background:var(--daylight);color:var(--ink);font:400 16px/1.6 var(--body);font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.root *,.root *::before,.root *::after{box-sizing:border-box}
.root h2,.root p,.root dl,.root dd,.root ul{margin:0}
.root h2{font-family:var(--display);font-optical-sizing:auto}
.root a{color:inherit;text-decoration-thickness:1.5px;text-underline-offset:4px;text-decoration-color:var(--olive)}
.root a:focus-visible,.root button:focus-visible,.root textarea:focus-visible{outline:2px solid var(--chartreuse);outline-offset:3px}
.root code{font-family:var(--mono);font-size:.9em}
[hidden]{display:none !important}
.state-h{padding:22px 80px 20px;font:600 17px/1.3 var(--body);color:var(--ink);background:var(--daylight);border-bottom:1px solid var(--rule-ink)}
.state + .state .state-h{border-top:1px solid var(--rule-ink)}
.sv{height:30px;background:var(--silver-tint) %(diag)s}
.contact{display:block;width:100%%;height:34px}
.st-gold{position:relative;padding:40px 80px 76px;background:var(--gold-tint) %(stip)s}
.unit{position:absolute;top:0;right:80px;font:italic 400 14px/1 var(--body);color:var(--ink)}
.split{display:grid;grid-template-columns:340px minmax(0,1fr);column-gap:60px;align-items:start}
.lead{align-self:stretch}
.lead h2{margin:0 0 12px;font-size:30px;font-weight:700;font-stretch:90%%;line-height:1.1;letter-spacing:-.012em;color:var(--ink)}
.lead p{font-size:15.5px;line-height:1.6;color:var(--ink-2)}
.lead code{color:var(--ink)}
.ctl{position:sticky;top:24px;margin-top:26px}
.btn{padding:12px 20px;border:0;border-radius:var(--radius);background:var(--chartreuse);color:var(--ink);font:600 16px/1.2 var(--body);cursor:pointer}
.btn:hover{background:var(--chartreuse-hi)}
.tools{margin-top:18px}
.btn-2{padding:10px 18px;border:1.5px solid var(--ink);border-radius:var(--radius);background:transparent;color:var(--ink);font:600 15px/1.2 var(--body);cursor:pointer}
.btn-2:hover{background:var(--daylight)}
.status{min-height:22px;margin-top:6px !important;font-size:14px;line-height:1.5;color:var(--ink)}
.need{margin-top:6px !important;font-size:14.5px;line-height:1.5;color:var(--ink-2)}
.need a{color:var(--ink)}
.nbcol{min-width:0}
/* the notebook: the homepage's markup and CSS (theme.src.css), with no completion popup below it */
.nb{background:var(--daylight);border:1.5px solid var(--ink);border-radius:4px;overflow:hidden;margin:0}
.nb-bar{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;height:40px;padding:0 18px 0 12px;background:var(--ink);font:500 13.5px/1 var(--mono)}
.nb-tab{padding:11px 18px 12px;border-radius:3px 3px 0 0;background:var(--daylight);color:var(--ink);white-space:nowrap}
.nb-kern{align-self:center;color:var(--on-petrol-2);white-space:nowrap}
.nb-body{position:relative;padding:16px 24px 10px 8px}
.cell{position:relative;display:grid;grid-template-columns:52px minmax(0,1fr);column-gap:10px;margin:0 0 9px}
.cell.out{margin:-3px 0 12px}
.pr{padding-top:12px;font:400 13px/1 var(--mono);color:var(--muted);text-align:right}
.in{margin:0;padding:8px 12px;overflow-x:auto;background:var(--topsoil);border:1px solid var(--rule-ink);border-radius:var(--radius);font:400 var(--fs-code)/1.6 var(--mono);color:var(--ink);white-space:pre}
.in .k{color:var(--petrol);font-weight:500}
.in .s{color:var(--clay-deep)}
.card{max-width:600px;overflow:hidden;background:var(--daylight);border:1px solid var(--rule-ink);border-radius:var(--radius)}
.card-h{padding:9px 14px;background:var(--topsoil);border-bottom:1px solid var(--rule-ink);font:500 15px/1.2 var(--mono);color:var(--petrol)}
.card dl{padding:7px 8px 1px}
.card dl div{display:grid;grid-template-columns:136px minmax(0,1fr);gap:14px;padding:2px 8px;border-radius:2px}
.card dl div:nth-child(odd){background:var(--zebra)}
.card dt{font:400 13.5px/1.5 var(--mono);color:var(--petrol)}
.card dd{font-size:14px;line-height:1.45;color:var(--ink)}
.card-f{margin:5px 14px 10px !important;padding-top:8px;border-top:1px solid var(--rule-ink);font-size:13.5px;color:var(--ink-2)}
.card-f code{padding:1px 5px;border-radius:2px;background:var(--topsoil);font-size:13px;color:var(--ink)}
.df-wrap{overflow-x:auto}
.df{border-collapse:collapse;margin:3px 0 0;font:400 13.5px/1 var(--body);font-variant-numeric:tabular-nums;color:var(--ink)}
.df th,.df td{padding:6px 12px;text-align:right;white-space:nowrap}
.df thead th{font-weight:600;border-bottom:1px solid var(--ink);vertical-align:bottom}
.df tbody th{font-weight:600}
.df tbody tr:nth-child(odd){background:var(--zebra)}
.fig{display:grid;row-gap:6px;justify-items:start;min-width:0}
.fig .txt{margin:0;padding-top:9px;font:400 var(--fs-code)/1.6 var(--mono);color:var(--ink);white-space:pre-wrap}
.fig img{display:block;max-width:100%%;height:auto}
.nb-src{display:block;width:calc(100%% - 24px);height:160px;margin:0 12px 12px;padding:8px 12px;border:1px solid var(--ink);border-radius:var(--radius);background:var(--daylight);color:var(--ink);font:400 13px/1.5 var(--mono);resize:vertical}
.st-deep{padding:64px 80px 92px;background:var(--petrol) %(gran)s;color:var(--on-petrol)}
.st-deep h2{font-size:30px;font-weight:700;font-stretch:90%%;line-height:1.1;letter-spacing:-.012em;color:var(--on-petrol)}
.rel{list-style:none;padding:0}
.rel li{padding:11px 0;border-top:1px solid var(--rule-petrol)}
.rel li:last-child{border-bottom:1px solid var(--rule-petrol)}
.rel a{color:var(--on-petrol);text-decoration-color:var(--chartreuse)}
.rel a code{font-size:15px}
.rel p{margin-top:3px !important;font-size:14px;line-height:1.5;color:var(--on-petrol-2)}
.rel p code{color:var(--on-petrol)}
@media (max-width: 699.98px){
  .state-h{padding:18px 16px 16px}
  .st-gold{padding:40px 16px 56px}
  .unit{right:16px}
  .split{grid-template-columns:minmax(0,1fr);row-gap:24px}
  .ctl{position:static;margin-top:20px}
  .st-deep{padding:52px 16px 72px}
  .st-deep .split{row-gap:14px}
  .nb-bar{padding:0 10px 0 6px}
  .nb-tab{padding-inline:12px}
  .nb-body{padding:12px 10px 8px 2px}
  .cell{grid-template-columns:36px minmax(0,1fr);column-gap:8px}
  .card dl div{grid-template-columns:minmax(0,1fr);gap:0;padding-block:4px}
}
""" % {"diag": tile(DIAG), "stip": tile(STIPPLE), "gran": tile(GRANITE)}

SPECS = [
    {
        "slug": "fuelhh", "title": "Generation by fuel type",
        "call": 'df = data.elexon.query("fuelhh", "2026-09-20", "2026-09-26")',
        "gold_note": ("Returns a pandas DataFrame from the DuckDB relation <code>silver_elexon_fuelhh</code>, filtered "
                      "on <code>settlement_date</code> with both ends included. Lineage columns are dropped."),
        "need": "20 to 26 September 2026",
        "plot_alt": ("Line plot of WIND generation_mw against timestamp_utc, 20 to 26 September 2026: about 16,000 MW "
                     "at the start, falling to about 1,400 MW late on the 22nd, peaks near 10,500 and 11,700 MW on "
                     "the 23rd and 25th, about 7,000 MW at the end."),
        "nb_aria": ("A demo notebook on the gridflow_models kernel: setup, the data.elexon help card, the fuelhh query "
                    "for 20 to 26 September 2026, the first five rows, and a plot of WIND generation."),
        "related": [
            ("elexon/fuelinst", "Instantaneous outturn by fuel type, from the same connector"),
            ("neso_data_portal/historic_generation_mix", "Where solar outturn lives"),
            ("elexon/bmunits_reference", "Shares the fuel-type codes"),
            ("elexon/indo", "Demand, used to check the interconnector sign"),
        ],
    },
    {
        "slug": "bmunits_reference", "title": "Balancing Mechanism units",
        "call": 'df = data.sql("SELECT * FROM silver_elexon_bmunits_reference ORDER BY bm_unit_id")',
        "gold_note": ("A register with no time axis: a <code>query()</code> date range filters it on "
                      "<code>ingested_at</code>, so read the whole table with <code>data.sql()</code>."),
        "need": "the BM unit register",
        "plot_alt": "",
        "nb_aria": ("A demo notebook on the gridflow_models kernel: setup, the data.elexon help card, the whole BM unit "
                    "register read with data.sql, the first five rows, and a count of units by fuel_type."),
        "related": [
            ("elexon/boal", "Bid-offer acceptances, joined on <code>bm_unit_id</code>"),
            ("elexon/pn", "Physical notifications, joined on <code>bm_unit_id</code>"),
            ("elexon/uou2t14d", "Availability per unit"),
            ("elexon/fuelhh", "Shares the fuel-type codes; interconnector flow lives there"),
        ],
    },
]


def board(spec: dict, w: int, states: list[tuple[str, bool, str]]) -> tuple[str, str]:
    name = f"1-{spec['slug'].replace('_', '-')}" + ("-390" if w < 700 else "")
    body = "".join(f'<section class="state" aria-label="{html.escape(lab, quote=True)}"><p class="state-h">{lab}</p>'
                   f'{fragment(spec, sfx, op, w)}</section>' for lab, op, sfx in states)
    hgt = HEIGHTS.get(name, 3000)
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{spec["title"]}: demo notebook</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{CSS}</style>
</helmet>
<div class="root" style="width: {w}px; height: {hgt}px; overflow: hidden; position: relative">
<main>
{body}
</main>
<script>
{JS}
</script>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{hgt}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""
    return name, out


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>\n', "")
    s = re.sub(r"</?x-dc>\n?", "", s)
    s = re.sub(r"</?helmet>\n?", "", s)
    s = re.sub(r'<script type="text/x-dc".*?</script>\n', "", s, flags=re.S)
    return s


if __name__ == "__main__":
    (HERE / "static").mkdir(exist_ok=True)
    jobs = [(SPECS[0], 1440, [("Closed, as the page loads", False, "c"), ("Open, after pressing the button", True, "o")]),
            (SPECS[1], 1440, [("Closed, as the page loads", False, "c"), ("Open, after pressing the button", True, "o")]),
            (SPECS[0], 390, [("Open, on a phone", True, "o")])]
    for spec, w, states in jobs:
        name, out = board(spec, w, states)
        assert "#A9C7C4" not in out.upper() and "\u2014" not in out and "\u00b7" not in out and "\u2192" not in out
        (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
        (HERE / "static" / f"{name}.html").write_text(static(out), encoding="utf-8")
        print(name, len(out))
