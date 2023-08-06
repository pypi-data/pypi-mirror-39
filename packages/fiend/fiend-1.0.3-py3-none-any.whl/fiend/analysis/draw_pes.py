import progressbar
import argparse
from mpi4py import MPI
import os
import fiend.analysis._pes_tsurff
from fiend.utils.misc import fiend_setup, set_logging


def compute_pes_main():
    """
    Computes angle-resolved photoelectron spectrum from
    an existing simulation. Note that the wavefunctions need to have
    been saved.
    """
    progressbar.streams.wrap_stderr()
    # Command line interface
    parser = argparse.ArgumentParser(
        description=("Draws the angle integrated"
                     "photoelectron spectrum."),
        argument_default=argparse.SUPPRESS
    )

    parser.add_argument("--max_energy", type=float, default=10)
    parser.add_argument("--delta_energy", type=float, default=0.2)
    parser.add_argument("--delta_p", type=float, default=0.3)
    parser.add_argument("--tsurff_radius", type=float)
    parser.add_argument("--num_angle_pts", type=int, default=300)
    parser.add_argument("--skip_steps", type=int, default=0)

    parser.add_argument("--save", action='store_true',
                        help=("Save the figure instead of "
                              "visualizing it interactively."),
                        default=False
                        )
    parser.add_argument("--debug", action='store_true', default=False)
    parser.add_argument("--debug_master", action='store_true', default=False)
    parser.add_argument("--latex", action="store_true",
                        help="Enables Latex",
                        default = False)


    parser.add_argument("--mpl_backend", type=str,
                        help="Matplotlib backend to use")


    args = vars(parser.parse_args())

    # Setup fiend and loggnig
    master, rank, comm = fiend_setup()
    set_logging(master, rank, args['debug'], args['debug_master'])

    # Setup matplotlib backend 
    if master:
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



    # Compute PES and ARPES
    arpes_fun, energies, pes = fiend.analysis._pes_tsurff.compute_pes(
        comm,
        args['max_energy'],
        args['delta_energy'],
        args['delta_p'],
        args['tsurff_radius'],
        args['num_angle_pts'],
        args['skip_steps']
    )
    # Only master process should draw the figures
    if master:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(energies, pes)
        ax.set_yscale('log')
        ax.set_xlabel('energy (a.u.)')
        ax.set_ylabel('PES')

        if args['save']:
            os.makedirs("data/figures", exist_ok=True)
            plt.savefig("data/figures/pes_capsurff.pdf")
        else:
            plt.show()

    comm.Barrier()


if __name__ == '__main__':
    compute_pes_main()
