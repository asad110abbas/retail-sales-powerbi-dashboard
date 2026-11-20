"""Generate a synthetic retail star schema for the Power BI dashboard.

Outputs CSVs into data/: dim_date, dim_product, dim_store, dim_customer, fact_sales.
Deterministic (seeded) so the dashboard numbers are reproducible.

    python scripts/generate_data.py --rows 50000 --seed 7
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

CATEGORIES = {
    "Mobiles": (["Phone X1", "Phone X2 Pro", "Phone Lite", "Phone Max", "Phone Mini"], (25000, 180000)),
    "Laptops": (["Book 13", "Book 15 Pro", "Gamer 17", "Ultra 14", "Student 14"], (80000, 450000)),
    "Audio": (["Buds Air", "Buds Pro", "Headset H1", "Speaker S2", "Soundbar B5"], (2500, 60000)),
    "Wearables": (["Watch Fit", "Watch Pro", "Band 5", "Ring R1"], (5000, 90000)),
    "Accessories": (["Charger 65W", "Cable USB-C", "Power Bank 20K", "Case Clear", "Screen Guard"], (500, 12000)),
}
REGIONS = {
    "North": ["Lahore", "Islamabad", "Faisalabad"],
    "South": ["Karachi", "Hyderabad"],
    "West": ["Quetta", "Peshawar"],
}
CHANNELS = ["Store", "Online", "Marketplace"]
SEGMENTS = ["Consumer", "Corporate", "Small Business"]


def build_dim_date(start: str, end: str) -> pd.DataFrame:
    d = pd.date_range(start, end, freq="D")
    return pd.DataFrame({
        "DateKey": d.strftime("%Y%m%d").astype(int),
        "Date": d.date,
        "Year": d.year,
        "Quarter": "Q" + d.quarter.astype(str),
        "MonthNo": d.month,
        "Month": d.strftime("%b"),
        "YearMonth": d.strftime("%Y-%m"),
        "WeekdayNo": d.weekday + 1,
        "Weekday": d.strftime("%a"),
        "IsWeekend": d.weekday >= 5,
    })


def build_dim_product(rng: np.random.Generator) -> pd.DataFrame:
    rows, key = [], 1
    for cat, (names, (lo, hi)) in CATEGORIES.items():
        for name in names:
            price = round(float(rng.uniform(lo, hi)), -1)
            cost = round(price * float(rng.uniform(0.62, 0.85)), -1)
            rows.append({"ProductKey": key, "SKU": f"SKU-{key:04d}", "Product": name, "Category": cat,
                         "UnitPrice": price, "UnitCost": cost})
            key += 1
    return pd.DataFrame(rows)


def build_dim_store() -> pd.DataFrame:
    rows, key = [], 1
    for region, cities in REGIONS.items():
        for city in cities:
            rows.append({"StoreKey": key, "Store": f"{city} Central", "City": city, "Region": region})
            key += 1
    return pd.DataFrame(rows)


def build_dim_customer(rng: np.random.Generator, n: int = 2500) -> pd.DataFrame:
    return pd.DataFrame({
        "CustomerKey": np.arange(1, n + 1),
        "CustomerID": [f"CUST-{i:05d}" for i in range(1, n + 1)],
        "Segment": rng.choice(SEGMENTS, n, p=[0.7, 0.15, 0.15]),
        "AgeBand": rng.choice(["18-24", "25-34", "35-44", "45-54", "55+"], n, p=[.2, .35, .25, .12, .08]),
    })


def build_fact_sales(rng, rows, dim_date, dim_product, dim_store, dim_customer) -> pd.DataFrame:
    dates = pd.to_datetime(dim_date["Date"])
    # Seasonality: weekend lift, Q4 peak, and steady year-on-year growth.
    weight = (1 + 0.25 * (dates.dt.weekday >= 5)) * (1 + 0.35 * (dates.dt.month.isin([11, 12])))
    weight *= 1 + 0.18 * (dates.dt.year - dates.dt.year.min())
    weight = (weight / weight.sum()).to_numpy()

    date_idx = rng.choice(len(dim_date), rows, p=weight)
    prod_pop = rng.dirichlet(np.ones(len(dim_product)) * 0.8)
    prod_idx = rng.choice(len(dim_product), rows, p=prod_pop)
    store_idx = rng.choice(len(dim_store), rows, p=rng.dirichlet(np.ones(len(dim_store)) * 3))
    cust_idx = rng.integers(0, len(dim_customer), rows)

    price = dim_product["UnitPrice"].to_numpy()[prod_idx]
    cost = dim_product["UnitCost"].to_numpy()[prod_idx]
    qty = np.where(price < 15000, rng.integers(1, 6, rows), rng.integers(1, 3, rows))
    discount = rng.choice([0, 0, 0, 0.05, 0.1, 0.15], rows)
    gross = price * qty
    net = np.round(gross * (1 - discount), 2)

    fact = pd.DataFrame({
        "OrderID": [f"ORD-{i:07d}" for i in range(1, rows + 1)],
        "DateKey": dim_date["DateKey"].to_numpy()[date_idx],
        "ProductKey": dim_product["ProductKey"].to_numpy()[prod_idx],
        "StoreKey": dim_store["StoreKey"].to_numpy()[store_idx],
        "CustomerKey": dim_customer["CustomerKey"].to_numpy()[cust_idx],
        "Channel": rng.choice(CHANNELS, rows, p=[0.5, 0.35, 0.15]),
        "Quantity": qty,
        "GrossAmount": gross,
        "DiscountPct": discount,
        "NetSales": net,
        "COGS": cost * qty,
        "Returned": rng.random(rows) < 0.03,
    })
    return fact.sort_values(["DateKey", "OrderID"]).reset_index(drop=True)


def generate(rows: int = 50000, seed: int = 7, start="2023-01-01", end="2025-12-31") -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    dim_date = build_dim_date(start, end)
    dim_product = build_dim_product(rng)
    dim_store = build_dim_store()
    dim_customer = build_dim_customer(rng)
    fact = build_fact_sales(rng, rows, dim_date, dim_product, dim_store, dim_customer)
    return {"dim_date": dim_date, "dim_product": dim_product, "dim_store": dim_store,
            "dim_customer": dim_customer, "fact_sales": fact}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rows", type=int, default=50000)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent.parent / "data")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, df in generate(args.rows, args.seed).items():
        df.to_csv(args.out / f"{name}.csv", index=False)
        print(f"{name:13s} {len(df):>7,} rows")


if __name__ == "__main__":
    main()
