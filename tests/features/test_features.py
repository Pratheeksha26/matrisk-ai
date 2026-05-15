import pytest
import pandas as pd
import numpy as np
from src.features.financial_features import calculate_returns, calculate_rsi

def test_calculate_returns():
    df = pd.DataFrame({'Close': [100.0, 110.0, 99.0]})
    df_res = calculate_returns(df)
    assert 'daily_return' in df_res.columns
    assert np.isclose(df_res['daily_return'].iloc[1], np.log(110/100))

def test_calculate_rsi():
    # Create a trend to get meaningful RSI
    prices = [10, 12, 14, 13, 15, 17, 18, 16, 14, 15, 17, 19, 21, 20, 22]
    df = pd.DataFrame({'Close': prices})
    df_res = calculate_rsi(df)
    assert 'rsi_14' in df_res.columns
    # RSI should be between 0 and 100
    assert df_res['rsi_14'].dropna().between(0, 100).all()
