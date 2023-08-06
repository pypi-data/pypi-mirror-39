import argparse
import os
from pathlib import Path
import numpy as np
import dolfin as df
from fiend.utils.mesh import load_mesh
import matplotlib.pyplot as plt

def draw_mesh():
    """Draws mesh"""
    comm = df.MPI.comm_world
    parser = argparse.ArgumentParser(
        description=("Draws the mesh."),
        argument_default=argparse.SUPPRESS
    )

    parser.add_argument("--which", type=str, default="tdse",
                        help=("Which mesh to visualize: tdse or tise.",
                             "Can also be a path to the mesh file"))
    parser.add_argument("--save", action='store_true',
                        help=("Save the figure instead of "
                              "visualizing it interactively."),
                        default=False
                        )

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


    mesh = df.Mesh()
    if args['which'].lower() == 'tise':
        mesh = load_mesh(comm, 'data/tise_mesh.h5')
    elif args['which'].lower() == 'tdse':
        mesh = load_mesh(comm, 'data/tdse_mesh.h5')
    elif Path(args['which']).exists() and Path(args['which']).is_file():
        mesh = load_mesh(comm, args['which'])
    else:
        raise TypeError("Simulation type '%s' is unknown." % args['which'])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    df.common.plotting.mplot_mesh(ax, mesh)
    ax.set_aspect(1)
    ax.set_xlabel(r'$\rho$ (a.u.)')
    ax.set_ylabel(r'$z$ (a.u.)')

    if args['save']:
        os.makedirs("data/figures", exist_ok=True)
        plt.savefig("data/figures/mesh.pdf")
    else:
        plt.show()


if __name__ == '__main__':
    draw_mesh()
