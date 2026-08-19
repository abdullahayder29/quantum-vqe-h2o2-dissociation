# Reproducibility Protocol

This document defines the canonical procedure for reproducing the H₂O₂ O–O dissociation study.

## 1. Clone

```bash
git clone https://github.com/abdullahayder29/quantum-vqe-h2o2-dissociation.git
cd quantum-vqe-h2o2-dissociation
```

## 2. Create the computational environment

The repository provides `environment.yml` and `requirements.txt`.

### Conda

```bash
conda env create -f environment.yml
conda activate h2o2-vqe
```

### pip

For a clean Python 3.12 environment:

```bash
python -m pip install -r requirements.txt
```

The original notebook execution records Python 3.12.13, PySCF 2.14.0, Qiskit 2.5.2, Qiskit Nature 0.8.0, Qiskit Aer 0.17.2, NumPy 2.0.2, SciPy 1.16.3, pandas 2.2.2, and Matplotlib 3.10.0. These recorded versions should be treated as the provenance of the supplied run.

## 3. Validate the environment

```bash
python -c "import qiskit, qiskit_nature, qiskit_aer, pyscf; print('Qiskit:', qiskit.__version__); print('Qiskit Nature:', qiskit_nature.__version__); print('Qiskit Aer:', qiskit_aer.__version__); print('PySCF:', pyscf.__version__)"
```

## 4. Execute the research notebook

Open:

`notebooks/H2O2_VQE_Bond_Dissociation.ipynb`

Execute it from a fresh kernel, in order.

The executable workflow covers:

1. environment validation;
2. H₂O₂ geometry generation;
3. classical electronic-structure reference calculations;
4. active-space Hamiltonian construction;
5. fermion-to-qubit mapping;
6. parity/Z₂ symmetry reduction;
7. VQE;
8. potential-energy-surface benchmarking;
9. finite-shot/noise analysis;
10. quantum-resource estimation.

## 5. Computational parameters that must be recorded

For every reproducible run, record:

- Python and package versions;
- operating system and CPU/backend;
- basis set;
- molecular geometry;
- O–O distance grid;
- active space and electron count;
- mapper and symmetry-reduction settings;
- ansatz;
- optimizer;
- initial parameters;
- convergence threshold;
- maximum iterations;
- number of shots;
- simulator or hardware backend;
- random seed where applicable.

## 6. Scientific provenance

Keep classical reference calculations, ideal simulator calculations, and finite-shot/noisy calculations distinguishable. Their results should not be treated as interchangeable.

Every reported result should be traceable to:

`input parameters → source code/notebook cell → environment → output artifact → figure/table`

## 7. Result artifacts

Generated machine-readable tables belong in `results/`. Figures belong in `figures/`. Derived results should be produced programmatically rather than manually edited.

Do not overwrite an existing reported result without documenting the change in Git history.

## 8. Source-methodology note

The supplied notebook describes its stack as “Qiskit 1.x”, while its recorded installation output and validation environment report Qiskit 2.5.2. This repository preserves the recorded environment rather than silently changing the source methodology. The terminology should be reconciled in a future manuscript/revision before publication.
