import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression

def calculate_degradation_slope(group):
    """
    Calculate the slope of condition ratings over time for a single asset.
    """
    if len(group) < 2:
        return 0.0
    
    # Simple linear regression to find the rate of decay
    X = group['year_built'].values.reshape(-1, 1) # Or inspection years if available
    y = group['condition_rating'].values
    
    model = LinearRegression()
    model.fit(X, y)
    return model.coef_[0]

def extract_nbi_decay_features(df):
    """
    Extract decay features from NBI data.
    """
    print("Extracting NBI decay features...")
    # Group by asset and material kind to find typical decay rates
    # Note: DS3 has 10 assets, so we can compute these
    
    decay_features = df.groupby(['material_kind'])['condition_rating'].mean().reset_index()
    decay_features.rename(columns={'condition_rating': 'avg_material_condition'}, inplace=True)
    
    # Calculate age-weighted degradation
    df['degradation_per_year'] = (9 - df['condition_rating']) / df['age_years']
    
    # Material specific average degradation
    material_decay = df.groupby('material_kind')['degradation_per_year'].mean().to_dict()
    df['expected_material_decay'] = df['material_kind'].map(material_decay)
    
    # Relative degradation (is this specific bridge decaying faster than average for its material?)
    df['relative_decay_index'] = df['degradation_per_year'] / df['expected_material_decay']
    
    return df

if __name__ == "__main__":
    # Example using DS3
    data_path = "data/external/DS3_infrastructure_bridges_5000.csv"
    if os.path.exists(data_path):
        # The sample data might have different columns, let's adjust to DS3 schema
        df = pd.read_csv(data_path)
        # Standardizing names if they don't match
        if 'Condition (1-9)' in df.columns:
            df.rename(columns={'Condition (1-9)': 'condition_rating', 'Material': 'material_kind', 'Age (yr)': 'age_years'}, inplace=True)
        
        features_df = extract_nbi_decay_features(df)
        output_path = "data/interim/nbi_decay_features.csv"
        features_df.to_csv(output_path, index=False)
        print(f"NBI decay features saved to {output_path}")
    else:
        print("DS3 data not found.")
