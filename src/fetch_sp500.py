import pandas as pd
import yfinance as yf
import os
import sys
import requests
import time
from io import StringIO

# --- CONFIGURATION ---
START_DATE = "2017-12-01"
END_DATE = "2020-07-19"
OUTPUT_DIR = os.path.join('data', 'raw')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'constituents.csv')
BATCH_SIZE = 50

def fetch_current_sp500_list():
    """Scrapes the current S&P 500 table from Wikipedia with a User-Agent."""
    print("Scrapping Wikipedia for current S&P 500 constituents...")
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tables = pd.read_html(StringIO(response.text))
        df = tables[0]
        df['Symbol'] = df['Symbol'].str.replace('.', '-', regex=False)
        return df
    except Exception as e:
        print(f"Error scraping Wikipedia: {e}")
        sys.exit(1)

def download_batch(tickers):
    """Downloads a batch of tickers safely."""
    try:
        data = yf.download(
            tickers, 
            start=START_DATE, 
            end=END_DATE, 
            progress=False,
            threads=True,
            auto_adjust=False
        )
        
        if 'Adj Close' in data:
            return data['Adj Close']
        elif 'Close' in data:
            print("   'Adj Close' missing, using 'Close' instead.")
            return data['Close']
        else:
            return pd.DataFrame()
            
    except Exception as e:
        print(f"   Batch error: {e}")
        return pd.DataFrame()

def filter_survivors(df_constituents):
    tickers = df_constituents['Symbol'].tolist()
    print(f"\nDownloading historical data for {len(tickers)} stocks...")
    print(f"   Strategy: Batching {BATCH_SIZE} stocks at a time.")

    all_batch_data = []
    
    for i in range(0, len(tickers), BATCH_SIZE):
        batch = tickers[i:i+BATCH_SIZE]
        print(f"   Processing batch {i} to {i+len(batch)}...", end="\r")
        
        batch_df = download_batch(batch)
        
        if not batch_df.empty:
            batch_df = batch_df.dropna(axis=1, how='all')
            all_batch_data.append(batch_df)
        
        time.sleep(1)

    print("\n   Download complete. Merging data...")
    
    if not all_batch_data:
        print("CRITICAL ERROR: No data was downloaded. Check internet or yfinance version.")
        sys.exit(1)

    full_data = pd.concat(all_batch_data, axis=1)
    
    print(f"   Raw Data Shape: {full_data.shape} (Rows, Columns)")
    
    expected_days = len(full_data)
    threshold = int(expected_days * 0.9)
    
    print(f"   Filtering: Keeping stocks with at least {threshold} valid trading days.")
    
    valid_data = full_data.dropna(axis=1, thresh=threshold)
    valid_tickers = valid_data.columns.tolist()
    
    print(f"\nFiltering Results:")
    print(f"   - Current S&P 500 Count: {len(tickers)}")
    print(f"   - Valid 'Survivors' (2018-2020): {len(valid_tickers)}")
    
    df_survivors = df_constituents[df_constituents['Symbol'].isin(valid_tickers)]
    return df_survivors

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    df_all = fetch_current_sp500_list()
    df_clean = filter_survivors(df_all)
    
    df_clean.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSuccess! Saved {len(df_clean)} validated tickers to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
    