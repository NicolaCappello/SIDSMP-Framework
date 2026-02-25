import matplotlib.pyplot as plt


def plot_regime_timeseries(results, load_levels, filename="timeseries.png"):
    """
    Plot representative time series across contrasting informational load regimes.

    This figure compares the system dynamics under low and high informational load,
    illustrating how structured information accumulation and energetic balance
    change as a function of load. Regimes are not imposed categorically, but emerge
    continuously from the underlying dynamics.
    """

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Low-load regime (first level) vs high-load regime (last level)
    ordered_loads = sorted(load_levels)
    if not ordered_loads:
        raise ValueError("load_levels is empty.")

    low = results.get(ordered_loads[0])
    high = results.get(ordered_loads[-1])

    if low is None or high is None:
        raise KeyError("Missing results for selected load levels.")

    # Structured information dynamics
    ax1.plot(low['t'], low['I_sub'], 'b-', label='Structured information (low load)')
    ax1.plot(high['t'], high['I_sub'], 'r--', label='Structured information (high load)')
    ax1.set_title("Structured Information Dynamics Across Load Levels")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Energetic balance (low-load regime only, for clarity)
    ax2.plot(low['t'], low['W_struct'], 'g-', label='Structural work $W_{struct}$')
    ax2.plot(low['t'], low['E_diss'], 'k-', alpha=0.5, label='Dissipated energy $E_{diss}$')
    ax2.fill_between(low['t'], low['W_struct'], low['E_diss'],
                     where=(low['W_struct'] > low['E_diss']),
                     color='green', alpha=0.1)
    ax2.set_title("Energetic Balance (Low Load)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    from pathlib import Path
    out_path = Path(filename)
    if out_path.parent and str(out_path.parent) not in (".", ""):
        out_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(out_path)
    plt.close()
    print(f"Saved: {out_path.resolve()}")