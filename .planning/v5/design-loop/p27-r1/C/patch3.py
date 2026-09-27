from pathlib import Path

HERE = Path(__file__).parent
p = HERE / "gen_C.py"
s = p.read_text(encoding="utf-8")
pairs = [
    ('"Two repositories, two sets of gates. Nothing merges or deploys without them.",',
     '"Two repositories, each with its own checks in GitHub Actions.",'),
    ('("gridflow-build --check", "The rendered pages match their sources, run for run"),',
     '("gridflow-build --check", "A second build changes nothing: the build is idempotent"),'),
    ('("As it stands", "21 validated version-1 builds and one version-2 build in the manifest; walk-forward "\n'
     '                                "backtests in gold; one issued version-2 forecast, 4 to 6 September 2026")',
     '("As it stands", "21 version-1 entries and one version-2 entry in the manifest; walk-forward backtests "\n'
     '                                "in gold; one issued version-2 forecast, 4 to 6 September 2026")'),
    ('"of each calendar month, MW. FUELHH covers transmission-metered generation, so this is not all GB wind.")',
     '"of each calendar month, MW. Transmission-metered output only.")'),
]
for a, b in pairs:
    assert a in s, a[:70]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
print("patched")
