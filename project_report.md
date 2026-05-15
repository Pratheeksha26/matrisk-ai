# MatRisk AI: Integrated Materials & Infrastructure Risk Platform
## Technical Project Report

### 1. Executive Summary
The MatRisk AI platform is an end-to-end intelligence system designed to bridge the gap between materials science, infrastructure health, and global commodity markets. This project has successfully integrated real-time data acquisition, advanced graph-based machine learning, and a high-fidelity decision-support dashboard.

---

### 2. Data Acquisition & Pipelines
The system utilizes three primary data streams:

*   **Materials Science (Materials Project)**: Automated ingestion of crystal structures and physical properties (Formation Energy, Band Gap, Moduli) for over 130,000 materials.
*   **Infrastructure Health (National Bridge Inventory - NBI)**: Real-time processing of the 2023 NBI dataset (specifically Florida), covering 12,881 assets. The pipeline handles data cleaning, non-numeric flag resolution, and condition scoring.
*   **Commodity Markets**: Ingestion of 10-year historical price data for key industrial commodities (Aluminum, Copper, Steel, Lithium, Nickel) to provide financial context to material risks.

---

### 3. Feature Engineering & AI Architecture
The platform employs a multi-layered feature engineering strategy:

*   **Crystal Graph Neural Networks (CGNN)**: Materials are converted into graph representations (nodes as atoms, edges as bonds) for physics-informed property prediction.
*   **Magpie Atomic Descriptors**: Automated extraction of chemical properties (electronegativity, atomic radius, etc.) from formulas.
*   **Cross-Domain Fusion**: A unique engine that correlates material scarcity with commodity price volatility and infrastructure exposure.

---

### 4. Interactive Dashboard Modules
The Streamlit-based dashboard provides specialized views for different stakeholders:

1.  **🔬 Material Property Explorer**: Real-time search and visualization of material properties compared to global distributions, including AI explainability (SHAP).
2.  **📈 Commodity Signal Dashboard**: Financial tracking with 10-year candlestick charts and automated trend analysis for procurement risk.
3.  **🌉 Infrastructure Risk Scorer**: Geospatial and condition-based risk analysis for large-scale asset portfolios using real NBI data.
4.  **🧪 Inverse Material Designer**: A discovery engine that allows researchers to input target physical constraints (Strength, Density, Budget) to find optimal candidate compositions.
5.  **🌱 ESG Impact Analyser**: A carbon-accounting tool that parses chemical formulas to estimate the CO2 footprint of material substitution scenarios.

---

### 5. Key Achievements & Fixes
*   **Fixed Data Integrity**: Resolved critical issues in NBI data parsing (handling 'N' flags and dictionary-formatted modulus strings).
*   **Model Training**: Successfully executed the full CGNN training pipeline on the Materials Project subset.
*   **Full Integration**: Migrated the entire dashboard from dummy placeholders to live, data-driven outputs.

---

### 6. Next Steps & Future Roadmap
*   **Live GAN Integration**: Fully connecting the generative adversarial network for "de novo" material synthesis.
*   **Geospatial Visualization**: Implementing Mapbox integration for the Infrastructure Risk Scorer.
*   **Real-time API Feeds**: Transitioning from CSV-based commodity data to live financial APIs (e.g., Bloomberg/AlphaVantage).

---
**Report Generated on**: 2026-05-15  
**System Version**: v1.0.0-Stable
