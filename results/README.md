# Results

Results produced by the notebook belong here.

Recommended organization:

```text
results/
├── classical/
├── vqe/
├── noise/
└── resource_estimates/
```

Each result file should record, at minimum:

- date/time of generation
- software environment or environment lock
- molecule and basis set
- geometry / O-O distance
- active-space definition
- mapper and symmetry-reduction settings
- ansatz
- optimizer and convergence settings
- simulator/backend
- number of shots, when applicable
- random seed, when applicable

Do not manually edit generated numerical results without documenting the change.
