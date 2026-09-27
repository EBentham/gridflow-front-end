"""Designer 3, "The engineering plate": the Architecture page.

The drawing is an annotated plate: the eight sources stand above ground, their cables run down through bronze and
silver into gold, and the readers hang at the foot. Every part carries a hairline leader to a keyed index column
whose entries sit level with it (the sources fan in from the landscape). The row's journey is one notebook whose
cells run the pack's real snippets beside their real outputs; the correctness rules are a spec sheet in the deep.
Every fact, label and snippet comes from ../../arch-pack (ARCH-PACK.md, pack.json, snippets/).
"""
from __future__ import annotations

import html
import json
import math
import re

import hp
import scenery as sn
from frame import (BRONZE, CHART, CLAY, DAY, GOLD, HERE, HORIZON, INK, KHAKI, OLIVE, ONP, ONP3, PETROL, SILVER,
                   SOFT, T_BRONZE, T_GOLD, T_SILVER, cable, contact_pts, contact_y, drop, f, footer, joint, masthead,
                   rough, sleeve, smooth, strata_svg, terminal)

NAME = "arch-3"
TITLE = "Architecture, engineering plate"
PACKD = HERE.parent.parent / "arch-pack"
PACK = json.loads((PACKD / "pack.json").read_text(encoding="utf-8"))
SEC = {s["id"]: s for s in PACK["sections"]}
PARTS = {p["id"]: p for p in SEC["drawing"]["parts"]}
STOPS = [s for s in SEC["journey"]["stops"]]


def snip(n: str) -> str:
    return (PACKD / "snippets" / n).read_text(encoding="utf-8").rstrip("\n")


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def short(path: str) -> str:
    """Link text for a repo file: the package-relative path (src/gridflow/x.py shows as x.py under gridflow)."""
    if path.startswith("src/gridflow_models/"):
        return path[len("src/"):]
    if path.startswith("src/gridflow/"):
        return path[len("src/gridflow/"):] + ("/" if path.endswith("views") else "")
    return path


def links(part_links: list[dict], models_page: bool = False) -> str:
    out = []
    for lk in part_links:
        if lk.get("file") == "site page":
            continue
        out.append(f'<a href="{lk["url"]}"><code>{short(lk["file"])}</code></a>')
    if models_page:
        out.append('<a class="pg" href="models.html">Models page</a>')
    return ", ".join(out)


# ================================================================ code highlighting
PY_KW = r"\b(from|import|with|as)\b"
SQL_KW = (r"\b(CREATE OR REPLACE VIEW|CREATE TABLE IF NOT EXISTS|SELECT|FROM|WHERE|AND|ORDER BY|QUALIFY|OVER|"
          r"PARTITION BY|DESC|NULLS LAST|CASE|WHEN|THEN|ELSE|END|AS|DATE|TIMESTAMPTZ|ROW_NUMBER|row_number|"
          r"PRIMARY KEY|NOT NULL|DEFAULT|VARCHAR|INTEGER|FLOAT|TIMESTAMP WITH TIME ZONE)\b")


def hl(code: str, lang: str) -> str:
    if lang == "py":
        tok, kw = r'"[^"\n]*"|#[^\n]*', PY_KW
    elif lang == "sql":
        tok, kw = r"'[^'\n]*'", SQL_KW
    elif lang == "json":
        tok, kw = r'"[^"\n]*"(?=\s*:)', None
    else:
        tok, kw = r"--[a-z]+", r"^(gridflow)\b"
    out, pos = [], 0

    def plain(s: str) -> str:
        e = esc(s)
        if kw:
            e = re.sub(kw, r'<span class="kw">\1</span>', e, flags=re.M)
        return e

    for m in re.finditer(tok, code):
        out.append(plain(code[pos:m.start()]))
        g = m.group(0)
        cls = "cm" if g.startswith("#") else ("opt" if g.startswith("--") else ("key" if lang == "json" else "str"))
        out.append(f'<span class="{cls}">{esc(g)}</span>')
        pos = m.end()
    out.append(plain(code[pos:]))
    return "".join(out)


# ================================================================ opening
def opening() -> str:
    op = SEC["opening"]
    return (f'<section class="st op" data-section="opening" data-st="opening" aria-labelledby="h1">'
            f'{masthead("Architecture")}'
            f'<h1 id="h1">How gridflow is built</h1>'
            f'<div class="op-grid"><p class="lead">{esc(op["lede"])}</p>'
            f'<p class="scope">{esc(op["scope"])}</p></div></section>')


# ================================================================ the plate: parts, index, drawing
# above ground, left to right as drawn: the continent's gas and power, then GB weather, wind and the grid
SRC = ["gie_alsi", "gie_agsi", "entsog", "entsoe", "open_meteo", "neso_data_portal", "neso", "elexon"]
LANES = [140, 236, 332, 428, 524, 620, 716, 830]       # underground lane of each source cable, same order
IX = 900                                               # the index column's left edge (its marks start here)
LX = IX - 7                                            # where a leader meets its mark

BELOW = [  # (index key, pack part id, group)
    ("k-conn", "boundary-vendor-connector", "top"),
    ("k-raw", "boundary-connector-bronze", "bronze"),
    ("k-bronze", "stratum-bronze", "bronze"),
    ("k-tr", "boundary-bronze-silver", "silver"),
    ("k-silver", "stratum-silver", "silver"),
    ("k-gold", "stratum-gold", "gold"),
    ("k-views", "boundary-silver-views", "gold"),
    ("k-db", "catalogue", "gold"),
    ("k-cli", "reader-cli", "gold"),
    ("k-client", "reader-client", "gold"),
    ("k-nb", "reader-notebooks", "gold"),
    ("k-models", "reader-gridflow-models", "gold"),
]
MONO_WORDS = ["gridflow quality", "available_at", "source_run_id", "dataset_version", "_latest", "read_parquet", ".meta.json",
              "pipeline_runs", "pipeline_watermarks", "quality_reports", "system_marginal_price",
              "gold_uk_imbalance_context", "gold_gb_day_ahead_benchmark", "gold_eu_gas_storage", "GridflowClient",
              "gridflow_models", "httpx", "_run{capture time}", "gridflow.duckdb"]
VERBS = ["init", "ingest", "transform", "build", "pipeline", "backfill", "export-csv", "status", "quality", "reset",
         "prune"]


def monoize(s: str) -> str:
    """Set column names, file and table names in Red Hat Mono; everything else stays Hanken."""
    e = esc(s)
    if e.startswith("bronze/{") or e.startswith("silver/{"):
        head, _, rest = e.partition(";") if ";" in e else e.partition(",")
        sep = ";" if ";" in e else ","
        return f"<code>{head}</code>{sep}{mono_words(rest)}"
    if e.startswith("from gridflow.serving.client import GridflowClient:"):
        head, _, rest = e.partition(":")
        meths = re.sub(r"\b(query|get_system_prices|get_imbalance_context|get_gas_storage)\b", r"<code>\1</code>",
                       rest)
        return f"<code>{head}</code>:{meths}"
    if e.rstrip(".").split(", ") == VERBS:
        return ", ".join(f"<code>{v}</code>" for v in VERBS) + "."
    return mono_words(e)


def mono_words(e: str) -> str:
    for w in sorted(MONO_WORDS, key=len, reverse=True):
        e = re.sub(rf"(?<![\w>{{/.]){re.escape(w)}(?![\w<])", f"<code>{w}</code>", e)
    return e


