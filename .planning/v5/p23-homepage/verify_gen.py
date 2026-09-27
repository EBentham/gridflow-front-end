from __future__ import annotations

import re
import sys

D = r"C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.claude\worktrees\agent-af17b8660dd5506f2\.planning\v4\design-loop"
sys.path[:0] = [D + r"\r3-7", D + r"\r3-6"]
import gen  # noqa: E402
import gen_b  # noqa: E402

ref = open(D + r"\r3-7\R3-final.dc.html", encoding="utf-8").read()


def chk(name: str, s: str) -> None:
    print(name, s in ref, len(s))


chk("landscape", gen.landscape())
chk("labels", gen.land_labels())
chk("core", gen.core_svg())
chk("bdraw", gen_b.drawing())
for k in ["stack", "smp", "resid", "solar", "wind", "demand"]:
    chk("mark " + k, gen_b.mark(k))
for k, v in gen.VENDORS.items():
    chk("spark " + k, gen.spark(v[3], zero=v[9]))
chk("patterns", gen.PATTERNS)
chk("key", gen.key_block().split('style=')[0])
