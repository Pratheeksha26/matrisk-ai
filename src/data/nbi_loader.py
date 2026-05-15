import pandas as pd
import os
import requests
import zipfile
import io

def download_nbi_data(year, state_code, output_dir):
    """
    Download NBI data for a specific year and state (or all states).
    FHWA provides data in ZIP or TXT files.
    """
    base_url = "https://www.fhwa.dot.gov/bridge/nbi/2023/delimited/"
    filename = f"{state_code}{str(year)[-2:]}.txt"
    url = f"{base_url}{filename}"
    
    print(f"Downloading NBI data from {url}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded NBI data to {file_path}")
            return file_path
        else:
            print(f"Failed to download NBI data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def load_and_preprocess_nbi(file_path):
    """
    Load NBI data and select relevant columns for MatRisk AI.
    Relevant columns as per PDF: material type, condition ratings, traffic.
    """
    # NBI has specific column codes (e.g., Item 43A for Material Type)
    # We'll map these to readable names
    column_mapping = {
        'STRUCTURE_NUMBER_008': 'asset_id',
        'YEAR_BUILT_027': 'year_built',
        'ADT_029': 'annual_traffic',
        'DECK_COND_058': 'deck_condition',
        'SUPERSTRUCTURE_COND_059': 'superstructure_condition',
        'SUBSTRUCTURE_COND_060': 'substructure_condition',
        'STRUCTURE_KIND_043A': 'material_kind',
        'STRUCTURE_TYPE_043B': 'structure_type',
        'PERCENT_ADT_TRUCK_109': 'truck_traffic_pct'
    }
    
    # NBI delimited files use single quote as text qualifier
    df = pd.read_csv(file_path, low_memory=False, quotechar="'")
    df = df[list(column_mapping.keys())]
    df = df.rename(columns=column_mapping)
    
    # Calculate age
    current_year = pd.Timestamp.now().year
    df['age_years'] = current_year - df['year_built']
    
    return df

if __name__ == "__main__":
    save_dir = "data/raw/nbi"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Download Florida (FL) data for 2023
    raw_file = download_nbi_data(2023, "FL", save_dir)
    
    # If file exists, process it
    if raw_file and os.path.exists(raw_file):
        print(f"Processing NBI data from {raw_file}...")
        processed_df = load_and_preprocess_nbi(raw_file)
        
        interim_dir = "data/interim"
        if not os.path.exists(interim_dir):
            os.makedirs(interim_dir)
            
        processed_file = os.path.join(interim_dir, "nbi_processed.csv")
        processed_df.to_csv(processed_file, index=False)
        print(f"NBI data processed and saved to {processed_file}.")

