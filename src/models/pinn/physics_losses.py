import torch

def elastic_moduli_consistency_loss(k_pred, g_pred, v_pred):
    """
    Ensures Bulk Modulus (K), Shear Modulus (G), and Poisson's Ratio (v) are consistent.
    Relationship: E = 2G(1+v) = 3K(1-2v) => 2G(1+v) - 3K(1-2v) = 0
    """
    # Using the relationship: 2G(1+v) = 3K(1-2v)
    term1 = 2 * g_pred * (1 + v_pred)
    term2 = 3 * k_pred * (1 - 2 * v_pred)
    
    loss = torch.mean((term1 - term2)**2)
    return loss

def thermodynamic_consistency_loss(g_pred, h_pred, t, s_pred):
    """
    Gibbs Free Energy consistency: G = H - TS
    """
    loss = torch.mean((g_pred - (h_pred - t * s_pred))**2)
    return loss

def poisson_ratio_bounds_loss(v_pred):
    """
    Penalty for Poisson's ratio outside physical bounds (-1, 0.5).
    """
    lower_bound_penalty = torch.clamp(-1 - v_pred, min=0)**2
    upper_bound_penalty = torch.clamp(v_pred - 0.5, min=0)**2
    return torch.mean(lower_bound_penalty + upper_bound_penalty)

def compute_pinn_loss(predictions, targets=None, lambda_physics=0.1):
    """
    Combine data loss with physics constraints.
    predictions: [formation, bandgap, bulk(K), shear(G), poisson(v)]
    """
    # Assuming the output has these indices
    k_pred = predictions[:, 2]
    g_pred = predictions[:, 3]
    # If the model predicts poisson ratio too
    if predictions.shape[1] > 4:
        v_pred = predictions[:, 4]
    else:
        # Approximation or constant if not predicted
        v_pred = torch.tensor(0.3, device=predictions.device)
        
    l_elastic = elastic_moduli_consistency_loss(k_pred, g_pred, v_pred)
    l_bounds = poisson_ratio_bounds_loss(v_pred)
    
    return lambda_physics * (l_elastic + l_bounds)
