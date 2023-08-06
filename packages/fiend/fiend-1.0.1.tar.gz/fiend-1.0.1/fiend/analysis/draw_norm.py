import argparse
import os
import numpy as np
import h5py
from scipy.signal import stft
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec


from fiend.analysis._unit_conversions import conversion_factors as cf


def draw_norm():
    """Draws the wavefunction norm as a function of time."""

    parser = argparse.ArgumentParser(
        description=("Draws the wavefunction norm."),
        argument_default=argparse.SUPPRESS
    )

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


    with h5py.File('data/tdse_observables.h5', 'r') as f:
        time = f['time'][:]
        norm = f['norm'][:]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(time, norm)

    ax.set_xlabel(r'time (a.u.)')
    if args['latex']:
        ax.set_ylabel(r'$\vert \braket{\psi(t)}{\psi(t)} \vert^2$')
    else:
        ax.set_ylabel(r'total norm')

    if args['save']:
        os.makedirs("data/figures", exist_ok=True)
        plt.savefig("data/figures/norm.pdf")
    else:
        plt.show()


if __name__ == '__main__':
    draw_norm()
