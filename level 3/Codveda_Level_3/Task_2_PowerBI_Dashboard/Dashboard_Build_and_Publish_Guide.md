# Level 3 — Task 2: Power BI Dashboard

**Assignment objectives:** import and clean the dataset in Power BI; create interactive visualizations; add filters/slicers; publish and share the dashboard.

## Dataset
Use `data/social_media_sentiment_raw.csv` (732 rows). It includes post text, sentiment labels, timestamps, platform, country, retweets, and likes. The two `Unnamed` columns are exported index fields and should be removed during Power Query cleaning. Several text fields contain leading/trailing spaces.

## 1. Import and clean in Power BI Desktop
1. Open Power BI Desktop.
2. Select **Home → Get data → Text/CSV** and open `data/social_media_sentiment_raw.csv`.
3. Choose **Transform Data**.
4. In Power Query Editor, open **Home → Advanced Editor**.
5. Open `Power_Query_Cleaning.m`, replace the placeholder path with the full path to `social_media_sentiment_raw.csv`, then paste the query into Advanced Editor.
6. Select **Done**, confirm the preview has the expected columns and data types, then select **Close & Apply**.
7. In the model/column tools, set the `Country` data category to **Country/Region** so the map visual can geocode countries.
8. Rename the table to `SocialMedia` if Power BI assigned a different query name. The DAX measures below use that table name.

## 2. Create the measures
In Power BI, select **Modeling → New measure** and add the expressions from `Measures.dax`.

## 3. Build the required interactive visuals
Create these visuals on one report page:

| Visual | Fields | Purpose |
|---|---|---|
| Bar chart | Axis: `Platform`; Values: `[Total Posts]` | Compare post volume across platforms. |
| Line chart | X-axis: `Timestamp` (month or date); Y-axis: `[Total Posts]` | Show post volume over time. |
| Map | Location: `Country`; Bubble size: `[Total Posts]` | Compare post volume by country. |

Add slicers for `Platform`, `Sentiment`, and `Year` so viewers can filter the visuals. Ensure the slicers interact with all three charts.

## 4. Publish and share
1. Save the report as `Codveda_Social_Media_Dashboard.pbix`.
2. Select **Publish** in Power BI Desktop and choose a workspace available to your account.
3. Open the report in Power BI Service, check the visuals and slicers, then use the available sharing option. Publishing/sharing availability depends on your Microsoft account, workspace, tenant settings, and license.

## Completion boundary
This package contains the supplied raw CSV, the Power Query cleaning script, the DAX measures, and the build/publish instructions. A native `.pbix` report and its publication must be created in Power BI Desktop/Service; those actions cannot be completed from this Python environment. Do not treat this task as published until you have saved and published the report yourself.
