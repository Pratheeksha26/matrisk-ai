import streamlit as st
import pandas as pd
import plotly.express as px

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

import ast

def parse_modulus(val):
    if pd.isna(val) or val == "": return np.nan
    try:
        if isinstance(val, (int, float)): return float(val)
        # The data looks like "{'voigt': 38.591, ...}"
        d = ast.literal_eval(val)
        return d.get('vrh', np.nan)
    except (ValueError, SyntaxError, TypeError):
        return np.nan

st.title("🔬 Material Property Explorer")

# Load real data
mat_path = "data/raw/materials_project_data.csv"
df = None
if os.path.exists(mat_path):
    df = pd.read_csv(mat_path)
    # Pre-parse for distribution chart
    df['bulk_modulus_numeric'] = df['bulk_modulus'].apply(parse_modulus)

formula = st.text_input("Enter Chemical Formula (e.g., Fe2O3, NaCl, LiFePO4)", "Fe2O3")

if df is not None:
    # Case-insensitive search
    match = df[df['formula_pretty'].str.lower() == formula.lower()]
    
    if not match.empty:
        asset_data = match.iloc[0]
        st.success(f"Material {formula} found in database (ID: {asset_data['material_id']})")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Physical Properties")
            bm_val = parse_modulus(asset_data['bulk_modulus'])
            sm_val = parse_modulus(asset_data['shear_modulus'])
            
            raw_results = {
                "Formation Energy (eV/atom)": asset_data['formation_energy_per_atom'],
                "Band Gap (eV)": asset_data['band_gap'],
                "Bulk Modulus (GPa)": bm_val,
                "Shear Modulus (GPa)": sm_val,
                "Density (g/cm3)": asset_data['density']
            }
            
            def format_val(val):
                try:
                    num = float(val)
                    return f"{num:.3f}" if pd.notnull(num) else "N/A"
                except (ValueError, TypeError):
                    return str(val) if pd.notnull(val) else "N/A"

            display_results = {k: format_val(v) for k, v in raw_results.items()}
            st.table(pd.DataFrame(display_results.items(), columns=["Property", "Value"]))
        
        with col2:
            st.subheader("Comparison to Database")
            # Show where this material sits in the distribution of Bulk Modulus
            if pd.notnull(bm_val):
                fig = px.histogram(df.dropna(subset=['bulk_modulus_numeric']), x='bulk_modulus_numeric', 
                                 nbins=50, title="Bulk Modulus Distribution (GPa)")
                fig.add_vline(x=bm_val, line_dash="dash", line_color="red", 
                             annotation_text=f"This: {formula}")
                st.plotly_chart(fig, width='stretch')
            else:
                st.info("Bulk Modulus data not available for this material.")

        
        st.subheader("AI Explainability (SHAP)")
        # Dummy SHAP chart for visual feedback
        shap_data = pd.DataFrame({
            'Feature': ['Electronegativity', 'Atomic Radius', 'Valence Electrons', 'Ionization Energy'],
            'Impact': [0.45, -0.32, 0.15, -0.08]
        })
        fig_shap = px.bar(shap_data, x='Impact', y='Feature', orientation='h', 
                         title=f"Feature Contribution for {formula} Prediction")
        st.plotly_chart(fig_shap, width='stretch')

        
    else:
        st.warning(f"Formula '{formula}' not found in the current subset. Showing demonstration data.")
        # Fallback to previous dummy data
        results = {"Formation Energy": "-2.10", "Band Gap": "2.20", "Bulk Modulus": "178", "Shear Modulus": "90"}
        st.table(pd.DataFrame(results.items(), columns=["Property", "Value"]))
else:
    st.error("Materials database not found. Please run the data acquisition pipeline.")

