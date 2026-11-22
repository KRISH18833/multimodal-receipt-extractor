from datetime import datetime
from schema import Receipt

LOW = 0.6
MID = 0.85

def _items_sum(r):
    by_qty, by_line = 0.0, 0.0
    for it in r.items:
        if it.price is None:
            continue
        by_qty += (it.qty if it.qty is not None else 1) * it.price
        by_line += it.price
    return round(by_qty, 2), round(by_line, 2)

def _close(a, b):
    return abs(a - b) <= max(0.05, 0.01 * abs(b))

def validate(r: Receipt) -> dict:
    issues = []
    field_status = {}
    for f, c in r.confidence.model_dump().items():
        v = getattr(r, f)
        if v is None or v == []:
            s = "missing"
        elif c < LOW:
            s = "low"
        elif c < MID:
            s = "medium"
        else:
            s = "high"
        if f in r.uncertain_fields and s == "high":
            s = "medium"
        field_status[f] = s

    if r.document_type == "not_a_document":
        return {"status": "reject", "field_status": field_status,
                "issues": ["Image is not a receipt or invoice."], "items_sum": None}

    if r.total is None:
        issues.append("Total is missing.")

    by_qty, by_line = _items_sum(r)
    candidates = [
        val for val in [
            r.subtotal,
            r.total,
            (round(r.total - r.tax, 2) if r.total is not None and r.tax is not None else None),
        ]
        if val is not None
    ]
    if r.items and candidates:
        if not any(_close(by_qty, c) or _close(by_line, c) for c in candidates):
            issues.append(f"Item sum ({by_qty}) does not match any of: {candidates}")
            field_status["items"] = "low"
            field_status["total"] = "low"

    if r.subtotal is not None and r.tax is not None and r.total is not None and not _close(r.subtotal, r.total):
        if not _close(r.subtotal + r.tax, r.total):
            issues.append("Subtotal + tax does not equal total.")

    if r.date:
        try:
            datetime.strptime(r.date, "%Y-%m-%d")
        except ValueError:
            issues.append(f"Date '{r.date}' is not a valid YYYY-MM-DD date.")
            field_status["date"] = "low"

    low_fields = [f for f, s in field_status.items() if s == "low"]
    if low_fields:
        issues.append("Low confidence fields: " + ", ".join(low_fields))
    if r.uncertain_fields:
        issues.append("Model flagged uncertain: " + ", ".join(r.uncertain_fields))

    status = "review" if issues else "ok"
    return {"status": status, "field_status": field_status,
            "issues": issues, "items_sum": by_qty}

if __name__ == "__main__":
    import sys, json
    from extractor import extract
    version = sys.argv[2] if len(sys.argv) > 2 else "v2"
    r = extract(sys.argv[1], version=version)
    print(r.model_dump_json(indent=2))
    print(json.dumps(validate(r), indent=2))
