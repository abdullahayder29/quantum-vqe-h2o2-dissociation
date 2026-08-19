import numpy as np

from src.geometry import generate_h2o2_geometry, sanity_check_geometry, R_OO_GRID


def test_grid_definition():
    assert R_OO_GRID == [1.00, 1.20, 1.45, 1.80, 2.20, 2.60, 3.00]


def test_geometry_bond_lengths():
    coords, symbols = generate_h2o2_geometry(1.45)
    assert symbols == ["O", "O", "H", "H"]
    sanity_check_geometry(coords, 1.45)
    assert np.isclose(np.linalg.norm(coords[0] - coords[1]), 1.45, atol=1e-5)
