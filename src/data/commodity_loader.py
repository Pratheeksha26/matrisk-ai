import yfinance as yf
import pandas as pd
import os

def download_commodity_data(tickers, start_date, end_date, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for ticker, name in tickers.items():
        print(f"Downloading {name} ({ticker})...")
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if not data.empty:
                # Flatten multi-index columns if they exist (common in yfinance 1.3.0+)
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                
                data.index.name = 'Date'
                file_path = os.path.join(output_dir, f"{name.lower().replace(' ', '_')}_prices.csv")
                data.to_csv(file_path)
                print(f"Saved to {file_path}")
            else:
                print(f"No data found for {ticker}")
        except Exception as e:
            print(f"Error downloading {ticker}: {e}")

if __name__ == "__main__":
    # Define tickers based on PDF requirements
    # Note: Some commodity futures might require specific LME/COMEX tickers
    commodity_tickers = {
        "HRC=F": "Steel HRC",
        "HG=F": "Copper",
        "ALI=F": "Aluminum",
        "JJN": "Nickel ETN", # More reliable than NI=F
        "TIO=F": "Iron Ore",
        "LIT": "Lithium ETF",
        "REMX": "Rare Earth ETF",
        "BATT": "Battery Metals ETF" # Proxy for Cobalt/Lithium
    }
    
    start = "2014-01-01"
    end = "2024-01-01"
    save_path = "data/raw/commodities"
    
    download_commodity_data(commodity_tickers, start, end, save_path)
