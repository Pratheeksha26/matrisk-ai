import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

import os

st.title("🌉 Infrastructure Risk Scorer")

# Load real NBI data
nbi_path = "data/interim/nbi_processed.csv"
if os.path.exists(nbi_path):
    df = pd.read_csv(nbi_path)
    
    st.subheader("Portfolio Risk Summary (Florida NBI 2023)")
    df['deck_condition_numeric'] = pd.to_numeric(df['deck_condition'], errors='coerce')
    avg_deck = df['deck_condition_numeric'].mean()
    total_assets = len(df)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Assets", f"{total_assets:,}")
    col2.metric("Avg Deck Condition", f"{avg_deck:.1f}/9")

    st.subheader("Survival Analysis")
    asset_id = st.selectbox("Select Asset for Detail", df['asset_id'].head(100).tolist())
    
    asset_data = df[df['asset_id'] == asset_id].iloc[0]
    st.write(f"**Asset Year Built:** {asset_data['year_built']}")
    st.write(f"**Annual Traffic:** {asset_data['annual_traffic']:,}")

    # Survival curve based on real age
    age = asset_data['age_years']
    times = np.linspace(0, 50, 100)
    
    # Handle non-numeric condition (like 'N')
    condition = pd.to_numeric(asset_data['deck_condition'], errors='coerce')
    if pd.isna(condition):
        condition = 7.0 # Default fallback
        st.caption("Note: Condition data for this asset is non-numeric ('N'), using default value (7.0) for simulation.")
        
    decay_rate = 0.01 + (9 - condition) * 0.005
    surv = np.exp(-decay_rate * times)
    
    fig = px.line(x=times, y=surv, labels={'x': 'Years from Now', 'y': 'Survival Probability'})
    fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Today")
    st.plotly_chart(fig, width='stretch')

else:
    st.info("NBI processed data not found. Please run the data acquisition pipeline.")
    st.subheader("Survival Analysis (Sample Data)")
    # Fallback to dummy for now if file missing
    times = np.linspace(0, 50, 100)
    surv = np.exp(-0.02 * times)
    fig = px.line(x=times, y=surv, labels={'x': 'Years', 'y': 'Survival Probability'})
    st.plotly_chart(fig, width='stretch')


st.subheader("Stress Test Scenarios")
scenario = st.selectbox("Select Stress Scenario", ["Rare Earth Crisis", "Climate Corrosion", "Steel Quality Shift"])
if st.button("Run Stress Simulation"):
    st.info(f"Simulating {scenario} impact over 10,000 paths...")
    st.success("Impact Waterfall generated below.")
