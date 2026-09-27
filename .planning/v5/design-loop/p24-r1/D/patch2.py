from __future__ import annotations

from pathlib import Path

p = Path(__file__).with_name("gen_d.py")
s = p.read_text(encoding="utf-8")
R = [
    ('''ident=f"Elexon BMRS {code('FUELHH')}, in gridflow as {code('elexon/fuelhh')}.",''',
     '''ident=f"Dataset {code('FUELHH')}, read in gridflow as {code('elexon/fuelhh')}.",'''),
    ('''ident=f"Elexon BMRS system prices ({code('DISEBSP')}), in gridflow as {code('elexon/system_prices')}.",''',
     '''ident=f"Dataset {code('DISEBSP')}, read in gridflow as {code('elexon/system_prices')}.",'''),
    ('''        ident=(f"ENTSOG Transparency Platform {code('operationalData')}, indicator Physical Flow, in gridflow as "
               f"{code('entsog/physical_flows')}."),''',
     '''        ident=(f"ENTSOG {code('operationalData')}, indicator Physical Flow, read in gridflow as "
               f"{code('entsog/physical_flows')}."),'''),
    ('''ident=f"Elexon BMRS {code('/reference/bmunits/all')}, in gridflow as {code('elexon/bmunits_reference')}.",''',
     '''ident=f"Endpoint {code('/reference/bmunits/all')}, read in gridflow as {code('elexon/bmunits_reference')}.",'''),
    ('''            ("What it is", "<p>The price at which imbalances are cashed out in each half-hour settlement period: the "
             "system sell price (SSP) and system buy price (SBP), with the net imbalance volume (NIV) in MWh. SSP has "
             "equalled SBP on every row since September 2021. The query reads a view that keeps the latest publication "
             "per period: 192 rows for four days.</p>"),''',
     '''            ("What it is", "<p>The price at which imbalances are cashed out, per half-hour settlement period: a "
             "system sell price (SSP) and a system buy price (SBP), equal on every row since September 2021, with the "
             "net imbalance volume (NIV) in MWh. Four days come back as 192 rows, one per period.</p>"),'''),
    ('''"£/MWh, no aggregation. SBP is identical, so one line carries both.</p>",''',
     '''"£/MWh, no aggregation.</p>",'''),
]
for a, b in R:
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
print("patched", len(R))
