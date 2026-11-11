let
    Source = Csv.Document(
        File.Contents("C:\REPLACE_WITH_YOUR_PATH\social_media_sentiment_raw.csv"),
        [Delimiter=",", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    RemovedExportIndexColumns = Table.RemoveColumns(
        PromotedHeaders,
        {"Unnamed: 0.1", "Unnamed: 0"}
    ),
    TrimmedTextColumns = Table.TransformColumns(
        RemovedExportIndexColumns,
        {
            {"Text", each if _ = null then null else Text.Trim(Text.Clean(Text.From(_))), type text},
            {"Sentiment", each if _ = null then null else Text.Trim(Text.Clean(Text.From(_))), type text},
            {"User", each if _ = null then null else Text.Trim(Text.Clean(Text.From(_))), type text},
            {"Platform", each if _ = null then null else Text.Trim(Text.Clean(Text.From(_))), type text},
            {"Hashtags", each if _ = null then null else Text.Trim(Text.Clean(Text.From(_))), type text},
            {"Country", each if _ = null then null else Text.Trim(Text.Clean(Text.From(_))), type text}
        }
    ),
    ChangedTypes = Table.TransformColumnTypes(
        TrimmedTextColumns,
        {
            {"Timestamp", type datetime},
            {"Retweets", Int64.Type},
            {"Likes", Int64.Type},
            {"Year", Int64.Type},
            {"Month", Int64.Type},
            {"Day", Int64.Type},
            {"Hour", Int64.Type}
        }
    )
in
    ChangedTypes