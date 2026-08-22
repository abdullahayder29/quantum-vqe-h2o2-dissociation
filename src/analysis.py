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
    """Plot the total-energy dissociation curves."""
    fig, ax = plt.subplots(figsize=(8, 5))
    r = df["r_oo_angstrom"]
    ax.plot(r, df["e_rhf_hartree"], "--o", label="RHF")
    ax.plot(r, df["e_cas22_hartree"], "-s", label="Exact CAS(2,2) reference")
    ax.plot(r, df["e_vqe_uccsd_hartree"], "--^", label="VQE (UCCSD, 2-qubit)")
    ax.plot(r, df["e_fci_full_hartree"], ":", label="Full-space FCI (STO-3G)")
    ax.set_xlabel("O-O interatomic distance R (Å)")
    ax.set_ylabel("Total electronic energy (Hartree)")
    ax.set_title(r"H$_2$O$_2$ Homolytic O-O Dissociation Potential Energy Surface")
    ax.legend()
    _save(fig, output)


def plot_error(df: pd.DataFrame, output: str | Path) -> None:
    """Plot VQE error relative to the active-space reference."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(1.6, linestyle="--", label="Chemical-accuracy threshold (1.6 mHa)")
    ax.plot(df["r_oo_angstrom"], df["vqe_error_mha"], "o-", label="UCCSD VQE error")
    ax.set_xlabel("O-O interatomic distance R (Å)")
    ax.set_ylabel("Absolute error vs CAS(2,2) (mHa)")
    ax.set_title("VQE Accuracy Along the Dissociation Coordinate")
    ax.legend()
    _save(fig, output)


def add_active_space_error(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with the CAS(2,2)-to-FCI model error in mHa."""
    out = df.copy()
    out["active_space_error_mha"] = (
        (out["e_cas22_hartree"] - out["e_fci_full_hartree"]).abs() * 1000.0
    )
    return out


def plot_active_space_error(df: pd.DataFrame, output: str | Path) -> None:
    """Plot the model-space error separately from VQE optimization error."""
    data = add_active_space_error(df)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        data["r_oo_angstrom"],
        data["active_space_error_mha"],
        "o-",
        label="|CAS(2,2) - full FCI|",
    )
    ax.set_xlabel("O-O interatomic distance R (Å)")
    ax.set_ylabel("Absolute model-space error (mHa)")
    ax.set_title("Active-Space Approximation Error Along Dissociation")
    ax.legend()
    _save(fig, output)


def plot_convergence(convergence: pd.DataFrame, output: str | Path) -> None:
    """Plot optimizer energy trajectories for selected geometries."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for distance, group in convergence.groupby("r_oo_angstrom", sort=True):
        ax.plot(
            group["evaluation"],
            group["energy_hartree"],
            label=f"R = {distance:.2f} Å",
        )
    ax.set_xlabel("Optimizer evaluation")
    ax.set_ylabel("Energy evaluation (Hartree)")
    ax.set_title("VQE Optimizer Energy Convergence (COBYLA)")
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
