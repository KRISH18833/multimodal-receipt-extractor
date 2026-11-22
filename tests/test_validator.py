import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from schema import Receipt, Item, Confidence
from validator import validate

def test_correct_receipt():
    r = Receipt(
        document_type="receipt",
        merchant="Supermarket",
        date="2026-11-20",
        currency="USD",
        items=[
            Item(name="Apples", qty=2.0, price=3.5),
            Item(name="Bread", qty=1.0, price=2.5),
        ],
        subtotal=None,
        tax=None,
        total=9.5,
        confidence=Confidence(
            merchant=0.95,
            date=0.95,
            currency=0.95,
            items=0.95,
            subtotal=0.95,
            tax=0.95,
            total=0.95,
        ),
        uncertain_fields=[],
    )
    res = validate(r)
    assert res["status"] == "ok", f"Expected status 'ok', got {res['status']}"
    assert len(res["issues"]) == 0, f"Expected no issues, got {res['issues']}"

def test_item_sum_mismatch():
    r = Receipt(
        document_type="receipt",
        merchant="Supermarket",
        date="2026-11-20",
        currency="USD",
        items=[
            Item(name="Apples", qty=2.0, price=3.5),
            Item(name="Bread", qty=1.0, price=2.5),
        ],
        subtotal=None,
        tax=None,
        total=99.0,
        confidence=Confidence(
            merchant=0.95,
            date=0.95,
            currency=0.95,
            items=0.95,
            subtotal=0.95,
            tax=0.95,
            total=0.95,
        ),
        uncertain_fields=[],
    )
    res = validate(r)
    assert res["status"] == "review", f"Expected status 'review', got {res['status']}"
    assert any("Item sum" in issue for issue in res["issues"]), (
        f"Expected 'Item sum' in issues, got {res['issues']}"
    )

def test_not_a_document():
    r = Receipt(
        document_type="not_a_document",
        merchant=None,
        date=None,
        currency=None,
        items=[],
        subtotal=None,
        tax=None,
        total=None,
        confidence=Confidence(
            merchant=0.1,
            date=0.1,
            currency=0.1,
            items=0.1,
            subtotal=0.1,
            tax=0.1,
            total=0.1,
        ),
        uncertain_fields=[],
    )
    res = validate(r)
    assert res["status"] == "reject", f"Expected status 'reject', got {res['status']}"

def test_tax_inclusive_receipt():
    r = Receipt(
        document_type="receipt",
        merchant="Berghotel Grosse Scheidegg",
        date="2026-11-20",
        currency="CHF",
        items=[
            Item(name="Latte Macchiato", qty=2.0, price=4.5),
            Item(name="Gloki", qty=1.0, price=5.0),
            Item(name="Schweinschnitzel", qty=1.0, price=22.0),
            Item(name="Chässpätzli", qty=1.0, price=18.5),
        ],
        subtotal=None,
        tax=3.85,
        total=54.5,
        confidence=Confidence(
            merchant=0.95,
            date=0.95,
            currency=0.95,
            items=0.95,
            subtotal=0.95,
            tax=0.95,
            total=0.95,
        ),
        uncertain_fields=[],
    )
    res = validate(r)
    assert res["status"] == "ok", f"Expected status 'ok', got {res['status']}, issues: {res['issues']}"
    assert len(res["issues"]) == 0, f"Expected no issues, got {res['issues']}"

def test_subtotal_tax_inclusive():
    r = Receipt(
        document_type="receipt",
        merchant="Berghotel Grosse Scheidegg",
        date="2026-11-20",
        currency="CHF",
        items=[
            Item(name="Latte Macchiato", qty=2.0, price=4.5),
            Item(name="Gloki", qty=1.0, price=5.0),
            Item(name="Schweinschnitzel", qty=1.0, price=22.0),
            Item(name="Chässpätzli", qty=1.0, price=18.5),
        ],
        subtotal=54.5,
        tax=3.85,
        total=54.5,
        confidence=Confidence(
            merchant=0.95,
            date=0.95,
            currency=0.95,
            items=0.95,
            subtotal=0.95,
            tax=0.95,
            total=0.95,
        ),
        uncertain_fields=[],
    )
    res = validate(r)
    assert res["status"] == "ok", f"Expected status 'ok', got {res['status']}, issues: {res['issues']}"
    assert len(res["issues"]) == 0, f"Expected no issues, got {res['issues']}"

def test_subtotal_tax_mismatch():
    r = Receipt(
        document_type="receipt",
        merchant="Supermarket",
        date="2026-11-20",
        currency="USD",
        items=[
            Item(name="Item 1", qty=1.0, price=50.0),
        ],
        subtotal=50.0,
        tax=5.0,
        total=99.0,
        confidence=Confidence(
            merchant=0.95,
            date=0.95,
            currency=0.95,
            items=0.95,
            subtotal=0.95,
            tax=0.95,
            total=0.95,
        ),
        uncertain_fields=[],
    )
    res = validate(r)
    assert res["status"] == "review", f"Expected status 'review', got {res['status']}"
    assert any("Subtotal + tax" in issue for issue in res["issues"]), (
        f"Expected 'Subtotal + tax' in issues, got {res['issues']}"
    )

if __name__ == "__main__":
    tests = [
        ("a) Correct receipt -> status 'ok'", test_correct_receipt),
        ("b) Total changed to 99.0 -> status 'review' with 'Item sum'", test_item_sum_mismatch),
        ("c) document_type 'not_a_document' -> status 'reject'", test_not_a_document),
        ("d) Tax-inclusive receipt -> status 'ok'", test_tax_inclusive_receipt),
        ("e) Subtotal tax-inclusive -> status 'ok'", test_subtotal_tax_inclusive),
        ("f) Subtotal + tax mismatch -> status 'review' with 'Subtotal + tax'", test_subtotal_tax_mismatch),
    ]

    all_passed = True
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"PASS: {name}")
        except AssertionError as e:
            all_passed = False
            print(f"FAIL: {name} - {e}")
        except Exception as e:
            all_passed = False
            print(f"ERROR: {name} - {e}")

    if not all_passed:
        exit(1)
