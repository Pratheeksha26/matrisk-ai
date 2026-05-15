import torch
import numpy as np
import pandas as pd

def validate_generated_compositions(compositions, target_properties, cost_budget, element_prices, cgnn_model):
    """
    Validate GAN output quality along three axes:
    1. Physical Validity (fractions sum to 1.0, non-negative)
    2. Property Achievement (closeness to target)
    3. Cost Compliance (within budget)
    """
    results = []
    
    # 1. Physical Validity
    sums = torch.sum(compositions, dim=1)
    physical_valid = torch.isclose(sums, torch.ones_like(sums), atol=1e-3)
    non_negative = torch.all(compositions >= 0, dim=1)
    
    # 2. Property Achievement
    # Use frozen CGNN to predict properties of generated alloys
    predicted_props = cgnn_model(compositions)
    error = torch.abs(predicted_props - target_properties) / (torch.abs(target_properties) + 1e-6)
    achieved = torch.all(error < 0.1, dim=1) # Within 10% tolerance
    
    # 3. Cost Compliance
    costs = torch.sum(compositions * element_prices, dim=1)
    cost_valid = costs <= cost_budget.squeeze()
    
    # Aggregated metrics
    validity_rate = torch.mean((physical_valid & non_negative).float()).item() * 100
    achievement_rate = torch.mean(achieved.float()).item() * 100
    cost_compliance_rate = torch.mean(cost_valid.float()).item() * 100
    
    print(f"GAN Validation Results:")
    print(f"- Physical Validity Rate: {validity_rate:.2f}%")
    print(f"- Property Achievement Rate (10% tol): {achievement_rate:.2f}%")
    print(f"- Cost Compliance Rate: {cost_compliance_rate:.2f}%")
    
    return {
        'physical_validity': validity_rate,
        'property_achievement': achievement_rate,
        'cost_compliance': cost_compliance_rate
    }

if __name__ == "__main__":
    pass
