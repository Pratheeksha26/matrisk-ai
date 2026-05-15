import numpy as np
import pandas as pd

class InsuranceCatModel:
    """
    Insurance catastrophe modeling using compound Poisson distribution and TVaR calculation.
    """
    def __init__(self, confidence_level=0.995):
        self.confidence_level = confidence_level

    def simulate_aggregate_loss(self, num_assets, avg_failure_prob, mean_severity, std_severity, num_simulations=10000):
        """
        Monte Carlo simulation of aggregate loss.
        """
        # 1. Number of events (Poisson)
        lambda_param = num_assets * avg_failure_prob
        num_events = np.random.poisson(lambda_param, num_simulations)
        
        aggregate_losses = []
        for n in num_events:
            if n > 0:
                # 2. Severity of each event (Log-normal)
                # Note: sigma and mu for lognormal
                sigma = np.sqrt(np.log(1 + (std_severity/mean_severity)**2))
                mu = np.log(mean_severity) - 0.5 * sigma**2
                severities = np.random.lognormal(mu, sigma, n)
                aggregate_losses.append(np.sum(severities))
            else:
                aggregate_losses.append(0.0)
                
        return np.array(aggregate_losses)

    def calculate_tvar(self, losses):
        """
        Tail Value at Risk (TVaR) beyond the confidence level.
        """
        var_threshold = np.percentile(losses, self.confidence_level * 100)
        tail_losses = losses[losses >= var_threshold]
        return np.mean(tail_losses)

if __name__ == "__main__":
    model = InsuranceCatModel()
    # Example: 100 buildings, 0.8% failure prob, $6.2M mean severity
    losses = model.simulate_aggregate_loss(100, 0.008, 6.2, 5.0)
    tvar = model.calculate_tvar(losses)
    print(f"TVaR at 99.5%: ${tvar:.2f}M")
