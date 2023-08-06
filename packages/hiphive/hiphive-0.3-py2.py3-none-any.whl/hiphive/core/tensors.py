"""
Module containing tensor related functions
"""

import numpy as np


_paths = dict()


def rotate_tensor(T, R, path=None):
    """Equivalent to T_abc... = T_ijk... R_ia R_jb R_kc ... """

    order = len(T.shape)
    if order not in _paths:
        path = ['einsum_path', (0, 1)]
        for i in range(order - 1, 0, -1):
            path.append((0, i))
        _paths[order] = path

    einsum_input = [T, list(range(order))]
    for i in range(order):
        einsum_input.append(R)
        einsum_input.append([i, order + i])
    return np.einsum(*einsum_input, optimize=_paths[order])


def rotation_to_cart_coord(R, cell):
    """Return the rotation matrix in cart coord given a cell metric """
    return np.dot(np.dot(cell.T, R), np.linalg.inv(cell.T))
