import pandas as pd
import numpy as np
import os

def calculate_returns(df, close_col='Close'):
    """
    Calculate log returns.
    """
    df['daily_return'] = np.log(df[close_col] / df[close_col].shift(1))
    return df

def calculate_rsi(df, close_col='Close', window=14):
    """
    Calculate Relative Strength Index.
    """
    delta = df[close_col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    df['rsi_14'] = 100 - (100 / (1 + rs))
    return df

def calculate_bollinger_bands(df, close_col='Close', window=20, num_std=2):
    """
    Calculate Bollinger Bands and Z-score.
    """
    rolling_mean = df[close_col].rolling(window=window).mean()
    rolling_std = df[close_col].rolling(window=window).std()
    
    df['bollinger_high'] = rolling_mean + (rolling_std * num_std)
    df['bollinger_low'] = rolling_mean - (rolling_std * num_std)
    df['bollinger_z'] = (df[close_col] - rolling_mean) / rolling_std
    return df

def calculate_volatility_garch(df, returns_col='daily_return', window=252):
    """
    Simple rolling volatility as a proxy for GARCH if arch package is not used.
    """
    df['vol_5d'] = df[returns_col].rolling(window=5).std() * np.sqrt(252) * 100
    return df

def extract_financial_features(df, close_col='Close'):
    """
    Main pipeline for financial feature extraction.
    Automatically handles messy Yahoo Finance formats.
    """
    df = df.copy()
    
    # Clean up multi-index if necessary
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # If 'Close' is not found, try to find a column that looks like it
    if close_col not in df.columns:
        potential_cols = [c for c in df.columns if 'Close' in str(c)]
        if potential_cols:
            close_col = potential_cols[0]
        else:
            # Fallback to second column if it's numeric
            df_numeric = df.apply(pd.to_numeric, errors='coerce')
            df_numeric = df_numeric.dropna(axis=1, how='all')
            if len(df_numeric.columns) >= 1:
                close_col = df_numeric.columns[0]

    # Convert to numeric and drop non-numeric metadata rows (like Ticker info)
    df[close_col] = pd.to_numeric(df[close_col], errors='coerce')
    df = df.dropna(subset=[close_col])
    
    # Run indicators
    df = calculate_returns(df, close_col)
    df = calculate_rsi(df, close_col)
    df = calculate_bollinger_bands(df, close_col)
    df = calculate_volatility_garch(df)
    
    if 'F2' in df.columns and 'F1' in df.columns:
        df['term_spread'] = df['F2'] - df['F1']
        
    return df

if __name__ == "__main__":
    raw_data_path = "data/external/DS2_commodity_prices_10yr.csv"
    if os.path.exists(raw_data_path):
        df = pd.read_csv(raw_data_path)
        features_df = extract_financial_features(df)
        print("Success!")
