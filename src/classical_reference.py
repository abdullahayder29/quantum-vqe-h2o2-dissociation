"""RHF, CAS(2,2) and full-space FCI reference calculations."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from pyscf import gto, scf, fci, mcscf


def run_classical_references(
    catalog_path: str | Path = "geometries/h2o2_grid_catalog.json",
    output_dir: str | Path = "results/tables",
):
    """Reproduce the notebook's classical reference calculation."""
    catalog_path = Path(catalog_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    results = []
    for geom_id, data in catalog.items():
        mol = gto.Mole()
        mol.atom = data["pyscf_atom_string"]
        mol.basis = "sto-3g"
        mol.charge = 0
        mol.spin = 0
        mol.verbose = 0
        mol.build()
        mf = scf.RHF(mol)
        e_rhf = mf.kernel()
        assert mf.converged, f"RHF failed to converge for {geom_id}"
        homo_idx = mol.nelectron // 2 - 1
        mycas = mcscf.CASCI(mf, ncas=2, nelecas=2)
        mycas.sort_mo([homo_idx + 1, homo_idx + 2])
        e_cas, *_ = mycas.kernel()
        e_fci_full, _ = fci.FCI(mf).kernel()
        results.append({
            "geom_id": geom_id,
            "r_oo_angstrom": data["r_oo_angstrom"],
            "e_rhf_hartree": float(e_rhf),
            "e_cas22_hartree": float(e_cas),
            "e_fci_full_hartree": float(e_fci_full),
            "active_corr_energy_mha": float((e_cas - e_rhf) * 1000.0),
            "rhf_converged": bool(mf.converged),
        })
    df = pd.DataFrame(results)
    df.to_csv(output_dir / "classical_reference_energies.csv", index=False)
    (output_dir / "classical_reference_energies.json").write_text(
        json.dumps(results, indent=4), encoding="utf-8"
    )
    return df


if __name__ == "__main__":
    run_classical_references()
