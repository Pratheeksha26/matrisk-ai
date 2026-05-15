import torch
import numpy as np

def audit_physics_constraints(predictions, tolerance=0.1):
    """
    Audit predictions against physics constraints and report satisfaction rate.
    predictions: [formation, bandgap, bulk(K), shear(G), poisson(v)]
    """
    k = predictions[:, 2]
    g = predictions[:, 3]
    v = predictions[:, 4]
    
    # 1. Elastic Consistency: E = 2G(1+v) = 3K(1-2v)
    # Check if 2G(1+v) is close to 3K(1-2v)
    term1 = 2 * g * (1 + v)
    term2 = 3 * k * (1 - 2 * v)
    elastic_violation = torch.abs(term1 - term2) / torch.abs(term1 + 1e-6)
    elastic_satisfied = elastic_violation < tolerance
    
    # 2. Poisson Bounds: -1 < v < 0.5
    poisson_satisfied = (v > -1) & (v < 0.5)
    
    # Overall satisfaction
    all_satisfied = elastic_satisfied & poisson_satisfied
    satisfaction_rate = torch.mean(all_satisfied.float()).item() * 100
    
    print(f"Physics Audit Results:")
    print(f"- Elastic Consistency Satisfaction: {torch.mean(elastic_satisfied.float()).item()*100:.2f}%")
    print(f"- Poisson Bounds Satisfaction: {torch.mean(poisson_satisfied.float()).item()*100:.2f}%")
    print(f"- Overall Constraint Satisfaction: {satisfaction_rate:.2f}%")
    
    return satisfaction_rate

if __name__ == "__main__":
    # Test with dummy data
    preds = torch.tensor([
        [0, 0, 150.0, 80.0, 0.3], # Near consistent
        [0, 0, 150.0, 80.0, 0.8], # Invalid poisson
    ])
    audit_physics_constraints(preds)
