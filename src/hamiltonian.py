"""CAS(2,2) second-quantized Hamiltonian construction and validation."""
from __future__ import annotations

import json
from pathlib import Path

import scipy.sparse.linalg as spla
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer
from qiskit_nature.second_q.mappers import JordanWignerMapper


def build_active_space_problem(atom_string: str):
    driver = PySCFDriver(atom=atom_string, basis="sto-3g", charge=0, spin=0)
    problem = driver.run()
    transformer = ActiveSpaceTransformer(num_electrons=2, num_spatial_orbitals=2)
    return transformer.transform(problem)


def validate_hamiltonians(
    catalog_path: str | Path = "geometries/h2o2_grid_catalog.json",
    reference_path: str | Path = "results/tables/classical_reference_energies.json",
    tolerance: float = 1e-6,
):
    catalog = json.loads(Path(catalog_path).read_text(encoding="utf-8"))
    refs = {
        x["geom_id"]: x["e_cas22_hartree"]
        for x in json.loads(Path(reference_path).read_text(encoding="utf-8"))
    }
    mapper = JordanWignerMapper()
    records = []
    for geom_id, data in catalog.items():
        problem = build_active_space_problem(data["pyscf_atom_string"])
        fermionic_op = problem.hamiltonian.second_q_op()
        offset = sum(problem.hamiltonian.constants.values())
        qubit_op = mapper.map(fermionic_op)
        evals, _ = spla.eigsh(qubit_op.to_matrix(sparse=True), k=1, which="SA")
        energy = evals[0].real + offset
        error = abs(energy - refs[geom_id])
        assert error < tolerance, f"Hamiltonian validation failed: {geom_id}: {error}"
        records.append({
            "geom_id": geom_id,
            "num_spin_orbitals": fermionic_op.num_spin_orbitals,
            "fermionic_terms": len(fermionic_op),
            "inactive_offset_hartree": float(offset),
            "diagonalization_error_hartree": float(error),
        })
    return records


if __name__ == "__main__":
    validate_hamiltonians()
