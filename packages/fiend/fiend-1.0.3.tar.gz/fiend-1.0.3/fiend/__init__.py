"""
FIEND is solver for time-dependent Schrödinger equation in cylindrically
symmetric systems. It's based on finite element discretization via the FEniCS
package and fast matrix-vector operations via PETSc and SLEPc.
"""

__author__ = 'Janne Solanpää'
__author_email__ = 'janne+fiend@solanpaa.fi'
__copyright__ = '© Janne Solanpää'
__credits__ = ''
__license__ = 'MIT License'
__version__ = '1.0.3'
__maintainer__ = 'Janne Solanpää'
__status__ = 'Production'
__name__ = 'fiend'
import sys
# Run default setup if possible. This may not be possible if we
# are just building the Docker containers on system without all the
# dependencies
try:
    import petsc4py
    try:
        idx = next(i for i,x in enumerate(sys.argv) if x=='PETSC_ARGS')
        petsc4py.init(sys.argv[idx+1:])
        sys.argv=sys.argv[:idx]
    except Exception as e:
        pass

    from fiend.utils.misc import fiend_setup

    fiend_setup()

    # FFC gives some futurewarnings, suppress those
    # https://stackoverflow.com/a/15778297
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
except BaseException:
    print("Default FIEND setup failed.")
