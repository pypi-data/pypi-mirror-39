"""
Setup of matrices and vectors for time propagation.
"""

import logging
import numpy as np
from collections import OrderedDict

from mpi4py import MPI
from petsc4py import PETSc

import dolfin as df

from fiend.utils.misc import fiend_setup, set_logging
from fiend.utils.dolfin import get_petsc_vec,\
        load_function_collection,save_function_collection, normalize,\
        project_cylindrical
from fiend.utils.mesh import save_mesh, remesh_function,\
                load_mesh
from fiend.utils.petsc_utils import petsc_save, petsc_convert_to_complex
from fiend.tise.tise import load_tise_states
from fiend.tdse.tdse import tdse_setup, plasmonic_vectorpotential_setup,\
                           save_tdse_preparation, save_and_convert_to_complex

from geometry import Nanotip
from parameters import *

# Set form compiler parameters and logging
# ----------------------------------------

master, rank, comm = fiend_setup(quadrature_degree=6)

set_logging(master, rank, False, True)

# Setup the system for TDSE
# -------------------------

nanotip = Nanotip(
                   apex_radius = apex_radius,
                   full_opening_angle = full_opening_angle
                 )  


mesh = nanotip.get_mesh(
                        boxsize = td_boxsize,
                        refined_mesh_distance = td_refined_mesh_distance,
                        transition_distance = td_transition_distance,
                        cell_minrad = td_cell_minrad,
                        cell_maxrad = td_cell_maxrad
                       )

pot_x_rho = nanotip.get_potential_times_rho(work_function)

# Load TISE mesh and states
# ------------------------

tise_mesh, Vtise, _, tise_states = load_tise_states(comm,
                                                    ti_num_states, 
                                                    ('Lagrange', 1))

# Interpolate our TISE solution to the new functionspace for TDSE
# ---------------------------------------------------------------

V = df.FunctionSpace(mesh, 'Lagrange', 1)
states = np.empty(ti_num_states, dtype=df.Function)
for i in range(ti_num_states):
    states[i] = remesh_function(V, tise_states[i])
    normalize(states[i])


# Prepare a custom initial state
# ------------------------------

logging.info("Preparing a custom initial state")

rho, z = df.SpatialCoordinate(mesh)
sigma = 50
z0 = 150
ini_state = project_cylindrical(df.exp(-(rho*rho+(z-z0)*(z-z0))/(2*sigma**2)), V)
normalize(ini_state)


# Define Dirichlet boundaries
# ---------------------------

def dirichlet_boundary(x, on_boundary):
    return on_boundary and not df.near(x[0], 0.0) \
            and not df.near(x[1], td_boxsize[1]/2.0)

pot_x_rho = df.project(pot_x_rho, V)

# Define a signed distance function for complex absorbing boundary
# ----------------------------------------------------------------

a = td_boxsize[0]
b = td_boxsize[1]/2
c2 = a**2-b**2 

def isinside_domain(x):
    """Returns true if point is inside the CAP surface, false otherwise."""
    rho, z = x
    if rho >= a:
        return False
    else:
        rth = np.arccos(rho/a)
        ze = b*np.sin(rth)
        if -ze <= z <= ze:
            return True
        else:
            return False

def sgn(x):
    if isinside_domain(x):
        return -1
    else:
        return 1

def signed_distance(x):
    """Returns signed distance to the CAP surface"""
    rho, z = x
    if z >= 0:
        return rho-a
    r = np.sqrt(rho*rho+z*z)
    t = np.roots([z*b, 2*rho*a+2*c2, 0, 2*rho*a-2*c2, -z*b])
    cos = (1-t**2)/(1+t**2)
    sin = 2*t/(1+t**2)
    d2 = (rho-a*cos)**2+(z-b*sin)**2
    d2 = np.real(d2[np.isreal(d2)])
    r = np.sqrt(np.min(d2))*sgn(x)
    return r


# Obtain matrices for TDSE
# ------------------------

S, S0, S1, H0, partialRho, partialZ,  Rho, Z, CAP, ACC, NMAT = \
    tdse_setup( mesh,
                pot_x_rho,
                td_cap_height, td_cap_width,
                ('Lagrange', 1),
                dirichlet_boundaries = [dirichlet_boundary],
                cap_sdistance_function = signed_distance
               )

logging.info("Saving files...")

# Save matrices and wavefunctions to file
# ---------------------------------------

save_tdse_preparation(comm, mesh, [ini_state], H0, S, S0, S1, partialRho, partialZ,
                      Rho, Z, CAP, ACC, NMAT)

# Load the spatial profile of the electric field
# ----------------------------------------------

logging.info("Loading electric field spatial profile...")

poisson_mesh = load_mesh(comm, 'data/poisson_mesh.h5')
poisson_funspace = df.FunctionSpace(poisson_mesh, 'Lagrange', 1)

Efuns = load_function_collection(comm, 'data/electric_field.h5', poisson_funspace)

# Set up plasmonic interaction operator for use within TDSE
# ----------------------------------------------------------
Erho = Efuns['E_rho']
Ez = Efuns['E_z']
Erho_tdse = remesh_function(V, Efuns['E_rho'])
Ez_tdse = remesh_function(V, Efuns['E_z'])
Enorm_sqr_tdse = remesh_function(V, Efuns['EnormSQR'])

Ap, Asqr = plasmonic_vectorpotential_setup(mesh, ('Lagrange', 1), Erho_tdse,
                                                         Ez_tdse,
                                                         Enorm_sqr_tdse,
                                                         dirichlet_boundaries=[dirichlet_boundary]) 

save_and_convert_to_complex(comm, "data/tdse_Ap", Ap)
save_and_convert_to_complex(comm, "data/tdse_Asqr", Asqr)

logging.debug("Exiting...")
