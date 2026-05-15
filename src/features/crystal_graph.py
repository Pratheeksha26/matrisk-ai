import numpy as np
import torch
from torch_geometric.data import Data
from pymatgen.core import Structure
from pymatgen.analysis.local_env import VoronoiNN
import os
import pandas as pd

def gaussian_expansion(distances, centers, width=0.5):
    """
    Expand distances using Gaussian basis functions.
    """
    return np.exp(-((distances[:, None] - centers[None, :]) / width) ** 2)

def structure_to_graph(structure, cutoff=8.0):
    """
    Convert a Pymatgen structure to a PyTorch Geometric Data object.
    """
    # 1. Get nodes (atoms)
    # Node features: atomic number, electronegativity, atomic radius, etc.
    node_features = []
    for site in structure:
        # Pymatgen provides easy access to elemental properties
        feat = [
            float(site.specie.number),
            float(site.specie.X) if site.specie.X else 0.0,
            float(site.specie.atomic_radius) if site.specie.atomic_radius else 0.0,
            float(site.specie.mendeleev_no) if site.specie.mendeleev_no else 0.0,
            float(site.specie.group) if site.specie.group else 0.0,
            float(site.specie.row) if site.specie.row else 0.0
        ]
        node_features.append(feat)
    
    node_features = torch.tensor(node_features, dtype=torch.float)
    
    # 2. Get edges (bonds)
    all_neighbors = structure.get_all_neighbors(cutoff)
    
    edge_index = []
    edge_attr = []
    
    # Gaussian expansion centers
    centers = np.linspace(0.5, cutoff, 40)
    
    for i, neighbors in enumerate(all_neighbors):
        for neigh in neighbors:
            edge_index.append([i, neigh.index])
            # Distance feature
            dist = neigh.nn_distance
            # Gaussian expansion
            dist_feat = gaussian_expansion(np.array([dist]), centers)
            edge_attr.append(dist_feat[0])
            
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_attr, dtype=torch.float)
    
    return Data(x=node_features, edge_index=edge_index, edge_attr=edge_attr)

def structures_to_dataset(df, structure_col='structure'):
    """
    Convert a DataFrame of structures and properties into a list of Data objects.
    """
    import ast
    from pymatgen.core import Structure
    
    dataset = []
    print(f"Converting {len(df)} structures to graphs...")
    
    for idx, row in df.iterrows():
        try:
            # Parse Python-style dictionary string from CSV
            s_str = row[structure_col]
            if isinstance(s_str, str):
                s_dict = ast.literal_eval(s_str)
            else:
                s_dict = s_str
                
            structure = Structure.from_dict(s_dict)
            
            # Create graph
            graph = structure_to_graph(structure)
            
            # Add target properties [formation, bandgap, bulk, shear]
            # Handle NaN values explicitly
            def clean(val):
                return float(val) if pd.notnull(val) else 0.0
                
            targets = [
                clean(row.get('formation_energy_per_atom', 0.0)),
                clean(row.get('band_gap', 0.0)),
                clean(row.get('bulk_modulus', 0.0)),
                clean(row.get('shear_modulus', 0.0))
            ]
            graph.y = torch.tensor([targets], dtype=torch.float)
            
            dataset.append(graph)
        except Exception as e:
            continue
            
    print(f"Dataset created with {len(dataset)} valid graphs.")
    return dataset

if __name__ == "__main__":
    # Example: Create a simple BCC Iron structure
    from pymatgen.core import Lattice
    lattice = Lattice.cubic(2.86)
    structure = Structure(lattice, ["Fe", "Fe"], [[0, 0, 0], [0.5, 0.5, 0.5]])
    
    graph = structure_to_graph(structure)
    print(f"Graph created: {graph}")
    print(f"Node features shape: {graph.x.shape}")
    print(f"Edge index shape: {graph.edge_index.shape}")
    print(f"Edge features shape: {graph.edge_attr.shape}")
