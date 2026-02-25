# sidsmp/simulation/plotting.py
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np


def plot_comprehensive_analysis(results, load_levels):
    """Generate the final figure for the paper (including the decoupling regime)."""

    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(2, 3, figure=fig)

    # --- A. Temporal Dynamics ---
    ax1 = fig.add_subplot(gs[0, 0])
    low = results[load_levels[0]]  # Functional regime
    high = results[load_levels[-1]]  # Decoupling regime

    ax1.plot(low['t'], low['I_sub'], 'b-', label='Structure (Functional regime)')
    ax1.plot(high['t'], high['I_sub'], 'r--', label='Structure (Decoupling regime)')
    ax1.set_title("A. Structure Formation")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # --- B. Coupling (NEW – Highlights the decoupling regime) ---
    ax2 = fig.add_subplot(gs[0, 1])
    for T in load_levels:
        if T > 2.0:  # Highlight only critical load conditions
            ax2.plot(results[T]['t'], results[T]['coupling'], label=f'Load T={T}')
    ax2.set_title("B. Decoupling from environmental constraint")
    ax2.set_ylabel("Coupling factor (0 = decoupled, 1 = coupled)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # --- C. Thermodynamic Efficiency ---
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(low['t'], low['W_struct'], 'g-', label='Useful work')
    ax3.plot(low['t'], low['E_diss'], 'r-', label='Dissipation')
    ax3.set_title("C. Energetic balance (Functional regime)")
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # --- D. Phase Diagram (P_t) ---
    ax4 = fig.add_subplot(gs[1, :])
    peak_P = [np.max(results[T]['P_t']) for T in load_levels]
    ax4.plot(load_levels, peak_P, 'b-o')

    # Regime zones
    ax4.axvspan(0, 1.5, color='green', alpha=0.1, label='Functional')
    ax4.axvspan(1.5, 2.5, color='orange', alpha=0.1, label='Saturation')
    ax4.axvspan(2.5, 5.0, color='red', alpha=0.1, label='Decoupling regime')

    ax4.set_title("D. Phase transition: from functional to decoupling regime")
    ax4.set_xlabel("Load T")
    ax4.set_ylabel("Maximum predictive capacity")
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('SIDSMP_Final_Result.png', dpi=300)
    print("Figure saved: SIDSMP_Final_Result.png")