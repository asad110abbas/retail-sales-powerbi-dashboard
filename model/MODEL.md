# Data model

Classic **star schema**: one fact table surrounded by conformed dimensions. All relationships are
**one-to-many, single direction** (dimension → fact), which keeps DAX predictable and fast.

```mermaid
erDiagram
    dim_date ||--o{ fact_sales : DateKey
    dim_product ||--o{ fact_sales : ProductKey
    dim_store ||--o{ fact_sales : StoreKey
    dim_customer ||--o{ fact_sales : CustomerKey

    fact_sales {
        string OrderID
        int DateKey FK
        int ProductKey FK
        int StoreKey FK
        int CustomerKey FK
        string Channel
        int Quantity
        decimal GrossAmount
        decimal DiscountPct
        decimal NetSales
        decimal COGS
        bool Returned
    }
    dim_date { int DateKey PK
        date Date
        int Year
        string Quarter
        string Month }
    dim_product { int ProductKey PK
        string SKU
        string Product
        string Category
        decimal UnitPrice }
    dim_store { int StoreKey PK
        string Store
        string City
        string Region }
    dim_customer { int CustomerKey PK
        string Segment
        string AgeBand }
```

## Modeling decisions

| Decision | Why |
|---|---|
| Integer surrogate keys (`DateKey` = `yyyymmdd`) | Smaller columns, faster relationships, VertiPaq-friendly |
| `dim_date` marked as date table | Required for time intelligence (`SAMEPERIODLASTYEAR`, `TOTALYTD`) |
| `Month` sorted by `MonthNo`, `Weekday` sorted by `WeekdayNo` | Correct axis order in visuals |
| Measures in a dedicated `_Measures` table | Clean field list, easy discovery |
| Hide foreign keys in `fact_sales` | Forces report authors to slice by dimension attributes |
| Hierarchies: Date (Year → Quarter → Month → Date), Geography (Region → City → Store), Product (Category → Product) | Drill-down without extra measures |
