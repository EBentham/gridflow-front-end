"""Write A-notes.md: the report (notes_head.md) plus every visible copy line of each board, verbatim, extracted from
the final static pages (block text inside <main>, drawing labels, and the aria-labels of the drawings and charts)."""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
BLOCK = {"h1", "h2", "h3", "p", "li", "dt", "dd", "figcaption", "caption", "th", "td"}
PAGES = ["A-data-sources", "A-vendor-elexon", "A-architecture", "A-models"]


class Grab(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_main = 0
        self.stack: list[list[str]] = []
        self.lines: list[str] = []
        self.labels: list[str] = []
        self.arias: list[str] = []
        self.in_text = False
        self.buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "svg" and a.get("role") == "img" and a.get("aria-label"):
            self.arias.append(a["aria-label"])
        if tag == "main":
            self.in_main += 1
        if tag == "text":
            self.in_text, self.buf = True, ""
        if self.in_main and tag in BLOCK:
            self.stack.append([tag, ""])
        elif self.stack and self.stack[-1][0] == "li" and (tag == "span" or a.get("class") == "p"):
            self.stack[-1][1] += " | "

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main -= 1
        if tag == "text" and self.in_text:
            self.in_text = False
            if self.buf.strip():
                self.labels.append(self.buf.strip())
        if self.in_main and tag in BLOCK and self.stack:
            t, s = self.stack.pop()
            s = re.sub(r"\s+", " ", s).strip()
            if s:
                self.lines.append(s)

    def handle_data(self, data):
        if self.in_text:
            self.buf += data
        if self.stack:
            self.stack[-1][1] += data


def copy_of(name: str) -> tuple[list[str], list[str], list[str]]:
    g = Grab()
    g.feed((HERE / "static" / f"{name}.html").read_text(encoding="utf-8"))
    out = list(g.lines)
    labs = []
    for s in g.labels:
        if s not in labs and not re.fullmatch(r"[-\d,.\s]+|GBP/MWh|MW|MW, UTC", s):
            labs.append(s)
    return out, labs, g.arias


def main() -> None:
    head = (HERE / "notes_head.md").read_text(encoding="utf-8")
    parts = [head, "\n## Every copy line on the boards, verbatim\n",
             "Extracted from the final static pages. Dataset keys, paths, model ids, numbers and the pack's own "
             "one-liners (vendor code descriptions, CLI lines) are facts from the pack; everything else is NEW COPY "
             "for approval.\n"]
    for n in PAGES:
        lines, labs, arias = copy_of(n)
        parts.append(f"\n### {n}\n")
        parts += [f"- {s}" for s in lines]
        parts.append("\nDrawing and chart labels: " + "; ".join(labs) + "\n")
        parts.append("Alt text (aria-label) of drawings and charts:\n")
        parts += [f"- {a}" for a in arias]
    (HERE / "A-notes.md").write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(sum(1 for _ in (HERE / "A-notes.md").read_text(encoding="utf-8").splitlines()), "lines")


if __name__ == "__main__":
    main()
