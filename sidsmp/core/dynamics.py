# sidsmp/core/dynamics.py
import numpy as np


def system_derivatives(y, t, T_load, params):
    """Compute the ODE right-hand side for the SIDSMP toy model (v2.1).

    Includes:
    - dynamic coherence C(t)
    - variable coupling (0.0–1.0) as a load-driven detachment / reattachment mechanism

    State vector y:
        y[0] = I_raw      (raw information)
        y[1] = I_sub      (structured information)
        y[2] = coupling   (degree of connection to input / environment)

    Args:
        y: current state [I_raw, I_sub, coupling]
        t: time (kept for ODE solver signature compatibility)
        T_load: exogenous load / pressure parameter
        params: Parameters object (must expose lambda_func, alpha, C_base, beta, mu, zeta, decouple_threshold)

    Returns:
        [dI_raw_dt, dI_sub_dt, d_coupling_dt]
    """
    I_raw, I_sub, coupling = y

    # Numerical safety: keep coupling within [0, 1] for downstream computations
    coupling = float(np.clip(coupling, 0.0, 1.0))

    # 1) Base transformability (depends on load T_load)
    lam = params.lambda_func(T_load)

    # 2) I_raw dynamics (decay / overwrite of raw information)
    dI_raw_dt = -lam * I_raw

    # 3) Dynamic coherence C(t) (emergent)
    # If I_raw changes too quickly (instability proxy), internal coherence decreases.
    instability = (dI_raw_dt) ** 2
    C_dynamic = params.C_base / (1 + params.beta * instability)

    # 4) Coupling dynamics (load-driven detachment mechanism)
    # If T_load exceeds a threshold, the system tends to detach (target=0).
    target_coupling = 0.0 if T_load > params.decouple_threshold else 1.0
    d_coupling_dt = params.zeta * (target_coupling - coupling)

    # 5) I_sub dynamics (structure formation)
    # Input enters only if there is coupling (coupling * ...).
    # If coupling≈0, structure formation becomes effectively isolated from new input.
    input_flow = coupling * params.alpha * C_dynamic * lam * I_raw
    decay_flow = params.mu * I_sub

    dI_sub_dt = input_flow - decay_flow

    return [dI_raw_dt, dI_sub_dt, d_coupling_dt]
# sidsmp/core/metrics.py
import numpy as np


def compute_energetics(I_raw, I_sub, coupling, C_dynamic, T_load, params):
    """
    THERMODYNAMIC METRICS (Eq. 7, Paper v2)

    P(t) = Useful Work / Dissipated Energy

    Notes:
    - This is an operational / proxy energetics model (not a direct calorimetric measurement).
    - `coupling` modulates whether transformed information can be expressed as effective work;
      in the decoupled regime (coupling≈0), useful work tends to zero.
    """
    lam = params.lambda_func(T_load)

    coupling = float(np.clip(coupling, 0.0, 1.0))

    # --- 1. Structural work (W_struct) ---
    # Effective conversion fraction (must remain in [0, 1])
    conv_frac = float(np.clip(coupling * params.alpha * C_dynamic, 0.0, 1.0))

    W_struct = conv_frac * lam * I_raw

    # --- 2. Dissipated energy (E_diss) ---
    # Cost A: transformation inefficiency (what does NOT become structure)
    inefficiency = 1.0 - conv_frac
    cost_transform = inefficiency * lam * I_raw

    # Cost B: structural maintenance (counteracting entropy / decay)
    cost_maintenance = params.mu * I_sub

    E_diss = cost_transform + cost_maintenance

    # --- 3. Predictive capacity P(t) ---
    # Operational thermodynamic efficiency of the system.
    P_t = W_struct / (E_diss + params.epsilon)

    return W_struct, E_diss, P_t