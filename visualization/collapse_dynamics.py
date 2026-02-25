import os
import matplotlib.pyplot as plt
import numpy as np


def plot_collapse_diagrams(
    results,
    load_levels,
    filename="collapse.png",
    focus_threshold=2.0,
    decoupling_span=(2.5, 5.0),
):
    """Visualize coupling dynamics and the emergence of predictive efficiency regimes."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 1. Coupling dynamics under increasing load (emergent decoupling)
    for T in load_levels:
        if T > focus_threshold:  # Focus on high-load conditions where decoupling emerges
            ax1.plot(results[T]['t'], results[T]['coupling'], label=f'T={T}')
    ax1.set_title("Coupling dynamics under high informational load")
    ax1.set_ylabel("Coupling (normalized functional coupling, 0–1)")
    ax1.set_xlabel("t (computational steps)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Emergence of predictive efficiency regimes
    ordered_loads = sorted(load_levels)
    peak_P = []
    valid_loads = []
    for T in ordered_loads:
        series = results.get(T, {}).get('P_t', None)
        if series is None:
            continue
        series = np.asarray(series)
        if series.size == 0:
            continue
        valid_loads.append(T)
        peak_P.append(float(np.max(series)))

    ax2.plot(valid_loads, peak_P, 'b-o')
    ax2.axvspan(decoupling_span[0], decoupling_span[1], color='red', alpha=0.1, label='High-load decoupling regime')
    ax2.set_title("Emergent regimes of predictive efficiency")
    ax2.set_xlabel("Informational load T")
    ax2.set_ylabel("Peak predictive efficiency P")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Ensure output directory exists (if a path is provided)
    out_dir = os.path.dirname(os.path.abspath(filename))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    fig.tight_layout()
    fig.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Figure saved: {os.path.abspath(filename)}")