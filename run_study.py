"""End-to-end reproducible H2O2 VQE dissociation study.

Run from the repository root with:
    python run_study.py

The script generates geometry, classical-reference, Hamiltonian, VQE,
convergence, resource and figure artifacts. No benchmark numbers are
hard-coded: results are produced by PySCF/Qiskit.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.geometry import build_dissociation_grid, R_OO_GRID
from src.classical_reference import run_classical_references
from src.hamiltonian import build_active_space_problem, validate_hamiltonians
from src.mapping import compare_mappings
from src.resource_estimation import compare_uccsd_resources
from src.vqe import benchmark_equilibrium, run_vqe_single_point
from src.analysis import (
    plot_pes,
    plot_error,
    plot_active_space_error,
    plot_convergence,
    plot_mapping_resources,
)
from qiskit_algorithms.optimizers import COBYLA
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.mappers import JordanWignerMapper

ROOT = Path(__file__).resolve().parent
GEOMETRY_DIR = ROOT / "geometries"
RESULTS = ROOT / "results"
TABLES = RESULTS / "tables"
FIGURES = RESULTS / "figures"


def run_pes(catalog: dict, references: pd.DataFrame) -> pd.DataFrame:
    ref_by_id = references.set_index("geom_id")["e_cas22_hartree"].to_dict()
    rows = []
    for geom_id, data in catalog.items():
        problem = build_active_space_problem(data["pyscf_atom_string"])
        fermionic_op = problem.hamiltonian.second_q_op()
        offset = sum(problem.hamiltonian.constants.values())
        mapper = JordanWignerMapper()
        qop = mapper.map(fermionic_op)
        hf = HartreeFock(problem.num_spatial_orbitals, problem.num_particles, mapper)
        ansatz = UCCSD(problem.num_spatial_orbitals, problem.num_particles, mapper, initial_state=hf)
        result, history = run_vqe_single_point(
            ansatz,
            qop,
            COBYLA(maxiter=200),
            initial_point=[0.0] * ansatz.num_parameters,
        )
        energy = float(result.eigenvalue.real + offset)
        reference = float(ref_by_id[geom_id])
        rows.append({
            "geom_id": geom_id,
            "r_oo_angstrom": data["r_oo_angstrom"],
            "e_rhf_hartree": float(references.loc[references.geom_id == geom_id, "e_rhf_hartree"].iloc[0]),
            "e_cas22_hartree": reference,
            "e_vqe_uccsd_hartree": energy,
            "e_fci_full_hartree": float(references.loc[references.geom_id == geom_id, "e_fci_full_hartree"].iloc[0]),
            "vqe_error_mha": abs(energy - reference) * 1000.0,
            "vqe_iterations": len(history),
            "chemical_accuracy": abs(energy - reference) <= 0.0016,
        })
    df = pd.DataFrame(rows).sort_values("r_oo_angstrom")
    df.to_csv(TABLES / "vqe_pes_benchmark.csv", index=False)
    return df


def run_convergence_study(catalog: dict, references: pd.DataFrame) -> pd.DataFrame:
    """Record optimizer trajectories at equilibrium and a stretched geometry."""
    ref_by_id = references.set_index("geom_id")["e_cas22_hartree"].to_dict()
    equilibrium_id = min(catalog, key=lambda k: abs(catalog[k]["r_oo_angstrom"] - 1.45))
    stretched_id = max(catalog, key=lambda k: catalog[k]["r_oo_angstrom"])
    rows = []

    for geom_id in (equilibrium_id, stretched_id):
        data = catalog[geom_id]
        problem = build_active_space_problem(data["pyscf_atom_string"])
        fermionic_op = problem.hamiltonian.second_q_op()
        offset = sum(problem.hamiltonian.constants.values())
        mapper = JordanWignerMapper()
        qop = mapper.map(fermionic_op)
        hf = HartreeFock(problem.num_spatial_orbitals, problem.num_particles, mapper)
        ansatz = UCCSD(problem.num_spatial_orbitals, problem.num_particles, mapper, initial_state=hf)
        result, history = run_vqe_single_point(
            ansatz,
            qop,
            COBYLA(maxiter=200),
            initial_point=[0.0] * ansatz.num_parameters,
        )
        reference = float(ref_by_id[geom_id])
        for evaluation, value in enumerate(history):
            rows.append({
                "geom_id": geom_id,
                "r_oo_angstrom": data["r_oo_angstrom"],
                "evaluation": evaluation,
                "energy_hartree": float(value + offset),
                "error_mha": abs(float(value + offset) - reference) * 1000.0,
                "final_vqe_energy_hartree": float(result.eigenvalue.real + offset),
            })

    df = pd.DataFrame(rows)
    df.to_csv(TABLES / "vqe_convergence.csv", index=False)
    return df


def main() -> None:
    for directory in (GEOMETRY_DIR, TABLES, FIGURES):
        directory.mkdir(parents=True, exist_ok=True)

    print("[1/8] Generating H2O2 dissociation geometries")
    catalog = build_dissociation_grid(GEOMETRY_DIR)

    print("[2/8] Running RHF, CAS(2,2) and full-space FCI references")
    references = run_classical_references(
        GEOMETRY_DIR / "h2o2_grid_catalog.json", TABLES
    )

    print("[3/8] Validating the active-space Hamiltonian against CAS(2,2)")
    validation = validate_hamiltonians(
        GEOMETRY_DIR / "h2o2_grid_catalog.json",
        TABLES / "classical_reference_energies.json",
    )
    pd.DataFrame(validation).to_csv(TABLES / "hamiltonian_validation.csv", index=False)

    equilibrium_id = min(catalog, key=lambda k: abs(catalog[k]["r_oo_angstrom"] - 1.45))
    equilibrium = catalog[equilibrium_id]
    equilibrium_reference = float(
        references.loc[references.geom_id == equilibrium_id, "e_cas22_hartree"].iloc[0]
    )
    problem = build_active_space_problem(equilibrium["pyscf_atom_string"])

    print("[4/8] Comparing fermion-to-qubit mappings at equilibrium")
    mapping = pd.DataFrame(compare_mappings(problem, equilibrium_reference))
    mapping.to_csv(TABLES / "mapping_comparison.csv", index=False)

    print("[5/8] Estimating UCCSD circuit resources")
    resources = pd.DataFrame(compare_uccsd_resources(problem))
    resources.to_csv(TABLES / "uccsd_resource_estimates.csv", index=False)

    print("[6/8] Running equilibrium VQE benchmarks and the dissociation PES")
    vqe_eq = pd.DataFrame(benchmark_equilibrium(problem, equilibrium_reference))
    vqe_eq.to_csv(TABLES / "equilibrium_vqe_benchmark.csv", index=False)
    pes = run_pes(catalog, references)

    print("[7/8] Recording convergence and generating figures")
    convergence = run_convergence_study(catalog, references)
    plot_pes(pes, FIGURES / "h2o2_dissociation_pes.png")
    plot_error(pes, FIGURES / "vqe_error_vs_bond_distance.png")
    plot_active_space_error(pes, FIGURES / "active_space_error_vs_bond_distance.png")
    plot_convergence(convergence, FIGURES / "vqe_convergence.png")
    plot_mapping_resources(mapping, resources, FIGURES / "mapping_and_resources.png")

    print("[8/8] Writing study summary")
    active_space_gap = (
        (pes["e_cas22_hartree"] - pes["e_fci_full_hartree"]).abs() * 1000.0
    )
    summary = {
        "equilibrium_r_oo_angstrom": equilibrium["r_oo_angstrom"],
        "grid_angstrom": R_OO_GRID,
        "chemical_accuracy_threshold_mha": 1.6,
        "all_pes_points_chemical_accuracy": bool(pes["chemical_accuracy"].all()),
        "max_vqe_error_mha": float(pes["vqe_error_mha"].max()),
        "min_vqe_error_mha": float(pes["vqe_error_mha"].min()),
        "max_active_space_error_mha": float(active_space_gap.max()),
        "min_active_space_error_mha": float(active_space_gap.min()),
        "convergence_geometries_angstrom": sorted(convergence["r_oo_angstrom"].unique().tolist()),
        "files": {
            "classical_references": "results/tables/classical_reference_energies.csv",
            "hamiltonian_validation": "results/tables/hamiltonian_validation.csv",
            "mapping_comparison": "results/tables/mapping_comparison.csv",
            "equilibrium_vqe": "results/tables/equilibrium_vqe_benchmark.csv",
            "pes": "results/tables/vqe_pes_benchmark.csv",
            "convergence": "results/tables/vqe_convergence.csv",
            "resources": "results/tables/uccsd_resource_estimates.csv",
            "pes_figure": "results/figures/h2o2_dissociation_pes.png",
            "error_figure": "results/figures/vqe_error_vs_bond_distance.png",
            "active_space_error_figure": "results/figures/active_space_error_vs_bond_distance.png",
            "convergence_figure": "results/figures/vqe_convergence.png",
            "resource_figure": "results/figures/mapping_and_resources.png",
        },
    }
    (RESULTS / "study_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
