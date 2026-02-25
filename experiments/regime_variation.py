import os
import sys

# Ensure the repository root is on sys.path (works when running from any CWD)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import numpy as np
from sidsmp.core.parameters import SystemParameters
from sidsmp.simulation.engine import run_single_simulation


def run_regime_experiment(load_levels=None):
    """
    Runs a systematic set of simulations across multiple values of the informational load parameter T.

    This experiment is designed to probe the emergence of distinct dynamical regimes
    (baseline, transition, and high-load decoupling) as described in the SIDSMP v2.x framework.

    Returns
    -------
    dict
        Mapping T_load -> simulation output dictionary.
    """
    if load_levels is None:
        # Informational load values selected to sample:
        # - baseline regime (low load)
        # - transition / threshold region
        # - high-load decoupling regime with predictive degradation
        #
        # T = 0.0  -> baseline regime (no informational load)
        # T ≈ 1.0  -> transition region near the transformation threshold
        # T ≥ 2.0  -> high-load regime with progressive predictive degradation
        load_levels = [0.0, 1.0, 2.0, 3.0, 5.0]

    params = SystemParameters()
    results = {}

    print(f"--- Experiment: Regime Variation (Loads: {load_levels}) ---")
    for T in load_levels:
        res = run_single_simulation(T, params)
        results[T] = res
        print(f"  > Load T={T:.1f} computed.")

    return results


if __name__ == "__main__":
    run_regime_experiment()