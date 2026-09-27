from pathlib import Path

HERE = Path(__file__).parent


def sub(path: str, pairs: list[tuple[str, str]]) -> None:
    p = HERE / path
    s = p.read_text(encoding="utf-8")
    for a, b in pairs:
        assert a in s, (path, a[:80])
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8")


sub("gen_C.py", [
    # A. sky: an optional block under the h1 (the on-this-page list for the long reads)
    ('''def sky(current: str, h1: str, lede: str, right_extra: str = "", crumbs: str = "", marks: str = "") -> str:
    cr = f'<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>' if crumbs else ""
    return (f'<div class="sky">{mast(current)}<div class="head"><div>{cr}<h1>{h1}</h1>{marks}</div>'
            f'<div><p class="lede">{lede}</p>{right_extra}</div></div>{D.horizon()}</div>')''',
     '''def sky(current: str, h1: str, lede: str, right_extra: str = "", crumbs: str = "", marks: str = "") -> str:
    cr = f'<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>' if crumbs else ""
    return (f'<div class="sky">{mast(current)}<div class="head"><div>{cr}<h1>{h1}</h1>{marks}</div>'
            f'<div><p class="lede">{lede}</p>{right_extra}</div></div>{D.horizon()}</div>')


def sky_toc(current: str, h1: str, lede: str, items: list[tuple[str, str]]) -> str:
    li = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in items)
    nav = f'<nav class="toc-l" aria-label="On this page"><ol>{li}</ol></nav>'
    return (f'<div class="sky">{mast(current)}<div class="head"><div><h1>{h1}</h1>{nav}</div>'
            f'<div><p class="lede">{lede}</p></div></div>{D.horizon()}</div>')'''),
    ('''    head = sky("Architecture", "Architecture", lede,
               toc([("brief", "In brief"), ("bronze", "Bronze"), ("silver", "Silver"), ("gold", "Gold"),
                    ("catalogue", "The catalogue"), ("commands", "Commands"), ("gates", "The build and the gates"),
                    ("not", "What it does not do")]))''',
     '''    head = sky_toc("Architecture", "Architecture", lede,
                   [("brief", "In brief"), ("bronze", "Bronze"), ("silver", "Silver"), ("gold", "Gold"),
                    ("catalogue", "The catalogue"), ("commands", "Commands"), ("gates", "The build and the gates"),
                    ("not", "What it does not do")])'''),
    ('''    head = sky("Models", "Models", lede,
               toc([("scores", "Reading the scores"), ("demand", "Day-ahead demand"), ("wind", "Wind generation"),
                    ("solar", "Solar generation"), ("stack", "GB merit-order stack"), ("smp", "Fundamentals SMP"),
                    ("workbench", "In the workbench")]))''',
     '''    head = sky_toc("Models", "Models", lede,
                   [("scores", "Reading the scores"), ("demand", "Day-ahead demand"), ("wind", "Wind generation"),
                    ("solar", "Solar generation"), ("stack", "GB merit-order stack"), ("smp", "Fundamentals SMP"),
                    ("workbench", "In the workbench")])'''),
    # B. hub: the column labels join the arrangement line
    ('''    colhead = ('<div class="tl-h" aria-hidden="true"><span>Dataset</span>'
               '<span>What it holds</span><span>Endpoint</span><span class="r">Held from</span></div>')
    arrange = ('<p class="arrange">Arranged by <a href="#" aria-current="true">what it '
               'measures</a><a href="#">request style</a></p>')''',
     '''    colhead = ""
    arrange = ('<div class="tl-h"><p class="arrange">Arranged by <a href="#" aria-current="true">what it '
               'measures</a><a href="#">request style</a></p><span aria-hidden="true">Endpoint</span>'
               '<span class="r" aria-hidden="true">Held from</span></div>')'''),
    # E. architecture: commands in two columns, the ci.yml row shortened
    ('''                + tl([(f"gridflow {k}", d) for k, d in CLI], "Commands", "220px minmax(0,1fr)")
                + '</div></div>')''',
     '''                + '<div class="two-tl">' + tl([(k, d) for k, d in CLI[:6]], "Commands, first half", "112px minmax(0,1fr)")
                + tl([(k, d) for k, d in CLI[6:]], "Commands, second half", "112px minmax(0,1fr)") + '</div>'
                + '</div></div>')'''),
    ('''CLI = [("init", "Create the DuckDB catalogue and register its views"),
       ("ingest", "API to bronze"),
       ("transform", "Bronze to silver: parsed, validated, deduplicated"),
       ("build", "Silver to gold"),
       ("pipeline", "Ingest, then transform; with <code>--gold</code>, build as well"),
       ("backfill", "Fetch history in chunks"),
       ("export-csv", "Silver Parquet to CSV"),
       ("status", "Run history and a quality summary"),
       ("quality", "Run the quality checks and write a report"),
       ("reset", "Delete bronze, silver and gold data and reset the catalogue"),
       ("prune", "Delete partitions older than a retention cutoff")]''',
     '''CLI = [("init", "Create the catalogue and register its views"),
       ("ingest", "API to bronze"),
       ("transform", "Bronze to silver, validated and deduplicated"),
       ("build", "Silver to gold"),
       ("pipeline", "Ingest, then transform; build too with <code>--gold</code>"),
       ("backfill", "Fetch history in chunks"),
       ("export-csv", "Silver Parquet to CSV"),
       ("status", "Run history and a quality summary"),
       ("quality", "Run the quality checks and write a report"),
       ("reset", "Delete every layer and reset the catalogue"),
       ("prune", "Delete partitions past a retention cutoff")]'''),
    ('''"Every verb is a Typer command on <code>gridflow</code>. Nothing runs on a timer.",''',
     '''"Each is a Typer command, run as <code>gridflow &lt;verb&gt;</code>. Nothing runs on a timer.",'''),
    ('''                 + tl([("ci.yml", "On pull requests and pushes to main: the staleness check, a baseline ratchet and "
                                  "<code>gridflow-build --check</code>"),''',
     '''                 + tl([("ci.yml", "On pull requests and pushes to main: the staleness check, a baseline ratchet "
                                  "and the build check"),'''),
    # F. models: the v2 handle
    ('''                f'<p class="n">In the workbench, <code>{handle}</code></p></div>\'''',
     '''                f'<p class="n">In the workbench, {handle}</p></div>\''''),
    ('''              "models.demand_forecast",''', '''              "<code>models.demand_forecast</code> and <code>models.demand_forecast_v2</code>",'''),
    ('''"models.wind_forecast",''', '''"<code>models.wind_forecast</code>",'''),
    ('''"models.solar_forecast",''', '''"<code>models.solar_forecast</code>",'''),
    ('''["stack.gb.v1"], "models.stack",''', '''["stack.gb.v1"], "<code>models.stack</code>",'''),
    ('''["fundamentals_smp.gb.v1"], "models.fundamentals_smp",''', '''["fundamentals_smp.gb.v1"], "<code>models.fundamentals_smp</code>",'''),
    # CSS additions
    ('''EXTRA_CSS = """''', '''EXTRA_CSS = """.toc-l ol{list-style:none;margin:24px 0 0;padding:0;display:flex;flex-wrap:wrap;column-gap:22px;row-gap:6px;max-width:640px;font-size:15px}
.toc-l a{color:#CFE0DC;text-decoration-color:rgba(175,198,78,.55)}
.toc-l a:hover{color:#F6F4EC;text-decoration-color:#AFC64E}
.hub .tl-h{align-items:baseline;margin:0 0 22px}
.hub .tl-h .arrange{grid-column:1/3;margin:0}
.two-tl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:40px}
.plate + .sc{margin-top:26px}
.folds tbody th{border-bottom:0}
.cell{grid-template-columns:66px minmax(0,1fr)}
.part{margin-top:92px}
.plate text.mono{font-family:"Red Hat Mono",monospace}
'''),
    ('''@media (max-width: 760px){.tl li{''', '''@media (max-width: 760px){.two-tl{grid-template-columns:minmax(0,1fr)}.tl li{'''),
])

