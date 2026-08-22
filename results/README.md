# Results

This directory contains **derived artifacts** from the H₂O₂ VQE study.

## Authoritative result sources

There are two distinct result layers and they should not be mixed:

1. **Executed notebook snapshot:** `results/notebook_run_snapshot.json`
   - This is an archival snapshot of the numerical values extracted from the executed research notebook that produced the figures currently shown in the repository.
   - It preserves the author's actual completed run.

2. **Regenerated study outputs:** `run_study.py`
   - These are generated from the canonical modular pipeline and the pinned environment.
   - They are the authoritative outputs for a fresh reproducibility run.

This separation prevents a copied notebook result from being mistaken for a newly regenerated calculation.

## Generated outputs

```text
results/
├── notebook_run_snapshot.json
├── tables/
│   ├── classical_reference_energies.csv
│   ├── classical_reference_energies.json
│   ├── hamiltonian_validation.csv
│   ├── mapping_comparison.csv
│   ├── equilibrium_vqe_benchmark.csv
│   ├── uccsd_resource_estimates.csv
│   ├── vqe_pes_benchmark.csv
│   └── vqe_convergence.csv
├── figures/
│   ├── h2o2_dissociation_pes.png
│   ├── vqe_error_vs_bond_distance.png
│   ├── active_space_error_vs_bond_distance.png
│   ├── vqe_convergence.png
│   └── mapping_and_resources.png
└── study_summary.json
```

## What the tables answer

- **Classical references:** RHF, CAS(2,2), and full-space FCI energies across the O–O scan.
- **Hamiltonian validation:** verifies that the mapped qubit Hamiltonian reproduces the CAS(2,2) reference by exact diagonalization.
- **Mapping comparison:** compares Jordan–Wigner, Bravyi–Kitaev, standard parity, and 2-qubit reduced parity.
- **Equilibrium VQE:** compares 4-qubit JW UCCSD, 2-qubit reduced-parity UCCSD, and a 2-qubit EfficientSU2 ansatz.
- **PES benchmark:** evaluates the canonical 2-qubit reduced-parity UCCSD VQE at every O–O distance and reports its error relative to CAS(2,2).
- **Convergence:** records COBYLA energy trajectories at 1.45 Å and 3.00 Å for the same 2-qubit reduced-parity UCCSD workflow used for the PES.
- **Resource estimates:** records qubit count, Pauli-term count, gate count, CNOT count, and circuit depth.

## Key archived findings

The executed notebook snapshot records:

- CAS(2,2) equilibrium energy at R = 1.45 Å: **−148.75976360 Ha**.
- 2-qubit parity-reduced UCCSD VQE at equilibrium: **−148.75976360 Ha**, with reported statevector error of **0.0000 mHa**.
- Across the seven-point PES, the largest archived UCCSD–CAS error is approximately **0.0097 mHa**, well below the 1.6 mHa chemical-accuracy threshold.
- At equilibrium, the reduced representation uses **2 qubits, 9 Pauli terms, 17 total gates, 4 CNOT gates, and depth 12**, compared with 4 qubits, 27 Pauli terms, 150 total gates, 56 CNOT gates, and depth 83 for the JW representation.
- The CAS(2,2)–full-space FCI gap reaches approximately **106.94 mHa** near R = 1.45 Å. This is an active-space/model-space discrepancy, not a VQE optimization error.

## Important methodological note

The finite-shot section in the original notebook is a **Gaussian shot-noise post-processing model** applied to an exact statevector VQE result. It is not a true sampled-Pauli finite-shot VQE. The archived snapshot preserves those values for provenance, but they should not be presented as hardware or sampled-measurement results.

The original notebook also contains a stale printed shot-noise target energy that differs from the actual target variable used to calculate the reported errors. This is recorded in `notebook_run_snapshot.json` and should be corrected in the notebook before publication.

## Reproducibility

From the repository root:

```bash
python -m pytest -q
python run_study.py
```

The script creates the `geometries/` directory and all fresh files under `results/tables/`, `results/figures/`, and `results/study_summary.json`.
