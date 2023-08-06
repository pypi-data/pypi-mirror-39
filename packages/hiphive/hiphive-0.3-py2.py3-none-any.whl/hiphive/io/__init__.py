def read_force_constants(filename, format=None):
    """
    Reads force constants from file. Several different file formats
    are supported including `phonopy`, `phono3py`, and `shengBTE`.

    Parameters
    ----------
    filename : str
        name of input file
    format : str
        format of input file

        possible values:
        ``phonopy``, ``phonopy-text``, ``phonopy-hdf5``, ``phono3py``,
        ``shengbte``

        In the case of ``phonopy`` hiphive will attempt to infer the file
        format (hdf5 or text) from the file name.

    Returns
    -------
    numpy.ndarray
        second (`phonopy`) or third-order (`phono3py`, `shengBTE`)
        force constant matrix

    Raises
    ------
    ValueError
        if file format cannot be recognized
    """
    from .phonopy import read_phonopy_fc2, read_phonopy_fc3
    from .shengBTE import read_shengBTE_fc3

    if format == 'phonopy':
        return read_phonopy_fc2(filename)
    elif format == 'phonopy-text':
        return read_phonopy_fc2(filename, format='text')
    elif format == 'phonopy-hdf5':
        return read_phonopy_fc2(filename, format='hdf5')
    elif format == 'phono3py':
        return read_phonopy_fc3(filename)
    elif format == 'shengbte':
        return read_shengBTE_fc3(filename)
    else:
        raise ValueError('Unrecognized file format: {}'.format(format))


def write_force_constants(filename, fc, format=None):
    """
    Writes force constants to file.

    Parameters
    ----------
    filename : str
        name of output file
    fc : ForceConstants or numpy.ndarray
        force constant matrix
    format : str
        format of output file

        possible values:
        ``phonopy``, ``phonopy-text``, ``phonopy-hdf5``, ``phono3py``,
        ``shengbte``

        In the case of `phonopy` hiphive will attempt to infer the file
        format (hdf5 or text) from the file name.

    Raises
    ------
    ValueError
        if file format cannot be recognized
    """
    from .phonopy import write_phonopy_fc2, write_phonopy_fc3
    from .shengBTE import write_shengBTE_fc3

    if format == 'phonopy':
        write_phonopy_fc2(filename, fc)
    elif format == 'phonopy-text':
        write_phonopy_fc2(filename, fc, format='text')
    elif format == 'phonopy-hdf5':
        write_phonopy_fc2(filename, fc, format='hdf5')
    elif format == 'phono3py':
        write_phonopy_fc3(filename, fc)
    elif format == 'shengbte':
        write_shengBTE_fc3(filename, fc)
    else:
        raise ValueError('Unrecognized file format: {}'.format(format))
