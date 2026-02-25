# sidsmp/core/metrics.py
import numpy as np


def compute_energetics(I_raw, I_sub, coupling, C_dynamic, T_load, params):
    """
    THERMODYNAMIC METRICS (Eq. 7, Paper v2)
    P(t) = Useful Work / Dissipated Energy

    Notes:
    - This is a toy implementation meant for regime illustration and reproducible figures.
    - Inputs are sanitized to avoid negative-energy artifacts from numerical solvers.
    """
    # --- Numerical safety guards (avoid negative energy artifacts) ---
    I_raw = max(float(I_raw), 0.0)
    I_sub = max(float(I_sub), 0.0)
    coupling = float(coupling)
    C_dynamic = float(C_dynamic)

    lam = params.lambda_func(T_load)

    # --- 1. Structural Work (W_struct) ---
    # Energy successfully converted into structure.
    # We bound the effective conversion fraction to [0, 1] to avoid unphysical negative dissipation
    # when coupling * alpha * C_dynamic exceeds 1 due to parameter choices.
    conv_frac = float(np.clip(coupling * params.alpha * C_dynamic, 0.0, 1.0))
    W_struct = conv_frac * lam * I_raw

    # --- 2. Dissipated Energy (E_diss) ---
    # Cost A: Transformation inefficiency (what does not become structure)
    cost_transform = (1.0 - conv_frac) * lam * I_raw

    # Cost B: Structural maintenance (fighting entropy)
    cost_maintenance = params.mu * I_sub

    E_diss = cost_transform + cost_maintenance

    # --- 3. Predictive Capacity P(t) ---
    # Thermodynamic efficiency of the system.
    P_t = float(W_struct / (E_diss + params.epsilon))

    return W_struct, E_diss, P_t