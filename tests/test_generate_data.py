import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from generate_data import generate  # noqa: E402


def test_star_schema_integrity():
    t = generate(rows=3000, seed=1)
    f = t["fact_sales"]
    assert len(f) == 3000
    assert f["OrderID"].is_unique
    for dim, key in [("dim_date", "DateKey"), ("dim_product", "ProductKey"),
                     ("dim_store", "StoreKey"), ("dim_customer", "CustomerKey")]:
        assert t[dim][key].is_unique
        assert f[key].isin(t[dim][key]).all(), f"orphan {key} in fact_sales"


def test_amounts_are_consistent():
    f = generate(rows=2000, seed=2)["fact_sales"]
    assert (f["NetSales"] <= f["GrossAmount"]).all()
    assert (f["Quantity"] >= 1).all()
    assert f["DiscountPct"].between(0, 0.5).all()


def test_deterministic():
    a = generate(rows=500, seed=3)["fact_sales"]
    b = generate(rows=500, seed=3)["fact_sales"]
    assert a.equals(b)
