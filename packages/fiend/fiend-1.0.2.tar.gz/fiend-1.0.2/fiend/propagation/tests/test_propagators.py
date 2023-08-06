"""
Tests for propagators
"""
import unittest

from mpi4py import MPI
import numpy as np

from fiend.propagation.propagators import *
from fiend.propagation.propagation_utils import load_representation
from fiend.utils.petsc_utils import petsc_vecload, petsc_matload

from petsc4py import PETSc
is_petsc_real = isinstance(PETSc.ScalarType(), np.floating)


@unittest.skipIf(is_petsc_real, "No propagation tests without complex PETSc")
class PropagationTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.comm = MPI.COMM_WORLD

        # Load states
        self.psi_1s = petsc_vecload('data/tdse_state_0_cplx', self.comm)
        self.psi_2s = petsc_vecload('data/tdse_state_1_cplx', self.comm)
        self.energies = [-0.5, -0.125]
        self.H0 = petsc_matload('data/tdse_H0_cplx', self.comm)
        self.S = petsc_matload('data/tdse_S1_cplx', self.comm)

        self.Z = petsc_matload('data/tdse_Z_cplx', self.comm)

        self.wrkvec = self.S.getVecRight()

    def propagator_test(self, propagator):

        def exact_solution(t):
            vec = self.S.getVecRight()
            vec.setValues(range(vec.size),
                          1 / np.sqrt(2) * np.exp(-1j * t *
                                                  self.energies[0]) * self.psi_1s
                          + 1 / np.sqrt(2) * np.exp(-1j * t *
                                                    self.energies[1]) * self.psi_2s
                          )
            vec.assemble()
            return vec

        def post_step_handler(ts):
            psi_exact = exact_solution(ts.getTime())
            psi_numerical = ts.getSolution()
            self.S.mult(psi_numerical, self.wrkvec)
            overlap = self.wrkvec.dot(psi_exact)
            norm = self.wrkvec.dot(psi_numerical)
            print("t=%.2f err=%g normerr=%g" % (ts.getTime(), np.fabs(np.abs(overlap) - 1),
                                                np.fabs(np.abs(norm) - 1.0)))
            self.assertTrue(np.fabs(np.abs(overlap) - 1.0) < 1e-4)
            self.assertTrue(np.fabs(np.abs(norm) - 1.0) < 1e-4)

        propagator.set_post_step_handler(post_step_handler)
        psi0 = exact_solution(0.0)
        propagator.propagate(psi0)

    def test_crank_nicolson_propagator(self):
        def laserfield(t):
            return 0.0

        propagator = PETScPropagator(self.S, self.H0, self.Z, laserfield,
                                     propagatortype='cn',
                                     delta_t=0.05,
                                     max_t=100,
                                     hamiltonian_tolerance=1e-16,
                                     inverse_tolerance=1e-22,
                                     ilu_factor_levels=3)
        self.propagator_test(propagator)

    def test_alpha_propagator(self):
        def laserfield(t):
            return 0.0

        propagator = PETScPropagator(self.S, self.H0, self.Z, laserfield,
                                     propagatortype='alpha',
                                     delta_t=0.05,
                                     max_t=100,
                                     hamiltonian_tolerance=1e-16,
                                     inverse_tolerance=1e-22,
                                     ilu_factor_levels=3)
        self.propagator_test(propagator)

    @unittest.skip("EXPMID propagator not working.")
    def test_expmid_propagator(self):
        def laserfield(t):
            return 0.0
        import logging
        logging.getLogger('').setLevel(logging.DEBUG)
        propagator = KrylovPropagator(self.S, self.H0, self.Z, laserfield,
                                      delta_t=0.1,
                                      max_t=100,
                                      solver_type='superlu',
                                      matexp_tolerance=1e-16,
                                      inverse_tolerance=1e-22,
                                      ilu_factor_levels=3)

        self.propagator_test(propagator)
