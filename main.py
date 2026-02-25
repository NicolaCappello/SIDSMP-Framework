import numpy as np

from sidsmp.core.parameters import SystemParameters
from sidsmp.simulation.engine import run_single_simulation
from sidsmp.simulation.plotting import plot_comprehensive_analysis


def main():
    print("=== SIDSMP Toy Model – Exploratory Driver ===")
    print("Regime Test: Functional → Saturation → Coupling Decoupling")
    print("(For full reproducible figures, run: validation/run_validation_suite.py)")

    # 1. Parameter initialization
    params = SystemParameters()

    # 2. Load definition
    # Include high load values (3.0, 5.0) to force the coupling decoupling regime
    load_levels = [0.0, 1.0, 2.0, 3.0, 5.0]
    results = {}

    # 3. Simulation execution
    for T in load_levels:
        print(f"Running simulation at load T={T:.1f}...", end="")
        results[T] = run_single_simulation(T, params)

        # Quick diagnostic feedback in the terminal
        max_P = np.max(results[T]['P_t'])
        final_coupling = results[T]['coupling'][-1]
        print(f" Done. Max P(t): {max_P:.3f} | Final coupling: {final_coupling:.3f}")

    print("\nGenerating diagnostic plots...")

    # 4. Plot generation
    plot_comprehensive_analysis(results, load_levels)
    print("Validation process completed.")


if __name__ == "__main__":
    main()