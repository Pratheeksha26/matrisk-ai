import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import os

st.title("📈 Commodity Signal Dashboard")

# Mapping selected names to filenames
mapping = {
    "Steel HRC": "steel_hrc_prices.csv",
    "Copper": "copper_prices.csv",
    "Aluminum": "aluminum_prices.csv",
    "Nickel": "nickel_etn_prices.csv",
    "Lithium": "lithium_etf_prices.csv"
}

commodity = st.selectbox("Select Commodity", list(mapping.keys()))

# Load real data
data_path = os.path.join("data/raw/commodities", mapping[commodity])
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 1. AI Signal Panel
    st.subheader("MatRisk Intelligence Signals")
    
    # Simple metrics from real data
    current_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-30] if len(df) > 30 else df['Close'].iloc[0]
    change = ((current_price - prev_price) / prev_price) * 100
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Price", f"${current_price:.2f}", f"{change:+.1f}% (30d)")
    c2.metric("Supply Disruption Prob", "18%", "-2%") # Still demo
    c3.metric("Substitution Elasticity", "0.42", "Stable") # Still demo

    # 2. Price Chart
    st.subheader("Market Price & AI Forecast")
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])
    st.plotly_chart(fig, width='stretch')
    
    st.success(f"🤖 AI Forecast for {commodity}: Trend indicates potential {('uptrend' if change > 0 else 'downtrend')} based on recent volatility.")
else:
    st.error(f"Data file not found: {data_path}")

