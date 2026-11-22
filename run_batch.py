import glob, json, os, sys, time
from extractor import extract
from validator import validate

version = sys.argv[1] if len(sys.argv) > 1 else "v1"
target_image = sys.argv[2] if len(sys.argv) > 2 else None
out_dir = os.path.join("results", version)
os.makedirs(out_dir, exist_ok=True)

if target_image:
    images = sorted(glob.glob(f"samples/{target_image}.*"))
else:
    images = sorted(glob.glob("samples/*.jpg") + glob.glob("samples/*.png"))
rows = []
for path in images:
    name = os.path.splitext(os.path.basename(path))[0]
    t = time.time()
    try:
        r = extract(path, version=version)
        v = validate(r)
        out = {"image": path, "prompt_version": version,
               "extraction": r.model_dump(), "validation": v}
        rows.append([name, r.document_type, r.merchant, r.currency, r.total,
                     v["status"], "; ".join(v["issues"]) or "-",
                     ", ".join(r.uncertain_fields) or "-", f"{time.time()-t:.1f}"])
    except Exception as e:
        out = {"image": path, "prompt_version": version, "error": str(e)}
        rows.append([name, "ERROR", "-", "-", "-", "error", str(e)[:80], "-", f"{time.time()-t:.1f}"])
    with open(os.path.join(out_dir, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(name, "->", rows[-1][5])
    time.sleep(2)

if not target_image:
    head = ["Image", "Type", "Merchant", "Currency", "Total", "Status", "Issues", "Uncertain", "Sec"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    with open(os.path.join(out_dir, f"summary_{version}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
