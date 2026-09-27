s = open("b_ar.py", encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
a = s.index('    m["fi"] = mark_svg(\'<g transform="translate(5 -25)">')
b = s.index('    m["vi"] = mark_svg(')
s = s[:a] + '''    m["fi"] = mark_svg(
        f'<rect x="6" y="1" width="18" height="18" fill="{SILVER}"></rect>'
        f'<rect x="12" y="1" width="6" height="18" fill="#B3BFBD"></rect>'
        f'<path d="M12 2 V19 M18 2 V19" stroke="{SILVER_DEEP}" stroke-width=".8"></path>'
        f'<path d="M6 8 H24 M6 14 H24" stroke="{SILVER_DEEP}" stroke-width=".6" opacity=".55"></path>'
        f'<rect x="6" y="1" width="18" height="18" fill="none" stroke="{INK}" stroke-width="1"></rect>')
''' + s[b:]
rep("land=True, names=True))", "land=True, names=False))")
open("b_ar.py", "w", encoding="utf-8").write(s)
