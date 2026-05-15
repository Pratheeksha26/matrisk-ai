import pytest
import torch
import pandas as pd
from src.models.survival.deep_surv import DeepSurv
from src.financial.credit_risk import CreditRiskModel
from src.financial.cat_model import InsuranceCatModel

def test_material_to_credit_risk_flow():
    """
    Integration test: GNN/Survival output -> PD -> Expected Loss.
    """
    # 1. Simulate Survival Model output
    # Input features (e.g., 10 features)
    x = torch.randn(1, 10)
    model = DeepSurv(input_dim=10)
    risk_score = model(x).item()
    
    # Map risk score to survival probability (proxy)
    survival_prob = 1.0 / (1.0 + np.exp(risk_score))
    
    # 2. Credit Risk conversion
    credit_model = CreditRiskModel()
    pd_val = credit_model.calculate_pd(survival_prob)
    el_val = credit_model.compute_expected_loss(pd_val, lgd=0.35, ead=10.0)
    
    assert 0 <= pd_val <= 1
    assert el_val >= 0
    print(f"Integration Flow OK: PD={pd_val:.4f}, EL={el_val:.4f}")

def test_insurance_cat_simulation():
    """
    Integration test: Insurance aggregate loss simulation.
    """
    cat_model = InsuranceCatModel()
    losses = cat_model.simulate_aggregate_loss(num_assets=10, avg_failure_prob=0.1, mean_severity=1.0, std_severity=0.5, num_simulations=100)
    tvar = cat_model.calculate_tvar(losses)
    
    assert len(losses) == 100
    assert tvar >= 0

if __name__ == "__main__":
    import numpy as np
    test_material_to_credit_risk_flow()
    test_insurance_cat_simulation()
