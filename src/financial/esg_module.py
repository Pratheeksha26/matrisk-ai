import pandas as pd

class ESGModule:
    """
    ESG and Sustainability Analytics module for material substitution and carbon footprint.
    """
    def __init__(self):
        # Emission factors (kg CO2 / kg material) - Sample data from page 13
        self.emission_factors = {
            'aluminum_virgin': 12.0,
            'aluminum_recycled': 0.6,
            'steel_bof': 2.0,
            'steel_eaf': 0.4
        }

    def calculate_carbon_intensity(self, material, quantity_kg):
        """
        Compute CO2 equivalent emissions.
        """
        factor = self.emission_factors.get(material.lower(), 1.0)
        return quantity_kg * factor

    def substitution_impact_analysis(self, original_material, new_material, quantity_kg):
        """
        Compute impact of switching materials.
        Returns carbon reduction and cost delta.
        """
        old_emissions = self.calculate_carbon_intensity(original_material, quantity_kg)
        new_emissions = self.calculate_carbon_intensity(new_material, quantity_kg)
        
        reduction = old_emissions - new_emissions
        reduction_pct = (reduction / old_emissions) * 100 if old_emissions > 0 else 0
        
        return {
            'carbon_reduction_kg': reduction,
            'reduction_percentage': reduction_pct
        }

    def score_green_bond_eligibility(self, project_data):
        """
        Assess project against ICMA Green Bond Principles.
        """
        # Criteria: Carbon intensity below threshold, renewable energy use, etc.
        score = 0
        if project_data.get('carbon_intensity_reduction_pct', 0) > 30:
            score += 50
        if project_data.get('use_recycled_materials', False):
            score += 50
            
        return score # 0-100

if __name__ == "__main__":
    esg = ESGModule()
    impact = esg.substitution_impact_analysis('aluminum_virgin', 'aluminum_recycled', 1000)
    print(impact)
