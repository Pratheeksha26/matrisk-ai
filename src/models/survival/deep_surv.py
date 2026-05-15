import torch
import torch.nn as nn
import numpy as np

class DeepSurv(nn.Module):
    """
    Deep Survival Network for predicting hazard rates of infrastructure assets.
    """
    def __init__(self, input_dim, hidden_dim=64):
        super(DeepSurv, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1) # Output is the risk score (log-hazard)
        )

    def forward(self, x):
        return self.network(x)

def negative_log_likelihood(risk_scores, durations, events):
    """
    Partial Likelihood Loss for Cox Proportional Hazards.
    """
    # Simplified version for demonstration
    # In practice, use a specialized library or more robust implementation
    # risk_scores: predicted log-hazard
    # durations: time-to-event
    # events: binary indicator (1=failed, 0=censored)
    
    # Sort by duration
    indices = np.argsort(-durations)
    risk_scores = risk_scores[indices]
    events = events[indices]
    
    # Log-sum-exp trick for stability
    exp_risk = torch.exp(risk_scores)
    risk_accum = torch.cumsum(exp_risk, dim=0)
    
    loss = -torch.mean(events * (risk_scores - torch.log(risk_accum)))
    return loss

if __name__ == "__main__":
    # Test model
    model = DeepSurv(input_dim=10)
    print(model)
