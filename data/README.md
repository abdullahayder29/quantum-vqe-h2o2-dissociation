# Data

This directory contains generated inputs and derived numerical data for the H2O2 O-O dissociation benchmark.

## Provenance

The molecular geometry workflow in the research notebook defines a seven-point O-O dissociation grid:

`1.00, 1.20, 1.45, 1.80, 2.20, 2.60, 3.00 Å`

Fixed geometric parameters used by the notebook are:

- O-H = 0.965 Å
- O-O-H = 100°
- H-O-O-H dihedral = 111.5°
- charge = 0
- spin = 0 (closed-shell singlet)

The notebook generates XYZ geometries and a JSON catalog from these parameters. Derived results should be regenerated rather than treated as immutable source data whenever practical.

Large generated files should not be committed unless they are necessary for reproducing or auditing a published result.
