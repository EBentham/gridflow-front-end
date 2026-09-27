from pathlib import Path

p = Path(__file__).parent / "b_ar.py"
s = p.read_text(encoding="utf-8")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


a = s.index('L["in"] = C_B + 46')
b = s.index("CAT_H = 700")
s = s[:a] + '''L["in"] = C_B + 46               # cable rings: gridflow ingest
L["bo"] = L["in"] + 144          # a response body (entry spacing = measured entry height + 26)
L["sc"] = L["bo"] + 182          # its sidecar
C_S = L["sc"] + 166              # bronze / silver
L["tr"] = C_S                    # gridflow transform, on the contact
L["fi"] = L["tr"] + 166          # bed A: a Parquet file
L["vi"] = L["fi"] + 184          # bed B: vintages
ROW_C = L["vi"] + 104
L["vw"] = ROW_C + 59             # the view bracket under bed C
C_G = L["vw"] + 144              # silver / gold
L["bu"] = C_G                    # gridflow build, on the contact
L["sq"] = L["bu"] + 144          # the SQL view veins meet
L["mo"] = L["sq"] + 204          # model-output ingots
PLATE_H = L["mo"] + 190
''' + s[b:]
rep('ROW = {"A": L["fi"], "B": L["vi"], "C": L["vw"] - 66, "D": L["vw"] + 62}',
    'ROW = {"A": L["fi"], "A2": L["fi"] + 92, "B": L["vi"], "C": ROW_C, "D": L["vw"] + 62}')
# names to the left in two lines; month labels only above the first bed
rep('''def bed(y: float, name: str, x0: float, x1: float, seed: int, stripes: int = 0, months=("08", "09"),
        h: float = BLOCK_H) -> str:''',
    '''def bed(y: float, name: str, x0: float, x1: float, seed: int, stripes: int = 0, months=("08", "09"),
        h: float = BLOCK_H, head: bool = False) -> str:''')
rep('''        out.append(f'<text class="mono sm" x="{f(start)}" y="{f(bot(start) + 17)}">month={m}/</text>')''',
    '''        if head:
            out.append(f'<text class="mono sm" x="{f(start)}" y="{f(top(start) - 12)}">year=2026/month={m}/</text>')''')
rep('''    out.insert(0, f'<text class="mono" x="{f(x0)}" y="{f(top(x0) - 10)}">{name}</text>')''',
    '''    src, ds = name.split("/")[0] + "/", name.split("/")[1] + "/"
    out.insert(0, f'<text class="mono" x="{f(x0 - 14)}" y="{f(y - 4)}" text-anchor="end">{src}</text>'
                  f'<text class="mono" x="{f(x0 - 14)}" y="{f(y + 13)}" text-anchor="end">{ds}</text>')''')
rep('''    g.append(bed(ROW["A"], "elexon/fuelhh/", 250, 962, 1))
    g.append(bed(ROW["B"], "elexon/system_prices/", 250, 962, 2, stripes=4))
    g.append(bed(ROW["C"], "neso/carbon_intensity/", 250, 962, 3))
    g.append(bed(ROW["D"], "elexon/mid/", 250, 962, 4))
    bx0, bx1 = 250, 962''',
    '''    g.append(bed(ROW["A"], "elexon/fuelhh/", 270, 962, 1, head=True))
    g.append(bed(ROW["A2"], "entsoe/day_ahead_prices/", 270, 962, 5))
    g.append(bed(ROW["B"], "elexon/system_prices/", 270, 962, 2, stripes=4))
    g.append(bed(ROW["C"], "neso/carbon_intensity/", 270, 962, 3))
    g.append(bed(ROW["D"], "elexon/mid/", 270, 962, 4))
    bx0, bx1 = 270, 962''')
rep('''    by = ROW["C"] + BLOCK_H / 2 + 28''', '''    by = L["vw"]''')
rep('''M606 {f(by)} V{f(by + 7)}" ''', '''M616 {f(by)} V{f(by + 7)}" ''')
rep('''    labels.append(f'<text class="mono sm" x="616" y="{f(by + 18)}">silver_neso_carbon_intensity</text>')''',
    '''    labels.append(f'<text class="mono sm" x="626" y="{f(by + 17)}">silver_neso_carbon_intensity</text>')''')
# veins: start in the beds they read, with the new geometry
rep('''    g.append(vein([(452, ROW["B"] + BLOCK_H / 2 - 4), (446, ROW["C"] + 6), (470, ROW["D"] - 20), (500, ROW["D"] + 40),
                   (570, C_G + 36), (680, jy - 34), (jx, jy)], 2.5, 12, 1))
    g.append(vein([(690, ROW["C"] + BLOCK_H / 2 - 4), (700, ROW["D"] + 10), (730, C_G + 24), (790, jy - 22), (jx, jy)],
                  2.5, 10, 2))''',
    '''    g.append(vein([(452, ROW["B"] + BLOCK_H / 2 - 4), (444, ROW["C"] + 4), (462, ROW["D"] - 22), (492, ROW["D"] + 38),
                   (560, C_G + 30), (680, jy - 24), (jx, jy)], 2.5, 12, 1))
    g.append(vein([(700, ROW["C"] + BLOCK_H / 2 - 4), (706, L["vw"] + 14), (722, ROW["D"] + 16), (760, C_G + 24),
                   (800, jy - 14), (jx, jy)], 2.5, 10, 2))''')
rep('''    g.append(vein([(330, ROW["D"] + BLOCK_H / 2 - 4), (334, C_G + 20), (300, C_G + 90), (250, C_G + 150)], 2.5, 11, 4))''',
    '''    g.append(vein([(330, ROW["D"] + BLOCK_H / 2 - 4), (336, C_G + 16), (310, C_G + 70), (262, C_G + 118)], 2.5, 11, 4))''')
rep('''    labels.append(f'<text class="mono sm" x="120" y="{f(C_G + 178)}">gold_gb_day_ahead_benchmark</text>')''',
    '''    labels.append(f'<text class="mono sm" x="96" y="{f(C_G + 146)}">gold_gb_day_ahead_benchmark</text>')''')
rep("vintages, NESO carbon intensity and Elexon MID)", "vintages, NESO carbon intensity and Elexon MID, and ENTSO-E day-ahead prices)")
p.write_text(s, encoding="utf-8")
print("ok")
