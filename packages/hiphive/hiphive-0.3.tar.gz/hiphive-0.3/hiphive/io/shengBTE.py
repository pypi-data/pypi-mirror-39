"""
The ``io.shengBTE`` module provides functions for reading and writing data
files in shengBTE format.

Todo
----
These functions have not really been tested, i.e. write a fc3 with
write_shengBTE_fc3 and pass the file to shengBTE

"""

import numpy as np
from ase.geometry import find_mic
from itertools import product


def read_shengBTE_fc3(filename):
    """ Read shengBTE fc3 file.

    Parameters
    ----------
    filename : str
        input file name

    Returns
    -------
    list
        list with shengBTE block entries, where an entry consist of
        [i, j, k, cell_pos2, cell_pos3, fc3]
    """
    lines_per_fc_block = 32

    fc3_data_shengBTE = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        num_fcs = int(lines[0])
        lind = 2
        for i in range(1, num_fcs+1):
            # sanity check
            assert int(lines[lind]) == i, (int(lines[lind]), i)

            # read cell poses
            cell_pos2 = np.array([float(fld) for fld in lines[lind+1].split()])
            cell_pos3 = np.array([float(fld) for fld in lines[lind+2].split()])

            # read basis indices
            i, j, k = (int(fld) for fld in lines[lind+3].split())

            # read fc
            fc3_ijk = np.zeros((3, 3, 3))
            for n in range(27):
                x, y, z = [int(fld) - 1 for fld in lines[lind+4+n].split()[:3]]
                fc3_ijk[x, y, z] = float(lines[lind+4+n].split()[-1])

            # append entry
            entry = [i, j, k, cell_pos2, cell_pos3, fc3_ijk]
            fc3_data_shengBTE.append(entry)
            lind += lines_per_fc_block

    return fc3_data_shengBTE


def write_shengBTE_fc3(filename, fcs, prim):
    """Write third order force constants file in shengBTE format.

    Parameters
    -----------
    filename: str
        input file name
    fcs : ForceConstants
        forceconstants must contain atoms object, and it must be a repeated
        from the atoms_prim
    prim: ASE Atoms object
        primitive configuration (equivalent to ``POSCAR`` file used in the
        shengBTE calculation)
    """

    fc3_data_shengBTE = _fcs_to_shengBTE_data(fcs, prim)

    with open(filename, 'w') as f:
        f.write('{}\n\n'.format(len(fc3_data_shengBTE)))

        for index, fc3_row in enumerate(fc3_data_shengBTE, start=1):
            i, j, k, cell_pos2, cell_pos3, fc3_ijk = fc3_row

            f.write('{:5d}\n'.format(index))

            f.write((3*'{:14.10f}'+'\n').format(*cell_pos2))
            f.write((3*'{:14.10f}'+'\n').format(*cell_pos3))
            f.write((3*'{:5d}'+'\n').format(i, j, k))

            for x, y, z in product(range(3), repeat=3):
                f.write((3*' {:}').format(x+1, y+1, z+1))
                f.write('    {:14.10f}\n'.format(fc3_ijk[x, y, z]))
            f.write('\n')


def _fcs_to_shengBTE_data(fcs, prim, cutoff=np.inf):
    """ Produces a list containing fcs in shengBTE format """

    atoms = fcs.atoms
    indices, offsets = [], []
    for atom in atoms:
        spos = np.linalg.solve(prim.cell.T, atom.position)
        for index, spos_prim in enumerate(prim.get_scaled_positions()):
            offset = spos - spos_prim
            rounded_offset = np.round(offset)
            if not np.allclose(rounded_offset, offset, rtol=0, atol=1e-3):
                continue
            rounded_offset = rounded_offset.astype(np.int64)
            assert np.allclose(rounded_offset, offset)
            indices.append(index)
            offsets.append(rounded_offset)
            break
        else:
            raise ValueError('prim not compatible with supercell')
    indices, offsets = np.array(indices), np.array(offsets)

    mic = np.zeros((len(atoms), len(atoms)), dtype=bool)
    for a0 in atoms:
        for a1 in atoms:
            dv = a1.position - a0.position
            tmp = find_mic([dv], atoms.cell)
            dv_mic, dr_mic = tmp[0][0], tmp[1][0]
            mic[a0.index, a1.index] = np.allclose(
                dv, dv_mic) and (dr_mic < cutoff)

    data = {}
    n_atoms = len(atoms)
    for i in range(n_atoms):
        for j in range(n_atoms):
            if not mic[i, j]:
                continue
            for k in range(n_atoms):
                if not (mic[i, k] and mic[j, k]):
                    continue

                i0 = indices[i]
                i1 = indices[j]
                i2 = indices[k]
                o0 = offsets[i]
                o1 = offsets[j] - o0
                o2 = offsets[k] - o0

                key = (i0, i1, i2) + tuple(o1) + tuple(o2)

                if key in data:
                    continue

                data[key] = fcs[i, j, k]

    new_data = []
    for k, fc in data.items():
        if np.linalg.norm(fc) < 1e-8:
            continue
        entry = [k[0] + 1, k[1] + 1, k[2] + 1]
        cell_pos1 = np.dot(k[3:6], prim.cell)
        cell_pos2 = np.dot(k[6:9], prim.cell)
        entry.extend([cell_pos1, cell_pos2])
        entry.append(fc)
        new_data.append(entry)

    return new_data
