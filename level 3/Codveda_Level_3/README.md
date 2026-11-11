# Codveda Data Analytics — Level 3

This ZIP contains the three Level 3 task folders. Open Jupyter notebooks from their own task folders so relative data paths work.

## Tasks included
1. **Classification** — predicts the `Platform` category from the supplied social-media dataset. The supplied four datasets do not contain a churn target. Includes categorical preprocessing, numeric scaling, Decision Tree, Logistic Regression, Random Forest, grid search, and requested test metrics.
2. **Power BI Dashboard** — raw dataset, Power Query cleaning script, DAX measures, and a build/publish guide. You must create and publish the `.pbix` in Power BI Desktop/Service; it is not generated in this package.
3. **NLP Sentiment Analysis** — tokenization, stopword removal, stemming, TextBlob polarity classification, sentiment distribution, and sentiment-specific word clouds.

## Environment
Python 3 with pandas, numpy, matplotlib, seaborn, scikit-learn, nltk, textblob, and wordcloud.

Install missing Python packages in the active Anaconda environment with:

```bash
conda install pandas numpy matplotlib seaborn scikit-learn nltk textblob wordcloud
```

Power BI Desktop is required for the dashboard task. Publishing and sharing depend on your Microsoft account and workspace permissions.
