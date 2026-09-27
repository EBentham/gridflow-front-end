"""Pull every visible copy line, in document order, out of the four static boards (for the notes' NEW COPY list)."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

E = Path(__file__).resolve().parent.parent
BLOCKS = {"h1", "h2", "h3", "p", "li", "dt", "dd", "figcaption", "caption", "pre", "th", "td", "text"}
SKIP_ROOTS = {"style", "title", "header", "footer"}


class Copy(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.buf: list[list[str]] = []
        self.lines: list[str] = []
        self.skip = 0
        self.aria: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag in SKIP_ROOTS:
            self.skip += 1
        if tag == "svg" and a.get("role") == "img" and a.get("aria-label"):
            self.aria.append(a["aria-label"] or "")
        if tag in BLOCKS:
            self.buf.append([])
        self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_ROOTS:
            self.skip -= 1
        if tag in BLOCKS and self.buf:
            text = " ".join("".join(self.buf.pop()).split())
            if text and not self.skip:
                if self.buf:
                    self.buf[-1].append(text + " ")
                else:
                    self.lines.append(text)
        while self.stack and self.stack.pop() != tag:
            pass

    def handle_data(self, data: str) -> None:
        if self.buf and not self.skip:
            self.buf[-1].append(data)


def dedupe(lines: list[str]) -> list[str]:
    out: list[str] = []
    for ln in lines:
        if ln not in out:
            out.append(ln)
    return out


def main() -> str:
    parts = []
    for name in ("E-data-sources", "E-vendor-elexon", "E-architecture", "E-models"):
        p = Copy()
        p.feed((E / "static" / f"{name}.html").read_text(encoding="utf-8"))
        parts.append(f"### {name}\n")
        parts += [f"- {ln}" for ln in dedupe(p.lines)]
        parts.append("\nDrawing and chart descriptions (aria-label):\n")
        parts += [f"- {a}" for a in p.aria]
        parts.append("")
    return "\n".join(parts)


if __name__ == "__main__":
    (E / "work" / "newcopy.md").write_text(main(), encoding="utf-8")
    print("ok")
