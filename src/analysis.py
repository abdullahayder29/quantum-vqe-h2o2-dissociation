"""Analysis helpers for benchmark tables and publication figures."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def load_pes(path: str | Path = "results/tables/vqe_pes_benchmark.csv"):
    return pd.read_csv(path)


def plot_pes(df: pd.DataFrame, output: str | Path):
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    r = df["r_oo_angstrom"]
    ax.plot(r, df["e_rhf_hartree"], "--o", label="RHF")
    ax.plot(r, df["e_cas22_hartree"], "-s", label="CAS(2,2)")
    ax.plot(r, df["e_vqe_uccsd_hartree"], "--^", label="VQE UCCSD")
    ax.plot(r, df["e_fci_full_hartree"], ":", label="Full FCI")
    ax.set_xlabel("O-O Interatomic Distance R (Å)")
    ax.set_ylabel("Total Electronic Energy (Hartree)")
    ax.set_title("H₂O₂ Homolytic O-O Dissociation Potential Energy Surface")
    ax.legend()
    fig.tight_layout()
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output)
    plt.close(fig)
