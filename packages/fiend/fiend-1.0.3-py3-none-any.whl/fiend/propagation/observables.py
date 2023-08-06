import logging
import os
from typing import *

import numpy as np
from mpi4py import MPI
from collections import OrderedDict
import h5py

from fiend.utils.petsc_utils import *


def _compute_expectation_value(state: PETSc.Vec,
                               mat: PETSc.Mat,
                               wrkvec: Optional[PETSc.Vec] = None):
    """
    Computes the expectation value <state|mat|state>

    Parameters
    ----------
    state : petsc4py.PETSc.Vec
    mat : petsc4py.PETSc.Mat
    wrkvec : petsc4py.PETSc.Vec (optional)

    Returns
    -------
    complex number
    """

    mat.mult(state, wrkvec)
    return wrkvec.dot(state)  # type: ignore


def save_wavefunction(WF: PETSc.Vec,
                      iteration: int,
                      wrkvec: Optional[PETSc.Vec] = None):
    """
    Saves the real and imaginary parts of the state to separate files

    Parameters
    ----------
    WF : petsc4py.PETSc.Vec
        The vector of expansions coefficients for the state
    iteration : int
        The number of time steps
    wrkvec : petsc4py.PETSc.Vec (optional)
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    master = rank == 0

    os.makedirs("data/tdse_wavefunction/", exist_ok=True)
    if not wrkvec:
        wrkvec = WF.duplicate()
    else:
        # Copy the state to wrkvec and extract the real part
        WF.copy(result=wrkvec)
    wf_local = wrkvec.getArray(readonly=False)
    wf_local[:] = np.real(wf_local)
    if isinstance(iteration, int):
        petsc_save("data/tdse_wavefunction/realpart_iteration_%d" % iteration, wrkvec,
                   comm)
    else:
        petsc_save("data/tdse_wavefunction/realpart_iteration_%s" % iteration, wrkvec,
                   comm)

    if master:
        if isinstance(iteration, int):
            petsc_convert_to_real(
                "data/tdse_wavefunction/realpart_iteration_%d" % iteration)
        else:
            petsc_convert_to_real(
                "data/tdse_wavefunction/realpart_iteration_%s" % iteration)

    # Copy the state to wrkvec and extract the imaginary part
    WF.copy(result=wrkvec)
    wf_local = wrkvec.getArray(readonly=False)
    wf_local[:] = np.imag(wf_local)
    if isinstance(iteration, int):
        petsc_save("data/tdse_wavefunction/imagpart_iteration_%d" % iteration, wrkvec,
                   comm)
    else:
        petsc_save("data/tdse_wavefunction/imagpart_iteration_%s" % iteration, wrkvec,
                   comm)

    if master:
        if isinstance(iteration, int):
            petsc_convert_to_real(
                "data/tdse_wavefunction/imagpart_iteration_%d" % iteration)
        else:
            petsc_convert_to_real(
                "data/tdse_wavefunction/imagpart_iteration_%s" % iteration)


def prepare_observables(observables_to_compute: List[Text],
                        S: PETSc.Mat,
                        S0: PETSc.Mat,
                        S1: PETSc.Mat,
                        H0: PETSc.Mat,
                        Z: PETSc.Mat,
                        P_z: PETSc.Mat,
                        ACC: PETSc.Mat) -> Tuple[
    Dict[str, Callable[[PETSc.Vec], float]],
                            Dict[str, Callable[[PETSc.Vec, int], None]]
]:
    """
    Prepares functions and datasets for computing observables

    Parameters
    ----------
    observables_to_compute : list of strings
    S : petsc4py.PETSc.Mat
        The overlap matrix
    H0 : petsc4py.PETSc.Mat
        Time-independent part of the Hamiltonian
    Z : petsc4py.PETSc.Mat
        <m|z|n>
    Pz : petsc4py.PETSc.Mat
        -i <m|∂_z|n>
    ACC : petsc4py.PETSc.Mat
        -<m| ∂_z Vstatic |n>

    Returns
    -------
    simple_observables : list of callables
        List of functions that computes a single value out of an observable.
        Call signature of these functions is
        f( petsc4py.PETSc.Vec,
           petsc4py.PETSc.Mat,
           petsc4py.PETSc.Vec (optional)
         )
    complex_observables : list of callables
        List of functions that compute observables that are more complex
        than a single value, e.g., the electron density. They handle saving the
        data themselves.
    """

    simple_observables = OrderedDict()
    complex_observables = OrderedDict()

    # Initialize some workspace for the functions
    wrkvec = S.getVecRight()

    # Handle simple observables
    if 'norm' in observables_to_compute:
        simple_observables['norm'] = \
            lambda WF: _compute_expectation_value(WF, S, wrkvec)

    if 'dipole_z' in observables_to_compute:
        simple_observables['dipole_z'] = \
            lambda WF: _compute_expectation_value(WF, Z, wrkvec)

    if 'momentum_z' in observables_to_compute:
        simple_observables['momentum_z'] = \
            lambda WF: _compute_expectation_value(WF, P_z, wrkvec)

    if 'acceleration_z' in observables_to_compute:
        simple_observables['acceleration_z'] = \
            lambda WF: _compute_expectation_value(WF, ACC, wrkvec)

    # Handle more complex observables
    if 'wavefunction' in observables_to_compute or 'density' in observables_to_compute:
        
        complex_observables['wavefunction'] = \
            lambda WF, iteration: save_wavefunction(WF, iteration, wrkvec)
    return simple_observables, complex_observables


def prepare_savefile(simple_observables: Dict[Text, Callable],
                     gaugename: Text, laserfield: Callable,
                     Tmax: float, dt: float):
    """
    Prepares the savefile for observables.

    Parameters
    ----------
    simple_observables : OrderedDict of callables returned by
                         _prepare_observables
    gaugename : str
        Name of the gauge, 'length' or 'velocity'
    laserfield : callable of a single argument
        Should return the electric field for length gauge and vector potential
        for velocity gauge
    Tmax : float
        Final time
    dt : float
        Time-step

    Returns
    -------
    file : h5py.File
    datasets : dictionary of h5py.Dataset for simple observables
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    master = rank == 0
    # Only master saves the observables
    savefile = h5py.File('data/tdse_observables.h5',
                         'w', driver='mpio', comm=comm)

    time = np.arange(0.0, Tmax + 3 * dt / 2, dt)
    buffer_length = len(time)

    savefile['time'] = time
    if gaugename == 'velocity':
        savefile['laser_vector_potential'] = [laserfield(t) for t in time]
    elif gaugename == 'length':
        savefile['laser_electric_field'] = [laserfield(t) for t in time]
    datasets = OrderedDict()

    for name in simple_observables:
        datasets[name] = savefile.create_dataset(name,
                                                 (buffer_length,),
                                                 dtype=float
                                                 )
    return savefile, datasets


