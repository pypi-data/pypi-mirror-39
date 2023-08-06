"""
This script demonstrates how to compute the spatial dependence of an electric
field around a metal nanotip in the quasistatic approximation.

All the values are in Hartree atomic units.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpi4py import MPI

import dolfin as df
import os
from geometry import Nanotip
from fiend.utils.misc import set_logging, fiend_setup
from fiend.utils.mesh import load_mesh
from fiend.utils.dolfin import load_function_collection
import fiend.analysis._visualization_utils as vu

# Setup logging of FIEND-library 
master, rank, comm = fiend_setup()
set_logging(master, rank, False, True)

poisson_mesh = load_mesh(comm, 'data/poisson_mesh.h5')

poisson_funspace = df.FunctionSpace(poisson_mesh, 'Lagrange', 1)

funs = load_function_collection(comm, 'data/electric_field.h5', poisson_funspace)

# Load fancy matplotlib
#try:
#    import matplotlib.style
#    matplotlib.style.use(os.path.dirname(os.path.abspath(vu.__file__))+"/custom.mplparams")
#except:
#    pass

gc = GridSpec(1,2,width_ratios=[0.9,0.1], left=0.26, right=0.85 )

fig = plt.figure(figsize=(2.46,4))
ax = fig.add_subplot(gc[0])
p, _ = vu.plot_scalarfield(ax, funs['Enorm'])

cax = fig.add_subplot(gc[1])
cbar = fig.colorbar(p, cax=cax)
cbar.set_label('field enhancement factor')
#ax.set_xlim((0,500))
#ax.set_ylim((-500,500))
ax.set_xlabel(r'$\rho$ (a.u.)')
ax.set_ylabel(r'$z$ (a.u.)')

plt.show()
#plt.savefig('electric_field.pdf')
