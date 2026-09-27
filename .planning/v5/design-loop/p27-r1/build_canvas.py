import json, re, shutil, datetime, pathlib
root = pathlib.Path("canvas/project")
pages = ["data-sources", "vendor-elexon", "architecture", "models"]
names = {"A": "A: Sections", "B": "B: Keyed atlas", "C": "C: Field guide", "D": "D: From the workbench", "E": "E: Survey sheets"}
ideas = {
"A": "A: Sections\nEach top page is its own geological section under the homepage sky; a cable runs from each drawn asset down through the strata to the entry it feeds. Data sources: a west-to-east section through GB, the North Sea and the continent, vendors staggered along their cables in bronze. Architecture: four feeds spliced into one trunk, real paths per layer, build and gates in the deep. Models: input taps in silver, the five models in gold.",
"B": "B: Keyed atlas\nOne large drawing of the real system per page, with a narrow keyed index whose marks are copied from the parts they name and set level with them. Data sources: Ireland to the Continent keyed to 7 vendors. Elexon: a GB panorama keyed to 5 groups, then all 33 listed. Architecture: a cutaway of the store keyed to 10 paths and commands. Models: the merit order as terraces flooded by residual demand.",
"C": "C: Field guide\nTypographic reference docs: entries set like species accounts and dense ruled table lists carry the identity; drawing held to a shallow horizon strip and one plate per page. Data sources: seven vendor accounts, the dataset key in four groups (power, gas, weather, carbon). Architecture: a precise written walk with real names in mono. Models: five entries with target, method, horizon and status as it stands.",
"D": "D: From the workbench\nEach page opens the gridflow-models notebook at the first cell a practitioner would run, with the plain-English account beside it. Data sources: the data handle's help card beside vendor entries. Elexon: data.elexon's card beside the grouped list. Architecture: system_prices followed down the strata, one cell per layer. Models: print(models) and the demand band plot beside five entries.",
"E": "E: Survey sheets\nEvery top page is one survey sheet with the same grounds holding the same blocks: sky (title, answer line), topsoil plate (keyed index + drawing, ends by ~930 px), bronze register, silver specimen, gold (reach it from code, how it is checked), deep (limits, sources). Data sources plate: one day cut at each vendor's publication grain.",
}
boards, order, notes = {}, [], {}
y = 0
for L in "ABCDE":
    hs = []
    for i, s in enumerate(pages):
        fn = f"{L}-{s}.dc.html"
        src = pathlib.Path(L) / fn
        shutil.copy(src, root / fn)
        h = int(re.search(r'"\$preview":\{"width":1440,"height":(\d+)\}', src.read_text(encoding="utf-8")).group(1))
        hs.append(h)
        boards[fn] = {"x": i * 1520, "y": y, "w": 1440, "h": h, "title": f"{L} {s}"}
        order.append(fn)
    notes[f"t{L}"] = {"x": 0, "y": y - 300, "text": names[L], "kind": "title1", "maxW": 5920}
    notes[f"m{L}"] = {"x": -800, "y": y, "text": ideas[L], "w": 680, "maxH": 1200, "size": "m", "fill": "teal"}
    y += max(hs) + 520
notes["intro"] = {"x": -800, "y": -1100, "w": 680, "maxH": 700, "size": "m", "fill": "orange",
 "text": "Round 1 of the top pages (no picks made). Five directions, each drawn for the data-sources landing, the vendor-hub pattern (Elexon), architecture and a five-model landing. Facts come from one verified pack. [N datasets] and [n] are placeholders until the page-set ruling. The Elexon grouping by theme is a proposal. All prose is new copy awaiting approval."}
canvas = {"v": 3, "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
 "title": "v5 top pages loop", "launch": {"view": "canvas"}, "pages": [], "boards": boards, "order": order, "notes": notes, "designSystems": []}
(root / "canvas.json").write_text(json.dumps(canvas, indent=1), encoding="utf-8")
print(len(boards), y)
