# Build the .pbix in Power BI Desktop (about 20 minutes)

1. **Generate data**: `python scripts/generate_data.py` (CSVs land in `data/`).
2. **Parameter**: *Home → Transform data → Manage Parameters → New*: `DataFolder` (Text) = full path to `data\` with a trailing backslash.
3. **Queries**: create blank queries from `powerquery/*.m` (`fact_sales`, `dim_date`, and `LoadCsv` for the other three dimensions). *Close & Apply*.
4. **Model view**: create the 4 relationships in `model/MODEL.md` (1:* single direction). Mark `dim_date` as date table on `Date`. Set *Sort by column* for `Month` and `Weekday`. Hide the key columns in `fact_sales`.
5. **Measures**: create table `_Measures` (*Enter data*, one empty column, then delete it) and paste the measures from `dax/measures.dax`.
6. **Theme**: *View → Themes → Browse for themes* → `theme/retail-theme.json`.
7. **Pages**:
   - **Executive Overview**: KPI cards (Total Sales, Gross Margin %, Orders, AOV, Sales YoY %), line chart Sales vs Sales PY by YearMonth, donut Category Share %, map or bar by Region, slicers Year / Channel.
   - **Product Performance**: matrix Category → Product with Sales, Margin %, Units, Product Rank, Pareto chart (bar Total Sales + line Pareto Cumulative %), top-N filter.
   - **Store & Region**: bar Store Share %, decomposition tree (Total Sales by Region → City → Store → Category).
   - **Customers**: Active Customers, New Customers, Sales per Customer by Segment and AgeBand.
8. Save as `RetailSalesDashboard.pbix` in the repo root and export page screenshots to `screenshots/`.
