from collections import OrderedDict

import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI

import dolfin as df

from fiend.utils.misc import set_logging, fiend_setup
from fiend.utils.mesh import save_mesh, load_mesh
from fiend.tise.tise import solve_tise
from fiend.utils.dolfin import save_function_collection

from geometry import Nanotip
from parameters import *

# Setup logging of FIEND-library
master, rank, comm = fiend_setup(quadrature_degree=20)
set_logging(master, rank, False, True)

# System definition
# -----------------

nanotip = Nanotip(
                   apex_radius = apex_radius,
                   full_opening_angle = full_opening_angle
                 )  

mesh = nanotip.get_mesh(
                        boxsize = ti_boxsize,
                        refined_mesh_distance = ti_refined_mesh_distance,
                        transition_distance = ti_transition_distance,
                        cell_minrad = ti_cell_minrad,
                        cell_maxrad = ti_cell_maxrad,
                        vacuum_length = 40.0
                       )

pot_x_rho = nanotip.get_potential_times_rho(potential_drop = 0.2)

# Define Dirichlet boundaries
# ---------------------------
# :: every boundary except inside the tip and upper boundary ::
def dirichlet_boundary(x, on_boundary):
    return on_boundary and not df.near(x[0], 0.0) \
            and not df.near(x[1], ti_boxsize[1]/2.0)

# Solve TISE with QDYN's utilities
# --------------------------------
evals, evecs = solve_tise(mesh, ti_num_states, pot_x_rho,
           dirichlet_boundaries = [ dirichlet_boundary ],
           eigensolver_max_iterations=500000,
           eigensolver_tol=1e-10,
           eigensolver_type = 'krylovschur')

# Save eigenvalues
np.savetxt("data/tise_eigenvalues", evals)

# Save mesh
save_mesh('data/tise_mesh.h5', mesh)

# Save stationary states
save_function_collection('data/tise_states.h5',
                         OrderedDict(
                            [('state_%d'%i, evecs[i]) for i in
                             range(evals.size)] ))
