import numpy as np
import pandas as pd

class StressTestEngine:
    """
    Monte Carlo stress testing engine for material-financial shock scenarios.
    """
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def run_scenario(self, scenario_name, shock_magnitude, num_paths=10000):
        """
        Run a specific stress scenario.
        """
        print(f"Running stress test: {scenario_name} (Shock: {shock_magnitude})")
        
        results = []
        for _ in range(num_paths):
            # 1. Apply Material Shock
            # (e.g., increase maintenance costs or reduce asset RUL)
            
            # 2. Simulate Financial Impact
            # (e.g., random walk for commodity prices with shifted mean)
            
            # 3. Compute Portfolio P&L
            pnl = np.random.normal(loc=-shock_magnitude, scale=0.5) # Simplified
            results.append(pnl)
            
        return np.array(results)

    def rare_earth_crisis_scenario(self):
        """
        Scenario: China restricts exports by 40%.
        Impact: EV material costs spike, infrastructure maintenance increases.
        """
        return self.run_scenario("Rare Earth Crisis", 0.40)

    def steel_quality_shift_scenario(self):
        """
        Scenario: Major mill shifts to lower-grade output (15% strength drop).
        Impact: Infrastructure repair acceleration, insurance claims spike.
        """
        return self.run_scenario("Steel Quality Shift", 0.15)

    def climate_corrosion_scenario(self):
        """
        Scenario: +2°C scenario accelerates corrosion 30%.
        Impact: RUL shortens, portfolio EL increases.
        """
        return self.run_scenario("Climate Corrosion", 0.30)

    def recycled_mandate_scenario(self):
        """
        Scenario: EU mandates 50% recycled content.
        Impact: Virgin demand drops, price restructuring, stranded assets.
        """
        return self.run_scenario("Recycled Mandate", 0.50)

    def novel_alloy_discovery_scenario(self):
        """
        Scenario: New alloy 20% stronger/cheaper.
        Impact: Steel demand shock, substitution cascade.
        """
        return self.run_scenario("Novel Alloy Discovery", 0.20)

if __name__ == "__main__":
    engine = StressTestEngine(portfolio=None)
    results = engine.rare_earth_crisis_scenario()
    print(f"Mean Stress P&L: {np.mean(results):.4f}")