def compute_and_save_observables(time_stepper: PETSc.TS,
                                 simple_observables: Dict[Text, Callable],
                                 complex_observables: Dict[Text, Callable],
                                 savefile: Text,
                                 datasets: Dict[Text, h5py.Dataset],
                                 save_interval: int = 1
                                 ) -> None:
    """
    Computes and saves observables. Should be given to PETSc.TS instance.

    Parameters
    ----------
    time_stepper : petsc4py.PETSc.TS
    simple_observables : OrderedDict of simple observables (callable)
    complex_observables : OrderedDict of complex observables (callable
                          that saves its own data)

    savefile : h5py.File
    datasets : dictionary of h5py.Dataset
    """
    logging.info("  t = %f" % time_stepper.getTime())
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    master = rank == 0

    stepnum = time_stepper.getStepNumber()

    if stepnum % save_interval == 0:
        saveslot = int(stepnum // save_interval)
        psi = time_stepper.getSolution()
        # Handle simple observables
        for name in sorted(simple_observables.keys()):
            obsval = simple_observables[name](psi)
            logging.debug("    %s = %.10g+%.2gi" % (name,
                                                    np.real(obsval),
                                                    np.imag(obsval)))
            if master:
                datasets[name][saveslot] = np.real(obsval)

        # Complex observables
        for name in sorted(complex_observables.keys()):
            complex_observables[name](psi, saveslot)
