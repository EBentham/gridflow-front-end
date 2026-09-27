from pathlib import Path
p = Path(__file__).parent / "b_mo.py"
s = p.read_text(encoding="utf-8")
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
rep("(560, de + 46), (660, de + 120),\n           (740, de + 300), (800, TOP_Y + 30)]",
    "(560, de + 50), (660, de + 130),\n           (770, de + 360), (880, TOP_Y + 6)]")
rep("[(800, so + 60), (812, TOP_Y + 16)]", "[(830, so + 70), (900, TOP_Y + 6)]")
rep("top = smooth(mid[5:11])", "top = smooth(mid[5:10])")
rep("for x, y in reversed(mid[5:11])", "for x, y in reversed(mid[5:10])")
p.write_text(s, encoding="utf-8")
print("ok")
