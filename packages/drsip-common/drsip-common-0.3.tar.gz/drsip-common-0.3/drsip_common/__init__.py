"""
========================================================
Common Functions (:mod:`drsip_common`)
========================================================

Module contains functions that are used by two or more functions from
different modules.

Functions
---------

.. autofunction:: get_best_fit_rot_mat
"""
import cStringIO
from Bio.SVDSuperimposer import SVDSuperimposer

superimpose_inst = SVDSuperimposer()


def get_best_fit_rot_mat(from_coord, to_coord):
    """
    Compute best-fit rotation matrix.

    The best-fit rotation matrix rotates from_coord such that the RMSD
    between the 2 sets of coordinates are minimized after the rotation.

    Parameters
    ----------
    from_coord, to_coord : np.array
        Nx3 coordinate arrays, where N is the number of atoms. The
        from_coord will rotated such that the rotation will minimize
        the RMSD between the rotated from_coord and to_coord.

    Returns
    -------
    np.array
        3x3 rotation matrix
    """
    superimpose_inst.set(to_coord.astype('float64'),
                         from_coord.astype('float64'))
    superimpose_inst.run()

    return superimpose_inst.get_rotran()[0].T

def convert_file_to_StrIO(filename):

    with open(filename, 'r') as file_obj:
        file_lines = file_obj.readlines()

    output = cStringIO.StringIO()
    output.writelines(file_lines)
    output.seek(0)

    return output

def convert_str_to_StrIO(str_input):
    output = cStringIO.StringIO()
    output.write(str_input)
    output.seek(0)

    return output

def convert_file_to_str(filename):

    with open(filename, 'r') as file_obj:
        file_lines = file_obj.readlines()

    return ''.join(file_lines)

def convert_StrIO_to_str(str_io):
    str_io.seek(0)

    return ''.join(str_io.readlines())