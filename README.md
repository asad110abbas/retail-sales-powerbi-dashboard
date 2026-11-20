# 📊 BRIHA · Retail Sales Power BI Dashboard

![BRIHA](https://img.shields.io/badge/Part_of-BRIHA-8B5CF6?style=for-the-badge&labelColor=0B1024) ![Module](https://img.shields.io/badge/Briha-Data_Lab-00F0FF?style=for-the-badge&labelColor=0B1024)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-measures-1F6FEB)
![Power Query](https://img.shields.io/badge/Power_Query-M-00B39F)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![CI](https://github.com/asad110abbas/retail-sales-powerbi-dashboard/actions/workflows/ci.yml/badge.svg)

> ⚡ **Part of [BRIHA](https://github.com/asad110abbas)**, built by Syed Asad Abbas.

An end-to-end **Power BI** sales analytics solution for a multi-region electronics retailer: a star-schema data
model, 30+ reusable **DAX** measures (time intelligence, Pareto, ranking, customer metrics), **Power Query (M)**
loaders and a custom report theme. The data is generated with Python, so the whole project is reproducible.

> All data is **synthetic**: 50,000 orders across 3 years, 24 products, 7 stores and 2,500 customers.

## Business questions answered
- How are sales and margin trending vs. last year (YoY, YTD, rolling 3 months)?
- Which 20% of products drive 80% of revenue (Pareto)?
- Which regions, stores and channels are over- or under-performing?
- How much revenue is lost to discounts and returns?
- Who are our customers by segment and age band, and how many are new?

## Report pages
| Page | Highlights |
|---|---|
| Executive Overview | KPI cards with conditional YoY colors, Sales vs PY trend, category share |
| Product Performance | Category → Product matrix, dense ranking, Pareto 80/20 chart |
| Store & Region | Store share, decomposition tree Region → City → Store → Category |
| Customers | Active / new customers, sales per customer by segment |

## Data model
Star schema with `fact_sales` and four dimensions (`dim_date`, `dim_product`, `dim_store`, `dim_customer`).
See [model/MODEL.md](model/MODEL.md) for the ER diagram and modeling decisions.

## Repository structure
```
scripts/generate_data.py   synthetic star-schema generator (seeded, reproducible)
data/                      generated CSVs
powerquery/                Power Query (M) loaders
dax/measures.dax           all DAX measures, grouped and commented
model/MODEL.md             ER diagram + modeling decisions
theme/retail-theme.json    custom report theme
BUILD_GUIDE.md             step-by-step build of the .pbix
tests/                     data integrity tests (pytest)
```

## Getting started
```bash
pip install -r requirements.txt
python scripts/generate_data.py --rows 50000
pytest -q
```
Then follow [BUILD_GUIDE.md](BUILD_GUIDE.md) to assemble the report in Power BI Desktop.

## Skills demonstrated
`Power BI` · `DAX` · `Power Query / M` · `Star schema modeling` · `Time intelligence` · `Python / pandas` · `Data quality testing`
