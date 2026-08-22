# Reproducibility Protocol

This document defines the canonical procedure for reproducing the H₂O₂ O–O dissociation study.

## 1. Clone

```bash
git clone https://github.com/abdullahayder29/quantum-vqe-h2o2-dissociation.git
cd quantum-vqe-h2o2-dissociation
```

## 2. Create the computational environment

`environment.yml` is the canonical environment specification. `requirements.txt` contains the same pinned Python packages for users who prefer pip.

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

The recorded study environment is Python 3.12.13 with PySCF 2.14.0, Qiskit 2.5.2, Qiskit Nature 0.8.0, Qiskit Aer 0.17.2, Qiskit Algorithms 0.4.0, NumPy 2.0.2, SciPy 1.16.3, pandas 2.2.2, and Matplotlib 3.10.0.

## 3. Validate the environment

```bash
python -c "import qiskit, qiskit_nature, qiskit_aer, pyscf; print('Qiskit:', qiskit.__version__); print('Qiskit Nature:', qiskit_nature.__version__); print('Qiskit Aer:', qiskit_aer.__version__); print('PySCF:', pyscf.__version__)"
```

## 4. Run the canonical study pipeline

From the repository root:

```bash
python -m pytest -q
python run_study.py
```

`run_study.py` is the canonical executable workflow. It generates the geometry catalog, RHF/CAS/full-FCI references, Hamiltonian validation, mapping comparison, equilibrium VQE benchmark, full dissociation PES, COBYLA convergence trajectories, resource estimates, tables, figures, and `results/study_summary.json`.

## 5. Research notebook

The single canonical notebook is:

`notebooks/H2O2_VQE_Bond_Dissociation.ipynb`

The notebook is the presentation and interactive analysis layer. The Python modules under `src/` and `run_study.py` are the canonical implementation layer. Avoid maintaining a second notebook that duplicates the computational pipeline.

## 6. Computational parameters that must be recorded

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
- number of shots, if sampled measurements are used;
- simulator or hardware backend;
- random seed where applicable.

## 7. Scientific provenance

Keep classical reference calculations, ideal simulator calculations, statistical shot-noise models, and future finite-shot/noisy calculations distinguishable. They should not be treated as interchangeable.

Every reported result should be traceable to:

`input parameters → source code/notebook cell → pinned environment → output artifact → figure/table`

## 8. Result artifacts

The canonical pipeline writes machine-readable tables to `results/tables/` and figures to `results/figures/`:

```text
results/
├── tables/
│   ├── classical_reference_energies.csv
│   ├── hamiltonian_validation.csv
│   ├── mapping_comparison.csv
│   ├── equilibrium_vqe_benchmark.csv
│   ├── vqe_pes_benchmark.csv
│   ├── vqe_convergence.csv
│   └── uccsd_resource_estimates.csv
├── figures/
│   ├── h2o2_dissociation_pes.png
│   ├── vqe_error_vs_bond_distance.png
│   ├── active_space_error_vs_bond_distance.png
│   ├── vqe_convergence.png
│   └── mapping_and_resources.png
└── study_summary.json
```

Derived results should be produced programmatically rather than manually edited. Do not overwrite an existing reported result without documenting the change in Git history.

## 9. Methodological boundary of the current study

The current baseline is an ideal-estimator VQE calculation. The repository's current shot-noise component is a statistical post-processing model with uncertainty scaling proportional to `1/sqrt(Nshots)`; it is **not** a genuine finite-shot VQE using sampled Pauli measurements.

Likewise, the current study is not a hardware demonstration and does not claim quantum advantage.

## 10. Version/provenance note

The source notebook contains older wording referring to a “Qiskit 1.x” stack, while the recorded installation output and pinned environment report Qiskit 2.5.2. The repository uses the recorded pinned environment as the reproducibility reference. Any future manuscript should describe the actual versions used in the final run.
