import torch
import torch.nn as nn
import os
import sys

# Ensure the root directory is in the python path
sys.path.append(os.getcwd())
import torch.optim as optim
from src.models.gan.generator import Generator, Critic

def compute_gradient_penalty(critic, real_samples, fake_samples, device):
    """
    Gradient Penalty for WGAN-GP.
    """
    alpha = torch.rand(real_samples.size(0), 1).to(device)
    interpolates = (alpha * real_samples + (1 - alpha) * fake_samples).requires_grad_(True)
    d_interpolates = critic(interpolates)
    
    fake = torch.ones(real_samples.size(0), 1).to(device)
    gradients = torch.autograd.grad(
        outputs=d_interpolates,
        inputs=interpolates,
        grad_outputs=fake,
        create_graph=True,
        retain_graph=True,
        only_inputs=True
    )[0]
    
    gradients = gradients.view(gradients.size(0), -1)
    gradient_penalty = ((gradients.norm(2, dim=1) - 1) ** 2).mean()
    return gradient_penalty

def train_gan_step(generator, critic, frozen_cgnn, real_compositions, target_properties, cost_budget, element_prices, optim_g, optim_c, device):
    """
    Single training step for the GAN.
    """
    # 1. Train Critic
    optim_c.zero_grad()
    
    noise = torch.randn(real_compositions.size(0), 100).to(device)
    fake_compositions = generator(noise, target_properties, cost_budget)
    
    real_validity = critic(real_compositions)
    fake_validity = critic(fake_compositions.detach())
    
    gp = compute_gradient_penalty(critic, real_compositions, fake_compositions.detach(), device)
    
    loss_c = -torch.mean(real_validity) + torch.mean(fake_validity) + 10 * gp
    loss_c.backward()
    optim_c.step()
    
    # 2. Train Generator
    optim_g.zero_grad()
    
    fake_compositions = generator(noise, target_properties, cost_budget)
    fake_validity = critic(fake_compositions)
    
    # Property Matching Loss (via frozen CGNN)
    # Predicted properties of generated alloy
    predicted_properties = frozen_cgnn(fake_compositions) # simplified
    loss_property = nn.MSELoss()(predicted_properties, target_properties)
    
    # Cost Penalty
    current_cost = torch.sum(fake_compositions * element_prices, dim=1)
    cost_penalty = torch.mean(torch.clamp(current_cost - cost_budget.squeeze(), min=0)**2)
    
    loss_g = -torch.mean(fake_validity) + 100 * loss_property + 10 * cost_penalty
    loss_g.backward()
    optim_g.step()
    
    return loss_g.item(), loss_c.item()

if __name__ == "__main__":
    pass
