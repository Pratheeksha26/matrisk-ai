import pandas as pd
import numpy as np

def calculate_mqi(material_properties, weights={'tensile': 0.4, 'hardness': 0.4, 'purity': 0.2}):
    """
    Calculate Material Quality Index (MQI).
    """
    # Assuming material_properties has standardized scores (0-1)
    mqi = (weights['tensile'] * material_properties['tensile_strength_ratio'] +
           weights['hardness'] * material_properties['hardness_ratio'] +
           weights['purity'] * (1 - material_properties['defect_density_ratio']))
    return mqi * 100

def calculate_supply_disruption_prob(geopolitical_risk, rarity, energy_intensity):
    """
    Calculate probability of supply disruption.
    """
    # Simple weighted average for demonstration
    prob = 0.5 * geopolitical_risk + 0.3 * rarity + 0.2 * energy_intensity
    return np.clip(prob, 0, 1)

def calculate_substitution_elasticity(property_similarity_score):
    """
    Calculate substitution elasticity.
    """
    # 0 = no substitutes, 1 = readily substitutable
    return property_similarity_score

def calculate_green_premium(price_recycled, price_virgin, carbon_virgin, carbon_recycled):
    """
    Calculate Green Premium Indicator.
    """
    # Avoid division by zero
    carbon_diff = carbon_virgin - carbon_recycled
    if carbon_diff <= 0:
        return 0.0
    
    return (price_recycled - price_virgin) / carbon_diff

def build_fusion_features(commodity_df, material_df):
    """
    Merge commodity and material data to create cross-domain features.
    """
    print("Building cross-domain fusion features...")
    # This would involve complex joins based on commodity-material mapping
    # For now, we'll demonstrate the structure
    
    # Placeholder for MQI
    commodity_df['MQI'] = 75.0 + np.random.normal(0, 5, len(commodity_df)) # Demo values
    commodity_df['MQI_21D_trend'] = commodity_df['MQI'].diff(21)
    
    # Placeholder for Supply Disruption
    commodity_df['supply_disruption_prob'] = 0.1 + np.random.uniform(0, 0.2, len(commodity_df))
    
    return commodity_df

if __name__ == "__main__":
    # Example usage
    commodity_data = pd.DataFrame({'date': pd.date_range('2023-01-01', periods=100)})
    fusion_df = build_fusion_features(commodity_data, None)
    print("Fusion features built.")
    print(fusion_df.head())
