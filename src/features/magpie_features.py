from matminer.featurizers.composition import ElementProperty
import pandas as pd
import os
import joblib

def extract_magpie_features(df, composition_col='composition', output_path=None):
    """
    Extract 132 Magpie compositional descriptors from chemical formulas.
    """
    print(f"Extracting Magpie features from column '{composition_col}'...")
    
    # Initialize the Magpie featurizer
    ep = ElementProperty.from_preset("magpie")
    
    # Featurize the dataframe
    # This adds 132 columns automatically
    df_features = ep.featurize_dataframe(df, col_id=composition_col, ignore_errors=True)
    
    if output_path:
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
        df_features.to_csv(output_path, index=False)
        print(f"Magpie features saved to {output_path}")
        
    return df_features

if __name__ == "__main__":
    # Example usage with sample data
    raw_data_path = "data/external/DS1_material_properties_5500.csv"
    if os.path.exists(raw_data_path):
        df = pd.read_csv(raw_data_path)
        # Ensure composition column exists (might be 'formula_pretty' or 'composition')
        if 'formula_pretty' in df.columns and 'composition' not in df.columns:
            df['composition'] = df['formula_pretty']
            
        output = "data/interim/material_magpie_features.csv"
        extract_magpie_features(df, output_path=output)
    else:
        print("Raw material data not found. Please run data acquisition first.")
