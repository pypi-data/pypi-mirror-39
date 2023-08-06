import argparse
import configparser
import os
from glob import glob
import progressbar

import numpy as np
import h5py
from mpi4py import MPI
import dolfin as df
import ufl

from fiend.analysis._unit_conversions import conversion_factors as cf
from fiend.utils.misc import parse_functionspace_argument
from fiend.tise.tise import load_tise_states
from fiend.analysis._visualization_utils import plot_scalarfield

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from matplotlib.animation import FuncAnimation, writers


def plot_state(state, number, energy, log_scale, max_radius, save, vmin_cap,
               triangulation):
    """Draws a new figure for state number 'state_nbr'"""
    if log_scale:
        norm = LogNorm()
    else:
        norm = Normalize()

    w, h = plt.figaspect(1.5)
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_subplot(111)
    ax.set_title('$E_%d = %g$' % (number, energy))
    ax.set_xlabel(r'$\rho$ (a.u.)')
    ax.set_ylabel(r'$z$ (a.u.)')
    dens = df.project(ufl.algebra.Abs(state)**2, state.function_space())
    p, tri = plot_scalarfield(ax, dens, log_scale=log_scale,
                         vmin_cap=vmin_cap, norm=norm,
                         triangulation=triangulation)
    cbar = fig.colorbar(p)
    cbar.set_label(r'$\vert \psi(\rho, z)\vert^2$')

    if not np.isinf(max_radius):
        ax.set_xlim(0, max_radius)
        ax.set_ylim(-max_radius, max_radius)

    ax.set_aspect(1)

    fig.tight_layout()
    if save:
        os.makedirs("data/figures/", exist_ok=True)
        fig.savefig('data/figures/state_%d.pdf' % number)
    return tri

def draw_stationary_states():
    """Animates the electron density"""

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
                        help=("Caps low end of datarange in log scale to this"
                              "value."))
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
        tise_config = config['TISE parameters']
    except BaseException:
        raise RuntimeError("No config data from a TISE simulation.")

    fs = parse_functionspace_argument(tise_config['functionspace'])

    # Load all computed stationary states
    _, funspace, energies, states = load_tise_states(MPI.COMM_WORLD,
                                                     num_states=np.inf,
                                                     functionspace=fs,
                                                     path='data/')
    tri = None
    for i, state in enumerate(progressbar.progressbar(states)):
        try:
            energy = energies[i]
        except:
            energy = energies
        tri = plot_state(state, i, energy, args['log_scale'], args['radius'],
                   args['save'], args['vmin_cap'], tri)
        if args['save']:
            plt.close(plt.gcf())
    if not args['save']:
        plt.show()


if __name__ == '__main__':
    draw_stationary_states()
