# Data and Input Provenance

This directory contains inputs and derived numerical data for the H₂O₂ O–O dissociation benchmark.

## Molecular system

The study follows homolytic O–O bond dissociation:

`H₂O₂ → 2 ·OH`

## Dissociation coordinate

The research notebook defines a seven-point O–O dissociation grid:

`1.00, 1.20, 1.45, 1.80, 2.20, 2.60, 3.00 Å`

Fixed geometric parameters used by the notebook are:

- O–H = 0.965 Å
- O–O–H = 100°
- H–O–O–H dihedral = 111.5°
- charge = 0
- spin = 0 (closed-shell singlet)

The notebook generates XYZ geometries and a JSON catalog from these parameters.

## Directory policy

- `raw/` is reserved for immutable source inputs.
- `processed/` contains generated or transformed data.
- Generated data should be reproducible from documented parameters whenever practical.
- Do not manually edit numerical outputs.
- Large generated files should not be committed unless required for reproducing or auditing a published result.

## Provenance chain

Every derived dataset should be traceable to:

`geometry/configuration → computational code or notebook cell → environment → output dataset`

The primary executable source is `notebooks/H2O2_VQE_Bond_Dissociation.ipynb`.
