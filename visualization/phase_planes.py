from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt


def plot_phase_space(results, load_levels, filename: str | Path = Path("phase_space.png")) -> Path:
    """
    Plot trajectories in the state space (I_raw vs I_sub).

    This visualization shows how increasing informational load (T_load)
    induces qualitative changes in the system's dynamical trajectories,
    without assuming predefined categories or pathological labels.

    Different colors represent increasing load regimes as a continuous
    control parameter, highlighting the emergence of distinct behaviors
    from the same underlying equations.

    Parameters
    ----------
    results : dict
        Mapping load -> dict with keys 'I_raw' and 'I_sub' (array-like).
    load_levels : iterable
        Loads to plot (must match keys in `results`).
    filename : str | Path
        Output file path. If a relative path is provided, it is resolved
        relative to the current working directory (PyCharm "Working directory").

    Returns
    -------
    Path
        Absolute path of the saved figure.
    """
    out_path = Path(filename)
    # Ensure parent directory exists (if any)
    if out_path.parent and str(out_path.parent) not in (".", ""):
        out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 8))

    ordered_loads = sorted(load_levels)
    for T in ordered_loads:
        res = results.get(T)
        if not res:
            continue
        if "I_raw" not in res or "I_sub" not in res:
            continue
        if len(res["I_raw"]) == 0 or len(res["I_sub"]) == 0:
            continue

        # Color coding reflects increasing informational load (continuous control parameter)
        if T < 1.5:
            color = "green"
        elif T < 2.5:
            color = "orange"
        else:
            color = "red"

        ax.plot(res["I_raw"], res["I_sub"], color=color, alpha=0.6, label=f"T={T}")
        # Mark the final point
        ax.plot(res["I_raw"][-1], res["I_sub"][-1], "o", color=color)

    ax.set_title("State Space Trajectories (I_raw vs I_sub)")
    ax.set_xlabel("Raw Information (I_raw)")
    ax.set_ylabel("Structured Information (I_sub)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    abs_path = out_path.resolve()
    print(f"Saved phase space figure to: {abs_path}")
    return abs_path