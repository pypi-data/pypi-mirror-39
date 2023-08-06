"""
This script demonstrates how to compute the spatial dependence of an electric
field around a metal nanotip in the quasistatic approximation.

All the values are in Hartree atomic units.
"""
import numpy as np
#import matplotlib.pyplot as plt

from mpi4py import MPI

import dolfin as df

from fiend.utils.misc import set_logging, fiend_setup
from fiend.utils.mesh import save_mesh
from fiend.utils.dolfin import save_function_collection, project_cylindrical
from geometry import Nanotip
from parameters import *

# Setup logging of FIEND-library 
master, rank, comm = fiend_setup()
set_logging(master, rank, False, True)

# System definition
# -----------------
nanotip = Nanotip(
                   apex_radius = apex_radius,
                   full_opening_angle = full_opening_angle
                 )  

mesh = nanotip.get_mesh(
                        boxsize = f_boxsize,
                        refined_mesh_distance = f_refined_mesh_distance,
                        transition_distance = f_transition_distance,
                        cell_minrad = f_cell_minrad,
                        cell_maxrad = f_cell_maxrad
                       )

# Finite element description of the PDE
# -------------------------------------
functionspace = df.VectorFunctionSpace(mesh, 'Lagrange', 1, dim=2)

vr, vi = df.TestFunctions(functionspace)
ur, ui = df.TrialFunctions(functionspace)
rho, z = df.SpatialCoordinate(mesh)

# Definitions of various parts of the mesh
# ----------------------------------------
#
# inside tip '1'
# vacuum '0'
subdomains = df.MeshFunction("size_t", mesh, mesh.topology().dim())
subdomains.set_all(0)

class Tip(df.SubDomain):

    def inside(self, x, on_boundary):
        return nanotip._is_inside_tip(x[0], x[1])

tip = Tip()
tip.mark(subdomains, 1)

# Selection of the boundary parts for Dirichlet BCs
# -------------------------------------------------
#
# :: bottom of the simulation box and on the vacuum side boundary ::
class DirichletBoundary(df.SubDomain):
    def inside(self, x, on_boundary):
        return on_boundary and not df.near(x[0], 0.0) \
                and not df.near( x[1], f_boxsize[1]/2)

# Boundary value 
# --------------
# The boundary value is set so that the resulting electric field
# faraway from the nanostructure should be 1 a.u. 
boundary_value = df.Expression(('x[1]', '0.0' ), degree=1)

dbc = DirichletBoundary()
bc = df.DirichletBC( functionspace, boundary_value, dbc )

# Weak form of the complex-valued PDE for the electric potential
# --------------------------------------------------------------
dx = df.dx( domain = mesh, subdomain_data = subdomains )
F = eps_vacuum * (
            df.inner( df.grad(vr), df.grad(ur) ) \
          + df.inner( df.grad(vi), df.grad(ui) ) \
          + df.inner( df.grad(vr), df.grad(ui) ) \
          - df.inner( df.grad(vi), df.grad(ur) )
                  ) * rho * dx(0) \
    + eps_tip_re * (
            df.inner( df.grad(vr), df.grad(ur) ) \
          + df.inner( df.grad(vi), df.grad(ui) ) \
          + df.inner( df.grad(vr), df.grad(ui) ) \
          - df.inner( df.grad(vi), df.grad(ur) )
                  ) * rho * dx(1) \
    + eps_tip_im * (
            df.inner( df.grad(vr), df.grad(ur) ) \
          + df.inner( df.grad(vi), df.grad(ui) ) \
          - df.inner( df.grad(vr), df.grad(ui) ) \
          + df.inner( df.grad(vi), df.grad(ur) )
                  ) * rho * dx(1) 
 
zero = (vr+vi) * df.Constant(0.0) * df.dx

# The solution will be saved here
potential = df.Function(functionspace)

# Solve the PDE
df.solve(F == zero, potential, bc)

# Compute the electric field
E = -1*df.grad(potential[0])

# Scalar functionspace
Vflat = df.FunctionSpace(mesh, 'Lagrange', 1)

# Compute certains aspects of the electric field
Ure = df.project(potential[0], Vflat)
#project_cylindrical(potential[0], Vflat)
Uim = df.project(potential[1], Vflat)
#project_cylindrical(potential[1], Vflat)
Erho = df.project(E[0], Vflat)
#project_cylindrical(E[0], Vflat)
Ez = df.project(E[1], Vflat)
#project_cylindrical(E[1], Vflat)
EnormSQR = df.project(E[0]**2+E[1]**2, Vflat)
#project_cylindrical( E[0]**2+E[1]**2, Vflat)
Enorm = df.project(df.sqrt(E[0]**2+E[1]**2), Vflat)
#project_cylindrical( df.sqrt(E[0]**2+E[1]**2), Vflat)
# Save the mesh and the electric field components to files
save_mesh('data/poisson_mesh.h5', mesh)

save_function_collection('data/electric_field.h5',
                         {'Ure' : Ure,
                          'Uim' : Uim,
                          'E_rho' : Erho,
                          'E_z' : Ez,
                          'EnormSQR' : EnormSQR,
                          'Enorm' : Enorm
                         })
