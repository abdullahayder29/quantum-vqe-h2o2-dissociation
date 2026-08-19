"""VQE benchmark implementations used in the H2O2 study."""
from __future__ import annotations

import numpy as np
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.mappers import JordanWignerMapper, ParityMapper
from qiskit.circuit.library import EfficientSU2

try:
    from qiskit.primitives import StatevectorEstimator as Estimator
except ImportError:  # pragma: no cover - compatibility with older Qiskit
    from qiskit.primitives import Estimator


def run_vqe_single_point(ansatz, qubit_operator, optimizer, initial_point=None):
    history = []

    def callback(eval_count, params, value, metadata=None):
        history.append(float(value))

    vqe = VQE(
        estimator=Estimator(),
        ansatz=ansatz,
        optimizer=optimizer,
        initial_point=initial_point,
        callback=callback,
    )
    return vqe.compute_minimum_eigenvalue(qubit_operator), history


def benchmark_equilibrium(problem, reference_energy: float):
    """Run the notebook's three equilibrium VQE architectures."""
    fermionic_op = problem.hamiltonian.second_q_op()
    offset = sum(problem.hamiltonian.constants.values())
    n_particles = problem.num_particles
    n_orbitals = problem.num_spatial_orbitals
    records = []

    mapper = JordanWignerMapper()
    qop = mapper.map(fermionic_op)
    hf = HartreeFock(n_orbitals, n_particles, mapper)
    ansatz = UCCSD(n_orbitals, n_particles, mapper, initial_state=hf)
    result, history = run_vqe_single_point(ansatz, qop, COBYLA(maxiter=200), np.zeros(ansatz.num_parameters))
    energy = float(result.eigenvalue.real + offset)
    records.append({"ansatz": "UCCSD (4-Qubit JW)", "num_qubits": 4, "num_parameters": ansatz.num_parameters, "iterations": len(history), "vqe_energy_hartree": energy, "error_mha": abs(energy-reference_energy)*1000})

    mapper = ParityMapper(num_particles=n_particles)
    qop = mapper.map(fermionic_op)
    hf = HartreeFock(n_orbitals, n_particles, mapper)
    ansatz = UCCSD(n_orbitals, n_particles, mapper, initial_state=hf)
    result, history = run_vqe_single_point(ansatz, qop, COBYLA(maxiter=200), np.zeros(ansatz.num_parameters))
    energy = float(result.eigenvalue.real + offset)
    records.append({"ansatz": "UCCSD (2-Qubit Parity)", "num_qubits": 2, "num_parameters": ansatz.num_parameters, "iterations": len(history), "vqe_energy_hartree": energy, "error_mha": abs(energy-reference_energy)*1000})

    ansatz = EfficientSU2(num_qubits=2, su2_gates=["ry", "rz"], entanglement="linear", reps=1)
    result, history = run_vqe_single_point(ansatz, qop, COBYLA(maxiter=300))
    energy = float(result.eigenvalue.real + offset)
    records.append({"ansatz": "EfficientSU2 (2-Qubit HEA)", "num_qubits": 2, "num_parameters": ansatz.num_parameters, "iterations": len(history), "vqe_energy_hartree": energy, "error_mha": abs(energy-reference_energy)*1000})
    return records
