"""
Methods for assembling FE matrices for propagating TDSE
"""

import logging
from typing import Union, Tuple, Text

import numpy as np

from mpi4py import MPI
from petsc4py import PETSc
from typing import List

import dolfin as df
from fiend.utils.dolfin import save_and_convert_to_complex, get_petsc_vec,\
    get_boundary_markers, wfnorm
from fiend.utils.petsc_utils import petsc_save, petsc_convert_to_complex,\
        symmetrize, antisymmetrize
from fiend.tdse.absorbing_boundaries import *
from fiend.utils.mesh import save_mesh

def tdse_setup(mesh: df.Mesh,
               pot_x_rho,
               cap_height: float,
               cap_width: float,
               funspace: df.FunctionSpace,
               **kwargs):
    r"""
    Initial setup before time-dependent simulation

    Parameters
    ----------
    mesh : df.Mesh
        Mesh of the (ρ,z)-halfplane
    pot_x_rho_expr : str
        String that defines potential⋅ρ. This string needs
        to be a valid C-syntax.
    cap_height : float
        Height of the complex absorbing potential
    cap_width : float
        Width of the complex absorbing potential
    functionspace : (str, int)
            Which functionspace to use. Name and degree
    **kwargs:
        dirichlet_boundaries : list of functions
            These functions mark the boundaries where we impose zero
            dirichlet boundary conditions.
        
    Returns
    -------
    Smat : petsc4py.PETSc.Mat
        Overlap matrix
    H0mat : petsc4py.PETSc.Mat
        Time-independent Hamiltonian
    partialZmat : petsc4py.PETSc.Mat
        <m|\partial_z|n>
    Zmat : petsc4py.PETSc.Mat
        <m|z|n>
    CAPmat : petsc4py.PETSc.Mat
        <m|CAP|n>
    """

    comm = mesh.mpi_comm()

    logging.info('Entering TDSE setup')

    radius = 0.0
    for vertex in df.vertices(mesh):
        point = vertex.point()
        radius = max([point.distance(df.Point(0.0, 0.0)), radius])

    radius = comm.allreduce(radius, op=MPI.MAX)

    FS = df.FunctionSpace(mesh, funspace[0], funspace[1])

    zero = df.Constant('0.0')

    boundaries = get_boundary_markers(mesh, kwargs.get('dirichlet_boundaries', None))
    ds = df.Measure("ds")(subdomain_data=boundaries)
    n = df.FacetNormal(mesh)
    bc = df.DirichletBC(FS, df.Constant(0.0), boundaries, 1)

    x = df.SpatialCoordinate(mesh)
    rho = x[0]
    z = x[1]

    v = df.TestFunction(FS)
    psi = df.TrialFunction(FS)

    # Define the weak formulation

    # Overlap between basis functions
    S_form = v * psi * rho * df.dx

    # Time-independent Hamiltonian matrix H0
    T_form = 0.5 * df.dot(df.grad(v), df.grad(psi)) * rho * df.dx

    V_form = pot_x_rho * v * psi * df.dx

    # Note correct partialRho for getting hermitian operator
    partialRho_form = v * df.Dx(psi, 0) * rho * df.dx +\
        0.5*v*psi*df.dx-0.5*v*psi*n[0]*rho*ds
    
    partialZ_form = v * df.Dx(psi, 1) * rho * df.dx \
        - 0.5*v*psi*n[1]*rho*ds

    Rho_form = v * psi * rho * rho * df.dx

    Z_form = v * psi * rho * z * df.dx

    if 'cap_sdistance_function' in kwargs:
        logging.info("Using a custom CAP shape")
        capfun = get_cap_from_signed_distance(kwargs.get('cap_sdistance_function'), cap_width, cap_height)
    else:
        logging.info("Using default CAP shape")
        capfun = get_cap(radius, cap_width, cap_height, mesh)

    CAP_form = v * capfun * psi * rho * df.dx

    ACC_form = - v * df.Dx(pot_x_rho, 1) * psi * df.dx

    comm.Barrier()

    logging.info('Assembling matrices for TDSE')

    # Assemble the matrices
    S = df.PETScMatrix()

    T = df.PETScMatrix()
    V = df.PETScMatrix()

    partialRho = df.PETScMatrix()
    partialZ = df.PETScMatrix()
    Rho = df.PETScMatrix()
    Z = df.PETScMatrix()

    CAP = df.PETScMatrix()
    ACC = df.PETScMatrix()

    logging.info("Assembling overlap")
    df.assemble(S_form, tensor=S)
    Smat = S.mat()
    S1mat = Smat.duplicate(copy=True)
    S0mat = Smat.duplicate(copy=True)
    S1 = df.PETScMatrix(S1mat)
    S0 = df.PETScMatrix(S0mat)
    _dummyvec = df.PETScVector()
    df.assemble(v*df.Constant(0.0)*df.dx, tensor=_dummyvec)
    bc.zero(S1)
    bc.zero(S0)
    bc.zero_columns(S1, _dummyvec, 1.0)
    bc.zero_columns(S0, _dummyvec, 0.0)

    logging.info("Assembling kinetic energy")
    df.assemble(T_form, tensor=T)
    bc.zero(T)
    bc.zero_columns(T, _dummyvec, 0.0)

    logging.info("Assembling static potential")
    df.assemble(V_form, tensor=V)
    bc.zero(V)
    bc.zero_columns(V, _dummyvec, 0.0)

    logging.info(r"Assembling p_\rho")
    df.assemble(partialRho_form, tensor=partialRho)
    bc.zero(partialRho)
    bc.zero_columns(partialRho, _dummyvec, 0.0)

    logging.info("Assembing p_z")
    df.assemble(partialZ_form, tensor=partialZ)
    bc.zero(partialZ)
    bc.zero_columns(partialZ, _dummyvec, 0.0)

    logging.info(r"Assembling \rho")
    df.assemble(Rho_form, tensor=Rho)
    bc.zero(Rho)
    bc.zero_columns(Rho, _dummyvec, 0.0)

    logging.info(r"Assembling z")
    df.assemble(Z_form, tensor=Z)
    bc.zero(Z)
    bc.zero_columns(Z, _dummyvec, 0.0)

    logging.info("Assembling CAP")
    df.assemble(CAP_form, tensor=CAP)
    bc.zero(CAP)
    bc.zero_columns(CAP, _dummyvec, 0.0)

    logging.info("Assembling acceleration_z")
    df.assemble(ACC_form, tensor=ACC)
    bc.zero(ACC)
    bc.zero_columns(ACC, _dummyvec, 0.0)

    ds = df.Measure("ds")[boundaries]
    n = df.FacetNormal(mesh)

    logging.info("Assembling Neumann boundary corrector")
    neumann_form = v*df.inner(n, df.grad(psi))*ds(2)
    neumann_matrix = df.PETScMatrix()
    df.assemble(neumann_form, tensor=neumann_matrix)
    neumann_matrix= neumann_matrix.mat()
    comm.Barrier()

    # Extract the underlying PETSc matrices and
    # get rid of numerical noise causing unsymmetricity/unantisymmetricity
    Smat = symmetrize(Smat)
    S0mat = symmetrize(S0mat)
    S1mat = symmetrize(S1mat)
    Tmat = symmetrize(T.mat())
    Vmat = symmetrize(V.mat())
    partialRhomat = antisymmetrize(partialRho.mat())
    partialZmat = antisymmetrize(partialZ.mat())
    Rhomat = symmetrize(Rho.mat())
    Zmat = symmetrize(Z.mat())
    CAPmat = symmetrize(CAP.mat())
    ACCmat = symmetrize(ACC.mat())

    return Smat, S0mat, S1mat, Tmat + \
        Vmat, partialRhomat, partialZmat, Rhomat, Zmat, CAPmat, ACCmat,\
        neumann_matrix


