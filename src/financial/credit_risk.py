import numpy as np
import pandas as pd

class CreditRiskModel:
    """
    Module to convert survival curves into financial credit risk metrics.
    """
    def __init__(self, lgd_default=0.45):
        self.lgd_default = lgd_default

    def calculate_pd(self, survival_prob):
        """
        Probability of Default (PD) at a specific time t.
        PD(t) = 1 - S(t|x)
        """
        return 1.0 - survival_prob

    def estimate_lgd(self, material_failure_mode):
        """
        Estimate Loss Given Default based on failure mode severity.
        Ductile = lower LGD, Brittle = higher LGD.
        """
        mapping = {
            'ductile': 0.35,
            'brittle': 0.75,
            'fatigue': 0.50
        }
        return mapping.get(material_failure_mode.lower(), self.lgd_default)

    def compute_expected_loss(self, pd, lgd, ead):
        """
        EL = PD * LGD * EAD
        """
        return pd * lgd * ead

    def portfolio_risk_summary(self, assets_df):
        """
        Aggregate risk metrics for a portfolio of infrastructure loans.
        """
        assets_df['PD'] = self.calculate_pd(assets_df['survival_prob'])
        assets_df['EL'] = assets_df['PD'] * assets_df['LGD'] * assets_df['EAD']
        
        total_el = assets_df['EL'].sum()
        portfolio_pd = total_el / assets_df['EAD'].sum()
        
        return {
            'total_expected_loss': total_el,
            'weighted_avg_pd': portfolio_pd
        }

if __name__ == "__main__":
    # Example assets
    data = {
        'asset_id': ['BR-001', 'PL-001'],
        'survival_prob': [0.92, 0.85],
        'LGD': [0.35, 0.45],
        'EAD': [12.0, 45.0]
    }
    df = pd.DataFrame(data)
    model = CreditRiskModel()
    summary = model.portfolio_risk_summary(df)
    print(summary)
