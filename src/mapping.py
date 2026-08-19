"""Qubit mapping comparisons for the CAS(2,2) Hamiltonian."""
from __future__ import annotations

import numpy as np
import scipy.sparse.linalg as spla
from qiskit_nature.second_q.mappers import JordanWignerMapper, BravyiKitaevMapper, ParityMapper


def compute_pauli_weight(pauli_op):
    weights = [sum(c in "XYZ" for c in label) for label in pauli_op.paulis.to_labels()]
    return float(np.mean(weights)), int(np.max(weights))


def compare_mappings(problem, reference_energy: float):
    fermionic_op = problem.hamiltonian.second_q_op()
    offset = sum(problem.hamiltonian.constants.values())
    mappers = {
        "Jordan-Wigner": JordanWignerMapper(),
        "Bravyi-Kitaev": BravyiKitaevMapper(),
        "Parity (Standard)": ParityMapper(),
        "Parity (2-Qubit Reduced)": ParityMapper(num_particles=problem.num_particles),
    }
    records = []
    for name, mapper in mappers.items():
        qubit_op = mapper.map(fermionic_op)
        avg_weight, max_weight = compute_pauli_weight(qubit_op)
        evals, _ = spla.eigsh(qubit_op.to_matrix(sparse=True), k=1, which="SA")
        energy = evals[0].real + offset
        error = abs(energy - reference_energy)
        assert error < 1e-6
        records.append({
            "mapping": name,
            "num_qubits": qubit_op.num_qubits,
            "num_pauli_terms": len(qubit_op),
            "avg_pauli_weight": avg_weight,
            "max_pauli_weight": max_weight,
            "eigenvalue_error_hartree": float(error),
        })
    return records
