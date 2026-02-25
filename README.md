# SIDSMP: State-Dependent Informational Substitution

**A Dynamical Framework for Memory, Prediction, and Subjective Emergence**

[![Status](https://img.shields.io/badge/Status-Working_Paper-blue)](https://zenodo.org/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18770278.svg)](https://doi.org/10.5281/zenodo.18770278)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Overview
This repository contains the **Computational Toy Model** associated with the paper:
> *State-Dependent Informational Substitution in Memory and Prediction (SIDSMP)*
> **Author:** Nicola Cappello (2026)

The framework models subjectivity not as an agent, but as an emergent dynamical attractor under resource constraints, minimizing computational cost by converting high-entropy raw data ($I_{raw}$) into stable structural representations ($I_{sub}$).

## Key Features
- **Thermodynamic Grounding:** Predictive capacity $P(t)$ is defined as the efficiency ratio between Structural Work ($W$) and Dissipated Energy ($E$).
- **Emergent Regimes:** distinct dynamical regimes (stabilization, overload, predictive collapse, and decoupling) emerge naturally as transformability $\lambda(T)$ collapses under load.
- **Decoupling Mechanism:** Simulates how the system decouples from environmental input constraints (Coupling $\to$ 0) to preserve internal coherence under unsustainable load.

## Repository Structure
- `sidsmp/`: Core library implementing the SIDSMP dynamics (Eq. 1–7).
- `experiments/`: Scripts for regime variation and sensitivity analysis.
- `visualization/`: Plotting tools (phase planes, time series, collapse diagrams).
- `validation/`: Validation suite that reproduces the figures (PNG) used in the paper.

**Default model parameters** are defined in `sidsmp/core/parameters.py` and can be modified to explore alternative dynamical regimes.

## Quick Start

Create and activate a virtual environment (recommended), then install dependencies and run the validation suite.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run the full validation suite (generates PNG figures)
python validation/run_validation_suite.py
```

**Outputs**: figures are saved to `validation/` as `validation_*.png`.

## Reproducibility

The primary entry point for reproducing the paper figures is:

```bash
python validation/run_validation_suite.py
```

This script runs:
- regime variation (load T)
- phase-space analysis
- sensitivity analysis (parameter k)

and saves the resulting plots in `validation/`.

## Zenodo

The archived release of this software is permanently available at:

https://doi.org/10.5281/zenodo.18770278

When citing this implementation, please reference the version-specific DOI above.