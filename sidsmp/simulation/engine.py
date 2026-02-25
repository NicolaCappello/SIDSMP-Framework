# sidsmp/simulation/engine.py
import numpy as np
from scipy.integrate import odeint
from sidsmp.core.dynamics import system_derivatives
from sidsmp.core.metrics import compute_energetics


def run_single_simulation(T_load, params, t_max=50, steps=500):
    t = np.linspace(0, t_max, steps)

    # Initial conditions: [I_raw=1.0, I_sub=0.0, Coupling=1.0]
    # Start fully coupled to the environment.
    y0 = [1.0, 0.0, 1.0]

    # ODE integration
    solution = odeint(system_derivatives, y0, t, args=(T_load, params))

    I_raw = solution[:, 0]
    I_sub = solution[:, 1]
    coupling = solution[:, 2]

    # --- Post-processing metrics ---
    # Recompute derived variables step-by-step (time-local)
    lam = params.lambda_func(T_load)
    dI_raw_dt = -lam * I_raw  # Analytical derivative of I_raw

    W_arr, E_arr, P_arr, C_arr = [], [], [], []

    for i in range(len(t)):
        # Recompute dynamic coherence C(t) at time index i
        instab = (dI_raw_dt[i]) ** 2
        C_dyn = params.C_base / (1 + params.beta * instab)
        C_arr.append(C_dyn)

        # Energetics
        W, E, P = compute_energetics(I_raw[i], I_sub[i], coupling[i], C_dyn, T_load, params)
        W_arr.append(W)
        E_arr.append(E)
        P_arr.append(P)

    return {
        't': t,
        'I_raw': I_raw,
        'I_sub': I_sub,
        'coupling': coupling,
        'C_dynamic': np.array(C_arr),
        'W_struct': np.array(W_arr),
        'E_diss': np.array(E_arr),
        'P_t': np.array(P_arr),
        'lambda_val': lam
    }