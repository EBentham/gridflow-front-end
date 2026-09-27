"""Writes C-notes.md. The NEW COPY section is extracted from the rendered static pages, so it is verbatim."""
from __future__ import annotations

import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
H = json.loads((HERE / "heights.json").read_text(encoding="utf-8"))
BLOCK = {"h1", "h2", "h3", "p", "dt", "dd", "li", "figcaption", "caption", "th", "td", "text", "label", "pre", "span"}


class Copy(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.buf: list[str] = []
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        a = dict(attrs)
        if tag in ("style", "script", "header", "footer") or a.get("class") in ("mast", "footing") or \
                (tag == "nav" and a.get("aria-label") in ("Primary", "Sections of the site")):
            self.skip += 1
            self.stack.append("#skip")
            return
        if tag == "input" and a.get("placeholder"):
            self.out.append(f"(search placeholder) {a['placeholder']}")
        if tag in ("li", "tr", "div") and self.buf:
            self.flush()
        self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        while self.stack:
            t = self.stack.pop()
            if t == "#skip":
                self.skip -= 1
                break
            if t == tag:
                break
        if tag in BLOCK - {"span"} or tag in ("tr", "li"):
            self.flush()

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.buf.append(data)

    def flush(self) -> None:
        t = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = []
        if t and (not self.out or self.out[-1] != t):
            self.out.append(t)


def copy_of(slug: str) -> list[str]:
    s = (HERE / "static" / f"C-{slug}.html").read_text(encoding="utf-8")
    s = s.split("<main>", 1)[0].split('<div class="sky">', 1)[1] + "<main>" + s.split("<main>", 1)[1]
    s = re.sub(r"<svg class=\"(mk|horizon|band-bg|sw)\".*?</svg>", "", s, flags=re.S)
    s = s.split('<nav class="footing"')[0]
    c = Copy()
    c.feed(s)
    c.flush()
    return [html.unescape(x) for x in c.out]


HEAD = f"""claude-opus-5-5

# Designer C, "The field guide": Phase 27 round 1 notes

## Boards (this folder; generator gen_C.py + draw_c.py + c.css; static copies in static\\; checks in measure.py)
- C-data-sources.dc.html, 1440 x {H['data-sources']}
- C-vendor-elexon.dc.html, 1440 x {H['vendor-elexon']}
- C-architecture.dc.html, 1440 x {H['architecture']}
- C-models.dc.html, 1440 x {H['models']}

## The idea
The site read as a field guide: species-account entries and dense ruled table lists carry the identity in type, the drawing
is held to a shallow horizon strip, one small plate per page and a stratified footing, and the footing's three strata are
the site's three sections (bronze = Data sources, silver = Architecture, gold = Models, as on the homepage key).

## Content model (ordered blocks)
- Data sources: sky (h1, on-this-page list of the seven vendors + the measure key, lede with the [N datasets] slot, find
  field) / The seven vendors: seven accounts (drawn identification mark, name, source key(s) in mono, [n] datasets link;
  one-sentence account, four facts Market / Access / Grain / History held, one "Reached at" line) / By what it measures:
  Power, Gas, Weather, Carbon, each a ruled table list (italic sub-label, key, what it holds, vendor) / How the catalogue
  is organised: three plain statements + the system_prices plate / strata footing (bronze current) / deep footer.
- Elexon hub: sky (breadcrumb, h1, field marks Source key / Access / Grain, lede, find field) / Every Elexon dataset:
  arrangement switch + column labels, five groups (head + one-line scope), 33 rows (key, one line, endpoint, held from) /
  About the feed: facts (base URL, connector, rate limit, history), Read before using (four caveats), the FUELHH wind plate
  / footing (bronze current) / footer.
- Architecture: sky (h1, on-this-page list, lede) / In brief: data-root note, six facts, plate "What lands on disk" /
  Bronze, Silver, Gold: swatch + layer name + one line; "Written by gridflow <verb>"; prose with real names; path well;
  sidecar fields or column or view table list; "In the code" references / The catalogue: tables, view names, client /
  Commands: eleven verbs in two ruled lists, quality checks in the margin / The build and the gates: gridflow CI (five),
  this site (four) / What it does not do (six) / footing (silver current) / footer.
- Models: sky (h1, on-this-page list, lede) / Reading the scores: five definitions / The five models: five accounts
  (name, model id(s), workbench handle; Target / Method / Horizon / As it stands); demand carries the plate, the two-run
  score table and the per-fold strip; SMP carries its two backtests and all five required caveats; wind, solar and stack
  carry no score / In the workbench: handles + a four-cell notebook (inputs only) / footing (gold current) / footer.

## Decisions the brief left to me
- Counts: [N datasets] in the landing lede; Elexon prints 33 (the brief and the locked scope fix it); every other vendor
  shows [n]. NESO keeps "in five families" (vault). No group counts on the hub.
- Hub grouping: the pack's thematic grouping (Prices and balancing, Generation and availability, Demand, System
  indicators, Reference and messages). The pack marks it PROPOSED, so it needs Bobbo's OK. The canonical vault grouping
  (by request style: settlement date 7, publish datetime 25, no params 1) is the second option of the visible
  "Arranged by" switch, and the endpoint column shows each row's request path either way. Note the pack's flag: boal,
  disbsad, mid and netbsad sit under settlement-date style in the vault but are publish-datetime in code.
- A vendor with 3 datasets (the NESO Data Portal): the same page, shorter. Sky unchanged (breadcrumb, name, field marks,
  lede); the find field is dropped under about ten rows; the list becomes one ungrouped ruled list with the same row
  anatomy (key, one line, endpoint, held from; here /api/3/action/package_show for all three and "Jan 2009" for the
  generation mix); About the feed keeps facts and caveats (current file only, no backfill) and takes a plate only where a
  deep series exists (historic_generation_mix since 2009 could supply one; none is computed in the pack, so none is
  drawn). GIE, with two source keys, groups its rows by key (AGSI+ storage, ALSI LNG).
- Vendor marks: one drawn asset per vendor, from the homepage's set: pylon (Elexon), converter station (ENTSO-E),
  substation (NESO Data Portal), gas-fired station (NESO Carbon Intensity), a pipeline with a valve (ENTSO-G), storage
  tanks (GIE), met mast (Open-Meteo). Framing only; they imply no dataset.
- Charts: three real series from the pack, each captioned with dataset, unit and window (system_prices daily mean;
  FUELHH WIND monthly mean; demand v1 fold 12 band vs outturn). The SMP series is not drawn; its scores are set as a table
  with every required caveat. Architecture has no chart: its plate is a drawing with no numbers.
- Punctuation: no em dashes; ranges written "2 to 14".

## Verification
- Detector (static copies, from the repo root): [] on all four boards.
- Layout: my Browser-pane tab could not open (tab cap reached by other sessions), so I drove headless Chrome myself
  (measure.py, http.server on port 9637, stopped afterwards). At 1440: content bottom == root height == $preview on all
  four; 0 text blocks clipped or outside the 80 px margins; 0 table-list rows wrapped past 46 px; 0 label collisions or
  labels outside their plate. Segment screenshots reviewed for each board.
- 390 px (root forced to 390): every page collapses to one column with no text past the 16 px gutters; the path wells
  and the two score tables scroll inside themselves.

## Could not do
- The Browser pane itself (tab cap), so no in-pane screenshots; all checks are headless Chrome.
- A phone rendering of the plates beyond scaling: at 390 the plates scale to width and stay legible but small.

## NEW COPY (verbatim, extracted from the rendered pages; facts come from the pack, wording is mine)
"""


def main() -> None:
    parts = [HEAD]
    for slug, name in (("data-sources", "Data sources"), ("vendor-elexon", "Elexon hub"),
                       ("architecture", "Architecture"), ("models", "Models")):
        parts.append(f"\n### {name}\n")
        for line in copy_of(slug):
            parts.append(f"- {line}\n")
    parts.append("\n### Footing (all pages)\n")
    for t, d in (("Data sources", "Every vendor gridflow ingests and every dataset it takes, found by vendor or by what it measures."),
                 ("Architecture", "Bronze, silver and gold on disk, the DuckDB catalogue, the commands, the build and its checks."),
                 ("Models", "Five models that read the warehouse: demand, wind, solar, the merit-order stack and a fundamentals price.")):
        parts.append(f"- {t}: {d}\n")
    (HERE / "C-notes.md").write_text("".join(parts), encoding="utf-8")
    print("notes", sum(len(p) for p in parts))


if __name__ == "__main__":
    main()
