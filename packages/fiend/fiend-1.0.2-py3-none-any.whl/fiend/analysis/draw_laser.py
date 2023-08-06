import os

import h5py
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import cumtrapz
import numpy as np


def draw_laser():
    """
    Draws the laser vector potential and electric field as a function of time
    """
    try:
        import matplotlib.style
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        matplotlib.style.use(scriptdir + '/custom.mplparams')
    except BaseException:
        ...

    # Load data
    with h5py.File('data/tdse_observables.h5', 'r') as savefile:
        time = savefile['time'][:]
        try:
            vecpot = savefile['laser_vector_potential'][:]
            efield = - np.gradient(vecpot) / (time[1] - time[0])
            vptime = time
            etime = time
        except BaseException:
            efield = savefile['laser_electric_field'][:]
            vecpot = cumtrapz(efield, time)
            vptime = time[1:]
            etime = time

    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.set_xlabel(r'time (a.u.)')
    ax.set_ylabel(r'efield (a.u.)')
    ax.plot(etime, efield)

    ax2 = fig.add_subplot(212, sharex=ax)
    ax2.set_xlabel(r'time (a.u.)')
    ax2.set_ylabel(r'vector potential (a.u.)')

    ax2.plot(vptime, vecpot)

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    draw_laser()