def mark(kind: str) -> str:
    """A small mark copied from the drawing part an index entry names (26 x 26)."""
    s = '<svg class="mk" width="26" height="26" viewBox="{vb}" aria-hidden="true">{b}</svg>'
    if kind.startswith("src-"):
        body, vb = asset(kind[4:], mini=True)
        x, y, w, h = (float(v) for v in vb.split())
        side = max(w, h) + 6
        x, y = x - (side - w) / 2, y - (side - h) + 3
        cut = (f'<rect x="{f(x)}" y="{f(y)}" width="{f(side)}" height="{f(side)}" fill="{CHART}"></rect>'
               f'<rect x="{f(x)}" y="100" width="{f(side)}" height="{f(y + side - 100)}" fill="{OLIVE}"></rect>')
        edge = (f'<rect x="{f(x)}" y="{f(y)}" width="{f(side)}" height="{f(side)}" fill="none" stroke="{INK}" '
                f'stroke-width="1.2" vector-effect="non-scaling-stroke"></rect>')
        return s.format(vb=f"{f(x)} {f(y)} {f(side)} {f(side)}", b=cut + body + edge)
    c = lambda d, core=BRONZE: cable(d, core, 3.4, 1.2)  # noqa: E731
    if kind == "k-conn":
        b = c("M13 0 V26") + box(13, 13)
    elif kind == "k-raw":
        b = c("M7 0 V26") + deposit(7, 13, k=.8)
    elif kind == "k-tr":
        b = (c("M13 0 V13") + c("M13 13 V26", SILVER)
             + f'<rect x="7" y="3" width="12" height="20" rx="6" fill="{T_SILVER}" stroke="{INK}" stroke-width="1.4"></rect>')
    elif kind in ("k-bronze", "k-silver", "k-gold2"):
        fill, pid = {"k-bronze": (T_BRONZE, "p-brick"), "k-silver": (T_SILVER, "p-diag"),
                     "k-gold2": (T_GOLD, "p-stip")}[kind]
        b = (f'<rect x="1" y="4" width="24" height="18" fill="{fill}"></rect>'
             f'<rect x="1" y="4" width="24" height="18" fill="url(#{pid})" opacity=".5"></rect>'
             f'<rect x="1" y="4" width="24" height="18" fill="none" stroke="{INK}" stroke-width="1.3"></rect>')
    elif kind == "k-gold":
        b = c("M20 0 V9", GOLD) + bed(3, 9, 22, 12)
    elif kind == "k-views":
        b = c("M5 0 L10 10 M13 0 V10 M21 0 L16 10", SILVER) + c("M13 16 V26", GOLD) + splice_box(13, 13, 20)
    elif kind == "k-db":
        b = c("M13 0 V6", GOLD) + lens(13, 14, 24, 14, small=True)
    elif kind == "k-models":
        b = c("M13 0 V13", GOLD) + terminal(13, 15, T_GOLD, 5.5)
    else:
        b = c("M13 0 V11", GOLD) + terminal(13, 15, T_GOLD, 5.5)
    return s.format(vb="0 0 26 26", b=b)


def index_html() -> str:
    parts = []
    src = []
    for k in SRC:
        p = PARTS[f"source-{k}"]
        lk = p["links"][0]
        desc = p["index"].split(": ", 1)[1]
        src.append(f'<li class="k" data-t="li-src-{k}">{mark("src-" + k)}<div>'
                   f'<p class="k-t" data-t="src-{k}"><a href="{lk["url"]}"><code>{k}</code></a> '
                   f'<span class="hn">{esc(p["human_name"])}</span></p>'
                   f'<p class="k-d">{esc(desc)}</p></div></li>')
    parts.append(f'<ul class="kx kx-sky" aria-label="Sources">{"".join(src)}</ul>')
    groups: dict[str, list[str]] = {}
    for key, pid, grp in BELOW:
        p = PARTS[pid]
        models = pid == "reader-gridflow-models"
        title = monoize(p["label"]) if pid != "reader-cli" else "The <code>gridflow</code> command"
        groups.setdefault(grp, []).append(
            f'<li class="k" data-t="li-{key}">{mark(key if key != "k-gold" else "k-gold")}<div>'
            f'<p class="k-t" data-t="{key}">{title}</p>'
            f'<p class="k-d">{monoize(p["index"])}</p>'
            f'<p class="k-l">{links(p["links"], models)}</p></div></li>')
    labels = {"top": "Below ground: the connectors", "bronze": "Bronze", "silver": "Silver", "gold": "Gold and the readers"}
    for grp in ("top", "bronze", "silver", "gold"):
        parts.append(f'<ul class="kx kx-{grp}" aria-label="{labels[grp]}">{"".join(groups[grp])}</ul>')
    return f'<div class="index">{"".join(parts)}</div>'


def plate_html(svg: str = "") -> str:
    return (f'<section class="plate" data-section="drawing" data-st="drawing" aria-labelledby="d-h">{svg}'
            f'<div class="plate-grid"><div class="plate-head"><h2 id="d-h">The whole system, in one section</h2>'
            f'<p>The sources stand above ground; gridflow’s layers lie below, with the readers at the foot. The '
            f'index names each part and links to its file on GitHub.</p>'
            f'<p class="nums">Discs <span class="sn">1</span> to <span class="sn">7</span> mark the stops of the row '
            f'followed below.</p></div>'
            f'{index_html()}</div></section>')


# ---------------------------------------------------------------- drawn parts
def box(x: float, y: float) -> str:
    """A connector: a junction box on the cable."""
    return (f'<rect x="{f(x - 8)}" y="{f(y - 6.5)}" width="16" height="13" rx="2" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="1.4"></rect><path d="M{f(x - 4)} {f(y)} H{f(x + 4)}" stroke="{INK}" stroke-width="1.2">'
            f'</path>')


def deposit(x: float, y: float, k: float = 1.0) -> str:
    """Raw bytes plus a sidecar: two response files and a small .meta.json tag, beside the cable."""
    out = []
    for i in (1, 0):
        dx, dy = x + 6 * k + i * 3 * k, y - 9 * k - i * 3 * k
        out.append(f'<path d="M{f(dx)} {f(dy)} h{f(12 * k)} l{f(4 * k)} {f(4 * k)} v{f(12 * k)} h{f(-16 * k)} Z" '
                   f'fill="{DAY}" stroke="{INK}" stroke-width="1.1" stroke-linejoin="round"></path>')
    out.append(f'<path d="M{f(x + 9 * k)} {f(y - 2 * k)} h{f(8 * k)} M{f(x + 9 * k)} {f(y + 1 * k)} h{f(10 * k)}" '
               f'stroke="{INK}" stroke-width=".8" opacity=".6"></path>')
    out.append(f'<rect x="{f(x + 18 * k)}" y="{f(y + 2 * k)}" width="{f(9 * k)}" height="{f(7 * k)}" rx="1" '
               f'fill="{KHAKI}" stroke="{INK}" stroke-width="1"></rect>')
    out.append(f'<path d="M{f(x)} {f(y)} H{f(x + 6 * k)}" stroke="{INK}" stroke-width="1.2"></path>')
    return "".join(out)


def pq(x: float, y: float, w: float = 26, h: float = 14) -> str:
    """Typed Parquet: a file cut into columns."""
    cols = " ".join(f"M{f(x + w * i / 4)} {f(y + 2)} V{f(y + h - 2)}" for i in (1, 2, 3))
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{w}" height="{h}" rx="1.5" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="1.2"></rect><path d="{cols}" stroke="{SILVER}" stroke-width="1.6"></path>')


def splice_box(x: float, y: float, w: float = 46) -> str:
    return (f'<rect x="{f(x - w / 2)}" y="{f(y - 6)}" width="{w}" height="12" rx="6" fill="{T_GOLD}" stroke="{INK}" '
            f'stroke-width="1.5"></rect>')


def lens(cx: float, cy: float, w: float, h: float, small: bool = False) -> str:
    """The catalogue: one DuckDB file, drawn as a lens of rock inside gold."""
    d = (f"M{f(cx - w / 2)} {f(cy)} C{f(cx - w / 2)} {f(cy - h * .62)} {f(cx - w * .28)} {f(cy - h / 2)} {f(cx)} "
         f"{f(cy - h / 2)} C{f(cx + w * .28)} {f(cy - h / 2)} {f(cx + w / 2)} {f(cy - h * .62)} {f(cx + w / 2)} "
         f"{f(cy)} C{f(cx + w / 2)} {f(cy + h * .62)} {f(cx + w * .28)} {f(cy + h / 2)} {f(cx)} {f(cy + h / 2)} "
         f"C{f(cx - w * .28)} {f(cy + h / 2)} {f(cx - w / 2)} {f(cy + h * .62)} {f(cx - w / 2)} {f(cy)} Z")
    out = [f'<path d="{d}" fill="{DAY}" stroke="{INK}" stroke-width="{1.2 if small else 1.6}"></path>']
    if small:
        out.append(f'<path d="M{f(cx - 6)} {f(cy - 2)} h12 M{f(cx - 6)} {f(cy + 2)} h12" stroke="{INK}" '
                   f'stroke-width=".8" opacity=".6"></path>')
    return "".join(out)


