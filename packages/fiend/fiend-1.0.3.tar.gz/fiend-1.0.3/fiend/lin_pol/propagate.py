#!/usr/bin/python3

from fiend.propagation.propagators import *
"""
This script is a command line tool for running a single time-propagation
simulation.
"""
import time
import os
import logging
from configparser import ConfigParser
from collections import OrderedDict

import numpy as np
from mpi4py import MPI
from petsc4py import PETSc
from fiend.utils.misc import set_logging
from fiend.propagation.propagation_utils import *
from fiend.propagation.observables import *

# Make sure the h5py is compatiable with MPI
import h5py
num_mpi_processes = MPI.COMM_WORLD.Get_size()
if num_mpi_processes > 1 and not h5py.get_config().mpi:
    print("Your h5py is not compatible with MPI")
    exit(1)


def fiend_propagate_main():

    # Check that we are working with complex version of PETSc
    is_petsc_real = isinstance(PETSc.ScalarType(), np.floating)
    if is_petsc_real:
        raise RuntimeError(("You have loaded PETSc compiled for "
                            "real numbers, please use complex "
                            "PETSc instead."))

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    master = rank == 0

    import argparse

    parser = argparse.ArgumentParser(
        description="Solves time-independent Schrödinger equation",
        argument_default=argparse.SUPPRESS)

    parser.add_argument("--initial_state", type=int, default=0)
    parser.add_argument("--delta_t", type=float, default=0.1)
    parser.add_argument("--vecpot", type=str, default='./laser')  # If a
    # configfile, parse Laser from there, else interpolate
    parser.add_argument("--extra_time", type=float, default=0.0)

    parser.add_argument("--matexp_tolerance", type=float,
                        default=10 * np.finfo(float).eps)
    parser.add_argument("--inverse_tolerance", type=float,
                        default=10 * np.finfo(float).eps)
    parser.add_argument("--ilu_factor_levels", type=int, default=1)
    parser.add_argument("--observables", nargs='+', type=str, default='')
    parser.add_argument("--save_interval", type=float, default=1)
    parser.add_argument("--gauge", type=str, default='velocity')
    parser.add_argument("--debug", action='store_true', default=False)
    parser.add_argument("--debug_master", action='store_true', default=False)
    parser.add_argument("--propagator", type=str, default='krylov')
    parser.add_argument("--solver_type", type=str, default='krylov')
    args = vars(parser.parse_args())

    set_logging(master, rank, args['debug'], args['debug_master'])

    if logging.getLogger('').isEnabledFor(logging.DEBUG):
        PETSc.Log().begin()

    psi, S, S0, S1, H0, _, P_z, _, Z, ACC = load_representation(
        args['initial_state'])

    vecpot, efield, Tmax = get_vector_potential(args['vecpot'])
    args['max_t'] = Tmax + args['extra_time']
    W, laserfield = setup_interaction(efield, vecpot,
                                      Z, P_z, args['gauge'])

    simple_observables, complex_observables = prepare_observables(
        args['observables'],
        S,
        S0,
        S1,
        H0,
        Z,
        P_z,
        ACC
    )

    h5file, datasets = prepare_savefile(simple_observables,
                                        args['gauge'],
                                        laserfield,
                                        Tmax,
                                        args['delta_t']
                                        )

    def poststep_function(ts): return compute_and_save_observables(
        ts,
        simple_observables,
        complex_observables,
        h5file,
        datasets,
        args['save_interval']
    )

    propagator = setup_propagator(S, H0, W, laserfield,
                                  **args)
    propagator.set_post_step_handler(poststep_function)
    propagator.propagate(psi)

    # Save final state
    save_wavefunction(psi, "final")
    os.makedirs("data/tdse_wavefunction", exist_ok=True)
    petsc_save("data/tdse_wavefunction/state_final_cplx", psi, comm)
    h5file.close()

    if logging.getLogger('').isEnabledFor(logging.DEBUG):
        PETSc.Log().view(PETSc.Viewer().STDOUT())


if __name__ == '__main__':
    fiend_propagate_main()
