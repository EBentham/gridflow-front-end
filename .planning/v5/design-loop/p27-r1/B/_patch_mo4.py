from pathlib import Path
p = Path(__file__).parent / "b_mo.py"
s = p.read_text(encoding="utf-8")
a = s.index("    for k in (WET + 1, WET + 2, WET + 3):")
b = s.index("    # residual demand: the span of the fill")
s = s[:a] + "\n" + s[b:]
s = s.replace("# the dry tail carries plant: a gas station on the first dry terrace, small peaking units above",
              "# the first dry terrace carries a gas station, wired to the line of pylons")
s = s.replace('with gas plant on "\n            "the dearer terraces and', 'with a gas station on "\n            "the first dry terrace and')
p.write_text(s, encoding="utf-8")
print("ok")
