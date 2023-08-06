#!/usr/bin/python3

"""
This script is a command line tool for solving time-independent Schrödinger
equation.
"""

import time
import os
import logging
import sys

from configparser import ConfigParser
from collections import OrderedDict

import numpy as np
from mpi4py import MPI

import dolfin as df

from fiend.utils.mesh import mesh_of_sphere_in_cylindrical_coordinates,\
    save_mesh
from fiend.utils.misc import parse_functionspace_argument, \
    set_logging, fiend_setup
from fiend.utils.predefined_potentials import atom_potential_times_rho_expr
from fiend.utils.dolfin import wfnorm
from fiend.tise.tise import solve_tise


def tirun(**kwargs):
    """
    Solves time-independent Schrödinger equation according to the keyword
    arguments provided.

    Keyword arguments
    -----------------
    atom_type : str
        Name of the single-electron potential we are using (see
        fiend.utils.atom_potential_times_rho_expr)

    radius : float
        Radius of the simulated domain. Dirichlet boundary conditions will be
        set at this distance from the origin.
    core_radius : float
        What region is to be considered 'atomic core', i.e., where the mesh is
        denser
    refinement_radius : float
        Up to which distance from the origin should we refine the mesh
    cellradius : float
        Maximum radius of a circle enclosing a mesh element far away from the
        origin
    core_cellradius : float
        Maximum radius of a circle enclosing a mesh element near the origin

    num_states : int
        Number of states we wish to solve (we always solve the states lowest in
        energy)
    eigensolver_tol : float
        Relative tolerance of the eigenvalues
    eigensolver_max_iterations : int
        Maximum number of iterations we allow the eigensolver to take
    eigensolver_type : str
        Which SLEPc eigensolver to use ('lapack', 'krylov-schur', ...)

    functionspace : (str, int)
        First element sets the basis functions to use and second their degree
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    master = rank == 0

    logging.info('Meshing')
    mesh = mesh_of_sphere_in_cylindrical_coordinates(
        kwargs['radius'],
        kwargs['core_radius'],
        kwargs['refinement_radius'],
        kwargs['cellradius'],
        kwargs['core_cellradius']
    )

    potential_expr = atom_potential_times_rho_expr(kwargs['atom_type'], mesh)

    logging.info('Computing stationary states')

    evals, evecs = solve_tise(
        mesh, kwargs['num_states'], potential_expr, **kwargs)

    logging.info("Eigenvalues: " + str(evals))

    # Save to file
    os.makedirs("data/", exist_ok=True)
    np.savetxt('data/tise_eigenvalues', evals)

    save_mesh('data/tise_mesh.h5', mesh)

    with df.HDF5File(comm, 'data/tise_states.h5', 'w') as savefile:
        for i in range(len(evecs)):
            savefile.write(evecs[i], "state_%d" % i)

    # Write parameters
    config = ConfigParser()
    secname = 'TISE parameters'
    config.add_section(secname)
    for key, val in sorted(kwargs.items()):
        config.set(secname, key, str(val))

    with open("data/config", 'w') as f:
        config.write(f)

    logging.info('Exiting...')


def tirun_main():
    """
    A standalone function that reads command line arguments and solves TISE
    accordingly.
    """
    master, rank, comm = fiend_setup()

    import argparse

    parser = argparse.ArgumentParser(
        description="Solves time-independent Schrödinger equation",
        argument_default=argparse.SUPPRESS)

    parser.add_argument("--radius", "-R", type=float, default=30.0,
                        help=("Radius of the simulated domain. Dirichlet "
                              "boundary conditions will be set at this "
                              "distance from the origin.")
                        )
    parser.add_argument("--core_radius", type=float, default=3.0,
                        help=("What region is to be considered as the 'atomic "
                              "core', i.e., where the mesh is denser.")
                        )
    parser.add_argument("--refinement_radius", type=float, default=10.0,
                        help=("Up to which distance from the origin should "
                              "we refine the mesh")
                        )
    parser.add_argument("--cellradius", type=float, default=1.0,
                        help=("Maximum radius of a circle enclosing a mesh "
                              "element far away from the origin")
                        )
    parser.add_argument("--core_cellradius", type=float, default=0.1,
                        help=("Maximum radius of a circle enclosing "
                              "a mesh element near the origin.")
                        )
    parser.add_argument("--atom_type", type=str, default='H',
                        help=("Type of the atom we wish to simulate "
                              "(sets the single-electron potential).")
                        )
    parser.add_argument("--num_states", type=int, default=1,
                        help="Number of eigenstates to solve.")
    parser.add_argument("--eigensolver_tol", type=float, default=1e-6,
                        help="Relative tolerance of the solved eigenenergies."
                        )
    parser.add_argument("--eigensolver_max_iterations", type=int,
                        default=1000000,
                        help=("Maximum number of iterations allowed for the "
                              "eigensolver")
                        )
    parser.add_argument("--eigensolver_type", type=str, default='krylov',
                        help=("Which eigensolver to use (krylov, lapack, arpack, "
                              "...)")
                        )

    parser.add_argument("--functionspace", type=str, default=('Lagrange,1'),
                        help=("Functionspace to use for TDSE. Should be "
                              "a pair separated by a comma. The first "
                              "argument sets the basis function type "
                              "and the second the maximum degree of the "
                              "basis functions.")
                        )

    parser.add_argument("--debug", action='store_true', default=False,
                        help="Debug information from all MPI processes"
                        )
    parser.add_argument("--debug_master", action='store_true', default=False,
                        help="Debug information from the rank 0 MPI process"
                        )
    parser.add_argument("--quadrature_degree", type=int)

    args = vars(parser.parse_args())
    if 'quadrature_degree' in args:
        df.parameters['form_compiler']['quadrature_degree'] = args['quadrature_degree']

    # Parse the functionspace argument
    args['functionspace'] = parse_functionspace_argument(args['functionspace'])

    set_logging(master, rank, args['debug'], args['debug_master'])

    tirun(**args)


if __name__ == '__main__':
    tirun_main()
