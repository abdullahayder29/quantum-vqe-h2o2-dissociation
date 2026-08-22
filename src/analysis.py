"""Analysis helpers for benchmark tables and publication figures."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def load_pes(path: str | Path = "results/tables/vqe_pes_benchmark.csv") -> pd.DataFrame:
    return pd.read_csv(path)


def _save(fig, output: str | Path) -> None:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_pes(df: pd.DataFrame, output: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    r = df["r_oo_angstrom"]
    ax.plot(r, df["e_rhf_hartree"], "--o", label="RHF")
    ax.plot(r, df["e_cas22_hartree"], "-s", label="CAS(2,2)")
    ax.plot(r, df["e_vqe_uccsd_hartree"], "--^", label="VQE UCCSD")
    ax.plot(r, df["e_fci_full_hartree"], ":", label="Full FCI")
    ax.set_xlabel("O-O interatomic distance R (Å)")
    ax.set_ylabel("Total electronic energy (Hartree)")
    ax.set_title("H₂O₂ O-O Dissociation Potential Energy Surface")
    ax.legend()
    _save(fig, output)


def plot_error(df: pd.DataFrame, output: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(1.6, linestyle="--", label="Chemical-accuracy threshold (1.6 mHa)")
    ax.plot(df["r_oo_angstrom"], df["vqe_error_mha"], "o-", label="UCCSD VQE error")
    ax.set_xlabel("O-O interatomic distance R (Å)")
    ax.set_ylabel("Absolute error vs CAS(2,2) (mHa)")
    ax.set_title("VQE Accuracy Along the Dissociation Coordinate")
    ax.legend()
    _save(fig, output)


def plot_mapping_resources(mapping: pd.DataFrame, resources: pd.DataFrame, output: str | Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].bar(mapping["mapping"], mapping["num_pauli_terms"])
    axes[0].set_ylabel("Number of Pauli terms")
    axes[0].set_title("Hamiltonian size by mapping")
    axes[0].tick_params(axis="x", rotation=35)

    axes[1].bar(resources["mapping"], resources["circuit_depth"])
    axes[1].set_ylabel("Circuit depth")
    axes[1].set_title("UCCSD circuit depth")
    axes[1].tick_params(axis="x", rotation=35)
    _save(fig, output)
