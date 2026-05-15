import requests
import pandas as pd
import os

def fetch_aflow_data(query, fields, output_path):
    """
    Fetch data from AFLOW REST API.
    query: AFLOW query string (e.g. 'species(Fe,O),nbelements(2)')
    fields: list of fields to fetch.
    """
    # AFLOW API endpoint: http://aflow.org/API/aurl/
    # For simplicity, we'll use a basic request approach
    base_url = "http://aflow.org/API/query-layer/?"
    fields_str = ",".join(fields)
    url = f"{base_url}{query}&{fields_str}"
    
    print(f"Querying AFLOW: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))
            df.to_csv(output_path, index=False)
            print(f"Saved {len(df)} entries to {output_path}")
        else:
            print(f"AFLOW API error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example fields as per PDF
    fields = [
        "compound", "formation_energy_per_atom", "band_gap", 
        "bulk_modulus_voigt", "shear_modulus_voigt", "density"
    ]
    query = "nbelements(1),crystal_system(cubic)" # Example filter
    output = "data/raw/aflow_data.csv"
    
    fetch_aflow_data(query, fields, output)