def bed(x: float, y: float, w: float, h: float) -> str:
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(min(h / 2, 8))}" fill="{GOLD}" '
            f'stroke="{INK}" stroke-width="1.3"></rect>'
            f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(min(h / 2, 8))}" fill="url(#q-stip)" '
            f'opacity=".6"></rect>')


def gas_entry(x: float, base: float) -> str:
    """ENTSO-G: a gas entry point, pipework rising out of the ground with a valve, and its kiosk."""
    pipe = f"M{f(x + 26)} {f(base)} V{f(base - 30)} H{f(x + 58)} V{f(base)} M{f(x + 38)} {f(base)} V{f(base - 18)} H{f(x + 70)} V{f(base)}"
    return "\n".join([
        f'<rect x="{f(x)}" y="{f(base - 24)}" width="18" height="24" fill="{DAY}" stroke="{INK}" stroke-width="1"></rect>',
        f'<path d="M{f(x - 2)} {f(base - 24)} L{f(x + 9)} {f(base - 30)} L{f(x + 20)} {f(base - 24)}" fill="{KHAKI}" '
        f'stroke="{INK}" stroke-width="1" stroke-linejoin="round"></path>',
        f'<path d="{pipe}" stroke="{INK}" stroke-width="6" fill="none" stroke-linejoin="round"></path>',
        f'<path d="{pipe}" stroke="{CLAY}" stroke-width="3.4" fill="none" stroke-linejoin="round"></path>',
        f'<path d="M{f(x + 42)} {f(base - 30)} V{f(base - 40)}" stroke="{INK}" stroke-width="1.4"></path>',
        f'<circle cx="{f(x + 42)}" cy="{f(base - 42)}" r="5" fill="none" stroke="{INK}" stroke-width="1.4"></circle>',
        f'<path d="M{f(x + 37)} {f(base - 42)} h10 M{f(x + 42)} {f(base - 47)} v10" stroke="{INK}" stroke-width=".9"></path>',
    ])


# the drawn assets: key -> (drawing function at (x, base), drop x for the cable, leader start)
ASSET_X = {"gie_alsi": 36, "gie_agsi": 206, "entsog": 330, "entsoe": 450, "open_meteo": 590,
           "neso_data_portal": 640, "neso": 790, "elexon": 880}


def asset(key: str, base: float | None = None, mini: bool = False) -> tuple[str, str]:
    """Draw one source's asset. Full size: returns (svg, leader point 'x y'); mini: (svg, viewBox)."""
    x = 0.0 if mini else ASSET_X[key]
    b = 100.0 if mini else base
    assert b is not None
    if key == "gie_alsi":
        g = hp.sc(sn.lng_terminal(x, b), x, b, .82)
        return (g, "-2 44 64 60") if mini else (g, f"{f(x + 25)} {f(b - 45)}")
    if key == "gie_agsi":
        g = hp.sc(hp.gasterminal(x, b), x, b, .9)
        return (g, "-3 58 54 44") if mini else (g, f"{f(x + 23)} {f(b - 41)}")
    if key == "entsog":
        g = gas_entry(x, b)
        return (g, "-4 50 80 52") if mini else (g, f"{f(x + 42)} {f(b - 47)}")
    if key == "entsoe":
        g = hp.sc(hp.converter(x, b), x, b, .84)
        return (g, "-38 34 114 68") if mini else (g, f"{f(x + 28)} {f(b - 53)}")
    if key == "open_meteo":
        h = 30 if mini else 138
        g = hp.metmast(x, b, h) if not mini else (
            f'<path d="M{f(x)} {f(b)} V{f(b - h)} M{f(x)} {f(b - h * .6)} H{f(x + 9)} M{f(x)} {f(b - h)} H{f(x + 9)} '
            f'M{f(x)} {f(b - h * .6)} H{f(x - 7)}" stroke="{INK}" stroke-width="1.6"></path>'
            f'<circle cx="{f(x + 9)}" cy="{f(b - h - 1.5)}" r="1.8" fill="{INK}"></circle>'
            f'<circle cx="{f(x + 9)}" cy="{f(b - h * .6 - 1.5)}" r="1.8" fill="{INK}"></circle>')
        return (g, "-13 64 26 38") if mini else (g, f"{f(x)} {f(b - h - 10)}")
    if key == "neso_data_portal":
        if mini:
            g = (f'<path d="M-14 100 L-11 78 L10 78 L12 100 Z" fill="{OLIVE}"></path>'
                 f'<path d="M-9 96 L9 96 L5 88 L-13 88 Z" fill="{CHART}" stroke="{INK}" stroke-width="1"></path>'
                 f'<path d="M-4 96 V100 M4 96 V100" stroke="{INK}" stroke-width="1"></path>'
                 f'<path d="M-10 86 L8 86 L5 80 L-13 80 Z" fill="{CHART}" stroke="{INK}" stroke-width="1"></path>')
            return g, "-15 76 26 26"
        g = sn.solar_farm_at(x, x + 120, hp.prof)
        return g, f"{f(x + 62)} {f(hp.prof(x + 62) - 44)}"
    if key == "neso":
        g = hp.ccgt(x, b, .8)
        return (g, "-22 8 104 94") if mini else (g, f"{f(x + 72)} {f(b - 92)}")
    if key == "elexon":
        sub, _ = hp.substation(x, b)
        return (sub, "-6 44 92 58") if mini else (sub, f"{f(x + 57)} {f(b - 52)}")
    raise KeyError(key)


def route(n: int, x: float, y: float) -> str:
    """A journey stop marker: the same numbered disc as the notebook's stop headings; stop 5 is energised."""
    fill = CHART if n == 5 else DAY
    return (f'<g class="rt"><circle cx="{f(x)}" cy="{f(y)}" r="9.5" fill="{fill}" stroke="{INK}" '
            f'stroke-width="1.4"></circle><text x="{f(x)}" y="{f(y + 4.3)}" text-anchor="middle">{n}</text></g>')


def leader(x0: float, y0: float, y1: float, sky: bool = False) -> str:
    """A hairline from a part to its index mark: dot on the part, a straight run, a short shoulder into the mark."""
    col = ONP if sky else INK
    kx = LX - 10
    d = f"M{f(x0)} {f(y0)} L{f(kx)} {f(y1)} H{f(LX)}" if abs(y1 - y0) > .5 or x0 < kx else f"M{f(x0)} {f(y0)} H{f(LX)}"
    return (f'<path d="{d}" stroke="{col}" stroke-width=".9" fill="none" opacity="{.72 if sky else .8}"></path>'
            f'<circle cx="{f(x0)}" cy="{f(y0)}" r="2.6" fill="{col}" stroke="{INK if sky else DAY}" '
            f'stroke-width=".8"></circle>')


def label(x: float, y: float, s: str, anchor: str = "start", col: str = INK, mono: bool = False) -> str:
    cls = ' class="mono"' if mono else ""
    return f'<text{cls} x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" fill="{col}">{s}</text>'