def plasmonic_vectorpotential_setup(mesh: df.Mesh,
                                    funspace: df.FunctionSpace,
                                    Arho: df.Function,
                                    Az: df.Function,
                                    A_sqr: df.Function,
                                    **kwargs) -> Tuple[PETSc.Mat,
                                                       PETSc.Mat,
                                                       PETSc.Mat]:
    r"""
    Initial setup before time-dependent simulation

    Parameters
    ----------
    mesh : df.Mesh
        Mesh of the (ρ,z)-halfplane
    functionspace : (str, int)
        Which functionspace to use. Name and degree
    Arho : df.Function(functionspace)
        rho-component of the vector potential
    Az : df.Function(functionspace)
        z-component of the vector potential
    A_sqr : df.Function(functionspace)
        norm squared of the vector potential

    **kwargs:
        dirichlet_boundaries : list of functions
            These functions mark the boundaries where we impose zero
            dirichlet boundary conditions.

    Returns
    -------
    Arho*prho : petsc4py.PETSc.Mat
        Product of Arho and prho
    Az*pz : petsc4py.PETSc.Mat
        Product of Az and pz
    Asqr : petsc4py.PETSc.Mat
        <m|\partial_z|n>
    """

    comm = mesh.mpi_comm()

    logging.info('Entering TDSE setup')

    V = df.FunctionSpace(mesh, funspace[0], funspace[1])

    boundaries = get_boundary_markers(mesh, kwargs.get('dirichlet_boundaries', None))
    bc = df.DirichletBC(V, df.Constant(0.0), boundaries, 1)

    ds = df.Measure("ds")(subdomain_data=boundaries)
    n = df.FacetNormal(mesh)

    x = df.SpatialCoordinate(mesh)
    rho = x[0]
    z = x[1]

    v = df.TestFunction(V)
    psi = df.TrialFunction(V)

    Ap_form = 0.5 * v * psi * (Arho + rho * Arho.dx(0) + Az.dx(1) * rho)  * df.dx\
             + v * ( Arho * psi.dx(0) + Az * psi.dx(1) ) * rho * df.dx\
             - 0.5*v * psi * (Arho * n[0] + Az*n[1]) * rho * ds
    
    Asqr_form = 0.5 * v * A_sqr * psi * rho * df.dx

    logging.info('Assembling plasmonic interaction matrices for TDSE')

    # Assemble the matrices
    Ap = df.PETScMatrix()
    Asqr = df.PETScMatrix()
    _dummyvec = df.PETScVector()
    df.assemble(v*df.Constant(0.0)*df.dx, tensor=_dummyvec)

    df.assemble(Ap_form, tensor = Ap)
    bc.zero(Ap)
    bc.zero_columns(Ap, _dummyvec, 0.0)

    df.assemble(Asqr_form, tensor=Asqr)
    bc.zero(Asqr)
    bc.zero_columns(Asqr, _dummyvec, 0.0)

    # Extract the underlying PETSc matrices
    Apmat = Ap.mat()
    Asqrmat = Asqr.mat()
    # A^2 should be symmetric, get rid of unsymmetricity
    Apmat = antisymmetrize(Apmat)
    Asqrmat = symmetrize(Asqrmat)

    return Apmat, Asqrmat


