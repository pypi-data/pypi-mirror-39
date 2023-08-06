"""
Methods for solving the time-independent Schrödinger equation.
"""
import logging
from typing import *

import numpy as np
import h5py
from mpi4py import MPI
from petsc4py import PETSc
from slepc4py import SLEPc
import dolfin as df

from fiend.utils.dolfin import get_boundary_markers, get_petsc_vec, wfnorm,\
        load_function_collection
from fiend.utils.mesh import load_mesh
from fiend.utils.petsc_utils import symmetrize

def solve_tise(mesh: df.Mesh,
               how_many: int = 1,
               pot_x_rho=df.Constant('0.0'),
               **kwargs) -> Tuple[np.array,
                                  np.array]:
    """
    Solves the time-independent Schrödinger equation in cylindrical coordinates
    for a single electron, and returns the eigenvalues and eigenstates of
    requested number of lowest eigenstates.

    Parameters
    ----------
    mesh : df.Mesh
        Mesh of the (ρ,z)-halfplane of cylindrical coordinates
    potential_times_rho_str : str
        String that defines potential⋅ρ. This string needs to be a valid
        C-syntax.
    how_many : int
        How many eigenpairs to solve and return

    **kwargs:
        eigensolver_tol : float
            Convergence tolerance for the eigensolver
        eigensolver_max_iterations : float
            Maximum number of iterations for the eigensolver
        eigensolver_type : str
            Which eigensolver to use
        functionspace : (str, int)
            Which functionspace to use. Name and degree
        dirichlet_boundaries : list of functions
            These functions mark the boundaries where we impose zero
            dirichlet boundary conditions, other boundaries will use
            Neumann boundary conditions
    Returns
    -------
    eigensystem : list of pairs (tuples)
        The list is ordered in increasing order of eigenvalues. First element
        of each pair (tuple) is the eigenenergy and the second element the
        eigenstate as dolfin.Function.

    """
    comm = df.MPI.comm_world

    logging.debug("Entering TISE solver")
    # Time independent problem => only real valued wavefunctions

    # Set up the function space
    funspace = kwargs.get('functionspace', ('Lagrange', 1))
    elem = df.FiniteElement(funspace[0], mesh.ufl_cell(), degree=funspace[1])
    FS = df.FunctionSpace(mesh, elem)
    zero = df.Constant('0.0')

    boundaries = get_boundary_markers(mesh, kwargs.get('dirichlet_boundaries', None))
    bc = df.DirichletBC(FS, df.Constant(0.0), boundaries, 1)

    # Weak formulation of the eigenvalue problem
    v = df.TestFunction(FS)
    phi = df.TrialFunction(FS)
    x = df.SpatialCoordinate(mesh)
    rho = x[0]
    z = x[1]

    H0_form = 0.5 * df.dot(df.grad(v), df.grad(phi)) * rho * df.dx\
        + v * phi * pot_x_rho * df.dx
    S_form = v * phi * rho * df.dx

    logging.debug("  entering eigensolver")

    # Solve the eigenpairs
    eigensolver = SLEPc.EPS().create(comm=comm)

    # Select solver (these are the ones that seem to work)
    solver_types = {
        'rqcg': SLEPc.EPS.Type.RQCG,
        'krylovschur': SLEPc.EPS.Type.KRYLOVSCHUR,
        'lapack': SLEPc.EPS.Type.LAPACK,
        'arpack': SLEPc.EPS.Type.ARPACK,
        'power' : SLEPc.EPS.Type.POWER,
        'arnoldi' : SLEPc.EPS.Type.ARNOLDI,
        'jd' : SLEPc.EPS.Type.JD,
        'subspace' : SLEPc.EPS.Type.SUBSPACE
    }
    solver_type_str = kwargs.get('eigensolver_type', 'rqcg').lower()
    solver_type = solver_types[solver_type_str]

    eigensolver.setType(solver_type)

    # Assemble the matrices
    H0 = df.PETScMatrix()
    S = df.PETScMatrix()
    _vec = df.PETScVector()
    vform = df.Constant(0.0)*v*df.dx
    df.assemble(vform, tensor=_vec)
    df.assemble(H0_form, tensor=H0)
    bc.zero(H0)
    bc.zero_columns(H0, _vec, 0)

    df.assemble(S_form, tensor=S)
    bc.zero(S)
    bc.zero_columns(S, _vec, 1)

    symmetrize(S.mat())
    symmetrize(H0.mat())
    logging.debug("  eigenproblem size: %d " % H0.size(0))

    # Set problem
    eigensolver.setProblemType(SLEPc.EPS.ProblemType.GHEP)
    eigensolver.setWhichEigenpairs(SLEPc.EPS.Which.SMALLEST_REAL)
    eigensolver.setOperators(H0.mat(), S.mat())
    
    # Set tolerance
    eigensolver.setConvergenceTest(SLEPc.EPS.Conv.REL)
    eigensolver.setTolerances(tol=kwargs.get('eigensolver_tol'),
                              max_it=kwargs.get('eigensolver_max_iterations'))

    # Set how many eigenpairs
    eigensolver.setDimensions(nev=how_many)

    # Set inner product to the one induced by S
    bv = eigensolver.getBV()
    bv.setMatrix(S.mat(), False)
    
    def monitor(eps, it, nconv, eig, errest):
        logging.debug("Iteration %d" % it)
        logging.debug("    eigenvalues:")
        for i in range(how_many):
            logging.debug("      %g ± %.2g" % (np.real(eig[i]), errest[i]))
    eigensolver.setMonitor(monitor)
    eigensolver.setFromOptions()
    eigensolver.setUp()
    logging.debug("    using solver " + eigensolver.getType())
    eigensolver.solve()

    logging.debug("  ... exiting eigensolver")

    if eigensolver.getConverged() < how_many:
            raise RuntimeError("Could not solve requested amount of eigenstates")
    # Prepare return data, note that we expect only real-valued output
    eigenvalues = np.empty(how_many, dtype=float)
    eigenstates = np.empty(how_many, dtype=df.Function)

    for i in range(how_many):
        psi = df.Function(FS)
        psivec = get_petsc_vec(psi)

        E = eigensolver.getEigenpair(i, Vr=psivec)
        comm.Barrier()
        eigenvalues[i] = np.real(E)

        # Create an empty function and swap its data pointer
        # with the one from our eigensolver

        # Update our vector swap
        psi.vector().apply('')
        # Normalize the state

        psivec /= np.sqrt(wfnorm(psi))
        psi.vector().apply('')

        eigenstates[i] = psi

    comm.Barrier()

    logging.debug("... exiting TISE solver")

    return eigenvalues, eigenstates


