import os
import sys

# Ensure the repository root is on sys.path (works when running from any CWD)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import numpy as np
from sidsmp.core.parameters import SystemParameters
from sidsmp.simulation.engine import run_single_simulation


def run_k_sensitivity():
    """
    Tests how the peak Predictive Efficiency P(t)
    varies as a function of system fragility k.
    """
    # Fragility parameter k controls how rapidly transformability λ(T)
    # collapses under increasing informational load.
    #
    # Lower k  -> more robust system (slow degradation of λ)
    # Higher k -> more fragile system (rapid degradation of λ)
    #
    # The selected values sample qualitatively distinct regimes
    # without imposing arbitrary thresholds or discontinuities.
    k_values = [0.5, 1.0, 1.2, 2.0]  # from robust to fragile
    T_range = np.linspace(0, 5, 20)

    # Informational load range.
    # Chosen to span normal operation, the threshold region,
    # and the high-load predictive degradation regime,
    # while preserving continuity in the system's response.
    sensitivity_data = {}

    print("--- Experiment: Sensitivity Analysis (Parameter k) ---")

    for k in k_values:
        params = SystemParameters()
        params.k = k  # Override fragility parameter

        peak_Ps = []
        for T in T_range:
            res = run_single_simulation(T, params)
            peak_Ps.append(np.max(res['P_t']))

        sensitivity_data[k] = (T_range, peak_Ps)
        print(f"  > k={k} analyzed.")

    return sensitivity_data