sub("draw_c.py", [
    # C. the wind plate's low label in ink (daylight on horizon fails AA)
    ('''f'<text x="{f(xs[lo])}" y="{f(ys[lo] + 22)}" text-anchor="middle" {LAB} fill="{DAY}">\'''',
     '''f'<text x="{f(xs[lo])}" y="{f(ys[lo] + 22)}" text-anchor="middle" {LAB} fill="{INK}">\''''),
    # D. mono file name in the disk plate
    ('''f'<text x="{gx + 54}" y="{gy + 38}" font-family="Red Hat Mono" font-size="13.5" fill="{INK}">gridflow.duckdb</text>\'''',
     '''f'<text class="mono" x="{gx + 54}" y="{gy + 38}" font-size="13.5" fill="{INK}">gridflow.duckdb</text>\''''),
    # G. the pipeline mark: a valve wheel on a riser, not a bench
    ('''            f'<path d="M{f(x + 22)} {f(base - 26)} v-12 M{f(x + 16)} {f(base - 38)} h12 M{f(x + 52)} {f(base - 35)} v-9" '
            f'stroke="{INK}" stroke-width="1.2"></path>'
            f'<path d="M{f(x + 47)} {f(base - 44)} h10 M{f(x + 58)} {f(base - 24)} v7 M{f(x + 61)} {f(base - 24)} v7" '
            f'stroke="{INK}" stroke-width="1.4"></path>'
            f'<path d="M{f(x + 16)} {f(base - 24)} L{f(x + 28)} {f(base - 17)} M{f(x + 28)} {f(base - 24)} L{f(x + 16)} {f(base - 17)}" '
            f'stroke="{INK}" stroke-width=".9"></path>')''',
     '''            f'<path d="M{f(x + 40)} {f(base - 33)} V{f(base - 40)}" stroke="{INK}" stroke-width="2.2"></path>'
            f'<circle cx="{f(x + 40)}" cy="{f(base - 44)}" r="5.5" fill="none" stroke="{INK}" stroke-width="1.4"></circle>'
            f'<path d="M{f(x + 34.5)} {f(base - 44)} h11 M{f(x + 40)} {f(base - 49.5)} v11" stroke="{INK}" stroke-width=".9"></path>'
            f'<path d="M{f(x + 20)} {f(base - 34)} v12 M{f(x + 60)} {f(base - 34)} v12" stroke="{INK}" stroke-width="1.6"></path>')'''),
])
print("patched")