def load_tise_states(comm: MPI.Comm,
                     num_states: Union[int, type(np.inf)],
                     functionspace: Tuple[str, int],
                     path: Text = 'data') -> Tuple[df.Mesh, df.FunctionSpace,
                                                   np.array, np.array]:
    """
    Loads states computed for time-independent Schrödinger equation

    Parameters
    ----------
    num_states : int
        Number of states to load
    functionspace : (name, int)
        Functionspace of the computed states
    comm : mpi communicator

    Returns
    -------
    mesh : df.Mesh
    Vtise : df.FunctionSpace
    energies : np.ndarray of floats
    states : list of df.Function(Vtise)
    """

    assert isinstance(num_states, int) or np.isinf(num_states)

    logging.debug("Loading previously computed solutions of TISE")
    mesh = load_mesh(comm, path+'/tise_mesh.h5')

    Vtise = df.FunctionSpace(mesh, functionspace[0], functionspace[1])

    tise_states = load_function_collection(comm,
                                           path+'/tise_states.h5',
                                           Vtise)

    energies = np.array(np.loadtxt(path + '/tise_eigenvalues'))
    if np.isinf(num_states):
        num_states = energies.size
        if len(energies.shape) != 0:
            energies = energies[:num_states]
    return mesh, Vtise, energies,\
                         [val for val in tise_states.values()][:num_states] 
