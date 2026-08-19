"""Circuit resource metrics for the JW and reduced-parity UCCSD ansätze."""
from __future__ import annotations

from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.mappers import JordanWignerMapper, ParityMapper


def _metrics(circuit, qubit_op, mapping):
    circuit = circuit.decompose().decompose()
    ops = circuit.count_ops()
    return {
        "mapping": mapping,
        "num_qubits": qubit_op.num_qubits,
        "num_pauli_terms": len(qubit_op),
        "total_gates": int(sum(ops.values())),
        "cnot_gates": int(ops.get("cx", 0)),
        "circuit_depth": int(circuit.depth()),
    }


def compare_uccsd_resources(problem):
    fermionic_op = problem.hamiltonian.second_q_op()
    n_particles = problem.num_particles
    n_orbitals = problem.num_spatial_orbitals
    records = []
    for mapping, mapper in (
        ("Jordan-Wigner (4-Qubit)", JordanWignerMapper()),
        ("Parity 2-Qubit Reduced", ParityMapper(num_particles=n_particles)),
    ):
        qop = mapper.map(fermionic_op)
        hf = HartreeFock(n_orbitals, n_particles, mapper)
        ansatz = UCCSD(n_orbitals, n_particles, mapper, initial_state=hf)
        records.append(_metrics(ansatz, qop, mapping))
    return records
