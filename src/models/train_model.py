import torch
import torch.nn as nn
import os
import sys

# Ensure the root directory is in the python path
sys.path.append(os.getcwd())
from torch_geometric.loader import DataLoader
import mlflow
import mlflow.pytorch
import os
import sys

# Ensure the root directory is in the python path
sys.path.append(os.getcwd())
import pandas as pd
from src.models.cgnn.model import CGNN
from src.models.pinn.physics_losses import compute_pinn_loss

def train_epoch(model, loader, optimizer, device, criterion, lambda_physics):
    model.train()
    total_loss = 0
    for data in loader:
        data = data.to(device)
        optimizer.zero_grad()
        
        out = model(data)
        
        # 1. Data Loss
        loss_data = criterion(out, data.y)
        
        # 2. Physics Loss (PINN)
        loss_physics = compute_pinn_loss(out, lambda_physics=lambda_physics)
        
        loss = loss_data + loss_physics
        loss.backward()
        optimizer.step()
        
        # Access num_graphs safely from the batch
        batch_size = data.y.size(0)
        total_loss += loss.item() * batch_size
        
    return total_loss / len(loader.dataset)

def train_model(train_dataset, val_dataset, params):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Wrap datasets in DataLoader
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32)
    
    model = CGNN(node_dim=params['node_dim'], edge_dim=params['edge_dim']).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=params['lr'])
    criterion = nn.MSELoss()
    
    mlflow.set_experiment("matrisk-cgnn-pinn")
    
    with mlflow.start_run():
        mlflow.log_params(params)
        
        for epoch in range(params['epochs']):
            train_loss = train_epoch(model, train_loader, optimizer, device, criterion, params['lambda_physics'])
            # Validation step...
            print(f"Epoch {epoch}: Train Loss {train_loss:.4f}")
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            
        # Save model manually as backup
        save_dir = "models"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        torch.save(model.state_dict(), os.path.join(save_dir, "cgnn_model.pt"))
        print(f"Model saved manually to {os.path.join(save_dir, 'cgnn_model.pt')}")

        try:
            # Save model to MLflow
            mlflow.pytorch.log_model(model, "model")
            print("Model logged to MLflow.")
        except Exception as e:
            print(f"MLflow logging warning: {e}")
            
        print("Training complete.")

if __name__ == "__main__":
    import pandas as pd
    from src.features.crystal_graph import structures_to_dataset
    from sklearn.model_selection import train_test_split
    
    print("Loading processed data...")
    # We need the 'structure' column which is in raw data
    raw_path = "data/raw/materials_project_data.csv"
    if os.path.exists(raw_path):
        df = pd.read_csv(raw_path)
        
        # Limit to 1000 for a quick training demo
        df_sample = df.head(1000)
        
        print("Converting materials to crystal graphs (this may take a minute)...")
        full_dataset = structures_to_dataset(df_sample, structure_col='structure')
        
        if len(full_dataset) > 0:
            train_data, test_data = train_test_split(full_dataset, test_size=0.2)
            
            params = {
                'node_dim': 6,  # 6 properties from crystal_graph.py
                'edge_dim': 40, # 40 Gaussian expansion centers
                'lr': 0.0001,
                'epochs': 10,   # Short run for demonstration
                'lambda_physics': 0.1
            }
            
            print(f"Starting training on {len(train_data)} samples...")
            train_model(train_data, test_data, params)
        else:
            print("Error: No valid graphs could be created.")
    else:
        print("Error: materials_project_data.csv not found in data/raw/")
