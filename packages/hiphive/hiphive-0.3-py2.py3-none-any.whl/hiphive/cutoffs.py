import pickle
import numpy as np
from ase.neighborlist import NeighborList


# TODO: Use another base class to hide internals from user
class Cutoffs:
    """ This class maintains information about the cutoff configuration,
    i.e. which clusters will be included (="inside cutoff"). It also
    encapsulates functionality that is used e.g., during cluster space
    construction.

    Here, `n-body` refers to number of atoms in a cluster. For example
    the cluster (0011) is a two-body cluster of fourth order and the
    cluster (123) is a three-body cluster of third order.

    Parameters
    ----------
    cutoff_matrix : numpy.ndarray
        the matrix element `ij` provides to the cutoff for order `i+2`
        and nbody `j+2`; elements with `j>i` will be ignored
    """

    def __init__(self, cutoff_matrix):

        self._cutoff_matrix = np.array(cutoff_matrix)

        for i in range(len(self._cutoff_matrix) - 1):
            assert max(self._cutoff_matrix[i, :]) >= \
                   max(self._cutoff_matrix[i+1, :]),\
                   'Make sure cutoffs are in decreasing order'

    @property
    def cutoff_matrix(self):
        """ numpy.ndarray : copy of cutoff matrix """
        return self._cutoff_matrix.copy()

    @property
    def orders(self):
        """ list(int) : allowed orders """
        return list(range(2, self.max_order + 1))

    @property
    def nbodies(self):
        """ list(int) : allowed bodies """
        return list(range(2, self.max_nbody + 1))

    def get_cutoff(self, order, nbody):
        """
        Returns cutoff for a given body and order.

        Parameters
        ----------
        order : int
        nbody : int

        Raises
        ------
        ValueError
            if order is not in orders
        ValueError
            if nbody is not in nbodies
        ValueError
            if nbody is larger than order

        Returns
        -------
        float
        """
        if order not in self.orders:
            raise ValueError('order not in orders')
        if nbody not in self.nbodies:
            raise ValueError('nbody not in nbodies')
        if nbody > order:
            raise ValueError('nbody can not be larger than order')
        return self._cutoff_matrix[nbody - 2, order - 2]

    @property
    def max_cutoff(self):
        """ float : maximum cutoff """
        max_cutoff = 0
        for i, row in enumerate(self._cutoff_matrix):
            max_cutoff = max(max_cutoff, np.max(row[i:]))
        return max_cutoff

    @property
    def max_nbody(self):
        """ int : maximum body """
        return self._cutoff_matrix.shape[0] + 1

    @property
    def max_order(self):
        """ int : maximum order """
        return self._cutoff_matrix.shape[1] + 1

    def max_nbody_cutoff(self, nbody):
        """ Return maximum cutoff for a given body. """
        if nbody not in self.nbodies:
            raise ValueError('nbody not in nbodies')
        return np.max(self._cutoff_matrix[nbody - 2, max(0, nbody - 2):])

    def max_nbody_order(self, nbody):
        """ Returns maximum order for a given body """
        if nbody not in self.nbodies:
            raise ValueError('nbody not in nbodies')
        arr = self._cutoff_matrix[nbody - 2, max(0, nbody - 2):]
        return np.count_nonzero(arr) + (nbody - 1)

    def write(self, fileobj):
        """ Writes instance to file.

        Parameters
        ----------
        fileobj : file-like object
            file-like object to which the cutoffs will be written to
        """
        pickle.dump(self._cutoff_matrix, fileobj)

    def read(fileobj):
        """ Reads an instance from file.

        Parameters
        ----------
        fileobj : file-like object
            input file to read from
        """
        data = pickle.load(fileobj)
        if type(data) is np.ndarray:
            return Cutoffs(data)
        else:
            cutoffs = data['cutoffs']
            return CutoffMaximumBody(cutoffs, len(cutoffs) + 1)

    def __str__(self):
        return str(self._cutoff_matrix)


class CutoffMaximumBody(Cutoffs):
    """ Specify cutoff-list plus maximum body

    Usefull when creating e.g. 6th order expansions but with only 3-body
    interactions.

    Parameters
    ----------
    cutoff_list : list
        list of cutoffs for order 2, 3, etc. Must be in decresing order
    max_nbody : int
        No clusters containing more than max_nbody atoms will be generated
    """

    def __init__(self, cutoff_list, max_nbody):
        cutoff_matrix = np.zeros((max_nbody - 1, len(cutoff_list)))
        for order, cutoff in enumerate(cutoff_list, start=2):
            cutoff_matrix[:, order - 2] = cutoff
        super().__init__(cutoff_matrix)


def is_cutoff_allowed(atoms, cutoff):
    """ Checks if atoms is compatible with cutoff

    Parameters
    ----------
    atoms : ase.Atoms
        structure used for checking compatibility with cutoff
    cutoff : float
        cutoff to be tested

    Returns
    -------
    bool
        True if cutoff compatible with atoms object, else False
    """
    nbrlist = NeighborList(cutoffs=[cutoff / 2] * len(atoms), skin=0,
                           self_interaction=False, bothways=True)
    nbrlist.update(atoms)

    for i in range(len(atoms)):
        neighbors, _ = nbrlist.get_neighbors(i)
        if i in neighbors:
            return False
        if len(neighbors) != len(set(neighbors)):
            return False
    return True


def estimate_maximum_cutoff(atoms, max_iter=11):
    """ Estimates the maximum possible cutoff given the atoms object

    Parameters
    ----------
    atoms : ase.Atoms
        structure used for checking compatibility with cutoff
    max_iter : int
        number of iterations in binary search
    """

    # First upper boundary of cutoff
    upper_cutoff = min(np.linalg.norm(atoms.cell, axis=1))

    # generate all possible offsets given upper_cutoff
    nbrlist = NeighborList(cutoffs=[upper_cutoff / 2] * len(atoms), skin=0,
                           self_interaction=False, bothways=True)
    nbrlist.update(atoms)
    all_offsets = []
    for i in range(len(atoms)):
        _, offsets = nbrlist.get_neighbors(i)
        all_offsets.extend([tuple(offset) for offset in offsets])

    # find lower boundary and new upper boundary
    unique_offsets = set(all_offsets)
    unique_offsets.discard((0, 0, 0))
    upper = min(np.linalg.norm(np.dot(offset, atoms.cell))
                for offset in unique_offsets)
    lower = upper / 2.0

    # run binary search between the upper and lower bounds
    for _ in range(max_iter):
        cutoff = (upper + lower) / 2
        if is_cutoff_allowed(atoms, cutoff):
            lower = cutoff
        else:
            upper = cutoff
    return lower
