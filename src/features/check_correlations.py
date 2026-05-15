import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def check_signal_correlation(df, signal_col, target_col='daily_return'):
    """
    Check correlation between engineered signals and target commodity returns.
    """
    if signal_col not in df.columns or target_col not in df.columns:
        print(f"Columns {signal_col} or {target_col} not found.")
        return None
    
    correlation = df[signal_col].corr(df[target_col])
    print(f"Correlation between {signal_col} and {target_col}: {correlation:.4f}")
    
    # Lagged correlation (predictive power)
    for lag in [1, 5, 21]:
        lag_corr = df[signal_col].shift(lag).corr(df[target_col])
        print(f"Predictive correlation ({lag}-day lag): {lag_corr:.4f}")
        
    return correlation

if __name__ == "__main__":
    processed_comm = "data/processed/commodity_features_final.csv"
    if os.path.exists(processed_comm):
        df = pd.read_csv(processed_comm)
        # Check MQI trend vs returns
        check_signal_correlation(df, 'MQI_21D_trend')