def draw_plate(m: dict) -> tuple[str, dict]:
    """The drawing, in page coordinates, wrapped to sit at the plate section's origin."""
    t = m["t"]
    D0, DH = m["secs"]["drawing"]
    mid = lambda k: (t[k][1] + t[k][3]) / 2 if k.startswith("li-") else t[k][1] + 11  # noqa: E731
    Ls = t["li-src-elexon"][3]
    G = t["k-conn"][1] - 52
    hp.Y["surf"] = G
    y_c = mid("k-conn")
    c_tb = t["li-k-raw"][1] - 36
    c_bs = t["li-k-tr"][1] - 38
    c_sg = t["li-k-gold"][1] - 38
    y_raw, y_br, y_ks = mid("k-raw"), mid("k-bronze"), mid("k-silver")
    y_g, y_m, y_db = mid("k-gold"), mid("k-views"), mid("k-db")
    y_cli, y_cl, y_nb, y_md = mid("k-cli"), mid("k-client"), mid("k-nb"), mid("k-models")
    out: list[str] = []
    back: list[str] = []
    labs: list[str] = []
    # ---------------------------------------------------------------- above ground
    FAR = "#297382"
    back.append(sn.ridge([(-20, G - 150), (160, G - 168), (330, G - 158), (520, G - 172), (700, G - 150),
                          (880, G - 134), (1060, G - 128), (1240, G - 122), (1460, G - 126)], G, FAR))
    near = [(-20, G - 112), (90, G - 128), (220, G - 136), (350, G - 120), (470, G - 130), (610, G - 116),
            (760, G - 104), (900, G - 98), (1080, G - 100), (1260, G - 94), (1460, G - 100)]
    back.append(sn.ridge(near, G, HORIZON))
    for i, (tx, ty) in enumerate([(90, G - 128), (220, G - 136), (350, G - 120), (470, G - 130)]):
        hgt = [58, 64, 56, 62][i]
        back.append(hp.turbine(tx, ty + 3, hgt, hgt * .5, ["sp2", "sp1", "sp3", "sp2"][i], 37 * i + 10))
    for i, tx in enumerate([1010, 1130, 1250, 1370]):
        back.append(hp.turbine(tx, G - 98, 44, 22, ["sp1", "sp3", "sp2", "sp1"][i], 23 * i + 5))
    top = [(-20, G - 70), (180, G - 78), (380, G - 66), (580, G - 76), (780, G - 70), (980, G - 64), (1200, G - 70),
           (1460, G - 62)]
    back.append(sn.field(top, hp.prof, -20, 1460, [[(-20, G - 50), (500, G - 54), (1000, G - 44), (1460, G - 48)],
                                                   [(200, G - 26), (800, G - 30), (1460, G - 22)]]))
    # a pylon line carries the grid away east of the substation, under the index
    pls = [(1000, hp.prof(1000), .56), (1170, hp.prof(1170), .5), (1330, hp.prof(1330), .46)]
    wires = [hp.spans(hp.tips(*pls[0], -1), [(956, G - 48), (962, G - 44), (968, G - 44)], 7)]
    for a, b in zip(pls, pls[1:]):
        wires.append(hp.spans(hp.tips(*a, 1), hp.tips(*b, -1), 10))
    wires.append(hp.spans(hp.tips(*pls[-1], 1), [(1460, G - 40), (1460, G - 52), (1460, G - 62)], 6))
    back.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.3">'
                + "".join(hp.pylon(*p) for p in pls) + "</g>")
    back.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".8"></path>')
    lead_pts = {}
    for k in SRC:
        g, pt = asset(k, hp.prof(ASSET_X[k] + 30))
        out.append(g)
        lead_pts[k] = tuple(float(v) for v in pt.split())
    # the fan: each asset's leader runs up to its index entry; the last (elexon) rises straight into its mark
    for k in SRC:
        x0, y0 = lead_pts[k]
        y1 = mid(f"src-{k}")
        if k == "elexon":
            mk_b = t[f"src-{k}"][1] + 24
            out.append(f'<path d="M{f(IX + 13)} {f(y0)} V{f(mk_b)}" stroke="{ONP}" stroke-width=".9" opacity=".72">'
                       f'</path><circle cx="{f(IX + 13)}" cy="{f(y0)}" r="2.6" fill="{ONP}" stroke="{INK}" '
                       f'stroke-width=".8"></circle>')
        else:
            out.append(leader(x0, y0, y1, sky=True))
    # ---------------------------------------------------------------- the cables
    drops = {"gie_alsi": 89, "gie_agsi": 256, "entsog": 350, "entsoe": 478, "open_meteo": 590,
             "neso_data_portal": 700, "neso": 815, "elexon": 922}
    y_j8 = y_ks + 30
    x_s = 500
    cab_b, cab_s, cab_g, parts = [], [], [], []
    for i, k in enumerate(SRC):
        xd, xl = drops[k], LANES[i]
        top_y = hp.prof(xd) - 2
        cab_b.append(cable(drop(xd, top_y, xl, contact_y("silver", c_bs, xl), G + 6, G + 42)))
        parts.append(box(xl, y_c))
        parts.append(deposit(xl, y_raw))
        parts.append(sleeve(xl, contact_y("silver", c_bs, xl), T_SILVER))
        yb = contact_y("silver", c_bs, xl)
        target = x_s - 21 + 6 * i
        if k == "elexon":
            cab_s.append(cable(f"M{xl} {f(yb)} V{f(y_g - 12)}", SILVER))
            cab_s.append(cable(drop(xl, y_j8, target, y_m - 6, y_j8 + 2, y_m - 20), SILVER))
            parts.append(pq(xl - 13, y_ks - 21))
            parts.append(pq(xl - 13, y_ks - 3))
            parts.append(joint(xl, y_j8, 3.6))
        else:
            cab_s.append(cable(drop(xl, yb, target, y_m - 6, y_ks + 40, y_m - 20), SILVER))
            parts.append(pq(xl - 13, y_ks - 7))
    # gold: the builder's bed fed by the elexon cable, the splice where every silver cable becomes a view,
    # the catalogue lens, then the readers
    xl8 = LANES[-1]
    parts.append(sleeve(xl8, contact_y("gold", c_sg, xl8), T_GOLD))
    cab_g.append(cable(f"M{xl8} {f(contact_y('gold', c_sg, xl8))} V{f(y_g - 9)}", GOLD))
    bx0, bw = 694, 176
    parts.append(bed(bx0, y_g - 10, bw, 20))
    labs.append(label(bx0 + 12, y_g + 4.5, "system_marginal_price", mono=True))
    lx0, lw, lh = x_s, 250, 64
    cab_g.append(cable(f"M{x_s} {f(y_m)} V{f(y_db - lh / 2 + 2)}", GOLD))
    parts.append(splice_box(x_s, y_m))
    parts.append(lens(lx0, y_db, lw, lh))
    labs.append(label(lx0, y_db + 5, "gridflow.duckdb", "middle", mono=True))
    # readers: cables leave the lens and step down and to the left, so no leader crosses a cable
    xc, xcl, xn, xm = 752, 622, 470, 196
    cab_g.append(cable(f"M{f(lx0 + 88)} {f(y_db + 22)} C{f(lx0 + 150)} {f(y_db + 60)} {f(xc)} {f(y_db + 40)} "
                       f"{f(xc)} {f(y_db + 84)} V{f(y_cli - 6)}", GOLD))
    cab_g.append(cable(f"M{f(lx0 + 30)} {f(y_db + 31)} C{f(lx0 + 40)} {f(y_db + 90)} {f(xcl)} {f(y_db + 70)} "
                       f"{f(xcl)} {f(y_db + 130)} V{f(y_cl - 6)}", GOLD))
    cab_g.append(cable(f"M{f(xcl)} {f(y_cl + 6)} C{f(xcl)} {f(y_cl + 60)} {f(xn)} {f(y_cl + 40)} {f(xn)} "
                       f"{f(y_cl + 90)} V{f(y_nb - 6)}", GOLD))
    y_tap = c_sg - 26
    cab_g.append(cable(f"M{xm} {f(y_md - 6)} V{f(contact_y('gold', c_sg, xm))}", GOLD))
    cab_s.append(cable(f"M{xm} {f(contact_y('gold', c_sg, xm))} V{f(y_tap + 8)}", SILVER))
    parts.append(sleeve(xm, contact_y("gold", c_sg, xm), T_GOLD))
    parts.append(f'<path d="M{f(xm - 9)} {f(y_tap + 8)} H{f(xm + 9)} M{f(xm - 6)} {f(y_tap + 3)} H{f(xm + 6)} '
                 f'M{f(xm - 3)} {f(y_tap - 2)} H{f(xm + 3)}" stroke="{INK}" stroke-width="1.6"></path>')
    for x, y in ((xc, y_cli), (xcl, y_cl), (xn, y_nb), (xm, y_md)):
        parts.append(terminal(x, y, T_GOLD))
    # labels, short, on the first cable or beside the part, never in a leader's path
    x1 = LANES[0]
    labs += [
        label(x1 - 16, y_c + 4.5, "connector", "end"),
        label(x1 - 12, y_raw - 3, "raw bytes,", "end"),
        label(x1 - 12, y_raw + 13, ".meta.json", "end"),
        label(x1 - 14, contact_y("silver", c_bs, x1) + 4.5, "transformer", "end"),
        label(x1 - 19, y_ks - 3, "typed", "end"),
        label(x1 - 19, y_ks + 13, "Parquet", "end"),
        label(xl8 - 22, y_ks - 12, "one file", "end"),
        label(xl8 - 22, y_ks + 5, "per capture", "end"),
        label(x_s - 30, y_m + 4.5, "views over Parquet", "end"),
        label(xm - 14, c_sg + 34, "reads silver files", "end"),
        label(xm - 14, c_sg + 51, "as of a time", "end"),
        label(xc + 14, y_cli + 24, "gridflow", mono=True),
        label(xcl + 14, y_cl + 24, "GridflowClient", mono=True),
        label(xn, y_nb + 26, "notebooks", "middle"),
        f'<a href="models.html">{label(xm, y_md + 26, "gridflow_models", "middle", mono=True)}</a>',
        label(1360, c_tb + 23, "bronze", "end"), label(1360, c_bs + 23, "silver", "end"), label(1360, c_sg + 23, "gold", "end"),
    ]
    # leaders below ground: every part is the rightmost thing at its own level
    leads = [
        leader(xl8 + 8, y_c, y_c),
        leader(xl8 + 27, y_raw + 5, y_raw),
        leader(IX - 36, y_br, y_br),
        leader(xl8 + 7, contact_y("silver", c_bs, xl8) + 10, mid("k-tr")),
        leader(xl8 + 13, y_ks - 3, y_ks),
        leader(bx0 + bw, y_g, y_g),
        leader(x_s + 23, y_m, y_m),
        leader(lx0 + lw / 2, y_db, y_db),
        leader(xc + 7, y_cli, y_cli),
        leader(xcl + 7, y_cl, y_cl),
        leader(xn + 7, y_nb, y_nb),
        leader(xm + 7, y_md, y_md),
    ]
    # the row's stops, on the elexon cable and the parts it reaches
    rts = [route(1, xc - 24, y_cli - 18), route(2, xl8 - 22, y_c - 12), route(3, xl8 - 22, y_raw - 12),
           route(4, xl8 - 44, y_ks - 34), route(5, x_s + 40, y_m - 22), route(6, bx0 - 18, y_g - 16),
           route(7, xcl - 24, y_cl - 18)]
    aria = ("The whole system in one section. Above ground, left to right: an LNG terminal (gie_alsi), gas storage "
            "tanks (gie_agsi), a gas entry point (entsog), an interconnector converter station (entsoe), a met mast "
            "(open_meteo), a solar farm (neso_data_portal), a gas-fired power station (neso) and a "
            "substation (elexon); each has a leader to its index entry. A cable drops from each through a connector "
            "in the topsoil, leaves raw bytes and a .meta.json sidecar in bronze, passes a transformer at the silver "
            "contact and becomes typed Parquet in silver, where elexon's system prices keep one file per capture. In "
            "gold, the elexon cable feeds the system_marginal_price builder, and every silver cable splices into "
            "views over Parquet inside one file, gridflow.duckdb. From it hang the gridflow command and "
            "GridflowClient, which notebooks open; gridflow_models reaches past the catalogue to read silver files "
            "as of a time. Numbered discs 1 to 7 mark the stops of the row followed below.")
    H = int(DH)
    svg = (f'<svg class="layer draw" width="1440" height="{H}" viewBox="0 {f(D0)} 1440 {H}" role="img" '
           f'aria-label="{aria}"><defs><pattern id="q-stip" width="6" height="6" patternUnits="userSpaceOnUse">'
           f'<circle cx="1.5" cy="2" r=".8" fill="{INK}"></circle><circle cx="4.5" cy="5" r=".6" fill="{INK}">'
           f'</circle></pattern></defs>'
           + "\n".join(back) + "\n" + "".join(cab_b + cab_s + cab_g) + "\n" + "".join(out) + "".join(parts)
           + "".join(leads) + "".join(rts) + f'<g class="lab">{"".join(labs)}</g></svg>')
    geo = {"G": G, "c_tb": c_tb, "c_bs": c_bs, "c_sg": c_sg, "Ls": Ls}
    return svg, geo


