# Project Structure

```text
market-sentiment-impact-analysis/
│
├── data/
│   ├── raw/                 # CSVs from Kaggle
│   ├── processed/           # Merged Price+Sentiment datasets
│   └── tickers/             # Generated lists (high_beta.csv, low_beta.csv)
│
├── notebooks/
│   ├── 00_ticker_selection.ipynb    # The Automated Selection Logic
│   ├── 01_data_ingestion.ipynb      # Fetching data for the selected 60 stocks
│   ├── 02_sentiment_scoring.ipynb   # VADER vs FinBERT comparison
│   ├── 03_linear_analysis.ipynb     # Granger Causality (Baseline)
│   └── 04_nonlinear_analysis.ipynb  # Transfer Entropy (Advanced)
│
├── src/
│   ├── financial_metrics.py # Functions to calc Beta, Volatility, etc.
│   ├── entropy_utils.py     # Functions for Transfer Entropy/Mutual Info, etc.
│   └── plotting.py          # Standardized chart styles
│
├── requirements.txt
└── README.md
```
