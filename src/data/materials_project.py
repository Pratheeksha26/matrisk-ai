from mp_api.client import MPRester
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_materials_data(api_key, query_params, output_path, chunk_size=1000):
    """
    Fetch data from Materials Project API in chunks to save memory.
    """
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    with MPRester(api_key) as mpr:
        print("Searching Materials Project database...")
        # Get all material IDs first (very light)
        mids = mpr.materials.summary.search(fields=["material_id"])
        total = min(len(mids), 10000) # Limit to 10,000 for faster development
        print(f"Total materials to retrieve: {total} (Limited from {len(mids)})")

        # Fetch in chunks
        for i in range(0, total, chunk_size):
            chunk_mids = [doc.material_id for doc in mids[i:i + chunk_size]]
            print(f"Fetching chunk {i//chunk_size + 1} ({i} to {i + len(chunk_mids)})...")
            
            docs = mpr.materials.summary.search(
                material_ids=chunk_mids,
                fields=query_params
            )
            
            df_chunk = pd.DataFrame([doc.dict() for doc in docs])
            
            # Append to CSV
            mode = 'w' if i == 0 else 'a'
            header = True if i == 0 else False
            df_chunk.to_csv(output_path, mode=mode, header=header, index=False)
            
        print(f"Successfully saved all entries to {output_path}")

if __name__ == "__main__":
    api_key = os.getenv("MP_API_KEY")
    if not api_key:
        print("Please set MP_API_KEY in your .env file")
    else:
        # Fields required as per PDF (page 21-23)
        fields = [
            "material_id", 
            "formula_pretty", 
            "symmetry", # Contains crystal_system and spacegroup_number
            "formation_energy_per_atom", 
            "band_gap", 
            "bulk_modulus", 
            "shear_modulus", 
            "homogeneous_poisson", 
            "density",
            "structure"
        ]
        
        output = "data/raw/materials_project_data.csv"
        # Note: Fetching 100K+ entries might take time and require pagination in real usage
        # This is a base implementation
        fetch_materials_data(api_key, fields, output)