# ================================================================ the journey: one notebook
PROMPT = 0


def cell(code: str, lang: str, tag: str, cls: str = "") -> str:
    global PROMPT
    PROMPT += 1
    return (f'<div class="cell{cls}"><span class="pr">[{PROMPT}]:</span><div class="in"><span class="lang">{tag}'
            f'</span><pre>{hl(code, lang)}</pre></div></div>')


def printed(text: str) -> str:
    return f'<div class="cell out"><span class="pr"></span><pre class="o">{esc(text)}</pre></div>'


def df(cols: list[str], rows: list[list[str]], prompt: bool = True) -> str:
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = "".join("<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for r in rows)
    pr = f"[{PROMPT}]:" if prompt else ""
    return (f'<div class="cell out"><span class="pr">{pr}</span><div class="scroll"><table class="df"><thead><tr>'
            f'{head}</tr></thead><tbody>{body}</tbody></table></div></div>')


def filepane(head: str, text: str, lang: str = "", note: str = "", cls: str = "") -> str:
    n = f'<span class="fn">{note}</span>' if note else ""
    return (f'<div class="cell file{cls}"><span class="pr"></span><div class="fp"><p class="fh"><code>{esc(head)}</code>'
            f'{n}</p><pre>{hl(text, lang) if lang else esc(text)}</pre></div></div>')


def md(n: int, stop: dict, extra: str = "") -> str:
    body = monoize_md(stop["body"])
    return (f'<div class="md"><h3 id="s{n}-h"><span class="sn{" hot" if n == 5 else ""}">{n}</span>'
            f'{esc(stop["heading"])}</h3><p>{body}</p>{extra}</div>')


def monoize_md(s: str) -> str:
    e = esc(s)
    for w in ["silver_elexon_system_prices_latest", "available_at", "source_run_id", "dataset_version",
              "system_marginal_price", "GridflowClient", "get_system_prices", "_latest", ".meta.json", "ingest",
              "transform"]:
        e = re.sub(rf"(?<![\w>_]){re.escape(w)}(?![\w<])", f"<code>{w}</code>", e)
    return e


def asof_figure() -> str:
    """Stop 5's figure: the two vintages in silver, and what an as-of read returns at each moment.

    Every number is from the pack: available_at 2026-09-08 17:48:45 (9.56) and 2026-09-09 17:44:29 (110.0), the
    as-of time 2026-09-09 12:00 of 05-as-of.sql, and the _latest view's answer, 110.0.
    """
    w, h = 872, 244
    L, R, Tp, B = 58, 24, 40, 40
    pw, ph = w - L - R, h - Tp - B
    hrs = 36.0

    def X(hh: float) -> float:
        return L + hh / hrs * pw

    def Y(v: float) -> float:
        return Tp + (120 - v) * ph / 120

    e1, e2, ao = 5 + 48 / 60 + 45 / 3600, 24 + 5 + 44 / 60 + 29 / 3600, 24.0
    g = []
    for v in (0, 50, 100):
        g.append(f'<path d="M{L - 5} {f(Y(v))} H{L}" stroke="{INK}" stroke-width="1"></path>'
                 f'<text x="{L - 9}" y="{f(Y(v) + 4)}" text-anchor="end">{v}</text>')
    for hh, s in ((6, "8 Sep 18:00"), (12, "9 Sep 00:00"), (24, "9 Sep 12:00"), (30, "9 Sep 18:00"),
                  (36, "10 Sep 00:00")):
        g.append(f'<path d="M{f(X(hh))} {Tp + ph} v6" stroke="{INK}" stroke-width="1"></path>'
                 f'<text x="{f(X(hh))}" y="{Tp + ph + 21}" text-anchor="middle">{s}</text>')
    g.append(f'<path d="M{L} {Tp - 8} V{Tp + ph} H{L + pw}" stroke="{INK}" stroke-width="1.2" fill="none"></path>')
    g.append(f'<text class="mono" x="{L + 8}" y="{Tp - 4}">system_sell_price</text>')
    # the as-of time of 05-as-of.sql
    g.append(f'<path d="M{f(X(ao))} {Tp - 2} V{Tp + ph}" stroke="{PETROL}" stroke-width="1.2"></path>')
    # what an as-of read returns at each moment: nothing before the first publication, then 9.56, then 110.0
    step = f"M{f(X(e1))} {f(Y(9.56))} H{f(X(e2))} V{f(Y(110))} H{f(L + pw)}"
    g.append(f'<path d="{step}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path>')
    g.append(f'<circle cx="{f(X(ao))}" cy="{f(Y(9.56))}" r="6.5" fill="{CHART}" stroke="{INK}" stroke-width="1.4">'
             f'</circle>')
    for hh, v in ((e1, 9.56), (e2, 110)):
        g.append(f'<circle cx="{f(X(hh))}" cy="{f(Y(v))}" r="4.2" fill="{DAY}" stroke="{INK}" stroke-width="1.6">'
                 f'</circle>')
    g.append(f'<text class="dl" x="{f(X(e1) + 2)}" y="{f(Y(9.56) - 30)}">first published</text>'
             f'<text class="dl" x="{f(X(e1) + 2)}" y="{f(Y(9.56) - 13)}">8 Sep 17:48:45, 9.56</text>')
    g.append(f'<text class="dl" x="{f(X(ao) - 12)}" y="{f(Y(9.56) - 30)}" text-anchor="end">an as-of read at 9 Sep '
             f'12:00</text><text class="dl" x="{f(X(ao) - 12)}" y="{f(Y(9.56) - 13)}" text-anchor="end">returns '
             f'9.56</text>')
    g.append(f'<text class="dl" x="{f(X(e2) + 10)}" y="{f(Y(110) - 25)}">revision published</text>'
             f'<text class="dl" x="{f(X(e2) + 10)}" y="{f(Y(110) - 9)}">9 Sep 17:44:29, 110.0</text>')
    g.append(f'<circle cx="{f(L + pw)}" cy="{f(Y(110))}" r="6.5" fill="{CHART}" stroke="{INK}" stroke-width="1.4">'
             f'</circle>')
    g.append(f'<text class="dl" x="{f(X(e2) + 12)}" y="{f(Y(110) + 24)}">the <tspan class="mono">_latest</tspan> '
             f'view</text><text class="dl" x="{f(X(e2) + 12)}" y="{f(Y(110) + 40)}">returns 110.0</text>')
    aria = ("Step chart for silver_elexon_system_prices, settlement date 2026-09-08, period 37: the system_sell_price "
            "an as-of read returns, by as-of time from 8 September 12:00 to 10 September 00:00 UTC. Nothing is known "
            "before 8 September 17:48:45, when 9.56 is first published; 9.56 holds until the revision is published "
            "on 9 September at 17:44:29, and 110.0 after it. A line at 9 September 12:00 marks the as-of read that "
            "returns 9.56; the _latest view returns 110.0.")
    svg = (f'<svg class="chart" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
           + "".join(g) + "</svg>")
    cap = ("<code>silver_elexon_system_prices</code>, settlement date 2026-09-08, period 37: the "
           "<code>system_sell_price</code> an as-of read returns at each moment, 8 to 10 September 2026, UTC.")
    return f'<figure class="fig">{svg}<figcaption class="cap">{cap}</figcaption></figure>'


OUT2 = "/balancing/settlement/system-prices/2026-09-08 {'page': 1}"

V_COLS = ["settlement_date", "settlement_period", "system_sell_price", "system_buy_price", "available_at",
          "vintage_policy", "source_run_id", "dataset_version"]
V_ROWS = [["2026-09-08", "37", "9.56", "9.56", "2026-09-08 17:48:45 UTC", "vendor",
           "494e780a-a127-4fa8-b371-25caf146c094", "2.0.0"],
          ["2026-09-08", "37", "110.0", "110.0", "2026-09-09 17:44:29 UTC", "vendor",
           "494e780a-a127-4fa8-b371-25caf146c094", "2.0.0"]]


def journey() -> str:
    global PROMPT
    PROMPT = 0
    s = {i + 1: st for i, st in enumerate(STOPS)}
    stops = []
    # 1: the command (not executed for the pack: no output shown)
    stops.append(f'<section class="stop" aria-labelledby="s1-h">{md(1, s[1])}<div class="cells">'
                 f'{cell(snip("01-cli.sh"), "sh", "shell")}</div></section>')
    # 2: the request
    stops.append(f'<section class="stop" aria-labelledby="s2-h">{md(2, s[2])}<div class="cells">'
                 f'{cell(snip("02-connector-request.py"), "py", "python")}'
                 f'{printed(OUT2)}'
                 f'{filepane("request_url", snip("02-connector-request.txt"), cls=" req")}</div></section>')
    # 3: bronze
    b_files = snip("03-bronze-files.txt").split("\n")
    stops.append(f'<section class="stop" aria-labelledby="s3-h">{md(3, s[3])}<div class="cells">'
                 f'{filepane(b_files[0], chr(10).join(x.strip() for x in b_files[1:]))}</div>'
                 f'<div class="wide pair">'
                 f'{filepane("raw_20260908T214403Z_3a7fca58.json", snip("03-bronze-body-excerpt.json"), "json", "excerpt")}'
                 f'{filepane("raw_20260908T214403Z_3a7fca58.meta.json", snip("03-bronze-sidecar.json"), "json")}'
                 f'</div></section>')
    # 4: silver
    s_files = snip("04-silver-files.txt").split("\n")
    stops.append(f'<section class="stop" aria-labelledby="s4-h">{md(4, s[4])}<div class="cells">'
                 f'{filepane(s_files[0], chr(10).join(x.strip() for x in s_files[1:]))}'
                 f'{cell(snip("04-silver-vintages.sql"), "sql", "sql")}</div>'
                 f'<div class="wide">{df(V_COLS, V_ROWS)}</div></section>')
    # 5: the latest view picks a winner (the highlighted stop)
    mech = f'<p class="mech">{monoize_md(s[5]["mechanism"])}</p>'
    c_latest = cell(snip("05-latest-view.sql"), "sql", "sql")
    t_latest = df(["settlement_date", "settlement_period", "system_sell_price", "system_buy_price", "available_at"],
                  [["2026-09-08", "37", "110.0", "110.0", "2026-09-09 17:44:29 UTC"]])
    ddl = cell(snip("05-latest-view-ddl.sql"), "sql", "sql", " ddl")
    c_asof = cell(snip("05-as-of.sql"), "sql", "sql")
    t_asof = df(["settlement_date", "settlement_period", "system_sell_price", "available_at"],
                [["2026-09-08", "37", "9.56", "2026-09-08 17:48:45 UTC"]])
    stops.append(f'<section class="stop hero" aria-labelledby="s5-h">{md(5, s[5], mech)}'
                 f'<div class="cells">{asof_figure()}{c_latest}{t_latest}</div>'
                 f'<div class="wide">{ddl}</div>'
                 f'<div class="wide pair2">{c_asof}{t_asof}</div>'
                 f'</section>')
    # 6: gold (the shell command was not executed for the pack; the row comes from build())
    c6a = cell(snip("06-gold-build.sh"), "sh", "shell")
    c6b = cell(snip("06-gold-build.py"), "py", "python")
    t6 = df(["settlement_date", "settlement_period", "system_buy_price", "system_sell_price", "spread",
             "abs_imbalance", "hour_of_day", "day_of_week"],
            [["2026-09-08", "37", "110.0", "110.0", "0.0", "346.717783", "17", "2"]], prompt=False)
    stops.append(f'<section class="stop" aria-labelledby="s6-h">{md(6, s[6])}<div class="cells">{c6a}{c6b}{t6}'
                 f'</div></section>')
    # 7: Polars
    c7 = cell(snip("07-client.py"), "py", "python")
    t7 = df(["settlement_date", "settlement_period", "system_sell_price", "system_buy_price", "available_at"],
            [["2026-09-08", "37", "110.0", "110.0", "2026-09-09 17:44:29 UTC"]], prompt=False)
    stops.append(f'<section class="stop" aria-labelledby="s7-h">{md(7, s[7])}<div class="cells">{c7}{t7}</div>'
                 f'</section>')
    aria = ("A notebook following one row, Elexon system_prices for settlement date 2026-09-08, period 37, through "
            "seven stops. Each stop's note sits beside the pack's real snippet and its real output.")
    nb = (f'<figure class="nb" aria-label="{aria}"><div class="nb-bar"><span class="nb-tab">'
          f'system_prices 2026-09-08 period 37</span></div>'
          f'<div class="nb-body">{"".join(stops)}</div></figure>')
    head = (f'<div class="j-head"><h2 id="j-h">One row, from the command to a DataFrame</h2>'
            f'<p>One real Elexon <code>system_prices</code> row, settlement date 2026-09-08, period 37. Two captures '
            f'of that day hold two versions of it: first published at 9.56, then 110.00 a day later. The numbered '
            f'stops match the discs on the drawing.</p></div>')
    return (f'<section class="st jr" data-section="journey" data-st="journey" aria-labelledby="j-h">{head}{nb}'
            f'</section>')


# ================================================================ how it stays correct: a spec sheet
TERMS = ["Raw bytes", "Re-runs", "Validation", "<code>available_at</code>", "One file"]


def correct() -> str:
    c = SEC["correctness"]
    rows = []
    for term, r in zip(TERMS, c["rules"]):
        rows.append(f'<div><dt>{term}</dt><dd><p>{monoize(r["rule"])}</p></dd>'
                    f'<dd class="lk">{links(r["links"])}</dd></div>')
    rt, ci = c["run_tracking"], c["ci"]
    rows.append(f'<div><dt>Run tracking</dt><dd><p>{monoize(rt["text"])}</p></dd>'
                f'<dd class="lk">{links(rt["links"]).replace(", ", "<br>")}</dd></div>')
    rows.append(f'<div><dt>CI</dt><dd><p>{esc(ci["text"]).replace("src/gridflow", "<code>src/gridflow</code>")}</p></dd><dd class="lk">{links(ci["links"])}</dd></div>')
    ddl = (f'<figure class="ddl-w"><p class="fh"><code>storage/duckdb.py</code>'
           f'</p><pre>{hl(snip("08-run-tracking.sql"), "sql")}</pre></figure>')
    return (f'<section class="st st-deep cor" data-section="correct" data-st="correct" aria-labelledby="c-h">'
            f'<div class="cor-grid"><div><h2 id="c-h">How it stays correct</h2><dl class="spec">{"".join(rows)}'
            f'</dl></div>{ddl}</div></section>')


def look() -> str:
    items = []
    for e in SEC["where_to_look"]["entries"]:
        what = e["for"][0].upper() + e["for"][1:]
        lk = ", ".join(f'<a href="{x["url"]}"><code>{short(x["file"])}</code></a>' for x in e["links"])
        items.append(f'<li><span class="for">{esc(what)}</span><span class="to">{lk}</span></li>')
    return (f'<section class="st st-deep look" data-section="look" data-st="look" aria-labelledby="l-h">'
            f'<h2 id="l-h">Where to look</h2><ul class="lk-list">{"".join(items)}</ul></section>')


def html_body(svg: str = "") -> str:
    return "\n".join([opening(), plate_html(svg), journey(), correct(), look(),
                      f'<div data-st="foot">{footer()}</div>'])


CSS = """.op{padding-bottom:58px}
.op h1{margin-top:62px;color:#F6F4EC;font-weight:760;font-stretch:84%;font-size:86px;line-height:.94;letter-spacing:-.022em}
.op-grid{display:grid;grid-template-columns:minmax(0,1fr) 460px;column-gap:0;margin-top:30px;align-items:start}
.op .lead{margin:0;max-width:40ch;font-size:21px;line-height:1.5;color:#F6F4EC}
.op .scope{margin:6px 0 0;font-size:16px;line-height:1.62;color:#CFE0DC;max-width:44ch}
.plate{position:relative;padding:0 80px 56px}
.plate-grid{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 460px;align-items:start}
.plate-head{padding-top:4px;max-width:470px}
.plate-head h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;color:#F6F4EC;margin:0 0 14px}
.plate-head p{margin:0 0 10px;font-size:16px;line-height:1.62;color:#CFE0DC;max-width:44ch}
.plate-head .nums{font-size:14.5px;color:#B4D0CD}
.sn{display:inline-block;box-sizing:border-box;width:22px;height:22px;border-radius:50%;border:1.4px solid #1C2B22;background:#F6F4EC;color:#1C2B22;font:600 12px/19.5px "Hanken Grotesk",sans-serif;text-align:center;vertical-align:1px}
.sn.hot{background:#AFC64E}
.plate-head .sn{border-color:#1C2B22;margin:0 1px}
.index{grid-column:2;padding-top:6px}
.kx{list-style:none;margin:0;padding:0}
.k{display:grid;grid-template-columns:26px minmax(0,1fr);column-gap:14px;margin:0 0 14px}
.mk{display:block;margin-top:-2px;overflow:hidden}
.k-t{margin:0;font-size:16px;line-height:22px;font-weight:650;color:#1C2B22}
.k-t code{font-size:14.5px;font-weight:500}
.k-d{margin:3px 0 0;font-size:14px;line-height:1.45;color:#3F4A3B}
.k-d code,.k-t code{color:#1C2B22}
.k-d code{font-size:13px;overflow-wrap:anywhere}
.k-l{margin:5px 0 0;font-size:12.5px;line-height:1.5;color:#3F4A3B}
.k-l code{font-size:12.5px}
.k-l .pg{font-weight:600;font-size:14px}
.kx-sky .k{margin-bottom:10px}
.kx-sky .k-t{color:#F6F4EC}
.kx-sky .k-t a{text-decoration-color:#AFC64E}
.kx-sky .k-t code{color:#F6F4EC}
.kx-sky .hn{font-weight:600;font-size:15px;margin-left:6px}
.kx-sky .k-d{color:#CFE0DC;margin-top:1px}
.kx-top{margin-top:214px}
.kx-bronze,.kx-silver,.kx-gold{margin-top:62px}
.draw text,.chart text{font-family:"Hanken Grotesk",sans-serif}
.draw .lab text{font-style:italic;font-size:13.5px}
.draw .lab text.mono,.chart text.mono,.chart tspan.mono{font-family:"Red Hat Mono",monospace;font-style:normal;font-size:12.5px}
.draw .rt text{font-size:12px;font-weight:600;fill:#1C2B22}
.draw a text{text-decoration:underline;text-decoration-color:#66793B}
.jr{padding-top:36px;padding-bottom:76px}
.j-head{display:grid;grid-template-columns:minmax(0,1fr) 460px;align-items:end;margin:0 0 26px}
.j-head h2,.cor h2,.look h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0;max-width:20ch}
.j-head p{margin:0;font-size:16px;line-height:1.62;color:#3F4A3B}
.j-head code{color:#1C2B22}
.nb{margin:0;background:#F6F4EC;border:1.5px solid #1C2B22;border-radius:4px;overflow:hidden}
.nb-bar{display:flex;justify-content:space-between;align-items:flex-end;height:40px;background:#1C2B22;padding:0 18px 0 12px;font:500 13.5px/1 "Red Hat Mono",monospace}
.nb-tab{background:#F6F4EC;color:#1C2B22;padding:11px 18px 12px;border-radius:3px 3px 0 0}
.nb-kern{color:#CFE0DC;align-self:center;font:400 13.5px/1 "Hanken Grotesk",sans-serif}
.nb-body{padding:8px 22px 18px 14px}
.stop{display:grid;grid-template-columns:292px minmax(0,1fr);column-gap:26px;align-items:start;padding:18px 0 18px;border-top:1px solid rgba(28,43,34,.16)}
.stop:first-child{border-top:0}
.stop .wide{grid-column:1 / -1;margin-top:10px}
.md h3{display:flex;gap:10px;align-items:flex-start;font-size:21px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;margin:0 0 8px}
.md h3 .sn{flex:none;margin-top:0}
.md p{margin:0;font-size:14.5px;line-height:1.55;color:#3F4A3B}
.md p.mech{margin-top:10px}
.md code{font-size:13px;color:#1C2B22}
.cells{min-width:0}
.cell{display:grid;grid-template-columns:40px minmax(0,1fr);column-gap:8px;margin:0 0 8px}
.cell.out{margin:-2px 0 10px}
.pr{font:400 12.5px/1 "Red Hat Mono",monospace;color:#5d6a55;text-align:right;padding-top:11px}
.in{position:relative;background:#ECE8DA;border:1px solid rgba(28,43,34,.18);border-radius:3px;min-width:0}
.in pre,.o,.fp pre{margin:0;padding:8px 12px;font:400 13px/1.62 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre;overflow-x:auto}
.lang{position:absolute;right:8px;top:6px;font:400 12px/1 "Hanken Grotesk",sans-serif;color:#5d6a55}
.in .kw{color:#155A6E;font-weight:500}
.in .str,.fp .str{color:#7C5530}
.in .cm,.in .opt{color:#5d6a55}
.fp .key{color:#155A6E}
.o{padding:4px 12px 2px}
.fp{border:1px solid rgba(28,43,34,.22);border-radius:3px;background:#F6F4EC;min-width:0}
.fh{display:flex;justify-content:space-between;gap:12px;margin:0;padding:6px 12px;border-bottom:1px solid rgba(28,43,34,.16);font-size:12.5px;color:#5d6a55;background:#EFEBDF}
.fh code{font-size:12.5px;color:#1C2B22}
.fn{font:italic 400 13px/1.3 "Hanken Grotesk",sans-serif;color:#5d6a55}
.file .fp pre{font-size:12.5px;line-height:1.52}
.req .fp pre{padding:7px 12px}
.pair{display:grid;grid-template-columns:376px minmax(0,1fr);column-gap:12px}
.pair .cell{grid-template-columns:minmax(0,1fr);margin:0}
.pair .cell .pr{display:none}
.pair .fp pre{font-size:12px}
.pair2{display:grid;column-gap:10px;align-items:start}
.scroll{overflow-x:auto;min-width:0}
.df{border-collapse:collapse;margin:2px 0 0;font:400 13px/1 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums;color:#1C2B22}
.df th,.df td{padding:6px 10px;text-align:right;white-space:nowrap}
.df thead th{font-weight:600;border-bottom:1px solid #1C2B22;vertical-align:bottom}
.df tbody tr:nth-child(odd){background:#EFEBDF}
.hero{background:#ECE8DA;margin:0 -22px 0 -14px;padding:24px 22px 20px 14px;border-top:1.5px solid #1C2B22;border-bottom:1.5px solid #1C2B22}
.hero + .stop{border-top:0}
.hero .md h3{font-size:30px;font-stretch:88%;line-height:1.04;margin-bottom:12px}
.hero .md h3 .sn{width:30px;height:30px;font-size:15px;line-height:27px;margin-top:0}
.hero .md p{font-size:15px}
.hero .in{background:#F6F4EC}
.hero .fig{margin:0 0 14px;padding:0 0 0 48px}
.chart{display:block;overflow:visible}
.chart text{font-size:13px;fill:#3F4A3B}
.chart text.dl{font-style:italic;font-size:13.5px;fill:#1C2B22}
.chart text.mono{font-size:12.5px;fill:#1C2B22}
.cap{margin:6px 0 0;font-size:13.5px;line-height:1.5;color:#3F4A3B;max-width:78ch}
.cap code{font-size:12.5px;color:#1C2B22}
.cell.ddl .in pre,.pair2 .in pre{font-size:12px;line-height:1.6}
.cell.ddl{grid-template-columns:36px minmax(0,1fr);column-gap:6px}
.cell.ddl .in pre{padding:8px 10px}
.pair2{grid-template-columns:640px minmax(0,1fr)}
.pair2 .cell.out{margin:0;grid-template-columns:40px minmax(0,1fr)}
.cor{padding-top:112px;padding-bottom:30px}
.cor-grid{display:grid;grid-template-columns:minmax(0,1fr) 470px;column-gap:44px;align-items:start}
.cor h2,.look h2{color:#F6F4EC;margin-bottom:24px}
.spec{margin:0;border-top:1px solid rgba(207,224,220,.22)}
.spec div{display:grid;grid-template-columns:128px minmax(0,1fr) 190px;column-gap:22px;padding:10px 0 11px;border-bottom:1px solid rgba(207,224,220,.22)}
.spec dt{font-weight:600;font-size:15px;line-height:1.45;color:#F6F4EC}
.spec dt code{font-size:13.5px;font-weight:500;color:#F6F4EC}
.spec dd{margin:0}
.spec dd p{margin:0;font-size:15px;line-height:1.5;color:#CFE0DC}
.spec dd p code{font-size:13px;color:#F6F4EC}
.spec .lk{margin:0;padding-top:3px;font-size:12.5px;line-height:1.7}
.spec .lk a,.lk-list a{text-decoration-color:#AFC64E;color:#F6F4EC}
.spec .lk code{font-size:12.5px}
.ddl-w{margin:66px 0 0;background:#ECE8DA;border:1.5px solid #1C2B22;border-radius:3px;overflow:hidden}
.ddl-w .fh{background:#E2DECF}
.ddl-w pre{margin:0;padding:10px 14px 12px;font:400 12.5px/1.62 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre;overflow-x:auto}
.ddl-w .kw{color:#155A6E;font-weight:500}
.ddl-w .str{color:#7C5530}
.look{padding-top:44px;padding-bottom:52px}
.lk-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:56px;border-top:1px solid rgba(207,224,220,.22)}
.lk-list li{display:grid;grid-template-columns:minmax(0,1fr) auto;column-gap:18px;align-items:baseline;padding:11px 0 10px;border-bottom:1px solid rgba(207,224,220,.22)}
.lk-list .for{font-size:14.5px;line-height:1.45;color:#CFE0DC}
.lk-list .to{font-size:13px;text-align:right}
.lk-list code{font-size:13px}
"""


# ================================================================ pass 2
def draw(m: dict) -> tuple[str, int]:
    H = int(math.ceil(m["H"]))
    secs = m["secs"]
    plate_svg, geo = draw_plate(m)
    surf = [(x, hp.prof(x)) for x in range(-40, 1481, 10)]
    y_deep = secs["correct"][0] + 58
    bg = strata_svg(H, geo["G"], surf, [("bronze", geo["c_tb"]), ("silver", geo["c_bs"]), ("gold", geo["c_sg"]),
                                         ("deep", y_deep)])
    return bg, H, plate_svg


_ = (BRONZE, OLIVE, SOFT, contact_pts, rough, smooth)
