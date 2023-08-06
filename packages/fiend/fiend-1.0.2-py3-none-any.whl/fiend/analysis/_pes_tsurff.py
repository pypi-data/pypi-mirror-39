"""
Assuming laser field is ~ linearly polarized in the z-direction in the
surface region
"""
import configparser
import logging
import sys
import os
import psutil
import re

import progressbar
import numpy as np
from scipy.integrate import quad, simps
from mpi4py import MPI

from petsc4py import PETSc

import dolfin as df
from fiend.utils.petsc_utils import petsc_vecload, petsc_matload
from fiend.utils.misc import parse_functionspace_argument
from fiend.utils.mesh import mesh_of_sphere_in_cylindrical_coordinates\
    as get_mesh
from fiend.utils.mesh import load_mesh, save_mesh, curve_mesh,\
    extract_equiradial_shell, remesh_function

from fiend.utils.dolfin import save_and_convert_to_complex, project_fast,\
    get_petsc_vec, load_function, project_cylindrical
from fiend.utils.mpi import get_num_processes_on_this_node
from fiend.pulseconfig_parser.parser import parse_laser
from fiend.pulseconfig_parser.laser import Laser


def compute_vectorpotential_and_integrals(comm, time, Afield):
    # Precompute field integrals
    time_indices = np.arange(0, time.size, 1, dtype=int)
    time_indices_for_this_process = np.array_split(time_indices,
                                                   comm.size)[comm.rank]
    T0 = time[0]
    Aint = np.zeros_like(time)
    A2int = np.zeros_like(time)
    for i in time_indices_for_this_process:
        if i == 0:
            t0 = T0
        else:
            t0 = time[i - 1]
        t = time[i]

        Aint[i] = quad(Afield, t0, t)[0]
        A2int[i] = quad(lambda tau: Afield(tau)**2, t0, t)[0]

    Aint = np.cumsum(comm.allreduce(sendobj=Aint, op=MPI.SUM))
    A2int = np.cumsum(comm.allreduce(sendobj=A2int, op=MPI.SUM))
    Avals = Afield(time)
    return Avals, Aint, A2int


def compute_prefactor(krho: float,
                      kz: float,
                      t: float,
                      T0: float,
                      Aint: float,
                      A2int: float,
                      radius: float):
    k2 = krho * krho + kz * kz
    phi = 0.5 * k2 * (t - T0) + 0.5 * Aint * kz + 0.5 * A2int
    return (2 * np.pi)**(-3.0 / 2.0) * np.exp(1j * phi)


def compute_instantaneous_amplitude_wo_prefactor(
        coskr,
        sinkr,
        β,
        ψ_re,
        ψ_im,
        grad_ψ_re,
        grad_ψ_im,
        normal):

    ρ, z = df.SpatialCoordinate(ψ_re.function_space().mesh())
    r = df.sqrt(ρ * ρ + z * z)

    comm = ψ_re.function_space().mesh().mpi_comm()
    real_part = df.Scalar(comm)
    imag_part = df.Scalar(comm)
    nβ = df.inner(normal, β)
    df.assemble(
        ρ * (coskr * nβ * ψ_re
             + sinkr * nβ * ψ_im
             + 0.5 * coskr * df.inner(normal, grad_ψ_im)
             - 0.5 * sinkr * df.inner(normal, grad_ψ_re)
             ) * df.dx, real_part)

    df.assemble(
        ρ * (coskr * nβ * ψ_im
             - sinkr * nβ * ψ_re
             - 0.5 * sinkr * df.inner(normal, grad_ψ_im)
             - 0.5 * coskr * df.inner(normal, grad_ψ_re)
             ) * df.dx, imag_part)

    return real_part.get_scalar_value() \
        + 1j * imag_part.get_scalar_value()


def _compute_derivatives(function, sfunspace, lfunspace,
                         sfunspace2, lfunspace2):
    sfun = df.project(function, sfunspace)
    lfun = remesh_function(lfunspace, sfun)

    grad_sfun = project_cylindrical(df.grad(sfun), sfunspace2)
    grad_lfun = remesh_function(lfunspace2, grad_sfun)

    return lfun, grad_lfun


def get_facet_normal(linemesh: df.Mesh) -> df.Function:
    """
    Returns a function on 2-component DG function that evaluates
    to the outward pointing facet normal on the line mesh embedded in R^2.
    """

    # See
    # https://bitbucket.org/fenics-project/dolfin/issues/53/dirichlet-boundary-conditions-of-the-form
    vertices = linemesh.coordinates()

    cells = linemesh.cells()
    tangent_vecs = vertices[cells[:, 1]] - vertices[cells[:, 0]]

    def rotate90_and_normalize(tv):
        norm = np.sqrt(tv[0]**2 + tv[1]**2)
        return np.array([tv[1], -tv[0]]) / norm
    normal_vecs = np.array([rotate90_and_normalize(tv) for tv in tangent_vecs])
    linemesh.init_cell_orientations(df.Expression(('x[0]', 'x[1]'), degree=1))
    normal_vecs[linemesh.cell_orientations() != 1] *= -1
    V = df.VectorFunctionSpace(linemesh, 'DG', degree=0, dim=2)
    normal = df.Function(V)
    nv = normal.vector()
    for n in (0, 1):
        dofmap = V.sub(n).dofmap()
        for i in range(dofmap.global_dimension()):
            dof_indices = dofmap.cell_dofs(i)
            assert len(dof_indices) == 1
            nv[dof_indices[0]] = normal_vecs[i, n]
    return normal


