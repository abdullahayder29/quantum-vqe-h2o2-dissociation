# Reproducibility protocol

## 1. Environment

Use `environment.yml` to create the pinned computational environment:

```bash
conda env create -f environment.yml
conda activate h2o2-vqe
```

The recorded notebook environment reports Python 3.12.13, PySCF 2.14.0, Qiskit 2.5.2, Qiskit Nature 0.8.0, Qiskit Aer 0.17.2, NumPy 2.0.2, SciPy 1.16.3, pandas 2.2.2, and Matplotlib 3.10.0.

## 2. Execution

Open the research notebook under `notebooks/` and execute cells in order. The notebook is the primary executable record of the study.

## 3. Geometry

The O-O dissociation scan is generated from the fixed molecular parameters documented in `data/README.md`. Do not hand-edit generated geometries when reproducing a result.

## 4. Classical reference

Run the classical electronic-structure calculations before evaluating VQE results. Reference energies provide the baseline against which variational energies are compared.

## 5. Quantum calculation

Record the mapper, active space, ansatz, optimizer, convergence threshold, initial point, simulator/backend, and shot count. For noisy or shot-based experiments, record the random seed where supported.

## 6. Outputs

Store generated tables and figures under `results/`. A result should be traceable from the output file to the notebook cell and environment that generated it.

## 7. Version control

Never overwrite a published result silently. Changes to computational settings should be represented by a Git commit and described in the commit message or a changelog.

## Important source note

The supplied notebook describes its stack as “Qiskit 1.x” but its recorded installation output and validation environment report Qiskit 2.5.2. This repository preserves the recorded environment rather than silently changing the source methodology. The terminology should be reconciled in a future manuscript/revision before publication.
