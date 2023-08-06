"""
AAA
"""
import logging
from typing import Callable, Text, Tuple

from mpi4py import MPI
import numpy as np

from scipy.interpolate import Akima1DInterpolator
from petsc4py import PETSc

from fiend.utils.petsc_utils import *
from fiend.pulseconfig_parser.parser import parse_laser
from fiend.propagation.propagators import *


def get_vector_potential(vecpotfile: Text) -> Tuple[Callable, Callable, float]:
    # Load the laser vector potential
    try:
        vecpot = np.loadtxt(vecpotfile)

        T0 = vecpot[:, 0].min()

        Tmax = vecpot[:, 0].max()

        # Time to [0, Tmax-T0]
        Tmax = Tmax - T0
        vecpotinterp = Akima1DInterpolator(vecpot[:, 0] - T0, vecpot[:, 1])

        def vecpot(t): return vecpotinterp(t) if t <= Tmax else 0.0

        def efield(t): return vecpotinterp(t, nu=1) if t <= Tmax else 0.0

    except Exception as e:
        try:
            laser_vecpot = parse_laser(vecpotfile)
            T0 = laser_vecpot.beginning_of_pulse()
            Tmax = laser_vecpot.end_of_pulse()

            def vecpot(t): return laser_vecpot(t + T0)

            def efield(t): return laser_vecpot.electric_field(t + T0)

            Tmax = Tmax - T0
        except Exception as e:
            logging.error(("Could not parse the laser field: "
                           "%s.\nExiting." % e))
            exit(1)
    return vecpot, efield, Tmax


def load_representation(initial_state_nbr: int) -> Tuple[
    PETSc.Vec,
    PETSc.Mat,
    PETSc.Mat,
    PETSc.Mat,
    PETSc.Mat,
    PETSc.Mat,
    PETSc.Mat,
    PETSc.Mat,
    PETSc.Mat,
    PETSc.Mat,
]:
    """
    Loads the initial state and matrices.

    Parameters
    ----------
    initial_state_nbr : int
        Number of the initial state (selected from the stationary states)

    Returns
    -------
    psi : petsc4py.PETSc.Vec
    S : petsc4py.PETSc.Mat
    H0 : petsc4py.PETSc.Mat
    P_z : petsc4py.PETSc.Mat
    Z : petsc4py.PETSc.Mat
    ACC : petsc4py.PETSc.Mat
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    master = rank == 0

    # Load initial state
    psi = petsc_vecload('data/tdse_state_%d_cplx' % initial_state_nbr, comm)
    psi.name = 'WAVEFUNCTION'

    H0 = petsc_matload('data/tdse_H0_cplx', comm)

    S0 = petsc_matload('data/tdse_S0_cplx', comm)
    S0.name = 'OVERLAP (boundary rows zero)'

    S1 = petsc_matload('data/tdse_S1_cplx', comm)
    S1.name = 'OVERLAP (boundary rows 1-diagonal)'

    S = petsc_matload('data/tdse_S_cplx', comm)
    S.name = 'OVERLAP'

    P_rho = petsc_matload('data/tdse_partialRho_cplx', comm)
    P_rho *= -1.0j
    P_rho.name = 'MOMENTUM_RHO'

    P_z = petsc_matload('data/tdse_partialZ_cplx', comm)
    P_z *= -1.0j
    P_z.name = 'MOMENTUM_Z'

    Rho = petsc_matload('data/tdse_Rho_cplx', comm)
    Rho.name = 'RHO-DIPOLE'
    Rho.setOption(PETSc.Mat.Option.SYMMETRIC, True)
    Rho.setOption(PETSc.Mat.Option.HERMITIAN, True)

    Z = petsc_matload('data/tdse_Z_cplx', comm)
    Z.setOption(PETSc.Mat.Option.HERMITIAN, True)
    Z.setOption(PETSc.Mat.Option.SYMMETRIC, True)
    Z.name = 'Z-DIPOLE'

    # TODO: Handle ABS/CAP here. They need some processing
    # before ready to use

    ABS = petsc_matload('data/tdse_ABS_cplx', comm)
    ABS.name = 'ABSORBER'

    ACC = petsc_matload('data/tdse_ACC_cplx', comm)
    ACC.name = 'Z-ACCELERATION'

    H0.axpy(-1.0j, ABS, structure=PETSc.Mat.Structure.SUBSET)
    #H0.setOption(PETSc.Mat.Option.SYMMETRIC, True)
    H0.name = 'TI HAMILTONIAN + ABSORBER'

    N = petsc_matload('data/tdse_NMAT_cplx', comm)
    N.name = 'NEUMANN MATRIX'

    return psi, S, S0, S1, H0, P_rho, P_z, Rho, Z, ACC, N


def setup_interaction(efield, vecpot, Z, P_z, gauge):
    """
    Select the interaction matrices based on the gauge

    Parameters
    ----------
    efield : callable
    vecpot : callable
    Z : petsc4py.PETSc.Mat
    P_z : petsc4py.PETSc.Mat
    gauge : str
        'length' or 'velocity'

    Returns
    -------
    petsc4py.PETSc.Mat
        The laser-electron interaction matrix
    callable
        THe callable giving the strength of the interaction at time t
    """
    if gauge == 'length':
        W = Z
        laserfield = efield
    elif gauge == 'velocity':
        W = P_z
        laserfield = vecpot
    else:
        raise ValueError('No such gauge: ' + args['gauge'])
    return W, laserfield


def setup_propagator(S: PETSc.Mat,
                     H0: PETSc.Mat,
                     W: PETSc.Mat,
                     laserfield: Callable,
                     pre_step_handler: Callable = None,
                     post_step_handler: Callable = None,
                     **kwargs
                     ):
    if kwargs['propagator'].startswith('petsc_'):
        propagator = PETScPropagator(S, H0, W, laserfield,
                                     propagatortype=kwargs['propagator'][6:],
                                     **kwargs)
    else:
        raise ValueError("Unknown propagator: " + kwargs['propagator'])

    if pre_step_handler:
        propagator.set_pre_step_handler(pre_step_handler)
    if post_step_handler:
        propagator.set_post_step_handler(post_step_handler)

    return propagator
