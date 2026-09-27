from pathlib import Path
p = Path(__file__).parent / "gen_C.py"
s = p.read_text(encoding="utf-8")
a = '''def sky_toc(current: str, h1: str, lede: str, items: list[tuple[str, str]]) -> str:
    li = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in items)
    nav = f'<nav class="toc-l" aria-label="On this page"><ol>{li}</ol></nav>'
    return (f'<div class="sky">{mast(current)}<div class="head"><div><h1>{h1}</h1>{nav}</div>'
            f'<div><p class="lede">{lede}</p></div></div>{D.horizon()}</div>')'''
b = '''def sky_toc(current: str, h1: str, lede: str, items: list[tuple[str, str]], right_extra: str = "") -> str:
    li = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in items)
    nav = f'<nav class="toc-l" aria-label="On this page"><ol>{li}</ol></nav>'
    return (f'<div class="sky">{mast(current)}<div class="head"><div><h1>{h1}</h1>{nav}</div>'
            f'<div><p class="lede">{lede}</p>{right_extra}</div></div>{D.horizon()}</div>')'''
assert a in s; s = s.replace(a, b)
a = '''    head = sky("Data sources", "Data sources", lede,
               find("Find a dataset", "A key, a code or a word: fuelhh, INDO, storage", "q-all"))'''
b = '''    head = sky_toc("Data sources", "Data sources", lede,
                   [(f"v-{v[2][0]}", v[1].replace(" Transparency Platform", "")) for v in VENDORS]
                   + [("measure", "By what it measures")],
                   find("Find a dataset", "A key, a code or a word: fuelhh, INDO, storage", "q-all"))'''
assert a in s; s = s.replace(a, b)
a = '''    return (f'<li class="ent v-ent"><div>{D.mark(kind)}'''
b = '''    return (f'<li class="ent v-ent" id="v-{keys[0]}"><div>{D.mark(kind)}'''
assert a in s; s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
print("patched")