def save_tdse_preparation(comm: MPI.Comm,
                          mesh: df.Mesh,
                          states: Union[List[df.Function], np.array,
                                        List[PETSc.Vec]],
                          H0: PETSc.Mat,
                          S: PETSc.Mat,
                          S0: PETSc.Mat,
                          S1: PETSc.Mat,
                          partialRho: PETSc.Mat,
                          partialZ: PETSc.Mat,
                          Rho: PETSc.Mat,
                          Z: PETSc.Mat,
                          ABS: PETSc.Mat,
                          ACC: PETSc.Mat,
                          NMAT : PETSc.Mat,
                          path: Text = 'data') -> None:

    save_mesh(path + '/tdse_mesh.h5', mesh)

    for i, state in enumerate(states):
        save_and_convert_to_complex(comm, path + "/tdse_state_%d" % i, state)

    save_and_convert_to_complex(comm, path + "/tdse_H0", H0)
    save_and_convert_to_complex(comm, path + "/tdse_S", S)
    save_and_convert_to_complex(comm, path + "/tdse_S0", S0)
    save_and_convert_to_complex(comm, path + "/tdse_S1", S1)
    save_and_convert_to_complex(comm, path + "/tdse_partialRho", partialRho)
    save_and_convert_to_complex(comm, path + "/tdse_partialZ", partialZ)
    save_and_convert_to_complex(comm, path + "/tdse_Rho", Rho)
    save_and_convert_to_complex(comm, path + "/tdse_Z", Z)
    save_and_convert_to_complex(comm, path + "/tdse_ABS", ABS)
    save_and_convert_to_complex(comm, path + "/tdse_ACC", ACC)
    save_and_convert_to_complex(comm, path + "/tdse_NMAT", NMAT)
