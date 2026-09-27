"""WCAG 2.x contrast for every text/background pair the homepage uses (CSS and SVG labels)."""
from __future__ import annotations

T = {
    "petrol": "#155A6E", "daylight": "#F6F4EC", "topsoil": "#ECE8DA", "zebra": "#EFEBDF", "ink": "#1C2B22",
    "ink-2": "#3F4A3B", "muted": "#5d6a55", "on-petrol": "#F6F4EC", "on-petrol-2": "#CFE0DC",
    "on-petrol-3": "#B4D0CD", "chartreuse": "#AFC64E", "chartreuse-hi": "#C3D86A", "clay": "#C77E3C",
    "khaki": "#A39A6A", "clay-deep": "#7C5530", "bronze-tint": "#E2CDB3", "silver-tint": "#DCE2DF",
    "gold-tint": "#E9DDAF", "horizon": "#3E8C97",
}


def rgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def mix(a: str, b: str, t: float) -> str:
    """b over a at opacity t."""
    ra, rb = rgb(a), rgb(b)
    return "#" + "".join(f"{round((x * (1 - t) + y * t) * 255):02X}" for x, y in zip(ra, rb))


def lum(h: str) -> float:
    def ch(c: float) -> float:
        return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb(h))
    return .2126 * r + .7152 * g + .0722 * b


def ratio(fg: str, bg: str) -> float:
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + .05) / (b + .05)


# Textures darken a ground slightly; the worst case is the texture colour at its opacity over the full cell,
# which overstates it (the marks cover a small part of each tile), so these are conservative.
SEA = mix(T["horizon"], T["daylight"], .13)
PAIRS = [
    ("hero h1, keys, nav current, about name", "on-petrol", "petrol"),
    ("lede, nav links, keys p, about body, skills dd, footer links", "on-petrol-2", "petrol"),
    ("scope line, about role, footer line", "on-petrol-3", "petrol"),
    ("notebook kernel name on the ink tab bar", "on-petrol-2", "ink"),
    ("primary button", "ink", "chartreuse"),
    ("primary button, hover", "ink", "chartreuse-hi"),
    ("text on topsoil", "ink", "topsoil"),
    ("secondary text on topsoil", "ink-2", "topsoil"),
    ("model ids / help-card heads on topsoil", "petrol", "topsoil"),
    ("text on bronze", "ink", "bronze-tint"),
    ("secondary text on bronze", "ink-2", "bronze-tint"),
    ("text on silver", "ink", "silver-tint"),
    ("secondary text on silver", "ink-2", "silver-tint"),
    ("text on gold", "ink", "gold-tint"),
    ("secondary text on gold", "ink-2", "gold-tint"),
    ("notebook text on daylight", "ink", "daylight"),
    ("help-card footer on daylight", "ink-2", "daylight"),
    ("help-card verbs on daylight", "petrol", "daylight"),
    ("help-card verbs on zebra rows", "petrol", "zebra"),
    ("DataFrame / help text on zebra", "ink", "zebra"),
    ("In [n] prompts on daylight", "muted", "daylight"),
    ("string literals in input wells", "clay-deep", "topsoil"),
    ("keywords in input wells", "petrol", "topsoil"),
    ("selected completion", "daylight", "ink"),
    ("SVG: light landscape labels on their petrol halo", "on-petrol", "petrol"),
    ("SVG: ink labels on the energised land", "ink", "chartreuse"),
    ("SVG: interconnector label over the sea", "ink", SEA),
    ("SVG: core / drawing labels on topsoil", "ink", "topsoil"),
    ("SVG: core scale ticks on topsoil", "ink-2", "topsoil"),
    ("SVG: Nuclear label on its petrol block", "daylight", "petrol"),
    ("SVG: CCGT / OCGT labels on their clay knock-out", "ink", "clay"),
    ("SVG: Coal label on khaki (hatch at 35%)", "ink", mix(T["khaki"], T["ink"], .35 * .127)),
    ("SVG: plot ticks on daylight", "ink", "daylight"),
]

TEXTURED = [("topsoil", "khaki", .5 * .05), ("bronze-tint", "clay-deep", .15 * .2), ("silver-tint", "#5E6E6B", .22 * .2),
            ("gold-tint", "#8A6F1E", .26 * .07)]

if __name__ == "__main__":
    worst = 99.0
    for name, fg, bg in PAIRS:
        f = T.get(fg, fg)
        b = T.get(bg, bg)
        r = ratio(f, b)
        worst = min(worst, r)
        print(f"{r:5.2f}  {'PASS' if r >= 4.5 else 'FAIL'}  {fg:>12} on {bg:<13} {name}")
    print("-- with texture coverage averaged in (mark area x opacity)")
    for ground, tex, cover in TEXTURED:
        g = mix(T[ground], T.get(tex, tex), cover)
        for fg in ("ink", "ink-2"):
            r = ratio(T[fg], g)
            worst = min(worst, r)
            print(f"{r:5.2f}  {'PASS' if r >= 4.5 else 'FAIL'}  {fg:>12} on textured {ground}")
    print(f"worst {worst:.2f}")
