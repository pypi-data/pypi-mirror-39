"""
Small helper functions
"""

import logging
import re
from typing import Tuple, Union, Text, List

import numpy as np

from petsc4py import PETSc
from mpi4py import MPI
try:
    import dolfin as df
except BaseException:
    ...


def fiend_setup(quadrature_degree: int = 6) -> Tuple[bool, int, MPI.Comm]:
    """
    Sets up default form compiler parameters,
    dolfin logging level, and quadrature degree of assembly.

    Parameters
    ----------
    quadrature_degree : int
        Degree of the assembly quadrature

    Returns
    -------
    master : bool
        True if current process is rank == 0
    rank : int
        Rank of current MPI process
    comm : mpi communicator
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    master = rank == 0
    try:
        df.set_log_level(df.LogLevel.ERROR)
        df.parameters['form_compiler']['optimize'] = True
        df.parameters['form_compiler']['cpp_optimize'] = True
        df.parameters['form_compiler']['cpp_optimize_flags'] = '-O3 -march=native'

        df.parameters['form_compiler']['quadrature_degree'] = quadrature_degree
        ffc_logger = logging.getLogger('FFC')
        ffc_logger.setLevel(logging.WARNING)

        ufl_logger = logging.getLogger('UFL')
        ufl_logger.setLevel(logging.WARNING)
    except BaseException:
        pass

    return master, rank, comm


def set_logging(master: bool,
                rank: int,
                debug: bool,
                debug_master: bool) -> None:
    """
    Initializes fiend's logging.

    Parameters
    ----------
    master : bool
        True if current MPI process' rank is zero, false otherwise
    rank : int
        Rank of the current MPI process
    debug : bool
        True if all processes should output debug information
    debug_master : bool
        True if master should output debug information
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG,
                            format='Rank ' + str(rank) + ' %(message)s')
    else:
        if master:
            if debug_master:
                logging.basicConfig(level=logging.DEBUG, format='%(message)s')
            else:
                logging.basicConfig(level=logging.INFO, format='%(message)s')
        else:
            logging.basicConfig(level=logging.WARNING,
                                format='Rank ' + str(rank) + ' %(message)s')


def parse_functionspace_argument(string: Text) -> Tuple[str, int]:
    """
    Parses the name and degree of basis functions

    Parameters
    ----------
    string

    Returns
    -------
    str : name
    int : degree

    Raises
    ------
    RuntimeError
        If parsing failed.
    """
    p = re.match(
        r"(\[|\(|\{)?'?(?P<element>\w*)'?(,|.|;|:)\s?'?(?P<degree>\d*)'?(\]|\)|\}?)'?",
        string)
    if not p:
        raise RuntimeError("Could not parse the functionspace from: " + string)

    name = p.group('element').lower()
    if name != 'lagrange' and name != 'cg':
        logging.warning(("Not using Lagrange finite elements! "
                         "Results will probably be bogus."))
    try:
        return p.group('element'), int(p.group('degree'))
    except BaseException:
        raise RuntimeError("Could not parse functionspace argument")


def triangle_incenter(coords: Union[List[List[float]], np.array]) -> Tuple[float,
                                                                           float]:
    """
    Given three vertices of a triangle, returns the incenter
    """
    xa, ya = coords[0]
    xb, yb = coords[1]
    xc, yc = coords[2]

    ab = np.hypot(xb - xa, yb - ya)
    bc = np.hypot(xc - xb, yc - yb)
    ac = np.hypot(xc - xa, yc - ya)

    xi = (bc * xa + ac * xb + ab * xc) / (ab + bc + ac)
    yi = (bc * ya + ac * yb + ab * yc) / (ab + bc + ac)

    return xi, yi
