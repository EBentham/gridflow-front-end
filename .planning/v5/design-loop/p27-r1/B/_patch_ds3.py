s = open("b_ds.py", encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
rep('top = " ".join(f"L{f(x)} {f(interp(pts, x) + 5 * math.sin(x / 23 + len(pts)) + 3 * math.sin(x / 9))}" for x in xs)',
    'top = " ".join(f"L{f(x)} {f(interp(pts, x) + 4 * math.sin(x / 41 + len(pts)) + 1.5 * math.sin(x / 13))}" for x in xs)')
rep('''    g.append(f'<path d="{pd}" stroke="{INK}" stroke-width="8.4" fill="none" stroke-linecap="round"></path>'
             f'<path d="{pd}" stroke="{CLAY}" stroke-width="5.8" fill="none" stroke-linecap="round"></path>')''',
    '''    g.append(f'<path d="{pd}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"></path>'
             f'<path d="{pd}" stroke="{CLAY}" stroke-width="4.6" fill="none" stroke-linecap="round"></path>')''')
open("b_ds.py", "w", encoding="utf-8").write(s)
