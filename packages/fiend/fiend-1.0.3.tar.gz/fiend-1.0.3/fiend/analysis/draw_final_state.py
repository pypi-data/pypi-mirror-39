import argparse
import configparser
import os
from glob import glob

import numpy as np
import h5py
from mpi4py import MPI
import dolfin as df
import ufl

from fiend.analysis._unit_conversions import conversion_factors as cf
from fiend.pulseconfig_parser.parser import parse_laser
from fiend.utils.misc import parse_functionspace_argument
from fiend.analysis._visualization_utils import plot_scalarfield
from fiend.utils.mesh import load_mesh
from fiend.utils.dolfin import load_function

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from matplotlib.animation import FuncAnimation, writers


def draw_snapshot():
    """Plots a snapshopt of the electron density"""

    parser = argparse.ArgumentParser(
        description=("Visualizes the stationary states"),
        argument_default=argparse.SUPPRESS
    )

    parser.add_argument("--log_scale", action='store_true',
                        default=False,
                        help=("Draws the electron density in "
                              "logarithmic scale.")
                        )

    parser.add_argument("--save", action='store_true',
                        help=("Save the figures instead of"
                              "visualizing them interactively."),
                        default=False
                        )

    parser.add_argument("--radius", type=float,
                        default=np.inf,
                        help=("Maximum radius to draw"),
                        )
    parser.add_argument("--vmin_cap", type=float,
                        default=1e-10,
                        help=("Caps data-range of log-scale density"
                              "from below to this value."))
    parser.add_argument("--latex", action="store_true",
                        help="Enables Latex",
                        default = False)

    parser.add_argument("--mpl_backend", type=str,
                        help="Matplotlib backend to use")


    args = vars(parser.parse_args())
    # Setup matplotlib backend 
    if args['save']:
        plt.switch_backend('Agg')
    else:
        try:
            plt.switch_backend(args['mpl_backend'])
        except:
            ...
    
    # Try to load matplotlib style file
    if args['latex']:
        try:
            import matplotlib.style
            scriptdir = os.path.dirname(os.path.abspath(__file__))
            matplotlib.style.use(scriptdir + '/custom.mplparams')
        except BaseException:
            ...

     # Load TISE config
    config = configparser.ConfigParser()
    try:
        config.read("data/config")
        tdse_config = config['TDSE parameters']
        prop_config = config['PROPAGATION parameters']
    except BaseException:
        raise RuntimeError("Missing config data.")

    fs = parse_functionspace_argument(tdse_config['functionspace'])
    mesh = load_mesh(MPI.COMM_SELF, 'data/tdse_mesh.h5')

    funspace = df.FunctionSpace(mesh, fs[0], fs[1])
    # Compute the nearest saved iteration
    psi_re = load_function('data/tdse_wavefunction/realpart_iteration_final_real',
                           funspace)

    psi_im = load_function('data/tdse_wavefunction/imagpart_iteration_final_real',
                           funspace)

    if args['log_scale']:
        norm = LogNorm()
    else:
        norm = Normalize()

    w, h = plt.figaspect(1.5)
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_subplot(111)
    ax.set_title('$t = $ final')
    ax.set_xlabel(r'$\rho$ (a.u.)')
    ax.set_ylabel(r'$z$ (a.u.)')
    dens = df.project(ufl.algebra.Abs(psi_re)**2
                      + ufl.algebra.Abs(psi_im)**2,
                      funspace)
    p, _ = plot_scalarfield(
        ax, dens, args['log_scale'], args['vmin_cap'], norm=norm)
    cbar = fig.colorbar(p)
    cbar.set_label(r'$\vert \psi(\rho, z, t)\vert^2$')
    max_radius = args['radius']
    if not np.isinf(max_radius):
        ax.set_xlim(0, max_radius)
        ax.set_ylim(-max_radius, max_radius)

    ax.set_aspect(1)

    fig.tight_layout()
    if args['save']:
        os.makedirs("data/figures/", exist_ok=True)
        fig.savefig('data/figures/snapshot_final.pdf')

    plt.show()


if __name__ == '__main__':
    draw_snapshot()
