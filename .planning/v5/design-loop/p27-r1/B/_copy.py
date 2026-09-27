"""Extract every visible copy line from the four static boards, verbatim, for the notes (a helper, not a deliverable)."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
BLOCK = {"h1", "h2", "h3", "p", "li", "td", "th", "figcaption", "text", "pre", "dt", "dd", "a", "span"}


class P(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.out: list[str] = []
        self.buf: list[str] = []
        self.skip = 0
        self.in_main = False

    def flush(self) -> None:
        t = " ".join("".join(self.buf).split())
        if t:
            self.out.append(t)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in ("span", "br", "code"):
            self.buf.append(" " if tag != "code" else "")
        if tag == "main":
            self.in_main = True
        if tag in ("style", "script", "title"):
            self.skip += 1
        if tag in ("h1", "h2", "h3", "p", "li", "td", "th", "figcaption", "text", "pre", "dt", "dd", "tr"):
            self.flush()

    def handle_endtag(self, tag):
        if tag in ("style", "script", "title"):
            self.skip -= 1
        if tag in ("h1", "h2", "h3", "p", "li", "td", "th", "figcaption", "text", "pre", "dt", "dd", "tr"):
            self.flush()
        if tag == "main":
            self.flush()
            self.in_main = False

    def handle_data(self, data):
        if self.skip or not self.in_main:
            return
        self.buf.append(data)


def lines(name: str) -> list[str]:
    p = P()
    p.feed((HERE / "static" / f"{name}.html").read_text(encoding="utf-8"))
    p.flush()
    seen, out = set(), []
    for t in p.out:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


if __name__ == "__main__":
    parts = []
    for n in ["B-data-sources", "B-vendor-elexon", "B-architecture", "B-models"]:
        parts.append(f"\n### {n}\n")
        parts += [f"- {t}" for t in lines(n)]
    (HERE / "_copy.txt").write_text("\n".join(parts), encoding="utf-8")
    print(sum(1 for x in parts if x.startswith("- ")), "lines")
