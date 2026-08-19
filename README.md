# Quantum Simulation of H₂O₂ O–O Bond Dissociation with VQE

A quantum-computational chemistry study of the homolytic O–O bond dissociation of hydrogen peroxide (H₂O₂ → 2 ·OH) using the Variational Quantum Eigensolver (VQE).

## Overview

This project follows the complete workflow from molecular geometry generation and classical electronic-structure reference calculations to second quantization, fermion-to-qubit mapping, symmetry reduction, VQE, potential-energy-surface benchmarking, shot-noise analysis, and quantum-resource estimation.

The accompanying research notebook uses a **CAS(2,2)** active space to capture the static correlation associated with O–O dissociation and investigates both standard Jordan–Wigner and symmetry-reduced parity representations.

## Main objectives

- Construct a controlled H₂O₂ O–O dissociation coordinate.
- Generate classical RHF and FCI reference energies.
- Build the second-quantized electronic Hamiltonian with Qiskit Nature.
- Map the fermionic Hamiltonian to qubits.
- Reduce the active-space problem using Z₂/parity symmetry.
- Benchmark VQE ansätze, including UCCSD and hardware-efficient circuits.
- Compare VQE energies against classical reference calculations.
- Investigate finite-shot noise and optimizer resilience.
- Estimate the quantum resources required for the calculation.

## Computational stack

- Python
- Qiskit
- Qiskit Nature
- Qiskit Aer
- Qiskit Algorithms
- PySCF
- NumPy
- SciPy
- pandas
- Matplotlib
- Jupyter / Google Colab

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── LICENSE
├── notebooks/
│   └── H2O2_VQE_Bond_Dissociation.ipynb
├── geometries/
│   └── xyz/
├── results/
└── src/
```

## Reproducibility

Create a clean Python environment and install the dependencies listed in `requirements.txt`. Then open the notebook and execute the workflow from top to bottom.

The notebook was developed around the Qiskit 1.x-compatible Qiskit Nature workflow and records its environment validation and computational assumptions explicitly.

## Scientific scope

This is a **benchmark and methodological study**, not a claim that present-day quantum hardware can outperform established classical electronic-structure methods for H₂O₂. The purpose is to examine how a small quantum chemistry problem behaves under active-space reduction, different qubit mappings, VQE optimization, and realistic sampling noise.

## Key benchmark reported in the notebook

The notebook's executive summary reports a reduction from 4 qubits under the standard Jordan–Wigner representation to 2 qubits using parity symmetry, alongside a substantial reduction in UCCSD CNOT depth.

All numerical claims should be interpreted in the context of the exact basis, active space, geometry, simulator/backend, optimizer, and convergence settings used in the notebook.

## Author

**Abdullah Hayder**  
Biomedical Sciences · Bioinformatics · Quantum Computing for Biology

## Status

Research/portfolio project — actively extensible.
