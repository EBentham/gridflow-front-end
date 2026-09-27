s = open("b_ds.py", encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
a = s.index("FAR = [(-10, LV[\"dp\"] + 250)")
b = s.index("NEAR_GB = [")
s = s[:a] + '''FAR = [(-10, LV["dp"] + 84), (90, LV["dp"] + 58), (190, LV["dp"] + 76), (290, LV["dp"] + 52), (376, LV["dp"] + 48),
       (432, LV["dp"] + 44), (488, LV["dp"] + 50), (544, LV["dp"] + 58), (630, LV["dp"] + 104), (720, LV["dp"] + 168),
       (820, LV["dp"] + 246), (900, LV["dp"] + 318), (970, S_L - 40), (1030, S_L)]
MID = [(-10, LV["ci"] + 70), (80, LV["ci"] + 104), (170, LV["ci"] + 74), (250, LV["ci"] + 106), (330, LV["ci"] + 90),
       (420, LV["ci"] + 96), (500, LV["ci"] + 132), (600, LV["ci"] + 176), (700, LV["ci"] + 214), (800, LV["ci"] + 252),
       (900, LV["ci"] + 300), (970, S_L - 30), (1010, S_L)]
''' + s[b:]
rep('NEAR_IE = [(-10, S_L - 34), (60, S_L - 40), (140, S_L - 28), (178, S_L - 6)]',
    'NEAR_IE = [(-10, S_L - 64), (56, S_L - 84), (124, S_L - 56), (160, S_L - 30), (178, S_L - 6)]')
rep('top = " ".join(f"L{f(x)} {f(interp(pts, x) + 2 * math.sin(x / 31))}" for x in xs)',
    'top = " ".join(f"L{f(x)} {f(interp(pts, x) + 5 * math.sin(x / 23 + len(pts)) + 3 * math.sin(x / 9))}" for x in xs)')
rep('bot = [(x, gy + 70 + 6 * math.sin(x / 90 + 1) + 3 * math.sin(x / 31)) for x in range(W + 40, -41, -24)]',
    'bot = [(x, gy + 108 + 6 * math.sin(x / 90 + 1) + 3 * math.sin(x / 31)) for x in range(W + 40, -41, -24)]')
rep('PLATE_H = LV["gie"] + 104', 'PLATE_H = LV["gie"] + 136')
rep('''    pipe = ([(tb_x + 14, tb_base - 2), (tb_x + 40, S_L + 12), (610, S_L + 26), (640, S_L + 36)] +''',
    '''    pipe = ([(tb_x + 14, tb_base - 2), (tb_x + 44, S_L + 8), (612, S_L + 24), (640, S_L + 40)] +''')
open("b_ds.py", "w", encoding="utf-8").write(s)
print("ok")
