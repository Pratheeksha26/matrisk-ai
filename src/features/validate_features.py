import pandas as pd
import great_expectations as ge
import os

def validate_material_features(df):
    """
    Validate material features using Great Expectations.
    """
    print("Validating material features...")
    ge_df = ge.from_pandas(df)
    
    # Check for expected number of Magpie features (132 + original cols)
    # ge_df.expect_table_column_count_to_be_between(130, 150)
    
    # Check for nulls in critical columns
    ge_df.expect_column_values_to_not_be_null("composition")
    
    # Check physical plausibility (example: density > 0)
    if 'density' in ge_df.columns:
        ge_df.expect_column_values_to_be_between("density", min_value=0, max_value=25)
        
    results = ge_df.validate()
    return results.success

def validate_financial_features(df):
    """
    Validate financial features.
    """
    print("Validating financial features...")
    ge_df = ge.from_pandas(df)
    
    # RSI should be between 0 and 100
    if 'rsi_14' in ge_df.columns:
        ge_df.expect_column_values_to_be_between("rsi_14", min_value=0, max_value=100)
        
    # Returns should not be extreme (thresholding for data quality)
    if 'daily_return' in ge_df.columns:
        ge_df.expect_column_values_to_be_between("daily_return", min_value=-0.5, max_value=0.5)
        
    results = ge_df.validate()
    return results.success

if __name__ == "__main__":
    processed_mat = "data/processed/material_features_final.csv"
    if os.path.exists(processed_mat):
        df = pd.read_csv(processed_mat)
        success = validate_material_features(df)
        print(f"Material validation success: {success}")
