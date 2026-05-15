import pandas as pd
import numpy as np

class SupplyChainRiskModule:
    """
    Supply chain risk analysis and dynamic LTV haircut modeling.
    """
    def __init__(self):
        pass

    def calculate_collateral_quality_score(self, mqi, supply_prob, substitution_elasticity):
        """
        Compute a quality score for material collateral.
        Higher MQI and Substitution Elasticity increase score.
        Higher Supply Prob (risk) decreases score.
        """
        score = (0.4 * mqi + 0.3 * (1 - supply_prob) * 100 + 0.3 * substitution_elasticity * 100)
        return np.clip(score, 0, 100)

    def dynamic_ltv_haircut(self, base_ltv, collateral_quality_score):
        """
        Adjust Loan-to-Value based on material quality.
        Lower quality = higher haircut (lower LTV).
        """
        # Example: for every 10 points below 80, add 5% haircut
        if collateral_quality_score < 80:
            haircut = (80 - collateral_quality_score) / 10 * 0.05
        else:
            haircut = 0
            
        adjusted_ltv = base_ltv - haircut
        return max(adjusted_ltv, 0.3) # Minimum floor

if __name__ == "__main__":
    scm = SupplyChainRiskModule()
    score = scm.calculate_collateral_quality_score(mqi=75, supply_prob=0.4, substitution_elasticity=0.6)
    ltv = scm.dynamic_ltv_haircut(0.8, score)
    print(f"Collateral Quality: {score:.2f}, Adjusted LTV: {ltv:.2%}")
