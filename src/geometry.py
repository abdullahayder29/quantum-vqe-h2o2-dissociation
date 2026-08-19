"""H2O2 O-O dissociation geometry generation.

This module preserves the geometry construction used in the research notebook.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

R_OO_GRID = [1.00, 1.20, 1.45, 1.80, 2.20, 2.60, 3.00]
R_OH = 0.965
THETA_OOH_DEG = 100.0
PHI_HOOH_DEG = 111.5


def generate_h2o2_geometry(
    r_oo: float,
    r_oh: float = R_OH,
    theta_ooh_deg: float = THETA_OOH_DEG,
    phi_deg: float = PHI_HOOH_DEG,
):
    """Generate the C2-symmetric Cartesian coordinates used by the notebook."""
    theta = np.radians(theta_ooh_deg)
    phi = np.radians(phi_deg)
    o1 = np.array([0.0, 0.0, r_oo / 2.0])
    o2 = np.array([0.0, 0.0, -r_oo / 2.0])
    z_h1 = o1[2] - r_oh * np.cos(theta)
    x_h1 = r_oh * np.sin(theta) * np.cos(phi / 2.0)
    y_h1 = r_oh * np.sin(theta) * np.sin(phi / 2.0)
    h1 = np.array([x_h1, y_h1, z_h1])
    h2 = np.array([x_h1, -y_h1, -z_h1])
    return np.vstack([o1, o2, h1, h2]), ["O", "O", "H", "H"]


def sanity_check_geometry(coords, target_r_oo: float, target_r_oh: float = R_OH):
    """Validate the O-O and O-H distances."""
    calc_r_oo = np.linalg.norm(coords[0] - coords[1])
    calc_r_oh1 = np.linalg.norm(coords[0] - coords[2])
    calc_r_oh2 = np.linalg.norm(coords[1] - coords[3])
    assert np.isclose(calc_r_oo, target_r_oo, atol=1e-5)
    assert np.isclose(calc_r_oh1, target_r_oh, atol=1e-5)
    assert np.isclose(calc_r_oh2, target_r_oh, atol=1e-5)


def build_dissociation_grid(output_dir: str | Path = "geometries"):
    """Generate XYZ geometries and a JSON catalog for the seven-point scan."""
    output_dir = Path(output_dir)
    xyz_dir = output_dir / "xyz"
    xyz_dir.mkdir(parents=True, exist_ok=True)
    catalog = {}
    for idx, r_oo in enumerate(R_OO_GRID, start=1):
        geom_id = f"H2O2_R{idx:02d}_{r_oo:.2f}A"
        coords, symbols = generate_h2o2_geometry(r_oo)
        sanity_check_geometry(coords, r_oo)
        atom_string = "; ".join(
            f"{sym} {c[0]:.6f} {c[1]:.6f} {c[2]:.6f}"
            for sym, c in zip(symbols, coords)
        )
        xyz_path = xyz_dir / f"{geom_id}.xyz"
        with xyz_path.open("w", encoding="utf-8") as f:
            f.write("4\n")
            f.write(f"H2O2 O-O dissociation coordinate point R = {r_oo:.2f} Angstrom\n")
            for sym, c in zip(symbols, coords):
                f.write(f"{sym:2s} {c[0]:12.6f} {c[1]:12.6f} {c[2]:12.6f}\n")
        catalog[geom_id] = {
            "r_oo_angstrom": r_oo,
            "pyscf_atom_string": atom_string,
            "xyz_file": str(xyz_path),
            "charge": 0,
            "spin": 0,
        }
    with (output_dir / "h2o2_grid_catalog.json").open("w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=4)
    return catalog


if __name__ == "__main__":
    build_dissociation_grid()