class photoelectron_amplitude(df.UserExpression):
    """
    A class for computing the momentum-space scattering amplitude b(k)
    and projecting it to a functionspace
    """

    def __init__(self, comm, tsurff_radius, num_angles, rfunspace, T0, time,
                 saveslot_indices, Avals, Aint, A2int, 
                 custom_load_function = None, **kwargs):
        r"""
        comm : MPI.Communicator
            Communicator for internal computations. You should really use
            MPI.COMM_SELF here
        rfunspace : dolfin.FunctionSpace
            Functionspace for the wavefunction
        T0 : float
            Time of the beginning of the laser pulse
        time : np.array of floats
            Array of times
        saveslot_indices : np.array of ints
            Array of ints corresponding to the saveslot for times
        Aint : np.array of floats
            Array of \int_T0^t A(τ) dτ with t corresponding to times in the
            'time' argument
        A2int : np.array of floats
            Array of \int_T0^t A(τ)^2 dτ with t corresponding to times in the
            'time' argument
        """
        self.rfunspace = rfunspace
        self.Avals = Avals
        self.Aint = Aint
        self.A2int = A2int
        self.T0 = T0
        self.time = time
        self.comm = comm
        self.saveslot_indices = saveslot_indices
        self.tsurff_radius = tsurff_radius

        # Expressions needed for computing instantaneous amplitude
        logging.info("Extracting surface region cells from mesh.")

        m = re.match(r"FiniteElement\('(?P<name>[a-zA-Z]*)', (?P<meshtype>[a-zA-Z]*), (?P<degree>[0-9])\)",
                     self.rfunspace.element().signature())

        function_name = m.group('name')

        degree = int(m.group('degree'))

        self.surfacemesh = extract_equiradial_shell(self.rfunspace.mesh(),
                                                    self.tsurff_radius)

        self.surfacefunspace = df.FunctionSpace(self.surfacemesh,
                                                function_name, degree)
        logging.info(
            "Functionspace successfully constructed for the surface region.")

        def path(s):
            return self.tsurff_radius * np.array([np.sin(np.pi * s),
                                                  np.cos(np.pi * s)]).T

        logging.info("Constructing 1D mesh on the spherical surface")
        self.linemesh = curve_mesh(path, num_angles)
        self.line_elem = df.FiniteElement('Lagrange',
                                          self.linemesh.ufl_cell(),
                                          1)
        self.linefunspace = df.FunctionSpace(self.linemesh, self.line_elem)
        self.surfacefunspace_vec = df.VectorFunctionSpace(self.surfacemesh,
                                                          function_name,
                                                          degree=degree, dim=2)

        self.linefunspace_vec = df.VectorFunctionSpace(self.linemesh,
                                                       function_name,
                                                       degree=degree, dim=2)

        self.surface_normal = get_facet_normal(self.linefunspace.mesh())

        # Load wavefunctions and their gradients
        # (and keep only the part that's on the surface)
        logging.info("Loading wavefunctions")

        self.psi_re = np.empty(self.saveslot_indices.size, dtype=df.Function)
        self.psi_im = np.empty(self.saveslot_indices.size, dtype=df.Function)
        self.grad_psi_re = np.empty(self.saveslot_indices.size,
                                    dtype=df.Function)
        self.grad_psi_im = np.empty(self.saveslot_indices.size,
                                    dtype=df.Function)

        if self.comm.rank == 0:
            my_ssi_iterable = progressbar.progressbar(self.saveslot_indices)
        else:
            my_ssi_iterable = self.saveslot_indices

        if custom_load_function:
            function_loader = custom_load_function
        else:
            function_loader = load_function

        for ssi, saveslot_nbr in enumerate(my_ssi_iterable):

            self.psi_re[ssi], self.grad_psi_re[ssi] = _compute_derivatives(
                function_loader(
                    'data/tdse_wavefunction/realpart_iteration_%d_real' % saveslot_nbr,
                    self.rfunspace),
                self.surfacefunspace,
                self.linefunspace,
                self.surfacefunspace_vec,
                self.linefunspace_vec
            )

            self.psi_im[ssi], self.grad_psi_im[ssi] = _compute_derivatives(
                function_loader(
                    'data/tdse_wavefunction/imagpart_iteration_%d_real' % saveslot_nbr,
                    self.rfunspace),
                self.surfacefunspace,
                self.linefunspace,
                self.surfacefunspace_vec,
                self.linefunspace_vec
            )

        logging.info("Wavefunctions loaded")
        super().__init__(**kwargs)

    def value_shape(self):
        return (2,)

    def eval(self, values, x):
        logging.debug("Computing k=(%.2f,%.2f)" % (x[0], x[1]))
        krho = x[0]
        kz = x[1]

        rho, z = df.SpatialCoordinate(self.linefunspace)

        kr = df.Constant(krho) * rho + df.Constant(kz) * z
        coskr = df.cos(kr)
        sinkr = df.sin(kr)

        bkt = np.zeros_like(self.time, dtype=complex)

        for i, t in enumerate(self.time):
            Aint = self.Aint[i]
            A2int = self.A2int[i]
            beta = df.Constant((0.5 * krho, 0.5 * kz + self.Avals[i]))

            saveslot = self.saveslot_indices[i]

            # Compute prefactor
            prefactor = compute_prefactor(krho, kz, t, self.T0, self.Aint[i],
                                          self.A2int[i], self.tsurff_radius)
            # Compute instantaneous amplitude
            bkti_wo_prefactor = compute_instantaneous_amplitude_wo_prefactor(
                coskr,
                sinkr,
                beta,
                self.psi_re[i],
                self.psi_im[i],
                self.grad_psi_re[i],
                self.grad_psi_im[i],
                self.surface_normal
            )
            bkt[i] = prefactor * bkti_wo_prefactor

        bk = simps(bkt, self.time)
        values[0] = np.real(bk)
        values[1] = np.imag(bk)


