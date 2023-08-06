#!/usr/bin/python3

"""
This script is a command line tool for running a single time-propagation
simulation.
"""

import time, os
import logging
from configparser import ConfigParser
from collections import OrderedDict

from fiend.utils.misc import set_logging, fiend_setup
from fiend.propagation.propagation_utils import *
from fiend.propagation.observables import *

import numpy as np
from mpi4py import MPI
from petsc4py import PETSc

# Make sure the h5py is compatiable with MPI
import h5py
num_mpi_processes = MPI.COMM_WORLD.Get_size()
if num_mpi_processes > 1 and not h5py.get_config().mpi:
    print("Your h5py is not compatible with MPI")
    exit(1)

from fiend.propagation.propagators import *
from fiend.utils.misc import set_logging

# Check that we are working with complex version of PETSc
is_petsc_real = isinstance(PETSc.ScalarType(), np.floating)
if is_petsc_real:
    raise RuntimeError( ("You have loaded PETSc compiled for "
                         "real numbers, please use complex "
                         "PETSc instead.") )

# Setup FIEND
# -----------

master, rank, comm = fiend_setup()

set_logging(master, rank, False, True)


# Setup command line argument parser
# ----------------------------------

import argparse

parser = argparse.ArgumentParser(
    description=("Solves time-dependent Schrödinger equation for the nanotip",
                 " geometry."),
                                 argument_default=argparse.SUPPRESS)

parser.add_argument("--initial_state", type=int, default=0)
parser.add_argument("--delta_t", type=float, default=0.1)
parser.add_argument("--extra_time", type=float, default=0.0)

parser.add_argument("--matexp_tolerance", type=float,
                    default=np.finfo(float).eps)
parser.add_argument("--hamiltonian_tolerance", type=float,
                    default=np.finfo(float).eps)
parser.add_argument("--observables", nargs='+', type=str, default='')
parser.add_argument("--save_interval", type=float, default=1)
parser.add_argument("--debug", action='store_true', default=False)
parser.add_argument("--debug_master", action='store_true', default=False)
parser.add_argument("--propagator", type=str, default='petsc_cn')
parser.add_argument("--solver_type", type=str, default='superlu_dist')
parser.add_argument("--vecpot", type=str, default='laser')
args = vars(parser.parse_args())

set_logging(master, rank, args['debug'], args['debug_master']) 


# Load the initial state and system matrices

psi, S, S0, S1, H0, P_rho, P_z, Rho, Z, ACC, NMAT = load_representation( args['initial_state'] )
# Setup laser-electron interaction manually here
# for plasmonic fields
# ----------------------------------------------

vecpot, efield, Tmax = get_vector_potential( args['vecpot'] )

laserfield = vecpot

# Load the interaction matrices
Ap = -1j * petsc_matload( 'data/tdse_Ap_cplx', comm)
Asqr = petsc_matload( 'data/tdse_Asqr_cplx', comm)

# Function for explicitely constructing H(t)
# Needed by the propagator since our interaction operator is slightly different 
# than usual
def RHSjac(ts, t, u, Amat, Pmat):
    H0.copy(Amat)
    Amat.axpy(-laserfield(t), Ap)
    Amat.axpy(laserfield(t)*laserfield(t), Asqr)


# Setup observables
args['max_t'] = Tmax + args['extra_time']

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

h5file, datasets = prepare_savefile( simple_observables, 
                                     'velocity', 
                                     laserfield,
                                     Tmax, 
                                     args['delta_t'] 
                                   )
 
post_step_handler = lambda ts: compute_and_save_observables(
                                            ts,
                                            simple_observables,
                                            complex_observables,
                                            h5file,
                                            datasets,
                                            args['save_interval']
                                            )

propagator = setup_propagator( S1, H0, None, laserfield, 
                              post_step_handler = post_step_handler,
                              RHSjac = RHSjac,
#                              boundary_metric=(NMAT, 1),
                               **args)

propagator.propagate(psi)

# Save final state
save_wavefunction(psi, -1)
os.makedirs("data/tdse_wavefunction", exist_ok = True)
petsc_save("data/tdse_wavefunction/state_final_cplx", psi, comm)

h5file.close()
