import streamlit as st

st.set_page_config(
    page_title="MatRisk AI Dashboard",
    page_icon="🔬",
    layout="wide"
)

st.title("MatRisk AI: Predictive Material Intelligence")
st.sidebar.success("Select a tool above.")

st.markdown("""
### Welcome to the MatRisk AI Intelligence Suite
This platform integrates computational material science with financial risk modeling to provide 
state-of-the-art predictive analytics for commodity markets and infrastructure assets.

**Core Modules:**
1. **Material Property Explorer**: Predict and visualize atomic-level properties.
2. **Commodity Signal Dashboard**: Material-aware price forecasting.
3. **Infrastructure Risk Scorer**: Physics-informed credit risk and survival analysis.
4. **Inverse Material Designer**: AI-driven alloy discovery with cost constraints.
5. **ESG Impact Analyser**: Substitution analysis for green transition.
""")

st.info("👈 Use the sidebar to navigate between modules.")
