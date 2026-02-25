from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class SystemParameters:
    """System parameters for the SIDSMP toy model.

    This module intentionally stays *substrate-independent*: the parameters are
    interpreted as *functional proxies* (computational/organizational constraints)
    rather than direct biological or thermodynamic quantities.

    Naming convention
    -----------------
    - ``lambda_0``: maximal transformability at rest (T_load = 0)
    - ``k``: susceptibility / fragility coefficient (how fast transformability collapses under load)
    - ``alpha``: conversion efficiency from raw information to structured information
    - ``mu``: structural damping / maintenance cost (forgetting / decay of structure)
    - ``C_base``: nominal upper bound for coherence
    - ``beta``: how strongly coherence is penalized by input instability
    - ``decouple_threshold``: load-domain bifurcation point beyond which the system dynamically detaches from input constraints
    - ``zeta``: decoupling speed (inertia of detachment)
    - ``epsilon``: small numerical stabilizer to avoid division by zero

    Note
    ----
    These parameters are aligned with the SIDSMP v2.x paper narrative and the
    corresponding review notes (dynamic C and decoupling regime).
    """

    # --- Fundamental parameters ---
    lambda_0: float = 1.0
    k: float = 1.2

    # --- Base efficiency ---
    alpha: float = 0.6
    mu: float = 0.15

    # --- Coherence dynamics ---
    C_base: float = 0.95
    beta: float = 2.0

    # Load-domain bifurcation parameter (conceptual, not physical)
    # --- Decoupling mechanism ---
    decouple_threshold: float = 2.5
    zeta: float = 0.1

    # --- Numerical constant ---
    epsilon: float = 1e-6

    def validate(self) -> None:
        """Validate parameter ranges.

        We keep this minimal on purpose: it prevents silent numerical pathologies
        (negative rates, invalid probabilities) without over-constraining the toy model.
        """
        if self.lambda_0 <= 0:
            raise ValueError("lambda_0 must be > 0")
        if self.k < 0:
            raise ValueError("k must be >= 0")
        if not (0 <= self.alpha <= 1.0):
            raise ValueError("alpha must be in [0, 1]")
        if self.mu < 0:
            raise ValueError("mu must be >= 0")
        if not (0 < self.C_base <= 1.0):
            raise ValueError("C_base must be in (0, 1]")
        if self.beta < 0:
            raise ValueError("beta must be >= 0")
        if self.decouple_threshold < 0:
            raise ValueError("decouple_threshold must be >= 0")
        if self.decouple_threshold == 0 and self.k > 0:
            raise ValueError(
                "decouple_threshold = 0 with k > 0 causes immediate decoupling; "
                "this is allowed mathematically but defeats the intended regime structure."
            )
        if self.zeta < 0:
            raise ValueError("zeta must be >= 0")
        if self.epsilon <= 0:
            raise ValueError("epsilon must be > 0")

    def lambda_func(self, T_load: float | np.ndarray) -> float | np.ndarray:
        """Transformability under load.

        Functional form used in the paper/toy model:
            lambda(T) = lambda_0 * exp(-k * T)

        Parameters
        ----------
        T_load:
            Abstract load index (not physical temperature). Can be scalar or NumPy array.
        """
        return self.lambda_0 * np.exp(-self.k * T_load)