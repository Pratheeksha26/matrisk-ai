import numpy as np

class MatRiskLab:
    """
    Gamified simulator for material-financial analysts.
    """
    def __init__(self, level=1):
        self.level = level
        self.score = 0
        self.quarter = 1
        self.portfolio = self._init_portfolio(level)

    def _init_portfolio(self, level):
        if level == 1:
            return {'assets': ['BR-001'], 'commodities': ['Steel HRC']}
        elif level == 2:
            return {'assets': ['BR-001', 'BR-002', 'PL-001'], 'commodities': ['Steel HRC', 'Copper', 'Aluminum']}
        return {}

    def next_quarter(self, player_decisions):
        """
        Process a quarter in the simulation.
        """
        print(f"Processing Quarter {self.quarter}...")
        
        # 1. Inject Random Material Event (if Level > 1)
        event = None
        if self.level >= 2 and self.quarter == 2:
            event = "Corrosion spike on PL-001"
            
        # 2. Update Market Prices
        # 3. Score Player Decisions (Sharpe, Risk, ESG)
        self.score += 500 # Simple increment for demo
        self.quarter += 1
        
        return {
            'event': event,
            'current_score': self.score,
            'quarter': self.quarter
        }

if __name__ == "__main__":
    game = MatRiskLab(level=2)
    res = game.next_quarter({'action': 'hedge'})
    print(res)
