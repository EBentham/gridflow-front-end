"""Writes A-notes.md from the same content source the boards use, so NEW COPY is verbatim."""
from __future__ import annotations

import json
import re
from pathlib import Path

from content import SPECIMENS

HERE = Path(__file__).parent


def strip(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


H = json.loads((HERE / "heights.json").read_text(encoding="utf-8"))
tot = {k: sum(v.values()) for k, v in H.items()}
L: list[str] = ["claude-opus-5-5", "", "# Designer A, “The section”: notes", ""]
L.append("Boards (1440 wide): " + ", ".join(f"{k}.dc.html {tot[k]} px" for k in tot)
         + ". Generator: gen_A.py + content.py + a.css; static copies in static/.")
L.append((HERE / "notes_head.txt").read_text(encoding="utf-8"))
tmpl = ["The raw feed", "Schema and sample rows", "Query it from a notebook", "What it is", "How it’s used",
        "What to watch for", "Related datasets", "A square marks the columns that identify a row.",
        "bronze, the response as fetched", "silver, typed and validated", "gold, served to the notebook",
        "Added to every row by the silver base transformer", "MIT licence",
        "settlement date; each starts at 23:00 UTC", "gas day, drawn to scale",
        "Relation <relation>, typed by <Class> in <file>; transformer version <v>."]
L += [f"- {t}" for t in tmpl]
for s in SPECIMENS:
    L.append(f"\n{s['key']}:")
    L.append(f"- h1: {s['title']}")
    L.append(f"- identity: {strip(s['code'])}")
    L.append(f"- one-liner: {strip(s['oneliner'])}")
    L += [f"- fact {k}: {v}" for k, v in s["facts"]]
    L.append(f"- chart heading: {s['chart_h2']}")
    L.append(f"- caption: {strip(s['chart_cap'])}")
    L.append(f"- what it is: {strip(s['what'])}")
    L += [f"- use: {strip(u)}" for u in s["uses"]]
    L.append(f"- bronze note: {strip(s['bronze_note'])}")
    L += [f"- command comment: # {m}" for _, m in s["cli"]]
    L += [f"- schema {c}: {strip(m)}" for c, _, m in s["schema"]]
    L.append(f"- sample caption: {s['df_cap']}")
    L.append(f"- gold note: {strip(s['gold_note'])}")
    L += [f"- caveat: {strip(a)} {strip(b)}" for a, b in s["caveats"]]
    L += [f"- related {k}: {strip(b)}" for k, b in s["related"]]
L.append((HERE / "notes_tail.txt").read_text(encoding="utf-8"))
(HERE / "A-notes.md").write_text("\n".join(L), encoding="utf-8")
print("words", len("\n".join(L).split()))
