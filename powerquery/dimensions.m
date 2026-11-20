// Power Query (M) - generic loader used for dim_product, dim_store and dim_customer.
// Create a blank query named LoadCsv with this function, then: = LoadCsv("dim_product.csv")
(fileName as text) as table =>
let
    Source = Csv.Document(File.Contents(DataFolder & fileName), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    // Auto-detect types from the first 200 rows
    Typed = Table.TransformColumnTypes(Promoted,
        List.Transform(Table.ColumnNames(Promoted), each {_, if Text.EndsWith(_, "Key") then Int64.Type else type any}))
in
    Typed
