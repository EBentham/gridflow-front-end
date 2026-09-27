import json, re, shutil, datetime, pathlib
root = pathlib.Path("canvas/project")
specs = ["fuelhh", "system-prices", "physical-flows", "bmunits-reference"]
names = {"A": "A: The section", "B": "B: Reference manual", "C": "C: The plate", "D": "D: Notebook first", "E": "E: Datasheet"}
models = {
"A": "CONTENT MODEL (A)\nSky: breadcrumb; name (5 words); key + vendor code (16); one-liner (18); facts grain, cadence, units, history, lag (14 each); asset strip.\nTopsoil: chart heading (10); caption with dataset, unit, aggregation, sign rule (40); chart + key; What it is (60); How it's used 2-3 x 14.\nBronze: note (30), vendor request, gridflow commands.\nSilver: relation + schema class (25); schema (14 per meaning); sample DataFrame.\nGold: note (35); notebook with the exact call.\nDeep: caveats up to 3 x 25; related up to 4 x 12; footer.\nStratum margin labels (6 words).",
"B": "CONTENT MODEL (B)\nBand: breadcrumb; mono key; vendor code + name; title (5); one-liner (20).\nFact rail, stays level (20 per value): grain, cadence, history with coverage strip, lag, units, rows, silver table, workbench call.\nChart + key + caption (60).\nWhat it is (60). How it's used 3 x 16. Caveats 3 x 30 (above schema).\nReference rows: schema (lineage folded), sample rows, how to get it (notebook cells, endpoint, CLI), related.\nDeep footer.\nAuth dropped: not established.",
"C": "CONTENT MODEL (C)\nSky: vendor back-link; h1 (6); id line; one-liner (25).\nPlate (first screen, full width): title (9); note with dataset, unit, window, aggregation (55); labels on the series.\nWhat it is (60). How it's used 3 x 18.\nFacts 6 pairs x 15 ('not established' printed). Caveats up to 3 x 40, beside facts.\nBronze: raw endpoint + CLI. Silver: schema (15 per row) + sample rows. Gold: workbench call (40).\nDeep: related, footer.\nPhone needs its own plate (labels to a list).",
"D": "CONTENT MODEL (D)\nHero: breadcrumb; name (5); code + key; one-liner (20).\nAnnotated notebook, notes level with cells:\n[1] exact call + one proven check, beside What it is (60).\n[2] rows = the sample, beside Facts: grain, cadence, stored, published, units (15 each).\nfuelhh only: band-mapping cell + note (60).\nChart cell, beside caption (50) + 3 caveats x 35.\nHow it's used 3 x 20. Schema card (12 per column, outside the notebook). Endpoint + CLI (25). Related up to 4 x 12. Footer.",
"E": "CONTENT MODEL (E)\nFirst screen (ends by ~890 px): breadcrumb; title (6); key; one-liner (20).\nFigure in a fixed 800x272 frame: title (10), caption (40).\nKey facts: same 7 rows every page (8 words each; 'not established' kept).\nHow to get it: workbench call, silver relation, vendor endpoint (16 each), keyed gold/silver/bronze.\nBelow the fold, strict order: What it is (60); How it's used 3 x (4 + 16); schema (lineage grouped); sample (8 rows x 7 cols); caveats up to 3 x 32; related up to 4 x 12.\nCLI cut (belongs on the vendor page).",
}
boards, order, notes = {}, [], {}
y = 0
for L in "ABCDE":
    hs = []
    for i, s in enumerate(specs):
        fn = f"{L}-{s}.dc.html"
        src = pathlib.Path(L) / fn
        shutil.copy(src, root / fn)
        h = int(re.search(r'"\$preview":\{"width":1440,"height":(\d+)\}', src.read_text(encoding="utf-8")).group(1))
        hs.append(h)
        boards[fn] = {"x": i * 1520, "y": y, "w": 1440, "h": h, "title": f"{L} {s}"}
        order.append(fn)
    notes[f"t{L}"] = {"x": 0, "y": y - 300, "text": names[L], "kind": "title1", "maxW": 5920}
    notes[f"m{L}"] = {"x": -800, "y": y, "text": models[L], "w": 680, "maxH": 1400, "size": "m", "fill": "teal"}
    y += max(hs) + 520
notes["intro"] = {"x": -800, "y": -1100, "w": 680, "maxH": 700, "size": "m", "fill": "yellow" if False else "orange",
 "text": "Round 1 of the dataset page (no picks made). Five directions, each rendered for the same four specimens: elexon/fuelhh, elexon/system_prices, entsog/physical_flows, elexon/bmunits_reference. Every fact comes from one verified pack (silver as of 2026-09-27). Each row's sticky holds its content model and word budgets. All prose on the boards is new copy awaiting approval."}
canvas = {"v": 3, "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
 "title": "v5 dataset page loop", "launch": {"view": "canvas"}, "pages": [], "boards": boards, "order": order, "notes": notes, "designSystems": []}
(root / "canvas.json").write_text(json.dumps(canvas, indent=1), encoding="utf-8")
print(len(boards), y)
