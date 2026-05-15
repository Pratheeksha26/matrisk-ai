import torch
import torch.nn as nn

class Generator(nn.Module):
    """
    Cost-constrained Generator for alloy composition generation.
    Architecture: 4-layer MLP with LayerNorm and LeakyReLU.
    """
    def __init__(self, noise_dim, target_dim, output_dim, hidden_dim=256):
        super(Generator, self).__init__()
        # Input: noise vector z + target property vector + cost budget
        input_dim = noise_dim + target_dim + 1 
        
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.LeakyReLU(0.2),
            
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.LeakyReLU(0.2),
            
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.LeakyReLU(0.2),
            
            nn.Linear(hidden_dim, output_dim),
            nn.Softmax(dim=1) # Ensure compositions sum to 1.0
        )

    def forward(self, z, target_properties, cost_budget):
        # Concatenate inputs
        x = torch.cat([z, target_properties, cost_budget], dim=1)
        return self.model(x)

class Critic(nn.Module):
    """
    Critic (Discriminator) for WGAN-GP.
    Architecture: 3-layer MLP with spectral normalization.
    """
    def __init__(self, input_dim, hidden_dim=256):
        super(Critic, self).__init__()
        
        self.model = nn.Sequential(
            nn.utils.spectral_norm(nn.Linear(input_dim, hidden_dim)),
            nn.LeakyReLU(0.2),
            
            nn.utils.spectral_norm(nn.Linear(hidden_dim, hidden_dim)),
            nn.LeakyReLU(0.2),
            
            nn.utils.spectral_norm(nn.Linear(hidden_dim, 1))
        )

    def forward(self, x):
        return self.model(x)

if __name__ == "__main__":
    # noise_dim=100, target_dim=4 properties, output_dim=10 elements
    gen = Generator(100, 4, 10)
    critic = Critic(10)
    print(gen)
    print(critic)
