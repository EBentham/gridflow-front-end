"""Headless-Chrome checks for the C boards: content height, text overflow, margin breaches, SVG label collisions,
wrapped table-list rows, and segment screenshots for review. Usage: python measure.py [shots] [w390]."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ST = HERE / "static"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "http://127.0.0.1:9637/"
PROF = HERE / ".chrome-prof"

JS = r"""
<script>
window.addEventListener('load', () => { document.fonts.ready.then(() => { setTimeout(() => {
  const W390 = location.hash.includes('w390');
  const root = document.querySelector('.root');
  if (W390) { root.style.width = '390px'; }
  const flow = document.querySelector('.flow');
  const out = {content: Math.round(flow.getBoundingClientRect().height), root: root.offsetHeight,
               scrollW: root.scrollWidth, issues: [], wrapped: [], labels: []};
  const rr = root.getBoundingClientRect();
  const lim = W390 ? [16, 374] : [80, 1360];
  const sel = 'p,h1,h2,h3,dt,dd,li>span,td,th,figcaption,pre,label,caption,code,a';
  for (const el of document.querySelectorAll(sel)) {
    if (el.closest('svg')) continue;
    const r = el.getBoundingClientRect();
    if (!r.width) continue;
    if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflow !== 'visible' && el.tagName !== 'CODE')
      out.issues.push(['clip', el.tagName, el.className, (el.textContent||'').slice(0,50)]);
    if (r.left - rr.left < lim[0] - 1 || r.right - rr.left > lim[1] + 1)
      out.issues.push(['margin', el.tagName, el.className, Math.round(r.left - rr.left), Math.round(r.right - rr.left), (el.textContent||'').slice(0,50)]);
  }
  for (const li of document.querySelectorAll('.tl li')) {
    const h = li.getBoundingClientRect().height;
    if (h > 46) out.wrapped.push([Math.round(h), (li.textContent||'').slice(0,70)]);
  }
  for (const svg of document.querySelectorAll('svg[role="img"]')) {
    const ts = [...svg.querySelectorAll('text')].map(t => [t.getBoundingClientRect(), t.textContent]);
    const sr = svg.getBoundingClientRect();
    for (let i = 0; i < ts.length; i++) {
      const [a, at] = ts[i];
      if (a.left < sr.left - 1 || a.right > sr.right + 1 || a.top < sr.top - 1 || a.bottom > sr.bottom + 1)
        out.labels.push(['outside', at]);
      for (let j = i + 1; j < ts.length; j++) {
        const [b, bt] = ts[j];
        if (a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1)
          out.labels.push(['overlap', at, bt]);
      }
    }
  }
  const pre = document.createElement('pre'); pre.id = 'measure'; pre.textContent = JSON.stringify(out);
  document.body.appendChild(pre);
}, 400); }); });
</script>
"""

SHIFT = r"""
<script>
window.addEventListener('load', () => { const m = location.hash.match(/y(\d+)/);
  if (m) document.querySelector('.root').style.marginTop = (-parseInt(m[1])) + 'px'; });
</script>
"""


def chrome(args: list[str]) -> str:
    base = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={PROF}",
            "--virtual-time-budget=6000", "--run-all-compositor-stages-before-draw"]
    r = subprocess.run(base + args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    return r.stdout


def measure(slug: str, w390: bool = False) -> dict:
    src = (ST / f"C-{slug}.html").read_text(encoding="utf-8")
    (ST / f"_m_{slug}.html").write_text(src.replace("</body>", JS + "</body>"), encoding="utf-8")
    url = BASE + f"_m_{slug}.html" + ("#w390" if w390 else "")
    dom = chrome(["--window-size=1440,1000" if not w390 else "--window-size=390,900", "--dump-dom", url])
    m = re.search(r'<pre id="measure">(.*?)</pre>', dom, re.S)
    return json.loads(m.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")) if m else {"err": dom[-400:]}


def shots(slug: str, height: int, step: int = 1400) -> list[str]:
    src = (ST / f"C-{slug}.html").read_text(encoding="utf-8")
    (ST / f"_s_{slug}.html").write_text(src.replace("</body>", SHIFT + "</body>"), encoding="utf-8")
    outs = []
    y = 0
    while y < height:
        png = HERE / "shots" / f"{slug}-{y:04d}.png"
        png.parent.mkdir(exist_ok=True)
        chrome([f"--screenshot={png}", f"--window-size=1440,{step}", BASE + f"_s_{slug}.html#y{y}"])
        outs.append(str(png))
        y += step
    return outs


if __name__ == "__main__":
    slugs = ["data-sources", "vendor-elexon", "architecture", "models"]
    res = {}
    for s in slugs:
        res[s] = measure(s, "w390" in sys.argv)
        r = res[s]
        print(s, "content", r.get("content"), "root", r.get("root"), "scrollW", r.get("scrollW"),
              "issues", len(r.get("issues", [])), "wrapped", len(r.get("wrapped", [])), "labels", len(r.get("labels", [])))
        for i in r.get("issues", [])[:12]:
            print("   ", i)
        for i in r.get("wrapped", [])[:40]:
            print("    wrap", i)
        for i in r.get("labels", [])[:12]:
            print("    lab", i)
        if "err" in r:
            print(r["err"])
    if "heights" in sys.argv:
        (HERE / "heights.json").write_text(json.dumps({s: res[s]["content"] for s in slugs}), encoding="utf-8")
        print("heights.json written")
    if "shots" in sys.argv:
        for s in slugs:
            print(shots(s, res[s]["content"]))
