"""Shot-noise model and circuit-resource analysis.

IMPORTANT: the original notebook computes an exact statevector VQE and then
adds a Gaussian perturbation with sigma=sqrt(0.25/shots). This is a statistical
post-processing model, not a finite-shot execution of every Hamiltonian term.
The implementation below preserves that original methodology explicitly.
"""
from __future__ import annotations

import numpy as np
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA, SPSA

try:
    from qiskit.primitives import StatevectorEstimator as Estimator
except ImportError:
    from qiskit.primitives import Estimator


def simulate_shot_noise_vqe(ansatz, qubit_op, optimizer, offset, reference_energy, shots=None, random_seed=42):
    np.random.seed(random_seed)
    vqe = VQE(estimator=Estimator(), ansatz=ansatz, optimizer=optimizer, initial_point=np.zeros(ansatz.num_parameters))
    result = vqe.compute_minimum_eigenvalue(qubit_op)
    exact_energy = float(result.eigenvalue.real + offset)
    if shots is None or shots == "Infinity":
        final_energy = exact_energy
    else:
        sigma = np.sqrt(0.25 / shots)
        final_energy = exact_energy + np.random.normal(0.0, sigma)
    error_mha = abs(final_energy - reference_energy) * 1000.0
    return final_energy, error_mha


def benchmark_shots(ansatz, qubit_op, offset, reference_energy, shots=(1024, 8192, 65536), seed=101):
    records = []
    exact, err = simulate_shot_noise_vqe(ansatz, qubit_op, COBYLA(maxiter=200), offset, reference_energy, "Infinity")
    records.append({"shots": "Infinity", "optimizer": "COBYLA", "e_vqe_hartree": exact, "error_mha": err})
    for n in shots:
        for name, optimizer in (("COBYLA", COBYLA(maxiter=150)), ("SPSA", SPSA(maxiter=100))):
            energy, error = simulate_shot_noise_vqe(ansatz, qubit_op, optimizer, offset, reference_energy, n, seed)
            records.append({"shots": n, "optimizer": name, "e_vqe_hartree": energy, "error_mha": error})
            seed += 1
    return records