def compute_pes(comm, Emax, dE, dp, tsurff_radius,
                num_angle_pts, skip_steps=0):
    """
    Computes the photoelectron spectrum from a previous
    propagation simulation based on the method introduced in
    PRA 71, 012712 (2005)
    """
    # Convert energy to momentum
    pmax = np.sqrt(2 * Emax)

    # Create p-mesh
    logging.debug('Creating p-mesh')
    pmesh = get_mesh(pmax, pmax, pmax, dp, dp)
    elem = df.FiniteElement("Lagrange", pmesh.ufl_cell(), 1)
    pfunspace = df.FunctionSpace(pmesh, elem * elem)
    arpes_space = df.FunctionSpace(pmesh, elem)

    # Load propagation parameters
    logging.debug('Loading propagation parameters')
    config = configparser.ConfigParser()
    try:
        config.read("data/config")
        tise_config = config['TDSE parameters']
        prop_config = config['PROPAGATION parameters']
    except BaseException:
        raise RuntimeError("No config data from a propagation simulation")

    # Load laser vector potential
    Afield = parse_laser('data/laser')

    T0 = Afield.beginning_of_pulse()
    Tmax = Afield.end_of_pulse()
    dt = (prop_config.getfloat('delta_t') *
          prop_config.getint('save_interval'))
    time = np.arange(T0, Tmax, dt)

    saveslot_indices = np.arange(0, time.size,
                                 1,
                                 dtype=int)

    # Check if we want to skip a few saved timesteps when computing PES
    time = time[::(skip_steps + 1)]
    saveslot_indices = saveslot_indices[::(skip_steps + 1)]

    logging.debug('Precomputing integrals of the vector potential')
    Avals, Aint, A2int = compute_vectorpotential_and_integrals(comm,
                                                               time,
                                                               Afield)
    logging.debug("Generating function space for wavefunctions")
    rmesh = load_mesh(MPI.COMM_SELF, 'data/tdse_mesh.h5')

    fs = parse_functionspace_argument(tise_config['functionspace'])
    rfunspace = df.FunctionSpace(rmesh, fs[0], fs[1])

    # Compute ARPES b(k)
    bp = photoelectron_amplitude(comm,
                                 tsurff_radius,
                                 num_angle_pts,
                                 rfunspace,
                                 T0,
                                 time,
                                 saveslot_indices,
                                 Avals,
                                 Aint,
                                 A2int)
    logging.debug("Computing angle-integrated spectrum")
    energies = np.arange(0, Emax, dE)

    delta_angle = np.pi / comm.size
    my_angles = [comm.rank * delta_angle, (comm.rank + 1) * delta_angle]

    def get_pes(energy, angles):
        kr = np.sqrt(2 * energy)

        def integrand(th):
            tmp = [0, 0]
            krho = kr * np.sin(th)
            kz = kr * np.cos(th)
            bp.eval(tmp, [krho, kz])
            return tmp[0]**2 + tmp[1]**2
        if kr == 0:
            return 0.0
        else:
            return quad(integrand, angles[0], angles[1])[0]

    eiterable = progressbar.progressbar(energies, redirect_stdout=True,
                                        redirect_stderr=True) if comm.rank == 0 else energies

    pes = np.array([get_pes(E, my_angles) for E in eiterable])

    pes = comm.allreduce(sendobj=pes, op=MPI.SUM)

    logging.debug("Dimension of P-functionspace: %d" % pfunspace.dim())

    bp_fun = project_cylindrical(bp, pfunspace)

    logging.debug(
        "Scattering amplitudes successfully computed, saving them...")

    # Save ARPES and mesh to file
    save_mesh('data/postprocessing/pmesh.h5', pmesh)

    save_and_convert_to_complex(comm, 'data/postprocessing/bp', bp_fun)

    ARPES_fun = project_cylindrical(bp[0]**2 + bp[1]**2, arpes_space)

    return ARPES_fun, energies, pes
