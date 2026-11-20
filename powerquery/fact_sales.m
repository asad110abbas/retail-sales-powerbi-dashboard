// Power Query (M) - load and type fact_sales.csv
// Set the folder path once via a parameter named DataFolder (e.g. C:\repo\data\)
let
    Source = Csv.Document(File.Contents(DataFolder & "fact_sales.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"OrderID", type text}, {"DateKey", Int64.Type}, {"ProductKey", Int64.Type},
        {"StoreKey", Int64.Type}, {"CustomerKey", Int64.Type}, {"Channel", type text},
        {"Quantity", Int64.Type}, {"GrossAmount", type number}, {"DiscountPct", Percentage.Type},
        {"NetSales", Currency.Type}, {"COGS", Currency.Type}, {"Returned", type logical}
    }),
    NoBlankKeys = Table.SelectRows(Typed, each [ProductKey] <> null and [DateKey] <> null)
in
    NoBlankKeys
