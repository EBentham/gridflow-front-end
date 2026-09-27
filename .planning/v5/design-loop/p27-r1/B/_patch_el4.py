s = open("b_el.py", encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
rep('''        rows.append(f'<tr class="gh" id="g-{k}"><td colspan="5">''', '''        rows.append(f'<tr class="gh" id="g-{k}"><td colspan="4">''')
rep('''                        f'<td class="m">{ONE_LINE[key]}</td><td>{QUERY[d["param_style"]]}</td>'
                        f'<td class="n">{held_from(d)}</td></tr>')''',
    '''                        f'<td class="m">{ONE_LINE[key]}</td><td class="n">{held_from(d)}</td></tr>')''')
rep('''            f'<th scope="col">BMRS code or path</th><th scope="col">What it holds</th><th scope="col">Queried by</th>'
            f'<th scope="col" class="n">In the store from</th></tr></thead>''',
    '''            f'<th scope="col">BMRS code or path</th><th scope="col">What it holds</th>'
            f'<th scope="col" class="n">In the store from</th></tr></thead>''')
rep('''<p>Grouped as in the drawing above. Six datasets reach back to September 2021 in the store; most of '
           f'the rest start in August 2026.</p>''',
    '''<p>Grouped as in the drawing above. Each is queried by publish time, except <code>system_prices</code> '
           f'and <code>market_depth</code> (by settlement date), <code>pn</code> (by settlement date and period) and '
           f'<code>bmunits_reference</code> (no parameters).</p>''')
rep('.el-tl td.m{width:48%}', '.el-tl td.k{width:190px}\n.el-tl td.c{width:330px}\n.el-tl td.n{width:150px}\n.tl-head p code{font-size:13px;color:#1C2B22}')
rep('TABLE_H = 150 + 58 + N_ROWS * 45 + len(GROUPS) * 64 + 90', 'TABLE_H = 160 + 50 + N_ROWS * 45 + len(GROUPS) * 63 + 96')
open("b_el.py", "w", encoding="utf-8").write(s)
print("ok")
