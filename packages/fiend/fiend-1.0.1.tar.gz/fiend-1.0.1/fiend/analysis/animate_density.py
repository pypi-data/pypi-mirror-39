import argparse
import configparser
import os
from glob import glob
import numpy as np
import h5py

import dolfin as df
import ufl
from mpi4py import MPI

from fiend.utils.petsc_utils import petsc_vecload
from fiend.analysis._unit_conversions import conversion_factors as cf
from fiend.analysis._visualization_utils import plot_scalarfield
from fiend.utils.misc import parse_functionspace_argument
from fiend.utils.dolfin import load_function
from fiend.utils.mesh import load_mesh

import progressbar
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from matplotlib.animation import FuncAnimation, writers



def animate_density():
    """Animates the electron density"""

    parser = argparse.ArgumentParser(
        description=("Animates the electron density"),
        argument_default=argparse.SUPPRESS
    )

    parser.add_argument("--tps", type=int,
                        default=100,
                        help=("Sets how many units of time shoud be show in "
                              "one second"),
                        )

    parser.add_argument("--log_scale", action='store_true',
                        default=False,
                        help=("Draws the electron density in "
                              "logarithmic scale.")
                        )

    parser.add_argument("--save", action='store_true',
                        help=("Save the animation instead of "
                              "visualizing it interactively."),
                        default=False
                        )

    parser.add_argument("--radius", type=float,
                        default=np.inf,
                        help=("Maximum radius to draw"),
                        )

    parser.add_argument("--vmin_cap", type=float,
                        default=1e-8,
                        help=("Caps low end of datarange in log scale to this"
                              "value."))
    parser.add_argument("--skip_steps", type=int,
                        default=0,
                        help=("How many timesteps to skip between frames"))

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


    # Parse some simulation parameters
    config = configparser.ConfigParser()
    try:
        config.read("data/config")
        tise_config = config['TDSE parameters']
        prop_config = config['PROPAGATION parameters']
    except BaseException:
        print("No config data, exiting...")
        exit(1)

    # Construct the functionspace
    fs = parse_functionspace_argument(tise_config['functionspace'])
    mesh = load_mesh(MPI.COMM_WORLD, 'data/tdse_mesh.h5')

    V = df.FunctionSpace(mesh, fs[0], fs[1])

    # Load data
    with h5py.File('data/tdse_observables.h5', 'r') as f:
        time = f['time'][::(args['skip_steps'] + 1)]
        norm = f['norm'][::(args['skip_steps'] + 1)]

    dt = time[1] - time[0]

    filenames = sorted(glob('data/tdse_wavefunction/realpart_iteration_[!final]*_real'),
                       key=lambda t: int(t.split('_')[3]))[::(1 + args['skip_steps'])]

    interval = dt / args['tps'] * 1000

    # Setup figure and axes for plotting
    w, h = plt.figaspect(1.4)
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_subplot(111)
    ax.set_xlabel(r'$\rho$ (a.u.)')
    ax.set_ylabel(r'$z$ (a.u.)')

    if args['log_scale']:
        norm = LogNorm()
    else:
        norm = Normalize()

    # Draw the first frame and initialize all objects
    filepath = filenames[0]
    i = int(filepath.split('_')[3])
    wf_re = load_function(filepath, V)
    wf_im = load_function(
        'data/tdse_wavefunction/imagpart_iteration_%d_real' % i,
        V
    )
    ax.set_title('T=%.2f' % time[i])
    dens = df.project(ufl.algebra.Abs(wf_re)**2 + ufl.algebra.Abs(wf_im)**2, V)
    densplot, triang= plot_scalarfield(
        ax, dens, log_scale=args['log_scale'], vmin_cap=args['vmin_cap'], norm=norm)
    ax.set_aspect(1)
    cbar = fig.colorbar(densplot)
    cbar.set_label(r'$\vert \psi(\rho,z,t) \vert^2$')
    def update_func(filepath, *fargs):
        frame_number = int(filepath.split('_')[3])
        try:
            wf_re = load_function(filepath, V)
            wf_im = load_function(
                'data/tdse_wavefunction/imagpart_iteration_%d_real' % frame_number,
                V
            )
        except Exception as e:
            print("Error! Could not load wavefunction, iteration  %d"%frame_number)
            exit(1)
        ax.set_title('T=%.2f' %
                     time[frame_number // ((args['skip_steps'] + 1))])
        dens = df.project(ufl.algebra.Abs(wf_re)**2 +
                          ufl.algebra.Abs(wf_im)**2, V)

        densplot, _ = plot_scalarfield(
            ax, dens, log_scale=args['log_scale'], vmin_cap=args['vmin_cap'],
            triangulation = fargs[0], norm=norm)

    if not np.isinf(args['radius']):
        ax.set_xlim(0, args['radius'])
        ax.set_ylim(-args['radius'], args['radius'])

    pbar = progressbar.progressbar(filenames)

    ani = FuncAnimation(fig, update_func, frames=pbar, interval=interval,
                        fargs=(triang,),
                        blit=False, repeat=True)
    if args['save']:
        os.makedirs("data/figures/", exist_ok=True)
        ani.save("data/figures/density.mp4", fps=1 / interval)
    else:
        plt.show()


if __name__ == '__main__':
    animate_density()
