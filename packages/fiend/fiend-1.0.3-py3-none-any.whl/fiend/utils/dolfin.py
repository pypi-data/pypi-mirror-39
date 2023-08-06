"""
Tools that simplify working with Dolfin.
"""
import re
from typing import Text, Union, List, Dict

from collections import OrderedDict

import numpy as np
from mpi4py import MPI
from petsc4py import PETSc
import dolfin as df
import h5py

from fiend.utils.petsc_utils import petsc_vecload, petsc_save,\
    petsc_convert_to_complex
from fiend.utils.mesh import extract_equiradial_shell, curve_mesh
from fiend.utils.misc import triangle_incenter

def project_cylindrical(v,
                        V: df.FunctionSpace,
                        v_includes_rho : bool = False) -> df.Function:
    """
    A fast projection of expression/function 'v' onto functionspace V.
    Uses a user-supplied solver and a preconditioning matrix.

    Parameters
    ----------
    v : df.Function or df.Expression
        Function to project
    V : df.FunctionSpace
        Functionspace where we project
    v_includes_rho : bool
        True if user has passed v*rho instead of v to the function
    Returns
    -------
    funout : df.Function
        The projection
    """
    dx = df.dx(V.mesh())
    rho, z = df.SpatialCoordinate(V.mesh())
    w = df.TestFunction(V)
    Pv = df.TrialFunction(V)
    a = df.inner(w, Pv) * rho* dx
    if v_includes_rho:
        L = df.inner(w, v) * rho * dx
    else:
        L = df.inner(w, v) * dx
    funout = df.Function(V)
    df.solve(a == L, funout)

    return funout


def project_fast(v,
                 V: df.FunctionSpace,
                 funout: df.Function,
                 wrkmat: df.PETScMatrix,
                 wrkvec: df.PETScVector,
                 ksp: PETSc.KSP,
                 pcmat: PETSc.Mat) -> df.Function:
    """
    A fast projection of expression/function 'v' onto functionspace V.
    Uses a user-supplied solver and a preconditioning matrix.

    Parameters
    ----------
    v : df.Function or df.Expression
        Function to project
    V : df.FunctionSpace
        Functionspace where we project
    funout : df.Function
        The projected function will be saved here
    wrkmat : df.PETScMatrix
    wrkvec : df.PETScVector
    ksp : petsc4py.PETSc.KSP
        Preset ksp-instance
    pcmat : petsc4py.PETSc.Mat
        Preconditioner matrix

    Returns
    -------
    funout : df.Function
        The projection
    """
    rho, z = df.SpatialCoordinate(V)
    w = df.TestFunction(V)
    Pv = df.TrialFunction(V)
    a = df.inner(w, Pv) * rho * df.dx
    L = df.inner(w, v) * rho * df.dx

    df.assemble_system(a, L, A_tensor=wrkmat, b_tensor=wrkvec)

    A = wrkmat.mat()
    b = wrkvec.vec()
    ksp.setOperators(A, pcmat)

    ksp.setUp()
    res = funout.vector().vec()
    ksp.solve(b, res)

    return funout

def extract_arcspaces(functionspace, radius, num_angles=None):
    """Extracts cells that are on a circle of radius R and forms a new
    (compatible) functionspace on the new mesh. Creates also a 1D mesh on the
    circular arc and a corresponding functionspace."""

    mesh = functionspace.mesh()

    assert mesh.mpi_comm().size == 1, "Arc extraction not supported for parallel meshes"

    smesh = extract_equiradial_shell(mesh, radius)
    m = re.match("FiniteElement\('(?P<family>[a-zA-Z]*)', (?P<meshtype>[a-zA-Z]*), (?P<degree>[0-9])\)",
                 functionspace.element().signature())
    family = m.group('family')
    degree = int(m.group('degree'))

    sfunctionspace = df.FunctionSpace(smesh, family, degree)

    if not num_angles:
        num_angles = smesh.num_cells()

    # Find the highest and lowest cell on smesh
    highest = max(df.cells(smesh),
                  key=lambda c: triangle_incenter(
        np.array(c.get_vertex_coordinates()).reshape(3, 2))[1])
    lowest = min(df.cells(smesh),
                 key=lambda c: triangle_incenter(
        np.array(c.get_vertex_coordinates()).reshape(3, 2))[1])
    hvtxs = np.array(highest.get_vertex_coordinates()).reshape(3, 2)
    hangles = [np.arctan2(v[1], v[0]) for v in hvtxs]

    lvtxs = np.array(lowest.get_vertex_coordinates()).reshape(3, 2)
    langles = [np.arctan2(v[1], v[0]) for v in lvtxs]

    langle = np.min(langles)
    hangle = np.max(hangles)
    arcangle = (hangle - langle)

    # Create the corresponding 1D mesh
    def path(s):
        return radius * np.array([
            np.sin(np.pi / 2 - hangle + s * arcangle),
            np.cos(np.pi / 2 - hangle + s * arcangle)
        ]).T

    lmesh = curve_mesh(path, num_angles)

    # Create the correspondung functionspace
    lfunctionspace = df.FunctionSpace(lmesh, family, degree)

    return lfunctionspace, sfunctionspace


