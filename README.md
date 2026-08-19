# Quantum Simulation of H₂O₂ O–O Bond Dissociation with VQE

A reproducible quantum-computational chemistry benchmark of homolytic H₂O₂ O–O bond dissociation using a CAS(2,2) active space and the Variational Quantum Eigensolver (VQE).

## Research question

How do active-space reduction, fermion-to-qubit mapping, variational ansatz choice, finite sampling, and circuit resources affect a small quantum-chemistry calculation along the H₂O₂ O–O dissociation coordinate?

## Computational workflow

```text
H₂O₂ geometry grid
        ↓
RHF / CAS(2,2) / full-space FCI references
        ↓
Qiskit Nature active-space Hamiltonian
        ↓
JW / BK / parity mappings
        ↓
2-qubit parity reduction
        ↓
VQE: UCCSD and EfficientSU2
        ↓
PES benchmark + convergence analysis
        ↓
shot-noise model + circuit resources
```

## Methods

- Molecule: H₂O₂
- Basis: STO-3G
- Charge: 0
- Spin: 0 (closed-shell singlet in the source workflow)
- Active space: CAS(2 electrons, 2 spatial orbitals)
- O–O scan: 1.00, 1.20, 1.45, 1.80, 2.20, 2.60, 3.00 Å
- Classical references: RHF, CAS(2,2), full-space FCI
- Qubit mappings: Jordan–Wigner, Bravyi–Kitaev, standard parity, 2-qubit reduced parity
- VQE ansätze: UCCSD and EfficientSU2
- Primary optimizer: COBYLA
- Chemical-accuracy threshold used by the notebook: 1.6 mHa

The geometry and methodological parameters are taken directly from the supplied research notebook. fileciteturn12file0L335-L443

## Repository structure

```text
.
├── README.md
├── CITATION.cff
├── LICENSE
├── requirements.txt
├── environment.yml
├── config/
│   └── study.yaml
├── notebooks/
│   └── H2O2_VQE_Bond_Dissociation.ipynb
├── src/
│   ├── geometry.py
│   ├── classical_reference.py
│   ├── hamiltonian.py
│   ├── mapping.py
│   ├── vqe.py
│   ├── noise_analysis.py
│   ├── resource_estimation.py
│   └── analysis.py
├── tests/
├── data/
├── results/
├── docs/
│   └── REPRODUCIBILITY.md
└── .github/workflows/
    └── tests.yml
```

## Reproducibility

The canonical environment is pinned to the versions recorded during the notebook run: Python 3.12.13, PySCF 2.14.0, Qiskit 2.5.2, Qiskit Nature 0.8.0, Qiskit Aer 0.17.2, NumPy 2.0.2, SciPy 1.16.3, pandas 2.2.2, and Matplotlib 3.10.0. fileciteturn12file0L264-L329

Create the environment with:

```bash
conda env create -f environment.yml
conda activate h2o2-vqe
```

Then run the smoke tests:

```bash
python -m pytest -q
```

The full execution protocol is documented in [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).

## Important methodological note

The notebook describes its stack as “Qiskit 1.x”, but its recorded installation and validation output show Qiskit 2.5.2. The repository preserves the **recorded computational environment** rather than silently rewriting the source study. fileciteturn12file0L84-L115 fileciteturn12file0L278-L329

The finite-shot section in the source notebook should also be interpreted carefully: it performs an exact-estimator VQE and then applies a Gaussian post-processing perturbation with σ ∝ 1/√Nshots; it is therefore a **shot-noise statistical model**, not a full finite-shot optimization using sampled Pauli measurements. fileciteturn13file0L636-L665

## Reported benchmark observations

At the equilibrium geometry used in the notebook (R(O–O) = 1.45 Å), the source workflow reports 4 qubits / 27 Pauli terms for Jordan–Wigner and 2 qubits / 9 Pauli terms for reduced parity, with both mappings reproducing the CAS reference to numerical precision. fileciteturn12file0L803-L921

The source notebook reports UCCSD reaching the CAS(2,2) reference at equilibrium for both the 4-qubit JW and 2-qubit parity implementations, while the 2-qubit EfficientSU2 result differs by 0.013 mHa in that run. fileciteturn13file0L41-L115

## Scope and limitations

This repository is a **small-system methodological benchmark**. It does not claim a quantum advantage over classical electronic-structure methods and does not represent a hardware demonstration. The active-space approximation, STO-3G basis, simulator configuration, optimizer, and noise model constrain the interpretation of all results.

In particular, the full-space FCI values are references within the STO-3G basis; CAS(2,2) is the direct target for the active-space VQE calculations.

## Citation

Citation metadata are provided in `CITATION.cff`. For a reproducible scientific citation, use a tagged release/DOI once the study reaches a stable version.

## Author

**Abdullah Hayder**

Biomedical Sciences · Bioinformatics · Quantum Computing for Biology
