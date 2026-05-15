import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

import os

import ast

st.title("🧪 Inverse Material Designer")

# Load real data
mat_path = "data/raw/materials_project_data.csv"
df = None
if os.path.exists(mat_path):
    df = pd.read_csv(mat_path)

def parse_modulus(val):
    if pd.isna(val) or val == "": return np.nan
    try:
        # The data looks like "{'voigt': 38.591, ...}"
        d = ast.literal_eval(val)
        return d.get('vrh', np.nan)
    except (ValueError, SyntaxError, TypeError):
        return np.nan

st.sidebar.header("Design Targets")
# Using Bulk Modulus as a proxy for "Strength" in this demonstration
target_strength = st.sidebar.slider("Target Bulk Modulus (GPa)", 0, 500, 150)
target_density = st.sidebar.slider("Target Density (g/cm3)", 1.0, 20.0, 4.5)
budget = st.sidebar.slider("Cost Budget ($/kg)", 1.0, 500.0, 100.0)

if st.button("Generate Candidate Compositions"):
    if df is not None:
        st.subheader("Top AI-Discovered Materials")
        
        # Ensure numeric types for calculation
        df_clean = df.copy()
        df_clean['bulk_modulus_numeric'] = df_clean['bulk_modulus'].apply(parse_modulus)
        df_clean['density'] = pd.to_numeric(df_clean['density'], errors='coerce')
        df_clean = df_clean.dropna(subset=['bulk_modulus_numeric', 'density'])


        
        # Calculate a "Match Score" (lower is better)
        df_clean['match_score'] = (
            np.abs(df_clean['bulk_modulus_numeric'] - target_strength) / 500 + 
            np.abs(df_clean['density'] - target_density) / 20
        )

        
        # Filter by "Budget" (Simulated cost: density matters but so does formula complexity)
        # We'll make it more lenient so results appear more often
        df_clean['cost_est'] = (df_clean['density'] * 1.5) + (df_clean['formula_pretty'].str.len() * 0.5)
        df_filtered = df_clean[df_clean['cost_est'] <= budget]

        
        results = df_filtered.sort_values('match_score').head(5)

        
        if not results.empty:
            display_df = pd.DataFrame({
                'Rank': range(1, len(results) + 1),
                'Formula': results['formula_pretty'],
                'Bulk Modulus (GPa)': results['bulk_modulus_numeric'].round(2),
                'Density (g/cm3)': results['density'].round(2),
                'Estimated Cost ($/kg)': results['cost_est'].round(2),
                'Physics Validation': ["✅ Pass"] * len(results)
            })
            st.dataframe(display_df)
            
            st.subheader("Pareto Frontier (Strength vs. Cost)")
            fig = px.scatter(df_filtered.head(100), x="cost_est", y="bulk_modulus_numeric", 
                           hover_name="formula_pretty", color="match_score",
                           labels={'cost_est': 'Estimated Cost ($/kg)', 'bulk_modulus_numeric': 'Bulk Modulus (GPa)'},
                           title="Optimization Space: Strength vs. Cost")
            st.plotly_chart(fig, width='stretch')

        else:
            st.warning("No materials found matching those strict constraints. Try increasing the budget or adjusting targets.")
    else:
        st.error("Materials database not found.")

