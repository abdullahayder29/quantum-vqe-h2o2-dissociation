import json
from pathlib import Path

import pandas as pd

from src.geometry import build_dissociation_grid, R_OO_GRID


def test_geometry_grid(tmp_path):
    catalog = build_dissociation_grid(tmp_path)
    assert len(catalog) == len(R_OO_GRID)
    distances = [row['r_oo_angstrom'] for row in catalog.values()]
    assert distances == sorted(distances)
    assert all(row['charge'] == 0 for row in catalog.values())
    assert all(row['spin'] == 0 for row in catalog.values())
    assert (tmp_path / 'h2o2_grid_catalog.json').exists()


def test_generated_pes_schema():
    path = Path('results/tables/vqe_pes_benchmark.csv')
    if not path.exists():
        return
    df = pd.read_csv(path)
    required = {
        'geom_id', 'r_oo_angstrom', 'e_rhf_hartree', 'e_cas22_hartree',
        'e_vqe_uccsd_hartree', 'e_fci_full_hartree', 'vqe_error_mha',
        'vqe_iterations', 'chemical_accuracy'
    }
    assert required.issubset(df.columns)
    assert len(df) == len(R_OO_GRID)
    assert (df['vqe_error_mha'] >= 0).all()


def test_generated_convergence_schema():
    path = Path('results/tables/vqe_convergence.csv')
    if not path.exists():
        return
    df = pd.read_csv(path)
    required = {
        'geom_id', 'r_oo_angstrom', 'evaluation', 'energy_hartree',
        'error_mha', 'final_vqe_energy_hartree'
    }
    assert required.issubset(df.columns)
    assert df['r_oo_angstrom'].nunique() == 2
    assert df['evaluation'].min() == 0


def test_summary_schema():
    path = Path('results/study_summary.json')
    if not path.exists():
        return
    summary = json.loads(path.read_text())
    assert summary['chemical_accuracy_threshold_mha'] == 1.6
    assert 'all_pes_points_chemical_accuracy' in summary
    assert 'max_active_space_error_mha' in summary
    assert 'files' in summary
