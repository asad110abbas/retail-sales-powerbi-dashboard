// Power Query (M) - load dim_date.csv and type it. Mark as Date Table on [Date] after loading.
let
    Source = Csv.Document(File.Contents(DataFolder & "dim_date.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"DateKey", Int64.Type}, {"Date", type date}, {"Year", Int64.Type}, {"Quarter", type text},
        {"MonthNo", Int64.Type}, {"Month", type text}, {"YearMonth", type text},
        {"WeekdayNo", Int64.Type}, {"Weekday", type text}, {"IsWeekend", type logical}
    })
in
    Typed
