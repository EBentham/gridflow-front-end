from pathlib import Path

p = Path(__file__).parent / "b_ar.py"
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('M616 {f(by)} V{f(by + 7)}" ', 'M770 {f(by)} V{f(by + 7)}" ')
rep('''labels.append(f'<text class="mono sm" x="626" y="{f(by + 17)}">silver_neso_carbon_intensity</text>')''',
    '''labels.append(f'<text class="mono sm" x="780" y="{f(by + 17)}">silver_neso_carbon_intensity</text>')''')
a = s.index('    aria = ("A cutaway of gridflow')
b = s.index('    svg = (f\'<svg class="draw ar-draw"')
s = s[:a] + '''    aria = ("A cutaway of gridflow's store. Feed cables come down from the landscape through the topsoil and end at "
            "rings at the top of bronze. Bronze is a stack of thin daily beds, the newest on top, each holding raw "
            "response bodies with a small sidecar beside each one. Below it, silver is five beds of columnar rock, one "
            "per dataset directory: Elexon fuelhh, ENTSO-E day-ahead prices, Elexon system prices (laminated with "
            "vintages), NESO carbon intensity and Elexon MID. Each column is one daily Parquet file and a dashed joint "
            "separates the months. A bracket under the carbon-intensity bed marks one view over a directory. Gold veins "
            "rise from the system-price and carbon-intensity beds and join as one view; a second vein rises from the MID "
            "bed. At the bottom, gold ingots lie in five piles, one per model-output table.")
''' + s[b:]
p.write_text(s, encoding="utf-8")
print("ok")
