"""Detector dry run: a skeleton board with the chrome and the main CSS patterns, before any content."""
from __future__ import annotations

import re
import sys
from pathlib import Path



from helpers import g

HERE = Path(__file__).parent
CSS = """body{margin:0}
.root{background:#155A6E;color:#1C2B22;font:400 16px/1.6 "Hanken Grotesk",sans-serif;font-variant-numeric:tabular-nums}
.sky{background:#155A6E;color:#F6F4EC;padding:26px 80px 40px}
.plate{background:#ECE8DA;padding:40px 80px}
.plate h2{font-family:"Bricolage Grotesque",sans-serif;font-size:22px;font-weight:700;font-stretch:90%;margin:0 0 12px}
.facts{display:grid;grid-template-columns:150px minmax(0,1fr);margin:0}
.facts dt,.facts dd{margin:0;padding:9px 0;border-top:1px solid rgba(28,43,34,.22)}
.well{background:#F6F4EC;border:1px solid #1C2B22;border-radius:3px;padding:8px 12px;font:400 14px/1.6 "Red Hat Mono",monospace}
"""
body = f"""<div class="sky"><header class="mast"><a class="brand" href="#">gridflow</a></header>
<h1>Generation outturn by fuel type</h1><p>Half-hourly GB generation outturn in MW.</p></div>
<main><section class="plate" aria-labelledby="kf"><h2 id="kf">Key facts</h2>
<dl class="facts"><dt>Grain</dt><dd>one row per settlement period and fuel code</dd><dt>Cadence</dt><dd>every 30 minutes</dd></dl>
<pre class="well">data.elexon.query("fuelhh", "2026-09-20", "2026-09-26")</pre></section></main>"""
out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Skeleton</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{g.FONTS}
<style>
{CSS}</style>
</helmet>
<div class="root" style="width: 1440px; height: 900px; overflow: hidden; position: relative">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":900}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""
(HERE / "static").mkdir(exist_ok=True)
(HERE / "static" / "skel.html").write_text(g.static(out), encoding="utf-8")
print("ok")
