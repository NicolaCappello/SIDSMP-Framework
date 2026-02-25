import os
import sys

# Ensure the repository root is on sys.path (works when running from any CWD)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Save all outputs inside the validation folder (portable + keeps repo tidy)
OUT_DIR = os.path.abspath(os.path.dirname(__file__))

from experiments.regime_variation import run_regime_experiment
from experiments.sensitivity_analysis import run_k_sensitivity
from visualization.timeseries import plot_regime_timeseries
from visualization.phase_planes import plot_phase_space
from visualization.collapse_dynamics import plot_collapse_diagrams
import matplotlib.pyplot as plt


def main():
    print("=== SIDSMP VALIDATION SUITE ===")

    # 1. Run regime variation experiment
    print("\n[1] Running regime variation experiment...")
    loads = [0.0, 1.0, 2.0, 3.0, 5.0]
    results = run_regime_experiment(loads)

    # 2. Generate standard validation plots
    print("\n[2] Generating standard plots...")
    plot_regime_timeseries(results, loads, os.path.join(OUT_DIR, "validation_timeseries.png"))
    plot_collapse_diagrams(results, loads, os.path.join(OUT_DIR, "validation_collapse.png"))

    # 3. Generate phase-space analysis (requested by reviewers)
    print("\n[3] Generating phase-space analysis...")
    plot_phase_space(results, loads, os.path.join(OUT_DIR, "validation_phase_space.png"))

    # 4. Sensitivity analysis (requested by reviewers)
    print("\n[4] Running sensitivity analysis (parameter k)...")
    sens_data = run_k_sensitivity()

    # Plot sensitivity results
    plt.figure(figsize=(10, 6))
    for k, (T_rng, Peaks) in sens_data.items():
        plt.plot(T_rng, Peaks, '-o', label=f'k={k}')
    plt.title("Sensitivity Analysis: System Fragility (k)")
    plt.xlabel("Load T")
    plt.ylabel("Maximum Predictive Efficiency P")
    plt.legend()
    plt.grid(True, alpha=0.3)
    sens_path = os.path.join(OUT_DIR, "validation_sensitivity.png")
    plt.savefig(sens_path)
    print(f"Saved: {sens_path}")

    print("\n=== VALIDATION COMPLETE ===")
    print(f"All output files generated in: {OUT_DIR}")


if __name__ == "__main__":
    main()