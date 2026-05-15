import pandas as pd
import os
import sys

# Ensure the root directory is in the python path
sys.path.append(os.getcwd())
from src.features.magpie_features import extract_magpie_features
from src.features.financial_features import extract_financial_features
from src.features.nbi_decay import extract_nbi_decay_features
from src.features.fusion_features import build_fusion_features

def main():
    print("Starting master feature engineering pipeline...")
    
    # 1. Material Features
    material_raw = "data/raw/materials_project_data.csv"
    if not os.path.exists(material_raw):
        material_raw = "data/external/DS1_material_properties_5500.csv"
        
    if os.path.exists(material_raw):
        print(f"Loading material data from {material_raw}...")
        df_mat = pd.read_csv(material_raw)
        
        if 'formula_pretty' in df_mat.columns:
            df_mat['composition'] = df_mat['formula_pretty']
        elif 'Formula' in df_mat.columns:
            df_mat['composition'] = df_mat['Formula']
            
        if 'composition' not in df_mat.columns:
             print("Error: Could not find composition column.")
             return

        df_mat_features = extract_magpie_features(df_mat)
        df_mat_features.to_csv("data/processed/material_features_final.csv", index=False)
    
    # 2. Commodity Features
    commodity_dir = "data/raw/commodities"
    if os.path.exists(commodity_dir):
        print(f"Processing commodity data from {commodity_dir}...")
        all_comm_features = []
        for file in os.listdir(commodity_dir):
            if file.endswith(".csv"):
                df_comm = pd.read_csv(os.path.join(commodity_dir, file))
                try:
                    df_comm_features = extract_financial_features(df_comm)
                    df_comm_final = build_fusion_features(df_comm_features, None)
                    df_comm_final['commodity'] = file.replace("_prices.csv", "")
                    all_comm_features.append(df_comm_final)
                except Exception as e:
                    print(f"Error processing {file}: {e}")
        
        if all_comm_features:
            pd.concat(all_comm_features).to_csv("data/processed/commodity_features_final.csv", index=False)
            print("Successfully processed all commodities.")
    
    # 3. Infrastructure Features
    infra_raw = "data/external/DS3_infrastructure_bridges_5000.csv"
    if os.path.exists(infra_raw):
        print(f"Loading infrastructure data from {infra_raw}...")
        df_infra = pd.read_csv(infra_raw)
        
        # Robust column mapping (keyword search)
        for col in df_infra.columns:
            c_low = str(col).lower()
            if 'condition' in c_low:
                df_infra.rename(columns={col: 'condition_rating'}, inplace=True)
            elif 'material' in c_low:
                df_infra.rename(columns={col: 'material_kind'}, inplace=True)
            elif 'age' in c_low:
                df_infra.rename(columns={col: 'age_years'}, inplace=True)
            elif 'structure' in c_low:
                df_infra.rename(columns={col: 'structure_id'}, inplace=True)

        if 'material_kind' not in df_infra.columns:
            print("Warning: material_kind column not found in infrastructure data.")
        else:
            df_infra_features = extract_nbi_decay_features(df_infra)
            df_infra_features.to_csv("data/processed/infrastructure_features_final.csv", index=False)
        
    print("Feature engineering pipeline complete.")

if __name__ == "__main__":
    main()
