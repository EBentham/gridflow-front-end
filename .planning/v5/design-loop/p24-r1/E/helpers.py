"""Load the homepage generator's drawing helpers (gen_a.py up to its variant section) without its data files."""
from __future__ import annotations

import types
from pathlib import Path

R37 = Path(r"C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v4\design-loop\r3-7")
_src = (R37 / "gen_a.py").read_text(encoding="utf-8")
_cut = _src.index("FAN = json.loads")
g = types.ModuleType("gen_home")
g.__file__ = str(R37 / "gen_a.py")
exec(compile(_src[:_cut], str(R37 / "gen_a.py"), "exec"), g.__dict__)
