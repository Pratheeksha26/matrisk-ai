import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import re

st.title("🌱 ESG Impact Analyser")

# Load real formulas
mat_path = "data/raw/materials_project_data.csv"
df_mat = None
formulas = ["Fe2O3", "Al2O3", "NaCl"]
if os.path.exists(mat_path):
    df_mat = pd.read_csv(mat_path)
    if 'formula_pretty' in df_mat.columns:
        formulas = df_mat['formula_pretty'].unique().tolist()

# Simulated element carbon intensity (kg CO2 / kg element)
ELEMENT_GWP = {
    'Li': 15.0, 'Ni': 6.5, 'Co': 8.0, 'Cu': 2.5, 'Al': 12.0, 
    'Fe': 1.8, 'O': 0.1, 'P': 0.5, 'S': 0.3, 'Na': 2.0, 'Cl': 1.5,
    'Si': 4.0, 'Ti': 9.0, 'V': 11.0, 'Mg': 14.0
}

def estimate_co2(formula, qty):
    # Very simple parsing: find elements and count them
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    total_impact = 0
    count_total = 0
    for elem, count in elements:
        count = int(count) if count else 1
        impact = ELEMENT_GWP.get(elem, 2.0) # Default 2.0 if not in list
        total_impact += impact * count
        count_total += count
    
    if count_total == 0: return 2.0 * qty
    return (total_impact / count_total) * qty

st.subheader("Material Substitution Scenario")
col1, col2 = st.columns(2)

with col1:
    original = st.selectbox("Current Material", formulas, index=0)
    quantity = st.number_input("Annual Quantity (kg)", 1000, 1000000, 10000)

with col2:
    # Filter out the original from substitution list
    sub_options = [f for f in formulas if f != original]
    substitute = st.selectbox("Proposed Substitute", sub_options, index=1 if len(sub_options)>1 else 0)

if st.button("Calculate ESG Impact"):
    orig_co2 = estimate_co2(original, quantity)
    sub_co2 = estimate_co2(substitute, quantity)
    
    st.subheader("Carbon Intensity Comparison")
    data = pd.DataFrame({
        'Material': [original, substitute],
        'CO2 footprint (kg CO2e)': [orig_co2, sub_co2]
    })
    fig = px.bar(data, x='Material', y='CO2 footprint (kg CO2e)', color='Material', 
                 color_discrete_sequence=['#ff4b4b', '#00d400'],
                 title=f"Carbon Footprint for {quantity:,} kg")
    st.plotly_chart(fig, width='stretch')
    
    reduction = ((orig_co2 - sub_co2) / orig_co2) * 100
    abs_reduction = orig_co2 - sub_co2
    
    if reduction > 0:
        st.success(f"✅ Potential Carbon Reduction: {reduction:.1f}% (-{abs_reduction:,.0f} kg CO2e)")
    else:
        st.warning(f"⚠️ Substitution increases footprint by {abs(reduction):.1f}% (+{abs(sub_co2 - orig_co2):,.0f} kg CO2e)")
    
    st.subheader("Portfolio Sustainability Score")
    # Base score of 50, modified by reduction
    score_val = 50 + (reduction / 2)
    score_val = max(0, min(100, score_val))
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score_val,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "ESG Alignment Score"},
        gauge = {'axis': {'range': [0, 100]},
                 'bar': {'color': "#00d400" if reduction > 0 else "#ff4b4b"},
                 'steps' : [
                     {'range': [0, 30], 'color': "#fee"},
                     {'range': [30, 70], 'color': "#fffbe6"},
                     {'range': [70, 100], 'color': "#f6ffed"}]}))
    st.plotly_chart(fig_gauge)