def load_function(filename: Text,
                  funspace: df.FunctionSpace) -> df.Function:
    """
    Loads a dolfin function whose degrees of freedom have been saved as a PETSc
    binary file.

    Parameters
    ----------
    filename : str
        Filename where the function DOF have been saved
    funspace : df.FunctionSpace
        Functionspace corresponding to the DOF
    """
    comm = funspace.mesh().mpi_comm()
    vec = petsc_vecload(filename, comm)
    fun = df.Function(funspace, df.PETScVector(vec))
    return fun

def save_function_collection(filename : Text,
                    fields : Dict[Text, df.Function]):
    """
    Saves a collection of dolfin functions to a HDF5-file.

    Parameters
    ----------
    filename : str
        Filepath where we save the functions
    fields : dict
        Dictionary of function names and the functions
        that will be saved in the file
    """
    fun1 = next(iter(fields.values()))
    comm = fun1.function_space().mesh().mpi_comm()
    with df.HDF5File(comm, filename, 'w') as savefile:
        for name, field in sorted(fields.items(), key=lambda t: t[0]):
            savefile.write(field, name)

def load_function_collection(comm: MPI.Comm, filename : Text, 
                             funspace : df.FunctionSpace):
    """
    Saves a collection of dolfin functions to a HDF5-file.

    Parameters
    ----------
    comm : mpi4py.MPI.Comm
    filename : str
        Filepath from where we load the functions
    funspace : df.Functionspace

    Returns
    -------
    dictionary of df.Functions found in the hdf5 file
    """
    with h5py.File(filename, 'r', driver='mpio', comm=comm) as datafile:
        keys=[k for k in datafile.keys()]
    
    funs = {}

    with df.HDF5File(comm, filename, 'r') as savefile:
        for name in keys:
            tmp = df.Function(funspace)
            savefile.read(tmp, name)
            funs[name]=tmp

    return OrderedDict(sorted(funs.items(), key=lambda t: t[0]))
            

def save_and_convert_to_complex(comm: MPI.Comm,
                                filename: Text,
                                field: Union[df.Function, PETSc.Vec]):
    """
    Saves DOFs of a function to PETSc binary file.

    Parameters
    ----------
    comm : MPI.Comm
        Communicator of the processes who share the function
    filename : str
        Savepath
    field : df.Function or PETSc.Vec
        The function/field to be saved
    """
    if isinstance(field, df.Function):
        field = get_petsc_vec(field)

    petsc_save(filename, field, comm)
    if comm.Get_rank() == 0:
        petsc_convert_to_complex(filename)


def get_petsc_vec(function: df.Function) -> PETSc.Vec:
    """
    Obtains the underlying vector of the FE representation of the input
    function.

    Parameters
    ----------
    function : df.Function

    Returns
    -------
    backend_vector (should be petsc4py.PETSc.Vec)
    """
    return df.as_backend_type(function.vector()).vec()


def wfnorm(psi: df.Function) -> float:
    """
    Computes the norm of the function in cylindrical coodinates.

    Parameters
    ----------
    psi : df.Function

    Returns
    -------
    float
    """
    # Extract mesh
    mesh = psi.function_space().mesh()
    x = df.SpatialCoordinate(mesh)
    rho = x[0]
    z = x[1]
    return df.assemble(psi * psi * rho * df.dx)


def normalize(psi: df.Function) -> None:
    """Normalizes a function wrt. to the norm induced by our inner product."""
    psivec = psi.vector()
    psivec /= np.sqrt(wfnorm(psi))
    psivec.apply('')


def default_dirichlet_boundary(x: Union[List[float], np.array],
                       on_boundary: bool) -> bool:
    """
    """
    return on_boundary and not df.near(x[0], 0)

class dirichlet_boundary(df.SubDomain):
    """Subdomain for marking Γ_D"""
    def _inside_nodirichlet(self, x, on_boundary):
        return False

    def _inside_default(self, x, on_boundary):
        return default_dirichlet_boundary(x, on_boundary)

    def _inside_custom(self, x, on_boundary):
        return np.any([bfun(x, on_boundary) for bfun in self.dirichlet_boundaries])

    def __init__(self, dirichlet_boundaries):
        self.dirichlet_boundaries = dirichlet_boundaries
        if not self.dirichlet_boundaries:
            self.inside = self._inside_default
        else:
            if len(dirichlet_boundaries) == 0:
                self.inside = self._nodirichlet
            else:
                self.inside = self._inside_custom
        super().__init__()

class rhozero_boundary(df.SubDomain):
    """Subdomain class for marking ρ=0"""
    def inside(self, x, on_b):
        return on_b and df.near(x[0], 0.0)

class neumann_boundary(df.SubDomain):
    """Subdomain class for marking Γ_N"""
    def __init__(self, dirichlet_boundary):
        self.dirichlet_boundary = dirichlet_boundary
        super().__init__()

    def inside(self, x, on_boundary):
        return on_boundary and not df.near(x[0], 0.0)\
               and not self.dirichlet_boundary.inside(x, on_boundary)

def get_boundary_markers(mesh, dirichlet_boundaries = None):
    """
    Returns a MeshFunction that marks boundary at ρ=0 with 0,
    dirichlet boundary Γ_D with 1, and neumann boundary Γ_N with 2.
    All other facets are marked with 3.
    """
    boundaries = df.MeshFunction("size_t", mesh, mesh.topology().dim()-1)
    boundaries.set_all(3)
    rhozero_boundary().mark(boundaries, 0)
    db = dirichlet_boundary(dirichlet_boundaries)
    nb = neumann_boundary(db)
    nb.mark(boundaries, 2)
    db.mark(boundaries, 1)
    return boundaries

