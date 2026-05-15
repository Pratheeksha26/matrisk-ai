import torch
import torch.nn.functional as F
from torch.nn import Linear, Sequential, ReLU, BatchNorm1d
from torch_geometric.nn import CGConv, GlobalAttention

class CGNN(torch.nn.Module):
    """
    Crystal Graph Neural Network (CGNN) using CGConv layers.
    Multi-task architecture for material property prediction.
    """
    def __init__(self, node_dim, edge_dim, hidden_dim=128, output_dim=4):
        super(CGNN, self).__init__()
        
        # Message Passing Layers
        self.conv1 = CGConv(node_dim, edge_dim)
        self.conv2 = CGConv(node_dim, edge_dim)
        self.conv3 = CGConv(node_dim, edge_dim)
        
        # Batch Normalization
        self.bn1 = BatchNorm1d(node_dim)
        self.bn2 = BatchNorm1d(node_dim)
        self.bn3 = BatchNorm1d(node_dim)
        
        # Attention Pooling
        # GlobalAttention computes weighted sums of node features
        self.pooling = GlobalAttention(gate_nn=Sequential(Linear(node_dim, 1)))
        
        # Multi-task Prediction Heads
        # Target properties: formation energy, band gap, bulk modulus, shear modulus
        self.head_formation = Sequential(
            Linear(node_dim, hidden_dim), ReLU(), Linear(hidden_dim, 1)
        )
        self.head_bandgap = Sequential(
            Linear(node_dim, hidden_dim), ReLU(), Linear(hidden_dim, 1)
        )
        self.head_bulk = Sequential(
            Linear(node_dim, hidden_dim), ReLU(), Linear(hidden_dim, 1)
        )
        self.head_shear = Sequential(
            Linear(node_dim, hidden_dim), ReLU(), Linear(hidden_dim, 1)
        )

    def forward(self, data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        
        # 1. Message Passing
        x = self.conv1(x, edge_index, edge_attr)
        x = self.bn1(x)
        x = F.relu(x)
        
        x = self.conv2(x, edge_index, edge_attr)
        x = self.bn2(x)
        x = F.relu(x)
        
        x = self.conv3(x, edge_index, edge_attr)
        x = self.bn3(x)
        x = F.relu(x)
        
        # 2. Global Pooling (Attention-based)
        # Condenses node features into a single crystal-level representation
        x_pool = self.pooling(x, batch)
        
        # 3. Multi-task Heads
        out_formation = self.head_formation(x_pool)
        out_bandgap = self.head_bandgap(x_pool)
        out_bulk = self.head_bulk(x_pool)
        out_shear = self.head_shear(x_pool)
        
        # Combine outputs: [formation, bandgap, bulk, shear]
        return torch.cat([out_formation, out_bandgap, out_bulk, out_shear], dim=1)

if __name__ == "__main__":
    # Test model instantiation
    model = CGNN(node_dim=6, edge_dim=40)
    print(model)
