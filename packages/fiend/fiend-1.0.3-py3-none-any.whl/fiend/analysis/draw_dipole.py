import argparse
import os

import numpy as np
import h5py
from scipy.signal import stft
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

from fiend.analysis._unit_conversions import conversion_factors as cf


def draw_dipole():
    """Draws the dipole moment, dipole spectrum, and
    spectrogram."""

    parser = argparse.ArgumentParser(
        description=("Draws the dipole moment, its fourier "
                     "transformation, and spectrogram."),
        argument_default=argparse.SUPPRESS
    )

    parser.add_argument("--save", action='store_true',
                        help=("Save the figure instead of "
                              "visualizing it interactively."),
                        default=False
                        )
    parser.add_argument("--stft-window-length", type=float,
                        default=1 / cf.au_in_fs,
                        help=("Window length of the "
                              "stft (in atomic units of time).")
                        )
    parser.add_argument("--stft-overlap-length", type=float,
                        help=("Overlap of two stft windows "
                              "(in atomic units of time).")
                        )
    parser.add_argument("--max-energy", type=float,
                        help="Maximum energy for visualization")

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


    if 'stft_overlap_length' not in args:
        args['stft_overlap_length'] = args['stft_window_length'] / 3. * 2

    with h5py.File('data/tdse_observables.h5', 'r') as f:
        time = f['time'][:]
        dipole = f['dipole_z'][:]

    dt = time[1] - time[0]

    w, h = plt.figaspect(1.4)
    fig = plt.figure(figsize=(w, h))

    gs_overview = GridSpec(1, 2, fig, width_ratios=[18, 1], wspace=0.02,
                           top=0.99, right=0.85, left=0.18, bottom=0.1)

    gs = GridSpecFromSubplotSpec(3, 1, gs_overview[0], hspace=0.3)
    gs_cbars = GridSpecFromSubplotSpec(3, 1, gs_overview[1], hspace=0.3)

    # Draw the dipole as a function of time
    ax1 = plt.subplot(gs[0])
    ax1.plot(time, dipole)
    ax1.set_xlabel(r'time (a.u.)')
    ax1.set_ylabel(r'$\mel*{\psi(t)}{\hat{z}}{\psi(t)}$ (a.u.)')

    ax1.set_xlim(time[0], time[-1])

    # Draw the dipole spectrum
    # D(w)

    Dw = np.fft.rfft(dipole, norm='ortho')
    w = 2 * np.pi * np.fft.rfftfreq(n=len(dipole), d=time[1] - time[0])

    ax2 = plt.subplot(gs[1])
    ax2.plot(w, np.abs(Dw)**2)

    ax2.set_xlabel(r'energy (a.u.)')
    ax2.set_ylabel(r'$\vert D_z(\omega) \vert^2$ (a.u.)')

    if 'max_energy' in args:
        ax2.set_xlim(w.min(), args['max_energy'])
    else:
        ax2.set_xlim(w.min(), w.max())

    ax2.set_yscale('log')

    # Draw the stft

    nperseg = int(args['stft_window_length'] / dt)
    noverlap = int(args['stft_overlap_length'] / dt)
    f, t, S = stft(x=dipole, fs=1 / dt, window='hann',
                   nperseg=nperseg, noverlap=noverlap)

    w = 2 * np.pi * f

    ax3 = plt.subplot(gs[2], sharex=ax1)

    p = ax3.pcolormesh(t, w, np.abs(S)**2, cmap='viridis', rasterized=True)

    ax3.set_xlabel(r'time (a.u.)')
    ax3.set_ylabel(r'energy (a.u.)')

    # Plot the colorbar
    cax = plt.subplot(gs_cbars[2])
    cbar = plt.colorbar(p, cax=cax)
    cbar.set_label(r'Spectral intensity')

    if 'max_energy' in args:
        ax3.set_ylim(w.min(), args['max_energy'])

    if args['save']:
        os.makedirs("data/figures", exist_ok=True)
        plt.savefig("data/figures/dipole.pdf")
    else:
        plt.show()


if __name__ == '__main__':
    draw_dipole()
